#!/usr/bin/env python3
"""
Generate publication-quality figures for the ISRU Economic Crossover paper.

Imports model logic from isru_model and MC engine from isru_mc, then produces
6 PDF figures:
  1. fig-cumulative-cost.pdf  — Earth vs ISRU cumulative cost curves
  2. fig-unit-cost.pdf        — Per-unit cost with launch cost floor
  3. fig-tornado.pdf          — Tornado chart of parameter sensitivities (NPV)
  4. fig-heatmap.pdf          — 2D heatmap: launch cost vs ISRU capital → crossover
  5. fig-histogram.pdf        — Monte Carlo histogram of crossover points (NPV)
  6. fig-npv-comparison.pdf   — Cumulative cost at multiple discount rates

Version E: Addresses Version D peer review (E1: pathway-specific delivery schedules,
E2: discount rate removed from MC stochastic params, E3: ISRU learning curve
empirical basis + no-learning/slow-learning scenarios, E4: survival-analysis-style
reporting, E5: distribution sensitivity test, E6: Table 5 verification,
E7: softened generality claims).

Usage:
    source publications/scripts/.venv/bin/activate
    python publications/scripts/generate_isru_figures.py
"""

from __future__ import annotations

from os.path import dirname, abspath, join
from os import makedirs

from numpy import (
    arange, argsort, array, clip, empty, interp,
    linspace, median, percentile, sum, zeros,
)
from numpy.random import default_rng
from matplotlib import use as mpl_use
mpl_use("Agg")
from matplotlib.pyplot import subplots, close, rcParams  # noqa: E402
from matplotlib.ticker import FuncFormatter  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from scipy.stats import spearmanr, triang  # noqa: E402

from isru_model import (  # noqa: E402
    BASELINE,
    clamp_param,
    cumulative_cost,
    cumulative_isru,
    cumulative_npv,
    earth_delivery_time,
    earth_unit_cost,
    find_crossover,
    find_crossover_npv,
    find_crossover_npv_phased,
    isru_ops_cost,
    isru_unit_cost,
    learning_exponent,
    s_curve,
    unit_to_time,
    _cumulative_production,
)
from isru_mc import run_mc  # noqa: E402

# ---------------------------------------------------------------------------
# Output directory
# ---------------------------------------------------------------------------
script_dir = dirname(abspath(__file__))
fig_dir = join(script_dir, "..", "drafts", "figures")
makedirs(fig_dir, exist_ok=True)

# ---------------------------------------------------------------------------
# Publication style
# ---------------------------------------------------------------------------
rcParams.update({
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
c_earth = "#d97706"     # amber
c_isru = "#0891b2"      # cyan
c_cross = "#16a34a"     # green
c_floor = "#dc2626"     # red for launch cost floor


# ---------------------------------------------------------------------------
# Figure 1: Cumulative Cost Comparison (undiscounted baseline)
# ---------------------------------------------------------------------------
def fig_cumulative_cost():
    p = BASELINE.copy()
    p["r"] = 0.0  # undiscounted for this figure
    cross_n = find_crossover(p)
    n_max = max(cross_n * 2 + 500, 8000)
    ns_e, _, cum_e = cumulative_cost(earth_unit_cost, n_max, p)
    ns_i, _, cum_i = cumulative_isru(n_max, p)

    cross_val = interp(cross_n, ns_e, cum_e)

    fig, ax = subplots()
    ax.plot(ns_e, cum_e / 1e9, color=c_earth, linewidth=2, label="Earth launch")
    ax.plot(ns_i, cum_i / 1e9, color=c_isru, linewidth=2, label="ISRU")

    ax.axvline(cross_n, color=c_cross, linestyle="--", linewidth=1, alpha=0.7)
    ax.plot(cross_n, cross_val / 1e9, "o", color=c_cross, markersize=8, zorder=5)

    txt_x = cross_n + n_max * 0.08
    txt_y = cross_val / 1e9 * 1.15
    ax.annotate(
        f"Crossover\n~{cross_n:,} units",
        xy=(cross_n, cross_val / 1e9),
        xytext=(txt_x, txt_y),
        fontsize=9,
        color=c_cross,
        fontweight="bold",
        arrowprops=dict(arrowstyle="->", color=c_cross, lw=1.2),
    )

    ax.fill_between(
        ns_e[cross_n - 1:], cum_e[cross_n - 1:] / 1e9, cum_i[cross_n - 1:] / 1e9,
        alpha=0.10, color=c_cross, label="ISRU savings",
    )

    ax.set_xlabel("Production Volume (units)")
    ax.set_ylabel("Cumulative Cost (\\$B)")
    ax.set_xlim(0, n_max)
    ax.set_ylim(0, None)
    ax.legend(loc="upper left", framealpha=0.9)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x):,}"))

    fig.savefig(join(fig_dir, "fig-cumulative-cost.pdf"))
    close(fig)
    print(f"  [1/6] fig-cumulative-cost.pdf  (crossover at ~{cross_n:,} units)")


# ---------------------------------------------------------------------------
# Figure 2: Per-Unit Cost Comparison
# ---------------------------------------------------------------------------
def fig_unit_cost():
    p = BASELINE.copy()
    cross_n = find_crossover(p)
    n_max = max(cross_n * 2 + 500, 8000)
    ns = arange(1, n_max + 1, dtype=float)

    earth_costs = earth_unit_cost(ns, p) / 1e6  # $M
    isru_costs = isru_unit_cost(ns, p) / 1e6

    launch_floor_val = p["m"] * p["p_launch"] / 1e6

    fig, ax = subplots()
    step = max(1, len(ns) // 800)
    ax.plot(ns[::step], earth_costs[::step], color=c_earth, linewidth=2, label="Earth launch")
    ax.plot(ns[::step], isru_costs[::step], color=c_isru, linewidth=2, label="ISRU")

    ax.axhline(launch_floor_val, color=c_floor, linestyle=":", linewidth=1.5, alpha=0.8)
    ax.annotate(
        f"Launch cost floor (\\${launch_floor_val:.2f}M/unit)",
        xy=(n_max * 0.55, launch_floor_val),
        xytext=(n_max * 0.55, launch_floor_val + 1.5),
        fontsize=8,
        color=c_floor,
    )

    y_max = max(earth_costs[0], 40)
    ax.set_xlabel("Cumulative Production (units)")
    ax.set_ylabel("Per-Unit Cost (\\$M)")
    ax.set_xlim(0, n_max)
    ax.set_ylim(0, y_max)
    ax.legend(loc="upper right", framealpha=0.9)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x):,}"))

    fig.savefig(join(fig_dir, "fig-unit-cost.pdf"))
    close(fig)
    print("  [2/6] fig-unit-cost.pdf")


# ---------------------------------------------------------------------------
# Figure 3: Tornado Diagram (NPV-based sensitivity)
# ---------------------------------------------------------------------------
def fig_tornado():
    base_cross = find_crossover_npv(BASELINE)

    variations = [
        ("Earth LR $\\pm$0.05", "LR_E", -0.05, +0.05),
        ("ISRU capital $\\pm$\\$25B", "K", -25e9, +25e9),
        ("Discount rate $\\pm$3%", "r", -0.03, +0.03),
        ("ISRU ops cost $\\pm$\\$3M", "C_ops1", -3e6, +3e6),
        ("Earth mfg cost $\\pm$\\$25M", "C_mfg1", -25e6, +25e6),
        ("ISRU LR $\\pm$0.05", "LR_I", -0.05, +0.05),
        ("Launch cost $\\pm$\\$500/kg", "p_launch", -500, +500),
        ("Mass penalty $\\alpha$ $\\pm$0.5", "alpha", -0.0, +1.0),
        ("Transport $\\pm$\\$100/kg", "p_transport", -100, +100),
    ]

    labels = []
    low_deltas = []
    high_deltas = []

    for label, param, delta_lo, delta_hi in variations:
        p_lo = BASELINE.copy()
        p_lo[param] = BASELINE[param] + delta_lo
        p_lo[param] = clamp_param(param, p_lo[param])
        cross_lo = find_crossover_npv(p_lo)

        p_hi = BASELINE.copy()
        p_hi[param] = BASELINE[param] + delta_hi
        cross_hi = find_crossover_npv(p_hi)

        labels.append(label)
        low_deltas.append(cross_lo - base_cross)
        high_deltas.append(cross_hi - base_cross)

    ranges = [abs(h - l) for h, l in zip(high_deltas, low_deltas)]
    order = argsort(ranges)[::-1]
    labels = [labels[i] for i in order]
    low_deltas = [low_deltas[i] for i in order]
    high_deltas = [high_deltas[i] for i in order]

    fig, ax = subplots(figsize=(6, 4.5))
    y_pos = arange(len(labels))

    for i, (lo, hi) in enumerate(zip(low_deltas, high_deltas)):
        ax.barh(i, lo, height=0.6, left=0, color=c_isru, alpha=0.85,
                edgecolor="white", linewidth=0.5)
        ax.barh(i, hi, height=0.6, left=0, color=c_earth, alpha=0.85,
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

    legend_elements = [
        Patch(facecolor=c_isru, alpha=0.85, label="Earlier crossover"),
        Patch(facecolor=c_earth, alpha=0.85, label="Later crossover"),
    ]
    ax.legend(handles=legend_elements, loc="lower right", fontsize=8, framealpha=0.9)

    fig.savefig(join(fig_dir, "fig-tornado.pdf"))
    close(fig)
    print(f"  [3/6] fig-tornado.pdf  (NPV baseline={base_cross:,}, r=5%)")


# ---------------------------------------------------------------------------
# Figure 4: 2D Heatmap — Launch Cost vs ISRU Capital → Crossover
# ---------------------------------------------------------------------------
def fig_heatmap():
    launch_costs = linspace(200, 2500, 60)
    isru_capitals = linspace(20e9, 120e9, 60)

    crossover_grid = zeros((len(isru_capitals), len(launch_costs)))

    for i, k_val in enumerate(isru_capitals):
        for j, pl in enumerate(launch_costs):
            p = BASELINE.copy()
            p["p_launch"] = pl
            p["K"] = k_val
            crossover_grid[i, j] = find_crossover_npv(p)

    fig, ax = subplots()
    im = ax.contourf(
        launch_costs,
        isru_capitals / 1e9,
        crossover_grid,
        levels=arange(0, 15001, 1000),
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

    ax.plot(
        BASELINE["p_launch"], BASELINE["K"] / 1e9,
        "k*", markersize=14, zorder=5, label="Baseline",
    )
    ax.legend(loc="upper left", fontsize=8, framealpha=0.9)

    ax.set_xlabel("Launch Cost (\\$/kg)")
    ax.set_ylabel("ISRU Capital Investment (\\$B)")

    fig.savefig(join(fig_dir, "fig-heatmap.pdf"))
    close(fig)
    print("  [4/6] fig-heatmap.pdf")


# ---------------------------------------------------------------------------
# Figure 5: Monte Carlo Histogram (NPV, 10k runs, correlated sampling)
# E2: Discount rate removed from stochastic params; MC run at fixed rates
# ---------------------------------------------------------------------------
def fig_histogram():
    """E2: Run MC at multiple fixed discount rates and generate per-rate histograms."""
    mc_rates = [0.03, 0.05, 0.08]
    all_results = {}

    for r_fixed in mc_rates:
        rng = default_rng(42)
        res = run_mc(r_fixed, rng)
        all_results[r_fixed] = res

    fig, axes = subplots(1, 3, figsize=(14, 4.5), sharey=True)

    for ax, r_fixed in zip(axes, mc_rates):
        res = all_results[r_fixed]
        converged_mask = res.converged_mask
        crossovers = res.crossovers
        n_converged = sum(converged_mask)

        plot_data = crossovers[converged_mask] if n_converged > 0 else crossovers
        ax.hist(plot_data, bins=50, color=c_isru, alpha=0.75,
                edgecolor="white", linewidth=0.5)

        ax.axvline(res.stats.cond_median, color=c_cross, linewidth=2, linestyle="-")
        ax.axvspan(res.stats.cond_q25, res.stats.cond_q75, alpha=0.12, color=c_earth)

        conv_pct = res.stats.convergence_rate
        cmed = int(res.stats.cond_median)
        r_pct = int(r_fixed * 100)
        ax.set_title(f"r = {r_pct}%\n"
                     f"Conv: {conv_pct:.1f}%, Med: {cmed:,}",
                     fontsize=9)
        ax.set_xlabel("$N^*$ (units)")
        ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x):,}"))

    axes[0].set_ylabel("Frequency")
    fig.tight_layout()
    fig.savefig(join(fig_dir, "fig-histogram.pdf"))
    close(fig)

    print_mc_diagnostics(all_results, mc_rates)
    print_copula_diagnostic(all_results[0.05])

    return all_results


def print_mc_diagnostics(all_results, mc_rates):
    """Print MC diagnostics for each discount rate."""
    for r_fixed in mc_rates:
        res = all_results[r_fixed]
        s = res.stats
        print(f"\n  [5/6] MC at r={r_fixed:.0%} (n=10,000):")
        print(f"         Convergence: {s.convergence_rate:.1f}% within {res.N_MAX_MC:,} units")
        print(f"         Unconditional: median={int(s.median):,}, "
              f"IQR=[{int(s.q25):,},{int(s.q75):,}], "
              f"P10={int(s.p10):,}, P90={int(s.p90):,}")
        print(f"         Conditional:   median={int(s.cond_median):,}, "
              f"IQR=[{int(s.cond_q25):,},{int(s.cond_q75):,}], "
              f"P10={int(s.cond_p10):,}, P90={int(s.cond_p90):,}")
        ci = s.ci_cond_median
        print(f"         Bootstrap 95% CI on cond. median: "
              f"[{int(ci[0]):,}\u2013{int(ci[1]):,}]")

        print("         P(N* \u2264 H) \u2014 survival-style:")
        for h in sorted(s.p_below_h.keys()):
            print(f"           H={h:>6,d}: P={s.p_below_h[h]:5.1f}%")

        print("         Spearman rank correlations (unconditional):")
        for sr in sorted(res.spearman, key=lambda x: -abs(x.rho)):
            print(f"           {sr.name:>12s}: rho={sr.rho:+.3f} {sr.stars}")

        if res.spearman_conditional:
            print("         Spearman rank correlations (conditional):")
            for sr in sorted(res.spearman_conditional, key=lambda x: -abs(x.rho)):
                print(f"           {sr.name:>12s}: rho={sr.rho:+.3f} {sr.stars}")

        ncp = res.non_convergence_profile
        if ncp.non_conv_drivers:
            print("         Non-convergence drivers (mean converging vs non-converging):")
            for name in sorted(ncp.non_conv_drivers.keys(),
                               key=lambda k: abs(ncp.non_conv_drivers[k][1] - ncp.non_conv_drivers[k][0]),
                               reverse=True)[:5]:
                mc, mnc = ncp.non_conv_drivers[name]
                print(f"           {name:>12s}: conv={mc:.4g}, non-conv={mnc:.4g}")
        if ncp.non_conv_by_K:
            print("         Non-convergence rate by K bucket:")
            for label, rate in ncp.non_conv_by_K.items():
                print(f"           K={label}: {rate:.1f}% non-converge")


def print_copula_diagnostic(res5):
    """Print copula diagnostic comparing correlated vs uncorrelated sampling."""
    rng2 = default_rng(99)
    n_diag = 5000
    p_launch_uncorr = rng2.uniform(500, 2000, n_diag)
    k_uncorr = rng2.uniform(30e9, 100e9, n_diag)
    crossovers_uncorr = empty(n_diag, dtype=float)
    for i in range(n_diag):
        p = BASELINE.copy()
        p["p_launch"] = p_launch_uncorr[i]
        p["K"] = k_uncorr[i]
        p["LR_E"] = clip(rng2.normal(0.85, 0.03), 0.75, 0.95)
        p["LR_I"] = clip(rng2.normal(0.90, 0.03), 0.80, 0.98)
        p["t0"] = rng2.uniform(3, 8)
        p["C_ops1"] = rng2.uniform(2e6, 10e6)
        p["C_mfg1"] = rng2.uniform(50e6, 100e6)
        p["r"] = 0.05
        p["alpha"] = rng2.uniform(1.0, 2.0)
        p["p_transport"] = rng2.uniform(50, 300)
        crossovers_uncorr[i] = find_crossover_npv(p, N_max=40000)
    spearman_uncorr_launch, _ = spearmanr(p_launch_uncorr, crossovers_uncorr)

    mono_launches = linspace(500, 2000, 10)
    mono_crossovers = []
    for pl in mono_launches:
        p = BASELINE.copy()
        p["p_launch"] = pl
        mono_crossovers.append(find_crossover_npv(p))
    mono_crossovers = array(mono_crossovers)
    mono_decreasing = all(mono_crossovers[i] >= mono_crossovers[i+1]
                          for i in range(len(mono_crossovers)-1))

    corr_rho = next(sr.rho for sr in res5.spearman if sr.name == "p_launch")

    print(f"\n         Copula diagnostics (at r=5%):")
    print(f"           Uncorrelated p_launch Spearman: rho={spearman_uncorr_launch:+.3f}")
    print(f"           Correlated p_launch Spearman:   rho={corr_rho:+.3f}")
    print(f"           Monotonicity check (p_launch sweep): "
          f"{'PASS' if mono_decreasing else 'FAIL'}")


# ---------------------------------------------------------------------------
# Figure 6: NPV Comparison at Multiple Discount Rates
# ---------------------------------------------------------------------------
def fig_npv_comparison():
    rates = [0.0, 0.03, 0.05, 0.10]
    rate_labels = ["0%", "3%", "5%", "10%"]
    colors_r = ["#6b7280", "#2563eb", "#16a34a", "#dc2626"]
    linestyles_r = ["-", "--", "-.", ":"]

    n_max = 12000

    fig, (ax1, ax2) = subplots(1, 2, figsize=(12, 4.5))

    for rate, label, color, ls in zip(rates, rate_labels, colors_r, linestyles_r):
        p = BASELINE.copy()
        p["r"] = rate
        ns, earth_cum, isru_cum = cumulative_npv(n_max, p)

        ax1.plot(ns, earth_cum / 1e9, color=c_earth, linewidth=1.5,
                 linestyle=ls, alpha=0.7)
        ax1.plot(ns, isru_cum / 1e9, color=c_isru, linewidth=1.5,
                 linestyle=ls, alpha=0.7)

        cross_n = find_crossover_npv(p, n_max)
        if cross_n < n_max:
            cross_val = interp(cross_n, ns, earth_cum)
            ax1.plot(cross_n, cross_val / 1e9, "o", color=color,
                     markersize=7, zorder=5)
            ax1.annotate(f"r={label}\nN*={cross_n:,}",
                         xy=(cross_n, cross_val / 1e9),
                         xytext=(cross_n + 400, cross_val / 1e9 + 15),
                         fontsize=7, color=color,
                         arrowprops=dict(arrowstyle="->", color=color, lw=0.8))

    ax1.set_xlabel("Production Volume (units)")
    ax1.set_ylabel("Discounted Cumulative Cost (\\$B)")
    ax1.set_xlim(0, n_max)
    ax1.set_ylim(0, None)
    ax1.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x):,}"))

    legend1 = [
        Line2D([0], [0], color=c_earth, linewidth=2, label="Earth launch"),
        Line2D([0], [0], color=c_isru, linewidth=2, label="ISRU"),
    ]
    legend2 = [
        Line2D([0], [0], color="gray", linestyle=ls, linewidth=1, label=f"r={label}")
        for ls, label in zip(linestyles_r, rate_labels)
    ]
    leg1 = ax1.legend(handles=legend1, loc="upper left", fontsize=8, framealpha=0.9)
    ax1.add_artist(leg1)
    ax1.legend(handles=legend2, loc="center left", fontsize=7, framealpha=0.9)

    r_range = linspace(0, 0.12, 50)
    crossovers_r = []
    for rate in r_range:
        p = BASELINE.copy()
        p["r"] = rate
        crossovers_r.append(find_crossover_npv(p, N_max=20000))
    crossovers_r = array(crossovers_r)

    ax2.plot(r_range * 100, crossovers_r, color=c_isru, linewidth=2)
    ax2.fill_between(r_range * 100, crossovers_r, alpha=0.1, color=c_isru)

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
    fig.savefig(join(fig_dir, "fig-npv-comparison.pdf"))
    close(fig)

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

    print("\n  Production schedule (E1: pathway-specific timing):")
    print(f"  {'n':>6s}  {'t_E(n)':>8s}  {'t_I(n)':>8s}  {'S(t)':>8s}  {'gap':>8s}")
    print(f"  {'------':>6s}  {'--------':>8s}  {'--------':>8s}  {'--------':>8s}  {'--------':>8s}")
    for n in milestones:
        t_earth = n / prod_rate
        t_isru = unit_to_time(n, prod_rate, t0, k)
        s = s_curve(float(t_isru), t0, k)
        gap = t_isru - t_earth
        print(f"  {n:>6,d}  {t_earth:>8.2f}  {t_isru:>8.2f}  {s:>8.4f}  {gap:>+8.2f}")


# ---------------------------------------------------------------------------
# E3: Learning rate scenario diagnostics
# ---------------------------------------------------------------------------
def print_learning_scenarios():
    """E3: Test no-learning and slow-learning ISRU scenarios."""
    base_npv = find_crossover_npv(BASELINE)

    scenarios = [
        ("Baseline (LR_I=0.90)", {"LR_I": 0.90}),
        ("Slow learning (LR_I=0.98)", {"LR_I": 0.98}),
        ("No learning (LR_I=1.00)", {"LR_I": 1.0}),
    ]

    print("\n  E3: ISRU learning rate scenarios (NPV, r=5%):")
    for label, overrides in scenarios:
        p = BASELINE.copy()
        p.update(overrides)
        cross = find_crossover_npv(p, N_max=40000)
        if cross >= 40000:
            print(f"    {label:40s}: N* > 40,000 (no crossover)")
        else:
            shift = cross - base_npv
            print(f"    {label:40s}: N* = {cross:,} (shift: {shift:+,})")


# ---------------------------------------------------------------------------
# E5: Distribution sensitivity test (uniform vs triangular)
# ---------------------------------------------------------------------------
def print_distribution_sensitivity():
    """E5: Compare uniform vs triangular distributions for K and p_launch."""
    rng = default_rng(42)
    n_runs = 5000
    n_max_mc = 40000

    uniform_crossovers = empty(n_runs)
    for i in range(n_runs):
        p = BASELINE.copy()
        p["p_launch"] = rng.uniform(500, 2000)
        p["K"] = rng.uniform(30e9, 100e9)
        p["LR_E"] = clip(rng.normal(0.85, 0.03), 0.75, 0.95)
        p["LR_I"] = clip(rng.normal(0.90, 0.03), 0.80, 0.98)
        p["t0"] = rng.uniform(3, 8)
        p["C_ops1"] = rng.uniform(2e6, 10e6)
        p["C_mfg1"] = rng.uniform(50e6, 100e6)
        p["r"] = 0.05
        p["alpha"] = rng.uniform(1.0, 2.0)
        p["p_transport"] = rng.uniform(50, 300)
        uniform_crossovers[i] = find_crossover_npv(p, N_max=n_max_mc)

    rng2 = default_rng(42)
    triang_crossovers = empty(n_runs)
    for i in range(n_runs):
        p = BASELINE.copy()
        c_launch = (1000 - 500) / (2000 - 500)
        p["p_launch"] = triang.rvs(c_launch, loc=500, scale=1500, random_state=rng2)
        c_k = (50e9 - 30e9) / (100e9 - 30e9)
        p["K"] = triang.rvs(c_k, loc=30e9, scale=70e9, random_state=rng2)
        p["LR_E"] = clip(rng2.normal(0.85, 0.03), 0.75, 0.95)
        p["LR_I"] = clip(rng2.normal(0.90, 0.03), 0.80, 0.98)
        p["t0"] = rng2.uniform(3, 8)
        p["C_ops1"] = rng2.uniform(2e6, 10e6)
        p["C_mfg1"] = rng2.uniform(50e6, 100e6)
        p["r"] = 0.05
        p["alpha"] = rng2.uniform(1.0, 2.0)
        p["p_transport"] = rng2.uniform(50, 300)
        triang_crossovers[i] = find_crossover_npv(p, N_max=n_max_mc)

    u_conv = uniform_crossovers[uniform_crossovers < n_max_mc]
    t_conv = triang_crossovers[triang_crossovers < n_max_mc]

    print("\n  E5: Distribution sensitivity (uniform vs triangular for K, p_launch):")
    print(f"    Uniform:     conv={len(u_conv)/n_runs*100:.1f}%, "
          f"cond. median={int(median(u_conv)):,}, "
          f"IQR=[{int(percentile(u_conv, 25)):,}, {int(percentile(u_conv, 75)):,}]")
    print(f"    Triangular:  conv={len(t_conv)/n_runs*100:.1f}%, "
          f"cond. median={int(median(t_conv)):,}, "
          f"IQR=[{int(percentile(t_conv, 25)):,}, {int(percentile(t_conv, 75)):,}]")
    shift = int(median(t_conv)) - int(median(u_conv))
    print(f"    Median shift: {shift:+,} units "
          f"({'meaningful' if abs(shift) > 500 else 'not meaningful'})")


# ---------------------------------------------------------------------------
# E6: Verify Table 5 cumulative economics
# ---------------------------------------------------------------------------
def print_cumulative_economics():
    """E6: Compute cumulative costs at year 5, 10, 15, 20 under baseline and print."""
    prod_rate = BASELINE["prod_rate"]
    t0 = BASELINE["t0"]
    k = BASELINE["k_ramp"]

    print("\n  E6: Cumulative economics verification (baseline, undiscounted):")
    print(f"  {'Year':>6s}  {'Units':>8s}  {'Earth ($B)':>12s}  {'ISRU ($B)':>12s}  {'Net ($B)':>10s}")
    print(f"  {'------':>6s}  {'--------':>8s}  {'------------':>12s}  {'------------':>12s}  {'----------':>10s}")

    for year in [5, 10, 15, 20]:
        n_produced = max(0, _cumulative_production(year, prod_rate, t0, k))
        n_produced = int(round(n_produced))
        if n_produced < 1:
            print(f"  {year:>6d}  {0:>8d}  {'---':>12s}  {'---':>12s}  {'---':>10s}")
            continue

        ns = arange(1, n_produced + 1, dtype=float)
        earth_cum = sum(earth_unit_cost(ns, BASELINE))
        isru_cum = BASELINE["K"] + sum(isru_ops_cost(ns, BASELINE))

        print(f"  {year:>6d}  {n_produced:>8,d}  "
              f"{earth_cum/1e9:>12.1f}  {isru_cum/1e9:>12.1f}  "
              f"{(earth_cum - isru_cum)/1e9:>+10.1f}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print(f"Generating figures in: {fig_dir}\n")

    print("E1: Pathway-specific delivery schedules:")
    for n in [1, 100, 1000, 5000]:
        t_e = earth_delivery_time(n, BASELINE["prod_rate"])
        t_i = unit_to_time(n, BASELINE["prod_rate"], BASELINE["t0"], BASELINE["k_ramp"])
        print(f"  n={n:>5,d}: t_Earth={t_e:.2f} yr, t_ISRU={t_i:.2f} yr")
    print()

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

    p_ll = BASELINE.copy()
    p_ll["LR_launch"] = 0.97
    b_launch = learning_exponent(0.97)
    p_ll["b_L"] = b_launch
    cross_ll = find_crossover_npv(p_ll)
    print(f"Launch learning (LR=0.97, NPV):   ~{cross_ll:,} units "
          f"(shift: +{cross_ll - base_npv:,} from NPV baseline)")

    base_phased = find_crossover_npv_phased(BASELINE, K_years=5)
    print(f"Phased capital (5yr, NPV):        ~{base_phased:,} units "
          f"(shift: {base_phased - base_npv:,} from lump-sum)")

    p_alpha = BASELINE.copy()
    p_alpha["alpha"] = 1.5
    cross_alpha = find_crossover_npv(p_alpha)
    print(f"Mass penalty alpha=1.5 (NPV):     ~{cross_alpha:,} units "
          f"(shift: +{cross_alpha - base_npv:,} from baseline)")

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
    print_learning_scenarios()
    print_distribution_sensitivity()
    print_cumulative_economics()

    print(f"\nDone. All figures saved to {fig_dir}")
