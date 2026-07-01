#!/usr/bin/env python3
"""Run DES with joint GE losses + exception telemetry to check for interaction effects."""

import sys
sys.path.insert(0, "/Users/hakketh/projects/experiments/dyson/publications/scripts")

from swarm_model import SwarmCoordinationConfig, SwarmCoordinationSimulator

N = 10_000
K_C = 100
SIM_DAYS = 1
MAX_EVENTS = N * 3

def run_config(label, **kwargs):
    cfg = SwarmCoordinationConfig(
        node_count=N,
        cluster_size=K_C,
        coordination_topology="hierarchical",
        simulation_days=SIM_DAYS,
        max_events=MAX_EVENTS,
        **kwargs
    )
    sim = SwarmCoordinationSimulator(cfg)
    r = sim.run()
    print(f"\n{label}:")
    print(f"  overhead_pct={r.communication_overhead_percent:.2f}%")
    print(f"  aoi_mean={r.aoi_mean_seconds:.1f}s  aoi_p99={r.aoi_p99_seconds:.1f}s")
    delivery = r.total_messages_delivered / max(1, r.total_messages_sent)
    print(f"  msg_delivery={delivery*100:.1f}%")
    print(f"  coord_drops={r.coordinator_drops}")
    print(f"  aoi_mean_pos_error={r.aoi_mean_position_error_m:.1f}m  aoi_p99_pos_error={r.aoi_p99_position_error_m:.1f}m")
    return r

# Baseline: no loss, no exception
r_base = run_config("Baseline (no loss, full reporting)")

# Exception only (p_exc=0.10)
r_exc = run_config("Exception only (p_exc=0.10)",
    enable_exception_telemetry=True,
    exception_threshold=0.10)

# GE loss only (80% availability)
r_ge = run_config("GE loss only",
    link_availability=0.80,
    ge_p_loss_good=0.01,
    ge_p_loss_bad=0.90,
    ge_p_good_to_bad=0.05,
    ge_p_bad_to_good=0.50)

# Joint: GE + exception
r_joint = run_config("Joint GE + exception",
    enable_exception_telemetry=True,
    exception_threshold=0.10,
    link_availability=0.80,
    ge_p_loss_good=0.01,
    ge_p_loss_bad=0.90,
    ge_p_good_to_bad=0.05,
    ge_p_bad_to_good=0.50)

print("\n" + "="*60)
print("INTERACTION ANALYSIS")
print("="*60)

# If effects are independent, joint AoI ≈ max(exc_AoI, ge_AoI)
# Or: joint delivery = exc_delivery × ge_delivery / base_delivery
def dr(r):
    return r.total_messages_delivered / max(1, r.total_messages_sent)
exc_delivery = dr(r_exc)
ge_delivery = dr(r_ge)
joint_delivery = dr(r_joint)
predicted_joint = exc_delivery * ge_delivery  # independent product

print(f"\nDelivery rates:")
print(f"  Exception only: {exc_delivery*100:.1f}%")
print(f"  GE loss only:   {ge_delivery*100:.1f}%")
print(f"  Joint actual:   {joint_delivery*100:.1f}%")
print(f"  Independent prediction: {predicted_joint*100:.1f}%")
print(f"  Interaction gap: {(joint_delivery - predicted_joint)*100:.1f} pp")

print(f"\nAoI P99:")
print(f"  Exception only: {r_exc.aoi_p99_seconds:.0f}s")
print(f"  GE loss only:   {r_ge.aoi_p99_seconds:.0f}s")
print(f"  Joint actual:   {r_joint.aoi_p99_seconds:.0f}s")
aoi_p99_additive = r_exc.aoi_p99_seconds + r_ge.aoi_p99_seconds - r_base.aoi_p99_seconds
print(f"  Additive prediction: {aoi_p99_additive:.0f}s")
print(f"  Interaction: joint - max(exc, ge) = {r_joint.aoi_p99_seconds - max(r_exc.aoi_p99_seconds, r_ge.aoi_p99_seconds):.0f}s")

print(f"\nPosition error P99:")
print(f"  Exception only: {r_exc.aoi_p99_position_error_m:.0f}m")
print(f"  GE loss only:   {r_ge.aoi_p99_position_error_m:.0f}m")
print(f"  Joint actual:   {r_joint.aoi_p99_position_error_m:.0f}m")
