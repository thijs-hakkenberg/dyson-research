"""Tests for moon_gravity: the full-model check of the node-to-escape leg (rq-0-52)."""

import numpy as np
import pytest

import cislunar_flyby as c
import moon_gravity as mg
import node_leg_direct as d


@pytest.fixture
def moon():
    return mg.Moon(d.Clocks(0.0, 180.0), 1234.5)


def test_barycentre_stays_on_the_cr3bp_earth(moon):
    for t in (0.0, 0.3, 1.7):
        bary = (c.MU_EARTH * moon.earth(t) + c.MU_MOON * moon.pos(t)) / (c.MU_EARTH + c.MU_MOON)
        assert np.linalg.norm(bary - c.EARTH) * mg.KM < 1e-6
        assert np.linalg.norm(moon.pos(t) - moon.earth(t)) * mg.KM == pytest.approx(np.linalg.norm(c.moon_position(0.0, 0.0)) * mg.KM, rel=1e-9)


def test_far_away_the_split_earth_and_moon_pull_like_one_point(moon):
    """Millions of km out, the Earth and Moon either side of the barycentre pull like one point
    of their summed mass (the rest is a quadrupole, ~1e-3 of the whole at 3 million km)."""
    r = c.EARTH + np.array([0.0, 3e6, 4e5]) / mg.KM
    a, _ = mg._extra(0.2, r, moon)
    split = mg._pull(r - c.EARTH, c.MU) + a
    point = mg._pull(r - c.EARTH, c.MU + moon.mu)
    assert np.linalg.norm(split - point) / np.linalg.norm(point) < 1e-3


def test_gradient_matches_finite_differences(moon):
    r = moon.pos(0.4) + np.array([3000.0, -1500.0, 800.0]) / mg.KM
    _, G = mg._extra(0.4, r, moon)
    h = 1e-3 / mg.KM
    for k in range(3):
        e = np.zeros(3)
        e[k] = h
        num = (mg._extra(0.4, r + e, moon)[0] - mg._extra(0.4, r - e, moon)[0]) / (2 * h)
        assert np.allclose(G[:, k], num, rtol=1e-5, atol=1e-9 * np.max(np.abs(G)))


def test_perilune_has_the_hyperbola_distance_and_speed(moon):
    v = 1.2 / c.VU_KMS
    ui = np.array([1.0, 0.0, 0.0])
    turn = np.radians(40.0)
    uo = np.array([np.cos(turn), np.sin(turn), 0.0])
    s = mg.perilune(moon, 0.5, v * ui, v * uo)
    rp = moon.mu / v**2 * (1 / np.sin(turn / 2) - 1)
    rel = s[:3] - moon.pos(0.5)
    assert np.linalg.norm(rel) == pytest.approx(rp, rel=1e-9)
    vin = s[3:] + mg._spin(s[:3] - c.EARTH) - moon.vel(0.5) - mg._spin(moon.pos(0.5) - c.EARTH)
    assert np.linalg.norm(vin) == pytest.approx(np.sqrt(v**2 + 2 * moon.mu / rp), rel=1e-6)
    assert abs(rel @ vin) / (np.linalg.norm(rel) * np.linalg.norm(vin)) < 1e-6  # at perilune the velocity is square to the radius
