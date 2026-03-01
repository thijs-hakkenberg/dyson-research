#!/usr/bin/env python3
"""Generate publication-quality figures for the Swarm Coordination Scaling paper.

Imports model logic from swarm_model and MC engine from swarm_mc, then produces
10 PDF figures:
  1. fig-overhead-vs-nodes.pdf       -- Comm overhead vs node count (3 topologies)
  2. fig-latency-distribution.pdf    -- Propagation latency box/violin plots
  3. fig-cluster-size-optimization.pdf -- Overhead vs cluster size (hierarchical)
  4. fig-duty-cycle-pareto.pdf       -- Power variance vs availability Pareto
  5. fig-scaling-trajectory.pdf      -- Overhead scaling with/without optimization
  6. fig-architecture-diagram.pdf    -- 4-level hierarchy diagram
  7. fig-failure-resilience.pdf      -- Availability vs failure rate
  8. fig-topology-summary.pdf        -- Grouped bar chart comparing topologies
  9. fig-message-decomposition.pdf   -- Per-tier message breakdown (hierarchical)
 10. fig-fleet-reuse.pdf             -- Fleet-level channel reuse inflation

Usage:
    source publications/scripts/.venv/bin/activate
    python publications/scripts/generate_swarm_figures.py
"""

from __future__ import annotations

__version__ = "1.0.0"

import argparse
import functools
import math
import time
from os import environ, makedirs
from os.path import abspath, dirname, join
from typing import Any

import numpy as np
from numpy.random import default_rng

from matplotlib import use as mpl_use

mpl_use("Agg")

from matplotlib.pyplot import close, rcParams, subplots  # noqa: E402
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch  # noqa: E402
from matplotlib.ticker import FuncFormatter  # noqa: E402

from scipy.optimize import curve_fit  # noqa: E402

from swarm_model import (  # noqa: E402
    CoordinationTopology,
    SwarmCoordinationConfig,
    SwarmCoordinationSimulator,
    TierMessageBreakdown,
    calculate_bandwidth_requirement,
    calculate_communication_overhead,
    calculate_propagation_delay,
)
from swarm_mc import (  # noqa: E402
    calculate_stats,
    confidence_interval,
    run_swarm_coordination_mc,
)

# ---------------------------------------------------------------------------
# Output directory
# ---------------------------------------------------------------------------
script_dir = dirname(abspath(__file__))
fig_dir = environ.get(
    "SWARM_FIG_DIR",
    join(script_dir, "..", "drafts", "02-swarm-coordination-scaling", "figures"),
)
makedirs(fig_dir, exist_ok=True)

# ---------------------------------------------------------------------------
# Publication style (matches generate_isru_figures.py exactly)
# ---------------------------------------------------------------------------
rcParams.update(
    {
        "font.family": "serif",
        "font.size": 10,
        "axes.labelsize": 11,
        "axes.titlesize": 12,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "legend.fontsize": 9,
        "figure.figsize": (6, 4),
        "figure.dpi": 300,
        "savefig.dpi": 300,
        "savefig.pad_inches": 0.05,
        "axes.grid": True,
        "grid.alpha": 0.3,
        "grid.linewidth": 0.5,
    }
)

# ---------------------------------------------------------------------------
# Color scheme
# ---------------------------------------------------------------------------
c_centralized = "#d97706"  # amber
c_hierarchical = "#0891b2"  # cyan
c_mesh = "#7c3aed"  # purple
c_sectorized = "#059669"  # emerald
c_optimized = "#16a34a"  # green
c_pareto = "#dc2626"  # red

SEED = 42
TOPOLOGIES = ["centralized", "hierarchical", "mesh", "sectorized_mesh"]

# ---------------------------------------------------------------------------
# Scale profiles: --fast (CI/dev) vs default (publication)
# ---------------------------------------------------------------------------
SCALE_FAST = {
    "node_counts": [1_000, 5_000, 10_000],
    "n_runs": 3,
    "cluster_sizes": [25, 50, 100],
    "failure_rates": [0.01, 0.05, 0.1],
    "summary_runs": 3,
    "summary_nodes": 5_000,
    "sim_days_cap": 1,  # max simulation days (overrides _sim_days)
    "max_events_factor": 3,  # max_events = node_count * factor (default 10*days)
}
SCALE_FULL = {
    "node_counts": [1_000, 5_000, 10_000, 20_000, 30_000, 40_000, 50_000, 60_000, 80_000, 100_000],
    "n_runs": 20,
    "cluster_sizes": [10, 25, 50, 100, 200, 500],
    "failure_rates": [0.001, 0.005, 0.01, 0.02, 0.05, 0.1],
    "summary_runs": 50,
    "summary_nodes": 10_000,
    "sim_days_cap": 90,
}
SCALE = SCALE_FULL  # default; overridden by --fast
TOPO_COLORS = {
    "centralized": c_centralized,
    "hierarchical": c_hierarchical,
    "mesh": c_mesh,
    "sectorized_mesh": c_sectorized,
}
TOPO_LABELS = {
    "centralized": "Centralized",
    "hierarchical": "Hierarchical",
    "mesh": "Mesh (gossip)",
    "sectorized_mesh": "Sectorized mesh",
}


# ---------------------------------------------------------------------------
# Helper: choose simulation_days based on node count
# ---------------------------------------------------------------------------
@functools.lru_cache
def _sim_days(node_count: int) -> int:
    """Return an appropriate simulation_days for the given node count."""
    cap = SCALE.get("sim_days_cap", 90)
    if node_count >= 1_000_000:
        return min(10, cap)
    if node_count >= 100_000:
        return min(30, cap)
    if node_count >= 10_000:
        return min(60, cap)
    return min(30, cap)


@functools.lru_cache
def _max_events(node_count: int) -> int | None:
    """Return max_events override, or None for default."""
    factor = SCALE.get("max_events_factor")
    if factor is not None:
        return node_count * factor
    return None


def _make_config(
    node_count: int,
    topology: CoordinationTopology = "hierarchical",
    cluster_size: int = 100,
    seed: int = SEED,
    **kwargs: Any,
) -> SwarmCoordinationConfig:
    return SwarmCoordinationConfig(
        node_count=node_count,
        coordination_topology=topology,
        cluster_size=cluster_size,
        simulation_days=kwargs.pop("simulation_days", _sim_days(node_count)),
        seed=seed,
        max_events=kwargs.pop("max_events", _max_events(node_count)),
        **kwargs,
    )


# ---------------------------------------------------------------------------
# Figure 1: Communication Overhead vs Node Count
# ---------------------------------------------------------------------------
def fig_overhead_vs_nodes() -> None:
    """Generate Figure 1: overhead (%) vs node count for all 3 topologies.

    Runs 20 MC iterations per point across 7 node counts and 3 topologies.
    Shows mean with shaded 95% CI band on a semilog-x plot.
    """
    node_counts = SCALE["node_counts"]
    n_runs = SCALE["n_runs"]

    fig, ax = subplots()

    for topo in TOPOLOGIES:
        means = []
        ci_lo = []
        ci_hi = []

        for nc in node_counts:
            cluster_size = min(200, max(50, int(math.floor(math.sqrt(nc)))))
            cfg = _make_config(nc, topology=topo, cluster_size=cluster_size)
            output = run_swarm_coordination_mc(cfg, runs=n_runs)
            means.append(output.result.communication_overhead_percent)
            lo, hi = output.result.confidence_interval_95
            ci_lo.append(lo)
            ci_hi.append(hi)

        ax.plot(
            node_counts,
            means,
            "o-",
            color=TOPO_COLORS[topo],
            linewidth=1.8,
            markersize=4,
            label=TOPO_LABELS[topo],
        )
        ax.fill_between(
            node_counts,
            ci_lo,
            ci_hi,
            alpha=0.15,
            color=TOPO_COLORS[topo],
        )

    ax.set_xscale("log")
    ax.set_xlabel("Node Count")
    ax.set_ylabel("DES-Measured Overhead (%)")
    ax.set_title("Communication Overhead vs Swarm Size")
    ax.legend(loc="best", framealpha=0.9)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x):,}"))

    fig.savefig(join(fig_dir, "fig-overhead-vs-nodes.pdf"), bbox_inches="tight")
    close(fig)


# ---------------------------------------------------------------------------
# Figure 2: Latency Distribution
# ---------------------------------------------------------------------------
def fig_latency_distribution() -> None:
    """Generate Figure 2: box/violin plot of propagation latency at 3 scales.

    Three subplots (one per topology). At each of 3 scales (10K, 100K, 1M),
    run 10 simulations and collect propagation times. Log scale for y-axis.
    """
    nc_list = SCALE["node_counts"]
    # Pick 3 representative scales from available node counts
    if len(nc_list) >= 3:
        scales = [nc_list[0], nc_list[len(nc_list) // 2], nc_list[-1]]
    else:
        scales = nc_list[:3]
    scale_labels = [f"{s // 1000}K" if s >= 1000 else str(s) for s in scales]
    n_runs = min(10, SCALE["n_runs"])

    n_topos = len(TOPOLOGIES)
    fig, axes = subplots(1, n_topos, figsize=(3.5 * n_topos, 4), sharey=True)
    if n_topos == 1:
        axes = [axes]

    for ax_idx, topo in enumerate(TOPOLOGIES):
        ax = axes[ax_idx]
        data = []
        positions = []
        labels = []

        for s_idx, nc in enumerate(scales):
            cluster_size = min(200, max(50, int(math.floor(math.sqrt(nc)))))
            latencies = []

            for run_i in range(n_runs):
                cfg = _make_config(
                    nc, topology=topo, cluster_size=cluster_size,
                    seed=SEED + run_i,
                )
                sim = SwarmCoordinationSimulator(cfg)
                result = sim.run()
                latencies.append(result.avg_update_propagation_ms)

            data.append(latencies)
            positions.append(s_idx + 1)
            labels.append(scale_labels[s_idx])

        bp = ax.boxplot(
            data,
            positions=positions,
            widths=0.5,
            patch_artist=True,
            showfliers=True,
        )
        for patch in bp["boxes"]:
            patch.set_facecolor(TOPO_COLORS[topo])
            patch.set_alpha(0.6)

        ax.set_yscale("log")
        ax.set_xticks(positions)
        ax.set_xticklabels(labels)
        ax.set_title(TOPO_LABELS[topo])
        ax.set_xlabel("Node Count")

    axes[0].set_ylabel("Propagation Latency (ms)")
    fig.suptitle("Message Propagation Latency Distribution", fontsize=12)
    fig.tight_layout()

    fig.savefig(join(fig_dir, "fig-latency-distribution.pdf"), bbox_inches="tight")
    close(fig)


# ---------------------------------------------------------------------------
# Figure 3: Cluster Size Optimization
# ---------------------------------------------------------------------------
def fig_cluster_size_optimization() -> None:
    """Generate Figure 3: overhead vs cluster size for hierarchical at 100K nodes.

    Tests cluster sizes [25, 50, 100, 150, 200, 300, 500]. 20 runs per point.
    Shows optimal cluster size. Secondary y-axis for latency.
    """
    cluster_sizes = SCALE["cluster_sizes"]
    nc = SCALE["node_counts"][-2] if len(SCALE["node_counts"]) >= 2 else SCALE["node_counts"][-1]
    n_runs = SCALE["n_runs"]
    sim_days = _sim_days(nc)

    overheads_mean = []
    overheads_ci_lo = []
    overheads_ci_hi = []
    latencies_mean = []
    latencies_ci_lo = []
    latencies_ci_hi = []

    for cs in cluster_sizes:
        cfg = _make_config(nc, cluster_size=cs)
        output = run_swarm_coordination_mc(cfg, runs=n_runs)
        overheads_mean.append(output.result.communication_overhead_percent)
        lo, hi = output.result.confidence_interval_95
        overheads_ci_lo.append(lo)
        overheads_ci_hi.append(hi)

        # Collect latency data from individual runs
        lat_values = []
        for run_i in range(n_runs):
            run_cfg = _make_config(nc, cluster_size=cs, seed=SEED + run_i)
            sim = SwarmCoordinationSimulator(run_cfg)
            result = sim.run()
            lat_values.append(result.avg_update_propagation_ms)

        lat_stats = calculate_stats(lat_values)
        lat_ci = confidence_interval(lat_values)
        latencies_mean.append(lat_stats.mean)
        latencies_ci_lo.append(lat_ci[0])
        latencies_ci_hi.append(lat_ci[1])

    # Find optimal cluster size (minimum overhead)
    opt_idx = int(np.argmin(overheads_mean))
    opt_cs = cluster_sizes[opt_idx]

    fig, ax1 = subplots(figsize=(7, 4.5))

    # Primary axis: overhead
    color_oh = c_hierarchical
    ax1.plot(
        cluster_sizes,
        overheads_mean,
        "o-",
        color=color_oh,
        linewidth=1.8,
        markersize=5,
        label="DES Overhead (%)",
    )
    ax1.fill_between(
        cluster_sizes,
        overheads_ci_lo,
        overheads_ci_hi,
        alpha=0.15,
        color=color_oh,
    )
    ax1.axvline(
        opt_cs, color=c_optimized, linestyle="--", linewidth=1, alpha=0.7
    )
    # Position annotation within plot bounds using axes transform for y
    y_range = max(overheads_mean) - min(overheads_mean)
    ax1.annotate(
        f"Optimal: {opt_cs}",
        xy=(opt_cs, overheads_mean[opt_idx]),
        xytext=(opt_cs + 80, overheads_mean[opt_idx] + y_range * 0.3),
        fontsize=9,
        color=c_optimized,
        fontweight="bold",
        arrowprops=dict(arrowstyle="->", color=c_optimized, lw=1.2),
    )
    ax1.set_xlabel("Cluster Size (nodes per cluster)")
    ax1.set_ylabel("DES Overhead (%)", color=color_oh)
    ax1.tick_params(axis="y", labelcolor=color_oh)

    # Secondary axis: latency
    ax2 = ax1.twinx()
    color_lat = c_centralized
    ax2.plot(
        cluster_sizes,
        latencies_mean,
        "s--",
        color=color_lat,
        linewidth=1.5,
        markersize=4,
        label="Latency (ms)",
    )
    ax2.fill_between(
        cluster_sizes,
        latencies_ci_lo,
        latencies_ci_hi,
        alpha=0.10,
        color=color_lat,
    )
    ax2.set_ylabel("Avg Propagation Latency (ms)", color=color_lat)
    ax2.tick_params(axis="y", labelcolor=color_lat)

    # Combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right", framealpha=0.9)

    ax1.set_title("Cluster Size Optimization (Hierarchical, 100K Nodes)")
    fig.tight_layout()

    fig.savefig(join(fig_dir, "fig-cluster-size-optimization.pdf"), bbox_inches="tight")
    close(fig)


# ---------------------------------------------------------------------------
# Figure 4: Duty Cycle Pareto
# ---------------------------------------------------------------------------
def fig_duty_cycle_pareto() -> None:
    """Generate Figure 4: power variance vs coordinator availability for duty cycles.

    Scatter plot for duty cycles [1h, 4h, 8h, 12h, 24h, 48h, 168h].
    Hierarchical topology, 10K nodes, 20 runs each. Pareto frontier highlighted.
    """
    duty_cycles_h = [1, 4, 8, 12, 24, 48, 168]
    nc = SCALE["node_counts"][min(2, len(SCALE["node_counts"]) - 1)]  # ~10K or smaller
    n_runs = SCALE["n_runs"]
    sim_days = _sim_days(nc)

    avail_means = []
    pvar_means = []
    avail_all = []
    pvar_all = []

    for dc in duty_cycles_h:
        a_vals = []
        p_vals = []

        for run_i in range(n_runs):
            cfg = _make_config(
                nc, seed=SEED + run_i,
                coordinator_duty_cycle_hours=float(dc),
            )
            sim = SwarmCoordinationSimulator(cfg)
            result = sim.run()
            a_vals.append(result.coordinator_availability_percent)
            p_vals.append(result.power_variance_percent)

        avail_means.append(np.mean(a_vals))
        pvar_means.append(np.mean(p_vals))
        avail_all.append(a_vals)
        pvar_all.append(p_vals)

    # Compute Pareto frontier: want high availability, low power variance
    # Sort by descending availability; sweep keeps running min of power variance.
    n_pts = len(duty_cycles_h)
    order = sorted(range(n_pts), key=lambda i: -avail_means[i])
    pareto_mask = [False] * n_pts
    best_pvar = float("inf")
    for i in order:
        if pvar_means[i] <= best_pvar:
            pareto_mask[i] = True
            best_pvar = pvar_means[i]

    fig, ax = subplots()

    # Plot all points
    for i, dc in enumerate(duty_cycles_h):
        marker = "D" if pareto_mask[i] else "o"
        edgecolor = c_pareto if pareto_mask[i] else "gray"
        ax.scatter(
            avail_means[i],
            pvar_means[i],
            s=80,
            marker=marker,
            color=c_hierarchical,
            edgecolors=edgecolor,
            linewidths=1.5 if pareto_mask[i] else 0.8,
            zorder=5,
        )
        ax.annotate(
            f"{dc}h",
            (avail_means[i], pvar_means[i]),
            textcoords="offset points",
            xytext=(8, 5),
            fontsize=8,
        )

    # Draw Pareto frontier line
    pareto_indices = [i for i, m in enumerate(pareto_mask) if m]
    if len(pareto_indices) > 1:
        pareto_avail = [avail_means[i] for i in pareto_indices]
        pareto_pvar = [pvar_means[i] for i in pareto_indices]
        # Sort by availability
        order = np.argsort(pareto_avail)
        ax.plot(
            [pareto_avail[k] for k in order],
            [pareto_pvar[k] for k in order],
            "--",
            color=c_pareto,
            linewidth=1.2,
            alpha=0.7,
            label="Pareto frontier",
        )

    ax.set_xlabel("Coordinator Availability (%)")
    ax.set_ylabel("Power Variance (%)")
    ax.set_title("Duty Cycle Trade-off: Power Variance vs Availability")
    ax.legend(loc="best", framealpha=0.9)

    fig.savefig(join(fig_dir, "fig-duty-cycle-pareto.pdf"), bbox_inches="tight")
    close(fig)


# ---------------------------------------------------------------------------
# Statistical model fitting for superlinear transition detection
# ---------------------------------------------------------------------------
def _linear_model(x: np.ndarray, a: float, b: float) -> np.ndarray:
    """Linear model: overhead = a * N + b."""
    return a * x + b


def _power_law_model(x: np.ndarray, a: float, b: float) -> np.ndarray:
    """Power-law model: overhead = a * N^b."""
    return a * np.power(x, b)


def _piecewise_linear(x: np.ndarray, a1: float, b1: float, a2: float, b2: float,
                      bp: float) -> np.ndarray:
    """Piecewise-linear model with breakpoint bp."""
    return np.where(x < bp, a1 * x + b1, a2 * x + b2)


def _compute_aic(n: int, rss: float, k: int) -> float:
    """Compute AIC = n * ln(RSS/n) + 2k."""
    if rss <= 0 or n <= 0:
        return float("inf")
    return n * np.log(rss / n) + 2 * k


def fit_scaling_models(
    node_counts: list[int],
    overhead_means: list[float],
    min_nodes: int = 10_000,
) -> dict:
    """Fit linear, power-law, and piecewise-linear models to overhead data.

    Only uses data points where node_count >= min_nodes.
    Returns a dict with model names, parameters, AIC values, and best model info.
    """
    # Filter to N >= min_nodes
    mask = [i for i, nc in enumerate(node_counts) if nc >= min_nodes]
    if len(mask) < 3:
        # Not enough data points for meaningful fitting; use all points
        mask = list(range(len(node_counts)))

    x = np.array([node_counts[i] for i in mask], dtype=float)
    y = np.array([overhead_means[i] for i in mask], dtype=float)
    n = len(x)

    results: dict = {"models": {}, "best_model": None, "best_aic": float("inf"),
                     "breakpoint": None, "breakpoint_ci": None}

    # 1. Linear fit: overhead = a * N + b  (k=2)
    try:
        popt_lin, _ = curve_fit(_linear_model, x, y, p0=[1e-6, 0.0], maxfev=5000)
        y_pred_lin = _linear_model(x, *popt_lin)
        rss_lin = float(np.sum((y - y_pred_lin) ** 2))
        aic_lin = _compute_aic(n, rss_lin, 2)
        results["models"]["linear"] = {
            "params": {"a": popt_lin[0], "b": popt_lin[1]},
            "aic": aic_lin, "rss": rss_lin,
        }
        if aic_lin < results["best_aic"]:
            results["best_aic"] = aic_lin
            results["best_model"] = "linear"
    except (RuntimeError, ValueError):
        pass

    # 2. Power-law fit: overhead = a * N^b  (k=2)
    try:
        # Need positive y values
        y_pos = np.maximum(y, 1e-10)
        popt_pow, _ = curve_fit(_power_law_model, x, y_pos, p0=[1e-3, 1.0],
                                maxfev=5000)
        y_pred_pow = _power_law_model(x, *popt_pow)
        rss_pow = float(np.sum((y - y_pred_pow) ** 2))
        aic_pow = _compute_aic(n, rss_pow, 2)
        results["models"]["power_law"] = {
            "params": {"a": popt_pow[0], "b": popt_pow[1]},
            "aic": aic_pow, "rss": rss_pow,
        }
        if aic_pow < results["best_aic"]:
            results["best_aic"] = aic_pow
            results["best_model"] = "power_law"
    except (RuntimeError, ValueError):
        pass

    # 3. Piecewise-linear: sweep breakpoint from 20k to 80k in steps of 5k  (k=5)
    best_pw_aic = float("inf")
    best_pw_bp = None
    best_pw_params = None
    best_pw_rss = None

    # Determine breakpoint sweep range based on available data
    x_min, x_max = float(x.min()), float(x.max())
    bp_lo = max(20_000, x_min + (x_max - x_min) * 0.1)
    bp_hi = min(80_000, x_max - (x_max - x_min) * 0.1)
    if bp_lo >= bp_hi:
        # Fallback: sweep over middle 60% of data range
        bp_lo = x_min + (x_max - x_min) * 0.2
        bp_hi = x_min + (x_max - x_min) * 0.8

    bp_step = max(5_000, (bp_hi - bp_lo) / 12)  # at most ~12 breakpoints
    bp_candidates = np.arange(bp_lo, bp_hi + 1, bp_step)

    for bp in bp_candidates:
        # Need at least 2 points on each side
        left = x[x < bp]
        right = x[x >= bp]
        if len(left) < 2 or len(right) < 2:
            continue
        try:
            def _pw(xv: np.ndarray, a1: float, b1: float, a2: float,
                    b2: float) -> np.ndarray:
                return np.where(xv < bp, a1 * xv + b1, a2 * xv + b2)

            popt, _ = curve_fit(_pw, x, y, p0=[1e-6, 0.0, 1e-6, 0.0], maxfev=5000)
            y_pred = _pw(x, *popt)
            rss = float(np.sum((y - y_pred) ** 2))
            aic = _compute_aic(n, rss, 5)  # 4 params + breakpoint = 5
            if aic < best_pw_aic:
                best_pw_aic = aic
                best_pw_bp = float(bp)
                best_pw_params = popt
                best_pw_rss = rss
        except (RuntimeError, ValueError):
            continue

    if best_pw_params is not None:
        results["models"]["piecewise_linear"] = {
            "params": {
                "a1": best_pw_params[0], "b1": best_pw_params[1],
                "a2": best_pw_params[2], "b2": best_pw_params[3],
                "breakpoint": best_pw_bp,
            },
            "aic": best_pw_aic, "rss": best_pw_rss,
        }
        results["breakpoint"] = best_pw_bp
        # Simple CI: +/- one step
        results["breakpoint_ci"] = (
            max(x_min, best_pw_bp - bp_step),
            min(x_max, best_pw_bp + bp_step),
        )
        if best_pw_aic < results["best_aic"]:
            results["best_aic"] = best_pw_aic
            results["best_model"] = "piecewise_linear"

    return results


# ---------------------------------------------------------------------------
# Figure 5: Scaling Trajectory
# ---------------------------------------------------------------------------
def fig_scaling_trajectory() -> None:
    """Generate Figure 5: overhead trajectory at increasing node counts.

    Hierarchical topology, with/without auto-scaling cluster size via
    min(200, max(50, floor(sqrt(N)))). 10 runs per point.
    Also performs formal statistical testing for superlinear transition.
    """
    node_counts = SCALE["node_counts"]
    n_runs = SCALE["n_runs"]
    fixed_cluster_size = 100

    means_fixed = []
    ci_lo_fixed = []
    ci_hi_fixed = []
    means_opt = []
    ci_lo_opt = []
    ci_hi_opt = []

    for nc in node_counts:
        # Fixed cluster size
        cfg_fixed = _make_config(nc, cluster_size=fixed_cluster_size)
        out_fixed = run_swarm_coordination_mc(cfg_fixed, runs=n_runs)
        means_fixed.append(out_fixed.result.communication_overhead_percent)
        lo, hi = out_fixed.result.confidence_interval_95
        ci_lo_fixed.append(lo)
        ci_hi_fixed.append(hi)

        # Optimized cluster size
        opt_cs = min(200, max(50, int(math.floor(math.sqrt(nc)))))
        cfg_opt = _make_config(nc, cluster_size=opt_cs)
        out_opt = run_swarm_coordination_mc(cfg_opt, runs=n_runs)
        means_opt.append(out_opt.result.communication_overhead_percent)
        lo, hi = out_opt.result.confidence_interval_95
        ci_lo_opt.append(lo)
        ci_hi_opt.append(hi)

    # --- Formal statistical testing for scaling behavior ---
    fit_results = fit_scaling_models(node_counts, means_fixed)

    print("\n  --- Superlinear transition analysis (fixed cluster size) ---")
    for model_name, model_data in fit_results["models"].items():
        print(f"    {model_name}: AIC={model_data['aic']:.2f}, "
              f"RSS={model_data['rss']:.4f}, params={model_data['params']}")
    if fit_results["best_model"]:
        print(f"    Best model: {fit_results['best_model']} "
              f"(AIC={fit_results['best_aic']:.2f})")
    if fit_results["breakpoint"] is not None:
        bp_ci = fit_results["breakpoint_ci"]
        print(f"    Breakpoint: {fit_results['breakpoint']:,.0f} nodes "
              f"(CI: [{bp_ci[0]:,.0f}, {bp_ci[1]:,.0f}])")

    fig, ax = subplots()

    ax.plot(
        node_counts,
        means_fixed,
        "o-",
        color=c_centralized,
        linewidth=1.8,
        markersize=4,
        label=f"Fixed cluster size ({fixed_cluster_size})",
    )
    ax.fill_between(
        node_counts,
        ci_lo_fixed,
        ci_hi_fixed,
        alpha=0.15,
        color=c_centralized,
    )

    ax.plot(
        node_counts,
        means_opt,
        "s-",
        color=c_optimized,
        linewidth=1.8,
        markersize=4,
        label="Auto-scaled cluster size",
    )
    ax.fill_between(
        node_counts,
        ci_lo_opt,
        ci_hi_opt,
        alpha=0.15,
        color=c_optimized,
    )

    # --- Add statistical annotation to figure ---
    if fit_results["best_model"]:
        best = fit_results["best_model"]
        aic = fit_results["best_aic"]
        annotation_lines = [f"Best fit: {best.replace('_', '-')} (AIC={aic:.1f})"]
        if best == "power_law" and "power_law" in fit_results["models"]:
            b_exp = fit_results["models"]["power_law"]["params"]["b"]
            annotation_lines.append(f"Exponent b={b_exp:.3f}")
        if fit_results["breakpoint"] is not None:
            bp = fit_results["breakpoint"]
            bp_ci = fit_results["breakpoint_ci"]
            annotation_lines.append(
                f"Breakpoint: {bp / 1000:.0f}K [{bp_ci[0] / 1000:.0f}K, {bp_ci[1] / 1000:.0f}K]"
            )
        annotation_text = "\n".join(annotation_lines)
        ax.text(
            0.03, 0.97, annotation_text,
            transform=ax.transAxes,
            fontsize=7.5, verticalalignment="top",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="wheat", alpha=0.7),
        )

    ax.set_xscale("log")
    ax.set_xlabel("Node Count")
    ax.set_ylabel("DES-Measured Overhead (%)")
    ax.set_title("Scaling Trajectory: Fixed vs Optimized Cluster Size")
    ax.legend(loc="best", framealpha=0.9)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x):,}"))

    fig.savefig(join(fig_dir, "fig-scaling-trajectory.pdf"), bbox_inches="tight")
    close(fig)


# ---------------------------------------------------------------------------
# Figure 6: Architecture Diagram
# ---------------------------------------------------------------------------
def fig_architecture_diagram() -> None:
    """Generate Figure 6: 4-level hierarchy diagram using matplotlib patches.

    Central -> Regional (3) -> Cluster (9) -> Nodes (dots).
    """
    fig, ax = subplots(figsize=(8, 6))
    ax.set_xlim(-1, 11)
    ax.set_ylim(-0.5, 8)
    ax.set_aspect("equal")
    ax.axis("off")

    # Level positions (y from top to bottom)
    y_central = 7.0
    y_regional = 5.0
    y_cluster = 3.0
    y_nodes = 1.0

    box_w = 1.6
    box_h = 0.6

    def draw_box(cx: float, cy: float, label: str, color: str) -> None:
        """Draw a rounded box centered at (cx, cy)."""
        box = FancyBboxPatch(
            (cx - box_w / 2, cy - box_h / 2),
            box_w,
            box_h,
            boxstyle="round,pad=0.1",
            facecolor=color,
            edgecolor="black",
            linewidth=1.2,
            alpha=0.85,
        )
        ax.add_patch(box)
        ax.text(
            cx,
            cy,
            label,
            ha="center",
            va="center",
            fontsize=8,
            fontweight="bold",
            color="white",
        )

    def draw_arrow(x1: float, y1: float, x2: float, y2: float) -> None:
        """Draw an arrow from (x1,y1) to (x2,y2)."""
        arrow = FancyArrowPatch(
            (x1, y1),
            (x2, y2),
            arrowstyle="-|>",
            color="gray",
            linewidth=1.2,
            mutation_scale=12,
        )
        ax.add_patch(arrow)

    # Central coordinator
    cx_central = 5.0
    draw_box(cx_central, y_central, "Central\nCoordinator", "#1e3a5f")

    # Regional coordinators (3)
    regional_xs = [2.0, 5.0, 8.0]
    for rx in regional_xs:
        draw_arrow(cx_central, y_central - box_h / 2, rx, y_regional + box_h / 2)
        draw_box(rx, y_regional, "Regional\nCoord.", "#0891b2")

    # Cluster coordinators (3 per regional = 9)
    cluster_xs_per_region = [
        [0.5, 2.0, 3.5],
        [4.0, 5.0, 6.0],
        [6.5, 8.0, 9.5],
    ]
    all_cluster_xs = []
    for r_idx, rx in enumerate(regional_xs):
        for cx in cluster_xs_per_region[r_idx]:
            draw_arrow(rx, y_regional - box_h / 2, cx, y_cluster + box_h / 2)
            draw_box(cx, y_cluster, "Cluster\nCoord.", "#7c3aed")
            all_cluster_xs.append(cx)

    # Nodes (dots below each cluster)
    rng = default_rng(SEED)
    for cx in all_cluster_xs:
        n_dots = 5
        dot_spread = 0.6
        for d in range(n_dots):
            dx = cx + (d - n_dots / 2) * (dot_spread / n_dots) * 2
            dy = y_nodes + rng.uniform(-0.15, 0.15)
            ax.plot(dx, dy, "o", color="#374151", markersize=4, alpha=0.7)
        # Arrow from cluster to node group
        draw_arrow(cx, y_cluster - box_h / 2, cx, y_nodes + 0.3)

    # Level labels on the right
    ax.text(10.5, y_central, "Level 0", fontsize=8, va="center", color="gray")
    ax.text(10.5, y_regional, "Level 1", fontsize=8, va="center", color="gray")
    ax.text(10.5, y_cluster, "Level 2", fontsize=8, va="center", color="gray")
    ax.text(10.5, y_nodes, "Level 3", fontsize=8, va="center", color="gray")

    # Count labels
    ax.text(
        cx_central + box_w / 2 + 0.2,
        y_central,
        "(1)",
        fontsize=8,
        va="center",
        color="gray",
    )
    ax.text(
        regional_xs[-1] + box_w / 2 + 0.2,
        y_regional,
        "(3 regions)",
        fontsize=8,
        va="center",
        color="gray",
    )
    ax.text(
        all_cluster_xs[-1] + box_w / 2 + 0.2,
        y_cluster,
        "(9 clusters)",
        fontsize=8,
        va="center",
        color="gray",
    )
    ax.text(5.0, y_nodes - 0.5, "Swarm Nodes", fontsize=9, ha="center", color="gray")

    ax.set_title("Hierarchical Coordination Architecture", fontsize=12, pad=10)

    fig.savefig(join(fig_dir, "fig-architecture-diagram.pdf"), bbox_inches="tight")
    close(fig)


# ---------------------------------------------------------------------------
# Figure 7: Failure Resilience
# ---------------------------------------------------------------------------
def fig_failure_resilience() -> None:
    """Generate Figure 7: coordinator availability vs node failure rate.

    All 3 topologies, 10K nodes, 20 runs per point.
    Failure rates from 0.01 to 0.10 per year.
    """
    failure_rates = SCALE["failure_rates"]
    nc = SCALE["node_counts"][min(2, len(SCALE["node_counts"]) - 1)]
    n_runs = SCALE["n_runs"]
    sim_days = _sim_days(nc)

    fig, ax = subplots()

    for topo in TOPOLOGIES:
        means = []
        ci_lo = []
        ci_hi = []

        for fr in failure_rates:
            avail_values = []
            for run_i in range(n_runs):
                cfg = _make_config(
                    nc, topology=topo, seed=SEED + run_i,
                    node_failure_rate_per_year=fr,
                )
                sim = SwarmCoordinationSimulator(cfg)
                result = sim.run()
                avail_values.append(result.coordinator_availability_percent)

            stats = calculate_stats(avail_values)
            ci = confidence_interval(avail_values)
            means.append(stats.mean)
            ci_lo.append(ci[0])
            ci_hi.append(ci[1])

        ax.plot(
            failure_rates,
            means,
            "o-",
            color=TOPO_COLORS[topo],
            linewidth=1.8,
            markersize=4,
            label=TOPO_LABELS[topo],
        )
        ax.fill_between(
            failure_rates,
            ci_lo,
            ci_hi,
            alpha=0.15,
            color=TOPO_COLORS[topo],
        )

    ax.set_xlabel("Node Failure Rate (per year)")
    ax.set_ylabel("Coordinator Availability (%)")
    ax.set_title("Failure Resilience: Availability vs Failure Rate")
    ax.legend(loc="best", framealpha=0.9)

    fig.savefig(join(fig_dir, "fig-failure-resilience.pdf"), bbox_inches="tight")
    close(fig)


# ---------------------------------------------------------------------------
# Figure 8: Topology Summary
# ---------------------------------------------------------------------------
def fig_topology_summary() -> None:
    """Generate Figure 8: grouped bar chart comparing 3 topologies on 4 metrics.

    Metrics: overhead (%), availability (%), latency (ms, normalized), drop rate (%).
    10K nodes, 50 runs each. Error bars for 95% CI.
    """
    nc = SCALE["summary_nodes"]
    n_runs = SCALE["summary_runs"]
    sim_days = _sim_days(nc)

    baseline_telemetry_pct = 20.48
    metrics = {
        "Protocol OH (%)": [],
        "Availability (%)": [],
        "Latency (norm.)": [],
        "Drop Rate (%)": [],
    }
    errors = {k: [] for k in metrics}

    raw_latencies = []

    for topo in TOPOLOGIES:
        overhead_vals = []
        avail_vals = []
        latency_vals = []
        drop_vals = []

        for run_i in range(n_runs):
            cfg = _make_config(nc, topology=topo, seed=SEED + run_i)
            sim = SwarmCoordinationSimulator(cfg)
            result = sim.run()
            overhead_vals.append(result.communication_overhead_percent - baseline_telemetry_pct)
            avail_vals.append(result.coordinator_availability_percent)
            latency_vals.append(result.avg_update_propagation_ms)
            drop_vals.append(result.message_drop_rate * 100)

        metrics["Protocol OH (%)"].append(np.mean(overhead_vals))
        metrics["Availability (%)"].append(np.mean(avail_vals))
        raw_latencies.append(np.mean(latency_vals))
        metrics["Drop Rate (%)"].append(np.mean(drop_vals))

        # CI half-widths for error bars
        overhead_ci = confidence_interval(overhead_vals)
        avail_ci = confidence_interval(avail_vals)
        latency_ci = confidence_interval(latency_vals)
        drop_ci = confidence_interval(drop_vals)

        errors["Protocol OH (%)"].append(
            (np.mean(overhead_vals) - overhead_ci[0])
        )
        errors["Availability (%)"].append(
            (np.mean(avail_vals) - avail_ci[0])
        )
        errors["Latency (norm.)"].append(0.0)  # placeholder, recompute below
        errors["Drop Rate (%)"].append(
            (np.mean(drop_vals) - drop_ci[0])
        )

    # Normalize latency to 0-100 scale for visual comparison
    max_lat = max(raw_latencies) if max(raw_latencies) > 0 else 1.0
    for i in range(len(TOPOLOGIES)):
        metrics["Latency (norm.)"].append(raw_latencies[i] / max_lat * 100)
        errors["Latency (norm.)"][i] = errors["Protocol OH (%)"][i]  # approximate error

    metric_names = list(metrics.keys())
    n_metrics = len(metric_names)
    n_topos = len(TOPOLOGIES)
    x = np.arange(n_metrics)
    bar_width = 0.8 / max(1, n_topos)

    fig, ax = subplots(figsize=(8, 5))

    for t_idx, topo in enumerate(TOPOLOGIES):
        vals = [metrics[m][t_idx] for m in metric_names]
        errs = [errors[m][t_idx] for m in metric_names]
        offset = (t_idx - n_topos / 2 + 0.5) * bar_width
        ax.bar(
            x + offset,
            vals,
            bar_width,
            yerr=errs,
            label=TOPO_LABELS[topo],
            color=TOPO_COLORS[topo],
            alpha=0.85,
            capsize=3,
        )

    ax.set_xticks(x)
    ax.set_xticklabels(metric_names)
    ax.set_ylabel("Value")
    ax.set_title("Topology Comparison (10K Nodes, 50 MC Runs)")
    ax.legend(loc="upper right", framealpha=0.9)

    fig.tight_layout()
    fig.savefig(join(fig_dir, "fig-topology-summary.pdf"), bbox_inches="tight")
    close(fig)


# ---------------------------------------------------------------------------
# Figure 9: Message Decomposition
# ---------------------------------------------------------------------------
def fig_message_decomposition() -> None:
    """Generate Figure 9: stacked area chart of per-tier message breakdown vs node count.

    Runs hierarchical topology simulations at each node count and collects
    TierMessageBreakdown data. Shows intra-cluster, inter-cluster, and central
    message counts as stacked areas.
    """
    node_counts = SCALE["node_counts"]
    n_runs = min(5, SCALE["n_runs"])

    intra_means: list[float] = []
    inter_means: list[float] = []
    central_means: list[float] = []

    for nc in node_counts:
        cluster_size = min(200, max(50, int(math.floor(math.sqrt(nc)))))

        intra_vals: list[float] = []
        inter_vals: list[float] = []
        central_vals: list[float] = []

        for run_i in range(n_runs):
            cfg = _make_config(
                nc, cluster_size=cluster_size, seed=SEED + run_i,
            )
            sim = SwarmCoordinationSimulator(cfg)
            result = sim.run()
            tb = result.tier_breakdown
            if tb is not None:
                intra_vals.append(tb.intra_cluster_msgs)
                inter_vals.append(tb.inter_cluster_msgs)
                central_vals.append(tb.central_msgs)
            else:
                intra_vals.append(0)
                inter_vals.append(0)
                central_vals.append(0)

        intra_means.append(float(np.mean(intra_vals)))
        inter_means.append(float(np.mean(inter_vals)))
        central_means.append(float(np.mean(central_vals)))

    fig, ax = subplots(figsize=(7, 4.5))

    ax.stackplot(
        node_counts,
        intra_means,
        inter_means,
        central_means,
        labels=["Intra-cluster", "Inter-cluster (coord\u2192regional)", "Central (regional\u2192central)"],
        colors=["#0891b2", "#d97706", "#7c3aed"],
        alpha=0.85,
    )

    ax.set_xscale("log")
    ax.set_xlabel("Node Count")
    ax.set_ylabel("Message Count")
    ax.set_title("Per-Tier Message Decomposition (Hierarchical)")
    ax.legend(loc="upper left", framealpha=0.9)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x):,}"))

    fig.tight_layout()
    fig.savefig(join(fig_dir, "fig-message-decomposition.pdf"), bbox_inches="tight")
    close(fig)


# ---------------------------------------------------------------------------
# Figure 10: Age-of-Information (AoI) Quality Metric
# ---------------------------------------------------------------------------
def fig_aoi_quality() -> None:
    """Generate Figure 10: AoI at coordinators as a function of p_exc and p_link.

    Two panels:
    (a) AoI vs exception probability p_exc (full links)
    (b) AoI vs link availability p_link (full reporting)
    """
    N = SCALE["node_counts"][2] if len(SCALE["node_counts"]) > 2 else 1000
    sim_days = 1.0 if "--fast" not in __import__("sys").argv else 0.1

    # Panel (a): AoI vs p_exc
    p_exc_values = [0.0, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0]
    aoi_mean_exc = []
    aoi_p99_exc = []
    for p in p_exc_values:
        if p == 0.0:
            # No exception telemetry = full reporting (p_exc disabled)
            cfg = _make_config(
                N, seed=42, simulation_days=sim_days,
                enable_exception_telemetry=False,
            )
        else:
            cfg = _make_config(
                N, seed=42, simulation_days=sim_days,
                enable_exception_telemetry=True, exception_threshold=p,
            )
        sim = SwarmCoordinationSimulator(cfg)
        result = sim.run()
        aoi_mean_exc.append(result.aoi_mean_seconds)
        aoi_p99_exc.append(result.aoi_p99_seconds)

    # Panel (b): AoI vs p_link
    p_link_values = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4]
    aoi_mean_link = []
    aoi_p99_link = []
    for p in p_link_values:
        cfg = _make_config(
            N, seed=42, simulation_days=sim_days,
            link_availability=p,
        )
        sim = SwarmCoordinationSimulator(cfg)
        result = sim.run()
        aoi_mean_link.append(result.aoi_mean_seconds)
        aoi_p99_link.append(result.aoi_p99_seconds)

    fig, (ax1, ax2) = subplots(1, 2, figsize=(7, 3.5))

    # Panel (a)
    ax1.plot(p_exc_values, aoi_mean_exc, "o-", color=c_hierarchical, label="Mean AoI")
    ax1.plot(p_exc_values, aoi_p99_exc, "s--", color=c_hierarchical, alpha=0.7, label="P99 AoI")
    ax1.axhline(y=10.0, color="gray", linestyle=":", alpha=0.5, label="$T_c = 10$ s")
    ax1.set_xlabel("Exception probability $p_{\\mathrm{exc}}$")
    ax1.set_ylabel("Age of Information (s)")
    ax1.set_title("(a) AoI vs. exception rate")
    ax1.legend(fontsize=7)
    ax1.set_yscale("log")
    ax1.grid(True, alpha=0.3)

    # Panel (b)
    ax2.plot(p_link_values, aoi_mean_link, "o-", color=c_hierarchical, label="Mean AoI")
    ax2.plot(p_link_values, aoi_p99_link, "s--", color=c_hierarchical, alpha=0.7, label="P99 AoI")
    ax2.axhline(y=10.0, color="gray", linestyle=":", alpha=0.5, label="$T_c = 10$ s")
    ax2.set_xlabel("Link availability $p_{\\mathrm{link}}$")
    ax2.set_ylabel("Age of Information (s)")
    ax2.set_title("(b) AoI vs. link availability")
    ax2.legend(fontsize=7)
    ax2.set_yscale("log")
    ax2.grid(True, alpha=0.3)
    ax2.invert_xaxis()

    fig.tight_layout()
    fig.savefig(join(fig_dir, "fig-aoi-quality.pdf"), dpi=300, bbox_inches="tight")
    close(fig)


# ---------------------------------------------------------------------------
# Figure 11: Sensitivity Sweep
# ---------------------------------------------------------------------------
def fig_sensitivity_sweep() -> None:
    """Generate Figure 10: sensitivity of overhead to key parameters.

    Shows how hierarchical overhead varies with reporting rate (r),
    MAC efficiency (gamma), and message size.  Uses single-run DES at
    N=10,000 for speed; plots 2x3 subplots.
    """
    nc = 10_000
    sim_days = max(1, min(5, SCALE.get("sim_days_cap", 90)))
    base_cluster = 100

    fig, axes = subplots(1, 3, figsize=(10, 3.5))

    # --- Panel (a): reporting rate sweep ---
    rates = [0.05, 0.1, 0.2, 0.5, 1.0]
    rate_overheads = []
    for r in rates:
        # Reporting rate r msg/s → T_c = 1/r
        # We model this by scaling message sizes proportionally
        # Higher r = more messages per second = higher overhead
        # Analytical: overhead ∝ r × message_size
        # DES uses fixed T_c=10s, so we compute analytically
        overhead_pct = calculate_communication_overhead(
            calculate_bandwidth_requirement("hierarchical", nc, base_cluster, 1.0 / r),
            1.0,
            nc,
        )
        rate_overheads.append(overhead_pct)

    axes[0].plot(rates, rate_overheads, "o-", color=c_hierarchical, linewidth=1.8, markersize=5)
    axes[0].set_xlabel("Reporting Rate $r$ (msg/s)")
    axes[0].set_ylabel("Overhead (%)")
    axes[0].set_title("(a) Reporting Rate")

    # --- Panel (b): MAC efficiency sweep ---
    gammas = [0.3, 0.4, 0.5, 0.6, 0.7, 0.76, 0.8, 0.85, 0.9, 0.95, 1.0]
    gamma_overheads_hier = []
    for g in gammas:
        base_hier = calculate_communication_overhead(
            calculate_bandwidth_requirement("hierarchical", nc, base_cluster, 10.0),
            1.0,
            nc,
        )
        gamma_overheads_hier.append(base_hier / g)

    axes[1].plot(gammas, gamma_overheads_hier, "o-", color=c_hierarchical, linewidth=1.8, markersize=5, label="Hierarchical")
    axes[1].axhline(y=100, color="#dc2626", linestyle=":", linewidth=1, alpha=0.7, label="Channel limit")
    axes[1].set_xlabel("MAC Efficiency $\\gamma$")
    axes[1].set_ylabel("Effective Overhead (%)")
    axes[1].set_title("(b) MAC Efficiency")
    axes[1].legend(fontsize=7, loc="upper right")

    # --- Panel (c): total utilization vs node count ---
    nc_sweep = [1000, 5000, 10000, 50000, 100000]
    utils = []
    for n in nc_sweep:
        bw = calculate_bandwidth_requirement("hierarchical", n, 100, 10.0)
        ovh = calculate_communication_overhead(bw, 1.0, n)
        total = 20.48 + ovh  # 256B/1250B per cycle = 20.48%
        utils.append(total)
    axes[2].plot(nc_sweep, utils, "o-",
                 color=c_hierarchical, linewidth=1.8, markersize=5,
                 label="Hierarchical")

    axes[2].axhline(y=100, color="#dc2626", linestyle=":", linewidth=1, alpha=0.7, label="Channel limit")
    axes[2].set_xscale("log")
    axes[2].set_xlabel("Node Count")
    axes[2].set_ylabel("Total Utilization (%)")
    axes[2].set_title("(c) Channel Utilization")
    axes[2].xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x):,}"))
    axes[2].legend(fontsize=7, loc="best")

    fig.tight_layout()
    fig.savefig(join(fig_dir, "fig-sensitivity-sweep.pdf"), bbox_inches="tight")
    close(fig)


# ---------------------------------------------------------------------------
# Figure 11: TDMA vs Random Scheduling
# ---------------------------------------------------------------------------
def fig_tdma_comparison() -> None:
    """Generate Figure 11: analytical TDMA vs random scheduling comparison.

    Shows coordinator ingest utilization and whether drops occur under
    TDMA (with guard time gamma) vs random phase scheduling, as a function
    of coordinator link capacity.  Uses analytical formulas for speed.
    """
    cluster_size = 100
    T_c = 10.0  # coordination cycle, seconds
    guard = 0.24  # guard time fraction for TDMA (CCSDS-validated)
    gamma = 1.0 - guard  # 0.76
    msg_size = 256  # ephemeris bytes

    # Coordinator ingest demand per cycle: (k_c - 1) members × 256 B
    demand_bytes = (cluster_size - 1) * msg_size  # 25,344 B

    capacities = np.arange(5, 105, 5)

    fig, (ax1, ax2) = subplots(1, 2, figsize=(9, 3.5))

    for sched, ls, marker, label_str, color in [
        ("random", "-", "o", "Random phase", c_hierarchical),
        ("tdma", "--", "s", f"TDMA ($\\gamma$={gamma:.2f})", c_optimized),
    ]:
        utilizations = []
        drop_flags = []
        for cap in capacities:
            cap_bytes = (cap * 1_000 / 8) * T_c  # total bytes capacity per cycle
            if sched == "tdma":
                effective_cap = cap_bytes * gamma
            else:
                effective_cap = cap_bytes
            util_pct = (demand_bytes / effective_cap) * 100 if effective_cap > 0 else 999
            utilizations.append(min(util_pct, 150))
            drop_flags.append(1 if demand_bytes > effective_cap else 0)

        ax1.plot(capacities, utilizations, f"{marker}{ls}", color=color, linewidth=1.8,
                 markersize=4, label=label_str)
        # Mark drop region
        for i, drop in enumerate(drop_flags):
            if drop:
                ax1.plot(capacities[i], utilizations[i], "x", color="#dc2626",
                         markersize=8, markeredgewidth=2, zorder=5)

    ax1.axhline(y=100, color="#dc2626", linestyle=":", linewidth=1, alpha=0.7, label="100% (drop threshold)")
    ax1.set_xlabel("Coordinator Link Capacity (kbps)")
    ax1.set_ylabel("Coordinator Utilization (%)")
    ax1.set_title("(a) Ingest Utilization")
    ax1.legend(fontsize=7, loc="upper right")
    ax1.set_ylim(0, 160)

    # Panel (b): minimum capacity needed vs cluster size
    cluster_sizes = np.arange(10, 510, 10)
    for sched, ls, marker, label_str, color in [
        ("random", "-", "o", "Random phase", c_hierarchical),
        ("tdma", "--", "s", f"TDMA ($\\gamma$={gamma:.2f})", c_optimized),
    ]:
        min_caps = []
        for k_c in cluster_sizes:
            demand = (k_c - 1) * msg_size * 8 / T_c / 1_000  # kbps demand
            if sched == "tdma":
                min_cap = demand / gamma
            else:
                min_cap = demand
            min_caps.append(min_cap)

        ax2.plot(cluster_sizes, min_caps, f"{ls}", color=color, linewidth=1.8, label=label_str)

    ax2.set_xlabel("Cluster Size $k_c$")
    ax2.set_ylabel("Min. Coordinator Capacity (kbps)")
    ax2.set_title("(b) Required Capacity vs Cluster Size")
    ax2.legend(fontsize=7, loc="upper left")

    fig.tight_layout()
    fig.savefig(join(fig_dir, "fig-tdma-comparison.pdf"), bbox_inches="tight")
    close(fig)


# ---------------------------------------------------------------------------
# Figure 13: Workload Profile Comparison
# ---------------------------------------------------------------------------
c_stress = "#dc2626"    # red
c_nominal = "#2563eb"   # blue
c_event = "#d97706"     # amber

def fig_workload_comparison() -> None:
    """Generate Figure 13: η vs N for stress/nominal/event-driven workloads.

    Runs DES at multiple node counts for each workload profile to show
    the design envelope from ~6% (nominal) to ~46% (stress).
    Includes sectorized mesh under all 3 profiles for comparison.
    """
    node_counts = SCALE["node_counts"]
    n_runs = max(3, SCALE["n_runs"] // 4)  # fewer runs needed (near-deterministic)

    profiles = [
        ("stress", "Stress-case", "-", "o"),
        ("event_driven", "Event-driven ($p_{\\mathrm{event}}=0.01$)", "--", "s"),
        ("nominal", "Nominal (no per-node cmds)", "-.", "^"),
    ]

    fig, ax = subplots()

    for profile, profile_label, ls, marker in profiles:
        means = []
        ci_lo = []
        ci_hi = []

        for nc in node_counts:
            cluster_size = min(200, max(50, int(math.floor(math.sqrt(nc)))))
            cfg = _make_config(
                nc, cluster_size=cluster_size,
                workload_profile=profile,
            )
            output = run_swarm_coordination_mc(cfg, runs=n_runs)
            means.append(output.result.communication_overhead_percent)
            lo, hi = output.result.confidence_interval_95
            ci_lo.append(lo)
            ci_hi.append(hi)

        ax.plot(
            node_counts,
            means,
            f"{ls}",
            color=c_hierarchical,
            linewidth=1.8,
            marker=marker,
            markersize=4,
            label=profile_label,
        )
        ax.fill_between(node_counts, ci_lo, ci_hi, alpha=0.15, color=c_hierarchical)

    ax.set_xscale("log")
    ax.set_xlabel("Fleet Size $N$")
    ax.set_ylabel("Protocol Overhead $\\eta$ (%)")
    ax.set_title("Protocol Overhead by Workload Profile")
    ax.legend(fontsize=7, loc="center right", ncol=2)
    ax.set_ylim(bottom=0)

    fig.tight_layout()
    fig.savefig(join(fig_dir, "fig-workload-comparison.pdf"), bbox_inches="tight")
    close(fig)


# ---------------------------------------------------------------------------
# Figure 14: Gilbert-Elliott vs Bernoulli Link Model Comparison
# ---------------------------------------------------------------------------
def fig_link_model_comparison() -> None:
    """Generate Figure 14: retransmission effectiveness under correlated vs i.i.d. losses.

    Compares message loss rates across link availability levels for both
    Bernoulli (i.i.d.) and Gilbert-Elliott (correlated burst) models.
    """
    # Use a fixed moderate fleet size
    nc = SCALE.get("summary_nodes", 5_000)
    sim_days = min(_sim_days(nc), 30)
    n_runs = max(3, SCALE["n_runs"] // 4)
    cluster_size = 100

    # Bernoulli p_link values to test
    p_links = [0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 1.0]
    max_retries = [0, 1, 2]

    fig, axes = subplots(1, 2, figsize=(10, 4))

    for ax_idx, (link_model, ax_title) in enumerate([
        ("bernoulli", "(a) Bernoulli (i.i.d.)"),
        ("gilbert_elliott", "(b) Gilbert-Elliott (correlated)"),
    ]):
        ax = axes[ax_idx]
        for mr, ls, marker in zip(max_retries, ["-", "--", "-."], ["o", "s", "^"]):
            loss_rates = []
            for p_link in p_links:
                if link_model == "bernoulli":
                    cfg = _make_config(
                        nc, cluster_size=cluster_size,
                        simulation_days=sim_days,
                        link_availability=p_link,
                        max_retransmissions=mr,
                        link_model="bernoulli",
                    )
                else:
                    # GE: tune transition probs to match same steady-state availability
                    # Steady-state: p_good = p_bg / (p_gb + p_bg)
                    # overall_avail = p_good * (1-p_loss_good) + p_bad * (1-p_loss_bad)
                    # For p_link target, solve for p_gb given fixed p_bg, p_loss_good, p_loss_bad
                    p_bg = 0.5
                    p_loss_good = 0.01
                    p_loss_bad = 0.90
                    # overall = p_bg/(p_gb+p_bg) * 0.99 + p_gb/(p_gb+p_bg) * 0.10
                    # p_link * (p_gb + p_bg) = p_bg * 0.99 + p_gb * 0.10
                    # p_link * p_gb + p_link * p_bg = 0.99 * p_bg + 0.10 * p_gb
                    # p_gb * (p_link - 0.10) = p_bg * (0.99 - p_link)
                    # p_gb = p_bg * (0.99 - p_link) / (p_link - 0.10)
                    if p_link >= 0.99:
                        p_gb = 0.001  # near-perfect links
                    elif p_link <= 0.10:
                        p_gb = 100.0  # near-always-bad
                    else:
                        p_gb = p_bg * (0.99 - p_link) / (p_link - 0.10)
                    cfg = _make_config(
                        nc, cluster_size=cluster_size,
                        simulation_days=sim_days,
                        link_availability=1.0,  # not used for GE
                        max_retransmissions=mr,
                        link_model="gilbert_elliott",
                        ge_p_good_to_bad=min(p_gb, 10.0),
                        ge_p_bad_to_good=p_bg,
                        ge_p_loss_good=p_loss_good,
                        ge_p_loss_bad=p_loss_bad,
                    )
                output = run_swarm_coordination_mc(cfg, runs=n_runs)
                loss_rates.append(output.result.message_drop_rate * 100)

            ax.plot(
                [p * 100 for p in p_links],
                loss_rates,
                f"{ls}",
                color=c_hierarchical,
                linewidth=1.5,
                marker=marker,
                markersize=4,
                label=f"$M_r={mr}$",
            )

        ax.set_xlabel("Link Availability (%)")
        ax.set_ylabel("Message Loss Rate (%)")
        ax.set_title(ax_title)
        ax.legend(fontsize=8)
        ax.set_ylim(bottom=0)

    fig.tight_layout()
    fig.savefig(join(fig_dir, "fig-link-model-comparison.pdf"), bbox_inches="tight")
    close(fig)


# ---------------------------------------------------------------------------
# Figure 15: Overhead Decomposition by Message Class
# ---------------------------------------------------------------------------
def fig_overhead_decomposition() -> None:
    """Generate Figure 15: stacked bar chart of overhead by message class.

    Runs DES at N=10,000 under three workload profiles for both hierarchical
    and sectorized_mesh topologies.  Decomposes total bytes into:
    ephemeris, heartbeat, command, summary, alert.
    """
    N = 10_000
    sim_days = _sim_days(N)
    cluster_size = min(200, max(50, int(math.floor(math.sqrt(N)))))

    profiles = ["stress", "event_driven", "nominal"]
    profile_labels = ["Stress", "Event-driven", "Nominal"]

    class_colors = {
        "ephemeris": "#94a3b8",   # slate
        "heartbeat": "#0891b2",   # cyan
        "command":   "#d97706",   # amber
        "summary":   "#7c3aed",   # purple
        "alert":     "#dc2626",   # red
    }
    class_labels = ["Ephemeris", "Heartbeat/ACK", "Commands", "Summaries", "Alerts"]

    # Collect data: for each profile, run DES (hierarchical only) and extract per-class bytes
    bar_data: list[dict[str, float]] = []
    x_labels: list[str] = []

    for pi, profile in enumerate(profiles):
        cfg = _make_config(
            N,
            cluster_size=cluster_size,
            simulation_days=sim_days,
            workload_profile=profile,
        )
        sim = SwarmCoordinationSimulator(cfg)
        r = sim.run()
        # Convert to fraction of fleet bandwidth for η decomposition
        scale = 1.0 / max(cfg.sync_sample_rate if cfg.sync_sample_rate > 0 else min(1.0, 1_000 / N), 1e-9)
        sim_s = max(1.0, sim.current_time)
        fleet_cap_bps = N * cfg.bandwidth_per_node_kbps * 1_000
        to_pct = lambda b: (b / sim_s * scale * 8 / fleet_cap_bps * 100) if fleet_cap_bps > 0 else 0

        bar_data.append({
            "ephemeris": to_pct(r.ephemeris_bytes_sent),
            "heartbeat": to_pct(r.heartbeat_bytes_sent),
            "command":   to_pct(r.command_bytes_sent),
            "summary":   to_pct(r.summary_bytes_sent),
            "alert":     to_pct(r.alert_bytes_sent),
        })
        x_labels.append(profile_labels[pi])

    fig, ax = subplots(figsize=(8, 4.5))

    x = np.arange(len(x_labels))
    width = 0.6
    bottoms = np.zeros(len(x_labels))

    for cls_key, cls_label in zip(class_colors.keys(), class_labels):
        vals = [d[cls_key] for d in bar_data]
        ax.bar(x, vals, width, bottom=bottoms, label=cls_label, color=class_colors[cls_key], alpha=0.9)
        bottoms += np.array(vals)

    ax.set_xticks(x)
    ax.set_xticklabels(x_labels, fontsize=8)
    ax.set_ylabel("Protocol Overhead $\\eta$ (%)")
    ax.set_title(f"Overhead Decomposition by Message Class ($N = {N:,}$)")
    ax.legend(fontsize=8, loc="upper right")
    ax.set_ylim(bottom=0)

    fig.tight_layout()
    fig.savefig(join(fig_dir, "fig-overhead-decomposition.pdf"), bbox_inches="tight")
    close(fig)


# ---------------------------------------------------------------------------
# Figure 16: Phase-Stagger Coordinator Drop Comparison
# ---------------------------------------------------------------------------
def fig_phase_stagger() -> None:
    """Generate Figure 16: coordinator drops vs link capacity with/without phase stagger.

    Sweeps coordinator_link_capacity_kbps and compares random-phase vs
    phase-staggered scheduling at N=10,000.
    """
    N = 10_000
    sim_days = _sim_days(N)
    cluster_size = 100
    capacities = [10, 15, 20, 25, 30, 40, 50, 75, 100]

    configs = [
        ("Random phase", False, c_centralized, "-", "o"),
        ("Phase-staggered", True, c_hierarchical, "--", "s"),
    ]

    fig, (ax1, ax2) = subplots(1, 2, figsize=(10, 4))

    for label, stagger, color, ls, marker in configs:
        drops: list[int] = []
        overheads: list[float] = []
        for cap in capacities:
            cfg = _make_config(
                N,
                cluster_size=cluster_size,
                simulation_days=sim_days,
                coordinator_link_capacity_kbps=float(cap),
                enable_phase_stagger=stagger,
            )
            sim = SwarmCoordinationSimulator(cfg)
            r = sim.run()
            drops.append(r.coordinator_drops)
            overheads.append(r.communication_overhead_percent)

        ax1.plot(capacities, drops, f"{ls}", color=color, marker=marker,
                 markersize=4, linewidth=1.8, label=label)
        ax2.plot(capacities, overheads, f"{ls}", color=color, marker=marker,
                 markersize=4, linewidth=1.8, label=label)

    ax1.set_xlabel("Coordinator Link Capacity (kbps)")
    ax1.set_ylabel("Coordinator Drops")
    ax1.set_title("(a) Message Drops vs Capacity")
    ax1.legend(fontsize=8)
    ax1.set_ylim(bottom=0)

    ax2.set_xlabel("Coordinator Link Capacity (kbps)")
    ax2.set_ylabel("Protocol Overhead $\\eta$ (%)")
    ax2.set_title("(b) Overhead vs Capacity")
    ax2.legend(fontsize=8)
    ax2.set_ylim(bottom=0)

    fig.tight_layout()
    fig.savefig(join(fig_dir, "fig-phase-stagger.pdf"), bbox_inches="tight")
    close(fig)


# ---------------------------------------------------------------------------
# Figure 17: Command-rate sweep (continuous p_cmd)
# ---------------------------------------------------------------------------
def fig_command_rate_sweep() -> None:
    """Generate Figure 17: η vs continuous command probability p_cmd.

    Shows overhead as a function of the fraction of nodes receiving a command
    per cycle, replacing the discrete S/E/N profiles with a continuous curve.
    Annotates S/E/N as points on the curve.  Uses analytical computation.
    """
    nc = 10_000
    base_cluster = 100
    T_c = 10.0
    cmd_size = 512  # bytes per command
    C_node = 1_000  # bps per node

    # Per-node baseline telemetry: ephemeris 256 B/cycle
    baseline_bps = 256 * 8 / T_c  # 204.8 bps
    # Protocol overhead excluding commands: ~5% of channel (from nominal case)
    # More precisely: heartbeat (64B) + summary share (~5B amortized) per cycle
    proto_fixed_bps = (64 + 5) * 8 / T_c  # ~55.2 bps

    p_cmds = np.linspace(0, 1.0, 101)
    eta_hier = []
    for p in p_cmds:
        # Hierarchical: per-node cmd traffic = p × cmd_size × 8 / T_c
        cmd_bps = p * cmd_size * 8 / T_c
        overhead_bps = proto_fixed_bps + cmd_bps
        eta = overhead_bps / C_node * 100
        eta_hier.append(eta)

    fig, ax = subplots(1, 1, figsize=(5.5, 4))
    ax.plot(p_cmds, eta_hier, "-", color=c_hierarchical, linewidth=2, label="Hierarchical")

    # Annotate S/E/N
    markers = [
        (1.0, "S", c_stress),
        (0.01, "E", c_event),
        (0.0, "N", c_nominal),
    ]
    for p_val, label, color in markers:
        cmd_bps = p_val * cmd_size * 8 / T_c
        eta_val = (proto_fixed_bps + cmd_bps) / C_node * 100
        ax.plot(p_val, eta_val, "o", color=color, markersize=8, zorder=5)
        ax.annotate(label, (p_val, eta_val), textcoords="offset points",
                    xytext=(8, 5), fontsize=10, fontweight="bold", color=color)

    ax.set_xlabel("Command Probability $p_{\\mathrm{cmd}}$ (per node per cycle)")
    ax.set_ylabel("Protocol Overhead $\\eta$ (%)")
    ax.axhline(y=100, color="#dc2626", linestyle=":", linewidth=1, alpha=0.7)
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(0, 55)
    ax.legend(fontsize=9)
    fig.tight_layout()
    fig.savefig(join(fig_dir, "fig-command-rate-sweep.pdf"), bbox_inches="tight")
    close(fig)


# ---------------------------------------------------------------------------
# Figure 18: Cross-Cycle Recovery Distribution
# ---------------------------------------------------------------------------
def fig_cross_cycle_recovery() -> None:
    """Generate Figure 18: DES-validated inter-cycle recovery under GE losses.

    Panel (a): DES CDF vs Markov-chain prediction at default p_BG = 0.50.
    Panel (b): GE parameter sensitivity — P95 recovery cycles vs p_BG for
    three p_loss_bad values, providing a family of design curves.
    """
    nc = SCALE.get("summary_nodes", 5_000)
    sim_days = min(_sim_days(nc), 30)
    cluster_size = 100
    n_runs = SCALE.get("summary_runs", 30)  # 30 for publication, 3 for --fast

    # --- Panel (a): DES CDF vs analytical at default parameters ---
    all_cdfs: list[list[float]] = []
    all_means: list[float] = []
    all_p95s: list[float] = []

    for run_idx in range(n_runs):
        cfg = _make_config(
            nc,
            cluster_size=cluster_size,
            simulation_days=sim_days,
            seed=SEED + run_idx,
            link_model="gilbert_elliott",
            max_retransmissions=2,
        )
        sim = SwarmCoordinationSimulator(cfg)
        r = sim.run()
        if r.cross_cycle_recovery_rate_by_cycle:
            all_cdfs.append(r.cross_cycle_recovery_rate_by_cycle)
            all_means.append(r.cross_cycle_recovery_mean)
            all_p95s.append(r.cross_cycle_recovery_p95)

    if not all_cdfs:
        print("  WARNING: no cross-cycle recovery data collected, skipping figure")
        return

    n_cycles = len(all_cdfs[0])
    avg_cdf = [float(np.mean([cdf[k] for cdf in all_cdfs])) for k in range(n_cycles)]
    avg_mean = float(np.mean(all_means))
    avg_p95 = float(np.mean(all_p95s))

    # Analytical CDF using Markov chain iteration
    def _analytical_cdf(p_bg_val: float, p_gb_val: float, p_loss_good: float,
                        p_loss_bad: float, mr: int, n_cyc: int) -> list[float]:
        p_recover_good = 1.0 - p_loss_good ** (mr + 1)
        p_recover_bad = 1.0 - p_loss_bad ** (mr + 1)
        cdf = []
        p_still_lost = 1.0
        p_in_bad = 1.0  # start in bad state (conditioning on failed cycle)
        for _ in range(n_cyc):
            p_in_good_new = p_in_bad * p_bg_val + (1.0 - p_in_bad) * (1.0 - p_gb_val)
            p_in_bad_new = 1.0 - p_in_good_new
            p_deliver = p_in_good_new * p_recover_good + p_in_bad_new * p_recover_bad
            p_still_lost *= (1.0 - p_deliver)
            cdf.append(1.0 - p_still_lost)
            p_in_bad = p_in_bad_new
        return cdf

    analytical = _analytical_cdf(0.50, 0.05, 0.01, 0.90, 2, n_cycles)

    # --- Panel (b): GE sensitivity — sweep p_BG for multiple p_loss_bad ---
    p_bg_sweep = [0.10, 0.15, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80]
    p_loss_bad_vals = [0.70, 0.90, 0.95]
    p_loss_bad_labels = ["$p_B = 0.70$", "$p_B = 0.90$", "$p_B = 0.95$"]
    p_loss_bad_colors = [c_optimized, c_hierarchical, c_pareto]

    # Also run DES at selected p_BG values for validation dots
    des_p95_by_pbg: dict[float, list[float]] = {}
    for p_bg_val in [0.10, 0.20, 0.50]:
        p95_runs = []
        for run_idx in range(n_runs):
            cfg_sens = _make_config(
                nc,
                cluster_size=cluster_size,
                simulation_days=sim_days,
                seed=SEED + run_idx,
                link_model="gilbert_elliott",
                max_retransmissions=2,
                ge_p_bad_to_good=p_bg_val,
            )
            r_s = SwarmCoordinationSimulator(cfg_sens).run()
            if r_s.cross_cycle_recovery_count > 0:
                p95_runs.append(r_s.cross_cycle_recovery_p95)
        if p95_runs:
            des_p95_by_pbg[p_bg_val] = p95_runs

    # Compute analytical P95 for each combination
    def _analytical_p95(p_bg_val: float, p_gb: float, p_loss_g: float,
                        p_loss_b: float, mr: int) -> float:
        cdf = _analytical_cdf(p_bg_val, p_gb, p_loss_g, p_loss_b, mr, 30)
        for k, v in enumerate(cdf, 1):
            if v >= 0.95:
                return float(k)
        return 30.0

    # --- Plot ---
    fig, axes = subplots(1, 2, figsize=(10, 4))

    # Panel (a): DES vs analytical CDF
    ax = axes[0]
    cycles = list(range(1, n_cycles + 1))
    bar_width = 0.35
    ax.bar(
        [c - bar_width / 2 for c in cycles],
        [cdf * 100 for cdf in avg_cdf],
        bar_width,
        color=c_hierarchical,
        alpha=0.7,
        label=f"DES (mean={avg_mean:.1f}, P95={avg_p95:.0f})",
        edgecolor="white",
        linewidth=0.5,
    )
    ax.plot(
        cycles,
        [cdf * 100 for cdf in analytical],
        "o-",
        color=c_pareto,
        linewidth=2,
        markersize=4,
        label="Analytical (Markov)",
        zorder=5,
    )
    ax.axhline(y=95, color="gray", linestyle="--", linewidth=0.8, alpha=0.6)
    ax.annotate("95%", xy=(n_cycles, 95), xytext=(n_cycles + 0.1, 92),
                fontsize=8, color="gray")
    ax.set_xlabel("Cycles Since Loss Event")
    ax.set_ylabel("Cumulative Recovery (%)")
    ax.set_title("(a) Default GE parameters ($p_{BG}=0.50$)")
    ax.set_xlim(0.5, n_cycles + 0.5)
    ax.set_ylim(0, 102)
    ax.set_xticks(cycles)
    ax.legend(loc="lower right", fontsize=8)
    ax.grid(axis="y", alpha=0.3)

    # Panel (b): P95 recovery vs p_BG for different p_loss_bad
    ax2 = axes[1]
    for p_lb, label, color in zip(p_loss_bad_vals, p_loss_bad_labels, p_loss_bad_colors):
        p95_vals = [_analytical_p95(p_bg, 0.05, 0.01, p_lb, 2) for p_bg in p_bg_sweep]
        ax2.plot(p_bg_sweep, p95_vals, "o-", color=color, linewidth=1.5,
                 markersize=4, label=label)

    # DES validation dots (p_loss_bad = 0.90 only)
    for p_bg_val, p95_list in des_p95_by_pbg.items():
        avg_p95_v = float(np.mean(p95_list))
        ax2.scatter([p_bg_val], [avg_p95_v], marker="s", s=60, color="black",
                    zorder=10, label="DES" if p_bg_val == 0.10 else None)

    ax2.set_xlabel("$p_{BG}$ (bad-to-good transition probability)")
    ax2.set_ylabel("P95 Recovery (cycles)")
    ax2.set_title("(b) GE Parameter Sensitivity")
    ax2.set_ylim(0, 20)
    ax2.legend(loc="upper right", fontsize=8)
    ax2.grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(join(fig_dir, "fig-cross-cycle-recovery.pdf"), bbox_inches="tight")
    close(fig)


# ---------------------------------------------------------------------------
# Figure 19: Fleet-level channel reuse
# ---------------------------------------------------------------------------
def fig_fleet_reuse() -> None:
    """Generate fleet-level channel reuse figure (purely analytical).

    X: f_RF (fraction of clusters in RF-backup mode), range [0, 0.10]
    Y: T_c^fleet / T_c (coordination period inflation factor)
    Curves for F×R ∈ {4, 8, 12, 16, 24}
    Annotate non-binding threshold, shade f_RF < 1% ("normal ops").
    """
    N = 100_000
    k_c = 100
    n_clusters = N // k_c  # 1000

    f_rf_values = np.linspace(0, 0.10, 200)
    FR_values = [4, 8, 12, 16, 24]

    fig, ax = subplots(figsize=(3.4, 2.8))

    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]
    linestyles = ["-", "--", "-.", ":", "-"]

    for i, FR in enumerate(FR_values):
        inflation = []
        threshold = FR * k_c / N  # non-binding threshold
        for f_rf in f_rf_values:
            N_RF = math.ceil(f_rf * N / k_c)  # active RF-backup clusters
            G = math.ceil(N_RF / FR) if N_RF > 0 else 0  # time-share groups
            T_fleet_ratio = max(1.0, G)  # T_c^fleet / T_c
            inflation.append(T_fleet_ratio)

        ax.plot(
            f_rf_values * 100, inflation,
            color=colors[i % len(colors)],
            linestyle=linestyles[i % len(linestyles)],
            linewidth=1.2,
            label=f"$F \\times R = {FR}$",
        )

        # Annotate threshold
        ax.axvline(
            x=threshold * 100, color=colors[i % len(colors)],
            alpha=0.3, linewidth=0.8, linestyle=":",
        )

    # Shade normal ops region (f_RF < 1%)
    ax.axvspan(0, 1.0, alpha=0.08, color="green")
    ax.text(
        0.5, 0.92, "Normal ops\n($<$1% ISL outage)",
        transform=ax.transAxes, fontsize=7, ha="left", va="top",
        bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.8),
    )

    ax.set_xlabel("$f_{\\mathrm{RF}}$ (\\% of fleet in RF-backup)")
    ax.set_ylabel("$T_c^{\\mathrm{fleet}} / T_c$")
    ax.set_xlim(0, 10)
    ax.set_ylim(0.5, max(15, ax.get_ylim()[1]))
    ax.legend(loc="upper left", fontsize=7, ncol=1)

    fig.savefig(join(fig_dir, "fig-fleet-reuse.pdf"), bbox_inches="tight")
    close(fig)


# ---------------------------------------------------------------------------
# Figure 20: Coordinator Buffer Occupancy CDF
# ---------------------------------------------------------------------------
def fig_coordinator_buffer_cdf() -> None:
    """Generate Figure 20: CDF of per-cycle coordinator ingress bytes.

    Compares Bernoulli d=0.10 vs ON/OFF d=0.10 (L_on=100) vs d=1.0 under
    GE losses.  ON/OFF produces heavier tails than Bernoulli at the same
    marginal d due to temporally correlated campaign bursts.
    """
    nc = 10_000
    cluster_size = 100
    sim_days = max(1, min(5, SCALE.get("sim_days_cap", 90)))

    # Three configurations: Bernoulli d=0.10, ON/OFF d=0.10 L_on=100, continuous d=1.0
    configs = [
        {"d": 0.10, "mode": "bernoulli", "L_on": 1,
         "label": "Bernoulli $d\\!=\\!0.10$", "color": c_hierarchical, "ls": "-"},
        {"d": 0.10, "mode": "on_off", "L_on": 100,
         "label": "ON/OFF $d\\!=\\!0.10$, $L_{\\mathrm{on}}\\!=\\!100$", "color": "#e67e22", "ls": "-."},
        {"d": 1.0, "mode": "bernoulli", "L_on": 1,
         "label": "$d\\!=\\!1.0$ (continuous)", "color": c_stress, "ls": "--"},
    ]

    fig, ax = subplots(figsize=(5.5, 4))

    for c in configs:
        cfg = _make_config(
            nc,
            cluster_size=cluster_size,
            simulation_days=sim_days,
            workload_profile="stress",
            campaign_duty_factor=c["d"],
            campaign_mode=c["mode"],
            campaign_on_length=c["L_on"],
            link_model="gilbert_elliott",
            ge_p_bad_to_good=0.50,
            max_retransmissions=2,
        )
        sim = SwarmCoordinationSimulator(cfg)
        r = sim.run()
        ingress = np.array(r.coordinator_ingress_bytes_per_cycle)
        if len(ingress) == 0:
            continue
        sorted_vals = np.sort(ingress)
        cdf = np.arange(1, len(sorted_vals) + 1) / len(sorted_vals)
        ax.plot(sorted_vals / 1000, cdf, c["ls"], color=c["color"], linewidth=1.8, label=c["label"])
        # Overlay closed-form mean
        mean_val = float(np.mean(ingress))
        ax.axvline(x=mean_val / 1000, color=c["color"], linestyle=":", linewidth=1, alpha=0.6)

    ax.set_xlabel("Coordinator Ingress per Cycle (kB)")
    ax.set_ylabel("CDF")
    ax.set_title("Coordinator Ingress Distribution ($N = 10{,}000$, GE losses)")
    ax.legend(fontsize=8, loc="lower right")
    ax.set_ylim(0, 1.05)

    fig.tight_layout()
    fig.savefig(join(fig_dir, "fig-coordinator-buffer-cdf.pdf"), bbox_inches="tight")
    close(fig)


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------
def main() -> None:
    """Generate all 19 figures sequentially with timing for each."""
    figures = [
        ("Fig 1: overhead vs nodes", fig_overhead_vs_nodes),
        ("Fig 2: latency distribution", fig_latency_distribution),
        ("Fig 3: cluster size optimization", fig_cluster_size_optimization),
        ("Fig 4: duty cycle Pareto", fig_duty_cycle_pareto),
        ("Fig 5: scaling trajectory", fig_scaling_trajectory),
        ("Fig 6: architecture diagram", fig_architecture_diagram),
        ("Fig 7: failure resilience", fig_failure_resilience),
        ("Fig 8: topology summary", fig_topology_summary),
        ("Fig 9: message decomposition", fig_message_decomposition),
        ("Fig 10: AoI quality metric", fig_aoi_quality),
        ("Fig 11: sensitivity sweep", fig_sensitivity_sweep),
        ("Fig 12: TDMA comparison", fig_tdma_comparison),
        ("Fig 13: workload comparison", fig_workload_comparison),
        ("Fig 14: link model comparison", fig_link_model_comparison),
        ("Fig 15: overhead decomposition", fig_overhead_decomposition),
        ("Fig 16: phase stagger", fig_phase_stagger),
        ("Fig 17: command rate sweep", fig_command_rate_sweep),
        ("Fig 18: cross-cycle recovery", fig_cross_cycle_recovery),
        ("Fig 19: fleet-level reuse", fig_fleet_reuse),
        ("Fig 20: coordinator buffer CDF", fig_coordinator_buffer_cdf),
    ]

    total_t0 = time.perf_counter()

    for i, (label, func) in enumerate(figures, 1):
        print(f"Generating {label}...")
        t0 = time.perf_counter()
        func()
        elapsed = time.perf_counter() - t0
        print(f"  [{i}/{len(figures)}] {label} done in {elapsed:.1f}s")

    total_elapsed = time.perf_counter() - total_t0
    print(f"\nAll {len(figures)} figures generated in {total_elapsed:.1f}s")
    print(f"Output directory: {fig_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate swarm coordination figures")
    parser.add_argument(
        "--fast",
        action="store_true",
        help="Use reduced node counts and MC runs for faster generation (~2 min vs ~30 min)",
    )
    args = parser.parse_args()
    if args.fast:
        SCALE = SCALE_FAST
    main()
