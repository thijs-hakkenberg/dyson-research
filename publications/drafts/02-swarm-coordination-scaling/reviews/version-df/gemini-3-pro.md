---
paper: "02-swarm-coordination-scaling"
version: "df"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-03-05"
recommendation: "Unknown"
---

Here is a comprehensive peer review of the manuscript "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version DF).

---

## 1. Significance & Novelty
**Rating: 5 (Excellent)**
The paper addresses a critical gap in the literature: the lack of closed-form sizing relationships for coordinating mega-constellations ($10^4$--$10^5$ nodes). While much prior work focuses on routing (ISL) or small-scale formation flying, this work rigorously tackles the "mid-tier" coordination problem—specifically the bandwidth and latency costs of hierarchical command and control. The derivation of the "Two-Test" feasibility framework (byte budget vs. TDMA airtime) is a significant contribution that provides a practical tool for system architects. The shift from abstract graph theory to concrete link-layer sizing (accounting for preambles, guard times, and FEC) adds substantial engineering value.

## 2. Methodological Soundness
**Rating: 4 (Good)**
The methodology is generally robust, combining analytical derivation with Discrete Event Simulation (DES) and a slot-level TDMA simulator. The explicit handling of the "Two-Test" framework is a major improvement over previous versions.
*   **Strengths:** The differentiation between "Model C" (CCSDS-based) and "Model S" (simplified) is crucial and well-executed. The use of the Gilbert-Elliott (GE) model to stress-test ARQ strategies is sound.
*   **Weakness:** The reliance on a "standards-based parameter estimate" for $\gamma$ rather than hardware-in-the-loop validation is a limitation, though the authors transparently acknowledge this as a "Tier 2" result. The assumption of centralized command generation simplifies the topology significantly; while justified for this specific architecture, it limits the applicability for fully decentralized swarms.

## 3. Validity & Logic
**Rating: 5 (Excellent)**
The internal logic is tight. The paper successfully closes the loop between the byte-level budget (Test A) and the physical layer constraints (Test B).
*   **Gamma Unification:** The paper successfully resolves previous inconsistencies regarding slot efficiency. The derivation of $\gamma \approx 0.76$ (down from the optimistic 0.95 in Model S) is logically sound and mathematically consistent with CCSDS Proximity-1 framing.
*   **Stress Case Context:** The clarification that the 46% overhead is a continuous-duty bound (occurring <1% of the time) effectively addresses concerns about "alarmist" overhead figures. The distinction between logical traffic allocation (1 kbps) and physical link rate (35 kbps) is clear.

## 4. Clarity & Structure
**Rating: 5 (Excellent)**
The manuscript is exceptionally well-structured. The "Rate Ladder" (Table III) and the "Feasibility Test" algorithm (Algorithm 1) are standout features that make the complex interdependencies accessible. The distinction between "Information Rate," "PHY Rate," and "Effective Throughput" is handled with precision. The notation table is comprehensive.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**
The authors provide a clear Data Availability statement with a GitHub link (including specific tags). The acknowledgment of AI usage for ideation (but not data generation) is transparent and aligns with emerging publication standards.

## 6. Scope & Referencing
**Rating: 4 (Good)**
The literature review covers the necessary bases (swarm robotics, constellation management, delay-tolerant networking). The inclusion of CCSDS standards (Proximity-1, LDPC) grounds the work in reality.
*   **Gap:** While the paper mentions spatial reuse ($R=7$), the justification relies on simple geometric arguments. A stronger connection to interference modeling literature (e.g., stochastic geometry for satellite networks) would strengthen the fleet-level claims, though this is arguably outside the scope of a cluster-level sizing paper.

## 7. Major Issues

1.  **Sensitivity of ARQ to the Coherence Time Assumption ($\tau_c$)**
    *   **Issue:** The paper concludes that intra-cycle ARQ is "structurally ineffective" because the GE model assumes state transitions occur only once per cycle ($T_c$). This implies $\tau_c \approx T_c$ (10s). However, for a tumbling spacecraft or one experiencing multipath, $\tau_c$ could be milliseconds. If $\tau_c \ll T_c$, intra-cycle ARQ becomes highly effective.
    *   **Impact:** This assumption drives the recommendation for inter-cycle recovery (P95 = 4 cycles), which significantly increases latency. If the channel is fast-fading, the system is being over-designed for latency.
    *   **Remedy:** In Section IV-C or Discussion, explicitly analyze the "Fast Fading" case where the GE state is redrawn *per slot* rather than per cycle. Acknowledge that the "ineffective ARQ" conclusion is valid *only* for slow-fading/shadowing regimes.

2.  **Lack of Sensitivity Analysis for Cluster Size ($k_c$) on $\gamma$**
    *   **Issue:** The derivation of $\gamma$ assumes $k_c=100$. However, as $k_c$ changes, the ratio of guard times to payload times might shift if the cluster geometry changes (affecting propagation delay) or if the total cycle time $T_c$ is held constant (squeezing slot times).
    *   **Impact:** The claim that $\gamma$ is purely rate-dependent might break down at extreme $k_c$ values (e.g., $k_c=500$ with fixed $T_c=10s$ leaves very little time per slot, potentially making acquisition overhead dominant).
    *   **Remedy:** Add a brief check or comment in Section V-C on how $\gamma$ behaves if $k_c$ scales up to 500 while keeping $T_c$ constant. Does the acquisition time eventually eat the entire budget?

3.  **Fleet-Level Interference Justification**
    *   **Issue:** The recommendation for Spatial Reuse Factor $R=7$ is based on a simple "6 first-tier interferers" calculation. In 3D orbital geometries (Walker constellations), interference patterns are dynamic and complex, often involving sidelobes from non-adjacent planes.
    *   **Impact:** If $R=7$ is insufficient, the fleet capacity calculation ($G=1$) collapses, and the system becomes interference-limited rather than bandwidth-limited.
    *   **Remedy:** Qualify the $R=7$ recommendation as a "geometric baseline" and explicitly state that high-fidelity orbital RF simulation (e.g., Systems Tool Kit or NS-3) is required to validate the C/I environment for specific constellation shells.

## 8. Minor Issues

1.  **Table I (Notation):** The definition of $\alpha_{RX}$ is listed as a "Computed output." It would be helpful to explicitly state that it represents the *duty cycle* of the receiver in the superframe.
2.  **Section III-B-2 (Thundering Herd):** The footnote calculation for the thundering herd effect is useful but dense. Consider moving the key result (140-160s recovery) into the main text for better flow.
3.  **Fig. 3 (Buffer CDF):** The "Continuous d=1.0" line is labeled "dashed" in the caption but looks similar to the "dash-dot" line in some renderings. Ensure distinct line styles.
4.  **Equation 5 (Consensus):** The variable $S_{raft}$ is defined in the text below the equation. Please add it to Table I for consistency.
5.  **Section IV-A (Oscillator Drift):** The calculation assumes a 600s resync interval. Please clarify if this is a hard parameter or derived from the GNSS denial scenario.

## 9. Overall Recommendation
**Recommendation: Accept with Minor Revisions**

This is a high-quality manuscript that offers a rigorous, mathematically grounded framework for sizing communication in large space swarms. The authors have successfully addressed the complexity of mapping high-level coordination requirements to physical layer constraints. The "Two-Test" framework and the $\gamma$ parameterization are valuable contributions to the field. The revisions requested (primarily regarding the coherence time assumption and interference justification) are necessary to bound the validity of the results but do not require new simulations or fundamental changes to the model.

## 10. Constructive Suggestions

1.  **Refine the ARQ Conclusion:** Instead of stating ARQ is "ineffective" under GE, frame it as "ineffective under slow-fading conditions (shadowing/occultation)." This nuances the design recommendation: use ARQ for multipath/pointing jitter, use inter-cycle recovery for shadowing.
2.  **Expand Algorithm 1:** Consider adding a "Step 0" to Algorithm 1 that estimates the required $R_{PHY}$ based on the heuristic equation, giving the user a starting point for the iteration.
3.  **Visualizing the Design Space:** A "heatmap" figure plotting Feasibility (Boolean) on axes of $k_c$ vs. $R_{PHY}$ would be a powerful visual addition to Section IV, showing the "cliff" where the protocol breaks down.
4.  **Hardware Context:** In the discussion of $\gamma$, briefly mentioning specific radio chipsets (e.g., S-band transceivers common in CubeSats) that support the assumed acquisition times (5ms) would ground the "Tier 2" assumptions in current hardware capabilities.