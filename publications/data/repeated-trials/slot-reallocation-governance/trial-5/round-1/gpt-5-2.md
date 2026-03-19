---
questionId: "rq-1-40"
questionSlug: "slot-reallocation-governance"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
roundNumber: 1
generated: "2026-02-24"
type: "discussion-response"
---

### Recommended slot reallocation governance protocol (opinionated baseline)

Treat slot reallocation as a **safety-critical, rate-limited, two-phase commit** process with **local autonomy for containment** and **beacon-mediated final authority for catalog truth**. In practice:

- **Tier 2 (cluster) has unilateral authority to:**
  1) declare *suspected failure*,  
  2) initiate *local quarantine/avoidance*,  
  3) allocate *temporary* “holding” slots and adjust intra-cluster element windows to maintain the <10⁻⁶/node-year conjunction requirement.

- **Tier 3 (beacons) has authority to:**
  1) finalize *slot retirement* and *permanent reassignment*,  
  2) publish the **authoritative ephemeris catalog** and slot ownership map,  
  3) arbitrate cross-cluster conflicts and enforce global rate limits on migrations.

This mirrors how you’d design a safety PLC vs. enterprise scheduler: **contain locally fast; commit globally carefully.**

---

## 1) Failure classification taxonomy (minimal set that maps cleanly to actions)

Define 5 states; don’t overfit early. Each state has an allowed governance action set.

1) **Nominal (GREEN)**  
   - Heartbeats + ephemeris updates within bounds.

2) **Comms-Degraded (YELLOW-C)**  
   - Missed heartbeats but last ephemeris still fresh enough for screening.  
   - Action: no reassignment; tighten conjunction screening margins; request relay routing changes.

3) **Nav-Degraded / Ephemeris-Stale (YELLOW-N)**  
   - Node is talking but orbit solution quality or timestamping violates bounds (ties to your ≤10 ms sync requirement and nav accuracy model).  
   - Action: treat as higher collision risk; enlarge its keep-out tube; restrict neighbors’ maneuvers that would reduce separation.

4) **Suspected Lost (ORANGE)**  
   - Threshold: e.g., **N missed heartbeats + no valid ephemeris for T_stale**, where N and T_stale are tuned per link budget and dynamics (typical: N=3–10, T_stale=1–6 hrs depending on conjunction environment).  
   - Action: **cluster coordinator can quarantine the slot and adjacent slots**; may reassign *temporary* occupancy only if ΔV-neutral (see “holding slots” below).

5) **Confirmed Lost / Uncontrolled (RED)**  
   - Trigger: independent confirmation from ≥2 sources (e.g., two relays, or relay + neighbor optical/radar ranging, or persistent non-response for T_confirm such as 24–72 hrs).  
   - Action: **beacon retires slot**, issues global catalog update, and schedules permanent reassignment when safe.

Key point: **slot reassignment is never triggered by YELLOW** states—only ORANGE/RED, and permanent reassignment only by RED.

---

## 2) Slot adjacency graph + “blast radius” modeling (what to simulate)

Model each cluster as a graph:

- **Vertices:** slots (orbital element windows + keep-out tubes)
- **Edges:** “conflict potential” (probability that uncertainties + drift could cause tube violation within horizon H)

Edge weights should incorporate:
- relative mean motion / differential elements,
- navigation covariance growth when ephemeris goes stale,
- maneuver authority (ΔV left, thrust availability),
- screening horizon (e.g., 7–30 days autonomous requirement).

From this, compute:
- **Quarantine set Q(f):** minimal set of slots to freeze/expand to keep collision probability under threshold when slot f becomes ORANGE/RED.
- **Criticality score:** expected ΔV and lost collection capacity if f is removed.

This gives you a principled way to decide when a failure should trigger **local quarantine only** vs. **cluster reshuffle** vs. **cross-cluster intervention**.

---

## 3) Governance: distributed consensus design (pragmatic, not crypto-theoretical)

### Intra-cluster decisions: Raft-like, not PBFT
For ~100-node clusters with a rotating coordinator, I recommend **Raft-style crash-fault tolerance** for *operational decisions*, not PBFT. Rationale:
- Your dominant fault mode is **non-Byzantine** (automotive-grade failures, comm dropouts), and PBFT overhead is high.
- You still need **cryptographic authentication** of messages, but you don’t need Byzantine agreement for every slot change.

**Quorum:** simple majority of “currently healthy voters” (dynamic membership).  
**Coordinator rotation:** time-based + health-based; ensure it doesn’t rotate during an ORANGE/RED event unless coordinator itself is suspect.

### Cross-cluster / global catalog: beacon-signed authority with challenge window
Beacons publish the authoritative catalog. To prevent beacon single-point mistakes without full PBFT:
- Require **M-of-N beacon signatures** for *permanent* slot retirement/reassignment (e.g., 2-of-3 or 3-of-5 depending on architecture).
- Allow a short **challenge window** (minutes to hours) where clusters can object with evidence (ephemeris logs, ranging).

This is closer to “federated notarization” than full Byzantine consensus and is implementable under autonomy constraints.

---

## 4) The actual protocol: containment → quarantine → commit → migrate

### Phase A — Detection & containment (Tier 2, seconds–minutes)
1) Missed heartbeat triggers YELLOW; stale ephemeris triggers YELLOW-N.  
2) Coordinator increases screening margins around the node and broadcasts a **Local Risk Advisory** to neighbors (cluster-only).

### Phase B — Quarantine (Tier 2, minutes–hours)
When ORANGE:
- Coordinator declares **Slot Quarantine**:
  - freeze maneuvers that reduce separation,
  - expand keep-out tubes for the suspect slot,
  - optionally quarantine adjacent slots per Q(f) from the adjacency graph.
- Coordinator assigns a **shadow track**: a propagated uncertainty tube for the failed node based on last known state + covariance growth, updated by any passive observations.

Crucially: quarantine is designed to be **ΔV-minimal**: it should rely on *restrictions* and *tube expansion* before maneuvers.

### Phase C — Beacon adjudication (Tier 3, hours–days)
Coordinator submits a **Failure Evidence Package** to beacons:
- last valid ephemeris + timestamp,
- heartbeat history,
- any neighbor ranging/angles-only observations,
- predicted drift envelope.

Beacons respond with one of:
- **Reinstate** (false positive): restore slot, shrink tubes gradually.
- **Extend quarantine** (insufficient evidence): keep ORANGE.
- **Confirm lost** (RED): retire slot and publish catalog update.

### Phase D — Reassignment and migration (Tier 3 schedules, Tier 2 executes)
Once RED:
- Beacon marks slot as **RETIRED (hazard)** for a defined hazard half-life (e.g., 30–180 days depending on drift dynamics and ability to observe).
- Only after hazard decays (or track certainty improves) does it become **VACANT (reassignable)**.

**Replacement strategy (ΔV-aware):**
- Prefer **“nearest-neighbor promotion”**: fill vacancy using a node already near the element window boundary to minimize ΔV.
- Use **holding slots**: pre-defined low-value, ΔV-cheap parking windows inside each cluster that can temporarily store spares or displaced nodes without disturbing packing.
- Enforce a **cluster ΔV budget governor**: cap migrations per year per cluster consistent with 0.5–5 m/s/year spec; if exceeded, accept reduced collection capacity rather than risk collision.

---

## 5) Beacon catalog update mechanism (format + cadence + security)

### Catalog structure (incremental, signed)
Use an append-only log of “Slot Governance Events”:
- `SLOT_QUARANTINE(slot_id, params, start_time, ttl)`
- `NODE_STATUS(node_id, state, confidence, timestamp)`
- `SLOT_RETIRED(slot_id, hazard_model, start_time, review_time)`
- `SLOT_VACANT(slot_id)`
- `SLOT_ASSIGNED(slot_id, node_id, effective_time, constraints)`
- `TUBE_UPDATE(slot_id, geometry_hash, effective_time)`

Each event:
- is **signed** by the issuing authority (cluster for quarantine advisories; beacons for retire/assign),
- includes a **monotonic epoch number** to avoid rollback/fork,
- supports **delta dissemination** so nodes don’t need full catalog every time.

### Cadence
- **Routine deltas:** minutes-level (tunable to comm geometry), since you’re not doing rigid formation flying.
- **Emergency deltas (ORANGE/RED):** immediate broadcast repeated over a bounded interval to ensure reception.

### Authentication
- Per-node identity keys as you noted; add:
  - beacon threshold signatures for permanent changes,
  - replay protection via epoch + timestamp bounds (ties to your ≤10 ms sync).

---

## 6) Risk controls and “don’t do this” guidance

**Avoid immediate permanent reassignment** on mere comms loss. The worst-case is you “double-occupy” a slot when the node comes back, forcing ΔV-expensive deconfliction.

**Avoid cluster-wide reshuffles** as a default response. With your ΔV budget, reshuffling is the quickest way to paint yourself into a corner over a 50-year life. Prefer:
1) quarantine,
2) accept temporary capacity loss,
3) slow, ΔV-minimized replacement.

**Don’t rely on PBFT everywhere.** Keep formal verification scope manageable (seL4 kernel + small critical protocols). Use simple, auditable state machines.

---

## 7) What to prototype/simulate first (highest leverage)

1) **Adjacency-graph-derived quarantine sets Q(f)** and their effect on collision probability and ΔV usage under Monte Carlo failures (10–90/year for Phase 1).  
2) **False-positive rate vs. reassignment latency** trade: tune N missed heartbeats and T_stale/T_confirm.  
3) **ΔV governor policies**: quantify how many reassignments/year you can afford before violating 0.5–5 m/s/year, and how much capacity you lose if you refuse migrations.  
4) **Catalog delta propagation latency**: ensure worst-case stale catalogs do not push collision risk above 10⁻⁶/node-year.

---

### Bottom line
Implement **fast local quarantine + slow global commit**, with **beacon-notarized permanent changes**, **graph-based quarantine sets**, and **ΔV-governed migration scheduling**. This directly addresses cascading conflicts, stale catalogs, and resource stranding while remaining feasible under autonomy and formal verification constraints.