---
paper: "01-isru-economic-crossover"
generated: "2026-02-17"
type: "review-summary"
reviewers:
  - claude-opus-4-6
  - gemini-3-pro
  - gpt-5-2
---



# Comparative Peer Review Synthesis

## Version Comparison

All three reviews provided here are for **Version A (formal academic voice)** only. No Version B reviews were supplied in the input materials, so a direct A-vs-B voice comparison cannot be performed. The ratings and commentary below therefore reflect only Version A assessments. Any Version B cells in the aggregated ratings table are marked as not available.

That said, the three Version A reviews do reveal an implicit tension between rigor and readability. **Gemini** praised the formal voice as "exceptionally well-written" and "dense but precise" (Clarity: 5/5), while **Claude** found the same text "excessively long" and reading "more like a technical report than a journal article," recommending a 30–40% length reduction (Clarity: 3/5). **GPT** occupied a middle position (Clarity: 4/5), agreeing the paper is well-organized but noting that "several sections in Results/Sensitivity repeat or re-justify points already made earlier." This suggests that the formal academic voice is technically precise but may sacrifice narrative economy—a trade-off that a humanized Version B might address, though this cannot be confirmed without those reviews.

---

## Consensus Strengths

1. **Novel and timely framework.** All three reviewers agreed that combining Wright learning curves for both pathways, schedule-aware NPV discounting, and Monte Carlo uncertainty propagation for generic structural manufacturing (rather than mission-specific propellant/water) represents a genuine contribution to the ISRU economics literature. Claude called it "the first systematic, uncertainty-quantified comparison"; Gemini predicted it "will likely become a standard reference"; GPT acknowledged it as "a meaningful contribution relative to much of the ISRU economic literature."

2. **Permanent vs. transient crossover distinction.** All reviewers highlighted the conceptual contribution of distinguishing crossovers that persist asymptotically from those reversed by the irreducible "vitamin" fraction. Claude called it "a meaningful conceptual contribution"; Gemini termed it "a significant theoretical contribution"; GPT described it as "a useful conceptual addition."

3. **Exemplary AI-assisted methodology disclosure and ethical transparency.** All three reviewers rated Ethical Compliance at 5/5 and specifically praised the footnote delineating AI-assisted tasks from human-authored quantitative work. Claude called it "exemplary"; Gemini said it "sets a high standard"; GPT described it as "unusually explicit and, in my view, exemplary."

4. **Exhaustive sensitivity and robustness analysis.** All reviewers acknowledged the breadth of robustness checks—learning plateaus, piecewise schedules, copula correlations, Kaplan-Meier survival analysis, revenue breakeven, and success probability thresholds. Gemini noted the checks "already cover the areas where a reviewer might typically raise objections." Claude and GPT, while noting the analysis was perhaps too exhaustive for the main text, recognized its thoroughness as a substantive strength.

5. **High model transparency and reproducibility signals.** The explicit parameter tables (Tables 1–2), active-equation configuration table (Table 4), distribution specifications, and code-availability commitment were praised by all reviewers as strong reproducibility practices.

6. **Revenue breakeven analysis as a policy-relevant qualification.** All three reviewers identified the finding that ISRU's advantage is strongest for non-revenue infrastructure as an important and nuanced insight. Claude called it "a particularly valuable contribution"; GPT noted it "fundamentally qualifies the headline finding."

---

## Consensus Weaknesses

1. **ISRU capital cost distribution is inadequately calibrated to space-specific cost growth data.** Claude identified this as a major issue: the paper cites JWST (10×) and ISS (3×) overruns but uses σ_ln = 0.70 (P90/P50 ≈ 2.5×), which is internally inconsistent. GPT raised the related concern that independent sampling of cost components can produce unrealistic implied labor shares without coherence constraints. Gemini did not flag this as a major issue but acknowledged reliance on terrestrial analogies as a limitation.

2. **Wright curve extrapolation beyond empirical range (n ≈ 200–1,000) to crossover volumes (n ≈ 4,000–40,000) is insufficiently bounded.** Claude specifically noted the absence of an Earth-side scaling penalty symmetric to the ISRU pioneering phase. GPT raised the related concern about inconsistent implied labor shares at extreme production volumes. Gemini acknowledged the limitation but considered the plateau model an adequate robustness check.

3. **Launch cost modeling ambiguity.** GPT identified this as a primary major issue: the relationship between the sampled p_launch (Table 1) and the decomposed model (Eq. 8) is unclear, with apparent contradictions between the sensitivity section text and Table 2. Claude raised the related concern about program-indexed vs. market-indexed learning for launch costs. Gemini did not flag this explicitly.

4. **Timing/delivery interpretation affects NPV and revenue results.** GPT noted that lunar-to-GEO transport duration is not modeled despite transport cost being included, creating a misalignment between production time and delivery time that affects discounting and the revenue breakeven threshold. Claude raised the related concern about the revenue breakeven approximation being buried in the discussion despite fundamentally qualifying the headline result. Gemini noted the need for clarification of timing variables in the revenue section.

5. **Headline "68% achieve crossover" conflates permanent and transient crossovers.** Claude flagged this as a major issue, arguing the abstract should lead with the decomposition (~6% permanent, ~62% transient). GPT raised the related concern that the conceptual link between asymptotic per-unit cost classification and discounted cumulative re-crossing behavior is not carefully stated. Gemini acknowledged the importance of the distinction but did not consider the current framing misleading.

6. **Excessive length and detail in the main text.** Claude recommended a 30–40% reduction, moving most sensitivity tests to supplementary material. GPT similarly suggested consolidating to "top 5 drivers and 3 failure modes." Gemini, by contrast, found the structure and length appropriate.

---

## Divergent Opinions

| Area | Position | Reviewer |
|------|----------|----------|
| **Overall recommendation** | Major Revision | **Claude**, **GPT** |
| | Accept | **Gemini** |
| **Severity of ISRU capital calibration issue** | Major issue requiring baseline recalibration to σ_ln ≈ 1.0 | **Claude** |
| | Minor concern; sensitivity tests adequate | **Gemini** |
| | Related concern about parameter coherence constraints | **GPT** |
| **Paper length and detail** | Excessively long; needs 30–40% reduction (Clarity: 3/5) | **Claude** |
| | Appropriate and well-structured (Clarity: 5/5) | **Gemini** |
| | Somewhat long but generally well-organized (Clarity: 4/5) | **GPT** |
| **Methodological soundness** | Adequate (3/5); copula correlations unjustified, missing physical correlations among independent parameters | **Claude** |
| | Excellent (5/5); state-of-the-art for early-phase TEA | **Gemini** |
| | Adequate (3/5); launch cost mapping and parameter coherence need fixing | **GPT** |
| **Launch cost modeling** | Concern about program-indexed vs. market-indexed learning (conceptual) | **Claude** |
| | Not flagged | **Gemini** |
| | Primary major issue: ambiguous variable mapping between Table 1 and Eq. 8 (definitional) | **GPT** |
| **Revenue breakeven treatment** | Should be elevated to co-equal result with dedicated figure | **Claude** |
| | Valuable addition; minor clarifications needed | **Gemini** |
| | Should use exact DCF formulation as primary result, not approximation | **GPT** |
| **Binary success/failure model** | Major issue; partial success states needed | **Claude** |
| | Minor suggestion to note salvage value as conservative bound | **Gemini** |
| | Not flagged as major issue | **GPT** |
| **Need for bottom-up ISRU architecture anchoring** | Important gap; cite ESA/lunar construction literature | **Claude** |
| | Acknowledged but not critical | **Gemini** |
| | Noted; positions paper as "exploratory/scoping study" | **GPT** |

---

## Aggregated Ratings

| Criterion | Claude A | Claude B | Gemini A | Gemini B | GPT A | GPT B |
|-----------|----------|----------|----------|----------|-------|-------|
| Significance & Novelty | 4 | N/A | 5 | N/A | 4 | N/A |
| Methodological Soundness | 3 | N/A | 5 | N/A | 3 | N/A |
| Validity & Logic | 3 | N/A | 4 | N/A | 3 | N/A |
| Clarity & Structure | 3 | N/A | 5 | N/A | 4 | N/A |
| Ethical Compliance | 5 | N/A | 5 | N/A | 5 | N/A |
| Scope & Referencing | 4 | N/A | 4 | N/A | 4 | N/A |
| **Mean** | **3.67** | — | **4.67** | — | **3.83** | — |

**Cross-reviewer mean by criterion:**
- Significance & Novelty: 4.33
- Methodological Soundness: 3.67
- Validity & Logic: 3.33
- Clarity & Structure: 4.00
- Ethical Compliance: 5.00
- Scope & Referencing: 4.00

---

## Priority Action Items

### 1. Resolve launch cost modeling ambiguity (Applies to: both versions)
**Flagged by: GPT (major), Claude (related concern)**

Eliminate the inconsistency between the sampled p_launch in Table 1 and the decomposed learning model in Eq. 8. Adopt one clean approach: either sample p_fuel and p_ops directly (removing p_launch from Table 1) or explicitly define the mapping from sampled p_launch to the decomposed model. Resolve the textual contradiction between "baseline uses constant launch cost" and Table 2 indicating launch learning is active. This is the highest priority because it affects reproducibility and may require re-running simulations.

### 2. Recalibrate ISRU capital cost baseline or justify current calibration (Applies to: both versions)
**Flagged by: Claude (major), GPT (related), Gemini (minor)**

The σ_ln = 0.70 baseline is inconsistent with the paper's own space-specific cost growth citations (JWST 10×, ISS 3×). Either recalibrate to σ_ln ≈ 1.0 as the baseline (consistent with ISS), present dual baselines (σ_ln = 0.70 and 1.0), or provide an explicit, substantive argument for why a first-of-kind ISRU facility would experience less cost growth than ISS/JWST. Add parameter coherence constraints (enforce C_mfg^(1) ≥ C_mat; C_ops^(1) ≥ C_floor) and report rejection rates.

### 3. Reframe headline crossover probability with permanent/transient decomposition (Applies to: both versions)
**Flagged by: Claude (major), GPT (major), Gemini (acknowledged)**

Restructure the abstract and conclusion to lead with the permanent/transient decomposition and savings window survival probability rather than the raw "68% achieve crossover." The current framing risks overstating robustness. Present the savings window probability (25–44% depending on program size) as the primary decision-relevant metric. Clarify that "transient" classification based on asymptotic per-unit costs does not necessarily predict practical re-crossing under discounting within finite horizons.

### 4. Define delivery timing explicitly and include transport duration (Applies to: both versions)
**Flagged by: GPT (major), Claude (related)**

Specify whether t_{n,I} represents production completion on the lunar surface or delivery to operational orbit (GEO). Add a transport-time parameter τ_trans (even if simple) so that discounting and revenue-delay calculations are consistent. Re-evaluate the revenue breakeven threshold R* with transport time included and report sensitivity. Upgrade the revenue breakeven section from an approximation to an exact discounted cash flow formulation, or clearly bound the approximation error.

### 5. Bound Wright curve extrapolation symmetrically for both pathways (Applies to: both versions)
**Flagged by: Claude (major), GPT (concern), Gemini (acknowledged)**

Add an Earth-side scaling penalty test (e.g., cost multiplier of 1.1–1.3× beyond n = 2,000) to mirror the ISRU pioneering phase. The current model tests only slower learning at high volumes but not cost increases from supply chain bottlenecks, workforce expansion, or regulatory burden at unprecedented production scales. This strengthens the claim of symmetric pathway treatment.

### 6. Reduce main text length by consolidating sensitivity analysis (Applies to: Version A primarily)
**Flagged by: Claude (major), GPT (moderate)**

Move the majority of §3.2 sensitivity tests to supplementary material, retaining only the top 5 most impactful tests in the main text with a summary table. The current exhaustive treatment (~15,000 words) dilutes the main narrative. Target 6,000–10,000 words for the main text, consistent with typical journal length for the target venues.

### 7. Elevate revenue breakeven to co-equal result and address ISRU partial failure modes (Applies to: both versions)
**Flagged by: Claude (major for both), Gemini (minor for partial failure), GPT (major for revenue)**

Develop the revenue breakeven finding into a co-equal result with a dedicated figure showing crossover probability as a function of revenue rate R. Address the tension that SPS (the most commonly cited application) is revenue-generating, which may favor the Earth pathway even at high volumes. For the success probability analysis, sketch at least a simple two-stage model with partial success states (e.g., 30% throughput) rather than binary success/failure.

---

## Overall Assessment

The manuscript presents a genuinely novel and timely parametric framework for comparing Earth-launch versus ISRU manufacturing pathways under uncertainty. All three reviewers recognized the conceptual contribution (permanent vs. transient crossover, revenue breakeven qualification), the thoroughness of the sensitivity analysis, and the exemplary ethical transparency. The paper's core finding—that ISRU crossover is plausible but conditional, fragile to capital cost uncertainty, and strongest for non-revenue infrastructure—is an important contribution to space economics.

However, two of three reviewers recommend **Major Revision**, and the consensus weaknesses are substantive: the launch cost modeling contains definitional ambiguities that may affect reproducibility and could require re-running simulations; the ISRU capital calibration is internally inconsistent with the paper's own cited data; the headline crossover probability is framed in a way that overstates robustness; and the revenue breakeven finding—arguably the most policy-relevant result—is insufficiently prominent. These issues are addressable but require more than cosmetic changes.

**Recommended path forward:** Proceed with **Version A** (formal academic voice), as it is the only version reviewed and received strong marks for precision and transparency. Prioritize the top 4 action items (launch cost mapping, capital calibration, headline reframing, and timing definition) before resubmission, as these affect the quantitative integrity of the results. Simultaneously reduce main text length by ~30% by moving secondary sensitivity tests to supplementary material. With these revisions, the paper should be a strong candidate for publication in *Advances in Space Research* or *Acta Astronautica*.