---
paper: "02-swarm-coordination-scaling"
version: "ck"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-03-03"
recommendation: "Unknown"
---

# Peer Review: "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version CK)

---

## 1. Significance & Novelty
**Rating: 3 (Adequate)**

The paper addresses a genuine gap: no prior work provides closed-form parametric sizing equations for hierarchical coordination architectures at the $10^3$–$10^5$ node scale with byte-level traffic accounting. The two-layer feasibility framework (byte budget + TDMA airtime) is a useful conceptual contribution, and the generalized $\gamma$ expression (Eq. 14) has clear practitioner value. However, the novelty is tempered by the fact that the individual analytical components (M/D/1 queueing, Gilbert-Elliott channels, AoI under geometric sampling, TDMA slot budgeting) are well-established. The contribution is primarily in their *assembly* into a coherent sizing workflow rather than in new analytical methods. The paper would benefit from a clearer articulation of what design decisions this framework enables that were previously impossible or impractical.

## 2. Methodological Soundness
**Rating: 3 (Adequate)**

The analytical framework is internally consistent and carefully constructed. The three-layer feasibility workflow (byte budget → rate/efficiency translation → TDMA superframe timing) is logically sound. However, several methodological concerns remain:

- The DES operates at message-layer granularity and reproduces its own input equations by construction. The authors acknowledge this (Tier 1 verification), but the DES still occupies substantial manuscript real estate relative to its incremental contribution (distributional tails and buffer sizing). The tail analysis in Fig. 7 is genuinely useful but could be presented more concisely.
- The slot-level simulator and packet-level simulator share the same sizing equations as the analytical model. Cross-model "consistency" between tools implementing the same equations is expected, not validating. The ARQ×TDMA coupling finding (Table VI, 52.7% deadline misses) is the one genuinely emergent result from the slot-level simulator—this deserves more prominence.
- The GE channel parameterization is acknowledged as illustrative, but the paper spends considerable space on a single operating point ($p_{BG}=0.50$, $p_B=0.90$) before revealing the sensitivity sweep. The sensitivity sweep (Fig. 5b) is the real contribution; the specific numbers should be de-emphasized.

## 3. Validity & Logic
**Rating: 4 (Good)**

The internal logic is generally tight. Specific strengths:

- The campaign duty factor $d$ adequately addresses workload realism. The decomposition $\eta = \eta_0 + d \cdot \eta_{\text{cmd}}$ with worked examples (orbit-raising, station-keeping, collision avoidance) and the practitioner recipe for estimating $d$ and $q$ are well done. The empirical anchoring to ESA maneuver cadence and Starlink orbit-raising windows is a welcome addition.
- The gamma unification is consistently applied: $\gamma_{C,24} = 0.761$ and $\gamma_{C,30} = 0.745$ are used throughout for all feasibility claims. Model S ($\gamma_S = 0.949$) is clearly labeled as an upper bound. I found no instances of inconsistent $\gamma$ usage.
- The stress-case ($\eta_S \approx 46\%$) is properly contextualized as a continuous-duty upper bound ($d=1$, $<1\%$ of operational time), with routine operations at $\eta \approx 5$–$10\%$.
- The screening heuristic ($\eta_{\text{total}}/\gamma < 0.50$) is appropriately caveated as non-binding and informational only.

One logical concern: the paper claims command traffic is "topology-invariant" but then derives $\eta_{\text{consensus}}$ (Eq. 5) showing it is architecture-dependent. The resolution (topology-invariant *under centralized broadcast semantics*) is stated but could be clearer in the abstract and conclusion.

## 4. Clarity & Structure
**Rating: 3 (Adequate)**

The paper is comprehensive but excessively long and dense. At its current length, it reads more like a technical report than a journal article. Specific issues:

- The manuscript is approximately 12,000+ words of body text plus extensive tables and figures. For IEEE T-AES, this is at the upper limit. Several sections could be condensed without loss of substance.
- The notation table (Table I) is helpful but incomplete—some symbols appear in the text before being defined (e.g., $\alpha_{\text{RX}}$ is used in the abstract but its derivation comes much later).
- The paper oscillates between presenting general framework equations and specific instantiation results without always clearly signaling which is which. The "Instantiation parameters" note at the start of Section IV helps but is insufficient.
- Many important caveats and qualifications are embedded in footnotes or parenthetical remarks, making them easy to miss. For example, the fact that hierarchical coordination is *suspended* during RF-backup (a critical architectural decision) is buried in Section III-B.2.
- Algorithm 1 is a useful synthesis but appears late in the paper (Section V). Moving it earlier (or at least forward-referencing it) would improve readability.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**

Exemplary transparency: open-source code with tagged release, full parameter tables, explicit AI disclosure with clear scope delineation (ideation vs. results vs. editing), honest acknowledgment of validation gaps, and clear labeling of all results as "preliminary design estimates." The claim map (Table IX) is an unusually rigorous self-assessment of evidence quality.

## 6. Scope & Referencing
**Rating: 4 (Good)**

The literature coverage is broad and appropriate, spanning constellation operations, swarm robotics, distributed systems, queueing theory, AoI, and CCSDS standards. The DVB-RCS2 reference for demand-assigned TDMA is a good addition. Two gaps: (1) no reference to the extensive literature on TDMA scheduling in terrestrial sensor networks (e.g., TSCH in IEEE 802.15.4e), which faces analogous slot-efficiency challenges; (2) the network calculus reference (Le Boudec) is mentioned but not applied—either apply it or remove the forward reference.

---

## Major Issues

**1. The DES verification provides limited value beyond confirming its own equations; the paper over-invests in internal consistency at the expense of external anchoring.**

*Why it matters:* Four tools (analytical, DES, slot-sim, packet-sim) all implement the same sizing equations. Their agreement to $<0.1\%$ is a tautology, not validation. The paper acknowledges this (Section V-A) but still devotes ~30% of the results section to DES-analytical comparisons. Readers may mistake internal consistency for model validation.

*Remedy:* (a) Reduce DES verification to a single paragraph confirming code correctness. (b) Elevate the genuinely new DES contributions (distributional tails, buffer sizing under correlated campaigns) to primary results. (c) Clearly separate "verification" (does the code implement the equations correctly?) from "validation" (do the equations predict reality?) throughout, not just in Section V-A. (d) Consider adding even a simple NS-3 experiment (e.g., 10-node TDMA with CCSDS-like framing) to provide one Tier-3 data point.

**2. The packet-level validation (Section IV-J) does not provide genuinely independent validation.**

*Why it matters:* Section IV-J is presented as "standards-grounded parameter derivation" and positioned as Tier-2 evidence. However, it derives $\gamma$ from CCSDS framing parameters and then feeds this $\gamma$ back into the same sizing equations used by all other tools. The "cross-model consistency" (Table XII) is therefore expected by construction. The packet-level simulator's value is in *anchoring* $\gamma$ to a physical standard, not in *validating* the sizing framework.

*Remedy:* Reframe Section IV-J explicitly as "parameter anchoring" rather than "validation." State clearly: "The packet-level simulator determines $\gamma$ from standards; it does not independently validate the sizing equations, which are shared across all tools." This is partially done in Table IX footnote $\ddagger$ but should be in the main text.

**3. The manuscript length and density exceed what is appropriate for a journal article.**

*Why it matters:* The paper attempts to be simultaneously a tutorial, a design handbook, and a research contribution. While each component has value, the combination produces a manuscript that is difficult to navigate and whose core contributions are diluted.

*Remedy:* (a) Move the worked examples (Ka-band ISL, $\gamma$ calibration checklist), practitioner recipes, and mission-phase mapping tables to an online supplementary document. (b) Consolidate Tables IV, V, VII, VIII, and X into fewer tables. (c) Reduce the coordinator failure transient analysis (thundering herd, back-off, compound probability) to essential results only—the current treatment is thorough but disproportionate to its importance.

**4. The GE channel model lacks any empirical grounding for ISL applications, and the paper's treatment of this gap is inconsistent.**

*Why it matters:* The paper correctly notes that "no ISL-specific GE measurement data are available in the open literature" and that the Lutz et al. framework was developed for land-mobile channels. Yet it proceeds to derive specific numeric results (P95 = 4 cycles, 27.1% intra-cycle recovery) that are presented with precision suggesting confidence. The geometric justification for structural shadowing (Section IV-C) is a reasonable physical argument but is not a substitute for measurement.

*Remedy:* (a) Present all GE-derived numbers as "at the illustrative operating point" consistently (partially done but not uniformly). (b) Make the sensitivity sweep (Fig. 5b) the *primary* result and the specific numbers secondary. (c) Add a prominent statement that the 4-cycle P95 result could be 3× higher or lower depending on actual ISL channel statistics.

**5. The three-layer feasibility framework conflates a screening heuristic with a design criterion in ways that may confuse practitioners.**

*Why it matters:* The paper defines three steps (byte budget, rate/efficiency translation, TDMA superframe timing) but the middle step ($\eta_{\text{total}}/\gamma$) is described as both a "screening heuristic" and part of the feasibility workflow. The 0.50 threshold is empirically motivated from a limited sweep. A practitioner following Algorithm 1 might skip Layer 2 based on the heuristic, despite the paper's warnings.

*Remedy:* (a) Remove the screening heuristic from Algorithm 1 entirely, or move it to a remark/note outside the algorithm. The algorithm should contain only necessary and sufficient conditions. (b) Alternatively, prove that $\eta_{\text{total}}/\gamma < 0.50$ is a *sufficient* condition for Layer-2 feasibility (which would require showing it implies $T_{\text{ing}} + T_{\text{egr}} \leq T_c$ for all valid parameter combinations), or remove the claim.

---

## Minor Issues

1. **Abstract length:** The abstract exceeds 250 words (IEEE T-AES guideline). The parenthetical caveats about ARQ infeasibility and sensitivity sweeps should be moved to the body.

2. **Eq. 1 ($M_{\text{total}}$):** The third term assumes a fixed number of regional coordinators $n_r$; this should be stated explicitly in the equation context, not just in Table III.

3. **Table II, footnote a:** "AoI depends on $p_{\text{exc}}$ and $T_c$, not $C_{\text{node}}$"—this is true only when the byte budget is not binding. At very low $C_{\text{node}}$, queue drops would increase AoI. Clarify the assumption.

4. **Section III-B.2, "Hierarchical coordination suspension":** This critical architectural decision (hierarchical coordination is suspended during RF-backup) should appear much earlier—ideally in the introduction or system model overview. It fundamentally changes the interpretation of the RF-backup analysis.

5. **Eq. 14 ($\gamma$ general):** The denominator mixes bits and time-domain quantities via the $10^{-3}$ conversion factor. A purely time-domain formulation (Eq. 15) is cleaner; consider making Eq. 15 the primary form and Eq. 14 the alternative.

6. **Table VI:** The "GE+Exc" column header is cryptic. Expand to "GE, $M_r=0$, exception telemetry" or add a clearer footnote.

7. **Fig. 3 (phase stagger):** The figure is referenced but the description suggests it shows coordinator drops vs. link capacity. Confirm the x-axis units and range are legible at column width.

8. **Section IV-E, "Empirical anchoring":** The ESA maneuver cadence (~10/yr per spacecraft) is for a fleet of ~30 spacecraft, not a mega-constellation. The scaling of conjunction frequency with fleet size ($\propto N^2$ for random encounters) should be acknowledged.

9. **Eq. 5 ($\eta_{\text{consensus}}$):** The formula assumes all quorum messages traverse the shared coordination channel. In practice, Raft implementations pipeline votes; the actual byte count depends on the implementation. Note this assumption.

10. **Section III-A, "runtime ~7 s at $N = 10^5$":** This is impressively fast but raises the question of whether the simulation is doing enough work. Clarify that the fast runtime is due to vectorized cycle-aggregated updates, not model simplification.

11. **Reference [1] (Starlink):** An FCC filing supplemented by a non-archival personal website is weak sourcing for the paper's motivating example. Consider citing McDowell's peer-reviewed publications or the FCC filing alone.

12. **Table I:** $f_{\text{RF}}$ and $F$ are defined but used only in Eq. 6 and surrounding text. Consider moving these to local definitions rather than the global notation table.

13. **"Version CK" in the title metadata:** Ensure version identifiers are removed for submission.

---

## Overall Recommendation
**Recommendation: Major Revision**

This manuscript presents a carefully constructed parametric sizing framework for hierarchical coordination in large space swarms—a topic of growing practical relevance as constellation sizes increase. The two-layer feasibility decomposition (byte budget + TDMA airtime), the generalized $\gamma$ expression anchored in CCSDS standards, and the campaign duty factor $d$ are genuine contributions that would serve the community. The transparency of the validation gap acknowledgment and the open-source data availability are commendable and set a good example.

However, the paper suffers from three interrelated problems that must be addressed before publication. First, the manuscript is substantially overlength and attempts to serve simultaneously as a research paper, design handbook, and tutorial—diluting its core contributions. Second, the extensive internal verification (four tools confirming the same equations) is presented with a weight that risks being mistaken for external validation; the paper needs to more sharply distinguish between "the code is correct" and "the model predicts reality." Third, the GE channel results are presented with a specificity that belies the complete absence of ISL channel measurements; the sensitivity sweep should be elevated to the primary result.

The most impactful revision would be a significant reduction in length (targeting ~8,000 words of body text) by moving practitioner recipes, worked examples, and detailed failure-mode analyses to supplementary material, while sharpening the presentation of the genuinely novel results: the feasibility framework structure, the ARQ×TDMA coupling finding, the distributional tail analysis under correlated campaigns, and the generalized $\gamma$ expression. With these changes, the paper would make a solid contribution to IEEE T-AES.

---

## Constructive Suggestions
*(Ordered by impact)*

1. **Restructure for clarity and length:** Create a 2-page online supplement containing: the $\gamma$ calibration checklist, Ka-band worked example, mission-phase mapping (Table VIII), margin inventory (Table VII), thundering herd analysis, and coordinator failure transient details. This alone would reduce the manuscript by ~25%.

2. **Elevate the ARQ×TDMA coupling as the key simulation finding:** The 52.7% deadline miss rate at 24 kbps with $M_r=1$ (Table VI) is the one result that *could not* have been obtained from the analytical model alone. Make this the centerpiece of the simulation contribution, not the $<0.1\%$ mean agreement.

3. **Add one external validation data point:** Even a minimal NS-3 experiment (10-node TDMA cluster, CCSDS-like framing, measured $\gamma$ vs. predicted) would transform the validation story from "zero external evidence" to "one anchoring point." This is feasible within a revision cycle.

4. **Reframe the GE analysis around the sensitivity sweep:** Present Fig. 5b first, then note the illustrative operating point. This correctly positions the framework as a design tool rather than a prediction.

5. **Simplify Algorithm 1:** Remove the screening heuristic (lines 6-8) from the algorithm. Present it as a separate remark. The algorithm should contain only the two binding feasibility checks (byte budget and superframe timing).

6. **Add a "quick-start" summary figure:** A single figure showing the complete sizing workflow (inputs → Layer 1 check → $\gamma$ computation → Layer 2 check → design point) would dramatically improve accessibility for practitioners.

7. **Discuss the $C_{\text{node}} = 1$ kbps assumption more critically:** This is the single most consequential parameter choice, yet it receives relatively little justification beyond "conservative allocation for RF backup." A sensitivity analysis showing how the feasibility boundary shifts with $C_{\text{node}} \in \{0.5, 1, 2, 5\}$ kbps would strengthen the framework's generality.