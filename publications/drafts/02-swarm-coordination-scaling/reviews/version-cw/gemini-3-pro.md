---
paper: "02-swarm-coordination-scaling"
version: "cw"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-03-05"
recommendation: "Unknown"
---

Here is a comprehensive peer review of the manuscript **"Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version CW)**, prepared for *IEEE Transactions on Aerospace and Electronic Systems*.

---

## 1. Significance & Novelty
**Rating: 4 (Good)**
The paper addresses a critical gap in the literature: the lack of closed-form sizing relationships for coordinating mega-constellations ($10^4$--$10^5$ nodes) under realistic bandwidth constraints. While swarm robotics and networking exist separately, this work bridges them by providing specific "byte-level" accounting for hierarchical architectures. The novelty lies in the derivation of the two-layer feasibility framework (byte budget vs. TDMA airtime) and the specific parameterization of the "stress case" ($\eta \approx 46\%$) versus routine operations. It moves beyond generic "scalability" claims to provide engineering design equations.

## 2. Methodological Soundness
**Rating: 4 (Good)**
The methodology is generally robust. The use of a discrete event simulation (DES) to verify analytical means (Tier 1) and a separate slot-level simulator to check TDMA timing (Tier 2) is a strong approach. The shift from arbitrary efficiency factors to a CCSDS-grounded $\gamma$ derivation (Model C) significantly strengthens the physical realism. The Gilbert-Elliott (GE) model is correctly identified as a "what-if" design tool rather than a predictive model, which is an important distinction often missed in similar works. The distinction between the logical 1 kbps budget and the physical 35 kbps link rate is now handled with necessary precision.

## 3. Validity & Logic
**Rating: 5 (Excellent)**
The internal logic is tight. The paper rigorously distinguishes between information rate, PHY rate, and effective throughput. The "Rate Ladder" (Table IV) and the feasibility algorithm (Algorithm 1) provide a clear logical progression. The analysis of the ARQ $\times$ TDMA coupling (where intra-cycle ARQ fails under correlated fading when $\tau_c \ge T_c$) is a logically sound and valuable insight. The authors are careful to bound their claims, explicitly stating where external validation is missing (Tier 3).

## 4. Clarity & Structure
**Rating: 5 (Excellent)**
The manuscript is exceptionally well-structured. The "Claim Map" (Table VIII) and the explicit definitions of overhead ($\eta$ vs. $\eta_{total}$) prevent ambiguity. The use of "Model C" (primary) vs. "Model S" (simplified) is clearly delineated, avoiding the confusion seen in earlier drafts of similar works. Figures are relevant, and the tables (especially the parameter sensitivity and rate ladder) are high-value. The writing is concise and professional.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**
The authors provide a clear Data Availability statement with a GitHub link (though obviously a placeholder for review, the intent is clear). The AI disclosure is transparent and specific ("AI-assisted editing applied to prose only"), adhering to modern ethical standards. There are no apparent conflicts of interest or plagiarism concerns.

## 6. Scope & Referencing
**Rating: 4 (Good)**
The scope is appropriate for TAES. The referencing covers the necessary bases: classical queueing theory (Kleinrock), distributed consensus (Raft, Lamport), current constellation operations (Starlink, OneWeb), and relevant CCSDS standards. The connection to DVB-RCS2 and Proximity-1 standards anchors the work in reality.

## 7. Theoretical Depth
**Rating: 4 (Good)**
The derivation of $\gamma$ (Eq. 12) and the stagger equations (Eq. 7) demonstrate sufficient theoretical depth for a systems engineering paper. The queueing analysis is standard but applied correctly to a novel domain. The probabilistic bounds on AoI and recovery cycles are mathematically sound.

## 8. Simulation & Experimentation
**Rating: 4 (Good)**
The simulation campaign is well-designed, covering $N=10^3$ to $10^5$. The use of 30 Monte Carlo replications with bootstrap CIs is statistically sound. The explicit separation of the "Packet-level" and "Cycle-aggregated" simulations is a strength. The lack of hardware-in-the-loop or NS-3 validation is a limitation, but the authors acknowledge this transparently in the "Validation Gap" section.

## 9. Practical Applicability
**Rating: 5 (Excellent)**
This is the paper's strongest point. It is written for practitioners. The "Design Equations" section, the "Rate Ladder," and the "Gamma-Conditional Lookup" (Table VII) are immediately useful for systems engineers sizing spacecraft avionics. The distinction between "theoretical minimum" (30 kbps) and "recommended" (35 kbps) demonstrates real-world engineering judgment regarding margins.

## 10. Overall Quality
**Rating: 4 (Good)**
A high-quality, rigorous systems engineering paper that successfully translates abstract distributed systems concepts into concrete sizing rules for aerospace applications.

---

## Major Issues

1.  **Clarification of "Suspended" Hierarchy during RF-Backup:**
    *   **Issue:** In Section III.B.2, the text states that during RF-backup, hierarchical coordination is "suspended" and nodes enter safe-hold. However, later sections discuss the "RF-backup coordinator failure" and "Thundering herd" election traffic on the backup link.
    *   **Why it matters:** If the hierarchy is suspended, why is there a Raft election on the backup link? If the backup link is only for beacons, how does the coordinator "fail" in a way that triggers an election storm on that specific link?
    *   **Remedy:** Clarify the Concept of Operations (ConOps). Does the swarm attempt to re-elect a coordinator via UHF to restore the high-bandwidth S-band hierarchy? Or does it degrade to a flat mesh? If the hierarchy is suspended, the "thundering herd" analysis might need to be framed as a "recovery transient" rather than an operational mode.

2.  **Spatial Reuse ($R=3$) Justification:**
    *   **Issue:** The paper asserts $R=3$ is feasible for fleet-wide scaling based on free-space path loss (Section IV.A.1 and V.C).
    *   **Why it matters:** In a dense shell (e.g., Starlink-like density), sidelobe interference is significant. $R=3$ is aggressive for omnidirectional or low-gain antennas often used for S-band coordination. If $R$ needs to be 7 (standard cellular), the fleet cycle time doubles, potentially invalidating the "non-binding" claim for fleet scaling.
    *   **Remedy:** Add a sensitivity sentence or footnote acknowledging that if $R=7$ is required, the number of frequency channels $F$ must increase to maintain $T_c$, or $T_c^{fleet}$ increases. This protects the paper from criticism regarding RF interference realism.

## Minor Issues

1.  **Equation 12 Denominator:** In Equation 12, the denominator lists $T_{payload} + T_{FEC} + T_{framing} + T_{guard} + T_{acq}$. Ensure the text explicitly states that $T_{framing}$ includes the *encoded* length of the framing bits, as framing is usually inside the FEC block in CCSDS (except ASM). The text mentions "framing bits are FEC-encoded," which is good, but the variable definition should be precise to avoid confusion with raw bits.
2.  **Table I Notation:** $\gamma_{24}$ and $\gamma_{30}$ are defined, but $\gamma_{35}$ (the recommended point) is missing from the notation table, though present in the text.
3.  **Figure 4 (Buffer CDF):** The caption mentions "Vertical lines: closed-form means," but the lines are difficult to distinguish in the dense plot. Consider thickening these lines or adding explicit labels/arrows.
4.  **Typos:** Section IV.J mentions "DVB-RCS2 terminals... sharing similar framing overhead ratios." It might be safer to say "analogous" rather than "similar" to avoid implying they are identical.

---

## Overall Recommendation
**Recommendation: Accept with Minor Revisions**

This manuscript is a rigorous and valuable contribution to the field of spacecraft swarm engineering. It successfully transitions from the abstract "scalability" discussions often found in literature to concrete, actionable design equations. The authors have done an excellent job addressing potential criticisms by explicitly defining their models (Model C vs. S), acknowledging validation gaps, and providing robust sensitivity analyses.

The "Two-Test Feasibility Framework" is a sound pedagogical and engineering tool. The shift to CCSDS-anchored parameters ($\gamma \approx 0.76$) significantly improves the paper's realism compared to generic efficiency assumptions. The "Stress Case" context ($d=1$ is episodic) is now handled perfectly.

The only substantive request is to clarify the ConOps regarding the "suspended" hierarchy vs. the "thundering herd" election on the backup link to ensure logical consistency in the failure mode analysis. Once addressed, this paper will serve as a standard reference for sizing coordination links.

---

## Constructive Suggestions

1.  **Refine the "Thundering Herd" Context:** In Section III.B.2, explicitly state that the Raft election on the UHF link is a *recovery procedure* to re-establish the S-band control plane, not a steady-state operation. This resolves the tension between "suspended hierarchy" and "election traffic."
2.  **Strengthen the $R=3$ Caveat:** In Section V.C (Limitations), explicitly mention that $R=3$ assumes sufficient antenna discrimination. Suggest that conservative designs might plan for $R=7$, which would linearly impact the fleet-wide update rate or spectrum requirements.
3.  **Expand Table VII:** Consider adding a column for "Max Effective Throughput" (kbps) next to the "Margin" column. This would allow a reader to instantly see the "pipe size" available for payload data at each recommended PHY rate.
4.  **Algorithm 1 Enhancement:** In Line 13 of Algorithm 1 ($L_{cmd}$ calculation), clarify if this assumes the worst-case unicast fraction ($q=1$). It appears to, but making it explicit helps the user.