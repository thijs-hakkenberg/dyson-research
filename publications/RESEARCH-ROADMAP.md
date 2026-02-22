# Research Roadmap: Papers, Studies, and Gap Analysis

**Generated:** 2026-02-22
**Based on:** Feasibility assessment, 142 research questions (107 open), 12 TRL assessments, 5 decision gates

---

## Executive Summary

The Phase 0 feasibility assessment identifies **2 project-ending risks**, **3 architecture-change risks**, and **107 open research questions** across 5 phases. Of these, **29 questions are immediately addressable through publication/analysis**, while 35 require physical experimentation. This document maps open questions to potential papers and identifies research priorities that would strengthen the feasibility assessment for a technical audience.

---

## Paper Portfolio

### Tier 1: In Progress

| # | Paper | Status | Est. Completion |
|---|-------|--------|-----------------|
| 01 | ISRU Economic Crossover | 3/3 Accept (AM) | Complete |
| 02 | Swarm Coordination Scaling | Outline + simulator exists | 8–12 weeks |
| 03 | Multi-Model AI Consensus | Outline + 16 deliberations exist | 7–10 weeks |

### Tier 2: High Priority — Directly Addresses Feasibility Risks

These papers would significantly strengthen the feasibility assessment by providing quantitative backing for the highest-risk technology areas.

#### Paper 04: Microgravity Metallurgy — State of the Art and Path to Industrial Scale

**Addresses:** Project-ending risk #1 (TRL 2–3, gap of 4–5 levels)
**Related RQs:** rq-0-11 (microgravity metallurgy), rq-0-12 (zone refining in zero-g), rq-0-15 (silicon purity)
**Decision Gate:** Gate 1 (Microgravity Materials Processing, month 36)

**Content:**
- Comprehensive literature review of all ISS metallurgy experiments (ESA Columbus lab, JAXA Kibo, NASA MSFC)
- Analysis of grain structure formation physics in microgravity (Marangoni convection, buoyancy absence)
- Scaling laws: what changes between 100g ISS samples and tonne-per-month industrial production
- Thermal management challenges unique to microgravity (no natural convection)
- Artificial gravity fallback: cost and mass implications of rotational station design
- Quantitative technology maturation timeline with go/no-go decision criteria

**Type:** Literature review + parametric analysis
**Effort:** 4–6 weeks
**Impact:** Directly informs the most consequential technology risk in the entire program

#### Paper 05: ISRU Water Extraction — Asteroid vs. Lunar Sources

**Addresses:** Project-ending risk #2 (TRL 3–4), architecture-change risk (source selection)
**Related RQs:** rq-0-6 (regolith excavation), rq-0-27 (water-first strategy), rq-0-39 (subsurface characterization), rq-1-50 (lunar regolith processing), rq-2-32 (comparative feedstock economics)
**Decision Gate:** Gate 3 (ISRU Water Extraction, month 48)

**Content:**
- Comparative analysis: C-type asteroid water vs. lunar polar ice vs. Phobos/Deimos
- Energy budget per kg H2O for each source (thermal extraction, electrolysis, purification)
- Transport cost model: source location → L4/L5 processing station
- Scaling analysis: extraction rate requirements for propellant self-sufficiency
- Monte Carlo over extraction yield uncertainty, transport delta-v, and energy costs
- Optimal source selection as function of program scale

**Type:** Parametric cost model + Monte Carlo (similar methodology to Paper 01)
**Effort:** 6–8 weeks
**Impact:** Resolves the second project-ending risk and informs propellant architecture

#### Paper 06: Cryogenic Propellant Architecture Trade Study

**Addresses:** Architecture-change risk (cryocooler scaling, TRL 4–5)
**Related RQs:** rq-0-30 (cryogenic boiloff), rq-0-49 (cryocooler scaling), rq-0-40 (thermal management volatiles), rq-0-16 (thruster lifetime)
**Decision Gate:** Gate 2 (Cryogenic Propellant Architecture, month 30) — nearest gate

**Content:**
- LH2/LOX vs. storable propellant comparison (Isp, mass ratio, handling complexity, ISRU chemistry)
- Cryocooler technology assessment: current state (milliwatt-class flight) → required (100–500W at 20K)
- Zero-boiloff depot sizing: thermal model, MLI performance, cryocooler power demand
- Fleet sizing implications: how 30% Isp reduction (storable) cascades through fleet size and transit time
- Decision framework: at what cryocooler TRL does the LH2 architecture close?
- Sensitivity analysis: which parameters have highest decision value?

**Type:** Systems trade study with parametric model
**Effort:** 5–7 weeks
**Impact:** Directly informs the nearest decision gate (month 30)

### Tier 3: Medium Priority — Strengthens Assessment for Technical Audience

#### Paper 07: Billion-Unit Collision Avoidance — Certification Pathways

**Addresses:** rq-2-3 (collision avoidance certification), rq-1-6 (collision probability), rq-2-30 (collisional cascade timescales)
**Feasibility gap:** No existing certification framework for autonomous collision avoidance at >100,000 objects

**Content:**
- Current space traffic management: USSPACECOM catalog, conjunction assessment, maneuver protocols
- Scaling analysis: O(N²) pairwise → spatial partitioning → mean-field approximation
- Cascade dynamics: Kessler syndrome thresholds for different orbital regimes
- Certification framework proposal: what "safe enough" means at 10^6 objects
- Comparison with terrestrial analogues: air traffic control, maritime AIS

**Type:** Analysis + simulation
**Effort:** 6–8 weeks

#### Paper 08: Space Solar Power Economics at Dyson Scale

**Addresses:** rq-2-20 (swarm ROI threshold), rq-1-44 (minimum PV production rate), rq-2-23 (GW-scale transmission efficiency)
**Feasibility gap:** Revenue breakeven analysis in Paper 01 was limited to single parameter

**Content:**
- Full economic model for SSP revenue generation from Dyson swarm elements
- Transmission efficiency: microwave vs. laser, atmospheric losses, rectenna requirements
- Market analysis: terrestrial energy demand projections, price competition with ground renewables
- Break-even analysis: minimum swarm size for commercial viability at various energy prices
- Deployment rate optimization: revenue-maximizing production schedule vs. cost-minimizing schedule

**Type:** Economic model + Monte Carlo
**Effort:** 6–8 weeks

#### Paper 09: Multi-Century Governance for Volunteer-Driven Space Projects

**Addresses:** rq-0-29 (governance structures), rq-1-40 (slot reallocation), rq-2-8 (repair authority)
**Feasibility gap:** Governance is the least technically grounded area in the assessment

**Content:**
- Historical analysis of multi-century projects (cathedral building, irrigation systems, intergenerational trusts)
- Organizational theory: how structures evolve over centuries (succession, schism, reform)
- Constitutional design for space infrastructure governance
- Decision-making protocols for irreversible actions (orbital modifications, end-of-life)
- Comparison with existing space governance (UN COPUOS, ITU, IADC)

**Type:** Policy/governance analysis
**Effort:** 4–6 weeks (different from engineering papers — literature-heavy, less simulation)

#### Paper 10: In-Space Thin-Film Deposition — Technology Assessment

**Addresses:** rq-1-46 (thin-film deposition crossover), rq-1-45 (UMG silicon viability), rq-0-44 (semiconductor fabrication), rq-2-14 (silicon purity), rq-2-15 (material selection)
**Feasibility gap:** Solar cell self-fabrication is assumed but not rigorously assessed

**Content:**
- Current terrestrial thin-film PV manufacturing: CdTe, CIGS, perovskite process flows
- Adaptation to vacuum/microgravity: which steps benefit, which are harder
- Material availability: which PV chemistries are feasible from asteroid/lunar feedstock
- Quality achievable from UMG silicon (6N? 4N? What efficiency trade-off?)
- Economic crossover: at what production scale does in-space deposition beat Earth-launched panels?
- Roadmap: ground demo → ISS demo → pilot production → full scale

**Type:** Technology assessment + parametric crossover model
**Effort:** 6–8 weeks

### Tier 4: Supporting Research — Fills Knowledge Gaps

#### Paper 11: Autonomous Assembly Reliability at Scale

**Addresses:** rq-1-16 (autonomy certification), rq-1-22 (assembly reliability 95%+)
- Reliability model for autonomous robotic assembly in space
- What failure rates are acceptable at 10^6 assembly operations?
- Comparison with terrestrial autonomous manufacturing (Tesla, FANUC)

#### Paper 12: Thermal Management Inside 1 AU

**Addresses:** rq-1-13 (thermal at 0.5 AU), rq-2-16 (radiator durability), rq-2-9 (drone thermal)
- Solar flux scaling: 1 AU (1,361 W/m²) → 0.5 AU (5,444 W/m²) → 0.3 AU (15,122 W/m²)
- Passive vs. active thermal management trade-offs at each orbit
- Radiator sizing and durability over 30-year mission life

#### Paper 13: Swarm Programming Languages and Communication Bandwidth

**Addresses:** rq-2-21 (programming language scalability), rq-2-22 (minimum bandwidth)
- What programming paradigm for 10^6+ autonomous agents?
- Bandwidth requirements: continuous telemetry vs. exception-based
- Edge computing vs. hierarchical aggregation

---

## Gap Analysis: Open Questions by Addressability

### Publication-Addressable (29 questions)
These can be investigated through modeling, simulation, literature review, or analysis — no new hardware needed.

**Phase 0:** rq-0-29 (governance)
**Phase 1:** rq-1-11 (power architecture), rq-1-16 (autonomy cert), rq-1-21 (feedstock timeline), rq-1-40 (slot governance), rq-1-44 (min PV rate), rq-1-45 (UMG silicon), rq-1-46 (thin-film deposition), rq-1-50 (lunar regolith)
**Phase 2:** rq-2-3 (collision avoidance), rq-2-8 (repair authority), rq-2-20 (swarm ROI), rq-2-21 (programming languages), rq-2-22 (bandwidth), rq-2-23 (GW transmission), rq-2-30 (cascade timescales), rq-2-31 (planetary perturbations), rq-2-32 (feedstock economics)
**Phase 3:** rq-3a-3 (consensus protocols), rq-3b-3 (He isotope economics), rq-3b-4 (orbit stability)

### Experimentation-Required (35 questions)
These need physical experiments (ISS, parabolic flights, ground labs, CubeSats).

**Highest priority** (project-ending or architecture-change):
- rq-0-11: Microgravity metallurgy scaling → ISS Materials Science Lab
- rq-0-15: Silicon purity in vacuum → ISS or dedicated free-flyer
- rq-0-6: Regolith excavation in microgravity → parabolic flights
- rq-0-7: Anchoring reliability → parabolic flights + ground testing
- rq-1-1: PV degradation at 0.3–0.5 AU → CubeSat or Parker Solar Probe data
- rq-1-4: High-voltage arc fault in plasma → ground plasma lab
- rq-2-1: Multi-kilovolt arc management → ground plasma lab (extension of rq-1-4)

### Engineering-Decision (43 questions)
These require trade studies, vendor engagement, or architectural choices that depend on earlier answers. Most cannot be resolved until gate criteria are met.

---

## Coverage Matrix: Feasibility Risks vs. Papers

| Feasibility Risk | Risk Level | Current Coverage | Proposed Paper |
|-----------------|-----------|-----------------|----------------|
| Microgravity metallurgy (TRL 2–3) | Project-ending | rq-0-11 open | **Paper 04** |
| ISRU water extraction (TRL 3–4) | Project-ending | rq-0-27 answered (strategy only) | **Paper 05** |
| Cryocooler scaling (TRL 4–5) | Architecture-change | rq-0-49 open | **Paper 06** |
| Silicon purity in vacuum (TRL 2–3) | Architecture-change | rq-0-15 open | **Paper 10** (partial) |
| Autonomous prospecting (TRL 5–6) | Schedule-delay | rq-0-5 answered | Covered |
| SEP at 100+ kW (TRL 6–7) | Schedule-delay | Mature heritage | Not needed |
| Sunshield heritage (TRL 6–7) | Cost-increase | JWST success | Not needed |
| ISRU economic crossover | N/A | **Paper 01** (complete) | Complete |
| Swarm coordination scaling | N/A | **Paper 02** (in progress) | In progress |
| Multi-model methodology | N/A | **Paper 03** (in progress) | In progress |

**Coverage after proposed papers:** 5/5 high-risk technologies have dedicated analytical/literature backing.

---

## Recommended Priority Order

1. **Paper 02** (Swarm Coordination) — existing simulator, immediate readiness
2. **Paper 03** (AI Consensus) — existing data, analysis-only
3. **Paper 06** (Cryogenic Architecture) — nearest decision gate (month 30)
4. **Paper 04** (Microgravity Metallurgy) — highest-consequence risk
5. **Paper 05** (Water Extraction) — second project-ending risk
6. **Paper 07** (Collision Avoidance) — strengthens long-term credibility
7. **Paper 08** (SSP Economics) — revenue model for the program
8. **Paper 10** (Thin-Film Deposition) — PV self-fabrication viability
9. **Paper 09** (Governance) — different audience, lower technical urgency
10. **Papers 11–13** — as capacity allows

---

## Timeline (Approximate)

```
2026 Q1:  Paper 01 ✓ (complete)
          Paper 02 development begins
          Paper 03 development begins (parallel)

2026 Q2:  Paper 02 in review cycle
          Paper 03 in review cycle
          Paper 06 development begins (parallel)

2026 Q3:  Paper 02 targeting 3/3 Accept
          Paper 03 targeting 3/3 Accept
          Paper 04 development begins
          Paper 06 in review cycle

2026 Q4:  Paper 04 in review cycle
          Paper 05 development begins
          Paper 07 development begins (parallel)

2027 Q1:  Papers 08–10 development
          Earlier papers submitted to venues
```

---

## Impact on Feasibility Assessment

If all Tier 1–2 papers (01–06) are completed:
- **Project-ending risks:** Both have dedicated analytical papers providing technology maturation timelines and fallback analysis
- **Architecture-change risks:** Cryogenic decision has a dedicated trade study; silicon purity is partially covered
- **Decision gates:** Gate 2 (month 30) has direct paper backing; Gates 1, 3 have literature foundations
- **Open question coverage:** ~40% of publication-addressable questions are covered by papers
- **Technical credibility:** The assessment moves from "identified risks" to "quantified risks with documented mitigation paths"
