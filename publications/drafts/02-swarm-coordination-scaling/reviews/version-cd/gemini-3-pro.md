---
paper: "02-swarm-coordination-scaling"
version: "cd"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-28"
recommendation: "Unknown"
---

Here is a comprehensive peer review of the manuscript.

---

**Manuscript ID:** [Assigned by Editor]
**Title:** Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms
**Version:** CD

## 1. Significance & Novelty
**Rating: 5 (Excellent)**
The manuscript addresses a critical gap in the literature: the lack of closed-form sizing relationships for spacecraft swarms in the $10^3$--$10^5$ node regime. While mega-constellation networking (routing) is well-studied, the specific problem of *command and control coordination* under strict bandwidth constraints (1 kbps RF backup) is novel. The derivation of the "stress-case" overhead bound ($\eta_S \approx 46\%$) and the distinction between byte-layer and airtime-layer feasibility are significant contributions that will aid future mission architects.

## 2. Methodological Soundness
**Rating: 5 (Excellent)**
The multi-tiered verification approach is rigorous. The authors successfully employ:
1.  **Analytical derivation:** Closed-form equations for overhead and capacity.
2.  **Message-level DES:** Validating the equations and exploring stochastic distributions (especially the bimodal nature of coordinator ingress).
3.  **Slot-level TDMA simulation:** Crucially identifying the "hidden" coupling between ARQ and TDMA framing that the fluid-flow DES misses.
4.  **Packet-level validation:** Deriving $\gamma$ from CCSDS standards rather than assuming it.
The explicit handling of the Gilbert-Elliott (GE) channel model and its interaction with TDMA slot timing is a highlight of methodological rigor.

## 3. Validity & Logic
**Rating: 4 (Good)**
The internal logic is strong. The progression from simple byte counting to complex TDMA schedulability is logical. The argument that the 1 kbps RF backup is the design-driving constraint (despite the existence of high-speed ISLs) is well-justified via safety-critical reasoning.
*Critique:* The assumption of centralized command generation for the stress case is a strong driver of the results. While the authors acknowledge this and discuss distributed consensus briefly, the paper would benefit from explicitly bounding how a decentralized task allocation logic would alter the $\eta_{\text{cmd}}$ term in the sizing equations.

## 4. Clarity & Structure
**Rating: 5 (Excellent)**
The paper is exceptionally well-written. The distinction between "Architecture-specific" and "Workload-dependent" overhead is clear. Figures are informative, particularly Fig. 6 (TDMA/GE sensitivity) and Fig. 9 (Coordinator buffer CDF). The "Validation Gap" section (Table XIV) is a model of intellectual honesty, clearly delineating what is proven vs. what requires future NS-3 work.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**
The authors provide a clear Data Availability statement with a GitHub link (anonymized for review). The acknowledgment of AI-assisted ideation is transparent and complies with emerging publication standards.

## 6. Scope & Referencing
**Rating: 5 (Excellent)**
The literature review covers the necessary bases: swarm robotics, constellation management, and delay-tolerant networking. The connection to CCSDS standards (Proximity-1) grounds the work in flight-proven reality, distinguishing it from purely theoretical academic exercises.

## 7. Theoretical Depth
**Rating: 4 (Good)**
The application of queueing theory ($D/D/1$ and $M/D/1$) is appropriate. The adaptation of Age of Information (AoI) metrics to the swarm context is useful. The derivation of the generalized gamma expression (Eq. 14) is a valuable theoretical tool for practitioners.

## 8. Simulation Rigor
**Rating: 5 (Excellent)**
The use of 30 Monte Carlo replications with bootstrap confidence intervals is standard and appropriate. The decision to build three distinct simulators (DES, Slot-level, Packet-level) to cross-validate results at different granularities is impressive and mitigates the risk of implementation error.

## 9. Practical Utility
**Rating: 5 (Excellent)**
This is the paper's strongest point. It provides actionable design equations and "rule of thumb" values (e.g., 30 kbps minimum coordinator PHY rate). The link budget justification (Table VI) ensures the parameters are physically realizable.

## 10. Overall Quality
**Rating: 5 (Excellent)**
A high-quality, rigorous, and practically relevant contribution to the field of aerospace electronic systems.

---

## Major Issues

1.  **Contextualization of the Stress Case ($d=1$):**
    *   **Issue:** The abstract and conclusion highlight $\eta_S \approx 46\%$ prominently. While the text explains this is a continuous-duty bound, a casual reader might interpret this as the *nominal* operating cost of hierarchy, which would seem prohibitively high compared to mesh architectures.
    *   **Why it matters:** It risks misrepresenting the efficiency of the hierarchical architecture.
    *   **Remedy:** In the Abstract and Conclusion, explicitly pair the 46% figure with the "Routine Operations" figure ($\approx 5\%$) to provide immediate context. Ensure the distinction between *capacity sizing* (designing for 46%) and *nominal load* (operating at 5%) is sharp.

2.  **Unicast Command Latency Implications:**
    *   **Issue:** The paper identifies that Type 2 (unicast) commands require a 22-cycle stagger (Eq. 7). This implies a command latency of $>3$ minutes for the last node in the cluster.
    *   **Why it matters:** For time-critical fleet reconfiguration (e.g., collision avoidance), this latency might be unacceptable.
    *   **Remedy:** Add a brief discussion on the operational impact of this stagger. Does this force the system to rely on broadcast commands for all safety-critical actions? If so, state that constraint explicitly.

## Minor Issues

1.  **Table I (Notation):** The definition of $\gamma$ refers to Eq. 14, but in the text, it is often discussed before Eq. 14 is formally introduced. Ensure the flow of definition matches the reading order.
2.  **Fig. 3 (Phase Stagger):** The caption mentions "random phase" vs. "phase stagger." Please clarify in the text if "random phase" implies a uniform distribution of start times within $T_c$.
3.  **Section IV-C (GE Model):** The text states "Antenna mispointing... has $\tau_c \geq T_c$." It would be helpful to clarify if this refers to the mechanical settling time or the control loop frequency.
4.  **Eq. 14:** The term $R_{\text{PHY}}/1000$ implies $R_{\text{PHY}}$ is in bps and the result is scaled. Please verify the units to ensure dimensional consistency (ms vs seconds).

## Overall Recommendation
**Recommendation: Accept with Minor Revisions**

This is an outstanding manuscript that sets a new standard for analyzing large-scale swarm coordination. The authors have successfully navigated the trade-off between high-level architectural sizing and low-level physical layer constraints. The three-layer feasibility framework (Byte Budget $\to$ MAC Efficiency $\to$ TDMA Airtime) is a robust contribution.

The revision should focus solely on clarifying the operational context of the "stress case" to prevent misinterpretation of the overhead costs, and briefly addressing the operational consequences of the unicast command latency. The validation against CCSDS standards and the rigorous cross-verification between DES and slot-level simulations make this paper highly trustworthy.

## Constructive Suggestions

1.  **Refine the "Design Envelope" Visual:** Figure 10 (Workload Comparison) is good, but a 2D plot showing "Campaign Duty Factor ($d$)" on the X-axis and "Required Coordinator Capacity" on the Y-axis, with regions shaded for "Feasible at 24kbps" and "Feasible at 30kbps," would be a powerful summary graphic for system engineers.
2.  **Explicit "Safe Mode" Definition:** You mention safe-mode requires $\eta \approx 5.7\%$. It would be valuable to explicitly list the message types allowed in safe mode in a small sub-table (e.g., "Heartbeat: Yes, Status: Decimated, Commands: Broadcast Only").
3.  **Generalized Gamma Applicability:** In the discussion, explicitly mention that Eq. 14 can be adapted for other protocols (e.g., CSP or ZigBee) by substituting the framing overhead bits, broadening the paper's appeal beyond CCSDS users.