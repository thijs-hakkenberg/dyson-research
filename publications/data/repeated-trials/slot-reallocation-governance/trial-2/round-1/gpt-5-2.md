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

A workable protocol has to do three things simultaneously: (1) prevent a drifting/unknown object from driving conjunction risk above 10⁻⁶ node‑year, (2) keep the ephemeris catalog “fresh enough” that distributed screening remains valid, and (3) avoid burning the limited ΔV budget (0.5–5 m/s/yr) on churn. The core design choice I recommend is:

**Tier‑2 (cluster) can autonomously quarantine and perform *temporary* intra‑cluster reallocations; Tier‑3 (beacons) ratify and publish *authoritative* slot ownership changes to the master catalog on a slower cadence.**  
This split keeps time‑critical safety actions local while preserving a single source of truth for long-lived assignments.

---

## 1) Failure classification taxonomy (what triggers what)

Use a small taxonomy with explicit thresholds and “actions allowed” per tier. Keep it simple enough to formally verify on seL4 and to implement consistently across thousands of nodes.

### A. Graceful exit (cooperative)
**Signature:** Node broadcasts signed “decommission/retire” intent + last state vector + predicted drift envelope.  
**Confidence:** High immediately.  
**Actions:**
- Tier‑2: immediate slot release + controlled handover window.
- Tier‑3: publish authoritative reassignment after a short hold (e.g., 1–3 beacon cycles).

### B. Comms loss (potential false positive)
**Signature:** missed heartbeats but neighbors still see optical/radar track or passive ranging returns; or link metrics indicate channel outage.  
**Confidence:** Medium; can be false positive.  
**Actions:**
- Tier‑2: **do not reassign**. Mark slot “degraded”; widen keep‑out tube margins locally; increase screening frequency.
- Tier‑3: annotate catalog with “uncertain control status” + covariance inflation.

### C. Sudden failure / dead bus (non-cooperative)
**Signature:** missed heartbeats + no maneuver acknowledgments + track indicates ballistic motion inconsistent with stationkeeping.  
**Confidence:** High after confirmation window.  
**Actions:**
- Tier‑2: immediate **quarantine** of the slot and adjacent risk region; initiate local avoidance rules.
- Tier‑3: publish “hazard object” entry (failed node as tracked debris-like object) with inflated covariance; freeze reassignment until drift is bounded.

### D. Partial degradation (navigation or propulsion degraded)
**Signature:** node still communicates but reports degraded GN&C, low thrust, poor attitude control, or increasing ephemeris residuals.  
**Confidence:** High.  
**Actions:**
- Tier‑2: reclassify node to a “wide window” mode; reduce its local priority; optionally migrate it to a low-density buffer region if ΔV allows.
- Tier‑3: catalog update; may trigger planned replacement.

**Key point:** Only category A triggers “fast reassignment.” Category C triggers “fast quarantine,” not reassignment.

---

## 2) Detection and confirmation logic (latency vs false positives)

You need deterministic thresholds that balance false positives against collision risk. I recommend a two-stage confirmation:

### Stage 1: Local suspicion (Tier‑2, seconds–minutes)
- Heartbeat expected at fixed cadence (e.g., 1–10 s within cluster; whatever your comms allow).
- **Suspect** after N₁ missed heartbeats (e.g., 3–10), but take only *non-destructive* actions: increase screening, widen keep-outs, request neighbor observations.

### Stage 2: Confirmed status (Tier‑2 + corroboration, minutes–hours)
Confirm failure state if **any two** of the following are true:
1) N₂ missed heartbeats (e.g., 30–300, depending on cadence),  
2) no response to directed challenge/nonce (prevents spoofing),  
3) independent track indicates noncompliance (ballistic drift or no stationkeeping),  
4) neighbor-to-neighbor ranging/angles-only solution diverges from reported ephemeris beyond threshold.

Then Tier‑2 can assert “confirmed failed” and trigger quarantine. **Reassignment still waits for Tier‑3 ratification unless it is a temporary local swap** (see below).

This aligns with your autonomy constraint (7–30+ days without ground) and uses the existing beacon-broadcast catalog concept as the distributed truth mechanism.

---

## 3) Slot adjacency graphs and “blast radius” modeling

Treat slots as a graph where edges represent conjunction coupling under your keep-out tube geometry and navigation error model. The governance protocol should be parameterized by graph metrics:

- **k-hop risk neighborhood:** nodes whose keep-out tubes can be violated within T hours given worst-case differential drift of a failed object.
- **Criticality score:** expected ΔV cost + expected collision probability increase if the slot becomes uncertain.

Use this graph in two ways:
1) **Quarantine sizing:** quarantine region = 1–k hops depending on failure class and covariance growth rate.  
2) **Replacement selection:** choose replacement candidates that minimize migration ΔV and do not traverse high-degree regions.

This is exactly where your 10,000+ node Monte Carlo environment pays off: you can empirically tune k, quarantine duration, and catalog update cadence to keep collision probability <10⁻⁶ without excessive maneuvering.

---

## 4) Governance: who can do what (and when)

### Tier‑2 Cluster Coordinator (fast safety authority)
Allowed actions (autonomous, no beacon approval required):
- Declare **temporary quarantine zones** in cluster coordinates (time-bounded).
- Issue **local avoidance advisories** and “do not enter” constraints.
- Execute **temporary slot borrowing**: a node may occupy a neighbor’s window *only if* both windows are flagged “temporary” and the coordinator publishes a signed local amendment with an expiry time.

Not allowed:
- Permanent slot ownership change in the master catalog.
- Cross-cluster reassignment without beacon mediation.

### Tier‑3 Beacon/Relay (slow authority / global consistency)
Responsibilities:
- Maintain the **authoritative ephemeris catalog** and slot ownership ledger.
- Ratify permanent reassignment after:
  - quorum evidence from Tier‑2 (see consensus below),
  - drift bounded enough to define stable keep-outs,
  - and conflict checks across cluster boundaries.

This is the cleanest way to resolve the ambiguity you flagged: Tier‑2 handles immediate safety; Tier‑3 handles long-term consistency.

---

## 5) Consensus protocol recommendation (pragmatic, not maximal)

You mentioned PBFT/Raft. Given the environment (radiation, comms dropouts, 1–3% annual failures, and long autonomy), I recommend:

- **Within a cluster (~100 nodes): use a Raft-like leader election for coordinator + signed append-only “cluster event log.”**  
  Raft is simpler to verify and operate than PBFT, and your threat model is more “crash fault + intermittent comms” than “Byzantine,” assuming strong per-node identity keys and hardware-rooted signing.

- **For malicious/spoof resistance:** rely on cryptographic authentication and challenge-response, plus beacon cross-checking. If you truly expect Byzantine behavior, do PBFT only at Tier‑3 among 3–5 beacons (small N), not at Tier‑2.

**Quorum rule for a confirmed failure report:** coordinator + M independent witnesses (e.g., 3–7) providing signed evidence (missed heartbeat logs, ranging residuals, optical tracks). This reduces false positives and makes spoofing harder.

---

## 6) Quarantine vs reassignment: default to quarantine, reassignment is staged

### Immediate response (minutes–hours)
- **Quarantine the failed node’s slot** plus a risk corridor based on predicted drift and covariance growth.
- Inflate covariance in the catalog entry for the failed object.
- Increase screening cadence locally; avoid “chain reaction” maneuvers by using a **priority rule** (e.g., only nodes within the predicted conjunction set maneuver; others hold).

### Stabilization (hours–days)
- Track the failed object until its motion is predictable enough (ballistic with bounded uncertainty).
- Shrink quarantine as uncertainty collapses.

### Reassignment (days–weeks)
- Only after quarantine shrinks to a stable boundary do you allow a replacement node to migrate into the orphaned slot.
- If power output demands faster recovery, allow **temporary occupancy** of the energy-collection role by a nearby node with minimal ΔV, but keep it logically distinct from permanent slot ownership.

This staging is what prevents cascading conflicts: you don’t rush a new node into a region with an uncontrolled object.

---

## 7) ΔV-aware reassignment policy (hard constraint)

With only 0.5–5 m/s/year, you must treat reassignment as a scarce resource. A good policy:

1) **Local-first replacement:** pick the nearest node (in orbital element space) that can reach the slot with ΔV below a cap (e.g., ≤0.1–0.2 m/s for the maneuver).  
2) **Annual ΔV envelope:** each cluster maintains a “ΔV bank” for governance maneuvers; if depleted, you accept reduced packing efficiency rather than risking depletion.  
3) **Batch migrations:** do not constantly reshuffle. Accumulate orphaned slots and perform periodic optimization (monthly/quarterly) unless safety requires immediate action.

This matches the reality that most failures should not force immediate migration; they force quarantine and catalog updates.

---

## 8) Beacon catalog update mechanism (data + cadence)

### Data structure (minimum viable)
For each node/slot:
- Slot ID + owner node ID (or “unassigned/quarantined”)
- Orbital element window definition + keep-out tube parameters
- State vector + covariance (or bounded set)
- Control status enum (nominal/degraded/comms-loss/failed)
- Validity interval + sequence number
- Signatures: cluster coordinator + beacon

### Cadence
- **Routine broadcast:** e.g., every 1–10 minutes (tunable).  
- **Event-driven delta updates:** immediate on quarantine declarations and confirmed failures (small deltas, not full catalog).  
- Nodes cache last K versions; reject stale updates via monotonic sequence numbers.

Security: per-node identity keys, coordinator signing, beacon countersigning for authoritative changes. This is compatible with formal verification constraints if you keep parsing and validation small and deterministic.

---

## 9) Cost/risk notes (opinionated)

- **Biggest operational risk:** false-positive failure declarations causing unnecessary quarantines and ΔV burn. Mitigation: two-stage confirmation + multi-witness evidence.
- **Biggest safety risk:** treating a dead node as “just an empty slot.” It is not empty; it’s an uncontrolled object. Default quarantine.
- **Biggest architecture risk:** trying to run heavy BFT at Tier‑2. It will increase complexity and verification burden without proportional safety benefit if your primary faults are crash/comm loss.

---

## What I would prototype first (to retire key uncertainties)

1) **Cluster event log + quarantine workflow** on seL4: implement suspicion→confirmed→quarantine→shrink→reassign state machine.  
2) **Adjacency-graph Monte Carlo**: tune quarantine size and catalog cadence to stay <10⁻⁶ node‑year with realistic covariance growth.  
3) **ΔV accounting simulator**: show how many reassignments/year are feasible under 0.5 vs 5 m/s/year and what batching policy minimizes churn.  
4) **Beacon delta-catalog propagation test**: measure time-to-consistency across clusters with seconds–minutes latency and intermittent links.

This protocol keeps safety actions autonomous and fast, preserves a coherent master ephemeris catalog, and explicitly respects ΔV scarcity—while remaining implementable and verifiable in the Project Dyson software constraints.