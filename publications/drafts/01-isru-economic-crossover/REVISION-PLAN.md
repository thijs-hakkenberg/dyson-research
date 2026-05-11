# Paper 01 — Revision Plan from Version AM → Resubmission

**Paper:** Economic Inflection Points in Space Manufacturing
**Peer-reviewed version:** `am` (frozen, see `01-isru-economic-crossover-am.tex`)
**Working version:** `an` (modular structure, see `01-isru-economic-crossover-an.tex` + `sections/` + `tables/`)
**Target venue:** *Advances in Space Research*

## Verdict to address

The three new-model peer reviews on version `am` returned:

| Reviewer | Verdict |
|---|---|
| Claude Opus 4.7 | **Major Revision** |
| Gemini 3.1 Pro | Accept with Minor Revisions |
| GPT-5.5 Pro | **Major Revision** |

Two of three require Major Revision. The reviews and the synthesis deck are in `reviews/version-am/`; the headline issue (raised independently by Claude and GPT-5.5) is that the abstract's "95% of draws" savings-window claim is a *conditional* probability reported as if it were *unconditional* — true value ≈ 80.6%.

## Issue inventory

Each issue ID is referenced below in the proposed revision sequence. *Reviewer* column: **C** = Claude 4.7, **G** = Gemini 3.1 Pro, **O** = GPT-5.5 Pro. Effort: T = trivial (≤30 min), L = low (≤2 h), M = medium (≤1 day), H = high (multi-day, requires re-run).

| ID | Reviewer | Description | Files affected | Effort |
|----|----|---|---|---|
| **M1** | C+O | Conditional vs unconditional savings-window probability misreport (95% → ≈80.6%). | `sections/00-frontmatter.tex` (abstract), `sections/04-results.tex` (4.3.x narrative), `sections/06-conclusion.tex`, `tables/savings_survival.tex` (caption + columns) | L |
| **M2** | C | Soften "functionally permanent" → "no re-crossing within $N=200{,}000$." Run subset (~500) at $N=10^6$ to characterize uncensored $N^{**}$ tail. | `sections/04-results.tex` §4.4, `sections/05-discussion.tex`, `sections/06-conclusion.tex`, `sections/00-frontmatter.tex`, `tables/recrossing.tex`, `publications/scripts/isru_mc.py` (extended-bound sweep) | M |
| **M3** | O | NPV not service-equivalent — ISRU's later delivery means its costs are discounted more. Add a common-deadline or shadow-service-value sensitivity. | `publications/scripts/isru_mc.py` (new sensitivity case), `publications/scripts/isru_model.py` (delayed-Earth comparison), new section `sections/04-results.tex` §4.6 (or extend §4.4), `sections/05-discussion.tex` | H |
| **M4** | C+G+O | Logistic saturation only deterministic — asymmetric vs stochastically-integrated piecewise plateau. Either stochastically integrate logistic or condition the headline 85% on the chosen form. | `publications/scripts/isru_mc.py` (logistic alternative as MC variant), `tables/logistic_comparison.tex`, `sections/04-results.tex` §4.3 | H |
| **M5** | C+O | Decompose $p_s$ into catastrophic-failure component (sunk K, all-or-nothing) and degraded-operations component (already in MC via low $A$, high $C_{\mathrm{ops}}^{(1)}$). Avoid double-counting. | `publications/scripts/isru_mc.py` (split $p_s$), `tables/ps_horizon.tex`, `sections/04-results.tex` §4.6, `sections/05-discussion.tex` | H |
| **M6** | C+G+O | Earth learning offset $n_0$ buried in appendix; sensitivity is dramatic (1,111 to >40,000 units). Promote to main text and integrate stochastically (e.g., $n_0 \sim \text{Uniform}[0, 300]$). | `publications/scripts/isru_mc.py` (add stochastic $n_0$), `publications/scripts/isru_model.py` (Earth learning curve takes $n_0$), `sections/03-model.tex` §3.1, `sections/04-results.tex` §4.2, move `tables/n0_lr_interaction.tex` from appendix → main | H |
| **M7** | C+O | Anchor $K$ against terrestrial heavy industry (offshore platforms, refineries, modular nuclear). Add recurring maintenance/spares term to canonical MC (currently appendix-only; shifts crossover by 1.4k–5.5k units). | `sections/03-model.tex` §3.2 + §3.4, `publications/scripts/isru_mc.py` (canonical with maintenance), `tables/params.tex`, new table `tables/k_anchor.tex`, references in `sections/99-bibliography.tex` | H |
| **M8** | C+O | Vitamin BOM 15% vs 5% reconciliation. Either model initial 15% decaying to a floor, or relabel to distinguish "Earth-sourced at early maturity" from "irreducible modeled vitamin fraction." Clarify where coatings/seals/sensors/wiring costs enter. | `tables/vitamin_bom.tex`, `sections/03-model.tex` §3.2 (vitamin definition), `publications/scripts/isru_model.py` (if dynamic update needed) | M |
| **M9** | C+G+O | Technology obsolescence too thin for 30–40 year horizons. Either add stochastic Poisson disruption model OR explicitly downgrade robustness claims; minimum: structured matrix varying disruption timing × magnitude × affected pathway. | `publications/scripts/isru_mc.py` (Poisson disruption), `sections/04-results.tex` (new disruption analysis), `sections/05-discussion.tex` §5.5 | H |
| **M10** | G+O | Decision-tree figure should show uncertainty (threshold ranges, $K$-dependent crossover probability, horizon-dependent $p_s^{\min}$). | `publications/scripts/generate_isru_figures.py` (decision_tree fig), `sections/05-discussion.tex` §5.4 | M |
| **M11** | G | Block-deployment revenue dynamics for SSP-style architectures — current eq. (28) overstates delay penalty. Provide a 2–3 sentence heuristic estimate even if full derivation is deferred. | `sections/05-discussion.tex` §5.2.2 | T |
| **M12** | O | Audit launch-learning numerical examples. At $n=10{,}000$, LR$_L=0.90$, learnable component should be ≈\$200/kg, not ≈\$334/kg. Add unit tests for analytical $n^b$ values. | `publications/scripts/isru_model.py` (`earth_unit_cost_launch_learning`), `publications/scripts/tests/test_isru_model.py`, `sections/04-results.tex` (numerical examples) | M |
| **M13** | O | Asymptotic cost-floor thresholds inconsistent with stated equations. Re-derive $C_{\mathrm{floor}}$ under each active configuration (constant launch, launch-learning, dynamic vitamin, plateau) using exact code expressions. | `sections/03-model.tex`, `sections/04-results.tex` §4.5 | M |
| **M14** | O | PRCC for $t_0$ interpretation backwards in narrative — negative PRCC means higher $t_0$ *lowers* crossover volume (not "delays"). Clarify volume vs calendar-time effects. | `sections/04-results.tex` §4.2 (Spearman/PRCC narrative), `tables/spearman.tex` if interpretation column present | T |
| **M15** | O | $\sigma_{\ln}$ description: for unclipped lognormal, P90/P50 = $\exp(1.2816\sigma)$ ≈ 3.6 at $\sigma=1$, not 4.1. State whether ratios are theoretical or clipped. | `sections/03-model.tex` §3.3, `tables/sigma_ln.tex` | T |
| **M16** | O | Stochastic parameter count: 19 independent + 2 derived, not 18 + 2. | `sections/00-frontmatter.tex` (abstract), `sections/03-model.tex`, `tables/params.tex` | T |
| **M17** | O | Avoid "100.0%" claims from finite MC. Use binomial CIs or "no re-crossings observed within 100,000 units." | `sections/04-results.tex`, `tables/savings_survival.tex` | T |
| **M18** | O | Earth cost driver framing: at crossover, manufacturing cost still > launch cost. Reframe as "Earth recurring manufacturing + launch floor, with LR$_E$ as dominant non-capital uncertainty." | `sections/04-results.tex`, `sections/05-discussion.tex` | L |
| **M19** | C+G+O | Residual "validate"/"validated" phrasing (e.g., "validate the PRCC rankings"). Replace with "support" / "corroborate" / "are consistent with". | `grep -rn` across all `sections/*.tex` | T |
| **M20** | C+O | Code commit hash "PENDING" — must be resolved. Frozen release tag, DOI archive, requirements file, seed, test suite, exact reproduction command. | `sections/90-back-matter.tex` (Code Availability), `publications/scripts/` release tag, Zenodo upload | L |
| **M21** | C | Manuscript length / table proliferation. Move secondary tables (Yield, K-clip, copula-6D, etc.) entirely to appendix; consolidate permanent/transient/savings-window framework into one subsection. | `sections/04-results.tex` (move tables), `sections/91-appendix-a-supplementary-sensitivity.tex` (receive), restructure §4.x | M |

Total: 21 issues. Of those, 6 are trivial (T), 5 low (L), 5 medium (M), 5 high (H — require code change + MC re-run).

## Proposed revision sequence

Each version letter is one Git revision tag with a specific scope. Most revisions are paper-only; only `aq`, `ar`, `as`, `at` require simulation work.

### Version `ao` — Easy paper-only fixes (1–2 days, no simulation)

**Scope:** Everything that can be fixed by editing text + table captions, without re-running the MC. This buys most of the "credibility hygiene" critique cheaply.

- **M1** (relabel savings-window probabilities as conditional/unconditional in abstract, results narrative, conclusion, table caption — values like 80.6% already exist in `tables/convergence.tex`)
- **M11** (block-deployment heuristic in §5.2.2)
- **M14** (PRCC for $t_0$ interpretation correction)
- **M15** (σ_ln description fix)
- **M16** (parameter count 18 → 19 audit)
- **M17** (binomial CIs for "100%" claims)
- **M18** (Earth cost driver framing)
- **M19** (`grep -nE "validat(e|ed|ion)"` over `sections/*.tex` and replace contextually)
- **M20** (resolve code commit hash; tag release; Zenodo deposit)

**Sanity check:** abstract probabilities in `sections/00-frontmatter.tex` match table values in `tables/savings_survival.tex` and `tables/convergence.tex` after edit; `tectonic` recompiles to 61-page PDF.

### Version `ap` — Numerical audit + soften permanence language (2–3 days)

**Scope:** Items requiring careful re-derivation but no model changes.

- **M2** (soften "functionally permanent"; can defer the $N=10^6$ subset run to `aq` since it's an MC re-run)
- **M12** (audit `earth_unit_cost_launch_learning` in `publications/scripts/isru_model.py:298`; add `tests/test_isru_model.py` cases for stated learning rates)
- **M13** (rederive asymptotic cost-floor thresholds)
- **M21** (move secondary tables to appendix; consolidate permanent/transient narrative)

**Sanity check:** `pytest publications/scripts/tests/test_isru_model.py` passes with new analytical-value tests; numerical examples in `sections/04-results.tex` match audited values; appendix length increases, main-text §4 length decreases.

### Version `aq` — Service-equivalence + uncensored re-crossing (1 week, requires MC re-run)

**Scope:** First simulation re-run cycle. These two need a single MC sweep each.

- **M3** (add common-deadline NPV sensitivity case to `isru_mc.py`; new function `find_crossover_npv_common_deadline` in `isru_model.py`; add a results subsection — proposed §4.4 "Service-equivalent comparison")
- **M2 simulation half** (subset run at $N=10^6$ to estimate uncensored $N^{**}$ tail; report fraction of transient runs whose true $N^{**}$ falls below 1M, 10M)

**Sanity check:** new tables (e.g., `tables/service_equivalent.tex`, updated `tables/recrossing.tex`) compile and reference correctly; the 80.6% unconditional savings-window number is unchanged or moves only marginally; uncensored $N^{**}$ tail report supports the softened permanence language.

### Version `ar` — Model-form symmetry + $p_s$ decomposition (1–2 weeks, MC re-run)

**Scope:** The two methodologically deep changes flagged by Claude.

- **M4** (stochastic logistic saturation: add `sample_logistic_saturation_params` to `isru_mc.py`, run as MC variant; update `tables/logistic_comparison.tex` to compare both stochastically; report joint convergence rate; condition headline 85% if results diverge)
- **M5** ($p_s$ decomposition: split into `p_s_catastrophic` (binary, sunk K) and `p_s_degraded` (already in MC); update `tables/ps_horizon.tex`; revise §4.6 narrative to avoid double-counting)

**Sanity check:** model-form-robustness statement in abstract is now supportable as written; $p_s^{\min}$ threshold reflects only catastrophic risk; new run-time for the canonical MC ≤ 2× the old (logistic stochastic adds parameters but not loops).

### Version `as` — Vitamin BOM + n_0 + K anchor + maintenance (1–2 weeks, MC re-run)

**Scope:** Three of the more conceptually demanding fixes.

- **M6** (stochastic $n_0$: add to `Params` dataclass in `isru_model.py`; sample $n_0 \sim \text{Uniform}[0, 300]$ in `isru_mc.py`; promote `tables/n0_lr_interaction.tex` from appendix → main §4.2; revise narrative on whether the modeled program class is "first-of-kind" or "follow-on")
- **M7** ($K$ anchor: write a 1–2 page subsection cross-checking $K$ median against a terrestrial reference class — proposed: lithium DLE plant, offshore platform, modular nuclear; add `tables/k_anchor.tex`; new bibliography entries; add maintenance/spares term to canonical MC — `m_maint` in `Params`, sampled from `Uniform`/`LogNormal`)
- **M8** (vitamin BOM reconciliation: decide between (a) initial 15% decaying to floor or (b) relabel; table caption + content rewrite)

**Sanity check:** canonical MC convergence rate may move (likely down) — that's expected and honest; new headline numbers reported with both old and new framing for one revision before old framing is retired.

### Version `at` — Technology obsolescence + decision-tree uncertainty (1 week)

**Scope:** Final substantive content fix.

- **M9** (Poisson disruption model: $\lambda$, magnitude distribution, affected pathway; integrate into MC; report convergence rate under disruption; OR if too costly, replace deterministic two-scenario test with a 6-scenario matrix and explicitly downgrade robustness claim)
- **M10** (decision-tree uncertainty annotations: regenerate via `generate_isru_figures.py`; either replace existing figure or add a probabilistic companion)

### Version `au` — Final polish + response letter (3–5 days)

- Re-read pass for consistency (terminology, table cross-refs, bibliography)
- Generate a `RESPONSE-TO-REVIEWERS.md` mapping each peer-review issue to its revision and quoting the changed text
- Final code archival (Zenodo DOI minted; URL in `90-back-matter.tex`)
- Submit to *Advances in Space Research*

## Files map (where each kind of edit lands)

| Concern | Primary files |
|---|---|
| Abstract & headline numbers | `sections/00-frontmatter.tex` |
| Model formulation | `sections/03-model.tex`, `publications/scripts/isru_model.py` |
| Monte Carlo configuration & sampling | `publications/scripts/isru_mc.py` |
| Sensitivity sweeps & extended runs | `publications/scripts/extended_copula_sensitivity.py` |
| Result narrative | `sections/04-results.tex` |
| Decision framework, disruption, policy | `sections/05-discussion.tex` |
| Conclusions | `sections/06-conclusion.tex` |
| Code availability, COI, acknowledgments | `sections/90-back-matter.tex` |
| Appendix supplementary | `sections/91-…` through `sections/95-…` |
| Bibliography | `sections/99-bibliography.tex` |
| Tables | `tables/<label>.tex` (one per `\label{tab:…}`) |
| Figures | `figures/*.pdf` produced by `publications/scripts/generate_isru_figures.py` |
| Tests | `publications/scripts/tests/test_isru_*.py` |

## Verification protocol

After each version landing:

1. **`tectonic 01-isru-economic-crossover-<version>.tex`** must compile to a 60–80 page PDF with no undefined references.
2. **`pytest publications/scripts/tests/test_isru_*.py`** must pass.
3. For versions with MC re-runs (`aq` onward), regenerate any tables that depend on canonical numbers — a one-line `python3 -m publications.scripts.isru_mc --canonical` style invocation should produce the reference numbers; cross-check 3 numbers in the abstract and §4 against the regenerated tables.
4. Run `node scripts/run-paper-review.js --version=<version>` once per version and read the new-model verdicts. The signal we're targeting: at least two of three new-model reviewers move from "Major Revision" to "Accept with Minor Revisions" or "Accept" by version `at`.
5. After `at`, run a final pass with the older trio (`scripts/run-peer-review.js --paper=01 --version=at`) to confirm the peer-review-tracking history shows the trajectory.

## Open questions for the user

These should be resolved before starting `ao`:

1. **Vitamin BOM resolution path (M8)**: prefer dynamic 15%→floor model, or relabel to distinguish? The dynamic model is more honest but adds a parameter; the relabel is cheaper. The reviewers asked for one or the other, not both.
2. **Technology obsolescence (M9)**: full Poisson disruption model, or 6-scenario matrix with explicit downgrade of robustness claims? The Poisson model is "right"; the matrix is cheaper and still defensible.
3. **K-anchor reference class (M7)**: which terrestrial benchmark should ground the $K$ median — offshore platform, lithium DLE plant, modular nuclear, or something else? Pick one or two; reviewers asked for "at least one."
4. **Manuscript length (M21)**: Claude flagged ~50 pages / >20 tables as too dense. Are we comfortable being aggressive about pushing secondary tables to appendix even at the cost of some main-text continuity?
5. **Submission target**: still *Advances in Space Research*, or has the analysis matured to consider *Acta Astronautica* or *Journal of Spacecraft and Rockets*? Affects formatting and tone of revisions.

## Estimated total effort

| Phase | Effort |
|---|---|
| `ao` paper-only fixes | 1–2 days |
| `ap` numerical audit | 2–3 days |
| `aq` service-equivalence + uncensored $N^{**}$ | 1 week |
| `ar` model-form + $p_s$ decomposition | 1–2 weeks |
| `as` vitamin/$n_0$/$K$/maintenance | 1–2 weeks |
| `at` obsolescence + decision tree | 1 week |
| `au` polish + response letter | 3–5 days |
| **Total** | **5–7 weeks** |

The first three versions (`ao`, `ap`, `aq`) deliver ~70% of the credibility lift for ~25% of the effort. The remaining versions are where the substantive scientific revisions live.
