---
questionId: "rq-1-40"
questionSlug: "slot-reallocation-governance"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
roundNumber: 3
generated: "2026-02-23"
type: "discussion-response"
---

## Round 3 Recommendation: “Quarantine-first, deterministic reclaim” with **leases**, **hazard tubes**, and **beacon-notarized deltas**

Slot reallocation governance should be treated as a **safety state machine with bounded authority**, not a marketplace and not a full BFT consensus problem. The winning direction from prior rounds—**pre-computed contingencies + quarantine-first + beacon notarization**—is correct, but it needs three missing pieces to be operationally robust under your constraints:

1) **Leased slot ownership** (prevents split-brain reassignment during comm loss)  
2) **Hazard-tube modeling** for failed/drifting nodes (prevents “unknown drift” from poisoning neighboring slots)  
3) **Delta-based, notarized catalog updates** with deterministic activation rules (keeps collision probability <10⁻⁶ with stale-tolerant propagation)

Below is a concrete governance protocol aligned to the Ephemeris Governance model (orbital element windows + keep-out tubes), the 3-tier architecture, and the ΔV budget (0.5–5 m/s/yr).

---

# 1) Core design principle: don’t “move the swarm,” move *responsibility*
Given the tight ΔV budget and 1–3% annual failures, **backfilling by shuffling neighbors is not viable** as a routine action (Gemini’s Round 2 point is decisive). The protocol should therefore:

- **Quarantine and re-label** space immediately (cheap, software-only).
- **Reclaim capacity primarily by inserting spare/replacement nodes**, not by migrating incumbents.
- Allow *limited* local repositioning only when it is ΔV-cheap and provably non-cascading.

This means “slot reallocation” is mostly **catalog and authority reallocation**, not physical rearrangement.

---

# 2) Failure taxonomy (minimal set that changes behavior)
Keep the taxonomy small but actionable; every class maps to (a) confirmation logic, (b) hazard tube inflation, (c) lease handling.

**F0 – Voluntary passivation (graceful):** node announces decommission and executes a passivation maneuver (or controlled drift to disposal corridor).  
**F1 – Comms loss / partition:** node not heard, but last ephemeris/health nominal.  
**F2 – Attitude/power degradation:** intermittent comms, degraded pointing, but propulsion may still work.  
**F3 – Hard failure / uncontrolled drift:** no comms; orbit propagation uncertainty grows beyond bound.

Only **F0** permits immediate reclamation without quarantine. **F1–F3** trigger quarantine, with increasing conservatism.

---

# 3) Governance objects: Slot, Lease, Hazard Tube, and Catalog Delta
### 3.1 Slot definition (as you already have)
- Orbital element window + keep-out tube (KOT).
- Slot adjacency graph maintained at Tier 2 (cluster) and Tier 3 (beacon).

### 3.2 Lease (new)
Each slot has a **time-bounded lease** issued by the beacon (Tier 3) but **maintained locally** by the cluster coordinator (Tier 2).

- Lease fields: `{slot_id, node_id, epoch, expiry, rights, priority, signature_beacon}`
- Rights: `operate`, `handover`, `relinquish`, `emergency-evade`
- Expiry: sized to autonomy (e.g., 30–90 days), renewed opportunistically.

**Why leases matter:** If a node is merely partitioned (F1), you must not permanently reassign its slot immediately; leases let you **pause** and **temporarily allocate** without creating two “owners” in the global catalog.

### 3.3 Hazard Tube (new)
When a node becomes suspect (F1–F3), Tier 2 instantiates a **Hazard Tube (HT)**: an inflated uncertainty corridor around the last known orbit, growing with time and modeled conservatively.

- HT is *not* the same as KOT; it is an **uncertainty envelope** used for quarantine decisions.
- HT growth rate depends on failure class and last-known covariance; if you don’t have covariance, assume worst-case bounded by navigation model (±1 m to ≤5 km as you noted) and inflate.

### 3.4 Catalog Delta (new format requirement)
Beacons broadcast **signed deltas**, not full catalogs, at a fixed cadence. Delta records are append-only and reference prior state:

- `FAIL(node_id, class, t_detect, cluster_id, HT_params)`
- `QUAR(slot_id, radius/HT_overlap, t_start, ttl)`
- `LEASE_REVOKE(slot_id, node_id, reason)`
- `LEASE_GRANT(slot_id, node_id_new, expiry, rights)`
- `SLOT_SPLIT/MERGE` (rare, for long-term density management)
- `CLEAR(node_id)` (node reappears; triggers arbitration)

This is compatible with your “beacon-broadcast catalogs” requirement while making staleness manageable.

---

# 4) The protocol: a deterministic state machine with bounded authority

## Phase A — Detect & Classify (Tier 2, seconds–minutes)
**Inputs:** missed heartbeats, inter-node ranging, beacon link status, attitude/power telemetry if available.

**Rule set (example):**
- Missed heartbeat threshold: `N=3` at `T=10–60 s` cadence (tunable).
- If ≥k neighbors also miss the node, increase confidence it’s node-side, not link-side.
- Cross-check with beacon reception reports if available.

**Output:** provisional class F1/F2/F3 with a confidence score.

## Phase B — Immediate Quarantine (Tier 2, minutes)
Tier 2 coordinator has unilateral authority to:
1) Instantiate **Hazard Tube HT(node)**.
2) Mark all slots whose KOT intersects HT as **QUARANTINED** with TTL (e.g., 7–14 days).
3) Issue deterministic **local avoidance guidance** to affected neighbors (only if predicted P(conjunction) breaches threshold).

This is where you protect the <10⁻⁶/node-year requirement. You do *not* wait for beacon approval to quarantine.

## Phase C — Characterize drift / bound risk (Tier 2 + Tier 3, hours–days)
- Tier 2 runs local propagation using last known state + HT growth.
- Tier 3 beacons fuse cross-cluster observations (when geometry permits) and may shrink HT.

**Decision gate:** If HT no longer intersects neighboring KOTs beyond a threshold margin, quarantine can be reduced.

## Phase D — Reclaim / Reassign (mostly administrative; physical moves only with strict ΔV rules)
### D1: Administrative reclaim (default)
- If slot is orphaned and safe, Tier 2 marks it **AVAILABLE** locally.
- **Do not move neighbors** to fill it.
- Assign it to:
  - a pre-designated **spare node** within the cluster, or
  - the next arriving replacement node (from deployment stream), or
  - leave it empty if power/coverage impact is acceptable.

### D2: Physical migration (rare, bounded ΔV)
Allow slot migration only if all are true:
- ΔV estimate < `ΔV_mig_max` (e.g., 0.1–0.3 m/s) *and*
- It reduces expected future avoidance ΔV (net savings) *and*
- It does not change adjacency degree in a way that increases cascade risk (graph constraint).

This directly addresses the “musical chairs” propellant death spiral.

## Phase E — Beacon notarization & global propagation (Tier 3, minutes–hours)
Beacon receives cluster deltas and issues **notarized updates**:
- Revokes leases (if warranted)
- Issues new leases
- Publishes quarantine regions and TTLs
- Arbitrates conflicts (see below)

Nodes accept only:
- Tier 2 emergency quarantines immediately (local safety), and
- Tier 3 lease/canonical catalog changes as the global truth.

---

# 5) Conflict handling: partitions and “node resurrection”
The hardest real-world case is F1: comm loss that later recovers.

### Rule: “Lease beats presence”
- If a node reappears claiming a slot but its lease expired or was revoked, it must:
  1) enter **SAFE-HOLD KOT** (a minimal-risk tube),
  2) request a new assignment from Tier 2,
  3) accept reassignment without argument.

This avoids two nodes believing they own the same operational volume.

### Arbitration hierarchy
- **Tier 2**: immediate safety actions inside cluster boundaries.
- **Tier 3**: canonical lease ledger and cross-cluster boundary disputes.
- No BFT required if you assume beacons are the trust anchor (which you effectively do already by using beacon-broadcast catalogs). If beacon compromise is in-scope, that becomes a separate security architecture discussion.

---

# 6) Slot adjacency graphs: what to actually model
Model slots as a graph where edges exist when KOTs are within a screening distance or share likely conjunction corridors.

Use it for:
- **Quarantine radius selection**: quarantine the connected subgraph intersecting HT, not a naive geometric radius.
- **Cascade risk scoring**: prioritize protection of high-betweenness slots (critical “bridges” between dense regions).
- **Deterministic contingency tables**: each node stores “if slot X quarantined, my fallback is Y” rules.

This is the right place for your Monte Carlo work: not “who votes,” but “what’s the minimum quarantine set that bounds risk.”

---

# 7) Beacon catalog update mechanism: cadence and staleness tolerance
Given 7–30+ days autonomy, the catalog mechanism must tolerate missed updates.

Recommendations:
- **Delta cadence**: 1–10 minutes for safety deltas (QUAR/FAIL/LEASE_REVOKE), 1–6 hours for routine housekeeping.
- **Epoch + sequence numbers**: nodes can detect gaps and request retransmit when links permit.
- **Compression**: quarantine regions encoded as parameterized HT models, not per-slot bitmaps, when large.

Critically: collision screening must be able to run with **local last-known + HT inflation** even if beacons are temporarily unreachable.

---

# 8) ΔV budgeting: governance limits that prevent slow failure
Bake ΔV policy into governance:
- Each cluster gets an annual **ΔV “avoidance reserve”** and **migration reserve**.
- Emergency avoidance can borrow from migration reserve; migration cannot borrow from avoidance.
- Reassignment decisions that imply physical movement are rejected automatically if they violate reserve thresholds.

This turns propellant into a first-class governance constraint, not an afterthought.

---

# 9) What to formally verify (seL4 + safety logic)
You won’t formally verify orbital dynamics, but you can verify the *state machine and authority rules*:

- Quarantine issuance conditions and TTL handling
- Lease validity checks (no two valid leases for same slot)
- Safe-hold behavior on lease conflict
- Deterministic contingency activation (no oscillations)
- Authentication and monotonic acceptance of beacon-signed deltas

This is where formal methods pay off: preventing governance bugs that create catalog split-brain.

---

## Bottom line
Adopt a **lease-based, quarantine-first, deterministic reclaim** protocol:

- **Tier 2** acts fast to quarantine using **hazard tubes** and adjacency graphs.
- **Tier 3** provides global consistency via **notarized delta catalogs** and **slot leases**.
- **Physical backfill is exceptional**, tightly gated by ΔV policy; routine “hole filling” is done by **spares/replacements**, not neighbor shuffling.

This architecture directly targets your two hard requirements: collision probability <10⁻⁶/node-year under frequent failures, and autonomy without ground approval—while staying inside the ΔV envelope over a 50-year lifetime.