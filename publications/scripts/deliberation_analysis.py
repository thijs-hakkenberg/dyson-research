#!/usr/bin/env python3
"""Quantitative analysis of Project Dyson multi-model AI deliberation transcripts.

Parses all deliberation transcripts from the Project Dyson multi-model discussion
system and produces convergence statistics, voting dynamics, per-model tendencies,
and category-level analysis.  Results are printed to stdout and exported as CSV
files for downstream use in Paper 03 (Multi-Model AI Consensus).

Requires: PyYAML, numpy, scipy
"""
from __future__ import annotations

__version__ = "1.0.0"

import csv
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np
import yaml
from scipy import stats as sp_stats

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

VOTE_NUMERIC = {"APPROVE": 2, "NEUTRAL": 1, "REJECT": 0}

MODELS = ["claude-opus-4-6", "gemini-3-pro", "gpt-5-2"]

# Keyword-based category classification
CATEGORY_KEYWORDS: dict[str, list[str]] = {
    "governance": [
        "governance",
        "disposal",
        "authority",
        "reallocation",
        "end-of-life",
        "slot",
        "multi-century",
    ],
    "economic": [
        "cost",
        "economics",
        "isru",
        "feedstock",
        "methodology",
        "roi",
        "threshold",
    ],
    "technical-systems": [
        "architecture",
        "power",
        "propellant",
        "collision",
        "avoidance",
        "coordination",
        "latency",
        "excavation",
        "bucket-wheel",
        "fleet",
    ],
    "certification": [
        "certification",
        "autonomy",
        "assembly",
        "human-rating",
        "repair",
    ],
}

# Canonical discussion directories (some may not exist on disk)
EXPECTED_DIRS: list[str] = [
    "phase-0/rq-0-14-propellant-production-phase-0-scope",
    "phase-0/rq-0-18-human-rating-transport-vehicles",
    "phase-0/rq-0-26-dual-bucket-wheel-excavation",
    "phase-0/rq-0-28-isru-cost-methodology-validation",
    "phase-0/rq-0-29-multi-century-governance-structure",
    "phase-1/rq-1-11-swarm-power-architecture-end-use",
    "phase-1/rq-1-16-autonomous-assembly-certification",
    "phase-1/rq-1-21-feedstock-acquisition-isru-timeline",
    "phase-1/rq-1-24-swarm-coordination-architecture-scale",
    "phase-1/rq-1-33-tug-end-of-life-disposal",
    "phase-1/rq-1-40-slot-reallocation-governance",
    "phase-1/rq-1-42-node-end-of-life-disposal",
    "phase-2/rq-2-3-billion-unit-collision-avoidance",
    "phase-2/rq-2-8-autonomous-repair-authority-limits",
    "phase-2/rq-2-17-fleet-coordination-scale-constraints",
    "phase-2/rq-2-20-swarm-roi-threshold-humanity-power-needs",
    "phase-3a/rq-3a-3-inter-layer-latency-consensus-protocols",
]

# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass
class Vote:
    """A single vote cast by one model evaluating another model's response."""

    voter_id: str
    target_id: str
    vote: str  # APPROVE | NEUTRAL | REJECT
    reasoning: str
    is_self_vote: bool
    numeric_value: int  # APPROVE=2, NEUTRAL=1, REJECT=0


@dataclass
class TerminationVote:
    """A model's vote on whether the discussion should end."""

    model_id: str
    vote: str  # CONCLUDE | CONTINUE
    reasoning: str


@dataclass
class Response:
    """A single model response within a discussion round."""

    model_id: str
    content: str
    word_count: int


@dataclass
class RoundResult:
    """Aggregated data for one round of deliberation."""

    round_number: int
    responses: list[Response]
    votes: list[Vote]
    termination_votes: list[TerminationVote]
    winner_id: str
    winner_score: float


@dataclass
class Discussion:
    """Complete parsed discussion including all rounds, votes, and metadata."""

    question_id: str
    question_slug: str
    question_title: str
    phase_id: str
    config: dict[str, Any]
    status: str
    rounds: list[RoundResult]
    total_rounds: int
    termination_reason: str
    conclusion_generated_by: str
    category: str  # governance | economic | technical-systems | certification


# ---------------------------------------------------------------------------
# Result containers
# ---------------------------------------------------------------------------


@dataclass
class ConvergenceStats:
    """Aggregate convergence statistics across all discussions."""

    rounds_per_discussion: list[int]
    mean_rounds: float
    median_rounds: float
    std_rounds: float
    ci_95_lower: float
    ci_95_upper: float
    convergence_by_category: dict[str, float]
    termination_reason_distribution: dict[str, int]


@dataclass
class ModelVotingProfile:
    """Per-model breakdown of voting behaviour."""

    model_id: str
    total_votes_given: int
    approves_given: int
    neutrals_given: int
    rejects_given: int
    approve_rate: float
    neutral_rate: float
    reject_rate: float
    self_approve_rate: float
    peer_approve_rate: float
    wins: int
    win_rate: float
    avg_weighted_score_received: float


@dataclass
class VotingDynamics:
    """Aggregate voting statistics across all discussions."""

    total_votes: int
    approve_count: int
    neutral_count: int
    reject_count: int
    approve_rate: float
    neutral_rate: float
    reject_rate: float
    self_vote_approve_rate: float
    peer_vote_approve_rate: float
    self_peer_score_correlation_pearson: float
    self_peer_score_correlation_spearman: float
    self_peer_pearson_pvalue: float
    self_peer_spearman_pvalue: float
    per_round_approve_rates: dict[int, float]
    per_model: dict[str, ModelVotingProfile]


# ---------------------------------------------------------------------------
# Category classification
# ---------------------------------------------------------------------------


def classify_question(title: str, slug: str) -> str:
    """Classify a discussion question into a thematic category.

    Uses keyword matching against the question title and slug.  If multiple
    categories match, the one with the most keyword hits wins.  Falls back
    to ``'technical-systems'`` when no keywords match.

    Parameters
    ----------
    title:
        Human-readable question title.
    slug:
        URL-safe question slug.

    Returns
    -------
    str
        One of ``'governance'``, ``'economic'``, ``'technical-systems'``,
        or ``'certification'``.
    """
    combined = (title + " " + slug).lower()
    scores: dict[str, int] = {}
    for category, keywords in CATEGORY_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in combined)
        if score > 0:
            scores[category] = score
    if not scores:
        return "technical-systems"
    return max(scores, key=lambda c: scores[c])


# ---------------------------------------------------------------------------
# Data loading helpers
# ---------------------------------------------------------------------------


def _parse_votes_from_flat_list(raw_votes: list[dict]) -> list[Vote]:
    """Parse a flat list of vote dicts (as found in round-N/votes.yaml ``votes`` key).

    Parameters
    ----------
    raw_votes:
        List of dicts each with ``voterId``, ``targetId``, ``vote``, ``reasoning``.

    Returns
    -------
    list[Vote]
    """
    results: list[Vote] = []
    for v in raw_votes:
        voter = v.get("voterId", "")
        target = v.get("targetId", "")
        vote_str = v.get("vote", "NEUTRAL")
        reasoning = v.get("reasoning", "")
        results.append(
            Vote(
                voter_id=voter,
                target_id=target,
                vote=vote_str,
                reasoning=reasoning,
                is_self_vote=(voter == target),
                numeric_value=VOTE_NUMERIC.get(vote_str, 1),
            )
        )
    return results


def _parse_votes_from_vote_results(vote_results: list[dict]) -> list[Vote]:
    """Parse votes from the ``voteResults`` structure embedded in discussion.yaml.

    Each entry in *vote_results* has ``targetId`` and a nested ``votes`` list.

    Parameters
    ----------
    vote_results:
        List of dicts with ``targetId`` and ``votes`` sub-list.

    Returns
    -------
    list[Vote]
    """
    results: list[Vote] = []
    for target_block in vote_results:
        nested_votes = target_block.get("votes", [])
        for v in nested_votes:
            voter = v.get("voterId", "")
            target = v.get("targetId", target_block.get("targetId", ""))
            vote_str = v.get("vote", "NEUTRAL")
            reasoning = v.get("reasoning", "")
            results.append(
                Vote(
                    voter_id=voter,
                    target_id=target,
                    vote=vote_str,
                    reasoning=reasoning,
                    is_self_vote=(voter == target),
                    numeric_value=VOTE_NUMERIC.get(vote_str, 1),
                )
            )
    return results


def _parse_termination_votes(raw: list[dict] | None) -> list[TerminationVote]:
    """Parse termination votes from a list of dicts.

    Parameters
    ----------
    raw:
        List of dicts with ``modelId``, ``vote``, and ``reasoning``.

    Returns
    -------
    list[TerminationVote]
    """
    if not raw:
        return []
    results: list[TerminationVote] = []
    for tv in raw:
        results.append(
            TerminationVote(
                model_id=tv.get("modelId", ""),
                vote=tv.get("vote", "CONTINUE"),
                reasoning=tv.get("reasoning", ""),
            )
        )
    return results


def _count_words(text: str) -> int:
    """Count words in a text string.

    Parameters
    ----------
    text:
        Markdown/plain text content.

    Returns
    -------
    int
        Word count.
    """
    return len(text.split())


def _parse_conclusion_frontmatter(conclusion_path: Path) -> dict[str, Any]:
    """Parse YAML frontmatter from a conclusion.md file.

    Parameters
    ----------
    conclusion_path:
        Path to the ``conclusion.md`` file.

    Returns
    -------
    dict
        Frontmatter fields, or empty dict if parsing fails.
    """
    if not conclusion_path.exists():
        return {}
    try:
        text = conclusion_path.read_text(encoding="utf-8")
    except OSError:
        return {}
    match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return {}
    try:
        return yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        return {}


def _load_round_votes_file(discussion_dir: Path, round_number: int) -> list[Vote]:
    """Attempt to load votes from a separate round-N/votes.yaml file.

    Parameters
    ----------
    discussion_dir:
        Directory containing the discussion.
    round_number:
        1-based round number.

    Returns
    -------
    list[Vote]
        Parsed votes, or empty list if file does not exist or is malformed.
    """
    votes_path = discussion_dir / f"round-{round_number}" / "votes.yaml"
    if not votes_path.exists():
        return []
    try:
        with open(votes_path, "r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
    except (yaml.YAMLError, OSError):
        return []
    if not isinstance(data, dict):
        return []
    flat_votes = data.get("votes", [])
    if isinstance(flat_votes, list) and flat_votes:
        return _parse_votes_from_flat_list(flat_votes)
    return []


def _load_round_termination_votes_file(
    discussion_dir: Path, round_number: int
) -> list[TerminationVote]:
    """Attempt to load termination votes from a separate round-N/votes.yaml file.

    Parameters
    ----------
    discussion_dir:
        Directory containing the discussion.
    round_number:
        1-based round number.

    Returns
    -------
    list[TerminationVote]
        Parsed termination votes, or empty list.
    """
    votes_path = discussion_dir / f"round-{round_number}" / "votes.yaml"
    if not votes_path.exists():
        return []
    try:
        with open(votes_path, "r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
    except (yaml.YAMLError, OSError):
        return []
    if not isinstance(data, dict):
        return []
    return _parse_termination_votes(data.get("terminationVotes"))


def _extract_winner_from_vote_results(
    vote_results: list[dict],
) -> Tuple[str, float]:
    """Extract winner id and score from voteResults block.

    Parameters
    ----------
    vote_results:
        The ``voteResults`` list from a votes.yaml or embedded round data.

    Returns
    -------
    tuple[str, float]
        (winner_id, winner_weighted_score).  Defaults to ``("", 0.0)`` if
        no results are available.
    """
    best_id = ""
    best_score = -1.0
    for vr in vote_results:
        ws = float(vr.get("weightedScore", 0))
        if ws > best_score:
            best_score = ws
            best_id = vr.get("targetId", "")
    return best_id, best_score


def _parse_round(
    round_data: dict[str, Any], discussion_dir: Path
) -> RoundResult:
    """Parse a single round from discussion.yaml round data.

    Falls back to loading the separate ``round-N/votes.yaml`` file when
    inline vote data is absent.

    Parameters
    ----------
    round_data:
        Dict from the ``rounds`` list in ``discussion.yaml``.
    discussion_dir:
        Path to the discussion directory (for loading separate vote files).

    Returns
    -------
    RoundResult
    """
    round_num: int = round_data.get("roundNumber", 0)

    # -- responses --
    responses: list[Response] = []
    for resp in round_data.get("responses", []):
        content = resp.get("content", "")
        word_count = resp.get("wordCount", _count_words(content))
        responses.append(
            Response(
                model_id=resp.get("modelId", ""),
                content=content,
                word_count=int(word_count),
            )
        )

    # -- votes --
    # discussion.yaml embeds votes in a ``votes`` key that uses the
    # voteResults structure (list of target blocks with nested votes).
    inline_votes = round_data.get("votes", [])
    votes: list[Vote] = []
    if isinstance(inline_votes, list) and inline_votes:
        # Check structure: voteResults format has dicts with 'targetId' and 'votes'
        first = inline_votes[0] if inline_votes else {}
        if isinstance(first, dict) and "votes" in first and "targetId" in first:
            # This is the voteResults structure embedded in discussion.yaml
            votes = _parse_votes_from_vote_results(inline_votes)
        elif isinstance(first, dict) and "voterId" in first:
            # Flat list (unlikely for inline, but handle gracefully)
            votes = _parse_votes_from_flat_list(inline_votes)

    # Fall back to separate file if no inline votes were parsed
    if not votes:
        votes = _load_round_votes_file(discussion_dir, round_num)

    # -- termination votes --
    inline_term = round_data.get("terminationVotes", [])
    termination_votes = _parse_termination_votes(inline_term)
    if not termination_votes:
        termination_votes = _load_round_termination_votes_file(
            discussion_dir, round_num
        )

    # -- winner --
    winner_id = round_data.get("winnerId", "")
    winner_score = float(round_data.get("winnerScore", 0))
    # If not embedded at round level, try to derive from vote results
    if not winner_id and isinstance(inline_votes, list) and inline_votes:
        first = inline_votes[0] if inline_votes else {}
        if isinstance(first, dict) and "weightedScore" in first:
            winner_id, winner_score = _extract_winner_from_vote_results(
                inline_votes
            )

    return RoundResult(
        round_number=round_num,
        responses=responses,
        votes=votes,
        termination_votes=termination_votes,
        winner_id=winner_id,
        winner_score=winner_score,
    )


def load_discussion(discussion_dir: Path) -> Optional[Discussion]:
    """Load a single discussion from its directory.

    Parameters
    ----------
    discussion_dir:
        Path to a directory containing ``discussion.yaml`` and optionally
        ``conclusion.md`` and ``round-N/votes.yaml`` files.

    Returns
    -------
    Discussion or None
        Parsed discussion, or ``None`` if the directory or required files
        are missing / malformed.
    """
    yaml_path = discussion_dir / "discussion.yaml"
    if not yaml_path.exists():
        return None
    try:
        with open(yaml_path, "r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
    except (yaml.YAMLError, OSError) as exc:
        print(f"  WARNING: could not parse {yaml_path}: {exc}", file=sys.stderr)
        return None

    if not isinstance(data, dict):
        return None

    question_id: str = data.get("questionId", "")
    question_slug: str = data.get("questionSlug", "")
    question_title: str = data.get("questionTitle", "")
    phase_id: str = data.get("phaseId", "")
    config: dict = data.get("config", {})
    status: str = data.get("status", "unknown")

    # Parse rounds
    rounds: list[RoundResult] = []
    for rd in data.get("rounds", []):
        rounds.append(_parse_round(rd, discussion_dir))

    total_rounds = int(
        data.get("stats", {}).get("totalRounds", data.get("currentRound", len(rounds)))
    )

    # Termination reason: prefer top-level field, then conclusion frontmatter
    termination_reason = data.get("terminationReason", "")

    # Conclusion metadata
    conclusion_fm = _parse_conclusion_frontmatter(
        discussion_dir / "conclusion.md"
    )
    conclusion_generated_by = conclusion_fm.get("generatedBy", "")
    if not termination_reason:
        termination_reason = conclusion_fm.get("terminationReason", "unknown")

    category = classify_question(question_title, question_slug)

    return Discussion(
        question_id=question_id,
        question_slug=question_slug,
        question_title=question_title,
        phase_id=phase_id,
        config=config,
        status=status,
        rounds=rounds,
        total_rounds=total_rounds,
        termination_reason=termination_reason,
        conclusion_generated_by=conclusion_generated_by,
        category=category,
    )


def load_all_discussions(base_dir: str | Path) -> list[Discussion]:
    """Load all discussion transcripts from the research-questions directory.

    Scans both the canonical ``EXPECTED_DIRS`` list and any additional
    discussion directories found on disk.

    Parameters
    ----------
    base_dir:
        Root directory of ``src/content/research-questions/``.

    Returns
    -------
    list[Discussion]
        Successfully loaded discussions, sorted by question_id.
    """
    base = Path(base_dir)
    seen_dirs: set[str] = set()
    discussions: list[Discussion] = []

    # 1. Try expected directories
    for rel in EXPECTED_DIRS:
        d = base / rel
        seen_dirs.add(str(d.resolve()))
        if d.is_dir():
            disc = load_discussion(d)
            if disc is not None:
                discussions.append(disc)
            else:
                print(f"  INFO: skipping {d} (no valid discussion.yaml)", file=sys.stderr)
        else:
            print(f"  INFO: directory not found: {d}", file=sys.stderr)

    # 2. Discover any additional discussion directories on disk
    if base.is_dir():
        for phase_dir in sorted(base.iterdir()):
            if not phase_dir.is_dir():
                continue
            for question_dir in sorted(phase_dir.iterdir()):
                if not question_dir.is_dir():
                    continue
                resolved = str(question_dir.resolve())
                if resolved in seen_dirs:
                    continue
                seen_dirs.add(resolved)
                disc_yaml = question_dir / "discussion.yaml"
                if disc_yaml.exists():
                    disc = load_discussion(question_dir)
                    if disc is not None:
                        discussions.append(disc)

    discussions.sort(key=lambda d: d.question_id)
    return discussions


# ---------------------------------------------------------------------------
# Analysis: Convergence
# ---------------------------------------------------------------------------


def _bootstrap_ci(
    data: np.ndarray,
    statistic: str = "mean",
    n_bootstrap: int = 10000,
    confidence: float = 0.95,
    rng_seed: int = 42,
) -> Tuple[float, float]:
    """Compute a bootstrap confidence interval.

    Parameters
    ----------
    data:
        1-D array of observations.
    statistic:
        ``'mean'`` or ``'median'``.
    n_bootstrap:
        Number of bootstrap resamples.
    confidence:
        Confidence level (e.g. 0.95).
    rng_seed:
        Seed for reproducibility.

    Returns
    -------
    tuple[float, float]
        (lower, upper) bounds of the confidence interval.
    """
    if len(data) < 2:
        val = float(data[0]) if len(data) == 1 else 0.0
        return val, val
    rng = np.random.default_rng(rng_seed)
    stat_fn = np.mean if statistic == "mean" else np.median
    boot_stats = np.empty(n_bootstrap)
    for i in range(n_bootstrap):
        sample = rng.choice(data, size=len(data), replace=True)
        boot_stats[i] = stat_fn(sample)
    alpha = (1 - confidence) / 2
    return float(np.percentile(boot_stats, 100 * alpha)), float(
        np.percentile(boot_stats, 100 * (1 - alpha))
    )


def compute_convergence_stats(
    discussions: Sequence[Discussion],
) -> ConvergenceStats:
    """Compute convergence statistics across all discussions.

    Parameters
    ----------
    discussions:
        List of loaded discussions.

    Returns
    -------
    ConvergenceStats
    """
    rounds_list = [d.total_rounds for d in discussions]
    arr = np.array(rounds_list, dtype=float)

    mean_r = float(np.mean(arr)) if len(arr) else 0.0
    median_r = float(np.median(arr)) if len(arr) else 0.0
    std_r = float(np.std(arr, ddof=1)) if len(arr) > 1 else 0.0
    ci_lo, ci_hi = _bootstrap_ci(arr) if len(arr) else (0.0, 0.0)

    # Per-category mean rounds
    cat_rounds: dict[str, list[int]] = {}
    for d in discussions:
        cat_rounds.setdefault(d.category, []).append(d.total_rounds)
    convergence_by_cat = {
        cat: float(np.mean(vals)) for cat, vals in cat_rounds.items()
    }

    # Termination reason distribution
    reason_dist: dict[str, int] = {}
    for d in discussions:
        reason_dist[d.termination_reason] = (
            reason_dist.get(d.termination_reason, 0) + 1
        )

    return ConvergenceStats(
        rounds_per_discussion=rounds_list,
        mean_rounds=mean_r,
        median_rounds=median_r,
        std_rounds=std_r,
        ci_95_lower=ci_lo,
        ci_95_upper=ci_hi,
        convergence_by_category=convergence_by_cat,
        termination_reason_distribution=reason_dist,
    )


# ---------------------------------------------------------------------------
# Analysis: Voting Dynamics
# ---------------------------------------------------------------------------


def _all_votes(discussions: Sequence[Discussion]) -> list[Vote]:
    """Flatten all votes from all rounds of all discussions.

    Parameters
    ----------
    discussions:
        List of loaded discussions.

    Returns
    -------
    list[Vote]
    """
    out: list[Vote] = []
    for d in discussions:
        for r in d.rounds:
            out.extend(r.votes)
    return out


def compute_voting_dynamics(
    discussions: Sequence[Discussion],
) -> VotingDynamics:
    """Compute detailed voting statistics.

    Parameters
    ----------
    discussions:
        List of loaded discussions.

    Returns
    -------
    VotingDynamics
    """
    all_v = _all_votes(discussions)
    total = len(all_v)

    approve_c = sum(1 for v in all_v if v.vote == "APPROVE")
    neutral_c = sum(1 for v in all_v if v.vote == "NEUTRAL")
    reject_c = sum(1 for v in all_v if v.vote == "REJECT")

    approve_rate = approve_c / total if total else 0.0
    neutral_rate = neutral_c / total if total else 0.0
    reject_rate = reject_c / total if total else 0.0

    # Self vs peer
    self_votes = [v for v in all_v if v.is_self_vote]
    peer_votes = [v for v in all_v if not v.is_self_vote]
    self_approve_rate = (
        sum(1 for v in self_votes if v.vote == "APPROVE") / len(self_votes)
        if self_votes
        else 0.0
    )
    peer_approve_rate = (
        sum(1 for v in peer_votes if v.vote == "APPROVE") / len(peer_votes)
        if peer_votes
        else 0.0
    )

    # Per-round approve rates
    round_votes: dict[int, list[Vote]] = {}
    for d in discussions:
        for r in d.rounds:
            round_votes.setdefault(r.round_number, []).extend(r.votes)
    per_round_approve: dict[int, float] = {}
    for rn, vlist in sorted(round_votes.items()):
        if vlist:
            per_round_approve[rn] = sum(
                1 for v in vlist if v.vote == "APPROVE"
            ) / len(vlist)

    # Correlation between self-vote score and peer-vote score per target per round
    # For each (discussion, round, target), compute self score and mean peer score
    self_scores: list[float] = []
    peer_scores: list[float] = []
    for d in discussions:
        for r in d.rounds:
            # Group votes by target
            target_votes: dict[str, list[Vote]] = {}
            for v in r.votes:
                target_votes.setdefault(v.target_id, []).append(v)
            for target, vl in target_votes.items():
                sv = [v for v in vl if v.is_self_vote]
                pv = [v for v in vl if not v.is_self_vote]
                if sv and pv:
                    self_scores.append(float(sv[0].numeric_value))
                    peer_scores.append(
                        float(np.mean([v.numeric_value for v in pv]))
                    )

    pearson_r, pearson_p = (0.0, 1.0)
    spearman_r, spearman_p = (0.0, 1.0)
    if len(self_scores) >= 3:
        try:
            pearson_r, pearson_p = sp_stats.pearsonr(self_scores, peer_scores)
        except Exception:
            pass
        try:
            res = sp_stats.spearmanr(self_scores, peer_scores)
            spearman_r = float(res.statistic)
            spearman_p = float(res.pvalue)
        except Exception:
            pass

    # Per-model profiles
    per_model: dict[str, ModelVotingProfile] = {}
    # Gather all round winners
    all_winners: list[str] = []
    for d in discussions:
        for r in d.rounds:
            if r.winner_id:
                all_winners.append(r.winner_id)
    total_rounds_with_winner = len(all_winners)

    for model in MODELS:
        mv = [v for v in all_v if v.voter_id == model]
        mv_self = [v for v in mv if v.is_self_vote]
        mv_peer = [v for v in mv if not v.is_self_vote]
        total_given = len(mv)
        approves = sum(1 for v in mv if v.vote == "APPROVE")
        neutrals = sum(1 for v in mv if v.vote == "NEUTRAL")
        rejects = sum(1 for v in mv if v.vote == "REJECT")

        self_a_rate = (
            sum(1 for v in mv_self if v.vote == "APPROVE") / len(mv_self)
            if mv_self
            else 0.0
        )
        peer_a_rate = (
            sum(1 for v in mv_peer if v.vote == "APPROVE") / len(mv_peer)
            if mv_peer
            else 0.0
        )

        wins = sum(1 for w in all_winners if w == model)
        win_rate = wins / total_rounds_with_winner if total_rounds_with_winner else 0.0

        # Average weighted score received (as a target)
        received_scores: list[float] = []
        for d in discussions:
            for r in d.rounds:
                target_v = [v for v in r.votes if v.target_id == model]
                if target_v:
                    sv = [v for v in target_v if v.is_self_vote]
                    pv = [v for v in target_v if not v.is_self_vote]
                    # Weighted score: self votes count 0.5, peers count 1.0
                    weighted = sum(v.numeric_value * 0.5 for v in sv) + sum(
                        v.numeric_value for v in pv
                    )
                    received_scores.append(weighted)

        avg_ws = float(np.mean(received_scores)) if received_scores else 0.0

        per_model[model] = ModelVotingProfile(
            model_id=model,
            total_votes_given=total_given,
            approves_given=approves,
            neutrals_given=neutrals,
            rejects_given=rejects,
            approve_rate=approves / total_given if total_given else 0.0,
            neutral_rate=neutrals / total_given if total_given else 0.0,
            reject_rate=rejects / total_given if total_given else 0.0,
            self_approve_rate=self_a_rate,
            peer_approve_rate=peer_a_rate,
            wins=wins,
            win_rate=win_rate,
            avg_weighted_score_received=avg_ws,
        )

    return VotingDynamics(
        total_votes=total,
        approve_count=approve_c,
        neutral_count=neutral_c,
        reject_count=reject_c,
        approve_rate=approve_rate,
        neutral_rate=neutral_rate,
        reject_rate=reject_rate,
        self_vote_approve_rate=self_approve_rate,
        peer_vote_approve_rate=peer_approve_rate,
        self_peer_score_correlation_pearson=pearson_r,
        self_peer_score_correlation_spearman=spearman_r,
        self_peer_pearson_pvalue=pearson_p,
        self_peer_spearman_pvalue=spearman_p,
        per_round_approve_rates=per_round_approve,
        per_model=per_model,
    )


# ---------------------------------------------------------------------------
# Analysis: Divergent Views (placeholder)
# ---------------------------------------------------------------------------


def compute_divergent_view_stats(
    discussions: Sequence[Discussion],
) -> dict[str, Any]:
    """Placeholder for divergent view analysis.

    When divergent-views.yaml files are loaded in a future iteration, this
    function will count and categorise divergent views by topic, model, and
    resolution status.

    Parameters
    ----------
    discussions:
        List of loaded discussions (currently unused).

    Returns
    -------
    dict
        Empty placeholder dict with structure hints.
    """
    return {
        "total_divergent_views": 0,
        "by_category": {},
        "by_model": {},
        "resolved_count": 0,
        "unresolved_count": 0,
        "note": "Divergent view parsing not yet implemented; add DV YAML loading here.",
    }


# ---------------------------------------------------------------------------
# Pretty-printing
# ---------------------------------------------------------------------------


def _fmt_pct(value: float) -> str:
    """Format a fraction as a percentage string."""
    return f"{value * 100:.1f}%"


def _fmt_float(value: float, decimals: int = 2) -> str:
    """Format a float to *decimals* decimal places."""
    return f"{value:.{decimals}f}"


def print_summary(
    discussions: list[Discussion],
    conv: ConvergenceStats,
    vd: VotingDynamics,
) -> None:
    """Print a comprehensive human-readable summary to stdout.

    Parameters
    ----------
    discussions:
        All loaded discussions.
    conv:
        Convergence statistics.
    vd:
        Voting dynamics.
    """
    sep = "=" * 90

    # ---- Header ----
    print(sep)
    print("  PROJECT DYSON -- MULTI-MODEL DELIBERATION ANALYSIS")
    print(f"  Script version {__version__}")
    print(sep)
    print()

    # ---- Per-discussion table ----
    print("DISCUSSION SUMMARY")
    print("-" * 90)
    hdr = f"{'ID':<10} {'Phase':<8} {'Rounds':>6}  {'Category':<20} {'Winner':<18} {'Term. Reason'}"
    print(hdr)
    print("-" * 90)
    for d in discussions:
        # Most frequent winner across rounds
        winners: dict[str, int] = {}
        for r in d.rounds:
            if r.winner_id:
                winners[r.winner_id] = winners.get(r.winner_id, 0) + 1
        top_winner = max(winners, key=lambda k: winners[k]) if winners else "N/A"
        short_winner = top_winner.replace("claude-opus-4-6", "Claude").replace(
            "gemini-3-pro", "Gemini"
        ).replace("gpt-5-2", "GPT")
        print(
            f"{d.question_id:<10} {d.phase_id:<8} {d.total_rounds:>6}  "
            f"{d.category:<20} {short_winner:<18} {d.termination_reason}"
        )
    print()

    # Also print titles
    print("QUESTION TITLES")
    print("-" * 90)
    for d in discussions:
        print(f"  {d.question_id}: {d.question_title}")
    print()

    # ---- Aggregate stats ----
    print("AGGREGATE STATISTICS")
    print("-" * 90)
    print(f"  Total discussions:       {len(discussions)}")
    total_rounds = sum(d.total_rounds for d in discussions)
    print(f"  Total rounds:            {total_rounds}")
    print(f"  Mean rounds:             {_fmt_float(conv.mean_rounds)}")
    print(f"  Median rounds:           {_fmt_float(conv.median_rounds)}")
    print(f"  Std dev rounds:          {_fmt_float(conv.std_rounds)}")
    print(
        f"  95% CI (bootstrap):      [{_fmt_float(conv.ci_95_lower)}, "
        f"{_fmt_float(conv.ci_95_upper)}]"
    )
    print()

    print("  Termination reasons:")
    for reason, count in sorted(
        conv.termination_reason_distribution.items(), key=lambda x: -x[1]
    ):
        print(f"    {reason:<30} {count}")
    print()

    print("  Mean rounds by category:")
    for cat, mean_r in sorted(conv.convergence_by_category.items()):
        n = sum(1 for d in discussions if d.category == cat)
        print(f"    {cat:<25} {_fmt_float(mean_r):>6}  (n={n})")
    print()

    # ---- Voting overview ----
    print("VOTING DYNAMICS")
    print("-" * 90)
    print(f"  Total votes cast:        {vd.total_votes}")
    print(
        f"  APPROVE:                 {vd.approve_count:>5}  ({_fmt_pct(vd.approve_rate)})"
    )
    print(
        f"  NEUTRAL:                 {vd.neutral_count:>5}  ({_fmt_pct(vd.neutral_rate)})"
    )
    print(
        f"  REJECT:                  {vd.reject_count:>5}  ({_fmt_pct(vd.reject_rate)})"
    )
    print()
    print(
        f"  Self-vote APPROVE rate:  {_fmt_pct(vd.self_vote_approve_rate)}"
    )
    print(
        f"  Peer-vote APPROVE rate:  {_fmt_pct(vd.peer_vote_approve_rate)}"
    )
    print()
    print("  Per-round APPROVE rates:")
    for rn, rate in sorted(vd.per_round_approve_rates.items()):
        print(f"    Round {rn}: {_fmt_pct(rate)}")
    print()

    # ---- Self-peer correlation ----
    print("SELF-VOTE vs PEER-VOTE CORRELATION")
    print("-" * 90)
    print(
        f"  Pearson r:   {_fmt_float(vd.self_peer_score_correlation_pearson, 4)}"
        f"  (p = {_fmt_float(vd.self_peer_pearson_pvalue, 4)})"
    )
    print(
        f"  Spearman rho: {_fmt_float(vd.self_peer_score_correlation_spearman, 4)}"
        f"  (p = {_fmt_float(vd.self_peer_spearman_pvalue, 4)})"
    )
    print()

    # ---- Per-model ----
    print("PER-MODEL PROFILES")
    print("-" * 90)
    for model in MODELS:
        mp = vd.per_model.get(model)
        if mp is None:
            continue
        short = model.replace("claude-opus-4-6", "Claude Opus 4.6").replace(
            "gemini-3-pro", "Gemini 3 Pro"
        ).replace("gpt-5-2", "GPT-5.2")
        print(f"  {short}")
        print(f"    Votes given:       {mp.total_votes_given}")
        print(
            f"    APPROVE/NEUTRAL/REJECT: "
            f"{mp.approves_given}/{mp.neutrals_given}/{mp.rejects_given}"
        )
        print(
            f"    APPROVE rate:      {_fmt_pct(mp.approve_rate)}  "
            f"(self: {_fmt_pct(mp.self_approve_rate)}, "
            f"peer: {_fmt_pct(mp.peer_approve_rate)})"
        )
        print(f"    Wins:              {mp.wins}  ({_fmt_pct(mp.win_rate)})")
        print(
            f"    Avg weighted score: {_fmt_float(mp.avg_weighted_score_received)}"
        )
        print()

    # ---- Response word counts ----
    print("RESPONSE WORD COUNTS")
    print("-" * 90)
    for model in MODELS:
        wc: list[int] = []
        for d in discussions:
            for r in d.rounds:
                for resp in r.responses:
                    if resp.model_id == model:
                        wc.append(resp.word_count)
        if wc:
            arr = np.array(wc, dtype=float)
            short = model.replace("claude-opus-4-6", "Claude").replace(
                "gemini-3-pro", "Gemini"
            ).replace("gpt-5-2", "GPT")
            print(
                f"  {short:<12} mean={_fmt_float(np.mean(arr)):>8}  "
                f"median={_fmt_float(np.median(arr)):>8}  "
                f"min={int(np.min(arr)):>6}  max={int(np.max(arr)):>6}  "
                f"n={len(wc)}"
            )
    print()

    # ---- Termination voting ----
    print("TERMINATION VOTING")
    print("-" * 90)
    conclude_counts: dict[str, int] = {}
    continue_counts: dict[str, int] = {}
    total_term = 0
    for d in discussions:
        for r in d.rounds:
            for tv in r.termination_votes:
                total_term += 1
                if tv.vote == "CONCLUDE":
                    conclude_counts[tv.model_id] = (
                        conclude_counts.get(tv.model_id, 0) + 1
                    )
                else:
                    continue_counts[tv.model_id] = (
                        continue_counts.get(tv.model_id, 0) + 1
                    )
    print(f"  Total termination votes: {total_term}")
    for model in MODELS:
        cc = conclude_counts.get(model, 0)
        co = continue_counts.get(model, 0)
        t = cc + co
        short = model.replace("claude-opus-4-6", "Claude").replace(
            "gemini-3-pro", "Gemini"
        ).replace("gpt-5-2", "GPT")
        rate_str = _fmt_pct(cc / t) if t else "N/A"
        print(
            f"    {short:<12} CONCLUDE: {cc:>3}  CONTINUE: {co:>3}  "
            f"conclude rate: {rate_str}"
        )
    print()
    print(sep)


# ---------------------------------------------------------------------------
# CSV export
# ---------------------------------------------------------------------------


def export_votes_csv(discussions: Sequence[Discussion], path: str | Path) -> None:
    """Export one row per vote across all discussions.

    Parameters
    ----------
    discussions:
        All loaded discussions.
    path:
        Output CSV file path.
    """
    fieldnames = [
        "question_id",
        "question_slug",
        "phase_id",
        "category",
        "round_number",
        "voter_id",
        "target_id",
        "vote",
        "numeric_value",
        "is_self_vote",
        "reasoning",
    ]
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for d in discussions:
            for r in d.rounds:
                for v in r.votes:
                    writer.writerow(
                        {
                            "question_id": d.question_id,
                            "question_slug": d.question_slug,
                            "phase_id": d.phase_id,
                            "category": d.category,
                            "round_number": r.round_number,
                            "voter_id": v.voter_id,
                            "target_id": v.target_id,
                            "vote": v.vote,
                            "numeric_value": v.numeric_value,
                            "is_self_vote": v.is_self_vote,
                            "reasoning": v.reasoning,
                        }
                    )
    print(f"  Exported votes CSV:       {path}")


def export_discussions_csv(
    discussions: Sequence[Discussion], path: str | Path
) -> None:
    """Export one row per discussion with summary statistics.

    Parameters
    ----------
    discussions:
        All loaded discussions.
    path:
        Output CSV file path.
    """
    fieldnames = [
        "question_id",
        "question_slug",
        "question_title",
        "phase_id",
        "category",
        "status",
        "total_rounds",
        "termination_reason",
        "conclusion_generated_by",
        "total_votes",
        "approve_count",
        "neutral_count",
        "reject_count",
        "approve_rate",
        "total_responses",
        "mean_word_count",
    ]
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for d in discussions:
            all_v = []
            all_wc = []
            for r in d.rounds:
                all_v.extend(r.votes)
                for resp in r.responses:
                    all_wc.append(resp.word_count)
            approve = sum(1 for v in all_v if v.vote == "APPROVE")
            neutral = sum(1 for v in all_v if v.vote == "NEUTRAL")
            reject = sum(1 for v in all_v if v.vote == "REJECT")
            total = len(all_v)
            writer.writerow(
                {
                    "question_id": d.question_id,
                    "question_slug": d.question_slug,
                    "question_title": d.question_title,
                    "phase_id": d.phase_id,
                    "category": d.category,
                    "status": d.status,
                    "total_rounds": d.total_rounds,
                    "termination_reason": d.termination_reason,
                    "conclusion_generated_by": d.conclusion_generated_by,
                    "total_votes": total,
                    "approve_count": approve,
                    "neutral_count": neutral,
                    "reject_count": reject,
                    "approve_rate": f"{approve / total:.4f}" if total else "0",
                    "total_responses": len(all_wc),
                    "mean_word_count": (
                        f"{np.mean(all_wc):.0f}" if all_wc else "0"
                    ),
                }
            )
    print(f"  Exported discussions CSV: {path}")


def export_rounds_csv(
    discussions: Sequence[Discussion], path: str | Path
) -> None:
    """Export one row per round across all discussions.

    Parameters
    ----------
    discussions:
        All loaded discussions.
    path:
        Output CSV file path.
    """
    fieldnames = [
        "question_id",
        "question_slug",
        "phase_id",
        "category",
        "round_number",
        "winner_id",
        "winner_score",
        "num_responses",
        "mean_word_count",
        "total_votes",
        "approve_count",
        "neutral_count",
        "reject_count",
        "conclude_votes",
        "continue_votes",
        "should_terminate",
    ]
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for d in discussions:
            for r in d.rounds:
                approve = sum(1 for v in r.votes if v.vote == "APPROVE")
                neutral = sum(1 for v in r.votes if v.vote == "NEUTRAL")
                reject = sum(1 for v in r.votes if v.vote == "REJECT")
                conclude = sum(
                    1 for tv in r.termination_votes if tv.vote == "CONCLUDE"
                )
                cont = sum(
                    1 for tv in r.termination_votes if tv.vote == "CONTINUE"
                )
                wc = [resp.word_count for resp in r.responses]
                writer.writerow(
                    {
                        "question_id": d.question_id,
                        "question_slug": d.question_slug,
                        "phase_id": d.phase_id,
                        "category": d.category,
                        "round_number": r.round_number,
                        "winner_id": r.winner_id,
                        "winner_score": r.winner_score,
                        "num_responses": len(r.responses),
                        "mean_word_count": (
                            f"{np.mean(wc):.0f}" if wc else "0"
                        ),
                        "total_votes": len(r.votes),
                        "approve_count": approve,
                        "neutral_count": neutral,
                        "reject_count": reject,
                        "conclude_votes": conclude,
                        "continue_votes": cont,
                        "should_terminate": conclude > cont,
                    }
                )
    print(f"  Exported rounds CSV:      {path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    """Entry point: load data, run analysis, print summary, export CSVs."""
    script_dir = Path(__file__).resolve().parent
    base_dir = script_dir / ".." / ".." / "src" / "content" / "research-questions"
    base_dir = base_dir.resolve()

    data_dir = (
        script_dir
        / ".."
        / "drafts"
        / "03-multi-model-ai-consensus"
        / "data"
    ).resolve()

    print(f"Base directory: {base_dir}")
    print(f"Output directory: {data_dir}")
    print()

    # Load
    print("Loading discussions...")
    discussions = load_all_discussions(base_dir)
    print(f"Loaded {len(discussions)} discussions.\n")

    if not discussions:
        print("ERROR: No discussions found. Check base_dir path.", file=sys.stderr)
        sys.exit(1)

    # Analyse
    conv = compute_convergence_stats(discussions)
    vd = compute_voting_dynamics(discussions)
    _dv = compute_divergent_view_stats(discussions)

    # Print
    print_summary(discussions, conv, vd)

    # Export
    os.makedirs(data_dir, exist_ok=True)
    print("\nExporting CSVs...")
    export_votes_csv(discussions, data_dir / "votes.csv")
    export_discussions_csv(discussions, data_dir / "discussions.csv")
    export_rounds_csv(discussions, data_dir / "rounds.csv")
    print("\nDone.")


if __name__ == "__main__":
    main()
