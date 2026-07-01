---
paper: "02-swarm-coordination-scaling"
version: "af"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-27"
recommendation: "Accept"
---

Here is the peer review for the manuscript "Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study."

---

# Peer Review Report

**Journal:** IEEE Transactions on Aerospace and Electronic Systems
**Manuscript ID:** [Assigned by Editor]
**Title:** Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study
**Version:** AF

## Review Criteria

### 1. Significance & Novelty
**Rating: 4 (Good)**

The paper addresses a critical and timely gap in the aerospace engineering literature: the scalability of coordination architectures for "mega-constellations" and future autonomous swarms ($10^3$ to $10^5$ nodes). While the current literature covers small-scale swarms (tens of agents) or centralized management of existing constellations, there is a lack of rigorous quantitative analysis for the intermediate regime where ground-based control breaks down but full mesh networking is bandwidth-prohibitive.

The novelty lies in the specific methodology: a cycle-aggregated Discrete Event Simulation (DES) with byte-level accounting that explicitly models the "middle ground" hierarchical architecture. The derivation of specific engineering constraints (e.g., the 21–50 kbps coordinator ingress requirement) provides actionable design data for future system architects. The distinction between "message-layer" and "MAC-layer" overhead is a significant practical contribution often overlooked in purely theoretical graph-theory papers.

### 2. Methodological Soundness
**Rating: 5 (Excellent)**

The methodology is the strongest aspect of this work. The authors have constructed a robust simulation framework that balances fidelity with computational feasibility.
*   **Validation:** The use of closed-form analytical cross-checks (Pollaczek–Khinchine for queues, geometric distributions for AoI) to validate the DES is exemplary. It builds high confidence in the simulation results.
*   **Parameter Sweeps:** The parametric sweep across topology, workload, and scheduling models is comprehensive. The "stress-case" vs. "nominal" workload differentiation is crucial for realistic system sizing.
*   **Statistical Rigor:** The use of Monte Carlo methods with 30 replications and bootstrap confidence intervals is appropriate for the stochastic elements (failures, phase offsets).
*   **Assumptions:** The assumptions (e.g., 1 kbps budget, specific message sizes) are clearly stated and justified as conservative bounds.

### 3. Validity & Logic
**Rating: 4 (Good)**

The conclusions are generally well-supported by the data. The paper effectively debunks the notion that hierarchical overhead scales poorly, demonstrating $O(1)$ scaling relative to fleet size. The analysis of the Gilbert-Elliott (GE) link model is particularly insightful, logically proving that intra-cycle retransmission is futile against correlated bursts—a finding that has significant implications for protocol design.

However, there is a slight logical tension regarding the "Sectorized Mesh." The paper compares a hierarchical model (which naturally handles global coordination via aggregation) against a sectorized mesh (which only handles local coordination). While the authors acknowledge this difference in "state completeness," the direct comparison of overhead percentages ($\eta$) feels slightly like comparing apples to oranges. The sectorized mesh is penalized for high overhead while providing a different quality of service (local vs. global). This should be nuanced further in the discussion.

### 4. Clarity & Structure
**Rating: 5 (Excellent)**

The manuscript is exceptionally well-written. The structure is logical, moving from problem definition to methodology, results, and discussion.
*   **Precision:** The definitions of metrics (e.g., $\eta$, $p_{\text{exc}}$, $\gamma$) are precise and used consistently.
*   **Visuals:** The description of figures suggests they are well-integrated with the text. The tables (especially Table IV regarding traffic accounting) are dense but highly informative.
*   **Readability:** The "Dual-Regime Interpretation" section is very helpful for readers who might question the 1 kbps constraint. The writing style is professional, concise, and suitable for a high-impact IEEE transaction.

### 5. Ethical Compliance
**Rating: 5 (Excellent)**

The authors provide a specific acknowledgment regarding the use of AI tools (Claude, Gemini, GPT) for "ideation" and "concept generation," which aligns with emerging transparency standards. There are no apparent conflicts of interest or ethical concerns regarding the research subject matter.

### 6. Scope & Referencing
**Rating: 4 (Good)**

The paper fits perfectly within the scope of *IEEE TAES*. The references are current and relevant, citing both classical distributed systems theory (Lamport, Lynch) and modern space systems literature (Starlink, Kuiper, CCSDS standards).

One minor gap is the lack of reference to specific Delay Tolerant Networking (DTN) routing protocols beyond the general architecture (BPv7). Since the paper concludes that store-and-forward is necessary, a brief nod to Contact Graph Routing (CGR) or similar specific implementations would strengthen the context.

---

## Major Issues

*None.* The paper is technically sound and ready for publication subject to the minor issues below.

## Minor Issues

1.  **Sectorized Mesh Fairness (Section IV-F):** As noted in the Validity section, the comparison between Hierarchical and Sectorized Mesh overhead is technically accurate but perhaps conceptually slightly unfair regarding *functionality*. The text states the sectorized mesh produces $1.35-1.95\times$ higher overhead. It would be beneficial to explicitly reiterate here that the Hierarchical model includes *global* summary aggregation, whereas the Sectorized model does not. The hierarchy is doing *more* work (global reach) for *less* bandwidth, which strengthens the argument, but the distinction in service level should be clearer in the summary comparison.
2.  **MAC Efficiency ($\gamma$) Notation:** The paper uses $\gamma$ for MAC efficiency. In Section IV-A, Eq. 11 defines $C_{\text{raw}} = C_{\text{coord}} / \gamma$. However, in Section I-C, the text states overhead scales by $1/\gamma$. These are consistent, but in Section IV-E (Table VIII), $\eta_{\text{eff}}$ is defined as $\eta_{\text{DES}} / \gamma$. Please ensure the reader does not confuse *capacity scaling* (multiplying required link rate by $1/\gamma$) with *overhead percentage scaling* (dividing the ratio by $\gamma$). The physics are correct, but the phrasing could be tightened to avoid confusion.
3.  **Coordinator Election Traffic:** In Section III-H, coordinator election traffic is dismissed as negligible ($<0.01\%$). While true for bandwidth, does this traffic have a latency impact? If an election occurs during a congestion event, does the Raft-style voting add to the queue depth? A single sentence clarifying if election messages are prioritized or treated as standard traffic would be helpful.
4.  **Table II (Mesh Traffic):** The footnote calculation for $R_{\text{conv}}$ mentions "gossip redundancy... factor ~1.4x". It would be helpful to cite the source of this factor (is it an empirical result from the DES or a theoretical constant from epidemic algorithms literature?).

## Overall Recommendation

**Accept / Minor Revision**

This is a high-quality paper that makes a distinct contribution to the field of autonomous space systems. The methodology is rigorous, the writing is clear, and the results are actionable. The revisions requested are clarifying in nature and do not require new simulations.

## Constructive Suggestions

1.  **Strengthen the "Store-and-Forward" Conclusion:** The paper concludes that inter-cycle store-and-forward is necessary for GE loss resilience. You could strengthen this by explicitly mentioning *Contact Graph Routing (CGR)* or *Schedule-Aware Bundle Routing (SABR)* as the likely implementation candidates for this mechanism in the Discussion.
2.  **Visualizing the "Design Envelope":** Fig. 10 (Workload Comparison) is good, but a "Design Chart" might be better for practitioners. Consider a plot with "Command Rate" on the X-axis and "Required Coordinator Bandwidth" on the Y-axis, with regions shaded for "Safe Operation" (Zero Drop) vs. "Saturated." This would synthesize the overhead and capacity sections into a single lookup tool.
3.  **Clarify "Physical Meaning" of AoI:** In Section IV-B, you map AoI to position error ($\sim 230$ m). You rightly caveat this as illustrative. It would be valuable to add a sentence explicitly stating that for *collision avoidance*, the relevant metric is often covariance ellipsoid overlap, and that stale covariance data generally leads to *larger* ellipsoids (false positives) rather than just position error (missed detections). This adds operational nuance.