---
paper: "02-swarm-coordination-scaling"
version: "ck"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-03-03"
recommendation: "Unknown"
---

Here is a rigorous peer review of the manuscript (Version CK), structured for *IEEE Transactions on Aerospace and Electronic Systems*.

---

# Peer Review Report

**Manuscript ID:** [Assumed Version CK]
**Title:** Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms
**Target Journal:** IEEE Transactions on Aerospace and Electronic Systems

## 1. Significance & Novelty
**Rating: 4 (Good)**
The paper addresses a critical gap in the literature: the lack of closed-form sizing relationships for coordination architectures in the $10^3$--$10^5$ node regime. While mega-constellation routing is well-studied, the specific problem of *command and control* (C2) traffic sizing under strict bandwidth constraints (1 kbps RF backup) is novel. The derivation of a two-layer feasibility framework (byte budget + TDMA airtime) is a significant contribution for systems engineers.

## 2. Methodological Soundness
**Rating: 4 (Good)**
The methodology is generally robust. The progression from analytical means to Discrete Event Simulation (DES) for tail analysis, and finally to slot-level simulation for schedulability, is logical. The explicit derivation of $\gamma$ (slot efficiency) from CCSDS standards rather than assuming a heuristic value is a major strength of this version. The Gilbert-Elliott (GE) model application is sound, though the reliance on assumed parameters ($p_{BG}$) rather than empirical ISL data remains a limitation (acknowledged by the authors).

## 3. Validity & Logic
**Rating: 5 (Excellent)**
The internal logic is tight. The authors have rigorously addressed previous concerns regarding the interaction between ARQ and TDMA timing. The distinction between "byte budget feasibility" and "airtime schedulability" is clearly articulated. The counter-intuitive finding that intra-cycle ARQ is ineffective under blockage-dominated coherence ($\tau_c \ge T_c$) is well-supported by the Markov analysis.

## 4. Clarity & Structure
**Rating: 5 (Excellent)**
The manuscript is exceptionally well-structured. The "Rate Ladder" (Table IV) and the "Feasibility Test" (Algorithm 1) are high-value additions that make the theoretical work immediately actionable for practitioners. The distinction between Model S (simplified) and Model C (CCSDS) is handled with precision, preventing confusion about where the margins come from.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**
The authors provide a clear data availability statement pointing to a repository. The AI disclosure is specific and appropriate (ideation/editing only, not result generation).

## 6. Scope & Referencing
**Rating: 4 (Good)**
The literature review covers swarm robotics, constellation management, and delay-tolerant networking well. The connection to CCSDS standards (Proximity-1, TC Space Data Link) is strong. However, the paper could benefit from slightly more engagement with recent work on optical-wireless hybrid scheduling, as this is the primary operational mode, even if RF is the bottleneck.

---

## Major Issues

1.  **Justification of the "Safe Mode" Locus of Control**
    *   **Issue:** The paper argues that the 1 kbps RF-backup channel is the design driver because it supports "safe mode." However, the text notes that hierarchical coordination is *suspended* during RF-backup (Section III-B-2) and nodes revert to beacon-only operations. If the hierarchy is suspended, why does the *hierarchical* coordinator ingress requirement (27 kbps) drive the RF link sizing? There is a logical tension here: you size the link for a hierarchy that you claim is suspended when using that link.
    *   **Why it matters:** This undercuts the central premise that the hierarchical overhead analysis dictates the RF backup hardware requirements.
    *   **Remedy:** Clarify the operational concept. Is the 35 kbps link intended for *degraded* operations (where hierarchy is maintained but optical is down) vs. *survival* operations (tumbling/safe-hold)? If the 35 kbps link is S-band (as per Table III), it is likely directional or semi-directional, not omni. The distinction between the "Coordination Channel" (S-band, 35 kbps) and "RF-Backup" (UHF, 1 kbps) needs to be sharper in the feasibility arguments. Explicitly state that the TDMA sizing applies to the S-band layer, not the UHF layer.

2.  **Sensitivity of $\gamma$ to Range/Guard Time Variations**
    *   **Issue:** The derivation of $\gamma_{C,24} = 0.761$ assumes a specific guard time based on a 500 km cluster diameter. However, during constellation deployment or phasing, ranges may vary significantly.
    *   **Why it matters:** If the cluster spreads to 1000 km or 2000 km, the propagation delay increases, potentially invalidating the fixed $\gamma$.
    *   **Remedy:** Add a brief sensitivity check or a formula modifier for distance $D$. Since $T_{prop} \approx 3.3 \mu s/km$, a 2000 km range adds ~5ms to the round trip, which is non-negligible against the 4.7ms guard budget.

3.  **Thundering Herd on Recovery**
    *   **Issue:** Section III-B-2 discusses the "thundering herd" when a coordinator fails. The analysis relies on Slotted ALOHA stability. However, if the coordinator fails, the *synchronization reference* for the slots might also drift or vanish (depending on if sync is GNSS-derived or coordinator-derived).
    *   **Why it matters:** If slots are lost, the system degrades to pure ALOHA (0.18 efficiency) rather than Slotted ALOHA (0.36), doubling the recovery time.
    *   **Remedy:** Explicitly state the synchronization assumption during coordinator failure. If GNSS is assumed, Slotted ALOHA holds. If not, the analysis must account for the efficiency drop.

## Minor Issues

1.  **Table II (Key Notation):** The symbol $d$ is defined as "Campaign duty factor," but in some contexts (Section IV-E), it implies a probability. Clarify if $d$ is a deterministic duty cycle or a Bernoulli probability.
2.  **Fig. 6 (Margin Sensitivity):** The caption mentions "Star" and "Diamond" markers, but check if these will be legible in black-and-white print. Ensure distinct shapes are used.
3.  **Section IV-C (GE Model):** The mapping of "Antenna mispointing" to $\tau_c \approx 10-60s$ is plausible, but a citation or derivation based on ADCS slew rates/deadbands would strengthen this.
4.  **Equation 5 (Fleet Reuse):** The variable $G$ is used for groups, but $G$ is often used for Antenna Gain or Offered Load in ALOHA contexts. Ensure no notation collision with the ALOHA discussion in Section III.
5.  **Typos:** Section IV-H, "The 24--48 h duty cycles occupy the Pareto frontier" - check if "h" should be spelled out or consistent with "s" (seconds).

---

## Overall Recommendation
**Recommendation: Accept with Minor Revisions**

This is a high-quality, rigorous manuscript that significantly advances the state of the art in sizing communication architectures for large-scale space swarms. The authors have done an excellent job of moving beyond simple "bits per second" calculations to include protocol overhead, framing efficiency, and stochastic effects.

The "Two-Layer Feasibility Framework" is a valuable contribution that should become standard practice for systems engineers in this field. The derivation of the CCSDS-based slot efficiency ($\gamma \approx 0.76$) is particularly useful, correcting optimistic assumptions often found in early-phase design.

The revisions requested are primarily clarifications regarding the operational concept (specifically the distinction between the S-band coordination layer and the UHF survival layer) to ensure the sizing logic holds up to scrutiny. Once these logical links are tightened, the paper is ready for publication.

## Constructive Suggestions

1.  **Refine the "Mode Map":** Table III is helpful, but I suggest explicitly linking the "Sizing Case" to the "Mode." For example, state clearly: "The TDMA sizing analysis (Section IV) applies strictly to the S-band Coordination Channel. The UHF link is sized only for the Safe Mode beacon profile." This resolves Major Issue #1.
2.  **Expand Algorithm 1:** Consider adding a check for "Latency Constraint" in Algorithm 1. Currently, it checks byte and airtime feasibility. Adding a line that checks `if L_cmd * Tc > Max_Allowed_Latency then Infeasible` would make it a complete system sizing tool.
3.  **Visualizing the "Cliff":** Figure 8 (Gamma vs Rate) is good. It might be impactful to overlay a "Feasibility Cliff" line showing exactly where the margin becomes negative for the $k_c=100$ baseline.