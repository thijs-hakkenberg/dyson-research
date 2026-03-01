# Publication Plan — Project Dyson Research Papers

**Last updated:** 2026-02-28
**Papers planned:** 10 (1 complete, 9 in pipeline)
**Open research questions:** 107 of 142 (75%)
**Publication-addressable:** 29 questions across 10 papers

---

## Status Overview

| # | Paper | Tier | Status | Blocking |
|---|-------|------|--------|----------|
| 01 | ISRU Economic Crossover | 1 | **COMPLETE** (3/3 Accept, Version AM) | — |
| 02 | Swarm Coordination Scaling | 1 | **Version CE** — 1 Accept + 2 Major (84 versions) | Feasibility flowchart, operational calibration, DES distributional strengthening, k_c/k_c-1 audit |
| 03 | Multi-Model AI Consensus | 1 | **Version J** — 1 Minor + 2 Major (10 versions) | Controlled baselines, inter-rater reliability, voting robustness analysis |
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
  - [x] Write pytest suite (118+29=147 tests pass — `test_swarm_model.py` + `test_swarm_mc.py`)
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
- [x] **Version G Code Infrastructure** (addressing Version F review items)
  - [x] Implement exception-based telemetry as DES mechanism (configurable threshold)
  - [x] Add stochastic link availability model (Bernoulli per-message, coordinator tracking)
  - [x] Formal statistical testing for superlinear transition (AIC: linear vs power-law vs piecewise)
- [x] **Version G — Tex Updates** (addressing all Version F review items)
  - [x] Reconcile all overhead numbers (DES-measured 1.8%-12.8%, DES/Projected labels)
  - [x] Add traffic accounting table (8 message types)
  - [x] Add formal metric definitions (overhead, cycle period, success, latency, handoff)
  - [x] Exception-based telemetry DES results (reduction 0.27 vs predicted 0.30)
  - [x] Link availability sensitivity analysis (sweep 0.4-1.0, topology ranking preserved ≥0.7)
  - [x] Formal statistical testing (piecewise AIC=-51.3, breakpoint N*=45k [40k,50k])
  - [x] Fix U-shape explanation (topology effects, not saturation)
  - [x] Frame mesh as intentional upper bound throughout
  - [x] Run Version G review (1 Minor + 2 Major)
- [x] **Version H — Address Version G Reviews** (1 Accept + 1 Major + 1 Reject)
  - [x] Replace analytical overhead with DES byte-count measurement
  - [x] Add coordinator bandwidth parameterization (Table IX)
  - [x] Fix timing consistency (T_c=10s all topologies)
  - [x] Multi-scale exception telemetry validation (Table VIII)
  - [x] Remove all "superlinear" claims, reframe as slope change
  - [x] Retransmission mechanism + link availability table (Table VII)
  - [x] Blocked by placeholder "---" in Tables V-IX (GPT=Major, Claude=Reject)
- [x] **Version I — Fix DES and Populate Tables**
  - [x] Fix `_reschedule_state_sync` exponential decay bug (always reschedule sampled nodes)
  - [x] Fix `_hierarchical_routing` to upward-aggregation only (no coordinator broadcast)
  - [x] Fix coordinator bandwidth cap to account for node sampling rate
  - [x] DES now shows constant ~21% overhead across N=1k-100k (O(1) scaling — key result)
  - [x] Populate all 4 tables with DES data (scaling, exception, link, coord bandwidth)
  - [x] Reframe paper: "slope change" → "constant overhead" (stronger result)
  - [x] All 132 tests pass (103 swarm_model + 29 swarm_mc)
  - [x] Run Version I review cycle (1 Minor + 2 Major)
- [x] **Versions J-Y** (16 additional review rounds)
  - [x] DES features: exception telemetry, stochastic link model, GE link model, workload profiles
  - [x] Statistical testing (AIC piecewise), AoI analysis, coordinator capacity sizing
  - [x] Figures: workload comparison, link model comparison, sensitivity sweep, AoI quality, TDMA comparison
  - [x] Version Y scores: Claude Major (3.67), Gemini Minor (4.50), GPT Major (3.67)
- [x] **Version Z: Structure refactor** — foreground 3 DES-unique contributions
  - [x] Restructure: coordinator capacity → AoI analysis → GE link model as primary results; O(1) verification as concise validation
  - [x] Specify coordinator timing model (pseudocode: member reports, aggregation, forwarding)
  - [x] Remove km claim from abstract; keep AoI in seconds, move km mapping to discussion with caveats
  - [x] Extend sectorized mesh comparison to all 3 workload profiles (run DES + update figure)
  - [x] Fix notation: gossip b/f footnote, eta→eta_proto
  - [x] Trim abstract, discussion, baseline note, contributions (~8% length reduction — short of 25-30% target)
  - [x] Run Version Z review: **Gemini Accept (4.67), Claude Major (3.17), GPT Major (3.50)**
  - [ ] Create CHANGELOG
- [x] **Version AA — Address Version Z Reviews**
  - [x] Add leaky-bucket ingress model + dual-model comparison table (Table~XII)
  - [x] Disambiguate "Coordination Success" → "Msg. Delivery (%)" with per-message/per-cycle footnotes
  - [x] Sweep sectorized mesh neighbor cap {5,10,20,50} with analytical table
  - [x] Latency path decomposition (propagation + processing + queueing) with phase-stagger mention
  - [x] Fix stale cross-references (V-E → V-C, IV-B → IV-G, IV-G → sec:coordinator_bandwidth)
  - [x] Finalize reproducibility: GE params + processing delay in Table~V, code tag in Data Availability
  - [x] TDMA guard-time γ=0.85 derivation (sync uncertainty + ramp + guard)
  - [x] Harmonize heartbeat sizes (footnote explaining 32B vs 64B difference)
  - [x] Coordinator election dead time quantified (<0.01% availability loss)
  - [x] Removed redundant coordinator summary table, trimmed analytical cross-check, removed sectorized mesh discussion subsection
  - [x] Run Version AA review: **Gemini Minor (4.83), Claude Major (3.00), GPT Major (3.50)**
  - Note: Gemini regressed from Accept (Z) to Minor (AA); TDMA derivation drew extra scrutiny
- [x] **Version AB — Code Changes + Address Version AA Reviews**
  - [x] **Phase-stagger experiment** (CODE): `enable_phase_stagger` config option, deterministic cluster offsets in `_schedule_state_sync_events()`, new Fig 16 (drops at ~25 kbps vs 50 kbps under random phase)
  - [x] **AoI-to-ephemeris coupling** (CODE): σ(t) = σ₀ + σ̇·AoI model in `_generate_result()`, config params `aoi_sigma_0_m=10`, `aoi_sigma_dot_m_per_s=0.5`, P99 441s → ~230 m position error
  - [x] **Overhead decomposition** (CODE): 6 per-message-class byte counters (`_ephemeris_bytes_sent`, etc.), new Fig 15 (commands >60% under stress, summaries <1%), Vallado reference added
  - [x] Phase stagger removes "Unresolved Questions" item 2 (now resolved experimentally)
  - [x] Updated abstract (4 contributions, position error, decomposition), conclusion (4 bullet points), contributions list
  - [x] All 103 tests pass, smoke tests pass, PDF compiles (no errors)
  - [x] Run Version AB review: **Gemini Accept (4.83), Claude Major (3.17), GPT Major (3.67)**
- [x] **Version AC — Address Version AB Reviews (all 3 reviewers)**
  - [x] Reposition DES contribution: "systematic integration" not "inaccessible to closed-form" (abstract, contributions, conclusion)
  - [x] Elevate coordinator Model B as recommended baseline, Model A as conservative bound
  - [x] Add operational mapping for stress-case workload (orbit-raising, formation-keeping, conjunction commanding)
  - [x] Add AoI analytic cross-check: geometric distribution derivation (Eq. 8), bootstrap CI [438, 444] s
  - [x] Soften AoI operational conclusions: first-order input not full conjunction assessment, cite Alfano P_c
  - [x] Add GE per-cycle cluster completion metric: <1% for k_c≥50, inter-cycle store-and-forward required
  - [x] Update conclusion: remove "inaccessible to closed-form", add γ caveat, update AoI bullet
  - [x] PDF compiles (464 KiB), version tag updated to paper-02-v-ac
  - [x] Run Version AC review: **Gemini Minor (4.50), Claude Major (3.33), GPT Major (3.67)**
  - Gemini regressed from Accept to Minor; all 3 want DES reframing, AoI threshold removal, γ sensitivity extension, continuous p_cmd sweep
- [ ] **Version AD — Address Version AC Reviews (all 3 reviewers)**
  - [x] Reframe DES as "validated parametric sweep tool" not "discovery instrument" (abstract, contributions, conclusion)
  - [x] Remove ALL AoI threshold claims — label Eq as "illustrative back-of-envelope"
  - [x] Add coordinator tier separation (cluster/regional/downlink bottleneck breakdown)
  - [x] Extend γ sensitivity sweep to 0.3 (Slotted ALOHA) + add stability boundary discussion
  - [x] Add continuous command-rate sweep figure (Fig 17: η vs p_cmd)
  - [x] Add C_node generality statement in contributions ("η applies at any C_node")
  - [x] PDF compiles (485 KiB), version tag updated to paper-02-v-ad
  - [x] Run Version AD review: **Gemini Accept (4.67), Claude Major (3.33), GPT Major (3.67)**
- [x] **Version AE — Fix μ_c/processing, relaxed completion, √N justification, design equations**
  - [x] Run Version AE review: **Gemini Accept, Claude Major, GPT Major**
- [x] **Version AF — Chernoff bound burstiness, dual-regime analysis, honest latency comparison**
  - [x] Run Version AF review: **Gemini Accept (4/5/4/5/5/4), Claude Major (3/3/3/4/4/3), GPT Major (4/3/3/4/4/4)**
- [x] **Version AG — DES value-add, physical-layer TDMA vignette, realistic centralized baseline**
  - [x] Joint GE×capacity independence experiment (run_joint_experiment2.py): GE retransmissions and coordinator drops are independent
  - [x] Add Section IV-D "Joint Parameter Interaction Verification" with Table (DES-specific contribution)
  - [x] Add physical-layer TDMA vignette: 500 km cluster, 24 kbps achievable, guard time derivation
  - [x] Add realistic centralized baseline (c=N/k_c, ρ≤0.7) — does not diverge until N≈10⁶
  - [x] Add Table 8 duty cycle analytical derivation (power CV, handoff success ARQ, Markov availability)
  - [x] Update abstract: mention joint independence result, physical-layer grounding, realistic centralized
  - [x] Update contributions: reframe DES as testing joint interactions analytical models cannot address
  - [x] Update conclusion: 5 results (including joint independence), realistic centralized baseline narrative
  - [x] PDF compiles (510 KiB)
  - [x] Run Version AG review
- [x] **Versions AH–BZ** (additional review rounds through Version BZ)
  - [x] Slot-level TDMA simulator, packet-level validation, link budget, orbital mechanics
  - [x] Airtime enforcement, distributed workload profiles, cross-cycle recovery tracking
  - [x] Exception telemetry, sectorized mesh cap sweep, coordinator scheduling models
  - [x] Fleet-level channel reuse analysis, unicast stagger derivation
  - [x] Figures expanded to 19 (AoI quality, sensitivity sweep, TDMA comparison, workload comparison, link model, overhead decomposition, phase stagger, command-rate sweep, cross-cycle recovery, fleet reuse)
  - [x] Tests expanded to 116 (airtime enforcement, distributed workload, cross-cycle recovery)
- [x] **Version CA — Campaign duty factor (d) + γ=0.76 unification**
  - [x] Campaign duty factor d∈[0,1] gates command generation per cycle (Bernoulli)
  - [x] η(d) = η₀ + d·η_cmd linear model with Table showing d=0.01→~5%, d=0.10→~9%, d=1.0→46%
  - [x] γ=0.76 from CCSDS Proximity-1 packet-level derivation applied consistently throughout
  - [x] Generalized γ equation (Eq. gamma_general) for arbitrary framing/FEC/acquisition parameters
  - [x] Run Version CA review: **Gemini Accept (5/5/4/5), GPT Major (4/3/3/4), Claude Major (3/3/4/3)**
  - Claude Validity improved 3→4, but Methodology stuck at 3
- [x] **Version CB — Address 5 common reviewer themes across CA reviews**
  - [x] **Theme 1: DES verification tautology** — Renamed "Overhead Verification" → "Implementation Consistency and Distributional Analysis"; added coordinator ingress CDF figure (Fig 20) showing bimodal distribution under stochastic d; reframed DES role in verification taxonomy and claim map (added "Distrib." column)
  - [x] **Theme 2: Sectorized mesh removal from comparisons** — Removed sectorized_mesh traces from 4 comparison figures (sensitivity sweep, workload comparison, overhead decomposition, command-rate sweep); kept in topology comparison table with †footnote; shortened sectorized subsection from 3 paragraphs to 1
  - [x] **Theme 3: Packet-level "validation" → "γ derivation"** — Renamed Section IV-J to "Standards-Grounded γ Derivation"; replaced all "packet-level validation" language with "standards-grounded γ derivation" (8 locations)
  - [x] **Theme 4: ≥10 kbps regime expansion** — Added 2 paragraphs analyzing higher-rate regime: antenna scheduling, interference, processing latency as binding constraints; "non-binding" finding tells practitioners 1 kbps is the only regime needing TDMA
  - [x] **Theme 5: Generalized γ equation** — Parametrized framing overhead as O_frame (was hardcoded 104 bits); added CCSDS TC Space Data Link worked example (O_frame=64, γ=0.79, 4% improvement)
  - [x] Code: coordinator ingress per-cycle tracking in swarm_model.py, 2 new tests (118 total pass), Fig 20 coordinator buffer CDF
  - [x] PDF compiles to 15 pages, 0 warnings
  - [x] Run Version CB review: **Gemini Accept (5/5/4/5), GPT Major (4/3/3/4), Claude Major (3/3/3/4)**
  - Gemini: Preserved Accept with Minor Revisions (Sig 5, Meth 5, Valid 4, Clarity 5)
  - GPT: Methodology 3, Validity 3, unchanged from CA. Still Major Revision.
  - Claude: Clarity improved 3→4. Validity regressed 4→3. Methodology stuck at 3. Still Major Revision.
  - **Net progress:** Claude Clarity +1, Claude Validity −1, all else unchanged. Target Meth 3→4 NOT achieved.
- [x] **Version CC — Address Version CB Reviews (definition tightening)**
  - [x] **Canonical η definitions** — Added canonical 3-tier decomposition (baseline/η₀/η_cmd) with Eq. eta_canonical in Section III-C; cross-referenced from all subsequent η mentions; replaced old Traffic Accounting subsection with single cross-ref
  - [x] **DES-TDMA disambiguation** — Added "Tool scope disambiguation" paragraph in Section III-A explicitly stating DES = fluid-server (no slots, no guard intervals), slot-sim = TDMA scheduling; DES drops ≠ TDMA deadline misses
  - [x] **GE coherence time justification** — Strengthened per-cycle assumption: now explicitly labeled as modeling choice; quantified conservatism per mechanism (structural ≈ T_c, mispointing > T_c → use p_BG ≤ 0.10 curves)
  - [x] **Campaign duty factor temporal correlation** — Added paragraph acknowledging Bernoulli limitation: exact for mean η, optimistic for peak buffer occupancy; geometric-duration model would produce identical η(d) with longer continuous bursts
  - [x] **η₀ decomposition audit** — Reconciled component sum (5.6%) vs DES measurement (5.0%): coordinator self-exclusion explains 0.6 pp difference; cross-referenced canonical definition
  - [x] Removed "Earlier versions: 0.850, Now superseded" row from Table IX (internal revision history per Claude Minor #14)
  - [x] PDF compiles to 15 pages, 0 warnings
  - [x] Run Version CC review: **Gemini Accept (5/5/4/5), GPT Major (4/3/3/4), Claude Major (3/3/3/4)**
  - Gemini: Preserved Accept with Minor Revisions — all scores identical to CB
  - GPT: All scores identical to CB. Still wants: γ consistency audit across all layers/tools, ON/OFF campaign model, requirements-to-modes mapping, Layer 2→3 formalization
  - Claude: All scores identical to CB. Still wants: honest DES scoping (reduce emphasis), ISL-specific GE grounding, topology comparison with real alternative, operational data, 30% length reduction
  - **Net progress:** Definition edits addressed surface clarity but did NOT move Methodology 3→4. Root cause: reviewers want structural changes (new modeling, data grounding, paper condensation), not definition polish
- [x] **Version CD — Structural Changes (target: Claude/GPT Methodology 3→4)**
  - [x] **ON/OFF Markov campaign model** — Added ON/OFF alternative to Bernoulli duty factor with geometric ON duration; DES validates heavier-tailed coordinator ingress under correlated bursts (Fig. 7)
  - [x] **Two-layer reframing (partial)** — Abstract says "two layers" but body/Table IX still showed 3 layers
  - [x] **GE qualification as parametric study** — GE analysis reframed as parametric sensitivity study with "illustrative rather than predictive" disclaimer; mechanism→regime mapping added
  - [x] **γ rate-dependence** — Added γ(30 kbps)=0.745 note; stated γ=0.76 as conservative 24 kbps reference
  - [x] **Paper condensation** — 15→14 pages
  - [x] Run Version CD review: **Gemini Accept (5/5/4/5), GPT Major (4/3/3/4), Claude Major (3/3/3/4)**
  - Claude: Validity regressed 4→3. Two-layer reframing was incomplete (abstract vs body inconsistency); GE "illustrative" disclaimer drew more attention without compensating mechanism→parameter table.
  - GPT: Unchanged. Wants γ rate-dependence applied consistently, feasibility flowchart, k_c vs k_c-1 audit.
  - Gemini: Preserved Accept. All scores identical.
  - **Net progress:** Claude Validity −1 (regression). Target Meth 3→4 NOT achieved.
- [x] **Version CE — Cross-Reviewer Structural Fixes (target: Claude Validity 3→4, Claude/GPT Meth 3→4)**
  - [x] **Complete two-layer restructure** — Table IX restructured from 3 layers to 2 (byte budget + airtime schedulability); PHY translation η/γ now labeled as necessary condition, not independent layer; all "Layer 3" and "three primary" references removed
  - [x] **γ(R_PHY) master table** — Added Table (PHY Rate Feasibility) with γ computed at 24/30/50 kbps; Eq. gamma_general rewritten with explicit 10^-3 unit annotation; γ=0.76 instances qualified with "(24 kbps reference)" where applicable
  - [x] **GE mechanism→parameter mapping table** — Added formal mechanism→parameter table (structural shadowing, antenna mispointing, Earth occultation) with estimated τ_c, p_BG, p_B, P95 recovery; caveat elevated to abstract
  - [x] **Concrete duty-factor scenarios** — Three worked campaign examples (orbit-raising d=0.05, station-keeping d=0.01, collision avoidance d→1.0) with annual-average and peak η values; abstract now pairs 46% with "routine 5–10%"
  - [x] **Contribution reframing** — Contributions list leads with "two-layer feasibility framework"; conclusion adds framework-value sentence; reduced from 4 items to 3
  - [x] **AoI operational mapping table** — Added AoI→function mapping (conjunction screening, maneuver execution, formation keeping, safe-mode)
  - [x] **DES further compression** — Compressed DES agreement text; condensed Table VIII (scaling) to summary rows
  - [x] **Notation table expansion** — Added α_RX, q, L_cmd, f_RF, F, R to Table I
  - [x] **η₀ arithmetic fix** — Replaced vague "coordinator self-exclusion" with explicit formula derivation (0.01 × 320 × 8 / 10000 = 0.026 pp/component ≈ 0.5 pp total)
  - [x] **Sectorized mesh minimized** — Moved from topology comparison table to footnote; cleaned figure caption
  - [x] **Cross-model table removed** — Replaced Table XIII with 2-sentence inline summary, saving ~12 lines
  - [x] **Additional condensation** — Cluster size table inlined; duty cycle table inlined; verification taxonomy condensed
  - [x] PDF compiles to 14 pages, 0 warnings
  - [x] Run Version CE review: **Gemini Accept (5/5/4/5), GPT Major (4/3/3/4), Claude Major (3/3/4/4)**
  - Gemini: Preserved Accept w/ Minor. All scores identical to CD. Wants RF-backup justification and unicast latency discussion.
  - GPT: Unchanged (4/3/3/4). Still wants feasibility flowchart/pseudocode, k_c vs k_c-1 consistency audit, empirical d anchoring, γ rate-dependence enforced everywhere, stress-case reframing with annual CDF.
  - Claude: Validity 3→4 (target met!). Significance 3, Methodology 3 unchanged. Wants operational calibration point, DES distributional strengthening, packet-level repositioning, static topology bounds.
  - **Net progress CD→CE:** Claude Validity 3→4 (+1). All other scores unchanged. Gemini Accept preserved.
  - **Cumulative (CC→CE):** Claude Validity 3→3→4, all others unchanged across CC/CD/CE.
- [ ] **Version CF — Next Steps (target: Claude/GPT Methodology 3→4)**
  - [ ] **Feasibility flowchart/pseudocode** — GPT CE Major #1: Present single algorithmic feasibility test (inputs → η → γ(R) → slot time → ingress/egress inequalities → minimum PHY rate)
  - [ ] **k_c vs k_c-1 consistency audit** — GPT CE Major #2: Standardize coordinator ingress expressions; reconcile 20.3 vs 20.5 kbps; update all equations/abstract/tables
  - [ ] **Operational calibration point** — Claude CE Major #5: Map Starlink conjunction screening cadence to framework parameters; validate AoI prediction
  - [ ] **DES distributional strengthening** — Claude CE Major #1: Add joint AoI×buffer occupancy, coordinator handoff transients, or correlated failure cascades
  - [ ] **γ rate-dependence everywhere** — GPT CE Major #4: Introduce γ_24/γ_30 or always write γ(R_PHY); update all numeric claims
  - [ ] Run Version CF review → target Claude/GPT Methodology 3→4
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
- [x] **Version H Analysis Infrastructure** (addressing Version G review items)
  - [x] Add semantic similarity: n-gram (1-3) TF-IDF, decision-sentence TF-IDF, tech parameter Jaccard
  - [x] All 6 metrics decrease across rounds (decision Δ=-0.031, tech params Δ=-0.064)
  - [x] New fig-decision-similarity.pdf (decision-sentence vs tech parameter trends)
  - [x] Create divergent view coding manual with operational definitions + real examples
- [x] **Version H — Tex Updates**
  - [x] Expand similarity analysis to 6 metrics (all decreasing, decision Δ=-0.031, tech Δ=-0.064)
  - [x] Add decision-similarity figure and comparison table
  - [x] Strengthen sycophancy discussion with semantic-level evidence
  - [x] Reference coding manual (Supplementary S1)
  - [x] Add Design Decisions subsection (winner visibility, truncation, self-vote)
  - [x] Sharpen novelty framing (3 precise contributions)
  - [x] Add 3 citations (Sharma, Lakshminarayanan, Christensen)
  - [x] Run Version H review (1 Accept + 2 Major)
- [x] **Version I — Address Version H Reviews**
  - [x] Run repeated trials: 4 questions × 5 repetitions at T=0.7
  - [x] Add commitment-level adoption analysis (Table 10)
  - [x] Version I scores: Claude Major (3.5), Gemini Minor (4.67), GPT Major (3.5)
- [x] **Version J: Statistical rigor + extraction procedure**
  - [x] Specify divergent view extraction procedure (3-step process with worked example from rq-1-24)
  - [x] Resolve inter-rater reliability: made consistent (single annotator, no kappa, 81% AI agreement as plausibility check)
  - [x] Add bootstrap CIs and Wilcoxon tests for similarity metrics (all non-significant, CIs overlap zero)
  - [x] Soften sycophancy claims throughout (4 locations: similarity analysis, interpretation, limitations, conclusion)
  - [x] Strengthen confounded baselines discussion (explicit about prompt/format differences)
  - [x] Run Version J review: **Gemini Minor (4.50), Claude Major (3.50), GPT Major (3.50)**
  - [ ] Create CHANGELOG
- [ ] **Version K+ — Address Version J Reviews** (consensus demands from Claude + GPT)
  - [ ] Run controlled baseline experiment: prompt-matched aggregation-only (Exp 1) + self-refinement (Exp 2) — All 3 demand
  - [ ] Obtain inter-rater reliability: recruit 2 independent coders OR LLM-as-judge proxy, report Cohen's κ — All 3 demand
  - [ ] Run winner-hidden ablation (even on 4 questions) to isolate anchoring — GPT strongest
  - [ ] Add voting robustness analysis: margin distributions, Condorcet cycles, tie-break sensitivity — GPT
  - [ ] Reframe similarity analysis as "descriptive characterization" not "evidence against sycophancy" — Claude + GPT
  - [ ] Separate "sycophancy" vs "anchoring" vs "convergence" definitions paragraph — GPT
  - [ ] Include 2-3 deliberations on verifiable engineering problems (not Dyson swarm) — Claude
  - [ ] Tighten manuscript 20-30%: consolidate repeated limitations, condense case study — Claude
  - [ ] Fix citation hygiene: Perez [10] uncited, Zheng year mismatch, date/venue checks — Claude + GPT
  - [ ] Run review cycle → target 3/3 Accept or Minor
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
