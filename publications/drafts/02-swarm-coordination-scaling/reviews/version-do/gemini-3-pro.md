---
paper: "02-swarm-coordination-scaling"
version: "do"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-03-07"
recommendation: "Unknown"
---

Here is a rigorous peer review of the manuscript "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version DO).

---

# Peer Review Report

**Manuscript ID:** [Assigned by Editor]
**Title:** Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms
**Version:** DO

## 1. Significance & Novelty
**Rating: 5 (Excellent)**
The manuscript addresses a critical gap in the literature: the specific intersection of mega-constellation scale ($10^4+$ nodes) and low-bandwidth coordination protocols. While routing in mega-constellations is well-studied, the *control plane* sizing for autonomous coordination is not. The derivation of closed-form sizing equations that link information-layer byte budgets to physical-layer TDMA constraints is a significant contribution for system architects. The introduction of the "campaign duty factor" ($d$) to model episodic workloads is a novel and necessary addition to standard traffic modeling.

## 2. Methodological Soundness
**Rating: 5 (Excellent)**
The methodology is robust. The authors employ a multi-modal validation strategy: analytical derivation, discrete-event simulation (DES), and a completely independent packet-level simulation (NS-3). The inclusion of a "matched-assumptions" experiment to isolate discrepancies between the analytical model and NS-3 is a hallmark of high-quality engineering research. The Gilbert-Elliott (GE) channel model is applied correctly as a sensitivity tool rather than a predictive oracle.

## 3. Validity & Logic
**Rating: 4 (Good)**
The logic is generally sound. The two-test feasibility framework (Test A and Test B) is logically consistent. The distinction between the "stress case" (continuous commanding) and nominal operations is now well-articulated via the $d$ parameter.
*Critique:* The fleet-level spatial reuse argument ($R=7$) remains the weakest logical link. While the authors acknowledge it is "provisional," the jump from cluster-level rigor to fleet-level assumptions is abrupt. However, within the scope of *per-cluster* sizing, the logic holds.

## 4. Clarity & Structure
**Rating: 5 (Excellent)**
The manuscript is exceptionally well-structured. The "Rate Ladder" (Table V) and the "Feasibility Test" algorithm provide clear, actionable guidance for practitioners. The notation is consistent, and the distinction between information rates and PHY rates is handled with unusual precision. The "Warning" regarding the difference between CCSDS and NS-3 framing overheads demonstrates attention to detail.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**
The authors provide a clear Data Availability statement pointing to a repository. The AI disclosure is specific, acknowledging the use of LLMs for ideation and editing but explicitly stating that results and data were not AI-generated. This sets a good standard for transparency.

## 6. Scope & Referencing
**Rating: 4 (Good)**
The literature review covers the necessary bases (swarm robotics, mega-constellation networking, CCSDS standards). The connection to DVB-RCS2 provides good industrial context.
*Critique:* The paper could benefit from slightly more engagement with recent work on "Age of Information" (AoI) in satellite networks beyond the basic citations, given that AoI is a key metric here.

## 7. Theoretical Depth
**Rating: 4 (Good)**
The derivation of $\gamma$ (slot efficiency) is grounded in first principles. The queueing analysis (AoI) is relatively standard but applied correctly. The theoretical treatment of the GE model's impact on ARQ effectiveness is insightful, particularly the distinction between fast and slow fading regimes relative to the cycle time $T_c$.

## 8. Simulation & Experimentation
**Rating: 5 (Excellent)**
The use of NS-3 to validate the custom Python DES is a major strength. The breakdown of the 3-8% discrepancy into framing, jitter, and scheduling residuals adds significant credibility to the results. The sensitivity analysis covering different slot structures (Table VII) preemptively answers "what-if" questions about protocol design choices.

## 9. Practical Applicability
**Rating: 5 (Excellent)**
This is the paper's strongest point. It is written for engineers. The lookup tables, the "Rate Ladder," and the explicit sizing algorithm are immediately useful for preliminary design reviews (PDRs). The focus on standard CCSDS framing ensures the results are relevant to actual flight hardware, not just academic abstractions.

## 10. Overall Quality
**Rating: 5 (Excellent)**
This is a high-quality manuscript that balances theoretical rigor with practical utility. It addresses the reviewer comments from previous versions (implied by the specific focus on $d$ and $\gamma$ consistency) effectively.

---

## Major Issues

1.  **Spatial Reuse Validation Gap:**
    *   **Issue:** The paper relies on a provisional assumption of spatial reuse factor $R=7$ to claim fleet-level feasibility. While the focus is per-cluster, the title implies "Large Autonomous Space Swarms," suggesting fleet-wide scalability.
    *   **Why it matters:** If $R$ must be 1 (no reuse) due to omnidirectional interference, the fleet-level cycle time blows up to infeasible levels ($G=25$).
    *   **Remedy:** The authors should explicitly calculate the "Break-even $R$"—i.e., what is the minimum $R$ required to keep $G=1$ or $G=2$? This is briefly mentioned in text, but a small plot or table showing $T_c^{\text{fleet}}$ vs. $R$ would clarify the boundary conditions for fleet scalability without requiring a full RF simulation.

2.  **Turnaround Time Sensitivity:**
    *   **Issue:** The analysis assumes a specific guard time based on a generic turnaround. COTS S-band transceivers vary wildly in TX/RX switching time (from <1ms to >50ms).
    *   **Why it matters:** If a radio requires 20ms to switch, the guard time increases, potentially invalidating the 35 kbps recommendation.
    *   **Remedy:** Add a sensitivity line to Figure 2 or a brief discussion quantifying the maximum allowable turnaround time before the 35 kbps link breaks the 1% deadline miss threshold. (e.g., "The 35 kbps design closes as long as $T_{turnaround} < X$ ms").

## Minor Issues

1.  **Table I (Notation):** The definition of $\eta$ includes $d$, but $\eta_{total}$ adds the 20.5% baseline. Ensure the text consistently distinguishes between protocol overhead ($\eta$) and total channel utilization ($\eta_{total}$).
2.  **Section II-C (Campaign Duty Factor):** The claim that "stress case occurs <1% of operational time" is stated as a fact. It should be framed as a "design assumption" or "operational constraint."
3.  **Equation 5 (Gamma):** The term $T_{framing}$ uses $R_{FEC}$ in the denominator. Please clarify if the framing bits (ASM, etc.) are indeed FEC encoded. In some CCSDS implementations, ASMs are attached *after* coding. If they are encoded, the formula is correct; if not, it needs adjustment. (The text says "framing bits are FEC-encoded per CCSDS practice," which is generally true for Proximity-1, but worth a double-check against the specific synchronization strategy).
4.  **Figure 3 (NS-3 Validation):** The caption mentions a "shaded band." Ensure this is visible in grayscale print.
5.  **References:** Ensure all URL references (e.g., Project Dyson) are accessible and stable.

## Overall Recommendation
**Recommendation: Accept with Minor Revisions**

This manuscript presents a highly relevant, rigorous, and practical framework for sizing coordination channels in large satellite swarms. The introduction of the "campaign duty factor" ($d$) successfully resolves previous concerns regarding workload realism, and the independent NS-3 validation provides high confidence in the results. The "Rate Ladder" and $\gamma$ derivations are valuable contributions to the field.

The primary reason for "Minor Revisions" rather than a straight "Accept" is the need to slightly fortify the fleet-level spatial reuse argument (Major Issue 1) and bound the hardware turnaround time requirements (Major Issue 2). These are clarifications rather than structural defects. Once addressed, this paper will serve as a standard reference for swarm communication architecture.

## Constructive Suggestions

1.  **Enhance the "Break-even" Analysis:** In Section IV-D (or Discussion), explicitly state: "For the proposed architecture to scale to $10^5$ nodes, the physical layer must support a spatial reuse factor of at least $R=3$." This sets a clear requirement for the RF subsystem designers.
2.  **Clarify "Cold Start":** In Table VII, explicitly define what "Cold-start" implies for the reader (i.e., no prior synchronization state). This emphasizes why it is the conservative bound.
3.  **AoI Context:** In the Discussion, briefly contrast the calculated AoI (5s) with typical GNSS Time To First Fix (TTFF) or orbit propagation errors to contextualize whether 5s is "good" or "bad" for collision avoidance. (e.g., "A 5s AoI is negligible compared to the 2-day propagation error growth...").