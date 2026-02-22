# Development Plan: Paper 02 — Swarm Coordination at Billion-Unit Scale

**Working Title:** Scaling Hierarchical Coordination for Billion-Unit Space Swarms: Discrete Event Simulation and Architectural Validation

**Target Venue:** IEEE Transactions on Aerospace and Electronic Systems

**Methodology:** Iterative AI peer review (Claude/Gemini/GPT), following the Paper 01 process (39 versions, 3/3 Accept)

---

## Current State Assessment

### What Already Exists

1. **Detailed outline** (`02-swarm-coordination-scaling.md`) — 277 lines covering abstract through references, 8 figures planned, 7 sections
2. **LaTeX + PDF draft** — initial compilation exists
3. **Discrete event simulation engine** (`src/lib/services/simulation/swarm-coordination/discrete-event-sim.ts`) — TypeScript, event-driven with message passing
4. **Monte Carlo wrapper** (`src/lib/services/simulation/swarm-coordination/monte-carlo.ts`) — parameter sweeps over the DES
5. **Interactive web simulators:**
   - `CoordinationSimulator.svelte` — topology comparison (centralized/hierarchical/mesh)
   - `SwarmDynamicsSimulator.svelte` — collision probability and stationkeeping
6. **5 answered research questions:**
   - rq-1-24: Swarm coordination architecture at scale (simulation, answered)
   - rq-1-39: Cluster coordinator duty cycle (simulation, answered)
   - rq-1-6: Swarm collision probability (simulation, answered)
   - rq-2-17: Fleet coordination scale constraints (simulation, answered)
   - rq-1-37: Propulsion actuation authority (simulation, answered)
7. **3 blog posts** summarizing preliminary findings:
   - `swarm-coordination-architecture-findings.md`
   - `swarm-dynamics-station-keeping-collision-findings.md`
   - `deployment-optimization-strategy-findings.md`

### What Needs to Be Built

The outline is comprehensive but the simulation code is TypeScript (web simulator). For a publication-quality paper following Paper 01's methodology, we need:

1. **Python simulation code** — standalone, reproducible, seed-controlled (like `isru_model.py`/`isru_mc.py`)
2. **Figure generation pipeline** — `generate_swarm_figures.py` producing all 8 publication figures
3. **Rigorous statistical framework** — 10,000+ Monte Carlo runs, PRCC sensitivity, confidence intervals
4. **Literature review with real citations** — arXiv IDs verified, no hallucinated references
5. **Full LaTeX paper** — formatted for IEEE TAES submission
6. **Iterative peer review cycle** — Version A through acceptance

---

## Development Phases

### Phase 1: Simulation Code (Python Port + Extension)

**Goal:** Create publication-quality Python simulation code in `publications/scripts/`

#### 1a. Port DES Engine to Python
- Port `discrete-event-sim.ts` to `swarm_des.py`
- Event-driven architecture with heapq priority queue
- Node model: position, velocity, health, cluster assignment, power state
- Message model: type, source, destination, payload size, timestamp
- Three topology implementations:
  - **Centralized:** single coordinator, M/D/1 queue model
  - **Hierarchical:** configurable cluster size, 4-level hierarchy (ground → regional → cluster → node)
  - **Mesh:** gossip protocol with configurable fanout
- Coordinator rotation model with state transfer
- Failure model: exponential inter-arrival, configurable annual rate
- Full type hints, docstrings, PEP 8

#### 1b. Port Monte Carlo Engine
- Port `monte-carlo.ts` to `swarm_mc.py`
- Parameter sampling: node count (1K–1M), cluster size (50–500), duty cycle (1h–7d), failure rate, bandwidth
- 10,000 runs per configuration
- Output metrics: communication overhead, message latency (P50/P95/P99), coordination success rate, availability
- PRCC sensitivity analysis (reuse methodology from `isru_mc.py`)
- Kaplan-Meier survival for topology failure analysis
- Convergence diagnostics (bootstrap CI)

#### 1c. Validation
- Cross-validate Python results against TypeScript simulator outputs
- Regression tests with seed 42
- pytest suite following Paper 01 pattern

**Estimated effort:** 3–5 days

### Phase 2: Figure Generation Pipeline

**Goal:** `generate_swarm_figures.py` producing all 8 figures

| Figure | Description | Data Source |
|--------|-------------|-------------|
| Fig 1 | Communication overhead vs. node count (all topologies, log scale) | MC sweep over node count |
| Fig 2 | Message processing latency distribution at 10K/100K/1M nodes | DES histograms |
| Fig 3 | Overhead vs. cluster size optimization curve | MC sweep over cluster size |
| Fig 4 | Duty cycle Pareto frontier (power variance vs. availability) | MC sweep over duty cycle |
| Fig 5 | Overhead trajectory with/without optimizations at scale | MC comparison runs |
| Fig 6 | Hierarchical architecture diagram (4-level) | Static diagram (matplotlib/tikz) |
| Fig 7 | Dynamic spatial partitioning illustration | Animated frames or multi-panel |
| Fig 8 | Multi-model convergence summary (voting results) | Discussion transcript data |

**Estimated effort:** 2–3 days

### Phase 3: LaTeX Paper — Version A

**Goal:** Complete first draft with all sections, figures, tables, and bibliography

#### Section-by-section plan:

1. **Abstract** (250 words) — derive from simulation results, not the outline's placeholder
2. **Introduction** (500 words) — frame the coordination scaling problem, cite Starlink as motivation
3. **Related Work** (700 words) — verify all arXiv citations exist:
   - arXiv:1805.03737 (GNN multi-robot coordination) — VERIFY
   - arXiv:0604110 (Mean-field game theory) — VERIFY
   - arXiv:2302.14587 (Decentralized control) — VERIFY
   - Brambilla et al. 2013 — standard swarm robotics survey, VERIFY
   - Add: Starlink FCC filings, ESA Space Debris Office publications
4. **Simulation Framework** (800 words) — describe DES architecture, topology models, node model, MC framework
5. **Results** (1,200 words) — present all 8 figures with statistical rigor (CIs, p-values where appropriate)
6. **Multi-Model Validation** (600 words) — document the deliberation that produced the Shepherd/Flock architecture
7. **Discussion** (700 words) — applicability to near-term systems, limitations, unresolved questions
8. **Conclusion** (300 words) — summarize key findings

**Key requirement:** Every quantitative claim must trace to a specific simulation run with reproducible seed.

**Estimated effort:** 3–4 days

### Phase 4: Iterative AI Peer Review

**Goal:** Achieve 3/3 Accept following Paper 01's methodology

#### Review Process:
1. Submit Version A to Claude, Gemini, GPT simultaneously
2. Each reviewer scores across 6 criteria: technical soundness, methodology, presentation, completeness, novelty, reproducibility
3. Each reviewer provides: verdict (Accept/Minor/Major/Reject), specific issues, recommended changes
4. Address all reviewer feedback in next version
5. Resubmit and iterate

#### Expected Review Concerns (based on Paper 01 experience):
- **Claude** will likely focus on: statistical rigor, confidence intervals, sensitivity analysis completeness, caveats about simulation fidelity
- **GPT** will likely focus on: real-world validation, comparison with actual Starlink data, scalability claims beyond simulation range
- **Gemini** will likely focus on: quantitative detail, missing edge cases, computational complexity analysis

#### Estimated Timeline:
- Versions A–E: Major structural changes (2–3 weeks)
- Versions F–M: Methodological refinements (2–3 weeks)
- Versions N–Z: Presentation polish, citation verification (2–3 weeks)
- Versions AA+: Final convergence to 3/3 Accept (1–2 weeks)

**Total estimated: 8–12 weeks** (Paper 01 took ~39 versions)

### Phase 5: Publication Package

**Goal:** Mirror Paper 01's publication structure

```
publications/papers/02-swarm-coordination-scaling/
├── 02-swarm-coordination-scaling-XX.pdf → (symlink to drafts)
├── 02-swarm-coordination-scaling-XX.tex → (symlink to drafts)
├── CHANGELOG.md → (symlink to drafts)
├── code → ../../scripts  (or dedicated scripts subdirectory)
└── figures → (symlink to drafts figures)
```

- README.md for reproduction
- All code MIT-licensed
- Seed 42 for exact reproducibility
- CHANGELOG documenting version evolution

---

## Key Technical Decisions

### 1. Simulation Fidelity vs. Tractability
The DES must simulate 1 year of operations at 1M nodes. At 1-second resolution for collision avoidance, that's ~31.5M time steps. **Decision:** Use 1-minute resolution for coordination events, 1-second resolution only for collision avoidance windows (event-driven, not time-stepped).

### 2. Spatial Partitioning Algorithm
The outline proposes octree vs. k-d tree vs. S2 geometry. **Decision:** Implement octree for the paper (simplest to explain, O(N log N) complexity), note S2 as a production recommendation in Discussion.

### 3. Correlated Failure Model
The outline notes independent exponential failure model as a limitation. **Decision:** Add a correlated failure mode (solar particle events affecting spatial clusters) as a secondary analysis, showing it doesn't qualitatively change topology comparison results.

### 4. Code Organization
**Decision:** Create `publications/scripts/swarm_des.py` and `publications/scripts/swarm_mc.py` alongside existing ISRU code. Share `publications/scripts/requirements.txt` and `pyproject.toml`. The figure generator will be `generate_swarm_figures.py`.

---

## Dependencies and Risks

| Risk | Mitigation |
|------|-----------|
| DES at 1M nodes is computationally expensive | Profile early, optimize critical path, consider pypy or numba for inner loops |
| Citation verification may find hallucinated references | Verify every arXiv ID before first review submission |
| GPT reviewer may demand real-world validation data | Prepare Starlink public data comparison as supplementary material |
| Review process may take longer than Paper 01 | Set intermediate milestones, parallelize review response work |
| Python port may diverge from TypeScript results | Establish cross-validation suite before proceeding |

---

## Success Criteria

1. All simulation code passes pytest suite with >95% coverage
2. All 8 figures reproduce identically from seed 42
3. Paper achieves 3/3 Accept from AI peer reviewers
4. Results are consistent with (and supersede) web simulator findings
5. Key finding confirmed: hierarchical coordination scales to 1M+ nodes with 2–8% overhead
6. 50,000-node inflection point is statistically robust (95% CI)
