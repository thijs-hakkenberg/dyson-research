"""
rq-0-52: target counts when the tug must leave from, and return to, the place the node
station is at on its orbit on the day.

    python run_cislunar_flyby_3d.py                                   # reach-3d-station-<orbit>.json
    for k in 0 .. 7: python run_trajectory_flyby_model.py --model=station-<orbit> --phase0=k
    python run_flyby_station_compare.py

The earlier passes took the best of every place on every node orbit of a kind. A station
is on one orbit and at one place on it at a time; that place is set by the date and by
where the station was put (phase0, eighths of the period at J2000). Compares, for each
orbit and each phase0, the targets that close, with the pooled result for the same kind
of orbit. Writes publications/data/nea-trajectories/{flyby-station-compare.json,
targets-flyby-station.csv}.
"""

from __future__ import annotations

import csv
import json
import os

import numpy as np

from run_flyby_3d_compare import CYCLE_CAPS, LEG_CAPS, best_cycle, load
from run_trajectory_study import OUT

ORBITS = {'halo-120': 'halo', 'halo-300': 'halo', 'planar-100': 'planar-orbits'}
PHASES = range(8)
CIS = os.path.join(OUT, '..', 'cislunar-flyby')
MODES = ((150, 90), (150, 150), (300, 60), (300, 105))


def reach_stats(orbit):
    """Reach within 15° of the ecliptic (median over longitude) for every station place and
    node angle: how much of the year a given burn and time budget gives anything at all."""
    d = json.load(open(os.path.join(CIS, f'reach-3d-station-{orbit}.json')))
    n = (len(d['lat_edges']) - 1) // 2
    out = {}
    for burn, days in MODES:
        t = np.asarray(d['vinf_kms'][str(burn)][str(days)])  # (place, node, lon, lat)
        med = np.median(t[:, :, :, n - 1 : n + 1], axis=(2, 3))  # (place, node)
        out[f'{burn} m/s, {days} d'] = {
            'best_place_any_node_kms': round(float(med.max()), 2), 'median_kms': round(float(np.median(med)), 2),
            'share_of_place_and_node_pairs_with_no_reach': round(float((med == 0).mean()), 2),
            'share_with_at_least_1.4_kms': round(float((med >= 1.4).mean()), 2),
            'median_by_station_place_kms': [round(float(x), 2) for x in np.median(med, axis=1)]}
    return out


def main():
    sweep = json.load(open(os.path.join(OUT, 'scout-launch-sweep.json')))['targets']
    scout = {n: {o: (v[0]['dv'] if v else np.inf) for o, v in t.items()} for n, t in sweep.items()}
    for n in scout:
        scout[n]['moon'] = min(scout[n]['moon'], scout[n]['moon_low'], scout[n]['c3_0'])
    pooled = {kind: load(os.path.join(OUT, f'legs-flyby-3d-{kind}.csv')) for kind in set(ORBITS.values())}
    out = {'phase0': 'place of the station on its orbit at J2000, in eighths of the period', 'orbits': {}}
    rows = {}
    keys = [(cap, Y, None) for cap in LEG_CAPS for Y in CYCLE_CAPS] + [(5.0, 4.0, {150})]
    label = lambda cap, Y, burns: f'leg<={cap} cycle<={Y}' + (', 150 m/s burns only' if burns else '')
    for orbit, kind in ORBITS.items():
        legs = {k: load(os.path.join(OUT, f'legs-flyby-station-{orbit}-p{k}.csv')) for k in PHASES
                if os.path.exists(os.path.join(OUT, f'legs-flyby-station-{orbit}-p{k}.csv'))}
        if not legs:
            continue
        names = sorted(n for n in pooled[kind] if best_cycle(pooled[kind][n], max(LEG_CAPS)) <= max(CYCLE_CAPS))
        res = {'targets_studied': len(names), 'station_phases_run': sorted(legs), 'reach': reach_stats(orbit), 'targets': {}}
        for cap, Y, burns in keys:
            base = {n for n in names if best_cycle(pooled[kind][n], cap, burns) <= Y}
            sets = {k: {n for n in names if best_cycle(legs[k].get(n, []), cap, burns) <= Y} for k in legs}
            counts = [len(sets[k]) for k in sorted(sets)]
            res['targets'][label(cap, Y, burns)] = {
                'pooled_over_orbits_and_places': len(base), 'by_phase0': counts, 'min': min(counts), 'median': float(np.median(counts)), 'max': max(counts),
                'for_every_phase0': len(set.intersection(*sets.values())), 'for_some_phase0': len(set.union(*sets.values())),
                'not_in_pooled': len(set.union(*sets.values()) - base)}
            if (cap, Y, burns) == (5.0, 4.0, None):
                res['joint_with_scout'] = {f'{o} within {b} km/s': [sum(scout.get(n, {}).get(o, np.inf) <= b for n in sets[k]) for k in sorted(sets)]
                                           for o, b in (('c3_6', 3.5), ('moon', 3.5), ('moon', 4.5))}
                cyc = {k: [best_cycle(legs[k][n], cap) for n in sets[k]] for k in sets}
                res['median_cycle_yr_by_phase0'] = [round(float(np.median(cyc[k])), 2) if cyc[k] else None for k in sorted(cyc)]
        for n in names:
            rows.setdefault(n, {})[orbit] = [best_cycle(legs[k].get(n, []), 5.0) for k in sorted(legs)]
            rows[n][kind] = best_cycle(pooled[kind][n], 5.0)
        out['orbits'][orbit] = res
    with open(os.path.join(OUT, 'targets-flyby-station.csv'), 'w', newline='') as f:
        w = csv.writer(f)
        done = [o for o in ORBITS if o in out['orbits']]
        w.writerow(['pdes'] + [f'cycle_pooled_{k}_leg5.0' for k in sorted(set(ORBITS.values()))]
                   + [f'cycle_{o}_p{k}_leg5.0' for o in done for k in out['orbits'][o]['station_phases_run']])
        fmt = lambda x: round(x, 3) if x is not None and np.isfinite(x) else ''
        for n in sorted(rows):
            w.writerow([n] + [fmt(rows[n].get(k)) for k in sorted(set(ORBITS.values()))]
                       + [fmt(x) for o in done for x in rows[n].get(o, [None] * len(out['orbits'][o]['station_phases_run']))])
    json.dump(out, open(os.path.join(OUT, 'flyby-station-compare.json'), 'w'), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == '__main__':
    main()
