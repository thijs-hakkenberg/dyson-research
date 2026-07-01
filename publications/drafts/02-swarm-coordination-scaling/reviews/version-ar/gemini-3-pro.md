---
paper: "02-swarm-coordination-scaling"
version: "ar"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-27"
recommendation: "Minor Revision"
---

**Review of Manuscript Version AR**
**Title:** Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms
**Journal Target:** IEEE Transactions on Aerospace and Electronic Systems

---

### 1. Significance & Novelty
**Rating: 4**

This manuscript addresses a critical and timely gap in the literature: the "missing middle" of coordination scaling between small-scale swarm robotics ($N < 100$) and massive, centrally-managed mega-constellations ($N > 10,000$). The authors correctly identify that while routing protocols for such networks exist, the *coordination overhead*—the byte-level cost of maintaining fleet coherence—is under-characterized.

The primary contribution—a set of closed-form design equations validated by simulation—is highly significant for systems engineers. The focus on the "RF-backup regime" (1 kbps/node) is particularly astute; while optical ISLs are becoming standard, the design driver for resilience is indeed the low-bandwidth backup state. The novelty lies not in the hierarchical topology itself, which is a standard pattern, but in the rigorous parametric sizing and the derivation of specific "practitioner-oriented" envelopes for bandwidth and latency.

### 2. Methodological Soundness
**Rating: 4**

The methodology combines analytical derivation with a cycle-aggregated Discrete Event Simulation (DES). This is an appropriate approach for high-level architectural sizing where packet-level fidelity (e.g., NS-3) would be computationally prohibitive at $N=10^5$.

*   **Strengths:** The decomposition of traffic into specific message types (heartbeats, commands, summaries) provides necessary granularity. The use of Gilbert-Elliott (GE) models for correlated loss is a significant improvement over standard Bernoulli assumptions.
*   **Weaknesses:** The abstraction of the MAC layer is the primary methodological weakness. The simulation treats the "Coordinator Ingress" primarily as a buffering/processing constraint (Model A/B). However, in a realistic RF-backup scenario within a cluster (50-100 nodes), the binding constraint is often the *shared medium contention* (spectral efficiency), not the coordinator's CPU or ingress buffer. While the authors apply a $\gamma$ factor (0.7–0.9) to account for MAC overhead, they treat this as a static scalar. In reality, retransmissions (Section IV-C) dynamically degrade $\gamma$ in shared media.

### 3. Validity & Logic
**Rating: 3**

The conclusions are generally well-supported by the data, with one notable exception regarding the "Joint Independence" claim in Section IV-D.

The authors claim that GE retransmissions and coordinator capacity interact independently. This validity holds *only* under the strict assumption of dedicated point-to-point links from every member to the coordinator. If the cluster operates on a shared RF channel (e.g., omnidirectional S-band TDMA/CSMA), retransmissions would increase channel utilization, thereby increasing collision probability and reducing effective capacity. The paper acknowledges this in the Discussion (Section V-B), but the "Design Equation" framing in the abstract and results section implies a universality that may mislead practitioners designing shared-spectrum systems.

The comparison with the "Sectorized Mesh" is logical and provides a necessary intermediate baseline between centralized and full-mesh architectures.

### 4. Clarity & Structure
**Rating: 5**

The manuscript is exceptionally well-written. The structure is logical, moving from problem definition to model, results, and synthesis.
*   **Definitions:** The distinction between "offered" and "delivered" overhead is handled with precision.
*   **Visuals:** Figures 5 (Phase Stagger) and 12 (Duty Cycle Pareto) are particularly effective at conveying complex trade-offs.
*   **Accessibility:** The "Design Equations Summary" in Section V is a high-value addition for the target audience.

### 5. Ethical Compliance
**Rating: 5**

The authors have included a specific acknowledgment regarding AI-assisted ideation, which aligns with emerging transparency standards. No human subjects are involved. The research appears ethically sound.

### 6. Scope & Referencing
**Rating: 5**

The paper is perfectly scoped for *IEEE TAES*. It bridges the gap between pure networking theory (Comms) and orbital dynamics/operations (Aerospace). The references are comprehensive, covering historical foundations (Kleinrock, Lamport), current operational reality (Starlink, OneWeb), and relevant theoretical work (Mean Field Games, Swarm Robotics).

---

### Major Issues

**1. The "Independence" of Loss and Capacity (Section IV-D)**
In Section IV-D, the paper states: *"GE retransmissions increase offered load by 22% but produce zero additional coordinator drops... This is a property of the modeled pipeline."*
This finding is an artifact of the simulation architecture where link loss occurs *before* the coordinator queue. In a real RF-backup scenario involving 100 nodes in a cluster, the "link" is likely a shared medium. A 22% increase in offered load due to retransmissions would significantly impact the MAC layer (lowering $\gamma$), potentially causing congestion collapse before messages even reach the coordinator's buffer.
*   **Requirement:** The authors must explicitly qualify the "Joint Independence" result. It should be framed as valid only for architectures with dedicated frequency/time slots per node (e.g., strict TDMA) where retransmissions do not cannibalize the slots of other nodes. For CSMA-based backup modes, this independence does not hold.

**2. Physical Layer Topology Assumptions**
The manuscript assumes a "1 kbps per-node budget" and a "Coordinator Ingress of ~21 kbps." This implies the coordinator has a receiver capable of 21x the bandwidth of a node, or 21 parallel receivers.
*   **Requirement:** Please clarify the assumed RF physical topology. Is this a Star topology where the coordinator acts as a hub with a higher-gain antenna/wider bandwidth? Or is it a Mesh where the coordinator is hardware-identical to members but uses more time slots? If it is the latter, the coordinator's transmission of commands (512 B to all members) becomes a massive bottleneck on the shared channel, which is not fully explored in the "Ingress" focused analysis.

### Minor Issues

1.  **Table I (M/D/c Sensitivity):** The label "Hyperscale data center" for $c=1000$ servers processing 10M msg/s is slightly misleading. Modern key-value stores (e.g., Redis/Kafka) can handle 1M+ msg/s on a single optimized node. The constraint for ground stations is usually RF front-ends, not compute servers. Consider renaming the "Representative System" column to reflect RF/Ground Station constraints rather than just "servers."
2.  **Section III-B-2 (Handoff):** The paper mentions a "seed handoff" of ~2 kB for RF-only mode. However, Raft consensus logs can grow significantly. Does this 2 kB include the current term and index, or just the roster? A brief clarification on the minimum viable state for Raft recovery would strengthen this.
3.  **Equation 10 (Safe Mode Floor):** The derivation $\gamma_{min} = \eta / 1.0$ is intuitive but perhaps too simple. Does this account for the "baseline telemetry" (20.5%)? If $\eta$ excludes baseline, then the floor should be $(\eta + 0.205) / 1.0$. Please verify if $\eta$ in Eq 10 includes the baseline.
4.  **Fig 9 (Scaling Trajectory):** The log-linear plot is effective, but the "Analytical Extrapolation" for latency in Fig 13 should be clearly marked as such in the caption (it currently is, but bolding it would help prevent misinterpretation).

### Overall Recommendation
**Minor Revision**

The manuscript is strong, novel, and relevant. The derivation of design equations for swarm coordination is a valuable contribution. However, the abstraction of the MAC layer—specifically the claim of independence between retransmissions and capacity—needs to be carefully qualified to ensure the results are not misapplied to shared-spectrum contention scenarios.

### Constructive Suggestions

1.  **Refine the "Joint Independence" Caveat:** In the abstract and Section IV-D, explicitly state that the independence of GE loss and Coordinator Capacity assumes a non-contention-based MAC (like fixed TDMA) or dedicated ISLs. Warn that in CSMA environments, these factors are coupled.
2.  **Clarify Total Channel Utilization:** In the "Design Equations Summary," explicitly write the equation for *Total* utilization: $U_{total} = (B_{baseline} + \eta) / \gamma$. This prevents readers from forgetting the 20.5% baseline telemetry when sizing their links.
3.  **Expand the "RF-Backup" Description:** Add a short paragraph in Section III describing the physical realization of the RF-backup link (e.g., "Assumed to be an omnidirectional S-band link using TDMA..."). This grounds the 1 kbps constraint in hardware reality.
4.  **AoI Context:** In Section IV-B, briefly mention that while 440s is high for collision *avoidance*, it is acceptable for *conjunction assessment* (screening), which typically happens hours or days in advance. This distinction is crucial for validity.