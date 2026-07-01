---
paper: "02-swarm-coordination-scaling"
version: "cz"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-03-05"
recommendation: "Unknown"
---

Here is a comprehensive peer review of the manuscript **"Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version CZ)**, prepared for *IEEE Transactions on Aerospace and Electronic Systems*.

---

## 1. Significance & Novelty
**Rating: 5 (Excellent)**
This paper addresses a critical gap in the literature: the specific sizing of communication control planes for mega-constellations ($10^4$--$10^5$ nodes). While much prior work focuses on high-speed data routing (ISL) or small-scale swarm robotics ($<100$ agents), this work rigorously defines the "coordination channel" requirements. The derivation of the 35 kbps requirement and the distinction between logical traffic allocation (1 kbps) and physical link dimensioning is a significant contribution to systems engineering for future autonomous fleets.

## 2. Methodological Soundness
**Rating: 4 (Good)**
The two-test feasibility framework (Test A: Byte Budget, Test B: TDMA Airtime) is robust. The shift from a fixed slot efficiency to a rate-dependent $\gamma(R_{\text{PHY}})$ based on CCSDS Proximity-1 framing significantly strengthens the physical layer realism compared to typical abstract network simulations. The use of Gilbert-Elliott (GE) models to stress-test ARQ strategies is appropriate.
*Critique:* The reliance on "internal tools" for validation (Tier 1/2) without external hardware-in-the-loop or high-fidelity network emulation (e.g., NS-3) is a limitation, though the authors are transparent about this in the "Validation Gap" section.

## 3. Validity & Logic
**Rating: 5 (Excellent)**
The logic is internally consistent. The authors have successfully addressed previous concerns regarding the "campaign duty factor" ($d$). The distinction between continuous-duty bounds ($\eta \approx 46\%$) and realistic episodic workloads ($\eta \approx 5-10\%$) is now mathematically sound and operationally convincing. The derivation of the "rate paradox" (where $\gamma$ decreases as PHY rate increases due to fixed-time overheads) is counter-intuitive but physically correct and well-explained.

## 4. Clarity & Structure
**Rating: 5 (Excellent)**
The manuscript is exceptionally well-structured. The "Rate Ladder" (Table IV) and the "Margin Analysis" (Table VI) provide clear, step-by-step justifications for the design recommendations. The distinction between Model S (simplified) and Model C (CCSDS) is handled with improved clarity, ensuring the reader knows which model drives the conclusions.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**
The authors provide a clear Data Availability statement pointing to a repository. The AI disclosure is specific and appropriate (ideation/editing only, not result generation).

## 6. Scope & Referencing
**Rating: 4 (Good)**
The referencing covers the intersection of swarm robotics, satellite operations (CCSDS), and networking well.
*Critique:* The paper relies heavily on CCSDS Proximity-1. While standard, many commercial mega-constellations use proprietary protocols. A brief discussion on how the $\gamma$ derivation adapts to non-CCSDS proprietary frames (e.g., shorter preambles in custom silicon) would broaden the scope.

## Major Issues

1.  **Lack of Sensitivity Analysis for $T_{\text{acq}}$ in the Recommended Regime**
    *   **Issue:** The recommendation of 35 kbps relies heavily on $\gamma_{35} \approx 0.73$, which assumes $T_{\text{acq}} = 5$ ms. However, in a tumbling scenario (RF backup mode context) or high-Doppler ISL acquisition, acquisition times can vary significantly.
    *   **Why it matters:** If $T_{\text{acq}}$ drifts to 10-15 ms due to poor SNR or Doppler search, the margin at 35 kbps might evaporate, potentially invalidating the primary recommendation.
    *   **Remedy:** Expand the sensitivity analysis (specifically around Eq. 14) to show the "breaking point" of $T_{\text{acq}}$ at 35 kbps. At what acquisition time does the margin drop below 10%?

2.  **Ambiguity in "Suspended" Hierarchy during RF Backup**
    *   **Issue:** Section III.B.2 states that during RF-backup, hierarchical coordination is "suspended" and nodes enter safe-hold. However, the text also discusses a "Thundering Herd" Raft election on UHF.
    *   **Why it matters:** It is contradictory to say coordination is suspended but then analyze a complex consensus election on the backup link. If the hierarchy is suspended, why is an election necessary immediately? Why not wait for optical link restoration?
    *   **Remedy:** Clarify the Concept of Operations (ConOps). Is the UHF election a *recovery* mechanism to restore the S-band control plane, or is it an attempt to continue coordination? If it is just for recovery, the timing constraints are much looser.

3.  **Spatial Reuse ($R=3$) Justification is Weak**
    *   **Issue:** The paper asserts a spatial reuse factor of $R=3$ is sufficient for fleet-wide scaling based on an "order-of-magnitude" estimate.
    *   **Why it matters:** In a dense shell (e.g., 550 km), sidelobe interference is a major limiter. If $R$ needs to be 7 (cellular standard), the available bandwidth per cluster drops by half, potentially rendering the 35 kbps target unachievable within allocated spectrum.
    *   **Remedy:** Either provide a link budget calculation showing that C/I (Carrier-to-Interference) allows $R=3$ with standard patch antennas, or explicitly mark $R=3$ as a "critical assumption requiring antenna pattern verification" in the limitations section.

## Minor Issues

1.  **Table I (Notation):** The definition of $\alpha_{\text{RX}}$ is listed as "derived," but it would be helpful to explicitly state it is the *duty cycle of the coordinator receiver*.
2.  **Section IV.J (Gamma):** The text mentions "proprietary ISL... $\gamma=0.530$". Please clarify the assumptions (overhead bits/timing) that lead to such low efficiency for the proprietary case, as custom protocols are usually *more* efficient than CCSDS, not less.
3.  **Fig. 3 (Buffer CDF):** The caption mentions "Bernoulli $d=0.10$". Clarify if this is memoryless Bernoulli or a Markov process (the text implies Markov/bursty).
4.  **Eq. 11 (Unicast Stagger):** The variable $q$ is introduced as the unicast fraction. Ensure $q$ is defined in the text immediately preceding the equation for flow.
5.  **Typos:** Section V.A, "emergent finding is the ARQxTDMA coupling" — strictly speaking, this is a model interaction, not a physical finding. Consider rephrasing to "emergent system dynamic."

## Overall Recommendation
**Recommendation: Accept with Minor Revisions**

This is a high-quality, rigorous manuscript that provides valuable "rules of thumb" and detailed sizing equations for spacecraft swarm designers. The authors have successfully navigated the complexity of coupling byte-level protocols with physical-layer timing.

The transition from the previous version's static $\gamma$ to the rate-dependent $\gamma(R_{\text{PHY}})$ is a substantial improvement that adds significant realism. The "Two-Test Feasibility" framework is a useful contribution to the systems engineering toolkit.

The requested revisions focus on bounding the risks of the assumptions made regarding acquisition timing and spatial reuse. Once these sensitivity limits are clarified, the paper will be an excellent reference for the community.

## Constructive Suggestions

1.  **Add a "Safety Factor" Variable:** In Algorithm 1, explicitly add a safety factor $S_F$ (e.g., 1.2) to the bandwidth requirement to account for the "unmodeled overheads" listed in Table VI, rather than relying on the residual margin check at the end.
2.  **Visualizing the Rate Paradox:** Figure 4 is good, but a second panel showing "Effective Throughput" vs. "PHY Rate" would visually demonstrate the diminishing returns caused by fixed overheads.
3.  **Operational Context:** In the discussion, briefly mention how this sizing impacts the ground segment. If the swarm handles this coordination autonomously, how much does ground contact time reduce? (Likely significantly, reinforcing the paper's value).