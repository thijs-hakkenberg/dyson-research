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


def sweep_acq_guard_feasibility(
    k_c: int = 100,
    payload_bytes: int = 256,
    T_c_ms: float = 10_000.0,
    T_egress_ms: float = 200.0,
    acq_range: tuple[float, float] = (0.0, 10.0),
    guard_range: tuple[float, float] = (3.0, 10.0),
    n_acq: int = 80,
    n_guard: int = 80,
    phy_lo: float = 24_000.0,
    phy_hi: float = 60_000.0,
) -> dict:
    """Sweep T_acq x T_guard and find minimum viable R_PHY via binary search.

    For each (T_acq, T_guard) pair, finds the lowest PHY rate in [phy_lo, phy_hi]
    where the scheduling margin >= 0:
        margin = T_c - (k_c - 1) * T_slot - T_egress

    Returns dict with:
        acq_vals: 1-D array of T_acq values (ms)
        guard_vals: 1-D array of T_guard values (ms)
        min_phy_kbps: 2-D array [n_guard, n_acq] of minimum viable R_PHY in kbps
                      (np.inf where no rate in range is feasible)
    """
    acq_vals = np.linspace(acq_range[0], acq_range[1], n_acq)
    guard_vals = np.linspace(guard_range[0], guard_range[1], n_guard)
    min_phy = np.full((n_guard, n_acq), np.inf)

    n_members = k_c - 1
    budget_ms = T_c_ms - T_egress_ms  # time available for ingress

    for i, t_guard in enumerate(guard_vals):
        for j, t_acq in enumerate(acq_vals):
            # Binary search for minimum viable R_PHY
            lo, hi = phy_lo, phy_hi
            best = np.inf

            # Quick feasibility check at hi rate
            cfg_hi = PacketLevelConfig(
                slot=SlotStructure(
                    acquisition_ms=t_acq,
                    guard_pre_ms=t_guard - 3.0 if t_guard > 3.0 else 0.0,
                    turnaround_ms=2.0,
                    jitter_margin_ms=1.0,
                ),
                phy_rate_bps=hi,
                payload_bytes=payload_bytes,
                k_c=k_c,
                T_c=T_c_ms / 1000.0,
            )
            # Recompute guard to match the total guard budget:
            # total guard = guard_pre + turnaround + jitter
            # We want total guard = t_guard, so set guard_pre accordingly
            desired_guard_total = t_guard
            cfg_hi = replace(
                cfg_hi,
                slot=SlotStructure(
                    acquisition_ms=t_acq,
                    guard_pre_ms=max(0.0, desired_guard_total - 2.0 - 1.0),
                    turnaround_ms=2.0,
                    jitter_margin_ms=1.0,
                ),
            )
            slot_hi = compute_slot_duration_ms(cfg_hi, payload_bytes)
            ingress_hi = n_members * slot_hi
            if ingress_hi > budget_ms:
                # Even at max rate, infeasible
                continue

            # Check if feasible at lo rate
            cfg_lo = replace(cfg_hi, phy_rate_bps=lo)
            slot_lo = compute_slot_duration_ms(cfg_lo, payload_bytes)
            ingress_lo = n_members * slot_lo
            if ingress_lo <= budget_ms:
                best = lo
            else:
                # Binary search
                for _ in range(50):  # ~50 iterations gives sub-bps precision
                    mid = (lo + hi) / 2.0
                    cfg_mid = replace(cfg_hi, phy_rate_bps=mid)
                    slot_mid = compute_slot_duration_ms(cfg_mid, payload_bytes)
                    ingress_mid = n_members * slot_mid
                    if ingress_mid <= budget_ms:
                        best = mid
                        hi = mid
                    else:
                        lo = mid

            min_phy[i, j] = best / 1000.0  # convert to kbps

    return {
        "acq_vals": acq_vals,
        "guard_vals": guard_vals,
        "min_phy_kbps": min_phy,
    }


def compute_gamma_vs_rate(
    phy_rates_bps: np.ndarray,
    k_c: int = 100,
    payload_bytes: int = 256,
    T_c_ms: float = 10_000.0,
    T_egress_ms: float = 200.0,
) -> dict:
    """Compute gamma (slot efficiency) vs PHY rate for two models.

    Model S (simplified): no FEC overhead, no acquisition time.
        slot = payload_bits / R_PHY + T_guard(4.7 ms)
        gamma_s = payload_bits / (R_PHY * T_slot)

    Model C (CCSDS): full framing + FEC + acquisition.
        Uses compute_gamma_decomposition() with default PacketLevelConfig.

    Returns dict with:
        phy_rates_kbps: array
        gamma_simple: array of gamma values for Model S
        gamma_ccsds: array of gamma values for Model C
        margin_simple_ms: array of scheduling margins for Model S
        margin_ccsds_ms: array of scheduling margins for Model C
    """
    n = len(phy_rates_bps)
    gamma_s = np.zeros(n)
    gamma_c = np.zeros(n)
    margin_s = np.zeros(n)
    margin_c = np.zeros(n)

    payload_bits = payload_bytes * 8
    n_members = k_c - 1
    budget_ms = T_c_ms - T_egress_ms

    for idx, rate in enumerate(phy_rates_bps):
        # Model S: simplified (no FEC, no acquisition, minimal guard)
        data_ms_simple = payload_bits / rate * 1000.0
        guard_simple = 4.7  # same as slot-sim default
        slot_simple = data_ms_simple + guard_simple
        gamma_s[idx] = payload_bits / (rate * slot_simple / 1000.0)
        margin_s[idx] = budget_ms - n_members * slot_simple

        # Model C: full CCSDS
        cfg = PacketLevelConfig(phy_rate_bps=rate, payload_bytes=payload_bytes,
                                k_c=k_c, T_c=T_c_ms / 1000.0)
        decomp = compute_gamma_decomposition(cfg)
        gamma_c[idx] = decomp["gamma_total"]
        margin_c[idx] = budget_ms - n_members * decomp["slot_duration_ms"]

    return {
        "phy_rates_kbps": phy_rates_bps / 1000.0,
        "gamma_simple": gamma_s,
        "gamma_ccsds": gamma_c,
        "margin_simple_ms": margin_s,
        "margin_ccsds_ms": margin_c,
    }


# ---------------------------------------------------------------------------
# Figure generation
# ---------------------------------------------------------------------------

def _setup_matplotlib():
    """Configure matplotlib for publication-quality IEEE figures."""
    from matplotlib import use as mpl_use
    mpl_use("Agg")
    from matplotlib.pyplot import rcParams
    rcParams.update({
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
        "savefig.pad_inches": 0.05,
        "axes.grid": True,
        "grid.alpha": 0.3,
        "grid.linewidth": 0.5,
    })


def generate_margin_sensitivity_figure(
    output_path: str,
    sweep_result: Optional[dict] = None,
) -> None:
    """Generate contour plot of minimum viable R_PHY vs (T_acq, T_guard).

    Saves to output_path as PDF.
    """
    _setup_matplotlib()
    import matplotlib.pyplot as plt

    if sweep_result is None:
        sweep_result = sweep_acq_guard_feasibility()

    acq = sweep_result["acq_vals"]
    guard = sweep_result["guard_vals"]
    Z = sweep_result["min_phy_kbps"].copy()

    # Cap inf values for plotting
    finite_mask = np.isfinite(Z)
    if finite_mask.any():
        z_max = Z[finite_mask].max()
    else:
        z_max = 60.0
    Z[~finite_mask] = z_max * 1.05

    fig, ax = plt.subplots(1, 1, figsize=(6, 4.5))

    # Contour levels in kbps -- use finer spacing matching data range
    z_min_finite = Z[np.isfinite(Z)].min()
    z_max_finite = Z[np.isfinite(Z)].max()
    levels = np.arange(
        math.floor(z_min_finite),
        math.ceil(z_max_finite) + 1.5,
        1.0,
    )

    ACQ, GUARD = np.meshgrid(acq, guard)
    cf = ax.contourf(ACQ, GUARD, Z, levels=levels, cmap="RdYlGn_r", extend="both")
    cs = ax.contour(ACQ, GUARD, Z, levels=levels, colors="k", linewidths=0.4,
                    alpha=0.5)
    ax.clabel(cs, inline=True, fontsize=7, fmt="%.0f")

    cbar = fig.colorbar(cf, ax=ax, label="Min. viable $R_{\\mathrm{PHY}}$ (kbps)")

    # --- Mark reference points ---
    # CCSDS default: T_acq=5, T_guard=4.7
    ccsds_acq, ccsds_guard = 5.0, 4.7
    # Compute R_PHY at this point
    ccsds_phy = _lookup_phy(sweep_result, ccsds_acq, ccsds_guard)
    ax.plot(ccsds_acq, ccsds_guard, marker="*", color="white", markersize=14,
            markeredgecolor="black", markeredgewidth=1.0, zorder=10)
    ax.annotate(f"CCSDS default\n{ccsds_phy:.0f} kbps",
                xy=(ccsds_acq, ccsds_guard), xytext=(ccsds_acq + 1.2, ccsds_guard - 1.0),
                fontsize=8, fontweight="bold", color="white",
                arrowprops=dict(arrowstyle="->", color="white", lw=1.2),
                bbox=dict(boxstyle="round,pad=0.3", fc="black", alpha=0.7),
                zorder=11)

    # Conservative: T_acq=10, T_guard=10
    cons_acq, cons_guard = 10.0, 10.0
    cons_phy = _lookup_phy(sweep_result, cons_acq, cons_guard)
    ax.plot(cons_acq, cons_guard, marker="D", color="white", markersize=10,
            markeredgecolor="black", markeredgewidth=1.0, zorder=10)
    ax.annotate(f"Conservative\n{cons_phy:.0f} kbps",
                xy=(cons_acq, cons_guard), xytext=(cons_acq - 3.5, cons_guard - 1.5),
                fontsize=8, fontweight="bold", color="white",
                arrowprops=dict(arrowstyle="->", color="white", lw=1.2),
                bbox=dict(boxstyle="round,pad=0.3", fc="black", alpha=0.7),
                zorder=11)

    ax.set_xlabel("Acquisition time $T_{\\mathrm{acq}}$ (ms)")
    ax.set_ylabel("Guard interval $T_{\\mathrm{guard}}$ (ms)")
    ax.set_title("Minimum viable PHY rate for schedulability ($k_c=100$, $S=256$ B)")

    fig.tight_layout()
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {output_path}")


def _lookup_phy(sweep_result: dict, acq: float, guard: float) -> float:
    """Look up interpolated minimum PHY rate from sweep result."""
    acq_vals = sweep_result["acq_vals"]
    guard_vals = sweep_result["guard_vals"]
    Z = sweep_result["min_phy_kbps"]

    # Find nearest indices
    i_acq = np.argmin(np.abs(acq_vals - acq))
    i_guard = np.argmin(np.abs(guard_vals - guard))
    return Z[i_guard, i_acq]


def generate_gamma_vs_rate_figure(
    output_path: str,
    rate_result: Optional[dict] = None,
) -> None:
    """Generate gamma vs R_PHY curve for Model S and Model C.

    Saves to output_path as PDF.
    """
    _setup_matplotlib()
    import matplotlib.pyplot as plt

    if rate_result is None:
        phy_rates = np.linspace(15_000, 80_000, 200)
        rate_result = compute_gamma_vs_rate(phy_rates)

    rates_kbps = rate_result["phy_rates_kbps"]
    gamma_s = rate_result["gamma_simple"]
    gamma_c = rate_result["gamma_ccsds"]
    margin_s = rate_result["margin_simple_ms"]
    margin_c = rate_result["margin_ccsds_ms"]

    fig, ax = plt.subplots(1, 1, figsize=(6, 4))

    # Plot gamma curves
    ax.plot(rates_kbps, gamma_s, color="#0891b2", linewidth=2.0,
            label="Model S (simplified, no FEC/acq.)", linestyle="--")
    ax.plot(rates_kbps, gamma_c, color="#d97706", linewidth=2.0,
            label="Model C (CCSDS w/ FEC + acq.)")

    # Shade feasible region for Model C
    feasible_c = margin_c >= 0
    if feasible_c.any():
        # Find the boundary rate
        boundary_idx = np.where(feasible_c)[0][0]
        boundary_rate = rates_kbps[boundary_idx]

        ax.axvline(x=boundary_rate, color="#d97706", linestyle=":", alpha=0.7,
                   linewidth=1.2)
        ax.fill_between(rates_kbps, 0, 1,
                        where=feasible_c, alpha=0.12, color="#d97706",
                        label=f"Feasible (Model C, $\\geq$ {boundary_rate:.0f} kbps)")

    # Shade feasible region for Model S
    feasible_s = margin_s >= 0
    if feasible_s.any():
        boundary_idx_s = np.where(feasible_s)[0][0]
        boundary_rate_s = rates_kbps[boundary_idx_s]

        ax.axvline(x=boundary_rate_s, color="#0891b2", linestyle=":", alpha=0.7,
                   linewidth=1.2)
        ax.fill_between(rates_kbps, 0, 1,
                        where=feasible_s & ~feasible_c, alpha=0.08, color="#0891b2",
                        label=f"Feasible (Model S only, $\\geq$ {boundary_rate_s:.0f} kbps)")

    # Shade infeasible region (where neither model is feasible)
    infeasible = ~feasible_c & ~feasible_s
    if infeasible.any():
        ax.fill_between(rates_kbps, 0, 1,
                        where=infeasible, alpha=0.10, color="#dc2626",
                        hatch="//", edgecolor="#dc2626",
                        label="Infeasible ($k_c=100$)")

    # Mark reference PHY rates
    for ref_rate, ref_label in [(24, "24 kbps"), (30, "30 kbps")]:
        ref_idx = np.argmin(np.abs(rates_kbps - ref_rate))
        ax.axvline(x=ref_rate, color="gray", linestyle="-.", alpha=0.3)
        ax.annotate(ref_label, xy=(ref_rate, gamma_c[ref_idx]),
                    xytext=(ref_rate + 1.5, gamma_c[ref_idx] + 0.02),
                    fontsize=7, color="gray")

    ax.set_xlabel("PHY rate $R_{\\mathrm{PHY}}$ (kbps)")
    ax.set_ylabel("Slot efficiency $\\gamma$")
    ax.set_title("Slot efficiency vs. PHY rate ($k_c=100$, $S=256$ B)")
    ax.set_xlim(rates_kbps[0], rates_kbps[-1])
    # Tighten y-axis to the relevant range
    y_lo = min(gamma_s.min(), gamma_c.min()) - 0.05
    y_hi = max(gamma_s.max(), gamma_c.max()) + 0.05
    ax.set_ylim(max(0, y_lo), min(1.0, y_hi))
    ax.legend(loc="upper right", framealpha=0.9, fontsize=8)

    fig.tight_layout()
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {output_path}")


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(description="Packet-level TDMA simulator")
    parser.add_argument("--sweep-margin", action="store_true",
                        help="Generate margin-sensitivity and gamma-vs-rate figures")
    parser.add_argument("--fig-dir", type=str, default=None,
                        help="Output directory for figures")
    args = parser.parse_args()

    if args.sweep_margin:
        # Determine output directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        fig_dir = args.fig_dir or os.path.join(
            script_dir, "..", "drafts", "02-swarm-coordination-scaling", "figures"
        )
        os.makedirs(fig_dir, exist_ok=True)

        print("=" * 70)
        print("Generating margin-sensitivity figures")
        print("=" * 70)

        # --- Figure 1: Margin sensitivity contour ---
        print("\n--- Sweeping T_acq x T_guard feasibility ---")
        sweep_result = sweep_acq_guard_feasibility()
        margin_path = os.path.join(fig_dir, "fig-margin-sensitivity.pdf")
        generate_margin_sensitivity_figure(margin_path, sweep_result)

        # Print reference point values
        ccsds_phy = _lookup_phy(sweep_result, 5.0, 4.7)
        cons_phy = _lookup_phy(sweep_result, 10.0, 10.0)
        print(f"  CCSDS default (5.0, 4.7): {ccsds_phy:.1f} kbps")
        print(f"  Conservative  (10, 10):   {cons_phy:.1f} kbps")

        # --- Figure 2: Gamma vs rate ---
        print("\n--- Computing gamma vs. PHY rate ---")
        phy_rates = np.linspace(15_000, 80_000, 200)
        rate_result = compute_gamma_vs_rate(phy_rates)
        gamma_path = os.path.join(fig_dir, "fig-gamma-vs-rate.pdf")
        generate_gamma_vs_rate_figure(gamma_path, rate_result)

        print("\nDone.")

    else:
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
