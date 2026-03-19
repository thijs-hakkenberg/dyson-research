---
questionId: "rq-1-40"
questionSlug: "slot-reallocation-governance"
type: "discussion-conclusion"
generatedBy: "claude-opus-4-6"
generated: "2026-02-24"
roundCount: 2
terminationReason: "consecutive-conclude"
---

# Conclusion: Slot Reallocation Governance Protocol

## Summary

The discussion converged strongly on a **quarantine-first, tiered-authority governance model** for managing slot reallocation in the heliocentric swarm. The foundational architectural insight is that slots should never be "reassigned"—instead, they follow an immutable lifecycle of `ACTIVE → QUARANTINED → RETIRED`, with replacement nodes commissioned into new slots derived from retired slot templates. This semantic distinction is not merely cosmetic: it eliminates distributed state-management bugs, maps cleanly onto the seL4 microkernel's capability system, and makes the entire slot state machine formally verifiable. The protocol prioritizes collision safety over rapid slot reuse, accepting a negligible ~0.3% capacity loss from quarantined slots as the correct trade for a 50-year unserviceable mission.

The authority hierarchy was resolved with clarity. Tier-1 individual nodes hold pre-delegated authority for micro-avoidance maneuvers (≤0.01 m/s per event) requiring no approval. Tier-2 cluster coordinators autonomously declare quarantines and manage intra-cluster safety decisions using a modified Raft consensus protocol—critical for the 7–30 day autonomous operation requirement. Tier-3 beacon spacecraft serve as the sole authority for commissioning new slots and maintaining the canonical ephemeris catalog, resolving inter-cluster conflicts and providing the global consistency check that cluster coordinators cannot perform independently. This split keeps safety-critical decisions fast and local while centralizing the integrity of the swarm's single most important data structure.

The discussion also surfaced **ΔV economics as the binding constraint** on the entire governance protocol. With annual propulsion budgets of 0.5–5 m/s/year and station-keeping consuming a baseline portion, nodes can afford at most 1–2 intra-cluster slot migrations per year and effectively zero inter-cluster transfers. This hard physical limit means the governance protocol is inseparable from a **spare pre-positioning strategy**: each cluster must maintain 2–5% warm spare nodes in offset slots ready for low-cost migration into vacated positions. Without this, the protocol's commissioning mechanism has no nodes to commission.

## Key Points

- **Quarantine-first philosophy**: Failed node slots are immediately quarantined (not reassigned) with time-dependent, failure-mode-dependent keep-out tube expansion. Minimum quarantine duration is 30 days, matching the autonomous operation window and allowing full trajectory characterization of the debris.

- **Four-class failure taxonomy**: Failures are classified as Graceful Decommission (Class A), Sudden Silent Failure (Class B), Partial Degradation (Class C), and Byzantine Behavior (Class D), each with distinct detection signatures, confirmation thresholds (e.g., 3 missed 60-second heartbeats + active interrogation for Class B), and response urgency levels.

- **Immutable slot lifecycle with template inheritance**: Slots are created once and eventually retired—never mutated or reassigned. Retired slots serve as geometric templates for commissioning replacement slots, preserving validated packing geometry without requiring full swarm-level re-optimization.

- **Raft consensus at Tier-2, centralized registry at Tier-3**: Cluster coordinators use modified Raft (quorum of 51% of currently-active nodes) for autonomous quarantine decisions. Beacon spacecraft maintain the canonical append-only slot registry, countersign state transitions, and resolve cross-cluster conflicts. PBFT was rejected as unnecessary overhead given authenticated communication links.

- **ΔV budget caps reassignment rate**: Annual reassignment ΔV is capped at ≤10% of total budget (0.05–0.5 m/s/year). Intra-cluster adjacent-slot migration costs ~0.01–0.05 m/s; cross-cluster migration is effectively prohibitive. This makes pre-positioned warm spares (2–5% per cluster) a mandatory architectural element.

- **Delta-compressed, authenticated catalog broadcasts**: The beacon ephemeris catalog uses ~128-byte signed slot records, with full catalog broadcast every 24 hours and delta updates every 300 seconds. Emergency quarantine amendments are broadcast immediately with triple redundancy. All entries require Ed25519 signatures from the authorizing coordinator and beacon countersignature.

## Unresolved Questions

1. **Quarantine zone cascading across cluster boundaries**: When a worst-case 72-hour quarantine envelope (~43 km for an uncharacterized 0.5 m/s impulse) spans multiple clusters, the cross-cluster handshake protocol (60-second ACK window with beacon escalation) was proposed but not validated. How does this perform under simultaneous multi-cluster failures, and what happens if the beacon is unreachable during the escalation?

2. **Correlated failure scenarios**: The ΔV-constrained spare capacity (2–5 nodes per cluster) is adequate for uniformly distributed failures but may be exhausted by correlated events (solar storms, manufacturing batch defects). What is the optimal spatial distribution strategy for production batches, and should the protocol include a "cluster emergency" state that triggers inter-cluster spare redistribution despite the high ΔV cost?

3. **Cluster coordinator rotation during active quarantine**: The consensus specifies rotating cluster coordinators, but the Raft leader maps to the coordinator role. How are in-progress quarantine state machines handed off during coordinator rotation without risking state inconsistency, and what is the minimum overlap period required?

4. **Catalog scalability at 10,000+ nodes**: The delta-compressed broadcast scheme works for Phase 1 (3,000 slots, 384 KB full catalog), but scaling to 10,000+ nodes with accumulated retired slot templates may stress inter-satellite link bandwidth. At what swarm size does the catalog architecture require fundamental redesign (e.g., hierarchical sharding by cluster)?

## Recommended Actions

1. **Formally specify and verify the slot state machine on seL4**: Implement the 5-state lifecycle (`ACTIVE → SUSPECT → QUARANTINED → AVAILABLE → COMMISSIONED`, plus terminal `RETIRED`) as a formally verified component within the seL4 capability system. Define preconditions, authorized initiators, and invariants for each transition. This is the highest-priority deliverable as it underpins all other protocol elements.

2. **Build quarantine propagation simulation in the 10,000+ node Monte Carlo environment**: Model slot adjacency graphs with quarantine depth as the primary metric. Simulate Class B failures with varying uncharacterized ΔV magnitudes (0.01–1.0 m/s) to identify critical slots where quarantine zones cascade across >5 neighbors or span cluster boundaries. Use results to inform slot placement optimization and critical-slot enhanced monitoring policies.

3. **Prototype the modified Raft consensus for Tier-2 quarantine decisions**: Implement and test the cluster-level Raft protocol with dynamic quorum (51% of active nodes), including the cross-cluster handshake mechanism. Validate against scenarios with simultaneous failures reducing cluster size below quorum thresholds, and measure consensus latency under realistic inter-satellite link conditions.

4. **Develop spare pre-positioning strategy and ΔV budget allocation model**: Quantify the trade-off between spare node percentage (energy collection loss) and reassignment capacity (failure resilience) as a function of cluster size, failure rate, and ΔV budget. Produce a recommended spare allocation policy for Phase 1 deployment, including manufacturing batch distribution rules to mitigate correlated failure risk.

5. **Define and test the beacon catalog broadcast protocol end-to-end**: Implement the 128-byte slot record format with Ed25519 authentication, delta compression, and emergency amendment broadcasting. Test full catalog reconstruction from log replay after 30-day communication gaps, and validate update propagation latency across the three-tier architecture under nominal and degraded (beacon loss) conditions.