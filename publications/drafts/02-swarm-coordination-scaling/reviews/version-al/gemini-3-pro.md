---
paper: "02-swarm-coordination-scaling"
version: "al"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-27"
recommendation: "Minor Revision"
---

# Peer Review: IEEE Transactions on Aerospace and Electronic Systems

**Manuscript ID:** [Version AL]
**Title:** Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study
**Authors:** Project Dyson Research Team

## 1. Significance & Novelty
**Rating: 5 (Excellent)**

This manuscript addresses a critical and timely gap in the aerospace systems literature: the "middle ground" between small-scale swarm robotics ($N < 100$) and massive, ground-managed constellations ($N > 10,000$). The specific focus on the $10^3$ to $10^5$ node regime, under the constraint of an RF-backup/safe-mode bandwidth budget (1 kbps/node), is highly relevant to the engineering of future mega-constellations and orbital debris remediation swarms.

The novelty lies not in the invention of new protocols, but in the rigorous **parametric characterization** of hierarchical architectures under realistic byte-level constraints. While hierarchical control is a standard concept, quantifying the specific "design envelope" (e.g., the 21–50 kbps coordinator ingress requirement and the specific interaction between Gilbert-Elliott losses and store-and-forward recovery) provides actionable design data for systems engineers. The distinction between "workload assumptions" and "architecture choice" as the driver for overhead is a valuable insight that corrects common misconceptions in distributed systems design.

## 2. Methodological Soundness
**Rating: 4 (Good)**

The use of a **Cycle-Aggregated Discrete Event Simulation (DES)** is an appropriate choice for simulating $10^5$ nodes over year-long durations, where packet-level simulation (e.g., NS-3) would be computationally prohibitive. The authors are transparent about the limitations of this abstraction (Table III).

Strengths:
*   **Analytical Cross-checks:** The manuscript consistently validates simulation results against closed-form analytical models (e.g., $M/D/1$ queueing, geometric AoI distributions). This builds high confidence in the simulation logic.
*   **Traffic Accounting:** The byte-level accounting (Table VI) is meticulous. Excluding the optical ISL bulk transfers from the RF coordination budget is the correct engineering approach.
*   **Statistical Rigor:** The use of Monte Carlo sweeps with bootstrap confidence intervals is standard and well-executed.

Weaknesses:
*   **MAC Layer Abstraction:** The assumption of a MAC efficiency factor $\gamma \in [0.7, 0.9]$ is a significant simplification. In a mesh topology with $10^5$ nodes, achieving $\gamma=0.7$ implies a highly effective distributed scheduling algorithm or rigid TDMA, which carries its own overhead not modeled here. While the authors acknowledge this in Section IV-F, the impact of contention on the "Sectorized Mesh" comparator is likely underestimated.

## 3. Validity & Logic
**Rating: 4 (Good)**

The conclusions are generally well-supported by the data.
*   **Coordinator Sizing:** The derivation of the 21–50 kbps requirement is logically sound and backed by the burstiness analysis.
*   **Independence Finding:** The finding in Section IV-D (that GE retransmissions and coordinator saturation are independent) is valid *under the specific assumption* of point-to-point ISLs. The authors properly qualify this, but it is a fragile conclusion that breaks if the physical layer changes to a shared medium (e.g., intra-cluster RF bus).
*   **AoI Analysis:** The mapping of AoI to position uncertainty (Eq. 12) is explicitly labeled as an "order-of-magnitude input," which is an appropriate level of fidelity for this study.

## 4. Clarity & Structure
**Rating: 4 (Good)**

The paper is written in a dense, high-density engineering style.
*   **Pros:** Precise definitions of metrics (Section III-H). Excellent use of tables to summarize parameters and results.
*   **Cons:** The Abstract is overwhelming. It contains too many numerical values, making it difficult to extract the core narrative. Section IV (Results) is very long and covers disparate topics (Capacity, AoI, Loss, Workload); it might benefit from better sub-structuring or a roadmap paragraph.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**

The authors provide a clear acknowledgment of AI-assisted ideation in the Acknowledgments section, complying with modern ethical standards. No human subjects are involved. The research appears ethically sound.

## 6. Scope & Referencing
**Rating: 5 (Excellent)**

The paper fits squarely within the scope of *IEEE TAES*, specifically the areas of Space Systems and Networked Systems. The references are a healthy mix of foundational theory (Kleinrock, Lamport, Reynolds) and contemporary operational data (Starlink, Kuiper, AoI literature). The inclusion of CCSDS standards (BPv7, Proximity-1) grounds the work in reality.

---

## Major Issues

1.  **MAC Efficiency Justification (Section IV-F & V-B):**
    The paper relies on a scalar parameter $\gamma$ to account for MAC-layer overhead. For the Hierarchical topology, the argument for TDMA ($\gamma \approx 0.85$) is plausible due to the central coordinator. However, for the **Sectorized Mesh**, assuming the same $\gamma$ range is optimistic. Distributed scheduling among neighbors usually results in lower efficiency or higher overhead than centralized scheduling.
    *   *Requirement:* The authors should explicitly discuss or simulate the sensitivity of the Sectorized Mesh to lower $\gamma$ values (e.g., CSMA/CA levels $\approx 0.4-0.5$). If the Mesh collapses at $\gamma=0.4$ while Hierarchical survives, this is a critical differentiator that strengthens the paper's argument.

2.  **Abstract Density:**
    The current abstract is a "wall of numbers." While quantitative abstracts are good, this one lists so many specific values (21-50 kbps, 440s, 87.5% vs 27%, 4-7 cycles, 7-29 min/day) that the reader loses the thread of *why* these numbers matter.
    *   *Requirement:* Rewrite the abstract to focus on the *relationships* and *implications* of these numbers, selecting only the 2-3 most critical quantitative results to highlight.

3.  **Joint Independence Qualification (Section IV-D):**
    The finding that "GE retransmission traffic and coordinator capacity saturation compose independently" is presented as a key result. This result is entirely dependent on the architecture being **Point-to-Point (P2P) Optical ISLs**. If the cluster uses a shared RF bus (common in swarm concepts to save mass/pointing complexity), retransmissions *would* consume channel time and cause saturation.
    *   *Requirement:* This qualification must be prominent in the Abstract and Conclusion, not just the body text. It is a conditional truth, not a universal scaling law.

---

## Minor Issues

*   **Title/Authors:** "Project Dyson Research Team" is listed. Ensure this complies with IEEE's specific double-blind or single-blind review policies for the final submission.
*   **Section III-A:** The distinction between "cycle-aggregated DES" and "packet-level DES" is made, but the text should clarify if *serialization delay* is modeled for the large handoff messages. (It appears to be, based on Section III-B-2, but explicit confirmation in III-A would help).
*   **Eq. 11 (Chernoff Bound):** The equation is presented as a heuristic. Please clarify if the $D_{KL}$ term is calculated for a Bernoulli process approximation.
*   **Figure 5/6 References:** Ensure the text references to figures match the actual content, particularly regarding the "Sectorized Mesh" inclusion in Fig 5 (Workload).
*   **Typos/Grammar:**
    *   Section IV-G: "Pareto frontier" is standard, but check capitalization.
    *   Table VII: "Handoff Cost" column uses qualitative terms (High, Low). Defining these in the caption or text (e.g., "High = >10% duty cycle overhead") would be more precise.

---

## Overall Recommendation
**Minor Revision**

The manuscript represents a high-quality contribution to the field of space systems engineering. The methodology is robust within its stated scope, and the results provide valuable design guidance for future constellations. The revisions requested are primarily regarding the presentation (Abstract), the qualification of claims (MAC layer and Independence), and minor clarifications. No new simulation runs are required, but a sensitivity discussion regarding Mesh MAC efficiency is necessary.

---

## Constructive Suggestions

1.  **Add a "MAC Sensitivity" Plot:** In Section IV-F (Topology Comparison), consider adding a small subplot or expanding the discussion to show at what $\gamma$ value the Sectorized Mesh breaks down compared to the Hierarchical topology. This would quantitatively demonstrate the "Spectrum Independence" argument.
2.  **Refine the "Vignette" (Section IV-A):** The calculation for the 500km cluster TDMA is excellent. To make it robust, cite a specific transceiver class (e.g., "S-band patch antenna with 1 Mbps raw rate") to ground the "24 kbps" requirement in existing hardware capabilities.
3.  **Structure Section IV:** Section IV is currently very long. Consider adding sub-headers or a "Summary of Results" table at the beginning of the section to guide the reader through the different dimensions (Capacity, Quality, Reliability, Scaling).
4.  **Clarify "Handoff" vs. "Coordination" Channels:** You mention they use different links (Optical vs. RF backup). Explicitly state in the Introduction or System Model that the study assumes a **dual-band architecture**. This is a significant hardware assumption that drives the results.