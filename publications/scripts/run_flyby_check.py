"""
rq-0-52: check the lunar-flyby assumption of the trajectory study against the literature.

    python run_flyby_check.py

The study credits a tug with a free Earth-relative excess speed (1.0 or 1.5 km/s) in any
direction at the Earth end of a leg, for 30 days. Published work supports about 1.4 km/s,
limits the direction (about ±30° from the ecliptic for a short sequence) and takes
60–200 days. This script measures how far the study's answers depend on the two parts the
literature does not support as modelled:

1. time: target counts re-assembled from legs.csv with a longer allowance per assisted leg;
2. direction: the legs behind each target's best cycle re-solved, and the ecliptic
   latitude of the excess velocity they use recorded.

Writes publications/data/nea-trajectories/flyby-check.json.
"""

from __future__ import annotations

import csv
import json
import os
from collections import defaultdict
from multiprocessing import Pool

import numpy as np

from nea_accessibility import J2000, TUG_IN, TUG_OUT, elements, load_catalogue, prefilter
from run_nea_accessibility import catalogue_path
from run_trajectory_study import DUTY, MIN_STAY, OUT, TOFS, grids
from trajectory_opt import REV_OPTIONS, low_thrust_leg, seed_velocities

ALLOWANCES = (30.0, 60.0, 90.0, 120.0, 200.0)  # days per assisted leg
SETTINGS = ((1.0, 5.0), (1.0, 6.5), (1.5, 5.0), (1.5, 6.5))  # (flyby km/s, leg Δv cap km/s)
CYCLE_CAPS = (4.0, 5.0)
LAT_LIMITS = (30.0, 45.0)


def load_legs():
    legs = defaultdict(list)
    with open(os.path.join(OUT, 'legs.csv')) as f:
        for r in csv.DictReader(f):
            if r['low_thrust_kms'] == '':
                continue
            legs[r['target']].append({'lga': float(r['lga_vinf']), 'leg': r['leg'], 'depart': J2000 + (float(r['depart_year']) - 2000) * 365.25,
                                      'tof': float(r['tof_days']), 'revs': int(r['revs']), 'impulsive': float(r['impulsive_kms']),
                                      'low_thrust': float(r['low_thrust_kms'])})
    return legs


def cycles(legs, g, cap, allowance, ok=lambda l: True):
    """All (cycle years, out leg, in leg) for one target, shortest first."""
    outs = [l for l in legs if l['lga'] == g and l['leg'] == 'out' and l['low_thrust'] <= cap and ok(l)]
    ins = [l for l in legs if l['lga'] == g and l['leg'] == 'in' and l['low_thrust'] <= cap and ok(l)]
    found = []
    for o in outs:
        arrive = o['depart'] + o['tof']
        for i in ins:
            if i['depart'] >= arrive + MIN_STAY:
                found.append(((i['depart'] + i['tof'] - o['depart'] + 2 * allowance) / 365.25, o, i))
    return sorted(found, key=lambda c: c[0])


def resolve(args):
    """Re-solve one leg and return the ecliptic latitude (deg) of the excess velocity used."""
    el1, leg, key = args
    outbound = leg['leg'] == 'out'
    grid = grids(20.0)[0 if outbound else 1]
    t = grid[np.argmin(np.abs(grid - leg['depart']))]
    veh = TUG_OUT if outbound else TUG_IN
    best = None
    for k, (nrev, _) in enumerate(REV_OPTIONS):
        if nrev != leg['revs']:
            continue
        r1, vs1, r2, vs2, v1, v2 = seed_velocities(el1, t, leg['tof'], outbound, True, k)
        if not np.all(np.isfinite(v1)):
            continue
        res = low_thrust_leg(r1, vs1, r2, vs2, leg['tof'], veh.accel, DUTY, seed=(v1, v2),
                             free_end='start' if outbound else 'end', lga_vinf_kms=leg['lga'])
        if res.ok and (best is None or abs(res.dv_kms - leg['low_thrust']) < abs(best.dv_kms - leg['low_thrust'])):
            best = res
    if best is None or abs(best.dv_kms - leg['low_thrust']) > 0.05:
        return key, None
    v = np.asarray(best.vinf_vec)
    n = float(np.linalg.norm(v))
    return key, (float(np.degrees(np.arcsin(abs(v[2]) / n))) if n > 1e-6 else 0.0, n)


def main():
    legs = load_legs()
    result = {'allowance_days_per_leg': {}, 'direction': {}}

    for g, cap in SETTINGS:
        for Y in CYCLE_CAPS:
            result['allowance_days_per_leg'][f'flyby={g} leg<={cap} cycle<={Y}'] = {
                str(int(a)): sum(1 for t in legs if (c := cycles(legs[t], g, cap, a)) and c[0][0] <= Y) for a in ALLOWANCES}

    cand = prefilter(load_catalogue(catalogue_path()), h_max=23.0)
    el = elements(cand)
    index = {r['pdes']: k for k, r in enumerate(cand)}
    el1 = lambda t: {k: v[index[t]] for k, v in el.items()}

    # every flyby leg that takes part in a cycle of at most 5 years at the loosest cap
    jobs = {}
    for t in legs:
        for g in (1.0, 1.5):
            for _, o, i in cycles(legs[t], g, 6.5, 30.0):
                for l in (o, i):
                    jobs[(t, g, l['leg'], l['depart'], l['tof'], l['revs'])] = (el1(t), l)
    print(f'{len(jobs)} legs to re-solve', flush=True)
    with Pool(min(7, os.cpu_count() or 2)) as pool:
        lat = dict(pool.imap_unordered(resolve, [(e, l, k) for k, (e, l) in jobs.items()], chunksize=4))
    solved = {k: v for k, v in lat.items() if v is not None}
    print(f'{len(solved)} reproduced', flush=True)
    lats = np.array([v[0] for v in solved.values()])
    used = np.array([v[1] for v in solved.values()])
    result['direction']['legs_resolved'] = len(jobs)
    result['direction']['legs_reproduced'] = len(solved)
    result['direction']['latitude_deg_percentiles'] = {str(p): round(float(np.percentile(lats, p)), 1) for p in (10, 50, 90, 100)}
    result['direction']['share_of_legs_within'] = {str(int(L)): round(float((lats <= L).mean()), 3) for L in LAT_LIMITS}
    result['direction']['share_using_full_credit'] = round(float((used >= 0.98 * np.array([k[1] for k in solved])).mean()), 3)

    def key(t, l):
        return (t, l['lga'], l['leg'], l['depart'], l['tof'], l['revs'])

    for g, cap in SETTINGS:
        for a in (30.0, 90.0):
            row = {'any direction': sum(1 for t in legs if (c := cycles(legs[t], g, cap, a)) and c[0][0] <= 4.0)}
            for L in LAT_LIMITS:
                row[f'within {int(L)} deg'] = sum(
                    1 for t in legs
                    if (c := cycles(legs[t], g, cap, a, ok=lambda l, t=t: key(t, l) in solved and solved[key(t, l)][0] <= L)) and c[0][0] <= 4.0)
            result['direction'][f'targets flyby={g} leg<={cap} cycle<=4 allowance={int(a)}d'] = row

    with open(os.path.join(OUT, 'flyby-check.json'), 'w') as f:
        json.dump(result, f, indent=1)
    print(json.dumps(result, indent=1))


if __name__ == '__main__':
    main()
