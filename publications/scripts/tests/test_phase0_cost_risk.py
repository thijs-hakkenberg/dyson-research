"""Tests for the Phase 0 cost-confidence model (rq-0-84)."""

import numpy as np
import pytest

from phase0_cost_risk import Settings, _lognormal, load_bom, simulate, Z90


def test_lognormal_envelope_ends_are_p10_and_p90():
    u = np.array([0.1, 0.5, 0.9])
    x = _lognormal(u, 2.0, 8.0, Z90)
    assert x[0] == pytest.approx(2.0)
    assert x[1] == pytest.approx(4.0)  # geometric midpoint
    assert x[2] == pytest.approx(8.0)


def test_envelope_only_median_sits_inside_the_bom_range():
    bom = load_bom()
    r = simulate(bom, Settings(n=20_000))
    base = bom['totals']['base']
    assert base['a']['min'] < r['0A']['P50'] < base['a']['max']
    assert base['b']['min'] < r['0B']['P50'] < base['b']['max']


def test_correlation_widens_the_tail():
    bom = load_bom()
    lo = simulate(bom, Settings(rho=0.0, n=40_000))['0A']
    hi = simulate(bom, Settings(rho=0.5, n=40_000))['0A']
    assert hi['P90'] - hi['P10'] > lo['P90'] - lo['P10']


def test_growth_lowers_the_confidence_of_the_funded_figure():
    bom = load_bom()
    plain = simulate(bom, Settings(n=20_000))['0A']['confidence_of_funded']
    grown = simulate(bom, Settings(n=20_000, growth=(1.3, 2.0)))['0A']['confidence_of_funded']
    assert grown < plain


def test_longer_0a_raises_run_rate_lines():
    bom = load_bom()
    short = simulate(bom, Settings(n=20_000, duration_years=(4, 4)))['0A']['P50']
    long = simulate(bom, Settings(n=20_000, duration_years=(12, 12)))['0A']['P50']
    assert long > short
