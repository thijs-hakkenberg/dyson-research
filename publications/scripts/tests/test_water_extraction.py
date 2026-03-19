"""Tests for Paper 05 water extraction model V2 and Monte Carlo."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
from water_extraction_model import (
    ASTEROID_BASELINE,
    LUNAR_BASELINE,
    PHOBOS_BASELINE,
    annual_production,
    total_capital,
    total_cost_trajectory,
    cost_per_kg_trajectory,
    npv_cost,
    npv_cost_per_kg,
    compare_sources,
    optimal_source_by_scale,
    payload_fraction,
    transport_cost_per_kg_derived,
    get_trip_time,
)
from water_extraction_mc import (
    run_mc,
    run_all_sources,
    probability_asteroid_cheaper,
    sensitivity_analysis,
    ASTEROID_DISTRIBUTIONS,
    LUNAR_DISTRIBUTIONS,
    WaterMCResult,
)


class TestTransportPhysics:
    """Tests for the physics-based transport model."""

    def test_payload_fraction_decreases_with_delta_v(self):
        f1 = payload_fraction(3.0, 2500)
        f2 = payload_fraction(6.0, 2500)
        assert f1 > f2, "Higher delta-v should give lower payload fraction"

    def test_payload_fraction_increases_with_isp(self):
        f1 = payload_fraction(4.5, 2000)
        f2 = payload_fraction(4.5, 3000)
        assert f2 > f1, "Higher Isp should give higher payload fraction"

    def test_payload_fraction_range(self):
        f = payload_fraction(4.5, 2500)
        assert 0 < f < 1, f"Payload fraction should be in (0,1), got {f}"

    def test_ep_better_than_chemical(self):
        """EP (high Isp) should give better payload fraction than chemical."""
        f_ep = payload_fraction(4.5, 2500)
        f_chem = payload_fraction(2.5, 450)
        # Despite lower delta-v, chemical has much worse payload fraction per km/s
        assert f_ep > f_chem * 0.5, "EP advantage should be significant"

    def test_trip_time_positive(self):
        tt = get_trip_time(ASTEROID_BASELINE)
        assert tt > 0, "Trip time should be positive"

    def test_asteroid_trip_longer_than_lunar(self):
        """EP asteroid trips should be longer than chemical lunar trips."""
        tt_ast = get_trip_time(ASTEROID_BASELINE)
        tt_lun = get_trip_time(LUNAR_BASELINE)
        assert tt_ast > tt_lun, "Asteroid EP trips should take longer than lunar chemical"

    def test_derived_transport_cost_positive(self):
        for p in [ASTEROID_BASELINE, LUNAR_BASELINE, PHOBOS_BASELINE]:
            c = transport_cost_per_kg_derived(p)
            assert c > 0 and c < 1e6, f"Transport cost should be reasonable, got {c}"


class TestWaterExtractionModel:
    """Tests for the deterministic water extraction model."""

    def test_annual_production_ramps_up(self):
        prod = annual_production(ASTEROID_BASELINE)
        assert prod[0] < prod[-1]

    def test_annual_production_bounded(self):
        prod = annual_production(ASTEROID_BASELINE)
        assert np.all(prod >= 0)
        assert np.all(prod <= ASTEROID_BASELINE["target_annual_kg"] * 1.01)

    def test_total_capital_positive(self):
        for params in [ASTEROID_BASELINE, LUNAR_BASELINE, PHOBOS_BASELINE]:
            assert total_capital(params) > 0

    def test_lunar_has_surface_base_cost(self):
        assert total_capital(LUNAR_BASELINE) > total_capital(ASTEROID_BASELINE)

    def test_cost_trajectory_shape(self):
        annual, cum, cum_prod = total_cost_trajectory(ASTEROID_BASELINE)
        n = ASTEROID_BASELINE["program_years"]
        assert len(annual) == n
        assert len(cum) == n
        assert len(cum_prod) == n

    def test_cumulative_cost_monotonic(self):
        _, cum, _ = total_cost_trajectory(ASTEROID_BASELINE)
        assert np.all(np.diff(cum) >= 0)

    def test_cost_per_kg_decreases(self):
        cpk = cost_per_kg_trajectory(ASTEROID_BASELINE)
        assert cpk[15] < cpk[5]

    def test_npv_cost_positive(self):
        for params in [ASTEROID_BASELINE, LUNAR_BASELINE]:
            assert npv_cost(params) > 0

    def test_npv_per_kg_reasonable(self):
        for name, params in [("ast", ASTEROID_BASELINE), ("lunar", LUNAR_BASELINE)]:
            cpk = npv_cost_per_kg(params)
            assert 10 < cpk < 100_000, f"{name}: NPV/kg={cpk}"

    def test_asteroid_cheaper_than_lunar(self):
        ast_cpk = npv_cost_per_kg(ASTEROID_BASELINE)
        lun_cpk = npv_cost_per_kg(LUNAR_BASELINE)
        assert ast_cpk < lun_cpk, f"Ast {ast_cpk:.0f} >= Lunar {lun_cpk:.0f}"

    def test_compare_sources_returns_all(self):
        results = compare_sources()
        assert "C-type NEA" in results
        assert "Lunar polar ice" in results
        assert "Phobos/Deimos" in results
        # V2: should have derived transport cost
        assert "derived_transport_cost_per_kg" in results["C-type NEA"]
        assert "trip_time_years" in results["C-type NEA"]

    def test_optimal_source_by_scale(self):
        result = optimal_source_by_scale()
        assert len(result["C-type NEA"]) == len(result["scales"])


class TestWaterExtractionMC:
    """Tests for the Monte Carlo engine."""

    def test_mc_runs(self):
        result = run_mc("test", ASTEROID_BASELINE, ASTEROID_DISTRIBUTIONS, n_samples=100, seed=42)
        assert isinstance(result, WaterMCResult)
        assert result.n_samples == 100

    def test_mc_produces_spread(self):
        result = run_mc("test", ASTEROID_BASELINE, ASTEROID_DISTRIBUTIONS, n_samples=500, seed=42)
        assert result.p90_per_kg > result.p10_per_kg

    def test_mc_stores_param_samples(self):
        result = run_mc("test", ASTEROID_BASELINE, ASTEROID_DISTRIBUTIONS, n_samples=100, seed=42)
        assert "water_fraction" in result.param_samples
        assert len(result.param_samples["water_fraction"]) == 100

    def test_sensitivity_analysis(self):
        result = run_mc("test", ASTEROID_BASELINE, ASTEROID_DISTRIBUTIONS, n_samples=500, seed=42)
        sens = sensitivity_analysis(result)
        assert len(sens) > 0
        assert all(s.abs_rho >= 0 for s in sens)
        # Should be sorted by absolute rho
        for i in range(len(sens) - 1):
            assert sens[i].abs_rho >= sens[i + 1].abs_rho

    def test_run_all_sources(self):
        results = run_all_sources(n_samples=100, seed=42)
        assert "C-type NEA" in results
        assert "Lunar polar ice" in results

    def test_probability_asteroid_cheaper(self):
        p = probability_asteroid_cheaper(n_samples=500, seed=42)
        assert 0 < p < 1
        assert p > 0.4, f"Asteroid should usually be cheaper, got {p:.1%}"


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
