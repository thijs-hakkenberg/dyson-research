---
paper: "02-swarm-coordination-scaling"
version: "ac"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-27"
recommendation: "Minor Revision"
---

Here is a rigorous peer review of the manuscript "Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study" (Version AC), prepared for *IEEE Transactions on Aerospace and Electronic Systems*.

---

### Review Criteria

**1. Significance & Novelty**
**Rating: 4 (Good)**

The paper addresses a critical and timely gap in the aerospace engineering literature: the scalability of coordination architectures for "mega-constellations" and future autonomous swarms in the $10^3$--$10^5$ node regime. While existing literature covers small-scale swarms ($<100$ nodes) or centralized constellation management, the specific focus on the "middle ground" of hierarchical autonomy with explicit byte-level accounting is valuable.

The novelty lies less in the invention of new protocols—hierarchical aggregation is a standard distributed systems technique—and more in the rigorous *parametric characterization* of these techniques applied to the specific constraints of orbital mechanics and limited-bandwidth inter-satellite links. The integration of Age-of-Information (AoI) metrics with physical orbital uncertainty (Equation 13) is a particularly strong contribution, bridging the gap between networking theory and astrodynamics.

**2. Methodological Soundness**
**Rating: 5 (Excellent)**

The methodology is the strongest aspect of this work. The authors have constructed a custom cycle-aggregated Discrete Event Simulation (DES) that strikes an intelligent balance between fidelity and computational feasibility. By abstracting bit-level physical layer events but retaining message-level queuing, drops, and byte accounting, the authors can simulate $10^5$ nodes—a scale often unreachable by packet-level simulators like NS-3 without massive computing resources.

The validation approach is exemplary. The authors cross-check their simulation results against closed-form analytical bounds (e.g., $M/D/1$ queuing, geometric AoI distributions) and report the delta ($<0.1\%$). The inclusion of a Gilbert-Elliott loss model to test correlated failures adds significant robustness compared to standard Bernoulli loss models. The distinction between "offered load" and "carried load" is handled with precision.

**3. Validity & Logic**
**Rating: 4 (Good)**

The conclusions are generally well-supported by the data. The derivation of the coordinator capacity requirement (21–50 kbps) is logically sound and robust across different scheduling assumptions (TDMA vs. random phase). The comparison against the "Sectorized Mesh" provides a fair decentralized baseline, avoiding the strawman argument of comparing only against a global-state mesh.

However, there is a slight logical tension regarding the "Stress Case" workload. The paper admits this is an extreme bound ($>$60% of traffic is commands), yet the headline overhead figure ($\eta \approx 46\%$) relies heavily on this assumption. While the authors do decompose this in Section IV-D, the abstract and conclusion lean heavily on the 46% figure, which might mislead readers about the cost of *maintenance* operations versus *active* campaigning.

**4. Clarity & Structure**
**Rating: 5 (Excellent)**

The manuscript is written with high clarity and professional polish suitable for IEEE TAES. The structure is logical, moving from architecture definition to simulation design, then results, and finally discussion. The distinction between "Baseline Telemetry" (topology-invariant) and "Protocol Overhead" is defined early and used consistently, preventing confusion.

The tables are particularly effective. Table I (M/D/c sensitivity) and Table X (Coordinator Bandwidth) provide immediate, actionable engineering data. The use of specific line items for byte-level accounting (Table VII) ensures reproducibility.

**5. Ethical Compliance**
**Rating: 5 (Excellent)**

The authors provide a transparent "Acknowledgment" section detailing the use of AI tools (Claude, Gemini, GPT) for ideation, which aligns with emerging publication standards. The data availability statement is robust, promising open-source code and configuration files. There are no apparent conflicts of interest or ethical concerns regarding the research content.

**6. Scope & Referencing**
**Rating: 4 (Good)**

The scope is well-aligned with TAES, specifically the "Space Systems" and "Command and Control" interest areas. The referencing is adequate, covering standard texts (Wertz, Vallado), classical distributed systems (Lamport, Lynch), and recent mega-constellation studies (Handley, Del Portillo).

One minor gap is the lack of comparison to specific CCSDS standards beyond BPv7. While Proximity-1 is mentioned, a brief discussion of CCSDS File Delivery Protocol (CFDP) overhead in the context of the "reliable" transfer assumption would strengthen the link to operational reality.

---

### Major Issues

1.  **MAC Layer Efficiency ($\gamma$) Justification:**
    The paper applies a scalar penalty $\gamma \in [0.7, 0.9]$ to account for MAC-layer inefficiencies (Section III-F and IV-E). While this is a necessary abstraction for a cycle-aggregated DES, the value range is asserted rather than derived. In dense swarms ($k_c = 100$ nodes per cluster) sharing a single frequency channel, hidden terminal problems and contention could drive efficiency significantly lower than 0.7 if using CSMA, or require substantial guard times if using TDMA.
    *   *Requirement:* The authors should either provide a citation justifying $\gamma=0.7-0.9$ for a 100-node orbital network or include a brief sensitivity analysis showing what happens if $\gamma$ drops to 0.3–0.5 (Slotted ALOHA levels). If the system breaks at $\gamma=0.5$, this is a critical stability boundary.

2.  **Coupling of AoI to Position Error (Eq. 13):**
    The mapping of P99 AoI (441s) to position error ($\sigma_{pos} \approx 230$m) using a linear drift model ($\dot{\sigma} = 0.5$ m/s) is useful but potentially dangerous if over-interpreted. In LEO, along-track error grows quadratically with time due to drag uncertainty, not linearly, over long intervals.
    *   *Requirement:* The authors must clarify that Eq. 13 is a *linearized approximation* valid only for short timescales. If 441s is "short" enough for linearity to hold, state this explicitly with a reference to orbital dynamics literature. If quadratic growth applies, the error at 441s could be significantly higher, potentially altering the conclusion about conjunction screening suitability.

---

### Minor Issues

1.  **Table VII (Traffic Accounting):** The table lists "Gossip exchange (mesh)" with size $256 \times b$. The footnote explains $b$, but it would be helpful to explicitly state the typical byte volume per cycle for the mesh case in the table body or caption for quick comparison with the hierarchical rows.
2.  **Section IV-A (Coordinator Capacity):** The text mentions "Model A" and "Model B" for coordinator ingress. It would be clearer to rename these in the text to "Deadline Model" and "Leaky-Bucket Model" to match the intuitive descriptions in Table IX.
3.  **Abstract:** The phrase "design envelope ($\eta \in [5\%, 46\%]$)" is slightly confusing without context. It might be clearer to say "workload-dependent overhead ranges from 5% (nominal) to 46% (stress-case)."
4.  **Section I-A (Introduction):** The citation [starlink_ops] is a non-archival website. If possible, replace or supplement with a filed FCC application or a peer-reviewed observation paper regarding Starlink's architecture to improve archival durability.
5.  **Section III-B-2:** The paper states "The downward command traffic approximately doubles the overhead." Please clarify if this assumes unicast commands to every node or broadcast commands. If unicast, the scaling is linear; if broadcast, it is constant. The text implies unicast ($N$ messages), but this should be explicit.

---

### Overall Recommendation

**Minor Revision**

This is a high-quality paper that makes a solid contribution to the field of space systems engineering. The simulation framework is rigorous, and the results are presented with admirable clarity. The "Major Issues" identified above do not invalidate the results but require better justification (MAC efficiency) and tighter physical definitions (AoI-to-error mapping) to ensure the conclusions are robust. Once these clarifications are made, the paper should be accepted.

---

### Constructive Suggestions

1.  **Add a "MAC Sensitivity" Plot:** In Figure 11 (Sensitivity Sweep), consider adding a line or region showing the impact of $\gamma$ dropping to 0.3 (Slotted ALOHA limit). This would visually demonstrate the necessity of TDMA/Token-Bucket scheduling for the hierarchical architecture.
2.  **Refine the AoI Discussion:** In Section IV-B, explicitly contrast the linear error growth assumption against a quadratic drag model. Even a single sentence acknowledging that "Quadratic drag effects would increase $\sigma_{pos}$ to approx $X$ meters, further reinforcing the need for lower $p_{exc}$ or inter-cycle updates" would protect the paper from astrodynamics critiques.
3.  **Strengthen the "Nominal" Case:** Since the "Stress Case" (46% overhead) is an upper bound, emphasize the "Nominal" case (5% overhead) more strongly in the Conclusion. This low overhead is the primary selling point of the hierarchical architecture—it stays out of the way when not needed.
4.  **Visualizing the Envelope:** In Figure 8 (Workload Comparison), consider shading the region between the "Stress" and "Nominal" curves to visually represent the "Operational Design Envelope." This makes the concept immediately intuitive.