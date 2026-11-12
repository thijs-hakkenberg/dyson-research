"""
Second-pass trajectory model for rq-0-52: multi-revolution transfers, lunar gravity assists
at the Earth end, and optimised low-thrust legs.

The first screen (nea_accessibility.py) used zero-revolution impulsive transfers × 1.15 and
no flybys. This module adds what that left out:

    lambert_multirev   transfers with N complete revolutions (both branches), vectorised
    propagate          two-body propagation (elliptic), vectorised
    low_thrust_leg     Sims–Flanagan transcription: the leg is cut into segments, each with
                       one impulse no larger than the thruster can deliver in that segment;
                       the total Δv is minimised subject to the two halves meeting
    lunar assist       modelled as a free Earth-relative excess speed (v∞) of up to
                       `lga_vinf` at the Earth end of a leg, direction free

Screening grade, not flight design. Limits: two-body dynamics about the Sun; 20 segments per
leg; thrust acceleration fixed at the leg's starting mass (conservative); the lunar assist
is an energy credit with no geometry (the Moon's 5° inclination to the ecliptic and the
phasing wait are represented only by a fixed time penalty); Earth resonant flybys with
v∞ leveraging are not modelled.

Units: AU, days, AU/day; Δv reported in km/s.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from nea_accessibility import GM, KMS, _stumpff, earth_state, kepler_state, sel1_state

AU_M = 1.495978707e11
ACC = 86400.0**2 / AU_M  # (AU/day²) per (m/s²)
V_SCALE = 0.0172  # AU/day, ~Earth's orbital speed; scales velocity mismatches
TRACE = False


# ---------------------------------------------------------------------------------------
# Lambert with N revolutions
# ---------------------------------------------------------------------------------------

def _tof_z(z, n1, n2, A):
    """Time of flight for universal variable z, and y; inf where the geometry is invalid."""
    C, S = _stumpff(z)
    y = n1 + n2 + A * (z * S - 1) / np.sqrt(C)
    ok = y > 0
    ys = np.where(ok, y, 1.0)
    t = ((ys / C) ** 1.5 * S + A * np.sqrt(ys)) / np.sqrt(GM)
    return np.where(ok, t, np.inf), y


def lambert_multirev(r1, r2, tof, nrev: int, branch: int, iters: int = 60):
    """Prograde transfer with `nrev` ≥ 1 complete revolutions. branch 0 = low-z (shorter
    period) side of the minimum-time solution, 1 = high-z side. NaN where tof is below the
    minimum for that revolution count."""
    r1, r2 = np.broadcast_arrays(np.asarray(r1, float), np.asarray(r2, float))
    tof = np.broadcast_to(tof, r1.shape[:-1]).astype(float)
    n1, n2 = np.linalg.norm(r1, axis=-1), np.linalg.norm(r2, axis=-1)
    cross_z = r1[..., 0] * r2[..., 1] - r1[..., 1] * r2[..., 0]
    cosd = np.clip(np.sum(r1 * r2, -1) / (n1 * n2), -1, 1)
    dth = np.arccos(cosd)
    dth = np.where(cross_z < 0, 2 * np.pi - dth, dth)
    A = np.sin(dth) * np.sqrt(n1 * n2 / (1 - cosd))
    zlo = (2 * np.pi * nrev) ** 2 + 1e-6
    zhi = (2 * np.pi * (nrev + 1)) ** 2 - 1e-6
    # minimum of t(z) on (zlo, zhi) by golden section (t is unimodal there)
    gr = 0.6180339887498949
    a = np.full(tof.shape, zlo)
    b = np.full(tof.shape, zhi)
    c = b - gr * (b - a)
    d = a + gr * (b - a)
    tc, _ = _tof_z(c, n1, n2, A)
    td, _ = _tof_z(d, n1, n2, A)
    for _ in range(45):
        left = tc < td
        b = np.where(left, d, b)
        a = np.where(left, a, c)
        c = b - gr * (b - a)
        d = a + gr * (b - a)
        tc, _ = _tof_z(c, n1, n2, A)
        td, _ = _tof_z(d, n1, n2, A)
    zmin = 0.5 * (a + b)
    tmin, _ = _tof_z(zmin, n1, n2, A)
    feasible = tof >= tmin
    if branch == 0:  # t decreases with z on (zlo, zmin)
        lo, hi = np.full(tof.shape, zlo), zmin.copy()
        for _ in range(iters):
            z = 0.5 * (lo + hi)
            t, _ = _tof_z(z, n1, n2, A)
            longer = t > tof
            lo = np.where(longer, z, lo)
            hi = np.where(longer, hi, z)
    else:  # t increases with z on (zmin, zhi)
        lo, hi = zmin.copy(), np.full(tof.shape, zhi)
        for _ in range(iters):
            z = 0.5 * (lo + hi)
            t, _ = _tof_z(z, n1, n2, A)
            longer = t > tof
            hi = np.where(longer, z, hi)
            lo = np.where(longer, lo, z)
    z = 0.5 * (lo + hi)
    t, y = _tof_z(z, n1, n2, A)
    f = 1 - y / n1
    g = A * np.sqrt(np.maximum(y, 0) / GM)
    gdot = 1 - y / n2
    bad = ~feasible | (y <= 0) | (np.abs(g) < 1e-12) | (np.abs(A) < 1e-9) | (np.abs(t - tof) > 1e-3 * tof)
    g = np.where(bad, np.nan, g)
    v1 = (r2 - f[..., None] * r1) / g[..., None]
    v2 = (gdot[..., None] * r2 - r1) / g[..., None]
    return v1, v2


# ---------------------------------------------------------------------------------------
# Two-body propagation (elliptic orbits)
# ---------------------------------------------------------------------------------------

def propagate(r, v, dt):
    """State after dt (may be negative). r, v shape (..., 3); dt broadcastable to (...)."""
    r0 = np.linalg.norm(r, axis=-1)
    v2 = np.sum(v * v, -1)
    inv_a = 2.0 / r0 - v2 / GM
    a = 1.0 / np.where(inv_a > 1e-3, inv_a, np.nan)  # unbound or near-parabolic: NaN
    n = np.sqrt(GM / a**3)
    sig = np.sum(r * v, -1) / np.sqrt(GM)
    sa = np.sqrt(a)
    M = n * dt
    E = M.copy() if isinstance(M, np.ndarray) else np.asarray(M, float)
    E = np.broadcast_to(E, r0.shape).copy()
    for _ in range(30):
        s, c = np.sin(E), np.cos(E)
        F = E - (1 - r0 / a) * s + sig / sa * (1 - c) - M
        dF = 1 - (1 - r0 / a) * c + sig / sa * s
        step = F / dF
        E = E - step
        if not np.nanmax(np.abs(step)) > 1e-13:
            break
    s, c = np.sin(E), np.cos(E)
    rn = a + (r0 - a) * c + sig * sa * s
    f = 1 - a / r0 * (1 - c)
    g = dt - (E - s) / n
    fd = -np.sqrt(GM * a) * s / (rn * r0)
    gd = 1 - a / rn * (1 - c)
    return f[..., None] * r + g[..., None] * v, fd[..., None] * r + gd[..., None] * v


# ---------------------------------------------------------------------------------------
# Low-thrust leg (Sims–Flanagan)
# ---------------------------------------------------------------------------------------

@dataclass
class LegResult:
    ok: bool
    dv_kms: float  # thruster Δv
    vinf_kms: float  # Earth-relative excess speed used at the Earth end (from the lunar assist)
    mismatch: float  # scaled position/velocity error where the two halves meet
    thrust_fraction: float  # share of the flight time spent thrusting


def _mismatch(X, r0, v0, rf, vf, tof, nseg, free_end):
    """Batched over rows of X. Returns (B, 6) scaled mismatch at the middle of the leg."""
    B = X.shape[0]
    dv = X[:, : 3 * nseg].reshape(B, nseg, 3)
    r = np.broadcast_to(r0, (B, 3)).copy()
    v = np.broadcast_to(v0, (B, 3)).copy()
    rb = np.broadcast_to(rf, (B, 3)).copy()
    vb = np.broadcast_to(vf, (B, 3)).copy()
    if free_end == 'start':
        v = v + X[:, 3 * nseg :]
    elif free_end == 'end':
        vb = vb + X[:, 3 * nseg :]
    h = tof / nseg
    half = nseg // 2
    hh = np.full(B, 0.5 * h)
    for k in range(half):
        r, v = propagate(r, v, hh)
        v = v + dv[:, k]
        r, v = propagate(r, v, hh)
    for k in range(nseg - 1, half - 1, -1):
        rb, vb = propagate(rb, vb, -hh)
        vb = vb - dv[:, k]
        rb, vb = propagate(rb, vb, -hh)
    out = np.concatenate([r - rb, (v - vb) / V_SCALE], axis=1)
    return np.where(np.isfinite(out), out, 10.0)


def _spread(total, cap, nseg, from_start: bool):
    """Split one impulse into consecutive capped segment impulses at one end of the leg."""
    out = np.zeros((nseg, 3))
    mag = np.linalg.norm(total)
    if mag == 0:
        return out
    u = total / mag
    order = range(nseg) if from_start else range(nseg - 1, -1, -1)
    left = mag
    for k in order:
        take = min(left, 0.98 * cap)
        out[k] = take * u
        left -= take
        if left <= 0:
            break
    return out


def low_thrust_leg(r0, v0, rf, vf, tof, accel_ms2, duty=0.85, nseg=20, seed=None,
                   free_end=None, lga_vinf_kms=0.0, iters=14) -> LegResult:
    """Minimum-Δv low-thrust transfer from (r0, v0) to (rf, vf) in `tof` days.

    Solved by sequential convex programming: the dynamics are linearised about the current
    trajectory and the fuel-optimal impulses found as a second-order cone program (Clarabel),
    inside a shrinking trust region.

    seed: (v1, v2) heliocentric velocities of an impulsive transfer between the same points.
    free_end: 'start' or 'end' marks the Earth end, where an excess velocity of up to
    `lga_vinf_kms` relative to (v0 or vf) is free.
    """
    import clarabel
    from scipy import sparse

    h = tof / nseg
    cap = accel_ms2 * ACC * duty * h * KMS  # km/s per segment
    nf = 3 if free_end else 0
    nx = 3 * nseg + nf
    vmax = lga_vinf_kms
    x = np.zeros(nx)  # km/s
    if seed is not None:
        d0, d1 = (seed[0] - v0) * KMS, (vf - seed[1]) * KMS
        if free_end == 'start':
            n0 = np.linalg.norm(d0)
            take = d0 * min(1.0, vmax / n0) if n0 > 0 else d0 * 0
            x[3 * nseg :] = take
            d0 = d0 - take
        elif free_end == 'end':
            n1 = np.linalg.norm(d1)
            take = d1 * min(1.0, vmax / n1) if n1 > 0 else d1 * 0
            x[3 * nseg :] = -take
            d1 = d1 - take
        if np.linalg.norm(d0) + np.linalg.norm(d1) > 0.98 * cap * nseg:
            return LegResult(False, np.inf, 0.0, np.inf, np.inf)
        x[: 3 * nseg] = (_spread(d0, cap, nseg, True) + _spread(d1, cap, nseg, False)).ravel()
        mags = np.linalg.norm(x[: 3 * nseg].reshape(nseg, 3), axis=1)
        over = mags > 0.98 * cap
        if over.any():
            x[: 3 * nseg] = (x[: 3 * nseg].reshape(nseg, 3) * np.where(over, 0.98 * cap / np.maximum(mags, 1e-12), 1.0)[:, None]).ravel()

    def mis(X):
        return _mismatch(X / KMS, r0, v0, rf, vf, tof, nseg, free_end)

    step = 1e-4  # km/s
    lam = 2e3
    # variable layout: d (3n) | w (nf) | t (n) | e (6) | tau (1)
    nt, ne = nseg, 6
    nz = nx + nt + ne + 1
    it0, ie0, itau = nx, nx + nt, nx + nt + ne
    q = np.zeros(nz)
    q[it0 : it0 + nt] = 1.0
    q[itau] = lam
    P = sparse.csc_matrix((nz, nz))
    settings = clarabel.DefaultSettings()
    settings.verbose = False
    settings.max_threads = 1
    settings.direct_solve_method = 'qdldl'
    delta = max(1.0, 2 * cap)
    best = None
    for it in range(iters):
        X = np.repeat(x[None, :], nx + 1, axis=0)
        X[1:] += step * np.eye(nx)
        m = mis(X)
        m0 = m[0]
        J = ((m[1:] - m0) / step).T  # (6, nx)
        err = float(np.max(np.abs(m0)))
        if TRACE:
            print(it, f"err {err:.2e} cost {np.linalg.norm(x[: 3 * nseg].reshape(nseg, 3), axis=1).sum():.4f} delta {delta:.3f}")
        dmag = np.linalg.norm(x[: 3 * nseg].reshape(nseg, 3), axis=1)
        if err < 2e-5 and np.all(dmag <= cap * 1.001):
            cost = float(dmag.sum())
            if best is None or cost < best[0] - 1e-4:
                improved = best is None or best[0] - cost > 2e-3
                best = (cost, x.copy(), err)
                if not improved and it > 2:
                    break
            elif it > 2:
                break
        if it >= 4 and best is None and err > 1e-3 and dmag.sum() > 0.97 * cap * nseg:
            break
        rows, cones, bs = [], [], []
        # linearised matching condition with slack: J z_x - e = J x - m0
        A1 = sparse.lil_matrix((6, nz))
        A1[:, :nx] = J
        A1[:, ie0 : ie0 + ne] = -np.eye(6)
        rows.append(A1)
        bs.append(J @ x - m0)
        cones.append(clarabel.ZeroConeT(6))
        # caps on segment magnitudes, and the trust region box
        A2 = sparse.lil_matrix((nt + 2 * nx, nz))
        for k in range(nt):
            A2[k, it0 + k] = 1.0
        for j in range(nx):
            A2[nt + j, j] = 1.0
            A2[nt + nx + j, j] = -1.0
        rows.append(A2)
        bs.append(np.concatenate([np.full(nt, cap), x + delta, -(x - delta)]))
        cones.append(clarabel.NonnegativeConeT(nt + 2 * nx))
        # |d_k| <= t_k
        A3 = sparse.lil_matrix((4 * nt, nz))
        for k in range(nt):
            A3[4 * k, it0 + k] = -1.0
            for c in range(3):
                A3[4 * k + 1 + c, 3 * k + c] = -1.0
            cones.append(clarabel.SecondOrderConeT(4))
        rows.append(A3)
        bs.append(np.zeros(4 * nt))
        if nf:
            A4 = sparse.lil_matrix((4, nz))
            for c in range(3):
                A4[1 + c, 3 * nseg + c] = -1.0
            rows.append(A4)
            bs.append(np.array([vmax, 0, 0, 0]))
            cones.append(clarabel.SecondOrderConeT(4))
        A5 = sparse.lil_matrix((7, nz))
        A5[0, itau] = -1.0
        for c in range(6):
            A5[1 + c, ie0 + c] = -1.0
        rows.append(A5)
        bs.append(np.zeros(7))
        cones.append(clarabel.SecondOrderConeT(7))
        A = sparse.vstack(rows).tocsc()
        sol = clarabel.DefaultSolver(P, q, A, np.concatenate(bs), cones, settings).solve()
        if str(sol.status) not in ('Solved', 'AlmostSolved'):
            break
        x = np.asarray(sol.x[:nx])
        delta = max(0.75 * delta, 0.02)
    if best is None:
        m0 = mis(x[None, :])[0]
        return LegResult(False, np.inf, 0.0, float(np.max(np.abs(m0))), np.inf)
    cost, xb, err = best
    vinf = float(np.linalg.norm(xb[3 * nseg :])) if nf else 0.0
    return LegResult(True, cost, vinf, err, cost / (cap * nseg))


# ---------------------------------------------------------------------------------------
# Impulsive leg tables with revolutions and the lunar assist credit
# ---------------------------------------------------------------------------------------

REV_OPTIONS = ((0, 0), (1, 0), (1, 1), (2, 0), (2, 1))  # (revolutions, branch)


def earth_end(t, lga: bool):
    """Reference state at the Earth end. Position is the SEL1 point in both cases. Without
    an assist the vehicle starts with SEL1's velocity (as in the first screen); with one its
    excess velocity is measured against Earth's."""
    r, v = sel1_state(t)
    if lga:
        _, v = earth_state(t)
    return r, v


def asteroid_state(el, t):
    return kepler_state(el['a'], el['e'], el['i'], el['om'], el['w'], el['ma'], el['epoch'], t)


def impulsive_tables(el: dict, t_dep: np.ndarray, tofs: np.ndarray, outbound: bool, credits=(0.0,),
                     revs=REV_OPTIONS):
    """Best impulsive Δv (km/s) over revolution options for every (asteroid, departure, tof),
    for each Earth-end credit (free excess speed, km/s). A credit of 0 measures against the
    SEL1 velocity, as the first screen did; a positive credit measures against Earth's.
    Returns {credit: (dv, rev_index)}, arrays of shape (N, D, T)."""
    from nea_accessibility import lambert

    N, D, T = len(el['a']), len(t_dep), len(tofs)
    td = np.broadcast_to(t_dep[None, :, None], (N, D, T))
    ta = td + tofs[None, None, :]
    ae = {k: np.asarray(el[k])[:, None, None] for k in ('a', 'e', 'i', 'om', 'w', 'ma', 'epoch')}
    te = td if outbound else ta
    re, ve_sel1 = sel1_state(te)
    _, ve_earth = earth_state(te)
    ra, va = asteroid_state(ae, ta if outbound else td)
    r1, r2 = (re, ra) if outbound else (ra, re)
    tt = np.broadcast_to(tofs[None, None, :], (N, D, T))
    best = {c: np.full((N, D, T), np.inf) for c in credits}
    which = {c: np.zeros((N, D, T), dtype=np.int8) for c in credits}
    for idx, (nrev, br) in enumerate(revs):
        if nrev == 0:
            v1, v2 = lambert(r1, r2, tt)
        else:
            v1, v2 = lambert_multirev(r1, r2, tt, nrev, br)
        vt_e, vt_a = (v1, v2) if outbound else (v2, v1)  # transfer velocity at Earth end, asteroid end
        ast = np.linalg.norm(vt_a - va, axis=-1) * KMS
        for c in credits:
            ref = ve_earth if c > 0 else ve_sel1
            dv = np.maximum(np.linalg.norm(vt_e - ref, axis=-1) * KMS - c, 0) + ast
            dv = np.where(np.isfinite(dv), dv, np.inf)
            better = dv < best[c]
            best[c] = np.where(better, dv, best[c])
            which[c] = np.where(better, idx, which[c])
    return {c: (best[c], which[c]) for c in credits}


def seed_velocities(el1: dict, t_dep: float, tof: float, outbound: bool, lga: bool, rev_index: int):
    """End states and the impulsive transfer velocities for one leg of one asteroid."""
    from nea_accessibility import lambert

    td, ta = np.array(t_dep, float), np.array(t_dep + tof, float)
    if outbound:
        r1, vs1 = earth_end(td, lga)
        r2, vs2 = asteroid_state(el1, ta)
    else:
        r1, vs1 = asteroid_state(el1, td)
        r2, vs2 = earth_end(ta, lga)
    r1, vs1, r2, vs2 = (np.asarray(q, float).reshape(3) for q in (r1, vs1, r2, vs2))
    nrev, br = REV_OPTIONS[rev_index]
    if nrev == 0:
        v1, v2 = lambert(r1[None], r2[None], np.array([tof]))
    else:
        v1, v2 = lambert_multirev(r1[None], r2[None], np.array([tof]), nrev, br)
    return r1, vs1, r2, vs2, v1[0], v2[0]
