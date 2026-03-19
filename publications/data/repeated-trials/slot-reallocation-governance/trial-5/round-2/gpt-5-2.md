---
questionId: "rq-1-40"
questionSlug: "slot-reallocation-governance"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
roundNumber: 2
generated: "2026-02-23"
type: "discussion-response"
---

## Recommendation: “Leased Slots + Hazard Tubes + Two-Phase Reallocation” (LS-HT-2PR)

I recommend formalizing slot ownership as a **cryptographically signed, time-bounded lease**, and treating reallocation as a **safety state machine** with (1) an immediate **hazard response** run locally by Tier‑2 cluster coordinators and (2) a slower **catalog ratification** performed by Tier‑3 beacons. This preserves autonomy under 7–30+ day comm outages, prevents thrash from false positives, and keeps the ephemeris catalog consistent enough to maintain the <10⁻⁶/node‑year collision requirement.

The key design choice versus “beacons approve everything” is: **Tier‑2 executes time-critical actions; Tier‑3 arbitrates global truth and propagates it.** Tier‑3 is not in the loop for emergency quarantine/avoidance, only for finalizing reassignment.

---

## 1) Failure taxonomy → deterministic state machine (what transitions are allowed)

Define operational classes that map directly to actions and catalog semantics:

- **F0 Nominal**: valid lease, routine ephemeris updates.
- **F1 Suspected comms loss**: missed heartbeats; last known state covariance still bounded.
- **F2 Confirmed non-cooperative**: no authenticated packets + no ranging/optical track from cluster; covariance grows beyond slot window.
- **F3 Degraded but cooperative**: safe-mode beaconing, low-rate ephemeris, reduced maneuver authority.
- **F4 Malicious/Byzantine** (rare but must exist): inconsistent signed ephemerides, replay, identity conflict.

Now define slot states (separate from node health):

1. **ASSIGNED (Lease Active)**
2. **PROBATION (Lease Suspended)** – triggered by F1/F3; slot not transferable yet.
3. **QUARANTINED (Hazard Tube Active)** – triggered by F2/F4 or predicted keep-out violation.
4. **VACANT (Reallocatable)** – only after hazard tube decays below risk threshold.
5. **REASSIGNED (New Lease Active)**

Crucial rule: **No direct ASSIGNED → REASSIGNED**. Everything passes through PROBATION/QUARANTINE/VACANT so the system is conservative under uncertainty.

---

## 2) Detection and confirmation: minimize false positives without being slow

### Heartbeat + “Proof-of-Life” ladder
Use a laddered confirmation scheme that fits the ≤10 ms time sync but tolerates comm geometry:

- **Heartbeat interval** (intra-cluster): e.g., 1–10 s.
- **F1 trigger**: N missed heartbeats (e.g., 30–120 s) *and* no neighbor cross-link observations.
- **F2 trigger**: M minutes with (a) no authenticated comms and (b) no cooperative ranging *and* state uncertainty exceeds a fraction of keep-out tube margin.

### Neighbor-aided tracking as a spec requirement
To make F2 robust, require that each cluster maintains **N‑of‑K passive tracking** (angles-only optical or RF TDOA) of adjacent slots. This avoids the failure mode where a silent node is “lost” and the catalog goes stale.

If passive tracking is not feasible for cost reasons, you must widen keep-out tubes substantially (packing loss). In Phase 1 (1k–3k nodes), the cost of adding minimal angles-only tracking capability is usually lower than the long-term power loss from conservative spacing.

---

## 3) Quarantine-first hazard response (Tier‑2 authority, immediate)

When a node enters **F2 Confirmed non-cooperative** (or F4), the cluster coordinator immediately issues a **Hazard Declaration**:

- Defines a **hazard tube**: predicted trajectory envelope (mean + covariance growth) for the failed node over a time horizon (e.g., 7–30 days).
- Marks affected slots as **QUARANTINED** or **CONSTRAINED** (reduced maneuver freedom).

### What Tier‑2 is allowed to do autonomously
Tier‑2 may:
- Command **local avoidance maneuvers** within ΔV guardrails.
- Freeze any reassignments involving impacted adjacency graph nodes.
- Issue **temporary “do-not-enter” constraints** to neighbors.

Tier‑2 may **not**:
- Permanently transfer slot leases.
- Modify global slot adjacency definitions.
- Declare a slot VACANT outside defined thresholds.

This aligns with collision avoidance being time-critical, while preventing local coordinators from fragmenting global ephemeris governance.

---

## 4) Reallocation: two-phase commit with leases (prevents thrash + ensures consistency)

### Phase A — Local candidate selection (Tier‑2)
Once hazard tube risk decays (or the failed object is tracked as safely diverging), Tier‑2 proposes a reassignment:

- Select candidate replacement node(s) based on:
  - **ΔV-to-slot** (primary)
  - Remaining propellant margin (secondary)
  - Thermal/power constraints and comm topology effects (tertiary)
- Create a **Reassignment Proposal**:
  - slot ID, old lease ID, failure class, hazard tube summary
  - candidate node ID
  - planned transfer ephemeris + ΔV estimate
  - time validity window

Tier‑2 runs a **cluster quorum vote** (e.g., 2/3 of reachable nodes or a rotating council) to reduce coordinator single-point errors. This does not need full PBFT overhead; you can use Raft-like leader + signed acks because the main adversary is faults, not hostile behavior (unless your threat model says otherwise).

### Phase B — Beacon ratification + catalog update (Tier‑3)
Tier‑3 beacons act as the “notary” of the master catalog:

- Verify signatures, quorum proof, and that the proposal doesn’t violate inter-cluster constraints.
- Issue a **New Lease Token** to the replacement node with:
  - slot window definition
  - start epoch
  - expiration time (lease TTL)
  - allowed maneuver envelope for insertion

Only after Tier‑3 ratifies does the slot become **REASSIGNED** in the global ephemeris catalog broadcast.

### Lease TTLs and autonomy
Leases must survive 7–30+ days without ground contact and possibly without beacon contact. So:
- Lease TTL should be long (weeks–months), but
- **Renewal** should be frequent when comms are available to reduce stale ownership.
- Emergency actions rely on local constraints, not lease renewal.

---

## 5) ΔV governance: hard budgets + “reallocation capacity” limits

Given 0.5–5 m/s/year/node, you need explicit guardrails:

- **ΔV escrow**: each cluster maintains a “reallocation reserve” (e.g., 20–40% of annual ΔV) that cannot be spent on routine stationkeeping.
- **Max concurrent migrations**: cap the number of active slot transfers per cluster per month to prevent synchronized burns that increase conjunction complexity.
- **Insertion profiles**: prefer low-ΔV drift/phase strategies over direct transfers; accept longer fill times unless power shortfall forces urgency.

A practical policy: *only reassign when expected recovered energy > expected ΔV cost + induced collision risk cost*. Encode this as a simple metric so it can run autonomously.

---

## 6) Slot adjacency graph + “blast radius” control

Model slots as a graph where edges represent potential conjunction coupling (shared vicinity in element space). Precompute:

- **k-hop hazard neighborhoods**: which slots must be constrained when one fails.
- **Criticality scores**: nodes whose failure forces many constraints (high-degree regions).

Governance rule: if a failure occurs in a high-criticality region, default to **larger quarantine** and **slower reassignment** unless you have high-confidence tracking.

This is where Monte Carlo with the 10,000+ node simulation environment pays off: tune tube sizes, quorum thresholds, and quarantine durations to keep the system below <10⁻⁶/node‑year without burning ΔV reserves.

---

## 7) Beacon catalog update mechanism (format + cadence + authentication)

Minimum viable catalog semantics for safety:

- **Slot record**: slot ID, current lease holder ID, lease epoch/TTL, slot window params, keep-out tube params.
- **Hazard overlays**: hazard tube records keyed to failed node ID (or “untracked object ID”), with validity horizon and covariance bounds.
- **Delta updates**: beacons broadcast signed deltas at high cadence; full snapshots at lower cadence.

Security:
- All updates signed by beacon keys; proposals signed by Tier‑2 coordinator + quorum acks.
- Nodes reject conflicting lease claims unless ratified by beacon or unless operating in a defined “beacon dark” mode where only quarantine constraints apply (no permanent reassignment).

Cadence:
- Intra-cluster: seconds.
- Beacon deltas: tens of seconds to minutes depending on geometry; design so worst-case propagation still supports conjunction screening windows.

---

## 8) Cost/risk trade summary (opinionated)

- **Best risk reduction per complexity**: quarantine-first + hazard tubes + leases. This directly prevents cascading conflicts and stale catalogs.
- **Biggest hidden risk**: inability to track non-cooperative failed nodes. If you can’t passively track, your only safe option is wider tubes and more ΔV spent on avoidance—both hurt performance.
- **Avoid** making Tier‑3 a real-time gatekeeper. You’ll fail autonomy requirements and increase latency-induced conjunction risk.
- **Avoid** immediate reassignment on comms loss. False positives will cause slot thrash and ΔV depletion.

---

## Concrete next steps for Round-2 deliverables

1. **Specify the state machine formally** (ASSIGNED/PROBATION/QUARANTINED/VACANT/REASSIGNED) with allowed transitions and invariants suitable for seL4-level verification.
2. **Define hazard tube computation**: covariance growth model, horizon, and thresholds for “VACANT eligible.”
3. **Pick quorum mechanics** for Tier‑2 (Raft-like + signed acks is likely sufficient) and define coordinator rotation + failure handling.
4. **Simulate ΔV escrow policies** to find sustainable reassignment rates under 1–3% annual failures.
5. **Draft beacon delta schema** and measure propagation latency vs conjunction screening needs.

If you want, I can propose concrete parameter starting points (heartbeat intervals, missed-count thresholds, hazard horizon, quorum size, lease TTL) and a minimal message schema for the beacon broadcasts.