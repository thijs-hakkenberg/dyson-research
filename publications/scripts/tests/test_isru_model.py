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


# ===== TestVitaminFractionCorrected =====

class TestVitaminFractionCorrected:
    """Verify the corrected (1-fv)*c_ops + fv*c_earth formula."""

    def test_reduces_isru_ops_component(self, baseline):
        """With fv>0, the ISRU-ops portion is scaled down by (1-fv)."""
        ns = np.array([100.0, 1000.0])
        cost_base = isru_ops_cost(ns, baseline)
        baseline["vitamin_frac"] = 0.10
        cost_vf = isru_ops_cost(ns, baseline)
        # The ISRU ops component is reduced (multiplied by 0.9),
        # but Earth cost is added. Net should still be > baseline
        # because Earth unit cost >> ISRU ops cost.
        assert np.all(cost_vf > cost_base)

    def test_less_penalty_than_additive(self):
        """Corrected formula gives lower cost than naive additive formula."""
        p = BASELINE.copy()
        ns = np.array([100.0, 1000.0])
        # Compute with corrected formula
        p["vitamin_frac"] = 0.10
        cost_corrected = isru_ops_cost(ns, p)
        # Compute naive additive: c_ops + 0.10 * c_earth
        p["vitamin_frac"] = 0.0
        cost_base = isru_ops_cost(ns, p)
        cost_naive = cost_base + 0.10 * earth_unit_cost(ns, p)
        # Corrected should be less than naive (by 0.10 * c_ops)
        assert np.all(cost_corrected < cost_naive)


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
