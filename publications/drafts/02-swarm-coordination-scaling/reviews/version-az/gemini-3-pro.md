---
paper: "02-swarm-coordination-scaling"
version: "az"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-27"
recommendation: "Minor Revision"
---

Here is a rigorous peer review of the manuscript "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version AZ), prepared for *IEEE Transactions on Aerospace and Electronic Systems*.

---

# Peer Review Report

**Manuscript ID:** Version AZ
**Title:** Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms
**Target Journal:** IEEE Transactions on Aerospace and Electronic Systems

## Review Criteria

### 1. Significance & Novelty
**Rating: 5 (Excellent)**

This manuscript addresses a critical and timely gap in the literature: the specific scaling properties of coordination architectures for "mega-constellations" ($10^3$--$10^5$ nodes). While existing literature covers routing (networking) or small-scale formation flying (GNC), there is a distinct lack of rigorous analysis on the *coordination* layer for fleets of this magnitude, particularly under bandwidth-constrained RF backup scenarios.

The novelty lies in the derivation of closed-form design equations that are verified against a cycle-aggregated Discrete Event Simulation (DES). The distinction between "byte-level" capacity and "time-slot" feasibility under TDMA in the presence of correlated losses (Gilbert-Elliott model) is a significant contribution. The finding that intra-cycle retransmission is structurally infeasible for all members simultaneously under TDMA is a valuable insight for system architects. The paper effectively bridges the gap between abstract distributed systems theory and practical spacecraft operations.

### 2. Methodological Soundness
**Rating: 4 (Good)**

The methodology is generally robust. The combination of analytical derivation (queueing theory, Markov chains) and numerical verification (Monte Carlo DES) is the gold standard for this type of systems engineering research. The authors are careful to define their abstraction layers, specifically the "message-layer" focus, and they honestly report where the simulation verifies vs. where it relies on assumptions (e.g., the static topology).

However, there is a slight disconnect regarding the "Sectorized Mesh" baseline. The paper compares a highly optimized hierarchical model against a mesh model that seems somewhat handicapped by the "capped fanout" assumption which limits connectivity to 3.2%. While the authors acknowledge this as a comparison of "overhead per unit of awareness," the mesh model could be criticized as a "strawman" if not justified more rigorously. Additionally, the reliance on a static topology for a 1-year simulation of LEO swarms is a strong simplification, though the authors provide a reasonable analytical bound for the re-association overhead in Section V-B.

### 3. Validity & Logic
**Rating: 5 (Excellent)**

The logic flow is tight and persuasive. The authors systematically dismantle the problem: first establishing the bottleneck (coordinator ingress), then sizing it, then analyzing latency (AoI), and finally addressing robustness (GE loss).

The "Joint Parameter Interaction Verification" (Section IV-D) is particularly strong. It explicitly tests the assumption that design equations can be composed, a step often skipped in systems papers. The distinction made in Section IV-A between queue overflow (decoupled from GE loss) and frame-time slots (coupled to GE loss) is logically sound and physically insightful. The limitations section is refreshing in its honesty, particularly regarding the validation gap with physical-layer phenomena like Doppler and antenna pointing.

### 4. Clarity & Structure
**Rating: 5 (Excellent)**

The manuscript is written to a very high standard. The structure is logical, following a standard progression from problem statement to model, results, and discussion. The use of specific "Research Questions" (RQ1-3) helps frame the contribution.

The tables are dense but informative. Table V (Coordinator Ingress Model Comparison) and Table X (Topology Comparison) are excellent summaries. The distinction between "offered" and "delivered" overhead is maintained consistently. The mathematical notation is standard and clear. The abstract is quantitative and impactful.

### 5. Ethical Compliance
**Rating: 5 (Excellent)**

The authors include a specific acknowledgment regarding AI-assisted ideation (Claude, Gemini, GPT), citing a specific internal report/methodology. This transparency regarding AI use in the research process is commendable and aligns with emerging best practices. No conflicts of interest are apparent. The research involves simulation of autonomous systems and poses no direct ethical risks to human subjects.

### 6. Scope & Referencing
**Rating: 4 (Good)**

The scope is perfectly aligned with *IEEE TAES*, fitting the "Aerospace Systems" and "Command and Control" interest areas. The references are a good mix of classical theory (Kleinrock, Lamport), space engineering standards (CCSDS, ECSS), and recent mega-constellation literature (Handley, Del Portillo).

A minor critique is the reliance on non-archival sources for some constellation data (e.g., "Jonathan's Space Report," "Starlink FCC filings"). While necessary due to the fast-moving nature of the industry, the authors should ensure these are cited as robustly as possible. The reference to "Project Dyson" (likely the authors' own group) appears frequently; care should be taken to ensure blind review integrity if this is a double-blind submission (though the manuscript provided seems to be a single-blind or final version draft).

---

## Major Issues

1.  **TDMA/GE Coupling Explanation:** In Section IV-A, the paper states: *"This means that under correlated loss with full retransmission, not all members can be scheduled within one cycle."* This is a critical finding. However, the manuscript does not explicitly detail *which* members get dropped or deferred in the DES when this constraint is hit. Does the DES implement a specific priority logic (e.g., random drop, round-robin deferral)? The text mentions "inter-cycle recovery is the effective mechanism," but the mechanism for moving a failed slot to the *next* cycle's schedule (which is also full of nominal reports) is not detailed. Does the system have slack capacity in the next cycle, or does a "bow wave" of retransmissions eventually cause a buffer overflow? This needs clarification in Section IV-A or IV-C.

2.  **Sectorized Mesh Connectivity:** In Section III-B-4, the authors note that the capped sectorized mesh achieves only "3.2% sector awareness" and does not create a connected graph. This severely undermines the utility of the mesh baseline. If the mesh is not connected, it cannot perform fleet-wide functions (like propagating a command from ground to a specific node via hops). If the mesh cannot support the "Command" workload effectively, comparing its overhead to the hierarchical architecture (which supports 100% command dissemination) is an apples-to-oranges comparison. The authors should clarify if the mesh is intended *only* for collision avoidance (local) or if it is meant to be a full C2 architecture. If the latter, the connectivity issue is a fatal flaw in the baseline model.

---

## Minor Issues

1.  **Abstract:** The phrase "under a 1 kbps RF-backup budget" is slightly ambiguous. Is this 1 kbps *available* or 1 kbps *consumed*? Later text clarifies it is the allocation ($C_{node}$), but the abstract could be sharper: "constrained to a 1 kbps/node allocation."
2.  **Section III-A (DES):** "The DES verifies that the closed-form design equations are implemented correctly." This phrasing is slightly circular. It should read: "The DES verifies the accuracy of the closed-form approximations against a stochastic simulation."
3.  **Section IV-A (Eq 8):** The derivation of $\gamma = 0.949$ is clear, but the decision to stick with $\gamma = 0.85$ "conservatively" is somewhat arbitrary. It would be better to list the specific overheads (FEC, ranging) that make up that difference, rather than just calling it conservative.
4.  **Section IV-I (Duty Cycle):** The power variance calculation (CV $\approx 12\%$) assumes a random distribution of coordinator roles. In a physical cluster, if coordinators are geographically adjacent, thermal/power environments might be correlated. A brief note that this assumes spatially distributed or randomized coordinator assignment within the cluster would be beneficial.
5.  **Figures:** Figure 5 (AoI) is referenced as having "Geometric growth," but the plot is linear-linear. "Exponential growth" or "Geometric progression" might be more accurate descriptions of the underlying phenomenon, but ensure the text matches the visual representation.
6.  **Typos:**
    *   Section I-C: "The centralized ($c=1$) and global-state mesh baselines are intentional bounds" - "bounds" should likely be "bounding cases."
    *   Table IV: "Status to coord." - ensure abbreviations are consistent (Coord. vs Coordinator).

---

## Overall Recommendation

**Recommendation: Minor Revision**

This is an excellent paper that provides a much-needed theoretical foundation for sizing coordination networks in large constellations. The derivation of design equations is rigorous, and the distinction between byte-level and time-level constraints is insightful. The "Major Issues" listed above regarding the Mesh baseline and the specific mechanics of TDMA deferral require clarification but do not invalidate the core results regarding the hierarchical architecture. Once these clarifications are added, the paper will be a strong contribution to *IEEE TAES*.

---

## Constructive Suggestions

1.  **Clarify the "Bow Wave" Effect:** In the discussion of Inter-cycle recovery (Section IV-C), explicitly address whether the system is stable if the channel remains in a "Bad" state for longer than the simulation duration. Does the queue of deferred packets eventually explode, or is there a "drop oldest" policy that stabilizes the system at the cost of data loss? Adding a sentence on queue stability conditions under sustained GE bad states would strengthen the analysis.
2.  **Strengthen the Mesh Baseline Argument:** To address the "apples-to-oranges" concern with the Sectorized Mesh, explicitly state that the Mesh is modeled primarily as a *Collision Avoidance* mechanism (local awareness), whereas Hierarchical is modeled for *Fleet Management* (global command/control). Acknowledging that the Mesh fails at global C2 makes the Hierarchical argument stronger, not weaker.
3.  **Add a "Practitioner's Lookup Table":** The "Design Equations Summary" in Section V-D is excellent. Consider converting this into a small "Quick Reference" table (Table XI) that lists the Input Parameter, the Equation, and a "Rule of Thumb" value (e.g., "Coordinator Bandwidth $\approx 25$ kbps"). This would highly increase the paper's utility for systems engineers.
4.  **Expand on Physical Layer Validation:** In Section V-A (Validation Gap), suggest a specific pathway for future work. For example, "Future work should couple this traffic model with an orbital propagator (e.g., GMAT) to capture deterministic link outages caused by Earth occlusion." This shows a clear path forward.