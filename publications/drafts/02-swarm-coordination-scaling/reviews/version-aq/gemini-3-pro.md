---
paper: "02-swarm-coordination-scaling"
version: "aq"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-27"
recommendation: "Minor Revision"
---

# Peer Review: IEEE Transactions on Aerospace and Electronic Systems

**Manuscript ID:** [Version AQ]
**Title:** Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms
**Authors:** Project Dyson Research Team

---

## Review Criteria

### 1. Significance & Novelty
**Rating: 5**
This manuscript addresses a critical and timely gap in the literature: the coordination of "mega-constellations" ($10^4$--$10^5$ nodes) under degraded communication conditions. While much existing literature focuses on nominal high-bandwidth optical routing or centralized management, this paper rigorously explores the "RF-backup" regime (1 kbps/node). This is a high-value contribution because system viability is often determined by behavior during fault modes, not nominal operations. The derivation of closed-form design equations (the "practitioner-oriented sizing table") is a novel and highly practical contribution for systems engineers.

### 2. Methodological Soundness
**Rating: 4**
The methodology combines analytical derivations (queueing theory, geometric distributions) with a custom cycle-aggregated Discrete Event Simulation (DES). The approach is generally robust. The choice to use a cycle-aggregated model rather than a packet-level simulator (like NS-3) is justified by the scale ($10^5$ nodes), though it introduces abstractions regarding MAC-layer contention that require careful scrutiny (see Major Issues). The statistical treatment (30 Monte Carlo replications, bootstrap CIs) is sound. The Gilbert-Elliott loss model is appropriate for the channel characteristics expected in LEO.

### 3. Validity & Logic
**Rating: 4**
The conclusions are well-supported by the data presented. The "Joint Independence" finding in Section IV-D—that retransmission load and coordinator ingress congestion decouple under point-to-point architectures—is a non-intuitive but logically sound result given the architectural assumptions. The comparison against baselines is fair, although the "Global-State Mesh" serves mostly as a theoretical upper bound rather than a viable competitor. The logic regarding coordinator duty cycles and power variance is sound.

### 4. Clarity & Structure
**Rating: 5**
The manuscript is exceptionally well-written. The structure is logical, moving from theoretical framing to simulation setup, results, and discussion. The distinction between "offered" and "delivered" overhead is handled with precision. Figures are referenced appropriately, and the tables (particularly Table X comparing topologies) are effective summaries. The abstract accurately reflects the content.

### 5. Ethical Compliance
**Rating: 5**
The authors include a specific acknowledgment regarding AI-assisted ideation (Claude, Gemini, etc.), which aligns with emerging transparency standards. No obvious conflicts of interest or ethical lapses regarding data fabrication are apparent.

### 6. Scope & Referencing
**Rating: 5**
The paper fits squarely within the scope of *IEEE TAES*, bridging space systems engineering, communications, and autonomous control. The references are a good mix of classical theoretical foundations (Kleinrock, Lamport) and modern operational context (Starlink, Kuiper, CCSDS standards).

---

## Major Issues

**1. MAC Layer Abstraction and Synchronization in "Backup" Mode**
The paper relies on a parameter $\gamma \in [0.7, 0.9]$ to account for MAC overhead and assumes TDMA is feasible (Section IV-A). While the paper acknowledges this is a message-layer analysis, the premise of the paper is the "RF-backup" regime where optical ISLs are down.
*   *Critique:* If the swarm is in a degraded state requiring RF backup, can it maintain the precise time synchronization required for efficient TDMA ($\gamma \approx 0.85$)? If the optical links used for clock transfer are down, the system might degrade to Slotted ALOHA or CSMA, where $\gamma$ drops significantly (to $\sim 0.36$ or lower).
*   *Requirement:* The authors should add a sensitivity analysis or a discussion paragraph addressing the *minimum* $\gamma$ required to sustain the "Nominal" and "Stress" workloads. If the system falls back to ALOHA, does the hierarchy collapse? (Section IV-F hints at this, but it needs to be explicit in the conclusion/summary).

**2. Topology Dynamics vs. Orbital Mechanics**
The hierarchical model assumes a relatively static tree structure ($k_c$ clusters).
*   *Critique:* In LEO mega-constellations, neighbor relationships are dynamic, especially between orbital planes. The paper mentions "handoff" (Section III-B-2) mostly in the context of leader election within a cluster. It does not adequately address the overhead of nodes *switching* clusters due to orbital mechanics (e.g., cross-plane drift).
*   *Requirement:* Please clarify if the simulation accounts for nodes moving between clusters, or if the topology is static for the 1-year duration. If static, this limitation must be stated clearly, as cluster re-association overhead could be non-negligible in high-inclination shells.

---

## Minor Issues

1.  **Table I (M/D/c Sensitivity):** The column for $N_{max}$ implies a hard limit. It would be helpful to explicitly state the assumed latency constraint that defines "max" here (is it queue stability $\rho < 1$, or a specific delay threshold?).
2.  **Section III-B-2 (Handoff):** The text mentions "Seed handoff" ($\sim 2$ kB) for RF-only mode. It is unclear if the simulation implements this specific fallback or if it assumes the optical link is always available for handoffs. Please clarify the simulation configuration regarding handoffs during the "RF-backup" experiments.
3.  **Eq. 8 (TDMA Capacity):** The equation uses $S_{eph}$. Please ensure $S_{eph}$ is defined in the text near the equation (it appears to be the status report size, 256 B, but explicit definition helps).
4.  **Figure 5 (Workload Comparison):** The visual distinction between the "Sectorized Mesh" and "Hierarchical (Stress)" lines is somewhat difficult to parse at the lower end of the Y-axis. Ensure line styles or markers are distinct.
5.  **Reference Style:** In the Acknowledgment, the citation `[dyson_multimodel]` is used for the AI methodology. Ensure this meets IEEE standards for citing non-archival/internal reports, or move the details into a footnote.

---

## Overall Recommendation

**Minor Revision**

This is a high-quality manuscript that makes a significant contribution to the field of autonomous spacecraft swarm operations. The analytical and simulation work is robust. The primary reason for requesting a revision is to ensure the assumptions regarding MAC layer efficiency ($\gamma$) and topology dynamics are more rigorously bounded, given that the paper's core value proposition is robustness in degraded environments.

---

## Constructive Suggestions

1.  **Add a "Safe Mode" Floor Calculation:** In Section IV-F (or Discussion), explicitly calculate the "Safe Mode Floor"—the minimum MAC efficiency $\gamma$ required to support the *Nominal* workload (heartbeats + summaries, no commands). This would give practitioners a hard lower bound for system viability (e.g., "The system survives on Slotted ALOHA for monitoring, but requires TDMA for command campaigns").
2.  **Expand on Orbital Dynamics:** Briefly discuss how the hierarchical clustering maps to orbital planes. For example, "Clusters are assumed to be intra-plane formations where relative topology is stable." This clarifies the scope of the validity of the static topology assumption.
3.  **Refine the Abstract:** The abstract is dense. Consider explicitly stating "Message-layer analysis" in the first sentence to manage reader expectations regarding PHY/MAC fidelity immediately.
4.  **Future Work - Covariance:** The point about coupling AoI to covariance propagation (Section V-A) is excellent. A sentence suggesting that "AoI requirements should be derived dynamically from the orbital uncertainty growth rate ($\dot{\sigma}$)" would strengthen the link to astrodynamics.