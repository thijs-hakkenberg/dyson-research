"""
Phase 0 chain closure and delivered cost per kilogram (rq-0-61).

One Monte Carlo draw follows the product chain the consensus describes:
  plant output → tug cycles (cycle time and Δv per leg from the rq-0-52 accessibility screen)
  → fleet size, propellant per cycle and per year → imported mass and launch mass over the
  0B run → 0B cost (BOM lines, with tugs, launch and propellant recomputed from the physics)
  → $/kg delivered to SEL1, against shipping the same mass from Earth at the same launch
  price (Claude's DEL-007: one price model for both sides of the economics gate).

Everything not recomputed comes from the consensus envelopes in phase-0-bom.json via
phase0_cost_risk.sample_lines. Each assumption that is not in a consensus document is
named in ASSUMPTIONS and reported with the results.
"""

from __future__ import annotations

import csv
import os
from dataclasses import dataclass, field

import numpy as np
from scipy.stats import spearmanr

from phase0_cost_risk import ROOT, Settings, load_bom, sample_lines

G0 = 9.80665
CANDIDATES = os.path.join(ROOT, 'publications', 'data', 'nea-catalogue', 'candidates.csv')

ASSUMPTIONS = {
    'commissioning_years': 'U(1, 2) from 0B start to the first product departing the NEA (not in consensus)',
    'site_power_mass_t': 'log-uniform 60–550 t for 2–8 MW at the NEA (consensus gives no mass; GPT placeholder 550 t)',
    'spares_import_t_per_yr': 'U(20, 60) t/yr (bom-0-14 gives cost, not mass)',
    'earth_material_cost_per_kg': 'U(50, 500) $/kg for the Earth-made equivalent product before launch',
    'site_cargo_outbound_t': 'U(0, 20) t per tug trip (spares and consumables on the outbound leg)',
    'run_rate_0b_lines': 'ops, spares and comms 0B lines rescaled from the run length their consensus priced '
    '(6.25, 5 and 7 yr) to the drawn run; tug, plant and robot life beyond ~7 yr not modelled (no replacements)',
}

# 0B lines priced per year of operation, and the run length their consensus assumed
RUN_RATE_0B = {'bom-0-10': 6.25, 'bom-0-14': 5.0, 'bom-0-9': 7.0}


@dataclass
class ChainSettings:
    n: int = 40_000
    seed: int = 11
    product_t_per_yr: tuple = (1000, 1300)  # bom-0-3 3-train reference, delivered
    ops_years: tuple = (6.0, 6.5)  # bom-0-10 0B operating years
    leg_cap: float = 6.5  # which accessibility column supplies cycles (km/s per leg)
    max_cycle_years: float = 4.0
    trajectory: str = 'catalogue'  # or 'consensus' (5 km/s legs, 3-year cycle, as written)
    isp_s: tuple = (2000, 3000)  # bom-0-4 ~2,500 s; bom-0-16 trade 3,000–3,500
    efficiency: float = 0.6
    tug_dry_t: tuple = (38, 70)  # bom-0-4 divergent views
    payload_t: tuple = (150, 300)  # bom-0-4
    tug_unit_cost: tuple = (0.3e9, 0.8e9)  # bom-0-4 consensus, including arrays
    tug_reserve: int = 2
    launch_price_per_kg: tuple = (1800, 4700)  # bom-0-8: GPT ~1.8–2.6k effective … Claude P_hand 4.7k
    packaging: tuple = (1.06, 1.10)  # bom-0-16
    iodine_per_kg: tuple = (35, 70)  # bom-0-16
    cartridge_cost: tuple = (0.15e6, 1.0e6)  # per 5 t cartridge, bom-0-16
    yard_cost: tuple = (120e6, 475e6)  # bom-0-16 SEL1 yard placeholder
    argon_t_per_yr: tuple = (15, 45)  # bom-0-16
    plant_mass_t: tuple = (250, 400)  # bom-0-3
    robots: tuple = (10, 12)
    robot_mass_t: tuple = (2.65, 3.4)  # bom-0-2
    node_mass_t: tuple = (25, 40)  # bom-0-13
    contingency_0b: float = 0.65  # bom-0-17 point
    earth_contingency: tuple = (0.20, 0.25)  # bom-0-17 fallback comparator (Claude)
    cost: Settings = field(default_factory=lambda: Settings(rho=0.3))


def _u(rng, lo_hi, n):
    return rng.uniform(lo_hi[0], lo_hi[1], n)


def load_cycles(leg_cap: float, max_cycle: float, h_max: float = 22.0):
    """(cycle_years, out_dv, in_dv) for catalogue targets closing under the leg cap."""
    rows = list(csv.DictReader(open(CANDIDATES)))
    cyc, out, inn = [], [], []
    col = f'cycle_yr_leg{leg_cap}'
    for r in rows:
        if not r.get(col) or float(r['H']) > h_max or float(r[col]) > max_cycle:
            continue
        # the per-leg Δv columns are recorded for the 6.5 km/s cap; other caps use the cap
        o = float(r['out_dv_leg6.5']) if r.get('out_dv_leg6.5') and leg_cap == 6.5 else leg_cap
        i = float(r['in_dv_leg6.5']) if r.get('in_dv_leg6.5') and leg_cap == 6.5 else leg_cap
        cyc.append(float(r[col]))
        out.append(o)
        inn.append(i)
    return np.array(cyc), np.array(out), np.array(inn)


def simulate(bom: dict, c: ChainSettings = ChainSettings()) -> dict:
    rng = np.random.default_rng(c.seed)
    n = c.n
    lines = sample_lines(bom, Settings(**{**c.cost.__dict__, 'n': n}), rng)

    # --- trajectories --------------------------------------------------------------------
    if c.trajectory == 'consensus':
        T = np.full(n, 3.0)
        dv_out = np.full(n, 5.0)
        dv_in = np.full(n, 5.0)
        targets = None
    else:
        cyc, o, i = load_cycles(c.leg_cap, c.max_cycle_years)
        if len(cyc) == 0:
            raise ValueError('no catalogue targets close under these limits')
        pick = rng.integers(0, len(cyc), n)
        T, dv_out, dv_in = cyc[pick], o[pick], i[pick]
        targets = len(cyc)

    # --- tugs and propellant -------------------------------------------------------------
    P = _u(rng, c.product_t_per_yr, n)
    isp = _u(rng, c.isp_s, n)
    ve = isp * G0 / 1e3  # km/s
    md = _u(rng, c.tug_dry_t, n)
    mp = _u(rng, c.payload_t, n)
    cargo = rng.uniform(0, 20, n)
    m_in = (md + mp) * (np.exp(dv_in / ve) - 1)
    m_out = (md + cargo + m_in) * np.exp(dv_out / ve) - (md + cargo + m_in)
    prop_cycle = m_in + m_out
    trips_per_yr = P / mp
    fleet = np.ceil(trips_per_yr * T) + c.tug_reserve
    argon = _u(rng, c.argon_t_per_yr, n)
    prop_yr = trips_per_yr * prop_cycle + argon

    # --- run length and delivered mass ---------------------------------------------------
    Y = _u(rng, c.ops_years, n)
    commissioning = rng.uniform(1, 2, n)
    first_delivery = commissioning + T / 2
    delivered_t = P * np.maximum(Y - first_delivery, 0)

    # --- imported and launched mass ------------------------------------------------------
    spares_yr = rng.uniform(20, 60, n)
    site_power = np.exp(rng.uniform(np.log(60), np.log(550), n))
    robots = rng.integers(c.robots[0], c.robots[1] + 1, n) * _u(rng, c.robot_mass_t, n)
    hardware_t = _u(rng, c.plant_mass_t, n) + fleet * md + robots + site_power + _u(rng, c.node_mass_t, n)
    pack = _u(rng, c.packaging, n)
    propellant_t = prop_yr * Y * pack
    launch_t = hardware_t + propellant_t + spares_yr * Y
    import_ratio = (prop_yr * pack + spares_yr) / P

    # --- 0B cost -------------------------------------------------------------------------
    price = _u(rng, c.launch_price_per_kg, n)
    tugs_b = fleet * _u(rng, c.tug_unit_cost, n)
    launch_b = launch_t * 1e3 * price
    propellant_b = (prop_yr * Y * 1e3 * _u(rng, c.iodine_per_kg, n)
                    + prop_yr * Y / 5 * _u(rng, c.cartridge_cost, n) + _u(rng, c.yard_cost, n))
    replaced = {'bom-0-4': tugs_b, 'bom-0-8': launch_b, 'bom-0-16': propellant_b}
    for k, yrs in RUN_RATE_0B.items():
        replaced[k] = lines[k][1] * Y / yrs
    base_b = sum(replaced.get(k, v[1]) for k, v in lines.items())
    base_a = sum(v[0] for v in lines.values())
    with_cont_b = base_b * (1 + c.contingency_0b)

    kg = delivered_t * 1e3
    with np.errstate(divide='ignore', invalid='ignore'):
        per_kg_0b = np.where(kg > 0, with_cont_b / kg, np.inf)
        per_kg_0b_base = np.where(kg > 0, base_b / kg, np.inf)
        per_kg_all = np.where(kg > 0, (with_cont_b + base_a * 1.45) / kg, np.inf)
    earth = (price + _u(rng, (50, 500), n)) * (1 + _u(rng, c.earth_contingency, n))
    # Break-even: the launch price at which Earth supply costs what 0B costs per kg. 0B also
    # pays launch, so solve per draw: (fixed + L·m)/kg = (L + mat)(1+e)
    fixed = with_cont_b - launch_b * (1 + c.contingency_0b)
    m_kg = launch_t * 1e3 * (1 + c.contingency_0b)
    mat = rng.uniform(50, 500, n)
    ec = _u(rng, c.earth_contingency, n)
    with np.errstate(divide='ignore', invalid='ignore'):
        denom = kg * (1 + ec) - m_kg
        breakeven = np.where((denom > 0) & (kg > 0), (fixed - mat * (1 + ec) * kg) / denom, np.inf)

    def q(x, p):
        return float(np.quantile(x[np.isfinite(x)], p)) if np.isfinite(x).any() else None

    inputs = {'cycle_years': T, 'dv_in': dv_in, 'dv_out': dv_out, 'isp': isp, 'payload_t': mp, 'tug_dry_t': md,
              'product_t_per_yr': P, 'launch_price': price, 'site_power_t': site_power}
    finite = np.isfinite(per_kg_0b)
    sens = {k: float(spearmanr(v[finite], per_kg_0b[finite]).statistic) for k, v in inputs.items() if np.std(v) > 0}
    return {
        'targets_sampled': targets,
        'fleet': {'P10': q(fleet, 0.1), 'P50': q(fleet, 0.5), 'P90': q(fleet, 0.9)},
        'propellant_per_cycle_t': {'P10': q(prop_cycle, 0.1), 'P50': q(prop_cycle, 0.5), 'P90': q(prop_cycle, 0.9)},
        'propellant_t_per_yr': {'P10': q(prop_yr, 0.1), 'P50': q(prop_yr, 0.5), 'P90': q(prop_yr, 0.9)},
        'import_ratio': {'P10': q(import_ratio, 0.1), 'P50': q(import_ratio, 0.5), 'P90': q(import_ratio, 0.9),
                         'P(<=0.5)': float((import_ratio <= 0.5).mean()), 'P(<=0.35)': float((import_ratio <= 0.35).mean())},
        'launch_kt': {'P10': q(launch_t / 1e3, 0.1), 'P50': q(launch_t / 1e3, 0.5), 'P90': q(launch_t / 1e3, 0.9),
                      'P(<1.3)': float((launch_t < 1300).mean()), 'P(>6)': float((launch_t > 6000).mean())},
        'propellant_share_of_launch': q(propellant_t / launch_t, 0.5),
        'delivered_kt': {'P10': q(delivered_t / 1e3, 0.1), 'P50': q(delivered_t / 1e3, 0.5), 'P90': q(delivered_t / 1e3, 0.9)},
        '0B_cost_with_contingency_B': {'P10': q(with_cont_b / 1e9, 0.1), 'P50': q(with_cont_b / 1e9, 0.5), 'P90': q(with_cont_b / 1e9, 0.9)},
        'per_kg_0B_with_contingency': {'P10': q(per_kg_0b, 0.1), 'P50': q(per_kg_0b, 0.5), 'P90': q(per_kg_0b, 0.9)},
        'per_kg_0B_base': {'P50': q(per_kg_0b_base, 0.5)},
        'per_kg_0A_and_0B': {'P50': q(per_kg_all, 0.5)},
        'earth_per_kg': {'P10': q(earth, 0.1), 'P50': q(earth, 0.5), 'P90': q(earth, 0.9)},
        'P(0B beats Earth)': float((per_kg_0b < earth).mean()),
        'ratio_0B_to_earth': {'P10': q(per_kg_0b / earth, 0.1), 'P50': q(per_kg_0b / earth, 0.5), 'P90': q(per_kg_0b / earth, 0.9)},
        'breakeven_launch_price_per_kg': {'P10': q(breakeven, 0.1), 'P50': q(breakeven, 0.5), 'P90': q(breakeven, 0.9)},
        'sensitivity_spearman_per_kg': dict(sorted(sens.items(), key=lambda kv: -abs(kv[1]))),
    }
