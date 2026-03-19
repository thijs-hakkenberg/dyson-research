---
questionId: "rq-1-40"
questionSlug: "slot-reallocation-governance"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
roundNumber: 2
generated: "2026-02-07"
type: "discussion-response"
---

# Slot Reallocation Governance Protocol: Round 2 Refinement

## Building on the Emerging Consensus

Round 1 produced remarkable convergence on several foundational principles: quarantine-first philosophy, append-only slot state machines, and tiered authority with cluster coordinators handling most decisions autonomously. I want to push beyond these agreements into the unresolved engineering details that will determine whether this protocol actually works at scale across a 50-year operational lifetime.

My central thesis: **The slot reallocation protocol is not primarily a consensus algorithm problem—it is a trajectory uncertainty propagation problem with a governance wrapper.** The protocol's correctness depends entirely on how accurately we can predict where a failed node will be over the next hours, days, and weeks. Everything else—authority hierarchies, state machines, catalog updates—is scaffolding around that core orbital mechanics challenge.

---

## 1. The Trajectory Uncertainty Problem Drives Everything

When a node fails, the critical unknown is its future trajectory. In heliocentric orbit, a dead satellite doesn't just "drift"—its behavior depends on failure mode:

- **Attitude-stable, thruster-safe failure**: The node follows a ballistic Keplerian orbit. Trajectory prediction is excellent for weeks to months. Quarantine zone can be tight (tens of meters expanding slowly).
- **Tumbling with residual angular momentum**: Solar radiation pressure torques become stochastic. Trajectory diverges from nominal over days. For a ~10 m² satellite at ~0.5 AU, SRP acceleration is ~10⁻⁵ m/s², which accumulates to ~0.9 m/s over a day—a significant fraction of the annual ΔV budget for neighboring nodes forced to avoid it.
- **Thruster stuck-on or leaking**: Worst case. Uncontrolled ΔV can push the node through multiple keep-out tubes within hours.

**Recommendation**: The failure classification taxonomy must map directly to trajectory uncertainty growth rates, not just communication status. A node that stops communicating but is tracked by neighbors via inter-satellite ranging (ISR) and shows stable ballistic trajectory is fundamentally different from one exhibiting anomalous acceleration. The state machine needs a **TRACKED-DEAD** state distinct from **UNTRACKED-DEAD**, with radically different quarantine geometries.

### Passive Tracking Requirement

I strongly advocate that every node must be passable trackable by its neighbors. This means:

- **Corner cube retroreflectors** (mass: ~50g each, 4 per satellite) enabling laser ranging from adjacent nodes at distances up to 50 km. This is mature technology from lunar laser ranging heritage, scaled down.
- **RF beacon in fail-safe mode**: Even after primary system failure, a simple crystal oscillator beacon powered by a dedicated small solar cell (independent of main power bus) transmits a carrier signal for Doppler tracking. Mass penalty: ~100g. Power: ~100 mW. This is the satellite equivalent of an aircraft's ELT.

These two systems allow neighbors to maintain trajectory estimates on a dead node for weeks, collapsing the uncertainty that drives quarantine zone sizing. Without passive tracking, quarantine zones must grow conservatively, potentially consuming 5–15 adjacent slots. With it, quarantine can be limited to 1–3 slots.

---

## 2. Quarantine Zone Geometry: A Concrete Model

Round 1 discussions referenced expanding quarantine zones but didn't specify the geometry. I propose:

**Quarantine zones are defined as inflated keep-out tubes along the predicted trajectory of the failed node**, not as static spherical exclusion volumes around the original slot.

The inflation factor is a function of:
- Time since last confirmed state vector (t)
- Trajectory uncertainty class (ballistic, tumbling, thrusting)
- Whether passive tracking is available

For a ballistic dead node with passive tracking:
- Keep-out tube inflation: σ_cross-track × 3 (3-sigma), where σ grows as ~t² due to unmodeled perturbations
- Typical values: ±5 m at t=0, ±50 m at t=7 days, ±500 m at t=30 days

For an untracked tumbling node:
- Inflation dominated by SRP uncertainty: σ grows as ~½ a_SRP × t²
- At t=7 days: ±2.6 km cross-track uncertainty
- This is why passive tracking is non-negotiable—without it, quarantine zones consume enormous swarm volume

**The quarantine zone propagates with the failed node's predicted orbit, not fixed to the original slot location.** This is critical: the original slot becomes safe to reoccupy once the dead node has drifted sufficiently far, even if the dead node itself remains hazardous.

---

## 3. Authority Architecture: Resolving the Tier 2/Tier 3 Ambiguity

Round 1 correctly identified cluster coordinators (Tier 2) as the primary decision authority. I want to make the authority boundaries precise:

### Cluster Coordinator (Tier 2) Authority — Autonomous, No Approval Required:
- Transition any intra-cluster slot from NOMINAL → SUSPECT → QUARANTINED
- Size and propagate quarantine zones using local tracking data
- Command neighboring nodes to execute avoidance maneuvers up to **0.05 m/s per event** (10% of minimum annual ΔV budget as a hard cap per single reallocation event)
- Retire quarantined slots and mint replacement slots within the cluster's allocated orbital element window
- Broadcast updated local ephemeris to beacon spacecraft

### Beacon Spacecraft (Tier 3) Authority — Required For:
- **Cross-cluster quarantine propagation**: When a failed node's predicted trajectory crosses cluster boundaries (this will happen—cluster boundaries in orbital element space are not physical walls)
- **Slot minting that modifies cluster boundary definitions**: If a cluster needs to expand its orbital element window to accommodate internal reorganization
- **Conflict resolution**: When two cluster coordinators disagree about a quarantine zone in their shared boundary region
- **Catalog reconciliation**: Merging cluster-level ephemeris updates into the master catalog and rebroadcasting

### Ground Authority — Required For:
- Policy changes (modifying quarantine inflation parameters, ΔV caps)
- Authorizing depletion of more than 25% of any node's remaining lifetime ΔV budget for reallocation purposes
- Approving cluster topology changes (merging depleted clusters, splitting overgrown ones)

**Key design decision**: Beacon spacecraft do NOT need to approve routine intra-cluster slot retirements and replacements. This eliminates the latency bottleneck. Beacons learn about changes after the fact via cluster coordinator reports and reconcile the master catalog asynchronously. The safety case relies on cluster coordinators being conservative (quarantine-first), not on beacon approval being fast.

---

## 4. The ΔV Budget Problem Is the Binding Constraint

With 0.5–5 m/s/year, slot reallocation competes directly with stationkeeping. I've modeled the ΔV costs:

**Slot migration within a cluster**: For orbital element windows of ±1 km (a reasonable cluster slot spacing), migrating one slot position requires ~0.01–0.05 m/s depending on transfer time allowed. At 1–3% annual failure rate in a 100-node cluster, that's 1–3 migrations/year, costing the migrating node 0.01–0.15 m/s/year—manageable.

**Avoidance maneuvers for quarantine enforcement**: Neighbors of a failed node may need 0.01–0.1 m/s per event. With the passive tracking system keeping quarantine zones small, typically only 2–4 neighbors need to maneuver.

**The real danger**: Multiple correlated failures (e.g., a solar storm damaging several nodes in the same cluster simultaneously). If 5+ nodes fail in one cluster within a short period, the cumulative avoidance ΔV for surviving nodes could exceed 0.5 m/s—consuming an entire year's budget.

**Recommendation**: Implement a **cluster-level ΔV reserve policy**. Each node maintains a 20% ΔV reserve that can only be expended for collision avoidance, not routine stationkeeping. The cluster coordinator tracks aggregate reserve levels and escalates to beacon/ground if reserves drop below threshold. This is analogous to fuel reserves in aviation.

---

## 5. Distributed Consensus: Keep It Simple

Round 1 mentioned PBFT and Raft. I recommend **against** full Byzantine fault tolerance for slot reallocation. The threat model doesn't justify it:

- These are our own satellites running formally verified seL4 code, not adversarial nodes
- The failure mode is crash failures, not Byzantine behavior
- BFT protocols require 3f+1 nodes to tolerate f failures, imposing massive communication overhead in a 100-node cluster

Instead, use **Raft-style leader-based consensus** with the cluster coordinator as leader. If the coordinator fails, standard Raft leader election among surviving nodes selects a replacement. Slot state transitions require confirmation from the coordinator plus **2 independent witnesses** (nodes that can corroborate the failure detection via their own observations—missed heartbeats, passive tracking data).

This gives us crash fault tolerance with minimal message complexity: O(n) per decision rather than O(n²) for PBFT.

---

## 6. Catalog Update Data Structure

The beacon-broadcast ephemeris catalog amendment should be:

```
SlotStateUpdate {
  slot_id:          uint64    // globally unique, monotonically increasing
  epoch:            float64   // TDB seconds, synchronized to swarm clock
  state:            enum      // NOMINAL, SUSPECT, QUARANTINED, RETIRED, MINTED
  state_vector:     float64[6] // position + velocity at epoch (heliocentric)
  covariance:       float64[21] // upper triangle of 6×6 covariance matrix
  quarantine_params: float64[4] // inflation rate, class, tracking status, expiry
  authority_node:   uint32    // coordinator that authorized the change
  witness_nodes:    uint32[2] // corroborating nodes
  signature:        bytes[64] // Ed25519 signature from authority node
  sequence_number:  uint64    // per-cluster monotonic, enables ordering
}
```

Total: ~300 bytes per update. At 90 failures/year across the swarm, plus state transitions (each failure generates ~4 updates through the state machine), that's ~360 updates/year, or ~108 KB annually—trivially small for the communication system.

---

## Summary of Concrete Recommendations

1. **Add passive tracking hardware** (retroreflectors + fail-safe RF beacon) to every node—~150g mass penalty, enormous reduction in quarantine zone size
2. **Quarantine zones propagate with the dead node's predicted orbit**, not fixed to original slot position
3. **Cluster coordinators act autonomously** for intra-cluster events; beacons handle cross-cluster propagation and catalog reconciliation
4. **Raft consensus, not BFT**—the threat model is crash failures, not adversarial behavior
5. **20% ΔV reserve policy** per node, enforced by cluster coordinator, dedicated to collision avoidance
6. **Append-only slot state machine** (per Round 1 consensus): slots are retired and minted, never reassigned