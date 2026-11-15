"""
rq-0-52: the lunar flyby from the SEL1 node with halo node orbits and the Moon on its
inclined orbit (extension of run_cislunar_flyby.py).

    python run_cislunar_flyby_3d.py [--quick]

Two things change from the planar model:

  * the Moon's orbit is tilted 5.1° to the ecliptic, so a departure meets the Moon only
    where its path crosses the Moon's orbit plane. The out-of-plane part of the burn is
    solved for that. The direction of the Moon's node line from the Sun–Earth line turns
    once a year, so the reach depends on the date; it is tabulated by that angle;
  * node orbits include northern halo orbits (120,000 and 300,000 km above the ecliptic)
    next to the planar orbits of the first model.

One swingby only: in the planar model the second swingby added at most 0.07 km/s to the
reach in any direction band.

Writes publications/data/cislunar-flyby/{reach-3d-planar-orbits.json, reach-3d-halo.json,
summary-3d.json, escapes-3d.npz}. The reach files are read by trajectory_opt.FlybyReach.
"""

from __future__ import annotations

import json
import os
import sys
import time
from multiprocessing import Pool

import numpy as np

import cislunar_flyby as c
from run_cislunar_flyby import BUDGETS, BURNS_MS, LON_EDGES, MIN_MOON_BINS, MOON_BINS, OUT, T_ENCOUNTER, T_TOTAL

ORBITS = (('planar', 20e3), ('planar', 100e3), ('planar', 200e3), ('halo', 120e3), ('halo', 300e3))
NODE_EDGES = np.arange(0.0, 361.0, 60.0)  # node angle at escape, degrees
LAT_EDGES_SIGNED = np.array([-90.0, -60.0, -45.0, -30.0, -15.0, 0.0, 15.0, 30.0, 45.0, 60.0, 90.0])
KEYS = ('vinf', 'lon', 'lat', 'days', 'moon', 'node', 'orbit', 'first_days', 'elev')


def grid(quick):
    """(phases round the orbit, burn azimuths, points per out-of-plane grid, node angles at the burn, swingby fan)"""
    if quick:
        return 6, 8, 5, np.radians([0.0, 180.0]), (5, 8)
    return 16, 24, 9, np.radians(np.arange(0.0, 360.0, 60.0)), (10, 24)


INPLANE = (0.98, 0.8, 0.5)  # share of the burn in the ecliptic; the rest is free to aim at the Moon's plane


def chunk(args):
    base, az, orbit, dv, quick, inc, shares = args
    _, _, n_up, nodes, fan_n = grid(quick)
    M = len(base)
    idx = np.repeat(np.arange(M), n_up)
    out = {k: [] for k in KEYS}
    n_enc = 0
    first = np.full(M, np.inf)
    cases = []
    for share in shares:
        ups = np.linspace(-1.0, 1.0, n_up if share < 1 else 2) * np.sqrt(1 - share**2)
        idx = np.repeat(np.arange(M), len(ups))
        flights = c.integrate(c.burn_states(base[idx], az[idx], np.tile(ups, M), dv, share), 0.0, T_ENCOUNTER * c.DAY, crossings=12)
        cases += [(share, ups, flights, node0) for node0 in (nodes if inc > 0 else nodes[:1])]
    for share, ups, flights, node0 in cases:
        ce, el, yc, tc = c.encounters_inclined(base, az, ups, dv, node0, T_ENCOUNTER * c.DAY, inc=inc, flights=flights, inplane=share)
        if not len(ce):
            continue
        n_enc += len(ce)
        np.minimum.at(first, ce, tc * c.TU_DAYS)
        _, _, place = c.encounter_vinf_inclined(yc, tc, node0, inc)
        fan, src = c.swingby_fan_inclined(yc, tc, node0, *fan_n, inc=inc)
        f = c.integrate(fan, tc[src], T_TOTAL * c.DAY)
        ok = f.status == 1
        v, lon, lat, c3 = c.escape_state(f.y[ok])
        keep = c3 > 0
        s, te = src[ok][keep], f.t[ok][keep]
        out['vinf'].append(v[keep])
        out['lon'].append(lon[keep])
        out['lat'].append(lat[keep])
        out['days'].append(te * c.TU_DAYS)
        out['moon'].append(place[s] + (c.N_MOON - 1.0) * (te - tc[s]))
        out['node'].append(np.degrees(node0 - te) % 360.0)
        out['orbit'].append(orbit[ce[s]])
        out['first_days'].append(tc[s] * c.TU_DAYS)
        out['elev'].append(np.degrees(np.arctan2(el[s], share)))
    return {k: np.concatenate(v) if v else np.zeros(0) for k, v in out.items()}, n_enc, first


def reach_table_3d(e, budget):
    """Largest excess speed per (node angle, longitude, signed latitude) bin reached within
    `budget` days by at least MIN_MOON_BINS of the twelve lunar-phase bins."""
    shape = (len(NODE_EDGES) - 1, len(LON_EDGES) - 1, len(LAT_EDGES_SIGNED) - 1)
    sel = e['days'] <= budget
    ni = np.clip(np.digitize(e['node'][sel], NODE_EDGES) - 1, 0, shape[0] - 1)
    li = np.clip(np.digitize(e['lon'][sel], LON_EDGES) - 1, 0, shape[1] - 1)
    bi = np.clip(np.digitize(e['lat'][sel], LAT_EDGES_SIGNED) - 1, 0, shape[2] - 1)
    mi = (np.floor((e['moon'][sel] % (2 * np.pi)) / (2 * np.pi) * MOON_BINS).astype(int)) % MOON_BINS
    best = np.zeros(shape + (MOON_BINS,))
    np.maximum.at(best, (ni, li, bi, mi), e['vinf'][sel])
    return np.sort(best, axis=3)[:, :, :, ::-1][:, :, :, MIN_MOON_BINS - 1]


def by_abs_latitude(tab):
    """Median over node angle and longitude of the reach by |latitude| band (both signs pooled)."""
    n = tab.shape[2] // 2
    return [float(np.median(np.concatenate([tab[:, :, n + k].ravel(), tab[:, :, n - 1 - k].ravel()]))) for k in range(n)]


def main(inc=c.INC_MOON, tag='', shares=INPLANE, orbits=ORBITS):
    quick = '--quick' in sys.argv
    n_phase, n_az, n_up, nodes, _ = grid(quick)
    os.makedirs(OUT, exist_ok=True)
    states = [(kind, a, *(c.lyapunov_orbit(a) if kind == 'planar' else c.halo_orbit(a))) for kind, a in orbits]
    base = np.concatenate([np.repeat(c.orbit_points(s, p, n_phase), n_az, axis=0) for _, _, s, p in states])
    az = np.tile(np.arange(n_az) * 2 * np.pi / n_az, len(states) * n_phase)
    orbit = np.repeat(np.arange(len(states)), n_phase * n_az)
    kinds = {'planar-orbits': [k for k, o in enumerate(orbits) if o[0] == 'planar'], 'halo': [k for k, o in enumerate(orbits) if o[0] == 'halo']}
    reach = {name: {'lon_edges': LON_EDGES.tolist(), 'lat_edges': LAT_EDGES_SIGNED.tolist(), 'node_edges': NODE_EDGES.tolist(),
                    'budgets_days': list(BUDGETS), 'vinf_kms': {}} for name in kinds}
    summary = {'model': 'Sun-Earth CR3BP; planar and halo node orbits about SEL1; Moon on an orbit inclined %.3f deg; one patched swingby (100 km)' % np.degrees(inc),
               'orbits': [{'kind': k, 'size_km': a, 'period_days': round(p * c.TU_DAYS, 2)} for k, a, _, p in states],
               'burns_ms': list(BURNS_MS), 'by_burn': {}}
    store = {}
    step = 24 if quick else 32
    for dv in BURNS_MS:
        t0 = time.time()
        parts = [(base[s : s + step], az[s : s + step], orbit[s : s + step], dv, quick, inc, shares) for s in range(0, len(base), step)]
        with Pool(min(7, os.cpu_count() or 2)) as pool:
            res = pool.map(chunk, parts, chunksize=1)
        e = {k: np.concatenate([r[0][k] for r in res]) for k in KEYS}
        first = np.concatenate([r[2] for r in res])
        store.update({f'{k}_{int(dv)}': v for k, v in e.items()})
        row = {'departures_tried': int(len(base) * n_up * len(shares)), 'encounters': int(sum(r[1] for r in res)), 'escapes': int(len(e['vinf']))}
        for name, members in kinds.items():
            sel = np.isin(e['orbit'], members)
            sub = {k: v[sel] for k, v in e.items()}
            tabs = {str(int(b)): np.round(reach_table_3d(sub, b), 3) for b in BUDGETS}
            reach[name]['vinf_kms'][str(int(dv))] = {k: v.tolist() for k, v in tabs.items()}
            fd = first[np.isin(orbit, members)]
            n = tabs['90'].shape[2] // 2
            if not sel.any():
                continue
            row[name] = {
                'escapes': int(sel.sum()),
                'days_to_first_encounter': {'min': round(float(fd.min()), 1), 'P10': round(float(np.percentile(fd[np.isfinite(fd)], 10)), 1)} if np.isfinite(fd).any() else None,
                'max_vinf': round(float(sub['vinf'].max()), 3) if sel.any() else None,
                'fastest_escape_days': {f'vinf>={v}': round(float(sub['days'][sub['vinf'] >= v].min()), 1) if (sub['vinf'] >= v).any() else None for v in (1.0, 1.4)},
                'burn_elevation_deg_percentiles': {str(p): round(float(np.percentile(np.abs(sub['elev']), p)), 1) for p in (50, 90)} if sel.any() else None,
                'reach_by_abs_latitude': {str(int(b)): dict(zip(('0-15', '15-30', '30-45', '45-60', '60-90'), by_abs_latitude(tabs[str(int(b))]))) for b in BUDGETS},
                'in_plane_reach_by_node_angle_at_90d': {f'{int(NODE_EDGES[k])}-{int(NODE_EDGES[k + 1])}': float(np.median(tabs['90'][k][:, n - 1 : n + 1])) for k in range(len(NODE_EDGES) - 1)},
            }
        summary['by_burn'][str(int(dv))] = row
        print(f'burn {dv:.0f} m/s  {time.time() - t0:.0f}s', json.dumps(row, indent=1), flush=True)
    q = '-quick' if quick else ''
    np.savez_compressed(os.path.join(OUT, f'escapes-3d{tag}{q}.npz'), **{k: v.astype(np.float32) for k, v in store.items()})
    for name in kinds:
        json.dump(reach[name], open(os.path.join(OUT, f'reach-3d-{name}{tag}{q}.json'), 'w'))
    json.dump(summary, open(os.path.join(OUT, f'summary-3d{tag}{q}.json'), 'w'), indent=1)


if __name__ == '__main__':
    if '--inc0' in sys.argv:  # check: no inclination, whole burn in the ecliptic, planar orbits: the first model
        main(inc=0.0, tag='-inc0', shares=(1.0,), orbits=ORBITS[:3])
    else:
        main()
