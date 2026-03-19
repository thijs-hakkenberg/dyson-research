---
questionId: "rq-1-40"
questionSlug: "slot-reallocation-governance"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
roundNumber: 2
generated: "2026-02-24"
type: "discussion-response"
---

## Slot Reallocation Governance Protocol (Round 2): “Quarantine-First, Lease-Then-Deed” (QFLD)

I recommend formalizing slot reallocation as a **safety-first, time-phased governance protocol** with **two separate authorities**:

- **Cluster tier (Tier 2)** has *immediate safety authority* to quarantine, fence, and locally deconflict within seconds–minutes.
- **Beacon tier (Tier 3)** has *global registry authority* to “deed” permanent slot ownership and publish the master ephemeris catalog.

This directly supports Project Dyson’s core constraints: **P(conjunction) < 10⁻⁶ per node-year**, **1–3% annual failures**, **0.5–5 m/s/year ΔV**, and **7–30+ days autonomous ops**.

The key architectural move is to treat a “vacated” slot as **hazardous until proven empty**, and to treat reassignment as a **lease→deed** process rather than instant ownership.

---

## 1) Failure taxonomy → governance actions (make it executable)

Define failure classes that map to *specific timers, quorum rules, and keep-out modifications*:

### F0: Cooperative release (graceful shutdown / planned exit)
- **Signature:** authenticated “RELEASE_SLOT” intent + final ephemeris + passivation status.
- **Action:** slot becomes **Immediately Releasable**; no quarantine expansion needed.
- **Authority:** cluster can issue **local lease**; beacon later issues deed.

### F1: Suspected loss (temporary comms / intermittent)
- **Signature:** missed heartbeats, but last state consistent; neighbors still ranging intermittently.
- **Action:** **soft quarantine** (increase keep-out tube margin), no reassignment.
- **Confirmation:** require *multi-sensor corroboration* (see §2).
- **Authority:** cluster only.

### F2: Confirmed non-cooperative (dead bus / no comms, but trackable)
- **Signature:** N missed heartbeats + independent orbit estimate from neighbors; no authenticated packets.
- **Action:** **hard quarantine**: enlarge keep-out tube and create an **exclusion annulus** around predicted drift corridor.
- **Reassignment:** only **after hazard corridor decays below threshold** (probabilistic).
- **Authority:** cluster initiates quarantine; beacon must approve any cross-cluster boundary changes.

### F3: Fragmentation / high-uncertainty event
- **Signature:** sudden loss + unexpected photometric/radar signatures (if available) or multiple tracklets from neighbor optical.
- **Action:** **cluster-wide emergency density reduction**: temporary widening of element windows and mandatory conjunction screening cadence increase.
- **Reassignment:** prohibited until debris hypothesis cleared.
- **Authority:** beacon declares “debris mode” for affected region; cluster executes.

This taxonomy prevents the most common governance failure: treating F1/F2 like F0.

---

## 2) Failure detection and confirmation (minimize false positives without stalling)

You already have ≤10 ms time sync; use it to make failure confirmation *statistical* rather than binary.

### Recommended confirmation rule (cluster-local)
A node is **F2 Confirmed** when:
1) **Heartbeat timeout**: e.g., 3–5 consecutive missed heartbeats over T = 30–120 s (tunable to comms geometry), **and**
2) **Independent track**: at least **k-of-n neighbors** (e.g., k=3) produce consistent relative state (angles-only + occasional ranging) within residual bounds, **and**
3) **No authenticated intent**: no signed “safe-mode” / “hold” message.

A node is **F3 Suspected** when:
- last known state + observed tracklets produce **innovation residuals inconsistent with single-body propagation**, or there is **sudden brightness/attitude signature** inconsistent with the bus.

This rule is implementable on seL4: it’s a bounded-time state machine with explicit thresholds, not a heuristic “seems dead.”

---

## 3) Slot state machine: Quarantine → Lease → Deed

Model every slot as one of these states, with explicit transition authority:

1) **Occupied (Nominal)**
2) **Soft-Quarantined** (F1): keep-out tube inflation factor α₁ (e.g., 1.5–3×)
3) **Hard-Quarantined** (F2/F3): inflation α₂ (e.g., 5–20×) + drift corridor exclusion
4) **Lease-Available** (probabilistic clearance met): cluster may assign a *temporary lease* to a replacement node
5) **Deeded** (beacon catalog update): permanent owner recorded in master ephemeris registry

### Clearance criterion (the heart of “reclaim later”)
A quarantined slot becomes **Lease-Available** only when:
- the predicted conjunction probability between the failed object’s uncertainty ellipsoid and the slot’s keep-out tube falls below a strict threshold, e.g.  
  **P < 10⁻⁸ per day** for **M consecutive days** (M=3–7), *and*
- the drift corridor no longer intersects any neighboring slot tubes at the current density.

This avoids “reoccupy too early” events that consume ΔV across the cluster.

---

## 4) Authority and consensus: what Tier 2 can do alone vs what needs Tier 3

### Tier 2 (cluster) autonomous authority
Allowed without beacon approval:
- Declare F1/F2 locally (with quorum)
- Inflate keep-out tubes and impose **local virtual fences**
- Issue **local leases** for intra-cluster replacements *only when clearance criterion is met*
- Schedule local avoidance maneuvers and screening cadence changes

Consensus mechanism: **Raft-style leader + witness quorum** is sufficient here. You do *not* need PBFT unless you assume malicious nodes; your threat model reads more like crash faults + Byzantine only at the edges. Keep it lightweight.

### Tier 3 (beacon) registry authority
Required for:
- Any reassignment that changes **cluster boundary allocations**
- Any permanent “deed” (master catalog ownership)
- Any long-duration “debris mode” declaration spanning multiple clusters
- Any changes to slot geometry policy (tube sizes, element window definitions)

Beacon consensus: small-N (3–5) so you *can* do PBFT or HotStuff-like BFT if you want robustness against a compromised beacon, but operationally you’ll likely accept redundant authenticated beacons + majority signature.

---

## 5) ΔV-aware reassignment: make “migration” rare and cheap

Given 0.5–5 m/s/year/node, the governance protocol must **prefer logical reassignment over physical migration**:

- **Default action:** reassign *workload* (power routing / comms role) rather than moving a spacecraft.
- **Physical slot migration** only when it’s ΔV-cheap:
  - candidate replacement already near the orbital element window
  - transfer can be done with low-cost differential corrections (e.g., along-track phasing rather than plane change)

### Practical policy
- Each cluster maintains a small pool (e.g., 1–3%) of **“floaters”**: nodes allowed larger element windows specifically to backfill vacated slots with minimal ΔV.
- Cap the number of migrations per node-year (e.g., ≤1 planned migration/year unless emergency). This prevents slow ΔV bankruptcy.

---

## 6) Beacon catalog update mechanism: append-only, signed, and latency-bounded

You want the catalog to stay fresh without making it chatty or fragile.

### Data structure recommendation
- Use an **append-only Slot Event Log**:
  - `EVENT = {slot_id, event_type, subject_node_id, epoch, validity_interval, geometry_hash, signatures}`
- Cluster emits **LEASE** events; beacon emits **DEED / GLOBAL_QUARANTINE / POLICY** events.
- Nodes consume the log and maintain a local derived state (“current slot map”).

### Authentication
- Cluster coordinator signs lease events; require **m-of-n co-sign** from witnesses to prevent a single faulty coordinator from reallocating aggressively.
- Beacon events require **2-of-3** (or majority-of-beacons) signatures.

### Cadence
- Beacon broadcasts:
  - **high-rate deltas** (every ~10–60 s) for safety-critical quarantine declarations
  - **lower-rate deeds** (hourly/daily) for permanent reallocations and optimization

This matches the reality that safety changes must propagate fast; ownership can lag.

---

## 7) Quarantine geometry: “virtual fence” must be corridor-based, not just tube inflation

Simple tube inflation is insufficient because drift is anisotropic in heliocentric orbit.

Implement quarantine as:
- **Inflated keep-out tube** around last-known slot
- Plus a **predicted drift corridor** (time-tagged volume) derived from:
  - last known state covariance
  - worst-case unmodeled accelerations (SRP, attitude tumbling)
  - bounded ballistic coefficient uncertainty

Neighbors then plan avoidance against the corridor, not a static bubble. This reduces unnecessary ΔV while still bounding risk.

---

## 8) What I would simulate first (to de-risk the protocol)

1) **F1 false positive rate vs quarantine cost**  
   Tune heartbeat + k-of-n tracking thresholds to minimize “panic quarantines” that reduce packing density.

2) **Clearance criterion sensitivity**  
   How many days of low predicted probability are needed before leasing is safe at your density? This is where you win/lose ΔV.

3) **Coordinator failure during reallocation**  
   Verify that Raft leader loss mid-event cannot create split-brain slot ownership. Append-only event log + witness co-signing is the fix.

4) **Multi-failure bursts (solar storm / comm outage)**  
   Ensure the protocol degrades gracefully: widespread F1 should trigger soft quarantine and screening cadence increase, not mass reassignment.

---

## Opinionated bottom line

- **Do not** allow immediate reassignment on missed heartbeats. That’s how you burn ΔV and trigger cascades.
- **Do** let clusters autonomously quarantine and issue *temporary leases* once probabilistic clearance is met.
- **Do** reserve permanent ownership (“deeds”) and cross-cluster boundary changes for beacons via a signed append-only event log.
- **Do** encode this as a formally verifiable state machine (seL4-friendly), with explicit timers, quorums, and geometry hashes.

If you want, I can propose concrete parameter starting points (heartbeat intervals, α₁/α₂ inflation factors, k-of-n values, and clearance thresholds) consistent with your current navigation accuracy assumptions (±1 m to ≤5 km).