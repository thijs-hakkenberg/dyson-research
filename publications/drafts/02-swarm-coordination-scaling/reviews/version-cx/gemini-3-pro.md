---
paper: "02-swarm-coordination-scaling"
version: "cx"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-03-05"
recommendation: "Unknown"
---

Here is a comprehensive peer review of the manuscript "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version CX), prepared for *IEEE Transactions on Aerospace and Electronic Systems*.

---

## 1. Significance & Novelty
**Rating: 4 (Good)**
The paper addresses a critical gap in the literature: the lack of closed-form sizing relationships for "mega-constellation" scale coordination ($N=10^5$). While high-level architectural studies exist, this work provides specific, byte-level accounting and a rigorous feasibility framework (Test A/Test B) that links protocol overhead to physical layer constraints. The derivation of the campaign duty factor ($d$) to parameterize episodic workloads is a significant contribution, moving the field away from unrealistic continuous-duty assumptions.

## 2. Methodological Soundness
**Rating: 5 (Excellent)**
The methodology is robust. The authors have successfully integrated a discrete event simulation (DES) with a slot-level TDMA simulator and analytical bounds. The distinction between Model S (simplified, for bounding) and Model C (CCSDS-grounded, for design) is handled with excellent rigor; the authors explicitly warn against using Model S for recommendations. The use of Gilbert-Elliott (GE) models to stress-test ARQ strategies adds necessary realism.

## 3. Validity & Logic
**Rating: 5 (Excellent)**
The internal logic is consistent. The derivation of the slot efficiency $\gamma$ as a rate-dependent variable (decreasing as PHY rate increases due to fixed overheads) is counter-intuitive but mathematically correct and well-explained. The coupling analysis between ARQ and TDMA timing (Table VII) effectively demonstrates why simple bandwidth calculations fail at the margins. The feasibility arguments are conservative and well-bounded.

## 4. Clarity & Structure
**Rating: 4 (Good)**
The paper is dense but well-organized. The "Rate Ladder" (Table IV) and the "Feasibility Test" (Algorithm 1) are excellent tools for practitioners. However, the distinction between the "1 kbps logical budget" and the "35 kbps PHY rate" requires careful reading to avoid confusion, though the authors have added text to clarify this.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**
The authors provide a clear Data Availability statement with a GitHub link. The AI disclosure is transparent and specific (ideation/editing only, not result generation).

## 6. Scope & Referencing
**Rating: 4 (Good)**
The referencing is adequate, covering standard CCSDS documents, swarm robotics literature, and recent constellation management papers. The scope is appropriately limited to per-cluster sizing, with fleet-level scaling acknowledged as a projection requiring future work.

## 7. Mathematical Rigor
**Rating: 5 (Excellent)**
The closed-form equations for overhead ($\eta$) and slot efficiency ($\gamma$) are derived from first principles and anchored in standards. The probabilistic bounds for AoI and GE recovery are sound.

## 8. Simulation & Data Analysis
**Rating: 4 (Good)**
The DES provides necessary verification of the analytical models, particularly regarding buffer sizing tails. The slot-level simulation adds critical insight into the ARQ/timing interaction. The lack of external hardware validation is a limitation, but one that is clearly acknowledged and mitigated by sensitivity analyses.

## 9. Practical Applicability
**Rating: 5 (Excellent)**
This is the paper's strongest point. It moves beyond abstract theory to provide actionable design equations (Eq. 12) and lookup tables (Table VIII) that engineers can immediately apply. The "What-If" nature of the GE analysis allows it to remain useful even without specific channel measurements.

## 10. Overall Quality
**Rating: 5 (Excellent)**
This is a high-quality technical paper that solves a specific engineering problem with rigor. It effectively bridges the gap between network theory and spacecraft operations.

---

## Major Issues

1.  **Clarification of the "1 kbps" vs. "35 kbps" Constraint**
    *   **Issue:** While the text explains that 1 kbps is a logical allocation and 35 kbps is the PHY rate, the abstract and introduction could still confuse a hurried reader. The phrase "1 kbps budget" appears frequently alongside "infeasible at 24 kbps."
    *   **Why it matters:** A reader might mistakenly believe the system requires only 1 kbps of link capacity, missing the critical finding that bursty TDMA ingress requires a 35 kbps pipe to satisfy timing constraints.
    *   **Remedy:** In the Abstract and Section I, explicitly define the 1 kbps as a "Time-Averaged Per-Node Traffic Allocation" and the 35 kbps as the "Burst-Rate Coordinator Ingress Requirement."

2.  **Spatial Reuse ($R=3$) Justification**
    *   **Issue:** The assumption of a spatial reuse factor of $R=3$ for fleet-level scaling is stated as an "order-of-magnitude plausibility argument."
    *   **Why it matters:** If $R=3$ is optimistic (e.g., due to sidelobes or dynamic geometry), the fleet-level cycle time $T_c^{fleet}$ could double or triple, potentially invalidating the global coordination premise.
    *   **Remedy:** Add a brief sensitivity sentence in Section V.C: "If realistic antenna patterns require $R=7$ (standard cellular reuse), the required number of frequency channels $F$ would need to increase from 4 to ${\sim}9$ to maintain the same update rate."

## Minor Issues

1.  **Table II Notation:** The definition of $\alpha_{RX}$ is hidden in the table. Please explicitly state in the caption or text that this is a *derived* value, not an input parameter, to prevent designers from arbitrarily setting it.
2.  **Figure 4 (Buffer CDF):** The distinction between the "Bernoulli" and "ON/OFF" lines is subtle. Ensure the legend clearly distinguishes these, perhaps by noting "Memoryless" vs. "Correlated."
3.  **Section IV.J (Gamma):** The explanation of why $\gamma$ decreases as rate increases is excellent. Consider adding a small textual cue (e.g., "Note:") to draw attention to this, as it defies initial intuition.
4.  **Typos:** Check Eq. 5 for consistency in the ceiling function brackets.

---

## Overall Recommendation
**Recommendation: Accept with Minor Revisions**

This manuscript represents a significant contribution to the field of spacecraft swarm coordination. It successfully transitions from high-level architectural concepts to rigorous, standards-based engineering sizing.

The authors have robustly addressed previous concerns regarding the realism of the workload (via the campaign duty factor $d$) and the validity of the slot efficiency (via the CCSDS-anchored Model C). The shift from a generic $\gamma=0.85$ to a rate-dependent $\gamma(R_{PHY})$ derived from Proximity-1 framing significantly strengthens the physical layer credibility.

The "Two-Test Feasibility Framework" is a valuable conceptual tool for the community. The paper is ready for publication subject to the minor clarifications regarding bandwidth definitions and spatial reuse sensitivity.

---

## Constructive Suggestions

1.  **Enhance Algorithm 1:** Add a step that explicitly checks for the "Rate Paradox." If a user increases $R_{PHY}$ to gain margin, but the resulting drop in $\gamma$ causes a violation (rare, but possible in edge cases), the algorithm should flag it.
2.  **Visualizing the "Cliff":** In Figure 5 (Gamma vs. Rate), consider annotating the "Infeasible Region" (below 30 kbps) with a red background or text indicating "Timing Violation" to make the feasibility cliff immediately apparent.
3.  **Hardware-in-the-Loop Context:** In the discussion, briefly mention that while external validation is absent, the derived margins (18.8% at 35 kbps) are specifically intended to absorb the discrepancies found in typical hardware-in-the-loop tests (e.g., processing jitter). This strengthens the defense of the theoretical results.