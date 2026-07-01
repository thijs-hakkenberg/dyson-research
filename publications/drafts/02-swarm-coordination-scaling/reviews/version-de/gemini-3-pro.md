---
paper: "02-swarm-coordination-scaling"
version: "de"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-03-05"
recommendation: "Unknown"
---

Here is a comprehensive peer review of the manuscript **"Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version DE)**, prepared for *IEEE Transactions on Aerospace and Electronic Systems*.

---

## 1. Significance & Novelty
**Rating: 5 (Excellent)**
The manuscript addresses a critical gap in the literature: the specific sizing of communication architectures for mega-constellations ($10^4$--$10^5$ nodes). While routing in such networks is well-studied, the *control plane* sizing—specifically the byte-level accounting and TDMA scheduling required for hierarchical coordination—is under-represented. The derivation of closed-form sizing equations that link message-layer byte budgets (Test A) with physical-layer airtime constraints (Test B) is a significant contribution. The distinction between "theoretical minimum" (30 kbps) and "recommended engineering margin" (35 kbps) based on CCSDS framing overhead is particularly valuable for practitioners.

## 2. Methodological Soundness
**Rating: 4 (Good)**
The two-test feasibility framework is robust. The authors correctly identify that bandwidth is not the only constraint; time-domain schedulability (ingress/egress slots) is the binding constraint at low data rates. The use of a Gilbert-Elliott (GE) model to stress-test the protocol is appropriate, though the reliance on assumed parameters ($p_{BG}=0.50$) rather than measured channel data is a limitation (acknowledged by the authors). The shift from a generic slot efficiency to a CCSDS-derived $\gamma(R_{\text{PHY}})$ significantly strengthens the realism of the results.

## 3. Validity & Logic
**Rating: 5 (Excellent)**
The internal logic is consistent. The paper rigorously distinguishes between logical traffic allocation (1 kbps) and physical link rates (35 kbps). The handling of the "stress case" ($\eta \approx 46\%$) vs. routine operations is logically sound, preventing the common error of sizing systems for worst-case continuous duty. The analysis of ARQ failure under correlated fading (where $\tau_c \geq T_c$) is mathematically sound and provides a crucial insight: intra-cycle ARQ is structurally ineffective when fading events outlast the cycle.

## 4. Clarity & Structure
**Rating: 5 (Excellent)**
The manuscript is exceptionally well-structured. The "Rate Ladder" (Table IV) and the "Feasibility Test" (Algorithm 1) provide clear, actionable summaries of complex analyses. The distinction between Model C (primary) and Model S (simplified) is handled carefully to avoid confusion. The notation is consistent, and the distinction between information rate and PHY rate is maintained throughout.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**
The authors provide a clear Data Availability statement with a repository link. The Acknowledgment section transparently discloses the use of AI for ideation and editing, adhering to emerging publication standards. There are no apparent conflicts of interest or human subject concerns.

## 6. Scope & Referencing
**Rating: 4 (Good)**
The literature review covers swarm robotics, constellation management, and delay-tolerant networking adequately. The integration of CCSDS standards (Proximity-1, LDPC) anchors the work in reality. However, the paper could benefit from slightly more discussion on how these results compare to specific non-CCSDS proprietary protocols used in NewSpace (e.g., LoRa-based derivatives often proposed for inter-satellite links), even if just to contrast the overhead efficiency.

---

## Major Issues

1.  **Dependency on $p_{BG}$ for ARQ Conclusions**
    *   **Issue:** The strong conclusion that intra-cycle ARQ is ineffective (27% recovery) relies entirely on the assumption that the channel coherence time $\tau_c \geq T_c$ (modeled via $p_{BG}=0.50$ or lower). If a mission experiences fast fading (e.g., multipath from solar panels during tumbling, where $\tau_c \ll T_c$), ARQ would be highly effective.
    *   **Why it matters:** Readers might discard ARQ based on this "structural consequence" without realizing it is conditional on the specific fading dynamic assumed.
    *   **Remedy:** In Section IV-C and the Conclusion, explicitly qualify the dismissal of ARQ. State clearly that *if* $\tau_c \ll T_c$, ARQ remains a viable strategy at 30 kbps. The current text calls this a "what-if design tool," but the recommendation to jump to 35 kbps implies the slow-fading model is the primary driver.

2.  **RF-Backup "Thundering Herd" Recovery Analysis**
    *   **Issue:** The paper estimates a ~160s recovery time for Raft election over UHF. However, the analysis assumes a standard Slotted ALOHA model. In a "thundering herd" scenario where 100 nodes wake up simultaneously after a coordinator failure, the collision probability will be near 100% initially.
    *   **Why it matters:** If the backoff window ($W$) isn't sized correctly for $N=100$, the channel could collapse, extending recovery indefinitely. The estimate of 160s seems optimistic without specifying the backoff algorithm (e.g., Binary Exponential Backoff).
    *   **Remedy:** Briefly specify the backoff mechanism assumed for the UHF election (e.g., "Slotted ALOHA with BEB, $W_{min}=32$"). If a simple fixed probability was used, acknowledge this as a lower-bound estimate.

3.  **Spatial Reuse ($R=3$) Interference Margin**
    *   **Issue:** Section IV-A.1 claims $R=3$ is sufficient based on a single-interferer calculation (26 dB C/I). In a hexagonal lattice, a cluster is surrounded by 6 first-tier co-channel interferers.
    *   **Why it matters:** The aggregate interference could degrade C/I by ~8 dB ($10 \log_{10} 6$), potentially violating the 20 dB requirement.
    *   **Remedy:** Update the calculation to include aggregate interference from at least the nearest tier of clusters ($C/I_{agg}$). If $R=3$ fails this check, suggest $R=4$ or $R=7$ and adjust the fleet-level capacity claims accordingly.

---

## Minor Issues

1.  **Clarification of $\alpha_{RX}$:** In Table I, $\alpha_{RX}$ is defined as a "Computed output." However, in some equations (e.g., Eq. 7), it appears as a variable determining stagger. Please clarify in the text of Section IV-A that $\alpha_{RX}$ is fixed by the ingress volume and PHY rate, and thus dictates the *remaining* time for egress, which in turn dictates the stagger $L_{cmd}$.
2.  **Table III Footnote:** Footnote 'b' mentions "single-threaded." Given modern SoCs on CubeSats, is this necessary? It's fine as a conservative bound, but perhaps clarify that parallel processing would only improve the margin.
3.  **Figure 2 (Architecture):** The caption mentions "Labels: aggregation ratios," but the figure description in the text implies a logical flow. Ensure the visual labels clearly correspond to the $k_c$ and $k_r$ parameters defined in Table I.
4.  **Typos:** Section IV-J, "Doppler budget": "$\pm 1.67 \times$ the symbol rate" seems high for 30 kbps (50 kHz Doppler). 50 kHz is indeed > 30 kHz. Please confirm the acquisition preamble length (in bits) is sufficient to sweep this range.

---

## Overall Recommendation
**Recommendation: Accept with Minor Revisions**

This is a high-quality, rigorous manuscript that makes a substantial contribution to the field of space systems engineering. The derivation of the $\gamma$ parameter from CCSDS standards and the two-test feasibility framework provide a concrete "handbook" for systems engineers sizing swarm constellations. The paper moves beyond generic networking assumptions to address the specific constraints of orbital mechanics and space-grade hardware.

The strengths of the paper lie in its actionable design equations (Section V-C) and the clear separation of byte-level logic from physical-layer timing. The "Major Issues" identified above are primarily requests for tighter boundary conditions (interference margins and fading coherence) rather than fundamental flaws in the methodology. Addressing these will make the design guidelines even more robust for future mission planners.

---

## Constructive Suggestions

1.  **Enhance the "Design Equations" Section:** Consider adding a small lookup table or graph for "Maximum Cluster Size ($k_c$) vs. PHY Rate" for a fixed $T_c=10s$. This would allow a reader to immediately see the scalability limit (e.g., "If I have 35 kbps, I can support up to 140 nodes").
2.  **Refine the Abstract:** The abstract is dense. Explicitly stating "We recommend a minimum 35 kbps PHY rate for 100-node clusters to accommodate CCSDS framing and ARQ margins" would make the takeaway even clearer.
3.  **Future Work - Optical Handoff:** You mention optical ISL for state transfer. A sentence in the discussion about the mechanical slew time constraints for optical links during coordinator switching would add depth, as this is often the bottleneck in hybrid RF/Optical architectures.