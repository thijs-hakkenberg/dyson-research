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


# ----------------------------------------------------------------------------- halo orbits, inclined Moon

@pytest.fixture(scope='module')
def halo():
    return c.halo_orbit(120e3)


def test_halo_orbit_closes_and_is_out_of_plane(halo):
    from scipy.integrate import solve_ivp

    s, period = halo
    sol = solve_ivp(c._f1, (0, period), s, method='DOP853', rtol=1e-12, atol=1e-13)
    assert np.abs(sol.y[:, -1] - s).max() < 1e-9
    assert period * c.TU_DAYS == pytest.approx(177.9, abs=0.5)  # the SOHO-class halo
    assert sol.y[2].max() * c.AU_KM == pytest.approx(120e3, rel=1e-6)
    assert sol.y[2].min() < 0 < sol.y[2].max()
    assert 600e3 < np.abs(sol.y[1]).max() * c.AU_KM < 720e3


def test_moon_geometry():
    node, u = np.radians([0.0, 40.0, 200.0]), np.radians([10.0, 95.0, 300.0])
    p = c.moon_position(node, u)
    n = c.moon_normal(node)
    assert np.allclose(np.linalg.norm(p, axis=1), c.A_MOON)
    assert np.allclose(np.sum(p * n, axis=1), 0.0, atol=1e-18)
    assert np.allclose(np.linalg.norm(n, axis=1), 1.0)
    # highest above the ecliptic a quarter of an orbit after the ascending node
    assert c.moon_position(0.3, np.pi / 2)[2] == pytest.approx(c.A_MOON * np.sin(c.INC_MOON))
    # no inclination: the planar Moon at longitude node + u
    flat = c.moon_position(node, u, inc=0.0)
    assert np.allclose(flat[:, 2], 0.0)
    assert np.allclose(np.arctan2(flat[:, 1], flat[:, 0]), c._wrap(node + u))


def test_plane_miss_follows_the_node_line():
    # a point on the Moon's orbit stays in the plane only at the right time
    node0, t = 1.1, 0.4
    p = c.moon_position(node0 - t, 2.0)
    y = np.concatenate([c.EARTH + p, np.zeros(3)])[None, :]
    assert c.plane_miss(y, np.array([t]), node0)[0] == pytest.approx(0.0, abs=1e-15)
    assert abs(c.plane_miss(y, np.array([t + 0.5]), node0)[0]) > 1e-5


def test_inclined_encounters_lie_in_the_moons_plane(halo):
    s, period = halo
    base = np.repeat(c.orbit_points(s, period, 4), 6, axis=0)
    az = np.tile(np.arange(6) * np.pi / 3, 4)
    ups = np.linspace(-1, 1, 7) * np.sqrt(1 - 0.9**2)
    node0 = 0.7
    ce, el, yc, tc = c.encounters_inclined(base, az, ups, 300.0, node0, 150 * c.DAY)
    assert len(ce) > 5
    assert np.abs(c.plane_miss(yc, tc, node0)).max() * c.AU_KM < 300.0
    assert np.allclose(np.linalg.norm(yc[:, :3] - c.EARTH, axis=1), c.A_MOON, rtol=1e-6)
    assert np.all(np.abs(el) <= np.sqrt(1 - 0.9**2) + 1e-12)  # the whole burn stays within 300 m/s
    # re-flying the solved burn reaches the same place
    k = 0
    f = c.integrate(c.burn_states(base[ce[k]][None], az[ce[k]][None], el[k][None], 300.0), 0.0, tc[k] + c.DAY, crossings=12)
    j = np.nanargmin(np.abs(f.t_cross[0] - tc[k]))
    assert np.allclose(f.y_cross[0, j], yc[k], atol=1e-7)


def test_inclined_swingby_keeps_the_excess_speed(halo):
    s, period = halo
    base = np.repeat(c.orbit_points(s, period, 4), 6, axis=0)
    az = np.tile(np.arange(6) * np.pi / 3, 4)
    node0 = 0.7
    ce, el, yc, tc = c.encounters_inclined(base, az, np.linspace(-1, 1, 7) * np.sqrt(1 - 0.9**2), 300.0, node0, 150 * c.DAY)
    vinf, vm, _ = c.encounter_vinf_inclined(yc, tc, node0)
    assert np.allclose(np.linalg.norm(vm, axis=1), c.V_MOON)
    rho = yc[:, :3] - c.EARTH
    assert np.allclose(np.sum(vm * rho, axis=1), 0.0, atol=1e-12)
    assert np.abs(vm[:, 2]).max() > 0.02 * c.V_MOON  # the Moon moves out of the ecliptic
    fan, src = c.swingby_fan_inclined(yc, tc, node0, 3, 4)
    v2, _, _ = c.encounter_vinf_inclined(fan, tc[src], node0)
    assert np.allclose(np.linalg.norm(v2, axis=1), np.linalg.norm(vinf[src], axis=1), rtol=1e-9)
    assert np.allclose(fan[:, :3], yc[src, :3])


def test_reach_table_with_node_angle(tmp_path):
    from trajectory_opt import moon_node_angle

    lat = [-90.0, -30.0, 0.0, 30.0, 90.0]
    tab = np.zeros((4, 12, 4))
    for k in range(4):
        tab[k] = 1.0 + 0.1 * k
    tab[1, :, 3] = 1.9  # node bin 90-180, northern high latitudes
    p = tmp_path / 'reach.json'
    json.dump({'lon_edges': list(np.arange(-180.0, 181.0, 30.0)), 'lat_edges': lat, 'node_edges': [0.0, 90.0, 180.0, 270.0, 360.0],
               'budgets_days': [90], 'vinf_kms': {'150': {'90': tab.tolist()}}}, open(p, 'w'))
    with pytest.raises(ValueError):
        FlybyReach(str(p), 150, 90)
    r = FlybyReach(str(p), 150, 90, node_deg=135.0)
    assert r.signed
    assert r.cap_at(0.0, 60.0) == pytest.approx(1.9)
    assert r.cap_at(0.0, -60.0) == pytest.approx(1.1)
    # between bin centres, and round the end of the circle
    assert FlybyReach(str(p), 150, 90, node_deg=90.0).cap_at(0.0, -60.0) == pytest.approx(1.05)
    assert FlybyReach(str(p), 150, 90, node_deg=0.0).cap_at(0.0, -60.0) == pytest.approx(1.15)
    # an arrival reads the mirror image: node 180° − node, and the velocity's z reversed
    arr = FlybyReach(str(p), 150, 90, node_deg=45.0, inbound=True)
    x = np.array([1.0, 0.0, 0.0])
    w_up = np.array([0.3, 0.2, 0.9])
    lon, la = arr.angles(w_up, x, True)
    assert la < 0 and lon == pytest.approx(np.degrees(np.arctan2(0.2, -0.3)))
    assert arr.cap(-w_up * np.array([1, -1, 1]), x, True) == pytest.approx(1.9)
    # node longitude 125.04° at J2000, seen from an Earth at longitude 100°
    e = np.array([np.cos(np.radians(100.0)), np.sin(np.radians(100.0)), 0.0])
    assert moon_node_angle(2451545.0, e) == pytest.approx(25.0445)
    assert moon_node_angle(2451545.0 + 365.25, e) == pytest.approx(25.0445 - 19.341, abs=0.01)
