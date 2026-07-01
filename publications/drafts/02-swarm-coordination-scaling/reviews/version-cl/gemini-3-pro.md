---
paper: "02-swarm-coordination-scaling"
version: "cl"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-03-03"
recommendation: "Unknown"
---

Here is a rigorous peer review of the manuscript "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version CL), tailored for *IEEE Transactions on Aerospace and Electronic Systems*.

---

# Peer Review Report

**Manuscript ID:** [Assigned by Editor]
**Title:** Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms
**Authors:** Project Dyson Research Team

## 1. Significance & Novelty
**Rating: 4 (Good)**
The paper addresses a critical gap in the literature: the specific sizing of coordination channels for mega-constellations ($10^3$--$10^5$ nodes). While high-bandwidth optical backbones are well-studied, the "control plane" (low-bandwidth, high-reliability RF backup) is often treated as an afterthought. The derivation of closed-form sizing equations for this specific regime is a valuable contribution. The novelty lies in the rigorous separation of message-layer byte budgets from physical-layer TDMA schedulability, specifically applied to the constraints of CCSDS Proximity-1 framing.

## 2. Methodological Soundness
**Rating: 5 (Excellent)**
The methodology is robust. The authors employ a triangulation approach: analytical derivations, cycle-aggregated Discrete Event Simulation (DES), and a slot-level TDMA simulator. The explicit handling of the "validation gap" (Tier 1 vs. Tier 3 evidence) is intellectually honest and rare in engineering papers. The use of Gilbert-Elliott (GE) models to stress-test the TDMA schedule against correlated losses is particularly strong. The derivation of $\gamma$ (slot efficiency) from first principles (CCSDS standards) rather than arbitrary constants adds significant credibility.

## 3. Validity & Logic
**Rating: 5 (Excellent)**
The internal logic is consistent. The progression from byte-budget feasibility (Layer 1) to airtime schedulability (Layer 2) is sound. The identification of the "stress case" ($\eta \approx 46\%$) as a continuous-duty upper bound, distinct from routine operations ($\eta \approx 5\%$), resolves potential concerns about bandwidth realism. The finding that intra-cycle ARQ is ineffective under blockage-dominated coherence ($\tau_c \ge T_c$) is logically derived and physically justified.

## 4. Clarity & Structure
**Rating: 4 (Good)**
The paper is dense but well-structured. The distinction between "Model S" (simplified) and "Model C" (CCSDS) is maintained clearly throughout. Tables are information-rich, particularly Table VII (Rate Ladder) and Table X (Margin Analysis). However, the density of variables in the text can occasionally hinder readability; a few transitions between the DES results and the analytical derivations could be smoother.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**
The authors provide a clear data availability statement pointing to a repository with source code and datasets. The AI disclosure is specific and appropriate, detailing that AI was used for ideation and editing but not for result generation.

## 6. Scope & Referencing
**Rating: 4 (Good)**
The literature review covers swarm robotics, constellation management, and networking protocols well. The connection to CCSDS standards (Proximity-1, TM Sync) is excellent. The paper fits well within the scope of *IEEE TAES*.

---

## Major Issues

1.  **Justification of the 1 kbps Constraint**
    *   **Issue:** The paper anchors heavily on a 1 kbps per-node budget. While the link budget (Section IV.A.1) justifies this based on UHF backup capabilities, the operational premise needs tightening.
    *   **Why it matters:** If the primary Optical ISL has $>$1 Gbps, readers may question why the coordination architecture is constrained to 1 kbps. The paper mentions "tumbling spacecraft" and "black-start," but this needs to be the central argument for the *sizing*, not just a side note.
    *   **Remedy:** In the Introduction or System Model, explicitly state that the coordination architecture is sized for the *lowest common denominator* (the survival mode) to ensure architectural invariance across failure modes. Emphasize that sizing for the optical link would leave the swarm uncontrollable during common fault states.

2.  **Sensitivity to Oscillator Drift in TDMA**
    *   **Issue:** The TDMA analysis assumes GNSS synchronization ($<100$ ns) or TCXO holdover. The margin analysis (Table X) allocates 6 ms for clock drift.
    *   **Why it matters:** In a GPS-denied environment (a common defense scenario) or during long eclipses, cheap oscillators on CubeSats drift significantly. If the guard times are underestimated, the $\gamma$ values for Model C are invalid, and the 35 kbps recommendation might be insufficient.
    *   **Remedy:** Add a brief sensitivity calculation or a few sentences discussing the impact of GNSS denial duration on $T_{\text{guard}}$. If the drift exceeds the 4.7 ms guard, how quickly does the system degrade?

## Minor Issues

1.  **Clarification of "Campaign Duty Factor" ($d$) vs. "Unicast Fraction" ($q$):** Table VIII is excellent, but the interaction between $d$ and $q$ in the text could be sharper. Ensure the reader understands that $d$ gates the *generation* of commands, while $q$ dictates the *transmission cost* (broadcast vs. staggered unicast).
2.  **Figure 6 Readability:** The "Model C" feasibility boundary is crucial. Consider adding a horizontal line at $\gamma \approx 0.75$ to visually reinforce the "knee" of the curve where returns diminish.
3.  **Typos/Phrasing:**
    *   Section IV.A: "The binding bottleneck is cluster coordinator ingress..." - clarify if this is strictly for the RF backup mode.
    *   Table I: Ensure all symbols ($\eta_0$, $\eta_{\text{cmd}}$) are consistently used in the text equations.

---

## Overall Recommendation
**Recommendation: Accept with Minor Revisions**

This is a high-quality, rigorous manuscript that provides actionable design equations for space systems engineers. The authors have successfully addressed the complexities of hierarchical coordination, moving beyond simple "bit-counting" to address protocol overheads, framing constraints, and correlated channel losses.

The transition from the earlier version's generic $\gamma=0.85$ to the standards-derived $\gamma \approx 0.76$ (Model C) significantly strengthens the paper, transforming it from a theoretical exercise into a practical engineering guide. The "Rate Ladder" (Table VII) is a standout contribution that clearly communicates the design rationale.

The revisions requested above are primarily for narrative tightening and defensive justification of the survival-mode constraints. Once addressed, this paper will serve as a standard reference for swarm coordination sizing.

## Constructive Suggestions

1.  **Expand the "Thundering Herd" Discussion:** The recovery from a coordinator failure involves 100 nodes contending for the channel. The paper mentions Slotted ALOHA. A brief mention of how the *new* coordinator establishes the TDMA schedule (e.g., does it broadcast a beacon to reset the timing?) would complete the operational picture.
2.  **Visualizing the "Cliff":** In the conclusion or discussion, a simple "Stoplight" chart (Green/Yellow/Red) mapping PHY rates (24, 30, 35, 50 kbps) to Feasibility (Margin, ARQ capability) would be a powerful summary for practitioners.
3.  **Generalized Gamma:** The inclusion of Eq. 14 is excellent. Suggest explicitly labeling it as the "General Sizing Equation" in the text to draw attention to its utility for non-CCSDS systems.