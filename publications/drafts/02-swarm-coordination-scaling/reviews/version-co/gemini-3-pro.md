---
paper: "02-swarm-coordination-scaling"
version: "co"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-03-03"
recommendation: "Unknown"
---

Here is a comprehensive peer review of the manuscript **"Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms"** (Version CO).

---

# Peer Review Report

**Journal:** IEEE Transactions on Aerospace and Electronic Systems
**Manuscript ID:** [Assigned by Editor]
**Title:** Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms
**Version:** CO

## 1. Significance & Novelty
**Rating: 4 (Good)**
The paper addresses a critical gap in the literature: the specific sizing of communication architectures for "mega-swarms" ($10^3$--$10^5$ nodes) where centralized ground control is untenable, yet full mesh networking is bandwidth-prohibitive. The derivation of closed-form sizing equations that link byte-level budgets to physical-layer TDMA constraints is a significant contribution for systems engineers. The novelty lies not in the invention of new protocols, but in the rigorous synthesis of existing standards (CCSDS) with queueing theory to create a "design manual" for this specific operational regime.

## 2. Methodological Soundness
**Rating: 5 (Excellent)**
The methodology is robust. The authors employ a multi-tiered approach: analytical derivation, discrete event simulation (DES) for message-level statistics, and a slot-level simulator for TDMA timing verification.
*   **Strengths:** The explicit separation of "byte budget" (Layer 1) and "airtime schedulability" (Layer 2) is excellent and prevents the common error of confusing throughput with schedulability. The anchoring of the slot efficiency parameter ($\gamma$) in CCSDS Proximity-1 framing adds necessary realism.
*   **Validation:** The use of DES to verify the analytical means (Tier 1) and the use of slot-level simulation to uncover ARQ/TDMA coupling (Tier 2) is methodologically sound. The authors are transparent about the lack of external hardware validation (Tier 3), which is acceptable for a design-theory paper.

## 3. Validity & Logic
**Rating: 5 (Excellent)**
The internal logic is consistent. The transition from the earlier version's generic $\gamma=0.85$ to the calculated $\gamma \approx 0.76$ (based on CCSDS) strengthens the validity significantly. The argument that 24 kbps is infeasible while 30 kbps is the theoretical minimum is mathematically supported by the margin analysis. The distinction between the "stress case" ($d=1$) as a theoretical bound versus the operational reality ($d \approx 0.1$) is logically sound and necessary for realistic sizing.

## 4. Clarity & Structure
**Rating: 4 (Good)**
The paper is dense but well-organized. The "Rate Ladder" (Table IV) and the "Feasibility Test" (Algorithm 1) are excellent tools for the reader.
*   **Critique:** The distinction between "Information Rate" and "PHY Rate" is handled well, but the reader must pay close attention to the subscripts. The "Unmodeled Overhead Inventory" (Table VI) is a highlight of clarity, explicitly accounting for where the margin goes.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**
The authors provide a clear Data Availability statement pointing to a repository. The AI disclosure is specific and appropriate (ideation/editing only, not data generation). There are no apparent conflicts of interest or plagiarism concerns.

## 6. Scope & Referencing
**Rating: 4 (Good)**
The scope is appropriate for TAES. The referencing covers the necessary bases: swarm robotics, constellation management, and CCSDS standards.
*   **Critique:** While the CCSDS references are strong, the paper could benefit from slightly more engagement with recent "mega-constellation" networking papers (e.g., from *IEEE/ACM Transactions on Networking*) to further differentiate this coordination-layer work from routing-layer work.

---

## Major Issues

1.  **Clarification of the "Suspension" Mode during RF-Backup**
    *   **Issue:** Section III-B-2 mentions that during RF-backup (UHF), hierarchical coordination is "suspended" and nodes enter safe-hold. However, the abstract and introduction imply the architecture is sized for the 1 kbps budget to guarantee invariance.
    *   **Why it matters:** There is a slight contradiction. If the hierarchy is suspended during UHF backup, then the sizing analysis for the hierarchy (Sections IV-V) applies strictly to the S-band Coordination Channel (35 kbps), not the UHF link.
    *   **Remedy:** Explicitly state in the Abstract and Conclusion that the sizing equations apply to the *S-band Coordination Channel* which is sized to support the hierarchy even when the high-speed Optical ISL is down. Clarify that the UHF link is a "survival mode" only, not a "coordination mode." (Note: Table II attempts this, but the text should be more explicit).

2.  **Sensitivity of $\gamma$ to Acquisition Time Assumptions**
    *   **Issue:** The derivation of $\gamma \approx 0.76$ relies on specific assumptions about acquisition time ($T_{acq} = 5$ ms) and guard bands. If a radio requires a longer preamble for cold-start acquisition (e.g., 10-20 ms), $\gamma$ drops precipitously, potentially rendering 35 kbps insufficient.
    *   **Why it matters:** Hardware realities vary. A practitioner using a radio with slow lock times might fail if they rely solely on the $\gamma=0.76$ figure.
    *   **Remedy:** Add a sensitivity plot or a small table showing $\gamma$ and required PHY rate as a function of $T_{acq}$ (e.g., 2ms, 5ms, 10ms, 20ms). This would make the "design manual" aspect of the paper much more robust to hardware variation.

3.  **Contextualization of the "Stress Case" ($d=1$)**
    *   **Issue:** While the paper correctly identifies $d=1$ as an upper bound, the resulting overhead ($\eta \approx 46\%$) is high enough that a casual reader might dismiss the architecture as inefficient.
    *   **Why it matters:** It is crucial to emphasize that this high overhead is acceptable *because* it is episodic.
    *   **Remedy:** In the Abstract and Conclusion, explicitly pair the "46% stress case" with the "5-10% routine case" in the same sentence to ensure the efficiency of the nominal state is not lost.

## Minor Issues

1.  **Table II Footnote:** The footnote regarding the 1 kbps budget is helpful, but could be moved to the main text for better visibility, as this is a core design constraint.
2.  **Figure 4 (Recovery):** Ensure the legend explicitly defines the difference between the solid and dashed lines if not fully clear in the caption.
3.  **Equation 11 (Stagger):** Define $\lceil \cdot \rceil$ as the ceiling function for clarity, though it is standard notation.
4.  **Typos:** Check Section IV-J for "unsubscripted $\gamma$" usage—ensure consistency throughout the text.
5.  **Reference Style:** Ensure all CCSDS citations include the specific Blue/Green book number (which they currently appear to do, but verify against latest versions).

---

## Overall Recommendation

**Recommendation: Accept with Minor Revisions**

**Summary:**
This is a high-quality manuscript that successfully bridges the gap between high-level swarm algorithms and low-level communication constraints. The authors have rigorously addressed previous concerns regarding the slot efficiency parameter ($\gamma$), replacing the generic 0.85 estimate with a solid derivation based on CCSDS Proximity-1 framing ($\gamma \approx 0.76$). This change fundamentally strengthens the paper's recommendation of a 35 kbps PHY rate.

The "Two-Layer Feasibility Framework" is a valuable contribution to the field, providing a clear method for sizing these complex systems. The distinction between the byte budget (Layer 1) and TDMA airtime (Layer 2) is handled with mathematical precision.

The revisions requested are primarily regarding clarity and robustness: ensuring the distinction between the "Coordination Channel" and the "Survival Link" is absolute, and expanding the sensitivity analysis of the acquisition time to ensure the design equations hold for a wider range of radio hardware. With these minor changes, the paper will be an excellent addition to the journal.

## Constructive Suggestions (Ordered by Impact)

1.  **Add an "Acquisition Sensitivity" Plot:** Create a figure showing "Minimum Viable PHY Rate" on the Y-axis vs. "Acquisition Time ($T_{acq}$)" on the X-axis. This will visually demonstrate why the 35 kbps recommendation is safe for standard radios but might need adjustment for slower radios.
2.  **Refine the "Suspension" Terminology:** In Section III, clarify that the architecture has *three* tiers of connectivity: Optical (Data), S-band (Coordination), and UHF (Survival). The paper focuses on sizing the *middle* tier.
3.  **Expand the "Unmodeled Overhead" Discussion:** In Section V, briefly mention how Doppler shift compensation might eat into the guard band if not perfectly compensated, reinforcing the need for the 18.8% margin at 35 kbps.