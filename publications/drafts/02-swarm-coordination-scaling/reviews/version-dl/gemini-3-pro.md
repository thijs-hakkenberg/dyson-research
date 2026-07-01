---
paper: "02-swarm-coordination-scaling"
version: "dl"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-03-06"
recommendation: "Unknown"
---

Here is a rigorous peer review of the manuscript "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version DL), prepared for *IEEE Transactions on Aerospace and Electronic Systems*.

---

## 1. Significance & Novelty
**Rating: 4 (Good)**
The paper addresses a critical gap in the literature: the lack of closed-form sizing relationships for coordinating large-scale ($10^4$--$10^5$) autonomous satellite swarms. While mega-constellation routing is well-studied, the specific problem of hierarchical command-and-control (C2) traffic accounting under strict bandwidth constraints is less explored. The derivation of the "two-test" feasibility framework (byte budget vs. TDMA airtime) is a valuable contribution for systems engineers. The novelty lies in the integration of CCSDS Proximity-1 framing overheads directly into the sizing equations via the $\gamma$ parameter, rather than treating the link as an idealized bit-pipe.

## 2. Methodological Soundness
**Rating: 4 (Good)**
The methodology is generally robust. The authors employ a multi-tiered simulation approach (DES for traffic/queueing, slot-level simulation for timing/ARQ) which is appropriate. The transition from a simplified $\gamma \approx 0.95$ to a CCSDS-grounded $\gamma \approx 0.73$--$0.76$ is a significant improvement in realism. The use of the Gilbert-Elliott (GE) model to stress-test ARQ strategies is sound, particularly the distinction between fast-fading and slow-fading regimes. However, the reliance on geometric assumptions for fleet-level frequency reuse ($R=7$) without RF simulation remains a weakness, though the authors acknowledge this limitation.

## 3. Validity & Logic
**Rating: 5 (Excellent)**
The internal logic is tight. The distinction between the logical per-node budget (1 kbps) and the physical burst rate (35 kbps) is clearly articulated and mathematically consistent. The analysis of the "stress case" ($\eta \approx 46\%$) is now properly contextualized as a continuous-duty bound that rarely occurs, preventing alarmist conclusions about infeasibility. The coupling between ARQ and TDMA frame timing is logically demonstrated: showing that 30 kbps is theoretically sufficient for bytes but insufficient for retransmission time margins is a subtle but critical validity check.

## 4. Clarity & Structure
**Rating: 5 (Excellent)**
The manuscript is exceptionally well-structured. The "Rate Ladder" (Table IV) and the "Slot Timing Ledger" (Table VII) provide unambiguous traceability for every bit and millisecond. The distinction between "In-$\gamma$" and "Outside-$\gamma$" overheads is handled with precision, resolving potential double-counting errors common in this type of analysis. The notation is consistent, and the decision to consolidate feasibility logic into Algorithm 1 makes the work reproducible.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**
The authors provide a clear data availability statement pointing to a repository with code and datasets. The acknowledgment section transparently discloses the use of AI for ideation and editing, adhering to modern ethical guidelines. There are no apparent conflicts of interest or plagiarism concerns.

## 6. Scope & Referencing
**Rating: 4 (Good)**
The scope is well-defined for S-band coordination. The referencing is adequate, covering standard texts (Wertz, Kleinrock), protocols (CCSDS, Raft), and recent constellation literature. However, the paper would benefit from slightly more engagement with recent works on optical-ISL control planes (e.g., laser-based routing) to better justify why S-band is still the critical bottleneck for coordination specifically, rather than just backup.

---

## Major Issues

1.  **Validation of the $R=7$ Reuse Factor**
    *   **Issue:** The claim that fleet-wide frequency reuse is non-binding relies on a geometric placeholder ($R=7$) derived from hexagonal packing assumptions.
    *   **Why it matters:** If orbital dynamics (particularly at polar convergence) require $R > 10$ to maintain $C/I \geq 20$ dB, the number of required frequency channels ($F$) could exceed available S-band spectrum allocation, invalidating the fleet-level feasibility even if cluster-level sizing works.
    *   **Remedy:** While full RF simulation is out of scope, the authors should add a sensitivity calculation (similar to Eq. 5) determining the *maximum* $R$ supported before the system becomes spectrum-bound given a standard 5-10 MHz allocation.

2.  **Acquisition Time Sensitivity at Lower Rates**
    *   **Issue:** The recommendation of 35 kbps relies heavily on the assumption that $T_{\text{acq}} = 5$ ms. Low-cost CubeSat radios often have PLL lock times closer to 10-20 ms.
    *   **Why it matters:** Table VIII shows that if $T_{\text{acq}}$ drifts to 19 ms, the 35 kbps margin is exhausted.
    *   **Remedy:** Explicitly state in the Abstract or Conclusion that the 35 kbps recommendation is valid *only* for radios with $T_{\text{acq}} \leq 10$ ms. For "lazy" radios ($>10$ ms), a higher rate (e.g., 50 kbps) or longer $T_c$ is required.

3.  **Unicast Command Latency Context**
    *   **Issue:** The derivation of $L_{\text{cmd}} = 19$ cycles (190 s) for unicast commands is mathematically correct but physically unintuitive for operations.
    *   **Why it matters:** A 3-minute latency for commanding a cluster seems high for "coordination."
    *   **Remedy:** Clarify in Section IV-D that this latency applies to *bulk* unicast (sending unique commands to all 100 nodes simultaneously). Clarify that a single unicast command to *one* node takes only 1 cycle.

---

## Minor Issues

1.  **Table I (Notation):** The definition of $\alpha_{\text{RX}}$ is listed as a "Computed output." It would be helpful to explicitly state it is unitless.
2.  **Section III-B (Thundering Herd):** The text mentions "initial $G=25$ (collapse)." Briefly define $G$ (offered load) for readers less familiar with Slotted ALOHA theory.
3.  **Fig. 3 (Margin Sensitivity):** The visual distinction between the "Star" and "Diamond" markers could be clearer; consider using distinct colors in addition to shapes.
4.  **Eq. 10 (Gamma Sensitivity):** The derivative is negative, which is correct, but the text explanation "shifts $R_{\text{PHY,min}}$ up" might be confusing to some. Rephrase to "a decrease in $\gamma$ requires an increase in $R$."
5.  **Typos:** Section IV-A mentions "regional ingress is not capacity-constrained" twice in similar phrasing; condense for flow.

---

## Overall Recommendation
**Recommendation: Accept with Minor Revisions**

This is a high-quality, rigorous manuscript that significantly advances the "systems engineering physics" of large-scale swarm coordination. The authors have successfully moved beyond simple bit-counting to a robust framework that accounts for framing overhead, guard times, and ARQ interactions.

The most critical improvements in this version (Version DL) are the rigorous definition of $\gamma$ based on CCSDS standards and the realistic handling of the campaign duty factor ($d$). The distinction between the "stress case" (46% load) and routine operations (5-10% load) resolves previous concerns about feasibility.

The paper is ready for publication subject to the minor clarifications regarding RF reuse limits and radio acquisition time constraints listed above.

---

## Constructive Suggestions

1.  **Add a "Practitioner's Lookup" for Radio Specs:** In Section V (Discussion), add a small text box or bullet list summarizing the required radio specifications to meet the "35 kbps feasible" claim: (1) $T_{\text{acq}} < 10$ ms, (2) Turnaround $< 2$ ms, (3) Support for CCSDS Proximity-1 or similar efficient framing. This makes the paper immediately useful for hardware selection.
2.  **Clarify "Logical" vs. "Physical" Link:** In the Introduction, emphasize even more strongly that the 1 kbps per-node budget is a *traffic policing policy*, not a hardware data rate. This is the most common point of confusion for readers accustomed to point-to-point links.
3.  **Future Work - Antenna Patterns:** Suggest that future work should investigate the impact of directional antenna sidelobes on the $R=7$ assumption, as this is the largest remaining uncertainty in the fleet-level scaling.