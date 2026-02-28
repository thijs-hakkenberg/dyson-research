"""Tests for orbital re-association analysis."""

import math
import sys
import os

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from orbital_reassociation import (
    compute_orbital_period,
    compute_raan_drift_rate,
    compute_reassociation_frequency,
    compute_reassociation_overhead,
    compute_aoi_transient,
)


class TestOrbitalPeriod:
    """Keplerian orbital period validation."""

    def test_orbital_period_iss_altitude(self):
        """400 km altitude should give ~92 min period."""
        T = compute_orbital_period(400)
        assert T / 60 == pytest.approx(92.3, abs=1.0)

    def test_orbital_period_starlink(self):
        """550 km altitude should give ~96 min period."""
        T = compute_orbital_period(550)
        assert T / 60 == pytest.approx(95.7, abs=1.0)

    def test_period_increases_with_altitude(self):
        """Higher altitude should give longer period."""
        T_low = compute_orbital_period(400)
        T_high = compute_orbital_period(1000)
        assert T_high > T_low

    def test_geostationary_period(self):
        """35786 km altitude should give ~24h period."""
        T = compute_orbital_period(35786)
        assert T / 3600 == pytest.approx(24.0, abs=0.5)


class TestRAANDrift:
    """J2 RAAN regression validation."""

    def test_raan_drift_sign(self):
        """Prograde orbits (i < 90°) should have negative RAAN drift."""
        drift = compute_raan_drift_rate(550, 53)
        assert drift < 0

    def test_raan_drift_polar_near_zero(self):
        """90° inclination should give near-zero RAAN drift."""
        drift = compute_raan_drift_rate(550, 90)
        assert abs(drift) < 0.01

    def test_raan_drift_retrograde_positive(self):
        """Retrograde orbits (i > 90°) should have positive RAAN drift."""
        drift = compute_raan_drift_rate(550, 120)
        assert drift > 0

    def test_raan_drift_starlink_magnitude(self):
        """Starlink (53°, 550 km) RAAN drift should be ~5 deg/day."""
        drift = compute_raan_drift_rate(550, 53)
        assert abs(drift) == pytest.approx(5.0, abs=1.0)


class TestReassociationFrequency:
    """Re-association event frequency for Walker constellations."""

    def test_co_orbital_zero_reassociation(self):
        """Co-orbital clusters should have zero re-association."""
        result = compute_reassociation_frequency(
            550, 53, 72, 22, "co-orbital"
        )
        assert result["co_orbital_reassociation_per_orbit"] == 0.0
        assert result["fleet_reassociation_per_orbit"] == 0.0

    def test_cross_plane_nonzero_encounters(self):
        """Cross-plane clusters should have nonzero encounters."""
        result = compute_reassociation_frequency(
            550, 53, 72, 22, "cross-plane"
        )
        assert result["fleet_reassociation_per_orbit"] > 0

    def test_single_plane_no_cross_encounters(self):
        """Single-plane constellation should have no cross-plane encounters."""
        result = compute_reassociation_frequency(
            550, 53, 1, 100, "cross-plane"
        )
        assert result["fleet_reassociation_per_orbit"] == 0.0

    def test_orbital_period_in_result(self):
        """Result should contain orbital period."""
        result = compute_reassociation_frequency(550, 53, 72, 22, "co-orbital")
        assert result["orbital_period_min"] == pytest.approx(95.7, abs=1.0)


class TestReassociationOverhead:
    """Amortized re-association overhead."""

    def test_zero_events_zero_overhead(self):
        """Zero events should give zero overhead."""
        result = compute_reassociation_overhead(events_per_orbit=0.0)
        assert result["overhead_fraction"] == 0.0

    def test_overhead_fraction_small(self):
        """Co-orbital re-association overhead should be < 1% of budget."""
        # Realistic: ~10 re-association events per orbit fleet-wide
        # (most encounters are transient and don't trigger full handoff)
        result = compute_reassociation_overhead(events_per_orbit=10)
        assert result["overhead_fraction"] < 0.01

    def test_bytes_per_event_correct(self):
        """Bytes per event should be election + handoff."""
        result = compute_reassociation_overhead(
            events_per_orbit=1,
            raft_election_bytes=12_800,
            state_handoff_bytes=2_000,
        )
        assert result["bytes_per_event"] == 14_800


class TestAoITransient:
    """Age-of-Information transient during re-association."""

    def test_total_transient_correct(self):
        """Total transient should be election + rebuild."""
        result = compute_aoi_transient(
            raft_election_s=3.0, state_rebuild_cycles=3, T_c=10.0
        )
        assert result["total_transient_s"] == 33.0

    def test_aoi_transient_bounded(self):
        """Total transient should be < 60 s with default parameters."""
        result = compute_aoi_transient()
        assert result["total_transient_s"] < 60.0

    def test_transient_fraction_modest(self):
        """Transient should be a small fraction of P99 AoI."""
        result = compute_aoi_transient()
        assert result["transient_fraction_of_p99"] < 0.1

    def test_custom_parameters(self):
        """Custom election and rebuild parameters should work."""
        result = compute_aoi_transient(
            raft_election_s=5.0, state_rebuild_cycles=5, T_c=10.0
        )
        assert result["total_transient_s"] == 55.0
