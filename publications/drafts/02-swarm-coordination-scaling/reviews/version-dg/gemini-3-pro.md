---
paper: "02-swarm-coordination-scaling"
version: "dg"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-03-05"
recommendation: "Unknown"
---

Here is a comprehensive peer review of the manuscript **"Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version DG)**, prepared for *IEEE Transactions on Aerospace and Electronic Systems*.

---

## 1. Significance & Novelty
**Rating: 4 (Good)**
The paper addresses a critical gap in the literature: the specific sizing of coordination channels for large-scale ($N=10^5$) autonomous swarms. While mega-constellation routing is well-studied, the specific intersection of hierarchical command-and-control (C2) traffic, byte-level accounting, and TDMA slot timing is novel. The derivation of closed-form sizing equations that link message-layer duty cycles ($d$) to physical-layer slot efficiency ($\gamma$) is a significant contribution for systems engineers. The novelty lies less in the invention of new protocols and more in the rigorous synthesis and parameterization of existing standards (CCSDS) for this specific application.

## 2. Methodological Soundness
**Rating: 5 (Excellent)**
The methodology is rigorous and well-structured. The authors employ a multi-tiered verification approach (analytical equations, DES, and slot-level simulation). The explicit separation of the "byte budget" (Test A) from "TDMA schedulability" (Test B) provides clarity often missing in ad-hoc network simulations. The handling of the Gilbert-Elliott (GE) channel model is particularly strong, correctly identifying the interaction between coherence time and intra-cycle ARQ effectiveness. The move to a standards-based derivation of $\gamma$ (Model C) rather than assuming a fixed efficiency adds significant credibility.

## 3. Validity & Logic
**Rating: 4 (Good)**
The internal logic is consistent. The transition from the infeasible 24 kbps case to the recommended 35 kbps case is supported by the data. The distinction between the stress-case ($d=1$) and realistic operational campaigns ($d=0.10$) is logically sound and prevents over-designing the system.
*Critique:* The paper relies heavily on the assumption that cluster membership is static. While addressed in Section V-C as a limitation, the impact of dynamic re-association in non-coplanar shells (e.g., Walker constellations) on the TDMA schedule stability is a logical weak point that deserves slightly more discussion, even if quantified as low overhead.

## 4. Clarity & Structure
**Rating: 5 (Excellent)**
The manuscript is exceptionally clear. The "Rate Ladder" (Table IV) and the "Two-Test Feasibility" definitions are pedagogical highlights. The notation is consistent, and the distinction between information rate, PHY rate, and effective throughput is handled with precision. Figures are legible and directly support the text. The explicit "Validation Gap" section is refreshing and demonstrates scientific integrity.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**
The authors provide a clear Data Availability statement with a repository link. The Acknowledgment section transparently discloses the use of AI for ideation and editing, adhering to emerging publication standards. There are no apparent conflicts of interest or dual-publication issues.

## 6. Scope & Referencing
**Rating: 4 (Good)**
The scope is well-aligned with TAES. The referencing covers the necessary bases: swarm robotics, delay-tolerant networking (DTN), and CCSDS standards.
*Critique:* The paper could benefit from slightly more engagement with recent literature on "Age of Information" (AoI) in satellite networks specifically, rather than general wireless networks, to strengthen the context for the AoI results.

---

## Major Issues

1.  **Clarification of the "Logical" 1 kbps Budget vs. Physical Link**
    *   **Issue:** The paper defines a 1 kbps per-node budget but recommends a 35 kbps PHY link. While Table II attempts to clarify this, the distinction between the *logical traffic allocation* (used for Test A) and the *physical channel capacity* (used for Test B) can still be confusing. A casual reader might wonder why a 1 kbps stream requires a 35 kbps link.
    *   **Why it matters:** This is the core sizing result. If readers confuse the average per-node throughput with the burst-rate requirement of the coordinator, they will misunderstand the scaling laws.
    *   **Remedy:** In Section IV-A or the introduction, explicitly state: "The 35 kbps requirement arises because the coordinator must ingest traffic from 99 other nodes sequentially within a 10-second window. The 1 kbps figure is the time-averaged allowance per node, whereas 35 kbps is the instantaneous burst rate required at the hub."

2.  **Sensitivity of $\gamma$ to Range/Doppler Variations**
    *   **Issue:** The derivation of $\gamma$ (Model C) assumes a fixed guard time of 4.7 ms. In LEO, differential Doppler between a coordinator and a node at the edge of a 500 km cluster can be significant, potentially affecting acquisition times or requiring larger guards if GNSS sync degrades.
    *   **Why it matters:** If the guard time is underestimated, the slot efficiency drops, and the 35 kbps recommendation might become marginal.
    *   **Remedy:** Add a brief calculation or sensitivity sentence in Section IV-J regarding Doppler shift at S-band for relative velocities in a swarm, confirming that the preamble/guard covers this specific dynamic.

3.  **Raft Election Storms on UHF**
    *   **Issue:** Section III-B-2 mentions a "Thundering Herd" problem where 100 nodes attempt election on the backup UHF channel. The analysis suggests a stable throughput after backoff, but Slotted ALOHA with 100 contenders often faces collapse before stabilization.
    *   **Why it matters:** If the backup channel collapses during a coordinator failure, the swarm loses command authority for longer than the estimated 160s.
    *   **Remedy:** Briefly justify the stability of the backoff parameters ($W_0=4, W_{max}=64$). Are these sufficient for $N=100$? A citation or a quick probability calculation of a successful slot capture in the first 10 rounds would strengthen this claim.

---

## Minor Issues

1.  **Table I (Notation):** The definition of $\alpha_{RX}$ is listed as a "Computed output." It would be helpful to explicitly state that it represents the *fraction of the cycle available for ingress*.
2.  **Section IV-H (Fleet Reuse):** The assumption of Spatial Reuse Factor $R=7$ is stated as a geometric baseline. A brief mention that this assumes isotropic or low-gain antennas would be helpful; directional ISLs might allow $R=3$ or $R=1$.
3.  **Equation 10 (Algorithm 1):** In the algorithm, `margin < 0.10 * Tc` triggers a warning. It might be useful to suggest *what* to do in the warning (e.g., "Recommend increasing PHY rate").
4.  **Typos/Formatting:**
    *   Table III: "Received C/N0" unit is dB-Hz, correct. Just ensure consistency in capitalization of "dB" throughout.
    *   Fig. 3 caption: "squares" are mentioned, ensure they are clearly visible in the final high-res figure.

---

## Overall Recommendation
**Recommendation: Accept with Minor Revisions**

This is a high-quality, rigorous manuscript that makes a valuable contribution to the field of spacecraft swarm operations. The authors have successfully translated abstract networking concepts into concrete engineering design equations relevant to aerospace practitioners.

The paper excels in its methodological transparency—specifically the "Two-Test" framework and the honest assessment of validation gaps. The transition from the "Model S" (simplified) to "Model C" (CCSDS-based) slot timing is a critical improvement that grounds the work in reality. The handling of the Campaign Duty Factor ($d$) resolves previous concerns about unrealistic continuous-duty workload assumptions.

The requested revisions are primarily clarifications to ensure the core distinction between logical bandwidth and physical burst rate is unambiguous, and to shore up the justification for the backup channel's stability. Once addressed, this paper will serve as a standard reference for sizing swarm coordination channels.

---

## Constructive Suggestions

1.  **Enhance the "Rate Ladder" (Table IV):** Consider adding a column for "Limiting Factor" (e.g., "Ingress Time," "ARQ Margin"). This would allow a systems engineer to instantly see *why* 24 kbps fails (Ingress Time) vs. why 30 kbps is marginal (ARQ Margin).
2.  **Visualizing the Duty Factor:** A small subplot in Figure 4 or a new schematic showing the timeline of a "Campaign" (Active vs. Routine) would help visualize the parameter $d$.
3.  **Algorithm 1 Refinement:** In the `Test B (ARQ)` section of the algorithm, explicitly add a check for the coherence regime. If $\tau_c < T_c$, the algorithm should permit intra-cycle ARQ; if $\tau_c \ge T_c$, it should force inter-cycle recovery. This aligns the algorithm with the text in Section IV-C.