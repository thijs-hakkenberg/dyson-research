---
paper: "01-isru-economic-crossover"
version: "al"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-22"
recommendation: "Accept"
---

# Peer Review Report

**Manuscript Title:** Economic Inflection Points in Space Manufacturing: Monte Carlo Analysis of In-Situ Resource Utilization vs. Earth Launch for Large-Scale Space Infrastructure
**Version:** AL (revision from AK)
**Reviewer Expertise:** Space Systems Engineering, Resource Economics, Parametric Cost Modeling

---

## Overall Recommendation

**Accept with Minor Revisions**

---

## Summary of Changes from Version AK

Version AL addresses the major and minor issues raised by all three AK reviewers with a thoroughness that is commendable. The specific changes are:

1. **K-median sweep elevated to primary framing.** Table 12 (K-median sweep) is now in the main text (Section 4.3) rather than relegated to an appendix. The conclusion explicitly states that headline results are "best read as a conditional surface over K, not as unconditional predictions." This directly addresses the consensus concern from GPT, Claude, and myself regarding the weak empirical grounding of K and the risk of readers interpreting conditional probabilities as frequentist predictions. The reframing is well-executed.

2. **Kaplan-Meier table promoted to main text.** Table 13 now appears in Section 4.3 with an interpretive paragraph distinguishing committed-program (conditional median) from portfolio-level (KM median) decision contexts. This resolves GPT's Major Issue #2 and substantially improves the paper's statistical integrity.

3. **Logistic learning saturation comparison (Table 9).** A smooth logistic saturation model is compared against the piecewise plateau across three transition volumes. This addresses GPT's Major Issue #3 and Claude's Major Issue #2, which both requested an alternative saturating learning curve form. The results show the crossover shifts by at most +491 units under the logistic form, confirming qualitative robustness.

4. **ISRU production yield parameter Y (Table 2).** A yield parameter capturing imperfect quality acceptance is introduced, with a sensitivity sweep from Y = 1.0 down to Y = 0.70. This addresses Claude's Major Issue #3 (reliability/quality cost modeling). The effect is modest: +259 units at Y = 0.80, +469 at Y = 0.70.

5. **NPV crossover equation updated.** Equation 12 now explicitly shows the five annual capex tranches with time-coupled discounting, matching the code's actual implementation. This resolves GPT's Major Issue #4 regarding the inconsistency between the displayed equation and the described implementation.

6. **Stale table fixes.** The convergence CDF table (Table 10), KM table (Table 13), copula table (Table A.6), and config table (Table C.5) have been regenerated from the canonical pipeline. The copula baseline row now shows 85.1% / 4,311, consistent with the main MC summary. This resolves GPT's Major Issue #1, which identified numerical inconsistencies across tables.

7. **Config table corrected.** The Learning plateau (Earth) row now correctly shows a checkmark (stochastic) rather than "off," and the Dynamic vitamin fraction row shows a checkmark. This resolves an error flagged in AK where the config table implied these features were disabled despite being active in the canonical MC.

8. **Abstract and conclusion updated.** Both now reference the K-conditional surface, KM median (~5,350), and the logistic comparison. The conditional language is consistent and appropriate.

---

## Assessment of Specific AK-to-AL Changes

### K-Conditional Framing

The elevation of the K-median sweep to primary status is the single most important improvement in this revision. The presentation is well-structured: Table 12 provides five K scenarios from $50B to $150B, with convergence rates ranging from 92% to 46%. The conclusion's statement that "the headline results are therefore best read as a conditional surface over K" is intellectually honest and appropriate given that K explains 63% of variance with no direct empirical anchor.

**Minor concern:** The abstract still leads with the 85% convergence figure before qualifying it with the K-conditional caveat. Placing the K-conditional framing earlier in the abstract would reinforce the revised narrative. As written, a casual reader may still fixate on the 85% headline.

### Logistic Learning Saturation (Table 9)

The model-form sensitivity test is well-designed and appropriately scoped. The comparison of piecewise plateau versus logistic saturation across three transition volumes provides useful bounds: the plateau shifts crossover earlier by 810--1,463 units (strengthening ISRU), while the logistic shifts it later by 94--491 units (weakening ISRU). The text correctly notes that the two forms differ in *direction* and that the model-form uncertainty (~1,500 units) is comparable to the K uncertainty.

**Minor concern:** The logistic form is defined inline in the "Epistemic vs. parametric uncertainty" paragraph (line ~684) rather than as a numbered equation. For a model-form comparison that is now a headline result cited in the abstract and conclusion, the logistic cost function deserves its own equation number for reader traceability.

### Yield Parameter Y

The yield parameter is a clean and appropriate addition. The sensitivity sweep (Table 2) covers Y from 1.0 to 0.70 and shows effects ranging from +52 to +469 units. The parameter is correctly integrated into the ISRU operational cost as $C_{\mathrm{ops}}(n)/Y$, and the table caption specifies the deterministic configuration.

However, the yield parameter is introduced and tested only as a deterministic sensitivity sweep. It is not included in the Monte Carlo sampling. Given that Y = 0.80 shifts the crossover by only +259 units (6.9%), the omission from the MC is unlikely to materially affect headline statistics, but it should be noted as a limitation. If Y were sampled stochastically (e.g., $Y \sim U[0.80, 1.0]$), it would add a small amount of variance and slightly increase the conditional median. The paper should state explicitly that Y is a deterministic sensitivity parameter, not a stochastic MC input.

### KM Promotion

The Kaplan-Meier table is now well-integrated into Section 4.3 with a clear interpretive framework: "For committed programs, the conditional median is the appropriate planning statistic. For portfolio-level decisions, the KM median is more appropriate." This is an important distinction that resolves the ambiguity GPT flagged. The divergence column (12% to 51% across discount rates) quantifies the selection bias from conditioning on convergence.

---

## Remaining Major Concerns

None. The revision has addressed all major concerns from the AK round.

---

## Remaining Minor Concerns

1. **Abstract bootstrap CI rounding.** The abstract reports "95% CI: [4,200, 4,420]" while the main text (line 682) states "[4,198, 4,423]." The upper bound differs by 3 units after rounding. This is trivial but should be corrected for precision: either report [4,200, 4,420] consistently (acceptable rounding) or use the exact values throughout.

2. **K-median sweep Det. N* column ambiguity.** Table 12 includes a "Det. N*" column showing deterministic crossover points at each K median value (e.g., 4,374 at $50B, 6,952 at $65B). The table caption does not specify whether these are lump-sum or phased-capital deterministic values. Since the config_crossover table (Table 8) distinguishes lump-sum ($50B: 4,374) from phased ($50B: 3,749), the K-median sweep's $50B Det. N* = 4,374 appears to be lump-sum. This should be noted in the caption or column header (e.g., "Det. N* (lump-sum)") to avoid confusion with the phased baseline.

3. **Logistic form needs equation number.** As noted above, the logistic saturation cost function ($C_{\mathrm{labor}}(n) = C_{\mathrm{floor}}^{\mathrm{labor}} + (C_{\mathrm{Wright}}(n) - C_{\mathrm{floor}}^{\mathrm{labor}}) / (1 + (n/n_{\mathrm{half}})^2)$) is defined inline in a paragraph. Given its prominence in Table 9, the abstract, and the conclusion, it should be a numbered equation for cross-referencing.

4. **Yield parameter not in MC.** Table 1 (MC parameter distributions) does not list Y among the stochastic parameters, and the yield sweep (Table 2) is deterministic only. The paper should explicitly state that Y is tested as a deterministic sensitivity variant, not included in the canonical MC ensemble, and briefly justify this choice (e.g., "The yield effect is small relative to K and LR_E variance; including Y in the MC would add <0.5% to total output variance").

5. **Code availability.** The commit hash remains "PENDING" (line 1036). This should be resolved before final submission.

6. **Sensitivity index (Table 6) formatting.** The "Max shift" column still mixes absolute units (+1,588), percentages (-16.5%), and qualitative labels ("varies," "---"). While this has been noted before, a consistent format would improve readability. Consider separating into "Shift (units)" and "Shift (%)" columns, or standardizing to one format.

7. **Dynamic vitamin fraction in config table.** Table C.5 (config table) shows Dynamic vitamin fraction with "$n_v \sim U[2000,10000]$" in the Sensitivity variants column. However, $n_v$ is also sampled in the canonical MC (per Table 1), so it should also appear in the Baseline MC column with the stochastic specification. The current presentation implies $n_v$ is only a sensitivity variant, which is inconsistent with the canonical configuration (Table 7).

8. **Convergence CDF table (Table 10) at H=40,000.** At $r = 5\%$ and $H = 40,000$, the MC summary (Table 9) reports Conv. = 85.1%. Table 10's last row is H = 20,000 at 80.6% for $r = 5\%$. Adding an H = 40,000 row to Table 10 (which should match 85.1%) would close the loop for readers who want to verify consistency. Alternatively, a sentence noting that "Table 9 reports the H = 40,000 endpoint of this CDF" would suffice.

---

## Positive Aspects

1. **Intellectual honesty of the K-conditional reframing.** The revision's most consequential improvement is the explicit acknowledgment that the headline 85% convergence rate is a function of the assumed K prior, and the presentation of the K-median sweep as the primary result. This is an uncommon level of epistemic transparency for a techno-economic analysis paper and substantially strengthens the paper's credibility.

2. **Model-form sensitivity is a genuine contribution.** The logistic vs. plateau comparison (Table 9) goes beyond what most parametric studies provide. The finding that the two forms produce directionally different shifts (plateau favors ISRU, logistic disfavors it) but the crossover persists in either case is a strong robustness result.

3. **Statistical maturity.** The combination of conditional medians, KM survival analysis, bootstrap CIs, PRCC rankings, variance decomposition, and two-part sensitivity decomposition constitutes a level of statistical rigor rarely seen in space systems engineering economics. The explicit attention to censoring, selection bias, and the distinction between parametric and epistemic uncertainty is exemplary.

4. **Decision-relevant framing.** The paper provides multiple decision-relevant outputs: the savings window probability (for committed programs), the KM median (for portfolio decisions), the K-conditional surface (for readers with different priors), the revenue breakeven (for distinguishing cost-driven from revenue-driven infrastructure), and the hybrid option value (for transition planning). This multi-dimensional decision framing makes the paper useful to a wide range of stakeholders.

5. **Yield parameter addresses quality realism.** While the effect is modest, introducing Y demonstrates awareness of the manufacturing quality challenge for early ISRU production and provides a hook for future empirical calibration.

6. **Internal consistency is now excellent.** The copula table, convergence CDF, KM table, config table, and headline numbers all align with the canonical baseline. The table provenance issue flagged by GPT in AK appears to have been resolved.

---

## Summary

Version AL has substantially addressed the concerns raised in the AK review round. The three most significant improvements are: (1) the K-conditional reframing of headline results, (2) the logistic learning saturation model-form test, and (3) the promotion of Kaplan-Meier survival analysis to the main text. The yield parameter and phased capex equation updates are welcome additions that further strengthen the analysis. The remaining concerns are minor (formatting, a missing equation number, an unresolved commit hash) and do not require re-running simulations. This paper is ready for publication after minor editorial corrections.
