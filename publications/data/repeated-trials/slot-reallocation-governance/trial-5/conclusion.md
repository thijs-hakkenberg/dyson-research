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

The discussion converged on a **tiered-authority, quarantine-first** governance model as the foundational architecture for slot reallocation in the Swarm Control System. The central design insight is semantic: slots are never "reassigned"—they are **retired and new slots are commissioned**. This distinction eliminates a class of state-consistency bugs and makes the protocol amenable to formal verification on the seL4 kernel. The approach directly addresses the core tension between safety (maintaining <10⁻⁶ collision probability per node-year) and operational continuity (recovering from 10–90 annual node failures across a 1,000–3,000 node Phase 1 deployment).

The protocol partitions authority cleanly across the existing three-tier architecture. Cluster coordinators (Tier 2) own all time-critical safety decisions—failure classification, quarantine initiation, and neighbor keep-out margin expansion—operating autonomously without beacon approval. Beacon spacecraft (Tier 3) own global-consistency decisions—slot retirement and new slot commissioning—where the latency cost of minutes is acceptable because these actions occur days to months after the triggering failure event. This separation ensures that the most dangerous scenarios (Byzantine nodes, sudden silent failures) receive immediate local response while preventing the global catalog inconsistencies that could arise from fully decentralized slot commissioning near cluster boundaries.

The quarantine-first principle is the protocol's most consequential design choice. Rather than rushing to fill vacated slots, the system prioritizes trajectory characterization of failed nodes—with quarantine durations ranging from 7 days (graceful decommission) to 90 days (communication-loss-only failures where residual station-keeping capability creates unpredictable future behavior). This conservative approach distributes trivial ΔV costs (~0.01 m/s) across neighboring nodes for keep-out margin expansion while preserving the collision probability budget through the full failure-to-replacement lifecycle.

## Key Points

- **Four-class failure taxonomy** (Graceful Decommission, Sudden Silent, Erratic/Byzantine, Communication Loss Only) with distinct detection signatures, confirmation thresholds, and quarantine durations drives all downstream protocol decisions. The 5-missed-heartbeat rule (~5 minutes at 60-second cadence) balances detection speed against false positive risk, with a 24-hour reversibility window for Class B declarations.

- **Quarantine before commissioning is mandatory.** No replacement node may enter a vacated volume until the failed node's ballistic trajectory is characterized to sufficient accuracy. This eliminates the cascading conjunction risk that would arise from premature slot occupation near an uncharacterized drifting object.

- **Authority is partitioned, not shared.** Cluster coordinators handle safety-critical, time-urgent quarantine decisions; beacon spacecraft handle globally-consistent slot commissioning. Raft consensus (not PBFT) is recommended for coordinator election due to simpler formal verification, lower message complexity, and sufficiency given that Byzantine member detection is handled through cross-validation rather than Byzantine-tolerant voting.

- **A 3–5% reserve node pool** is essential to avoid taxing operational nodes with slot migrations. No individual node should migrate more than once every 5 years to preserve ΔV margin, and annual governance-related ΔV consumption should remain below 5% of total budget.

- **30-day autonomous operation is preserved** by design: nodes store quarantine schedules locally and continue honoring expanded keep-out margins without beacon contact. The system degrades gracefully—collision avoidance is maintained even when slot commissioning (requiring beacon authority) is unavailable.

- **Beacon catalog amendments** use a structured format with monotonically increasing version numbers, cryptographic signatures, and triple-redundant broadcast to ensure swarm-wide consistency convergence within 30 minutes of any amendment.

## Unresolved Questions

1. **Correlated failure response**: The protocol addresses individual and small-number failures well, but what happens during a solar particle event that simultaneously disables 10–30% of a cluster? The quarantine-first model may be untenable when the number of quarantined slots exceeds the capacity of remaining nodes to expand keep-out margins without exhausting ΔV budgets. A distinct "mass casualty" protocol tier may be needed.

2. **Cluster coordinator tenure and handoff**: The recommended 72-hour minimum tenure for governance purposes conflicts with potential shorter rotation periods for other coordinator functions. How should coordinator role decomposition work in practice, and what state must be transferred during handoff to maintain quarantine timer continuity and Class D optical tracking campaigns?

3. **Cross-cluster drift jurisdiction**: When a failed node's ballistic trajectory carries it across cluster boundaries, the handoff of tracking responsibility and quarantine authority between cluster coordinators is undefined. What protocol governs this transition, and how are beacon spacecraft involved in adjudication?

4. **Reserve pool positioning and replenishment**: Where in the swarm geometry should reserve nodes be stationed to minimize migration ΔV to any potential vacancy? How are reserves replenished over the 50-year operational lifetime as they are consumed by failures—is this purely a launch-scheduling problem or does it require in-swarm redistribution?

## Recommended Actions

1. **Implement the four-class failure taxonomy in simulation**: Using the planned 10,000+ node simulation environment, model all four failure classes with realistic automotive-grade component failure distributions. Validate the 5-heartbeat detection threshold and 24-hour reversibility window against false positive rates, targeting <1% unnecessary quarantine events. Prioritize Monte Carlo stress testing of correlated failure scenarios (solar particle events, common-mode power bus faults).

2. **Prototype the Raft-based coordinator election with governance extensions**: Build a formal seL4-compatible implementation of Raft consensus adapted for the 72-hour minimum tenure requirement and slot governance state machine (quarantine timers, failure classification tracking, optical observation tasking). Verify liveness properties under realistic communication loss scenarios matching the 30-day autonomous operation requirement.

3. **Quantify quarantine ΔV budgets through orbital mechanics analysis**: Calculate the actual per-neighbor cost of 50% keep-out margin expansion as a function of swarm density, orbital element window size, and slot geometry for representative Phase 1 configurations. Establish the maximum number of simultaneous quarantine events a cluster can sustain before ΔV constraints force protocol modification.

4. **Design and validate the beacon catalog amendment data structure**: Formalize the amendment format (including cryptographic authentication chain), implement broadcast and retransmission protocols, and measure consistency convergence time against the 30-minute target across realistic swarm communication topologies with partial link outages.

5. **Develop the reserve pool positioning strategy**: Model optimal reserve node placement as a facility-location problem minimizing worst-case migration ΔV across the swarm geometry. Integrate with mission-level launch scheduling to establish replenishment cadence compatible with the 1–3% annual failure rate over the 50-year mission lifetime.