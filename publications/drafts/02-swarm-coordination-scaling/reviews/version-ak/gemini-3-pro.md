---
paper: "02-swarm-coordination-scaling"
version: "ak"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-27"
recommendation: "Minor Revision"
---

**Review of Manuscript Version AK**
**Journal:** IEEE Transactions on Aerospace and Electronic Systems

## Review Criteria

**1. Significance & Novelty**
**Rating: 5**
This manuscript addresses a critical and timely gap in the literature regarding mega-constellation operations. While distributed consensus and routing algorithms are well-studied, there is a scarcity of work that rigorously quantifies the "control plane" overhead for swarms of $10^4$--$10^5$ nodes using byte-level accounting. The paper’s focus on the *scaling properties* of hierarchical coordination versus mesh baselines provides concrete architectural guidance (e.g., the 21–50 kbps coordinator ingress requirement) that is directly applicable to system architects. The distinction between "message-layer" simulation and physical-layer constraints is handled with appropriate nuance, making this a valuable contribution to the systems engineering domain.

**2. Methodological Soundness**
**Rating: 4**
The use of a cycle-aggregated Discrete Event Simulation (DES) is an appropriate choice for simulating $10^5$ nodes over year-long durations; a packet-level simulation would be computationally intractable for these parametric sweeps. The authors are careful to validate their simulation against analytical closed-form solutions (e.g., $M/D/1$ queues, geometric AoI distributions), which builds confidence in the results.
*Critique:* The reliance on a MAC efficiency factor ($\gamma$) to bridge the gap between message-layer events and physical link reality is a necessary simplification, but the defense of the TDMA feasibility in Section IV-A (the "Physical-layer vignette") relies on "co-moving" clusters. The validity of the results for cross-plane links (where Doppler and pointing dynamics are more severe) is less certain and should be caveated more strongly.

**3. Validity & Logic**
**Rating: 4**
The conclusions are generally well-supported by the data. The analysis of the "Joint Parameter Interaction" (Section IV-D) is particularly insightful, demonstrating that under specific architectural assumptions (point-to-point optical ISLs), failure modes do not compound non-linearly.
*Critique:* The logic regarding the "Sectorized Mesh" neighbor discovery is slightly glossed over. The paper assumes nodes know their "10 neighbors" to gossip with. In a dynamic swarm, the *discovery* of those neighbors itself consumes bandwidth (beacons/hello messages), which does not appear to be fully accounted for in the overhead calculation, potentially underestimating the mesh overhead.

**4. Clarity & Structure**
**Rating: 5**
The manuscript is exceptionally well-organized. The progression from individual parameter characterization to joint interaction and finally to workload envelopes is logical. The distinction between "Offered" and "Delivered" overhead is maintained rigorously throughout, preventing confusion. The tables are dense but informative, and the "Roadmap" paragraph in Section IV is a helpful guide for the reader.

**5. Ethical Compliance**
**Rating: 5**
The authors provide a detailed and transparent disclosure regarding the use of AI tools for ideation in the Acknowledgments section, which complies with and exceeds standard ethical requirements. No conflicts of interest are apparent.

**6. Scope & Referencing**
**Rating: 5**
The paper fits squarely within the scope of IEEE TAES, bridging aerospace systems engineering and electronic communication systems. The references are a healthy mix of foundational theory (Kleinrock, Lamport) and contemporary operational context (Starlink, CCSDS standards).

---

## Major Issues

**1. Hardware Processing Constraints in Joint Interaction Analysis (Section IV-D)**
In Section IV-D, the authors claim that "GE retransmissions and coordinator ingress saturation are independent failure modes" because the loss occurs on the link before the queue. While this holds for *link* bandwidth, it may not hold for *processor* interrupt load. Even if a message is corrupted/lost at the link layer, the physical transceiver often still triggers an interrupt or consumes DMA cycles to handle the errored frame. At $10^5$ nodes, if a coordinator is bombarded by retransmissions (even failed ones), the CPU burden could be non-trivial. The authors should add a clarifying sentence or footnote acknowledging that this independence assumes the coordinator's CPU/interface hardware is not the bottleneck for handling physical-layer rejection of bad frames.

**2. Neighbor Discovery Overhead in Sectorized Mesh**
The Sectorized Mesh model (Section III-B-4) assumes a capped fanout where nodes gossip with neighbors. The overhead calculation (Eq. 9) accounts for the payload of these messages. However, it does not appear to account for the *neighbor discovery* process. How does a node know which 10 peers are closest without a global oracle? Typically, this requires periodic "Hello" beacons or a spatial indexing service. If the simulation uses a "god-view" oracle to assign neighbors without charging bandwidth for discovery, the mesh overhead is underestimated. The authors should clarify if discovery overhead is included or explicitly state this as a limitation.

**3. The 1 kbps Baseline Justification**
The choice of $C_{\text{node}} = 1$ kbps is central to the "high overhead" percentages reported (e.g., $\eta \approx 46\%$). While the authors justify this as an "RF backup constraint" (Section III-F), this is a very conservative lower bound for modern S-band or UHF radios, which often achieve 10–50 kbps even on nanosats. By anchoring the entire paper to 1 kbps, the results might appear alarmist (46% overhead) to readers used to Gbps ISLs.
*Recommendation:* In the Abstract and Conclusion, explicitly qualify the high overhead percentages as being specific to the *backup/safe-mode* regime. The "Dual-Regime Interpretation" (Section IV-E-3) is excellent but appears too late in the paper. A brief mention in the Introduction that "under nominal optical operation, overhead is negligible (<1%)" would prevent readers from dismissing the architecture as inefficient.

---

## Minor Issues

1.  **Table I (Simulation Parameters):** The footnote regarding collision avoidance rates ($10^{-4}$/node/s) is quite long. It might be better moved to the main text in Section III-E to improve table readability.
2.  **Section IV-A (TDMA Vignette):** The text mentions "Doppler spread... <1 Hz". Please clarify the carrier frequency assumed for this calculation (presumably S-band or similar if using RF backup logic, or optical frequency). If optical, the Doppler shift is much larger in absolute Hz, though perhaps small relative to symbol rate.
3.  **Eq. 11 (AoI Analytic):** The ceiling function brackets are used, but the text description implies a continuous geometric approximation. Ensure the notation $\lceil \dots \rceil$ is strictly intended.
4.  **Figure 5:** The dashed line for "projected overhead" is helpful, but the legend should explicitly state that the solid lines are DES-measured.
5.  **Reference 1 (Starlink):** Citing a "non-archival" website is sometimes unavoidable, but consider adding a reference to a formal FCC filing or a Jonathan McDowell (planet4589) report if available, as these are more stable citations for constellation numbers.

---

## Overall Recommendation

**Minor Revision**

This is a high-quality manuscript that offers valuable quantitative insights into the scaling limits of autonomous space swarms. The methodology is rigorous within its stated scope, and the results are non-trivial. The revisions requested are primarily clarifications regarding assumptions (neighbor discovery, CPU load) and framing (emphasizing the "backup mode" nature of the 1 kbps constraint) to ensure the results are not misinterpreted. No new simulation runs are required.

---

## Constructive Suggestions

1.  **Strengthen the "Safe Mode" Narrative:** Move the insight from Section IV-E-3 ("Dual-Regime Interpretation") up to the Introduction. Frame the paper explicitly as "Designing the Control Plane for the Worst Case (RF Backup)." This makes the 46% overhead result a feature of robustness rather than a bug of inefficiency.
2.  **Clarify Mesh Discovery:** Add a paragraph in Section III-B-4 discussing how neighbors are identified. If an Oracle is used, justify why the bandwidth cost of discovery is negligible (e.g., "Discovery beacons are piggybacked on heartbeats").
3.  **Expand on "Point-to-Point" Limitations:** In the Discussion (Section V), briefly mention that the "Independence" finding for GE losses might fail in "Bus" topologies (e.g., shared wireless medium within a cluster) where retransmissions cause collisions, unlike the dedicated ISL model used here.
4.  **AoI Operational Context:** In Section IV-B, the coupling of AoI to position error (230m along-track) is very useful. Consider adding a sentence comparing this to the typical "hard-body radius" of a satellite to emphasize that 230m uncertainty is indeed a "coarse" screening value, not a precision navigation value.