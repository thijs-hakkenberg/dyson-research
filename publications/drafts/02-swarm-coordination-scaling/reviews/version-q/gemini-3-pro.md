---
paper: "02-swarm-coordination-scaling"
version: "q"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-24"
recommendation: "Minor Revision"
---

## Peer Review: IEEE Transactions on Aerospace and Electronic Systems

**Manuscript ID:** [Version Q]
**Title:** Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study
**Authors:** Project Dyson Research Team

---

### Review Criteria

**1. Significance & Novelty**
**Rating: 4 (Good)**
The manuscript addresses a timely and critical issue in aerospace engineering: the scalability of command and control architectures for mega-constellations and future large-scale swarms ($10^5$ nodes). While the concept of hierarchical control is not new, the specific contribution of quantifying the "protocol coefficient" ($\eta \approx 21\%$) and establishing hardware-sizing thresholds (e.g., the 50 kbps vs. 24 kbps coordinator link requirement) constitutes a significant engineering contribution. The distinction between the "Global-State Mesh" (upper bound) and the "Sectorized Mesh" (practical decentralized) adds necessary nuance to the distributed systems literature in this domain.

**2. Methodological Soundness**
**Rating: 4 (Good)**
The use of a cycle-aggregated Discrete Event Simulation (DES) is an appropriate choice for simulating $10^5$ nodes over year-long durations, where packet-level simulation (e.g., ns-3) would be computationally intractable. The authors are transparent about their abstraction level (message-passing layer) and explicitly list what is *not* modeled (MAC contention, physical link acquisition). The validation against closed-form analytical predictions (Section IV-E) is rigorous. However, the reliance on a 10-second coordination cycle ($T_c$) raises questions regarding the fidelity of collision avoidance latency modeling, which typically requires sub-second responsiveness.

**3. Validity & Logic**
**Rating: 4 (Good)**
The conclusions are generally well-supported by the data. The authors correctly identify that the $O(1)$ scaling of the hierarchical architecture is an analytical inevitability of their message model, focusing their analysis instead on the magnitude of the overhead and the queueing dynamics. The "Coordinator Bandwidth Stress Test" (Section IV-G) is logically sound and provides valuable constraints for radio subsystem design. A minor logical weakness exists in the presentation of the Centralized Baseline; while the text acknowledges parallelization ($M/D/c$), the graphical representation (Fig. 2) focuses on the single-server failure mode, which creates a somewhat "strawman" comparison against modern cloud-native ground systems.

**4. Clarity & Structure**
**Rating: 5 (Excellent)**
The manuscript is exceptionally well-written. The definitions of metrics (Section III-H) and traffic accounting (Table V) are precise, eliminating ambiguity regarding what is included in the overhead calculations. Figures are clear, and the separation of "delivered" vs. "offered" load in the availability analysis is a sophisticated distinction often missed in similar literature. The flow from architecture definition to simulation results to sensitivity analysis is logical and easy to follow.

**5. Ethical Compliance**
**Rating: 5 (Excellent)**
The authors include a specific disclosure regarding the use of AI for ideation (Section VI, Acknowledgment), which aligns with emerging transparency standards. No obvious conflicts of interest are apparent, assuming "Project Dyson" is a pseudonym for the review process.

**6. Scope & Referencing**
**Rating: 5 (Excellent)**
The paper fits squarely within the scope of *IEEE TAES*, bridging space systems engineering, communications, and autonomous control. The literature review covers relevant ground from swarm robotics (Brambilla) to satellite networking (Akyildiz, Handley), though it could benefit from more recent references on specific inter-satellite link (ISL) standards beyond CCSDS (e.g., SDA Transport Layer standards).

---

### Major Issues

1.  **Centralized Baseline Representation (Fig. 2):**
    Figure 2 shows the Centralized Ground Processing overhead diverging vertically at $N \approx 10^4$. While the text (Section III-B-1) fairly discusses $M/D/c$ queues and admits this is a "single-server parameterization," the visual representation is misleading. A reader skimming the paper might conclude that centralized control is mathematically impossible beyond 10,000 nodes, which is empirically false (Starlink manages ~7,000 nodes centrally today and is scaling up).
    *   *Requirement:* Please add a second curve to Figure 2 (or a shaded region) representing a parallelized ground system (e.g., $c=100$) to show that the bottleneck for centralized systems is actually spectrum/propagation, not processing. This would provide a fairer comparison.

2.  **Time Resolution of Collision Avoidance:**
    The simulation operates on a coordination cycle of $T_c = 10$ s. The text mentions that collision avoidance events are handled with "1-second resolution" via a priority queue. However, it is unclear how this interacts with the cycle-aggregated message passing. If a collision alert is generated at $t=1.5$ s, does it wait for the $t=10$ s cycle boundary to be "counted" and routed? If so, the latency analysis for safety-critical messages may be optimistic.
    *   *Requirement:* Clarify the temporal handling of priority messages within the cycle-aggregated framework. If they are batched into the 10s cycle, the limitations regarding time-critical collision avoidance must be stated more strongly.

3.  **Anonymity Check:**
    The manuscript cites "Project Dyson" and provides a URL (`https://projectdyson.org`). If this is a placeholder for the review process, it is acceptable. However, if this is a live URL that leads to the authors' identities or institution, it violates the double-blind review policy of IEEE TAES.
    *   *Requirement:* Ensure the URL and project name do not reveal author identity during the review phase.

---

### Minor Issues

1.  **Table VII (Coordinator Bandwidth):** The table lists "Drops (%)" and "Coord. Success (%)". These appear to be complements (summing to 100%). If so, one column is redundant. If they are distinct metrics, the difference should be explained.
2.  **Section IV-B (Cluster Size):** The text states overhead is "nearly invariant" to cluster size. It would be helpful to explicitly state *why* mathematically in this section (i.e., the dominant terms in the overhead equation are linear in $N$ and independent of $k_c$).
3.  **Reference Style:** Reference [1] and [3] are marked "non-archival; accessed February 2026". Please ensure the access dates are accurate to the current time of writing (2026 seems to be a future placeholder).
4.  **Fig 6 (Scaling Trajectory):** The "Analytical Extrapolation" to $10^6$ nodes is useful, but please mark the transition from "DES Validated" to "Extrapolated" clearly on the line itself (e.g., change line style from solid to dashed at $10^5$).

---

### Overall Recommendation

**Minor Revision**

The manuscript represents a high-quality contribution to the field of space systems engineering. The methodology is rigorous, and the results provide actionable design constraints for future constellation architects. The revisions requested are primarily regarding the presentation of the baseline comparisons to ensure fairness, and clarification of the temporal resolution for safety-critical events. Once these interpretative issues are addressed, the paper is well-suited for publication in *IEEE TAES*.

---

### Constructive Suggestions

1.  **Enhance the TDMA Discussion:** The finding that TDMA reduces the required coordinator link capacity from 50 kbps to 24 kbps is a high-impact result. Consider moving the "TDMA Scheduling Analysis" (currently Section IV-J) earlier, perhaps integrating it with the "Coordinator Bandwidth Stress Test" (Section IV-G), to consolidate the hardware sizing recommendations.
2.  **Physical Layer "Back-of-the-Envelope" Check:** In the Discussion, briefly calculate the link budget closure for the "50 kbps" requirement. Assuming standard optical ISL powers (which you list as 1-10 Gbps capability), this is trivial, but for an RF backup link (e.g., S-band or Ka-band inter-satellite), 50 kbps omnidirectional reception might drive antenna requirements. A brief sentence on this would strengthen the hardware implications.
3.  **Sectorized Mesh Visualization:** Figure 5 (Failure Resilience) compares Centralized, Global Mesh, and Hierarchical. Adding the "Sectorized Mesh" curve to this specific plot would be very valuable, as it likely represents the strongest "competitor" to the hierarchical approach in terms of robustness.