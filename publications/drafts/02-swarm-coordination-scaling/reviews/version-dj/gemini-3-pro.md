---
paper: "02-swarm-coordination-scaling"
version: "dj"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-03-06"
recommendation: "Unknown"
---

Here is a comprehensive peer review of the manuscript (Version DJ) for *IEEE Transactions on Aerospace and Electronic Systems*.

---

# Peer Review Report

**Manuscript Title:** Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms
**Version:** DJ

## 1. Significance & Novelty
**Rating: 4 (Good)**
The paper addresses a critical gap in the literature: the specific sizing of coordination channels for mega-constellations where centralized ground control is untenable. While high-level architecture papers exist, this work provides concrete, closed-form sizing equations that link byte-level protocol overhead to physical-layer TDMA timing. The distinction between "loose coordination" (S-band) and "tight formation" (optical) is a necessary pragmatic boundary. The derivation of the "continuous-duty bound" ($\eta \approx 46\%$) vs. routine operations is a valuable contribution for mission planners.

## 2. Methodological Soundness
**Rating: 5 (Excellent)**
The methodology is rigorous. The authors employ a multi-tiered verification approach (Tier 1-3) that is intellectually honest about what is validated (internal consistency) vs. what is parameterized (CCSDS standards). The shift from a simplified slot model to "Model C" (CCSDS Proximity-1) significantly strengthens the realism. The use of the Gilbert-Elliott (GE) model as a "what-if" design tool, rather than claiming it represents a specific measured channel, is the correct scientific approach given the lack of public ISL data. The two-test feasibility framework (Byte Budget + TDMA Airtime) is logically sound.

## 3. Validity & Logic
**Rating: 5 (Excellent)**
The internal logic is consistent. The authors have successfully addressed previous concerns regarding the coupling of ARQ and TDMA. The demonstration that intra-cycle ARQ is ineffective under slow-fading conditions ($\tau_c \ge T_c$) is mathematically sound and crucial for design. The derivation of the slot efficiency $\gamma$ is transparent, and the sensitivity analysis regarding acquisition timing ($T_{acq}$) provides necessary robustness. The distinction between logical traffic allocation (1 kbps) and burst PHY rate (35 kbps) is clearly explained and justified.

## 4. Clarity & Structure
**Rating: 4 (Good)**
The paper is dense but well-organized. The "Rate Ladder" (Table IV) and the "Feasibility Test" (Algorithm 1) are excellent synthesis tools that make the complex derivation actionable for practitioners. However, the density of variables and parenthetical definitions in the text can occasionally impede flow. The distinction between the various overhead metrics ($\eta$, $\eta_{total}$, $\eta_0$) is handled well via the "Canonical overhead definitions" section.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**
The authors provide a clear Data Availability statement pointing to a repository. The acknowledgment of AI usage for ideation (but not generation of results) aligns with current IEEE guidelines. There are no apparent conflicts of interest or plagiarism concerns.

## 6. Scope & Referencing
**Rating: 4 (Good)**
The literature review covers the intersection of swarm robotics, constellation management, and networking well. The inclusion of CCSDS standards (Proximity-1, Space Packet Protocol) anchors the work in reality. The paper fits well within the scope of TAES, bridging the gap between abstract control theory and practical communication systems engineering.

---

## Major Issues

1.  **Contextualization of the "Stress Case" (46%)**
    *   **Issue:** While the abstract and introduction mention that the 46% overhead occurs $<1\%$ of the time, the results section (specifically Table VI) presents the "Full-load" profile prominently alongside routine profiles. A casual reader might interpret 46% as the design point for power/thermal sizing rather than a transient worst-case.
    *   **Why it matters:** Misinterpreting this bound could lead engineers to massively oversize the RF system or battery capacity, negating the benefits of the proposed architecture.
    *   **Remedy:** In Section IV.E (Workload Design Envelope), explicitly state that thermal/power subsystems should likely be sized for the $d=0.10$ case, while the *buffer* and *spectrum* allocation must handle the $d=1.0$ burst. Differentiate between "dimensioning for throughput" (spectrum) and "dimensioning for energy" (battery).

2.  **Unicast Command Latency Implications**
    *   **Issue:** The paper notes that unicast commands require a 19-cycle stagger ($L_{cmd} \approx 190$s). While the text claims this is acceptable for "non-time-critical orchestration," it does not sufficiently explore the operational risk. If a regional coordinator needs to patch a vulnerability or update an ephemeris for a specific subset of nodes to avoid a conjunction, 3 minutes is a long time.
    *   **Why it matters:** This latency might violate reaction time requirements for certain classes of collision avoidance if the optical link is down.
    *   **Remedy:** Add a brief discussion or a constraint in Algorithm 1 that flags a warning if $L_{cmd} \times T_c$ exceeds a user-defined "Max Reaction Time."

3.  **Fleet-level Interference vs. Cluster Sizing**
    *   **Issue:** The paper relies on a geometric argument ($R=7$) to dismiss inter-cluster interference. While the math ($G=1$) holds for the assumptions given, the dynamic nature of orbital mechanics means that line-of-sight geometries change. A "worst-case" conjunction of multiple clusters over the poles is not modeled.
    *   **Why it matters:** If interference rises, the effective $C/I$ drops, potentially requiring a lower modulation scheme (QPSK vs. higher orders), which would lower the PHY rate and invalidate the 35 kbps recommendation.
    *   **Remedy:** Strengthen the limitation section regarding polar convergence. Explicitly state that the $R=7$ assumption may break down at high latitudes and suggest that future work must address dynamic frequency assignment.

---

## Minor Issues

1.  **Table I (Notation):** The definition of $\alpha_{RX}$ is listed as a "Computed output." It would be helpful to explicitly state it is the "Duty cycle of the ingress phase" for clarity.
2.  **Section III.B.2 (Thundering Herd):** The analysis assumes Slotted ALOHA for the Raft election. Please clarify if the "slots" here are the same dimension as the TDMA data slots or shorter "election mini-slots."
3.  **Figure 3 (Gamma vs. Rate):** The "Model S" curve is retained for comparison. Ensure the caption explicitly says "Model S is for illustrative comparison only; do not use for design," to prevent misuse.
4.  **Algorithm 1, Line 11:** The logic `IF M_r > 0 AND ...` is correct, but the fallback `ELSIF` condition implies that if ARQ fits, we use it; if not, we drop it entirely. Is there a middle ground (e.g., reducing $M_r$ from 2 to 1)? A comment on adaptive $M_r$ would be beneficial.
5.  **Typos:**
    *   Section IV.A: "margin = -1,300 ms" (negative margin). Phrasing is slightly awkward; perhaps "deficit of 1,300 ms."
    *   References: Ensure all URL access dates are consistent (some say Feb 2026, which implies this is a future-dated draft).

---

## Overall Recommendation
**Recommendation: Accept with Minor Revisions**

This manuscript represents a high-quality, rigorous contribution to the field of spacecraft swarm coordination. The authors have successfully moved beyond abstract graph theory to provide concrete, standards-based engineering sizing equations.

**Summary of Assessment:**
The paper's strength lies in its "Two-Test Feasibility Framework," which elegantly decouples the information-theoretic byte budget from the physical-layer timing constraints. The transition to "Model C" (CCSDS framing) addresses previous concerns about realism, and the resulting recommendation of a 35 kbps PHY rate to support a 1 kbps logical stream is well-justified by the margin analysis.

The treatment of the "Campaign Duty Factor" ($d$) is robust, effectively solving the problem of how to dimension for bursty command workloads without oversizing for steady-state. The distinction between slow-fading (inter-cycle recovery) and fast-fading (intra-cycle ARQ) channels provides a nuanced guide for practitioners.

**Critical Improvements Needed:**
The revisions requested are primarily regarding contextualization. The authors must ensure the "stress case" (46% overhead) is not misinterpreted as a continuous power requirement. Additionally, the limitations of the geometric interference model at orbital poles should be highlighted to prevent over-generalization of the $R=7$ reuse factor.

---

## Constructive Suggestions

1.  **Refine the "Design Heuristic":** In Section IV.A, explicitly link the heuristic $R_{PHY} \ge C_{info} / (\gamma \cdot \alpha_{RX})$ to the algorithm. It is a powerful "back-of-the-envelope" tool that deserves to be highlighted as the "first pass" check before running the full Algorithm 1.
2.  **Visualizing the Stagger:** A small timing diagram showing the "Unicast Stagger" ($L_{cmd}$) vs. "Broadcast" would clarify why the unicast latency jumps to 19 cycles. This would help visualize the half-duplex constraint.
3.  **Gamma Lookup Table:** Table VIII is excellent. Consider adding a column for "Required $E_b/N_0$" for the implied modulation/coding at those rates, linking back to the link budget. This connects the MAC layer back to the PHY layer constraints.