---
paper: "02-swarm-coordination-scaling"
version: "by"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-28"
recommendation: "Minor Revision"
---

## Peer Review: IEEE Transactions on Aerospace and Electronic Systems

**Manuscript ID:** [Version BY]
**Title:** Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms

### 1. Significance & Novelty
**Rating: 5**

This manuscript addresses a critical and timely gap in the literature: the scalability of command and control (C2) architectures for mega-constellations ($10^4+$ nodes). While existing literature covers networking (routing/ISL) or localized swarm control (GNC), there is a paucity of work quantifying the "management plane" traffic at this scale.

The derivation of closed-form "design equations" is a significant contribution for systems engineers. By distinguishing between byte-level feasibility, MAC efficiency ($\gamma$), and TDMA airtime, the authors provide a practical framework for sizing RF backup links—a critical safety constraint often overlooked in purely optical-ISL studies. The characterization of correlated losses via the Gilbert-Elliott model adds necessary rigor for the space environment.

### 2. Methodological Soundness
**Rating: 4**

The methodology is generally robust. The authors employ a tiered simulation approach: a cycle-aggregated Discrete Event Simulation (DES) for year-long fleet statistics, coupled with a slot-level TDMA simulator to validate timing constraints. This is an appropriate strategy to handle the computational complexity of $10^5$ nodes.

However, a notable limitation is the abstraction of the physical layer into the efficiency parameter $\gamma$. While the authors provide a sensitivity analysis for $\gamma$, the assumption that $\gamma=0.85$ is "conservative" (Abstract) may be optimistic for LEO operations involving rapid Doppler shifts and pointing acquisition, particularly in the RF backup mode. The reliance on a static cluster membership model for the duration of a year (Section III-B-2) is also a strong simplification for non-coplanar formations (e.g., Walker constellations), though the authors attempt to bound the re-association overhead analytically.

### 3. Validity & Logic
**Rating: 5**

The logical flow is excellent. The decomposition of overhead into architecture-specific ($\eta_0$) and workload-dependent ($\eta_{cmd}$) components is insightful and clarifies why previous literature often diverges on overhead estimates. The analysis of the "Stress" workload vs. "Nominal" workload effectively bounds the design space.

The conclusions regarding the infeasibility of intra-cycle ARQ under slow-mixing Gilbert-Elliott channels (Section IV-C) are mathematically sound and supported by the simulation data. The distinction between the "Sectorized Mesh" (local monitoring) and the Hierarchical architecture (cluster-wide awareness) is handled fairly; the authors correctly identify that these are functionally distinct capabilities, preventing an unfair "apples-to-oranges" comparison.

### 4. Clarity & Structure
**Rating: 4**

The paper is well-organized and written in a professional, academic tone suitable for TAES. The notation is consistent. However, the manuscript is extremely dense. Several tables (e.g., Table I, Table VI) contain extensive footnotes that contain critical analysis; this information would be better integrated into the main text to improve readability.

The distinction between the "fluid server" model used in the DES and the "slot-based" model used in the verification step is crucial but requires careful reading to grasp. Section III-A could more clearly delineate the boundaries of the two simulation tools to prevent confusion.

### 5. Ethical Compliance
**Rating: 5**

The authors include a specific acknowledgment regarding the use of AI-assisted ideation (Claude, Gemini, GPT) for the architecture concept, citing a methodology paper. This level of transparency regarding AI tools is commendable and aligns with emerging ethical standards. No conflicts of interest are apparent.

### 6. Scope & Referencing
**Rating: 5**

The paper fits squarely within the scope of TAES, bridging space systems engineering, communications, and autonomous operations. The referencing is comprehensive, connecting classical queueing theory (Kleinrock), channel modeling (Lutz), and distributed consensus (Lamport, Raft) with modern constellation literature (Starlink, Kuiper).

---

### Major Issues

1.  **Static Topology Assumption:**
    In Section III-B-2, the simulation assumes static cluster membership for one year. While valid for co-planar formations, most mega-constellations (Starlink, OneWeb) use Walker-Delta or similar configurations where planes precess and relative positions drift. While the authors argue re-association overhead is low ($<0.5\%$), the *complexity* of managing dynamic clustering (handoff logic, split-brain avoidance) is non-trivial. The paper should explicitly acknowledge that the *protocol complexity* and potential for transient state inconsistency during re-association are not captured by the byte-count analysis.

2.  **Justification of $\gamma$:**
    In Section IV-A ("TDMA frame model"), the authors derive $\gamma \approx 0.95$ based on slot structure and adopt $\gamma = 0.85$ as conservative. However, this parameter must absorb FEC, guard times, ranging, *and* control channel overheads. In many space protocols (e.g., CCSDS Proximity-1), the overhead for hailing, link establishment, and radiometrics can be significant. The claim that 0.85 is conservative needs stronger justification or a reference to specific radio hardware performance. If $\gamma$ drops to 0.6 (e.g., due to frequent re-pointing), the feasibility conclusions in Table IV change significantly.

### Minor Issues

*   **Table Footnotes:** Tables IV, VI, and X have excessively long footnotes. For example, Table IV, footnote 'a' discusses "Stress workload" vs "Baseline telemetry." This discussion belongs in the text (Section IV-B), not the table footer.
*   **Figure 5 (Fleet Reuse):** The shading for "Normal operations" vs "Correlated outages" is somewhat difficult to interpret in grayscale. Ensure the visual distinction is clear.
*   **Section IV-A (Coordinator Ingress):** The text states "Coordinator ingress is sized as...". It would be helpful to explicitly state that this assumes the coordinator is not performing other payload data downlinks simultaneously on the same radio, or that this is a dedicated control channel.
*   **Eq. 5 (Unicast Stagger):** The variable $q$ is introduced as the "fraction of stress-case commands requiring per-node unicast." Please clarify if this $q$ is a random variable or a design parameter in the equation.
*   **Typos/Grammar:**
    *   Section III-B-2: "Nominal handoff: 3--5 s (Raft election...)" - The sentence structure is a bit fragmented.
    *   Table VII: "Processing limit at c=1; propagation/spectrum limits persist." - This is very telegraphic; consider expanding for clarity.

### Overall Recommendation
**Minor Revision**

The manuscript represents a high-quality contribution with rigorous analytical and simulation-based support. The "Design Equations" are a valuable takeaway for the community. The requested revisions focus on better justifying the physical layer abstractions ($\gamma$) and acknowledging the complexities of dynamic topology beyond simple byte-counting. These changes will strengthen the paper's applicability to real-world constellation design without requiring new simulations.

### Constructive Suggestions

1.  **Expand the $\gamma$ Discussion:** Add a paragraph in Section IV-A specifically discussing the components absorbed by $\gamma$ (e.g., pilot tones, FEC rates like LDPC 1/2 vs 7/8, link acquisition time). A small table showing $\gamma$ values for common space protocols (e.g., CSP, CCSDS) would ground the $\gamma=0.85$ assumption in reality.
2.  **Dynamic Topology Sensitivity:** Since the simulation is static, consider adding an analytical "re-association budget" equation to the set of Design Equations. Express the cost of re-clustering as a function of orbital plane drift rate. This would make the framework robust for Walker constellations.
3.  **Clarify "Safe Mode" Implications:** The distinction between the 1 kbps RF backup and the optical ISL is critical. Emphasize in the Conclusion that the sizing equations are primarily driving the *backup* radio requirements, which is often the "last line of defense" for spacecraft survival.
4.  **Refactor Tables:** Move the extensive analysis currently buried in the footnotes of Tables IV, VI, and X into the main body text. This will improve the flow and ensure the reader doesn't miss key caveats.