"""
rq-0-52: the target count with several stations on the node orbit, or with tugs that park
on it, solved directly.

    python run_node_legs_direct.py --orbit=halo-120 --phase0=0,1,2,3,4,5,6,7
    python run_node_stations_direct.py [--orbit=halo-120] [--cap=5.0] [--cycle=4.0]

With one station its place on the node orbit is fixed by the date, and most tug legs can't
be flown from where it is (node-legs-direct-*.json). Here every tug leg has been solved
directly from each of eight station places, an eighth of the orbit apart; the escape may
fall up to 10 days either side of the leg's date, which moves the place by about half an
eighth, so eight places together cover the orbit.

Station sets: k = 1, 2, 4 or 8 stations evenly spaced round the orbit (every rotation of
each set is counted). A tug leaves from any station of the set and comes back to any (or,
in the stricter count, to the one it left). Eight stations stand in for a tug that parks on
the node orbit and leaves from wherever it needs to be; the cost of moving round the orbit
to get there (phasing) is not charged, nor the cost of reaching the station afterwards.

A target closes when it has an outbound and a return leg, each within the leg cap with the
missing excess speed charged to the thrusters, the stay at least MIN_STAY days, and node to
node within the cycle cap (as run_node_legs_direct.pairs with direct=True).

Writes publications/data/nea-trajectories/node-stations-direct-<orbit>.json and
targets-node-stations-direct-<orbit>.csv.
"""

from __future__ import annotations

import csv
import json
import os
import sys

import numpy as np

from run_trajectory_study import OUT

arg = lambda k, default: next((a.split('=')[1] for a in sys.argv if a.startswith(f'--{k}=')), default)
ORBIT = arg('orbit', 'halo-120')
CAP = float(arg('cap', '5.0'))
CYCLE = float(arg('cycle', '4.0'))
MIN_STAY = 60.0
PLACES = 8
COUNTS = (1, 2, 4, 8)
TAG = '' if (CAP, CYCLE) == (5.0, 4.0) else f'-c{CAP:g}-y{CYCLE:g}'


def load():
    """{place: [leg rows]} from the per-leg files of run_node_legs_direct.py."""
    legs = {}
    for p in range(PLACES):
        path = os.path.join(OUT, f'node-legs-direct-{ORBIT}-p{p}{TAG}-legs.csv')
        rows = []
        for r in csv.DictReader(open(path)):
            rows.append({'target': r['target'], 'leg': r['leg'], 'burn_ms': int(r['burn_ms']), 'budget': float(r['budget']), 'place': p, 'depart': float(r['depart']), 'tof': float(r['tof']),
                         'dv_eff': float(r['dv_eff']), 'node_T': float(r['node_T']) if r['node_T'] not in ('', 'nan') else np.nan,
                         'delivered': float(r['delivered']), 'vinf': float(r['vinf']), 'timed_out': r['timed_out'] == 'True'})
        legs[p] = rows
    return legs


def best_cycle(rows, places, same_station=False):
    """Shortest node-to-node cycle (years) of one target from the given station places, or None."""
    outs = [r for r in rows if r['leg'] == 'out' and r['place'] in places and r['dv_eff'] <= CAP]
    ins = [r for r in rows if r['leg'] == 'in' and r['place'] in places and r['dv_eff'] <= CAP]
    best = None
    for o in outs:
        for i in ins:
            if (same_station and i['place'] != o['place']) or i['depart'] < o['depart'] + o['tof'] + MIN_STAY:
                continue
            cyc = (i['node_T'] - o['node_T']) / 365.25
            if cyc <= CYCLE and (best is None or cyc < best):
                best = cyc
    return best


class Phasing:
    """Two-burn phasing costs on the node orbit (run_node_phasing.py)."""

    def __init__(self, path, period_days):
        z = json.load(open(path))
        self.starts = np.array(z['starts'])
        self.offsets = z['offsets_eighths']
        self.taus = [float(t) for t in z['taus_days']]
        self.cost = np.array([[[np.inf if x is None else x for x in row] for row in plane] for plane in z['cost_ms']]) / 1e3  # km/s
        self.period = period_days

    def cost_at(self, start_place, delta_eighths, j):
        """km/s to move a tug by delta eighths (wrapped to -3..4) of the orbit in taus[j] days,
        starting at start_place (fraction of the orbit; nearest tabulated start)."""
        delta = (delta_eighths + 3) % 8 - 3
        if delta == 0:
            return 0.0
        i = int(np.round(start_place % 1.0 * len(self.starts))) % len(self.starts)
        c = self.cost[i, self.offsets.index(delta), j]
        return min(c, self.cost[i, self.offsets.index(-4), j]) if delta == 4 else c


def best_cycle_parking(rows, station, phasing):
    """Shortest cycle (years) for one station at `station` (eighths at J2000) whose tugs move round
    the orbit to leave from, and come back from, the place each leg was solved for. Phasing is
    paid out of the leg's Δv cap and adds its time to the cycle. None if nothing closes."""
    P = phasing.period
    outs, ins = [], []
    for r in rows:
        if not np.isfinite(r['dv_eff']) or r['dv_eff'] > CAP:
            continue
        delta = r['place'] - station
        if delta == 0:
            (outs if r['leg'] == 'out' else ins).append((r['node_T'], r))
            continue
        for j, tau in enumerate(phasing.taus):
            if r['leg'] == 'out':  # from the station to the leg's place, ending at the burn
                c = phasing.cost_at(station / PLACES + (r['node_T'] - tau) / P, delta, j)
                if r['dv_eff'] + c <= CAP:
                    outs.append((r['node_T'] - tau, r))
            else:  # from the leg's place, starting on arrival, back to the station
                c = phasing.cost_at(r['place'] / PLACES + r['node_T'] / P, -delta, j)
                if r['dv_eff'] + c <= CAP:
                    ins.append((r['node_T'] + tau, r))
    best = None
    for t0, o in outs:
        for t1, i in ins:
            if i['depart'] < o['depart'] + o['tof'] + MIN_STAY:
                continue
            cyc = (t1 - t0) / 365.25
            if cyc <= CYCLE and (best is None or cyc < best):
                best = cyc
    return best


def station_sets(k):
    step = PLACES // k
    return [tuple(range(j, PLACES, step)) for j in range(step)]


def main():
    legs = load()
    rows = [r for p in legs.values() for r in p]
    names = sorted({r['target'] for r in rows})
    by = {n: [r for r in rows if r['target'] == n] for n in names}
    out = {'orbit': ORBIT, 'leg_cap_kms': CAP, 'cycle_cap_yr': CYCLE, 'min_stay_days': MIN_STAY, 'places': PLACES,
           'targets_tried': len(names), 'legs_per_place': {p: len(v) for p, v in legs.items()},
           'legs_timed_out': sum(r['timed_out'] for r in rows), 'stations': {}}
    per_target = {n: {} for n in names}
    for k in COUNTS:
        res = []
        for s in station_sets(k):
            cyc = {n: best_cycle(by[n], s) for n in names}
            same = {n: best_cycle(by[n], s, same_station=True) for n in names}
            closing = sorted(n for n in names if cyc[n] is not None)
            res.append({'places': list(s), 'targets': len(closing), 'targets_same_station': sum(v is not None for v in same.values()),
                        'median_cycle_yr': round(float(np.median([cyc[n] for n in closing])), 2) if closing else None, 'closing': closing})
            for n in names:
                if cyc[n] is not None:
                    per_target[n].setdefault(k, []).append(round(cyc[n], 3))
        counts = [r['targets'] for r in res]
        out['stations'][k] = {'targets_min': min(counts), 'targets_max': max(counts),
                              'targets_same_station_min': min(r['targets_same_station'] for r in res),
                              'targets_same_station_max': max(r['targets_same_station'] for r in res), 'sets': res}
    path = os.path.join(OUT, f'node-phasing-{ORBIT}.json')
    if os.path.exists(path):
        from run_cislunar_flyby_3d import STATION_ORBITS, orbit_label
        import node_leg_direct as d
        kinds = [orbit_label(k, a) for k, a in STATION_ORBITS]
        phasing = Phasing(path, d.NodeOrbit(*STATION_ORBITS[kinds.index(ORBIT)]).period_days)
        res = []
        for st in range(PLACES):
            cyc = {n: best_cycle_parking(by[n], st, phasing) for n in names}
            closing = sorted(n for n in names if cyc[n] is not None)
            res.append({'station': st, 'targets': len(closing), 'closing': closing,
                        'median_cycle_yr': round(float(np.median([cyc[n] for n in closing])), 2) if closing else None})
        out['parking_two_burn_phasing'] = {'targets_min': min(r['targets'] for r in res), 'targets_max': max(r['targets'] for r in res),
                                           'note': 'one station; tugs phase round the orbit with two-burn transfers (an upper bound on the phasing cost) paid from the leg cap', 'by_station': res}
    # legs: which places deliver each leg in full or in part
    deliver = {}
    for n in names:
        keys = {(r['leg'], r['burn_ms'], round(r['depart'], 3), r['tof'], r['vinf'], r['budget']) for r in by[n]}
        for key in keys:
            rs = [r for r in by[n] if (r['leg'], r['burn_ms'], round(r['depart'], 3), r['tof'], r['vinf'], r['budget']) == key]
            deliver.setdefault('full', []).append(sum(r['delivered'] >= r['vinf'] - 0.005 for r in rs))
            deliver.setdefault('any', []).append(sum(r['delivered'] > 0 for r in rs))
    full, anyp = np.array(deliver['full']), np.array(deliver['any'])
    out['legs'] = {'distinct': int(len(full)), 'delivered_in_full_from_some_place': int((full > 0).sum()),
                   'delivered_at_all_from_some_place': int((anyp > 0).sum()), 'places_delivering_in_full_median_where_any': float(np.median(full[full > 0])) if (full > 0).any() else None}
    with open(os.path.join(OUT, f'targets-node-stations-direct-{ORBIT}{TAG}.csv'), 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['pdes'] + [f'sets_closing_of_{len(station_sets(k))}_with_{k}' for k in COUNTS] + ['best_cycle_yr_8'])
        for n in names:
            w.writerow([n] + [len(per_target[n].get(k, [])) for k in COUNTS] + [min(per_target[n][8]) if 8 in per_target[n] else ''])
    json.dump(out, open(os.path.join(OUT, f'node-stations-direct-{ORBIT}{TAG}.json'), 'w'), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k not in ('stations', 'parking_two_burn_phasing')}, indent=1))
    if 'parking_two_burn_phasing' in out:
        p = out['parking_two_burn_phasing']
        print('1 station, tugs parking with two-burn phasing:', p['targets_min'], '-', p['targets_max'], 'targets')
    for k in COUNTS:
        s = out['stations'][k]
        print(k, 'stations:', s['targets_min'], '-', s['targets_max'], 'targets; returning to the same station', s['targets_same_station_min'], '-', s['targets_same_station_max'])


if __name__ == '__main__':
    main()
