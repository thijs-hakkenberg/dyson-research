---
paper: "02-swarm-coordination-scaling"
version: "p"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-24"
recommendation: "Minor Revision"
---

Here is a comprehensive peer review of the manuscript "Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study" (Version P), prepared for *IEEE Transactions on Aerospace and Electronic Systems*.

---

# Peer Review Report

**Manuscript Title:** Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study
**Target Journal:** IEEE Transactions on Aerospace and Electronic Systems

## Review Criteria

### 1. Significance & Novelty
**Rating: 5 (Excellent)**

This paper addresses a critical and rapidly emerging gap in the aerospace literature: the "intermediate regime" of constellation management between current scales ($10^3$ nodes) and future mega-constellations ($10^5$--$10^6$ nodes). While swarm robotics literature handles small scales and constellation management handles current scales, the specific engineering trade-offs of hierarchical coordination at $10^5$ nodes have not been rigorously quantified in this manner.

The novelty lies in the specific quantification of the "protocol coefficient" ($\eta \approx 20.66\%$) and the rigorous comparison against both a centralized baseline and a sectorized mesh topology. The introduction of the sectorized mesh as a realistic decentralized comparator (bridging the gap between the global-state mesh upper bound and the hierarchy) is a significant conceptual contribution. The findings regarding coordinator bandwidth requirements ($C_{\text{coord}} \geq 59$ kbps for zero-drop TDMA) provide actionable design constraints for next-generation inter-satellite link (ISL) hardware.

### 2. Methodological Soundness
**Rating: 4 (Good)**

The Discrete Event Simulation (DES) framework is robust and appropriate for the research questions. The authors are transparent about their abstraction level (message-passing layer), explicitly listing what is modeled vs. abstracted (Table III). The use of full-participation simulation (no sampling) for up to $10^5$ nodes adds significant weight to the results. The statistical approach—using 30 Monte Carlo replications and replacing confidence intervals with parametric sensitivity analysis due to the low variance—is statistically sound for a near-deterministic protocol model.

However, there is a minor methodological tension regarding the "Coordinator Link Capacity." The paper alternates between modeling coordinator bandwidth as a pooled resource ($k_c \times 1$ kbps) and a constrained ingress pipe ($C_{\text{coord}}$). While Section IV-G clarifies this with a stress test, the initial assumption in the hierarchy model description (Section III-B-2) could be clearer about the hardware implications earlier on. Additionally, the reliance on an exponential failure model is a standard simplification, but the discussion of correlated failures (e.g., solar particle events) is qualitative; a quantitative sensitivity check on correlated failures would strengthen the "robustness" claims.

### 3. Validity & Logic
**Rating: 4 (Good)**

The conclusions are generally well-supported by the data. The derivation of the $O(1)$ overhead scaling for the hierarchical topology is logically sound and empirically validated by the DES. The distinction between "delivered overhead" and "offered load" in the link availability analysis (Section IV-F) is a crucial and well-handled nuance.

One logical weak point is the comparison of the centralized baseline. The authors acknowledge that the single-server ($c=1$) model is an "intentional bound," but the divergence at $10^4$ nodes (Fig. 2) is purely an artifact of this parameter choice. While the authors defend this by pointing to physical constraints (propagation latency, spectrum), the visual representation of the centralized curve "blowing up" due to processing latency is slightly misleading if parallelization is trivial. The argument against centralized control is strong enough based on spectrum and latency without relying on a single-server bottleneck.

### 4. Clarity & Structure
**Rating: 5 (Excellent)**

The manuscript is exceptionally well-written. The structure is logical, following a standard progression from introduction to model description, results, and discussion. The definition of metrics (Section III-H) is precise, and the distinction between "baseline telemetry" and "protocol overhead" is maintained consistently.

Tables are highly effective, particularly Table I (Simulation Parameters) and Table III (Abstraction Scope), which greatly aid reproducibility. Figures are clear, though Figure 2 (Overhead Scaling) is dense. The use of specific line references to previous sections helps the reader navigate the complex parameter space.

### 5. Ethical Compliance
**Rating: 5 (Excellent)**

The authors provide a specific acknowledgment regarding AI-assisted ideation (Claude, Gemini, GPT) in the Acknowledgments section, citing a companion methodology paper. This level of transparency regarding Generative AI usage is commendable and exceeds current standard requirements. No conflicts of interest are apparent.

### 6. Scope & Referencing
**Rating: 5 (Excellent)**

The paper fits perfectly within the scope of *IEEE TAES*, bridging space systems engineering, communications, and autonomous control. The references are comprehensive, covering historical foundations (O'Neill, Reynolds), standard texts (Wertz/SMAD), and very recent developments (Starlink, Kuiper, current distributed systems literature). The inclusion of non-archival but relevant industry citations (Starlink operations) is appropriate given the fast-moving nature of the field.

---

## Major Issues

1.  **Centralized Baseline Parameterization ($c=1$):**
    While the authors state that the single-server model is an "intentional bound," Figure 2 shows the centralized overhead/latency diverging sharply at $10^4$ nodes. This divergence is driven by the $M/D/1$ queue saturation. However, as noted in Table II, a hyperscale data center ($c=1000$) would not saturate until $10^7$ nodes.
    *   *Critique:* Visualizing the single-server failure mode in Figure 2 weakens the paper because it attacks a "straw man." A competent ground segment for 10,000 satellites would never use a single server.
    *   *Requirement:* The authors should consider plotting a "Parallelized Ground" curve (e.g., $c=100$) in Figure 2 or explicitly annotating the plot to indicate that the divergence is processing-limited, not bandwidth-limited. The text argues that *spectrum* and *propagation* are the real killers for centralized control; the plot should ideally reflect that, or at least not visually overemphasize the processing bottleneck.

2.  **TDMA vs. Random Phase Discrepancy:**
    The paper identifies a zero-drop threshold of 50 kbps for random-phase scheduling but notes that TDMA would require only ~24 kbps (plus overhead). The abstract mentions "MAC-adjusted $\geq 59$ kbps," which seems to apply the efficiency factor $\gamma$ to the *random-phase* result (50 / 0.85).
    *   *Critique:* This is confusing. If one implements TDMA, one eliminates the random-phase collisions. Therefore, the requirement should be based on the TDMA capacity ($23.9$ kbps) divided by $\gamma$, not the random-phase capacity ($50$ kbps) divided by $\gamma$. The current recommendation of 59 kbps appears to double-count the penalty (paying for random collisions *and* TDMA guard bands).
    *   *Requirement:* Clarify the calculation in the Abstract and Section IV-G. If the system uses TDMA, the base capacity requirement drops to the theoretical minimum (~20.5 kbps). The 59 kbps figure seems to be a worst-case conservative bound, but the derivation needs to be precise.

---

## Minor Issues

1.  **Abstract, Line 15:** "protocol beyond baseline telemetry..." The phrasing here is dense. Consider simplifying to "Protocol overhead is $\eta = 20.66\%$ (excluding baseline telemetry)."
2.  **Section III-B-2 (Hierarchical Topology):** The text states "regional coordinators forward 1024-byte region summaries." Later, Figure 6 shows "Region Summary" as a distinct message type. Please clarify if the Regional Coordinator aggregates *all* cluster summaries into one message, or sends a summary *per* cluster. The aggregation ratio math suggests the former, but explicit confirmation is helpful.
3.  **Section IV-B (Cluster Size):** The text mentions "smaller clusters ($k_c < 50$) generate excessive inter-cluster traffic." However, Figure 5 shows overhead is nearly invariant. The text should clarify that "excessive" refers to *message count* or *processing load* at the regional level, not necessarily total byte overhead.
4.  **Figure 4 (Failure Resilience):** The x-axis is "Node Failure Rate." Is this per year or per second? The text mentions 2%/year. If the x-axis goes up to high percentages (e.g., 10-20%), please clarify the time unit.
5.  **Equation 10 (Power Overhead):** The equation $\Delta P_{\text{avg}} = 15\text{W} / 100 = 0.15\text{W}$ assumes the coordinator power is *additional* to baseline. The text says "15--20 W in coordinator mode" vs "5 W baseline." So $\Delta P = 10$--$15$ W. The math is correct, but the text "15--20 W" implies the *total* power, not the delta. Please ensure consistency in terminology.

---

## Overall Recommendation

**Recommendation: Minor Revision**

This is a high-quality paper that makes a significant contribution to the field of space systems engineering. The simulation framework is rigorous, and the results are valuable for the design of future mega-constellations. The "Major Issues" identified above regarding the centralized baseline visualization and the TDMA bandwidth calculation require clarification and potentially minor re-plotting/re-calculation, but do not invalidate the core findings. The manuscript is suitable for publication in *IEEE TAES* once these points are addressed.

---

## Constructive Suggestions

1.  **Refine the Bandwidth Recommendation:** In the Abstract and Conclusion, explicitly distinguish between the "Unscheduled/Random Access" requirement (~50 kbps) and the "Scheduled/TDMA" requirement (~24 kbps / $\gamma \approx 28$ kbps). The current "59 kbps" figure likely overestimates the TDMA requirement. This is good news for the design—it's easier to meet!
2.  **Strengthen the Centralized Argument:** In Section IV-A, deemphasize the processing saturation ($M/D/1$) and emphasize the *uplink spectrum bottleneck*. A simple calculation showing that $10^5$ nodes $\times$ 1 kbps = 100 Mbps uplink is manageable, but $10^6$ nodes = 1 Gbps (approaching single-beam limits) would be a stronger physical argument than server queuing.
3.  **Visualizing the Sectorized Mesh:** Figure 2 is excellent. Consider adding a small inset or a secondary panel that specifically zooms in on the difference between the Hierarchical and Sectorized Mesh curves, as this comparison is the most novel architectural contribution.
4.  **Future Work - Correlated Failures:** Since you cannot run new simulations for this revision, expand the "Unresolved Questions" (Section V-D) to explicitly mention "Geographically correlated outages due to regional jamming or localized space weather," which is a key military/defense concern for swarms.