# Publication Plan — Project Dyson Research Papers

**Last updated:** 2026-02-23
**Papers planned:** 10 (1 complete, 9 in pipeline)
**Open research questions:** 107 of 142 (75%)
**Publication-addressable:** 29 questions across 10 papers

---

## Status Overview

| # | Paper | Tier | Status | Blocking |
|---|-------|------|--------|----------|
| 01 | ISRU Economic Crossover | 1 | **COMPLETE** (3/3 Accept, Version AM) | — |
| 02 | Swarm Coordination Scaling | 1 | **Version F** — 1 Minor + 1 Major + 1 Unknown | Link model, optimization eval |
| 03 | Multi-Model AI Consensus | 1 | **Version G** — 2 Major + 1 Unknown | Blind deliberation experiment |
| 04 | Microgravity Metallurgy | 2 | Inputs cataloged | — |
| 05 | ISRU Water Extraction | 2 | Inputs cataloged | — |
| 06 | Cryogenic Propellant Architecture | 2 | Inputs cataloged | — |
| 07 | Collision Avoidance Certification | 3 | Inputs cataloged | Paper 02 (shared sim) |
| 08 | Space Solar Power Economics | 3 | Inputs cataloged | — |
| 09 | Multi-Century Governance | 3 | Inputs cataloged | — |
| 10 | In-Space Thin-Film Deposition | 3 | Inputs cataloged | Paper 04 (silicon overlap) |

---

## Parallelization Strategy

```
            Q1 2026              Q2 2026              Q3 2026              Q4 2026
           ┌──────────┐         ┌──────────┐         ┌──────────┐         ┌──────────┐
Track A:   │ Paper 02  │─────── │ 02 review │─────── │ 02 accept│         │          │
           │ sim port  │        │ cycle     │        │          │         │          │
           └──────────┘         └──────────┘         └──────────┘         └──────────┘
           ┌──────────┐         ┌──────────┐         ┌──────────┐         ┌──────────┐
Track B:   │ Paper 03  │─────── │ 03 review │─────── │ 03 accept│         │          │
           │ analysis  │        │ cycle     │        │          │         │          │
           └──────────┘         └──────────┘         └──────────┘         └──────────┘
                                ┌──────────┐         ┌──────────┐         ┌──────────┐
Track C:                        │ Paper 06  │─────── │ 06 review │─────── │ 06 accept│
                                │ trade stdy│        │ cycle     │        │          │
                                └──────────┘         └──────────┘         └──────────┘
                                ┌──────────┐         ┌──────────┐         ┌──────────┐
Track D:                        │ Paper 04  │─────── │ 04 review │─────── │ 04 accept│
                                │ lit review│        │ cycle     │        │          │
                                └──────────┘         └──────────┘         └──────────┘
                                            ┌──────────┐         ┌──────────┐
Track E:                                    │ Paper 05  │─────── │ 05 review│──── ...
                                            │ MC model  │        │ cycle    │
                                            └──────────┘         └──────────┘
                                                      ┌──────────┐         ┌──────────┐
Track F:                                              │ 07,08,09  │─────── │ review   │
                                                      │ 10 start  │        │ cycles   │
                                                      └──────────┘         └──────────┘
```

**Max parallel tracks:** 4 (limited by AI review bandwidth — each review cycle needs 3 model API calls per version)

**Independence analysis:**
- Papers 02, 03 are fully independent — start immediately in parallel
- Papers 04, 05, 06 are independent of each other — can run 2-3 in parallel once 02/03 free up
- Paper 07 shares simulation code with Paper 02 — start after 02's sim is stable
- Paper 10 overlaps with Paper 04 on silicon — coordinate scope before starting
- Paper 09 is fully independent (no simulation) — can slot in anytime

---

## Actionable Checklist

### Paper 01: ISRU Economic Crossover
- [x] Simulation code (isru_model.py, isru_mc.py)
- [x] Figure generation (generate_isru_figures.py)
- [x] LaTeX paper — Version A through AM
- [x] 3/3 Accept (Claude, Gemini, GPT)
- [x] Publication package (papers/01-isru-economic-crossover/)
- [x] CHANGELOG (39 versions documented)
- [x] Code refactored for publication (README, LICENSE, requirements.txt)
- [x] Site content updated to reflect paper findings
- [x] Blog article written
- [ ] Update AM tex `PENDING` commit hash to actual hash
- [ ] Submit to *Advances in Space Research*

### Paper 02: Swarm Coordination Scaling
- [x] **Simulation Code**
  - [x] Port `discrete-event-sim.ts` → `swarm_model.py` (DES engine, topology, message passing, coordinator model)
  - [x] Port `monte-carlo.ts` → `swarm_mc.py` (MC engine, topology comparison, scaling analysis, PRCC)
  - [ ] Cross-validate Python vs TypeScript outputs
  - [x] Write pytest suite (124 tests pass — `test_swarm_model.py` + `test_swarm_mc.py`)
  - [x] Profile and optimize (O(1) node lookup, lazy scheduling, batched power, gossip early-exit)
- [x] **Figures**
  - [x] Create `generate_swarm_figures.py` (--fast mode: ~90s, full mode: ~30min)
  - [x] Fig 1: Communication overhead vs. node count (all topologies)
  - [x] Fig 2: Message latency distribution at 3 scales
  - [x] Fig 3: Overhead vs. cluster size optimization
  - [x] Fig 4: Duty cycle Pareto frontier
  - [x] Fig 5: Scaling trajectory with/without optimization
  - [x] Fig 6: Architecture diagram (4-level hierarchy)
  - [x] Fig 7: Failure resilience vs. failure rate
  - [x] Fig 8: Topology comparison summary
- [x] **Paper — Version A through E** (5 review rounds: 1 Minor + 2 Major)
  - [x] Verify all arXiv citations exist (3 fixed: tolstaya year, li year, badescu title)
  - [x] Write Version A (full LaTeX — 585 lines, 10 pages, 8 figures integrated)
  - [x] Write Versions B through E (5 review rounds)
  - [x] Fix figures (protocol overhead baseline subtraction, annotation positioning)
- [x] **Code-Level Fixes** (Version F)
  - [x] Fix bandwidth model — compressed summaries (512B cluster, 1024B region) between tiers
  - [x] Add intermediate-scale data points (20k, 30k, 40k, 60k, 80k nodes)
  - [x] Add per-tier message decomposition (Fig 9: intra-cluster vs inter-cluster vs central)
  - [x] Write Version F with code fixes + run review (1 Minor + 1 Major + 1 Unknown)
  - [x] Add Fig 9: per-tier message decomposition stacked area chart
- [ ] **Remaining Issues** (from Version F reviews)
  - [ ] Add stochastic link availability model or strengthen idealised-link caveats
  - [ ] Rigorous DES-level evaluation of three optimizations (currently analytical projections)
  - [ ] Run Version G+ review cycle → 3/3 Accept
  - [ ] Create CHANGELOG
- [ ] **Publication Package**
  - [ ] Assemble papers/02-swarm-coordination-scaling/
  - [ ] Update site content with paper findings
  - [ ] Write blog article

### Paper 03: Multi-Model AI Consensus
- [x] **Data Extraction & Analysis**
  - [x] Parse all 16 deliberation transcripts → structured dataset (`deliberation_analysis.py`)
  - [x] Compute convergence statistics (mean 1.44 rounds, 95% CI [1.19, 1.75])
  - [x] Analyze voting dynamics (71.5% APPROVE, 0% REJECT, self-vote r=0.13 n.s.)
  - [x] Export CSV datasets (207 votes, 16 discussions, 23 rounds)
  - [ ] Categorize divergent views (27 DV files across BOM specs)
  - [ ] Cross-reference divergent views with literature
- [x] **Figures**
  - [x] Create `generate_consensus_figures.py` (~1.2s)
  - [x] Fig 1: Rounds to convergence by category
  - [x] Fig 2: Vote distribution across rounds
  - [x] Fig 3: Convergence scatter (approve rate vs rounds)
  - [x] Fig 4: Self-vote vs. peer-vote correlation
  - [x] Fig 5: Model performance profiles
  - [x] Fig 6: System architecture diagram
  - [x] Fig 7: Word count distribution
  - [x] Fig 8: Termination voting patterns
- [x] **Paper — Version A through F** (6 review rounds: 3/3 Major)
  - [x] Verify all citations (5 fixed: arulmohan, wang, zheng year, chan venue, wu authors)
  - [x] Write Version A (full LaTeX — 580 lines, 24 pages, 8 figures integrated)
  - [x] Write Versions B through F (6 review rounds)
  - [x] Run aggregation-only baseline (16/16 questions)
  - [x] Run self-refinement baseline (4 stratified questions)
- [x] **Version G Improvements**
  - [x] Transcript-based similarity analysis (TF-IDF cosine, keyword Jaccard, heading overlap)
  - [x] Key finding: cross-model similarity DECREASES across rounds (evidence against sycophancy)
  - [x] Reduce paper length 27% (890→647 lines, targeting IEEE IS ~8k-9k words)
  - [x] Add reproducibility metadata note (endpoint IDs, dates, system prompt hashes)
  - [x] Soften overclaims per reviewer feedback
  - [x] Run Version G review (2 Major + 1 Unknown)
- [ ] **Remaining Issues** (from Version G reviews)
  - [ ] Run prompt-matched controlled experiment (Experiment 3: Blind Deliberation, est. <$1,400)
  - [ ] Recruit 2-3 independent domain experts for blinded divergent view evaluation
  - [ ] Run Version H+ review cycle → 3/3 Accept
  - [ ] Create CHANGELOG
- [ ] **Publication Package**
  - [ ] Assemble papers/03-multi-model-ai-consensus/
  - [ ] Include deliberation transcripts as supplementary data
  - [ ] Write blog article

### Paper 04: Microgravity Metallurgy
- [ ] **Literature Review**
  - [ ] Catalog all ISS metallurgy experiments (ESA/JAXA/NASA)
  - [ ] Summarize Marangoni convection effects on grain structure
  - [ ] Analyze buoyancy-free solidification studies
  - [ ] Review terrestrial zone refining scaling laws
  - [ ] Assess artificial gravity fallback cost/mass implications
- [ ] **Parametric Analysis**
  - [ ] Scaling law model: lab-scale → industrial production
  - [ ] Thermal management sizing for microgravity processing
  - [ ] Define quantitative go/no-go criteria for Gate 1
- [ ] **Paper**
  - [ ] Write Version A (full LaTeX)
  - [ ] Run iterative AI peer review → 3/3 Accept
  - [ ] Create CHANGELOG
- [ ] **Publication Package**

### Paper 05: ISRU Water Extraction
- [ ] **Simulation Code**
  - [ ] Extend Paper 01 NPV framework for source comparison
  - [ ] Water extraction yield model (thermal, energy, purity)
  - [ ] Transport cost model: NEA → L4/L5 vs. Moon → L4/L5
  - [ ] Monte Carlo over extraction yield, purity, delta-v, energy cost
  - [ ] pytest suite
- [ ] **Figures**
  - [ ] Create `generate_water_figures.py`
  - [ ] Source comparison cost curves
  - [ ] Optimal source as function of program scale
  - [ ] Extraction rate sensitivity analysis
  - [ ] Transport delta-v comparison
- [ ] **Paper**
  - [ ] Write Version A (full LaTeX)
  - [ ] Run iterative AI peer review → 3/3 Accept
  - [ ] Create CHANGELOG
- [ ] **Publication Package**

### Paper 06: Cryogenic Propellant Architecture
- [ ] **Trade Study Model**
  - [ ] LH2/LOX vs. storable propellant comparison model
  - [ ] Cryocooler technology assessment (current → required)
  - [ ] ZBO depot thermal model
  - [ ] Fleet sizing cascade: Isp → fleet size → propellant demand → ISRU plant
  - [ ] Decision framework: cryocooler TRL threshold for LH2 architecture
- [ ] **Figures**
  - [ ] Cryo vs. storable total program cost comparison
  - [ ] Fleet sizing cascade diagram
  - [ ] Cryocooler TRL decision boundary
  - [ ] Depot thermal balance
- [ ] **Paper**
  - [ ] Write Version A (full LaTeX)
  - [ ] Run iterative AI peer review → 3/3 Accept
  - [ ] Create CHANGELOG
- [ ] **Publication Package**

### Paper 07: Collision Avoidance Certification
- [ ] **Analysis & Simulation**
  - [ ] Extend Paper 02 collision model for cascade dynamics
  - [ ] Kessler threshold analysis for heliocentric orbits
  - [ ] Mean-field collision model for large populations
  - [ ] Certification framework proposal
- [ ] **Paper**
  - [ ] Write Version A
  - [ ] Run review cycle → 3/3 Accept
- [ ] **Publication Package**

### Paper 08: Space Solar Power Economics
- [ ] **New Simulation Code**
  - [ ] SSP revenue model (production → deployment → transmission → revenue)
  - [ ] Transmission efficiency model (microwave vs. laser)
  - [ ] Market analysis (demand projections, price competition)
  - [ ] Monte Carlo break-even analysis
- [ ] **Paper**
  - [ ] Write Version A
  - [ ] Run review cycle → 3/3 Accept
- [ ] **Publication Package**

### Paper 09: Multi-Century Governance
- [ ] **Literature Analysis**
  - [ ] Historical multi-century project case studies
  - [ ] Ostrom commons governance framework application
  - [ ] Constitutional design for irreversible decisions
  - [ ] Space governance comparison (COPUOS, ITU, IADC)
  - [ ] Synthesize 4 concluded AI deliberations on governance topics
- [ ] **Paper**
  - [ ] Write Version A
  - [ ] Run review cycle → 3/3 Accept
- [ ] **Publication Package**

### Paper 10: In-Space Thin-Film Deposition
- [ ] **Technology Assessment**
  - [ ] CdTe, CIGS, perovskite, a-Si process flow analysis for space
  - [ ] Material availability from ISRU feedstock
  - [ ] UMG silicon efficiency vs. purity curves
  - [ ] Economic crossover model (Paper 01 methodology)
- [ ] **Paper**
  - [ ] Write Version A
  - [ ] Run review cycle → 3/3 Accept
- [ ] **Publication Package**

---

## Cross-Paper Dependencies

```
Paper 01 (complete)
  └── methodology reused by → Paper 05, Paper 08, Paper 10
  └── revenue analysis extended by → Paper 08

Paper 02 (in progress)
  └── simulation code shared with → Paper 07
  └── case study used in → Paper 03

Paper 03 (in progress)
  └── governance convergence data used by → Paper 09
  └── methodology applies to all papers (meta-level)

Paper 04
  └── silicon scope coordinated with → Paper 10

Paper 05
  └── water extraction informs → Paper 06 (propellant source)

Paper 06
  └── propellant architecture constrains → Paper 05 (ISRU chemistry)
```

---

## Feasibility Risk Coverage After All Papers

| Risk | Level | Paper | Coverage |
|------|-------|-------|----------|
| Microgravity metallurgy | Project-ending | 04 | Literature review + scaling laws |
| ISRU water extraction | Project-ending | 05 | Parametric model + source comparison |
| Cryocooler scaling | Architecture-change | 06 | Systems trade study |
| Silicon purity | Architecture-change | 04 + 10 | Literature (04) + crossover model (10) |
| Collision avoidance | Critical | 02 + 07 | Simulation (02) + certification (07) |
| ISRU economics | Resolved | 01 | **Complete** |
| Swarm coordination | High | 02 | Simulation + validation |
| Multi-model methodology | Meta | 03 | Empirical analysis |
| SSP revenue viability | High | 08 | Economic model |
| Governance | Medium | 09 | Policy analysis |

**Result:** All project-ending and architecture-change risks have dedicated papers. All 5 decision gates have at least one paper providing evidence.

---

## Shared Infrastructure

### Reusable from Paper 01
- NPV cost framework (`isru_model.py`) — reuse for Papers 05, 08, 10
- Monte Carlo engine with PRCC (`isru_mc.py`) — reuse for Papers 05, 08
- Figure generation patterns — reuse structure for all papers
- Publication packaging (symlinks, README, LICENSE) — standardized

### New Infrastructure Needed
- DES engine in Python (Paper 02) — reuse for Paper 07
- Deliberation transcript parser (Paper 03) — one-time
- SSP revenue model (Paper 08) — new
- Thin-film crossover model (Paper 10) — extends Paper 01 pattern

### AI Peer Review Process
- Standardized across all papers: 3 reviewers, 6 criteria, iterative to 3/3 Accept
- Review scripts: adapt from Paper 01 process
- CHANGELOG generation: adapt from Paper 01 tooling
