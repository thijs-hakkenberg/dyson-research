"""Monte Carlo engine for the ISRU Economic Crossover paper.

Provides sampling, loop execution, statistics computation, and correlation
analysis as composable functions. No matplotlib, no prints.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from numpy import (
    floating, array, clip, empty, exp as np_exp, log as np_log,
    percentile, sum, mean, median, std as np_std, sqrt as np_sqrt,
    argsort, unique, zeros_like, inf,
)
from numpy.random import Generator
from numpy.linalg import cholesky
from numpy.typing import NDArray
from scipy.stats import norm as sp_norm, spearmanr

from isru_model import (
    BASELINE,
    Params,
    find_crossover,
    find_crossover_npv,
    is_permanent_crossover,
    significance_stars,
)
from scipy.stats import rankdata

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
class PRCCResult:
    """Partial Rank Correlation Coefficient for one parameter."""
    name: str
    prcc: float
    p_val: float
    stars: str


@dataclass
class NonConvergenceProfile:
    """Characterization of non-convergence drivers."""
    non_conv_drivers: dict[str, tuple[float, float]]
    non_conv_by_K: dict[str, float]


@dataclass
class SobolResult:
    """First-order variance decomposition (rank-regression R² based)."""
    param_r2: dict[str, float]           # individual R² for each parameter
    top_k_cumulative_r2: list[tuple[str, float]]  # cumulative R² in order of importance
    total_r2: float                       # full model R²


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
    prcc: list[PRCCResult] = field(default_factory=list)
    prcc_conditional: list[PRCCResult] = field(default_factory=list)
    permanent_mask: NDFloat = field(default_factory=lambda: array([]))
    n_permanent: int = 0
    n_transient: int = 0
    sobol: SobolResult | None = None
    sobol_conditional: SobolResult | None = None
    n_clamped: int = 0  # AD2: count of runs with coherence clamping


# ---------------------------------------------------------------------------
# Sampling
# ---------------------------------------------------------------------------
def sample_mc_params(
    rng: Generator,
    n_runs: int,
    *,
    rho: float = 0.3,
    rho_k_prod: float = 0.5,
    correlated: bool = True,
    k_distribution: str = "lognormal",
    sigma_ln: float = 0.70,
    k_clip_upper: float = 200e9,
) -> dict[str, NDFloat]:
    """Sample MC parameter arrays.

    Parameters
    ----------
    rng : numpy Generator
    n_runs : int
    rho : float
        Correlation between p_launch and K (Gaussian copula).
    rho_k_prod : float
        Correlation between K and prod_rate (Gaussian copula).
        Reflects that higher-capacity facilities require larger capital.
    correlated : bool
        If False, sample p_launch, K, and prod_rate independently (uniform).
    k_distribution : str
        "lognormal" (default) or "uniform". Log-normal calibrated to
        median=$65B with σ_ln (Flyvbjerg megaproject reference class),
        clipped to [20B, 200B].
    sigma_ln : float
        Log-normal standard deviation for K distribution (default 0.70).
        Higher values give heavier tails (Z5 sensitivity test).
    k_clip_upper : float
        Upper clip bound for K in dollars (default 200e9).
        Used for K-clip sensitivity analysis (AA2).
    """
    if correlated:
        # 3D Gaussian copula: (p_launch, K, prod_rate)
        cov_matrix = array([
            [1.0,  rho,       0.0],
            [rho,  1.0,       rho_k_prod],
            [0.0,  rho_k_prod, 1.0],
        ])
        L = cholesky(cov_matrix)
        z = rng.standard_normal((n_runs, 3))
        corr_normals = z @ L.T
        u_launch = sp_norm.cdf(corr_normals[:, 0])
        u_capital = sp_norm.cdf(corr_normals[:, 1])
        u_prod = sp_norm.cdf(corr_normals[:, 2])
        p_launch_samples = 500 + u_launch * (2000 - 500)
        prod_rate_samples = 250 + u_prod * (750 - 250)

        if k_distribution == "lognormal":
            # Y1: Log-normal K calibrated to Flyvbjerg megaproject data:
            # median=$65B, σ_ln parameterized (default 0.70, P90/P50≈2.5×,
            # conservative end of Flyvbjerg's 2-4× range for large infrastructure)
            mu_ln = float(np_log(65e9))
            # Transform copula uniform to log-normal via inverse CDF
            ln_k = sp_norm.ppf(u_capital) * sigma_ln + mu_ln
            k_samples = np_exp(ln_k)
            k_samples = clip(k_samples, 20e9, k_clip_upper)
        else:
            k_samples = 30e9 + u_capital * (100e9 - 30e9)
    else:
        p_launch_samples = rng.uniform(500, 2000, n_runs)
        prod_rate_samples = rng.uniform(250, 750, n_runs)

        if k_distribution == "lognormal":
            mu_ln = float(np_log(65e9))
            ln_k = rng.normal(mu_ln, sigma_ln, n_runs)
            k_samples = np_exp(ln_k)
            k_samples = clip(k_samples, 20e9, k_clip_upper)
        else:
            k_samples = rng.uniform(30e9, 100e9, n_runs)

    # U1: Sample C_mfg1 and split into C_mat (fixed) + C_labor1 (learnable)
    C_mfg1_samples = rng.uniform(50e6, 100e6, n_runs)
    C_mat_samples = rng.uniform(0.5e6, 2e6, n_runs)
    C_labor1_samples = C_mfg1_samples - C_mat_samples

    # Y2: p_fuel sampled stochastically U[100, 400] $/kg to reflect
    # uncertainty in the operational asymptote (propellant + GEO delivery ops)
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
        "tau_transport": rng.uniform(0.25, 2.0, n_runs),  # AD1: lunar-to-GEO transport (years)
        # AK1: Stochastic learning plateau — Earth mfg learning saturates at
        # n_break with damping η, so cost exponent transitions from b to b*η.
        # n_break ~ U[200, 1000]: onset of saturation (within empirical base)
        # eta_earth ~ U[0.3, 0.7]: residual learning rate beyond n_break
        "n_break_earth": rng.uniform(200, 1000, n_runs),
        "eta_earth": rng.uniform(0.3, 0.7, n_runs),
        # AK2: Dynamic vitamin fraction — f_v decays from initial value toward
        # a floor as ISRU maturity grows.  vitamin_decay_n is the e-folding
        # scale (units); vitamin_frac_floor is the irreducible minimum.
        "vitamin_decay_n": rng.uniform(2000, 10000, n_runs),
        "vitamin_frac_floor": rng.uniform(0.01, 0.03, n_runs),
    }


def run_mc_loop(
    param_arrays: dict[str, NDFloat],
    r_fixed: float,
    n_max: int,
    *,
    baseline_override: dict[str, Any] | None = None,
    k_years: int | None = 5,
) -> tuple[NDFloat, NDFloat]:
    """Execute the MC loop: for each sample, compute crossover at fixed r.

    When the baseline has launch learning (b_L is set), the sampled p_launch
    is decomposed into fuel and ops components: p_fuel is held at the baseline
    value (irreducible propellant floor), and p_ops = p_launch - p_fuel
    captures the learnable operational component.

    Parameters
    ----------
    baseline_override : dict or None
        If provided, use this as the base parameter set instead of BASELINE.
        Used for product archetype comparisons (AA2).

    Returns (crossovers, permanent_mask) where permanent_mask[i] is True
    if run i has a permanent (not transient) crossover.
    """
    base = baseline_override if baseline_override is not None else BASELINE
    n_runs = len(next(iter(param_arrays.values())))
    crossovers = empty(n_runs, dtype=float)
    permanent = empty(n_runs, dtype=bool)
    n_clamped = 0
    for i in range(n_runs):
        p = base.copy()
        for name, arr in param_arrays.items():
            p[name] = arr[i]
        p["r"] = r_fixed
        # AD2: Coherence constraints — material can't exceed total mfg,
        # ops floor can't exceed first-unit ops
        clamped = False
        if p["C_mat"] >= p["C_mfg1"]:
            p["C_mat"] = p["C_mfg1"] * 0.1
            p["C_labor1"] = p["C_mfg1"] - p["C_mat"]
            clamped = True
        if p.get("C_floor", 0) >= p.get("C_ops1", 5e6):
            p["C_floor"] = p["C_ops1"] * 0.1
            clamped = True
        if clamped:
            n_clamped += 1
        # Decompose sampled p_launch into fuel/ops when launch learning is active
        # Y2: p_fuel is now sampled stochastically; use sampled value if present
        if p.get("b_L") is not None:
            p_fuel_val = p.get("p_fuel", base.get("p_fuel", 200))
            p_launch_sampled = p["p_launch"]
            p["p_fuel"] = p_fuel_val
            p["p_ops_launch"] = max(p_launch_sampled - p_fuel_val, 0)
        crossovers[i] = find_crossover(p, n_max, discount=True, phased_k_years=k_years)
        permanent[i] = is_permanent_crossover(p)
    return crossovers, permanent, n_clamped


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


def compute_prcc(
    param_arrays: dict[str, NDFloat],
    crossovers: NDFloat,
    *,
    mask: NDFloat | None = None,
) -> list[PRCCResult]:
    """Compute Partial Rank Correlation Coefficients.

    For each parameter X_i:
      1. Rank all variables.
      2. Regress rank(X_i) on ranks of all other parameters -> residuals R_Xi.
      3. Regress rank(Y) on ranks of all other parameters -> residuals R_Y.
      4. PRCC = Spearman(R_Xi, R_Y).

    PRCC isolates the effect of each parameter after removing the linear
    effects of all other parameters, resolving confounding from correlations
    (e.g., the launch cost sign reversal caused by the copula).
    """
    from numpy.linalg import lstsq

    names = list(param_arrays.keys())
    n_params = len(names)

    # Apply mask if provided
    if mask is not None:
        arrays = {k: v[mask] for k, v in param_arrays.items()}
        y = crossovers[mask]
    else:
        arrays = param_arrays
        y = crossovers

    n_obs = len(y)
    if n_obs < n_params + 2:
        return []

    # Build rank matrix (n_obs x n_params)
    rank_matrix = empty((n_obs, n_params))
    for j, name in enumerate(names):
        rank_matrix[:, j] = rankdata(arrays[name])

    rank_y = rankdata(y)

    results = []
    for i, name in enumerate(names):
        # Other parameter ranks (all columns except i)
        X_others = rank_matrix[:, [j for j in range(n_params) if j != i]]

        # Regress rank(X_i) on X_others
        # Add intercept column
        X_design = empty((n_obs, X_others.shape[1] + 1))
        X_design[:, 0] = 1.0
        X_design[:, 1:] = X_others
        coef_xi, _, _, _ = lstsq(X_design, rank_matrix[:, i], rcond=None)
        resid_xi = rank_matrix[:, i] - X_design @ coef_xi

        # Regress rank(Y) on X_others
        coef_y, _, _, _ = lstsq(X_design, rank_y, rcond=None)
        resid_y = rank_y - X_design @ coef_y

        # PRCC = Spearman correlation of residuals
        corr, p_val = spearmanr(resid_xi, resid_y)
        results.append(PRCCResult(
            name=name,
            prcc=float(corr),
            p_val=float(p_val),
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
# Variance decomposition (rank-regression R² approximation of Sobol S1)
# ---------------------------------------------------------------------------
def compute_variance_decomposition(
    param_arrays: dict[str, NDFloat],
    crossovers: NDFloat,
    *,
    mask: NDFloat | None = None,
) -> SobolResult:
    """Approximate first-order Sobol indices via rank-regression R².

    For each parameter X_i, computes R² from a univariate rank regression
    of rank(Y) on rank(X_i). Also fits a full multivariate rank regression
    and reports total R² and cumulative contribution.

    This is a computationally cheap approximation to Saltelli-style Sobol
    analysis that works well when the model is monotonic in most parameters.
    """
    from numpy.linalg import lstsq

    names = list(param_arrays.keys())
    n_params = len(names)

    if mask is not None:
        arrays = {k: v[mask] for k, v in param_arrays.items()}
        y = crossovers[mask]
    else:
        arrays = param_arrays
        y = crossovers

    n_obs = len(y)
    if n_obs < n_params + 2:
        return SobolResult(param_r2={}, top_k_cumulative_r2=[], total_r2=0.0)

    rank_y = rankdata(y)
    ss_total = float(((rank_y - rank_y.mean()) ** 2).sum())
    if ss_total == 0:
        return SobolResult(param_r2={}, top_k_cumulative_r2=[], total_r2=0.0)

    # Individual R² (univariate rank regression)
    param_r2: dict[str, float] = {}
    for name in names:
        rank_x = rankdata(arrays[name])
        X = empty((n_obs, 2))
        X[:, 0] = 1.0
        X[:, 1] = rank_x
        coef, _, _, _ = lstsq(X, rank_y, rcond=None)
        resid = rank_y - X @ coef
        ss_resid = float((resid ** 2).sum())
        param_r2[name] = 1.0 - ss_resid / ss_total

    # Full model R²
    X_full = empty((n_obs, n_params + 1))
    X_full[:, 0] = 1.0
    for j, name in enumerate(names):
        X_full[:, j + 1] = rankdata(arrays[name])
    coef_full, _, _, _ = lstsq(X_full, rank_y, rcond=None)
    resid_full = rank_y - X_full @ coef_full
    ss_resid_full = float((resid_full ** 2).sum())
    total_r2 = 1.0 - ss_resid_full / ss_total

    # Cumulative R² in order of individual importance
    sorted_params = sorted(param_r2.items(), key=lambda x: -x[1])
    top_k: list[tuple[str, float]] = []
    used_cols: list[int] = [0]  # intercept
    for name, _ in sorted_params:
        j = names.index(name)
        used_cols.append(j + 1)
        X_sub = X_full[:, used_cols]
        coef_sub, _, _, _ = lstsq(X_sub, rank_y, rcond=None)
        resid_sub = rank_y - X_sub @ coef_sub
        ss_sub = float((resid_sub ** 2).sum())
        cum_r2 = 1.0 - ss_sub / ss_total
        top_k.append((name, cum_r2))

    return SobolResult(
        param_r2=param_r2,
        top_k_cumulative_r2=top_k,
        total_r2=total_r2,
    )


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------
def run_mc(
    r_fixed: float,
    rng: Generator,
    n_runs: int = 10000,
    n_max_mc: int = 40000,
    *,
    baseline_override: dict[str, Any] | None = None,
    k_clip_upper: float = 200e9,
    k_years: int | None = 5,
) -> MCResult:
    """Run full Monte Carlo at a fixed discount rate.

    This is the thin orchestrator that composes sampling, loop, stats,
    correlations, and non-convergence analysis.

    Parameters
    ----------
    baseline_override : dict or None
        If provided, use as base parameter set instead of BASELINE (AA2).
    k_clip_upper : float
        Upper clip bound for K (AA2 K-clip sensitivity).
    """
    param_arrays = sample_mc_params(rng, n_runs, rho=0.3, rho_k_prod=0.5,
                                    correlated=True, k_clip_upper=k_clip_upper)
    crossovers, permanent_mask, n_clamped = run_mc_loop(param_arrays, r_fixed, n_max_mc,
                                                        baseline_override=baseline_override,
                                                        k_years=k_years)

    converged_mask = crossovers < n_max_mc
    n_converged = int(sum(converged_mask))

    # V3: Classify converging runs as permanent or transient
    conv_and_perm = converged_mask & permanent_mask
    conv_and_trans = converged_mask & ~permanent_mask
    n_permanent = int(sum(conv_and_perm))
    n_transient = int(sum(conv_and_trans))

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

    prcc = compute_prcc(param_arrays, crossovers)
    prcc_conditional = (
        compute_prcc(param_arrays, crossovers, mask=converged_mask)
        if n_converged > 100
        else []
    )

    sobol = compute_variance_decomposition(param_arrays, crossovers)
    sobol_conditional = (
        compute_variance_decomposition(param_arrays, crossovers, mask=converged_mask)
        if n_converged > 100
        else None
    )

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
        prcc=prcc,
        prcc_conditional=prcc_conditional,
        permanent_mask=permanent_mask,
        n_permanent=n_permanent,
        n_transient=n_transient,
        sobol=sobol,
        sobol_conditional=sobol_conditional,
        n_clamped=n_clamped,
    )


# ---------------------------------------------------------------------------
# N1c: Kaplan-Meier survival estimator for right-censored crossover data
# ---------------------------------------------------------------------------
def compute_kaplan_meier(
    crossovers: NDFloat,
    n_max_mc: int,
) -> tuple[float, NDFloat, NDFloat]:
    """Kaplan-Meier product-limit estimator for right-censored crossover data.

    Runs that did not converge within n_max_mc are treated as right-censored.
    Returns (km_median, km_times, km_survival).
    """
    event = crossovers < n_max_mc  # True = event observed (converged)
    order = argsort(crossovers)
    times = crossovers[order]
    events = event[order]
    n = len(times)

    # Unique event times (only where events actually occurred)
    unique_event_times = unique(times[events])

    survival = 1.0
    km_times = [0.0]
    km_survival = [1.0]
    at_risk = n

    for t in unique_event_times:
        # Count censored observations strictly before this event time
        # (they leave the risk set before this time)
        mask_t = times == t
        d = int(sum(mask_t & events))       # events at t
        c = int(sum(mask_t & ~events))       # censored at t

        # Remove subjects censored at earlier times from risk set
        # (handled by decrementing at_risk after each unique time)
        survival *= (at_risk - d) / at_risk
        km_times.append(float(t))
        km_survival.append(survival)
        at_risk -= (d + c)
        if at_risk <= 0:
            break

    # KM median = smallest t where S(t) <= 0.5
    km_median = float(inf)
    for t_val, s_val in zip(km_times, km_survival):
        if s_val <= 0.5:
            km_median = t_val
            break

    return km_median, array(km_times), array(km_survival)
