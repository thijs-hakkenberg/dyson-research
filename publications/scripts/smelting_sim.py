"""
Fe-Ni process-route simulator for Phase 0 (rq-0-56, rq-0-11).

Question: is there a way to turn chondritic asteroid regolith into acceptable Fe-Ni product
in space, and which configuration does it? The known obstacle (bom-0-3 consensus,
2026-10-20): melting dissolves troilite (FeS) sulfur into the metal, flux to remove it must
be imported, and the no-melt carbonyl route has unproven kinetics on meteoritic metal.

This is a screening model: one mass balance (metal, troilite, silicate; sulfur tracked)
pushed through a flowsheet of unit operations, each a first-order physical model with
uncertain parameters drawn by Monte Carlo. It ranks routes and shows which unknown decides
each one. It is not a design tool; every parameter range in PHYSICS_RANGES needs the
literature check in PLAN-2026-11.md §4.4 before any number here is quoted as a result.

Flowsheet
    grind + magnetic separation
      → [H2 desulfurisation, solid state, ≤950 °C]      FeS + H2 = Fe + H2S, H2S cold-trapped
      → [liquation in a hot centrifuge, 990–1450 °C]    drain the Fe–S liquid from solid metal
      → finish: 'sinter' (hot-press, no melt) | 'melt' (centrifuge; optional CaO flux,
                 optional vacuum hold) | 'carbonyl' (CO extraction + vapour deposition)

Unit-operation physics
    beneficiation   liberation from grind size against metal grain size; brittle troilite and
                    silicate are rejected when liberated, locked fractions carry over
    H2 desulf       equilibrium K(T) from ΔG° = 59,960 − 3.2·T J/mol, shrinking-core kinetics,
                    gas circulated = S / (K · approach)
    liquation       Fe–S liquidus for the liquid composition; packed-bed residual saturation
                    from the capillary number (Dombrowski & Brownell centrifuge correlation)
    melt            Hadamard–Rybczynski settling of the dispersed phase at the rotor's G;
                    sulfur split by a slag/metal partition ratio; vacuum loss first order;
                    Fe evaporation by Langmuir flux, reduced by the enclosure
    carbonyl        first-order extraction with an uncertain time constant scaled by CO
                    pressure and grain size; S stays in the residue
    rotor           self-stress ρ·G·r against an allowable stress for the hot material
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

G_EARTH = 9.80665
SIGMA_SB = 5.670374e-8
R_GAS = 8.314462

# --- material constants -----------------------------------------------------------------
RHO_METAL, RHO_FES, RHO_SIL = 7800.0, 4600.0, 3300.0
RHO_METAL_L, RHO_SIL_L = 7000.0, 2800.0
S_IN_FES = 0.365
CP_METAL, CP_FES, CP_SIL = 0.70, 0.75, 1.15  # kJ/kg/K, averaged to process temperature
LAT_METAL, LAT_FES, LAT_SIL = 270.0, 370.0, 400.0  # kJ/kg
T_REF = 250.0  # K, feed temperature
T_EUTECTIC = 988.0  # °C, Fe–FeS
# Fe–S liquidus on the iron-rich side: wt% S in the liquid in equilibrium with solid Fe
_LIQ_T = np.array([988.0, 1100.0, 1200.0, 1300.0, 1400.0, 1500.0, 1538.0])
_LIQ_S = np.array([31.6, 27.0, 23.0, 18.0, 12.0, 3.5, 0.0])

FEEDS = {
    # wt fractions of run-of-mine material: Fe-Ni metal, troilite; rest silicate
    'H': dict(metal=(0.15, 0.19), fes=(0.050, 0.060)),
    'L': dict(metal=(0.06, 0.09), fes=(0.055, 0.065)),
    'LL': dict(metal=(0.02, 0.04), fes=(0.050, 0.060)),
    'EH': dict(metal=(0.20, 0.28), fes=(0.07, 0.12)),
}

# Uncertain physics: (low, high, distribution). Sources are generic until §4.4 is done.
PHYSICS_RANGES = {
    'metal_d50_um': (80, 400, 'log', 'metal grain size in ordinary chondrites'),
    'locked_fes': (0.08, 0.45, 'lin', 'share of troilite intergrown with metal at coarse grind'),
    'locked_sil': (0.004, 0.03, 'log', 'share of silicate mass carried at coarse grind'),
    'mag_recovery': (0.88, 0.98, 'lin', 'metal recovery of magnetic separation when liberated'),
    'tau_h2_h': (2, 40, 'log', 'H2 desulfurisation time constant, 100 µm troilite at 900 °C'),
    'h2_approach': (0.3, 0.9, 'lin', 'approach to H2S/H2 equilibrium in the bed'),
    'gamma_sulfide': (0.35, 0.9, 'lin', 'surface tension of Fe–S liquid, N/m'),
    'wetting_cos': (0.6, 1.0, 'lin', 'cosine of the contact angle of Fe–S liquid on metal'),
    'residual_factor': (0.5, 2.0, 'log', 'multiplier on the residual-saturation correlation'),
    'bed_porosity': (0.34, 0.45, 'lin', 'packed metal grain bed'),
    'mu_sil_1600': (0.3, 5.0, 'log', 'silicate melt viscosity at 1600 °C, Pa·s'),
    'incl_d50_um': (15, 120, 'log', 'silicate inclusion / metal droplet size in the melt'),
    'ls_native': (0.3, 5.0, 'log', 'S partition slag/metal for FeO-bearing chondritic slag'),
    'ls_flux': (20, 200, 'log', 'S partition with CaO-rich reducing slag'),
    'k_vac_S': (5e-7, 1e-5, 'log', 'vacuum S evaporation rate constant, m/s'),
    'tau_carb_h': (15, 300, 'log', 'Fe carbonylation time constant, 100 µm at 100 bar, 175 °C'),
    'carb_cap': (0.80, 0.97, 'lin', 'maximum Fe extraction (passivation, locked metal)'),
    'co_loss': (0.002, 0.03, 'log', 'CO lost (leaks, side reactions) per unit of CO bound to product'),
    'heat_eff': (0.6, 0.8, 'lin', 'induction heating efficiency'),
    'eps_eff': (0.02, 0.06, 'lin', 'effective emissivity of the shielded furnace shell'),
    'bond_wi': (12, 20, 'lin', 'Bond work index of chondritic silicate, kWh/t'),
    'refractory_melt': (2, 10, 'lin', 'refractory wear in melt routes, kg per t metal'),
    'mill_wear': (0.05, 0.5, 'log', 'grinding media wear, kg per t ROM at 300 µm'),
}

# Allowable rotor stress (Pa) against process temperature (°C): superalloy, then TZM-class
_ROTOR_T = np.array([900.0, 1000.0, 1100.0, 1300.0, 1500.0, 1700.0])
_ROTOR_S = np.array([120e6, 80e6, 40e6, 60e6, 40e6, 25e6])
RHO_ROTOR = 9000.0


@dataclass
class Physics:
    """n Monte Carlo draws of the uncertain quantities (arrays of length n)."""

    n: int
    feed: str
    metal: np.ndarray
    fes: np.ndarray
    p: dict

    def __getattr__(self, k):
        try:
            return self.__dict__['p'][k]
        except KeyError as e:
            raise AttributeError(k) from e


def draw_physics(n: int = 2000, feed: str = 'H', seed: int = 1) -> Physics:
    rng = np.random.default_rng(seed)
    f = FEEDS[feed]
    p = {}
    for k, (lo, hi, dist, _) in PHYSICS_RANGES.items():
        p[k] = np.exp(rng.uniform(np.log(lo), np.log(hi), n)) if dist == 'log' else rng.uniform(lo, hi, n)
    return Physics(n, feed, rng.uniform(*f['metal'], n), rng.uniform(*f['fes'], n), p)


@dataclass(frozen=True)
class Design:
    finish: str = 'melt'  # 'sinter' | 'melt' | 'carbonyl'
    grind_um: float = 300.0
    # H2 desulfurisation
    h2: bool = False
    h2_T: float = 900.0
    h2_hours: float = 12.0
    # liquation
    liquation: bool = False
    liq_T: float = 1100.0
    liq_G: float = 300.0  # multiples of Earth gravity
    liq_pellet_um: float = 0.0  # 0 = bed of the ground grains; else agglomerated granules
    # melt
    melt_T: float = 1600.0
    melt_G: float = 1.0
    melt_minutes: float = 20.0
    melt_depth_m: float = 0.10
    flux_kg_per_kg: float = 0.0  # CaO per kg concentrate
    vacuum_minutes: float = 0.0
    enclosure: str = 'lidded'  # 'open' | 'lidded' | 'pressurised'
    # carbonyl
    carb_P_bar: float = 100.0
    carb_T: float = 175.0
    carb_hours: float = 72.0
    # rotor
    rotor_r_m: float = 0.5

    def label(self) -> str:
        parts = ['grind']
        if self.h2:
            parts.append('H2')
        if self.liquation:
            parts.append('liquation')
        fin = self.finish
        if fin == 'melt':
            fin += '+flux' if self.flux_kg_per_kg > 0 else ''
            fin += '+vac' if self.vacuum_minutes > 0 else ''
        parts.append(fin)
        return ' → '.join(parts)


# ---------------------------------------------------------------------------------------
# Unit operations. State: masses per kg of run-of-mine feed (arrays).
# ---------------------------------------------------------------------------------------

def beneficiate(ph: Physics, d: Design) -> dict:
    """Grind and magnetic separation. Finer grind liberates more, at more energy and wear."""
    lib = 1.0 / (1.0 + (d.grind_um / ph.metal_d50_um) ** 1.5)  # liberated share, 0..1
    metal = ph.metal * ph.mag_recovery * (0.90 + 0.10 * lib)
    fes = ph.fes * ph.locked_fes * (1.0 - 0.85 * lib)
    sil = (1 - ph.metal - ph.fes) * ph.locked_sil * (1.0 - 0.85 * lib)
    # Bond's law from 10 mm feed, kWh per kg ROM
    grind_kwh = 10 * ph.bond_wi * (1 / np.sqrt(d.grind_um) - 1 / np.sqrt(10_000.0)) / 1000.0
    wear = ph.mill_wear * np.sqrt(300.0 / d.grind_um) / 1000.0  # kg per kg ROM
    return dict(metal=metal, fes=fes, sil=sil, s_free=np.zeros(ph.n), energy=grind_kwh, imports=wear,
                hours=np.zeros(ph.n), lost_metal=ph.metal - metal)


def h2_desulfurise(st: dict, ph: Physics, d: Design) -> dict:
    """FeS + H2 → Fe + H2S below the eutectic; H2S frozen out, H2 recirculated."""
    T = d.h2_T + 273.15
    K = np.exp(-(59_960.0 - 3.2 * T) / (R_GAS * T))
    # troilite particle scale follows the grind; diffusion-limited → τ ∝ d², Arrhenius in T
    tau = ph.tau_h2_h * (min(d.grind_um, 400.0) / 100.0) ** 2 * np.exp(15_000.0 * (1 / T - 1 / 1173.15))
    x = 1.0 - np.exp(-d.h2_hours / tau)
    s_removed = st['fes'] * S_IN_FES * x
    st = dict(st)
    st['metal'] = st['metal'] + st['fes'] * x * (1 - S_IN_FES)
    st['fes'] = st['fes'] * (1 - x)
    # H2 circulated (kg) = mol S / (K·approach) · 2 g/mol; make-up = H leaving as H2S
    circulated = s_removed / 32.06 / (K * ph.h2_approach) * 2.016
    st['imports'] = st['imports'] + s_removed * 2.016 / 32.06 * 1.2
    solids = st['metal'] + st['fes'] + st['sil']
    heat = solids * (CP_METAL * (T - T_REF)) / 3600.0 / 0.9
    st['energy'] = st['energy'] + heat + circulated * 0.15  # blower + cold trap, kWh per kg H2 circulated
    st['hours'] = st['hours'] + d.h2_hours
    st['h2_circulated'] = circulated
    return st


def residual_saturation(n_cap):
    """Dombrowski & Brownell centrifuge drainage correlation (as used for filter cakes)."""
    n_cap = np.maximum(n_cap, 1e-9)
    return np.where(n_cap <= 0.14, 0.0524 * n_cap ** -0.19, 0.0139 * n_cap ** -0.86)


def liquate(st: dict, ph: Physics, d: Design) -> dict:
    """Hold between the Fe–FeS eutectic and the metal liquidus; spin the Fe–S liquid out."""
    st = dict(st)
    if d.liq_T < T_EUTECTIC:
        return st
    x_l = np.interp(d.liq_T, _LIQ_T, _LIQ_S) / 100.0  # wt fraction S in the liquid
    s = st['fes'] * S_IN_FES
    iron_avail = st['metal'] + st['fes'] * (1 - S_IN_FES)
    m_liq = np.minimum(s / max(x_l, 1e-6), s + iron_avail)  # all S goes to the liquid
    solid_metal = np.maximum(st['metal'] + st['fes'] - m_liq, 0.0)
    rho_l = RHO_FES + (RHO_METAL_L - RHO_FES) * (1 - x_l / 0.316)
    eps = ph.bed_porosity
    solids_vol = solid_metal / RHO_METAL + st['sil'] / RHO_SIL
    pore_vol = solids_vol * eps / (1 - eps)
    s0 = np.minimum(m_liq / rho_l / np.maximum(pore_vol, 1e-12), 1.0)
    dp = (d.liq_pellet_um if d.liq_pellet_um > 0 else min(d.grind_um, 600.0)) * 1e-6
    perm = dp**2 * eps**3 / (180 * (1 - eps) ** 2)
    n_cap = perm * rho_l * d.liq_G * G_EARTH / (ph.gamma_sulfide * ph.wetting_cos)
    s_inf = np.minimum(residual_saturation(n_cap) * ph.residual_factor, s0)
    # granules keep the liquid in their internal pores: only the share between granules drains
    internal = 0.5 if d.liq_pellet_um > 0 else 0.0
    kept = s_inf / np.maximum(s0, 1e-12) * (1 - internal) + internal
    m_res = m_liq * kept
    drained = m_liq - m_res
    st['lost_metal'] = st['lost_metal'] + drained * (1 - x_l)
    # what stays: solid metal + residual liquid, booked as metal + FeS-equivalent sulfur
    s_left = m_res * x_l
    st['fes'] = s_left / S_IN_FES
    st['metal'] = np.maximum(solid_metal + m_res - st['fes'], 0.0)
    T = d.liq_T + 273.15
    heated = solid_metal + m_liq + st['sil']
    st['energy'] = st['energy'] + (heated * CP_METAL * (T - T_REF) + m_liq * LAT_FES) / 3600.0 / ph.heat_eff
    st['imports'] = st['imports'] + st['metal'] * 0.5e-3  # liner wear at ≤1450 °C
    st['hours'] = st['hours'] + 1.0
    st['liq_drain_fraction'] = 1 - kept
    return st


def hr_velocity(drho, g, r, mu_c, mu_d):
    """Hadamard–Rybczynski terminal velocity of a fluid sphere."""
    return 2 * drho * g * r**2 / (3 * mu_c) * (mu_c + mu_d) / (2 * mu_c + 3 * mu_d)


def melt(st: dict, ph: Physics, d: Design) -> dict:
    """Melt in a spinning crucible: phases separate by density, sulfur splits metal/slag."""
    st = dict(st)
    T = d.melt_T + 273.15
    g = d.melt_G * G_EARTH
    flux = d.flux_kg_per_kg * (st['metal'] + st['fes'] + st['sil'])
    slag = st['sil'] + flux
    metal_l = st['metal'] + st['fes'] * (1 - S_IN_FES)
    s = st['fes'] * S_IN_FES
    # silicate fully molten only above ~1550 °C; below that it is a stiff crystal mush
    melt_frac = np.clip((d.melt_T - 1100.0) / 450.0, 0.05, 1.0)
    mu_sil = ph.mu_sil_1600 * np.exp(22_000.0 * (1 / T - 1 / 1873.15)) * (1 - 0.95 * (1 - melt_frac)) ** -2.5
    mu_met = 0.006
    vol_met, vol_slag = metal_l / RHO_METAL_L, slag / RHO_SIL_L
    metal_continuous = vol_met >= vol_slag
    r = ph.incl_d50_um * 1e-6 / 2
    v = np.where(metal_continuous,
                 hr_velocity(RHO_METAL_L - RHO_SIL_L, g, r, mu_met, mu_sil),
                 hr_velocity(RHO_METAL_L - RHO_SIL_L, g, r, mu_sil, mu_met))
    # dispersed elements start uniformly through the depth: share cleared in the hold
    cleared = np.clip(v * d.melt_minutes * 60.0 / d.melt_depth_m, 0.0, 1.0)
    # sulfur: equilibrium between metal and slag
    ls = ph.ls_flux if d.flux_kg_per_kg > 0 else ph.ls_native
    s_metal = s * metal_l / (metal_l + ls * np.maximum(slag, 1e-12))
    # vacuum hold: first order on the free surface, area/volume = 1/depth
    if d.vacuum_minutes > 0:
        s_metal = s_metal * np.exp(-ph.k_vac_S * d.vacuum_minutes * 60.0 / d.melt_depth_m)
    # Fe evaporation (Langmuir): log10 p(Pa) = 11.353 − 19,574/T (liquid Fe, ~8 Pa at 1600 °C),
    # cut by a lid or cover gas
    p_fe = 10 ** (11.353 - 19_574.0 / T)
    flux_fe = p_fe * np.sqrt(0.05585 / (2 * np.pi * R_GAS * T))  # kg/m²/s
    cut = {'open': 1.0, 'lidded': 0.02, 'pressurised': 0.001}[d.enclosure]
    area_per_kg = 1.0 / (RHO_METAL_L * d.melt_depth_m)
    evap = np.minimum(flux_fe * cut * area_per_kg * (d.melt_minutes + d.vacuum_minutes) * 60.0, 0.5) * metal_l
    # outcome: metal continuous → uncleared slag stays as inclusions; else uncleared metal is lost
    incl = np.where(metal_continuous, slag * (1 - cleared), 0.0)
    recovered = np.where(metal_continuous, metal_l, metal_l * cleared) - evap
    recovered = np.maximum(recovered, 0.0)
    st['lost_metal'] = st['lost_metal'] + (metal_l - recovered)
    st['metal'] = recovered
    st['fes'] = s_metal * (recovered / np.maximum(metal_l, 1e-12)) / S_IN_FES
    st['metal'] = np.maximum(st['metal'] - st['fes'] * (1 - S_IN_FES), 0.0)
    st['sil'] = incl
    heat = (metal_l * (CP_METAL * (T - T_REF) + LAT_METAL) + s * CP_FES * (T - T_REF)
            + slag * (CP_SIL * (T - T_REF) + LAT_SIL * melt_frac)) / 3600.0 / ph.heat_eff
    # shell loss for a 50 kg charge: area ≈ 1.5 m²
    hold_h = (d.melt_minutes + d.vacuum_minutes) / 60.0
    loss = ph.eps_eff * SIGMA_SB * T**4 * 1.5 * hold_h / 1000.0 / 50.0 * (metal_l + slag)
    st['energy'] = st['energy'] + heat + loss
    cover = {'open': 0.0, 'lidded': 0.0, 'pressurised': 3e-3}[d.enclosure]
    st['imports'] = st['imports'] + flux + recovered * (ph.refractory_melt / 1000.0 + cover)
    st['hours'] = st['hours'] + hold_h + 1.5
    st['evap_loss'] = evap
    st['flux'] = flux
    return st


def sinter(st: dict, ph: Physics, d: Design) -> dict:
    """Hot-press at ~1100 °C: consolidates, removes nothing."""
    st = dict(st)
    T = 1100.0 + 273.15
    mass = st['metal'] + st['fes'] + st['sil']
    st['energy'] = st['energy'] + mass * CP_METAL * (T - T_REF) / 3600.0 / 0.9
    st['imports'] = st['imports'] + st['metal'] * 0.5e-3
    st['hours'] = st['hours'] + 2.0
    return st


def carbonyl(st: dict, ph: Physics, d: Design) -> dict:
    """CO extraction of Fe and Ni as carbonyls, then vapour deposition. S and silicate stay behind."""
    st = dict(st)
    T = d.carb_T + 273.15
    # Arrhenius about 175 °C, but carbonyls decompose as T rises: cap falls above ~200 °C
    rate = np.exp(-60_000.0 / R_GAS * (1 / T - 1 / 448.15))
    tau = ph.tau_carb_h * (100.0 / d.carb_P_bar) * (min(d.grind_um, 600.0) / 100.0) / rate
    stability = np.clip(1.0 - max(d.carb_T - 200.0, 0.0) / 80.0 * (100.0 / d.carb_P_bar), 0.0, 1.0)
    x = ph.carb_cap * stability * (1.0 - np.exp(-d.carb_hours / tau))
    product = st['metal'] * x
    st['lost_metal'] = st['lost_metal'] + st['metal'] - product
    # 2.5 kg CO is bound per kg Fe and released again at deposition; a share is lost each cycle
    st['imports'] = st['imports'] + product * 2.5 * ph.co_loss + product * 1e-3
    # decomposition ~0.95 kWh/kg; recompressing the 2.5 kg CO released per kg Fe from ~1 bar
    # (isothermal, 70% efficient) + loop circulation
    st['energy'] = st['energy'] + product * (0.95 + 0.089 * np.log(d.carb_P_bar) + 0.05) + (
        st['metal'] + st['fes'] + st['sil']) * CP_METAL * (T - T_REF) / 3600.0 / 0.9
    st['hours'] = st['hours'] + d.carb_hours + 6.0
    st['metal'], st['fes'], st['sil'] = product, np.zeros(ph.n), np.zeros(ph.n)
    st['carb_extraction'] = x
    return st


def rotor_ok(d: Design) -> bool:
    """Rotor self-stress ρ·G·r within half the allowable for the hottest spinning step."""
    checks = []
    if d.liquation:
        checks.append((d.liq_T, d.liq_G))
    if d.finish == 'melt':
        checks.append((d.melt_T, d.melt_G))
    for T, G in checks:
        if RHO_ROTOR * G * G_EARTH * d.rotor_r_m > 0.5 * np.interp(T, _ROTOR_T, _ROTOR_S):
            return False
    return True


# ---------------------------------------------------------------------------------------
# Evaluation and scoring
# ---------------------------------------------------------------------------------------

TIERS = {
    # product sulfur (wt%), Fe+Ni purity (wt%)
    'structural (S≤0.05, ≥98)': (0.05, 98.0),
    'envelope (S≤0.10, ≥97)': (0.10, 97.0),
    'remelt stock (S≤0.5, ≥95)': (0.5, 95.0),
    'bulk mass (S≤2, ≥90)': (2.0, 90.0),
}
MIN_YIELD = 0.75  # product metal / metal in the mined feed
MAX_ENERGY = 7.0  # kWh per kg product (bom-0-5 upper estimate, whole plant)
MAX_IMPORT = 20.0  # kg imported per t product (≤25 t/yr on ~1.2 kt/yr)


def evaluate(d: Design, ph: Physics) -> dict:
    st = beneficiate(ph, d)
    if d.h2:
        st = h2_desulfurise(st, ph, d)
    if d.liquation:
        st = liquate(st, ph, d)
    st = {'melt': melt, 'sinter': sinter, 'carbonyl': carbonyl}[d.finish](st, ph, d)
    product = st['metal'] + st['fes'] + st['sil']
    with np.errstate(divide='ignore', invalid='ignore'):
        s_pct = np.where(product > 0, st['fes'] * S_IN_FES / product * 100, 100.0)
        purity = np.where(product > 0, (st['metal'] + st['fes'] * (1 - S_IN_FES)) / product * 100, 0.0)
        yld = st['metal'] / ph.metal
        energy = np.where(st['metal'] > 0, st['energy'] / st['metal'], np.inf)
        imports = np.where(st['metal'] > 0, st['imports'] / st['metal'] * 1000, np.inf)
    ok_common = (yld >= MIN_YIELD) & (energy <= MAX_ENERGY) & (imports <= MAX_IMPORT) & rotor_ok(d)
    out = dict(S_pct=s_pct, purity=purity, yield_=yld, energy=energy, imports=imports, hours=st['hours'],
               rom_per_product=1.0 / np.maximum(st['metal'], 1e-12), rotor_ok=rotor_ok(d), state=st)
    out['pass'] = {name: ok_common & (s_pct <= s) & (purity >= pu) for name, (s, pu) in TIERS.items()}
    return out


def summarise(d: Design, ph: Physics) -> dict:
    r = evaluate(d, ph)
    med = lambda x: float(np.median(x[np.isfinite(x)])) if np.isfinite(x).any() else float('inf')
    q = lambda x, p: float(np.quantile(x[np.isfinite(x)], p)) if np.isfinite(x).any() else float('inf')
    return {
        'route': d.label(),
        'design': {k: v for k, v in d.__dict__.items()},
        'S_pct': {'P10': q(r['S_pct'], 0.1), 'P50': med(r['S_pct']), 'P90': q(r['S_pct'], 0.9)},
        'purity_pct': med(r['purity']),
        'yield': {'P10': q(r['yield_'], 0.1), 'P50': med(r['yield_'])},
        'energy_kwh_per_kg': {'P50': med(r['energy']), 'P90': q(r['energy'], 0.9)},
        'imports_kg_per_t': {'P50': med(r['imports']), 'P90': q(r['imports'], 0.9)},
        'hours_per_batch': med(r['hours']),
        'rotor_ok': bool(r['rotor_ok']),
        'P_pass': {k: float(v.mean()) for k, v in r['pass'].items()},
    }


# ---------------------------------------------------------------------------------------
# Design search
# ---------------------------------------------------------------------------------------

ROUTES = {
    'grind → sinter': dict(finish='sinter'),
    'grind → melt': dict(finish='melt'),
    'grind → melt+flux': dict(finish='melt', _flux=True),
    'grind → melt+vac': dict(finish='melt', _vac=True),
    'grind → H2 → sinter': dict(finish='sinter', h2=True),
    'grind → H2 → melt': dict(finish='melt', h2=True),
    'grind → liquation → sinter': dict(finish='sinter', liquation=True),
    'grind → liquation → melt': dict(finish='melt', liquation=True),
    'grind → H2 → liquation → melt': dict(finish='melt', h2=True, liquation=True),
    'grind → carbonyl': dict(finish='carbonyl'),
}


def random_design(route: dict, rng: np.random.Generator) -> Design:
    lu = lambda lo, hi: float(np.exp(rng.uniform(np.log(lo), np.log(hi))))
    u = lambda lo, hi: float(rng.uniform(lo, hi))
    kw = {k: v for k, v in route.items() if not k.startswith('_')}
    d = Design(
        grind_um=lu(40, 1500), h2_T=u(750, 950), h2_hours=lu(2, 120),
        liq_T=u(1000, 1450), liq_G=lu(1, 3000), liq_pellet_um=0.0 if rng.random() < 0.6 else lu(800, 4000),
        melt_T=u(1520, 1680), melt_G=lu(0.01, 300), melt_minutes=lu(2, 120), melt_depth_m=lu(0.02, 0.3),
        flux_kg_per_kg=lu(0.01, 0.3) if route.get('_flux') else 0.0,
        vacuum_minutes=lu(10, 600) if route.get('_vac') else 0.0,
        enclosure=str(rng.choice(['lidded', 'pressurised'])),
        carb_P_bar=lu(20, 250), carb_T=u(120, 230), carb_hours=lu(12, 240), rotor_r_m=lu(0.2, 3.0),
        **kw,
    )
    return d


def search(route_name: str, ph: Physics, trials: int = 400, seed: int = 3, tier: str = 'envelope (S≤0.10, ≥97)') -> dict:
    """Best design for a route by P(pass tier), ties broken by lower energy."""
    rng = np.random.default_rng(seed)
    best, best_key = None, None
    for _ in range(trials):
        d = random_design(ROUTES[route_name], rng)
        s = summarise(d, ph)
        key = (round(s['P_pass'][tier], 3), -s['energy_kwh_per_kg']['P50'])
        if best_key is None or key > best_key:
            best, best_key = s, key
    best['route'] = route_name
    return best


def sensitivity(d: Design, ph: Physics, metric: str = 'S_pct') -> dict:
    """Spearman rank correlation of an output with each uncertain input."""
    from scipy.stats import spearmanr

    r = evaluate(d, ph)[metric]
    ok = np.isfinite(r)
    out = {}
    for k, v in {**ph.p, 'feed_metal': ph.metal, 'feed_fes': ph.fes}.items():
        if np.std(v[ok]) > 0 and np.std(r[ok]) > 0:
            out[k] = float(spearmanr(v[ok], r[ok]).statistic)
    return dict(sorted(out.items(), key=lambda kv: -abs(kv[1]))[:6])
