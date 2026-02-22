# Development Plan: Paper 03 — Multi-Model AI Consensus Methodology

**Working Title:** Multi-Model AI Deliberation for Complex Engineering Decisions: Methodology, Implementation, and Empirical Results from 16 Architectural Trade Studies

**Target Venue:** AI & Society / IEEE Intelligent Systems / Design Science

**Methodology:** Iterative AI peer review (Claude/Gemini/GPT), following the Paper 01 process

---

## Current State Assessment

### What Already Exists

1. **Detailed outline** (`03-multi-model-ai-consensus.md`) — 362 lines covering abstract through ethical statement, 8 figures planned, 7 sections + 3 appendices
2. **LaTeX + PDF draft** — initial compilation exists
3. **Orchestration implementation** (`scripts/run-discussion.js`) — fully functional multi-model deliberation engine:
   - Proposal generation with context injection
   - Structured voting (APPROVE/NEUTRAL/REJECT) with 0.5x self-vote weight
   - Termination detection (unanimous CONCLUDE for 2 consecutive rounds)
   - Conclusion synthesis with divergent views extraction
4. **16 completed deliberations** (14 discussion-type + 2 resolved via other means):
   - Phase 0: rq-0-14 (propellant scope), rq-0-18 (human rating), rq-0-28 (cost methodology), rq-0-29 (governance)
   - Phase 1: rq-1-11 (power architecture), rq-1-16 (autonomy certification), rq-1-21 (feedstock timeline), rq-1-33 (tug disposal), rq-1-40 (slot governance), rq-1-42 (node disposal)
   - Phase 2: rq-2-3 (collision avoidance), rq-2-8 (repair authority), rq-2-20 (swarm ROI)
   - Phase 3a: rq-3a-3 (inter-layer consensus)
5. **Discussion transcripts** — full round-by-round records for each deliberation
6. **Divergent views** — structured YAML for each question with model attribution
7. **2 methodology blog posts** documenting the approach
8. **Publication assessment** rating this as "Tier 1 — immediately publication-ready"

### Unique Advantage

Unlike Papers 01 and 02 (which require new simulation code), Paper 03's primary data already exists. The 16 deliberation transcripts, voting records, and divergent views are the empirical dataset. The paper is fundamentally an **analysis of existing data** plus **methodology documentation**.

### What Needs to Be Built

1. **Quantitative analysis code** — Python scripts to compute convergence statistics, voting dynamics, divergent view categorization
2. **Figure generation pipeline** — all 8 publication figures from deliberation data
3. **Full LaTeX paper** — formatted for target venue
4. **Citation verification** — especially for multi-agent LLM literature (fast-moving field)
5. **Iterative peer review cycle** — Version A through acceptance

---

## Development Phases

### Phase 1: Data Extraction and Analysis

**Goal:** Extract structured data from all 16 deliberation transcripts for quantitative analysis

#### 1a. Transcript Data Extraction (`deliberation_analysis.py`)
- Parse all 16 deliberation transcripts
- Extract per-round: proposals, votes (with self-vote flag), justifications, CONTINUE/CONCLUDE votes
- Output: structured JSON/CSV dataset

Fields per deliberation:
```
question_id, round_number, model_id, proposal_word_count,
vote_target, vote_value (APPROVE=2/NEUTRAL=1/REJECT=0),
is_self_vote, justification_length, conclude_vote (bool)
```

#### 1b. Convergence Analysis
- Rounds to convergence per question
- Convergence rate by question category (well-constrained physics vs. economic vs. governance)
- Terminal state: unanimous-conclude vs. max-rounds
- Bootstrap 95% CI on mean rounds to convergence

#### 1c. Voting Dynamics Analysis
- Self-vote vs. peer-vote correlation (Pearson r)
- APPROVE/NEUTRAL/REJECT distribution across rounds (does rejection decrease over time?)
- Per-model voting tendencies (is one model systematically more/less critical?)
- Effect of 0.5x self-vote weight on outcome ranking

#### 1d. Divergent View Analysis
- Parse all divergent-views.yaml files
- Categorize: sizing/scaling, economic assumptions, technology readiness, governance, other
- Cross-reference with literature to identify genuine trade-offs vs. knowledge gaps
- Quality assessment: which divergent views proved informative for downstream decisions?

**Estimated effort:** 2–3 days

### Phase 2: Figure Generation Pipeline

**Goal:** `generate_consensus_figures.py` producing all 8 figures

| Figure | Description | Data Source |
|--------|-------------|-------------|
| Fig 1 | Rounds to convergence by question category | Convergence analysis |
| Fig 2 | Vote distribution across rounds (stacked area) | Voting records |
| Fig 3 | Convergence rate vs. question "hardness" (scatter) | Category + rounds data |
| Fig 4 | Self-vote vs. peer-vote correlation (scatter) | Voting records |
| Fig 5 | Divergent view categorization (pie/bar) | DV analysis |
| Fig 6 | System architecture diagram | Static (matplotlib/tikz) |
| Fig 7 | Case study timeline: swarm coordination deliberation | Single deliberation trace |
| Fig 8 | Comparison: multi-model vs. Delphi vs. single-model | Summary table/chart |

**Estimated effort:** 2 days

### Phase 3: LaTeX Paper — Version A

**Goal:** Complete first draft with all sections, figures, tables, and bibliography

#### Section-by-section plan:

1. **Abstract** (250 words) — derived from actual analysis results, not placeholder values
2. **Introduction** (600 words) — the expert consensus problem, LLMs as engineering reasoners, gap in literature, contribution
3. **Related Work** (600 words) — verify all citations:
   - Irving et al. 2018 — AI safety via debate — VERIFY
   - Du et al. 2023 — Improving factuality through debate — VERIFY
   - Wu et al. 2023 — AutoGen — VERIFY
   - Zheng et al. 2024 — LLM-as-judge — VERIFY
   - Bai et al. 2022 — Constitutional AI — VERIFY
   - Linstone & Turoff 1975 — Delphi method — VERIFY (this is a book, cite properly)
   - **Add recent 2025–2026 multi-agent LLM papers** (field is evolving rapidly)
4. **Methodology** (1,200 words) — system architecture, round structure, conclusion generation, DV schema, configuration parameters
5. **Results** (1,200 words) — convergence statistics, voting dynamics, divergent view analysis, case study
6. **Discussion** (800 words) — comparison with human panels, model diversity value, limitations, epistemology, responsible deployment
7. **Conclusion** (300 words)
8. **Appendices:** prompt templates, voting records, DV catalog

**Key requirement:** The paper must be transparent about what "consensus" means for LLMs vs. human experts. Epistemological section is critical for credibility.

**Estimated effort:** 3–4 days

### Phase 4: Iterative AI Peer Review

**Goal:** Achieve 3/3 Accept

#### Expected Review Concerns:
- **Epistemological objections:** "LLM agreement doesn't constitute consensus" — must address head-on in Discussion §6.4
- **Training data overlap:** "Models may agree because they share training data" — acknowledge as limitation, argue diversity is still informative
- **Domain specificity:** "Results may not generalize beyond space engineering" — discuss applicability, recommend replication studies
- **Sycophancy risk:** "Models may just agree with each other" — present 0.5x self-vote weight analysis, REJECT vote frequency as counter-evidence
- **N=16 sample size:** "Too few deliberations for statistical claims" — acknowledge, present as proof-of-concept with effect sizes
- **Missing human baseline:** "No comparison with actual expert panel" — acknowledge, propose as future work

#### Estimated Timeline:
- Versions A–D: Major structural changes, epistemological framing (2 weeks)
- Versions E–L: Statistical rigor, additional analyses per reviewer requests (2–3 weeks)
- Versions M–T: Presentation refinement, citation updates (2 weeks)
- Versions U+: Final convergence (1–2 weeks)

**Total estimated: 7–10 weeks** (may be faster than Paper 01 since methodology is more contained)

### Phase 5: Publication Package

```
publications/papers/03-multi-model-ai-consensus/
├── 03-multi-model-ai-consensus-XX.pdf → (symlink)
├── 03-multi-model-ai-consensus-XX.tex → (symlink)
├── CHANGELOG.md → (symlink)
├── code → ../../scripts (or dedicated analysis scripts)
├── data/ → deliberation transcripts, voting records, DVs
└── figures → (symlink)
```

---

## Key Technical Decisions

### 1. What Counts as a "Deliberation"
**Decision:** Include all 14 questions with `questionType: "discussion"` that went through the full orchestrated process. Exclude rq-1-12 (ISRU transition, simulation-based) and other non-discussion questions, even though they involved multi-model input during consensus synthesis.

### 2. How to Handle the Self-Referential Nature
This paper describes a multi-model AI methodology and will itself be reviewed by the same multi-model AI process. **Decision:** Acknowledge this explicitly in the paper as a form of "meta-validation" — the methodology is being applied to evaluate itself. Frame as a feature (the process is self-consistent) while acknowledging the circularity.

### 3. Code Availability
**Decision:** Release the orchestration code (`run-discussion.js`) as the primary artifact. The analysis scripts (`deliberation_analysis.py`, `generate_consensus_figures.py`) are secondary. Include full deliberation transcripts as supplementary data.

### 4. Ethical Framing
**Decision:** Include a dedicated Ethical Statement (already in outline). Frame as "AI-assisted preliminary trade study," explicitly NOT as "AI-validated engineering decision." Reference responsible AI deployment guidelines.

### 5. Venue Selection
**Decision:** Target IEEE Intelligent Systems first (broader AI audience, good fit for methodology papers). Fallback: AI & Society (more epistemological focus) or Design Science (engineering methodology focus).

---

## Dependencies and Risks

| Risk | Mitigation |
|------|-----------|
| Epistemological objections may be hard to fully address | Consult philosophy of science literature on machine epistemology; frame claims carefully |
| Multi-agent LLM literature is evolving fast | Do thorough arXiv search right before Version A submission; update citations during review |
| N=16 may be considered too small | Emphasize qualitative richness of each deliberation; present as methodology paper with proof-of-concept results |
| Self-referential review process may draw criticism | Address head-on; show that the process produces useful engineering outputs regardless of epistemological status |
| Deliberation transcripts may contain errors or hallucinations | Audit all 16 transcripts for factual claims before citing |

---

## Success Criteria

1. Analysis code produces all statistics and figures reproducibly
2. Paper achieves 3/3 Accept from AI peer reviewers
3. Epistemological section is rigorous and addresses obvious objections
4. All 16 deliberation case studies are accurately represented
5. Divergent views are shown to be genuinely informative (not just noise)
6. Methodology is described with enough detail for independent replication
