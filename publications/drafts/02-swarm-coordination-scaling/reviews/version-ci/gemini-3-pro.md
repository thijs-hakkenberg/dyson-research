---
paper: "02-swarm-coordination-scaling"
version: "ci"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-03-01"
recommendation: "Accept with Minor Revisions"
---

Here is a rigorous peer review of the manuscript "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version CI), tailored for *IEEE Transactions on Aerospace and Electronic Systems*.

---

## 1. Significance & Novelty
**Rating: 5 (Excellent)**
The paper addresses a critical gap in the literature: the lack of closed-form sizing relationships for coordinating mega-constellations ($10^4$--$10^5$ nodes) under strict bandwidth constraints. While swarm robotics and networking literature exist separately, this work uniquely bridges them by deriving a "physics-of-coordination" framework. The distinction between message-layer feasibility (byte budget) and physical-layer schedulability (TDMA airtime) is a significant conceptual contribution that moves beyond the abstract graph-theory models often seen in this domain.

## 2. Methodological Soundness
**Rating: 5 (Excellent)**
The multi-tiered validation approach is robust. The authors successfully employ a cycle-aggregated DES for distributional analysis, a slot-level simulator for TDMA timing verification, and a packet-level derivation for the slot efficiency parameter ($\gamma$). The explicit derivation of $\gamma_{C,24} = 0.760$ from CCSDS Proximity-1 standards is a substantial improvement over previous versions that relied on assumed efficiencies. The Gilbert-Elliott (GE) model application to characterize correlated loss recovery is mathematically sound, and the sensitivity sweep (Fig. 10b) provides valuable design tools for practitioners.

## 3. Validity & Logic
**Rating: 4 (Good)**
The internal logic is consistent. The derivation of the coordinator ingress bottleneck and the subsequent sizing equations are algebraically correct. The argument for the 35 kbps design point is well-supported by the margin analysis.
*Critique:* The assumption that cluster membership is static is a limitation, though the authors attempt to bound the re-association overhead. The logic regarding "thundering herd" contention during coordinator failure relies on Slotted ALOHA stability assumptions that may be optimistic if the control channel is shared across multiple clusters (though fleet reuse is discussed).

## 4. Clarity & Structure
**Rating: 5 (Excellent)**
The manuscript is exceptionally well-structured. The progression from research questions to analytical models, then to simulation results, and finally to standards-grounded derivation is logical. The distinction between Model S (simplified) and Model C (CCSDS) is handled with great clarity, preventing confusion about which assumptions apply where. Tables are dense but informative, particularly Table VIII (Superframe Time Budget).

## 5. Ethical Compliance
**Rating: 5 (Excellent)**
The authors provide a clear Data Availability statement with a GitHub link (anonymized for review, presumably). The acknowledgment section transparently discloses the use of AI for ideation and editing, adhering to emerging best practices in scientific publishing.

## 6. Scope & Referencing
**Rating: 4 (Good)**
The literature review covers relevant ground in swarm robotics, constellation management, and delay-tolerant networking.
*Critique:* The paper would benefit from tighter integration with recent work on "mega-constellation" routing (e.g., recent papers on Starlink topology dynamics) to better contextualize the static-cluster assumption. The referencing of CCSDS standards is exemplary.

## 7. Data Analysis
**Rating: 5 (Excellent)**
The statistical treatment of the Monte Carlo data is rigorous (30 replications, bootstrap CIs). The analysis of tail behavior (P99 AoI, P95 recovery) is exactly what is needed for high-reliability aerospace systems. The "campaign duty factor" ($d$) analysis effectively addresses workload realism.

## 8. Theoretical Depth
**Rating: 4 (Good)**
The queueing theoretic models ($D/D/1$ batch, $M/D/c$) are appropriate approximations. The derivation of the unicast stagger cycles ($L_{cmd}$) is a nice theoretical addition that quantifies the cost of addressing individual nodes.
*Critique:* The theoretical treatment of the "thundering herd" problem is less developed than the steady-state analysis.

## 9. Practical Relevance
**Rating: 5 (Excellent)**
This is the paper's strongest asset. It provides actionable design equations (Algorithm 1) that engineers can immediately use. The focus on the RF-backup channel (1 kbps) as the design driver demonstrates deep operational insight—most academic papers ignore safe-mode constraints.

## 10. Figures & Tables
**Rating: 5 (Excellent)**
Figures are high-quality and information-dense. Figure 10 (GE recovery) and Figure 12 (Coordinator buffer CDF) are particularly illuminating. Table XIII (Claim Map) is a helpful guide for the reviewer and reader.

---

## Major Issues

1.  **Contextualization of the Stress-Case ($\eta_S \approx 46\%$):**
    *   **Issue:** While the paper now introduces the campaign duty factor ($d$), the abstract and conclusion still heavily feature the 46% stress-case figure without immediately qualifying it as a rare bound.
    *   **Why it matters:** A casual reader might conclude the protocol is inefficient (consuming half the bandwidth) during normal operations, whereas the routine overhead is only 5-10%.
    *   **Remedy:** In the Abstract and Conclusion, explicitly pair the 46% figure with the "routine" figure (5-10%) in the same sentence to prevent misinterpretation. (e.g., "Routine overhead is ~5%, rising to a bounded 46% during intensive reconfiguration").

2.  **Thundering Herd & ALOHA Stability:**
    *   **Issue:** Section III-B-2 mentions that if >200 nodes share a channel, ALOHA saturation occurs. However, the paper does not explicitly model the *transition* from saturation back to stability.
    *   **Why it matters:** If the control channel collapses during a coordinator failure (when it is needed most), the recovery time could be infinite (deadlock), not just delayed.
    *   **Remedy:** Add a brief discussion or a reference to a back-off strategy (e.g., exponential back-off) that ensures the system exits the saturation regime. A simple acknowledgement that a static probability ALOHA is insufficient for $N>200$ without back-off would suffice.

3.  **Unicast Stagger vs. Operational Reality:**
    *   **Issue:** The derivation of $L_{cmd} = 31$ cycles (310 seconds) for unicast commands is mathematically correct but operationally concerning.
    *   **Why it matters:** A 5-minute command latency for individual nodes might be unacceptable for certain fault recovery scenarios.
    *   **Remedy:** Explicitly discuss *which* types of commands require unicast vs. broadcast. If most critical commands (e.g., "Safe Mode Now") are broadcast, the 310s latency is a non-issue. Clarify that safety-critical commands are almost always Type 1 (broadcast).

## Minor Issues

1.  **Table I (Key Notation):** The definition of $\alpha_{RX}$ is specific to the $k_c=100$ case. Please clarify in the table caption that this is a *representative* value, or provide the formula in the table.
2.  **Section IV-C (GE Model):** The justification for $\tau_c \ge T_c$ based on tumble rates is good, but please clarify if this assumes the antenna is on the body or a deployed panel.
3.  **Algorithm 1:** In line 7, the check $\eta_{total}/\gamma < 0.50$ is called a "Screening indicator." Please clarify if this threshold is empirical or derived from a specific utilization bound.
4.  **Typos:** Check the capitalization of "Gilbert-Elliott" throughout; it appears consistent but worth a final proof.

---

## Overall Recommendation
**Recommendation: Accept with Minor Revisions**

**Summary:**
This is an exceptional manuscript that makes a substantial contribution to the field of spacecraft swarm coordination. The authors have successfully moved beyond abstract networking models to provide a "physics-based" sizing framework grounded in CCSDS standards and realistic link budgets. The distinction between message-layer feasibility and TDMA schedulability is a key theoretical insight, and the rigorous characterization of the "RF-backup" regime ensures the results are operationally relevant.

The previous concerns regarding the validation of the slot efficiency parameter ($\gamma$) have been comprehensively addressed via the packet-level derivation in Section IV-J. The introduction of the campaign duty factor ($d$) successfully contextualizes the high-overhead stress cases.

The requested revisions are primarily regarding presentation and framing to ensure the efficiency of the protocol under routine conditions is not overshadowed by the worst-case bounds, and to ensure the stability of the contention channel is addressed.

## Constructive Suggestions

1.  **Refine Abstract Metrics:** Modify the abstract to explicitly state: "Routine operations yield $\eta \approx 5\%$; stress-case reconfiguration is bounded at 46%." This highlights the efficiency of the steady state.
2.  **Expand on Back-off:** In the "Thundering Herd" section, briefly mention that an exponential back-off or randomized access window is required to resolve the contention if the cluster size exceeds the ALOHA stability limit.
3.  **Operational ConOps for Unicast:** In the discussion of the 31-cycle stagger, add a sentence confirming that "time-critical safety commands are architecturally restricted to Broadcast (Type 1) to avoid this latency."
4.  **Future Work - Doppler:** Briefly mention that for LEO-to-LEO links at 2.2 GHz, Doppler compensation is assumed to be handled by the transceiver (standard for Proximity-1 radios), justifying its exclusion from the $\gamma$ calculation.