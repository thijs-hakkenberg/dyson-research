---
paper: "03-multi-model-ai-consensus"
version: "e"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-02-23"
recommendation: "Unknown"
---

## 1. Significance & Novelty — **Rating: 4/5 (Good)**

The manuscript addresses a real and under-served gap: how to use *multiple* LLMs as a structured panel for engineering trade studies, with explicit attention to adversarial review, termination rules, and—most notably—preservation of disagreements as first-class artifacts. The “divergent views” output (Section 3.5) is the clearest novel contribution relative to most multi-agent/debate work, which typically optimizes for a single best answer rather than durable design rationale. Positioning disagreement capture as the core deliverable is also well-aligned with design rationale traditions (QOC/DRL) and with engineering practice, where unresolved trade-offs often matter more than a synthesized narrative.

The paper is also timely: multi-agent LLM systems are proliferating, but engineering decision support has distinct requirements (no single ground truth; multi-criteria trade-offs; traceability). The protocol-level specificity (round structure, scoring rule in Eq. 1, termination conditions, configuration table) is a meaningful step toward reproducible “methods papers” in this space.

That said, novelty is partly *method integration* rather than a fundamentally new algorithmic result. Many components resemble known patterns (Delphi-like iteration, LLM-as-judge voting, debate-inspired critique). The manuscript would read as more strongly novel if it articulated a sharper conceptual differentiation from (i) Delphi/NGT, (ii) debate, and (iii) “ensemble + synthesis” beyond the divergent-view schema—e.g., what properties the voting/termination rules guarantee or empirically tend to yield (stability, diversity retention, failure detection). As written, the novelty claim is credible, but it would benefit from more explicit “design principles” and/or hypotheses that this protocol uniquely enables.

---

## 2. Methodological Soundness — **Rating: 3/5 (Adequate)**

The methodology is described with commendable operational detail: system layers (Section 3.1), explicit scoring rule (Eq. 1), tie-breaking, termination logic, and key configuration parameters (Table 1). The authors also appropriately flag uncontrolled variables (head truncation; fixed temperature; winner visibility) and provide a concrete validation roadmap (Section 6.2), which is unusually candid and helpful for a systems paper.

However, several methodological choices are currently under-justified or risk being “baked-in confounds” that substantially affect observed convergence and disagreement yield. The biggest are: (a) revealing the winner identity and score in later rounds (Section 3.2.1) which plausibly induces anchoring/sycophancy; (b) head truncation to 1,000 words, which preferentially preserves framing over caveats/risks; (c) using a single synthesizer model (Section 3.3) which may systematically shape what is treated as “resolved” vs “unresolved”; and (d) the empirically chosen self-vote weight of 0.5 without a principled derivation or pre-registered selection. You do examine winner sensitivity to self-vote weight post hoc (Section 5.4), which helps, but comparable sensitivity analyses for winner visibility and truncation are likely more consequential.

Reproducibility is partially addressed via “archived transcripts” and open-source code, but the paper should specify enough to reproduce *the same* experimental conditions: exact prompts/templates, system messages, parsing rules, retry logic, and the precise JSON schema expected. Right now, key elements are described narratively (e.g., “structured JSON response format” in Section 3.2.2) without the schema in the paper/appendix. Given that 8.3% of Gemini voting instances malformed JSON (Section 5.3), the parsing/repair behavior is not incidental—it is part of the method and should be fully specified.

---

## 3. Validity & Logic — **Rating: 3/5 (Adequate)**

The manuscript is generally careful not to over-claim. The abstract and Section 5 explicitly label the results “illustrative rather than evaluative,” and Section 6.2 lays out the controlled experiments required to establish causal benefit. The discussion of epistemological ambiguity of LLM consensus (Section 6.6) is unusually strong for an applied systems paper, and the threats-to-validity section is concrete and directionally reasoned (Section 6.5).

Still, some interpretations drift toward “design validation” without sufficient separation between (i) properties mechanically induced by the protocol and (ii) substantive improvements in engineering quality. For example, the relationship between approval rate and rounds-to-conclude (Section 5.1; Fig. 2) is acknowledged as partly mechanical, but the narrative still risks being read as an empirical regularity about “question difficulty.” Similarly, the statement that “iterative deliberation may enrich proposals” (Abstract; Table 9) is plausible but currently confounded by increased context, extra tokens, and winner anchoring; the paper notes this, yet the within-study comparisons (Table 9) are presented with quasi-quantitative metrics (e.g., “0/20 contradictions”) without describing the coding protocol sufficiently to judge reliability.

The divergent-view validation is a promising step (Section 5.5), but it also needs tighter methodological framing to support the conclusion that the schema “captures substantive engineering disagreements.” The review team are system designers; the literature search is “targeted” but not described in enough detail in the paper; and the mapping from “divergent topic” to the four categories is inherently subjective. Reporting Cohen’s κ/α is noted as missing, but more importantly: you need to clarify whether the unit of analysis is a *topic*, a *pair of positions*, or a *claim*, and how “confirmed by literature” was operationalized (e.g., what counts as evidence for both sides, how contradictions were handled, how hallucinated citations were treated). Without that, the “12/47 genuine trade-offs” number reads more definitive than the underlying procedure supports.

---

## 4. Clarity & Structure — **Rating: 4/5 (Good)**

The paper is well organized and reads like a methods + case-study systems paper: Introduction → Related Work → Methodology → Application Domain → Results → Discussion/Limitations/Ethics. The abstract is accurate in its caveats and in highlighting disagreement preservation as the key contribution. The termination logic, scoring, and protocol phases are described clearly enough for a reader to implement a similar system.

Figures and tables appear thoughtfully chosen (architecture diagram; convergence scatter; vote distributions; parameter sensitivity). The inclusion of the YAML schema (Listing 1) is particularly helpful; it concretizes what “divergent views” means and makes the contribution legible. The discussion sections (threats to validity; epistemology) are unusually clear and appropriately cautious.

Clarity issues are mainly about *operational specificity* and *metric definitions*. Several quantitative claims rely on coding/heuristics (trade-off counts; contradictions; “framework adoption rate”) without enough detail to replicate. Also, the post-hoc aggregation comparison (Section 5.8) is potentially confusing because the “aggregation-only” condition is prompted to produce a Trade-offs section, while the deliberation conclusion is not—this is acknowledged, but the table (Table 8) still invites naive interpretation. Consider either (i) harmonizing the output format for both conditions, or (ii) moving the numeric comparison to an appendix and keeping the main text qualitative.

---

## 5. Ethical Compliance — **Rating: 4/5 (Good)**

Disclosure is strong and unusually explicit: the author footnote, the Ethics Statement (Section 7), and repeated reminders that outputs are “AI-assisted preliminary trade studies” rather than validated decisions. The manuscript also acknowledges risks of misuse (selective reporting of consensus) and positions the divergent-view schema as a partial mitigation. The energy/cost discussion is brief but appropriate for the scale.

Two ethics-related gaps remain. First, there is a potential conflict-of-interest/positionality issue: the paper evaluates a methodology used by the same team to advance their own project’s engineering specifications (Section 4). That is not inherently problematic, but it should be framed explicitly as an “internal methods report / design science artifact” with clear boundaries on claims, and ideally include a plan for independent replication or third-party evaluation (you gesture at this in Section 6.2, but it could be strengthened). Second, governance questions (Section 5.2, 5.5) can have real-world normative implications; the paper acknowledges “value disagreement,” but it would benefit from a clearer statement about how such outputs should (and should not) be used in organizational decision-making, especially given the risk of laundering normative choices through “AI consensus.”

---

## 6. Scope & Referencing — **Rating: 3/5 (Adequate)**

The paper fits well for IEEE Intelligent Systems / design science / AI systems venues; it is less obviously a fit for a space systems *technical* journal because it does not validate engineering designs, but rather validates a deliberation protocol. The manuscript generally cites appropriate foundational work: Delphi, groupthink, AHP/MAUT, debate, AutoGen, LLM-as-judge, design rationale, swarm robotics. The mix is reasonable.

Referencing has two weaknesses. First, several citations are somewhat mismatched or dated for the specific claims being supported (e.g., “NASA mission studies reach different conclusions…” is plausible, but the cited NASA SE handbook is not a mission power trade study; similarly “Autodesk generative design overview” is a weak scholarly anchor). Second, the multi-agent LLM literature has expanded rapidly; you cite major early entries, but there are likely more directly relevant works on agentic workflows, self-consistency/ensembling, and structured critique (including more recent “multi-agent for planning/engineering” papers) that would strengthen the positioning. The paper also leans on arXiv preprints; that is acceptable in this area, but a few peer-reviewed anchors for LLM evaluation reliability and for ensemble methods would improve credibility.

Finally, for an engineering-methods paper, you may want to cite established trade study/process standards more directly (e.g., NASA/SP trade study guidance beyond the SE handbook; INCOSE guidance is cited but not used substantively). This would help readers see precisely how your outputs map to conventional trade study artifacts (alternatives, criteria, weights, decision rationale, sensitivity).

---

## Major Issues

1. **Winner visibility / anchoring is a first-order confound that undermines interpretation of “deliberation.”**  
   In Section 3.2.1 you reveal the winning proposal identity and score in subsequent rounds. Combined with the observed 70% “framework adoption” (Section 6.4), this makes it unclear whether improvements are due to adversarial evaluation or to a strong anchoring signal. This is not just a “future work” concern: it affects the internal validity of essentially all descriptive findings about convergence. At minimum, the paper should (i) treat current results as “informed-iteration deliberation,” not generic deliberation, and (ii) include an ablation on winner visibility for at least a subset of questions.

2. **Insufficient specification of prompts, schemas, and parsing behavior for reproducibility.**  
   The method depends critically on prompt templates, the JSON voting schema, and the error-handling policy when JSON is malformed (Section 5.3). Without including these (appendix or repository link with immutable commit hash), the paper is not reproducible in the “independent reproduction” sense claimed in the Introduction/Conclusion. Provide the exact system prompt, user prompt template per phase, the JSON schema, and the parsing/repair algorithm.

3. **Divergent-view extraction procedure is underspecified and risks subjectivity.**  
   Section 3.5 provides the schema, but not the extraction method: Who/what extracts topics (a model? rules? humans)? When is a “topic” created vs merged? How are positions deduplicated across rounds? Without this, “47 divergent topics” is not an interpretable metric. If extraction is model-assisted, you must specify the extractor prompt and how you prevent it from hallucinating disagreements.

4. **Quantitative comparisons rely on heuristics/coding without enough methodological detail.**  
   Examples: “internal contradictions” (Table 9), “framework adoption rate” (Section 6.4), and trade-off counts in aggregation vs deliberation (Section 5.8). These are central to the narrative that deliberation yields richer outputs, but the coding protocols are not described sufficiently to assess reliability or bias. You should either (i) formalize these as a small annotated study with clear labeling rules and reliability stats, or (ii) downgrade them to qualitative observations.

---

## Minor Issues

- **Eq. (1) scoring range and threshold clarity.** With 3 models and self-vote at 0.5, the maximum score is \(2 + 2 + 1 = 5\). You use convergence criterion “score ≥ 5.0” (Termination condition 3). That implies *perfect* peer approval and self-approval. Explicitly state the maximum and interpretability of that threshold (Section 3.2.3). As written, some readers may not immediately see why 5.0 is special.

- **“Judging LLM-as-a-judge with MT-Bench…” citation year mismatch.** The bib entry says NeurIPS 2023 but is cited as 2024 in text in places (Related Work). Ensure consistency.

- **Aggregation comparison (Section 5.8) is structurally biased by prompt format.** You acknowledge this, but Table 8 still presents means as if comparable. Consider revising the table or adding a “not directly comparable” note in the caption, or harmonize prompts and rerun.

- **Model versioning and naming.** The footnote in Section 3.1 is good, but consider adding a repository commit hash and timestamps for each run; “January–February 2026” is not enough for forensic reproducibility.

- **Ethics statement: open-source release claim.** Provide the license name (e.g., Apache-2.0/MIT) and a permanent URL (tagged release or DOI via Zenodo), not just the project homepage.

- **Table 6 “validated divergent views” includes “Governance longevity” as “genuine engineering trade-off.”** That seems closer to “value disagreement” per your own category definitions unless tightly framed as institutional design under constraints. Clarify why it is not categorized as value-laden, or adjust.

---

## Overall Recommendation — **Major Revision**

The paper is a strong, timely methods contribution with a clear potential impact, especially via the divergent-views artifact and the protocol-level specification. However, several core components are under-specified (prompt/schema/parsing; divergent-view extraction), and the current illustrative results are heavily confounded by winner visibility/anchoring and by heuristic-coded metrics presented with quasi-quantitative authority. Addressing these issues does not require a full-scale controlled study, but it *does* require tightening the methodological specification and either adding small ablations (winner visibility; extraction reliability) or reframing claims to match what the current evidence supports.

---

## Constructive Suggestions

1. **Add a “Protocol Specification Appendix” (or main-text subsection) with exact artifacts.**  
   Include: system prompt(s), per-phase user prompt templates, the exact JSON schema for votes/termination, parsing/repair rules, and the divergent-view extraction prompt (if model-assisted). Provide an immutable repository reference (commit hash + archived release).

2. **Ablate winner visibility on a small subset (e.g., 4 questions) and report effects.**  
   Run “winner hidden” vs “winner shown” (keeping everything else constant) to quantify anchoring’s effect on convergence rounds, framework adoption, and divergent-topic yield. Even a small ablation would substantially strengthen internal validity.

3. **Specify and validate the divergent-view extraction process.**  
   Define: unit of analysis (“topic”), merge/split rules, and whether extraction is done by humans, an LLM, or hybrid. If LLM-assisted, report an error analysis (false positives/negatives) on a small manually annotated subset.

4. **Replace or formalize heuristic metrics used for quality claims.**  
   For “contradictions,” “trade-offs per proposal,” and “framework adoption,” provide explicit labeling rubrics and at least basic inter-rater reliability on a subset. Alternatively, demote these to qualitative observations and avoid precise counts.

5. **Reframe the aggregation-only comparison to be format-controlled.**  
   Either rerun the deliberation synthesizer with the same required section headings as aggregation-only, or rerun aggregation-only without an explicit “Trade-offs” section request. Then compare like-with-like (or move the current comparison to an appendix as an illustrative artifact rather than a metric).