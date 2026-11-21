"""Multi-burn phasing on the node orbit (node_phasing_multi.py)."""

import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import node_leg_direct as d  # noqa: E402
import node_phasing as ph  # noqa: E402
import node_phasing_multi as pm  # noqa: E402


@pytest.fixture(scope='module')
def orbit():
    return d.NodeOrbit('halo', 120e3)


def test_derivatives_match_finite_differences(orbit):
    t = pm.Transfer(orbit, 0.1, 0.125, 90.0, 3)
    z = np.random.default_rng(1).normal(size=t.n) * 0.3
    _, g = t.cost(z)
    e = np.eye(t.n) * 1e-6
    gn = np.array([(t.cost(z + x)[0] - t.cost(z - x)[0]) / 2e-6 for x in e])
    jn = np.array([(t.joins(z + x) - t.joins(z - x)) / 2e-6 for x in e]).T
    assert np.max(np.abs(g - gn)) < 1e-3
    assert np.max(np.abs(t.joins_jac(z) - jn)) < 1e-3


def test_one_coast_is_the_two_burn_transfer(orbit):
    two = ph.transfer(orbit, 0.0, 0.125, 60.0)[0]
    sol = pm.Transfer(orbit, 0.0, 0.125, 60.0, 1).solve()
    assert sol['miss_km'] < 1e-3 and abs(sol['total_ms'] - two) < 0.1


def test_more_burns_cost_less_but_not_much(orbit):
    two = pm.Transfer(orbit, 0.0, 0.125, 120.0, 1).solve()['total_ms']
    many, sol = pm.phasing(orbit, 0.0, 0.125, 120.0, coast_days=30.0)
    assert len(sol['burns_ms']) == 5 and sol['miss_km'] < 1.0
    assert 0.5 * two < many < two
