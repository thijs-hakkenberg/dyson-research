---
paper: "02-swarm-coordination-scaling"
version: "dk"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-03-06"
recommendation: "Unknown"
---

Here is a comprehensive peer review of the manuscript (Version DK), structured for *IEEE Transactions on Aerospace and Electronic Systems*.

---

# Peer Review: Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms

## 1. Significance & Novelty
**Rating: 4 (Good)**
The paper addresses a critical gap in the literature: the specific dimensioning of communication resources for large-scale ($N=10^5$) autonomous satellite swarms. While high-level architectural papers exist, this work provides concrete, closed-form sizing equations that link byte-level protocol accounting with physical layer (PHY) timing constraints. The derivation of the "two-test" feasibility framework (Test A: Byte Budget, Test B: TDMA Airtime) is a valuable contribution for systems engineers. The novelty lies in the rigorous integration of CCSDS Proximity-1 framing overheads into the swarm coordination problem, moving beyond the abstract graph-theory models often seen in this domain.

## 2. Methodological Soundness
**Rating: 4 (Good)**
The methodology is generally robust. The authors employ a multi-fidelity approach: analytical derivation, cycle-aggregated discrete event simulation (DES), and a slot-level TDMA simulator.
*   **Strengths:** The explicit modeling of CCSDS framing overheads (leading to $\gamma \approx 0.73-0.76$) significantly improves realism over "ideal" channel models. The distinction between information rate and PHY rate is handled with necessary rigor.
*   **Weaknesses:** The reliance on a Gilbert-Elliott (GE) model without empirical validation from actual inter-satellite link (ISL) data is a limitation, though the authors transparently acknowledge this as a "what-if" tool. The assumption of static cluster membership for the DES is a simplification, but the justification regarding orbital dynamics (co-planar vs. cross-plane) is acceptable for a sizing paper.

## 3. Validity & Logic
**Rating: 5 (Excellent)**
The internal logic is tight. The paper meticulously tracks the interaction between protocol layers. The transition from the earlier version's generic $\gamma=0.85$ to the CCSDS-derived $\gamma \approx 0.76$ strengthens the validity of the results. The argument that intra-cycle ARQ is ineffective under slow-fading conditions ($\tau_c \ge T_c$) is logically sound and mathematically supported. The decoupling of Test A and Test B at low duty cycles is well-argued.

## 4. Clarity & Structure
**Rating: 5 (Excellent)**
The manuscript is exceptionally well-structured. The "Rate Ladder" (Table IV) and the "Feasibility Test" algorithm (Algorithm 1) are standout features that make the complex interdependencies accessible. The distinction between "Model S" (simplified) and "Model C" (CCSDS) is maintained clearly throughout, preventing confusion about which parameters drive the design recommendations.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**
The authors provide a clear Data Availability statement with a repository link. The acknowledgment of AI assistance in ideation/editing is transparent and complies with emerging IEEE policies.

## 6. Scope & Referencing
**Rating: 4 (Good)**
The scope is appropriate for TAES. The referencing covers the necessary bases: swarm robotics theory, standard queuing theory, and relevant CCSDS/ETSI standards.
*   **Gap:** While *Starlink* and *Kuiper* are mentioned, the paper could benefit from slightly more engagement with recent literature on "Mega-Constellation" routing protocols (e.g., recent works in *IEEE/ACM Transactions on Networking* regarding ISL topology dynamics) to better contextualize why the static cluster assumption holds for specific shell geometries.

---

## Major Issues

1.  **Contextualization of the "Stress Case" ($\eta \approx 46\%$):**
    *   **Issue:** While the abstract and introduction mention that the 46% overhead is a "continuous-duty upper bound," the results section (specifically IV.E) risks giving the impression that this is a typical operating state. If a reader skims, they might conclude the protocol is inefficient.
    *   **Why it matters:** High overhead might scare off practitioners looking for lightweight protocols. The distinction between *provisioning* for the stress case (buffer sizing) and *operating* in the stress case (thermal/power) needs to be sharper.
    *   **Remedy:** In Section IV.E, explicitly state that while the *link* must be dimensioned for the stress case to avoid collapse, the *power budget* can likely be dimensioned for the routine case ($d=0.10$). Add a sentence clarifying that sustaining $d=1.0$ for long durations would likely violate thermal constraints before bandwidth constraints on a CubeSat.

2.  **Sensitivity to Acquisition Time ($T_{acq}$):**
    *   **Issue:** The recommendation of 35 kbps relies heavily on the margin analysis. The paper assumes $T_{acq} = 5$ ms (cold start). However, if the radio hardware is lower-end (common in CubeSats), acquisition could take 10-20 ms.
    *   **Why it matters:** If $T_{acq}$ doubles to 10 ms, the slot efficiency $\gamma$ drops significantly, potentially rendering 35 kbps insufficient.
    *   **Remedy:** Expand the sensitivity analysis in Section IV.J or add a row to Table VIII (Gamma-Conditional PHY Rate Lookup) specifically addressing "Slow Acquisition Hardware" (e.g., $T_{acq} > 10$ ms). Provide a specific $R_{PHY}$ recommendation for this sub-case (likely ~40-50 kbps).

3.  **The "Logical" vs. "Physical" 1 kbps Budget:**
    *   **Issue:** The concept of a "1 kbps per-node budget" is central, but the text sometimes conflates this with a physical link limit.
    *   **Why it matters:** Readers might confuse the *allocation* (policy) with the *capacity* (physics).
    *   **Remedy:** In Section III.E ("Communication Overhead Definition"), reinforce the statement: "1 kbps is a traffic policing policy enforced by the scheduler, not a hardware limit of the radio." This ensures the reader understands that the 35 kbps PHY rate is required to service the *aggregate* of these 1 kbps policies.

## Minor Issues

1.  **Table I (Notation):** The definition of $\alpha_{RX}$ is listed as a "Computed output." It would be helpful to explicitly state here that it includes the guard times and acquisition overheads, just to be precise.
2.  **Section IV.A (TDMA Frame Model):** The text mentions "TCXO drift 0.6 ms << 4.7 ms." Please clarify the duration over which this drift accumulates. Is it per slot? Per cycle? (Presumably per cycle/superframe, but explicit is better).
3.  **Figure 3 (Buffer CDF):** The caption mentions "Buffer factor M = 1.30". Please clarify in the text if this factor is applied to the mean or the P99 value.
4.  **Equation 6 (Consensus):** The variable $f_{decision}$ is defined as "decisions per cycle." It might be clearer to define it as "consensus rounds initiated per cycle."
5.  **Typos:**
    *   Section IV.H: "margin > 90%---both tests trivially satisfied." (Check if em-dash spacing is correct per IEEE style).
    *   References: Ensure all "ArXiv" preprints are updated to their final publication venue if available.

## Overall Recommendation
**Recommendation: Accept with Minor Revisions**

This is a high-quality manuscript that provides much-needed engineering rigor to the problem of satellite swarm coordination. The authors have successfully moved beyond abstract graph theory to provide actionable design equations rooted in CCSDS standards.

The "Two-Test" framework is a strong contribution. The revision from previous versions (unifying the $\gamma$ parameter) has resolved prior methodological concerns. The paper is honest about its limitations (lack of external validation) and provides tools (sensitivity curves) rather than just point solutions.

The requested revisions focus on sharpening the interpretation of the "stress case" to prevent misinterpretation of the protocol's efficiency, and expanding the sensitivity analysis regarding radio acquisition times to ensure the sizing equations hold for lower-cost hardware.

## Constructive Suggestions

1.  **Impact:** Add a "Practitioner's Summary" or a "Design Procedure" text box (distinct from Algorithm 1) that lists the 5 steps a systems engineer should take to size their radio. (1. Determine $k_c$, 2. Estimate $T_{acq}$, 3. Calculate $\gamma$, 4. Run Test B, 5. Add 20% margin).
2.  **Visualization:** Figure 4 (Gamma vs. Rate) is excellent. Consider annotating it with a "Forbidden Region" shaded in red where $T_{slot} > T_{c}/k_c$, making the visualization of the feasibility cliff immediate.
3.  **Future Work:** Explicitly suggest that future work should investigate "dynamic TDMA" where slot sizes change based on the specific message type (e.g., short slots for heartbeats, long slots for commands), rather than the fixed-slot assumption used here.