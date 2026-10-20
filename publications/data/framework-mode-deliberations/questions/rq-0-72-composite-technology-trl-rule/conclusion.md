---
questionId: "rq-0-72"
questionSlug: "composite-technology-trl-rule"
type: "discussion-conclusion"
generatedBy: "gpt-6-1-sol"
generated: "2026-10-17"
framework: "18f503fe4ec6"
roundCount: 1
terminationReason: "unanimous-conclude"
---

## Summary

Claude Opus 5.5 and Gemini 3.1 Pro recommended combining a weakest-critical-function bound with an integration assessment. GPT-6.1 Sol initially recommended configuration-specific integration assessment without automatically inheriting published component ratings, while treating unresolved critical deficiencies as binding blockers. **In the final votes, all three models approved Claude’s bounded-integration proposal**, including its provision that applicable integrated-test evidence updates critical-function sub-ratings before the bound is applied.

The panel therefore converged on a proposed rule: the headline must reflect demonstrated integration maturity and must not conceal an immature critical function. All three rejected averaging and leaving the reporting convention unresolved. Claude’s approved proposal additionally sets a TRL 4 ceiling without a tested integrated article. GPT’s own response challenged a blanket ceiling unless the assessment boundary and required article are properly specified; the votes did not separately resolve that implementation detail.

Claude and GPT both identified assessor reproducibility as unproven and recommended calibration. GPT explicitly preserved T26’s **TRL 3, with TRL 4 conditional**; Claude requested verification against its underlying evidence. Gemini’s claim that the hybrid rule retroactively justified T26 was challenged by both other models as unsupported.

## Decision record

### Converged proposal: bounded integration assessment

**Models:** Claude Opus 5.5 proposed it; Gemini 3.1 Pro and GPT-6.1 Sol approved it in the final votes.

> **Y-statement:** In the context of a Phase 0 TRL baseline feeding the irreversible, no-waiver KDP-0B gate, facing a choice between weakest-critical-part capping and integration assessment, we chose a bounded integration assessment: applicable critical-function sub-ratings and integration-demonstration requirements bound the headline, while documented integration assessment sets it at or below those bounds, to achieve defensible readiness claims that expose both component and integration deficiencies, accepting greater assessment effort and residual assessor judgment.

**Warrant — Claude, supported by Gemini and GPT’s approval:** A weakest-critical-function rating is an upper bound, not a sufficient estimate of composite maturity; integration introduces requirements that constituent ratings alone do not demonstrate.

**Qualifier — Claude, expressly supported by GPT’s vote:** Integrated testing may update a critical function’s sub-rating. The bound is applied **after** that evidence attribution, so stale labels do not impose artificial limits.

**Accepted downside — Claude; consistent with Gemini and GPT:** More documentation, interface scrutiny and assessment effort. Claude additionally accepted possible conservative under-rating and acknowledged that reproducibility had not been demonstrated.

### Proposed rule text

The following condenses Claude’s approved proposal:

- A composite headline shall not exceed the lowest applicable critical-function sub-rating, after incorporating applicable integrated-test evidence.
- The headline shall not exceed TRL 4 without a tested integrated article of the rated configuration.
- Within those bounds, assess configuration match, interface coverage, tested operating envelope, coupled-load fidelity and anomaly closure. Any reduction below the bound requires a named finding.
- Do not average, weight or multiply constituent TRLs.
- Publish the configuration, critical sub-ratings and evidence, integration findings, binding constraint and upgrade conditions.
- At KDP-0B, project-ending composites require headline TRL 6 or above, critical sub-ratings of 6 or above, and an integrated article matching the committed configuration, without waivers.

**Implementation reservation — GPT’s original response:** Article requirements must follow the claimed level and assessment boundary rather than an arbitrary whole-system boundary. GPT also allowed explicit reconciliation of a lower constituent rating through a justified scope distinction, provided no real dependency is excluded.

## Decision-quality audit

### Round 1 — Claude Opus 5.5 response

- **Weakest link named in votes:** Claude and GPT named **information**; Gemini named none. All three approved.
- **Missing or unsupported Scaffold elements:** Claude identified unverified T26 sub-rating details and an absence of calibration evidence for assessor reproducibility. GPT’s approval likewise identified reproducibility as unproven.
- **Trade-off rather than factual dispute:** Claude identified auditability versus integration fidelity, and conservative under-rating versus false readiness claims. Claude treated D-02 as favouring protection against false readiness at KDP-0B.

### Round 1 — Gemini 3.1 Pro response

- **Weakest link named in votes:** Claude named **alternatives** and rejected; Gemini and GPT named **reasoning** and voted neutral.
- **Missing or unsupported Scaffold elements:** All three voters noted that Gemini selected a hybrid rule that had not appeared as an evaluated alternative. Claude also criticised the weighting basis, lack of aggregation and failure to separate likelihood from confidence. GPT challenged the claim of “absolute gate integrity”; Claude and GPT challenged the asserted retrospective justification of T26.
- **Trade-off rather than factual dispute:** Gemini framed mechanical strictness versus engineering accuracy as the central owner-value choice.

### Round 1 — GPT-6.1 Sol response

- **Weakest link named in votes:** Claude named **reasoning** and voted neutral; GPT named **information** and approved; Gemini named none and approved.
- **Missing or unsupported Scaffold elements:** Claude challenged the maximum false-claim-prevention score because “justified scope distinction” could become an escape hatch. Claude also objected that preserving T26 mixed continuity with technical requirements. GPT acknowledged that consistency and assessment-cost benefits remained prospective.
- **Trade-off rather than factual dispute:** GPT identified consistency versus assessment effort, conservatism versus useful maturity information, and breadth versus depth of early testing. Claude’s concern about scope reconciliation reflects a different tolerance for assessor discretion at a one-way gate.

## Key Points

- **Minimum alone is insufficient:** Claude and Gemini said mature components can still form an immature integration; GPT likewise required direct integration assessment.
- **Integration success alone is insufficient:** All three required unresolved critical functions to block unsupported headline claims.
- **Evidence attribution bridges much of the split:** Claude’s update-before-capping provision was explicitly endorsed by GPT in its approval vote.
- **The null option was rejected:** All three opposed retaining incompatible conventions and relying on case-by-case owner adjudication.
- **Reporting must expose the basis:** Claude and GPT requested configuration-specific evidence and blockers; Gemini requested publication of integration, weakest-critical and headline ratings.
- **T26 does not settle the general rule:** Claude treated compatibility as unverified; GPT preserved the ruling without retrospective reinterpretation. Gemini’s stronger compatibility claim was challenged.

## Unresolved Questions

1. **Assessment boundary and article definition:** Claude proposed an article implementing every critical function and relevant coupled interfaces; GPT cautioned against requiring an arbitrarily broad whole-system article.
2. **Scope reconciliation:** GPT allowed justified distinctions between constituent and composite claims; Claude’s critique asked how that avoids becoming a gate escape hatch.
3. **Criticality:** Claude and Gemini identified the definition of “critical” as decisive; GPT also required coverage of critical interfaces and actual dependencies.
4. **Reproducibility:** Claude and GPT acknowledged that independent assessors’ consistency remains untested.
5. **T26 evidence:** Claude requested verification of its sub-ratings and conditional upgrade basis; GPT requested precise recording of the evidence needed for TRL 4.
6. **Review authority:** Claude left open whether downward integration findings require owner sign-off or documented assessor findings alone.

## Recommended Actions

1. **Put the bounded-integration proposal to the owner.** Claude supplied rule text for the baseline and gates; all three approved that response. Record the evidence-update provision alongside the cap.
2. **Define critical functions, interfaces and the rated article.** Claude proposed definitions; GPT’s boundary concerns identify where clarification is needed.
3. **Pilot independent assessments.** Claude proposed three assessors rating three composites; GPT recommended representative propulsion, power and processing cases. Compare conclusions, findings and assessment effort.
4. **Publish traceable composite entries.** Follow Claude and GPT’s proposed configuration, evidence, blocker and upgrade-condition reporting, incorporating Gemini’s three-part rating display where useful.
5. **Reconcile T26 without automatically rerating it.** Follow GPT’s preservation of the existing ruling and Claude’s request to inspect its supporting evidence.
6. **Pre-commit review triggers.** Claude proposed reconsidering the rule if evidence cannot be attributed to critical functions or assessors diverge materially; GPT proposed revisiting it if calibration shows inconsistency, unsupported claims or excessive cost without improved validity.

```yaml
questionId: "rq-0-72"
topics:
  - id: headline-rule
    topic: Bounded integration assessment versus automatic inheritance
    positions:
      - statement: "Use integration assessment within a weakest-critical-function bound, updating sub-ratings from applicable integrated evidence before applying the bound."
        models: ["Claude Opus 5.5", "Gemini 3.1 Pro", "GPT-6.1 Sol"]
        evidence: "Claude proposed the bounded rule; all three approved Claude's response. Gemini independently recommended a hybrid minimum."
      - statement: "Do not automatically inherit published constituent minima; reconcile lower ratings through applicable evidence or a justified scope distinction without excluding actual dependencies."
        models: ["GPT-6.1 Sol"]
        evidence: "GPT's original recommendation; Claude's critique identified scope reconciliation as a possible gate escape hatch."
    resolution_status: partially-resolved
    priority: high
  - id: integrated-article-ceiling
    topic: TRL 4 ceiling and assessment boundary
    positions:
      - statement: "Do not exceed TRL 4 without a tested integrated article implementing all critical functions and coupled interfaces."
        models: ["Claude Opus 5.5"]
        evidence: "Claude's R2 in the unanimously approved response."
      - statement: "Article requirements must follow the claimed technology level and assessment boundary, not an arbitrary whole-system boundary."
        models: ["GPT-6.1 Sol"]
        evidence: "GPT's original critique of the blanket ceiling; final approval did not separately explain this boundary issue."
    resolution_status: partially-resolved
    priority: high
  - id: t26-consistency
    topic: Relationship to the existing T26 ruling
    positions:
      - statement: "Verify T26's supporting sub-ratings and conditions before claiming compatibility."
        models: ["Claude Opus 5.5"]
        evidence: "Claude explicitly identified compatibility as an unverified assumption."
      - statement: "Retain TRL 3 with TRL 4 conditional; the general rule does not itself rerate or reinterpret T26."
        models: ["GPT-6.1 Sol"]
        evidence: "GPT's continuity requirement and consequences."
      - statement: "The hybrid rule retroactively justifies T26."
        models: ["Gemini 3.1 Pro"]
        evidence: "Gemini's consequences section; Claude and GPT challenged the assertion as unsupported."
    resolution_status: open
    priority: medium
  - id: assessment-calibration
    topic: Reproducibility and assessment burden
    positions:
      - statement: "Pilot independent assessments and reconsider the approach if material inconsistency or excessive burden appears."
        models: ["Claude Opus 5.5", "GPT-6.1 Sol"]
        evidence: "Both identified calibration as missing; Claude proposed simplifying the rule if variance is excessive, while GPT proposed tightening criteria or using a conservative interim default."
    resolution_status: partially-resolved
    priority: high
```