---
paper: "02-swarm-coordination-scaling"
version: "v"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-24"
recommendation: "Minor Revision"
---

## Peer Review: IEEE Transactions on Aerospace and Electronic Systems

**Manuscript Title:** Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study
**Version:** V

---

### 1. Significance & Novelty
**Rating: 5**

This manuscript addresses a critical and timely gap in the aerospace engineering literature: the "middle ground" of coordination scaling between established constellation management ($<10^4$ nodes, ground-centric) and theoretical swarm robotics ($>10^6$ nodes, often abstract). As commercial mega-constellations (Starlink, Kuiper) expand and future architectures (Dyson precursors, orbital manufacturing) are considered, the specific engineering trade-offs of hierarchical coordination at the $10^5$-node scale become vital.

The novelty lies not in the hierarchical topology itself (which is standard in networking), but in the **rigorous, byte-level characterization of the design envelope** specifically for orbital mechanics constraints (collision avoidance, ephemeris propagation). The distinction between "message-layer" and "physical-layer" overhead, combined with the explicit comparison of TDMA vs. random-phase scheduling for coordinator links, provides actionable engineering data that is currently missing from high-level architectural studies. The introduction of the "Sectorized Mesh" as a hybrid comparator is a significant improvement over standard binary comparisons between centralized and fully distributed systems.

### 2. Methodological Soundness
**Rating: 4**

The methodology is generally robust. The use of a cycle-aggregated Discrete Event Simulation (DES) is appropriate for the scale ($10^5$ nodes) where packet-level simulation would be computationally prohibitive. The authors are careful to define their abstraction layer (Table V) and traffic accounting (Table VII), which aids reproducibility.

**Strengths:**
*   **Explicit Accounting:** The breakdown of overhead into baseline telemetry vs. protocol overhead is excellent.
*   **Statistical Rigor:** The Monte Carlo approach with bootstrap confidence intervals is standard and well-applied.
*   **TDMA Analysis:** Deriving the MAC efficiency parameter $\gamma$ and the zero-drop thresholds from the timing model is a strong methodological contribution.

**Weaknesses:**
*   **"Validation" Circularity:** The paper frequently claims the DES "validates" the analytical protocol coefficient. Since the DES implements the same counting logic as the analytical formula, this is code verification, not physical validation. (See Major Issues).
*   **Link Model Discretization:** The Gilbert-Elliott model transitions only once per $T_c$ (10s). This is very coarse for LEO channel dynamics where fading can occur on millisecond timescales. While the authors acknowledge this, it limits the fidelity of the burst-error analysis.

### 3. Validity & Logic
**Rating: 4**

The conclusions are logically derived from the data. The identification of the 5–46% design envelope is well-supported by the workload profiles. The argument that centralized architectures fail due to spectrum/latency rather than processing capacity is nuanced and correct, distinguishing this work from naive scalability studies.

However, the validity of the "stress-case" saturation relies heavily on the **1 kbps/node control-plane budget**. While the authors justify this as a "traffic budget" rather than a physical link rate, it is an arbitrary constraint. If the budget were 10 kbps (still negligible on a 1 Gbps optical link), the "saturation" concerns would vanish. The paper treats this budget as a hard constraint rather than a variable design parameter, which colors the severity of the overhead conclusions.

### 4. Clarity & Structure
**Rating: 5**

The manuscript is exceptionally well-written. The structure is logical, moving from architecture definitions to simulation setup, then results, and finally sensitivity analysis.
*   **Tables:** Tables VII (Traffic Accounting) and VIII (Link Availability) are exemplary in their detail.
*   **Figures:** Figure 5 (Overhead Scaling) and Figure 12 (TDMA Comparison) clearly convey complex trade-offs.
*   **Definitions:** The distinction between "delivered overhead" and "offered load" is handled with necessary precision.

### 5. Ethical Compliance
**Rating: 5**

The authors provide a specific disclosure regarding AI-assisted ideation in the Acknowledgments, which meets and exceeds standard transparency requirements. No human subjects or hazardous materials are involved. The research appears ethically sound.

### 6. Scope & Referencing
**Rating: 5**

The paper is perfectly scoped for *IEEE TAES*. It bridges the gap between pure networking theory and orbital systems engineering. The references are comprehensive, covering historical foundations (O'Neill, Reynolds), current constellation operations (Starlink, OneWeb), and relevant theoretical frameworks (AoI, Mean-field games). The inclusion of CCSDS standards (BPv7, Proximity-1) grounds the work in practical space systems engineering.

---

### Major Issues

1.  **Verification vs. Validation:**
    In Section IV-E and throughout the text, the authors state that the DES "validates" the analytical protocol coefficient ($O(1)$ scaling). This is terminologically incorrect. Because the DES is built upon the same message generation rules as the analytical formula (Table VII), the close agreement ($<0.1\%$) confirms that the *code is bug-free* (verification), not that the *model represents reality* (validation). True validation would require comparison against hardware-in-the-loop data or high-fidelity packet-level simulation (e.g., NS-3).
    *   *Required Revision:* Rephrase these claims to emphasize "verification of the simulation implementation" or "confirmation of analytical predictions," rather than "validation."

2.  **Justification of the 1 kbps Budget:**
    The central tension of the paper—that overhead reaches 46% and threatens saturation—is predicated on the 1 kbps/node budget. Given that the authors assume optical ISLs (1–10 Gbps) for handoffs, restricting the control plane to $10^{-6}$ of the link capacity seems overly conservative.
    *   *Required Revision:* Provide a stronger justification for this specific constraint. Is it based on a specific processor I/O limit, a legacy bus constraint (e.g., CAN/SpaceWire), or a specific "tax" requirement from commercial operators? A sensitivity analysis extending the budget to 10 kbps would likely show that the system is nowhere near saturation, changing the narrative from "design envelope" to "ample margin."

3.  **Age of Information (AoI) Context:**
    The AoI analysis (Section IV-F) shows P99 staleness of >400s for exception-based telemetry. The paper calls this a "proxy for coordination freshness." However, without linking this to orbital dynamics, the number is hard to interpret. For a satellite in a stable orbit, 400s old data might be perfectly fine. For a satellite undergoing a maneuver, it is fatal.
    *   *Required Revision:* The authors should explicitly state that the acceptability of the AoI values depends entirely on the *prediction error covariance growth rate*, which is not modeled. The current text implies 400s is "bad" without establishing the error bounds associated with that delay.

---

### Minor Issues

1.  **Table VIII (Link Availability):** The distinction between "Delivered $\eta$" and "Offered" is crucial but slightly confusing in the table headers. "Offered" implies the load presented to the MAC, while "Delivered" implies goodput. Please add a footnote or clarify in the caption that "Offered" is the metric to be used for link dimensioning/sizing.
2.  **Figure 2 (Latency Distribution):** The caption mentions the $10^6$ node curve is an "analytical extrapolation." This is honest, but visually it looks like simulation data. Please make the line style distinct (e.g., dotted) to visually separate it from the DES-measured data.
3.  **Section III-B-2 (Handoff):** The paper states handoff uses a "separate optical ISL terminal." This assumes a hardware architecture with multiple terminals. If a node has only one optical head, it cannot maintain the coordination mesh while doing the bulk transfer. Please clarify if the availability analysis accounts for the temporary loss of the coordination link during the 1-10s handoff if single-terminal hardware is used.
4.  **Gilbert-Elliott Discretization:** In Section III-J, the state transitions occur once per $T_c$ (10s). This effectively makes the minimum burst duration 10s. Please explicitly state that this model cannot capture sub-10s fading (e.g., antenna pointing jitter) and is intended only for macroscopic outages (occlusion).

---

### Overall Recommendation
**Minor Revision**

The manuscript represents a high-quality, rigorous contribution to the field. The simulation framework is sound, and the results provide valuable engineering guidelines for future constellation architects. The issues identified (terminology regarding validation, justification of the bandwidth constraint) are matters of framing and clarification rather than fundamental flaws in the data or analysis.

---

### Constructive Suggestions

1.  **Rename "Validation" to "Verification":** In Section IV-E, change the header to "Analytical Verification" and rewrite the text to acknowledge that the perfect match confirms the code correctly implements the accounting model.
2.  **Expand the Bandwidth Sensitivity:** In Section IV-I (Parametric Sensitivity), add a brief discussion or a second axis to Figure 11 showing how the "saturation" risk evaporates if the control plane budget is raised to 5 or 10 kbps. This puts the "46% overhead" result in better context.
3.  **Refine the AoI Conclusion:** In the abstract and conclusion, qualify the AoI result. Instead of just stating "P99 AoI exceeds 400s," add "which requires high-fidelity onboard orbital propagation to maintain safety margins."
4.  **TDMA Implementation Detail:** In Section IV-J, explicitly mention that the TDMA capacity gain comes at the cost of requiring precise fleet-wide time synchronization (which is non-trivial at LEO velocities), whereas the random-phase approach is robust to timing drift. This adds operational context to the byte-level result.