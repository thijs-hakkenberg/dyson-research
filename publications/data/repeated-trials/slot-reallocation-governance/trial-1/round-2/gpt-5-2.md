---
questionId: "rq-1-40"
questionSlug: "slot-reallocation-governance"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
roundNumber: 2
generated: "2026-02-24"
type: "discussion-response"
---

## Slot Reallocation Governance Protocol (Round 2): “Quarantine → Retire → Commission” with leased authority and ΔV-aware auctions

I recommend formalizing slot handling as a **safety-first lifecycle** with three distinct objects:

- **Node** (physical spacecraft, may fail or drift)
- **Slot** (a *governance construct*: orbital-element window + keep-out tube + adjacency constraints)
- **Occupancy lease** (time-bounded right for a node to occupy a slot)

Key rule: **we never “reassign a slot” in-place.** We **retire** a slot’s current lease, optionally **quarantine** the slot volume, and later **commission a new lease** (possibly for the same geometric slot ID, but with a new epoch/version). This keeps the state machine simple enough to formally verify (seL4) and prevents split-brain catalogs.

---

# 1) Failure taxonomy with machine-enforceable triggers and timelines

Use a **four-level certainty ladder** (avoid binary “dead/alive”), each level mapping to allowed actions and authority tier.

### F0 — `HEALTHY`
Normal ops. Heartbeats + ephemeris updates nominal.

### F1 — `SUSPECT_COMMS`
**Trigger:** missed heartbeats for `T_suspect` (e.g., 3–5 intervals) *but* last state vector age < `T_state_max`.  
**Allowed actions (Tier‑2):**
- Expand local screening uncertainty for that node (inflate covariance / keep-out margin)
- Freeze *new* migrations into adjacent slots
- Start “shadow tracking” using last known dynamics + perturbation model

**Not allowed:** slot lease termination, catalog “death” marking.

### F2 — `PROBABLE_FAILURE`
**Trigger:** missed heartbeats for `T_prob` (e.g., 30–120 minutes, tuned to comm geometry), *and* at least one independent corroborator:
- beacon relay non-reception + neighbor non-reception, or
- inconsistent ranging/optical track, or
- node violates its element window without initiating avoidance protocol

**Allowed actions (Tier‑2, immediate):**
- **Quarantine**: temporarily enlarge keep-out tubes around the suspect node’s predicted tube (time-bounded)
- **Local conjunction priority override**: adjacent nodes may spend ΔV beyond routine budget under a capped “safety reserve”
- **Lease suspension**: mark the slot “non-allocatable” locally (soft-lock)

**Tier‑3 action:** issue *provisional* catalog flag: `UNRESPONSIVE` with uncertainty envelope.

### F3 — `CONFIRMED_LOST` (dead, uncontrolled, or adversarial)
**Trigger:** sustained absence for `T_confirm` (e.g., 12–72 hours depending on cluster density) plus one of:
- independent tracking shows non-compliant drift, or
- power/thermal telemetry cessation + no RF carrier, or
- cryptographic identity replay anomalies (Byzantine suspicion)

**Allowed actions:**
- Tier‑2: maintain quarantine + emergency deconfliction
- Tier‑3: **terminate lease**, **retire slot version**, publish canonical catalog update

This ladder explicitly manages false positives: **only Tier‑3 can “kill” a lease**, but Tier‑2 can protect safety quickly.

---

# 2) Authority hierarchy: leased authority with bounded autonomy

### Tier‑2 (cluster coordinator) authority: **fast safety + local locks**
- Can declare `SUSPECT/PROBABLE` and impose **temporary local locks/quarantines**
- Can command **emergency avoidance** within cluster
- Can propose lease termination to Tier‑3 with evidence bundle
- Cannot permanently re-open a quarantined region without Tier‑3 confirmation (prevents local optimism)

### Tier‑3 (beacon/relay) authority: **global registry + canonical catalog**
- Owns the **canonical slot/lease registry** and versioning
- Issues signed **Catalog Deltas** (see §5) with monotonic sequence numbers
- Arbitrates disputes between adjacent clusters (cross-boundary conjunction risk)

### Governance primitive: **Occupancy Lease**
- Lease fields: `{slot_id, slot_version, node_id, start_epoch, expiry_epoch, constraints_hash}`
- Default lease expiry forces periodic reaffirmation (e.g., 7–30 days to match autonomy requirement)
- If a node goes silent beyond expiry, Tier‑3 can retire without waiting for perfect certainty

This “lease expiry” is a major safety tool: it converts “hard death detection” into “failure to renew.”

---

# 3) Slot adjacency graph + quarantine mechanics (prevent cascades)

Model each cluster as a graph:

- Vertices: slots (element windows)
- Edges: adjacency (potential conjunction coupling given covariance + perturbations)
- Edge weights: estimated collision risk sensitivity and ΔV coupling cost

**Quarantine is applied on the graph**, not just geometrically:
- When a node enters F2/F3, quarantine its slot and apply a **k-hop adjacency hold** (k=1–2 typical) where:
  - migrations into those slots are forbidden,
  - keep-out tubes are temporarily expanded by factor `q(t)` that decays with improved track certainty.

**Why this matters:** it prevents “helpful” migrations into a region that’s about to become dynamically uncertain, which is a common cascade trigger.

---

# 4) Reallocation policy: ΔV-aware commissioning, not “musical chairs”

After a lease is terminated and the region is safe enough:

### Step A — Decide whether to **recommission** capacity
Not every orphaned slot should be refilled immediately. Use a rule:
- Recommission only if expected energy yield gain over horizon `H` exceeds expected ΔV + risk cost:
  - `Value = P_gain(H) - λ1*ΔV_cost - λ2*Risk_increment`
This keeps you within 0.5–5 m/s/year budgets.

### Step B — Choose a replacement via **cluster-local auction**
Within the cluster, candidates bid with:
- ΔV to migrate (computed from current element window to target)
- time-to-arrive
- remaining prop margin
- expected tracking quality (sensor health)
- thermal/power margin

Coordinator selects the winner, but **Tier‑3 must ratify** if:
- crossing cluster boundaries, or
- the quarantine touched multi-cluster adjacency edges, or
- catalog delta rate is high (avoid thrash).

This avoids repeated “nearest neighbor” moves that slowly drain a subset of nodes.

### Step C — Migration as a two-phase commit (2PC)
1. **Prepare:** Tier‑3 issues a signed `LEASE_PREPARE(slot_version+1, node_id, deadline)`
2. **Commit:** after the node reports it is within the acceptance tube, Tier‑3 issues `LEASE_COMMIT`
If the node fails mid-transfer, the lease auto-aborts and quarantine persists.

This is how you keep the ephemeris catalog consistent under intermittent comms.

---

# 5) Beacon catalog update mechanism: delta-based, signed, and bounded

Do not rebroadcast entire catalogs frequently; use **authenticated deltas**:

### Canonical objects
- `SLOT_DEF(slot_id, version, constraints_hash, adjacency_hash)`
- `LEASE_STATE(slot_id, version, node_id | null, state, epochs, quarantine_params)`
- `TRACK_ENVELOPE(node_id, epoch, mean_state, covariance_or_bounds, source_confidence)`

### Update format
- **Monotonic sequence number** per beacon + hash chain (`prev_hash`)
- Threshold signatures (e.g., 2-of-3 beacons) for `CONFIRMED_LOST` and `LEASE_COMMIT`
- Lightweight single signature for `UNRESPONSIVE` flags

### Cadence
- Normal: slow (minutes)
- On F2/F3 events: burst mode (seconds) until local clusters ack receipt
- Nodes maintain a **staleness budget**: if catalog age > `T_stale`, they automatically widen keep-outs and suspend migrations (failsafe).

This directly supports the <10⁻⁶ collision probability target by preventing silent catalog divergence.

---

# 6) Handling the “dead node drift” explicitly (the hard part)

For F2/F3 nodes, treat them as **uncooperative debris with known area-to-mass uncertainty**. Protocol requirements:

- Maintain a **propagated uncertainty tube** (not a point ephemeris)
- Require neighbors to plan avoidance against the tube, not the mean
- Quarantine decay is gated by *track quality improvement*, not time alone

If the node is likely still thrusting (Byzantine or partial failure), you escalate:
- keep quarantine longer,
- require multi-sensor corroboration before shrinking keep-outs,
- raise the authority to Tier‑3 for cross-cluster coordination.

---

# 7) Concrete parameter starting points (tunable in simulation)

For Phase 1 (1k–3k nodes, ~100/node clusters):

- Heartbeat interval: 10–60 s (depends on comm duty cycle)
- `T_suspect`: 3–5 missed
- `T_prob`: 30–120 min (must exceed typical comm outages)
- `T_confirm`: 12–72 hr (density-dependent)
- Lease expiry: 7–14 days (aligns with autonomy)
- Quarantine k-hop: 1 by default; 2 if track uncertainty grows faster than threshold
- Safety ΔV reserve: fixed per year (e.g., 20–30% of annual budget) with strict accounting

These are intentionally conservative; Monte Carlo will tighten them.

---

# 8) What to simulate (so we can converge fast)

1. **False-positive stress tests**: comm outages, beacon eclipses, coordinator failures. Measure unnecessary quarantines and ΔV burn.
2. **Cascade scenarios**: failure in high-degree adjacency slots; verify k-hop holds prevent chain migrations.
3. **Catalog divergence**: delayed deltas + partitioned clusters; ensure widening keep-outs keeps collision probability under threshold.
4. **Auction fairness**: ensure the same nodes aren’t repeatedly selected and depleted.

---

## Bottom line recommendation

Adopt a **lease-based governance state machine** with **Tier‑2 quarantine authority** and **Tier‑3 canonical lease retirement/commissioning**, backed by **delta-signed catalog updates** and **ΔV-aware auctions** for replacement selection. This directly addresses cascade risk, catalog staleness, and propulsion constraints while remaining implementable and verifiable in the seL4-based autonomy stack.