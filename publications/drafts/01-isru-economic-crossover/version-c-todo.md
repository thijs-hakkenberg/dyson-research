# Version C — Peer Review Response TODO

## Status Overview

| Step | Description | Status |
|------|-------------|--------|
| 1 | Python model changes | Done |
| 2 | Regenerate figures | Done |
| 3 | Write LaTeX Version C | Not started |
| 4 | Humanize intro/discussion | Not started |

---

## Step 1: Python Model Changes (Done)

File: `publications/scripts/generate-isru-figures.py`

- [x] **1a.** New baseline parameters: `C_floor=0.5M`, `r=0.05`, `b_L=None`, `p_fuel=200`, `p_ops_launch=800`
- [x] **1b.** ISRU cost floor in `isru_unit_cost()` and new `isru_ops_cost()`: `C_floor + (C_ops1 - C_floor) * n^b_I / S`
- [x] **1c.** NPV crossover function `find_crossover_npv()` with time-mapped discounting
- [x] **1d.** Launch learning function `earth_unit_cost_launch_learning()` (two-component: fuel fixed + ops learns)
- [x] **1e.** Monte Carlo overhaul: 10k runs, stochastic `C_ops1 ~ U[2M,10M]`, `C_mfg1 ~ U[50M,100M]`, `r ~ U[0,0.10]`, Gaussian copula for `p_launch`/`K` (rho=0.3), bootstrap CIs (5k resamples), Spearman correlations
- [x] **1f.** Updated tornado: 7 parameters (added `r`, `C_ops1`, `C_mfg1`), NPV-based with `r=0.05` baseline
- [x] **1g.** New figure `fig_npv_comparison()`: dual-panel (cumulative curves at 4 rates + crossover vs r)
- [x] **1h.** Launch learning scenario printed: LR=0.97 → N*=7,360 (+468 from NPV baseline)
- [x] **1i.** Production schedule table printer for LaTeX reference

## Step 2: Figure Generation (Done)

All 6 PDFs in `publications/drafts/figures/`:

| Figure | File | Key result |
|--------|------|------------|
| 1 | `fig-cumulative-cost.pdf` | Crossover ~3,557 units (undiscounted) |
| 2 | `fig-unit-cost.pdf` | Launch floor $1.85M/unit |
| 3 | `fig-tornado.pdf` | NPV baseline=6,892, r=5%; 7 parameters |
| 4 | `fig-heatmap.pdf` | NPV-based contours |
| 5 | `fig-histogram.pdf` | 10k runs, median ~12k (unconditional) |
| 6 | `fig-npv-comparison.pdf` | Curves at r=0/3/5/10% + crossover(r) |

### Key Numbers for LaTeX

**Crossover points:**
| Scenario | N* (units) |
|----------|-----------|
| Undiscounted baseline | ~3,557 |
| NPV r=0% | ~3,557 |
| NPV r=3% | ~5,047 |
| NPV r=5% (baseline) | ~6,892 |
| NPV r=10% | >20,000 |
| Optimistic (NPV) | ~3,278 |
| Conservative (NPV) | >20,000 |
| Launch learning LR=0.97 (NPV) | ~7,360 (+468) |

**Monte Carlo (10,000 runs, NPV):**
- Convergence: 63.5% within 40k-unit horizon; 36.5% non-converging
- Conditional (converging only): median ~6,400, IQR [3,800, 10,900], P10 ~2,500, P90 ~17,000
- Unconditional: median ~12,000

**Bootstrap 95% CIs:**
- Median: [11,486–12,318] (unconditional)
- P10: [2,902–3,074]

**Spearman rank correlations (param → N*):**
| Param | rho | Significance |
|-------|-----|-------------|
| r (discount rate) | +0.539 | *** |
| LR_E (Earth learning) | -0.519 | *** |
| K (ISRU capital) | +0.459 | *** |
| C_mfg1 (Earth mfg cost) | -0.274 | *** |
| C_ops1 (ISRU ops cost) | +0.098 | *** |
| t0 (ramp-up time) | +0.083 | *** |
| p_launch (launch cost) | +0.077 | *** |
| LR_I (ISRU learning) | +0.073 | *** |

**Production schedule (k=2.0, t0=5, prod_rate=500):**
| n | t(n) yr | S(t) | 1/S penalty |
|---|---------|------|-------------|
| 1 | 5.0 | 0.50 | 2.00 |
| 10 | 5.0 | 0.51 | 1.96 |
| 100 | 5.2 | 0.60 | 1.67 |
| 500 | 6.0 | 0.88 | 1.14 |
| 1,000 | 7.0 | 0.98 | 1.02 |
| 5,000 | 15.0 | 1.00 | 1.00 |
| 10,000 | 25.0 | 1.00 | 1.00 |

---

## Step 3: Write LaTeX Version C (TODO)

Source: `01-isru-economic-crossover-a.tex` → `01-isru-economic-crossover-c.tex`

### 3a. Equation changes (Section 3)
- [ ] Add NPV variant of Earth cumulative (new equation)
- [ ] Add NPV variant of ISRU cumulative (new equation)
- [ ] Modify Eq 7 (ISRU ops) to include cost floor
- [ ] Relabel Eq 6 as "illustrative average cost" with N_total caveat (P4)
- [ ] Add production schedule equation: t_n = t0 + n/n_dot_max
- [ ] Annotate S-curve: state k=2.0 explicitly
- [ ] Add launch learning equation in sensitivity section

### 3b. Table 1 expansion
- [ ] Add rows: k=2.0 (fixed), C_ops1 ~ U[2M,10M], C_mfg1 ~ U[50M,100M], C_floor=0.5M (fixed), r ~ U[0,0.10], prod_rate=500 (fixed)

### 3c. New subsection §3.4 Parameter Justification (P3)
- [ ] C_mfg1=$75M: spacecraft production data (Starlink comparison)
- [ ] C_ops1=$5M: regolith processing energy, equipment wear, consumables
- [ ] K=$50B: NASA COMPASS reference, industrial facility analogy
- [ ] k=2.0: justify steepness; S(t0)=0.5, S(t0+2)>0.88

### 3d. Results section updates
- [ ] §4.1: Present undiscounted first (r=0, ~3,557), then NPV at r=5% (~6,892)
- [ ] §4.2: Updated tornado (7 params), launch learning paragraph (+468 units)
- [ ] §4.3: 10k runs, convergence rate (63.5%), conditional stats, bootstrap CIs, Spearman table
- [ ] §4.4: Recalculate cumulative economics table from Python model
- [ ] New Figure 6: NPV comparison reference
- [ ] New Table: Spearman rank correlations

### 3e. Production schedule table (P2)
- [ ] Table or appendix: n → t(n) → S(t) → 1/S at milestones
- [ ] Document S_min = 0.05 floor

### 3f. Discussion updates
- [ ] Remove "we defer NPV to future work" — now addressed
- [ ] Update "10,000 unit rule" to NPV-adjusted threshold
- [ ] Keep throughput constraint (praised)
- [ ] Strengthen limitations with remaining genuine future work

### 3g. Bibliography expansion (P6)
Must-add (~12 new, target ~27 total):
- [ ] Kornuta et al. 2019 (lunar propellant architecture)
- [ ] Metzger et al. 2013 (bootstrapping lunar industry)
- [ ] Sowers 2021 (lunar ice business case)
- [ ] NASA Cost Estimating Handbook
- [ ] Ishimatsu et al. 2016 (space logistics)
- [ ] Dutton & Thomas 1984 (progress functions)
- [ ] Argote & Epple 1990 (learning curves in manufacturing)
- [ ] Nagy et al. 2013 (statistical basis for tech progress)

Fixes:
- [ ] O'Neill date: 1974 vs 1977 mismatch
- [ ] Cite Crawford 2015 and Cilliers 2023 in text (currently orphaned)
- [ ] Replace/supplement SpaceX Users Guide with peer-reviewed source

### 3h. AI disclosure expansion
- [ ] Specify which AI tools used
- [ ] Note MC code was human-written and validated
- [ ] All quantitative claims independently verified

### 3i. Abstract update
- [ ] Reflect NPV analysis, 10k MC runs, stochastic C_ops1/C_mfg1
- [ ] Revised crossover numbers (undiscounted ~3,600; NPV r=5% ~6,900)

---

## Step 4: Humanize Intro & Discussion (TODO)

- [ ] Introduction (Section 1, ~14 paragraphs): engaging without colloquialisms
- [ ] Discussion (Section 5, ~4 subsections): policy implications more readable
- [ ] Do NOT humanize: Abstract, Related Work, Model Description, Results, Conclusion
- [ ] Avoid Version B phrases: "kicking around", "nailed this down", "deep in the red", "PowerPoint decks", "waiting until you are thirsty to dig the well"
- [ ] Target: Version A formal register + selectively accessible phrasing

---

## Verification Checklist

- [x] Python script runs without errors → 6 PDFs
- [ ] LaTeX compiles: `pdflatex 01-isru-economic-crossover-c.tex` → no missing refs (no pdflatex installed; braces/citations/refs validated programmatically)
- [x] P1: NPV equations (Eq crossover_npv) + figure (fig-npv-comparison) + MC uses find_crossover_npv
- [x] P2: k=2.0 defined in text + Table 1, t(n) mapping explicit (Eq production_schedule), production schedule table (Tab production_schedule)
- [x] P3: Parameter justification subsection (§3.4), C_ops1 ~ U[2M,10M], C_mfg1 ~ U[50M,100M], cost floor C_floor=0.5M
- [x] P4: Eq 6 relabeled as "illustrative average cost", N_total=10,000 defined with caveat
- [x] P5: Launch learning scenario in §4.2 (Eq launch_learning, +468 units / 7% shift)
- [x] P6: 23 references (up from 15), O'Neill fixed (oneill1974), Crawford/Cilliers cited in Related Work
- [x] P7: 10k runs, bootstrap CIs (5k resamples), Spearman table (Tab spearman), Gaussian copula (rho=0.3)
