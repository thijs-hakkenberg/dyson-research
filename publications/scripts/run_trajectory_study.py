"""
rq-0-52, second pass: which asteroids close a tug cycle once multi-revolution transfers,
lunar gravity assists and optimised low-thrust legs are modelled.

    python run_trajectory_study.py [--quick]

Stage 1  every asteroid passing the orbit prefilter: impulsive transfers with 0–2
         revolutions and a lunar-assist credit at the Earth end, × the first screen's
         low-thrust factor, for comparison with that screen.
Stage 2  the shortlist: each candidate leg re-solved as a low-thrust optimisation
         (trajectory_opt.low_thrust_leg), then the shortest SEL1 → asteroid → SEL1 cycle
         assembled from the legs that are feasible for the tug.

Writes publications/data/nea-trajectories/{summary.json, targets.csv, legs.csv}.
"""

from __future__ import annotations

import csv
import json
import os
import sys
import time
import warnings
from multiprocessing import Pool

import numpy as np

from nea_accessibility import (J2000, SCOUT, TUG_IN, TUG_OUT, Criteria, best_cycle, burn_fits, elements, jd,
                               load_catalogue, metal_plausible, prefilter)
from run_nea_accessibility import catalogue_path
from trajectory_opt import REV_OPTIONS, impulsive_tables, low_thrust_leg, seed_velocities

warnings.simplefilter('ignore')
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'data', 'nea-trajectories')

LGA = (0.0, 1.0, 1.5)  # km/s of Earth-relative excess speed a lunar assist is taken to give
SCOUT_LAUNCH = (0.0, 1.0, 1.5, 3.16)  # km/s; 1.0–1.5 = lunar assist from a C3≈0 launch; 3.16 = C3 10
LEG_CAPS = (5.0, 5.75, 6.5, 7.5)
CYCLE_CAPS = (3.0, 4.0, 5.0, 6.0)
LGA_DAYS = 30.0  # phasing allowance per assisted leg
SHORTLIST = 150
K1 = 1.15  # the first screen's low-thrust factor, used in stage 1 only
DUTY = 0.85
MIN_STAY = 60.0
C = Criteria()
TOFS = np.asarray(C.tofs_days, float)
YEAR = lambda t: 2000 + (t - J2000) / 365.25


def grids(step):
    return (np.arange(jd(C.first_year), jd(C.last_year), step),
            np.arange(jd(C.first_year), jd(C.last_year + 7.0), step))


# ----------------------------------------------------------------------------- stage 1

def stage1_chunk(args):
    sub, step = args
    t_dep, t_ret = grids(step)
    out = impulsive_tables(sub, t_dep, TOFS, True, credits=sorted(set(LGA) | set(SCOUT_LAUNCH)))
    ret = impulsive_tables(sub, t_ret, TOFS, False, credits=LGA)
    n = len(sub['a'])
    tf = TOFS[None, None, :]
    scout = {}
    for v in SCOUT_LAUNCH:
        dv = out[v][0] * K1
        dv = np.where(burn_fits(dv, tf, SCOUT, DUTY), dv, np.inf)
        scout[v] = dv.min(axis=(1, 2))
    cyc = {}
    for g in LGA:
        o, r = out[g][0] * K1, ret[g][0] * K1
        of, rf = burn_fits(o, tf, TUG_OUT, DUTY), burn_fits(r, tf, TUG_IN, DUTY)
        pen = 2 * LGA_DAYS if g > 0 else 0.0
        for L in LEG_CAPS:
            c = np.full(n, np.inf)
            for j in range(n):
                d, _ = best_cycle((o[j] <= L) & of[j], (r[j] <= L) & rf[j], t_dep, t_ret, TOFS, MIN_STAY)
                c[j] = (d + pen) / 365.25
            cyc[(g, L)] = c
    return scout, cyc


# ----------------------------------------------------------------------------- stage 2

def pick_seeds(dv, which, t_grid, max_dv, per_bin=2, bin_days=60.0, limit=40):
    """Candidate (departure, tof) cells for one asteroid and one leg: per departure bin the
    lowest-Δv cell and the shortest cell under max_dv."""
    D, T = dv.shape
    seeds = {}
    bins = ((t_grid - t_grid[0]) // bin_days).astype(int)
    for b in np.unique(bins):
        idx = np.nonzero(bins == b)[0]
        block = dv[idx]
        if not np.isfinite(block).any() or block.min() > max_dv:
            continue
        d, t = np.unravel_index(np.argmin(block), block.shape)
        seeds[(idx[d], t)] = block[d, t]
        ok = np.nonzero(block <= max_dv)
        if ok[0].size and per_bin > 1:
            k = np.argmin(ok[1])  # shortest flight time under the limit
            seeds[(idx[ok[0][k]], ok[1][k])] = block[ok[0][k], ok[1][k]]
    items = sorted(seeds.items(), key=lambda kv: kv[1])[:limit]
    return [(int(d), int(t), float(v), int(which[d, t])) for (d, t), v in items]


def stage2_target(args):
    el1, step, name = args
    t_dep, t_ret = grids(step)
    one = {k: np.asarray([v]) for k, v in el1.items()}
    out = impulsive_tables(one, t_dep, TOFS, True, credits=sorted(set(LGA) | set(SCOUT_LAUNCH)))
    ret = impulsive_tables(one, t_ret, TOFS, False, credits=LGA)
    legs = []
    for g in LGA:
        for outbound, tab, grid, veh in ((True, out[g], t_dep, TUG_OUT), (False, ret[g], t_ret, TUG_IN)):
            for d, t, imp, rev in pick_seeds(tab[0][0], tab[1][0], grid, 7.5):
                r1, vs1, r2, vs2, v1, v2 = seed_velocities(el1, grid[d], TOFS[t], outbound, g > 0, rev)
                if not np.all(np.isfinite(v1)):
                    continue
                res = low_thrust_leg(r1, vs1, r2, vs2, TOFS[t], veh.accel, DUTY, seed=(v1, v2),
                                     free_end=('start' if outbound else 'end') if g > 0 else None, lga_vinf_kms=g)
                legs.append({'target': name, 'lga': g, 'leg': 'out' if outbound else 'in', 'depart': float(grid[d]),
                             'tof': float(TOFS[t]), 'revs': REV_OPTIONS[rev][0], 'impulsive': imp,
                             'low_thrust': res.dv_kms if res.ok else None, 'thrust_fraction': res.thrust_fraction if res.ok else None})
    scout = {}
    for v in SCOUT_LAUNCH:
        best = np.inf
        for d, t, imp, rev in pick_seeds(out[v][0][0], out[v][1][0], t_dep, 5.5, per_bin=1, limit=16):
            r1, vs1, r2, vs2, v1, v2 = seed_velocities(el1, t_dep[d], TOFS[t], True, v > 0, rev)
            if not np.all(np.isfinite(v1)):
                continue
            res = low_thrust_leg(r1, vs1, r2, vs2, TOFS[t], SCOUT.accel, DUTY, seed=(v1, v2),
                                 free_end='start' if v > 0 else None, lga_vinf_kms=v)
            if res.ok:
                best = min(best, res.dv_kms)
        scout[v] = best
    return name, legs, scout


def assemble(legs, g, cap):
    """Shortest cycle (years) from optimised legs for one lunar-assist setting and Δv cap."""
    outs = [l for l in legs if l['lga'] == g and l['leg'] == 'out' and l['low_thrust'] is not None and l['low_thrust'] <= cap]
    ins = [l for l in legs if l['lga'] == g and l['leg'] == 'in' and l['low_thrust'] is not None and l['low_thrust'] <= cap]
    best = None
    pen = 2 * LGA_DAYS if g > 0 else 0.0
    for o in outs:
        arrive = o['depart'] + o['tof']
        for i in ins:
            if i['depart'] >= arrive + MIN_STAY:
                cyc = (i['depart'] + i['tof'] - o['depart'] + pen) / 365.25
                if best is None or cyc < best[0]:
                    best = (cyc, o, i)
    return best


def windows(legs, g, cap, cycle_cap):
    """Distinct departure years with a cycle no longer than cycle_cap."""
    outs = [l for l in legs if l['lga'] == g and l['leg'] == 'out' and l['low_thrust'] is not None and l['low_thrust'] <= cap]
    ins = [l for l in legs if l['lga'] == g and l['leg'] == 'in' and l['low_thrust'] is not None and l['low_thrust'] <= cap]
    pen = 2 * LGA_DAYS if g > 0 else 0.0
    yrs = set()
    for o in outs:
        arrive = o['depart'] + o['tof']
        if any(i['depart'] >= arrive + MIN_STAY and (i['depart'] + i['tof'] - o['depart'] + pen) / 365.25 <= cycle_cap for i in ins):
            yrs.add(int(YEAR(o['depart'])))
    return sorted(yrs)


def main():
    quick = '--quick' in sys.argv
    step = 30.0 if quick else 20.0
    os.makedirs(OUT, exist_ok=True)
    rows = load_catalogue(catalogue_path())
    cand = prefilter(rows, h_max=23.0)
    if quick:
        cand = cand[::6]
    el = elements(cand)
    H = np.array([r['H'] for r in cand])
    h22 = H <= 22.0
    N = len(cand)
    print(f'{len(rows)} NEAs; {N} in the prefilter (H <= 23), {int(h22.sum())} with H <= 22', flush=True)

    cache = os.path.join(OUT, 'stage1-quick.npz' if quick else 'stage1.npz')
    if os.path.exists(cache) and '--fresh' not in sys.argv:
        z = np.load(cache)
        assert list(z['pdes']) == [r['pdes'] for r in cand], 'stage 1 cache does not match the catalogue; rerun with --fresh'
        scout1 = {v: z[f'scout_{v}'] for v in SCOUT_LAUNCH}
        cyc1 = {(g, L): z[f'cyc_{g}_{L}'] for g in LGA for L in LEG_CAPS}
        print('stage 1 from cache', flush=True)
    else:
        t0 = time.time()
        chunks = [({k: v[s : s + 40] for k, v in el.items()}, step) for s in range(0, N, 40)]
        with Pool(min(7, os.cpu_count() or 2)) as pool:
            parts = pool.map(stage1_chunk, chunks)
        scout1 = {v: np.concatenate([p[0][v] for p in parts]) for v in SCOUT_LAUNCH}
        cyc1 = {key: np.concatenate([p[1][key] for p in parts]) for key in parts[0][1]}
        np.savez_compressed(cache, pdes=np.array([r['pdes'] for r in cand]), **{f'scout_{v}': scout1[v] for v in SCOUT_LAUNCH},
                            **{f'cyc_{g}_{L}': cyc1[(g, L)] for g in LGA for L in LEG_CAPS})
        print(f'stage 1 {time.time() - t0:.0f}s', flush=True)

    stage1 = {
        'scout_reachable_H22': {f'launch_vinf={v}': {f'cap={cap}': int(((scout1[v] <= cap) & h22).sum()) for cap in (3.5, 4.5, 5.5)} for v in SCOUT_LAUNCH},
        'tug_cycles_H22': {f'lga={g}': {f'leg={L}': {f'cycle<={Y}': int(((cyc1[(g, L)] <= Y) & h22).sum()) for Y in CYCLE_CAPS} for L in LEG_CAPS} for g in LGA},
    }
    print(json.dumps(stage1['tug_cycles_H22'], indent=None), flush=True)

    # shortlist: H <= 22 objects that close within 6 years at the loosest stage-1 setting,
    # ranked by their cycle with a 1.0 km/s lunar assist and 6.5 km/s legs, then the loosest
    loose = np.minimum.reduce([cyc1[(g, 7.5)] for g in LGA])
    eligible = h22 & np.isfinite(loose) & (loose <= 6.0)
    order = np.lexsort((loose, np.where(np.isfinite(cyc1[(1.0, 6.5)]), cyc1[(1.0, 6.5)], 99)))
    short = [int(j) for j in order if eligible[j]][: (12 if quick else SHORTLIST)]
    print(f'shortlist {len(short)} of {int(eligible.sum())} eligible (H <= 22)', flush=True)

    t0 = time.time()
    jobs = [({k: float(el[k][j]) for k in el}, step, cand[j]['pdes']) for j in short]
    with Pool(min(7, os.cpu_count() or 2)) as pool:
        res2 = pool.map(stage2_target, jobs, chunksize=1)
    print(f'stage 2 {time.time() - t0:.0f}s', flush=True)

    all_legs, targets = [], []
    ratios = {'out': [], 'in': []}
    solved = {'out': [0, 0], 'in': [0, 0]}
    for j, (name, legs, scout) in zip(short, res2):
        all_legs += legs
        for l in legs:
            solved[l['leg']][1] += 1
            if l['low_thrust'] is not None:
                solved[l['leg']][0] += 1
                if l['impulsive'] > 0.5:
                    ratios[l['leg']].append(l['low_thrust'] / l['impulsive'])
        r = cand[j]
        m = metal_plausible(r['taxonomy'])
        row = {'pdes': name, 'name': r['full_name'].strip(), 'H': r['H'], 'taxonomy': r['taxonomy'],
               'metal_plausible': '' if m is None else int(m), 'rot_per_h': r['rot_per'] if np.isfinite(r['rot_per']) else '',
               'a': round(r['a'], 4), 'e': round(r['e'], 4), 'i_deg': round(r['i'], 3)}
        for v in SCOUT_LAUNCH:
            row[f'scout_dv_vinf{v}'] = round(scout[v], 3) if np.isfinite(scout[v]) else ''
        for g in LGA:
            for L in LEG_CAPS:
                b = assemble(legs, g, L)
                row[f'cycle_lga{g}_leg{L}'] = round(b[0], 3) if b else ''
                if L == 6.5:
                    row[f'out_dv_lga{g}'] = round(b[1]['low_thrust'], 3) if b else ''
                    row[f'in_dv_lga{g}'] = round(b[2]['low_thrust'], 3) if b else ''
                    row[f'departs_lga{g}'] = round(YEAR(b[1]['depart']), 2) if b else ''
                    row[f'windows_4yr_lga{g}'] = ' '.join(map(str, windows(legs, g, L, 4.0)))
        targets.append(row)

    def num(row, key):
        return row[key] if row[key] != '' else np.inf

    is22 = {cand[j]['pdes']: bool(h22[j]) for j in short}
    stage2 = {}
    for g in LGA:
        stage2[f'lga={g}'] = {
            f'leg={L}': {f'cycle<={Y}': int(sum(num(t, f'cycle_lga{g}_leg{L}') <= Y and is22[t['pdes']] for t in targets)) for Y in CYCLE_CAPS}
            for L in LEG_CAPS
        }
    joint = {}
    for (sv, sc, g, L, Y) in [(0.0, 3.5, 0.0, 5.0, 3.0), (3.16, 3.5, 0.0, 6.5, 4.0), (1.0, 3.5, 1.0, 5.0, 3.0), (1.0, 3.5, 1.0, 5.0, 4.0),
                             (1.0, 3.5, 1.0, 6.5, 4.0), (1.5, 3.5, 1.5, 5.0, 3.0), (1.5, 3.5, 1.5, 5.0, 4.0), (1.5, 3.5, 1.5, 6.5, 4.0),
                             (3.16, 3.5, 1.5, 5.0, 4.0), (3.16, 3.5, 1.5, 6.5, 4.0), (3.16, 4.5, 1.5, 6.5, 5.0)]:
        sel = [t for t in targets if is22[t['pdes']] and num(t, f'scout_dv_vinf{sv}') <= sc and num(t, f'cycle_lga{g}_leg{L}') <= Y]
        joint[f'scout<={sc}@vinf{sv} tug lga={g} leg<={L} cycle<={Y}'] = {
            'H22': len(sel), 'metal_taxonomy': sum(t['metal_plausible'] == 1 for t in sel), 'unclassified': sum(t['metal_plausible'] == '' for t in sel)}

    q = lambda a: [round(float(x), 3) for x in np.percentile(a, [10, 50, 90])] if len(a) else None
    summary = {
        'method': 'stage 1: impulsive, 0-2 revolutions, lunar-assist credit, x1.15; stage 2: Sims-Flanagan low thrust (20 segments, SOCP) on the shortlist',
        'assumptions': {'lunar_assist_vinf_kms': list(LGA), 'lunar_assist_days_per_leg': LGA_DAYS, 'tug_accel_out_ms2': TUG_OUT.accel,
                        'tug_accel_in_ms2': TUG_IN.accel, 'scout_accel_ms2': SCOUT.accel, 'duty': DUTY, 'min_stay_days': MIN_STAY,
                        'dep_step_days': step, 'tofs_days': list(C.tofs_days), 'cycles_start': [C.first_year, C.last_year]},
        'prefiltered_H23': N, 'prefiltered_H22': int(h22.sum()), 'shortlist': len(short), 'shortlist_eligible': int(eligible.sum()),
        'stage1': stage1,
        'stage2_tug_cycles_H22': stage2,
        'stage2_joint': joint,
        'low_thrust_over_impulsive_p10_p50_p90': {k: q(v) for k, v in ratios.items()},
        'legs_solved': {k: {'feasible': v[0], 'attempted': v[1]} for k, v in solved.items()},
    }
    json.dump(summary, open(os.path.join(OUT, 'summary.json'), 'w'), indent=2)
    targets.sort(key=lambda t: (num(t, 'cycle_lga1.0_leg6.5'), num(t, 'cycle_lga1.5_leg7.5')))
    with open(os.path.join(OUT, 'targets.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(targets[0].keys()))
        w.writeheader()
        w.writerows(targets)
    with open(os.path.join(OUT, 'legs.csv'), 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['target', 'lga_vinf', 'leg', 'depart_year', 'tof_days', 'revs', 'impulsive_kms', 'low_thrust_kms', 'thrust_fraction'])
        for l in all_legs:
            if l['low_thrust'] is not None:
                w.writerow([l['target'], l['lga'], l['leg'], round(YEAR(l['depart']), 3), l['tof'], l['revs'], round(l['impulsive'], 3),
                            round(l['low_thrust'], 3), round(l['thrust_fraction'], 3)])
    print(json.dumps({k: summary[k] for k in ('stage2_tug_cycles_H22', 'stage2_joint', 'low_thrust_over_impulsive_p10_p50_p90', 'legs_solved')}, indent=1))


if __name__ == '__main__':
    main()
