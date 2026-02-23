---
paper: "02-swarm-coordination-scaling"
version: "c"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-23"
recommendation: "Major Revision"
---

## Peer Review: IEEE Transactions on Aerospace and Electronic Systems

**Manuscript Title:** Scaling Hierarchical Coordination for Million-Unit Space Swarms: Discrete Event Simulation and Architectural Analysis
**Version:** C

---

### 1. Significance & Novelty
**Rating: 5**

This manuscript addresses a rapidly emerging and critical gap in aerospace systems engineering. While the literature is saturated with control strategies for small swarms ($<100$ agents) and management of current constellations ($<10^4$ nodes), there is a distinct lack of rigorous analysis regarding the "intermediate regime" of $10^5$ to $10^6$ nodes. As commercial mega-constellations (Starlink, Kuiper) expand and future orbital infrastructure is proposed, this gap becomes a significant risk.

The novelty lies in the systematic, comparative Discrete Event Simulation (DES) across three orders of magnitude in scale. The identification of specific scaling limits—specifically the bandwidth wall for mesh topologies at $10^5$ nodes and the specific duty cycle trade-offs for hierarchical coordinators—provides actionable design guidance. The "Shepherd/Flock" concept, while derived via a novel (and debatable) AI-assisted method, represents a distinct architectural contribution. This work is highly relevant to the TAES readership.

### 2. Methodological Soundness
**Rating: 3**

The core DES framework and the application of queueing theory ($M/D/1$ and $M/D/c$) are generally sound for a high-level architectural trade study. However, for a journal of this caliber, the abstraction level of the communication layer presents a significant methodological weakness.

The simulation treats message passing as an abstract event with a calculated delay, largely ignoring the physical realities of Inter-Satellite Links (ISLs) in Low Earth Orbit (LEO). The paper acknowledges this in Section V-E, noting that Earth occlusion and pointing constraints are not modeled. In a mesh or hierarchical network at $10^6$ nodes, topology changes due to orbital mechanics are continuous. Assuming a static connectivity graph or simple distance-based delay without accounting for line-of-sight occlusion significantly underestimates the latency and buffer requirements, particularly for the Mesh topology.

Furthermore, the "AI-assisted design exploration" (Section V-B), while transparently disclosed, is methodologically porous. Using LLMs to "vote" on architectures based on simulation prompts introduces a circular feedback loop. While the resulting "Shepherd/Flock" concept is engineering-sound, the *method* of deriving it lacks the rigor of the rest of the paper. It should be framed as a discussion point or a heuristic search, rather than a primary methodological contribution.

### 3. Validity & Logic
**Rating: 4**

The conclusions regarding the scalability of hierarchical systems versus centralized and mesh systems are logically sound and supported by the data presented. The derivation of the $O(N^2)$ cost for global mesh convergence is mathematically indisputable given the requirement for global state awareness.

However, there is a logical gap regarding the "50,000-node inflection point" (Section IV-D). The authors calculate an analytical threshold of $5 \times 10^6$ nodes (Eq. 8) but observe the inflection at $5 \times 10^4$ in simulation. They attribute this 100x discrepancy to "inter-regional state reconciliation," but do not provide data to validate this hypothesis. If the simulation diverges from the analytical model by two orders of magnitude, either the model is wrong, or the simulation has an uncharacterized bottleneck. This discrepancy requires deeper investigation before publication.

### 4. Clarity & Structure
**Rating: 5**

The manuscript is exceptionally well-written. The structure is logical, moving from theoretical framing to simulation design, results, and discussion. The mathematical notation is consistent, and the distinction between the different queueing models is clearly articulated.

The figures are well-conceived, particularly Fig. 6 (Duty Cycle Pareto) and Fig. 7 (Scaling Trajectory). The abstract accurately summarizes the paper. The definitions of "Communication Overhead" and the bandwidth breakdown are precise, aiding reproducibility.

### 5. Ethical Compliance
**Rating: 4**

The authors provide a commendable level of transparency regarding the use of AI tools (Claude, Gemini, GPT) in the design exploration phase. This aligns with emerging guidelines on AI disclosure.

However, the citation `[PENDING]` for the GitHub repository needs to be resolved before final publication to ensure reproducibility. Additionally, the author affiliation "Project Dyson Research Team" appears to be a pseudonym or placeholder; standard IEEE policy requires individual author names and specific institutional affiliations for accountability.

### 6. Scope & Referencing
**Rating: 4**

The paper fits squarely within the scope of IEEE TAES, bridging the gap between electronic systems (communications/computing) and aerospace operations. The referencing is generally good, covering foundational distributed systems theory (Lamport, Lynch) and current space operations (Starlink, ESA).

The paper would benefit from stronger referencing regarding ISL technologies (e.g., optical comms standards, pointing acquisition times) to ground the simulation parameters in physical hardware capabilities. The references to military swarm programs are relevant and up-to-date.

---

### Major Issues

1.  **Lack of Orbital Dynamics in Link Model:** The simulation assumes nodes are connected based on distance, but ignores Earth occlusion. In a $10^6$ node swarm in LEO, a significant percentage of the mesh or cluster peers will be occluded by the Earth at any given moment. This forces multi-hop routing even within "local" clusters or requires store-and-forward protocols, which drastically changes latency distributions. The paper must either:
    *   Integrate a basic orbital propagator (e.g., SGP4) to determine valid Line-of-Sight (LOS) links; OR
    *   Apply a stochastic penalty to link availability (e.g., random 40% packet loss or path rerouting delay) to simulate occlusion effects.
    *   *Why:* Without this, the "Mesh" and "Hierarchical" latency results are overly optimistic.

2.  **Unresolved Analytical Discrepancy (The 50k Inflection):** The gap between the predicted threshold ($5 \times 10^6$) and observed threshold ($5 \times 10^4$) in Section IV-D is too large to leave unresolved. The authors speculate it is due to "inter-regional state reconciliation."
    *   *Requirement:* The authors should instrument the simulation to explicitly measure inter-regional message volume. If the speculation is correct, show the data. If not, there may be a bug in the simulation logic or the analytical model (Eq. 8) is missing a term (perhaps an $O(k_r^2)$ interaction term).

3.  **Justification of "Global State" for Mesh:** The paper penalizes the Mesh topology by requiring *global* state convergence ($O(N^2)$). The authors justify this via the need for "fleet-wide collision avoidance." However, in reality, collision avoidance only requires state knowledge of objects on intersecting orbits, not the whole fleet.
    *   *Critique:* This assumption sets the Mesh topology up to fail. A "Sectorized Mesh" (gossiping only with relevant orbital neighbors) is a more fair comparison. The authors should either run a "Sectorized Mesh" variant or more robustly defend why *every* node needs *every* other node's state (e.g., for global optimization of maneuvers, not just collision avoidance).

### Minor Issues

*   **Section III-B-1:** The comparison between Centralized ($c=1$) and Hierarchical is slightly unfair. A centralized system for $10^6$ satellites would obviously use a data center ($c=1000$). While the paper acknowledges this in Table I, the abstract and conclusion focus heavily on the "single server" bottleneck. The text should emphasize the *spectrum/propagation* limits of centralized systems more than the processing limit, which is solvable with money.
*   **Section V-B (AI Exploration):** The methodology description "cross-evaluated each other's proposals across two rounds of structured voting" is vague. How was voting weighted? This section reads more like a tech demo than scientific inquiry. It should be condensed or moved to an appendix, with the focus remaining on the *result* (Shepherd/Flock) rather than the *process*.
*   **Eq. 5:** The aggregation ratio logic is clear, but does $k_r$ represent clusters per region or nodes per region? The text says "clusters per regional coordinator," but consistency with $k_c$ (nodes per cluster) suggests checking the variable definitions carefully.
*   **Figures:** Figure 5 (Latency Distribution) needs a log scale on the Y-axis (Probability Density) to better show the "heavy tail" effects mentioned in the text.

### Overall Recommendation
**Major Revision**

The paper tackles a vital subject with a strong general approach, but the abstraction of the physical layer (orbital mechanics/occlusion) is too high for a definitive architectural comparison in TAES. The discrepancy between the analytical model and simulation results regarding the inflection point indicates a need for deeper analysis. Addressing the orbital link availability and resolving the 50k-node mystery will make this a seminal paper.

### Constructive Suggestions

1.  **Introduce a "Link Availability" Sensitivity Analysis:** Run a set of Monte Carlo simulations where the probability of a successful link ($P_{link}$) varies from 1.0 (current) down to 0.5 (realistic LEO occlusion/contention). Show how the Hierarchical vs. Mesh trade-off changes when links are unreliable.
2.  **Debug the Inflection Point:** Add a specific metric to the simulation to track "Inter-Regional Protocol Overhead" separate from "Status Reports." Plot this metric against $N$ to prove that it is indeed the cause of the 50k inflection. Update Eq. 8 to reflect the actual scaling law observed.
3.  **Refine the Mesh Baseline:** Include a "Local Mesh" or "Sector Mesh" trace in Figure 2. Even if it fails for other reasons (lack of global convergence), it provides a fairer bandwidth comparison than the $O(N^2)$ global gossip model.
4.  **Hardware Heterogeneity Simulation:** Since the "Shepherd/Flock" concept is a key output, run a simulation configuration specifically modeling this (e.g., 10% of nodes have high bandwidth/power, 90% have low). Quantify the power savings to validate the AI-generated concept.