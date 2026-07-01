---
paper: "02-swarm-coordination-scaling"
version: "ai"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-27"
recommendation: "Minor Revision"
---

**Review for IEEE Transactions on Aerospace and Electronic Systems**

**Manuscript Title:** Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study
**Version:** AI

---

### 1. Significance & Novelty
**Rating: 4**

The manuscript addresses a critical and timely issue in aerospace engineering: the scalability of command and control (C2) architectures for mega-constellations and future autonomous swarms. As commercial entities deploy constellations exceeding 10,000 nodes, the transition from human-in-the-loop ground control to autonomous hierarchical coordination is inevitable.

The novelty lies not in the hierarchical topology itself—which is a well-understood structure in distributed systems—but in the **quantitative, byte-level characterization** of the control plane under specific orbital constraints (1 kbps backup links, correlated losses). The paper successfully moves beyond abstract "Big O" complexity analysis to provide concrete engineering sizing values (e.g., the 21–50 kbps coordinator ingress requirement). The distinction between "workload-driven" and "topology-driven" overhead is a valuable contribution that clarifies where the bandwidth budget is actually spent.

### 2. Methodological Soundness
**Rating: 4**

The use of a cycle-aggregated Discrete Event Simulation (DES) is an appropriate choice for simulating $10^5$ nodes; a packet-level simulation (e.g., NS-3) would likely be computationally intractable for Monte Carlo sweeps at this scale. The authors have done an excellent job of validating their simulation against analytical bounds (M/D/1, Binomial, Geometric distributions), which builds high confidence in the results.

However, a significant methodological limitation is the abstraction of the MAC layer. The paper applies a scalar efficiency factor ($1/\gamma$) to account for MAC overhead. While this is acceptable for the hierarchical topology (which naturally lends itself to TDMA), it likely underestimates the performance degradation of the "Sectorized Mesh" comparator. In a mesh topology with high node density, hidden terminal problems and contention window back-offs would likely cause throughput to collapse faster than the linear $1/\gamma$ scaling suggests. The authors acknowledge this in the Discussion, but it remains a limitation of the comparative analysis.

### 3. Validity & Logic
**Rating: 5**

The conclusions are rigorously supported by the data. The authors are careful to distinguish between *offered load* and *delivered throughput*, which is crucial when analyzing lossy links. The finding in Section IV-D—that Gilbert-Elliott (GE) retransmissions and coordinator capacity saturation interact independently under point-to-point link assumptions—is a subtle but logically sound system engineering insight.

The "Dual-Regime Interpretation" (Section IV-E-3) is particularly strong. It correctly identifies that while 46% overhead sounds high, it applies to the worst-case RF backup link (1 kbps), and the absolute byte count is negligible for optical ISLs. This nuance prevents the reader from misinterpreting the overhead as a disqualifying factor for high-speed operations.

### 4. Clarity & Structure
**Rating: 5**

The manuscript is exceptionally well-written and organized. The progression from single-factor analysis (capacity, AoI, loss) to joint interaction (Section IV-D) is logical. The tables are dense but informative, specifically Table VII (Topology Comparison), which effectively synthesizes the paper's findings.

The definition of metrics is precise. The distinction between "Baseline Telemetry" (topology-invariant) and "Protocol Overhead" ($\eta$) is maintained consistently, preventing apples-to-oranges comparisons.

### 5. Ethical Compliance
**Rating: 3**

The research content appears ethically sound. However, I must flag the **Authorship** and **Acknowledgment** sections for the Editor's attention regarding IEEE policy.
1.  **Authorship:** "Project Dyson Research Team" is listed as the author. IEEE policy generally requires individual human authors to be listed to establish accountability.
2.  **AI Disclosure:** The Acknowledgment states that AI models (Claude, Gemini, GPT) were used for "ideation." While IEEE guidelines generally permit AI use for editing and idea generation (provided human authors take full responsibility), the specific phrasing and the anonymity of the team require verification to ensure compliance with the *IEEE Submission Guidelines for AI-Generated Text*.

### 6. Scope & Referencing
**Rating: 5**

The paper fits squarely within the scope of TAES, bridging the gap between communication systems and orbital operations. The references are a good mix of classical theory (Kleinrock, Lamport, Reynolds) and modern operational context (Starlink, Kuiper, CCSDS standards). The inclusion of CCSDS BPv7 and Proximity-1 references grounds the theoretical work in practical space standards.

---

### Major Issues

1.  **MAC Layer Contention in Mesh Topologies:**
    In Section IV-F and Fig. 10, the Sectorized Mesh is shown to scale with a constant overhead factor relative to the hierarchy. This relies on the assumption that MAC efficiency $\gamma$ remains constant as density increases. In reality, for a mesh architecture using shared spectrum (RF), collision probability increases with node density within the sector. The paper should explicitly state that the Sectorized Mesh results represent a *best-case scheduled access* (TDMA) implementation, rather than a contention-based (CSMA) one, or acknowledge that mesh performance would degrade super-linearly in contention scenarios.

2.  **The "Single-Server" Centralized Baseline:**
    In Fig. 10 and the abstract, the authors compare against a centralized baseline with $c=1$ (single server), showing it diverges at $N=10^4$. While the paper admits this is a "theoretical bound," it is somewhat of a strawman. No operational system for 10,000 satellites would run on a single thread. The "Realistic Centralized" ($c=N/k_c$) baseline discussed in the text is the fair comparator. The abstract and conclusion should emphasize the comparison against the *realistic* centralized baseline (which fails due to spectrum/latency, not processing) to avoid overstating the processing advantage of the hierarchy.

### Minor Issues

1.  **Eq. 12 (AoI to Position Error):** The model $\sigma_{pos} = \sigma_0 + \dot{\sigma} \cdot \text{AoI}$ assumes linear error growth. In orbital mechanics, along-track error due to drag uncertainty grows quadratically with time ($t^2$) over longer durations. For the short timescales involved (400s), linear is an acceptable approximation, but this should be clarified.
2.  **Table I (Authors):** The URL "https://projectdyson.org" is cited. Ensure this is a persistent, archival link or remove it in favor of a standard repository citation for the code.
3.  **Section IV-A (Coordinator Capacity):** The distinction between "Cluster Coordinator Ingress" and "Regional Coordinator Ingress" is made, but the capacity results focus heavily on the cluster level. A brief sentence confirming that Regional Coordinators (handling $N/k_c$ summaries) are not the bottleneck would be helpful.
4.  **Fig. 6 (Workload):** The "Event-driven" profile is very close to "Nominal." It might be visually clearer to plot the delta or use a log scale for the Y-axis to distinguish them, though the linear scale emphasizes the dominance of the Stress case.

---

### Overall Recommendation
**Minor Revision**

The paper is technically rigorous, well-written, and highly relevant. The simulation methodology is sound for the message-layer abstraction chosen. The revisions required are primarily regarding the framing of the baselines (to ensure fairness) and clarifying the limitations of the MAC abstraction for the mesh topology. The authorship attribution must be resolved with the Editor to meet IEEE standards.

### Constructive Suggestions

1.  **Refine the Mesh Comparator:** Explicitly label the Sectorized Mesh results as "Scheduled/TDMA Mesh" to clarify that contention-based collapse is not modeled. This strengthens the paper by defining the boundary of the simulation.
2.  **Update Abstract regarding Centralized Baseline:** Modify the abstract to de-emphasize the $c=1$ processing limit (which is artificial) and highlight the *spectrum* and *latency* limits of the centralized architecture, which are the true physical differentiators identified in Section IV-F.
3.  **Expand on Eq. 12:** Add a brief qualifier that the linear position error growth is a short-term approximation and that full covariance propagation would be required for precise conjunction assessment (as noted in Future Work).
4.  **Authorship Compliance:** Replace "Project Dyson Research Team" with specific human author names and affiliations to comply with IEEE accountability standards.