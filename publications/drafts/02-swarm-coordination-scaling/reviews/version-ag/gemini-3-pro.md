---
paper: "02-swarm-coordination-scaling"
version: "ag"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-27"
recommendation: "Accept"
---

Here is a comprehensive peer review of the manuscript "Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study" (Version AG), prepared for *IEEE Transactions on Aerospace and Electronic Systems*.

---

# Peer Review Report

**Manuscript Title:** Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study
**Target Journal:** IEEE Transactions on Aerospace and Electronic Systems

## 1. Significance & Novelty
**Rating: 5 (Excellent)**

This manuscript addresses a critical and timely gap in the aerospace engineering literature: the specific scaling behaviors of autonomous coordination architectures for "mega-constellations" ($10^4$--$10^5$ nodes). While existing literature covers small-scale swarms ($<100$ nodes) or centralized management of current constellations ($<5,000$ nodes), there is a paucity of rigorous quantitative analysis on the "middle ground" where physics-based propagation delays and bandwidth constraints break centralized models, yet full mesh networking is computationally prohibitive.

The novelty lies in the methodological approach: a cycle-aggregated Discrete Event Simulation (DES) that bridges the gap between abstract analytical queueing models and computationally expensive packet-level network simulators. The specific contributions regarding coordinator ingress sizing (21--50 kbps) and the interaction between Gilbert-Elliott (GE) losses and coordinator saturation provide actionable design guidance for next-generation constellation architects. The "dual-regime" interpretation of bandwidth—framing 1 kbps as a binding backup constraint rather than a nominal optical limit—is a sophisticated and valuable insight.

## 2. Methodological Soundness
**Rating: 4 (Good)**

The methodology is generally robust. The choice of a cycle-aggregated DES is appropriate for the scale ($10^5$ nodes) and allows for statistically significant Monte Carlo sweeps that would be impossible with packet-level fidelity. The validation against analytical bounds (Pollaczek–Khinchine for centralized, geometric distributions for AoI) builds high confidence in the simulation engine.

However, there is a slight disconnect in the physical layer abstraction. The paper acknowledges that MAC-layer effects are abstracted via an efficiency factor $\gamma \in [0.7, 0.9]$. While this is standard for high-level architectural studies, the assumption that TDMA scheduling is perfectly achievable over 500 km inter-satellite links without significant guard time penalties (beyond the 15% allotted) is optimistic, particularly given the dynamic topology of non-Keplerian swarms or differential drag. The "Physical-layer vignette" in Section IV-A helps, but the reliance on $\gamma$ as a linear scaling factor is a simplification that deserves more critical scrutiny in the discussion.

## 3. Validity & Logic
**Rating: 5 (Excellent)**

The logic of the paper is exceptionally tight. The authors rigorously cross-check simulation results against closed-form analytical expectations (e.g., Table VII). The distinction between "workload assumptions" and "architecture choice" as drivers of overhead is a crucial finding that corrects common misconceptions in distributed systems design.

The analysis of the "Joint Parameter Interaction" (Section IV-D) is particularly strong. By explicitly testing whether GE losses and coordinator saturation interact, the authors validate the use of compositional design equations. This is a subtle but methodologically vital contribution. The conclusions regarding the "Sectorized Mesh" as a realistic intermediate baseline are well-supported by the data, providing a fair comparison that avoids setting up a "straw man" argument against purely global meshes.

## 4. Clarity & Structure
**Rating: 5 (Excellent)**

The manuscript is written to a very high standard. The structure is logical, moving from architecture definitions to simulation mechanics, then to results and discussion. The use of "Roadmap" paragraphs at the start of the Results section is helpful.

Figures are well-referenced and appear (based on descriptions) to be integral to the argument. The "Design Equations Summary" in the Discussion is an excellent feature for practitioners. The definitions of metrics (Section III-H) are precise, particularly the distinction between "per-message delivery" and "per-cycle completion," which is vital for interpreting the GE loss results.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**

The authors provide a transparent "Acknowledgment" section detailing the use of AI tools for ideation (Claude, Gemini, GPT), which complies with emerging academic standards for AI transparency. The data availability statement is exemplary, providing links to code, scripts, and data. There are no apparent conflicts of interest or ethical concerns regarding the subject matter.

## 6. Scope & Referencing
**Rating: 4 (Good)**

The paper fits perfectly within the scope of *IEEE TAES*. The referencing is adequate, covering the necessary bases of swarm robotics, delay-tolerant networking (DTN), and constellation operations.

However, the references regarding "mega-constellation" routing could be strengthened. While Handley (2018) and Del Portillo (2019) are cited, more recent work on software-defined networking (SDN) in space or specific optical inter-satellite link (OISL) topology optimization (e.g., grid vs. motif) from 2020–2023 would strengthen the context for the "Cluster Coordinator" topology choice.

---

### Major Issues

1.  **MAC Layer Abstraction & Contention (Section IV-F):**
    The paper argues that the Sectorized Mesh disadvantage is understated because of hidden terminal effects, while the Hierarchical topology benefits from structural TDMA. This is a strong claim that relies heavily on the assumption that the Hierarchical cluster can maintain precise TDMA synchronization.
    *   *Critique:* In a dynamic swarm where relative positions change, maintaining TDMA slots requires significant overhead for guard times and synchronization beacons. The paper uses a fixed $\gamma \in [0.7, 0.9]$.
    *   *Requirement:* The authors should include a sensitivity analysis or a more detailed derivation of $\gamma$ specifically for the Hierarchical case. If the cluster diameter changes or nodes drift, does $\gamma$ degrade? A brief calculation of guard time requirements vs. clock drift/position uncertainty would solidify the claim that 24 kbps is achievable.

2.  **Coordinator Failure & Election Storms:**
    The paper models coordinator failure and election (Section IV-G) but treats election traffic as negligible ($<0.01\%$).
    *   *Critique:* This assumes elections happen in isolation. In a correlated failure event (e.g., a radiation event affecting a specific orbital sector), multiple coordinators might fail simultaneously. This could trigger a "broadcast storm" of election votes and topology reconfiguration messages that saturates the control plane exactly when it is most brittle.
    *   *Requirement:* The authors should briefly address (even if analytically) the impact of simultaneous coordinator failures. Does the 1 kbps budget hold up if 10% of clusters are electing simultaneously?

### Minor Issues

1.  **Table II (Mesh Traffic):** The footnote calculation for mesh traffic mentions "vastly exceeding the 1 kbps budget." It would be helpful to explicitly state the calculated bandwidth requirement in kbps or Mbps in the table body or caption for immediate visual comparison, rather than just "Exceeds."
2.  **Section IV-B (AoI):** The coupling of AoI to position error ($\sigma_{pos}$) is useful but linear. The text mentions "drag variability can produce nonlinear growth." It would be beneficial to explicitly state that this linear model is a *lower bound* on error, as cross-track errors due to $J_2$ perturbations are also relevant.
3.  **Section IV-A (TDMA Vignette):** The Doppler calculation (<1 Hz) assumes "co-orbital nodes... slightly different orbital elements." Please clarify if this holds for counter-rotating planes or crossing orbits, or if the cluster is strictly defined as a co-moving formation. If strictly co-moving, this limits the applicability to specific constellation geometries (e.g., trains) rather than shells.
4.  **Equation 11 (Chernoff Bound):** The notation $D_{KL}(\alpha p \| p)$ is standard in information theory but might be opaque to some TAES readers. A brief inline definition or reference for the KL divergence in this context would improve readability.
5.  **Typos/Formatting:**
    *   Section III-B-2: "The total message complexity per coordination cycle is $O(N)$..." is repeated in the paragraph immediately following.
    *   Table X: The column header "Handoff Cost" is qualitative (High/Low), while others are quantitative. Defining "Cost" (e.g., in MB or time) would be more consistent.

### Overall Recommendation
**Accept with Minor Revisions**

This is a high-quality paper that makes a significant contribution to the field of space systems engineering. The simulation framework is rigorous, the results are counter-intuitive yet well-explained (e.g., the independence of GE losses and coordinator saturation), and the design guidance is actionable. The revisions requested regarding the MAC layer abstraction and correlated election storms will strengthen the robustness of the conclusions but do not require a fundamental re-execution of the study.

### Constructive Suggestions

1.  **Strengthen the MAC Argument:** Add a small subsection or expanded paragraph in the Discussion explicitly deriving the guard time $\tau_g$ required for a 500 km cluster given standard GNSS timing errors and ephemeris uncertainty. This moves the $\gamma$ factor from a "heuristic" to a "derived constraint."
2.  **Visualizing the "Dual Regime":** Consider adding a small inset to Figure 10 or a new plot that shows the "Dual Regime" concept visually—perhaps a plot of Overhead vs. Link Capacity ($C_{node}$), showing the asymptote where overhead becomes negligible. This would powerfully communicate why the 1 kbps constraint is a design corner case.
3.  **Expand on Store-and-Forward:** The paper identifies that inter-cycle store-and-forward is needed for GE losses. A brief paragraph suggesting a specific buffer sizing strategy (e.g., "Coordinators require $B_{buf} = 5 \times k_c \times S_{report}$ to ride out 95% of GE bursts") would add immediate engineering value.
4.  **Clarify "Cluster" Geometry:** Explicitly define the orbital geometry of a "cluster." Is it a string of pearls? A swarm in a bounded relative motion box? The feasibility of the ISL links depends heavily on this geometry, and clarifying it will preempt questions about line-of-sight or range variations.