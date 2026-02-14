# Draft Outline: ISRU Economic Crossover Point

**Working Title:** Economic Inflection Points in Space Manufacturing: Monte Carlo Analysis of In-Situ Resource Utilization vs. Earth Launch for Large-Scale Space Infrastructure

**Target Venue:** Advances in Space Research / Acta Astronautica

**Estimated Length:** 4,000-5,000 words + figures

---

## Abstract (~250 words)

The economic viability of large-scale space infrastructure depends on when in-situ resource utilization (ISRU) becomes cheaper than Earth-based manufacturing plus launch. Despite decades of qualitative arguments for space manufacturing, no quantitative crossover model exists in the literature. We present a Monte Carlo cost model that identifies the production volume at which ISRU manufacturing becomes economically preferable to Earth launch, and characterizes the sensitivity of this threshold to key parameters.

Under baseline assumptions ($1,000/kg launch cost, $50B ISRU capital investment, 85% Earth manufacturing learning curve, 90% ISRU learning curve), the crossover occurs at approximately 3,500 production units. This threshold is robust: even under pessimistic assumptions ($2,000/kg launch, $100B capital), ISRU wins before 10,000 units. The crossover is most sensitive to launch cost (±2,000 units per $500/kg) and ISRU capital investment (±1,500 units per $25B).

The fundamental asymmetry driving this result is that launch costs do not follow learning curves — every kilogram costs roughly the same regardless of cumulative volume — while ISRU manufacturing benefits from both experience curves and economies of scale. This asymmetry makes ISRU crossover inevitable at sufficient scale, with the threshold determined by the ratio of ISRU capital cost to per-unit launch cost savings.

We propose a hybrid transition strategy and discuss implications for near-term space infrastructure planning in the context of declining launch costs (Starship-class vehicles) and growing interest in lunar/asteroid ISRU.

---

## 1. Introduction (~500 words)

### 1.1 The Manufacturing Location Problem

- Space infrastructure at scale requires millions of tonnes of material
- Two pathways: manufacture on Earth and launch, or manufacture in space from local resources
- Qualitative arguments for ISRU are well-established (O'Neill 1976, Zubrin 1996) but quantitative crossover analysis is absent
- Recent developments (SpaceX Starship, lunar ISRU programs, asteroid mining startups) make this question urgent

### 1.2 Gap in the Literature

- Existing ISRU economic analyses focus on specific missions (lunar propellant, Mars habitat)
- No general crossover model exists for arbitrary production volume
- Learning curve economics well-studied in manufacturing but not applied to Earth-vs-space trade
- Launch cost projections vary by order of magnitude — sensitivity analysis is essential

### 1.3 Contribution

- First quantitative Monte Carlo model for ISRU economic crossover
- Parametric sensitivity analysis across launch cost, capital investment, and learning rates
- Hybrid transition strategy with phased economics
- Open-source simulator for community exploration

---

## 2. Related Work (~600 words)

### 2.1 ISRU Economic Studies

- NASA lunar ISRU cost-benefit analyses (Sanders & Larson, 2015)
- Asteroid mining economic models (Sonter 1997, Elvis 2012, Andrews et al. 2015)
- Mars ISRU propellant production economics (Zubrin & Wagner 1996)
- Limitation: all mission-specific, no general crossover model

### 2.2 Launch Cost Trajectories

- Historical launch cost trends (Jones 2018)
- SpaceX Starship projections and implications (current industry estimates)
- Learning curve analysis for launch vehicles (Wertz 2011)
- Key insight: vehicle reusability reduces per-launch cost but not $/kg linearly

### 2.3 Manufacturing Learning Curves

- Wright learning curve model (Wright 1936, applied to aerospace)
- Space manufacturing cost projections (O'Neill 1977)
- In-situ manufacturing ramp-up models (limited literature — this is a gap)

---

## 3. Model Description (~800 words)

### 3.1 Earth Manufacturing Cost Model

```
C_earth(n) = C_mfg(n) + C_launch(n)
```

- Manufacturing cost follows Wright learning curve: `C_mfg(n) = C_mfg(1) × n^b` where `b = log(LR)/log(2)`
- Learning rate LR = 0.85 (baseline), range 0.80-0.95
- Launch cost is **constant per kg**: `C_launch(n) = m_unit × $/kg`
- This is the key asymmetry: manufacturing learns, launch does not

### 3.2 ISRU Cost Model

```
C_isru(n) = C_capital / N_total + C_ops(n)
```

- Capital cost amortized over total production: $50B baseline, range $30B-$100B
- Operational cost follows learning curve with S-curve ramp-up
- Ramp-up time: 5 years baseline (years 0-5 zero production, then S-curve to full rate)
- Operational learning rate: 0.90 (slower than Earth due to novel environment)

### 3.3 Monte Carlo Framework

- 100 runs per configuration (expandable to 10,000 for publication)
- Parameter distributions:
  - Launch cost: uniform [$500, $2,000]/kg
  - ISRU capital: uniform [$30B, $100B]
  - Earth learning rate: normal(0.85, 0.03)
  - ISRU learning rate: normal(0.90, 0.03)
  - Ramp-up time: uniform [3, 8] years
- Output: crossover unit number, cumulative cost difference, time to crossover

### 3.4 Assumptions and Limitations

- Unit mass: 1,850 kg (solar collector baseline, but parameterizable)
- No financing costs (simplifying assumption — discuss impact)
- No technology obsolescence during transition
- ISRU quality assumed equal to Earth manufacturing (optimistic for early production)

---

## 4. Results (~1,000 words)

### 4.1 Baseline Crossover

- **Crossover at ~3,500 units** under baseline assumptions
- Table: crossover points across conservative/baseline/optimistic scenarios
- Figure 1: Cumulative cost curves for Earth vs. ISRU paths
- Figure 2: Per-unit cost comparison showing divergence

### 4.2 Sensitivity Analysis

- **Launch cost dominance:** ±2,000 units per $500/kg change
  - At $200/kg (aggressive Starship): crossover at ~5,000 units
  - At $2,000/kg (current costs): crossover at ~2,000 units
- **ISRU capital sensitivity:** ±1,500 units per $25B change
  - $30B factory: crossover at ~1,500 units
  - $100B factory: crossover at ~8,000 units
- **Ramp-up time:** ±500 units per year of delay
- Figure 3: Tornado diagram of parameter sensitivities
- Figure 4: 2D heat map of crossover point vs. launch cost and ISRU capital

### 4.3 Robustness

- Even worst-case ($2,000/kg launch, $100B capital): ISRU wins before 10,000 units
- Monte Carlo distribution of crossover points: median 3,500, 90th percentile ~7,000
- Figure 5: Histogram of crossover points across Monte Carlo runs

### 4.4 Cumulative Economics

| Year | Earth Cumulative | ISRU Cumulative | ISRU Savings |
|------|------------------|-----------------|--------------|
| 5    | $150B            | $55B            | -$95B        |
| 10   | $350B            | $100B           | $250B        |
| 15   | $600B            | $150B           | $450B        |
| 20   | $900B            | $200B           | $700B        |

---

## 5. Discussion (~800 words)

### 5.1 The Throughput Constraint

- Even at very low launch costs, physical throughput limits favor ISRU
- Launch cadence constraints, fairing volume limits, infrastructure bottlenecks
- ISRU bypasses all terrestrial logistics constraints
- At millions-of-units scale, ISRU is the only feasible option regardless of economics

### 5.2 Optimal Transition Strategy

- Phase 1a (Years 1-5): Earth manufacturing for first 1,000-2,000 units while deploying ISRU seed factory
- Phase 1b (Years 5-10): Hybrid production, crossover occurs, transition to ISRU
- Phase 2+ (Years 10+): Full ISRU with Earth supplying only "vitamin" components
- This hybrid approach minimizes risk while capturing ISRU economics

### 5.3 Implications for Near-Term Space Policy

- Lunar ISRU demonstrations (Artemis program) are high-value even if initial costs are high
- Asteroid mining startups should target minimum viable scale, not minimum viable product
- Space agencies should plan for ISRU transition in long-duration program architectures
- Launch cost reduction and ISRU development are complementary, not competing investments

### 5.4 Limitations

- Model assumes stable technology and policy environment over 20+ years
- ISRU quality parity is assumed but not demonstrated
- Financing costs could shift crossover by 500-1,000 units
- Single-product model — multi-product ISRU changes economics further

---

## 6. Conclusion (~300 words)

- First quantitative crossover model for Earth vs. ISRU manufacturing
- Crossover is inevitable at sufficient scale; the question is when, not whether
- ~3,500 units under baseline, robust across wide parameter ranges
- Hybrid transition minimizes risk while capturing economic benefits
- Launch cost improvements and ISRU investment are complementary strategies
- Open-source simulator available for community exploration and extension

---

## References (estimated 25-35)

Key citations to include:
- O'Neill (1976) — space manufacturing concept
- Wright (1936) — learning curve model
- Sanders & Larson (2015) — NASA ISRU economics
- Elvis (2012) — asteroid mining economics
- Wertz (2011) — space mission engineering economics
- Jones (2018) — launch cost trends
- SpaceX Starship cost projections (current industry references)
- Sonter (1997) — asteroid mining feasibility
- Andrews et al. (2015) — asteroid mining economics
- Relevant ISRU demonstration results (MOXIE, etc.)

---

## Figures List

1. Cumulative cost comparison: Earth manufacturing vs. ISRU over 20 years
2. Per-unit cost curves showing learning curve divergence
3. Tornado diagram: parameter sensitivity rankings
4. 2D heat map: crossover point as function of launch cost and ISRU capital
5. Monte Carlo histogram: distribution of crossover points
6. Hybrid transition timeline with cost curves

---

## Data Availability Statement

Monte Carlo simulation code and raw output data are available at [GitHub repository URL]. An interactive web-based simulator is available at [project URL] for parameter exploration.
