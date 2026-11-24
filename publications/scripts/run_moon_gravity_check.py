"""
rq-0-52: do the one-station cycles survive the Moon's gravity?

    python run_moon_gravity_check.py [--orbit=halo-120] [--place=0] [--cap=5.0] [--cycle=5.0] [--pairs=3] [--maxiter=300] [--workers=9]

Takes the targets whose node-to-node cycle closes from one station place
(run_node_stations_direct.py, the same caps), and for each the `pairs` shortest cycles
(out leg + in leg). Every leg they use is solved again by node_leg_direct.reachable (its
settings are not stored), then flown with the Moon's gravity throughout (moon_gravity.FullLeg,
correction burns allowed every 10 days). The extra Δv over the patched swingby is charged
to the leg's dv_eff, and the targets are counted again.

A leg whose full-model path does not join (or passes too low) has no full-model cost. The
count is given both ways: such legs kept at their patched cost (`targets_if_unsolved_kept`)
and dropped (`targets_if_unsolved_dropped`). Neither is preferred.

Per-leg results are cached in node-moon-gravity-<orbit>-p<place>-c<cap>-y<cycle>-legs.csv,
so a stopped run resumes; the summary goes to the matching .json.
"""

from __future__ import annotations

import csv
import json
import os
import sys
import time
from multiprocessing import Pool

import numpy as np


def arg(name, default):
    for a in sys.argv[1:]:
        if a.startswith(f'--{name}='):
            return a.split('=', 1)[1]
    return default


ORBIT = arg('orbit', 'halo-120')
PLACE = int(arg('place', '0'))
CAP = float(arg('cap', '5.0'))
CYCLE = float(arg('cycle', '5.0'))
PAIRS = int(arg('pairs', '3'))
MAXITER = int(arg('maxiter', '300'))
WORKERS = int(arg('workers', '9'))
WINDOW, SEEDS, SECONDS, MIN_STAY = 10.0, 3, 900.0, 60.0
TAG = f'-c{CAP:g}-y{CYCLE:g}'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'nea-trajectories')
LEGS_IN = os.path.join(OUT, f'node-legs-direct-{ORBIT}-p{PLACE}{TAG}-legs.csv')
CACHE = os.path.join(OUT, f'node-moon-gravity-{ORBIT}-p{PLACE}{TAG}-legs.csv')
SUMMARY = os.path.join(OUT, f'node-moon-gravity-{ORBIT}-p{PLACE}{TAG}.json')
COLUMNS = ('target', 'leg', 'burn_ms', 'budget', 'depart', 'tof', 'dv_eff', 'resolved_delivered', 'ok', 'join_km', 'join_ms', 'burn_ms_full',
           'corrections_ms', 'corrections', 'extra_ms', 'lowest_km', 'escape_shift_days', 'flight_days', 'iterations', 'seconds')


def key(r):
    return (r['target'], r['leg'], int(r['burn_ms']), round(float(r['budget']), 3), round(float(r['depart']), 3), round(float(r['tof']), 3))


def load():
    rows = []
    for r in csv.DictReader(open(LEGS_IN)):
        node_T = float(r['node_T']) if r['node_T'] not in ('', 'nan') else np.nan
        rows.append(dict(r, dv_eff=float(r['dv_eff']), node_T=node_T, depart=float(r['depart']), tof=float(r['tof'])))
    return rows


def pairs(rows, extra=None):
    """Cycles of one target within the caps, shortest first, as (years, out row, in row).
    `extra` maps a leg key to its added Δv (km/s), or to None for a leg to leave out."""
    def cost(r):
        if extra is None:
            return r['dv_eff']
        e = extra.get(key(r), 0.0)
        return np.inf if e is None else r['dv_eff'] + e
    outs = [r for r in rows if r['leg'] == 'out' and cost(r) <= CAP]
    ins = [r for r in rows if r['leg'] == 'in' and cost(r) <= CAP]
    found = []
    for o in outs:
        for i in ins:
            if i['depart'] < o['depart'] + o['tof'] + MIN_STAY:
                continue
            cyc = (i['node_T'] - o['node_T']) / 365.25
            if cyc <= CYCLE:
                found.append((cyc, o, i))
    return sorted(found, key=lambda t: t[0])


_ctx = {}


def _init():
    sys.argv = [sys.argv[0], f'--orbit={ORBIT}']
    import run_node_legs_direct as R
    _ctx['R'] = R
    _ctx.update(R.setup())


def check(r):
    import node_leg_direct as d
    import moon_gravity as mg
    t0 = time.time()
    out = r['leg'] == 'out'
    T_earth = (r['depart'] if out else r['depart'] + r['tof']) - d.J2000
    clocks = d.Clocks(PLACE / 8, _ctx['orbit'].period_days)
    clocks = clocks if out else clocks.mirrored()
    lon, lat, burn, budget = float(r['lon']), float(r['lat']), float(r['burn_ms']), float(r['budget'])
    esc = T_earth if out else -T_earth
    v, sol, _, _ = d.reachable(_ctx['orbit'], _ctx['clouds'][int(burn)], clocks, lon, lat, float(r['vinf']), burn, esc, WINDOW, budget, n_seeds=SEEDS, seconds=SECONDS)
    res = {k: r[k] for k in ('target', 'leg', 'burn_ms', 'budget', 'depart', 'tof', 'dv_eff')}
    res['resolved_delivered'] = round(float(v), 4)
    if sol is None:
        return dict(res, ok=False, seconds=round(time.time() - t0, 1))
    leg = mg.FullLeg(_ctx['orbit'], clocks, sol.x, sol.flown.encounter_days, burn, v * d.direction(lon, lat), esc, WINDOW, budget)
    _, ch, _ = leg.solve(maxiter=MAXITER)
    return dict(res, ok=ch.ok, join_km=round(ch.join_km, 3), join_ms=round(ch.join_ms, 4), burn_ms_full=round(ch.burn_ms, 1), corrections_ms=round(ch.tcm_ms, 1),
                corrections=ch.corrections, extra_ms=round(ch.extra_ms, 1), lowest_km=round(ch.lowest_km), escape_shift_days=round(float(ch.escape_shift_days), 2),
                flight_days=round(float(ch.flight_days), 1), iterations=ch.iterations, seconds=round(time.time() - t0, 1))


def main():
    rows = load()
    by = {}
    for r in rows:
        by.setdefault(r['target'], []).append(r)
    closing = sorted(n for n in by if pairs(by[n]))
    todo = {}
    for n in closing:
        for _, o, i in pairs(by[n])[:PAIRS]:
            todo[key(o)], todo[key(i)] = o, i
    done = {}
    if os.path.exists(CACHE):
        for r in csv.DictReader(open(CACHE)):
            done[key(r)] = r
    jobs = [r for k, r in todo.items() if k not in done]
    print(f'{len(closing)} targets close; {len(todo)} legs in their {PAIRS} shortest cycles, {len(jobs)} to fly', flush=True)
    new = not os.path.exists(CACHE)
    with open(CACHE, 'a', newline='') as f:
        w = csv.DictWriter(f, COLUMNS)
        if new:
            w.writeheader()
        with Pool(WORKERS, initializer=_init) as pool:
            for res in pool.imap_unordered(check, jobs):
                w.writerow({c: res.get(c, '') for c in COLUMNS})
                f.flush()
                done[key(res)] = {c: str(res.get(c, '')) for c in COLUMNS}
                print(res['target'], res['leg'], 'ok', res['ok'], 'extra', res.get('extra_ms'), 'corr', res.get('corrections'), 'low', res.get('lowest_km'),
                      'join', res.get('join_km'), f"{res['seconds']}s", flush=True)

    legs = [done[k] for k in todo]
    ok = [r for r in legs if r['ok'] == 'True']
    extra_ok = {key(r): max(float(r['extra_ms']), 0.0) / 1e3 for r in ok}
    kept = dict(extra_ok)
    dropped = {**extra_ok, **{key(r): None for r in legs if r['ok'] != 'True'}}
    # a leg outside the checked cycles is left out of the recount (its full-model cost is unknown)
    unchecked = {key(r): None for n in closing for r in by[n] if key(r) not in todo}
    kept.update(unchecked)
    dropped.update(unchecked)
    count = lambda ex: sorted(n for n in closing if pairs(by[n], ex))
    still_kept, still_dropped = count(kept), count(dropped)
    ex = np.array([float(r['extra_ms']) for r in ok]) if ok else np.array([np.nan])
    summary = {
        'orbit': ORBIT, 'place': PLACE, 'leg_cap_kms': CAP, 'cycle_cap_yr': CYCLE, 'pairs_per_target': PAIRS, 'maxiter': MAXITER,
        'model': 'Sun-Earth CR3BP with the Earth and the Moon about the barycentre; correction burns allowed every 10 days',
        'targets_closing_patched': len(closing),
        'legs_checked': len(legs), 'legs_solved': len(ok),
        'extra_ms': {'median': round(float(np.median(ex)), 1), 'p90': round(float(np.percentile(ex, 90)), 1), 'max': round(float(np.max(ex)), 1),
                     'share_over_100': round(float(np.mean(ex > 100)), 3)},
        'corrections_median': float(np.median([int(r['corrections']) for r in ok])) if ok else None,
        'lowest_km_min': min((float(r['lowest_km']) for r in ok), default=None),
        'targets_if_unsolved_kept': len(still_kept), 'targets_if_unsolved_dropped': len(still_dropped),
        'lost_if_unsolved_kept': sorted(set(closing) - set(still_kept)), 'lost_if_unsolved_dropped': sorted(set(closing) - set(still_dropped)),
        'note': 'extra_ms is an upper bound (SLSQP stopped at its iteration cap). Legs outside each target\'s checked cycles are not counted in the recount.',
    }
    json.dump(summary, open(SUMMARY, 'w'), indent=1)
    print(json.dumps(summary, indent=1))


if __name__ == '__main__':
    main()
