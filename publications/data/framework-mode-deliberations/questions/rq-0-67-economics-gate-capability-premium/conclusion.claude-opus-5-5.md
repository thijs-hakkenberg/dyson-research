---
questionId: "rq-0-67"
questionSlug: "economics-gate-capability-premium"
type: "discussion-conclusion"
generatedBy: "claude-opus-5-5"
generated: "2026-10-17"
framework: "18f503fe4ec6"
roundCount: 1
terminationReason: "unanimous-conclude"
role: "alternate synthesis"
---

## Summary

In this single round all three models converged on the core ruling. **The economics gate tests cost parity (R = 1 in effect), and any capability premium above Earth supply requires a separate, explicit owner decision.** A premium approved that way is not an economics pass.

- **GPT-6.1 Sol** restated its earlier panel position and developed it into rule text.
- **Claude Opus 5.5** moved off its earlier "R set by the owner inside the gate" position. It now treats parity as the in-gate test, with R > 1 reachable only through a separate decision (D-xx).
- **Gemini 3.1 Pro** abandoned its earlier "undercut" threshold. It rejected undercut as contradicting D-01 and endorsed GPT's position.

All three now agree that D-01 ("capability programme, not a cost saving") allows a premium in principle but does not itself authorise one or set its amount. They also agree that the null option, leaving the panel split as is, should be rejected.

The panel did **not** converge on **when** the premium decision is taken, and this is the most consequential remaining split.

- **Claude** argues the failure mode is the timing of R. If R can be set after the P70 estimate is known, the gate "cannot fail on cost". Claude therefore requires D-xx no later than the 0A mid-term review, priced and dollar-capped, with a default of R_max = 1.0 if the owner does not decide.
- **GPT** allows the premium decision "at the same KDP-0B meeting", provided it is recorded separately. GPT's rule text does require the ordinary-pass funding envelope and downside limits to be fixed "before gate adjudication".
- **Gemini** treats deciding at KDP-0B as a benefit: it "enables the owner to dynamically assess the value of the capability premium at the exact moment of the KDP-0B decision."

Claude's vote flagged both GPT and Gemini on this point. GPT, in turn, criticised Claude's operational exceptions: late amendments, ratio relaxation in the low-launch-price scenario, and the market-backed exemption from the dollar cap.

Votes favoured GPT's response (three APPROVE) and Claude's response (two APPROVE, one NEUTRAL). Gemini's response received three NEUTRAL votes, mainly for unshown scoring arithmetic and a disputed claim about how a falling Earth benchmark affects the absolute premium.

## Decision record

**Converged core (all three models).**

> **In the context of** a one-way KDP-0B gate for a programme declared a capability programme, not a cost saving (D-01), under D-02's "stringency follows reversibility",
> **facing** cost estimates dispersed from the $15.7B BOM to $22–195B (panel), and an Earth-supply baseline that moves with launch price,
> **we chose** a parity-based economics finding (R = 1 for an ordinary pass), with any above-parity capability premium authorised only by a separate, explicit, bounded owner decision,
> **to achieve** a gate that can fail on cost, explicit owner accountability for any subsidy, and a preserved route to buying capability,
> **accepting** extra approval work and the possibility of proceeding with a disclosed adverse economics finding.

- **Warrant.** In GPT's words, "capability value can justify investment without demonstrating cost competitiveness. Keeping those propositions separate prevents a strategic rationale from silently changing a cost threshold." Claude's version: "any threshold that can be chosen after the evidence is known stops being a test."
- **Qualifier.**
  - GPT: the ruling holds unless the full D-01/D-02 text already delegates premium authority, or Earth supply proves not to be a comparable alternative.
  - Gemini: it holds provided parity is not physically impossible under any model.
  - Claude: "likely" the right structure, with moderate confidence, because the behavioural evidence comes from analogous domains.
- **Accepted downside.** GPT: a strategically meritorious project carries an explicit adverse economics finding, and this is "useful disclosure, not a defect". Gemini: two-step approval friction.

**Divergent sub-positions on the timing and form of the premium decision.**

- **Position T1 (Claude Opus 5.5).**
  > In the context of a one-way gate, facing escalation-of-commitment risk, we chose a premium decision (D-xx) taken by the 0A mid-term review, capped by both R_max and an absolute ΔC_max, tied to named benefits, defaulting to R_max = 1.0, and unalterable by gate reviewers, to achieve pre-commitment integrity, accepting that a capability discovered late in 0A cannot be credited without a recorded amendment made before the KDP-0B package is assembled.
- **Position T2 (GPT-6.1 Sol).**
  > In the context of separate economics and investment findings, we chose to allow premium authorisation at or before KDP-0B, recorded separately, specifying the capability purchased, beneficiaries, alternatives, maximum incremental premium, total envelope, downside acceptance and stop/review triggers, with an absolute cap not reduced to a ratio, to achieve transparency without delaying commitment, accepting additional approval work.
- **Position T3 (Gemini 3.1 Pro).**
  > We chose a premium decided at KDP-0B as an "explicit executive exception" using a standard "Capability Premium Justification" template, to achieve assessment against the latest signed demand, accepting governance friction.

## Decision-quality audit

| Response (Round 1) | Votes | Weakest DQ link named | Missing or unsupported scaffold steps | Trade-off points (values, not facts) |
|---|---|---|---|---|
| **Claude Opus 5.5** | APPROVE (Claude, Gemini); NEUTRAL (GPT) | **Information** (self-vote); **commitment** (GPT) | All nine steps present, with criteria stated before options, a null option and a re-weighting check. GPT judged the operational rule to weaken its own commitments in three ways: late amendments undercut pre-evidence freezing; the L-low rule waives the ratio ceiling; market-backed premiums escape ΔC_max without equivalent funding safeguards. The self-vote noted that the ±30% readiness band and the L-low rule "rest on somewhat assumed calibration". | T1 capability against cost; T2 gate integrity against flexibility. Claude labels both explicitly as values questions. |
| **Gemini 3.1 Pro** | NEUTRAL ×3 | **Reasoning** (Claude, GPT); **alternatives** (self) | Weighted scores (4.7 and 8.5) come from Low/Medium/High labels with no shown arithmetic (Claude). Option 1 is described as both pre-set and "hidden" (Claude, GPT). Evidence and assumptions are thin (Claude). The null option was rejected quickly (self). GPT says the sensitivity claim is reversed: with fixed R and quantity, a lower Earth benchmark *reduces* the permitted absolute premium. GPT judged that correcting these points could change the option ranking. | Governance friction against financial transparency. |
| **GPT-6.1 Sol** | APPROVE ×3 | **Commitment** (Claude); **information** (self); none (Gemini) | Claude noted the premium may still be authorised at KDP-0B after the evidence is seen, and that Option C scores 3.8, not 3.75. The self-vote noted the underlying decision text was not inspected; GPT qualifies this explicitly and pairs it with falsifiers. | Capability against expenditure; risk against early commitment; decision speed against assurance. |

**Divergences that are facts to settle, not values questions:**

- Whether a falling Earth-supply benchmark raises or lowers the absolute premium allowed under a fixed R. Gemini holds one view. GPT and Claude (S1) hold the other: a fixed R implies a moving absolute premium, which is why both want a dollar cap.
- Whether "±30%" is meaningful without a stated confidence level, scope and validation method. GPT says it is not. Claude uses it as a readiness precondition.
- Whether Earth supply is an equivalent comparator in quality, availability and schedule (GPT A2; Claude A2).

**Divergence that is a values or governance question:** the timing of the premium decision (T1 against T2/T3). It trades pre-commitment integrity against flexibility to use the latest evidence.

## Key Points

**Convergence on the core ruling**

- All three models: R = 1 for an ordinary economics pass. A premium is permissible but needs a separate owner decision, and D-01 does not by itself authorise one.
- All three models reject the null option.
  - Claude: the R value would be set "by whoever is in the room" after the estimate.
  - GPT: it "invites selection of the favourable interpretation at KDP-0B".
  - Gemini: it renders the gate "un-executable".
- All three models now reject strict undercut.
  - Claude: it double-counts margin, because the test already compares P70 against P50.
  - GPT: it needs a justified margin, not an arbitrary one.
  - Gemini: it violates D-01.
  - Claude still lists Gemini's undercut as a retained "conflict", although Gemini has itself withdrawn it.

**Absolute cap and reporting**

- Claude and GPT: an absolute dollar cap is required alongside, or instead of, a ratio. GPT says the implied R should be reported but "is not itself the probability of beating Earth supply".
- Claude and GPT: report the parity verdict separately from any premium-authorised verdict or authorisation.

**Gate structure and fallback**

- GPT, and implicitly Claude: premium approval never waives D-02's TRL 6 no-waiver rule or the target, demand and licence gates.
- Claude: introduces a "NOT READY" verdict, distinct from FAIL, for when the estimate band or comparator spec is not met. Both verdicts route to the fallback "0A only, Earth supply".
- GPT: an economics failure without authorisation invokes the same fallback.

**Comparator and scenarios**

- Claude: launch-price scenarios (L-low, L-central, L-high) frozen at the 0A mid-term review.
- GPT: predeclared core scenarios, with a "non-contingent economics pass" required to survive all of them. Results that hold only under some scenarios become conditional findings or require premium authorisation.
- GPT: the cost basis must be consistent. Forward avoidable costs are compared with each other, sunk costs are disclosed separately, and project marginal cost is never compared with Earth full-service cost.

**Coupling with demand**

- Claude: demand signed at above-Earth prices makes a premium "market-backed" and exempt from ΔC_max.
- GPT: warns against double-counting a capability benefit already included in customer payments (A3), and criticised the exemption for lacking funding safeguards.

## Unresolved Questions

1. **Timing of the premium decision.** It could be fixed before the 0B evidence (Claude: by the 0A mid-term review, frozen) or taken at the KDP-0B meeting (GPT: allowed; Gemini: preferred). If amendments are allowed, what is the latest point at which they can be made?
2. **Exceptions.** Should the low-launch-price scenario allow the ratio to exceed R_max while the dollar cap holds (Claude's proposal; GPT objects)? Should market-backed premiums escape ΔC_max?
3. **Absolute premium under a falling benchmark.** In which direction does a falling Earth benchmark move the absolute premium under a fixed R (Gemini against GPT)?
4. **Estimate band.** What confidence level, scope and validation method gives "±30%" meaning (GPT), and can it be reached by KDP-0B (Claude A3)?
5. **Ownership of the comparator.** Who owns the Earth-supply reference architecture, and is $/kg parity an adequate comparator if equivalent quality, schedule or assured availability cannot be bought from Earth (Claude A2, GPT A2)?
6. **D-01 text.** Does the full accepted D-01 text already delegate any premium authority? GPT did not inspect the file and flags this as its main falsifier.
7. **Value of R, if any.** This is a values call reserved to the owner. Claude's non-binding guidance is R_max ≤ about 1.5, no ratio-only premium, and ΔC_max no higher than the cost of buying the benefit directly. Claude also notes that a premium inside about 1.3 is "mostly estimate noise".

## Recommended Actions

1. **Record the converged ruling as an owner decision** (all three models). The economics gate tests parity (R = 1), and above-parity expenditure is not an economics pass and requires a separate, bounded owner authorisation.
2. **Owner to rule on premium timing** (T1 against T2/T3). This should be an explicit trade-off decision between pre-commitment integrity and flexibility. Claude's proposed default, if no D-xx is taken, is R_max = 1.0, ΔC_max = 0.
3. **Specify the contents of any premium authorisation.**
   - From GPT: capability purchased, beneficiaries, alternatives, maximum incremental premium, total funding envelope, downside acceptance, stop/review triggers.
   - From Claude: named benefits, each with the evidence that would show it was delivered, plus an absolute dollar cap.
4. **Resolve Claude's exceptions** (L-low ratio relaxation, market-backed exemption, late amendment) against GPT's objections before the rule text enters `gates-proposal.yaml`.
5. **Commission an owned Earth-supply reference spec** (Claude, GPT). It should cover equivalent service specification, transfer stage and predeclared launch-price, demand, utilisation, replacement and delay scenarios. Claude proposes freezing it at the 0A mid-term review.
6. **Reconcile the $15.7B BOM against the $22–195B panel range during 0A** (Claude, GPT). Use a common cost breakdown and an independent estimate. Define the confidence level, scope and validation method behind any accuracy band before using it as a readiness precondition (GPT).
7. **Settle the factual dispute** over how a falling Earth benchmark affects the absolute premium under a fixed R (Gemini against GPT/Claude) before it is used to argue for one governance option over another.
8. **Verify the full D-01/D-02 text** for any existing premium delegation (GPT A1).

```yaml
questionId: "rq-0-67"
topics:
  - id: premium-locus
    topic: Whether a capability premium can pass inside the economics gate or needs a separate owner decision
    positions:
      - statement: Economics gate tests parity (R = 1); any premium above parity requires a separate, explicit, bounded owner decision and is not an economics pass
        models: [Claude Opus 5.5, Gemini 3.1 Pro, GPT-6.1 Sol]
        evidence: D-01 states purpose but sets no premium amount or authority; D-02 irreversible-gate discipline; a threshold adjustable at the gate cannot fail; cost dispersion $15.7B BOM vs $22-195B panel
    resolution_status: resolved
    priority: critical
  - id: premium-timing
    topic: When the premium decision must be taken relative to the 0B cost evidence
    positions:
      - statement: Premium decision (D-xx) must be taken no later than the 0A mid-term review, frozen, capped in ratio and dollars, default R_max = 1.0; amendments only by recorded owner decision before the KDP-0B package is assembled
        models: [Claude Opus 5.5]
        evidence: Escalation of commitment (Staw 1976), megaproject overrun literature (Flyvbjerg), NASA 70% JCL practice with thresholds set before confirmation; an R set after the P70 is known makes the gate unable to fail on cost
      - statement: Premium may be authorised at the same KDP-0B meeting provided it is recorded as a separate finding; ordinary-pass funding envelope and downside limits fixed before gate adjudication
        models: [GPT-6.1 Sol]
        evidence: Separate findings with different warrants preserve auditability; avoids sequential delay (A4); decision-structure reasoning rather than Project Dyson outcome data
      - statement: Premium decided at KDP-0B as an explicit executive exception, letting the owner assess value with the latest signed Phase 1 demand
        models: [Gemini 3.1 Pro]
        evidence: Governance clarity and accountability weighted 45%; explicit sign-off at the gate
    resolution_status: open
    priority: critical
  - id: undercut-threshold
    topic: Whether 0B must undercut Earth supply
    positions:
      - statement: Strict undercut is rejected; it double-counts margin (P70 vs P50), adds false precision inside the estimate band, needs a justified margin, and contradicts D-01
        models: [Claude Opus 5.5, Gemini 3.1 Pro, GPT-6.1 Sol]
        evidence: D-01 "not a cost saving"; P70 vs P50 comparison already conservative; ±30% band noise (Claude)
    resolution_status: resolved
    priority: medium
  - id: rule-exceptions
    topic: Low-launch-price ratio relaxation, market-backed exemption and late amendments
    positions:
      - statement: In L-low the ratio may exceed R_max if the dollar cap holds; premiums covered by signed Phase 1 prices above Earth P50 do not count against dC_max; recorded amendments allowed before the KDP-0B package
        models: [Claude Opus 5.5]
        evidence: Prevents verdict flipping when the denominator collapses; signed above-Earth demand is market evidence for H-capability
      - statement: These exceptions weaken the pre-evidence freeze and the funding safeguards and could change approval; avoid double-counting benefits already in customer payments
        models: [GPT-6.1 Sol]
        evidence: Vote critique of Claude's response; assumption A3 on double counting
    resolution_status: open
    priority: high
  - id: ratio-vs-absolute-cap
    topic: Relationship between R and the absolute dollar premium under a moving Earth benchmark
    positions:
      - statement: A static R with falling Earth-supply costs could authorise massive absolute subsidies
        models: [Gemini 3.1 Pro]
        evidence: Arithmetic of relative multipliers on a fluctuating baseline
      - statement: With fixed R and quantity, a lower Earth benchmark reduces the permitted absolute premium; ratio and absolute cap answer different questions, so an absolute cap is required and R is reported only
        models: [GPT-6.1 Sol]
        evidence: Vote correction of Gemini; rule text item 4 and the reporting guidance
      - statement: A fixed R implies a moving absolute premium, so the ratio and the dollars must both be capped
        models: [Claude Opus 5.5]
        evidence: Sensitivity point S1 (launch $/kg roughly $1,500 to $200 to LEO)
    resolution_status: partially-resolved
    priority: medium
  - id: estimate-readiness
    topic: Estimate-band precondition and NOT READY verdict
    positions:
      - statement: Require a 0B estimate band of ±30% or better before the gate is evaluable; otherwise verdict NOT READY (distinct from FAIL), routed to the fallback 0A only, Earth supply
        models: [Claude Opus 5.5]
        evidence: Current dispersion roughly 9x, far beyond ±30%; R values between about 0.8 and 1.3 cannot be told apart inside the band
      - statement: ±30% is not meaningful assurance without a stated confidence level, cost scope and validation method; reported spread is not a probability distribution; reconcile estimates before asserting a calibrated P70
        models: [GPT-6.1 Sol]
        evidence: Evidence-certainty table; low confidence in current P70 calibration
    resolution_status: partially-resolved
    priority: medium
  - id: comparator-definition
    topic: Definition and ownership of the Earth-supply counterfactual and scenario set
    positions:
      - statement: Owned Earth-supply reference spec with three launch-price scenarios, frozen at the 0A mid-term review
        models: [Claude Opus 5.5]
        evidence: Assumption A2; the denominator is unowned otherwise
      - statement: Comparator must match material quality, availability and schedule on a common price base and consistent avoidable-cost scope; a non-contingent pass must survive the predeclared core scenarios
        models: [GPT-6.1 Sol]
        evidence: Sensitivity points 1-5; rule text items 1-2
    resolution_status: partially-resolved
    priority: high
```