---
questionId: "rq-1-40"
questionSlug: "slot-reallocation-governance"
type: "discussion-conclusion"
generatedBy: "claude-opus-4-6"
generated: "2026-02-24"
roundCount: 1
terminationReason: "unanimous-conclude"
---

# Conclusion: Slot Reallocation Governance Protocol

## Summary

The discussion converged on a **tiered-authority model with deterministic fallback rules**, rejecting distributed consensus algorithms (PBFT, Raft) in favor of **Deterministic Slot State Machines (DSSM)** for time-critical slot reassignment decisions. The core architectural insight is that slot reallocation, when properly formulated, is a state machine problem rather than a consensus problem: given identical ephemeris data and failure detection inputs, every node in the swarm should independently arrive at the same slot state classification without requiring voting or quorum. This approach aligns naturally with the seL4 formally verified kernel (the state machine is small enough to be tractable for formal verification), degrades gracefully during the 7–30+ day autonomous operation windows, and eliminates the fragility of BFT algorithms under exactly the conditions—multiple simultaneous failures—when they would be most needed.

The protocol introduces a four-class failure taxonomy (Graceful Shutdown, Sudden Silent Failure, Partial Degradation, Communication Loss Only) with a critical distinction between Class B (truly dead, ballistically predictable) and Class D (deaf but potentially maneuvering, unpredictable within its control envelope). Slot states progress through a deterministic lifecycle—ACTIVE → SUSPECT → QUARANTINED → VACANT → RESERVED → ACTIVE—with each tier of the three-tier architecture assigned clear, non-overlapping authority: individual nodes autonomously widen keep-out margins for self-preservation, cluster coordinators manage intra-cluster reassignment and VACANT transitions, and beacon spacecraft ratify catalog updates, resolve cross-cluster boundary conflicts, and serve as authoritative tiebreakers. This achieves autonomy with eventual consistency rather than requiring synchronous agreement.

At Phase 1 densities (1,000–3,000 nodes), the recommended default response to node failure is **quarantine absorption**—neighboring nodes passively widen their keep-out margins to accommodate the expanding uncertainty ellipsoid of the failed node—rather than active avoidance maneuvering. This preserves the limited ΔV budget (0.5–5 m/s/year), with 15% reserved annually for failure-response maneuvers. Replacement node assignment follows a greedy nearest-neighbor algorithm prioritized by a composite score of energy value, connectivity value, and migration ΔV cost, with low-priority slots simply abandoned rather than expensively repopulated.

## Key Points

- **Deterministic over democratic**: DSSM embedded in every node's flight software eliminates the need for distributed consensus, ensuring that collision avoidance decisions remain locally executable and formally verifiable. Every node runs the state machine for its adjacency set (~6–15 neighbors); coordinators run it for the full cluster.

- **Class B ≠ Class D**: The protocol enforces a strict distinction between dead nodes (ballistic, predictable drift) and deaf nodes (potentially maneuvering, unpredictable). Quarantine geometry, keep-out margin expansion, and adjacent-node response differ fundamentally between these cases. Conflating them is identified as a primary safety risk.

- **Tiered authority with eventual consistency**: Cluster coordinators (Tier 2) can authorize intra-cluster reassignments without beacon (Tier 3) approval, but must propagate updates within 2 broadcast cycles. Beacons issue CORRECTION broadcasts to resolve inconsistencies, providing a clean separation between time-critical safety actions and system-wide catalog coherence.

- **Quarantine absorption as Phase 1 default**: At planned deployment densities, passively absorbing expanding uncertainty ellipsoids is geometrically feasible and ΔV-free. Active avoidance maneuvering is reserved for high-density clusters or overlapping multi-failure scenarios.

- **15% ΔV reservation for failure response**: This budget allocation (0.075–0.75 m/s/year depending on propulsion capability) must be tracked at the cluster level and factored into all replacement assignment decisions, constraining reassignment frequency over the 50-year operational lifetime.

- **Pre-computed migration plans**: Slot adjacency graphs and migration lookup tables should be computed on the ground and uploaded, avoiding computationally expensive in-flight optimization on resource-constrained automotive-grade processors.

## Unresolved Questions

1. **Cluster coordinator failover during active reassignment**: If the rotating cluster coordinator itself fails mid-reassignment (while slots are in RESERVED state), how does the successor coordinator recover the in-progress state machine without introducing inconsistency? The DSSM is deterministic for failure *detection*, but the replacement *assignment* step (choosing which node fills a VACANT slot) involves optimization that may not be identically reproducible.

2. **Class D resolution timeline and escalation**: The protocol marks deaf-but-maneuvering nodes as CONTESTED, transitioning to QUARANTINED after 6 hours of no detected maneuvers. But what if a Class D node *is* maneuvering—potentially into neighboring keep-out tubes? At what point does the protocol authorize active intervention (e.g., neighboring nodes performing evasive maneuvers), and how is this coordinated without communication with the rogue node?

3. **Scaling behavior at Phase 2+ densities**: The quarantine absorption default assumes Phase 1 sparsity. At 10,000+ nodes, overlapping quarantine ellipsoids from even modest failure rates (1–3%) could consume significant swarm volume. What density threshold triggers a transition from passive absorption to active avoidance as the default policy, and how is this threshold communicated across the swarm?

4. **Cross-cluster cascade scenarios**: The protocol handles intra-cluster reassignment cleanly, but failures near cluster boundaries—especially simultaneous failures in adjacent clusters—may require coordinated response across cluster coordinators with potentially different local state views. The beacon tiebreaker mechanism needs further specification for multi-cluster cascade events.

## Recommended Actions

1. **Formally verify the DSSM in seL4**: Implement the 8-state slot lifecycle state machine and prove key safety properties—particularly that no two nodes can simultaneously hold ACTIVE status for the same slot, and that QUARANTINED → VACANT transitions cannot occur without either beacon ratification or a deterministic timeout. Target this as an early deliverable for the flight software architecture.

2. **Run Monte Carlo failure cascade simulations**: Using the planned 10,000+ node simulation environment, model 3+ simultaneous failures within a single 100-node cluster (estimated ~0.1%/year probability at 3% failure rate) and cross-cluster boundary failures. Quantify quarantine ellipsoid overlap frequency, ΔV consumption under both passive absorption and active avoidance policies, and catalog staleness as a function of beacon broadcast cadence.

3. **Prototype the beacon catalog differential update mechanism**: Implement the ~48-byte amendment structure (Slot ID, state, epoch, state vector/covariance, authority signature, ratification flag) with 60-second differential and 3600-second full rebroadcast cycles. Validate update propagation latency and catalog convergence under simulated 30-day beacon-loss scenarios where nodes rely solely on local DSSM execution.

4. **Develop Class D detection and response doctrine**: Commission a focused study on distinguishing deaf-but-maneuvering nodes from dead nodes using only passive observation (optical tracking, radar ranging from neighbors). Define the decision boundary for escalating from CONTESTED to active evasion, including ΔV cost models and authority thresholds for cluster coordinators to authorize emergency maneuvers.

5. **Design the coordinator failover protocol for in-progress reassignments**: Specify how RESERVED slot states are persisted and recovered during coordinator handoff. Evaluate whether the replacement assignment algorithm can be made fully deterministic (eliminating the optimization ambiguity) or whether a lightweight two-phase commit between the outgoing and incoming coordinator is necessary—and whether that introduces unacceptable latency for safety-critical scenarios.