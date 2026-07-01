---
paper: "02-swarm-coordination-scaling"
version: "h"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-23"
recommendation: "Accept"
---

Here is the peer review for the manuscript "Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study" (Version H).

***

# Peer Review Report
**Journal:** IEEE Transactions on Aerospace and Electronic Systems
**Manuscript ID:** [Pending]
**Title:** Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study
**Version:** H

## Review Criteria

### 1. Significance & Novelty
**Rating: 5 (Excellent)**

This paper addresses a critical and rapidly approaching problem in aerospace engineering: the scalability of coordination architectures for mega-constellations and future autonomous swarms. While existing literature covers small-scale swarm robotics ($N < 1000$) or current constellation management ($N < 10,000$), there is a significant gap in the intermediate regime ($10^4$ to $10^6$ nodes). The authors correctly identify that linear extrapolation of current centralized methods fails at these scales due to spectrum and latency constraints, not just processing power.

The novelty lies in the rigorous comparison of three distinct topologies using a consistent Discrete Event Simulation (DES) framework across three orders of magnitude. The identification of the "slope change" in overhead near 45,000 nodes—driven by inter-cluster traffic—is a specific, actionable insight that advances the theoretical understanding of hierarchical control in orbital mechanics. The practical parameterization of coordinator bandwidth and duty cycles makes this highly relevant for near-term system architects (e.g., Starlink, Kuiper).

### 2. Methodological Soundness
**Rating: 5 (Excellent)**

The methodology is robust and demonstrates a high degree of rigor. The transition from analytical formulas to direct DES message byte counting (a correction from previous versions mentioned in the text) significantly strengthens the validity of the results. The use of Monte Carlo methods with bootstrap confidence intervals is appropriate for capturing the stochastic nature of node failures and message timing.

The queueing theory models ($M/D/1$ and $M/D/c$) are correctly applied as reference baselines. The authors are careful to define their metrics precisely (Section III-H), particularly the distinction between baseline telemetry and protocol overhead. The addition of a Bernoulli link availability model with retransmission (ARQ) addresses a common weakness in high-level swarm simulations, providing a more realistic assessment of robustness. The validation of the exception-based telemetry optimization at multiple scales ($10^4, 10^5, 5 \times 10^5$) adds significant weight to the proposed optimizations.

### 3. Validity & Logic
**Rating: 4 (Good)**

The conclusions are generally well-supported by the data. The authors frankly acknowledge the limitations of their baselines, noting that the centralized model is a "processing bound" and the global-state mesh is an "upper bound." This intellectual honesty prevents straw-man comparisons. The analysis of the "U-shaped" optimization for cluster size ($k_c \approx 100$) is logical and well-explained by the trade-off between inter-cluster traffic and intra-cluster latency.

However, there is a minor logical tension regarding the "Sectorized Mesh" discussion. The authors admit this is a "promising intermediate architecture" but do not simulate it. While they justify this by framing the study as "Hierarchical vs. Bounds," the sectorized mesh is likely the strongest *real-world* competitor to their proposed hierarchy. Its absence doesn't invalidate the hierarchical results, but it leaves a small gap in the comparative logic. Additionally, the assumption that coordinators can simply be assigned higher bandwidth ($C_{coord}$) is physically nontrivial; while the parameterization in Section IV-G is excellent, the physical realization (e.g., larger antennas, higher power) implies a heterogeneity that contradicts the "homogeneous rotating coordinator" assumption used in the power analysis.

### 4. Clarity & Structure
**Rating: 5 (Excellent)**

The manuscript is exceptionally well-written. The structure is logical, moving from problem definition to simulation framework, results, and discussion. The distinction between "Version A-G" artifacts and "Version H" corrections is transparent and helpful for the review process, though these meta-comments should be smoothed out for final publication.

The figures are likely effective (based on descriptions), particularly the "scaling trajectory" (Fig. 8) and "latency distribution" (Fig. 3). The tables are dense but informative. The definitions in Section III-H are crucial for clarity and are placed well. The abstract is comprehensive and quantitative.

### 5. Ethical Compliance
**Rating: 5 (Excellent)**

The authors provide a specific "Acknowledgment" section detailing the use of AI tools (Claude, Gemini, GPT) for ideation and code generation, which aligns with emerging best practices for transparency. There are no apparent conflicts of interest or ethical concerns regarding the research subject matter.

### 6. Scope & Referencing
**Rating: 4 (Good)**

The paper fits perfectly within the scope of *IEEE TAES*, bridging the gap between electronic systems (communications) and aerospace systems (orbital mechanics/constellations). The references are a good mix of classical distributed systems theory (Lamport, Lynch), standard astrodynamics texts (Wertz), and recent literature on mega-constellations and swarm robotics.

One minor gap is the lack of references to specific Delay Tolerant Networking (DTN) routing protocols beyond the general architecture (Cerf). More specific citation of Contact Graph Routing (CGR) literature would strengthen the discussion on link intermittency, as CGR is the standard solution for this problem in space networks.

---

## Major Issues

*None.* The manuscript is technically sound. The authors have proactively addressed potential major issues (such as the lack of link error modeling in previous versions) by introducing the Bernoulli link availability and retransmission analysis in Section IV-F.

## Minor Issues

1.  **Coordinator Heterogeneity vs. Rotation:** In Section IV-G, the paper establishes that a coordinator needs $\approx 25\times$ the bandwidth of a normal node. However, Section IV-H discusses "rotating coordinators" to distribute power load. If the coordinator requires specific hardware (high-gain antennas or distinct radio front-ends) to support 25 kbps inbound vs 1 kbps, can any node truly serve as a coordinator? The paper should clarify if the "enhanced bandwidth" is a function of dynamic spectrum allocation (software-defined) or physical hardware. If it is hardware, the rotation strategy is invalid. If it is spectrum allocation, this should be explicitly stated as a TDMA/FDMA assumption.
2.  **Sectorized Mesh Justification:** In Section V-C, the authors describe the Sectorized Mesh as a "natural extension" that bridges the gap. It would be beneficial to explicitly state *why* it was not simulated if it represents a more realistic competitor than the Global-State Mesh. A simple sentence stating it was out of scope due to the complexity of implementing neighbor discovery in the DES would suffice.
3.  **Meta-Commentary Removal:** The text contains several references to "Versions A-G" and "Version H" (e.g., Section IV-D, Section IV-F.1). While helpful for peer review, these should be removed or rephrased as "Previous analytical models..." for the final archival version.
4.  **Figure 8 Caption:** The caption for Figure 8 mentions "unvalidated dynamic partitioning." This phrasing is slightly confusing; it should perhaps read "analytically projected dynamic partitioning (not yet validated by DES)."

## Overall Recommendation
**Accept**

This is a high-quality manuscript that makes a significant contribution to the literature on large-scale space systems. The simulation is rigorous, the metrics are well-defined, and the conclusions are nuanced. The authors have successfully bounded the design space for future mega-constellation architectures.

## Constructive Suggestions

1.  **Clarify Coordinator Hardware Assumptions:** Add a sentence in Section IV-H or IV-G clarifying that the $25\times$ bandwidth requirement is assumed to be achieved via dynamic resource allocation (e.g., assigning more time slots or frequency channels to the current coordinator) rather than static hardware differences, to preserve the validity of the rotation logic.
2.  **Expand on CGR:** Briefly mention Contact Graph Routing (CGR) in the Related Work or Discussion as the standard implementation for the "store-and-forward" behavior mentioned in the context of DTN.
3.  **Refine "Slope Change" Terminology:** In the Abstract and Conclusion, the phrase "change in the linear slope rather than a transition to superlinear complexity" is excellent. Ensure this distinction is highlighted in the Introduction as well, as many readers might assume "scaling limit" implies exponential or quadratic growth.
4.  **Future Work Priority:** In Section V-D, explicitly prioritize the "Sectorized Mesh" simulation as the immediate next step, acknowledging that it likely represents the true "competitor" to the hierarchical model.