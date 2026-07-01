---
paper: "02-swarm-coordination-scaling"
version: "AA"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-26"
recommendation: "Minor Revision"
---

## Peer Review: IEEE Transactions on Aerospace and Electronic Systems

**Manuscript ID:** Version AA
**Title:** Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study
**Authors:** Project Dyson Research Team

---

### 1. Significance & Novelty
**Rating: 5**

This manuscript addresses a critical and timely gap in the aerospace engineering literature: the specific scaling behaviors of coordination architectures for "mega-constellations" ($10^4$--$10^5$ nodes). While swarm robotics literature handles small $N$ and networking literature handles routing, there is a paucity of work that rigorously characterizes the *control plane* overhead for autonomous operations at this specific scale.

The novelty lies not in the proposal of hierarchical control (which is well-established), but in the **quantitative characterization** of its limits under strict bandwidth constraints (1 kbps/node). The application of Age-of-Information (AoI) metrics to satellite telemetry and the comparative analysis of Gilbert-Elliott channel models against standard Bernoulli losses provide significant practical value for system architects. The identification of the "9x design envelope" based on workload assumptions is a valuable contribution that moves beyond generic "O(N)" complexity statements.

### 2. Methodological Soundness
**Rating: 4**

The methodology is generally robust. The choice of a cycle-aggregated Discrete Event Simulation (DES) is appropriate for the scale; simulating individual packets for $10^5$ nodes over a year would be computationally intractable. The authors have taken care to validate their simulation against closed-form analytical models (Section IV-E), which builds high confidence in the results.

However, there is a notable tension in the abstraction level. The simulation operates at the "message layer" (Table VI), abstracting away MAC-layer contention, link acquisition, and pointing errors. While the authors introduce a guard-time efficiency factor ($\gamma$), this linear scalar may not capture non-linear congestion effects in a real shared medium, particularly for the sectorized mesh topology. The assumption that TDMA is perfectly achievable with a 15% guard band in a dynamic orbital environment is optimistic.

### 3. Validity & Logic
**Rating: 5**

The conclusions are well-supported by the data presented. The authors are careful to distinguish between topology-invariant loads (baseline telemetry) and protocol overhead. The logic regarding the "strawman" nature of the centralized and global-mesh baselines is sound—they serve as boundary conditions rather than competitive proposals.

The analysis of the Coordinator Capacity (Section IV-A) is particularly strong. The distinction between the "Deadline" model and the "Leaky-bucket" model provides a nuanced view of how burstiness affects hardware requirements. The conclusion that store-and-forward is structurally required for correlated losses (Section IV-C) is logically sound and mathematically verified by the simulation results.

### 4. Clarity & Structure
**Rating: 5**

The manuscript is exceptionally well-written. The structure is logical, moving from architecture definitions to simulation setup, results, and discussion. The definitions of metrics (Section III-H) are precise. Tables are dense but informative, particularly Table V (Simulation Parameters) and Table VII (Traffic Accounting), which ensure reproducibility. The distinction between the "Stress," "Nominal," and "Event-driven" workloads helps clarify the wide variance in overhead results.

### 5. Ethical Compliance
**Rating: 5**

The authors disclose the use of AI for ideation in the Acknowledgments, which complies with emerging publication standards. No human subjects are involved. The research appears ethically sound.

### 6. Scope & Referencing
**Rating: 5**

The paper fits squarely within the scope of *IEEE TAES*, bridging the gap between electronic systems (communications/networking) and aerospace operations. The references are comprehensive, covering foundational queueing theory (Kleinrock), distributed consensus (Lamport, Ongaro), and modern constellation literature (Handley, Del Portillo).

---

### Major Issues

**1. The "Single-Server" Centralized Baseline is a Weak Strawman**
In Section III-B-1, the centralized baseline is modeled as a single server ($c=1$). While the authors acknowledge this is an "intentional worst-case bound," it weakens the comparison. Modern ground segments for constellations like Starlink are cloud-native, hyperscale distributed systems. The bottleneck for centralized control is rarely *processing* capacity ($\mu_s$), but rather **uplink/downlink spectrum availability** and **propagation latency**.
*   **Critique:** By focusing on the $M/D/1$ queue divergence, the paper attacks the easiest target.
*   **Requirement:** The authors should explicitly acknowledge that while the *processing* limit of centralized control can be solved via horizontal scaling ($c \to \infty$), the *bandwidth* and *latency* limits cannot. The comparison should focus more on the spectrum cost of backhauling all telemetry to Earth versus the processing bottleneck.

**2. TDMA Synchronization Feasibility**
In Section IV-A, the paper suggests TDMA reduces the coordinator zero-drop threshold from 50 kbps to ~24 kbps. This relies on a guard-time factor $\gamma = 0.85$.
*   **Critique:** In a swarm of 100 satellites moving at 7.6 km/s with varying relative ranges, maintaining slot synchronization to within 15% overhead is non-trivial. It requires precise clock synchronization and range-compensated transmission times.
*   **Requirement:** The discussion needs to address the *cost* of this synchronization. Does the "Heartbeat/ACK" traffic include the necessary timing exchange to maintain this TDMA schedule? If not, the overhead for TDMA might be understated.

---

### Minor Issues

1.  **Table II (Scalability Sensitivity):** The table lists "10,000,000" for a hyperscale data center. While mathematically correct for the $M/D/c$ model, this number is practically limited by the number of ground station antennas, not servers. A footnote clarifying that RF front-ends are the hard limit would be beneficial.
2.  **Section IV-B (AoI):** The result that $p_{exc}=0.10$ leads to P99 AoI > 440s is excellent. However, the text mentions "mission-specific trade-off." It would be helpful to explicitly state that 440s is likely essentially useless for LEO collision avoidance (where conjunctions evolve rapidly), rendering this setting viable only for station-keeping, not safety.
3.  **Handoff Accounting:** The paper excludes handoff state transfers (10-50 MB) from the overhead metric $\eta$ because they use a "dedicated optical ISL." This is a valid architectural choice, but it implies a hardware requirement: every node must have a separate high-speed data plane distinct from the control plane. This hardware implication should be emphasized in the conclusion.
4.  **Fig. 6 (Latency Distribution):** The caption mentions an "analytical extrapolation" for the $10^6$ node curve. Please ensure this curve is visually distinct (e.g., dashed) to prevent confusion with DES-measured data.
5.  **Equation 10:** The power overhead calculation assumes the coordinator load is perfectly amortized ($15W / 100$). In reality, thermal subsystems must be sized for the *peak* load (20W), not the average. The text acknowledges this, but the equation might mislead a reader scanning for power budget impacts.

---

### Overall Recommendation
**Minor Revision**

The paper is of high quality and presents a rigorous characterization of a complex systems problem. The methodology is sound, and the results are valuable for the community. The revisions requested are primarily regarding the framing of the baselines and the justification of physical-layer assumptions, rather than requiring new simulation runs.

---

### Constructive Suggestions

1.  **Strengthen the Centralized Argument:** Instead of relying on the $M/D/1$ queue blow-up to disqualify centralized control, calculate the **aggregate spectrum required** to downlink full telemetry for $10^5$ nodes to ground stations. This is a much stronger, physics-based argument against centralization than server processing limits.
2.  **Refine the TDMA Discussion:** Add a paragraph in Section V (Discussion) specifically addressing the challenges of "Orbital TDMA." Acknowledge that while the simulation assumes slots are met, real-world implementation would likely require a dedicated time-sync protocol (like PTP adapted for high-delay links), which would eat into the $\gamma$ efficiency factor.
3.  **Visualize the "Design Envelope":** Figure 8 (Workload Comparison) is good, but a new figure plotting "Protocol Overhead vs. AoI" (combining the results of IV-B and IV-D) would be very powerful. It would visually demonstrate the Pareto frontier that system architects must navigate.
4.  **Sectorized Mesh Safety:** Explicitly state in the conclusion that the "Capped-fanout" sectorized mesh (fanout=10) is a heuristic that *lacks a safety proof*. This distinguishes it from the Hierarchical model (which has global aggregation) and the Global Mesh (which has full state).