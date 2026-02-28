"""Orbital re-association analysis for Walker constellations.

Computes re-association frequency, AoI transient, and overhead for
co-orbital and cross-plane cluster interactions using Keplerian
orbital mechanics with J2 perturbation.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


# Physical constants
MU_EARTH = 3.986004418e14   # Earth gravitational parameter (m^3/s^2)
R_EARTH = 6.371e6           # Earth mean radius (m)
J2 = 1.08263e-3             # Earth J2 oblateness coefficient


def compute_orbital_period(altitude_km: float) -> float:
    """Compute Keplerian orbital period from altitude.

    Parameters
    ----------
    altitude_km : float
        Orbital altitude above Earth surface (km).

    Returns
    -------
    float
        Orbital period in seconds.
    """
    a = R_EARTH + altitude_km * 1000  # semi-major axis (m)
    return 2 * math.pi * math.sqrt(a**3 / MU_EARTH)


def compute_raan_drift_rate(altitude_km: float, inclination_deg: float) -> float:
    """Compute RAAN regression rate from J2 perturbation.

    The J2 secular perturbation causes the Right Ascension of the
    Ascending Node (RAAN) to precess. For prograde orbits (i < 90 deg),
    RAAN drifts westward (negative rate).

    Parameters
    ----------
    altitude_km : float
        Orbital altitude (km).
    inclination_deg : float
        Orbital inclination (degrees).

    Returns
    -------
    float
        RAAN drift rate in degrees per day.
    """
    a = R_EARTH + altitude_km * 1000
    i_rad = math.radians(inclination_deg)
    n = math.sqrt(MU_EARTH / a**3)  # mean motion (rad/s)

    # J2 RAAN precession: dOmega/dt = -3/2 * n * J2 * (R_E/a)^2 * cos(i)
    d_omega_rad_s = -1.5 * n * J2 * (R_EARTH / a)**2 * math.cos(i_rad)

    # Convert to degrees per day
    return math.degrees(d_omega_rad_s) * 86400


def compute_reassociation_frequency(
    altitude_km: float,
    inclination_deg: float,
    n_planes: int,
    n_sats_per_plane: int,
    cluster_definition: str = "co-orbital",
) -> dict:
    """Compute re-association events per orbit for a Walker constellation.

    Parameters
    ----------
    altitude_km : float
        Orbital altitude (km).
    inclination_deg : float
        Orbital inclination (degrees).
    n_planes : int
        Number of orbital planes.
    n_sats_per_plane : int
        Number of satellites per plane.
    cluster_definition : str
        "co-orbital" (same plane) or "cross-plane" (adjacent planes).

    Returns
    -------
    dict with:
        orbital_period_s, raan_drift_deg_day,
        co_orbital_reassociation_per_orbit,
        cross_plane_differential_drift_deg_day,
        cross_plane_reassociation_period_orbits,
        fleet_reassociation_per_orbit
    """
    T_orb = compute_orbital_period(altitude_km)
    raan_drift = compute_raan_drift_rate(altitude_km, inclination_deg)
    orbits_per_day = 86400 / T_orb

    # RAAN spacing between adjacent planes
    raan_spacing_deg = 360.0 / n_planes

    # Differential drift between adjacent planes:
    # In a Walker constellation, all planes have the same inclination and altitude,
    # so J2 drift rate is identical. Differential RAAN drift is zero for
    # ideal Walker. In practice, small eccentricity/altitude differences
    # cause residual drift.
    #
    # For co-orbital clusters: no re-association (same plane, same drift).
    # For cross-plane: encounters occur when phase angles align due to
    # different in-plane phasing, not RAAN drift.
    co_orbital_reasso = 0.0

    # Cross-plane encounters: satellites in adjacent planes pass through
    # the same latitude band. Encounter frequency depends on the relative
    # angular velocity between planes.
    #
    # In-plane angular velocity: 360 / T_orb degrees per second.
    # Cross-plane relative motion comes from different ascending node times.
    # For adjacent planes, the ascending node crossing offset is:
    # delta_t = (raan_spacing_deg / 360) * T_orb (in seconds)
    #
    # Satellites encounter each other near the poles where orbital planes
    # converge. For a Walker constellation with P planes:
    # - Each plane has 2 intersections with each adjacent plane (ascending
    #   and descending crossings)
    # - Each satellite encounters sats from adjacent plane ~2 times per orbit
    #
    # However, cluster re-association (coordinator handoff) only happens
    # if the encounter distance is below cluster radius.
    cross_plane_encounters_per_orbit = 2.0 if n_planes > 1 else 0.0

    # Fractional overlap time: how long satellites from adjacent planes
    # are within cluster distance (~500 km).
    # At 550 km altitude, orbital velocity ~7.6 km/s.
    # Adjacent planes converge at ~cos(inclination) of orbital velocity.
    # Dwell time within 500 km: ~500 / (7.6 * sin(raan_spacing / 2)) ~65 s
    # This is short compared to T_orb (~5700 s), so encounters are transient.
    v_orbital = 2 * math.pi * (R_EARTH + altitude_km * 1000) / T_orb / 1000  # km/s
    raan_half_rad = math.radians(raan_spacing_deg / 2)
    relative_v = v_orbital * math.sin(raan_half_rad)  # km/s cross-track
    cluster_radius_km = 500.0
    if relative_v > 0:
        dwell_s = cluster_radius_km / relative_v
    else:
        dwell_s = T_orb  # same plane

    # Whether encounters trigger re-association depends on operational rules.
    # Conservative: every cross-plane encounter triggers assessment.
    # For fleet-wide: n_planes boundaries × 2 encounters/orbit × n_sats_per_plane
    fleet_cross_plane_per_orbit = (
        (n_planes - 1) * cross_plane_encounters_per_orbit * n_sats_per_plane
        if cluster_definition == "cross-plane"
        else 0.0
    )

    # For co-orbital clusters: zero by definition
    fleet_co_orbital_per_orbit = 0.0

    total_fleet_reasso_per_orbit = (
        fleet_co_orbital_per_orbit + fleet_cross_plane_per_orbit
    )

    return {
        "orbital_period_s": T_orb,
        "orbital_period_min": T_orb / 60,
        "raan_drift_deg_day": raan_drift,
        "orbits_per_day": orbits_per_day,
        "co_orbital_reassociation_per_orbit": co_orbital_reasso,
        "cross_plane_encounters_per_orbit_per_sat": cross_plane_encounters_per_orbit,
        "raan_spacing_deg": raan_spacing_deg,
        "encounter_dwell_s": dwell_s,
        "orbital_velocity_km_s": v_orbital,
        "fleet_reassociation_per_orbit": total_fleet_reasso_per_orbit,
        "cluster_definition": cluster_definition,
    }


def compute_reassociation_overhead(
    events_per_orbit: float,
    raft_election_bytes: int = 12_800,
    state_handoff_bytes: int = 2_000,
    C_node_bps: float = 1_000,
    k_c: int = 100,
    T_c: float = 10.0,
) -> dict:
    """Compute amortized re-association overhead as fraction of byte budget.

    Parameters
    ----------
    events_per_orbit : float
        Re-association events per orbit.
    raft_election_bytes : int
        Total bytes for Raft leader election (3 rounds × k_c × vote_size).
    state_handoff_bytes : int
        Coordinator state transfer bytes.
    C_node_bps : float
        Per-node data rate (bps).
    k_c : int
        Cluster size.
    T_c : float
        Cycle duration (seconds).

    Returns
    -------
    dict with:
        bytes_per_event, bytes_per_orbit, byte_budget_per_orbit,
        overhead_fraction
    """
    bytes_per_event = raft_election_bytes + state_handoff_bytes

    # Byte budget per orbit: k_c nodes × C_node × T_orb
    # But T_orb isn't known here, so express per-orbit overhead
    # relative to per-orbit capacity.
    # Per cycle: k_c × C_node × T_c bytes = 100 × 1000 × 10 / 8 = 125,000 bytes
    byte_budget_per_cycle = k_c * C_node_bps * T_c / 8

    # Events per cycle: events_per_orbit / (T_orb / T_c)
    # Since T_orb ~5700s, T_c=10s: ~570 cycles per orbit
    # events_per_cycle = events_per_orbit / 570 (approximate)
    # But let's be exact: use standard orbital period
    T_orb_approx = 5700  # ~95 min, placeholder
    cycles_per_orbit = T_orb_approx / T_c
    bytes_per_orbit = events_per_orbit * bytes_per_event
    byte_budget_per_orbit = byte_budget_per_cycle * cycles_per_orbit

    if byte_budget_per_orbit > 0:
        overhead_fraction = bytes_per_orbit / byte_budget_per_orbit
    else:
        overhead_fraction = 0.0

    return {
        "bytes_per_event": bytes_per_event,
        "bytes_per_orbit": bytes_per_orbit,
        "byte_budget_per_orbit": byte_budget_per_orbit,
        "overhead_fraction": overhead_fraction,
        "events_per_orbit": events_per_orbit,
        "cycles_per_orbit": cycles_per_orbit,
    }


def compute_aoi_transient(
    raft_election_s: float = 3.0,
    state_rebuild_cycles: int = 3,
    T_c: float = 10.0,
) -> dict:
    """Compute Age-of-Information transient during re-association.

    During re-association:
    1. Raft election: raft_election_s seconds (no coordinator)
    2. State rebuild: state_rebuild_cycles × T_c seconds (partial state)

    Parameters
    ----------
    raft_election_s : float
        Raft leader election duration (seconds).
    state_rebuild_cycles : int
        Number of cycles to rebuild full cluster state.
    T_c : float
        Cycle duration (seconds).

    Returns
    -------
    dict with:
        election_s, rebuild_s, total_transient_s,
        normal_aoi_p99_s (reference), transient_aoi_s
    """
    rebuild_s = state_rebuild_cycles * T_c
    total_transient = raft_election_s + rebuild_s

    # Normal AoI P99 from paper: ~440 s at f_RF = 5%
    normal_aoi_p99 = 440.0

    return {
        "election_s": raft_election_s,
        "rebuild_s": rebuild_s,
        "total_transient_s": total_transient,
        "normal_aoi_p99_s": normal_aoi_p99,
        "transient_fraction_of_p99": total_transient / normal_aoi_p99,
    }


if __name__ == "__main__":
    print("=" * 70)
    print("Orbital Re-association Analysis")
    print("=" * 70)

    # Starlink-like: 53° inc, 550 km, 72 planes, 22 sats/plane
    altitude = 550
    inclination = 53
    n_planes = 72
    n_sats = 22

    T_orb = compute_orbital_period(altitude)
    raan_drift = compute_raan_drift_rate(altitude, inclination)

    print(f"\n--- Orbital Parameters ({altitude} km, {inclination}° inc) ---")
    print(f"  Orbital period:  {T_orb:.1f} s ({T_orb/60:.1f} min)")
    print(f"  RAAN drift:      {raan_drift:.3f} °/day")

    # Co-orbital
    reasso_co = compute_reassociation_frequency(
        altitude, inclination, n_planes, n_sats, "co-orbital"
    )
    print(f"\n--- Co-Orbital Clusters ---")
    print(f"  Re-association/orbit: {reasso_co['co_orbital_reassociation_per_orbit']:.1f}")
    print(f"  Fleet total/orbit:    {reasso_co['fleet_reassociation_per_orbit']:.1f}")

    # Cross-plane
    reasso_cp = compute_reassociation_frequency(
        altitude, inclination, n_planes, n_sats, "cross-plane"
    )
    print(f"\n--- Cross-Plane Clusters ---")
    print(f"  Encounters/orbit/sat: {reasso_cp['cross_plane_encounters_per_orbit_per_sat']:.1f}")
    print(f"  Encounter dwell:      {reasso_cp['encounter_dwell_s']:.1f} s")
    print(f"  Fleet total/orbit:    {reasso_cp['fleet_reassociation_per_orbit']:.0f}")

    # Overhead
    overhead = compute_reassociation_overhead(
        events_per_orbit=reasso_cp["fleet_reassociation_per_orbit"]
    )
    print(f"\n--- Amortized Overhead ---")
    print(f"  Bytes/event:          {overhead['bytes_per_event']:,}")
    print(f"  Bytes/orbit:          {overhead['bytes_per_orbit']:,.0f}")
    print(f"  Budget/orbit:         {overhead['byte_budget_per_orbit']:,.0f}")
    print(f"  Overhead fraction:    {overhead['overhead_fraction']:.4f} ({overhead['overhead_fraction']*100:.2f}%)")

    # AoI transient
    aoi = compute_aoi_transient()
    print(f"\n--- AoI Transient ---")
    print(f"  Election:             {aoi['election_s']:.1f} s")
    print(f"  State rebuild:        {aoi['rebuild_s']:.1f} s")
    print(f"  Total transient:      {aoi['total_transient_s']:.1f} s")
    print(f"  Fraction of P99 AoI:  {aoi['transient_fraction_of_p99']:.3f}")
