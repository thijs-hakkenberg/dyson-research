---
paper: "02-swarm-coordination-scaling"
version: "ca"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-28"
recommendation: "Accept with Minor Revisions"
---

Here is a rigorous peer review of the manuscript **"Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version CA)**, prepared for *IEEE Transactions on Aerospace and Electronic Systems*.

---

## 1. Significance & Novelty
**Rating: 5 (Excellent)**
The paper addresses a critical gap in the literature: the lack of closed-form sizing relationships for spacecraft swarms in the $10^3$--$10^5$ node regime. While mega-constellation routing is well-studied, the specific problem of *command and control* (C2) coordination under strict bandwidth constraints (1 kbps RF backup) is novel. The distinction between "byte budget" feasibility and "TDMA airtime" feasibility is a significant contribution that prevents the common error of assuming channel capacity equals throughput in half-duplex systems.

## 2. Methodological Soundness
**Rating: 5 (Excellent)**
The multi-tiered verification approach is robust. The authors successfully employ:
1.  **Analytical derivation:** Closed-form equations for overhead and capacity.
2.  **Cycle-aggregated DES:** For fleet-wide statistics and logical verification.
3.  **Slot-level TDMA simulation:** To capture timing violations and ARQ interactions that the DES misses.
4.  **Packet-level validation:** To derive the MAC efficiency parameter ($\gamma$) from CCSDS standards rather than assuming it.
This "ladder of abstraction" is highly effective. The use of the Gilbert-Elliott model for correlated losses is appropriate for the LEO environment.

## 3. Validity & Logic
**Rating: 4 (Good)**
The internal logic is generally sound. The derivation of $\gamma = 0.76$ from CCSDS Proximity-1 framing is a strong anchor point. The argument regarding the infeasibility of intra-cycle ARQ under slow-mixing fading is mathematically convincing.
*Critique:* The treatment of the "sectorized mesh" baseline is slightly defensive. While the authors correctly identify it as having a different functional scope, the comparison in Figure 11 feels like comparing apples to oranges. However, the text acknowledges this limitation explicitly, preserving validity.

## 4. Clarity & Structure
**Rating: 5 (Excellent)**
The manuscript is exceptionally well-structured. The progression from simple sizing to complex TDMA interactions is logical. Tables are dense but informative (particularly Table VII on workload feasibility). The distinction between "Nominal," "Event," and "Stress" profiles is clear. The notation is consistent.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**
The authors provide a clear Data Availability statement with a GitHub link. The acknowledgment of AI assistance in the ideation phase is transparent and consistent with emerging IEEE guidelines.

## 6. Scope & Referencing
**Rating: 4 (Good)**
The literature review covers swarm robotics, constellation management, and networking well. The inclusion of CCSDS standards (Proximity-1, TM Sync) grounds the work in reality.
*Critique:* The paper could benefit from slightly more engagement with recent work on "mega-constellation" distributed consensus (e.g., recent papers on Byzantine Fault Tolerance in space), though the focus here is rightly on the transport/sizing layer rather than the consensus algorithm itself.

---

## Major Issues

1.  **Contextualization of the Stress Case ($\eta \approx 46\%$)**
    *   **Issue:** The abstract and conclusion highlight the stress-case overhead ($\eta \approx 46\%$) prominently. While the text explains this assumes continuous command injection ($d=1$), a casual reader might interpret this as the steady-state cost of hierarchy.
    *   **Why it matters:** It risks making the hierarchical architecture appear inefficient compared to mesh approaches, when in reality, routine operations yield $\eta \approx 5\%$.
    *   **Remedy:** In the Abstract and Conclusion, explicitly pair the 46% figure with the "routine" figure (5%) in the same sentence. For example: *"Protocol overhead ranges from ~5% during routine operations to a bounded 46% during continuous fleet-wide reconfiguration."*

2.  **RF-Backup Link Budget Margin**
    *   **Issue:** Table IV shows the RF-backup mode has an $E_b/N_0$ of 16.5 dB at 1 kbps, but fails at 24 kbps. However, the coordinator ingress requirement is $\approx 27$ kbps. This implies the coordinator *cannot* operate on the RF backup link using the same omnidirectional hardware as the nodes, or it requires a different modulation scheme not detailed.
    *   **Why it matters:** The paper argues that 1 kbps is the "design-driving" constraint for nodes, but the coordinator needs 30 kbps. If the coordinator loses its optical ISL and falls back to RF, can it sustain the 30 kbps ingress required for the hierarchy? If not, the hierarchy collapses during the very emergency state it is designed for.
    *   **Remedy:** Clarify the coordinator's RF capabilities. Does the coordinator have a higher-gain antenna? Or does the hierarchy revert to a "safe mode" with reduced reporting rates ($p_{exc} \ll 1.0$) when on RF backup to fit the lower aggregate capacity? Section IV-A mentions a 30 kbps design point, but Table IV suggests this is impossible at 1000 km with omni antennas.

3.  **Fleet-Level Reuse and Interference**
    *   **Issue:** Section IV-A-2 discusses fleet reuse ($f_{RF}$) and spatial reuse ($R$). It assumes clusters can be treated independently if $f_{RF}$ is low. However, in a dense shell (Starlink-like), physical proximity might force $R$ to be much higher than 3 to avoid co-channel interference, especially with omnidirectional UHF.
    *   **Why it matters:** If $R$ needs to be 7 or 12 (typical cellular reuse patterns) rather than 3, the "non-binding" threshold for $f_{RF}$ drops significantly, potentially making the RF backup channel congested during a fleet-wide event (e.g., a solar storm triggering safe mode for everyone).
    *   **Remedy:** Add a brief sensitivity analysis or qualitative discussion on how a higher reuse factor ($R$) impacts the "safe mode" latency. Acknowledge that a fleet-wide safe mode might require significantly relaxed $T_c$ (e.g., 60s instead of 10s).

---

## Minor Issues

1.  **Table I (Notation):** The definition of $\eta$ is given as "Protocol overhead... beyond baseline." It would be helpful to explicitly state $\eta = B_{protocol}/C_{node}$ to clarify it is a dimensionless ratio.
2.  **Section IV-A (TDMA Frame):** The derivation of $\gamma = 0.949$ vs. $\gamma = 0.76$ is excellent. However, the text mentions "ranging/calibration" as part of the margin. Is there a specific slot allocated for ranging, or is it assumed to happen in the guard times? A brief clarification would help.
3.  **Figure 5 (Unicast Stagger):** The caption mentions "slot-level simulation validation (crosses)." Ensure the crosses are clearly visible and distinct from the line in the final print version.
4.  **Equation 10 (Gamma General):** The term $1000$ in the denominator presumably converts ms to seconds. It would be cleaner to define $T_{guard}$ in seconds or make the unit conversion explicit in the text.
5.  **Typos:**
    *   Section III-B-2: "Nominal handoff: 3--5 s... RF-backup handoff: ~160 s." Ensure the distinction between "handoff duration" and "service interruption time" is clear.
    *   Table VIII: "Power Var." is listed as "CV". Define CV (Coefficient of Variation) in the footnote if not already defined.

---

## Overall Recommendation
**Recommendation: Accept with Minor Revisions**

This is a high-quality manuscript that provides a definitive reference for sizing hierarchical coordination networks in large space swarms. The authors have done an impressive job of moving from high-level byte counting to low-level physical layer constraints (CCSDS framing, GE losses, half-duplex turnarounds).

The distinction between the three feasibility layers (Byte, MAC, Airtime) is a valuable pedagogical contribution to the systems engineering community. The validation of $\gamma=0.76$ adds significant rigor.

The only substantive gap is the reconciliation of the Coordinator's RF bandwidth requirements (30 kbps) with the RF link budget presented in Table IV (which maxes out at ~2.5 kbps for omni-omni links). Addressing how the coordinator closes the link at 30 kbps (or how the protocol adapts if it can't) is the only major hurdle to publication.

---

## Constructive Suggestions

1.  **Resolve the Coordinator RF Link Budget:** (Highest Priority)
    *   If the coordinator uses the same RF hardware as nodes (omni/0.1W), it cannot support 30 kbps ingress.
    *   *Suggestion:* Explicitly state that under RF backup, the system *must* switch to "Exception-Only" reporting ($p_{exc} \approx 0.1$) or "Summary-Only" mode to reduce aggregate ingress to <2.5 kbps. Alternatively, specify that coordinators require high-gain directional UHF antennas (which adds pointing complexity). The current text implies the 30 kbps requirement persists even in RF backup, which contradicts Table IV.

2.  **Refine the "Stress Case" Narrative:**
    *   The 46% overhead figure is a useful bound but a scary number for a system designer. Emphasize the "Campaign Duty Factor" ($d$) earlier in the abstract. The system is viable because $d$ is typically low.

3.  **Expand on "Safe Mode" Concurrency:**
    *   In Section IV-A-2, you discuss $f_{RF}$. Explicitly link this to the "Coordinator RF Link Budget" issue. If the whole fleet goes to RF backup (e.g., a solar event disrupts optical tracking), the interference environment changes. A brief acknowledgment that $T_c$ might need to scale to minutes in a "Global Safe Mode" would add operational realism.

4.  **Visualizing the Feasibility Layers:**
    *   Consider adding a small graphical abstract or flow chart showing the "Three-Layer Feasibility" filter (Byte $\to$ MAC $\to$ Airtime). This would be very citation-friendly.