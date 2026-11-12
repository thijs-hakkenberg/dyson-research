"""
Run the rq-0-61 chain-closure cases and write publications/data/phase0-chain/results.json.

    python run_phase0_chain.py

Needs publications/data/nea-catalogue/candidates.csv (run_nea_accessibility.py).
"""

import json
import os

from phase0_chain_model import ASSUMPTIONS, ChainSettings, simulate
from phase0_cost_risk import ROOT, Settings, load_bom

OUT = os.path.join(ROOT, 'publications', 'data', 'phase0-chain')

CASES = {
    'reference: catalogue legs <=6.5 km/s, cycle <=4 yr, 1.0-1.3 kt/yr, 6-6.5 yr run': ChainSettings(),
    'consensus as written: 5 km/s legs, 3-yr cycle': ChainSettings(trajectory='consensus'),
    'catalogue legs <=7.5 km/s, cycle <=5 yr': ChainSettings(leg_cap=7.5, max_cycle_years=5.0),
    'Isp 3,000-3,500 s (bom-0-16 trade)': ChainSettings(isp_s=(3000, 3500)),
    '2.3-2.7 kt/yr (upper demand)': ChainSettings(product_t_per_yr=(2300, 2700)),
    'run 10 yr': ChainSettings(ops_years=(10, 10)),
    'run 15 yr': ChainSettings(ops_years=(15, 15)),
    'run 20 yr, Isp 3,000-3,500 s, 2.3-2.7 kt/yr': ChainSettings(ops_years=(20, 20), isp_s=(3000, 3500), product_t_per_yr=(2300, 2700)),
    'reference with cost growth 1.3/2.0': ChainSettings(cost=Settings(rho=0.3, growth=(1.3, 2.0))),
}


def main():
    bom = load_bom()
    res = {'assumptions_not_in_consensus': ASSUMPTIONS, 'cases': {}}
    for name, cs in CASES.items():
        r = simulate(bom, cs)
        res['cases'][name] = r
        k = r['per_kg_0B_with_contingency']
        print(f"{name:78s} fleet {r['fleet']['P50']:.0f} prop {r['propellant_t_per_yr']['P50']:.0f} t/yr PIR {r['import_ratio']['P50']:.2f}"
              f" launch {r['launch_kt']['P50']:.1f} kt delivered {r['delivered_kt']['P50']:.1f} kt  $/kg {k['P50']:,.0f}"
              f" x{r['ratio_0B_to_earth']['P50']:.1f} Earth  P(beat) {r['P(0B beats Earth)']:.2f}  breakeven {r['breakeven_launch_price_per_kg']['P50']}")
    os.makedirs(OUT, exist_ok=True)
    json.dump(res, open(os.path.join(OUT, 'results.json'), 'w'), indent=2)


if __name__ == '__main__':
    main()
