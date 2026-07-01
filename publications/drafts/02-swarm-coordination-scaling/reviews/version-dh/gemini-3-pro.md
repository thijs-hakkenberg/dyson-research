---
paper: "02-swarm-coordination-scaling"
version: "dh"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-03-06"
recommendation: "Unknown"
---

Here is the peer review for the manuscript "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version DH).

---

**Reviewer:** Peer Reviewer #1
**Journal:** IEEE Transactions on Aerospace and Electronic Systems
**Manuscript ID:** [Assigned by Editor]
**Date:** October 26, 2023

---

### 1. Significance & Novelty
**Rating: 5 (Excellent)**
This paper addresses a critical gap in the literature regarding the "middle-ground" scaling of autonomous space systems. While swarm robotics literature handles small $N$ and mega-constellation literature handles routing, there is a lack of rigorous sizing models for the coordination layer of $10^3$--$10^5$ node fleets. The derivation of closed-form sizing equations that link physical layer constraints (TDMA timing, acquisition) directly to application-layer feasibility (byte budgets, campaign duty factors) is a significant contribution. The distinction between the "stress case" (continuous duty) and realistic episodic campaigns is particularly valuable for mission planners who often over-design for worst-case scenarios.

### 2. Methodological Soundness
**Rating: 5 (Excellent)**
The methodology is robust. The authors employ a multi-tiered approach: analytical derivation, discrete event simulation (DES) for traffic dynamics, and a specific slot-level simulator for TDMA timing verification.
*   **Strengths:** The transition from a simplified slot model (Model S) to a CCSDS-grounded model (Model C) is handled with exceptional rigor. The explicit accounting for acquisition times, guard bands, and FEC overhead in the $\gamma$ parameter is a highlight.
*   **Validation:** The use of DES to validate the analytical means (Tier 1) and the use of slot-level simulation to uncover ARQ coupling (Tier 2) is methodologically sound. The authors are honest about the lack of external hardware validation (Tier 3), which is acceptable for a design/sizing paper.

### 3. Validity & Logic
**Rating: 4 (Good)**
The internal logic is consistent. The two-test feasibility framework (Test A: Byte Budget, Test B: Airtime) is logical and clearly explained.
*   **Gamma Unification:** The shift to $\gamma \approx 0.73-0.76$ based on CCSDS Proximity-1 framing resolves previous ambiguities in the field regarding slot efficiency.
*   **Stress Case Context:** The paper successfully contextualizes the 46% overhead figure as a rare bound ($<1\%$ of time), preventing the reader from dismissing the architecture as inefficient.
*   **Minor Critique:** The reliance on the Gilbert-Elliott (GE) model for correlated loss is standard, but the specific parameter selection ($p_{BG}=0.50$) is heavily relied upon for the "inter-cycle recovery" recommendation. While sensitivity analysis is provided, the strong recommendation to abandon intra-cycle ARQ at 30 kbps hinges entirely on the coherence time assumption ($\tau_c \geq T_c$).

### 4. Clarity & Structure
**Rating: 5 (Excellent)**
The manuscript is exceptionally well-structured. The "Rate Ladder" (Table IV) and the "Gamma Decomposition" (Table VIII) are exemplary ways to present complex sizing trade-offs. The distinction between "Information Rate," "PHY Rate," and "Recommended Design Point" is clear. The notation table is comprehensive.

### 5. Ethical Compliance
**Rating: 5 (Excellent)**
The authors provide a clear Data Availability statement pointing to a repository. The AI disclosure is specific and appropriate (ideation/editing only, not data generation).

### 6. Scope & Referencing
**Rating: 5 (Excellent)**
The scope is perfectly aligned with *IEEE TAES*. The referencing covers the necessary bases: swarm theory, CCSDS standards, queueing theory, and recent constellation literature. The inclusion of DVB-RCS2 as a comparative baseline for TDMA efficiency is a nice touch.

---

### Major Issues

1.  **Clarification of the "Logical" 1 kbps Budget vs. Physical Link**
    *   **Issue:** In Section III.E and Table II, the paper states the per-node budget is 1 kbps, but the physical link is 35 kbps. While explained, the distinction between the *traffic allocation policy* (1 kbps) and the *physical channel capacity* (35 kbps) could be sharper in the Abstract and Introduction. A casual reader might think the radio hardware is limited to 1 kbps.
    *   **Why it matters:** This is the fundamental constraint of the paper. If readers confuse the allocation for the hardware limit, the TDMA analysis makes no sense.
    *   **Remedy:** In the Abstract, change "Under a 1 kbps time-averaged per-node traffic allocation" to "Under a 1 kbps logical traffic allocation (enforced via TDMA on a high-rate burst channel)."

2.  **Sensitivity of Inter-Cycle Recovery to $p_{BG}$**
    *   **Issue:** The recommendation to rely on inter-cycle recovery (Section IV.C) rather than intra-cycle ARQ at 30 kbps is based on $p_{BG}=0.50$. If a mission experiences fast fading (e.g., tumbling at high rates where $\tau_c \ll T_c$), intra-cycle ARQ becomes viable and perhaps preferred.
    *   **Why it matters:** The paper strongly advises against intra-cycle ARQ at 30 kbps. For a tumbling satellite, this might be bad advice.
    *   **Remedy:** In Section IV.C or the Conclusion, explicitly add a conditional statement: "If $\tau_c \ll T_c$ (fast fading), intra-cycle ARQ remains effective; however, for stabilized links or structural blockage ($\tau_c \geq T_c$), inter-cycle recovery is required." (Note: The manuscript touches on this, but it should be elevated to the "Constructive Suggestions" or "Design Equations" summary).

### Minor Issues

1.  **Table I (Notation):** The definition of $\alpha_{RX}$ is listed as a "Computed output." It would be helpful to explicitly state it is a function of $k_c$ and $R_{PHY}$ in the table description to reinforce that it is not a free parameter.
2.  **Figure 3 (Gamma vs. Rate):** The shaded region is labeled "feasible." Please clarify in the caption if this refers to Test A, Test B, or both.
3.  **Section IV.J (Gamma Decomposition):** The mention of "proprietary modems" achieving better acquisition times is vague. It might be better to phrase this as "non-standard fast-acquisition implementations."
4.  **Typos:**
    *   Section III.B.2: "The simulation assumes *static* cluster membership..." - Consider adding "(dynamic re-association discussed in Sec V.C)" for immediate context.

---

### Overall Recommendation
**Recommendation: Accept with Minor Revisions**

This is a high-quality manuscript that offers a rigorous, closed-form approach to sizing communication architectures for large space swarms. The authors have successfully addressed the complexities of TDMA timing, CCSDS framing overhead, and bursty campaign workloads.

The shift from a generic efficiency factor to a rate-dependent $\gamma(R_{PHY})$ derived from CCSDS Proximity-1 is a significant improvement over standard literature assumptions. The "Two-Test" framework provides a clear recipe for systems engineers.

The only required changes are clarifying the "logical vs. physical" bandwidth distinction in the abstract and adding a slightly stronger caveat regarding the channel coherence time assumption for the ARQ recommendation.

---

### Constructive Suggestions

1.  **Elevate the "Rate Ladder" (Table IV):** This is the most practical tool for engineers in the paper. Consider referencing it earlier in the Introduction or Section III as the roadmap for the results.
2.  **Algorithm 1 Refinement:** In Line 12 of Algorithm 1, the fallback to "inter-cycle recovery" is mentioned. It would be beneficial to add a step that estimates the AoI impact: `AoI_penalty = T_c / (1 - p_loss_inter_cycle)`.
3.  **Hardware Validation Note:** In Section V.B (Validation Roadmap), explicitly suggest that future work should characterize the distribution of $T_{acq}$ on actual flight radios (e.g., S-band transceivers common in CubeSats), as the variance in acquisition time is the largest unmodeled risk to the TDMA margin.