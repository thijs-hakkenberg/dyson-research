#!/usr/bin/env python3
"""Run simulation sweeps to populate table values in Paper 02 tex.

All runs use full-fidelity simulation (sync_sample_rate=1.0) with 30 Monte
Carlo replications per configuration for statistically robust CIs.

Usage:
    cd publications/scripts
    python3 -u run_table_sweeps.py
"""
from __future__ import annotations

import json
import sys
import time

import numpy as np

from swarm_model import (
    SwarmCoordinationConfig,
    SwarmCoordinationSimulator,
)


def flush_print(*args, **kwargs):
    print(*args, **kwargs)
    sys.stdout.flush()


def run_single(config: SwarmCoordinationConfig) -> dict:
    """Run a single DES and return key metrics."""
    sim = SwarmCoordinationSimulator(config)
    result = sim.run()
    total_attempted = result.total_messages_sent + getattr(result, 'coordinator_drops', 0)
    coord_drop_pct = (
        getattr(result, 'coordinator_drops', 0) / total_attempted * 100
        if total_attempted > 0 else 0.0
    )
    return {
        "overhead": result.communication_overhead_percent,
        "queue_drop_rate": result.message_drop_rate * 100,
        "exc_reduction": result.exception_telemetry_reduction,
        "loss_rate": result.message_loss_rate * 100,
        "coord_drops": getattr(result, 'coordinator_drops', 0),
        "coord_drop_pct": coord_drop_pct,
        "retransmission_count": getattr(result, 'retransmission_count', 0),
        "total_msgs_sent": result.total_messages_sent,
        "total_msgs_delivered": result.total_messages_delivered,
        "coordination_success": 1.0 - result.message_drop_rate - result.message_loss_rate,
    }


def run_mc(base_config: dict, n_runs: int = 30) -> dict:
    """Run n_runs with different seeds and return mean + 95% CI."""
    all_results = []
    for i in range(n_runs):
        cfg = SwarmCoordinationConfig(**{**base_config, "seed": 42 + i})
        all_results.append(run_single(cfg))

    keys = all_results[0].keys()
    means = {}
    ci_lo = {}
    ci_hi = {}
    stds = {}
    for k in keys:
        vals = [r[k] for r in all_results]
        means[k] = float(np.mean(vals))
        stds[k] = float(np.std(vals, ddof=1)) if len(vals) > 1 else 0.0
        # 95% CI via bootstrap percentile
        rng = np.random.default_rng(123)
        boot_means = []
        for _ in range(2000):
            sample = rng.choice(vals, size=len(vals), replace=True)
            boot_means.append(np.mean(sample))
        ci_lo[k] = float(np.percentile(boot_means, 2.5))
        ci_hi[k] = float(np.percentile(boot_means, 97.5))

    return {"mean": means, "std": stds, "ci_lo": ci_lo, "ci_hi": ci_hi}


# Common base config: full fidelity, 1 day
FULL_FIDELITY_BASE = {
    "coordination_topology": "hierarchical",
    "cluster_size": 100,
    "simulation_days": 1,
    "sync_sample_rate": 1.0,  # full fidelity — no node sampling
}

N_MC = 30  # Monte Carlo replications per config


def sweep_scaling():
    """Table VI: Hierarchical overhead at different N (full fidelity, 30 MC runs)."""
    flush_print("=" * 60)
    flush_print(f"SWEEP 1: Scaling Trajectory (Table VI) — {N_MC} MC runs, full fidelity")
    flush_print("=" * 60)

    node_counts = [1_000, 5_000, 10_000, 20_000, 30_000,
                   40_000, 50_000, 60_000, 80_000, 100_000]

    results = {}
    for N in node_counts:
        base = {**FULL_FIDELITY_BASE, "node_count": N}
        t0 = time.time()
        res = run_mc(base, N_MC)
        elapsed = time.time() - t0
        results[N] = res
        m = res["mean"]
        s = res["std"]
        flush_print(f"  N={N:>10,}: overhead={m['overhead']:.2f}% "
                    f"(SD={s['overhead']:.3f}%, 95%CI=[{res['ci_lo']['overhead']:.2f},"
                    f"{res['ci_hi']['overhead']:.2f}]) "
                    f"msgs={m['total_msgs_sent']:.0f} [{elapsed:.1f}s]")

    return results


def sweep_exception():
    """Table VIII: Exception telemetry multi-scale validation (full fidelity)."""
    flush_print("\n" + "=" * 60)
    flush_print(f"SWEEP 2: Exception Telemetry (Table VIII) — {N_MC} MC runs")
    flush_print("=" * 60)

    configs = [
        (10_000, 0.10),
        (10_000, 0.30),
        (10_000, 0.50),
        (100_000, 0.10),
        (100_000, 0.30),
        (100_000, 0.50),
    ]

    results = {}
    for N, p_exc in configs:
        # Baseline (no exception)
        base_cfg = {**FULL_FIDELITY_BASE, "node_count": N}
        base_res = run_mc(base_cfg, N_MC)

        # With exception telemetry
        exc_cfg = {
            **base_cfg,
            "enable_exception_telemetry": True,
            "exception_threshold": p_exc,
        }
        t0 = time.time()
        exc_res = run_mc(exc_cfg, N_MC)
        elapsed = time.time() - t0

        key = f"N={N},p={p_exc}"
        results[key] = {
            "base_overhead": base_res["mean"]["overhead"],
            "exc_overhead": exc_res["mean"]["overhead"],
            "reduction": exc_res["mean"]["exc_reduction"],
            "reduction_std": exc_res["std"]["exc_reduction"],
            "error_vs_analytical": abs(exc_res["mean"]["exc_reduction"] - p_exc),
        }
        flush_print(f"  N={N:>10,}, p_exc={p_exc:.2f}: "
                    f"reduction={exc_res['mean']['exc_reduction']:.4f} "
                    f"(SD={exc_res['std']['exc_reduction']:.4f}), "
                    f"err={abs(exc_res['mean']['exc_reduction'] - p_exc):.4f} "
                    f"[{elapsed:.1f}s]")

    return results


def sweep_link():
    """Table VII: Link availability with retransmission (full fidelity)."""
    flush_print("\n" + "=" * 60)
    flush_print(f"SWEEP 3: Link Availability (Table VII) — {N_MC} MC runs")
    flush_print("=" * 60)

    p_link_values = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4]
    N = 10_000

    results = {}
    for p_link in p_link_values:
        base = {**FULL_FIDELITY_BASE, "node_count": N, "link_availability": p_link}

        # M_r = 0
        res0 = run_mc({**base, "max_retransmissions": 0}, N_MC)

        # M_r = 2
        t0 = time.time()
        res2 = run_mc({**base, "max_retransmissions": 2}, N_MC)
        elapsed = time.time() - t0

        results[str(p_link)] = {
            "overhead_M0": res0["mean"]["overhead"],
            "overhead_M2": res2["mean"]["overhead"],
            "loss_M0": res0["mean"]["loss_rate"],
            "loss_M2": res2["mean"]["loss_rate"],
            "success_M0": res0["mean"]["coordination_success"] * 100,
            "success_M2": res2["mean"]["coordination_success"] * 100,
        }
        flush_print(f"  p_link={p_link:.1f}: "
                    f"oh_M0={res0['mean']['overhead']:.2f}%, "
                    f"oh_M2={res2['mean']['overhead']:.2f}%, "
                    f"loss_M0={res0['mean']['loss_rate']:.1f}%, "
                    f"loss_M2={res2['mean']['loss_rate']:.1f}% "
                    f"[{elapsed:.1f}s]")

    return results


def sweep_coordinator_bw():
    """Table IX: Coordinator bandwidth parameterization (full fidelity).

    Also computes MAC-adjusted thresholds: for TDMA with efficiency gamma,
    the required raw link capacity is C_coord / gamma.
    """
    flush_print("\n" + "=" * 60)
    flush_print(f"SWEEP 4: Coordinator Bandwidth (Table IX) — {N_MC} MC runs")
    flush_print("=" * 60)

    N = 10_000
    caps =   [1.0,  5.0, 10.0, 25.0, 50.0, 100.0, 0.0]
    labels = ["1",  "5",  "10", "25", "50", "100", "inf"]
    mac_gamma = 0.85  # TDMA efficiency (guard time + acquisition overhead)

    results = {}
    for cap, label in zip(caps, labels):
        base = {
            **FULL_FIDELITY_BASE,
            "node_count": N,
            "coordinator_link_capacity_kbps": cap,
        }
        t0 = time.time()
        res = run_mc(base, N_MC)
        elapsed = time.time() - t0

        success = 100.0 - res["mean"]["coord_drop_pct"]
        raw_cap_needed = cap / mac_gamma if cap > 0 else 0
        results[label] = {
            "coord_drop_pct": res["mean"]["coord_drop_pct"],
            "coord_drop_std": res["std"]["coord_drop_pct"],
            "success_pct": success,
            "overhead": res["mean"]["overhead"],
            "mac_adjusted_kbps": round(raw_cap_needed, 1),
        }
        mac_note = f" (MAC-adj: {raw_cap_needed:.0f} kbps)" if cap > 0 else ""
        flush_print(f"  C_coord={label:>5} kbps: "
                    f"drops={res['mean']['coord_drop_pct']:.1f}% "
                    f"(SD={res['std']['coord_drop_pct']:.2f}%), "
                    f"success={success:.1f}%, "
                    f"overhead={res['mean']['overhead']:.2f}%{mac_note} [{elapsed:.1f}s]")

    flush_print(f"\n  MAC efficiency gamma={mac_gamma} (TDMA with guard bands)")
    flush_print(f"  MAC-adjusted minimum: 25/{mac_gamma:.2f} = {25/mac_gamma:.0f} kbps raw link")

    return results


def sweep_sampling_validation():
    """Table XII: Sampling validation — full-fidelity vs sampled at all N."""
    flush_print("\n" + "=" * 60)
    flush_print("SWEEP 5: Sampling Validation (Table XII)")
    flush_print("=" * 60)

    node_counts = [1_000, 2_000, 5_000, 10_000, 20_000, 50_000, 100_000]

    results = {}
    for N in node_counts:
        # Full fidelity
        full_cfg = {**FULL_FIDELITY_BASE, "node_count": N}
        t0 = time.time()
        full_res = run_mc(full_cfg, N_MC)
        full_elapsed = time.time() - t0

        # Sampled (auto: min(1, 1000/N))
        sampled_cfg = {
            "coordination_topology": "hierarchical",
            "cluster_size": 100,
            "simulation_days": 1,
            "node_count": N,
            "sync_sample_rate": 0.0,  # auto sampling
        }
        t0 = time.time()
        samp_res = run_mc(sampled_cfg, N_MC)
        samp_elapsed = time.time() - t0

        sample_rate = min(1.0, 1000 / N)
        discrepancy = abs(full_res["mean"]["overhead"] - samp_res["mean"]["overhead"])

        results[N] = {
            "full_overhead": full_res["mean"]["overhead"],
            "full_std": full_res["std"]["overhead"],
            "sampled_overhead": samp_res["mean"]["overhead"],
            "sampled_std": samp_res["std"]["overhead"],
            "discrepancy": discrepancy,
            "sample_rate": sample_rate,
        }
        flush_print(f"  N={N:>10,} (r_s={sample_rate:.3f}): "
                    f"full={full_res['mean']['overhead']:.3f}% "
                    f"(SD={full_res['std']['overhead']:.3f}%), "
                    f"sampled={samp_res['mean']['overhead']:.3f}% "
                    f"(SD={samp_res['std']['overhead']:.3f}%), "
                    f"Δ={discrepancy:.3f}% "
                    f"[full:{full_elapsed:.1f}s, samp:{samp_elapsed:.1f}s]")

    return results


def main():
    flush_print("Paper 02 — Table Parameter Sweep (Full Fidelity, 30 MC runs)")
    flush_print(f"Started at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    flush_print()

    t_start = time.time()

    scaling = sweep_scaling()
    exception = sweep_exception()
    link = sweep_link()
    coord_bw = sweep_coordinator_bw()
    validation = sweep_sampling_validation()

    total = time.time() - t_start
    flush_print(f"\n{'=' * 60}")
    flush_print(f"All sweeps complete in {total:.0f}s ({total/60:.1f} min)")

    all_results = {
        "scaling": {str(k): v for k, v in scaling.items()},
        "exception": exception,
        "link": link,
        "coordinator": coord_bw,
        "sampling_validation": {str(k): v for k, v in validation.items()},
    }

    out_path = "table_sweep_results.json"
    with open(out_path, "w") as f:
        json.dump(all_results, f, indent=2)
    flush_print(f"Results saved to {out_path}")


if __name__ == "__main__":
    main()
