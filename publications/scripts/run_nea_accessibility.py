"""
Run the rq-0-52 accessibility screen on the JPL SBDB NEA catalogue.

    python run_nea_accessibility.py [--quick]

Reads publications/data/nea-catalogue/sbdb_neo_raw.json (or .json.gz); writes
candidates.csv and summary.json next to it. --quick uses a coarser date grid.

Low-thrust factor: the run uses k = 1.15. Because the Δv test is k × impulsive ≤ cap, a
count at cap L and k = 1.15 equals the count at cap L × k'/1.15 for another k' (the
burn-time check aside), so the leg-cap columns double as the k sensitivity.
"""

from __future__ import annotations

import csv
import gzip
import json
import os
import sys
import time

import numpy as np

from nea_accessibility import Criteria, elements, load_catalogue, metal_plausible, prefilter, screen

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', 'data', 'nea-catalogue')
LAUNCH_VINF = (0.0, 1.5, 3.16)  # km/s; 3.16 = C3 10 km²/s²
LEG_CAPS = (5.0, 5.75, 6.5, 7.5)  # km/s low-thrust per leg (5.0 = bom-0-4 storage envelope)
CYCLE_CAPS = (3.0, 4.0, 5.0, 6.0)  # years (3.0 = bom-0-4 KDP-0B criterion)


def catalogue_path() -> str:
    raw = os.path.join(DATA, 'sbdb_neo_raw.json')
    if os.path.exists(raw):
        return raw
    tmp = os.path.join(DATA, '.sbdb_neo_raw.json')
    with gzip.open(raw + '.gz', 'rb') as f, open(tmp, 'wb') as o:
        o.write(f.read())
    return tmp


def main():
    quick = '--quick' in sys.argv
    rows = load_catalogue(catalogue_path())
    cand = prefilter(rows, h_max=23.0)
    el = elements(cand)
    c = Criteria(dep_step_days=30.0 if quick else 15.0)
    print(f'{len(rows)} NEAs; {len(cand)} pass the orbit prefilter with H <= 23')
    t0 = time.time()
    res = screen(el, c, launch_vinf=LAUNCH_VINF, leg_caps=LEG_CAPS)
    print(f'screen {time.time() - t0:.0f}s')

    H = np.array([r['H'] for r in cand])
    rot = np.array([r['rot_per'] for r in cand])
    mp = [metal_plausible(r['taxonomy']) for r in cand]
    metal = np.array([m is True for m in mp])
    unclassified = np.array([m is None for m in mp])
    rot_ok = ~np.isfinite(rot) | (rot >= 4.0)
    size = {'H22': H <= 22.0, 'H23': H <= 23.0}

    scout_tab = {
        f'vinf={v}': {f'cap={cap}': {s: int(((res.scout_dv[v] <= cap) & m).sum()) for s, m in size.items()} for cap in (3.5, 4.5, 5.5)}
        for v in LAUNCH_VINF
    }
    tug_tab = {
        f'leg={L}': {f'cycle<={Y}': {s: int(((res.cycle_years[L] <= Y) & m).sum()) for s, m in size.items()} for Y in CYCLE_CAPS}
        for L in LEG_CAPS
    }

    def joint(scout_cap, v, L, Y, extra=True):
        return (res.scout_dv[v] <= scout_cap) & (res.cycle_years[L] <= Y) & extra

    joint_tab = {}
    for (sc, v, L, Y) in [
        (3.5, 0.0, 5.0, 3.0),  # consensus budgets as written
        (4.5, 0.0, 5.0, 3.0),
        (3.5, 3.16, 5.0, 3.0),
        (3.5, 3.16, 5.0, 4.0),
        (3.5, 3.16, 5.75, 4.0),
        (3.5, 3.16, 6.5, 4.0),
        (3.5, 3.16, 6.5, 5.0),
        (4.5, 3.16, 7.5, 5.0),
    ]:
        key = f'scout<={sc}@vinf{v} tug leg<={L} cycle<={Y}'
        j = joint(sc, v, L, Y)
        joint_tab[key] = {
            'H22': int((j & size['H22']).sum()),
            'H23': int(j.sum()),
            'H22_metal_taxonomy': int((j & size['H22'] & metal).sum()),
            'H22_unclassified': int((j & size['H22'] & unclassified).sum()),
            'H22_unclassified_rot_ok': int((j & size['H22'] & unclassified & rot_ok).sum()),
            'H22_non_metal_taxonomy': int((j & size['H22'] & ~metal & ~unclassified).sum()),
        }

    best_leg = {f'{L}': (float(np.nanmin(np.where(size['H22'], res.cycle_years[L], np.nan))) if np.isfinite(np.where(size['H22'], res.cycle_years[L], np.inf)).any() else None) for L in LEG_CAPS}
    summary = {
        'catalogue': 'JPL SBDB Query API (sb-group=neo), retrieved 2026-10-25',
        'catalogue_count': len(rows),
        'prefilter': 'i <= 12 deg, e <= 0.45, 0.6 <= a <= 1.8 AU, H <= 23',
        'prefiltered': len(cand),
        'prefiltered_H22': int(size['H22'].sum()),
        'classified_in_prefilter_H22': int((size['H22'] & ~unclassified).sum()),
        'metal_taxonomy_in_prefilter_H22': int((size['H22'] & metal).sum()),
        'model': {'k_lowthrust': c.k_lowthrust, 'dep_step_days': c.dep_step_days, 'tofs_days': list(c.tofs_days),
                  'min_stay_days': c.min_stay_days, 'cycles_start': [c.first_year, c.last_year]},
        'scout_reachable': scout_tab,
        'tug_cycles': tug_tab,
        'joint': joint_tab,
        'shortest_cycle_years_H22_by_leg_cap': best_leg,
    }
    json.dump(summary, open(os.path.join(DATA, 'summary.json'), 'w'), indent=2)
    print(json.dumps({k: summary[k] for k in ('joint', 'shortest_cycle_years_H22_by_leg_cap')}, indent=1))

    out = os.path.join(DATA, 'candidates.csv')
    keep = (res.scout_dv[3.16] <= 4.5) | (res.cycle_years[7.5] <= 6.0)
    order = np.lexsort((res.scout_dv[3.16], np.where(np.isfinite(res.cycle_years[6.5]), res.cycle_years[6.5], 99)))
    with open(out, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['pdes', 'name', 'H', 'diameter_km', 'albedo', 'rot_per_h', 'taxonomy', 'metal_plausible', 'a', 'e', 'i_deg',
                    'scout_dv_c3_0', 'scout_dv_c3_10'] + [f'cycle_yr_leg{L}' for L in LEG_CAPS] + ['departs_leg6.5', 'out_dv_leg6.5', 'in_dv_leg6.5'])
        fmt = lambda x: round(float(x), 3) if np.isfinite(x) else ''
        for j in order:
            if not keep[j]:
                continue
            r = cand[j]
            m = metal_plausible(r['taxonomy'])
            d = res.cycle_detail[6.5][j] or {}
            w.writerow([r['pdes'], r['full_name'].strip(), r['H'], fmt(r['diameter']), fmt(r['albedo']), fmt(r['rot_per']), r['taxonomy'],
                        '' if m is None else int(m), round(r['a'], 4), round(r['e'], 4), round(r['i'], 3),
                        fmt(res.scout_dv[0.0][j]), fmt(res.scout_dv[3.16][j])] + [fmt(res.cycle_years[L][j]) for L in LEG_CAPS]
                       + [d.get('departs', ''), d.get('out_dv', ''), d.get('in_dv', '')])
    print('wrote', out, int(keep.sum()), 'rows')


if __name__ == '__main__':
    main()
