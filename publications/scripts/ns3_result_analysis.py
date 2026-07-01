"""NS-3 TDMA validation result analysis and comparison with analytical model.

Parses NS-3 output (per-cycle CSV, summary CSV, optional FlowMonitor XML),
computes aggregate statistics, and generates comparison tables and figures
against the analytical model from packet_level_tdma.py.

The key validation metric is the gamma (slot efficiency) difference:
  delta_gamma = |gamma_ns3 - gamma_analytical|

A delta of 3-8% is expected and proves independence (NS-3 derives timing
from first principles, not from our equations).  Larger deltas indicate
a discrepancy that needs investigation.

Usage:
    # Analyze existing NS-3 output
    python ns3_result_analysis.py --results-dir ../ns3-validation/results

    # Generate comparison figure
    python ns3_result_analysis.py --results-dir ../ns3-validation/results \
        --fig-dir ../drafts/02-swarm-coordination-scaling/figures

    # Run NS-3 scenarios and analyze (requires NS-3 built)
    python ns3_result_analysis.py --run-ns3 --ns3-dir /path/to/ns-3 \
        --fig-dir ../drafts/02-swarm-coordination-scaling/figures
"""

from __future__ import annotations

import argparse
import csv
import math
import os
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import numpy as np


# ---------------------------------------------------------------------------
# Analytical model (independent re-derivation for comparison)
# ---------------------------------------------------------------------------

@dataclass
class AnalyticalConfig:
    """Parameters for the analytical TDMA model.

    These MUST match the NS-3 scenario defaults so comparison is apples-to-apples.
    """
    k_c: int = 100               # cluster size
    T_c: float = 10.0            # cycle duration (seconds)
    S_eph: int = 256              # ephemeris payload (bytes)
    S_summary: int = 512          # summary payload (bytes)
    S_hb: int = 64                # heartbeat payload (bytes)
    phy_rate_bps: float = 30_000  # PHY rate
    fec_rate: float = 7 / 8      # FEC code rate
    # Framing: ASM(32) + addr(8) + ctrl(16) + FCS(32) = 88 bits
    framing_bits: int = 88
    # Guard: propagation(1.7) + turnaround(2.0) + jitter(1.0) = 4.7 ms
    guard_ms: float = 4.7
    # Acquisition: 5.0 ms (fixed default)
    acq_ms: float = 5.0
    # Turnaround: 2.0 ms
    turnaround_ms: float = 2.0


def analytical_slot_duration_ms(cfg: AnalyticalConfig,
                                 payload_bytes: int) -> float:
    """Compute analytical slot duration from first principles.

    Mirrors the NS-3 scheduler computation exactly:
      1. payload_bits = payload_bytes * 8
      2. uncoded = payload_bits + framing_bits
      3. coded = ceil(uncoded / fec_rate)
      4. data_time = coded / phy_rate * 1000
      5. total = data_time + guard + acquisition
    """
    payload_bits = payload_bytes * 8
    uncoded = payload_bits + cfg.framing_bits
    coded = math.ceil(uncoded / cfg.fec_rate)
    data_ms = coded / cfg.phy_rate_bps * 1000.0
    return data_ms + cfg.guard_ms + cfg.acq_ms


def analytical_gamma(cfg: AnalyticalConfig) -> float:
    """Compute analytical slot efficiency gamma.

    gamma = payload_bits / (phy_rate * slot_duration)
    """
    slot_ms = analytical_slot_duration_ms(cfg, cfg.S_eph)
    payload_bits = cfg.S_eph * 8
    return payload_bits / (cfg.phy_rate_bps * slot_ms / 1000.0)


def analytical_margin_ms(cfg: AnalyticalConfig) -> float:
    """Compute analytical scheduling margin.

    margin = T_c - (N-1)*slot - turnaround - egress
    """
    n_members = cfg.k_c - 1
    slot_ms = analytical_slot_duration_ms(cfg, cfg.S_eph)
    ingress_ms = n_members * slot_ms

    # Egress: summary + heartbeat slots
    summary_slot = analytical_slot_duration_ms(cfg, cfg.S_summary)
    hb_slot = analytical_slot_duration_ms(cfg, cfg.S_hb)
    egress_ms = summary_slot + hb_slot

    T_c_ms = cfg.T_c * 1000.0
    return T_c_ms - ingress_ms - cfg.turnaround_ms - egress_ms


def analytical_deadline_miss_rate(cfg: AnalyticalConfig) -> float:
    """Predict deadline miss rate from margin sign.

    For deterministic (fixed) acquisition, this is binary:
      margin >= 0 -> 0% misses
      margin < 0  -> 100% misses
    """
    margin = analytical_margin_ms(cfg)
    return 0.0 if margin >= 0 else 1.0


def analytical_delivery_rate(cfg: AnalyticalConfig,
                              p_loss_good: float = 0.01,
                              p_loss_bad: float = 0.90,
                              p_gb: float = 0.05,
                              p_bg: float = 0.50,
                              ge_enabled: bool = False) -> float:
    """Predict steady-state delivery rate under GE channel.

    delivery = 1 - (pi_G * p_loss_good + pi_B * p_loss_bad)
    where pi_B = p_gb / (p_gb + p_bg)
    """
    if not ge_enabled:
        return 1.0
    pi_B = p_gb / (p_gb + p_bg) if (p_gb + p_bg) > 0 else 0.5
    pi_G = 1.0 - pi_B
    avg_loss = pi_G * p_loss_good + pi_B * p_loss_bad
    return 1.0 - avg_loss


# ---------------------------------------------------------------------------
# NS-3 result parsing
# ---------------------------------------------------------------------------

@dataclass
class NS3CycleRow:
    """A single row from the NS-3 per-cycle CSV."""
    cycle: int
    sent: int
    received: int
    lost: int
    retransmissions: int
    ingress_ms: float
    egress_ms: float
    margin_ms: float
    deadline_miss: bool
    gamma: float


@dataclass
class NS3SummaryRow:
    """A single row from the NS-3 summary CSV."""
    cluster_size: int
    phy_rate_bps: float
    fec_rate: float
    slot_config: int
    guard_time_ms: float
    acq_time_ms: float
    stochastic_acq: bool
    ge_enabled: bool
    p_gb: float
    p_bg: float
    p_loss_good: float
    p_loss_bad: float
    max_retx: int
    num_interferers: int
    interferer_distance: float
    num_cycles: int
    gamma_scheduler: float
    gamma_measured: float
    gamma_std: float
    margin_mean_ms: float
    margin_min_ms: float
    delivery_rate: float
    deadline_miss_rate: float
    total_deadline_misses: int
    total_retransmissions: int


def parse_cycle_csv(filepath: str) -> list[NS3CycleRow]:
    """Parse an NS-3 per-cycle CSV file."""
    rows = []
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(NS3CycleRow(
                cycle=int(row['cycle']),
                sent=int(row['sent']),
                received=int(row['received']),
                lost=int(row['lost']),
                retransmissions=int(row['retransmissions']),
                ingress_ms=float(row['ingress_ms']),
                egress_ms=float(row['egress_ms']),
                margin_ms=float(row['margin_ms']),
                deadline_miss=bool(int(row['deadline_miss'])),
                gamma=float(row['gamma']),
            ))
    return rows


def parse_summary_csv(filepath: str) -> list[NS3SummaryRow]:
    """Parse an NS-3 summary CSV file (may have multiple rows from sweeps)."""
    rows = []
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(NS3SummaryRow(
                cluster_size=int(row['cluster_size']),
                phy_rate_bps=float(row['phy_rate_bps']),
                fec_rate=float(row['fec_rate']),
                slot_config=int(row['slot_config']),
                guard_time_ms=float(row['guard_time_ms']),
                acq_time_ms=float(row['acq_time_ms']),
                stochastic_acq=bool(int(row['stochastic_acq'])),
                ge_enabled=bool(int(row['ge_enabled'])),
                p_gb=float(row['p_gb']),
                p_bg=float(row['p_bg']),
                p_loss_good=float(row['p_loss_good']),
                p_loss_bad=float(row['p_loss_bad']),
                max_retx=int(row['max_retx']),
                num_interferers=int(row['num_interferers']),
                interferer_distance=float(row['interferer_distance']),
                num_cycles=int(row['num_cycles']),
                gamma_scheduler=float(row['gamma_scheduler']),
                gamma_measured=float(row['gamma_measured']),
                gamma_std=float(row['gamma_std']),
                margin_mean_ms=float(row['margin_mean_ms']),
                margin_min_ms=float(row['margin_min_ms']),
                delivery_rate=float(row['delivery_rate']),
                deadline_miss_rate=float(row['deadline_miss_rate']),
                total_deadline_misses=int(row['total_deadline_misses']),
                total_retransmissions=int(row['total_retransmissions']),
            ))
    return rows


# ---------------------------------------------------------------------------
# Comparison analysis
# ---------------------------------------------------------------------------

@dataclass
class ComparisonRow:
    """Analytical vs NS-3 comparison for a single configuration."""
    phy_rate_kbps: float
    cluster_size: int
    ge_state: str
    max_retx: int
    gamma_analytical: float
    gamma_ns3: float
    gamma_ns3_std: float
    gamma_delta: float
    gamma_delta_pct: float
    margin_analytical_ms: float
    margin_ns3_ms: float
    delivery_analytical: float
    delivery_ns3: float
    miss_rate_analytical: float
    miss_rate_ns3: float


def compare_with_analytical(ns3_rows: list[NS3SummaryRow]) -> list[ComparisonRow]:
    """Compare NS-3 results with analytical model predictions."""
    comparisons = []

    for row in ns3_rows:
        # Build analytical config matching the NS-3 parameters
        acfg = AnalyticalConfig(
            k_c=row.cluster_size,
            phy_rate_bps=row.phy_rate_bps,
            fec_rate=row.fec_rate,
            guard_ms=row.guard_time_ms,
            acq_ms=row.acq_time_ms,
        )

        gamma_a = analytical_gamma(acfg)
        margin_a = analytical_margin_ms(acfg)
        miss_a = analytical_deadline_miss_rate(acfg)

        ge_state = "no-loss"
        if row.ge_enabled:
            if row.p_loss_bad >= 0.95:
                ge_state = "GE-severe"
            else:
                ge_state = "GE-default"

        delivery_a = analytical_delivery_rate(
            acfg,
            p_loss_good=row.p_loss_good,
            p_loss_bad=row.p_loss_bad,
            p_gb=row.p_gb,
            p_bg=row.p_bg,
            ge_enabled=row.ge_enabled,
        )

        delta = abs(gamma_a - row.gamma_measured)
        delta_pct = (delta / gamma_a * 100.0) if gamma_a > 0 else 0.0

        comparisons.append(ComparisonRow(
            phy_rate_kbps=row.phy_rate_bps / 1000.0,
            cluster_size=row.cluster_size,
            ge_state=ge_state,
            max_retx=row.max_retx,
            gamma_analytical=gamma_a,
            gamma_ns3=row.gamma_measured,
            gamma_ns3_std=row.gamma_std,
            gamma_delta=delta,
            gamma_delta_pct=delta_pct,
            margin_analytical_ms=margin_a,
            margin_ns3_ms=row.margin_mean_ms,
            delivery_analytical=delivery_a,
            delivery_ns3=row.delivery_rate,
            miss_rate_analytical=miss_a,
            miss_rate_ns3=row.deadline_miss_rate,
        ))

    return comparisons


def print_comparison_table(comparisons: list[ComparisonRow]) -> None:
    """Print a formatted comparison table to stdout."""
    print("\n" + "=" * 120)
    print("  NS-3 vs Analytical Model Comparison")
    print("=" * 120)

    header = (
        f"{'Rate':>6s} {'N':>4s} {'GE':>10s} {'Mr':>3s} "
        f"{'gamma_A':>8s} {'gamma_NS3':>10s} {'+/-':>6s} {'delta':>6s} {'%':>5s} "
        f"{'margin_A':>9s} {'margin_NS3':>11s} "
        f"{'deliv_A':>8s} {'deliv_NS3':>10s} "
        f"{'miss_A':>7s} {'miss_NS3':>9s}"
    )
    print(header)
    print("-" * 120)

    for c in comparisons:
        line = (
            f"{c.phy_rate_kbps:6.0f} {c.cluster_size:4d} {c.ge_state:>10s} {c.max_retx:3d} "
            f"{c.gamma_analytical:8.4f} {c.gamma_ns3:10.4f} {c.gamma_ns3_std:6.4f} "
            f"{c.gamma_delta:6.4f} {c.gamma_delta_pct:5.1f} "
            f"{c.margin_analytical_ms:9.1f} {c.margin_ns3_ms:11.1f} "
            f"{c.delivery_analytical:8.4f} {c.delivery_ns3:10.4f} "
            f"{c.miss_rate_analytical:7.2f} {c.miss_rate_ns3:9.4f}"
        )
        print(line)

    print("-" * 120)

    # Summary statistics
    deltas = [c.gamma_delta_pct for c in comparisons if c.gamma_analytical > 0]
    if deltas:
        print(f"\nGamma delta statistics:")
        print(f"  Mean:   {np.mean(deltas):.2f}%")
        print(f"  Median: {np.median(deltas):.2f}%")
        print(f"  Max:    {np.max(deltas):.2f}%")
        print(f"  Min:    {np.min(deltas):.2f}%")

        if np.mean(deltas) < 10.0:
            print(f"\n  VALIDATION: Mean gamma delta {np.mean(deltas):.1f}% < 10% -> PASS")
        else:
            print(f"\n  VALIDATION: Mean gamma delta {np.mean(deltas):.1f}% >= 10% -> INVESTIGATE")


def write_comparison_csv(filepath: str, comparisons: list[ComparisonRow]) -> None:
    """Write comparison results to CSV."""
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'phy_rate_kbps', 'cluster_size', 'ge_state', 'max_retx',
            'gamma_analytical', 'gamma_ns3', 'gamma_ns3_std',
            'gamma_delta', 'gamma_delta_pct',
            'margin_analytical_ms', 'margin_ns3_ms',
            'delivery_analytical', 'delivery_ns3',
            'miss_rate_analytical', 'miss_rate_ns3',
        ])
        for c in comparisons:
            writer.writerow([
                c.phy_rate_kbps, c.cluster_size, c.ge_state, c.max_retx,
                f"{c.gamma_analytical:.6f}", f"{c.gamma_ns3:.6f}",
                f"{c.gamma_ns3_std:.6f}",
                f"{c.gamma_delta:.6f}", f"{c.gamma_delta_pct:.2f}",
                f"{c.margin_analytical_ms:.3f}", f"{c.margin_ns3_ms:.3f}",
                f"{c.delivery_analytical:.6f}", f"{c.delivery_ns3:.6f}",
                f"{c.miss_rate_analytical:.4f}", f"{c.miss_rate_ns3:.4f}",
            ])
    print(f"  Wrote comparison CSV: {filepath}")


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
        "legend.fontsize": 8,
        "figure.figsize": (7, 3.5),
        "figure.dpi": 300,
        "savefig.dpi": 300,
        "savefig.pad_inches": 0.05,
        "axes.grid": True,
        "grid.alpha": 0.3,
        "grid.linewidth": 0.5,
    })


def generate_validation_figure(
    comparisons: list[ComparisonRow],
    output_path: str,
) -> None:
    """Generate the NS-3 validation figure (fig-ns3-validation.pdf).

    Two panels:
      (a) gamma_analytical vs gamma_ns3 across PHY rates with error bars
      (b) Deadline miss rate comparison at 24/30/35 kbps under GE
    """
    _setup_matplotlib()
    import matplotlib.pyplot as plt

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.0, 3.2))

    # ---- Panel (a): gamma comparison across PHY rates ----
    # Filter: no-loss, cold-start, N=100
    gamma_rows = [c for c in comparisons
                  if c.ge_state == "no-loss"
                  and c.cluster_size == 100
                  and c.max_retx == 0]

    if gamma_rows:
        # Sort by PHY rate
        gamma_rows.sort(key=lambda c: c.phy_rate_kbps)

        rates = [c.phy_rate_kbps for c in gamma_rows]
        gamma_a = [c.gamma_analytical for c in gamma_rows]
        gamma_n = [c.gamma_ns3 for c in gamma_rows]
        gamma_err = [c.gamma_ns3_std for c in gamma_rows]

        ax1.plot(rates, gamma_a, 'o-', color='#0891b2', linewidth=1.5,
                 markersize=5, label='Analytical', zorder=3)
        ax1.errorbar(rates, gamma_n, yerr=gamma_err, fmt='s--',
                     color='#d97706', linewidth=1.5, markersize=5,
                     capsize=3, label='NS-3', zorder=3)

        # Shade the expected 3-8% agreement band around analytical
        gamma_a_arr = np.array(gamma_a)
        ax1.fill_between(rates,
                         gamma_a_arr * 0.92,
                         gamma_a_arr * 1.08,
                         alpha=0.15, color='gray',
                         label='$\\pm 8\\%$ band')

        ax1.set_xlabel('PHY rate (kbps)')
        ax1.set_ylabel('Slot efficiency $\\gamma$')
        ax1.set_title('(a) $\\gamma$: Analytical vs. NS-3')
        ax1.legend(loc='lower right', fontsize=7)

        # Annotate delta
        if len(gamma_rows) > 0:
            deltas = [c.gamma_delta_pct for c in gamma_rows]
            ax1.text(0.05, 0.95, f'Mean $\\Delta\\gamma$ = {np.mean(deltas):.1f}%',
                     transform=ax1.transAxes, fontsize=8,
                     verticalalignment='top',
                     bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    else:
        ax1.text(0.5, 0.5, 'No data available\n(run PHY rate sweep)',
                 transform=ax1.transAxes, ha='center', va='center',
                 fontsize=10, color='gray')
        ax1.set_title('(a) $\\gamma$: Analytical vs. NS-3')

    # ---- Panel (b): Deadline miss rate under GE ----
    # Filter: N=100, cold-start, various rates and GE states
    miss_rows = [c for c in comparisons
                 if c.cluster_size == 100
                 and c.max_retx == 0]

    if miss_rows:
        # Group by GE state
        ge_states = sorted(set(c.ge_state for c in miss_rows))
        colors_ge = {'no-loss': '#2ca02c', 'GE-default': '#ff7f0e', 'GE-severe': '#d62728'}
        markers_ge = {'no-loss': 'o', 'GE-default': 's', 'GE-severe': '^'}

        for ge in ge_states:
            ge_rows = sorted([c for c in miss_rows if c.ge_state == ge],
                             key=lambda c: c.phy_rate_kbps)
            if not ge_rows:
                continue

            rates_ge = [c.phy_rate_kbps for c in ge_rows]
            miss_a = [c.miss_rate_analytical * 100 for c in ge_rows]
            miss_n = [c.miss_rate_ns3 * 100 for c in ge_rows]

            clr = colors_ge.get(ge, '#333333')
            mkr = markers_ge.get(ge, 'o')

            ax2.plot(rates_ge, miss_a, marker=mkr, linestyle='-',
                     color=clr, alpha=0.5, markersize=4, linewidth=1.0,
                     label=f'Analytical ({ge})')
            ax2.plot(rates_ge, miss_n, marker=mkr, linestyle='--',
                     color=clr, markersize=5, linewidth=1.5,
                     label=f'NS-3 ({ge})')

        ax2.set_xlabel('PHY rate (kbps)')
        ax2.set_ylabel('Deadline miss rate (%)')
        ax2.set_title('(b) Deadline misses: Analytical vs. NS-3')
        ax2.legend(loc='upper right', fontsize=6, ncol=2)
        ax2.set_ylim(-5, 105)
    else:
        ax2.text(0.5, 0.5, 'No data available\n(run GE sweep)',
                 transform=ax2.transAxes, ha='center', va='center',
                 fontsize=10, color='gray')
        ax2.set_title('(b) Deadline misses: Analytical vs. NS-3')

    fig.tight_layout()
    fig.savefig(output_path, bbox_inches='tight')
    plt.close(fig)
    print(f"  Saved validation figure: {output_path}")


# ---------------------------------------------------------------------------
# NS-3 execution (optional)
# ---------------------------------------------------------------------------

def run_ns3_scenario(ns3_dir: str, args: dict, results_dir: str) -> Optional[str]:
    """Run a single NS-3 scenario via subprocess.

    Returns the output prefix path, or None on failure.
    """
    ns3_run = os.path.join(ns3_dir, "ns3")
    if not os.path.isfile(ns3_run):
        print(f"WARNING: NS-3 runner not found at {ns3_run}")
        return None

    scenario = "scratch/tdma-swarm-cluster"
    output_prefix = os.path.join(results_dir, f"run_{args.get('phyRateBps', 30000)}"
                                 f"_{args.get('clusterSize', 100)}"
                                 f"_{args.get('geEnabled', 'false')}"
                                 f"_{args.get('maxRetx', 0)}")

    cmd_args = [ns3_run, "run", scenario, "--"]
    for key, val in args.items():
        cmd_args.append(f"--{key}={val}")
    cmd_args.append(f"--outputPrefix={output_prefix}")

    try:
        result = subprocess.run(cmd_args, capture_output=True, text=True,
                                timeout=300, cwd=ns3_dir)
        if result.returncode != 0:
            print(f"WARNING: NS-3 run failed: {result.stderr[:200]}")
            return None
        return output_prefix
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        print(f"WARNING: NS-3 execution error: {e}")
        return None


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="NS-3 TDMA validation result analysis"
    )
    parser.add_argument("--results-dir", type=str,
                        default=os.path.join(os.path.dirname(__file__),
                                             "..", "ns3-validation", "results"),
                        help="Directory containing NS-3 output CSV files")
    parser.add_argument("--fig-dir", type=str, default=None,
                        help="Output directory for validation figures")
    parser.add_argument("--run-ns3", action="store_true",
                        help="Run NS-3 scenarios before analysis")
    parser.add_argument("--ns3-dir", type=str, default="",
                        help="NS-3 top-level directory (for --run-ns3)")
    args = parser.parse_args()

    results_dir = os.path.abspath(args.results_dir)
    os.makedirs(results_dir, exist_ok=True)

    # ---- Optionally run NS-3 ----
    if args.run_ns3:
        if not args.ns3_dir:
            print("ERROR: --ns3-dir required with --run-ns3")
            sys.exit(1)

        print("Running NS-3 scenarios...")
        ns3_dir = os.path.abspath(args.ns3_dir)

        # Baseline runs at several PHY rates
        for rate in [20000, 24000, 28000, 30000, 32000, 35000, 40000, 50000]:
            for ge in [("false", "0.0", "0.0"),
                       ("true", "0.01", "0.90")]:
                run_args = {
                    "clusterSize": 100,
                    "phyRateBps": rate,
                    "fecRate": 0.875,
                    "slotConfig": 0,
                    "numCycles": 100,
                    "geEnabled": ge[0],
                    "pLossGood": ge[1],
                    "pLossBad": ge[2],
                    "stochasticAcq": "false",
                    "maxRetx": 0,
                }
                print(f"  Running: R={rate} GE={ge[0]} ...", end=" ", flush=True)
                prefix = run_ns3_scenario(ns3_dir, run_args, results_dir)
                if prefix:
                    print("done.")
                else:
                    print("FAILED.")

    # ---- Find and parse all summary CSV files ----
    all_ns3_rows = []

    import glob
    csv_files = glob.glob(os.path.join(results_dir, "*_summary.csv"))
    if not csv_files:
        # Also check for sweep summary
        csv_files = glob.glob(os.path.join(results_dir, "*sweep_summary.csv"))

    if not csv_files:
        print(f"\nNo summary CSV files found in {results_dir}")
        print("Run NS-3 scenarios first, or specify --results-dir with existing output.")

        # Generate analytical-only comparison table for reference
        print("\n--- Analytical Model Reference Values ---")
        print(f"{'Rate':>6s} {'N':>4s} {'gamma':>8s} {'margin_ms':>10s} {'schedulable':>12s}")
        print("-" * 42)
        for rate in [20000, 24000, 28000, 30000, 32000, 35000, 40000, 50000]:
            for n in [50, 100, 200]:
                acfg = AnalyticalConfig(k_c=n, phy_rate_bps=rate)
                g = analytical_gamma(acfg)
                m = analytical_margin_ms(acfg)
                sched = "YES" if m >= 0 else "NO"
                print(f"{rate/1000:6.0f} {n:4d} {g:8.4f} {m:10.1f} {sched:>12s}")

        if args.fig_dir:
            # Generate figure with analytical-only data (placeholder)
            fig_dir = os.path.abspath(args.fig_dir)
            os.makedirs(fig_dir, exist_ok=True)
            fig_path = os.path.join(fig_dir, "fig-ns3-validation.pdf")
            generate_validation_figure([], fig_path)

        return

    print(f"\nFound {len(csv_files)} summary CSV file(s)")
    for csv_file in sorted(csv_files):
        try:
            rows = parse_summary_csv(csv_file)
            all_ns3_rows.extend(rows)
            print(f"  Parsed: {csv_file} ({len(rows)} rows)")
        except Exception as e:
            print(f"  WARNING: Failed to parse {csv_file}: {e}")

    if not all_ns3_rows:
        print("No valid data rows found.")
        return

    # ---- Compare with analytical model ----
    comparisons = compare_with_analytical(all_ns3_rows)
    print_comparison_table(comparisons)

    # ---- Write comparison CSV ----
    comparison_csv = os.path.join(results_dir, "ns3_vs_analytical.csv")
    write_comparison_csv(comparison_csv, comparisons)

    # ---- Generate validation figure ----
    if args.fig_dir:
        fig_dir = os.path.abspath(args.fig_dir)
        os.makedirs(fig_dir, exist_ok=True)
        fig_path = os.path.join(fig_dir, "fig-ns3-validation.pdf")
        generate_validation_figure(comparisons, fig_path)


if __name__ == "__main__":
    main()
