"""
rq-0-52: reachable Earth-relative excess velocity for a tug leaving a Sun–Earth L1 node by
way of the Moon, from the three-body model in cislunar_flyby.py.

    python run_cislunar_flyby.py [--quick]

For each departure burn size it flies: node orbit → burn → coast to the Moon → swingby →
escape, and the same with a second swingby after a Sun-perturbed Moon-to-Moon transfer.
Every escape is recorded with its excess speed, direction and time since the burn.

Writes publications/data/cislunar-flyby/{escapes.npz, reach.json, summary.json}.
reach.json is the table the heliocentric leg optimiser reads (trajectory_opt.FlybyReach).
"""

from __future__ import annotations

import json
import os
import sys
import time
from multiprocessing import Pool

import numpy as np

import cislunar_flyby as c

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'data', 'cislunar-flyby')
BURNS_MS = (50.0, 150.0, 300.0)
ORBITS_KM = (20e3, 100e3, 200e3)  # Sun-side distance of the node orbit from SEL1
T_TOTAL = 220.0  # days from the burn; nothing later is recorded
T_ENCOUNTER = 170.0
BUDGETS = (45.0, 60.0, 75.0, 90.0, 105.0, 120.0, 150.0, 200.0)
LON_EDGES = np.arange(-180.0, 181.0, 30.0)
LAT_EDGES = np.array([0.0, 15.0, 30.0, 45.0, 60.0, 90.0])
LEVELS = np.round(np.arange(0.3, 2.41, 0.05), 2)
MOON_BINS = 12
MIN_MOON_BINS = 2  # a speed counts as reachable if at least two of twelve lunar phases give it


def escapes_of(y, t, src, extra):
    """Fly a batch to escape and return the records of those that do."""
    f = c.integrate(y, t, T_TOTAL * c.DAY)
    ok = f.status == 1
    v, lon, lat, c3 = c.escape_state(f.y[ok])
    keep = c3 > 0
    return {'vinf': v[keep], 'lon': lon[keep], 'lat': np.abs(lat[keep]), 'days': f.t[ok][keep] * c.TU_DAYS,
            't_esc': f.t[ok][keep], 'src': src[ok][keep], **{k: v_[ok][keep] for k, v_ in extra.items()}}


def chunk(args):
    yc, tc, quick = args
    out = []
    _, _, th1 = c.encounter_vinf(yc)
    fan, idx = c.swingby_fan(yc, *( (6, 7) if quick else (10, 13)))
    e = escapes_of(fan, tc[idx], idx, {})
    e['moon'] = th1[e['src']] + (c.N_MOON - 1.0) * (e['t_esc'] - tc[e['src']])
    e['swingbys'] = np.ones(len(e['vinf']), int)
    e['first_days'] = tc[e['src']] * c.TU_DAYS
    out.append(e)
    ce, _, y2, t2 = c.moon_to_moon(yc, tc, np.full(len(yc), T_TOTAL * c.DAY), n_delta=121 if quick else 241)
    if len(ce):
        _, _, th2 = c.encounter_vinf(y2)
        fan, idx = c.swingby_fan(y2, *((6, 7) if quick else (10, 13)))
        e = escapes_of(fan, t2[idx], idx, {})
        e['moon'] = th2[e['src']] + (c.N_MOON - 1.0) * (e['t_esc'] - t2[e['src']])
        e['swingbys'] = np.full(len(e['vinf']), 2)
        e['first_days'] = tc[ce[e['src']]] * c.TU_DAYS
        out.append(e)
    keys = ('vinf', 'lon', 'lat', 'days', 'moon', 'swingbys', 'first_days')
    return {k: np.concatenate([o[k] for o in out]) for k in keys}, len(ce)


def reach_table(e, budget):
    """Largest excess speed per direction bin reached within `budget` days of the burn. Each
    solution needs the Moon at one phase, which comes round once a synodic month; a speed
    counts only if two of twelve phase bins reach it, so one stray solution cannot set it."""
    tab = np.zeros((len(LON_EDGES) - 1, len(LAT_EDGES) - 1))
    sel = e['days'] <= budget
    li = np.clip(np.digitize(e['lon'][sel], LON_EDGES) - 1, 0, tab.shape[0] - 1)
    bi = np.clip(np.digitize(e['lat'][sel], LAT_EDGES) - 1, 0, tab.shape[1] - 1)
    mi = (np.floor((e['moon'][sel] % (2 * np.pi)) / (2 * np.pi) * MOON_BINS).astype(int)) % MOON_BINS
    v = e['vinf'][sel]
    best = np.zeros(tab.shape + (MOON_BINS,))
    np.maximum.at(best, (li, bi, mi), v)
    srt = np.sort(best, axis=2)[:, :, ::-1]
    return srt[:, :, MIN_MOON_BINS - 1]


def main():
    quick = '--quick' in sys.argv
    os.makedirs(OUT, exist_ok=True)
    summary = {'model': 'Sun-Earth CR3BP, planar Lyapunov node orbits about SEL1, patched lunar swingbys (100 km), up to two swingbys',
               'burns_ms': list(BURNS_MS), 'node_orbits_km': list(ORBITS_KM), 'by_burn': {}}
    reach = {'lon_edges': LON_EDGES.tolist(), 'lat_edges': LAT_EDGES.tolist(), 'budgets_days': list(BUDGETS), 'vinf_kms': {}}
    store = {}
    for dv in BURNS_MS:
        t0 = time.time()
        ys = np.concatenate([c.node_departures(ax, *((8, 12) if quick else (16, 24)), dv)[0] for ax in ORBITS_KM])
        f = c.integrate(ys, 0.0, T_TOTAL * c.DAY, crossings=12)
        hit = np.isfinite(f.t_cross) & (f.t_cross < T_ENCOUNTER * c.DAY)
        rows, cols = np.nonzero(hit)
        yc, tc = f.y_cross[rows, cols], f.t_cross[rows, cols]
        first = f.t_cross[:, 0] * c.TU_DAYS
        parts = [(yc[s : s + 60], tc[s : s + 60], quick) for s in range(0, len(yc), 60)]
        with Pool(min(7, os.cpu_count() or 2)) as pool:
            res = pool.map(chunk, parts, chunksize=1)
        e = {k: np.concatenate([r[0][k] for r in res]) for k in res[0][0]}
        n_mm = sum(r[1] for r in res)
        store.update({f'{k}_{int(dv)}': v for k, v in e.items()})
        tabs = {str(int(b)): np.round(reach_table(e, b), 3) for b in BUDGETS}
        reach['vinf_kms'][str(int(dv))] = {k: v.tolist() for k, v in tabs.items()}
        one, two = e['swingbys'] == 1, e['swingbys'] == 2
        summary['by_burn'][str(int(dv))] = {
            'departures': len(ys), 'reach_the_moon': int(np.isfinite(first).sum()),
            'days_to_first_encounter': {p: round(float(np.nanpercentile(first, q)), 1) for p, q in (('min', 0), ('P10', 10), ('P50', 50))},
            'encounters': len(yc), 'moon_to_moon_transfers': int(n_mm), 'escapes': int(len(e['vinf'])),
            'max_vinf_one_swingby': round(float(e['vinf'][one].max()), 3),
            'max_vinf_two_swingbys': round(float(e['vinf'][two].max()), 3) if two.any() else None,
            'fastest_escape_days': {f'vinf>={v}': round(float(e['days'][e['vinf'] >= v].min()), 1) if (e['vinf'] >= v).any() else None for v in (0.5, 1.0, 1.4)},
            'in_plane_reach_by_budget': {str(int(b)): {'min': float(tabs[str(int(b))][:, 0].min()), 'median': float(np.median(tabs[str(int(b))][:, 0])),
                                                         'max': float(tabs[str(int(b))][:, 0].max())} for b in BUDGETS},
            'reach_by_latitude_at_120d': {f'{int(LAT_EDGES[k])}-{int(LAT_EDGES[k + 1])}': {'median': float(np.median(tabs['120'][:, k])), 'max': float(tabs['120'][:, k].max())}
                                            for k in range(len(LAT_EDGES) - 1)},
        }
        print(f'burn {dv:.0f} m/s  {time.time() - t0:.0f}s', json.dumps(summary['by_burn'][str(int(dv))], indent=1), flush=True)
    tag = '-quick' if quick else ''
    np.savez_compressed(os.path.join(OUT, f'escapes{tag}.npz'), **{k: v.astype(np.float32) for k, v in store.items()})
    json.dump(reach, open(os.path.join(OUT, f'reach{tag}.json'), 'w'))
    json.dump(summary, open(os.path.join(OUT, f'summary{tag}.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
