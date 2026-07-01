---
paper: "02-swarm-coordination-scaling"
version: "ah"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-27"
recommendation: "Accept"
---

**Review of Manuscript Version AH**
**Journal:** IEEE Transactions on Aerospace and Electronic Systems
**Title:** Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study

---

### 1. Significance & Novelty
**Rating: 5**

This manuscript addresses a critical and timely gap in the aerospace systems literature: the "middle ground" of coordination scaling between small swarms ($<100$ nodes) and massive, ground-managed constellations. While much existing literature focuses on routing protocols (networking layer) or formation flying (GNC layer), this paper successfully isolates the *coordination control plane*—specifically the cost of maintaining fleet coherence.

The novelty lies in the "parametric design-space characterization." Rather than proposing a new, complex protocol, the authors rigorously characterize the fundamental scaling limits of hierarchical aggregation against centralized and mesh baselines. The finding that centralized architectures (when properly provisioned) do not fail due to processing limits until $N \approx 10^6$ challenges the common "centralized doesn't scale" trope, shifting the argument correctly toward spectrum and fault-tolerance constraints.

### 2. Methodological Soundness
**Rating: 4**

The Cycle-Aggregated Discrete Event Simulation (DES) approach is appropriate for the scale ($10^5$ nodes) and duration (1 year) of the study. A packet-level simulation (e.g., NS-3) would be computationally intractable for these parameters.

**Strengths:**
*   **Analytical Cross-Validation:** The authors consistently validate simulation results against closed-form analytical models (e.g., $M/D/1$ queueing, geometric distributions for AoI, Chernoff bounds for burstiness). This builds high confidence in the DES implementation.
*   **Byte-Level Accounting:** The traffic accounting (Table VI) is rigorous. Excluding the optical ISL bulk transfers from the coordination budget is a crucial and correct modeling decision.

**Weakness:**
*   **MAC Layer Abstraction:** The reliance on a generic efficiency factor $\gamma \in [0.7, 0.9]$ is the primary methodological weakness. While the authors acknowledge this limitation (Table III) and provide a "Physical-layer vignette" (Section IV-A), the assumption that a cluster of 100 nodes can achieve $\gamma=0.85$ efficiency without significant contention overhead is optimistic, even with TDMA, given the guard time requirements cited.

### 3. Validity & Logic
**Rating: 5**

The conclusions are logical and strictly supported by the data. The authors are careful not to overclaim; for instance, they explicitly state that the 46% overhead figure is a result of the *workload assumption* (stress-case commanding) rather than the architecture itself.

The "Dual-Regime Interpretation" (Section IV-E.3) is excellent. It preempts the criticism that 1 kbps is an artificially low constraint by framing it correctly as the "binding design point" for backup modes. The analysis of the Gilbert-Elliott (GE) link model is also logically sound; the finding that intra-cycle retransmission is structurally ineffective against correlated bursts is a standard networking result, but its application here to orbital coordination cycles is valuable.

### 4. Clarity & Structure
**Rating: 5**

The manuscript is exceptionally well-written. The structure is logical, moving from architecture definitions to isolated parameter characterization, and finally to joint interactions.
*   **Tables:** Tables I (Scalability Sensitivity) and VII (Coordinator Bandwidth) are particularly effective at synthesizing complex trade-offs.
*   **Definitions:** The distinction between "Baseline telemetry" and "Protocol overhead" is clearly defined and consistently applied.
*   **Abstract:** The abstract is quantitative and informative, accurately reflecting the paper's contributions.

### 5. Ethical Compliance
**Rating: 5**

The authors include a specific acknowledgment regarding "AI-assisted ideation," which complies with modern transparency standards. No conflicts of interest are apparent. The research involves simulation of theoretical systems and poses no human-subject ethical issues.

### 6. Scope & Referencing
**Rating: 5**

The paper fits squarely within the scope of *IEEE TAES*, bridging the gap between electronic systems (communications) and aerospace operations. The references are comprehensive, covering the necessary bases: classical distributed systems (Lynch, Lamport), swarm robotics (Brambilla, Dorigo), and modern mega-constellation literature (Handley, del Portillo). The inclusion of CCSDS standards (BPv7, Proximity-1) grounds the work in operational reality.

---

### Major Issues

1.  **MAC Efficiency Justification (Section IV-A):**
    The paper relies heavily on the assumption that $\gamma \approx 0.85$ is achievable via TDMA. While the "Physical-layer vignette" calculates slot times based on propagation delay, it glosses over the complexity of *synchronization* in a distributed, mobile cluster. In a hierarchical system where the coordinator rotates, the overhead of re-synchronizing the TDMA schedule after every handoff could be significant.
    *   *Requirement:* Please add a brief discussion or sensitivity analysis regarding the "setup cost" of TDMA. If a coordinator rotates every 24 hours, how much time/bandwidth is lost re-establishing the time slots? If this is negligible, explicitly state why (e.g., GNSS time discipline).

2.  **Sectorized Mesh "Capped Fanout" Fairness (Section III-B-4):**
    The comparison between the hierarchical model and the "Sectorized Mesh" relies on a capped fanout of 10 neighbors. As $N$ scales from $10^3$ to $10^5$, the physical density of the shell increases.
    *   *Critique:* By keeping the neighbor cap constant at 10, the effective "sensing radius" of the mesh shrinks relative to the inter-satellite distance as $N$ grows. This might unfairly penalize the mesh's collision avoidance utility or unfairly advantage its bandwidth scaling.
    *   *Requirement:* Clarify if the "capped fanout" implies a fixed sensing range (and thus variable neighbor count) or a fixed neighbor count (and thus variable sensing range). If the latter, discuss the operational implication of shrinking the sensing horizon at $N=10^5$.

---

### Minor Issues

1.  **Figure 5 (Overhead Scaling):** The log-log scale makes it difficult to see the small differences between the "Nominal" and "Event-driven" profiles for the hierarchical topology. Consider an inset or a separate linear-scale plot for the low-overhead regime.
2.  **Section IV-B (AoI):** The text states "P99 AoI exceeds 440 s." Please clarify if this includes the processing time at the coordinator and the regional aggregator, or if it is strictly the age of the data *at* the cluster coordinator.
3.  **Eq. 11 (Chernoff Bound):** The notation $D_{KL}(\alpha p \| p)$ is standard, but for the aerospace audience, it might be helpful to write out the specific form of the KL divergence for Bernoulli trials to make the bound immediately reproducible.
4.  **Reference Style:** Reference [1] and [3] are cited as "non-archival; accessed February 2026." Since the current date is likely 2024 or 2025, please ensure these access dates are updated to the actual time of submission/revision.
5.  **Typos:**
    *   Section IV-G: "The 24--48 hour duty cycles occupy the Pareto frontier" - Ensure Figure 12 clearly labels the frontier.

---

### Overall Recommendation
**Accept with Minor Revisions**

This is a high-quality manuscript that offers a rigorous, quantitative analysis of a complex systems engineering problem. The methodology is sound, the validation is thorough, and the writing is clear. The "Major Issues" listed above are requests for clarification and tighter justification of assumptions, not fundamental flaws in the research. The paper will make a valuable contribution to the literature on mega-constellation operations.

---

### Constructive Suggestions

1.  **Strengthen the TDMA Argument:** Explicitly mention GNSS (GPS/Galileo) time discipline as the enabler for the tight guard times ($\gamma=0.85$) in Section IV-A. Without a common clock source, the guard times would need to be much larger to account for clock drift, significantly lowering $\gamma$.
2.  **Operationalize the AoI Result:** In the discussion of the 440s AoI (Section IV-B), explicitly link this to a specific orbital regime (e.g., "At 550 km, a 440s delay corresponds to approximately 30 degrees of true anomaly travel..."). This gives the reader a visceral sense of the staleness.
3.  **Highlight the "Independence" Finding:** The finding in Section IV-D (that GE losses and capacity saturation are independent failure modes under point-to-point links) is a subtle but important system design insight. Consider elevating this to the Abstract or Conclusion more prominently—it suggests that designers can size memory (for ARQ) and bandwidth (for ingress) separately.
4.  **Expand on Store-and-Forward:** You mention that inter-cycle store-and-forward is needed for GE recovery. A brief sentence suggesting the magnitude of the buffer required (e.g., "Buffer depth of 3-5 $T_c$ is likely required") would add practical value for satellite bus designers.