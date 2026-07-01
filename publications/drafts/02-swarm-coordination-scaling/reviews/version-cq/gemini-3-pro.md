---
paper: "02-swarm-coordination-scaling"
version: "cq"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-03-04"
recommendation: "Unknown"
---

Here is a comprehensive peer review of the manuscript **"Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version CQ)**, prepared for *IEEE Transactions on Aerospace and Electronic Systems*.

---

## 1. Significance & Novelty
**Rating: 4 (Good)**
The paper addresses a critical gap in the literature: the specific sizing of communication architectures for "mega-constellation" swarms ($10^3$--$10^5$ nodes). While high-level routing and formation flying control are well-studied, the "middle layer" of coordination protocol sizing—specifically byte-level accounting linked to TDMA constraints—is often glossed over. The derivation of the "two-layer" feasibility framework (byte budget + airtime) is a valuable contribution for systems engineers. The novelty lies not in new mathematical invention, but in the rigorous synthesis of queueing theory, CCSDS standards, and swarm dynamics to produce actionable design equations.

## 2. Methodological Soundness
**Rating: 4 (Good)**
The methodology is generally robust. The authors use a multi-tiered approach: analytical equations, a discrete event simulation (DES) for message flows, and a slot-level simulator for TDMA timing.
*   **Strengths:** The explicit derivation of $\gamma$ from CCSDS Proximity-1 framing (Model C) rather than relying on the simplified Model S is a significant improvement over typical conceptual papers. The separation of "information rate" from "PHY rate" is handled with necessary rigor.
*   **Weaknesses:** The reliance on assumed Gilbert-Elliott (GE) parameters ($p_{BG}=0.50$) without empirical ISL data is a limitation, though the authors transparently acknowledge this and provide sensitivity sweeps. The lack of NS-3 simulation to validate MAC contention assumptions (specifically the claim that contention is negligible at $\geq$10 kbps) is a minor gap, but acceptable given the focus on TDMA sizing.

## 3. Validity & Logic
**Rating: 5 (Excellent)**
The internal logic is tight. The paper meticulously distinguishes between "drops" (queue overflow) and "misses" (TDMA deadline violations). The identification of the ARQ$\times$TDMA coupling failure mode at 24 kbps is a strong logical deduction supported by the slot-level simulation. The argument for the 1 kbps "logical" budget within a 35 kbps physical channel is well-reasoned (sizing for the lowest common denominator failure mode). The transition from the "stress case" ($d=1$) to the "campaign duty factor" ($d \approx 0.1$) is logically sound and necessary for realistic sizing.

## 4. Clarity & Structure
**Rating: 5 (Excellent)**
The manuscript is exceptionally clear. The distinction between Model C (design) and Model S (comparison) is explicit. Tables are information-dense but readable. The "Rate Ladder" (Table IV) is a standout pedagogical device that clearly communicates the progression from theory to engineering recommendation. The notation is consistent, and the "Unmodeled Overhead Inventory" (Table VII) demonstrates high engineering rigor.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**
The authors provide a clear Data Availability statement pointing to a repository. The AI disclosure is specific and appropriate (ideation/editing only, not data generation). There are no apparent conflicts of interest or plagiarism concerns.

## 6. Scope & Referencing
**Rating: 4 (Good)**
The scope is well-suited for TAES. The referencing covers the necessary bases: classical queueing theory (Kleinrock), standard swarm literature (Dorigo, Brambilla), and relevant space standards (CCSDS, ECSS). The inclusion of recent mega-constellation literature (Handley, del Portillo) contextualizes the work well.

---

## Major Issues

1.  **Justification of Spatial Reuse ($R=3$) in S-band**
    *   **Issue:** The paper assumes a spatial reuse factor of $R=3$ allows for fleet-wide scaling (Section IV-E-1). However, S-band is omnidirectional or low-gain; achieving $>$20 dB isolation at only $10\times$ cluster diameter separation might be optimistic given sidelobes and the "near-far" problem in dynamic orbits.
    *   **Why it matters:** If $R=3$ is insufficient and $R$ must be 7 or higher, the "Fleet-Level Channel Reuse" argument weakens, potentially limiting the total fleet size supported by the available spectrum.
    *   **Remedy:** Add a brief calculation or citation justifying the path loss assumption ($L_{fs}$) vs. interference threshold ($I_{th}$) for the specific geometry. Explicitly state that this assumes specific antenna pattern discrimination or power control.

2.  **Sensitivity of Re-association Overhead to Orbital Geometry**
    *   **Issue:** Section V-C mentions that static cluster membership is assumed and claims re-association overhead is $<0.5\%$. This is valid for co-planar trains (Starlink-like) but potentially invalid for Walker-Delta constellations with crossing planes where relative velocities are high (${\sim}14$ km/s) and cluster dwell times are short.
    *   **Why it matters:** If the architecture is applied to a Walker constellation, the "handoff" traffic could dominate the "status" traffic, invalidating the byte budget.
    *   **Remedy:** Qualify the "static membership" claim in the Abstract and Introduction as "valid for co-planar or co-moving formations." In the Limitations section, explicitly note that high-relative-velocity constellations would require a dynamic graph analysis not covered here.

3.  **The "Thundering Herd" Risk in RF-Backup**
    *   **Issue:** Section III-B-2 mentions a "thundering herd" scenario where 100 nodes attempt Raft election on the UHF backup link. The text estimates 140-160s recovery.
    *   **Why it matters:** Slotted ALOHA collapses under high load ($G \gg 1$). If the back-off window ($W_{max}=64$) is too small for $N=100$, the channel could latch into a collision state, leading to indefinite loss of command and control.
    *   **Remedy:** Provide a quick calculation of the collision probability or throughput $S = G e^{-G}$ for the specific backoff parameters to prove the channel stabilizes. If $G$ remains $>1$, the 160s estimate is optimistic.

---

## Minor Issues

1.  **Table I (Notation):** The definition of $\alpha_{RX}$ is listed as "Ingress fraction... derived." It would be helpful to explicitly state $\alpha_{RX} \approx 0.9$ in the table for quick reference, as this value drives the egress bottleneck.
2.  **Section IV-A (Slot-level analysis):** The text states "margin = 614 ms" for Model S but later "margin = 730 ms" for Model C at 30 kbps. Clarify if the margin definitions differ or if this is purely due to the rate difference (24 vs 30 kbps).
3.  **Figure 4 (Buffer CDF):** The label "Bernoulli $d=0.10$" is slightly ambiguous. Does this mean a Bernoulli process per cycle? Clarify the legend text to "Bernoulli (i.i.d.)".
4.  **Equation 5 (Consensus):** The term $f_{decision}$ is defined as "decisions per cycle." Is this an integer? Can it be $<1$? Clarify if fractional decisions (amortized) are allowed.
5.  **Typos:**
    *   Section III-B-2: "triple fault... $1.8 \times 10^{-5}$/yr" - check the exponent, seems high for a triple fault if individual is 2%/yr.
    *   Section IV-J: "rate-1/2 doubles symbol time" - strictly speaking, it doubles the *number of symbols* for a fixed data size, or halves the data rate for fixed symbol rate. "Doubles transmission duration" might be clearer.

---

## Overall Recommendation
**Recommendation: Accept with Minor Revisions**

This is a high-quality, rigorous engineering paper that successfully bridges the gap between abstract swarm theory and concrete communication system sizing. The authors have effectively addressed the "workload realism" concern via the campaign duty factor ($d$) and have anchored their simulation results in CCSDS standards (Model C), removing the ambiguity of earlier simplified models.

The "two-layer" feasibility framework is a useful tool for the community. The paper's frank admission of the lack of external validation (Tier 3) and the clear delineation of what is modeled vs. what is assumed (e.g., the GE parameters) demonstrates high scientific integrity.

The requested revisions (Major Issues) are primarily regarding boundary conditions (spatial reuse, orbital geometry) and do not require re-running the core simulations. Addressing these will ensure the paper's conclusions are properly bounded for practitioners.

---

## Constructive Suggestions

1.  **Enhance the "Rate Ladder" (Table IV):** This is the strongest takeaway for practitioners. Consider adding a column for "Limiting Factor" (e.g., "Byte Budget," "Slot Timing," "ARQ Margin") to show *why* the rate jumps at each step.
2.  **Generalized Gamma Lookup:** The $\gamma$-conditional lookup in Section V-D is excellent. Consider presenting this as a small subplot or a dedicated lookup table (e.g., "If your link is X, use Y") to make it even more accessible.
3.  **Explicit Warning on UHF:** The suspension of hierarchy during RF-backup is a critical operational detail. Emphasize in the Conclusion that the "1 kbps budget" does *not* apply to the UHF link (which is beacon-only), to prevent readers from sizing their backup links incorrectly.
4.  **Future Work - Optical:** You mention Optical ISL is used for bulk data. A brief sentence in the discussion about how the control plane might migrate to Optical (if pointing allows) would be interesting, as it would render the S-band constraints moot.