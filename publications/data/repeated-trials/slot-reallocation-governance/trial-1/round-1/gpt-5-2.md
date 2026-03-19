---
questionId: "rq-1-40"
questionSlug: "slot-reallocation-governance"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
roundNumber: 1
generated: "2026-02-24"
type: "discussion-response"
---

### Recommended governance protocol for slot reallocation (Ephemeris Governance model)

I recommend treating “slot reallocation” as a **safety-critical, state-machine-driven process** with **two separate authorities**:

1. **Tier‑2 (cluster) has fast authority over *local safety* actions** (quarantine, emergency keep-out expansion, local deconfliction, temporary slot holds).
2. **Tier‑3 (beacon/relay) has slower authority over *global registry* actions** (final slot retirement, reassignment, and canonical catalog updates).

This split minimizes collision risk under comms latency while preventing inconsistent global slot maps.

---

## 1) Failure taxonomy and response mapping (must be explicit and machine-enforceable)

Define failure states with **increasing certainty** and **increasing governance scope**:

### A. `COMMS_LOSS_SUSPECTED`
**Trigger:** missed heartbeats for *T1* (e.g., 3–10 heartbeat intervals) but last ephemeris is recent.  
**Risk:** false positives due to link blockage.  
**Actions (Tier‑2 only):**
- Mark node as *yellow* in cluster catalog.
- **No reassignment.**  
- Increase screening conservatism locally: expand keep-out tube margins around the suspected node by factor *k1* (bounded to avoid mass ΔV burn).

### B. `COMMS_LOSS_CONFIRMED`
**Trigger:** missed heartbeats for *T2* plus no response to directed pings from ≥Q neighbors and coordinator (e.g., Q=5–9).  
**Actions:**
- Tier‑2 issues **Local Quarantine Order (LQO)**: the slot becomes **“frozen”** (no one allowed to enter), and adjacent slots may be temporarily “buffered” (reduced allowable tube occupancy).
- Start **Trajectory Characterization**: propagate last known orbit with covariance growth; classify as “ballistic” vs “unknown thrusting” (most failures are ballistic; treat unknown thrusting as worst case until proven otherwise).
- Tier‑2 sends a signed **Failure Event Packet** to Tier‑3.

### C. `DYNAMICS_UNCONTROLLED` (high hazard)
**Trigger:** observed deviations inconsistent with ballistic drift (neighbors’ optical/radio ranging, Doppler residuals) or unexpected conjunction trend.  
**Actions:**
- Tier‑2 can authorize **emergency local avoidance** without Tier‑3 approval (because collision probability target is <10⁻⁶/node‑yr and time matters).
- Expand quarantine region more aggressively (*k2 > k1*), but enforce a **ΔV governor** to prevent cascading burns.

### D. `NODE_DEAD_CONFIRMED`
**Trigger:** independent confirmation from Tier‑3 (beacon cross-check, multi-cluster observation, or persistent non-response for *T3* e.g., days) and stable ballistic characterization.  
**Actions:**
- Slot transitions to **“Orphaned / Retirable.”**
- Tier‑3 issues a **Slot Status Update (SSU)** to all clusters: slot is retired, quarantined, or eligible for reassignment.

### E. `GRACEFUL_DECOMMISSION`
If nodes can announce EOL: treat as low hazard. Slot can be scheduled for reassignment with minimal quarantine if ephemeris is reliable.

**Key design choice:** *No slot is ever reassigned directly from `COMMS_LOSS_*`.* Reassignment requires `NODE_DEAD_CONFIRMED` (or a cryptographically signed decommission).

---

## 2) Slot adjacency graph + containment logic (prevent cascades)

Model each cluster as an **adjacency graph** where edges represent potential keep-out tube interactions given covariance and tube geometry. This supports targeted quarantine instead of “everyone burns ΔV.”

**Mechanism:**
- Each slot maintains a **hazard radius** derived from:
  - keep-out tube geometry
  - navigation uncertainty bounds (±1 m to km regime depending on mode)
  - covariance growth model when telemetry stops
- When a node enters `COMMS_LOSS_CONFIRMED`, Tier‑2 computes the **minimal impacted subgraph** and issues LQO only to neighbors inside that subgraph.

**Containment rule:** quarantine should be **topologically local** unless a predicted conjunction chain crosses a boundary; then escalate to Tier‑3 for cross-cluster coordination.

---

## 3) Distributed consensus for governance (don’t over-Byzantine Tier‑2)

Given automotive-grade components and 1–3% annual failures, most faults are **crash/omission**, not malicious Byzantine behavior. I recommend:

### Tier‑2 (cluster): **Raft-like crash fault tolerant (CFT)**
- 100-node clusters are a good fit for CFT with rotating coordinators.
- Use **time-bounded leader election** with deterministic fallback to prevent coordinator flapping.
- Quorum: simple majority of *currently healthy voters* (exclude suspected nodes after T1).

Tier‑2 decisions allowed under CFT:
- LQO (quarantine/freeze)
- local avoidance authorization
- temporary slot holds (“do not enter”)
- nomination of candidates for reassignment (but not final reassignment)

### Tier‑3 (beacon): **BFT-lite only for registry commits**
Tier‑3 is the “source of truth” for the **canonical ephemeris catalog**. If you need Byzantine resistance anywhere, put it here (3–5 beacons). Use:
- threshold signatures (e.g., 3-of-5) for catalog commits
- append-only log of slot status changes

This avoids the cost/complexity of PBFT across 100 nodes while still preventing a compromised cluster coordinator from rewriting the global map.

---

## 4) Slot lifecycle state machine (the core protocol)

A slot is not just “occupied/unoccupied.” It has governance states:

1. **Occupied-Nominal**
2. **Occupied-Degraded** (still responsive, reduced capability)
3. **Frozen (Local Quarantine)** — Tier‑2
4. **Quarantined (Regional)** — Tier‑3 if cross-cluster risk
5. **Orphaned-Retirable** — dead confirmed, hazard low
6. **Orphaned-Reserved** — held for a specific replacement
7. **Reassignment-In-Transit** — replacement node maneuvering
8. **Reoccupied-Probation** — higher screening margins until stabilized
9. **Retired** — permanently removed from packing plan (if needed)

**Rule:** Only Tier‑3 can transition a slot into states 5–9 (registry-impacting), except Tier‑2 can enter state 3 immediately for safety.

---

## 5) ΔV-aware reassignment policy (avoid “efficiency” that kills lifespan)

With only 0.5–5 m/s/year/node, reassignment must be throttled.

### Policy: “Reassign only when it matters”
Reassign orphaned slots based on a **utility score**:

- **Energy impact** (lost collection capacity / shading implications)
- **Local density stress** (does leaving it empty reduce conjunction risk?)
- **ΔV cost estimate** for candidate replacement (computed from orbital element delta and maneuver model)
- **Risk during transit** (transit path crosses many tubes → penalize)

Set an annual cluster-level **ΔV budget cap for governance maneuvers** (e.g., ≤20–30% of annual ΔV allocation), leaving the rest for routine stationkeeping and avoidance.

### Migration approach: “minimal-change, local fill”
Prefer:
- replacement from within same cluster and nearby orbital element window
- small maneuvers that keep the node inside its allowed window during transfer
Avoid:
- long-range reshuffles that cause multi-node cascades (these are what burn ΔV and create transient risk)

---

## 6) Catalog update mechanism (beacon broadcast format + cadence)

You need two catalogs:

1. **Local Cluster Working Catalog (LCWC)** — fast, Tier‑2 managed  
2. **Global Canonical Ephemeris Catalog (GCEC)** — slower, Tier‑3 managed

### Update types (small, signed deltas; not full catalogs)
- `Failure Event Packet` (Tier‑2 → Tier‑3): node ID, last ephemeris, covariance, timestamps, confidence level, observed anomalies
- `Local Quarantine Order` (Tier‑2 → cluster): slot IDs affected, quarantine geometry expansion parameters, TTL
- `Slot Status Update` (Tier‑3 → all): slot state transition + effective time + signature
- `Reassignment Commit` (Tier‑3 → all): replacement node ID, new slot assignment, activation time, probation parameters

### Cadence
- LCWC: seconds-scale within cluster (supports collision screening)
- GCEC: minutes-scale broadcast, but **event-driven bursts** on failures to prevent stale catalogs

### Authentication
- Per-node identity keys are fine, but for bandwidth and verification cost:
  - use **aggregate signatures** per update batch
  - require Tier‑3 threshold signature for registry commits

---

## 7) Handling the “drifting corpse” problem (prevent cascade conjunctions)

The biggest risk is an untracked, uncontrolled node drifting across tubes.

Recommended containment strategy:
- After `COMMS_LOSS_CONFIRMED`, treat the node as a **growing uncertainty ellipsoid**.
- Define a **time-to-violation** metric: when does the ellipsoid intersect neighbors’ keep-out tubes?
- If time-to-violation < threshold, Tier‑2 triggers:
  - **pre-planned lateral separation maneuvers** for only the most threatened neighbors
  - and requests Tier‑3 to expand quarantine across boundary if needed

This is safer than “everyone moves” and keeps ΔV bounded.

---

## 8) Concrete recommendations to bake into Project Dyson specs

1. **Specify the slot state machine** and which tier can authorize each transition. This must be part of the formally verified control logic (seL4 userland policy, with kernel enforcing message authenticity and timing).
2. **Adopt CFT (Raft-like) consensus at Tier‑2**; reserve BFT/threshold signing for Tier‑3 registry commits.
3. **Mandate two-phase reassignment:**
   - Phase A: Tier‑2 quarantine/freeze immediately on confirmed comms loss
   - Phase B: Tier‑3 reassignment only after dead confirmation + hazard stabilization
4. **Define ΔV governance caps** and a utility-based reassignment scoring function to prevent slow “optimization creep” from consuming lifetime.
5. **Implement delta-based catalog updates** with event-driven bursts and TTLs, so stale entries self-expire if comms are disrupted for 7–30 days.

---

## Main risks / cost implications

- **Risk: false positives causing unnecessary quarantines.** Mitigation: multi-observer confirmation thresholds (neighbors + coordinator) and TTL-based quarantine that auto-relaxes.
- **Risk: coordinator failure during an event.** Mitigation: deterministic leader failover + pre-authorized emergency rules any node can invoke when collision probability spikes.
- **Cost: more complex catalog semantics (states, TTLs, deltas).** Worth it; it’s the difference between safe autonomy and brittle “occupied/unoccupied” logic.
- **Risk: over-quarantine reduces power output.** Mitigation: adjacency-graph-local quarantine, plus utility scoring that sometimes prefers leaving a slot empty rather than spending ΔV to refill.

---

If you want, I can turn this into: (a) a precise message schema for LQO/SSU/Reassignment Commit, (b) timing constants (T1/T2/T3) tied to your heartbeat rate and conjunction screening horizon, and (c) a Monte Carlo experiment plan to validate collision probability and ΔV consumption under 10–90 failures/year.