---
questionId: "rq-1-40"
questionSlug: "slot-reallocation-governance"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
roundNumber: 2
generated: "2026-02-23"
type: "discussion-response"
---

# Slot Reallocation Governance Protocol: Round 2 Refinement

## Building on the Consensus

Round 1 produced strong convergence around three principles: quarantine-first response, lease-based slot ownership, and tiered authority with Tier 2 cluster coordinators handling time-critical decisions. I agree with all three. Rather than relitigate those foundations, I want to push into the areas where Round 1 left ambiguity or underspecified the engineering, and where I think the winning response needs sharpening to survive contact with the actual orbital mechanics and software architecture.

---

## 1. The Detection Problem Is Harder Than Stated

All three Round 1 responses proposed heartbeat-based failure detection with escalating missed-heartbeat thresholds (typically 3–5 missed beats before declaring a node suspect). This is necessary but insufficient, and I want to be specific about why.

**The geometry problem**: In a heliocentric swarm at ~1 AU, inter-node distances within a cluster can range from tens of kilometers to hundreds of kilometers depending on packing density and the orbital element window assignments. At these distances, with the low-power inter-satellite links specified for automotive-grade hardware, **communication is not omnidirectional and continuous**. Nodes will have scheduled communication windows with their cluster coordinator and neighbors. A "missed heartbeat" might mean the node failed, or it might mean the node's antenna is thermally depointed, or a solar conjunction geometry is degrading the link margin.

**My recommendation**: Failure detection must fuse three independent observables:

1. **Communication heartbeat** (active): Missed scheduled transmissions. Threshold: 3 consecutive missed windows before escalating to C1 (comms-loss suspected).
2. **Ranging/tracking residuals** (passive): Neighboring nodes performing cooperative ranging will notice if a target node's position deviates from its broadcast ephemeris. If range residuals exceed the keep-out tube boundary prediction by >3σ, escalate independently of heartbeat status. This catches the critical case: a node that is still transmitting heartbeats but has lost attitude/orbit control.
3. **Power/thermal signature** (opportunistic): Nodes with star trackers or navigation cameras may detect a neighbor's solar reflectance signature drifting. Low reliability, but useful as a tiebreaker.

The key insight: **a node that is communicating but drifting is more dangerous than a node that is silent but station-keeping**. The state machine must handle both, and the ranging residual channel is the only one that catches the former without waiting for a keep-out tube violation.

**Detection latency budget**: For a node drifting at the maximum uncontrolled rate (driven by solar radiation pressure differential once attitude control is lost—roughly 0.1–1 mm/s² for a lightweight panel), keep-out tube violation of a ±1 km boundary occurs in hours to days. The detection-to-quarantine pipeline must complete within **4 hours** for sudden failures. This is achievable with hourly ranging cycles and 3-heartbeat confirmation at 30-minute intervals.

---

## 2. Quarantine Zone Geometry: Getting Specific

Round 1 correctly identified quarantine as the first response, but was vague on quarantine zone sizing. This matters enormously because oversized quarantine zones cascade—quarantining one slot may force neighbors to restrict their own operational volumes, consuming ΔV for avoidance and potentially triggering secondary quarantines.

**Quarantine zone sizing algorithm**:

The quarantine zone around a failed node must be the **reachable set** of the node's trajectory over the quarantine duration, convolved with navigation uncertainty. Concretely:

- Take the last known state vector (position + velocity) with covariance matrix from the cooperative navigation solution
- Propagate forward under solar gravity + solar radiation pressure (SRP), with SRP uncertainty bounded by the node's known area-to-mass ratio ± attitude uncertainty
- The 99.97% (3σ) reachable ellipsoid at each time step defines the instantaneous quarantine boundary
- Union of all instantaneous boundaries over the quarantine period (I recommend 72 hours initial, extendable) defines the quarantine volume

**Critical design choice**: The quarantine volume must be computed **by the cluster coordinator**, not by individual nodes, because it requires the failed node's last state vector from the cluster ephemeris catalog. Individual nodes then receive a simplified quarantine boundary (e.g., a bounding ellipsoid with 6 parameters) via the beacon broadcast, and apply it as an additional keep-out constraint in their local conjunction screening.

**ΔV impact quantification**: For a typical cluster with ~100 nodes in a volume of roughly 100 km × 100 km × 50 km (order-of-magnitude for a heliocentric cluster segment), a single quarantine zone of ~5 km radius affects 2–6 adjacent slots. Each affected node needs approximately 0.01–0.05 m/s to adjust its orbit enough to maintain separation from the expanding quarantine boundary. At the low end of the ΔV budget (0.5 m/s/year), a node can absorb ~10–50 such events per year before exhausting its budget. Given 1–3 failures per 100-node cluster per year, this is comfortable—**but only if quarantine zones are properly sized and don't cascade**.

---

## 3. Authority Architecture: Resolving the Tier 2/Tier 3 Ambiguity

Round 1's winning response proposed Tier 2 as the primary decision authority with Tier 3 as ratifier. I agree but want to formalize the boundary with a specific rule:

**The Sovereignty Principle**: A cluster coordinator has **unilateral authority** over any action that affects only slots within its own cluster. It has **proposal authority** over any action that affects slots in adjacent clusters, requiring acknowledgment (not approval) from the affected cluster coordinator within a timeout window.

Specifically:

| Action | Authority | Rationale |
|--------|-----------|-----------|
| Declare node C1 (suspect) | Cluster coordinator, unilateral | Time-critical, local information |
| Declare node C2 (incapacitated), activate quarantine | Cluster coordinator, unilateral | Safety-critical, cannot wait for beacon |
| Expand quarantine into adjacent cluster's volume | Originating coordinator proposes; adjacent coordinator must acknowledge within 30 min or quarantine auto-activates | Prevents deadlock if adjacent coordinator is also degraded |
| Transition slot to C4 (available for reassignment) | Cluster coordinator proposes; beacon ratifies within next catalog broadcast cycle | Ensures master catalog consistency |
| Assign replacement node to vacated slot | Beacon authorizes via signed lease in catalog broadcast | Prevents conflicting assignments across clusters |

**The 30-day autonomy constraint** is the hardest case. If beacon spacecraft are unreachable for 30 days, cluster coordinators must be able to issue **provisional leases** for vacated slots, valid until the next beacon contact. These provisional leases are cryptographically signed by the coordinator and carry a "provisional" flag that replacement nodes must honor—meaning they accept the slot but budget ΔV for a possible correction if the beacon's ratification assigns a slightly different orbital element window.

---

## 4. The Distributed Consensus Question

Round 1 mentioned PBFT and Raft. I want to push back on both as overkill for this application.

**The actual consensus requirement is narrow**: We don't need general-purpose Byzantine fault tolerance for slot reallocation. We need agreement among a small number of parties (the cluster coordinator, 2–4 adjacent nodes that can independently verify the failed node's status via ranging, and optionally the beacon) on a binary question: "Is node X failed, and should its slot be quarantined?"

**My recommendation**: Use a **witness-based confirmation protocol**, not a full BFT consensus:

1. Cluster coordinator detects anomaly (heartbeat + ranging fusion)
2. Coordinator requests **ranging confirmation** from the 3 nearest neighbors of the suspect node
3. If ≥2 of 3 witnesses confirm anomalous ranging residuals (>3σ deviation from broadcast ephemeris), the coordinator declares quarantine
4. Decision is logged with witness signatures and broadcast to the cluster
5. Any node can challenge within one communication cycle by providing contradictory ranging data

This is simpler, faster, and more appropriate than PBFT. Byzantine faults (malicious nodes broadcasting false ranging data) are a concern, but the threat model for a solar power satellite swarm is fundamentally different from a cryptocurrency network. The primary adversary is physics (hardware failure, SRP perturbations), not malice. If we later need Byzantine resilience (e.g., against cyber attack), it can be layered on top.

**Quorum for coordinator election** is a separate question. When a cluster coordinator itself fails, the rotating coordinator protocol needs a lightweight leader election. Raft is appropriate here—it's simple, well-understood, and the ~100 nodes per cluster provide ample redundancy. But this is coordinator election, not slot reallocation consensus.

---

## 5. Slot Reassignment ΔV Economics

This is where I think Round 1 was weakest. The question of *which* replacement node occupies a vacated slot is fundamentally a **ΔV optimization problem**, and the answer depends on the swarm's operational phase.

**Phase 1 (1,000–3,000 nodes, buildup)**: New nodes are being launched regularly. The optimal strategy is to **not reassign existing nodes** to vacated slots. Instead, mark vacated slots as priority targets for the next launch batch, and have new nodes injected directly into the vacated orbital element windows during deployment. This preserves existing nodes' ΔV budgets entirely.

**Steady-state operations**: When launch cadence slows, reassignment from within the swarm becomes necessary. The selection algorithm should minimize total ΔV cost across the cluster, not just for the migrating node. The cluster coordinator maintains a **ΔV budget ledger** for each node and selects the replacement that:

1. Has the highest remaining ΔV margin (longest remaining useful life)
2. Is closest in orbital element space to the vacated slot (lowest migration cost)
3. Leaves the smallest gap in its origin position (minimizing secondary reassignment)

Typical intra-cluster slot migration costs: for nodes separated by 5–20 km in a heliocentric orbit, the ΔV for a Hohmann-like transfer over a multi-week timeline is **0.01–0.1 m/s**. This is manageable within the annual budget, but the protocol must track cumulative reassignment ΔV and flag nodes approaching budget limits.

---

## 6. Formally Verified Implementation

The slot state machine (C0→C1→C2→C3→C4→C0) must be implemented as a **formally verified module** within the seL4 kernel's trusted computing base. Specifically:

- The state transition function and its guards (heartbeat counts, ranging thresholds, witness confirmations) should be specified in a theorem prover (Isabelle/HOL, consistent with seL4's verification toolchain)
- The quarantine zone computation can run in userspace (it's computationally intensive but not safety-critical in the kernel sense), but the **decision to activate quarantine** must be a verified kernel-level state transition
- Lease validation (checking cryptographic signatures, expiry times, provisional flags) runs in the kernel's capability system

This is tractable because the state machine is small—6 states, ~12 transitions, with well-defined guards. The verification effort is weeks, not years.

---

## Summary Recommendation

Build a **witness-confirmed, quarantine-first, lease-governed** protocol with cluster coordinators as the primary authority for time-critical safety decisions and beacon spacecraft as the authoritative catalog source. Size quarantine zones using propagated reachable sets. Minimize reassignment ΔV by preferring new-launch replacement over intra-swarm migration. Formally verify the state machine in the seL4 toolchain. And critically—**fuse ranging data with heartbeat data for detection**, because a communicating but drifting node is the most dangerous failure mode this system will face.