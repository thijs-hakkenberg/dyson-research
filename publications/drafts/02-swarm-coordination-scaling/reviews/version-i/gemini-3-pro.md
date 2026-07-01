---
paper: "02-swarm-coordination-scaling"
version: "i"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-23"
recommendation: "Minor Revision"
---

Here is a rigorous peer review of the provided manuscript, written from the perspective of an expert reviewer for *IEEE Transactions on Aerospace and Electronic Systems*.

***

# Peer Review Report

**Journal:** IEEE Transactions on Aerospace and Electronic Systems
**Manuscript ID:** [Version I]
**Title:** Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study
**Date:** October 26, 2023

## 1. Significance & Novelty
**Rating: 5 (Excellent)**

This manuscript addresses a critical and rapidly emerging problem in aerospace engineering: the scalability of command and control architectures for "mega-constellations" and future autonomous swarms. While the literature is rich with studies on small-scale swarms ($N < 100$) and traditional constellation management ($N < 10^4$), there is a significant gap in quantitative analysis for the intermediate regime ($10^4$ to $10^6$ nodes). As commercial entities like SpaceX and Amazon Kuiper push into tens of thousands of satellites, and future concepts look toward millions, this work is timely and highly relevant.

The novelty lies in the systematic comparison of three distinct topologies (Centralized, Hierarchical, Global-State Mesh) using a Discrete Event Simulation (DES) that measures overhead directly from byte counts rather than relying solely on analytical abstractions. The demonstration of $O(1)$ overhead percentage scaling for hierarchical architectures is a significant finding that provides a theoretical foundation for future constellation network design. The specific parameterization of coordinator bandwidth and the "U-shaped" optimization curve for cluster size provide actionable design guidelines for system architects.

## 2. Methodological Soundness
**Rating: 4 (Good)**

The methodology is generally robust. The move from analytical formulas to direct DES byte counting (as noted in the transition from Version G to H) significantly strengthens the validity of the results. The use of Monte Carlo methods with bootstrap confidence intervals is appropriate for capturing stochastic variability in failure rates and message timing.

However, there is a notable tension in the "Global-State Mesh" baseline. The authors define this as an "intentional upper bound" requiring global state convergence for every node. While this serves as a valid theoretical ceiling, it is perhaps too much of a "straw man." A sectorized mesh (which the authors identify as future work) is the actual competitor to hierarchical systems. Comparing a hierarchical system against a mesh system forced to behave globally creates a somewhat lopsided comparison.

Additionally, the coordinator bandwidth parameterization ($C_{coord}$) is a welcome addition, but the assumption that coordinator nodes can simply "pool" the bandwidth of their cluster members ($100 \times 1$ kbps) requires stronger justification regarding the physical link layer. Is this achieved via multiple transceivers, wider channels, or time-slot aggregation? The paper treats this largely as a logic-layer parameter rather than a physical-layer constraint.

## 3. Validity & Logic
**Rating: 4 (Good)**

The conclusions logically follow from the simulation data. The identification of the $k_c \approx 100$ sweet spot is well-supported by the trade-off between inter-cluster traffic and intra-cluster serialization delay. The analysis of the duty cycle trade-offs (power variance vs. handoff risk) is insightful and adds practical engineering value.

The validation of exception-based telemetry is strong, showing high agreement between analytical predictions and DES measurements. The logic regarding the "robust operating regime" for link availability ($p_{link} \geq 0.5$ with retransmission) is sound, though it relies on the assumption that link failures are independent Bernoulli trials. In reality, link failures in LEO are often correlated (e.g., geometric occlusion, solar storms, or regional interference). The authors acknowledge this in the limitations, but it remains a threat to validity for the specific quantitative thresholds reported.

## 4. Clarity & Structure
**Rating: 5 (Excellent)**

The paper is exceptionally well-written. The structure is logical, moving from problem definition to simulation framework, results, and discussion. The distinction between "Baseline Telemetry" (topology-invariant) and "Protocol Overhead" is crucial and is explained with high clarity.

The tables are dense but informative, particularly Table V (Duty Cycle Trade-offs) and Table VII (Link Availability). The figures are referenced appropriately, and the captioning is descriptive. The explicit "Traffic Accounting" section (Table III) is a best-practice inclusion that ensures reproducibility and clarity regarding what is and isn't included in the $\eta$ metric.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**

The authors provide a transparent disclosure regarding the use of AI tools for ideation in the Acknowledgments section, citing a companion methodology paper. This aligns with emerging standards for AI transparency in research. There are no apparent conflicts of interest or ethical concerns regarding the subject matter.

## 6. Scope & Referencing
**Rating: 4 (Good)**

The scope is well-suited for *IEEE TAES*. The references are a good mix of classical distributed systems theory (Lamport, Lynch), standard space engineering texts (SMAD), and recent literature on mega-constellations and swarm robotics.

One minor gap is the lack of reference to specific Delay Tolerant Networking (DTN) routing protocols beyond the general BPv7 citation. Since the mesh and hierarchical handoffs involve store-and-forward mechanics, citing specific routing algorithms (e.g., CGR - Contact Graph Routing) would strengthen the connection to existing space networking standards.

---

## Major Issues

1.  **The "Straw Man" Mesh Baseline:**
    The paper compares the Hierarchical architecture against a "Global-State Mesh" where every node must know the trajectory of every other node ($O(N^2)$). While the authors explicitly state this is an upper bound, it risks overstating the relative advantage of the hierarchical approach. In a real collision avoidance scenario, a mesh node only needs state from neighbors within a kinematic screening volume.
    *   *Requirement:* The authors should either (a) include a "Sectorized Mesh" estimation in the comparison graphs (even if analytical) to show where a realistic mesh would fall, or (b) explicitly qualify the "Global-State Mesh" in the abstract and conclusion as a "worst-case theoretical bound" rather than a "decentralized baseline," to avoid misleading readers about the viability of mesh networks.

2.  **Physical Layer Abstraction of Coordinator Bandwidth:**
    In Section IV-G, the paper states: "we assumed coordinators could pool the combined coordination bandwidth of their cluster members." This is a massive physical layer assumption. If a node has a single antenna/transceiver, it cannot arbitrarily increase its bandwidth just because it is designated a coordinator.
    *   *Requirement:* The paper must clarify the physical realization of this bandwidth. Does the coordinator have different hardware? Or does the TDMA schedule allocate 100 slots to the coordinator? If it is the latter, the *total* system capacity is constant, and giving the coordinator $100\times$ bandwidth means starving other nodes. The implications of this resource allocation need to be explicit.

## Minor Issues

1.  **Section III-A (Simulation Framework):** The text mentions "one-second resolution applies only to collision avoidance events," but later discusses routine events at $T_c = 10$s. Clarify if the simulation steps are fixed at 1s or if it is a variable-step DES.
2.  **Table I (Scalability Sensitivity):** The column header $N_{max}$ should likely specify that this is a *processing* limit, distinct from bandwidth limits.
3.  **Equation 5 (Hierarchy):** The term $\frac{N}{k_c \cdot k_r}$ represents the regional-to-ground traffic. Ensure the text clarifies that this is the volume *entering the ground station*, not the total volume in the ether.
4.  **Section IV-H (Power Budget):** The calculation $\Delta P_{avg} = 0.15$ W assumes the power cost is averaged over the whole cluster. However, for the specific node acting as coordinator, the thermal load is $3\times$ higher (15W vs 5W). The thermal design must size for the *peak* (15W), not the average. Please add a sentence acknowledging that thermal hardware cannot be "averaged" like power generation.
5.  **References:** Reference [1] and [3] are non-archival websites. If possible, replace with or add white papers or FCC filings which are more permanent records of Starlink/Kuiper operational parameters.

## Overall Recommendation
**Minor Revision**

The manuscript represents a high-quality contribution to the field of large-scale space systems coordination. The simulation is rigorous, and the findings regarding hierarchical scaling are significant. The revisions requested are primarily to clarify physical layer assumptions regarding coordinator bandwidth and to nuance the comparison against the mesh topology to ensure the claims are not overstated.

## Constructive Suggestions

1.  **Add a "Sectorized Mesh" Projection:** In Figure 2 (Overhead Scaling), add a dotted line representing the analytical cost of a Sectorized Mesh (as discussed in Section V-C). This would visually contextualize the Hierarchical solution between the "Global Mesh" ceiling and a more realistic decentralized alternative.
2.  **Clarify TDMA vs. Hardware:** In the Coordinator Bandwidth section, explicitly state that achieving $C_{coord} \geq 25$ kbps requires either (a) a dedicated high-rate radio on all nodes (increasing SWaP), or (b) a TDMA scheme where the coordinator consumes 25 time slots for every 1 slot used by a member node.
3.  **Thermal Sizing Note:** In the discussion on duty cycles, mention that while *energy* storage can smooth the power requirement, *thermal radiators* must be sized for the peak 15-20W load, which imposes a mass penalty on every node in the swarm if the coordinator role rotates.
4.  **Collision Rate Sensitivity:** The collision avoidance rate is set to $10^{-4}$/node/s. Briefly mention how sensitive the results are to this parameter. If the environment becomes dirtier (Kessler syndrome), does the hierarchical system choke before the mesh system? A sentence or two in the discussion would add robustness.