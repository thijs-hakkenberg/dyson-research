"""Tests for the Fe-Ni process-route simulator (rq-0-56)."""

import numpy as np
import pytest

from smelting_sim import (
    G_EARTH, S_IN_FES, Design, beneficiate, draw_physics, evaluate, hr_velocity, h2_desulfurise,
    liquate, residual_saturation, rotor_ok, summarise,
)

PH = draw_physics(1500, 'H', seed=2)


def test_mass_is_conserved_through_every_route():
    for d in (Design(), Design(finish='sinter', h2=True), Design(liquation=True, liq_T=1300), Design(finish='carbonyl')):
        st = evaluate(d, PH)['state']
        # metal in product + metal lost = metal in the feed (Fe released from FeS can add a little)
        total = st['metal'] + st['lost_metal']
        assert (total >= PH.metal * 0.999).all()
        assert (total <= PH.metal + PH.fes).all()


def test_plain_melting_keeps_the_sulfur():
    # the bom-0-3 finding: melting dissolves troilite S into the metal, at any gravity
    lo = summarise(Design(melt_G=0.1), PH)['S_pct']['P50']
    hi = summarise(Design(melt_G=100), PH)['S_pct']['P50']
    assert lo > 0.5 and hi > 0.5
    assert hi == pytest.approx(lo, rel=0.05)


def test_h2_equilibrium_constant_is_small_and_rises_with_temperature():
    k = lambda T: np.exp(-(59_960.0 - 3.2 * T) / (8.314462 * T))
    assert 2e-3 < k(1173.15) < 5e-3
    assert k(1223.15) > k(1073.15)


def test_h2_removes_sulfur_and_longer_holds_remove_more():
    st0 = beneficiate(PH, Design(grind_um=100))
    a = h2_desulfurise(st0, PH, Design(grind_um=100, h2=True, h2_hours=6))
    b = h2_desulfurise(st0, PH, Design(grind_um=100, h2=True, h2_hours=60))
    assert (b['fes'] < a['fes']).all() and (a['fes'] < st0['fes']).all()
    # hydrogen make-up is 2 g per 32 g of sulfur, with a small margin
    s_removed = (st0['fes'] - b['fes']) * S_IN_FES
    assert np.allclose(b['imports'] - st0['imports'], s_removed * 2.016 / 32.06 * 1.2)


def test_residual_saturation_falls_with_capillary_number_and_is_continuous_enough():
    n = np.array([1e-4, 1e-2, 0.14, 1.0, 10.0])
    s = residual_saturation(n)
    assert (np.diff(s) < 0).all()
    assert 0.05 < s[2] < 0.1


def test_liquation_drains_more_at_higher_g_but_cannot_reach_the_envelope():
    low = summarise(Design(finish='sinter', liquation=True, liq_T=1300, liq_G=10), PH)['S_pct']['P50']
    high = summarise(Design(finish='sinter', liquation=True, liq_T=1300, liq_G=2000, rotor_r_m=0.2), PH)['S_pct']['P50']
    assert high <= low
    assert high > 0.10


def test_settling_velocity_scales_with_g_and_radius_squared():
    v1 = hr_velocity(4200, G_EARTH, 50e-6, 1.0, 0.006)
    assert hr_velocity(4200, 10 * G_EARTH, 50e-6, 1.0, 0.006) == pytest.approx(10 * v1)
    assert hr_velocity(4200, G_EARTH, 100e-6, 1.0, 0.006) == pytest.approx(4 * v1)


def test_melt_purity_improves_with_gravity():
    lo = summarise(Design(h2=True, h2_hours=96, grind_um=100, melt_G=0.001), PH)['purity_pct']
    hi = summarise(Design(h2=True, h2_hours=96, grind_um=100, melt_G=1.0), PH)['purity_pct']
    assert hi > lo


def test_carbonyl_product_is_sulfur_free_and_yield_rises_with_time_and_pressure():
    a = summarise(Design(finish='carbonyl', carb_hours=48, carb_P_bar=80), PH)
    b = summarise(Design(finish='carbonyl', carb_hours=168, carb_P_bar=200), PH)
    assert a['S_pct']['P90'] == 0 and b['yield']['P50'] > a['yield']['P50']


def test_rotor_limit_rejects_large_fast_hot_rotors():
    assert rotor_ok(Design(melt_G=10, rotor_r_m=0.5))
    assert not rotor_ok(Design(melt_G=3000, rotor_r_m=3.0))


def test_open_vacuum_melting_evaporates_more_iron_than_a_lidded_crucible():
    o = evaluate(Design(enclosure='open', melt_minutes=60), PH)['state']['evap_loss']
    c = evaluate(Design(enclosure='lidded', melt_minutes=60), PH)['state']['evap_loss']
    assert (o > c).all()
