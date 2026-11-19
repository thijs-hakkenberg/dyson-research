"""
rq-0-61 on the tug legs rq-0-52 solved directly, with one station at one place on the node orbit.

    python run_node_legs_direct.py --orbit=halo-120 --phase0=0,...,7 --cap=5.0 --cycle=5.0
    python run_phase0_chain_direct.py [--orbit=halo-120] [--cap=5.0] [--cycle=5.0]

For each of the eight station places, the legs solved directly (node-legs-direct-<orbit>-p<k>
[-c<cap>-y<cycle>]-legs.csv) are written in the layout of the flyby leg files the chain model
reads (phase0_chain_model.load_model_legs). The changes from the table legs:

  Δv          the leg's Δv plus the excess speed the node leg could not deliver (dv_eff);
  node date   the date found by the direct solve, as the allowance between node and leg;
  thrust      the leg's thrust fraction scaled by dv_eff / dv (the extra Δv is thrust for
              longer at the same acceleration; above 1 the tug model drops the leg).

Legs with no solution are left out. The chain model is then run at the given caps, and at
four-year cycles for comparison, for runs of 6.25, 10 and 20 years.

Writes publications/data/nea-trajectories/legs-direct-<orbit>-p<k>-c<cap>-y<cycle>.csv and
publications/data/phase0-chain/direct-<orbit>-c<cap>-y<cycle>.json.
"""

from __future__ import annotations

import csv
import json
import os
import sys
from dataclasses import replace

import numpy as np

from phase0_chain_model import ChainSettings
from phase0_cost_risk import ROOT, load_bom
from run_phase0_chain_v2 import run

arg = lambda k, default: next((a.split('=')[1] for a in sys.argv if a.startswith(f'--{k}=')), default)
ORBIT = arg('orbit', 'halo-120')
CAP = float(arg('cap', '5.0'))
CYCLE = float(arg('cycle', '5.0'))
TAG = '' if (CAP, CYCLE) == (5.0, 4.0) else f'-c{CAP:g}-y{CYCLE:g}'
TRAJ = os.path.join(ROOT, 'publications', 'data', 'nea-trajectories')
OUT = os.path.join(ROOT, 'publications', 'data', 'phase0-chain', f'direct-{ORBIT}-c{CAP:g}-y{CYCLE:g}.json')
TABLE_LEGS = os.path.join(TRAJ, 'legs-flyby-3d-halo.csv')
RUNS = (6.25, 10.0, 20.0)
COLUMNS = ('target', 'burn_ms', 'budget_days', 'leg', 'depart_year', 'tof_days', 'revs', 'low_thrust_kms', 'thruster_only_kms', 'thrust_fraction',
           'vinf_kms', 'vinf_lon_deg', 'vinf_lat_deg', 'allowance_days')
J2000 = 2451545.0


def key(target, leg, burn, depart_jd, tof, budget):
    return (target, leg, int(burn), round(depart_jd, 3), round(float(tof), 3), round(float(budget), 1))


def table_rows():
    rows = {}
    for r in csv.DictReader(open(TABLE_LEGS)):
        jd = J2000 + (float(r['depart_year']) - 2000.0) * 365.25
        rows[key(r['target'], r['leg'], r['burn_ms'], jd, r['tof_days'], r['budget_days'])] = r
    return rows


def write_legs(place, table):
    """Leg file for one station place; returns its path and counts."""
    src = os.path.join(TRAJ, f'node-legs-direct-{ORBIT}-p{place}{TAG}-legs.csv')
    dst = os.path.join(TRAJ, f'legs-direct-{ORBIT}-p{place}-c{CAP:g}-y{CYCLE:g}.csv')
    n, kept, missing = 0, 0, 0
    with open(dst, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(COLUMNS)
        for r in csv.DictReader(open(src)):
            n += 1
            dv_eff = float(r['dv_eff'])
            if not np.isfinite(dv_eff) or r['node_T'] in ('', 'nan'):
                continue
            t = table.get(key(r['target'], r['leg'], r['burn_ms'], float(r['depart']), r['tof'], r['budget']))
            if t is None:
                missing += 1
                continue
            depart, tof, node = float(r['depart']), float(r['tof']), J2000 + float(r['node_T'])
            allowance = depart - node if r['leg'] == 'out' else node - (depart + tof)
            tf = float(t['thrust_fraction']) * dv_eff / float(r['dv'])
            w.writerow([t['target'], t['burn_ms'], t['budget_days'], t['leg'], t['depart_year'], t['tof_days'], t['revs'], round(dv_eff, 3),
                        t['thruster_only_kms'], round(tf, 3), t['vinf_kms'], t['vinf_lon_deg'], t['vinf_lat_deg'], round(allowance, 2)])
            kept += 1
    return dst, {'legs': n, 'flown': kept, 'unmatched': missing}


def summary(r):
    if not r:
        return None
    return {'targets': r['targets'], 'cycle_yr': r['cycle_yr'], 'import_ratio': r['import_ratio'], 'ratio_to_earth_P50': r['ratio_to_earth']['P50']}


def main():
    bom = load_bom()
    table = table_rows()
    res = {'orbit': ORBIT, 'leg_cap_kms': CAP, 'cycle_cap_yr': CYCLE, 'node_burns_ms': [150, 300], 'places': {}}
    for place in range(8):
        path, counts = write_legs(place, table)
        base = ChainSettings(trajectory='optimised', replacements=True, flyby_legs=path, flyby_burns_ms=(150, 300), leg_cap=CAP)
        res['places'][place] = {'leg_file': os.path.basename(path), **counts}
        for cyc in sorted({4.0, CYCLE}):
            cs = replace(base, max_cycle_years=cyc)
            full = {f'{y} yr': run(bom, replace(cs, ops_years=(y, y))) for y in RUNS}
            res['places'][place][f'cycle <={cyc:g} yr'] = {'full': full, 'summary': {k: summary(v) for k, v in full.items()}}
            s = res['places'][place][f'cycle <={cyc:g} yr']['summary']
            print(place, cyc, counts, {k: v and (v['targets'], v['cycle_yr'], v['import_ratio'], v['ratio_to_earth_P50']) for k, v in s.items()}, flush=True)
    for cyc in sorted({4.0, CYCLE}):
        rows = [res['places'][p][f'cycle <={cyc:g} yr']['summary'] for p in range(8)]
        agg = {}
        for y in RUNS:
            v = [r[f'{y} yr'] for r in rows if r[f'{y} yr']]
            agg[f'{y} yr'] = {k: [min(x[k] for x in v), float(np.median([x[k] for x in v])), max(x[k] for x in v)] for k in ('targets', 'cycle_yr', 'import_ratio', 'ratio_to_earth_P50')} if v else None
            agg[f'{y} yr'] = agg[f'{y} yr'] and {**agg[f'{y} yr'], 'places_closing': len(v)}
        res[f'over places, cycle <={cyc:g} yr (min, median, max)'] = agg
    json.dump(res, open(OUT, 'w'), indent=1, default=float)
    for k, v in res.items():
        if k.startswith('over places'):
            print(k, json.dumps(v))


if __name__ == '__main__':
    main()
