---
questionId: "rq-0-73"
questionSlug: "scout-trl-milestone"
type: "discussion-conclusion"
generatedBy: "gpt-6-1-sol"
generated: "2026-10-17"
framework: "18f503fe4ec6"
roundCount: 1
terminationReason: "unanimous-conclude"
---

## Summary

Claude, Gemini and GPT converged on **TRL 6 for T11 and T18 at scout PDR**, followed by successful in-situ sampling and assay before the target decision can pass. Claude and GPT additionally converged on an explicit **pre-launch qualification requirement** and a **target gate governed by decision-grade data, not a TRL label alone**. All three rejected leaving the original panel split unresolved.

The panel did **not** converge on the complete rule. Gemini retained TRL 7 as the target-gate criterion and argued that pre-launch TRL 8 was impossible; Claude and GPT challenged that premise in their votes. Claude proposed an ISO-based ladder and an explicit flight-demonstrated T18 requirement at KDP-0B; GPT retained D-02’s general TRL-6 floor while separately requiring validated scout results before the target gate. Claude alone added TRL 5 at SRR. Accordingly, the discussion supports a shared milestone structure, but not an unqualified adoption of any one response.

## Decision record

### Claude’s position

**Y-statement:** In the context of the scouts supplying sampled-grade evidence for the target gate, facing different milestones and TRL interpretations, **Claude chose** TRL 5 at SRR, TRL 6 at PDR, ISO TRL 8 flight qualification at launch release, a data-based target gate, and operationally demonstrated T18 before KDP-0B, to achieve milestone-specific assurance, accepting first-scout failure risk and possible delay or Earth-supply fallback.

- **Warrant — Claude:** PDR assesses technology maturity; launch release assesses qualification; the target gate assesses resource evidence; KDP-0B requires project-ending technology demonstrated where it must work.
- **Qualifier — Claude:** The proposal assumes a credible T18 analogue test environment and at least two staggered scouts.
- **Accepted downside — Claude:** Greater qualification effort, possible target-gate delay and residual in-situ failure risk. Claude labelled its numerical failure estimate low-confidence judgement.

### Gemini’s position

**Y-statement:** In the context of Phase 0A target validation, facing conflicting readiness requirements, **Gemini chose** TRL 6 at scout PDR and TRL 7 through successful target sampling and assay before the target gate and KDP-0B, to achieve operationally demonstrated evidence, accepting that the first scout is itself the technology demonstration.

- **Warrant — Gemini:** Operational demonstration is necessary before the target decision; Gemini also argued that TRL 8 could not precede first flight.
- **Qualifier — Gemini:** The proposal assumes sampled-grade evidence is necessary and that 0A can absorb failure and reflight.
- **Accepted downside — Gemini:** First-flight demonstration risk and a target gate that must wait for successful target operations.
- **Recorded challenge — Claude and GPT:** Both rejected Gemini’s claim that flight qualification necessarily requires prior spaceflight.

### GPT’s position

**Y-statement:** In the context of D-01’s gated option and D-02’s assurance policy, facing requirements attached to different milestones, **GPT chose** TRL 6 for critical novel technologies at PDR, TRL 8 for each actual integrated flight system before launch, and validated sampling evidence at the target gate, to achieve credible flight readiness and an evidence-based resource decision, accepting additional early qualification expenditure and potentially later gate passage.

- **Warrant — GPT:** Technology maturity, flight qualification and investment evidence are distinct assurance claims.
- **Qualifier — GPT:** PDR timing can be revised on a documented test-and-cost case; launch qualification and target evidence remain required.
- **Accepted downside — GPT:** A technically successful mission may still fail the target gate because its measurements are insufficient or unrepresentative.
- **KDP-0B rule — GPT:** Retain D-02’s no-waiver TRL-6 requirement for all project-ending technologies; successful scout operations do not mature undemonstrated production technologies.

## Decision-quality audit

All three Round 1 responses addressed the nine Composite Scaffold headings. The voting criticism concerned support, completeness and commitment rather than wholesale omission.

| Round 1 response | Weakest links named in votes | Missing or unsupported elements identified by reviewers |
|---|---|---|
| **Claude** | Claude: **reasoning**; Gemini: **alternatives**; GPT: **information** | Claude acknowledged that the scoring margin was sensitive to the coherence weight. Gemini criticised rejecting alternatives before completing their assessment. GPT challenged the claimed NASA–ISO incompatibility and the suggestion that NASA TRL 8 necessarily presupposes operational flight. |
| **Gemini** | Claude: **information**; Gemini: **alternatives**; GPT: **information** | Claude and GPT challenged the high-certainty claim that TRL 8 cannot precede first flight. Claude identified no explicit launch-release criterion, a TRL-labelled rather than data-quality target gate, an unscored qualitative matrix and no precursor alternative. Gemini’s self-review noted limited alternatives and premature rejection of options. |
| **GPT** | Claude: **alternatives**; Gemini: **alternatives**; GPT: **commitment** | Claude identified no explicit precursor or single-scout option and considered some alternatives incomplete representations of competing positions. Gemini criticised pre-judging alternatives. GPT acknowledged that detailed test envelopes and target-evidence thresholds remained implementation tasks. Claude considered GPT’s KDP-0B wording weaker than its own, while compliant with D-02. |

### Trade-off points, rather than facts to settle

- **First-flight risk versus delay:** Claude explicitly treated avoiding a precursor mission in exchange for residual scout risk as an owner risk-appetite choice. Gemini likewise accepted first-flight demonstration risk.
- **Qualification spending versus tolerated loss:** GPT identified this as a mission-assurance trade-off; Claude proposed stricter testing if only one scout is funded.
- **Early maturity versus design flexibility:** GPT treated TRL 6 at PDR versus a controlled TRL-5 development path as a cost-and-risk trade-off.
- **Additional evidence versus exercising 0B sooner:** GPT identified the value of more reconnaissance against delayed commitment.
- **TRL vocabulary versus data-specific criteria:** Claude described this partly as a values difference; Claude and GPT nevertheless argued that a TRL label alone cannot establish resource-evidence sufficiency.

## Key Points

- **Shared PDR threshold:** All three proposed TRL 6 at scout PDR. Claude and GPT treated month 12–24 as conditional on demonstrated readiness rather than a guaranteed achievement date.
- **Explicit launch assurance:** Claude and GPT required flight qualification before launch. Claude proposed qualifying the design and accepting subsequent units; GPT required configuration-specific qualification and acceptance evidence for every actual integrated flight system.
- **Target evidence:** Claude and GPT required predeclared sampled-data thresholds. Gemini required successful in-situ sampling and assay, expressed as TRL 7.
- **Timing consequence:** All three placed the target gate after successful target operations. GPT explicitly included data return, validation and independent review.
- **No agreed calendar date:** Claude supplied an illustrative month 36–66 target-gate range as judgement; the other responses did not endorse that range.
- **KDP-0B distinction:** Claude explicitly strengthened T18’s requirement to operational demonstration. GPT preserved D-02’s general TRL-6 floor alongside the separate target-evidence prerequisite. Gemini prohibited progression until T18’s target demonstration.
- **TRL-definition dispute:** Claude and GPT’s votes challenged Gemini’s pre-launch impossibility claim; GPT also challenged Claude’s claimed NASA–ISO incompatibility. The votes did not establish a jointly accepted scale interpretation.

## Unresolved Questions

1. **Which standard and crosswalk govern?** Claude proposed ISO/ECSS with a NASA crosswalk; GPT required an adopted definition but disputed the asserted incompatibility; Gemini relied on its NASA/DoD interpretation.
2. **How should T18’s KDP-0B requirement be written?** Claude proposed an explicit operational-demonstration requirement; GPT retained the general D-02 floor plus target-gate evidence; Gemini used TRL 7 before progression.
3. **What constitutes sufficient target evidence?** Claude and GPT required thresholds for uncertainty, coverage and representativeness, but neither supplied final values.
4. **Can T18 credibly reach TRL 6 within the proposed PDR window?** All three identified relevant-environment fidelity as a material uncertainty.
5. **How many scouts are funded, and with what cadence?** Claude’s proportionality argument assumed multiple staggered scouts; Gemini also identified single-scout funding as a reason for stronger ground qualification.
6. **Should TRL 5 at SRR become mandatory?** Claude proposed it; Gemini and GPT did not adopt that additional milestone.

## Recommended Actions

- **Record the shared PDR requirement:** Following all three responses, specify TRL 6 for T11/T18 critical functions at PDR, subject to documented relevant-environment evidence.
- **Resolve definitions before approving final rule text:** Following Claude’s scale-declaration proposal and GPT’s critique, document the governing TRL definition and crosswalk; do not rely on the contested prior-flight premise.
- **Specify launch-release evidence separately:** Following Claude and GPT, define qualification, configuration applicability, unit acceptance and anomaly-closure requirements.
- **Write the target-data specification before flight:** Following Claude and GPT, connect sampling coverage, assay uncertainty, calibration and representativeness to the resource and economics decision.
- **Resolve the explicit T18 KDP-0B wording:** Compare Claude’s operational-demonstration requirement with GPT’s general floor plus separate target gate and Gemini’s TRL-7 condition.
- **Rebaseline against evidence:** Following all three responses, assess analogue-test fidelity and single-scout risk before fixing dates. Claude and GPT recommended replanning rather than relabelling inadequate evidence.
- **Preserve the agreed programme fallback:** Claude and GPT reiterated “0A only, Earth supply” if required evidence cannot support progression within the authorised programme terms.

```yaml
questionId: "rq-0-73"
topics:
  - id: pdr-readiness
    topic: Scout and payload readiness at PDR
    positions:
      - statement: Require TRL 6 for T11 and T18 critical technologies at scout PDR.
        models: ["Claude Opus 5.5", "Gemini 3.1 Pro", "GPT-6.1 Sol"]
        evidence: "All three Round 1 proposals specify relevant-environment demonstration by PDR."
    resolution_status: resolved
    priority: high

  - id: launch-qualification-and-scale
    topic: Pre-launch qualification and governing TRL definition
    positions:
      - statement: Require flight qualification before launch, expressed as ISO TRL 8 with a recorded NASA crosswalk.
        models: ["Claude Opus 5.5"]
        evidence: "Claude's ladder separates qualification of the design from acceptance of later units."
      - statement: Require TRL 8 for each actual integrated flight system; prior successful operational flight is not inherently required.
        models: ["GPT-6.1 Sol"]
        evidence: "GPT cites NASA TRL descriptions and distinguishes flight qualification from mission operation."
      - statement: Reject pre-launch TRL 8 because it requires prior spaceflight.
        models: ["Gemini 3.1 Pro"]
        evidence: "Gemini's definition-based argument; Claude and GPT challenged its premise in their votes."
    resolution_status: partially-resolved
    priority: high

  - id: target-gate-criterion
    topic: Target-gate evidence versus TRL label
    positions:
      - statement: Require validated target-specific sampled-data thresholds; TRL is supporting evidence, not a sufficient pass criterion.
        models: ["Claude Opus 5.5", "GPT-6.1 Sol"]
        evidence: "Both distinguish successful operation from adequate uncertainty, coverage and resource representativeness."
      - statement: Require T18 TRL 7 through successful in-situ sampling and assay before the target gate.
        models: ["Gemini 3.1 Pro"]
        evidence: "Gemini's proposed rule makes operational demonstration the target-gate threshold."
    resolution_status: partially-resolved
    priority: critical

  - id: kdp-0b-t18-requirement
    topic: Explicit T18 requirement at KDP-0B
    positions:
      - statement: Require operationally demonstrated T18; TRL 6 alone is insufficient.
        models: ["Claude Opus 5.5"]
        evidence: "Claude identifies T18 as project-ending and explicitly requires in-situ sampling and assay."
      - statement: Retain D-02's no-waiver TRL-6 floor alongside the separate validated target-evidence requirement.
        models: ["GPT-6.1 Sol"]
        evidence: "GPT preserves D-02 and prevents scout success from conferring maturity on production technologies."
      - statement: Do not progress to KDP-0B until T18 achieves TRL 7 on the target.
        models: ["Gemini 3.1 Pro"]
        evidence: "Gemini's rule ties progression to successful operational demonstration."
    resolution_status: partially-resolved
    priority: critical

  - id: schedule-and-risk-posture
    topic: Calendar commitment and first-scout risk
    positions:
      - statement: Use a conditional PDR window and a multiple-scout strategy; strengthen testing if only one scout is funded.
        models: ["Claude Opus 5.5"]
        evidence: "Claude conditions its proposal on analogue fidelity and staggered scouts; its target-gate date range is judgement."
      - statement: Accept first-flight demonstration risk, conditional on funding failure recovery.
        models: ["Gemini 3.1 Pro"]
        evidence: "Gemini assumes the 0A budget can absorb failure and reflight."
      - statement: Rebaseline dates from test evidence and schedule the target gate after validated mission results.
        models: ["GPT-6.1 Sol"]
        evidence: "GPT treats month 12–24 as a planning window and identifies data validation as a timing dependency."
    resolution_status: open
    priority: high
```