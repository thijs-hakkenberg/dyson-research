"""
rq-0-52: phasing on the node orbit with many burns, over one or more revolutions; cheaper than
the two-burn transfers of node_phasing.py, which are an upper bound.

A tug at place a of the orbit is to be at the place `delta` of a period ahead of where the
station is after tau days (delta < 0: behind), in the Sun-Earth three-body model
(cislunar_flyby._f1). The transfer is split into m coasts of equal length with a burn at the
start of each and one on arrival (m + 1 burns). It is solved by multiple shooting: the
unknowns are the velocity after the first burn and the position and velocity after each later
burn; the coasts must join in position and end on the orbit; the sum of the burn sizes is
minimised (SLSQP, with the state transition matrix for the derivatives). The first guess slides
the tug along the orbit at a steady rate.

With one coast this is the two-burn transfer. With many short coasts it approaches what a
low-thrust tug spending tau on it pays. It is a local optimum from one first guess, so it is
still an upper bound on the cheapest phasing, but a lower one.
"""

from __future__ import annotations

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import minimize

import cislunar_flyby as c

MU = c.MU
MS = c.VU_KMS * 1e3  # m/s per velocity unit
PS = 1e3 / c.AU_KM  # optimisation unit of position: 1000 km
VS = 1.0 / MS  # optimisation unit of velocity: 1 m/s
EPS = 1e-2  # m/s, smooths the burn size at zero


def _f_stm(t, w):
    x, y, z, vx, vy, vz = w[:6]
    r1v = np.array([x + MU, y, z])
    r2v = np.array([x - 1.0 + MU, y, z])
    r1, r2 = np.sqrt(r1v @ r1v), np.sqrt(r2v @ r2v)
    acc = np.array([2 * vy + x, -2 * vx + y, 0.0]) - (1 - MU) * r1v / r1**3 - MU * r2v / r2**3
    U = (1 - MU) * (3 * np.outer(r1v, r1v) / r1**5 - np.eye(3) / r1**3) + MU * (3 * np.outer(r2v, r2v) / r2**5 - np.eye(3) / r2**3)
    U[0, 0] += 1.0
    U[1, 1] += 1.0
    P = w[6:].reshape(6, 6)
    dP = np.empty((6, 6))
    dP[:3] = P[3:]
    dP[3:] = U @ P[:3]
    dP[3] += 2 * P[4]
    dP[4] -= 2 * P[3]
    return np.concatenate([[vx, vy, vz], acc, dP.ravel()])


def coast_stm(state, t):
    w = solve_ivp(_f_stm, (0, t), np.concatenate([state, np.eye(6).ravel()]), method='DOP853', rtol=1e-11, atol=1e-13).y[:, -1]
    return w[:6], w[6:].reshape(6, 6)


def _norm_eps(d):
    return np.sqrt(d @ d + EPS**2)


class Transfer:
    """The multiple-shooting problem for one start place, offset, transfer time and number of coasts."""

    def __init__(self, orbit, a: float, delta: float, tau_days: float, coasts: int):
        self.m = coasts
        self.h = tau_days * c.DAY / coasts
        self.start = orbit.at(a)
        self.goal = orbit.at(a + tau_days / orbit.period_days + delta)
        # first guess: slide along the orbit at a steady rate from a to the goal's place
        step = (tau_days / orbit.period_days + delta) / coasts
        self.guess = [orbit.at(a + i * step) for i in range(coasts)]
        self.n = 3 + 6 * (coasts - 1)
        self._z = None

    def states(self, z):
        s = [np.concatenate([self.start[:3], self.guess[0][3:] + z[:3] * VS])]
        for i in range(1, self.m):
            k = 3 + 6 * (i - 1)
            s.append(np.concatenate([self.guess[i][:3] + z[k:k + 3] * PS, self.guess[i][3:] + z[k + 3:k + 6] * VS]))
        return s

    def _eval(self, z):
        if self._z is not None and np.array_equal(z, self._z):
            return
        self._z = z.copy()
        self.s = self.states(z)
        self.e, self.phi = zip(*(coast_stm(s, self.h) for s in self.s))

    def burns(self, z):
        """Burns in m/s: first, between coasts, on arrival."""
        self._eval(z)
        b = [(self.s[0][3:] - self.start[3:]) * MS]
        b += [(self.s[i][3:] - self.e[i - 1][3:]) * MS for i in range(1, self.m)]
        b.append((self.goal[3:] - self.e[-1][3:]) * MS)
        return b

    def _cols(self, i):
        """Columns of z that set the start of coast i, and d(state)/d(those columns)."""
        if i == 0:
            return slice(0, 3), np.vstack([np.zeros((3, 3)), np.eye(3) * VS])
        k = 3 + 6 * (i - 1)
        return slice(k, k + 6), np.diag([PS] * 3 + [VS] * 3)

    def cost(self, z):
        b = self.burns(z)
        g = np.zeros(self.n)
        f = 0.0
        for j, d in enumerate(b):
            nd = _norm_eps(d)
            f += nd
            u = d / nd
            if j < self.m:  # the burn's own velocity
                cols, ds = self._cols(j)
                g[cols] += u @ (ds[3:] * MS)
            if j > 0:  # minus the velocity the previous coast arrives with
                cols, ds = self._cols(j - 1)
                g[cols] -= u @ (self.phi[j - 1][3:] @ ds * MS)
        return f, g

    def joins(self, z):
        self._eval(z)
        out = [(self.e[i][:3] - self.s[i + 1][:3]) / PS for i in range(self.m - 1)]
        out.append((self.e[-1][:3] - self.goal[:3]) / PS)
        return np.concatenate(out)

    def joins_jac(self, z):
        self._eval(z)
        J = np.zeros((3 * self.m, self.n))
        for i in range(self.m):
            cols, ds = self._cols(i)
            J[3 * i:3 * i + 3, cols] = self.phi[i][:3] @ ds / PS
            if i < self.m - 1:
                nc, nds = self._cols(i + 1)
                J[3 * i:3 * i + 3, nc] -= nds[:3] / PS
        return J

    def solve(self, z0=None, maxiter: int = 400):
        z0 = np.zeros(self.n) if z0 is None else z0
        r = minimize(self.cost, z0, jac=True, method='SLSQP', options={'maxiter': maxiter, 'ftol': 1e-8},
                     constraints={'type': 'eq', 'fun': self.joins, 'jac': self.joins_jac})
        miss_km = float(np.max(np.abs(self.joins(r.x)))) * 1e3
        b = self.burns(r.x)
        return {'total_ms': float(sum(np.linalg.norm(d) for d in b)), 'burns_ms': [float(np.linalg.norm(d)) for d in b],
                'miss_km': miss_km, 'converged': bool(r.success), 'z': r.x,
                'min_earth_km': float(min(np.linalg.norm(s[:3] - c.EARTH) for s in self.s + list(self.e)) * c.AU_KM)}


def phasing(orbit, a: float, delta: float, tau_days: float, coast_days: float = 15.0, max_miss_km: float = 1.0):
    """Cheapest multi-burn cost (m/s) found, or inf; and the solution."""
    m = max(1, int(round(tau_days / coast_days)))
    sol = Transfer(orbit, a, delta, tau_days, m).solve()
    return (sol['total_ms'] if sol['miss_km'] <= max_miss_km else np.inf), sol
