---
paper: "02-swarm-coordination-scaling"
version: "br"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-27"
recommendation: "Minor Revision"
---

## Peer Review: IEEE Transactions on Aerospace and Electronic Systems

**Manuscript ID:** [Version BR]
**Title:** Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms
**Authors:** Project Dyson Research Team

---

### 1. Significance & Novelty
**Rating: 4 (Good)**

The manuscript addresses a critical and timely challenge in aerospace engineering: the scalability of command and control (C2) architectures for mega-constellations and large-scale swarms ($10^3$--$10^5$ nodes). As commercial and defense sectors move toward proliferated LEO architectures, the shift from centralized ground-in-the-loop control to autonomous, hierarchical on-orbit coordination is inevitable.

The primary contribution—a set of closed-form "design equations" validated by simulation—is highly valuable for systems engineers. The distinction between "byte budget," "MAC efficiency," and "airtime scheduling" (feasibility layers) provides a robust framework for sizing inter-satellite links (ISLs). While hierarchical control is not new in distributed systems theory, its rigorous application to the specific constraints of space operations (long propagation delays, orbital dynamics, specific packet standards like CCSDS) constitutes a significant contribution to the TAES community.

### 2. Methodological Soundness
**Rating: 4 (Good)**

The authors employ a multi-fidelity approach: analytical derivation, cycle-aggregated Discrete Event Simulation (DES), and a specific slot-level TDMA simulator. This triangulation strengthens the results significantly.
*   **Strengths:** The use of the Gilbert-Elliott (GE) model for correlated losses (Section IV-C) is commendable; standard Bernoulli loss models are often insufficient for characterizing RF link fading or structural blockage in swarms. The derivation of the TDMA superframe budget (Table VII) is rigorous and provides necessary realism regarding guard times and turnaround constraints.
*   **Weaknesses:** The reliance on a "static topology" assumption for the duration of a 1-year simulation (Section III-B-2) is a strong simplification. While acceptable for co-planar formations, it does not accurately reflect cross-plane mega-constellation geometries where neighbor relationships change dynamically ($\sim$10-minute timescales). While the authors address re-association overhead analytically, the *latency* implications of dynamic topology changes are under-represented in the DES results.

### 3. Validity & Logic
**Rating: 4 (Good)**

The conclusions are generally well-supported by the data. The paper effectively demonstrates that at low bandwidths (1 kbps backup links), the coordinator ingress link is the bottleneck, not processing power.
*   **Logic Check:** The argument that the "1 kbps regime is uniquely design-driving" is logically sound for safety-critical backup modes, though it risks making the paper seem less relevant for nominal optical-ISL operations. The authors handle this balance well by framing it as a "safe-mode floor."
*   **Baseline Comparison:** The comparison to the Centralized Ground Processing baseline (Section III-B-1) uses an $M/D/1$ queue to model ground server processing. This is a "strawman" argument. Centralized architectures are rarely limited by ground compute cycles ($N_{max} \approx 10^6$); they are limited by uplink spectrum availability and contact windows. The paper acknowledges this in text, but the quantitative comparison in figures focuses on the compute bound, which may mislead readers regarding the actual bottleneck of centralized systems.

### 4. Clarity & Structure
**Rating: 5 (Excellent)**

The manuscript is exceptionally well-written. The structure is logical, moving from problem definition to analytical derivation, then simulation validation, and finally sensitivity analysis.
*   **Notation:** The notation table is helpful, and variable definitions are consistent.
*   **Visualization:** Figures 5 (Recovery) and 8 (Workload Comparison) are effective. Table VII (TDMA Superframe) is a highlight, providing immediate utility to practitioners.
*   **Abstract:** The abstract is dense but accurate, clearly stating quantitative findings.

### 5. Ethical Compliance
**Rating: 5 (Excellent)**

The authors provide a clear acknowledgment of AI-assisted ideation (Claude, Gemini, GPT) in the Acknowledgments section, citing a specific methodology paper. This transparency aligns with emerging best practices in academic publishing. No conflicts of interest are apparent.

### 6. Scope & Referencing
**Rating: 5 (Excellent)**

The paper fits squarely within the scope of *IEEE TAES*, specifically the areas of Space Systems and Networked Control. The referencing is robust, bridging classical swarm robotics literature (Brambilla, Dorigo), space operations standards (CCSDS), and recent networking literature on mega-constellations (Handley, Bhattacherjee).

---

### Major Issues

1.  **The "Static Topology" Assumption:**
    In Section III-B-2, the authors state: *"The simulation assumes static cluster membership for the 1-year duration."* For a paper claiming relevance to mega-constellations (Starlink/Kuiper scale), this is a significant limitation. In Walker-Delta or polar constellations, cross-plane ISLs break and reform continuously. While the authors argue the *bandwidth* cost is low (<0.5%), the *protocol complexity* and potential for transient loops or packet loss during handoff are non-trivial.
    *   *Requirement:* The authors must explicitly discuss how the "Design Equations" hold up when $k_c$ (cluster size) fluctuates dynamically, or when a node is in a "handoff" state between clusters. A sensitivity analysis on "handoff frequency" would strengthen the validity for non-coplanar swarms.

2.  **Centralized Baseline Model:**
    The reference baseline for centralized control (Section III-B-1) models the ground station as a server queue ($M/D/1$). This suggests the limit of centralized control is CPU processing speed. In reality, the limit is RF spectrum and visibility (contact time).
    *   *Requirement:* The comparison in Table X and Figure 10 should be qualified. The authors should explicitly state that the "Centralized" curve represents a theoretical compute bound, and that a realistic centralized curve would saturate much earlier due to uplink bandwidth constraints. Comparing a bandwidth-constrained hierarchical model against a compute-constrained centralized model is an "apples-to-oranges" comparison.

3.  **MAC Layer Abstraction ($\gamma$):**
    The paper relies heavily on $\gamma$ (MAC efficiency) to abstract away contention. While the slot-level simulator validates the TDMA frame *assuming* synchronization, it does not validate the *acquisition* of that synchronization. In a 1 kbps RF backup scenario (GNSS denial), how do 100 nodes achieve slot alignment without consuming significant bandwidth?
    *   *Requirement:* Expand the discussion on synchronization overhead in the "RF-backup" regime. If the system relies on Slotted ALOHA to bootstrap the TDMA schedule, the initial convergence time could be significant.

### Minor Issues

1.  **Table I (Notation):** The definition of $\eta$ is given as "Protocol overhead." It would be helpful to explicitly state here that this excludes the 20.5% baseline telemetry, to avoid confusion with $\eta_{total}$.
2.  **Section IV-A (Sanity Checks):** The description of "Model A" and "Model B" is somewhat dense. A brief sentence explaining *why* these specific queueing models were chosen (e.g., "Model A represents a hard real-time constraint, while Model B represents a leaky bucket shaper") would improve readability.
3.  **Figure 6 (Joint Interaction):** The caption notes "Zero additional coordinator drops." It might be worth highlighting that this is due to the "Pipeline decoupling" mentioned in the text, as this is a counter-intuitive result for many readers who expect losses to trigger retransmission floods that overflow queues.
4.  **Equation 10 (AoI):** The derivation assumes independent Bernoulli trials for exception reporting. Does this hold if the "exception" is an external event (e.g., a solar flare) that triggers simultaneous reporting from all nodes? A brief note on correlated exception events would be beneficial.
5.  **Typos/Formatting:**
    *   Section III-A: "cycle-aggregated DES... (${\sim}7$ s at $N = 10^5$)" - Please clarify if this is wall-clock time per simulation run.
    *   References: Ensure all URL access dates are consistent (some say "accessed Feb 2026").

### Overall Recommendation
**Minor Revision**

The manuscript represents a high-quality contribution to the field. The derivation of sizing equations for large-scale space swarms fills a clear gap in the literature. The methodology is generally sound, and the writing is excellent. The "Major Issues" identified above regarding topology dynamics and the centralized baseline require textual clarification and perhaps minor analytical additions, but do not require a fundamental re-design of the simulation or experiments.

### Constructive Suggestions

1.  **Add a "Dynamic Topology" Subsection:** In the Discussion, add a dedicated paragraph estimating the impact of cross-plane link dynamics. Even a back-of-the-envelope calculation showing that handoff overhead remains negligible at typical LEO orbital periods would suffice to address the static topology concern.
2.  **Refine the Centralized Comparison:** In Table X, consider adding a row for "Centralized (Uplink Limited)" using a heuristic for spectral efficiency. If that is out of scope, simply reinforce the text to ensure readers understand the $M/D/1$ model is a theoretical upper bound on compute, not a system-level performance prediction.
3.  **Highlight the "10 kbps" Inflection Point:** The finding that all constraints vanish at $\geq$10 kbps is powerful. Consider moving this finding up to the conclusion or abstract more prominently. It tells designers that the difference between "barely functional" and "robust" is a very small amount of bandwidth, which is a key architectural insight.
4.  **Expand on Synchronization:** Briefly describe the "Sync Beacon" mechanism mentioned in Table VII. Is it a high-power broadcast? How robust is it to the Hidden Node Problem? A few sentences here would add credibility to the $\gamma = 0.85$ assumption.