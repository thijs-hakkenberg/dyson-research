---
paper: "02-swarm-coordination-scaling"
version: "ab"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-26"
recommendation: "Accept"
---

**IEEE Transactions on Aerospace and Electronic Systems**
**Peer Review Report**

**Manuscript ID:** [Assigned by Editor]
**Title:** Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study
**Version:** AB

---

### **Review Summary**

This manuscript presents a parametric design-space characterization of coordination architectures for large-scale autonomous satellite swarms ($10^3$ to $10^5$ nodes). The authors utilize a cycle-aggregated Discrete Event Simulation (DES) to compare a hierarchical topology against centralized and mesh baselines. Key contributions include quantifying the bandwidth requirements for coordinators (finding a break-point around 25–50 kbps), analyzing the trade-off between Age-of-Information (AoI) and bandwidth using exception-based telemetry, and demonstrating the failure of intra-cycle retransmission under Gilbert-Elliott correlated link losses.

This is a strong, rigorous paper that addresses a critical gap in the literature: the "missing middle" between small-scale swarm robotics ($<100$ agents) and massive ground-managed constellations. The byte-level traffic accounting is meticulous, and the distinction between topology-induced overhead and workload-induced overhead is a valuable insight for system architects.

---

### **1. Significance & Novelty**
**Rating: 5 (Excellent)**

**Assessment:**
The scaling of autonomous coordination to $10^5$ nodes is a highly relevant problem given current commercial mega-constellation roadmaps (Starlink, Kuiper) and future sparse-aperture concepts. Most existing literature relies on asymptotic complexity analysis ($O(N)$ vs $O(N^2)$) or small-scale simulations. By simulating $10^5$ nodes with specific byte-level protocol accounting, this paper provides concrete engineering data (e.g., the 50 kbps coordinator threshold) that theoretical papers miss. The characterization of the "design envelope" (9$\times$ spread between nominal and stress workloads) is a significant contribution to the systems engineering of future space architectures.

### **2. Methodological Soundness**
**Rating: 4 (Good)**

**Assessment:**
The cycle-aggregated DES approach is innovative for achieving the necessary scale ($10^5$ nodes) while maintaining reasonable runtime. The authors are transparent about the abstraction level (message-layer vs. packet-layer). The statistical treatment (Monte Carlo with bootstrap intervals) is sound.

However, the abstraction of the MAC layer into a simple efficiency factor ($\gamma$) is a limitation, particularly for the mesh topology comparators. In a real RF environment with $10^5$ nodes, the hidden terminal problem and noise floor rise could render the "Sectorized Mesh" significantly less efficient than the $\gamma=0.7$ assumption implies. While the paper acknowledges this in Section V, the comparison between the deterministic TDMA hierarchy and the likely contention-based mesh may be slightly biased in favor of the hierarchy.

### **3. Validity & Logic**
**Rating: 5 (Excellent)**

**Assessment:**
The conclusions are logically derived from the simulation data. The decomposition of overhead in Fig. 8 (showing that commands, not topology maintenance, drive bandwidth) effectively supports the argument that hierarchical structures are not inherently wasteful. The analysis of the Gilbert-Elliott link model (Section IV-C) is particularly strong; the finding that intra-cycle retransmission is structurally ineffective for correlated bursts is a crucial validation of the need for DTN/store-and-forward protocols in this domain.

### **4. Clarity & Structure**
**Rating: 5 (Excellent)**

**Assessment:**
The manuscript is exceptionally well-written. The definitions are precise (e.g., the distinction between "baseline telemetry" and "protocol overhead"), and the roadmap in Section IV helps navigate the dense results. The figures are high-quality and information-dense. The "Baseline Interpretation Note" in the introduction is helpful for managing reader expectations regarding the reference models.

### **5. Ethical Compliance**
**Rating: 5 (Excellent)**

**Assessment:**
The authors provide a clear acknowledgment of AI-assisted ideation in the Acknowledgments section, consistent with emerging publication standards. No human subjects are involved. The research appears ethically sound.

### **6. Scope & Referencing**
**Rating: 5 (Excellent)**

**Assessment:**
The paper fits squarely within the scope of *IEEE TAES*. The literature review covers the necessary bases, bridging swarm robotics (Brambilla, Dorigo), networking (DTN, Akyildiz), and space operations. The inclusion of recent mega-constellation context (Starlink, Kuiper) keeps the work timely.

---

### **Major Issues**

1.  **MAC Layer Contention in Mesh Topologies:**
    In Section III-B-4 (Sectorized Mesh), the paper calculates overhead based on message counts. However, unlike the hierarchical model where the coordinator can enforce TDMA (as detailed in Section IV-A), the mesh topology presumably relies on distributed random access (e.g., CSMA or Slotted ALOHA) within the sector. At high densities ($k_s \approx 317$ neighbors), the collision probability would be non-trivial. The paper applies a generic $\gamma$ factor, but mesh performance degrades non-linearly with load.
    *   *Requirement:* Please add a paragraph in the Discussion or Section III-B acknowledging that the Sectorized Mesh results represent a "best-case" scenario assuming perfect scheduling, and that real-world contention would likely increase the effective overhead or latency further than reported.

2.  **Orbital Dynamics Simplification:**
    Equation 11 ($\sigma_{pos}(t) = \sigma_0 + \dot{\sigma} \cdot \text{AoI}$) assumes linear error growth. In orbital mechanics, along-track error grows linearly due to drag uncertainty/period mismatch, but cross-track and radial errors oscillate. While the linear model is an acceptable approximation for the "along-track dominant" error in LEO over short timescales (minutes), the text should explicitly state that this models *along-track* uncertainty specifically, as this is the primary collision risk driver.
    *   *Requirement:* Clarify in Section IV-B that this model applies specifically to along-track uncertainty, which is the dominant error term for conjunction assessment.

---

### **Minor Issues**

1.  **Table II (Mesh Traffic):** The footnote states "Sectorized mesh generates $\leq$1.6 KB/node/cycle". Please clarify if this includes the overhead of the contention window or headers, or if this is purely payload + application header.
2.  **Section IV-A (Coordinator Capacity):** The distinction between "Model A" and "Model B" is excellent. However, in Table VI, the column "MAC $\gamma$" lists 1.0 for Models A and B. Is this realistic? Even a leaky bucket shaper feeding a physical link has framing overhead.
3.  **Figure 6 (AoI):** The caption mentions "P99 AoI exceeds 400 s". The text says 441 s. Please ensure consistency.
4.  **Reference Style:** Reference [1] and [3] are non-archival websites. While necessary for current constellations, ensure the access dates are recent (the draft says "accessed February 2026" which implies this is a future-dated draft or a template error—please correct the year to the current date).
5.  **Author Anonymity:** The manuscript is authored by "Project Dyson Research Team." Ensure this complies with IEEE's double-blind review policy if applicable. If this is the final version text, it is fine, but for review, standard anonymous formatting is usually preferred.

---

### **Overall Recommendation**
**Accept with Minor Revisions**

This paper makes a substantial contribution to the systems engineering of large-scale space swarms. The simulation framework is robust for the questions asked, and the results provide actionable design guidance (specifically regarding coordinator sizing and the limits of retransmission). The requested revisions regarding the MAC layer and orbital dynamics are clarifications to ensure the bounds of validity are clear, rather than flaws requiring new simulation runs.

---

### **Constructive Suggestions**

1.  **Strengthen the Physical Layer Link:** In Section V (Discussion), explicitly mention that while the DES models the *network* layer, the transition to hardware implementation would require a specific MAC protocol (e.g., 802.11-derivative or CCSDS Proximity-1) that supports the assumed $\gamma$ efficiencies.
2.  **Expand on "Phase Staggering":** The finding that phase staggering reduces the coordinator requirement from 50 kbps to 25 kbps is operationally very important. A sentence recommending this as a "default" implementation requirement for hierarchical swarms would strengthen the conclusion.
3.  **AoI Operational Context:** In Section IV-B, when discussing the 440s AoI, briefly mention that for *maneuver planning* (vs. immediate collision avoidance), 7-minute staleness is often acceptable, which reinforces the viability of the nominal workload profile.