---
paper: "02-swarm-coordination-scaling"
version: "bl"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-27"
recommendation: "Accept"
---

Here is a rigorous peer review of the manuscript "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version BL), prepared for *IEEE Transactions on Aerospace and Electronic Systems*.

---

### Review Criteria

**1. Significance & Novelty**
**Rating: 5 (Excellent)**

This paper addresses a critical and timely gap in the literature: the specific communication sizing requirements for autonomous coordination of mega-constellations ($10^3$--$10^5$ nodes). While existing literature covers routing in mega-constellations (Handley, Bhattacherjee) or small-scale swarm robotics (Brambilla, Dorigo), there is a distinct lack of "middle-ware" analysis that bridges the gap between high-level distributed algorithms and physical-layer link budgeting.

The derivation of closed-form sizing equations (specifically the distinction between architecture-specific overhead $\eta_0$ and workload-dependent overhead $\eta_{\text{cmd}}$) is a valuable contribution for systems engineers. The finding that command traffic, rather than topology maintenance, dominates the stress case is a significant design insight that challenges common assumptions about the cost of hierarchy. The parametric analysis of the "RF-backup" regime (1 kbps) provides a crucial lower-bound survivability criterion that is often overlooked in favor of nominal optical ISL performance.

**2. Methodological Soundness**
**Rating: 4 (Good)**

The methodology combines analytical derivations (queueing theory, TDMA framing) with a custom Cycle-Aggregated Discrete Event Simulation (DES). The cross-verification between the analytical models and the DES (showing $<0.1\%$ agreement) is a strong point, lending confidence to the results. The use of Gilbert-Elliott (GE) models to capture correlated link losses is appropriate for the LEO environment, where obstructions are often temporal rather than purely random.

However, there is a slight disconnect in the "Joint Parameter Interaction" section (IV-D). The authors note that the DES uses a fluid-server model while the analytical section relies on TDMA slotting. While the paper acknowledges this distinction, the reliance on a fluid model for the DES might underestimate the "fragmentation" losses inherent in fixed-slot TDMA, particularly when messages are of variable size (though most here seem fixed). The justification for the static topology assumption is sound for the bandwidth analysis but perhaps optimistic for latency tail statistics during cross-plane reorganization.

**3. Validity & Logic**
**Rating: 4 (Good)**

The logic flow is generally rigorous. The distinction between "byte budget" feasibility and "airtime scheduling" feasibility is a critical nuance that the authors handle well. The analysis of the "Stress Case" (unicast commands) correctly identifies the physical layer bottleneck (egress time) rather than just a throughput bottleneck.

One area requiring tighter logic is the comparison with the "Sectorized Mesh." The paper admits this is a "local-neighborhood awareness baseline" and not a full coordination architecture, yet compares overhead percentages directly. While Table V attempts to clarify the functional scope, the text occasionally conflates the two, potentially making the mesh look artificially inefficient ($65\%$ overhead vs $5\%$) without sufficiently emphasizing that the mesh provides a fundamentally different service (distributed collision avoidance vs. hierarchical command dissemination).

**4. Clarity & Structure**
**Rating: 5 (Excellent)**

The manuscript is exceptionally well-structured. The progression from research questions to model definitions, results, and discussion is logical. The use of "Design Equations" summaries in the Discussion section is very helpful for practitioners. The distinction between "Nominal," "Event," and "Stress" workloads is clear and effectively bounds the problem space.

The notation is consistent, and the tables (particularly Table I and Table VI) are informative. The inclusion of a specific "Validation Gap" section (V-A) demonstrates intellectual honesty and clear scoping.

**5. Ethical Compliance**
**Rating: 5 (Excellent)**

The authors provide a specific acknowledgment regarding the use of AI tools for ideation, citing a specific internal report/methodology. This transparency meets and exceeds current standard requirements. There are no apparent conflicts of interest or ethical concerns regarding the subject matter.

**6. Scope & Referencing**
**Rating: 5 (Excellent)**

The paper fits perfectly within the scope of *IEEE TAES*, specifically the intersection of space systems operations and electronic communication systems. The references are comprehensive, spanning classical queueing theory (Kleinrock), modern AoI literature (Yates, Kaul), and current constellation filings (SpaceX, Amazon). The inclusion of recent distributed systems work (Raft, SWIM) alongside astrodynamics references creates a well-rounded bibliography.

---

### Major Issues

1.  **Inconsistency in TDMA vs. Fluid Server Modeling (Section IV-D):**
    The paper states in Section III-A that the DES implements "fluid-server ingress, not TDMA slot scheduling," yet Section IV-A derives strict TDMA constraints (24 kbps requirement). The "Joint Parameter Interaction" verification (Table VIII) relies on the DES. Therefore, Table VIII verifies the *byte budget* interaction, not the *schedulability* interaction.
    *   *Critique:* You cannot claim to verify the "interaction" of parameters if the simulation model (fluid) lacks the constraints of the analytical model (TDMA slots). If a GE burst wipes out a specific slot in a TDMA frame, that slot is lost. In a fluid model, the bits might just be delayed.
    *   *Requirement:* The authors must explicitly clarify in Section IV-D that Table VIII validates queue dynamics and throughput, but *not* TDMA framing violations. The claim that "GE recovery and coordinator capacity equations apply independently" needs to be qualified: they apply independently to the *byte budget*, but potentially not to *latency/jitter* in a rigid frame.

2.  **Sectorized Mesh Comparison Fairness (Section III-B-4 & IV-F):**
    The comparison between Hierarchical ($\eta \approx 5\%$) and Sectorized Mesh ($\eta \approx 65\%$) is heavily emphasized. However, the mesh overhead is driven by the $O(\sqrt{N})$ neighbor assumption.
    *   *Critique:* In many sparse swarm formations, a node does not need to communicate with $\sqrt{N}$ neighbors, but rather a fixed number of metric neighbors (e.g., the $k$-nearest within range $R$). Scaling the neighbor count by $\sqrt{N}$ forces the mesh overhead to explode mathematically.
    *   *Requirement:* The authors should justify why the neighbor count *must* scale as $\sqrt{N}$ for the mesh case, or acknowledge that for constant-density swarms (where neighbor count is constant regardless of total $N$), the mesh overhead would be constant (though likely still higher than hierarchy).

---

### Minor Issues

1.  **Section IV-A, Egress Model:** The paper mentions "Type 1: Fleet-wide broadcast" and "Type 2: Per-node unicast." It states Type 2 requires 22 cycles. It would be beneficial to explicitly state if the system supports *multicast* addressing (e.g., commanding a specific cluster of 100 nodes). This is an intermediate case between broadcast and unicast that is operationally relevant.
2.  **Table VII (AoI):** The P99 AoI for $p_{exc}=0.10$ is 441s. The text compares this to a 24-hour TCA (Time of Closest Approach). It would be useful to briefly mention if this AoI is sufficient for *intra-swarm* collision avoidance (which requires faster loops) or if that is handled purely locally (bypassing the coordinator).
3.  **Equation 7 (Gamma):** The derivation $\gamma = 88.0/92.7 = 0.949$ is clear, but the decision to stick with 0.85 is called "conservative." It might be worth noting that 0.85 also helps account for the "Guard Time" potentially needing to be larger if the swarm is not perfectly synchronized (e.g., GNSS denial drift).
4.  **Reference Format:** Reference [1] and [3] are non-archival URLs. While necessary for industry data, ensure the access dates are recent (the text says "accessed Feb 2026" - assuming this is a forward-looking placeholder, please ensure this is accurate to the actual submission date).
5.  **Typos:**
    *   Section III-B-2: "RequestVote: 100 B broadcast... 51 responders required" - In Raft, the response is a `RequestVoteResponse`. The bandwidth calculation should account for the *responses* converging on the candidate, which is a many-to-one burst.
    *   Table IV: "Status reports... 205 bps". This is consistent, but ensure the header overhead is included in this bit rate.

---

### Overall Recommendation

**Accept with Minor Revisions**

This is a high-quality paper that provides a necessary theoretical foundation for the operation of large-scale satellite swarms. The analytical derivations are useful, and the simulation results are robust. The critique regarding the TDMA/Fluid model mismatch and the Mesh comparison fairness can be addressed with textual clarifications and nuanced discussion, without requiring new simulation runs.

---

### Constructive Suggestions

1.  **Add a "Hybrid" Note:** In the discussion, briefly mention that a real system might switch between Hierarchical (for nominal ops) and Sectorized Mesh (for collision avoidance/safety) dynamically. This softens the "Hierarchy vs. Mesh" dichotomy.
2.  **Refine the Raft Analysis:** For the "RF-backup handoff," explicitly model the congestion caused by 51 nodes trying to send `RequestVoteResponse` packets to the candidate simultaneously in a Slotted ALOHA channel. This is likely the bottleneck of the election, not the request itself.
3.  **Visualizing the Design Space:** Figure 9 (Topology Summary) is good, but a "Design Chart" that plots "Required Coordinator Bandwidth" vs. "Cluster Size" with contours for different $\eta$ targets would be a very "grab-and-go" tool for system architects.
4.  **Clarify "Byte Budget" vs "PHY Rate":** In the abstract and conclusion, explicitly reiterate that the "1 kbps" constraint is an *average allocated throughput*, while the radio must burst at $\geq 24$ kbps. This distinction is crucial for hardware selection and is currently buried in the text.