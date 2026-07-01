#!/usr/bin/env python3
"""Run DES: GE retransmissions + coordinator bandwidth limit interaction."""

import sys
sys.path.insert(0, "/Users/hakketh/projects/experiments/dyson/publications/scripts")

from swarm_model import SwarmCoordinationConfig, SwarmCoordinationSimulator

N = 10_000
K_C = 100
SIM_DAYS = 5
MAX_EVENTS = N * 50

def run_config(label, **kwargs):
    cfg = SwarmCoordinationConfig(
        node_count=N,
        cluster_size=K_C,
        coordination_topology="hierarchical",
        simulation_days=SIM_DAYS,
        max_events=MAX_EVENTS,
        max_retransmissions=2,
        **kwargs
    )
    sim = SwarmCoordinationSimulator(cfg)
    r = sim.run()
    dr = r.total_messages_delivered / max(1, r.total_messages_sent) * 100
    print(f"\n{label}:")
    print(f"  overhead={r.communication_overhead_percent:.2f}%  loss={r.message_loss_rate*100:.1f}%")
    print(f"  aoi_mean={r.aoi_mean_seconds:.1f}s  aoi_p99={r.aoi_p99_seconds:.1f}s")
    print(f"  coord_drops={r.coordinator_drops}  retransmissions={r.retransmission_count}")
    print(f"  total_sent={r.total_messages_sent}  delivered={r.total_messages_delivered}  delivery={dr:.1f}%")
    print(f"  bytes_sent={r.total_bytes_sent}  bytes_attempted={r.total_bytes_attempted}")
    return r

# Sweep coordinator bandwidth with and without GE losses
capacities = [15, 20, 25, 30, 50, 100]

print("="*70)
print("EXPERIMENT: Coordinator bandwidth × GE loss interaction")
print("="*70)

print("\n--- No loss (baseline) ---")
for cap in capacities:
    run_config(f"  Cap={cap}kbps, no loss",
        coordinator_link_capacity_kbps=cap)

print("\n--- GE losses (80% avail) ---")
for cap in capacities:
    run_config(f"  Cap={cap}kbps, GE loss",
        coordinator_link_capacity_kbps=cap,
        link_availability=0.80,
        ge_p_loss_good=0.01,
        ge_p_loss_bad=0.90,
        ge_p_good_to_bad=0.05,
        ge_p_bad_to_good=0.50)

print("\n--- GE losses + exception (p_exc=0.10) ---")
for cap in capacities:
    run_config(f"  Cap={cap}kbps, GE+exc",
        coordinator_link_capacity_kbps=cap,
        link_availability=0.80,
        ge_p_loss_good=0.01,
        ge_p_loss_bad=0.90,
        ge_p_good_to_bad=0.05,
        ge_p_bad_to_good=0.50,
        enable_exception_telemetry=True,
        exception_threshold=0.10)
