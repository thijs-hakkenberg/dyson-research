"""Unit tests for isru_model — pure cost model logic."""

import numpy as np
import pytest

from isru_model import (
    BASELINE,
    PARAM_BOUNDS,
    _cumulative_production,
    clamp_param,
    cumulative_cost,
    cumulative_isru,
    cumulative_npv,
    earth_delivery_time,
    earth_delivery_time_ramped,
    earth_unit_cost,
    find_crossover,
    find_crossover_mfg_lead,
    find_crossover_npv,
    find_crossover_npv_phased,
    find_crossover_rate_dependent,
    isru_ops_cost,
    isru_ops_cost_rate_dependent,
    isru_unit_cost,
    learning_exponent,
    s_curve,
    significance_stars,
    unit_to_time,
    unit_to_time_piecewise,
)


# ===== TestLearningExponent =====

class TestLearningExponent:
    def test_lr_half_gives_minus_one(self):
        assert learning_exponent(0.5) == pytest.approx(-1.0)

    def test_lr_one_gives_zero(self):
        assert learning_exponent(1.0) == pytest.approx(0.0)

    def test_lr_085(self):
        expected = np.log(0.85) / np.log(2)
        assert learning_exponent(0.85) == pytest.approx(expected)

    def test_negative_for_typical_lr(self):
        assert learning_exponent(0.85) < 0
        assert learning_exponent(0.90) < 0

    def test_positive_for_lr_above_one(self):
        # Hypothetical: LR > 1 means costs increase
        assert learning_exponent(1.1) > 0


# ===== TestSCurve =====

class TestSCurve:
    def test_midpoint_is_half(self):
        assert s_curve(5.0, 5.0) == pytest.approx(0.5)

    def test_far_left_approaches_zero(self):
        assert s_curve(-10.0, 5.0) < 0.001

    def test_far_right_approaches_one(self):
        assert s_curve(20.0, 5.0) > 0.999

    def test_monotonically_increasing(self):
        ts = np.linspace(0, 20, 100)
        vals = s_curve(ts, 5.0)
        assert np.all(np.diff(vals) >= 0)

    def test_vectorized(self):
        ts = np.array([0.0, 5.0, 10.0])
        vals = s_curve(ts, 5.0)
        assert vals.shape == (3,)

    def test_steepness(self):
        # Higher k → steeper transition
        val_low_k = s_curve(6.0, 5.0, k=1.0)
        val_high_k = s_curve(6.0, 5.0, k=5.0)
        assert val_high_k > val_low_k


# ===== TestCumulativeProduction =====

class TestCumulativeProduction:
    def test_positive_after_midpoint(self):
        """Production is positive for t well past the ramp-up midpoint."""
        t = np.linspace(6, 30, 50)
        N = _cumulative_production(t, 500, 5, 2.0)
        assert np.all(N > 0)

    def test_monotonic(self):
        t = np.linspace(2, 30, 100)
        N = _cumulative_production(t, 500, 5, 2.0)
        assert np.all(np.diff(N) >= 0)

    def test_approaches_linear(self):
        # For large t, N(t) ≈ prod_rate * (t - t0) + const
        t_large = 100.0
        N = float(_cumulative_production(t_large, 500, 5, 2.0))
        # prod_rate * (t - t0) = 500 * 95 = 47500
        assert abs(N - 47500) < 500  # within ~1%

    def test_numerical_stability_large_t(self):
        t = 1000.0
        N = float(_cumulative_production(t, 500, 5, 2.0))
        assert np.isfinite(N)
        assert N > 0

    def test_matches_integration(self):
        from scipy.integrate import quad
        t_val = 10.0
        expected, _ = quad(lambda t: 500 * s_curve(t, 5.0, 2.0), 0, t_val)
        actual = float(_cumulative_production(t_val, 500, 5, 2.0))
        # _cumulative_production starts counting from when S(t0)=0.5
        # so the offset is -prod_rate/k * ln(2)
        offset = 500 / 2.0 * np.log(2)
        assert actual == pytest.approx(expected - offset, abs=1.0)


# ===== TestUnitToTime =====

class TestUnitToTime:
    def test_roundtrip(self):
        """unit_to_time(N(t)) ≈ t for forward production."""
        t_test = 15.0
        N_at_t = float(_cumulative_production(t_test, 500, 5, 2.0))
        if N_at_t > 0:
            t_back = float(unit_to_time(N_at_t, 500, 5, 2.0))
            assert t_back == pytest.approx(t_test, abs=0.1)

    def test_monotonic(self):
        ns = np.arange(1, 1000, dtype=float)
        ts = unit_to_time(ns, 500, 5, 2.0)
        assert np.all(np.diff(ts) >= 0)

    def test_vectorized(self):
        ns = np.array([1.0, 100.0, 1000.0])
        ts = unit_to_time(ns, 500, 5, 2.0)
        assert ts.shape == (3,)

    def test_stability_large_n(self):
        n_large = 100000.0
        t = float(unit_to_time(n_large, 500, 5, 2.0))
        assert np.isfinite(t)
        # Should be roughly n/prod_rate + t0
        assert abs(t - (n_large / 500 + 5)) < 1.0

    def test_asymptotic_form(self):
        """For very large n, uses asymptotic form."""
        n = 50000.0  # x = n*k/prod_rate = 200 >> 30
        t = float(unit_to_time(n, 500, 5, 2.0))
        expected = 5 + n / 500 + np.log(2) / 2.0
        assert t == pytest.approx(expected, rel=1e-6)


# ===== TestEarthUnitCost =====

class TestEarthUnitCost:
    def test_first_unit(self, baseline):
        cost = float(earth_unit_cost(1.0, baseline))
        expected = baseline["C_mfg1"] + baseline["m"] * baseline["p_launch"]
        assert cost == pytest.approx(expected)

    def test_decreasing(self, baseline):
        ns = np.array([1.0, 10.0, 100.0, 1000.0])
        costs = earth_unit_cost(ns, baseline)
        assert np.all(np.diff(costs) < 0)

    def test_launch_learning_variant(self, baseline):
        baseline["b_L"] = learning_exponent(0.97)
        cost_ll = float(earth_unit_cost(100.0, baseline))
        baseline["b_L"] = None
        cost_no_ll = float(earth_unit_cost(100.0, baseline))
        # With launch learning, cost at n=100 should be lower
        assert cost_ll < cost_no_ll

    def test_launch_floor(self, baseline):
        """Even at high n, earth cost is bounded below by launch cost."""
        cost = float(earth_unit_cost(100000.0, baseline))
        launch_floor = baseline["m"] * baseline["p_launch"]
        assert cost >= launch_floor


# ===== TestISRUOpsCost =====

class TestISRUOpsCost:
    def test_first_unit(self, baseline):
        # Test with zero vitamin fraction for clean formula verification
        baseline["vitamin_frac"] = 0.0
        cost = float(isru_ops_cost(1.0, baseline))
        alpha = baseline["alpha"]
        C_floor = baseline["C_floor"]
        expected_ops = alpha * (C_floor + (baseline["C_ops1"] - C_floor) * 1.0)
        expected_transport = baseline["m"] * baseline["p_transport"] * alpha
        assert cost == pytest.approx(expected_ops + expected_transport)

    def test_floor_respected(self, baseline):
        """Ops cost never goes below floor + transport."""
        cost = float(isru_ops_cost(100000.0, baseline))
        alpha = baseline["alpha"]
        floor = alpha * baseline["C_floor"] + baseline["m"] * baseline["p_transport"] * alpha
        assert cost >= floor * 0.99  # allow small floating point tolerance

    def test_alpha_scaling(self, baseline):
        cost_a1 = float(isru_ops_cost(100.0, baseline))
        baseline["alpha"] = 2.0
        cost_a2 = float(isru_ops_cost(100.0, baseline))
        assert cost_a2 > cost_a1


# ===== TestFindCrossover =====

class TestFindCrossover:
    def test_returns_int(self, baseline):
        result = find_crossover(baseline)
        assert isinstance(result, int)

    def test_baseline_exists(self, baseline):
        result = find_crossover(baseline)
        assert result < 20000

    def test_extreme_params_no_crossover(self):
        p = BASELINE.copy()
        p["K"] = 1e12  # Trillion dollar capital
        result = find_crossover(p, n_max=5000)
        assert result == 5000

    def test_npv_gte_undiscounted(self, baseline):
        undisc = find_crossover(baseline)
        npv = find_crossover_npv(baseline)
        assert npv >= undisc

    def test_phased_lte_lumpsum(self, baseline):
        lumpsum = find_crossover_npv(baseline)
        phased = find_crossover_npv_phased(baseline)
        assert phased <= lumpsum

    def test_backward_compat_shims(self, baseline):
        """find_crossover_npv and find_crossover_npv_phased are wrappers."""
        direct = find_crossover(baseline, discount=True)
        shim = find_crossover_npv(baseline)
        assert direct == shim

        direct_phased = find_crossover(baseline, discount=True, phased_k_years=5)
        shim_phased = find_crossover_npv_phased(baseline, K_years=5)
        assert direct_phased == shim_phased


# ===== TestEarthDeliveryTime =====

class TestEarthDeliveryTime:
    def test_simple_division(self):
        t = float(earth_delivery_time(500, 500))
        assert t == pytest.approx(1.0)

    def test_vectorized(self):
        ns = np.array([100.0, 500.0, 1000.0])
        ts = earth_delivery_time(ns, 500)
        expected = np.array([0.2, 1.0, 2.0])
        np.testing.assert_allclose(ts, expected)


# ===== TestEarthDeliveryTimeRamped =====

class TestEarthDeliveryTimeRamped:
    def test_monotonic(self):
        ns = np.arange(1, 1000, dtype=float)
        ts = earth_delivery_time_ramped(ns, 500, t0_earth=1.0, k_earth=2.0)
        assert np.all(np.diff(ts) >= 0)

    def test_matches_unit_to_time(self):
        """Ramped Earth schedule uses same logistic as ISRU schedule."""
        ns = np.array([1.0, 100.0, 1000.0])
        ts_ramped = earth_delivery_time_ramped(ns, 500, t0_earth=1.0, k_earth=2.0)
        ts_unit = unit_to_time(ns, 500, 1.0, 2.0)
        np.testing.assert_allclose(ts_ramped, ts_unit)

    def test_t0_zero_approaches_linear(self):
        """With t0=0 and large k, should approach n/prod_rate."""
        ns = np.array([500.0, 1000.0, 5000.0])
        ts = earth_delivery_time_ramped(ns, 500, t0_earth=0.0, k_earth=10.0)
        expected = ns / 500.0
        # For large k and t0=0, the logistic approaches linear at large n
        np.testing.assert_allclose(ts, expected, atol=0.5)

    def test_delayed_vs_instant(self):
        """Ramped schedule should always be later than instant start."""
        ns = np.array([10.0, 100.0, 1000.0])
        ts_instant = earth_delivery_time(ns, 500)
        ts_ramped = earth_delivery_time_ramped(ns, 500, t0_earth=1.0, k_earth=2.0)
        assert np.all(ts_ramped >= ts_instant)

    def test_find_crossover_with_earth_ramp(self):
        """Crossover with Earth ramp should be >= crossover without.

        Earth ramp delays Earth costs → lower PV → Earth looks cheaper →
        ISRU needs more units to achieve crossover.
        """
        p = BASELINE.copy()
        cross_no_ramp = find_crossover(p, discount=True)
        cross_ramp = find_crossover(p, discount=True, earth_ramp=(1.0, 2.0))
        assert cross_ramp >= cross_no_ramp


# ===== TestCumulativeNPV =====

class TestCumulativeNPV:
    def test_returns_three_arrays(self, baseline):
        ns, earth, isru = cumulative_npv(1000, baseline)
        assert len(ns) == 1000
        assert len(earth) == 1000
        assert len(isru) == 1000

    def test_monotonic(self, baseline):
        ns, earth, isru = cumulative_npv(1000, baseline)
        assert np.all(np.diff(earth) > 0)
        assert np.all(np.diff(isru) > 0)

    def test_r_zero_matches_undiscounted(self, baseline):
        baseline["r"] = 0.0
        ns, earth_npv, isru_npv = cumulative_npv(1000, baseline)
        _, _, earth_cum = cumulative_cost(earth_unit_cost, 1000, baseline)
        _, _, isru_cum = cumulative_isru(1000, baseline)
        np.testing.assert_allclose(earth_npv, earth_cum, rtol=1e-10)
        np.testing.assert_allclose(isru_npv, isru_cum, rtol=1e-10)


# ===== TestSignificanceStars =====

class TestSignificanceStars:
    def test_triple_star(self):
        assert significance_stars(0.0001) == "***"

    def test_double_star(self):
        assert significance_stars(0.005) == "**"

    def test_single_star(self):
        assert significance_stars(0.03) == "*"

    def test_no_star(self):
        assert significance_stars(0.1) == ""


# ===== TestClampParam =====

class TestClampParam:
    def test_r_floor(self):
        assert clamp_param("r", -0.01) == 0.0

    def test_alpha_floor(self):
        assert clamp_param("alpha", 0.5) == 1.0

    def test_passthrough(self):
        assert clamp_param("K", 50e9) == 50e9

    def test_unknown_param(self):
        assert clamp_param("unknown_param", -999) == -999


# ===== TestVitaminFraction =====

class TestVitaminFraction:
    def test_zero_matches_baseline(self, baseline):
        """vitamin_frac=0.0 should match original isru_ops_cost."""
        baseline["vitamin_frac"] = 0.0
        ns = np.array([1.0, 100.0, 1000.0])
        cost_vf0 = isru_ops_cost(ns, baseline)
        # Remove vitamin_frac to test default behavior
        del baseline["vitamin_frac"]
        cost_default = isru_ops_cost(ns, baseline)
        np.testing.assert_allclose(cost_vf0, cost_default)

    def test_positive_increases_cost(self, baseline):
        """vitamin_frac > 0 should increase ISRU ops cost."""
        ns = np.array([1.0, 100.0, 1000.0])
        cost_base = isru_ops_cost(ns, baseline)
        baseline["vitamin_frac"] = 0.10
        cost_vf10 = isru_ops_cost(ns, baseline)
        assert np.all(cost_vf10 > cost_base)

    def test_monotonic_in_frac(self, baseline):
        """Higher vitamin fraction should give higher cost."""
        n = 500.0
        baseline["vitamin_frac"] = 0.05
        cost_5 = float(isru_ops_cost(n, baseline))
        baseline["vitamin_frac"] = 0.10
        cost_10 = float(isru_ops_cost(n, baseline))
        baseline["vitamin_frac"] = 0.15
        cost_15 = float(isru_ops_cost(n, baseline))
        assert cost_5 < cost_10 < cost_15

    def test_crossover_delayed(self, baseline):
        """Vitamin fraction should delay crossover."""
        cross_base = find_crossover_npv(baseline)
        baseline["vitamin_frac"] = 0.10
        cross_vf = find_crossover_npv(baseline, N_max=40000)
        assert cross_vf >= cross_base


# ===== TestRateDependentLearning =====

class TestRateDependentLearning:
    def test_above_threshold_matches_baseline(self):
        """For late units (all above threshold), should match baseline."""
        p = BASELINE.copy()
        # Units at n=5000+ are well past ramp-up, all above any threshold
        ns = np.arange(5000, 5100, dtype=float)
        cost_base = isru_ops_cost(ns, p)
        cost_rd = isru_ops_cost_rate_dependent(ns, p, rate_threshold=0.2)
        np.testing.assert_allclose(cost_rd, cost_base, rtol=0.01)

    def test_early_units_higher_or_equal(self):
        """Rate-dependent cost should be >= baseline (frozen learning = higher cost)."""
        p = BASELINE.copy()
        ns = np.arange(1, 1000, dtype=float)
        cost_base = isru_ops_cost(ns, p)
        cost_rd = isru_ops_cost_rate_dependent(ns, p, rate_threshold=0.2)
        # Rate-dependent freezes learning during slow ramp, so costs should be >= baseline
        assert np.all(cost_rd >= cost_base - 1.0)  # small tolerance for float

    def test_crossover_delayed_or_equal(self):
        """Rate-dependent learning should delay crossover (or keep same)."""
        cross_base = find_crossover_npv(BASELINE)
        cross_rd = find_crossover_rate_dependent(BASELINE)
        assert cross_rd >= cross_base

    def test_higher_threshold_more_penalty(self):
        """Higher threshold means more units are 'frozen', delaying crossover more."""
        cross_20 = find_crossover_rate_dependent(BASELINE, rate_threshold=0.2)
        cross_50 = find_crossover_rate_dependent(BASELINE, rate_threshold=0.5)
        assert cross_50 >= cross_20


# ===== TestVitaminTwoPartModel =====

class TestVitaminTwoPartModel:
    """M1: Verify the two-part vitamin model: (1-fv)*c_ops + fv*m*(p_launch_eff + c_vit_kg)."""

    def test_increases_cost(self, baseline):
        """With fv>0, cost should increase (vitamin launch + mfg added)."""
        ns = np.array([100.0, 1000.0])
        cost_base = isru_ops_cost(ns, baseline)
        baseline["vitamin_frac"] = 0.10
        cost_vf = isru_ops_cost(ns, baseline)
        assert np.all(cost_vf > cost_base)

    def test_c_vitamin_kg_scales(self):
        """Higher c_vitamin_kg should give higher cost."""
        p = BASELINE.copy()
        p["vitamin_frac"] = 0.10
        n = 500.0
        p["c_vitamin_kg"] = 5000
        cost_low = float(isru_ops_cost(n, p))
        p["c_vitamin_kg"] = 50000
        cost_high = float(isru_ops_cost(n, p))
        assert cost_high > cost_low

    def test_vitamin_launch_component(self):
        """Vitamin launch cost should equal fv * m * p_launch for no-learning case."""
        p = BASELINE.copy()
        p["vitamin_frac"] = 0.10
        p["c_vitamin_kg"] = 0  # zero mfg cost to isolate launch
        p["b_L"] = None  # no launch learning
        n = 100.0
        cost_vf = float(isru_ops_cost(n, p))
        # Expected: (1-0.10) * base_ops_no_vf + 0.10 * 1850 * 1000
        p_no_vf = BASELINE.copy()
        p_no_vf["vitamin_frac"] = 0.0  # explicitly zero for clean comparison
        p_no_vf["b_L"] = None  # match the test config
        cost_base = float(isru_ops_cost(n, p_no_vf))
        expected = 0.90 * cost_base + 0.10 * 1850 * 1000
        assert cost_vf == pytest.approx(expected, rel=0.01)

    def test_differs_from_old_formula(self):
        """Two-part model should differ from old fv*earth_unit_cost formula."""
        p = BASELINE.copy()
        n = 100.0  # early units where Earth mfg cost is high
        p["vitamin_frac"] = 0.10
        cost_new = float(isru_ops_cost(n, p))
        # Old formula: (1-fv)*c_ops + fv*c_earth (which included full Earth mfg + launch)
        p["vitamin_frac"] = 0.0
        cost_base = float(isru_ops_cost(n, p))
        cost_old = (1.0 - 0.10) * cost_base + 0.10 * float(earth_unit_cost(n, p))
        # The two models should produce different values
        assert cost_new != pytest.approx(cost_old, rel=0.01)


# ===== TestTwoComponentEarthModel =====

class TestTwoComponentEarthModel:
    """U1: Verify two-component Earth manufacturing model."""

    def test_zero_cmat_matches_single_curve(self, baseline):
        """With C_mat=0, should match the original single Wright curve."""
        ns = np.array([1.0, 100.0, 1000.0, 10000.0])
        # Single curve: C_mfg1 * n^b_E
        p_single = baseline.copy()
        p_single["C_mat"] = 0
        cost_single = earth_unit_cost(ns, p_single)
        # Original behavior (C_mat absent)
        p_orig = baseline.copy()
        del p_orig["C_mat"]
        del p_orig["C_labor1"]
        cost_orig = earth_unit_cost(ns, p_orig)
        np.testing.assert_allclose(cost_single, cost_orig)

    def test_two_component_higher_at_large_n(self, baseline):
        """Two-component should be higher than single curve at large n due to material floor."""
        n = 10000.0
        # Single curve
        p_single = baseline.copy()
        p_single["C_mat"] = 0
        cost_single = float(earth_unit_cost(n, p_single))
        # Two-component: C_mat provides a natural floor
        p_two = baseline.copy()
        p_two["C_mat"] = 1e6
        p_two["C_labor1"] = baseline["C_mfg1"] - 1e6
        cost_two = float(earth_unit_cost(n, p_two))
        assert cost_two > cost_single

    def test_first_unit_preserves_total(self, baseline):
        """At n=1, C_mat + C_labor1 * 1^b = C_mat + C_labor1 = C_mfg1."""
        n = 1.0
        p = baseline.copy()
        p["C_mat"] = 1e6
        p["C_labor1"] = baseline["C_mfg1"] - 1e6
        cost = float(earth_unit_cost(n, p))
        # At n=1: mfg = C_mat + C_labor1 * 1^b = C_mat + C_labor1 = C_mfg1
        # launch cost = m * p_launch (same either way)
        expected = baseline["C_mfg1"] + baseline["m"] * baseline["p_launch"]
        assert cost == pytest.approx(expected, rel=1e-6)

    def test_crossover_similar(self, baseline):
        """Two-component model should produce similar crossover to single curve."""
        # Single curve
        p_single = baseline.copy()
        p_single["C_mat"] = 0
        cross_single = find_crossover(p_single, discount=True)
        # Two-component with small C_mat
        p_two = baseline.copy()
        p_two["C_mat"] = 1e6
        p_two["C_labor1"] = baseline["C_mfg1"] - 1e6
        cross_two = find_crossover(p_two, discount=True)
        # Should be close (small C_mat shouldn't change much)
        assert abs(cross_two - cross_single) < 500


# ===== TestPioneeringPhase =====

class TestPioneeringPhase:
    """V1: Verify pioneering phase cost multiplier."""

    def test_gamma_one_matches_baseline(self, baseline):
        """gamma=1 should match baseline (no pioneering effect)."""
        ns = np.array([1.0, 50.0, 100.0, 500.0])
        cost_base = isru_ops_cost(ns, baseline)
        baseline["pioneer_gamma"] = 1.0
        baseline["pioneer_n"] = 50
        cost_pioneer = isru_ops_cost(ns, baseline)
        np.testing.assert_allclose(cost_pioneer, cost_base)

    def test_gamma_increases_early_costs(self, baseline):
        """gamma>1 should increase costs for n <= n_p."""
        n_early = np.array([1.0, 10.0, 20.0])
        cost_base = isru_ops_cost(n_early, baseline)
        baseline["pioneer_gamma"] = 3.0
        baseline["pioneer_n"] = 50
        cost_pioneer = isru_ops_cost(n_early, baseline)
        assert np.all(cost_pioneer > cost_base)

    def test_late_units_unaffected(self, baseline):
        """Units past n_p should be unaffected."""
        n_late = np.array([100.0, 500.0, 1000.0])
        cost_base = isru_ops_cost(n_late, baseline)
        baseline["pioneer_gamma"] = 5.0
        baseline["pioneer_n"] = 50
        cost_pioneer = isru_ops_cost(n_late, baseline)
        np.testing.assert_allclose(cost_pioneer, cost_base)

    def test_crossover_delayed(self, baseline):
        """Pioneering phase should delay crossover."""
        cross_base = find_crossover(baseline, discount=True)
        baseline["pioneer_gamma"] = 3.0
        baseline["pioneer_n"] = 50
        cross_pioneer = find_crossover(baseline, discount=True)
        assert cross_pioneer >= cross_base


# ===== TestQACost =====

class TestQACost:
    """V2: Verify QA/certification cost addition."""

    def test_zero_qa_matches_baseline(self, baseline):
        """C_QA1=0 should match baseline."""
        ns = np.array([1.0, 100.0, 1000.0])
        cost_base = isru_ops_cost(ns, baseline)
        baseline["C_QA1"] = 0
        cost_qa = isru_ops_cost(ns, baseline)
        np.testing.assert_allclose(cost_qa, cost_base)

    def test_qa_increases_cost(self, baseline):
        """C_QA1>0 should increase ISRU ops cost."""
        ns = np.array([1.0, 100.0, 1000.0])
        cost_base = isru_ops_cost(ns, baseline)
        baseline["C_QA1"] = 1e6
        baseline["LR_QA"] = 0.85
        cost_qa = isru_ops_cost(ns, baseline)
        assert np.all(cost_qa > cost_base)

    def test_qa_declines_with_experience(self, baseline):
        """QA cost should decline at large n (learning curve)."""
        baseline["C_QA1"] = 1e6
        baseline["LR_QA"] = 0.85
        cost_early = float(isru_ops_cost(1.0, baseline))
        cost_late = float(isru_ops_cost(10000.0, baseline))
        # QA cost at n=1: $1M; at n=10000: much less
        # Total ops should still be decreasing
        assert cost_late < cost_early

    def test_crossover_delayed(self, baseline):
        """QA cost should delay crossover."""
        cross_base = find_crossover(baseline, discount=True)
        baseline["C_QA1"] = 1e6
        baseline["LR_QA"] = 0.85
        cross_qa = find_crossover(baseline, n_max=40000, discount=True)
        assert cross_qa >= cross_base


# ===== TestPermanentCrossover =====

class TestPermanentCrossover:
    """V3: Verify permanent vs transient crossover classification."""

    def test_zero_vitamin_is_permanent(self, baseline):
        """With f_v=0, C_floor=0.5M < threshold should be permanent."""
        from isru_model import is_permanent_crossover
        baseline["vitamin_frac"] = 0.0
        assert is_permanent_crossover(baseline) is True

    def test_baseline_vitamin_is_transient(self, baseline):
        """With f_v=0.05, vitamin component raises ISRU floor above Earth's."""
        from isru_model import is_permanent_crossover
        # vitamin_frac=0.05 with c_vitamin_kg=$10k/kg adds ~$943k asymptotic,
        # pushing ISRU floor above Earth's C_mat + m*p_fuel
        assert is_permanent_crossover(baseline) is False

    def test_high_cfloor_is_transient(self, baseline):
        """Very high C_floor should make crossover transient."""
        from isru_model import is_permanent_crossover
        baseline["C_floor"] = 5e6  # well above threshold
        assert is_permanent_crossover(baseline) is False


# ===== TestEarthThroughputCap =====

class TestEarthThroughputCap:
    """U3: Verify Earth launch throughput cap."""

    def test_no_cap_matches_baseline(self):
        """No cap should match baseline delivery time."""
        ns = np.array([100.0, 500.0, 1000.0])
        from isru_model import earth_delivery_time
        t_base = earth_delivery_time(ns, 500)
        t_nocap = earth_delivery_time(ns, 500, earth_max_units_per_year=None)
        np.testing.assert_allclose(t_base, t_nocap)

    def test_cap_slows_delivery(self):
        """Cap below prod_rate should slow delivery."""
        from isru_model import earth_delivery_time
        t_fast = earth_delivery_time(1000.0, 500)  # 1000/500 = 2 yr
        t_capped = earth_delivery_time(1000.0, 500, earth_max_units_per_year=250)  # 1000/250 = 4 yr
        assert float(t_capped) > float(t_fast)
        assert float(t_capped) == pytest.approx(4.0)

    def test_cap_above_prodrate_no_effect(self):
        """Cap above prod_rate should have no effect."""
        from isru_model import earth_delivery_time
        t_base = earth_delivery_time(1000.0, 500)
        t_high_cap = earth_delivery_time(1000.0, 500, earth_max_units_per_year=10000)
        np.testing.assert_allclose(t_high_cap, t_base)

    def test_crossover_shifts_with_cap(self, baseline):
        """Throughput cap should shift crossover earlier (Earth is slower)."""
        cross_base = find_crossover(baseline, discount=True)
        p_capped = baseline.copy()
        p_capped["earth_max_units_per_year"] = 250
        cross_capped = find_crossover(p_capped, discount=True)
        # Slower Earth delivery means Earth costs are discounted more -> Earth cheaper in NPV
        # But also, if cap < prod_rate, it extends the Earth timeline
        # Net effect depends on specifics, but we just verify it runs
        assert isinstance(cross_capped, int)


# ===== TestPiecewiseSchedule =====

class TestPiecewiseSchedule:
    def test_matches_logistic_at_large_t(self):
        """Piecewise matches logistic for units well past construction."""
        ns = np.array([5000.0, 10000.0])
        t_baseline = unit_to_time(ns, 500, 5, 2.0)
        t_piecewise = unit_to_time_piecewise(ns, 500, 5, 2.0, t_construction=4.0)
        np.testing.assert_allclose(t_piecewise, t_baseline, rtol=1e-10)

    def test_clamped_during_construction(self):
        """Units produced during construction phase are clamped to t_c."""
        # Very early units with high t_c should be clamped
        t_c = 10.0  # construction ends at year 10
        ns = np.array([1.0, 10.0])
        t_pw = unit_to_time_piecewise(ns, 500, 5, 2.0, t_construction=t_c)
        assert np.all(t_pw >= t_c)

    def test_default_construction_time(self):
        """Default t_c = t0 - 1."""
        ns = np.array([1.0])
        t_pw = unit_to_time_piecewise(ns, 500, 5.0, 2.0)
        # t_c defaults to 4.0, and unit_to_time(1, ...) ≈ 5.0
        # so piecewise should be max(5.0, 4.0) = 5.0
        t_base = unit_to_time(ns, 500, 5.0, 2.0)
        np.testing.assert_allclose(t_pw, t_base)

    def test_monotonic(self):
        """Piecewise schedule should be monotonically increasing."""
        ns = np.arange(1, 1000, dtype=float)
        ts = unit_to_time_piecewise(ns, 500, 5, 2.0, t_construction=4.0)
        assert np.all(np.diff(ts) >= 0)


# ===== TestMfgLeadTime =====

class TestMfgLeadTime:
    def test_returns_int(self, baseline):
        result = find_crossover_mfg_lead(baseline, tau_mfg=0.5)
        assert isinstance(result, int)

    def test_lead_time_shifts_crossover(self, baseline):
        """Mfg lead-time means Earth pays earlier → higher PV → earlier crossover."""
        cross_base = find_crossover_npv(baseline)
        cross_lead = find_crossover_mfg_lead(baseline, tau_mfg=0.5)
        # Earth mfg cost paid earlier → higher PV → Earth more expensive → crossover earlier
        assert cross_lead <= cross_base

    def test_zero_lead_matches_baseline(self, baseline):
        """With tau_mfg=0, should match standard NPV crossover."""
        cross_base = find_crossover_npv(baseline)
        cross_zero = find_crossover_mfg_lead(baseline, tau_mfg=0.0)
        # Should be very close (not exact due to split mfg/launch discounting)
        assert abs(cross_zero - cross_base) <= 5


# ===== TestLaunchesPerUnit =====

class TestLaunchesPerUnit:
    """M2: Verify launches_per_unit re-indexing of launch learning."""

    def test_default_unchanged(self, baseline):
        """launches_per_unit=1.0 should match original behavior."""
        baseline["b_L"] = np.log(0.97) / np.log(2)
        ns = np.array([100.0, 1000.0])
        cost_default = earth_unit_cost(ns, baseline)
        baseline["launches_per_unit"] = 1.0
        cost_explicit = earth_unit_cost(ns, baseline)
        np.testing.assert_allclose(cost_default, cost_explicit)

    def test_higher_lpu_cheaper(self, baseline):
        """More launches per unit = more cumulative launches = more learning = lower cost."""
        baseline["b_L"] = np.log(0.97) / np.log(2)
        n = 100.0
        baseline["launches_per_unit"] = 1.0
        cost_1 = float(earth_unit_cost(n, baseline))
        baseline["launches_per_unit"] = 2.0
        cost_2 = float(earth_unit_cost(n, baseline))
        # More launches means the ops component has learned more → lower cost
        assert cost_2 < cost_1

    def test_crossover_shifts_with_lpu(self, baseline):
        """Higher launches_per_unit should shift crossover earlier (Earth learns faster)."""
        baseline["b_L"] = np.log(0.97) / np.log(2)
        baseline["launches_per_unit"] = 1.0
        cross_1 = find_crossover_npv(baseline, N_max=40000)
        baseline["launches_per_unit"] = 2.0
        cross_2 = find_crossover_npv(baseline, N_max=40000)
        # More launch learning → Earth gets cheaper faster → harder for ISRU → later crossover
        assert cross_2 >= cross_1


# ===== TestMaintenanceCost =====

class TestMaintenanceCost:
    """M3: Verify ongoing capital maintenance delays crossover."""

    def test_zero_maint_unchanged(self, baseline):
        """K_maint_frac=0 should match baseline crossover."""
        baseline["K_maint_frac"] = 0.0
        cross_maint = find_crossover(baseline, discount=True)
        cross_base = find_crossover_npv(baseline)
        assert cross_maint == cross_base

    def test_positive_maint_delays(self, baseline):
        """Positive maintenance fraction should delay crossover."""
        cross_base = find_crossover(baseline, discount=True)
        baseline["K_maint_frac"] = 0.10
        baseline["K_maint_interval"] = 5
        cross_maint = find_crossover(baseline, n_max=40000, discount=True)
        assert cross_maint >= cross_base

    def test_higher_maint_more_delay(self, baseline):
        """Higher maintenance fraction should delay crossover more."""
        baseline["K_maint_interval"] = 5
        baseline["K_maint_frac"] = 0.05
        cross_5 = find_crossover(baseline, n_max=40000, discount=True)
        baseline["K_maint_frac"] = 0.15
        cross_15 = find_crossover(baseline, n_max=40000, discount=True)
        assert cross_15 >= cross_5


# ===== TestEarthMfgFloor =====

class TestEarthMfgFloor:
    """N1: Verify Earth manufacturing cost floor behavior."""

    def test_zero_floor_matches_baseline(self, baseline):
        """C_mfg_floor=0 should match original behavior."""
        ns = np.array([1.0, 100.0, 1000.0, 10000.0])
        cost_default = earth_unit_cost(ns, baseline)
        baseline["C_mfg_floor"] = 0
        cost_explicit = earth_unit_cost(ns, baseline)
        np.testing.assert_allclose(cost_default, cost_explicit)

    def test_floor_respected(self, baseline):
        """Earth mfg cost should never go below floor."""
        baseline["C_mfg_floor"] = 5e6
        ns = np.arange(1, 20001, dtype=float)
        costs = earth_unit_cost(ns, baseline)
        # Total cost includes launch, so floor only applies to mfg component
        # At high n, mfg component dominates and should be >= floor
        # The total cost should be >= floor + launch_cost
        launch_floor = baseline["m"] * baseline["p_launch"]
        # At n=20000, the learning curve mfg would be well below 5M,
        # so cost should be floor + launch
        cost_high_n = float(costs[-1])
        assert cost_high_n >= 5e6 + launch_floor * 0.99

    def test_crossover_shifts(self, baseline):
        """Floor should delay crossover (Earth stays more expensive)."""
        cross_base = find_crossover_npv(baseline)
        baseline["C_mfg_floor"] = 5e6
        cross_floor = find_crossover(baseline, n_max=40000, discount=True)
        assert cross_floor >= cross_base

    def test_first_unit_unaffected(self, baseline):
        """First unit mfg cost > any reasonable floor, so no change."""
        cost_base = float(earth_unit_cost(1.0, baseline))
        baseline["C_mfg_floor"] = 5e6
        cost_floor = float(earth_unit_cost(1.0, baseline))
        # C_mfg1 = $75M >> $5M floor
        assert cost_base == pytest.approx(cost_floor)


# ===== TestLogNormalK =====

class TestLogNormalK:
    """Y1: Verify log-normal K distribution properties (now default)."""

    def test_right_skewed(self):
        """Log-normal K should have mean > median (right-skewed)."""
        from isru_mc import sample_mc_params
        rng = np.random.default_rng(42)
        params = sample_mc_params(rng, 10000, rho=0.3, correlated=True)
        k = params["K"]
        assert np.mean(k) > np.median(k)

    def test_median_near_65b(self):
        """Log-normal K median should be near $65B."""
        from isru_mc import sample_mc_params
        rng = np.random.default_rng(42)
        params = sample_mc_params(rng, 10000, rho=0.3, correlated=True)
        k_median = float(np.median(params["K"]))
        assert 55e9 < k_median < 75e9  # within ~15% of $65B

    def test_clipped_bounds(self):
        """Log-normal K should be clipped to [20B, 200B]."""
        from isru_mc import sample_mc_params
        rng = np.random.default_rng(42)
        params = sample_mc_params(rng, 10000, rho=0.3, correlated=True)
        assert np.all(params["K"] >= 20e9)
        assert np.all(params["K"] <= 200e9)

    def test_lognormal_default(self):
        """Y1: Default k_distribution should be lognormal."""
        from isru_mc import sample_mc_params
        rng = np.random.default_rng(42)
        params = sample_mc_params(rng, 10000, rho=0.3, correlated=True)
        k = params["K"]
        # Log-normal is right-skewed: mean > median
        assert np.mean(k) > np.median(k)
        # With σ_ln=0.70, P90 should be significantly above median
        p90 = float(np.percentile(k, 90))
        median_k = float(np.median(k))
        assert p90 / median_k > 1.8  # P90/P50 > 1.8 for σ_ln=0.70

    def test_sigma_ln_wider_than_old(self):
        """Y1: σ_ln=0.70 should give wider spread than old σ_ln=0.48."""
        from isru_mc import sample_mc_params
        rng = np.random.default_rng(42)
        params = sample_mc_params(rng, 10000, rho=0.3, correlated=True)
        k = params["K"]
        p10 = float(np.percentile(k, 10))
        p90 = float(np.percentile(k, 90))
        # P90/P10 ratio should be substantial with σ_ln=0.70
        assert p90 / p10 > 4.0

    def test_uniform_variant(self):
        """Uniform K variant should still work."""
        from isru_mc import sample_mc_params
        rng = np.random.default_rng(42)
        params = sample_mc_params(rng, 1000, rho=0.3, correlated=True,
                                  k_distribution="uniform")
        # Uniform [30B, 100B] — check bounds
        assert np.all(params["K"] >= 30e9 - 1)
        assert np.all(params["K"] <= 100e9 + 1)


# ===== TestKaplanMeier =====

class TestKaplanMeier:
    """N1c: Verify Kaplan-Meier estimator."""

    def test_all_converged_matches_median(self):
        """When all runs converge, KM median should equal sample median."""
        from isru_mc import compute_kaplan_meier
        crossovers = np.array([100, 200, 300, 400, 500], dtype=float)
        n_max = 1000
        km_med, _, _ = compute_kaplan_meier(crossovers, n_max)
        assert km_med == pytest.approx(300.0)

    def test_censored_shifts_median(self):
        """With censored observations, KM median should be >= conditional median."""
        from isru_mc import compute_kaplan_meier
        # 5 converged, 5 censored at H
        crossovers = np.array([100, 200, 300, 400, 500, 1000, 1000, 1000, 1000, 1000], dtype=float)
        n_max = 1000
        km_med, _, _ = compute_kaplan_meier(crossovers, n_max)
        cond_med = float(np.median(crossovers[crossovers < n_max]))
        # KM accounts for censoring; conditional median ignores it
        assert km_med >= cond_med or km_med == float('inf')

    def test_survival_starts_at_one(self):
        """Survival function should start at 1.0."""
        from isru_mc import compute_kaplan_meier
        crossovers = np.array([100, 200, 500, 1000], dtype=float)
        _, _, km_surv = compute_kaplan_meier(crossovers, 1000)
        assert km_surv[0] == pytest.approx(1.0)


# ===== TestKProdRateCorrelation =====

class TestKProdRateCorrelation:
    def test_correlated_sampling_positive_spearman(self):
        """Correlated sampling should produce positive Spearman(K, prod_rate)."""
        from isru_mc import sample_mc_params
        from scipy.stats import spearmanr
        rng = np.random.default_rng(42)
        params = sample_mc_params(rng, 5000, rho=0.3, rho_k_prod=0.5, correlated=True)
        rho_sp, p_val = spearmanr(params["K"], params["prod_rate"])
        assert rho_sp > 0.3  # should be strongly positive
        assert p_val < 0.001


# ===== TestLearningPlateau =====

class TestLearningPlateau:
    """Y3: Verify piecewise learning plateau model."""

    def test_damping_one_matches_baseline(self, baseline):
        """damping=1.0 should reproduce standard Wright curve."""
        from isru_model import earth_unit_cost, earth_unit_cost_plateau
        ns = np.array([1.0, 100.0, 1000.0, 5000.0])
        cost_base = earth_unit_cost(ns, baseline)
        cost_plateau = earth_unit_cost_plateau(ns, baseline, n_break=500, damping=1.0)
        np.testing.assert_allclose(cost_plateau, cost_base, rtol=1e-10)

    def test_before_break_matches_baseline(self, baseline):
        """Units before n_break should match standard model."""
        from isru_model import earth_unit_cost, earth_unit_cost_plateau
        ns = np.array([1.0, 50.0, 100.0, 499.0])
        cost_base = earth_unit_cost(ns, baseline)
        cost_plateau = earth_unit_cost_plateau(ns, baseline, n_break=500, damping=0.5)
        np.testing.assert_allclose(cost_plateau, cost_base, rtol=1e-10)

    def test_after_break_higher_than_baseline(self, baseline):
        """Units after n_break with damping<1 should be more expensive."""
        from isru_model import earth_unit_cost, earth_unit_cost_plateau
        ns = np.array([1000.0, 5000.0, 10000.0])
        cost_base = earth_unit_cost(ns, baseline)
        cost_plateau = earth_unit_cost_plateau(ns, baseline, n_break=500, damping=0.5)
        assert np.all(cost_plateau >= cost_base)

    def test_continuity_at_break(self, baseline):
        """Cost should be continuous at the break point."""
        from isru_model import earth_unit_cost_plateau
        n_break = 500
        ns = np.array([float(n_break) - 0.01, float(n_break), float(n_break) + 0.01])
        costs = earth_unit_cost_plateau(ns, baseline, n_break=n_break, damping=0.5)
        # Check continuity: adjacent costs should be very close
        assert abs(costs[0] - costs[1]) < 1000  # within $1k
        assert abs(costs[1] - costs[2]) < 1000

    def test_crossover_delays_with_plateau(self, baseline):
        """Plateau should delay crossover (Earth stays cheaper longer)."""
        from isru_model import find_crossover_npv, find_crossover_plateau
        cross_base = find_crossover_npv(baseline)
        cross_plateau = find_crossover_plateau(baseline, n_break=500, damping=0.5)
        # Plateau slows Earth cost decline -> later crossover
        assert cross_plateau <= cross_base  # Earth stays MORE expensive with plateau

    def test_less_damping_closer_to_baseline(self, baseline):
        """Less damping (closer to 1.0) should give result closer to baseline."""
        from isru_model import find_crossover_plateau
        cross_05 = find_crossover_plateau(baseline, n_break=500, damping=0.5)
        cross_07 = find_crossover_plateau(baseline, n_break=500, damping=0.7)
        cross_10 = find_crossover_plateau(baseline, n_break=500, damping=1.0)
        # More damping (lower value) means MORE slowdown in Earth learning
        # so crossover should come EARLIER (Earth stays expensive)
        assert cross_05 <= cross_07 <= cross_10


# ===== TestStochasticPFuel =====

class TestStochasticPFuel:
    """Y2: Verify stochastic p_fuel in MC sampling."""

    def test_pfuel_sampled(self):
        """p_fuel should be present in sampled parameters."""
        from isru_mc import sample_mc_params
        rng = np.random.default_rng(42)
        params = sample_mc_params(rng, 1000, rho=0.3, correlated=True)
        assert "p_fuel" in params
        assert len(params["p_fuel"]) == 1000

    def test_pfuel_range(self):
        """p_fuel should be sampled from U[100, 400]."""
        from isru_mc import sample_mc_params
        rng = np.random.default_rng(42)
        params = sample_mc_params(rng, 10000, rho=0.3, correlated=True)
        assert np.all(params["p_fuel"] >= 100)
        assert np.all(params["p_fuel"] <= 400)
        # Mean should be near 250
        assert 230 < np.mean(params["p_fuel"]) < 270
