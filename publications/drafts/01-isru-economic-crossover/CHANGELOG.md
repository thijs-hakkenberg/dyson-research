# CHANGELOG

Evolution of the ISRU Economic Crossover paper across 39 versions (A through AM),
documenting changes made in response to AI peer review (Claude Opus 4.6, Gemini 3 Pro, GPT-5.2).

---

## Version A (Initial Draft)
- Initial draft of the ISRU Economic Crossover paper
- Reviewer verdicts: Claude: Major Revision, Gemini: Major Revision, GPT: Major Revision

## Version A --> Version B
- Added discussion of limitations and acknowledged the need for NPV/discount rate analysis
- Addressed some bibliographic errors (O'Neill date mismatch partially)
- Minor refinements to related work section and tone
- Reviewer verdicts: Claude: Major Revision, Gemini: Major Revision, GPT: Major Revision

## Version B --> Version C
- Added Net Present Value (NPV) discounting formulation with pathway-specific delivery schedules
- Introduced Gaussian copula for correlated sampling between launch cost and ISRU capital
- Added Spearman rank correlations for global sensitivity analysis
- Added bootstrap confidence intervals on Monte Carlo statistics
- Added ISRU operational cost floor (C_floor) parameter
- Added parameter justification section (Section 3.5) grounding estimates in engineering analogy
- Expanded reference list substantially
- Reviewer verdicts: Claude: Major Revision, Gemini: Major Revision, GPT: Major Revision

## Version C --> Version D
- Separated delivery schedules: distinct Earth and ISRU production time models (Eqs. 6-9)
- Introduced closed-form inverse logistic function for ISRU schedule (Eq. 8-9)
- Removed S-curve cost divisor to avoid double-counting ramp-up in costs
- Diagnosed and explained the launch cost Spearman sign paradox via copula correlation analysis
- Added production schedule table showing timing gap between pathways
- Expanded sensitivity analysis with launch learning scenario, organizational forgetting test, and Earth ramp-up delay test
- Added ISRU transport cost term to the model
- Added mass penalty factor (alpha) parameter
- Reviewer verdicts: Claude: Major Revision, Gemini: Minor Revision, GPT: Major Revision

## Version D --> Version E
- Separated discount rate from stochastic parameters: now treated as fixed scenario parameter
- Ran Monte Carlo at fixed discount rates (r = 0%, 3%, 5%, 8%) for cleaner sensitivity interpretation
- Improved handling of non-convergence with conditional vs. unconditional statistics
- Added survival-style convergence reporting
- Added vitamin fraction model (Eq. 14) for Earth-sourced components
- Added stochastic C_floor and production rate parameters
- Expanded robustness tests including piecewise schedule, cash-flow timing, and Earth capex
- Reviewer verdicts: Claude: Major Revision, Gemini: Minor Revision, GPT: Major Revision

## Version E --> Version F
- Made production rate (n_max) stochastic with range [250, 750] units/year
- Added K-n_max correlation test (rho = 0.5)
- Added stochastic cost floor with U[$0.3M, $2.0M] range
- Refined parameter justification with bottom-up energy cost derivation for C_ops
- Added convergence diagnostics section
- Expanded sensitivity analysis with deterministic cost floor sweep
- Added launch learning sweep from 90-99%
- Added notation distinction between N*_0 (undiscounted) and N*_r (NPV crossover)
- Reviewer verdicts: Claude: Minor Revision, Gemini: Minor Revision, GPT: Major Revision

## Version F --> Version G
- Added comprehensive launch learning rate parametric sweep (90%-99%)
- Added fuel floor vs. operations decomposition sensitivity
- Added organizational forgetting sensitivity test
- Added vitamin fraction sensitivity analysis
- Added opportunity cost of delay discussion (Section 5.2) with revenue breakeven analysis
- Expanded convergence analysis with horizon-dependent reporting
- Refined claims about "structural asymmetry" with more careful caveating
- Reviewer verdicts: Claude: Major Revision, Gemini: Minor Revision, GPT: Major Revision

## Version G --> Version H
- Corrected vitamin fraction formulation: ISRU ops now scaled by (1-f_v) to avoid double-counting
- Added K-n_max correlation in Monte Carlo (rho = 0.5 test)
- Added piecewise schedule variant test
- Added cash-flow timing sensitivity (manufacturing lead time)
- Added Earth capex sensitivity test
- Added convergence curve (Figure 8) as P(N* <= H) across horizons
- Expanded parameter justification with capital decomposition table
- Added additive manufacturing learning rate citations
- Reviewer verdicts: Claude: Major Revision, Gemini: Minor Revision, GPT: Major Revision

## Version H --> Version I
- Resolved LR_E sign/interpretation issue in sensitivity discussion
- Added two-component launch cost model as extended analysis (fuel floor + learnable ops)
- Added fuel floor sensitivity sweep
- Expanded opportunity cost discussion with revenue breakeven rate (~$0.9M/unit/year)
- Added stochastic ramp-up time t_0 parameter
- Added explicit conflict of interest statement
- Expanded references with Dixit & Pindyck (real options), Benkard (organizational forgetting), Thompson (learning-by-doing)
- Reviewer verdicts: Claude: Major Revision, Gemini: Minor Revision, GPT: Major Revision

## Version I --> Version J
- Addressed launch cost learning indexing: acknowledged program-specific vs industry-wide learning
- Added explicit orbit definition (GEO reference case) with transport cost rationale
- Added convergence statistics at multiple horizons (H = 10k, 20k, 40k)
- Refined vitamin fraction model with clearer cost/mass fraction definitions
- Improved reproducibility documentation with code repository details
- Reviewer verdicts: Claude: Major Revision, Gemini: Minor Revision, GPT: Major Revision

## Version J --> Version K
- Added fuel floor sensitivity as stochastic parameter
- Resolved launch cost decomposition mapping in Monte Carlo
- Added explicit "theory of what is learning" statement for ISRU composite learning rate
- Expanded distributional sensitivity with triangular diagnostic for key parameters
- Added revenue breakeven as a more prominent result
- Improved discussion of censoring/selection effects in conditional median interpretation
- Reviewer verdicts: Claude: Major Revision, Gemini: Minor Revision, GPT: Major Revision

## Version K --> Version L
- Added revenue breakeven analysis as formal equation (Eq. 16) with structured discussion
- Added explicit NRE/Earth fixed-cost discussion and justification for exclusion
- Expanded launch learning indexing discussion with cumulative-mass alternative
- Added maintenance/recapex sensitivity parameter (beta)
- Improved convergence probability reporting as primary Monte Carlo output
- Reviewer verdicts: Claude: Major Revision, Gemini: Minor Revision, GPT: Major Revision

## Version L --> Version M
- Added maintenance cost parameter (beta) as formal model component
- Added launch learning indexing sensitivity (cumulative units vs cumulative mass)
- Expanded capex phasing with explicit beta test
- Added discussion connecting to specific infrastructure contexts (SSP, habitats)
- Improved statistical reporting with both conditional and unconditional sensitivity measures
- Reviewer verdicts: Claude: Major Revision, Gemini: Minor Revision, GPT: Major Revision

## Version M --> Version N
- Expanded to 11+ stochastic Monte Carlo parameters
- Added Kaplan-Meier censoring treatment for non-convergence
- Expanded to ~28 sensitivity analyses
- Added throughput constraint discussion (physical launch rate limits)
- Reviewer verdicts: Claude: Minor Revision, Gemini: Minor Revision, GPT: Major Revision

## Version N --> Version O
- Added availability parameter (A) to Monte Carlo as a stochastic variable
- Improved ISRU capital cost (K) justification with better decomposition table
- Refined vitamin fraction model and cost specification
- Reviewer verdicts: Claude: Major Revision, Gemini: Accept, GPT: Major Revision

## Version O --> Version P
- Added Earth pathway validation against known production programs (Starlink analogy)
- Strengthened parameter justification for K decomposition
- Reviewer verdicts: Claude: Major Revision, Gemini: Accept, GPT: Major Revision

## Version P --> Version Q
- Clarified orbit cost normalization (GEO vs LEO basis)
- Added re-crossing analysis: analytical asymptotic condition for permanent vs transient crossover
- Refined launch learning indexing discussion
- Reviewer verdicts: Claude: Minor Revision, Gemini: Accept, GPT: Major Revision

## Version Q --> Version R
- Added demand context table mapping crossover volumes to specific infrastructure architectures
- Further refined revenue breakeven analysis
- Improved terminology around launch cost "floor" vs "operational asymptote"
- Reviewer verdicts: Claude: Minor Revision, Gemini: Accept, GPT: Major Revision

## Version R --> Version S
- Added distributional robustness tests
- Expanded permanent vs transient crossover distinction
- Improved Spearman correlation table with conditional analysis
- Reviewer verdicts: Claude: Major Revision, Gemini: Minor Revision, GPT: Major Revision

## Version S --> Version T
- Added pathway-specific delivery schedule improvements
- Expanded KM survival analysis reporting
- Refined risk-adjusted discounting section with clearer interpretive caveats
- Added success probability framework and technical readiness discussion
- Reviewer verdicts: Claude: Minor Revision, Gemini: Minor Revision, GPT: Major Revision

## Version T --> Version T-H (Hotfix)
- Hotfix addressing specific issues flagged in Version T reviews
- Addressed vitamin fraction baseline justification and launch cost floor explanation
- Reviewer verdicts: Claude: Major Revision, Gemini: Minor Revision, GPT: Major Revision

## Version T-H --> Version U
- Added two-component Earth manufacturing cost model (materials floor + learnable labor)
- Improved ISRU production schedule equations for physical consistency
- Added PRCC (partial rank correlation coefficients) to sensitivity analysis
- Expanded revenue breakeven analysis
- Added permanent vs transient crossover classification to MC summary statistics
- Reviewer verdicts: Claude: Major Revision, Gemini: Accept, GPT: Major Revision

## Version U --> Version V
- Refined baseline model configuration clarity (which equations active in MC vs deterministic)
- Further improvements to sensitivity analysis reporting
- Reviewer verdicts: Claude: Major Revision, Gemini: Minor Revision, GPT: Major Revision

## Version V --> Version W
- Addressed "passive structure vs cost paradox" (if unit is simple enough for ISRU, why $75M on Earth?)
- Improved parameter justification for Earth first-unit cost
- Reviewer verdicts: Claude: Major Revision, Gemini: Minor Revision, GPT: Major Revision

## Version W --> Version X
- Fixed correlation inconsistencies (abstract vs table vs body text for copula parameters)
- Improved multivariate correlation matrix documentation
- Added variance decomposition improvements
- Reviewer verdicts: Claude: Major Revision, Gemini: Minor Revision, GPT: Major Revision

## Version X --> Version Y
- Improved global sensitivity analysis with PRCC and rank-regression R-squared
- Refined permanent vs transient crossover reporting
- Improved positioning as strategic parametric economics paper
- Reviewer verdicts: Claude: Major Revision, Gemini: Minor Revision, GPT: Major Revision

## Version Y --> Version Z
- Added model configuration table (baseline vs MC vs sensitivities)
- Further refined launch learning baseline definition
- Improved permanent/transient crossover classification
- Reviewer verdicts: Claude: Major Revision, Gemini: Accept, GPT: Major Revision

## Version Z --> Version AA
- Consolidated baseline model consistency across all analysis modes
- Improved abstract and conclusion framing
- Reviewer verdicts: Claude: Major Revision, Gemini: Accept, GPT: Major Revision

## Version AA --> Version AB
- Addressed baseline launch cost model inconsistencies (constant vs. two-component learning)
- Clarified vitamin fraction presentation (15% total vs. 5% irreducible)
- Added re-crossing volume estimates for transient crossover cases
- Improved code availability with version-specific repository reference
- Reviewer verdicts: Claude: Major Revision, Gemini: Minor Revision, GPT: Major Revision

## Version AB --> Version AC
- Refined vitamin fraction terminology and model clarity
- Addressed distributional assumption concerns (uniform priors and clipping justification)
- Improved permanent/transient crossover framing with savings window survival analysis
- Clarified parameter coherence constraints (Earth cost components, C_labor derivation)
- Reviewer verdicts: Claude: Major Revision, Gemini: Accept, GPT: Major Revision

## Version AC --> Version AD
- Added transport time to delivery schedule (lunar-to-GEO duration in NPV/revenue timing)
- Added coherence constraints ensuring C_mfg >= C_mat to prevent negative derived C_labor
- Introduced exact discounted annuity formulation for revenue breakeven
- Added dual sigma_ln baselines (0.70 terrestrial and 1.0 space-specific)
- Added Earth scaling penalty sensitivity test
- Reviewer verdicts: Claude: Major Revision, Gemini: Accept, GPT: Major Revision

## Version AD --> Version AE
- Resolved baseline definition contradictions around launch learning
- Standardized crossover probability reporting with explicit horizon H
- Clarified NRE/fixed cost treatment in Earth manufacturing learning curve
- Expanded correlation/schedule-risk treatment (K correlated with t_0 and A)
- Improved discounting/timing narrative
- Reviewer verdicts: Claude: Major Revision, Gemini: Minor Revision, GPT: Major Revision

## Version AE --> Version AF
- Elevated revenue breakeven / deployment delay finding to Abstract and Conclusion
- Strengthened vitamin cost justification and physical archetype definition
- Made phased capital K the baseline (replacing lump-sum at t=0)
- Elevated commercial discount rate viability finding (r > 20% kills business case) to abstract
- Improved abstract readability
- Reviewer verdicts: Claude: Major Revision, Gemini: Minor Revision, GPT: Major Revision

## Version AF --> Version AG
- Addressed market realism for production volume (~4,500 units context against real architectures)
- Clarified "physics-driven propellant floor" as "assumed operational asymptote"
- Added savings window survival analysis improvements
- Strengthened parameter distribution justification
- Reviewer verdicts: Claude: Major Revision, Gemini: Minor Revision, GPT: Major Revision

## Version AG --> Version AH
- Addressed hybrid strategy inconsistency (Table 14 negative option value)
- Coupled capex timing to construction schedule (linking phased K to t_0)
- Strengthened baseline unit cost realism with cost build-up context
- Reframed MC probabilities as "fraction of modeled scenario space" vs. predictive probabilities
- Established single consistent canonical baseline configuration
- Reviewer verdicts: Claude: Major Revision, Gemini: Minor Revision, GPT: Major Revision

## Version AH --> Version AI
- Created canonical configuration table (Table 8) anchoring to a single baseline
- Added parameter confidence assessment table (Table 5) with grounding quality ratings
- Added decision tree (Figure 7) synthesizing the analysis
- Resolved revenue breakeven inconsistency ($0.65M vs. $0.94M discrepancy)
- Improved permanent/transient terminology and savings window as primary decision metric
- Reviewer verdicts: Claude: Major Revision, Gemini: Minor Revision, GPT: Major Revision

## Version AI --> Version AJ
- Further refined learning plateau model formulation
- Strengthened schedule + phased capex coupling
- Addressed ISRU mass penalty alpha double-scaling concern
- Improved vitamin model asymptotic cost expression consistency
- Added demand context discussion for required production scales
- Addressed risk asymmetry between pathways (TRL 9 Earth vs. TRL 3-5 ISRU)
- Reviewer verdicts: Claude: Major Revision, Gemini: Accept, GPT: Major Revision

## Version AJ --> Version AK
- Added stochastic learning plateau parameters (n_break, eta) to canonical MC
- Added dynamic vitamin fraction model (f_v decays with production maturity)
- Elevated K-median sweep to primary result framing
- Promoted Kaplan-Meier survival analysis to main text
- Added logistic learning saturation comparison
- Added ISRU production yield parameter Y for quality/reliability modeling
- Updated NPV equation to explicitly show phased capex tranches with time-coupled discounting
- Regenerated all tables from single canonical pipeline
- Reviewer verdicts: Claude: Major Revision, Gemini: Accept, GPT: Major Revision

## Version AK --> Version AL
- K-median sweep elevated from appendix to main text (Table 10) as primary result surface
- Logistic saturation comparison added as model-form sensitivity test
- Yield parameter sweep covering Y = 0.70 to 1.0
- Block deployment discussion added for revenue breakeven
- Phased capex equation updated to explicitly show five annual tranches
- Stale tables regenerated from canonical pipeline; copula baseline now consistent at 85.1%/4,311
- Config table corrected (plateau and dynamic vitamin checkmarks)
- Abstract and conclusion updated with K-conditional surface, KM median, and logistic comparison
- Reviewer verdicts: Claude: Minor Revision, Gemini: Accept, GPT: Minor Revision

## Version AL --> Version AM (Final)
- Abstract split into two paragraphs for readability
- Logistic saturation formula numbered with cross-references
- Permanent/transient percentages unified to "% of converging runs" throughout
- Yield parameter explicitly acknowledged as deterministic-only with variance justification
- K-median sweep Det. N* column header clarified as "(lump)" with caption
- Phased capital equation labeled as special case of coupled equation
- Dual sigma_ln baseline noted in abstract with table reference
- **Reviewer verdicts: Claude: Minor Revision, Gemini: Accept, GPT: Accept (3/3 Accept-level)**

---

## Verdict Progression Summary

| Version | Claude | Gemini | GPT |
|---------|--------|--------|-----|
| A | Major | Major | Major |
| B | Major | Major | Major |
| C | Major | Major | Major |
| D | Major | **Minor** | Major |
| E | Major | Minor | Major |
| F | **Minor** | Minor | Major |
| G | Major | Minor | Major |
| H | Major | Minor | Major |
| I | Major | Minor | Major |
| J | Major | Minor | Major |
| K | Major | Minor | Major |
| L | Major | Minor | Major |
| M | Major | Minor | Major |
| N | Minor | Minor | Major |
| O | Major | **Accept** | Major |
| P | Major | Accept | Major |
| Q | Minor | Accept | Major |
| R | Minor | Accept | Major |
| S | Major | Minor | Major |
| T | Minor | Minor | Major |
| T-H | Major | Minor | Major |
| U | Major | **Accept** | Major |
| V | Major | Minor | Major |
| W | Major | Minor | Major |
| X | Major | Minor | Major |
| Y | Major | Minor | Major |
| Z | Major | **Accept** | Major |
| AA | Major | Accept | Major |
| AB | Major | Minor | Major |
| AC | Major | Accept | Major |
| AD | Major | Accept | Major |
| AE | Major | Minor | Major |
| AF | Major | Minor | Major |
| AG | Major | Minor | Major |
| AH | Major | Minor | Major |
| AI | Major | Minor | Major |
| AJ | Major | **Accept** | Major |
| AK | Major | Accept | Major |
| AL | **Minor** | Accept | **Minor** |
| AM | **Minor** | **Accept** | **Accept** |

**Key patterns:**
- **Gemini** was consistently the most favorable reviewer, reaching Accept as early as Version O and oscillating between Accept and Minor Revision thereafter.
- **GPT** was the most demanding, maintaining Major Revision for 38 consecutive versions before finally reaching Accept at Version AM. Its persistent concerns centered on cash-flow timing asymmetry, distributional assumptions, and baseline model definition consistency.
- **Claude** oscillated between Minor and Major Revision throughout, tending to raise new issues as old ones were resolved. It reached stable Minor Revision only at Version AL.
- The paper required 39 versions of iterative peer review to achieve 3/3 Accept-level consensus.
