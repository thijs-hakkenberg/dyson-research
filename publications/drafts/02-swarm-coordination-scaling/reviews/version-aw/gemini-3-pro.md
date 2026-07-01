---
paper: "02-swarm-coordination-scaling"
version: "aw"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-27"
recommendation: "Minor Revision"
---

# Peer Review Report

**Journal:** IEEE Transactions on Aerospace and Electronic Systems
**Manuscript Version:** AW
**Title:** Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms

---

## Review Criteria

### 1. Significance & Novelty
**Rating: 5**

This manuscript addresses a critical and rapidly emerging gap in the aerospace literature: the control plane scalability of mega-constellations ($10^4$--$10^5$ nodes). While significant prior work exists on *routing* (data plane) for such networks (e.g., Handley, Del Portillo), the literature on *coordination* (control plane) has largely been bifurcated between small-scale swarm robotics ($<100$ agents) and traditional centralized constellation management.

The novelty lies in the derivation of "closed-form design equations" specifically for the RF-backup regime (1 kbps budget). This is a highly practical contribution for systems engineers who need to size telemetry budgets before high-fidelity simulations are available. The systematic comparison of hierarchical architectures against sectorized meshes at this specific scale is, to my knowledge, unique in the TAES domain.

### 2. Methodological Soundness
**Rating: 4**

The methodology combines analytical derivation with a custom Cycle-Aggregated Discrete Event Simulation (DES). The approach is generally robust. The authors have taken care to validate their simulation against standard theoretical bounds (Pollaczek-Khinchine for centralized, Gossip bounds for mesh), which builds confidence in the results.

However, the reliance on a "cycle-aggregated" model rather than a packet-level simulator (like NS-3) abstracts away intra-cycle contention. While the authors address this via the $\gamma$ parameter and TDMA frame analysis (Section IV-A), this abstraction is a limitation. The assumption of perfect TDMA slot alignment in a distributed swarm, particularly during the "RF-backup" scenarios where GNSS might be denied, is a strong one. The derivation of $\gamma = 0.949$ is mathematically sound based on the slot definition, but operationally optimistic for a distributed system without a central time reference.

### 3. Validity & Logic
**Rating: 4**

The conclusions are well-supported by the data presented. The decoupling of Gilbert-Elliott (GE) losses from coordinator saturation (Section IV-D) is a valuable insight, though the authors correctly note this only holds for dedicated/orthogonal links.

One logical tension exists in the comparison with the **Sectorized Mesh**. The authors "cap" the mesh fanout to keep it within the bandwidth budget (Table IV), but then note that this severely limits sector coverage (3.2% coverage at Cap=10). While this is a fair *bandwidth* comparison, it is arguably not a fair *functional* comparison. A mesh that only sees 3% of its neighbors may not be operationally viable for collision avoidance, whereas the hierarchical system maintains global awareness (via aggregation). The paper should more explicitly acknowledge that the Sectorized Mesh fails not just on bandwidth, but on *utility* under these constraints.

### 4. Clarity & Structure
**Rating: 5**

The manuscript is exceptionally well-written. The structure is logical, moving from problem definition to modeling, results, and discussion. The distinction between "Stress," "Nominal," and "Event-driven" workload profiles (Section IV-E) is excellent and adds significant nuance to the overhead analysis.

The tables are dense but informative. Specifically, **Table I** (Sensitivity) and **Table X** (Duty Cycle) provide immediate value to the reader. The mathematical notation is consistent. The abstract accurately reflects the paper's content.

### 5. Ethical Compliance
**Rating: 5**

The authors include a specific acknowledgment regarding AI-assisted ideation (Claude, Gemini, GPT), citing a methodology paper. This transparency is commendable and aligns with emerging ethical standards. No conflicts of interest are apparent. The research involves simulation of autonomous systems and poses no direct ethical risks regarding human subjects.

### 6. Scope & Referencing
**Rating: 5**

The paper is perfectly scoped for *IEEE TAES*. It bridges the gap between electronic systems (communications, bandwidth sizing) and aerospace operations (constellation management, orbital dynamics). The references are comprehensive, covering historical foundations (Kleinrock, Lamport), current operational systems (Starlink, OneWeb), and relevant theoretical work (Mean Field Games, Gossip protocols).

---

## Major Issues

1.  **TDMA Synchronization in RF-Backup Mode (Section IV-A):**
    The paper derives a high MAC efficiency ($\gamma \approx 0.95$, conservatively 0.85) based on a TDMA frame structure. This assumes nodes are synchronized. However, the primary use case for this 1 kbps budget is "RF-backup," which often implies a loss of primary optical links and potentially GNSS denial (as hinted in Section IV-A, "TDMA synchronization").
    *   *Critique:* If GNSS is denied, maintaining the microsecond-level synchronization required for tight TDMA slots across a 500km cluster is non-trivial. The paper mentions a "sync beacon" adding 0.8% overhead.
    *   *Requirement:* Please expand on the feasibility of this sync beacon. If the channel is shared/contentious, how does the coordinator reliably broadcast the beacon without collision? If the beacon is lost, does the TDMA schedule collapse into Slotted ALOHA? The robustness of $\gamma$ depends entirely on this sync mechanism.

2.  **Coordinator Failure Recovery Dynamics:**
    The paper models coordinator failure rates identical to node failure rates (2%/year) and claims "graceful degradation."
    *   *Critique:* In a hierarchical topology, the loss of a cluster coordinator is an event of higher severity than the loss of a leaf node. The paper mentions Raft election and state transfer, but does not quantify the *transient* impact on the swarm during the election window.
    *   *Requirement:* Please provide a specific metric or discussion regarding the "Time to Recovery" for a cluster. During the 3-5s handoff window (or longer if re-election is needed), is the cluster effectively blind? Does this transient outage exceed the AoI requirements derived in Section IV-B?

---

## Minor Issues

1.  **Table II (Scalability Sensitivity):** The column "Representative System" lists "Hyperscale data center" for $c=1000$. This seems slightly colloquial for a formal academic table. Consider changing to "Cloud-native distributed backend" or similar.
2.  **Figure 5 (AoI):** The caption describes "Geometric growth." Looking at Eq. 10, AoI scales with $1/\ln(1-p)$, which is roughly inverse-linear for small $p$, not geometric. Please verify the terminology.
3.  **Section IV-D (Joint Interaction):** The text states "GE losses remove messages *before* they reach the coordinator ingress queue." This is a crucial physical assumption. Please clarify if this assumes the coordinator has infinite receive radios (one per member) or a single radio with time-slotted access. If it is a single radio, a "bad" packet still occupies an RF slot, even if the payload is corrupted, potentially blocking a "good" packet from another node if scheduling isn't perfect.
4.  **Equation 5:** $M_{total}$ includes $N/k_c$ (cluster summaries). Does this assume the cluster coordinator *also* sends its own status report as a leaf node? Usually, the coordinator is a member of the cluster. Clarify if $N$ includes the coordinators or if they are separate entities.
5.  **Section V-B (Limitations):** The discussion on "Static topology" is good, but the "Cross-plane drift" explanation is dense. The estimate of <0.5% overhead is analytical. A sentence acknowledging that this assumes efficient neighbor discovery (which can be expensive) would be beneficial.

---

## Overall Recommendation

**Minor Revision**

This is a high-quality manuscript that makes a significant contribution to the field of large-scale space systems engineering. The derivation of design equations is novel and practically useful. The major issues identified relate to the robustness of assumptions regarding synchronization and failure recovery, which can be addressed through textual clarification and perhaps a small expansion of the discussion, without requiring new simulation runs.

---

## Constructive Suggestions

1.  **Add a "Safe Mode" Analysis for MAC:** In Section IV-A, explicitly calculate the system performance if synchronization fails and the network reverts to Slotted ALOHA ($\gamma \approx 0.36$). Does the "Nominal" workload still fit? This would provide a lower-bound robustness check that strengthens the engineering value of the paper.
2.  **Clarify Sectorized Mesh Utility:** In the discussion or conclusion, explicitly state that while the Sectorized Mesh *can* be sized to fit the bandwidth (via capping), its *functional utility* for global coordination is severely degraded compared to the Hierarchical approach at this specific bandwidth constraint. This prevents readers from thinking they are functionally equivalent options.
3.  **Visualizing the Design Envelope:** Figure 10 (Topology Summary) is good. Consider adding a "Design Region" overlay that highlights the specific combination of $N$, Bandwidth, and Latency where Hierarchical is the *only* viable solution (i.e., where Centralized fails on spectrum/latency and Mesh fails on bandwidth). This would crystallize the "sweet spot" for the proposed architecture.