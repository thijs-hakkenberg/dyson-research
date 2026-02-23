---
paper: "03-multi-model-ai-consensus"
version: "e"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-23"
recommendation: "Major Revision"
---

# Peer Review: Multi-Model AI Deliberation for Complex Engineering Decisions

**Manuscript ID:** [Version E]
**Reviewer Role:** Academic Peer Reviewer (AI Systems / Engineering Design)
**Target Venue:** IEEE Intelligent Systems / Design Science

---

## Review Criteria

### 1. Significance & Novelty
**Rating: 4 (Good)**

The manuscript addresses a critical and timely gap in the literature: moving Multi-Agent Systems (MAS) from conversational games or simple coding tasks to complex, unstructured engineering trade studies. The paper's primary conceptual contribution—shifting the goal from "consensus" to the "structured preservation of divergent views"—is excellent. This reframes the hallucination/disagreement problem in LLMs as a feature for design space exploration, which is a novel and valuable perspective for the engineering design community.

However, while the *application* and the *divergent view schema* are novel, the underlying mechanics (voting, iterative refinement) are incremental improvements on existing debate frameworks (e.g., Du et al., 2023; Liang et al., 2024). The significance lies heavily in the formalization of the *process* and the *artifacts* (YAML schemas for disagreement) rather than algorithmic breakthroughs in the models themselves.

### 2. Methodological Soundness
**Rating: 3 (Adequate)**

The deliberation protocol itself is defined with admirable rigor. The voting logic, round structure, and termination conditions are specified clearly enough to be reproduced. The choice of $0.5\times$ weighting for self-votes is a thoughtful heuristic.

However, the **experimental validation** contains a significant weakness. The paper relies primarily on within-study comparisons (Round 1 vs. Final Round) and a confounded post-hoc aggregation baseline. As the authors honestly admit in Section 6.2, comparing Round 1 (independent generation) to Round $N$ (deliberation) conflates the benefits of *adversarial review* with the benefits of simply *more compute and context*.

To claim that multi-model deliberation is superior, the study lacks a critical control: **Single-Model Self-Refinement**. Without comparing the deliberation results against a single model iterating on its own work for the same number of rounds (with its own prior outputs as context), we cannot isolate the "wisdom of the crowd" effect from the "chain of thought" effect.

### 3. Validity & Logic
**Rating: 3 (Adequate)**

The authors demonstrate high intellectual integrity. Section 6 (Discussion) is refreshing in its honesty regarding limitations, specifically the "Sycophancy" threat (70% framework adoption rate) and the lack of repeated trials. The analysis of the "Divergent Views" is qualitatively strong, and the effort to validate these against external literature (Table 4) adds necessary grounding.

The logic falters slightly in the interpretation of the results. The paper presents the convergence patterns (Fig. 3) as findings, but as noted in the text, these are largely mechanical consequences of the termination rules. Furthermore, the reliance on a "Dyson Swarm" case study—while fascinating—introduces a domain where "ground truth" is speculative. While this is acceptable for *methodological* papers, it makes validity checking difficult compared to established engineering benchmarks.

### 4. Clarity & Structure
**Rating: 5 (Excellent)**

The manuscript is exceptionally well-written. The structure is logical, following a standard Design Science flow. The distinction between the *Model*, *Orchestration*, and *Output* layers (Fig. 1) is clear. The inclusion of code snippets (YAML schema) greatly aids understanding. The definitions of voting criteria and termination logic are unambiguous.

### 5. Ethical Compliance
**Rating: 5 (Excellent)**

The Ethics Statement (Section 7) is exemplary. The authors clearly disclose the use of AI assistance in writing, the use of commercial APIs, and the lack of human subjects. The discussion regarding the environmental cost of multi-round deliberation is a welcome addition often missing from MAS papers.

### 6. Scope & Referencing
**Rating: 5 (Excellent)**

The paper is perfectly scoped for a journal like *IEEE Intelligent Systems* or *Design Science*. It bridges the gap between raw AI capability research and systems engineering methodology. The references are comprehensive, covering the history of Delphi methods (Linstone, 1975), classic design rationale (MacLean, 1991), and modern LLM debate literature.

---

## Major Issues

**1. Missing Control Condition (The "Self-Refine" Baseline)**
The paper argues that multi-model deliberation improves outcomes. However, the current baseline (Round 1 independent proposals) is insufficient. It is well-known that LLMs improve their output when given a chance to critique and refine their own work.
*   **Requirement:** The authors must perform the "Experiment 2" listed in their own Validation Roadmap (Section 6.2.2). Run a subset of questions where a single model (e.g., Claude 4.6) generates a proposal, critiques it, and refines it for the same number of rounds as the deliberation group. Compare the final quality and trade-off identification of this "Self-Refine" condition against the "Multi-Model Deliberation" condition. Without this, the paper cannot claim that *multi-agent* dynamics are the source of improvement.

**2. Sycophancy vs. Consensus**
The observation that 70% of Round 2+ proposals adopt the previous winner's framework (Section 6.4) is alarming. This suggests the system might be an "echo chamber generator" rather than a deliberation engine.
*   **Requirement:** While a full $2\times2$ factorial experiment might be out of scope for a revision, the authors must provide stronger evidence that the convergence is not merely sycophantic. A qualitative analysis of *why* the framework was adopted in a few specific cases (e.g., did the model explicitly cite a superior feature of the winner?) would strengthen the defense against the sycophancy hypothesis.

**3. Evaluation of "Quality"**
The paper relies on the authors' own manual review to validate the "Divergent Views" (Section 5.5). While the authors have domain expertise, self-evaluation is prone to bias.
*   **Requirement:** If possible, a small subset of the outputs (e.g., 3 questions) should be evaluated by an external expert blinded to the source (Deliberation vs. Baseline). If external evaluation is not feasible, the authors must calculate and report inter-rater reliability (Cohen’s $\kappa$) for their internal classification of the 47 divergent topics to demonstrate that the categorization of "Genuine trade-off" vs. "Knowledge gap" is robust.

---

## Minor Issues

1.  **Truncation Strategy:** Section 3.2.1 mentions "head truncation" (first 1,000 words). This is a potential validity threat. In engineering proposals, the "Risk" and "Cost" sections often come at the end. Truncating them means models are debating the *introductory philosophy* rather than the *downstream consequences*. The authors should acknowledge this specifically as a limitation or justify why head-truncation was chosen over summarization.
2.  **Temperature Sensitivity:** The paper uses a fixed temperature of $T=0.7$. In consensus-seeking tasks, temperature is a critical hyperparameter. A brief mention of why 0.7 was chosen (vs. 0.0 for reproducibility or 1.0 for diversity) would be helpful.
3.  **Synthesizer Bias:** Section 3.3 notes that Claude 4.6 is the default synthesizer. Does this bias the final report toward Claude's stylistic preferences? A brief sentence addressing this potential bias is warranted.
4.  **Figure 4 (Vote Distribution):** The figure is referenced but the analysis of *why* REJECT votes are so rare (8%) could be deepened. Is the voting scale too coarse?

---

## Overall Recommendation

**Major Revision**

This paper presents a high-quality methodology and a valuable new perspective on AI-assisted engineering (focusing on disagreement preservation). However, the empirical validation is currently insufficient to support the central claims. The comparison between "Single-shot" and "Multi-round deliberation" is scientifically weak because it ignores the confounding variable of iteration.

I strongly encourage the authors to perform the **Single-Model Self-Refinement** control experiment described in their own "Future Work" section. Adding this data—even for a subset of the questions—would isolate the specific contribution of the multi-agent architecture and make this a landmark paper.

---

## Constructive Suggestions

1.  **Execute the "Self-Refine" Baseline:** Take 4 representative questions (one from each difficulty category). Run a single model (e.g., GPT-5.2) through a loop: *Generate -> Critique -> Refine -> Critique -> Refine*. Compare the final output to the Multi-Model output. If the Multi-Model output finds more *valid* divergent views or trade-offs, your hypothesis is proven.
2.  **Formalize the Divergent View Schema:** The YAML snippet in Section 3.4 is excellent. Consider proposing this schema as a standard for the field (e.g., "The Engineering Disagreement Interchange Format"). This elevates the paper from a case study to a standards proposal.
3.  **Strengthen the "Human-in-the-loop" Narrative:** Emphasize more strongly that this system is a *pre-processor* for humans. The value proposition is strongest when you frame this as "saving the human expert from starting with a blank page" rather than "making the decision."
4.  **Visualize the Genealogy:** A graph showing how a specific idea (e.g., the "Shepherd" node) originated in Model A, was critiqued by Model B, and refined by Model C would be a powerful visual addition to Section 5.6.