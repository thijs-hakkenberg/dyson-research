---
questionId: "rq-1-40"
questionSlug: "slot-reallocation-governance"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
roundNumber: 2
generated: "2026-02-24"
type: "discussion-response"
---

# Slot Reallocation Governance Protocol: Engineering the Safety-Capacity Boundary

## Executive Summary

Building on the strong convergence from Round 1—all three respondents independently arrived at quarantine-first, tiered-authority architectures—I want to push the discussion toward the **unresolved engineering decisions** that will determine whether this protocol actually works at scale. Specifically, I argue for three positions that sharpen or challenge the emerging consensus:

1. **Quarantine geometry must be asymmetric and drift-aware**, not simple spherical exclusion zones.
2. **Cluster coordinators need binding safety authority but must not have reassignment authority**—the separation of safety and optimization that GPT-5.2 identified is correct, but the implementation boundary should be drawn differently than proposed.
3. **The ΔV cost of slot reallocation is the binding constraint** that makes most "replacement node fills vacated slot" scenarios operationally infeasible in Phase 1, forcing a fundamentally different capacity recovery strategy.

---

## 1. Quarantine Zone Geometry: The Drift Cone Problem

Round 1 discussions treated quarantine zones as relatively static constructs. This underestimates the problem. A failed node in heliocentric orbit doesn't drift isotropically—it follows a predictable trajectory governed by its last known state vector, residual angular momentum, and solar radiation pressure. The quarantine zone is not a sphere; it is a **drift cone** that elongates along the orbital velocity vector and broadens with time uncertainty.

**Concrete proposal**: Each node's onboard formally verified kernel (seL4) should maintain a pre-computed **drift reachability set** for every neighbor within its keep-out tube adjacency graph. This is a 6D phase-space envelope, but for practical implementation it can be conservatively approximated as a truncated cone with:

- **Apex** at the node's last confirmed position
- **Half-angle** determined by attitude uncertainty at time of failure (worst case: tumbling, so full 4π sr for thrust-capable nodes; constrained to solar pressure perturbation envelope for passivated nodes)
- **Length** growing at the differential velocity uncertainty rate, typically 0.1–10 mm/s for nodes within a cluster's orbital element window

For a Class B failure (sudden, non-cooperative) with no final state broadcast, the drift cone half-angle is large initially but **collapses** as neighboring nodes track the debris optically or via inter-satellite ranging. This creates a natural quarantine zone that shrinks over time—a critical feature, because permanent large exclusion zones in a dense swarm are operationally catastrophic.

**Detection timeline**: I recommend a **3-heartbeat confirmation threshold** before declaring failure. With heartbeat intervals of 10–60 seconds (tunable per cluster density), this gives 30–180 seconds to failure declaration. This is conservative enough to avoid false positives from transient communication blockage while fast enough to begin drift cone propagation before the failed node moves appreciably.

**Key specification**: The beacon catalog broadcast format must include not just current ephemeris but a **quarantine zone descriptor**—a compact parameterization (perhaps 12–16 bytes: cone apex epoch, half-angle, drift rate, confidence level) appended to the failed node's last catalog entry. This is far more useful than a binary "slot occupied/vacant" flag.

---

## 2. Authority Hierarchy: Safety is Local, Optimization is Global

I agree with the Round 1 consensus that cluster coordinators (Tier 2) must have autonomous safety authority. But I want to be precise about what this means and where the boundary falls.

**Safety authority (Cluster Coordinator, autonomous, latency < 5 minutes):**
- Declare node failure after confirmation threshold
- Compute and broadcast quarantine zone descriptor to all cluster members
- Command neighboring nodes to execute collision avoidance maneuvers if drift cone intersects their keep-out tubes
- Temporarily suspend slot assignments within quarantine zone
- Escalate to beacon tier via next available communication window

**What cluster coordinators must NOT do:**
- Reassign slots to replacement nodes
- Modify the master ephemeris catalog's slot allocation table
- Authorize cross-cluster node migration

**Why this boundary?** Slot reassignment has **global externalities**. Moving Node X into Slot Y changes the conjunction geometry not just for Cluster A but potentially for adjacent Clusters B and C whose orbital element windows overlap at the boundaries. The cluster coordinator lacks visibility into these cross-boundary effects. Only the beacon tier, which maintains the full swarm ephemeris catalog, can safely authorize reassignment.

**Consensus mechanism for cluster-level safety decisions**: I recommend against full Byzantine fault tolerance (PBFT) for safety-critical actions. PBFT requires 3f+1 nodes to tolerate f Byzantine failures—in a 100-node cluster, tolerating even 3 Byzantine nodes requires 10 participants in the consensus, with multiple round-trip message exchanges. This is unnecessarily complex for safety decisions that are **deterministic given shared state**: if all nodes agree on the failed node's last state vector, the quarantine zone computation is a mathematical function, not a negotiation.

Instead, I propose a **deterministic safety protocol**: the cluster coordinator computes the quarantine zone and broadcasts it. Any node that independently computes a materially different zone (disagreement threshold: >10% volume difference) raises a conflict flag, triggering fallback to the secondary coordinator. This is simpler, faster, and more amenable to formal verification on seL4 than a full consensus protocol. Reserve Raft-style consensus for coordinator **election**, not for operational safety decisions.

---

## 3. The ΔV Budget Reality: Reallocation is Expensive

This is where I diverge most sharply from the implicit assumptions in Round 1. Let me run the numbers.

**Slot migration cost**: Within a cluster, orbital element windows are on the order of ±1–5 km in position. Moving a node from its current slot to an adjacent vacated slot requires a Hohmann-like transfer within the cluster's orbital element space. For a 5 km position change in heliocentric orbit, the ΔV is small in absolute terms—perhaps 0.01–0.1 m/s depending on the transfer time allowed. This seems affordable against a 0.5–5 m/s/year budget.

**But the real cost is cumulative**: With 1–3% annual failure rate across 1,000–3,000 nodes, we get 10–90 failures per year. If each failure triggers slot migration for 1–3 neighboring nodes (to fill the gap and rebalance local density), that's 10–270 migration maneuvers per year distributed across the swarm. For nodes near failure-prone regions (thermal extremes, higher radiation zones), the local migration burden could be 3–5× the average, consuming 0.3–0.5 m/s/year—a significant fraction of the total budget, especially for nodes at the low end of the ΔV range.

**My recommendation: Absorb rather than replace.** For Phase 1, the swarm should be designed with **5–10% slot overcapacity**—more allocated slots than active nodes. When a node fails, its slot is quarantined, then retired. Replacement nodes launched in subsequent batches are assigned to **new slots** in the overcapacity pool rather than migrating existing nodes into vacated positions. This costs zero ΔV for slot migration and requires only that the swarm's energy collection efficiency degrades gracefully with modest density reduction.

The exception is **critical topology slots**—positions that serve as communication relay points or whose vacancy creates unacceptable gaps in the power beaming geometry. These should be pre-identified in the slot adjacency graph (Research Direction #2 from the background) and assigned higher-capability nodes with larger ΔV budgets.

---

## 4. Beacon Catalog Update Protocol

The beacon spacecraft must propagate catalog amendments reliably across the entire swarm within one broadcast cycle. I propose:

- **Broadcast cadence**: Every 15 minutes (aligned with the existing time synchronization architecture)
- **Amendment format**: Delta updates, not full catalog retransmission. Each amendment is a signed (per-node Ed25519 key) tuple: `{node_id, epoch, new_status, quarantine_descriptor, authorizing_coordinator, beacon_signature}`
- **Size**: ~128 bytes per amendment. At 90 failures/year, the annual amendment volume is trivial (~11 KB). Even batched with routine ephemeris updates, this fits comfortably in the beacon broadcast budget.
- **Consistency guarantee**: Each amendment carries a monotonically increasing sequence number. Nodes that detect a gap in sequence numbers request retransmission from their cluster coordinator, not from the beacon directly (reducing beacon load).
- **30-day autonomy**: Cluster coordinators cache all amendments and can reconstruct the full catalog state for any node that has been out of contact. The catalog is append-only during autonomous periods; conflict resolution (if two clusters independently reassign overlapping slots) is deferred to beacon adjudication upon reconnection.

---

## 5. Critical Open Question: Coordinator Failure During Reallocation

The most dangerous scenario is not a single node failure—it is a **cluster coordinator failure during an active quarantine event**. The secondary coordinator must seamlessly assume authority, but it may have incomplete state if the primary failed mid-broadcast. I recommend that quarantine zone declarations be **idempotent and self-describing**: any node receiving the declaration can independently verify its validity from the failed node's last catalog entry. This eliminates the need for coordinator state transfer during failover.

---

## Summary of Recommendations

| Decision | Recommendation |
|---|---|
| Quarantine geometry | Asymmetric drift cones, shrinking over time as tracking improves |
| Safety authority | Cluster coordinators, deterministic protocol, no BFT needed |
| Reassignment authority | Beacon tier only, with cross-cluster visibility |
| Slot filling strategy | Absorb losses into overcapacity pool; minimize migration ΔV |
| Catalog updates | Delta amendments, 128 bytes each, 15-min broadcast cycle |
| Coordinator failover | Idempotent quarantine declarations, no state transfer required |

The governing principle throughout: **the swarm must be safe before it is efficient.** Capacity recovery is a logistics problem solvable over weeks and months. Collision avoidance is a physics problem measured in minutes and hours. The governance protocol must never sacrifice the latter for the former.