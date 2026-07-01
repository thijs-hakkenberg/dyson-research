---
paper: "02-swarm-coordination-scaling"
version: "cy"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-03-05"
recommendation: "Unknown"
---

Here is a comprehensive peer review of the manuscript **"Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version CY)**.

---

# Peer Review Report

**Journal:** IEEE Transactions on Aerospace and Electronic Systems
**Manuscript ID:** [Assigned by Editor]
**Version:** CY
**Reviewer Expertise:** Distributed Systems, Spacecraft Autonomy, TDMA/MAC Scheduling, Swarm Coordination

## 1. Significance & Novelty
**Rating: 4 (Good)**
The paper addresses a critical gap in the literature regarding the scalability of autonomous coordination for "mega-constellations" ($10^4$--$10^5$ nodes). While high-level architectural concepts for swarms exist, this work provides specific, closed-form sizing equations that link byte-level protocol overhead to physical-layer (PHY) constraints. The derivation of a "two-layer feasibility framework" (byte budget + TDMA airtime) is a valuable contribution for systems engineers. The novelty lies not in new fundamental networking theory, but in the rigorous application and parameterization of these theories for the specific constraints of S-band inter-satellite links (ISL) in large clusters.

## 2. Methodological Soundness
**Rating: 5 (Excellent)**
The methodology is rigorous and well-anchored. The authors have significantly improved the fidelity of the slot-timing models compared to previous iterations. The distinction between Model S (simplified) and Model C (CCSDS-grounded) is crucial and handled with excellent transparency. The use of a Gilbert-Elliott (GE) model to stress-test the TDMA schedule against correlated losses is appropriate. The derivation of $\gamma$ (slot efficiency) from standard CCSDS Proximity-1 framing adds necessary realism. The simulation framework (Tier 1 verification) appears robust for the scope of the claims.

## 3. Validity & Logic
**Rating: 4 (Good)**
The internal logic is consistent. The transition from identifying a bottleneck (coordinator ingress) to proposing a solution (35 kbps PHY rate) is supported by the data. The handling of the "stress case" ($d=1$) vs. realistic campaign duty factors ($d=0.10$) is logical and prevents over-designing the system for rare events.
*Critique:* The argument regarding "fleet-level reuse" ($R=3$) relies on an order-of-magnitude estimate that is not validated by antenna pattern simulation. While the authors acknowledge this limitation, the validity of the fleet-wide scaling claims is weaker than the per-cluster claims.

## 4. Clarity & Structure
**Rating: 5 (Excellent)**
The manuscript is exceptionally well-structured. The "Rate Ladder" (Table IV) and the "Feasibility Test" (Algorithm 1) are standout features that make the results immediately actionable for practitioners. The distinction between "Information Rate," "PHY Rate," and "Effective Throughput" is handled with precision, avoiding common confusion in this domain. Figures are clear, and the notation table is comprehensive.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**
The authors provide a clear Data Availability statement pointing to a repository with code and datasets. The AI disclosure is transparent and specific (ideation/editing only, not result generation). There are no apparent conflicts of interest or plagiarism concerns.

## 6. Scope & Referencing
**Rating: 4 (Good)**
The scope is well-suited for TAES. The literature review covers both classical networking (Kleinrock, Bertsekas) and modern space systems (Starlink, CCSDS standards).
*Critique:* The paper would benefit from slightly more engagement with recent literature on "Age of Information" (AoI) in satellite networks specifically, rather than just general wireless networks, to strengthen the context of Section IV-B.

---

## Major Issues

1.  **Validation of Fleet-Level Spatial Reuse ($R=3$)**
    *   **Issue:** In Section IV-A-1 and Section V-C, the paper claims that spatial reuse $R=3$ allows for fleet-wide scaling. This is based on a high-level assumption of >20 dB isolation at 500 km.
    *   **Why it matters:** If $R=3$ is optimistic and realistic antenna sidelobes require $R=7$ (standard cellular reuse), the effective cycle time $T_c^{\text{fleet}}$ doubles, potentially violating mission latency requirements.
    *   **Remedy:** The authors should either (a) provide a link budget calculation using a standard patch antenna pattern to justify the 20 dB isolation claim, or (b) explicitly calculate the impact of $R=7$ on the total cycle time and add this as a sensitivity case in the discussion.

2.  **Sensitivity of $\gamma$ to Doppler-Induced Guard Times**
    *   **Issue:** The derivation of $\gamma$ (Table VIII) assumes a fixed guard time of 4.7 ms. While this covers propagation and turnaround, it is unclear if it adequately accounts for the worst-case Doppler shift at S-band (approx. $\pm 50$ kHz) for cross-plane links in LEO.
    *   **Why it matters:** If the guard time needs to be significantly larger to handle Doppler compensation (depending on the modem implementation), $\gamma$ decreases, potentially pushing the 35 kbps recommendation to failure.
    *   **Remedy:** Add a specific calculation or statement regarding the Doppler budget within the 4.7 ms guard time. If the modem requires preamble extension for Doppler acquisition, this should be reflected in the $T_{\text{acq}}$ or $T_{\text{guard}}$ parameter.

3.  **Clarification of "Suspension" vs. "Failure" in RF-Backup**
    *   **Issue:** Section III-B-2 mentions that hierarchical coordination is "suspended" during RF-backup. However, the text also discusses a Raft election on UHF. It is slightly contradictory to say coordination is suspended but an election (a coordination task) is occurring.
    *   **Why it matters:** It confuses the operational concept. Is the UHF link used for *control* or just *survival*?
    *   **Remedy:** Clarify that the Raft election on UHF is a *recovery transient* to re-establish the S-band control plane, not a steady-state coordination mode. Explicitly state that the 1 kbps budget does not apply to the UHF backup link.

## Minor Issues

1.  **Table I (Notation):** The definition of $\alpha_{\text{RX}}$ is listed as "Ingress fraction... derived." It would be helpful to explicitly state that this includes the guard times between slots, as this is a common source of error in TDMA calculations.
2.  **Section IV-C (GE Model):** The text states "intra-cycle ARQ is structurally ineffective... when $\tau_c \geq T_c$." Please clarify if this conclusion holds for *all* $M_r$ or if a massive increase in $M_r$ (e.g., $M_r=10$) would help. (Presumably not, due to the state persistence, but worth a sentence).
3.  **Figure 4 (Buffer CDF):** The caption mentions "Bernoulli $d=0.10$." Please clarify if this is a Bernoulli process per cycle or per message.
4.  **Typos:**
    *   Section IV-A: "margin = -1,300 ms" (ensure the negative sign is clearly visible/not a dash).
    *   References: Ensure all "ArXiv" preprints are updated to peer-reviewed versions if available (e.g., Starlink/Kuiper references).

---

## Overall Recommendation
**Recommendation: Accept with Minor Revisions**

This manuscript represents a high-quality, rigorous engineering analysis of the communication bottlenecks in large-scale space swarms. The authors have successfully translated abstract networking concepts into concrete design equations and actionable recommendations (specifically the 35 kbps PHY requirement and the $\gamma$ parameterization).

The "Two-Test Feasibility Framework" is a robust contribution that will aid future system designers. The paper has moved beyond simple simulations to provide a "what-if design tool" via the Gilbert-Elliott analysis.

The requested revisions focus on bounding the assumptions regarding fleet-wide reuse and clarifying the operational concept during backup modes. These are necessary to ensure the paper's claims are fully robust, but they do not require new simulations or fundamental changes to the methodology.

## Constructive Suggestions

1.  **Strengthen the $R=3$ Justification:** Even a back-of-the-envelope calculation showing the path loss difference between the target cluster (500 km) and the nearest interfering cluster (at distance $D$) given a standard gain roll-off would significantly strengthen the fleet-level claims.
2.  **Expand on Acquisition Timing:** In Table VIII, the 5.0 ms acquisition time is a dominant factor. A brief note on how this scales with SNR (or if it is a fixed modem sync time) would be valuable for practitioners using different radios.
3.  **AoI Context:** Briefly contrast the 441s AoI result with the requirements for specific swarm behaviors (e.g., "This is sufficient for orbit maintenance but insufficient for collision avoidance, necessitating the optical ISL for the latter"). This contextualizes the numbers for the reader.