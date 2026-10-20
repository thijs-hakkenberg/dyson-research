---
questionId: "rq-0-70"
questionSlug: "licence-gate-redesign-reapply"
type: "discussion-conclusion"
generatedBy: "claude-opus-5-5"
generated: "2026-10-17"
framework: "18f503fe4ec6"
roundCount: 1
terminationReason: "unanimous-conclude"
role: "alternate synthesis"
---

## Summary

In round 1 all three models converged on the core ruling. A failed g-licence gate blocks 0B production with no waiver, but permits **one** bounded redesign and reapplication. A second failure, or exhausting the bounds, ends 0B and leaves "0A only, Earth supply". This is a change from the gate synthesis, where Claude and Gemini had treated failure as final.

- **Claude Opus 5.5** reconciled the change with D-02. A waiver passes the gate without meeting the criterion. A reapplication meets the same criterion later with a different design. Claude recorded its earlier terminal position as the owner's trade-off alternative (T1).
- **Gemini 3.1 Pro** adopted the bounded extension and dropped its earlier "0A only" position.
- **GPT-6.1 Sol** kept its position and framed it as separating reversible learning from irreversible commitment.

All three rejected the null option (leave the split) and open-ended or discretionary redesign. Claude and GPT gave sensitivity checks showing the bounded option beats immediate closure only by a narrow margin, and only if its bounds are credible.

The models did not converge on how the retry is bounded or who grants it:

- **Eligibility.**
  - Claude classifies failures into F1–F6 using thresholds frozen at pathfinder PDR, applied by an independent board not funded by 0B. Gross exceedance (> 10× the limit) and regulator refusal are terminal.
  - GPT makes eligibility conditional on a documented diagnosis, a regulator-informed evidence plan and a pre-approved cap, authorised by the owner.
  - Gemini voids the extension only if a fundamental technology change is needed.
- **Time box.** Gemini proposed 6 months, GPT 12 and Claude 18.
- **Site changes.** Gemini lists site adjustments as a permitted redesign. Claude and GPT treat a site change as a restart or rebaseline.

Votes favoured GPT's response (approved by all three) and Claude's (two approvals; GPT neutral). Gemini's response drew two neutrals and a rejection from GPT for a circular warrant.

## Decision record

The panel converged on the core rule. The open parameters are listed beneath the record.

**Y-statement (converged core).** *In the context of* D-01's gated 0B real option and D-02's no-waiver one-way KDP-0B gate, with the ≤ 1 t/yr figure (D-03) interim and unsigned and rq-0-41 open, *facing* a panel split between terminal failure and redesign-and-reapply, *we chose* to prohibit 0B production on g-licence failure while permitting at most one pre-bounded redesign and reapplication that returns to KDP-0B for full reassessment, *to achieve* preservation of a recoverable 0B option without relaxing the criterion or authorising unlicensed production, *accepting* a capped delay, a ring-fenced spend, and the possibility of closing 0B despite eventual technical promise. (All three models.)

**Warrant**

- **Claude:** D-02 makes the *criterion* and the *outcome of exhausting the rule* irreversible, not the first attempt. One capped, pre-committed retry does not lower the criterion. Unbounded or discretionary retries do.
- **GPT:** Reversible learning need not be prohibited just because irreversible commitment is blocked.
- **Gemini:** TRL 6 is already achieved, so failures are likely to be marginal. Both Claude and GPT disputed this warrant in their votes.

**Qualifier**

- **Claude:** "Presumably", given three assumptions:
  - failure classes can be assigned objectively;
  - one hardware iteration fits in about 18 months;
  - the 0A reserve can fund one rescue.
- **GPT:** Provided a credible, affordable regulatory recovery path exists. If the cap and deadline are not approved before the initial gate, failure defaults to closure.
- **Gemini:** Provided the licensing state permits rapid reapplication.

**Accepted downside**

- **Claude and GPT:** One unsuccessful attempt can consume money and delay closure.
- **GPT:** A hard sunset can discard a design that might eventually become licensable.
- **Claude:** Regulator refusal (F4) ends 0B even when the regulator, not the engineering, is the obstacle. Claude says this is intended.

**Open parameters.** Each position is stated as a sub-Y-statement.

- **Classified eligibility (Claude).** An independent board classifies the failure:
  - F1/F2 (inconclusive, or 1–10× the limit) and F5 (frequency coordination only) get one 18-month reapplication;
  - F3 (> 10× the limit, or an uncontained abnormal event) and F4 (refusal or an unachievable limit) are terminal;
  - F6 (no binding limit) is NOT READY. It is handled by D-01 option expiry and does not consume the retry.
- **Diagnosis-gated eligibility (GPT).** The owner may authorise one 12-month cycle only if all four conditions hold:
  - a documented diagnosis identifies a credible corrective action;
  - a regulator-informed evidence plan exists under rq-0-41;
  - a cap and deadline protected from 0A were fixed before the gate;
  - the revised design returns to KDP-0B for full reassessment.

  An incomplete licensing basis is "not ready" with an explicit sunset.
- **Short extension (Gemini).** One attempt of at most about 6 months, limited to throughput and containment scaling. Site adjustments are allowed. A fundamental technology change voids the extension.

## Decision-quality audit

| Response | Votes (weakest link named) | Missing or unsupported scaffold steps | Trade-off points (values, not facts) |
|---|---|---|---|
| **Claude Opus 5.5**, round 1 | Self: APPROVE (reasoning). Gemini: APPROVE (commitment). GPT: NEUTRAL (information). | Claude's self-vote found matrix arithmetic errors: O1 = 385 not 395, O2 = 230 not 260, O3 = 340 not 345. Correcting them widens O4's lead. The self-vote also notes that scoring O1 at 5 on C3 is inconsistent with the claim that harm barely differs between options. GPT says the 10× F2/F3 threshold and the ranking of recoverable failure hypotheses lack supporting evidence, and that these determine eligibility. Claude's own certainty table rates the key claims low to very low. | T1: option value vs pre-commitment discipline. Claude asks that this be recorded, not averaged. T2: throughput reduction as a cure, i.e. how small a 0B is still worth doing. |
| **Gemini 3.1 Pro**, round 1 | Self: NEUTRAL (alternatives). Claude: NEUTRAL (reasoning). GPT: REJECT (reasoning). | Claude and GPT say the warrant is circular: TRL 6 is taken as evidence that failures are marginal, yet relevant-environment demonstration does not establish compliance with an independent regulatory limit. Claude adds four points: certainty is uncalibrated ("virtually certain", "absolute"); scoring is qualitative only; two options are dropped before assessment; the 6-month box is unjustified. Claude says site adjustments as a minor change conflict with licensing scope. Gemini's self-vote says it lacks a failure classification. | Option value vs schedule predictability. |
| **GPT-6.1 Sol**, round 1 | Self: APPROVE (information). Claude: APPROVE (information). Gemini: APPROVE (information). | Musts are kept outside the weighting, the arithmetic is correct and a sensitivity check is given (Claude). The weakest link is information: no costed remediation case and no regulator-informed recovery schedule. GPT itself rates the sufficiency of 12 months as "very low" certainty. Claude notes that GPT lacks objective failure-class thresholds and relies on owner-authorised diagnosis. | Option preservation vs expenditure discipline. Finality vs adaptability. Schedule certainty vs opportunity. |

**Questions of fact, not values**, which the models' evidence lists say data can settle:

- whether failure classes can be assigned reliably (Claude's inter-rater dry run);
- containment iteration time (Claude);
- whether the regulator imposes a cooling-off period after rejection (Gemini);
- remediation feasibility, cost and the regulatory timetable (GPT).

## Key Points

- **Unanimous in round 1:** no 0B production after failure; one bounded reapplication; a second failure is terminal; the null and open-ended options are rejected.
- **Retry versus waiver:**
  - Claude and GPT both argue a retry is not a waiver under D-02, because the criterion is unchanged.
  - Both make the binding rq-0-41 limit authoritative over the interim D-03 figure.
  - Claude adds that the programme never relaxes the limit to produce a pass (G-LIC-F.7).
- **Missing binding limit:** Claude and GPT both separate "not ready" from "failed".
  - Claude: not-ready does not consume the retry and hands over to D-01 option expiry.
  - GPT: not-ready requires an explicit hold with a sunset.
- **Pre-commitment timing:**
  - Claude: D-03 must be signed and the F1–F5 thresholds frozen before pathfinder PDR. Otherwise the rule degrades to the null option.
  - GPT: the cap and deadline must be approved before the initial gate, or failure defaults to closure.
- **Re-running other gates:**
  - Claude: a throughput reduction requires g-economics and g-demand to be re-run and passed.
  - GPT: every resubmission returns to KDP-0B with all affected technology, target, demand, economics and licence evidence renewed.
- **Changes requiring a restart or rebaseline** (Claude and GPT): new process or chemistry, throughput increase, change of licensing jurisdiction.
  - Claude also lists a change of target body or site, and the addition of a project-ending technology.
  - GPT also lists a material site change and a new hazard class.
  - Claude adds an anti-forum-shopping clause: under a new state, the limit is no looser than the stricter of the original binding limit and the D-03 ALARP value.
- **Detection limit:** GPT calls Claude's ≤ 10% detection limit useful instrumentation discipline but insufficient alone to demonstrate compliance.
- **Frequency filings:** Claude says ITU and national filings must start during 0A for an F5 cure to fit any time box.

## Unresolved Questions

1. **Eligibility mechanism.** Should eligibility use objective classes applied by an independent board (Claude), or an owner-authorised diagnosis subject to conditions (GPT)? Neither model has evidence for Claude's 10× threshold, which GPT flagged.
2. **Time-box length.**
   - Gemini: 6 months. Gemini also said a box over 12 months makes hard-fail the winner.
   - GPT: 12 months, described as a governance proposal.
   - Claude: 18 months, an engineering estimate at low confidence, extendable to 24 if schedule data require it.
   - No regulator or test-facility schedule has been supplied.
3. **Site change.** Is a site change a permitted redesign (Gemini) or a restart or rebaseline (Claude, GPT)?
4. **Regulator refusal.** Is it always terminal (Claude, F4)? Or terminal only where a written determination finds no acceptable configuration (GPT's falsifier)?
5. **Reapplication and the regulator.** Will the licensing state treat reapplication neutrally (Claude A4)? Does it impose a cooling-off period (Gemini)?
6. **Funding.** Can the 0A reserve fund a repeat T08 campaign without breaching D-01? Claude A3 and GPT both say that if it cannot, choose closure honestly.
7. **Escape floor.** Does the containment architecture have an escape floor near the limit? Claude says this would promote H-phys and favour terminal failure.
8. **Owner's T1 value judgement.** If the owner rules that any post-failure deliberation is corrosive, Claude says terminal failure is legitimate.

## Recommended Actions

1. **Ratify the converged core rule** in `decisions.md` and record the Claude/Gemini terminal position as the T1 alternative (Claude).
2. **Have the owner set the time box, expenditure cap and ring-fenced funding line before the initial KDP-0B.** Adopt GPT's default: if these are not set, failure means closure.
3. **Choose the eligibility mechanism.** Before adopting Claude's classes, run Claude's dry run. If two independent reviewers disagree in more than 1 in 5 cases, sharpen the thresholds or fall back to terminal.
4. **Advance D-03 signature and rq-0-41.** Claude needs this before pathfinder PDR. GPT needs a regulator-informed evidence plan covering particle and velocity classes, confidence level, averaging interval and abnormal-event limits.
5. **Settle the redesign scope list**, especially site change, and decide whether to adopt Claude's anti-forum-shopping clause.
6. **Move ITU and national frequency filings into 0A** (Claude).
7. **Obtain the deciding evidence:**
   - 0A containment-module build-test cycle data (Claude);
   - ground or vacuum-chamber escape-floor data (Claude);
   - the licensing state's resubmission rules and any cooling-off period (Gemini, Claude);
   - a costed remediation case with an updated demand and economics case after derating (GPT).
8. **Recheck the 0A reserve against the cost of a repeat T08 campaign** (Claude A3, GPT).

```yaml
questionId: "rq-0-70"
topics:
  - id: core-failure-ruling
    topic: Is g-licence failure final, or may 0B be redesigned and reapplied?
    positions:
      - statement: Failure prohibits 0B production with no waiver, but permits one bounded redesign and reapplication that returns to KDP-0B; a second failure or exhausted bounds closes 0B (0A only, Earth supply).
        models: [Claude Opus 5.5, Gemini 3.1 Pro, GPT-6.1 Sol]
        evidence: A retry meets the unchanged criterion later and is not a waiver (Claude, GPT); D-01 keeps 0B as a real option; escalation-of-commitment literature supports bounded rather than open retries (Claude, moderate certainty); sensitivity checks show the margin over closure is narrow (Claude 400 vs 385 after its self-vote correction; GPT 4.00 vs 3.80).
      - statement: Any first failure ends 0B. This was the prior gate-synthesis position, now retained only as the owner's T1 trade-off alternative.
        models: [Claude Opus 5.5]
        evidence: Absolute pre-commitment discipline; legitimate if the owner judges any post-failure deliberation corrosive, or if the classification dry run shows poor inter-rater agreement.
    resolution_status: resolved
    priority: critical
  - id: retry-eligibility-mechanism
    topic: How eligibility for the single retry is determined
    positions:
      - statement: An independent board not funded by 0B classifies the failure using thresholds frozen at pathfinder PDR. F1, F2 and F5 get one retry; F3 (>10x the limit or an uncontained abnormal event) and F4 (refusal or unachievable limit) are terminal; F6 is NOT READY.
        models: [Claude Opus 5.5]
        evidence: ACH ranks metrology and fixable engineering defects as the least-disconfirmed failure causes; a tenfold retention gain is judged not credible within one iteration. GPT noted the 10x threshold lacks supporting evidence.
      - statement: The owner may authorise one retry only with a documented diagnosis, a regulator-informed evidence plan, and a cap and deadline set before the gate. Non-remediability, as in a written regulatory determination, closes 0B.
        models: [GPT-6.1 Sol]
        evidence: Governance distinction between reversible learning and irreversible commitment; probability of successful correction rated not estimable.
      - statement: Retry is allowed unless a fundamental technology change is required.
        models: [Gemini 3.1 Pro]
        evidence: Warrant that TRL 6 implies marginal failures; Claude and GPT judged this warrant circular.
    resolution_status: open
    priority: high
  - id: time-box-length
    topic: Length of the bounded extension
    positions:
      - statement: About 6 months; a box over 12 months makes hard-fail the better choice.
        models: [Gemini 3.1 Pro]
        evidence: Schedule predictability for D-01 demand sizing; Claude called the figure unjustified.
      - statement: 12 months from recorded failure, set before the initial gate.
        models: [GPT-6.1 Sol]
        evidence: A governance proposal, not evidence-derived; sufficiency rated very low certainty.
      - statement: 18 months from classification, extendable to 24 if schedule data require it.
        models: [Claude Opus 5.5]
        evidence: One containment hardware iteration plus a repeat T08 campaign is plausibly 12-18 months (low-confidence engineering estimate).
    resolution_status: open
    priority: high
  - id: permitted-redesign-scope
    topic: Which changes are permitted without restarting KDP-0B
    positions:
      - statement: Containment hardware, procedures and duty cycle, instrumentation and throughput reduction (with economics and demand re-run) are permitted. Site, architecture or chemistry change, an added project-ending technology, a throughput increase or a licensing-state change require a full new KDP-0B.
        models: [Claude Opus 5.5]
        evidence: Site change re-opens g-target; architecture change is a restart.
      - statement: Containment changes or derating are permitted within the approved envelope with renewed evidence. A material site change, new process, throughput increase, new hazard class or changed jurisdiction requires owner-level rebaselining.
        models: [GPT-6.1 Sol]
        evidence: Only demonstrably unaffected evidence may be reused.
      - statement: Site adjustments, throughput throttling and containment sensor upgrades are permitted; changing the core particle-retention mechanism triggers hard fail.
        models: [Gemini 3.1 Pro]
        evidence: None given beyond the framework; Claude said site adjustments conflict with licensing scope.
    resolution_status: open
    priority: high
  - id: retry-authority
    topic: Who decides whether the retry is granted
    positions:
      - statement: An independent review board not funded by 0B.
        models: [Claude Opus 5.5]
        evidence: Classification can be gamed, so an independent classifier and pre-fixed thresholds are needed.
      - statement: The owner, subject to pre-approved conditions, with default closure if bounds are not set.
        models: [GPT-6.1 Sol]
        evidence: Explicit caps and sunset limit discretion (noted in Claude's vote).
    resolution_status: open
    priority: medium
  - id: not-ready-handling
    topic: Treatment when no binding limit exists at KDP-0B
    positions:
      - statement: Status is NOT READY, governed by D-01 option expiry; it does not consume the reapplication.
        models: [Claude Opus 5.5]
        evidence: Conflating not-ready with failure would let an unresolved regulator question consume the single retry.
      - statement: Status is not ready; it blocks KDP-0B and requires an explicit hold with a sunset, not an unlimited waiting category.
        models: [GPT-6.1 Sol]
        evidence: An incomplete licensing basis cannot count as passed.
    resolution_status: partially-resolved
    priority: medium
  - id: funding-and-default
    topic: Funding of the retry and the default when bounds are unset
    positions:
      - statement: A ring-fenced cost cap is set at KDP-0B entry; if the 0A reserve cannot fund a repeat T08 campaign, choose terminal honestly.
        models: [Claude Opus 5.5]
        evidence: Assumption A3 and its falsifier.
      - statement: The expenditure cap is protected from 0A and fixed before the initial gate; with no approved cap and deadline, failure defaults to closure.
        models: [GPT-6.1 Sol]
        evidence: Prevents improvised extensions after failure.
      - statement: Phase 0 schedule and budget carry a risk buffer (for example 6 months of holding costs).
        models: [Gemini 3.1 Pro]
        evidence: Schedule predictability.
    resolution_status: partially-resolved
    priority: medium
  - id: jurisdiction-change
    topic: Changing licensing state after failure
    positions:
      - statement: Requires a full new KDP-0B; under the new state the limit is no looser than the stricter of the original binding limit and the D-03 ALARP value (anti-forum-shopping).
        models: [Claude Opus 5.5]
        evidence: A project that only works under a lenient state is not licensable in D-02's sense.
      - statement: A changed licence jurisdiction requires owner-level rebaselining; it is not a minor correction.
        models: [GPT-6.1 Sol]
        evidence: Material change to the licence basis.
    resolution_status: partially-resolved
    priority: medium
  - id: verification-sufficiency
    topic: Adequacy of the detection-limit criterion for a pass
    positions:
      - statement: Pass requires uncertainty-bounded annualised escape, including credible failures, below the binding limit, a detection limit of at most 10% of the limit, T04/T08/T19 at TRL 6 and accepted frequency filings.
        models: [Claude Opus 5.5]
        evidence: Metrology immaturity is the least-disconfirmed failure hypothesis.
      - statement: The 10% detection limit is useful discipline but insufficient alone; the assurance case must cover normal operation, credible failures, measurement uncertainty and the statistical basis.
        models: [GPT-6.1 Sol]
        evidence: rq-0-41 sets particle and velocity classes, confidence, averaging interval and abnormal-event limits.
    resolution_status: partially-resolved
    priority: medium
  - id: frequency-coordination
    topic: Treatment of ITU and national frequency coordination shortfalls
    positions:
      - statement: A frequency-only shortfall (F5) gets an administrative cure inside the same box; filings must begin during 0A, because coordination for non-geostationary systems typically takes multiple years.
        models: [Claude Opus 5.5]
        evidence: ITU Radio Regulations timelines (low-moderate certainty).
    resolution_status: open
    priority: low
```