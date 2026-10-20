---
questionId: "rq-0-66"
questionSlug: "kdp-0b-trl6-scope-secondary-technologies"
type: "discussion-conclusion"
generatedBy: "gpt-6-1-sol"
generated: "2026-10-17"
framework: "18f503fe4ec6"
roundCount: 1
terminationReason: "unanimous-conclude"
---

## Summary

**All three models rejected a blanket requirement that all five technologies receive a new TRL-6 demonstration at KDP-0B.** Claude Opus 5.5, Gemini 3.1 Pro and GPT-6.1 Sol supported using applicable 0A mission evidence for T11/T18 and distinguishing supporting implementations from project-ending dependencies. All three rejected leaving the panel split unresolved. Their mutual approvals of Claude’s and GPT’s responses establish support for those approaches, but not convergence on identical gate text.

**The remaining disagreement concerns T18’s binding criterion and the strength of exceptions for T09, T12 and T20.** Claude retained T18 as project-ending and required target-specific in-situ bulk-grade evidence; Gemini assessed T18 through its 0A mission rather than a separate pre-gate TRL requirement; GPT required TRL 6 for the relevant sampling-and-assay capability plus acceptable target-specific results. For T09/T12/T20, Claude proposed TRL 6 by default, with TRL-5 exceptions backed by qualified TRL-6 fallbacks and joint-fallback economics. Gemini allowed TRL 5 with an approved waiver, defined fallback and funded maturation plan. GPT tied TRL 6 to irreversible dependency, permitting lower maturity only where independently demonstrated substitution or deferral protects the authorised investment case.

Claude and GPT expressly treated fallback adequacy as unproven; both required the affected item to revert to TRL-6 treatment when the exception’s evidence is insufficient. Gemini expressed greater confidence in substitutability, which Claude and GPT challenged as unsupported. No response established that any particular fallback already qualifies.

## Decision record

### Claude Opus 5.5: differentiated gates with qualified-fallback exceptions

**Y-statement:** In the context of D-01’s gated real option and D-02’s one-way KDP-0B gate, facing disputed classifications and potentially cumulative waiver exposure, **Claude chose** to retain T18 as project-ending with target-specific in-situ assay evidence, remove T11 from the KDP-0B list unless Phase 1 inherits its hardware or software, and require TRL 6 for T09/T12/T20 unless a qualified-fallback exception is earned, to protect the irreversible commitment without unnecessarily blocking substitutable implementations, accepting fallback-qualification expenditure, potentially worse Phase 1 economics, and a gate date dependent on scout assay return.

- **Warrant — Claude:** The gate should test the consequence of failure; target evidence addresses T18’s risk, while qualified alternatives can address architecture-change risk.
- **Qualifier — Claude:** A TRL-5 exception requires a named TRL-6 fallback, passing economics with all waived items on their fallbacks simultaneously, fallback penalties in the baseline, and independent waiver authority.
- **Accepted downside — Claude:** Phase 1 may use a costlier fallback; absent qualifying evidence, the item requires TRL 6 without an exception.

### Gemini 3.1 Pro: mission-evidence assessment and tiered exemption

**Y-statement:** In the context of defining KDP-0B criteria, facing a split over five technologies outside the agreed core, **Gemini chose** to assess T11/T18 through their 0A mission evidence and permit T09/T12/T20 at TRL 5 with an approved waiver, defined fallback and fully funded maturation plan, to preserve schedule realism and architectural flexibility, accepting the possibility of expensive Phase 1 redesign.

- **Warrant — Gemini:** 0A flight technologies mature through their missions, while architecture-change technologies can be substituted rather than treated as project-ending.
- **Qualifier — Gemini:** Its recommendation depends on scout evidence arriving before KDP-0B and on supporting-system failures remaining manageable through alternatives.
- **Accepted downside — Gemini:** A waived technology may require costly redesign. Gemini also identified T18’s necessity to the economic case as a sensitivity that could invalidate its preferred exemption.

### GPT-6.1 Sol: dependency-based gate with inherited evidence

**Y-statement:** In the context of D-01 and D-02, facing disputed labels and potentially irreversible dependencies, **GPT chose** capability-based TRL-6 gating with applicable inherited 0A evidence and independently demonstrated reversibility, to protect the investment case without duplicate maturation, accepting additional assurance work and the possibility that all five ultimately require TRL 6.

- **Warrant — GPT:** Irreversibility, rather than technology-list membership or selection alone, determines required stringency.
- **Qualifier — GPT:** An unproven substitution defaults to TRL-6 treatment. Lower-maturity acceptance requires a funded, scheduled, interface-compatible alternative or deferral preserving demand, economics, safety and licensing.
- **Accepted downside — GPT:** The rule requires judgment, dependency analysis and explicit commitment controls rather than a simple fixed list.

## Decision-quality audit

### Round 1 — Claude Opus 5.5

- **Weakest link named in votes:** Claude and GPT named **information**; Gemini named **none**.
- **Composite Scaffold support:** Claude and GPT’s votes recognised criteria-before-options, null options, sensitivity analysis, falsifiable assumptions and concrete gate text. Their reservations concerned speculative maturity forecasts, possible fallbacks and the unconfirmed interpretation that current target-gate text permits remote-sensing-only evidence.
- **Missing or unsupported elements identified:** No voter identified a missing scaffold step. Claude and GPT identified evidence gaps within the information and certainty steps; approval did not establish the forecasts or fallback feasibility as facts.
- **Values trade-off identified by Claude:** Waiting for the preferred implementation versus accepting a costlier qualified fallback; spending Phase 0 resources on primary maturation versus fallback qualification.

### Round 1 — Gemini 3.1 Pro

- **Weakest links named in votes:** Claude and GPT named **reasoning**; Gemini named **alternatives**. All three votes were neutral.
- **Composite Scaffold support gaps identified by Claude/GPT:** Gemini selected its tiered exemption without resolving its own T18 sensitivity. Claude noted that Gemini’s matrix favoured the hybrid on risk containment without a demonstrated aggregation supporting the final choice. Both challenged high confidence in substitutability and the absence of combined-fallback economics.
- **Missing or unsupported elements identified by Gemini:** Gemini’s self-review cited insufficient null-option evaluation and no rigorous competing-hypotheses analysis.
- **Values trade-off identified by Gemini:** Schedule realism and flexibility versus stronger pre-commitment risk containment. Claude and GPT’s objections also concerned missing evidence, not merely different values.

### Round 1 — GPT-6.1 Sol

- **Weakest link named in votes:** Claude and GPT named **commitment**; Gemini named **none**.
- **Composite Scaffold support:** The votes recognised non-compensable requirements, criteria-before-options, a null option, qualified evidence ratings, falsifiable assumptions and a default-to-TRL-6 rule.
- **Missing or unsupported elements identified:** No voter identified a missing scaffold step. Claude described the commitment as less concrete because its application could still require TRL 6 for all five; GPT acknowledged judgment remains over sufficient alternative maturity.
- **Values trade-offs identified by GPT:** Demonstration expenditure versus conditional authorisation, deployment delay versus flexibility, and the amount of bounded rework risk acceptable after project-ending exposure is excluded.

## Key Points

- **All three models:** No uniform, duplicate TRL-6 demonstration requirement is justified solely by these five technology identifiers.
- **All three models:** Leaving the split unresolved is not an acceptable gate policy.
- **Claude and GPT:** T18’s technological maturity cannot substitute for adequate selected-target evidence.
- **Claude:** T18 must supply in-situ bulk-grade evidence; ground TRL 6 alone is insufficient.
- **Gemini:** T11/T18 should be assessed through 0A mission data rather than a separate pre-gate TRL rule.
- **Claude and GPT:** Applicable 0A evidence should be reused, although Claude’s T11 re-entry trigger is hardware/software inheritance and GPT’s is an outstanding critical capability.
- **Claude and GPT:** A funded maturation plan alone does not establish that Phase 1 survives implementation failure.
- **Claude:** Multiple exceptions must pass a simultaneous joint-fallback economics case.
- **GPT:** Exceptions must remain reversible through explicit substitution deadlines and automatic stop triggers.
- **All three models:** Their proposed flexibility does not authorise a waiver for a genuinely project-ending dependency under D-02.

## Unresolved Questions

1. **T18’s exact criterion:** Claude requires target-based in-situ bulk assay; GPT requires applicable TRL 6 plus acceptable target evidence; Gemini relies on mission evidence. The panel did not agree identical wording.
2. **T11’s return to the gate:** Claude uses Phase 1 hardware/software inheritance; GPT uses continuing critical dependency. Gemini did not specify an equivalent re-entry rule.
3. **Exception strength:** Claude requires TRL-6 fallbacks and joint-fallback economics; Gemini proposes a defined fallback and funded maturation; GPT requires independently demonstrated reversibility without Claude’s explicit universal fallback-TRL threshold.
4. **Fallback feasibility:** Claude and GPT identify this as unevidenced; Gemini’s higher confidence was challenged in the votes.
5. **Reference implementation:** Claude binds it to the frozen design and operating scope; GPT binds it to the configuration underpinning the approved architecture, models, interfaces and qualification plan. The precise shared definition remains unwritten.
6. **Owner preferences:** Claude and GPT identify acceptable delay, fallback expenditure and bounded rework exposure as values decisions rather than facts testing alone can settle.

## Recommended Actions

- **Following all three models:** Replace the unresolved split with explicit gate text before teams rely on it for maturation planning.
- **Following Claude and GPT:** Require an evidence-applicability record showing which 0A demonstrations satisfy which KDP-0B capabilities.
- **Following Claude and GPT:** Confirm the scout payload, assay scope, target-evidence acceptance criteria and delivery date; inspect the actual target-gate text before accepting Claude’s proposed remote-sensing loophole as established.
- **Following Claude:** Commission named fallback trades for T09/T12/T20 and test simultaneous fallback economics, carrying penalties in the baseline.
- **Following GPT:** Map irreversible commitments, substitution deadlines, interface constraints and automatic stop triggers.
- **Following Claude and GPT:** Default affected dependencies to TRL 6 when exception evidence is inadequate; do not treat proposed alternatives as qualified.
- **Following the distinctions identified by all three:** Ask the owner to settle T18 wording, T11 re-entry and exception thresholds explicitly, while recording schedule-versus-assurance preferences.
- **Following GPT:** Preserve the pre-committed “0A only, Earth supply” outcome if required evidence is unavailable.

```yaml
questionId: "rq-0-66"
topics:
  - id: blanket-trl-six
    topic: Blanket TRL-6 requirement for all five technologies
    positions:
      - statement: Reject a uniform duplicate demonstration requirement; reuse applicable 0A evidence and distinguish dependencies.
        models: ["Claude Opus 5.5", "Gemini 3.1 Pro", "GPT-6.1 Sol"]
        evidence: "All three rejected blanket treatment and the unresolved null option in Round 1."
    resolution_status: resolved
    priority: high

  - id: t18-gate-criterion
    topic: Binding requirement for T18
    positions:
      - statement: Retain project-ending status and require selected-target in-situ bulk-grade evidence; ground TRL 6 alone is insufficient.
        models: ["Claude Opus 5.5"]
        evidence: "Claude's proposed target-evidence provenance rule and no-waiver requirement."
      - statement: Assess T18 through 0A mission evidence rather than a separate pre-gate TRL requirement.
        models: ["Gemini 3.1 Pro"]
        evidence: "Gemini's tiered exemption, conditional on scout evidence supporting the gate."
      - statement: Require TRL 6 for the applicable sampling-and-assay capability plus acceptable target-specific results.
        models: ["GPT-6.1 Sol"]
        evidence: "GPT's distinction between capability maturity and target adequacy."
    resolution_status: partially-resolved
    priority: critical

  - id: t11-evidence-and-reentry
    topic: T11 evidence inheritance and return to KDP-0B
    positions:
      - statement: Remove T11 from the list unless Phase 1 inherits its hardware or software.
        models: ["Claude Opus 5.5"]
        evidence: "Claude's explicit inheritance-based re-entry condition."
      - statement: Assess T11 through its 0A mission data.
        models: ["Gemini 3.1 Pro"]
        evidence: "Gemini's classification of T11 as a self-proving 0A flight technology."
      - statement: Reuse applicable 0A evidence and require TRL 6 for outstanding scout capabilities critical to 0B.
        models: ["GPT-6.1 Sol"]
        evidence: "GPT's configuration-applicability and continuing-dependency tests."
    resolution_status: partially-resolved
    priority: high

  - id: supporting-system-exceptions
    topic: Exceptions for T09, T12 and T20
    positions:
      - statement: Default to TRL 6; permit TRL 5 only with TRL-6 fallbacks, joint-fallback economics, baseline penalties and independent authority.
        models: ["Claude Opus 5.5"]
        evidence: "Claude's waiver-stacking analysis; fallback feasibility remains conditional."
      - statement: Permit TRL 5 with an approved waiver, defined fallback and fully funded maturation plan.
        models: ["Gemini 3.1 Pro"]
        evidence: "Gemini's architecture-change classification; Claude and GPT challenged its confidence in substitutability."
      - statement: Require TRL 6 for irreversible dependencies; otherwise permit TRL 5 only with independently demonstrated substitution or deferral and commitment controls.
        models: ["GPT-6.1 Sol"]
        evidence: "GPT's dependency rule, stop triggers and default to TRL 6 when reversibility is unproven."
    resolution_status: partially-resolved
    priority: critical
```