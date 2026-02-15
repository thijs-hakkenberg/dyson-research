"""Monte Carlo engine for the ISRU Economic Crossover paper.

Provides sampling, loop execution, statistics computation, and correlation
analysis as composable functions. No matplotlib, no prints.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from numpy import floating, array, clip, empty, percentile, sum, mean, median, std as np_std, sqrt as np_sqrt
from numpy.random import Generator
from numpy.linalg import cholesky 
from numpy.typing import NDArray
from scipy.stats import norm as sp_norm, spearmanr

from isru_model import (
    BASELINE,
    Params,
    find_crossover_npv,
    significance_stars,
)

NDFloat = NDArray[floating[Any]]

# ---------------------------------------------------------------------------
# Result dataclasses
# ---------------------------------------------------------------------------

@dataclass
class ConvergenceStats:
    """Statistics from a MC ensemble."""
    median: float
    q25: float
    q75: float
    p10: float
    p90: float
    cond_median: float
    cond_q25: float
    cond_q75: float
    cond_p10: float
    cond_p90: float
    ci_cond_median: NDFloat
    convergence_rate: float
    p_below_h: dict[int, float]


@dataclass
class SpearmanResult:
    """Spearman rank correlation for one parameter."""
    name: str
    rho: float
    p_val: float
    stars: str


@dataclass
class NonConvergenceProfile:
    """Characterization of non-convergence drivers."""
    non_conv_drivers: dict[str, tuple[float, float]]
    non_conv_by_K: dict[str, float]


@dataclass
class MCResult:
    """Full result of a Monte Carlo run."""
    r_fixed: float
    crossovers: NDFloat
    converged_mask: NDFloat
    stats: ConvergenceStats
    spearman: list[SpearmanResult]
    spearman_conditional: list[SpearmanResult]
    non_convergence_profile: NonConvergenceProfile
    param_arrays: dict[str, NDFloat]
    N_MAX_MC: int
    convergence_drivers: list[tuple[str, float]] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Sampling
# ---------------------------------------------------------------------------
def sample_mc_params(
    rng: Generator,
    n_runs: int,
    *,
    rho: float = 0.3,
    correlated: bool = True,
) -> dict[str, NDFloat]:
    """Sample MC parameter arrays.

    Parameters
    ----------
    rng : numpy Generator
    n_runs : int
    rho : float
        Correlation between p_launch and K (Gaussian copula).
    correlated : bool
        If False, sample p_launch and K independently (uniform).
    """
    if correlated:
        cov_matrix = array([[1.0, rho], [rho, 1.0]])
        L = cholesky(cov_matrix)
        z = rng.standard_normal((n_runs, 2))
        corr_normals = z @ L.T
        u_launch = sp_norm.cdf(corr_normals[:, 0])
        u_capital = sp_norm.cdf(corr_normals[:, 1])
        p_launch_samples = 500 + u_launch * (2000 - 500)
        k_samples = 30e9 + u_capital * (100e9 - 30e9)
    else:
        p_launch_samples = rng.uniform(500, 2000, n_runs)
        k_samples = rng.uniform(30e9, 100e9, n_runs)

    return {
        "p_launch": p_launch_samples,
        "K": k_samples,
        "LR_E": clip(rng.normal(0.85, 0.03, n_runs), 0.75, 0.95),
        "LR_I": clip(rng.normal(0.90, 0.03, n_runs), 0.80, 0.98),
        "t0": rng.uniform(3, 8, n_runs),
        "C_ops1": rng.uniform(2e6, 10e6, n_runs),
        "C_mfg1": rng.uniform(50e6, 100e6, n_runs),
        "alpha": rng.uniform(1.0, 2.0, n_runs),
        "p_transport": rng.uniform(50, 300, n_runs),
        "C_floor": rng.uniform(0.3e6, 2.0e6, n_runs),
        "prod_rate": rng.uniform(250, 750, n_runs),
    }


def run_mc_loop(
    param_arrays: dict[str, NDFloat],
    r_fixed: float,
    n_max: int,
) -> NDFloat:
    """Execute the MC loop: for each sample, compute crossover at fixed r.

    Returns array of crossover values.
    """
    n_runs = len(next(iter(param_arrays.values())))
    crossovers = empty(n_runs, dtype=float)
    for i in range(n_runs):
        p = BASELINE.copy()
        for name, arr in param_arrays.items():
            p[name] = arr[i]
        p["r"] = r_fixed
        crossovers[i] = find_crossover_npv(p, N_max=n_max)
    return crossovers


def compute_convergence_stats(
    crossovers: NDFloat,
    n_max_mc: int,
    rng: Generator,
    *,
    n_boot: int = 5000,
    horizons: list[int] | None = None,
) -> ConvergenceStats:
    """Compute convergence and bootstrap statistics from crossover array."""
    if horizons is None:
        horizons = [1000, 2000, 5000, 10000, 20000, 40000]

    n_runs = len(crossovers)
    converged_mask = crossovers < n_max_mc
    n_converged = int(sum(converged_mask))
    convergence_rate = n_converged / n_runs * 100

    p_below_h = {h: float(mean(crossovers <= h) * 100) for h in horizons}

    # Unconditional statistics
    calc_median = float(median(crossovers))
    q25, q75 = [float(x) for x in percentile(crossovers, [25, 75])]
    p10, p90 = [float(x) for x in percentile(crossovers, [10, 90])]

    # Conditional statistics
    if n_converged > 0:
        cond_crossovers = crossovers[converged_mask]
        cond_median = float(median(cond_crossovers))
        cond_q25, cond_q75 = [float(x) for x in percentile(cond_crossovers, [25, 75])]
        cond_p10, cond_p90 = [float(x) for x in percentile(cond_crossovers, [10, 90])]
    else:
        cond_median = cond_q25 = cond_q75 = cond_p10 = cond_p90 = float(n_max_mc)

    # Bootstrap confidence intervals
    boot_cond_medians = empty(n_boot)
    for b in range(n_boot):
        boot_sample = rng.choice(crossovers, size=n_runs, replace=True)
        boot_conv = boot_sample[boot_sample < n_max_mc]
        boot_cond_medians[b] = median(boot_conv) if len(boot_conv) > 0 else n_max_mc
    ci_cond_median = percentile(boot_cond_medians, [2.5, 97.5])

    return ConvergenceStats(
        median=calc_median, q25=q25, q75=q75, p10=p10, p90=p90,
        cond_median=cond_median, cond_q25=cond_q25, cond_q75=cond_q75,
        cond_p10=cond_p10, cond_p90=cond_p90,
        ci_cond_median=ci_cond_median,
        convergence_rate=convergence_rate,
        p_below_h=p_below_h,
    )


def compute_spearman_correlations(
    param_arrays: dict[str, NDFloat],
    crossovers: NDFloat,
    *,
    mask: NDFloat | None = None,
) -> list[SpearmanResult]:
    """Compute Spearman rank correlations between params and crossovers."""
    results = []
    for name, arr in param_arrays.items():
        if mask is not None:
            a, c = arr[mask], crossovers[mask]
        else:
            a, c = arr, crossovers
        corr, p_val = spearmanr(a, c)
        results.append(SpearmanResult(
            name=name, rho=float(corr), p_val=float(p_val),
            stars=significance_stars(float(p_val)),
        ))
    return results


def characterize_nonconvergence(
    param_arrays: dict[str, NDFloat],
    converged_mask: NDFloat,
    crossovers: NDFloat,
    n_max_mc: int,
    *,
    k_buckets: list[tuple[float, float, str]] | None = None,
) -> NonConvergenceProfile:
    """Characterize drivers of non-convergence."""
    if k_buckets is None:
        k_buckets = [
            (30e9, 50e9, "$30-50B"),
            (50e9, 75e9, "$50-75B"),
            (75e9, 100e9, "$75-100B"),
        ]

    n_converged = int(sum(converged_mask))
    n_runs = len(converged_mask)

    non_conv_drivers: dict[str, tuple[float, float]] = {}
    if n_converged > 100 and (n_runs - n_converged) > 100:
        for name, arr in param_arrays.items():
            mean_conv = float(mean(arr[converged_mask]))
            mean_nonconv = float(mean(arr[~converged_mask]))
            non_conv_drivers[name] = (mean_conv, mean_nonconv)

    k_samples = param_arrays["K"]
    non_conv_by_K: dict[str, float] = {}
    for lo, hi, label in k_buckets:
        bucket_mask = (k_samples >= lo) & (k_samples < hi)
        if sum(bucket_mask) > 0:
            non_conv_by_K[label] = float(
                (1 - mean(crossovers[bucket_mask] < n_max_mc)) * 100
            )

    return NonConvergenceProfile(
        non_conv_drivers=non_conv_drivers,
        non_conv_by_K=non_conv_by_K,
    )


def compute_convergence_drivers(
    param_arrays: dict[str, NDFloat],
    converged_mask: NDFloat,
) -> list[tuple[str, float]]:
    """Censoring-aware analysis: standardized mean difference for each param.

    Computes Cohen's d between converged and non-converged groups for each
    parameter, ranking by |d|. This avoids the censoring bias in Spearman
    correlations (which treat non-converged runs as tied at H).
    """
    n_conv = int(sum(converged_mask))
    n_nonconv = int(sum(~converged_mask))
    if n_conv < 30 or n_nonconv < 30:
        return []

    results = []
    for name, arr in param_arrays.items():
        m_conv = float(mean(arr[converged_mask]))
        m_nonconv = float(mean(arr[~converged_mask]))
        s_conv = float(np_std(arr[converged_mask], ddof=1))
        s_nonconv = float(np_std(arr[~converged_mask], ddof=1))
        # Pooled standard deviation
        s_pooled = float(np_sqrt(
            ((n_conv - 1) * s_conv**2 + (n_nonconv - 1) * s_nonconv**2)
            / (n_conv + n_nonconv - 2)
        ))
        d = (m_conv - m_nonconv) / s_pooled if s_pooled > 0 else 0.0
        results.append((name, d))

    results.sort(key=lambda x: abs(x[1]), reverse=True)
    return results


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------
def run_mc(
    r_fixed: float,
    rng: Generator,
    n_runs: int = 10000,
    n_max_mc: int = 40000,
) -> MCResult:
    """Run full Monte Carlo at a fixed discount rate.

    This is the thin orchestrator that composes sampling, loop, stats,
    correlations, and non-convergence analysis.
    """
    param_arrays = sample_mc_params(rng, n_runs, rho=0.3, correlated=True)
    crossovers = run_mc_loop(param_arrays, r_fixed, n_max_mc)

    converged_mask = crossovers < n_max_mc
    n_converged = int(sum(converged_mask))

    stats = compute_convergence_stats(crossovers, n_max_mc, rng)

    spearman = compute_spearman_correlations(param_arrays, crossovers)
    spearman_conditional = (
        compute_spearman_correlations(
            param_arrays, crossovers, mask=converged_mask
        )
        if n_converged > 100
        else []
    )

    nonconv = characterize_nonconvergence(
        param_arrays, converged_mask, crossovers, n_max_mc
    )

    conv_drivers = compute_convergence_drivers(param_arrays, converged_mask)

    return MCResult(
        r_fixed=r_fixed,
        crossovers=crossovers,
        converged_mask=converged_mask,
        stats=stats,
        spearman=spearman,
        spearman_conditional=spearman_conditional,
        non_convergence_profile=nonconv,
        param_arrays=param_arrays,
        N_MAX_MC=n_max_mc,
        convergence_drivers=conv_drivers,
    )
