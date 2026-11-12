"""Tests for the NEA joint-accessibility screen (rq-0-52)."""

import numpy as np
import pytest

from nea_accessibility import (
    GM,
    KMS,
    Criteria,
    earth_state,
    jd,
    kepler_state,
    lambert,
    metal_plausible,
    screen,
)


def test_earth_state_is_one_au_and_30_kms():
    r, v = earth_state(jd(2030.0))
    assert np.linalg.norm(r) == pytest.approx(1.0, abs=0.02)
    assert np.linalg.norm(v) * KMS == pytest.approx(29.8, abs=0.6)


def test_kepler_circular_period():
    t0 = jd(2030.0)
    r0, _ = kepler_state(1.0, 0.0, 0.0, 0.0, 0.0, 0.0, t0, t0)
    r1, _ = kepler_state(1.0, 0.0, 0.0, 0.0, 0.0, 0.0, t0, t0 + 2 * np.pi / np.sqrt(GM))
    assert np.allclose(r0, r1, atol=1e-9)


def test_lambert_recovers_a_propagated_orbit():
    t0 = jd(2031.0)
    el = (1.3, 0.2, 3.0, 40.0, 70.0, 10.0, t0)
    r1, v1 = kepler_state(*el, t0)
    r2, v2 = kepler_state(*el, t0 + 150.0)
    lv1, lv2 = lambert(r1[None], r2[None], np.array([150.0]))
    assert np.allclose(lv1[0], v1, rtol=1e-5)
    assert np.allclose(lv2[0], v2, rtol=1e-5)


def test_hohmann_like_transfer_costs_what_it_should():
    # Earth (1 AU) to a coplanar circular 1.2 AU orbit: Hohmann 1.32 + 1.27 = 2.59 km/s
    t0 = jd(2032.0)
    r1 = np.array([[1.0, 0.0, 0.0]])
    tof = np.pi * np.sqrt(1.1**3 / GM)
    r2 = np.array([[-1.2, -1e-4, 0.0]])
    v1, v2 = lambert(r1, r2, np.array([tof]))
    vc1 = np.sqrt(GM / 1.0)
    vc2 = np.sqrt(GM / 1.2)
    dv = (np.linalg.norm(v1[0] - [0, vc1, 0]) + np.linalg.norm([0, -vc2, 0] - v2[0])) * KMS
    assert dv == pytest.approx(2.59, abs=0.02)


def test_earth_like_orbit_is_cheap_and_cycles_inside_three_years():
    # An asteroid on a near-Earth orbit should be both scout- and tug-accessible
    el = {'a': np.array([1.05]), 'e': np.array([0.04]), 'i': np.array([1.0]), 'om': np.array([30.0]),
          'w': np.array([60.0]), 'ma': np.array([40.0]), 'epoch': np.array([jd(2030.0)])}
    r = screen(el, Criteria(dep_step_days=30), leg_caps=(5.0,))
    assert r.scout_dv[0.0][0] < 3.5
    assert r.cycle_years[5.0][0] <= 3.0
    # launch energy can only help the scout
    assert r.scout_dv[3.16][0] <= r.scout_dv[0.0][0]


def test_high_inclination_orbit_is_not_accessible():
    el = {'a': np.array([1.3]), 'e': np.array([0.3]), 'i': np.array([25.0]), 'om': np.array([30.0]),
          'w': np.array([60.0]), 'ma': np.array([40.0]), 'epoch': np.array([jd(2030.0)])}
    r = screen(el, Criteria(dep_step_days=40), leg_caps=(5.0,))
    assert r.scout_dv[0.0][0] > 3.5
    assert not np.isfinite(r.cycle_years[5.0][0])


def test_known_targets_match_mission_experience():
    # Ryugu and Itokawa from a standing start at SEL1 cost ~4–5 km/s impulsive per direct leg;
    # Hayabusa/Hayabusa2 needed launch C3 plus an Earth flyby. Elements: JPL SBDB, epoch 2026.
    t_dep = np.arange(jd(2030), jd(2040), 10.0)
    tofs = np.arange(60, 1000, 20.0)
    from nea_accessibility import leg_table
    ryugu = {'a': np.array([1.191]), 'e': np.array([0.1911]), 'i': np.array([5.87]), 'om': np.array([251.29]),
             'w': np.array([211.6]), 'ma': np.array([0.0]), 'epoch': np.array([jd(2026.5)])}
    d, a = leg_table(ryugu, t_dep, tofs, True)
    assert 3.8 < (d + a).min() < 5.5


def test_metal_plausible_taxonomy():
    assert metal_plausible('Sq') is True
    assert metal_plausible('Xe') is True
    assert metal_plausible('C') is False
    assert metal_plausible('') is None
