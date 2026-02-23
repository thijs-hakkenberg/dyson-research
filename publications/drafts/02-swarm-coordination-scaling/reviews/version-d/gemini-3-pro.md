---
paper: "02-swarm-coordination-scaling"
version: "d"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-23"
recommendation: "Minor Revision"
---

Here is a rigorous peer review of the manuscript "Scaling Hierarchical Coordination for Million-Unit Space Swarms: Discrete Event Simulation and Architectural Analysis," prepared for *IEEE Transactions on Aerospace and Electronic Systems*.

***

# Peer Review Report

**Manuscript Title:** Scaling Hierarchical Coordination for Million-Unit Space Swarms: Discrete Event Simulation and Architectural Analysis
**Version:** D
**Target Journal:** IEEE Transactions on Aerospace and Electronic Systems

## Review Criteria

### 1. Significance & Novelty
**Rating: 5 (Excellent)**

This paper addresses a critical and timely gap in the aerospace engineering literature: the "intermediate regime" of coordination between current constellations ($10^3$ nodes) and theoretical far-future swarms ($>10^9$ nodes). While swarm robotics literature handles small scales and mean-field game theory handles infinite scales, the specific engineering challenges of $10^5–10^6$ nodes—relevant to near-term mega-constellations like Starlink and Kuiper—are under-represented.

The novelty lies in the systematic, comparative Discrete Event Simulation (DES) across three orders of magnitude. The identification of a "superlinear scaling regime" near 50,000 nodes is a significant contribution that provides a concrete target for system architects. The analysis of coordinator duty cycles (24-48 hours) offers practical operational guidance that is currently missing from abstract graph-theoretic studies. This work is highly relevant to the *IEEE TAES* readership.

### 2. Methodological Soundness
**Rating: 4 (Good)**

The methodology is generally robust. The use of DES combined with Monte Carlo analysis is the appropriate tool for this problem. The queueing models ($M/D/1$ and $M/D/c$) are standard and correctly applied. The authors are careful to distinguish between processing bottlenecks (solvable via parallelization) and fundamental physical constraints (spectrum, latency), which adds credibility to the analysis.

However, there is a slight disconnect in the mesh topology modeling. The assumption that *global* state convergence is required for *all* nodes in a mesh is a strong worst-case bound. While the authors justify this via the need for global orbit-raising coordination, in practice, a sectorized mesh (which they mention but do not simulate) is the standard engineering solution. The paper would be stronger if it acknowledged that the $O(N^2)$ result for mesh is a consequence of the specific "global awareness" requirement rather than an inherent failure of mesh topologies in general. Additionally, the specific implementation of the "superlinear" scaling detection relies on only five data points; while the trend is clear, the precise inflection point of 50,000 nodes warrants more granular simulation data.

### 3. Validity & Logic
**Rating: 4 (Good)**

The conclusions logically follow from the simulation results. The trade-off analysis between centralized, hierarchical, and mesh architectures is nuanced and avoids declaring a single "winner" without context. The decomposition of bandwidth into baseline telemetry vs. protocol overhead is a crucial distinction that prevents the results from being skewed by fixed costs.

The logic regarding the "Shepherd/Flock" concept (Section V-B) is the weakest part of the paper. While the authors are transparent that this was an AI-assisted ideation exercise, its inclusion as a "result" or "discussion" point feels premature compared to the rigorous DES data presented elsewhere. It is a valid concept, but it relies on generative design rather than the engineering validation applied to the rest of the paper.

### 4. Clarity & Structure
**Rating: 5 (Excellent)**

The manuscript is exceptionally well-written. The structure is logical, moving from theoretical framing to simulation design, results, and discussion. The mathematical notation is consistent. Figures are well-referenced and described. The distinction between "local" and "global" coordination requirements is articulated clearly in Section III-B-3. The abstract accurately summarizes the findings.

### 5. Ethical Compliance
**Rating: 5 (Excellent)**

The authors provide a specific and transparent disclosure regarding the use of AI (Claude, Gemini, GPT) for the architectural exploration section. This aligns with emerging best practices for AI disclosure in academic publishing. The conflict of interest statement and data availability sections are present. The "Project Dyson" affiliation appears to be a placeholder for blind review, which is appropriate.

### 6. Scope & Referencing
**Rating: 4 (Good)**

The paper fits perfectly within the scope of *IEEE TAES*. The references are a good mix of classical distributed systems theory (Lamport, Lynch), standard astrodynamics texts (Wertz), and recent literature on GNNs and mega-constellations.

One minor gap is the lack of reference to Delay/Disruption Tolerant Networking (DTN) protocols (RFC 5050/BPv7). Given the discussion of link availability and occlusion, DTN is a relevant standard for space internetworking that should be acknowledged in the Related Work or Discussion sections.

---

## Major Issues

1.  **Mesh Topology Parameterization (Section III-B-3):** The paper asserts that mesh topology incurs $O(N^2)$ overhead because "each node must eventually receive trajectory updates from all $O(N)$ nodes." This is a worst-case assumption. In reality, collision probability decreases rapidly with orbital separation. A "sectorized" mesh (which the authors mention as a future investigation) is the standard approach for large networks. By simulating only the "global gossip" version, the paper sets up a strawman argument against mesh topologies.
    *   *Requirement:* The authors should explicitly label the simulated mesh as "Global-State Mesh" throughout the results to differentiate it from "Sectorized Mesh." A paragraph should be added to the discussion estimating how a sectorized approach might shift the crossover point with hierarchical topologies.

2.  **Granularity of Superlinear Regime (Section IV-D):** The claim of a superlinear scaling onset "near 50,000 nodes" is based on a data set with large gaps ($10^4$ to $5 \times 10^4$ to $10^5$). The curve fitting here is heavily dependent on the specific reporting rate $r$.
    *   *Requirement:* The authors should soften the claim about the specific number (50,000) or acknowledge that this threshold is highly sensitive to the reporting rate parameter $r$. It is not a universal constant of the architecture but a function of the specific link capacity and message frequency chosen.

---

## Minor Issues

1.  **Equation 5 (Hierarchical Messages):** The equation $M_{\text{total}} = N + N/k_c + N/(k_c \cdot k_r)$ describes the *upward* flow of reporting. The text mentions that downward commands "approximately double" this. It would be more precise to include a factor $\beta$ (command ratio) in the equation or explicitly state that this equation represents telemetry load only.
2.  **Table I (Simulation Parameters):** The "Coordinator capacity" is listed as 1,000 msg/s. Is this CPU-bound or I/O-bound? For a space-hardened processor (often generations behind terrestrial CPUs), 1,000 complex trajectory processing messages per second might be optimistic. A brief justification of this number based on representative flight hardware (e.g., LEON3/4 or ARM Cortex-A53 class) would be beneficial.
3.  **Section V-B (AI-Assisted Design):** The phrase "The following reports an exploratory ideation exercise, not a validated design methodology" is honest, but the section consumes considerable space. It might be better placed as a subsection of Future Work rather than a main Discussion point, to avoid distracting from the validated simulation results.
4.  **Reference Format:** Reference [20] is a magazine article; ensure this meets IEEE citation standards for peer-reviewed journals. Reference [31] is a "manuscript in preparation"; if possible, cite a preprint or remove if not publicly available.

---

## Overall Recommendation

**Minor Revision**

The paper represents a high-quality contribution to the field of space systems engineering. The simulation framework is sound, and the results regarding hierarchical scaling and duty cycles are valuable. The revisions requested are primarily regarding the framing of the mesh topology results (to avoid overstating the inefficiency of mesh in general versus the specific global-state variant simulated) and minor clarifications on parameter sensitivity. The paper does not require new simulations to be publishable, but the interpretation of the existing data needs slight refinement.

---

## Constructive Suggestions

1.  **Refine the Mesh Terminology:** Rename "Mesh Topology" to "Global-State Mesh" in figures and tables. This clarifies that the $O(N^2)$ scaling is a cost of the *requirement* (global awareness), not the *topology* itself. This protects the paper from criticism by mesh networking experts.
2.  **Sensitivity Analysis for the 50k Threshold:** In Section IV-D, add a brief discussion or a small analytical derivation showing how the 50,000-node threshold shifts if the link capacity increases (e.g., to 10 kbps) or reporting rate decreases. This generalizes the finding beyond the specific simulation parameters.
3.  **DTN Integration:** Add a sentence or two in the Related Work section acknowledging CCSDS Bundle Protocol (DTN) as a relevant standard for the transport layer, clarifying that this paper focuses on the application-layer coordination logic rather than the store-and-forward transport mechanics.
4.  **Hardware Context:** In the discussion of coordinator power (Section IV-E), mention specific examples of space-grade processors (e.g., "equivalent to a high-utilization RAD750 or moderate-utilization Snapdragon flight board") to ground the 15-20W power estimate in current hardware realities.