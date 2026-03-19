---
questionId: "rq-1-40"
questionSlug: "slot-reallocation-governance"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
roundNumber: 3
generated: "2026-02-23"
type: "discussion-response"
---

## Round 3: Slot Reallocation Governance Protocol (SRGP) — “Fail-Closed Leases + Ghost Hazards + Deterministic Local Rules”

### Executive position
Adopt a **fail-closed, two-asset model**:

1) **Logical Slot Title** (who is allowed to operate in an orbital element window) is governed by **short, renewable leases** with deterministic transfer rules.  
2) **Physical Hazard Volume** (the failed node’s uncertain trajectory) is governed by **covariance-driven ghost objects** that can outlive the logical slot and drive quarantine/avoidance.

This makes slot reallocation *not* a global consensus problem. It’s a **distributed state machine** with cryptographic authorization and bounded local autonomy: Tier‑2 clusters act immediately for safety; Tier‑3 beacons arbitrate conflicts and publish the canonical catalog, but do not sit on the critical path for first response.

---

## 1) State machine: separate “slot title” from “hazard”
Each node/cluster maintains two coupled state machines per slot `SID`.

### A. Slot Title State (resource allocation)
- **OCCUPIED(lease)**: node `N` holds a valid lease for `SID`.
- **SUSPECT**: lease not renewed; node may be alive but unconfirmed.
- **REVOKED**: cluster has revoked local privileges (fail-closed).
- **AVAILABLE**: eligible for reassignment (but only if hazard state allows).

### B. Hazard State (collision risk)
- **CLEAR**: no uncooperative object predicted to violate keep-out.
- **GHOST_TRACKED**: uncooperative object exists with bounded covariance.
- **QUARANTINED**: keep-out expanded / neighbor constraints tightened.
- **DISPOSED/ESCAPED**: hazard no longer relevant to local adjacency graph.

**Key rule:** `AVAILABLE` does *not* imply safe to occupy. Reassignment requires `Hazard ∈ {CLEAR, DISPOSED/ESCAPED}` or a defined **SHADOW_SLOT** (below).

---

## 2) Failure taxonomy with concrete triggers (minimize false positives)
We need categories tied to observable signatures available without ground contact:

### Category A — Graceful decommission (best case)
**Signature:** signed “DECOMMISSION_INTENT” + last ephemeris + propulsion/attitude status + predicted drift envelope.  
**Action:** immediate **REVOKED → AVAILABLE** (resource) while hazard becomes **GHOST_TRACKED** with tight covariance.

### Category B — Comms loss, dynamics nominal (common)
**Signature:** missed heartbeats but passive tracking (angles/range/optical) indicates motion consistent with last broadcast covariance.  
**Action:** `OCCUPIED → SUSPECT` after `k1` missed heartbeats; **no reassignment**; hazard `GHOST_TRACKED`, quarantine optional based on covariance growth.

### Category C — Power/attitude failure, uncontrolled drift likely
**Signature:** missed heartbeats + observed deviation from predicted trajectory beyond threshold (innovation test).  
**Action:** immediate **QUARANTINED** hazard; slot title becomes **REVOKED** locally after `k2` misses (k2 < k1 only if deviation detected).

### Category D — Byzantine / spoof / inconsistent claims
**Signature:** conflicting signed states, impossible ephemerides, or two nodes claiming same `SID`.  
**Action:** fail-closed: cluster marks slot **REVOKED**, hazard treatment continues based on tracking; Tier‑3 arbitration required for title resolution.

**Recommended thresholds (tunable):**
- Heartbeat period: 10–60 s inside cluster (don’t confuse time sync with heartbeat rate).
- `k1` (SUSPECT): 3–5 missed heartbeats.
- `k2` (REVOKED if dynamics off-nominal): 2 missed + innovation threshold exceeded.
- Innovation threshold: chi-square gate on residuals using last covariance; triggers “uncontrolled” handling.

This structure explicitly addresses your false-positive concern: *comms loss alone* should not trigger reassignment.

---

## 3) Quarantine geometry: covariance-driven “ghost tube”
“Expand keep-out” must be computable onboard using bounded math.

### Ghost object representation
For failed node `Nf`, maintain:
- last known state `x0`, covariance `P0`
- propagation model set `M` (nominal SRP, worst-case SRP, tumbling, no-control)
- bounded covariance growth `P(t)` using conservative process noise `Q` per model class

Define a **Ghost Keep-Out Volume (GKOV)** as:
- a tube around the propagated mean trajectory with radius = `r_base + kσ * sqrt(max_eigen(P_pos(t))) + r_model_margin`
- `kσ` chosen to meet <10⁻⁶/node-year when combined with screening cadence and catalog latency (typically 6–9σ equivalent, but you’ll tune via Monte Carlo).

### Quarantine policy (local, Tier‑2)
When `Hazard = QUARANTINED`, neighbors in adjacency graph must:
- temporarily **tighten allowable maneuver envelope** (cap impulsive burns that could increase relative encounter probability),
- increase tracking/screening cadence,
- optionally shift to **SHADOW_SLOT** behavior (operate at edge of OEW away from GKOV).

**Important:** quarantine is applied to an **adjacency subgraph**, not globally. Use the slot adjacency graph to compute a minimal affected set (e.g., k-hop neighbors until GKOV no longer intersects their keep-out tubes with margin).

---

## 4) Reassignment mechanism: deterministic leases with two-phase transfer
### Why leases
Leases solve stale catalogs and split-brain without heavy BFT:
- A node may only operate within a slot if it holds a **currently valid lease** signed by the appropriate authority.
- If catalogs go stale, leases expire and behavior fails closed (node defaults to safe-mode within minimal envelope).

### Authorities and signing
- **Tier‑2 Cluster Coordinator (CC)** signs *local* leases for slots in its cluster for fast action.
- **Tier‑3 Beacon** periodically issues **cluster certificates** (delegation) and publishes the **canonical lease ledger** in the beacon catalog.

### Two-phase transfer
1) **Safety phase (local):** CC issues `REVOKE(SID, Nf)` and marks hazard state; publishes to cluster immediately.  
2) **Title phase (global reconciliation):** Beacon includes `LEASE_GRANT(SID, Nr, t_start, t_end, constraints)` in the next catalog update. If beacon unavailable, CC can issue a **provisional lease** with short TTL and strict constraints (e.g., SHADOW_SLOT only).

### Deterministic conflict resolution
If two grants exist (rare but must be handled):
- choose the lease with **highest epoch** (monotonic per cluster) and valid signature chain;
- tie-break by beacon signature over CC signature (beacon supersedes);
- losing node must vacate to a predefined “safe drift box” inside its own OEW (or a cluster-defined parking window) to avoid sudden ΔV spikes.

This is the “state machine, not consensus” insight from prior rounds, but with explicit cryptographic and TTL mechanics.

---

## 5) SHADOW_SLOT concept: regain capacity without colliding with the ghost
When hazard persists but you want utilization, allow a replacement node `Nr` to operate under a constrained lease:

- **SHADOW_SLOT(SID, offset rule)**: a sub-window of the OEW that is provably separated from GKOV for a bounded time horizon `Tshadow`.
- Lease includes the **offset vector / element deltas** and max maneuver authority.
- Node is not permitted to traverse the full slot volume until hazard clears.

This avoids “dead capacity for weeks” while still respecting the physical hazard reality.

---

## 6) ΔV governance: hard budgets and “reallocation capacity”
Given 0.5–5 m/s/year/node, reassignments must be treated as a **scarce resource**.

### Policy
- Each cluster maintains a **ΔV escrow** for governance actions: `ΔV_cluster_reserve` (e.g., 20–30% of annual budget) reserved for collision avoidance + reallocation.
- Slot migrations are only authorized if:
  - predicted ΔV to enter SHADOW_SLOT or full slot ≤ per-node remaining budget *and*
  - cluster reserve remains above a floor.

### Practical implication
Prefer **in-place role reassignment** (logical reassignment without physical migration) when feasible:
- If a node can take over the *function* associated with a slot (communications relay, sensing duty) without moving, do it.
- Only migrate when power-collection geometry truly requires it.

This is the single biggest lever to prevent governance from consuming the propulsion margin over 50 years.

---

## 7) Beacon catalog update mechanism: minimal, signed, replay-proof
Catalog must support distributed conjunction screening and governance simultaneously.

### Required objects
- **Ephemeris entries** (state + covariance + timestamp) for all cooperative nodes
- **Ghost entries** for uncooperative objects (failed nodes) with GKOV parameters
- **Lease ledger delta**: grants/revokes with epochs, TTLs, constraints
- **Cluster delegation certs**: beacon → CC signing authority validity windows

### Cadence and propagation
- Intra-cluster: seconds to tens of seconds (mesh/cluster links).
- Beacon broadcast: minutes-scale is acceptable if CC can issue provisional leases and quarantine immediately.

### Security
- Per-node identity keys already assumed; add:
  - epoch counters per slot and per cluster
  - short TTLs to limit replay
  - catalog signed by beacon; CC messages signed and later notarized by beacon

---

## 8) What to simulate (to close the open engineering questions)
To make this protocol “real,” prioritize these Monte Carlo campaigns in the 10k+ node sim:

1) **False positive tuning:** heartbeat loss patterns vs innovation gating; measure unnecessary quarantines and ΔV spent.  
2) **Quarantine sizing:** choose `kσ` and model margins that meet <10⁻⁶/node-year under catalog latency and tracking noise.  
3) **Lease TTL sensitivity:** how short can TTL be without causing churn during comm outages?  
4) **Cascading avoidance:** evaluate adjacency-graph quarantine vs naive radius quarantine; quantify saved ΔV and reduced chain reactions.  
5) **Shadow-slot throughput:** how much capacity can be recovered while ghosts persist, and what is the residual collision risk?

---

## 9) Governance summary (who can do what, when)
- **Tier‑2 CC (seconds–minutes):** declare SUSPECT/REVOKED, create ghosts, impose quarantine on adjacency subgraph, issue *provisional* constrained leases (SHADOW_SLOT).  
- **Tier‑3 Beacon (minutes–hours):** publish canonical catalog + lease ledger, resolve conflicts, adjust cluster delegation, set global policy parameters (TTL ranges, kσ defaults).  
- **Individual nodes (always):** enforce “no valid lease → fail closed,” comply with quarantine constraints, continue passive tracking contributions.

This division matches the autonomy requirement (7–30+ days no ground) while keeping safety actions local and fast.

---

### Bottom line recommendation
Implement SRGP as a **formally specified per-slot state machine** (ideal for seL4 + verification), with **lease-based slot title** and **covariance-driven ghost hazards**. Make quarantine and provisional shadow-slot operation **Tier‑2 local authority**, and make beacons the **notary and reconciler** rather than the gatekeeper. This minimizes ΔV burn, prevents stale-catalog hazards, and avoids brittle distributed consensus dependencies while still providing deterministic, auditable governance.