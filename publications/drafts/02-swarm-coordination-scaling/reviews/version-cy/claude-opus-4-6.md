---
paper: "02-swarm-coordination-scaling"
version: "cy"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-03-05"
recommendation: "Unknown"
---



# Peer Review: "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version CY)

---

## 1. Significance & Novelty
**Rating: 3 (Adequate)**

The paper addresses a genuine gap: closed-form parametric sizing for hierarchical coordination at the 10³–10⁵ node scale with byte-level traffic accounting. The two-test feasibility framework (byte budget + TDMA airtime) is a useful conceptual contribution, and the rate-ladder methodology from information-rate through PHY selection is practically oriented. However, the novelty is tempered by several factors: (a) the core equations are relatively straightforward traffic accounting and TDMA slot arithmetic—the intellectual contribution lies more in systematic assembly than in new analytical techniques; (b) the absence of any external validation means the practical significance remains speculative; (c) the paper's own analysis shows that at ≥10 kbps per-node budgets, the entire TDMA analysis becomes non-binding, limiting the regime where these results matter to a narrow 1–10 kbps window. The campaign duty factor and γ parameterization are useful engineering contributions but not methodologically novel.

## 2. Methodological Soundness
**Rating: 3 (Adequate)**

The three-layer verification structure (analytical, DES, slot-sim) is clearly described, and the authors are commendably transparent about the tautological nature of the DES verification. The CCSDS-grounded γ derivation is well-executed. However, several methodological concerns persist:

- The DES is cycle-aggregated and shares equations with the analytical model, so agreement is definitional. The distributional analysis (buffer sizing) is the sole non-trivial DES output, but it depends on an assumed ON/OFF Markov campaign process that is itself unvalidated.
- The GE channel model is presented as a "what-if design tool," which is appropriate framing, but the default parameters (p_BG = 0.50, p_B = 0.90) are acknowledged as illustrative with no ISL measurements. The sensitivity curves partially mitigate this, but the specific numeric claims (27% intra-cycle recovery, P95 = 4 cycles) are parameter-dependent artifacts.
- The M/D/1 centralized baseline and O(N²) mesh bound are intentionally simplistic reference points, not competing architectures—this is stated but could mislead readers into thinking the hierarchical approach is being compared against realistic alternatives.

## 3. Validity & Logic
**Rating: 4 (Good)**

The internal logic is generally sound and self-consistent. The paper has clearly improved across versions in several areas:

- The campaign duty factor (d) now properly contextualizes the stress-case η_S ≈ 46% as a continuous-duty upper bound occurring <1% of operational time. The yearly mixture calculation (η̄ = 5.6%) and mission-phase mapping (Table 7) are convincing.
- The gamma unification around 0.76 (CCSDS-derived, replacing the earlier 0.85) is consistently applied throughout. I verified that Tables 4, 5, 6, 8, 9, and Algorithm 1 all use Model C values. The rate-dependent γ formulation (Eq. 14) is correctly derived and the "rate paradox" (γ decreasing with R_PHY due to fixed-time overheads) is well-explained.
- The stress-case is now clearly labeled as a continuous-duty upper bound with proper operational context.

One logical concern: the paper claims topology-invariance of η_cmd under centralized command generation, but this holds only for broadcast semantics. Under unicast (q > 0), the stagger L_cmd introduces a scheduling dependency that is topology-sensitive (coordinator must track per-node state). This is partially acknowledged but understated.

## 4. Clarity & Structure
**Rating: 3 (Adequate)**

The paper is dense but generally well-organized. The roadmap at the start of Section IV and the boxed feasibility framework are helpful. The rate ladder (Table 4) and claim map (Table 10) are excellent organizational devices. However:

- The paper is extremely long for a journal article and suffers from over-specification. Many caveats, footnotes, and parenthetical qualifications—while individually justified—collectively impede readability. The manuscript reads more like a technical report than a journal paper.
- The dual model system (Model S vs. Model C) adds complexity. While the authors are careful to label which model is used where, Model S appears only as a comparison bound and could be relegated to an appendix without loss.
- Some notation is introduced but used inconsistently or redundantly (e.g., α_RX is defined as "derived" but appears as both an input and output in different contexts).
- Figure quality cannot be assessed from LaTeX source, but the descriptions suggest appropriate content.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**

Exemplary transparency: the AI disclosure is specific (models named, scope of use defined), the validation gap is prominently stated in the abstract, the claim map (Table 10) explicitly marks absent external validation, and the data availability statement includes repository tags and computational environment. The V&V tier structure (IEEE 1012) is properly applied. The paper does not overclaim.

## 6. Scope & Referencing
**Rating: 3 (Adequate)**

The reference list covers the major relevant areas (CCSDS standards, swarm robotics, constellation management, AoI theory, distributed consensus). The DVB-RCS2 comparison for γ plausibility is a good addition. However:

- Several references are non-archival (Amazon Kuiper overview, DARPA program pages, DOD fact sheets). While understandable for programmatic context, these weaken the scholarly foundation.
- The paper does not engage with recent work on LEO ISL channel characterization (e.g., measurements from Starlink or similar systems that may have appeared in IEEE Aerospace Conference proceedings).
- Network calculus (Le Boudec) is cited but not used; the paper could benefit from actually applying deterministic service curve analysis as a complement to the mean-value approach.
- The LEACH comparison is superficial—LEACH's energy-driven cluster-head rotation has limited relevance to the fixed-coordinator model here.

---

## Major Issues

**1. The DES verification provides negligible independent value, yet occupies substantial manuscript space.**

The authors acknowledge (Section III-A, Section IV-F) that DES mean-value agreement is "by construction" and that the distributional analysis is the "sole non-tautological contribution." Yet the DES framework, configuration, and results occupy ~3 pages. The buffer sizing rule (M = 1.30 at d = 0.10) depends entirely on the assumed ON/OFF Markov campaign model, which is itself unvalidated. This creates a circular dependency: the DES's only unique output depends on an assumed input that has no empirical basis.

*Why it matters:* Manuscript length and reader attention are finite. Space devoted to self-confirming verification could be used for sensitivity analysis, external comparison, or deeper physical-layer modeling.

*Remedy:* Reduce DES description to ~1 page. Present the distributional analysis as a "conditional illustration" with explicit sensitivity to the campaign model. Consider moving DES details to supplementary material.

**2. The packet-level validation (Section IV-J) is parameter anchoring, not validation, and the paper's framing still occasionally conflates these.**

The CCSDS-derived γ is computed from nominal framing specifications and assumed timing parameters (T_acq = 5 ms, T_guard = 4.7 ms). No modem measurements are used. The DVB-RCS2 comparison provides a plausibility bound but from a fundamentally different operational environment (GEO user terminals vs. LEO ISL). The paper correctly labels this as a "standards-based parameter estimate" in Section IV-J but the claim map (Table 10) column header "Param. est." could be misread as providing stronger evidence than it does.

*Why it matters:* The entire rate-ladder recommendation (24 kbps infeasible → 30 kbps minimum → 35 kbps recommended) hinges on γ. A 15% error in γ shifts the minimum viable PHY by ~5 kbps.

*Remedy:* (a) Rename the Table 10 column to "Std.-based est." or similar to avoid any ambiguity. (b) Add a brief uncertainty quantification: if γ_30 ∈ [0.65, 0.82] (wider than the ±0.07 currently stated), what is the range of R_PHY,min? (c) Explicitly state that the 35 kbps recommendation is robust to γ uncertainty within [0.65, 0.82] (if true).

**3. The three-layer feasibility framework conflates two genuinely independent tests with a unit conversion.**

The boxed framework (Section IV) correctly states that γ is "a parameter within Test B" and that C_raw = C_coord,info/γ is "a unit conversion embedded in Test B, not a third check." Yet the manuscript repeatedly discusses "three layers" (byte budget, MAC efficiency, TDMA airtime) in ways that suggest three independent constraints. The earlier abstract mentions "two tests" but the body text and some tables imply three.

*Why it matters:* Practitioners implementing Algorithm 1 need clarity on what constitutes an independent check vs. an intermediate calculation.

*Remedy:* Consistently use "two-test framework" throughout. Ensure all tables and figures label γ-related computations as "within Test B" rather than as a separate layer. A single pass for terminological consistency would suffice.

**4. The 1 kbps per-node budget is the most consequential assumption but receives insufficient justification.**

The physical justification (Section III-E) derives 1 kbps from a 200 kbps aggregate S-band capacity shared among k_c = 100 nodes with 50% margin. But the 200 kbps aggregate itself depends on specific link budget assumptions (2.2 GHz, 1 W, 6 dBi, 500 km) that are stated without uncertainty bounds. The paper shows (Table 2) that at ≥10 kbps, the entire TDMA analysis is non-binding—meaning the paper's primary technical contribution (TDMA sizing) is relevant only if the 1 kbps assumption holds.

*Why it matters:* If the per-node budget is 5 kbps (plausible with slightly different link assumptions), the stress-case η drops to ~13% and TDMA scheduling is non-binding. The paper's central contribution becomes moot.

*Remedy:* (a) Provide link budget uncertainty analysis (±3 dB in link margin → what per-node budget range?). (b) Explicitly identify the "binding regime" as C_node ∈ [0.5, 5] kbps and state that outside this range, only Test A matters. (c) Consider whether the paper's contribution is better framed as "identifying the regime where TDMA sizing binds" rather than "providing TDMA sizing equations."

**5. Static cluster membership is a significant limitation that is underexplored.**

The paper assumes static cluster membership for 1 year and provides a brief J2 analysis showing <0.3% overhead for cross-plane re-association. However, this analysis assumes a Walker constellation geometry. For heterogeneous orbits (different altitudes, inclinations), differential precession rates can be much higher, and cluster re-association could become a dominant overhead source. The paper acknowledges this ("evaluate ∝ ΔΩ/T_c") but does not quantify it.

*Why it matters:* The target application includes "autonomous space swarms" which may not follow regular Walker patterns. If re-association overhead exceeds 5%, it changes the η_0 term and potentially the feasibility conclusions.

*Remedy:* Provide a parametric expression for re-association overhead as a function of differential precession rate, and identify the threshold at which it becomes significant relative to η_0.

---

## Minor Issues

1. **Abstract length:** At ~200 words, the abstract is dense but within IEEE limits. However, it contains implementation-level detail (T_acq = 5 ms, T_guard = 4.7 ms) that belongs in the body. Recommend trimming to key results and contributions.

2. **Table 1 (Notation):** The γ entry includes specific numeric values (γ_24 = 0.761, etc.) that are results, not notation. Move these to the results section.

3. **Eq. 3 (η_canonical):** The equation defines η but the text immediately below uses η_total. Clarify that η_total = η + 20.5% is the operational metric while η is the architecture-specific increment.

4. **Section III-B.2, coordinator failure transient:** The thundering herd analysis (footnote) is interesting but the BEB convergence estimate ("2 doubling rounds") assumes independent backoff, which may not hold under correlated GE channel states. Note this assumption.

5. **Table 5 (Superframe):** The footnote states "ACK mini-slots (0.5 ms each)... transmitted within the jitter sub-slot." This is a clever design but the timing analysis should verify that the ACK can be decoded within the 0.5 ms window at 30 kbps (0.5 ms × 30 kbps = 15 bits—sufficient for a 1-bit ACK with framing, but barely).

6. **Eq. 8 (η_consensus):** The stability limit f_decision,max ≈ 24 seems high for a shared 1 kbps channel. Verify that this accounts for the serialization constraint mentioned in the text.

7. **Section IV-B (AoI):** The statement "AoI P99 = 441 s is <0.5% of a 24 h TCA window" is true but misleading—conjunction avoidance requires progressively more precise state knowledge as TCA approaches, not just any update within 24 h.

8. **Table 7 (Duty mapping):** Collision avoidance is listed as d = 1.0 "during event" but the background rate is d < 0.01. The transition between these states is not modeled—is it instantaneous? What is the detection-to-command latency?

9. **Section V-C (Limitations):** "Priority queueing: equal-priority" is listed as a limitation but safety-critical CA messages (128 B) are described as always single-cycle feasible. If priority queueing is not modeled, how is this guaranteed under full-load conditions?

10. **Reference [3] (Kuiper):** "accessed February 2026" appears to be a future date. Verify.

11. **Eq. 14 (γ time-domain):** The framing term T_framing = O_frame / (R_FEC · R_PHY) assumes framing bits are FEC-encoded. This is stated as "CCSDS standard practice" but should cite the specific standard clause.

12. **Algorithm 1, Line 4:** The footnote states algebraic equivalence with Eq. 14, but Line 4 computes (S × 8 + O_frame)/(R_FEC · R_PHY) while Eq. 14 separates T_payload, T_FEC, and T_framing. Verify these are truly equivalent (they are, but only if T_FEC includes the framing parity contribution).

13. **Section IV-A:** "Phase-staggered scheduling... DES confirms zero drops at ≥25 kbps vs. 50 kbps under random phase." This is a significant result buried in a paragraph. Consider a brief table or figure.

---

## Overall Recommendation
**Recommendation: Major Revision**

This manuscript presents a systematic, well-documented parametric sizing framework for hierarchical coordination in large space swarms. Its principal strengths are: (1) the two-test feasibility decomposition with clear separation of byte-budget and airtime constraints; (2) the CCSDS-grounded γ derivation replacing earlier ad hoc values; (3) exceptional transparency about validation limitations, with the claim map (Table 10) and V&V tier structure setting a high standard for intellectual honesty; and (4) the campaign duty factor formulation that properly contextualizes the stress-case as an episodic bound.

The most critical improvements needed are: (a) reducing manuscript length by ~30%, primarily by condensing the DES description and eliminating redundant caveats; (b) strengthening the justification for the 1 kbps per-node budget with link budget uncertainty analysis, since this assumption determines whether the paper's central contribution (TDMA sizing) is relevant; (c) resolving the residual terminological inconsistency between "two-test" and "three-layer" frameworks; and (d) providing a more rigorous treatment of the static-membership assumption's validity domain. The paper would also benefit from engaging with any available LEO ISL channel measurements to narrow the γ uncertainty range. In its current form, the paper is a thorough technical report that needs tightening and sharpening to meet journal standards for conciseness and impact.

## Constructive Suggestions

1. **Highest impact: Tighten the narrative arc.** The paper currently reads as "here is everything we computed." Restructure around the key insight: *at 1 kbps per-node budgets, TDMA scheduling is the binding constraint, and the PHY rate must be ≥35 kbps.* Everything else supports or qualifies this finding. This would reduce length by ~30% and sharpen impact.

2. **Quantify the binding regime.** Add a figure showing which test (A or B) binds as a function of C_node and k_c. This would immediately communicate when the TDMA analysis matters and when it doesn't—arguably the paper's most useful practical contribution.

3. **Strengthen γ anchoring.** Contact modem vendors or search IEEE Aerospace Conference proceedings for any published Proximity-1 or S-band ISL slot efficiency measurements. Even a single data point would elevate the γ estimate from "standards-based calculation" to "partially validated parameter."

4. **Add a worked example for a non-default parameter set** (e.g., k_c = 200, S = 512 B, T_c = 5 s) to demonstrate the generality of Algorithm 1 and the γ-conditional lookup table.

5. **Consider network calculus bounds.** Since Le Boudec is already cited, applying a simple deterministic service curve analysis would provide worst-case delay bounds complementary to the mean-value approach, strengthening the methodology without requiring new simulation.

6. **Reframe the DES contribution.** Instead of "DES confirms analytical equations," present it as "DES explores distributional tails that closed-form analysis cannot capture." This is already partially done but could be more prominent, with the buffer sizing rule as the headline DES result.