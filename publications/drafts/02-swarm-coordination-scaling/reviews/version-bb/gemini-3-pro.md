---
paper: "02-swarm-coordination-scaling"
version: "bb"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-27"
recommendation: "Accept"
---

Here is a rigorous academic peer review of the manuscript "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version BB), prepared for *IEEE Transactions on Aerospace and Electronic Systems*.

---

# Peer Review Report

**Manuscript ID:** [Assigned by Editor]
**Title:** Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms
**Target Journal:** IEEE Transactions on Aerospace and Electronic Systems

## Review Criteria

### 1. Significance & Novelty
**Rating: 5 (Excellent)**

This manuscript addresses a critical and timely gap in the literature: the scalability of coordination architectures for mega-constellations ($10^4$--$10^5$ nodes). While existing literature covers routing (ISL) and small-scale swarms ($<100$ agents), there is a distinct lack of rigorous sizing models for the "mid-tier" coordination layer that sits between physical link management and high-level mission planning.

The derivation of closed-form design equations for coordinator ingress sizing and Age-of-Information (AoI) under constrained bandwidth (1 kbps RF-backup) is a significant contribution. The paper effectively bridges the gap between abstract distributed systems theory and practical spacecraft operations. The differentiation between "nominal" and "stress-case" workloads provides valuable bounds for system architects. The focus on the RF-backup regime is particularly relevant for resilience engineering, a high-priority topic for operators like Starlink and Kuiper.

### 2. Methodological Soundness
**Rating: 4 (Good)**

The methodology combines analytical derivation (queueing theory, Markov chains) with a custom Cycle-Aggregated Discrete Event Simulation (DES). The approach is generally robust.
*   **Strengths:** The use of a Gilbert-Elliott (GE) model to capture correlated link losses is appropriate for the space environment. The cross-verification between closed-form equations and DES results (matching within 0.1%) builds confidence in the arithmetic consistency of the models.
*   **Weaknesses:** The primary methodological limitation is the abstraction of the MAC layer. While the authors derive $\gamma$ (MAC efficiency) based on a TDMA frame structure in Section IV.A, the simulation itself is "cycle-aggregated" and does not simulate packet collisions or slot timing violations directly. The paper acknowledges this "Validation Gap" (Section V.A), but for *IEEE TAES*, the reliance on $\gamma$ as a scalar proxy for all MAC dynamics is a simplification that warrants slightly more scrutiny, particularly regarding synchronization overheads in the stress case.

### 3. Validity & Logic
**Rating: 5 (Excellent)**

The logical flow is rigorous. The authors carefully define their terms (e.g., the distinction between "offered" vs. "delivered" overhead, and "link loss" vs. "queue drop").
*   **Coordinator Sizing:** The conclusion that coordinator ingress capacity ($\sim$21-25 kbps) is the binding constraint—rather than CPU processing—is well-supported by the data.
*   **GE Recovery:** The finding that intra-cycle retransmission is ineffective under correlated fading (due to the coherence time assumption) is logically sound and leads to the important conclusion that inter-cycle recovery is the dominant mechanism.
*   **Independence:** The demonstration in Section IV.D that GE losses and queue drops are decoupled under dedicated links is a valuable insight for system designers.

### 4. Clarity & Structure
**Rating: 4 (Good)**

The paper is well-written, dense with technical content, and professionally formatted.
*   **Notation:** Table I is helpful, though the distinction between $C_{node}$ (average budget) and $C_{coord}$ (ingress rate) needs to be emphasized even more strongly in the introduction to avoid reader confusion.
*   **Figures:** The figures are generally clear. Figure 4 (TDMA comparison) and Figure 6 (Cross-cycle recovery) are particularly effective.
*   **Minor Issue:** The transition between the general hierarchical model and the specific "RF-backup" use case could be smoother. The abstract mentions the 1 kbps budget immediately, but the generalizability to higher bandwidths (Table II) is sometimes lost in the detailed discussion of the low-bandwidth constraints.

### 5. Ethical Compliance
**Rating: 5 (Excellent)**

The authors include a specific acknowledgment regarding AI-assisted ideation (Claude, Gemini, GPT), citing a specific internal report. This transparency is commendable and aligns with emerging publication standards. No obvious conflicts of interest or ethical concerns regarding the research content are apparent.

### 6. Scope & Referencing
**Rating: 5 (Excellent)**

The paper fits perfectly within the scope of *IEEE TAES*, specifically the areas of Space Systems and Command & Control. The referencing is extensive and current, citing both foundational texts (Kleinrock, Wertz) and recent developments (Starlink FCC filings, mega-constellation routing papers). The comparison against "Global-State Mesh" and "Centralized" baselines provides necessary context for the hierarchical contribution.

---

## Major Issues

1.  **MAC Layer Abstraction vs. TDMA Feasibility (Section IV.A):**
    The paper relies heavily on the parameter $\gamma$ to represent MAC efficiency. In Section IV.A, the authors calculate $\gamma \approx 0.949$ but conservatively use $0.85$. However, the feasibility check (Eq. 9 and 10) suggests that under GE steady-state ($\bar{M}_r = 0.18$), the ingress time exceeds $T_c$.
    *   *Critique:* The paper states intra-cycle retry is "infeasible" under GE. However, the simulation seems to allow $M_r$ retries to contribute to "offered load" statistics even if they wouldn't fit in the time slot.
    *   *Requirement:* Clarify if the DES enforces the *time-slot* constraint for retries, or only the *byte-count* constraint. If the DES allows retries that would physically push the transmission past $T_c$, the "Delivered $\eta$" in Table XI might be optimistic.

2.  **Sectorized Mesh "Capped" Definition:**
    In Section III.B.4, the "Capped-fanout sectorized mesh" restricts heartbeats to $\min(k_s - 1, 10)$.
    *   *Critique:* This cap seems arbitrary and potentially unfair to the mesh topology. By capping neighbors at 10 when the sector has 317 nodes, the mesh is forced into a disconnected state (3.2% coverage). Comparing the overhead of a *disconnected* mesh against a *fully connected* hierarchical cluster is an "apples-to-oranges" functional comparison, even if the byte-level comparison is accurate.
    *   *Requirement:* The authors should explicitly acknowledge that the "Capped Mesh" is not functionally equivalent to the Hierarchical model in terms of fleet-wide reachability. It serves as a "local awareness" baseline, not a "command dissemination" baseline. This distinction is made in the text but should be highlighted in the Abstract or Conclusion to prevent misleading takeaways.

---

## Minor Issues

1.  **Table II (Bandwidth Scaling):** The row "AoI P99 (exception)" lists "440 s" for all bandwidth regimes. While mathematically true that AoI depends on $T_c$ and $p_{exc}$, higher bandwidths (100 kbps) would likely allow for a shorter $T_c$ (e.g., 1s instead of 10s). Keeping $T_c$ fixed at 10s for a 100 kbps system seems artificial. A footnote explaining that $T_c$ is held constant for comparison would be helpful.
2.  **Section IV.A (TDMA Sync):** The paper mentions a "sync beacon (8 bits)." 8 bits seems incredibly short for a synchronization sequence in a noisy RF environment involving Doppler and potential interference. A standard CCSDS sync marker is usually 32 bits (ASM). This is a negligible overhead difference, but "8 bits" hurts credibility regarding PHY realism.
3.  **Equation 5 (Mesh Messages):** The complexity is listed as $O(N \cdot f \cdot \log N)$. Standard gossip complexity to reach all nodes is usually $O(N \log N)$. The inclusion of $f$ (fanout) is correct, but the notation could be cleaner.
4.  **Figure 5 (AoI):** The y-axis is log-scale? The text says "Geometric growth," but the visual curve looks linear or polynomial. Please verify the axis scaling or the descriptor.
5.  **Typos/Formatting:**
    *   Section III.A: "Palm--Khintchine" (spelling check).
    *   Table VIII: The header "Handoff Cost" appears twice; the first instance seems to refer to "System Avail."

---

## Overall Recommendation

**Accept with Minor Revisions**

This is a high-quality paper that provides valuable engineering tools for the design of large-scale satellite constellations. The analytical models are rigorous, and the simulation results are presented clearly. The "Major Issues" identified above require clarification in the text but do not invalidate the core results. The distinction between the functional capabilities of the capped mesh vs. the hierarchical tree is the most important point to clarify to ensure fair comparison.

---

## Constructive Suggestions

1.  **Refine the Mesh Comparison:** Rename "Sectorized Mesh" to "Local-Neighborhood Mesh" or similar in the plots/tables to emphasize that it provides a different service (local safety) compared to the Hierarchical model (fleet management). This clarifies why the overheads differ.
2.  **Expand on Synchronization:** Add a brief paragraph or footnote in Section IV.A regarding the practical implementation of TDMA sync in the absence of GNSS. The reliance on a coordinator beacon is a single point of failure for the timing reference; briefly mention how a secondary coordinator might take over timing duties.
3.  **Sensitivity to $T_c$:** The paper fixes $T_c = 10s$. A brief discussion (or a single plot) showing how overhead scales if $T_c$ is reduced to 1s (for tighter control loops) would add significant value. It would likely show that the 1 kbps budget is untenable at $T_c=1s$, reinforcing the paper's choice of 10s.
4.  **Packet-Level Future Work:** In the "Validation Gap" section, explicitly mention *which* specific NS-3 modules (e.g., `lr-wpan` or `wifi` adapted for long delays) would be appropriate for this validation. This guides future researchers.