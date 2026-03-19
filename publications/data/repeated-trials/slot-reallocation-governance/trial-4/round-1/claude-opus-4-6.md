---
questionId: "rq-1-40"
questionSlug: "slot-reallocation-governance"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
roundNumber: 1
generated: "2026-02-24"
type: "discussion-response"
---

# Slot Reallocation Governance Protocol: A Concrete Architecture

## Executive Summary

I recommend a **tiered-authority model with deterministic fallback rules** that eliminates the need for distributed consensus algorithms for time-critical reassignments. The core insight: slot reallocation is not a consensus problem—it's a state machine problem. Every node should be able to independently compute the correct reallocation outcome given the same failure inputs, making Byzantine fault tolerance largely unnecessary for this specific function.

---

## Failure Classification Taxonomy

The protocol begins with four failure classes, each with distinct detection signatures and response timelines:

**Class A – Graceful Shutdown**: Node self-reports imminent failure (battery degradation, reaction wheel desaturation approaching limits, thermal exceedance). The node broadcasts a structured decommission message including its final state vector with uncertainty bounds. Response: **immediate slot release and catalog update**. This is the easy case—the node cooperates in its own removal. Expected frequency: ~60% of failures based on automotive-grade component degradation curves.

**Class B – Sudden Silent Failure**: Node stops transmitting with no warning. Detection requires missed heartbeats. I recommend a **3-heartbeat confirmation threshold** with heartbeat intervals of 60 seconds, giving 3-minute detection latency. This balances false-positive risk against drift accumulation. At typical heliocentric relative velocities, 3 minutes of uncontrolled drift is negligible relative to keep-out tube dimensions. Response: **slot quarantine, then reassignment**.

**Class C – Erratic Behavior**: Node transmits but with inconsistent state vectors, conflicting commands, or violated keep-out boundaries. This is the most dangerous class—a misbehaving node that still occupies RF and physical space. Detection via cross-validation: neighboring nodes compare the suspect's self-reported ephemeris against their own tracking observations. **Two independent neighbor disagreements** trigger classification. Response: **immediate quarantine of the node's slot plus adjacent buffer slots**.

**Class D – Communication Loss (Ambiguous)**: Node stops communicating but may be experiencing transient RF interference, antenna pointing error, or solar event disruption. Distinguished from Class B by context—if multiple nodes in a region lose contact simultaneously, classify as Class D. Response: **extended confirmation window (30 minutes) before quarantine**. This directly addresses the false-positive concern.

---

## The State Machine Approach (Not Consensus)

Here's where I diverge from the research direction suggesting PBFT or Raft. Those algorithms solve the problem of *disagreement among honest participants about ordering of events*. Slot reallocation doesn't have that problem if we design it correctly.

**Deterministic Slot State Transitions**: Every slot exists in one of five states: `ACTIVE`, `SUSPECT`, `QUARANTINED`, `AVAILABLE`, `MIGRATING`. Transitions are triggered by signed failure reports that include timestamps synchronized to the ≤10 ms swarm-wide clock. Given identical inputs, every node in the cluster computes identical state transitions. No voting required.

The state machine rules:

- `ACTIVE` → `SUSPECT`: First missed heartbeat or first neighbor disagreement report
- `SUSPECT` → `ACTIVE`: Heartbeat resumes within confirmation window
- `SUSPECT` → `QUARANTINED`: Confirmation threshold reached (3 heartbeats for Class B, 2 neighbor reports for Class C)
- `QUARANTINED` → `AVAILABLE`: Failed node trajectory fully characterized AND keep-out tube clearance confirmed (typically 24–72 hours)
- `AVAILABLE` → `MIGRATING`: Replacement node claims slot per priority rules
- `MIGRATING` → `ACTIVE`: Replacement node achieves station-keeping within orbital element window

**Why this works without consensus**: The inputs are signed, timestamped heartbeat messages (or their absence) and signed neighbor observation reports. As long as >50% of cluster members receive the same messages—which the beacon broadcast mechanism ensures via periodic catalog reconciliation—they converge on identical state. Temporary disagreements are harmless because the quarantine buffer absorbs timing differences.

---

## Authority Hierarchy: Cluster-Autonomous with Beacon Ratification

**Tier 2 (Cluster Coordinators)** have full authority for intra-cluster slot state transitions. They don't need beacon approval for quarantine or reassignment. The latency argument is decisive: beacon spacecraft may be light-seconds away, and Class C failures require sub-minute response.

**Tier 3 (Beacon Spacecraft)** serve three functions in this protocol:

1. **Ratification and conflict resolution**: Beacons maintain the authoritative catalog. If two cluster coordinators disagree on a slot state (possible at cluster boundaries), the beacon resolves based on timestamp priority.

2. **Cross-cluster reassignment authorization**: When a replacement node must migrate from one cluster to another, beacon approval is required because this affects two clusters' density maps simultaneously.

3. **Catalog reconciliation broadcast**: Every beacon broadcast cycle (I recommend 15-minute intervals) includes a hash of the current slot state table. Nodes compare against their local state and request corrections for any discrepancies. This is the consistency mechanism that replaces formal consensus.

**Rotating coordinator failure**: If the cluster coordinator itself fails, the protocol must handle this gracefully. I recommend **pre-computed coordinator succession lists** embedded in each broadcast cycle. The next three successors are always known. If the coordinator misses two broadcast cycles, the first successor assumes authority and broadcasts assumption-of-command. This is simpler and more deterministic than a leader election algorithm.

---

## Quarantine Geometry and Adjacency Modeling

The quarantine zone around a failed node must account for worst-case drift. For a node that fails with residual angular momentum (tumbling), the trajectory uncertainty grows roughly linearly with time until ground or beacon tracking characterizes the orbit.

**Quarantine zone sizing**: I propose a dynamic quarantine radius:

- T+0 to T+1 hour: Navigation uncertainty at last known state (±1 m to ±100 m depending on tracking quality)
- T+1 hour to T+24 hours: Propagated uncertainty including unmodeled ΔV from residual thruster pressure, solar radiation pressure on tumbling geometry. Conservative estimate: ±500 m cross-track growth per day.
- T+24 hours to T+72 hours: Beacon tracking narrows uncertainty. Quarantine zone shrinks as orbit determination improves.

**Adjacency graph implications**: With ~100 nodes per cluster and keep-out tubes on the order of 1–5 km, a single quarantine event typically affects 2–6 adjacent slots. The slot adjacency graph should be precomputed and updated each broadcast cycle. **Critical slots**—those whose quarantine would cascade to affect >10 neighbors—should be identified and assigned to higher-reliability nodes or given larger keep-out margins. This is a straightforward graph centrality analysis.

Monte Carlo simulation priority: I strongly recommend simulating **correlated failures** (solar particle events damaging multiple nodes in a region) rather than just independent failures. A coronal mass event could take out 5–15 nodes in a geometric cone, creating a large contiguous quarantine zone. The protocol must handle this without requiring the entire cluster to evacuate.

---

## ΔV Budget for Slot Migration

This is the binding constraint on reassignment frequency. Key calculations:

**Intra-cluster migration** (moving to an adjacent slot within the same orbital element window family): Typical ΔV cost of 0.01–0.1 m/s for a phasing maneuver over 1–2 orbital periods. At the low end of the propulsion budget (0.5 m/s/year), a node could perform ~5–50 such migrations over its lifetime. This is acceptable.

**Cross-cluster migration**: Potentially 0.5–2.0 m/s depending on orbital plane differences. This consumes a significant fraction of annual budget and should be rare—reserved for cases where a cluster has lost >10% of nodes and cannot maintain minimum density from internal reserves.

**Recommendation**: Maintain a **5% ΔV reserve** specifically for slot migration across the mission lifetime. For a 50-year mission with 2 m/s/year budget, that's 5 m/s total reserved for reallocation maneuvers—sufficient for ~50–500 intra-cluster migrations or 2–10 cross-cluster migrations. This should be tracked as a consumable resource in each node's health telemetry.

**Spare node strategy**: Rather than migrating operational nodes, deploy 3–5% spare nodes per cluster in parking orbits at cluster periphery. These spares consume minimal station-keeping ΔV and can migrate inward when slots become available. This is far more ΔV-efficient than reshuffling the operational constellation.

---

## Beacon Catalog Update Data Structure

The ephemeris catalog amendment should be minimal and authenticated:

```
SlotUpdate {
    slot_id:        uint32          // unique slot identifier
    new_state:      enum[5]         // ACTIVE/SUSPECT/QUARANTINED/AVAILABLE/MIGRATING
    timestamp:      uint64          // synchronized swarm time, ms precision
    authority:      node_id         // cluster coordinator or beacon ID
    signature:      ed25519_sig     // 64 bytes, per-node identity key
    trajectory:     optional<6DOF>  // only for QUARANTINED state, failed node orbit
    assignee:       optional<node_id> // only for MIGRATING state
}
```

Total size: ~150 bytes per update. At 90 failures/year for Phase 1, this is negligible bandwidth. The 15-minute beacon broadcast can include all pending updates plus the full catalog hash for reconciliation.

**Authentication**: Ed25519 signatures verified against the pre-deployed key registry in each node's seL4 secure enclave. Cluster coordinators hold signing authority for their cluster's slots. Beacons hold override authority for all slots. Key revocation for compromised nodes is handled via beacon broadcast—another reason beacons must be hardened Tier 3 assets.

---

## Key Recommendation

Build the prototype around the deterministic state machine, not a consensus algorithm. Validate with the 10,000-node simulation environment using correlated failure scenarios. The state machine approach is simpler to formally verify on seL4, requires less inter-node communication, and degrades gracefully when communication is intermittent—exactly the properties needed for 30-day autonomous operation.