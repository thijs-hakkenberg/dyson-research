"""
rq-0-52, scout launch trade, step 1: the scout's own Δv against how it leaves Earth.

    python run_scout_launch_sweep.py

For each of the 150 shortlisted asteroids the least-Δv low-thrust transfer of a scout is
solved for every way of starting:

  c3_0        launch to C3 = 0, no assist (leaves with Earth's sphere of influence at rest);
  moon_low    launch to C3 <= -1.0 km²/s², one lunar swingby (three-body reach by direction);
  moon        the same from C3 <= -0.2 km²/s²;
  c3_2 … 20   launch straight to that C3, any direction.

Unlike the earlier passes, transfers above the scout's 3.5 km/s are kept (seeds up to
8 km/s), so the result can be read as "Δv the scout would need" for each launch.
All solutions from a C3 = 10 launch are kept as well, for the shared-launch check.

Writes publications/data/cislunar-flyby/reach-launch-low.json and
publications/data/nea-trajectories/scout-launch-sweep.json.
"""

from __future__ import annotations

import csv
import json
import os
from multiprocessing import Pool

import numpy as np

import run_scout_flyby_model as rs
from nea_accessibility import SCOUT, elements, load_catalogue, prefilter
from run_cislunar_flyby import OUT as CIS
from run_nea_accessibility import catalogue_path
from run_trajectory_study import DUTY, OUT, TOFS, grids, pick_seeds
from trajectory_opt import REV_OPTIONS, FlybyReach, impulsive_tables, low_thrust_leg, seed_velocities

DIRECT_C3 = (2, 4, 6, 8, 10, 15, 20)
REACH = {'moon': rs.REACH_LAUNCH, 'moon_low': os.path.join(CIS, 'reach-launch-low.json')}
LOW_LAUNCH = (-1.8, -1.4, -1.0)
SEED_MAX = 8.0
SWEEP = os.path.join(OUT, 'scout-launch-sweep.json')


def options():
    opts = [('c3_0', 0.0, None), ('moon_low', None, 'moon_low'), ('moon', None, 'moon')]
    return opts + [(f'c3_{c}', float(np.sqrt(c)), None) for c in DIRECT_C3]


def sweep_target(args):
    el1, name = args
    t_dep, _ = grids(20.0)
    one = {k: np.asarray([v]) for k, v in el1.items()}
    credits = sorted({0.0, 1.0, 1.5} | {float(np.sqrt(c)) for c in DIRECT_C3})
    tab = impulsive_tables(one, t_dep, TOFS, True, credits=credits)
    out = {}
    for key, vinf, reach in options():
        rc = FlybyReach(REACH[reach], 'launch', rs.BUDGET) if reach else None
        seeds = {}
        for g in ((1.0, 1.5) if reach else (vinf,)):
            for d, t, imp, rev in pick_seeds(tab[g][0][0], tab[g][1][0], t_dep, SEED_MAX, per_bin=1, limit=16):
                seeds.setdefault((d, t, rev), imp)
        sols = []
        for (d, t, rev) in seeds:
            lga = reach is not None or vinf > 0
            r1, vs1, r2, vs2, v1, v2 = seed_velocities(el1, t_dep[d], TOFS[t], True, lga, rev)
            if not np.all(np.isfinite(v1)):
                continue
            res = low_thrust_leg(r1, vs1, r2, vs2, TOFS[t], SCOUT.accel, DUTY, seed=(v1, v2),
                                 free_end='start' if lga else None, lga_vinf_kms=vinf or 0.0, reach=rc)
            if res.ok:
                w = [round(float(x), 4) for x in res.vinf_vec] if res.vinf_vec is not None else None
                sols.append({'dv': round(res.dv_kms, 4), 'depart': float(t_dep[d]), 'tof': float(TOFS[t]),
                             'rev': int(rev), 'vinf': round(res.vinf_kms, 3), 'w': w,
                             'thrust_fraction': round(res.thrust_fraction, 3)})
        sols.sort(key=lambda s: s['dv'])
        out[key] = sols if key == 'c3_10' else sols[:1]
    return name, out


def main():
    if not os.path.exists(REACH['moon_low']):
        keep = rs.LAUNCH_C3, rs.REACH_LAUNCH
        rs.LAUNCH_C3, rs.REACH_LAUNCH = LOW_LAUNCH, REACH['moon_low']
        rs.launch_reach()
        rs.LAUNCH_C3, rs.REACH_LAUNCH = keep
    names = sorted({r['pdes'] for r in csv.DictReader(open(os.path.join(OUT, 'targets-flyby-model.csv')))})
    cand = prefilter(load_catalogue(catalogue_path()), h_max=23.0)
    el = elements(cand)
    index = {r['pdes']: k for k, r in enumerate(cand)}
    jobs = [({k: v[index[n]] for k, v in el.items()}, n) for n in names]
    res = {}
    with Pool(min(7, os.cpu_count() or 2)) as pool:
        for k, (name, out) in enumerate(pool.imap_unordered(sweep_target, jobs, chunksize=2)):
            res[name] = out
            if k % 10 == 0:
                print(k, name, {o: (v[0]['dv'] if v else None) for o, v in out.items()}, flush=True)
    json.dump({'options': [o[0] for o in options()], 'direct_c3': list(DIRECT_C3), 'low_launch_c3': list(LOW_LAUNCH),
               'launch_c3': list(rs.LAUNCH_C3), 'seed_max_kms': SEED_MAX, 'rev_options': [list(r) for r in REV_OPTIONS],
               'targets': res}, open(SWEEP, 'w'))
    print('written', SWEEP)


if __name__ == '__main__':
    main()
