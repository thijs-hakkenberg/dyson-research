---
paper: "02-swarm-coordination-scaling"
version: "cg"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-03-01"
recommendation: "Unknown"
---

**Review of Manuscript Version CG**
**Title:** Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms
**Target Journal:** IEEE Transactions on Aerospace and Electronic Systems

---

### 1. Significance & Novelty
**Rating: 5 (Excellent)**
This manuscript addresses a critical gap in the literature between abstract swarm algorithms and physical-layer reality. While swarm robotics and mega-constellation routing are well-studied in isolation, the specific parametric sizing of the *coordination layer*—specifically accounting for byte-level overheads, framing, and TDMA constraints—is a novel and highly relevant contribution. The derivation of closed-form sizing equations for $10^3$--$10^5$ node regimes is particularly valuable for systems engineers.

### 2. Methodological Soundness
**Rating: 5 (Excellent)**
The multi-fidelity approach is rigorous. The authors successfully integrate three distinct layers of abstraction:
1.  **Analytical:** Closed-form mean-value equations.
2.  **Message-Level DES:** Validates the byte budget and provides tail statistics (e.g., buffer occupancy).
3.  **Slot-Level/Packet-Level:** Crucially, the authors do not rely solely on fluid-flow approximations. The inclusion of a slot-level simulator to capture half-duplex turnaround and ARQ interactions (Table VII) and the derivation of $\gamma$ from CCSDS standards (Section IV-J) provides a high degree of confidence in the results.

### 3. Validity & Logic
**Rating: 4 (Good)**
The internal logic is consistent. The transition from the "byte budget" (Layer 1) to "airtime schedulability" (Layer 2) is well-reasoned. The use of the Gilbert-Elliott (GE) model to demonstrate the infeasibility of intra-cycle ARQ under slow fading is a strong logical step.
*Critique:* There is a subtle tension regarding the RF-backup mode capacity versus the Coordinator requirements that needs explicit resolution (detailed in Major Issue #1).

### 4. Clarity & Structure
**Rating: 4 (Good)**
The paper is dense but well-organized. The distinction between "Model S" (simplified) and "Model C" (CCSDS) is necessary but adds cognitive load; the authors handle this reasonably well by explicitly flagging which model is used for feasibility claims. Figures are informative, particularly Fig. 10 (Buffer CDF) and Fig. 12 (GE Recovery).

### 5. Ethical Compliance
**Rating: 5 (Excellent)**
The authors provide a link to source code and datasets, enhancing reproducibility. AI usage is disclosed in the acknowledgments.

### 6. Scope & Referencing
**Rating: 5 (Excellent)**
The scope is perfectly aligned with *IEEE TAES*. The literature review covers the necessary bases, bridging swarm robotics (Dorigo et al.) with space networking (CCSDS, DTN) and constellation operations.

---

### Major Issues

**1. Feasibility of Hierarchical Coordination in RF-Backup Mode**
*   **Issue:** The manuscript establishes that a Cluster Coordinator requires an ingress capacity of ${\sim}27$ kbps (Eq. 4) to sustain the hierarchical protocol ($k_c=100$). However, Table III (Link Budget) indicates the RF-backup mode (UHF Omni) has a maximum physical rate of ${\sim}2.5$ kbps.
*   **Why it matters:** This implies that the hierarchical topology *cannot function* in RF-backup mode. The coordinator simply cannot ingest the reports. The text mentions "safe hold" and "inertial coasting" during RF backup, but the feasibility analysis (e.g., Table VIII, Regime B) is slightly ambiguous about whether *coordination* continues or if the system reverts to a silence/beacon-only state.
*   **Remedy:** Explicitly state that the hierarchical coordination protocol is **suspended** during RF-backup operations due to the 2.5 kbps < 27 kbps deficit. Clarify that RF-backup is exclusively for "survival/safe-mode" (heartbeats + collision alerts only) and cannot support the standard status reporting loop.

**2. Centralized vs. Distributed Command Generation Overhead**
*   **Issue:** The stress-case overhead ($\eta_{cmd} \approx 41\%$) assumes centralized command generation (ground or high-level autonomous agent) pushed down to the fleet. If the swarm utilizes distributed decision-making (e.g., consensus), the traffic pattern changes from $1 \to N$ (broadcast) to $N \to N$ (all-to-all or gossip).
*   **Why it matters:** The paper claims the results are "topology-invariant" under centralized assumptions. However, for a paper on "Autonomous Space Swarms," distributed consensus is a likely operational mode. The current text briefly mentions consensus ($\eta \approx 30.7\%$) in Section IV-E, but the implications for the sizing equations (specifically Eq. 2) are not fully integrated.
*   **Remedy:** In the Discussion or Section IV-E, provide a clearer distinction: "If command generation is distributed (consensus), $\eta_{cmd}$ is no longer topology-invariant and scales as $O(k_c^2)$ or $O(k_c)$ depending on the consensus algorithm." A brief qualitative qualification of the "topology-invariant" claim in the abstract is also warranted.

---

### Minor Issues

1.  **Gamma Notation:** In Eq. 13, the term $10^{-3}$ is used to convert units. Please explicitly state the units for $R_{PHY}$ (bps vs kbps) in the text immediately surrounding the equation to prevent implementation errors by practitioners.
2.  **Figure 10 Interpretation:** The caption describes the Bernoulli distribution as "bimodal." Technically, the distribution of *bytes* is bimodal (zero vs. full), but the underlying process is Bernoulli. The text is clear, but ensure the caption distinguishes between the *process* and the *resultant buffer state*.
3.  **Table VIII Clarification:** The column headers "$M_r=0$" and "$M_r=2$" for Regime B (RF-backup) could be confusing given the finding that ARQ is infeasible at low rates. A footnote clarifying that "$M_r=2$ is theoretical/byte-budget only for Regime B" would help.
4.  **Abstract Precision:** The abstract mentions "Coordinator ingress $\approx 27$ kbps... confirming 30 kbps as minimum." It would be helpful to clarify that this is for the *Cluster* coordinator specifically, as Regional coordinators have different loads.

---

### Overall Recommendation
**Recommendation: Accept with Minor Revisions**

This is a high-quality, rigorous manuscript that makes a significant contribution to the systems engineering of large-scale space swarms. The authors have successfully moved beyond abstract algorithmic scaling to provide concrete, standards-grounded sizing equations. The "Three-Layer" feasibility framework is a robust tool for the community.

The requested revisions are primarily clarifications regarding the operational limits of the RF-backup mode and the boundaries of the "topology-invariant" assumption. Once these are addressed to prevent reader misconception, the paper is ready for publication.

### Constructive Suggestions

1.  **Refine Algorithm 1:** Consider adding a "Mode Check" step at the very beginning. `IF Mode == RF_Backup AND Capacity < Ingress_Req THEN Revert to Safe_Mode`. This formalizes the finding that the hierarchy is bandwidth-constrained in backup modes.
2.  **Generalized Gamma Plot:** A small subplot showing $\gamma$ vs. $R_{PHY}$ (Eq. 13) would be visually instructive to show how efficiency drops off at very high rates (due to fixed guard times) or very low rates (due to header overhead), helping practitioners find the "sweet spot."
3.  **AoI Context:** In Section IV-B, explicitly link the 440s AoI to the "Safe Mode" discussion. Since RF-backup forces the system into a low-bandwidth state, the 440s latency confirms that only strategic (not tactical) deconfliction is possible in that mode.