---
paper: "02-swarm-coordination-scaling"
version: "j"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-23"
recommendation: "Minor Revision"
---

## Peer Review Report

**Journal:** IEEE Transactions on Aerospace and Electronic Systems
**Manuscript ID:** [Version J]
**Title:** Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study
**Reviewer Expertise:** Distributed Systems, Swarm Robotics, Discrete Event Simulation, Mega-constellation Operations

---

### 1. Significance & Novelty
**Rating: 5**

This manuscript addresses a timely and critical gap in aerospace systems engineering: the coordination of "mega-constellations" in the $10^4$ to $10^6$ node regime. While current literature covers small swarms ($<100$ nodes) and traditional constellations ($<10^4$ nodes), the intermediate regime remains under-explored. The paper’s focus on quantifying the specific overhead costs of hierarchical architectures versus centralized and mesh baselines is highly relevant to operators like Starlink, Kuiper, and future sovereign space infrastructure. The parameterization of coordinator bandwidth and the duty cycle trade-off analysis provide novel, actionable design guidelines.

### 2. Methodological Soundness
**Rating: 4**

The Discrete Event Simulation (DES) framework appears robust. The authors have taken care to validate their simulation against analytical models (Pollaczek–Khinchine for queues, gossip bounds for mesh). The use of Monte Carlo methods with bootstrapping for confidence intervals is appropriate given the stochastic nature of node failures and message timing.

However, a methodological weakness lies in the **Centralized Baseline parameterization**. The authors use a single-server ($c=1$) model as the primary baseline. While they acknowledge this is a "worst-case bound," it creates a "strawman" comparison. A constellation of $10^5$ satellites would undoubtedly utilize a distributed ground server cluster ($c \gg 1$). While the paper discusses $M/D/c$ sensitivity in text (Table I), the graphical comparisons (e.g., Fig. 2) rely on the single-server failure mode, which exaggerates the relative benefit of the hierarchical model regarding *processing* latency, even if propagation latency remains the hard constraint.

### 3. Validity & Logic
**Rating: 4**

The conclusions are generally well-supported by the data. The identification of the optimal cluster size ($k_c \approx 100$) is logically derived from the trade-off between inter-cluster traffic and intra-cluster management costs.

There is, however, a tautological aspect to the "scaling finding." The authors claim the $O(1)$ overhead percentage is a key finding. Mathematically, if the architecture is defined such that message volume scales linearly with $N$ (Eq. 5) and total system bandwidth also scales linearly with $N$ (1 kbps/node), the ratio $\eta$ *must* be constant by construction. The simulation validates that second-order effects (queuing) do not disrupt this, which is valuable, but the "constant scaling" itself is an analytical inevitability rather than an emergent simulation discovery. The *value* of the constant ($\approx 21\%$) is the true contribution.

### 4. Clarity & Structure
**Rating: 5**

The manuscript is exceptionally well-written. The structure is logical, moving from architecture definitions to simulation setup, results, and discussion. The distinction between "Baseline Telemetry" and "Protocol Overhead" is crucial and well-explained. Figures are clear, and the "Traffic Accounting" table (Table III) is a best-practice inclusion that greatly aids reproducibility.

### 5. Ethical Compliance
**Rating: 5**

The authors provide a clear acknowledgment of AI-assisted ideation in the Acknowledgments section, citing specific models used for brainstorming. This transparency meets and exceeds current ethical standards for AI disclosure. No conflicts of interest are apparent.

### 6. Scope & Referencing
**Rating: 5**

The paper fits squarely within the scope of *IEEE TAES*. It bridges the gap between pure networking theory and orbital systems engineering. The references are comprehensive, covering historical foundations (O'Neill), classical distributed theory (Lamport, Lynch), and modern constellation literature (Handley, del Portillo).

---

### Major Issues

1.  **The "Strawman" Centralized Baseline:**
    In Section III-B-1 and Figure 2, the centralized baseline is capped at $N \approx 10^4$ due to the saturation of a single server ($c=1$). This is an unrealistic constraint for a system of this magnitude. A ground segment for 100,000 satellites would employ hyperscale cloud compute.
    *   *Requirement:* The authors should either (a) plot an $M/D/c$ curve in Figure 2 with a realistic $c$ (e.g., $c=100$) to show where the *bandwidth* or *propagation* limits kick in, rather than the processing limit, or (b) explicitly label the curve in Figure 2 as "Single-Server Centralized" to avoid misleading readers about the viability of ground processing. The current presentation implies centralized control fails at $10^4$ nodes due to CPU limits, which is not strictly true.

2.  **Physical Layer Abstraction Risks:**
    The simulation assumes a "1 kbps coordination channel" and abstracts away MAC-layer contention, link acquisition times, and pointing dynamics. In a dense swarm with $k_c=100$, 100 nodes trying to talk to one coordinator within $T_c=10s$ creates significant TDMA scheduling overhead or CSMA collisions.
    *   *Requirement:* The authors must expand the "Limitations" section or the "Coordinator Bandwidth" section to discuss the *spectral efficiency* penalty. The 25 kbps requirement for the coordinator (Section IV-G) assumes perfect scheduling. A "MAC efficiency factor" (e.g., Slotted ALOHA efficiency or TDMA guard bands) should be applied to the overhead calculations to provide a more realistic engineering margin.

3.  **Tautological Scaling Claim:**
    As noted in "Validity," the claim that "Hierarchical coordination... maintains a constant overhead percentage" is presented as a simulation result. This is an analytical property of the tree structure.
    *   *Requirement:* Rephrase the contribution. The simulation does not *discover* the $O(1)$ scaling; it *quantifies the constant factor* ($\eta \approx 21\%$) and *confirms* that queueing dynamics do not diverge from the analytical prediction. This distinction is subtle but important for academic rigor.

---

### Minor Issues

1.  **Collision Rate Justification:** In Table II, the collision avoidance rate is $10^{-4}$/node/s. This seems high (approx. 8 events per day per satellite). While the text explains this includes "screening alerts," a citation for this specific rate of screening events in dense shells (e.g., from Starlink or ESA data) would strengthen the parameter selection.
2.  **Figure 5 (Latency):** The $10^6$-node curve is labeled as an "analytical extrapolation." Please ensure the caption or legend clearly distinguishes this from the DES-generated data to prevent confusion.
3.  **Sectorized Mesh:** The discussion in V-C is excellent. However, the paper compares Hierarchical against "Global-State Mesh" (an upper bound). It would be beneficial to explicitly state in the Abstract or Conclusion that a "Sectorized Mesh" is the true competitive architecture that remains to be studied, preventing the reader from thinking Hierarchical is the *only* solution.
4.  **Equation 11:** The power overhead calculation assumes linear scaling. Is there a base power cost for activating the high-bandwidth transmitter regardless of throughput? (e.g., warm-up time). If so, the power cost might be slightly higher. A brief comment is sufficient.

---

### Overall Recommendation
**Minor Revision**

The manuscript represents a high-quality contribution to the field of large-scale space systems. The simulation is rigorous, and the results are valuable for future constellation architects. The required revisions are primarily regarding the framing of the baselines (to avoid strawman comparisons) and a more precise articulation of the scaling findings (quantification vs. discovery). Addressing the physical layer abstractions with slightly more detail will align the paper with the rigorous standards of *IEEE TAES*.

---

### Constructive Suggestions

1.  **Add a "Realistic Ground" Curve:** In Figure 2, add a dashed line representing a centralized system with infinite processing power ($c \to \infty$) but limited by the 205 Mbps uplink spectrum constraint mentioned in the text. This would show the *physical* limit of centralized control, which is a much stronger argument than the *processing* limit.
2.  **MAC Overhead Factor:** Introduce a parameter $\gamma$ (MAC efficiency, e.g., 0.8 for TDMA) into the overhead calculation in Section IV-G. This would make the "25 kbps" requirement more robust: $C_{req} = \frac{25 \text{ kbps}}{\gamma}$.
3.  **Refine Abstract:** Change "We establish... centralized baseline saturates at $N=10^4$" to "We establish... single-server centralized baseline saturates..." to be precise.
4.  **Highlight the "Exception" Result:** The reduction from 21% to 2.5% overhead via exception-based telemetry is arguably the most impactful engineering result for practitioners. Consider moving this up in the conclusion or highlighting it more visually in the figures (perhaps an arrow in Fig 6).