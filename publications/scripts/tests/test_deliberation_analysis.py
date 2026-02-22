"""Comprehensive tests for deliberation_analysis — data model, classification,
convergence stats, voting dynamics, and CSV export."""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path
from typing import Optional

import numpy as np
import pytest

from deliberation_analysis import (
    CATEGORY_KEYWORDS,
    Discussion,
    ConvergenceStats,
    ModelVotingProfile,
    Response,
    RoundResult,
    TerminationVote,
    Vote,
    VotingDynamics,
    MODELS,
    VOTE_NUMERIC,
    classify_question,
    compute_convergence_stats,
    compute_voting_dynamics,
    export_discussions_csv,
    export_rounds_csv,
    export_votes_csv,
    load_all_discussions,
)


# ---------------------------------------------------------------------------
# Synthetic data helpers
# ---------------------------------------------------------------------------


def make_vote(
    voter_id: str = "claude-opus-4-6",
    target_id: str = "gemini-3-pro",
    vote: str = "APPROVE",
) -> Vote:
    """Build a minimal Vote dataclass instance."""
    return Vote(
        voter_id=voter_id,
        target_id=target_id,
        vote=vote,
        reasoning=f"Test reasoning for {vote}",
        is_self_vote=(voter_id == target_id),
        numeric_value=VOTE_NUMERIC.get(vote, 1),
    )


def make_round(
    round_number: int = 1,
    votes: Optional[list[Vote]] = None,
    termination_votes: Optional[list[TerminationVote]] = None,
    winner_id: str = "claude-opus-4-6",
    winner_score: float = 3.5,
    word_counts: Optional[dict[str, int]] = None,
) -> RoundResult:
    """Build a minimal RoundResult with 3 model responses and 9 votes.

    Parameters
    ----------
    round_number:
        The 1-based round number.
    votes:
        Custom votes list.  If None, generates 9 default votes (all APPROVE).
    termination_votes:
        Custom termination votes.  If None, generates 3 CONCLUDE votes.
    winner_id:
        ID of the round winner.
    winner_score:
        Weighted score of the winner.
    word_counts:
        Per-model word count overrides.  Defaults to 500 per model.
    """
    wc = word_counts or {}
    responses = [
        Response(
            model_id=m,
            content=f"Response from {m} in round {round_number}",
            word_count=wc.get(m, 500),
        )
        for m in MODELS
    ]

    if votes is None:
        votes = []
        for voter in MODELS:
            for target in MODELS:
                votes.append(make_vote(voter_id=voter, target_id=target, vote="APPROVE"))

    if termination_votes is None:
        termination_votes = [
            TerminationVote(model_id=m, vote="CONCLUDE", reasoning="Done")
            for m in MODELS
        ]

    return RoundResult(
        round_number=round_number,
        responses=responses,
        votes=votes,
        termination_votes=termination_votes,
        winner_id=winner_id,
        winner_score=winner_score,
    )


def make_discussion(
    question_id: str = "rq-test-1",
    title: str = "Test question",
    phase: str = "phase-0",
    rounds: int = 1,
    votes_per_round: int = 9,
    winner: str = "claude-opus-4-6",
    category: Optional[str] = None,
    termination_reason: str = "consensus",
    vote_pattern: str = "all_approve",
) -> Discussion:
    """Build a minimal Discussion object with synthetic data.

    Parameters
    ----------
    question_id:
        Unique question ID.
    title:
        Human-readable title (used for category classification if category
        is not explicitly set).
    phase:
        Phase ID (e.g. "phase-0").
    rounds:
        Number of rounds to generate.
    votes_per_round:
        Not directly used when generating default votes (always 9), but
        kept for API compatibility.
    winner:
        Winner model ID for each round.
    category:
        Explicit category override.  If None, derived from title/slug via
        ``classify_question``.
    termination_reason:
        Termination reason string.
    vote_pattern:
        One of 'all_approve', 'mixed', 'all_reject'.  Controls the vote
        values in each round.
    """
    slug = question_id.replace("rq-", "").replace(" ", "-").lower()

    round_results: list[RoundResult] = []
    for r in range(1, rounds + 1):
        # Build votes according to pattern
        votes: list[Vote] = []
        for voter in MODELS:
            for target in MODELS:
                if vote_pattern == "all_approve":
                    v = "APPROVE"
                elif vote_pattern == "all_reject":
                    v = "REJECT"
                elif vote_pattern == "mixed":
                    if voter == target:
                        v = "APPROVE"  # self-vote is approve
                    else:
                        v = "NEUTRAL"
                else:
                    v = "APPROVE"
                votes.append(make_vote(voter_id=voter, target_id=target, vote=v))

        # Termination votes: last round => CONCLUDE, earlier => CONTINUE
        if r == rounds:
            term_votes = [
                TerminationVote(model_id=m, vote="CONCLUDE", reasoning="Done")
                for m in MODELS
            ]
        else:
            term_votes = [
                TerminationVote(model_id=m, vote="CONTINUE", reasoning="More needed")
                for m in MODELS
            ]

        round_results.append(
            make_round(
                round_number=r,
                votes=votes,
                termination_votes=term_votes,
                winner_id=winner,
                winner_score=3.5,
            )
        )

    resolved_category = category or classify_question(title, slug)

    return Discussion(
        question_id=question_id,
        question_slug=slug,
        question_title=title,
        phase_id=phase,
        config={"maxRounds": 3},
        status="concluded",
        rounds=round_results,
        total_rounds=rounds,
        termination_reason=termination_reason,
        conclusion_generated_by=winner,
        category=resolved_category,
    )


# ===========================================================================
# TestVoteDataclass
# ===========================================================================


class TestVoteDataclass:
    """Test the Vote dataclass construction and computed fields."""

    def test_numeric_value_approve(self):
        v = make_vote(vote="APPROVE")
        assert v.numeric_value == 2

    def test_numeric_value_neutral(self):
        v = make_vote(vote="NEUTRAL")
        assert v.numeric_value == 1

    def test_numeric_value_reject(self):
        v = make_vote(vote="REJECT")
        assert v.numeric_value == 0

    def test_self_vote_detection(self):
        v_self = make_vote(voter_id="claude-opus-4-6", target_id="claude-opus-4-6")
        assert v_self.is_self_vote is True

        v_peer = make_vote(voter_id="claude-opus-4-6", target_id="gemini-3-pro")
        assert v_peer.is_self_vote is False

    def test_vote_fields(self):
        v = make_vote(voter_id="gpt-5-2", target_id="gemini-3-pro", vote="NEUTRAL")
        assert v.voter_id == "gpt-5-2"
        assert v.target_id == "gemini-3-pro"
        assert v.vote == "NEUTRAL"
        assert "NEUTRAL" in v.reasoning


# ===========================================================================
# TestClassifyQuestion
# ===========================================================================


class TestClassifyQuestion:
    """Test keyword-based question category classification."""

    def test_governance_keywords(self):
        assert classify_question("Governance structure for multi-century operations", "governance-structure") == "governance"

    def test_governance_from_slug(self):
        assert classify_question("Some question", "end-of-life-disposal") == "governance"

    def test_economic_keywords(self):
        assert classify_question("ISRU cost methodology validation", "isru-cost-methodology") == "economic"

    def test_economic_roi(self):
        assert classify_question("ROI threshold for investment", "roi-threshold") == "economic"

    def test_technical_keywords(self):
        assert classify_question("Swarm power architecture end use", "swarm-power-architecture") == "technical-systems"

    def test_technical_collision(self):
        assert classify_question("Billion unit collision avoidance", "collision-avoidance") == "technical-systems"

    def test_certification_keywords(self):
        assert classify_question("Autonomous assembly certification", "assembly-certification") == "certification"

    def test_certification_human_rating(self):
        assert classify_question("Human-rating transport vehicles", "human-rating-transport") == "certification"

    def test_default_technical(self):
        """When no keywords match, default to technical-systems."""
        assert classify_question("Unrelated abstract topic", "unrelated-abstract") == "technical-systems"

    def test_multiple_category_match_highest_wins(self):
        """When multiple categories match, the one with more keyword hits wins."""
        # 'governance' and 'disposal' -> governance (2 hits)
        # 'architecture' -> technical-systems (1 hit)
        result = classify_question(
            "Governance of disposal and architecture",
            "governance-disposal-architecture",
        )
        assert result == "governance"


# ===========================================================================
# TestComputeConvergenceStats
# ===========================================================================


class TestComputeConvergenceStats:
    """Test convergence statistics computation from synthetic Discussion objects."""

    def test_single_round_discussions(self):
        discussions = [
            make_discussion(question_id=f"rq-t-{i}", rounds=1, category="technical-systems")
            for i in range(5)
        ]
        cs = compute_convergence_stats(discussions)
        assert cs.mean_rounds == pytest.approx(1.0)
        assert cs.median_rounds == pytest.approx(1.0)
        assert cs.std_rounds == pytest.approx(0.0)

    def test_multi_round_discussions(self):
        discussions = [
            make_discussion(question_id="rq-t-1", rounds=1, category="governance"),
            make_discussion(question_id="rq-t-2", rounds=3, category="governance"),
            make_discussion(question_id="rq-t-3", rounds=2, category="economic"),
        ]
        cs = compute_convergence_stats(discussions)
        assert cs.mean_rounds == pytest.approx(2.0)
        assert cs.median_rounds == pytest.approx(2.0)
        assert cs.rounds_per_discussion == [1, 3, 2]

    def test_mean_rounds(self):
        discussions = [
            make_discussion(question_id="rq-a", rounds=2, category="governance"),
            make_discussion(question_id="rq-b", rounds=4, category="governance"),
        ]
        cs = compute_convergence_stats(discussions)
        assert cs.mean_rounds == pytest.approx(3.0)

    def test_category_breakdown(self):
        discussions = [
            make_discussion(question_id="rq-g1", rounds=2, category="governance"),
            make_discussion(question_id="rq-g2", rounds=4, category="governance"),
            make_discussion(question_id="rq-e1", rounds=1, category="economic"),
            make_discussion(question_id="rq-t1", rounds=3, category="technical-systems"),
        ]
        cs = compute_convergence_stats(discussions)
        assert cs.convergence_by_category["governance"] == pytest.approx(3.0)
        assert cs.convergence_by_category["economic"] == pytest.approx(1.0)
        assert cs.convergence_by_category["technical-systems"] == pytest.approx(3.0)

    def test_termination_reasons(self):
        discussions = [
            make_discussion(question_id="rq-1", termination_reason="consensus", category="governance"),
            make_discussion(question_id="rq-2", termination_reason="consensus", category="governance"),
            make_discussion(question_id="rq-3", termination_reason="max_rounds", category="economic"),
        ]
        cs = compute_convergence_stats(discussions)
        assert cs.termination_reason_distribution["consensus"] == 2
        assert cs.termination_reason_distribution["max_rounds"] == 1

    def test_ci_bounds_with_variance(self):
        discussions = [
            make_discussion(question_id=f"rq-ci-{i}", rounds=r, category="governance")
            for i, r in enumerate([1, 2, 3, 4, 5])
        ]
        cs = compute_convergence_stats(discussions)
        assert cs.ci_95_lower <= cs.mean_rounds
        assert cs.ci_95_upper >= cs.mean_rounds

    def test_empty_discussions(self):
        cs = compute_convergence_stats([])
        assert cs.mean_rounds == pytest.approx(0.0)
        assert cs.rounds_per_discussion == []


# ===========================================================================
# TestComputeVotingDynamics
# ===========================================================================


class TestComputeVotingDynamics:
    """Test detailed voting statistics computation."""

    def _make_standard_discussions(self) -> list[Discussion]:
        """Create a set of discussions for voting dynamics tests."""
        return [
            make_discussion(
                question_id="rq-v-1",
                rounds=2,
                vote_pattern="all_approve",
                category="governance",
            ),
            make_discussion(
                question_id="rq-v-2",
                rounds=1,
                vote_pattern="mixed",
                category="economic",
            ),
        ]

    def test_total_votes(self):
        discussions = self._make_standard_discussions()
        vd = compute_voting_dynamics(discussions)
        # Discussion 1: 2 rounds * 9 votes = 18
        # Discussion 2: 1 round * 9 votes = 9
        assert vd.total_votes == 27

    def test_approve_neutral_reject_counts(self):
        # All-approve discussion: 2 rounds * 9 APPROVE = 18 APPROVE
        # Mixed discussion: 1 round * 3 self-APPROVE + 6 NEUTRAL = 3A + 6N
        discussions = self._make_standard_discussions()
        vd = compute_voting_dynamics(discussions)
        assert vd.approve_count == 21  # 18 + 3
        assert vd.neutral_count == 6   # 0 + 6
        assert vd.reject_count == 0

    def test_self_vote_rate(self):
        # All-approve: self votes are APPROVE (6 self votes across 2 rounds)
        # Mixed: self votes are APPROVE (3 self votes)
        # Total self APPROVE: 6 + 3 = 9
        # Total self votes: 6 + 3 = 9
        discussions = self._make_standard_discussions()
        vd = compute_voting_dynamics(discussions)
        assert vd.self_vote_approve_rate == pytest.approx(1.0)

    def test_peer_vote_rate(self):
        # All-approve: 12 peer APPROVE (2 rounds * 6 peer votes)
        # Mixed: 0 peer APPROVE (6 NEUTRAL peer votes)
        # Total peer APPROVE: 12, total peer: 18
        discussions = self._make_standard_discussions()
        vd = compute_voting_dynamics(discussions)
        expected = 12 / 18
        assert vd.peer_vote_approve_rate == pytest.approx(expected)

    def test_per_model_stats(self):
        discussions = [
            make_discussion(
                question_id="rq-pm-1",
                rounds=1,
                vote_pattern="all_approve",
                category="governance",
            ),
        ]
        vd = compute_voting_dynamics(discussions)
        for model in MODELS:
            mp = vd.per_model[model]
            assert mp.model_id == model
            assert mp.total_votes_given == 3  # 3 targets per voter per round
            assert mp.approves_given == 3
            assert mp.approve_rate == pytest.approx(1.0)

    def test_per_model_wins(self):
        discussions = [
            make_discussion(
                question_id="rq-w-1",
                rounds=1,
                winner="claude-opus-4-6",
                category="governance",
            ),
            make_discussion(
                question_id="rq-w-2",
                rounds=1,
                winner="gemini-3-pro",
                category="economic",
            ),
        ]
        vd = compute_voting_dynamics(discussions)
        assert vd.per_model["claude-opus-4-6"].wins == 1
        assert vd.per_model["gemini-3-pro"].wins == 1
        assert vd.per_model["gpt-5-2"].wins == 0

    def test_reject_pattern(self):
        discussions = [
            make_discussion(
                question_id="rq-rej",
                rounds=1,
                vote_pattern="all_reject",
                category="governance",
            ),
        ]
        vd = compute_voting_dynamics(discussions)
        assert vd.reject_count == 9
        assert vd.approve_count == 0
        assert vd.reject_rate == pytest.approx(1.0)

    def test_per_round_approve_rates(self):
        discussions = [
            make_discussion(
                question_id="rq-pr-1",
                rounds=2,
                vote_pattern="all_approve",
                category="governance",
            ),
        ]
        vd = compute_voting_dynamics(discussions)
        # Both rounds have 100% approve rate
        for rn, rate in vd.per_round_approve_rates.items():
            assert rate == pytest.approx(1.0)

    def test_empty_discussions(self):
        vd = compute_voting_dynamics([])
        assert vd.total_votes == 0
        assert vd.approve_rate == pytest.approx(0.0)


# ===========================================================================
# TestExportCsv
# ===========================================================================


class TestExportCsv:
    """Test CSV export functions using tmp_path fixture."""

    def _make_discussions(self) -> list[Discussion]:
        return [
            make_discussion(
                question_id="rq-csv-1",
                title="CSV test question one",
                rounds=2,
                category="governance",
            ),
            make_discussion(
                question_id="rq-csv-2",
                title="CSV test question two",
                rounds=1,
                category="economic",
            ),
        ]

    def test_votes_csv_columns(self, tmp_path: Path):
        discussions = self._make_discussions()
        out = tmp_path / "votes.csv"
        export_votes_csv(discussions, out)

        with open(out, newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            rows = list(reader)

        expected_columns = {
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
        }
        assert expected_columns == set(reader.fieldnames)
        # 2 rounds * 9 votes + 1 round * 9 votes = 27
        assert len(rows) == 27

    def test_discussions_csv_rows(self, tmp_path: Path):
        discussions = self._make_discussions()
        out = tmp_path / "discussions.csv"
        export_discussions_csv(discussions, out)

        with open(out, newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            rows = list(reader)

        assert len(rows) == 2
        assert rows[0]["question_id"] == "rq-csv-1"
        assert rows[0]["total_rounds"] == "2"
        assert rows[1]["question_id"] == "rq-csv-2"
        assert rows[1]["total_rounds"] == "1"

    def test_rounds_csv_rows(self, tmp_path: Path):
        discussions = self._make_discussions()
        out = tmp_path / "rounds.csv"
        export_rounds_csv(discussions, out)

        with open(out, newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            rows = list(reader)

        # Discussion 1 has 2 rounds, discussion 2 has 1 round = 3 rows
        assert len(rows) == 3

        expected_columns = {
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
        }
        assert expected_columns == set(reader.fieldnames)

    def test_votes_csv_content(self, tmp_path: Path):
        discussions = self._make_discussions()
        out = tmp_path / "votes.csv"
        export_votes_csv(discussions, out)

        with open(out, newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            rows = list(reader)

        # Verify all votes have valid vote types
        valid_votes = {"APPROVE", "NEUTRAL", "REJECT"}
        for row in rows:
            assert row["vote"] in valid_votes

    def test_empty_discussions_csv(self, tmp_path: Path):
        out = tmp_path / "votes.csv"
        export_votes_csv([], out)

        with open(out, newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            rows = list(reader)

        assert len(rows) == 0


# ===========================================================================
# TestLoadDiscussions (integration — reads from disk)
# ===========================================================================


@pytest.mark.integration
class TestLoadDiscussions:
    """Integration tests that load real discussion data from disk.

    These tests require the project's research-questions directory to exist.
    Mark with ``@pytest.mark.integration`` so they can be skipped in fast
    CI runs: ``pytest -m "not integration"``.
    """

    @pytest.fixture
    def base_dir(self) -> Path:
        """Return the resolved path to the research-questions directory."""
        script_dir = Path(__file__).resolve().parent.parent
        return (
            script_dir / ".." / ".." / "src" / "content" / "research-questions"
        ).resolve()

    def test_loads_from_disk(self, base_dir: Path):
        if not base_dir.exists():
            pytest.skip(f"Research questions directory not found: {base_dir}")
        discussions = load_all_discussions(base_dir)
        assert isinstance(discussions, list)
        assert len(discussions) > 0

    def test_expected_count(self, base_dir: Path):
        """Expect at least 10 discussions (currently 17 canonical)."""
        if not base_dir.exists():
            pytest.skip(f"Research questions directory not found: {base_dir}")
        discussions = load_all_discussions(base_dir)
        assert len(discussions) >= 10

    def test_has_rounds(self, base_dir: Path):
        if not base_dir.exists():
            pytest.skip(f"Research questions directory not found: {base_dir}")
        discussions = load_all_discussions(base_dir)
        for d in discussions:
            assert d.total_rounds >= 1
            assert len(d.rounds) >= 1

    def test_has_votes(self, base_dir: Path):
        if not base_dir.exists():
            pytest.skip(f"Research questions directory not found: {base_dir}")
        discussions = load_all_discussions(base_dir)
        total_votes = sum(len(r.votes) for d in discussions for r in d.rounds)
        assert total_votes > 0

    def test_discussions_have_categories(self, base_dir: Path):
        if not base_dir.exists():
            pytest.skip(f"Research questions directory not found: {base_dir}")
        discussions = load_all_discussions(base_dir)
        valid_categories = {"governance", "economic", "technical-systems", "certification"}
        for d in discussions:
            assert d.category in valid_categories

    def test_discussions_sorted_by_id(self, base_dir: Path):
        if not base_dir.exists():
            pytest.skip(f"Research questions directory not found: {base_dir}")
        discussions = load_all_discussions(base_dir)
        ids = [d.question_id for d in discussions]
        assert ids == sorted(ids)
