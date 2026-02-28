---
paper: "02-swarm-coordination-scaling"
version: "bz"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-28"
recommendation: "Accept"
---

**Review of IEEE Transactions on Aerospace and Electronic Systems Manuscript (Version BZ)**

**Title:** Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms

---

### 1. Significance & Novelty
**Rating: 5**

This manuscript addresses a critical and timely gap in the literature: the scalability of autonomous coordination for "mega-constellations" ($10^3$--$10^5$ nodes). While existing literature covers swarm robotics (small scale) and constellation routing (networking focus), there is a paucity of work that provides rigorous sizing equations for the *command and control* layer of such large systems.

The novelty lies in the derivation of closed-form "design equations" that account for physical-layer constraints (turnaround times, framing overhead, correlated shadowing) while remaining abstract enough for architectural sizing. The distinction between "byte budget feasibility" and "TDMA airtime feasibility" is a significant contribution that prevents the common error of assuming raw bandwidth equals throughput in half-duplex space systems.

### 2. Methodological Soundness
**Rating: 5**

The methodology is exceptionally rigorous. The authors employ a "verification taxonomy" that is rarely seen in systems engineering papers but is highly effective here. By using a fast cycle-aggregated Discrete Event Simulation (DES) for fleet-wide statistics and validating it against independent slot-level and packet-level simulators, the authors balance computational feasibility with physical fidelity.

The use of the Gilbert-Elliott (GE) model for correlated channel losses, grounded in Lutz et al. and ITU-R P.681, is appropriate for the LEO environment. The derivation of the MAC efficiency parameter ($\gamma$) from CCSDS Proximity-1 framing standards (Section IV-J) rather than relying on arbitrary assumptions strengthens the results significantly.

### 3. Validity & Logic
**Rating: 4**

The conclusions are well-supported by the data. The finding that intra-cycle ARQ is infeasible under slow-mixing shadowing (structural blockage) is logically sound and mathematically validated. The link budget justification for the 1 kbps RF-backup mode is grounded in physics.

One minor limitation regarding validity is the assumption of static cluster membership. While the authors argue that re-association overhead is negligible ($<0.5\%$), this assumes a specific orbital configuration (likely Walker-Delta). In highly non-coplanar configurations or during deployment phases, topology churn might be higher. However, for the purpose of *bandwidth sizing* (the paper's primary goal), this abstraction is acceptable, provided the limitations are clearly scoped.

### 4. Clarity & Structure
**Rating: 4**

The paper is dense but logically organized. The progression from analytical equations to simulation results to packet-level validation is effective. Tables are used effectively to summarize complex data (particularly Table V and Table XIV).

However, the density of the paper can be overwhelming. The distinction between the three simulation tools (Cycle-aggregated DES, Slot-level Sim, Packet-level Sim) is crucial but requires careful reading to track. A graphical representation of how these models feed into each other would improve clarity. Additionally, the definition of command types (Type 1 vs. Type 2) appears somewhat late in the text relative to its importance.

### 5. Ethical Compliance
**Rating: 5**

The authors include a specific acknowledgment regarding AI-assisted ideation (Claude, Gemini, etc.), which aligns with emerging transparency standards. No conflicts of interest are apparent. The research involves simulation of standard engineering systems and raises no human subject concerns.

### 6. Scope & Referencing
**Rating: 5**

The scope is perfectly aligned with *IEEE TAES*. It bridges the gap between astrodynamics (constellation design) and electronic systems (communications protocols). The references are comprehensive, covering foundational texts (Kleinrock, Wertz), current operational systems (Starlink, OneWeb), and relevant standards (CCSDS).

---

### Major Issues

*None.* The manuscript is technically sound and ready for publication subject to the minor revisions suggested below. The validation gap regarding NS-3 simulation for full MAC contention is acknowledged by the authors in Section V-A and is an acceptable limitation for a paper focused on sizing equations and TDMA feasibility.

### Minor Issues

1.  **Definition of Command Types:** In Section IV-A-3 ("Half-duplex TX/RX partitioning"), the terms "Type 1 (broadcast)" and "Type 2 (per-node unicast)" are introduced. These terms are critical for understanding the stress-case analysis in Table XI. It would be helpful to define these formally in Section III (Simulation Framework) or Table II (Simulation Parameters) so the reader understands the workload model before reaching the results section.
2.  **Clarification of $\gamma$ Usage:** The paper uses $\gamma=0.85$ for the bulk of the analysis but later derives $\gamma=0.76$ in Section IV-J. While the text explains this transition well, it might confuse a reader skimming the results. I suggest adding a footnote to Table I (Key Notation) explicitly stating that $\gamma=0.85$ is the baseline assumption, while Section IV-J derives the lower bound based on CCSDS framing.
3.  **Static Topology Justification:** In Section V-B (Limitations), the authors discuss orbital mechanics. The statement "Cross-plane encounters are infrequent" is true for operational Walker constellations but perhaps less true for "shells" of satellites at different inclinations. A brief qualifying sentence specifying that the static assumption holds primarily for "organized constellation shells" rather than "disorganized swarms" would add precision.
4.  **Equation 10 ($L_{cmd}$):** The variable $q$ (unicast fraction) is introduced in the text immediately preceding the equation. Please ensure $q$ is added to a nomenclature table or clearly defined as a dimensionless ratio $[0,1]$.

### Overall Recommendation

**Accept / Minor Revision**

This is a high-quality paper that offers a significant contribution to the systems engineering of mega-constellations. The derivation of closed-form sizing equations backed by multi-level simulation is rigorous and valuable for practitioners. The revisions requested are strictly for clarity and presentation.

### Constructive Suggestions

1.  **Add a "Model Hierarchy" Figure:** In Section III-A, consider adding a small flow diagram showing the relationship between the three models:
    *   *Input:* Analytical Equations $\to$
    *   *Fleet Dynamics:* Cycle-Aggregated DES (Output: $\eta$, AoI) $\to$
    *   *Feasibility Check:* Slot-Level Sim (Output: Timing margins, ARQ failure) $\to$
    *   *Physical Validation:* Packet-Level Sim (Output: Derived $\gamma$).
    This would help the reader navigate the "Verification Taxonomy."

2.  **Strengthen the "Practitioner's Guide":** Section V-C (Message-Layer Design Equations Summary) is excellent. I suggest highlighting this further, perhaps by boxing these equations or creating a "Summary of Design Rules" table. This will likely be the most cited/used part of the paper.

3.  **Expand on FEC Sensitivity:** In Section IV-J-3, the paper notes that Rate 1/2 LDPC makes 30 kbps infeasible. Given that Rate 1/2 is common for noisy links, it would be valuable to briefly state what PHY rate *would* be required if Rate 1/2 were necessary (e.g., "If link conditions require Rate 1/2 FEC, the coordinator PHY rate must increase to approx. X kbps"). This adds robustness to the sizing advice.