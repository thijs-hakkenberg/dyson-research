"""
rq-0-52: what halo node orbits and the Moon's inclined orbit do to the target counts.

    python run_cislunar_flyby_3d.py                       # reach tables
    python run_trajectory_flyby_model.py --model=planar-orbits
    python run_trajectory_flyby_model.py --model=halo
    python run_flyby_3d_compare.py

Compares the tug legs solved against three reach tables:

  planar          first three-body model: planar node orbits, Moon in the ecliptic, two swingbys;
  planar-orbits   the same node orbits, Moon on its inclined orbit, one swingby;
  halo            halo node orbits, Moon on its inclined orbit, one swingby.

and applies the scout constraint from the launch sweep. Writes
publications/data/nea-trajectories/flyby-3d-compare.json and targets-flyby-3d.csv.
"""

from __future__ import annotations

import csv
import json
import os

import numpy as np

from run_trajectory_study import OUT

MODELS = {'planar': 'legs-flyby-model.csv', 'planar-orbits': 'legs-flyby-3d-planar-orbits.csv', 'halo': 'legs-flyby-3d-halo.csv'}
LEG_CAPS = (5.0, 5.75, 6.5)
CYCLE_CAPS = (4.0, 5.0)
MIN_STAY = 60.0
SCOUT = (('c3_6', 3.5), ('c3_10', 3.5), ('moon', 3.5), ('moon', 4.5))


def load(path):
    legs = {}
    for r in csv.DictReader(open(path)):
        legs.setdefault(r['target'], []).append({
            'leg': r['leg'], 'burn_ms': int(r['burn_ms']), 'depart': float(r['depart_year']) * 365.25, 'tof': float(r['tof_days']),
            'dv': float(r['low_thrust_kms']), 'allowance': float(r['allowance_days']), 'vinf': float(r['vinf_kms']), 'lat': abs(float(r['vinf_lat_deg']))})
    return legs


def best_cycle(legs, cap, burns=None):
    """Shortest node-to-node cycle in years (as run_trajectory_flyby_model.best_cycle)."""
    ok = lambda l: l['dv'] <= cap and (burns is None or l['burn_ms'] in burns)
    o = np.array([(l['depart'], l['tof'], l['allowance']) for l in legs if l['leg'] == 'out' and ok(l)]).reshape(-1, 3)
    i = np.array([(l['depart'], l['tof'], l['allowance']) for l in legs if l['leg'] == 'in' and ok(l)]).reshape(-1, 3)
    if not len(o) or not len(i):
        return np.inf
    fits = i[None, :, 0] >= (o[:, 0] + o[:, 1] + MIN_STAY)[:, None]
    cyc = np.where(fits, (i[None, :, 0] + i[None, :, 1] + i[None, :, 2]) - o[:, None, 0] + o[:, None, 2], np.inf)
    return float(cyc.min()) / 365.25


def main():
    sweep = json.load(open(os.path.join(OUT, 'scout-launch-sweep.json')))['targets']
    scout = {n: {o: (v[0]['dv'] if v else np.inf) for o, v in t.items()} for n, t in sweep.items()}
    for n in scout:
        scout[n]['moon'] = min(scout[n]['moon'], scout[n]['moon_low'], scout[n]['c3_0'])
    legs = {m: load(os.path.join(OUT, f)) for m, f in MODELS.items()}
    names = sorted(set().union(*[set(v) for v in legs.values()]))
    cyc = {m: {n: {cap: best_cycle(legs[m].get(n, []), cap) for cap in LEG_CAPS} for n in names} for m in MODELS}
    cyc150 = {m: {n: best_cycle(legs[m].get(n, []), 5.0, {150}) for n in names} for m in MODELS}
    out = {'models': list(MODELS), 'targets_studied': len(names), 'tug': {}, 'joint_with_scout': {}, 'against_planar': {}}
    for m in MODELS:
        out['tug'][m] = {}
        out['joint_with_scout'][m] = {}
        for cap in LEG_CAPS:
            cs = np.array([cyc[m][n][cap] for n in names])
            fin = cs[np.isfinite(cs)]
            for Y in CYCLE_CAPS:
                key = f'leg<={cap} cycle<={Y}'
                s = [n for n in names if cyc[m][n][cap] <= Y]
                out['tug'][m][key] = len(s)
                out['joint_with_scout'][m][key] = {f'{o} within {b} km/s': sum(scout.get(n, {}).get(o, np.inf) <= b for n in s) for o, b in SCOUT}
            out['tug'][m][f'leg<={cap} closing at any cycle'] = int(len(fin))
            out['tug'][m][f'leg<={cap} median cycle yr'] = round(float(np.median(fin)), 2) if len(fin) else None
        out['tug'][m]['leg<=5.0 cycle<=4.0, 150 m/s burns only'] = sum(cyc150[m][n] <= 4.0 for n in names)
        used = [l for n in names for l in legs[m].get(n, [])]
        out['tug'][m]['legs_solved'] = len(used)
        out['tug'][m]['vinf_used_kms'] = {str(p): round(float(np.percentile([l['vinf'] for l in used], p)), 2) for p in (10, 50, 90)}
    base = {cap: {Y: {n for n in names if cyc['planar'][n][cap] <= Y} for Y in CYCLE_CAPS} for cap in LEG_CAPS}
    for m in ('planar-orbits', 'halo'):
        out['against_planar'][m] = {}
        for cap in LEG_CAPS:
            for Y in CYCLE_CAPS:
                s = {n for n in names if cyc[m][n][cap] <= Y}
                both = sorted(s & base[cap][Y])
                d = [cyc[m][n][cap] - cyc['planar'][n][cap] for n in both]
                out['against_planar'][m][f'leg<={cap} cycle<={Y}'] = {
                    'kept': len(both), 'lost': len(base[cap][Y] - s), 'gained': len(s - base[cap][Y]),
                    'median_cycle_change_yr': round(float(np.median(d)), 2) if d else None}
    with open(os.path.join(OUT, 'targets-flyby-3d.csv'), 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['pdes'] + [f'cycle_{m}_leg{cap}' for m in MODELS for cap in LEG_CAPS] + ['scout_dv_c3_6', 'scout_dv_c3_10', 'scout_dv_moon'])
        for n in names:
            w.writerow([n] + [round(cyc[m][n][cap], 3) if np.isfinite(cyc[m][n][cap]) else '' for m in MODELS for cap in LEG_CAPS]
                       + [round(scout[n][o], 3) if n in scout and np.isfinite(scout[n][o]) else '' for o in ('c3_6', 'c3_10', 'moon')])
    json.dump(out, open(os.path.join(OUT, 'flyby-3d-compare.json'), 'w'), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == '__main__':
    main()
