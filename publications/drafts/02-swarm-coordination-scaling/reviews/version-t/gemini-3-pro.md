---
paper: "02-swarm-coordination-scaling"
version: "t"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-24"
recommendation: "Minor Revision"
---

# Peer Review: IEEE Transactions on Aerospace and Electronic Systems

**Manuscript ID:** [Version T]
**Title:** Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study
**Authors:** Project Dyson Research Team

---

### 1. Significance & Novelty
**Rating: 5**

This manuscript addresses a critical and rapidly emerging problem in aerospace engineering: the command and control (C2) scalability of mega-constellations and future autonomous swarms. As commercial entities (Starlink, Kuiper) push constellation sizes into the tens of thousands, and future concepts envision millions of nodes, the transition from human-in-the-loop ground control to autonomous distributed coordination is inevitable.

The novelty lies in the specific gap the authors address. While swarm robotics literature covers small scales ($N < 100$) and networking literature covers routing protocols, there is a lack of rigorous systems engineering analysis for the $10^3$ to $10^5$ node regime that explicitly accounts for byte-level protocol overhead. The introduction of the "Sectorized Mesh" as an intermediate comparator between the hierarchical architecture and the theoretical global-mesh upper bound is a significant contribution that adds realism to the trade space. The quantification of Age-of-Information (AoI) costs associated with exception-based telemetry is also a high-value contribution for system architects.

### 2. Methodological Soundness
**Rating: 4**

The methodology relies on a cycle-aggregated Discrete Event Simulation (DES). This is an appropriate choice for the scale of the problem ($10^5$ nodes), as packet-level simulation would be computationally prohibitive. The authors are transparent about their abstraction level (Table III), clearly delineating what is modeled (message passing, queueing) versus what is abstracted (MAC layer, link acquisition). The traffic accounting (Table IV) is rigorous, and the "Validation Cross-Check" against analytical models (Section IV-E) provides confidence in the implementation.

However, a rating of 4 is given rather than 5 due to the abstraction of the Physical/MAC layer. The authors claim "no queueing-induced nonlinearities," but in wireless/optical networks, nonlinearities often arise from medium contention (CSMA collisions or TDMA slot exhaustion) rather than message-layer processing queues. While the authors attempt to capture this via the $\gamma$ (MAC efficiency) parameter and the coordinator bandwidth stress test, the absence of a contention model means the simulation represents a "best-case" flow. The results are valid as *offered load* characterizations, but the link performance conclusions should be qualified.

### 3. Validity & Logic
**Rating: 4**

The conclusions are generally well-supported by the data. The authors do an excellent job of nuance regarding the "Centralized" baseline. Rather than setting up a strawman argument based on processing capacity (which they acknowledge is solvable via parallelization), they correctly identify propagation latency and uplink spectrum scarcity as the true hard limits of centralized control.

The logic regarding the "Sectorized Mesh" is sound; by capping fanout, they demonstrate that mesh architectures can scale, but at a higher overhead cost (${\sim}1.5\times$) than hierarchical approaches due to the lack of aggregation.

One logical tension exists in the "1 kbps/node" bandwidth constraint. The authors state this is a "traffic budget" from a Gbps optical link. If the physical link is Gbps, serialization delay is negligible (as noted). However, treating the budget as a hard constraint for *drops* (in the Coordinator Bandwidth section) implies a bottleneck. If the bottleneck is artificial (a budget) rather than physical (link capacity), the "drops" are a policy decision, not a physical failure. This distinction needs sharper articulation.

### 4. Clarity & Structure
**Rating: 5**

The manuscript is exceptionally well-written. The structure is logical, moving from architecture definitions to simulation setup, results, and sensitivity analysis. The use of tables is effective, particularly Table IV (Traffic Accounting) and Table VII (Link Availability), which allow for easy reproducibility. The distinction between "Baseline Telemetry" (topology-invariant) and "Protocol Overhead" is crucial and clearly maintained throughout. The abstract is quantitative and accurate.

### 5. Ethical Compliance
**Rating: 5**

The authors include a specific acknowledgment regarding the use of AI tools (Claude, Gemini, GPT) for ideation, citing a companion methodology paper. This meets and exceeds current transparency standards. No obvious conflicts of interest or ethical lapses regarding data fabrication are apparent.

### 6. Scope & Referencing
**Rating: 5**

The paper is perfectly scoped for *IEEE TAES*. It bridges the gap between pure networking theory and orbital systems engineering. The references are comprehensive, covering historical foundations (O'Neill, Reynolds), standard texts (Wertz/SMAD), and current operational context (Starlink, Kuiper). The inclusion of recent work on Graph Neural Networks (GNNs) and Mean Field Games acknowledges the theoretical frontier while focusing the paper on practical engineering parameters.

---

### Major Issues

1.  **Physical Layer Abstraction vs. Stability Claims:**
    In Section IV-E, the authors claim the DES confirms "queue stability... no queueing-induced nonlinearities." This is circular. The simulation models message generation and FIFO processing queues. It does *not* model the stochasticity of link acquisition, pointing errors, or MAC contention (beyond a static efficiency factor $\gamma$). Therefore, the "stability" observed is a property of the deterministic message generation model, not the physical network.
    *   *Requirement:* The authors must rephrase these claims to specify that *message-layer* queues are stable. They should explicitly state that physical-layer instability (e.g., congestion collapse in CSMA, synchronization loss in TDMA) remains an unmodeled risk that could introduce the nonlinearities they claim are absent.

2.  **The "1 kbps" Constraint Justification:**
    The assumption of a 1 kbps/node coordination budget is central to the overhead metrics ($\eta$). However, with modern Optical Inter-Satellite Links (OISLs) operating at 1-10 Gbps, a 1 kbps budget seems artificially low (0.0001% of capacity).
    *   *Requirement:* The authors need to better justify this constraint. Is it based on a specific "control plane" time-slot allocation? Is it to reserve 99.999% of bandwidth for user data? Without this context, the "saturation" of the mesh topology feels like a result of an arbitrary constraint rather than a physical limit.

### Minor Issues

1.  **Table II ($M/D/c$ Sensitivity):** Please double-check the $N_{max}$ calculation for $c=1000$. If $\mu_s = 1000$ and $r=0.1$, then $N_{max} = c \cdot \mu_s / r = 1000 \cdot 1000 / 0.1 = 10^7$. The table lists $10^7$, which is correct, but the text in Section III-B-1 mentions "processing does not bind for $c \geq 100$ within the simulated range." It would be helpful to explicitly state the simulated range limit ($10^5$) in that sentence for clarity.
2.  **Figure 5 (Extrapolation):** The dashed line for $10^6$ nodes in Figure 3 (Latency) is labeled "Analytical Extrapolation." Please ensure the caption explicitly warns that this data point is *not* validated by the DES, as the text notes validation only up to $10^5$.
3.  **Section IV-G (Coordinator Bandwidth):** The distinction between "Unscheduled" and "TDMA" is excellent. However, Eq. 12 ($C_{raw} = C_{coord} / \gamma$) is presented before the TDMA analysis. It might be clearer to move the TDMA equations (Eq. 13) closer to Table VIII.
4.  **Reference Format:** Reference [1] and [3] are non-archival websites. While necessary for current constellations, please ensure the access dates are current (the draft says "accessed February 2026"—assuming this is a future-dated draft or a typo).

---

### Overall Recommendation
**Minor Revision**

The paper represents a high-quality contribution to the field. The simulation framework is robust for the architectural questions asked, and the results provide valuable quantitative bounds for swarm system designers. The major issues regarding physical layer abstraction do not invalidate the results but require careful re-framing of the conclusions to avoid overclaiming "stability."

### Constructive Suggestions

1.  **Refine the "Stability" Conclusion:** Instead of claiming the system is stable, frame the result as: "The hierarchical protocol logic introduces no inherent bottlenecks; instability will be dominated by physical-layer effects (MAC/Link) rather than architectural message flow."
2.  **Contextualize the 1 kbps Budget:** Add a sentence explaining that while OISLs are Gbps, commercial operators require near-100% duty cycle for revenue-generating user traffic. Thus, the "coordination budget" is a strict constraint to minimize "overhead tax" on the payload.
3.  **Expand on AoI Implications:** The finding that $p_{exc}=0.10$ leads to P99 AoI > 400s is critical. Suggest adding a brief discussion on what types of missions can tolerate 7-minute staleness (e.g., station-keeping vs. debris avoidance).
4.  **Visualizing the Sectorized Mesh:** Figure 2 shows the Hierarchical architecture. A small sub-figure or diagram illustrating the "Sectorized Mesh" (showing the screening volume vs. inter-sector relay) would help the reader visualize the intermediate comparator.