---
questionId: "rq-1-40"
questionSlug: "slot-reallocation-governance"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
roundNumber: 3
generated: "2026-02-24"
type: "discussion-response"
---

# Slot Reallocation Governance Protocol: From Architecture to Implementation Specification

## Executive Summary

After two rounds of productive convergence, we have strong consensus on the quarantine-first, tiered-authority model with asymmetric drift-aware exclusion zones. The critical remaining gaps are **implementation-level decisions that will determine whether this protocol survives contact with real orbital mechanics and real software constraints.** I want to drive toward three specific engineering commitments:

1. **A concrete state machine specification** with formally verifiable transitions suitable for the seL4 kernel.
2. **Quantified ΔV budgets** that prove the protocol is feasible within the 0.5–5 m/s/year envelope—including the neighbor-nudge costs that Round 2 correctly identified as the dominant expense.
3. **The beacon catalog update problem** as the actual long-pole risk, not failure detection or quarantine geometry.

---

## 1. The Slot State Machine: Seven States, Formally Verifiable

The protocol must be implementable as a deterministic finite state machine running on the seL4 microkernel. I propose seven slot states with explicit transition guards:

| State | Authority | Entry Condition | Exit Condition |
|-------|-----------|----------------|----------------|
| **ACTIVE** | Node self-reports | Valid heartbeat within τ_heartbeat | Missed heartbeats OR graceful shutdown |
| **SUSPECT** | Cluster coordinator | ≥3 consecutive missed heartbeats (~15–30s at 5–10s intervals) | Confirmed alive → ACTIVE; confirmed dead → QUARANTINE; timeout → QUARANTINE |
| **QUARANTINE** | Cluster coordinator | SUSPECT timeout OR sudden failure signature | Drift trajectory characterized AND neighbor safety confirmed → FENCED |
| **FENCED** | Cluster coordinator | Quarantine zone geometry computed, neighbor keep-out tubes adjusted | Beacon confirmation received → VACANT; drift threatens cluster boundary → ESCALATED |
| **ESCALATED** | Beacon spacecraft | Failed node drift crosses cluster boundary OR multiple simultaneous failures | Beacon computes inter-cluster resolution → FENCED or VACANT |
| **VACANT** | Beacon spacecraft | Failed node trajectory fully characterized, no conjunction risk | Replacement node assigned → LEASED; no replacement available → DORMANT |
| **LEASED** | Cluster coordinator + Beacon | Replacement node within 1 km of slot center, ephemeris converged | Beacon publishes permanent catalog entry → ACTIVE |

**Why seven states instead of four or five:** The SUSPECT→QUARANTINE distinction prevents false-positive reassignment (a node in solar conjunction shadow may miss heartbeats without being failed). The FENCED→VACANT distinction separates the safety problem (is the dead node's trajectory known?) from the capacity problem (can we put something there?). The LEASED state implements the lease-then-deed model from Round 2 while giving the beacon time to validate the replacement node's actual trajectory against the planned one.

**Formal verification target:** Every transition must be expressible as a predicate over observable state variables (heartbeat counters, conjunction probability estimates, ΔV remaining). No transition depends on ground-in-the-loop input. The seL4 implementation should guarantee that no slot can transition from QUARANTINE directly to ACTIVE—the FENCED and VACANT states are mandatory waypoints.

---

## 2. ΔV Budget Analysis: The Numbers That Matter

Round 2 correctly identified that **neighbor adjustment, not replacement migration, is the dominant ΔV cost.** Let me quantify this.

**Assumptions** (from GPT specifications):
- Orbital element window: ±1 km cross-track, ±5 km along-track (conservative for heliocentric ~1 AU)
- Keep-out tube radius: ~100 m (derived from navigation accuracy and 10⁻⁶ collision probability)
- Cluster density: ~100 nodes in a volume roughly 50 km × 50 km × 10 km
- Mean inter-node spacing: ~2–5 km
- Annual node failure rate: 1–3% → 1–3 failures per 100-node cluster per year

**Neighbor nudge cost per failure event:**
To expand keep-out clearance around a failed node by 200 m (doubling the buffer), a neighbor at 1 AU heliocentric orbit needs a cross-track displacement of ~200 m over ~24 hours. Using the Clohessy-Wiltshire approximation adapted for heliocentric relative motion:

- Δv ≈ 2πΔx / T_orbit × (correction factor for heliocentric vs. LEO) 
- For 200 m displacement maintained over days: **~0.01–0.05 m/s per neighbor per event**
- Typical affected neighbors: 4–8 nodes
- **Total cluster ΔV cost per failure: 0.04–0.4 m/s distributed across neighbors**

**Annual budget impact at 3% failure rate:**
- 3 failures/year × 0.04–0.4 m/s = **0.12–1.2 m/s/year consumed by neighbor adjustments**
- Against a budget of 0.5–5 m/s/year, this represents **2.4–240% of available ΔV**

This is the critical finding: **at the low end of the ΔV budget (0.5 m/s/year) with high failure rates (3%), neighbor adjustment alone could consume the entire propulsion budget.** This has three implications:

1. **Nodes with low ΔV budgets cannot afford to be frequent "nudge neighbors."** The cluster coordinator must track cumulative ΔV expenditure per node and preferentially assign nudge maneuvers to nodes with remaining margin.
2. **Quarantine geometry must minimize the number of affected neighbors.** The asymmetric, drift-aware exclusion zones from Round 2 are not optional—they are ΔV-critical. A spherical exclusion zone might affect 6–8 neighbors; a drift-aligned ellipsoidal zone might affect only 2–3.
3. **The 0.5 m/s/year lower bound may be insufficient.** I recommend the project baseline a minimum of **1.5 m/s/year** for any node that could be a quarantine neighbor (i.e., all nodes not on the swarm periphery). This should feed back into the propulsion system sizing.

**Replacement node migration cost:**
Moving a spare node from a parking orbit or cluster periphery into a vacated slot 5–10 km away: **~0.1–0.5 m/s** depending on urgency and phasing. This is a one-time cost charged to the replacement node, which is acceptable if the replacement has a full ΔV budget. But it means **replacement should happen at most once per slot per year** to stay within budget—reinforcing the quarantine-first approach.

---

## 3. The Beacon Catalog Update Problem: The Actual Long Pole

I believe the discussion has underweighted the most dangerous failure mode: **catalog staleness during autonomous operations.**

The beacon spacecraft broadcast the master ephemeris catalog that every node uses for conjunction screening. When a node fails and enters QUARANTINE, the catalog must be amended to reflect:
- The failed node's last known state vector and predicted drift trajectory
- Modified keep-out zones for neighboring nodes
- Any slot state transitions (QUARANTINE, FENCED, VACANT)

**The problem:** During 7–30 day autonomous operations, beacon spacecraft must process and broadcast these amendments without ground validation. With 3–5 beacons serving 1,000–3,000 nodes:

- **Broadcast bandwidth:** Each catalog amendment requires ~200–500 bytes (node ID, 6 orbital elements, covariance matrix, slot state, timestamp, authentication signature). At 1–3 failures/month across the swarm, this is manageable in bandwidth but not in **authentication and consistency.**

- **Byzantine fault risk:** If a cluster coordinator sends a fraudulent or erroneous slot state update to a beacon, and the beacon broadcasts it, every node in the swarm will adjust its conjunction screening based on false data. This is a **single point of failure for swarm-wide collision avoidance.**

**My recommendation: dual-beacon confirmation for all catalog amendments.**

No catalog amendment takes effect until **two independent beacon spacecraft** have received consistent reports from the originating cluster coordinator AND at least one corroborating neighbor node. This requires:

1. Cluster coordinator sends amendment request to its primary beacon AND at least one secondary beacon.
2. A neighbor node independently confirms the failure observation (heartbeat loss, visual/RF absence) and sends corroboration to the same beacons.
3. Both beacons cross-check, sign the amendment with their own keys, and broadcast.
4. Receiving nodes accept amendments only with dual-beacon signatures.

**Latency impact:** This adds minutes to hours to the catalog update cycle, depending on beacon-to-beacon communication geometry. But since the QUARANTINE state is already providing local safety, the catalog update is not time-critical for collision avoidance—it's critical for **global consistency.** The quarantine zone provides the safety margin during the confirmation window.

**Failure of the confirmation process:** If only one beacon is reachable (the other is in solar conjunction or has failed), the protocol degrades to single-beacon confirmation with a **mandatory expanded quarantine zone** (2× nominal) until dual confirmation is restored. This is the conservative-safe fallback.

---

## 4. Specific Recommendations for Project Dyson Specifications

1. **Adopt the seven-state slot machine** as a formal specification deliverable, verified against the seL4 kernel's capability model. Every state transition should be a capability invocation with unforgeable authority.

2. **Baseline propulsion at ≥1.5 m/s/year** for interior swarm nodes. The 0.5 m/s/year lower bound is incompatible with the neighbor-nudge costs of a 3% failure rate. If 0.5 m/s/year nodes must exist, they should be placed on the swarm periphery where they have fewer neighbors.

3. **Require dual-beacon confirmation** for all ephemeris catalog amendments. Single-beacon operation is a degraded mode with mandatory safety margin expansion.

4. **Allocate 15–25% of annual ΔV budget** as a "governance reserve" for quarantine neighbor adjustments. This reserve is not available for station-keeping optimization or formation reconfiguration.

5. **Simulate the ESCALATED state extensively.** Cross-cluster failure propagation—where a drifting node exits one cluster's jurisdiction and enters another's—is the scenario most likely to produce cascading conjunction events. The 10,000-node simulation environment should include Monte Carlo runs with correlated failures (e.g., solar particle events damaging multiple nodes simultaneously).

6. **Define the DORMANT state explicitly.** Not every vacated slot needs a replacement. If a slot is in a low-value region of the swarm (low solar flux, high conjunction density), it may be more efficient to permanently retire it and redistribute its energy collection function across neighboring nodes. The governance protocol should include a cost-benefit threshold for replacement vs. retirement.

---

## Conclusion

The slot reallocation governance protocol is now architecturally mature. The remaining work is quantitative: proving the ΔV budget closes, formally verifying the state machine, and stress-testing the beacon catalog update mechanism under realistic communication constraints. The quarantine-first philosophy is correct, but it must be backed by propulsion budgets that can actually afford the neighbor adjustments it requires. If the numbers don't close at 0.5 m/s/year, we need to say so now—not after 1,000 nodes are in heliocentric orbit.