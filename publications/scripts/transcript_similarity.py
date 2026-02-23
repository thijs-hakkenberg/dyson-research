#!/usr/bin/env python3
"""Transcript-based similarity analysis for Project Dyson multi-model AI deliberations.

Loads all deliberation transcripts from the research-questions directory, computes
round-to-round similarity metrics (TF-IDF cosine similarity, keyword Jaccard overlap,
heading structure overlap), and cross-model convergence statistics.  Results are
printed to stdout, exported as a CSV, and visualised in two publication-quality
PDF figures for Paper 03 (Multi-Model AI Consensus).

Figures:
  1. fig-similarity-heatmap.pdf   -- Pairwise model similarity per round
  2. fig-convergence-trend.pdf    -- Cross-model similarity across rounds (with CI bands)

Requires: PyYAML, numpy, scikit-learn, matplotlib
"""
from __future__ import annotations

__version__ = "1.0.0"

import csv
import os
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from os.path import abspath, dirname, join
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np
import yaml
from matplotlib import use as mpl_use

mpl_use("Agg")

from matplotlib.pyplot import close, rcParams, subplots  # noqa: E402
from sklearn.feature_extraction.text import TfidfVectorizer  # noqa: E402
from sklearn.metrics.pairwise import cosine_similarity  # noqa: E402

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SEED = 42

MODELS = ["claude-opus-4-6", "gemini-3-pro", "gpt-5-2"]

MODEL_LABELS = {
    "claude-opus-4-6": "Claude",
    "gemini-3-pro": "Gemini",
    "gpt-5-2": "GPT",
}

# Re-use the canonical directory list from deliberation_analysis.py
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
# Output paths
# ---------------------------------------------------------------------------
script_dir = dirname(abspath(__file__))
fig_dir = os.environ.get(
    "CONSENSUS_FIG_DIR",
    join(script_dir, "..", "drafts", "03-multi-model-ai-consensus", "figures"),
)
csv_out_path = join(script_dir, "similarity_data.csv")

# ---------------------------------------------------------------------------
# Publication style  (matches generate_consensus_figures.py)
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

# Model colours (same as generate_consensus_figures.py)
MODEL_COLORS = {
    "claude-opus-4-6": "#3b82f6",
    "gemini-3-pro": "#f97316",
    "gpt-5-2": "#22c55e",
}

# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass
class Transcript:
    """A single model response from one round of a discussion."""

    question_slug: str
    model_id: str
    round_number: int
    raw_text: str        # full text including frontmatter
    body_text: str       # text after stripping YAML frontmatter
    headings: list[str]  # extracted markdown headings
    word_count: int


@dataclass
class QuestionRound:
    """All model transcripts for a single round of a single question."""

    question_slug: str
    round_number: int
    transcripts: dict[str, Transcript]  # model_id -> Transcript


@dataclass
class QuestionData:
    """All rounds for a single discussion question."""

    question_slug: str
    phase_id: str
    rounds: dict[int, QuestionRound]  # round_number -> QuestionRound

    @property
    def num_rounds(self) -> int:
        return len(self.rounds)

    @property
    def has_multi_round(self) -> bool:
        return self.num_rounds >= 2


# ---------------------------------------------------------------------------
# Data model -- similarity results
# ---------------------------------------------------------------------------


@dataclass
class SimilarityRecord:
    """One row of similarity data for export."""

    question_slug: str
    phase_id: str
    model_id: str
    round_number: int
    metric: str  # "tfidf_cosine", "keyword_jaccard", "heading_jaccard"
    comparison_type: str  # "within_model_round_to_round" or "cross_model_within_round"
    comparison_target: str  # model_id or "round_N-to-N+1"
    value: float


# ---------------------------------------------------------------------------
# Loading helpers
# ---------------------------------------------------------------------------


def _strip_frontmatter(text: str) -> str:
    """Remove YAML frontmatter delimited by ``---`` markers at file start.

    Parameters
    ----------
    text:
        Raw markdown file content.

    Returns
    -------
    str
        Content with frontmatter removed.
    """
    match = re.match(r"^---\s*\n.*?\n---\s*\n?", text, re.DOTALL)
    if match:
        return text[match.end():]
    return text


def _extract_headings(text: str) -> list[str]:
    """Extract markdown headings (lines starting with ``#``).

    Parameters
    ----------
    text:
        Markdown body text (frontmatter already stripped).

    Returns
    -------
    list[str]
        Heading texts with leading ``#`` characters removed and stripped.
    """
    headings: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            # Remove leading '#' chars and whitespace
            heading_text = stripped.lstrip("#").strip()
            if heading_text:
                headings.append(heading_text.lower())
    return headings


def _extract_keywords(text: str, min_length: int = 4) -> set[str]:
    """Extract technical keywords from text.

    Tokenises on word boundaries, lowercases, and keeps words of
    *min_length* or longer that contain at least one letter.  Filters
    out very common English stop-words to focus on technical terms.

    Parameters
    ----------
    text:
        Body text (frontmatter stripped).
    min_length:
        Minimum word length to include.

    Returns
    -------
    set[str]
        Set of lowercase keyword strings.
    """
    stop_words = {
        "this", "that", "with", "from", "have", "will", "been", "would",
        "could", "should", "their", "there", "these", "those", "which",
        "about", "after", "before", "between", "through", "during",
        "each", "other", "some", "such", "than", "then", "them", "they",
        "into", "over", "also", "more", "most", "only", "very", "when",
        "what", "where", "while", "does", "done", "make", "made",
        "being", "like", "just", "both", "need", "much", "many", "well",
        "here", "under", "must", "case", "used", "using", "based",
        "however", "because", "approach", "provide", "system", "systems",
        "model", "models", "design", "level", "within", "across",
        "rather", "given", "since", "even", "still", "every",
    }
    tokens = re.findall(r"\b[a-zA-Z][\w-]*\b", text.lower())
    return {
        t for t in tokens
        if len(t) >= min_length and t not in stop_words
    }


def _load_transcript(filepath: Path, question_slug: str) -> Optional[Transcript]:
    """Load and parse a single transcript markdown file.

    Parameters
    ----------
    filepath:
        Path to a round-N/model-id.md file.
    question_slug:
        The question slug this transcript belongs to.

    Returns
    -------
    Transcript or None
        Parsed transcript, or ``None`` if file cannot be read.
    """
    try:
        raw = filepath.read_text(encoding="utf-8")
    except OSError:
        return None

    # Parse frontmatter for metadata
    fm: dict[str, Any] = {}
    fm_match = re.match(r"^---\s*\n(.*?)\n---", raw, re.DOTALL)
    if fm_match:
        try:
            fm = yaml.safe_load(fm_match.group(1)) or {}
        except yaml.YAMLError:
            pass

    model_id = fm.get("modelId", filepath.stem)
    round_number = int(fm.get("roundNumber", 0))

    body = _strip_frontmatter(raw)
    headings = _extract_headings(body)
    word_count = len(body.split())

    return Transcript(
        question_slug=question_slug,
        model_id=model_id,
        round_number=round_number,
        raw_text=raw,
        body_text=body,
        headings=headings,
        word_count=word_count,
    )


def load_all_transcripts(base_dir: Path) -> dict[str, QuestionData]:
    """Load all deliberation transcripts organised by question and round.

    Scans both ``EXPECTED_DIRS`` and any additional directories found on disk.

    Parameters
    ----------
    base_dir:
        Root ``src/content/research-questions/`` directory.

    Returns
    -------
    dict[str, QuestionData]
        Mapping from question_slug to ``QuestionData``.
    """
    questions: dict[str, QuestionData] = {}
    seen_dirs: set[str] = set()

    def _process_dir(discussion_dir: Path) -> None:
        resolved = str(discussion_dir.resolve())
        if resolved in seen_dirs:
            return
        seen_dirs.add(resolved)

        if not discussion_dir.is_dir():
            return

        # Derive slug and phase from path
        slug = discussion_dir.name
        phase_id = discussion_dir.parent.name

        # Find round directories
        round_dirs = sorted(
            [d for d in discussion_dir.iterdir() if d.is_dir() and d.name.startswith("round-")],
            key=lambda d: d.name,
        )
        if not round_dirs:
            return

        q_rounds: dict[int, QuestionRound] = {}
        for rd in round_dirs:
            try:
                rn = int(rd.name.split("-")[1])
            except (IndexError, ValueError):
                continue

            transcripts: dict[str, Transcript] = {}
            for model_file in rd.iterdir():
                if not model_file.is_file() or not model_file.name.endswith(".md"):
                    continue
                model_id = model_file.stem  # e.g. "claude-opus-4-6"
                t = _load_transcript(model_file, slug)
                if t is not None:
                    # Ensure round_number is set correctly
                    t.round_number = rn
                    t.model_id = model_id
                    transcripts[model_id] = t

            if transcripts:
                q_rounds[rn] = QuestionRound(
                    question_slug=slug,
                    round_number=rn,
                    transcripts=transcripts,
                )

        if q_rounds:
            questions[slug] = QuestionData(
                question_slug=slug,
                phase_id=phase_id,
                rounds=q_rounds,
            )

    # 1. Expected directories
    for rel in EXPECTED_DIRS:
        _process_dir(base_dir / rel)

    # 2. Discover additional
    if base_dir.is_dir():
        for phase_dir in sorted(base_dir.iterdir()):
            if not phase_dir.is_dir():
                continue
            for question_dir in sorted(phase_dir.iterdir()):
                if not question_dir.is_dir():
                    continue
                _process_dir(question_dir)

    return questions


# ---------------------------------------------------------------------------
# Similarity computation
# ---------------------------------------------------------------------------


def _jaccard(set_a: set[str], set_b: set[str]) -> float:
    """Compute Jaccard similarity between two sets.

    Parameters
    ----------
    set_a, set_b:
        Sets of strings.

    Returns
    -------
    float
        Jaccard index in [0, 1].
    """
    if not set_a and not set_b:
        return 0.0
    intersection = set_a & set_b
    union = set_a | set_b
    return len(intersection) / len(union)


def _tfidf_cosine_pair(text_a: str, text_b: str) -> float:
    """Compute TF-IDF cosine similarity between two texts.

    Parameters
    ----------
    text_a, text_b:
        Document texts.

    Returns
    -------
    float
        Cosine similarity in [0, 1].
    """
    if not text_a.strip() or not text_b.strip():
        return 0.0
    vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
    try:
        tfidf_matrix = vectorizer.fit_transform([text_a, text_b])
        sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        return float(sim[0, 0])
    except ValueError:
        return 0.0


def _tfidf_cosine_multi(texts: list[str]) -> np.ndarray:
    """Compute pairwise TF-IDF cosine similarity for a list of texts.

    Parameters
    ----------
    texts:
        List of document texts.

    Returns
    -------
    np.ndarray
        Pairwise cosine similarity matrix of shape (n, n).
    """
    if not texts or all(not t.strip() for t in texts):
        return np.zeros((len(texts), len(texts)))
    vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
    try:
        tfidf_matrix = vectorizer.fit_transform(texts)
        return cosine_similarity(tfidf_matrix)
    except ValueError:
        return np.eye(len(texts))


def compute_within_model_similarity(
    questions: dict[str, QuestionData],
) -> list[SimilarityRecord]:
    """Compute round-to-round similarity for each model within multi-round questions.

    For each question with 2+ rounds, computes TF-IDF cosine similarity,
    keyword Jaccard overlap, and heading Jaccard overlap between each model's
    Round N and Round N+1 response.

    Parameters
    ----------
    questions:
        All loaded question data.

    Returns
    -------
    list[SimilarityRecord]
        One record per (question, model, metric, round-pair).
    """
    records: list[SimilarityRecord] = []

    for slug, qdata in sorted(questions.items()):
        if not qdata.has_multi_round:
            continue

        sorted_rounds = sorted(qdata.rounds.keys())

        for i in range(len(sorted_rounds) - 1):
            rn_curr = sorted_rounds[i]
            rn_next = sorted_rounds[i + 1]
            round_curr = qdata.rounds[rn_curr]
            round_next = qdata.rounds[rn_next]
            comparison_label = f"round_{rn_curr}-to-{rn_next}"

            for model_id in MODELS:
                t_curr = round_curr.transcripts.get(model_id)
                t_next = round_next.transcripts.get(model_id)
                if t_curr is None or t_next is None:
                    continue

                # TF-IDF cosine
                cos_sim = _tfidf_cosine_pair(t_curr.body_text, t_next.body_text)
                records.append(SimilarityRecord(
                    question_slug=slug,
                    phase_id=qdata.phase_id,
                    model_id=model_id,
                    round_number=rn_curr,
                    metric="tfidf_cosine",
                    comparison_type="within_model_round_to_round",
                    comparison_target=comparison_label,
                    value=cos_sim,
                ))

                # Keyword Jaccard
                kw_curr = _extract_keywords(t_curr.body_text)
                kw_next = _extract_keywords(t_next.body_text)
                kw_jacc = _jaccard(kw_curr, kw_next)
                records.append(SimilarityRecord(
                    question_slug=slug,
                    phase_id=qdata.phase_id,
                    model_id=model_id,
                    round_number=rn_curr,
                    metric="keyword_jaccard",
                    comparison_type="within_model_round_to_round",
                    comparison_target=comparison_label,
                    value=kw_jacc,
                ))

                # Heading Jaccard
                h_curr = set(t_curr.headings)
                h_next = set(t_next.headings)
                h_jacc = _jaccard(h_curr, h_next)
                records.append(SimilarityRecord(
                    question_slug=slug,
                    phase_id=qdata.phase_id,
                    model_id=model_id,
                    round_number=rn_curr,
                    metric="heading_jaccard",
                    comparison_type="within_model_round_to_round",
                    comparison_target=comparison_label,
                    value=h_jacc,
                ))

    return records


def compute_cross_model_similarity(
    questions: dict[str, QuestionData],
) -> list[SimilarityRecord]:
    """Compute pairwise cross-model similarity within each round.

    For every round of every question, computes pairwise TF-IDF cosine
    similarity, keyword Jaccard, and heading Jaccard between all model
    pairs present in that round.

    Parameters
    ----------
    questions:
        All loaded question data.

    Returns
    -------
    list[SimilarityRecord]
        One record per (question, round, model-pair, metric).
    """
    records: list[SimilarityRecord] = []

    for slug, qdata in sorted(questions.items()):
        for rn, qround in sorted(qdata.rounds.items()):
            present_models = [m for m in MODELS if m in qround.transcripts]
            if len(present_models) < 2:
                continue

            # Compute pairwise for all model pairs
            for i in range(len(present_models)):
                for j in range(i + 1, len(present_models)):
                    m_a = present_models[i]
                    m_b = present_models[j]
                    t_a = qround.transcripts[m_a]
                    t_b = qround.transcripts[m_b]

                    pair_label = f"{m_a}_vs_{m_b}"

                    # TF-IDF cosine
                    cos_sim = _tfidf_cosine_pair(t_a.body_text, t_b.body_text)
                    # Record from perspective of both models
                    for model_id in (m_a, m_b):
                        records.append(SimilarityRecord(
                            question_slug=slug,
                            phase_id=qdata.phase_id,
                            model_id=model_id,
                            round_number=rn,
                            metric="tfidf_cosine",
                            comparison_type="cross_model_within_round",
                            comparison_target=pair_label,
                            value=cos_sim,
                        ))

                    # Keyword Jaccard
                    kw_a = _extract_keywords(t_a.body_text)
                    kw_b = _extract_keywords(t_b.body_text)
                    kw_jacc = _jaccard(kw_a, kw_b)
                    for model_id in (m_a, m_b):
                        records.append(SimilarityRecord(
                            question_slug=slug,
                            phase_id=qdata.phase_id,
                            model_id=model_id,
                            round_number=rn,
                            metric="keyword_jaccard",
                            comparison_type="cross_model_within_round",
                            comparison_target=pair_label,
                            value=kw_jacc,
                        ))

                    # Heading Jaccard
                    h_a = set(t_a.headings)
                    h_b = set(t_b.headings)
                    h_jacc = _jaccard(h_a, h_b)
                    for model_id in (m_a, m_b):
                        records.append(SimilarityRecord(
                            question_slug=slug,
                            phase_id=qdata.phase_id,
                            model_id=model_id,
                            round_number=rn,
                            metric="heading_jaccard",
                            comparison_type="cross_model_within_round",
                            comparison_target=pair_label,
                            value=h_jacc,
                        ))

    return records


def compute_heading_adoption(
    questions: dict[str, QuestionData],
) -> dict[str, Any]:
    """Analyse whether Round 1 headings are adopted by other models in later rounds.

    For multi-round questions, examines which model's Round 1 headings appear
    in other models' Round 2 responses.

    Parameters
    ----------
    questions:
        All loaded question data.

    Returns
    -------
    dict
        Summary of heading adoption by originator model.
    """
    adoption_counts: dict[str, list[float]] = {m: [] for m in MODELS}

    for slug, qdata in sorted(questions.items()):
        if not qdata.has_multi_round:
            continue

        round_1 = qdata.rounds.get(1)
        round_2 = qdata.rounds.get(2)
        if round_1 is None or round_2 is None:
            continue

        for originator in MODELS:
            t_orig = round_1.transcripts.get(originator)
            if t_orig is None or not t_orig.headings:
                continue

            orig_headings = set(t_orig.headings)

            # Check adoption by other models in round 2
            for adopter in MODELS:
                if adopter == originator:
                    continue
                t_adopt = round_2.transcripts.get(adopter)
                if t_adopt is None or not t_adopt.headings:
                    continue
                adopt_headings = set(t_adopt.headings)
                overlap = len(orig_headings & adopt_headings)
                rate = overlap / len(orig_headings) if orig_headings else 0.0
                adoption_counts[originator].append(rate)

    result: dict[str, Any] = {}
    for model_id, rates in adoption_counts.items():
        if rates:
            result[model_id] = {
                "mean_adoption_rate": float(np.mean(rates)),
                "median_adoption_rate": float(np.median(rates)),
                "n_pairs": len(rates),
            }
        else:
            result[model_id] = {
                "mean_adoption_rate": 0.0,
                "median_adoption_rate": 0.0,
                "n_pairs": 0,
            }

    return result


# ---------------------------------------------------------------------------
# Aggregate statistics
# ---------------------------------------------------------------------------


def _bootstrap_ci(
    data: np.ndarray,
    n_bootstrap: int = 10000,
    confidence: float = 0.95,
    rng_seed: int = SEED,
) -> Tuple[float, float]:
    """Compute bootstrap 95% CI for the mean.

    Parameters
    ----------
    data:
        1-D array of observations.
    n_bootstrap:
        Number of resamples.
    confidence:
        Confidence level.
    rng_seed:
        Random seed for reproducibility.

    Returns
    -------
    tuple[float, float]
        (lower, upper) bounds.
    """
    if len(data) < 2:
        val = float(data[0]) if len(data) == 1 else 0.0
        return val, val
    rng = np.random.default_rng(rng_seed)
    boot_means = np.empty(n_bootstrap)
    for i in range(n_bootstrap):
        sample = rng.choice(data, size=len(data), replace=True)
        boot_means[i] = np.mean(sample)
    alpha = (1 - confidence) / 2
    return (
        float(np.percentile(boot_means, 100 * alpha)),
        float(np.percentile(boot_means, 100 * (1 - alpha))),
    )


def compute_aggregate_stats(
    within_records: list[SimilarityRecord],
    cross_records: list[SimilarityRecord],
) -> dict[str, Any]:
    """Compute aggregate similarity statistics.

    Parameters
    ----------
    within_records:
        Within-model round-to-round similarity records.
    cross_records:
        Cross-model within-round similarity records.

    Returns
    -------
    dict
        Nested dict of aggregate statistics.
    """
    stats: dict[str, Any] = {}

    # --- Within-model stats ---
    within_by_metric: dict[str, list[float]] = defaultdict(list)
    for r in within_records:
        within_by_metric[r.metric].append(r.value)

    stats["within_model_round_to_round"] = {}
    for metric, values in sorted(within_by_metric.items()):
        arr = np.array(values)
        stats["within_model_round_to_round"][metric] = {
            "mean": float(np.mean(arr)),
            "median": float(np.median(arr)),
            "std": float(np.std(arr, ddof=1)) if len(arr) > 1 else 0.0,
            "n": len(arr),
        }

    # --- Cross-model stats by round ---
    # De-duplicate: each pair is recorded twice (once per model), so take unique pairs
    cross_unique: dict[str, list[SimilarityRecord]] = defaultdict(list)
    for r in cross_records:
        # Use a canonical key to avoid double-counting
        pair_key = f"{r.question_slug}|{r.round_number}|{r.metric}|{r.comparison_target}"
        cross_unique[pair_key].append(r)

    # Use only first occurrence of each pair
    deduped: list[SimilarityRecord] = []
    seen_keys: set[str] = set()
    for r in cross_records:
        pair_key = f"{r.question_slug}|{r.round_number}|{r.metric}|{r.comparison_target}"
        if pair_key not in seen_keys:
            seen_keys.add(pair_key)
            deduped.append(r)

    # Group by round and metric
    by_round_metric: dict[Tuple[int, str], list[float]] = defaultdict(list)
    for r in deduped:
        by_round_metric[(r.round_number, r.metric)].append(r.value)

    stats["cross_model_by_round"] = {}
    for (rn, metric), values in sorted(by_round_metric.items()):
        key = f"round_{rn}_{metric}"
        arr = np.array(values)
        ci = _bootstrap_ci(arr) if len(arr) >= 2 else (float(arr[0]) if len(arr) else 0.0, float(arr[0]) if len(arr) else 0.0)
        stats["cross_model_by_round"][key] = {
            "mean": float(np.mean(arr)),
            "median": float(np.median(arr)),
            "std": float(np.std(arr, ddof=1)) if len(arr) > 1 else 0.0,
            "ci_95_lower": ci[0],
            "ci_95_upper": ci[1],
            "n": len(arr),
        }

    # --- Convergence hypothesis: is Round 2 cross-model sim > Round 1? ---
    convergence: dict[str, Any] = {}
    for metric in ["tfidf_cosine", "keyword_jaccard", "heading_jaccard"]:
        r1_vals = by_round_metric.get((1, metric), [])
        r2_vals = by_round_metric.get((2, metric), [])
        if r1_vals and r2_vals:
            convergence[metric] = {
                "round_1_mean": float(np.mean(r1_vals)),
                "round_2_mean": float(np.mean(r2_vals)),
                "delta": float(np.mean(r2_vals)) - float(np.mean(r1_vals)),
                "round_1_n": len(r1_vals),
                "round_2_n": len(r2_vals),
            }

    stats["convergence_hypothesis"] = convergence

    return stats


# ---------------------------------------------------------------------------
# Pretty-printing
# ---------------------------------------------------------------------------


def _fmt_pct(value: float) -> str:
    """Format a fraction as percentage string."""
    return f"{value * 100:.1f}%"


def _fmt_f(value: float, decimals: int = 4) -> str:
    """Format a float to given decimal places."""
    return f"{value:.{decimals}f}"


def print_summary(
    questions: dict[str, QuestionData],
    within_records: list[SimilarityRecord],
    cross_records: list[SimilarityRecord],
    agg_stats: dict[str, Any],
    heading_adoption: dict[str, Any],
) -> None:
    """Print comprehensive summary statistics to stdout.

    Parameters
    ----------
    questions:
        All loaded question data.
    within_records:
        Within-model similarity records.
    cross_records:
        Cross-model similarity records.
    agg_stats:
        Aggregate statistics dict.
    heading_adoption:
        Heading adoption analysis results.
    """
    sep = "=" * 90

    print(sep)
    print("  PROJECT DYSON -- TRANSCRIPT SIMILARITY ANALYSIS")
    print(f"  Script version {__version__}")
    print(sep)
    print()

    # --- Question overview ---
    total = len(questions)
    multi = sum(1 for q in questions.values() if q.has_multi_round)
    single = total - multi
    print("TRANSCRIPT OVERVIEW")
    print("-" * 90)
    print(f"  Total questions with transcripts:     {total}")
    print(f"  Questions with 2+ rounds:             {multi}")
    print(f"  Questions with 1 round only:          {single}")
    print()

    print(f"  {'Question Slug':<52} {'Phase':<10} {'Rounds':>6}")
    print("  " + "-" * 70)
    for slug in sorted(questions.keys()):
        q = questions[slug]
        rounds_str = ", ".join(str(r) for r in sorted(q.rounds.keys()))
        print(f"  {slug:<52} {q.phase_id:<10} {rounds_str:>6}")
    print()

    # --- Within-model round-to-round stats ---
    wm = agg_stats.get("within_model_round_to_round", {})
    if wm:
        print("WITHIN-MODEL ROUND-TO-ROUND SIMILARITY")
        print("-" * 90)
        print("  (Do models repeat themselves across rounds?)")
        print()
        for metric, vals in sorted(wm.items()):
            print(f"  {metric}:")
            print(f"    Mean:   {_fmt_f(vals['mean'])}")
            print(f"    Median: {_fmt_f(vals['median'])}")
            print(f"    Std:    {_fmt_f(vals['std'])}")
            print(f"    N:      {vals['n']}")
            print()

    # --- Cross-model within-round stats ---
    cm = agg_stats.get("cross_model_by_round", {})
    if cm:
        print("CROSS-MODEL WITHIN-ROUND SIMILARITY")
        print("-" * 90)
        print("  (Are models converging to similar content?)")
        print()
        for key, vals in sorted(cm.items()):
            print(f"  {key}:")
            print(f"    Mean:   {_fmt_f(vals['mean'])}")
            print(f"    Median: {_fmt_f(vals['median'])}")
            print(f"    Std:    {_fmt_f(vals['std'])}")
            print(f"    95% CI: [{_fmt_f(vals['ci_95_lower'])}, {_fmt_f(vals['ci_95_upper'])}]")
            print(f"    N:      {vals['n']}")
            print()

    # --- Convergence hypothesis ---
    conv = agg_stats.get("convergence_hypothesis", {})
    if conv:
        print("CONVERGENCE HYPOTHESIS")
        print("-" * 90)
        print("  (Is Round 2 cross-model similarity > Round 1?)")
        print()
        for metric, vals in sorted(conv.items()):
            direction = "YES (increase)" if vals["delta"] > 0 else "NO (decrease)"
            print(f"  {metric}:")
            print(f"    Round 1 mean: {_fmt_f(vals['round_1_mean'])}  (n={vals['round_1_n']})")
            print(f"    Round 2 mean: {_fmt_f(vals['round_2_mean'])}  (n={vals['round_2_n']})")
            print(f"    Delta:        {_fmt_f(vals['delta'])}  => {direction}")
            print()

    # --- Heading adoption ---
    print("HEADING ADOPTION ANALYSIS")
    print("-" * 90)
    print("  (Are other models adopting a model's Round 1 headings in their Round 2 responses?)")
    print()
    for model_id in MODELS:
        label = MODEL_LABELS.get(model_id, model_id)
        ha = heading_adoption.get(model_id, {})
        print(f"  {label} as originator:")
        print(f"    Mean adoption rate:   {_fmt_f(ha.get('mean_adoption_rate', 0.0))}")
        print(f"    Median adoption rate: {_fmt_f(ha.get('median_adoption_rate', 0.0))}")
        print(f"    N pairs:              {ha.get('n_pairs', 0)}")
        print()

    print(sep)


# ---------------------------------------------------------------------------
# CSV export
# ---------------------------------------------------------------------------


def export_csv(
    within_records: list[SimilarityRecord],
    cross_records: list[SimilarityRecord],
    path: str,
) -> None:
    """Export all similarity data to CSV.

    Parameters
    ----------
    within_records:
        Within-model round-to-round records.
    cross_records:
        Cross-model within-round records.
    path:
        Output file path.
    """
    fieldnames = [
        "question_slug",
        "phase_id",
        "model_id",
        "round_number",
        "metric",
        "comparison_type",
        "comparison_target",
        "value",
    ]
    all_records = within_records + cross_records
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for r in all_records:
            writer.writerow(
                {
                    "question_slug": r.question_slug,
                    "phase_id": r.phase_id,
                    "model_id": r.model_id,
                    "round_number": r.round_number,
                    "metric": r.metric,
                    "comparison_type": r.comparison_type,
                    "comparison_target": r.comparison_target,
                    "value": f"{r.value:.6f}",
                }
            )
    print(f"  Exported similarity CSV: {path}")


# ---------------------------------------------------------------------------
# Figure generation
# ---------------------------------------------------------------------------


def generate_similarity_heatmap(
    questions: dict[str, QuestionData],
    output_path: str,
) -> None:
    """Generate heatmap showing pairwise model TF-IDF cosine similarity per round.

    Creates a grid of 3x3 heatmaps (one per round present across all questions),
    showing average pairwise similarity between models.

    Parameters
    ----------
    questions:
        All loaded question data.
    output_path:
        Path to save the PDF figure.
    """
    # Collect pairwise similarities per round
    # round_number -> (i, j) -> list of similarities
    round_sims: dict[int, dict[Tuple[int, int], list[float]]] = defaultdict(
        lambda: defaultdict(list)
    )

    for slug, qdata in sorted(questions.items()):
        for rn, qround in sorted(qdata.rounds.items()):
            present = [m for m in MODELS if m in qround.transcripts]
            if len(present) < 2:
                continue
            texts = [qround.transcripts[m].body_text for m in present]
            sim_matrix = _tfidf_cosine_multi(texts)

            # Map present models to full MODELS index
            model_idx = {m: MODELS.index(m) for m in present}
            for a_i, m_a in enumerate(present):
                for b_i, m_b in enumerate(present):
                    i = model_idx[m_a]
                    j = model_idx[m_b]
                    round_sims[rn][(i, j)].append(float(sim_matrix[a_i, b_i]))

    all_rounds = sorted(round_sims.keys())
    n_rounds = len(all_rounds)

    if n_rounds == 0:
        print("  WARNING: No data for similarity heatmap.", file=sys.stderr)
        return

    fig, axes = subplots(
        1, n_rounds,
        figsize=(3.2 * n_rounds + 0.5, 3.5),
        squeeze=False,
    )

    for col, rn in enumerate(all_rounds):
        ax = axes[0, col]
        avg_matrix = np.zeros((3, 3))
        for (i, j), vals in round_sims[rn].items():
            avg_matrix[i, j] = np.mean(vals)

        im = ax.imshow(
            avg_matrix,
            cmap="YlOrRd",
            vmin=0.0,
            vmax=1.0,
            aspect="equal",
        )

        # Annotate cells
        for i in range(3):
            for j in range(3):
                val = avg_matrix[i, j]
                color = "white" if val > 0.6 else "black"
                ax.text(
                    j, i, f"{val:.2f}",
                    ha="center", va="center",
                    fontsize=9, fontweight="bold",
                    color=color,
                )

        labels = [MODEL_LABELS[m] for m in MODELS]
        ax.set_xticks(range(3))
        ax.set_xticklabels(labels, fontsize=8)
        ax.set_yticks(range(3))
        ax.set_yticklabels(labels, fontsize=8)
        ax.set_title(f"Round {rn}", fontsize=11, fontweight="bold")

    # Colorbar
    cbar = fig.colorbar(im, ax=axes.ravel().tolist(), shrink=0.8, pad=0.04)
    cbar.set_label("TF-IDF Cosine Similarity", fontsize=9)

    fig.suptitle(
        "Pairwise Model Similarity by Round",
        fontsize=12,
        fontweight="bold",
        y=1.02,
    )

    fig.savefig(output_path, format="pdf")
    close(fig)
    print(f"  Saved figure: {output_path}")


def generate_convergence_trend(
    questions: dict[str, QuestionData],
    cross_records: list[SimilarityRecord],
    output_path: str,
) -> None:
    """Generate line plot showing cross-model similarity trend across rounds.

    Shows mean TF-IDF cosine similarity per round with 95% bootstrap CI bands.

    Parameters
    ----------
    questions:
        All loaded question data.
    cross_records:
        Cross-model similarity records.
    output_path:
        Path to save the PDF figure.
    """
    # De-duplicate cross records (each pair recorded twice)
    seen: set[str] = set()
    deduped: list[SimilarityRecord] = []
    for r in cross_records:
        if r.metric != "tfidf_cosine":
            continue
        key = f"{r.question_slug}|{r.round_number}|{r.comparison_target}"
        if key not in seen:
            seen.add(key)
            deduped.append(r)

    # Group by round
    by_round: dict[int, list[float]] = defaultdict(list)
    for r in deduped:
        by_round[r.round_number].append(r.value)

    if not by_round:
        print("  WARNING: No data for convergence trend.", file=sys.stderr)
        return

    rounds_sorted = sorted(by_round.keys())
    means = []
    ci_lowers = []
    ci_uppers = []
    n_samples = []

    for rn in rounds_sorted:
        arr = np.array(by_round[rn])
        means.append(float(np.mean(arr)))
        n_samples.append(len(arr))
        if len(arr) >= 2:
            ci = _bootstrap_ci(arr)
            ci_lowers.append(ci[0])
            ci_uppers.append(ci[1])
        else:
            ci_lowers.append(float(arr[0]) if len(arr) else 0.0)
            ci_uppers.append(float(arr[0]) if len(arr) else 0.0)

    # Also compute per-metric trends for keyword and heading Jaccard
    metrics_data: dict[str, dict[int, list[float]]] = {
        "tfidf_cosine": {},
        "keyword_jaccard": {},
        "heading_jaccard": {},
    }

    seen2: set[str] = set()
    for r in cross_records:
        key = f"{r.question_slug}|{r.round_number}|{r.metric}|{r.comparison_target}"
        if key not in seen2:
            seen2.add(key)
            metrics_data[r.metric].setdefault(r.round_number, []).append(r.value)

    fig, ax = subplots(figsize=(6, 4))

    metric_styles = {
        "tfidf_cosine": {"color": "#3b82f6", "marker": "o", "label": "TF-IDF Cosine"},
        "keyword_jaccard": {"color": "#f97316", "marker": "s", "label": "Keyword Jaccard"},
        "heading_jaccard": {"color": "#22c55e", "marker": "^", "label": "Heading Jaccard"},
    }

    for metric, round_vals in sorted(metrics_data.items()):
        if not round_vals:
            continue
        style = metric_styles[metric]
        rs = sorted(round_vals.keys())
        m_means = []
        m_ci_lo = []
        m_ci_hi = []
        for rn in rs:
            arr = np.array(round_vals[rn])
            m_means.append(float(np.mean(arr)))
            if len(arr) >= 2:
                ci = _bootstrap_ci(arr)
                m_ci_lo.append(ci[0])
                m_ci_hi.append(ci[1])
            else:
                val = float(arr[0]) if len(arr) else 0.0
                m_ci_lo.append(val)
                m_ci_hi.append(val)

        ax.plot(
            rs, m_means,
            color=style["color"],
            marker=style["marker"],
            linewidth=2,
            markersize=7,
            label=style["label"],
            zorder=3,
        )
        ax.fill_between(
            rs, m_ci_lo, m_ci_hi,
            color=style["color"],
            alpha=0.15,
            zorder=2,
        )

    ax.set_xlabel("Round Number")
    ax.set_ylabel("Mean Cross-Model Similarity")
    ax.set_title("Cross-Model Convergence Across Rounds", fontweight="bold")
    ax.set_xticks(rounds_sorted)
    ax.set_xticklabels([f"Round {r}" for r in rounds_sorted])
    ax.set_ylim(0, 1.0)
    ax.legend(loc="best", framealpha=0.9)

    # Add sample size annotations
    for rn_idx, rn in enumerate(rounds_sorted):
        n = len(by_round.get(rn, []))
        ax.annotate(
            f"n={n}",
            xy=(rn, 0.02),
            ha="center",
            fontsize=7,
            color="gray",
        )

    fig.savefig(output_path, format="pdf")
    close(fig)
    print(f"  Saved figure: {output_path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    """Entry point: load data, compute similarity, print summary, export."""
    base_dir = Path(script_dir) / ".." / ".." / "src" / "content" / "research-questions"
    base_dir = base_dir.resolve()

    print(f"Base directory: {base_dir}")
    print(f"Figure output:  {fig_dir}")
    print(f"CSV output:     {csv_out_path}")
    print()

    # Ensure output directories exist
    os.makedirs(fig_dir, exist_ok=True)

    # Load
    print("Loading transcripts...")
    questions = load_all_transcripts(base_dir)
    print(f"Loaded {len(questions)} questions with transcripts.")
    total_transcripts = sum(
        len(t) for q in questions.values() for r in q.rounds.values() for t in [r.transcripts]
    )
    print(f"Total individual transcripts: {total_transcripts}")
    print()

    if not questions:
        print("ERROR: No transcripts found. Check base_dir path.", file=sys.stderr)
        sys.exit(1)

    # Compute similarities
    print("Computing within-model round-to-round similarity...")
    within_records = compute_within_model_similarity(questions)
    print(f"  Generated {len(within_records)} within-model records.")

    print("Computing cross-model within-round similarity...")
    cross_records = compute_cross_model_similarity(questions)
    print(f"  Generated {len(cross_records)} cross-model records.")

    print("Computing heading adoption analysis...")
    heading_adoption = compute_heading_adoption(questions)
    print()

    # Aggregate stats
    agg_stats = compute_aggregate_stats(within_records, cross_records)

    # Print summary
    print_summary(questions, within_records, cross_records, agg_stats, heading_adoption)

    # Export CSV
    print("\nExporting CSV...")
    export_csv(within_records, cross_records, csv_out_path)

    # Generate figures
    print("\nGenerating figures...")
    generate_similarity_heatmap(
        questions,
        join(fig_dir, "fig-similarity-heatmap.pdf"),
    )
    generate_convergence_trend(
        questions,
        cross_records,
        join(fig_dir, "fig-convergence-trend.pdf"),
    )

    print("\nDone.")


if __name__ == "__main__":
    main()
