---
paper: "02-swarm-coordination-scaling"
version: "y"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-24"
recommendation: "Minor Revision"
---

Here is the peer review for the manuscript "Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study" (Version Y).

***

# Peer Review Report
**Journal:** IEEE Transactions on Aerospace and Electronic Systems
**Manuscript ID:** [Assigned by Editor]
**Title:** Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study

## Review Criteria

### 1. Significance & Novelty
**Rating: 4 (Good)**

The manuscript addresses a timely and critical problem in aerospace engineering: the scalability of command and control architectures for mega-constellations and future autonomous swarms ($10^3$--$10^5$ nodes). While the current literature covers small-scale swarms ($<100$ nodes) or centralized management of existing constellations, there is a significant gap regarding the "middle ground" of autonomous, hierarchical coordination at the $10^5$ scale. The paper's focus on byte-level traffic accounting and the specific comparison of hierarchical vs. mesh architectures under a fixed bandwidth budget is a valuable contribution.

The novelty lies less in the proposal of hierarchical control (which is a standard pattern) and more in the rigorous parametric characterization of its limits using Discrete Event Simulation (DES). The quantification of the "zero-drop" coordinator bandwidth thresholds and the specific Age-of-Information (AoI) trade-offs for exception-based telemetry provide actionable engineering data. However, the significance is slightly tempered by the reliance on somewhat idealized link models, though the authors attempt to mitigate this with the Gilbert-Elliott analysis.

### 2. Methodological Soundness
**Rating: 4 (Good)**

The methodology is generally robust. The choice of a cycle-aggregated DES is appropriate for the scale of the problem ($10^5$ nodes), as packet-level simulation would be computationally prohibitive. The authors are transparent about their abstractions (Table IV is excellent). The validation against closed-form analytical solutions (Section III-A and IV-E) builds confidence in the simulation engine.

However, there is a tension in the "Coordinator Bandwidth" analysis (Section IV-G). The paper compares unscheduled access (random phase) against TDMA. While the derivation of the 50 kbps vs. 24 kbps threshold is sound, the assumption that a swarm of $10^5$ nodes can maintain the precise synchronization required for TDMA ($\gamma=0.85$) without a detailed synchronization model is a strong one. Additionally, the exclusion of handoff state transfers from the primary overhead metric ($\eta$) is justified by the use of a separate optical ISL, but this creates a "hidden cost" that should be more fastidiously tracked in the power/complexity analysis.

### 3. Validity & Logic
**Rating: 5 (Excellent)**

The conclusions are well-supported by the data. The authors are careful to frame the centralized and global-state mesh architectures as "intentional bounds" rather than strawmen, which strengthens the logical positioning of the hierarchical approach. The analysis of the Gilbert-Elliott link model (Section IV-J) is particularly strong, logically demonstrating why intra-cycle retransmission fails in correlated loss environments.

The distinction between "delivered overhead" and "offered load" in Table XII is a crucial logical step often missed in networking papers; the authors handle this correctly. The argument regarding Age-of-Information (AoI) is also logically sound: the trade-off between bandwidth savings ($p_{exc}=0.10$) and state staleness (P99 > 400s) is clearly quantified and interpreted within the context of orbital mechanics (along-track uncertainty).

### 4. Clarity & Structure
**Rating: 5 (Excellent)**

The manuscript is exceptionally well-written. The structure is logical, moving from problem definition to simulation design, then results, and finally discussion. The use of tables to summarize simulation parameters (Table III) and traffic accounting (Table VI) ensures reproducibility. The figures are described clearly in the text. The distinction between the "message layer" and "physical layer" is maintained consistently throughout.

### 5. Ethical Compliance
**Rating: 5 (Excellent)**

The authors provide a specific acknowledgment regarding the use of AI tools for "ideation" in the Acknowledgment section, citing a companion methodology paper. This transparency meets and exceeds current ethical standards for AI disclosure. No conflicts of interest are apparent.

### 6. Scope & Referencing
**Rating: 4 (Good)**

The paper fits perfectly within the scope of *IEEE TAES*, specifically the areas of space systems and command and control. The referencing is adequate, covering standard texts (Wertz, Kleinrock) and recent relevant work (Starlink operations, AoI literature).

However, the references regarding optical Inter-Satellite Links (ISLs) could be strengthened. The paper relies heavily on the assumption of 1-10 Gbps optical links for handoffs. References to specific hardware capabilities or standards (beyond CCSDS) would bolster the feasibility of the "separate channel" assumption.

---

## Major Issues

1.  **TDMA Synchronization Feasibility:**
    In Section IV-G and IV-H, the paper argues that TDMA reduces the coordinator ingress requirement from 50 kbps to 24 kbps. This relies on a MAC efficiency $\gamma = 0.85$. Achieving this efficiency requires tight time synchronization. In a swarm of $10^5$ nodes with high relative velocities (Doppler) and potential GPS denial (or reliance solely on ISL ranging), maintaining slot boundaries to this precision is non-trivial. The paper treats $\gamma$ as a parameter, but does not discuss the *cost* (in terms of protocol overhead) of maintaining that synchronization. If synchronization messages are required, they must be added to the traffic accounting in Table VI.

2.  **Handoff Channel "Free Lunch":**
    The paper excludes handoff state transfers (10-50 MB) from $\eta$ because they use a "dedicated optical ISL." While valid for bandwidth accounting on the coordination channel, this implies that the optical ISL is always available and idle. In a real mega-constellation, optical ISLs are the primary backbone for user data (internet traffic). Using them for control plane handoffs introduces contention with revenue-generating traffic. The paper should at least estimate the *utilization* of the optical ISL caused by handoffs to prove it is indeed negligible compared to user traffic.

---

## Minor Issues

1.  **Table VII (Traffic Accounting):** The footnote regarding Collision Avoidance alerts states that the DES models "only the alert and command messages." However, in Section III-A, the event rate is given as $10^{-4}$/node/s. It would be helpful to clarify if this rate includes false positives from the screening process, as raw conjunction rates are much lower. (The text attempts to clarify this in Section III-E, but the link between the rate and the table could be tighter).
2.  **Figure 6 (AoI):** The caption mentions "mean AoI approximately triples." It would be helpful to explicitly state the reference value in the caption for quick reading (e.g., "triples from 4.9s to ~15s").
3.  **Section IV-C (Duty Cycle):** The paper discusses power variance. It mentions "coordinators consume 15-20W versus the 5W baseline." Is this purely communication power, or does it include the compute power required to process the $k_c$ incoming messages? A brief clarification on the power model assumptions would be beneficial.
4.  **Equation 11 (Analytical Crosscheck):** The equation is dense. Breaking it down or defining the terms $N(1-1/k_c)$ more explicitly in the text immediately preceding it would improve readability.
5.  **Typos/Formatting:**
    *   Section III-B-1: "The binding constraints... are propagation latency... and uplink spectrum scarcity." Consider adding "ground station visibility windows" if applicable, or clarify if continuous coverage is assumed via a relay.
    *   References: Ensure all URLs in the bibliography have access dates (some do, check consistency).

---

## Overall Recommendation
**Minor Revision**

The manuscript represents a high-quality contribution to the field of autonomous space systems. The simulation framework is rigorous, and the results provide valuable quantitative bounds for system architects. The major issues identified regarding TDMA synchronization costs and optical ISL contention do not invalidate the results but require additional discussion and perhaps a sensitivity analysis or a "synchronization overhead" term to be fully rigorous.

---

## Constructive Suggestions

1.  **Add a "Synchronization Cost" Term:** In the discussion of TDMA (Section IV-H), introduce a variable for synchronization overhead (e.g., $\eta_{sync}$). Even if you set it to 0 for the baseline, acknowledging that $\gamma=0.85$ implies a non-zero $\eta_{sync}$ for clock discipline would make the physical layer abstraction more robust.
2.  **Quantify Optical ISL Load:** Add a short paragraph or table row estimating the optical ISL utilization fraction used by handoffs. Even if it is $0.01\%$, showing the number explicitly defends the decision to exclude it from the main bottleneck analysis.
3.  **Expand on "Sectorized Mesh":** The comparison between Hierarchical and Sectorized Mesh is one of the most interesting parts of the paper. Consider adding a specific plot (perhaps a subplot in Fig. 8) that shows the "crossover point" where Sectorized Mesh might become more efficient than Hierarchical, or explicitly stating that Hierarchical dominates across the whole $10^3-10^5$ range if that is the case.
4.  **Refine the Abstract:** The abstract is dense with numbers. Consider rounding the "2.8 km" uncertainty to "~3 km" for readability, as the precision suggests a specific orbital altitude that isn't the main focus.
5.  **Future Work - Dynamic Clustering:** You mention dynamic spatial partitioning as future work. A brief sentence speculating on how this would impact the "handoff" overhead (likely increasing it) would show foresight.