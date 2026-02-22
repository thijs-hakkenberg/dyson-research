---
paper: "01-isru-economic-crossover"
version: "am"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-22"
recommendation: "Minor Revision"
---



# Peer Review: "Economic Inflection Points in Space Manufacturing: Monte Carlo Analysis of In-Situ Resource Utilization vs. Earth Launch for Large-Scale Space Infrastructure"

**Manuscript Version:** AM
**Target Journal:** Advances in Space Research
**Previous Version:** AL (Claude recommendation: Minor Revision)

---

## Overall Recommendation

**Minor Revision**

Version AM has addressed the majority of the eleven minor concerns raised in my AL review. The permanent/transient percentage framing is now internally consistent (using "% of converging runs" throughout the body text and abstract). The logistic saturation formula correctly uses $C_{\mathrm{mat}}$ instead of the previously undefined $C_{\mathrm{floor}}^{\mathrm{labor}}$, and is now numbered as Eq. 13 with a cross-reference in the abstract. The abstract has been split into two paragraphs. The K-median sweep table column header now reads "Det. $N^*$ (lump)" with caption clarification. The dual $\sigma_{\ln}$ baseline is noted in the abstract with a Table reference. These are all substantive improvements that enhance clarity and reproducibility.

Two minor issues remain, one of which is new to Version AM. With those addressed, the paper is ready for publication.

---

## Assessment of Prior Concerns (AL Review)

### AL Minor Concern 1: Permanent/transient percentage presentation

**Status: Fully addressed.**

The abstract now states "Of converging runs, 22% are analytically permanent; the remaining 78% are functionally permanent." The body text (Section 3.3, Permanent versus transient crossovers paragraph) now explicitly reports: "of the 8,511 converging runs, 1,889 (22.2% of converging) achieve permanent crossover, while 6,622 (77.8%) achieve transient crossover." The conclusion mirrors this framing. The percentages are now consistently expressed as fractions of converging runs throughout the narrative text. The only residual trace of the old framing is in the re-crossing table (Table 12), where "6,622 (66.2%)" reports the transient count as a fraction of total runs. This is a defensible choice for a table that summarizes the full MC ensemble, not the converging subset, but a footnote clarifying that 66.2% is of total runs (vs. 77.8% of converging runs) would eliminate any ambiguity. This is cosmetic, not substantive.

### AL Minor Concern 2: Logistic saturation formula definition ($C_{\mathrm{floor}}^{\mathrm{labor}}$)

**Status: Fully addressed.**

The logistic saturation formula (now Eq. 13, `eq:logistic_saturation`) uses $C_{\mathrm{mat}}$ in place of the previously undefined $C_{\mathrm{floor}}^{\mathrm{labor}}$, and the text explicitly defines it: "$C_{\mathrm{mat}} = m \cdot p_{\mathrm{fuel}}$ is the irreducible material cost (the natural labor-cost floor for Earth manufacturing)." This resolves the ambiguity completely.

However, a new concern arises from this definition -- see New Concern 1 below.

### AL Minor Concern 3: Logistic form not tested stochastically

**Status: Addressed.**

The text following Eq. 13 now includes the sentence: "The logistic form has been tested at three deterministic parameter values; full stochastic integration would require specifying prior distributions for $n_{\mathrm{half}}$ and is deferred to future work." This is exactly the acknowledgment requested. The asymmetry between the stochastic piecewise plateau and the deterministic logistic form is now transparent to the reader.

### AL Minor Concern 4: Yield parameter as MC stochastic

**Status: Addressed.**

The yield parameter $Y$ remains deterministic (baseline $Y = 1.0$ in the MC), but Section 2.2 now explicitly states: "$Y$ is tested as a deterministic sensitivity parameter (Table 1), not a stochastic MC input, because the effect is small relative to $K$ and LR$_E$ variance ($<$0.5% of total output variance at $Y \geq 0.80$). Even at $Y = 0.80$, the crossover shifts by only +259 units (+6.9%)." This provides both the justification and the acknowledgment requested. The decision not to add $Y$ to the MC is now a defended modeling choice rather than an unexplained omission.

### AL Minor Concern 5: Table 7 logistic form non-monotone shift behavior

**Status: Not directly addressed, but acceptable.**

The logistic comparison table (now Table 8) still shows the non-monotone pattern ($n_{\mathrm{half}} = 200$: +94; $n_{\mathrm{half}} = 500$: +491; $n_{\mathrm{half}} = 1000$: +469) without a brief explanation. On reflection, the pattern is self-explanatory to the target audience: at $n_{\mathrm{half}} = 200$, the logistic saturates before the crossover region, so its effect is small; at $n_{\mathrm{half}} \geq 500$, saturation occurs near the crossover and the effect plateaus. I withdraw this concern as a required change. An explanation would be helpful but is not necessary for publication.

### AL Minor Concern 6: Code availability commit hash

**Status: Not addressed.**

The code availability section (line 1041) still reads: "version AM of the codebase (commit `PENDING`)." This has been flagged since the AK review by all three reviewers. The version label has been correctly updated to AM, but the commit hash remains a placeholder. This must be resolved before final publication but is understood to be a pre-acceptance administrative item.

### AL Minor Concern 7: Paper length

**Status: N/A (withdrawn in AL review).**

I withdrew this concern in the AL review and maintain that position. The paper is dense but each section serves a purpose.

### AL Minor Concern 8: Abstract density / split into two paragraphs

**Status: Fully addressed.**

The abstract is now split into two paragraphs. Paragraph 1 covers the model description, primary result (crossover probability, conditional and KM medians with CIs, permanent/transient breakdown, savings window probability, and dual $\sigma_{\ln}$ note). Paragraph 2 covers the variance decomposition, K-conditional surface, model-form sensitivity, failure modes, and revenue breakeven. This is a clear improvement in readability.

### AL Minor Concern 9: K-median sweep table deterministic $N^*$ column

**Status: Fully addressed.**

Table 11 (`tab:k_median_sweep`) now has the column header "Det. $N^*$ (lump)" and the caption explicitly states: "'Det. $N^*$' uses lump-sum $K$ at the listed median value (not phased); compare Table 6 for phased baselines." This resolves the ambiguity between lump-sum and phased capital in the deterministic column. The cross-reference to the configuration-to-crossover mapping table is helpful.

### AL Minor Concern 10: Exponential vs. logistic vitamin decay functional form

**Status: Not directly addressed, but acceptable.**

No discussion of the vitamin decay functional form sensitivity has been added. Given that the vitamin parameters collectively explain <0.5% of variance (Section 3.3), this remains a minor concern that does not materially affect the conclusions. I withdraw this as a required change.

### AL Minor Concern 11: Dual $\sigma_{\ln}$ baseline in abstract

**Status: Fully addressed.**

The abstract now includes: "Results are reported at $\sigma_{\ln} = 0.70$ (megaproject reference class); a space-specific variant ($\sigma_{\ln} = 1.0$) appears in Table ref{tab:dual_baseline}." This gives the reader immediate notice that the headline figures use the terrestrial reference class and that the space-specific variant is available.

---

## Remaining Major Concerns

None.

---

## Minor Concerns

### New Concern 1: Abstract statement "both forms are tested deterministically only" is misleading

The abstract (paragraph 2) states: "Model-form sensitivity (piecewise plateau vs. logistic saturation, Eq. 13) shifts the crossover by $\pm$1,500 units without eliminating it; both forms are tested deterministically only."

This sentence is misleading. The piecewise plateau model IS tested stochastically -- it is a core component of the canonical MC (Table 3: "Learning model: Wright with stochastic plateau ($n_{\mathrm{break}}$, $\eta$)"; Table 2: $n_{\mathrm{break}} \sim U[200, 1000]$, $\eta \sim U[0.3, 0.7]$). The logistic form is tested deterministically only. The comparison in Table 8 tests both forms deterministically at matched parameter values, which is the source of the $\pm$1,500 unit spread. However, saying "both forms are tested deterministically only" implies that neither form is in the MC, which contradicts Section 3.3 and the canonical configuration table.

Suggested fix: Replace "both forms are tested deterministically only" with "the comparison table tests both forms at deterministic parameter values; only the piecewise plateau is integrated into the stochastic MC." Alternatively: "the model-form comparison (Table 8) is deterministic; the logistic form is not integrated into the MC."

### Residual Concern: Re-crossing table percentage basis

Table 12 reports "Transient runs (count): 6,622 (66.2%)" where 66.2% is a fraction of total runs (6,622/10,000). In the body text directly above, the same 6,622 runs are described as "77.8% [of converging]." Both are correct in their respective contexts, but the table and the paragraph it supports use different denominators without flagging the switch. A table footnote -- e.g., "66.2% of total runs; equivalently, 77.8% of converging runs" -- would eliminate any misreading. This is cosmetic.

---

## Internal Consistency Checks

- **Convergence rate at $r = 5\%$:** 85.1% (or "85%") is consistent across Tables 4, 5, 7, 8, 9, 11, 12, abstract, and conclusion. **Pass.**
- **Conditional median at $r = 5\%$:** 4,311 in body tables; ~4,300 (rounded) in abstract and conclusion. **Pass.**
- **KM median at $r = 5\%$:** ~5,350 in Table 10, abstract, and conclusion. **Pass.**
- **Bootstrap CI on conditional median:** [4,198, 4,423] in body and conclusion; [4,200, 4,420] (rounded) in abstract. **Pass.**
- **Savings window at 20k:** 94.7% in Table 14, abstract reports 95% (rounded), with 95% CI [94%, 95%]. **Pass.**
- **Permanent fraction:** "Of converging runs, 22% are analytically permanent" in abstract; "1,889 (22.2% of converging)" in body. **Pass.** (Unified framing per AL Concern 1.)
- **Variance decomposition:** $K$ = 63%, LR$_E$ = 20%, cumulative ~83% in abstract; body reports $K$ = 62.6%, LR$_E$ = 20.0%, cumulative 82.6%. **Pass** (rounding).
- **Revenue breakeven:** $R^* \approx \$0.94$M/unit/yr in abstract, body (Section 4.2), and conclusion. **Pass.**
- **Logistic saturation equation:** Eq. 13 uses $C_{\mathrm{mat}}$ consistently. Referenced in abstract (Eq. 13) and conclusion (Eq. 13). **Pass.**
- **K-median sweep table:** "Det. $N^*$ (lump)" column header, with caption "uses lump-sum $K$." $K = \$65$B row: Conv. = 85.1%, matching canonical MC. **Pass.**
- **Phased capital equation (Eq. 20):** Text correctly states "At the deterministic baseline ($t_0 = 5$), the coupled form reduces to:" followed by the uncoupled summation. This clarifies that Eq. 20 is a special case of Eq. 8 when $t_0 = 5$. **Pass.**
- **Yield parameter:** Table 1 reports baseline $N^* = 3,749$ at $Y = 1.0$; maximum shift +469 at $Y = 0.70$. Consistent with sensitivity index table. **Pass.**
- **$K = \$50$B deterministic phased crossover:** 3,749 in Tables 3, 6 (config-to-crossover), yield table caption, and body. **Pass.**
- **Table 2 (new in AK):** Plateau and vitamin parameters listed under "new in AK." $n_v$ in range column: [2,000, 10,000]. **Pass.**
- **Dual baseline table (Table 5):** $\sigma_{\ln} = 0.70$: 85.1%, 4,311, 94.7%. $\sigma_{\ln} = 1.0$: 80.8%, 3,753, 93.7%. Both consistent with sigma_ln table (Table 4). **Pass.**

No numerical inconsistencies detected.

---

## Comparison with AL-to-AM Change List

The user-provided change list identifies the following AM changes. I verify each:

1. **Permanent/transient % framing uses % of converging runs in body text.** Verified. Body text (line 784) now reports "22.2% of converging" and "77.8%." Abstract uses "Of converging runs." Conclusion uses "Of converging runs." **Addressed.**

2. **$C_{\mathrm{floor}}^{\mathrm{labor}}$ replaced with $C_{\mathrm{mat}}$ in logistic formula.** Verified. Eq. 13 uses $C_{\mathrm{mat}}$ with explicit definition. No instances of $C_{\mathrm{floor}}^{\mathrm{labor}}$ remain in the manuscript. **Addressed.**

3. **Logistic form explicitly acknowledged as deterministic-only with justification.** Verified. Text following Eq. 13: "The logistic form has been tested at three deterministic parameter values; full stochastic integration would require specifying prior distributions for $n_{\mathrm{half}}$ and is deferred to future work." **Addressed.** (But the abstract sentence "both forms are tested deterministically only" is misleading -- see New Concern 1.)

4. **Yield parameter acknowledged as deterministic-only with variance justification.** Verified. Section 2.2: "$Y$ is tested as a deterministic sensitivity parameter... because the effect is small relative to $K$ and LR$_E$ variance ($<$0.5% of total output variance at $Y \geq 0.80$)." **Addressed.**

5. **Abstract split into 2 paragraphs.** Verified. **Addressed.**

6. **Dual $\sigma_{\ln}$ noted in abstract with Table reference.** Verified. Abstract paragraph 1: "Results are reported at $\sigma_{\ln} = 0.70$ (megaproject reference class); a space-specific variant ($\sigma_{\ln} = 1.0$) appears in Table 5." **Addressed.**

7. **K-median sweep Det. $N^*$ column clarified as "(lump)."** Verified. Column header: "Det. $N^*$ (lump)." Caption: "uses lump-sum $K$ at the listed median value (not phased)." **Addressed.**

8. **Eq. phased_capital labeled as $t_0 = 5$ special case.** Verified. Line 834: "At the deterministic baseline ($t_0 = 5$), the coupled form reduces to:" followed by Eq. 20. This makes clear that Eq. 20 is a special case, not the general form. **Addressed.**

9. **Logistic equation numbered for cross-referencing.** Verified. Eq. 13 (`eq:logistic_saturation`), referenced in abstract and conclusion. **Addressed.**

10. **Code availability updated to AM.** Verified. "version AM of the codebase (commit PENDING)." Version label updated; commit hash still pending. **Partially addressed.**

---

## Summary

Version AM completes the resolution of the AL review's minor concerns. Nine of eleven concerns are fully addressed; one is withdrawn as acceptable without change (vitamin decay functional form); one remains an administrative placeholder (commit hash). The paper is now internally consistent in its permanent/transient framing, the logistic saturation formula is properly defined and numbered, the abstract is readable, the K-median table is unambiguous, and the dual baseline is noted upfront.

The only substantive new concern is the abstract's statement that "both forms are tested deterministically only," which misrepresents the stochastic status of the piecewise plateau model in the canonical MC. This is a one-sentence fix.

With this correction and the commit hash resolved, the paper is ready for publication. It makes a genuine and carefully qualified contribution to the ISRU economics literature.

---

## Constructive Suggestions

1. **Fix the abstract sentence.** Replace "both forms are tested deterministically only" with language that accurately reflects the asymmetry: the piecewise plateau is stochastic in the MC; the logistic form is deterministic only; the model-form comparison table (Table 8) tests both at deterministic parameter values.

2. **Add a footnote to Table 12** clarifying that "66.2%" is of total MC runs, corresponding to 77.8% of converging runs, to maintain consistency with the body text framing.

3. **Resolve the commit hash** before final submission. This has been flagged since version AK and is the last remaining administrative item.
