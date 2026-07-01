---
paper: "02-swarm-coordination-scaling"
version: "ao"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-27"
recommendation: "Minor Revision"
---

## Peer Review: IEEE Transactions on Aerospace and Electronic Systems

**Manuscript ID:** [Version AO]
**Title:** Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms
**Authors:** Project Dyson Research Team

---

### 1. Significance & Novelty
**Rating: 5 (Excellent)**

This manuscript addresses a critical and timely gap in the aerospace engineering literature: the "missing middle" of coordination scaling between current constellations ($10^3$ nodes) and futuristic mega-swarms ($10^6$ nodes). While swarm robotics literature handles small numbers and networking literature handles routing, there is a scarcity of work that rigorously quantifies the *systems engineering* overhead of coordination architectures at the $10^4-10^5$ scale.

The primary contribution—a set of closed-form design equations validated by simulation—is highly relevant to practitioners designing the control planes for next-generation constellations (e.g., Starlink Gen2, Kuiper). The distinction between "nominal" and "stress-case" workloads, and the explicit byte-level accounting, provides a level of granularity often missing in high-level architectural studies. The derivation of the "21–50 kbps" coordinator ingress requirement is a concrete, actionable design value.

### 2. Methodological Soundness
**Rating: 4 (Good)**

The methodology relies on a cycle-aggregated Discrete Event Simulation (DES). This is an appropriate choice for the scale of the problem ($10^5$ nodes), as packet-level simulation (e.g., NS-3) would be computationally prohibitive for year-long operational sweeps. The authors are transparent about the abstraction level (Table VI is particularly helpful).

However, there is a tension in the methodology regarding the Physical/MAC layer. The paper uses a generic efficiency factor ($\gamma$) to bridge the gap between the message layer and the physical link. While the authors defend this with a TDMA vignette, the assumption that a 1 kbps RF-backup link can support efficient TDMA with low guard times across a 500km cluster is optimistic. Specifically, the synchronization overhead for TDMA on low-rate links is non-trivial.

Furthermore, the statistical treatment is robust (Monte Carlo with bootstrap confidence intervals), and the analytical cross-checks (e.g., Geometric distribution for AoI) add significant confidence to the simulation results.

### 3. Validity & Logic
**Rating: 4 (Good)**

The conclusions generally follow logically from the data. The comparison between Centralized, Hierarchical, and Mesh topologies is balanced. The authors rightly identify that the "Centralized" baseline is limited by spectrum and ground availability rather than pure processing power, which is a nuanced and correct interpretation often missed in similar papers.

**Crucial Caveat:** There is a potential logical conflict in Section IV-D (Joint Parameter Interaction). The authors claim that Gilbert-Elliott (GE) retransmissions and coordinator drops are independent because they occur at different stages of a "point-to-point ISL" architecture. However, the paper frames the 1 kbps budget as an "RF-backup" scenario. RF backup links in swarms are frequently shared-medium (omnidirectional) rather than point-to-point directed links. If the RF backup is a shared medium, retransmissions *would* increase contention and degrade throughput, invalidating the independence claim. This needs clarification.

### 4. Clarity & Structure
**Rating: 5 (Excellent)**

The manuscript is exceptionally well-written. The structure is logical, moving from problem definition to model, then results, and finally discussion. The "Practitioner-oriented sizing table" concept mentioned in the abstract is effectively realized in the Conclusion/Discussion.

Figures are well-captioned and legible. The distinction between "offered" and "delivered" overhead is maintained consistently, which is crucial for this type of analysis. The definitions in Section III-H are precise.

### 5. Ethical Compliance
**Rating: 5 (Excellent)**

The authors provide a clear acknowledgment of AI-assisted ideation in the Acknowledgments section, complying with emerging publication standards. No human subjects are involved. The research appears ethically sound.

### 6. Scope & Referencing
**Rating: 5 (Excellent)**

The paper fits squarely within the scope of *IEEE TAES*, specifically the areas of Space Systems and Command & Control. The references are comprehensive, covering the necessary triad of: (1) classical astrodynamics/constellation management (Wertz, Vallado), (2) distributed systems theory (Lynch, Lamport), and (3) modern networking (DTN, BPv7).

---

### Major Issues

1.  **Contradiction in Link Topology (RF Backup vs. Point-to-Point):**
    In Section IV-D, the finding that GE losses and coordinator drops are independent relies on the assumption of "point-to-point ISL architectures." However, the entire premise of the 1 kbps budget is that it represents an "RF-backup/safe-mode" (Section I-C). In reality, optical ISLs are point-to-point, but low-rate RF backup links (e.g., S-band inter-satellite) are often omnidirectional or semi-directional shared media to ensure connectivity during tumbling.
    *   *Critique:* If the system is in RF backup mode, it is likely a shared medium. In a shared medium, retransmissions consume channel capacity available to other nodes, directly impacting the coordinator's effective ingress rate (via collisions or MAC backoff).
    *   *Requirement:* The authors must explicitly reconcile the "RF backup" constraint with the "point-to-point" topology assumption. If the backup link is shared-medium, the independence result in IV-D likely does not hold, and this limitation must be prominently stated.

2.  **TDMA Feasibility on Low-Rate Links:**
    Section IV-A presents a vignette for TDMA feasibility ($k_c=100$, 24 kbps raw rate). The guard time analysis assumes propagation delay is the dominant factor. However, at very low data rates (1 kbps - 24 kbps), the *transmission time* of the packet is large, but the *clock drift* and *synchronization keep-alive* traffic become significant percentages of the channel capacity.
    *   *Critique:* The paper assumes a MAC efficiency $\gamma \approx 0.85$. For a distributed swarm maintaining TDMA slots over a 1 kbps link, the overhead of time synchronization messages (to keep slots aligned) might drive $\gamma$ much lower.
    *   *Requirement:* Provide a brief calculation or reference justifying that slot synchronization is maintainable with $<15\%$ overhead on a 1 kbps channel, or lower the $\gamma$ estimate for the RF-backup case.

### Minor Issues

1.  **Author Anonymity:** The manuscript lists "Project Dyson Research Team" as the author. While acceptable for the review process, IEEE policy requires individual authors to be listed for the final publication. The footnote acknowledges this, but ensure this is resolved upon acceptance.
2.  **Section III-B-4 (Sectorized Mesh):** The heuristic $k_s = \sqrt{N}$ is based on a density argument. In Walker Delta constellations, the number of neighbors is constant (typically 4 or 6) regardless of $N$, provided the number of planes scales with $N$. The $\sqrt{N}$ scaling implies a volumetric cloud rather than a shell. Please clarify if the simulation assumes a volumetric distribution or a shell.
3.  **Fig. 4 Caption:** The caption mentions "Sectorized mesh (capped fanout) maintains ~65-67%". Visually, the line for sectorized mesh seems to be flat, but the text suggests it might vary slightly. Ensure the text description matches the visual data exactly.
4.  **Equation 11 (Chernoff Bound):** The equation uses $D_{KL}$. While standard, defining the specific form of KL divergence for Bernoulli variables used here would aid readability for non-information-theory specialists.
5.  **Reference 1 (Starlink):** The citation is an FCC filing. While appropriate, adding a peer-reviewed source regarding Starlink's architecture (if available) or a more permanent technical reference would be stronger.

---

### Overall Recommendation
**Minor Revision**

The manuscript represents a high-quality contribution to the field. The analytical models are sound, and the simulation campaign is extensive. The "Major Issues" identified above relate to the interpretation of physical layer constraints (RF topology and MAC efficiency) rather than the fundamental logic of the hierarchical coordination. Clarifying the assumptions regarding the RF backup topology and its impact on the "independence" result will be sufficient to make this paper ready for publication.

### Constructive Suggestions

1.  **Add a "Shared Medium" Caveat to Section IV-D:** Explicitly state that if the RF backup link uses a shared bus (CSMA or ALOHA) rather than FDMA/CDMA/Point-to-Point, the independence between GE losses and coordinator saturation vanishes. This adds necessary engineering rigor.
2.  **Refine the "Practitioner Sizing Table":** Consider moving the summary design equations from the Conclusion (Section VI) into a standalone Table in the Discussion. This would be the "takeaway" artifact for engineers.
3.  **Expand on "Coordinator Election" Overhead:** You mention Raft briefly. A short sentence quantifying the bandwidth cost of a Raft election storm (e.g., if a regional failure triggers 10 simultaneous cluster elections) would strengthen the fault tolerance argument.
4.  **Clarify "1 kbps" vs "Spectrum":** In the introduction, clarify that 1 kbps is a *per-node budget* derived from spectrum constraints, not necessarily the hardware limit of the transceiver. This helps readers understand why the coordinator can listen at 50 kbps while nodes send at 1 kbps.