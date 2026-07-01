---
paper: "02-swarm-coordination-scaling"
version: "bp"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-27"
recommendation: "Accept"
---

Here is a rigorous peer review of the manuscript "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version BP), prepared for *IEEE Transactions on Aerospace and Electronic Systems*.

---

### Review Criteria

**1. Significance & Novelty**
**Rating: 5 (Excellent)**

This manuscript addresses a critical and timely gap in the literature: the specific scaling properties of coordination architectures for "mega-constellations" ($10^3$--$10^5$ nodes). While existing literature covers swarm robotics (typically $<100$ agents) and traditional constellation management (centralized, $<1000$ nodes), there is a distinct lack of rigorous, closed-form sizing for the intermediate regime where bandwidth constraints and light-speed delays collide.

The derivation of "design equations" that distinguish between byte-level budgets, MAC efficiency, and TDMA airtime is a significant contribution. The paper moves beyond generic "O(N)" complexity claims to provide concrete engineering values (e.g., the 24 kbps coordinator ingress requirement). This is highly relevant to current industry developments (Starlink, Kuiper) and future autonomous architectures. The distinction between "architecture-specific" overhead ($\eta_0$) and "workload-dependent" overhead ($\eta_{cmd}$) is a valuable conceptual contribution that clarifies where the bandwidth actually goes.

**2. Methodological Soundness**
**Rating: 4 (Good)**

The methodology combines analytical derivations with a custom Cycle-Aggregated Discrete Event Simulation (DES). The approach is generally robust. The use of a Gilbert-Elliott (GE) model to capture correlated link losses is appropriate for the LEO environment (tumbling, shadowing), and the validation of the GE recovery against Markov chain predictions is strong.

However, there is a slight tension in the methodology regarding the "Message-Layer" vs. "Physical-Layer" abstraction. The authors are transparent about this (Section V-A), but the reliance on a fixed $\gamma$ (MAC efficiency) to bridge this gap is a simplification. While the derivation of $\gamma \approx 0.95$ (Eq. 7) and the conservative use of 0.85 are logical, the interaction between MAC contention and the GE burst errors in a non-TDMA fallback mode (which is discussed but not simulated) remains a minor weak point. The "fluid-server" approximation in the DES is acceptable given the analytical TDMA cross-checks, provided the limitations are clearly bounded, which the authors have done well.

**3. Validity & Logic**
**Rating: 5 (Excellent)**

The logic is tight and the conclusions follow directly from the premises. The authors successfully demonstrate that at low bandwidths (1 kbps), the system is constrained by TDMA airtime and coordinator ingress, whereas at higher bandwidths ($\geq$10 kbps), these constraints vanish. This "regime distinction" is a key insight.

The handling of the "Stress Case" (unicast commands) is particularly honest. Acknowledging that per-node unicast commands require a 22-cycle stagger (Eq. 9) rather than forcing a fit into a single cycle adds significant credibility to the analysis. The distinction between "link loss" (PHY), "queue drop" (buffer), and "deadline miss" (latency) is handled with precision. The counter-intuitive finding that exception telemetry reduces load but does not fix the GE correlated loss problem (Section IV-D) is a strong, logically sound result.

**4. Clarity & Structure**
**Rating: 5 (Excellent)**

The manuscript is exceptionally well-written. The structure is logical, moving from problem definition to model, then results, and finally discussion. The "Design Equations Summary" in Section V-C is a fantastic addition for practitioners.

The notation is consistent, and the distinction between different types of overhead ($\eta$, $\eta_0$, $\eta_{total}$) is maintained rigorously throughout. Figures are referenced appropriately, and the tables (particularly Table V and Table VIII) are dense with information but readable. The abstract is quantitative and specific, which is a strength.

**5. Ethical Compliance**
**Rating: 5 (Excellent)**

The authors provide a specific acknowledgment regarding AI assistance ("AI-assisted ideation exercise... not validated here"), which complies with emerging publication standards. Data availability is clearly stated with a GitHub link. There are no apparent conflicts of interest or ethical concerns regarding the research content.

**6. Scope & Referencing**
**Rating: 4 (Good)**

The scope is perfectly aligned with *IEEE TAES*. The references are a good mix of classical networking theory (Kleinrock, Lamport), space systems engineering (Wertz, Vallado), and recent mega-constellation literature (Handley, Del Portillo).

One minor gap is the connection to Delay Tolerant Networking (DTN) standards beyond just citing BPv7. While the paper mentions DTN is "not modeled," the "store-and-forward" nature of the hierarchical aggregation is implicitly a DTN architecture. A brief sentence explicitly positioning this hierarchy within the Bundle Protocol architecture (e.g., are coordinators acting as Custodians?) would strengthen the theoretical grounding, though it is not strictly necessary for the sizing equations.

---

### Major Issues

*None.* The paper is technically sound, mathematically consistent, and the simulation results validate the analytical models to a high degree of precision.

### Minor Issues

1.  **TDMA Guard Time Justification (Section IV-A):** The derivation of $\gamma$ (Eq. 7) assumes a guard time of 4.7 ms based on 500 km differential propagation and 2 ms turnaround. However, in a hierarchical cluster, if the coordinator is at the center, the differential delay might be smaller, but if the cluster is linear (e.g., a "train" of satellites), it could be larger. A brief mention of the cluster geometry assumption (e.g., "assuming a spherical cluster volume") would clarify the 1.7 ms propagation component.
2.  **Coordinator Failure Recovery (Section III-B-2):** The text states "RF-backup recovery: ~160 s." It mentions this is the "design-driving case." However, it would be beneficial to explicitly state the impact of this 160s outage on the *ephemeris validity*. If a node relies on updates every $T_c=10$s, a 160s outage means propagating state for 16 cycles. Is the error growth during this period acceptable for collision avoidance? A sentence referencing typical LEO error growth rates (e.g., "Along-track error grows to X meters after 160s") would contextualize the operational risk of this recovery window.
3.  **Table X (Topology Summary):** The "Scalability Limit" for the Sectorized Mesh is listed as "$>10^5$ (DES)". However, the text notes that for the mesh to work at this scale, it requires limited neighbors (capped). It might be clearer to label this "Sectorized Mesh (Capped)" in the table to avoid confusion with the $O(N^{3/2})$ uncapped version.
4.  **Eq. 9 (Unicast Stagger):** The equation uses $\alpha_{RX}$. Please ensure $\alpha_{RX}$ is explicitly defined in the text immediately preceding or following the equation. It appears to be the "ingress fraction of $T_c$," but an explicit definition would help readability.

### Overall Recommendation

**Accept**

This is a high-quality paper that provides valuable, quantitative design tools for the aerospace engineering community. It bridges the gap between abstract distributed systems theory and the concrete bandwidth/latency constraints of orbital mechanics. The combination of closed-form equations and DES validation is rigorous.

### Constructive Suggestions

1.  **Add Error Growth Context:** In Section IV-B (AoI), briefly mention the physical implication of AoI = 440s. For example, "Assuming a typical LEO drag uncertainty, a 440s stale state corresponds to an along-track error of approximately $X$ meters," to ground the abstract AoI metric in mission safety.
2.  **Clarify "Fluid Server" vs. TDMA:** In Section III-A, explicitly reiterate that while the DES uses a fluid server, the *feasibility* is checked against TDMA constraints analytically. This prevents readers from thinking the DES proves TDMA feasibility directly.
3.  **Visualizing the "Cliff":** Figure 6 (Overhead vs. Nodes) is excellent. Consider adding a vertical line or shaded region indicating where current constellations (Starlink) sit versus proposed future architectures to highlight the relevance of the $10^5$ regime.
4.  **Future Work - Geometry:** Suggest adding "dynamic cluster geometry effects on guard times" to the future work section, acknowledging that non-spherical clusters might degrade $\gamma$.