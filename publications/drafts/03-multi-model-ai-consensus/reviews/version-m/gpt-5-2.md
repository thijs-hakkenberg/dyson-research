---
paper: "03-multi-model-ai-consensus"
version: "m"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-03-19"
recommendation: "Major Revision"
---

## 1. Significance & Novelty  
**Rating: 4 (Good)**  
The manuscript’s strongest and most novel contribution remains the **divergent views schema** as a first-class, machine-readable design rationale artifact with attribution, evidence, and resolution status. For aerospace/space systems engineering, this is plausibly impactful because it aligns with traceability and trade-space rationale practices (QOC/DRL-like) while leveraging heterogeneous frontier LLMs as a “computational Delphi.” The paper is also timely in addressing multi-agent LLM deliberation beyond “debate for factuality” toward **ill-posed engineering trade studies**.

That said, the empirical claims are appropriately tempered in several places, but the paper still risks being read as implying decision-quality improvement without expert adjudication. The novelty is methodological/artifactual more than performance-based, and the manuscript should keep foregrounding that.

---

## 2. Methodological Soundness  
**Rating: 3 (Adequate)**  
The protocol is described in enough detail to be reproducible at a high level (round phases, scoring, termination rules, artifacts, temperature, self-vote weight). The addition of **controlled baselines (aggregation-only, self-refinement)** is a meaningful improvement over prior “absence of baselines” concerns and is directionally the right experimental move.

However, several methodological weaknesses remain material for a top-tier aerospace/space journal standard of evidence:

- The baselines are **structure-matched but not outcome-validated** (no expert scoring, no correctness/utility metric, no downstream design impact measure).  
- The winner-hidden ablation is **confounded** (Gemini failures → effectively two-model deliberations), limiting interpretability for anchoring/herding.  
- Divergent view extraction depends on a **single annotator** correcting an LLM-generated candidate list; reliability is acknowledged but not addressed empirically.  
- Head truncation is a nontrivial uncontrolled factor that can affect convergence, similarity, and “framework adoption.”

---

## 3. Validity & Logic  
**Rating: 3 (Adequate)**  
Internal logic is mostly coherent, and the manuscript does a better job than many LLM-systems papers in explicitly separating *descriptive characterization* from *causal inference*. The reframing of similarity analysis as descriptive is appropriate given the small \(n\) and the inability of lexical metrics to disambiguate convergence vs anchoring vs herding.

Key validity concerns:

- **Construct validity**: the “commitment” extraction heuristic (recommendation keywords) is plausible but under-specified and may miss domain-specific commitments expressed without those tokens (e.g., “baseline,” “shall,” “assume,” “size to,” “allocate”).  
- **Causal claims**: some language still implicitly links observed patterns to “genuine refinement” more strongly than warranted (even with caveats). The evidence supports “consistent with” but not “indicative of,” especially since similarity decreases (including decision-sentence similarity) could also reflect stylistic divergence rather than substantive refinement.  
- **External validity**: the application domain (Dyson swarm) is highly speculative; while that is acceptable for methodology demonstration, it limits claims about aerospace engineering generality unless tied to more conventional spacecraft systems trade studies.

---

## 4. Clarity & Structure  
**Rating: 4 (Good)**  
The manuscript is well organized: architecture → protocol → artifacts → application → baselines/ablations → limitations. The explicit “threats to validity” style is helpful. The definitions paragraph (sycophancy/anchoring/convergence/herding) is a net improvement and mostly precise.

Two clarity issues remain:

- Some metrics are reported without sufficient operational detail (e.g., “technical parameter Jaccard”: what extraction rules? units normalization? handling of ranges/uncertainty?).  
- The paper sometimes mixes levels: “illustrative rather than evaluative” is stated, but later sections read like quasi-evaluation (e.g., “REJECT justifications identified genuine technical issues” without an independent rubric).

---

## 5. Ethical Compliance  
**Rating: 4 (Good)**  
Strong AI disclosure, clear statement of non-human-subjects, and explicit warning that “LLM consensus is not truth.” Data availability and open-source release are positives.

Remaining ethical/reproducibility gaps:

- “Frontier model” endpoints via Databricks are inherently non-stationary; the paper acknowledges ambiguity but should provide **stronger provenance controls** (exact request/response logs, system prompts, full prompt templates, and ideally a containerized orchestrator with pinned dependencies).  
- If any transcripts include sensitive operational/security-relevant content (less likely here), a redaction policy should be stated.

---

## 6. Scope & Referencing  
**Rating: 3 (Adequate)**  
Citations cover multi-agent LLM debate, Delphi, design rationale, and sycophancy reasonably. For an aerospace engineering journal, the engineering decision-analysis references (Keeney/Raiffa, Pugh, AHP) are appropriate, but the paper would benefit from deeper linkage to **aerospace trade study practice** (e.g., NASA/ESA conceptual design review processes, MBSE/SE rationale capture, uncertainty quantification in early-phase design).

Also, several cited LLM works are arXiv-era and not necessarily archival; that’s common in this area but may need balancing with more peer-reviewed systems/SE literature.

---

# 7. Experimental Design & Baselines Adequacy  
**Rating: 3 (Adequate)**  
Section 5.5 is a substantive improvement: it directly addresses the baseline gap by comparing deliberation to (i) aggregation-only and (ii) self-refinement under prompt-matched conditions. The conclusion—“quantitative output structure comparable; distinctive value is divergent views + peer evaluation”—is appropriately cautious and, importantly, does *not* overclaim performance gains.

However, the baselines are still **not controlled for key confounds**:

- Deliberation has multiple rounds and winner visibility; aggregation-only is single-shot; self-refinement has multiple rounds but no cross-model exposure. These are fine as contrasts, but the paper needs a clearer statement of what is being held constant vs varied (a small factorial table would help).  
- The metrics used (“key points,” “actions,” word count) are weak proxies for engineering quality. They can support claims about output *formatting/structure* but not decision usefulness.

---

# 8. Divergent Views Schema & Evidence of Utility  
**Rating: 4 (Good)**  
The divergent views schema remains the manuscript’s strongest contribution. The paper is convincing that deliberation produces a *curated* set of persistent disagreements, while aggregation yields a broader enumeration. The “aggregation extracted more topics, higher fraction ‘genuine trade-offs’” result is interesting and the interpretation (enumeration vs curation) is plausible.

But the evidence for “utility” is still incomplete:

- The “12 confirmed trade-offs” literature check is not described with enough rigor (search protocol, inclusion criteria, how “confirmed” is decided).  
- Single-annotator classification is a major limitation because the central contribution is an artifact whose value depends on reliable extraction and categorization.

---

# 9. Sycophancy/Anchoring/Herding Analysis  
**Rating: 3 (Adequate)**  
**Definitions paragraph precision:**  
- *Sycophancy* as “agreement to please/conform to evaluator preferences independent of evidence quality” is acceptable, though in this setting the “evaluator” is another model and the “preference” is inferred from winner status—this should be made explicit because it differs from user-sycophancy in Sharma/Perez.  
- *Anchoring* is correctly framed as disproportionate influence of early/prominent information.  
- *Convergence* is reasonably defined as evidence-responsive agreement.  
- *Herding* is framed as convergence driven by observing others rather than independent evaluation; operationalizing via winner-visibility manipulation is reasonable.

**Similarity reframing:** Calling the similarity analysis “descriptive characterization” is appropriate and a good correction. The manuscript also correctly notes that lexical similarity cannot disambiguate constructs.

Main concern: the current empirical package (decreasing similarity + commitment adoption + small ablation) is **not yet sufficient** to support even moderate claims about anchoring vs sycophancy vs genuine refinement. The paper mostly stays cautious, but a few phrases (“consistent with genuine refinement”) should be tightened further or paired with explicit alternative explanations.

---

# 10. Reproducibility, Reliability & Statistical Treatment  
**Rating: 3 (Adequate)**  
Repeated trials (n=5 on 4 questions) are a meaningful step toward reliability characterization; reporting Wilson CI and entropy is good practice. The paper is honest about limited power (n=6 for similarity deltas) and reports bootstrap CIs and Wilcoxon tests.

Remaining issues:

- No seed control is fine for “operational reliability,” but for scientific reproducibility it would help to report whether the API supports deterministic settings and whether they were attempted.  
- The winner-stability metric conflates “proposal identity” with “model identity” (it reads like “which model’s proposal won”). If the orchestrator labels proposals by model, stability may reflect model-specific style/vote dynamics rather than content robustness. Consider reporting stability at multiple levels (model-winner vs content-cluster-winner).  
- The Monte Carlo/reliability framing could be strengthened: currently it’s “repeated trials,” but not tied to a reliability model (e.g., variance decomposition across question/model/round).

---

# Major Issues

1. **Winner-hidden ablation is confounded (effectively 2-model) and cannot support anchoring/herding claims.**  
   - **Why it matters:** The ablation is the only experimental lever aimed at separating anchoring/herding from genuine convergence. With one model missing, voting dynamics, diversity, and tie-breaking behavior change qualitatively. Any observed change in rounds/stability may be due to reduced panel size rather than winner visibility.  
   - **Remedy:** Re-run winner-hidden across the same 4 questions (or ideally all 16) with all three models functioning, or replace Gemini with a stable third model family for the ablation. Report results as a proper comparison: 3-model shown vs 3-model hidden, same questions, multiple trials per question.

2. **Central contribution (divergent views) lacks independent reliability evidence; single-annotator coding is a critical gap.**  
   - **Why it matters:** The paper’s key artifact is only as credible as its extraction and categorization reliability. Single-annotator correction introduces confirmation bias and threatens replicability.  
   - **Remedy:** Add at least two independent human coders for (a) topic extraction correctness (are the topics real/persistent?), (b) attribution correctness, and (c) category assignment (trade-off vs knowledge gap vs value-laden). Report Cohen’s \(\kappa\)/Krippendorff’s \(\alpha\). If full 16 is too heavy, do a preregistered subset (e.g., 6 questions stratified) but include it in this version if possible.

3. **Baseline experiments do not evaluate engineering decision quality; current metrics are weak proxies.**  
   - **Why it matters:** For an aerospace engineering journal, readers will ask whether deliberation improves trade study usefulness, not whether it produces similar counts of bullet points. The baselines now exist, but they don’t adjudicate value.  
   - **Remedy:** Add an expert evaluation study (even small): blinded pairwise ranking of outputs (deliberation vs aggregation vs self-refine) on criteria such as correctness, completeness, traceability, actionable recommendations, and identification of key trade-offs/risks. If expert recruitment is hard, use a structured rubric and at least 3 raters with relevant background; report inter-rater agreement.

4. **Operational definitions for similarity metrics and “technical parameter Jaccard” are under-specified.**  
   - **Why it matters:** The surprising result that *decision-level similarity decreases* hinges on extraction quality. Without clear extraction/normalization rules, the metric may be measuring noise (formatting differences, unit changes, rounding) rather than substantive divergence.  
   - **Remedy:** Provide a precise algorithm (regex/NER rules, unit normalization, handling of ranges, deduplication, synonym mapping). Include an error analysis on a small sample (precision/recall of parameter extraction).

5. **Potential truncation and prompt-conditioning effects are not controlled and may drive observed dynamics (framework adoption, convergence speed).**  
   - **Why it matters:** Head truncation plus winner visibility can mechanically increase apparent consensus or shift what information is salient. This threatens internal validity of convergence/anchoring interpretations.  
   - **Remedy:** Add at least one controlled comparison: head-truncation vs summary-truncation (or no truncation on a subset) and report impact on rounds, winner stability, and divergent views. At minimum, quantify how often truncation occurred and how many tokens were removed by round/model.

6. **“12 confirmed trade-offs through literature review” is not methodologically transparent.**  
   - **Why it matters:** This statistic is used to argue that divergent views capture real engineering trade-offs. Without a documented review protocol, it reads as subjective.  
   - **Remedy:** Provide a short methods subsection: databases used, search strings, inclusion/exclusion criteria, what qualifies as “confirmed,” and whether confirmation required multiple sources. Consider adding a supplementary table with citations per confirmed trade-off.

---

# Minor Issues

1. **Terminology drift:** “frontier LLMs” is defined, but for aerospace audiences consider also “commercial general-purpose LLMs from distinct vendors” to avoid implying technical superiority relevant to engineering truth.  
2. **Voting math clarity:** Eq. (1) uses \(v_{ji}\) but the text says JSON justifications—ensure consistency (JSON vs YAML vs structured fields).  
3. **Tie-breaking rule:** “persistent ties favor the prior-round winner” can introduce path dependence; note this explicitly as an anchoring mechanism and quantify how often ties occurred.  
4. **“70% framework adoption” needs operational definition:** what constitutes adopting a framework? Provide annotation rules and examples.  
5. **Gemini parsing failures:** clarify whether failures were due to model behavior, prompt format, or orchestration; and whether retries were attempted.  
6. **Figures:** several figures are referenced but not described in enough detail for standalone interpretation (axes labels/units, sample sizes).  
7. **Data availability:** provide a permanent DOI (Zenodo) in addition to a project website, if possible, for archival stability.

---

## Overall Recommendation  
**Recommendation:** **Major Revision**

The manuscript is promising and increasingly well-scoped: it presents a reproducible deliberation protocol and, importantly, a genuinely useful artifact (divergent views schema) that aligns with engineering rationale capture. Version M makes clear progress by adding controlled baselines and reframing similarity analysis as descriptive rather than causal. The writing is generally strong and the limitations are unusually candid for this area.

The remaining blockers for a top-tier aerospace/space journal are primarily **evidence and validity**: (i) the anchoring/herding ablation is confounded and cannot support the central behavioral interpretation; (ii) the divergent views extraction/categorization—your strongest contribution—still lacks independent reliability measurement; and (iii) baseline comparisons do not yet assess engineering decision quality, only output structure. Addressing these with a modest but well-designed expert evaluation and inter-rater reliability study would substantially elevate the paper from “interesting methodology demo” to “credible engineering decision-support method.”

---

## Constructive Suggestions (ordered by impact)

1. **Fix the winner-hidden ablation and scale it:** run shown vs hidden with 3 functioning models, multiple trials per question, and report effect sizes with uncertainty.  
2. **Add independent coding for divergent views:** at least 2 additional coders; report \(\kappa\)/\(\alpha\); include attribution accuracy checks.  
3. **Add blinded expert evaluation across the three conditions (deliberation/aggregation/self-refine):** even 6 questions × 3 outputs × 3 raters can be informative if well-designed.  
4. **Strengthen operational definitions and extraction algorithms:** especially “framework adoption,” “commitments,” and “technical parameter” extraction; include an error analysis.  
5. **Quantify truncation prevalence and impact:** report how often truncation occurred and perform a small controlled truncation strategy comparison.  
6. **Tighten claims language further:** wherever “consistent with genuine refinement” appears, pair with explicit alternative explanations and avoid implying mechanism identification without manipulation.  
7. **Improve aerospace engineering contextualization:** connect to established trade study/SE practices (MBSE rationale, design review artifacts, uncertainty management) and clarify where this method fits in a conventional project lifecycle.

If the authors address items (1)–(3) convincingly, the paper would be much closer to publishable in a top-tier aerospace engineering venue, with the divergent views schema as a clear standout contribution.