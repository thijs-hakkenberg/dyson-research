---
paper: "02-swarm-coordination-scaling"
version: "o"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-24"
recommendation: "Minor Revision"
---

Here is a rigorous peer review of the manuscript "Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study" (Version O), prepared for *IEEE Transactions on Aerospace and Electronic Systems*.

---

# Peer Review Report

**Manuscript Title:** Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study
**Target Journal:** IEEE Transactions on Aerospace and Electronic Systems
**Version:** O

## Review Criteria

### 1. Significance & Novelty
**Rating: 4 (Good)**

The manuscript addresses a critical and timely gap in the aerospace literature: the "intermediate regime" of coordination scaling between current constellations ($10^3$ nodes) and future mega-structures ($10^6$ nodes). While swarm robotics literature covers small scales and constellation management covers current scales, the specific quantitative analysis of hierarchical architectures at $10^5$ nodes is a valuable contribution. The paper effectively challenges the scalability of centralized ground control not just through processing limits (which it rightly notes are solvable via parallelization) but through physical constraints like spectrum scarcity and propagation latency.

The novelty lies less in the proposal of hierarchical control (a well-known concept in distributed systems) and more in the specific, rigorous parameterization for the orbital domain. The quantification of the "protocol coefficient" ($\eta \approx 20.66\%$) and the stress-testing of coordinator bandwidth provide actionable engineering data for system architects.

### 2. Methodological Soundness
**Rating: 4 (Good)**

The Discrete Event Simulation (DES) approach is appropriate for this problem. The authors are commendable for using a "full-participation" model rather than statistical extrapolation for the primary results, and for running 30 Monte Carlo replications to bound variance. The distinction between the message-passing abstraction and physical layer reality is clearly drawn in Table III, which is crucial for validity.

However, there is a tension in the methodology regarding the "Coordinator Bandwidth Stress Test" (Section IV-G). The paper acknowledges that a TDMA model is required for realistic high-utilization links but proceeds with a random-phase arrival model that induces artificial drops. While the authors transparently calculate the theoretical TDMA limit ($\sim 59$ kbps), the reliance on a random-phase model for the stress test slightly weakens the fidelity of the "zero-drop" threshold results. Additionally, the assumption of uncorrelated exponential failures is a standard simplification but potentially optimistic for space systems where common-mode failures (e.g., solar storms) are relevant.

### 3. Validity & Logic
**Rating: 5 (Excellent)**

The logic driving the conclusions is robust. The authors are careful to frame their baselines (Single-Server Centralized and Global-State Mesh) as "intentional bounds" rather than straw men, preventing the common pitfall of comparing an optimized proposed system against artificially crippled alternatives. The derivation of the $O(1)$ overhead scaling is mathematically sound and empirically validated by the DES data.

The analysis of the duty cycle trade-off (Section IV-C) is particularly strong, identifying the Pareto frontier between power variance and availability. The distinction between "delivered overhead" and "offered load" in the link availability analysis (Section IV-F) demonstrates a sophisticated understanding of network engineering requirements. The conclusions regarding the necessity of either heterogeneous hardware or TDMA slot aggregation are well-supported by the data.

### 4. Clarity & Structure
**Rating: 5 (Excellent)**

The manuscript is exceptionally well-written. The structure is logical, moving from problem definition to model description, results, and discussion. The use of tables to summarize parameters (Table II) and abstraction scope (Table III) greatly aids reproducibility.

The definitions of metrics are precise, and the distinction between baseline telemetry (topology-invariant) and protocol overhead is maintained consistently throughout. Figures are well-referenced and clearly captioned. The explicit "Traffic Accounting" section (Table V) is a best practice that many simulation papers lack, ensuring the reader knows exactly what is being counted in the overhead metric.

### 5. Ethical Compliance
**Rating: 5 (Excellent)**

The authors provide a transparent disclosure regarding the use of AI tools for ideation in the Acknowledgments section, citing a companion methodology paper. This aligns with emerging best practices for AI disclosure in academic publishing. There are no apparent conflicts of interest or ethical concerns regarding the research content.

### 6. Scope & Referencing
**Rating: 4 (Good)**

The paper fits squarely within the scope of *IEEE TAES*, specifically the areas of space systems and command/control architectures. The references are generally good, covering standard texts (Wertz, Kleinrock), classical distributed systems (Lamport, Lynch), and recent constellation developments (Starlink, Kuiper).

However, the discussion on "Sectorized Mesh" (Section V-C) relies heavily on analytical argumentation. While the authors rightly identify this as future work, referencing existing literature on geometric routing or region-based gossip in sensor networks (beyond just the general gossip references) would strengthen the claim that sectorized mesh is the "practical decentralized alternative."

---

## Major Issues

1.  **Coordinator Bandwidth vs. MAC Layer Reality:**
    In Section IV-G, the paper derives a "zero-drop" requirement of 50 kbps based on random-phase arrivals, then analytically adjusts this to ~59 kbps for TDMA overhead. This is a critical interface between the simulation and reality. The paper states that "MAC-layer scheduling... is not modeled."
    *   *Critique:* At utilizations near 50%, the specific MAC protocol (Slotted ALOHA vs. TDMA) dictates performance entirely. A random-phase model approximates an unslotted or pure ALOHA channel, which is unstable above 18% utilization. If the system is intended to be TDMA, the random-phase simulation is overly pessimistic regarding collisions but optimistic regarding synchronization overhead.
    *   *Requirement:* The authors should explicitly clarify if the "random phase" model implies a Slotted ALOHA assumption or simply an uncoordinated arrival process. If the latter, the 50 kbps requirement is likely an artifact of the simulation's collision logic rather than a physical limit. A paragraph clarifying the specific collision logic used in the DES (e.g., "do overlapping messages destructively interfere, or is it a buffer fill model?") is necessary to interpret the 50 kbps figure correctly.

2.  **Latency Extrapolation in Figure 3:**
    Figure 3 includes a curve for $10^6$ nodes labeled as "Analytical extrapolation."
    *   *Critique:* The rest of the paper prides itself on "full-participation DES" results up to $10^5$. Mixing analytical extrapolation into a primary results figure, even with a disclaimer, risks misleading readers who may glance at the plot. The behavior of queueing systems at $10^6$ could diverge from linear extrapolation due to second-order effects not captured in the simple analytical model.
    *   *Requirement:* I recommend removing the $10^6$ curve from Figure 3 or visually distinguishing it much more aggressively (e.g., different color, dotted line, and explicit legend entry "Extrapolated (Not Simulated)").

---

## Minor Issues

1.  **Table I (M/D/c Sensitivity):** The table lists "Hyperscale data center" for $c=1000$. While illustrative, this terminology is slightly vague in a space systems context. Perhaps "Cloud-based Ground Segment" is more appropriate.
2.  **Section IV-E (Scaling Behavior):** The text states "SD < 0.001%". While this demonstrates the deterministic nature of the protocol, it might imply to a casual reader that the *system* has no variance. It would be helpful to reiterate here that this low variance is due to the fixed message sizes and deterministic routing, and that real-world variance (channel fading) is treated separately in Section IV-F.
3.  **Equation 5 (Hierarchy):** The equation $M_{\text{total}} = N + N/k_c + \dots$ describes the message count. It would be helpful to explicitly state that this is *per reporting cycle*.
4.  **Section V-C (Sectorized Mesh):** The claim that sectorized mesh overhead scales as $O(N^{1.5})$ assumes a specific shell density growth. It would be precise to clarify that this assumes constant altitude/shell thickness as $N$ grows (constant density implies surface area growth, but here the area is fixed, so density increases).
5.  **Reference Format:** Reference [1] and [3] are non-archival websites. While necessary for current constellation data, ensure the access dates are recent and consider if there are white papers or FCC filings that could be cited instead for greater permanence.

---

## Overall Recommendation

**Minor Revision**

The manuscript represents a high-quality simulation study with significant relevance to the future of space operations. The methodology is generally rigorous, and the writing is excellent. The issues identified regarding the MAC layer abstraction and the visual representation of extrapolated data can be addressed with textual clarifications and minor figure edits without requiring new simulation runs.

---

## Constructive Suggestions

1.  **Clarify the Buffer Model:** In Section IV-G, explicitly describe the "drop" mechanism. Is it a buffer overflow (tail drop) or a channel collision (interference)? The text mentions "ingress rate" and "byte budget," implying a buffer model, but the discussion of "random phase" implies collisions. Clarifying this will solidify the bandwidth conclusions.
2.  **Strengthen the "Sectorized Mesh" Argument:** Since this is the true competitor to the proposed architecture, add a few sentences in the Discussion citing specific algorithms (e.g., geometric routing or localized gossip protocols) that would enable the sectorized approach, giving the reader a concrete path for future comparison.
3.  **Visual Distinction for Extrapolation:** Modify Figure 3 to make the $10^6$ node line dashed or dotted to clearly separate simulated data from analytical projection.
4.  **Link Budget Context:** In the conclusion, explicitly link the "59 kbps" requirement to standard CubeSat/SmallSat radio hardware capabilities (e.g., "This is well within the capabilities of S-band or X-band inter-satellite links..."). This grounds the theoretical result in hardware reality.