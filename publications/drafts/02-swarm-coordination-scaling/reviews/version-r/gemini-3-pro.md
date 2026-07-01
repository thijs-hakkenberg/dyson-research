---
paper: "02-swarm-coordination-scaling"
version: "r"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-24"
recommendation: "Minor Revision"
---

## Peer Review: IEEE Transactions on Aerospace and Electronic Systems

**Manuscript Title:** Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study
**Version:** R

---

### 1. Significance & Novelty
**Rating: 5 (Excellent)**

This manuscript addresses a critical and rapidly emerging gap in aerospace systems engineering: the coordination of "mega-constellations" and future autonomous swarms at the $10^4$--$10^5$ node scale. While existing literature covers small swarms ($<100$ nodes) or traditional constellation management, there is a paucity of rigorous quantitative analysis for the intermediate regime where centralized control breaks down but fully distributed mesh is bandwidth-prohibitive.

The novelty lies in the specific "byte-counting" approach. Rather than relying on abstract complexity classes ($O(N)$ vs $O(\log N)$), the authors provide concrete engineering parameters (e.g., "21% overhead," "50 kbps coordinator links"). The introduction of the **Sectorized Mesh** as an intermediate comparator is a significant contribution, providing a realistic decentralized baseline rather than just the "strawman" global-state mesh. The Age-of-Information (AoI) analysis regarding exception-based telemetry is also a high-value contribution, quantifying the cost of bandwidth savings in terms of state staleness.

### 2. Methodological Soundness
**Rating: 4 (Good)**

The use of a **cycle-aggregated Discrete Event Simulation (DES)** is an appropriate methodological choice for this scale. Simulating $10^5$ nodes at the packet level (e.g., using ns-3) for year-long durations is computationally intractable; the authors' abstraction to the message-passing layer allows for statistically significant Monte Carlo runs (30 replications) across a wide parameter space.

However, the abstraction of the MAC layer (Physical Layer) is a limitation that prevents a perfect rating. The assumption that MAC inefficiencies can be captured by a linear scalar $\gamma \in [0.7, 0.9]$ is a strong one. In reality, as node density increases, the noise floor and contention in shared spectrum (even with TDMA) can exhibit non-linear scaling effects. While the authors acknowledge this in the "Limitations" and Section V-E, the claim of "queue stability" is valid only within the logical message-passing abstraction, not necessarily the physical link layer.

The validation against closed-form analytical models (Section IV-E) is robust and increases confidence in the DES implementation.

### 3. Validity & Logic
**Rating: 4 (Good)**

The conclusions are generally well-supported by the data. The derivation of the $O(1)$ overhead scaling for the hierarchical architecture is mathematically sound given the aggregation rules. The trade-off analysis between duty cycle, power variance, and handoff reliability is logical and provides actionable design heuristics.

A minor concern regarding logic appears in the comparison with the Centralized Baseline. The authors explicitly state in the text that the single-server ($c=1$) model is a worst-case bound. However, presenting this specific bound in Figure 2 creates a visual argument that centralized processing fails at $10^4$ nodes. As the authors admit in Table I, a hyperscale cloud backend ($c=1000$) handles this easily. The *logic* holds, but the *visual presentation* of the centralized baseline borders on a "strawman" argument, despite the textual disclaimers.

### 4. Clarity & Structure
**Rating: 5 (Excellent)**

The manuscript is exceptionally well-written. The structure is logical, following a standard progression from architecture to simulation to results. The definitions of metrics (Section III-H) are precise. The "Baseline Interpretation Note" in the Introduction is a helpful guide for the reader.

Figures are generally clear and informative. Figure 1 (Architecture) and Figure 8 (Topology Summary) are particularly effective. The distinction between "Protocol Overhead" ($\eta$) and "Total Utilization" is handled carefully to avoid confusion.

### 5. Ethical Compliance
**Rating: 5 (Excellent)**

The authors provide a clear acknowledgment of AI-assisted ideation in the Acknowledgments section, citing specific models and the scope of their use. This aligns with emerging best practices for transparency. There are no apparent conflicts of interest or ethical concerns regarding the research content.

### 6. Scope & Referencing
**Rating: 5 (Excellent)**

The paper fits squarely within the scope of *IEEE TAES*, specifically the areas of Space Systems and Networked Systems. The reference list is comprehensive, bridging classical swarm robotics (Brambilla, Dorigo), modern constellation networking (Handley, Del Portillo), and theoretical distributed systems (Lynch, Lamport). The inclusion of recent industry context (Starlink, Kuiper) keeps the work grounded in current operational realities.

---

### Major Issues

1.  **Visual Representation of Centralized Baseline (Fig. 2):**
    While the text (Section III-B-1) honestly acknowledges that the single-server ($c=1$) centralized model is a worst-case bound, Figure 2 plots this curve alongside the optimized hierarchical and mesh curves. This visual comparison is misleading. A reader skimming the figures would conclude that centralized architectures fundamentally fail at processing $10^4$ nodes, which is false (as shown in Table I).
    *   *Requirement:* Figure 2 must be updated to include at least one parallelized centralized curve (e.g., $M/D/c$ with $c=100$) to show where a realistic ground system would saturate. This will likely show that processing is *not* the bottleneck, reinforcing the authors' text argument that *propagation latency* and *uplink spectrum* are the true drivers for distributed architectures.

2.  **Coordinator Election Overhead Accounting:**
    The paper discusses "Handoff" traffic (state transfer) and excludes it from $\eta$ because it uses a separate optical ISL. However, the paper does not explicitly account for the **Coordinator Election** traffic (e.g., Raft/Paxos consensus messages, heartbeats required to detect coordinator failure *before* a new one is elected).
    *   *Requirement:* Clarify if election protocol overhead (voting messages) is included in $\eta$. If not, justify why this overhead is negligible. In a dynamic environment with 24-hour duty cycles, the control traffic to agree on the *next* coordinator is non-zero.

### Minor Issues

1.  **Section IV-G (Coordinator Bandwidth):** The distinction between "Unscheduled" (50 kbps) and "TDMA" (24 kbps) is valuable. However, the text states "TDMA eliminates random-phase burstiness." While true for the *schedule*, it assumes perfect synchronization. Please briefly mention the requirement for time synchronization accuracy to maintain the $\gamma=0.85$ efficiency.
2.  **Figure 5 (Latency Distribution):** The caption notes that the $10^6$ curve is an "analytical extrapolation." This should be marked more clearly on the plot itself (e.g., dashed lines or a distinct marker style) to distinguish it from DES-validated data.
3.  **Equation 10 (Power):** This equation assumes linear amortization of power. It neglects the power conversion efficiency losses when switching modes. This is a minor point but worth a quick check.
4.  **Section V-E (Limitations):** The limitation regarding "Correlated failures (SPE)" is mentioned. It would be beneficial to explicitly state that the current model assumes Independent and Identically Distributed (i.i.d.) failures, which is the "best case" for reliability analysis.

---

### Overall Recommendation
**Minor Revision**

The manuscript represents a high-quality contribution to the field with rigorous simulation and clear writing. The "Sectorized Mesh" and "AoI" analyses are excellent. The revision is primarily requested to correct the visual representation of the centralized baseline (to ensure intellectual fairness) and to clarify the accounting of election protocol traffic. These changes do not require re-running the core simulations but will significantly improve the robustness of the arguments.

---

### Constructive Suggestions

1.  **Revise Figure 2:** Plot the Centralized Baseline as a *region* (shaded area) bounded by $c=1$ (single server) and $c=100$ (cluster), rather than a single line. This visually demonstrates that while processing *can* be solved, it requires scaling ground resources linearly, whereas the hierarchical architecture stays constant.
2.  **Expand on "Election" vs. "Handoff":** Add a paragraph in Section III-B-2 distinguishing between the *state transfer* (bulk data, optical link) and the *consensus signaling* (voting, coordination channel). Explicitly state that the voting traffic is included in the "Coordination command/ACK" budget or explain why it is omitted.
3.  **Strengthen the Physical Layer Caveat:** In the Conclusion, explicitly recommend that future work should move from "Cycle-Aggregated DES" to "Packet-Level Simulation" for a specific sub-scale cluster (e.g., $N=100$) to validate the $\gamma$ (MAC efficiency) parameter used in this study.
4.  **AoI Context:** In Section IV-F, relate the P99 AoI of 400s (at $p_{exc}=0.10$) to a specific orbital dynamic scenario. For example, "In LEO, a 400s delay corresponds to a positional uncertainty growth of $X$ km," to give the reader a physical sense of the risk.