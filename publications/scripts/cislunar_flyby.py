"""
rq-0-52: three-body model of a tug leaving (or returning to) a Sun–Earth L1 node by way of
lunar swingbys.

The heliocentric study (trajectory_opt.py) credits a leg with a free Earth-relative excess
speed at its Earth end. This module computes what that credit really is: for a vehicle that
leaves a periodic orbit about SEL1 along its unstable manifold, meets the Moon once or
twice, and escapes, it gives the excess speed reached as a function of direction and of
the time taken.

Model
  * Sun–Earth circular restricted three-body problem, normalised units (AU, year/2π).
  * The Moon is on a circular, ecliptic orbit about the Earth. Its gravity acts only at an
    encounter, where it turns the Moon-relative excess velocity by up to the angle a
    100 km-altitude pass allows (patched swingby, as in Chen et al. 2016). A separate
    integration with the Moon's gravity switched on checks this (`moon=` in `integrate`).
  * Node orbits: planar Lyapunov orbits about SEL1, left with an impulsive in-plane burn
    (50–300 m/s). Without a burn the coast to the Moon takes four months.
  * Sequences: manifold → swingby → escape, and manifold → swingby → Sun-perturbed
    Moon-to-Moon transfer (planar) → swingby → escape.

Capture is the mirror image: the equations are unchanged under (x, y, z, t) → (x, −y, z, −t),
so an escape with excess velocity (vx, vy, vz) corresponds to an arrival with (−vx, vy, −vz)
that ends on the node orbit's stable manifold after the same time.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.integrate import RK45, solve_ivp
from scipy.optimize import brentq

MU_SUN = 1.32712440018e11  # km³/s²
MU_EARTH = 398600.4418
MU_MOON = 4902.800
AU_KM = 149597870.7
MU = MU_EARTH / (MU_SUN + MU_EARTH)
TU_DAYS = 365.25636 / (2 * np.pi)
VU_KMS = AU_KM / (TU_DAYS * 86400.0)
A_MOON = 384400.0 / AU_KM
N_MOON = 365.25636 / 27.321661  # sidereal mean motion, normalised
V_MOON = N_MOON * A_MOON  # Earth-relative, non-rotating axes
MUM = MU_MOON / (MU_SUN + MU_EARTH)
R_PERILUNE = 1838.0 / AU_KM  # 100 km altitude
R_PERIGEE = 6600.0 / AU_KM  # about 220 km altitude
R_ESCAPE = 1.5e6 / AU_KM
EARTH = np.array([1.0 - MU, 0.0, 0.0])


def rhs(y, moon_theta=None):
    """Rotating-frame equations of motion, batched over rows of y (N, 6)."""
    x, yy, z, vx, vy, vz = y.T
    d1 = ((x + MU) ** 2 + yy**2 + z**2) ** 1.5
    dx2 = x - 1.0 + MU
    d2 = (dx2**2 + yy**2 + z**2) ** 1.5
    ax = 2 * vy + x - (1 - MU) * (x + MU) / d1 - MU * dx2 / d2
    ay = -2 * vx + yy - (1 - MU) * yy / d1 - MU * yy / d2
    az = -(1 - MU) * z / d1 - MU * z / d2
    if moon_theta is not None:
        mx = dx2 - A_MOON * np.cos(moon_theta)
        my = yy - A_MOON * np.sin(moon_theta)
        d3 = (mx**2 + my**2 + z**2) ** 1.5
        ax = ax - MUM * mx / d3
        ay = ay - MUM * my / d3
        az = az - MUM * z / d3
    return np.stack([vx, vy, vz, ax, ay, az], axis=1)


def _hermite(y0, y1, f0, f1, h, s):
    s = s[:, None]
    h = h[:, None]
    return ((2 * s**3 - 3 * s**2 + 1) * y0 + (s**3 - 2 * s**2 + s) * h * f0
            + (-2 * s**3 + 3 * s**2) * y1 + (s**3 - s**2) * h * f1)


def _radius(y):
    return np.sqrt((y[:, 0] - EARTH[0]) ** 2 + y[:, 1] ** 2 + y[:, 2] ** 2)


def _root(y0, y1, f0, f1, h, level):
    """Fraction of the step at which the Earth distance equals `level` (one crossing assumed)."""
    lo = np.zeros(len(y0))
    hi = np.ones(len(y0))
    rising = _radius(y1) > _radius(y0)
    for _ in range(36):
        mid = 0.5 * (lo + hi)
        above = _radius(_hermite(y0, y1, f0, f1, h, mid)) > level
        go_hi = above == rising
        hi = np.where(go_hi, mid, hi)
        lo = np.where(go_hi, lo, mid)
    s = 0.5 * (lo + hi)
    return s, _hermite(y0, y1, f0, f1, h, s)


@dataclass
class Flight:
    status: np.ndarray  # 0 ran out of time, 1 escaped (state at R_ESCAPE), 2 hit the Earth, 3 hit the Moon
    t: np.ndarray  # final time
    y: np.ndarray  # final state
    n_cross: np.ndarray  # number of crossings of the Moon's orbital distance recorded
    t_cross: np.ndarray  # (N, K)
    y_cross: np.ndarray  # (N, K, 6)
    moon_min: np.ndarray  # closest approach to the Moon (only with moon=)


def integrate(y0, t0, t_end, crossings: int = 0, moon=None, tol: float = 1e-9, h_max: float = 0.5 / TU_DAYS,
              stop_at_escape: bool = True) -> Flight:
    """Dormand–Prince 5(4) with a step per row. `moon` is the Moon's rotating-frame angle at
    t = 0 for each row; when given, its gravity is included."""
    A, B, C, E = RK45.A, RK45.B, RK45.C, RK45.E
    y = np.array(y0, float)
    N = len(y)
    t = np.broadcast_to(np.asarray(t0, float), (N,)).copy()
    t_end = np.broadcast_to(np.asarray(t_end, float), (N,)).copy()
    h = np.full(N, 1e-4)
    status = np.full(N, -1)
    n_cross = np.zeros(N, int)
    t_cross = np.full((N, max(crossings, 1)), np.nan)
    y_cross = np.full((N, max(crossings, 1), 6), np.nan)
    moon_min = np.full(N, np.inf)
    moon0 = None if moon is None else np.broadcast_to(np.asarray(moon, float), (N,))
    rate = N_MOON - 1.0

    def f(idx, tt, yy):
        return rhs(yy, None if moon0 is None else moon0[idx] + rate * tt)

    act = np.arange(N)
    k1 = f(act, t, y)
    for _ in range(400000):
        if act.size == 0:
            break
        ya, ta = y[act], t[act]
        ha = np.minimum(np.minimum(h[act], h_max), t_end[act] - ta)
        K = [k1]
        for s in range(1, 6):
            K.append(f(act, ta + C[s] * ha, ya + ha[:, None] * sum(A[s, j] * K[j] for j in range(s))))
        yn = ya + ha[:, None] * sum(B[j] * K[j] for j in range(6))
        K.append(f(act, ta + ha, yn))
        err = np.sqrt(np.mean((ha[:, None] * sum(E[j] * K[j] for j in range(7)) / tol) ** 2, axis=1))
        ok = err <= 1.0
        fac = np.where(err > 0, 0.9 * np.maximum(err, 1e-10) ** -0.2, 5.0)
        h[act] = ha * np.clip(fac, 0.2, 5.0)
        k_next = np.where(ok[:, None], K[6], k1)
        if ok.any():
            a = act[ok]
            y0s, y1s, f0s, f1s, hs = ya[ok], yn[ok], k1[ok], K[6][ok], ha[ok]
            r0, r1 = _radius(y0s), _radius(y1s)
            if crossings:
                hit = ((r0 - A_MOON) * (r1 - A_MOON) < 0) & (n_cross[a] < crossings)
                if hit.any():
                    s, yc = _root(y0s[hit], y1s[hit], f0s[hit], f1s[hit], hs[hit], A_MOON)
                    rows = a[hit]
                    t_cross[rows, n_cross[rows]] = ta[ok][hit] + s * hs[hit]
                    y_cross[rows, n_cross[rows]] = yc
                    n_cross[rows] += 1
            y[a] = y1s
            t[a] = ta[ok] + hs
            if moon0 is not None:
                th = moon0[a] + rate * t[a]
                dm = np.sqrt((y1s[:, 0] - EARTH[0] - A_MOON * np.cos(th)) ** 2 + (y1s[:, 1] - A_MOON * np.sin(th)) ** 2 + y1s[:, 2] ** 2)
                moon_min[a] = np.minimum(moon_min[a], dm)
                status[a[dm < R_PERILUNE]] = 3
            esc = (r1 >= R_ESCAPE) & (r0 < R_ESCAPE) & (status[a] < 0)
            if esc.any() and stop_at_escape:
                s, ye = _root(y0s[esc], y1s[esc], f0s[esc], f1s[esc], hs[esc], R_ESCAPE)
                rows = a[esc]
                y[rows] = ye
                t[rows] = ta[ok][esc] + s * hs[esc]
                status[rows] = 1
            status[a[(r1 < R_PERIGEE) & (status[a] < 0)]] = 2
            done = (t[a] >= t_end[a] - 1e-12) & (status[a] < 0)
            status[a[done]] = 0
        keep = status[act] < 0
        act = act[keep]
        k1 = k_next[keep]
    status[status < 0] = 0
    return Flight(status, t, y, n_cross, t_cross, y_cross, moon_min)


# ---------------------------------------------------------------------------------------
# Node orbits and their unstable manifolds
# ---------------------------------------------------------------------------------------

def l1_x() -> float:
    g = lambda x: x - (1 - MU) / (x + MU) ** 2 + MU / (x - 1 + MU) ** 2
    return brentq(g, 1 - MU - 0.02, 1 - MU - 0.005)


def _f1(t, s):
    return rhs(np.asarray(s)[None, :])[0]


def _half_period(x0, vy0):
    ev = lambda t, s: s[1]
    ev.terminal, ev.direction = True, -1
    sol = solve_ivp(_f1, (0, 6), [x0, 0, 0, 0, vy0, 0], method='DOP853', rtol=1e-12, atol=1e-13, events=ev)
    if not len(sol.t_events[0]):
        return np.nan, np.array([np.nan, 0, 0, -1.0, 0, 0])  # fell sunward without returning: too slow
    return sol.t_events[0][0], sol.y_events[0][0]


def lyapunov_orbit(ax_km: float):
    """Planar Lyapunov orbit about SEL1 whose Sun-side crossing is ax_km from the point.
    Returns (state at that crossing, period)."""
    xl = l1_x()
    c2 = MU / abs(xl - 1 + MU) ** 3 + (1 - MU) / abs(xl + MU) ** 3
    lam = np.sqrt((2 - c2 + np.sqrt(9 * c2**2 - 8 * c2)) / 2)
    kappa = (lam**2 + 1 + 2 * c2) / (2 * lam)
    a = ax_km / AU_KM
    x0, guess = xl - a, kappa * lam * a
    g = lambda vy: _half_period(x0, vy)[1][3]
    lo = 0.97 * guess
    for _ in range(60):
        hi = lo + 0.004 * guess
        if g(lo) < 0 <= g(hi):
            break
        lo = hi
    vy = brentq(g, lo, hi, xtol=1e-15)
    return np.array([x0, 0, 0, 0, vy, 0]), 2 * _half_period(x0, vy)[0]


def unstable_direction(state, period):
    """Unstable eigenvector of the planar monodromy matrix (finite differences) and its multiplier."""
    idx = [0, 1, 3, 4]
    eps = 1e-8

    def flow(s):
        return solve_ivp(_f1, (0, period), s, method='DOP853', rtol=1e-12, atol=1e-13).y[:, -1]

    M = np.zeros((4, 4))
    for j, k in enumerate(idx):
        d = np.zeros(6)
        d[k] = eps
        M[:, j] = (flow(state + d) - flow(state - d))[idx] / (2 * eps)
    w, v = np.linalg.eig(M)
    k = np.argmax(np.abs(w))
    vec = np.zeros(6)
    vec[idx] = np.real(v[:, k]) / np.linalg.norm(np.real(v[:, k]))
    return vec, float(np.real(w[k]))


def node_departures(ax_km: float, n_phase: int = 16, n_angle: int = 24, dv_ms: float = 150.0):
    """States just after an in-plane departure burn of dv_ms, at n_phase points evenly spaced
    in time round a node orbit and n_angle burn directions. The leg clock starts here.
    Returns (states (n_phase * n_angle, 6), orbit period in days)."""
    x0, period = lyapunov_orbit(ax_km)
    times = np.arange(n_phase) * period / n_phase
    base = solve_ivp(_f1, (0, period), x0, method='DOP853', rtol=1e-12, atol=1e-13, t_eval=times).y.T
    ang = np.arange(n_angle) * 2 * np.pi / n_angle
    y = np.repeat(base, n_angle, axis=0)
    a = np.tile(ang, n_phase)
    dv = dv_ms / 1e3 / VU_KMS
    y[:, 3] += dv * np.cos(a)
    y[:, 4] += dv * np.sin(a)
    return y, period * TU_DAYS


# ---------------------------------------------------------------------------------------
# Swingbys
# ---------------------------------------------------------------------------------------

def encounter_vinf(yc):
    """Moon-relative excess velocity (non-rotating axes, expressed in the rotating frame's
    axes at that instant) for states at the Moon's orbital distance, with the Moon taken to
    be at the same place. Returns (v_inf (N, 3), Moon velocity (N, 3), angle of the place)."""
    rho = yc[:, :3] - EARTH
    th = np.arctan2(rho[:, 1], rho[:, 0])
    vi = yc[:, 3:] + np.stack([-rho[:, 1], rho[:, 0], np.zeros(len(yc))], axis=1)
    vm = V_MOON * np.stack([-np.sin(th), np.cos(th), np.zeros(len(yc))], axis=1)
    return vi - vm, vm, th


def max_turn(vinf_norm):
    """Largest turn of the excess velocity at the lowest allowed pass."""
    return 2 * np.arcsin(1.0 / (1.0 + R_PERILUNE * vinf_norm**2 / MUM))


def turn(vinf, delta, roll):
    """Rotate each excess velocity by `delta` away from its direction, towards the azimuth
    `roll` measured about it from the ecliptic-plane perpendicular. roll = 0 or π stays in plane."""
    n = np.linalg.norm(vinf, axis=1, keepdims=True)
    u = vinf / n
    z = np.array([0.0, 0.0, 1.0])
    p = np.cross(z, u)
    p /= np.linalg.norm(p, axis=1, keepdims=True)  # in-plane perpendicular
    q = np.cross(u, p)  # completes the triad (out of plane for planar u)
    d = np.asarray(delta)[:, None]
    r = np.asarray(roll)[:, None]
    return n * (np.cos(d) * u + np.sin(d) * (np.cos(r) * p + np.sin(r) * q))


def after_swingby(yc, vout, vm):
    """Rotating-frame state leaving an encounter with Moon-relative excess velocity vout."""
    rho = yc[:, :3] - EARTH
    vi = vm + vout
    y = yc.copy()
    y[:, 3:] = vi - np.stack([-rho[:, 1], rho[:, 0], np.zeros(len(yc))], axis=1)
    return y


def escape_state(y):
    """Earth-relative excess speed (km/s), longitude from the Sun→Earth line and latitude
    from the ecliptic (degrees) of the velocity, for states at R_ESCAPE."""
    rho = y[:, :3] - EARTH
    vi = y[:, 3:] + np.stack([-rho[:, 1], rho[:, 0], np.zeros(len(y))], axis=1)
    v2 = (vi**2).sum(axis=1)
    c3 = (v2 - 2 * MU / np.linalg.norm(rho, axis=1)) * VU_KMS**2
    lon = np.degrees(np.arctan2(vi[:, 1], vi[:, 0]))
    lat = np.degrees(np.arcsin(vi[:, 2] / np.sqrt(v2)))
    return np.sqrt(np.maximum(c3, 0.0)), lon, lat, c3


# ---------------------------------------------------------------------------------------
# Sequences
# ---------------------------------------------------------------------------------------

DAY = 1.0 / TU_DAYS


def swingby_fan(yc, n_delta: int = 10, n_roll: int = 13):
    """All outgoing states of a swingby on a grid of turn angles and azimuths (upper half
    only; the lower half is its mirror image in the ecliptic). Returns (states, index of the
    encounter each came from)."""
    vinf, vm, _ = encounter_vinf(yc)
    dmax = max_turn(np.linalg.norm(vinf, axis=1))
    M = len(yc)
    frac = np.concatenate([[0.0], np.repeat(np.arange(1, n_delta + 1) / n_delta, n_roll)])
    roll = np.concatenate([[0.0], np.tile(np.linspace(0, np.pi, n_roll), n_delta)])
    idx = np.repeat(np.arange(M), len(frac))
    delta = np.tile(frac, M) * dmax[idx]
    vout = turn(vinf[idx], delta, np.tile(roll, M))
    return after_swingby(yc[idx], vout, vm[idx]), idx


def _wrap(a):
    return (a + np.pi) % (2 * np.pi) - np.pi


def _planar_states(yc, delta):
    vinf, vm, _ = encounter_vinf(yc)
    return after_swingby(yc, turn(vinf, np.abs(delta), np.where(delta >= 0, 0.0, np.pi)), vm)


def moon_to_moon(yc, tc, t_limit, n_delta: int = 241, k: int = 8):
    """Planar Sun-perturbed transfers from each encounter back to the Moon.

    The first swingby turns the excess velocity in the ecliptic by δ; the vehicle then coasts
    under Sun and Earth. A solution is a δ for which the vehicle is back at the Moon's
    orbital distance at the place the Moon has reached. Returns (index of the first
    encounter, δ, state at the second encounter, time of the second encounter)."""
    vinf, vm, th1 = encounter_vinf(yc)
    dmax = max_turn(np.linalg.norm(vinf, axis=1))
    M = len(yc)
    grid = np.linspace(-1, 1, n_delta)
    idx = np.repeat(np.arange(M), n_delta)
    delta = np.tile(grid, M) * dmax[idx]

    def fly(ix, dl, t_stop):
        f = integrate(_planar_states(yc[ix], dl), tc[ix], t_stop, crossings=k)
        th = np.arctan2(f.y_cross[:, :, 1], f.y_cross[:, :, 0] - EARTH[0])
        moon = th1[ix][:, None] + (N_MOON - 1.0) * (f.t_cross - tc[ix][:, None])
        radial = ((f.y_cross[:, :, 0] - EARTH[0]) * f.y_cross[:, :, 3] + f.y_cross[:, :, 1] * f.y_cross[:, :, 4])
        return f, _wrap(th - moon), np.sign(radial)

    f, mis, rad = fly(idx, delta, t_limit[idx])
    ok = np.isfinite(mis) & (f.t_cross - tc[idx][:, None] > 3 * DAY)
    a = np.arange(len(idx) - 1)
    same = idx[a] == idx[a + 1]
    cands = []
    for j in range(k):
        for jj in (j - 1, j, j + 1):  # the crossing count can shift by one between neighbours
            if jj < 0 or jj >= k:
                continue
            good = (same & ok[a, j] & ok[a + 1, jj] & (rad[a, j] == rad[a + 1, jj]) & (mis[a, j] * mis[a + 1, jj] < 0)
                    & (np.abs(mis[a, j]) < 1.0) & (np.abs(mis[a + 1, jj]) < 1.0)
                    & (np.abs(f.t_cross[a, j] - f.t_cross[a + 1, jj]) < 2 * DAY))
            for r in np.nonzero(good)[0]:
                cands.append((idx[r], delta[r], delta[r + 1], mis[r, j], 0.5 * (f.t_cross[r, j] + f.t_cross[r + 1, jj]), rad[r, j]))
    if not cands:
        return np.zeros(0, int), np.zeros(0), np.zeros((0, 6)), np.zeros(0)
    ce, lo, hi, mlo, tt, rr = (np.array(c) for c in zip(*cands))
    ce = ce.astype(int)
    alive = np.ones(len(ce), bool)
    yb = np.zeros((len(ce), 6))
    tb = np.zeros(len(ce))
    mb = np.full(len(ce), np.inf)
    for _ in range(16):
        mid = 0.5 * (lo + hi)
        f, mis, rad = fly(ce, mid, tt + 6 * DAY)
        dt = np.where(np.isfinite(f.t_cross) & (rad == rr[:, None]), np.abs(f.t_cross - tt[:, None]), np.inf)
        j = np.argmin(dt, axis=1)
        rows = np.arange(len(ce))
        found = dt[rows, j] < 3 * DAY
        alive &= found
        m = np.where(found, mis[rows, j], 0.0)
        better = found & (np.abs(m) < np.abs(mb))
        yb[better], tb[better], mb[better] = f.y_cross[rows, j][better], f.t_cross[rows, j][better], m[better]
        tt = np.where(found, f.t_cross[rows, j], tt)
        left = m * mlo > 0
        lo, mlo = np.where(left, mid, lo), np.where(left, m, mlo)
        hi = np.where(left, hi, mid)
    keep = alive & (np.abs(mb) < 1e-3)
    return ce[keep], 0.5 * (lo + hi)[keep], yb[keep], tb[keep]
