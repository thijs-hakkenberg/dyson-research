---
paper: "02-swarm-coordination-scaling"
version: "dn"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-03-07"
recommendation: "Unknown"
---

Here is a rigorous peer review of the manuscript **"Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version DN)**, prepared for *IEEE Transactions on Aerospace and Electronic Systems*.

---

## 1. Significance & Novelty
**Rating: 4 (Good)**
The paper addresses a critical gap in the literature: the lack of closed-form sizing relationships for coordinating "mega-constellation" scale swarms ($10^4$--$10^5$ nodes). While high-bandwidth optical ISLs are well-studied, the specific focus on a robust, low-bandwidth S-band control plane is timely and practically valuable. The derivation of the campaign duty factor ($d$) and the two-test feasibility framework provides a novel, usable toolset for systems engineers. The novelty lies not in new fundamental networking theory, but in the rigorous application and parameterization of these theories for a specific, constrained aerospace domain.

## 2. Methodological Soundness
**Rating: 5 (Excellent)**
The methodology is robust. The authors have moved beyond simple mean-value analysis by integrating a Gilbert-Elliott (GE) channel model to capture bursty loss dynamics, which is essential for RF ISLs. The inclusion of an independent NS-3 packet-level simulation to validate the custom Python discrete-event simulation (DES) is a significant strength, directly addressing common concerns about custom simulator validity. The decomposition of the discrepancy between analytical and NS-3 results (framing, jitter, residual) is scientifically rigorous.

## 3. Validity & Logic
**Rating: 4 (Good)**
The logical flow from traffic modeling to bandwidth sizing is sound. The distinction between information rate, PHY rate, and slot efficiency ($\gamma$) is handled with necessary precision. The "Two-Test" framework (Byte Budget vs. Airtime) correctly decouples logical traffic generation from physical layer constraints. The argument for 35 kbps as a robust design point is well-supported by the sensitivity analysis. However, the reliance on a static cluster membership assumption (mentioned as a limitation) slightly weakens the logic regarding dynamic topology management, though the authors attempt to bound this.

## 4. Clarity & Structure
**Rating: 5 (Excellent)**
The manuscript is exceptionally well-written. The notation is consistent, and the distinction between similar variables (e.g., $\eta$ vs. $\eta_{total}$) is explicit. Algorithm 1 provides a clear summary of the proposed sizing procedure. Figures are relevant, particularly Fig. 3 (NS-3 validation) and Fig. 4 (Inter-cycle recovery). The "Rate Ladder" (Table V) is a very effective pedagogical tool for explaining the overhead stack-up.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**
The authors provide a clear Data Availability statement pointing to a repository with source code and datasets. The Acknowledgment section transparently discloses the use of AI for ideation and editing, adhering to emerging best practices for AI disclosure in scientific publishing.

## 6. Scope & Referencing
**Rating: 4 (Good)**
The references cover the necessary bases: constellation operations (Starlink, OneWeb), networking protocols (CCSDS, DTN), and theoretical foundations (queueing, consensus). The connection to DVB-RCS2 standards for TDMA context is appreciated. The scope is appropriate for *IEEE TAES*, bridging the gap between pure networking theory and spacecraft systems engineering.

---

## Major Issues

1.  **Spatial Reuse Factor ($R=7$) Justification**
    *   **Issue:** The paper assumes a spatial reuse factor of $R=7$ to dismiss fleet-level channel reuse constraints (Eq. 9), stating it is "provisional pending RF simulation."
    *   **Why it matters:** If $R$ must be lower (e.g., $R=3$ or $R=1$) due to omnidirectional antenna patterns or specific orbital geometries, the fleet-level TDMA cycle $T_c^{fleet}$ could explode, rendering the 10s cycle time impossible regardless of the intra-cluster sizing.
    *   **Remedy:** While a full RF simulation is out of scope, the authors must provide a stronger analytical geometric argument or a worst-case sensitivity analysis for $R$. Specifically, calculate the "break-even" $R$ value below which the system fails, and discuss if that value is physically plausible for S-band patch antennas.

2.  **Cluster Coordinator Handover Overhead**
    *   **Issue:** The simulation assumes static cluster membership. While the text claims re-association overhead is $<0.5\%$, this is relegated to the Supplement.
    *   **Why it matters:** In LEO swarms, relative motion and node failures necessitate coordinator rotation (LEACH-style). This creates "dead time" or bursty signaling traffic that isn't captured in the steady-state $\eta$ or Test B.
    *   **Remedy:** Bring the summary of the re-association overhead analysis into the main text (Section IV or V). Explicitly state how the "Guard" or "Margin" in the TDMA superframe absorbs the specific signaling required for a coordinator handover.

3.  **Latency Tail in "Stress" Case**
    *   **Issue:** The paper notes that the stress case ($d=1$) is feasible regarding bandwidth, but does not explicitly detail the latency/AoI tail behavior during this saturation event.
    *   **Why it matters:** If the queues build up during a "reconfiguration campaign," the Age of Information (AoI) might degrade to the point where the control loop becomes unstable, even if the bytes eventually fit.
    *   **Remedy:** Add a sentence or small data point regarding the P99 AoI specifically during the $d=1$ stress phase. Does it stay within the 30s safety bound?

---

## Minor Issues

1.  **Eq. 10 (Raft Consensus):** The variable $f_{decision}$ is introduced in Eq. 10 but not defined in Table I or the immediate text. Presumably, it is the frequency of consensus decisions, but units (Hz? per cycle?) should be explicit.
2.  **Table IV (Superframe):** The "Re-sync preamble (32-bit ASM)" is listed as 1ms. At 30 kbps, 32 bits is $\approx 1.06$ ms. Please clarify if this includes any silence/padding, or if the rounding is just for the table.
3.  **Figure 2 (Margin Sensitivity):** The caption mentions a "Star" and "Diamond" marker, but in black-and-white print, these can be hard to distinguish if the plot lines are dense. Ensure markers are distinct in size/shape.
4.  **Section III-A (Feasibility Threshold):** The derivation $\epsilon^{50} < 0.01$ assumes independence. The text immediately acknowledges GE correlation, but the initial derivation might confuse a reader skimming. Rephrase to lead with the correlated reality or clearly label the independence assumption as a "best-case baseline."
5.  **Reference Style:** Ref [14] is a technical report from the authors. Ensure this link is persistent/archived (e.g., ArXiv or Zenodo) rather than a generic project URL which may rot.

---

## Overall Recommendation
**Recommendation: Accept with Minor Revisions**

This is a high-quality manuscript that offers a pragmatic, mathematically sound approach to sizing communication links for large-scale space swarms. The authors have successfully addressed the "reality gap" often found in such papers by incorporating CCSDS framing overheads, stochastic acquisition jitter, and correlated channel losses.

The transition from a purely theoretical model to a validated engineering tool (via NS-3 and the "Two-Test" framework) is the paper's strongest contribution. The 35 kbps recommendation is well-justified. The revisions requested regarding the Spatial Reuse Factor and Coordinator Handover are necessary to ensure the "system level" feasibility claims hold up to scrutiny, but they do not require new experimentation—only better contextualization of existing assumptions.

---

## Constructive Suggestions

1.  **Strengthen the "Design Heuristic":** In Section III-A, you present $R_{PHY,min}$ as a heuristic. I suggest elevating this. It is effectively a "Rule of Thumb" for early-phase mission design. Consider highlighting it in a call-out box or a specific "Key Takeaway" subsection for practitioners.
2.  **Clarify "Campaign Duty Factor" usage:** The parameter $d$ is excellent. To make it more usable, explicitly suggest how a mission planner should estimate $d$. Is it based on the $\Delta V$ budget? The number of conjunction warnings per year? A brief sentence linking $d$ to physical mission constraints would add value.
3.  **GE Model Context:** In Section II-E, you mention "Missions should measure $\tau_c$." Suggest adding a reference to *how* they might do this (e.g., using RSSI sampling on existing beacons).
4.  **Visualizing the "Cliff":** Fig. 3(b) shows the deadline miss rate. It would be powerful to overlay the "Analytical Prediction" line on this plot to visually demonstrate the agreement (or the slight offset) regarding where the "cliff" occurs (24 vs 30 kbps).