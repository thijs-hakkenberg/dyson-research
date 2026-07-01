---
paper: "02-swarm-coordination-scaling"
version: "ba"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-27"
recommendation: "Accept"
---

Here is the peer review for the manuscript "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version BA), prepared for *IEEE Transactions on Aerospace and Electronic Systems*.

---

# Peer Review Report

**Manuscript ID:** [Version BA]
**Title:** Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms
**Target Journal:** IEEE Transactions on Aerospace and Electronic Systems

## Review Criteria

### 1. Significance & Novelty
**Rating: 5 (Excellent)**

This manuscript addresses a timely and critical gap in the literature: the scalability of coordination architectures for mega-constellations ($10^4$--$10^5$ nodes). While existing literature covers routing in mega-constellations (Handley, Bhattacherjee) or swarm behavior in small groups (Brambilla), there is a distinct lack of rigorous, byte-level traffic analysis for the command and control (C2) of autonomous fleets at this scale. The focus on the "RF-backup regime" (1 kbps budget) is particularly valuable for resilient operations design.

The derivation of closed-form design equations validated by Monte Carlo simulation provides a practical toolkit for system architects. The distinction between "offered" vs. "delivered" overhead and the specific analysis of Gilbert-Elliott (GE) correlated losses in a TDMA context are significant contributions. The paper moves beyond high-level architectural diagrams to provide concrete sizing parameters (e.g., coordinator ingress of 21–25 kbps), which is exactly the type of engineering data needed by the TAES community.

### 2. Methodological Soundness
**Rating: 4 (Good)**

The methodology combines analytical derivation (queueing theory, Markov chains) with a custom Cycle-Aggregated Discrete Event Simulation (DES). The approach is generally rigorous. The authors are careful to define their atomic units (message-layer events) and justify their abstractions. The cross-verification between the closed-form equations and the DES (matching within 0.1%) builds strong confidence in the arithmetic consistency of the model.

However, there is a slight tension regarding the physical layer validation. The authors acknowledge a "Validation Gap" (Section V-A) regarding MAC-layer contention and antenna pointing. While they derive $\gamma$ (MAC efficiency) analytically in Section IV-A, the reliance on a cycle-aggregated model rather than a packet-level simulator (like NS-3) means that second-order effects of contention under heavy load might be underestimated. The assumption of static cluster membership for a 1-year simulation of LEO constellations is a strong simplification, though the authors provide a reasonable analytical bound for the re-association overhead in Section V-C.

### 3. Validity & Logic
**Rating: 5 (Excellent)**

The conclusions are well-supported by the data presented. The paper exhibits a high degree of intellectual honesty, particularly in identifying the limitations of the centralized baseline (processing vs. spectrum constraints) and the sectorized mesh (connectivity vs. overhead). The logic regarding the "pipeline decoupling" of GE losses under dedicated links versus the coupling under TDMA slot constraints is sophisticated and physically sound.

The distinction between intra-cycle and inter-cycle recovery is a key logical strength. The demonstration that intra-cycle retries are structurally ineffective under the assumed GE parameters ($p_{BG}=0.50$, cycle coherence) is a crucial insight that prevents naive retransmission designs. The parametric sensitivity analysis (Fig. 13) effectively bounds the design space.

### 4. Clarity & Structure
**Rating: 4 (Good)**

The paper is dense but well-organized. The progression from research questions to model definitions, results, and discussion is logical. The use of "Design Equations" summaries in Section V-D is excellent for readability and utility.

There are, however, areas where the density hinders comprehension. The distinction between the various overhead metrics ($\eta$, $\eta_{delivered}$, $\eta_{total}$) is defined in Section III-E, but the reader must remain very vigilant to track which is being used in specific tables. Additionally, the explanation of the "Sectorized Mesh" connectivity (Section III-B-4) is somewhat complex; the distinction between "capped fanout" and "uncapped" could be tabulated more clearly to allow for easier comparison with the hierarchical model.

### 5. Ethical Compliance
**Rating: 5 (Excellent)**

The authors provide a specific acknowledgment regarding AI-assisted ideation (Claude, Gemini, GPT) in the Acknowledgments section, citing a specific internal methodology paper. This transparency is commendable and aligns with emerging best practices. There are no apparent conflicts of interest or ethical concerns regarding the research content.

### 6. Scope & Referencing
**Rating: 5 (Excellent)**

The scope is perfectly aligned with *IEEE TAES*, bridging the gap between orbital mechanics (constellation design), communications engineering, and systems autonomy. The references are comprehensive, covering historical foundations (O'Neill, Reynolds), standard texts (Wertz/SMAD, Kleinrock), and recent mega-constellation literature (Del Portillo, Handley). The inclusion of relevant CCSDS standards (Proximity-1, Space Packet Protocol) grounds the work in realistic space systems engineering.

---

## Major Issues

1.  **TDMA Guard Time & Propagation Delay Assumptions (Section IV-A):**
    In Section IV-A, the derivation of $\gamma$ assumes a guard time of 4.7 ms based on a 500 km cluster diameter. However, for a hierarchical cluster in LEO, the relative geometry can change rapidly. If the cluster definition is topological (nearest $k$ neighbors) rather than geographic, the line-of-sight distances could vary significantly, especially near orbital intersections.
    *   *Critique:* The paper should explicitly state if the 500 km diameter is a hard constraint enforced by the clustering algorithm or an average. If nodes drift beyond this, the guard times fail, and slots collide.
    *   *Requirement:* Clarify the geometric bounds of the clusters. If they are not bounded by 500 km, the $\gamma$ calculation needs a sensitivity margin for larger differential delays.

2.  **Static Topology vs. Cross-Plane Drift (Section III-B-2 & V-C):**
    The simulation assumes static membership for 1 year. The authors argue in Section V-C that re-association overhead is negligible ($<0.5\%$). However, this argument focuses on *bandwidth*. The more critical impact of dynamic topology in a hierarchical system is *state consistency* and *control loop stability*.
    *   *Critique:* When a node switches clusters, there is a period where it might not be covered by either coordinator's summary, or covered by both.
    *   *Requirement:* The paper needs to explicitly address the "handoff" logic. Does a node leave Cluster A before joining Cluster B (break-before-make), or the reverse? While a full simulation isn't required, a paragraph discussing the *control* implication (not just bandwidth) of this churn is necessary to support the claim that static simulation is a valid proxy.

---

## Minor Issues

1.  **Abstract Clarity:** The phrase "Age-of-Information P99 = 440 s under exception-based telemetry" in the abstract is slightly misleading without context. It sounds alarmingly high for a coordination system until one reads the paper and realizes this is a feature of the *exception* logic (no news is good news). Consider rephrasing to "Age-of-Information P99 = 440 s (nominal silence) under exception-based telemetry."
2.  **Figure 5 (TDMA Comparison):** The caption mentions "red crosses indicate drop conditions," but in black-and-white print, these may be hard to distinguish. Ensure markers are distinct by shape as well.
3.  **Table I (M/D/c Sensitivity):** The column header $N_{max}$ is derived from $N_{max} = c \cdot \mu_s / r$. It would be helpful to explicitly state the assumed $r$ in the caption (presumably 0.1 msg/s) to make the table standalone.
4.  **Equation 10 (AoI):** The ceiling function brackets are used, but the text description is slightly dense. Defining the terms clearly immediately after the equation would help.
5.  **Section IV-C (GE Model):** The text states "The assumption is conservative for recovery... Conversely, for burst length...". This is a crucial argument. It would be strengthened by citing a reference regarding typical LEO channel coherence times or fading durations (e.g., scintillation or structural blockage statistics) to ground the $T_c=10s$ assumption.

---

## Overall Recommendation

**Accept with Minor Revisions**

This is a high-quality paper that contributes significant, practical design equations for the next generation of space systems. The analytical rigor is high, and the simulation campaign is extensive. The limitations are well-acknowledged. The requested revisions focus on clarifying geometric assumptions regarding TDMA timing and strengthening the justification for the static topology assumption regarding control stability. These can be addressed without new simulations.

---

## Constructive Suggestions

1.  **Add a "Practitioner's Lookup Table":** Section V-D is excellent. Consider adding a small lookup table summarizing the recommended design values (Coordinator Bandwidth, Buffer Size, Frame Size) for a "Standard" LEO mission (e.g., $N=10,000$, 1 kbps link) to make the results instantly usable for systems engineers.
2.  **Expand on the "Validation Gap":** In Section V-A, explicitly mention that while the *logic* is validated, the *link budget* is not. A sentence warning readers that $\gamma$ does not account for low-SNR packet loss (only collision/overhead) would prevent misuse of the equations.
3.  **Visualizing the Hierarchy:** Figure 1 is a block diagram. A visualization of the orbital configuration (e.g., a snapshot of a Walker constellation showing the physical extent of a "cluster" and a "region") would help the reader visualize the 500 km diameter assumption used in the TDMA analysis.