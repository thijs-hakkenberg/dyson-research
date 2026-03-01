"""TDMA slot-level simulator for single-cluster verification.

Validates the analytical superframe budget (Table V in Paper 02) by
explicitly modeling slot scheduling, half-duplex partitioning, guard
times, and Gilbert-Elliott correlated losses at the slot level.

This bridges the gap between the message-layer DES (fluid-server ingress)
and the analytical TDMA feasibility claims.

Enhanced with:
- GE coherence-time parameter (ge_coherence_slots) for sensitivity analysis
- Command unicast fraction (cmd_unicast_fraction) for mixed addressing
- Parameter sweep functions for publication figures
"""

from __future__ import annotations

import argparse
import math
import os
import sys

import numpy as np
from dataclasses import dataclass, replace
from typing import Optional


@dataclass
class TDMAConfig:
    """TDMA superframe configuration matching Paper 02 Table V."""
    k_c: int = 100                  # cluster size (members + coordinator)
    phy_rate_bps: float = 24_000    # PHY rate (bps)
    T_c: float = 10.0               # cycle duration (seconds)
    S_eph: int = 256                # ephemeris report size (bytes)
    S_cmd: int = 512                # command size (bytes)
    S_hb: int = 64                  # heartbeat size (bytes)
    S_summary: int = 512            # coordinator summary size (bytes)
    preamble_bits: int = 32         # preamble/sync bits per slot
    header_bits: int = 16           # header bits per slot
    crc_bits: int = 16              # CRC bits per slot
    guard_time_ms: float = 4.7     # guard time per slot (ms)
    turnaround_ms: float = 2.0     # TX/RX turnaround (ms)
    gamma: float = 0.85            # MAC efficiency (conservative)

    # Gilbert-Elliott channel parameters
    p_G: float = 0.01              # loss probability in Good state
    p_B: float = 0.90              # loss probability in Bad state
    p_GB: float = 0.05             # Good -> Bad transition probability
    p_BG: float = 0.50             # Bad -> Good transition probability

    # Workload
    p_cmd: float = 0.0             # command probability per node per cycle
    n_retransmissions: int = 0     # max retransmissions per slot

    # GE coherence: controls intra-cycle state transitions.
    # Represents the channel coherence time in TDMA slot units.
    # At each retransmission slot, P(GE transition) = 1/ge_coherence_slots.
    # ge_coherence_slots=1: per-slot transitions (fast mixing, ARQ effective)
    # ge_coherence_slots=99 (k_c-1): per-cycle coherence (slow mixing, ARQ ineffective)
    # Default 0 means per-slot transitions (original behavior, equivalent to 1).
    ge_coherence_slots: int = 0

    # Command addressing: fraction of commands requiring per-node unicast.
    # 0.0 = all broadcast (default), 1.0 = all unicast.
    cmd_unicast_fraction: float = 0.0


def compute_slot_duration_ms(cfg: TDMAConfig, payload_bytes: int) -> float:
    """Compute TDMA slot duration: data + guard (no gamma division -- gamma is derived)."""
    payload_bits = payload_bytes * 8
    total_bits = cfg.preamble_bits + cfg.header_bits + payload_bits + cfg.crc_bits
    data_time_ms = total_bits / cfg.phy_rate_bps * 1000
    return data_time_ms + cfg.guard_time_ms


def _ge_transition(ge_state: bool, rng: np.random.Generator, p_GB: float, p_BG: float) -> bool:
    """Apply a single GE state transition."""
    if ge_state:  # currently Good
        if rng.random() < p_GB:
            return False
    else:  # currently Bad
        if rng.random() < p_BG:
            return True
    return ge_state


def run_tdma_simulation(
    cfg: TDMAConfig,
    n_cycles: int = 10_000,
    seed: int = 42,
    verbose: bool = False,
) -> dict:
    """Simulate TDMA slot scheduling for a single cluster.

    Models:
    - Ingress phase: k_c-1 members send reports in assigned TDMA slots
    - GE channel: slot-level loss with configurable coherence time
    - Half-duplex: coordinator cannot transmit during ingress
    - Egress phase: coordinator broadcasts/unicasts summary + commands
    - Guard times and turnaround between phases

    Returns dict with:
    - ingress_utilization: fraction of T_c used for ingress
    - egress_utilization: fraction of T_c used for egress
    - margin_ms: remaining time in cycle
    - delivery_rate: fraction of reports successfully received
    - deadline_misses: cycles where total time exceeded T_c
    - slot_waste_from_loss: airtime consumed by lost packets
    """
    rng = np.random.default_rng(seed)
    n_members = cfg.k_c - 1  # coordinator doesn't send to itself

    # Slot timing (compute_slot_duration_ms already includes guard)
    slot_with_guard_ms = compute_slot_duration_ms(cfg, cfg.S_eph)

    # Egress slots (already include guard)
    summary_slot_ms = compute_slot_duration_ms(cfg, cfg.S_summary)
    hb_slot_ms = compute_slot_duration_ms(cfg, cfg.S_hb)
    cmd_slot_ms = compute_slot_duration_ms(cfg, cfg.S_cmd)

    T_c_ms = cfg.T_c * 1000

    # GE steady-state probabilities
    if cfg.p_GB + cfg.p_BG > 0:
        pi_B = cfg.p_GB / (cfg.p_GB + cfg.p_BG)
    else:
        pi_B = 0.5  # i.i.d. case: no state transitions

    # GE coherence: 0 or 1 means per-slot (original behavior)
    coherence = max(1, cfg.ge_coherence_slots)

    # Per-cycle tracking
    total_reports_sent = 0
    total_reports_received = 0
    total_slot_waste_ms = 0.0
    deadline_misses = 0
    ingress_times_ms = []
    egress_times_ms = []
    margin_times_ms = []
    per_cycle_delivery = []

    # GE state per member link (True = Good, False = Bad)
    ge_states = rng.random(n_members) > pi_B  # initialize to steady-state

    # Pre-compute loop-invariant egress values
    turnaround_time = cfg.turnaround_ms
    cmd_egress_time = 0.0
    if cfg.p_cmd > 0:
        n_commands = int(np.round(cfg.p_cmd * n_members))
        if n_commands > 0:
            # Broadcast portion
            n_unicast = round(cfg.cmd_unicast_fraction * n_members)
            n_broadcast = 1 if cfg.cmd_unicast_fraction < 1.0 else 0
            cmd_egress_time = n_broadcast * cmd_slot_ms + n_unicast * cmd_slot_ms

    for cycle in range(n_cycles):
        ingress_time = 0.0
        reports_received = 0
        slot_waste = 0.0

        # === INGRESS PHASE: members send reports ===
        for m in range(n_members):
            # Inter-cycle GE transition: always applied once per member per
            # cycle.  This models the channel evolving between cycles
            # regardless of coherence time.
            ge_states[m] = _ge_transition(
                ge_states[m], rng, cfg.p_GB, cfg.p_BG
            )

            # Determine if this slot's transmission succeeds
            p_loss = cfg.p_G if ge_states[m] else cfg.p_B
            lost = rng.random() < p_loss

            # Slot consumes airtime regardless of success
            ingress_time += slot_with_guard_ms
            total_reports_sent += 1

            if lost:
                slot_waste += slot_with_guard_ms

                # Retransmission attempts
                for retry in range(cfg.n_retransmissions):
                    # Intra-cycle GE transition: gated by coherence.
                    # P(transition) = 1/coherence at each retry slot.
                    # coherence=1: always transition (fast mixing, ARQ effective)
                    # coherence=99: ~1% chance (slow mixing, ARQ ineffective)
                    if coherence <= 1 or rng.random() < (1.0 / coherence):
                        ge_states[m] = _ge_transition(
                            ge_states[m], rng, cfg.p_GB, cfg.p_BG
                        )

                    p_loss_retry = cfg.p_G if ge_states[m] else cfg.p_B
                    retry_lost = rng.random() < p_loss_retry
                    ingress_time += slot_with_guard_ms

                    if not retry_lost:
                        reports_received += 1
                        break
                    else:
                        slot_waste += slot_with_guard_ms
            else:
                reports_received += 1

        # === EGRESS PHASE: coordinator sends summary + heartbeat + commands ===
        egress_time = summary_slot_ms + hb_slot_ms + cmd_egress_time

        total_time = ingress_time + turnaround_time + egress_time
        margin = T_c_ms - total_time

        ingress_times_ms.append(ingress_time)
        egress_times_ms.append(egress_time)
        margin_times_ms.append(margin)
        total_reports_received += reports_received
        total_slot_waste_ms += slot_waste
        per_cycle_delivery.append(reports_received / n_members)

        if margin < 0:
            deadline_misses += 1

    ingress_arr = np.array(ingress_times_ms)
    egress_arr = np.array(egress_times_ms)
    margin_arr = np.array(margin_times_ms)
    delivery_arr = np.array(per_cycle_delivery)

    results = {
        "n_cycles": n_cycles,
        "n_members": n_members,
        "slot_duration_ms": slot_with_guard_ms,
        "ingress_mean_ms": float(np.mean(ingress_arr)),
        "ingress_p99_ms": float(np.percentile(ingress_arr, 99)),
        "egress_mean_ms": float(np.mean(egress_arr)),
        "margin_mean_ms": float(np.mean(margin_arr)),
        "margin_min_ms": float(np.min(margin_arr)),
        "delivery_rate": float(total_reports_received / total_reports_sent),
        "per_cycle_delivery_mean": float(np.mean(delivery_arr)),
        "per_cycle_delivery_p01": float(np.percentile(delivery_arr, 1)),
        "deadline_misses": deadline_misses,
        "deadline_miss_rate": deadline_misses / n_cycles,
        "slot_waste_fraction": total_slot_waste_ms / (n_cycles * T_c_ms),
        "analytical_ingress_ms": n_members * slot_with_guard_ms,
        "analytical_margin_ms": T_c_ms - n_members * slot_with_guard_ms - cfg.turnaround_ms - (summary_slot_ms + hb_slot_ms),
    }

    return results


# ---------------------------------------------------------------------------
# Parameter sweep functions
# ---------------------------------------------------------------------------

def sweep_ge_coherence(
    cfg_base: TDMAConfig,
    coherence_values: list[int],
    n_retransmissions_values: list[int],
    n_cycles: int = 10_000,
    seed: int = 42,
) -> dict:
    """Sweep GE coherence time for multiple retransmission counts.

    Returns dict with keys:
    - coherence_values: list of coherence slot counts
    - results: dict mapping M_r -> list of result dicts (one per coherence value)
    """
    results = {}
    for mr in n_retransmissions_values:
        mr_results = []
        for coh in coherence_values:
            cfg = replace(cfg_base, ge_coherence_slots=coh, n_retransmissions=mr)
            r = run_tdma_simulation(cfg, n_cycles=n_cycles, seed=seed)
            r["ge_coherence_slots"] = coh
            r["n_retransmissions"] = mr
            mr_results.append(r)
        results[mr] = mr_results
    return {"coherence_values": coherence_values, "results": results}


def sweep_unicast_fraction(
    cfg_base: TDMAConfig,
    q_values: list[float],
    n_cycles: int = 10_000,
    seed: int = 42,
) -> dict:
    """Sweep command unicast fraction.

    Returns dict with keys:
    - q_values: list of unicast fractions
    - results: list of result dicts (one per q value)
    - analytical_L: list of analytical stagger cycles
    """
    sim_results = []
    analytical_L = []
    n_members = cfg_base.k_c - 1
    cmd_slot_ms = compute_slot_duration_ms(cfg_base, cfg_base.S_cmd)
    T_c_ms = cfg_base.T_c * 1000
    slot_with_guard_ms = compute_slot_duration_ms(cfg_base, cfg_base.S_eph)
    summary_slot_ms = compute_slot_duration_ms(cfg_base, cfg_base.S_summary)
    hb_slot_ms = compute_slot_duration_ms(cfg_base, cfg_base.S_hb)
    ingress_ms = n_members * slot_with_guard_ms
    fixed_egress_ms = summary_slot_ms + hb_slot_ms + cfg_base.turnaround_ms
    available_egress_ms = T_c_ms - ingress_ms - fixed_egress_ms

    for q in q_values:
        cfg = replace(cfg_base, cmd_unicast_fraction=q, p_cmd=1.0)
        r = run_tdma_simulation(cfg, n_cycles=n_cycles, seed=seed)
        r["cmd_unicast_fraction"] = q
        sim_results.append(r)

        # Analytical L_cmd(q)
        n_unicast = round(q * n_members)
        n_broadcast = 1 if q < 1.0 else 0
        total_cmd_ms = (n_broadcast + n_unicast) * cmd_slot_ms
        if total_cmd_ms <= available_egress_ms:
            L = 1
        else:
            L = math.ceil(total_cmd_ms / available_egress_ms)
        analytical_L.append(L)

    return {
        "q_values": q_values,
        "results": sim_results,
        "analytical_L": analytical_L,
    }


def sweep_gamma(
    cfg_base: TDMAConfig,
    gamma_values: list[float] | None = None,
    phy_rates: list[float] | None = None,
    n_cycles: int = 10_000,
    seed: int = 42,
) -> dict:
    """Sweep MAC efficiency γ at multiple PHY rates.

    For each γ, computes the required guard_time_ms = data_time_ms × (1/γ - 1),
    then runs the TDMA simulation.  Reports margin, deadline miss rate, and
    schedulability for each (γ, PHY rate) pair.

    Returns dict with keys:
    - gamma_values: list of γ values
    - phy_rates: list of PHY rates
    - results: dict mapping phy_rate -> list of result dicts (one per γ)
    """
    if gamma_values is None:
        gamma_values = [0.60, 0.65, 0.67, 0.70, 0.75, 0.80, 0.85, 0.90, 0.949]
    if phy_rates is None:
        phy_rates = [24_000, 30_000]

    all_results: dict[float, list[dict]] = {}
    for rate in phy_rates:
        rate_results = []
        for g in gamma_values:
            # Compute guard time from γ: γ = data / (data + guard)
            # => guard = data × (1/γ - 1)
            payload_bits = cfg_base.S_eph * 8
            total_bits = (cfg_base.preamble_bits + cfg_base.header_bits
                          + payload_bits + cfg_base.crc_bits)
            data_time_ms = total_bits / rate * 1000
            guard_ms = data_time_ms * (1.0 / g - 1.0)

            cfg = replace(
                cfg_base,
                phy_rate_bps=rate,
                gamma=g,
                guard_time_ms=guard_ms,
            )
            r = run_tdma_simulation(cfg, n_cycles=n_cycles, seed=seed)
            r["gamma"] = g
            r["phy_rate_bps"] = rate
            r["guard_time_ms"] = guard_ms
            r["schedulable"] = r["deadline_misses"] == 0
            rate_results.append(r)
        all_results[rate] = rate_results

    return {
        "gamma_values": gamma_values,
        "phy_rates": phy_rates,
        "results": all_results,
    }


def sweep_phy_rate(
    cfg_base: TDMAConfig,
    phy_rates: list[float],
    n_cycles: int = 10_000,
    seed: int = 42,
) -> dict:
    """Sweep PHY rate.

    Returns dict with keys:
    - phy_rates: list of PHY rates
    - results: list of result dicts
    """
    sim_results = []
    for rate in phy_rates:
        cfg = replace(cfg_base, phy_rate_bps=rate)
        r = run_tdma_simulation(cfg, n_cycles=n_cycles, seed=seed)
        r["phy_rate_bps"] = rate
        sim_results.append(r)
    return {"phy_rates": phy_rates, "results": sim_results}


def sweep_phy_rate_ge_joint(
    cfg_base: TDMAConfig,
    phy_rates: Optional[list[float]] = None,
    n_cycles: int = 10_000,
    seed: int = 42,
) -> dict:
    """Sweep PHY rate × channel condition for TDMA-aware joint interaction.

    Conditions:
    - No Loss:     p_G=0, p_B=0, M_r=0
    - GE M_r=0:    default GE, no retry
    - GE M_r=1:    default GE, 1 retry
    - GE+Exc:      GE M_r=0, p_exc=0.10 (p_cmd=0, reduced offered load)

    Returns dict with keys:
    - phy_rates: list of PHY rates
    - conditions: list of condition labels
    - results: dict mapping condition_label -> list of result dicts (one per rate)
    """
    if phy_rates is None:
        phy_rates = [15_000, 20_000, 24_000, 25_000, 30_000, 50_000]

    conditions = {
        "No Loss": lambda rate: replace(
            cfg_base, phy_rate_bps=rate, p_G=0.0, p_B=0.0,
            n_retransmissions=0, p_cmd=0.0,
        ),
        "GE $M_r$=0": lambda rate: replace(
            cfg_base, phy_rate_bps=rate, n_retransmissions=0, p_cmd=0.0,
        ),
        "GE $M_r$=1": lambda rate: replace(
            cfg_base, phy_rate_bps=rate, n_retransmissions=1, p_cmd=0.0,
        ),
        "GE+Exc": lambda rate: replace(
            cfg_base, phy_rate_bps=rate, n_retransmissions=0,
            p_cmd=0.0,
        ),
    }

    all_results = {}
    for label, cfg_fn in conditions.items():
        cond_results = []
        for rate in phy_rates:
            cfg = cfg_fn(rate)
            r = run_tdma_simulation(cfg, n_cycles=n_cycles, seed=seed)
            r["phy_rate_bps"] = rate
            r["condition"] = label
            cond_results.append(r)
        all_results[label] = cond_results

    return {
        "phy_rates": phy_rates,
        "conditions": list(conditions.keys()),
        "results": all_results,
    }


# ---------------------------------------------------------------------------
# Figure generation
# ---------------------------------------------------------------------------

def generate_figures(output_dir: str) -> None:
    """Generate publication-quality PDF figures for Paper 02 BV.

    Produces:
    1. fig-tdma-ge-sensitivity.pdf (2 panels): delivery rate and deadline miss
       rate vs GE coherence for M_r in {0, 1, 2}
    2. fig-unicast-stagger.pdf (1 panel): stagger cycles vs unicast fraction
       at 24 kbps and 30 kbps with analytical overlay
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.ticker import MaxNLocator

    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 9,
        "axes.labelsize": 9,
        "axes.titlesize": 9,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "legend.fontsize": 7.5,
        "figure.dpi": 300,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.02,
    })

    os.makedirs(output_dir, exist_ok=True)

    # -----------------------------------------------------------------------
    # Figure 1: GE coherence sensitivity (2 panels)
    # -----------------------------------------------------------------------
    # Coherence values: 1 (per-slot, ~93 ms) to 99 (per-cycle, ~10 s)
    coherence_values = [1, 2, 5, 10, 20, 50, 99]
    mr_values = [0, 1, 2]

    cfg_ge = TDMAConfig(p_cmd=0.0)  # GE default, no commands
    sweep = sweep_ge_coherence(
        cfg_ge, coherence_values, mr_values, n_cycles=10_000, seed=42
    )

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.5, 2.6))

    slot_ms = compute_slot_duration_ms(cfg_ge, cfg_ge.S_eph)
    coherence_labels = [f"{c}" for c in coherence_values]

    markers = ["o", "s", "^"]
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c"]

    for i, mr in enumerate(mr_values):
        delivery = [r["per_cycle_delivery_mean"] for r in sweep["results"][mr]]
        miss_rate = [r["deadline_miss_rate"] for r in sweep["results"][mr]]

        ax1.plot(coherence_values, delivery, marker=markers[i], color=colors[i],
                 label=f"$M_r = {mr}$", markersize=4, linewidth=1.2)
        ax2.plot(coherence_values, [m * 100 for m in miss_rate],
                 marker=markers[i], color=colors[i],
                 label=f"$M_r = {mr}$", markersize=4, linewidth=1.2)

    ax1.set_xscale("log")
    ax1.set_xlabel("GE coherence (slots)")
    ax1.set_ylabel("Intra-cycle delivery rate")
    ax1.set_ylim(0.0, 1.05)
    ax1.legend(loc="lower right")
    ax1.set_title("(a) Delivery rate vs. coherence")
    ax1.set_xticks(coherence_values)
    ax1.set_xticklabels(coherence_labels)

    ax2.set_xscale("log")
    ax2.set_xlabel("GE coherence (slots)")
    ax2.set_ylabel("Deadline miss rate (%)")
    ax2.legend(loc="upper left")
    ax2.set_title("(b) Deadline misses vs. coherence")
    ax2.set_xticks(coherence_values)
    ax2.set_xticklabels(coherence_labels)

    fig.tight_layout()
    path1 = os.path.join(output_dir, "fig-tdma-ge-sensitivity.pdf")
    fig.savefig(path1)
    plt.close(fig)
    print(f"  Saved: {path1}")

    # -----------------------------------------------------------------------
    # Figure 2: Unicast stagger design curve (1 panel)
    # -----------------------------------------------------------------------
    q_values = [0.0, 0.01, 0.02, 0.05, 0.10, 0.20, 0.30, 0.50, 0.75, 1.0]

    fig2, ax3 = plt.subplots(1, 1, figsize=(3.4, 2.6))

    for rate, ls, clr, lbl in [
        (24_000, "-", "#1f77b4", "24 kbps"),
        (30_000, "--", "#ff7f0e", "30 kbps"),
    ]:
        cfg_uni = TDMAConfig(p_G=0.0, p_B=0.0, p_cmd=1.0, phy_rate_bps=rate)
        sweep_uni = sweep_unicast_fraction(cfg_uni, q_values, n_cycles=1_000, seed=42)

        # Simulated: count cycles where margin < 0
        sim_L = []
        for r in sweep_uni["results"]:
            if r["margin_mean_ms"] >= 0:
                sim_L.append(1)
            else:
                # Estimate L from how much egress overflows
                overflow_ms = -r["margin_mean_ms"]
                n_members = cfg_uni.k_c - 1
                slot_ms = compute_slot_duration_ms(cfg_uni, cfg_uni.S_eph)
                summary_ms = compute_slot_duration_ms(cfg_uni, cfg_uni.S_summary)
                hb_ms = compute_slot_duration_ms(cfg_uni, cfg_uni.S_hb)
                avail = cfg_uni.T_c * 1000 - n_members * slot_ms - cfg_uni.turnaround_ms - summary_ms - hb_ms
                cmd_ms = compute_slot_duration_ms(cfg_uni, cfg_uni.S_cmd)
                q = r["cmd_unicast_fraction"]
                n_uni = round(q * n_members)
                n_bc = 1 if q < 1.0 else 0
                total_cmd = (n_bc + n_uni) * cmd_ms
                sim_L.append(max(1, math.ceil(total_cmd / max(avail, 1))))

        ax3.plot(q_values, sweep_uni["analytical_L"], marker="o", linestyle=ls,
                 color=clr, markersize=4, linewidth=1.2,
                 label=f"Analytical ({lbl})")
        ax3.plot(q_values, sim_L, marker="x", linestyle="none",
                 color=clr, markersize=5, linewidth=1.0,
                 label=f"Sim ({lbl})")

    ax3.set_xlabel("Unicast fraction $q$")
    ax3.set_ylabel("Stagger cycles $L_{\\mathrm{cmd}}$")
    ax3.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax3.legend(loc="upper left", fontsize=7)
    ax3.set_xlim(-0.02, 1.02)

    fig2.tight_layout()
    path2 = os.path.join(output_dir, "fig-unicast-stagger.pdf")
    fig2.savefig(path2)
    plt.close(fig2)
    print(f"  Saved: {path2}")


# ---------------------------------------------------------------------------
# Comparison table (original CLI entry point)
# ---------------------------------------------------------------------------

def run_comparison_table(seed: int = 42) -> None:
    """Run the TDMA simulation under multiple conditions and print comparison table."""

    print("=" * 80)
    print("TDMA Slot-Level Simulation vs Analytical Superframe Budget")
    print("=" * 80)

    configs = [
        ("Nominal (no loss)", TDMAConfig(p_G=0.0, p_B=0.0, p_cmd=0.0)),
        ("Nominal + broadcast cmd", TDMAConfig(p_G=0.0, p_B=0.0, p_cmd=1.0)),
        ("GE default (no ARQ)", TDMAConfig(p_cmd=0.0, n_retransmissions=0)),
        ("GE + 1 retry", TDMAConfig(p_cmd=0.0, n_retransmissions=1)),
        ("GE + 2 retries", TDMAConfig(p_cmd=0.0, n_retransmissions=2)),
        ("i.i.d. loss (p=0.125)", TDMAConfig(p_G=0.125, p_B=0.125, p_GB=0.0, p_BG=0.0, p_cmd=0.0)),
        ("Nominal, 30 kbps", TDMAConfig(p_G=0.0, p_B=0.0, p_cmd=0.0, phy_rate_bps=30_000)),
        ("GE, 30 kbps", TDMAConfig(p_cmd=0.0, phy_rate_bps=30_000, n_retransmissions=0)),
    ]

    print(f"\n{'Scenario':<30} {'Ingress':>10} {'Egress':>8} {'Margin':>8} {'Deadline':>10} {'Delivery':>10} {'Waste':>8}")
    print(f"{'':30} {'(ms)':>10} {'(ms)':>8} {'(ms)':>8} {'Misses':>10} {'Rate':>10} {'Frac':>8}")
    print("-" * 85)

    for name, cfg in configs:
        r = run_tdma_simulation(cfg, n_cycles=10_000, seed=seed)
        print(f"{name:<30} {r['ingress_mean_ms']:10.1f} {r['egress_mean_ms']:8.1f} "
              f"{r['margin_mean_ms']:8.1f} {r['deadline_misses']:10d} "
              f"{r['per_cycle_delivery_mean']:10.4f} {r['slot_waste_fraction']:8.4f}")

    print("-" * 85)

    # Analytical comparison
    cfg_nom = TDMAConfig(p_G=0.0, p_B=0.0)
    r_nom = run_tdma_simulation(cfg_nom, n_cycles=1000, seed=seed)
    print(f"\nAnalytical vs Simulated (Nominal, no loss):")
    print(f"  Analytical ingress: {r_nom['analytical_ingress_ms']:.1f} ms")
    print(f"  Simulated ingress:  {r_nom['ingress_mean_ms']:.1f} ms")
    print(f"  Analytical margin:  {r_nom['analytical_margin_ms']:.1f} ms")
    print(f"  Simulated margin:   {r_nom['margin_mean_ms']:.1f} ms")

    # GE retransmission analysis
    print(f"\nGE Retransmission Airtime Analysis:")
    for n_retry in [0, 1, 2]:
        cfg_ge = TDMAConfig(p_cmd=0.0, n_retransmissions=n_retry)
        r_ge = run_tdma_simulation(cfg_ge, n_cycles=10_000, seed=seed)
        print(f"  M_r={n_retry}: ingress={r_ge['ingress_mean_ms']:.1f} ms, "
              f"margin={r_ge['margin_mean_ms']:.1f} ms, "
              f"deadline_misses={r_ge['deadline_misses']}/10000, "
              f"delivery={r_ge['per_cycle_delivery_mean']:.4f}")

    # GE coherence sensitivity summary
    print(f"\nGE Coherence Sensitivity:")
    for coh in [1, 10, 99]:
        for mr in [0, 1, 2]:
            cfg_coh = TDMAConfig(p_cmd=0.0, n_retransmissions=mr, ge_coherence_slots=coh)
            r_coh = run_tdma_simulation(cfg_coh, n_cycles=10_000, seed=seed)
            print(f"  coherence={coh:3d}, M_r={mr}: "
                  f"delivery={r_coh['per_cycle_delivery_mean']:.4f}, "
                  f"deadline_misses={r_coh['deadline_misses']}/10000")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TDMA slot-level simulator")
    parser.add_argument("--figures", action="store_true",
                        help="Generate publication figures")
    parser.add_argument("--output-dir", type=str,
                        default="publications/drafts/02-swarm-coordination-scaling/figures",
                        help="Output directory for figures")
    args = parser.parse_args()

    if args.figures:
        print("Generating figures...")
        generate_figures(args.output_dir)
        print("Done.")
    else:
        run_comparison_table()
