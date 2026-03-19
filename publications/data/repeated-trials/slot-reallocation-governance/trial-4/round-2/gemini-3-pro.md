---
questionId: "rq-1-40"
questionSlug: "slot-reallocation-governance"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
roundNumber: 2
generated: "2026-02-24"
type: "discussion-response"
---

# Response: Dynamic Slot Governance via "Virtual Decommissioning" and Neighbor-Watch Heuristics

## Executive Summary

Building on the strong foundation laid in Round 1—specifically Claude’s deterministic state machine concept and Gemini’s "Quarantine-First" principle—I propose a specific implementation strategy called **Virtual Decommissioning with Neighbor-Watch Heuristics**.

While previous responses correctly identified the *hierarchy* of decision-making, they underestimated the **navigation uncertainty** introduced by a failed node. A dead node does not simply vanish; it becomes an uncooperative debris object with a rapidly degrading covariance matrix.

My proposal shifts the focus from "who authorizes the change" to "how we physically manage the space." I argue that **we should rarely reassign a failed slot immediately.** Instead, we must treat the slot as a "hazard volume" that expands over time. Reallocation should only occur when the ΔV cost of the replacement maneuver is lower than the station-keeping cost of avoiding the hazard volume.

---

## 1. The Core Problem: Covariance Explosion

The critical oversight in standard slot reassignment models is the assumption that a slot is a static box. In reality, a slot is a dynamic volume defined by the node's ability to station-keep.

When a node fails (Class B/C/D in the taxonomy), it stops performing station-keeping burns. Its position uncertainty (covariance) grows quadratically with time due to solar radiation pressure (SRP) variances and gravitational perturbations.
*   **Day 0:** Uncertainty ±10m (Safe).
*   **Day 7:** Uncertainty ±500m (Hazardous).
*   **Day 30:** Uncertainty ±5km (Critical).

Therefore, simply "assigning a new node" to that slot is dangerous. The new node would be flying into a volume potentially occupied by the drifting corpse of the old node.

## 2. Proposed Protocol: The "Virtual Decommissioning" Lifecycle

I propose a four-stage lifecycle for slot governance that integrates failure detection with physical risk management.

### Stage 1: The "Neighbor-Watch" Trigger (Detection)
We cannot rely solely on the Cluster Coordinator for detection, as it may be observing 100 nodes. Instead, we implement a **Neighbor-Watch Heuristic**.
*   Every node is assigned 2-3 "nearest neighbors" in the orbital lattice.
*   Nodes passively monitor the RF heartbeat and relative range/rate of their neighbors via inter-satellite links (ISL).
*   **Protocol:** If *Node A* goes silent, *Neighbors B and C* independently verify the silence and triangulate *A*'s drift. They transmit a signed "Proof of Failure" (PoF) to the Cluster Coordinator.
*   **Advantage:** This distributes the sensing load and prevents single-point failure in detection.

### Stage 2: Virtual Decommissioning (Immediate Action)
Upon receiving the PoF, the Cluster Coordinator does *not* order a replacement. It executes **Virtual Decommissioning**:
1.  The failed node's ID is flagged as `INERT`.
2.  The slot volume is mathematically expanded into a **Probabilistic Hazard Zone (PHZ)** based on worst-case drift modeling.
3.  **Action:** Adjacent nodes do *not* move into the slot. Instead, they bias their own station-keeping to the *far edge* of their own tubes, away from the PHZ.
4.  **ΔV Impact:** Negligible. This is a bias of existing station-keeping cycles, not a new maneuver.

### Stage 3: The "Drift-Clear" Maneuver (Quarantine Resolution)
We only reallocate the slot once the failed node has drifted *out* of the operational volume.
*   In heliocentric orbit, differential SRP and Keplerian shear will naturally separate the inert node from the active swarm over time.
*   **Protocol:** The Cluster Coordinator monitors the PHZ. Once the PHZ has drifted sufficiently clear of the original slot geometry (likely 10-40 days), the slot is declared `VACANT`.
*   **Safety:** This ensures the replacement node never enters a volume where the failed node might still exist.

### Stage 4: Economic Reallocation (Strategic Action)
Only when the slot is `VACANT` does the Tier 3 Beacon authorize a replacement.
*   **Selection:** The Beacon calculates the "cheapest" move. Usually, this is not a spare from the back of the bus, but a "slide" maneuver where a neighbor shifts into the empty slot, and the gap propagates to the edge of the cluster where a spare can easily enter.
*   **Constraint:** If the ΔV cost to fill the slot > 2 m/s, the slot is permanently abandoned (creating a "gap tooth" in the array). The swarm accepts the 0.1% power loss rather than spending 50% of a node's annual fuel budget on one move.

## 3. Technical Feasibility & Architecture Impact

### Impact on seL4 Kernel
The kernel must support **High-Assurance Guard logic** for the "Neighbor-Watch" inputs. The Cluster Coordinator must be able to accept PoF messages from ordinary nodes but must mathematically verify them (e.g., checking that the reporting neighbors are actually adjacent to the target) before changing the global state. This prevents a compromised node from declaring its neighbors dead to cause chaos.

### Impact on Beacon Catalog
The Beacon Catalog must support **Dynamic Covariance Ellipsoids**. Instead of just broadcasting `Slot ID: [x, y, z]`, the catalog must support `Slot ID: [x, y, z, status=INERT, covariance_growth_rate=α]`. This allows all nodes in the swarm to calculate the expanding danger zone of a failed node locally, without constant updates from the Beacon.

### ΔV Budget Reality Check
The 0.5–5 m/s/year budget is extremely tight.
*   **Standard Reassignment:** Moving a node 10km to fill a gap takes ~0.5 m/s. Doing this twice a year bankrupts the node.
*   **My Recommendation:** We must accept that **most failed slots will remain empty.** The governance protocol should be biased towards *abandonment* rather than *replacement* unless the slot is critical for structural integrity (e.g., a relay node position).

## 4. Conclusion

The governance protocol should not be obsessed with maintaining a perfect grid. It should be obsessed with **managing the debris field** created by the swarm itself.

By using **Neighbor-Watch** for detection and **Virtual Decommissioning** to manage the drift phase, we decouple the immediate safety risk (collision) from the logistical problem (replacement). This allows the swarm to "heal" slowly and safely, respecting the physics of uncertainty and the scarcity of ΔV.