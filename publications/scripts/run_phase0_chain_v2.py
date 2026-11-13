"""
rq-0-61, second pass: chain closure with the optimised trajectories of rq-0-52 and with
replacement hardware on long runs. Writes publications/data/phase0-chain/results-v2.json.

    python run_phase0_chain_v2.py

Needs publications/data/nea-trajectories/legs.csv (run_trajectory_study.py).
"""

import json
import os
from dataclasses import replace

from phase0_chain_model import ASSUMPTIONS, ChainSettings, simulate
from phase0_cost_risk import ROOT, load_bom

OUT = os.path.join(ROOT, 'publications', 'data', 'phase0-chain')
OPT = ChainSettings(trajectory='optimised', replacements=True)

TRAJECTORY = {
    'no flyby, legs <=6.5 km/s': replace(OPT, lga=0.0, leg_cap=6.5),
    'flyby 1.0 km/s, legs <=5.0 km/s': replace(OPT, lga=1.0, leg_cap=5.0),
    'flyby 1.0 km/s, legs <=6.5 km/s': replace(OPT, lga=1.0, leg_cap=6.5),
    'flyby 1.5 km/s, legs <=5.0 km/s': replace(OPT, lga=1.5, leg_cap=5.0),
    'flyby 1.0 km/s, legs <=5.0 km/s, fastest quarter of targets': replace(OPT, lga=1.0, leg_cap=5.0, target_fraction=0.25),
    'flyby 1.0 km/s, legs <=6.5 km/s, fastest quarter of targets': replace(OPT, lga=1.0, leg_cap=6.5, target_fraction=0.25),
}
RUNS = (6.25, 10.0, 15.0, 20.0)
REF = replace(OPT, lga=1.0, leg_cap=6.5, ops_years=(10.0, 10.0))
POWERS = (0.75, 1.0, 1.5, 2.25, 3.0)
PAYLOADS = (100, 150, 200, 250, 300)
ISPS = (2000, 2500, 3250)


def row(r):
    return {
        'targets': r['targets_sampled'], 'cycle_yr': round(r['cycle_years']['P50'], 2), 'fleet': r['fleet']['P50'],
        'propellant_t_per_yr': round(r['propellant_t_per_yr']['P50']), 'import_ratio': round(r['import_ratio']['P50'], 3),
        'import_ratio_with_replacements': round(r['import_ratio_with_replacements']['P50'], 3),
        'P(import_ratio<=0.5)': round(r['import_ratio']['P(<=0.5)'], 2), 'launch_kt': round(r['launch_kt']['P50'], 2),
        'delivered_kt': round(r['delivered_kt']['P50'], 2), 'cost_0B_B': round(r['0B_cost_with_contingency_B']['P50'], 1),
        'replacement_cost_B': round(r['replacement_cost_B']['P50'], 1), 'per_kg': round(r['per_kg_0B_with_contingency']['P50']),
        'ratio_to_earth': {k: round(v, 2) for k, v in r['ratio_0B_to_earth'].items()}, 'P(beats Earth)': round(r['P(0B beats Earth)'], 3),
    }


def run(bom, cs):
    try:
        return row(simulate(bom, cs))
    except ValueError:
        return None  # no target closes for this tug


def main():
    bom = load_bom()
    res = {'assumptions_not_in_consensus': ASSUMPTIONS, 'by_trajectory_and_run': {}, 'replacements_effect': {}, 'tug_trade': [], 'scale': {}}
    for name, cs in TRAJECTORY.items():
        res['by_trajectory_and_run'][name] = {f'{y} yr': run(bom, replace(cs, ops_years=(y, y))) for y in RUNS}
        r = res['by_trajectory_and_run'][name]
        print(name, {k: (v['ratio_to_earth']['P50'], v['import_ratio']) if v else None for k, v in r.items()}, 'targets', r['10.0 yr'] and r['10.0 yr']['targets'])
    for y in RUNS:
        cs = replace(TRAJECTORY['flyby 1.0 km/s, legs <=6.5 km/s'], ops_years=(y, y))
        res['replacements_effect'][f'{y} yr'] = {'with': run(bom, cs), 'without': run(bom, replace(cs, replacements=False))}
    for isp in ISPS:
        for pw in POWERS:
            for pl in PAYLOADS:
                r = run(bom, replace(REF, tug_power_mw=pw, payload_t=(pl, pl), isp_s=(isp, isp)))
                res['tug_trade'].append({'isp_s': isp, 'power_mw': pw, 'payload_t': pl, **(r or {'targets': 0})})
    for label, cs in {
        '1.0-1.3 kt/yr, 10 yr': REF,
        '2.3-2.7 kt/yr, 10 yr': replace(REF, product_t_per_yr=(2300, 2700)),
        '2.3-2.7 kt/yr, 20 yr': replace(REF, product_t_per_yr=(2300, 2700), ops_years=(20.0, 20.0)),
        '5 kt/yr, 20 yr': replace(REF, product_t_per_yr=(5000, 5000), ops_years=(20.0, 20.0)),
    }.items():
        res['scale'][label] = run(bom, cs)
    os.makedirs(OUT, exist_ok=True)
    json.dump(res, open(os.path.join(OUT, 'results-v2.json'), 'w'), indent=2)
    for isp in ISPS:
        print(f'Isp {isp}: rows = power MW, columns = payload t {PAYLOADS}; cells = targets / cycle yr / x Earth / import ratio')
        for pw in POWERS:
            cells = [next(t for t in res['tug_trade'] if t['isp_s'] == isp and t['power_mw'] == pw and t['payload_t'] == pl) for pl in PAYLOADS]
            print(f'  {pw:4.2f}', '  '.join(f"{c['targets']:3d}/{c['cycle_yr']:.1f}/{c['ratio_to_earth']['P50']:.1f}/{c['import_ratio']:.2f}" if c['targets'] else '  0/ - / - / -  ' for c in cells))
    print(json.dumps(res['replacements_effect'], indent=None)[:0])
    for k, v in res['replacements_effect'].items():
        print(k, 'with', v['with']['ratio_to_earth']['P50'], v['with']['replacement_cost_B'], 'without', v['without']['ratio_to_earth']['P50'])
    for k, v in res['scale'].items():
        print(k, v and (v['fleet'], v['per_kg'], v['ratio_to_earth'], v['import_ratio'], v['P(beats Earth)']))


if __name__ == '__main__':
    main()
