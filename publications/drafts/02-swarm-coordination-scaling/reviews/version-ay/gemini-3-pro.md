---
paper: "02-swarm-coordination-scaling"
version: "ay"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-27"
recommendation: "Minor Revision"
---

**Review of Manuscript ID: [Version AY]**
**Title:** Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms
**Target Journal:** IEEE Transactions on Aerospace and Electronic Systems

---

### 1. Significance & Novelty
**Rating: 5 (Excellent)**

This manuscript addresses a critical and timely gap in the literature: the scalability of the "control plane" for mega-constellations and large-scale autonomous swarms. While existing literature extensively covers routing (data plane) and small-scale swarm robotics ($N < 100$), there is a paucity of rigorous analysis regarding the coordination overhead for fleets in the $10^3–10^5$ node regime.

The derivation of closed-form design equations for hierarchical coordination, specifically under the constraint of a low-bandwidth RF backup channel (1 kbps), is a significant contribution. The paper moves beyond qualitative architecture comparisons to provide quantitative sizing rules (e.g., coordinator ingress capacity, GE recovery cycles). The concept of "pipeline decoupling" under TDMA/orthogonal links is a valuable theoretical insight that simplifies the design of retransmission schemes. This work will likely serve as a reference for systems engineers sizing TT&C subsystems for future constellations.

### 2. Methodological Soundness
**Rating: 4 (Good)**

The methodology combines standard queueing theory ($M/D/c$, $D[k]/D/1$) with a custom cycle-aggregated Discrete Event Simulation (DES). The authors are commendably transparent about the role of the DES: it is used to *verify* the closed-form equations and explore tail statistics (like inter-cycle recovery) that are difficult to model analytically, rather than to *validate* against physical hardware.

However, there is one methodological simplification that requires stronger justification: the assumption of **static cluster membership** for the one-year duration. In a real LEO mega-constellation (e.g., Walker-Delta), planes precess, and relative positions shift, necessitating cluster handovers. While the authors address this analytically in the Discussion (Section V-C), claiming $<0.5\%$ overhead, the simulation itself does not model the topology churn. For a paper claiming to model "large autonomous space swarms," the lack of dynamic graph maintenance in the DES is a limitation, though likely not fatal to the core conclusions regarding bandwidth sizing.

### 3. Validity & Logic
**Rating: 5 (Excellent)**

The logical progression from research questions to analytical derivation and simulation verification is tight. The distinction made in Section IV-A between "queue saturation" (byte limits) and "frame-time feasibility" (slot limits) is sophisticated and demonstrates a deep understanding of Time Division Multiple Access (TDMA) constraints.

The Gilbert-Elliott (GE) loss analysis is robust. The authors correctly identify that intra-cycle retransmissions are futile during correlated bad-state bursts (coherence time $\geq T_c$) and rightly focus on inter-cycle recovery. The sensitivity sweep provided in Fig. 6b is highly practical for designers. The comparison against baselines is fair; the authors explicitly state that the centralized $c=1$ model is a theoretical bound and acknowledge that spectrum, not CPU, is the real bottleneck for centralized systems.

### 4. Clarity & Structure
**Rating: 4 (Good)**

The paper is dense but well-organized. The abstract is quantitative and impactful. The distinction between "offered" and "delivered" overhead is maintained consistently.

There are minor clarity issues regarding the "Sectorized Mesh" model. The description of the "capped-fanout" mechanism (Section III-B-4) implies that nodes only gossip with a subset of their sector. It is not immediately clear if a cap of 10 neighbors guarantees connectivity within a sector of $k_s \approx 317$ nodes. If the graph becomes partitioned due to the cap, the overhead comparison might be unfair (i.e., the mesh achieves lower overhead by failing to deliver global state). A brief note on the graph connectivity of the capped mesh would improve clarity.

### 5. Ethical Compliance
**Rating: 5 (Excellent)**

The authors include a specific acknowledgment regarding AI-assisted ideation (Section VII), which aligns with emerging transparency standards. No conflicts of interest are apparent. The research involves simulation of standard communication protocols and poses no human-subject risks.

### 6. Scope & Referencing
**Rating: 5 (Excellent)**

The paper fits squarely within the scope of IEEE TAES, bridging space systems engineering, communications, and autonomous control. The referencing is comprehensive, covering historical foundations (Kleinrock, Reynolds), current operational reality (Starlink, OneWeb), and relevant protocols (CCSDS, Raft, DTN). The inclusion of recent "HotNets" papers on mega-constellation routing shows the authors are up-to-date with the networking community's work in this domain.

---

### Major Issues

1.  **Sectorized Mesh Connectivity Verification:**
    In Section III-B-4, the "Capped-fanout sectorized mesh" limits heartbeats to $\min(k_s - 1, 10)$. For a sector size of $k_s \approx 317$ (at $N=10^5$), a degree cap of 10 is relatively sparse (approx 3%). The paper compares the overhead of this architecture against the hierarchical one, but it does not explicitly state whether this capped mesh achieves 100% intra-sector connectivity or message delivery. If the cap causes the sector graph to fragment, the mesh is not performing the equivalent function of the hierarchical cluster.
    *   *Requirement:* Please add a metric or statement regarding the *delivery ratio* or *graph connectivity* of the sectorized mesh under the capped regime to ensure the overhead comparison is "apples-to-apples."

2.  **Dynamic Topology Justification:**
    The assumption of static cluster membership (Section III-B-2) is a strong simplification for a 1-year simulation of orbiting bodies. While the analytical bound in the Discussion is helpful, the *Methods* section should explicitly justify why static topology is acceptable for the *Monte Carlo* analysis of overhead.
    *   *Requirement:* Move the justification for static topology from the Discussion to the Methods section (or reference it earlier). Explain why the transient overhead of re-clustering (which involves state transfer) does not invalidate the steady-state bandwidth conclusions.

### Minor Issues

1.  **Table II Footnote:** The footnote for Table II is excessively long and contains critical analysis ("vastly exceeding the 1 kbps budget"). This should be moved into the main text for better readability.
2.  **Figure 5b ($p_B$ value):** In Figure 5b, the caption or legend should explicitly state which $p_B$ value is used for the curves shown, or if it aggregates multiple $p_B$ values.
3.  **"RF-Backup" Terminology:** The paper uses the term "RF-backup" to define the 1 kbps constraint. However, the simulation seems to run this mode 100% of the time. It would be helpful to clarify if the "Nominal" workload profile assumes optical links are active, or if "Nominal" refers to the *traffic volume* (summaries only) while still using the RF link.
4.  **Equation 8 (TDMA Capacity):** The derivation uses $S_{eph} \times 8$. Please clarify if $S_{eph}$ includes the overhead headers mentioned in the text (preamble, CRC), or if those are accounted for solely in $\gamma$.
5.  **Section V-A (Validation Gap):** The list of physical layer effects is excellent. Item 4 (Doppler) mentions $\pm 40$ kHz at S-band. It might be worth noting that for low-rate (1 kbps) links, Doppler compensation is primarily a radio synchronization issue rather than a throughput reduction issue, provided the radio can track the shift.

### Overall Recommendation
**Minor Revision**

The manuscript is of high quality and offers significant contributions to the field of space systems engineering. The analytical rigor is strong, and the simulation framework is well-suited to the research questions. The requested revisions regarding the mesh connectivity verification and the placement of the topology justification are intended to strengthen the paper's argumentation and readability.

### Constructive Suggestions

1.  **Enhance the "Pipeline Decoupling" Discussion:** The insight that GE losses decouple from queue saturation under TDMA (Section IV-D) is a strong theoretical contribution. Consider highlighting this more in the Conclusion or Abstract. It implies that designers can size buffers based on traffic arrival rates and size link margins based on fade statistics *independently*, which simplifies the systems engineering process.
2.  **Design Curve Utility:** Figure 6b is a very useful tool for practitioners. Consider annotating it with a few "typical" operational scenarios (e.g., "Antenna Shadowing," "Tumpling Spacecraft") to help readers map physical phenomena to the $p_{BG}$ parameter.
3.  **Clarify "Command" vs. "Control":** The paper uses "Command" for 512B messages. In many constellations, "Control" implies closed-loop feedback. Explicitly stating whether these commands are open-loop directives (e.g., "execute schedule ID 5") or closed-loop setpoints would clarify the operational concept.