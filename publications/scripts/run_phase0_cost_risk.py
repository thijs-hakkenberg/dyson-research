"""
Run the rq-0-84 cost-confidence cases and write publications/data/phase0-cost-risk/results.json.

    python run_phase0_cost_risk.py
"""

import json
import os

from phase0_cost_risk import ROOT, Settings, load_bom, simulate

OUT = os.path.join(ROOT, 'publications', 'data', 'phase0-cost-risk')

CASES = {
    'envelopes only, rho 0.3': Settings(rho=0.3),
    'envelopes only, rho 0.5': Settings(rho=0.5),
    'envelopes only, rho 0.3, P5/P95': Settings(rho=0.3, tail='P5/P95'),
    'growth 1.3/2.0, rho 0.3': Settings(rho=0.3, growth=(1.3, 2.0)),
    'growth 1.3/2.0, rho 0.5': Settings(rho=0.5, growth=(1.3, 2.0)),
    'growth 1.5/2.5, rho 0.3': Settings(rho=0.3, growth=(1.5, 2.5)),
    '0A 6-15 yr, NRE 30% level-of-effort, rho 0.3': Settings(rho=0.3, duration_years=(6, 15), nre_level_of_effort=0.3),
    'growth 1.3/2.0 + 0A 6-15 yr + NRE 30% LOE, rho 0.3': Settings(rho=0.3, growth=(1.3, 2.0), duration_years=(6, 15), nre_level_of_effort=0.3),
}


def main():
    bom = load_bom()
    res = {
        'source': 'src/lib/data/phase-0-bom.json (consensus 2026-10-20)',
        'method': 'publications/scripts/phase0_cost_risk.py',
        'cases': {name: {'settings': {k: v for k, v in s.__dict__.items() if k not in ('n', 'seed')}, **simulate(bom, s)} for name, s in CASES.items()},
    }
    os.makedirs(OUT, exist_ok=True)
    json.dump(res, open(os.path.join(OUT, 'results.json'), 'w'), indent=2)
    B = lambda x: f'${x / 1e9:.1f}B'
    for name, r in res['cases'].items():
        a, b = r['0A'], r['0B']
        print(f"{name:52s} 0A P50 {B(a['P50'])} P80 {B(a['P80'])} conf(45%) {a['confidence_of_funded']:.2f} P(<=16B) {a['P(<=16B)']:.2f}"
              f" | 0B P50 {B(b['P50'])} P80 {B(b['P80'])} conf(65%) {b['confidence_of_funded']:.2f}")


if __name__ == '__main__':
    main()
