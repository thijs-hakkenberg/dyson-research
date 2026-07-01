---
paper: "02-swarm-coordination-scaling"
version: "be"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-27"
recommendation: "Accept"
---

Here is a rigorous peer review of the manuscript "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version BE), prepared for *IEEE Transactions on Aerospace and Electronic Systems*.

---

# Peer Review Report

**Manuscript Title:** Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms
**Target Journal:** IEEE Transactions on Aerospace and Electronic Systems

## Review Criteria

### 1. Significance & Novelty
**Rating: 5 (Excellent)**

This manuscript addresses a critical and timely gap in the literature: the specific scaling properties of coordination architectures for "mega-constellations" ($10^4$--$10^5$ nodes). While existing literature covers routing (networking) or small-scale formation flying (GNC), there is a scarcity of work that treats the *command and control* (C2) layer as a distributed systems problem with strict bandwidth constraints. The derivation of closed-form sizing relationships for this regime is a high-value contribution for practitioners.

The distinction between "architecture-specific overhead" (nominal) and "workload-dependent overhead" (stress-case) is a novel and useful framing. The finding that hierarchical overhead is dominated by command traffic rather than topology maintenance challenges the common assumption that hierarchy maintenance is prohibitively expensive in dynamic networks. The specific focus on the "RF-backup regime" (1 kbps) is particularly significant for system robustness analysis, as this is often the failure mode that kills constellations.

### 2. Methodological Soundness
**Rating: 4 (Good)**

The methodology combines standard queueing theory ($M/D/1$, $D/D/1$) with a custom cycle-aggregated Discrete Event Simulation (DES). The approach is generally rigorous. The authors use the DES primarily to validate the closed-form equations and to explore tail statistics (like Gilbert-Elliott recovery) that are hard to derive analytically. This is a sound approach.

However, there is a slight tension in the "Coordinator Capacity Sizing" section (IV-A). The paper presents three models (A, B, and TDMA). While the convergence of these models is argued well, the reliance on a "token bucket" model to approximate PHY-layer time-division admission is an abstraction that requires careful justification. The authors acknowledge this, but the link between the token bucket parameters and the physical TDMA slot structure could be made more explicit. Additionally, the assumption of static cluster membership for a 1-year simulation of LEO swarms is a strong simplification. While the authors justify this by stating that re-association overhead is low ($<0.5\%$), the *transient* effects of re-association on latency and packet loss during cross-plane maneuvers are not fully captured.

### 3. Validity & Logic
**Rating: 5 (Excellent)**

The logic is tight and the conclusions follow directly from the data. The authors are commendably careful with their definitions (e.g., distinguishing "offered" vs. "delivered" overhead, and "queue drops" vs. "link losses"). The analysis of the Gilbert-Elliott (GE) link model is a highlight; the demonstration that intra-cycle retransmission is structurally ineffective under correlated fading is a crucial insight that invalidates many naive ARQ schemes.

The "Validation Gap" section (V-A) is refreshing in its honesty. By explicitly listing what is *not* modeled (MAC contention, specific orbital mechanics), the authors strengthen the validity of what *is* modeled. The comparison between the hierarchical approach and the sectorized mesh is fair, highlighting the bandwidth-robustness trade-off rather than declaring a simple "winner."

### 4. Clarity & Structure
**Rating: 4 (Good)**

The paper is dense but well-organized. The progression from research questions to simulation framework to results is logical. The "Design Equations Summary" in Section V-C is an excellent addition that increases the paper's utility.

*Minor critique:* The notation is generally clear, but the density of variables in the abstract and introduction (e.g., $\eta$, $\gamma$, $p_{BG}$) can be overwhelming before they are formally defined. Table I helps, but the text is heavy. The distinction between "Type 1" and "Type 2" commands in Section IV-A is vital but buried in the middle of a paragraph; it deserves more visual prominence (perhaps a sub-table or bullet list) given its impact on the schedulability conclusion.

### 5. Ethical Compliance
**Rating: 5 (Excellent)**

The authors include a specific acknowledgment regarding AI-assisted ideation (Claude, Gemini, GPT), citing a methodology paper. This transparency is exemplary and aligns with emerging best practices. No conflicts of interest are apparent.

### 6. Scope & Referencing
**Rating: 5 (Excellent)**

The scope is perfectly aligned with *IEEE TAES*. The references are comprehensive, spanning classical queueing theory (Kleinrock), distributed algorithms (Lynch, Lamport), and modern constellation operations (Starlink, Kuiper). The inclusion of CCSDS standards (Space Packet Protocol, Proximity-1) grounds the theoretical work in engineering reality.

---

## Major Issues

None. The manuscript is technically sound. The limitations (static topology, simplified MAC) are clearly acknowledged and do not invalidate the core contributions regarding bandwidth sizing and protocol overhead scaling.

---

## Minor Issues

1.  **Section IV-A (TDMA Frame Model):** The derivation of $\gamma = 0.949$ is optimistic. While the math holds for the assumptions given, a 4.7 ms guard time for a 92.7 ms slot is tight for a distributed system without a central atomic clock, relying on potentially degraded GNSS. The authors conservatively use $\gamma = 0.85$ for the rest of the paper, which is good, but the text should perhaps emphasize *why* 0.949 is likely unachievable in practice (e.g., clock drift between sync beacons, software jitter).
2.  **Table III (Per-Node Bandwidth Breakdown):** The "Global-State Mesh" column lists ">1 kbps" and "Exceeds." It would be more impactful to provide the specific estimated number (e.g., "~73 MB/cycle" as derived in the text) to quantify *how much* it exceeds the budget.
3.  **Section IV-C (GE Model):** The text states "The assumption is conservative for recovery." This is true. However, it might be worth briefly mentioning that if the fading coherence time is *exactly* synchronized with the cycle time (unlikely but theoretically possible), the model might behave differently. The current justification is sufficient but could be tightened.
4.  **Fig. 6 (Inter-cycle recovery):** The caption mentions "DES bars" but the plot description implies curves. Ensure the visual representation (bars vs. lines) is clearly described.
5.  **Typos/Formatting:**
    *   Section III-B-2: "RequestVote: 100 B x quorum of ~5" — The formatting of "x" should be consistent (use $\times$).
    *   Table VII: The footnote regarding "Processing limit at c=1" is slightly cut off or dense in the LaTeX source; ensure it renders cleanly in the final PDF.

---

## Overall Recommendation

**Accept / Minor Revision**

This is a high-quality paper that provides a rigorous analytical foundation for the design of future large-scale space systems. The combination of closed-form derivations and Monte Carlo verification provides a robust toolkit for system architects. The revisions requested are minor clarifications to improve readability and emphasize the practical conservatism of the parameters.

---

## Constructive Suggestions

1.  **Enhance the "Type 1 vs. Type 2" Command Distinction:** In Section IV-A, explicitly separate the discussion of Broadcast (Type 1) vs. Unicast (Type 2) commands. The fact that Unicast commands require 22 cycles to clear is a massive operational constraint. Consider adding a small table or a call-out box summarizing "Command Schedulability" to make this finding impossible to miss.
2.  **Strengthen the Static Topology Justification:** In Section V-B (Limitations), expand slightly on the "cross-plane" scenario. A brief sentence estimating the percentage of the fleet undergoing re-association at any given moment (likely small) would further justify why the static assumption doesn't invalidate the bandwidth results.
3.  **Clarify "RF-Backup" Context:** In the Introduction, explicitly state that the 1 kbps budget is a *design constraint for robustness*, not the primary operational link (which is likely optical/Ka-band). While mentioned later, placing this upfront prevents readers from thinking the authors are proposing to run a mega-constellation solely on 1 kbps links.
4.  **Visualizing the Bottleneck:** Figure 3 (TDMA comparison) is good, but a simple diagram showing the "Coordinator Funnel" — visualizing the 100:1 compression ratio and the resulting ingress pressure — might help readers intuitively grasp why the coordinator ingress is the binding constraint.