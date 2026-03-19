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

I recommend a **tiered-authority, quarantine-first** governance model where slot reallocation is treated as a safety-critical function partitioned across the existing three-tier architecture with clear authority boundaries. The core principle: **no slot is ever reassigned—slots are retired and new slots are commissioned.** This semantic distinction eliminates an entire class of state-management bugs and makes the protocol formally verifiable on the seL4 kernel.

---

## 1. Failure Classification Taxonomy and Detection

The protocol begins with detection, and detection must be conservative. I propose four failure classes with distinct response timelines:

**Class A – Graceful Decommission**: Node self-reports imminent failure (battery degradation, reaction wheel desaturation approaching limits, thermal exceedance). The node broadcasts a structured retirement message including its current state vector, predicted drift trajectory, and remaining ΔV. Response: **immediate slot quarantine, orderly handoff.** Timeline: hours to days.

**Class B – Sudden Silent Failure**: Node stops responding. This is the most common case given automotive-grade components. Detection requires **three consecutive missed heartbeats at the cluster level** (I recommend 60-second heartbeat intervals, so confirmation at ~3 minutes) followed by **active interrogation** from two neighboring nodes using directed RF. If no response to active interrogation within 10 minutes, the cluster coordinator declares the node presumptively failed. Response: **slot quarantine with trajectory prediction.** Timeline: ~15 minutes to quarantine declaration.

**Class C – Partial Degradation**: Node responds but reports anomalous telemetry—attitude errors exceeding keep-out tube margins, propulsion faults, or communication degradation. The node remains in its slot but is flagged for **enhanced monitoring** (increased heartbeat rate to 10-second intervals from neighbors). Response: **conditional quarantine if trajectory prediction shows keep-out tube violation within 72 hours.** Timeline: hours.

**Class D – Byzantine Behavior**: Node transmits inconsistent or contradictory ephemeris data. This is the most dangerous class because it can corrupt the catalog. Detection requires **cross-validation by ≥3 neighboring nodes** comparing the suspect node's self-reported state vector against their own tracking observations. Response: **immediate catalog isolation—the node's ephemeris entries are flagged as untrusted and replaced with externally-observed trajectory predictions.** Timeline: minutes.

The critical design choice: **Class B and D failures trigger quarantine, never immediate reassignment.** The urgency is in protecting neighboring nodes, not in filling the vacant slot.

---

## 2. The Quarantine-First Protocol

When a slot enters quarantine, the following sequence executes:

**Step 1 – Trajectory Prediction (T+0 to T+1 hour)**: The cluster coordinator, using the failed node's last known state vector and a simplified force model (solar gravity + SRP, which dominates in heliocentric orbit), propagates the debris trajectory forward 30 days. This computation is lightweight—two-body with SRP perturbation is well within the capability of the rad-tolerant processors specified in the consensus.

**Step 2 – Keep-Out Tube Expansion (T+1 hour)**: Adjacent slots have their keep-out tubes temporarily expanded by a factor proportional to the trajectory prediction uncertainty. For a node at ~1 AU with no active station-keeping, positional uncertainty grows roughly linearly at the node's residual velocity error—typically meters per second. Over 30 days, this translates to ~100–2,500 km of positional uncertainty depending on the failure mode. The expanded keep-out tubes are broadcast to all cluster members.

**Step 3 – Neighbor Avoidance Assessment (T+1 to T+6 hours)**: Each node adjacent to the quarantined slot runs its own conjunction screening against the predicted debris trajectory. If any node's collision probability exceeds 10⁻⁷ (one order of magnitude below the annual threshold, applied per-event), it executes a **pre-authorized micro-avoidance maneuver** of ≤0.01 m/s. This is critical: the maneuver authority is pre-delegated and does not require coordinator approval. At 0.01 m/s, even 50 such events per year consume only 0.5 m/s—the floor of the annual ΔV budget.

**Step 4 – Quarantine Duration (30 days minimum)**: The slot remains quarantined until either (a) the debris is tracked to sufficient accuracy that its trajectory is confirmed to not intersect any active keep-out tube for the next year, or (b) the debris has drifted sufficiently far from the cluster that it is reclassified as a background conjunction object in the beacon catalog.

This quarantine-first approach is deliberately conservative. With 10–90 failures per year in Phase 1, and a 30-day quarantine, we have on average 1–7 slots in quarantine at any time out of 1,000–3,000. This is a negligible capacity loss (<0.3%) and does not justify the risk of premature reassignment.

---

## 3. Authority Hierarchy: Who Decides What

This is where I take a strong position against ambiguity:

**Tier 1 (Individual Nodes)**: Authority to execute pre-authorized collision avoidance maneuvers ≤0.01 m/s without any approval. Authority to self-report Class A retirement. Authority to vote in cluster consensus decisions. **No authority to modify the ephemeris catalog.**

**Tier 2 (Cluster Coordinators)**: Authority to declare quarantine for Class A, B, and C failures within their cluster. Authority to compute and broadcast expanded keep-out tubes. Authority to **request** slot commissioning from Tier 3. Authority to manage intra-cluster slot geometry optimization (small adjustments to orbital element windows that don't change the cluster's aggregate footprint). **Quarantine declarations are autonomous and require no Tier 3 approval.** This is essential for the 7–30 day autonomous operation requirement.

**Tier 3 (Beacon Spacecraft)**: **Sole authority to commission new slots and update the master ephemeris catalog.** This is the critical centralization point. Beacons maintain the authoritative catalog, resolve inter-cluster conflicts, and approve slot commissions that change the global swarm topology. Beacon approval can be asynchronous—a cluster coordinator submits a slot commission request, and the beacon approves it on the next catalog broadcast cycle (which I recommend at 6-hour intervals for routine updates, with emergency broadcasts for Class D events).

The rationale for centralizing slot commissioning at Tier 3: **the ephemeris catalog is the single most safety-critical data structure in the entire system.** Allowing 30+ cluster coordinators to independently modify it creates a distributed state consistency problem that is extraordinarily difficult to formally verify. By contrast, having 3–5 beacon spacecraft maintain the authoritative catalog—with cluster coordinators holding read-only cached copies plus local quarantine overlays—is a well-understood primary-backup architecture.

For beacon spacecraft consensus among themselves, I recommend **Raft over PBFT**. With only 3–5 beacons, Byzantine fault tolerance is overkill (it would require 3f+1 nodes to tolerate f Byzantine faults, meaning 4 beacons to tolerate 1 Byzantine failure). Raft's crash fault tolerance (requiring a majority quorum of 2/3 or 3/5) is sufficient because beacon spacecraft are high-reliability assets with authenticated communication links. If we genuinely suspect Byzantine behavior from a beacon, we have larger problems.

---

## 4. Slot Commissioning (Not Reassignment)

When a quarantined slot is ready for reuse, the process is:

1. **Cluster coordinator** identifies a replacement node (either a newly deployed spare or a node migrating from a less critical position) and computes a proposed orbital element window for the new slot. This window may differ from the original—orbital mechanics may have shifted the optimal position.

2. **Cluster coordinator** submits a **Slot Commission Request** to the beacon network, including: proposed orbital elements, keep-out tube dimensions, identity key of the replacement node, planned transfer trajectory, and ΔV cost.

3. **Beacon** validates the request against the master catalog—checking for conflicts with all other active and quarantined slots swarm-wide, not just within the requesting cluster. This global check is what cluster coordinators cannot do independently.

4. **Beacon** broadcasts the approved commission in the next catalog update. The replacement node begins its transfer maneuver.

The ΔV cost of slot migration is the binding constraint on commissioning rate. For nodes within the same cluster, typical slot-to-slot transfers require 0.005–0.05 m/s (depending on orbital element window spacing). This is affordable. Cross-cluster transfers are far more expensive (0.1–1.0 m/s) and should be avoided except during major reconfigurations.

---

## 5. Implementation on seL4

The quarantine state machine has exactly 5 states: **Active → Suspect → Quarantined → Available → Commissioned** (plus a terminal **Retired** state for permanently abandoned slots). This is small enough to be formally verified as a component within the seL4 microkernel's capability system. Each state transition has a single authorized initiator and a defined set of preconditions.

The beacon catalog update message should be a **signed, versioned, append-only log** rather than a mutable database. Each entry is a slot commission or retirement event with a monotonic sequence number. Nodes reconstruct current catalog state by replaying the log. This makes the 30-day autonomous operation requirement tractable: a node that has been out of contact simply requests log entries since its last known sequence number.

---

## 6. Key Quantitative Recommendations

| Parameter | Recommended Value | Rationale |
|---|---|---|
| Heartbeat interval | 60 s | Balances detection latency vs. communication overhead |
| Failure confirmation | 3 missed heartbeats + active interrogation (≤15 min) | Avoids false positives from transient comm loss |
| Minimum quarantine duration | 30 days | Matches autonomous operation window; allows trajectory characterization |
| Pre-authorized avoidance ΔV | ≤0.01 m/s per event | 50 events/year stays within budget floor |
| Beacon catalog broadcast | Every 6 hours (routine), immediate (emergency) | Balances bandwidth vs. staleness |
| Annual reassignment ΔV budget | ≤10% of total ΔV budget (0.05–0.5 m/s/year) | Preserves station-keeping margin |
| Maximum simultaneous quarantined slots per cluster | 5 (triggers cluster-level alert at 3) | Prevents cascading density loss |

---

## Conclusion

The quarantine-first, commission-not-reassign architecture is deliberately conservative. It prioritizes safety (collision avoidance) over efficiency (rapid slot reuse), which is the correct trade for a 50-year mission with no servicing capability. The 0.3% capacity loss from quarantined slots is negligible compared to the risk of a cascading conjunction event that could disable an entire cluster. The authority hierarchy is clean, formally verifiable, and compatible with extended autonomous operations.