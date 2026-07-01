---
paper: "02-swarm-coordination-scaling"
version: "cv"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-03-05"
recommendation: "Unknown"
---

Here is a comprehensive peer review of the manuscript "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version CV).

---

# Peer Review Report

**Manuscript ID:** [Assigned by Editor]
**Title:** Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms
**Target Journal:** IEEE Transactions on Aerospace and Electronic Systems

## 1. Significance & Novelty
**Rating: 4 (Good)**
The paper addresses a critical gap in the literature: the specific dimensioning of coordination channels for mega-constellations ($10^4$--$10^5$ nodes). While routing and networking for such constellations are well-studied, the *control plane* sizing—specifically the interplay between hierarchical topology, byte-level budgets, and TDMA slot timing—is under-explored. The derivation of closed-form sizing equations that link physical layer constraints (CCSDS framing) to application layer requirements (campaign duty factors) is a significant contribution for system architects.

## 2. Methodological Soundness
**Rating: 4 (Good)**
The two-layer feasibility framework (byte budget + TDMA airtime) is logically sound. The transition from a simplified slot model (Model S) to a CCSDS-grounded model (Model C) adds necessary rigor. The use of a Gilbert-Elliott (GE) channel model is appropriate for capturing bursty losses, and the authors correctly identify it as a "what-if" design tool rather than empirical validation. The distinction between information rate and PHY rate is handled with necessary precision.

## 3. Validity & Logic
**Rating: 5 (Excellent)**
The internal logic is robust. The paper meticulously tracks overheads (framing, FEC, guard times) that are often glossed over in high-level swarm studies. The analysis of the "stress case" ($d=1$) vs. realistic campaigns ($d=0.10$) effectively resolves potential concerns about bandwidth feasibility. The identification of the ARQ $\times$ TDMA coupling—where intra-cycle retransmissions become structurally ineffective under slow-fading conditions—is a strong, logically derived finding.

## 4. Clarity & Structure
**Rating: 5 (Excellent)**
The manuscript is exceptionally well-structured. The distinction between "Model S" (simplified) and "Model C" (CCSDS) is made explicit early on, preventing confusion. Tables are information-dense but clear. The "Rate Ladder" (Table IV) is particularly helpful for guiding the reader through the sizing logic. The explicit "Validation Gap" section demonstrates high scientific integrity.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**
The authors provide a clear Data Availability statement with a repository link. The AI disclosure is specific and limits usage to ideation/editing, which complies with standard IEEE policies.

## 6. Scope & Referencing
**Rating: 4 (Good)**
The literature review covers relevant ground in swarm robotics, constellation networking, and delay-tolerant networking. The referencing of CCSDS standards (Proximity-1, TM Sync) is appropriate. The scope is correctly bounded to the coordination channel, explicitly excluding high-bandwidth optical payloads.

---

## Major Issues

1.  **Justification of the 1 kbps Constraint**
    *   **Issue:** The paper anchors heavily on a 1 kbps per-node information budget. While Section III-E attempts to justify this based on an S-band link budget ($E_b/N_0$ yielding ~200 kbps aggregate / 100 nodes), this feels like a circular constraint. If the system needs more bandwidth, a designer would simply allocate more power or spectrum, or reduce $k_c$.
    *   **Why it matters:** It treats a design variable as a hard physical constraint. Readers may dismiss the "stress case" warnings if they believe the 1 kbps limit is arbitrary.
    *   **Remedy:** Clarify that 1 kbps is a *baseline design target* for low-power, omni-directional coordination to preserve power for the primary payload, rather than a hard physical limit. Explicitly state that the equations scale linearly if this budget is increased (e.g., to 2 kbps).

2.  **Spatial Reuse ($R=3$) Plausibility**
    *   **Issue:** The paper assumes a spatial reuse factor of $R=3$ allows for fleet-wide scaling. In dense orbital shells (like Starlink or Kuiper), line-of-sight geometry and sidelobe interference might require a much more conservative reuse factor (e.g., $R=7$ or higher), significantly impacting the "Fleet Reuse" claims in Eq. 5.
    *   **Why it matters:** If $R=3$ is optimistic, the fleet-wide cycle time $T_c^{fleet}$ could double or triple, invalidating the scalability argument for $N=10^5$.
    *   **Remedy:** Add a sensitivity check or discussion paragraph acknowledging that $R$ is highly sensitive to orbital altitude and antenna beamwidth. Re-calculate the impact on $T_c^{fleet}$ if $R=7$ is required.

3.  **Thundering Herd on RF-Backup Recovery**
    *   **Issue:** The paper notes a "thundering herd" problem when 100 nodes attempt Raft election on the backup UHF link (Section III-B-2). The mitigation (Slotted ALOHA with BEB) is mentioned, but the convergence time (~160s) seems optimistic for a channel with only ~2.5 kbps capacity and high collision probability during the initial burst.
    *   **Why it matters:** This is the critical failure recovery mode. If recovery takes 10+ minutes, the swarm is effectively uncontrolled for a significant duration.
    *   **Remedy:** Provide a slightly more detailed justification for the 160s estimate. Did the simulation explicitly model the collision/backoff dynamics at the packet level for the UHF link, or is this an analytical approximation?

## Minor Issues

1.  **Table I (Notation):** The definition of $\gamma$ refers to "Eq. 2" but the generalized form is Eq. 10. Ensure equation references are consistent.
2.  **Figure 2 (Buffer CDF):** The caption mentions "Bernoulli $d=0.10$" and "ON/OFF $d=0.10$". Please clarify in the text if the "ON/OFF" model implies a Markovian arrival process, which is distinct from simple Bernoulli trials.
3.  **Section IV-J (Gamma Derivation):** The text states $\gamma$ decreases with PHY rate. While mathematically correct due to fixed overheads, it might be counter-intuitive to some readers. A brief sentence explicitly stating "Higher rates transmit payload faster, making fixed guard times a larger percentage of the slot" would improve readability for non-experts.
4.  **Algorithm 1:** In line 4, the formula for $T_{slot}$ is presented. It would be cleaner to reference Eq. 10 directly rather than rewriting the algebraic expansion, or ensure the notation is identical.

---

## Overall Recommendation
**Recommendation: Accept with Minor Revisions**

This is a high-quality, rigorous manuscript that makes a valuable contribution to the field of spacecraft swarm coordination. The authors have successfully addressed the complexities of cross-layer sizing (PHY to Application). The distinction between the simplified model and the CCSDS-grounded model is excellent, and the "Rate Ladder" provides clear, actionable guidance for practitioners.

The revisions requested are primarily regarding the contextualization of assumptions (specifically the 1 kbps budget and spatial reuse factor) rather than the fundamental mathematics or simulation architecture. Once these boundary conditions are softened or better justified, the paper will be ready for publication.

## Constructive Suggestions

1.  **Strengthen the "Design Tool" Aspect:** The paper excels when it positions the GE model and the sizing equations as tools for the reader. Highlight Algorithm 1 even more—perhaps by moving it earlier or referencing it in the Introduction—as the primary "product" of the paper.
2.  **Expand on FEC Choices:** The paper assumes LDPC 7/8. A brief sentence mentioning how the sizing changes if a mission requires stronger coding (e.g., Turbo 1/2 due to lower link margin) would add practical value.
3.  **Visualizing the "Cliff":** Figure 4 (Gamma vs. Rate) is good, but a plot showing "Margin vs. PHY Rate" might be more impactful. It would visually demonstrate the "cliff" at 24 kbps where margin becomes negative, reinforcing the infeasibility finding.