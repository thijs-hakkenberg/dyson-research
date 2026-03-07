---
paper: "02-swarm-coordination-scaling"
version: "dp"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-03-07"
recommendation: "Unknown"
---

Here is a comprehensive peer review of the manuscript **"Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version DP)**.

---

## 1. Significance & Novelty
**Rating: 5 (Excellent)**
The paper addresses a critical gap in the literature: the specific sizing relationships for coordinating "mega-constellation" scale swarms ($10^4$--$10^5$ nodes) using hierarchical architectures. While high-level networking for such constellations is well-studied (ISL routing), the specific command-and-control (C2) traffic dimensioning has been largely ignored or assumed to be negligible. The derivation of closed-form equations linking byte-level budgets to TDMA slot physics is a significant contribution for systems engineers. The "Two-Test" framework provides a practical tool for early-phase design.

## 2. Methodological Soundness
**Rating: 4 (Good)**
The modeling approach is generally rigorous. The separation of information-layer constraints (Test A) from physical-layer schedulability (Test B) is logically sound. The inclusion of an independent NS-3 validation study significantly strengthens the paper, addressing a common weakness in analytical modeling papers. The decomposition of the discrepancy between the analytical model and NS-3 (framing, jitter, scheduling) is excellent scientific practice. However, the reliance on a specific set of CCSDS Proximity-1 parameters for the "general" equations requires careful caveats regarding applicability to non-standard radios.

## 3. Validity & Logic
**Rating: 5 (Excellent)**
The internal logic is consistent. The authors have successfully addressed previous concerns regarding the "stress case" by introducing the campaign duty factor ($d$), which properly contextualizes the 46% overhead figure as a rare operational mode rather than a continuous baseline. The handling of the Gilbert-Elliott (GE) channel model is mature; the distinction between intra-cycle ARQ (ineffective under slow fading) and inter-cycle recovery is a crucial insight often missed in similar studies.

## 4. Clarity & Structure
**Rating: 5 (Excellent)**
The manuscript is written with high clarity. The notation is well-defined in Table I. The progression from system model to feasibility framework to results is intuitive. The "Rate Ladder" (Table VI) is a particularly effective pedagogical device for explaining how information rates translate to PHY requirements.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**
The authors provide a clear Data Availability statement pointing to a repository with source code and datasets. The acknowledgment section transparently discloses the use of AI for ideation and editing, adhering to modern ethical guidelines.

## 6. Scope & Referencing
**Rating: 4 (Good)**
The literature review covers relevant ground in swarm robotics, satellite networking, and delay-tolerant networking. The comparison with DVB-RCS2 standards adds industrial relevance. The scope is appropriately bounded to per-cluster sizing, though the fleet-level spatial reuse argument ($R=7$) remains the most speculative part of the paper.

---

## Major Issues

1.  **Fleet-Level Spatial Reuse Validation (Conditional Feasibility)**
    *   **Issue:** The abstract and conclusion state that fleet-level scaling is "conditional on spatial reuse validation ($R \geq 3$)." While the per-cluster analysis is robust, the paper relies on a geometric argument for $R=7$ without an RF interference analysis to back it up. If $R$ must be 1 (due to omnidirectional antennas and lack of frequency planning), the system breaks ($G=25$).
    *   **Why it matters:** The title implies applicability to "Large Autonomous Space Swarms" (implying the whole fleet), but the math is solid only for the cluster. If the inter-cluster interference forces $T_c^{\text{fleet}}$ to 250s, the architecture fails for real-time control.
    *   **Remedy:** The paper should explicitly state in the *System Model* or *Results* that the proposed architecture *requires* directional antennas (or distinct frequency bands) to function at scale. The current text mentions this in passing; it should be a stated requirement, not just a sensitivity analysis result.

2.  **Turnaround Time Sensitivity**
    *   **Issue:** The analysis assumes a specific guard time ($T_{\text{guard}} = 4.7$ ms) and acquisition time. However, half-duplex switching time for COTS S-band transceivers can vary wildly (from $<1$ms to $>50$ms).
    *   **Why it matters:** If the radio hardware requires 20ms to switch from RX to TX, the guard time must increase significantly. In a TDMA scheme with 100 slots per cycle, adding 15ms of dead time per slot consumes 1.5 seconds of the cycle, potentially invalidating the 35 kbps recommendation.
    *   **Remedy:** Add a sensitivity plot or a specific paragraph discussing the maximum tolerable transceiver turnaround time before the 35 kbps link budget is violated. This defines the hardware specification for the radio selection.

## Minor Issues

1.  **Clarification of $\eta$ vs. $\eta_{\text{total}}$:** In the Abstract, the text mentions "routine $\eta \approx 5-10\%$". It would be clearer to explicitly state "routine protocol overhead $\eta \approx 5-10\%$ (total utilization $\approx 25-30\%$)" to avoid confusion with the total link utilization, which includes the 20.5% baseline.
2.  **Table II (Mode Map):** The "RF-backup" row lists "2.5 kbps". Is this effective throughput or PHY rate? Please clarify for consistency with the other rows.
3.  **Equation 6 (Fleet Reuse):** The variable $f_{\text{RF}}$ is defined as the "fraction of clusters requiring simultaneous RF coordination." Please clarify if this assumes that clusters not requiring coordination are silent, or if they are just not transmitting *coordination* messages (but might be transmitting payload data that causes interference).
4.  **Figure 3 (NS-3 Validation):** The caption mentions a "shaded band: $\pm$8% agreement." Ensure this band is clearly visible in the final print version; sometimes light shading is lost.

---

## Overall Recommendation
**Recommendation: Accept with Minor Revisions**

This is a high-quality manuscript that offers a rigorous, closed-form analytical foundation for sizing spacecraft swarm communication networks. The authors have successfully addressed the complexity of mapping byte-level requirements to physical-layer TDMA constraints. The introduction of the "Campaign Duty Factor" ($d$) resolves previous concerns about workload realism, and the independent NS-3 validation provides high confidence in the results.

The primary strength of the paper is the "Two-Test Feasibility Framework," which is likely to become a standard reference for systems engineers in this domain. The weakness lies in the fleet-level interference assumptions, which are acknowledged but not rigorously modeled. However, given the scope is explicitly "per-cluster sizing," this is acceptable provided the hardware requirements (directional antennas) are made explicit.

---

## Constructive Suggestions

1.  **Hardware Specification Table:** Consider adding a small "Recommended Hardware Specification" table. This would summarize the derived requirements: Minimum PHY Rate (35 kbps), Max Turnaround Time (X ms), Antenna Beamwidth (approximate for $R=7$), and Onboard Clock Stability (to support the assumed guard times). This would make the paper immediately actionable for hardware procurement.
2.  **Gamma Unification:** The paper uses $\gamma_{30} = 0.745$ and $\gamma_{35} = 0.732$. Ensure that the text consistently uses the specific $\gamma$ associated with the rate being discussed, rather than a generic "0.76". The current draft is good at this, but a final sweep is recommended.
3.  **Visualizing the "Cliff":** In the discussion of the GE channel and ARQ, a small plot showing "Effective Throughput vs. Coherence Time $\tau_c$" would be very illuminating. It would visually demonstrate the regime where ARQ works vs. where it fails, reinforcing the text's argument about slow fading.