---
paper: "02-swarm-coordination-scaling"
version: "b"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-23"
recommendation: "Major Revision"
---

Here is the peer review for the manuscript "Scaling Hierarchical Coordination for Million-Unit Space Swarms: Discrete Event Simulation and Architectural Analysis" (Version B).

***

# Peer Review Report

**Journal:** IEEE Transactions on Aerospace and Electronic Systems
**Manuscript ID:** [Assigned by Editor]
**Title:** Scaling Hierarchical Coordination for Million-Unit Space Swarms: Discrete Event Simulation and Architectural Analysis
**Date:** October 26, 2023

## Review Criteria

### 1. Significance & Novelty
**Rating: 4 (Good)**

The manuscript addresses a highly relevant and forward-looking problem: the coordination of space assets at scales ($10^5$ to $10^6$) that far exceed current operational experience. As mega-constellations like Starlink expand and new infrastructures are proposed, the transition from centralized ground control to autonomous distributed coordination is inevitable. The paper's systematic comparison of three topologies across three orders of magnitude is a valuable contribution, filling a gap between swarm robotics literature (typically small scale) and constellation management literature (typically centralized/moderate scale).

The novelty lies primarily in the specific quantification of the "breaking points" for centralized and mesh architectures in the context of orbital mechanics and collision avoidance. The identification of the 50,000-node inflection point for hierarchical overhead is a useful heuristic for system architects. However, the "Shepherd/Flock" concept, while practical, is a well-known pattern in terrestrial networks (as the authors acknowledge), so the novelty there is in the application domain rather than the fundamental architecture.

### 2. Methodological Soundness
**Rating: 3 (Adequate)**

The Discrete Event Simulation (DES) framework is generally appropriate for this type of architectural trade-off analysis. The use of Monte Carlo methods to capture stochastic failures is robust. The queueing theoretic models ($M/D/1$ and $M/D/c$) are standard and correctly applied to establish bounds.

However, there are two notable methodological weaknesses. First, the centralized model is somewhat of a "straw man." While the authors acknowledge that $M/D/c$ shifts the limit, modeling a million-node constellation with a single-server queue ($c=1$) creates an artificially low ceiling ($N=10,000$). A realistic ground segment for a mega-constellation would employ massive parallelism and distributed data centers. The paper would be stronger if it modeled the *cost* or *complexity* of the ground segment required to support $10^6$ nodes, rather than implying it is impossible due to a single-server queue limit.

Second, the "AI-Assisted Architectural Exploration" section, while transparent, is methodologically weak. As the authors themselves admit, the LLMs were primed with simulation results, making their "convergence" on hierarchical solutions circular. This section feels more like a novelty demonstration than rigorous engineering methodology.

### 3. Validity & Logic
**Rating: 4 (Good)**

The conclusions regarding the scalability of hierarchical systems versus flat mesh networks are logically sound and supported by the simulation data. The derivation of the $O(N^2)$ cost for mesh networks in the context of *global* collision avoidance is correct and a critical distinction from local flocking behaviors. The analysis of coordinator duty cycles is thorough, and the identification of the Pareto frontier between power variance and availability is a strong analytical result.

The logic falters slightly in the "Shepherd/Flock" proposal. The simulation assumes homogeneous nodes with rotating coordinators, but the AI section proposes heterogeneous hardware. While this is a valid design pivot, the simulation data presented does not explicitly model the heterogeneous case (e.g., different failure rates for Shepherds vs. Flock, or the impact of losing a Shepherd in a heterogeneous vs. homogeneous setup). The connection between the simulation results and the heterogeneous proposal is qualitative rather than quantitative.

### 4. Clarity & Structure
**Rating: 5 (Excellent)**

The manuscript is exceptionally well-written. The structure is logical, moving from problem definition to simulation framework, results, and discussion. The mathematical notation is clear and consistent. Figures are well-described in the text (though I cannot see the visual rendering, the captions and references suggest they are appropriate). The distinction between the simulation results and the AI-generated concepts is clearly demarcated, preventing confusion between quantitative data and qualitative ideation.

### 5. Ethical Compliance
**Rating: 5 (Excellent)**

The authors provide a model of transparency regarding the use of AI. Section V explicitly details the methodology, the specific models used, and crucially, the limitations of this approach (priming effects, training data overlap). The "Acknowledgment" section properly credits the AI tools. There are no apparent conflicts of interest, though the affiliation "Project Dyson" appears to be a placeholder or a private research initiative; the editor should verify the institutional standing if this is not a standard academic lab.

### 6. Scope & Referencing
**Rating: 4 (Good)**

The paper fits well within the scope of *IEEE TAES*, bridging aerospace systems engineering and electronic systems/communications. The referencing is solid, covering foundational distributed systems theory (Lamport, Lynch), swarm robotics (Brambilla, Dorigo), and current space industry developments (Starlink, Kuiper). The inclusion of recent work on Graph Neural Networks (Tolstaya et al.) shows awareness of the cutting edge.

***

## Major Issues

1.  **The "Straw Man" Centralized Model:**
    In Section III.B.1 and Section IV.A, the centralized topology is limited by a single-server $M/D/1$ queue. The authors state, "Our single-server parameterization... represents the architectural worst case." This is too conservative to be useful for a fair comparison. A ground system for 10,000 satellites would obviously use load balancing and parallel processing.
    *   **Requirement:** The authors should re-run or re-calculate the centralized baseline using a realistic $M/D/c$ model where $c$ scales with $N$ (perhaps logarithmically or linearly with a cost function). The argument against centralized control should be based on *propagation latency* (speed of light to ground and back) and *bandwidth constraints* (uplink/downlink spectrum scarcity), not just server queueing delay, which is easily solved with more ground hardware.

2.  **Mesh Topology Parameterization:**
    The paper argues that mesh topology fails because global state convergence is required for collision avoidance ($O(N^2)$). This is a strong assumption. Many swarm algorithms rely on *local* sensing and communication for collision avoidance ($O(k)$ where $k$ is neighbor count), only requiring global convergence for task assignment.
    *   **Requirement:** The authors must justify why *global* trajectory awareness is strictly necessary for collision avoidance in their model. If a node only needs to avoid neighbors in its orbital shell, the $O(N^2)$ assumption may be flawed. If the assumption stands, it needs a stronger astrodynamics justification (e.g., intersecting orbital planes requiring non-local awareness).

3.  **AI Section Methodology:**
    Section V is interesting but scientifically weak. The authors admit the "priming effect" invalidates the independence of the AI's proposal.
    *   **Requirement:** This section should be significantly condensed or moved to the Discussion. It currently occupies too much space (an entire main section) relative to its evidentiary value. The "Shepherd/Flock" concept should be presented as a discussion point derived from the *simulation's* findings on power variance, rather than attributing it to an AI "deliberation" which adds little engineering rigor.

***

## Minor Issues

1.  **Equation 5 (Hierarchical Messages):** The equation $M_{\text{total}} = N + N/k_c + N/(k_c \cdot k_r)$ describes the message volume. It would be helpful to explicitly state if this is *per reporting cycle*.
2.  **Section III.A (Simulation Clock):** The text mentions "one-second resolution for collision avoidance... and one-minute resolution for routine coordination." Please clarify how synchronization is handled between these two time scales in the event loop.
3.  **Section IV.D (50,000 Node Threshold):** The authors note that "five data points... provide limited resolution." This is a candid admission, but since this is a simulation, generating more data points is purely a computational cost. Why not run intermediate points ($2 \times 10^4, 3 \times 10^4$, etc.) to smooth this curve?
4.  **Section VI.D (Limitations):** The limitation regarding "no line-of-sight occlusion by the Earth" is significant for Low Earth Orbit (LEO) ISLs. This should be emphasized, as it significantly impacts the mesh topology's connectivity graph.
5.  **References:** Reference [31] (Project Dyson Research Team, 2025) cites a "manuscript in preparation." Self-citing unpublished work is generally discouraged; please ensure this is necessary or remove it.

***

## Overall Recommendation

**Major Revision**

The paper tackles a critical scaling problem with a solid simulation approach, but the comparison is skewed by an unrealistically weak centralized baseline and a potentially overly strict requirement for global mesh convergence. Furthermore, the AI-assisted section, while transparent, distracts from the core engineering analysis. The paper needs to strengthen the "Centralized" model to be a fair competitor (focusing on latency/spectrum rather than server CPU) and should likely demote the AI exploration to a discussion subsection to focus on the quantitative results.

***

## Constructive Suggestions

1.  **Refine the Centralized Comparison:** Instead of a processing bottleneck ($M/D/1$), model the centralized constraint based on **spectrum availability**. Calculate the total bandwidth required to downlink telemetry for $10^6$ nodes and compare it to available X/Ka-band spectrum. This makes the argument against centralization physical and irrefutable, rather than dependent on server assumptions.
2.  **Hybrid Topology:** Consider adding a brief analysis or discussion of a "Hybrid" approach, where collision avoidance is local (Mesh/Flock) but tasking is hierarchical. This is the most likely real-world architecture and would add nuance to the binary choice between Mesh and Hierarchy.
3.  **Strengthen the Astrodynamics Context:** Explicitly mention the orbital shell configuration (e.g., Walker Delta). The density of the swarm determines the collision risk and therefore the communication requirements. A brief mention of the orbital parameters used for the distance calculations would add rigor.
4.  **Condense Section V:** Summarize the AI exploration in 2-3 paragraphs within the Discussion section. Use the saved space to expand on the "Dynamic Spatial Partitioning" algorithm, which is a more substantial engineering contribution than the AI deliberation process.