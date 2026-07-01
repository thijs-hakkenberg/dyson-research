---
paper: "02-swarm-coordination-scaling"
version: "ae"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-27"
recommendation: "Accept"
---

## Peer Review: IEEE Transactions on Aerospace and Electronic Systems

**Manuscript ID:** [Version AE]
**Title:** Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study
**Reviewer Expertise:** Distributed Systems, Swarm Robotics, Discrete Event Simulation, Mega-constellation Architectures.

---

### 1. Significance & Novelty
**Rating: 5 (Excellent)**

This manuscript addresses a critical and timely gap in the aerospace literature: the specific scaling properties of coordination architectures for "mega-swarms" ($10^4$--$10^5$ nodes). While existing literature covers constellation management (typically centralized, $<10^4$ nodes) and swarm robotics (typically decentralized, $<10^3$ nodes), this paper rigorously explores the "uncomfortable middle" where centralized control breaks down due to latency/spectrum limits, but full mesh networking breaks down due to $O(N^2)$ state explosion.

The novelty lies in the **byte-level traffic accounting** applied to a hierarchical topology at this specific scale. Most swarm papers rely on abstract agent-based modeling without realistic communication constraints; this paper treats bandwidth as the primary scarce resource (1 kbps/node budget). The definition of the "Workload Design Envelope" (spanning $9\times$ from nominal to stress cases) provides valuable engineering intuition for system architects.

### 2. Methodological Soundness
**Rating: 4 (Good)**

The use of Cycle-Aggregated Discrete Event Simulation (DES) is an appropriate choice for simulating $10^5$ nodes over year-long durations. A packet-level simulator (like NS-3) would be computationally intractable at this scale. The authors are transparent about the abstraction level (message-passing layer) and explicitly list what is *not* modeled (MAC scheduling, link acquisition).

However, the reliance on a linear MAC efficiency factor ($\gamma \in [0.7, 0.9]$) to convert message-layer overhead to physical bandwidth is a simplification. While the authors argue this understates the disadvantage of the mesh topology (which would suffer non-linear contention), a more rigorous justification or a sensitivity analysis extending $\gamma$ down to Slotted ALOHA levels (0.36) for the mesh cases would strengthen the method.

The validation against analytical models (M/D/1 for centralized, Geometric distribution for AoI) builds confidence in the simulation engine.

### 3. Validity & Logic
**Rating: 5 (Excellent)**

The conclusions are logically derived from the data. The paper effectively debunks the notion that hierarchical overhead scales poorly; by proving $O(1)$ scaling analytically and validating it via DES, the authors make a strong case for hierarchy in large constellations.

The analysis of the Gilbert-Elliott (GE) link model is particularly strong. The finding that intra-cycle retransmission is structurally ineffective against correlated bursts (recovering only 27% vs 87.5%) is a crucial insight that dictates the need for inter-cycle store-and-forward protocols (like DTN/BPv7).

The distinction between the "Global-State Mesh" (upper bound) and "Sectorized Mesh" (competitor) is fair. The authors avoid setting up a "straw man" by including the sectorized mesh, which is a viable decentralized alternative, and showing that the hierarchy still outperforms it in terms of overhead ($\sim$46% vs $\sim$65%).

### 4. Clarity & Structure
**Rating: 5 (Excellent)**

The manuscript is exceptionally well-written. The structure is logical, moving from architecture definitions to simulation setup, then results, and finally design implications.

*   **Tables:** Table V (Traffic Accounting) and Table VII (Coordinator Bandwidth) are exemplary. They allow for reproducibility and quick reference.
*   **Figures:** Figure 6 (Workload Comparison) and Figure 10 (Overhead vs. Nodes) clearly communicate the core scaling findings.
*   **Abstract:** The abstract is dense but informative, containing specific quantitative results rather than vague generalizations.

### 5. Ethical Compliance
**Rating: 5 (Excellent)**

The authors provide a clear "Data Availability" statement pointing to a repository and explicitly disclose the use of AI tools for "ideation" in the Acknowledgments, which aligns with emerging best practices for transparency. No human subjects or hazardous materials are involved.

### 6. Scope & Referencing
**Rating: 4 (Good)**

The paper fits squarely within the scope of *IEEE TAES*. It bridges the gap between networking/communications and orbital systems engineering.

The references are generally good, covering foundational distributed systems theory (Lynch, Lamport) and modern space networking (CCSDS, DTN). However, there is a reliance on some non-archival sources for current constellation data (e.g., Starlink/Kuiper websites). While unavoidable given the rapid pace of industry, the authors should ensure these are cited as "accessed on [Date]" or replaced with regulatory filings (FCC/ITU) where possible for permanence.

---

### Major Issues

1.  **Abstract "Stress Case" Dominance:**
    The abstract states that the design envelope has a "stress-case upper bound at $\eta \approx 46\%$." While the paper later clarifies that the "nominal" operations are only $\sim 5\%$, the prominence of the 46% figure in the abstract and introduction risks misleading the reader into thinking the architecture is inherently inefficient. A 46% overhead for a control plane is arguably unacceptably high for a commercial system. The abstract should be rephrased to emphasize that 5% is the *sustained* operating point, and 46% is a *peak* capacity sizing requirement for worst-case maneuvering.

2.  **MAC Layer Contention in Sectorized Mesh:**
    In Section IV-F (Topology Comparison), the comparison between Hierarchical and Sectorized Mesh relies on the message-layer overhead. The authors note in the text that "MAC-layer efficiency... scales absolute bandwidth by $1/\gamma$." However, for the Sectorized Mesh, $\gamma$ is not a constant; it is a function of node density and neighbor count ($k_s$). With 10 neighbors competing for the channel, the effective $\gamma$ would likely be much lower than the 0.7-0.9 range used for the scheduled hierarchical links. The paper should explicitly acknowledge that assuming a constant $\gamma$ likely *favors* the mesh topology, making the hierarchical advantage even stronger than reported.

### Minor Issues

*   **Section I-C (Baseline Interpretation):** The phrasing "The two reference baselines are intentional bounds" is helpful, but the definition of the "Global-State Mesh" requiring $O(N)$ peers is extremely aggressive. It is worth reiterating here that no practical engineer would build a global-state mesh for $10^5$ nodes; it is purely a theoretical upper bound.
*   **Section IV-A (Coordinator Capacity):** The distinction between "Model A" (Deadline) and "Model B" (Leaky Bucket) is excellent. However, in Table VIII, the column "Raw Link" for TDMA is listed as 28 kbps. Please clarify in the caption or text if this includes the guard-time overhead calculated in Eq. 12.
*   **Eq. 11 (AoI Analytic):** The formula uses $\ln(1 - 0.99)$. Please double-check the sign convention. $\ln(0.01)$ is negative, and $\ln(1-p_{exc})$ is negative, resulting in a positive integer. The math is correct, but the notation could be slightly cleaner as $\frac{\ln(1-P)}{\ln(1-p)}$.
*   **Table II:** The label "Hyperscale data center" for $c=1000$ servers (processing 1M messages/sec) seems hyperbolic. A single modern Kafka cluster can handle this. Perhaps rename to "High-performance compute cluster."
*   **Typos:**
    *   Table IV Footnote 'a': "This rate includes all proximity monitoring events... not maneuver-triggering conjunctions." This is a very important distinction that is buried in a footnote. Consider moving this to the main text in Section III-E.

### Overall Recommendation
**Accept with Minor Revisions**

This is a high-quality paper that contributes valuable quantitative design data to the field of large-scale space systems. The simulation methodology is robust for the questions asked, and the results regarding coordinator sizing and correlated losses are directly applicable to future constellation designs. The revisions requested are primarily regarding the presentation of the "stress case" to prevent misinterpretation and clarifying the MAC layer assumptions for the mesh topology.

### Constructive Suggestions

1.  **Reframe the Abstract:** Rewrite the abstract to lead with the "Nominal" overhead ($\sim 5\%$) as the standard operating condition. Frame the 46% explicitly as a "worst-case sizing parameter" for link budgeting, rather than a typical operating overhead.

2.  **Strengthen the Mesh MAC Argument:** In the Discussion (Section V), add a brief qualitative argument or a reference regarding CSMA/CA throughput degradation with node density. This will fortify the claim that the Sectorized Mesh performance is an upper bound on what is achievable, further supporting the Hierarchical recommendation.

3.  **AoI Context:** In Section IV-B, when discussing the 230m position error, add a stronger disclaimer that this assumes a specific orbit and drag environment. Suggest adding a sentence: "This mapping is highly sensitive to orbital altitude and solar activity; operational implementations must utilize full covariance propagation."

4.  **Handoff Clarification:** Explicitly state in the Introduction or System Model that the architecture *requires* a dual-band approach (RF/Optical for coordination vs. Optical for bulk state transfer). The feasibility of the architecture hinges on the assumption that the 10-50 MB state transfer does not clog the 1 kbps control channel. This is mentioned, but it is a critical architectural constraint that deserves highlighting.