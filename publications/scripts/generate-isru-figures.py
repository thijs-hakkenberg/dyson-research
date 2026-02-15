#!/usr/bin/env python3
"""
Generate publication-quality figures for the ISRU Economic Crossover paper.

Implements Equations 1-9 (plus NPV extensions) from the paper and produces
6 PDF figures:
  1. fig-cumulative-cost.pdf  — Earth vs ISRU cumulative cost curves
  2. fig-unit-cost.pdf        — Per-unit cost with launch cost floor
  3. fig-tornado.pdf          — Tornado chart of parameter sensitivities (NPV)
  4. fig-heatmap.pdf          — 2D heatmap: launch cost vs ISRU capital → crossover
  5. fig-histogram.pdf        — Monte Carlo histogram of crossover points (NPV)
  6. fig-npv-comparison.pdf   — Cumulative cost at multiple discount rates

Version D: Addresses Version C peer review (D1: integrated ramp-up in production
schedule, D2: Spearman diagnostics, D3: phased capital deployment, D4: censoring-
aware MC reporting, D5: mass penalty factor alpha, D6: transport cost).

Usage:
    source publications/scripts/.venv/bin/activate
    python publications/scripts/generate-isru-figures.py
"""

import os
import numpy as np
from scipy import stats as sp_stats
# brentq no longer needed — unit_to_time uses closed-form inverse
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
    "C_floor": 0.5e6,       # ISRU ops cost floor ($)
    "r": 0.05,              # discount rate (real)
    "b_L": None,            # launch learning exponent (None = no learning)
    "p_fuel": 200,          # fuel component of launch cost ($/kg)
    "p_ops_launch": 800,    # ops component of launch cost ($/kg)
    "alpha": 1.0,           # D5: mass penalty factor for ISRU units
    "p_transport": 100,     # D6: ISRU-to-orbit transport cost ($/kg)
}


# ---------------------------------------------------------------------------
# Cost model (Equations 1-9 plus NPV extensions)
# ---------------------------------------------------------------------------

def learning_exponent(lr):
    """Wright learning curve exponent: b = ln(LR) / ln(2)."""
    return np.log(lr) / np.log(2)


def s_curve(t, t0, k=2.0):
    """Logistic ramp-up function S(t) = 1 / (1 + exp(-k*(t - t0)))."""
    return 1.0 / (1.0 + np.exp(-k * (t - t0)))


def _cumulative_production(t, prod_rate, t0, k):
    """Cumulative production N(t) by integrating ṅ(t) = prod_rate * S(t).

    D1: The integral of the logistic S(t) has closed form:
      N(t) = (prod_rate / k) * [ln(1 + exp(k*(t - t0))) - ln(2)]

    This accounts for the S-curve ramp-up in the production *rate*, not
    just as a cost penalty. Early production is slower, so early units
    are produced later than the old linear schedule assumed.
    """
    t = np.asarray(t, dtype=float)
    # Use log-sum-exp trick for numerical stability
    arg = k * (t - t0)
    # ln(1 + exp(x)) = x + ln(1 + exp(-x)) for large x (avoids overflow)
    log1pexp = np.where(arg > 20, arg, np.log1p(np.exp(arg)))
    return (prod_rate / k) * (log1pexp - np.log(2))


def unit_to_time(n, prod_rate=500, t0=5, k=2.0):
    """D1: Map unit number to calendar time by inverting N(t).

    Closed-form inverse of N(t) = (prod_rate/k) * [ln(1+exp(k*(t-t0))) - ln(2)]:
      t(n) = t0 + (1/k) * ln(2*exp(n*k/prod_rate) - 1)

    For large n*k/prod_rate (>30), uses asymptotic form to avoid overflow:
      t(n) ~ t0 + n/prod_rate + ln(2)/k

    Fully vectorized — no per-element root finding.
    """
    n = np.asarray(n, dtype=float)
    x = n * k / prod_rate  # dimensionless argument

    # Exact formula: t = t0 + (1/k) * ln(2*exp(x) - 1)
    # For large x: ln(2*exp(x) - 1) ~ x + ln(2), avoiding overflow
    result = np.where(
        x < 30,
        t0 + (1.0 / k) * np.log(np.maximum(2.0 * np.exp(x) - 1.0, 1e-300)),
        t0 + n / prod_rate + np.log(2.0) / k,
    )
    return result


def earth_unit_cost(n, params):
    """Eq 2-4: Earth per-unit cost = manufacturing learning + launch."""
    n = np.asarray(n, dtype=float)
    b_E = learning_exponent(params["LR_E"])
    c_mfg = params["C_mfg1"] * n ** b_E

    # Launch cost: optionally with learning on ops component
    b_L = params.get("b_L", None)
    if b_L is not None:
        p_fuel = params.get("p_fuel", 200)
        p_ops = params.get("p_ops_launch", 800)
        c_launch = params["m"] * (p_fuel + p_ops * n ** b_L)
    else:
        c_launch = params["m"] * params["p_launch"]

    return c_mfg + c_launch


def earth_unit_cost_launch_learning(n, params):
    """Launch cost with two-component learning model.

    C_L(n) = m * [p_fuel + p_ops * n^b_L]
    where b_L = ln(LR_L) / ln(2), and only the ops component learns.
    """
    n = np.asarray(n, dtype=float)
    p_fuel = params.get("p_fuel", 200)
    p_ops = params.get("p_ops_launch", 800)
    lr_launch = params.get("LR_launch", 0.97)
    b_L = learning_exponent(lr_launch)
    return params["m"] * (p_fuel + p_ops * n ** b_L)


def isru_ops_cost(n, params):
    """D1/D5/D6: Operational cost only (no amortized capital).

    D1: Ramp-up effect is now purely through production schedule timing
    (unit_to_time integrates S(t)), so the 1/S(t) penalty is removed.
    D5: Mass penalty alpha multiplies ops cost.
    D6: Transport cost added as m * p_transport * alpha.
    """
    n = np.asarray(n, dtype=float)
    b_I = learning_exponent(params["LR_I"])
    alpha = params.get("alpha", 1.0)
    C_floor = params.get("C_floor", 0)

    # Learning curve ops cost (no S-curve penalty — D1)
    c_ops = alpha * (C_floor + (params["C_ops1"] - C_floor) * n ** b_I)

    # D6: Transport cost
    p_transport = params.get("p_transport", 0)
    if p_transport > 0:
        c_transport = params["m"] * p_transport * alpha
        c_ops = c_ops + c_transport

    return c_ops


def isru_unit_cost(n, params):
    """ISRU per-unit cost = amortized capital + ops (for display)."""
    c_capital = params["K"] / params["N_total"]
    return c_capital + isru_ops_cost(n, params)


def cumulative_cost(unit_cost_fn, N_max, params):
    """Compute cumulative cost for units 1..N_max."""
    ns = np.arange(1, N_max + 1, dtype=float)
    unit_costs = unit_cost_fn(ns, params)
    cum = np.cumsum(unit_costs)
    return ns, unit_costs, cum


def cumulative_isru(N_max, params):
    """Eq 9: ISRU cumulative = K + sum of ops costs."""
    ns = np.arange(1, N_max + 1, dtype=float)
    ops_costs = isru_ops_cost(ns, params)
    cum = params["K"] + np.cumsum(ops_costs)
    # Per-unit costs include amortized capital (for display)
    unit_costs = params["K"] / params["N_total"] + ops_costs
    return ns, unit_costs, cum


def find_crossover(params, N_max=20000):
    """Find smallest N where ISRU cumulative <= Earth cumulative (undiscounted)."""
    ns = np.arange(1, N_max + 1, dtype=float)
    # Earth cumulative
    earth_units = earth_unit_cost(ns, params)
    earth_cum = np.cumsum(earth_units)
    # ISRU cumulative
    ops = isru_ops_cost(ns, params)
    isru_cum = params["K"] + np.cumsum(ops)
    # Find crossover
    diff = isru_cum - earth_cum
    crossings = np.where(diff <= 0)[0]
    if len(crossings) > 0:
        return int(ns[crossings[0]])
    return N_max  # no crossover found


def find_crossover_npv(params, N_max=20000):
    """Find smallest N where discounted ISRU cumulative <= discounted Earth cumulative.

    NPV formulation:
      Sigma_E^NPV(N) = sum_{n=1}^{N} C_E(n) / (1+r)^{t_n}
      Sigma_I^NPV(N) = K + sum_{n=1}^{N} C_ops(n) / (1+r)^{t_n}
    Capital K is incurred at t=0 (no discount).
    """
    r = params.get("r", 0.0)
    if r == 0:
        return find_crossover(params, N_max)

    ns = np.arange(1, N_max + 1, dtype=float)
    k_ramp = params.get("k_ramp", 2.0)
    t_n = unit_to_time(ns, params.get("prod_rate", 500), params["t0"], k_ramp)
    discount = (1.0 + r) ** (-t_n)

    # Earth discounted cumulative
    earth_units = earth_unit_cost(ns, params)
    earth_cum_npv = np.cumsum(earth_units * discount)

    # ISRU discounted cumulative (K at t=0, no discount)
    ops = isru_ops_cost(ns, params)
    isru_cum_npv = params["K"] + np.cumsum(ops * discount)

    # Find crossover
    diff = isru_cum_npv - earth_cum_npv
    crossings = np.where(diff <= 0)[0]
    if len(crossings) > 0:
        return int(ns[crossings[0]])
    return N_max


def find_crossover_npv_phased(params, N_max=20000, K_years=5):
    """D3: NPV crossover with phased capital deployment.

    Instead of lump-sum K at t=0, spread K linearly over K_years annual
    tranches, each discounted:
      K_eff = sum_{y=0}^{K_years-1} (K/K_years) / (1+r)^y
    """
    r = params.get("r", 0.0)
    K = params["K"]
    tranche = K / K_years

    if r == 0:
        # Phased capital at r=0 is identical to lump sum
        return find_crossover(params, N_max)

    # Discounted capital
    K_eff = sum(tranche / (1.0 + r) ** y for y in range(K_years))

    ns = np.arange(1, N_max + 1, dtype=float)
    k_ramp = params.get("k_ramp", 2.0)
    t_n = unit_to_time(ns, params.get("prod_rate", 500), params["t0"], k_ramp)
    discount = (1.0 + r) ** (-t_n)

    earth_units = earth_unit_cost(ns, params)
    earth_cum_npv = np.cumsum(earth_units * discount)

    ops = isru_ops_cost(ns, params)
    isru_cum_npv = K_eff + np.cumsum(ops * discount)

    diff = isru_cum_npv - earth_cum_npv
    crossings = np.where(diff <= 0)[0]
    if len(crossings) > 0:
        return int(ns[crossings[0]])
    return N_max


def cumulative_npv(N_max, params):
    """Compute discounted cumulative costs for both pathways."""
    r = params.get("r", 0.0)
    ns = np.arange(1, N_max + 1, dtype=float)
    k_ramp = params.get("k_ramp", 2.0)
    t_n = unit_to_time(ns, params.get("prod_rate", 500), params["t0"], k_ramp)
    discount = (1.0 + r) ** (-t_n) if r > 0 else np.ones_like(t_n)

    earth_units = earth_unit_cost(ns, params)
    earth_cum = np.cumsum(earth_units * discount)

    ops = isru_ops_cost(ns, params)
    isru_cum = params["K"] + np.cumsum(ops * discount)

    return ns, earth_cum, isru_cum


# ---------------------------------------------------------------------------
# Figure 1: Cumulative Cost Comparison (undiscounted baseline)
# ---------------------------------------------------------------------------
def fig_cumulative_cost():
    p = BASELINE.copy()
    p["r"] = 0.0  # undiscounted for this figure
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
    print(f"  [1/6] fig-cumulative-cost.pdf  (crossover at ~{cross_n:,} units)")


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
    print("  [2/6] fig-unit-cost.pdf")


# ---------------------------------------------------------------------------
# Figure 3: Tornado Diagram (NPV-based sensitivity)
# ---------------------------------------------------------------------------
def fig_tornado():
    base_cross = find_crossover_npv(BASELINE)

    # Parameter variations: includes D5 (alpha) and D6 (p_transport)
    variations = [
        ("Earth LR $\\pm$0.05", "LR_E", -0.05, +0.05),
        ("ISRU capital $\\pm$\\$25B", "K", -25e9, +25e9),
        ("Discount rate $\\pm$3%", "r", -0.03, +0.03),
        ("ISRU ops cost $\\pm$\\$3M", "C_ops1", -3e6, +3e6),
        ("Earth mfg cost $\\pm$\\$25M", "C_mfg1", -25e6, +25e6),
        ("ISRU LR $\\pm$0.05", "LR_I", -0.05, +0.05),
        ("Launch cost $\\pm$\\$500/kg", "p_launch", -500, +500),
        ("Mass penalty $\\alpha$ $\\pm$0.5", "alpha", -0.0, +1.0),  # range 1.0-2.0
        ("Transport $\\pm$\\$100/kg", "p_transport", -100, +100),  # range 0-200
    ]

    labels = []
    low_deltas = []
    high_deltas = []

    for label, param, delta_lo, delta_hi in variations:
        p_lo = BASELINE.copy()
        p_lo[param] = BASELINE[param] + delta_lo
        # Ensure discount rate doesn't go negative
        if param == "r":
            p_lo[param] = max(0, p_lo[param])
        # Ensure alpha doesn't go below 1.0
        if param == "alpha":
            p_lo[param] = max(1.0, p_lo[param])
        # Ensure transport doesn't go negative
        if param == "p_transport":
            p_lo[param] = max(0, p_lo[param])
        cross_lo = find_crossover_npv(p_lo)

        p_hi = BASELINE.copy()
        p_hi[param] = BASELINE[param] + delta_hi
        cross_hi = find_crossover_npv(p_hi)

        labels.append(label)
        low_deltas.append(cross_lo - base_cross)
        high_deltas.append(cross_hi - base_cross)

    # Sort by total range (most sensitive first)
    ranges = [abs(h - l) for h, l in zip(high_deltas, low_deltas)]
    order = np.argsort(ranges)[::-1]
    labels = [labels[i] for i in order]
    low_deltas = [low_deltas[i] for i in order]
    high_deltas = [high_deltas[i] for i in order]

    fig, ax = plt.subplots(figsize=(6, 4.5))
    y_pos = np.arange(len(labels))

    for i, (lo, hi) in enumerate(zip(low_deltas, high_deltas)):
        ax.barh(i, lo, height=0.6, left=0, color=C_ISRU, alpha=0.85,
                edgecolor="white", linewidth=0.5)
        ax.barh(i, hi, height=0.6, left=0, color=C_EARTH, alpha=0.85,
                edgecolor="white", linewidth=0.5)
        for val in [lo, hi]:
            if val != 0:
                ha = "right" if val < 0 else "left"
                offset = -50 if val < 0 else 50
                ax.text(val + offset, i, f"{val:+,.0f}",
                        va="center", ha=ha, fontsize=7)

    ax.axvline(0, color="black", linewidth=0.8)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels)
    ax.set_xlabel(f"Change in NPV Crossover from Baseline ({base_cross:,} units, r=5%)")
    ax.invert_yaxis()

    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=C_ISRU, alpha=0.85, label="Earlier crossover"),
        Patch(facecolor=C_EARTH, alpha=0.85, label="Later crossover"),
    ]
    ax.legend(handles=legend_elements, loc="lower right", fontsize=8, framealpha=0.9)

    fig.savefig(os.path.join(FIG_DIR, "fig-tornado.pdf"))
    plt.close(fig)
    print(f"  [3/6] fig-tornado.pdf  (NPV baseline={base_cross:,}, r=5%)")


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
            crossover_grid[i, j] = find_crossover_npv(p)

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

    fig.colorbar(im, ax=ax, label="NPV Crossover Point (units)")

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
    print("  [4/6] fig-heatmap.pdf")


# ---------------------------------------------------------------------------
# Figure 5: Monte Carlo Histogram (NPV, 10k runs, correlated sampling)
# ---------------------------------------------------------------------------
def fig_histogram():
    rng = np.random.default_rng(42)
    n_runs = 10000
    N_MAX_MC = 40000

    # --- Correlated sampling for p_launch and K (rho=0.3) ---
    rho = 0.3
    cov_matrix = np.array([[1.0, rho], [rho, 1.0]])
    # Generate correlated normal samples via Cholesky
    L = np.linalg.cholesky(cov_matrix)
    z = rng.standard_normal((n_runs, 2))
    corr_normals = z @ L.T
    # Transform to uniform via CDF (Gaussian copula)
    from scipy.stats import norm as sp_norm
    u_launch = sp_norm.cdf(corr_normals[:, 0])
    u_capital = sp_norm.cdf(corr_normals[:, 1])
    # Map to target ranges
    p_launch_samples = 500 + u_launch * (2000 - 500)
    K_samples = 30e9 + u_capital * (100e9 - 30e9)

    # --- Independent samples for remaining params ---
    LR_E_samples = np.clip(rng.normal(0.85, 0.03, n_runs), 0.75, 0.95)
    LR_I_samples = np.clip(rng.normal(0.90, 0.03, n_runs), 0.80, 0.98)
    t0_samples = rng.uniform(3, 8, n_runs)
    C_ops1_samples = rng.uniform(2e6, 10e6, n_runs)
    C_mfg1_samples = rng.uniform(50e6, 100e6, n_runs)
    r_samples = rng.uniform(0.0, 0.10, n_runs)
    # D5: mass penalty alpha
    alpha_samples = rng.uniform(1.0, 2.0, n_runs)
    # D6: transport cost
    p_transport_samples = rng.uniform(50, 300, n_runs)

    # --- Run MC ---
    crossovers = np.empty(n_runs, dtype=float)
    for i in range(n_runs):
        p = BASELINE.copy()
        p["p_launch"] = p_launch_samples[i]
        p["K"] = K_samples[i]
        p["LR_E"] = LR_E_samples[i]
        p["LR_I"] = LR_I_samples[i]
        p["t0"] = t0_samples[i]
        p["C_ops1"] = C_ops1_samples[i]
        p["C_mfg1"] = C_mfg1_samples[i]
        p["r"] = r_samples[i]
        p["alpha"] = alpha_samples[i]
        p["p_transport"] = p_transport_samples[i]
        crossovers[i] = find_crossover_npv(p, N_max=N_MAX_MC)

    # --- D4: Censoring-aware reporting ---
    converged_mask = crossovers < N_MAX_MC
    n_converged = np.sum(converged_mask)
    convergence_rate = n_converged / n_runs * 100
    non_convergence_rate = 100 - convergence_rate

    # P(N* < H) for multiple horizons
    horizons = [5000, 10000, 20000, 40000]
    p_below_h = {h: np.mean(crossovers < h) * 100 for h in horizons}

    # Unconditional statistics (censored at N_MAX_MC)
    median = np.median(crossovers)
    q25, q75 = np.percentile(crossovers, [25, 75])
    p10, p90 = np.percentile(crossovers, [10, 90])

    # Conditional statistics (converging runs only)
    if n_converged > 0:
        cond_crossovers = crossovers[converged_mask]
        cond_median = np.median(cond_crossovers)
        cond_q25, cond_q75 = np.percentile(cond_crossovers, [25, 75])
        cond_p10, cond_p90 = np.percentile(cond_crossovers, [10, 90])
    else:
        cond_median = cond_q25 = cond_q75 = cond_p10 = cond_p90 = N_MAX_MC

    # --- Bootstrap confidence intervals (5,000 resamples) ---
    n_boot = 5000
    boot_medians = np.empty(n_boot)
    boot_cond_medians = np.empty(n_boot)
    boot_p10 = np.empty(n_boot)
    boot_p90 = np.empty(n_boot)
    for b in range(n_boot):
        boot_sample = rng.choice(crossovers, size=n_runs, replace=True)
        boot_medians[b] = np.median(boot_sample)
        boot_p10[b] = np.percentile(boot_sample, 10)
        boot_p90[b] = np.percentile(boot_sample, 90)
        boot_conv = boot_sample[boot_sample < N_MAX_MC]
        boot_cond_medians[b] = np.median(boot_conv) if len(boot_conv) > 0 else N_MAX_MC

    ci_median = np.percentile(boot_medians, [2.5, 97.5])
    ci_cond_median = np.percentile(boot_cond_medians, [2.5, 97.5])
    ci_p10 = np.percentile(boot_p10, [2.5, 97.5])
    ci_p90 = np.percentile(boot_p90, [2.5, 97.5])

    # --- Spearman rank correlations (unconditional) ---
    param_arrays = {
        "p_launch": p_launch_samples,
        "K": K_samples,
        "LR_E": LR_E_samples,
        "LR_I": LR_I_samples,
        "C_ops1": C_ops1_samples,
        "C_mfg1": C_mfg1_samples,
        "r": r_samples,
        "t0": t0_samples,
        "alpha": alpha_samples,
        "p_transport": p_transport_samples,
    }
    spearman_results = {}
    for name, arr in param_arrays.items():
        corr, pval = sp_stats.spearmanr(arr, crossovers)
        spearman_results[name] = (corr, pval)

    # D4: Conditional Spearman (converging runs only)
    spearman_conditional = {}
    if n_converged > 100:
        for name, arr in param_arrays.items():
            corr, pval = sp_stats.spearmanr(arr[converged_mask], cond_crossovers)
            spearman_conditional[name] = (corr, pval)

    # --- D2: Uncorrelated MC diagnostic for p_launch Spearman ---
    rng2 = np.random.default_rng(99)
    n_diag = 5000
    # Independent sampling (no copula)
    p_launch_uncorr = rng2.uniform(500, 2000, n_diag)
    K_uncorr = rng2.uniform(30e9, 100e9, n_diag)
    crossovers_uncorr = np.empty(n_diag, dtype=float)
    for i in range(n_diag):
        p = BASELINE.copy()
        p["p_launch"] = p_launch_uncorr[i]
        p["K"] = K_uncorr[i]
        p["LR_E"] = np.clip(rng2.normal(0.85, 0.03), 0.75, 0.95)
        p["LR_I"] = np.clip(rng2.normal(0.90, 0.03), 0.80, 0.98)
        p["t0"] = rng2.uniform(3, 8)
        p["C_ops1"] = rng2.uniform(2e6, 10e6)
        p["C_mfg1"] = rng2.uniform(50e6, 100e6)
        p["r"] = rng2.uniform(0.0, 0.10)
        p["alpha"] = rng2.uniform(1.0, 2.0)
        p["p_transport"] = rng2.uniform(50, 300)
        crossovers_uncorr[i] = find_crossover_npv(p, N_max=N_MAX_MC)

    spearman_uncorr_launch, _ = sp_stats.spearmanr(p_launch_uncorr, crossovers_uncorr)

    # D2: Monotonicity sanity check — sweep p_launch at baseline
    mono_launches = np.linspace(500, 2000, 10)
    mono_crossovers = []
    for pl in mono_launches:
        p = BASELINE.copy()
        p["p_launch"] = pl
        mono_crossovers.append(find_crossover_npv(p))
    mono_crossovers = np.array(mono_crossovers)
    mono_decreasing = all(mono_crossovers[i] >= mono_crossovers[i+1]
                          for i in range(len(mono_crossovers)-1))

    # --- Plot histogram ---
    fig, ax = plt.subplots()

    # Only plot converging scenarios in histogram; note non-convergence
    plot_data = crossovers[converged_mask] if n_converged > 0 else crossovers
    ax.hist(
        plot_data, bins=60, color=C_ISRU, alpha=0.75,
        edgecolor="white", linewidth=0.5,
    )

    # Conditional median line with bootstrap CI
    ax.axvline(cond_median, color=C_CROSS, linewidth=2, linestyle="-",
               label=f"Cond. median: {int(cond_median):,} "
                     f"[{int(ci_cond_median[0]):,}\u2013{int(ci_cond_median[1]):,}]")
    # IQR shaded (conditional)
    ax.axvspan(cond_q25, cond_q75, alpha=0.12, color=C_EARTH,
               label=f"Cond. IQR: [{int(cond_q25):,}, {int(cond_q75):,}]")
    # P10/P90 (conditional)
    ax.axvline(cond_p10, color="#6b7280", linewidth=1.5, linestyle=":",
               alpha=0.7, label=f"P10: {int(cond_p10):,}")
    ax.axvline(cond_p90, color=C_FLOOR, linewidth=1.5, linestyle=":",
               alpha=0.7, label=f"P90: {int(cond_p90):,}")

    # D4: Note non-convergence in legend
    from matplotlib.patches import Patch
    nc_patch = Patch(facecolor='none', edgecolor='none',
                     label=f"{non_convergence_rate:.1f}% did not converge (N>{N_MAX_MC:,})")
    handles, _ = ax.get_legend_handles_labels()
    handles.append(nc_patch)

    ax.set_xlabel("NPV Crossover Point $N^*$ (units)")
    ax.set_ylabel("Frequency")
    ax.legend(handles=handles, loc="upper right", framealpha=0.9, fontsize=7)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x):,}"))

    fig.savefig(os.path.join(FIG_DIR, "fig-histogram.pdf"))
    plt.close(fig)

    # --- Print diagnostics ---
    print(f"  [5/6] fig-histogram.pdf  (n={n_runs:,})")
    print(f"         Convergence: {convergence_rate:.1f}% within {N_MAX_MC:,} units")
    print(f"         Unconditional: median={int(median):,}, "
          f"IQR=[{int(q25):,},{int(q75):,}], P10={int(p10):,}, P90={int(p90):,}")
    print(f"         Conditional:   median={int(cond_median):,}, "
          f"IQR=[{int(cond_q25):,},{int(cond_q75):,}], "
          f"P10={int(cond_p10):,}, P90={int(cond_p90):,}")
    print(f"         Bootstrap 95% CIs: cond. median "
          f"[{int(ci_cond_median[0]):,}\u2013{int(ci_cond_median[1]):,}], "
          f"uncond. median [{int(ci_median[0]):,}\u2013{int(ci_median[1]):,}]")

    # D4: P(N* < H) table
    print("         P(N* < H) for multiple horizons:")
    for h in horizons:
        print(f"           H={h:>6,d}: P={p_below_h[h]:5.1f}%")

    # Spearman tables
    print("         Spearman rank correlations (unconditional, param -> N*):")
    for name in sorted(spearman_results.keys(), key=lambda k: -abs(spearman_results[k][0])):
        corr, pval = spearman_results[name]
        sig = "***" if pval < 0.001 else ("**" if pval < 0.01 else ("*" if pval < 0.05 else ""))
        print(f"           {name:>12s}: rho={corr:+.3f} {sig}")

    if spearman_conditional:
        print("         Spearman rank correlations (conditional on convergence):")
        for name in sorted(spearman_conditional.keys(),
                           key=lambda k: -abs(spearman_conditional[k][0])):
            corr, pval = spearman_conditional[name]
            sig = "***" if pval < 0.001 else ("**" if pval < 0.01 else ("*" if pval < 0.05 else ""))
            print(f"           {name:>12s}: rho={corr:+.3f} {sig}")

    # D2: Uncorrelated diagnostics
    print(f"\n         D2 Diagnostics:")
    print(f"           Uncorrelated p_launch Spearman: rho={spearman_uncorr_launch:+.3f}")
    print(f"           Correlated p_launch Spearman:   rho={spearman_results['p_launch'][0]:+.3f}")
    print(f"           Monotonicity check (p_launch sweep): "
          f"{'PASS - N* decreases as p_launch increases' if mono_decreasing else 'FAIL'}")
    if not mono_decreasing:
        print(f"           Sweep values: {list(zip(mono_launches.astype(int), mono_crossovers.astype(int)))}")

    return {
        "crossovers": crossovers,
        "converged_mask": converged_mask,
        "convergence_rate": convergence_rate,
        "median": median, "q25": q25, "q75": q75, "p10": p10, "p90": p90,
        "cond_median": cond_median, "cond_q25": cond_q25, "cond_q75": cond_q75,
        "ci_median": ci_median, "ci_cond_median": ci_cond_median,
        "ci_p10": ci_p10, "ci_p90": ci_p90,
        "spearman": spearman_results,
        "spearman_conditional": spearman_conditional,
        "p_below_h": p_below_h,
        "spearman_uncorr_launch": spearman_uncorr_launch,
        "mono_decreasing": mono_decreasing,
    }


# ---------------------------------------------------------------------------
# Figure 6: NPV Comparison at Multiple Discount Rates
# ---------------------------------------------------------------------------
def fig_npv_comparison():
    rates = [0.0, 0.03, 0.05, 0.10]
    rate_labels = ["0%", "3%", "5%", "10%"]
    colors_r = ["#6b7280", "#2563eb", "#16a34a", "#dc2626"]
    linestyles_r = ["-", "--", "-.", ":"]

    N_max = 12000

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))

    # Left panel: cumulative cost curves at different rates
    for rate, label, color, ls in zip(rates, rate_labels, colors_r, linestyles_r):
        p = BASELINE.copy()
        p["r"] = rate
        ns, earth_cum, isru_cum = cumulative_npv(N_max, p)

        ax1.plot(ns, earth_cum / 1e9, color=C_EARTH, linewidth=1.5,
                 linestyle=ls, alpha=0.7)
        ax1.plot(ns, isru_cum / 1e9, color=C_ISRU, linewidth=1.5,
                 linestyle=ls, alpha=0.7)

        # Mark crossover
        cross_n = find_crossover_npv(p, N_max)
        if cross_n < N_max:
            cross_val = np.interp(cross_n, ns, earth_cum)
            ax1.plot(cross_n, cross_val / 1e9, "o", color=color,
                     markersize=7, zorder=5)
            ax1.annotate(f"r={label}\nN*={cross_n:,}",
                         xy=(cross_n, cross_val / 1e9),
                         xytext=(cross_n + 400, cross_val / 1e9 + 15),
                         fontsize=7, color=color,
                         arrowprops=dict(arrowstyle="->", color=color, lw=0.8))

    ax1.set_xlabel("Production Volume (units)")
    ax1.set_ylabel("Discounted Cumulative Cost (\\$B)")
    ax1.set_xlim(0, N_max)
    ax1.set_ylim(0, None)
    ax1.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x):,}"))

    # Custom legend for pathways and rates
    from matplotlib.lines import Line2D
    legend1 = [
        Line2D([0], [0], color=C_EARTH, linewidth=2, label="Earth launch"),
        Line2D([0], [0], color=C_ISRU, linewidth=2, label="ISRU"),
    ]
    legend2 = [
        Line2D([0], [0], color="gray", linestyle=ls, linewidth=1, label=f"r={label}")
        for ls, label in zip(linestyles_r, rate_labels)
    ]
    leg1 = ax1.legend(handles=legend1, loc="upper left", fontsize=8, framealpha=0.9)
    ax1.add_artist(leg1)
    ax1.legend(handles=legend2, loc="center left", fontsize=7, framealpha=0.9)

    # Right panel: crossover as a function of discount rate (continuous)
    r_range = np.linspace(0, 0.12, 50)
    crossovers_r = []
    for rate in r_range:
        p = BASELINE.copy()
        p["r"] = rate
        crossovers_r.append(find_crossover_npv(p, N_max=20000))
    crossovers_r = np.array(crossovers_r)

    ax2.plot(r_range * 100, crossovers_r, color=C_ISRU, linewidth=2)
    ax2.fill_between(r_range * 100, crossovers_r, alpha=0.1, color=C_ISRU)

    # Mark key rates
    for rate, label, color in [(0.0, "0%", "#6b7280"), (0.05, "5%", "#16a34a"),
                                (0.10, "10%", "#dc2626")]:
        p = BASELINE.copy()
        p["r"] = rate
        cn = find_crossover_npv(p, N_max=20000)
        ax2.plot(rate * 100, cn, "o", color=color, markersize=8, zorder=5)
        ax2.annotate(f"{cn:,}", xy=(rate * 100, cn),
                     xytext=(rate * 100 + 0.5, cn + 300),
                     fontsize=8, color=color)

    ax2.set_xlabel("Real Discount Rate (%)")
    ax2.set_ylabel("NPV Crossover $N^*$ (units)")
    ax2.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:.0f}%"))
    ax2.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x):,}"))

    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "fig-npv-comparison.pdf"))
    plt.close(fig)

    # Print summary
    for rate, label in zip(rates, rate_labels):
        p = BASELINE.copy()
        p["r"] = rate
        cn = find_crossover_npv(p)
        print(f"  [6/6] NPV crossover at r={label}: ~{cn:,} units")


# ---------------------------------------------------------------------------
# Production schedule table (for LaTeX)
# ---------------------------------------------------------------------------
def print_production_schedule():
    """Print production schedule table showing n -> t(n) with integrated ramp-up."""
    milestones = [1, 10, 100, 500, 1000, 5000, 10000]
    k = BASELINE["k_ramp"]
    t0 = BASELINE["t0"]
    prod_rate = BASELINE["prod_rate"]

    print("\n  Production schedule (integrated S-curve, k=2.0, t0=5, prod_rate=500):")
    print(f"  {'n':>6s}  {'t(n) new':>10s}  {'t(n) old':>10s}  {'S(t)':>8s}  {'delay':>8s}")
    print(f"  {'------':>6s}  {'----------':>10s}  {'----------':>10s}  {'--------':>8s}  {'--------':>8s}")
    for n in milestones:
        t_new = unit_to_time(n, prod_rate, t0, k)
        t_old = t0 + n / prod_rate  # old Version C formula
        s = s_curve(float(t_new), t0, k)
        delay = t_new - t_old
        print(f"  {n:>6,d}  {t_new:>10.2f}  {t_old:>10.1f}  {s:>8.4f}  {delay:>+8.2f}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print(f"Generating figures in: {FIG_DIR}\n")

    # Diagnostic: print baseline and scenario crossovers
    base_undisc = find_crossover(BASELINE)
    base_npv = find_crossover_npv(BASELINE)
    print(f"Baseline crossover (undiscounted): ~{base_undisc:,} units")
    print(f"Baseline crossover (NPV, r=5%):   ~{base_npv:,} units")

    p_opt = BASELINE.copy()
    p_opt["p_launch"] = 500
    p_opt["K"] = 30e9
    print(f"Optimistic crossover (NPV):       ~{find_crossover_npv(p_opt):,} units")

    p_con = BASELINE.copy()
    p_con["p_launch"] = 2000
    p_con["K"] = 100e9
    print(f"Conservative crossover (NPV):     ~{find_crossover_npv(p_con):,} units")

    # Launch learning scenario
    p_ll = BASELINE.copy()
    p_ll["LR_launch"] = 0.97
    b_L = learning_exponent(0.97)
    p_ll["b_L"] = b_L
    cross_ll = find_crossover_npv(p_ll)
    print(f"Launch learning (LR=0.97, NPV):   ~{cross_ll:,} units "
          f"(shift: +{cross_ll - base_npv:,} from NPV baseline)")

    # D3: Phased capital comparison
    base_phased = find_crossover_npv_phased(BASELINE, K_years=5)
    print(f"Phased capital (5yr, NPV):        ~{base_phased:,} units "
          f"(shift: {base_phased - base_npv:,} from lump-sum)")

    # D5: Alpha sensitivity
    p_alpha = BASELINE.copy()
    p_alpha["alpha"] = 1.5
    cross_alpha = find_crossover_npv(p_alpha)
    print(f"Mass penalty alpha=1.5 (NPV):     ~{cross_alpha:,} units "
          f"(shift: +{cross_alpha - base_npv:,} from baseline)")

    # D6: Transport cost sensitivity
    p_notrans = BASELINE.copy()
    p_notrans["p_transport"] = 0
    cross_notrans = find_crossover_npv(p_notrans)
    print(f"No transport cost (NPV):          ~{cross_notrans:,} units "
          f"(shift: {cross_notrans - base_npv:,} from baseline)")
    print()

    fig_cumulative_cost()
    fig_unit_cost()
    fig_tornado()
    fig_heatmap()
    mc_results = fig_histogram()
    fig_npv_comparison()

    print_production_schedule()

    print(f"\nDone. All figures saved to {FIG_DIR}")
