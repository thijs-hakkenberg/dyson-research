"""
rq-0-52: the leg between the node station and the edge of the Earth's sphere of influence,
solved for one tug leg at a time.

The reach tables (run_cislunar_flyby_3d.py) say what excess velocity a departure can reach,
binned by direction, node angle and station place. With the station's place fixed the bins
are thinly filled, so the tables under-count. Here the question is put directly: on this
date, with the station where it is, the Moon where it is and its node line where it is, is
there a burn at the station and a swingby that give exactly the excess velocity this tug
leg needs?

Unknowns: the date of the burn, its three components, and the swingby's turn and azimuth.
Conditions: the path crosses the Moon's orbital distance in the Moon's orbit plane, the
Moon is at that place at that time, and the excess velocity at escape is the one wanted.
Bounds: burn size, the lowest pass of the Moon, the time allowed, and the escape date
within a window of the date the leg was solved for. If the full excess speed cannot be had
in the wanted direction, the most that can is found. Seeds come from the stored sample of
escapes. An arrival is solved as its mirror image (cislunar_flyby.mirror).
"""

from __future__ import annotations

import time
from dataclasses import dataclass

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import least_squares

import cislunar_flyby as c

J2000 = 2451545.0
MOON_RATE = 12.19074912  # deg/day, mean elongation
NODE_RATE = -0.0529538 - 0.98564736  # deg/day, node angle from the Sun→Earth line
KM = c.AU_KM


def wrap(a, period=360.0):
    return (np.asarray(a, float) + period / 2) % period - period / 2


@dataclass(frozen=True)
class Clocks:
    """Where the station, the Moon's node line and the Moon are, by days from J2000.
    place: fraction of the node orbit's period; node, moon: degrees from the Sun→Earth line."""
    place0: float
    period_days: float
    node0: float = 125.0445 - 100.4665
    moon0: float = 297.8502 + 180.0

    def place(self, T):
        return (self.place0 + np.asarray(T, float) / self.period_days) % 1.0

    def node(self, T):
        return (self.node0 + NODE_RATE * np.asarray(T, float)) % 360.0

    def moon(self, T):
        return (self.moon0 + MOON_RATE * np.asarray(T, float)) % 360.0

    def mirrored(self):
        """The clocks of the mirror-image problem, in which time runs as −T: an arrival on
        day T is a departure on day −T of these."""
        return Clocks(-self.place0, self.period_days, 180.0 - self.node0, -self.moon0)


class NodeOrbit:
    def __init__(self, kind: str, size_km: float):
        self.state, self.period = (c.halo_orbit if kind == 'halo' else c.lyapunov_orbit)(size_km)
        self.period_days = self.period * c.TU_DAYS
        self._sol = solve_ivp(c._f1, (0, self.period), self.state, method='DOP853', rtol=1e-12, atol=1e-13, dense_output=True).sol

    def at(self, place: float):
        return self._sol((place % 1.0) * self.period)


def _moon_cross(t, s):
    return np.hypot(np.hypot(s[0] - c.EARTH[0], s[1]), s[2]) - c.A_MOON


def _escape(t, s):
    return np.hypot(np.hypot(s[0] - c.EARTH[0], s[1]), s[2]) - c.R_ESCAPE


_escape.terminal, _escape.direction = True, 1

_deadline = [np.inf]  # wall-clock limit (time.monotonic) on the leg being solved; reachable() sets it


def _clock(t, s):
    return _deadline[0] - time.monotonic()


_clock.terminal = True


def out_of_time() -> bool:
    return time.monotonic() > _deadline[0]


@dataclass
class Flown:
    ok: bool
    plane_km: float = np.nan
    moon_km: float = np.nan
    w: np.ndarray = None  # excess velocity at escape, km/s, (towards Sun→Earth, along track, north)
    burn_frac: float = np.nan
    flight_days: float = np.nan
    encounter_days: float = np.nan
    escape_T: float = np.nan


def fly(orbit: NodeOrbit, clocks: Clocks, x, dv_ms: float, tc_guess_days: float, t_max_days: float = 230.0) -> Flown:
    """One departure. x = (burn day from J2000, burn azimuth, in-plane share, out-of-plane
    share, swingby turn as a fraction of the largest allowed, swingby azimuth)."""
    T, az, share, up, frac, roll = x
    y0 = c.burn_states(orbit.at(float(clocks.place(T)))[None, :], np.array([az]), np.array([up]), dv_ms, share)[0]
    t1 = (tc_guess_days + 6.0) * c.DAY
    a = solve_ivp(c._f1, (0, t1), y0, method='DOP853', rtol=1e-10, atol=1e-12, events=(_moon_cross, _clock))
    if not len(a.t_events[0]) or len(a.t_events[1]):
        return Flown(False)
    k = int(np.argmin(np.abs(a.t_events[0] - tc_guess_days * c.DAY)))
    tc, yc = a.t_events[0][k], a.y_events[0][k][None, :]
    if abs(tc * c.TU_DAYS - tc_guess_days) > 5.0:
        return Flown(False)
    node_burn = np.radians(float(clocks.node(T)))
    tca = np.array([tc])
    plane = float(c.plane_miss(yc, tca, node_burn)[0]) * KM
    vinf, vm, place = c.encounter_vinf_inclined(yc, tca, node_burn)
    moon = np.radians(float(clocks.moon(T + tc * c.TU_DAYS)))
    moon_km = float(wrap(place[0] - moon, 2 * np.pi)) * c.A_MOON * KM
    speed = np.linalg.norm(vinf, axis=1)
    out = c.turn(vinf, np.array([frac]) * c.max_turn(speed), np.array([roll]))
    y1 = c.after_swingby(yc, out, vm)[0]
    b = solve_ivp(c._f1, (tc, t_max_days * c.DAY), y1, method='DOP853', rtol=1e-10, atol=1e-12, events=(_escape, _clock))
    if not len(b.t_events[0]) or len(b.t_events[1]):
        return Flown(False, plane, moon_km)
    te, ye = b.t_events[0][0], b.y_events[0][0][None, :]
    v, lon, lat, c3 = c.escape_state(ye)
    if c3[0] <= 0:
        return Flown(False, plane, moon_km)
    lo, la = np.radians(lon[0]), np.radians(lat[0])
    w = v[0] * np.array([np.cos(la) * np.cos(lo), np.cos(la) * np.sin(lo), np.sin(la)])
    return Flown(True, plane, moon_km, w, float(np.hypot(share, up)), te * c.TU_DAYS, tc * c.TU_DAYS, T + te * c.TU_DAYS)


def direction(lon_deg, lat_deg):
    lo, la = np.radians(lon_deg), np.radians(lat_deg)
    return np.array([np.cos(la) * np.cos(lo), np.cos(la) * np.sin(lo), np.sin(la)])


@dataclass
class Solution:
    ok: bool
    x: np.ndarray = None
    flown: Flown = None
    evals: int = 0
    speed: float = 0.0  # km/s delivered along the wanted direction


TOL = {'plane_km': 50.0, 'moon_km': 500.0, 'direction_ms': 10.0}


def accept(f: Flown, w_target, escape_T, window_days, budget_days) -> bool:
    return bool(f.ok and abs(f.plane_km) < TOL['plane_km'] and abs(f.moon_km) < TOL['moon_km']
                and np.linalg.norm(f.w - w_target) * 1e3 < TOL['direction_ms'] and f.burn_frac <= 1.0 + 1e-4
                and f.flight_days <= budget_days + 0.5 and abs(f.escape_T - escape_T) <= window_days + 0.5)


def solve(orbit: NodeOrbit, clocks: Clocks, seed, w_target, dv_ms: float, escape_T: float, window_days: float,
          budget_days: float, max_nfev: int = 20) -> Solution:
    """Least squares from one seed (settings, encounter time in days after the burn) to the
    exact excess velocity w_target (km/s) under all conditions."""
    x0, tc_guess = np.asarray(seed[0], float), float(seed[1])
    count = [0]

    def res(x):
        count[0] += 1
        f = fly(orbit, clocks, x, dv_ms, tc_guess)
        if not f.ok:
            return np.full(8, 1e3)
        return np.concatenate([[f.plane_km / 20.0, f.moon_km / 200.0], (f.w - w_target) * 1e3 / 4.0,
                               [max(0.0, f.burn_frac - 1.0) * 200.0, max(0.0, abs(f.escape_T - escape_T) - window_days) * 10.0,
                                max(0.0, f.flight_days - budget_days) * 10.0]])

    lo = np.array([x0[0] - 20.0, -np.inf, 0.0, -1.0, 0.0, -np.inf])
    hi = np.array([x0[0] + 20.0, np.inf, 1.0, 1.0, 1.0, np.inf])
    x0 = np.clip(x0, lo + 1e-9, hi - 1e-9)
    try:
        r = least_squares(res, x0, bounds=(lo, hi), x_scale=np.array([1.0, 0.1, 0.05, 0.05, 0.05, 0.1]), diff_step=1e-6, max_nfev=max_nfev, xtol=1e-10, ftol=1e-8)
    except ValueError:
        return Solution(False, evals=count[0])
    f = fly(orbit, clocks, r.x, dv_ms, tc_guess)
    ok = accept(f, w_target, escape_T, window_days, budget_days)
    return Solution(ok, r.x, f, count[0], float(np.linalg.norm(w_target)) if ok else 0.0)


def climb(orbit, clocks, seed, seed_speed, u, speed, dv_ms, escape_T, window_days, budget_days, step=0.15):
    """From a seed: first meet all conditions exactly at a speed the seed nearly has, then
    raise the speed along u step by step, each solve starting from the last, until `speed`
    is reached or a step fails (the step is halved twice before giving up)."""
    args = (dv_ms, escape_T, window_days, budget_days)
    best, evals = None, 0
    for start in (1.0, 0.6):
        v = min(seed_speed * start, speed)
        s = solve(orbit, clocks, seed, v * u, *args, max_nfev=30)
        evals += s.evals
        if s.ok:
            best = s
            break
    if best is None:
        return Solution(False, evals=evals)
    while best.speed < speed - 1e-9 and step >= 0.03 and not out_of_time():
        v = min(best.speed + step, speed)
        s = solve(orbit, clocks, (best.x, best.flown.encounter_days), v * u, *args)
        evals += s.evals
        if s.ok:
            best = s
        else:
            step /= 2
    best.evals = evals
    return best


class Cloud:
    """The stored escapes of one node orbit and burn size, as seeds."""

    def __init__(self, z, burn_ms: int, orbit_index: int, period_days: float):
        g = lambda k: np.asarray(z[f'{k}_{burn_ms}'], float)
        sel = g('orbit') == orbit_index
        self.period_days = period_days
        for k in ('vinf', 'lon', 'lat', 'days', 'moon', 'node', 'first_days', 'station', 'burn_place', 'burn_az', 'burn_up', 'burn_share', 'turn_frac', 'roll'):
            setattr(self, k, g(k)[sel])
        self.dir = direction(self.lon, self.lat).T  # (N, 3)
        self.moon_deg = np.degrees(self.moon) % 360.0

    def seeds(self, clocks: Clocks, u, speed: float, escape_T: float, window_days: float, budget_days: float, n: int = 4):
        """Up to n stored escapes to start from: near the wanted direction, with the three
        clocks near what they are on the day the escape's station place would put it, the
        fastest first. The match is widened once if nothing is found. Returns
        (settings, encounter time, speed) per seed."""
        ang = np.degrees(np.arccos(np.clip(self.dir @ u, -1, 1)))
        dT = wrap(self.station - float(clocks.place(escape_T)), 1.0) * self.period_days  # shift that matches the station
        Te = escape_T + dT
        dnode = np.abs(wrap(self.node - clocks.node(Te)))
        dmoon = np.abs(wrap(self.moon_deg - clocks.moon(Te)))
        base = (self.days <= budget_days) & (np.abs(dT) <= window_days) & (dnode < 45.0)
        for cone, moon in ((15.0, 20.0), (30.0, 40.0)):
            idx = np.nonzero(base & (ang < cone) & (dmoon < moon))[0]
            if len(idx):
                break
        if not len(idx):
            return []
        order = idx[np.argsort(-np.minimum(self.vinf[idx], speed) + 0.002 * ang[idx] + 0.002 * dmoon[idx])]
        best, seen = [], set()
        for i in order:  # skip near-copies of a seed already taken (same burn place, direction and encounter)
            key = (round(self.burn_place[i], 3), round(self.first_days[i]), round(self.burn_az[i], 2), round(self.burn_share[i], 2))
            if key not in seen:
                seen.add(key)
                best.append(i)
            if len(best) == n:
                break
        return [((Te[i] - self.days[i], self.burn_az[i], self.burn_share[i], self.burn_up[i], self.turn_frac[i], self.roll[i]), self.first_days[i], self.vinf[i]) for i in best]


def reachable(orbit: NodeOrbit, cloud: Cloud, clocks: Clocks, lon_deg, lat_deg, speed, dv_ms, escape_T, window_days, budget_days, n_seeds: int = 4,
              seconds: float = np.inf):
    """Most excess speed (km/s, up to `speed`) that can be delivered exactly in the wanted
    direction, over the seeds tried, within `seconds` of wall clock (a few solves stall in
    slow integrations; the best found by then is kept). Returns (speed or 0, best Solution
    or None, seeds tried, whether the time ran out)."""
    u = direction(lon_deg, lat_deg)
    best, runs = None, 0
    _deadline[0] = time.monotonic() + seconds
    try:
        for x, tc, v in cloud.seeds(clocks, u, speed, escape_T, window_days, budget_days, n_seeds):
            if out_of_time():
                break
            runs += 1
            s = climb(orbit, clocks, (x, tc), v, u, speed, dv_ms, escape_T, window_days, budget_days)
            if s.ok and (best is None or s.speed > best.speed):
                best = s
            if best is not None and best.speed >= speed - 0.005:
                break
        timed_out = out_of_time()
    finally:
        _deadline[0] = np.inf
    return (best.speed if best else 0.0), best, runs, timed_out
