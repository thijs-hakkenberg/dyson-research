---
paper: "02-swarm-coordination-scaling"
version: "da"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-03-05"
recommendation: "Unknown"
---

Here is a rigorous peer review of the manuscript "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version DA), structured for *IEEE Transactions on Aerospace and Electronic Systems*.

---

# Peer Review Report

**Manuscript ID:** [Assigned by Editor]
**Title:** Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms
**Version:** DA

## 1. Significance & Novelty
**Rating: 4 (Good)**
The paper addresses a critical gap in the literature: the specific sizing relationships for coordinating "mega-constellation" scale swarms ($10^4$--$10^5$ nodes) where centralized ground control fails. While high-level architectural concepts for swarms exist, this work provides concrete, closed-form engineering sizing equations (the "byte budget" and "airtime" tests) that are directly usable by systems engineers. The derivation of the "campaign duty factor" ($d$) to bridge the gap between continuous and episodic workloads is a significant practical contribution. The novelty lies not in new fundamental network theory, but in the rigorous application and parameterization of these theories for the specific constraints of S-band inter-satellite links (ISL).

## 2. Methodological Soundness
**Rating: 5 (Excellent)**
The methodology is robust. The authors employ a multi-tiered verification approach (Tier 1-3) that is intellectually honest about what has been proven (code correctness, internal consistency) versus what remains unvalidated (external physical channel behavior). The shift from a simplified TDMA model (Model S) to a CCSDS-grounded model (Model C) for all feasibility claims is a major strength. The use of Gilbert-Elliott (GE) models as a "what-if" design tool rather than a predictive truth is the correct approach given the lack of on-orbit ISL channel data. The two-test feasibility framework (Test A: Bytes, Test B: Airtime) is logically sound and mathematically consistent.

## 3. Validity & Logic
**Rating: 5 (Excellent)**
The logic is tight. The paper meticulously distinguishes between information rate, PHY rate, and effective throughput. The identification of the "ARQ $\times$ TDMA coupling" (where retransmissions break the schedule at lower rates) is a subtle but valid finding. The authors correctly identify that the 1 kbps per-node budget is a logical allocation, not a physical link limit, and properly contextualize the stress-case ($\eta \approx 46\%$) as an upper bound that occurs rarely. The distinction between the S-band coordination channel and the UHF backup channel (and the suspension of hierarchy during backup) resolves potential logical conflicts regarding bandwidth.

## 4. Clarity & Structure
**Rating: 4 (Good)**
The paper is dense but well-structured. The "Rate Ladder" (Table IV) and the "Feasibility Test" (Algorithm 1) are excellent synthesis tools that make the complex derivations accessible. The explicit definition of overhead terms ($\eta_0$, $\eta_{\text{cmd}}$, $\eta_{\text{total}}$) prevents ambiguity. However, the density of variables and parenthetical values in the text can occasionally hinder readability. The distinction between Model S and Model C is clear, but the reader must be careful not to conflate the two when looking at figures (though the captions are generally good).

## 5. Ethical Compliance
**Rating: 5 (Excellent)**
The authors provide a clear Data Availability statement pointing to a repository with source code and calculators. The acknowledgment of AI usage for ideation/editing (but not data generation) is transparent and complies with modern ethical standards.

## 6. Scope & Referencing
**Rating: 4 (Good)**
The scope is well-suited for *IEEE TAES*. The referencing covers the necessary bases: swarm robotics, constellation management, and CCSDS standards. The inclusion of recent mega-constellation literature (Starlink, Kuiper) alongside classical queueing theory (Kleinrock) and networking standards (CCSDS Proximity-1) is appropriate.

---

## Major Issues

1.  **Sensitivity of $\gamma$ to Doppler-Induced Guard Time**
    *   **Issue:** The paper asserts that Doppler ($\pm 50$ kHz) is handled by the acquisition preamble and does not impact the guard time ($T_{\text{guard}}$). While true for frequency lock, high Doppler rates in LEO cross-plane links can result in significant range-rate changes during a slot, potentially requiring larger guard times to prevent slot overlap at the edges of the cluster, or requiring dynamic guard bands.
    *   **Why it matters:** If $T_{\text{guard}}$ needs to be 10ms instead of 4.7ms to account for worst-case range-rate variation or loose synchronization, $\gamma$ drops further, potentially threatening the 35 kbps recommendation.
    *   **Remedy:** Add a brief calculation or justification regarding the maximum range-rate ($\dot{\rho}$) within a cluster and its impact on slot timing over the slot duration. If $\dot{\rho} \times T_{\text{slot}}$ is negligible, state this explicitly. If not, adjust the guard time sensitivity analysis (Fig. 2) to reflect this.

2.  **Raft Election Storm on UHF Backup**
    *   **Issue:** The paper mentions a "thundering herd" scenario where 100 nodes attempt Raft election on a 2.5 kbps UHF link using Slotted ALOHA. The analysis claims convergence in $\sim 160$s. However, Slotted ALOHA collapses under high load ($G \gg 1$). The Binary Exponential Backoff (BEB) logic is described, but with 100 nodes starting simultaneously, the collision probability is near 100% for the first several rounds.
    *   **Why it matters:** If the backup link is saturated by the election protocol, the cluster cannot recover from a coordinator failure, rendering the "robustness" claim invalid.
    *   **Remedy:** Provide a more rigorous justification for the UHF election convergence. Specifically, confirm that the BEB window expansion ($W_{max}=64$) is sufficient for $N=100$. A simple simulation or reference to standard ALOHA backoff convergence times for $N=100$ would strengthen this claim.

## Minor Issues

1.  **Clarification of "Logical" vs. "Physical" 1 kbps:** While Table II helps, the text should reiterate early on that the "1 kbps per-node budget" is a traffic shaping rule enforced by software, not a hardware limit of the S-band radio. This prevents confusion when the paper later discusses 35 kbps links.
2.  **Table I (Notation):** The definition of $\alpha_{RX}$ is dense. Consider moving the formula to the text or a footnote to make the table cleaner.
3.  **Fig. 3 (Gamma vs. Rate):** The "Model S" curve is prominent but explicitly "not for recommendations." Consider making the Model S curve dashed or lighter to visually de-emphasize it compared to the Model C curve.
4.  **Equation 6 (Consensus):** The variable $f_{\text{decision}}$ is defined as "decisions per cycle," but the context implies it might be a fraction. Clarify if this is an integer count or a frequency.
5.  **Typos:** Section IV-A mentions "margin = -1,300 ms" (negative margin). While mathematically correct for "deficit," phrasing it as "deficit of 1,300 ms" might be clearer.

---

## Overall Recommendation
**Recommendation: Accept with Minor Revisions**

This is a high-quality, rigorous engineering paper that successfully bridges the gap between abstract swarm theory and practical spacecraft communications design. The derivation of the "two-test" feasibility framework and the "campaign duty factor" provides a valuable toolkit for systems engineers. The authors have been meticulous in grounding their parameters in CCSDS standards (Model C) rather than relying on simplified assumptions.

The paper is ready for publication subject to addressing the specific concerns regarding Doppler effects on guard times and the stability of the UHF election backup. These are not fatal flaws but require tighter technical justification to ensure the proposed architecture is truly robust.

## Constructive Suggestions (Ordered by Impact)

1.  **Strengthen the UHF Election Analysis:** Add a sentence or footnote explicitly validating that the Slotted ALOHA backoff parameters ($W_0, W_{max}$) prevent persistent collision deadlock for $N=100$.
2.  **Expand Doppler Justification:** Explicitly calculate the maximum timing error introduced by relative motion during a single slot to confirm the 4.7ms guard is sufficient.
3.  **Visual Hierarchy in Figures:** In Figure 3, visually subordinate the "Model S" data to prevent readers from extracting optimistic values by mistake.
4.  **Algorithm 1 Refinement:** In Line 15 of Algorithm 1, clarify if $L_{\text{cmd}}$ is a hard constraint or just an output. If $L_{\text{cmd}} > \text{some limit}$, does the test fail?
5.  **Gamma Lookup Table:** In Table VIII, explicitly state that these values assume the specific framing overheads of CCSDS Proximity-1. A user with a different framing structure (e.g., AX.25) would need to recompute.