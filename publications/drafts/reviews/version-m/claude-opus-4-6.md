---
paper: "01-isru-economic-crossover"
version: "m"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-16"
recommendation: "Major Revision"
---



# Peer Review: "Economic Inflection Points in Space Manufacturing: Monte Carlo Analysis of ISRU vs. Earth Launch for Large-Scale Space Infrastructure"

**Manuscript:** Version M
**Target Journal:** Advances in Space Research

---

## 1. Significance & Novelty

**Rating: 4 (Good)**

This paper addresses a genuine and important gap in the ISRU literature. As the authors correctly identify, most prior ISRU economic analyses are mission-specific (propellant production, water extraction, PGM mining) rather than generalizable to manufactured structural goods. The combination of Wright learning curves, pathway-specific NPV discounting, and Monte Carlo uncertainty propagation in a single comparative framework is, to my knowledge, novel. The separation of the discount rate from the stochastic parameter set is a methodologically sound choice that improves interpretability over earlier formulations.

The paper's most significant contribution is the probabilistic framing of the crossover question—reporting convergence probabilities (51–77%) rather than point estimates—which is far more useful for decision-makers than deterministic breakeven analyses. The finding that the discount rate primarily affects *whether* crossover occurs rather than *where* it occurs (conditional median stable at ~5,100–5,900 across r ∈ [3%, 8%]) is a genuinely useful insight for space policy. The revenue breakeven analysis (§Discussion) adds an important dimension that pure cost-minimization models miss.

However, the novelty claim should be tempered. The individual components—Wright learning curves, NPV analysis, Monte Carlo simulation—are all well-established. The contribution is in their integration and application to the ISRU-vs-launch question, not in methodological innovation per se. The paper would benefit from more explicitly positioning itself relative to Sowers (2021, 2023), who also uses NPV analysis for lunar resource economics, and Ishimatsu et al. (2016), whose multicommodity network flow model addresses a related logistics optimization problem. The claim in §1 that no prior work provides "a schedule-aware NPV crossover model" for generic manufactured products should be verified more carefully against the recent cislunar economics literature.

## 2. Methodological Soundness

**Rating: 3 (Adequate)**

The parametric cost model is clearly specified and internally consistent. The two-component launch cost structure (irreducible propellant floor + learnable operations) is well-motivated by the Zapata (2019) analysis and represents a meaningful improvement over single-parameter launch cost models. The pathway-specific delivery schedules with integrated logistic ramp-up are physically reasonable, and the closed-form inverse (Eq. 9) is a useful analytical convenience. The extensive robustness testing (23+ sensitivity analyses) is commendable and unusual for this literature.

However, several methodological concerns require attention:

**Learning curve application.** The Wright learning curve is applied to cumulative *units* for both Earth manufacturing and ISRU operations, but the two pathways have fundamentally different cost structures. Earth manufacturing of 1,850 kg structural modules is a labor/capital-intensive process where unit-level learning is well-documented. ISRU "operational cost" (Eq. 11) bundles energy, consumables, remote operations overhead, and quality assurance—these are process costs, not unit production costs in the traditional Wright sense. Process industries (chemicals, refining) typically exhibit learning in *yield* and *throughput* rather than in per-unit cost, and the appropriate model may be a log-linear relationship with cumulative *throughput* rather than cumulative *units*. The authors acknowledge this implicitly by including a cost floor, but the functional form of the learning curve for ISRU operations deserves more scrutiny. The analogy to additive manufacturing learning rates (Baumers et al., 2016) is the strongest empirical anchor, but additive manufacturing operates in a controlled terrestrial environment with human operators—the extrapolation to autonomous extraterrestrial processing is a significant leap.

**Monte Carlo design.** The 11-parameter Monte Carlo with Gaussian copula is adequate but has limitations the authors partially acknowledge. The use of uniform distributions for 7 of 11 parameters represents "maximal ignorance" but also means the results are sensitive to the *bounds* rather than the *shape* of the distributions. The authors test triangular distributions and find <200-unit shifts, which is reassuring, but the bounds themselves (e.g., K ∈ [$30B, $100B]) are the real assumption. More critically, the 40,000-unit planning horizon introduces right-censoring that affects 23–49% of runs. The authors acknowledge this and propose AFT regression as future work, but the current treatment—reporting conditional statistics on converging runs—can produce misleading summaries if the censoring mechanism is informative (which it is: non-convergence is correlated with parameter values). The Cohen's d analysis partially addresses this, but a more rigorous treatment is needed.

**Production schedule modeling.** The logistic ramp-up function (Eq. 7) with fixed k = 2.0 is a reasonable first approximation, but k is not varied in the Monte Carlo despite being a consequential parameter. The piecewise schedule test (§4.9) shows zero sensitivity, but this is because the test only adds a hard cutoff before the logistic midpoint—it does not test slower ramp-ups (lower k) or delayed full-capacity achievement. Given that the ramp-up timing directly affects the NPV calculation, k should either be included as a stochastic parameter or its fixed value should be more rigorously justified.

**Discount rate treatment.** Running the Monte Carlo at fixed discount rates is defensible, but the paper does not adequately discuss *which* discount rate is appropriate for this class of investment. The reference to Arrow et al. (2014) on declining discount rates is apt but underdeveloped. For a 20–40 year infrastructure program, the Ramsey rule and intergenerational equity considerations suggest that a constant 5% rate may be too high for the social discount rate, while the commercial rate discussion (§4.12) correctly identifies the financing constraint. The paper would benefit from a brief discussion of the appropriate discount rate framework for megastructure-class investments.

## 3. Validity & Logic

**Rating: 4 (Good)**

The conclusions are generally well-supported by the analysis, and the authors are admirably transparent about limitations. The probabilistic framing (51–77% convergence) avoids the overconfidence that plagues many ISRU advocacy papers. The explicit identification of conditions under which crossover *fails*—vitamin costs >$50k/kg, discount rates >12%, success probability <69%—is valuable and honest.

Several logical issues merit attention:

The claim that "per-kilogram launch costs exhibit limited learning compared to manufacturing" (§1, and reiterated throughout) is central to the paper's thesis but is stated more strongly than the evidence supports. The two-component model with LR_L = 0.97 is one parameterization; the actual mechanism by which launch costs decline (reusability, flight rate, operational efficiency) may not follow a Wright curve at all. The Zapata (2019) analysis shows that Falcon 9 cost reductions came primarily from fixed-cost amortization at high flight rates—a mechanism that *does* scale with cumulative launches but through a different functional form than the Wright curve. The paper should acknowledge that the Wright model for launch cost learning is a convenience, not an empirically validated relationship.

The revenue breakeven analysis (Eq. 17) is an important addition but is somewhat buried in the Discussion. The finding that at $2M/yr revenue per unit, the Earth pathway is preferred on a utility-maximizing basis despite being more expensive on a cost-minimizing basis is potentially the paper's most policy-relevant result. This deserves more prominent treatment—possibly its own subsection in Results.

The "counterintuitive" result that risk-adjusted discounting *reduces* the crossover (§4.11) is correctly identified as an artifact of the discounting mechanism rather than a genuine risk assessment. The caveat paragraph is well-written, but the section title "Risk-adjusted discounting" may mislead readers who skim. Consider retitling to "Differential discounting sensitivity" or similar.

The throughput constraint discussion (§5.1) makes a compelling qualitative argument but, as the authors note, is not integrated into the quantitative model. The claim that "at scales of 10^5 units and beyond, the throughput argument for ISRU may prove even more decisive than the economic argument" is plausible but unsubstantiated within the paper's framework. Either integrate it quantitatively or soften the claim.

## 4. Clarity & Structure

**Rating: 4 (Good)**

The paper is exceptionally well-organized for its length and complexity. The model description (§3) is clear and self-contained, with each equation building logically on the previous one. The extensive use of tables for parameter justification (Tables 1–4) and results summary (Tables 5–9) aids comprehension. The separation of deterministic results, sensitivity analysis, and Monte Carlo robustness into distinct subsections is effective.

The abstract is accurate and comprehensive, though at 250+ words it is long for ASR (typical limit: 200 words). It should be tightened—the list of robustness tests can be condensed.

The paper is, however, very long. At approximately 12,000–15,000 words of body text plus extensive tables and figures, it exceeds the typical length for ASR research articles. Several sections could be condensed without loss of substance: the parameter justification (§3.4) repeats information from Table 2; the sensitivity analysis (§4.2) reports many small-effect results that could be summarized in a single table; and the Discussion limitations section (§5.4) reads more like a research agenda than a focused discussion of the current paper's constraints. I would recommend moving some of the robustness tests (piecewise schedule, launch re-indexing, cash-flow timing, Earth-side fixed costs) to supplementary material, as they all show small effects and primarily serve to demonstrate thoroughness rather than to alter conclusions.

The notation is generally consistent, but the overloading of $n$ as both unit index and cumulative production count could confuse readers in places (e.g., Eq. 4 vs. Eq. 8). The distinction between $N^*_0$ (undiscounted) and $N^*_r$ (NPV) introduced in §3.2.3 is not consistently maintained—later sections use $N^*$ ambiguously.

Figures are referenced but not viewable in this review; based on the captions and text references, they appear well-chosen and appropriately labeled. The tornado diagram (Fig. 4), histogram (Fig. 6), and convergence curve (Fig. 8) are standard and effective visualization choices for this type of analysis.

## 5. Ethical Compliance

**Rating: 5 (Excellent)**

The AI-assisted methodology disclosure (footnote 1) is exemplary—clear, specific, and appropriately scoped. The distinction between AI use for "literature synthesis, editorial review, and peer review simulation" versus human-authored simulation code with independent verification is precisely the kind of transparency that should become standard practice. The conflict of interest statement is clear. The open-source code availability commitment enhances reproducibility.

One minor note: the affiliation "Project Dyson, Open Research Initiative" is not a recognized institution. While this does not raise ethical concerns per se, the journal may require clarification of the author's institutional affiliation and qualifications. The single-author nature of the paper, combined with the AI assistance disclosure, may prompt questions about the depth of domain expertise—the paper's technical quality largely addresses this concern, but a brief author biography or ORCID link would help.

## 6. Scope & Referencing

**Rating: 4 (Good)**

The paper is well-suited to ASR's scope, which encompasses space economics, mission design, and technology assessment. The reference list (40 items) is adequate and covers the major relevant works: O'Neill (1974/1976) for historical context, Sanders & Larson (2015) for ISRU economics, Wright (1936) and Argote & Epple (1990) for learning curves, and Jones (2018/2020/2022) for launch cost trajectories.

Several gaps in the referencing should be addressed:

- The paper does not cite Benaroya (2010, "Turning Dust to Gold") or Benaroya & Bernold (2008), which provide engineering-economic analyses of lunar construction that are directly relevant.
- The real options literature for space systems is cited (Saleh et al., 2003; de Weck et al., 2004) but the more recent work by Lamassoure & Hastings (2002, "A framework to account for flexibility in modeling the value of on-orbit servicing") and Jilla & Miller (2004) on flexibility in space system design should be considered.
- The bootstrapping/self-replication literature beyond Metzger et al. (2013) is thin—Metzger's more recent work (2016, 2020) on lunar industrial development should be cited.
- The paper cites Cilliers et al. (2023) for regolith processing but does not reference the substantial body of work on lunar regolith simulant processing (e.g., Meurisse et al., 2018; Jakus et al., 2017) that provides empirical data on sintering yields and energy requirements.
- The NASA Artemis Cost Assessment (OIG, 2021) would provide a more current anchor for the $K$ parameter than the 2015 NASA Cost Estimating Handbook.

The Jones (2018, 2020, 2022) references are all conference papers (ICES); while appropriate, the paper would benefit from citing peer-reviewed journal articles on launch cost trends where available.

---

## Major Issues

1. **ISRU learning curve functional form (§3.2.2, Eq. 11).** The application of a unit-level Wright learning curve to ISRU operational costs is not adequately justified. ISRU operations are process-intensive (energy, throughput, yield) rather than unit-intensive (labor hours per unit). The paper should either (a) provide a more detailed argument for why the Wright model applies to process costs in this context, (b) test an alternative functional form (e.g., learning in throughput/yield rather than per-unit cost), or (c) explicitly bound the error introduced by this modeling choice. The boundary test at LR_I = 1.0 partially addresses this but does not test alternative functional forms.

2. **Right-censoring treatment (§4.3).** With 23–49% of Monte Carlo runs censored at H = 40,000, the conditional statistics (median, IQR) reported as primary results are computed on a non-representative subsample. The paper acknowledges this and proposes AFT regression as future work, but this is a methodological gap that should be addressed in the current version. At minimum, a Kaplan-Meier estimator of the crossover "survival function" should be reported alongside the conditional statistics, and the paper should clearly state that the conditional median is a *lower bound* on the true median of the full (uncensored) distribution.

3. **S-curve steepness parameter k (§3.2.1).** The parameter k = 2.0 is fixed throughout the analysis despite controlling the ramp-up dynamics that directly affect the NPV calculation. The justification ("moderately aggressive ramp-up consistent with industrial commissioning timelines") is vague. This parameter should either be (a) included in the Monte Carlo with a justified range, or (b) subjected to a dedicated sensitivity sweep showing the crossover response to k ∈ [0.5, 4.0]. The piecewise schedule test (§4.9) does not substitute for this because it tests a different aspect of the schedule (hard cutoff vs. continuous).

4. **Absence of Earth manufacturing cost floor (§3.1, §5.4).** The paper acknowledges in the Discussion that Earth manufacturing at high volumes might transition to industrial-class production with a cost floor, but does not implement this in the model. This is a significant asymmetry: the ISRU pathway has an explicit cost floor ($C_{\text{floor}}$), but the Earth pathway's manufacturing cost declines without bound under the Wright curve. At N = 40,000 with LR_E = 0.85, the Earth manufacturing cost per unit falls to ~$75M × 40,000^{-0.234} ≈ $4.5M—still above the launch cost, so the omission may not be material. But the paper should verify this numerically and either implement an Earth manufacturing floor or demonstrate that its absence does not affect the crossover.

5. **Single-product assumption and capital utilization.** The model assumes the entire $30–100B ISRU capital investment is dedicated to producing a single product type. In practice, any facility of this scale would produce multiple product types, and the capital amortization would be shared. The paper mentions this in §3.5 ("multi-product ISRU facilities with shared infrastructure would shift the crossover earlier") but does not quantify the effect. Even a simple two-product model (structural modules + propellant) with shared power and excavation infrastructure would substantially reduce the effective K per product line and could shift the crossover by thousands of units.

---

## Minor Issues

1. **Eq. 8, constant term.** The statement "$N(t_0) = 0$" with the $-\ln 2$ constant is correct, but the physical interpretation is slightly awkward: at the logistic midpoint, cumulative production is zero but the instantaneous rate is half-maximal. This means the facility is "running" but has produced nothing—a modeling artifact. A brief note acknowledging this would help.

2. **Table 1 (production schedule).** The column "$S(t_{n,I})$" shows $S = 0.50$ at $n = 1$, but $n = 1$ is produced at $t_{n,I} = 5.00$ which is exactly $t_0$. This is consistent with the model but may confuse readers who expect the first unit to be produced during ramp-up, not at the midpoint.

3. **§3.4, first-unit manufacturing cost.** The Starlink comparison is helpful but the back-calculation is not shown. At LR_E = 0.85 and 6,000 units, the implied first-unit cost is ~$250k × 6000^{0.234} ≈ $2.5M—not "orders of magnitude higher" than $250k. The comparison should be made more carefully or removed.

4. **§4.2, fuel floor sensitivity.** The statement that the crossover shifts by "only ±54 units" across the fuel floor sweep is reassuring but the sweep range ($50–$400/kg) is quite narrow relative to the total launch cost ($1,000/kg). This should be noted.

5. **§4.3, convergence diagnostic.** The statement that the conditional median "stabilizes within ±2% of the final value by n = 5,000" is adequate but a formal convergence criterion (e.g., Gelman-Rubin statistic or running-mean plot) would be more rigorous.

6. **§4.4, phased capital.** The five-year uniform tranche assumption is arbitrary. Real infrastructure deployment would likely be front-loaded (site preparation, power systems) with declining annual investment. A non-uniform phasing schedule would be more realistic.

7. **Eq. 17 (revenue breakeven).** The denominator sums $\delta_n \cdot (1+r)^{-t_{n,I}}$, but the discounting should arguably be at $t_{n,E}$ (the time at which Earth revenue begins) rather than $t_{n,I}$, since the lost revenue occurs during the interval $[t_{n,E}, t_{n,I}]$. The current formulation may underestimate $R^*$.

8. **§3.2.2, Eq. 11.** The transport cost term $m \cdot p_{\text{transport}} \cdot \alpha$ is outside the learning curve brackets, implying transport cost does not decline with experience. This is reasonable for propellant-dominated transport but should be stated explicitly.

9. **Table 6 (scenarios).** The "Time" column header should specify which delivery schedule is used (ISRU, per the text note).

10. **Throughout.** The paper uses "crossover" and "convergence" somewhat interchangeably in the Monte Carlo context. "Convergence" typically refers to the Monte Carlo simulation converging (i.e., statistics stabilizing with sample size), not to the cost curves crossing. Consider using "crossover achievement" or "crossover occurrence" consistently.

11. **§1, paragraph 2.** The claim that "the ten-thousandth kilogram launched costs nearly the same as the first in per-kg terms" is an overstatement given the paper's own two-component model with LR_L = 0.97. At 10,000 units, the ops component has declined by ~30%. Soften to "exhibits modest learning."

12. **Abstract.** At ~280 words, this exceeds ASR's 200-word guideline. The list of robustness tests should be condensed to a single sentence.

---

## Overall Recommendation

**Major Revision**

This is a well-conceived and thoroughly executed paper that addresses a genuine gap in the ISRU economics literature. The probabilistic framing, pathway-specific NPV formulation, and extensive robustness testing represent a meaningful advance over existing point-estimate analyses. The paper is clearly written, transparently documented, and commendably honest about limitations.

However, several methodological issues require substantive revision before publication: (1) the ISRU learning curve functional form needs stronger justification or alternative testing; (2) the right-censoring of 23–49% of Monte Carlo runs requires more rigorous statistical treatment than conditional statistics alone; (3) the fixed S-curve steepness parameter k should be varied or rigorously justified; and (4) the asymmetric treatment of cost floors (present for ISRU, absent for Earth manufacturing) introduces a structural bias that should be quantified. The paper is also substantially longer than typical ASR articles and would benefit from moving secondary robustness tests to supplementary material. None of these issues are fatal—they are addressable within a single revision cycle—but they collectively prevent acceptance in the current form.

---

## Constructive Suggestions

1. **Implement a Kaplan-Meier survival analysis for the crossover distribution.** Treat "crossover at unit N" as a time-to-event outcome with right-censoring at H = 40,000. Report the Kaplan-Meier median (which accounts for censoring) alongside the current conditional median. If the two differ substantially, the current conditional statistics are misleading. This is computationally trivial and would substantially strengthen the statistical rigor. Consider also fitting a parametric survival model (Weibull or log-normal AFT) to obtain regression coefficients for each parameter.

2. **Add an Earth manufacturing cost floor and test its impact.** Implement $C_{\text{mfg}}(n) = \max(C_{\text{mfg}}^{(1)} \cdot n^{b_E},\; C_{\text{mfg,floor}})$ with $C_{\text{mfg,floor}}$ representing the irreducible materials and tooling cost per unit (plausibly $2–10M for a 1,850 kg structural module). This creates symmetric treatment with the ISRU cost floor and tests whether the crossover is robust to Earth manufacturing reaching commodity-like costs at high volumes. If the crossover persists, this strengthens the paper's conclusions; if it doesn't, this is an important finding.

3. **Vary k in the Monte Carlo or provide a dedicated sensitivity sweep.** The S-curve steepness directly controls how quickly ISRU production ramps up, which affects the NPV timing gap that is central to the paper's crossover calculation. Test k ∈ [0.5, 4.0] (corresponding to ramp-ups from ~6 months to ~4 years from 10% to 90% capacity) and report the crossover sensitivity. If k is as influential as the ramp-up time $t_0$, it should be a stochastic parameter; if not, the fixed value is justified.

4. **Promote the revenue breakeven analysis to a Results subsection.** The finding that ISRU may not be preferred for revenue-generating infrastructure at revenue rates above ~$1M/unit/year is arguably the paper's most policy-relevant result, but it is currently buried in the Discussion. Formalize it with a figure showing $R^*$ as a function of production volume and discount rate, and discuss the implications for space solar power (the paper's motivating application) explicitly.

5. **Condense the paper by 20–30%.** Move the following to supplementary material: piecewise schedule test (§4.9, zero effect), launch re-indexing test (§4.2, ±18 units), cash-flow timing sensitivity (§4.10, small effect), Earth-side fixed costs (§4.11, straightforward), and the copula/distribution sensitivity diagnostics (§4.3). Retain the results in a summary table but remove the detailed prose. This would bring the paper within ASR length norms and improve readability without sacrificing rigor.