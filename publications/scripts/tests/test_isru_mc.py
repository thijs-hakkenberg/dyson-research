"""Tests for isru_mc — Monte Carlo engine."""

import numpy as np
import pytest

from isru_mc import (
    MCResult,
    characterize_nonconvergence,
    compute_convergence_stats,
    compute_prcc,
    compute_spearman_correlations,
    run_mc,
    run_mc_loop,
    sample_mc_params,
)


class TestSampleMCParams:
    def test_output_shapes(self, rng):
        params = sample_mc_params(rng, 100)
        for name, arr in params.items():
            assert arr.shape == (100,), f"{name} has wrong shape"

    def test_all_params_present(self, rng):
        params = sample_mc_params(rng, 10)
        expected = {
            "p_launch", "K", "LR_E", "LR_I", "t0", "C_ops1", "C_mfg1",
            "C_mat", "C_labor1",
            "alpha", "p_transport", "C_floor", "prod_rate", "availability",
            "p_fuel",
        }
        assert set(params.keys()) == expected

    def test_ranges_respected(self, rng):
        params = sample_mc_params(rng, 10000)
        assert np.all(params["p_launch"] >= 500) and np.all(params["p_launch"] <= 2000)
        assert np.all(params["K"] >= 20e9) and np.all(params["K"] <= 200e9)
        assert np.all(params["LR_E"] >= 0.75) and np.all(params["LR_E"] <= 0.95)
        assert np.all(params["LR_I"] >= 0.80) and np.all(params["LR_I"] <= 0.98)
        assert np.all(params["t0"] >= 3) and np.all(params["t0"] <= 8)
        assert np.all(params["C_ops1"] >= 2e6) and np.all(params["C_ops1"] <= 10e6)
        assert np.all(params["C_mfg1"] >= 50e6) and np.all(params["C_mfg1"] <= 100e6)
        assert np.all(params["alpha"] >= 1.0) and np.all(params["alpha"] <= 2.0)
        assert np.all(params["p_transport"] >= 50) and np.all(params["p_transport"] <= 300)
        assert np.all(params["C_floor"] >= 0.3e6) and np.all(params["C_floor"] <= 2.0e6)
        assert np.all(params["prod_rate"] >= 250) and np.all(params["prod_rate"] <= 750)
        assert np.all(params["p_fuel"] >= 100) and np.all(params["p_fuel"] <= 400)

    def test_correlated_vs_uncorrelated(self, rng):
        """Correlated samples should have positive correlation between p_launch and K."""
        rng1 = np.random.default_rng(42)
        corr_params = sample_mc_params(rng1, 5000, correlated=True)
        from scipy.stats import pearsonr
        r_corr, _ = pearsonr(corr_params["p_launch"], corr_params["K"])

        rng2 = np.random.default_rng(42)
        uncorr_params = sample_mc_params(rng2, 5000, correlated=False)
        r_uncorr, _ = pearsonr(uncorr_params["p_launch"], uncorr_params["K"])

        # Correlated should show meaningful positive correlation
        assert r_corr > 0.15
        # Uncorrelated should be near zero
        assert abs(r_uncorr) < 0.1


class TestSigmaLn:
    """Z5: Verify sigma_ln parameter controls K tail heaviness."""

    def test_default_sigma_matches(self, rng):
        """Default sigma_ln=0.70 should match hardcoded behavior."""
        rng1 = np.random.default_rng(42)
        params1 = sample_mc_params(rng1, 1000, rho=0.3, correlated=True)
        rng2 = np.random.default_rng(42)
        params2 = sample_mc_params(rng2, 1000, rho=0.3, correlated=True, sigma_ln=0.70)
        np.testing.assert_array_equal(params1["K"], params2["K"])

    def test_higher_sigma_wider_spread(self, rng):
        """Higher sigma_ln should give wider K spread (P90/P10 ratio)."""
        rng1 = np.random.default_rng(42)
        params_narrow = sample_mc_params(rng1, 5000, rho=0.3, correlated=True, sigma_ln=0.70)
        rng2 = np.random.default_rng(42)
        params_wide = sample_mc_params(rng2, 5000, rho=0.3, correlated=True, sigma_ln=1.3)

        k_narrow = params_narrow["K"]
        k_wide = params_wide["K"]

        ratio_narrow = float(np.percentile(k_narrow, 90)) / float(np.percentile(k_narrow, 10))
        ratio_wide = float(np.percentile(k_wide, 90)) / float(np.percentile(k_wide, 10))

        assert ratio_wide > ratio_narrow

    def test_sigma_works_uncorrelated(self, rng):
        """sigma_ln should also work with uncorrelated sampling."""
        rng1 = np.random.default_rng(42)
        params = sample_mc_params(rng1, 1000, correlated=False, sigma_ln=1.0)
        assert np.all(params["K"] >= 20e9)
        assert np.all(params["K"] <= 200e9)


class TestRunMCLoop:
    def test_output_shape(self, rng):
        params = sample_mc_params(rng, 50)
        crossovers, perm = run_mc_loop(params, 0.05, 5000)
        assert crossovers.shape == (50,)
        assert perm.shape == (50,)

    def test_all_positive(self, rng):
        params = sample_mc_params(rng, 50)
        crossovers, _ = run_mc_loop(params, 0.05, 5000)
        assert np.all(crossovers > 0)

    def test_bounded_by_n_max(self, rng):
        params = sample_mc_params(rng, 50)
        N_max = 5000
        crossovers, _ = run_mc_loop(params, 0.05, N_max)
        assert np.all(crossovers <= N_max)


class TestConvergenceStats:
    def test_rate_in_range(self, rng):
        crossovers = rng.uniform(1000, 40000, 100)
        stats = compute_convergence_stats(crossovers, 40000, rng, n_boot=100)
        assert 0 <= stats.convergence_rate <= 100

    def test_cond_median_lte_unconditional(self, rng):
        """Conditional median (excluding censored) should be <= unconditional."""
        crossovers = np.concatenate([
            rng.uniform(1000, 10000, 80),
            np.full(20, 40000.0),  # 20% censored
        ])
        stats = compute_convergence_stats(crossovers, 40000, rng, n_boot=100)
        assert stats.cond_median <= stats.median

    def test_ci_contains_estimate(self, rng):
        crossovers = rng.uniform(2000, 8000, 500)
        stats = compute_convergence_stats(crossovers, 40000, rng, n_boot=1000)
        lo, hi = stats.ci_cond_median
        assert lo <= stats.cond_median <= hi

    def test_all_converged(self, rng):
        crossovers = rng.uniform(1000, 5000, 100)
        stats = compute_convergence_stats(crossovers, 40000, rng, n_boot=100)
        assert stats.convergence_rate == pytest.approx(100.0)


class TestSpearmanCorrelations:
    def _make_test_data(self, rng, n=500):
        """Create correlated test data with known relationships."""
        K = rng.uniform(30e9, 100e9, n)
        # Higher K → later crossover (positive correlation)
        crossovers = 3000 + K / 1e9 * 50 + rng.normal(0, 500, n)
        param_arrays = {"K": K, "other": rng.uniform(0, 1, n)}
        return param_arrays, crossovers

    def test_k_positive(self, rng):
        params, crossovers = self._make_test_data(rng)
        results = compute_spearman_correlations(params, crossovers)
        k_result = next(r for r in results if r.name == "K")
        assert k_result.rho > 0

    def test_other_near_zero(self, rng):
        params, crossovers = self._make_test_data(rng)
        results = compute_spearman_correlations(params, crossovers)
        other_result = next(r for r in results if r.name == "other")
        assert abs(other_result.rho) < 0.15

    def test_with_mask(self, rng):
        params, crossovers = self._make_test_data(rng, n=200)
        mask = crossovers < np.median(crossovers)
        results = compute_spearman_correlations(params, crossovers, mask=mask)
        assert len(results) == 2


class TestPRCC:
    """U2: Verify PRCC computation."""

    def test_returns_results(self, rng):
        """PRCC should return one result per parameter."""
        K = rng.uniform(30e9, 100e9, 200)
        other = rng.uniform(0, 1, 200)
        crossovers = 3000 + K / 1e9 * 50 + rng.normal(0, 500, 200)
        param_arrays = {"K": K, "other": other}
        results = compute_prcc(param_arrays, crossovers)
        assert len(results) == 2

    def test_k_positive(self, rng):
        """K should have positive PRCC (higher K -> later crossover)."""
        K = rng.uniform(30e9, 100e9, 500)
        other = rng.uniform(0, 1, 500)
        crossovers = 3000 + K / 1e9 * 50 + rng.normal(0, 500, 500)
        param_arrays = {"K": K, "other": other}
        results = compute_prcc(param_arrays, crossovers)
        k_result = next(r for r in results if r.name == "K")
        assert k_result.prcc > 0

    def test_resolves_confounding(self, rng):
        """PRCC should resolve confounding from correlations."""
        n = 500
        # Create correlated X1 and X2
        X1 = rng.uniform(0, 1, n)
        X2 = 0.5 * X1 + 0.5 * rng.uniform(0, 1, n)
        # Y depends only on X1 (not X2)
        Y = 10 * X1 + rng.normal(0, 1, n)
        results = compute_prcc({"X1": X1, "X2": X2}, Y)
        x1_prcc = next(r for r in results if r.name == "X1").prcc
        x2_prcc = next(r for r in results if r.name == "X2").prcc
        # X1's PRCC should be much larger than X2's
        assert abs(x1_prcc) > abs(x2_prcc) * 2


class TestNonconvergenceRate:
    def test_higher_K_more_nonconvergence(self, rng):
        """Higher K should lead to more non-convergence."""
        params = sample_mc_params(rng, 500)
        # Make some crossovers > N_MAX for high-K runs
        crossovers = np.where(params["K"] > 70e9, 40000.0, 3000.0)
        converged_mask = crossovers < 40000
        nonconv = characterize_nonconvergence(
            params, converged_mask, crossovers, 40000
        )
        # Higher K bucket should have more non-convergence
        if "$30-50B" in nonconv.non_conv_by_K and "$75-100B" in nonconv.non_conv_by_K:
            assert nonconv.non_conv_by_K["$75-100B"] > nonconv.non_conv_by_K["$30-50B"]


class TestRunMCIntegration:
    @pytest.mark.slow
    def test_full_run_produces_valid_result(self):
        rng = np.random.default_rng(42)
        result = run_mc(0.05, rng, n_runs=500, n_max_mc=20000)
        assert isinstance(result, MCResult)
        assert result.r_fixed == 0.05
        assert len(result.crossovers) == 500
        assert 0 <= result.stats.convergence_rate <= 100
        assert len(result.spearman) == 15  # 15 parameters (incl. C_mat, C_labor1, p_fuel)

    @pytest.mark.slow
    def test_reproducible_with_same_seed(self):
        rng1 = np.random.default_rng(123)
        res1 = run_mc(0.05, rng1, n_runs=200, n_max_mc=10000)

        rng2 = np.random.default_rng(123)
        res2 = run_mc(0.05, rng2, n_runs=200, n_max_mc=10000)

        np.testing.assert_array_equal(res1.crossovers, res2.crossovers)
