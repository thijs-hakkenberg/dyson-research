---
paper: "02-swarm-coordination-scaling"
version: "bf"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-27"
recommendation: "Accept"
---

Here is a rigorous peer review of the manuscript "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version BF), prepared for *IEEE Transactions on Aerospace and Electronic Systems*.

---

# Peer Review Report

**Manuscript ID:** [Assigned by Editor]
**Title:** Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms
**Target Journal:** IEEE Transactions on Aerospace and Electronic Systems

## Review Criteria

### 1. Significance & Novelty
**Rating: 5 (Excellent)**

This manuscript addresses a critical and timely gap in the literature: the specific scaling properties of coordination architectures for "mega-constellations" ($10^3$--$10^5$ nodes). While existing literature covers small-scale swarms ($<100$ agents) or routing protocols for large networks, there is a distinct lack of closed-form sizing relationships for the *command and control* (C2) layer of autonomous fleets at this scale.

The novelty lies in the derivation of "practitioner-ready" design equations that link physical constraints (bandwidth, duty cycle) to architectural performance (AoI, recovery time). The differentiation between "nominal" ($\eta \approx 5\%$) and "stress-case" ($\eta \approx 46\%$) workloads is a significant contribution that challenges the assumption that hierarchical control is bandwidth-prohibitive for large swarms. The analysis of Gilbert-Elliott (GE) correlated losses in the context of orbital mechanics (shadowing vs. occultation) adds substantial practical value.

### 2. Methodological Soundness
**Rating: 4 (Good)**

The methodology combines standard queueing theory ($M/D/1$, $D[k]/D/1$) with a custom Cycle-Aggregated Discrete Event Simulation (DES). The approach is generally rigorous. The authors use the DES primarily to validate the analytical closed-form equations, which is a sound strategy. The use of 30 Monte Carlo replications with bootstrap confidence intervals is appropriate for this level of stochasticity.

However, there is a slight disconnect in the "Validation Gap" regarding the MAC layer. The paper derives $\gamma$ (MAC efficiency) analytically (Section IV.A) but acknowledges that the DES does not model contention. While the authors are transparent about this, the reliance on a calculated $\gamma = 0.85$ for TDMA without simulating slot drift or guard-time violations under realistic orbital uncertainty is a minor weakness. The assumption of static cluster membership for a 1-year simulation is justified for co-planar formations but perhaps too optimistic for cross-plane constellations where relative velocities are high; the authors acknowledge this in Section V.B, but a sensitivity analysis on dynamic re-clustering would strengthen the method.

### 3. Validity & Logic
**Rating: 5 (Excellent)**

The conclusions are logically derived from the data. The distinction between "link rate" (burst capacity) and "traffic budget" (average allocation) is crucial and well-handled. The analysis of the Gilbert-Elliott model is particularly strong; the finding that intra-cycle retransmission is structurally ineffective during bad-state bursts (due to the coherence time assumption) is a critical insight for protocol designers.

The comparison against baselines (Centralized and Global-State Mesh) is fair. The authors explicitly state that these are "intentional bounds" rather than strawmen, and they correctly identify that the centralized bottleneck is spectrum/latency, not compute. The logic regarding the "Bandwidth-Robustness Tradeoff" (Section IV.F) is sound: the hierarchy saves bandwidth at the cost of coordinator dependence, while the mesh pays a bandwidth premium for local robustness.

### 4. Clarity & Structure
**Rating: 4 (Good)**

The paper is dense but well-organized. The progression from Research Questions to Simulation Framework to Results is logical. The "Design Equations Summary" in Section V.C is an excellent addition for practitioners.

There are, however, areas where the density of information hinders readability. The abstract is heavily packed with quantitative results, making it difficult to grasp the high-level narrative immediately. In Section IV.A, the discussion on "Type 1" vs "Type 2" commands and their impact on $\eta$ vs. schedulability is complex and requires careful reading to disentangle "byte budget" from "delivery time."

### 5. Ethical Compliance
**Rating: 5 (Excellent)**

The authors provide a specific acknowledgment regarding AI-assisted ideation (Claude 4.6, etc.), citing a specific internal report/policy. This transparency is commendable and aligns with emerging publication standards. No human subject data is involved.

### 6. Scope & Referencing
**Rating: 5 (Excellent)**

The paper fits perfectly within the scope of *IEEE TAES*, bridging the gap between aerospace engineering (orbital dynamics, constellation ops) and electronic systems (networking, protocol design). The references are comprehensive, covering historical foundations (O'Neill, Reynolds), standard texts (Wertz/SMAD), and recent mega-constellation literature (Handley, Del Portillo). The inclusion of CCSDS standards (Space Packet Protocol, Proximity-1) grounds the work in reality.

---

## Major Issues

1.  **MAC Layer Abstraction vs. TDMA Feasibility:**
    In Section IV.A, the derivation of $\gamma = 0.949$ (conservatively 0.85) relies on a guard time of 4.7ms. The text states this accounts for propagation uncertainty and turnaround. However, for a distributed swarm without a central clock reference (GNSS-denied), clock drift between synchronization beacons could be significant. If the "Sync Beacon" is lost (as discussed in the GE section), the system reverts to Slotted ALOHA ($\gamma \approx 0.36$). The paper argues the system survives in "exception-only" mode.
    *   *Critique:* The transition between TDMA and ALOHA is binary in the model. In reality, there is a degradation phase where guard times are violated before sync is declared lost. The paper should briefly address the sensitivity of $\gamma$ to clock drift *before* the fallback to ALOHA triggers.

2.  **Coordinator Ingress vs. Egress Asymmetry:**
    Section IV.A discusses the half-duplex constraint. It states ingress takes ~9.18s of the 10s cycle, leaving ~0.8s for egress. It then claims "Total egress: ~200ms." This assumes *broadcast* commands (Type 1).
    *   *Critique:* If the workload shifts even slightly toward unicast (Type 2) or if there are many ARQ NACKs to send back to nodes, the 0.8s egress window will vanish. The paper admits unicast requires 22 cycles. This creates a potential deadlock where the coordinator cannot acknowledge reports because it is busy listening. The paper needs to explicitly state that *acknowledgments* (if used) must fit in that 0.8s window, or clarify that the protocol uses implicit ACKs (e.g., via the next summary).

---

## Minor Issues

1.  **Abstract Density:** The abstract is numerically very dense. Consider moving the specific "22-cycle scheduling" detail to the body to improve flow.
2.  **Table II Footnote:** The footnote regarding "AoI depends on $p_{exc}$... not $C_{node}$" is slightly misleading. While analytically true, if $C_{node}$ is too low, queueing delays increase, which *does* increase AoI. Clarify that this holds only when the link is not saturated.
3.  **Section III.B.2 (Coordinator Failure):** The text mentions "Seed handoff... ~16s at 1 kbps." Is this 1 kbps the *node* budget or the *coordinator* link? If the new coordinator is just a regular node promoted, does it have the high-gain antenna/power to sustain the 21-25 kbps ingress immediately? Clarify if "coordinator mode" implies hardware switching or just logical role switching.
4.  **Fig. 5 (AoI):** The y-axis scale is not specified in the caption (presumably seconds).
5.  **Eq. 10 (Guard Time):** The derivation assumes 500km cluster diameter. For "mega-constellations" at different altitudes, this might vary. A brief mention of sensitivity to range would be beneficial.
6.  **Typos/Formatting:**
    *   Section IV.A: "The zero-drop raw capacity is..." The text repeats "Intuition checks (Models A/B)" in two consecutive paragraphs. Consolidate these.
    *   Table VI: The column headers for "Delivered $\eta$" are slightly ambiguous. Does this mean "Throughput"?

---

## Overall Recommendation

**Accept with Minor Revisions**

This is a high-quality paper that offers significant contributions to the field of autonomous space systems. The analytical models are robust, and the simulation campaign is extensive. The "practitioner toolkit" approach (design equations) is highly valuable for TAES readers. The revisions requested are primarily for clarity and to slightly tighten the arguments regarding MAC-layer degradation and egress timing.

---

## Constructive Suggestions

1.  **Refine the Egress/ACK Logic:** Explicitly describe how the coordinator acknowledges the receipt of the $k_c$ reports. If ACKs are required for the ARQ mechanism (Section IV.C), they must fit in the egress window. If they don't fit, the "Inter-cycle recovery" might be delayed not by channel loss, but by lack of egress time for ACKs.
2.  **Consolidate Section IV.A:** The discussion on Models A, B, and TDMA is slightly repetitive. Merge the "Intuition checks" paragraphs to streamline the argument that 21-25 kbps is the convergence point.
3.  **Visualizing the Design Envelope:** Figure 8 (Workload Comparison) is good, but a "Design Region" plot with $N$ on the x-axis and $C_{node}$ on the y-axis, showing the feasible regions for Hierarchical vs. Mesh, would be a powerful visual summary of the paper's core finding.
4.  **Hardware Implications:** Briefly expand on the hardware implication of the "Coordinator Mode." Does every node need a 25 kbps receiver, or only specific "designated" nodes? If every node is a candidate (for robustness), this drives the hardware cost of the entire fleet. This is a key systems engineering insight worth highlighting in the discussion.