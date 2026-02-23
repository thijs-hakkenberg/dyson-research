---
paper: "03-multi-model-ai-consensus"
version: "e"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-23"
recommendation: "Major Revision"
---

# Peer Review: Multi-Model AI Deliberation for Complex Engineering Decisions

## 1. Significance & Novelty

**Rating: 3.5 (Adequate to Good)**

The paper addresses a genuinely interesting gap at the intersection of multi-agent LLM systems and engineering design methodology. The core insight—that structured disagreement preservation is more valuable than consensus—is compelling and well-articulated. The connection to the Delphi method tradition is apt, and the divergent views schema (Section 3.4) represents a concrete, implementable contribution that could see adoption in engineering practice. The positioning of this work within the design rationale tradition (DRL, QOC) is particularly well done and adds intellectual depth.

However, the novelty claim requires qualification. The paper states (Section 1, paragraph 3) that "no structured methodology has been published for multi-model deliberation on engineering trade studies." While this specific combination may be novel, the individual components—multi-agent debate (Du et al., 2023), LLM-as-judge (Zheng et al., 2024), structured output schemas—are well-established. The contribution is primarily one of integration and application rather than fundamental methodological innovation. The divergent views schema is the most novel element, but its value proposition rests on empirical claims about quality (the 12 confirmed trade-offs) that are validated only through the authors' own review, not independent assessment.

The significance is also limited by the absence of controlled experiments. The authors are commendably transparent about this (the validation roadmap in Section 6.2 is unusually well-specified for a limitations section), but the paper as submitted is essentially a methodology description with illustrative case studies. The field has moved past the point where methodology proposals without empirical validation carry high impact. The post-hoc aggregation comparison (Section 5.7) is a step in the right direction but, as the authors acknowledge, is confounded.

## 2. Methodological Soundness

**Rating: 3 (Adequate)**

The methodology is described with commendable precision and reproducibility. The round structure (Section 3.2), voting mechanics (Equation 1), termination conditions (Section 3.2.3), and divergent views schema (Section 3.4) are specified in sufficient detail for independent implementation. The open-source release of the orchestration code strengthens reproducibility. The configuration parameter table (Table 1) is a useful reference.

Several methodological concerns warrant attention. First, the three-level voting scale (APPROVE/NEUTRAL/REJECT = 2/1/0) is coarse. With only three models voting, the effective score range per proposal is narrow (0–5 with self-vote weighting), creating limited discriminative power. The authors note that ties are broken by APPROVE count, but the scoring resolution may be insufficient to distinguish meaningfully between proposals of similar quality. A finer-grained scale (e.g., 1–5 or 1–10) would provide greater discrimination, though at the cost of potentially less reliable LLM scoring. The rationale for the three-level choice is not discussed.

Second, the selection of Claude 4.6 as the default synthesizer (Section 3.3) introduces a systematic bias that the authors acknowledge (Section 6.4, "Single synthesizer bias") but do not mitigate. Given that Claude also casts the most REJECT votes (Section 5.3), its role as both the most critical evaluator and the default synthesizer creates a potential confound: the synthesized conclusions may systematically reflect Claude's more conservative framing. At minimum, a sensitivity analysis using each model as synthesizer for a subset of questions would strengthen the paper.

Third, the question selection criteria (Section 4.2) explicitly exclude questions where single-model responses were adequate, creating a selection bias that the authors acknowledge. However, the implications are more severe than stated: the 16 questions were selected *because* they were expected to benefit from multi-model deliberation, making any within-study comparison of Round 1 versus final-round proposals (Table 6) circular. The questions were chosen for complexity, so of course multi-round treatment produces richer outputs.

Fourth, the self-vote weight of 0.5 is described as "selected empirically" (Section 3.2.2), but no details of this empirical selection process are provided. Was it tuned on a held-out set? Selected from a grid search? Chosen based on intuition and post-hoc justified? The sensitivity analysis (Table 4) is welcome but was conducted post-hoc on the same data used to select the parameter.

## 3. Validity & Logic

**Rating: 4 (Good)**

This is the paper's strongest dimension. The authors demonstrate an unusual degree of intellectual honesty about the limitations of their evidence. The careful distinction between "illustrative" and "evaluative" results (Section 5, opening paragraph) is maintained consistently throughout. The three competing interpretations of framework adoption (Section 6.4, sycophancy discussion) are a model of balanced analysis. The bootstrap CI caveat (Section 6.4, "No repeated trials") correctly notes that the empirical distribution is more informative than the interval. The aggregation comparison (Section 5.7) is presented with appropriate caveats about confounding.

The logic of the divergent views quality assessment (Section 5.5) is sound in structure but limited in execution. The 81% initial inter-rater agreement is reported transparently, but the absence of Cohen's κ is a notable gap—81% raw agreement with only four categories could reflect moderate to substantial agreement depending on the marginal distributions. More critically, the reviewers are members of the Project Dyson research team who designed the system, creating an obvious conflict of interest in quality assessment. The authors acknowledge this ("the use of system designers as reviewers rather than independent domain experts represent limitations"), but this is not merely a limitation—it is a fundamental threat to the validity of the quality claims. The 12 "confirmed genuine trade-offs" are confirmed only by the system's creators.

The correlation between self-votes and peer votes (r = 0.72, p < 0.001, n = 54) is reported with appropriate aggregation to the proposal level to address non-independence. However, with only 54 observations and a three-point scale, the distributional assumptions underlying the Pearson correlation should be examined. A Spearman rank correlation would be more appropriate for ordinal data, or at minimum the Pearson result should be accompanied by a note about the ordinal nature of the underlying scale.

The claim that "31 substantive disagreements (66% of total) represent design space that single-model or single-expert approaches would likely have missed" (Section 8) is not supported by any evidence. No single-model or single-expert baseline was run to determine what those approaches would have identified. This claim should be softened or removed.

## 4. Clarity & Structure

**Rating: 4.5 (Good to Excellent)**

The paper is exceptionally well-written for a methodology paper. The prose is clear, precise, and well-organized. The logical flow from motivation (Section 1) through related work (Section 2), methodology (Section 3), application domain (Section 4), results (Section 5), and discussion (Section 6) is natural and easy to follow. The abstract accurately represents the paper's content and claims, including appropriate hedging language.

The figures are well-conceived and informative, though I note that all figures reference PDF files that are not included with the submission. The captions are detailed enough to understand the intended content, which partially compensates. The tables are well-formatted and informative; Table 5 (comparison with Delphi) is particularly effective, and the footnote about cost comparison caveats demonstrates responsible framing.

The case study in Section 5.6 (Swarm Coordination Architecture) is an effective illustration that makes the abstract methodology concrete. The level of detail—specific model proposals, voting dynamics, convergence trajectory—gives the reader a clear picture of how the system operates in practice.

Minor clarity issues: The paper is long (approximately 12,000 words excluding references), which is at the upper bound for most target venues. Some compression is possible in the related work section, which is thorough but could be tightened. The validation roadmap (Section 6.2) is unusually detailed for a discussion section and might be better positioned as a standalone section or appendix.

## 5. Ethical Compliance

**Rating: 5 (Excellent)**

The ethical disclosure in this paper is exemplary and could serve as a model for AI-assisted research. The title page footnote clearly states AI involvement in both the research system and manuscript preparation. Section 7 addresses four specific ethical considerations: false authority, selective reporting, AI writing assistance, and computational energy costs. The recommendation that outputs "always be reviewed by qualified domain experts before informing engineering decisions" (Section 7) is responsible and consistently maintained throughout.

The divergent views schema itself has an ethical dimension that the authors identify: by making disagreements as visible as agreements, it structurally resists the temptation to cherry-pick consensus while ignoring dissent. This is a thoughtful design choice with genuine ethical value.

The open-source release of all code, transcripts, and outputs enables independent auditing, which is the gold standard for transparency in AI-assisted research.

## 6. Scope & Referencing

**Rating: 3.5 (Adequate to Good)**

The reference list is well-curated and covers the relevant literatures: multi-agent LLM systems, Delphi methodology, engineering design methods, and structured decision-making. The connections to design rationale (Lee & Lai, 1991; MacLean et al., 1991) and multi-criteria decision analysis (Keeney & Raiffa, 1976; Saaty, 1980) are particularly valuable and not commonly seen in the LLM literature.

Several gaps in the referencing should be addressed. First, the paper does not cite recent work on LLM ensemble methods and mixture-of-agents approaches (e.g., Wang et al., "Mixture-of-Agents Enhances Large Language Model Capabilities," 2024), which are directly relevant to the multi-model aggregation question. Second, the structured argumentation literature (Toulmin's argument model, IBIS notation) is relevant to the divergent views schema but not cited. Third, the paper does not engage with the growing literature on LLM calibration and confidence estimation, which is relevant to the self-vote analysis. Fourth, the model versions cited (Claude 4.6, Gemini 3 Pro, GPT-5.2) are described as February 2026 releases accessed through Databricks endpoints. The footnote on model versioning ambiguity (Section 3.1) is appropriate, but the paper should note that results may not generalize to other model versions or future releases.

The paper's scope sits somewhat awkwardly between venues. It is too focused on LLM methodology for a space systems journal, too focused on space applications for a pure AI venue, and too preliminary in its empirical results for a design science journal. IEEE Intelligent Systems, as listed in the header, is probably the best fit, but the paper would benefit from stronger empirical grounding to meet that venue's standards.

---

## Major Issues

1. **Absence of controlled baselines (fundamental).** The paper's central claim—that multi-model deliberation produces valuable outputs for engineering trade studies—rests entirely on illustrative case studies without any controlled comparison. The validation roadmap (Section 6.2) is well-specified but unexecuted. The post-hoc aggregation comparison (Section 5.7) is confounded by prompt structure. At minimum, Experiments 1 and 2 from the roadmap (aggregation without deliberation, single-model self-refinement) should be conducted before publication. The authors themselves estimate the cost at $360–$1,360 in API fees—a trivially small barrier. **A methodology paper without empirical validation of the methodology's core mechanism is incomplete.**

2. **Non-independent quality assessment.** The 12 "confirmed genuine trade-offs" (Section 5.5) were validated by the system's designers, not independent domain experts. This is acknowledged but not adequately addressed. The paper's strongest empirical claim—that the divergent views schema captures genuine engineering trade-offs—requires independent validation. At minimum, a subset of divergent views should be assessed by domain experts who are blind to the study's hypotheses and who did not design the system.

3. **No repeated trials.** With n=1 per question at a non-zero temperature (T=0.7), the reproducibility of every reported result is unknown. The authors acknowledge this clearly (Section 6.4), but it undermines all quantitative claims: convergence statistics, voting patterns, divergent view counts, and the aggregation comparison could all be artifacts of a single stochastic realization. Experiment 4 from the roadmap (repeated trials for 4 questions × 5 runs) should be conducted before publication.

4. **Circular question selection.** Questions were selected because single-model responses were inadequate (Section 4.2), then the paper observes that multi-round deliberation improves on single-model responses (Table 6). This is methodologically circular. The selection bias is acknowledged but its implications for the paper's claims are understated.

## Minor Issues

1. **Section 3.2.2:** The Pearson correlation (r = 0.72) is applied to ordinal data (0/1/2 scale). Report Spearman's ρ instead or in addition.

2. **Section 5.3:** "162 individual votes across 16 deliberations" — the arithmetic should be verified. With 3 models × 3 votes per round × varying rounds per deliberation, the expected count depends on the round distribution. The paper reports mean 2.3 rounds × 16 questions × 9 votes/round ≈ 331 votes, which does not match 162. Clarify whether 162 refers to peer votes only, unique proposal evaluations, or another subset.

3. **Table 3 (aggregation results):** The aggregation-only condition identifies 5.4 mean trade-offs versus 1.3 for deliberation. This *reversal* of the expected direction (deliberation producing fewer enumerated trade-offs) deserves more discussion. The explanation offered (prompt structure differences) is plausible but should be explored more carefully—it may indicate that the deliberation process actually *reduces* trade-off enumeration through premature convergence.

4. **Section 3.2.3:** The termination condition descriptions contain a parenthetical about "consecutive-round requirement in the configuration provides a stability check for majority-conclude scenarios" that is somewhat confusing. Clarify the relationship between the unanimous and consecutive-conclude pathways.

5. **Equation 1:** The score formula sums over j ≠ i for peer votes but uses a single self-vote term. With 3 models, this gives a maximum score of 2 + 2 + (0.5 × 2) = 5.0. State the theoretical score range explicitly.

6. **Section 5.5:** The operational definitions of the four classification categories are clear, but the boundary between "reasonable judgment" and "knowledge gap" (where 9 of the inter-rater disagreements concentrated) suggests these categories may not be sufficiently distinct. Consider whether a three-category scheme (genuine trade-off, uncertain/insufficient evidence, error) would be more reliable.

7. **References:** Several arXiv preprints (Du et al., Wu et al., Liang et al., Chan et al.) may have been published in proceedings by the paper's stated date (February 2026). Update citations to published versions where available.

8. **Section 6.1, Table 5:** The Delphi cost range footnote references "Linstone & Turoff (1975)" for 1975 dollar figures but then provides a "contemporary" range of $10,000–$100,000 without citation. Provide a source for the contemporary cost estimate.

9. **Abstract:** At 347 words, the abstract is long for most venues. Consider trimming to ~250 words by condensing the validation roadmap preview.

## Overall Recommendation

**Major Revision**

This paper presents a well-conceived methodology for multi-model AI deliberation with an unusually thoughtful treatment of limitations and a genuinely novel contribution in the divergent views schema. The writing quality is high, the ethical disclosure is exemplary, and the validation roadmap demonstrates that the authors understand exactly what empirical work is needed. However, the paper as submitted is essentially a methodology proposal illustrated by uncontrolled case studies. The authors' own roadmap identifies experiments costing $360–$1,360 in API fees that would substantially strengthen the empirical foundation. The non-independent quality assessment of divergent views and the absence of repeated trials further limit the paper's contribution in its current form. I recommend major revision with the expectation that the authors execute at least Experiments 1, 2, and 4 from their roadmap, obtain independent expert assessment of a subset of divergent views, and report Experiment 3 (blind deliberation) results or clearly scope it as future work. The intellectual framework is strong; the empirical foundation needs to catch up.

## Constructive Suggestions

1. **Execute your own roadmap (highest priority).** Experiments 1 (aggregation without deliberation) and 2 (single-model self-refinement) are inexpensive and would transform the paper from a methodology proposal into an empirical contribution. Run them with matched prompts (identical output format instructions) and report effect sizes with confidence intervals. Even null results would be informative and publishable.

2. **Obtain independent expert evaluation of divergent views.** Recruit 2–3 domain experts (aerospace engineering, space systems) who are not affiliated with Project Dyson to blindly assess a stratified sample of 15–20 divergent views using your four-category scheme. Report Cohen's κ for inter-rater reliability. This addresses the most serious validity threat at modest cost.

3. **Run repeated trials for variance estimation.** Select 4 questions (one per convergence category) and run each 5 times at T=0.7. Report winner stability, convergence round variance, and Jaccard similarity of divergent topic sets. This is Experiment 4 from your roadmap and would cost approximately $100–$400 in API fees. Without this, no quantitative claim in the paper has a known error bar.

4. **Investigate the aggregation trade-off reversal.** The finding that aggregation-only synthesis identifies *more* enumerated trade-offs than full deliberation (5.4 vs. 1.3 per question) is potentially the most interesting empirical result in the paper, but it is buried in caveats. Design a controlled comparison with matched prompts and output formats to determine whether deliberation genuinely reduces trade-off enumeration (possibly through premature convergence) or whether this is purely a prompt artifact. This could become a central finding rather than an awkward footnote.

5. **Consider a finer-grained voting scale or alternative aggregation.** The three-level scale (0/1/2) with three voters produces very limited score discrimination. Explore whether a 5-point or 7-point scale, or alternative aggregation methods (e.g., rank-order voting, pairwise comparison), would produce more informative voting dynamics. This could be tested on a subset of questions without re-running all 16 deliberations.