---
paper: "02-swarm-coordination-scaling"
version: "as"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-27"
recommendation: "Minor Revision"
---

Here is a comprehensive peer review of the manuscript "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version AS), prepared for *IEEE Transactions on Aerospace and Electronic Systems*.

---

# Peer Review Report

**Manuscript Title:** Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms
**Target Journal:** IEEE Transactions on Aerospace and Electronic Systems

## Review Criteria

### 1. Significance & Novelty
**Rating: 5 (Excellent)**

This paper addresses a critical and timely gap in the literature: the specific traffic engineering and sizing requirements for coordinating "mega-constellations" and large-scale autonomous swarms ($10^3$--$10^5$ nodes). While existing literature covers routing (networking layer) or formation flying (control layer), there is a distinct lack of work on the "middleware" layer—specifically, the byte-level accounting of coordination protocols under strict bandwidth constraints.

The derivation of closed-form design equations validated by cycle-aggregated simulation is a significant contribution. The distinction between "nominal" and "stress-case" workloads, and the quantification of the "RF-backup" regime (1 kbps/node), provides highly practical value for system architects. The finding that hierarchical overhead scales constantly ($\eta \approx 46\%$) while centralized and mesh architectures diverge or saturate is intuitive but rigorously quantified here.

### 2. Methodological Soundness
**Rating: 4 (Good)**

The methodology is generally robust. The use of a cycle-aggregated Discrete Event Simulation (DES) is appropriate for the scale ($10^5$ nodes) where packet-level simulation would be computationally prohibitive. The authors are transparent about their abstractions (Table IV).

However, there is a tension regarding the Physical/MAC layer abstraction. The paper derives results based on a "message-layer" model and applies a correction factor $\gamma$ for MAC efficiency. While the authors acknowledge this in Section V-B, the assumption that the Gilbert-Elliott (GE) loss model and Coordinator Ingress capacity are independent (Section IV-D) is heavily dependent on the "point-to-point ISL" assumption. If the RF backup link is shared-medium (e.g., omnidirectional S-band within a cluster), this independence collapses. The paper acknowledges this, but the strength of the "design equation" claim is slightly weakened by this topological constraint.

### 3. Validity & Logic
**Rating: 5 (Excellent)**

The logic is tight and well-structured. The authors do an excellent job of cross-validating simulation results against analytical models (e.g., the Pollaczek–Khinchine formula for centralized latency, Markov chains for GE recovery). The breakdown of overhead into specific message classes (Fig. 10) and the sensitivity analysis (Fig. 12) provide strong evidence for the conclusions.

The argument regarding the "Sectorized Mesh" as an intermediate comparator is well-reasoned. The distinction between "offered" vs. "delivered" load is handled correctly. The conclusion that hierarchical architectures are preferred not for latency, but for fault tolerance and spectrum independence, is a nuanced and mature takeaway that avoids overclaiming.

### 4. Clarity & Structure
**Rating: 4 (Good)**

The paper is written with high technical density but remains readable. The structure is logical: Introduction $\rightarrow$ Simulation Framework $\rightarrow$ Results $\rightarrow$ Discussion.

*   **Strengths:** The use of tables to summarize parameters (Table V) and traffic accounting (Table VII) is excellent. The "Design Equations Summary" in Section V-C is a fantastic resource for practitioners.
*   **Weaknesses:** The notation can be slightly overwhelming. There are many variables ($k_c, k_r, k_s, \mu_c, \mu_s, \eta, \gamma$). A nomenclature table would be helpful. Additionally, the distinction between Model A and Model B for coordinator ingress (Section IV-A) is buried in the text; it would benefit from a clearer visual or tabular comparison earlier in the section.

### 5. Ethical Compliance
**Rating: 5 (Excellent)**

The authors provide a specific "Acknowledgment" section detailing the use of AI tools (Claude, Gemini, GPT) for ideation, citing a specific internal report. This aligns with emerging transparency standards. No human subject data is involved. The open-source availability of the code (Section VI) enhances reproducibility and ethical transparency.

### 6. Scope & Referencing
**Rating: 5 (Excellent)**

The paper fits perfectly within the scope of *IEEE TAES*, bridging space systems engineering, communications, and autonomous control. The references are comprehensive, covering historical foundations (O'Neill, Reynolds), standard texts (Wertz/SMAD), and recent mega-constellation literature (Handley, Del Portillo). The inclusion of recent swarm robotics literature (Dorigo) alongside constellation management ensures a balanced view.

---

## Major Issues

1.  **MAC Layer Contention Coupling (Section IV-D):**
    The paper claims "Joint Independence" between GE losses and coordinator capacity. This is valid *only* for the specific topology modeled (dedicated links). However, the "RF-backup" scenario often implies low-gain, omnidirectional antennas which are inherently shared-medium. If $100$ nodes in a cluster try to retransmit simultaneously after a bad-state burst, the noise floor rises, and collision rates spike, potentially causing a congestion collapse that the current model (which separates loss from ingress) misses.
    *   *Requirement:* The authors must explicitly qualify the "Joint Independence" claim in the Abstract and Conclusion as applying strictly to non-contention-based physical layers (e.g., FDMA/CDMA or directional links), or acknowledge that it represents a best-case lower bound for shared-medium RF.

2.  **Coordinator Handoff Mechanics (Section III-B-2):**
    The paper mentions a 10–50 MB state transfer over optical ISL. However, the "RF-backup" regime assumes optical ISLs are unavailable. The text briefly mentions a "minimal seed handoff" of ~2 kB for this case.
    *   *Requirement:* This is a critical operational edge case. If the system is in RF-backup mode *because* optical links failed, how does the coordinator rotate? If it cannot rotate the full state, does the cluster degrade to a stateless mode? The paper needs to clarify the operational concept for coordinator rotation specifically during the RF-only contingency.

---

## Minor Issues

1.  **Abstract:** The phrase "validated with an open-source cycle-aggregated simulation" appears, but the link is in Section VI. It might be helpful to mention the tool name or specific methodology (DES) more prominently.
2.  **Section III-B-2 (Hierarchy):** The text states "static cluster membership... corresponds to intra-plane formations." It should briefly acknowledge that for cross-plane communication (e.g., a grid topology), the static assumption breaks down.
3.  **Eq. 10 (TDMA Capacity):** The equation uses $S_{\text{eph}}$. Please ensure $S_{\text{eph}}$ is defined clearly in the text near the equation (it appears to be the status report size, 256 B).
4.  **Figure 5 (TDMA):** The caption mentions "red crosses indicate drop conditions," but in black-and-white print, this may be hard to distinguish. Ensure markers are distinct by shape.
5.  **Typos/Formatting:**
    *   Table III: "10,000,000" in the last row causes column alignment visual tension.
    *   Section IV-E: "Fig. 10 decomposes $\eta$..." Check figure numbering; the text references Fig. 10, but the flow suggests it might be Fig. 8 or 9 based on standard LaTeX float behavior.
6.  **Nomenclature:** A dedicated nomenclature table is recommended due to the high density of variables ($N, k_c, \eta, \gamma, \rho, \mu$).

---

## Overall Recommendation

**Minor Revision**

This is a high-quality paper that offers significant practical value to the aerospace community. The analytical derivations are sound, and the simulation campaign is extensive. The "Major Issues" identified above regarding MAC layer coupling and RF-only handoff are matters of clarification and scoping rather than fundamental flaws in the data. With these clarifications, the paper will be an excellent addition to *IEEE TAES*.

---

## Constructive Suggestions

1.  **Add a "Practitioner's Guide" Box or Subsection:** The "Design Equations Summary" (Section V-C) is excellent. Consider formatting this as a distinct text box or a highlighted table in the final layout to serve as a quick-reference guide for system engineers.
2.  **Clarify the "RF-Backup" Scenario:** Explicitly state in the Introduction that the primary design driver is the *loss of optical ISLs*. This frames the 1 kbps constraint not just as "low bandwidth" but as a "survival mode," which justifies the tolerance for high overhead percentages (46%).
3.  **Expand on "Seed Handoff":** In Section III-B-2, elaborate slightly on the "minimal seed handoff." If the coordinator fails during an RF-only period, does the new coordinator have to rebuild the 50 MB state from scratch by polling all members? This would be a valuable insight into recovery latency.
4.  **Visualizing the Envelope:** Figure 12 (Sensitivity) is good, but a "Safe Operating Area" plot—showing $N$ vs. $C_{\text{node}}$ with shaded regions for "Viable" and "Saturated" based on the derived equations—would be a powerful visual conclusion.