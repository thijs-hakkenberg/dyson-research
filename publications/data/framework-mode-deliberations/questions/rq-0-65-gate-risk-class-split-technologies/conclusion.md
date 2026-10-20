---
questionId: "rq-0-65"
questionSlug: "gate-risk-class-split-technologies"
type: "discussion-conclusion"
generatedBy: "gpt-6-1-sol"
generated: "2026-10-17"
framework: "18f503fe4ec6"
roundCount: 1
terminationReason: "unanimous-conclude"
---

## Summary

Claude Opus 5.5 and GPT-6.1 Sol converged on an **evidence-conditioned rule**: classify a function as project-ending unless an independently reviewed fallback preserves viable, authorised 0B production. Gemini 3.1 Pro also favoured classification by fallback viability, but considered several alternatives sufficiently credible to justify architecture-change immediately. Thus, the panel shared a governing principle but **did not converge on all eight classifications or on the evidence needed before lowering a class**.

GPT recommended project-ending for **T02, T10, T14, T15, T22, T24 and T25**, retaining T26 as architecture-change subject to a KDP-0A closure test. Claude recommended project-ending for T02, safety-critical T10 and T15/T22, while proposing conditional or provisional architecture-change treatment for productivity T10, T14, T24 and T25. Gemini recommended project-ending for T10, T14, T24 and T25, and architecture-change for T02, T15, T22 and T26. All three retained T26’s existing architecture-change classification; GPT additionally proposed automatic elevation if its closure test failed.

The votes exposed the main unresolved issue: **Claude and GPT both identified a contradiction between Claude’s project-ending default and its immediate lowering of classes before fallback dossiers were accepted**. Claude and GPT also rejected Gemini’s lower classifications as resting on unevidenced fallback assumptions. GPT’s response received approval from all three models, but those approvals did not establish an explicit revised classification agreement from the other two respondents.

## Decision record

### Claude Opus 5.5: function-level classification with conditional lower classes

**Y-statement:** In the context of D-01/D-02 and a one-way KDP-0B commitment, facing disagreements Claude attributed mainly to inconsistent scope and definitions, Claude chose a function-level fallback rule, to protect 0B while avoiding unnecessary qualification, accepting additional 0A work and dependence on independent dossier review.

- **Warrant:** Claude argued that consequences and fallback viability—not model votes—should determine class.
- **Proposed classifications:**
  - **Project-ending:** T02; T10a, safety-critical autonomy; T15; T22.
  - **Architecture-change, conditional or provisional:** T10b, productivity autonomy; T14; T24; T25.
  - **T26:** retain architecture-change under rq-0-64; leave possible elevation to that decision.
- **Qualifier:** Claude’s written rule made project-ending the default until an accepted fallback dossier existed.
- **Accepted downside:** Claude accepted potentially longer TRL 6 holds and the risk of optimistic fallback costing.
- **Recorded inconsistency:** Claude’s self-review and GPT’s vote both said the conditional lower classifications contradicted that default.

### Gemini 3.1 Pro: split according to asserted fallback viability

**Y-statement:** In the context of the KDP-0B gate, facing disputed classifications, Gemini chose to distinguish core operating technologies from technologies with alternative implementations, to balance 0A schedule with commitment protection, accepting that the alternatives might degrade Phase 1 economics.

- **Warrant:** Gemini argued that project-ending should be reserved for technologies without viable functional fallbacks.
- **Proposed classifications:**
  - **Project-ending:** T10, T14, T24, T25.
  - **Architecture-change:** T02, T15, T22, T26.
- **Qualifier:** Gemini assumed smaller arrays, localised power, Earth-based packaging and existing communications services would preserve acceptable economics.
- **Accepted downside:** Gemini accepted economic degradation from those alternatives.
- **Recorded challenge:** Claude and GPT rejected the decisive fallback claims as insufficiently evidenced.

### GPT-6.1 Sol: conservative current classes with an evidence-based exit

**Y-statement:** In the context of funded 0A and optional 0B production, facing unresolved classifications and unevidenced fallbacks, GPT chose seven project-ending classifications and a time-bounded architecture-change ruling for T26, to protect irreversible investment while permitting demonstrated substitution, accepting additional qualification effort and possible delay or rejection of 0B.

- **Warrant:** GPT argued that indispensable production functions require demonstrated capability or an evidenced substitute before commitment.
- **Proposed classifications:**
  - **Project-ending:** T02, T10, T14, T15, T22, T24, T25.
  - **T26:** architecture-change under rq-0-64, with a proposed KDP-0A test; failure would elevate the affected capability to project-ending.
- **Qualifier:** GPT allowed reclassification following owner acceptance of an independently reviewed, architecture-specific fallback package.
- **Accepted downside:** GPT accepted additional 0A analysis, testing and possible delay.
- **Voting outcome:** Claude, Gemini and GPT approved this response; neither Claude nor Gemini supplied a revised classification table explicitly adopting it.

## Decision-quality audit

### Round 1

| Response | Weakest links named in votes | Missing or unsupported Composite Scaffold elements |
|---|---|---|
| **Claude** | Claude: **reasoning**; GPT: **commitment**; Gemini: none | Claude and GPT identified a mismatch between the generating rule and the operative classifications in the decision step. Claude also identified minor assessment-matrix arithmetic errors. Gemini approved the overall decision chain. |
| **Gemini** | Claude and GPT: **information**; Gemini: **information** | Claude challenged the qualitative weights and matrix, thin certainty claims, and unsupported fallback evidence. GPT challenged the architecture-specific evidence and calibrated confidence, especially for T26. Gemini’s self-review identified the absence of a structured ACH analysis. |
| **GPT** | Claude: **alternatives**; GPT: **information**; Gemini: none | Claude said the all-project-ending and evidence-conditioned options differed mainly in the reclassification path, and noted minor arithmetic errors. GPT acknowledged that the record contained no supporting fallback studies or test reports. All three nevertheless approved the response. |

### Trade-off points, rather than facts to settle

- **Burden of proof:** Claude and GPT explicitly favoured a project-ending default; both framed the balance between extra 0A work and irreversible 0B exposure as an owner value judgment.
- **Acceptable degraded production:** Claude and GPT said the owner must define how much throughput, schedule or cost degradation still counts as a successful 0B fallback.
- **Meaning of “project-ending”:** Claude recommended a definition tied to viable 0B production; GPT explicitly distinguished ending the proposed 0B commitment from ending the funded 0A programme.
- **Schedule versus assurance:** Gemini explicitly prioritised a balance between 0A velocity and KDP-0B confidence.
- **Not merely a trade-off:** Claude and GPT treated fallback performance, maturity, cost and independence as evidence questions—not matters that an owner preference alone could settle.

## Key Points

- **Shared principle, disputed application:** All three responses used fallback viability to distinguish classes. Claude and GPT required stronger evidence before lowering them than Gemini supplied.
- **The source labels need care:** GPT warned that the background’s “agreed core” was not evidence of unanimous original classifications. Claude likewise identified scope and definition inconsistencies, including its own T25 entries.
- **T10 may need functional separation:** Claude proposed separating safety-critical autonomy from productivity autonomy. GPT supported splitting broad technology IDs where necessary, but retained T10 as project-ending in its current table.
- **TRL and consequence are different:** Claude and GPT argued that current maturity estimates or familiar components do not establish that a function is replaceable.
- **The economics gate is not sufficient by itself:** Claude and GPT rejected using economics modelling to compensate for missing technical evidence about a fallback.
- **T26 has a narrower agreement:** All three retained architecture-change. Only GPT proposed automatic elevation at KDP-0A; Claude explicitly kept possible elevation within rq-0-64.
- **Earth supply has two different roles in the responses:** GPT treated “0A only, Earth supply” as a programme exit, not continued 0B production. Gemini proposed Earth-based packaging as a T22 fallback, which Claude and GPT considered insufficiently demonstrated.

## Unresolved Questions

1. **Which classifications operate before dossiers are accepted?** Claude’s rule implies project-ending holds, but its table grants several lower classes; Claude and GPT both flagged this contradiction.
2. **What constitutes an admissible fallback?** Claude proposed explicit maturity, costing, economics, independence and schedule conditions. GPT proposed an independently reviewed qualification and transition package. Gemini did not establish comparable evidence thresholds.
3. **What degraded 0B remains authorised?** Claude and GPT requested owner-defined production, cost and schedule boundaries.
4. **Which technology scopes should be controlled?** Claude identified tug versus site power, safety versus productivity autonomy, and communications links versus integrated command service as important distinctions.
5. **How should T26 close?** GPT proposed automatic elevation; Claude deferred that question to rq-0-64; Gemini considered existing communications alternatives credible.
6. **Can the economics model discriminate fallback branches?** Claude said failure of that capability would undermine its proposed rule and favour conservative holds.
7. **What evidence exists beyond this record?** GPT distinguished “not demonstrated in the supplied record” from “no fallback exists.”

## Recommended Actions

The following actions reflect proposals made by the models, rather than a new classification ruling:

1. **Obtain an explicit owner decision on current classes.** Claude and GPT’s reviews require resolving the contradiction between provisional architecture-change labels and a project-ending-until-evidenced rule.
2. **Record the generating rule alongside the classification table.** Claude and GPT proposed independently reviewed fallback evidence; the owner should explicitly accept or modify the required thresholds.
3. **Define acceptable fallback outcomes at KDP-0A.** Claude and GPT requested controlled limits for production, economics, safety, licence, schedule and cost.
4. **Commission bounded fallback packages.** Claude proposed dossiers for T02, productivity T10, T14, T24 and T25; GPT proposed function-specific qualification and fallback packages across the disputed technologies.
5. **Control scopes before revising the baseline.** Claude proposed splitting T10 and separating tug-array scope from site-power scope; GPT supported function-level decomposition where necessary.
6. **Close T26 through rq-0-64.** Consider GPT’s proposed KDP-0A substitution/disconnection test explicitly, without presenting its automatic-elevation mechanism as already agreed.
7. **Preserve the independent gates and programme exit.** GPT proposed retaining target, demand, economics and licence gates independently, with “0A only, Earth supply” if KDP-0B fails.

```yaml
questionId: "rq-0-65"
topics:
  - id: current-risk-classes
    topic: Operative classifications for the seven technologies other than T26
    positions:
      - statement: "Classify T02, T10, T14, T15, T22, T24 and T25 as project-ending until an evidenced alternative warrants reclassification."
        models: ["GPT-6.1 Sol"]
        evidence: "Indispensable production functions and no qualifying fallback packages demonstrated in the supplied record."
      - statement: "Keep T02, safety-critical T10, T15 and T22 project-ending; allow conditional or provisional architecture-change for productivity T10, T14, T24 and T25."
        models: ["Claude Opus 5.5"]
        evidence: "Proposed supervised operations, alternative propellants, replaceable mechanisms and cooperative navigation fallbacks; Claude and GPT subsequently flagged inconsistency with Claude's dossier-first rule."
      - statement: "Classify T10, T14, T24 and T25 as project-ending, and T02, T15 and T22 as architecture-change."
        models: ["Gemini 3.1 Pro"]
        evidence: "Asserted fallback viability through smaller arrays, localised power and Earth-based packaging; Claude and GPT challenged the supporting evidence."
    resolution_status: open
    priority: critical
  - id: fallback-admissibility
    topic: Evidence required before lowering a risk class
    positions:
      - statement: "Require an accepted, independently reviewed fallback dossier before lowering a project-ending class."
        models: ["Claude Opus 5.5", "GPT-6.1 Sol"]
        evidence: "Both proposed architecture-specific performance, cost, schedule and dependency checks; Claude additionally specified maturity and costing thresholds."
      - statement: "Known alternative implementations justify architecture-change, subject to economic viability."
        models: ["Gemini 3.1 Pro"]
        evidence: "Gemini's classification split relied on asserted alternatives and assumed acceptable Phase 1 economics."
    resolution_status: partially-resolved
    priority: critical
  - id: t26-closure
    topic: T26 architecture-change ruling and possible elevation
    positions:
      - statement: "Retain architecture-change and leave possible project-ending elevation within rq-0-64."
        models: ["Claude Opus 5.5"]
        evidence: "Existing owner ruling and proposed application of the fallback test within that decision."
      - statement: "Retain architecture-change because existing deep-space communications services provide alternatives."
        models: ["Gemini 3.1 Pro"]
        evidence: "DSN and commercial service alternatives; GPT challenged whether fleet-level capacity and resilience were demonstrated."
      - statement: "Retain architecture-change provisionally, with automatic elevation if substitution or tolerable disconnection is not demonstrated at KDP-0A."
        models: ["GPT-6.1 Sol"]
        evidence: "Existing owner ruling, unresolved integrated-service maturity and absence of demonstrated fallback service capacity in the record."
    resolution_status: partially-resolved
    priority: high
  - id: authorised-fallback-outcome
    topic: Definition of viable continued 0B production
    positions:
      - statement: "Judge fallbacks against owner-approved production and economic boundaries; define acceptable degradation explicitly."
        models: ["Claude Opus 5.5", "GPT-6.1 Sol"]
        evidence: "Both identified acceptable reduced output, cost and schedule as owner trade-offs rather than settled technical facts."
      - statement: "Accept less efficient alternatives if the economics remain viable."
        models: ["Gemini 3.1 Pro"]
        evidence: "Gemini explicitly accepted degraded Phase 1 economics as the downside of its architecture-change classifications."
    resolution_status: open
    priority: high
```