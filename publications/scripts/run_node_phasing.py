"""
rq-0-52: phasing cost on the node orbit, tabulated for the parking count.

    python run_node_phasing.py [--orbit=halo-120]

For 16 start places, offsets of ±1 to ±4 eighths of the orbit, and transfer times of 20 to
200 days, the two-burn cost of node_phasing.transfer. Two burns is an upper bound on the
cost of phasing (more burns or revolutions can cost less), so the parking count charged
with it is a lower bound.

Writes publications/data/nea-trajectories/node-phasing-<orbit>.json:
cost_ms[start][offset][tau] (inf where the shooting found no transfer).
"""

from __future__ import annotations

import json
import os
import sys
import time
from multiprocessing import Pool

import numpy as np

import node_leg_direct as d
import node_phasing as ph
from run_cislunar_flyby_3d import STATION_ORBITS, orbit_label
from run_trajectory_study import OUT

arg = lambda k, default: next((a.split('=')[1] for a in sys.argv if a.startswith(f'--{k}=')), default)
ORBIT = arg('orbit', 'halo-120')
STARTS = np.arange(16) / 16.0
OFFSETS = (1, 2, 3, 4)  # eighths
TAUS = tuple(range(20, 201, 10))
_orbit = {}


def job(args):
    a, sign, tau = args
    if not _orbit:
        kinds = [orbit_label(k, s) for k, s in STATION_ORBITS]
        _orbit['o'] = d.NodeOrbit(*STATION_ORBITS[kinds.index(ORBIT)])
    res = ph.sweep(_orbit['o'], a, [sign * k / 8.0 for k in OFFSETS], tau)
    return a, sign, tau, [res[sign * k / 8.0] for k in OFFSETS]


def main():
    t0 = time.time()
    jobs = [(a, s, t) for a in STARTS for s in (1, -1) for t in TAUS]
    cost = np.full((len(STARTS), 2 * len(OFFSETS), len(TAUS)), np.inf)
    offsets = [k for k in OFFSETS] + [-k for k in OFFSETS]
    with Pool(int(arg('workers', '2'))) as pool:
        for n, (a, s, t, v) in enumerate(pool.imap_unordered(job, jobs)):
            i, j = list(STARTS).index(a), TAUS.index(t)
            for k, c in zip(OFFSETS, v):
                cost[i, offsets.index(s * k), j] = c
            if n % 50 == 49:
                print(f'{n + 1}/{len(jobs)} {time.time() - t0:.0f}s', flush=True)
    best = np.min(cost, axis=2)
    out = {'orbit': ORBIT, 'method': 'two burns, shooting with continuation in the offset (node_phasing.py)',
           'starts': STARTS.tolist(), 'offsets_eighths': offsets, 'taus_days': list(TAUS),
           'cost_ms': [[[None if not np.isfinite(x) else round(float(x), 1) for x in row] for row in plane] for plane in cost],
           'best_over_tau_ms': {str(o): {'min': round(float(np.min(best[:, j])), 1), 'median': round(float(np.median(best[:, j])), 1),
                                         'max': round(float(np.max(best[:, j])), 1)} for j, o in enumerate(offsets)},
           'transfers_found': int(np.isfinite(cost).sum()), 'transfers_tried': int(cost.size), 'seconds': round(time.time() - t0)}
    json.dump(out, open(os.path.join(OUT, f'node-phasing-{ORBIT}.json'), 'w'), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != 'cost_ms'}, indent=1))


if __name__ == '__main__':
    main()
