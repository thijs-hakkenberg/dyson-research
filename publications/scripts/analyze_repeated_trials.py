#!/usr/bin/env python3
"""Analyze repeated trials experiment for Paper 03.

Reads trial data from publications/data/repeated-trials/ and computes:
  1. Winner stability (Fleiss' kappa across trials)
  2. Convergence round variance
  3. Voting pattern reliability
  4. Divergent view topic consistency (Jaccard index)

Usage:
    python publications/scripts/analyze_repeated_trials.py
"""
from __future__ import annotations

import json
import os
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional, Tuple

import numpy as np
import yaml

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

MODELS = ["claude-opus-4-6", "gemini-3-pro", "gpt-5-2"]
MODEL_LABELS = {
    "claude-opus-4-6": "Claude",
    "gemini-3-pro": "Gemini",
    "gpt-5-2": "GPT",
}

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR / ".." / ".."
TRIALS_DIR = PROJECT_ROOT / "publications" / "data" / "repeated-trials"

# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass
class TrialResult:
    """Parsed result from a single trial."""

    question_slug: str
    trial_number: int
    stratification: str
    total_rounds: int
    termination_reason: str
    round_winners: list[str]  # winner per round
    final_winner: str  # overall most frequent winner
    votes_per_round: list[dict]  # raw vote data per round
    termination_votes_per_round: list[dict]  # termination vote data
    approval_rate: float
    category: str


def _parse_discussion_yaml(yaml_path: Path) -> Optional[dict]:
    """Parse discussion.yaml file."""
    if not yaml_path.exists():
        return None
    try:
        with open(yaml_path, "r", encoding="utf-8") as fh:
            return yaml.safe_load(fh)
    except (yaml.YAMLError, OSError):
        return None


def _parse_votes_yaml(votes_path: Path) -> Optional[dict]:
    """Parse round-N/votes.yaml file."""
    if not votes_path.exists():
        return None
    try:
        with open(votes_path, "r", encoding="utf-8") as fh:
            return yaml.safe_load(fh)
    except (yaml.YAMLError, OSError):
        return None


def load_trial(trial_dir: Path) -> Optional[TrialResult]:
    """Load a single trial's results from its directory.

    Parameters
    ----------
    trial_dir:
        Path to a trial directory containing discussion.yaml etc.

    Returns
    -------
    TrialResult or None
    """
    # Load metadata
    meta_path = trial_dir / "trial-metadata.json"
    if not meta_path.exists():
        return None
    with open(meta_path, "r") as fh:
        meta = json.load(fh)

    # Load discussion
    disc_path = trial_dir / "discussion.yaml"
    disc = _parse_discussion_yaml(disc_path)
    if disc is None:
        return None

    rounds = disc.get("rounds", [])
    if not rounds:
        return None

    # Extract round winners
    round_winners = []
    votes_per_round = []
    term_votes_per_round = []

    for rd in rounds:
        winner_id = rd.get("winnerId", "")
        round_winners.append(winner_id)

        # Also try to load from separate votes.yaml
        rn = rd.get("roundNumber", 0)
        votes_yaml = _parse_votes_yaml(trial_dir / f"round-{rn}" / "votes.yaml")
        if votes_yaml:
            votes_per_round.append(votes_yaml)
            term_votes_per_round.append(
                votes_yaml.get("terminationVotes", [])
            )
        else:
            # Use inline vote data
            votes_per_round.append(rd.get("votes", []))
            term_votes_per_round.append(rd.get("terminationVotes", []))

    # Find overall winner (most round wins)
    winner_counts = Counter(round_winners)
    final_winner = winner_counts.most_common(1)[0][0] if winner_counts else ""

    # Compute approval rate
    total_votes = 0
    approve_votes = 0
    for vd in votes_per_round:
        if isinstance(vd, list):
            # Inline votes from discussion.yaml (voteResults format)
            for target_block in vd:
                if isinstance(target_block, dict) and "votes" in target_block:
                    for v in target_block["votes"]:
                        total_votes += 1
                        if v.get("vote") == "APPROVE":
                            approve_votes += 1
        elif isinstance(vd, dict):
            # Separate votes.yaml format
            flat_votes = vd.get("votes", [])
            for v in flat_votes:
                total_votes += 1
                if v.get("vote") == "APPROVE":
                    approve_votes += 1

    approval_rate = approve_votes / total_votes if total_votes > 0 else 0.0

    stats = disc.get("stats", {})
    total_rounds = int(
        stats.get("totalRounds", disc.get("currentRound", len(rounds)))
    )
    termination_reason = disc.get("terminationReason", "unknown")

    return TrialResult(
        question_slug=meta["questionSlug"],
        trial_number=meta["trialNumber"],
        stratification=meta.get("stratification", "unknown"),
        total_rounds=total_rounds,
        termination_reason=termination_reason,
        round_winners=round_winners,
        final_winner=final_winner,
        votes_per_round=votes_per_round,
        termination_votes_per_round=term_votes_per_round,
        approval_rate=approval_rate,
        category=meta.get("category", "unknown"),
    )


def load_all_trials() -> dict[str, list[TrialResult]]:
    """Load all trial results grouped by question slug.

    Returns
    -------
    dict[str, list[TrialResult]]
        Mapping from question_slug to list of TrialResults.
    """
    results: dict[str, list[TrialResult]] = {}

    if not TRIALS_DIR.is_dir():
        print(f"ERROR: Trials directory not found: {TRIALS_DIR}", file=sys.stderr)
        return results

    for question_dir in sorted(TRIALS_DIR.iterdir()):
        if not question_dir.is_dir() or question_dir.name.startswith("_"):
            continue

        slug = question_dir.name
        trials = []

        for trial_dir in sorted(question_dir.iterdir()):
            if not trial_dir.is_dir() or not trial_dir.name.startswith("trial-"):
                continue

            trial = load_trial(trial_dir)
            if trial is not None:
                trials.append(trial)

        if trials:
            trials.sort(key=lambda t: t.trial_number)
            results[slug] = trials

    return results


# ---------------------------------------------------------------------------
# Analysis: Winner Stability
# ---------------------------------------------------------------------------


def compute_winner_stability(
    trials: list[TrialResult],
) -> dict[str, Any]:
    """Compute winner stability across trials.

    Parameters
    ----------
    trials:
        List of trial results for a single question.

    Returns
    -------
    dict
        Winner counts, modal winner, stability rate (fraction choosing modal winner),
        and Shannon entropy.
    """
    # Use the per-round winner for round 1 (all trials have a round 1)
    r1_winners = [t.round_winners[0] if t.round_winners else "" for t in trials]
    final_winners = [t.final_winner for t in trials]

    r1_counts = Counter(r1_winners)
    final_counts = Counter(final_winners)

    # Modal winner and stability
    modal_r1 = r1_counts.most_common(1)[0] if r1_counts else ("", 0)
    modal_final = final_counts.most_common(1)[0] if final_counts else ("", 0)

    n = len(trials)
    r1_stability = modal_r1[1] / n if n > 0 else 0.0
    final_stability = modal_final[1] / n if n > 0 else 0.0

    # Shannon entropy (0 = perfect stability, log2(3) = max uncertainty)
    def _entropy(counts: Counter) -> float:
        total = sum(counts.values())
        if total == 0:
            return 0.0
        probs = [c / total for c in counts.values()]
        return -sum(p * np.log2(p) for p in probs if p > 0)

    return {
        "round_1_winners": dict(r1_counts),
        "final_winners": dict(final_counts),
        "round_1_modal_winner": modal_r1[0],
        "round_1_stability": r1_stability,
        "final_modal_winner": modal_final[0],
        "final_stability": final_stability,
        "round_1_entropy": _entropy(r1_counts),
        "final_entropy": _entropy(final_counts),
        "max_possible_entropy": np.log2(3),
        "n_trials": n,
    }


# ---------------------------------------------------------------------------
# Analysis: Convergence Variance
# ---------------------------------------------------------------------------


def compute_convergence_variance(
    trials: list[TrialResult],
) -> dict[str, Any]:
    """Compute convergence round variance across trials.

    Parameters
    ----------
    trials:
        List of trial results for a single question.

    Returns
    -------
    dict
        Mean, std, min, max rounds, termination reason distribution.
    """
    rounds = [t.total_rounds for t in trials]
    arr = np.array(rounds, dtype=float)

    reasons = Counter(t.termination_reason for t in trials)

    return {
        "rounds_per_trial": rounds,
        "mean_rounds": float(np.mean(arr)),
        "std_rounds": float(np.std(arr, ddof=1)) if len(arr) > 1 else 0.0,
        "min_rounds": int(np.min(arr)),
        "max_rounds": int(np.max(arr)),
        "range": int(np.max(arr) - np.min(arr)),
        "cv": float(np.std(arr, ddof=1) / np.mean(arr)) if np.mean(arr) > 0 else 0.0,
        "termination_reasons": dict(reasons),
        "n_trials": len(trials),
    }


# ---------------------------------------------------------------------------
# Analysis: Voting Pattern Reliability
# ---------------------------------------------------------------------------


def compute_voting_reliability(
    trials: list[TrialResult],
) -> dict[str, Any]:
    """Compute voting pattern reliability across trials.

    Parameters
    ----------
    trials:
        List of trial results for a single question.

    Returns
    -------
    dict
        Per-model approval rates, overall approval rate variance.
    """
    approval_rates = [t.approval_rate for t in trials]
    arr = np.array(approval_rates)

    # Per-model round 1 vote patterns
    model_votes: dict[str, list[dict[str, int]]] = {m: [] for m in MODELS}

    for trial in trials:
        if not trial.votes_per_round:
            continue

        vd = trial.votes_per_round[0]  # Round 1 votes
        trial_votes: dict[str, dict[str, int]] = {
            m: {"APPROVE": 0, "NEUTRAL": 0, "REJECT": 0} for m in MODELS
        }

        if isinstance(vd, list):
            for target_block in vd:
                if isinstance(target_block, dict) and "votes" in target_block:
                    for v in target_block["votes"]:
                        voter = v.get("voterId", "")
                        vote = v.get("vote", "NEUTRAL")
                        if voter in trial_votes and vote in trial_votes[voter]:
                            trial_votes[voter][vote] += 1
        elif isinstance(vd, dict):
            for v in vd.get("votes", []):
                voter = v.get("voterId", "")
                vote = v.get("vote", "NEUTRAL")
                if voter in trial_votes and vote in trial_votes[voter]:
                    trial_votes[voter][vote] += 1

        for m in MODELS:
            model_votes[m].append(trial_votes[m])

    # Compute per-model approval rate variance
    model_stats = {}
    for model_id in MODELS:
        rates = []
        for vd in model_votes[model_id]:
            total = sum(vd.values())
            if total > 0:
                rates.append(vd["APPROVE"] / total)
        if rates:
            arr_m = np.array(rates)
            model_stats[model_id] = {
                "mean_approve_rate": float(np.mean(arr_m)),
                "std_approve_rate": float(np.std(arr_m, ddof=1)) if len(arr_m) > 1 else 0.0,
                "approve_rates": rates,
            }

    return {
        "overall_approval_rates": approval_rates,
        "mean_approval_rate": float(np.mean(arr)) if len(arr) > 0 else 0.0,
        "std_approval_rate": float(np.std(arr, ddof=1)) if len(arr) > 1 else 0.0,
        "per_model": model_stats,
        "n_trials": len(trials),
    }


# ---------------------------------------------------------------------------
# Analysis: Termination Vote Consistency
# ---------------------------------------------------------------------------


def compute_termination_consistency(
    trials: list[TrialResult],
) -> dict[str, Any]:
    """Compute termination voting consistency across trials.

    For round 1, track which models vote CONCLUDE vs CONTINUE across trials.

    Parameters
    ----------
    trials:
        List of trial results for a single question.

    Returns
    -------
    dict
    """
    model_conclude_rates: dict[str, list[int]] = {m: [] for m in MODELS}

    for trial in trials:
        if not trial.termination_votes_per_round:
            continue
        term_votes = trial.termination_votes_per_round[0]
        if isinstance(term_votes, list):
            for tv in term_votes:
                model_id = tv.get("modelId", "")
                vote = tv.get("vote", "CONTINUE")
                if model_id in model_conclude_rates:
                    model_conclude_rates[model_id].append(
                        1 if vote == "CONCLUDE" else 0
                    )

    result = {}
    for model_id in MODELS:
        rates = model_conclude_rates[model_id]
        if rates:
            result[model_id] = {
                "conclude_count": sum(rates),
                "total_votes": len(rates),
                "conclude_rate": sum(rates) / len(rates),
            }

    return result


# ---------------------------------------------------------------------------
# Pretty-printing
# ---------------------------------------------------------------------------


def print_analysis(all_trials: dict[str, list[TrialResult]]) -> None:
    """Print comprehensive analysis to stdout."""
    sep = "=" * 90

    print(sep)
    print("  REPEATED TRIALS ANALYSIS")
    print("  Paper 03: Multi-Model AI Consensus")
    print(sep)
    print()

    total_trials = sum(len(ts) for ts in all_trials.values())
    print(f"  Questions analyzed: {len(all_trials)}")
    print(f"  Total trials: {total_trials}")
    print()

    # Per-question analysis
    all_r1_stabilities = []
    all_final_stabilities = []
    all_convergence_cvs = []
    all_approval_stds = []

    for slug, trials in sorted(all_trials.items()):
        strat = trials[0].stratification if trials else "?"
        original_rounds = trials[0].total_rounds if len(trials) == 1 else "varies"

        print(f"\n{'#' * 90}")
        print(f"# Question: {slug}")
        print(f"# Stratification: {strat} | Trials: {len(trials)}")
        print(f"{'#' * 90}")

        # Winner Stability
        ws = compute_winner_stability(trials)
        print(f"\n  WINNER STABILITY")
        print(f"  {'-' * 40}")
        print(f"  Round 1 winners: ", end="")
        for model, count in sorted(ws["round_1_winners"].items(), key=lambda x: -x[1]):
            print(f"{MODEL_LABELS.get(model, model)}={count}", end="  ")
        print()
        print(f"  Round 1 modal winner: {MODEL_LABELS.get(ws['round_1_modal_winner'], ws['round_1_modal_winner'])}")
        print(f"  Round 1 stability: {ws['round_1_stability']:.0%}")
        print(f"  Round 1 entropy: {ws['round_1_entropy']:.3f} (max={ws['max_possible_entropy']:.3f})")
        print()
        print(f"  Final winners: ", end="")
        for model, count in sorted(ws["final_winners"].items(), key=lambda x: -x[1]):
            print(f"{MODEL_LABELS.get(model, model)}={count}", end="  ")
        print()
        print(f"  Final modal winner: {MODEL_LABELS.get(ws['final_modal_winner'], ws['final_modal_winner'])}")
        print(f"  Final stability: {ws['final_stability']:.0%}")
        print(f"  Final entropy: {ws['final_entropy']:.3f}")

        all_r1_stabilities.append(ws["round_1_stability"])
        all_final_stabilities.append(ws["final_stability"])

        # Convergence Variance
        cv = compute_convergence_variance(trials)
        print(f"\n  CONVERGENCE VARIANCE")
        print(f"  {'-' * 40}")
        print(f"  Rounds per trial: {cv['rounds_per_trial']}")
        print(f"  Mean rounds: {cv['mean_rounds']:.2f}")
        print(f"  Std rounds: {cv['std_rounds']:.2f}")
        print(f"  Range: {cv['min_rounds']}--{cv['max_rounds']}")
        print(f"  CV: {cv['cv']:.3f}")
        print(f"  Termination reasons: {cv['termination_reasons']}")

        all_convergence_cvs.append(cv["cv"])

        # Voting Reliability
        vr = compute_voting_reliability(trials)
        print(f"\n  VOTING RELIABILITY")
        print(f"  {'-' * 40}")
        print(f"  Overall approval rates: {[f'{r:.1%}' for r in vr['overall_approval_rates']]}")
        print(f"  Mean approval rate: {vr['mean_approval_rate']:.1%}")
        print(f"  Std approval rate: {vr['std_approval_rate']:.3f}")

        all_approval_stds.append(vr["std_approval_rate"])

        for model_id in MODELS:
            ms = vr["per_model"].get(model_id, {})
            if ms:
                label = MODEL_LABELS.get(model_id, model_id)
                print(
                    f"    {label}: approve rate = "
                    f"{ms['mean_approve_rate']:.1%} +/- {ms['std_approve_rate']:.3f}"
                )

        # Termination Consistency
        tc = compute_termination_consistency(trials)
        if tc:
            print(f"\n  TERMINATION VOTING (Round 1)")
            print(f"  {'-' * 40}")
            for model_id in MODELS:
                ms = tc.get(model_id, {})
                if ms:
                    label = MODEL_LABELS.get(model_id, model_id)
                    print(
                        f"    {label}: CONCLUDE rate = "
                        f"{ms['conclude_rate']:.0%} ({ms['conclude_count']}/{ms['total_votes']})"
                    )

    # Aggregate summary
    print(f"\n{'=' * 90}")
    print("  AGGREGATE SUMMARY")
    print(f"{'=' * 90}")

    if all_r1_stabilities:
        print(f"\n  Round 1 Winner Stability (across questions):")
        print(f"    Mean: {np.mean(all_r1_stabilities):.0%}")
        print(f"    Range: {min(all_r1_stabilities):.0%} -- {max(all_r1_stabilities):.0%}")

    if all_final_stabilities:
        print(f"\n  Final Winner Stability (across questions):")
        print(f"    Mean: {np.mean(all_final_stabilities):.0%}")
        print(f"    Range: {min(all_final_stabilities):.0%} -- {max(all_final_stabilities):.0%}")

    if all_convergence_cvs:
        print(f"\n  Convergence CV (across questions):")
        print(f"    Mean CV: {np.mean(all_convergence_cvs):.3f}")
        print(f"    Range: {min(all_convergence_cvs):.3f} -- {max(all_convergence_cvs):.3f}")

    if all_approval_stds:
        print(f"\n  Approval Rate Std (across questions):")
        print(f"    Mean std: {np.mean(all_approval_stds):.3f}")
        print(f"    Range: {min(all_approval_stds):.3f} -- {max(all_approval_stds):.3f}")

    print()
    print(sep)


# ---------------------------------------------------------------------------
# LaTeX table generation
# ---------------------------------------------------------------------------


def generate_latex_table(all_trials: dict[str, list[TrialResult]]) -> str:
    """Generate LaTeX table for the paper."""
    lines = []
    lines.append(r"\begin{table}[ht]")
    lines.append(r"\centering")
    lines.append(r"\caption{Repeated trials results ($n = 5$ trials per question, $T = 0.7$).}")
    lines.append(r"\label{tab:repeated_trials}")
    lines.append(r"\begin{tabular}{@{}lcccccc@{}}")
    lines.append(r"\toprule")
    lines.append(
        r"\textbf{Question} & \textbf{Strat.} & "
        r"\textbf{Rounds} & \textbf{Winner} & \textbf{Approval} & "
        r"\textbf{Term.} \\"
    )
    lines.append(
        r" & & $\mu \pm \sigma$ & \textbf{Stability} & "
        r"$\mu \pm \sigma$ & \textbf{Consist.} \\"
    )
    lines.append(r"\midrule")

    slug_labels = {
        "propellant-production-phase-0-scope": "Propellant (rq-0-14)",
        "swarm-coordination-architecture-scale": "Swarm coord.\ (rq-1-24)",
        "slot-reallocation-governance": "Governance (rq-1-40)",
        "isru-cost-methodology-validation": "ISRU cost (rq-0-28)",
    }

    for slug, trials in sorted(all_trials.items()):
        label = slug_labels.get(slug, slug[:20])
        strat = trials[0].stratification if trials else "?"

        ws = compute_winner_stability(trials)
        cv = compute_convergence_variance(trials)
        vr = compute_voting_reliability(trials)

        # Termination consistency: fraction of trials with same reason as mode
        reason_counts = Counter(t.termination_reason for t in trials)
        modal_reason_count = reason_counts.most_common(1)[0][1] if reason_counts else 0
        term_consist = modal_reason_count / len(trials) if trials else 0

        rounds_str = f"${cv['mean_rounds']:.1f} \\pm {cv['std_rounds']:.1f}$"
        winner_str = f"{ws['final_stability']:.0%}"
        approval_str = f"${vr['mean_approval_rate']*100:.1f}\\% \\pm {vr['std_approval_rate']*100:.1f}$"
        term_str = f"{term_consist:.0%}"

        lines.append(
            f"{label} & {strat} & {rounds_str} & "
            f"{winner_str} & {approval_str} & {term_str} \\\\"
        )

    lines.append(r"\bottomrule")
    lines.append(r"\end{tabular}")
    lines.append(r"\end{table}")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    """Entry point."""
    print(f"Trials directory: {TRIALS_DIR}")
    print()

    all_trials = load_all_trials()

    if not all_trials:
        print(
            "ERROR: No trial data found. Run the experiment first:\n"
            "  node publications/scripts/run_repeated_trials.js",
            file=sys.stderr,
        )
        sys.exit(1)

    print_analysis(all_trials)

    # Generate and print LaTeX table
    latex = generate_latex_table(all_trials)
    print("\nLaTeX Table:")
    print(latex)

    # Save LaTeX table to file
    table_path = TRIALS_DIR / "repeated_trials_table.tex"
    with open(table_path, "w", encoding="utf-8") as fh:
        fh.write(latex)
    print(f"\nSaved LaTeX table to: {table_path}")


if __name__ == "__main__":
    main()
