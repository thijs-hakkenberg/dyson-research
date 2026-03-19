---
questionId: "rq-1-40"
questionSlug: "slot-reallocation-governance"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
roundNumber: 3
generated: "2026-02-23"
type: "discussion-response"
---

# Slot Reallocation Governance Protocol: Round 3 — Closing the Engineering Gaps

## Executive Summary

Two rounds of convergent analysis have established the conceptual architecture: quarantine-first, deterministic state machines, tiered authority with Tier-2 primacy, and physics-driven hazard volumes. This round, I focus on **the three hardest remaining problems** that will determine whether this protocol actually works across a 50-year operational lifetime with 10,000+ nodes: (1) the observability problem—how do surviving nodes actually track a dead satellite's trajectory with sufficient accuracy to bound quarantine zones; (2) the ΔV sustainability problem—proving that the cumulative cost of avoidance maneuvers and slot migrations doesn't consume the propulsion budget within a decade; and (3) the protocol failure modes—what happens when the governance system itself degrades.

---

## 1. The Observability Problem: Tracking Dead Nodes with a Distributed Sensor Network

Previous rounds correctly identified that quarantine zone geometry depends on bounding the failed node's covariance ellipsoid. But we glossed over *how* surviving nodes actually observe the dead one. This is the critical engineering gap.

**The sensing chain.** Each operational node carries star trackers and likely inter-satellite link (ISL) ranging capability. A dead node is a ~1–10 m² object at distances of hundreds of meters to kilometers. It is not cooperative—no transponder, no retroreflector (unless we mandate one, which I recommend). The observation modes are:

- **Passive optical**: Sunlit dead node against star background. At 1 km range, a 3 m² satellite subtends ~1.7 mrad—easily resolved by a star tracker with ~10 arcsec accuracy. But this only works when geometry permits solar illumination from the observer's perspective. In heliocentric orbit at ~1 AU, illumination conditions are generally favorable, but the observer must dedicate tracker time to debris tracking rather than attitude determination.

- **ISL ranging to silence**: The absence of a ranging response is itself data—it confirms the node is non-cooperative. But active radar ranging to a non-cooperative target requires dedicated RF hardware that the baseline design likely doesn't include.

- **Collaborative triangulation**: Multiple neighboring nodes each take bearing measurements. With 3+ observers at known positions (±1 m navigation accuracy per spec), triangulation yields position fixes. At 1 km baseline and 10 arcsec bearing accuracy, cross-range position error is ~50 mm. Along-range (depth) error depends on baseline geometry but is typically 10–100× worse—call it 0.5–5 m.

**My recommendation: mandate corner-cube retroreflectors on every node.** Mass cost: ~50 g. This enables laser ranging from any node with a laser comm terminal, providing sub-meter range accuracy to dead nodes. This single hardware addition transforms the observability problem from "hard" to "solved" and should be added to the node specification immediately. The cost-benefit ratio is extraordinary—50 g of passive hardware eliminates the largest uncertainty in the entire governance protocol.

**Observation cadence and covariance propagation.** With collaborative triangulation every ~6 hours (compatible with cluster coordinator duty cycles), a dead node's state vector can be maintained to ~10 m position accuracy over weeks. The covariance growth rate depends on unmodeled perturbations—primarily solar radiation pressure (SRP) uncertainty. For a tumbling dead node, the SRP area-to-mass ratio is uncertain by perhaps ±50%, creating acceleration uncertainty of ~10⁻⁸ m/s². Over 30 days, this produces position uncertainty growth of:

Δx ≈ ½ · a_unc · t² ≈ ½ · 10⁻⁸ · (2.6×10⁶)² ≈ 34 m

This is manageable. A 34 m position uncertainty at 30 days means quarantine zones need only be ~100 m radius (3σ + margin), not kilometers. This is a crucial quantitative result: **quarantine zones are small relative to typical slot spacing**, meaning most adjacent slots are unaffected by a single failure.

---

## 2. ΔV Sustainability: A 50-Year Budget Model

The specification allocates 0.5–5 m/s/year for stationkeeping. Slot reallocation imposes three categories of ΔV cost:

**Category 1: Avoidance maneuvers by neighbors of failed nodes.** With quarantine zones of ~100 m and keep-out tubes of similar scale, most neighbors won't need to maneuver at all—the quarantine zone fits within the existing buffer between slots. For the ~2–4 immediately adjacent nodes that do need adjustment, a typical avoidance maneuver is a few mm/s impulse. At 10–90 failures/year across the swarm, any individual node faces perhaps 0–2 neighbor failures per year. **Annual ΔV cost: ~0.01–0.05 m/s.** This is 1–10% of the minimum budget. Sustainable.

**Category 2: Slot migration for replacement nodes.** A replacement node launched to fill a vacated slot must transfer from its injection orbit to the target slot. If replacements are deployed in batches and injected near the target cluster, the migration ΔV is dominated by phasing within the cluster—typically meters to tens of meters of orbital element adjustment. For heliocentric orbits with ~1 km slot spacing, a phase adjustment of 1 km over a synodic period of weeks requires ΔV of ~0.01–0.1 m/s. **This is affordable but must be budgeted at manufacture time**—replacement nodes should carry a dedicated migration ΔV allocation of ~0.5 m/s beyond the standard stationkeeping budget.

**Category 3: Cumulative slot compaction.** Over decades, random failures create a Swiss-cheese pattern of vacancies. Periodically, the swarm benefits from compacting—shifting nodes to close gaps and improve energy collection density. This is the most expensive operation. Moving a node by one full slot spacing (~1 km) in heliocentric orbit costs ~0.1–1 m/s depending on timeline. **Compaction should be performed no more than once per 5–10 years per cluster**, triggered when vacancy fraction exceeds ~10%. Annual amortized cost: ~0.05–0.1 m/s/year.

**Total governance ΔV overhead: ~0.1–0.25 m/s/year**, consuming 5–25% of the minimum 0.5 m/s/year budget at the low end, or 2–5% of the 5 m/s/year budget at the high end. **This is feasible but not negligible.** The propulsion budget specification should explicitly reserve 20% for governance-related maneuvers.

---

## 3. Protocol Failure Modes: When Governance Itself Breaks

The most dangerous scenario isn't a single node failure—it's a governance protocol failure. Three specific modes demand attention:

**Mode 1: Cluster coordinator failure during active quarantine management.** If the coordinator dies while managing a quarantine event, the quarantine state machine is orphaned. **Solution**: Every quarantine action is encoded as a signed, timestamped state transition broadcast to all cluster members. Any node can reconstruct the current quarantine map from the broadcast log. The replacement coordinator (elected per the rotating coordinator protocol) inherits a fully consistent state. This requires that quarantine state transitions be idempotent and order-independent—a constraint that must be enforced in the formal verification of the seL4 kernel's governance module.

**Mode 2: Correlated failures (solar storm, manufacturing defect batch).** If 5–10 nodes in a single cluster fail simultaneously, the quarantine zones may overlap, the observation network is degraded, and the coordinator election may lack quorum. **Solution**: Define a "cluster emergency" threshold (e.g., >5% simultaneous failures). When triggered, the beacon spacecraft (Tier 3) assumes direct governance of the affected cluster, broadcasting an authoritative quarantine map and suspending normal slot reassignment until the situation stabilizes. This is the one scenario where Tier 3 must override Tier 2 authority. The beacon's catalog broadcast should include a "cluster status" field with emergency flags.

**Mode 3: Byzantine behavior from a malfunctioning (not dead) node.** A node with corrupted software might broadcast false heartbeats, claim slots it doesn't occupy, or refuse to acknowledge quarantine boundaries. This is the hardest case. **Solution**: Slot ownership is verified by *physical observation*, not just protocol messages. If a node claims to occupy slot X but neighboring nodes observe it at slot Y's coordinates, the cluster coordinator can revoke its slot lease. This requires the "slot lease" data structure from Round 2 to include a "last verified position" field updated by neighbor observations. Revocation requires a supermajority (>2/3) of observing neighbors to agree the node is out of position—a lightweight Byzantine fault detection mechanism that doesn't require full BFT consensus.

---

## 4. Concrete Protocol Specification

Synthesizing all three rounds, the complete state machine has **six slot states**:

| State | Authority | Duration | Entry Condition |
|-------|-----------|----------|-----------------|
| **ACTIVE** | Node self-governs | Indefinite | Valid lease + position verification |
| **SUSPECT** | Cluster coordinator | 3–10 heartbeat cycles (~minutes) | Missed heartbeats |
| **QUARANTINE** | Cluster coordinator | Hours to weeks | Failure confirmed; hazard volume computed |
| **AVAILABLE** | Cluster coordinator | Until claimed | Dead node trajectory bounded; zone clear |
| **MIGRATING** | Cluster coordinator + assignee | Days to weeks | Replacement node en route |
| **EMERGENCY** | Beacon (Tier 3) | Until resolved | Correlated failure threshold exceeded |

Transitions are deterministic, signed, and broadcast. Any node can independently verify any transition by checking the cryptographic signature chain and the physical observables (heartbeat logs, position measurements).

---

## 5. Critical Recommendations for the Specification

1. **Add corner-cube retroreflectors to the node hardware spec.** 50 g, passive, transforms dead-node tracking from uncertain to reliable.

2. **Reserve 20% of ΔV budget for governance maneuvers.** Make this explicit in the propulsion specification so mission planners don't treat the full budget as available for stationkeeping.

3. **Define "cluster emergency" thresholds and Tier-3 override authority** in the beacon spacecraft requirements. This is the only scenario requiring centralized control and must be pre-authorized.

4. **Require quarantine state transitions to be idempotent and order-independent** in the seL4 formal verification scope. This is the mathematical property that makes coordinator failover safe.

5. **Include dead-node tracking as a formal mission requirement** for the star tracker and ISL subsystems. Allocate 5–10% of sensor duty cycle to debris observation.

6. **Prototype the six-state machine in the 10,000-node simulation environment** with Monte Carlo failure injection, including correlated failure scenarios, before finalizing the beacon catalog data structure.

The governance protocol is now sufficiently specified to begin formal verification and simulation. The remaining open question—cluster coordinator duty cycle and election mechanism—should be resolved in parallel, as it directly affects quarantine management latency.