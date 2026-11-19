"""
rq-0-52: settle the target count with the station's place fixed, by solving the leg
between the node and the edge of the Earth's sphere of influence for each tug leg.

    python run_cislunar_flyby_3d.py --station        # the sample of escapes used as seeds
    python run_node_legs_direct.py --orbit=halo-120 --phase0=0 [--legs=pooled|station] [--window=10] [--cap=5.0] [--cycle=4.0]

Takes tug legs already solved against a reach table: the pooled halo table
(legs-flyby-3d-halo.csv; only targets that close there can close with the station's place
fixed) or, with --legs=station, this station's own table (legs-flyby-station-*.csv, which
run_trajectory_flyby_model.py --model=station-<orbit> regenerates). For every leg that is
part of a cycle within the caps, node_leg_direct.reachable finds whether the excess
velocity the leg uses can be delivered on that date, and if not, how much of it. Missing
excess speed is charged to the tug's thrusters one for one (an upper bound on its cost).
The escape may fall within `window` days of the date the leg was solved for; the
heliocentric leg is kept as solved.

Writes publications/data/nea-trajectories/node-legs-direct-<orbit>-p<k>[-w<window>].json.
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
PHASE0 = int(arg('phase0', '0'))
WINDOW = float(arg('window', '10'))
CAP = float(arg('cap', '5.0'))
CYCLE = float(arg('cycle', '4.0'))
MIN_STAY = 60.0
LEGS = arg('legs', 'pooled')  # pooled: legs solved against the pooled halo table; station: against this station's own table
SEEDS = int(arg('seeds', '3'))
_ctx = {}


def load_legs():
    legs = {}
    name = 'legs-flyby-3d-halo.csv' if LEGS == 'pooled' else f'legs-flyby-station-{ORBIT}-p{PHASE0}.csv'
    for r in csv.DictReader(open(os.path.join(OUT, name))):
        legs.setdefault(r['target'], []).append({
            'target': r['target'], 'leg': r['leg'], 'burn_ms': int(r['burn_ms']), 'budget': float(r['budget_days']),
            'depart': d.J2000 + (float(r['depart_year']) - 2000.0) * 365.25, 'tof': float(r['tof_days']), 'dv': float(r['low_thrust_kms']),
            'vinf': float(r['vinf_kms']), 'lon': float(r['vinf_lon_deg']), 'lat': float(r['vinf_lat_deg']), 'allowance': float(r['allowance_days'])})
    return legs


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


def setup():
    if not _ctx:
        kinds = [orbit_label(k, a) for k, a in STATION_ORBITS]
        kind, size = STATION_ORBITS[kinds.index(ORBIT)]
        orbit = d.NodeOrbit(kind, size)
        z = np.load(os.path.join(CIS, 'escapes-3d-station.npz'))
        _ctx.update(orbit=orbit, clouds={b: d.Cloud(z, b, kinds.index(ORBIT), orbit.period_days) for b in (150, 300)},
                    clocks=d.Clocks(PHASE0 / 8.0, orbit.period_days))
    return _ctx


def solve_leg(leg):
    ctx = setup()
    out = leg['leg'] == 'out'
    T_earth = (leg['depart'] if out else leg['depart'] + leg['tof']) - d.J2000  # day the leg leaves or reaches the sphere of influence
    clocks = ctx['clocks'] if out else ctx['clocks'].mirrored()
    v, sol, runs = d.reachable(ctx['orbit'], ctx['clouds'][leg['burn_ms']], clocks, leg['lon'], leg['lat'], leg['vinf'], float(leg['burn_ms']),
                               T_earth if out else -T_earth, WINDOW, leg['budget'], n_seeds=SEEDS)
    res = dict(leg, delivered=v, runs=runs)
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
    legs = load_legs()
    jobs, base = [], {}
    for n, L in legs.items():
        outs, ins = [l for l in L if l['leg'] == 'out'], [l for l in L if l['leg'] == 'in']
        ps = pairs(outs, ins, CAP, CYCLE)
        if ps:
            base[n] = min(p[0] for p in ps)
            used = {id(p[1]): p[1] for p in ps} | {id(p[2]): p[2] for p in ps}
            jobs += list(used.values())
    print(f'{ORBIT} phase0 {PHASE0}/8 window {WINDOW:g} d: {len(base)} targets, {len(jobs)} legs', flush=True)
    t0 = time.time()
    with Pool(min(7, os.cpu_count() or 2)) as pool:
        solved = []
        for k, r in enumerate(pool.imap_unordered(solve_leg, jobs, chunksize=1)):
            solved.append(r)
            if k % 25 == 24:
                print(f'{k + 1}/{len(jobs)} legs, {time.time() - t0:.0f}s', flush=True)
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
    summary = {'legs_from': LEGS, 'orbit': ORBIT, 'phase0_eighths': PHASE0, 'window_days': WINDOW, 'leg_cap_kms': CAP, 'cycle_cap_yr': CYCLE, 'seeds_per_leg': SEEDS,
               'tolerances': d.TOL, 'targets_closing_on_table': len(base), 'targets_closing_direct': len(closing), 'closing': closing,
               'legs_tried': len(solved), 'legs_delivered_in_full': sum(l['delivered'] >= l['vinf'] - 0.005 for l in solved),
               'legs_delivered_in_part': sum(0 < l['delivered'] < l['vinf'] - 0.005 for l in solved),
               'legs_without_seed': sum(l['runs'] == 0 for l in solved),
               'flight_days_median': round(float(np.median([l['flight_days'] for l in ok])), 1) if ok else None,
               'burn_fraction_median': round(float(np.median([l['burn_frac'] for l in ok])), 2) if ok else None,
               'median_cycle_yr': round(float(np.median([targets[n]['direct_cycle_yr'] for n in closing])), 2) if closing else None,
               'seconds': round(time.time() - t0), 'targets': targets}
    tag = f'{ORBIT}-p{PHASE0}' + ('' if LEGS == 'pooled' else '-station-legs') + ('' if WINDOW == 10 else f'-w{WINDOW:g}')
    json.dump(summary, open(os.path.join(OUT, f'node-legs-direct-{tag}.json'), 'w'), indent=1)
    print(json.dumps({k: v for k, v in summary.items() if k != 'targets'}, indent=1))


if __name__ == '__main__':
    main()
