"""Tests for TDMA alternative slot designs comparison."""

import sys
import os

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from tdma_alternative_designs import (
    FramingParams,
    SlotConfig,
    config_a_cold_start,
    config_b_multi_packet,
    config_c_tracking,
    config_d_bitmap_ack,
    ALL_CONFIGS,
    compute_slot_timing,
    compute_gamma,
    compute_cycle_budget_ms,
    find_min_phy_rate,
    generate_comparison_table,
)


# Default PHY rates for sweeps
PHY_RATES_BPS = [24_000, 28_000, 30_000, 32_000, 35_000, 40_000, 50_000]


class TestColdStartGamma:
    """Verify cold-start gamma matches paper's derived values."""

    def test_cold_start_gamma_matches_paper_30kbps(self):
        """gamma at 30 kbps should be approximately 0.745 (within 2%)."""
        cfg = config_a_cold_start()
        gamma = compute_gamma(cfg, 30_000)
        assert gamma == pytest.approx(0.745, abs=0.015)

    def test_cold_start_gamma_at_35kbps(self):
        """gamma at 35 kbps should be approximately 0.732 (within 2%)."""
        cfg = config_a_cold_start()
        gamma = compute_gamma(cfg, 35_000)
        assert gamma == pytest.approx(0.732, abs=0.015)

    def test_gamma_decreases_with_rate(self):
        """gamma should decrease as PHY rate increases (fixed overhead dominates)."""
        cfg = config_a_cold_start()
        gammas = [compute_gamma(cfg, rate) for rate in PHY_RATES_BPS]
        # gamma should be monotonically decreasing
        for i in range(len(gammas) - 1):
            assert gammas[i] > gammas[i + 1], (
                f"gamma should decrease: {gammas[i]:.4f} > {gammas[i+1]:.4f} "
                f"at {PHY_RATES_BPS[i]/1000:.0f} vs {PHY_RATES_BPS[i+1]/1000:.0f} kbps"
            )


class TestMultiPacketHigherGamma:
    """Config B (multi-packet) should have higher gamma than Config A."""

    def test_multi_packet_higher_gamma_all_rates(self):
        """Config B gamma > Config A gamma at all PHY rates."""
        cfg_a = config_a_cold_start()
        cfg_b = config_b_multi_packet()
        for rate in PHY_RATES_BPS:
            gamma_a = compute_gamma(cfg_a, rate)
            gamma_b = compute_gamma(cfg_b, rate)
            assert gamma_b > gamma_a, (
                f"Config B gamma ({gamma_b:.4f}) should exceed "
                f"Config A gamma ({gamma_a:.4f}) at {rate/1000:.0f} kbps"
            )


class TestTrackingHigherThanColdStart:
    """Config C (tracking) should have higher gamma than Config A (cold-start).

    Note: Config B (multi-packet) has the highest gamma because it amortizes
    acquisition over 3 back-to-back packets with only 0.5ms inter-packet gaps,
    whereas tracking mode still pays full guard intervals between each slot.
    The ordering is: B > C > A.
    """

    def test_multi_packet_highest_gamma_all_rates(self):
        """Config B gamma > Config C gamma > Config A gamma at all rates."""
        cfg_a = config_a_cold_start()
        cfg_b = config_b_multi_packet()
        cfg_c = config_c_tracking()
        for rate in PHY_RATES_BPS:
            gamma_a = compute_gamma(cfg_a, rate)
            gamma_b = compute_gamma(cfg_b, rate)
            gamma_c = compute_gamma(cfg_c, rate)
            assert gamma_b > gamma_c > gamma_a, (
                f"Expected B > C > A at {rate/1000:.0f} kbps: "
                f"{gamma_b:.4f} > {gamma_c:.4f} > {gamma_a:.4f}"
            )


class TestBitmapSimilarToColdStart:
    """Config D (bitmap ACK) should have gamma close to Config A."""

    def test_bitmap_similar_to_cold_start(self):
        """Config D gamma should be within 5% of Config A gamma at all rates."""
        cfg_a = config_a_cold_start()
        cfg_d = config_d_bitmap_ack()
        for rate in PHY_RATES_BPS:
            gamma_a = compute_gamma(cfg_a, rate)
            gamma_d = compute_gamma(cfg_d, rate)
            assert gamma_d == pytest.approx(gamma_a, rel=0.05), (
                f"Config D ({gamma_d:.4f}) should match Config A ({gamma_a:.4f}) "
                f"within 5% at {rate/1000:.0f} kbps"
            )


class TestMinPhyRateOrdering:
    """Minimum feasible PHY rates should follow expected ordering.

    Multi-packet amortizes acquisition most aggressively, so it has
    the lowest R_PHY_min.  The ordering is: B < C < A.
    """

    def test_min_phy_rate_ordering(self):
        """R_PHY_min: multi-packet < tracking < cold-start."""
        cfg_a = config_a_cold_start()
        cfg_b = config_b_multi_packet()
        cfg_c = config_c_tracking()
        min_a = find_min_phy_rate(cfg_a, n_nodes=100)
        min_b = find_min_phy_rate(cfg_b, n_nodes=100)
        min_c = find_min_phy_rate(cfg_c, n_nodes=100)
        assert min_b < min_c < min_a, (
            f"Expected multi-packet ({min_b:.0f}) < tracking ({min_c:.0f}) "
            f"< cold-start ({min_a:.0f})"
        )


class TestFeasibilityAt35kbps:
    """35 kbps should be feasible for all configurations."""

    def test_35kbps_feasible_all_configs(self):
        """All configs should have R_PHY_min < 35 kbps for N=100."""
        for config_fn in ALL_CONFIGS:
            cfg = config_fn()
            min_phy = find_min_phy_rate(cfg, n_nodes=100)
            assert min_phy < 35_000, (
                f"Config '{cfg.name}' R_PHY_min = {min_phy/1000:.1f} kbps "
                f"exceeds 35 kbps"
            )

    def test_positive_margin_at_35kbps(self):
        """All configs should have positive margin at 35 kbps."""
        for config_fn in ALL_CONFIGS:
            cfg = config_fn()
            budget = compute_cycle_budget_ms(cfg, 35_000, n_nodes=100)
            assert budget["margin_ms"] > 0, (
                f"Config '{cfg.name}' has negative margin "
                f"({budget['margin_ms']:.1f} ms) at 35 kbps"
            )


class TestSlotTimingPositive:
    """All computed timing values should be positive."""

    def test_slot_timing_positive(self):
        """All timing components should be positive for all configs and rates."""
        for config_fn in ALL_CONFIGS:
            cfg = config_fn()
            for rate in PHY_RATES_BPS:
                timing = compute_slot_timing(cfg, rate)
                assert timing["payload_time_ms"] > 0, (
                    f"Negative payload time for {cfg.name} at {rate/1000:.0f} kbps"
                )
                assert timing["total_slot_ms"] > 0, (
                    f"Negative slot duration for {cfg.name} at {rate/1000:.0f} kbps"
                )
                assert timing["n_packets"] >= 1, (
                    f"Zero packets for {cfg.name}"
                )


class TestGammaBounded:
    """Gamma should be bounded in (0, 1) for all configs and rates."""

    def test_gamma_bounded(self):
        """0 < gamma < 1 for all configurations and PHY rates."""
        for config_fn in ALL_CONFIGS:
            cfg = config_fn()
            for rate in PHY_RATES_BPS:
                gamma = compute_gamma(cfg, rate)
                assert 0 < gamma < 1, (
                    f"gamma = {gamma:.4f} out of bounds for {cfg.name} "
                    f"at {rate/1000:.0f} kbps"
                )


class TestComparisonTable:
    """Smoke test for the comparison table generator."""

    def test_table_has_all_configs(self):
        """Table should contain entries for all four configurations."""
        rows = generate_comparison_table()
        names = {r["config_name"] for r in rows}
        assert names == {"cold_start", "multi_packet", "tracking", "bitmap_ack"}

    def test_table_gamma_values_present(self):
        """Each row should have gamma values for all default PHY rates."""
        rows = generate_comparison_table()
        for row in rows:
            assert len(row["gamma_per_rate"]) == 7  # default 7 rates
            for rate_k, gamma in row["gamma_per_rate"].items():
                assert 0 < gamma < 1

    def test_table_min_phy_rate_positive(self):
        """Minimum PHY rate should be positive for all configs."""
        rows = generate_comparison_table()
        for row in rows:
            assert row["min_phy_rate_kbps"] > 0
