---
paper: "02-swarm-coordination-scaling"
version: "av"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-27"
recommendation: "Minor Revision"
---

Here is a rigorous peer review of the manuscript "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version AV), prepared for *IEEE Transactions on Aerospace and Electronic Systems*.

***

# Peer Review Report

**Manuscript ID:** [Version AV]
**Title:** Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms
**Target Journal:** IEEE Transactions on Aerospace and Electronic Systems

## 1. Significance & Novelty
**Rating: 5 (Excellent)**

This manuscript addresses a critical and timely gap in the literature: the scalability of coordination architectures for "mega-constellations" ($10^3$--$10^5$ nodes). While existing literature covers routing (networking) or orbital mechanics (astrodynamics) in isolation, there is a scarcity of work that rigorously couples byte-level traffic accounting with architectural sizing for autonomous operations. The specific focus on the "RF-backup regime" (1 kbps budget) is highly relevant for resilience engineering, a topic of increasing interest to both commercial (Starlink, Kuiper) and defense sectors.

The derivation of closed-form design equations, validated by discrete event simulation (DES), provides a practical toolkit for system architects. The distinction between "pipeline decoupling" in point-to-point links versus shared media is a subtle but operationally significant theoretical contribution. The paper moves beyond generic "scalability" claims to provide concrete sizing parameters (e.g., coordinator ingress of 21–50 kbps), which is exactly the type of engineering data required by the *TAES* readership.

## 2. Methodological Soundness
**Rating: 4 (Good)**

The methodology is generally robust, combining analytical derivations (queueing theory, Markov chains) with a custom cycle-aggregated DES. The use of a Gilbert-Elliott (GE) model to capture correlated link losses is appropriate for the space environment, where fading or attitude loss often persists over multiple seconds. The validation of the DES against analytical bounds (Pollaczek–Khinchine, gossip convergence) builds confidence in the results.

However, there is one area that requires clarification. The paper asserts that the "point-to-point pipeline architecture" decouples GE retransmissions from coordinator saturation. While analytically sound under the assumption of dedicated links (e.g., optical or directed RF), the paper applies this to an "RF-backup" scenario. In many small-sat implementations, backup RF is omnidirectional and shared-medium (e.g., S-band Aloha or CSMA). The authors acknowledge this in Section IV-D and V-B, but the abstract and conclusion present the "decoupling" as a general property of the hierarchy. This distinction needs to be sharper: the decoupling is a function of the *link topology* (dedicated vs. shared), not just the hierarchical *logic*.

Additionally, the derivation of $\gamma = 0.949$ (Eq. 8) seems optimistic for a backup RF link with potential Doppler shifts and synchronization jitters typical of low-cost swarms. The authors wisely retain $\gamma = 0.85$ for conservative sizing, but a more detailed justification of the guard times for $N=10^5$ constellations (where differential Doppler can be significant) would strengthen the physical layer abstraction.

## 3. Validity & Logic
**Rating: 5 (Excellent)**

The conclusions are well-supported by the data. The paper does an excellent job of bounding the problem: defining the "Stress," "Nominal," and "Event-driven" workloads allows the reader to understand the operational envelope. The analysis of the "Sectorized Mesh" as an intermediate comparator is fair and insightful, demonstrating that even with locality optimizations, mesh architectures suffer from higher overhead than hierarchies under command-heavy workloads.

The treatment of Age of Information (AoI) is logical. The finding that exception-based telemetry degrades P99 AoI to ~440s is a crucial operational constraint that is rightly highlighted. The logic regarding coordinator duty cycles (Table XI) is sound, balancing power variance against handoff risks.

## 4. Clarity & Structure
**Rating: 5 (Excellent)**

The manuscript is written with high clarity and precision. The structure is logical, moving from problem definition to modeling, results, and discussion. The use of "Research Questions" (RQ1-RQ3) in the introduction helps frame the contributions.

The tables are particularly effective. Table IV (Traffic Accounting) and Table X (Topology Comparison) provide dense, valuable information at a glance. The distinction between "offered" and "delivered" overhead is maintained consistently, which is often a source of confusion in networking papers. The LaTeX formatting is professional, and the equations are clearly typeset.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**

The authors include a specific "Acknowledgment" section detailing the use of AI tools (Claude, Gemini, GPT) for ideation, citing a specific methodology paper. This level of transparency regarding AI assistance is exemplary and exceeds current standard practices. There are no apparent conflicts of interest or ethical concerns regarding the research content.

## 6. Scope & Referencing
**Rating: 4 (Good)**

The scope is well-aligned with *TAES*. The referencing is generally strong, covering the necessary bases of swarm robotics, constellation operations, and networking.

However, the references regarding "mega-constellation" operations rely heavily on non-archival sources (FCC filings, web pages) or somewhat dated texts (Wertz, 2011). While this is understandable given the proprietary nature of current systems (Starlink), the paper would benefit from including more recent academic work on *Software Defined Satellite Networks (SDSN)* or *Space Information Networks (SIN)* to ground the networking assumptions in the latest peer-reviewed literature.

***

## Major Issues

1.  **MAC Layer Assumption in Abstract/Conclusion:** The Abstract states: *"By the point-to-point pipeline architecture, GE retransmissions and coordinator saturation decouple."* This is a strong claim that relies entirely on the assumption that the "RF-backup" uses dedicated links (e.g., CDMA or directed beams) rather than a shared medium. If the backup is a simple omni-directional S-band using Slotted Aloha (common for safe-mode), retransmissions *do* increase collision probability, thus coupling loss and saturation.
    *   *Requirement:* Qualify this statement in the Abstract and Conclusion. Specify that this holds only for *dedicated* or *orthogonal* links (like TDMA/FDMA), not shared-medium contention access.

2.  **TDMA Synchronization at Scale:** The paper assumes a TDMA frame efficiency $\gamma \approx 0.85-0.95$. For a swarm of $10^5$ nodes, maintaining the precise time synchronization required for efficient TDMA over low-bandwidth backup links is a non-trivial distributed systems problem.
    *   *Requirement:* Add a brief discussion or calculation regarding the synchronization overhead. If the swarm relies on GNSS for time, state this. If it requires internal synchronization over the 1 kbps link, the overhead for time-sync messages needs to be accounted for or justified as negligible.

## Minor Issues

1.  **Table I (M/D/c Sensitivity):** The table lists $N_{max}$ values based purely on processing capacity. It would be helpful to add a column or footnote explicitly stating that RF spectrum/uplink slots are the actual bottleneck for the centralized case, reinforcing the text in Section III-B-1.
2.  **Eq. 8 (Gamma Derivation):** The guard time calculation ($T_{guard} = 4.7$ ms) assumes a 500 km cluster diameter. Please clarify if this accounts for the worst-case relative velocity (Doppler shift) impact on symbol timing, or if it is purely propagation delay + turnaround.
3.  **Section IV-C (GE Model):** The text states, "The assumption is conservative: if the channel coherence time were shorter... some intra-cycle retries would succeed." Please verify this logic. If the channel oscillates rapidly (fast fading), you might get a success *or* a failure. The current block-fading assumption (constant for $T_c$) is indeed conservative for *recovery*, but it might be optimistic for *burst error length* if real outages last $>10s$. A brief sentence clarifying that $T_c=10s$ is likely shorter than many physical obstructions (e.g., antenna shadowing) would be beneficial.
4.  **Typos/Formatting:**
    *   Section III-A: "Palm--Khintchine" (spelling check).
    *   Table VI: "Coord. commands... ~410 bps" - clarify if this is average or peak.
    *   Fig. 5 caption: "Geometric growth..." - ensure the figure axes are clearly labeled with units.

## Overall Recommendation
**Minor Revision**

This is a high-quality paper that makes a significant contribution to the engineering of large-scale space systems. The analytical and simulation work is rigorous. The requested revisions focus on scoping the claims regarding MAC-layer decoupling and adding necessary physical-layer context (synchronization) to support the design equations. Once these clarifications are made, the paper is highly recommended for publication.

## Constructive Suggestions

1.  **Refine the "Decoupling" Claim:** In the Introduction and Discussion, explicitly contrast the "Hierarchical + TDMA/Dedicated Link" case (decoupled) vs. "Hierarchical + CSMA/Aloha" case (coupled). This adds nuance and prevents readers from misapplying the result to shared-spectrum radios.
2.  **Add a "Synchronization" Parameter:** In your design equations summary (Section V-C), consider adding a term or note for time-synchronization traffic. Even if it is small (e.g., 10 bytes/cycle), acknowledging it makes the "toolkit" more complete for practitioners.
3.  **Expand on "Cluster Re-association":** The discussion in Section V-B regarding cross-plane drift is excellent. Consider moving the key quantitative finding (overhead < 0.5%) to the Abstract or Conclusion to preempt reviewer concerns about dynamic topologies.
4.  **Visualizing the Design Space:** Figure 12 (Topology Summary) is good, but a "Design Chart" plotting *Coordinator Bandwidth Required* (y-axis) vs. *Cluster Size* (x-axis) with contours for different *Packet Loss Rates* would be a very powerful tool for the "Parametric Sizing" promised in the title.