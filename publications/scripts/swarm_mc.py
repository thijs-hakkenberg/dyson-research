"""Monte Carlo engine for Dyson swarm coordination analysis.

Wraps :mod:`swarm_model` to run ensembles of discrete-event simulations,
aggregate statistics with confidence intervals, compare topologies, and
perform scaling / sensitivity analyses.

Ported from ``src/lib/services/simulation/swarm-coordination/monte-carlo.ts``.
"""

from __future__ import annotations

__version__ = "1.0.0"

import math
import time
from dataclasses import dataclass, field
from typing import Any, Callable, NamedTuple, Optional

import numpy as np
from numpy.random import Generator
from numpy.typing import NDArray
from scipy.stats import spearmanr, rankdata
from numpy.linalg import lstsq

from swarm_model import (
    CoordinationTopology,
    SwarmCoordinationConfig,
    SwarmCoordinationRunResult,
    SwarmCoordinationSimulator,
)

NDFloat = NDArray[np.floating[Any]]

# ---------------------------------------------------------------------------
# Default configuration
# ---------------------------------------------------------------------------
DEFAULT_SWARM_COORDINATION_CONFIG = SwarmCoordinationConfig(
    node_count=10_000,
    coordination_topology="hierarchical",
    cluster_size=100,
    coordinator_duty_cycle_hours=24,
    bandwidth_per_node_kbps=1.0,
    node_failure_rate_per_year=0.02,
    coordinator_power_w=18.0,
    base_power_w=5.0,
    simulation_days=90,
    seed=42,
)


# ---------------------------------------------------------------------------
# Statistics helpers
# ---------------------------------------------------------------------------
class Stats(NamedTuple):
    """Summary statistics for a Monte Carlo sample."""

    mean: float
    stddev: float
    median: float
    p5: float
    p95: float
    min: float
    max: float


def calculate_stats(values: NDFloat | list[float]) -> Stats:
    """Compute summary statistics for *values*."""
    a = np.asarray(values, dtype=float)
    if a.size == 0:
        return Stats(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    return Stats(
        mean=float(np.mean(a)),
        stddev=float(np.std(a, ddof=0)),
        median=float(np.median(a)),
        p5=float(np.percentile(a, 5)),
        p95=float(np.percentile(a, 95)),
        min=float(np.min(a)),
        max=float(np.max(a)),
    )


def confidence_interval(
    values: NDFloat | list[float],
    confidence: float = 0.95,
) -> tuple[float, float]:
    """Return the ``(lower, upper)`` confidence interval for the mean.

    Uses a z-score approximation (valid for n > 30).
    """
    a = np.asarray(values, dtype=float)
    if a.size == 0:
        return (0.0, 0.0)
    m = float(np.mean(a))
    s = float(np.std(a, ddof=0))
    n = a.size

    z_scores = {0.90: 1.645, 0.95: 1.96, 0.99: 2.576}
    z = z_scores.get(confidence, 1.96)
    margin = z * (s / math.sqrt(n))
    return (m - margin, m + margin)


# ---------------------------------------------------------------------------
# Result dataclasses
# ---------------------------------------------------------------------------
@dataclass
class SwarmCoordinationResult:
    """Aggregated results across Monte Carlo runs."""

    communication_overhead_percent: float = 0.0
    communication_overhead_std_dev: float = 0.0
    bottleneck_threshold_nodes: float = 0.0
    bottleneck_threshold_std_dev: float = 0.0
    coordinator_availability_percent: float = 0.0
    coordinator_availability_std_dev: float = 0.0
    power_variance_percent: float = 0.0
    power_variance_std_dev: float = 0.0
    avg_update_propagation_ms: float = 0.0
    max_update_propagation_ms: float = 0.0
    failed_handoffs: float = 0.0
    failed_handoffs_std_dev: float = 0.0
    message_drop_rate: float = 0.0
    message_drop_rate_std_dev: float = 0.0
    confidence_interval_95: tuple[float, float] = (0.0, 0.0)


@dataclass
class SwarmCoordinationOutput:
    """Full Monte Carlo output for one topology."""

    config: SwarmCoordinationConfig
    result: SwarmCoordinationResult
    runs: int
    execution_time_ms: float


@dataclass
class TopologyComparisonResult:
    """Comparison result across multiple topologies."""

    configs: list[SwarmCoordinationConfig]
    results: list[SwarmCoordinationResult]
    optimal_config_index: int
    analysis: dict[str, Any]


@dataclass
class ScalingAnalysisResult:
    """Result of a scaling analysis."""

    configs: list[SwarmCoordinationConfig]
    results: list[SwarmCoordinationResult]
    max_viable_nodes: int
    latency_at_max: float


@dataclass
class PRCCResult:
    """Partial Rank Correlation Coefficient for one parameter."""

    name: str
    prcc: float
    p_val: float


# ---------------------------------------------------------------------------
# Core MC runner
# ---------------------------------------------------------------------------
def run_swarm_coordination_mc(
    config: SwarmCoordinationConfig,
    runs: int = 100,
    on_progress: Optional[Callable[[int, int, float], None]] = None,
) -> SwarmCoordinationOutput:
    """Run *runs* Monte Carlo simulations and aggregate results.

    Parameters
    ----------
    config : SwarmCoordinationConfig
        Base configuration.  Each run uses ``seed = config.seed + i``.
    runs : int
        Number of simulation runs.
    on_progress : callable, optional
        ``on_progress(current_run, total_runs, percent_complete)``

    Returns
    -------
    SwarmCoordinationOutput
    """
    t_start = time.perf_counter()
    results: list[SwarmCoordinationRunResult] = []

    for i in range(runs):
        seed = config.seed + i
        run_cfg = SwarmCoordinationConfig(
            node_count=config.node_count,
            coordination_topology=config.coordination_topology,
            cluster_size=config.cluster_size,
            coordinator_duty_cycle_hours=config.coordinator_duty_cycle_hours,
            bandwidth_per_node_kbps=config.bandwidth_per_node_kbps,
            node_failure_rate_per_year=config.node_failure_rate_per_year,
            coordinator_power_w=config.coordinator_power_w,
            base_power_w=config.base_power_w,
            simulation_days=config.simulation_days,
            seed=seed,
        )
        sim = SwarmCoordinationSimulator(run_cfg)
        result = sim.run()
        result.run_id = i
        results.append(result)

        if on_progress is not None:
            on_progress(i + 1, runs, (i + 1) / runs * 100)

    elapsed_ms = (time.perf_counter() - t_start) * 1_000
    return SwarmCoordinationOutput(
        config=config,
        result=aggregate_results(results),
        runs=runs,
        execution_time_ms=elapsed_ms,
    )


# ---------------------------------------------------------------------------
# Aggregation
# ---------------------------------------------------------------------------
def aggregate_results(
    results: list[SwarmCoordinationRunResult],
) -> SwarmCoordinationResult:
    """Compute statistics across an ensemble of run results."""
    overheads = np.array([r.communication_overhead_percent for r in results])
    bottlenecks = np.array([r.bottleneck_threshold_nodes for r in results])
    availabilities = np.array([r.coordinator_availability_percent for r in results])
    power_vars = np.array([r.power_variance_percent for r in results])
    avg_props = np.array([r.avg_update_propagation_ms for r in results])
    max_props = np.array([r.max_update_propagation_ms for r in results])
    handoffs = np.array([r.failed_handoffs for r in results], dtype=float)
    drop_rates = np.array([r.message_drop_rate for r in results])

    overhead_stats = calculate_stats(overheads)
    bottleneck_stats = calculate_stats(bottlenecks)
    avail_stats = calculate_stats(availabilities)
    power_stats = calculate_stats(power_vars)
    handoff_stats = calculate_stats(handoffs)
    drop_stats = calculate_stats(drop_rates)

    ci = confidence_interval(overheads)

    return SwarmCoordinationResult(
        communication_overhead_percent=overhead_stats.mean,
        communication_overhead_std_dev=overhead_stats.stddev,
        bottleneck_threshold_nodes=bottleneck_stats.mean,
        bottleneck_threshold_std_dev=bottleneck_stats.stddev,
        coordinator_availability_percent=avail_stats.mean,
        coordinator_availability_std_dev=avail_stats.stddev,
        power_variance_percent=power_stats.mean,
        power_variance_std_dev=power_stats.stddev,
        avg_update_propagation_ms=float(np.mean(avg_props)),
        max_update_propagation_ms=float(np.max(max_props)),
        failed_handoffs=handoff_stats.mean,
        failed_handoffs_std_dev=handoff_stats.stddev,
        message_drop_rate=drop_stats.mean,
        message_drop_rate_std_dev=drop_stats.stddev,
        confidence_interval_95=ci,
    )


# ---------------------------------------------------------------------------
# Topology comparison
# ---------------------------------------------------------------------------
def find_optimal_config(
    results: list[SwarmCoordinationResult],
    topologies: list[CoordinationTopology],
) -> int:
    """Return the index of the optimal topology using a weighted score.

    Score = 0.3 * latency + 0.25 * bandwidth + 0.25 * availability + 0.2 * reliability
    """
    best_index = 0
    best_score = -math.inf

    for i, r in enumerate(results):
        latency_score = 1_000 / (r.avg_update_propagation_ms + 1)
        bandwidth_score = 100 / (r.communication_overhead_percent + 1)
        availability_score = r.coordinator_availability_percent / 100
        reliability_score = 1.0 - r.message_drop_rate

        score = (
            latency_score * 0.3
            + bandwidth_score * 0.25
            + availability_score * 0.25
            + reliability_score * 0.2
        )
        if score > best_score:
            best_score = score
            best_index = i

    return best_index


def _analyze_comparison(
    topologies: list[CoordinationTopology],
    results: list[SwarmCoordinationResult],
) -> dict[str, Any]:
    """Produce an analysis dict for the topology comparison."""
    best_lat = 0
    best_bw = 0
    best_pwr = 0
    for i in range(1, len(results)):
        if results[i].avg_update_propagation_ms < results[best_lat].avg_update_propagation_ms:
            best_lat = i
        if results[i].communication_overhead_percent < results[best_bw].communication_overhead_percent:
            best_bw = i
        if results[i].power_variance_percent < results[best_pwr].power_variance_percent:
            best_pwr = i

    optimal_idx = find_optimal_config(results, topologies)
    optimal_topo = topologies[optimal_idx]

    if optimal_topo == "hierarchical":
        rec = (
            "Hierarchical topology recommended for large-scale swarms. "
            "Provides good balance of latency, bandwidth efficiency, and fault tolerance. "
            "Cluster-based coordination scales well with proper coordinator duty cycling."
        )
    elif optimal_topo == "mesh":
        rec = (
            "Mesh topology recommended for this configuration. "
            "Gossip protocol provides robust propagation with no single point of failure. "
            "Higher latency but better fault tolerance for dynamic swarms."
        )
    else:
        rec = (
            "Centralized topology acceptable for smaller swarms. "
            "Simpler implementation but single point of failure risk. "
            "Consider hierarchical for swarms exceeding bottleneck threshold."
        )

    return {
        "bestLatency": topologies[best_lat],
        "bestBandwidth": topologies[best_bw],
        "bestPower": topologies[best_pwr],
        "recommendation": rec,
    }


def run_topology_comparison(
    base_config: SwarmCoordinationConfig,
    topologies: Optional[list[CoordinationTopology]] = None,
    runs_per: int = 50,
    on_progress: Optional[Callable[[int, int, float, str], None]] = None,
) -> TopologyComparisonResult:
    """Run MC for each topology and compare.

    Parameters
    ----------
    base_config : SwarmCoordinationConfig
        Topology field will be overridden per topology.
    topologies : list
        Topologies to compare (default: all three).
    runs_per : int
        Runs per topology.
    on_progress : callable, optional
        ``on_progress(current_run, total_runs, pct, current_topology)``
    """
    if topologies is None:
        topologies = ["centralized", "hierarchical", "mesh"]

    configs: list[SwarmCoordinationConfig] = []
    results: list[SwarmCoordinationResult] = []
    total_runs = len(topologies) * runs_per
    completed = 0

    for topo in topologies:
        cfg = SwarmCoordinationConfig(
            node_count=base_config.node_count,
            coordination_topology=topo,
            cluster_size=base_config.cluster_size,
            coordinator_duty_cycle_hours=base_config.coordinator_duty_cycle_hours,
            bandwidth_per_node_kbps=base_config.bandwidth_per_node_kbps,
            node_failure_rate_per_year=base_config.node_failure_rate_per_year,
            coordinator_power_w=base_config.coordinator_power_w,
            base_power_w=base_config.base_power_w,
            simulation_days=base_config.simulation_days,
            seed=base_config.seed,
        )
        configs.append(cfg)

        def _progress(cur: int, tot: int, pct: float, _topo: str = topo) -> None:
            if on_progress is not None:
                overall_pct = (completed + cur) / total_runs * 100
                on_progress(completed + cur, total_runs, overall_pct, _topo)

        output = run_swarm_coordination_mc(cfg, runs_per, _progress)
        results.append(output.result)
        completed += runs_per

    return TopologyComparisonResult(
        configs=configs,
        results=results,
        optimal_config_index=find_optimal_config(results, topologies),
        analysis=_analyze_comparison(topologies, results),
    )


# ---------------------------------------------------------------------------
# Scaling analysis
# ---------------------------------------------------------------------------
def generate_scaling_configs(
    base_config: SwarmCoordinationConfig,
    node_counts: Optional[list[int]] = None,
) -> list[SwarmCoordinationConfig]:
    """Generate configs with varying node counts and auto-scaled cluster sizes."""
    if node_counts is None:
        node_counts = [1_000, 5_000, 10_000, 50_000, 100_000, 500_000, 1_000_000]

    configs: list[SwarmCoordinationConfig] = []
    for nc in node_counts:
        cs = min(200, max(50, int(math.floor(math.sqrt(nc)))))
        configs.append(
            SwarmCoordinationConfig(
                node_count=nc,
                coordination_topology=base_config.coordination_topology,
                cluster_size=cs,
                coordinator_duty_cycle_hours=base_config.coordinator_duty_cycle_hours,
                bandwidth_per_node_kbps=base_config.bandwidth_per_node_kbps,
                node_failure_rate_per_year=base_config.node_failure_rate_per_year,
                coordinator_power_w=base_config.coordinator_power_w,
                base_power_w=base_config.base_power_w,
                simulation_days=base_config.simulation_days,
                seed=base_config.seed,
            )
        )
    return configs


def run_scaling_analysis(
    base_config: SwarmCoordinationConfig,
    target_latency_ms: float = 1_000.0,
    runs_per_size: int = 30,
    on_progress: Optional[Callable[[int, int, float], None]] = None,
) -> ScalingAnalysisResult:
    """Run MC at multiple node counts and find the maximum viable size.

    *Viable* means ``avg_update_propagation_ms <= target_latency_ms``.
    """
    node_counts = [1_000, 5_000, 10_000, 50_000, 100_000, 500_000, 1_000_000]
    configs = generate_scaling_configs(base_config, node_counts)
    results: list[SwarmCoordinationResult] = []

    completed = 0
    total_runs = len(configs) * runs_per_size

    for cfg in configs:
        def _progress(cur: int, tot: int, pct: float) -> None:
            if on_progress is not None:
                on_progress(completed + cur, total_runs, (completed + cur) / total_runs * 100)

        output = run_swarm_coordination_mc(cfg, runs_per_size, _progress)
        results.append(output.result)
        completed += runs_per_size

    # Find maximum viable
    max_viable_idx = 0
    for i, r in enumerate(results):
        if r.avg_update_propagation_ms <= target_latency_ms:
            max_viable_idx = i

    return ScalingAnalysisResult(
        configs=configs,
        results=results,
        max_viable_nodes=configs[max_viable_idx].node_count,
        latency_at_max=results[max_viable_idx].avg_update_propagation_ms,
    )


# ---------------------------------------------------------------------------
# PRCC sensitivity analysis
# ---------------------------------------------------------------------------
def compute_prcc_sensitivity(
    base_config: SwarmCoordinationConfig,
    runs: int = 200,
    rng: Optional[Generator] = None,
) -> list[PRCCResult]:
    """Run PRCC sensitivity analysis for key parameters vs. overhead.

    Varies ``node_count``, ``cluster_size``, and ``coordinator_duty_cycle_hours``
    across their plausible ranges, runs one simulation per sample, then
    computes Partial Rank Correlation Coefficients.

    Parameters
    ----------
    base_config : SwarmCoordinationConfig
        Baseline configuration.
    runs : int
        Number of Latin-hypercube-like samples.
    rng : Generator, optional
        Random number generator.

    Returns
    -------
    list[PRCCResult]
        PRCC for each sampled parameter against communication overhead,
        power variance, and propagation delay.
    """
    if rng is None:
        rng = np.random.default_rng(base_config.seed)

    # Sample parameter space
    node_counts = rng.integers(1_000, 50_001, size=runs).astype(float)
    cluster_sizes = rng.integers(50, 201, size=runs).astype(float)
    duty_cycles = rng.uniform(1.0, 168.0, size=runs)

    overheads = np.empty(runs, dtype=float)
    power_vars = np.empty(runs, dtype=float)

    print(f"PRCC sensitivity: running {runs} samples ...")

    for i in range(runs):
        cfg = SwarmCoordinationConfig(
            node_count=int(node_counts[i]),
            coordination_topology=base_config.coordination_topology,
            cluster_size=int(cluster_sizes[i]),
            coordinator_duty_cycle_hours=float(duty_cycles[i]),
            bandwidth_per_node_kbps=base_config.bandwidth_per_node_kbps,
            node_failure_rate_per_year=base_config.node_failure_rate_per_year,
            coordinator_power_w=base_config.coordinator_power_w,
            base_power_w=base_config.base_power_w,
            simulation_days=min(30, base_config.simulation_days),
            seed=base_config.seed + i,
        )
        sim = SwarmCoordinationSimulator(cfg)
        result = sim.run()
        overheads[i] = result.communication_overhead_percent
        power_vars[i] = result.power_variance_percent

        if (i + 1) % 50 == 0 or i == runs - 1:
            print(f"  [{i + 1}/{runs}]")

    # Build param arrays
    param_arrays: dict[str, NDFloat] = {
        "node_count": node_counts,
        "cluster_size": cluster_sizes,
        "duty_cycle": duty_cycles,
    }

    # PRCC against overhead
    prcc_overhead = _compute_prcc(param_arrays, overheads)
    # PRCC against power variance
    prcc_power = _compute_prcc(param_arrays, power_vars)

    results: list[PRCCResult] = []
    for pr in prcc_overhead:
        results.append(PRCCResult(
            name=f"{pr.name} vs overhead",
            prcc=pr.prcc,
            p_val=pr.p_val,
        ))
    for pr in prcc_power:
        results.append(PRCCResult(
            name=f"{pr.name} vs power_variance",
            prcc=pr.prcc,
            p_val=pr.p_val,
        ))
    return results


def _compute_prcc(
    param_arrays: dict[str, NDFloat],
    response: NDFloat,
) -> list[PRCCResult]:
    """Compute Partial Rank Correlation Coefficients.

    For each parameter X_i the algorithm:
      1. Ranks all variables.
      2. Regresses rank(X_i) on ranks of all other parameters -> residuals.
      3. Regresses rank(Y) on ranks of all other parameters -> residuals.
      4. PRCC = Spearman(residual_X_i, residual_Y).
    """
    names = list(param_arrays.keys())
    n_params = len(names)
    n_obs = len(response)

    if n_obs < n_params + 2:
        return []

    rank_matrix = np.empty((n_obs, n_params))
    for j, name in enumerate(names):
        rank_matrix[:, j] = rankdata(param_arrays[name])
    rank_y = rankdata(response)

    results: list[PRCCResult] = []
    for i, name in enumerate(names):
        x_others = rank_matrix[:, [j for j in range(n_params) if j != i]]
        x_design = np.empty((n_obs, x_others.shape[1] + 1))
        x_design[:, 0] = 1.0
        x_design[:, 1:] = x_others

        coef_xi, _, _, _ = lstsq(x_design, rank_matrix[:, i], rcond=None)
        resid_xi = rank_matrix[:, i] - x_design @ coef_xi

        coef_y, _, _, _ = lstsq(x_design, rank_y, rcond=None)
        resid_y = rank_y - x_design @ coef_y

        corr, p_val = spearmanr(resid_xi, resid_y)
        results.append(PRCCResult(name=name, prcc=float(corr), p_val=float(p_val)))

    return results


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------
def _print_result(
    label: str,
    result: SwarmCoordinationResult,
) -> None:
    """Pretty-print a single topology's aggregated results."""
    print(f"\n  --- {label} ---")
    print(f"  Overhead           : {result.communication_overhead_percent:>10.2f} %"
          f"  (sd {result.communication_overhead_std_dev:.2f})")
    print(f"  Bottleneck         : {result.bottleneck_threshold_nodes:>10,.0f} nodes"
          f"  (sd {result.bottleneck_threshold_std_dev:,.0f})")
    print(f"  Availability       : {result.coordinator_availability_percent:>10.2f} %"
          f"  (sd {result.coordinator_availability_std_dev:.2f})")
    print(f"  Power variance     : {result.power_variance_percent:>10.2f} %"
          f"  (sd {result.power_variance_std_dev:.2f})")
    print(f"  Avg propagation    : {result.avg_update_propagation_ms:>10.2f} ms")
    print(f"  Max propagation    : {result.max_update_propagation_ms:>10.2f} ms")
    print(f"  Failed handoffs    : {result.failed_handoffs:>10.2f}"
          f"  (sd {result.failed_handoffs_std_dev:.2f})")
    print(f"  Message drop rate  : {result.message_drop_rate:>10.6f}"
          f"  (sd {result.message_drop_rate_std_dev:.6f})")
    ci = result.confidence_interval_95
    print(f"  95% CI (overhead)  : [{ci[0]:.2f}, {ci[1]:.2f}]")


if __name__ == "__main__":
    import sys

    RUNS_PER = 100
    NODE_COUNT = 1_000  # Use smaller count for demo speed

    print("=" * 72)
    print("Swarm Coordination Monte Carlo -- topology comparison")
    print("=" * 72)
    print(f"Runs per topology: {RUNS_PER}")
    print(f"Node count       : {NODE_COUNT:,}")

    base = SwarmCoordinationConfig(
        node_count=NODE_COUNT,
        coordination_topology="hierarchical",
        cluster_size=100,
        coordinator_duty_cycle_hours=24,
        bandwidth_per_node_kbps=1.0,
        node_failure_rate_per_year=0.02,
        coordinator_power_w=18.0,
        base_power_w=5.0,
        simulation_days=30,
        seed=42,
    )

    topos: list[CoordinationTopology] = ["centralized", "hierarchical", "mesh"]

    def progress_cb(cur: int, total: int, pct: float, topo: str) -> None:
        if cur % 25 == 0 or cur == total:
            print(f"  [{topo:>14s}] {cur}/{total}  ({pct:.0f}%)")

    t0 = time.perf_counter()
    comparison = run_topology_comparison(base, topos, runs_per=RUNS_PER, on_progress=progress_cb)
    elapsed = time.perf_counter() - t0

    print(f"\nCompleted in {elapsed:.1f} s")

    for i, topo in enumerate(topos):
        _print_result(topo.upper(), comparison.results[i])

    analysis = comparison.analysis
    print(f"\nAnalysis:")
    print(f"  Best latency     : {analysis['bestLatency']}")
    print(f"  Best bandwidth   : {analysis['bestBandwidth']}")
    print(f"  Best power       : {analysis['bestPower']}")
    print(f"  Optimal topology : {topos[comparison.optimal_config_index]}")
    print(f"  Recommendation   : {analysis['recommendation']}")

    # ----- PRCC sensitivity -----
    print("\n" + "=" * 72)
    print("PRCC Sensitivity Analysis")
    print("=" * 72)
    prcc_results = compute_prcc_sensitivity(base, runs=100)
    for pr in prcc_results:
        sig = "***" if pr.p_val < 0.001 else ("**" if pr.p_val < 0.01 else ("*" if pr.p_val < 0.05 else ""))
        print(f"  {pr.name:<35s}  PRCC={pr.prcc:+.4f}  p={pr.p_val:.4f}  {sig}")

    print("\nDone.")
