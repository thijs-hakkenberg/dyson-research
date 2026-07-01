---
paper: "02-swarm-coordination-scaling"
version: "s"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-24"
recommendation: "Minor Revision"
---

# Peer Review Report

**Journal:** IEEE Transactions on Aerospace and Electronic Systems
**Manuscript ID:** [Version S]
**Title:** Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study

---

## Review Criteria

### 1. Significance & Novelty
**Rating: 4**

The manuscript addresses a critical and timely gap in the aerospace literature: the specific engineering parameters required to coordinate mega-constellations ($10^4$--$10^5$ nodes) without reliance on ground-in-the-loop control. While hierarchical control theory is well-established, the novelty here lies in the **quantitative characterization** of the protocol overhead ($\eta \approx 21\%$) and the specific dimensioning of coordinator links (50 kbps vs. 24 kbps) using a simulation that bridges the gap between abstract graph theory and packet-level networking.

The introduction of the "Sectorized Mesh" as an intermediate comparator is a significant improvement over binary comparisons between Centralized and Global Mesh architectures often seen in literature. The Age-of-Information (AoI) analysis provides a necessary counter-weight to bandwidth optimization, highlighting the operational risks of exception-based telemetry. This work will likely serve as a reference benchmark for future constellation network architecture studies.

### 2. Methodological Soundness
**Rating: 4**

The methodology is generally robust. The authors employ a cycle-aggregated Discrete Event Simulation (DES) which is an appropriate choice for simulating $10^5$ nodes where packet-level simulation would be computationally prohibitive. The validation of the DES against analytical closed-form solutions (Section IV-E) builds confidence in the implementation.

However, a specific methodological caveat requires attention: the "cycle-aggregated" nature of the simulation abstracts away MAC-layer contention within the cycle. While the authors address this via the $\gamma$ parameter and the coordinator bandwidth stress test, the main overhead results are effectively "application-layer" results. The paper is transparent about this (Table III is excellent), but the distinction between the *logical* 1 kbps budget and the *physical* link rate needs to be reinforced to ensure readers do not misinterpret the latency results.

### 3. Validity & Logic
**Rating: 5**

The conclusions are logically derived from the data. The authors are commendably careful in their claims, explicitly noting that the centralized baseline is a "worst-case bound" and not a representation of a modern parallelized ground segment. This nuance is often missing in papers advocating for distributed systems.

The logic regarding the $O(1)$ scaling of the hierarchical architecture is sound; the authors correctly identify that the contribution is not the asymptotic class (which is obvious from the tree structure) but the specific coefficient of that scaling. The analysis of the coordinator duty cycle trade-off (Power vs. Availability vs. Handoff reliability) is comprehensive and provides actionable engineering heuristics.

### 4. Clarity & Structure
**Rating: 5**

The manuscript is exceptionally well-written. The structure is logical, moving from architecture definitions to simulation setup, then results, and finally sensitivity analysis. Figures are well-captioned and informative.

*   **Table III (Traffic Accounting)** is particularly helpful for reproducibility.
*   **Table VII (Coordinator Capacity)** clearly delineates between unscheduled and TDMA requirements, a crucial distinction for system designers.
*   The distinction between "Global-State Mesh" (theoretical upper bound) and "Sectorized Mesh" (practical implementation) is handled with high clarity.

### 5. Ethical Compliance
**Rating: 5**

The authors provide a clear acknowledgment of AI-assisted ideation in the Acknowledgments section, complying with emerging standards for transparency. No human subjects are involved. The research appears ethically sound.

### 6. Scope & Referencing
**Rating: 5**

The paper fits squarely within the scope of IEEE TAES, specifically the intersection of space systems, autonomy, and communications. The reference list is comprehensive, spanning foundational texts (Kleinrock, Lamport), standard space engineering references (SMAD), and recent literature on mega-constellations and swarm robotics.

---

## Major Issues

1.  **Clarification of "1 kbps" Budget vs. Physical Link Rate:**
    In Section III-F ("Communication Overhead Definition"), the distinction between the 1 kbps *traffic budget* and the physical link rate (1-10 Gbps) is made, but it is critical for the interpretation of latency. If a reader misses this distinction, the serialization delay of a 512-byte message on a 1 kbps link would be $>4$ seconds, contradicting the latency results in Table V ($\sim$500ms).
    *   *Requirement:* Please add a specific sentence or footnote in **Table V** or **Section IV-B** explicitly reminding the reader that serialization delay is negligible because the physical link is Gbps-class, and the 1 kbps figure is solely an accounting budget for capacity planning.

2.  **MAC Efficiency ($\gamma$) Application:**
    In Section IV-G and Table VIII, the paper applies the MAC efficiency factor $\gamma$. The text states: *"Note that applying the MAC efficiency penalty $1/\gamma$ to the unscheduled threshold is incorrect..."* This is a subtle but vital point.
    *   *Requirement:* The derivation of the 50 kbps unscheduled threshold relies on the "random-phase burstiness." Is this burstiness derived from a Poisson approximation or the actual uniform random phase offsets in the DES? If it is the latter, does the DES explicitly model the "tail drop" mechanism at the coordinator queue within the cycle? Please clarify in **Section IV-G** whether the 50 kbps threshold is an analytical derivation or a measured DES result where drops were observed.

---

## Minor Issues

1.  **Figure 3 (Latency Distribution):** The caption notes that the $10^6$ node curve is an "analytical extrapolation." This is acceptable, but visually it looks identical to the simulation data. Please consider making the $10^6$ line dashed or distinct to visually separate simulation data from extrapolation.
2.  **Equation 10 (Power Overhead):** The equation $\Delta P_{avg} = \Delta P_{coord} / k_c$ assumes the coordinator power penalty is perfectly amortized. It might be worth mentioning that this assumes a homogeneous fleet where every node is capable of being a coordinator (carrying the necessary antenna hardware), which implies a mass penalty on *every* node, even if the power penalty is time-averaged.
3.  **Abstract:** The phrase "model-form uncertainty $\eta_{eff} \in [18\%, 27\%]$" is slightly dense for the abstract without context. Consider rephrasing to "effective overhead $\eta_{eff} \approx 18\text{--}27\%$ when accounting for MAC efficiency."
4.  **Section IV-E (Validation):** The text states the DES matches analysis to within 0.05%. This is expected since the DES implements the accounting model. It might be more accurate to call this "Verification" (code matches model) rather than "Validation" (model matches reality), though in simulation studies these terms are often used interchangeably.

---

## Overall Recommendation

**Minor Revision**

The manuscript is of high quality and presents significant, actionable engineering data for the design of autonomous space swarms. The methodology is sound within the stated scope, and the limitations are honestly acknowledged. The revisions requested are primarily for clarity to prevent misinterpretation of the link budget definitions and to tighten the explanation of the coordinator queueing model.

---

## Constructive Suggestions

1.  **Add a "Key Design Recommendations" Table:** Synthesize the findings into a lookup table for engineers. Columns could be: "Swarm Size," "Recommended Topology," "Coordinator Bandwidth (TDMA)," "Coordinator Bandwidth (Random)," "Expected Overhead." This would significantly increase the practical impact of the paper.
2.  **Expand on the "Sectorized Mesh" Hybrid Nature:** In the Discussion, emphasize that the "Sectorized Mesh" as modeled is actually a *local hierarchy* (due to the sector coordinator). This reinforces the finding that some form of aggregation/hierarchy is inevitable for efficiency, even in "mesh" designs.
3.  **AoI vs. Dynamics:** In Section IV-F, you mention the AoI metric. It would be valuable to briefly mention the *orbital regime* dependency. In LEO, 400s staleness is different than in GEO due to relative velocities. A brief sentence contextualizing the 400s P99 AoI against a typical LEO relative velocity ($\sim$7 km/s closing speed) would highlight the danger of the $p_{exc}=0.10$ setting.