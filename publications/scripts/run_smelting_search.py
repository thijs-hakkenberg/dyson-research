"""
Search process configurations with the Fe-Ni route simulator (rq-0-56) and write
publications/data/smelting-routes/results.json.

    python run_smelting_search.py [--quick]
"""

import json
import os
import sys

import numpy as np

from smelting_sim import PHYSICS_RANGES, ROUTES, TIERS, Design, draw_physics, evaluate, search, sensitivity, summarise

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'smelting-routes')
TIER = 'envelope (S≤0.10, ≥97)'


def binned(x, ok, edges):
    return [{'from': float(a), 'to': float(b), 'P_pass': float(ok[(x >= a) & (x < b)].mean()) if ((x >= a) & (x < b)).any() else None}
            for a, b in zip(edges[:-1], edges[1:])]


def falsifiers(ph):
    """What each promising route needs from its least certain parameter, and the gravity the melt needs."""
    out = {}
    # H2 desulfurisation: pass rate against the kinetic time constant, for three hold times
    edges = np.array([2, 4, 8, 14, 22, 40])
    out['h2_tau_h_vs_pass'] = {}
    for hours in (24, 48, 96):
        d = Design(finish='melt', h2=True, h2_T=925, h2_hours=hours, grind_um=100, melt_G=20, melt_minutes=10)
        r = evaluate(d, ph)
        out['h2_tau_h_vs_pass'][f'{hours} h hold'] = binned(ph.tau_h2_h, r['pass'][TIER], edges)
    # grind size against the same step (τ ∝ d²)
    out['h2_grind_vs_pass_48h'] = {f'{g} um': float(evaluate(Design(finish='melt', h2=True, h2_T=925, h2_hours=48, grind_um=g, melt_G=20, melt_minutes=10), ph)['pass'][TIER].mean())
                                    for g in (60, 100, 150, 250, 400)}
    # carbonyl: yield against the Fe time constant
    cedges = np.array([15, 30, 60, 120, 300])
    out['carbonyl_tau_h_vs_yield_pass'] = {}
    for label, d in (('100 bar, 72 h', Design(finish='carbonyl', grind_um=100, carb_P_bar=100, carb_hours=72)),
                     ('200 bar, 168 h', Design(finish='carbonyl', grind_um=100, carb_P_bar=200, carb_hours=168))):
        r = evaluate(d, ph)
        out['carbonyl_tau_h_vs_yield_pass'][label] = binned(ph.tau_carb_h, r['pass'][TIER], cedges)
    # gravity needed by the melt finisher (after H2), 20 min hold, 10 cm depth
    out['melt_gravity'] = {}
    for label, grind in (('concentrate (grind 100 um)', 100), ('coarse concentrate (grind 800 um)', 800)):
        rows = {}
        for G in (0.0001, 0.001, 0.01, 0.1, 1, 10, 100):
            s = summarise(Design(finish='melt', h2=True, h2_T=925, h2_hours=96, grind_um=grind, melt_G=G), ph)
            rows[str(G)] = {'purity_P50': s['purity_pct'], 'P_pass': s['P_pass'][TIER]}
        out['melt_gravity'][label] = rows
    return out


def main():
    quick = '--quick' in sys.argv
    trials = 120 if quick else 600
    res = {'tier_searched': TIER, 'tiers': {k: {'S_max_pct': v[0], 'purity_min_pct': v[1]} for k, v in TIERS.items()},
           'physics_ranges': {k: {'low': v[0], 'high': v[1], 'what': v[3]} for k, v in PHYSICS_RANGES.items()}, 'feeds': {}}
    for feed in ('H', 'L', 'EH'):
        ph = draw_physics(1500 if quick else 3000, feed)
        rows = []
        for route in ROUTES:
            best = search(route, ph, trials=trials, tier=TIER)
            d = Design(**best['design'])
            best['S_sensitivity'] = sensitivity(d, ph, 'S_pct')
            best['yield_sensitivity'] = sensitivity(d, ph, 'yield_')
            rows.append(best)
        rows.sort(key=lambda r: (-r['P_pass'][TIER], r['energy_kwh_per_kg']['P50']))
        res['feeds'][feed] = rows
        print(f'\n=== feed {feed} (best design per route, ranked by P(pass {TIER}))')
        for r in rows:
            pp = r['P_pass']
            print(f"{r['route']:32s} S {r['S_pct']['P50']:.3f} (P90 {r['S_pct']['P90']:.2f}) pur {r['purity_pct']:.1f} yld {r['yield']['P50']:.2f}"
                  f" E {r['energy_kwh_per_kg']['P50']:.2f} imp {r['imports_kg_per_t']['P50']:.0f} h {r['hours_per_batch']:.0f}"
                  f"  pass {' / '.join(f'{v:.2f}' for v in pp.values())}")
    res['falsifiers'] = falsifiers(draw_physics(6000, 'H', seed=5))
    os.makedirs(OUT, exist_ok=True)
    json.dump(res, open(os.path.join(OUT, 'results.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
