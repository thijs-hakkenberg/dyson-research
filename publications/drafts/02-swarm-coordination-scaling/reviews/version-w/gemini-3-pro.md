---
paper: "02-swarm-coordination-scaling"
version: "w"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-24"
recommendation: "Minor Revision"
---

**Review of Manuscript Version W**
**Title:** Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study
**Journal:** IEEE Transactions on Aerospace and Electronic Systems

---

### 1. Significance & Novelty
**Rating: 5**

This manuscript addresses a critical and forward-looking gap in the aerospace engineering literature: the specific scaling behaviors of coordination architectures for autonomous swarms in the $10^4$ to $10^5$ node regime. While existing literature covers small-scale swarms ($<100$ nodes) or centralized constellation management, the "mega-constellation" autonomous regime is under-characterized.

The novelty lies not in the proposal of hierarchical coordination itself (which is a standard distributed systems pattern), but in the **rigorous quantitative characterization of the design envelope** under specific bandwidth constraints. The derivation of the 5%–46% overhead range, the specific analysis of TDMA vs. random-phase buffer requirements (reducing the zero-drop threshold from 50 kbps to 24 kbps), and the application of Age-of-Information (AoI) as a coordination freshness proxy are significant contributions. The introduction of the "Sectorized Mesh" as a hybrid comparator adds substantial value, moving beyond the typical binary comparison of "Centralized vs. Flooding."

### 2. Methodological Soundness
**Rating: 4**

The methodology is generally robust and well-documented. The use of a cycle-aggregated Discrete Event Simulation (DES) is appropriate for the scale of the problem ($10^5$ nodes), where packet-level simulation would be computationally prohibitive. The authors have taken excellent care to validate their simulation against analytical closed-form solutions (Section IV-F), achieving <0.1% error, which builds high confidence in the implementation.

However, a specific limitation in the **Gilbert-Elliott (GE) link model** warrants attention. The manuscript states that GE state transitions occur once per coordination cycle ($T_c = 10$ s). While this is acceptable for modeling macroscopic outages (e.g., Earth occlusion or slewing), it is too coarse to capture fast-fading multipath effects or short-duration scintillation. The authors acknowledge this in Section III-J, but the implications for the retransmission analysis in Section IV-K should be qualified further: the results apply to *correlated outages*, not necessarily fast-fading channel dynamics.

### 3. Validity & Logic
**Rating: 5**

The conclusions are logically sound and supported by the data. The paper avoids the common pitfall of claiming the hierarchical approach is "optimal" in all cases; instead, it rigorously defines the trade-offs. The distinction between the "single-server" centralized baseline (a theoretical bound) and realistic parallelized ground systems is handled with intellectual honesty in the Introduction and Results.

The analysis of **TDMA vs. Random-phase scheduling** (Section IV-I) is particularly strong. The finding that TDMA reduces the required coordinator capacity by eliminating Poisson-like burstiness is a solid engineering insight that is not immediately obvious from simple byte-counting. The logic regarding Exception-Based Telemetry (Section IV-G) is also sound: the paper correctly identifies that the bandwidth savings come at the cost of "staleness" (AoI), and quantifies this trade-off explicitly.

### 4. Clarity & Structure
**Rating: 5**

The manuscript is exceptionally well-written. The structure is logical, moving from architecture definitions to simulation details, then to results and sensitivity analyses.

*   **Tables:** Table V (Simulation Abstraction Scope) is a model of transparency that other papers should emulate. It clearly delineates what is and isn't modeled. Table IV (Traffic Accounting) is crucial for reproducibility.
*   **Figures:** Figure 2 (Overhead Scaling) and Figure 9 (TDMA Comparison) are effective and clearly labeled.
*   **Terminology:** The distinction between "Baseline Telemetry" (topology-invariant) and "Protocol Overhead" (topology-dependent) is maintained consistently, preventing confusion in the results.

### 5. Ethical Compliance
**Rating: 5**

The authors have included a specific acknowledgment regarding the use of AI tools for ideation (Claude, Gemini, GPT) in the Acknowledgments section, citing a companion methodology paper. This level of transparency regarding AI-assisted workflows meets and exceeds current ethical standards. No conflicts of interest are apparent.

### 6. Scope & Referencing
**Rating: 5**

The paper is squarely within the scope of *IEEE TAES*, bridging the gap between electronic systems (communications/networking) and aerospace operations (constellation management). The references are comprehensive, covering foundational texts (Kleinrock, Lynch), standard space references (SMAD, CCSDS), and recent mega-constellation literature (Handley, Del Portillo). The inclusion of AoI literature (Kaul, Yates) connects the work to modern networking theory effectively.

---

### Major Issues

**1. Visual Representation of Centralized Baseline (Figure 2)**
While the text in Section III-B-1 and IV-A clearly states that the centralized baseline uses $c=1$ (single server) as a "worst-case bound," **Figure 2** presents this curve diverging at $N=10^4$ without visual context for parallelization. A casual reader scanning the figures might incorrectly conclude that centralized architectures fundamentally fail at $10^4$ nodes due to processing, which contradicts the text's admission that $c=100$ shifts the limit to $10^6$.
*   *Requirement:* Please add a second dashed line to Figure 2 (or an annotation) representing a parallelized ground system (e.g., $c=100$) to visually demonstrate that the constraint on centralized systems is physical (latency/spectrum), not processing.

**2. Physical Layer Abstraction vs. Link Budget**
The paper defines a "1 kbps/node" budget. Section III-F explains this is a *control-plane allocation* from a much larger optical link. However, the overhead results ($\eta \approx 46\%$) are presented as percentages of this arbitrary allocation.
*   *Critique:* If the optical ISL is 1 Gbps, the "overhead" is negligible in terms of *link capacity*. The constraint is actually **processing ingress** at the coordinator (which you address) and **spectrum allocation** if using RF backup.
*   *Requirement:* The discussion should clarify that the high overhead percentages (46-67%) are critical for *dimensioning the control plane reservation*, not necessarily for link closure. If the control plane is congested, it blocks safety-critical commands, even if the data plane is empty. This distinction needs to be sharper in the Conclusion.

### Minor Issues

1.  **Table III (Simulation Parameters):** The "Screening alert rate" is listed as $10^{-4}$/node/s. The footnote explains this includes proximity monitoring, not just maneuvers. Please explicitly state if this rate assumes a specific orbital shell density (e.g., 550 km Starlink-like density). The rate is density-dependent.
2.  **Section IV-H (AoI):** The paper states "P99 AoI exceeds 400 s." It would be helpful to contextualize this against a typical LEO orbital period (~5400 s). 400s is ~7% of an orbit. Is this acceptable for propagation? A brief sentence on orbital error growth over 400s (e.g., "In-track error growth for a typical LEO object over 7 minutes is approximately X meters") would strengthen the "proxy" argument.
3.  **Equation 11 (TDMA Capacity):** The approximation $23.9$ kbps is derived. Please double-check the arithmetic consistency with the guard time $\gamma=0.85$. $(20.3 / 0.85) \approx 23.88$. The text is correct, just a minor check.
4.  **Typos:**
    *   Section III-A: "cycle-aggregated discrete event simulation (DES)" - ensure capitalization consistency throughout.
    *   References: Ensure all "non-archival" references (Starlink, Kuiper) have access dates (which they do, good job).

---

### Overall Recommendation
**Minor Revision**

The manuscript is technically sound, novel, and well-presented. The simulation framework is validated, and the results provide specific, actionable engineering data for space system architects. The "Major Issues" listed above are primarily regarding presentation and context (visualizing the centralized parallelization and clarifying the control-plane nature of the budget) rather than fundamental flaws in the data or logic.

---

### Constructive Suggestions

1.  **Enhance Figure 2:** Add a "Theoretical Parallelized Ground ($c=100$)" curve to Figure 2. This will strengthen your argument that the *real* reason to avoid centralized control is latency and spectrum, not the processing bottleneck shown by the $c=1$ curve.
2.  **Contextualize AoI:** In Section IV-H, add a "back-of-the-envelope" calculation for position uncertainty growth over the 400s P99 AoI interval (e.g., assuming $J_2$ perturbations or simple drag uncertainty). This connects the abstract AoI metric to physical collision risk.
3.  **Refine GE Model Description:** In Section III-J, explicitly rename the model to "Correlated Outage Model" or clarify that the 10s discretization is intended to capture *occlusion events*, not *channel fading*. This prevents RF engineers from criticizing the coarse time step.
4.  **Coordinator Hardware Implication:** In the Discussion, expand slightly on the hardware implication of the "50 kbps ingress" requirement. Does this imply that *every* node needs a receiver capable of 50 kbps (in case it is elected coordinator), or can the fleet be heterogeneous? (You mention this briefly in IV-F, but it's a key spacecraft design driver).