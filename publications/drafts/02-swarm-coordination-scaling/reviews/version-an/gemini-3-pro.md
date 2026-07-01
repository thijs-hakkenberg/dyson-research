---
paper: "02-swarm-coordination-scaling"
version: "an"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-27"
recommendation: "Minor Revision"
---

**IEEE Transactions on Aerospace and Electronic Systems**
**Peer Review Report**

**Manuscript ID:** [Version AN]
**Title:** Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study
**Authors:** Project Dyson Research Team

---

### 1. Significance & Novelty
**Rating: 4**

This manuscript addresses a timely and critical gap in the literature: the scalability of the *control plane* for mega-constellations and large-scale autonomous swarms ($10^3$–$10^5$ nodes). While significant prior work exists on data-plane routing (ISL topology) and small-scale swarm robotics ($<100$ agents), there is a paucity of rigorous analysis on the transition regime where centralized ground control becomes untenable but fully distributed mesh approaches saturate bandwidth.

The novelty lies not in the proposal of hierarchical coordination itself (a standard distributed systems pattern), but in the rigorous *characterization* of this architecture under specific space-domain constraints—specifically, the "RF-backup" regime of 1 kbps/node. The definition of the "workload design envelope" (spanning 5% to 46% overhead) provides a valuable parametric reference for system architects. The analysis of how Gilbert-Elliott (GE) link losses interact with coordinator queueing is a specific, high-value contribution.

### 2. Methodological Soundness
**Rating: 4**

The methodology is generally robust. The choice of a cycle-aggregated Discrete Event Simulation (DES) is appropriate for the scale ($10^5$ nodes) where packet-level simulation would be computationally prohibitive. The authors have done an excellent job of validating the simulation against closed-form analytical models (M/D/1, geometric distributions), which builds confidence in the results.

However, the abstraction of the Physical/MAC layer into a simple efficiency factor ($\gamma$) and a capacity limit is a significant simplification. While the "Physical-layer vignette" in Section IV-A attempts to ground this, the assumption that 100 nodes can close a TDMA loop with 15% guard time overhead relies heavily on precise synchronization that is non-trivial in orbit. Additionally, the independence of GE losses and coordinator saturation (Section IV-D) is heavily dependent on the assumption of point-to-point optical ISLs; this conclusion would likely collapse under a shared-medium RF assumption.

### 3. Validity & Logic
**Rating: 5**

The conclusions are logically derived from the data presented. The authors are careful to distinguish between "offered" and "delivered" load, which is crucial when analyzing saturation regimes. The "dual-regime" interpretation (Section IV-F)—clarifying that the 1 kbps constraint is a worst-case backup mode while nominal optical operations have ample headroom—is vital for the validity of the study; without this context, the overhead figures would appear alarmingly high for modern systems.

The comparison against baselines is fair. The authors explicitly state that the centralized single-server model and the global-state mesh are "intentional bounds," preventing straw-man arguments. The introduction of the "Sectorized Mesh" provides a necessary and realistic intermediate comparator.

### 4. Clarity & Structure
**Rating: 5**

The manuscript is exceptionally well-written and organized. The definition of metrics (Section III-H) and traffic accounting (Table VI) is precise, eliminating ambiguity regarding what is included in the overhead $\eta$. The "Roadmap" provided at the beginning of Section IV is helpful for navigating the results. Figures are high-quality, particularly the overhead scaling trajectory (Fig. 9) and the workload comparison (Fig. 7).

### 5. Ethical Compliance
**Rating: 5**

The authors provide a clear Acknowledgment regarding the use of AI tools (Claude, Gemini, GPT) for ideation, which aligns with emerging transparency standards. Data availability is addressed with a link to a repository (noted as a placeholder for the review). No human subjects or hazardous materials are involved.

### 6. Scope & Referencing
**Rating: 5**

The paper fits squarely within the scope of *IEEE TAES*, bridging space systems engineering, communications, and autonomous control. The references are comprehensive, covering foundational distributed systems theory (Lynch, Lamport), space networking (CCSDS, DTN), and current constellation operations (Starlink, OneWeb).

---

### Major Issues

1.  **Conditional Independence of GE Loss and Saturation (Section IV-D):**
    The finding that "GE retransmissions and coordinator ingress saturation are independent failure modes" is presented as a general result. However, this is strictly an artifact of the *point-to-point* ISL topology modeled. In many swarm concepts, intra-cluster communication utilizes a shared RF medium (e.g., omnidirectional S-band) to reduce pointing requirements. In a shared medium, retransmissions *would* consume channel capacity and increase collision probability, directly coupling loss to saturation. The manuscript must explicitly qualify this finding. It currently reads as a fundamental property of the hierarchy, rather than a property of the specific physical layer topology chosen.

2.  **Latency vs. Conjunction Assessment:**
    In Section IV-B, the paper links Age of Information (AoI) to position uncertainty ($\sigma_{pos} \approx 230$ m). While the authors caveat this as an "order-of-magnitude input," there is a risk of over-claiming. A 230m along-track error is massive for collision avoidance. The paper should clarify that this architecture likely supports *coarse* screening (identifying pairs for scrutiny), but that *fine* screening and maneuver decisions likely require a different mechanism (e.g., direct node-to-node negotiation or on-demand precision tracking) that bypasses the periodic reporting loop. The current text implies the hierarchical loop might be sufficient for safety, which is debatable at 440s latency.

### Minor Issues

1.  **Table II (Simulation Parameters):** The "Collision avoidance rate" is listed as $10^{-4}$/node/s. The footnote explains this includes screening alerts, not just maneuvers. However, this rate seems high for a background process and low for a crisis. A brief justification or citation for this specific event frequency density would strengthen the workload model.
2.  **Figure 6 (Phase Stagger):** The caption mentions "overhead is unaffected by scheduling mode." This is intuitive (same bytes), but worth explicitly stating in the text that scheduling changes *drops*, not *overhead*.
3.  **Equation 11 (AoI Analytic):** Please verify the ceiling function usage. If the result is 43.7 cycles, the P99 is the 44th cycle. The notation is correct, but the text "matching... within one cycle" could be tightened to "matching exactly due to discrete time steps."
4.  **Section IV-H (Duty Cycle):** The power variance calculation assumes uncorrelated rotation schedules across clusters. If the fleet is deployed in a synchronized manner, could all clusters rotate coordinators simultaneously, causing a fleet-wide power dip? A note on randomized initialization of duty cycles would address this.
5.  **Typos/Formatting:**
    *   Section III-B: "The simulation is *not* a per-packet or per-bit DES..." - This is stated clearly, but later in Section IV-A, the text discusses "byte-level traffic accounting." Ensure consistent terminology so readers don't confuse "byte-level accounting" with "byte-level simulation."

### Overall Recommendation
**Minor Revision**

The manuscript represents a solid contribution to the field of space systems engineering. The simulation framework is rigorous, and the results provide valuable sizing rules for future constellation architects. The requested revisions are primarily regarding the scoping of claims (specifically the independence of loss/saturation) and clarifying the operational implications of the latency results. No new simulation runs are required, but the text needs to be tightened to avoid over-generalization of the specific topology modeled.

### Constructive Suggestions

1.  **Refine the "Independence" Claim:** In the Abstract and Section IV-D, change "compose independently" to "compose independently under point-to-point ISL architectures." Add a sentence in the Discussion contrasting this with shared-medium RF scenarios where contention would couple these factors.
2.  **Strengthen the Physical Layer Caveat:** In Section V-B (Limitations), explicitly list "Shared-medium contention" as a limitation. The current text mentions "MAC-layer scheduling," but distinguishing between *scheduling* (TDMA) and *contention* (CSMA) is vital for the validity of the overhead results.
3.  **Clarify Conjunction Operations:** In Section IV-B, explicitly state that the 440s AoI is suitable for *strategic* deconfliction (days to hours out) but that *tactical* collision avoidance (seconds to minutes) must rely on the direct node-to-node links (which are modeled but distinct from the hierarchical reporting loop).
4.  **Visualizing the Envelope:** Consider adding a shaded region to Figure 9 representing the "Design Envelope" (the area between the Nominal and Stress curves), labeling it as the "Operational Control Plane Capacity." This would visually reinforce the main sizing contribution.