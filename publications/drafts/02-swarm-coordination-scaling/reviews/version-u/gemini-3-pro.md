---
paper: "02-swarm-coordination-scaling"
version: "u"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-24"
recommendation: "Minor Revision"
---

# Peer Review: IEEE Transactions on Aerospace and Electronic Systems

**Manuscript ID:** [Version U]
**Title:** Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study
**Authors:** Project Dyson Research Team

---

## Review Criteria

### 1. Significance & Novelty
**Rating: 5 (Excellent)**

This manuscript addresses a critical and timely gap in the aerospace engineering literature: the transition from ground-controlled constellations (currently $10^3$ nodes, e.g., Starlink) to fully autonomous, space-coordinated swarms ($10^5+$ nodes). While the literature is rich in swarm robotics (small scale) and networking routing (large scale), there is a distinct lack of systems engineering analysis that quantifies the *control plane* overhead for mega-constellations.

The novelty lies in the rigorous application of Age-of-Information (AoI) metrics to the spacecraft telemetry problem and the comparative analysis of hierarchical vs. sectorized mesh architectures under explicit byte-level constraints. The quantification of the "design envelope" (spanning 5% to 46% overhead) provides actionable data for system architects. This work is highly relevant to the scope of *IEEE TAES*.

### 2. Methodological Soundness
**Rating: 4 (Good)**

The use of a cycle-aggregated Discrete Event Simulation (DES) is an appropriate choice for simulating $10^5$ nodes; a packet-level simulation would be computationally intractable for year-long operational timelines. The authors are transparent about their abstraction level (message-passing layer vs. PHY/MAC layer). The inclusion of the "Sectorized Mesh" as a comparator significantly strengthens the methodology, moving beyond the strawman "Global Mesh" used in previous iterations of similar work.

However, the reliance on a generic MAC efficiency factor ($\gamma$) and the abstraction of link acquisition/pointing dynamics is a limitation. While the "Coordinator Bandwidth Stress Test" (Section IV-G) cleverly proxies for ALOHA-like contention via random phasing, the paper would benefit from a more explicit discussion of how specific MAC protocols (e.g., TDMA vs. CSMA/CA) would alter the effective overhead beyond a simple scalar multiplier.

### 3. Validity & Logic
**Rating: 4 (Good)**

The conclusions are generally well-supported by the data. The analytical cross-check (Section IV-E) validating the DES results against closed-form traffic accounting is a strong indicator of internal validity. The distinction between "offered load" and "delivered overhead" in the link availability analysis is handled with necessary rigor.

A minor logical weakness exists in the "Stress Case" workload definition. The assumption that *every* node receives a unique 512-byte command *every* cycle (10s) drives the high overhead result (46%). In reality, station-keeping maneuvers are infrequent. While the authors acknowledge this is a "conservative upper bound," the prominence of the 46% figure might mislead readers about typical operational costs. The "Nominal" profile (5%) is likely the true steady state.

### 4. Clarity & Structure
**Rating: 5 (Excellent)**

The manuscript is exceptionally well-written. The definitions of metrics (Section III-G) are precise, and the distinction between "baseline telemetry" and "protocol overhead" is maintained consistently. Figures are informative, particularly Fig. 5 (Cluster Size Optimization) and Fig. 12 (Workload Comparison). The abstract is dense but accurate.

### 5. Ethical Compliance
**Rating: 5 (Excellent)**

The authors provide a clear acknowledgment of AI-assisted ideation in the Acknowledgment section, complying with emerging publication standards. No human subjects are involved. The research appears ethically sound.

### 6. Scope & Referencing
**Rating: 5 (Excellent)**

The paper fits perfectly within the scope of *IEEE TAES*, specifically the areas of Space Systems and Command & Control. The bibliography is robust, bridging classical queueing theory (Kleinrock), distributed algorithms (Lynch, Lamport), and modern satellite networking (Handley, Akyildiz). The inclusion of AoI literature (Kaul, Yates) is particularly welcome.

---

## Major Issues

**1. MAC Layer Abstraction vs. Congestion Reality**
While the cycle-aggregated DES is necessary for scale, the abstraction of the MAC layer into an efficiency factor ($\gamma$) and a random-phase arrival model risks understating the non-linear effects of congestion. In a real optical ISL or RF mesh, as utilization approaches 67% (the total utilization cited in Section IV-F), contention delays in random-access protocols often grow exponentially, not linearly.
*   **Critique:** The paper relies on the "Coordinator Bandwidth Stress Test" to show that 50 kbps is needed for zero drops. However, this assumes a drop-tail queue based on byte limits. It does not model the *stochastic collision* of packets in the time domain if the MAC is not perfectly TDMA.
*   **Requirement:** The authors should expand the discussion in Section V-E (Limitations) to explicitly state that the linear scaling results assume a collision-free schedule (TDMA) or sufficient over-provisioning to avoid the ALOHA cliff. The claim of "Queue stability confirmation" (Section IV-D) is valid for the *message* queues, but perhaps not for the *channel* access if it were modeled at the packet layer.

**2. Justification of the "Stress Case" Workload**
The headline result of $\eta \approx 46\%$ is derived from the "Stress Case" (Profile S), which assumes every node receives a 512-byte command every 10 seconds.
*   **Critique:** For a constellation of $10^5$ satellites, this implies $10^4$ commands per second globally. This is orders of magnitude higher than current station-keeping requirements. By dominating the abstract and conclusion with this 46% figure, the paper paints an overly pessimistic view of hierarchical efficiency.
*   **Requirement:** The Abstract and Conclusion should balance the 46% figure more equally with the "Nominal" (5%) and "Event-Driven" (6%) figures. The 46% should be framed clearly as a "theoretical saturation point" rather than an expected operational cost.

---

## Minor Issues

1.  **Table I (Sim Params):** The "Collision avoidance rate" is listed as $10^{-4}$/node/s. This seems high for actual maneuvers but appropriate for *screening alerts*. The footnote clarifies this, but it might be helpful to explicitly label it "Screening Alert Rate" in the table body to avoid confusion with physical maneuver rates.
2.  **Figure 6 (Latency Distribution):** The curve for $10^6$ nodes is labeled as an "analytical extrapolation." Please ensure the caption or legend visually distinguishes this curve (e.g., dotted line) from the DES-validated curves to prevent readers from assuming $10^6$ nodes were simulated directly.
3.  **Section IV-G (Coordinator Bandwidth):** The distinction between "Unscheduled" (50 kbps) and "TDMA" (24 kbps) is excellent. However, the text mentions "Doppler compensation" as part of the overhead. For optical ISLs, Doppler is usually handled by the transceiver hardware/DSP, not the MAC frame overhead. Please verify if this inclusion in $\gamma$ is appropriate.
4.  **Equation 10 (Analytical Cross-check):** The equation is helpful, but the term $N(1-1/k_c)$ appears twice. It might be cleaner to factor out the common terms for readability.
5.  **Typos:**
    *   Section III-A: "Pollaczek–Khinchine formula" - check spelling (Khintchine is also common, just be consistent).
    *   Table IV: Check the footnote referencing "Protocol offered load alone" - the phrasing is slightly convoluted.

---

## Overall Recommendation
**Minor Revision**

The manuscript is technically sound, novel, and well-presented. The simulation framework is robust for the questions asked. The primary revisions required are regarding the framing of the results (balancing the "Stress Case" vs. "Nominal" case) and a more explicit discussion of the limitations regarding MAC-layer contention. These can be addressed without running new simulations.

---

## Constructive Suggestions

1.  **Refine the Abstract:** Explicitly state the "Nominal" overhead (5%) alongside the "Stress Case" (46%) in the first sentence of the results. This gives a more accurate picture of the architecture's efficiency for 99% of the mission duration.
2.  **Enhance the MAC Limitation Discussion:** In Section V-E, add a sentence acknowledging that while the message-layer queues are stable, physical layer protocols (like Slotted ALOHA) would likely suffer congestion collapse at 67% utilization, thereby enforcing a requirement for TDMA or Reservation-based MACs for this architecture to work.
3.  **AoI Operational Context:** In Section IV-F (AoI), briefly discuss *why* a 400s staleness (at $p_{exc}=0.10$) might be acceptable. For example, cite the typical propagation time of covariance errors or the decision timeline for conjunction assessment (usually hours/days, not seconds). This validates that the 5% overhead mode is actually usable.
4.  **Visualizing the "Design Envelope":** Consider adding a shaded region to Figure 12 (Workload Comparison) that highlights the "Likely Operational Zone" between the Nominal and Event-Driven curves, distinguishing it from the theoretical Stress Case ceiling.