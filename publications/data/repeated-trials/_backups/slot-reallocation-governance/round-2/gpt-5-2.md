---
questionId: "rq-1-40"
questionSlug: "slot-reallocation-governance"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
roundNumber: 2
generated: "2026-02-07"
type: "discussion-response"
---

## Slot reallocation governance protocol (Round 2): “Quarantine-first, append-only slots, cluster-led with beacon escrow”

### Design stance
Adopt a **quarantine-first** protocol with **append-only slot identity** and **cluster-autonomous execution**. Practically: **we never “reassign” a slot ID**; we **retire** an affected slot ID and **mint** a new slot ID (possibly same geometry) once it is safe. This makes catalog evolution monotonic, reduces split-brain risk, and is much easier to specify/verify in seL4 than in-place edits.

Authority is **Tier 2 (cluster) for time-critical safety actions**; **Tier 3 (beacons) act as escrow/arbiter for cross-cluster boundary changes and global catalog reconciliation**. This matches the autonomy requirement (7–30+ days) and reduces beacon latency coupling.

---

## 1) Failure taxonomy + evidence thresholds (what triggers governance)
Define a small set of failure classes with **explicit evidence** and **timers** so nodes can implement it deterministically.

### Node health classes (inputs)
- **H0 Nominal**: heartbeats + nav residuals within bounds.
- **H1 Comms loss**: missed heartbeats, but last ephemeris was consistent.
- **H2 Nav divergence**: ephemeris updates arrive but residuals exceed bounds / inconsistent timebase.
- **H3 Graceful decommission**: node declares intent (battery, propulsion, attitude) and provides predicted drift.
- **H4 Catastrophic**: no comms + last state suggests loss of attitude control / propulsion anomaly.

### Confirmation logic (cluster-local)
Use **two independent channels** before declaring “failed”: (a) comms/heartbeat and (b) **third-party tracking** from neighbors (angles-only / RF TDOA / relative ranging where available). Avoids false positives from RF shadowing.

Concrete thresholds (tunable, but start here):
- **SUSPECT** after `3` missed heartbeats (e.g., 3× broadcast period).
- **FAILED (probable)** after `N=10` missed heartbeats *and* at least `M=3` neighbor observations inconsistent with expected ephemeris, or no observations possible due to geometry.
- **FAILED (confirmed)** after `T_confirm = 24–72 h` with continued absence *or* a beacon-level independent track mismatch (if available).

Rationale: you want **fast quarantine** (minutes–hours) but **slow retirement/minting** (days) unless the node self-reports graceful decommission.

---

## 2) Slot state machine (what we govern)
Govern **slots as first-class objects**, not just satellites. Each slot has: slot ID, element-window definition, keep-out tube, adjacency list, last-known occupant, and hazard model.

### Slot states
1. **OCCUPIED-NOMINAL**
2. **OCCUPIED-SUSPECT** (node uncertain)
3. **GHOST-QUARANTINE** (assume uncontrolled drift; expanded keep-out)
4. **RETIRED** (slot ID frozen; never reused)
5. **MINTED-AVAILABLE** (new slot ID created; safe to assign)
6. **MIGRATING** (a replacement node is transferring)
7. **OCCUPIED-RECOVERING** (post-migration settling + validation)

### Key rule: quarantine is reversible; retirement is not
- If the node reappears and proves it can hold its window, you can move from **GHOST-QUARANTINE → OCCUPIED-RECOVERING → OCCUPIED-NOMINAL**.
- If you **RETIRE**, you never go back. You mint a new slot ID even if geometry is identical. That prevents stale catalogs from “resurrecting” old authority.

This append-only approach also aligns with the beacon broadcast catalog: nodes can safely accept updates out of order as long as they have the latest epoch + signature chain.

---

## 3) Quarantine geometry: dynamic “hazard tubes” not static buffers
When a node is suspected failed, the danger is not the nominal slot—it’s the **uncertainty growth** in along-track and cross-track.

Define a **Hazard Keep-Out Tube (HKOT)** around the last known state, propagated with conservative covariance growth:
- Start with nav uncertainty (per spec range ±1 m to ≤5 km depending on model).
- Inflate with a worst-case uncontrolled drift model (SRP + attitude tumble + thermal re-radiation; keep it simple but conservative).
- Apply **time-indexed inflation**: HKOT(t) grows until either (a) node is reacquired, (b) it is confirmed dead and its drift is characterized, or (c) it exits the cluster’s operational volume.

Operationally:
- **Immediate action**: neighbors treat HKOT as a temporary keep-out, adjusting their own control laws *without* burning ΔV unless predicted conjunction probability rises above threshold.
- **Escalation**: if HKOT intersects adjacent slot windows, those slots enter **LOCAL-RESTRICTION** (an internal flag) to reduce maneuver noise and increase tracking cadence.

This is how you prevent cascades: you avoid “everyone maneuvers now” and instead tighten estimation + restrict motion unless a conjunction is actually predicted.

---

## 4) Authority and consensus: cluster quorum + beacon escrow
### Intra-cluster actions (Tier 2)
Cluster coordinator can:
- Declare **SUSPECT**, **GHOST-QUARANTINE**
- Publish **local catalog deltas** (signed) to cluster members
- Assign **tracking tasks** (who observes whom, at what cadence)
- Initiate **MIGRATING** for a replacement *only after* safe conditions are met

Consensus mechanism: keep it simple and verifiable.
- Use **Raft-style leader + log** within the ~100-node cluster for catalog deltas (not PBFT unless you truly assume Byzantine nodes; automotive-grade failures are mostly crash/fault, not adversarial).
- Require **quorum ≥ 2/3 of reachable nodes** for irreversible transitions: **RETIRE**, **MINT**, **ASSIGN replacement**.
- Allow **leader-only** for reversible safety transitions: **SUSPECT**, **QUARANTINE**, because latency matters.

### Cross-cluster / boundary actions (Tier 3)
Beacons:
- Maintain the **global catalog checkpoint** and reconcile cluster logs.
- Approve any action that changes **boundary slot geometry** or affects adjacency across clusters.
- Provide **timebase + catalog epoch anchoring** (prevents partitions from persisting divergent slot graphs).

Think of beacons as “certificate authority + notary” rather than day-to-day traffic cops.

---

## 5) Replacement policy: “capacity recovery without ΔV death spirals”
Given the 0.5–5 m/s/year ΔV budget, you cannot afford frequent long-range migrations.

### Policy recommendations
1. **Prefer local spares**: each cluster maintains `1–3%` **warm spares** already near cluster mean elements (not in a tight slot), minimizing transfer ΔV.
2. **Only backfill after hazard stabilizes**:
   - Condition A: HKOT no longer intersects any active slot windows *for a full planning horizon* (e.g., 30–90 days).
   - Condition B: replacement transfer ΔV estimate < cluster budget fraction (e.g., <0.2 m/s typical).
3. **If hazard persists**: don’t backfill; instead **mint a new slot** slightly shifted in mean anomaly / RAAN within the cluster’s allowed envelope, preserving packing while avoiding the ghost.

This is the key trade: accept small geometry drift of the swarm over time rather than spending ΔV to “restore” an exact lattice.

---

## 6) Beacon catalog update mechanism (format + cadence)
You need fast propagation for conjunction screening, but also robust under partitions.

### Data model
Use an **append-only delta log**:
- `CatalogEpoch` (monotonic)
- `DeltaID` (hash)
- `SlotStateChange` records: (slotID, newState, HKOT params, effective time)
- `MintSlot` records: (newSlotID, geometry definition, adjacency edges)
- `AssignOccupant` records: (nodeID → slotID)
- Signatures: cluster leader + quorum attestation; beacon countersign for boundary/global changes

### Cadence
- Cluster broadcasts deltas at **seconds-to-tens-of-seconds** scale (fits local collision screening).
- Beacons broadcast **checkpoint snapshots** at **minutes** scale plus urgent deltas immediately.

Nodes keep both:
- a **recent delta window** for real-time screening
- a **checkpoint** for recovery after comm outages

This directly addresses “stale catalog” risk without requiring constant beacon contact.

---

## 7) Cascading conjunction prevention: explicit “maneuver governance”
Avoidance maneuvers themselves can create cascades if uncoordinated.

Add a governance layer:
- **Maneuver intent broadcast**: any node planning ΔV > threshold (e.g., 1 cm/s) publishes an intent with time window and expected element change.
- Cluster coordinator runs a **conflict check** against adjacency graph and can (a) approve, (b) delay, or (c) request an alternative.
- Emergency autonomy: if a node predicts collision probability above hard limit and cannot reach coordinator, it may maneuver but must broadcast immediately after.

This is cheap in software and prevents “everyone dodges into each other.”

---

## 8) Verification hooks (seL4 / formally verified transitions)
To make this implementable in a high-assurance kernel:
- Keep the slot state machine **small** (7–9 states max).
- Make irreversible transitions require **quorum proof objects** (signed attestations) that are easy to validate.
- Ensure every catalog delta is **purely additive** (append-only), making replay protection and monotonic reasoning straightforward.

---

## Risk notes / cost implications
- **Warm spares cost mass/capex** but save ΔV and reduce long migrations; with 1–3% annual failures, this is usually cheaper than designing for large ΔV margins.
- **Raft vs PBFT**: if you later decide adversarial behavior is in-scope, you can upgrade specific transitions (RETIRE/MINT) to a BFT committee without changing the quarantine mechanics.
- **Over-conservative HKOT** reduces capacity temporarily; that’s preferable to ΔV cascades and catalog inconsistency that jeopardize the <10⁻⁶/node-year requirement.

---

### Bottom line
Implement slot reallocation as **(1) fast local quarantine, (2) slow irreversible retirement, (3) mint-new-slot recovery**, governed by **cluster quorum logs** with **beacon escrow only where necessary**. This architecture is ΔV-aware, autonomy-compatible, minimizes cascade risk, and is realistically specifiable and verifiable.