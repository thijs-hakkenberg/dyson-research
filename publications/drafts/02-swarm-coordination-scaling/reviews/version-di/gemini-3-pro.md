---
paper: "02-swarm-coordination-scaling"
version: "di"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-03-06"
recommendation: "Unknown"
---

Here is a rigorous peer review of the manuscript "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version DI), prepared for *IEEE Transactions on Aerospace and Electronic Systems*.

---

# Peer Review Report

**Manuscript ID:** [Assigned by Editor]
**Title:** Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms
**Version:** DI

## 1. Significance & Novelty
**Rating: 4 (Good)**
The paper addresses a critical gap in the literature: the specific sizing of coordination protocols for "mega-constellation" scale swarms ($10^4$--$10^5$ nodes) under strict bandwidth constraints. While high-level architectural studies exist, this work provides closed-form, byte-level accounting that links physical layer timing (TDMA) with application-layer logic (consensus/reporting). The derivation of the "two-test" feasibility framework is a valuable contribution for systems engineers. The novelty lies in the detailed coupling of CCSDS Proximity-1 framing overheads with swarm coordination logic, a level of detail often glossed over in formation-flying literature.

## 2. Methodological Soundness
**Rating: 5 (Excellent)**
The methodology is rigorous. The authors employ a multi-tiered simulation approach (Cycle-aggregated DES, Slot-level TDMA simulation, and Packet-level framing analysis) that is well-justified. The transition from the earlier simplified $\gamma \approx 0.85$ to a standards-derived $\gamma(R_{\text{PHY}})$ based on CCSDS Proximity-1 is a significant improvement in fidelity. The use of the Gilbert-Elliott (GE) model as a "what-if" design tool rather than a predictive truth is methodologically responsible given the lack of on-orbit ISL data.

## 3. Validity & Logic
**Rating: 5 (Excellent)**
The internal logic is consistent. The distinction between the byte-budget (Test A) and airtime-schedulability (Test B) is clearly articulated. The analysis of the "stress case" ($\eta \approx 46\%$) is now properly contextualized as an episodic upper bound rather than a steady-state requirement. The counter-intuitive finding that intra-cycle ARQ is ineffective under slow-fading conditions ($\tau_c \geq T_c$) is logically sound and mathematically supported by the Markov analysis.

## 4. Clarity & Structure
**Rating: 4 (Good)**
The paper is dense but well-structured. The "Rate Ladder" (Table IV) and the "Feasibility Test" algorithm (Algorithm 1) are excellent synthesis tools that make the complex derivation actionable. However, the distinction between "Model C" (primary) and "Model S" (illustrative) needs to be maintained strictly to avoid confusion; while the text is careful, the sheer number of parameters ($d$, $q$, $\gamma$, $\alpha_{RX}$) requires the reader to pay close attention.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**
The authors provide a clear Data Availability statement pointing to a repository with source code and datasets. The acknowledgment of AI assistance in the ideation phase (but not result generation) is transparent and aligns with emerging publication standards.

## 6. Scope & Referencing
**Rating: 4 (Good)**
The scope is appropriate for TAES. The referencing covers the necessary bases, from classical queueing theory (Kleinrock) to modern constellation networking (Handley, del Portillo) and CCSDS standards. The connection to swarm robotics literature (Brambilla, Dorigo) is present but could be strengthened by contrasting the "static cluster" assumption here with dynamic ad-hoc networking often seen in robotics.

---

## Major Issues

1.  **Validation of the "Static Membership" Assumption for Cross-Plane Links**
    *   **Issue:** The manuscript relies heavily on static cluster membership ($k_c = 50$--$500$). While Section V-C mentions J2 perturbations and cross-plane re-association costs ($<0.5\%$), this is a critical simplification for a paper claiming applicability to "Large Autonomous Space Swarms." In mega-constellations (e.g., Walker Delta patterns), cross-plane ISLs are highly dynamic.
    *   **Why it matters:** If cluster membership changes frequently (e.g., every few minutes due to orbital dynamics), the "handoff" overhead (Raft election + state transfer) might dominate the byte budget, invalidating the $\eta$ calculations.
    *   **Remedy:** The paper needs a more rigorous justification for the static assumption. Explicitly state that this architecture targets *intra-plane* or *co-orbital* clusters primarily, or provide a quantitative bound on how often topology changes occur in a representative Walker constellation to prove the $<0.5\%$ claim is robust.

2.  **Sensitivity of $\gamma$ to Acquisition Time ($T_{acq}$)**
    *   **Issue:** The recommendation of 35 kbps relies on $\gamma_{35} \approx 0.732$, derived assuming $T_{acq} = 5$ ms. However, Table VII shows that if $T_{acq}$ rises to 19 ms, the margin vanishes. In non-coherent burst-mode receivers, acquisition can be highly variable.
    *   **Why it matters:** If hardware reality forces $T_{acq}$ to 10-15 ms (common in lower-cost radios), the 35 kbps link becomes infeasible, and the design breaks.
    *   **Remedy:** Add a "Safety Factor" recommendation to Algorithm 1. Rather than just checking `margin > 0`, the algorithm should enforce `margin > k * T_slot` (where $k$ is related to cluster size) to absorb acquisition variance.

3.  **Unicast Command Latency Contextualization**
    *   **Issue:** The paper notes that unicast commands to the whole cluster require a 19-cycle stagger ($L_{cmd} = 19$, or ~190s).
    *   **Why it matters:** For some "autonomy" applications (e.g., coordinated collision avoidance requiring distinct trajectories per node), 190s might be too slow.
    *   **Remedy:** Explicitly categorize which autonomy tasks are compatible with this latency. Clarify that "tight formation control" is *not* supported by this S-band architecture and must use the optical ISL, reinforcing the hierarchical nature of the physical layer.

## Minor Issues

1.  **Notation Overload:** The variable $\eta$ is used for protocol overhead, while $\eta_{total}$ includes the baseline. Ensure $\eta$ is never used as a generic efficiency variable (confusing it with $\gamma$). The definitions in Table I are clear, but the text must be consistent.
2.  **Figure Legibility:** Figure 3 (Coordinator Buffer CDF) is dense. Ensure the difference between the "Bernoulli" and "ON/OFF" lines is distinguishable in black-and-white print.
3.  **Algorithm 1 Clarification:** In Line 6, $\alpha_{RX}$ is calculated. It would be helpful to explicitly state that $\alpha_{RX}$ cannot exceed 1.0 (a sanity check).
4.  **Typos:** Section IV-A mentions "margin = -1,300 ms" for 24 kbps. While mathematically correct (negative margin), phrasing it as "deficit of 1,300 ms" is clearer.

---

## Overall Recommendation
**Recommendation: Accept with Minor Revisions**

This is a high-quality, technically sound manuscript that offers a significant contribution to the systems engineering of large-scale space swarms. The derivation of the sizing equations is robust, and the shift to CCSDS-based framing analysis (Model C) addresses the fidelity concerns of previous iterations. The paper successfully bridges the gap between abstract networking theory and practical link-budget constraints.

The "Two-Test" framework is a useful tool for practitioners. The paper is honest about its limitations (lack of external validation, reliance on GE models). The revisions requested (Major Issues) are primarily regarding the *bounds* of applicability (dynamic topology and acquisition variance) rather than the fundamental derivation. Addressing these will make the paper a definitive reference for constellation designers.

---

## Constructive Suggestions

1.  **Enhance Algorithm 1:** Modify the algorithm to output a "Recommended Hardware Specification" based on the inputs. For example, if the user inputs $T_{acq}=20$ms, the algorithm should flag that standard Proximity-1 timing is insufficient and suggest a specific stability requirement for the oscillator or a higher PHY rate.
2.  **Visualizing the "Cliff":** Consider adding a heatmap visualization of Feasibility (Binary or Margin %) with axes $k_c$ (Cluster Size) and $R_{PHY}$ (Data Rate). This would instantly show the "cliff" where 24 kbps fails and 30+ kbps succeeds, providing a powerful visual aid for the "35 kbps recommendation."
3.  **Hardware-in-the-Loop Context:** In the discussion, briefly mention how a practitioner would validate $\gamma$ on the bench. A sentence suggesting "measuring the distribution of $T_{acq}$ on engineering models" would bridge the gap between the paper's theory and the "Validation Roadmap."