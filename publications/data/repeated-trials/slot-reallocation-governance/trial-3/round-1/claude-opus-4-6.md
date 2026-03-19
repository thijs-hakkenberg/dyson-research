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

I recommend a **tiered-authority, quarantine-first** governance model where slot reallocation operates on three distinct timescales: immediate quarantine (seconds to minutes, cluster-autonomous), provisional reassignment (hours to days, cluster-coordinated with beacon confirmation), and permanent catalog amendment (days to weeks, beacon-authorized). This architecture respects the physical realities of orbital mechanics, the communication constraints of the federated hierarchy, and the ΔV poverty of individual nodes.

---

## 1. Failure Classification Taxonomy

The protocol must begin with unambiguous failure categorization, because the response to a node that gracefully deactivated its thruster system is fundamentally different from one that fragmented. I propose four classes:

**Class A – Graceful Shutdown**: Node broadcasts end-of-life or fault-detected message, executes passivation maneuver to drift to edge of its keep-out tube, and ceases active station-keeping. Detection is immediate via the broadcast. The node's trajectory is well-characterized because its final state vector is self-reported.

**Class B – Silent Failure**: Node stops responding to heartbeats but remains structurally intact (power system failure, processor lockup). Detection requires 3–5 missed heartbeat cycles. Trajectory is predictable via last-known state vector plus ballistic propagation, but uncertainty grows with time.

**Class C – Partial Degradation**: Node remains communicative but reports inability to maintain station (thruster failure, attitude control loss, partial power loss). This is the most complex class because the node may drift unpredictably while still occupying communication bandwidth. Detection is immediate but characterization is ongoing.

**Class D – Catastrophic/Fragmentation**: Node ceases communication and may have generated debris. Detection via missed heartbeats plus anomalous radar/lidar returns from neighboring nodes. This is the highest-urgency class because it potentially threatens multiple adjacent slots simultaneously.

**Confirmation thresholds**: For Classes B and D, I recommend a **5-heartbeat confirmation window** before declaring failure. If the heartbeat interval is 10 seconds (reasonable for intra-cluster coordination), this gives a 50-second confirmation latency—fast enough to begin quarantine before meaningful orbital drift occurs, slow enough to avoid false positives from transient communication shadowing. The cluster coordinator should poll the suspect node on at least two independent communication paths before confirming.

---

## 2. The Quarantine-First Principle

This is the core architectural decision I want to argue for strongly: **never reassign a slot until the failed node's trajectory is characterized to within one keep-out tube diameter over a 30-day propagation horizon.**

The reasoning is straightforward. A failed node in heliocentric orbit doesn't stop existing—it becomes an uncontrolled object. If you reassign its slot to a replacement node before you know where the dead node is going, you may be sending the replacement into a conjunction. The failed node's differential drift rate relative to its assigned slot depends on its last station-keeping state, solar radiation pressure (which varies with attitude, now uncontrolled), and any residual ΔV from the failure event itself.

**Quarantine protocol**:

1. Upon failure confirmation, the cluster coordinator broadcasts a **slot quarantine message** to all nodes within 3 slot radii of the failed node. This is a Tier 2 autonomous action requiring no beacon approval.

2. Adjacent nodes increase their conjunction screening cadence for the quarantined region from nominal (every orbital period) to **high-rate (every 10 minutes of propagated time)**.

3. The cluster coordinator tasks 2–3 nodes with the best sensor geometry to perform **tracking observations** of the failed node, building an independent orbit determination solution.

4. Quarantine persists until either: (a) the failed node's 30-day predicted trajectory clears all active keep-out tubes with 3σ confidence, or (b) the failed node is confirmed to have exited the cluster's operational volume entirely.

For Class A failures, quarantine may last only hours because the final state vector is well-known. For Class D, quarantine could persist for weeks—and that's acceptable. The energy collection loss from one orphaned slot is negligible compared to the risk of a cascading conjunction event.

---

## 3. Authority Hierarchy: Who Decides What

I recommend the following clean separation of authority:

**Tier 2 (Cluster Coordinator) – Autonomous Authority Over:**
- Declaring and lifting slot quarantines
- Commanding emergency avoidance maneuvers for nodes adjacent to failed nodes
- Provisional slot reassignment within the cluster (moving an existing cluster member to a vacated slot)
- Temporary keep-out tube expansion around quarantined zones

**Tier 3 (Beacon Spacecraft) – Required Approval For:**
- Permanent catalog amendments (removing a slot, adding a replacement node)
- Cross-cluster slot reassignment (moving a node from one cluster to another)
- Cluster boundary adjustments triggered by multiple failures
- Authorizing replacement node deployment into a vacated slot

The rationale: cluster coordinators have the lowest-latency awareness of local geometry and can act within seconds. But they lack global context. A beacon spacecraft maintains the authoritative ephemeris catalog and can detect situations where multiple clusters are simultaneously experiencing failures that might interact. The beacon's approval latency (seconds to minutes for intra-swarm communication) is acceptable for permanent reassignment because quarantine has already secured the safety envelope.

**Critical design point**: The cluster coordinator role must rotate on a deterministic schedule (I suggest weekly, synchronized to the swarm time reference) with at least 2 designated successors. If the coordinator itself fails, the first successor assumes authority after 10 missed coordinator heartbeats. This must be implemented as a **deterministic state machine, not a consensus election**, to avoid Byzantine failure modes during the exact moment when coordinator authority is most needed.

I'm deliberately avoiding PBFT or Raft for the time-critical quarantine decision. These protocols are appropriate for non-urgent configuration changes, but quarantine declaration is a **unilateral coordinator action** that neighboring nodes must obey immediately and can appeal later. The coordinator has authority; if it's wrong, the cost is a temporarily quarantined slot. If it's slow because it's waiting for quorum, the cost could be a collision.

---

## 4. ΔV Budget for Slot Migration

This is the binding constraint that makes aggressive reassignment impractical. Let me work the numbers.

For a node in heliocentric orbit at ~1 AU, the differential velocity between adjacent slots depends on the orbital element window size. With the specified ±1 m to ≤5 km positional accuracy range, let's take a representative keep-out tube radius of 500 m and inter-slot spacing of 2 km.

Moving one slot position (2 km lateral translation over a reasonable transfer time of ~1 orbital period, roughly 1 year for heliocentric) requires a ΔV on the order of **0.01–0.1 m/s** depending on the phasing geometry. This seems cheap against the 0.5–5 m/s/year budget, but consider:

- Station-keeping itself consumes the majority of the ΔV budget (solar radiation pressure compensation, orbital element window maintenance)
- At 1–3% annual failure rate with 100 nodes per cluster, a cluster experiences 1–3 failures per year
- If each failure triggers migration of 2–4 adjacent nodes (to fill the gap and rebalance spacing), that's 2–12 migration maneuvers per cluster per year
- Cumulative migration ΔV: 0.02–1.2 m/s/year per migrating node

**My recommendation**: Reserve **no more than 20% of annual ΔV budget** for slot migration. At the low end (0.5 m/s/year total budget), this means 0.1 m/s/year for migration—enough for 1–2 single-slot moves. At the high end (5 m/s/year), this allows 1 m/s/year—sufficient for even aggressive rebalancing.

This constraint means that **most vacated slots should be filled by newly deployed replacement nodes rather than by migrating existing nodes.** Slot migration should be reserved for safety-critical rebalancing (closing gaps that create conjunction geometry problems) rather than optimizing energy collection.

---

## 5. Beacon Catalog Update Mechanism

The ephemeris catalog amendment must be treated as a **signed, versioned, append-only ledger**. Each entry contains:

- Slot ID, assigned node ID, orbital element window (6 elements + tolerances)
- Keep-out tube parameters
- Status: ACTIVE / QUARANTINED / VACANT / RESERVED
- Amendment authority (coordinator ID + beacon confirmation hash)
- Epoch timestamp (swarm time reference)

Beacon spacecraft broadcast catalog deltas (not full catalogs) at a cadence of **once per hour** during nominal operations, increasing to **once per minute** when any slot within their coverage is in QUARANTINED status. Each delta is signed with the beacon's identity key and includes a Merkle root of the full catalog state for integrity verification.

For the 30-day autonomous operation requirement: each node must carry a full catalog snapshot plus the ability to apply deltas. Catalog size for 3,000 nodes at ~200 bytes per entry is ~600 KB—trivially storable. Delta messages for single-slot amendments are <1 KB.

---

## 6. Key Risk: Correlated Failures

The elephant in the room is correlated failure. A solar particle event, a software bug in a common firmware version, or a manufacturing defect batch could take out dozens of nodes simultaneously. The quarantine-first approach scales poorly here because quarantining 10% of a cluster's slots simultaneously may fragment the cluster's communication topology.

**Mitigation**: Beacon spacecraft must monitor cluster-level failure rates and trigger a **cluster-wide safe mode** if failures exceed 5% within any 24-hour window. Safe mode expands all keep-out tubes by 2x, halves the conjunction screening interval, and suspends all non-essential operations until beacon spacecraft can perform global trajectory assessment.

This is the scenario that most strongly justifies the beacon tier's existence—it's the adult supervision that prevents cluster-level autonomous responses from conflicting with each other during a swarm-wide crisis.

---

## Summary of Recommendations

| Decision | Recommendation |
|----------|---------------|
| Primary philosophy | Quarantine-first; never reassign before trajectory characterization |
| Quarantine authority | Cluster coordinator, unilateral, no consensus required |
| Permanent reassignment authority | Beacon-confirmed |
| Failure confirmation | 5 missed heartbeats (~50 seconds) |
| ΔV reservation for migration | ≤20% of annual budget |
| Catalog update format | Signed, versioned deltas with Merkle integrity |
| Correlated failure threshold | >5% cluster loss in 24 hours triggers safe mode |
| Consensus protocol for non-urgent changes | Raft (simpler than PBFT, sufficient given authenticated channels) |