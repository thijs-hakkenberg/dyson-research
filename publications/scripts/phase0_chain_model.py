"""
Phase 0 chain closure and delivered cost per kilogram (rq-0-61).

One Monte Carlo draw follows the product chain the consensus describes:
  plant output → tug cycles (cycle time and Δv per leg from the rq-0-52 accessibility screen)
  → fleet size, propellant per cycle and per year → imported mass and launch mass over the
  0B run → 0B cost (BOM lines, with tugs, launch and propellant recomputed from the physics)
  → $/kg delivered to SEL1, against shipping the same mass from Earth at the same launch
  price (Claude's DEL-007: one price model for both sides of the economics gate).

Second pass (2026-11): `trajectory='optimised'` takes cycles from the rq-0-52 low-thrust study
(publications/data/nea-trajectories/legs.csv), re-checking each leg against the thrust of the
tug being modelled, and `replacements=True` buys replacement tugs, plant modules and robots on
runs longer than their service life.

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
LEGS = os.path.join(ROOT, 'publications', 'data', 'nea-trajectories', 'legs.csv')
# The tug the rq-0-52 study flew: 1.5 MW, 60% efficient, 2,500 s; 175 t leaving SEL1, 330 t leaving the asteroid
STUDY = {'power_mw': 1.5, 'isp_s': 2500.0, 'm_out_t': 175.0, 'm_in_t': 330.0}
POWER_SHARE = 0.55  # share of tug dry mass and cost that scales with installed power
LGA_DAYS = 30.0
MIN_STAY_DAYS = 60.0

ASSUMPTIONS = {
    'commissioning_years': 'U(1, 2) from 0B start to the first product departing the NEA (not in consensus)',
    'site_power_mass_t': 'log-uniform 60–550 t for 2–8 MW at the NEA (consensus gives no mass; GPT placeholder 550 t)',
    'spares_import_t_per_yr': 'U(20, 60) t/yr (bom-0-14 gives cost, not mass)',
    'earth_material_cost_per_kg': 'U(50, 500) $/kg for the Earth-made equivalent product before launch',
    'site_cargo_outbound_t': 'U(0, 20) t per tug trip (spares and consumables on the outbound leg)',
    'tug_scaling_with_power': '55% of tug dry mass and unit cost scales with installed power, 45% is fixed (not in consensus)',
    'leg_feasibility_at_other_thrust': 'an optimised leg stays flyable if its thrust fraction fits the modelled tug\'s '
    'acceleration (0.95 margin); its Δv is not re-optimised, and legs infeasible in the study are never added back',
    'tug_life_years': 'U(10, 15): Claude and GPT carry a 15-year objective, Gemini states none; replacement is pro rata for the years beyond that life',
    'plant_life_years': 'U(10, 15) (bom-0-3 design life); 40–70% of plant cost and mass is replaced at end of life (not in consensus)',
    'robot_attrition_per_yr': 'U(0.3, 0.7) robots a year beyond the first 6.25 years (from 2–4 replacements on 6 active in bom-0-2)',
    'not_replaced': 'site power, the SEL1 node and the propellant yard are assumed to last 20 years',
    'run_rate_0b_lines': 'ops, spares and comms 0B lines rescaled from the run length their consensus priced '
    '(6.25, 5 and 7 yr) to the drawn run',
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
    trajectory: str = 'catalogue'  # 'consensus' (5 km/s legs, 3-year cycle, as written) or 'optimised' (rq-0-52 second pass)
    lga: float = 1.0  # km/s of lunar-flyby excess speed, for 'optimised' (0, 1.0 or 1.5)
    lga_days: float = LGA_DAYS  # time allowance per flyby-assisted leg; the literature supports 60–90 (rq-0-52)
    tug_power_mw: float = 1.5
    target_fraction: float = 1.0  # sample targets from this fastest share of those that close ('optimised')
    replacements: bool = False
    tug_life_yr: tuple = (10, 15)
    plant_life_yr: tuple = (10, 15)
    plant_replace_fraction: tuple = (0.4, 0.7)
    robot_attrition_per_yr: tuple = (0.3, 0.7)
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


_LEG_CACHE = {}


def load_legs(path: str = LEGS) -> dict:
    """{target: {lga: {'out'|'in': array of (depart_day, tof_days, dv_kms, thrust_fraction)}}}"""
    if path in _LEG_CACHE:
        return _LEG_CACHE[path]
    legs = {}
    for r in csv.DictReader(open(path)):
        d = legs.setdefault(r['target'], {}).setdefault(float(r['lga_vinf']), {'out': [], 'in': []})
        d[r['leg']].append((float(r['depart_year']) * 365.25, float(r['tof_days']), float(r['low_thrust_kms']), float(r['thrust_fraction'])))
    for t in legs.values():
        for g in t.values():
            for k in ('out', 'in'):
                g[k] = np.array(g[k]).reshape(-1, 4)
    _LEG_CACHE[path] = legs
    return legs


def best_cycle(g: dict, leg_cap: float, s_out: float, s_in: float, lga: float, lga_days: float = LGA_DAYS):
    """Shortest cycle (years) and its leg Δv for one target, using only legs the tug can fly:
    Δv within the cap and thrust fraction within the tug's acceleration relative to the study's."""
    o, i = g['out'], g['in']
    o = o[(o[:, 2] <= leg_cap) & (o[:, 3] <= 0.95 * s_out)]
    i = i[(i[:, 2] <= leg_cap) & (i[:, 3] <= 0.95 * s_in)]
    if len(o) == 0 or len(i) == 0:
        return None
    ready = o[:, 0] + o[:, 1] + MIN_STAY_DAYS  # earliest return departure for each outbound leg
    home = i[:, 0] + i[:, 1]
    ok = i[None, :, 0] >= ready[:, None]
    cyc = np.where(ok, home[None, :] - o[:, None, 0], np.inf)
    a, b = np.unravel_index(np.argmin(cyc), cyc.shape)
    if not np.isfinite(cyc[a, b]):
        return None
    pen = 2 * lga_days if lga > 0 else 0.0
    return (cyc[a, b] + pen) / 365.25, o[a, 2], i[b, 2]


def optimised_cycles(c: 'ChainSettings', dry_t: float, payload_t: float, isp_s: float, cargo_t: float = 10.0):
    """Per-target (cycle_years, out_dv, in_dv) for the tug being modelled. The tug's
    acceleration on each leg depends on the propellant it carries, which depends on the legs
    chosen, so each target is solved twice."""
    ve = isp_s * G0 / 1e3
    thrust = (c.tug_power_mw / STUDY['power_mw']) * (STUDY['isp_s'] / isp_s)
    rows = []
    for name, by_lga in load_legs().items():
        g = by_lga.get(c.lga)
        if g is None:
            continue
        s_out, s_in, res = thrust, thrust, None
        for _ in range(2):
            res = best_cycle(g, c.leg_cap, s_out, s_in, c.lga, c.lga_days)
            if res is None:
                break
            _, dvo, dvi = res
            m_in = (dry_t + payload_t) * (np.exp(dvi / ve) - 1)
            m_in_start = dry_t + payload_t + m_in
            m_out_start = (dry_t + cargo_t + m_in) * np.exp(dvo / ve)
            s_in = thrust * STUDY['m_in_t'] / m_in_start
            s_out = thrust * STUDY['m_out_t'] / m_out_start
        if res is not None:
            res = best_cycle(g, c.leg_cap, s_out, s_in, c.lga, c.lga_days)
        if res is not None and res[0] <= c.max_cycle_years:
            rows.append((name,) + res)
    return rows


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
    elif c.trajectory == 'optimised':
        scale = 1 - POWER_SHARE + POWER_SHARE * c.tug_power_mw / STUDY['power_mw']
        rows = optimised_cycles(c, float(np.mean(c.tug_dry_t)) * scale, float(np.mean(c.payload_t)), float(np.mean(c.isp_s)))
        if not rows:
            raise ValueError('no optimised targets close for this tug under these limits')
        rows.sort(key=lambda r: r[1])
        cyc, o, i = (np.array([r[k] for r in rows]) for k in (1, 2, 3))
        pick = rng.integers(0, max(1, int(np.ceil(len(cyc) * c.target_fraction))), n)
        T, dv_out, dv_in = cyc[pick], o[pick], i[pick]
        targets = len(cyc)
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
    power_scale = 1 - POWER_SHARE + POWER_SHARE * c.tug_power_mw / STUDY['power_mw']
    md = _u(rng, c.tug_dry_t, n) * power_scale
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
    n_robots = rng.integers(c.robots[0], c.robots[1] + 1, n)
    robot_t = _u(rng, c.robot_mass_t, n)
    robots = n_robots * robot_t
    plant_t = _u(rng, c.plant_mass_t, n)
    hardware_t = plant_t + fleet * md + robots + site_power + _u(rng, c.node_mass_t, n)
    tug_unit = _u(rng, c.tug_unit_cost, n) * power_scale
    replace_t = np.zeros(n)
    replace_b = np.zeros(n)
    if c.replacements:
        # pro rata: hardware is replaced as it wears out, and only for the years still to run
        tug_gen = np.maximum(Y / _u(rng, c.tug_life_yr, n) - 1, 0)
        plant_gen = np.maximum(Y / _u(rng, c.plant_life_yr, n) - 1, 0)
        frac = _u(rng, c.plant_replace_fraction, n)
        extra_robots = _u(rng, c.robot_attrition_per_yr, n) * np.maximum(Y - 6.25, 0)
        replace_t = tug_gen * fleet * md + plant_gen * frac * plant_t + extra_robots * robot_t
        replace_b = (tug_gen * fleet * tug_unit + plant_gen * frac * lines['bom-0-3'][1]
                     + extra_robots * lines['bom-0-2'][1] / n_robots)
        hardware_t = hardware_t + replace_t
    pack = _u(rng, c.packaging, n)
    propellant_t = prop_yr * Y * pack
    launch_t = hardware_t + propellant_t + spares_yr * Y
    import_ratio = (prop_yr * pack + spares_yr) / P
    import_ratio_all = import_ratio + replace_t / (Y * P)

    # --- 0B cost -------------------------------------------------------------------------
    price = _u(rng, c.launch_price_per_kg, n)
    tugs_b = fleet * tug_unit
    launch_b = launch_t * 1e3 * price
    propellant_b = (prop_yr * Y * 1e3 * _u(rng, c.iodine_per_kg, n)
                    + prop_yr * Y / 5 * _u(rng, c.cartridge_cost, n) + _u(rng, c.yard_cost, n))
    replaced = {'bom-0-4': tugs_b, 'bom-0-8': launch_b, 'bom-0-16': propellant_b}
    for k, yrs in RUN_RATE_0B.items():
        replaced[k] = lines[k][1] * Y / yrs
    base_b = sum(replaced.get(k, v[1]) for k, v in lines.items()) + replace_b
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
        'import_ratio_with_replacements': {'P50': q(import_ratio_all, 0.5), 'P(<=0.5)': float((import_ratio_all <= 0.5).mean())},
        'cycle_years': {'P10': q(T, 0.1), 'P50': q(T, 0.5), 'P90': q(T, 0.9)},
        'replacement_cost_B': {'P50': q(replace_b / 1e9, 0.5)},
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
