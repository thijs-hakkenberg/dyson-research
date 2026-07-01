---
paper: "02-swarm-coordination-scaling"
version: "cc"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-28"
recommendation: "Unknown"
---

Here is a rigorous peer review of the manuscript "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version CC), prepared for *IEEE Transactions on Aerospace and Electronic Systems*.

---

# Peer Review Report

**Manuscript ID:** [Assumed Version CC]
**Title:** Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms
**Target Journal:** IEEE Transactions on Aerospace and Electronic Systems

## 1. Significance & Novelty
**Rating: 5 (Excellent)**
The manuscript addresses a critical gap in the aerospace literature: the specific scaling properties of coordination protocols for "mega-constellations" ($10^4$--$10^5$ nodes). While networking literature covers routing, and robotics literature covers small swarms, this paper uniquely derives closed-form sizing equations for the *coordination layer* (byte-level accounting) under realistic space link constraints. The distinction between the "byte budget," "MAC efficiency," and "TDMA airtime" feasibility layers is a significant conceptual contribution that will aid future system architects.

## 2. Methodological Soundness
**Rating: 5 (Excellent)**
The methodology is robust. The authors employ a multi-tiered verification strategy (IEEE 1012 style) that is highly appropriate for this domain. The combination of:
1.  Closed-form analytical derivations;
2.  Cycle-aggregated Discrete Event Simulation (DES) for fleet-wide statistics;
3.  Slot-level TDMA simulation for timing/schedulability; and
4.  Packet-level validation based on CCSDS standards to derive $\gamma$;
provides a high degree of confidence in the results. The explicit handling of the "stress case" versus "nominal operations" via the campaign duty factor ($d$) adds necessary operational realism.

## 3. Validity & Logic
**Rating: 4 (Good)**
The logic is generally sound. The derivation of the MAC efficiency ($\gamma = 0.76$) from CCSDS Proximity-1 standards is a major improvement over previous iterations (where it might have been assumed). The link budget justification for the 1 kbps RF-backup channel is technically defensible.
*Critique:* The argument regarding "topology-invariant command overhead" relies heavily on the assumption of centralized command generation. While the authors acknowledge this, the paper would benefit from a slightly stronger caveat that this invariance breaks down if the swarm adopts distributed task allocation (e.g., market-based auctions), which is a common proposal in autonomy literature.

## 4. Clarity & Structure
**Rating: 5 (Excellent)**
The manuscript is exceptionally well-structured. The progression from analytical equations to simulation results to physical-layer validation is logical. Tables are dense but informative. The distinction between the three workload profiles (Nominal, Event, Stress) is clearly defined and consistently applied.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**
The authors provide a clear Data Availability statement with a GitHub link. They also transparently disclose the use of AI for ideation in the Acknowledgments, adhering to emerging best practices.

## 6. Scope & Referencing
**Rating: 4 (Good)**
The literature review covers the intersection of swarm robotics and satellite networking well. The references to CCSDS standards (Proximity-1, TM Sync) are crucial and well-placed.
*Critique:* The paper could briefly reference the Consultative Committee for Space Data Systems (CCSDS) *Schedule Aware Bundle Routing* (SABR) or similar delay-tolerant networking (DTN) efforts more explicitly in the context of the "store-and-forward" nature of the hierarchical summaries, though this is a minor omission given the focus on the coordination layer rather than the transport layer.

---

## Major Issues

**1. Contextualization of the "Non-Binding" High-Rate Regime**
*   **Issue:** The paper states that at $\geq$10 kbps, all constraints are "non-binding." While mathematically true for the *message layer*, this ignores the processing latency scaling at the coordinator node. If a coordinator receives 100 kbps of traffic, the CPU load for deserialization, integrity checking, and logic processing increases linearly.
*   **Why it matters:** Readers might assume that increasing bandwidth solves all scaling problems, neglecting the compute bottleneck on radiation-hardened processors.
*   **Remedy:** In Section IV-A or the Discussion, briefly quantify the CPU load (IPS/FLOPS) required at the coordinator for the 100 kbps regime to confirm it remains within the capabilities of standard flight computers (e.g., LEON3/4 or ARM Cortex-R).

**2. Unicast Stagger Logic Verification**
*   **Issue:** Equation (7) describes the unicast stagger cycles $L_{\text{cmd}}(q)$. The denominator uses $(1 - \alpha_{\text{RX}})$. However, if the system is half-duplex, the coordinator cannot transmit during the ingress slots.
*   **Why it matters:** It is crucial to ensure that the "egress" time available for commands doesn't overlap with the "ingress" time required for status reports *if* the radio is strictly half-duplex and single-channel.
*   **Remedy:** Please double-check that the slot-level simulator explicitly forbids the coordinator from transmitting command packets during the reserved member reporting slots. If the coordinator has a separate TX chain but shares the antenna, this constraint holds. If it has full-duplex capability (separate frequencies/antennas), the constraint relaxes. Clarify the transceiver assumption (Half-Duplex vs. Full-Duplex) in Section IV-A explicitly.

## Minor Issues

1.  **Table I (Notation):** The symbol $p_{\text{exc}}$ is defined as "Exception reporting probability," but in some contexts, it implies the probability of *generating* an exception message, while in others (AoI), it implies the probability of *sending* a report. Ensure consistent terminology (e.g., "Transmission probability under exception policy").
2.  **Section IV-C (GE Model):** The text states "structural shadowing matches $T_c$." A brief sentence explaining *why* structural shadowing (e.g., solar panel rotation relative to ISL antenna) operates on a 10s timescale would help readers unfamiliar with spacecraft attitude dynamics.
3.  **Figure 5 (AoI):** The y-axis label should clearly state whether it is "Mean AoI" or "P99 AoI" to match the caption and text discussion.
4.  **Typos:**
    *   Section IV-A: "margin $= 614$~ms" vs Table IV "623 ms". Please reconcile this small discrepancy (likely due to rounding or slight parameter shift).

---

## Overall Recommendation
**Recommendation: Accept with Minor Revisions**

This is a high-quality manuscript that offers a significant contribution to the field of space systems engineering. The derivation of sizing equations for hierarchical swarms, grounded in CCSDS standards and validated via multi-fidelity simulation, provides a "handbook" value for future mission designers. The authors have successfully addressed the complexity of the problem by decomposing it into byte-level, MAC-level, and airtime-level constraints.

The revisions requested are primarily clarifications to ensure the physical realism of the "non-binding" high-bandwidth claims and to tighten the definitions regarding half-duplex constraints. Once addressed, this paper will serve as a standard reference for scaling autonomous satellite coordination.

---

## Constructive Suggestions

1.  **Strengthen the "Campaign Duty Factor" Application:** The introduction of $d$ is excellent. To make it even more useful, consider adding a "Recommended Design Margin" subsection. For example, suggest that practitioners size the system for $d=0.1$ (intensive reconfiguration) but ensure the hardware can survive $d=1.0$ (stress) by degrading AoI, rather than sizing the hardware for $d=1.0$ which drives unnecessary cost.
2.  **Generalize Gamma Further:** Equation (13) is very useful. You might suggest that for optical ISLs, $\gamma$ could be much lower due to pointing acquisition times relative to packet duration, whereas for omni-directional RF, it is dominated by framing. A sentence contrasting $\gamma_{\text{RF}}$ vs $\gamma_{\text{Optical}}$ would add depth.
3.  **Visualizing the "Cliff":** Figure 6 (Workload Comparison) is good, but a "Feasibility Map" (Heatmap) with $N$ on the x-axis and $C_{\text{node}}$ on the y-axis, showing the regions where TDMA is required vs. CSMA, would be a powerful visual summary of the paper's findings.