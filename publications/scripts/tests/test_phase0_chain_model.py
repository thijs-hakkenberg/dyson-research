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


# --- second pass: optimised trajectories and replacements ---------------------------------

from dataclasses import replace  # noqa: E402

from phase0_chain_model import best_cycle, load_legs, optimised_cycles  # noqa: E402

OPT = ChainSettings(trajectory='optimised', lga=1.0, leg_cap=6.5, **SMALL)


def test_best_cycle_uses_only_legs_the_tug_can_fly():
    # columns: depart day, flight days, Δv km/s, thrust fraction
    g = {'out': np.array([[0.0, 200.0, 4.0, 0.5], [0.0, 100.0, 4.0, 0.9]]),
         'in': np.array([[400.0, 200.0, 4.0, 0.5], [170.0, 100.0, 6.0, 0.5]])}
    cyc, dvo, dvi = best_cycle(g, 6.5, 1.0, 1.0, 0.0)
    assert cyc == pytest.approx(270 / 365.25) and (dvo, dvi) == (4.0, 6.0)  # fast out, 60-day stay, fast back
    assert best_cycle(g, 5.0, 1.0, 1.0, 0.0)[0] == pytest.approx(600 / 365.25)  # the 6 km/s return is over the cap
    assert best_cycle(g, 5.0, 0.6, 1.0, 0.0)[0] == pytest.approx(600 / 365.25)  # weaker tug loses the hard-thrusting outbound leg
    assert best_cycle(g, 5.0, 0.3, 1.0, 0.0) is None
    assert best_cycle(g, 6.5, 1.0, 1.0, 1.0)[0] == pytest.approx((270 + 60) / 365.25)  # flyby phasing allowance


def test_optimised_targets_respect_limits_and_shrink_for_a_weaker_tug():
    assert len(load_legs()) > 50
    full = optimised_cycles(OPT, 54.0, 225.0, 2500.0)
    weak = optimised_cycles(replace(OPT, tug_power_mw=0.75), 54.0, 300.0, 3250.0)
    assert 0 < len(weak) < len(full)
    assert all(r[1] <= 4.0 and r[2] <= 6.5 and r[3] <= 6.5 for r in full)
    assert len(optimised_cycles(replace(OPT, leg_cap=5.0), 54.0, 225.0, 2500.0)) < len(full)


def test_lunar_flyby_lowers_propellant_and_import_ratio():
    none = simulate(BOM, replace(OPT, lga=0.0))
    fly = simulate(BOM, replace(OPT, lga=1.5, leg_cap=5.0))
    assert fly['propellant_t_per_yr']['P50'] < none['propellant_t_per_yr']['P50']
    assert fly['import_ratio']['P50'] < none['import_ratio']['P50']
    assert fly['targets_sampled'] > none['targets_sampled']


def test_replacements_cost_nothing_inside_service_life_and_add_cost_beyond_it():
    short = simulate(BOM, replace(OPT, replacements=True, ops_years=(6.25, 6.25)))
    assert short['replacement_cost_B']['P50'] == pytest.approx(0.0, abs=1e-9)
    kw = dict(ops_years=(20.0, 20.0))
    without = simulate(BOM, replace(OPT, **kw))
    with_r = simulate(BOM, replace(OPT, replacements=True, **kw))
    assert with_r['replacement_cost_B']['P50'] > 1.0
    assert with_r['per_kg_0B_with_contingency']['P50'] > without['per_kg_0B_with_contingency']['P50']
    assert with_r['import_ratio_with_replacements']['P50'] > with_r['import_ratio']['P50']
    assert without['import_ratio_with_replacements']['P50'] == pytest.approx(without['import_ratio']['P50'])


def test_fastest_targets_give_shorter_cycles():
    every = simulate(BOM, OPT)
    best = simulate(BOM, replace(OPT, target_fraction=0.25))
    assert best['cycle_years']['P50'] < every['cycle_years']['P50']
    assert best['fleet']['P50'] <= every['fleet']['P50']
