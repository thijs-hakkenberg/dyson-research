---
paper: "02-swarm-coordination-scaling"
version: "f"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-23"
recommendation: "Minor Revision"
---

Here is a comprehensive peer review of the manuscript "Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study" (Version F).

---

# Peer Review Report

**Journal:** IEEE Transactions on Aerospace and Electronic Systems
**Manuscript ID:** [Assigned by Editor]
**Title:** Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study
**Date:** October 26, 2023

## Review Criteria

### 1. Significance & Novelty
**Rating: 5 (Excellent)**

This manuscript addresses a critical and rapidly emerging gap in the aerospace engineering literature: the "intermediate regime" of constellation management between current operational scales ($10^3$ nodes) and theoretical far-future concepts ($>10^9$ nodes). While significant literature exists for small swarms (<100 agents) and traditional constellation management, the specific analysis of the $10^4$ to $10^6$ node transition is timely given the approved expansion plans of Starlink, Kuiper, and others.

The novelty lies in the systematic, quantitative comparison of three distinct topologies (Centralized, Hierarchical, Global-State Mesh) using a unified Discrete Event Simulation (DES) framework. The identification of a specific "superlinear scaling transition" between 30,000 and 60,000 nodes is a high-value contribution that provides concrete guidance for system architects. The paper moves beyond qualitative arguments to provide specific scaling laws and overhead quantifications.

### 2. Methodological Soundness
**Rating: 4 (Good)**

The methodology is generally robust. The use of Discrete Event Simulation (DES) combined with Monte Carlo analysis is the appropriate tool for this problem. The authors have done an excellent job detailing their simulation parameters (Table II), which aids reproducibility. The decomposition of overhead into "baseline telemetry" (topology-invariant) and "protocol overhead" is a smart analytical distinction that prevents the results from being dominated by fixed costs.

However, there is a slight disconnect in the physical layer modeling. The paper acknowledges that MAC-layer contention and link acquisition are abstracted away (Section V-E), yet claims the results are robust to these factors. In a dense swarm using optical ISLs, link acquisition time and topology switching costs are non-trivial. While the authors argue these are "topology-neutral," a hierarchical system relies heavily on specific bottleneck links (Cluster $\to$ Regional) remaining stable. If those specific links fail or face acquisition delays, the impact is higher than in a mesh. The review will request a more rigorous justification or sensitivity analysis regarding link stability.

### 3. Validity & Logic
**Rating: 4 (Good)**

The conclusions are logically derived from the simulation data. The U-shaped optimization curve for cluster size (Fig. 6) is intuitive and well-supported by queueing theory principles. The trade-off analysis between coordinator duty cycle, power variance, and handoff reliability is sophisticated and adds significant practical value.

One concern regarding validity is the "Optimized" curve in Fig. 9. The text states these optimizations are "modeled analytically... rather than implemented as discrete event mechanisms." This is a significant limitation. While analytical projections are useful, mixing pure DES results with analytical projections in the same graph can be misleading if not heavily caveated. The paper claims the optimizations "restore overhead to acceptable levels," but this is a prediction, not a simulation result. The review will suggest clearly distinguishing these data series visually or textually.

### 4. Clarity & Structure
**Rating: 5 (Excellent)**

The manuscript is exceptionally well-written. The structure is logical, following a standard Introduction $\to$ Related Work $\to$ Framework $\to$ Results $\to$ Discussion flow. The mathematical formulations for queueing models (Eq. 1-3) are clear. The figures are high-quality, particularly the message decomposition (Fig. 10) which effectively isolates the driver of superlinear scaling. The distinction between "local" and "global" coordination requirements is articulated clearly in Section III-B-3.

### 5. Ethical Compliance
**Rating: 5 (Excellent)**

The authors provide a specific "Acknowledgment" section detailing the use of AI tools (Claude, Gemini, GPT) for ideation, which aligns with emerging transparency standards. The data availability statement is present (though the commit hash is pending, which is standard for review). There are no apparent conflicts of interest or ethical concerns regarding the research content.

### 6. Scope & Referencing
**Rating: 5 (Excellent)**

The paper fits perfectly within the scope of *IEEE TAES*, bridging the gap between electronic systems (communications/control) and aerospace operations. The bibliography is comprehensive, covering foundational distributed systems theory (Lamport, Lynch), classical queueing theory (Kleinrock), and modern constellation literature (Starlink, Kuiper). The inclusion of recent work on Graph Neural Networks (Tolstaya et al.) and Mean Field Games demonstrates a strong command of the state-of-the-art.

---

## Major Issues

1.  **Analytical vs. Simulated Optimizations (Section IV-D):**
    The "Optimized" curve in Figure 9 is derived analytically, whereas the baseline curves are DES-generated. This is a methodological discontinuity. The paper states: *"These optimizations are modeled analytically in the simulation rather than implemented as discrete event mechanisms."*
    *   **Critique:** Analytical models often underestimate the "friction" of implementation (e.g., the signaling overhead required to *negotiate* dynamic spatial partitioning).
    *   **Requirement:** The authors must either (a) implement at least one optimization (e.g., exception-based telemetry) in the DES to validate the analytical projection, or (b) significantly modify Figure 9 and the abstract to clarify that the "restored overhead" is a theoretical projection, not a simulated result.

2.  **Link Stability and Hierarchy Fragility:**
    The paper argues that physical layer abstractions are "topology-neutral." I challenge this assumption regarding the Hierarchical topology.
    *   **Critique:** In a mesh, link failures are locally absorbed. In a fixed hierarchy, the failure of a Cluster Coordinator-to-Regional Coordinator link isolates 100 nodes. The simulation models node failure, but does it model *link* instability (e.g., pointing errors, occlusion) distinct from node death?
    *   **Requirement:** Please clarify if link intermittency (distinct from node failure) is modeled. If not, the reliability analysis for the Hierarchical topology (Fig. 5) may be overly optimistic. A discussion on how the hierarchy recovers from *link* loss (not just node loss) is needed.

---

## Minor Issues

1.  **Table I (Scalability Sensitivity):** The table lists $c=1000$ servers for a "Hyperscale data center." This seems low. Hyperscale centers have tens of thousands of cores. The point stands, but the label might be slightly inaccurate regarding modern computing scale.
2.  **Eq. 5 (Hierarchy Levels):** The text describes a four-level hierarchy, but Eq. 5 implies three aggregation steps. It is correct, but the notation $N/(k_c \cdot k_r)$ implies the ground station receives regional summaries. Please explicitly state if the Ground Station is considered "Level 0" or "Level 4" to avoid off-by-one confusion in the depth description.
3.  **Section III-E (Bandwidth):** The distinction between the 1 kbps per-node allocation and the "higher-capacity link budget" for coordinators is crucial. It is currently buried in the text. This should be highlighted in Table II or a dedicated footnote, as it is a major hardware assumption.
4.  **Figure 8 (Pareto Frontier):** The visual distinction between the 24h and 48h points is small. Ensure the axis scaling allows the reader to see the trade-off clearly.
5.  **Typos/Grammar:**
    *   Section II-A: "OneWeb employs a similar centralized paradigm... none has published evidence..." -> "none have published evidence" (plural).
    *   Section V-E: "MAC-layer contention... could increase protocol overhead... We argue they are approximately topology-neutral." -> This argument needs a citation or a stronger logical basis (see Major Issue 2).

---

## Overall Recommendation

**Minor Revision**

This is a high-quality paper that makes a significant contribution to the field of large-scale space systems. The simulation framework is robust, and the results are novel. The recommendation for "Minor Revision" is primarily to address the distinction between simulated and analytical results in the optimization section and to strengthen the justification regarding link stability assumptions. Once these points are clarified, the manuscript should be accepted for publication.

---

## Constructive Suggestions

1.  **Hybrid Simulation Validation:** To address Major Issue #1 without rewriting the whole code base, run a small-scale DES ($N=10^4$) with "Exception-Based Telemetry" implemented simply (e.g., probability of transmission $p=0.01$). Compare this single data point to your analytical projection. If they align, you can justify the analytical curve for the larger scales.
2.  **Sensitivity Analysis for Link Failure:** Add a paragraph in Section V discussing "Link Fragility." Even if you cannot simulate it, acknowledge that hierarchical topologies are logically more brittle to specific link failures than meshes, and suggest "multi-parent" hierarchies (where a cluster reports to two regionals) as a future mitigation.
3.  **Clarify "Global State":** In the introduction, explicitly define what "Global State" means in this context early on. You do this well in Section III-B-3, but a brief sentence in the Intro (e.g., "Global State implies every node possesses the orbital elements of every other node") would help set the stage for why the Mesh baseline fails so hard.
4.  **Hardware Heterogeneity Impact:** You mention heterogeneous hardware as an optimization. It would be valuable to add a few sentences on the *logistics* of this. Does this require mixed launches? Or software-defined radios where any node can boost power to become a coordinator? The latter is much more robust for constellation replenishment.