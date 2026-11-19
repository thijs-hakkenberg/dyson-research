"""
rq-0-52: multi-burn phasing cost on the node orbit, tabulated for the parking count.

    python run_node_phasing_multi.py [--orbit=halo-120] [--coast=20] [--workers=9]

The grid of run_node_phasing.py (16 start places, offsets of ±1 to ±4 eighths, transfer times
of 20 to 200 days) and longer transfers of 240 to 360 days, solved with node_phasing_multi
(a burn every `coast` days, the sum of the burns minimised). Each cell keeps the cheaper of
this and the two-burn cost of node-phasing-<orbit>.json where that has the cell; both are
recorded.

Writes publications/data/nea-trajectories/node-phasing-multi-<orbit>.json, in the layout of the
two-burn table (cost_ms[start][offset][tau], null where nothing was found), so the parking count
can read either.
"""

from __future__ import annotations

import json
import os
import sys
import time
from multiprocessing import Pool

import numpy as np

import node_leg_direct as d
import node_phasing_multi as pm
from run_cislunar_flyby_3d import STATION_ORBITS, orbit_label
from run_trajectory_study import OUT

arg = lambda k, default: next((a.split('=')[1] for a in sys.argv if a.startswith(f'--{k}=')), default)
ORBIT = arg('orbit', 'halo-120')
COAST = float(arg('coast', '20'))
STARTS = np.arange(16) / 16.0
OFFSETS = (1, 2, 3, 4, -1, -2, -3, -4)  # eighths
TAUS = tuple(range(20, 201, 10)) + (240, 300, 360)
_orbit = {}


def job(args):
    a, k, tau = args
    if not _orbit:
        kinds = [orbit_label(kk, s) for kk, s in STATION_ORBITS]
        _orbit['o'] = d.NodeOrbit(*STATION_ORBITS[kinds.index(ORBIT)])
    cost, sol = pm.phasing(_orbit['o'], a, k / 8.0, tau, COAST)
    return a, k, tau, cost, len(sol['burns_ms']), sol['min_earth_km']


def main():
    t0 = time.time()
    two = json.load(open(os.path.join(OUT, f'node-phasing-{ORBIT}.json')))
    jobs = [(a, k, t) for a in STARTS for k in OFFSETS for t in TAUS]
    multi = np.full((len(STARTS), len(OFFSETS), len(TAUS)), np.inf)
    burns = np.zeros(multi.shape, int)
    earth = np.inf
    with Pool(int(arg('workers', '9'))) as pool:
        for n, (a, k, t, c, nb, e) in enumerate(pool.imap_unordered(job, jobs)):
            i, j, l = list(STARTS).index(a), OFFSETS.index(k), TAUS.index(t)
            multi[i, j, l], burns[i, j, l] = c, nb
            earth = min(earth, e) if np.isfinite(c) else earth
            if n % 100 == 99:
                print(f'{n + 1}/{len(jobs)} {time.time() - t0:.0f}s', flush=True)
    tb = np.full(multi.shape, np.inf)
    for i, a in enumerate(STARTS):
        ti = two['starts'].index(float(a))
        for j, k in enumerate(OFFSETS):
            tj = two['offsets_eighths'].index(k)
            for l, t in enumerate(TAUS):
                if t in two['taus_days']:
                    x = two['cost_ms'][ti][tj][two['taus_days'].index(t)]
                    tb[i, j, l] = np.inf if x is None else x
    cost = np.minimum(multi, tb)
    rows = lambda arr: [[[None if not np.isfinite(x) else round(float(x), 1) for x in row] for row in plane] for plane in arr]
    stats = lambda arr: {str(o): {'min': round(float(np.min(b[:, j])), 1), 'median': round(float(np.median(b[:, j])), 1), 'max': round(float(np.max(b[:, j])), 1)}
                         for b in [np.min(arr, axis=2)] for j, o in enumerate(OFFSETS)}
    short = [l for l, t in enumerate(TAUS) if t <= 200]
    out = {'orbit': ORBIT, 'method': f'many burns (one every {COAST:g} days), multiple shooting, sum of burns minimised (node_phasing_multi.py); '
                                     'each cell the cheaper of that and the two-burn table',
           'starts': STARTS.tolist(), 'offsets_eighths': list(OFFSETS), 'taus_days': list(TAUS),
           'cost_ms': rows(cost), 'multi_burn_ms': rows(multi), 'burns': burns.tolist(),
           'best_over_tau_ms': stats(cost), 'best_over_tau_up_to_200_days_ms': stats(cost[:, :, short]),
           'two_burn_best_over_tau_ms': two['best_over_tau_ms'],
           'cells_cheaper_than_two_burn': int(np.sum(multi < tb)), 'cells_with_two_burn': int(np.isfinite(tb).sum()),
           'transfers_found': int(np.isfinite(multi).sum()), 'transfers_tried': int(multi.size),
           'closest_to_earth_km': round(float(earth)), 'seconds': round(time.time() - t0)}
    json.dump(out, open(os.path.join(OUT, f'node-phasing-multi-{ORBIT}.json'), 'w'), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k not in ('cost_ms', 'multi_burn_ms', 'burns')}, indent=1))


if __name__ == '__main__':
    main()
