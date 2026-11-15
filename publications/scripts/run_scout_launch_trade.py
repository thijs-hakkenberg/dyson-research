"""
rq-0-52, scout launch trade, step 2 (open question 1.2): what each way of leaving Earth
costs, and how many targets it keeps.

    python run_scout_launch_sweep.py     # step 1, ~15 min
    python run_scout_launch_trade.py

Reads the sweep and answers four things:

  counts    targets within reach against the scout's Δv budget, for every launch option,
            alone and jointly with the tug cycle (third-pass targets);
  loop      Earth-to-Earth loops under thrust (an Earth flyby in place of launch energy):
            the Δv that turns a lunar-swingby departure into a faster return to Earth;
  pairs     whether two scouts for different asteroids can share one launch to C3 = 10,
            which gives them the same day and the same direction of departure;
  mass      scout wet mass and thruster hours for each Δv budget, a chemical perigee kick,
            and launcher capacity against C3.

Writes publications/data/nea-trajectories/{scout-launch-trade.json, scout-launch-sweep.csv}.
"""

from __future__ import annotations

import csv
import json
import os
from multiprocessing import Pool

import numpy as np

import scout_launch_trade as m
from nea_accessibility import KMS, SCOUT, elements, jd, load_catalogue, prefilter
from run_nea_accessibility import catalogue_path
from run_scout_launch_sweep import SWEEP
from run_trajectory_study import DUTY, OUT, TOFS
from trajectory_opt import REV_OPTIONS, earth_end, lambert_multirev, low_thrust_leg, seed_velocities

BUDGETS = (3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 7.0)
TUG_SETS = ((5.0, 4.0), (5.0, 5.0), (6.5, 4.0), (6.5, 5.0))
SCOUT_LIMIT = 3.5
MOON_REACH = {'moon_low': 1.52, 'moon': 1.78}  # km/s in the ecliptic, from reach-launch*.json
LOOP_DAYS = (330.0, 400.0, 440.0, 480.0, 540.0, 620.0, 700.0, 760.0)
LOOP_C3 = (4, 6, 8, 10, 15)
PAIR_SCREEN = 5.0  # km/s impulsive; pairs above this are not solved


def num(x):
    return float(x) if x not in ('', None) else np.inf


# ----------------------------------------------------------------------------- loop

def loop_job(args):
    """Least Δv of a thrust loop that leaves Earth with at most `v_out` km/s (any direction)
    and returns `days` later with excess velocity `w_in` (km/s, given)."""
    v_out, days, c3, ang, t0 = args
    best = np.inf
    r1, ve1 = earth_end(np.array(t0), True)
    r2, ve2 = earth_end(np.array(t0 + days), True)
    r1, ve1, r2, ve2 = (np.asarray(q, float).reshape(3) for q in (r1, ve1, r2, ve2))
    along = ve2 / np.linalg.norm(ve2)
    radial = r2 / np.linalg.norm(r2)
    radial = radial - along * (radial @ along)
    radial /= np.linalg.norm(radial)
    w = np.sqrt(c3) * (np.cos(ang) * along + np.sin(ang) * radial) / KMS
    for nrev, br in ((1, 0), (1, 1), (2, 0), (2, 1)):
        if nrev == 2 and days < 600:
            continue
        v1, v2 = lambert_multirev(r1[None], r2[None], np.array([days]), nrev, br)
        if not (np.all(np.isfinite(v1)) and np.all(np.isfinite(v2))):
            continue
        res = low_thrust_leg(r1, ve1, r2, ve2 + w, days, SCOUT.accel, DUTY, seed=(v1[0], v2[0]),
                             free_end='start', lga_vinf_kms=v_out)
        if res.ok:
            best = min(best, res.dv_kms)
    return v_out, days, c3, ang, best


def loops(pool):
    t0 = jd(2032.0)
    angs = np.radians(np.arange(0, 360, 15))
    jobs = [(v, d, c3, a, t0 + s) for v in MOON_REACH.values() for d in LOOP_DAYS for c3 in LOOP_C3
            for a in angs for s in (0.0, 91.0)]
    best = {}
    for v, d, c3, a, dv in pool.imap_unordered(loop_job, jobs, chunksize=8):
        k = (v, c3)
        if dv < best.get(k, (np.inf,))[0]:
            best[k] = (dv, d, float(np.degrees(a)))
    return best


# ----------------------------------------------------------------------------- pairs

def pair_job(args):
    """Scout B on scout A's launch: same day, same excess velocity. Least Δv for B."""
    name_a, name_b, sols, el_b = args
    best = np.inf
    for depart, w in sols:
        w_au = np.asarray(w) / KMS
        cands = []
        for tof in TOFS:
            for rev in range(len(REV_OPTIONS)):
                r1, vs1, r2, vs2, v1, v2 = seed_velocities(el_b, depart, tof, True, True, rev)
                if not (np.all(np.isfinite(v1)) and np.all(np.isfinite(v2))):
                    continue
                imp = (np.linalg.norm(v1 - vs1 - w_au) + np.linalg.norm(vs2 - v2)) * KMS
                if imp <= PAIR_SCREEN:
                    cands.append((imp, tof, r1, vs1, r2, vs2, v1, v2))
        cands.sort(key=lambda c: c[0])
        for imp, tof, r1, vs1, r2, vs2, v1, v2 in cands[:3]:
            res = low_thrust_leg(r1, vs1 + w_au, r2, vs2, tof, SCOUT.accel, DUTY, seed=(v1, v2))
            if res.ok:
                best = min(best, res.dv_kms)
    return name_a, name_b, best


def matching(nodes, edges):
    """Disjoint pairs by a greedy choice (fewest partners first): a lower bound on the
    largest pairing, so the launch count from it is an upper bound."""
    adj = {n: set() for n in nodes}
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    used, n = set(), 0
    for a in sorted(nodes, key=lambda x: len(adj[x])):
        if a in used:
            continue
        free = [b for b in adj[a] if b not in used]
        if free:
            b = min(free, key=lambda x: len(adj[x]))
            used |= {a, b}
            n += 1
    return n


def pairs(pool, sweep, el, index, names):
    jobs = []
    for a in names:
        sols = [(s['depart'], s['w']) for s in sweep[a]['c3_10'] if s['dv'] <= SCOUT_LIMIT and s['w']]
        for b in names:
            if b != a and sols:
                jobs.append((a, b, sols, {k: v[index[b]] for k, v in el.items()}))
    dv = {}
    for a, b, best in pool.imap_unordered(pair_job, jobs, chunksize=4):
        dv[(a, b)] = best
    return dv


# ----------------------------------------------------------------------------- main

def main():
    sw = json.load(open(SWEEP))
    sweep, opts = sw['targets'], sw['options']
    names = sorted(sweep)
    tgt = {r['pdes']: r for r in csv.DictReader(open(os.path.join(OUT, 'targets-flyby-model.csv')))}
    best = {n: {o: (sweep[n][o][0]['dv'] if sweep[n][o] else np.inf) for o in opts} for n in names}
    tof = {n: {o: (sweep[n][o][0]['tof'] if sweep[n][o] else np.nan) for o in opts} for n in names}
    for n in names:  # a swingby departure may also be flown without using the swingby
        for o in ('moon_low', 'moon'):
            if best[n]['c3_0'] < best[n][o]:
                best[n][o], tof[n][o] = best[n]['c3_0'], tof[n]['c3_0']
        if best[n]['moon_low'] < best[n]['moon']:
            best[n]['moon'], tof[n]['moon'] = best[n]['moon_low'], tof[n]['moon_low']

    with open(os.path.join(OUT, 'scout-launch-sweep.csv'), 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['pdes', 'name', 'H', 'taxonomy'] + [f'scout_dv_{o}' for o in opts] + [f'tof_days_{o}' for o in opts])
        for n in names:
            w.writerow([n, tgt[n]['name'], tgt[n]['H'], tgt[n]['taxonomy']]
                       + [round(best[n][o], 3) if np.isfinite(best[n][o]) else '' for o in opts]
                       + [int(tof[n][o]) if np.isfinite(tof[n][o]) else '' for o in opts])

    tug = {f'leg<={cap} cycle<={Y}': [n for n in names if num(tgt[n][f'tug_cycle_leg{cap}']) <= Y] for cap, Y in TUG_SETS}
    out = {'scout_limit_kms': SCOUT_LIMIT, 'options': opts, 'budgets_kms': list(BUDGETS)}
    out['scouts_within_budget'] = {o: {str(b): sum(best[n][o] <= b for n in names) for b in BUDGETS} for o in opts}
    out['joint_with_tug'] = {k: {o: {str(b): sum(best[n][o] <= b for n in s) for b in BUDGETS} for o in opts} for k, s in tug.items()}
    out['median_flight_days_of_least_dv_transfer'] = {
        o: float(np.nanmedian([tof[n][o] for n in names if best[n][o] <= 7.0] or [np.nan])) for o in opts}
    need = {}
    for k, s in tug.items():
        need[k] = {'targets': len(s)}
        for o in opts:
            d = np.sort([best[n][o] for n in s])
            need[k][o] = {'median': round(float(np.median(d)), 2) if np.isfinite(np.median(d)) else None,
                          'for_20_targets': round(float(d[19]), 2) if len(d) >= 20 and np.isfinite(d[19]) else None,
                          'for_all': round(float(d[-1]), 2) if np.isfinite(d[-1]) else None}
    out['scout_dv_needed_kms'] = need

    cand = prefilter(load_catalogue(catalogue_path()), h_max=23.0)
    el = elements(cand)
    index = {r['pdes']: k for k, r in enumerate(cand)}
    cache_path = os.path.join(OUT, 'scout-launch-trade-cache.json')  # not committed
    cache = json.load(open(cache_path)) if os.path.exists(cache_path) else {}
    with Pool(min(7, os.cpu_count() or 2)) as pool:
        if 'loops' not in cache:
            cache['loops'] = [[v, c3, *map(float, val)] for (v, c3), val in loops(pool).items()]
            json.dump(cache, open(cache_path, 'w'))
        lp = {(v, c3): (dv, d, a) for v, c3, dv, d, a in cache['loops']}
        pair_sets = {}
        for key in ('leg<=5.0 cycle<=4.0', 'leg<=5.0 cycle<=5.0'):
            s = [n for n in tug[key] if best[n]['c3_10'] <= SCOUT_LIMIT]
            if key not in cache:
                cache[key] = [[a, b, float(v)] for (a, b), v in pairs(pool, sweep, el, index, s).items()]
                json.dump(cache, open(cache_path, 'w'))
            dv = {(a, b): v for a, b, v in cache[key]}
            edges = {tuple(sorted(p)) for p, v in dv.items() if v <= SCOUT_LIMIT}
            loose = {tuple(sorted(p)) for p, v in dv.items() if v <= 4.5}
            with_partner = {n for e in edges for n in e}
            pair_sets[key] = {'targets': len(s), 'pairs_tried': len(s) * (len(s) - 1) // 2,
                              'pairs_within_3.5': len(edges), 'targets_with_a_partner': len(with_partner),
                              'launches_for_all_targets': len(s) - matching(s, edges),
                              'pairs_within_4.5': len(loose),
                              'launches_for_all_targets_at_4.5': len(s) - matching(s, loose),
                              'second_scout_dv_percentiles': {str(p): round(float(np.percentile([v for v in dv.values() if np.isfinite(v)] or [np.nan], p)), 2)
                                                              for p in (10, 50, 90)},
                              'pairs_solved': int(sum(np.isfinite(v) for v in dv.values()))}
    out['shared_launch_to_c3_10'] = pair_sets

    out['earth_loop'] = {}
    for label, v in MOON_REACH.items():
        rows = {}
        for c3 in LOOP_C3:
            dv, days, ang = lp.get((v, c3), (np.inf, np.nan, np.nan))
            rows[str(c3)] = {'loop_dv_kms': round(dv, 2) if np.isfinite(dv) else None, 'loop_days': days,
                             'return_vinf_kms': round(float(np.sqrt(c3)), 2)}
        tot = {}
        for n in names:  # loop, then on to the asteroid with the flyby turning the excess velocity freely
            cands = [lp[(v, c3)][0] + best[n][f'c3_{c3}'] for c3 in LOOP_C3 if (v, c3) in lp]
            tot[n] = min(cands + [best[n][label]])
        out['earth_loop'][label] = {
            'departure_vinf_kms': v, 'loops': rows,
            'scouts_within_budget': {str(b): sum(tot[n] <= b for n in names) for b in BUDGETS},
            'joint_with_tug': {k: {str(b): sum(tot[n] <= b for n in s) for b in BUDGETS} for k, s in tug.items()}}

    mass = {}
    for s in m.SCOUTS:
        mass[s.name] = {'fixed_kg': round(s.fixed_kg), 'planned_thruster_life_h': s.life_hours,
                        'by_dv': {str(b): {'wet_kg': round(float(s.wet_for(b))), 'propellant_kg': round(float(s.propellant_for(b))),
                                           'thrust_hours': round(float(s.thrust_hours(b)), -1),
                                           'accel_mm_s2': round(s.accel(b) * 1e3, 3)} for b in BUDGETS}}
    out['scout_mass'] = mass
    kick = {}
    for c3_from in (-1.8, -0.2):
        dv = float(m.kick_dv(c3_from, 10.0))
        kick[f'from C3={c3_from}'] = {'dv_kms': round(dv, 3)}
        for s in m.SCOUTS:
            wet = float(s.wet_for(SCOUT_LIMIT))
            p, d = m.kick_mass(wet, dv)
            kick[f'from C3={c3_from}'][s.name] = {'scout_kg': round(wet), 'kick_propellant_kg': round(float(p)),
                                                   'kick_dry_kg': round(float(d)), 'total_kg': round(wet + float(p) + float(d))}
    out['perigee_kick_to_c3_10'] = kick
    out['launcher_payload_kg'] = {L.name: {str(c3): {'first stage recovered': round(float(L.payload(c3, True)), -1),
                                                     'expended': round(float(L.payload(c3, False)), -1)} for c3 in (-2, 0, 5, 10, 15, 20)}
                                  for L in (m.FALCON9_LOW, m.FALCON9_HIGH)}
    json.dump(out, open(os.path.join(OUT, 'scout-launch-trade.json'), 'w'), indent=1, default=float)
    print(json.dumps(out, indent=1, default=float))


if __name__ == '__main__':
    main()
