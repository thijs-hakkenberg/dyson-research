---
paper: "03-multi-model-ai-consensus"
version: "g"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-23"
recommendation: "Major Revision"
---

# Peer Review: Multi-Model AI Deliberation for Complex Engineering Decisions

**Manuscript:** Multi-Model AI Deliberation for Complex Engineering Decisions: A Structured Methodology with Divergent View Preservation
**Venue:** IEEE Intelligent Systems
**Version:** G — February 2026

---

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a genuine gap at the intersection of multi-agent LLM systems and engineering design methodology. The core idea—treating disagreement among LLMs as a first-class informational output rather than noise to be minimized—is conceptually appealing and, to my knowledge, has not been formalized in the published literature for engineering trade studies specifically. The divergent views schema (Listing 1) is a concrete, potentially useful contribution that could see adoption in design rationale systems.

However, the novelty claim requires qualification. The methodology is essentially a computational Delphi method with LLMs substituted for human experts—a connection the authors acknowledge (Section 6.1) but perhaps understate. The round structure (propose → evaluate → iterate) is well-established in consensus methods, and the voting mechanism (Eq. 1) is straightforward weighted aggregation. The intellectual contribution lies more in the *application* and *framing* (disagreement preservation) than in algorithmic innovation. The paper would benefit from more precisely delineating what is genuinely new versus what is a known technique applied in a new context.

The practical significance is also somewhat unclear. The authors position the methodology as producing "inputs for human judgment" (Section 8), but without expert evaluation of those inputs, we cannot assess whether the methodology produces *useful* inputs. The 12 literature-confirmed trade-offs (Table 5) are encouraging but represent a modest validation: confirming that LLMs can identify known trade-offs is a weaker claim than showing they surface *novel* or *non-obvious* ones. The paper would be strengthened by at least one example where the deliberation surfaced a trade-off that was genuinely surprising to domain experts.

## 2. Methodological Soundness

**Rating: 2 (Needs Improvement)**

The methodology is described in commendable detail—sufficient for reproduction, as claimed. The round structure (Section 3.2), voting mechanics (Eq. 1), and termination conditions are precisely specified. The open-source release strengthens reproducibility. However, several methodological concerns are significant.

**Absence of repeated trials.** This is the most critical weakness. Each of the 16 deliberations was run exactly once at T=0.7. The authors acknowledge this (Section 6.3) but the implications are severe: we have no estimate of the variance of *any* reported statistic. The mean of 2.3 rounds could be 1.5 or 3.5 on a different day. The 47 divergent topics could be 30 or 60. The bootstrap CI reported ([1.9, 2.8]) is explicitly acknowledged as cross-question variation, not run-to-run variation, yet it appears in the abstract-adjacent text in a way that could mislead. For a methodology paper, demonstrating stability is essential—without it, we are evaluating a single trajectory through a stochastic process.

**Confounded baselines.** Both baseline comparisons are acknowledged as confounded, but the paper still draws conclusions from them. The aggregation baseline uses a different prompt structure and a different temperature (T=0.3 vs. T=0.7). The self-refinement baseline was run on only 4 of 16 questions. The qualitative differences reported (Section 5.5, items 1–3) are plausible but anecdotal—they describe individual instances rather than systematic patterns. The claim that "31 substantive disagreements... represent design space that single-model approaches were not observed to surface" (Section 5.3) is stated more strongly than the evidence supports, given the confounded comparison.

**Similarity analysis limitations.** The TF-IDF similarity decrease (Δ = −0.022) is presented as evidence against sycophancy, but the effect size is tiny and no statistical test is reported. With n=6 multi-round deliberations, statistical power is very low. The authors correctly note that conceptual sycophancy could coexist with textual divergence, but this caveat appears only in Section 6.3, while the finding is presented more assertively in the abstract and conclusion. The 0% heading adoption metric is interesting but narrow—models could converge substantively while using different section headers.

**Reviewer classification.** The 47 divergent topics were classified by "three reviewers" who appear to be system designers rather than independent domain experts. The 81% initial agreement is reported without Cohen's κ, and all disagreements were "resolved through discussion"—a process that could mask systematic bias. The authors acknowledge these limitations but proceed to use the classifications as if they were reliable.

## 3. Validity & Logic

**Rating: 4 (Good)**

This is where the paper distinguishes itself from many LLM-systems papers: the authors are remarkably honest about the limitations of their evidence. Nearly every empirical claim is accompanied by an appropriate caveat. The abstract uses "illustrative" and "preliminary" correctly. Section 6.3 is an unusually thorough self-critique. The validation roadmap (Section 6.4, Table 7) specifies exactly what experiments are needed, with cost estimates, demonstrating that the authors understand what would constitute proper validation.

The logical structure of the argument is sound: the paper claims to present a *methodology* and *illustrate* it, not to *validate* it. This framing is appropriate given the evidence. However, there are places where the rhetoric slightly outpaces the evidence. The abstract's "partial evidence against sycophantic convergence" is fair, but the conclusion's "preliminary evidence addresses key concerns about sycophancy" (Section 8) is slightly stronger than warranted by a Δ of −0.022 on 6 deliberations. Similarly, "31 substantive disagreements... represent design space that was not surfaced in the single-model baselines tested" conflates "not observed in a confounded comparison" with "would not be surfaced."

The case study (Section 5.4) is well-chosen and effectively illustrates the methodology's dynamics. The progression from independent proposals through mutual refinement to preserved divergent views is clearly narrated. However, a single case study cannot establish generalizability—the paper would benefit from a second case study showing a *failure mode* (e.g., one of the governance questions where convergence was problematic).

The epistemological discussion in Section 6.3 ("LLM consensus is not truth") is thoughtful and important. The argument that divergent views are epistemically more valuable than consensus is well-made, though it could be developed further with reference to the epistemology of disagreement literature (e.g., Christensen & Lackey, 2013).

## 4. Clarity & Structure

**Rating: 4 (Good)**

The paper is well-organized and clearly written. The progression from methodology (Section 3) through application domain (Section 4) to illustrative results (Section 5) and discussion (Section 6) is logical. The abstract accurately represents the paper's contents and claims. Technical details are presented with appropriate precision—the YAML schema (Listing 1), scoring equation (Eq. 1), and configuration table (Table 1) enable reproduction.

Figures are numerous (8 referenced) and appear well-chosen, though I cannot evaluate them directly from the LaTeX source. The paper may be slightly over-figured for its length—Figures 4 (word count distribution) and 7 (similarity heatmap) could potentially be moved to supplementary material without loss. Tables are effective, particularly Table 5 (validated divergent views) and Table 7 (required experiments).

A few structural issues: Section 5 is titled "Illustrative Application" but contains baseline comparisons (5.5) and similarity analysis (5.6) that are more evaluative than illustrative—these might be better placed in a separate "Preliminary Evaluation" section. The paper is long for IEEE Intelligent Systems (which typically targets 6,000–8,000 words for feature articles); this manuscript likely exceeds 8,000 words and would benefit from tightening, particularly in Sections 5.2 (voting dynamics) and 6.1 (comparison with human panels).

Minor clarity issues: the term "frontier LLMs" is defined in the introduction but used inconsistently thereafter. The footnote about model versioning (Section 3.1) raises an important concern that deserves more than a footnote—if the weights served through Databricks differ from direct API access, reproducibility is compromised in a way that should be discussed in the limitations.

## 5. Ethical Compliance

**Rating: 5 (Excellent)**

The ethics statement (Section 7) is thorough and addresses the key concerns: AI writing assistance disclosure, potential for misuse (selective reporting), false authority, and computational cost. The title-page footnote about AI involvement is prominent and specific. The recommendation that outputs "always be reviewed by qualified domain experts" is repeated appropriately.

The paper goes beyond minimum compliance in several ways: the divergent views schema is explicitly framed as a safeguard against selective reporting; the "LLM consensus is not truth" discussion (Section 6.3) is a responsible epistemological framing; and the open-source release enables scrutiny. The acknowledgment that system designers rather than independent experts performed the divergent view classification is commendably honest.

One minor gap: the paper does not discuss potential dual-use concerns. While the Dyson swarm application is benign, the methodology could be applied to domains where AI-generated engineering recommendations carry safety-critical implications (e.g., nuclear systems, autonomous weapons). A brief note acknowledging this would strengthen the ethics discussion.

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The reference list (29 items) covers the key areas: multi-agent LLM systems, consensus methods, engineering design, and structured disagreement. Core references are appropriate (Linstone & Turoff, Du et al., Wu et al., Surowiecki). The inclusion of design rationale literature (Lee 1991, MacLean 1991) and structured disagreement methods (Zenko, Schwenk) demonstrates breadth.

However, several gaps are notable. The paper does not cite recent work on LLM calibration and uncertainty quantification (e.g., Xiong et al., 2024, "Can LLMs Express Their Uncertainty?"), which is directly relevant to the divergent views contribution. The ensemble methods literature in machine learning—where model disagreement has been studied extensively as a signal of epistemic uncertainty (Lakshminarayanan et al., 2017)—is entirely absent, despite the clear conceptual parallel. Work on LLM sycophancy beyond Perez et al. (2022) should be cited (e.g., Sharma et al., 2024, "Towards Understanding Sycophancy in Language Models"). The epistemology of disagreement literature mentioned in my validity assessment is also missing.

The paper targets IEEE Intelligent Systems, which is appropriate for the multi-agent AI systems contribution. However, the engineering trade study framing might find a more receptive audience at venues like ASME IDETC, Systems Engineering journal, or AIAA, where the domain expertise of reviewers would better match the application. The paper sits somewhat uncomfortably between an AI systems contribution (where the evaluation is too preliminary) and an engineering methodology contribution (where the AI novelty is the main draw).

Reference [10] (Perez et al., 2022) is cited in the bibliography but I do not find it cited in the main text—this should be verified.

---

## Major Issues

1. **No repeated trials (critical).** The complete absence of repeated trials undermines every quantitative claim in the paper. A methodology paper must demonstrate that its outputs are stable. Even 3 repetitions of 4 strategically chosen questions (matching the self-refinement baseline scope) would dramatically strengthen the contribution. Without this, the 47 divergent topics, 2.3-round mean, and similarity statistics are point estimates from a single stochastic realization. The authors' own Experiment 4 (Table 7) estimates this at $100–400—it should have been conducted before submission.

2. **Baselines are insufficient for the claims made.** The paper repeatedly contrasts deliberation outputs with baseline outputs (e.g., "31 substantive disagreements... represent design space that was not surfaced in the single-model baselines tested"), but both baselines are acknowledged as confounded. The self-refinement baseline covers only 4 questions. Either the claims should be weakened to match the evidence, or at minimum Experiment 2 (full self-refinement across 16 questions with controlled prompts) should be completed.

3. **No independent expert evaluation.** The divergent view classification was performed by system designers, not independent domain experts. The within-study comparison (Table 6) uses metrics defined by the authors. No external validation of output quality exists. For a paper claiming to produce useful engineering trade study inputs, at least a small-scale expert evaluation (even 3–4 questions assessed by 2 independent engineers) would substantially strengthen the contribution.

4. **Similarity analysis is underpowered and over-interpreted.** The TF-IDF decrease of −0.022 across 6 multi-round deliberations is presented in the abstract as "partial evidence against sycophantic convergence." No significance test is reported. The sample size (n=6) is too small for reliable inference. The effect could easily be noise. This finding should be presented more cautiously or supplemented with additional analysis (e.g., semantic similarity using embedding models, which would capture conceptual convergence better than TF-IDF).

## Minor Issues

1. **Section 3.1:** The justification for three models ("with fewer than three, meaningful voting dynamics cannot emerge") is asserted without support. Two models can engage in meaningful debate; the issue is more about tie-breaking and diversity. Consider citing literature on optimal panel size.

2. **Equation 1:** The notation could be clearer—$v_{ji}$ is defined as "the score assigned by model $j$ to proposal $i$" but the three-level scale (0, 1, 2) should be stated in the equation's context, not only earlier in the text.

3. **Section 5.2:** The correlation $r = 0.72$ between self-votes and peer-votes ($n = 54$) is reported with $p < 0.001$, but the unit of analysis (proposals) may violate independence assumptions since the same models appear across deliberations. A mixed-effects model or clustered standard errors would be more appropriate.

4. **Table 3:** The self-vote sensitivity analysis is useful but reports only winner changes, not score magnitude changes. A small score change that doesn't flip the winner could still affect the deliberation dynamics.

5. **Section 5.4 (case study):** "Two of three models voted CONCLUDE; unanimity was not achieved due to a JSON parsing failure." This is a concerning failure mode—a technical bug affected the termination decision. Was this the only instance? The 4/48 parsing failure rate (8.3%) for Gemini deserves more discussion of robustness.

6. **Abstract:** "with 0% heading adoption between models" is an oddly specific metric to highlight in the abstract. Consider replacing with a more interpretable finding.

7. **Reference formatting:** Several arXiv preprints have been published at venues (e.g., [6] Wu et al. appeared at ICLR 2024; [7] Zheng et al. at NeurIPS 2023 as noted). Citations should be updated to published versions.

8. **Section 4:** The description of Project Dyson as maintaining "over 142 research questions" is oddly precise for an approximate count. Either give the exact number or say "over 140."

9. **Table 2 (comparison):** The cost comparison (\$5–20 vs. \$5,000–50,000) is misleading without the quality caveat being in the table itself, not just the caption. Consider adding a row for "Output quality validation" showing "Pending" for multi-model.

10. **Missing citation in text:** Reference [10] (Perez et al., 2022) and [22] (Kadavath et al., 2022) appear in the bibliography but I cannot locate where they are cited in the body text.

---

## Overall Recommendation

**Major Revision**

This paper presents a well-conceived methodology with a genuinely interesting core idea (structured disagreement preservation), described with unusual honesty about its limitations. The writing quality is high, the self-critique is thorough, and the open-source release adds value. However, the empirical foundation is insufficient for publication in its current form. The absence of repeated trials, the confounded baselines, the lack of independent expert evaluation, and the underpowered similarity analysis collectively mean that the paper's empirical claims—even the modest ones it makes—are not adequately supported. The authors have essentially written their own revision roadmap (Section 6.4, Table 7); completing Experiments 2 and 4 at minimum, and ideally a small-scale expert evaluation, would transform this from a promising methodology sketch into a publishable contribution. The methodology description and divergent views schema are publication-ready; the evaluation needs substantial strengthening.

---

## Constructive Suggestions

1. **Conduct repeated trials (Experiment 4) before resubmission.** Run at least 4 questions × 5 repetitions at T=0.7. Report winner stability (% of runs producing the same winner), divergent view consistency (Jaccard overlap of topics across runs), and convergence round variance. This is estimated at $100–400 and would address the single most critical weakness. Present results as a stability analysis table.

2. **Add semantic similarity analysis alongside TF-IDF.** Use sentence-level embedding models (e.g., text-embedding-3-large) to compute cross-model similarity, which would capture conceptual convergence that TF-IDF misses. This directly addresses the "conceptual sycophancy with textual independence" concern the authors raise. Report both metrics side-by-side to provide a more complete picture.

3. **Recruit 2–3 independent domain experts for a small-scale quality evaluation.** Even evaluating 4 deliberation outputs (one per convergence category) against matched self-refinement outputs in a blinded comparison would provide crucial external validation. Use the quality dimensions from Table 6 as the evaluation rubric. Report inter-rater reliability with Cohen's κ.

4. **Add a failure-mode case study.** The swarm coordination case study (Section 5.4) illustrates the methodology working well. Add a second case study showing a governance question where convergence was problematic, illustrating the methodology's limitations concretely. This would strengthen the paper's credibility and provide practical guidance for users.

5. **Sharpen the novelty claim relative to computational Delphi.** The current framing sometimes implies more novelty than exists. Consider explicitly positioning the contribution as: (a) the first application of computational Delphi with heterogeneous LLMs to engineering trade studies, (b) the divergent views schema as a novel output artifact, and (c) the empirical characterization of multi-model deliberation dynamics. This more precise framing would be more defensible and arguably more useful to the community.