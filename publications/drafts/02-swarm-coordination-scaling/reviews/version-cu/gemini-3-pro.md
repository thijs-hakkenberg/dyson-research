---
paper: "02-swarm-coordination-scaling"
version: "cu"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-03-05"
recommendation: "Unknown"
---

Here is a comprehensive peer review of the manuscript **"Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version CU)**.

---

## 1. Significance & Novelty
**Rating: 5 (Excellent)**
This paper addresses a critical gap in the literature: the lack of closed-form sizing relationships for coordinating mega-constellations ($10^4$--$10^5$ nodes). While swarm robotics and networking literature exist separately, this work bridges them by providing specific engineering design equations for the "middle layer" between physical links and high-level autonomy. The derivation of a two-layer feasibility framework (byte budget vs. TDMA airtime) is a significant contribution that will likely become a standard reference for systems engineers designing future autonomous fleets.

## 2. Methodological Soundness
**Rating: 4 (Good)**
The methodology is generally robust. The use of a cycle-aggregated Discrete Event Simulation (DES) anchored by a slot-level TDMA simulator is appropriate. The transition from a simplified slot model (Model S) to a CCSDS-grounded model (Model C) significantly strengthens the realism. The explicit handling of the Gilbert-Elliott (GE) channel model as a "what-if" design tool rather than a claim of measured reality is a mature and scientifically honest approach. However, the reliance on unvalidated assumptions for inter-cluster interference (spatial reuse factor $R=3$) remains a weak point, though the authors acknowledge this limitation.

## 3. Validity & Logic
**Rating: 5 (Excellent)**
The internal logic is tight. The authors have rigorously addressed previous concerns regarding the coupling between ARQ and TDMA timing. The distinction between "information rate" and "PHY rate" is handled with precision, avoiding common pitfalls in link budgeting. The derivation of the campaign duty factor ($d$) effectively resolves the tension between continuous and episodic workload modeling. The conclusion that intra-cycle ARQ is structurally ineffective under slow-fading conditions ($\tau_c \ge T_c$) is logically sound and well-supported by the analysis.

## 4. Clarity & Structure
**Rating: 5 (Excellent)**
The manuscript is exceptionally well-written. The notation is consistent, and the distinction between Model S (simplified) and Model C (CCSDS) is clearly demarcated, preventing confusion. Figures are informative, particularly Fig. 3 (recovery analysis) and Fig. 5 (gamma vs. rate). The "Rate Ladder" (Table IV) is a standout pedagogical tool that clearly communicates the design progression.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**
The authors provide a clear Data Availability statement with a GitHub link (though obviously a placeholder for review). The AI disclosure is specific and appropriate, detailing that AI was used for ideation and editing but not for data generation. There are no apparent conflicts of interest or plagiarism concerns.

## 6. Scope & Referencing
**Rating: 4 (Good)**
The literature review covers the necessary bases, ranging from classical queueing theory (Kleinrock) to modern constellation management (Starlink, OneWeb) and CCSDS standards. The inclusion of DVB-RCS2 as a reference for TDMA efficiency adds practical grounding. The scope is well-suited for *IEEE TAES*. A minor expansion on specific antenna technologies required to achieve the assumed spatial reuse would strengthen the fleet-level scaling claims.

---

## Major Issues

1.  **Fleet-Level Spatial Reuse Validation ($R=3$)**
    *   **Issue:** The paper claims fleet-level scaling to $10^5$ nodes relies on a spatial reuse factor $R=3$ and $F=4$ orthogonal channels. This is asserted as an "order-of-magnitude plausibility argument" based on free-space path loss.
    *   **Why it matters:** Without valid spatial reuse, the system capacity collapses for large $N$. In dense orbital shells, sidelobe interference is a complex dynamic problem, not just a static geometric one. $R=3$ is aggressive for omnidirectional or low-gain antennas often used for backup links.
    *   **Remedy:** While full NS-3 simulation is out of scope, the authors should add a sensitivity calculation or a "safety factor" discussion for $R$. If $R$ must be 7 (standard cellular hex reuse), does the architecture break? Explicitly state the impact of $R=7$ on the required number of frequency channels ($F$) to maintain the same $T_c$.

2.  **Coordinator Failure and "Thundering Herd" Recovery**
    *   **Issue:** Section III-B-2 mentions a "thundering herd" scenario where 100 nodes attempt Raft election simultaneously. The text claims Slotted ALOHA with Binary Exponential Backoff (BEB) resolves this in $\sim 2$ doubling rounds.
    *   **Why it matters:** This assumes ideal ALOHA behavior. In reality, 100 nodes waking up simultaneously often leads to persistent collisions or capture effects that can stall elections much longer than theoretical means, especially if the channel is fading (GE model).
    *   **Remedy:** Provide a more conservative upper bound for the election duration. Does the 160s RF-backup transition account for a "bad case" election where the backoff window grows large ($W_{max}=64$ might be too small for 100 contenders)? A brief justification of the $W_{max}$ selection relative to $k_c$ is needed.

3.  **Unicast Stagger Latency Contextualization**
    *   **Issue:** Eq. 8 derives a unicast stagger of 19 cycles ($\sim 190$s). The text states this is acceptable for "orchestration-level commands."
    *   **Why it matters:** Readers might interpret "coordination" as "control." If a collision avoidance maneuver requires individual trajectories for 100 nodes, a 3-minute latency might be unsafe.
    *   **Remedy:** Explicitly restrict the "safety-critical" claim to *broadcast* commands (which are single-cycle). Clarify that if unique trajectories are needed for collision avoidance (unicast), the system latency is 190s, and discuss if this fits within the decision timeline of typical conjunction events (usually hours/days, so likely yes, but needs to be explicit).

---

## Minor Issues

1.  **Table I (Notation):** The definition of $\alpha_{RX}$ is listed as "derived." It would be helpful to explicitly state it is a function of $k_c$ and $S_{eph}$ in the table for quick reference.
2.  **Section IV-J (Gamma Derivation):** The text mentions "DVB-RCS2 terminals... achieve measured slot efficiencies of 0.70--0.85." Please clarify if this includes the return link (TDMA) or forward link (TDM), as return link efficiencies are typically lower due to guard times.
3.  **Fig. 4 (Buffer CDF):** The caption mentions "Bernoulli $d=0.10$." Is this independent Bernoulli per cycle? Please clarify "memoryless" vs "bursty" in the caption to aid interpretation of the tail.
4.  **Eq. 11 (Consensus Stability):** The derivation of $f_{decision,max} \approx 24$ assumes linear scaling. Does this account for the probability of Raft leader re-elections consuming bandwidth? A brief note that this is a "stable leader" upper bound would be precise.
5.  **Typos/Formatting:**
    *   Section III-B-2: "Triple fault... $1.8 \times 10^{-5}$/yr" - check units/exponent consistency with the footnote calculation.
    *   Table V: "Re-sync preamble" is listed as 4ms. Is this per slot or per superframe? (Context implies superframe, but clarify).

---

## Overall Recommendation
**Recommendation: Accept with Minor Revisions**

This is a high-quality manuscript that significantly advances the state of the art in sizing communication architectures for large space swarms. The authors have successfully navigated the complexity of cross-layer design (byte-level protocols vs. signal-level TDMA) and provided actionable design equations.

The manuscript's strengths lie in its rigorous "two-test" feasibility framework, the realistic handling of CCSDS framing overheads (Model C), and the honest treatment of channel model limitations. The distinction between the 24 kbps (infeasible) and 35 kbps (recommended) design points is backed by solid quantitative evidence.

The requested revisions are primarily to bound the claims regarding fleet-level spatial reuse and to clarify specific operational constraints (unicast latency for safety-critical events). Addressing these will ensure the paper serves as a robust reference for the community.

---

## Constructive Suggestions

1.  **Add a "Reuse Sensitivity" Note:** In Section V-C (Design Equations), add a brief note or equation modifier for the Fleet Reuse factor. E.g., "If $R=7$ is required due to antenna sidelobes, the number of frequency channels $F$ must increase to $\approx 9$ to maintain $T_c=10$s."
2.  **Refine the "Thundering Herd" Footnote:** In Section III-B-2, explicitly mention that $W_{max}=64$ is chosen because $k_c=100$ implies an optimal window of $\approx 100$, so 64 is the nearest power-of-two under-provisioning, forcing some collisions but ensuring resolution.
3.  **Visual Aid for Stagger:** Consider annotating Table VI (Feasibility Summary) with a specific row for "Unicast Collision Avoidance" showing the 19-cycle latency, to contrast sharply with "Broadcast Collision Avoidance" (1 cycle). This prevents readers from missing the unicast latency penalty.