---
paper: "02-swarm-coordination-scaling"
version: "cr"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-03-04"
recommendation: "Unknown"
---

Here is a comprehensive peer review of the manuscript "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version CR).

---

## 1. Significance & Novelty
**Rating: 4 (Good)**
The paper addresses a critical gap in the literature: the specific scaling properties of coordination architectures for "mega-constellations" ($10^3$--$10^5$ nodes). While high-level networking and routing for such systems are well-studied (e.g., Starlink routing), the specific intersection of *command-and-control* traffic sizing, hierarchical aggregation, and physical-layer TDMA constraints is under-explored. The derivation of closed-form sizing equations that link byte-level budgets to slot-level timing is a significant contribution for systems engineers. The novelty lies in the integrated "two-layer" feasibility framework rather than in new fundamental theoretical discoveries.

## 2. Methodological Soundness
**Rating: 4 (Good)**
The methodology is generally robust. The authors employ a multi-tiered approach: analytical derivation, cycle-aggregated Discrete Event Simulation (DES), and a slot-level TDMA simulator. The cross-verification between these tools (Tier 1 and Tier 2 V&V) is well-documented. The use of the Gilbert-Elliott (GE) model for correlated link losses is appropriate for this domain, and the sensitivity sweep (Fig. 4b) adds significant value by decoupling the results from specific channel assumptions. The explicit derivation of $\gamma$ (slot efficiency) from CCSDS standards is a strong methodological improvement over previous versions.

## 3. Validity & Logic
**Rating: 4 (Good)**
The internal logic is consistent. The distinction between the logical byte budget (1 kbps) and the physical link rate (30-35 kbps) is clearly maintained. The argument for the 35 kbps recommendation is logically sound, based on the interaction between GE-correlated losses and the TDMA superframe margin. The identification of the "ARQ coupling" effect at lower data rates (where retransmissions cause deadline misses) is a valid and critical insight. The limitations regarding the lack of external validation are honestly stated.

## 4. Clarity & Structure
**Rating: 5 (Excellent)**
The manuscript is exceptionally well-structured. The "Rate Ladder" (Table 4) and the "Feasibility Test" (Algorithm 1) provide clear, actionable summaries of complex interdependencies. The notation is consistent, and the distinction between Model C (design basis) and Model S (comparison bound) is handled carefully to avoid confusion. Figures are legible and directly support the text.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**
The authors provide a clear Data Availability statement with a GitHub link. The acknowledgment section transparently discloses the use of AI for ideation and editing, adhering to modern ethical guidelines. There are no apparent conflicts of interest or human subject concerns.

## 6. Scope & Referencing
**Rating: 4 (Good)**
The scope is well-defined for *IEEE TAES*. The referencing covers standard astrodynamics texts, CCSDS standards, and relevant distributed systems literature. The inclusion of recent mega-constellation filings (SpaceX, Kuiper) anchors the work in current industrial reality. The paper could benefit from slightly more engagement with recent literature on "Age of Information" in satellite networks specifically, rather than general wireless networks, but the current coverage is adequate.

## 7. Theoretical Depth
**Rating: 3 (Adequate)**
The theoretical component is practical rather than abstract. The queueing theory applied (M/D/1, MMPP/D/1) is standard. The value here is in the *application* of these theories to a specific constraint satisfaction problem (spacecraft coordination) rather than advancing queueing theory itself. This is appropriate for a systems engineering paper.

## 8. Simulation Rigor
**Rating: 4 (Good)**
The simulation campaign is rigorous. The use of 30 Monte Carlo replications with bootstrap confidence intervals is standard practice. The separation of the DES (for campaign dynamics) and the slot-simulator (for timing constraints) is a smart architectural choice that allows for efficient simulation of large $N$. The lack of NS-3 simulation for MAC contention is a noted limitation, but acceptable given the focus on TDMA schedulability.

## 9. Practical Utility
**Rating: 5 (Excellent)**
This is the paper's strongest point. The "Design Equations" and "Feasibility Test" algorithm are directly usable by satellite constellation architects. The sensitivity analyses (gamma vs. rate, recovery vs. burstiness) allow practitioners to adapt the findings to their specific hardware and orbits.

## 10. Overall Quality
**Rating: 4 (Good)**
A high-quality, polished manuscript that solves a specific, relevant engineering problem with rigor and clarity.

---

## Major Issues

1.  **Justification of Spatial Reuse ($R=3$):**
    *   **Issue:** The paper asserts that a spatial reuse factor of $R=3$ is sufficient based on a "magnitude plausibility argument" regarding free-space path loss.
    *   **Why it matters:** In dense swarms or constellations, co-channel interference is a primary capacity limiter. If $R=3$ is optimistic (e.g., due to sidelobes or specific orbital geometries), the fleet-wide capacity claims (Eq. 5) may be invalid.
    *   **Remedy:** While full RF simulation is out of scope, the authors should provide a slightly more rigorous geometric justification. For example, cite specific antenna beamwidth assumptions (e.g., patch antennas vs. dipoles) that support the $>$20 dB isolation claim at $10\times$ cluster diameter. A brief calculation of the interference-to-noise ratio (INR) from a worst-case nearest-neighbor cluster would strengthen this claim.

2.  **Unicast Stagger Latency Context:**
    *   **Issue:** The paper notes a 19-cycle (190s) stagger for unicast commands (Eq. 7) but dismisses it as acceptable for "orbit-raising."
    *   **Why it matters:** For large swarms, 190s is a significant latency if the swarm must react to a dynamic environment (e.g., solar weather, debris field entry) in a coordinated but heterogeneous manner.
    *   **Remedy:** Explicitly discuss the operational constraints this imposes. Does this latency prohibit certain types of formation flying control loops? A sentence clarifying that "tight formation control" is assumed to happen via the optical ISL, and this RF link is strictly for high-level orchestration, would resolve the ambiguity.

## Minor Issues

1.  **Table 1 (Notation):** The definition of $\alpha_{RX}$ is listed as "Ingress fraction... derived from schedule." It would be helpful to explicitly state in the table that this includes retransmission slots, as this is a key driver of the 35 kbps recommendation.
2.  **Section IV-J (Gamma Derivation):** The text mentions "DVB-RCS2 terminals achieve measured slot efficiencies of 0.70--0.85." It would be beneficial to briefly explain *why* DVB-RCS2 is a valid proxy for ISL links (e.g., similar framing overhead ratios), as they are different physical standards.
3.  **Fig. 3 (Buffer CDF):** The caption mentions "Bernoulli d=0.10" and "ON/OFF d=0.10". The visual distinction between the solid and dash-dot lines is somewhat subtle. Ensure the final figure has high contrast or distinct line markers.
4.  **Eq. 10 (Gamma):** The term $T_{framing}$ is defined in the text below the equation but uses $O_{frame}$ in the numerator. Ensure consistency in variable names between Table 1 and Eq. 10.

## Overall Recommendation
**Recommendation: Accept with Minor Revisions**

This is a strong, well-reasoned paper that makes a concrete contribution to the systems engineering of large space swarms. The authors have successfully navigated the complexity of cross-layer design (byte budgets vs. TDMA timing) and provided a rigorous framework for sizing these systems.

The manuscript has significantly matured from potential earlier iterations. The distinction between Model C (design) and Model S (bound) is handled with excellent discipline, preventing the "optimism bias" often seen in theoretical papers. The validation of the 35 kbps recommendation via the "ARQ coupling" phenomenon in the slot-level simulator is a compelling result.

The requested revisions are primarily to bolster the justification for the spatial reuse factor and to clarify operational constraints regarding latency. Once addressed, this paper will serve as a valuable reference for constellation architects.

## Constructive Suggestions

1.  **Enhance the "Validation Roadmap":** In Section V-B, consider adding a specific call for "Hardware-in-the-Loop" (HITL) testing of the acquisition times. The sensitivity analysis shows $T_{acq}$ is a major driver of $\gamma$. Emphasizing that radio vendors need to characterize this parameter under Doppler stress would be a valuable message to the industry.
2.  **Expand on "Safe Mode" Implications:** The paper notes that hierarchical coordination is suspended during RF-backup (UHF). It would be valuable to add a sentence in Section III-B-2 discussing how the swarm *recovers* from this state. Does the coordinator have to re-ingest the state of all 100 nodes via UHF beacons before resuming TDMA? This affects the "Time to Recovery" metric.
3.  **Clarify "Information Rate":** In Table 4 (Rate Ladder), Step 1 is "Info-rate req. 20.2 kbps." It might be helpful to add a parenthetical note "(Application Layer)" to distinguish it further from the PHY rates, for readers scanning the table.