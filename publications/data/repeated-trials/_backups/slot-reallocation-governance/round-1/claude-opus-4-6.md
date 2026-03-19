---
questionId: "rq-1-40"
questionSlug: "slot-reallocation-governance"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
roundNumber: 1
generated: "2026-02-07"
type: "discussion-response"
---

# Slot Reallocation Governance Protocol: A Concrete Architecture

## Executive Summary

I recommend a **tiered-authority, quarantine-first** governance model where slot reallocation operates as a state machine with formally verified transitions, executed primarily at the cluster coordinator level (Tier 2) with beacon oversight (Tier 3) limited to cross-cluster reassignments and catalog reconciliation. The core design principle: **no slot is ever reassigned—slots are retired and new slots are minted**. This eliminates an entire class of state synchronization bugs and makes the protocol append-only, which is dramatically easier to formally verify on the seL4 kernel.

---

## 1. Failure Classification Taxonomy and Detection

The protocol begins with detection, and detection must be conservative. I propose four failure classes with distinct response timelines:

**Class A – Graceful Decommission**: Node self-reports impending failure (battery degradation, reaction wheel desaturation approaching limits, thermal exceedance). The node broadcasts a structured `SLOT_RELINQUISH` message with its final best-estimate ephemeris and predicted drift trajectory. Response: immediate slot retirement, no quarantine needed. This is the easy case and should be the *designed-for* case—every node's end-of-life software should attempt graceful decommission.

**Class B – Sudden Silent Failure**: Node stops heartbeating. Confirmation requires **3 consecutive missed heartbeats from at least 2 independent neighbors**, with heartbeat intervals of 60 seconds. This gives a 3-minute detection floor. The two-neighbor requirement guards against false positives from single-link communication failures. Response: slot enters quarantine immediately.

**Class C – Erratic Behavior**: Node transmits but with inconsistent ephemeris, anomalous thrust commands, or authentication failures. This is the most dangerous class because the node may actively maneuver into neighboring keep-out tubes. Response: neighbors treat the node's keep-out tube as **expanded by 2×** and the cluster coordinator broadcasts a `SLOT_SUSPECT` alert. If erratic behavior persists for 10 minutes, escalate to Class B treatment.

**Class D – Communication Partition**: Multiple nodes in a region become unreachable simultaneously, suggesting a communication failure rather than mass hardware failure. Response: **no slot changes**. Nodes on both sides of the partition continue operating within their assigned orbital element windows. Reconciliation occurs when communication is restored. This is critical—partitions must not trigger cascading reassignments.

The detection signatures map directly to onboard state machine transitions that can be formally verified. Each transition requires cryptographically signed attestations from the detecting nodes, creating an auditable chain.

---

## 2. The Quarantine-First Protocol

When a Class B or C failure is confirmed, the failed node's slot enters a **quarantine state** with the following properties:

- The slot's keep-out tube is **expanded by 3×** in the ephemeris catalog, effectively creating a buffer zone. With nominal keep-out tubes of ±1 m to ±5 km (depending on navigation accuracy regime), this expansion is geometrically tractable.
- Adjacent nodes are notified to bias their station-keeping toward the *far side* of their own orbital element windows, away from the quarantined slot. This costs ΔV but is a small, predictable expenditure—I estimate 0.01–0.05 m/s per event for immediate neighbors, based on typical station-keeping correction magnitudes.
- The cluster coordinator begins tracking the failed node passively (if still radar/optically observable by neighbors) or propagating its last-known state forward using SGP4-class or higher-fidelity orbit prediction.

**Quarantine duration**: minimum 72 hours, maximum 30 days. The 72-hour floor allows sufficient tracking to characterize the failed node's actual trajectory to within the expanded keep-out tube with high confidence. The 30-day ceiling aligns with the autonomous operation window—if ground contact occurs within that window, human operators can review the quarantine disposition.

After quarantine, the slot transitions to **retired**. It is never reused with the same slot ID. A new slot may be minted at or near the same orbital elements, but it receives a new identifier, new authentication keys, and a fresh entry in the ephemeris catalog. This append-only approach is the single most important architectural decision in the protocol.

---

## 3. Authority Hierarchy: Who Decides What

**Cluster coordinators (Tier 2) have full authority for:**
- Declaring quarantine on slots within their cluster
- Expanding keep-out tubes for quarantined slots
- Directing adjacent nodes to bias station-keeping
- Retiring quarantined slots after the minimum quarantine period
- Minting new slots within their cluster's allocated orbital volume for replacement nodes

**Beacon spacecraft (Tier 3) have exclusive authority for:**
- Cross-cluster slot operations (when a failed node's drift trajectory crosses cluster boundaries)
- Reconciling the master ephemeris catalog after communication partitions
- Allocating new orbital volume to clusters (rebalancing after multiple failures deplete a cluster)
- Resolving conflicting quarantine declarations (if two clusters both claim authority over a boundary-region slot)

This division is clean and minimizes beacon involvement in routine operations. With 10–90 failures per year across 10–30 clusters, each cluster handles 0.3–9 failures annually—roughly one every 1–12 months. This is well within the capacity of a cluster coordinator running on the specified rad-tolerant processor (LEON4-class or similar).

**Consensus mechanism**: For intra-cluster decisions, I recommend a **simplified Raft protocol** rather than full PBFT. The threat model within a cluster is hardware failure, not Byzantine behavior—nodes have no economic incentive to lie about slot states, and authentication keys prevent spoofing. Raft is simpler to implement, easier to formally verify, and requires only a majority quorum. With ~100 nodes per cluster, a quorum of 51 is robust against simultaneous multi-node failures. The cluster coordinator acts as Raft leader; if the coordinator itself fails, standard Raft leader election promotes a successor.

For cross-cluster decisions requiring beacon involvement, I recommend a **two-phase commit** with the beacon as coordinator. Phase 1: affected cluster coordinators propose their local changes. Phase 2: beacon validates consistency, resolves conflicts, and broadcasts the committed catalog update. Latency for this is seconds to low minutes, acceptable for non-emergency cross-cluster operations.

---

## 4. ΔV Budget Analysis for Slot Migration

This is the binding constraint on reassignment frequency. Let me work through the numbers:

**Station-keeping bias during quarantine**: ~0.01–0.05 m/s per event for 4–8 adjacent nodes. Annual cost for a cluster experiencing 3 failures/year: 0.03–0.15 m/s per affected node. This is 1–30% of the low end of the annual ΔV budget (0.5 m/s/year). Manageable but not negligible.

**Replacement node migration to new slot**: This depends critically on where the replacement comes from. I strongly recommend **pre-positioning spare nodes** at cluster boundaries rather than migrating operational nodes. A spare node parked 10–50 km from the target slot in a similar heliocentric orbit requires approximately 0.1–0.5 m/s for the transfer, depending on urgency (faster transfer = more ΔV). If we budget 1 spare per 20 operational nodes (5% spares), a cluster of 100 nodes carries 5 spares, sufficient for ~2 years of average failure rates before resupply.

**Critical insight**: Slot migration of *operational* nodes should be avoided entirely. Moving Node X into the slot vacated by Node Y means Node X's original slot is now vacant, creating a cascade of moves. The spare-node approach eliminates this cascade. The ΔV cost is borne entirely by the spare, which has a full propulsion budget available.

**Annual reassignment ΔV budget per cluster**: I recommend reserving 15% of each node's annual ΔV budget for failure-response maneuvers (station-keeping biases, emergency avoidance). For spare nodes, 50% of their first-year budget is allocated to migration. This yields a sustainable system through the 50-year lifetime with periodic spare replenishment.

---

## 5. Beacon Catalog Update Mechanism

The ephemeris catalog amendment structure should be:

```
SlotUpdate {
    update_id:      uint64    // monotonically increasing, globally unique
    update_type:    enum      // QUARANTINE, RETIRE, MINT, MODIFY_KEEPOUT
    slot_id:        uint64    // affected slot (old ID for retire, new for mint)
    epoch:          float64   // update effective time (TAI seconds)
    orbital_window: OEW[6]    // orbital element window bounds
    keepout_params: KOT[3]    // keep-out tube dimensions
    authority:      uint32    // issuing cluster coordinator ID
    attestations:   Sig[N]    // Raft quorum signatures
    beacon_ack:     Sig       // beacon countersignature (if cross-cluster)
}
```

**Broadcast cadence**: Catalog deltas broadcast every 60 seconds by cluster coordinators to local nodes. Full catalog snapshots broadcast by beacons every 3600 seconds. Delta compression keeps per-update messages under 256 bytes, well within the inter-satellite link bandwidth.

**Authentication**: Each node holds a unique Ed25519 key pair provisioned at manufacture. Cluster coordinators hold cluster-level keys. Beacons hold root keys. Catalog updates require valid signatures matching the authority hierarchy. This prevents a compromised node from forging slot reassignments.

**30-day autonomy**: Nodes cache the full catalog locally with a 30-day TTL. If no updates are received for 30 days, nodes expand all keep-out tubes by 1.5× as a precautionary measure and restrict themselves to the inner 80% of their orbital element windows. This degrades packing efficiency but maintains the 10⁻⁶ collision probability threshold.

---

## 6. Key Recommendations

1. **Adopt append-only slot lifecycle** (mint → active → quarantine → retired). Never reuse slot IDs.
2. **Quarantine-first, always**. The 72-hour minimum is non-negotiable for safety.
3. **Cluster coordinators own routine reallocation**. Beacon involvement only for cross-cluster operations.
4. **Pre-position spare nodes** at 5% of cluster population. Do not cascade operational node migrations.
5. **Reserve 15% of per-node annual ΔV** for failure-response maneuvers.
6. **Use Raft, not PBFT**, for intra-cluster consensus. The threat model doesn't justify Byzantine tolerance.
7. **Formally verify the slot state machine** on seL4 as a first-class kernel service, not an application-layer concern.

The most important simulation work to prioritize: Monte Carlo modeling of correlated failure scenarios (solar particle events causing multiple simultaneous Class B failures within a cluster) to validate that the quarantine expansion geometry doesn't consume all available orbital volume when 5+ adjacent nodes fail simultaneously.