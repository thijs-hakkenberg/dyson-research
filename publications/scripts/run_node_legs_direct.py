"""
rq-0-52: settle the target count with the station's place fixed, by solving the leg
between the node and the edge of the Earth's sphere of influence for each tug leg.

    python run_cislunar_flyby_3d.py --station        # the sample of escapes used as seeds
    python run_node_legs_direct.py --orbit=halo-120 --phase0=0[,1,...] [--legs=pooled|station] [--window=10] [--cap=5.0] [--cycle=4.0] [--seconds=900]

Takes tug legs already solved against a reach table: the pooled halo table
(legs-flyby-3d-halo.csv; only targets that close there can close with the station's place
fixed) or, with --legs=station, this station's own table (legs-flyby-station-*.csv, which
run_trajectory_flyby_model.py --model=station-<orbit> regenerates). For every leg that is
part of a cycle within the caps, node_leg_direct.reachable finds whether the excess
velocity the leg uses can be delivered on that date, and if not, how much of it. Missing
excess speed is charged to the tug's thrusters one for one (an upper bound on its cost).
The escape may fall within `window` days of the date the leg was solved for; the
heliocentric leg is kept as solved.

Several station places can be given at once (--phase0=0,1,2,...,7); their legs share one
pool of workers. A leg is given at most --seconds of wall clock; the best found by then is
kept and the leg is marked timed_out.

Legs already solved for this place under other caps are reused (the solve does not depend
on the caps).

Writes publications/data/nea-trajectories/node-legs-direct-<orbit>-p<k>[-w<window>][-c<cap>-y<cycle>].json
(caps other than 5 km/s and 4 yr are tagged) and, per leg, node-legs-direct-<orbit>-p<k>[...]-legs.csv
(read by run_node_stations_direct.py).
"""

from __future__ import annotations

import csv
import json
import os
import sys
import time
from multiprocessing import Pool

import numpy as np

import node_leg_direct as d
from run_cislunar_flyby import OUT as CIS
from run_cislunar_flyby_3d import STATION_ORBITS, orbit_label
from run_trajectory_study import OUT

arg = lambda k, default: next((a.split('=')[1] for a in sys.argv if a.startswith(f'--{k}=')), default)
ORBIT = arg('orbit', 'halo-120')
PHASES = [int(p) for p in arg('phase0', '0').split(',')]
WINDOW = float(arg('window', '10'))
CAP = float(arg('cap', '5.0'))
CYCLE = float(arg('cycle', '4.0'))
MIN_STAY = 60.0
LEGS = arg('legs', 'pooled')  # pooled: legs solved against the pooled halo table; station: against this station's own table
SEEDS = int(arg('seeds', '3'))
SECONDS = float(arg('seconds', '900'))
LEG_COLUMNS = ('target', 'leg', 'burn_ms', 'budget', 'depart', 'tof', 'dv', 'vinf', 'lon', 'lat', 'allowance', 'delivered', 'dv_eff', 'node_T',
               'flight_days', 'burn_frac', 'escape_shift_days', 'runs', 'timed_out', 'seconds')
_ctx = {}


def load_legs(phase0):
    legs = {}
    name = 'legs-flyby-3d-halo.csv' if LEGS == 'pooled' else f'legs-flyby-station-{ORBIT}-p{phase0}.csv'
    for r in csv.DictReader(open(os.path.join(OUT, name))):
        legs.setdefault(r['target'], []).append({
            'target': r['target'], 'leg': r['leg'], 'burn_ms': int(r['burn_ms']), 'budget': float(r['budget_days']),
            'depart': d.J2000 + (float(r['depart_year']) - 2000.0) * 365.25, 'tof': float(r['tof_days']), 'dv': float(r['low_thrust_kms']),
            'vinf': float(r['vinf_kms']), 'lon': float(r['vinf_lon_deg']), 'lat': float(r['vinf_lat_deg']), 'allowance': float(r['allowance_days'])})
    return legs


def caps_tag(cap=None, cycle=None):
    cap, cycle = CAP if cap is None else cap, CYCLE if cycle is None else cycle
    return '' if (cap, cycle) == (5.0, 4.0) else f'-c{cap:g}-y{cycle:g}'


def pairs(outs, ins, cap, cycle, direct=False):
    """(cycle years, out, in) of every pair within the caps. direct: use the node dates found."""
    res = []
    for o in outs:
        if o['dv_eff' if direct else 'dv'] > cap:
            continue
        for i in ins:
            if i['dv_eff' if direct else 'dv'] > cap or i['depart'] < o['depart'] + o['tof'] + MIN_STAY:
                continue
            if direct:
                cyc = (i['node_T'] - o['node_T']) / 365.25
            else:
                cyc = (i['depart'] + i['tof'] + i['allowance'] - o['depart'] + o['allowance']) / 365.25
            if cyc <= cycle:
                res.append((cyc, o, i))
    return res


NUMERIC = {'burn_ms': int, 'runs': int}


def reuse(phase0):
    """Legs of this place already solved under other caps (same date, burn and window), by key.
    The solve does not depend on the caps, so they are taken as they are."""
    import glob
    done = {}
    for path in glob.glob(os.path.join(OUT, f'node-legs-direct-{ORBIT}-p{phase0}*-legs.csv')):
        if '-station-legs' in path or (WINDOW != 10) != ('-w' in os.path.basename(path)):
            continue
        for r in csv.DictReader(open(path)):
            row = {}
            for k, v in r.items():
                if k in ('target', 'leg'):
                    row[k] = v
                elif k == 'timed_out':
                    row[k] = v == 'True'
                elif v == '':
                    continue
                else:
                    row[k] = NUMERIC.get(k, float)(v)
            row['phase0'] = phase0
            done[key(row)] = row
    return done


def key(leg):
    return (leg['target'], leg['leg'], int(leg['burn_ms']), round(leg['depart'], 4), round(leg['tof'], 4), round(leg['vinf'], 4), round(leg['budget'], 1))


def setup():
    if not _ctx:
        kinds = [orbit_label(k, a) for k, a in STATION_ORBITS]
        kind, size = STATION_ORBITS[kinds.index(ORBIT)]
        orbit = d.NodeOrbit(kind, size)
        z = np.load(os.path.join(CIS, 'escapes-3d-station.npz'))
        _ctx.update(orbit=orbit, clouds={b: d.Cloud(z, b, kinds.index(ORBIT), orbit.period_days) for b in (150, 300)})
    return _ctx


def solve_leg(job):
    phase0, leg = job
    ctx = setup()
    out = leg['leg'] == 'out'
    T_earth = (leg['depart'] if out else leg['depart'] + leg['tof']) - d.J2000  # day the leg leaves or reaches the sphere of influence
    clocks = d.Clocks(phase0 / 8.0, ctx['orbit'].period_days)
    clocks = clocks if out else clocks.mirrored()
    t0 = time.time()
    v, sol, runs, timed_out = d.reachable(ctx['orbit'], ctx['clouds'][leg['burn_ms']], clocks, leg['lon'], leg['lat'], leg['vinf'], float(leg['burn_ms']),
                                          T_earth if out else -T_earth, WINDOW, leg['budget'], n_seeds=SEEDS, seconds=SECONDS)
    res = dict(leg, phase0=phase0, delivered=v, runs=runs, timed_out=timed_out, seconds=round(time.time() - t0, 1))
    if sol is not None:
        f = sol.flown
        burn_T = float(sol.x[0])
        res.update(dv_eff=leg['dv'] + (leg['vinf'] - v), flight_days=f.flight_days, burn_frac=f.burn_frac,
                   node_T=burn_T if out else -burn_T, escape_shift_days=(f.escape_T - (T_earth if out else -T_earth)) * (1 if out else -1),
                   plane_km=f.plane_km, moon_km=f.moon_km)
    else:
        res.update(dv_eff=np.inf, node_T=np.nan)
    return res


def main():
    jobs, base, reused = [], {}, []
    for phase0 in PHASES:
        done = reuse(phase0) if LEGS == 'pooled' else {}
        base[phase0] = {}
        for n, L in load_legs(phase0).items():
            outs, ins = [l for l in L if l['leg'] == 'out'], [l for l in L if l['leg'] == 'in']
            ps = pairs(outs, ins, CAP, CYCLE)
            if ps:
                base[phase0][n] = min(p[0] for p in ps)
                used = {id(p[1]): p[1] for p in ps} | {id(p[2]): p[2] for p in ps}
                for l in used.values():
                    if key(l) in done:
                        reused.append(dict(done[key(l)], **{k: l[k] for k in ('budget', 'tof', 'allowance')}))
                    else:
                        jobs.append((phase0, l))
    print(f'{ORBIT} phases {PHASES} window {WINDOW:g} d, legs <= {CAP:g} km/s, cycles <= {CYCLE:g} yr: {len(jobs)} legs to solve, {len(reused)} reused', flush=True)
    t0 = time.time()
    with Pool(min(9, os.cpu_count() or 2)) as pool:
        solved = list(reused)
        for k, r in enumerate(pool.imap_unordered(solve_leg, jobs, chunksize=1)):
            solved.append(r)
            if k % 25 == 24:
                print(f'{k + 1}/{len(jobs)} legs, {time.time() - t0:.0f}s', flush=True)
    for phase0 in PHASES:
        write(phase0, base[phase0], [r for r in solved if r['phase0'] == phase0], time.time() - t0)


def write(phase0, base, solved, seconds):
    by = {}
    for r in solved:
        by.setdefault(r['target'], []).append(r)
    targets = {}
    for n in sorted(base):
        L = by.get(n, [])
        ps = pairs([l for l in L if l['leg'] == 'out'], [l for l in L if l['leg'] == 'in'], CAP, CYCLE, direct=True)
        full = [l for l in L if l['delivered'] >= l['vinf'] - 0.005]
        targets[n] = {'table_cycle_yr': round(base[n], 3), 'legs_tried': len(L), 'legs_delivered_in_full': len(full),
                      'legs_delivered_in_part': sum(0 < l['delivered'] < l['vinf'] - 0.005 for l in L),
                      'out_legs_delivered': sum(l['delivered'] > 0 and l['leg'] == 'out' for l in L),
                      'in_legs_delivered': sum(l['delivered'] > 0 and l['leg'] == 'in' for l in L),
                      'direct_cycle_yr': round(min(p[0] for p in ps), 3) if ps else None}
    closing = [n for n, t in targets.items() if t['direct_cycle_yr'] is not None]
    ok = [l for l in solved if l['delivered'] > 0]
    summary = {'legs_from': LEGS, 'orbit': ORBIT, 'phase0_eighths': phase0, 'window_days': WINDOW, 'leg_cap_kms': CAP, 'cycle_cap_yr': CYCLE, 'seeds_per_leg': SEEDS,
               'seconds_per_leg_limit': SECONDS, 'tolerances': d.TOL, 'targets_closing_on_table': len(base), 'targets_closing_direct': len(closing), 'closing': closing,
               'legs_tried': len(solved), 'legs_delivered_in_full': sum(l['delivered'] >= l['vinf'] - 0.005 for l in solved),
               'legs_delivered_in_part': sum(0 < l['delivered'] < l['vinf'] - 0.005 for l in solved),
               'legs_without_seed': sum(l['runs'] == 0 for l in solved), 'legs_timed_out': sum(bool(l['timed_out']) for l in solved),
               'flight_days_median': round(float(np.median([l['flight_days'] for l in ok])), 1) if ok else None,
               'burn_fraction_median': round(float(np.median([l['burn_frac'] for l in ok])), 2) if ok else None,
               'median_cycle_yr': round(float(np.median([targets[n]['direct_cycle_yr'] for n in closing])), 2) if closing else None,
               'seconds': round(seconds), 'targets': targets}
    tag = f'{ORBIT}-p{phase0}' + ('' if LEGS == 'pooled' else '-station-legs') + ('' if WINDOW == 10 else f'-w{WINDOW:g}') + caps_tag()
    json.dump(summary, open(os.path.join(OUT, f'node-legs-direct-{tag}.json'), 'w'), indent=1)
    with open(os.path.join(OUT, f'node-legs-direct-{tag}-legs.csv'), 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(LEG_COLUMNS)
        for r in sorted(solved, key=lambda r: (r['target'], r['leg'], r['depart'], r['burn_ms'])):
            w.writerow([round(r[k], 4) if isinstance(r.get(k), float) else r.get(k, '') for k in LEG_COLUMNS])
    print(json.dumps({k: v for k, v in summary.items() if k != 'targets'}, indent=1), flush=True)


if __name__ == '__main__':
    main()
