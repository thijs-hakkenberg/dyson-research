---
paper: "02-swarm-coordination-scaling"
version: "cb"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-28"
recommendation: "Unknown"
---

Here is a comprehensive peer review of the manuscript **"Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version CB)**, prepared for *IEEE Transactions on Aerospace and Electronic Systems*.

---

## 1. Significance & Novelty
**Rating: 5 (Excellent)**
The manuscript addresses a critical gap in the aerospace literature: the lack of closed-form sizing relationships for coordinating massive satellite constellations ($10^3$--$10^5$ nodes). While commercial mega-constellations exist, their coordination logic remains proprietary and largely centralized. This paper provides a generalized, open-source framework for hierarchical coordination that is distinct from standard ad-hoc routing or pure swarm robotics approaches. The distinction between "byte budget" feasibility and "TDMA airtime" feasibility is a significant contribution that prevents the common pitfall of sizing links based solely on average throughput.

## 2. Methodological Soundness
**Rating: 5 (Excellent)**
The methodology is rigorous and multi-layered. The authors employ a "verification taxonomy" that effectively combines analytical derivations, cycle-aggregated Discrete Event Simulation (DES), slot-level TDMA simulation, and packet-level validation. The derivation of the MAC efficiency parameter ($\gamma = 0.76$) from CCSDS Proximity-1 standards is a substantial improvement over previous versions that relied on assumptions. The use of the Gilbert-Elliott model for correlated losses is appropriate for the LEO environment (structural shadowing/tumbling), and the sensitivity analysis regarding coherence time is insightful.

## 3. Validity & Logic
**Rating: 4 (Good)**
The logic is generally sound. The transition from the 1 kbps RF-backup constraint to the high-bandwidth optical ISL regime is handled well, clarifying that the sizing equations are binding primarily for the backup case. The argument for the "stress case" ($\eta \approx 46\%$) vs. "routine operations" ($\eta \approx 5\%$) is logically consistent.
*Critique:* The paper argues that centralized command generation makes overhead topology-invariant. While true for the specific message model chosen, this is a strong assumption. If the architecture shifted to distributed consensus (as briefly mentioned), the topology would matter immensely. The paper acknowledges this, but the "topology-invariant" claim in the abstract/intro could be slightly too strong without the "under centralized command" qualifier.

## 4. Clarity & Structure
**Rating: 5 (Excellent)**
The manuscript is exceptionally well-structured. The progression from research questions to analytical models, then to simulation results, and finally to standards-based validation is logical. Figures are clear (particularly Fig. 8 regarding the design envelope). The notation table is helpful. The distinction between the three feasibility layers (Byte, MAC, Airtime) is communicated effectively.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**
The authors provide a clear Data Availability statement with a GitHub link (anonymized for review, presumably). They also include a specific acknowledgment regarding AI usage in the ideation phase, which aligns with emerging transparency standards in scientific publishing.

## 6. Scope & Referencing
**Rating: 4 (Good)**
The literature review covers the necessary bases: constellation management, swarm robotics, and networking. The inclusion of CCSDS standards (Proximity-1, TM Sync) anchors the work in reality.
*Critique:* The paper could benefit from slightly more engagement with recent work on "mega-constellation" routing (e.g., recent papers on Starlink topology from *IEEE/ACM Transactions on Networking*) to better situate the *control plane* traffic (this paper) against the *user plane* traffic (routing papers).

## 7. Theoretical Depth
**Rating: 4 (Good)**
The queueing theory application ($D[k_c]/D/1$) and the Markov chain analysis for GE recovery are correctly applied. The derivation of the unicast stagger cycles ($L_{cmd}$) is a useful theoretical contribution for operational planning.

## 8. Simulation/Experimentation
**Rating: 5 (Excellent)**
The simulation campaign is robust. The use of 30 Monte Carlo replications with bootstrap confidence intervals is statistically sound. The cross-validation between the DES (fluid flow) and the slot-level simulator (discrete timing) is a highlight, specifically revealing the "hidden" coupling between ARQ and TDMA scheduling that the fluid model missed.

## 9. Practical Applicability
**Rating: 5 (Excellent)**
This is the paper's strongest point. The "Design Equations Summary" (Section V-C) is immediately useful for systems engineers. The link budget justification for the 1 kbps backup channel is grounded in physics (Friis transmission equation parameters for UHF omnis). The decision rules for GE recovery (intra-cycle vs. inter-cycle) provide actionable guidance.

## 10. Overall Quality
**Rating: 5 (Excellent)**
This is a high-quality manuscript that meets the standards of a top-tier journal. It moves beyond qualitative descriptions of swarms to provide hard engineering constraints and sizing rules.

---

## Major Issues

1.  **Clarification of "Topology Invariance" Scope**
    *   **Issue:** The abstract and introduction claim that command traffic is "topology-invariant." This holds *only* because the authors assume a centralized command generation model where the hierarchy acts merely as a distribution tree. If the cluster coordinators were generating commands based on local consensus, overhead would be highly topology-dependent.
    *   **Why it matters:** Readers might misinterpret this as a general property of hierarchical swarms, rather than a specific property of the *centralized-command-over-hierarchy* architecture modeled here.
    *   **Remedy:** Qualify this claim in the Abstract and Introduction. Change "is topology-invariant" to "is topology-invariant under centralized command generation." (Section IV-E discusses this, but the initial framing needs the caveat).

2.  **Antenna Slew/Acquisition in the $\gamma$ Derivation**
    *   **Issue:** In Table X (Gamma Decomposition), an acquisition efficiency of 0.955 (5ms dwell) is used. However, for a rotating TDMA schedule among 100 nodes, the coordinator must re-point or re-phase (if phased array) for *every* slot.
    *   **Why it matters:** If the RF-backup utilizes simple UHF omnidirectionals (as per the Link Budget justification), there is no pointing loss or acquisition time—it is broadcast/receive-all. If it uses directional S-band (ISL mode), 5ms might be optimistic for mechanical steering, though fine for electronic.
    *   **Remedy:** Clarify in Section IV-J whether the RF-backup mode (the binding constraint) assumes directional antennas. If it is omnidirectional (as suggested in Table VI), the $\gamma_{acq}$ term should perhaps be 1.0, which would actually *improve* the margin. If the system requires directional antennas to close the link at 30 kbps, this contradicts the "omnidirectional backup" claim. Please reconcile the antenna assumption in the Link Budget (Omni) with the Gamma derivation (Acquisition loss included).

## Minor Issues

1.  **Table I (Notation):** The definition of $\eta$ is given as "Protocol overhead... beyond baseline." It would be helpful to explicitly state here that baseline is 20.5%, so readers don't have to hunt for that number later.
2.  **Section III-B-2 (Coordinator Failure):** The text mentions "inertial coasting." For LEO satellites in low altitudes (e.g., 300-400km), drag is significant. Clarify if "inertial coasting" implies "decaying orbit" or if there is autonomous station-keeping that doesn't require coordination.
3.  **Fig. 6 (TDMA Comparison):** The y-axis label "Coordinator Utilization" could be clearer. Is this Time Utilization or Byte Utilization? Given the distinction made in the paper, precision here is key.
4.  **Reference Style:** Ensure all references (e.g., [1] Starlink) follow IEEE format strictly. "Non-archival; accessed Feb 2026" is acceptable for web sources, but ensure the URL is stable if possible.
5.  **Typos:**
    *   Section IV-A: "scheduling disciplines converge to ~21--25 kbps" - clarify if this refers to the *required capacity* or the *throughput*.
    *   Table VIII: "Delivered $\eta$" column header is slightly ambiguous. Perhaps "Effective Throughput" or "Goodput"?

## Overall Recommendation
**Recommendation: Accept with Minor Revisions**

This is an excellent paper that provides a rigorous, quantitative foundation for sizing spacecraft swarm communication networks. The authors have successfully addressed the complexities of hierarchical scaling, specifically distinguishing between byte-level and time-slot-level constraints.

The "Major Issues" listed above are primarily regarding scoping and consistency of assumptions (antenna types) rather than fundamental flaws in the derivation. Once the authors reconcile the omnidirectional link budget assumption with the directional acquisition loss in the efficiency calculation, and qualify the topology-invariance claim, the paper will be ready for publication.

## Constructive Suggestions

1.  **Impact of $\gamma$ on Omni-directional Backup:** If you remove the acquisition penalty ($\gamma_{acq}$) because the backup link is omnidirectional (Table VI), your derived $\gamma$ increases from 0.76 to $\approx 0.79$. This would relax your binding constraint slightly. It is worth adding a sentence discussing this "Omni-bonus."
2.  **Visualizing the "Cliff":** Figure 5 (TDMA-GE sensitivity) is very effective. Consider annotating the "Cliff" where the system transitions from stable to unstable to make it even more accessible to practitioners.
3.  **Future Work - Orbital Dynamics:** You mention orbital mechanics are future work. A brief sentence speculating on the impact of Doppler shift on the guard times (currently 4.7ms) would add robustness. (e.g., "Doppler at S-band for LEO-LEO relative velocity is approx X kHz, which is handled by the radio PLL, but propagation delay variation is the primary driver for guard times.")