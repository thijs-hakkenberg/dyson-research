"""
rq-0-52: the node-to-escape leg checked with the Moon's gravity acting all the way.

node_leg_direct flies the leg in the Sun-Earth three-body model and treats the swingby as
instantaneous: where the path crosses the Moon's orbital distance, with the Moon there, the
excess velocity relative to the Moon is turned (patched conics). Before and after, the Moon
does not pull. Here the same leg is flown with the Moon's gravity throughout. The CR3BP's
Earth point is taken as the Earth-Moon barycentre (as for Sun-Earth L1/L2 work generally):
the Earth and the Moon sit either side of it, the Moon on its inclined circular orbit placed
by the leg's clocks. (Holding the Earth fixed and adding the Moon's indirect pull instead
makes the tug drift ~12.5 m/s, ~10,000 km per 10 days, against the patched states: an
artefact of mixing frames, not a cost.)

The patched swingby gives a hyperbola about the Moon: the turn fixes the perilune distance,
the incoming and outgoing directions fix where perilune is and which way the tug moves
there. The leg is then solved by multiple shooting from the patched path: states every
`spacing` days along it (the burn at the node orbit, the patched path before and after the
swingby, and the perilune state in place of the instant turn) are the unknowns, and the
coasts between them, flown with the full model, must join in position. Correction burns
are allowed at every node but perilune (corrections='all'; or only a couple of days before
the swingby, corrections='one', which rarely converges: the months near Earth before the
swingby drift by thousands of km). The escape must give the leg's excess velocity within
the escape window and time budget, and the tug must pass no lower than 100 km above the
Moon. The sum of all burns is minimised by SLSQP with exact (STM) derivatives; `extra_ms`
is that sum less the patched model's burn: what the Moon's gravity costs. SLSQP is stopped
at its iteration cap well before it reports convergence, so `extra_ms` is an upper bound
on the cost of the joined path it found.

A continuation in the Moon's mass (patched conics at a small share, stepped up) was tried
and dropped: at a small share the swingby passes tens of km from a point Moon, where the
problem is stiffest.
"""

from __future__ import annotations

import time
from dataclasses import dataclass

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import OptimizeResult, minimize

import cislunar_flyby as c
import node_leg_direct as d
import node_phasing_multi as pm

KM = c.AU_KM
MS = c.VU_KMS * 1e3
R_MOON = 1738.0 / KM
SHARE = c.MU_MOON / (c.MU_EARTH + c.MU_MOON)  # the Moon's share of the Earth-Moon mass
BOX = (3000.0, 100.0)  # how far a stage may move each node from where it started (km, m/s)
MAX_EVALS, MAX_SECONDS = 300, 900.0  # per stage


class _Stop(Exception):
    pass
TOL = {'join_km': 1.0, 'join_ms': 0.1, 'direction_ms': 1.0, 'lowest_km': 99.0}
ODE = dict(method='DOP853', rtol=1e-11, atol=1e-14)
ODE_STM = dict(method='DOP853', rtol=1e-10, atol=np.r_[[1e-14] * 6, [1e-10] * 36])  # tighter STM tolerances fail through perilune


class Moon:
    """Rotating-frame position of the Moon from the leg's clocks; t in time units from day T0."""

    def __init__(self, clocks: d.Clocks, T0: float, k: float = 1.0):
        self.clocks, self.T0 = clocks, T0
        self.mu = c.MUM * k

    def rel(self, t):
        """Earth to Moon."""
        days = self.T0 + t * c.TU_DAYS
        node = np.radians(self.clocks.node(days))
        lam = np.radians(self.clocks.moon(days))
        u = np.arctan2(np.sin(lam - node), np.cos(lam - node) * np.cos(c.INC_MOON))
        return c.moon_position(node, u)

    def pos(self, t):
        """The CR3BP's Earth point is taken as the Earth-Moon barycentre: the Moon sits
        on one side of it and the Earth (earth(t)) on the other."""
        return c.EARTH + (1.0 - SHARE) * self.rel(t)

    def earth(self, t):
        return c.EARTH - SHARE * self.rel(t)

    def vel(self, t, h=1e-6):
        return (self.pos(t + h) - self.pos(t - h)) / (2 * h)


def _pull(dr, mu):
    return -mu * dr / np.linalg.norm(dr) ** 3


def _grad(dr, mu):
    r = np.linalg.norm(dr)
    return -mu * (np.eye(3) / r**3 - 3 * np.outer(dr, dr) / r**5)


def _extra(t, r, moon: Moon):
    """The CR3BP's point Earth at the barycentre is replaced by the Earth and the Moon
    either side of it: acceleration and its gradient to add to the CR3BP's."""
    de0, de, dm = r - c.EARTH, r - moon.earth(t), r - moon.pos(t)
    a = -_pull(de0, c.MU) + _pull(de, c.MU) + _pull(dm, moon.mu)
    G = -_grad(de0, c.MU) + _grad(de, c.MU) + _grad(dm, moon.mu)
    return a, G


def rhs(t, s, moon: Moon):
    f = c._f1(t, s)
    f[3:] += _extra(t, s[:3], moon)[0]
    return f


def _spin(rho):
    return np.array([-rho[1], rho[0], 0.0])


def perilune(moon: Moon, tc: float, vinf_in, vinf_out):
    """Rotating-frame state at perilune of the hyperbola that turns vinf_in into vinf_out
    (Moon-relative, non-rotating axes), with the Moon where the clocks put it at tc."""
    v = np.linalg.norm(vinf_in)
    ui, uo = vinf_in / v, vinf_out / np.linalg.norm(vinf_out)
    delta = np.arccos(np.clip(ui @ uo, -1, 1))
    rp = moon.mu / v**2 * (1 / np.sin(delta / 2) - 1)
    p = (ui - uo) / np.linalg.norm(ui - uo)  # from the Moon to the tug: away from the way it is turned
    q = (ui + uo) / np.linalg.norm(ui + uo)
    vp = np.sqrt(v**2 + 2 * moon.mu / rp)
    rm = moon.pos(tc)
    vm_inertial = moon.vel(tc) + _spin(rm - c.EARTH)
    r = rm + rp * p
    return np.concatenate([r, vm_inertial + vp * q - _spin(r - c.EARTH)])


def _escape(t, s, moon):
    return np.linalg.norm(s[:3] - c.EARTH) - c.R_ESCAPE


_escape.terminal, _escape.direction = True, 1


def closest(sol, moon: Moon, t0: float, t1: float, n: int = 400) -> float:
    """Least distance (time units of length) from the Moon over [t0, t1] of a dense solution."""
    dist = lambda t: np.linalg.norm(sol(t)[:3] - moon.pos(t))
    ts = np.linspace(t0, t1, n)
    ds = np.array([dist(t) for t in ts])
    k = int(np.argmin(ds))
    lo, hi = ts[max(k - 1, 0)], ts[min(k + 1, n - 1)]
    for _ in range(40):  # golden-section search on the bracket
        m1, m2 = hi - 0.618 * (hi - lo), lo + 0.618 * (hi - lo)
        if dist(m1) < dist(m2):
            hi = m2
        else:
            lo = m1
    return min(ds[k], dist(0.5 * (lo + hi)))


def _f_stm(t, w, moon: Moon):
    f = pm._f_stm(t, w)
    a, G = _extra(t, w[:3], moon)
    f[3:6] += a
    P = w[6:].reshape(6, 6)
    f[6:].reshape(6, 6)[3:] += G @ P[:3]
    return f


def _escape_stm(t, w, moon):
    return np.linalg.norm(w[:3] - c.EARTH) - c.R_ESCAPE


_escape_stm.terminal, _escape_stm.direction = True, 1


def _w(y):
    v, lon, lat, c3 = c.escape_state(y[None, :])
    return v[0] * d.direction(lon[0], lat[0])


@dataclass
class Check:
    ok: bool
    converged: bool = False
    join_km: float = np.nan  # worst position mismatch between coasts
    join_ms: float = np.nan  # worst velocity mismatch between coasts, other than at the correction burn
    burn_ms: float = np.nan  # departure burn
    tcm_ms: float = np.nan  # correction burns, summed
    corrections: int = 0  # correction burns above 1 m/s
    total_ms: float = np.nan
    extra_ms: float = np.nan  # total less the patched model's burn
    direction_ms: float = np.nan  # |excess velocity - wanted|
    escape_shift_days: float = np.nan  # escape date less the patched model's
    flight_days: float = np.nan
    lowest_km: float = np.nan  # height of the lowest pass over the Moon
    iterations: int = 0
    seconds: float = 0.0


class FullLeg:
    """One leg solved by node_leg_direct (settings x), re-solved with the Moon's gravity by
    multiple shooting. Burns are allowed at the node orbit (departure) and at the nodes in
    `free` (corrections); elsewhere the coasts must join in position and velocity. The sum of
    the burns is minimised, so `extra_ms` is what the Moon's gravity costs over the patched
    swingby."""

    def __init__(self, orbit, clocks, x, tc_days, dv_ms, w_target, escape_T, window_days, budget_days, spacing=10.0, near=2.0, corrections='all'):
        T, az, share, up, frac, roll = x
        self.patched = d.fly(orbit, clocks, x, dv_ms, tc_days)
        self.dv_ms, self.w_target, self.escape_T, self.window, self.budget = dv_ms, np.asarray(w_target, float), escape_T, window_days, budget_days
        self.node = orbit.at(float(clocks.place(T)))
        y0 = c.burn_states(self.node[None, :], np.array([az]), np.array([up]), dv_ms, share)[0]
        self.burn_patched = float(np.linalg.norm(y0[3:] - self.node[3:]) * MS)
        a = solve_ivp(c._f1, (0, (self.patched.encounter_days + 1) * c.DAY), y0, dense_output=True, events=d._moon_cross, **ODE)
        k = int(np.argmin(np.abs(a.t_events[0] - self.patched.encounter_days * c.DAY)))
        tc, yc = a.t_events[0][k], a.y_events[0][k][None, :]
        vin, vm, _ = c.encounter_vinf_inclined(yc, np.array([tc]), np.radians(float(clocks.node(T))))
        vout = c.turn(vin, np.array([frac]) * c.max_turn(np.linalg.norm(vin, axis=1)), np.array([roll]))
        y1 = c.after_swingby(yc, vout, vm)[0]
        self.t_max = (budget_days + 30.0) * c.DAY
        b = solve_ivp(c._f1, (tc, self.t_max), y1, dense_output=True, events=d._escape, **ODE)
        te = b.t_events[0][0]
        self.moon = Moon(clocks, T)
        h, n = spacing * c.DAY, min(near * c.DAY, 0.5 * tc)
        t_in = list(np.arange(0.0, tc - n - 0.5 * c.DAY, h)) or [0.0]
        t_out = list(np.arange(tc + n + h, te - 1.0 * c.DAY, h))
        # the nodes either side of the Moon start on the hyperbola, flown out from perilune with the Moon's gravity
        p0 = perilune(self.moon, tc, vin[0], vout[0])
        back = solve_ivp(rhs, (tc, tc - n), p0, args=(self.moon,), **ODE).y[:, -1]
        fwd = solve_ivp(rhs, (tc, tc + n), p0, args=(self.moon,), **ODE).y[:, -1]
        self.times = t_in + [tc - n, tc, tc + n] + t_out
        self.peri = len(t_in) + 1
        self.tcm = self.peri - 1
        # nodes where a correction burn is allowed: one before the swingby, or every node but perilune
        self.free = (self.tcm,) if corrections == 'one' else tuple(i for i in range(1, len(self.times)) if i != self.peri)
        self.guess = [y0] + [a.sol(t) for t in t_in[1:]] + [back, p0, fwd] + [b.sol(t) for t in t_out]
        self.N = len(self.times)
        self.n = 3 + 6 * (self.N - 1)
        self.patched_escape_T = T + te * c.TU_DAYS
        self._z = None

    # --- unknowns
    def _cols(self, i):
        return slice(0, 3) if i == 0 else slice(3 + 6 * (i - 1), 9 + 6 * (i - 1))

    def _ds(self, i):
        """d(state of node i)/d(its unknowns): 1 km and 1 m/s."""
        if i == 0:
            return np.vstack([np.zeros((3, 3)), np.eye(3) / MS])
        return np.diag([1.0 / KM] * 3 + [1.0 / MS] * 3)

    def states(self, z):
        s = [np.concatenate([self.node[:3], self.guess[0][3:] + z[:3] / MS])]
        for i in range(1, self.N):
            s.append(self.guess[i] + z[self._cols(i)] * np.array([1.0 / KM] * 3 + [1.0 / MS] * 3))
        return s

    def _eval(self, z):
        if self._z is not None and np.array_equal(z, self._z):
            return
        self._z = z.copy()
        self.s = self.states(z)
        self.e, self.phi = [], []
        self.failed = False
        for i in range(self.N - 1):
            sol = solve_ivp(_f_stm, (self.times[i], self.times[i + 1]), np.concatenate([self.s[i], np.eye(6).ravel()]), args=(self.moon,), **ODE_STM)
            self.failed |= sol.status < 0
            w = sol.y[:, -1]
            self.e.append(w[:6])
            self.phi.append(w[6:].reshape(6, 6))
        r = solve_ivp(_f_stm, (self.times[-1], self.t_max), np.concatenate([self.s[-1], np.eye(6).ravel()]), args=(self.moon,), events=_escape_stm, **ODE_STM)
        self.failed |= r.status < 0
        self.escaped = bool(len(r.t_events[0])) and not self.failed
        w = r.y_events[0][0] if self.escaped else r.y[:, -1]
        ye, P = w[:6], w[6:].reshape(6, 6)
        fe = rhs(0.0 if not self.escaped else r.t_events[0][0], ye, self.moon)
        dg = np.concatenate([(ye[:3] - c.EARTH) / np.linalg.norm(ye[:3] - c.EARTH), np.zeros(3)])
        dt = -(dg @ P) / (dg @ fe)  # d(escape time)/d(last node state)
        self.ye, self.te = ye, (r.t_events[0][0] if self.escaped else self.t_max)
        self.dye = P + np.outer(fe, dt)
        self.dte = dt
        jw = np.zeros((3, 6))
        for k in range(6):
            h = np.zeros(6)
            h[k] = 1e-9
            jw[:, k] = (_w(ye + h) - _w(ye - h)) / 2e-9
        self.dw = jw @ self.dye  # d(w km/s)/d(last node state)

    # --- objective: the two burns
    def burns(self, z):
        self._eval(z)
        b0 = (self.s[0][3:] - self.node[3:]) * MS
        return b0, [(self.s[i][3:] - self.e[i - 1][3:]) * MS for i in self.free]

    def cost(self, z):
        b0, bt = self.burns(z)
        g = np.zeros(self.n)
        n0 = np.sqrt(b0 @ b0 + pm.EPS**2)
        g[self._cols(0)] += (b0 / n0) @ (self._ds(0)[3:] * MS)
        f = n0
        for i, b in zip(self.free, bt):
            nb = np.sqrt(b @ b + pm.EPS**2)
            f += nb
            g[self._cols(i)] += (b / nb) @ (self._ds(i)[3:] * MS)
            g[self._cols(i - 1)] -= (b / nb) @ (self.phi[i - 1][3:] @ self._ds(i - 1) * MS)
        return f, g

    # --- equalities: joins and the excess velocity
    def eq(self, z):
        self._eval(z)
        out = []
        for i in range(self.N - 1):
            m = self.e[i] - self.s[i + 1]
            out.append(m[:3] * KM)
            if i + 1 not in self.free:
                out.append(m[3:] * MS)
        out.append((_w(self.ye) - self.w_target) * 1e3 if self.escaped else np.full(3, 1e4))
        return np.concatenate(out)

    def eq_jac(self, z):
        self._eval(z)
        rows = []
        for i in range(self.N - 1):
            parts = [(slice(0, 3), KM)] + ([(slice(3, 6), MS)] if i + 1 not in self.free else [])
            for sl, u in parts:
                J = np.zeros((3, self.n))
                J[:, self._cols(i)] += u * self.phi[i][sl] @ self._ds(i)
                J[:, self._cols(i + 1)] -= u * self._ds(i + 1)[sl]
                rows.append(J)
        J = np.zeros((3, self.n))
        J[:, self._cols(self.N - 1)] = 1e3 * self.dw @ self._ds(self.N - 1)
        rows.append(J)
        return np.vstack(rows)

    # --- inequalities: lowest pass, escape window, time budget
    def ineq(self, z):
        self._eval(z)
        rp = self.s[self.peri][:3] - self.moon.pos(self.times[self.peri])
        esc = self.moon.T0 + self.te * c.TU_DAYS
        return np.array([np.linalg.norm(rp) * KM - (R_MOON * KM + 100.0), self.window - (esc - self.escape_T), self.window + (esc - self.escape_T),
                         self.budget - (esc - self.moon.T0)])

    def ineq_jac(self, z):
        self._eval(z)
        J = np.zeros((4, self.n))
        rp = self.s[self.peri][:3] - self.moon.pos(self.times[self.peri])
        J[0, self._cols(self.peri)] = np.concatenate([rp / np.linalg.norm(rp), np.zeros(3)])
        dte = self.dte @ self._ds(self.N - 1) * c.TU_DAYS
        J[1, self._cols(self.N - 1)] = -dte
        J[2, self._cols(self.N - 1)] = dte
        J[3, self._cols(self.N - 1)] = -dte
        return J

    def report(self, z, converged=False, iterations=0) -> Check:
        self._eval(z)
        b0, bt = self.burns(z)
        joins = [self.e[i] - self.s[i + 1] for i in range(self.N - 1)]
        jk = max(np.linalg.norm(m[:3]) * KM for m in joins)
        jv = max([np.linalg.norm(m[3:]) * MS for i, m in enumerate(joins) if i + 1 not in self.free], default=0.0)
        tc = self.times[self.peri]
        sol = lambda i: solve_ivp(rhs, (self.times[i], self.times[i + 1]), self.s[i], args=(self.moon,), dense_output=True, **ODE).sol
        low = (min(closest(sol(self.peri - 1), self.moon, self.times[self.peri - 1], tc), closest(sol(self.peri), self.moon, tc, self.times[self.peri + 1])) - R_MOON) * KM
        tcms = [float(np.linalg.norm(b)) for b in bt]
        tot = float(np.linalg.norm(b0) + sum(tcms))
        esc = self.moon.T0 + self.te * c.TU_DAYS
        ch = Check(False, converged, float(jk), float(jv), float(np.linalg.norm(b0)), sum(tcms), sum(t > 1.0 for t in tcms), tot, tot - self.burn_patched,
                   float(np.linalg.norm(_w(self.ye) - self.w_target) * 1e3) if self.escaped else np.inf, esc - self.patched_escape_T,
                   esc - self.moon.T0, float(low), iterations)
        ch.ok = bool(self.escaped and jk < TOL['join_km'] and jv < TOL['join_ms'] and ch.direction_ms < TOL['direction_ms'] and low >= TOL['lowest_km']
                     and abs(esc - self.escape_T) <= self.window + 0.5 and ch.flight_days <= self.budget + 0.5)
        return ch

    def _stage(self, z, maxiter, max_evals=MAX_EVALS, max_seconds=MAX_SECONDS):
        """One SLSQP solve at the current Moon mass, kept within a box around its start (the
        nodes move at most BOX km and m/s) and stopped after max_evals new evaluations or
        max_seconds, so a stage that wanders off cannot run on for hours."""
        evals, t0 = [0], time.time()
        best = [z.copy(), np.inf]

        def cost(v):
            if self._z is None or not np.array_equal(v, self._z):
                evals[0] += 1
                if evals[0] > max_evals or time.time() - t0 > max_seconds:
                    raise _Stop
            out = self.cost(v)
            viol = max(np.max(np.abs(self.eq(v))), -np.min(self.ineq(v)), 0.0)
            if viol < best[1]:
                best[0], best[1] = v.copy(), viol
            return out
        lo = z - np.r_[[BOX[1]] * 3, np.tile([BOX[0]] * 3 + [BOX[1]] * 3, self.N - 1)]
        hi = 2 * z - lo
        try:
            r = minimize(cost, z, jac=True, method='SLSQP', bounds=list(zip(lo, hi)), options={'maxiter': maxiter, 'ftol': 1e-6},
                         constraints=[{'type': 'eq', 'fun': self.eq, 'jac': self.eq_jac}, {'type': 'ineq', 'fun': self.ineq, 'jac': self.ineq_jac}])
        except _Stop:
            r = OptimizeResult(x=best[0], success=False, nit=0, message='stopped: evaluation or time cap')
        feasible = bool(np.max(np.abs(self.eq(r.x))) < 1.0 and np.min(self.ineq(r.x)) > -1.0)
        return r, feasible

    def solve(self, maxiter: int = 100, restarts: int = 3):
        """SLSQP from the patched path, restarted from where it stopped up to `restarts`
        times while it has not converged. Returns (the patched path flown as is, the
        solution, its unknowns)."""
        t0 = time.time()
        first = self.report(np.zeros(self.n))
        z, its, r = np.zeros(self.n), 0, None
        for _ in range(restarts):
            r, ok = self._stage(z, maxiter)
            its += r.nit
            z = r.x
            if ok and r.success:
                break
        out = self.report(z, bool(r.success), its)
        out.seconds = time.time() - t0
        return first, out, z
