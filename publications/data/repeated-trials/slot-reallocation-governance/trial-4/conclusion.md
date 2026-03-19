---
questionId: "rq-1-40"
questionSlug: "slot-reallocation-governance"
type: "discussion-conclusion"
generatedBy: "claude-opus-4-6"
generated: "2026-02-24"
roundCount: 2
terminationReason: "consecutive-conclude"
---

# Slot Reallocation Governance Protocol: Discussion Conclusion

## Summary

The discussion converged on a **tiered-authority, deterministic state machine architecture** as the foundation for slot reallocation governance, with cluster coordinators (Tier 2) holding autonomous authority for time-critical quarantine and intra-cluster reassignment, and beacon spacecraft (Tier 3) serving as canonical catalog publishers, cross-cluster arbiters, and consistency enforcers. The critical insight from Round 1—that slot reallocation is primarily a state machine problem rather than a distributed consensus problem—survived scrutiny but was refined in Round 2 to acknowledge that approximately 15% of cases (cross-cluster boundary slots and correlated failure events) require coordination mechanisms beyond purely deterministic local rules.

The protocol centers on a **quarantine-first safety posture**: failed nodes trigger expanding keep-out zones modeled by trajectory uncertainty propagation, and slots transition through a well-defined state sequence (ACTIVE → SUSPECT → QUARANTINED → AVAILABLE → MIGRATING → ACTIVE). This quarantine zone growth was identified as the single most important forcing function for the entire protocol—it drives reassignment urgency, ΔV budget allocation, escalation thresholds, and ultimately determines whether the system can maintain the 10⁻⁶ collision probability requirement. The discussion also established that ΔV is the binding constraint on reassignment frequency, motivating a formal escrow model that partitions each node's propulsion budget across station-keeping, collision avoidance, slot migration, and end-of-life disposal.

Round 2 importantly surfaced three problems that Round 1 underspecified: correlated failure events (solar particle events, batch defects) that can overwhelm local deterministic rules; cross-cluster boundary coordination that creates genuine distributed agreement requirements; and the long-term quarantine zone growth problem where unremoved failed nodes progressively consume neighboring slots. These remain the primary areas requiring simulation validation and further architectural refinement before the protocol can be considered implementation-ready.

## Key Points

- **Deterministic state machine for the common case (~85%)**: Intra-cluster, non-boundary slot reallocations should be handled by deterministic priority queues computed identically by all cluster members, eliminating the need for Byzantine fault-tolerant consensus algorithms (PBFT, Raft) and simplifying formal verification on the seL4 kernel.

- **Four-class failure taxonomy drives response timing**: Graceful shutdown (Class A, ~60% of failures), sudden silent failure (Class B, 3-minute confirmation), erratic behavior (Class C, most dangerous, requires neighbor cross-validation), and ambiguous communication loss (Class D, 30-minute extended window). Each class maps to specific detection signatures, confirmation thresholds, and quarantine geometries.

- **Quarantine zone growth is the critical forcing function**: Failed node trajectory uncertainty expands over time due to unknown tumbling, solar radiation pressure, and potential propulsion leakage. The quarantine radius model R_quarantine(t) = R_nominal + σ_pos(t) × k_safety must be validated against realistic propagation models, as errors in either direction compromise safety or waste ΔV.

- **ΔV escrow model constrains reassignment economics**: A 60/20/10/10 budget split (station-keeping / collision avoidance / slot migration / end-of-life disposal) provides each node a one-time migration capability while preserving operational and safety reserves across the 50-year mission. Spare nodes (3–5% per cluster) parked at cluster periphery offer a more ΔV-efficient alternative to reshuffling operational nodes.

- **Beacon-published append-only catalog with cryptographic chaining**: Ephemeris catalog amendments are structured as a hash-chained log enabling nodes to reconstruct current state after communication gaps of up to 30 days. Tiered broadcast cadence (full snapshots weekly, deltas every 10–60 seconds) balances bandwidth against consistency requirements.

- **Escalation hierarchy for edge cases**: Cross-cluster boundary slots use a sealed-bid mechanism arbitrated by beacons (adding minutes of latency but acceptable given quarantine buffers). Correlated failure events (>3 nodes per cluster in 24 hours) trigger beacon-level cluster restructuring, the only scenario potentially requiring human-in-the-loop review within the 7–30 day ground contact window.

## Unresolved Questions

1. **How should quarantine zone growth be modeled for tumbling spacecraft with unknown attitude?** The solar radiation pressure cross-section varies dramatically with attitude, and tumbling dynamics may be chaotic. What fidelity of propagation model is computationally feasible on automotive-grade processors, and what safety margin is needed to compensate for model uncertainty without being so conservative that quarantine zones consume entire cluster regions?

2. **What is the correlated failure threshold that overwhelms the protocol?** At what point does simultaneous node loss (e.g., from a solar particle event affecting 10–20% of a cluster) cause cascading quarantine zone overlaps, ΔV budget exhaustion from emergency avoidance maneuvers, or catalog divergence that degrades collision prediction below 10⁻⁶? Is cluster merging a viable recovery strategy, and what are its ΔV costs?

3. **How should cluster coordinator succession handle contested or partitioned scenarios?** Pre-computed succession lists work for clean coordinator failures, but network partitions could produce two nodes simultaneously claiming coordinator authority for the same cluster. What is the minimum reconciliation mechanism that avoids conflicting slot assignments without requiring full consensus?

4. **What is the long-term steady-state slot occupancy under realistic failure and replacement rates?** Over the 50-year mission, cumulative failures, quarantine zone persistence, and ΔV depletion will progressively reduce effective swarm capacity. At what replacement deployment cadence does the swarm maintain target energy collection, and how does this interact with the phased deployment schedule (Phase 1: 1,000–3,000 nodes → Phase 2: 10,000+ nodes)?

## Recommended Actions

1. **Develop and validate the quarantine zone propagation model (Priority 1)**: Build a computationally tractable trajectory uncertainty propagation model for failed/tumbling spacecraft in heliocentric orbit, incorporating solar radiation pressure with unknown cross-section, residual angular momentum, and potential propulsion leakage. Validate against historical LEO debris conjunction screening data (adapted for heliocentric dynamics). This model is the prerequisite for all downstream protocol parameters and should be the first deliverable from the simulation campaign.

2. **Implement the deterministic state machine prototype on seL4**: Code the five-state slot lifecycle (ACTIVE/SUSPECT/QUARANTINED/AVAILABLE/MIGRATING) with the four failure class detection rules as a formally verifiable module targeting the seL4 microkernel. Test with simulated heartbeat streams including false-positive scenarios (transient communication loss, solar conjunction interference). This validates the core architectural claim that deterministic rules suffice for the common case.

3. **Run correlated failure Monte Carlo simulations**: Using the planned 10,000+ node simulation environment, inject correlated failure storms (5–15% cluster loss over 1–6 hour windows) and measure: quarantine zone overlap area, cumulative emergency avoidance ΔV, catalog convergence time, and collision probability. Identify the failure rate threshold at which the protocol degrades below the 10⁻⁶ safety requirement, and use this to set the escalation trigger for beacon-level cluster restructuring.

4. **Define the beacon catalog amendment data structure and broadcast protocol**: Specify the exact wire format for the append-only, hash-chained catalog log, including authentication (Ed25519 signatures against pre-deployed key registry), compression, and tiered broadcast cadence. Prototype the 30-day replay mechanism where a node reconstructs current catalog state from a stale snapshot plus accumulated deltas. Quantify bandwidth requirements against available inter-node communication capacity.

5. **Conduct a 50-year ΔV lifecycle analysis**: Run stochastic simulations of the full mission timeline with realistic failure rates (including temporal clustering), the proposed 60/20/10/10 escrow model, and varying spare node deployment strategies. Determine whether the 10% migration reserve is sufficient, identify when nodes become ΔV-bankrupt and must be retired early, and quantify the replacement deployment rate needed to maintain swarm capacity. This analysis directly informs the spare node percentage and the economic case for on-orbit servicing or refueling.