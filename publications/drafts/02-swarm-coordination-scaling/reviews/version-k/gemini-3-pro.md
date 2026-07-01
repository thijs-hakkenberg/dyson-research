---
paper: "02-swarm-coordination-scaling"
version: "k"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-24"
recommendation: "Accept"
---

Here is the peer review for the manuscript "Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study" (Version K).

***

# Peer Review Report
**Journal:** IEEE Transactions on Aerospace and Electronic Systems
**Manuscript ID:** [Assigned by Editor]
**Title:** Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study
**Date:** October 26, 2023

## Review Criteria

### 1. Significance & Novelty
**Rating: 5 (Excellent)**

This manuscript addresses a critical and rapidly emerging gap in aerospace systems engineering: the coordination of "mega-constellations" and future autonomous swarms in the $10^4$ to $10^6$ node regime. While existing literature covers small swarms ($<100$ nodes) and current constellation management ($<10^4$ nodes), the intermediate and high-scale regimes are under-explored. The paper's specific focus on quantifying the "constant overhead factor" of hierarchical architectures via full-fidelity Discrete Event Simulation (DES) is a significant contribution.

The novelty lies in the rigorous quantitative comparison of hierarchical scaling against two distinct reference bounds (centralized ground processing and global-state mesh) using a consistent simulation framework. The identification of specific engineering constraints—such as the 59 kbps zero-drop link requirement and the validation of exception-based telemetry—provides actionable design guidelines for next-generation system architects. This work moves beyond abstract algorithmic complexity ($O(N)$ vs $O(N^2)$) to concrete byte-level traffic analysis, which is highly relevant to the *IEEE TAES* audience.

### 2. Methodological Soundness
**Rating: 5 (Excellent)**

The methodology is robust and rigorously described. The authors employ a Discrete Event Simulation (DES) with full-fidelity node participation (no sampling), which is computationally impressive for $N=10^5$. The use of 30 Monte Carlo replications per configuration ensures statistical significance, and the reporting of confidence intervals and standard deviations adds credibility.

The paper excels in its definitions. Section III.F and III.G (Traffic Accounting) are particularly strong, explicitly listing which message types are included in the overhead metric. This level of transparency is often missing in simulation studies and allows for reproducibility. The queueing theoretic baselines ($M/D/1$ and $M/D/c$) are correctly applied as theoretical bounds. The sensitivity analyses—specifically the link availability sweep with retransmission (Section IV.F) and the coordinator bandwidth stress test (Section IV.G)—address potential criticisms regarding idealized assumptions effectively.

### 3. Validity & Logic
**Rating: 4 (Good)**

The conclusions are generally well-supported by the data. The central claim—that hierarchical coordination maintains constant overhead ($\approx 20.66\%$) across scales—is logically sound and empirically validated by the simulation results. The analysis of coordinator duty cycles and the resulting power/availability trade-offs is logical and insightful.

However, there is a minor logical tension regarding the "Sectorized Mesh" discussion (Section V.C). The authors correctly identify that a global-state mesh is an intentional upper bound, but the comparison between the hierarchical model and a potential sectorized mesh remains qualitative. While the paper acknowledges this as future work, the argument that hierarchical is superior to sectorized mesh at large $N$ relies on analytical intuition rather than the simulation data presented. This does not invalidate the results but suggests a slight overreach in the comparative discussion. Additionally, the assumption that coordinator nodes can effectively pool bandwidth ($k_c \times 1$ kbps) is a strong one; while the stress test in IV.G mitigates this, the physical feasibility of such dynamic spectrum sharing in a dense cluster warrants slightly more caution in the text.

### 4. Clarity & Structure
**Rating: 5 (Excellent)**

The manuscript is exceptionally well-written. The structure is logical, following a standard Introduction $\to$ Related Work $\to$ Framework $\to$ Results $\to$ Discussion format. The distinction between "Baseline Telemetry" and "Protocol Overhead" is crucial and explained clearly.

The figures are effective, particularly Fig. 2 (Overhead vs. Nodes) and Fig. 6 (Scaling Trajectory), which clearly visualize the divergence of the baselines. The tables are dense with information but well-formatted; Table VII (Coordinator Bandwidth) is particularly useful for engineering practitioners. The abstract is concise and accurately reflects the paper's quantitative findings.

### 5. Ethical Compliance
**Rating: 5 (Excellent)**

The authors provide a specific "Acknowledgment" section detailing the use of AI tools (Claude, Gemini, GPT) for ideation, citing a companion methodology paper. This transparency regarding AI-assisted workflows sets a high standard for ethical disclosure. There are no apparent conflicts of interest or ethical concerns regarding the research content.

### 6. Scope & Referencing
**Rating: 4 (Good)**

The paper fits perfectly within the scope of *IEEE TAES*, bridging the gap between communication systems, orbital mechanics, and systems engineering. The references are comprehensive, covering historical foundations (O'Neill, Kleinrock), standard texts (Wertz/SMAD), and recent developments (Starlink, Kuiper, distributed consensus).

One minor gap is the lack of reference to specific Consultative Committee for Space Data Systems (CCSDS) standards regarding file transfer beyond BPv7. References to CCSDS File Delivery Protocol (CFDP) might be relevant for the discussion on large state transfers during handoff, as this is the standard protocol for such operations in space.

---

## Major Issues

*None.* The manuscript is technically sound, and the simulation campaign is rigorous. The limitations are clearly acknowledged in Section V.E.

## Minor Issues

1.  **Section III.B.1 (Centralized Scalability):** The paper states, "At a reporting rate of $r = 0.1$ messages per second per node, utilization reaches $\rho = 1.0$ at $N = 10{,}000$." While mathematically correct for a single thread, the text should perhaps emphasize earlier that this is a *processing* limit, not a *bandwidth* limit, to avoid confusion before the $M/D/c$ discussion. The current text does this, but the distinction could be sharper in the first paragraph of this section.
2.  **Section IV.G (MAC Efficiency):** The assumption of $\gamma \approx 0.85$ for TDMA efficiency in a dynamic swarm environment might be optimistic. In high-mobility LEO environments, guard times often need to be larger to account for Doppler shifts and clock drift. A brief sentence acknowledging that $\gamma$ could be lower (e.g., 0.6-0.7) in worst-case scenarios would strengthen the conservatism of the 59 kbps requirement.
3.  **Fig. 3 (Latency Distribution):** The caption notes that the $10^6$-node curve is an "analytical extrapolation." It would be beneficial to visually distinguish this curve (e.g., using a dotted line rather than a solid line) in the plot itself to prevent readers from mistaking it for DES data.
4.  **Equation 5 (Hierarchy Levels):** The text mentions "Levels: Ground $\to$ Regional $\to$ Cluster $\to$ Node," but the equation label is `eq:hierarchy` while the text immediately following refers to `eq:hierarchical_messages` (which is Eq. 5). Please check the LaTeX labeling to ensure the equation numbers align with the text references.
5.  **Typos/Grammar:**
    *   Section I.A: "conjunction events [3]" - ensure citation 3 is the most appropriate for "conjunction events" specifically (it appears to be ESA, which is correct).
    *   Section IV.F: "simple retransmission extends the robust operating regime... to $p_{\text{link}} \geq 0.5$." It might be clearer to say "link packet success rate" rather than just "link availability," as availability often implies uptime rather than PER (Packet Error Rate).

## Overall Recommendation
**Accept**

This is a high-quality manuscript that makes a distinct contribution to the literature on large-scale space systems. The simulation framework is rigorous, the results are quantified with appropriate statistical bounds, and the engineering implications are clearly derived. It requires no significant changes prior to publication.

## Constructive Suggestions

1.  **Visual Distinction for Extrapolation:** In Figure 3, change the line style for the $10^6$ node curve to dotted or dashed to visually reinforce that it is an analytical extrapolation, distinct from the solid DES-validated lines.
2.  **CFDP Reference:** In the discussion of coordinator handoff (transferring 10-50 MB), briefly mention CCSDS File Delivery Protocol (CFDP) as the likely transport mechanism, as it handles the file completeness and retransmission logic assumed in the handoff success rates.
3.  **Sectorized Mesh Clarification:** In Section V.C, explicitly state that while hierarchical aggregation offers compression benefits ($k_c \to 1$), sectorized mesh offers lower latency for neighbor-to-neighbor collision avoidance (0 hops vs 2 hops to coordinator). This adds nuance to the trade-off discussion.
4.  **Bandwidth Pooling Note:** In Section III.F, add a footnote or brief comment that "pooling" bandwidth ($k_c \times 1$ kbps) implies a Frequency Division Multiple Access (FDMA) or sophisticated Code Division Multiple Access (CDMA) scheme if done simultaneously, or simply a high-speed serial link in TDMA. Clarifying the physical layer assumption behind the "pooled" math would be helpful for comms engineers.