"""Scout launch trade: mass, perigee kick and launcher capacity models."""

import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import scout_launch_trade as m


@pytest.mark.parametrize('s', m.SCOUTS, ids=lambda s: s.name)
def test_design_point_reproduces_the_stated_wet_mass(s):
    assert float(s.wet_for(s.dv_design)) == pytest.approx(s.wet_kg, rel=1e-9)
    assert 0 < s.fixed_kg < s.wet_kg


def test_wet_mass_and_hours_rise_with_dv():
    s = m.SCOUTS[0]
    w = s.wet_for([3.5, 4.5, 5.5, 7.0])
    h = [float(s.thrust_hours(d)) for d in (3.5, 4.5, 5.5, 7.0)]
    assert np.all(np.diff(w) > 0) and np.all(np.diff(h) > 0)
    # electric Δv is cheap in mass: 2 km/s more costs well under a fifth of the scout
    assert (w[2] - w[0]) / w[0] < 0.2


def test_thrust_hours_match_propellant_over_flow_rate():
    s = m.SCOUTS[0]
    thrust = 2 * s.efficiency * s.power_w / (s.ve * 1e3)  # N
    assert thrust == pytest.approx(0.118, abs=0.005)
    hours = float(s.propellant_for(4.5)) * s.ve * 1e3 / thrust / 3600
    assert float(s.thrust_hours(4.5)) == pytest.approx(hours, rel=1e-9)


def test_wet_mass_does_not_close_when_tanks_outgrow_the_gain():
    s = m.ScoutDesign('x', 500.0, 4.0, 300.0, 2000.0, tank_fraction=0.5)
    assert np.isinf(s.wet_for(6.0))


def test_leo_to_c3_matches_textbook_values():
    assert float(m.leo_to_c3(0.0)) == pytest.approx(3.22, abs=0.02)
    assert float(m.leo_to_c3(10.0)) == pytest.approx(3.67, abs=0.02)


def test_perigee_kick():
    dv = float(m.kick_dv(-1.8, 10.0))
    assert dv == pytest.approx(0.53, abs=0.01)
    assert float(m.kick_dv(-1.8, -1.8)) == 0.0
    prop, dry = m.kick_mass(550.0, dv)
    assert 90 < prop < 115 and dry == pytest.approx(0.15 * prop)
    # rocket equation closes on the total
    total = 550.0 + prop + dry
    assert m.G0 * 320.0 / 1e3 * np.log(total / (total - prop)) == pytest.approx(dv, rel=1e-9)


@pytest.mark.parametrize('L', (m.FALCON9_LOW, m.FALCON9_HIGH), ids=lambda L: L.name)
def test_launcher_reproduces_its_anchors(L):
    for x, p in L.anchors:
        c3 = (np.sqrt(m.MU_EARTH / m.R_PARK) + x) ** 2 - 2 * m.MU_EARTH / m.R_PARK
        assert float(L.payload(c3, recover=False)) == pytest.approx(p, rel=1e-6)
    c3_gto = (np.sqrt(m.MU_EARTH / m.R_PARK) + L.gto_dv) ** 2 - 2 * m.MU_EARTH / m.R_PARK
    assert float(L.payload(c3_gto, recover=True)) == pytest.approx(L.gto_recover_kg, rel=1e-6)


def test_launcher_payload_falls_with_c3_and_with_recovery():
    for L in (m.FALCON9_LOW, m.FALCON9_HIGH):
        p = [float(L.payload(c, True)) for c in (-2, 0, 10, 20)]
        assert np.all(np.diff(p) < 0)
        assert float(L.payload(10, True)) < float(L.payload(10, False))
    # the two fits bracket a pair of scouts with room to spare, and not six
    assert 2000 < float(m.FALCON9_LOW.payload(10, True)) < float(m.FALCON9_HIGH.payload(10, True)) < 3000
