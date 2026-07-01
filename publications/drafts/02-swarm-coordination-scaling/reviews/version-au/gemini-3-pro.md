---
paper: "02-swarm-coordination-scaling"
version: "au"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-27"
recommendation: "Accept"
---

Here is a rigorous academic peer review of the manuscript "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms," prepared for *IEEE Transactions on Aerospace and Electronic Systems*.

---

# Peer Review Report

**Manuscript ID:** Version AU
**Title:** Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms
**Target Journal:** IEEE Transactions on Aerospace and Electronic Systems

## Review Criteria

### 1. Significance & Novelty
**Rating: 5 (Excellent)**

This manuscript addresses a timely and critical gap in the literature: the specific scaling properties of coordination architectures for mega-constellations ($10^3$--$10^5$ nodes) under constrained bandwidth conditions. While existing literature covers swarm robotics (small scale) and networking routing (data plane), the control plane scalability for autonomous operations at this magnitude is under-explored.

The derivation of closed-form design equations that are validated against a custom discrete event simulation (DES) is a significant contribution. The focus on the "RF-backup" regime (1 kbps budget) is particularly valuable for high-reliability system engineering, as it addresses the worst-case survival mode rather than just the nominal optical-link best case. The distinction between "offered" vs. "delivered" overhead and the decoupling of Gilbert-Elliott losses from coordinator saturation are novel architectural insights that will benefit practitioners designing future constellation management systems.

### 2. Methodological Soundness
**Rating: 4 (Good)**

The methodology combines standard analytical techniques (queueing theory, Markov chains) with a custom cycle-aggregated DES. The approach is generally rigorous. The cross-validation between the analytical models and the DES results (e.g., Table VI and Table X) provides high confidence in the findings. The use of Gilbert-Elliott (GE) models for correlated link loss is appropriate for the space environment, where link outages are often bursty due to attitude tumbling or obstruction.

However, there is a minor methodological disconnect regarding the MAC layer. The paper derives $\gamma$ (MAC efficiency) from a TDMA frame analysis in Section IV-A but applies it somewhat broadly across different comparisons. While the authors acknowledge this abstraction, the reliance on a static $\gamma$ for the hierarchical model versus the contention-based implications for the sectorized mesh could be sharpened. Additionally, the assumption of static cluster membership for a full year of simulation is a strong simplification for LEO constellations with differential nodal regression, though the authors acknowledge this in Section V-B.

### 3. Validity & Logic
**Rating: 5 (Excellent)**

The logical flow from research questions to analytical derivation to simulation validation is exemplary. The conclusions are strictly supported by the data presented. The authors are careful to define their baselines (Centralized and Global-State Mesh) as intentional bounds rather than strawmen, which adds credibility to the intermediate results.

The "Pipeline Decoupling" finding in Section IV-D is a highlight of logical rigor. By demonstrating that retransmission load does not compound coordinator ingress congestion due to the point-to-point architecture, the authors provide a robust design principle. The sensitivity analyses (Figures 10, 11, 12) cover the necessary parameter spaces effectively.

### 4. Clarity & Structure
**Rating: 4 (Good)**

The paper is well-written, dense with technical detail, and logically organized. The distinction between "nominal," "stress," and "event-driven" workloads is clear and helpful.

There are, however, areas where the density of information hampers readability.
1.  **In-text definitions:** Some variables are defined inline within dense paragraphs (e.g., the derivation of $\gamma$ in Section IV-A).
2.  **Table density:** Tables I and IV contain extensive footnotes that contain critical modeling assumptions. These might be better placed in the main text to ensure they are not overlooked.
3.  **Figure referencing:** The text frequently references figures that appear later; ensuring the narrative flow matches the visual evidence would improve readability.

### 5. Ethical Compliance
**Rating: 5 (Excellent)**

The authors provide a specific "Acknowledgment" section detailing the use of AI tools (Claude, Gemini, GPT) for ideation, explicitly stating that the validation is independent. This aligns with emerging transparency standards. The open-source availability of the code and data (Section VI) supports reproducibility and ethical scientific practice. No conflicts of interest are apparent.

### 6. Scope & Referencing
**Rating: 5 (Excellent)**

The paper fits perfectly within the scope of *IEEE TAES*, specifically the intersection of space systems, autonomy, and communications. The references are comprehensive, spanning foundational queueing theory (Kleinrock), distributed systems (Lamport, Lynch), and modern constellation literature (Handley, Del Portillo). The inclusion of recent industry filings (SpaceX, Amazon) grounds the theoretical work in current industrial reality.

---

## Major Issues

1.  **Static Topology Assumption vs. Orbital Dynamics:**
    In Section III-B-2, the authors state: *"The simulation assumes static cluster membership for the 1-year simulation duration."* While justified for co-moving formations, this is a significant limitation for mega-constellations (e.g., Starlink/Kuiper) where planes intersect and relative distances change rapidly. The paper claims the hierarchical advantage is fault tolerance, but dynamic reclustering is a primary source of fault/overhead in real systems.
    *   *Requirement:* The authors must expand the discussion in Section V-B (Limitations) to quantitatively estimate the overhead of cluster handovers based on orbital mechanics (e.g., how often does a node switch clusters in a Walker Delta constellation?). Even a back-of-the-envelope calculation added to the discussion would suffice to bound this error.

2.  **MAC Layer Abstraction in Comparison:**
    In Section IV-F (Topology Comparison), the comparison between Hierarchical (TDMA-friendly) and Sectorized Mesh (likely CSMA/random access) relies heavily on the $\gamma$ parameter. The paper states: *"At Slotted ALOHA efficiency... sectorized mesh reaches 181%."*
    *   *Requirement:* The paper should explicitly clarify if the Sectorized Mesh overhead includes the control messages required to maintain the neighbor list if a TDMA schedule were attempted, or if it defaults to CSMA. If the latter, the "collision" aspect of the MAC layer is abstracted into $\gamma$ but might be non-linear at 65% utilization. A brief clarification on why linear scaling by $1/\gamma$ is valid for the mesh topology at high loads is needed.

---

## Minor Issues

1.  **Table I Footnotes:** The footnote regarding "Screening events, not maneuver-triggering" is critical for interpreting the collision rate. This should be moved to the main text in Section III-A to ensure the reader understands the event generation model.
2.  **Equation 10 (AoI):** The ceiling function is used, but AoI is a continuous time metric in reality. Please clarify if this is a discrete-time approximation based on $T_c$.
3.  **Figure 5 (TDMA):** The caption mentions "red crosses indicate drop conditions," but in black-and-white print, this may be difficult to distinguish. Ensure markers are distinct by shape as well.
4.  **Section IV-A (Coordinator Capacity):** The text mentions "Model A" and "Model B" ingress. While defined in the text, a small table or list explicitly defining the rules for A vs. B (buffer size, refill rate, drop policy) would be clearer than the narrative description.
5.  **Typos/Formatting:**
    *   Section I-A: "mid-2024" (ensure this is consistent with the publication date).
    *   Table III: "Status to coord." is listed as 256 B. Ensure this aligns with the "Status reports" row in Table VIII (205 bps). (256B * 8 bits / 10s = 204.8 bps, so it matches, but the units switch between Bytes and bps frequently).

---

## Overall Recommendation

**Accept with Minor Revisions**

This is a high-quality manuscript that offers a substantial contribution to the engineering of large-scale space systems. The derivation of closed-form design equations, validated by simulation, provides a practical toolkit for system architects. The limitations regarding orbital dynamics and MAC layer abstractions are noted but do not invalidate the core results, provided they are more explicitly bounded in the discussion.

---

## Constructive Suggestions

1.  **Add a "Design Guide" Sidebar or Box:** The "Design Equations Summary" in Section V-C is excellent. Consider formatting this as a distinct "Practitioner's Guide" or a lookup table that maps System Constraints (e.g., "I have 5 kbps") $\to$ Achievable Architecture (e.g., "Hierarchical with $p_{exc}=0.1$").
2.  **Expand the "Safe Mode" Discussion:** The concept of a "Safe Mode Floor" (Section IV-F) is very compelling. Expanding this to discuss how a system might autonomously degrade from Stress Case $\to$ Nominal $\to$ Safe Mode based on observed channel conditions would add significant operational value.
3.  **Clarify "Byte-Level" vs. "Packet-Level":** In the introduction, emphasize earlier that "byte-level" accounting implies zero-overhead framing in the simulation, which is why the $\gamma$ factor is applied *post-hoc*. This prevents confusion for networking experts looking for header overheads in the simulation loop.
4.  **Visualizing the Pipeline Decoupling:** A simple block diagram showing the "Member $\to$ Link (Loss) $\to$ Buffer $\to$ Coordinator (Ingress)" flow would make the argument in Section IV-D (that losses don't cause ingress congestion) immediately intuitive.