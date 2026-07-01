---
paper: "02-swarm-coordination-scaling"
version: "cn"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-03-03"
recommendation: "Unknown"
---

Here is a rigorous peer review of the manuscript "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version CN).

---

# Peer Review Report

**Journal:** IEEE Transactions on Aerospace and Electronic Systems
**Manuscript ID:** [Assigned by Editor]
**Title:** Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms
**Version:** CN

## 1. Significance & Novelty
**Rating: 4 (Good)**
The paper addresses a critical gap in the literature: the "missing middle" between small-scale swarm robotics ($N < 100$) and mega-constellation networking ($N > 10,000$). While existing literature covers routing or formation flying separately, this work uniquely integrates byte-level protocol accounting with physical-layer TDMA constraints to derive closed-form sizing equations. The distinction between "byte budget" feasibility and "airtime" feasibility is a significant conceptual contribution for systems engineers. The novelty lies not in new mathematical invention, but in the rigorous synthesis of queueing theory, framing standards (CCSDS), and parametric simulation to create a design framework for large-scale autonomy.

## 2. Methodological Soundness
**Rating: 5 (Excellent)**
The methodology is robust and multi-layered. The authors successfully employ a "V&V tier" approach, using analytical equations to verify a Discrete Event Simulation (DES), and a slot-level simulator to identify emergent behaviors (like the ARQ-TDMA coupling) that the DES misses.
*   **Strengths:** The derivation of $\gamma$ (slot efficiency) from CCSDS Proximity-1 standards is a major improvement over previous versions, replacing arbitrary constants with physics-based values. The separation of ingress (RX) and egress (TX) constraints in the TDMA analysis is mathematically sound.
*   **Validation:** The use of Gilbert-Elliott (GE) models for correlated loss is appropriate for the domain, and the sensitivity sweep (Fig. 6b) is a highly practical design tool.

## 3. Validity & Logic
**Rating: 4 (Good)**
The internal logic is consistent. The transition from the 24 kbps infeasibility finding to the 35 kbps recommendation is well-supported by the margin analysis.
*   **Campaign Duty Factor ($d$):** The introduction of $d$ resolves previous concerns about unrealistic continuous workloads. The logic that routine operations ($d \approx 0.01-0.10$) are manageable while stress cases ($d=1$) are episodic bounds is sound.
*   **Gamma Unification:** The paper consistently applies $\gamma \approx 0.76$ (Model C) for decision-making, relegating Model S (0.95) to a comparison bound. This corrects inconsistencies found in earlier drafts.

## 4. Clarity & Structure
**Rating: 5 (Excellent)**
The manuscript is exceptionally well-structured. The "Rate Ladder" (Table V) and the "Feasibility Test" (Algorithm 1) are standout features that make the theoretical work immediately actionable for practitioners. The distinction between "Tier 1" (code verification) and "Tier 3" (external validation) is intellectually honest and clearly communicated. Figures are high-quality, particularly the margin sensitivity plots.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**
The authors provide a clear Data Availability statement pointing to a repository. The acknowledgment section transparently discloses the use of AI for ideation and editing, adhering to emerging IEEE policies. There are no apparent conflicts of interest or human subject concerns.

## 6. Scope & Referencing
**Rating: 4 (Good)**
The scope is well-defined (hierarchical coordination for $10^3-10^5$ nodes). The referencing is adequate, covering swarm theory, CCSDS standards, and queueing basics.
*   **Gap:** While CCSDS is well-cited, the paper could benefit from slightly more engagement with recent optical ISL networking papers (e.g., from the Starlink/Telesat technical community or recent IEEE networking conferences) to better contextualize why RF backup remains the critical bottleneck.

---

## Major Issues

1.  **Contextualization of the "Stress Case" ($\eta \approx 46\%$)**
    *   **Issue:** While the paper now defines $d$, the abstract and conclusion still heavily feature the 46% overhead figure. A casual reader might assume the system *always* runs at 46% overhead, which would be disqualifying for many mission designers.
    *   **Why it matters:** It risks making the architecture appear inefficient.
    *   **Remedy:** In the Abstract and Conclusion, explicitly pair the 46% figure with the phrase "episodic worst-case" and immediately contrast it with the routine overhead (5-9%). Ensure the distinction between *designing for capacity* (handling the peak) and *average utilization* is sharp.

2.  **Justification of the 1 kbps Constraint**
    *   **Issue:** The paper asserts the 1 kbps budget is driven by the RF-backup link. However, in modern constellations, the optical backbone is the primary control plane.
    *   **Why it matters:** Critics might argue that sizing the entire architecture based on a "survival mode" (RF backup) is overly conservative and limits capability.
    *   **Remedy:** Strengthen the argument in Section III-E. Explicitly state that *hierarchical coordination must be invariant to optical link failure*. If the control plane depends on Gbps optical links, the swarm becomes uncontrollable exactly when it is most vulnerable (tumbling/recovery). This "lowest common denominator" argument needs to be the central thesis for the 1 kbps choice.

3.  **Unicast Stagger Analysis ($L_{cmd}$)**
    *   **Issue:** The derivation of $L_{cmd} = 19$ cycles for unicast commands (Eq. 7) is mathematically correct but operationally severe (190 seconds latency).
    *   **Why it matters:** This high latency might be unacceptable for certain "Type 2" commands (e.g., immediate collision avoidance).
    *   **Remedy:** Explicitly discuss the operational workaround. Presumably, time-critical commands (Collision Avoidance) are *always* broadcast (Type 1, 1-cycle latency), while unicast is reserved for non-urgent tasks (software patching, orbit raising). Table IX hints at this, but the text should explicitly state that safety-critical commands are never subject to the 19-cycle stagger.

## Minor Issues

1.  **Table IV (Rate Ladder):** In Step 3, the derivation $27.1 / 0.908$ yields 29.84, rounded to 29.9. Please clarify in the footnote that $\alpha_{RX}$ is derived from the specific slot count at that rate, as $\alpha_{RX}$ itself changes slightly with PHY rate (due to fixed overheads).
2.  **Figure 6 (GE Recovery):** The caption mentions "DES bars" vs "Markov-chain analytical model." Ensure the visual distinction between the bars and the analytical lines is clear in black-and-white print.
3.  **Section IV-J (Gamma Decomposition):** The text mentions "Rate-1/2 LDPC makes 30 kbps infeasible." It would be helpful to briefly state *why* (i.e., it doubles the symbol rate/time, pushing ingress beyond $T_c$).
4.  **Typos/Phrasing:**
    *   Section III-B-2: "Triple fault... $1.8 \times 10^{-5}$/yr" - clarify if this is per cluster or fleet-wide.
    *   Section V-C: "Practitioners evaluate at their specific PHY rate." - Consider changing to "Practitioners *must* evaluate..." to emphasize this is a requirement.

---

## Overall Recommendation
**Recommendation: Accept with Minor Revisions**

This is a high-quality, rigorous manuscript that successfully translates theoretical swarm concepts into actionable systems engineering equations. The authors have robustly addressed the complexities of physical-layer timing, framing overhead, and correlated channel losses.

The "Two-Layer Feasibility Framework" is a valuable contribution to the aerospace community. The revision has successfully integrated the campaign duty factor ($d$) and anchored the slot efficiency ($\gamma$) in CCSDS standards, addressing the primary weaknesses of hypothetical earlier drafts.

The requested revisions are primarily regarding framing and emphasis—specifically, ensuring the "stress case" is not misinterpreted as nominal operation, and defending the "survival mode" bandwidth constraint more aggressively. Once these narrative points are sharpened, the paper is ready for publication.

## Constructive Suggestions (Ordered by Impact)

1.  **Strengthen the "Survival Mode" Argument:** Add a sentence to the Abstract or Introduction: "We size the coordination architecture for the RF-backup link (1 kbps) to guarantee control authority persists during optical link failures (tumbling/safe-mode), ensuring architectural invariance across all fault states."
2.  **Clarify Safety-Critical Latency:** In Section IV-F (Fleet Reuse/Stagger), explicitly state: "Safety-critical commands (e.g., collision avoidance) utilize Type 1 Broadcast (single-cycle latency); the 19-cycle stagger applies only to non-urgent unicast maintenance tasks."
3.  **Expand Validation Roadmap:** In Section V-B, suggest that "Software-Defined Radio (SDR) testbeds" could serve as an intermediate validation step between simulation and orbit, specifically for measuring $\gamma$ and acquisition times.
4.  **Visual Aid for Layer Mapping:** Consider a small flowchart or diagram illustrating the flow from Layer 1 (Byte Budget) $\to$ Layer 2 (Airtime) $\to$ Margin Check. This would complement Algorithm 1 visually.