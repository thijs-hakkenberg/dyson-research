---
paper: "02-swarm-coordination-scaling"
version: "ch"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-03-01"
recommendation: "Accept with Minor Revisions"
---

Here is a rigorous peer review of the manuscript (Version CH), structured according to IEEE Transactions on Aerospace and Electronic Systems standards.

---

# Peer Review Report

**Manuscript ID:** [Assumed: TAES-2025-XXXX]
**Title:** Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms
**Version:** CH

## 1. Significance & Novelty
**Rating: 5 (Excellent)**
The paper addresses a critical gap in the literature: the lack of closed-form sizing relationships for spacecraft swarms in the $10^4$--$10^5$ node regime. While swarm robotics and mega-constellation routing are well-studied individually, the intersection—specifically the byte-level accounting of hierarchical coordination protocols under realistic link constraints—is novel. The derivation of a "two-layer" feasibility framework (byte budget vs. TDMA airtime) provides a significant contribution to the systems engineering of future autonomous fleets.

## 2. Methodological Soundness
**Rating: 5 (Excellent)**
The methodology is robust. The authors employ a multi-fidelity approach: analytical closed-form equations, a cycle-aggregated Discrete Event Simulation (DES) for distributional analysis, and a slot-level TDMA simulator for timing verification. The explicit derivation of the slot efficiency parameter ($\gamma$) from CCSDS Proximity-1 standards (Section IV-J) is a substantial improvement over previous iterations that relied on assumed efficiencies. The Gilbert-Elliott (GE) model is correctly applied to test correlated loss sensitivity.

## 3. Validity & Logic
**Rating: 4 (Good)**
The logic is generally sound. The distinction between "byte budget" feasibility and "airtime" feasibility is crucial and well-argued. The stress-case analysis ($d=1$) effectively bounds the problem, while the campaign duty factor ($d$) adds necessary realism.
*Critique:* The paper argues that intra-cycle ARQ is "structurally ineffective" for coherence times $\tau_c \ge T_c$. While logically valid for the parameters chosen, the mapping of physical obstruction mechanisms to these specific GE parameters (Table VIII) relies on estimation rather than empirical data. The authors acknowledge this limitation, but the strength of the conclusion depends heavily on the assumption that obstruction coherence is indeed $\ge 10$s.

## 4. Clarity & Structure
**Rating: 5 (Excellent)**
The manuscript is exceptionally well-organized. The progression from analytical models to simulation results to standards-based derivation is logical. Figures are high-quality and informative, particularly Fig. 10 (Coordinator Buffer CDF) and Fig. 15 (Gamma vs. Rate). The notation table is comprehensive. The distinction between Model S (simplified) and Model C (CCSDS) is handled with great clarity, preventing confusion about which assumptions apply to which result.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**
The authors provide a clear Data Availability statement with a GitHub link (though obviously a placeholder for review). The acknowledgment of AI assistance in the ideation phase is transparent and complies with emerging publication standards.

## 6. Scope & Referencing
**Rating: 4 (Good)**
The literature review covers swarm robotics, constellation management, and networking well. The references to CCSDS standards are appropriate.
*Critique:* The paper focuses heavily on the RF backup link (1 kbps). While justified as the "design-driving" constraint, the interaction between the optical ISL (for bulk transfer) and the RF control plane could be fleshed out slightly more, specifically regarding how optical link failures might cascade into the RF network.

---

## Major Issues

1.  **Justification of GE Parameters for ISL Blockage (Section IV-C)**
    *   **Issue:** The claim that intra-cycle ARQ is "structurally ineffective" rests on the assumption that blockage coherence time $\tau_c \ge T_c$ (10s). While Table VIII maps "Structural shadowing" to 1-10s, there is no citation or geometric derivation provided for this specific duration.
    *   **Why it matters:** If structural shadowing is actually faster (e.g., caused by a thin antenna boom passing quickly across the field of view of a tumbling satellite), $\tau_c$ could be $< 1$s, making intra-cycle ARQ viable.
    *   **Remedy:** Provide a brief geometric justification for the 1-10s estimate. For example, calculate the angular width of a solar array at typical spacecraft dimensions and divide by a representative tumble rate (e.g., $1^\circ$/s).

2.  **Coordinator Failure Recovery Timeline (Section III-B-2)**
    *   **Issue:** The paper states that RF-backup handoff takes $\sim 160$s. However, it is not clear if this accounts for the "thundering herd" problem. If a coordinator fails, $k_c=100$ nodes might simultaneously detect the timeout and attempt to initiate an election or report to a regional node.
    *   **Why it matters:** In a bandwidth-constrained environment (1 kbps), simultaneous control-plane signaling from 100 nodes could cause MAC collapse (Slotted ALOHA saturation), extending recovery time well beyond 160s.
    *   **Remedy:** Clarify if the 160s estimate includes MAC contention backoff for the election traffic. If not, add a caveat or a rough calculation of the contention delay (e.g., using standard Slotted ALOHA throughput $\approx 0.36$).

3.  **Unicast Command Staggering Operational Impact (Section IV-D)**
    *   **Issue:** Eq. 7 shows that unicast commands require a 31-cycle stagger ($L_{cmd}=31$). The paper notes this is feasible for byte budget but fails airtime.
    *   **Why it matters:** A 310-second latency for unicast commanding might be operationally unacceptable for certain fault recovery scenarios. The paper treats this as a "schedulability" result, but the operational consequence needs to be explicit.
    *   **Remedy:** Explicitly state in the text (near Table X) whether a 5-minute command latency is acceptable for the "Stress (unicast)" profile. If this profile represents emergency reconfiguration, 310s might be too slow.

## Minor Issues

1.  **Table I (Notation):** The symbol $\eta$ is defined as "Protocol overhead." It would be helpful to explicitly state here that this excludes the 20.5% baseline, to avoid confusion with $\eta_{total}$.
2.  **Fig. 6 (Margin Sensitivity):** The caption mentions "Star" and "Diamond" markers, but ensure these are clearly visible in the final high-resolution print.
3.  **Section IV-J (Gamma Decomposition):** The derivation uses "LDPC rate 7/8". Briefly mention why 7/8 was chosen over 1/2 (presumably to maximize rate at the cost of link margin, given the short ISL range).
4.  **Typos:**
    *   Section IV-A: "Phase-staggered scheduling... reduces drops." Ensure "drops" refers to queue overflows, not link errors.
    *   Table XI: Check the footnote regarding "Regime B". It says "TDMA airtime for retransmission is unavailable," which is correct, but the column header "Delivered" might imply success. Perhaps rename to "Theoretical Delivery (Byte Budget Only)."

---

## Overall Recommendation
**Recommendation: Accept with Minor Revisions**

**Summary:**
This is an excellent paper that provides a much-needed theoretical foundation for scaling spacecraft swarms. The authors have successfully moved beyond generic "swarm" concepts to provide rigorous, standards-grounded sizing equations. The distinction between message-layer feasibility and PHY-layer schedulability is a key insight. The "Version CH" improvements—specifically the CCSDS derivation of $\gamma$ and the rigorous treatment of the campaign duty factor ($d$)—have addressed previous potential weaknesses regarding realism.

The only substantive request is to strengthen the justification for the Gilbert-Elliott coherence time assumptions, as this drives the strong conclusion regarding ARQ infeasibility. With that clarification and the minor tweaks suggested, this paper will be a valuable reference for the aerospace community.

---

## Constructive Suggestions

1.  **Geometric Justification for $\tau_c$:** Add a back-of-the-envelope calculation in Section IV-C. Assume a 1m wide solar panel at 2m distance subtends $\sim 26^\circ$. If the tumble rate is $2^\circ/s$, the blockage lasts 13s. This simple check would firmly anchor the $\tau_c \ge T_c$ assumption.
2.  **Algorithm 1 Enhancement:** Consider adding a "Step 0" to Algorithm 1 that checks the link budget margin. If the link margin at the required modulation (for 30 kbps) is insufficient, the algorithm should terminate before checking byte budgets.
3.  **Future Work - MAC:** You correctly identify MAC contention as a Tier 3 validation gap. I suggest explicitly mentioning "reservation-based Slotted ALOHA" (R-ALOHA) as a potential candidate for future investigation, as it bridges the gap between the random access needed for election and the TDMA needed for steady-state.