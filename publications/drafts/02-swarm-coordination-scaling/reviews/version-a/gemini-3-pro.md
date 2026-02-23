---
paper: "02-swarm-coordination-scaling"
version: "a"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-23"
recommendation: "Major Revision"
---

# Peer Review: IEEE Transactions on Aerospace and Electronic Systems

**Manuscript ID:** [Assigned by Editor]
**Title:** Scaling Hierarchical Coordination for Billion-Unit Space Swarms: Discrete Event Simulation and Architectural Validation
**Version:** A

## Review Criteria

### 1. Significance & Novelty
**Rating: 4**

The manuscript addresses a highly relevant and timely topic. With the rapid deployment of mega-constellations (Starlink, Kuiper) and future concepts for large-scale space infrastructure, the transition from ground-based centralized control to autonomous distributed coordination is a critical area of research. The paper’s focus on the "intermediate regime" of $10^4$ to $10^6$ nodes fills a distinct gap between existing constellation management literature (up to $\sim10^4$) and theoretical swarm robotics literature (often abstract or small-scale). The identification of the 50,000-node inflection point is a valuable contribution to the systems engineering of future constellations.

### 2. Methodological Soundness
**Rating: 2**

The Discrete Event Simulation (DES) framework described in Section 3 appears competent for a high-level architectural trade study. The use of M/D/1 queueing models for the centralized bottleneck is appropriate. However, there are two significant methodological flaws.

First, the modeling of the Mesh topology (Section 3.2.3) assumes a requirement for global state convergence ($O(N^2)$ complexity). In practical swarm robotics, mesh topologies rarely require every node to know the state of every other node; they typically rely on local neighbor interactions ($O(k)$ where $k$ is neighbor count). This assumption creates a "strawman" argument that artificially penalizes the mesh topology.

Second, and most critically, Section 5 ("Multi-Model Architectural Validation") is methodologically invalid. Large Language Models (LLMs) are probabilistic text generators trained on existing literature. While they can synthesize consensus from training data, they cannot perform independent engineering validation or physics-based reasoning. Citing LLM consensus as "independent validation" of a simulation result is scientifically unsound. This section conflates *generative design assistance* with *verification and validation (V&V)*.

### 3. Validity & Logic
**Rating: 3**

The conclusions regarding the scalability of hierarchical systems (Section 4) follow logically from the simulation parameters and are supported by the data presented. The analysis of coordinator duty cycles and the power/availability trade-off is well-reasoned and provides practical engineering insights.

However, the validity is undermined by the title-content discrepancy (see Major Issues) and the reliance on AI deliberation as a proof mechanism. The logic that "three models agreed, therefore the architecture is valid" is circular; the models likely agreed because they were trained on similar corpus data that favors hierarchical structures for large systems (e.g., cellular networks, DNS).

### 4. Clarity & Structure
**Rating: 4**

The paper is generally well-written, organized, and easy to follow. The progression from problem statement to simulation setup, results, and discussion is logical. Figures 1 through 7 are high-quality and clearly illustrate the data. The mathematical notation in Section 3 is standard and clear.

### 5. Ethical Compliance
**Rating: 3**

The authors disclose the use of AI in Section 5 and the Acknowledgments, which meets transparency requirements. However, the *application* of the AI raises epistemic and rigorousness concerns rather than purely ethical ones. Additionally, the authorship is listed as "Project Dyson Research Team." IEEE TAES typically requires individual human authors to be listed for accountability, even if representing a consortium.

### 6. Scope & Referencing
**Rating: 4**

The scope is well-suited for *IEEE TAES*, fitting squarely within the "Aerospace Systems" and "Command and Control" interest areas. The references are a good mix of classical space systems engineering (SMAD), distributed computing theory (Lynch), and recent swarm robotics work.

---

## Major Issues

1.  **Title vs. Content Discrepancy:** The title claims "Billion-Unit Space Swarms" ($10^9$), but the abstract and simulation results only cover up to $10^6$ (one million) nodes. This is a three-order-of-magnitude error. The title must be corrected to reflect the actual scope of the study ($10^6$).
2.  **Invalid "AI Validation" Methodology (Section 5):** The premise that LLM consensus constitutes "independent validation" is rejected. LLMs do not possess the capability to validate engineering constraints or physics simulations; they output text based on statistical likelihood. If the authors wish to retain the AI component, it must be reframed as "AI-Assisted Design Exploration" or "Generative Architectural Search." It cannot be presented as validation of the DES results. The current framing suggests a fundamental misunderstanding of V&V principles in aerospace engineering.
3.  **Mesh Topology "Strawman":** The simulation forces the mesh topology to perform global state propagation ($O(N^2)$). This is not how scalable mesh swarms operate (e.g., Reynolds flocking is local). The authors must either (a) justify why global state knowledge is required for this specific mission profile, or (b) include a "Local Mesh" topology in the simulation that scales linearly, likely showing it fails due to lack of global coordination rather than bandwidth saturation.
4.  **Authorship:** "Project Dyson Research Team" is likely insufficient for final publication. Specific authors must be identified to assume responsibility for the content.

## Minor Issues

1.  **Abstract:** "7,000 operational satellites... 12,000 approved." Please ensure these numbers are dated or cited, as they change rapidly.
2.  **Section 3.2.2 (Hierarchical):** The paper mentions "optical inter-satellite links." It should clarify if the simulation accounts for Line-of-Sight (LOS) occlusion by the Earth, which is a major constraint for LEO constellations, or if an ideal connectivity graph is assumed.
3.  **Section 4.4 (Inflection Point):** The term "exception-based telemetry" is used. In control theory, this is often called "event-triggered control." It would be beneficial to reference standard literature on event-triggered control to ground this optimization in established theory.
4.  **Figure 5:** The y-axis label should be explicitly defined in the caption (presumably percentage of total fleet uptime).
5.  **References:** Reference [30] cites a "manuscript in preparation." If this paper relies on the methodology of [30], that methodology needs to be summarized more fully here, as the citation is not accessible to readers.

## Overall Recommendation

**Major Revision**

**Justification:**
The core simulation work (Sections 1-4) offers valuable insights into the scalability of constellation management, particularly the analysis of the hierarchical inflection point and duty cycles. However, the manuscript cannot be published in its current form due to the misleading title ($10^9$ vs $10^6$) and the scientifically invalid framing of Section 5 (AI Validation). The authors must re-scope the title, re-frame or remove the AI section to align with rigorous engineering standards, and address the limitations of their Mesh topology model.

## Constructing Suggestions

1.  **Reframe Section 5:** Rename this section "Generative Architectural Search" or "AI-Assisted Concept Generation." Move it *before* the simulation results to show how the AI suggested the architecture, which was *then* validated by the DES. This reverses the logic flow to be scientifically sound: AI proposes, Physics/Simulation validates.
2.  **Refine the Mesh Model:** Introduce a "Local Mesh" baseline in the simulation that only gossips with $k$ neighbors. You will likely find that while bandwidth is fine, latency for global commands (e.g., "Orbit Raise") becomes the bottleneck. This would be a fairer and more nuanced comparison than the current bandwidth-saturation argument.
3.  **Expand on "Dynamic Spatial Partitioning":** This is a strong concept. Add a paragraph discussing the specific challenges of this in LEO, specifically the high relative velocities at polar crossings (if applicable) or the handover frequency required.
4.  **Correct the Title:** Change "Billion-Unit" to "Million-Unit" or "Mega-Constellation Scale."
5.  **Clarify Assumptions:** Explicitly state in Section 3 that the simulation assumes ideal Line-of-Sight or simplified orbital mechanics, acknowledging that full orbital propagation might introduce further constraints.