---
questionId: "rq-1-40"
questionSlug: "slot-reallocation-governance"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
roundNumber: 2
generated: "2026-02-24"
type: "discussion-response"
---

## Slot Reallocation Governance Protocol (Round 2): Deterministic, quarantine-first, beacon-ratified

### Position (opinionated)
Treat slot reallocation as **(1) a safety state machine with deterministic rules** and **(2) a catalog publication problem**, not as an open-ended distributed consensus problem. Use **Tier‑2 clusters for immediate safety actions** (quarantine + provisional ownership) and **Tier‑3 beacons as the canonical “ephemeris ledger” publisher** (ratification + cross-cluster conflict resolution). This avoids PBFT-style complexity while still meeting the collision risk and autonomy constraints.

---

## 1) Failure classification taxonomy → mandatory state machine
Define a small set of failure states with unambiguous triggers and prescribed actions. Every node/cluster should compute the same transitions given the same inputs.

### States
**S0 — Nominal**
- Heartbeats + ephemeris updates within expected bounds.

**S1 — Suspected (Comms/Telemetry Loss)**
- Trigger: `N_miss` missed heartbeats OR stale ephemeris > `T_stale`.
- Action: *No reassignment.* Increase tracking uncertainty; start “shadow propagation” using last known state + process noise.

**S2 — Confirmed Non-Cooperative (NC)**
- Trigger: (a) `N_confirm` consecutive misses from ≥`k` independent observers (within cluster), OR (b) beacon cannot authenticate any recent signed state, OR (c) ranging/optical confirms divergence from commanded window.
- Action: **Automatic quarantine** of affected volume (details below). Freeze slot ownership.

**S3 — Hazardous Drift / Tumbling / Thrusting (HD)**
- Trigger: observed covariance growth rate exceeds threshold, or trajectory intersects neighbor keep-out tubes within `T_CA` (time to closest approach), or unexpected ΔV signature.
- Action: **Expand quarantine**, initiate local avoidance advisories, and prohibit migrations into adjacent slots until hazard decays.

**S4 — Cleared / Removed**
- Trigger: (a) confirmed passivation + stable drift outside governance volume, OR (b) replacement has taken slot and NC object’s predicted conjunction risk drops below threshold for `T_clear`.
- Action: quarantine shrinks/removed; slot becomes eligible for reassignment.

### Key design choice: confirmation thresholds
Use **two-tier confirmation** to avoid false positives:
- Cluster-level confirm: e.g., `N_miss=3` heartbeats → S1; `N_confirm=12` heartbeats + ≥`k=5` observers → S2.
- Beacon-level confirm: beacon ratifies S2/S3 when it receives cluster’s signed evidence bundle or independently observes.

This keeps “temporary comms fade” from causing slot churn (ΔV waste) while still moving quickly when a node is truly gone.

---

## 2) Quarantine-first geometry (the core safety mechanism)
When a node enters S2/S3, do **not** immediately reassign. Instead create a **Quarantine Volume (QV)** around the failed slot and, if needed, its adjacency set.

### Quarantine volume definition (practical)
Define QV as:
- Failed node’s **keep-out tube inflated** by a factor based on covariance growth and worst-case unmodeled acceleration.
- Plus **adjacent-slot guard bands** along-track/radial/normal directions depending on swarm geometry.

A workable rule:
- `Inflation = max(σ_pos(t), a_unk * t^2 / 2)` projected over a horizon `T_h` (e.g., 7–14 days for autonomy).
- If predicted miss distance to any neighbor < `D_min` within `T_h`, quarantine expands to include that neighbor’s tube as “restricted operations”.

### Operational consequences
- Nodes inside QV remain in their slots but switch to **tight conjunction posture**: higher cadence relative navigation, reduced discretionary maneuvers, and pre-approved avoidance templates.
- **No slot migrations into QV** until S4.

This directly addresses cascading conflicts: you spend *computation and catalog bandwidth* first, not ΔV.

---

## 3) Authority hierarchy: “provisional local, canonical global”
### Tier 2 (cluster coordinators): tactical authority
Cluster coordinators can:
- Declare S1/S2/S3 for members **within the cluster**.
- Instantiate QV and publish **Provisional Slot Status Updates (PSSU)**.
- Assign a **temporary custodian** node to maintain the slot’s “metadata presence” (catalog continuity) without physically moving.

They cannot:
- Permanently transfer slot ownership across clusters.
- Shrink quarantine below minimum safety bounds without beacon ratification.

### Tier 3 (beacons): canonical publisher / arbiter
Beacons:
- Maintain the **master ephemeris catalog** (the “ledger of record”).
- Ratify cluster actions and resolve cross-cluster conflicts (e.g., overlapping quarantines, competing claims).
- Issue **Catalog Delta Blocks** at a fixed cadence (e.g., every 5–15 minutes) signed with beacon keys.

This matches the autonomy requirement: clusters act fast even if beacons are temporarily unreachable; beacons later reconcile.

---

## 4) Slot reallocation itself: decouple “ownership” from “occupancy”
A major ΔV saver is to avoid treating reassignment as immediate physical relocation.

### Three-step reallocation
1) **Logical vacancy** (immediate): slot marked “vacant / quarantined”, but still exists in catalog with predicted hazard object.
2) **Logical reassignment** (hours–days): a replacement node (or spare within cluster) is granted *ownership* of the slot ID and window, but **does not move yet** if QV still active.
3) **Physical migration** (days–weeks): only when QV cleared and ΔV budget allows.

This prevents “catalog staleness” without triggering impulsive maneuvers.

### Migration policy (ΔV-aware)
Adopt a hard annual “maneuver budget envelope” per cluster (derived from 0.5–5 m/s/year per node spec). Example governance rule:
- Only allow **X migrations per cluster per quarter**, where X is computed from median transfer ΔV and remaining prop margin.
- If failures exceed capacity, accept reduced fill factor rather than burning the fleet’s lifetime ΔV.

---

## 5) Consensus mechanism: deterministic rules + signed evidence, not PBFT
PBFT/Raft across ~100 nodes is expensive and brittle under intermittent links. Instead:

### Deterministic decision function
Define a deterministic function `F(observations) → state transition + QV parameters` so any honest node can reproduce the result.

### Evidence bundles
Cluster coordinator publishes:
- Missed-heartbeat counts from multiple observers
- Last authenticated ephemeris
- Tracking residuals / covariance estimate
- QV definition + horizon
All **signed** and **time-stamped** (≤10 ms sync helps here).

### Quorum requirement
Use a simple **k-of-n attestation** for S2/S3:
- S2: k=5 independent witnesses
- S3: k=8 or “any two sensors + conjunction prediction breach”
This is not Byzantine consensus; it’s thresholded evidence to gate high-impact actions.

---

## 6) Beacon catalog update mechanism (format + cadence)
To keep conjunction probability <10⁻⁶ per node-year, the catalog must be fresh and authenticated.

### Data structure
- Base catalog snapshot (less frequent)
- **Delta blocks** (frequent): append-only list of slot status changes, QV polygons/tubes, and updated state vectors/covariances.

Each delta block includes:
- `block_id`, `time_range`, `beacon_signature`
- For each slot: `slot_id`, `status` (nominal/suspected/NC/hazard/quarantine), `owner_id`, `occupant_id` (can be null), `state_vector`, `covariance`, `valid_until`, `QV_ref`

### Cadence
- Cluster PSSU: 30–120 s (local dissemination)
- Beacon delta blocks: 5–15 min (global coherence)
- Emergency delta: immediate broadcast when predicted conjunction risk crosses threshold.

---

## 7) Handling the “failed node drift” worst case (cascading avoidance prevention)
When S3 triggers, impose a **cluster-wide maneuver governor**:
- Avoidance maneuvers must be **coordinated at cluster level** to prevent oscillatory “everyone dodges everyone” behavior.
- Use a deterministic priority rule: protect nodes with lowest remaining ΔV and those in high-degree adjacency graph positions first.
- Prefer **along-track phasing nudges** (if geometry allows) over radial/normal burns to minimize long-term dispersion and stationkeeping penalty.

---

## 8) What to simulate / verify next (to close the open questions)
1) **Adjacency graph criticality**: identify high-centrality slots; pre-allocate larger windows or extra guard bands there.
2) **QV sizing law**: tune `a_unk`, `T_h`, and inflation factors to keep false quarantines low while guaranteeing <10⁻⁶ risk.
3) **Catalog latency vs risk**: Monte Carlo with realistic link outages; verify that delta cadence + local PSSU keeps screening valid during 7–30 day autonomy.
4) **ΔV economics**: quantify “logical reassignment” benefit; set migration caps that preserve 50-year lifetime.
5) **Formal verification scope (seL4)**: verify state-machine transitions, signature checking, and deterministic QV computation; do *not* attempt to formally verify orbital dynamics—verify bounds and invariants instead.

---

### Bottom line
Adopt **Quarantine-First**, **deterministic state-machine governance**, **cluster tactical authority**, and **beacon-signed catalog deltas**. Reassign **ownership quickly** to keep the ledger coherent, but delay **physical migration** until quarantine clears and ΔV budgets permit. This architecture is implementable under autonomy constraints and directly targets the two real failure modes: stale catalogs and cascading avoidance.