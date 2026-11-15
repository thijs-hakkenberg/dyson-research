"""
rq-0-52, third pass: tug cycles with the lunar flyby taken from the three-body model.

    python run_trajectory_flyby_model.py

The second pass (run_trajectory_study.py) gave each leg a free Earth-relative excess speed
of 1.0 or 1.5 km/s in any direction for 30 days. Here the excess speed is limited by
direction, using the reach table of run_cislunar_flyby.py for a given node burn and time
budget; the node burn is added to the leg's Δv, and the time allowance is the budget plus
half a synodic month of waiting for the Moon.

Writes publications/data/nea-trajectories/{legs-flyby-model.csv, flyby-model.json}.
"""

from __future__ import annotations

import csv
import json
import os
from multiprocessing import Pool

import numpy as np

from nea_accessibility import TUG_IN, TUG_OUT, elements, load_catalogue, prefilter
from run_nea_accessibility import catalogue_path
from run_trajectory_study import DUTY, MIN_STAY, OUT, TOFS, YEAR, grids, pick_seeds
from trajectory_opt import FlybyReach, impulsive_tables, low_thrust_leg, seed_velocities

REACH = os.path.join(OUT, '..', 'cislunar-flyby', 'reach.json')
MODES = ((150, 60), (150, 90), (150, 150), (300, 60), (300, 105))  # (node burn m/s, days from burn to escape)
MOON_WAIT_DAYS = 14.8  # mean wait for the lunar phase a solution needs
LEG_CAPS = (5.0, 5.75, 6.5)
CYCLE_CAPS = (4.0, 5.0)
SEED_CREDITS = (1.0, 1.5)
_REACH = {}


def reach(mode):
    if mode not in _REACH:
        _REACH[mode] = FlybyReach(REACH, *mode)
    return _REACH[mode]


def target_legs(args):
    el1, name = args
    t_dep, t_ret = grids(20.0)
    one = {k: np.asarray([v]) for k, v in el1.items()}
    out = impulsive_tables(one, t_dep, TOFS, True, credits=SEED_CREDITS)
    ret = impulsive_tables(one, t_ret, TOFS, False, credits=SEED_CREDITS)
    legs = []
    for outbound, tabs, grid, veh in ((True, out, t_dep, TUG_OUT), (False, ret, t_ret, TUG_IN)):
        seeds = {}
        for g in SEED_CREDITS:
            for d, t, imp, rev in pick_seeds(tabs[g][0][0], tabs[g][1][0], grid, 7.5):
                seeds.setdefault((d, t, rev), imp)
        for (d, t, rev), imp in seeds.items():
            r1, vs1, r2, vs2, v1, v2 = seed_velocities(el1, grid[d], TOFS[t], outbound, True, rev)
            if not np.all(np.isfinite(v1)):
                continue
            for mode in MODES:
                rc = reach(mode)
                res = low_thrust_leg(r1, vs1, r2, vs2, TOFS[t], veh.accel, DUTY, seed=(v1, v2),
                                     free_end='start' if outbound else 'end', reach=rc)
                if not res.ok:
                    continue
                w = np.asarray(res.vinf_vec)
                lon, lat = rc.angles(w, r2 if not outbound else r1, not outbound)
                legs.append({'target': name, 'burn_ms': mode[0], 'budget_days': mode[1], 'leg': 'out' if outbound else 'in',
                             'depart': float(grid[d]), 'tof': float(TOFS[t]), 'revs': int(rev), 'thruster_dv': res.dv_kms,
                             'dv': res.dv_kms + mode[0] / 1e3, 'thrust_fraction': res.thrust_fraction, 'vinf': res.vinf_kms,
                             'lon': lon, 'lat': lat, 'allowance': mode[1] + MOON_WAIT_DAYS})
    return name, legs


def best_cycle(legs, cap, modes=None):
    """Shortest node-to-node cycle (years). The outbound leg leaves the node `allowance`
    days before its heliocentric departure; the return reaches the node `allowance` days
    after its heliocentric arrival."""
    ok = lambda l: l['dv'] <= cap and (modes is None or (l['burn_ms'], l['budget_days']) in modes)
    outs = [l for l in legs if l['leg'] == 'out' and ok(l)]
    ins = [l for l in legs if l['leg'] == 'in' and ok(l)]
    best = None
    for o in outs:
        arrive = o['depart'] + o['tof']
        for i in ins:
            if i['depart'] >= arrive + MIN_STAY:
                cyc = (i['depart'] + i['tof'] + i['allowance'] - o['depart'] + o['allowance']) / 365.25
                if best is None or cyc < best[0]:
                    best = (cyc, o, i)
    return best


def main():
    names = sorted({r['target'] for r in csv.DictReader(open(os.path.join(OUT, 'legs.csv')))})
    cand = prefilter(load_catalogue(catalogue_path()), h_max=23.0)
    el = elements(cand)
    index = {r['pdes']: k for k, r in enumerate(cand)}
    jobs = [({k: v[index[n]] for k, v in el.items()}, n) for n in names]
    with Pool(min(7, os.cpu_count() or 2)) as pool:
        res = []
        for k, r in enumerate(pool.imap_unordered(target_legs, jobs, chunksize=1)):
            res.append(r)
            if k % 10 == 9:
                print(f'{k + 1}/{len(jobs)} targets', flush=True)
    by = dict(res)
    with open(os.path.join(OUT, 'legs-flyby-model.csv'), 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['target', 'burn_ms', 'budget_days', 'leg', 'depart_year', 'tof_days', 'revs', 'low_thrust_kms', 'thruster_only_kms',
                    'thrust_fraction', 'vinf_kms', 'vinf_lon_deg', 'vinf_lat_deg', 'allowance_days'])
        for n in names:
            for l in by[n]:
                w.writerow([n, l['burn_ms'], l['budget_days'], l['leg'], round(YEAR(l['depart']), 3), l['tof'], l['revs'], round(l['dv'], 3),
                            round(l['thruster_dv'], 3), round(l['thrust_fraction'], 3), round(l['vinf'], 3), round(l['lon'], 1), round(l['lat'], 1),
                            round(l['allowance'], 1)])
    summary = {'modes': [list(m) for m in MODES], 'moon_wait_days': MOON_WAIT_DAYS, 'targets_studied': len(names), 'targets_closing': {}, 'cycle_years': {}}
    groups = {'any mode': None, **{f'burn {b} m/s, {d} d': {(b, d)} for b, d in MODES},
              'burn 150 m/s, any budget': {m for m in MODES if m[0] == 150}}
    for label, modes in groups.items():
        row, cyc = {}, {}
        for cap in LEG_CAPS:
            cs = [c[0] for n in names if (c := best_cycle(by[n], cap, modes))]
            for Y in CYCLE_CAPS:
                row[f'leg<={cap} cycle<={Y}'] = int(sum(1 for c in cs if c <= Y))
            cyc[f'leg<={cap}'] = {'closing at any cycle': len(cs), 'median': round(float(np.median(cs)), 2) if cs else None,
                                  'P10': round(float(np.percentile(cs, 10)), 2) if cs else None}
        summary['targets_closing'][label] = row
        summary['cycle_years'][label] = cyc
    used = [l for n in names for l in by[n]]
    summary['legs_solved'] = len(used)
    summary['vinf_used_kms'] = {str(p): round(float(np.percentile([l['vinf'] for l in used], p)), 2) for p in (10, 50, 90)}
    summary['latitude_used_deg'] = {str(p): round(float(np.percentile([l['lat'] for l in used], p)), 1) for p in (50, 90, 100)}
    json.dump(summary, open(os.path.join(OUT, 'flyby-model.json'), 'w'), indent=1)
    print(json.dumps(summary, indent=1))


if __name__ == '__main__':
    main()
