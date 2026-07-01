---
paper: "02-swarm-coordination-scaling"
version: "dc"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-03-05"
recommendation: "Unknown"
---

Here is a comprehensive peer review of the manuscript "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version DC), prepared for *IEEE Transactions on Aerospace and Electronic Systems*.

---

## 1. Significance & Novelty
**Rating: 4 (Good)**
The paper addresses a critical gap in the literature: the lack of closed-form sizing relationships for coordinating massive space swarms ($10^4$--$10^5$ nodes) under strict bandwidth constraints. While high-level architecture papers exist, this work provides specific, actionable engineering equations linking byte-level budgets to physical-layer TDMA timing. The derivation of the "two-test feasibility framework" is a significant contribution for systems engineers. The novelty lies in the integration of CCSDS-grounded framing overheads into a swarm coordination model, moving beyond abstract graph-theory approaches.

## 2. Methodological Soundness
**Rating: 5 (Excellent)**
The methodology is rigorous. The authors have moved away from arbitrary efficiency factors (the previous 0.85) to a derived $\gamma$ based on CCSDS Proximity-1 framing, which is a substantial improvement. The use of a three-tier simulation approach (Analytical $\to$ DES $\to$ Slot-level) provides strong internal verification. The explicit handling of the "rate paradox" (where $\gamma$ decreases as PHY rate increases) demonstrates deep insight into the physical layer constraints. The link budget calculations are standard and correct.

## 3. Validity & Logic
**Rating: 4 (Good)**
The logic is generally sound. The distinction between the logical 1 kbps allocation and the physical 35 kbps link is clearly articulated. The handling of the "stress case" ($d=1$) vs. "nominal case" ($d=0.10$) is logical and prevents over-designing for rare events.
*Critique:* The logic regarding the "structural ineffectiveness" of intra-cycle ARQ under the GE model is mathematically correct *given the assumption* that the channel state is coherent over the cycle ($T_c$). However, this assumption is a strong one. While the paper acknowledges this as a "what-if" tool, the binary classification of "ineffective" vs "effective" could be nuanced by partial coherence models.

## 4. Clarity & Structure
**Rating: 5 (Excellent)**
The manuscript is exceptionally well-structured. The "Rate Ladder" (Table IV) and the "Margin Analysis" (Table VI) are exemplary ways to present complex sizing trade-offs. The distinction between Model C (CCSDS) and Model S (Simplified) is handled with great care to avoid confusion. The notation table is comprehensive.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**
The authors provide a clear Data Availability statement with a GitHub link (though obviously a placeholder for this review exercise, the intent is clear). The AI disclosure is specific and appropriate, detailing that AI was used for ideation and editing but not for result generation.

## 6. Scope & Referencing
**Rating: 4 (Good)**
The referencing is adequate, covering swarm robotics, constellation management, and CCSDS standards.
*Critique:* The paper relies heavily on CCSDS Proximity-1. While appropriate, a brief discussion or reference to commercial proprietary protocols (like those used by Starlink or Kuiper, even if inferred from filings) would strengthen the context, acknowledging that not all mega-constellations will use CCSDS.

## 7. Theoretical Depth
**Rating: 4 (Good)**
The derivation of the sizing equations is solid. The queueing theory application ($M/D/1$, $M/D/c$) is standard but applied correctly to the specific domain. The probabilistic bounds for AoI and recovery cycles are well-derived.

## 8. Simulation & Experimentation
**Rating: 4 (Good)**
The DES and slot-level simulators are well-described. The use of 30 Monte Carlo trials with bootstrap CIs is statistically sound.
*Critique:* As noted by the authors themselves, there is a "Validation Gap" regarding external hardware or channel measurements. While the paper is honest about this, the lack of NS-3 simulation to validate the spatial reuse ($R=3$) and interference assumptions is a limitation for a "top-tier" journal, though the analytical arguments are persuasive.

## 9. Practical Applicability
**Rating: 5 (Excellent)**
This is the paper's strongest point. Algorithm 1 and the lookup tables provide immediate value to practitioners. The "what-if" design curves for the GE model allow engineers to input their own coherence times. The focus on "sizing" rather than just "analyzing" makes it highly relevant for early-phase mission design.

## 10. Overall Quality
**Rating: 4 (Good)**
This is a high-quality engineering paper. It bridges the gap between high-level swarm algorithms and low-level link constraints. The revisions (Version DC) have addressed previous concerns about realism (gamma derivation, duty factors) effectively.

---

## Major Issues

1.  **Interference Analysis for Spatial Reuse ($R=3$):**
    *   **Issue:** The paper asserts that a spatial reuse factor of $R=3$ is sufficient based on a single-interferer C/I calculation ($26$ dB $> 20$ dB).
    *   **Why it matters:** In a dense swarm or mega-constellation, a cluster will likely see aggregate interference from *multiple* co-channel clusters (the "cocktail party" effect). If 6 surrounding clusters are transmitting, the noise floor rises, potentially violating the 20 dB requirement.
    *   **Remedy:** You must refine the C/I calculation in Section IV-A-1 to account for aggregate interference. If $C/(\sum I) < 20$ dB, you may need to recommend $R=7$ (and consequently $F=8$ channels). At minimum, add a sensitivity note that $R=3$ is a best-case geometry and $R=7$ is the conservative bound.

2.  **RF-Backup "Suspension" vs. "Coordination":**
    *   **Issue:** The paper states hierarchical coordination is "suspended" during RF-backup, yet discusses Raft elections on UHF.
    *   **Why it matters:** There is a slight contradiction in terms. If Raft is running, *some* coordination is happening. If the system is in "safe-hold," why is a leader election urgent?
    *   **Remedy:** Clarify in Section III-B-2 that the UHF Raft election is a *recovery transient* to restore the S-band control plane, not a steady-state coordination mode. Explicitly state that during the ~300s gap, nodes rely on passive orbital safety (which is valid given the low collision probability cited) and do not perform active station-keeping.

3.  **Unicast Stagger Latency Context:**
    *   **Issue:** The result that unicast commands require a 19-cycle stagger ($L_{cmd}=19$, ~190s) is presented as feasible.
    *   **Why it matters:** For formation flying or collision avoidance, 190s might be too long.
    *   **Remedy:** Explicitly qualify *which* types of commands are acceptable with 190s latency (e.g., orbit raising, software patches) and which are not (e.g., immediate collision avoidance). Reiterate that safety-critical commands use the broadcast slot (1 cycle latency).

## Minor Issues

1.  **Table I (Notation):** The definition of $\gamma$ refers to "Section IV-J". In the text, this appears to be Section IV-I or IV-J depending on formatting. Ensure section references align with the final layout.
2.  **Section IV-H (Standards-Based...):** The text mentions "DVB-RCS2 terminals achieve $\gamma = 0.70$--$0.85$." Please clarify if this is a return link (TDMA) or forward link (TDM) comparison, as DVB-RCS2 overhead structures differ significantly from Proximity-1.
3.  **Figure 3 (Margin Sensitivity):** The caption mentions "Star" and "Diamond" markers. Ensure these are clearly visible in the final high-res figures; in some drafts, markers on lines can be obscured.
4.  **Eq. 10 (Gamma):** The term $T_{framing}$ is defined as $O_{frame} / (R_{FEC} \cdot R_{PHY})$. Verify if the framing bits (ASM) are actually FEC encoded in Proximity-1. Usually, the ASM is attached *after* coding to aid synchronization. If ASM is uncoded, the equation should be $T_{ASM} + (O_{header}/R_{FEC})/R_{PHY}$. This is a minor timing difference ($<1$ ms) but worth precision.
5.  **Typos:**
    *   Section III-A: "Slot-sim reveals ARQ$\times$TDMA coupling" - ensure "Slot-sim" is consistent (sometimes "slot-sim", sometimes "TDMA simulator").

## Overall Recommendation
**Recommendation: Accept with Minor Revisions**

This manuscript presents a robust, mathematically grounded framework for sizing communication resources in large space swarms. The authors have successfully addressed the "realism gap" often found in swarm literature by incorporating rigorous CCSDS-based framing overheads ($\gamma$) and a realistic campaign duty factor ($d$). The "Two-Test Feasibility Framework" is a valuable contribution to the field.

The primary strengths are the closed-form design equations, the clear distinction between logical and physical bandwidths, and the honest assessment of validation gaps. The stress-case analysis ($d=1$) vs. routine operations ($d=0.10$) effectively resolves concerns about over-provisioning.

The requested revisions are focused on tightening the interference assumptions (moving from single-interferer to aggregate) and clarifying the operational concept during RF-backup modes. These are well within the scope of minor revisions.

## Constructive Suggestions

1.  **Refine the Interference Argument:** In Section IV-A-1, calculate the aggregate interference from the first tier of co-channel clusters (usually 6 in a hexagonal lattice). If this pushes the link margin below requirements, update the recommendation to $R=7$ or suggest adaptive coding/modulation (ACM) for edge-of-cell cases.
2.  **Strengthen the "Rate Paradox" Explanation:** The insight that $\gamma$ decreases as rate increases is counter-intuitive to many. Consider adding a small callout box or a specific sentence in the conclusion emphasizing this: "Designers must account for the diminishing returns of higher PHY rates due to constant-time acquisition overheads."
3.  **Operationalize the GE Model:** You present the GE model as a "what-if" tool. To make it even more practical, provide a "measurement protocol" in the discussion: "We recommend missions log RSSI transitions per cycle to estimate $p_{BG}$ and $\tau_c$ during commissioning, then use Fig. 2b to set $M_r$ dynamically."
4.  **Clarify ASM Coding:** Check CCSDS 131.0-B-4 regarding Attached Sync Markers (ASM). If the ASM is not LDPC encoded (which is standard for sync), adjust Eq. 10 slightly. The impact on $\gamma$ is negligible ($<0.01$), but it demonstrates attention to detail.