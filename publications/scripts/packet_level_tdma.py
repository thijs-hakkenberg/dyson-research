"""Packet-level TDMA simulator with CCSDS-standard framing.

Independently validates coordinator ingress sizing and ARQ infeasibility
by modeling CCSDS Proximity-1 packet framing from first principles.
gamma is DERIVED from physical-layer parameters, not assumed.

References:
- CCSDS 211.0-B-5: Proximity-1 Space Link Protocol
- CCSDS 131.0-B-4: TM Synchronization and Channel Coding (LDPC)
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field, replace
from typing import Optional

import numpy as np


@dataclass
class PacketFraming:
    """CCSDS Proximity-1 inspired packet framing (CCSDS 211.0-B-5)."""
    asm_bits: int = 32           # Attached Sync Marker
    flag_bits: int = 8           # HDLC flag
    address_bits: int = 8        # Link address
    control_bits: int = 16       # Control field
    fcs_bits: int = 32           # Frame Check Sequence (CRC-32)
    closing_flag_bits: int = 8   # Closing HDLC flag
    fec_rate: float = 7 / 8     # FEC code rate (LDPC per CCSDS 131.0-B-3)


@dataclass
class SlotStructure:
    """TDMA slot physical structure."""
    acquisition_ms: float = 5.0   # Antenna acquisition/pointing dwell
    guard_pre_ms: float = 1.7     # Propagation uncertainty (500 km cluster)
    turnaround_ms: float = 2.0    # TX/RX turnaround (CCSDS Prox-1)
    jitter_margin_ms: float = 1.0 # Timing jitter margin


@dataclass
class PacketLevelConfig:
    """Complete packet-level configuration."""
    framing: PacketFraming = field(default_factory=PacketFraming)
    slot: SlotStructure = field(default_factory=SlotStructure)
    k_c: int = 100
    T_c: float = 10.0
    phy_rate_bps: float = 24_000
    payload_bytes: int = 256      # S_eph
    cmd_bytes: int = 512
    hb_bytes: int = 64
    summary_bytes: int = 512
    # GE channel parameters (same as tdma_slot_sim)
    p_G: float = 0.01
    p_B: float = 0.90
    p_GB: float = 0.05
    p_BG: float = 0.50
    n_retransmissions: int = 0


def _overhead_bits(framing: PacketFraming) -> int:
    """Total framing overhead bits (before FEC)."""
    return (framing.asm_bits + framing.flag_bits + framing.address_bits
            + framing.control_bits + framing.fcs_bits + framing.closing_flag_bits)


def _coded_bits(uncoded_bits: int, fec_rate: float) -> int:
    """Total bits after FEC encoding."""
    return math.ceil(uncoded_bits / fec_rate)


def compute_slot_duration_ms(cfg: PacketLevelConfig, payload_bytes: int) -> float:
    """Compute full slot duration including framing, FEC, guard, and acquisition."""
    payload_bits = payload_bytes * 8
    overhead = _overhead_bits(cfg.framing)
    uncoded_total = payload_bits + overhead
    coded_total = _coded_bits(uncoded_total, cfg.framing.fec_rate)
    data_time_ms = coded_total / cfg.phy_rate_bps * 1000

    guard_ms = (cfg.slot.guard_pre_ms + cfg.slot.turnaround_ms
                + cfg.slot.jitter_margin_ms)
    return data_time_ms + guard_ms + cfg.slot.acquisition_ms


def compute_data_time_ms(cfg: PacketLevelConfig, payload_bytes: int) -> float:
    """Compute only the data transmission time (coded bits / PHY rate)."""
    payload_bits = payload_bytes * 8
    overhead = _overhead_bits(cfg.framing)
    uncoded_total = payload_bits + overhead
    coded_total = _coded_bits(uncoded_total, cfg.framing.fec_rate)
    return coded_total / cfg.phy_rate_bps * 1000


def compute_gamma_decomposition(cfg: PacketLevelConfig) -> dict:
    """Decompose MAC efficiency gamma into independent sub-efficiencies.

    Returns dict with:
        gamma_framing: payload_bits / (payload_bits + overhead_bits)
        gamma_fec: fec_rate
        gamma_guard: data_ms / (data_ms + guard_ms)
        gamma_acq: data_ms / (data_ms + acquisition_ms)
        gamma_total: product of all components (equivalently: payload_bits / (phy_rate * slot_ms))
        slot_duration_ms: full slot time
        data_time_ms: coded data transmission time
        overhead_bits: framing overhead
        uncoded_bits: payload + overhead before FEC
        coded_bits: after FEC encoding
    """
    payload_bits = cfg.payload_bytes * 8
    overhead = _overhead_bits(cfg.framing)
    uncoded_total = payload_bits + overhead
    coded_total = _coded_bits(uncoded_total, cfg.framing.fec_rate)

    data_time_ms = coded_total / cfg.phy_rate_bps * 1000
    guard_ms = (cfg.slot.guard_pre_ms + cfg.slot.turnaround_ms
                + cfg.slot.jitter_margin_ms)
    acq_ms = cfg.slot.acquisition_ms
    slot_ms = data_time_ms + guard_ms + acq_ms

    # Sub-efficiencies
    gamma_framing = payload_bits / uncoded_total
    gamma_fec = cfg.framing.fec_rate
    gamma_guard = data_time_ms / (data_time_ms + guard_ms)
    gamma_acq = (data_time_ms + guard_ms) / (data_time_ms + guard_ms + acq_ms)

    # Total: payload_bits / (phy_rate_bps * slot_ms / 1000)
    gamma_total = payload_bits / (cfg.phy_rate_bps * slot_ms / 1000)

    return {
        "gamma_framing": gamma_framing,
        "gamma_fec": gamma_fec,
        "gamma_guard": gamma_guard,
        "gamma_acq": gamma_acq,
        "gamma_total": gamma_total,
        "gamma_product": gamma_framing * gamma_fec * gamma_guard * gamma_acq,
        "slot_duration_ms": slot_ms,
        "data_time_ms": data_time_ms,
        "overhead_bits": overhead,
        "uncoded_bits": uncoded_total,
        "coded_bits": coded_total,
    }


def _ge_transition(ge_state: bool, rng, p_GB: float, p_BG: float) -> bool:
    """Apply a single GE state transition."""
    if ge_state:  # currently Good
        if rng.random() < p_GB:
            return False
    else:  # currently Bad
        if rng.random() < p_BG:
            return True
    return ge_state


def run_packet_level_simulation(
    cfg: PacketLevelConfig,
    n_cycles: int = 10_000,
    seed: int = 42,
) -> dict:
    """Simulate packet-level TDMA scheduling for a single cluster.

    Models each cycle with:
    - Ingress: (k_c - 1) slots with full framing + FEC + guard + acquisition
    - GE channel at packet level
    - TX/RX turnaround
    - Egress: summary + heartbeat

    Returns dict with metrics comparable to run_tdma_simulation().
    """
    rng = np.random.default_rng(seed)
    n_members = cfg.k_c - 1

    # Slot timings
    eph_slot_ms = compute_slot_duration_ms(cfg, cfg.payload_bytes)
    summary_slot_ms = compute_slot_duration_ms(cfg, cfg.summary_bytes)
    hb_slot_ms = compute_slot_duration_ms(cfg, cfg.hb_bytes)
    turnaround_ms = cfg.slot.turnaround_ms

    T_c_ms = cfg.T_c * 1000

    # GE steady-state
    if cfg.p_GB + cfg.p_BG > 0:
        pi_B = cfg.p_GB / (cfg.p_GB + cfg.p_BG)
    else:
        pi_B = 0.5

    # Per-cycle tracking
    total_reports_sent = 0
    total_reports_received = 0
    deadline_misses = 0
    ingress_times_ms = []
    margin_times_ms = []
    per_cycle_delivery = []

    # GE state per member link
    ge_states = rng.random(n_members) > pi_B

    for cycle in range(n_cycles):
        ingress_time = 0.0
        reports_received = 0

        # === INGRESS PHASE ===
        for m in range(n_members):
            ge_states[m] = _ge_transition(
                ge_states[m], rng, cfg.p_GB, cfg.p_BG
            )

            p_loss = cfg.p_G if ge_states[m] else cfg.p_B
            lost = rng.random() < p_loss
            ingress_time += eph_slot_ms
            total_reports_sent += 1

            if lost:
                for retry in range(cfg.n_retransmissions):
                    ge_states[m] = _ge_transition(
                        ge_states[m], rng, cfg.p_GB, cfg.p_BG
                    )
                    p_loss_retry = cfg.p_G if ge_states[m] else cfg.p_B
                    retry_lost = rng.random() < p_loss_retry
                    ingress_time += eph_slot_ms

                    if not retry_lost:
                        reports_received += 1
                        break
            else:
                reports_received += 1

        # === EGRESS PHASE ===
        egress_time = summary_slot_ms + hb_slot_ms

        total_time = ingress_time + turnaround_ms + egress_time
        margin = T_c_ms - total_time

        ingress_times_ms.append(ingress_time)
        margin_times_ms.append(margin)
        total_reports_received += reports_received
        per_cycle_delivery.append(reports_received / n_members)

        if margin < 0:
            deadline_misses += 1

    ingress_arr = np.array(ingress_times_ms)
    margin_arr = np.array(margin_times_ms)
    delivery_arr = np.array(per_cycle_delivery)

    return {
        "n_cycles": n_cycles,
        "n_members": n_members,
        "slot_duration_ms": eph_slot_ms,
        "ingress_mean_ms": float(np.mean(ingress_arr)),
        "ingress_p99_ms": float(np.percentile(ingress_arr, 99)),
        "margin_mean_ms": float(np.mean(margin_arr)),
        "margin_min_ms": float(np.min(margin_arr)),
        "delivery_rate": float(total_reports_received / total_reports_sent),
        "per_cycle_delivery_mean": float(np.mean(delivery_arr)),
        "per_cycle_delivery_p01": float(np.percentile(delivery_arr, 1)),
        "deadline_misses": deadline_misses,
        "deadline_miss_rate": deadline_misses / n_cycles,
        "analytical_ingress_ms": n_members * eph_slot_ms,
        "analytical_margin_ms": T_c_ms - n_members * eph_slot_ms - turnaround_ms - (summary_slot_ms + hb_slot_ms),
    }


def cross_model_comparison(
    pkt_cfg: PacketLevelConfig,
    n_cycles: int = 10_000,
    seed: int = 42,
) -> dict:
    """Run packet-level sim and compute equivalent slot-sim metrics for comparison.

    Returns dict with packet-level and slot-sim-equivalent results.
    """
    # Packet-level results
    pkt_result = run_packet_level_simulation(pkt_cfg, n_cycles=n_cycles, seed=seed)

    # Slot-sim equivalent: same parameters but without FEC and acquisition
    # (i.e., the slot-sim uses preamble+header+CRC+guard, no FEC, no acquisition)
    slot_sim_slot_ms = _slot_sim_equivalent_slot_ms(pkt_cfg)

    n_members = pkt_cfg.k_c - 1
    T_c_ms = pkt_cfg.T_c * 1000

    slot_sim_ingress = n_members * slot_sim_slot_ms
    slot_sim_margin = T_c_ms - slot_sim_ingress - pkt_cfg.slot.turnaround_ms

    gamma_decomp = compute_gamma_decomposition(pkt_cfg)

    return {
        "packet_level": pkt_result,
        "slot_sim_equivalent": {
            "slot_duration_ms": slot_sim_slot_ms,
            "analytical_ingress_ms": slot_sim_ingress,
            "analytical_margin_ms": slot_sim_margin,
        },
        "gamma_decomposition": gamma_decomp,
    }


def _slot_sim_equivalent_slot_ms(cfg: PacketLevelConfig) -> float:
    """Compute slot-sim-equivalent slot duration (no FEC, no acquisition)."""
    payload_bits = cfg.payload_bytes * 8
    # Slot-sim uses: preamble(32) + header(16) + payload + CRC(16) + guard(4.7ms)
    total_bits = 32 + 16 + payload_bits + 16
    data_time_ms = total_bits / cfg.phy_rate_bps * 1000
    guard_ms = 4.7  # tdma_slot_sim default
    return data_time_ms + guard_ms


def sweep_fec_rate(
    cfg: PacketLevelConfig,
    fec_rates: Optional[list[float]] = None,
    phy_rates: Optional[list[float]] = None,
    n_cycles: int = 1_000,
    seed: int = 42,
) -> dict:
    """Sweep FEC rate x PHY rate -> gamma and schedulability.

    Returns dict with:
        fec_rates, phy_rates,
        results[phy_rate][fec_rate] = {gamma_decomposition, simulation}
    """
    if fec_rates is None:
        fec_rates = [0.5, 2 / 3, 0.75, 7 / 8, 1.0]
    if phy_rates is None:
        phy_rates = [24_000, 30_000]

    results: dict = {}
    for rate in phy_rates:
        results[rate] = {}
        for fec in fec_rates:
            new_framing = replace(cfg.framing, fec_rate=fec)
            new_cfg = replace(cfg, framing=new_framing, phy_rate_bps=rate)

            gamma_d = compute_gamma_decomposition(new_cfg)
            sim = run_packet_level_simulation(new_cfg, n_cycles=n_cycles, seed=seed)

            results[rate][fec] = {
                "gamma_decomposition": gamma_d,
                "simulation": sim,
            }

    return {
        "fec_rates": fec_rates,
        "phy_rates": phy_rates,
        "results": results,
    }


if __name__ == "__main__":
    print("=" * 70)
    print("Packet-Level TDMA Validation")
    print("=" * 70)

    # Default config: 24 kbps, FEC 7/8
    cfg_24 = PacketLevelConfig()
    gamma = compute_gamma_decomposition(cfg_24)

    print("\n--- Gamma Decomposition (24 kbps, FEC 7/8) ---")
    print(f"  Framing overhead:  {gamma['overhead_bits']} bits")
    print(f"  Uncoded total:     {gamma['uncoded_bits']} bits")
    print(f"  Coded total:       {gamma['coded_bits']} bits")
    print(f"  Data time:         {gamma['data_time_ms']:.1f} ms")
    print(f"  Slot duration:     {gamma['slot_duration_ms']:.1f} ms")
    print(f"  gamma_framing:     {gamma['gamma_framing']:.3f}")
    print(f"  gamma_fec:         {gamma['gamma_fec']:.3f}")
    print(f"  gamma_guard:       {gamma['gamma_guard']:.3f}")
    print(f"  gamma_acq:         {gamma['gamma_acq']:.3f}")
    print(f"  gamma_total:       {gamma['gamma_total']:.3f}")
    print(f"  gamma_product:     {gamma['gamma_product']:.3f}")

    # 30 kbps
    cfg_30 = replace(cfg_24, phy_rate_bps=30_000)
    gamma_30 = compute_gamma_decomposition(cfg_30)
    print(f"\n--- Gamma Decomposition (30 kbps, FEC 7/8) ---")
    print(f"  Slot duration:     {gamma_30['slot_duration_ms']:.1f} ms")
    print(f"  gamma_total:       {gamma_30['gamma_total']:.3f}")

    # Feasibility check
    n_members = cfg_24.k_c - 1
    print(f"\n--- Feasibility (k_c={cfg_24.k_c}) ---")
    print(f"  24 kbps: {n_members} slots x {gamma['slot_duration_ms']:.1f} ms = "
          f"{n_members * gamma['slot_duration_ms']:.0f} ms vs T_c = {cfg_24.T_c * 1000:.0f} ms "
          f"-> {'INFEASIBLE' if n_members * gamma['slot_duration_ms'] > cfg_24.T_c * 1000 else 'feasible'}")
    print(f"  30 kbps: {n_members} slots x {gamma_30['slot_duration_ms']:.1f} ms = "
          f"{n_members * gamma_30['slot_duration_ms']:.0f} ms vs T_c = {cfg_30.T_c * 1000:.0f} ms "
          f"-> {'INFEASIBLE' if n_members * gamma_30['slot_duration_ms'] > cfg_30.T_c * 1000 else 'feasible'}")

    # Cross-model comparison
    print("\n--- Cross-Model Comparison (30 kbps, no loss) ---")
    cfg_30_noloss = replace(cfg_30, p_G=0.0, p_B=0.0)
    cmp = cross_model_comparison(cfg_30_noloss, n_cycles=1_000, seed=42)
    print(f"  Packet-level ingress: {cmp['packet_level']['analytical_ingress_ms']:.0f} ms")
    print(f"  Slot-sim ingress:     {cmp['slot_sim_equivalent']['analytical_ingress_ms']:.0f} ms")
    print(f"  Packet-level margin:  {cmp['packet_level']['analytical_margin_ms']:.0f} ms")
    print(f"  Slot-sim margin:      {cmp['slot_sim_equivalent']['analytical_margin_ms']:.0f} ms")

    # FEC sweep
    print("\n--- FEC Rate Sweep ---")
    sweep = sweep_fec_rate(cfg_24, n_cycles=100, seed=42)
    for rate in sweep["phy_rates"]:
        print(f"\n  PHY rate: {rate/1000:.0f} kbps")
        for fec in sweep["fec_rates"]:
            g = sweep["results"][rate][fec]["gamma_decomposition"]
            s = sweep["results"][rate][fec]["simulation"]
            print(f"    FEC {fec:.3f}: gamma={g['gamma_total']:.3f}, "
                  f"slot={g['slot_duration_ms']:.1f} ms, "
                  f"miss_rate={s['deadline_miss_rate']:.3f}")
