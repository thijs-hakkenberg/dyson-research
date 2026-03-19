---
questionId: "rq-1-40"
questionSlug: "slot-reallocation-governance"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
roundNumber: 1
generated: "2026-02-07"
type: "discussion-response"
---

### Recommended slot reallocation governance protocol (autonomous, safety-first, ΔV-aware)

The governance problem is fundamentally a **state-management and authority** problem under uncertainty: you need to (1) classify the “missing” node, (2) prevent its potential drift from causing conjunction cascades, (3) update the ephemeris catalog fast enough to preserve the <10⁻⁶/node-year requirement, and (4) reassign capacity without burning the limited 0.5–5 m/s/year ΔV budget. The protocol below is designed to be implementable in the 3-tier architecture (node / ~100-node cluster / 3–5 beacons), and to work for 7–30+ days without ground.

---

## 1) Failure taxonomy and state machine (what we govern)

Use a **small, formally verifiable state machine** with explicit timers and evidence thresholds. Every slot (not just every node) has a state.

### Slot states
1. **NOMINAL (occupied, healthy)**
2. **SUSPECT (node missing/abnormal, not yet declared failed)**
3. **QUARANTINED (keep-out expanded; no reassignment allowed)**
4. **ORPHANED (declared unoccupied; eligible for reassignment)**
5. **MIGRATING (a replacement is en route; temporary constraints apply)**
6. **REASSIGNED (new node committed; catalog updated)**

### Failure classes (node-level) mapped to slot actions
- **Graceful shutdown / announced decommission**: immediate transition to ORPHANED after last confirmed ephemeris + passivation confirmation; minimal quarantine.
- **Comms loss (likely alive)**: SUSPECT → QUARANTINED; do *not* reassign until evidence supports failure.
- **Attitude/power degradation (telemetry indicates loss of control)**: immediate QUARANTINED with expanded tube; reassignment delayed.
- **Catastrophic failure (sudden silence + last state indicates risk)**: QUARANTINED quickly; possible *local avoidance* by neighbors.
- **Byzantine/malicious behavior (inconsistent ephemeris, invalid signatures)**: treat as hazardous; QUARANTINED + neighbor avoidance; exclude from quorum.

This is the minimum taxonomy that prevents premature reassignment while still enabling fast containment.

---

## 2) Detection and confirmation thresholds (avoid false positives)

### Heartbeat + ephemeris freshness rules
- Each node emits a signed **heartbeat** at a fixed cadence (e.g., 1–10 minutes) including:
  - time (≤10 ms synced)
  - current state vector / orbital element estimate + covariance
  - propulsion/attitude health bits
  - “intent” (planned maneuvers, if any) for the next window
- Cluster coordinator maintains a **freshness score** for each slot:
  - `Fresh` if last valid heartbeat < T_fresh
  - `Stale` if between T_fresh and T_suspect
  - `Suspect` if > T_suspect

### Suggested timers (tunable by ops concept)
- `T_fresh`: 2–3 heartbeat intervals
- `T_suspect`: 6–12 heartbeat intervals (hours-scale if cadence is minutes)
- `T_fail_confirm`: require **multi-source evidence**, not just silence:
  - missed heartbeats **plus**
  - no crosslink ranging response **plus**
  - no optical/radio occultation signature (if available) **or**
  - neighbors’ passive observations inconsistent with expected track

**Key rule:** *Slot reassignment is never triggered by a single failure detector.* It requires a quorum decision (below) and a **hazard assessment** (drift envelope vs. neighbors).

---

## 3) Authority hierarchy and decision rights (who can do what)

You need fast local action without allowing inconsistent global catalogs. The clean split:

### Tier 2 (cluster coordinator) authority — “local safety + provisional governance”
The cluster coordinator can autonomously:
- declare **SUSPECT** and **QUARANTINED**
- command **local collision-avoidance** within cluster policy limits
- issue **provisional catalog deltas** for the cluster (“soft updates”)
- allocate a **replacement candidate** and start MIGRATING *within the cluster*, but only as “provisional” until beacon commit

### Tier 3 (beacons/relays) authority — “global commit and cross-cluster consistency”
Beacons:
- maintain the **master ephemeris catalog**
- arbitrate **cross-cluster** boundary conflicts
- issue **committed slot reassignment certificates** (hard updates)
- coordinate catalog update cadence and revocation lists (Byzantine / key compromise)

This division is critical: it keeps response latency low (Tier 2) while preventing divergent truth across the swarm (Tier 3).

---

## 4) The governance protocol: 3-phase reallocation (contain → characterize → reclaim)

### Phase A — Contain (minutes to hours)
Triggered when node enters SUSPECT.

1. **Expand keep-out tube** around the SUSPECT slot by a hazard factor based on:
   - last covariance
   - expected uncontrolled drift rates
   - SRP sensitivity / attitude state
2. Neighbors adopt a **local “no-approach” constraint** (soft avoidance) that biases station-keeping away from the expanded tube with minimal ΔV.
3. Coordinator publishes a **Cluster Hazard Bulletin (CHB)**: signed message containing
   - slot ID, last known ephemeris, covariance
   - quarantine radius/timebox
   - confidence level and evidence summary
4. Beacon receives CHB and rebroadcasts it swarm-wide on next cadence.

**Goal:** Stop cascades by making everyone treat the slot as potentially occupied and unpredictable.

### Phase B — Characterize (hours to days)
Coordinator and beacon attempt to determine whether the object is:
- still controlled but comms-impaired
- uncontrolled but trackable
- gone (deorbited, shattered, or dead but stable)

Actions:
- solicit **passive tracking** from nearby nodes (angles-only, RF signal strength, opportunistic ranging)
- fit an updated trajectory and expand/contract covariance
- if evidence indicates uncontrolled drift that may cross adjacent tubes, pre-authorize **micro-avoidance** budgets for affected neighbors (bounded burn policy)

Output: **Hazard Envelope Estimate (HEE)** with a time-evolving keep-out region.

### Phase C — Reclaim (days to weeks)
Only after quarantine conditions are satisfied.

A slot becomes **ORPHANED** (eligible for reassignment) when:
- either the node is confirmed non-existent / inert and its predicted path stays outside the slot volume for a defined clearance window, **or**
- the object is confirmed to have drifted into a designated **graveyard corridor** (predefined in ephemeris governance), **or**
- the slot is redefined (absorbed/merged) by governance decision.

Then:
1. Coordinator proposes a **Reassignment Plan (RP)**:
   - candidate replacement node(s)
   - ΔV estimate and time-to-slot
   - interim constraints during MIGRATING
2. Beacon runs **global conflict check** (cross-cluster adjacency graph + catalog).
3. Beacon issues a **Slot Reassignment Certificate (SRC)**:
   - new slot owner identity key
   - effective time
   - updated keep-out tube parameters
   - revocation of prior owner (if any)
4. Catalog delta is broadcast; nodes update local conjunction screening.

**Key property:** Tier 2 can start migration early, but **ownership only flips on beacon commit** to prevent split-brain.

---

## 5) Distributed consensus choice (pragmatic, not academic)

For ~100-node clusters, a full PBFT-style protocol is heavy and failure-prone under intermittent links. My recommendation:

### Intra-cluster: Raft-like coordinator + witness quorum
- Use a rotating coordinator, but treat it as **leader** for fixed epochs.
- Decisions (QUARANTINE, ORPHAN, MIGRATION PROPOSAL) require:
  - leader signature **plus**
  - `k-of-n` witness signatures from a designated “safety committee” subset (e.g., 7–15 nodes chosen deterministically per epoch)
- This is not full Byzantine tolerance, but it’s robust to benign failure and limits single-node bad decisions.

### Beacon-level: Byzantine-resilient commit among 3–5 beacons
With only 3–5 beacons, you *can* do BFT properly:
- 3 beacons: tolerate 1 fault only with strong assumptions; better to have 5 for practical BFT margins.
- Use a lightweight BFT commit for SRC issuance and catalog deltas.

**Why this split works:** most events are local; global commits are rarer but must be authoritative.

---

## 6) Slot adjacency graphs and “blast radius” control

Model the swarm as a **graph of slot adjacency** (edges = potential conjunction coupling given covariance + drift). Use it operationally:

- When a slot is QUARANTINED, automatically compute its **impact set**: nodes whose keep-out tubes intersect the hazard envelope within horizon H (e.g., 7–30 days).
- Apply graduated responses:
  1. **Bias-only station-keeping** (near-zero ΔV)
  2. **Micro-avoidance** within strict per-month ΔV caps
  3. **Temporary local density reduction** (widen windows) if risk rises

This prevents “everyone maneuvers” cascades.

---

## 7) ΔV-aware reassignment policy (capacity recovery without budget blowout)

Given 0.5–5 m/s/year, reassignment must be **rate-limited** and **batched**.

Policies:
- **Do not immediately refill every orphan.** Maintain a target **spare capacity margin** (e.g., 1–3%) so power loss doesn’t force high-ΔV reshuffles.
- Prefer **nearest-neighbor replacements** in orbital element space (minimize plane/phase changes).
- Use **opportunistic drift**: allow natural differential drift to do most of the phase adjustment; reserve ΔV for trimming.
- Enforce a **cluster ΔV ledger**:
  - each node has annual ΔV budget
  - cluster has an aggregate “reallocation budget”
  - coordinator cannot approve migrations that exceed remaining budget without beacon override

---

## 8) Beacon catalog update mechanism (staleness is a safety hazard)

Catalog updates must be small, frequent, authenticated, and resilient to delay.

### Data model
- Baseline catalog + **signed deltas**:
  - slot state changes (NOMINAL→QUARANTINED→ORPHANED→REASSIGNED)
  - ephemeris updates + covariance bounds
  - certificates (SRC) and revocations

### Cadence
- **Regular cadence** (e.g., every 5–30 minutes) plus **event-driven priority bursts** for QUARANTINE/SRC.
- Nodes keep operating safely if they miss updates by using:
  - conservative growth of covariance with time
  - default “treat stale as occupied” rule

### Security
- Per-node identity keys for heartbeats and intents.
- Beacon signs SRCs; coordinators sign CHBs/RPs.
- Maintain a revocation mechanism for compromised nodes/coordinators.

---

## 9) What I would simulate first (to de-risk Phase 1)

In the 10,000+ node simulation environment, prioritize:
1. **False positive comms loss** scenarios: show that quarantine doesn’t cause ΔV cascades.
2. **Uncontrolled drift crossing adjacency**: validate hazard envelope sizing and impact set responses.
3. **Simultaneous multi-failure** (10–90/year scaled): ensure catalog staleness doesn’t violate <10⁻⁶/node-year.
4. **Beacon partition / delayed commit**: prove provisional vs committed governance prevents split-brain slot ownership.

Success metric: collision probability stays below threshold with ΔV expenditure within annual budgets and with bounded time-to-reclaim orphan capacity.

---

## Bottom line recommendations
- Make **QUARANTINE the default fast action**, and **REASSIGNMENT a slower, certificate-based action**.
- Give **Tier 2 authority for immediate safety** and **Tier 3 authority for global truth**.
- Use **witness-quorum local decisions** + **BFT beacon commits** rather than trying to run PBFT everywhere.
- Treat ephemeris governance as a **slot-state ledger** with signed deltas, not just a trajectory catalog.
- Enforce **ΔV ledgers and batching**, otherwise reallocation becomes the dominant propellant sink.

If you want, I can propose concrete parameter values (heartbeat cadence, quorum sizes, quarantine growth laws) and a minimal message schema for CHB/RP/SRC suitable for formal verification on seL4.