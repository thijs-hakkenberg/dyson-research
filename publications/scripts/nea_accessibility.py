"""
NEA joint accessibility for Phase 0 (rq-0-52): which catalogued near-Earth asteroids can a
rendezvous scout reach, and which support tug round trips to the SEL1 receiving node, in
2030–2040 windows?

Screening model, not a trajectory optimiser:
  - Two-body Kepler ephemerides from JPL SBDB elements (asteroids) and the Standish J2000
    mean elements (Earth–Moon barycentre). SEL1 is taken as Earth's heliocentric state
    scaled by 0.99 (1.5 million km sunward), close enough for Δv screening.
  - Impulsive zero-revolution Lambert transfers (universal variables, bisection) over a grid
    of departure dates and flight times. Departure is from C3 ≈ 0, so the EP stage supplies
    the whole Δv, as the bom-0-1 and bom-0-4 consensus assume.
  - Low-thrust Δv ≈ k × impulsive Δv (k = 1.15 reference, 1.0–1.4 sensitivity), and the
    burn must fit in the flight time at the vehicle's acceleration (thrust duty 0.85).
    Solar power is held at its 1 AU value; targets here stay within ~0.75–1.6 AU.

Thresholds come from the regenerated consensus (static/content/bom-specs/phase-0/*):
  scout: ≤3.5 km/s low-thrust to the primary target (bom-0-1)
  tug:   ≤5 km/s per leg (100–150 t iodine storage covers "a 5 km/s-per-leg envelope"),
         ≥60 days at the asteroid, round trip ≤3.0 years (bom-0-4 KDP-0B criterion)
  size:  H ≤ 22 (~100 m at albedo 0.25); rotation ≥4 h where known (bom-0-12 envelope)
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field

import numpy as np

GM = 2.959122082855911e-4  # AU^3 / day^2
KMS = 1731.45683681  # km/s per AU/day
J2000 = 2451545.0
G0 = 9.80665

# Metal-plausible taxonomy: S/Q complex (ordinary-chondrite analogues, 2–20 wt% Fe-Ni metal)
# and X complex (incl. E enstatite and M metal-rich candidates). C, B, D, T, V, L, K, O excluded.
METAL_PLAUSIBLE_PREFIXES = ('S', 'Q', 'X', 'M', 'E')


def jd(year: float) -> float:
    return J2000 + (year - 2000.0) * 365.25


# ---------------------------------------------------------------------------------------
# Ephemerides
# ---------------------------------------------------------------------------------------

def solve_kepler(M: np.ndarray, e: np.ndarray) -> np.ndarray:
    E = np.where(e < 0.8, M, np.pi * np.ones_like(M))
    for _ in range(30):
        E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    return E


def kepler_state(a, e, i, om, w, M0, epoch, t):
    """Heliocentric ecliptic J2000 position (AU) and velocity (AU/day).

    Element arrays broadcast against t; angles in degrees, epoch and t in JD.
    """
    a, e, i, om, w, M0, epoch, t = np.broadcast_arrays(*map(np.asarray, (a, e, i, om, w, M0, epoch, t)))
    i, om, w = np.radians(i), np.radians(om), np.radians(w)
    n = np.sqrt(GM / a**3)
    M = np.radians(M0) + n * (t - epoch)
    M = np.mod(M + np.pi, 2 * np.pi) - np.pi
    E = solve_kepler(M, e)
    cE, sE = np.cos(E), np.sin(E)
    b = a * np.sqrt(1 - e**2)
    x, y = a * (cE - e), b * sE
    r = a * (1 - e * cE)
    vx = -np.sqrt(GM * a) / r * sE
    vy = np.sqrt(GM * a) / r * np.sqrt(1 - e**2) * cE
    co, so, ci, si, cw, sw = np.cos(om), np.sin(om), np.cos(i), np.sin(i), np.cos(w), np.sin(w)
    R = np.stack(
        [
            np.stack([co * cw - so * sw * ci, -co * sw - so * cw * ci], -1),
            np.stack([so * cw + co * sw * ci, -so * sw + co * cw * ci], -1),
            np.stack([sw * si, cw * si], -1),
        ],
        -2,
    )  # (..., 3, 2)
    pos = (R @ np.stack([x, y], -1)[..., None])[..., 0]
    vel = (R @ np.stack([vx, vy], -1)[..., None])[..., 0]
    return pos, vel


def earth_elements(t):
    """Standish (1992) mean elements of the Earth–Moon barycentre, valid 1800–2050."""
    T = (np.asarray(t) - J2000) / 36525.0
    a = 1.00000261 + 0.00000562 * T
    e = 0.01671123 - 0.00004392 * T
    i = -0.00001531 - 0.01294668 * T
    L = 100.46457166 + 35999.37244981 * T
    varpi = 102.93768193 + 0.32327364 * T
    Om = 0.0 * T
    return a, e, i, Om, varpi - Om, L - varpi


def earth_state(t):
    a, e, i, Om, w, M = earth_elements(t)
    return kepler_state(a, e, i, Om, w, M, t, t)


def sel1_state(t):
    r, v = earth_state(t)
    return 0.99 * r, 0.99 * v


# ---------------------------------------------------------------------------------------
# Lambert (zero revolutions, prograde), vectorised
# ---------------------------------------------------------------------------------------

def _stumpff(z):
    C = np.empty_like(z)
    S = np.empty_like(z)
    p, n, s = z > 1e-6, z < -1e-6, np.abs(z) <= 1e-6
    sp = np.sqrt(z[p])
    C[p] = (1 - np.cos(sp)) / z[p]
    S[p] = (sp - np.sin(sp)) / sp**3
    sn = np.sqrt(-z[n])
    C[n] = (np.cosh(sn) - 1) / (-z[n])
    S[n] = (np.sinh(sn) - sn) / sn**3
    C[s] = 0.5 - z[s] / 24
    S[s] = 1 / 6 - z[s] / 120
    return C, S


def lambert(r1, r2, tof, iters: int = 70):
    """Velocities (v1, v2) for a prograde zero-revolution transfer; NaN where it fails."""
    r1, r2 = np.broadcast_arrays(r1, r2)
    tof = np.broadcast_to(tof, r1.shape[:-1]).astype(float)
    n1, n2 = np.linalg.norm(r1, axis=-1), np.linalg.norm(r2, axis=-1)
    cross_z = r1[..., 0] * r2[..., 1] - r1[..., 1] * r2[..., 0]
    cosd = np.clip(np.sum(r1 * r2, -1) / (n1 * n2), -1, 1)
    dth = np.arccos(cosd)
    dth = np.where(cross_z < 0, 2 * np.pi - dth, dth)
    A = np.sin(dth) * np.sqrt(n1 * n2 / (1 - cosd))
    lo = np.full(tof.shape, -40.0)
    hi = np.full(tof.shape, 4 * np.pi**2 - 1e-6)
    sq = np.sqrt(GM)
    for _ in range(iters):
        z = 0.5 * (lo + hi)
        C, S = _stumpff(z)
        y = n1 + n2 + A * (z * S - 1) / np.sqrt(C)
        ok = y > 0
        ys = np.where(ok, y, 1.0)
        t = ((ys / C) ** 1.5 * S + A * np.sqrt(ys)) / sq
        too_short = ~ok | (t < tof)
        lo = np.where(too_short, z, lo)
        hi = np.where(too_short, hi, z)
    z = 0.5 * (lo + hi)
    C, S = _stumpff(z)
    y = n1 + n2 + A * (z * S - 1) / np.sqrt(C)
    f = 1 - y / n1
    g = A * np.sqrt(np.maximum(y, 0) / GM)
    gdot = 1 - y / n2
    bad = (y <= 0) | (np.abs(g) < 1e-12) | (np.abs(A) < 1e-9)
    g = np.where(bad, np.nan, g)
    v1 = (r2 - f[..., None] * r1) / g[..., None]
    v2 = (gdot[..., None] * r2 - r1) / g[..., None]
    return v1, v2


# ---------------------------------------------------------------------------------------
# Vehicles and the screen
# ---------------------------------------------------------------------------------------

@dataclass(frozen=True)
class Vehicle:
    name: str
    power_w: float
    efficiency: float
    isp_s: float
    mass_kg: float

    @property
    def accel(self) -> float:  # m/s^2
        return 2 * self.efficiency * self.power_w / (G0 * self.isp_s) / self.mass_kg


# bom-0-1: 500–550 kg wet, ~2–2.5 kW to EP, Isp 1,700–2,200 s
SCOUT = Vehicle('scout', 2.2e3, 0.5, 1900, 525)
# bom-0-4: ~1.2–2.0 MWe to the PPUs, ~2,500 s; 45–70 t dry. Outbound with ~100 t iodine
# and some site cargo; inbound with a 150–300 t product pallet.
TUG_OUT = Vehicle('tug outbound', 1.5e6, 0.6, 2500, 175e3)
TUG_IN = Vehicle('tug inbound', 1.5e6, 0.6, 2500, 330e3)


@dataclass
class Criteria:
    k_lowthrust: float = 1.15
    scout_dv: float = 3.5  # km/s
    tug_leg_dv: float = 5.0  # km/s
    min_stay_days: float = 60
    max_cycle_years: float = 3.0
    duty: float = 0.85
    first_year: float = 2030.0
    last_year: float = 2040.0
    dep_step_days: float = 20.0
    tofs_days: tuple = (60, 90, 120, 150, 180, 220, 260, 300, 350, 400, 460, 520, 600, 700, 800, 950)


def burn_fits(dv_kms, tof_days, vehicle: Vehicle, duty: float):
    return dv_kms * 1e3 / vehicle.accel <= duty * tof_days * 86400


def leg_table(el: dict, t_dep: np.ndarray, tofs: np.ndarray, outbound: bool):
    """Impulsive departure and arrival Δv (km/s) for every (asteroid, departure, tof).

    Returns (dep, arr), each shape (N, D, T); inf where the transfer fails.
    """
    N, D, T = len(el['a']), len(t_dep), len(tofs)
    td = np.broadcast_to(t_dep[None, :, None], (N, D, T))
    ta = td + tofs[None, None, :]
    ae = {k: np.asarray(el[k])[:, None, None] for k in ('a', 'e', 'i', 'om', 'w', 'ma', 'epoch')}
    if outbound:
        r1, vs1 = sel1_state(td)
        r2, vs2 = kepler_state(ae['a'], ae['e'], ae['i'], ae['om'], ae['w'], ae['ma'], ae['epoch'], ta)
    else:
        r1, vs1 = kepler_state(ae['a'], ae['e'], ae['i'], ae['om'], ae['w'], ae['ma'], ae['epoch'], td)
        r2, vs2 = sel1_state(ta)
    v1, v2 = lambert(r1, r2, np.broadcast_to(tofs[None, None, :], (N, D, T)))
    dep = np.linalg.norm(v1 - vs1, axis=-1) * KMS
    arr = np.linalg.norm(vs2 - v2, axis=-1) * KMS
    bad = ~(np.isfinite(dep) & np.isfinite(arr))
    return np.where(bad, np.inf, dep), np.where(bad, np.inf, arr)


@dataclass
class Result:
    """Per asteroid. Scout Δv is keyed by launch v∞ (km/s); cycles by tug leg cap (km/s)."""

    scout_dv: dict
    cycle_years: dict
    cycle_detail: dict = field(default_factory=dict)


def best_cycle(out_ok, ret_ok, t_dep, t_ret, tofs, min_stay):
    """Shortest SEL1 → NEA → SEL1 cycle (days) for one asteroid, with its indices."""
    ret_arrival = np.where(ret_ok, t_ret[:, None] + tofs[None, :], np.inf)  # (R, T)
    ret_best = ret_arrival.min(axis=1)
    ret_bt = ret_arrival.argmin(axis=1)
    # suffix minimum over return departures: any later departure also works
    suf = ret_best.copy()
    sufi = np.arange(len(t_ret))
    for q in range(len(t_ret) - 2, -1, -1):
        if suf[q + 1] < suf[q]:
            suf[q], sufi[q] = suf[q + 1], sufi[q + 1]
    od, ot = np.nonzero(out_ok)
    if od.size == 0:
        return np.inf, None
    arrive = t_dep[od] + tofs[ot]
    k0 = np.searchsorted(t_ret, arrive + min_stay)
    valid = k0 < len(t_ret)
    if not valid.any():
        return np.inf, None
    home = np.where(valid, suf[np.minimum(k0, len(t_ret) - 1)], np.inf)
    cyc = home - t_dep[od]
    m = int(np.argmin(cyc))
    if not np.isfinite(cyc[m]):
        return np.inf, None
    q = sufi[k0[m]]
    return cyc[m], (od[m], ot[m], q, ret_bt[q])


def screen(el: dict, c: Criteria = Criteria(), chunk: int = 150,
           launch_vinf=(0.0, 1.5, 3.16), leg_caps=(5.0, 5.5, 6.0, 7.0)) -> Result:
    """Low-thrust Δv to reach each asteroid and the shortest tug cycle under each leg cap.

    Scout: departure Δv beyond the launch v∞ plus arrival Δv, × k, must fit its burn time.
    Tug: SEL1 → NEA → SEL1, both legs ≤ cap (× k applied), each burn fitting its flight time,
    stay ≥ min_stay; cycles start in [first_year, last_year), returns may depart up to
    max cycle (7 years) later.
    """
    t_dep = np.arange(jd(c.first_year), jd(c.last_year), c.dep_step_days)
    t_ret = np.arange(jd(c.first_year), jd(c.last_year + 7.0), c.dep_step_days)
    tofs = np.asarray(c.tofs_days, float)
    N = len(el['a'])
    scout = {v: np.full(N, np.inf) for v in launch_vinf}
    cycles = {L: np.full(N, np.inf) for L in leg_caps}
    detail = {L: [None] * N for L in leg_caps}
    tf = tofs[None, None, :]
    for s in range(0, N, chunk):
        sub = {k: np.asarray(v)[s : s + chunk] for k, v in el.items()}
        od_, oa_ = leg_table(sub, t_dep, tofs, True)
        rd_, ra_ = leg_table(sub, t_ret, tofs, False)
        for v in launch_vinf:
            dv = (np.maximum(od_ - v, 0) + oa_) * c.k_lowthrust
            dv = np.where(burn_fits(dv, tf, SCOUT, c.duty), dv, np.inf)
            scout[v][s : s + chunk] = dv.min(axis=(1, 2))
        out = (od_ + oa_) * c.k_lowthrust
        ret = (rd_ + ra_) * c.k_lowthrust
        out_fit = burn_fits(out, tf, TUG_OUT, c.duty)
        ret_fit = burn_fits(ret, tf, TUG_IN, c.duty)
        for L in leg_caps:
            for j in range(out.shape[0]):
                cyc, idx = best_cycle((out[j] <= L) & out_fit[j], (ret[j] <= L) & ret_fit[j], t_dep, t_ret, tofs, c.min_stay_days)
                cycles[L][s + j] = cyc / 365.25
                if idx:
                    o_d, o_t, q, q_t = idx
                    detail[L][s + j] = {
                        'departs': round(2000 + (t_dep[o_d] - J2000) / 365.25, 2),
                        'out_dv': round(float(out[j, o_d, o_t]), 3),
                        'out_tof_d': float(tofs[o_t]),
                        'in_dv': round(float(ret[j, q, q_t]), 3),
                        'in_tof_d': float(tofs[q_t]),
                    }
    return Result(scout, cycles, detail)


# ---------------------------------------------------------------------------------------
# Catalogue
# ---------------------------------------------------------------------------------------

def _f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return np.nan


def load_catalogue(path: str) -> list[dict]:
    d = json.load(open(path))
    rows = []
    for r in d['data']:
        row = dict(zip(d['fields'], r))
        for k in ('epoch', 'e', 'a', 'q', 'i', 'om', 'w', 'ma', 'H', 'diameter', 'albedo', 'rot_per'):
            row[k] = _f(row[k])
        row['taxonomy'] = (row.get('spec_B') or row.get('spec_T') or '').strip()
        rows.append(row)
    return rows


def metal_plausible(tax: str) -> bool | None:
    """True/False from taxonomy; None when unclassified."""
    if not tax:
        return None
    return tax.upper().startswith(METAL_PLAUSIBLE_PREFIXES)


def prefilter(rows: list[dict], h_max: float = 22.0) -> list[dict]:
    """Orbits that could possibly close at ≤5 km/s per leg (plane change alone at i = 12° is ~6 km/s)."""
    return [
        r
        for r in rows
        if r['i'] <= 12 and r['e'] <= 0.45 and 0.6 <= r['a'] <= 1.8 and np.isfinite(r['H']) and r['H'] <= h_max
    ]


def elements(rows: list[dict]) -> dict:
    return {k: np.array([r[k] for r in rows]) for k in ('a', 'e', 'i', 'om', 'w', 'ma', 'epoch')}
