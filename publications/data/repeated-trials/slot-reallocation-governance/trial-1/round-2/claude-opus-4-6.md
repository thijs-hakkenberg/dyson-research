---
questionId: "rq-1-40"
questionSlug: "slot-reallocation-governance"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
roundNumber: 2
generated: "2026-02-24"
type: "discussion-response"
---

# Slot Reallocation Governance Protocol: Round 2 Refinement

## Framing

Round 1 produced strong convergence on several principles: quarantine-first philosophy, tiered authority split between Tier-2 (fast/local safety) and Tier-3 (slow/global registry), and the importance of treating dead-node trajectory characterization as the first-order problem. I agree with all of these. Rather than re-derive them, I want to push into the areas where Round 1 left ambiguity or made assumptions that deserve challenge, and propose concrete mechanisms where the prior discussion remained abstract.

I'll focus on five areas: (1) why "retire, don't reassign" is correct but incomplete, (2) the quarantine geometry problem that nobody fully solved, (3) a specific distributed consensus mechanism for Tier-2 decisions, (4) the ΔV economics that constrain everything, and (5) the beacon catalog data structure.

---

## 1. Retire-and-Commission vs. Reassign: Getting the Semantics Right

Claude Opus 4.6's insight that "no slot is ever reassigned—slots are retired and new slots are commissioned" is elegant and I endorse it for the formal verification layer. On the seL4 kernel, slot identity should be immutable: a slot is a tuple `(slot_id, orbital_element_window, keep_out_tube, epoch, expiry)` that is created once and eventually marked `RETIRED`. A replacement node occupying a similar orbital volume gets a *new* slot_id with a *new* epoch.

However, this creates a practical problem at scale over 50 years. With 10–90 failures/year across Phase 1 and eventual scaling to 10,000+ nodes, the slot registry accumulates thousands of retired entries. More critically, the orbital element windows of retired slots represent *physically desirable locations*—they were chosen for optimal packing density and energy collection geometry. A pure retire-and-commission model must include a mechanism for **slot template inheritance**: the new slot's orbital element window can be derived from the retired slot's parameters, adjusted for any drift or updated conjunction analysis, but carrying forward the geometric intent.

I propose a three-state slot lifecycle:

- **`ACTIVE`** → normal operations, node occupying the slot broadcasts ephemeris
- **`QUARANTINED`** → slot's keep-out tube is expanded, no node may occupy, trajectory of former occupant being characterized
- **`RETIRED`** → terminal state; slot parameters archived as a **template** available for new slot commissioning

The template inheritance mechanism is what makes this operationally tractable. Without it, every replacement requires full swarm-level optimization to find a new orbital element window—computationally expensive and unnecessary when the retired slot's geometry was already validated.

---

## 2. Quarantine Geometry: The Expanding Envelope Problem

All Round 1 responses endorsed quarantine zones but none specified the geometry rigorously. This is where the physics gets hard.

A failed node in heliocentric orbit doesn't just "drift"—its trajectory diverges from the assigned orbital element window at a rate determined by its failure mode. A node that loses attitude control but retains orbital velocity diverges slowly (solar radiation pressure perturbations dominate, ~10⁻⁷ m/s² for a lightweight panel). A node that fires a thruster during failure diverges fast (even 0.1 m/s impulse creates ~3 km/year drift in semi-major axis).

The quarantine zone must therefore be **time-dependent and failure-mode-dependent**:

**Conservative envelope (Class B/C sudden failure, unknown state):**
- At detection (T+0): expand keep-out tube to 2× nominal radius
- At T+24h: propagate last known state vector with uncertainty covariance growing at worst-case rate (assume 0.5 m/s uncharacterized ΔV in random direction)
- At T+72h: if no radar/optical tracking data refines the estimate, expand to 3σ uncertainty ellipsoid
- At T+7d: beacon spacecraft should have sufficient tracking arcs to collapse uncertainty to ±100m; quarantine zone can shrink to refined trajectory ± margin

**Key quantitative constraint**: The keep-out tube nominal radius in the consensus ranges from ±1m to ≤5km depending on navigation accuracy model. For automotive-grade GPS-denied heliocentric operations, I'll assume ±500m nominal keep-out radius as a working figure. The worst-case quarantine expansion at T+72h for an uncharacterized 0.5 m/s impulse is approximately ±43 km (0.5 m/s × 259,200s ≈ 130 km, but constrained to the orbital plane). This means **quarantine zones can encompass multiple adjacent slots**, forcing neighboring nodes into temporary avoidance configurations.

This cascading quarantine effect is the most dangerous failure mode for swarm coherence. I recommend that slot adjacency graphs (Research Direction 2) be constructed with **quarantine propagation depth** as the primary metric: for each slot, calculate how many neighbors fall within the worst-case 72-hour quarantine envelope. Slots with quarantine depth >5 are **critical slots** requiring enhanced monitoring (higher heartbeat frequency, redundant communication paths).

---

## 3. Distributed Consensus for Tier-2 Slot Decisions

The prior round mentioned PBFT and Raft but didn't commit. I'll be specific: **use Raft, not PBFT, with modifications.**

Rationale:
- PBFT tolerates Byzantine faults (malicious nodes) but requires 3f+1 nodes to tolerate f failures, and message complexity is O(n²). For ~100-node clusters, this means ~10,000 messages per consensus round. With the inter-satellite link bandwidth constraints of small satellites, this is expensive.
- Raft tolerates crash faults only, requires 2f+1 nodes, and has O(n) message complexity. Since we're not defending against malicious nodes (these are our own satellites, and per-node identity keys provide authentication), Byzantine tolerance is unnecessary overhead.
- The rotating coordinator architecture already maps naturally to Raft's leader election mechanism.

**Modified Raft for Slot Governance:**

The cluster coordinator serves as Raft leader. Slot state transitions (`ACTIVE` → `QUARANTINED`, `QUARANTINED` → `RETIRED`) are log entries replicated to a quorum of cluster members. I recommend a **quorum of 51% of currently-ACTIVE nodes in the cluster**, not 51% of all assigned nodes—this prevents a cluster with multiple simultaneous failures from losing quorum.

Critical modification: **split-brain prevention across cluster boundaries.** When a quarantine zone spans two clusters, both cluster coordinators must agree on the quarantine geometry. I propose a lightweight **cross-cluster handshake**: the initiating coordinator sends a signed quarantine proposal to the adjacent coordinator, who must ACK within 60 seconds or the initiating coordinator escalates to Tier-3 (beacon). This keeps the common case fast (intra-cluster, milliseconds to seconds) while handling the edge case (cross-cluster, seconds to minutes) without requiring beacon involvement for every decision.

Beacon spacecraft (Tier-3) serve as the **Raft log archive and conflict resolver**. They don't participate in normal consensus rounds but receive all committed log entries and maintain the canonical slot registry. If two clusters produce conflicting slot state transitions (possible during communication partitions), the beacon resolves by timestamp ordering with the cluster-coordinator's signed epoch.

---

## 4. ΔV Economics of Slot Migration

This is the binding constraint that Round 1 underweighted. Let me put numbers on it.

**Slot migration cost model:**
- Moving to an adjacent slot (one slot-width lateral displacement): For ±500m keep-out radius with ~2km slot pitch, a Hohmann-like phasing maneuver costs approximately 0.01–0.05 m/s depending on orbital period.
- Moving across a cluster (~50 slot-widths, ~100km): approximately 0.5–2.0 m/s.
- Moving between clusters: likely exceeds annual ΔV budget; effectively impossible without dedicated transfer ΔV allocation.

**Implication**: With 0.5–5 m/s/year total budget and station-keeping consuming a baseline ~0.1–0.3 m/s/year, a node can afford **at most 1–2 intra-cluster migrations per year** and **zero inter-cluster migrations** without compromising its operational lifetime.

This means replacement nodes must be **pre-positioned** or **launched into approximately correct orbits**. The governance protocol should maintain a **replacement queue**: 2–5% of nodes per cluster designated as "warm spares" occupying slightly offset slots that require minimal ΔV to migrate into vacated positions. This is a direct trade against energy collection capacity (spare nodes are producing power but are suboptimally positioned) but is essential for maintaining swarm density.

**Annual reassignment capacity per cluster (~100 nodes, 2–5 spares):**
- 2–5 slot replacements per year from pre-positioned spares
- Additional replacements require new node launches into the cluster's orbital regime

Given 10–90 failures/year across 10–30 clusters in Phase 1, this budget is tight but feasible if failures are distributed roughly uniformly. **Correlated failures** (solar storm, manufacturing defect batch) could exhaust a cluster's spare capacity, requiring Tier-3 beacon coordination to redistribute spares from adjacent clusters—but this hits the inter-cluster migration ΔV wall. This is a strong argument for **manufacturing diversity** and **spatial distribution of production batches** across clusters.

---

## 5. Beacon Catalog Data Structure

The ephemeris catalog broadcast is the single point of truth for collision avoidance. I propose a specific format:

**Slot Record (per entry, ~128 bytes):**
```
slot_id:          uint64    (8B)
state:            enum8     (1B) {ACTIVE, QUARANTINED, RETIRED}
epoch:            uint64    (8B) - TAI microseconds
orbital_elements: float64×6 (48B) - Keplerian elements at epoch
covariance_diag:  float32×6 (24B) - diagonal of covariance matrix
keepout_radius:   float32   (4B) - meters
quarantine_radius: float32  (4B) - meters (0 if not quarantined)
node_id:          uint64    (8B) - occupying node (0 if vacant)
auth_signature:   bytes     (23B) - Ed25519 truncated signature
```

**Catalog broadcast cadence:**
- Full catalog: every 3600 seconds (1 hour). For 3,000 slots × 128 bytes = 384 KB. At even modest 1 kbps inter-satellite link rates, this takes ~51 minutes—too long. **Delta compression is mandatory.** Broadcast full catalog every 24 hours; broadcast deltas (changed records only) every 300 seconds.
- Emergency amendments (quarantine declarations): broadcast immediately on priority channel, repeated 3× over 30 seconds.

**Authentication**: Each slot state transition is signed by the authorizing cluster coordinator's Ed25519 key. Beacon spacecraft countersign when they incorporate the change into the canonical catalog. Nodes reject unsigned or improperly signed catalog entries—this prevents a malfunctioning node from corrupting the shared ephemeris.

---

## Summary Recommendation

The governance protocol is: **detect conservatively, quarantine aggressively, retire cleanly, commission from templates, and pre-position spares.** Authority is split: Tier-2 owns safety-critical quarantine decisions with Raft consensus, Tier-3 owns the canonical registry and resolves conflicts. The ΔV budget is the hard constraint that limits reassignment to pre-positioned spares within clusters, making spare allocation strategy as important as the governance protocol itself. All of this must be formally verified on the seL4 kernel, which the retire-don't-reassign semantics and explicit state machine make tractable.