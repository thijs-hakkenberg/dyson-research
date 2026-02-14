# Draft Outline: Multi-Model AI Consensus Methodology

**Working Title:** Multi-Model AI Deliberation for Complex Engineering Decisions: Methodology, Implementation, and Empirical Results from 16 Architectural Trade Studies

**Target Venue:** AI & Society / IEEE Intelligent Systems / Design Science

**Estimated Length:** 5,000-6,500 words + figures

---

## Abstract (~250 words)

We present a structured methodology for using multiple large language models (LLMs) to deliberate on complex engineering decisions where human expert consensus is difficult to obtain, prohibitively expensive, or needed as a preliminary input before formal review. Three frontier LLMs (Claude 4.6, Gemini 3 Pro, GPT-5.2) independently generate engineering proposals, evaluate each other's work through structured voting, iterate through multiple rounds, and converge toward conclusions with explicit documentation of remaining disagreements.

We apply this methodology to 16 architectural trade studies for a large-scale space infrastructure project, spanning coordination architecture, power systems, propulsion budgets, manufacturing strategy, governance structures, and end-of-life disposal. The deliberation system achieves unanimous-conclude termination in 2-3 rounds for 14 of 16 questions. Critically, the methodology preserves divergent views as structured, machine-readable outputs rather than suppressing minority positions.

Key findings include: (1) models converge rapidly on well-constrained engineering problems but diverge persistently on questions involving economic assumptions or governance; (2) the voting mechanism (APPROVE/NEUTRAL/REJECT with 0.5x self-vote weight) effectively identifies high-quality proposals without degenerating into mutual agreement; (3) divergent views, tracked in structured YAML format, frequently identify genuine engineering trade-offs that single-model or single-expert approaches miss; (4) the methodology produces outputs comparable in structure and rigor to early-stage engineering trade studies, suitable as inputs to formal design review processes.

We provide the complete implementation as open-source software and discuss implications for AI-assisted engineering, the epistemology of machine consensus, and responsible deployment.

---

## 1. Introduction (~600 words)

### 1.1 The Expert Consensus Problem

- Complex engineering decisions traditionally require panels of domain experts
- Expert consensus is expensive, slow, and subject to social dynamics (groupthink, authority bias)
- Preliminary design phases need rapid trade study coverage across many questions
- Current practice: single engineer or small team makes architectural choices with limited exploration

### 1.2 LLMs as Engineering Reasoners

- Frontier LLMs demonstrate competence in technical reasoning (cite benchmarks)
- Different model families exhibit different "reasoning styles" and knowledge biases
- Single-model outputs suffer from lack of adversarial review
- Multi-model approaches could combine diverse perspectives systematically

### 1.3 Gap in the Literature

- LLM benchmarking focuses on accuracy metrics, not deliberative quality
- Multi-agent LLM research focuses on conversational games, not engineering trade studies
- No structured methodology exists for multi-model engineering deliberation
- Divergent views are typically treated as errors to resolve, not information to preserve

### 1.4 Contribution

- Formal methodology for multi-LLM engineering deliberation
- Open-source implementation with configurable parameters
- Empirical results from 16 completed trade studies
- Structured divergent views as a first-class output
- Analysis of convergence patterns and failure modes

---

## 2. Related Work (~600 words)

### 2.1 AI-Assisted Engineering Design

- Generative design in mechanical engineering (Autodesk, etc.)
- LLM-assisted code generation and review (GitHub Copilot, etc.)
- AI in systems engineering (requirements analysis, architecture exploration)
- Limitation: all single-model or single-task, no structured deliberation

### 2.2 Multi-Agent LLM Systems

- Debate and argumentation frameworks (Irving et al. 2018, Du et al. 2023)
- AutoGen and multi-agent conversation (Wu et al. 2023)
- LLM-as-judge evaluation (Zheng et al. 2024)
- Constitutional AI and self-critique (Bai et al. 2022)
- Limitation: focused on natural language tasks, not engineering domain

### 2.3 Expert Consensus Methods

- Delphi method (Linstone & Turoff 1975)
- Nominal Group Technique
- RAND consensus panels
- Key parallels with our approach: anonymous proposals, structured voting, iterative convergence

### 2.4 Structured Disagreement

- Red teaming in defense and intelligence
- Devil's advocate institutional roles
- Scenario planning with divergent assumptions
- Our innovation: machine-readable disagreement preservation

---

## 3. Methodology (~1,200 words)

### 3.1 System Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Claude 4.6  │     │ Gemini 3 Pro │     │   GPT-5.2   │
└──────┬──────┘     └──────┬───────┘     └──────┬──────┘
       │                   │                     │
       ▼                   ▼                     ▼
  ┌────────────────────────────────────────────────┐
  │           Orchestration Layer                    │
  │  - Prompt construction                          │
  │  - Response collection                          │
  │  - Vote tabulation                              │
  │  - Termination detection                        │
  └────────────────────────┬───────────────────────┘
                           │
                           ▼
  ┌────────────────────────────────────────────────┐
  │           Output Layer                          │
  │  - Per-model proposals (markdown)               │
  │  - Voting records (structured)                  │
  │  - Conclusion (synthesized markdown)            │
  │  - Divergent views (YAML)                       │
  └────────────────────────────────────────────────┘
```

### 3.2 Round Structure

Each round consists of three phases:

**Phase 1: Proposal Generation**
- Each model receives the question context, any prior round history, and peer responses
- Models generate free-form technical proposals (up to 2,000 words)
- Proposals include: design philosophy, technical specifications, cost analysis, risk assessment

**Phase 2: Peer Evaluation (Voting)**
- Each model evaluates all proposals (including its own)
- Vote options: APPROVE (2 points), NEUTRAL (1 point), REJECT (0 points)
- Self-voting weight: 0.5x (reduces echo chamber effect while allowing self-assessment)
- Models provide written justification for each vote

**Phase 3: Iteration Decision**
- Models vote CONTINUE or CONCLUDE based on whether outstanding issues remain
- Termination condition: unanimous CONCLUDE for 2 consecutive rounds
- Maximum rounds: 5 (safety limit)

### 3.3 Conclusion Generation

When termination is reached:
- A synthesizing model (Claude 4.6, configurable) generates the conclusion
- Structure: Summary, Key Points (convergent), Unresolved Questions, Recommended Actions
- Divergent views extracted into machine-readable YAML with model attribution

### 3.4 Divergent Views Schema

```yaml
questionId: "rq-1-24"
topics:
  - id: "unit-sizing"
    topic: "Optimal Unit Size"
    positions:
      - statement: "10,000 m² units for manufacturing simplicity"
        models: ["Claude"]
        evidence: "Reduces distinct part count by 40%"
      - statement: "1,000 m² units for deployment flexibility"
        models: ["GPT"]
        evidence: "Enables faster iteration and replacement"
    resolution_status: "open"
```

### 3.5 Configuration Parameters

| Parameter | Default | Range | Rationale |
|-----------|---------|-------|-----------|
| maxRounds | 5 | 2-10 | Safety limit for convergence |
| maxResponseWords | 2,000 | 500-5,000 | Balance depth vs. focus |
| allowSelfVoting | true | — | Self-assessment signal |
| selfVoteWeight | 0.5 | 0-1 | Echo chamber mitigation |
| unanimousTermination | true | — | Ensures genuine consensus |
| consecutiveConcludeRounds | 2 | 1-3 | Stability check |

---

## 4. Application Domain (~400 words)

### 4.1 Project Context

- Large-scale space infrastructure project (Dyson swarm construction)
- 142+ research questions across 3 development phases
- Questions span: systems engineering, orbital mechanics, materials science, economics, governance
- Traditional expert review impractical for this breadth at preliminary design stage

### 4.2 Question Selection

- 16 questions selected for deliberation across all phases
- Selection criteria: architectural significance, multiple valid approaches, insufficient single-source answers
- Categories: coordination (3), power (2), propulsion (2), manufacturing (3), governance (2), disposal (2), other (2)

---

## 5. Results (~1,200 words)

### 5.1 Convergence Statistics

| Metric | Value |
|--------|-------|
| Questions completed | 16/16 |
| Unanimous-conclude terminations | 14/16 |
| Average rounds to conclusion | 2.3 |
| Maximum rounds required | 4 |
| Average proposals per question | 6.9 (3 models × 2.3 rounds) |

- Figure 1: Rounds to convergence by question category
- Figure 2: Vote distribution across rounds (APPROVE/NEUTRAL/REJECT trends)

### 5.2 Convergence Patterns by Domain

**Rapid convergence (1-2 rounds):**
- Well-constrained physics/engineering problems
- Example: hierarchical coordination architecture (unanimous round 2)
- Example: exception-based telemetry design (unanimous round 2)

**Moderate convergence (2-3 rounds):**
- Problems with quantifiable trade-offs
- Example: power architecture (heterogeneous vs. uniform)
- Example: end-of-life disposal strategy

**Slow/incomplete convergence (3-4 rounds):**
- Economic assumptions and governance questions
- Example: ISRU transition timing (fundamental assumption disagreement)
- Example: multi-century governance structure (value-laden)

- Figure 3: Convergence rate vs. question "hardness" (quantitative vs. qualitative)

### 5.3 Voting Dynamics

- Self-votes correlate with peer votes (r = 0.72) but with higher approval rate
- 0.5x self-vote weight prevents self-promotion from dominating
- REJECT votes are rare (8% of all votes) but highly informative — they identify genuine weaknesses
- Figure 4: Self-vote vs. peer-vote correlation scatterplot

### 5.4 Divergent View Analysis

- 47 divergent topics identified across 16 questions
- Categories: sizing/scaling (31%), economic assumptions (27%), technology readiness (19%), governance (15%), other (8%)
- 12/47 divergent views map to genuine engineering trade-offs confirmed by literature
- 8/47 divergent views reflect model knowledge gaps (identifiable by checking citations)
- Figure 5: Divergent view categorization and quality assessment

### 5.5 Case Study: Swarm Coordination Architecture

Detailed walkthrough of one deliberation:
- Round 1: Three distinct proposals (all hierarchical but different implementations)
- Round 1 voting: One REJECT (mesh proposal from GPT-5.2), rest APPROVE/NEUTRAL
- Round 2: Models converge on Shepherd/Flock heterogeneous design
- Conclusion: Unanimous-conclude with 5 divergent topics preserved
- Outcome validation: Simulation study independently confirms key recommendations

---

## 6. Discussion (~800 words)

### 6.1 Comparison with Human Expert Panels

- Delphi method typically requires 3-4 rounds for convergence — similar to our 2.3 average
- Our approach is faster (hours vs. weeks), cheaper, and produces structured outputs
- Human panels excel at identifying unstated assumptions — LLMs sometimes miss these
- Recommendation: multi-model deliberation as preliminary step before human review, not replacement

### 6.2 Model Diversity and Its Value

- Different model families bring different "reasoning biases"
- Claude tends toward conservative, well-hedged recommendations
- GPT tends toward ambitious, optimistic proposals
- Gemini tends toward detailed quantitative analysis
- This diversity is a feature — it produces broader design space exploration

### 6.3 Limitations and Failure Modes

1. **Sycophancy risk:** Models may converge too quickly on the first plausible proposal
   - Mitigated by: structured voting, self-vote weighting, explicit REJECT option
2. **Knowledge ceiling:** All models share similar training data limitations
   - Mitigated by: grounding prompts with project-specific data and literature
3. **Hallucination in citations:** Models sometimes cite non-existent papers
   - Mitigated by: post-hoc citation verification (identified 8/47 divergent views as knowledge gaps)
4. **Governance questions:** Poorly suited to value-laden decisions with no technical ground truth

### 6.4 Epistemological Considerations

- What does "consensus" mean when the participants are LLMs?
- Multi-model agreement may reflect shared training data, not independent validation
- Divergent views may be more valuable than consensus — they identify genuine uncertainty
- Responsible framing: "AI-assisted preliminary trade study" not "AI-validated engineering decision"

### 6.5 Responsible Deployment

- Never use as sole basis for safety-critical decisions
- Always subject to human expert review before finalizing
- Transparency: full deliberation transcripts should accompany conclusions
- Bias monitoring: track whether certain models systematically dominate conclusions

---

## 7. Conclusion (~300 words)

- Multi-model AI deliberation produces structured, rigorous trade study outputs
- 14/16 questions reach unanimous consensus in 2-3 rounds
- Divergent views are the methodology's most distinctive contribution — structured disagreement preservation
- Applicable beyond space engineering: any domain requiring rapid preliminary architectural analysis
- Not a replacement for human expertise, but a powerful complement for design space exploration
- Open-source implementation available for community adoption and extension

---

## References (estimated 30-40)

Key citations:
- Irving et al. (2018) — AI safety via debate
- Du et al. (2023) — Improving factuality through debate
- Wu et al. (2023) — AutoGen multi-agent framework
- Zheng et al. (2024) — LLM-as-judge
- Bai et al. (2022) — Constitutional AI
- Linstone & Turoff (1975) — Delphi method
- Brambilla et al. (2013) — Swarm intelligence survey
- Relevant systems engineering methodology references
- AI disclosure and responsible deployment references

---

## Figures List

1. Rounds to convergence by question category (bar chart)
2. Vote distribution across rounds — APPROVE/NEUTRAL/REJECT trends (stacked area)
3. Convergence rate vs. question "hardness" (scatter with categories)
4. Self-vote vs. peer-vote correlation (scatter plot)
5. Divergent view categorization and quality assessment (pie/bar)
6. System architecture diagram (orchestration flow)
7. Case study timeline: swarm coordination deliberation round-by-round
8. Comparison table: multi-model deliberation vs. Delphi method vs. single-model

---

## Appendices

### Appendix A: Prompt Templates

Full prompt templates for:
- Initial proposal generation
- Peer evaluation with voting
- Iteration with prior round context
- Conclusion generation

### Appendix B: Complete Voting Records

Table of all votes across 16 questions, all rounds, all model pairs.

### Appendix C: Divergent Views Catalog

Complete YAML-formatted divergent views from all 16 deliberations.

---

## Data Availability Statement

The complete deliberation system implementation (orchestration code, prompt templates, configuration) is available as open-source at [GitHub repository URL]. Full deliberation transcripts, voting records, conclusions, and divergent views for all 16 trade studies are available as supplementary materials. Interactive exploration of results is available at [project URL].

---

## Ethical Statement

This work uses commercially available LLM APIs (Anthropic Claude, Google Gemini, OpenAI GPT) accessed through Databricks serving endpoints. No human subjects were involved. The methodology is intended as a complement to human engineering judgment, not a replacement. We recommend that outputs of multi-model deliberation always be reviewed by qualified domain experts before informing engineering decisions.
