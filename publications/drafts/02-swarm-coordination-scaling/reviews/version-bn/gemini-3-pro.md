---
paper: "02-swarm-coordination-scaling"
version: "bn"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-27"
recommendation: "Accept"
---

Here is the peer review for the manuscript "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version BN).

***

# Peer Review Report

**Journal:** IEEE Transactions on Aerospace and Electronic Systems
**Manuscript ID:** [Assigned by Editor]
**Version:** BN
**Date:** October 26, 2023

## 1. Significance & Novelty
**Rating: 5 (Excellent)**

This manuscript addresses a critical and rapidly emerging gap in the aerospace literature: the specific communication sizing requirements for autonomous coordination of mega-constellations ($10^3$--$10^5$ nodes). While existing literature covers routing in mega-constellations (Handley, Bhattacherjee) or small-scale swarm robotics (Brambilla, Dorigo), there is a distinct lack of rigorous, closed-form sizing models for the "middle ground" of large-scale autonomous fleet management.

The derivation of closed-form design equations that distinguish between byte-level, MAC-level, and airtime-level feasibility is a significant contribution. The distinction between architecture-specific overhead ($\eta_0$) and workload-dependent traffic ($\eta_{cmd}$) provides a valuable heuristic for system architects. Furthermore, the focus on the "RF backup" regime (1 kbps) as the design-driving case is a highly practical insight that moves beyond the optimistic assumptions often found in purely academic formation-flying papers. This work will likely serve as a foundational reference for sizing future autonomous constellation management systems.

## 2. Methodological Soundness
**Rating: 5 (Excellent)**

The methodology is rigorous and well-triangulated. The authors employ a dual approach: analytical derivation of closed-form equations backed by a custom cycle-aggregated Discrete Event Simulation (DES). The correspondence between the analytical model and the DES results ($<0.1\%$ discrepancy) builds strong confidence in the proposed equations.

The use of a Gilbert-Elliott (GE) model to capture correlated link losses is appropriate for the LEO environment, where obstructions and tumbling cause bursty errors. The analysis of the "stress case" versus "nominal" workloads effectively bounds the design space. The specific attention paid to TDMA frame timing (preamble, guard times, turnaround) adds a layer of engineering realism often missing from high-level protocol studies.

One minor methodological note: The assumption of static cluster membership for the DES duration is justified in the text, but the cross-plane re-association overhead calculation (Section V-B) relies on a heuristic ($\lambda_h$). While likely sufficient for this level of abstraction, a brief sensitivity analysis on $\lambda_h$ would strengthen the claim that dynamic topology effects are negligible.

## 3. Validity & Logic
**Rating: 4 (Good)**

The conclusions are generally well-supported by the data. The identification of the coordinator ingress link as the primary bottleneck (rather than CPU or egress) is logically sound given the asymmetry of the traffic model. The analysis of the "unicast stagger" problem (requiring 22 cycles for unique commands) is a crucial finding that highlights the limitations of hierarchical control for individualized actuation.

However, there is a slight logical tension regarding the "Sectorized Mesh" baseline. The authors argue that the mesh is an "intentional worst-case," but then cap the neighbor count to make it budget-feasible. The comparison in Table VI shows the mesh at 65-67% overhead versus the hierarchy at 46%. This comparison feels slightly asymmetric because the functional scope differs (local vs. cluster-wide). The authors acknowledge this in Table VII, but the text in Section IV-F could more clearly emphasize that the mesh is being penalized for a different *kind* of awareness (local density vs. hierarchical aggregation).

Additionally, the claim that "at $\geq$10 kbps... all message-layer constraints are non-binding" is valid within the model, but the discussion should more explicitly caveat that physical layer constraints (interference, Doppler shift management) likely become the new binding constraints at those rates, preventing a trivial solution.

## 4. Clarity & Structure
**Rating: 5 (Excellent)**

The paper is exceptionally well-written. The structure is logical, moving from problem definition to model, results, and discussion. The notation is consistent (Table I is very helpful), and the distinction between the three feasibility layers (Byte, MAC, Airtime) is maintained throughout.

The figures are high quality and directly support the text. Figure 5 (Workload Comparison) and Figure 9 (Cross-cycle recovery) are particularly effective at conveying complex trade-offs. The abstract is concise and quantitative, providing specific numbers that summarize the key findings. The "Design Equations Summary" in Section V-C is a fantastic addition that increases the paper's utility as a handbook for practitioners.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**

The authors provide a specific acknowledgment regarding the use of AI tools for ideation (Claude, Gemini, GPT), citing a specific methodology paper. This level of transparency regarding AI assistance is exemplary and sets a good standard. There are no apparent conflicts of interest or ethical concerns regarding the research subject matter.

## 6. Scope & Referencing
**Rating: 4 (Good)**

The scope is well-aligned with *IEEE TAES*. The references are comprehensive, bridging the gap between classical astrodynamics (Vallado, Wertz), networking (Handley, Cerf), and multi-agent systems (Dorigo, Lynch).

A small gap exists in the discussion of Time-Sensitive Networking (TSN) or deterministic networking standards. While the paper derives a custom TDMA frame, referencing standards like IEEE 802.1Qbv or TTEthernet (often used in avionics) would provide useful context, even if those specific protocols aren't used over the ISL. Additionally, a reference to specific radio hardware capabilities (e.g., S-band transceivers for CubeSats) would ground the 1 kbps / 24 kbps assumptions in COTS hardware reality.

***

## Major Issues

1.  **TDMA Synchronization Feasibility:**
    The paper assumes a TDMA structure with a guard time of 4.7ms (Section IV-A). While the derivation is sound based on propagation and turnaround, it assumes tight clock synchronization. The text mentions GNSS denial and a "sync beacon." However, in a large swarm with potential multi-hop distances from a GNSS-locked node, clock drift can accumulate. The paper should explicitly address the *precision* required for the sync beacon. If the coordinator fails, how quickly does the TDMA slotting degrade before the backup random-access mode is required? A brief calculation of clock drift vs. guard time during the election/handoff phase would validate the robustness of the $\gamma=0.85$ assumption during transients.

2.  **Coordinator Failure & RF-Backup Interaction:**
    In Section III-B (Coordinator failure transient), the paper notes a "Double-fault scenario" where optical ISL is down, forcing an RF-based election taking ~160s. This is a critical failure mode. The analysis assumes the RF channel is available for this election. However, if the system is under "Stress" workload ($\eta \approx 46\%$), the channel is already heavily utilized. Does the election traffic *preempt* the command/telemetry traffic? If not, the collision probability in Slotted ALOHA (used for backup) might extend the 160s recovery significantly. The interaction between high load and the contention-based election process needs clarification.

## Minor Issues

1.  **Table I (Notation):** The definition of $\eta$ includes $\eta_{cmd}$, but the text later defines $\eta_{total} = \eta + 20.5\%$. It might be clearer to explicitly label the 20.5% as $\eta_{baseline}$ in the table to avoid confusion between protocol overhead and total link utilization.
2.  **Section IV-A (Egress Model):** The text states "Commands are broadcast... Type 1." It later discusses "Type 2: Per-node unicast." It would be helpful to clarify if the "Stress" profile in Table VIII assumes Type 1 or Type 2 commands for the "1-Cycle?" check. (It appears to be Type 1 based on the checkmark, but explicit clarification in the table caption would help).
3.  **Section V-B (Limitations):** The cross-plane re-association rate calculation assumes a uniform distribution of node crossings. In some constellation geometries (e.g., Walker Star), crossings might be synchronized or bursty at the poles. A brief sentence acknowledging orbital geometry effects on handoff burstiness would be beneficial.
4.  **Equation 8:** The derivation of $\gamma$ is clear, but the variable $T_{slot}$ is used before it is formally defined in the text flow. Ensure the definition order is intuitive.
5.  **Typos:**
    *   Section III-B: "RF-backup handoff... ~113 s at 1 kbps" - verify the arithmetic consistency with the packet sizes listed.
    *   References: Ensure all "non-archival; accessed..." dates are updated to the final submission date.

## Overall Recommendation
**Accept with Minor Revisions**

This is a high-quality paper that makes a distinct theoretical and practical contribution to space systems engineering. The derivation of sizing equations for the "middle scale" of autonomy is novel and necessary. The validation via DES is robust. The requested revisions regarding TDMA synchronization drift and the interaction of election traffic with high-load baselines will strengthen the failure mode analysis but do not require a fundamental restructuring of the paper.

## Constructive Suggestions

1.  **Add a "Drift Analysis" Subsection:** In Section IV-A, add a short paragraph calculating how many cycles the cluster can maintain TDMA slotting without a sync beacon (based on standard TCXO drift rates) before guard times are violated. This quantifies the "coasting" capability of the swarm.
2.  **Refine Table VIII:** Split the "Stress" row into "Stress (Broadcast)" and "Stress (Unicast)" to explicitly show that Unicast fails the 1-cycle airtime constraint while Broadcast passes. This highlights the architectural constraint on command granularity.
3.  **Visualizing the Bottleneck:** Consider adding a small subplot to Figure 3 showing the "Unicast Stagger" delay as a function of cluster size ($k_c$). This would visually reinforce the $O(k_c)$ latency penalty for individualized control.
4.  **Hardware Mapping:** In the Discussion, briefly map the $C_{coord}$ requirements (24 kbps) to specific COTS radio classes (e.g., "Achievable with S-band patch antennas and SDRs typical of 3U CubeSats") to ground the theory in hardware reality.