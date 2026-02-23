---
paper: "02-swarm-coordination-scaling"
generated: "2026-02-23"
type: "review-summary"
reviewers:
  - claude-opus-4-6
  - gemini-3-pro
  - gpt-5-2
---



# Comparative Peer Review Synthesis

## Version Comparison

All three reviews provided here are for **Version F (formal academic voice)** only. No Version A/B comparison is possible from the supplied materials, as each reviewer submitted a single review of one version. Therefore, a direct voice-style comparison cannot be conducted.

However, indirect observations about how the formal voice was received are informative. **Gemini 3 Pro** rated Clarity & Structure at 5/5 ("exceptionally well-written"), suggesting the formal academic register was highly effective for that reviewer. **Claude Opus 4.6** rated Clarity at 4/5 ("well-organized and generally well-written") but noted the paper was too long and broad. **GPT-5.2** also rated Clarity at 4/5, praising the information density but flagging inconsistencies between the abstract and tables that undermine readability. All three reviewers found the formal voice appropriate for IEEE T-AES, though Claude and GPT both noted that the paper's breadth came at the cost of depth—a trade-off that may be more pronounced in a formal register where concision is expected.

No reviewer expressed a preference for a more accessible or humanized tone; the formal voice appears well-matched to the target venue. The primary readability concerns were structural (paper length, inconsistent numbers, under-defined metrics) rather than stylistic.

---

## Consensus Strengths

1. **Timely and well-motivated problem.** All three reviewers agreed that the $10^3$–$10^6$ node "intermediate regime" is a genuine and important gap in the literature, directly relevant to Starlink, Kuiper, and OneWeb expansion trajectories. (Claude: "timely given the growth trajectories"; Gemini: "critical and rapidly emerging gap"; GPT: "genuinely important and under-quantified problem.")

2. **Rigorous simulation framework with strong reproducibility support.** All reviewers praised the detailed parameter table (Table II), Monte Carlo replication (50–100 runs), and validation against closed-form queueing and gossip bounds. (Claude: "parameter table supports reproducibility"; Gemini: "excellent job detailing simulation parameters"; GPT: "commendably explicit about many parameters.")

3. **Useful analytical decomposition of overhead.** The separation of "baseline telemetry" (topology-invariant) from "protocol overhead" (topology-dependent) was recognized by all reviewers as a smart methodological choice that isolates the architectural contribution from fixed costs. (Gemini: "smart analytical distinction"; GPT: "helpful normalization"; Claude acknowledged the approach but noted interpretability challenges.)

4. **Message decomposition diagnostic is a high-value contribution.** All reviewers highlighted the per-tier message decomposition figure as the paper's most effective diagnostic tool for explaining the superlinear transition mechanism. (Claude: "valuable diagnostic"; Gemini: "effectively isolates the driver of superlinear scaling"; GPT: "exactly the right diagnostic.")

5. **Transparent and commendable limitations disclosure.** All three reviewers noted that the authors were unusually forthcoming about the study's limitations, including the physical-layer abstraction, the analytical (non-simulated) nature of the optimizations, and the conditional nature of quantitative claims. (Claude: "commendably transparent"; Gemini acknowledged the acknowledgments; GPT: "limitations are acknowledged.")

6. **Appropriate ethical and AI-use disclosure.** All reviewers found the AI-assisted ideation acknowledgment to be in line with emerging transparency norms and praised the data availability statement.

---

## Consensus Weaknesses

1. **Analytically projected optimizations conflated with DES results.** All three reviewers identified this as a critical problem. The "optimized" curve in the scaling figure and the headline "8% at $10^6$ nodes" claim in the abstract are derived from analytical projections, not discrete event simulation, yet they are presented alongside and sometimes indistinguishable from simulated results. (Claude: "conflation of simulated and projected results is misleading"; Gemini: "methodological discontinuity…mixing pure DES results with analytical projections"; GPT: "must be visually and rhetorically separated from simulation outputs.")

2. **Global-state mesh baseline is a strawman.** All reviewers questioned the assumption that every node must maintain full trajectory state for all $O(N)$ peers, noting that operational conjunction assessment does not require this. The omission of a sectorized or partitioned mesh alternative—acknowledged by the authors themselves as a natural competitor—leaves a critical gap. (Claude: "straw man…sectorized mesh not simulated"; Gemini implicitly via the "Global State" clarification suggestion; GPT: "not generally necessary for safe operations…should either treat as intentionally extreme upper bound or include intermediate baseline.")

3. **Physical-layer abstraction is too aggressive for quantitative claims in a space-systems journal.** All reviewers flagged the absence of link intermittency, MAC contention, pointing/acquisition overhead, and Earth occlusion modeling. The authors' own estimate of 2–4× overhead increase from unmodeled effects was noted as potentially invalidating the headline results. The claim that these effects are "topology-neutral" was challenged by all three reviewers, with specific arguments that hierarchical systems are disproportionately vulnerable to coordinator link failures. (Claude: "could shift overhead from 8% to 16–32%"; Gemini: "link acquisition time and topology switching costs are non-trivial"; GPT: "neutrality claim is not established and is likely false.")

4. **Inconsistent overhead numbers across abstract, tables, and figures.** Claude and GPT both identified specific numerical inconsistencies (abstract claims 8% at $10^6$; Table "inflection" shows 10% at $5 \times 10^5$; Table "cluster_size" shows 4.8% at $10^6$ for $k_c=100$). GPT called this "a publication-blocking validity problem." Claude traced the discrepancy to the conflation of simulated and optimized results. Gemini did not flag this explicitly but noted the need to distinguish analytical from simulated data, which is the root cause.

5. **Centralized baseline comparison is structurally unfair.** Claude and GPT both noted that the centralized baseline uses $c=1$ (single server) while the hierarchical architecture is fully optimized, making the comparison asymmetric. The $M/D/c$ sensitivity analysis exists but is not carried through to the main comparison tables and figures. (Claude: "framing presents the comparison as if the three architectures are on equal footing"; GPT: "deliberately pessimistic configuration…must be consistently presented.")

6. **Key performance metrics are under-defined.** GPT explicitly flagged that "coordination success rate," "deadline," and "availability" are used in results but never operationally defined. Claude noted the "Status" column labels in Table V are subjective and undefined. Gemini implicitly raised this via the handoff reliability discussion. Without clear definitions, the duty-cycle and failure-resilience results are difficult to interpret or reproduce.

---

## Divergent Opinions

**Overall recommendation and severity assessment:**
- **Gemini 3 Pro** recommended **Minor Revision**, characterizing the paper as "high-quality" with issues that are primarily about clarification and separation of analytical vs. simulated results.
- **Claude Opus 4.6** recommended **Major Revision**, identifying five major issues including unfair baselines, missing sectorized mesh simulation, and insufficient statistical rigor for the superlinear transition claim.
- **GPT-5.2** recommended **Major Revision**, with six major issues centered on inconsistent numbers, under-defined metrics, and the strawman mesh baseline.

**Significance & Novelty:**
- **Gemini** rated this 5/5 (Excellent), viewing the systematic quantitative comparison and the specific superlinear transition identification as high-value contributions.
- **Claude** rated this 3/5 (Adequate), arguing the finding that hierarchical architectures scale better than flat ones is well-established and the contribution is primarily quantitative characterization under idealized conditions.
- **GPT** rated this 4/5 (Good), positioning the paper as a useful "reference scaling study under a declared parameterization" but noting limited novelty due to idealized assumptions.

**Statistical rigor of the superlinear transition:**
- **Claude** devoted significant attention to this, arguing that overlapping confidence intervals across adjacent data points and the unverifiable $R^2 > 0.99$ claim undermine the finding, and requested formal model comparison (AIC/BIC).
- **Gemini** and **GPT** did not raise this as a major concern, implicitly accepting the transition characterization as adequately supported.

**Scope and breadth of the paper:**
- **Claude** argued the paper is too broad ("three topologies, four-dimensional parameter sweep, three optimizations, four application domains") and recommended narrowing scope and deepening analysis.
- **Gemini** found the breadth appropriate and rated Scope & Referencing 5/5.
- **GPT** did not explicitly critique breadth but noted the applicability discussion could be better grounded.

**Coordinator bandwidth assumption:**
- **GPT** elevated this to a major issue, arguing that the shared-bandwidth model for coordinators ($k_c \times 1$ kbps) changes the meaning of "per-node bandwidth allocation" and could bias comparisons.
- **Claude** flagged it as a minor issue (should be formalized in Table II).
- **Gemini** flagged it as a minor issue (should be highlighted more prominently).

**Service-rate justification and U-shaped optimum causation:**
- **GPT** identified a logical inconsistency: the utilization math suggests $k_c=500$ gives $\rho=0.25$ (well below saturation), yet the text attributes the U-shape to saturation. GPT requested correction of the causal explanation and sensitivity sweeps.
- **Claude** and **Gemini** did not flag this specific inconsistency.

---

## Aggregated Ratings

Since all three reviewers reviewed only Version F, the table below reflects that single version. Columns for Version A and Version B are marked N/A where no review was provided.

| Criterion | Claude F | Claude (other) | Gemini F | Gemini (other) | GPT F | GPT (other) |
|-----------|----------|----------------|----------|----------------|-------|-------------|
| Significance & Novelty | 3 | N/A | 5 | N/A | 4 | N/A |
| Methodological Soundness | 2 | N/A | 4 | N/A | 3 | N/A |
| Validity & Logic | 3 | N/A | 4 | N/A | 3 | N/A |
| Clarity & Structure | 4 | N/A | 5 | N/A | 4 | N/A |
| Ethical Compliance | 4 | N/A | 5 | N/A | 4 | N/A |
| Scope & Referencing | 3 | N/A | 5 | N/A | 3 | N/A |
| **Mean across criteria** | **3.17** | — | **4.67** | — | **3.50** | — |

**Cross-reviewer means per criterion:**
| Criterion | Mean | Spread |
|-----------|------|--------|
| Significance & Novelty | 4.00 | 3–5 |
| Methodological Soundness | 3.00 | 2–4 |
| Validity & Logic | 3.33 | 3–4 |
| Clarity & Structure | 4.33 | 4–5 |
| Ethical Compliance | 4.33 | 4–5 |
| Scope & Referencing | 3.67 | 3–5 |

---

## Priority Action Items

### 1. Reconcile all overhead numbers and separate simulated from projected results
**Flagged by:** All three reviewers (Claude, Gemini, GPT)
**Applies to:** Both versions

This is the single most critical fix. The abstract's "2% at $10^3$ to 8% at $10^6$" claim must be reconciled with Table "inflection" (10% at $5 \times 10^5$) and Table "cluster_size" (4.8% at $10^6$). Create a comprehensive traffic-accounting table specifying exactly which message types are included in each reported result. All figures and tables must clearly label whether data points are DES-simulated or analytically projected (e.g., separate figure panels, dashed vs. solid lines with explicit legend entries). The abstract and conclusions must report only DES-verified results, with projections clearly qualified.

### 2. Implement at least one optimization in the DES
**Flagged by:** All three reviewers
**Applies to:** Both versions

Exception-based telemetry is the simplest candidate: replace periodic reporting with threshold-triggered reporting and run at least one scale point ($N = 10^4$ or $10^5$) to validate the analytical projection. If the DES result aligns with the projection, the analytical curve gains credibility. If not, that discrepancy is itself an important finding. This single implementation would transform the paper's most contested claim into an empirically grounded one.

### 3. Add a stochastic link availability model
**Flagged by:** All three reviewers
**Applies to:** Both versions

Even a simple Bernoulli on/off model per link (e.g., 50% duty cycle representing Earth occlusion, or a parameter sweep from 40–80%) would dramatically strengthen the paper's quantitative claims. Critically, this would test the contested "topology-neutral" assertion: if hierarchical coordinator links experience outages, queue buildup and missed coordination cycles may disproportionately degrade hierarchical performance relative to mesh. Report whether the topology ranking is preserved under intermittent links.

### 4. Strengthen the centralized baseline and mesh baseline comparisons
**Flagged by:** Claude (major), GPT (major), Gemini (implicit)
**Applies to:** Both versions

For the centralized baseline: carry the $M/D/c$ analysis at $c = 10$ and $c = 100$ through to all main comparison tables and figures, not just the sensitivity table. For the mesh baseline: either (a) simulate a sectorized/partitioned mesh as a fourth topology, or (b) explicitly and prominently frame the global-state mesh as an intentional upper bound throughout the paper (not just in limitations), and substantially qualify all claims about hierarchical superiority over "decentralized" approaches.

### 5. Formally define all performance metrics
**Flagged by:** GPT (major), Claude (minor), Gemini (implicit)
**Applies to:** Both versions

Provide operational definitions for: coordination cycle period, per-event-type deadlines (routine status vs. collision alert), what constitutes a "coordination success" vs. failure, how "availability" is computed, and the handoff failure model (bit error, link outage, pointing failure). The "Status" column in Table V should either be defined against quantitative thresholds or removed.

### 6. Apply formal statistical testing to the superlinear transition claim
**Flagged by:** Claude (major)
**Applies to:** Both versions

Fit linear, power-law ($aN^b$), and piecewise-linear models to the overhead data across the 10,000–100,000 node range. Report AIC/BIC values, confidence intervals on the breakpoint location, and formal hypothesis tests comparing models. Address the overlapping confidence intervals at adjacent data points. This is the paper's most specific empirical contribution and deserves rigorous statistical support.

### 7. Justify or sensitivity-sweep coordinator service rates and correct the U-shaped optimum causal explanation
**Flagged by:** GPT (major), Claude (minor)
**Applies to:** Both versions

The claimed saturation-driven U-shape is inconsistent with the utilization math ($\rho = 0.25$ at $k_c = 500$). Either correct the causal explanation (identifying the actual dominant mechanism—handoff state size, inter-cluster traffic, etc.) or provide sensitivity sweeps over $C_{\text{cluster}}$, message sizes, and handoff state scaling to demonstrate that the 50–100 optimum is robust to parameter choices.

---

## Overall Assessment

The paper addresses a timely and important problem—scaling coordination architectures for autonomous space swarms from $10^3$ to $10^6$ nodes—and provides a well-structured discrete event simulation study with commendable transparency about its limitations. The simulation framework, parameter documentation, and message decomposition analysis are genuine strengths. The writing quality and organization are strong and appropriate for IEEE T-AES.

However, the paper has several publication-blocking issues that prevent acceptance in its current form. The most critical are: (1) internal inconsistencies in the headline overhead numbers, (2) conflation of DES-simulated results with analytically projected optimizations, (3) structurally unfair baseline comparisons (single-server centralized, full-dissemination mesh) that overstate the hierarchical architecture's advantages, and (4) absence of any physical-layer realism (link intermittency, MAC contention) despite the authors' own acknowledgment that unmodeled effects could increase overhead by 2–4×. Two of three reviewers recommended **Major Revision**; the third recommended Minor Revision but identified overlapping concerns.

The consensus recommendation is **Major Revision**. The seven priority action items above are ordered by impact and feasibility. Items 1, 2, and 5 are primarily editorial and analytical work; items 3, 4, 6, and 7 require additional simulation runs or statistical analysis. Addressing all seven would transform the paper from a promising but contested preliminary study into a robust, citable scaling reference for the space systems community.

Since only Version F was reviewed, no version preference can be established. The authors should proceed with revisions on the formal academic version, which was well-received stylistically by all three reviewers.