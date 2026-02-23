---
paper: "02-swarm-coordination-scaling"
version: "e"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-23"
recommendation: "Minor Revision"
---

Here is a rigorous peer review of the manuscript "Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study" (Version E), prepared for *IEEE Transactions on Aerospace and Electronic Systems*.

---

# Peer Review Report

**Manuscript Title:** Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study
**Target Journal:** IEEE Transactions on Aerospace and Electronic Systems

## Review Criteria

### 1. Significance & Novelty
**Rating: 5 (Excellent)**

This paper addresses a critical and rapidly emerging gap in the aerospace literature: the "intermediate regime" of coordination scaling between current constellations ($10^3$ nodes) and future mega-structures ($10^6$ nodes). While swarm robotics literature covers small scales and astrodynamics literature covers trajectory optimization, the specific intersection of *communication architecture scalability* and *orbital mechanics constraints* at this magnitude is under-explored.

The novelty lies in the systematic comparison of three distinct topologies (Centralized, Global-State Mesh, Hierarchical) using a unified Discrete Event Simulation (DES) framework. The identification of a "superlinear scaling regime" near 50,000 nodes is a significant finding that could influence the design of next-generation mega-constellations (e.g., Starlink Gen2/3, Kuiper). The practical guidelines regarding coordinator duty cycles (24-48 hours) provide immediate engineering value.

### 2. Methodological Soundness
**Rating: 4 (Good)**

The methodology is generally robust. The use of Discrete Event Simulation (DES) combined with Monte Carlo analysis is the appropriate tool for this problem space. The authors have done an excellent job defining their parameters (Table III) and explicitly stating the queueing models used ($M/D/1$ and $M/D/c$). The validation against analytical bounds (Pollaczek–Khinchine and gossip convergence) adds confidence to the simulation results.

However, there is a slight disconnect in the physical layer modeling. The paper acknowledges that physical layer effects (occlusion, Doppler, pointing) are abstracted away, arguing they are "topology-neutral." While likely true for the broad ranking of architectures, this assumption may weaken the specific quantitative results (e.g., the exact 2-8% overhead figures). A sensitivity analysis on link availability would strengthen the claim that the hierarchy remains superior under degraded link conditions. Additionally, the collision avoidance rate ($10^{-4}$/node/s) is well-justified in the text, but its impact on the specific "superlinear" threshold should be more explicitly stress-tested.

### 3. Validity & Logic
**Rating: 5 (Excellent)**

The conclusions logically follow from the data presented. The authors are careful to distinguish between *processing* limits (which can be solved with more hardware) and *fundamental* limits (spectrum, propagation delay, $O(N^2)$ state complexity). This distinction is crucial and often missed in less rigorous studies.

The analysis of the coordinator duty cycle is particularly strong, identifying a Pareto frontier between power variance and availability. The "Sectorized Mesh" discussion in Section V-C is a vital intellectual bridge, correctly identifying that the hierarchical model is essentially a formalized version of a sectorized mesh. The limitations section is refreshingly honest, particularly regarding the idealized link conditions.

### 4. Clarity & Structure
**Rating: 5 (Excellent)**

The manuscript is exceptionally well-written. The structure follows a logical progression: Problem $\rightarrow$ Models $\rightarrow$ Results $\rightarrow$ Discussion. The mathematical formulations for queueing delays and message complexity are clear and correct.

The figures are well-conceived. Figure 2 (Architecture Diagram) clearly illustrates the hierarchy. Figure 3 (Overhead Scaling) effectively visualizes the divergence of the baselines. The distinction between "Baseline Telemetry" (topology-invariant) and "Protocol Overhead" is defined early and used consistently, preventing confusion in the results.

### 5. Ethical Compliance
**Rating: 5 (Excellent)**

The authors provide a specific "Acknowledgment" section detailing the use of AI tools (Claude, Gemini, GPT) for *ideation* and *methodology design*, citing a companion methodology paper. This level of transparency regarding AI assistance sets a high standard for ethical disclosure. The data availability statement promises open-source access to the code, which supports reproducibility.

### 6. Scope & Referencing
**Rating: 4 (Good)**

The paper fits perfectly within the scope of *IEEE TAES*, bridging electronic systems (communication architectures) and aerospace systems (orbital mechanics/constellation ops). The literature review is comprehensive, covering historical foundations (Lamport, Reynolds), current operations (Starlink, OneWeb), and theoretical work (Mean-field games).

One minor gap is the lack of reference to specific CCSDS standards regarding *security* (e.g., SDLS). While security is not the focus, the overhead of encryption and authentication in a hierarchical system (where coordinators change roles) would be non-trivial and is relevant to the "Protocol Overhead" metric.

---

## Major Issues

1.  **Superlinear Scaling Regime Granularity:**
    The paper identifies a superlinear scaling regime starting near 50,000 nodes but admits in Section IV-D that this is based on "only five data points spanning three orders of magnitude." For a finding this significant—which implies a phase transition in coordination complexity—the resolution is too coarse. The authors identify this as future work, but for a journal of this caliber, a targeted simulation sweep between 10k and 100k nodes (e.g., 20k, 40k, 60k, 80k) should be included in *this* manuscript to confirm the shape of the curve. Is it a knee or a smooth exponential rise? This distinction matters for system architects.

2.  **Physical Layer Abstraction Justification:**
    In Section V-E, the authors argue that physical layer effects (occlusion, pointing) are "approximately topology-neutral." This is a strong assumption. A centralized topology relies on ground-to-space links (GSLs), while hierarchical and mesh rely heavily on inter-satellite links (ISLs). Atmospheric attenuation affects GSLs but not ISLs; conversely, relative motion Doppler and pointing jitter affect ISLs differently than GSLs. The paper needs a stronger defense—or a limited simulation case—demonstrating that introducing a stochastic link failure model does not invert the ranking of the architectures.

---

## Minor Issues

1.  **Equation 5 (Hierarchical Messages):** The equation $M_{\text{total}} = N + N/k_c + N/(k_c \cdot k_r)$ describes upward reporting. The text immediately following mentions that bidirectional overhead is 1.5-2x this value. It would be clearer to formalize the downward command traffic in the equation itself or explicitly state that Eq. 5 represents *uplink* complexity only.
2.  **Table I (M/D/c Sensitivity):** The table lists $N_{max}$ for various server counts. It would be helpful to add a column for "Estimated Latency at $0.9 N_{max}$" to emphasize that even before saturation, queueing delays might be operationally unacceptable for collision avoidance.
3.  **Section III-B-2 (Cluster Saturation):** The text states "Since our parameterization uses $k_c \leq 500$, the cluster coordinator operates well below saturation." It would be beneficial to explicitly state the utilization $\rho$ for the worst-case $k_c=500$ to prove it is safe (e.g., $\rho = 0.25$).
4.  **Figure 6 (Scaling Trajectory):** The "Optimized" curve flattens near 4-5%. The text explains *why* (exception-based telemetry), but the figure caption should explicitly link the flattening to the specific optimizations enabled at that scale.
5.  **Reference Format:** Reference [1] and [3] are non-archival websites. While necessary for current constellations, ensure the access dates are recent (the manuscript says "accessed February 2026", which implies this is a future-dated draft or a typo).

---

## Overall Recommendation

**Minor Revision**

This is a high-quality paper that makes a significant contribution to the field of large-scale space systems engineering. The simulation framework is sound, and the results are novel. The "Major Issues" identified above regarding the granularity of the superlinear regime and the physical layer justification do not invalidate the core results but addressing them would significantly strengthen the manuscript. I recommend publication after these points are addressed.

---

## Constructive Suggestions

1.  **Run a "Zoom-In" Simulation:** Conduct a limited set of Monte Carlo runs specifically in the $N \in [20,000, 80,000]$ range. Plotting these points on Figure 7 would definitively characterize the onset of the superlinear regime, transforming a speculative observation into a rigorous finding.
2.  **Add a "Link Availability" Sensitivity Plot:** Add a figure showing Protocol Overhead vs. Link Availability (e.g., 100% down to 80%). If the Hierarchical model's overhead spikes faster than the Mesh model as links degrade (due to coordinator bottlenecks), this is a crucial design constraint that should be reported.
3.  **Expand on "Exception-Based Telemetry":** The discussion in Section IV-D is excellent but brief. Consider adding a small table or equation estimating the bandwidth savings factor ($\beta$) provided by exception-based reporting, based on the ratio of "quiet" orbits to "maneuvering" orbits.
4.  **Clarify "Coordinator Failure" Impact:** In Section III-B-2, you mention a "degraded mode" during handoff/failure. Explicitly define what happens to a collision alert generated *during* this window. Is it dropped? Queued? This affects the safety case.