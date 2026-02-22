#!/usr/bin/env python3
"""Generate publication-quality figures for the Multi-Model AI Consensus paper.

Loads all multi-model deliberation transcripts via ``deliberation_analysis``,
computes convergence statistics, voting dynamics, and per-model profiles, then
produces 8 PDF figures for Paper 03.

Figures:
  1. fig-rounds-by-category.pdf   -- Mean rounds to convergence by category
  2. fig-vote-distribution.pdf    -- Stacked APPROVE/NEUTRAL/REJECT per round
  3. fig-convergence-scatter.pdf  -- Rounds to convergence by category & phase
  4. fig-self-peer-vote.pdf       -- Self-vote vs peer-vote score scatter
  5. fig-model-profiles.pdf       -- Three-panel model voting profiles
  6. fig-system-architecture.pdf  -- Deliberation protocol flowchart
  7. fig-word-count-distribution.pdf -- Box plot of response word counts
  8. fig-termination-voting.pdf   -- CONCLUDE vs CONTINUE votes per model

Usage:
    source publications/scripts/.venv/bin/activate
    python publications/scripts/generate_consensus_figures.py
"""

from __future__ import annotations

__version__ = "1.0.0"

import time
from collections import defaultdict
from os import environ, makedirs
from os.path import abspath, dirname, join

import numpy as np
from matplotlib import use as mpl_use

mpl_use("Agg")

from matplotlib.pyplot import close, rcParams, subplots  # noqa: E402
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from scipy import stats as sp_stats  # noqa: E402

from deliberation_analysis import (  # noqa: E402
    Discussion,
    ModelVotingProfile,
    MODELS,
    VOTE_NUMERIC,
    compute_convergence_stats,
    compute_voting_dynamics,
    load_all_discussions,
)

# ---------------------------------------------------------------------------
# Output directory
# ---------------------------------------------------------------------------
script_dir = dirname(abspath(__file__))
fig_dir = environ.get(
    "CONSENSUS_FIG_DIR",
    join(script_dir, "..", "drafts", "03-multi-model-ai-consensus", "figures"),
)
makedirs(fig_dir, exist_ok=True)

# ---------------------------------------------------------------------------
# Publication style
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
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.05,
        "axes.grid": True,
        "grid.alpha": 0.3,
        "grid.linewidth": 0.5,
    }
)

# ---------------------------------------------------------------------------
# Color schemes
# ---------------------------------------------------------------------------
# Vote colors
c_approve = "#22c55e"  # green
c_neutral = "#eab308"  # gold
c_reject = "#ef4444"  # red

# Phase colors
c_phase0 = "#3b82f6"  # blue
c_phase1 = "#f97316"  # orange
c_phase2 = "#22c55e"  # green
PHASE_COLORS = {
    "phase-0": c_phase0,
    "phase-1": c_phase1,
    "phase-2": c_phase2,
    "phase-3a": "#a855f7",  # purple
}

# Model colors
c_claude = "#3b82f6"  # blue
c_gemini = "#f97316"  # orange
c_gpt = "#22c55e"  # green
MODEL_COLORS = {
    "claude-opus-4-6": c_claude,
    "gemini-3-pro": c_gemini,
    "gpt-5-2": c_gpt,
}
MODEL_LABELS = {
    "claude-opus-4-6": "Claude",
    "gemini-3-pro": "Gemini",
    "gpt-5-2": "GPT",
}

# Category ordering
CATEGORY_ORDER = ["governance", "economic", "technical-systems", "certification"]
CATEGORY_LABELS = {
    "governance": "Governance",
    "economic": "Economic",
    "technical-systems": "Technical",
    "certification": "Certification",
}


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def _save(fig, name: str) -> None:
    """Save figure to fig_dir and close it."""
    path = join(fig_dir, name)
    fig.savefig(path)
    close(fig)
    print(f"  Saved: {path}")


# ---------------------------------------------------------------------------
# Figure 1: Rounds by Category (grouped bar with jittered dots)
# ---------------------------------------------------------------------------


def fig_rounds_by_category(discussions: list[Discussion]) -> None:
    """Grouped bar chart showing mean rounds to convergence per category.

    Individual data points are overlaid as jittered dots.  Error bars are
    included for categories with n > 1.

    Parameters
    ----------
    discussions:
        All loaded discussions.
    """
    cat_rounds: dict[str, list[int]] = defaultdict(list)
    for d in discussions:
        cat_rounds[d.category].append(d.total_rounds)

    categories = [c for c in CATEGORY_ORDER if c in cat_rounds]
    means = [float(np.mean(cat_rounds[c])) for c in categories]
    stds = [
        float(np.std(cat_rounds[c], ddof=1)) if len(cat_rounds[c]) > 1 else 0.0
        for c in categories
    ]
    labels = [CATEGORY_LABELS.get(c, c) for c in categories]

    fig, ax = subplots(figsize=(7, 4.5))
    x = np.arange(len(categories))
    bar_width = 0.5
    bars = ax.bar(
        x,
        means,
        bar_width,
        color=[c_phase0, c_phase1, c_gpt, "#a855f7"],
        alpha=0.7,
        edgecolor="black",
        linewidth=0.5,
        yerr=stds,
        capsize=4,
        error_kw={"linewidth": 1.0},
        zorder=2,
    )

    # Overlay jittered individual data points
    rng = np.random.default_rng(42)
    for i, cat in enumerate(categories):
        pts = cat_rounds[cat]
        jitter = rng.uniform(-0.15, 0.15, size=len(pts))
        ax.scatter(
            x[i] + jitter,
            pts,
            color="black",
            alpha=0.5,
            s=25,
            zorder=3,
            edgecolors="white",
            linewidths=0.5,
        )

    # Add count labels above bars
    for i, (m, n) in enumerate(zip(means, [len(cat_rounds[c]) for c in categories])):
        ax.text(
            x[i],
            m + stds[i] + 0.15,
            f"n={n}",
            ha="center",
            va="bottom",
            fontsize=8,
            fontstyle="italic",
        )

    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel("Rounds to Convergence")
    ax.set_title("Mean Rounds to Convergence by Question Category")
    ax.set_ylim(bottom=0)
    ax.grid(axis="y", alpha=0.3)
    ax.grid(axis="x", visible=False)

    _save(fig, "fig-rounds-by-category.pdf")


# ---------------------------------------------------------------------------
# Figure 2: Vote Distribution (stacked bar per round)
# ---------------------------------------------------------------------------


def fig_vote_distribution(discussions: list[Discussion]) -> None:
    """Stacked bar chart showing APPROVE/NEUTRAL/REJECT counts per round.

    Uses green/gold/red color scheme.  Total vote count is labelled on each bar.

    Parameters
    ----------
    discussions:
        All loaded discussions.
    """
    round_counts: dict[int, dict[str, int]] = defaultdict(
        lambda: {"APPROVE": 0, "NEUTRAL": 0, "REJECT": 0}
    )
    for d in discussions:
        for r in d.rounds:
            for v in r.votes:
                if v.vote in round_counts[r.round_number]:
                    round_counts[r.round_number][v.vote] += 1

    if not round_counts:
        print("  WARNING: no votes found, skipping fig-vote-distribution.pdf")
        return

    rounds_sorted = sorted(round_counts.keys())
    approves = [round_counts[rn]["APPROVE"] for rn in rounds_sorted]
    neutrals = [round_counts[rn]["NEUTRAL"] for rn in rounds_sorted]
    rejects = [round_counts[rn]["REJECT"] for rn in rounds_sorted]
    totals = [a + n + r for a, n, r in zip(approves, neutrals, rejects)]

    fig, ax = subplots(figsize=(6, 4.5))
    x = np.arange(len(rounds_sorted))
    bar_width = 0.5

    ax.bar(
        x,
        approves,
        bar_width,
        label="APPROVE",
        color=c_approve,
        edgecolor="black",
        linewidth=0.5,
    )
    ax.bar(
        x,
        neutrals,
        bar_width,
        bottom=approves,
        label="NEUTRAL",
        color=c_neutral,
        edgecolor="black",
        linewidth=0.5,
    )
    bottoms_reject = [a + n for a, n in zip(approves, neutrals)]
    ax.bar(
        x,
        rejects,
        bar_width,
        bottom=bottoms_reject,
        label="REJECT",
        color=c_reject,
        edgecolor="black",
        linewidth=0.5,
    )

    # Total vote count labels
    for i, total in enumerate(totals):
        ax.text(
            x[i],
            total + 1,
            str(total),
            ha="center",
            va="bottom",
            fontsize=8,
            fontweight="bold",
        )

    ax.set_xticks(x)
    ax.set_xticklabels([f"Round {rn}" for rn in rounds_sorted])
    ax.set_ylabel("Vote Count")
    ax.set_title("Vote Distribution by Round")
    ax.legend(loc="upper right")
    ax.set_ylim(bottom=0)
    ax.grid(axis="y", alpha=0.3)
    ax.grid(axis="x", visible=False)

    _save(fig, "fig-vote-distribution.pdf")


# ---------------------------------------------------------------------------
# Figure 3: Convergence Scatter
# ---------------------------------------------------------------------------


def fig_convergence_scatter(discussions: list[Discussion]) -> None:
    """Scatter plot of rounds to convergence by category and phase.

    x-axis is question category (jittered), y-axis is rounds to convergence.
    Color encodes phase.  Horizontal lines show the mean per category.

    Parameters
    ----------
    discussions:
        All loaded discussions.
    """
    cat_indices = {c: i for i, c in enumerate(CATEGORY_ORDER)}
    categories_present = sorted(
        {d.category for d in discussions}, key=lambda c: CATEGORY_ORDER.index(c)
    )

    fig, ax = subplots(figsize=(7, 4.5))
    rng = np.random.default_rng(99)

    # Per-category collection for mean lines
    cat_rounds: dict[str, list[int]] = defaultdict(list)

    for d in discussions:
        if d.category not in cat_indices:
            continue
        cx = cat_indices[d.category]
        jitter = rng.uniform(-0.2, 0.2)
        color = PHASE_COLORS.get(d.phase_id, "#888888")
        ax.scatter(
            cx + jitter,
            d.total_rounds,
            color=color,
            s=50,
            edgecolors="black",
            linewidths=0.5,
            zorder=3,
        )
        cat_rounds[d.category].append(d.total_rounds)

    # Mean horizontal lines
    for cat in categories_present:
        if cat not in cat_indices:
            continue
        cx = cat_indices[cat]
        mean_val = float(np.mean(cat_rounds[cat]))
        ax.hlines(
            mean_val,
            cx - 0.35,
            cx + 0.35,
            colors="black",
            linewidths=1.5,
            linestyles="--",
            zorder=4,
        )

    ax.set_xticks(range(len(CATEGORY_ORDER)))
    ax.set_xticklabels([CATEGORY_LABELS.get(c, c) for c in CATEGORY_ORDER])
    ax.set_ylabel("Rounds to Convergence")
    ax.set_title("Convergence by Category and Phase")

    # Legend for phases
    phase_handles = []
    for phase, color in PHASE_COLORS.items():
        if any(d.phase_id == phase for d in discussions):
            label = phase.replace("phase-", "Phase ").replace("3a", "3A")
            phase_handles.append(
                Line2D(
                    [0],
                    [0],
                    marker="o",
                    color="w",
                    markerfacecolor=color,
                    markeredgecolor="black",
                    markersize=8,
                    label=label,
                )
            )
    phase_handles.append(
        Line2D(
            [0],
            [0],
            color="black",
            linewidth=1.5,
            linestyle="--",
            label="Category mean",
        )
    )
    ax.legend(handles=phase_handles, loc="upper right")
    ax.set_ylim(bottom=0)
    ax.grid(axis="y", alpha=0.3)
    ax.grid(axis="x", visible=False)

    _save(fig, "fig-convergence-scatter.pdf")


# ---------------------------------------------------------------------------
# Figure 4: Self-vote vs Peer-vote Score Scatter
# ---------------------------------------------------------------------------


def fig_self_peer_vote(discussions: list[Discussion]) -> None:
    """Scatter of mean self-vote score vs mean peer-vote score per (model, discussion).

    Includes a diagonal identity line, per-model regression line, and
    Pearson r-value annotation.

    Parameters
    ----------
    discussions:
        All loaded discussions.
    """
    # Collect (model, discussion) -> (self_scores, peer_scores)
    points: dict[str, list[tuple[float, float]]] = defaultdict(list)

    for d in discussions:
        # Aggregate per model across all rounds in this discussion
        model_self: dict[str, list[float]] = defaultdict(list)
        model_peer: dict[str, list[float]] = defaultdict(list)
        for r in d.rounds:
            for v in r.votes:
                if v.is_self_vote:
                    model_self[v.target_id].append(float(v.numeric_value))
                else:
                    model_peer[v.target_id].append(float(v.numeric_value))
        for model in MODELS:
            if model in model_self and model in model_peer:
                mean_self = float(np.mean(model_self[model]))
                mean_peer = float(np.mean(model_peer[model]))
                points[model].append((mean_self, mean_peer))

    fig, ax = subplots(figsize=(5.5, 5.5))

    # Identity line
    ax.plot([0, 2], [0, 2], "k--", alpha=0.3, linewidth=1, label="Identity line")

    all_self = []
    all_peer = []
    for model in MODELS:
        if model not in points:
            continue
        sx = [p[0] for p in points[model]]
        py = [p[1] for p in points[model]]
        all_self.extend(sx)
        all_peer.extend(py)
        ax.scatter(
            sx,
            py,
            color=MODEL_COLORS[model],
            label=MODEL_LABELS[model],
            s=40,
            alpha=0.6,
            edgecolors="black",
            linewidths=0.3,
            zorder=3,
        )

    # Overall regression line
    if len(all_self) >= 3:
        slope, intercept, r_value, p_value, _ = sp_stats.linregress(
            all_self, all_peer
        )
        x_line = np.linspace(0, 2, 100)
        y_line = slope * x_line + intercept
        ax.plot(x_line, y_line, "r-", linewidth=1.5, alpha=0.7, label="Regression")
        ax.text(
            0.05,
            0.95,
            f"r = {r_value:.3f}  (p = {p_value:.3f})",
            transform=ax.transAxes,
            fontsize=9,
            verticalalignment="top",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="wheat", alpha=0.5),
        )

    ax.set_xlabel("Mean Self-Vote Score")
    ax.set_ylabel("Mean Peer-Vote Score")
    ax.set_title("Self-Vote vs Peer-Vote Score per Model per Discussion")
    ax.set_xlim(-0.1, 2.1)
    ax.set_ylim(-0.1, 2.1)
    ax.set_aspect("equal")
    ax.legend(loc="lower right", fontsize=8)
    ax.grid(alpha=0.3)

    _save(fig, "fig-self-peer-vote.pdf")


# ---------------------------------------------------------------------------
# Figure 5: Model Profiles (three-panel)
# ---------------------------------------------------------------------------


def fig_model_profiles(discussions: list[Discussion]) -> None:
    """Three-subplot panel (one per model) showing voting profile summary.

    Each subplot contains a stacked horizontal bar with APPROVE/NEUTRAL/REJECT
    given, wins count, and average weighted score.

    Parameters
    ----------
    discussions:
        All loaded discussions.
    """
    vd = compute_voting_dynamics(discussions)

    fig, axes = subplots(1, 3, figsize=(12, 4), sharey=False)

    for idx, model in enumerate(MODELS):
        ax = axes[idx]
        mp = vd.per_model.get(model)
        if mp is None:
            ax.set_visible(False)
            continue

        label = MODEL_LABELS[model]
        color = MODEL_COLORS[model]

        # Stacked horizontal bar for vote distribution
        categories = ["Votes\nGiven"]
        ax.barh(
            categories,
            mp.approves_given,
            color=c_approve,
            edgecolor="black",
            linewidth=0.5,
            label="APPROVE",
            height=0.4,
        )
        ax.barh(
            categories,
            mp.neutrals_given,
            left=mp.approves_given,
            color=c_neutral,
            edgecolor="black",
            linewidth=0.5,
            label="NEUTRAL",
            height=0.4,
        )
        ax.barh(
            categories,
            mp.rejects_given,
            left=mp.approves_given + mp.neutrals_given,
            color=c_reject,
            edgecolor="black",
            linewidth=0.5,
            label="REJECT",
            height=0.4,
        )

        # Text annotations
        total = mp.total_votes_given
        text_lines = [
            f"Wins: {mp.wins}  ({mp.win_rate * 100:.1f}%)",
            f"Avg weighted score: {mp.avg_weighted_score_received:.2f}",
            f"Approve rate: {mp.approve_rate * 100:.1f}%",
            f"Self-approve: {mp.self_approve_rate * 100:.1f}%",
            f"Peer-approve: {mp.peer_approve_rate * 100:.1f}%",
        ]
        text_str = "\n".join(text_lines)
        ax.text(
            0.5,
            -0.55,
            text_str,
            transform=ax.transAxes,
            fontsize=8,
            verticalalignment="top",
            horizontalalignment="center",
            family="monospace",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#f0f0f0", alpha=0.8),
        )

        ax.set_title(label, fontsize=12, fontweight="bold", color=color)
        ax.set_xlabel("Vote Count")
        if idx == 0:
            ax.legend(fontsize=7, loc="upper right")
        ax.grid(axis="x", alpha=0.3)
        ax.grid(axis="y", visible=False)

    fig.suptitle("Per-Model Voting Profiles", fontsize=13, fontweight="bold", y=1.02)
    fig.subplots_adjust(bottom=0.35, wspace=0.4)

    _save(fig, "fig-model-profiles.pdf")


# ---------------------------------------------------------------------------
# Figure 6: System Architecture Flowchart
# ---------------------------------------------------------------------------


def fig_system_architecture() -> None:
    """Flowchart diagram of the deliberation protocol.

    Draws: Question Input -> Model Responses (3 parallel) -> Voting Matrix ->
    Score Calculation -> Termination Check -> CONCLUDE/CONTINUE branch.
    Uses matplotlib patches and arrows.
    """
    fig, ax = subplots(figsize=(10, 7))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")
    ax.set_aspect("equal")

    box_kw = dict(
        boxstyle="round,pad=0.3",
        edgecolor="black",
        linewidth=1.2,
    )

    def _box(x, y, w, h, text, color="#e0e7ff", fontsize=9, bold=False):
        """Draw a rounded rectangle with centered text."""
        patch = FancyBboxPatch(
            (x - w / 2, y - h / 2),
            w,
            h,
            boxstyle="round,pad=0.15",
            facecolor=color,
            edgecolor="black",
            linewidth=1.2,
        )
        ax.add_patch(patch)
        weight = "bold" if bold else "normal"
        ax.text(
            x,
            y,
            text,
            ha="center",
            va="center",
            fontsize=fontsize,
            fontweight=weight,
            wrap=True,
        )
        return (x, y)

    def _arrow(start, end, color="black", style="->", lw=1.5):
        """Draw an arrow between two (x,y) points."""
        arrow = FancyArrowPatch(
            start,
            end,
            arrowstyle=style,
            color=color,
            linewidth=lw,
            mutation_scale=15,
            connectionstyle="arc3,rad=0",
        )
        ax.add_patch(arrow)

    # Layout (center column)
    cx = 5.0
    bw, bh = 2.4, 0.6

    # Row 1: Question Input
    _box(cx, 9.0, bw, bh, "Question Input", color="#dbeafe", bold=True)
    _arrow((cx, 9.0 - bh / 2), (cx, 8.0 + bh / 2))

    # Row 2: Model Responses (3 boxes side by side)
    _box(cx, 8.0, 3.2, bh, "Model Responses", color="#dbeafe", fontsize=9, bold=True)
    models_y = 7.0
    model_boxes_x = [3.0, 5.0, 7.0]
    model_names = ["Claude", "Gemini", "GPT"]
    model_colors_list = [c_claude, c_gemini, c_gpt]
    _arrow((cx, 8.0 - bh / 2), (cx, models_y + bh / 2))
    for mx, mn, mc in zip(model_boxes_x, model_names, model_colors_list):
        _box(mx, models_y, 1.6, bh, mn, color=mc + "40", fontsize=9)

    # Arrow from models to voting
    for mx in model_boxes_x:
        _arrow((mx, models_y - bh / 2), (cx, 5.8 + bh / 2))

    # Row 3: Voting Matrix
    _box(cx, 5.8, bw, bh, "Voting Matrix\n(9 votes per round)", color="#fef3c7", fontsize=8)
    _arrow((cx, 5.8 - bh / 2), (cx, 4.8 + bh / 2))

    # Row 4: Score Calculation
    _box(cx, 4.8, bw, bh, "Score Calculation\n(weighted: self=0.5, peer=1.0)", color="#fef3c7", fontsize=8)
    _arrow((cx, 4.8 - bh / 2), (cx, 3.7 + bh / 2))

    # Row 5: Termination Check (diamond-like)
    _box(cx, 3.7, 2.8, 0.7, "Termination Check\n(CONCLUDE / CONTINUE)", color="#fce4ec", fontsize=8, bold=True)

    # Branch left: CONCLUDE
    _arrow((cx - 1.4, 3.7), (1.8, 3.7), color="#16a34a")
    _box(1.5, 3.7, 2.0, bh, "CONCLUDE\n-> Synthesis", color="#dcfce7", fontsize=9, bold=True)

    # Branch right: CONTINUE
    _arrow((cx + 1.4, 3.7), (8.2, 3.7), color="#ef4444")
    _box(8.5, 3.7, 2.0, bh, "CONTINUE\n-> Next Round", color="#fee2e2", fontsize=9, bold=True)

    # Loop arrow from CONTINUE back up to Model Responses
    _arrow((8.5, 3.7 + bh / 2), (8.5, 7.0), color="#ef4444", style="-|>")
    _arrow((8.5, 7.0), (7.0 + 0.8, 7.0), color="#ef4444", style="-|>")

    # Bottom: output
    _arrow((1.5, 3.7 - bh / 2), (1.5, 2.5 + bh / 2), color="#16a34a")
    _box(1.5, 2.5, 2.4, bh, "Conclusion &\nDivergent Views", color="#bbf7d0", fontsize=9)

    ax.set_title(
        "Multi-Model Deliberation Protocol",
        fontsize=13,
        fontweight="bold",
        pad=10,
    )

    _save(fig, "fig-system-architecture.pdf")


# ---------------------------------------------------------------------------
# Figure 7: Word Count Distribution
# ---------------------------------------------------------------------------


def fig_word_count_distribution(discussions: list[Discussion]) -> None:
    """Box plot showing word count distribution per model across all responses.

    Includes median line and mean marker (diamond).

    Parameters
    ----------
    discussions:
        All loaded discussions.
    """
    model_wc: dict[str, list[int]] = defaultdict(list)
    for d in discussions:
        for r in d.rounds:
            for resp in r.responses:
                model_wc[resp.model_id].append(resp.word_count)

    data = []
    labels = []
    colors = []
    for model in MODELS:
        if model in model_wc:
            data.append(model_wc[model])
            labels.append(MODEL_LABELS[model])
            colors.append(MODEL_COLORS[model])

    if not data:
        print("  WARNING: no responses found, skipping fig-word-count-distribution.pdf")
        return

    fig, ax = subplots(figsize=(6, 4.5))

    bp = ax.boxplot(
        data,
        tick_labels=labels,
        patch_artist=True,
        showmeans=True,
        meanprops=dict(
            marker="D",
            markerfacecolor="red",
            markeredgecolor="black",
            markersize=6,
        ),
        medianprops=dict(color="black", linewidth=1.5),
        whiskerprops=dict(linewidth=1.0),
        capprops=dict(linewidth=1.0),
        flierprops=dict(marker="o", markersize=4, alpha=0.5),
    )

    for patch, color in zip(bp["boxes"], colors):
        patch.set_facecolor(color + "60")
        patch.set_edgecolor("black")
        patch.set_linewidth(1.0)

    # Add n= annotation
    for i, wc_list in enumerate(data):
        n = len(wc_list)
        median_val = float(np.median(wc_list))
        ax.text(
            i + 1,
            max(wc_list) + 50,
            f"n={n}",
            ha="center",
            va="bottom",
            fontsize=8,
            fontstyle="italic",
        )

    ax.set_ylabel("Word Count")
    ax.set_title("Response Word Count Distribution by Model")
    ax.grid(axis="y", alpha=0.3)
    ax.grid(axis="x", visible=False)

    # Custom legend for mean marker
    legend_elements = [
        Line2D(
            [0],
            [0],
            marker="D",
            color="w",
            markerfacecolor="red",
            markeredgecolor="black",
            markersize=6,
            label="Mean",
        ),
        Line2D([0], [0], color="black", linewidth=1.5, label="Median"),
    ]
    ax.legend(handles=legend_elements, loc="upper right", fontsize=8)

    _save(fig, "fig-word-count-distribution.pdf")


# ---------------------------------------------------------------------------
# Figure 8: Termination Voting
# ---------------------------------------------------------------------------


def fig_termination_voting(discussions: list[Discussion]) -> None:
    """Grouped bar chart of CONCLUDE vs CONTINUE votes per model.

    Conclude rate is annotated as text on each group.

    Parameters
    ----------
    discussions:
        All loaded discussions.
    """
    conclude_counts: dict[str, int] = defaultdict(int)
    continue_counts: dict[str, int] = defaultdict(int)

    for d in discussions:
        for r in d.rounds:
            for tv in r.termination_votes:
                if tv.vote == "CONCLUDE":
                    conclude_counts[tv.model_id] += 1
                else:
                    continue_counts[tv.model_id] += 1

    models_present = [m for m in MODELS if conclude_counts[m] + continue_counts[m] > 0]
    if not models_present:
        print("  WARNING: no termination votes found, skipping fig-termination-voting.pdf")
        return

    fig, ax = subplots(figsize=(7, 4.5))
    x = np.arange(len(models_present))
    bar_width = 0.3

    conclude_vals = [conclude_counts[m] for m in models_present]
    continue_vals = [continue_counts[m] for m in models_present]

    bars_conclude = ax.bar(
        x - bar_width / 2,
        conclude_vals,
        bar_width,
        label="CONCLUDE",
        color="#16a34a",
        edgecolor="black",
        linewidth=0.5,
    )
    bars_continue = ax.bar(
        x + bar_width / 2,
        continue_vals,
        bar_width,
        label="CONTINUE",
        color="#ef4444",
        edgecolor="black",
        linewidth=0.5,
    )

    # Conclude rate text
    for i, model in enumerate(models_present):
        total = conclude_counts[model] + continue_counts[model]
        rate = conclude_counts[model] / total if total > 0 else 0.0
        max_h = max(conclude_vals[i], continue_vals[i])
        ax.text(
            x[i],
            max_h + 0.8,
            f"{rate * 100:.0f}% conclude",
            ha="center",
            va="bottom",
            fontsize=8,
            fontweight="bold",
        )

    ax.set_xticks(x)
    ax.set_xticklabels([MODEL_LABELS[m] for m in models_present])
    ax.set_ylabel("Vote Count")
    ax.set_title("Termination Voting by Model")
    ax.legend(loc="upper right")
    ax.set_ylim(bottom=0)
    ax.grid(axis="y", alpha=0.3)
    ax.grid(axis="x", visible=False)

    _save(fig, "fig-termination-voting.pdf")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    """Entry point: load data, generate all 8 figures, print timing."""
    t0 = time.time()

    script_dir_local = dirname(abspath(__file__))
    base_dir = join(
        script_dir_local, "..", "..", "src", "content", "research-questions"
    )

    print(f"Loading discussions from: {abspath(base_dir)}")
    discussions = load_all_discussions(base_dir)
    print(f"Loaded {len(discussions)} discussions.\n")

    if not discussions:
        print("ERROR: No discussions found. Check base_dir path.")
        return

    print("Generating figures...")
    fig_rounds_by_category(discussions)
    fig_vote_distribution(discussions)
    fig_convergence_scatter(discussions)
    fig_self_peer_vote(discussions)
    fig_model_profiles(discussions)
    fig_system_architecture()
    fig_word_count_distribution(discussions)
    fig_termination_voting(discussions)

    elapsed = time.time() - t0
    print(f"\nAll 8 figures generated in {elapsed:.1f}s.")
    print(f"Output directory: {abspath(fig_dir)}")


if __name__ == "__main__":
    main()
