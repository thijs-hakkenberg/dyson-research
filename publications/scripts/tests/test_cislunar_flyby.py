"""Tests for the three-body lunar-flyby model (rq-0-52 third pass)."""

import json
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.dirname(__file__))

import cislunar_flyby as c  # noqa: E402
from trajectory_opt import FlybyReach, low_thrust_leg  # noqa: E402


def jacobi(y):
    x, yy, z, vx, vy, vz = y.T
    r1 = np.sqrt((x + c.MU) ** 2 + yy**2 + z**2)
    r2 = np.sqrt((x - 1 + c.MU) ** 2 + yy**2 + z**2)
    return x**2 + yy**2 + 2 * (1 - c.MU) / r1 + 2 * c.MU / r2 - (vx**2 + vy**2 + vz**2)


@pytest.fixture(scope='module')
def departures():
    return c.node_departures(100e3, 4, 6, 150.0)


def test_l1_is_about_one_and_a_half_million_km_sunward():
    assert (1 - c.MU - c.l1_x()) * c.AU_KM == pytest.approx(1.4916e6, rel=2e-3)


def test_node_orbit_closes_and_has_the_known_period():
    x0, period = c.lyapunov_orbit(100e3)
    from scipy.integrate import solve_ivp
    end = solve_ivp(c._f1, (0, period), x0, method='DOP853', rtol=1e-12, atol=1e-13).y[:, -1]
    assert np.abs(end - x0).max() < 1e-8
    assert 170 < period * c.TU_DAYS < 185


def test_integrator_conserves_the_jacobi_constant_and_finds_the_moons_distance(departures):
    y, _ = departures
    f = c.integrate(y, 0.0, 120 * c.DAY, crossings=4)
    assert np.abs(jacobi(f.y) - jacobi(y)).max() < 1e-8
    hit = f.n_cross > 0
    assert hit.any()
    r = np.linalg.norm(f.y_cross[hit, 0, :3] - c.EARTH, axis=1)
    assert np.allclose(r, c.A_MOON, rtol=1e-7)


def test_a_bigger_node_burn_reaches_the_moon_sooner():
    first = {}
    for dv in (50.0, 300.0):
        f = c.integrate(c.node_departures(20e3, 2, 12, dv)[0], 0.0, 200 * c.DAY, crossings=1)
        first[dv] = np.nanmin(f.t_cross[:, 0]) * c.TU_DAYS
    assert first[300.0] < 35 < 60 < first[50.0]


def test_swingby_keeps_the_moon_relative_speed_and_is_limited_in_turn():
    v = np.array([[0.02, 0.01, 0.0], [0.03, -0.02, 0.0]])
    out = c.turn(v, np.array([0.4, 1.0]), np.array([0.0, np.pi / 2]))
    assert np.allclose(np.linalg.norm(out, axis=1), np.linalg.norm(v, axis=1))
    assert np.allclose(np.arccos((out * v).sum(1) / (np.linalg.norm(v, axis=1) ** 2)), [0.4, 1.0])
    assert out[0, 2] == pytest.approx(0.0) and abs(out[1, 2]) > 0  # roll 0 stays in the ecliptic
    slow, fast = c.max_turn(np.array([0.5, 1.5]) / c.VU_KMS)
    assert np.radians(60) < fast < slow < np.radians(180)


def test_one_swingby_gives_escape_speeds_in_the_published_range(departures):
    y, _ = departures
    f = c.integrate(y, 0.0, 150 * c.DAY, crossings=2)
    rows = np.nonzero(f.n_cross > 0)[0]
    yc, tc = f.y_cross[rows, 0], f.t_cross[rows, 0]
    fan, idx = c.swingby_fan(yc, 6, 7)
    e = c.integrate(fan, tc[idx], 220 * c.DAY)
    v, lon, lat, c3 = c.escape_state(e.y[e.status == 1])
    assert 1.2 < v.max() < 1.9  # literature: 1.4–1.6 km/s from one swingby
    assert np.abs(lat).max() < 75


def test_reach_table_interpolates_and_mirrors_for_arrivals(tmp_path):
    table = np.zeros((12, 5))
    table[6, 0] = 1.6  # longitude bin 0..30°, in plane
    path = tmp_path / 'reach.json'
    json.dump({'lon_edges': list(range(-180, 181, 30)), 'lat_edges': [0, 15, 30, 45, 60, 90], 'budgets_days': [90],
               'vinf_kms': {'150': {'90': table.tolist()}}}, open(path, 'w'))
    r = FlybyReach(str(path), 150, 90)
    earth = np.array([1.0, 0.0, 0.0])  # Sun→Earth along x, Earth moving along y
    w = np.array([np.cos(np.radians(15)), np.sin(np.radians(15)), 0.0])
    assert r.cap(w, earth, False) == pytest.approx(1.6)
    assert r.cap(w, earth, True) < 0.1  # the same vector as an arrival maps to longitude 165°
    assert r.cap(np.array([-w[0], w[1], 0.0]), earth, True) == pytest.approx(1.6)
    assert 0 < r.cap(np.array([np.cos(np.radians(30)), np.sin(np.radians(30)), 0.0]), earth, False) < 1.6
    assert r.cap(np.array([w[0], w[1], 2.0]), earth, False) == pytest.approx(0.0)


def test_leg_optimiser_respects_a_direction_limited_credit(tmp_path):
    from test_trajectory_opt import hohmann_like

    r0, v0, rf, vf, tof, seed, _ = hohmann_like()
    lon_edges, lat_edges = list(range(-180, 181, 30)), [0, 15, 30, 45, 60, 90]

    def reach(value):
        path = tmp_path / f'reach{value}.json'
        json.dump({'lon_edges': lon_edges, 'lat_edges': lat_edges, 'budgets_days': [90],
                   'vinf_kms': {'150': {'90': np.full((12, 5), value).tolist()}}}, open(path, 'w'))
        return FlybyReach(str(path), 150, 90)

    flat = low_thrust_leg(r0, v0, rf, vf, tof, 4.2e-4, seed=seed, free_end='start', lga_vinf_kms=0.5)
    same = low_thrust_leg(r0, v0, rf, vf, tof, 4.2e-4, seed=seed, free_end='start', reach=reach(0.5))
    none = low_thrust_leg(r0, v0, rf, vf, tof, 4.2e-4, seed=seed, free_end='start', reach=reach(0.0))
    base = low_thrust_leg(r0, v0, rf, vf, tof, 4.2e-4, seed=seed)
    assert same.ok and same.dv_kms == pytest.approx(flat.dv_kms, abs=0.05)
    assert none.ok and none.vinf_kms < 2e-3 and none.dv_kms == pytest.approx(base.dv_kms, abs=0.05)


def test_launch_to_moon_reach_matches_the_published_single_flyby_range(tmp_path, monkeypatch):
    import run_scout_flyby_model as s

    monkeypatch.setattr(s, 'REACH_LAUNCH', str(tmp_path / 'reach-launch.json'))
    monkeypatch.setattr(s, 'LAUNCH_C3', (-1.0,))
    tab, e = s.launch_reach()
    assert 1.2 < e['vinf'].max() < 1.8  # Casalino and Filizola 2017: 1.2–1.4 km/s verified
    assert np.median(tab[:, 0]) > np.median(tab[:, 2])  # less reach out of the ecliptic
    assert e['days'].max() < 60
