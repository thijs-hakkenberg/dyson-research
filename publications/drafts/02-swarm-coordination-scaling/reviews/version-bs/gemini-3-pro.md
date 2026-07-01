---
paper: "02-swarm-coordination-scaling"
version: "bs"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-27"
recommendation: "Minor Revision"
---

# Peer Review: IEEE Transactions on Aerospace and Electronic Systems

**Manuscript Title:** Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms
**Version:** BS
**Reviewer Expertise:** Distributed systems, swarm robotics, discrete event simulation, mega-constellation operations.

---

## 1. Significance & Novelty
**Rating: 5 (Excellent)**

This manuscript addresses a critical and timely gap in the aerospace literature. While significant work exists in swarm robotics (usually focused on $N < 100$ agents) and mega-constellation networking (focused on user-data routing), there is a paucity of rigorous analysis regarding the *control plane* scalability for autonomous fleets in the $10^3$--$10^5$ node regime.

The derivation of closed-form sizing equations for this specific domain is a high-value contribution. The distinction between "byte budget," "MAC efficiency," and "airtime scheduling" (the three feasibility layers) provides a novel framework for systems engineers. Furthermore, the explicit handling of the "stress case" (fleet-wide reconfiguration) versus nominal operations offers realistic bounding conditions that are often ignored in more theoretical consensus papers.

## 2. Methodological Soundness
**Rating: 4 (Good)**

The methodology combines analytical derivation with Cycle-Aggregated Discrete Event Simulation (DES). This is a standard and robust approach for this type of systems engineering analysis.
*   **Strengths:** The cross-validation between the analytical model and the DES (showing $<0.1\%$ agreement) builds strong confidence in the sizing equations. The use of a Gilbert-Elliott (GE) model for link losses is appropriate for the LEO environment, where obstructions and pointing errors create bursty loss patterns.
*   **Weaknesses:** The reliance on a "fluid-server" abstraction in the DES (Section III-A) to validate a system that the authors conclude *requires* TDMA (Section IV-A) is a slight methodological mismatch. While the authors acknowledge this in Section IV-D ("Queue-loss decoupling"), it means the DES does not capture the specific latency penalties of slot misalignment or guard times, only byte-level throughput. Additionally, the assumption of a static topology for a 1-year duration (Section III-B) is a strong simplification for non-coplanar LEO constellations, where cross-plane links are highly dynamic.

## 3. Validity & Logic
**Rating: 5 (Excellent)**

The logical flow from problem statement to solution is rigorous.
*   The argument that **intra-cycle ARQ is ineffective under correlated losses** (Section IV-C) is mathematically sound and a crucial insight for protocol designers.
*   The derivation of the **unicast command bottleneck** (requiring a 22-cycle stagger) effectively demonstrates why broadcast/multicast addressing is mandatory for scalable command and control.
*   The "Design Equations Summary" (Section V-C) is logically derived from the preceding analysis and provides high utility to practitioners.
*   The comparison against the "Sectorized Mesh" is fair, explicitly noting the difference in functional scope (Table VI).

## 4. Clarity & Structure
**Rating: 4 (Good)**

The paper is well-written, dense with technical content, and logically organized.
*   **Strengths:** The "Three-Layer Feasibility" concept is explained clearly. Table I (Notation) and Table VIII (Superframe Budget) are excellent references. The distinction between "Architecture-specific" ($\eta_0$) and "Workload-dependent" ($\eta_{cmd}$) overhead is a helpful taxonomy.
*   **Critique:** The density of information is high. The transition between the "RF-backup" regime (1 kbps) and the "Optical" regime (10+ kbps) is sometimes abrupt. It must be emphasized earlier and more frequently that the 1 kbps constraint is a *survival* mode, as this drives the entire complexity of the paper. Without this constraint, the problem is trivial (as noted in Section IV-A), but the reader might lose sight of why the authors are optimizing so aggressively for 1 kbps.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**

The authors provide a specific and transparent acknowledgment regarding the use of AI tools for ideation (Claude, Gemini, GPT), citing a specific methodology paper. This exceeds current standard disclosure requirements and is commendable. No conflicts of interest are apparent.

## 6. Scope & Referencing
**Rating: 5 (Excellent)**

The scope is perfectly aligned with *IEEE TAES*. The references are a healthy mix of foundational queuing theory (Kleinrock), classical distributed systems (Lamport, Lynch), and modern space networking (Handley, Fraire, CCSDS standards). The inclusion of recent mega-constellation filings (Starlink, Kuiper) grounds the theoretical work in industrial reality.

---

## Major Issues

1.  **Static Topology Assumption vs. LEO Reality:**
    In Section III-B, the authors assume static cluster membership for 1 year. While valid for co-planar clusters, most mega-constellations (Starlink, Kuiper) use Walker-Delta patterns where neighbors change rapidly (every few minutes) across planes. The authors claim re-association overhead is $<0.5\%$, but this only accounts for *bytes*.
    *   *Critique:* The paper ignores the **latency** impact of topology churn. If a node is handing off between clusters, it may miss the TDMA window or the broadcast command slot.
    *   *Requirement:* Please add a paragraph or a small sensitivity analysis discussing the *latency* or *reliability* impact of dynamic topology, not just the bandwidth cost. If the protocol requires a "seed handoff" of 16s (Section III-B), does this create a blind spot during handover?

2.  **The "Fluid Server" Abstraction Limitation:**
    Section IV-D states: "In the DES's fluid-server model, GE losses and coordinator queue occupancy are independent... This decoupling is a property of the fluid-server abstraction, not of the intended TDMA implementation."
    *   *Critique:* This is a significant limitation. In a real TDMA system, a lost packet still consumes a time slot (airtime). The DES confirms the *byte budget* (Layer 1) but does not fully validate the *airtime feasibility* (Layer 3) under dynamic conditions.
    *   *Requirement:* The authors should explicitly state that the DES results for "Drops" in Table VII are optimistic because they do not account for slot fragmentation or wastage due to loss. The analytical check in Table VIII covers this, but the discrepancy between the simulation model and the physical reality needs stronger caveats in the Abstract and Conclusion.

---

## Minor Issues

1.  **Abstract:** "Gilbert-Elliott inter-cycle recovery P95 in 4 cycles." Please clarify if this is 4 *consecutive* cycles or 4 cycles *total duration*. (The text implies duration, but it's ambiguous in the abstract).
2.  **Section III-B (Coordinator Service Discipline):** The text mentions "$D[k_c]/D/1$ batch system." Standard notation is usually $D^{[k]}/D/1$. Please verify standard queuing notation.
3.  **Section IV-A (TDMA Frame Model):** The calculation of $\gamma = 0.949$ is based on a 24 kbps PHY rate. However, if the link degrades (adaptive coding and modulation), the slot time increases. Is the 24 kbps a "worst case" or "nominal" rate? If it's nominal, the margin of 623 ms (Table VIII) might vanish under link adaptation.
4.  **Table V (Sectorized Mesh):** The column "$\eta_{sector}$" has values $>100\%$. While mathematically correct for the formula, physically this means saturation/collapse. It might be clearer to label this "Required Utilization" or mark $>100\%$ as "Saturated."
5.  **Figure 6 (Recovery):** The distinction between the bars (DES) and the line (Analytical) is clear, but the caption should explicitly state that the "squares" in panel (b) represent the simulation data points to avoid confusion.

---

## Overall Recommendation
**Minor Revision**

This is a high-quality paper that makes a significant contribution to the field of space systems engineering. The analytical rigor is high, and the results are non-intuitive and valuable (particularly regarding the unicast command stagger and correlated loss recovery). The revisions requested are primarily to clarify assumptions regarding topology dynamics and to ensure the limitations of the fluid-server simulation are clearly bounded so as not to mislead the reader.

---

## Constructive Suggestions

1.  **Enhance the "Design Equations Summary" (Section V-C):** This is the strongest part of the paper for practitioners. I suggest adding a "Rule of Thumb" for the **Coordinator PHY Rate**. For example: "$C_{coord} \approx 1.25 \times \frac{N_{cluster} \cdot S_{report}}{T_c}$". This gives engineers a quick sizing heuristic before they dive into the full $\gamma$ derivation.

2.  **Clarify the 1 kbps vs. 10 kbps Context:** In the Introduction, explicitly frame the 1 kbps case as the "Survival Mode" or "Safe Mode." The current text mentions it, but the tension between "High-tech autonomous swarm" and "1 kbps link" can be jarring until the reader understands this is the RF backup. A sentence like: *"We size the architecture for the RF-backup channel (1 kbps) to ensure coordination survival during optical link failures"* would be helpful early on.

3.  **Visualizing the "Stagger":** A small timing diagram showing the "Type 2 Unicast Command" staggering (22 cycles) vs. the "Type 1 Broadcast" (1 cycle) would be very effective. It would visually demonstrate why unicast is impossible for fleet-wide commands in this bandwidth regime.

4.  **Sectorized Mesh "Apples-to-Apples":** In Section IV-F, you compare Hierarchical vs. Sectorized Mesh. Ensure you emphasize that the Hierarchical model includes *global* (aggregated) awareness, whereas the Sectorized Mesh only provides *local* awareness. You mention this in the text, but it should be prominent in the comparison table (Table IX) to justify why the Mesh overhead is so much higher for "less" global data.