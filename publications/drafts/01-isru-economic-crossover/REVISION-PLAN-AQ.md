# Paper 01 — Version AQ Detailed Plan

**Cycle:** First simulation/MC re-run cycle (AQ).
**Inputs:** AP reviews (`reviews/version-ap/{claude-opus-4-7,gemini-3-1-pro,gpt-5-5-pro}.md`).
**Headline targets:** convert one of the three Major-Revision reviewers (most plausibly Claude) toward Accept-w-Minor by directly resolving the right-censoring critique that's been the central obstacle since AM, and address the timing/NPV-equivalence problem that GPT-5.5 has flagged in every round.
**Effort budget:** 5–7 working days. ~1 week.
**No code refactor of the canonical MC** beyond the additions enumerated below; parameter set unchanged.

## What changed since the high-level REVISION-PLAN

The AP reviews surfaced 6 substantive new methodological concerns that weren't catalogued in the original plan (M22–M28). They're the natural simulation/methodology cycle work and belong in AQ, not in AR/AS/AT. Catalogue first, then design.

## Issue inventory for AQ

Reviewer attribution: **C** = Claude 4.7, **O** = GPT-5.5 Pro, **G** = Gemini 3.1.

### Primary — require new simulation runs

| ID | Reviewer | Description | Files (sim + paper) |
|----|----|---|---|
| **M3** | O (×3) | NPV not service-equivalent — ISRU's later delivery means costs discount more, biasing cost-only NPV toward the slower pathway. Need at least one common-timing variant (common deadline OR optimally-delayed Earth OR explicit shadow-service-value). | `isru_model.py` (new `find_crossover_npv_common_deadline`), `isru_mc.py` (new MC variant), new §4.x subsection, abstract update |
| **M2-sim** | C+O+G | Right-censored $N^{**}$ at 200,000 undermines the headline savings-window framing. Need extended-bound subset run (1,000–2,000 transient runs to $N=10^6$ or $10^7$) to convert Wilson lower bound into empirical tail distribution. | `isru_mc.py` (extended-bound subset runner), `isru_model.py` (`find_recrossing_volume` with configurable bound), updated `tables/recrossing.tex`, new §4.4 paragraph |
| **M24** | O | Hybrid transition `Eq. eq:hybrid` sums ISRU costs from $n=N^*+1$ to $N$, which gives ISRU the learning benefit of having already produced $N^*$ units (those units were Earth-produced). Bug. | `isru_model.py` (re-index hybrid), regenerate `tables/hybrid.tex`, §5.x narrative correction |
| **M28** | O | Capital phasing in `Eq. eq:crossover_npv` discounts tranches at $t_0-5+y$. With $t_0\sim U[3,8]$, some draws place capex before $t=0$, contradicting the stated program start. Either redefine $t=0$ or constrain $t_0\ge 5$ (or distribute capex over $[0,t_0]$). Re-run canonical MC. | `isru_model.py` (`find_crossover_npv_phased` capex schedule), `isru_mc.py` (parameter-bound update), all canonical headline numbers re-validated |

### Secondary — analytic / paper-only companions to the primary work

| ID | Reviewer | Description | Files |
|----|----|---|---|
| **M22** | O | $K$ vs $K_{\mathrm{eff}}$ consistency audit. Several equations (`eq:recrossing`, hybrid, success-probability) use $K$ where $K_{\mathrm{eff}}$ (the phased+discounted form) is the active quantity. Notation cleanup; no new physics. | `sections/03-model.tex`, `sections/04-results.tex` (multiple eq references) |
| **M23** | O | Active-cost-function definitions. After vitamins / yield / plateau / launch-learning are introduced, equations still reference generic $C_{\mathrm{ops}}(n)$. Define $C_{E,\mathrm{active}}(n)$ and $C_{I,\mathrm{active}}(n)$ explicitly (one display equation each in §3) and use everywhere. | `sections/03-model.tex` (two new display eqs), references in `sections/04-results.tex` and `sections/05-discussion.tex` |
| **M25** | O | Analytic discounted-tail bound for re-crossing. Under positive discounting, an undiscounted asymptotic per-unit disadvantage may not produce a finite re-crossing because future differences attenuate. Add a bound: classify each transient run as (a) asymptotic-permanent, (b) discounted-permanent (tail bound proves no finite re-crossing), (c) finite re-crossing observed, (d) right-censored. Pairs with M2-sim. | `isru_model.py` (`classify_run_permanence` helper), `tables/recrossing.tex` (new column), §4.4 narrative |
| **M26** | O | Numerical consistency audit. Appendix convergence-curve text says $P(N^*\le 10{,}000) \approx 60\%$, Table~`convergence` gives 68.6%. Other stale numbers may exist. Build a `consistency_check.py` script that regenerates every headline number from the canonical MC and dumps a comparison table; fix any drifts. | New `publications/scripts/consistency_check.py`, fixes in `sections/91-appendix-a-supplementary-sensitivity.tex` and elsewhere |

### Opportunistic — low-cost cleanups that complement the simulation work

| ID | Reviewer | Description | Files |
|----|----|---|---|
| **M27** | C+O | Abstract too dense (six numerical estimates, two CIs, two $\sigma_{\ln}$ baselines). Trim to the three most decision-relevant numbers. Lead with the K-conditional framing per Claude's recommendation: "85% at K-median \$65B; 92% at \$50B; 46% at \$150B" rather than the canonical 85% as if unconditional. | `sections/00-frontmatter.tex` |
| **M34** | G | "planned for the next revision" is self-referential and inappropriate in a published manuscript. Global replace with "deferred to future work" or remove. | All `sections/*.tex`, `tables/*.tex` |
| **M30** | C | `\fnref{fn1}` for AI-disclosure footnote is on the address rather than the author byline. Move to author. | `sections/00-frontmatter.tex` |
| **M31** | C | `Eq. 13` (`C_ops^vit`) uses $p_{\mathrm{launch,eff}}(n)$ but the symbol isn't defined locally; readers must trace back to Eq. 9. Add a 1-line gloss. | `sections/03-model.tex` |
| **M32** | C | Iridium NEXT cross-check implies LR ≈ 0.79 at the boundary of the prior $\mathcal{N}(0.85, 0.03)$ truncated at [0.75, 0.95]. Either widen the prior or note the boundary case explicitly. | `sections/91-appendix-a-supplementary-sensitivity.tex`, possibly `tables/params.tex` |
| **M33** | C | `Eq. 14` (dynamic $f_v(n)$) — the asymptotic-permanence note (uses $f_v^{\mathrm{floor}}$ at large $n$) is several pages later. Move to immediate vicinity of the equation. | `sections/03-model.tex` |
| **M19'** | O | `Kaplan-Meier` "unbiased median" → "censoring-adjusted median estimate"; "operational asymptote" → "assumed architecture-dependent cost floor"; minor wording. | Multiple sections |
| **M21+** | C | §3 is ~12 pages; the \$74M $C_{\mathrm{labor}}^{(1)}$ build-up and the four-config $C_{\mathrm{floor}}^{\max}$ table can move to Appendix D with brief in-text summaries. | `sections/03-model.tex`, `sections/94-appendix-d-parameter-justification.tex` |

### Deferred (not in AQ)

| ID | Reason |
|---|---|
| M4 (stochastic logistic) | Targeted for AR — distinct concern about model-form propagation deserves its own version. |
| M6 (stochastic n_0 in MC) | Targeted for AS — pairs naturally with the K-anchor work. |
| M7 (four K-anchors) | Targeted for AS. |
| M8 (vitamin BOM dynamic 15%→floor) | Targeted for AS. |
| M9 (Poisson disruption model) | Targeted for AT. |
| M10 (decision tree uncertainty annotations) | Targeted for AT. |
| M29 (p_s distribution over MC) | Could fit AT alongside M9; not core to AQ's NPV-timing scope. |

---

## Implementation design — primary issues

### M3 — Service-equivalent NPV variant

**Two formulations, run as separate MC variants alongside the canonical:**

1. **Common-deadline variant.** Both pathways must deliver $N$ units by the same calendar date $T^*$. Earth manufacturing rate is dialed down (or up) so the Earth pathway also commissions at $t_0^{\mathrm{ISRU}}$ and reaches $N$ by $T^*$. This eliminates the discount-favoring of the slower pathway.
2. **Shadow-service-value variant.** Add a per-unit-per-year service value $v_{\mathrm{service}}$ to the NPV objective; the pathway with later delivery loses NPV proportional to delivery delay × shadow value. Default $v_{\mathrm{service}} = 0$ recovers cost-only; a sensitivity sweep at $v_{\mathrm{service}} \in \{0, R^*/2, R^*, 2R^*\}$ shows how the cost-equivalence assumption affects the conclusion.

**Code locations:**

- `publications/scripts/isru_model.py` — new pure functions:
  ```python
  def find_crossover_npv_common_deadline(params: Params, deadline_years: float) -> float: ...
  def find_crossover_npv_with_service_value(params: Params, v_service: float) -> float: ...
  ```
  Both reuse existing `cumulative_npv` machinery; common-deadline rescales Earth's `\dot{n}_{\max}` per run; shadow-value adds an `r_star_npv_term` to both pathways.

- `publications/scripts/isru_mc.py` — new variant flag `service_equivalent: bool` (or three: `common_deadline`, `shadow_value`); when set, the per-run loop calls the appropriate `find_crossover_npv_*` function instead of the default.

- New tests in `tests/test_isru_model.py`:
  - `TestCommonDeadline::test_common_deadline_increases_N_star_or_eliminates`: at $r > 0$, common-deadline should never make $N^*$ smaller than the cost-only version.
  - `TestShadowServiceValue::test_zero_service_value_recovers_cost_only`: with $v_{\mathrm{service}} = 0$, results match canonical to ±1 unit.
  - `TestShadowServiceValue::test_high_service_value_eliminates_crossover`: at $v_{\mathrm{service}} = 5 R^*$, no crossover should occur.

**Paper integration:**

- New §4.6 ("Service-equivalent comparison") between the existing §4.5 (cost-floor threshold) and §4.6 (technical success probability — renumber to §4.7). 4–6 paragraphs:
  - Motivation (the cost-only NPV asymmetry; cite the GPT-5.5 critique implicitly via the negative $t_0$ PRCC observation).
  - Common-deadline result (one new headline number, e.g., "under common-deadline, conditional median crossover shifts from 4,311 to 5,260 units" — placeholder pending the actual run).
  - Shadow-service-value sweep table (small, 4 rows × 3 cols: $v_{\mathrm{service}} \in \{0, R^*/2, R^*, 2R^*\}$ × {convergence rate, median $N^*$, savings window prob}).
  - One-paragraph reconciliation: cost-only NPV is the lower bound on Earth's preferred regime; service-equivalent NPV is closer to the policy-relevant case.
- Abstract sentence added: "Under a service-equivalent comparison (common deadline), crossover shifts to ≈$N$ units with X% convergence, indicating the cost-only result is a lower bound on the ISRU advantage."
- Discussion §5.2 — explicit note that the revenue-breakeven analysis is a special case of the shadow-service-value model.

### M2-sim — Extended-bound $N^{**}$ characterization

**Run a subset of the existing canonical MC's 6,622 transient runs through an extended search.** Choose the subset by stratified sampling on $K$ (so the extended runs span the same K-distribution as the full ensemble). 1,500 transient runs is enough to characterize quintiles cheaply:

- Search bound for the subset: $N = 10^7$ (50× the original).
- The discount factor at $r=5\%$ over an additional 35 years (rough conversion of $5 \times 10^6$ extra units at 500 units/yr) is $e^{-1.75} \approx 0.17$, so most transient runs that are "discounted-permanent" (no finite re-crossing) will be confirmed; most that are "asymptotic-permanent only" (finite but very-late re-crossing) will be revealed.
- Computational budget: 1,500 runs × 50× horizon ≈ 75 million unit-evaluations. The current MC is 10,000 runs × 200,000 horizon = 2 billion unit-evaluations, so this is ~4% additional compute. Trivial.

**Code locations:**

- `publications/scripts/isru_model.py:find_recrossing_volume` — already exists; verify it accepts a `max_n` argument (or extend it to do so).
- `publications/scripts/isru_mc.py` — new helper `run_extended_recrossing_subset(canonical_results, subset_size=1500, max_n=10_000_000)` that:
  1. Selects 1,500 transient runs via stratified sampling on K.
  2. Re-runs `find_recrossing_volume` with `max_n=10_000_000`.
  3. Returns per-run $N^{**}$ values plus right-censoring flag.
  4. Computes empirical tail distribution.

**Paper integration:**

- `tables/recrossing.tex` gets a new section / sub-table:
  ```
  Extended-bound subset (1,500 transient runs, search to N = 10^7):
    N** P10  ........  > 10^7 (X% censored)
    N** P50  ........  $X
    N** P90  ........  $Y
    Discounted-permanent fraction (no finite re-crossing): Z%
  ```
- §4.4 paragraph rewritten to lead with the extended-bound result and frame the original 200,000 search bound as the headline for computational tractability.
- Abstract phrasing tightened: "78% are technically transient; of these, X% are discounted-permanent (no finite re-crossing within $N \le 10^7$) and Y% have observed median $N^{**}$ at Z."

### M24 — Hybrid transition strategy ISRU learning re-indexing

**The bug:** `Eq. eq:hybrid` (in `sections/05-discussion.tex` or `04-results.tex` — verify) sums ISRU costs from $n = N^* + 1$ to $N$. ISRU's first hybrid-built unit should be cost $C_{\mathrm{ops}}(j=1)$, not $C_{\mathrm{ops}}(j=N^* + 1)$. The current formulation undercounts ISRU's hybrid cost by the learning savings ISRU couldn't actually have realized.

**Fix:** Re-index the ISRU branch with $j = 1, \ldots, N - N_{\mathrm{switch}}$ where $N_{\mathrm{switch}} = N^*$. Use $C_{I,\mathrm{active}}(j)$ (M23's active cost function) at index $j$, not at $n = N^* + j$.

**Code locations:**

- `publications/scripts/isru_model.py` — find the hybrid implementation (likely in or near `find_crossover_npv` if hybrid is integrated, or a separate `compute_hybrid_savings` function — locate via `grep -n "hybrid\|N_switch" publications/scripts/*.py`).
- Re-run hybrid table generation (`tables/hybrid.tex`) and the §5.3 (hybrid strategy) narrative.
- Add `TestHybridIndexing::test_isru_branch_starts_at_unit_one`: explicit unit test that the hybrid ISRU branch's first cost equals $C_{I,\mathrm{active}}(1)$, not $C_{I,\mathrm{active}}(N^* + 1)$.

**Paper integration:**

- §5.3 narrative: re-state the hybrid value at the corrected indexing. The hybrid value will likely DECREASE (since the previous formulation was over-crediting). Note this honestly in the discussion.
- Revise any abstract / conclusion claim about hybrid value at scales ≥ 20,000 units; the new threshold may be different.

### M28 — Capital phasing negative-time cash flow

**The issue:** Eq. crossover_npv assumes $K$ tranches paid in years $[t_0 - 5, t_0)$. If $t_0 < 5$, some tranches are at negative time, contradicting the program start at $t = 0$.

**Two acceptable fixes — pick one:**

- **(A) Constrain the prior:** $t_0 \sim U[5, 10]$ instead of $U[3, 8]$. Justification: 5 years is plausibly the minimum lunar-surface ISRU plant construction time given delivery + assembly + commissioning. This shifts the canonical median $t_0$ from 5.5 to 7.5 years. Re-run canonical MC.
- **(B) Rephase capex:** Distribute $K$ uniformly over $[0, t_0]$ rather than $[t_0 - 5, t_0)$. This avoids negative time and ties capex spending to construction duration directly. Re-run canonical MC.

**Recommendation: (A).** It's a tighter prior with a defensible engineering justification (Sowers et al. lunar architecture studies put plant construction at 5–8 years), and it preserves the $K_{\mathrm{eff}}$ NPV convention without changing the cash-flow model. (B) would require redefining $K_{\mathrm{eff}}$ derivation, which propagates further. Document the choice in §3.

**Code locations:**

- `publications/scripts/isru_model.py` — `Params` bound for `t_0` updated; `PARAM_BOUNDS["t0_years"]` changed to `(5, 10)`.
- `publications/scripts/isru_mc.py` — verify sampling uses the bound.
- All canonical MC headline numbers re-validated. The expected effects:
  - Convergence rate: likely DECREASES slightly (3–5 pp) because longer t_0 means more discount of K but also of the program start.
  - Conditional median: slightly higher (longer ISRU ramp delays crossover in volume).
  - Savings-window probability: roughly unchanged.

**Paper integration:**

- §3.3 (parameter justification) — add a short paragraph on the t_0 lower bound and its engineering justification.
- §4 — update all canonical headline numbers (this is the main reason AQ is a simulation cycle).
- Tables `params`, `convergence`, `mc_summary`, `savings_survival`, `recrossing` — regenerate.
- Abstract — update headline numbers to match.

---

## Implementation design — secondary issues

### M22 — K vs K_eff consistency

Audit equations across `sections/03-model.tex`, `04-results.tex`, `05-discussion.tex` for uses of $K$ that should be $K_{\mathrm{eff}}$:

- `eq:crossover_npv` — already uses $K_{\mathrm{eff}}$ (verify).
- `eq:recrossing` — likely uses $K$, should use $K_{\mathrm{eff}}$ (GPT-5.5's specific call-out).
- `eq:hybrid` — needs review along with M24 fix.
- `eq:p_success` — `p_s^{min} = K / (S + K)` — likely uses $K$, should use $K_{\mathrm{eff}}$.
- Asymptotic-permanence threshold derivation — uses $K$ where the discounted form is irrelevant (asymptotic per-unit cost doesn't include capital). OK to keep $K$ here.

For each usage, add a comment in the equation's neighborhood clarifying which form is used and why.

### M23 — Active cost function definitions

In `sections/03-model.tex`, after the model is fully described (post-vitamin, post-plateau, post-launch-learning subsections), add a "Summary: active unit-cost functions" subsection with two display equations:

```latex
\subsection{Summary: active unit-cost functions}\label{sec:active_costs}

The full Earth and ISRU per-unit cost functions used in the canonical Monte Carlo are:
\begin{align}
  C_{E,\mathrm{active}}(n; \theta) &= C_{\mathrm{mat}} + C_{\mathrm{labor}}^{(1)} (n + n_0)^{b_E} \cdot \min(1, \eta + (1-\eta)(n_{\mathrm{break}}/n)^{|b_E|}) + m \cdot \left[p_{\mathrm{fuel}} + p_{\mathrm{ops}} \cdot n^{b_L}\right] \\
  C_{I,\mathrm{active}}(n; \theta) &= \frac{1}{Y} \left[\alpha \cdot \max\left(C_{\mathrm{floor}}, C_{\mathrm{ops}}^{(1)} n^{b_I}\right) + m \cdot p_{\mathrm{transport}} \cdot \alpha\right] + f_v(n) \cdot m \cdot (p_{\mathrm{fuel}} + c_{\mathrm{vit}})
\end{align}

where $f_v(n) = f_v^{\mathrm{floor}} + (f_v^{(0)} - f_v^{\mathrm{floor}}) e^{-n/n_v}$. All subsequent equations (NPV, re-crossing, hybrid, success-probability) use these definitions.
```

References to generic $C_{\mathrm{ops}}(n)$ in `eq:crossover_npv`, `eq:recrossing`, `eq:hybrid` get replaced with $C_{I,\mathrm{active}}(n)$ or $C_{E,\mathrm{active}}(n)$ as appropriate.

### M25 — Analytic discounted-tail bound

For each transient run with $N^*$ converging, compute the discounted tail bound:

$$\Delta_{\mathrm{tail}}(N) = \sum_{n=N+1}^{\infty} \frac{C_{I,\mathrm{active}}(n) - C_{E,\mathrm{active}}(n)}{(1+r)^{t(n)}}$$

If $\Delta_{\mathrm{tail}}(N) > -\Sigma_{\mathrm{ISRU}}^{\mathrm{advantage}}(N)$ for all reachable $N$ within the budget, then no finite re-crossing exists in the discounted-cumulative metric (run is "discounted-permanent"). Otherwise, re-crossing might exist; check empirically (M2-sim).

The tail can be bounded analytically: for $n > n_{\mathrm{break}}$, both $C_E$ and $C_I$ have asymptotes (M13's table), and the difference $C_I^{\mathrm{asymp}} - C_E^{\mathrm{asymp}}$ is constant. The tail sum becomes a geometric series:

$$\Delta_{\mathrm{tail}}(N) = (C_I^{\mathrm{asymp}} - C_E^{\mathrm{asymp}}) \cdot \frac{(1+r)^{-t(N)}}{1 - (1+r)^{-1/\dot{n}_{\max}}}$$

Add as a helper:

```python
def classify_run_permanence(params: Params, n_star: float, max_n: float = 200_000) -> str:
    """Returns one of:
      "asymptotic_permanent" — C_I^asymp < C_E^asymp; permanent in undiscounted per-unit terms
      "discounted_permanent" — re-crossing impossible in discounted-cumulative metric
                                (analytic tail bound proves no finite N**)
      "finite_recrossing"     — re-crossing observed within max_n
      "right_censored"        — search horizon exhausted; permanence indeterminate
    """
```

`tables/recrossing.tex` gets a new column showing the count in each class. Combined with M2-sim, the paper can report:

> "Of 6,622 transient runs (canonical MC, 78% of converging), X are asymptotic-permanent, Y are discounted-permanent (analytic tail bound), Z have observed finite re-crossing (median $N^{**} = W$), and the remaining are right-censored beyond the extended search horizon $N = 10^7$."

### M26 — Numerical consistency audit

New script `publications/scripts/consistency_check.py`:

```python
"""Regenerate every headline number cited in the manuscript from the canonical MC
and emit a comparison table. Fails (exit nonzero) if any cited number drifts
from the regenerated value by more than the stated tolerance.
"""
```

Walks the `sections/*.tex` files via grep to extract numerical claims, regenerates each from the canonical run, prints a side-by-side table, exits nonzero on disagreements.

For the AP review issue specifically: the appendix paragraph says "$P(N^* \le 10{,}000) \approx 60\%$ at $r = 5\%$" while `tables/convergence.tex` says 68.6%. Either the appendix paragraph is from an older configuration (lump-sum K, before phased K) or it's a stale number — find which and reconcile.

The script becomes a pre-commit-style check for future revisions.

---

## Implementation design — opportunistic cleanups

### M27 — Abstract restructure (K-conditional surface as headline)

Old (current AP):
> ...A 10,000-run Monte Carlo at $r = 5\%$ (canonical configuration: Table 1) finds crossover in 85.1% of draws (conditional median ~4,300; KM median ~5,350; 95% CI: [4,200, 4,420]). Of converging runs, 22% are analytically permanent; the remaining 78% show no re-crossing within the searched horizon $N=200,000$ (this savings-window characterization is therefore a lower bound; uncensored characterization is planned for the next revision)....

New (target AQ):
> Across a 10,000-run Monte Carlo with $r = 5\%$, the crossover rate is highly $K$-dependent: 92% at $K$-median \$50B, 85% at \$65B (canonical), and 46% at \$150B (Table $K$-median sweep). At the canonical point the conditional median is ~4,300 units (KM median ~5,350; 95% CI: [4,200, 4,420]). 78% of converging runs show no re-crossing within $N = 10^7$ (extended subset; X% are discounted-permanent, Y% asymptotic-permanent), confirming that the savings-window framing is robust to the right-censoring concern. Under a service-equivalent (common-deadline) comparison, the crossover shifts to ~$N$ with W% convergence — the cost-only result is a lower bound on the ISRU advantage....

(Six numerical estimates → four; remove the explicit 95% bootstrap CI in favor of single point estimates; remove the "next revision" caveat since it's resolved; add the K-conditional surface and the service-equivalence sentence.)

### M34 — "next revision" language sweep

Global search-and-replace across `sections/*.tex` and `tables/*.tex`:
- "the next revision" → "future work"
- "planned for the next revision" → (delete; replace with a positive statement about what's there now)
- "committed for the next revision" → "deferred to future work"

### M30 — fnref relocation

`sections/00-frontmatter.tex` — move `\fnref{fn1}` from `\address[dyson]{...\fnref{fn1}}` to `\author[dyson]{Thijs Hakkenberg\corref{cor1}\fnref{fn1}}`.

### M31 — Eq. 13 symbol gloss

`sections/03-model.tex`, in the vicinity of the vitamin/ops cost equation that uses $p_{\mathrm{launch,eff}}(n)$: add a parenthetical "(where $p_{\mathrm{launch,eff}}(n) = p_{\mathrm{fuel}} + p_{\mathrm{ops}} \cdot n^{b_L}$ is the effective per-kg launch cost from Eq.~\ref{eq:earth_launch_learn})".

### M32 — Iridium NEXT cross-check tension

Appendix-A — add one sentence acknowledging that the implied LR ≈ 0.79 from the Iridium cross-check sits at the lower boundary of the prior $\mathcal{N}(0.85, 0.03)$ truncated at [0.75, 0.95]. Note this is suggestive of the prior under-weighting the empirical mean; do not adjust the prior in AQ (a prior change would invalidate every AP table). Flag as future work or acceptable conservatism.

### M33 — Eq. 14 vitamin asymptotic note placement

`sections/03-model.tex` — move the asymptotic-permanence note (currently a few pages later) to a footnote on `Eq. 14` itself, so readers see it in context.

### M19' — Wording polish

- "unbiased median" → "censoring-adjusted median estimate" (in any §3.x or §4.x mentioning Kaplan-Meier).
- "operational asymptote" (for $p_{\mathrm{fuel}}$) → "assumed architecture-dependent cost floor" (in `sections/03-model.tex`, `04-results.tex`, anywhere `p_fuel` is described).

### M21+ — §3 length cuts (continuation of AP M21)

Move from `sections/03-model.tex` to `sections/94-appendix-d-parameter-justification.tex`:

- The full \$74M $C_{\mathrm{labor}}^{(1)}$ build-up paragraph (currently in §3.1).
- The four-configuration $C_{\mathrm{floor}}^{\max}$ table (currently in §4.5 — but Claude flagged it as too long for §3-style explanation; consider relocating or compressing).
- The $K$-subsystem decomposition.

In each main-text location, replace with a 1-sentence summary citing the appendix.

---

## Files modified

**Code:**
- `publications/scripts/isru_model.py` — new functions (`find_crossover_npv_common_deadline`, `find_crossover_npv_with_service_value`, `classify_run_permanence`), updated capex schedule, hybrid re-indexing fix, optional `max_n` arg on `find_recrossing_volume`. **Existing tests must continue to pass.**
- `publications/scripts/isru_mc.py` — service-equivalent variants, extended-bound subset runner, t_0 prior bound update.
- `publications/scripts/tests/test_isru_model.py` — 5 new test classes (`TestCommonDeadline`, `TestShadowServiceValue`, `TestHybridIndexing`, `TestRunPermanenceClassification`, `TestT0BoundConstraint`).
- `publications/scripts/consistency_check.py` — new file (M26).

**Paper sections:**
- `sections/00-frontmatter.tex` — abstract restructure (M27); fnref relocation (M30); language sweep (M34).
- `sections/03-model.tex` — active cost functions (M23); K vs K_eff audit (M22); §3 length cuts (M21+); Eq. 13 symbol (M31); Eq. 14 placement (M33); t_0 bound paragraph (M28); wording (M19').
- `sections/04-results.tex` — new §4.6 "Service-equivalent comparison" (M3); updated §4.4 with extended-bound result (M2-sim); updated headline numbers from MC re-run (M28); language sweep (M34).
- `sections/05-discussion.tex` — corrected hybrid value (M24); link revenue-breakeven to shadow-service-value model (M3 reconciliation); language sweep (M34).
- `sections/06-conclusion.tex` — match new abstract framing (M27); avoid verbatim repetition (Claude minor #11); language sweep (M34).
- `sections/91-appendix-a-supplementary-sensitivity.tex` — Iridium tension note (M32); appendix convergence-curve fix (M26 specific item); language sweep.
- `sections/94-appendix-d-parameter-justification.tex` — receive §3 length cuts (M21+).

**Tables (regenerated from new MC runs):**
- `tables/canonical.tex` — possibly updated baseline numbers (M28 t_0 bound effect).
- `tables/convergence.tex` — re-run.
- `tables/mc_summary.tex` — re-run.
- `tables/savings_survival.tex` — re-run; possibly add extended-horizon row.
- `tables/recrossing.tex` — extended-bound subset section + permanence classification column (M2-sim, M25).
- `tables/hybrid.tex` — re-run with corrected indexing (M24).
- `tables/spearman.tex` — re-run; potentially add p_fuel row (Claude minor #9).
- `tables/params.tex` — t_0 bound update (M28).
- New: `tables/service_equivalent.tex` — common-deadline + shadow-value sensitivity (M3).

**Master:**
- `01-isru-economic-crossover-aq.tex` — copy of `ap.tex` with version letter changed.

## Verification

1. **Unit tests pass**:
   ```
   cd publications/scripts && python3 -m pytest tests/test_isru_model.py -v
   ```
   All previous tests pass (incl. AP's TestLaunchLearning + TestAsymptoticThresholds), 5 new test classes pass.

2. **Canonical MC re-runs successfully** with the new t_0 bound (M28) and new active-cost wiring (M23):
   ```
   python3 -m publications.scripts.isru_mc --canonical --seed 42 --n-runs 10000
   ```
   Convergence rate within 5 pp of the AP value (85.1%); conditional median within 500 units.

3. **Extended-bound subset runs** (M2-sim):
   ```
   python3 -m publications.scripts.isru_mc --extended-recrossing --subset 1500 --max-n 10000000
   ```
   Produces a per-run $N^{**}$ distribution; tail summary statistics populate `tables/recrossing.tex`.

4. **Service-equivalent variants run**:
   ```
   python3 -m publications.scripts.isru_mc --service-equivalent common-deadline
   python3 -m publications.scripts.isru_mc --service-equivalent shadow-value --v-service 1e6
   ```
   Each produces a results bundle that feeds `tables/service_equivalent.tex`.

5. **Numerical consistency check passes**:
   ```
   python3 publications/scripts/consistency_check.py
   ```
   All cited numbers in `sections/*.tex` match regenerated values within tolerance.

6. **Compile**:
   ```
   cd publications/drafts/01-isru-economic-crossover && tectonic --keep-logs --print=false 01-isru-economic-crossover-aq.tex
   ```
   No undefined references. Page count 65 ± 3 (paper restructuring may add or subtract).

7. **Reviewer trajectory** — run all three new models on AQ:
   ```
   node scripts/run-paper-review.js --version=aq
   ```
   **Target outcomes:**
   - **Claude:** Acknowledges the extended-bound $N^{**}$ characterization (resolves issue #1 from AP), the service-equivalent variant (resolves the timing critique), and the hybrid fix. May still flag K-dependence (deferred to AS) and $n_v$ ungrounding (deferred to AS) — those are acceptable. Verdict could plausibly move from Major Revision to **Accept with Minor Revisions**, depending on how the headline numbers shift after the t_0 bound change.
   - **GPT-5.5:** Acknowledges all four primary issues addressed (M3, M2-sim, M24, M28). Major Revision likely persists due to the deferred items (M4 logistic stochastic, M7 K-anchor, M8 vitamin BOM, M9 obsolescence) but the criticism shifts from foundational to incremental. May find new minor issues to flag.
   - **Gemini:** Already at Accept-w-Minor; should continue at the same level or improve.

8. **Regression check**:
   ```
   git diff --stat ap..aq
   ```
   Substantial diff in code (+/− several hundred lines), tables (most regenerated), and the §4 results narrative. Master file structure unchanged; sections/ and tables/ tree unchanged.

## Risk register

- **R1 — t_0 bound change shifts headline numbers materially.** If convergence drops from 85% to 75% or median moves significantly, the paper's narrative needs more rework than just numerical updates. *Mitigation:* run M28 first as a single-day spike before committing to AQ scope; if shifts are too large, consider option (B) (capex distribution) or revisit the bound choice.
- **R2 — Hybrid re-indexing fix shows the hybrid strategy isn't actually value-positive at 20,000 units.** This was a paper headline; a negative result would force revising §5.3 conclusions. *Mitigation:* run M24 second; have a fallback narrative ready ("hybrid value-positive only at scales ≥ N units" with N from the corrected calc).
- **R3 — Extended-bound subset reveals more right-censoring than expected.** If even at $N = 10^7$ many runs are still censored, the M2-sim concern isn't fully resolved. *Mitigation:* compute the analytic discounted-tail bound (M25) for those runs to classify them as discounted-permanent without empirical observation.
- **R4 — Service-equivalent variant collapses the ISRU advantage.** Possible — if common-deadline shifts the crossover dramatically, the paper's central claim weakens. *Mitigation:* present both cost-only and service-equivalent as bookends; emphasize the cost-only as the lower bound on Earth's preferred regime.
- **R5 — Compute budget overrun.** The full canonical re-run + extended subset + two service-equivalent variants is ~3× the AP simulation budget. *Mitigation:* parallelizable; and the canonical 10k-run MC already takes < 30 minutes on a laptop.

## Order of execution (suggested)

1. **Day 1 morning:** M28 (t_0 bound) implementation + canonical MC re-run. Validate that headline numbers are still in family. **Decision point** before continuing.
2. **Day 1 afternoon:** M24 (hybrid re-indexing) + hybrid table regeneration.
3. **Day 2:** M22 + M23 (notation cleanup, active cost functions). Mostly paper editing.
4. **Day 3:** M3 (service-equivalent variants) — both common-deadline and shadow-value functions implemented and tested; new MC variants run.
5. **Day 4:** M2-sim (extended-bound subset) + M25 (analytic tail bound). Pairs naturally.
6. **Day 5:** M27 (abstract restructure) + M26 (consistency check) + opportunistic cleanups (M30, M31, M32, M33, M19', M34, M21+).
7. **Day 6:** Compile, verify, run reviewer trajectory, commit.
8. **Day 7 (buffer):** Any items from the risk register that materialized.
