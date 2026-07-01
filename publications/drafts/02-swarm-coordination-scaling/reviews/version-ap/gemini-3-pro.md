---
paper: "02-swarm-coordination-scaling"
version: "ap"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-27"
recommendation: "Minor Revision"
---

**IEEE Transactions on Aerospace and Electronic Systems**
**Peer Review Report**

**Manuscript ID:** [Version AP]
**Title:** Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms
**Authors:** Project Dyson Research Team

---

### **1. Significance & Novelty**
**Rating: 5 (Excellent)**

This manuscript addresses a critical and timely gap in the literature: the coordination of "mega-constellations" (10,000+ nodes) under constrained bandwidth conditions. While significant literature exists on routing (networking layer) and formation flying (GNC layer), there is a paucity of work on the *coordination layer*—specifically regarding byte-level traffic accounting for autonomous operations.

The paper’s focus on the "RF-backup regime" (1 kbps/node) is particularly valuable. Most modern literature assumes high-bandwidth optical Inter-Satellite Links (ISLs) are always available; however, robust systems engineering requires viable fallback modes. By deriving closed-form design equations for this constrained regime, the authors provide a significant contribution to the resilience engineering of future space systems. The scaling analysis up to $10^5$ nodes distinguishes this work from standard swarm robotics papers.

### **2. Methodological Soundness**
**Rating: 4 (Good)**

The methodology is generally robust. The authors employ a cycle-aggregated Discrete Event Simulation (DES) which is an appropriate choice for simulating $10^5$ nodes; a packet-level simulation would be computationally intractable for year-long operational horizons.

*   **Strengths:** The separation of "offered" vs. "delivered" load is rigorous. The use of Gilbert-Elliott (GE) models for link loss, rather than simple Bernoulli trials, adds necessary realism for space channels. The analytical cross-checks (e.g., comparing simulation results to Pollaczek–Khinchine and geometric tail distributions) build high confidence in the simulation engine.
*   **Weaknesses:** The abstraction of the MAC layer via the efficiency factor $\gamma$ is the primary methodological risk. While the authors acknowledge this (Section V-B), the assumption that $\gamma \in [0.7, 0.9]$ implies a highly efficient TDMA scheme. In a "backup" scenario where the system might be recovering from faults, maintaining the tight time synchronization required for high-$\gamma$ TDMA is non-trivial. The paper would benefit from a sensitivity analysis where $\gamma$ drops to Slotted ALOHA levels ($\approx 0.36$) to bound the worst-case synchronization loss.

### **3. Validity & Logic**
**Rating: 4 (Good)**

The conclusions are logically derived from the data. The distinction between the "stress-case" (command-heavy) and "nominal" (exception-based) workloads is crucial, and the authors rightly identify that workload assumptions drive overhead more than topology does.

There is, however, a potential logical inconsistency regarding the "Handoff" mechanism (Section III-B-2). The paper states that handoffs use "dedicated optical ISL at 1–10 Gbps" and are thus excluded from the RF overhead budget. However, the premise of the paper is designing for the **RF-backup regime** (Section I-C), which implies optical links might be unavailable. If the system is in RF-backup mode because optical links have failed, how can the coordinator perform a 10–50 MB state transfer? If the coordinator cannot hand off during an optical outage, the system availability calculations in Table X might be optimistic.

### **4. Clarity & Structure**
**Rating: 5 (Excellent)**

The manuscript is exceptionally well-written. The structure is logical, moving from problem definition to model description, results, and design equations.
*   **Figures/Tables:** The tables are dense but highly informative. Table I (Scalability Sensitivity) and Table VII (Traffic Accounting) are particularly useful for the reader.
*   **Practitioner Focus:** The inclusion of "Design Equations Summary" in Section V is a fantastic feature for engineering practitioners.
*   **Abstract:** The abstract is quantitative and accurately reflects the paper's contributions.

### **5. Ethical Compliance**
**Rating: 5 (Excellent)**

The authors provide a specific disclosure regarding AI-assisted ideation (Section VI), which complies with emerging publication standards. No conflicts of interest are apparent. The research involves simulation of theoretical systems and poses no human-subject risks.

### **6. Scope & Referencing**
**Rating: 5 (Excellent)**

The paper fits squarely within the scope of TAES, bridging space systems engineering, communications, and autonomous control. The referencing is comprehensive, covering classical queueing theory (Kleinrock), distributed consensus (Lamport, Ongaro), and modern constellation operations (Starlink, Kuiper).

---

### **Major Issues**

1.  **The Handoff Paradox in RF-Backup Mode:**
    As noted in the Validity section, there is a conflict between the operational premise (RF-backup mode when optical is down) and the coordinator handoff mechanism (relies on optical ISLs).
    *   *Critique:* If the fleet is operating in the 1 kbps RF mode because of a systemic optical failure (e.g., pointing loss, software error), the 10–50 MB state transfer becomes impossible ($>100$ hours at 1 kbps).
    *   *Requirement:* The authors must clarify if the "RF backup" mode assumes optical ISLs are *intermittently* available or *permanently* down. If they are down, the paper must explain how coordinator rotation occurs, or acknowledge that coordinator rotation is suspended during RF-backup operations (which impacts the power/thermal arguments).

2.  **MAC Layer Synchronization Assumptions:**
    The results rely on $\gamma \approx 0.85$ (TDMA). This assumes that despite being in a backup mode, the swarm maintains precise time synchronization.
    *   *Critique:* In many failure scenarios requiring RF backup, GNSS or network time synchronization might be degraded. If the system falls back to CSMA or Slotted ALOHA, the effective capacity drops significantly.
    *   *Requirement:* Please add a brief discussion or a sensitivity plot line showing the system viability if $\gamma$ drops to 0.36 (Slotted ALOHA). Does the "Stress Case" still fit within the budget at $\gamma = 0.36$? (Looking at Fig. 11b, it appears it might not). This boundary condition should be explicitly stated.

---

### **Minor Issues**

1.  **Section IV-D (Joint Interaction):** The claim that GE losses and coordinator drops are independent is valid for the modeled point-to-point links. However, please clarify in the text that this independence *breaks down* if the RF backup is a shared medium (e.g., a shared omni-directional frequency) where retransmissions would increase the noise floor or collision rate for other nodes.
2.  **Table VIII (Latency):** The "Within-cycle batch queueing" is listed as 250 ms. Please clarify if this is the mean waiting time for a $D/D/1$ queue. With $k_c=100$ and service time 5ms, the first packet waits 0ms, the last waits 500ms. Average is 250ms. The math is correct, but the label "batch queueing" could be more precise (e.g., "Mean batch service wait").
3.  **Anonymization:** The author block lists "Project Dyson Research Team" and a URL. While this hides individual names, the URL links to a specific project which might reveal the authors' identities. Ensure this complies with the specific double-blind requirements of the target issue/editor.
4.  **Eq. 10:** Check the ceiling function notation. It appears correct, but ensure the log base matches the derivation (natural log vs base 10).
5.  **Fig. 5 (AoI):** Consider using a log scale for the Y-axis in Fig 5a. The geometric growth makes the lower $p_{exc}$ values hard to distinguish on a linear scale.

---

### **Overall Recommendation**
**Minor Revision**

The manuscript is a high-quality contribution that offers valuable design tools for large-scale space systems. The analytical rigor and simulation validation are strong. The "Major Issues" identified above regarding the logical consistency of the handoff mechanism and MAC efficiency in backup modes are critical for robustness, but likely require textual clarification and minor analytical bounding rather than a full re-simulation.

---

### **Constructive Suggestions**

1.  **Add a "Degraded Synchronization" Case:** In Section IV-F or the Discussion, explicitly calculate the maximum supportable command rate if $\gamma = 0.36$. This establishes the "safe mode" floor.
2.  **Clarify Handoff Strategy:** Explicitly state that during RF-backup operations, coordinator rotation is either (a) suspended (forcing the current coordinator to remain active, impacting power), or (b) performed via a minimal state transfer (e.g., just the random seed and index, not the full 50MB covariance matrix). Option (b) would strengthen the paper significantly.
3.  **Expand the "Practitioner's Guide":** In the Conclusion or Discussion, consider adding a small lookup table for "Recommended Coordinator Capacity" based on cluster size $k_c$. E.g., "For $k_c=50$, provision 12 kbps; for $k_c=100$, provision 25 kbps." This makes the results instantly usable for systems engineers.
4.  **Future Work - Orbital Dynamics:** Briefly mention that while AoI is 440s, the *utility* of that information depends on the orbital regime (LEO vs. GEO). 440s is an eternity in VLEO (Very Low Earth Orbit) drag regimes, but acceptable in GEO. A sentence qualifying this would add astrodynamics context.