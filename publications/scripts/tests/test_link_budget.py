"""Tests for ISL link budget calculator."""

import math
import sys
import os

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from link_budget import compute_link_budget, compute_fspl, sweep_link_budget


class TestFSPL:
    """Free-Space Path Loss validation."""

    def test_fspl_textbook_value(self):
        """FSPL at 500 km, 2.2 GHz should match textbook (~153 dB)."""
        fspl = compute_fspl(freq_hz=2.2e9, distance_m=500e3)
        # 20*log10(4*pi*500e3*2.2e9/3e8)
        assert fspl == pytest.approx(153.3, abs=0.5)

    def test_fspl_uhf_1000km(self):
        """FSPL at 1000 km, 400 MHz should be ~144.5 dB."""
        fspl = compute_fspl(freq_hz=400e6, distance_m=1000e3)
        assert fspl == pytest.approx(144.5, abs=0.5)


class TestISLMode:
    """ISL mode: S-band, 2.2 GHz, 1W, 6 dBi, 500 km."""

    def setup_method(self):
        self.result = compute_link_budget(
            tx_power_w=1.0,
            tx_gain_dbi=6.0,
            rx_gain_dbi=6.0,
            freq_hz=2.2e9,
            distance_m=500e3,
        )

    def test_isl_supports_30kbps(self):
        """S-band ISL max rate should far exceed 30 kbps."""
        assert self.result["max_data_rate_bps"] > 30_000

    def test_isl_ebn0_at_24kbps_positive(self):
        """Eb/N0 at 24 kbps should be well above threshold."""
        assert self.result["ebn0_at_24kbps"] > 9.6  # required for BPSK BER<1e-5


class TestRFBackupMode:
    """RF-backup: UHF, 400 MHz, 0.1W, 0 dBi, 1000 km."""

    def setup_method(self):
        self.result = compute_link_budget(
            tx_power_w=0.1,
            tx_gain_dbi=0.0,
            rx_gain_dbi=0.0,
            freq_hz=400e6,
            distance_m=1000e3,
        )

    def test_link_closes_at_1kbps_uhf(self):
        """UHF backup Eb/N0 at 1 kbps should exceed required threshold."""
        assert self.result["ebn0_at_1kbps"] > 9.6

    def test_link_fails_at_24kbps_uhf(self):
        """UHF backup Eb/N0 at 24 kbps should be below required threshold."""
        assert self.result["ebn0_at_24kbps"] < 9.6

    def test_max_rate_in_low_kbps_range(self):
        """UHF backup max rate should be in the low kbps range."""
        rate_kbps = self.result["max_data_rate_bps"] / 1000
        assert 1.0 < rate_kbps < 10.0


class TestMonotonicity:
    """Monotonicity properties of link budget."""

    def test_max_rate_decreases_with_distance(self):
        """Max rate should decrease monotonically with distance."""
        rates = []
        for d_km in [100, 500, 1000, 2000]:
            r = compute_link_budget(
                tx_power_w=0.1,
                tx_gain_dbi=0.0,
                rx_gain_dbi=0.0,
                freq_hz=400e6,
                distance_m=d_km * 1000,
            )
            rates.append(r["max_data_rate_bps"])
        for i in range(len(rates) - 1):
            assert rates[i] > rates[i + 1]

    def test_max_rate_increases_with_power(self):
        """Max rate should increase monotonically with power."""
        rates = []
        for pw in [0.01, 0.1, 1.0, 10.0]:
            r = compute_link_budget(
                tx_power_w=pw,
                tx_gain_dbi=0.0,
                rx_gain_dbi=0.0,
                freq_hz=400e6,
                distance_m=1000e3,
            )
            rates.append(r["max_data_rate_bps"])
        for i in range(len(rates) - 1):
            assert rates[i] < rates[i + 1]


class TestSweep:
    """Sweep function structure tests."""

    def test_sweep_structure(self):
        """Sweep returns correct structure."""
        s = sweep_link_budget(
            distances_km=[100, 500],
            tx_powers_w=[0.1, 1.0],
            freq_hz=400e6,
            tx_gain_dbi=0.0,
            rx_gain_dbi=0.0,
        )
        assert s["distances_km"] == [100, 500]
        assert s["tx_powers_w"] == [0.1, 1.0]
        for pw in [0.1, 1.0]:
            for d in [100, 500]:
                assert d in s["results"][pw]
                assert "max_data_rate_bps" in s["results"][pw][d]
