"""
rq-0-61 on the tug legs of the three-body flyby studies (rq-0-52).

    python run_phase0_chain_flyby.py [--model=planar|planar-orbits|halo]
    python run_phase0_chain_flyby.py --model=station-<orbit> --phase0=<k>   # station at one place on one orbit

planar is the first three-body model (planar node orbits, Moon in the ecliptic);
planar-orbits and halo are the legs solved against the inclined-Moon reach tables.
Writes publications/data/phase0-chain/flyby-model.json or flyby-3d-<model>.json.
"""

import json
import os
import sys
from dataclasses import replace

from phase0_chain_model import ChainSettings
from phase0_cost_risk import ROOT, load_bom
from run_phase0_chain_v2 import run

MODEL = next((a.split('=')[1] for a in sys.argv if a.startswith('--model=')), 'planar')
PHASE0 = next((a.split('=')[1] for a in sys.argv if a.startswith('--phase0=')), '0')
NAME = 'flyby-model' if MODEL == 'planar' else f'flyby-{MODEL}-p{PHASE0}' if MODEL.startswith('station-') else f'flyby-3d-{MODEL}'
LEGS = os.path.join(ROOT, 'publications', 'data', 'nea-trajectories', f'legs-{NAME}.csv')
OUT = os.path.join(ROOT, 'publications', 'data', 'phase0-chain', f'{NAME}.json')
RUNS = (6.25, 10.0, 20.0)


def main():
    bom = load_bom()
    base = ChainSettings(trajectory='optimised', replacements=True, flyby_legs=LEGS)
    res = {}
    for burns, label in (((150,), '150'), ((150, 300), '150/300')):
        for cap in (5.0, 5.75, 6.5):
            for cyc in (4.0, 5.0):
                cs = replace(base, flyby_burns_ms=burns, leg_cap=cap, max_cycle_years=cyc)
                key = f'node burn {label} m/s, legs <={cap} km/s, cycle <={cyc} yr'
                res[key] = {f'{y} yr': run(bom, replace(cs, ops_years=(y, y))) for y in RUNS}
                r = res[key]['10.0 yr']
                print(key, r and (r['targets'], r['cycle_yr'], r['import_ratio'], {k: v['ratio_to_earth']['P50'] for k, v in res[key].items() if v}))
    json.dump(res, open(OUT, 'w'), indent=1)


if __name__ == '__main__':
    main()
