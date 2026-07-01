---
paper: "02-swarm-coordination-scaling"
version: "cj"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-03-02"
recommendation: "Major Revision"
---

# Peer Review: "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version CJ)

---

## 1. Significance & Novelty
**Rating: 3 (Adequate)**

The paper addresses a genuine gap: no prior work provides closed-form parametric sizing for hierarchical coordination at the $10^3$–$10^5$ node scale with byte-level traffic accounting. The two-layer feasibility framework (byte budget + TDMA airtime) is a useful conceptual contribution, and the generalized $\gamma$ expression (Eq. 14) has clear practitioner value. However, the novelty is tempered by the fact that the individual analytical components (M/D/1 queueing, GE channel models, AoI under geometric reporting, TDMA slot budgeting) are well-established. The contribution is primarily one of *integration and parameterization* rather than fundamental methodological advance. The paper would benefit from a more explicit positioning statement acknowledging this—the value is in the complete sizing workflow (Algorithm 1), not in any single analytical result.

## 2. Methodological Soundness
**Rating: 3 (Adequate)**

The three-layer verification hierarchy (analytical → DES → slot-level/packet-level) is well-structured, and the authors are commendably transparent about what each tool can and cannot demonstrate. Several methodological concerns remain:

- The DES is cycle-aggregated and message-layer only; its agreement with closed-form means is tautological (acknowledged by the authors as Tier 1 verification). The distributional tail analysis (Fig. 7) is the genuine incremental contribution of the DES, but the paper devotes disproportionate space to mean-value verification.
- The slot-level simulator and packet-level simulator share the same underlying timing model; their "cross-model" agreement is less independent than presented. The packet-level simulator *derives* $\gamma$ from CCSDS parameters and then feeds it into the same equations—this is parameter anchoring, not independent validation.
- The GE channel model is parameterized from physical reasoning (structural shadowing geometry) rather than measurement data. While the sensitivity sweep partially mitigates this, the paper should more prominently flag that the *absolute* recovery times (P95 = 4 cycles) are illustrative, not predictive.

## 3. Validity & Logic
**Rating: 4 (Good)**

The internal logic is generally sound and self-consistent. Key improvements in this version:

- The campaign duty factor $d$ now properly contextualizes the stress-case ($\eta_S \approx 46\%$) as a continuous-duty upper bound, with worked examples anchoring $d$ in realistic mission phases. This is a significant improvement.
- The $\gamma$ unification at 0.760 (replacing the earlier 0.85) is consistently applied throughout, with clear Model S/Model C labeling. I verified several cross-references and found no inconsistencies.
- The stress-case is now explicitly labeled as $d = 1$ (continuous-duty bound, $<$1% of operational time), with routine operations at $\eta \approx 5$–10%. This framing is appropriate.

One logical concern: the paper claims command traffic is "topology-invariant" but then shows distributed consensus overhead ranges from 2.8%–31% (Eq. 7). The topology-invariance claim should be more carefully scoped—it holds only under centralized broadcast semantics, which is stated but could be more prominent.

## 4. Clarity & Structure
**Rating: 3 (Adequate)**

The paper is comprehensive but *excessively long* for a journal article. At approximately 12,000+ words of body text plus extensive tables and figures, it reads more like a technical report than a focused journal contribution. Specific concerns:

- The notation table (Table I) is helpful but incomplete—several symbols used later ($\alpha_{\text{RX}}$, $L_{\text{cmd}}$, $q$) are defined inline but not in the table. (Update: I see $\alpha_{\text{RX}}$, $q$, and $L_{\text{cmd}}$ are now in Table I. Good.)
- Section IV is sprawling (A through J) and would benefit from consolidation. The roadmap paragraph helps but cannot fully compensate for structural complexity.
- The paper oscillates between presenting a *general framework* and a *specific instantiation* ($k_c = 100$, $T_c = 10$ s, 1 kbps). While the authors flag this distinction, readers may lose track of which results are general and which are parameter-specific.
- Several important caveats are buried in footnotes or parenthetical remarks rather than being stated prominently (e.g., the 0.005 rounding discrepancy in $\gamma$, the independence assumption for compound failure probability).

## 5. Ethical Compliance
**Rating: 5 (Excellent)**

Exemplary transparency: open-source code with tagged release, full parameter tables, explicit AI disclosure with clear delineation of AI-assisted vs. human-generated content, and honest acknowledgment of validation gaps. The V&V tier framework with bold-faced caveats about absent external validation is a model for responsible reporting.

## 6. Scope & Referencing
**Rating: 4 (Good)**

The literature coverage is broad and appropriate for the target journal. CCSDS standards, DVB-RCS2, network calculus, AoI theory, and swarm robotics are all properly cited. The paper correctly identifies the gap between swarm robotics (10–100 agents) and constellation management ($\sim$10,000 nodes). Minor gaps: no citation of ESA's OPS-SAT or recent autonomous constellation management demonstrations; the Iridium NEXT reference [19] is from 1995 and predates the NEXT constellation by two decades.

---

## Major Issues

**1. The DES verification provides limited value beyond confirming its own equations.**

The paper acknowledges this (Section III-A, "code verification, not model validation") but then devotes substantial space to DES results that reproduce analytical means to $<$0.1%. The genuine DES contribution—distributional tail analysis under stochastic campaigns (Fig. 7, Section IV-F)—deserves more prominence, while the mean-value verification should be compressed to a single paragraph with a summary table.

*Why it matters:* Readers may overestimate the validation strength of the framework. The current presentation risks conflating implementation correctness with model fidelity.

*Remedy:* Restructure Section IV-F to lead with the distributional/buffer results. Reduce mean-value verification to: "DES reproduces all closed-form means to $<$0.1% (30 MC replications); see supplementary material for detailed comparison." Move the scale-invariance verification to an appendix or supplementary file.

**2. The packet-level validation (Section IV-J) provides parameter anchoring, not independent validation.**

The packet-level simulator derives $\gamma$ from CCSDS framing parameters and then feeds this value into the same sizing equations used by all other tools. This is valuable for *anchoring* $\gamma$ in standards, but it is not an independent check on the framework's predictions. The cross-model consistency (Table IX) is expected by construction once $\gamma$ is shared.

*Why it matters:* The claim map (Table VII) lists packet-level results under "Tier 2 (Cross-Model)" alongside the slot-level simulator, but the two provide different types of evidence. The slot-level simulator reveals genuinely new interactions (ARQ × TDMA coupling); the packet-level simulator provides parameter derivation.

*Remedy:* Relabel the packet-level contribution as "parameter anchoring" rather than "cross-model validation" in Table VII. Add a sentence explicitly stating: "The packet-level simulator anchors $\gamma$ in CCSDS standards but does not independently validate the sizing equations, which are shared across all tools."

**3. Absence of any external validation limits the paper's predictive claims.**

The paper is transparent about this (bold-faced caveat in Section III-A), but the gap is significant for a journal targeting aerospace practitioners. No comparison with operational constellation data (even at the level of published Starlink/Iridium operational statistics), no NS-3 or hardware-in-the-loop results, and no ISL channel measurements.

*Why it matters:* Without Tier 3 validation, the framework's utility is limited to preliminary design sizing. The paper should explicitly state this scope limitation in the abstract and conclusion.

*Remedy:* (a) Add to the abstract: "The framework is validated internally (code verification and cross-model consistency) but lacks external validation against operational ISL data or high-fidelity network simulation; results should be treated as preliminary design estimates." (b) If any publicly available ISL statistics exist (e.g., from Iridium NEXT publications or ESA ISL demonstrations), even a qualitative comparison would strengthen the paper significantly.

**4. The generalized $\gamma$ expression (Eq. 14) conflates time-domain and bit-domain quantities.**

Equation 14 mixes payload bytes ($S$), framing bits ($O_{\text{frame}}$), time quantities ($T_{\text{guard}}$, $T_{\text{acq}}$ in ms), and PHY rate ($R_{\text{PHY}}$ in bps), with a $10^{-3}$ conversion factor. While dimensionally correct, this is error-prone for practitioners. The time-domain form (Eq. 15) is cleaner and should be presented as the primary expression.

*Why it matters:* A practitioner-facing equation should minimize unit-conversion errors.

*Remedy:* Present Eq. 15 (time-domain) as the primary form; relegate Eq. 14 to an equivalent alternative. Add a worked example with explicit units at each step (partially done in the text below Eq. 15, but could be more systematic).

**5. The 0.005 discrepancy in $\gamma$ ($0.760$ vs. $0.765$) undermines confidence in the precision claimed elsewhere.**

The footnote explains this as intermediate rounding, but a 0.7% discrepancy in the key parameter driving the feasibility boundary is non-trivial when the margin at 30 kbps is only 2.9%. If the rounding convention changes, the feasibility conclusion could shift.

*Why it matters:* The entire TDMA feasibility analysis hinges on $\gamma$; inconsistency in its computation, even at the 0.7% level, erodes trust in the precision of the margin analysis.

*Remedy:* Adopt a single computation method (preferably the time-domain Eq. 15 with full precision) and carry it through consistently. Report $\gamma$ to 3 significant figures from a single calculation path. If the multiplicative decomposition (Table V) introduces rounding error, note this but use the time-domain value as authoritative.

---

## Minor Issues

1. **Table I notation completeness:** $f_{\text{RF}}$ and $F$ are defined in Table I but $R_{\text{FEC}}$, $O_{\text{frame}}$, and $T_{\text{payload}}$ (used in Eqs. 14–15) are not. Add these or reference the equations where they are defined.

2. **Reference [19] (Iridium):** The 1995 Maine et al. reference describes the original Iridium architecture, not Iridium NEXT (launched 2017–2019). The text references "Iridium NEXT crosslink statistics" in Section IV-C but cites the 1995 paper. Either find an Iridium NEXT reference or remove the NEXT qualifier.

3. **Section III-B-3 (Global-State Mesh):** The claim "$\sim$73 MB/node/cycle" at $N = 10^5$ should show the calculation explicitly (e.g., $10^5 \times 256$ B $\times$ gossip rounds).

4. **Table III (Simulation Parameters):** The collision avoidance rate ($10^{-4}$/node/s) footnote says "screening notifications, not autonomous maneuver commands," but the message model uses 128 B "collision avoidance msg" without clarifying whether this is a screening alert or a maneuver command. Clarify.

5. **Eq. 6 (unicast stagger):** The floor function $\lfloor q \cdot k_c \rfloor$ in Eq. 7 should arguably be $\lceil q \cdot k_c \rceil$ (ceiling) for conservative sizing. The $(1 + \lfloor \cdot \rfloor)$ construction is non-standard; explain the +1 term (coordinator's own command slot?).

6. **Fig. 4 (phase stagger):** The caption says "phase staggering eliminates drops at $\sim$25 kbps vs. 50 kbps under random phase," but the figure is not shown in the manuscript text. Verify the figure file exists and is correctly referenced.

7. **Section IV-B (AoI):** The geometric inter-report model assumes memoryless reporting decisions. If exception reporting is triggered by threshold crossings (e.g., state deviation exceeds tolerance), the inter-report distribution is not geometric. Acknowledge this assumption.

8. **Algorithm 1, Line 7:** The screening heuristic ($\eta_{\text{total}}/\gamma < 0.50$) is followed by "still evaluate Layer 2 below," but the algorithm structure suggests the heuristic branch could be skipped. Make the control flow explicit (the heuristic is informational only; Layer 2 is always evaluated).

9. **Section V-B (Limitations):** "J2 perturbation analysis" is mentioned but no orbital mechanics simulation is described in Section III. Clarify whether this is an analytical estimate or a separate simulation.

10. **Typographical:** "${\sim}7$~s at $N = 10^5$" (Section III-A) and "${\sim}0.2$--$7$~s per run" (Section III-D) are inconsistent—clarify the range.

11. **Table VI (Feasibility Summary):** The $\eta_{\text{total}}/\gamma$ column header should specify which $\gamma$ is used ($\gamma_{30} = 0.745$).

12. **Section IV-A:** "Fleet-wide TDMA cost is 0.28 kbps/node (1% coordinators at $k_c = 100$)"—this calculation is unclear. Show: $C_{\text{TDMA}} / k_c = 26.7 / 100 = 0.267$ kbps/node, or explain the 0.28 figure.

---

## Overall Recommendation
**Recommendation: Major Revision**

This is a substantial and carefully constructed paper that addresses a genuine gap in the literature—parametric sizing for hierarchical coordination in large autonomous space swarms. The two-layer feasibility framework, the generalized $\gamma$ expression, the campaign duty factor parameterization, and the GE sensitivity sweep are all useful contributions. The authors demonstrate commendable transparency about validation limitations, and the open-source release with tagged datasets sets a high standard for reproducibility.

However, the paper suffers from three significant weaknesses that prevent acceptance in its current form. First, the validation architecture, while internally consistent, is largely self-referential: the DES confirms its own equations, the packet-level simulator anchors parameters rather than independently validating predictions, and no external validation exists. The paper needs to more clearly delineate what is *verified* (implementation correctness) from what is *validated* (model fidelity), and scope its claims accordingly—particularly in the abstract and conclusion. Second, the manuscript is excessively long and structurally complex for a journal article; consolidation of Section IV and reduction of mean-value verification reporting would significantly improve readability. Third, the $\gamma$ computation inconsistency (0.760 vs. 0.765), while small, is concerning given that the feasibility boundary depends critically on this parameter with only 2.9% margin at the minimum viable PHY rate.

The strengths—particularly the complete sizing workflow (Algorithm 1), the practitioner-facing $\gamma$ calibration checklist, the worked campaign duty-factor examples, and the honest validation gap disclosure—make this a paper worth revising. With tighter scoping of claims, manuscript compression, and resolution of the $\gamma$ computation path, this could become a valuable reference for the constellation design community.

## Constructive Suggestions (ordered by impact)

1. **Tighten validation claims throughout.** Replace "validated" with "verified" for all Tier 1 results. Reserve "validated" for Tier 2 cross-model results and explicitly note the absence of Tier 3. Modify abstract and conclusion accordingly.

2. **Compress the manuscript by ~25%.** Consolidate Sections IV-F (DES distributional) and IV-G (topology comparison) into a single section. Move mean-value verification details to supplementary material. Reduce the coordinator failure transient discussion (Section III-B-2) to essential results.

3. **Resolve the $\gamma$ computation path.** Adopt the time-domain calculation (Eq. 15) as authoritative, carry full precision, and reconcile with the multiplicative decomposition. Report a single $\gamma_{C,24}$ value with stated precision.

4. **Add a "Limitations of Internal Validation" subsection** (or expand Section V-A) that explicitly lists what failure modes the framework *cannot* detect without external validation: MAC contention collapse, antenna scheduling conflicts, correlated multi-node failures, and real ISL channel statistics.

5. **Strengthen the practitioner value of Eq. 14/15** by providing a second worked example with different parameters (e.g., Ka-band ISL, rate-1/2 LDPC, 10 ms acquisition) to demonstrate generality.

6. **Consider splitting the paper** into a focused journal article (framework + key results + Algorithm 1) and a companion technical report (full DES details, sensitivity sweeps, all tables). This would improve the journal article's impact while preserving the comprehensive analysis.