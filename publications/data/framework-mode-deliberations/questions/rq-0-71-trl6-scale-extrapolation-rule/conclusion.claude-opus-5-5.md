---
questionId: "rq-0-71"
questionSlug: "trl6-scale-extrapolation-rule"
type: "discussion-conclusion"
generatedBy: "claude-opus-5-5"
generated: "2026-10-17"
framework: "18f503fe4ec6"
roundCount: 1
terminationReason: "unanimous-conclude"
role: "alternate synthesis"
---

## Summary

The panel answered in one round. All three models rejected a universal hard 10× cap on every axis. The models that evaluated the null option (Claude Opus 5.5 and GPT-6.1 Sol) also rejected leaving the split unresolved. Gemini 3.1 Pro labelled Claude's original proposal as its "null", so it never assessed a true null. All three models agreed on several further points:
- Duration may be met by partial physical testing plus a validated degradation model.
- Accelerated testing counts only where the failure mechanism is shown not to change across stress levels.
- Some form of independent review is needed.

Claude and GPT also agreed on two more points:
- Numbering-up of replicated modules must be assessed differently from scaling up a single unit, with interaction and coupling tests.
- The evidence standard should be agreed before pathfinder data exist. Claude called this a frozen "Scaling Basis" at the 0A mid-term review; GPT called it a pre-agreed evidence plan with pre-declared prediction tests.

The panel did not converge on whether any number should bind at the gate. There are three positions:
- **Claude** proposes a rebuttable presumption: a 10× default for single units, a 10–100× band that needs a pre-registered regime case plus an intermediate anchor test, and a non-waivable 100× backstop.
- **GPT** proposes no universal ratio, with or without exceptions. Readiness credit is instead limited to a technology-specific, evidence-bounded deployment envelope with independent concurrence. Unsupported extrapolation below 10× earns no credit, and supported extrapolation above 10× is not a waiver.
- **Gemini** proposes no limit for power and throughput if dimensionless regimes are matched, with a fixed 10× cap on duration (a minimum 10% physical life test).

The peer votes favoured GPT's response (three approvals) and Claude's (two approvals, one neutral from GPT). Gemini's response received three rejections. Claude flagged the backstop disagreement as one to "keep for the owner, not average away".

GPT's neutral vote on Claude centres on the 100× backstop. GPT argued that no evidence links that threshold to acceptable risk, so low confidence does not justify making it non-waivable. GPT conceded its own position depends on independent review proving effective. On GPT's own sensitivity check, the ranking flips to the presumptive-10× option (scores 4.00 against 3.75) if that review fails. Both Claude and GPT therefore make enforceable, independent assurance the hinge of the ruling.

## Decision record

The panel did not converge. One Y-statement per position follows.

**Position A: pre-registered, axis-specific rebuttable presumption with a hard backstop (Claude Opus 5.5)**
> In the context of a one-way KDP-0B gate requiring TRL 6 for project-ending technologies with no waivers, **facing** MW-class and kt/yr targets that no test facility reaches, **we chose** a pre-registered, axis-specific rebuttable presumption with these elements:
> - ≤10× default for a single unit;
> - 10–100× only with a regime case, an anchor test and independent review;
> - >100× never counts as TRL 6;
> - numbering-up assessed through interaction tests;
> - duration through a mechanism-invariant degradation model with 1.5× equivalent-life margin.
>
> **To achieve** auditable gate protection that respects technology-specific physics and lets pathfinders be sized at 0A, **accepting** larger and costlier pathfinders for single-unit technologies (ISRU especially), more review effort at the mid-term review, and the possibility that a sound technology fails solely on the backstop.

- **Warrant:** At an irreversible gate, the evidence standard should be tied to failure physics and fixed before the evidence exists. A backstop is needed because "models validated over two orders of magnitude rarely hold over three for novel hardware."
- **Qualifier:** Moderate confidence in the structure. Low confidence in the specific numbers (10×, 100×, 10%, 1.5×), which are offered as tunable until the Scaling Bases are frozen.
- **Accepted downside:** Ground ISRU at tens of t/yr cannot pass against a kt/yr target without about a 100 t/yr anchor or a modular argument. If that is unaffordable, the "0A only, Earth supply" fallback applies.

**Position B: no universal ratio; evidence-bounded deployment envelope (GPT-6.1 Sol)**
> In the context of Project Dyson's irreversible KDP-0B commitment, **facing** heterogeneous scale-up and lifetime risks, **we chose** technology-specific, independently reviewed evidence envelopes rather than a universal extrapolation ceiling, **to achieve** defensible TRL 6 decisions without mandating unnecessary test scale, **accepting** greater assurance effort and less numerical simplicity.

- **Warrant:** Representativeness depends on failure mechanisms, interactions and validated predictive reach, not on one aggregate ratio.
- **Qualifier:** The position holds only while independent review and validation are demonstrably effective.
- **Accepted downside:**
  - more front-loaded analysis and review cost;
  - disputed judgments are possible;
  - some technologies may still need near-deployment-scale tests.

**Position C: regime-matching for power and throughput, fixed duration cap (Gemini 3.1 Pro)**
> In the context of the KDP-0B transition, **facing** project-ending technologies requiring MW-class/kt-yr scales, **we chose** no fixed limit for power and throughput if governing dimensionless regimes match, plus a fixed ≤10× duration extrapolation limit, **to achieve** affordable pathfinder sizing without sacrificing scaling confidence, **accepting** the schedule delay of a minimum 10% physical life test.

- **Warrant:** Physics regimes can be "mathematically proven" to match at sub-scale, whereas wear is empirical and non-linear.
- **Qualifier:** The position holds only where governing dimensionless parameters can be isolated and matched in a ground facility.
- **Accepted downside:** A schedule constraint from early long-duration testing.

## Decision-quality audit

**Claude Opus 5.5, Round 1.** Votes: APPROVE (Claude, Gemini), NEUTRAL (GPT).
- **Weakest link named:**
  - Information, by Claude's self-vote: arithmetic slips. Claude's vote states O4 should total 3.80, O0 2.10 and O1 2.60; the ranking is unchanged.
  - Reasoning, by GPT: the 100× backstop lacks evidence connecting it to acceptable risk, and this could change the O4 versus O5 choice.
- **Missing or unsupported scaffold steps:**
  - The scaffold was complete: criteria before options, a true null, must-screening, sensitivity separated from trade-off, calibrated certainty, falsifiable assumptions, ACH, Toulmin and consequences.
  - The specific thresholds rest on evidence Claude itself rated "Low" (the 10× heuristic) or did not source (the 100× backstop).
- **Trade-off points (values questions):**
  - T1: false pass versus false fail, that is, how much pathfinder money gate protection is worth.
  - T2: auditability versus physical fidelity.
  - T3: schedule versus life evidence.
  - Whether a non-waivable backstop should exist is presented as a values disagreement with GPT, not a fact to be settled.

**Gemini 3.1 Pro, Round 1.** Votes: REJECT (Claude, Gemini, GPT).
- **Weakest link named:**
  - Alternatives, by Claude and Gemini's self-vote: there is no true null, because Claude's proposal is mislabelled as the null.
  - Information, by GPT: the near-certainty claim that wear needs at least 10% physical runtime is unsupported, yet it drives the duration cap.
- **Missing or unsupported scaffold steps:**
  - no genuine null option;
  - a qualitative assessment matrix without scores;
  - swing ranges not calibrated (Gemini's self-vote);
  - certainty not calibrated ("virtually certain" for the 10% life claim; regimes "mathematically proven" to match);
  - no backstop and no treatment of modular numbering-up (Claude);
  - no explicit list of evidence that would change the ruling, beyond the falsification conditions on its assumptions.
- **Trade-off points (values questions):**
  - Cost weighted at 40%, equal to risk. Claude's vote said this is not reconciled with D-02's no-waiver, one-way-gate stance.
  - This weighting is a values divergence: the cost weights are Claude 15%, GPT 25% and Gemini 40%.

**GPT-6.1 Sol, Round 1.** Votes: APPROVE (Claude, Gemini, GPT).
- **Weakest link named:**
  - Commitment, by GPT's self-vote: technology-specific acceptance thresholds remain to be set.
  - Reasoning, by Claude: lack of a hard backstop, though Claude judged this "a defensible values position" because it is explicitly conditioned on effective review.
- **Missing or unsupported scaffold steps:**
  - The scaffold was complete, with non-compensable requirements stated first.
  - GPT rated its own cost-saving claim (that E is cheaper than P or F for equivalent assurance) as "Low certainty".
  - It deliberately gave P and E equal readiness-protection scores, stating there is no Dyson evidence that either produces fewer false passes.
- **Trade-off points (values questions):**
  - how much pathfinder spend is justified to reduce residual uncertainty;
  - how much reviewer discretion is acceptable;
  - whether to prefer a smaller, demonstrable 0B architecture over a larger, less supportable one.

## Key Points

- **Hard universal 10× cap rejected.** All three models rejected it. Claude and GPT gave the same two reasons: regime transitions can occur inside small factors (GPT: "a 3× change can cross an instability threshold"), and replicated modules can legitimately scale far beyond 10×.
- **Null option rejected.** Claude and GPT rejected leaving the split. Their reasons: it defers the standard to the gate, after pathfinders are sized; it invites gate-time negotiation; and it gives no basis for sizing pathfinders. Claude also argued it is "a waiver by another name".
- **Agree the standard before the data.** Claude (a frozen Scaling Basis at the 0A mid-term review) and GPT (a pre-agreed evidence plan and pre-declared prediction tests) both require this. They differ on firmness. Claude freezes the basis, and post-data changes reset the evidence clock. GPT treats the mid-term review as the point to revise test scale while it is still reversible.
- **Numbering-up versus scale-up.** Claude and GPT agreed that replication carries different risks, namely interaction, coupling, shared resources and correlated faults. Claude specified an interaction test of at least 4 units or a representative cell, with an SRU defined by governing physics. Gemini did not address this.
- **Duration.** All three accepted partial test plus a degradation model. Claude and GPT both require mechanism invariance for accelerated credit. Gemini and Claude both set a 10% of design life minimum physical test; Claude's version is the larger of 10% or the time to reach 25% of the failure criterion. GPT argued that "a single 'hours multiplier' is insufficient" and that different damage modes may need different tests.
- **A sub-10× factor is not an automatic pass.** GPT's rule text gives no credit to unsupported extrapolation even below 10×. Claude's ≤10× tier still requires a model correlated to test data.
- **Envelope and configuration control (GPT).** Readiness credit is limited to a specified deployment configuration. Demand cannot enlarge readiness credit, and material changes trigger reassessment after approval.
- **Pathfinder sizing (Claude).** Claude's rule converts directly into minimum test scales: full scale ÷ 100 as an absolute floor, or ÷ 10 without a regime case. It also pushes designs towards modular SRUs.
- **TRL definitions.** Claude rated as "High" certainty that ISO 16290/ECSS and NASA NPR 7123.1 set no numerical scale limit, so any factor would be a programme supplement. GPT's position is consistent with this.

## Unresolved Questions

1. **Backstop.** Should a non-waivable ceiling (Claude: 100×) exist for single-unit extrapolation, or should no number bind (GPT, Gemini for power and throughput)? Claude and GPT both framed this partly as a values question.
2. **Default presumption.** Should 10× be a burden-shifting default (Claude), or at most a non-binding planning heuristic that confers no gate entitlement (GPT)?
3. **Regime matching.** Is matching dimensionless regimes sufficient on its own (Gemini), or must it be accompanied by anchor tests and validated prediction (Claude, GPT)? GPT's vote held that it is treated as stronger assurance than warranted.
4. **Duration minimum.** Is a 10% physical life minimum justified as a general rule? Gemini and Claude both proposed it; GPT challenged its evidence base.
5. **Review independence.** Can genuinely independent review be staffed (Claude A3; GPT's first assumption)? Both models said their rulings change if it cannot.
6. **Cost versus protection weight.** How much should pathfinder cost weigh against one-way-gate protection (15% / 25% / 40% across the models)?
7. **Linked definitions.** The SRU boundary, the mandatory combined environments within "relevant environment", and freezing the project-ending technology list. Claude raised all three as dependencies.

## Recommended Actions

1. **Owner rules on the backstop question explicitly** (Claude's T1/T2; GPT's discretion trade-off). The options are: (a) a non-waivable single-unit ceiling, or (b) no binding ratio, conditioned on demonstrated review effectiveness.
2. **Adopt the common ground now:**
   - reject the null and a hard universal 10× cap;
   - require each project-ending technology to submit a scale-and-life evidence plan or Scaling Basis, reviewed at the 0A mid-term review before major pathfinder spend (Claude, GPT);
   - require mechanism-invariant acceleration for any accelerated life credit (all three);
   - treat numbering-up with interaction tests (Claude, GPT).
3. **Decide the freeze semantics.** Choose between Claude's frozen basis with a reset clock and GPT's revisable test scale at the mid-term review.
4. **Confirm review staffing independent of pathfinder teams.** Claude and GPT both conditioned their positions on this. If it cannot be staffed, Claude would move to a hard cap and GPT's own sensitivity analysis favours the presumptive option.
5. **Commission evidence that would move the ruling:**
   - blind or pre-declared cross-scale prediction tests on representative Dyson technologies (GPT; Claude's trigger 2 would raise the default to about 30× with a 300× backstop);
   - tracking of regime-case failures during 0A (Claude's trigger 1: two or more failures, move to a hard 10× cap);
   - tests of accelerated-life mechanism invariance (Claude trigger 3; GPT);
   - inter-reviewer reproducibility checks (GPT).
6. **Resolve the linked owner choices together:** the SRU definition, the combined-environment set within "relevant environment", and freezing the project-ending technology list (Claude).
7. **Ask the panel to source the 10% life minimum.** The owner should ask Gemini and Claude for its basis before adopting it, given GPT's challenge.

```yaml
questionId: "rq-0-71"
topics:
  - id: hard-backstop
    topic: Whether a non-waivable single-unit extrapolation ceiling should exist
    positions:
      - statement: Single-unit extrapolation above 100× never satisfies TRL 6, regardless of argument; some number must exist that argument cannot cross at a no-waiver one-way gate
        models: [Claude Opus 5.5]
        evidence: Models validated over two orders of magnitude rarely hold over three for novel hardware; refusing to state a number moves it into reviewers' heads; backstop flagged as low-confidence sensitivity point S2
      - statement: No universal ratio establishes or prohibits acceptance; readiness credit limited to an evidence-bounded deployment envelope with independent concurrence
        models: [GPT-6.1 Sol]
        evidence: Ratio is neither sufficient nor necessary evidence of representativeness; no evidence links 100× to acceptable risk; NASA-STD-7009 and NASA/SP-2016-6105 credibility disciplines
      - statement: No fixed limit for power and throughput if governing dimensionless regimes match
        models: [Gemini 3.1 Pro]
        evidence: Physics regimes can be shown to match at sub-scale via dimensionless numbers; fixed limits drive pathfinder costs beyond Phase 0 budgets
    resolution_status: open
    priority: critical
  - id: default-presumption
    topic: Role of a 10× default for single-unit scale-up
    positions:
      - statement: 10× is a burden-shifting default; 10–100× requires a pre-registered regime case, an intermediate anchor test and independent review
        models: [Claude Opus 5.5]
        evidence: Practitioner heuristic of about 10× per step (rated low certainty); scale-up failures cluster at regime changes (Merrow et al. pioneer plant studies, moderate certainty)
      - statement: 10× is at most a temporary planning heuristic and confers no gate entitlement; unsupported extrapolation below 10× earns no credit
        models: [GPT-6.1 Sol]
        evidence: A 3× change can cross an instability threshold; replication can make larger factors less risky than modest unit scaling
    resolution_status: open
    priority: high
  - id: regime-sufficiency
    topic: Whether regime matching alone justifies extrapolation
    positions:
      - statement: Matching dimensionless parameters suffices for power and throughput extrapolation
        models: [Gemini 3.1 Pro]
        evidence: Regimes can be mathematically proven to match; qualified by the Froude-Reynolds conflict in 1g as a falsifier
      - statement: Regime preservation must be accompanied by validated prediction against independent or anchor data and quantified uncertainty
        models: [Claude Opus 5.5, GPT-6.1 Sol]
        evidence: Claude requires an anchor test at the geometric mean of test and full scale; GPT requires pre-declared prediction tests addressing model discrepancy; GPT's vote held that Gemini overstates regime-matching assurance
    resolution_status: partially-resolved
    priority: high
  - id: duration-rule
    topic: Duration and wear evidence standard
    positions:
      - statement: Real-time test of at least 10% of design life or 25% of the failure criterion; acceleration calibrated at 3 or more stress levels with mechanism invariance; at least 1.5× equivalent life; no credit beyond the demonstrated life
        models: [Claude Opus 5.5]
        evidence: Physics-of-failure practice; NSTAR and NEXT life-test history
      - statement: Duration extrapolation capped at 10× (at least a 10% physical life test)
        models: [Gemini 3.1 Pro]
        evidence: Claimed near-certain that wear cannot be modelled without 10% runtime, citing NASA EP qualification practice; GPT's vote said this was unsupported
      - statement: Partial plus accelerated testing only with a validated degradation model and acceleration relationship; no single hours multiplier; different damage modes may need different tests
        models: [GPT-6.1 Sol]
        evidence: Reliability-engineering reasoning (moderate certainty)
    resolution_status: partially-resolved
    priority: high
  - id: numbering-up
    topic: Treatment of modular replication versus single-unit scale-up
    positions:
      - statement: No limit on replication count if each smallest replicated unit (defined by governing physics) passes and interaction tests and coupling models bound the coupling effects
        models: [Claude Opus 5.5]
        evidence: Power-electronics and phased-array practice; interaction effects often under-tested
      - statement: Distinguish unit enlargement from replication; test shared-resource limits and correlated failures
        models: [GPT-6.1 Sol]
        evidence: Strong engineering basis; applicability depends on architecture (moderate certainty)
    resolution_status: partially-resolved
    priority: medium
  - id: pre-registration-firmness
    topic: Whether the scaling basis is frozen or revisable at the mid-term review
    positions:
      - statement: Scaling Basis frozen at the 0A mid-term review once accepted; post-data changes are recorded and reset the evidence clock
        models: [Claude Opus 5.5]
        evidence: Clinical-trial pre-registration evidence (transfer to engineering plausible but unmeasured); gate failures driven by advocacy
      - statement: Evidence plan agreed before major spend; test scale revised at the mid-term review while still reversible; configuration control triggers reassessment after approval
        models: [GPT-6.1 Sol]
        evidence: Non-compensable auditability requirement; deployment-envelope assumption
    resolution_status: partially-resolved
    priority: medium
  - id: cost-weighting
    topic: Weight of pathfinder cost against gate protection
    positions:
      - statement: Cost weighted at 15%, below one-way-gate protection at 30%
        models: [Claude Opus 5.5]
        evidence: D-01 frames Phase 0 as a capability programme, not a cost saving; D-02 reversibility principle
      - statement: Cost weighted at 25%, below readiness protection at 40%
        models: [GPT-6.1 Sol]
        evidence: Cost can determine whether 0A affordably preserves the 0B option
      - statement: Cost weighted at 40%, equal to technical risk
        models: [Gemini 3.1 Pro]
        evidence: Difference between 100 kW and 1 MW pathfinders is hundreds of millions and years; Claude's vote said this is not reconciled with D-02
    resolution_status: open
    priority: high
```