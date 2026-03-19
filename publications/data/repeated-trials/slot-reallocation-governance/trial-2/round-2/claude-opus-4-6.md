---
questionId: "rq-1-40"
questionSlug: "slot-reallocation-governance"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
roundNumber: 2
generated: "2026-02-23"
type: "discussion-response"
---

# Slot Reallocation Governance: From Pre-Computed Contingencies to Operational Reality

## Building on Round 1 Consensus

Round 1 converged on several important principles: pre-computed contingency tables over real-time negotiation (Claude Opus), quarantine-first over backfill-first (Gemini), and a two-phase quarantine→reclaim state machine with cluster-local authority and beacon notarization (GPT). I agree with all three positions and consider them largely complementary rather than competing. My contribution here is to push toward **implementation specificity** on the unresolved tensions and to address several critical gaps that Round 1 left open.

---

## 1. The Unresolved Authority Boundary Problem

Round 1 established that Tier 2 cluster coordinators should handle time-critical safety actions and Tier 3 beacons should handle catalog notarization. But the actual boundary condition is harder than anyone acknowledged. Consider this scenario:

**Node 47 in Cluster A fails (F2-class sudden failure). Its projected drift trajectory will carry it across the Cluster A / Cluster B boundary within 14 hours.**

Who owns this? Cluster A's coordinator detected the failure. Cluster B's coordinator needs to issue avoidance maneuvers to its own nodes. The beacon may be 3–8 light-seconds away. This is precisely the scenario where cascading conjunctions originate, and it falls in a governance gap.

### Recommended Solution: Bilateral Cluster Handshake with Beacon Arbitration

I propose a **cross-cluster conjunction alert (CCCA) protocol** as a mandatory extension to the intra-cluster quarantine mechanism:

1. **Cluster A coordinator** propagates the failed node's trajectory forward 72 hours (well within onboard computational capacity for a single-body Keplerian propagation with J2-equivalent solar radiation pressure perturbations).

2. If the propagated trajectory intersects **any adjacent cluster's keep-out volume envelope**, Cluster A's coordinator transmits a **CCCA message** directly to the affected cluster coordinator(s) via inter-cluster mesh links. This message contains: failed node ID, last known state vector, failure class, propagated trajectory coefficients, and Cluster A's quarantine zone definition.

3. **Cluster B coordinator** independently verifies the trajectory propagation (trust but verify—this is a safety-critical system, not a trust exercise), then establishes its own complementary quarantine zone on its side of the boundary.

4. Both coordinators **simultaneously** report to the beacon for catalog notarization. The beacon resolves any inconsistencies in quarantine zone definitions and publishes the authoritative update.

5. If Cluster B's coordinator is unreachable (its own coordinator has failed, or mesh link is degraded), Cluster A escalates directly to the beacon, which issues a **directed quarantine order** to Cluster B's nodes individually via broadcast.

The key design principle: **no cluster coordinator ever needs permission to protect its own nodes**, but cross-boundary situations require bilateral coordination with beacon backstop. This maps cleanly onto the existing three-tier architecture without introducing a new governance layer.

---

## 2. Pre-Computed Contingency Tables: Practical Sizing and Update Cadence

Claude Opus's Round 1 insight about pre-computed reassignment tables is exactly right, but we need to nail down the implementation parameters.

### Table Structure

For a ~100-node cluster, each node needs contingency entries for:
- **Its own failure**: passivation trajectory and slot release notification (trivial, ~100 bytes)
- **Each neighbor's failure**: typically 6–12 adjacent slots in a quasi-hexagonal packing, with pre-computed quarantine zone boundaries and optional avoidance maneuver sequences (~500 bytes per neighbor)
- **Coordinator failure**: fallback coordinator election priority list and interim self-governance rules (~1 KB)
- **Multi-failure scenarios**: 2-of-N neighbor failures for the most critical adjacency pairs (~2 KB for top-10 pairwise scenarios)

**Total per-node contingency table: ~10–15 KB.** This is trivially small for any modern flight computer and can be stored in radiation-hardened MRAM alongside the ephemeris catalog.

### Update Cadence

The contingency tables must be refreshed when:
- Orbital element windows drift due to stationkeeping maneuvers (cadence: weekly to monthly)
- A slot reassignment changes the local topology (event-driven)
- Solar radiation pressure models are updated with new area-to-mass ratio estimates (cadence: quarterly)

I recommend **beacon-computed, cluster-coordinator-distributed updates on a 14-day baseline cadence**, with event-driven patches for topology changes. The beacon has the global view needed to compute cross-cluster boundary contingencies; the cluster coordinator handles distribution and acknowledgment tracking. This fits within the 30-day autonomous operation window with comfortable margin—even if one update cycle is missed, the tables remain valid for ~6 weeks given typical orbital element drift rates in heliocentric orbit at ~1 AU.

---

## 3. The ΔV Budget Allocation Problem

Round 1 identified ΔV cost as a constraint but didn't quantify the allocation framework. This matters enormously for long-term swarm sustainability.

### Baseline ΔV Partitioning

With 0.5–5 m/s/year total budget (I'll use 2 m/s/year as a working median for automotive-grade cold-gas or electrospray systems), I recommend:

| Function | Allocation | Rationale |
|----------|-----------|-----------|
| Stationkeeping (SRP, orbital maintenance) | 60% = 1.2 m/s/yr | Primary operational need |
| Collision avoidance maneuvers | 20% = 0.4 m/s/yr | Safety reserve, must be available on demand |
| Slot migration (reassignment) | 10% = 0.2 m/s/yr | Enables ~1 slot migration per node lifetime |
| Margin/contingency | 10% = 0.2 m/s/yr | End-of-life passivation, unexpected perturbations |

### Slot Migration Cost Estimation

For a typical keep-out tube radius of ~100 m and inter-slot spacing of ~500 m (consistent with the ±1 m to ≤5 km navigation accuracy range, biased toward the tighter end for Phase 1 density), a single-slot migration (moving one position in the adjacency graph) requires a Hohmann-like two-impulse transfer of approximately:

**ΔV ≈ 2 × (Δa × n) / 2 ≈ n × Δa**

where n is the mean motion (~2×10⁻⁷ rad/s at 1 AU) and Δa is the semi-major axis change (~500 m). This gives ΔV ≈ 0.1 mm/s per slot hop—**essentially negligible** for radial repositioning.

However, the dominant cost is **phasing**: changing the mean anomaly to arrive at the correct position within the new slot's orbital element window. For a 500 m along-track repositioning at 1 AU, the phasing maneuver over a reasonable timeline (1–4 weeks) costs approximately 0.01–0.05 m/s. This means each node can afford **4–20 slot migrations over its lifetime** from the 10% allocation, which is more than sufficient given the 1–3% annual failure rate.

**Critical implication**: ΔV is not the binding constraint on slot reallocation. **Catalog update latency and quarantine duration are the binding constraints.** This reframes the optimization problem entirely—we should optimize for fast, safe quarantine resolution rather than ΔV-minimizing migration paths.

---

## 4. The Formally Verified State Machine

The slot lifecycle must be implemented as a formally verified state machine within the seL4 kernel's trusted computing base. I propose seven states:

```
ACTIVE → SUSPECT → QUARANTINED → CHARACTERIZED → {RECLAIMABLE | ABANDONED} → ASSIGNED → ACTIVE
```

- **ACTIVE**: Normal operations, node occupying slot within orbital element window
- **SUSPECT**: Missed heartbeats detected, confirmation period active (3–5 missed heartbeats at 10–60 second intervals = 30 seconds to 5 minutes)
- **QUARANTINED**: Failure confirmed, keep-out tube expanded by 2–3× nominal radius, adjacent nodes alerted
- **CHARACTERIZED**: Failed node trajectory propagated and validated over ≥2 orbital determination arcs (~hours to days depending on tracking geometry)
- **RECLAIMABLE**: Trajectory confirmed non-threatening, slot available for reassignment
- **ABANDONED**: Trajectory too uncertain or slot geometry compromised, permanent exclusion zone established
- **ASSIGNED**: Replacement node committed to migration, in transit

Each transition has formally specified preconditions, postconditions, and invariants. The critical safety invariant: **no slot may transition from QUARANTINED to RECLAIMABLE unless the failed node's trajectory has been independently verified by at least two sources** (cluster coordinator propagation + beacon tracking or + adjacent node optical tracking).

This state machine should be verified using the same formal methods toolchain (likely Isabelle/HOL) used for the seL4 kernel itself, ensuring that no implementation bug can skip the quarantine phase or assign two nodes to the same slot.

---

## 5. Open Issues Requiring Simulation

Two questions I cannot resolve analytically and recommend for the 10,000+ node Monte Carlo simulation environment:

**A. Quarantine zone cascading**: When a quarantine zone expands a keep-out tube by 2–3×, does this force adjacent nodes into their own avoidance maneuvers, creating a "quarantine cascade"? At what packing density does this become pathological? I suspect the answer depends strongly on the ratio of keep-out tube radius to inter-slot spacing, and there may be a critical density threshold above which the swarm becomes fragile to single-node failures.

**B. Coordinator failure during active reallocation**: If a cluster coordinator fails while managing another node's quarantine→reclaim transition, the state machine is in an intermediate state with no authoritative owner. The fallback coordinator election must include state transfer of all in-progress reallocation transactions. What is the probability of data loss during this handoff, and what are the safety implications?

---

## Summary Position

Slot reallocation governance should be implemented as a **formally verified state machine with pre-computed contingency tables, cluster-local authority for intra-cluster actions, bilateral handshake for cross-cluster situations, and beacon notarization for global catalog consistency**. The binding constraint is not ΔV but catalog update latency and quarantine characterization time. The protocol must be designed, verified, and tested as safety-critical software with the same rigor as collision avoidance itself—because it *is* collision avoidance, just on a longer timescale.