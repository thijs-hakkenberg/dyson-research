---
paper: "03-multi-model-ai-consensus"
version: "h"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-23"
recommendation: "Major Revision"
---

**Review for IEEE Intelligent Systems**

**Manuscript Title:** Multi-Model AI Deliberation for Complex Engineering Decisions: A Structured Methodology with Divergent View Preservation
**Version:** H

---

### Review Criteria

**1. Significance & Novelty**
**Rating: 4/5**
The manuscript addresses a critical and timely gap in the literature: moving multi-agent LLM systems from conversational games or simple factual benchmarks toward complex, open-ended engineering reasoning. The core contribution—the "Divergent Views Schema"—is conceptually significant. By treating disagreement as a first-class artifact (epistemic uncertainty) rather than noise to be averaged out, the authors align AI outputs with the reality of engineering trade studies. This represents a meaningful advance over standard "Chain of Thought" or simple voting ensembles. The application to a specific domain (space infrastructure) provides necessary grounding, though the methodology is clearly transferable.

**2. Methodological Soundness**
**Rating: 3/5**
The system architecture and the deliberation protocol (rounds, voting, termination) are well-defined and reproducible. The choice of three distinct model families (Claude, Gemini, GPT) is appropriate for ensuring diversity. However, the experimental validation has weaknesses that the authors themselves acknowledge in Section 6.4. The baseline comparisons are confounded by prompt structure differences, making it difficult to isolate the benefit of the deliberation mechanism versus the benefit of simply having a better prompt or more compute. The reliance on a "Validation Roadmap" (listing experiments *to be done*) rather than performing those experiments is a significant weakness for a journal of this caliber.

**3. Validity & Logic**
**Rating: 3/5**
The qualitative analysis of the "Divergent Views" is rigorous and insightful. The identification of 12 confirmed engineering trade-offs validates the system's utility. However, the quantitative claims regarding sycophancy (Section 5.6) are based on a very small sample size ($n=6$ multi-round deliberations). While the finding that semantic similarity *decreases* is counter-intuitive and fascinating, the statistical power is low. Furthermore, the decision to reveal the "winner" of the previous round to the models in subsequent rounds introduces a strong anchoring bias that complicates the interpretation of convergence.

**4. Clarity & Structure**
**Rating: 5/5**
The manuscript is exceptionally well-written. The distinction between the Model, Orchestration, and Output layers is clear. The inclusion of code snippets (YAML schema) and specific prompt strategies (head truncation) aids reproducibility. The limitations section is refreshingly honest and detailed, anticipating many potential critiques.

**5. Ethical Compliance**
**Rating: 5/5**
The authors provide a model Ethics Statement. The disclosure of AI assistance in writing is precise. More importantly, the discussion regarding the risk of "false authority" in AI-generated trade studies is nuanced and responsible. The open-sourcing of the artifacts supports transparency.

**6. Scope & Referencing**
**Rating: 5/5**
The paper fits well within the scope of *IEEE Intelligent Systems*, bridging AI methodology with systems engineering. The literature review is robust, correctly identifying the roots of this work in the Delphi method, design rationale (QOC/DRL), and recent multi-agent LLM literature.

---

### Major Issues

**1. "Validation Roadmap" vs. Actual Validation**
Section 6.4 outlines four necessary experiments (Aggregation w/o deliberation, Self-refinement, Blind deliberation, Repeated trials) but treats them as future work. For a methodology paper, at least one of these controlled experiments is necessary *now* to prove the method's efficacy over simpler baselines. Specifically, **Experiment 3 (Blind Deliberation)** is critical. Without it, we cannot know if the convergence observed is due to genuine consensus or simply the models anchoring on the "winner" revealed in the prompt. The authors must execute a version of this ablation to disentangle anchoring from reasoning.

**2. Confounded Baselines**
In Section 5.5, the authors admit the baselines are confounded by prompt structure. Comparing a deliberation process to a single-shot synthesis that *lacks* the voting data is an unfair comparison. A stronger baseline would be "Parallel Generation + Synthesis," where the synthesizer sees all three independent proposals (and perhaps simulated votes) but the models never interact. The current comparison does not sufficiently isolate the value of the *iterative* component.

**3. Sample Size for Similarity Analysis**
The claim in Section 5.6 that "all metrics decrease" across rounds is a strong counter-evidence to the sycophancy hypothesis. However, this analysis is performed on only the subset of questions that went to multiple rounds ($n=6$). Drawing broad conclusions about model behavior from six data points is statistically precarious. The authors should either expand the dataset (run more questions) or significantly soften the statistical claims, framing them as preliminary observations.

---

### Minor Issues

*   **Section 3.2 (Head Truncation):** Truncating the tail of the previous proposal to fit context windows is a risky design choice. In engineering proposals, the "conclusion" or "recommendation" often appears at the end. Truncating this might force models to evaluate incomplete arguments. A summary-based approach or "Introduction + Conclusion" extraction would be safer.
*   **Section 3.2 (Self-Vote Weighting):** The choice of $0.5$ weighting for self-votes is heuristic. While the sensitivity analysis (Table 5) is helpful, the paper would benefit from a brief justification of why $0.5$ was chosen over $0.0$ (disallowing self-votes entirely), which is standard in many human peer-review processes.
*   **Section 5.3 (Inter-rater Reliability):** The paper mentions 81% agreement among reviewers but does not specify who the reviewers were (authors vs. independent experts). If they were the authors, this introduces confirmation bias.
*   **Figure 5:** The text references "JSON parsing failures" for Gemini. It would be valuable to know if these failures were random or correlated with specific types of complex engineering arguments.
*   **Typos/Formatting:**
    *   Section 2: "Chan et al. [12] proposed ChatEval..." - Ensure citation numbering aligns with the final bibliography order.
    *   Table 4: "Tech parameter Jaccard" - Define exactly how parameters were extracted (regex? LLM extraction?) in the table caption or text.

---

### Overall Recommendation

**Major Revision**

The paper presents a high-quality system and a novel conceptual contribution (the Divergent Views Schema). However, it currently reads like a "System Description" paper that stops short of the necessary empirical validation. The admission that the baselines are confounded and the proposal of a "Validation Roadmap" instead of actual results is the primary barrier to publication.

To warrant acceptance, the authors must move at least one of the proposed "Roadmap" experiments (ideally the Blind/Winner-Hidden ablation) from "future work" into the "Results" section. This is necessary to substantiate the claims that the multi-model dynamic adds value beyond simple aggregation.

---

### Constructive Suggestions

1.  **Execute the "Blind Deliberation" Ablation:** Run a subset of the questions where the "Winner Identity" is hidden from the models in Round 2. Compare the convergence rate and similarity metrics to the standard protocol. This will definitively answer the "anchoring vs. consensus" question.
2.  **Formalize the Divergent Views Schema:** The schema is the paper's strongest theoretical contribution. Consider elevating it. Create a formal definition or ontology for it, rather than just showing a YAML snippet. Discuss how this schema maps to the DRL (Design Rationale Language) or IBIS (Issue-Based Information Systems) frameworks mentioned in Related Work.
3.  **Strengthen the Baseline:** Rerun the "Aggregation-only" baseline using a prompt that is as structurally identical as possible to the Deliberation prompt (requesting the same sections). This removes the confounding variable and allows for a fair comparison of content quality.
4.  **Qualitative "Win" Examples:** Provide a specific example where a model changed its mind (switched from Position A to Position B) based on a specific piece of evidence provided by another model. This "evidence transfer" is the holy grail of deliberation; showing it happens (even once) is more persuasive than aggregate voting stats.