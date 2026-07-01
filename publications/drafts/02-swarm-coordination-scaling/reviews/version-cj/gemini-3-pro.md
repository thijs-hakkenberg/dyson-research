---
paper: "02-swarm-coordination-scaling"
version: "cj"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-03-02"
recommendation: "Accept with Minor Revisions"
---

Here is a comprehensive peer review of the manuscript "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version CJ), prepared for *IEEE Transactions on Aerospace and Electronic Systems*.

---

# Peer Review Report

**Manuscript ID:** [Assumed Version CJ]
**Title:** Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms
**Target Journal:** IEEE Transactions on Aerospace and Electronic Systems

## 1. Significance & Novelty
**Rating: 5 (Excellent)**
This paper addresses a critical gap in the literature: the lack of closed-form sizing relationships for coordination architectures in the "mega-constellation" regime ($10^3$--$10^5$ nodes). While existing literature covers small swarms ($<100$ nodes) or networking protocols for routing, this work uniquely tackles the *coordination* layer (command dissemination, status aggregation, and fault recovery) with rigorous byte-level accounting. The derivation of a two-layer feasibility framework (byte budget + TDMA airtime) is a significant contribution that will likely become a standard reference for systems engineers designing future constellation management systems.

## 2. Methodological Soundness
**Rating: 5 (Excellent)**
The methodology is robust and multi-faceted. The authors employ a "triangulation" approach: analytical closed-form equations are verified against a Discrete Event Simulation (DES) for mean-value correctness and distributional analysis, and further anchored by a slot-level TDMA simulator to capture physical-layer timing constraints. The explicit derivation of the slot efficiency parameter ($\gamma$) from CCSDS Proximity-1 standards (rather than assuming an arbitrary efficiency) adds significant engineering credibility. The treatment of correlated losses via the Gilbert-Elliott model is mathematically sound and provides necessary realism over simple Bernoulli loss models.

## 3. Validity & Logic
**Rating: 4 (Good)**
The internal logic is consistent. The distinction between message-layer overhead ($\eta$) and physical-layer schedulability is clearly maintained. The argument for the 35 kbps design point is logically derived from the margin analysis.
*Critique:* The assumption that command generation is centralized (making $\eta_{\text{cmd}}$ topology-invariant) is a strong one. While the authors address distributed planning in Section V-C, the transition from centralized to distributed logic could be smoother. However, the logic regarding the "stress case" bounding continuous operations is sound.

## 4. Clarity & Structure
**Rating: 5 (Excellent)**
The manuscript is exceptionally well-structured. The progression from research questions to analytical derivation, then to simulation verification, and finally to sensitivity analysis is intuitive. The "Rate Ladder" (Table V) and the "Feasibility Test" algorithm are standout features that make the theoretical work immediately actionable for practitioners. The distinction between Model S (simplified) and Model C (CCSDS) is handled with great clarity, preventing confusion about where the overhead numbers come from.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**
The authors provide a clear data availability statement pointing to a repository with source code and datasets. The acknowledgment section transparently discloses the use of AI for ideation and prose editing, adhering to modern ethical guidelines.

## 6. Scope & Referencing
**Rating: 4 (Good)**
The literature review covers the necessary bases (swarm robotics, constellation management, delay-tolerant networking). The mapping of the proposed work against reference baselines (Centralized Ground, Global-State Mesh) helps contextualize the contribution.
*Critique:* The paper would benefit from slightly more engagement with recent work on "serverless" or "edge computing" in space, which is the software-layer equivalent of the architectural trade-offs discussed here.

---

## Major Issues

1.  **Justification of the "Safe Mode" Independence Assumption**
    *   **Issue:** In Section III-B-2, the paper estimates the probability of simultaneous ISL outage and coordinator failure as independent events ($6.3 \times 10^{-12}$).
    *   **Why it matters:** Common-cause failures (e.g., a massive solar particle event or a software update bug) are the primary driver of catastrophic loss in large fleets. Assuming independence here risks significantly understating the criticality of the RF-backup mode.
    *   **Remedy:** The authors acknowledge this briefly, but it requires a stronger caveat. Please explicitly state that this probability is a *lower bound* and that common-mode failures would drive this rate higher, thereby reinforcing the necessity of the RF-backup sizing analysis.

2.  **Contextualization of the "Stress Case" ($\eta \approx 46\%$)**
    *   **Issue:** The abstract and introduction highlight the 46% overhead figure. A casual reader might interpret this as the system being inefficient.
    *   **Why it matters:** As shown in Table XI, routine operations are only 5-10%. The 46% figure is a theoretical upper bound ($d=1$).
    *   **Remedy:** In the Abstract and Conclusion, explicitly pair the 46% figure with the "routine" figure (5-10%) to prevent misinterpretation of the protocol's efficiency. (e.g., "Routine operations yield $\eta \approx 5\%$, while the theoretical stress-case bound is 46%").

3.  **Clarification of "Thundering Herd" Back-off**
    *   **Issue:** Section III-B-2 mentions the "thundering herd" problem during coordinator election and cites a 114s recovery time based on Slotted ALOHA throughput.
    *   **Why it matters:** Slotted ALOHA is unstable under saturation ($G > 1$). Without an explicit back-off mechanism (e.g., binary exponential back-off), the channel will collapse to zero throughput, not 36%.
    *   **Remedy:** Explicitly mention the back-off algorithm assumed (e.g., "assuming binary exponential back-off") to justify the convergence claim. The current text implies static probability ALOHA might suffice, which is incorrect for $N=100$ simultaneous transmitters.

## Minor Issues

1.  **Table II (Key Notation):** The definition of $\alpha_{\text{RX}}$ is specific to the $k_c=100$ case. Please clarify in the table caption or definition that this is an *example* value, or define it generally as $T_{\text{ingress}}/T_c$.
2.  **Figure 6 (AoI):** The y-axis should be clearly labeled as "Seconds" if it isn't already (hard to verify without the image, but standard practice).
3.  **Section IV-J (Packet Derivation):** The distinction between "Info-rate" and "PHY-rate" is crucial here. Ensure that every instance of "kbps" in this section is explicitly qualified as one or the other to avoid confusion.
4.  **Typos:**
    *   Section IV-A: "Phase-staggered scheduling... reducing drops" - ensure the figure reference matches the text description.
    *   References: Ensure all URLs in the bibliography are accessible or archived.

---

## Overall Recommendation
**Recommendation: Accept with Minor Revisions**

**Summary:**
This is an outstanding paper that brings rigorous systems engineering and quantitative analysis to the problem of coordinating massive satellite constellations. The authors have successfully navigated the trade-off between analytical tractability and simulation realism.

**Strengths:**
*   **The Two-Layer Framework:** The separation of byte-budget feasibility from TDMA airtime feasibility is a crucial insight for practitioners.
*   **Standards Anchoring:** Deriving $\gamma = 0.760$ from CCSDS Proximity-1 rather than guessing "0.8" or "0.9" sets a high standard for future work.
*   **Actionable Design Tools:** The "Rate Ladder," "Feasibility Test" algorithm, and GE sensitivity curves (Fig. 8b) are immediately useful for system designers.
*   **Rigorous Validation:** The use of three distinct modeling tiers (Analytical, DES, Slot-Sim) provides high confidence in the results.

**Critical Improvements Needed:**
The primary improvements needed are interpretative rather than technical. The authors must ensure the "stress case" overhead is not misinterpreted as the nominal operating point, and they should strengthen the justification regarding common-mode failures to fully motivate the RF-backup analysis. Addressing the stability of the ALOHA channel during election (via back-off) is the only technical correction required.

## Constructive Suggestions (Ordered by Impact)

1.  **Refine the Abstract:** Explicitly contrast the "Routine" overhead (5%) with the "Stress" overhead (46%) in the same sentence to highlight efficiency.
2.  **Expand Algorithm 1:** Consider adding a check for "Common Mode Failure" in the feasibility test, or at least a comment that $d$ (duty factor) might effectively become 1.0 during such events.
3.  **Visualizing the Margin:** In Figure 9 (Margin Sensitivity), consider shading the region that represents "Typical COTS Radio Performance" to help readers place their hardware on the curve.
4.  **Future Work:** Explicitly mention that while NS-3 is future work, the current analysis provides the *input traffic models* that such a simulation would require.