---
paper: "02-swarm-coordination-scaling"
version: "g"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-23"
recommendation: "Minor Revision"
---

## Peer Review Report

**Journal:** IEEE Transactions on Aerospace and Electronic Systems
**Manuscript ID:** [Version G]
**Title:** Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study

---

### Review Criteria

**1. Significance & Novelty**
**Rating: 5**
This manuscript addresses a critical and rapidly approaching problem in aerospace systems engineering: the coordination of mega-constellations and future autonomous swarms at scales ($10^5$--$10^6$ nodes) that break current centralized paradigms. The identification of a specific "superlinear scaling transition" at $N \approx 45,000$ nodes is a novel and operationally significant finding. The paper successfully bridges the gap between small-scale swarm robotics literature and current constellation management practices. The rigorous characterization of the "middle ground" between centralized control and full mesh networking is a valuable contribution to the field.

**2. Methodological Soundness**
**Rating: 4**
The Discrete Event Simulation (DES) framework is robust and appropriate for the research questions. The authors are commended for the explicit "Traffic Accounting" (Table V), which ensures reproducibility and clarity regarding what is included in the overhead metrics. The use of AIC to select the piecewise-linear model adds statistical rigor to the scaling analysis.
*Critique:* The power budget analysis (Section IV-G, Eq. 8) focuses on *average* power consumption but neglects the systems engineering implication of *peak* power sizing. If nodes are homogeneous and rotate roles, *every* node must be hardware-sized (battery, thermal, radio) for the coordinator role, imposing a mass penalty on the entire fleet, not just an average power penalty. This mass/cost implication is understated.

**3. Validity & Logic**
**Rating: 4**
The conclusions are generally well-supported by the simulation data. The authors wisely include a "Baseline Interpretation Note" (Section I-C) to preemptively defend against the criticism that their baselines are strawmen.
*Critique:* While the Global-State Mesh serves as a valid theoretical upper bound, it is an inefficient implementation of decentralization. The logic that Hierarchical is superior to Mesh relies heavily on the assumption that the Mesh must maintain *global* state. While justified for fleet-wide collision avoidance, a "Sectorized Mesh" (mentioned in Discussion) is the true competitor. The validity of the "Projected" curve in Fig. 8 relies on analytical assumptions that are only partially validated (via the exception-based telemetry test); this distinction needs to be sharper.

**4. Clarity & Structure**
**Rating: 5**
The paper is exceptionally well-written and organized. The progression from topology definition to simulation results to optimization is logical. Figures are high-quality and informative, particularly the message decomposition in Fig. 7. The distinction between "baseline telemetry" (topology-invariant) and "protocol overhead" is handled with excellent clarity.

**5. Ethical Compliance**
**Rating: 5**
The authors provide a clear disclosure regarding the use of AI tools for ideation in the Acknowledgment section. No ethical concerns regarding the research content are apparent.

**6. Scope & Referencing**
**Rating: 5**
The topic fits perfectly within the scope of *IEEE TAES*. The references are current and relevant, spanning classical distributed systems theory (Lamport, Lynch), modern constellation operations (Starlink), and relevant standards (CCSDS).

---

### Major Issues

1.  **Homogeneous Hardware Mass Penalty (Section IV-G):**
    The analysis in Section IV-G and Equation 8 calculates the *average* power overhead per node ($\Delta P_{avg} = 0.15$ W). However, this obscures a critical systems engineering constraint. In a homogeneous swarm with rotating coordinators, *every* spacecraft must carry the power generation (solar array), energy storage (battery), and thermal control capacity to support the peak load of the coordinator mode (15-20 W vs 5 W baseline). Even if a node only acts as coordinator 1% of the time, it must be *built* to survive that 1%. This implies a significant mass and cost penalty for the entire fleet that is not captured by the "average power" metric. The manuscript should acknowledge that the "Heterogeneous Hardware" optimization (mentioned in Section IV-D) is not just an optimization but potentially a requirement to avoid over-sizing the entire fleet.

2.  **Validation of "Projected" Optimizations (Fig. 8):**
    Figure 8 presents a dashed line for "Analytically projected" overhead. While the authors successfully validate the *exception-based telemetry* component via DES (Section IV-E), the other two components (dynamic partitioning and heterogeneous hardware) remain purely analytical. The visual weight of the dashed line in Fig. 8 implies a level of certainty that may not exist. The text should more explicitly separate the DES-validated reduction from the purely theoretical reductions, perhaps by showing an intermediate curve in Fig. 8 that includes *only* the DES-validated exception-based telemetry.

### Minor Issues

1.  **Section I-C (Baseline Interpretation):** The authors state that practical decentralized approaches would fall "between the mesh upper bound and hierarchical curves." It is theoretically possible that a highly optimized Sectorized Mesh could outperform the fixed 4-level Hierarchy at very large $N$ due to the hierarchy's root congestion (even with aggregation). It would be safer to state they "likely" fall between them.
2.  **Table I (Scalability Sensitivity):** The table lists "Hyperscale data center" for $c=1000$. While true for processing, the text correctly notes that spectrum/propagation are the hard limits. It might be helpful to add a column or note in the table indicating "Binding Constraint" (e.g., Processing vs. Spectrum) to reinforce the text.
3.  **Section III-E (Collision Rate):** The rate of $10^{-4}$/node/s seems high for *maneuver* events but the text clarifies these are *screening* events. Please ensure the simulation actually treats these as small messages (alerts) rather than full maneuver commands, as this impacts the bandwidth significantly. (Table V suggests they are 128B alerts, which is consistent).
4.  **Data Availability:** The GitHub link contains a placeholder commit hash `[PENDING]`. Ensure this is updated or removed for the final camera-ready version.
5.  **Fig 6 (Duty Cycle):** The y-axis label "Power Variance" should be explicitly defined in the caption (e.g., "Coefficient of Variation") to match Table IV.

---

### Overall Recommendation
**Minor Revision**

The manuscript represents a high-quality contribution to the literature on space systems coordination. The methodology is sound, and the findings regarding the superlinear scaling transition are valuable. The "Major Issues" identified above primarily concern the interpretation of systems engineering implications (mass penalty) and the visualization of projected data, rather than fundamental flaws in the simulation itself. Addressing these points will strengthen the paper's practical applicability.

---

### Constructive Suggestions

1.  **Refine the Power/Mass Argument:** In Section IV-G, add a paragraph discussing the "sizing penalty." Acknowledge that while average power is low, the specific energy density ($Wh/kg$) and power density ($W/kg$) of the satellite bus must accommodate the peak coordinator load. This strengthens the argument for the "Heterogeneous Hardware" optimization proposed later.
2.  **Split the Projected Curve:** In Figure 8, consider plotting two dashed lines: one showing "DES + Exception Telemetry" (which is validated) and a second showing "Full Projected Optimizations." This clearly delineates validated results from theoretical projections.
3.  **Sectorized Mesh Context:** In the Discussion (Section V-C), explicitly contrast the Hierarchical approach with a Sectorized Mesh in terms of *latency*. While overhead might be similar, the Hierarchical approach likely offers better latency for fleet-wide commands (O(log N) hops) vs. a Mesh (O(sqrt N) hops). This adds another dimension of defense for the Hierarchical architecture.
4.  **Link Availability "Cliff":** The finding that coordination success drops below 80% when $p_{link} < 0.6$ is critical. I suggest highlighting this "availability cliff" in the Conclusion as a specific design constraint for optical ISL hardware specifications.