"""
rq-0-52: the cost of moving a tug round the node orbit (phasing), so that a tug parked at the
station can leave from another place on the orbit, and come back.

A two-burn transfer in the Sun-Earth three-body model (cislunar_flyby._f1): the tug leaves the
orbit at place a with a burn, coasts for tau, and meets the orbit again with a second burn at
the place that is `delta` of a period ahead of where the station then is (delta < 0: behind).
The first burn is solved by shooting on the arrival position; the second matches the
orbit's velocity there. Large offsets are reached by continuation from delta = 0, where both
burns vanish.

An impulsive cost, which a low-thrust tug spending tau on it can roughly match; it is not a
minimum over all phasing strategies (more burns or more revolutions can cost less).
"""

from __future__ import annotations

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import least_squares

import cislunar_flyby as c

KM = c.AU_KM
MS = c.VU_KMS * 1e3  # m/s per velocity unit


def coast(state, tau_days):
    return solve_ivp(c._f1, (0, tau_days * c.DAY), state, method='DOP853', rtol=1e-11, atol=1e-13).y[:, -1]


def transfer(orbit, a: float, delta: float, tau_days: float, guess=None):
    """Two-burn transfer from place a to the place delta of a period ahead of the station after
    tau_days. Returns (total m/s, first burn m/s, second burn m/s, first burn vector in velocity
    units, arrival miss km)."""
    start = orbit.at(a)
    goal = orbit.at(a + tau_days / orbit.period_days + delta)

    def miss(dv):
        s = start.copy()
        s[3:] += dv / MS
        return (coast(s, tau_days)[:3] - goal[:3]) * KM / 100.0  # in 100 km

    x0 = np.zeros(3) if guess is None else np.asarray(guess, float)
    r = least_squares(miss, x0, xtol=1e-12, ftol=1e-12, gtol=1e-12, max_nfev=60, diff_step=1e-7)
    s = start.copy()
    s[3:] += r.x / MS
    end = coast(s, tau_days)
    dv1 = float(np.linalg.norm(r.x))
    dv2 = float(np.linalg.norm(goal[3:] - end[3:]) * MS)
    return dv1 + dv2, dv1, dv2, r.x, float(np.linalg.norm(end[:3] - goal[:3]) * KM)


def sweep(orbit, a: float, deltas, tau_days: float, step: float = 1.0 / 64.0, max_miss_km: float = 1.0):
    """Costs for offsets `deltas` (all of one sign, increasing in size) at one start place and
    transfer time, by continuation from zero offset. Returns {delta: total m/s or inf}."""
    out, guess, d, tot = {}, np.zeros(3), 0.0, 0.0
    deltas = list(deltas)
    for target in deltas:
        h = step
        while abs(d) < abs(target) - 1e-12 and h >= step / 8:
            nd = np.sign(target) * min(abs(d) + h, abs(target))
            t, _, _, x, m = transfer(orbit, a, nd, tau_days, guess)
            if m > max_miss_km:
                h /= 2  # a smaller step before giving up
                continue
            d, guess, tot = nd, x, t
        if abs(d - target) < 1e-12:
            out[target] = tot
            continue
        t, _, _, x, m = transfer(orbit, a, target, tau_days)  # last try: straight from no burn
        out[target] = t if m <= max_miss_km else np.inf
        if m <= max_miss_km:
            d, guess, tot = target, x, t
    return out
