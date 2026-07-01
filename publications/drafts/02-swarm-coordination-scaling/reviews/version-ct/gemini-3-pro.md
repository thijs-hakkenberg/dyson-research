---
paper: "02-swarm-coordination-scaling"
version: "ct"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-03-04"
recommendation: "Unknown"
---

Here is a rigorous peer review of the manuscript **"Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version CT)**, prepared for *IEEE Transactions on Aerospace and Electronic Systems*.

---

## 1. Significance & Novelty
**Rating: 4 (Good)**
The paper addresses a critical gap in the literature: the lack of closed-form sizing relationships for "mega-constellation" scale coordination. While high-level architectural concepts exist (e.g., centralized vs. distributed), this work provides specific, byte-level accounting and PHY-layer timing analysis that is valuable for systems engineers. The novelty lies in the integration of a campaign duty factor ($d$) with a two-layer feasibility framework (byte budget + TDMA airtime), moving beyond generic "throughput" metrics to specific operational constraints.

## 2. Methodological Soundness
**Rating: 4 (Good)**
The methodology is generally robust. The decomposition into Layer 1 (information rate) and Layer 2 (TDMA airtime) is logical. The use of a Gilbert-Elliott (GE) model to stress-test the TDMA schedule is appropriate, and the distinction between intra-cycle and inter-cycle recovery is a strong analytical contribution. The derivation of $\gamma$ from CCSDS Proximity-1 standards adds necessary realism. However, the reliance on a "fluid-server" approximation in the DES for some queueing metrics, while checked against a slot-level simulator, requires careful interpretation regarding jitter.

## 3. Validity & Logic
**Rating: 5 (Excellent)**
The internal logic is tight. The authors have rigorously addressed previous concerns regarding the "stress case" by introducing the campaign duty factor ($d$), correctly identifying that continuous stress is an invalid design point. The coupling analysis between ARQ and TDMA (Table V) is a highlight, demonstrating that 24 kbps is infeasible not just due to bandwidth, but due to slot-timing constraints when retransmissions are added. The distinction between Model S (simplified) and Model C (CCSDS) is clearly maintained, preventing misleading conclusions.

## 4. Clarity & Structure
**Rating: 5 (Excellent)**
The manuscript is exceptionally well-structured. The "Rate Ladder" (Table III) and the "Feasibility Test" (Algorithm 1) are high-value artifacts for practitioners. The notation is consistent, and the distinction between information rate and PHY rate is handled with unusual precision. The "Validation Gap" section is refreshingly honest.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**
The authors provide a clear Data Availability statement with a GitHub link (simulators, code). The AI disclosure is specific (ideation/editing only, not data generation), adhering to current IEEE guidelines.

## 6. Scope & Referencing
**Rating: 4 (Good)**
The referencing is adequate, covering standard texts (Wertz, Kleinrock) and relevant CCSDS standards. The connection to recent distributed systems literature (Raft, Gossip) is good. The scope is correctly bounded to the "coordination channel" (S-band), explicitly excluding high-speed optical payloads, which clarifies the contribution.

---

## Major Issues

1.  **Fleet-Level Spatial Reuse Validation (Section IV-A.1 / V-C)**
    *   **Issue:** The paper asserts a spatial reuse factor of $R=3$ allows scaling to $10^5$ nodes based on an "order-of-magnitude estimate."
    *   **Why it matters:** If $R=3$ is optimistic (e.g., due to sidelobe interference in dense shells), the fleet-level capacity collapses, invalidating the "Large Swarm" claim in the title. Standard cellular reuse is often $R=7$.
    *   **Remedy:** While full NS-3 simulation is out of scope (as noted), the authors should provide a brief geometric justification or link budget calculation (C/I ratio) in the appendix or text to support $R=3$ vs. $R=7$. Alternatively, explicitly calculate the impact if $R=7$ is required (presumably just reducing the duty cycle or requiring more frequency channels).

2.  **Unicast Command Latency Context (Eq. 7)**
    *   **Issue:** The derivation shows a 19-cycle stagger ($L_{cmd} \approx 190$s) for unicast commands at $q=1$.
    *   **Why it matters:** This is a very high latency for "coordination." While the text mentions this is for "orchestration," it risks confusing readers who expect "swarm coordination" to imply tight formation flying.
    *   **Remedy:** Explicitly state in the abstract or introduction that this architecture supports *loose* coordination (tasking, orbit maintenance) and is *insufficient* for tight, closed-loop formation control (which requires the optical ISL). The current disclaimer in Section IV-A.1 is buried too deep.

3.  **Sensitivity to Oscillator Drift in "Guard" Time**
    *   **Issue:** The guard time is fixed at 4.7 ms. The text mentions TCXO holdover, but does not explicitly link the guard time budget to the specific oscillator stability (ppm) and resynchronization interval.
    *   **Why it matters:** For low-cost swarms (CubeSats), oscillators may drift faster than modeled. If the guard is violated, the TDMA scheme fails catastrophically (collisions).
    *   **Remedy:** Add a brief calculation: $\Delta t = \text{drift}_{ppm} \times T_{sync}$. Confirm that 4.7 ms covers the drift over the synchronization interval for a standard commercial TCXO.

---

## Minor Issues

1.  **Table I (Notation):** The definition of $\eta$ includes $\eta_{cmd}$, but the text later defines $\eta_{total}$ as including the baseline. Ensure the distinction between "protocol overhead" and "total channel utilization" is rigorous throughout all figure captions.
2.  **Figure 4 (Buffer CDF):** The label "Bernoulli d=0.10" is slightly ambiguous. Clarify if this is "Independent Bernoulli" vs. "Correlated/Burst Bernoulli."
3.  **Section IV-J (Gamma):** The text states "DVB-RCS2 terminals... achieve 0.70-0.85." Please clarify if this is a measured throughput efficiency or a slot structure efficiency. The comparison is useful but needs precise terminology.
4.  **Algorithm 1, Line 12:** "Intra-cycle ARQ infeasible." It might be helpful to add "Fallback to Inter-cycle ARQ" to the output or state explicitly that the system is still functional, just with higher latency.
5.  **Typos:** Check Eq. 5 (Fleet reuse) for consistency with the definition of $G$.

---

## Overall Recommendation
**Recommendation: Accept with Minor Revisions**

This is a high-quality, rigorous paper that makes a tangible contribution to the systems engineering of large-scale satellite constellations. The authors have successfully moved beyond generic networking simulations to provide actionable sizing equations grounded in CCSDS standards and realistic timing constraints.

The introduction of the **Campaign Duty Factor ($d$)** and the **Gamma ($\gamma$) unification** resolves the primary weaknesses of earlier drafts. The distinction between the byte-budget feasibility (Layer 1) and the TDMA airtime feasibility (Layer 2) is a strong pedagogical and practical tool.

The revisions requested are primarily regarding context (clarifying the "loose" nature of the coordination and justifying the spatial reuse assumption) rather than the core mathematical derivation, which appears sound.

---

## Constructive Suggestions

1.  **Enhance the "Rate Ladder" (Table III):** Consider adding a column for "Link Margin (dB)" at each step, assuming a reference radio (e.g., 1W S-band). This would visually demonstrate the trade-off between rate and robustness.
2.  **Operational Vignette:** A short paragraph describing a "Day in the Life" of the coordinator buffer—showing it filling during a campaign and draining during routine ops—would make the abstract $d$ parameter more concrete for readers.
3.  **Future Work - Asynchronous Access:** Briefly mention if Slotted ALOHA is a viable fallback for the *entire* system if the coordinator fails, or if the system goes silent. (The text mentions "safe-hold beacon," but could data be passed?)