---
paper: "02-swarm-coordination-scaling"
version: "ad"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-27"
recommendation: "Accept"
---

Here is a rigorous peer review of the manuscript "Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study" (Version AD), prepared for *IEEE Transactions on Aerospace and Electronic Systems*.

---

# Peer Review Report

**Manuscript ID:** [Assigned by Editor]
**Title:** Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study
**Target Journal:** IEEE Transactions on Aerospace and Electronic Systems

## Review Summary

This paper presents a parametric design-space characterization of hierarchical coordination architectures for large-scale autonomous space swarms ($10^3$--$10^5$ nodes). Using a cycle-aggregated discrete event simulation (DES), the authors quantify protocol overhead, latency, and failure resilience, comparing a hierarchical approach against centralized and mesh baselines. The study offers specific engineering guidance on coordinator bandwidth sizing (21--50 kbps), Age-of-Information (AoI) trade-offs, and the impact of correlated link losses.

The work is technically sound, highly relevant to the emerging era of mega-constellations, and offers valuable quantitative insights that move beyond abstract algorithmic complexity. The distinction between message-layer overhead and physical-layer constraints is handled well. However, the paper would benefit from a clearer justification of the specific "stress-case" workload assumptions and a more explicit discussion of the operational implications of the high AoI values reported.

---

## Detailed Assessment

### 1. Significance & Novelty
**Rating: 5 (Excellent)**

The coordination of autonomous spacecraft at the $10^5$ scale is a critical, forward-looking problem that is currently under-addressed in the literature. Most existing work focuses either on small-scale swarm robotics ($<100$ agents) or centralized management of existing constellations ($<10^4$ nodes). This paper bridges that gap effectively.

The novelty lies not in the invention of a new hierarchy (hierarchical control is well-established), but in the *quantitative characterization* of its scaling properties under specific space-systems constraints (1 kbps/node budget, orbital dynamics, specific message sizes). The derivation of the "zero-drop" coordinator ingress capacity (21--50 kbps) and the quantification of the failure of intra-cycle retransmission under Gilbert-Elliott loss models are significant, practical contributions that will aid system architects.

### 2. Methodological Soundness
**Rating: 4 (Good)**

The methodology is generally robust. The use of cycle-aggregated DES is an appropriate choice for simulating $10^5$ nodes over year-long durations, where packet-level simulation would be computationally prohibitive. The authors are careful to validate their simulation against analytical closed-form solutions (Pollaczek–Khinchine, geometric distributions), which builds confidence in the results.

The "stress-case" workload assumption (one 512-byte command per node per cycle) is the primary driver of the high overhead ($\eta \approx 46\%$). While the authors acknowledge this is a bound, the justification for *why* a swarm would need 0.1 Hz global commanding is thin. In many autonomous architectures, high-frequency control is local, while global commands are sparse. The inclusion of "Nominal" and "Event-driven" profiles helps, but the heavy reliance on the stress case for headline metrics might overstate the bandwidth requirements.

The Gilbert-Elliott (GE) link model implementation is sound, and the insight regarding the failure of intra-cycle retransmission is mathematically valid. The statistical treatment (30 Monte Carlo runs, bootstrap confidence intervals) is standard and appropriate.

### 3. Validity & Logic
**Rating: 5 (Excellent)**

The conclusions follow logically from the data. The authors are disciplined in their interpretation, explicitly distinguishing between message-layer overhead and MAC-layer efficiency ($\gamma$). The "Baseline Interpretation Note" in the introduction is helpful in framing the centralized and global-mesh models as theoretical bounds rather than straw-man competitors.

The analysis of Age-of-Information (AoI) is particularly strong. The finding that exception-based telemetry ($p_{exc}=0.10$) saves bandwidth but results in a P99 AoI of $>7$ minutes is a crucial trade-off that is often overlooked in efficiency-focused studies. The authors correctly identify that this staleness has physical implications for orbit determination, even if they stop short of a full orbital dynamics propagator (which is outside the stated scope).

### 4. Clarity & Structure
**Rating: 4 (Good)**

The paper is well-written and dense with technical detail. The structure is logical, moving from architecture definitions to results and then discussion. Tables are used effectively to summarize parameters and results.

However, the density of the text can occasionally hinder readability. For instance, the distinction between "handoff state transfer" (optical ISL, not in $\eta$) and "coordinator election" (coordination channel, in $\eta$) is made in multiple places but could be consolidated. The "Baseline Interpretation Note" (Section I-C) feels out of place as a standalone subsection in the Introduction; it might fit better in the System Model section.

### 5. Ethical Compliance
**Rating: 5 (Excellent)**

The authors provide a specific "Acknowledgment" section detailing the use of AI tools (Claude, Gemini, GPT) for ideation, which aligns with emerging transparency standards. No human subjects are involved. The research appears ethically sound.

### 6. Scope & Referencing
**Rating: 5 (Excellent)**

The scope is perfectly aligned with *IEEE TAES*. The references are comprehensive, covering historical foundations (Reynolds, Lynch), space systems engineering (Wertz, CCSDS standards), and recent networking literature (AoI, mega-constellation routing). The connection to standard protocols (BPv7, CCSDS Proximity-1) grounds the theoretical work in engineering reality.

---

## Major Issues

1.  **Justification of the Stress-Case Workload:**
    The paper's headline overhead figure ($\eta \approx 46\%$) is driven by the "Stress-Case" workload, defined as one 512-byte command per node per cycle (0.1 Hz). This implies a continuous, fleet-wide downlink of commands. In autonomous systems, high-frequency control loops are typically closed locally or within the cluster, while ground-to-space commands are infrequent (schedule updates, coarse orbit maintenance).
    *   *Critique:* By centering the abstract and conclusion on the 46% figure, the paper may inadvertently suggest that hierarchical coordination is inherently bandwidth-heavy, when in fact it is the *workload assumption* that is heavy.
    *   *Requirement:* The authors should consider elevating the "Nominal" ($\eta \approx 5\%$) or "Event-Driven" ($\eta \approx 6\%$) profiles to equal prominence with the Stress-Case in the Abstract and Conclusion. The Stress-Case should be clearly framed as a "saturation test" or "worst-case provision" rather than a typical operating point.

2.  **MAC Layer Abstraction vs. Reality:**
    The paper applies a simple efficiency factor $1/\gamma$ to account for MAC overhead. While the authors acknowledge this abstraction (Table IV), the interaction between topology and MAC is non-trivial. Specifically, in the Sectorized Mesh model, the "hidden terminal" problem and contention in a shared wireless medium could degrade performance far more than a linear factor $\gamma$ suggests, especially at high utilization.
    *   *Critique:* The comparison between Hierarchical (which implies a structured, likely TDMA, flow to a coordinator) and Mesh (which implies contention-based or complex scheduled peer-to-peer links) might be unfair to the Hierarchy if the Mesh's MAC penalties are underestimated.
    *   *Requirement:* Add a brief qualitative discussion (perhaps in Section V) acknowledging that the $1/\gamma$ scaling likely underestimates the difficulty of implementing the Sectorized Mesh at high loads due to contention/scheduling complexity, further reinforcing the Hierarchical advantage.

---

## Minor Issues

1.  **Section I-C (Baseline Interpretation Note):** This subsection is very short and breaks the flow of the Introduction. Consider moving this text into Section III-B (Topology Models) where the baselines are defined.
2.  **Equation 10 (AoI Analytic):** The ceiling function is applied to the result of the log ratio. Please verify the notation. Usually, for discrete time steps, the formula is correct, but ensure the variables are clearly defined as integers where necessary.
3.  **Table VII (Coordinator Bandwidth):** The column $\beta$ is defined in the footnote. It would be helpful to explicitly state in the caption or text that $\beta$ represents the "oversubscription factor" or "pooling factor" to aid quick interpretation.
4.  **Figure 6 (AoI Quality):** The y-axis scale (linear vs log) significantly impacts the visual interpretation of the "long tail." Ensure the caption clarifies the scale used.
5.  **Terminology - "Handoff":** In Section III-B-2, handoff is described. In Section III-H, it is defined again. Ensure the distinction between the *control plane* aspect of handoff (election messages) and the *data plane* aspect (state transfer) is consistent throughout.
6.  **Reference 1 (Starlink):** Citing a "non-archival" website for critical operational data is weak, though understandable given the proprietary nature. If a regulatory filing (FCC) or a conference presentation by SpaceX engineers exists, it would be a stronger citation.

---

## Overall Recommendation

**Accept with Minor Revisions**

This paper represents a high-quality contribution to the field of space systems engineering. It addresses a scaling problem that is becoming increasingly relevant and provides concrete, quantitative design guidance. The simulation framework is well-validated, and the results are analyzed with rigor. The requested revisions regarding the workload justification and MAC layer discussion will strengthen the paper's archival value but do not require new experimentation.

---

## Constructive Suggestions

1.  **Reframe the Abstract:** Explicitly mention the "Nominal" overhead ($\sim 5\%$) alongside the "Stress-Case" ($\sim 46\%$) in the abstract. This provides a more balanced view of the architecture's efficiency during 99% of mission time.
2.  **Expand on "Sectorized Mesh" Implementation:** The Sectorized Mesh is a strong comparator. Briefly expanding on how "capped fanout" would be enforced in a real distributed system (e.g., "nodes select the $k$ nearest neighbors based on ephemeris") would add practical weight to that section.
3.  **Strengthen the Conclusion:** The conclusion currently summarizes the results well. To increase impact, add a sentence explicitly recommending the "Leaky Bucket" coordinator ingress model over the "Deadline" model for future hardware specifications, based on the 21 kbps vs 50 kbps finding.
4.  **Visualizing the Design Envelope:** Consider adding a "Design Recommendation" table or figure that maps Fleet Size ($N$) to recommended architecture and coordinator bandwidth, summarizing the study's output for a system architect.