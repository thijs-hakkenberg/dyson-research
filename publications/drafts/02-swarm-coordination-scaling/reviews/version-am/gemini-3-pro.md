---
paper: "02-swarm-coordination-scaling"
version: "am"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-27"
recommendation: "Minor Revision"
---

Here is a rigorous academic peer review of the manuscript "Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study" for *IEEE Transactions on Aerospace and Electronic Systems*.

---

# Peer Review Report

**Manuscript Title:** Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study
**Target Journal:** IEEE Transactions on Aerospace and Electronic Systems
**Version:** AM

## Review Criteria

### 1. Significance & Novelty
**Rating:** 5 (Excellent)

This paper addresses a critical and timely gap in the aerospace engineering literature: the specific scaling behaviors of coordination architectures for "mega-constellations" and future autonomous swarms in the $10^4$--$10^5$ node regime. While existing literature covers small-scale swarms ($<100$ nodes) or centralized management of current constellations ($<5,000$ nodes), there is a distinct lack of rigorous quantitative analysis for the intermediate-to-large scale autonomous regime.

The novelty lies in the specific methodology: a cycle-aggregated Discrete Event Simulation (DES) that performs byte-level accounting under a fixed per-node bandwidth budget (the "RF-backup" constraint). The distinction between "message-layer" and "packet-layer" simulation allows the authors to simulate $10^5$ nodes efficiently while retaining fidelity on queueing dynamics and protocol overhead. The findings regarding the independence of Gilbert-Elliott losses and coordinator saturation under point-to-point architectures constitute a significant theoretical contribution to system reliability modeling.

### 2. Methodological Soundness
**Rating:** 4 (Good)

The methodology is generally robust. The choice of a cycle-aggregated DES is appropriate for the scale of the problem; a full packet-level simulation for $10^5$ nodes over a year would be computationally intractable. The authors are careful to validate their simulation against analytical bounds (Pollaczek–Khinchine for centralized, geometric distributions for AoI), which builds high confidence in the tool.

However, there is one area where the methodology requires tighter justification. The paper relies heavily on the "1 kbps per node" budget as a binding constraint. While the authors justify this as an RF-backup/safe-mode scenario, the interaction between this low-rate control plane and the high-rate optical data plane (used for handoffs) is treated somewhat dichotomously. The assumption that handoffs *always* succeed over optical links while routine coordination *must* fit in the RF budget is a strong design choice. It is methodologically sound as a worst-case analysis, but the paper would benefit from a sensitivity analysis where the coordination channel has access to a fraction of the optical capacity (e.g., 10 kbps or 100 kbps), to see if the topological ranking changes.

### 3. Validity & Logic
**Rating:** 5 (Excellent)

The logic is rigorous. The authors systematically decompose the problem into bandwidth, latency, and reliability components. The derivation of the coordinator capacity requirement (21–50 kbps) is mathematically sound and supported by the simulation results. The distinction between "offered" and "delivered" load is maintained consistently, preventing common accounting errors in throughput analysis.

The "Joint Parameter Interaction Verification" (Section IV-D) is particularly strong. The counter-intuitive finding—that correlated losses do not increase coordinator drops in a point-to-point architecture—is explained clearly through the logic of where the loss occurs (pre-ingress). The authors correctly identify the boundary condition for this validity (shared-medium vs. point-to-point), demonstrating a sophisticated understanding of the underlying network theory.

### 4. Clarity & Structure
**Rating:** 4 (Good)

The manuscript is well-written and structured logically. The progression from single-factor analysis (capacity, AoI, loss) to joint interaction and finally topology comparison is effective. The tables are dense but informative.

There are minor clarity issues regarding the "Sectorized Mesh" model. The distinction between "capped" and "uncapped" fanout is made, but the specific mechanism for "Inter-sector relay" (Table III) needs more explicit definition in the text. Specifically, how are boundary nodes selected? Is it dynamic or fixed? This detail affects the reproducibility of the sectorized mesh results. Additionally, the definition of $\gamma$ (MAC efficiency) is introduced late in the text relative to its importance; it should be defined formally in Section III.

### 5. Ethical Compliance
**Rating:** 5 (Excellent)

The authors include a specific "Acknowledgment" section detailing the use of AI tools (Claude, Gemini, GPT) for ideation, which complies with emerging transparency standards. The data availability statement is exemplary, providing links to code and data. There are no apparent conflicts of interest or ethical concerns regarding the research content.

### 6. Scope & Referencing
**Rating:** 5 (Excellent)

The paper fits perfectly within the scope of *IEEE TAES*, bridging the gap between electronic systems (communications/networking) and aerospace systems (constellation operations). The references are comprehensive, spanning classical distributed systems theory (Lamport, Lynch), current space networking standards (CCSDS, DTN), and recent swarm robotics literature. The inclusion of "grey literature" (FCC filings, Starlink operational reports) is necessary given the rapid commercial development in this sector and is handled appropriately.

---

## Major Issues

1.  **MAC Layer Abstraction ($\gamma$) Justification:**
    The paper applies a scalar factor $1/\gamma$ to account for MAC-layer overhead, with $\gamma \in [0.7, 0.9]$. While this is a standard engineering approximation, it is critical for the "Sectorized Mesh" results. The paper notes in Section IV-F that for contention-based mesh (CSMA), $\gamma$ could drop significantly (e.g., to Slotted ALOHA levels $\approx 0.36$).
    *   *Critique:* The comparison between Hierarchical (TDMA-friendly, high $\gamma$) and Mesh (contention-prone, low $\gamma$) is currently biased in favor of Mesh by using the same $\gamma$ range for the primary results.
    *   *Requirement:* The authors should explicitly calculate or simulate the effective $\gamma$ for the Sectorized Mesh under the specific node density and traffic load ($N=10^5$). If the Mesh relies on CSMA/CA, the overhead is likely underestimated in the current "capped fanout" results. A separate $\gamma_{mesh}$ vs $\gamma_{hier}$ parameterization is needed to make the comparison fair.

2.  **Coordinator Handoff Failure Modes:**
    Section IV-I discusses coordinator duty cycles and handoffs. The analysis assumes handoff success is determined solely by BER on the optical link.
    *   *Critique:* This ignores the logical complexity of the Raft election and state transfer synchronization. If a coordinator fails *during* the handoff window (e.g., due to the 2% annual failure rate or a GE burst), the cluster state might be inconsistent.
    *   *Requirement:* The paper should briefly address the "split-brain" or "failed handoff" scenario. Does the cluster revert to a safe mode? Does this impact the "System Availability" metric in Table X? A brief qualitative discussion or a quantitative worst-case adjustment to the availability numbers is required.

---

## Minor Issues

1.  **Table I (Sim Params):** The "Collision avoidance rate" is listed as $10^{-4}$/node/s. In the text, it is clarified that this refers to screening alerts, not maneuvers. However, this rate seems high for *alerts* requiring 128B transmissions if it implies full message generation. Please clarify if this is the rate of *computation* or *transmission*.
2.  **Section III-B-1 (Centralized):** The assumption of $\mu_s = 1,000$ msg/s for a single server seems arbitrary. While the authors state it is an "intentional worst-case bound," it would be helpful to reference a real-world benchmark (e.g., current telemetry processing rates for a standard ground station modem) to ground this number.
3.  **Equation 10 (AoI Coupling):** The linear model $\sigma_{pos} = \sigma_0 + \dot{\sigma} \cdot AoI$ is a very rough approximation. While the text acknowledges this, it would be beneficial to mention that $\dot{\sigma}$ is highly dependent on solar activity and altitude. A range of $\dot{\sigma}$ (e.g., 0.1 to 1.0 m/s) would be more robust than a single scalar.
4.  **Figure 5 (Workload Comparison):** The y-axis label should explicitly state "Offered Overhead $\eta$ (%)" to distinguish it from delivered throughput.
5.  **Typos/Formatting:**
    *   Section IV-A: "Chernoff bound... gives: $P(...) \leq ...$" - Ensure the notation for the KL divergence is standard.
    *   References: Ensure all URL access dates are consistent (some say "Feb 2026", which implies this paper is being reviewed in the future or the authors are projecting dates—please correct to current date).

---

## Overall Recommendation

**Recommendation:** **Minor Revision**

**Justification:**
This is a high-quality manuscript that makes a significant contribution to the modeling of large-scale space systems. The simulation framework is novel, the validation is thorough, and the results regarding coordinator sizing and loss independence are valuable for system architects. The "Major Issues" identified primarily concern the fairness of the comparison between topologies regarding MAC efficiency and the robustness of the handoff failure model. These can be addressed through analytical adjustments and textual clarifications without requiring a full re-simulation or major structural changes.

---

## Constructive Suggestions

1.  **Differentiate $\gamma$ by Topology:** In the final comparison (Section IV-F), explicitly penalize the Sectorized Mesh with a lower $\gamma$ (e.g., 0.4–0.5 for CSMA) compared to the Hierarchical topology (0.8–0.9 for TDMA). This will likely strengthen the case for Hierarchical coordination at scale and provide a more realistic engineering trade-off.
2.  **Expand the "Physical-Layer Vignette":** The discussion in Section IV-A regarding the 500 km cluster TDMA feasibility is excellent. Consider adding a sentence about the impact of *inter-cluster* interference. If multiple clusters are geographically adjacent, do they need frequency planning or orthogonal codes?
3.  **Refine the "RF-Backup" Narrative:** Emphasize in the Abstract and Conclusion that the results represent a "safe-mode" or "resilience" dimensioning. This clarifies that while optical links solve the *bandwidth* problem, the hierarchical architecture solves the *robustness* problem when optical links fail.
4.  **Add a "Key Takeaways for Practitioners" Box or Subsection:** Given the practical utility of the results (e.g., "Coordinators need 21-50 kbps ingress"), a summarized list of design rules-of-thumb would increase the paper's impact for industry engineers designing these constellations.