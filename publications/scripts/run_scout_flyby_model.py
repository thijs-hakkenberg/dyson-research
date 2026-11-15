"""
rq-0-52, third pass: the scout constraint on the targets of run_trajectory_flyby_model.py.

    python run_scout_flyby_model.py

A scout must reach its asteroid within 3.5 km/s of its own propulsion (bom-0-1). Two ways
of starting are compared:

  launch to C3 = 10 km²/s²  – 3.16 km/s of excess speed in any direction, from the launcher
                              (already solved in the second pass: targets.csv);
  launch to C3 ≈ 0 + Moon   – a launch that just reaches the Moon, one swingby, escape. The
                              reachable excess speed by direction is computed here in the
                              three-body model, then used as the limit in the leg optimiser.

Writes publications/data/cislunar-flyby/reach-launch.json and
publications/data/nea-trajectories/{targets-flyby-model.csv, scout-flyby-model.json}.
"""

from __future__ import annotations

import csv
import json
import os
from multiprocessing import Pool

import numpy as np

import cislunar_flyby as c
from nea_accessibility import SCOUT, elements, load_catalogue, prefilter
from run_cislunar_flyby import LAT_EDGES, LON_EDGES, reach_table
from run_cislunar_flyby import OUT as CIS
from run_nea_accessibility import catalogue_path
from run_trajectory_flyby_model import LEG_CAPS, MODES, best_cycle
from run_trajectory_study import DUTY, OUT, TOFS, grids, pick_seeds
from trajectory_opt import FlybyReach, impulsive_tables, low_thrust_leg, seed_velocities

LAUNCH_C3 = (-1.8, -1.4, -1.0, -0.6, -0.2)  # km²/s²; all reach the Moon's distance, none escapes unaided
PERIGEE_KM = 6578.0
SCOUT_LIMIT = 3.5
BUDGET = 45
REACH_LAUNCH = os.path.join(CIS, 'reach-launch.json')


def launch_reach():
    """Reach table for launch → Moon → one swingby → escape. The Moon may be anywhere on its
    orbit (the launch day is free), so every place on it is tried."""
    states, t0 = [], []
    mu = c.MU_EARTH
    for c3 in LAUNCH_C3:
        a = -mu / c3
        vp = np.sqrt(c3 + 2 * mu / PERIGEE_KM)
        h = PERIGEE_KM * vp
        r = c.A_MOON * c.AU_KM
        v = np.sqrt(c3 + 2 * mu / r)
        vt = h / r
        vr = np.sqrt(max(v * v - vt * vt, 0.0))
        e = 1 - PERIGEE_KM / a
        E = np.arccos((1 - r / a) / e)
        days = np.sqrt(a**3 / mu) * (E - e * np.sin(E)) / 86400.0  # perigee to the Moon's distance
        for th in np.radians(np.arange(0, 360, 5)):
            rh = np.array([np.cos(th), np.sin(th), 0.0])
            thh = np.array([-np.sin(th), np.cos(th), 0.0])
            rho = c.A_MOON * rh
            vi = (vr * rh + vt * thh) / c.VU_KMS  # Earth-relative, non-rotating axes
            states.append(np.concatenate([c.EARTH + rho, vi - np.array([-rho[1], rho[0], 0.0])]))
            t0.append(days * c.DAY)
    yc, tc = np.array(states), np.array(t0)
    _, _, th1 = c.encounter_vinf(yc)
    fan, idx = c.swingby_fan(yc, 16, 25)
    f = c.integrate(fan, tc[idx], 60 * c.DAY)
    ok = f.status == 1
    v, lon, lat, c3 = c.escape_state(f.y[ok])
    k = c3 > 0
    e = {'vinf': v[k], 'lon': lon[k], 'lat': np.abs(lat[k]), 'days': f.t[ok][k] * c.TU_DAYS,
         'moon': th1[idx[ok][k]] + (c.N_MOON - 1.0) * (f.t[ok][k] - tc[idx[ok][k]])}
    tab = np.round(reach_table(e, BUDGET), 3)
    json.dump({'lon_edges': LON_EDGES.tolist(), 'lat_edges': LAT_EDGES.tolist(), 'budgets_days': [BUDGET],
               'vinf_kms': {'launch': {str(BUDGET): tab.tolist()}}}, open(REACH_LAUNCH, 'w'))
    return tab, e


def scout_target(args):
    el1, name = args
    rc = FlybyReach(REACH_LAUNCH, 'launch', BUDGET)
    t_dep, _ = grids(20.0)
    one = {k: np.asarray([v]) for k, v in el1.items()}
    out = impulsive_tables(one, t_dep, TOFS, True, credits=(1.0, 1.5))
    seeds = {}
    for g in (1.0, 1.5):
        for d, t, imp, rev in pick_seeds(out[g][0][0], out[g][1][0], t_dep, 5.5, per_bin=1, limit=16):
            seeds.setdefault((d, t, rev), imp)
    best = (np.inf, 0.0, 0.0)
    for (d, t, rev) in seeds:
        r1, vs1, r2, vs2, v1, v2 = seed_velocities(el1, t_dep[d], TOFS[t], True, True, rev)
        if not np.all(np.isfinite(v1)):
            continue
        res = low_thrust_leg(r1, vs1, r2, vs2, TOFS[t], SCOUT.accel, DUTY, seed=(v1, v2), free_end='start', reach=rc)
        if res.ok and res.dv_kms < best[0]:
            best = (res.dv_kms, res.vinf_kms, rc.angles(np.asarray(res.vinf_vec), r1, False)[1])
    return name, best


def main():
    tab, e = launch_reach()
    old = {r['pdes']: r for r in csv.DictReader(open(os.path.join(OUT, 'targets.csv')))}
    legs = {}
    for r in csv.DictReader(open(os.path.join(OUT, 'legs-flyby-model.csv'))):
        legs.setdefault(r['target'], []).append({'leg': r['leg'], 'burn_ms': int(r['burn_ms']), 'budget_days': int(r['budget_days']),
                                                 'depart': 2451545.0 + (float(r['depart_year']) - 2000) * 365.25, 'tof': float(r['tof_days']),
                                                 'dv': float(r['low_thrust_kms']), 'allowance': float(r['allowance_days'])})
    names = sorted(legs)
    cand = prefilter(load_catalogue(catalogue_path()), h_max=23.0)
    el = elements(cand)
    index = {r['pdes']: k for k, r in enumerate(cand)}
    with Pool(min(7, os.cpu_count() or 2)) as pool:
        scout = dict(pool.imap_unordered(scout_target, [({k: v[index[n]] for k, v in el.items()}, n) for n in names], chunksize=2))
    rows = []
    for n in names:
        o = old[n]
        row = {'pdes': n, 'name': o['name'], 'H': o['H'], 'taxonomy': o['taxonomy'], 'metal_plausible': o['metal_plausible'],
               'scout_dv_launch_c3_10': o['scout_dv_vinf3.16'], 'scout_dv_moon_flat_1.5': o['scout_dv_vinf1.5'],
               'scout_dv_moon_modelled': round(scout[n][0], 3) if np.isfinite(scout[n][0]) else '',
               'scout_vinf_used': round(scout[n][1], 2), 'scout_vinf_lat_deg': round(scout[n][2], 1)}
        for cap in LEG_CAPS:
            b = best_cycle(legs[n], cap)
            row[f'tug_cycle_leg{cap}'] = round(b[0], 3) if b else ''
            b150 = best_cycle(legs[n], cap, {m for m in MODES if m[0] == 150})
            row[f'tug_cycle_leg{cap}_burn150'] = round(b150[0], 3) if b150 else ''
        rows.append(row)
    with open(os.path.join(OUT, 'targets-flyby-model.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    num = lambda r, k: float(r[k]) if r[k] not in ('', None) else np.inf
    summary = {'scout_limit_kms': SCOUT_LIMIT,
               'launch_moon_reach_kms': {'in_plane_min_median_max': [float(tab[:, 0].min()), float(np.median(tab[:, 0])), float(tab[:, 0].max())],
                                         'median_by_latitude': {f'{int(LAT_EDGES[k])}-{int(LAT_EDGES[k + 1])}': float(np.median(tab[:, k])) for k in range(tab.shape[1])},
                                         'max_found': round(float(e['vinf'].max()), 3), 'days_from_launch_median': round(float(np.median(e['days'])), 1)},
               'scouts_within_limit': {'launch C3=10': sum(num(r, 'scout_dv_launch_c3_10') <= SCOUT_LIMIT for r in rows),
                                       'C3~0 + Moon, flat 1.5 km/s (second pass)': sum(num(r, 'scout_dv_moon_flat_1.5') <= SCOUT_LIMIT for r in rows),
                                       'C3~0 + Moon, modelled': sum(num(r, 'scout_dv_moon_modelled') <= SCOUT_LIMIT for r in rows)},
               'joint': {}}
    for cap in LEG_CAPS:
        for Y in (4.0, 5.0):
            tug = [r for r in rows if num(r, f'tug_cycle_leg{cap}') <= Y]
            both = [r for r in tug if num(r, 'scout_dv_launch_c3_10') <= SCOUT_LIMIT]
            summary['joint'][f'leg<={cap} cycle<={Y}'] = {
                'tug only': len(tug),
                'and scout from C3=10': len(both),
                'and scout from C3~0 + Moon': sum(num(r, 'scout_dv_moon_modelled') <= SCOUT_LIMIT for r in tug),
                'and scout by either': sum(min(num(r, 'scout_dv_launch_c3_10'), num(r, 'scout_dv_moon_modelled')) <= SCOUT_LIMIT for r in tug),
                'tug with 150 m/s burns only, scout from C3=10': sum(num(r, f'tug_cycle_leg{cap}_burn150') <= Y and num(r, 'scout_dv_launch_c3_10') <= SCOUT_LIMIT for r in rows),
                'of the C3=10 set: unclassified / metal-plausible': [sum(1 for r in both if not r['taxonomy']), sum(1 for r in both if r['metal_plausible'] in ('True', '1', 'yes'))],
            }
    json.dump(summary, open(os.path.join(OUT, 'scout-flyby-model.json'), 'w'), indent=1)
    print(json.dumps(summary, indent=1))


if __name__ == '__main__':
    main()
