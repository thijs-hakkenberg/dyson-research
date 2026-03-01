---
paper: "02-swarm-coordination-scaling"
version: "cf"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-03-01"
recommendation: "Unknown"
---

Here is a comprehensive peer review of the manuscript **"Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version CF)**.

---

# Peer Review Report

**Journal:** IEEE Transactions on Aerospace and Electronic Systems
**Manuscript ID:** [Assigned by Editor]
**Title:** Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms
**Version:** CF

## 1. Significance & Novelty
**Rating: 5 (Excellent)**
The manuscript addresses a critical gap in the literature: the lack of closed-form sizing relationships for spacecraft swarms in the $10^4$--$10^5$ node regime. While swarm robotics and mega-constellation routing are well-studied in isolation, the intersection—specifically the byte-level accounting of hierarchical coordination under strict bandwidth constraints—is novel. The derivation of a "two-layer feasibility framework" (byte budget vs. airtime schedulability) provides a valuable tool for systems engineers. The distinction between the 1 kbps RF-backup constraint and optical ISL capacity is a significant practical contribution, grounding the theoretical work in realistic failure modes.

## 2. Methodological Soundness
**Rating: 5 (Excellent)**
The methodology is rigorous and multi-faceted. The authors employ a "three-tier" verification strategy (analytical, message-level DES, and slot-level TDMA simulation) that is highly effective. The explicit derivation of the MAC efficiency parameter ($\gamma$) from CCSDS standards (Section IV-J) is a major improvement over previous iterations that might have assumed arbitrary efficiencies. The use of Gilbert-Elliott (GE) models to stress-test the TDMA schedule against correlated losses adds necessary depth. The distinction between "fluid" queueing models and discrete slot-level constraints is handled with exceptional clarity.

## 3. Validity & Logic
**Rating: 5 (Excellent)**
The internal logic is consistent. The paper successfully argues that while byte-level budgets might appear feasible at 24 kbps, the half-duplex turnaround and guard times (Layer 2) render that rate insufficient when using standard framing. The handling of the "stress case" ($d=1$) vs. "routine operations" ($d \approx 0.01$) is logically sound and prevents the paper from over-dimensioning the system based on rare events. The argument for the 1 kbps backup channel based on link budgets (Table IV) is physically justified.

## 4. Clarity & Structure
**Rating: 5 (Excellent)**
The manuscript is written with high precision. The notation is consistent, and the distinction between different types of overhead ($\eta_0$ vs. $\eta_{\text{cmd}}$) is maintained throughout. Figures are well-captioned and directly support the text. The inclusion of an algorithmic summary (Algorithm 1) is a helpful addition for practitioners. The "Claim Map" (Table XIV) is an excellent structural device that transparently links claims to their specific evidence tier.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**
The authors provide a clear Data Availability statement pointing to a repository with source code and datasets. The acknowledgment section transparently discloses the use of AI for ideation, adhering to emerging best practices for AI disclosure in scientific publishing.

## 6. Scope & Referencing
**Rating: 4 (Good)**
The literature review covers the necessary bases (swarm robotics, constellation management, delay-tolerant networking). The references to CCSDS standards are particularly strong. However, the paper could benefit from slightly more engagement with recent work on distributed optimization in satellite networks (e.g., ADMM-based approaches) to further contextualize why the hierarchical approach was chosen over purely distributed optimization, even if the latter is bandwidth-prohibitive.

## 7. Theoretical Depth
**Rating: 4 (Good)**
The queueing theoretic models ($M/D/1$, $D/D/1$ batch) are standard but applied correctly. The derivation of the unicast stagger cycles ($L_{\text{cmd}}$) and the fleet reuse factors are solid theoretical contributions. The GE analysis is robust.

## 8. Simulation Rigor
**Rating: 5 (Excellent)**
The simulation campaign is extensive ($N=10^5$, 30 MC replications). The use of bootstrap confidence intervals and the explicit separation of message-level DES from slot-level schedulability simulation demonstrates a sophisticated understanding of simulation architecture. The sensitivity sweeps (Figures 8, 10, 12) cover the design space well.

## 9. Practical Relevance
**Rating: 5 (Excellent)**
This is the paper's strongest point. It moves beyond abstract algorithms to provide concrete engineering values: 30 kbps minimum PHY rate, 440s AoI for safe mode, and specific buffer sizing for correlated outages. The link budget analysis for the UHF backup mode is directly applicable to CubeSat and small-sat constellation designers.

## 10. Overall Quality
**Rating: 5 (Excellent)**
This is a high-quality manuscript that makes a definitive contribution to the field of large-scale space systems engineering. It balances theoretical derivation with practical constraints (CCSDS framing, half-duplex radios) effectively.

---

## Major Issues
*None.* The manuscript is exceptionally polished. The rigorous cross-verification between the analytical model, DES, and slot-level simulator resolves potential concerns regarding the validity of the sizing equations.

## Minor Issues

1.  **Clarification on "Antenna Acquisition":** In Table X ($\gamma$ decomposition), "Acquisition" is listed as a 5 ms dwell with an efficiency factor. It would be beneficial to briefly clarify if this assumes a specific beamwidth or if this is a worst-case slew-and-settle time for an electronically steered array vs. a mechanical system. The text mentions "pointing dwell," but a sentence on the assumed hardware class (e.g., patch array vs. helical) would strengthen the justification for the 5 ms value.
2.  **Section IV-E (Campaign Duty Factor):** The text states "The Bernoulli model is exact for mean $\eta$ and optimistic for peak buffer occupancy." While true, it might be worth explicitly stating *why* it is optimistic (it ignores the autocorrelation of traffic bursts which fills buffers). The reference to Figure 9 covers this, but a direct sentence in the text would improve flow.
3.  **Table VIII (AoI Operational Mapping):** The row "Formation keeping" lists "Optical ISL" as the channel. It might be worth adding a footnote or brief mention that this assumes the ISL topology matches the formation topology, or that multi-hop latency over ISL is negligible for this control loop.
4.  **Typos/Formatting:**
    *   Table I: "$\gamma_{30} = 0.745$" is cited, but later text sometimes rounds this. Ensure consistency in significant figures throughout.
    *   References: Ensure all URL access dates are consistent (some say "accessed Feb 2026").

## Overall Recommendation
**Recommendation: Accept**

This manuscript represents a significant advancement in the systems engineering of large-scale autonomous constellations. The authors have successfully derived and validated a sizing framework that bridges the gap between high-level swarm algorithms and low-level physical layer constraints.

The paper is particularly strong in its "two-layer" approach, demonstrating that a byte-level budget is insufficient without a rigorous check of TDMA airtime schedulability. The inclusion of CCSDS-grounded overheads and Gilbert-Elliott loss models moves the work from theoretical abstraction to engineering reality. The validation strategy—triangulating between closed-form math, discrete event simulation, and slot-level simulation—is exemplary.

The manuscript is ready for publication. The minor issues noted above are suggestions for polish rather than requirements for validity.

## Constructive Suggestions

1.  **Enhance the GE Parameter Discussion:** In Section IV-C, you provide a sensitivity sweep for $p_{BG}$. It would be valuable to add a sentence explicitly linking $p_{BG}$ to physical orbital parameters. For example, "A $p_{BG}$ of 0.10 corresponds to a blockage duration of approx. 10 cycles (100s), which is characteristic of a slow rotation or specific orbital harmonic." This helps practitioners pick the right point on the curve.
2.  **Future Work - NS-3:** You correctly identify the lack of NS-3 simulation as a limitation. In the discussion, you might briefly hypothesize what you expect NS-3 to reveal. For example, "We anticipate NS-3 simulations will reveal non-linear latency growth at the boundaries of cluster handover regions due to contention, which our static topology model does not capture."
3.  **Algorithm 1 Refinement:** In Algorithm 1, Step 12 ($T_{\text{egress}}$), you sum $T_{\text{cmd}}$, $T_{\text{hb}}$, and $T_{\text{sync}}$. It might be helpful to explicitly note in the algorithm comment that $T_{\text{cmd}}$ here refers to the *broadcast* duration (Type 1), as Type 2 requires the stagger check in Step 17. This prevents confusion for a reader implementing the algorithm blindly.