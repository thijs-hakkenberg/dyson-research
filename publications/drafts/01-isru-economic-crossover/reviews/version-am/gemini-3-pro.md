---
paper: "01-isru-economic-crossover"
version: "am"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-22"
recommendation: "Accept"
---

# Peer Review Report

**Manuscript Title:** Economic Inflection Points in Space Manufacturing: Monte Carlo Analysis of In-Situ Resource Utilization vs. Earth Launch for Large-Scale Space Infrastructure
**Version:** AM (revision from AL)
**Reviewer Expertise:** Space Systems Engineering, Resource Economics, Parametric Cost Modeling

---

## Overall Recommendation

**Accept**

---

## Summary of Changes from Version AL

Version AM addresses the consensus and individual concerns from the AL review round with precision and economy. The specific changes are:

1. **Abstract split into two paragraphs.** Paragraph 1 covers the model description and primary results (crossover rate, conditional/KM medians, permanent/transient breakdown, savings window probability, dual $\sigma_{\ln}$ reference). Paragraph 2 covers variance decomposition, K-conditional surface, model-form sensitivity, failure modes, and revenue breakeven. This directly addresses Claude's Minor Concern #8 (abstract density) and substantially improves first-pass readability without sacrificing content.

2. **Logistic saturation equation now numbered (Eq. 14).** The logistic form $C_{\mathrm{labor}}(n) = C_{\mathrm{mat}} + (C_{\mathrm{Wright}}(n) - C_{\mathrm{mat}}) / (1 + (n/n_{\mathrm{half}})^2)$ is now a numbered equation (`\label{eq:logistic_saturation}`), cross-referenced in both the abstract and conclusion. This addresses my AL Minor Concern #3 and GPT's consensus request for a numbered equation.

3. **$C_{\mathrm{floor}}^{\mathrm{labor}}$ replaced with $C_{\mathrm{mat}}$.** The undefined quantity $C_{\mathrm{floor}}^{\mathrm{labor}}$ in the logistic formula has been replaced with $C_{\mathrm{mat}}$, which is defined earlier in the paper as the non-learnable per-unit material cost (\$1M). The text after the equation now states: "$C_{\mathrm{mat}} = m \cdot p_{\mathrm{fuel}}$ is the irreducible material cost (the natural labor-cost floor for Earth manufacturing)." This directly addresses Claude's AL Minor Concern #2.

4. **K-median sweep Det. N* column now says "(lump)" with caption clarification.** The column header reads "Det. $N^*$ (lump)" and the caption explicitly states: "Det. $N^*$ uses lump-sum $K$ at the listed median value (not phased); compare Table ref for phased baselines." This resolves the consensus concern (all three AL reviewers) about the Det. N* column appearing to contradict Table 8.

5. **Yield parameter acknowledged as deterministic-only.** The yield paragraph now includes an explicit justification: "Y is tested as a deterministic sensitivity parameter (Table ref), not a stochastic MC input, because the effect is small relative to $K$ and LR$_E$ variance ($<$0.5% of total output variance at $Y \geq 0.80$)." This addresses my AL Minor Concern #4 and Claude's Minor Concern #4.

6. **Logistic form acknowledged as deterministic-only.** The text following Eq. 14 states: "The logistic form has been tested at three deterministic parameter values; full stochastic integration would require specifying prior distributions for $n_{\mathrm{half}}$ and is deferred to future work." The abstract also notes: "both forms are tested deterministically only." This addresses my AL Minor Concern #4 and Claude's Minor Concern #3.

7. **Permanent/transient percentages now use % of converging runs in body.** The body text (permanent vs. transient crossovers paragraph) now reports: "of the 8,511 converging runs, 1,889 (22.2% of converging) achieve permanent crossover, while 6,622 (77.8%) achieve transient crossover." This matches the abstract's framing ("of converging runs, 22% are analytically permanent") and resolves Claude's Minor Concern #1.

8. **Eq. phased_capital labeled as $t_0 = 5$ special case.** The text preceding Eq. 20 now reads: "At the deterministic baseline ($t_0 = 5$), the coupled form reduces to:" -- explicitly identifying it as the special case of the general Eq. 8 ($t_0$-coupled formulation). This addresses GPT's Minor Issue #2.

9. **Dual $\sigma_{\ln}$ noted in abstract.** The first paragraph of the abstract now includes: "Results are reported at $\sigma_{\ln} = 0.70$ (megaproject reference class); a space-specific variant ($\sigma_{\ln} = 1.0$) appears in Table ref." This addresses Claude's Minor Concern #11.

10. **Code availability updated to AM.** The code availability section now references "version AM" rather than "version AL."

---

## Assessment of Specific AL-to-AM Changes

### Abstract Restructuring

The two-paragraph split is well-executed. The first paragraph delivers the headline result (85% convergence, conditional median ~4,300, KM median ~5,350, savings window 95%) with the $\sigma_{\ln}$ qualification. The second paragraph provides the sensitivity context (K-dominance, model-form spread, failure modes, revenue breakeven). A reader encountering the abstract for the first time can now absorb the primary finding before being confronted with the qualifications. This is a meaningful improvement in communication.

### Logistic Equation (Eq. 14) and $C_{\mathrm{mat}}$ Substitution

The logistic form now reads $C_{\mathrm{labor}}(n) = C_{\mathrm{mat}} + (C_{\mathrm{Wright}}(n) - C_{\mathrm{mat}}) / (1 + (n/n_{\mathrm{half}})^2)$, with $C_{\mathrm{mat}}$ defined in the text as $m \cdot p_{\mathrm{fuel}}$. The equation is numbered and cross-referenced in the abstract ("Eq. ref") and conclusion. This resolves both the undefined-quantity problem (Claude) and the traceability concern (Gemini, GPT).

**Minor observation:** The definition $C_{\mathrm{mat}} = m \cdot p_{\mathrm{fuel}}$ equates the Earth material cost floor with $m \cdot p_{\mathrm{fuel}}$ (mass times propellant floor), which is conceptually the launch cost floor, not the material cost. Earlier in the paper (Eq. 2), $C_{\mathrm{mat}} = \$1$M is defined as "the non-learnable per-unit material cost (aerospace-grade aluminum alloy at ~\$540/kg x 1,850 kg)." The reuse of $C_{\mathrm{mat}}$ to denote $m \cdot p_{\mathrm{fuel}} = 1{,}850 \times \$200 = \$0.37$M creates a notational collision: $C_{\mathrm{mat}}$ is \$1M in the Earth manufacturing context (Eq. 2) but \$0.37M in the logistic saturation context (Eq. 14). If the logistic form's floor is intended to be $m \cdot p_{\mathrm{fuel}}$, this should use a distinct symbol (e.g., $C_{\mathrm{floor}}^{E}$ or $C_{\mathrm{Earth}}^{\min}$) to avoid overloading $C_{\mathrm{mat}}$. Alternatively, if the intent is that the logistic form's floor should be $C_{\mathrm{mat}} = \$1$M (the actual material cost), the parenthetical definition "$C_{\mathrm{mat}} = m \cdot p_{\mathrm{fuel}}$" should be corrected. This is the only substantive concern I have with Version AM; it is a notational issue, not a modeling error, since the logistic form is tested deterministically and the exact floor value has modest impact on the crossover shift.

### K-Median Sweep Table

The column header "Det. $N^*$ (lump)" and the caption's explicit statement about lump-sum treatment fully resolve the ambiguity. The cross-reference to the config-to-crossover table for phased baselines is helpful. No further action needed.

### Deterministic-Only Acknowledgments

Both the yield parameter and the logistic form are now clearly identified as deterministic-only tests. The justification for excluding $Y$ from the MC (effect is <0.5% of total output variance) is quantitative and appropriate. The abstract's "both forms are tested deterministically only" is a commendably transparent disclosure for a headline claim. These changes resolve the consensus concerns from the AL round.

### Permanent/Transient Framing

The body text now consistently uses percentages of converging runs (22.2% permanent, 77.8% transient), matching the abstract. The raw counts (1,889 and 6,622) are retained for verifiability. This resolves Claude's concern cleanly.

### Phased Capital Equation

The preceding text for Eq. 20 now explicitly states "At the deterministic baseline ($t_0 = 5$), the coupled form reduces to:" -- making it clear that Eq. 20 is a special case of Eq. 8, not an alternative formulation. The subsequent paragraph explains the coupling mechanism for the MC case ($t_0 \sim U[3,8]$). This resolves GPT's Minor Issue #2.

---

## Remaining Major Concerns

None.

---

## Remaining Minor Concerns

1. **$C_{\mathrm{mat}}$ notational collision in Eq. 14.** As detailed above, $C_{\mathrm{mat}}$ is defined as \$1M (aerospace-grade aluminum alloy) in Eq. 2 but re-defined as $m \cdot p_{\mathrm{fuel}} = \$0.37$M in the text following Eq. 14. These are different quantities. The logistic equation's floor should use a distinct symbol, or the parenthetical definition should be corrected if the intent is to use the same \$1M material cost. This is a notational correction that does not require re-running any simulations.

2. **Config table (Table C.5): Dynamic vitamin fraction row.** The Baseline MC column shows "$\checkmark$ ($f_v^{\mathrm{floor}} \sim U[0.01,0.03]$)" while the Sensitivity variants column shows "$n_v \sim U[2000,10000]$." This presentation implies that $n_v$ is only varied as a sensitivity test, not sampled in the canonical MC. However, Table 1 (MC parameter distributions) lists $n_v \sim U[2{,}000, 10{,}000]$ under "Plateau & vitamin parameters" as a stochastic parameter in the baseline MC. The config table should show $n_v$ in the Baseline MC column (e.g., "$\checkmark$ ($f_v^{\mathrm{floor}} \sim U[0.01,0.03]$; $n_v \sim U[2000,10000]$)") or the Sensitivity variants column should be marked "---" if $n_v$ has no separate sensitivity sweep distinct from its baseline MC sampling. This was flagged as my AL Minor Concern #7 and remains unaddressed.

3. **Code availability commit hash.** The commit hash remains "PENDING" (line 1041). The version label has been updated to "AM," which is progress, but a fixed commit hash and a DOI-archived snapshot are required for final submission. This was flagged by all three AL reviewers.

4. **Sensitivity index table (Table 6) formatting.** The "Max shift" column continues to mix absolute units ($+$1,588), percentages ($-$16.5\%), qualitative labels ("varies," "---"), and mixed formats ($+$469 ($Y{=}0.70$)). While this was noted in both the AK and AL rounds, the table is legible and the information is complete. I withdraw this as a required change; it is an editorial preference rather than a technical deficiency. The authors may wish to standardize at their discretion.

5. **Convergence CDF table (Table 10) terminates at H = 20,000.** The table's last row shows $P(N^* \leq 20{,}000)$ = 80.6% at $r = 5\%$, while the MC summary reports Conv. = 85.1% at $H = 40{,}000$. The gap (80.6% to 85.1%) over the $H = 20{,}000$ to $H = 40{,}000$ range is not directly visible in the table. Adding an $H = 40{,}000$ row (which would read 91.9% / 85.1% / 75.0% to match Table 7) would close the loop for readers cross-checking consistency. Alternatively, a brief note referencing Figure 6 (convergence curve) for the continuous CDF would suffice. This was flagged as my AL Minor Concern #8 and remains unaddressed. It is truly minor and I do not consider it blocking.

---

## Positive Aspects

1. **Surgical precision of revisions.** Version AM addresses every consensus concern from the AL round without introducing new material that would require further review. The changes are targeted edits (equation numbering, column headers, paragraph splits, notational fixes) rather than structural additions. This demonstrates the maturity of the underlying analysis and the authors' responsiveness to reviewer feedback.

2. **Abstract readability.** The two-paragraph abstract is a genuine improvement. The first-time reader can now absorb the primary finding (crossover at ~4,300 units, 85% probability, savings window covering 95% of draws) before encountering the qualifications (K-dominance, model-form uncertainty, failure modes). The $\sigma_{\ln}$ dual-baseline reference in paragraph 1 is an elegant way to acknowledge the space-specific uncertainty class without cluttering the headline.

3. **Epistemic transparency.** The abstract now contains three explicit caveats in paragraph 2: (a) K explains 63% of variance and dominates the conditional surface; (b) both logistic and plateau forms are "tested deterministically only"; (c) three specific conditions prevent crossover. This level of self-qualification is rare in techno-economic analysis papers and substantially reduces the risk of misinterpretation.

4. **Internal consistency remains excellent.** Cross-checking headline statistics across the abstract, Tables 4, 5, 7, 8, 10, 11, 14, and the conclusion: convergence rate (85.1%), conditional median (4,311), KM median (~5,350), bootstrap CI ([4,198, 4,423] in body; [4,200, 4,420] rounded in abstract), savings window at 20k (94.7%), permanent fraction (22.2% of converging), and revenue breakeven (~\$0.94M/unit/yr) are all consistent. No numerical discrepancies detected.

5. **Decision-relevant framing.** The paper continues to provide a multi-dimensional decision toolkit: conditional median (for committed programs), KM median (for portfolio decisions), K-conditional surface (for readers with different priors), savings window probability (for finite-horizon planners), revenue breakeven (for revenue-generating infrastructure), and hybrid option value (for transition planning). This makes the paper useful across a wide range of stakeholder contexts.

---

## Summary

Version AM has addressed all eight consensus concerns from the AL review round. The logistic equation is now numbered and cross-referenceable. The K-median sweep column is unambiguous. The yield parameter and logistic form are explicitly identified as deterministic-only. The permanent/transient framing is consistent throughout. The abstract is more readable. The phased capital equation is correctly identified as a special case. The $\sigma_{\ln}$ dual baseline is referenced in the abstract.

The remaining concerns are minor: a notational collision in the logistic equation's floor definition, the config table's vitamin row presentation, the still-pending commit hash, and two presentational items carried forward from AL. None of these require re-running simulations or restructuring the analysis. The notational collision (Minor Concern #1) should be corrected in the proofs stage to prevent reader confusion, but it does not affect any numerical results because the logistic form is tested deterministically.

This paper is ready for publication. The combination of parametric NPV cost modeling, 10,000-run Monte Carlo with 20 stochastic parameters, model-form sensitivity testing, K-conditional framing, Kaplan-Meier survival analysis, and the multi-dimensional decision toolkit constitutes a genuine contribution to the ISRU economics literature. The epistemic transparency -- particularly the explicit acknowledgment that K explains 63% of variance with no direct empirical anchor, and that headline probabilities are conditional on both the assumed priors and the model structure -- sets a standard that future techno-economic analyses in this space would do well to emulate.
