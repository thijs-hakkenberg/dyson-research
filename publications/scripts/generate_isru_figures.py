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
    unit_to_time,
    unit_to_time_piecewise,
    _cumulative_production,
)
from isru_mc import run_mc, sample_mc_params, run_mc_loop, compute_convergence_stats, compute_kaplan_meier, compute_prcc  # noqa: E402

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

        # V3: Permanent vs transient crossover split
        n_conv = int(sum(res.converged_mask))
        if n_conv > 0:
            print(f"         Permanent/transient: {res.n_permanent:,} permanent, "
                  f"{res.n_transient:,} transient "
                  f"(of {n_conv:,} converging)")
            perm_pct = res.n_permanent / len(res.crossovers) * 100
            trans_pct = res.n_transient / len(res.crossovers) * 100
            print(f"           Permanent crossover rate: {perm_pct:.1f}% "
                  f"(transient: {trans_pct:.1f}%)")

        if res.prcc:
            print("         PRCC (unconditional):")
            for pr in sorted(res.prcc, key=lambda x: -abs(x.prcc)):
                print(f"           {pr.name:>12s}: PRCC={pr.prcc:+.3f} {pr.stars}")

        if res.prcc_conditional:
            print("         PRCC (conditional):")
            for pr in sorted(res.prcc_conditional, key=lambda x: -abs(x.prcc)):
                print(f"           {pr.name:>12s}: PRCC={pr.prcc:+.3f} {pr.stars}")

        if res.convergence_drivers:
            print("         Convergence drivers (Cohen's d, converged vs non-converged):")
            for name, d in res.convergence_drivers[:5]:
                direction = "favors conv." if d > 0 else "favors non-conv."
                print(f"           {name:>12s}: d={d:+.3f} ({direction})")


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

    # Stagger annotation offsets to avoid overlap
    annotation_offsets = [
        (400, 30),   # r=0%
        (400, 15),   # r=3%
        (600, -25),  # r=5%
        (400, -15),  # r=10%
    ]

    for idx, (rate, label, color, ls) in enumerate(zip(rates, rate_labels, colors_r, linestyles_r)):
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
            dx, dy = annotation_offsets[idx]
            ax1.annotate(f"r={label}\nN*={cross_n:,}",
                         xy=(cross_n, cross_val / 1e9),
                         xytext=(cross_n + dx, cross_val / 1e9 + dy),
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
# F4: Earth ramp-up robustness test
# ---------------------------------------------------------------------------
def print_earth_ramp_robustness():
    """F4: Test crossover with Earth logistic ramp-up (1yr and 2yr midpoints)."""
    base_npv = find_crossover(BASELINE, discount=True)
    print("\n  F4: Earth ramp-up robustness (NPV, r=5%):")
    print(f"    Baseline (instant Earth start):     N* = {base_npv:,}")
    for t0_e in [1.0, 2.0]:
        cross = find_crossover(
            BASELINE, discount=True, earth_ramp=(t0_e, 2.0)
        )
        shift = cross - base_npv
        pct = shift / base_npv * 100
        print(f"    Earth ramp-up t0={t0_e:.0f}yr, k=2.0:    N* = {cross:,} "
              f"(shift: {shift:+,}, {pct:+.1f}%)")


# ---------------------------------------------------------------------------
# F3: C_floor threshold analysis
# ---------------------------------------------------------------------------
def print_cfloor_threshold():
    """F3: Sweep C_floor to find where crossover fails."""
    from numpy import linspace as np_linspace
    floors = np_linspace(0.3e6, 3.0e6, 28)
    print("\n  F3: C_floor threshold analysis (NPV, r=5%):")
    n_max = 40000
    threshold_found = False
    for cf in floors:
        p = BASELINE.copy()
        p["C_floor"] = cf
        cross = find_crossover(p, n_max=n_max, discount=True)
        label = f"${cf/1e6:.1f}M"
        if cross >= n_max and not threshold_found:
            print(f"    C_floor = {label:>6s}: NO CROSSOVER within {n_max:,} units  <-- threshold")
            threshold_found = True
        elif not threshold_found:
            print(f"    C_floor = {label:>6s}: N* = {cross:,}")
    if not threshold_found:
        print(f"    Crossover achieved at all tested C_floor values up to $3.0M")


# ---------------------------------------------------------------------------
# F6: Production rate sensitivity
# ---------------------------------------------------------------------------
def print_prod_rate_sensitivity():
    """F6: Sweep prod_rate and show crossover shift."""
    base_npv = find_crossover(BASELINE, discount=True)
    rates = [250, 500, 750, 1000]
    print("\n  F6: Production rate sensitivity (NPV, r=5%):")
    for pr in rates:
        p = BASELINE.copy()
        p["prod_rate"] = pr
        cross = find_crossover(p, discount=True)
        shift = cross - base_npv
        print(f"    prod_rate={pr:>5d} units/yr: N* = {cross:,} (shift: {shift:+,})")


# ---------------------------------------------------------------------------
# G1a: Launch learning rate parametric sweep
# ---------------------------------------------------------------------------
def print_launch_learning_sweep():
    """G1a: Sweep launch learning rate and report NPV crossover shift."""
    base_npv = find_crossover_npv(BASELINE)
    lr_values = [0.90, 0.93, 0.95, 0.97, 0.99, 1.00]

    print("\n  G1a: Launch learning rate sweep (NPV, r=5%):")
    print(f"  {'LR_L':>6s}  {'b_L':>8s}  {'N*':>8s}  {'Shift':>8s}  {'Note':>30s}")
    print(f"  {'------':>6s}  {'--------':>8s}  {'--------':>8s}  {'--------':>8s}  {'------------------------------':>30s}")

    for lr_l in lr_values:
        p = BASELINE.copy()
        if lr_l < 1.0:
            b_l = learning_exponent(lr_l)
            p["b_L"] = b_l
            p["LR_launch"] = lr_l
        # else: no launch learning (baseline behavior)
        cross = find_crossover_npv(p)
        shift = cross - base_npv
        note = ""
        if lr_l == 1.00:
            note = "(no launch learning = baseline)"
        elif lr_l == 0.97:
            note = "(Version F default)"
        elif lr_l == 0.90:
            note = "(aggressive learning)"
        print(f"  {lr_l:>6.2f}  {learning_exponent(lr_l) if lr_l < 1.0 else 0.0:>8.4f}  "
              f"{cross:>8,d}  {shift:>+8,d}  {note:>30s}")

    # Decomposition note
    p_fuel = BASELINE.get("p_fuel", 200)
    p_ops = BASELINE.get("p_ops_launch", 800)
    print(f"\n    Launch cost decomposition: fuel=${p_fuel}/kg (fixed) + ops=${p_ops}/kg (learnable)")
    print(f"    At n=10,000 with LR_L=0.97: ops component = ${p_ops} * 10000^{learning_exponent(0.97):.4f} = "
          f"${p_ops * 10000**learning_exponent(0.97):.0f}/kg")


# ---------------------------------------------------------------------------
# G1b: MC convergence diagnostic
# ---------------------------------------------------------------------------
def print_mc_convergence():
    """G1b: Show MC convergence stabilization at increasing sample sizes."""
    checkpoints = [100, 500, 1000, 2000, 5000, 10000]
    rng = default_rng(42)
    n_max_mc = 40000

    # Sample full 10,000 params upfront
    param_arrays = sample_mc_params(rng, 10000, rho=0.3, correlated=True)
    crossovers, _ = run_mc_loop(param_arrays, 0.05, n_max_mc)

    print("\n  G1b: MC convergence diagnostic (r=5%, rho=0.3):")
    print(f"  {'N_runs':>8s}  {'Conv%':>8s}  {'Cond.Med':>10s}  {'Cond.IQR':>20s}  {'Stable?':>8s}")
    print(f"  {'--------':>8s}  {'--------':>8s}  {'----------':>10s}  {'--------------------':>20s}  {'--------':>8s}")

    prev_med = None
    for cp in checkpoints:
        subset = crossovers[:cp]
        converged = subset[subset < n_max_mc]
        conv_rate = len(converged) / cp * 100
        if len(converged) > 0:
            cond_med = int(median(converged))
            q25 = int(percentile(converged, 25))
            q75 = int(percentile(converged, 75))
        else:
            cond_med = n_max_mc
            q25 = q75 = n_max_mc
        stable = "---"
        if prev_med is not None and prev_med > 0:
            pct_change = abs(cond_med - prev_med) / prev_med * 100
            stable = "YES" if pct_change < 2.0 else "no"
        prev_med = cond_med
        print(f"  {cp:>8,d}  {conv_rate:>7.1f}%  {cond_med:>10,d}  [{q25:>8,d}, {q75:>8,d}]  {stable:>8s}")


# ---------------------------------------------------------------------------
# G1c: NPV cumulative economics (extends E6)
# ---------------------------------------------------------------------------
def print_cumulative_economics_npv():
    """G1c: Cumulative economics with NPV-discounted columns at r=5%."""
    prod_rate = BASELINE["prod_rate"]
    t0 = BASELINE["t0"]
    k = BASELINE["k_ramp"]
    r = BASELINE["r"]

    print("\n  G1c: Cumulative economics with NPV (r=5%, baseline):")
    print(f"  {'Year':>6s}  {'Units':>8s}  "
          f"{'Earth($B)':>10s}  {'ISRU($B)':>10s}  {'Net($B)':>10s}  "
          f"{'EarthNPV':>10s}  {'ISRU_NPV':>10s}  {'NetNPV':>10s}")
    print(f"  {'------':>6s}  {'--------':>8s}  "
          f"{'----------':>10s}  {'----------':>10s}  {'----------':>10s}  "
          f"{'----------':>10s}  {'----------':>10s}  {'----------':>10s}")

    for year in [5, 10, 15, 20]:
        n_produced = max(0, _cumulative_production(year, prod_rate, t0, k))
        n_produced = int(round(n_produced))
        if n_produced < 1:
            print(f"  {year:>6d}  {0:>8d}  {'---':>10s}  {'---':>10s}  {'---':>10s}  "
                  f"{'---':>10s}  {'---':>10s}  {'---':>10s}")
            continue

        ns = arange(1, n_produced + 1, dtype=float)

        # Undiscounted
        earth_cum = sum(earth_unit_cost(ns, BASELINE))
        isru_cum = BASELINE["K"] + sum(isru_ops_cost(ns, BASELINE))

        # NPV discounted
        t_e = earth_delivery_time(ns, prod_rate)
        t_i = unit_to_time(ns, prod_rate, t0, k)
        disc_e = (1.0 + r) ** (-t_e)
        disc_i = (1.0 + r) ** (-t_i)
        earth_npv = sum(earth_unit_cost(ns, BASELINE) * disc_e)
        isru_npv = BASELINE["K"] + sum(isru_ops_cost(ns, BASELINE) * disc_i)

        print(f"  {year:>6d}  {n_produced:>8,d}  "
              f"{earth_cum/1e9:>10.1f}  {isru_cum/1e9:>10.1f}  {(earth_cum-isru_cum)/1e9:>+10.1f}  "
              f"{earth_npv/1e9:>10.1f}  {isru_npv/1e9:>10.1f}  {(earth_npv-isru_npv)/1e9:>+10.1f}")


# ---------------------------------------------------------------------------
# G1d: Copula rho sensitivity
# ---------------------------------------------------------------------------
def print_copula_rho_sensitivity():
    """G1d: MC at r=5% with different copula rho values."""
    rho_values = [0.0, 0.3, 0.6]
    n_runs = 10000
    n_max_mc = 40000

    print("\n  G1d: Copula rho sensitivity (r=5%, n=10,000):")
    print(f"  {'rho':>6s}  {'Conv%':>8s}  {'Cond.Med':>10s}  {'Cond.IQR':>20s}")
    print(f"  {'------':>6s}  {'--------':>8s}  {'----------':>10s}  {'--------------------':>20s}")

    for rho in rho_values:
        rng = default_rng(42)
        param_arrays = sample_mc_params(rng, n_runs, rho=rho, correlated=(rho > 0))
        crossovers, _ = run_mc_loop(param_arrays, 0.05, n_max_mc)
        converged = crossovers[crossovers < n_max_mc]
        conv_rate = len(converged) / n_runs * 100
        if len(converged) > 0:
            cond_med = int(median(converged))
            q25 = int(percentile(converged, 25))
            q75 = int(percentile(converged, 75))
        else:
            cond_med = q25 = q75 = n_max_mc
        print(f"  {rho:>6.1f}  {conv_rate:>7.1f}%  {cond_med:>10,d}  [{q25:>8,d}, {q75:>8,d}]")


# ---------------------------------------------------------------------------
# G1e: Rate-dependent ISRU learning robustness
# ---------------------------------------------------------------------------
def print_rate_dependent_learning():
    """G1e: Compare baseline vs rate-dependent learning crossover."""
    base_npv = find_crossover_npv(BASELINE)
    rd_npv = find_crossover_rate_dependent(BASELINE)

    print("\n  G1e: Rate-dependent learning (organizational forgetting, r=5%):")
    print(f"    Baseline (smooth learning):     N* = {base_npv:,}")
    print(f"    Rate-dependent (threshold=20%): N* = {rd_npv:,} "
          f"(shift: {rd_npv - base_npv:+,})")

    # Also test with a higher threshold
    rd_30 = find_crossover_rate_dependent(BASELINE, rate_threshold=0.3)
    print(f"    Rate-dependent (threshold=30%): N* = {rd_30:,} "
          f"(shift: {rd_30 - base_npv:+,})")


# ---------------------------------------------------------------------------
# G1f: Vitamin fraction sensitivity
# ---------------------------------------------------------------------------
def print_vitamin_sensitivity():
    """M1: Two-part vitamin model sensitivity (fraction and $/kg)."""
    base_npv = find_crossover_npv(BASELINE)
    fracs = [0.0, 0.05, 0.10, 0.15]

    print("\n  M1: Two-part vitamin model sensitivity (NPV, r=5%):")
    print(f"  {'Vitamin%':>10s}  {'c_vit$/kg':>10s}  {'N*':>8s}  {'Shift':>8s}")
    print(f"  {'----------':>10s}  {'----------':>10s}  {'--------':>8s}  {'--------':>8s}")

    for vf in fracs:
        p = BASELINE.copy()
        p["vitamin_frac"] = vf
        cross = find_crossover_npv(p, N_max=40000)
        shift = cross - base_npv
        c_vit = int(p.get("c_vitamin_kg", 10000))
        if cross >= 40000:
            print(f"  {vf*100:>9.0f}%  {c_vit:>9,d}$  {'>40,000':>8s}  {'N/A':>8s}")
        else:
            print(f"  {vf*100:>9.0f}%  {c_vit:>9,d}$  {cross:>8,d}  {shift:>+8,d}")

    # Sweep c_vitamin_kg at fixed vitamin_frac=10%
    print(f"\n  M1b: c_vitamin_kg sweep at vitamin_frac=10% (NPV, r=5%):")
    print(f"  {'c_vit$/kg':>10s}  {'N*':>8s}  {'Shift':>8s}")
    print(f"  {'----------':>10s}  {'--------':>8s}  {'--------':>8s}")
    for cvk in [5000, 10000, 50000]:
        p = BASELINE.copy()
        p["vitamin_frac"] = 0.10
        p["c_vitamin_kg"] = cvk
        cross = find_crossover_npv(p, N_max=40000)
        shift = cross - base_npv
        if cross >= 40000:
            print(f"  {cvk:>9,d}$  {'>40,000':>8s}  {'N/A':>8s}")
        else:
            print(f"  {cvk:>9,d}$  {cross:>8,d}  {shift:>+8,d}")


# ---------------------------------------------------------------------------
# Figure 7: Production Schedule Validation (Phase 3)
# ---------------------------------------------------------------------------
def fig_production_schedule():
    """Two-panel figure: instantaneous rate and cumulative production for both pathways."""
    p = BASELINE.copy()
    prod_rate = p["prod_rate"]
    t0 = p["t0"]
    k = p["k_ramp"]

    t = linspace(0, 25, 500)

    # ISRU: instantaneous rate = prod_rate * S(t)
    isru_rate = prod_rate * s_curve(t, t0, k)
    # ISRU: cumulative production
    isru_cum = array([max(0, float(_cumulative_production(ti, prod_rate, t0, k))) for ti in t])

    # Earth: constant rate from t=0
    earth_rate = prod_rate * array([1.0] * len(t))
    earth_cum = prod_rate * t

    fig, (ax1, ax2) = subplots(1, 2, figsize=(12, 4.5))

    # Left panel: instantaneous rate
    ax1.plot(t, earth_rate, color=c_earth, linewidth=2, label="Earth $\\dot{n}(t)$")
    ax1.plot(t, isru_rate, color=c_isru, linewidth=2, label="ISRU $\\dot{n}(t)$")
    ax1.axvline(t0, color="gray", linestyle=":", linewidth=1, alpha=0.7)
    ax1.annotate(f"$t_0 = {t0}$ yr", xy=(t0, prod_rate * 0.5),
                 xytext=(t0 + 1.5, prod_rate * 0.3), fontsize=9, color="gray",
                 arrowprops=dict(arrowstyle="->", color="gray", lw=0.8))
    ax1.set_xlabel("Time (years)")
    ax1.set_ylabel("Production Rate (units/year)")
    ax1.set_xlim(0, 25)
    ax1.set_ylim(0, prod_rate * 1.15)
    ax1.legend(loc="center right", framealpha=0.9)
    ax1.set_title("(a) Instantaneous Production Rate")

    # Right panel: cumulative production
    ax2.plot(t, earth_cum, color=c_earth, linewidth=2, label="Earth $N(t)$")
    ax2.plot(t, isru_cum, color=c_isru, linewidth=2, label="ISRU $N(t)$")
    ax2.axvline(t0, color="gray", linestyle=":", linewidth=1, alpha=0.7)

    # Mark timing gap at N=1000
    n_mark = 1000
    t_earth_mark = n_mark / prod_rate
    t_isru_mark = float(unit_to_time(n_mark, prod_rate, t0, k))
    ax2.plot([t_earth_mark, t_isru_mark], [n_mark, n_mark], "k-", linewidth=1.5, alpha=0.6)
    ax2.plot(t_earth_mark, n_mark, "o", color=c_earth, markersize=6, zorder=5)
    ax2.plot(t_isru_mark, n_mark, "o", color=c_isru, markersize=6, zorder=5)
    ax2.annotate(f"Gap: {t_isru_mark - t_earth_mark:.1f} yr",
                 xy=((t_earth_mark + t_isru_mark) / 2, n_mark),
                 xytext=((t_earth_mark + t_isru_mark) / 2, n_mark + 800),
                 fontsize=8, ha="center",
                 arrowprops=dict(arrowstyle="->", color="black", lw=0.8))

    ax2.set_xlabel("Time (years)")
    ax2.set_ylabel("Cumulative Units Produced")
    ax2.set_xlim(0, 25)
    ax2.set_ylim(0, None)
    ax2.legend(loc="upper left", framealpha=0.9)
    ax2.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax2.set_title("(b) Cumulative Production")

    fig.tight_layout()
    fig.savefig(join(fig_dir, "fig-production-schedule.pdf"))
    close(fig)
    print("  [7/7] fig-production-schedule.pdf")


# ---------------------------------------------------------------------------
# H1c: Convergence curve figure — P(N* <= H) vs H as continuous curve
# ---------------------------------------------------------------------------
def fig_convergence_curve():
    """H1c: Plot P(N* <= H) as continuous curve for three discount rates."""
    mc_rates = [0.03, 0.05, 0.08]
    rate_labels = ["3%", "5%", "8%"]
    rate_colors = ["#2563eb", "#16a34a", "#dc2626"]

    fig, ax = subplots(figsize=(6, 4))
    horizons = arange(1000, 40001, 100)

    for r_fixed, label, color in zip(mc_rates, rate_labels, rate_colors):
        rng = default_rng(42)
        res = run_mc(r_fixed, rng)
        crossovers = res.crossovers

        # Compute P(N* <= H) for each horizon value
        p_below = array([float((crossovers <= h).mean() * 100) for h in horizons])
        ax.plot(horizons, p_below, color=color, linewidth=2, label=f"r = {label}")

    ax.set_xlabel("Planning Horizon $H$ (units)")
    ax.set_ylabel("$P(N^* \\leq H)$ (\\%)")
    ax.set_xlim(1000, 40000)
    ax.set_ylim(0, 100)
    ax.legend(loc="lower right", framealpha=0.9)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x):,}"))

    # Mark key horizons
    for h in [10000, 20000]:
        ax.axvline(h, color="gray", linestyle=":", linewidth=0.8, alpha=0.5)

    fig.savefig(join(fig_dir, "fig-convergence-curve.pdf"))
    close(fig)
    print("  [H1c] fig-convergence-curve.pdf")


# ---------------------------------------------------------------------------
# H1b: K–prod_rate correlation MC comparison
# ---------------------------------------------------------------------------
def print_k_prodrate_correlation():
    """H1b: Compare MC results with and without K-prod_rate correlation."""
    n_runs = 10000
    n_max_mc = 40000
    r_fixed = 0.05

    print("\n  H1b: K-prod_rate correlation sensitivity (r=5%, n=10,000):")
    print(f"  {'rho(K,prod)':>12s}  {'Conv%':>8s}  {'Cond.Med':>10s}  {'Cond.IQR':>20s}")
    print(f"  {'------------':>12s}  {'--------':>8s}  {'----------':>10s}  {'--------------------':>20s}")

    for rho_kp in [0.0, 0.5]:
        rng = default_rng(42)
        param_arrays = sample_mc_params(rng, n_runs, rho=0.3, rho_k_prod=rho_kp, correlated=True)
        crossovers, _ = run_mc_loop(param_arrays, r_fixed, n_max_mc)
        converged = crossovers[crossovers < n_max_mc]
        conv_rate = len(converged) / n_runs * 100
        if len(converged) > 0:
            cond_med = int(median(converged))
            q25 = int(percentile(converged, 25))
            q75 = int(percentile(converged, 75))
        else:
            cond_med = q25 = q75 = n_max_mc

        # Check Spearman(K, prod_rate)
        from scipy.stats import spearmanr as sp_corr
        rho_actual, _ = sp_corr(param_arrays["K"], param_arrays["prod_rate"])
        print(f"  {rho_kp:>12.1f}  {conv_rate:>7.1f}%  {cond_med:>10,d}  [{q25:>8,d}, {q75:>8,d}]  "
              f"(actual Spearman K-prod: {rho_actual:+.3f})")


# ---------------------------------------------------------------------------
# H1d: Piecewise schedule sensitivity test
# ---------------------------------------------------------------------------
def print_piecewise_schedule_test():
    """H1d: Compare baseline logistic vs piecewise schedule crossover."""
    base_npv = find_crossover_npv(BASELINE)

    print("\n  H1d: Piecewise schedule sensitivity (NPV, r=5%):")
    print(f"    Baseline (continuous logistic):  N* = {base_npv:,}")

    # Compute piecewise crossover by using unit_to_time_piecewise in a manual loop
    from numpy import arange as np_arange, cumsum as np_cumsum, where as np_where2
    r = BASELINE["r"]
    ns = np_arange(1, 20001, dtype=float)
    prod_rate = BASELINE["prod_rate"]
    k_ramp = BASELINE["k_ramp"]
    t0 = BASELINE["t0"]

    # Earth side (same as baseline)
    earth_units = earth_unit_cost(ns, BASELINE)
    t_n_earth = earth_delivery_time(ns, prod_rate)
    discount_earth = (1.0 + r) ** (-t_n_earth)
    earth_cum = np_cumsum(earth_units * discount_earth)

    for t_c_offset in [-1.0, -2.0]:
        t_c = t0 + t_c_offset
        t_n_isru = unit_to_time_piecewise(ns, prod_rate, t0, k_ramp, t_construction=t_c)
        ops = isru_ops_cost(ns, BASELINE)
        discount_isru = (1.0 + r) ** (-t_n_isru)
        isru_cum = BASELINE["K"] + np_cumsum(ops * discount_isru)

        diff = isru_cum - earth_cum
        crossings = np_where2(diff <= 0)[0]
        cross_pw = int(ns[crossings[0]]) if len(crossings) > 0 else 20000
        shift = cross_pw - base_npv
        pct = shift / base_npv * 100
        print(f"    Piecewise (t_c={t_c:.0f}yr, t0={t0:.0f}yr):   N* = {cross_pw:,} "
              f"(shift: {shift:+,}, {pct:+.1f}%)")


# ---------------------------------------------------------------------------
# H1e: Cash-flow timing sensitivity (manufacturing lead-time)
# ---------------------------------------------------------------------------
def print_cashflow_timing_test():
    """H1e: Test sensitivity to manufacturing lead-time adjustment."""
    base_npv = find_crossover_npv(BASELINE)

    print("\n  H1e: Cash-flow timing sensitivity (NPV, r=5%):")
    print(f"    Baseline (pay-at-delivery):      N* = {base_npv:,}")

    for tau in [0.5, 1.0]:
        cross = find_crossover_mfg_lead(BASELINE, tau_mfg=tau)
        shift = cross - base_npv
        pct = shift / base_npv * 100
        print(f"    Mfg lead-time tau={tau:.1f}yr:         N* = {cross:,} "
              f"(shift: {shift:+,}, {pct:+.1f}%)")


# ---------------------------------------------------------------------------
# I1: Earth fixed-cost (K_E) sensitivity
# ---------------------------------------------------------------------------
def print_earth_capex_sensitivity():
    """I1: Test effect of adding Earth-side factory capex."""
    base_npv = find_crossover_npv(BASELINE)

    print("\n  I1: Earth fixed-cost sensitivity (NPV, r=5%):")
    print(f"    Baseline (K_E=0, Earth base pre-existing): N* = {base_npv:,}")

    for k_e in [1e9, 5e9, 10e9]:
        # Add Earth capex: subtract from Earth cumulative at t=0
        # Equivalent to reducing ISRU advantage by K_E
        from numpy import arange as np_arange, cumsum as np_cumsum, where as np_where3
        r = BASELINE["r"]
        ns = np_arange(1, 20001, dtype=float)
        prod_rate = BASELINE["prod_rate"]
        k_ramp = BASELINE["k_ramp"]

        earth_units = earth_unit_cost(ns, BASELINE)
        t_n_earth = earth_delivery_time(ns, prod_rate)
        discount_earth = (1.0 + r) ** (-t_n_earth)
        earth_cum = k_e + np_cumsum(earth_units * discount_earth)

        ops = isru_ops_cost(ns, BASELINE)
        t_n_isru = unit_to_time(ns, prod_rate, BASELINE["t0"], k_ramp)
        discount_isru = (1.0 + r) ** (-t_n_isru)
        isru_cum = BASELINE["K"] + np_cumsum(ops * discount_isru)

        diff = isru_cum - earth_cum
        crossings = np_where3(diff <= 0)[0]
        cross = int(ns[crossings[0]]) if len(crossings) > 0 else 20000
        shift = cross - base_npv
        print(f"    K_E=${k_e/1e9:.0f}B:                          N* = {cross:,} "
              f"(shift: {shift:+,})")


# ---------------------------------------------------------------------------
# I2: Extended C_floor sweep to find failure threshold
# ---------------------------------------------------------------------------
def print_cfloor_failure_threshold():
    """I2: Find exact C_floor at which crossover fails."""
    from numpy import linspace as np_linspace
    n_max = 40000

    print("\n  I2: C_floor failure threshold (NPV, r=5%, N_max=40,000):")
    for cf in np_linspace(2.0e6, 10.0e6, 17):
        p = BASELINE.copy()
        p["C_floor"] = cf
        cross = find_crossover(p, n_max=n_max, discount=True)
        label = f"${cf/1e6:.1f}M"
        if cross >= n_max:
            print(f"    C_floor = {label:>7s}: NO CROSSOVER within {n_max:,} units  <-- threshold")
            break
        else:
            print(f"    C_floor = {label:>7s}: N* = {cross:,}")


# ---------------------------------------------------------------------------
# I3: Additional correlation tests
# ---------------------------------------------------------------------------
def print_additional_correlations():
    """I3: Test additional plausible correlations in MC."""
    n_runs = 10000
    n_max_mc = 40000
    r_fixed = 0.05

    print("\n  I3: Additional correlation sensitivity (r=5%, n=10,000):")
    print(f"  {'Config':>30s}  {'Conv%':>8s}  {'Cond.Med':>10s}")
    print(f"  {'------------------------------':>30s}  {'--------':>8s}  {'----------':>10s}")

    configs = [
        ("Baseline (rho_pK=0.3)", 0.3, 0.0),
        ("+ rho(K,prod)=0.5", 0.3, 0.5),
    ]

    for label, rho_pk, rho_kp in configs:
        rng = default_rng(42)
        param_arrays = sample_mc_params(rng, n_runs, rho=rho_pk, rho_k_prod=rho_kp, correlated=True)
        crossovers, _ = run_mc_loop(param_arrays, r_fixed, n_max_mc)
        converged = crossovers[crossovers < n_max_mc]
        conv_rate = len(converged) / n_runs * 100
        cond_med = int(median(converged)) if len(converged) > 0 else n_max_mc
        print(f"  {label:>30s}  {conv_rate:>7.1f}%  {cond_med:>10,d}")


# ---------------------------------------------------------------------------
# I4: Revenue breakeven calculation
# ---------------------------------------------------------------------------
def print_revenue_breakeven():
    """I4: Calculate breakeven revenue rate where ISRU delay eliminates savings."""
    prod_rate = BASELINE["prod_rate"]
    t0 = BASELINE["t0"]
    k_ramp = BASELINE["k_ramp"]
    r = BASELINE["r"]

    # At crossover, compute ISRU savings and delay cost
    cross_npv = find_crossover_npv(BASELINE)
    n_check = cross_npv * 2  # check at 2x crossover

    from numpy import arange as np_arange2, sum as np_sum2
    ns = np_arange2(1, n_check + 1, dtype=float)

    # Timing
    t_earth = earth_delivery_time(ns, prod_rate)
    t_isru = unit_to_time(ns, prod_rate, t0, k_ramp)
    delay = t_isru - t_earth  # years of delay per unit

    # ISRU NPV savings at 2x crossover
    earth_units = earth_unit_cost(ns, BASELINE)
    disc_earth = (1.0 + r) ** (-t_earth)
    earth_cum = float(np_sum2(earth_units * disc_earth))

    ops = isru_ops_cost(ns, BASELINE)
    disc_isru = (1.0 + r) ** (-t_isru)
    isru_cum = BASELINE["K"] + float(np_sum2(ops * disc_isru))

    savings_npv = earth_cum - isru_cum  # positive = ISRU cheaper

    # Opportunity cost: sum of (revenue * delay * discount) per unit
    # Revenue R per unit per year, lost for 'delay' years
    # Approximate: opportunity cost = R * sum(delay_n * disc_n)
    opp_cost_factor = float(np_sum2(delay * disc_isru))  # sum of discounted delay-years

    # Breakeven: savings = R * opp_cost_factor
    if opp_cost_factor > 0:
        breakeven_revenue = savings_npv / opp_cost_factor
    else:
        breakeven_revenue = float('inf')

    print(f"\n  I4: Revenue breakeven analysis (at N={n_check:,}, r=5%):")
    print(f"    NPV crossover at baseline:     N* = {cross_npv:,}")
    print(f"    ISRU NPV savings at N={n_check:,}:  ${savings_npv/1e9:.1f}B")
    print(f"    Mean ISRU delay:               {float(delay.mean()):.1f} years")
    print(f"    Breakeven revenue per unit:     ${breakeven_revenue/1e6:.2f}M/yr")
    print(f"    (Below this, ISRU is preferred; above, Earth is preferred)")
    print(f"    For context: at $2M/yr revenue per unit,")

    opp_cost_2m = 2e6 * opp_cost_factor
    net = savings_npv - opp_cost_2m
    print(f"      Opportunity cost = ${opp_cost_2m/1e9:.1f}B, net benefit = ${net/1e9:.1f}B "
          f"({'ISRU preferred' if net > 0 else 'Earth preferred'})")


# ---------------------------------------------------------------------------
# I5: No-launch-learning sensitivity (now that baseline has launch learning)
# ---------------------------------------------------------------------------
def print_no_launch_learning_sensitivity():
    """I5: Report crossover without launch learning as sensitivity bound."""
    base_npv = find_crossover_npv(BASELINE)

    p_no_ll = BASELINE.copy()
    p_no_ll["b_L"] = None
    cross_no_ll = find_crossover_npv(p_no_ll)

    print(f"\n  I5: No-launch-learning sensitivity (NPV, r=5%):")
    print(f"    Baseline (LR_L=0.97):     N* = {base_npv:,}")
    print(f"    No launch learning:       N* = {cross_no_ll:,} (shift: {cross_no_ll - base_npv:+,})")


# ---------------------------------------------------------------------------
# J1: Fuel floor sensitivity
# ---------------------------------------------------------------------------
def print_fuel_floor_sensitivity():
    """J1: Sweep fuel floor to show robustness of structural asymmetry argument."""
    base_npv = find_crossover_npv(BASELINE)

    print(f"\n  J1: Fuel floor sensitivity (NPV, r=5%, baseline N*={base_npv:,}):")
    print(f"  {'p_fuel':>8s}  {'p_ops':>8s}  {'N*':>8s}  {'Shift':>8s}")
    print(f"  {'--------':>8s}  {'--------':>8s}  {'--------':>8s}  {'--------':>8s}")

    for p_fuel in [50, 100, 200, 300, 400]:
        p = BASELINE.copy()
        p["p_fuel"] = p_fuel
        p["p_ops_launch"] = 1000 - p_fuel  # keep total first-unit = $1000/kg
        cross = find_crossover_npv(p)
        shift = cross - base_npv
        print(f"  {p_fuel:>7d}$  {1000-p_fuel:>7d}$  {cross:>8,d}  {shift:>+8,d}")


# ---------------------------------------------------------------------------
# K1: Risk-adjusted discounting sensitivity
# ---------------------------------------------------------------------------
def print_risk_premium_sensitivity():
    """K1: Apply risk premium to ISRU pathway only."""
    from numpy import arange as np_arange3, cumsum as np_cumsum3, where as np_where4
    base_npv = find_crossover_npv(BASELINE)

    print(f"\n  K1: Risk-adjusted discounting (ISRU risk premium, r_base=5%):")
    print(f"    Baseline (same rate both pathways): N* = {base_npv:,}")

    for delta_r in [0.02, 0.03, 0.05]:
        r_earth = BASELINE["r"]
        r_isru = BASELINE["r"] + delta_r

        ns = np_arange3(1, 40001, dtype=float)
        prod_rate = BASELINE["prod_rate"]
        k_ramp = BASELINE["k_ramp"]

        # Earth side at base rate
        earth_units = earth_unit_cost(ns, BASELINE)
        t_n_earth = earth_delivery_time(ns, prod_rate)
        discount_earth = (1.0 + r_earth) ** (-t_n_earth)
        earth_cum = np_cumsum3(earth_units * discount_earth)

        # ISRU side at elevated rate
        ops = isru_ops_cost(ns, BASELINE)
        t_n_isru = unit_to_time(ns, prod_rate, BASELINE["t0"], k_ramp)
        discount_isru = (1.0 + r_isru) ** (-t_n_isru)
        isru_cum = BASELINE["K"] + np_cumsum3(ops * discount_isru)

        diff = isru_cum - earth_cum
        crossings = np_where4(diff <= 0)[0]
        cross = int(ns[crossings[0]]) if len(crossings) > 0 else 40000
        shift = cross - base_npv
        status = f"N* = {cross:,} (shift: {shift:+,})" if cross < 40000 else "NO CROSSOVER within 40,000"
        print(f"    ISRU premium +{delta_r:.0%} (r_ISRU={r_isru:.0%}):  {status}")


# ---------------------------------------------------------------------------
# M2: Launch learning re-indexing sensitivity
# ---------------------------------------------------------------------------
def print_launches_per_unit_sensitivity():
    """M2: Sweep launches_per_unit to show effect of re-indexing launch learning."""
    base_npv = find_crossover_npv(BASELINE)

    print(f"\n  M2: Launch learning re-indexing (launches_per_unit, NPV, r=5%):")
    print(f"  {'L/unit':>8s}  {'N*':>8s}  {'Shift':>8s}  {'Note':>30s}")
    print(f"  {'--------':>8s}  {'--------':>8s}  {'--------':>8s}  {'------------------------------':>30s}")

    for lpu in [0.5, 1.0, 2.0]:
        p = BASELINE.copy()
        p["launches_per_unit"] = lpu
        cross = find_crossover_npv(p, N_max=40000)
        shift = cross - base_npv
        note = ""
        if lpu == 0.5:
            note = "(co-manifesting, 2 units/launch)"
        elif lpu == 1.0:
            note = "(baseline, 1:1)"
        elif lpu == 2.0:
            note = "(dedicated, 2 launches/unit)"
        if cross >= 40000:
            print(f"  {lpu:>8.1f}  {'>40,000':>8s}  {'N/A':>8s}  {note:>30s}")
        else:
            print(f"  {lpu:>8.1f}  {cross:>8,d}  {shift:>+8,d}  {note:>30s}")


# ---------------------------------------------------------------------------
# M3: Capital maintenance sensitivity
# ---------------------------------------------------------------------------
def print_maintenance_sensitivity():
    """M3: Sweep K_maint_frac to show effect of ongoing capital maintenance."""
    base_npv = find_crossover_npv(BASELINE)

    print(f"\n  M3: Capital maintenance sensitivity (NPV, r=5%):")
    print(f"  {'K_maint%':>10s}  {'Interval':>10s}  {'N*':>8s}  {'Shift':>8s}")
    print(f"  {'----------':>10s}  {'----------':>10s}  {'--------':>8s}  {'--------':>8s}")

    for frac in [0.0, 0.05, 0.10, 0.15]:
        p = BASELINE.copy()
        p["K_maint_frac"] = frac
        p["K_maint_interval"] = 5
        cross = find_crossover(p, n_max=40000, discount=True)
        shift = cross - base_npv
        if cross >= 40000:
            print(f"  {frac*100:>9.0f}%  {5:>8d}yr  {'>40,000':>8s}  {'N/A':>8s}")
        else:
            print(f"  {frac*100:>9.0f}%  {5:>8d}yr  {cross:>8,d}  {shift:>+8,d}")


# ---------------------------------------------------------------------------
# M4: Technical success probability
# ---------------------------------------------------------------------------
def print_success_probability():
    """M4: Expected value analysis as function of technical success probability."""
    base_npv = find_crossover_npv(BASELINE)

    # At 2x crossover, compute ISRU savings
    n_check = base_npv * 2
    ns = arange(1, n_check + 1, dtype=float)
    prod_rate = BASELINE["prod_rate"]
    k_ramp = BASELINE["k_ramp"]
    r = BASELINE["r"]

    t_earth = earth_delivery_time(ns, prod_rate)
    t_isru = unit_to_time(ns, prod_rate, BASELINE["t0"], k_ramp)

    earth_units = earth_unit_cost(ns, BASELINE)
    disc_earth = (1.0 + r) ** (-t_earth)
    earth_cum = float(sum(earth_units * disc_earth))

    ops = isru_ops_cost(ns, BASELINE)
    disc_isru = (1.0 + r) ** (-t_isru)
    isru_cum = BASELINE["K"] + float(sum(ops * disc_isru))

    savings = earth_cum - isru_cum  # positive = ISRU cheaper
    K = BASELINE["K"]

    # p_s * savings > (1-p_s) * K  →  p_s > K / (savings + K)
    p_s_min = K / (savings + K) if (savings + K) > 0 else 1.0

    print(f"\n  M4: Technical success probability (NPV, r=5%, N={n_check:,}):")
    print(f"    ISRU NPV savings at N={n_check:,}: ${savings/1e9:.1f}B")
    print(f"    ISRU capital at risk:           ${K/1e9:.0f}B")
    print(f"    Minimum p_success for ISRU preference: {p_s_min:.2%}")

    print(f"\n  {'p_success':>12s}  {'E[NPV_ISRU]-E[NPV_Earth]':>25s}  {'Preferred':>12s}")
    print(f"  {'------------':>12s}  {'-------------------------':>25s}  {'------------':>12s}")
    for ps in [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]:
        # E[ISRU cost] = ps * isru_cum + (1-ps) * (K + earth_cum)  [failure: sunk K + revert to Earth]
        # E[Earth cost] = earth_cum
        # Net = E[ISRU] - E[Earth] = ps*(isru_cum - earth_cum) + (1-ps)*K
        net = ps * (isru_cum - earth_cum) + (1 - ps) * K
        pref = "ISRU" if net < 0 else "Earth"
        print(f"  {ps:>11.0%}  {net/1e9:>+24.1f}B  {pref:>12s}")


# ---------------------------------------------------------------------------
# M5: Commercial discount rate (r=15%)
# ---------------------------------------------------------------------------
def print_commercial_rate():
    """M5: Report crossover at r=15% (commercial hurdle rate)."""
    base_npv = find_crossover_npv(BASELINE)

    print(f"\n  M5: Commercial discount rate (r=15%):")
    p = BASELINE.copy()
    p["r"] = 0.15
    cross = find_crossover(p, n_max=40000, discount=True)
    if cross >= 40000:
        print(f"    r=15%: NO CROSSOVER within 40,000 units")
    else:
        print(f"    r=15%: N* = {cross:,}")

    # Also report at r=10% and r=12% for reference
    for rate in [0.10, 0.12, 0.15, 0.20]:
        p["r"] = rate
        cross = find_crossover(p, n_max=40000, discount=True)
        status = f"N* = {cross:,}" if cross < 40000 else "NO CROSSOVER"
        print(f"    r={rate:.0%}: {status}")


# ---------------------------------------------------------------------------
# M6: Capex-schedule coupling
# ---------------------------------------------------------------------------
def print_capex_coupling():
    """M6: Test phased capex coupling to deployment schedule."""
    base_npv = find_crossover_npv(BASELINE)

    print(f"\n  M6: Capex-schedule coupling (phased K over 5yr, NPV, r=5%):")
    print(f"    Baseline (lump-sum K, t0=5yr): N* = {base_npv:,}")

    base_phased = find_crossover(BASELINE, n_max=40000, discount=True, phased_k_years=5)
    print(f"    Phased K (5yr, no coupling):   N* = {base_phased:,}")

    # Coupling: t0 = t0_base + beta * (K_years - 1)
    for beta in [0.0, 0.5, 1.0]:
        t0_eff = BASELINE["t0"] + beta * (5 - 1)
        p = BASELINE.copy()
        p["t0"] = t0_eff
        cross = find_crossover(p, n_max=40000, discount=True, phased_k_years=5)
        shift = cross - base_npv
        if cross >= 40000:
            print(f"    beta={beta:.1f} (t0_eff={t0_eff:.0f}yr):          NO CROSSOVER")
        else:
            print(f"    beta={beta:.1f} (t0_eff={t0_eff:.0f}yr):          N* = {cross:,} (shift: {shift:+,})")


# ---------------------------------------------------------------------------
# O1: p_s_min vs evaluation horizon
# ---------------------------------------------------------------------------
def print_ps_min_vs_horizon():
    """O1: Compute minimum success probability as function of evaluation horizon."""
    from numpy import arange as np_ar, sum as np_sum
    prod_rate = BASELINE["prod_rate"]
    k_ramp = BASELINE["k_ramp"]
    r = BASELINE["r"]
    K = BASELINE["K"]
    cross_npv = find_crossover_npv(BASELINE)

    print(f"\n  O1: p_s_min vs evaluation horizon (NPV, r=5%, N*={cross_npv:,}):")
    print(f"  {'Horizon':>10s}  {'Mult':>6s}  {'Savings($B)':>12s}  {'p_s_min':>10s}")
    print(f"  {'----------':>10s}  {'------':>6s}  {'------------':>12s}  {'----------':>10s}")

    for mult in [1.5, 2.0, 3.0, 5.0]:
        n_check = int(cross_npv * mult)
        ns = np_ar(1, n_check + 1, dtype=float)

        t_earth = earth_delivery_time(ns, prod_rate)
        t_isru = unit_to_time(ns, prod_rate, BASELINE["t0"], k_ramp)

        earth_units = earth_unit_cost(ns, BASELINE)
        disc_earth = (1.0 + r) ** (-t_earth)
        earth_cum = float(np_sum(earth_units * disc_earth))

        ops = isru_ops_cost(ns, BASELINE)
        disc_isru = (1.0 + r) ** (-t_isru)
        isru_cum = K + float(np_sum(ops * disc_isru))

        savings = earth_cum - isru_cum
        p_s_min = K / (savings + K) if (savings + K) > 0 else 1.0
        print(f"  {n_check:>8,d}N  {mult:>5.1f}x  {savings/1e9:>11.1f}B  {p_s_min:>9.1%}")

    # Also compute at fixed unit counts
    print(f"\n  {'Units':>10s}  {'Savings($B)':>12s}  {'p_s_min':>10s}")
    print(f"  {'----------':>10s}  {'------------':>12s}  {'----------':>10s}")
    for n_fix in [5000, 10000, 20000]:
        ns = np_ar(1, n_fix + 1, dtype=float)
        t_earth = earth_delivery_time(ns, prod_rate)
        t_isru = unit_to_time(ns, prod_rate, BASELINE["t0"], k_ramp)
        earth_units = earth_unit_cost(ns, BASELINE)
        disc_earth = (1.0 + r) ** (-t_earth)
        earth_cum = float(np_sum(earth_units * disc_earth))
        ops = isru_ops_cost(ns, BASELINE)
        disc_isru = (1.0 + r) ** (-t_isru)
        isru_cum = K + float(np_sum(ops * disc_isru))
        savings = earth_cum - isru_cum
        p_s_min = K / (savings + K) if (savings + K) > 0 else 1.0
        print(f"  {n_fix:>8,d}  {savings/1e9:>11.1f}B  {p_s_min:>9.1%}")


# ---------------------------------------------------------------------------
# O2: ISRU facility availability sensitivity
# ---------------------------------------------------------------------------
def print_availability_sensitivity():
    """O2: Sweep ISRU facility availability factor."""
    base_npv = find_crossover_npv(BASELINE)

    print(f"\n  O2: ISRU facility availability sensitivity (NPV, r=5%):")
    print(f"  {'Avail':>8s}  {'Eff.Rate':>10s}  {'N*':>8s}  {'Shift':>8s}")
    print(f"  {'--------':>8s}  {'----------':>10s}  {'--------':>8s}  {'--------':>8s}")

    for avail in [1.0, 0.95, 0.85, 0.80, 0.70]:
        p = BASELINE.copy()
        p["availability"] = avail
        eff_rate = int(p["prod_rate"] * avail)
        cross = find_crossover(p, n_max=40000, discount=True)
        shift = cross - base_npv
        if cross >= 40000:
            print(f"  {avail:>7.0%}  {eff_rate:>8d}/yr  {'>40,000':>8s}  {'N/A':>8s}")
        else:
            print(f"  {avail:>7.0%}  {eff_rate:>8d}/yr  {cross:>8,d}  {shift:>+8,d}")


# ---------------------------------------------------------------------------
# N1: Earth manufacturing cost floor sensitivity
# ---------------------------------------------------------------------------
def print_earth_mfg_floor_sensitivity():
    """N1: Sweep C_mfg_floor to show effect of Earth manufacturing cost floor."""
    base_npv = find_crossover_npv(BASELINE)

    print(f"\n  N1: Earth mfg cost floor sensitivity (NPV, r=5%):")
    print(f"  {'C_mfg_floor':>12s}  {'N*':>8s}  {'Shift':>8s}")
    print(f"  {'------------':>12s}  {'--------':>8s}  {'--------':>8s}")

    for floor in [0, 2e6, 5e6, 10e6]:
        p = BASELINE.copy()
        p["C_mfg_floor"] = floor
        cross = find_crossover(p, n_max=40000, discount=True)
        shift = cross - base_npv
        label = f"${floor/1e6:.0f}M" if floor > 0 else "$0 (none)"
        if cross >= 40000:
            print(f"  {label:>12s}  {'>40,000':>8s}  {'N/A':>8s}")
        else:
            print(f"  {label:>12s}  {cross:>8,d}  {shift:>+8,d}")

    # Show what happens to Earth unit cost at n=10000
    n_test = 10000.0
    base_cost = float(earth_unit_cost(n_test, BASELINE))
    for floor in [5e6, 10e6]:
        p = BASELINE.copy()
        p["C_mfg_floor"] = floor
        cost = float(earth_unit_cost(n_test, p))
        print(f"    Earth unit cost at n={int(n_test):,} with floor=${floor/1e6:.0f}M: "
              f"${cost/1e6:.2f}M (baseline: ${base_cost/1e6:.2f}M)")


# ---------------------------------------------------------------------------
# N1b: Log-normal K MC comparison
# ---------------------------------------------------------------------------
def print_lognormal_k_comparison():
    """N1b: Compare uniform vs log-normal K distribution in MC."""
    n_runs = 10000
    n_max_mc = 40000
    r_fixed = 0.05

    print(f"\n  N1b: Log-normal K distribution comparison (r=5%, n={n_runs:,}):")
    print(f"  {'K dist':>12s}  {'Conv%':>8s}  {'Cond.Med':>10s}  {'Cond.IQR':>20s}  {'K median':>10s}  {'K mean':>10s}")
    print(f"  {'------------':>12s}  {'--------':>8s}  {'----------':>10s}  {'--------------------':>20s}  {'----------':>10s}  {'----------':>10s}")

    for k_dist in ["uniform", "lognormal"]:
        rng = default_rng(42)
        param_arrays = sample_mc_params(rng, n_runs, rho=0.3, correlated=True,
                                         k_distribution=k_dist)
        crossovers, _ = run_mc_loop(param_arrays, r_fixed, n_max_mc)
        converged = crossovers[crossovers < n_max_mc]
        conv_rate = len(converged) / n_runs * 100
        if len(converged) > 0:
            cond_med = int(median(converged))
            q25 = int(percentile(converged, 25))
            q75 = int(percentile(converged, 75))
        else:
            cond_med = q25 = q75 = n_max_mc

        k_med = float(median(param_arrays["K"])) / 1e9
        k_mean = float(param_arrays["K"].mean()) / 1e9
        print(f"  {k_dist:>12s}  {conv_rate:>7.1f}%  {cond_med:>10,d}  [{q25:>8,d}, {q75:>8,d}]  ${k_med:>8.1f}B  ${k_mean:>8.1f}B")


# ---------------------------------------------------------------------------
# N1c: Kaplan-Meier survival diagnostic
# ---------------------------------------------------------------------------
def print_kaplan_meier_diagnostic():
    """N1c: Compare KM median with conditional median across discount rates."""
    mc_rates = [0.03, 0.05, 0.08]
    n_runs = 10000
    n_max_mc = 40000

    print(f"\n  N1c: Kaplan-Meier survival analysis (n={n_runs:,}):")
    print(f"  {'Rate':>6s}  {'Conv%':>8s}  {'Cond.Med':>10s}  {'KM Med':>10s}  {'Divergence':>12s}")
    print(f"  {'------':>6s}  {'--------':>8s}  {'----------':>10s}  {'----------':>10s}  {'------------':>12s}")

    for r_fixed in mc_rates:
        rng = default_rng(42)
        res = run_mc(r_fixed, rng, n_runs=n_runs, n_max_mc=n_max_mc)
        km_med, km_times, km_surv = compute_kaplan_meier(res.crossovers, n_max_mc)
        cond_med = res.stats.cond_median
        if km_med < float('inf') and cond_med < n_max_mc:
            divergence = abs(km_med - cond_med) / cond_med * 100
            div_label = f"{divergence:.1f}%"
        else:
            div_label = "N/A"
        km_label = f"{int(km_med):,}" if km_med < float('inf') else ">H"
        conv_pct = res.stats.convergence_rate
        print(f"  {r_fixed:.0%}  {conv_pct:>7.1f}%  {int(cond_med):>10,d}  {km_label:>10s}  {div_label:>12s}")

    print("    (Divergence measures bias from ignoring censored observations)")


# ---------------------------------------------------------------------------
# N1d: S-curve k_ramp sensitivity
# ---------------------------------------------------------------------------
def print_k_ramp_sensitivity():
    """N1d: Sweep k_ramp to show effect of S-curve steepness on crossover."""
    base_npv = find_crossover_npv(BASELINE)

    print(f"\n  N1d: S-curve steepness (k_ramp) sensitivity (NPV, r=5%):")
    print(f"  {'k_ramp':>8s}  {'N*':>8s}  {'Shift':>8s}  {'Ramp 10-90% (yr)':>18s}")
    print(f"  {'--------':>8s}  {'--------':>8s}  {'--------':>8s}  {'------------------':>18s}")

    for k in [0.5, 1.0, 2.0, 3.0, 4.0]:
        p = BASELINE.copy()
        p["k_ramp"] = k
        cross = find_crossover(p, n_max=40000, discount=True)
        shift = cross - base_npv
        # Time for S-curve to go from 10% to 90%: t(0.9) - t(0.1)
        # S(t) = 0.1 → t = t0 + ln(0.1/0.9)/k; S(t)=0.9 → t = t0 + ln(9)/k
        import math
        ramp_time = 2 * math.log(9) / k
        if cross >= 40000:
            print(f"  {k:>8.1f}  {'>40,000':>8s}  {'N/A':>8s}  {ramp_time:>17.1f}yr")
        else:
            print(f"  {k:>8.1f}  {cross:>8,d}  {shift:>+8,d}  {ramp_time:>17.1f}yr")


# ---------------------------------------------------------------------------
# N1e: Revenue breakeven with finite asset lifetime
# ---------------------------------------------------------------------------
def print_revenue_breakeven_with_lifetime():
    """N1e: Revenue breakeven R* for multiple asset lifetimes L."""
    from numpy import arange as np_ar, sum as np_sum, minimum as np_min
    prod_rate = BASELINE["prod_rate"]
    t0 = BASELINE["t0"]
    k_ramp = BASELINE["k_ramp"]
    r = BASELINE["r"]

    cross_npv = find_crossover_npv(BASELINE)
    n_check = cross_npv * 2

    ns = np_ar(1, n_check + 1, dtype=float)
    t_earth = earth_delivery_time(ns, prod_rate)
    t_isru = unit_to_time(ns, prod_rate, t0, k_ramp)
    delay = t_isru - t_earth

    # Compute ISRU NPV savings
    earth_units = earth_unit_cost(ns, BASELINE)
    disc_earth = (1.0 + r) ** (-t_earth)
    earth_cum = float(np_sum(earth_units * disc_earth))

    ops = isru_ops_cost(ns, BASELINE)
    disc_isru = (1.0 + r) ** (-t_isru)
    isru_cum = BASELINE["K"] + float(np_sum(ops * disc_isru))
    savings_npv = earth_cum - isru_cum

    print(f"\n  N1e: Revenue breakeven with finite asset lifetime (N={n_check:,}, r=5%):")
    print(f"    ISRU NPV savings: ${savings_npv/1e9:.1f}B")
    print(f"  {'Lifetime':>10s}  {'R* ($/yr/unit)':>16s}  {'R* ($M/yr)':>12s}  {'Note':>30s}")
    print(f"  {'----------':>10s}  {'----------------':>16s}  {'------------':>12s}  {'------------------------------':>30s}")

    for L in [10, 20, 30, 1000]:
        # Opportunity cost factor: sum of min(delay_n, L) * discount per unit
        effective_delay = np_min(delay, L)
        opp_cost_factor = float(np_sum(effective_delay * disc_isru))

        if opp_cost_factor > 0:
            r_star = savings_npv / opp_cost_factor
        else:
            r_star = float('inf')

        note = ""
        if L == 1000:
            note = "(infinite lifetime approx)"
        elif L == 20:
            note = "(baseline assumption)"
        print(f"  {L:>8d}yr  {r_star:>16,.0f}  {r_star/1e6:>11.2f}M  {note:>30s}")


# ---------------------------------------------------------------------------
# V1: Pioneering phase sensitivity
# ---------------------------------------------------------------------------
def print_pioneering_phase_sensitivity():
    """V1: Test two-phase ISRU learning model with elevated early-unit costs."""
    base_npv = find_crossover_npv(BASELINE)

    print(f"\n  V1: Pioneering phase sensitivity (NPV, r=5%, baseline N*={base_npv:,}):")
    print(f"  {'gamma':>8s}  {'n_p':>6s}  {'N*':>8s}  {'Shift':>8s}  {'%':>6s}")
    print(f"  {'--------':>8s}  {'------':>6s}  {'--------':>8s}  {'--------':>8s}  {'------':>6s}")

    for gamma in [1, 2, 5]:
        for n_p in [20, 50, 100, 500, 1000]:
            p = BASELINE.copy()
            p["pioneer_gamma"] = gamma
            p["pioneer_n"] = n_p
            cross = find_crossover(p, n_max=40000, discount=True)
            shift = cross - base_npv
            pct = shift / base_npv * 100 if base_npv > 0 else 0
            if cross >= 40000:
                print(f"  {gamma:>8d}  {n_p:>6d}  {'>40,000':>8s}  {'N/A':>8s}  {'N/A':>6s}")
            else:
                print(f"  {gamma:>8d}  {n_p:>6d}  {cross:>8,d}  {shift:>+8,d}  {pct:>+5.1f}%")


# ---------------------------------------------------------------------------
# V2: QA/certification cost sensitivity
# ---------------------------------------------------------------------------
def print_qa_cost_sensitivity():
    """V2: Test per-unit QA/certification cost added to ISRU pathway."""
    base_npv = find_crossover_npv(BASELINE)

    print(f"\n  V2: QA/certification cost sensitivity (NPV, r=5%, baseline N*={base_npv:,}):")
    print(f"  {'C_QA1':>10s}  {'LR_QA':>8s}  {'N*':>8s}  {'Shift':>8s}")
    print(f"  {'----------':>10s}  {'--------':>8s}  {'--------':>8s}  {'--------':>8s}")

    for c_qa in [0.5e6, 1e6, 3e6]:
        for lr_qa in [0.85, 0.90]:
            p = BASELINE.copy()
            p["C_QA1"] = c_qa
            p["LR_QA"] = lr_qa
            cross = find_crossover(p, n_max=40000, discount=True)
            shift = cross - base_npv
            label = f"${c_qa/1e6:.1f}M"
            if cross >= 40000:
                print(f"  {label:>10s}  {lr_qa:>8.2f}  {'>40,000':>8s}  {'N/A':>8s}")
            else:
                print(f"  {label:>10s}  {lr_qa:>8.2f}  {cross:>8,d}  {shift:>+8,d}")


# ---------------------------------------------------------------------------
# V4: ISRU ops timing sensitivity (symmetric with Earth lead-time test)
# ---------------------------------------------------------------------------
def print_isru_ops_timing_sensitivity():
    """V4: Test ISRU ops pre-purchase timing (symmetric with Earth cash-flow test)."""
    base_npv = find_crossover_npv(BASELINE)

    print(f"\n  V4: ISRU ops pre-purchase timing sensitivity (NPV, r=5%):")
    print(f"    Baseline (pay-at-production):   N* = {base_npv:,}")

    # Shift a fraction of ISRU ops cost earlier by tau_ops years
    from numpy import arange as np_ar, cumsum as np_cs, where as np_w
    r = BASELINE["r"]
    ns = np_ar(1, 20001, dtype=float)
    prod_rate = BASELINE["prod_rate"]
    k_ramp = BASELINE["k_ramp"]

    # Earth side (standard)
    earth_units = earth_unit_cost(ns, BASELINE)
    from isru_model import earth_delivery_time as edt, unit_to_time_piecewise as utp
    t_n_earth = edt(ns, prod_rate)
    discount_earth = (1.0 + r) ** (-t_n_earth)
    earth_cum = np_cs(earth_units * discount_earth)

    from numpy import maximum as np_max
    for tau_ops, g in [(0.5, 0.3), (0.5, 0.7), (1.0, 0.5)]:
        # ISRU side: fraction g of ops cost paid tau_ops years earlier
        ops = isru_ops_cost(ns, BASELINE)
        t_n_isru = utp(ns, prod_rate, BASELINE["t0"], k_ramp)
        t_early = np_max(t_n_isru - tau_ops, 0.0)

        # Split: g fraction at t_early, (1-g) at t_n_isru
        disc_early = (1.0 + r) ** (-t_early)
        disc_normal = (1.0 + r) ** (-t_n_isru)
        ops_npv = g * ops * disc_early + (1.0 - g) * ops * disc_normal

        isru_cum = BASELINE["K"] + np_cs(ops_npv)
        diff = isru_cum - earth_cum
        crossings = np_w(diff <= 0)[0]
        cross = int(ns[crossings[0]]) if len(crossings) > 0 else 20000
        shift = cross - base_npv
        pct = shift / base_npv * 100
        print(f"    tau={tau_ops:.1f}yr, g={g:.0%} pre-purchase:  N* = {cross:,} "
              f"(shift: {shift:+,}, {pct:+.1f}%)")


# ---------------------------------------------------------------------------
# U3: Earth launch throughput cap sensitivity
# ---------------------------------------------------------------------------
def print_throughput_cap_sensitivity():
    """U3: Sweep Earth delivery rate cap and report crossover shift."""
    base_npv = find_crossover_npv(BASELINE)

    print(f"\n  U3: Earth launch throughput cap sensitivity (NPV, r=5%):")
    print(f"  {'Cap (units/yr)':>16s}  {'N*':>8s}  {'Shift':>8s}  {'Note':>35s}")
    print(f"  {'----------------':>16s}  {'--------':>8s}  {'--------':>8s}  {'-----------------------------------':>35s}")

    configs = [
        (None, "(no cap, baseline)"),
        (27000, "(~50M tonnes/yr, ~500 Starship/yr)"),
        (10000, "(~18.5M tonnes/yr, ~185 Starship/yr)"),
        (5000, "(~9.25M tonnes/yr, ~93 Starship/yr)"),
        (2000, "(~3.7M tonnes/yr, ~37 Starship/yr)"),
    ]

    for cap, note in configs:
        p = BASELINE.copy()
        if cap is not None:
            p["earth_max_units_per_year"] = cap
        cross = find_crossover(p, n_max=40000, discount=True)
        shift = cross - base_npv
        cap_label = f"{cap:,}" if cap else "Unlimited"
        if cross >= 40000:
            print(f"  {cap_label:>16s}  {'>40,000':>8s}  {'N/A':>8s}  {note:>35s}")
        else:
            print(f"  {cap_label:>16s}  {cross:>8,d}  {shift:>+8,d}  {note:>35s}")


# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# W3: Independent p_fuel sensitivity (total launch cost varies)
# ---------------------------------------------------------------------------
def print_pfuel_independent_sensitivity():
    """W3: Sweep p_fuel while holding p_ops fixed — total launch cost varies."""
    base_npv = find_crossover_npv(BASELINE)

    print(f"\n  W3: Independent p_fuel sensitivity (p_ops=$800 fixed, NPV, r=5%):")
    print(f"  {'p_fuel':>8s}  {'p_ops':>8s}  {'total':>8s}  {'N*':>8s}  {'Shift':>8s}")
    print(f"  {'--------':>8s}  {'--------':>8s}  {'--------':>8s}  {'--------':>8s}  {'--------':>8s}")

    for p_fuel in [50, 100, 200, 400]:
        p = BASELINE.copy()
        p["p_fuel"] = p_fuel
        p["p_ops_launch"] = 800  # held fixed
        # Total first-unit launch cost = p_fuel + p_ops = varies
        cross = find_crossover_npv(p)
        shift = cross - base_npv
        total = p_fuel + 800
        if cross >= 40000:
            print(f"  {p_fuel:>7d}$  {800:>7d}$  {total:>7d}$  {'>40,000':>8s}  {'N/A':>8s}")
        else:
            print(f"  {p_fuel:>7d}$  {800:>7d}$  {total:>7d}$  {cross:>8,d}  {shift:>+8,d}")


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
    print_earth_ramp_robustness()
    print_cfloor_threshold()
    print_prod_rate_sensitivity()

    # Version G diagnostics
    print_launch_learning_sweep()
    print_mc_convergence()
    print_cumulative_economics_npv()
    print_copula_rho_sensitivity()
    print_rate_dependent_learning()
    print_vitamin_sensitivity()
    fig_production_schedule()

    # Version H diagnostics
    fig_convergence_curve()
    print_k_prodrate_correlation()
    print_piecewise_schedule_test()
    print_cashflow_timing_test()

    # Version I diagnostics
    print_earth_capex_sensitivity()
    print_cfloor_failure_threshold()
    print_additional_correlations()
    print_revenue_breakeven()
    print_no_launch_learning_sensitivity()
    print_fuel_floor_sensitivity()
    print_risk_premium_sensitivity()

    # Version M diagnostics
    print_launches_per_unit_sensitivity()
    print_maintenance_sensitivity()
    print_success_probability()
    print_commercial_rate()
    print_capex_coupling()

    # Version N diagnostics
    print_earth_mfg_floor_sensitivity()
    print_lognormal_k_comparison()
    print_kaplan_meier_diagnostic()
    print_k_ramp_sensitivity()
    print_revenue_breakeven_with_lifetime()

    # Version O diagnostics
    print_ps_min_vs_horizon()
    print_availability_sensitivity()

    # Version U diagnostics
    print_throughput_cap_sensitivity()

    # Version V diagnostics
    print_pioneering_phase_sensitivity()
    print_qa_cost_sensitivity()
    print_isru_ops_timing_sensitivity()

    # Version W diagnostics
    print_pfuel_independent_sensitivity()

    print(f"\nDone. All figures saved to {fig_dir}")
