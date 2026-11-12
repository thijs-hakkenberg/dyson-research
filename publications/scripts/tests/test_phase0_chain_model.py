"""Tests for the Phase 0 chain-closure model (rq-0-61)."""

import numpy as np
import pytest

from phase0_chain_model import ChainSettings, load_cycles, simulate
from phase0_cost_risk import load_bom

BOM = load_bom()
SMALL = dict(n=6_000)


def test_catalogue_cycles_respect_the_limits():
    cyc, out, inn = load_cycles(6.5, 4.0)
    assert len(cyc) > 0
    assert (cyc <= 4.0).all()
    assert (out <= 6.5 + 1e-9).all() and (inn <= 6.5 + 1e-9).all()


def test_propellant_follows_the_rocket_equation():
    # Fixed inputs: 5 km/s legs, Isp 2,500 s, 54 t dry, 225 t payload, no cargo spread worth testing
    r = simulate(BOM, ChainSettings(trajectory='consensus', isp_s=(2500, 2500), tug_dry_t=(54, 54), payload_t=(225, 225), **SMALL))
    ve = 2500 * 9.80665 / 1e3
    m_in = (54 + 225) * (np.exp(5 / ve) - 1)
    lo = m_in + (54 + 0 + m_in) * (np.exp(5 / ve) - 1)
    hi = m_in + (54 + 20 + m_in) * (np.exp(5 / ve) - 1)
    p = r['propellant_per_cycle_t']
    assert lo - 1e-6 <= p['P10'] <= p['P90'] <= hi + 1e-6


def test_fleet_is_trips_times_cycle_plus_reserve():
    r = simulate(BOM, ChainSettings(trajectory='consensus', payload_t=(200, 200), product_t_per_yr=(1200, 1200), **SMALL))
    assert r['fleet']['P50'] == np.ceil(1200 / 200 * 3.0) + 2


def test_higher_isp_cuts_propellant():
    a = simulate(BOM, ChainSettings(**SMALL))['propellant_t_per_yr']['P50']
    b = simulate(BOM, ChainSettings(isp_s=(3000, 3500), **SMALL))['propellant_t_per_yr']['P50']
    assert b < a


def test_a_longer_run_lowers_cost_per_kg():
    short = simulate(BOM, ChainSettings(**SMALL))['per_kg_0B_with_contingency']['P50']
    long = simulate(BOM, ChainSettings(ops_years=(15, 15), **SMALL))['per_kg_0B_with_contingency']['P50']
    assert long < short


def test_earth_benchmark_is_launch_price_plus_material_with_contingency():
    e = simulate(BOM, ChainSettings(**SMALL))['earth_per_kg']
    assert 1800 * 1.2 + 50 < e['P10'] < e['P90'] < (4700 + 500) * 1.25
