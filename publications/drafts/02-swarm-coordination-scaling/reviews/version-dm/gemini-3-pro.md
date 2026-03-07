---
paper: "02-swarm-coordination-scaling"
version: "dm"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-03-07"
recommendation: "Unknown"
---

Here is a comprehensive peer review of the manuscript **"Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version DM)**.

---

## 1. Significance & Novelty
**Rating: 4 (Good)**
The paper addresses a critical gap in the literature: the specific dimensioning of coordination channels for mega-constellations and large swarms ($10^3$--$10^5$ nodes). While high-speed optical ISLs are well-studied, the "control plane" sizing—specifically the low-rate, high-reliability RF backup or coordination channel—is often hand-waved. The derivation of closed-form sizing equations (Test A/Test B framework) is a valuable contribution for systems engineers. The novelty lies not in the invention of new protocols, but in the rigorous application of existing standards (CCSDS) to the specific constraints of hierarchical swarm control.

## 2. Methodological Soundness
**Rating: 5 (Excellent)**
The methodology is robust. The authors have moved beyond simple throughput calculations to a detailed frame-level timing analysis. The inclusion of an independent NS-3 validation (Section IV-J) significantly strengthens the paper, addressing previous concerns about circular validation where the simulation merely implements the analytical equations. The use of the Gilbert-Elliott (GE) model as a "what-if" design tool rather than a predictive propagation model is appropriate for this stage of design. The distinction between information rate, PHY rate, and slot efficiency ($\gamma$) is handled with high precision.

## 3. Validity & Logic
**Rating: 5 (Excellent)**
The internal logic is consistent. The transition from a byte-level budget (Test A) to a time-domain schedule (Test B) is seamless. The handling of the "stress case" ($d=1$) vs. nominal operations is now logically sound, preventing the over-design that would occur if the system were sized purely for continuous worst-case traffic. The argument for the 35 kbps recommendation is well-supported by the margin analysis and the ARQ requirements under correlated loss.

## 4. Clarity & Structure
**Rating: 4 (Good)**
The paper is generally well-written and organized. The notation is clear (Table I is helpful). The distinction between the "logical" 1 kbps allocation and the "physical" 35 kbps channel is explained well. However, the density of information in the abstract and introduction is high; some of the "alphabet soup" (DES, CCSDS, GE, MAC, TDMA) could be smoothed out for a broader readership. The figures are referenced appropriately, though Figure 3 (NS-3 validation) is critical and needs to be legible in the final print.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**
The authors provide a clear Data Availability statement with a GitHub link (including a specific tag). They also include a specific acknowledgment regarding AI usage (ideation/editing only), which aligns with emerging best practices in scientific publishing.

## 6. Scope & Referencing
**Rating: 4 (Good)**
The scope is well-defined (per-cluster sizing). The referencing covers the necessary bases: standard astrodynamics texts, CCSDS standards, and relevant networking literature. The comparison to DVB-RCS2 provides good context. A minor gap exists in referencing specific hardware limitations of current S-band transceivers for CubeSats/SmallSats—confirming that 35 kbps half-duplex switching times are realistic for COTS hardware would strengthen the practical applicability.

---

## Major Issues

1.  **Contextualization of the "Campaign Duty Factor" ($d$)**
    *   **Issue:** While $d$ is defined mathematically, its operational derivation is still slightly abstract. The paper states $d=0.10$ is the default, but does not fully justify *why* 10% is the correct number for a generic mission.
    *   **Why it matters:** If $d$ is actually 0.50 for a specific mission class (e.g., active debris removal), the sizing conclusions change.
    *   **Remedy:** In Section II-C or IV-E, explicitly link $d$ to specific mission phases (e.g., "During station-keeping, $d \approx 0.01$; during collision avoidance maneuvers, $d$ effectively spikes to 1.0 for short bursts"). The current text touches on this, but a small table mapping Mission Phase $\to$ Estimated $d$ would add immense practical value.

2.  **Assumption of Static Cluster Membership**
    *   **Issue:** The simulation assumes static membership with re-association overhead dismissed as $<0.5\%$.
    *   **Why it matters:** In LEO mega-constellations, relative motion between orbital planes is high. If clusters are defined topologically (nearest neighbors), membership changes frequently. If defined by orbital plane, they are static but cross-plane links vary.
    *   **Remedy:** Clarify in the System Model whether clusters are intra-plane (static neighbors) or inter-plane. If intra-plane, the static assumption holds. If inter-plane, the Doppler and handover overheads need a stronger defense than a single sentence.

3.  **Hardware Turnaround Time Sensitivity**
    *   **Issue:** The feasibility relies on $\alpha_{RX}$ and the ability to fit ingress/egress into $T_c$. The margin analysis (Table IV) lists "TX/RX turnaround" as 4ms total.
    *   **Why it matters:** Many COTS S-band radios have turnaround times in the 10-50ms range, not 2ms. If the hardware is slow, the guard times must increase, potentially invalidating the 35 kbps recommendation.
    *   **Remedy:** Add a sensitivity check or a comment in Section V (Falsification Conditions) specifically regarding radio turnaround time. If $T_{turnaround} > 20$ms, does the 35 kbps link still close the timing budget?

## Minor Issues

1.  **Figure 3 Legibility:** Ensure the shaded band in Figure 3(a) (NS-3 validation) is clearly visible in black-and-white print.
2.  **Equation 10 (Consensus):** The variable $N_R$ is used but not defined in Table I or the immediate text (presumably "Number of Replicas"?). Please define.
3.  **Abstract Density:** The abstract is very dense with numbers. Consider rounding "0.73--0.76" to "0.73--0.76" (en-dash) and perhaps removing the specific "46%" reference in favor of "stress-case bounds" to improve readability.
4.  **Section IV-C:** The text refers to "Table V" for slot structures, but the caption says "Table VI". Please verify table numbering.
5.  **Typos:**
    *   Section I-A: "mid-2024" (ensure this is current at time of publication).
    *   Section II-A: "NASA DSA [23]" - ensure the citation year is correct (2024 is listed, which is fine, just verify).

---

## Overall Recommendation
**Recommendation: Accept with Minor Revisions**

This is a high-quality manuscript that presents a rigorous, mathematically sound framework for sizing spacecraft swarm coordination channels. The authors have successfully addressed the "circular validation" concerns of previous iterations by introducing a distinct NS-3 simulation. The "Two-Test" framework (Byte Budget + Time Budget) is a practical tool for systems engineers.

The revisions requested are primarily to improve the operational context (justifying the duty factor $d$) and to ensure the hardware assumptions (turnaround time) are robust. Once these minor points are addressed, the paper will make a significant contribution to the field of autonomous space systems.

## Constructive Suggestions

1.  **Add a "Hardware Reality Check" Subsection:** In the Discussion, briefly mention typical parameters for S-band patch antennas and transceivers (e.g., GomSpace, EnduroSat) to ground the 35 kbps/2ms turnaround assumptions in COTS reality.
2.  **Expand the "Falsification Conditions":** This is an excellent section. Expand it to include "If inter-cluster interference requires $F > 4$ frequency reuse factors, the effective throughput drops..."
3.  **Visualizing the Duty Factor:** A simple plot of $\eta_{total}$ vs. $d$ would visually demonstrate the linear relationship and help the reader understand the "cost" of increasing command frequency.