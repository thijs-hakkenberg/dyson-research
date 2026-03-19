---
questionId: "rq-1-40"
questionSlug: "slot-reallocation-governance"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
roundNumber: 1
generated: "2026-02-24"
type: "discussion-response"
---

### Recommended governance protocol for slot reallocation (Phase 1: 1,000–3,000 nodes; clusters ~100; 3–5 beacons)

I recommend treating slot reallocation as a **safety-critical state machine** whose primary goal is to preserve the **collision probability < 10⁻⁶ per node-year** under **1–3% annual failure**, while staying inside the **0.5–5 m/s/year ΔV** envelope and operating **7–30+ days autonomously**. The key design choice: **separate “safety authority” from “capacity optimization.”** Safety actions must be fast and local; optimization can be slower and beacon-mediated.

---

## 1) Failure classification taxonomy (what to do depends on what failed)

Define four operationally meaningful failure classes with explicit detection signatures and actions:

**F0 — Planned/Graceful Exit (cooperative)**
- Signature: authenticated “intent-to-deactivate” + last known ephemeris + health OK.
- Action: immediate slot release (no quarantine needed), catalog update.

**F1 — Comms Loss / Unconfirmed Failure (possibly healthy)**
- Signature: missed heartbeats but still present in passive ranging/optical or last ephemeris consistent.
- Action: *do not reassign slot yet.* Enter **Soft Quarantine** (below). Attempt re-contact and independent tracking.

**F2 — Confirmed Non-Cooperative (dead or attitude/prop fault)**
- Signature: N missed heartbeats + no authenticated response + kinematic inconsistency + no commanded maneuvers.
- Action: **Hard Quarantine** around predicted trajectory envelope; begin conjunction-driven neighbor protections; slot is *not* immediately reusable.

**F3 — Malicious/Byzantine (rare but must be bounded)**
- Signature: inconsistent signed messages, impossible ephemerides, replay, key compromise indicators.
- Action: isolate from consensus, treat as F2 for physical safety; revoke credentials at beacon tier.

**Why this taxonomy matters:** it prevents the most dangerous governance failure mode—**premature reassignment after transient comms loss**—while still allowing fast safety containment for true non-cooperative drift.

---

## 2) Slot adjacency graph + “quarantine tubes” as the core abstraction

Model each cluster as a graph:

- **Vertices:** slots (orbital element windows + keep-out tubes).
- **Edges:** adjacency/conflict relations (two slots whose keep-out tubes can be violated under expected navigation error + differential drift + maneuver uncertainty).

Maintain two safety envelopes per slot:
1. **Nominal Keep-Out Tube (KOT):** the normal collision-avoidance constraint.
2. **Quarantine Tube (QT):** an expanded envelope used when a neighbor is F1/F2. QT size is driven by:
   - navigation uncertainty growth without updates,
   - worst-case passive drift rates,
   - time to beacon catalog convergence,
   - and acceptable risk (targeting <10⁻⁶/node-year).

**Operational rule:** slot reallocation is allowed only when the candidate slot and its neighbors are not under QT constraints that would violate minimum separation.

This graph structure also supports identifying **critical slots** (high degree / centrality) whose failure causes disproportionate quarantines—those should get:
- higher-quality components,
- more frequent tracking,
- or larger nominal windows to reduce cascade risk.

---

## 3) Authority hierarchy: local safety, global consistency

### Tier-2 (cluster coordinator) authority — **fast safety actions**
Cluster coordinators should have unilateral authority to:
- declare **Soft Quarantine** for F1 quickly,
- declare **Hard Quarantine** for F2 when local evidence passes thresholds,
- command **local collision-avoidance maneuvers** for cooperative neighbors,
- publish **provisional catalog deltas** for the cluster.

This is necessary because waiting for Tier-3 beacon approval injects latency into the only thing that must be real-time: preventing conjunction cascades.

### Tier-3 (beacon/relay) authority — **global catalog finalization + reallocation rights**
Beacons should:
- merge cluster deltas into the **master ephemeris catalog**,
- arbitrate cross-cluster conflicts,
- issue **final slot status** (Active / SoftQ / HardQ / Released / Reassigned),
- and authorize **slot reassignment** (capacity optimization) once safe.

**Key point:** coordinators can *contain* risk; beacons can *reclaim* capacity.

This division also aligns with autonomy constraints: clusters can operate independently for 7–30 days, while beacons provide eventual consistency when connectivity allows.

---

## 4) Consensus protocol choice: don’t over-Byzantine the physical layer

Within a ~100-node cluster, I recommend **Raft-style crash fault tolerance** for routine governance, with a thin Byzantine detection layer for message authentication and misbehavior flagging.

- **Why not PBFT everywhere:** it’s expensive (message complexity, timing assumptions) and the dominant failure mode is *crash/non-cooperative drift*, not adversarial behavior.
- **What you do need:** strong crypto identity, signed ephemeris updates, replay protection, and a way to quarantine nodes that send inconsistent state.

**Quorums:**
- **Soft Quarantine (F1):** coordinator + ≥2 independent witnesses (e.g., missed heartbeats + passive tracking inconsistency).
- **Hard Quarantine (F2):** coordinator + ≥(N/3) witnesses *or* coordinator + beacon corroboration when available.
- **Slot Release/Reassign:** beacon-signed finalization (or multi-beacon threshold signature if you truly have 3–5 beacons and want redundancy).

This gives you fast local action without making the whole swarm hostage to BFT overhead.

---

## 5) The actual protocol: state machine and timers

### States for each slot
**ACTIVE → SUSPECT(F1) → SOFT_QUARANTINE → HARD_QUARANTINE → RELEASED → REASSIGNED**

### Key timers (tunable; pick conservative defaults early)
- **Heartbeat interval:** seconds to tens of seconds (not ms; your ≤10 ms is time sync, not health telemetry).
- **Suspect trigger:** e.g., 3 missed heartbeats.
- **F1 confirmation window:** e.g., 30–120 minutes of attempted reacquisition + passive tracking.
- **Hard quarantine trigger:** confirmed non-cooperative + predicted QT intersects any neighbor KOT within a lookahead horizon.

### Actions by state
**SUSPECT / SOFT_Q**
- Freeze reassignment.
- Expand local safety buffers (QT).
- Increase tracking duty cycle for neighbors.
- Coordinator publishes “provisional risk bulletin” to beacon and adjacent clusters.

**HARD_Q**
- Coordinator computes predicted drift envelope (with uncertainty growth).
- Neighbors may execute minimal-ΔV separation maneuvers only if conjunction probability exceeds threshold.
- Beacon marks slot “non-reusable” until conditions met.

**RELEASED**
- Only allowed when either:
  1) failed node is confirmed to be passivated in a stable non-intersecting orbit, or
  2) drift envelope no longer intersects any operational volume for a defined horizon.

**REASSIGNED**
- Beacon assigns a candidate replacement based on ΔV cost and local density constraints.

---

## 6) ΔV-aware reassignment: minimize migrations, prefer “absorption,” use auctions sparingly

Given only **0.5–5 m/s/year**, the governance protocol must treat reassignment as a scarce resource.

I recommend this priority order:

1. **Do nothing (absorb):** leave the slot empty if power loss is tolerable and density risk is reduced by the gap.
2. **Local swap:** choose a replacement already near the slot in orbital element space (min ΔV).
3. **Slow drift fill:** if natural differential drift can move a node into the slot with minimal thrust, schedule it over weeks/months.
4. **Active transfer:** only if the slot is high-value (e.g., critical geometry for power beaming or comms topology).

Mechanism: a simple **ΔV-bounded bidding** inside the cluster:
- nodes compute estimated ΔV to occupy slot within allowed windows,
- coordinator selects best candidate subject to keeping overall cluster ΔV under budget,
- beacon finalizes to avoid cross-cluster surprises.

Avoid continuous reshuffling—optimize for **stability**, not perfect packing.

---

## 7) Beacon catalog update mechanism: “delta-first, signed, versioned, eventually consistent”

The ephemeris catalog should be treated like a distributed database:

- **Base snapshot** (periodic full broadcast)
- **Signed deltas** (frequent)
- **Monotonic version numbers** per cluster and per beacon
- **Time validity intervals** (so stale data can be rejected deterministically)

Minimum fields in a delta:
- slot ID
- node ID (or null if orphaned)
- slot state (Active/SoftQ/HardQ/Released/Reassigned)
- predicted ephemeris (mean + covariance or bounded envelope)
- validity start/stop
- signature (coordinator and/or beacon)

Cadence:
- **Cluster → beacon:** event-driven + periodic (e.g., every few minutes)
- **Beacon → swarm:** periodic (e.g., 1–10 minutes) plus immediate broadcast on HardQ events

This directly addresses the “stale catalog” risk that undermines the 10⁻⁶ requirement.

---

## 8) Risk factors and cost/feasibility notes

**Biggest technical risk:** QT sizing and uncertainty propagation. If you under-model uncertainty growth for dead nodes, you’ll get surprise conjunctions; if you over-model, you’ll quarantine too much capacity. This is where Monte Carlo in the 10,000+ node sim environment pays off.

**Biggest governance risk:** coordinator failure during an event. Mitigation:
- rotating coordinator is fine, but require **hot-standby** and **state replication** (Raft log) so quarantine state survives leadership change.

**Biggest operational cost driver:** excessive avoidance maneuvers due to slow classification. Mitigation:
- invest in passive tracking (inter-sat ranging, optical angles) so F1→F2 decisions are evidence-based without ground.

---

## 9) What I would prototype first (highest leverage)

1. **State machine + signed delta catalog** (end-to-end in sim).
2. **Adjacency graph + QT rules** with Monte Carlo calibration to hit <10⁻⁶/node-year.
3. **ΔV-bounded reassignment selection** (absorb vs fill vs transfer).
4. **Coordinator failover under stress** (simulated comms partitions + multiple simultaneous F2 events).

---

### Bottom line recommendation
Adopt a **two-speed governance model**: **cluster coordinators act immediately for safety via quarantine and local avoidance**, while **beacons finalize catalog consistency and authorize reassignment** once the failed node’s drift envelope is bounded. Implement slot governance as a **versioned, signed, delta-based ephemeris database**, and make reassignment explicitly **ΔV-budgeted** to prevent slow “optimization churn” from consuming propulsion margins over a 50-year life.