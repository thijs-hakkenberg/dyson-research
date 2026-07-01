---
paper: "02-swarm-coordination-scaling"
version: "bt"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-27"
recommendation: "Minor Revision"
---

## Peer Review: IEEE Transactions on Aerospace and Electronic Systems

**Manuscript ID:** [Version BT]
**Title:** Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms
**Reviewer Expertise:** Distributed Systems, Swarm Robotics, Discrete Event Simulation, Mega-constellation Operations

---

### 1. Significance & Novelty
**Rating: 4 (Good)**

The manuscript addresses a timely and critical issue in aerospace engineering: the scalability of command and control (C2) architectures for mega-constellations ($10^3$ to $10^5$ nodes). As commercial entities deploy constellations like Starlink and Kuiper, and future architectures propose autonomous swarms, the shift from centralized ground-in-the-loop control to autonomous hierarchical coordination is inevitable.

The primary contribution—a set of closed-form sizing equations for hierarchical coordination—is novel in its specific application to the bandwidth-constrained, high-latency space environment. The distinction between the three feasibility layers (Byte Budget, MAC Efficiency, and Airtime Scheduling) provides a valuable framework for system architects. The paper moves beyond generic "scalability" claims to provide concrete engineering values (e.g., the 24 kbps coordinator bottleneck), which is highly significant for practical system design.

### 2. Methodological Soundness
**Rating: 3 (Adequate)**

The methodological approach combines analytical derivation with a custom Cycle-Aggregated Discrete Event Simulation (DES). The mathematical derivations for the hierarchical overhead and TDMA frame sizing appear robust and are well-grounded in queueing theory and networking fundamentals.

However, there is a circularity in the validation strategy. The authors use a DES that implements the same message-layer logic as the analytical equations to "validate" those equations. As noted in Section V-A, this verifies implementation consistency (verification) rather than physical realism (validation). The agreement of $<0.1\%$ is expected because the simulation and the math share the same underlying assumptions. The lack of a packet-level simulation (e.g., NS-3 or OPNET) to test the MAC layer assumptions ($\gamma$) and physical layer effects (interference, capture effect) is a limitation, though the authors acknowledge this as future work.

Additionally, the Gilbert-Elliott (GE) model implementation assumes state coherence across the full coordination cycle ($T_c = 10s$). While this is justified as conservative for burst length, it simplifies the intra-cycle dynamics significantly.

### 3. Validity & Logic
**Rating: 4 (Good)**

The conclusions are generally well-supported by the data presented. The analysis of the "Stress Case" (unicast vs. broadcast commands) is logically sound and highlights a critical operational constraint often overlooked in high-level architecture papers. The finding that command traffic, rather than topology maintenance, dominates the bandwidth budget during reconfiguration is a valuable insight.

A logical weakness exists in the comparison baselines. The "Centralized Ground Processing" baseline models the ground station as an M/D/1 queue limited by server CPU processing ($\mu_s$). In reality, centralized C2 for mega-constellations is limited by uplink spectrum availability, contact time windows, and ground station antenna availability, not server compute cycles. By focusing on compute latency, the paper sets up a "strawman" comparison that doesn't reflect the actual bottleneck of centralized architectures.

### 4. Clarity & Structure
**Rating: 5 (Excellent)**

The manuscript is exceptionally well-written. The structure is logical, moving from problem definition to model description, results, and discussion. The distinction between the three "feasibility layers" is a strong pedagogical device that clarifies the complex interaction between bandwidth and time.

The tables are dense but highly informative, particularly Table VI (TDMA Superframe Time Budget) and Table VIII (Workload Feasibility). The notation is consistent, and the abstract accurately summarizes the key quantitative findings. The writing style is concise and appropriate for *IEEE TAES*.

### 5. Ethical Compliance
**Rating: 5 (Excellent)**

The authors provide a clear acknowledgment of AI-assisted ideation in the Acknowledgments section, citing specific models used. This transparency is commendable and aligns with emerging publication standards. There are no apparent conflicts of interest or ethical concerns regarding the research content.

### 6. Scope & Referencing
**Rating: 4 (Good)**

The paper fits squarely within the scope of *IEEE TAES*, specifically the areas of Space Systems and Command & Control. The referencing is adequate, covering foundational texts (Kleinrock, Lynch), historical space systems (Iridium), and modern developments (Starlink, Kuiper).

The paper would benefit from tighter integration with the Delay/Disruption Tolerant Networking (DTN) literature. While CCSDS BPv7 is mentioned, the specific challenges of hierarchical routing in DTN (e.g., Contact Graph Routing in a hierarchy) are relevant context for the "Regional" and "Cluster" coordinator logic.

---

### Major Issues

1.  **Verification vs. Validation Distinction:**
    The paper claims the DES "validates" the analytical equations (e.g., Abstract, Section IV-F). Since the DES and the equations share the same message-layer abstractions and assumptions (e.g., fluid server approximation, deterministic processing times), this is *verification* (checking the math is solved correctly), not *validation* (checking the math represents reality).
    *   *Requirement:* Please rephrase instances of "validation" to "verification" or "consistency check" throughout the text, specifically regarding the DES results. Explicitly state that physical-layer validation (MAC contention, hidden nodes) remains an open challenge.

2.  **The 1 kbps Constraint Justification:**
    The entire analysis hinges on the 1 kbps per-node bandwidth constraint. The authors argue this is the "design-driving edge case" for RF backup. However, modern S-band transceivers for CubeSats often achieve 10-100 kbps even with omni-directional antennas. If the budget is raised to 10 kbps, Table II shows that all constraints vanish.
    *   *Requirement:* Provide a stronger justification for the 1 kbps limit. Is this based on a specific link budget calculation (e.g., worst-case tumbling mode, low-gain antenna, max slant range)? Without this context, the constraint feels artificial to force the optimization problem.

3.  **Centralized Baseline Model:**
    Section III-B-1 models the centralized baseline using an M/D/1 queue where $\mu_s$ is processing capacity. This implies the limit of centralized control is CPU power.
    *   *Requirement:* The authors must acknowledge that the primary bottleneck for centralized control is *spectrum and contact availability*, not ground processing. The current comparison (Fig. 11) suggests centralized architectures scale infinitely if you just add more CPUs ($c=N/k_c$), which is misleading regarding the actual constraints of ground-based C2.

---

### Minor Issues

1.  **Table I (Notation):** The symbol $S_{\text{eph}}$ is defined as "Status report size," but the text often refers to "ephemeris." Ensure terminology is consistent (Status Report vs. Ephemeris).
2.  **Equation 7 ($\gamma$ derivation):** The derivation assumes perfect slot alignment. In a distributed swarm, guard times must account for clock drift between synchronization events. The text mentions GNSS, but in GNSS-denied environments, drift could be significant. A brief mention of the required clock stability to maintain $\gamma=0.949$ would be beneficial.
3.  **Section IV-A (Coordinator Capacity):** The text mentions "Model A" and "Model B" for random-phase arrivals. It would be helpful to explicitly state that these are standard queueing approximations (e.g., G/D/1) if applicable, or clarify if they are custom derivations.
4.  **Fig. 4 (AoI):** Clarify in the caption whether the AoI curves represent the average AoI across the fleet or the AoI of a specific worst-case node.
5.  **Typos:**
    *   Section III-B-2: "RequestVote: 100 B broadcast... quorum = 51 responders required." Ensure the distinction between "responders" and "votes" is clear in the context of Raft.

---

### Overall Recommendation
**Minor Revision**

The manuscript represents a high-quality contribution with significant practical utility for space system architects. The mathematical framework is sound, and the results are presented with exceptional clarity. The requested revisions are primarily regarding the framing of the validation (verification vs. validation), the justification of the boundary conditions (1 kbps), and the realism of the centralized baseline comparison. These changes will strengthen the paper's rigor without requiring new simulation runs.

---

### Constructive Suggestions

1.  **Add a Link Budget Calculation:** To justify the 1 kbps constraint, add a small sidebar or appendix with a link budget (Transmit Power, Path Loss at 1000km, Noise Floor, Antenna Gain) showing that 1 kbps is indeed the physical limit for a tumbling satellite on an S-band backup link. This grounds the math in physics.
2.  **Refine the "Centralized" Comparison:** Instead of comparing against an M/D/1 CPU queue, compare against a "Uplink Capacity" limit. For example, assume a ground station has $X$ Mbps of uplink bandwidth. This would show that centralized architectures saturate due to spectrum, while hierarchical ones saturate due to coordinator cross-links.
3.  **Sensitivity to $\gamma$:** Since $\gamma$ (MAC efficiency) is a proxy for all unmodeled physical layer effects, consider adding a plot showing "Max Feasible Fleet Size vs. $\gamma$." This would allow readers to determine feasibility based on their own MAC implementation performance.
4.  **Clarify "Static Topology":** Add a sentence or two explaining *why* the static topology assumption holds for the bandwidth analysis. Explicitly state that while node IDs change during handoffs, the *number* of nodes per cluster ($k_c$) remains roughly constant, preserving the validity of the bandwidth sizing equations.