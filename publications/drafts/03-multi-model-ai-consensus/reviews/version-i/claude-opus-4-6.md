---
paper: "03-multi-model-ai-consensus"
version: "i"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-24"
recommendation: "Major Revision"
---

# Peer Review: Multi-Model AI Deliberation for Complex Engineering Decisions

## 1. Significance & Novelty

**Rating: 4 (Good)**

This paper addresses a genuine and timely gap at the intersection of multi-agent LLM systems and engineering design methodology. The core insight—that disagreement among LLM agents should be treated as a first-class informational artifact rather than noise to be minimized—is both original and practically valuable. The divergent views schema (Section 3.3) is the paper's most distinctive contribution and represents a meaningful advance over existing multi-agent debate frameworks (Du et al., Irving et al.), which focus on convergence toward correctness rather than preservation of legitimate design trade-offs.

The framing as a "computational Delphi" is well-motivated and the connection to the expert consensus literature is more than superficial—the authors demonstrate genuine understanding of why Delphi works (anonymity, structured feedback, iteration) and how those principles translate to the LLM setting. The application to engineering trade studies, where multiple valid solutions exist along incommensurable dimensions, is a meaningful departure from the factual accuracy tasks that dominate the multi-agent debate literature.

However, the novelty claim should be tempered somewhat. The orchestration architecture itself (parallel generation → peer evaluation → iteration) is relatively straightforward, and the weighted voting mechanism (Eq. 1) is simple. The paper's novelty rests primarily on (a) the application domain, (b) the divergent views schema, and (c) the empirical characterization. Of these, (b) is the strongest contribution, while (a) and (c) are limited by the illustrative rather than evaluative nature of the study. The authors are commendably honest about this (e.g., "illustrative rather than evaluative" in Section 5), but it does limit the paper's immediate impact.

## 2. Methodological Soundness

**Rating: 3 (Adequate)**

The methodology is described with commendable precision—the round structure (Section 3.2), scoring formula (Eq. 1), termination conditions, and configuration parameters (Table 2) are specified in sufficient detail for reproduction. The open-source release of transcripts and code further supports reproducibility. The authors deserve credit for the level of protocol specification, which exceeds most papers in this space.

However, several methodological concerns limit confidence in the findings. First, the choice of three specific models is justified only briefly ("balances diversity against coordination complexity"), but the paper provides no systematic analysis of how results would change with different model combinations or with newer model versions. Given the rapid pace of LLM development, the specific models used (Claude 4.6, Gemini 3 Pro, GPT-5.2) may behave quite differently from their successors, raising questions about the generalizability of the observed dynamics. The footnote acknowledging that "model weights served may differ from providers' direct APIs" is appreciated but underscores this fragility.

Second, the repeated trials experiment (Section 5.7, $n = 5$ trials on 4 questions) is a welcome addition but remains underpowered. With only 20 total trials, the 85% winner stability figure has wide confidence intervals that are not reported. A simple binomial confidence interval for 17/20 successes gives approximately [62%, 97%] at 95% confidence—substantially less impressive than the point estimate suggests. The stratification strategy (one question per convergence category) is reasonable but means each category is represented by a single question, making it impossible to separate question-level effects from category-level effects.

Third, the similarity analysis (Section 5.6) is creative but the interpretation requires caution. The finding that all six metrics decrease across rounds is presented as evidence against sycophancy, but an alternative explanation is that models, having seen each other's proposals, deliberately differentiate their language while converging on substance—a form of "cosmetic divergence" that the authors partially acknowledge ("more sophisticated forms of strategic agreement... cannot be ruled out"). The sample of $n = 6$ multi-round deliberations is small, and no statistical tests are reported for the decreases in Table 6. Given the magnitudes involved (e.g., $\Delta = -0.001$ for heading Jaccard), some of these decreases may not be meaningful.

Fourth, the temperature setting of $T = 0.7$ is used throughout without justification beyond "balances creativity with coherence." Given that temperature directly affects the stochasticity that the repeated trials rely on for independence, a sensitivity analysis across temperature values is a significant omission.

## 3. Validity & Logic

**Rating: 4 (Good)**

The paper demonstrates an unusually high degree of self-awareness about its limitations, which substantially strengthens the validity of its claims. The authors consistently hedge appropriately: "illustrative rather than evaluative" (Section 5), "confounded by prompt structure" (Section 5.5), "suggestive but confounded" (Section 6.3). The validation roadmap (Section 6.3, Table 9) is admirably specific about what experiments are needed and what they would establish.

The logical structure of the sycophancy analysis is well-constructed. The authors present three complementary lines of evidence: (1) decreasing cross-model similarity (Table 6), (2) commitment-level tracking showing winner self-consistency exceeds non-winner adoption (Table 7), and (3) zero heading adoption. The reconciliation of 70% framework adoption with decreasing textual similarity through the commitment-level analysis (Section 5.7) is a genuinely insightful piece of analysis that resolves what initially appears to be a contradiction.

However, several logical issues deserve attention. The claim that "11 of 13 REJECT justifications identified genuine technical issues" (Section 5.2) is presented without specifying who made this determination or what criteria were used. If the system designers made this judgment, it is subject to confirmation bias. Similarly, the divergent view categorization (Table 4) was performed by "three reviewers" who appear to be the system designers themselves—the paper acknowledges this limitation but does not adequately address it.

The causal interpretation of convergence patterns (Section 5.1) conflates protocol mechanics with substantive findings. The observation that "questions with higher initial agreement terminate faster" is, as the authors note, "a partly mechanical consequence of the voting-based termination rules." More such mechanical confounds may exist but go unacknowledged—for instance, the finding that governance questions take more rounds could reflect the models' training data distribution (more diverse governance perspectives in training data) rather than anything about the questions' inherent difficulty.

The comparison in Table 8 (Round 1 vs. final round) is particularly problematic. The improvements shown (more design dimensions covered, more trade-offs identified, fewer contradictions) could be entirely explained by the additional compute and context provided in later rounds, independent of the multi-model deliberation mechanism. The authors acknowledge this but still present the table prominently, which may mislead readers who skim rather than read carefully.

## 4. Clarity & Structure

**Rating: 4 (Good)**

The paper is well-organized and clearly written, with a logical flow from motivation through methodology, application, and discussion. The abstract is accurate and appropriately hedged, though at 250+ words it is somewhat long for IEEE Intelligent Systems. The case study (Section 5.4) effectively grounds the abstract methodology in concrete deliberation dynamics, and the YAML schema example (Listing 1) makes the divergent views contribution tangible.

Tables and figures are generally well-designed. Table 1 (convergence statistics) and Table 6 (similarity metrics) are clean and informative. The self-vote sensitivity analysis (Table 5) is a model of how to present robustness checks. However, the paper references 10 figures, many of which appear to serve similar purposes (e.g., Fig. 2 and Fig. 3 both address convergence; Figs. 7–9 all address similarity). Given that figures are described but not viewable in this review, it is difficult to assess whether all are necessary, but the paper would likely benefit from consolidation.

The writing quality is high throughout, with technical precision and appropriate hedging. One structural concern is that Section 5 ("Illustrative Application") at ~4,500 words is disproportionately long relative to the methodology section (~2,000 words). Some of the detailed voting analysis (e.g., Gemini's JSON parsing failures) could be moved to supplementary material without loss.

The paper's most significant clarity issue is the relationship between the various analyses addressing sycophancy. The reader encounters this concern in at least four places: Section 5.2 (voting dynamics), Section 5.6 (similarity analysis), Section 5.7 (commitment tracking), and Section 6.2 (limitations). While each analysis adds value, the distributed treatment makes it difficult to form a unified assessment. A consolidated "Sycophancy Assessment" subsection would be more effective.

## 5. Ethical Compliance

**Rating: 5 (Excellent)**

The ethics statement (Section 7) is thorough and thoughtful, addressing four specific concerns including the risk of false authority, selective reporting, AI writing assistance, and computational costs. The AI involvement disclosure in the author footnote is transparent. The recommendation that outputs be characterized as "AI-assisted preliminary trade studies" rather than "AI-validated engineering decisions" reflects responsible framing.

The open-source release of all transcripts, code, and outputs is commendable and supports both reproducibility and accountability. The inclusion of endpoint identifiers, generation dates, temperature settings, and transcript checksums in the data availability statement exceeds typical standards.

The paper's most important ethical contribution may be the divergent views schema itself, which is explicitly designed to prevent the misuse scenario where AI consensus is selectively reported while disagreements are suppressed. This is a structural safeguard rather than merely a disclosure, and it represents thoughtful ethical design.

## 6. Scope & Referencing

**Rating: 4 (Good)**

The paper is well-positioned for IEEE Intelligent Systems, sitting at the intersection of multi-agent AI systems and engineering decision-making. The reference list is comprehensive and well-curated, spanning multi-agent LLM systems, expert consensus methods, engineering design methodology, and epistemology of disagreement. The inclusion of Christensen & Lackey (epistemology of disagreement) and Lakshminarayanan et al. (deep ensembles for uncertainty) demonstrates intellectual breadth beyond the immediate LLM literature.

Several relevant works appear to be missing. The paper does not cite recent work on LLM-based engineering design assistants (e.g., work on LLMs for requirements analysis or systems engineering). The connection to ensemble methods in machine learning could be developed further—the paper cites Lakshminarayanan et al. but does not engage with the broader ensemble diversity literature (e.g., negative correlation learning, diversity measures for ensembles). Work on structured argumentation frameworks (e.g., Dung's abstract argumentation, ASPIC+) is relevant to the divergent views schema but uncited.

The Sharma et al. [2024] sycophancy reference is well-chosen and directly relevant, but the paper could benefit from engaging with more recent work on LLM calibration and self-knowledge (beyond Kadavath et al., which is cited but not discussed in the text). The reference to Perez et al. [2022] appears in the bibliography but is not cited in the text body.

One scope concern: the paper's target journal is listed as IEEE Intelligent Systems, but the title mentions "Complex Engineering Decisions" and the application domain is space infrastructure. The paper would need to emphasize the AI/systems contribution over the domain application to fit the journal's scope, which it largely does, though the case study section is heavily domain-specific.

---

## Major Issues

1. **Insufficient statistical rigor for key claims.** The similarity analysis (Table 6) reports decreases across six metrics but provides no statistical tests (e.g., paired t-tests, Wilcoxon signed-rank tests, or bootstrap confidence intervals) for any of the reported differences. With $n = 6$ multi-round deliberations, some of these differences (e.g., heading Jaccard $\Delta = -0.001$) are likely not statistically distinguishable from zero. The paper's central anti-sycophancy argument rests on these metrics, so this is a critical gap. Similarly, the 85% winner stability from repeated trials lacks confidence intervals.

2. **Absence of controlled baselines.** The paper acknowledges this extensively but the absence remains a major limitation. The "reference observations" (Section 5.5) are confounded by prompt structure, output format, and sample size differences. Without at minimum a properly controlled aggregation-only baseline (same prompt structure, same output format, blinded expert evaluation), it is impossible to attribute any observed benefits to the deliberation mechanism rather than to additional compute, context, or prompt engineering. The validation roadmap (Table 9) is helpful but does not substitute for actual experiments.

3. **Inter-rater reliability is unestablished.** The divergent view categorization—a central contribution—was performed by system designers without formal inter-rater reliability metrics. The 81% initial agreement among three reviewers is reported but Cohen's $\kappa$ is not computed, and the reviewers are not independent of the system. The claim that "12 were confirmed as genuine engineering trade-offs through literature review" is only as strong as the categorization process, which is currently unvalidated. The coding manual in Supplementary Material S1 is a positive step but insufficient without actual independent coding.

4. **Single synthesizer introduces systematic bias.** Claude 4.6 serves as both the default synthesizer (Section 3.3) and the most frequent round winner (implied by the repeated trials data showing Claude winning in most trials). This creates a potential confound: the final conclusions may systematically reflect Claude's reasoning style and preferences. The paper acknowledges this as a threat to validity but does not test it. At minimum, a sensitivity analysis using each model as synthesizer for a subset of questions would address this concern.

## Minor Issues

1. **Abstract length.** At ~280 words, the abstract exceeds typical IEEE Intelligent Systems limits (~200 words). Consider tightening, particularly the repeated trials details which could be summarized more concisely.

2. **Eq. 1 notation.** The scoring formula uses $v_{ji}$ without explicitly defining the range. While the text states APPROVE=2, NEUTRAL=1, REJECT=0, the equation should include this: $v_{ji} \in \{0, 1, 2\}$.

3. **Perez et al. [2022] uncited.** Reference \cite{perez2022sycophancy} appears in the bibliography but is never cited in the text. Either cite it (likely in the sycophancy discussion) or remove it.

4. **Kadavath et al. [2022] uncited.** Similarly, \cite{kadavath2022language} appears in the bibliography but is not referenced in the text.

5. **Table 3 (convergence) formatting.** "Average approval rate" of 72.2% is reported without a confidence interval or standard deviation, unlike other metrics in the repeated trials table.

6. **Section 5.2, "162 individual votes."** The arithmetic should be verified: 16 questions × mean 2.3 rounds × 3 models × 3 votes per model ≈ 331 votes, not 162. If 162 refers to peer votes only (excluding self-votes), this should be clarified.

7. **"Frontier LLMs" definition.** The footnoted definition ("most capable commercially available models from distinct model families at the time of the study") is helpful but should appear in the main text rather than being implied.

8. **Figure overload.** Ten figures are referenced. Consider consolidating Figs. 7–9 (similarity analyses) into a single multi-panel figure, and Figs. 2–3 (convergence) similarly.

9. **Section 3.4 placement.** "Design Decisions and Rationale" reads as part of the methodology but includes empirical observations (e.g., "89\% versus 68\%" self-vote rates). Consider moving empirical content to Section 5.

10. **Typo/style.** "mfg." in the YAML listing (Listing 1) should be expanded to "manufacturing" for clarity in a formal publication.

## Overall Recommendation

**Major Revision**

This paper presents a genuinely novel and well-motivated methodology with a distinctive contribution in the divergent views schema. The writing quality is high, the self-awareness about limitations is exemplary, and the validation roadmap demonstrates mature thinking about what would constitute proper empirical validation. However, the paper in its current form makes empirical claims—particularly regarding sycophancy resistance—that are not adequately supported by statistical analysis. The absence of controlled baselines, formal inter-rater reliability, and statistical tests for the similarity analysis are significant gaps that prevent the paper from meeting the evidentiary standards expected for a top venue. The good news is that most of these issues are addressable: adding statistical tests to the similarity analysis, computing confidence intervals for repeated trials, conducting at least one properly controlled baseline experiment, and obtaining independent inter-rater reliability for the divergent view categorization would substantially strengthen the paper. The conceptual contribution is strong enough to warrant revision rather than rejection.

## Constructive Suggestions

1. **Add statistical tests to the similarity analysis.** For each metric in Table 6, report a paired test (or bootstrap confidence interval) across the $n = 6$ deliberations. If some differences are not significant, acknowledge this honestly—it would actually strengthen the paper's credibility. Consider reporting effect sizes (Cohen's $d$) alongside $p$-values.

2. **Conduct at least one properly controlled baseline before resubmission.** The blind deliberation experiment (Experiment 3 in Table 9) would be the highest-impact addition, as it directly addresses the sycophancy concern that dominates the discussion. Alternatively, a controlled aggregation-only baseline with harmonized prompts and blinded evaluation would establish whether the deliberation mechanism adds value beyond simple aggregation. The estimated costs ($80–$320) suggest this is feasible.

3. **Obtain independent inter-rater reliability for divergent view categorization.** Recruit 2–3 coders who are not system designers, provide them with the coding manual (Supplementary Material S1), and report Cohen's $\kappa$ or Krippendorff's $\alpha$. This is essential for the paper's central claim that 12 divergent views represent "genuine engineering trade-offs."

4. **Consolidate the sycophancy analysis into a single coherent section.** Currently, evidence for and against sycophancy is distributed across Sections 5.2, 5.6, 5.7, and 6.2. A unified treatment would be more compelling and easier to evaluate. Structure it as: (a) the concern, (b) evidence from voting patterns, (c) evidence from textual similarity, (d) evidence from commitment tracking, (e) remaining limitations and planned experiments.

5. **Test synthesizer sensitivity.** Run at least 4 questions through synthesis with each of the three models as synthesizer and report whether conclusions differ systematically. This is low-cost and would address a significant confound. If conclusions are robust to synthesizer choice, this strengthens the paper; if not, it identifies an important design parameter.