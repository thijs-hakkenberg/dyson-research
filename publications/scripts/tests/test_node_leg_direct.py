"""The node-to-escape leg solved one tug leg at a time (node_leg_direct.py)."""

import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import cislunar_flyby as c  # noqa: E402
import node_leg_direct as d  # noqa: E402


@pytest.fixture(scope='module')
def case():
    """One escape from the batch model, with clocks set so that it is exact on day 1000."""
    orbit = d.NodeOrbit('halo', 120e3)
    place, az, share, dv, node0, T = 0.25, np.array([0.5 + k * 0.4 for k in range(8)]), 0.8, 300.0, np.radians(60.0), 1000.0
    base = np.repeat(orbit.at(place)[None, :], len(az), axis=0)
    ups = np.linspace(-1, 1, 9) * np.sqrt(1 - share**2)
    ce, el, yc, tc = c.encounters_inclined(base, az, ups, dv, node0, 170 * c.DAY, inplane=share)
    assert len(ce)
    fan, src = c.swingby_fan_inclined(yc, tc, node0, 2, 4)
    f = c.integrate(fan, tc[src], 220 * c.DAY)
    v, lon, lat, c3 = c.escape_state(f.y)
    k = int(np.argmax(np.where((f.status == 1) & (c3 > 0), v, 0)))
    j = src[k]
    nf = 1 + 2 * 4
    frac = np.concatenate([[0.0], np.repeat([0.5, 1.0], 4)])[k % nf]
    roll = np.concatenate([[0.0], np.tile(np.arange(4) * np.pi / 2, 2)])[k % nf]
    _, _, at = c.encounter_vinf_inclined(yc[j : j + 1], tc[j : j + 1], node0)
    clocks = d.Clocks((place - T / orbit.period_days) % 1.0, orbit.period_days, node0=np.degrees(node0) - d.NODE_RATE * T,
                      moon0=np.degrees(at[0]) - d.MOON_RATE * (T + tc[j] * c.TU_DAYS))
    x = np.array([T, az[ce[j]], share, el[j], frac, roll])
    return orbit, clocks, x, tc[j] * c.TU_DAYS, v[k] * d.direction(lon[k], lat[k]), f.t[k] * c.TU_DAYS, dv


def test_clocks_and_their_mirror_image():
    k = d.Clocks(0.125, 177.87)
    assert float(k.place(177.87 * 2.5)) == pytest.approx(0.625)
    assert float(k.moon(29.530589)) == pytest.approx(float(k.moon(0.0)), abs=0.01)  # one synodic month
    assert float(d.wrap(k.node(346.62) - k.node(0.0))) == pytest.approx(0.0, abs=0.05)  # one eclipse year
    m = k.mirrored()
    for T in (0.0, 123.4):
        assert float(m.place(-T)) == pytest.approx((-float(k.place(T))) % 1.0)
        assert float(d.wrap(m.node(-T) - (180.0 - k.node(T)))) == pytest.approx(0.0, abs=1e-9)
        assert float(d.wrap(m.moon(-T) + k.moon(T))) == pytest.approx(0.0, abs=1e-9)


def test_single_flight_reproduces_the_batch_model(case):
    orbit, clocks, x, tc, w, days, dv = case
    f = d.fly(orbit, clocks, x, dv, tc)
    assert f.ok and abs(f.plane_km) < 400 and abs(f.moon_km) < 1.0
    assert np.linalg.norm(f.w - w) * 1e3 < 2.0
    assert f.flight_days == pytest.approx(days, abs=0.01)
    assert f.escape_T == pytest.approx(1000.0 + days, abs=0.01)


def test_solver_recovers_a_reachable_excess_velocity_and_refuses_an_unreachable_one(case):
    orbit, clocks, x, tc, w, days, dv = case
    f = d.fly(orbit, clocks, x, dv, tc)
    start = x + np.array([0.3, 0.02, 0.0, 0.01, -0.05, 0.05])
    s = d.solve(orbit, clocks, (start, tc), 0.97 * f.w, dv, f.escape_T, 5.0, days + 5.0, max_nfev=40)
    assert s.ok and abs(s.flown.plane_km) < d.TOL['plane_km'] and abs(s.flown.moon_km) < d.TOL['moon_km']
    assert np.linalg.norm(s.flown.w - 0.97 * f.w) * 1e3 < d.TOL['direction_ms']
    assert s.flown.burn_frac <= 1.0 + 1e-4 and 0.0 <= s.x[4] <= 1.0
    # twice the speed is beyond any swingby of this approach
    assert not d.solve(orbit, clocks, (x, tc), 2.0 * f.w, dv, f.escape_T, 5.0, days + 5.0).ok
    # nor is the same velocity available when the escape must fall a month away
    assert not d.solve(orbit, clocks, (x, tc), 0.97 * f.w, dv, f.escape_T + 30.0, 5.0, days + 5.0).ok
