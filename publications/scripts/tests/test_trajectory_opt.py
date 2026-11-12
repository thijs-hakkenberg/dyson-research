"""Tests for the second-pass trajectory model (rq-0-52)."""

import os
import sys
import warnings

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from nea_accessibility import GM, KMS, jd, lambert  # noqa: E402
from trajectory_opt import (REV_OPTIONS, impulsive_tables, lambert_multirev, low_thrust_leg, propagate,  # noqa: E402
                            seed_velocities)

warnings.simplefilter('ignore')


def circ(a, th):
    v = np.sqrt(GM / a)
    return np.array([a * np.cos(th), a * np.sin(th), 0.0]), np.array([-v * np.sin(th), v * np.cos(th), 0.0])


def test_propagate_returns_after_one_period():
    r, v = circ(1.2, 0.7)
    v = v * 1.1 + np.array([0, 0, 0.001])
    a = 1 / (2 / np.linalg.norm(r) - v @ v / GM)
    P = 2 * np.pi * np.sqrt(a**3 / GM)
    r2, v2 = propagate(r[None], v[None], np.array([P]))
    assert np.allclose(r2[0], r, atol=1e-9) and np.allclose(v2[0], v, atol=1e-11)
    rb, vb = propagate(*propagate(r[None], v[None], np.array([137.0])), np.array([-137.0]))
    assert np.allclose(rb[0], r, atol=1e-9)


@pytest.mark.parametrize('nrev,branch', [(1, 0), (1, 1), (2, 0), (2, 1)])
def test_multirev_lambert_hits_the_target_with_the_right_revolution_count(nrev, branch):
    ang = np.array([0.5, 1.5, 4.5, 5.5])
    r1 = np.tile([1.0, 0.0, 0.0], (4, 1))
    r2 = np.stack([1.3 * np.cos(ang), 1.3 * np.sin(ang), np.full(4, 0.05)], 1)
    tof = np.full(4, 400.0 * nrev + 250)
    v1, v2 = lambert_multirev(r1, r2, tof, nrev, branch)
    assert np.isfinite(v1).all()
    rp, vp = propagate(r1, v1, tof)
    assert np.abs(rp - r2).max() < 1e-8 and np.abs(vp - v2).max() < 1e-9
    a = 1 / (2 / 1.0 - np.sum(v1 * v1, -1) / GM)
    revs = tof / (2 * np.pi * np.sqrt(a**3 / GM))
    assert np.all((revs > nrev) & (revs < nrev + 1))


def test_multirev_lambert_is_nan_below_the_minimum_time():
    r1, r2 = np.array([[1.0, 0, 0]]), np.array([[0.0, 1.3, 0.02]])
    v1, _ = lambert_multirev(r1, r2, np.array([300.0]), 2, 0)
    assert np.isnan(v1).all()


def hohmann_like():
    r0, v0 = circ(1.0, 0.0)
    rf, vf = circ(1.1, np.pi - 0.15)
    tof = 190.0
    v1, v2 = lambert(r0[None], rf[None], np.array([tof]))
    imp = (np.linalg.norm(v1[0] - v0) + np.linalg.norm(vf - v2[0])) * KMS
    return r0, v0, rf, vf, tof, (v1[0], v2[0]), imp


def test_low_thrust_approaches_impulsive_at_high_thrust_and_costs_more_at_low_thrust():
    r0, v0, rf, vf, tof, seed, imp = hohmann_like()
    hi = low_thrust_leg(r0, v0, rf, vf, tof, 5e-3, seed=seed)
    lo = low_thrust_leg(r0, v0, rf, vf, tof, 4.2e-4, seed=seed)
    assert hi.ok and lo.ok
    assert imp * 0.98 < hi.dv_kms < imp * 1.08
    assert lo.dv_kms > hi.dv_kms
    assert lo.mismatch < 2e-5 and 0 < lo.thrust_fraction <= 1.0


def test_low_thrust_reports_an_underpowered_leg_as_infeasible():
    r0, v0, rf, vf, tof, seed, _ = hohmann_like()
    assert not low_thrust_leg(r0, v0, rf, vf, tof, 2.2e-4, seed=seed).ok
    assert not low_thrust_leg(r0, v0, rf, vf, tof, 5e-5, seed=seed).ok


def test_lunar_assist_credit_reduces_thruster_dv_and_respects_its_limit():
    r0, v0, rf, vf, tof, seed, _ = hohmann_like()
    base = low_thrust_leg(r0, v0, rf, vf, tof, 4.2e-4, seed=seed)
    lga = low_thrust_leg(r0, v0, rf, vf, tof, 4.2e-4, seed=seed, free_end='start', lga_vinf_kms=0.5)
    assert lga.ok and lga.dv_kms < base.dv_kms - 0.3
    assert lga.vinf_kms <= 0.5 + 1e-3


def test_impulsive_tables_improve_with_revolutions_and_credit():
    el = {'a': np.array([1.12]), 'e': np.array([0.08]), 'i': np.array([2.0]), 'om': np.array([40.0]), 'w': np.array([100.0]),
          'ma': np.array([10.0]), 'epoch': np.array([jd(2030.0)])}
    t_dep = np.arange(jd(2030.0), jd(2032.0), 60.0)
    tofs = np.array([200.0, 400.0, 700.0, 950.0])
    zero = impulsive_tables(el, t_dep, tofs, True, credits=(0.0, 1.0), revs=((0, 0),))
    full = impulsive_tables(el, t_dep, tofs, True, credits=(0.0, 1.0))
    assert np.all(full[0.0][0] <= zero[0.0][0] + 1e-12)
    assert full[0.0][0].min() < zero[0.0][0][:, :, 2:].min()  # long legs gain from extra revolutions
    assert full[1.0][0].min() < full[0.0][0].min()
    # the recorded revolution option reproduces the tabulated Δv
    dv, which = full[0.0]
    d, t = np.unravel_index(np.argmin(dv[0]), dv[0].shape)
    el1 = {k: float(v[0]) for k, v in el.items()}
    r1, vs1, r2, vs2, v1, v2 = seed_velocities(el1, t_dep[d], tofs[t], True, False, int(which[0, d, t]))
    again = (np.linalg.norm(v1 - vs1) + np.linalg.norm(vs2 - v2)) * KMS
    assert again == pytest.approx(dv[0, d, t], rel=1e-6)
    assert REV_OPTIONS[0] == (0, 0)
