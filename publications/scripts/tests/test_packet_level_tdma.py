"""Tests for packet-level TDMA simulator."""

import math
import sys
import os

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from packet_level_tdma import (
    PacketFraming,
    SlotStructure,
    PacketLevelConfig,
    compute_gamma_decomposition,
    compute_slot_duration_ms,
    run_packet_level_simulation,
    cross_model_comparison,
    sweep_fec_rate,
)
from dataclasses import replace


class TestGammaDecomposition:
    """Gamma decomposition from CCSDS framing parameters."""

    def setup_method(self):
        self.cfg = PacketLevelConfig()  # 24 kbps, FEC 7/8
        self.gamma = compute_gamma_decomposition(self.cfg)

    def test_framing_efficiency_range(self):
        """gamma_framing should be in [0.90, 0.97] for 256-byte payload."""
        assert 0.90 <= self.gamma["gamma_framing"] <= 0.97

    def test_fec_efficiency_matches_rate(self):
        """gamma_fec should equal the configured FEC rate exactly."""
        assert self.gamma["gamma_fec"] == self.cfg.framing.fec_rate

    def test_guard_efficiency_range(self):
        """gamma_guard should be in [0.90, 0.99]."""
        assert 0.90 <= self.gamma["gamma_guard"] <= 0.99

    def test_acquisition_efficiency_range(self):
        """gamma_acq should be in [0.85, 0.97]."""
        assert 0.85 <= self.gamma["gamma_acq"] <= 0.97

    def test_total_is_product_of_components(self):
        """gamma_total should approximately equal product of sub-efficiencies."""
        product = (self.gamma["gamma_framing"] * self.gamma["gamma_fec"]
                   * self.gamma["gamma_guard"] * self.gamma["gamma_acq"])
        assert self.gamma["gamma_total"] == pytest.approx(product, abs=0.001)

    def test_product_matches_total(self):
        """gamma_product field should match gamma_total."""
        assert self.gamma["gamma_product"] == pytest.approx(
            self.gamma["gamma_total"], abs=0.001
        )

    def test_derived_gamma_lower_than_slot_sim(self):
        """Derived gamma should be below slot-sim's assumed 0.949."""
        assert self.gamma["gamma_total"] < 0.949

    def test_derived_gamma_below_paper_assumed(self):
        """Derived gamma should be below paper's assumed 0.85."""
        assert self.gamma["gamma_total"] < 0.85

    def test_no_fec_no_acq_approaches_slot_sim(self):
        """With FEC=1.0 and no acquisition, gamma should approach slot-sim's."""
        framing = PacketFraming(fec_rate=1.0)
        slot = SlotStructure(acquisition_ms=0.0)
        cfg = replace(self.cfg, framing=framing, slot=slot)
        g = compute_gamma_decomposition(cfg)
        # Slot-sim gamma at 24 kbps with default params is 0.949
        # Without FEC and acquisition but with CCSDS framing overhead,
        # we should be in the range [0.85, 0.95]
        assert 0.85 <= g["gamma_total"] <= 0.96

    def test_overhead_bits_correct(self):
        """Overhead should be ASM+flag+addr+ctrl+FCS+closing = 104 bits."""
        expected = 32 + 8 + 8 + 16 + 32 + 8  # = 104
        assert self.gamma["overhead_bits"] == expected


class TestPacketLevelSimulation:
    """Simulation-level validation."""

    def test_no_loss_ingress_matches_analytical(self):
        """With no loss, simulated ingress should match analytical within 1%."""
        cfg = PacketLevelConfig(p_G=0.0, p_B=0.0)
        result = run_packet_level_simulation(cfg, n_cycles=100, seed=42)
        assert result["ingress_mean_ms"] == pytest.approx(
            result["analytical_ingress_ms"], rel=0.01
        )

    def test_24kbps_fec78_infeasible(self):
        """24 kbps with FEC 7/8 should be infeasible (100% deadline misses)."""
        cfg = PacketLevelConfig(p_G=0.0, p_B=0.0)
        result = run_packet_level_simulation(cfg, n_cycles=100, seed=42)
        assert result["deadline_miss_rate"] == 1.0

    def test_30kbps_fec78_feasible(self):
        """30 kbps with FEC 7/8 should be feasible (0% deadline misses)."""
        cfg = PacketLevelConfig(phy_rate_bps=30_000, p_G=0.0, p_B=0.0)
        result = run_packet_level_simulation(cfg, n_cycles=100, seed=42)
        assert result["deadline_miss_rate"] == 0.0

    def test_arq_infeasibility_confirmed(self):
        """M_r=1 at 24 kbps should still cause deadline misses."""
        cfg = PacketLevelConfig(n_retransmissions=1, p_G=0.0, p_B=0.0)
        result = run_packet_level_simulation(cfg, n_cycles=100, seed=42)
        # Even with no loss and retries, 24 kbps is infeasible
        assert result["deadline_miss_rate"] == 1.0

    def test_ge_delivery_below_one(self):
        """With GE channel, delivery rate should be below 1.0."""
        cfg = PacketLevelConfig(phy_rate_bps=30_000)  # default GE params
        result = run_packet_level_simulation(cfg, n_cycles=500, seed=42)
        assert result["delivery_rate"] < 1.0

    def test_delivery_rate_positive(self):
        """Delivery rate should be positive even with GE losses."""
        cfg = PacketLevelConfig(phy_rate_bps=30_000)
        result = run_packet_level_simulation(cfg, n_cycles=500, seed=42)
        assert result["delivery_rate"] > 0.5

    def test_result_structure(self):
        """Result should contain all expected keys."""
        cfg = PacketLevelConfig(p_G=0.0, p_B=0.0, phy_rate_bps=30_000)
        result = run_packet_level_simulation(cfg, n_cycles=10, seed=42)
        expected_keys = [
            "n_cycles", "n_members", "slot_duration_ms",
            "ingress_mean_ms", "ingress_p99_ms",
            "margin_mean_ms", "margin_min_ms",
            "delivery_rate", "per_cycle_delivery_mean",
            "per_cycle_delivery_p01", "deadline_misses",
            "deadline_miss_rate", "analytical_ingress_ms",
            "analytical_margin_ms",
        ]
        for key in expected_keys:
            assert key in result, f"Missing key: {key}"


class TestCrossModelComparison:
    """Cross-model comparison between packet-level and slot-sim."""

    def test_packet_slots_longer_than_slot_sim(self):
        """Packet-level slots should be longer than slot-sim equivalent."""
        cfg = PacketLevelConfig(phy_rate_bps=30_000, p_G=0.0, p_B=0.0)
        cmp = cross_model_comparison(cfg, n_cycles=100, seed=42)
        assert cmp["packet_level"]["slot_duration_ms"] > cmp["slot_sim_equivalent"]["slot_duration_ms"]

    def test_30kbps_both_feasible(self):
        """Both models should agree on 30 kbps feasibility."""
        cfg = PacketLevelConfig(phy_rate_bps=30_000, p_G=0.0, p_B=0.0)
        cmp = cross_model_comparison(cfg, n_cycles=100, seed=42)
        # Packet-level: positive margin
        assert cmp["packet_level"]["analytical_margin_ms"] > 0
        # Slot-sim: positive margin
        assert cmp["slot_sim_equivalent"]["analytical_margin_ms"] > 0

    def test_gamma_decomposition_present(self):
        """Cross-model comparison should include gamma decomposition."""
        cfg = PacketLevelConfig(phy_rate_bps=30_000, p_G=0.0, p_B=0.0)
        cmp = cross_model_comparison(cfg, n_cycles=10, seed=42)
        assert "gamma_decomposition" in cmp
        assert "gamma_total" in cmp["gamma_decomposition"]


class TestFECSweep:
    """FEC rate sweep validation."""

    def test_higher_fec_worse_margin(self):
        """Lower FEC rate (more redundancy) should worsen margin."""
        cfg = PacketLevelConfig(p_G=0.0, p_B=0.0, phy_rate_bps=30_000)
        sweep = sweep_fec_rate(cfg, fec_rates=[0.5, 7/8, 1.0],
                               phy_rates=[30_000], n_cycles=10, seed=42)
        results = sweep["results"][30_000]
        # gamma at FEC=0.5 < gamma at FEC=7/8 < gamma at FEC=1.0
        g_half = results[0.5]["gamma_decomposition"]["gamma_total"]
        g_78 = results[7/8]["gamma_decomposition"]["gamma_total"]
        g_none = results[1.0]["gamma_decomposition"]["gamma_total"]
        assert g_half < g_78 < g_none

    def test_no_fec_best_margin(self):
        """FEC rate 1.0 (no FEC) should give maximum gamma."""
        cfg = PacketLevelConfig(p_G=0.0, p_B=0.0, phy_rate_bps=30_000)
        sweep = sweep_fec_rate(cfg, fec_rates=[0.5, 0.75, 1.0],
                               phy_rates=[30_000], n_cycles=10, seed=42)
        results = sweep["results"][30_000]
        g_none = results[1.0]["gamma_decomposition"]["gamma_total"]
        for fec in [0.5, 0.75]:
            assert results[fec]["gamma_decomposition"]["gamma_total"] < g_none

    def test_sweep_structure(self):
        """Sweep should return correct structure."""
        cfg = PacketLevelConfig(p_G=0.0, p_B=0.0)
        sweep = sweep_fec_rate(cfg, fec_rates=[0.5, 1.0],
                               phy_rates=[24_000], n_cycles=10, seed=42)
        assert "fec_rates" in sweep
        assert "phy_rates" in sweep
        assert "results" in sweep
        assert 24_000 in sweep["results"]
        assert 0.5 in sweep["results"][24_000]
        assert 1.0 in sweep["results"][24_000]
        assert "gamma_decomposition" in sweep["results"][24_000][0.5]
        assert "simulation" in sweep["results"][24_000][0.5]
