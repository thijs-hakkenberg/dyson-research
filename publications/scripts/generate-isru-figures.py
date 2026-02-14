#!/usr/bin/env python3
"""
Generate publication-quality figures for the ISRU Economic Crossover paper.

Implements Equations 1-9 from the paper and produces 5 PDF figures:
  1. fig-cumulative-cost.pdf  — Earth vs ISRU cumulative cost curves
  2. fig-unit-cost.pdf        — Per-unit cost with launch cost floor
  3. fig-tornado.pdf          — Tornado chart of parameter sensitivities
  4. fig-heatmap.pdf          — 2D heatmap: launch cost vs ISRU capital → crossover
  5. fig-histogram.pdf        — Monte Carlo histogram of crossover points

Usage:
    source publications/scripts/.venv/bin/activate
    python publications/scripts/generate-isru-figures.py
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# ---------------------------------------------------------------------------
# Output directory
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(SCRIPT_DIR, "..", "drafts", "figures")
os.makedirs(FIG_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# Publication style
# ---------------------------------------------------------------------------
plt.rcParams.update({
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
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.05,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "grid.linewidth": 0.5,
})

# ---------------------------------------------------------------------------
# Color scheme
# ---------------------------------------------------------------------------
C_EARTH = "#d97706"     # amber
C_ISRU = "#0891b2"      # cyan
C_CROSS = "#16a34a"     # green
C_FLOOR = "#dc2626"     # red for launch cost floor

# ---------------------------------------------------------------------------
# Baseline parameters (Table 1 in paper)
# ---------------------------------------------------------------------------
BASELINE = {
    "m": 1850,              # unit mass (kg)
    "p_launch": 1000,       # launch cost ($/kg)
    "K": 50e9,              # ISRU capital ($)
    "C_mfg1": 75e6,         # first-unit Earth manufacturing cost ($)
    "C_ops1": 5e6,          # first-unit ISRU ops cost ($)
    "LR_E": 0.85,           # Earth learning rate
    "LR_I": 0.90,           # ISRU learning rate
    "t0": 5,                # ramp-up midpoint (years)
    "k_ramp": 2.0,          # S-curve steepness
    "N_total": 10000,       # amortization horizon
    "prod_rate": 500,       # units/year at full capacity
}


# ---------------------------------------------------------------------------
# Cost model (Equations 1-9)
# ---------------------------------------------------------------------------

def learning_exponent(lr):
    """Wright learning curve exponent: b = ln(LR) / ln(2)."""
    return np.log(lr) / np.log(2)


def s_curve(t, t0, k=2.0):
    """Logistic ramp-up function S(t) = 1 / (1 + exp(-k*(t - t0)))."""
    return 1.0 / (1.0 + np.exp(-k * (t - t0)))


def unit_to_time(n, prod_rate=500, t0=5):
    """Map unit number to elapsed time (years).

    Production begins at the ramp-up midpoint t0 (after construction),
    then accumulates at prod_rate units/year at full capacity.
    """
    return t0 + np.asarray(n, dtype=float) / prod_rate


def earth_unit_cost(n, params):
    """Eq 2-4: Earth per-unit cost = manufacturing learning + constant launch."""
    b_E = learning_exponent(params["LR_E"])
    c_mfg = params["C_mfg1"] * np.asarray(n, dtype=float) ** b_E
    c_launch = params["m"] * params["p_launch"]
    return c_mfg + c_launch


def isru_unit_cost(n, params):
    """Eq 6-8: ISRU per-unit cost = amortized capital + ops*learning/S-curve."""
    n = np.asarray(n, dtype=float)
    b_I = learning_exponent(params["LR_I"])
    t_n = unit_to_time(n, params.get("prod_rate", 500), params["t0"])
    s = s_curve(t_n, params["t0"], params.get("k_ramp", 2.0))
    s = np.maximum(s, 0.05)
    c_capital = params["K"] / params["N_total"]
    c_ops = params["C_ops1"] * n ** b_I / s
    return c_capital + c_ops


def cumulative_cost(unit_cost_fn, N_max, params):
    """Compute cumulative cost for units 1..N_max."""
    ns = np.arange(1, N_max + 1, dtype=float)
    unit_costs = unit_cost_fn(ns, params)
    cum = np.cumsum(unit_costs)
    return ns, unit_costs, cum


def cumulative_isru(N_max, params):
    """Eq 9: ISRU cumulative = K + sum of ops costs."""
    ns = np.arange(1, N_max + 1, dtype=float)
    b_I = learning_exponent(params["LR_I"])
    t_n = unit_to_time(ns, params.get("prod_rate", 500), params["t0"])
    s = s_curve(t_n, params["t0"], params.get("k_ramp", 2.0))
    s = np.maximum(s, 0.05)
    ops_costs = params["C_ops1"] * ns ** b_I / s
    cum = params["K"] + np.cumsum(ops_costs)
    # Per-unit costs include amortized capital (for display)
    unit_costs = params["K"] / params["N_total"] + ops_costs
    return ns, unit_costs, cum


def find_crossover(params, N_max=20000):
    """Find smallest N where ISRU cumulative <= Earth cumulative."""
    ns = np.arange(1, N_max + 1, dtype=float)
    # Earth cumulative
    b_E = learning_exponent(params["LR_E"])
    earth_cum = np.cumsum(params["C_mfg1"] * ns ** b_E + params["m"] * params["p_launch"])
    # ISRU cumulative
    b_I = learning_exponent(params["LR_I"])
    t_n = unit_to_time(ns, params.get("prod_rate", 500), params["t0"])
    s = s_curve(t_n, params["t0"], params.get("k_ramp", 2.0))
    s = np.maximum(s, 0.05)
    ops = params["C_ops1"] * ns ** b_I / s
    isru_cum = params["K"] + np.cumsum(ops)
    # Find crossover
    diff = isru_cum - earth_cum
    crossings = np.where(diff <= 0)[0]
    if len(crossings) > 0:
        return int(ns[crossings[0]])
    return N_max  # no crossover found


# ---------------------------------------------------------------------------
# Figure 1: Cumulative Cost Comparison
# ---------------------------------------------------------------------------
def fig_cumulative_cost():
    p = BASELINE.copy()
    cross_n = find_crossover(p)
    N_max = max(cross_n * 2 + 500, 8000)
    ns_e, _, cum_e = cumulative_cost(earth_unit_cost, N_max, p)
    ns_i, _, cum_i = cumulative_isru(N_max, p)

    # Interpolate crossover cumulative value
    cross_val = np.interp(cross_n, ns_e, cum_e)

    fig, ax = plt.subplots()
    ax.plot(ns_e, cum_e / 1e9, color=C_EARTH, linewidth=2, label="Earth launch")
    ax.plot(ns_i, cum_i / 1e9, color=C_ISRU, linewidth=2, label="ISRU")

    # Mark crossover
    ax.axvline(cross_n, color=C_CROSS, linestyle="--", linewidth=1, alpha=0.7)
    ax.plot(cross_n, cross_val / 1e9, "o", color=C_CROSS, markersize=8, zorder=5)

    # Place annotation adaptively
    txt_x = cross_n + N_max * 0.08
    txt_y = cross_val / 1e9 * 1.15
    ax.annotate(
        f"Crossover\n~{cross_n:,} units",
        xy=(cross_n, cross_val / 1e9),
        xytext=(txt_x, txt_y),
        fontsize=9,
        color=C_CROSS,
        fontweight="bold",
        arrowprops=dict(arrowstyle="->", color=C_CROSS, lw=1.2),
    )

    # Shade savings region
    ax.fill_between(
        ns_e[cross_n - 1:], cum_e[cross_n - 1:] / 1e9, cum_i[cross_n - 1:] / 1e9,
        alpha=0.10, color=C_CROSS, label="ISRU savings",
    )

    ax.set_xlabel("Production Volume (units)")
    ax.set_ylabel("Cumulative Cost (\\$B)")
    ax.set_xlim(0, N_max)
    ax.set_ylim(0, None)
    ax.legend(loc="upper left", framealpha=0.9)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x):,}"))

    fig.savefig(os.path.join(FIG_DIR, "fig-cumulative-cost.pdf"))
    plt.close(fig)
    print(f"  [1/5] fig-cumulative-cost.pdf  (crossover at ~{cross_n:,} units)")


# ---------------------------------------------------------------------------
# Figure 2: Per-Unit Cost Comparison
# ---------------------------------------------------------------------------
def fig_unit_cost():
    p = BASELINE.copy()
    cross_n = find_crossover(p)
    N_max = max(cross_n * 2 + 500, 8000)
    ns = np.arange(1, N_max + 1, dtype=float)

    earth_costs = earth_unit_cost(ns, p) / 1e6  # $M
    isru_costs = isru_unit_cost(ns, p) / 1e6

    launch_floor = p["m"] * p["p_launch"] / 1e6

    fig, ax = plt.subplots()
    step = max(1, len(ns) // 800)
    ax.plot(ns[::step], earth_costs[::step], color=C_EARTH, linewidth=2, label="Earth launch")
    ax.plot(ns[::step], isru_costs[::step], color=C_ISRU, linewidth=2, label="ISRU")

    # Launch cost floor
    ax.axhline(launch_floor, color=C_FLOOR, linestyle=":", linewidth=1.5, alpha=0.8)
    ax.annotate(
        f"Launch cost floor (\\${launch_floor:.2f}M/unit)",
        xy=(N_max * 0.55, launch_floor),
        xytext=(N_max * 0.55, launch_floor + 1.5),
        fontsize=8,
        color=C_FLOOR,
    )

    # Determine y-axis range: show enough to see both curves clearly
    # but clip extreme early ISRU values
    y_max = max(earth_costs[0], 40)
    ax.set_xlabel("Cumulative Production (units)")
    ax.set_ylabel("Per-Unit Cost (\\$M)")
    ax.set_xlim(0, N_max)
    ax.set_ylim(0, y_max)
    ax.legend(loc="upper right", framealpha=0.9)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x):,}"))

    fig.savefig(os.path.join(FIG_DIR, "fig-unit-cost.pdf"))
    plt.close(fig)
    print("  [2/5] fig-unit-cost.pdf")


# ---------------------------------------------------------------------------
# Figure 3: Tornado Diagram (Sensitivity Analysis)
# ---------------------------------------------------------------------------
def fig_tornado():
    base_cross = find_crossover(BASELINE)

    # Define parameter variations (label, param_key, low_delta, high_delta)
    # Note: ramp-up time t0 does not affect unit-count crossover (it cancels
    # in the S-curve since production starts at t0), so it is omitted here.
    variations = [
        ("Earth LR ±0.05", "LR_E", -0.05, +0.05),
        ("ISRU capital ±\\$25B", "K", -25e9, +25e9),
        ("ISRU LR ±0.05", "LR_I", -0.05, +0.05),
        ("Launch cost ±\\$500/kg", "p_launch", -500, +500),
    ]

    labels = []
    low_deltas = []
    high_deltas = []

    for label, param, delta_lo, delta_hi in variations:
        p_lo = BASELINE.copy()
        p_lo[param] = BASELINE[param] + delta_lo
        cross_lo = find_crossover(p_lo)

        p_hi = BASELINE.copy()
        p_hi[param] = BASELINE[param] + delta_hi
        cross_hi = find_crossover(p_hi)

        labels.append(label)
        low_deltas.append(cross_lo - base_cross)
        high_deltas.append(cross_hi - base_cross)

    # Sort by total range (most sensitive first)
    ranges = [abs(h - l) for h, l in zip(high_deltas, low_deltas)]
    order = np.argsort(ranges)[::-1]
    labels = [labels[i] for i in order]
    low_deltas = [low_deltas[i] for i in order]
    high_deltas = [high_deltas[i] for i in order]

    fig, ax = plt.subplots(figsize=(6, 3.5))
    y_pos = np.arange(len(labels))

    for i, (lo, hi) in enumerate(zip(low_deltas, high_deltas)):
        # Draw the two bars from center (0) outward
        ax.barh(i, lo, height=0.6, left=0, color=C_ISRU, alpha=0.85,
                edgecolor="white", linewidth=0.5)
        ax.barh(i, hi, height=0.6, left=0, color=C_EARTH, alpha=0.85,
                edgecolor="white", linewidth=0.5)
        # Value labels at ends
        for val in [lo, hi]:
            if val != 0:
                ha = "right" if val < 0 else "left"
                offset = -50 if val < 0 else 50
                ax.text(val + offset, i, f"{val:+,.0f}",
                        va="center", ha=ha, fontsize=7)

    ax.axvline(0, color="black", linewidth=0.8)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels)
    ax.set_xlabel(f"Change in Crossover from Baseline ({base_cross:,} units)")
    ax.invert_yaxis()

    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=C_ISRU, alpha=0.85, label="Earlier crossover"),
        Patch(facecolor=C_EARTH, alpha=0.85, label="Later crossover"),
    ]
    ax.legend(handles=legend_elements, loc="lower right", fontsize=8, framealpha=0.9)

    fig.savefig(os.path.join(FIG_DIR, "fig-tornado.pdf"))
    plt.close(fig)
    print(f"  [3/5] fig-tornado.pdf  (baseline={base_cross:,})")


# ---------------------------------------------------------------------------
# Figure 4: 2D Heatmap — Launch Cost vs ISRU Capital → Crossover
# ---------------------------------------------------------------------------
def fig_heatmap():
    launch_costs = np.linspace(200, 2500, 60)
    isru_capitals = np.linspace(20e9, 120e9, 60)

    crossover_grid = np.zeros((len(isru_capitals), len(launch_costs)))

    for i, K in enumerate(isru_capitals):
        for j, pl in enumerate(launch_costs):
            p = BASELINE.copy()
            p["p_launch"] = pl
            p["K"] = K
            crossover_grid[i, j] = find_crossover(p)

    fig, ax = plt.subplots()
    im = ax.contourf(
        launch_costs,
        isru_capitals / 1e9,
        crossover_grid,
        levels=np.arange(0, 15001, 1000),
        cmap="RdYlGn_r",
        extend="max",
    )
    contour_lines = ax.contour(
        launch_costs,
        isru_capitals / 1e9,
        crossover_grid,
        levels=[2000, 3500, 5000, 7500, 10000],
        colors="black",
        linewidths=0.8,
        alpha=0.6,
    )
    ax.clabel(contour_lines, inline=True, fontsize=8, fmt="%d")

    fig.colorbar(im, ax=ax, label="Crossover Point (units)")

    # Mark baseline
    ax.plot(
        BASELINE["p_launch"], BASELINE["K"] / 1e9,
        "k*", markersize=14, zorder=5, label="Baseline",
    )
    ax.legend(loc="upper left", fontsize=8, framealpha=0.9)

    ax.set_xlabel("Launch Cost (\\$/kg)")
    ax.set_ylabel("ISRU Capital Investment (\\$B)")

    fig.savefig(os.path.join(FIG_DIR, "fig-heatmap.pdf"))
    plt.close(fig)
    print("  [4/5] fig-heatmap.pdf")


# ---------------------------------------------------------------------------
# Figure 5: Monte Carlo Histogram
# ---------------------------------------------------------------------------
def fig_histogram():
    rng = np.random.default_rng(42)
    n_runs = 1000
    crossovers = []

    for _ in range(n_runs):
        p = BASELINE.copy()
        p["p_launch"] = rng.uniform(500, 2000)
        p["K"] = rng.uniform(30e9, 100e9)
        p["LR_E"] = np.clip(rng.normal(0.85, 0.03), 0.75, 0.95)
        p["LR_I"] = np.clip(rng.normal(0.90, 0.03), 0.80, 0.98)
        p["t0"] = rng.uniform(3, 8)
        crossovers.append(find_crossover(p))

    crossovers = np.array(crossovers)
    median = np.median(crossovers)
    q25, q75 = np.percentile(crossovers, [25, 75])
    p5, p90, p95 = np.percentile(crossovers, [5, 90, 95])

    fig, ax = plt.subplots()
    ax.hist(
        crossovers, bins=40, color=C_ISRU, alpha=0.75,
        edgecolor="white", linewidth=0.5,
    )

    # Median line
    ax.axvline(median, color=C_CROSS, linewidth=2, linestyle="-",
               label=f"Median: {int(median):,}")
    # IQR shaded
    ax.axvspan(q25, q75, alpha=0.12, color=C_EARTH,
               label=f"IQR: [{int(q25):,}, {int(q75):,}]")
    # 90th percentile
    ax.axvline(p90, color=C_FLOOR, linewidth=1.5, linestyle=":",
               alpha=0.7, label=f"90th pctl: {int(p90):,}")

    ax.set_xlabel("Crossover Point $N^*$ (units)")
    ax.set_ylabel("Frequency")
    ax.legend(loc="upper right", framealpha=0.9)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x):,}"))

    fig.savefig(os.path.join(FIG_DIR, "fig-histogram.pdf"))
    plt.close(fig)
    print(f"  [5/5] fig-histogram.pdf  (median={int(median):,}, "
          f"IQR=[{int(q25):,},{int(q75):,}], P90={int(p90):,})")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print(f"Generating figures in: {FIG_DIR}\n")

    # Diagnostic: print baseline and scenario crossovers
    base = find_crossover(BASELINE)
    print(f"Baseline crossover:     ~{base:,} units")

    p_opt = BASELINE.copy()
    p_opt["p_launch"] = 500
    p_opt["K"] = 30e9
    print(f"Optimistic crossover:   ~{find_crossover(p_opt):,} units")

    p_con = BASELINE.copy()
    p_con["p_launch"] = 2000
    p_con["K"] = 100e9
    print(f"Conservative crossover: ~{find_crossover(p_con):,} units")
    print()

    fig_cumulative_cost()
    fig_unit_cost()
    fig_tornado()
    fig_heatmap()
    fig_histogram()

    print(f"\nDone. All figures saved to {FIG_DIR}")
