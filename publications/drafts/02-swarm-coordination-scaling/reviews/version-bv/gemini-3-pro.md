---
paper: "02-swarm-coordination-scaling"
version: "bv"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-27"
recommendation: "Minor Revision"
---

Here is a rigorous academic peer review of the manuscript "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version BV), prepared for *IEEE Transactions on Aerospace and Electronic Systems*.

---

### Review Criteria

**1. Significance & Novelty**
**Rating: 5 (Excellent)**

This paper addresses a critical and timely gap in the literature: the scalability of coordination architectures for "mega-constellations" ($10^3$--$10^5$ nodes). While existing literature covers swarm robotics (typically small scale) and traditional constellation management (centralized), there is a paucity of work rigorously defining the communication sizing requirements for autonomous fleets of this magnitude. The derivation of closed-form sizing equations—specifically distinguishing between topology-dependent overhead ($\eta_0$) and workload-dependent traffic ($\eta_{\text{cmd}}$)—is a valuable contribution that provides a "first-principles" design guide for future system architects.

The distinction between byte-level feasibility, MAC efficiency, and TDMA airtime schedulability (the "three feasibility layers") is particularly insightful. It moves beyond simple throughput calculations to address the specific constraints of half-duplex RF links in space environments. This work effectively bridges the gap between abstract distributed systems theory and practical spacecraft operations.

**2. Methodological Soundness**
**Rating: 4 (Good)**

The methodology combines analytical derivation with two distinct simulation layers: a cycle-aggregated Discrete Event Simulation (DES) for fleet-wide statistics and a slot-level TDMA simulator for superframe timing verification. This multi-fidelity approach is robust. The use of a Gilbert-Elliott (GE) model to capture correlated channel losses is appropriate for the LEO environment, where obstructions (structural or physical) create bursty errors.

However, a few methodological points require clarification. First, the specific implementation of the "fluid server" in the DES versus the "slot-level" constraints in the analytical model creates a potential disconnect. While the authors acknowledge this (Section IV-D), the paper would benefit from a more explicit discussion on how the fluid approximation might underestimate latency tails compared to rigid TDMA slotting. Second, the assumption of static cluster membership for the 1-year duration is a strong simplification. While the authors argue the re-association overhead is $<0.5\%$, this claim relies on an analytical bound rather than simulation data.

**3. Validity & Logic**
**Rating: 5 (Excellent)**

The conclusions are well-supported by the data. The authors are careful to bound their claims, explicitly stating that results are "message-layer predictions" and identifying unmodeled physical-layer constraints (antenna scheduling, interference) as future work. The cross-validation between the analytical equations and the DES results (agreement $<0.1\%$) builds high confidence in the derived scaling laws.

The logic regarding the "stress-case" command distribution is sound. The identification of the unicast command stagger (22 cycles) as a binding constraint is a crucial finding that highlights the limitations of RF backup links. The analysis of the Gilbert-Elliott recovery times (P95 in 4 cycles) provides actionable design data for buffer sizing.

**4. Clarity & Structure**
**Rating: 4 (Good)**

The paper is generally well-written and logically organized. The progression from problem statement to model definition, results, and discussion is clear. The notation table is helpful, and the distinction between the different overhead components ($\eta$, $\eta_0$, $\eta_{\text{total}}$) is maintained consistently.

There are minor clarity issues in the presentation of the TDMA superframe results. Table IV (Superframe Time Budget) is dense and could be better explained in the text. Specifically, the derivation of the "unallocated margin" needs to be explicitly tied back to the guard time assumptions. Additionally, the distinction between "Type 1" and "Type 2" commands in Section IV-A is critical but appears somewhat abruptly; defining these command types earlier in the "Workload Profiles" section would improve flow.

**5. Ethical Compliance**
**Rating: 5 (Excellent)**

The authors provide a clear acknowledgment of AI assistance in the ideation phase, citing a specific internal report/methodology. This transparency is commendable and aligns with emerging publication standards. There are no apparent conflicts of interest or ethical concerns regarding the research content. The open-source availability of the simulation code and data further supports ethical transparency and reproducibility.

**6. Scope & Referencing**
**Rating: 5 (Excellent)**

The paper fits squarely within the scope of *IEEE TAES*, addressing aerospace electronic systems (satellite communications) and system design. The references are comprehensive, covering historical foundations (Kleinrock, Lamport), swarm robotics (Dorigo, Brambilla), and current mega-constellation literature (Handley, Del Portillo). The inclusion of CCSDS standards (Proximity-1, Space Packet Protocol) grounds the work in realistic engineering constraints.

---

### Major Issues

1.  **TDMA/DES Disconnect on Latency Tails:**
    The paper uses a cycle-aggregated DES (fluid server) to validate byte counts but relies on a separate slot-level simulator for timing. While byte-count validation is successful, the fluid server model likely underestimates queueing latency tails compared to a rigid TDMA structure where a packet arriving *just after* its slot must wait a full frame ($T_c$). The paper reports "Within-cycle batch queueing" (Table VIII) based on a $D[k_c]/D/1$ model. The authors should clarify if the DES latency statistics account for the "wait-for-slot" delay inherent in TDMA, or if they only account for processing/serialization. If the latter, the latency results (Table V) may be optimistic.

2.  **Sectorized Mesh Fairness:**
    The comparison between the Hierarchical architecture and the Sectorized Mesh (Section III-B-4 and Table IX) feels slightly unbalanced. The authors cap the mesh neighbor monitoring at 10 peers to keep it within budget, then compare it to a hierarchy that monitors 100% of the cluster. While the "Functional Capability Matrix" (Table X) attempts to clarify this, the text in Section IV-F describes the mesh as having "higher overhead with narrower scope." It would be fairer to explicitly state that the Sectorized Mesh is *functionally incapable* of providing equivalent global/cluster state awareness under the 1 kbps constraint, rather than framing it purely as an efficiency comparison.

---

### Minor Issues

1.  **Section IV-A (TDMA Frame Model):** The derivation of $\gamma = 0.949$ is presented, but then $\gamma = 0.85$ is used "conservatively." While prudent, the specific breakdown of the remaining 10% (FEC, ranging, control) is somewhat hand-waved. A brief sentence citing typical overheads for CCSDS LDPC or similar coding would strengthen the justification for 0.85.
2.  **Eq. 10 (Unicast Stagger):** The variable $q$ is introduced as the "fraction of stress-case commands require per-node unicast." Please clarify if $q$ refers to the fraction of *nodes* receiving a unicast command, or the fraction of the *command volume* that is unicast.
3.  **Table VII (Joint Interaction):** The column header "GE + Exc. Drops" shows a massive reduction in drops. The text explains this is due to load reduction. It would be helpful to explicitly state the offered load (in MB or messages) for the "GE + Exc." case in the table caption or text to make the comparison with the "No Loss" case (which presumably has higher load) more direct.
4.  **Fig. 6 (Cross-cycle recovery):** The caption mentions "Markov-chain analytical model." Please ensure the specific equation used for the analytical curve is referenced or provided in the text near the figure callout.
5.  **Typos/Formatting:**
    *   Section III-B-2: "RequestVote: 100 B broadcast... 51 responders required" - clarify if this is 51 *responses* of size X, or just the logic.
    *   Table I: $S_{\text{eph}}$ is defined as 256 B. Ensure this is consistent with "Status report size" in Table II.

---

### Overall Recommendation

**Minor Revision**

This is a high-quality paper that makes a significant contribution to the field of autonomous spacecraft coordination. The analytical framework is novel, and the simulation validation is rigorous. The requested revisions are primarily clarifications regarding the latency modeling assumptions and a more nuanced framing of the topology comparison. Once these points are addressed, the paper will be an excellent addition to *IEEE TAES*.

---

### Constructive Suggestions

1.  **Enhance Latency Discussion:** Add a paragraph in Section IV-F explicitly contrasting the latency profile of the "fluid" DES model vs. the "rigid" TDMA model. Acknowledge that while throughput is validated, the DES likely represents a lower bound on latency variance.
2.  **Refine Mesh Comparison:** In the abstract and conclusion, sharpen the distinction between the hierarchy and the mesh. Instead of saying the mesh has "higher overhead," state that the mesh "cannot support equivalent state awareness within the 1 kbps budget," which is a stronger and more accurate conclusion.
3.  **Visualizing the Feasibility Layers:** Consider adding a small diagram or flowchart illustrating the "Three Feasibility Layers" (Byte Budget $\to$ MAC Efficiency $\to$ Airtime Scheduling). This would help readers visualize how a design passes the first two checks but fails the third (as in the unicast stress case).
4.  **Operational Context:** Briefly expand on the "1 kbps RF backup" scenario. Mentioning specific radio hardware (e.g., S-band patch antennas vs. high-gain dishes) or link budget assumptions (e.g., tumbling satellite gain margins) would ground the 1 kbps constraint in physical reality for the reader.