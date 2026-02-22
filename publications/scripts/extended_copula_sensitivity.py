#!/usr/bin/env python3
"""AE1: Extended 6D copula sensitivity analysis.

Compares the baseline 3D Gaussian copula (p_launch, K, prod_rate) with an
extended 6D copula that adds correlations between K and three additional
parameters: t0, availability (A), and C_ops1.

Rationale (reviewer consensus):
  - rho(K, t0) = +0.4   — bigger facility → longer ramp-up
  - rho(K, A)  = -0.3   — bigger facility → more downtime
  - rho(K, C_ops1) = +0.3 — bigger facility → higher initial ops

All other new off-diagonals = 0. Existing rho(p,K)=0.3, rho(K,n)=0.5 preserved.

Usage:
    cd publications/scripts
    python extended_copula_sensitivity.py
"""

from __future__ import annotations

__version__ = "1.0.0"

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from numpy import array, clip, exp as np_exp, log as np_log, mean, median
from numpy.linalg import cholesky
from numpy.random import default_rng
from scipy.stats import norm as sp_norm

from isru_mc import run_mc_loop, compute_convergence_stats
from isru_model import BASELINE


def sample_mc_params_6d(
    rng,
    n_runs: int,
    sigma_ln: float = 0.70,
):
    """Sample MC params with the extended 6D copula.

    Correlated variables (in order):
      0: p_launch   (uniform marginal)
      1: K          (log-normal marginal)
      2: prod_rate  (uniform marginal)
      3: t0         (uniform marginal)
      4: A          (uniform marginal, availability)
      5: C_ops1     (uniform marginal)

    Correlation matrix preserves existing 3D structure and adds:
      rho(K, t0)    = +0.4
      rho(K, A)     = -0.3
      rho(K, C_ops1)= +0.3
    """
    # 6D correlation matrix
    #          p_L    K      n_dot  t0     A      C_ops1
    corr = array([
        [1.0,   0.3,   0.0,   0.0,   0.0,   0.0],   # p_launch
        [0.3,   1.0,   0.5,   0.4,  -0.3,   0.3],   # K
        [0.0,   0.5,   1.0,   0.0,   0.0,   0.0],   # prod_rate
        [0.0,   0.4,   0.0,   1.0,   0.0,   0.0],   # t0
        [0.0,  -0.3,   0.0,   0.0,   1.0,   0.0],   # A (availability)
        [0.0,   0.3,   0.0,   0.0,   0.0,   1.0],   # C_ops1
    ])
    L = cholesky(corr)
    z = rng.standard_normal((n_runs, 6))
    corr_normals = z @ L.T

    # Transform to uniform marginals via CDF
    u = sp_norm.cdf(corr_normals)

    # Apply marginal distributions
    p_launch_samples = 500 + u[:, 0] * (2000 - 500)

    # Log-normal K
    mu_ln = float(np_log(65e9))
    ln_k = sp_norm.ppf(u[:, 1]) * sigma_ln + mu_ln
    k_samples = np_exp(ln_k)
    k_samples = clip(k_samples, 20e9, 200e9)

    prod_rate_samples = 250 + u[:, 2] * (750 - 250)
    t0_samples = 3 + u[:, 3] * (8 - 3)
    availability_samples = 0.70 + u[:, 4] * (0.95 - 0.70)
    C_ops1_samples = 2e6 + u[:, 5] * (10e6 - 2e6)

    # Remaining params: independent (same as baseline)
    C_mfg1_samples = rng.uniform(50e6, 100e6, n_runs)
    C_mat_samples = rng.uniform(0.5e6, 2e6, n_runs)
    C_labor1_samples = C_mfg1_samples - C_mat_samples
    p_fuel_samples = rng.uniform(100, 400, n_runs)

    return {
        "p_launch": p_launch_samples,
        "K": k_samples,
        "LR_E": clip(rng.normal(0.85, 0.03, n_runs), 0.75, 0.95),
        "LR_I": clip(rng.normal(0.90, 0.03, n_runs), 0.80, 0.98),
        "t0": t0_samples,
        "C_ops1": C_ops1_samples,
        "C_mfg1": C_mfg1_samples,
        "C_mat": C_mat_samples,
        "C_labor1": C_labor1_samples,
        "alpha": rng.uniform(1.0, 2.0, n_runs),
        "p_transport": rng.uniform(50, 300, n_runs),
        "C_floor": rng.uniform(0.3e6, 2.0e6, n_runs),
        "prod_rate": prod_rate_samples,
        "availability": availability_samples,
        "p_fuel": p_fuel_samples,
        "tau_transport": rng.uniform(0.25, 2.0, n_runs),
    }


def sample_mc_params_3d(rng, n_runs: int, sigma_ln: float = 0.70):
    """Baseline 3D copula sampling (matches isru_mc.sample_mc_params)."""
    corr_3d = array([
        [1.0, 0.3, 0.0],
        [0.3, 1.0, 0.5],
        [0.0, 0.5, 1.0],
    ])
    L = cholesky(corr_3d)
    z = rng.standard_normal((n_runs, 3))
    corr_normals = z @ L.T
    u_launch = sp_norm.cdf(corr_normals[:, 0])
    u_capital = sp_norm.cdf(corr_normals[:, 1])
    u_prod = sp_norm.cdf(corr_normals[:, 2])

    p_launch_samples = 500 + u_launch * (2000 - 500)
    prod_rate_samples = 250 + u_prod * (750 - 250)

    mu_ln = float(np_log(65e9))
    ln_k = sp_norm.ppf(u_capital) * sigma_ln + mu_ln
    k_samples = np_exp(ln_k)
    k_samples = clip(k_samples, 20e9, 200e9)

    C_mfg1_samples = rng.uniform(50e6, 100e6, n_runs)
    C_mat_samples = rng.uniform(0.5e6, 2e6, n_runs)
    C_labor1_samples = C_mfg1_samples - C_mat_samples
    p_fuel_samples = rng.uniform(100, 400, n_runs)

    return {
        "p_launch": p_launch_samples,
        "K": k_samples,
        "LR_E": clip(rng.normal(0.85, 0.03, n_runs), 0.75, 0.95),
        "LR_I": clip(rng.normal(0.90, 0.03, n_runs), 0.80, 0.98),
        "t0": rng.uniform(3, 8, n_runs),
        "C_ops1": rng.uniform(2e6, 10e6, n_runs),
        "C_mfg1": C_mfg1_samples,
        "C_mat": C_mat_samples,
        "C_labor1": C_labor1_samples,
        "alpha": rng.uniform(1.0, 2.0, n_runs),
        "p_transport": rng.uniform(50, 300, n_runs),
        "C_floor": rng.uniform(0.3e6, 2.0e6, n_runs),
        "prod_rate": prod_rate_samples,
        "availability": rng.uniform(0.70, 0.95, n_runs),
        "p_fuel": p_fuel_samples,
        "tau_transport": rng.uniform(0.25, 2.0, n_runs),
    }


def main():
    seed = 42
    n_runs = 10_000
    r_fixed = 0.05
    n_max = 40_000

    print(f"Extended Copula Sensitivity Analysis (AE1)")
    print(f"{'='*60}")
    print(f"Runs: {n_runs}, r={r_fixed}, H={n_max}, seed={seed}")
    print()

    # --- Baseline 3D copula ---
    rng_3d = default_rng(seed)
    params_3d = sample_mc_params_3d(rng_3d, n_runs)
    crossovers_3d, perm_3d, clamp_3d = run_mc_loop(params_3d, r_fixed, n_max)
    stats_3d = compute_convergence_stats(crossovers_3d, n_max, default_rng(seed + 1))

    print(f"3D Copula (baseline):")
    print(f"  Convergence rate: {stats_3d.convergence_rate:.1f}%")
    print(f"  Conditional median: {stats_3d.cond_median:,.0f}")
    print(f"  95% CI: [{stats_3d.ci_cond_median[0]:,.0f}, {stats_3d.ci_cond_median[1]:,.0f}]")
    print()

    # --- Extended 6D copula (same seed for comparability) ---
    rng_6d = default_rng(seed)
    params_6d = sample_mc_params_6d(rng_6d, n_runs)
    crossovers_6d, perm_6d, clamp_6d = run_mc_loop(params_6d, r_fixed, n_max)
    stats_6d = compute_convergence_stats(crossovers_6d, n_max, default_rng(seed + 1))

    print(f"6D Copula (extended):")
    print(f"  Convergence rate: {stats_6d.convergence_rate:.1f}%")
    print(f"  Conditional median: {stats_6d.cond_median:,.0f}")
    print(f"  95% CI: [{stats_6d.ci_cond_median[0]:,.0f}, {stats_6d.ci_cond_median[1]:,.0f}]")
    print()

    # --- Comparison ---
    delta_conv = stats_6d.convergence_rate - stats_3d.convergence_rate
    delta_cmed = stats_6d.cond_median - stats_3d.cond_median

    print(f"Comparison (6D vs 3D):")
    print(f"  Convergence shift: {delta_conv:+.1f} pp")
    print(f"  Conditional median shift: {delta_cmed:+,.0f} units")
    print()

    # --- Summary table for paper ---
    print(f"{'='*60}")
    print(f"For Appendix A table:")
    print(f"{'Copula':<12} {'Conv. %':>10} {'Cond. med.':>12} {'Shift (pp)':>12}")
    print(f"{'-'*46}")
    print(f"{'3D (base)':<12} {stats_3d.convergence_rate:>9.1f}% {stats_3d.cond_median:>11,.0f} {'---':>12}")
    print(f"{'6D (ext.)':<12} {stats_6d.convergence_rate:>9.1f}% {stats_6d.cond_median:>11,.0f} {delta_conv:>+11.1f}")


if __name__ == "__main__":
    main()
