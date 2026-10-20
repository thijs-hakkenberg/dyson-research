---
questionId: "rq-0-74"
questionSlug: "d02-0a-milestone-trl-flight-projects"
type: "discussion-conclusion"
generatedBy: "claude-opus-5-5"
generated: "2026-10-17"
framework: "18f503fe4ec6"
roundCount: 1
terminationReason: "unanimous-conclude"
role: "alternate synthesis"
---

## Summary

The panel ran one round and partly converged. All three models (Claude Opus 5.5, Gemini 3.1 Pro, GPT-6.1 Sol) accepted D-02's principle, "stringency follows reversibility". All three said the label "internal 0A milestone" does not make a gate reversible, because a 0A launch, and the hardware commitment before it, is one-way. All three kept TRL 4–5 for the MTR as a two-way tranche release. All three placed a separate, stricter technology gate at each scout or pathfinder PDR, so that passing the MTR cannot authorise flight. All three left KDP-0B's no-waiver TRL 6 requirement unchanged. Each also proposed rule text that changes D-02. Claude and GPT called this an explicit amendment. Gemini called it "amend D-02 interpretation".

The main split is over technologies whose flight is meant to mature them.

- **Claude and GPT** both divide each flight project's technologies into flight-enabling technologies and technologies under test (experimental). They differ in how the second group is gated:
  - **Claude** sets numeric floors: TRL 5 at PDR with a documented relevant environment, failure-mode ground tests before CDR, and TRL 6 for those failure modes at launch readiness.
  - **GPT** sets no TRL floor. It requires an approved demonstration assurance case and independent review of the boundary between the two groups.
- **Gemini** made no such distinction. It requires TRL 6 at PDR for all of a project's flight-critical technologies.

Claude also proposed provisions that no other model endorsed:

- a pathfinder cost-share trigger (25 % of the 0A budget, an owner value), above which pathfinder PDR becomes a no-waiver one-way gate;
- owner-signed Class D waivers for scout enabling technologies.

Votes favoured the Claude and GPT responses. GPT received three APPROVE votes. Claude received two APPROVE votes and one NEUTRAL from GPT, which disputed Claude's argument that TRL 6 at PDR is circular and asked for better justification of the TRL 5 exception and the 25 % threshold. Gemini received two REJECT votes and one NEUTRAL (its own), mainly for a missing null option, an unweighted matrix and uncalibrated certainty.

## Decision record

The panel converged on a common core but not on the full rule. The shared core is stated first, then one Y-statement per position.

**Shared core (Claude, Gemini, GPT)**
- MTR and other tranche releases are two-way: TRL 4–5 suffices to release funding.
- A scout or pathfinder PDR, or any earlier irreversible hardware commitment, is a separate gate. It needs TRL 6 for flight-enabling or flight-critical technologies.
- Passing the MTR does not authorise flight.
- KDP-0B is unchanged.
- The null option, "leave the split", is rejected. Claude and GPT rejected it explicitly. Gemini's Option A was a relabelled panel position rather than a true null.

**Position 1: role × commitment, with numeric floors (Claude Opus 5.5)**
> In the context of Phase 0A, which funds both reversible tranches and irreversible flight projects, facing a panel split over whether D-02's TRL 4–5 applies to scout and pathfinder gates, we chose to classify gates by what they commit and technologies by their role in the flight. That means TRL 4–5 for MTR tranches. At PDR, enabling technologies need TRL 6, and technologies under test need TRL 5 plus a relevant-environment definition. Before CDR, failure-mode ground tests are required. At launch, the flight system must be qualified and accepted. A pathfinder above 25 % of the 0A budget falls under the KDP-0B rule. Scouts may take Class D waivers. We chose this to avoid the documented post-PDR cost-growth pattern while keeping 0A's learning tempo. We accept a classification judgment at SRR that can be gamed, a modest extra ground-test bill, and an amendment to an accepted decision.

- **Warrant:** irreversibility belongs to the commitment, not the phase. Gate stringency should also stop short of requiring the evidence the gate exists to produce.
- **Qualifier:** "probably right" for the pathfinder (medium confidence) and "plausibly right" for small scouts (low–medium).
- **Rebuttal:** if cheap, rapid reflight exists, scout launches become near two-way and the scout rule relaxes.

**Position 2: function-specific amendment with a demonstration assurance case (GPT-6.1 Sol)**
> In the context of D-01's capability programme and D-02's consequence-sensitive gates, facing ambiguous treatment of 0A flight projects, we chose a function-specific amendment. It separates reversible development releases (TRL 4–5, not flight authorisation) from flight-enabling readiness (TRL 6 by PDR or by an earlier irreversible commitment, with qualification and acceptance before launch and TRL 8 as the target for the completed system). Experimental technologies may fly below those levels only under an approved, independently reviewed assurance case. We chose this to achieve useful learning without weakening assurance on irreversible commitments. We accept extra governance work and explicit experiment-failure risk.

- **Warrant:** readiness must match the consequences of the authorised action, not its phase label.
- **Qualifier:** holds only where experimental failure is demonstrably bounded and the learning case is credible.

**Position 3: gate stratification without a technology-role distinction (Gemini 3.1 Pro)**
> In the context of the Phase 0 TRL re-baseline, facing a conflict between programme funding gates and flight-project physics, we chose to stratify gates. The MTR, a programme gate, releases funding at TRL 4–5. Each scout or pathfinder PDR, a project gate, requires TRL 6 in a relevant environment for that project's own flight-critical technologies. We chose this to release funding quickly while preventing premature hardware fabrication. We accept the administrative overhead of tracking project PDRs separately from the MTR.

- **Warrant:** bending metal for launch is irreversible, but the MTR is a two-way funding gate.
- **Qualifier:** none stated beyond "almost certain; high confidence". Two voters flagged this as uncalibrated.

## Decision-quality audit

| Response (Round 1) | Votes received | Weakest link named | Missing or unsupported scaffold steps | Divergences that are trade-off points (values) |
|---|---|---|---|---|
| **Claude Opus 5.5** | APPROVE (Claude, self), APPROVE (Gemini), NEUTRAL (GPT) | Information (self), commitment (Gemini), reasoning (GPT) | **Self-assessment:** the 25 % pathfinder threshold and the TRL 5 figure for technologies under test are engineering judgment with low direct evidence. **GPT's challenge to the reasoning:** treating TRL 6 at PDR as circular does not follow when the flight is meant to establish TRL 7. On that reading the TRL 5 exception is not justified by circularity alone. **Governance:** the project declares its own classification at SRR, and the response names no independent reviewer. | **T1** (loss avoidance vs learning tempo), with the explicit tipping condition w₁ > 2w₂ + w₃ + w₅. **T2** (scout waivability vs unambiguity). The 25 % threshold and the minimum-data-return floors are owner values. |
| **Gemini 3.1 Pro** | REJECT (Claude), NEUTRAL (Gemini, self), REJECT (GPT) | Information (all three voters) | **Null option:** no true null; Option A is a panel position relabelled (Claude, Gemini self). **Matrix:** qualitative and unweighted (Claude). **Evidence:** "almost certain" certainty is uncalibrated and conflates launch irreversibility with PDR policy (Claude, GPT). **Assumptions:** Assumption 2 has no falsifier (Claude), and falsification conditions are weak (Gemini self). **Sensitivity:** confuses the MTR with the PDR (Claude). **Circularity:** TRL 6 is applied to technologies whose flight is meant to raise their TRL, and the experimental-technology distinction is omitted (Claude, GPT). The response names no evidence that would change its ruling. | Administrative simplicity vs the physical reality of irreversible commitment. The response presents this as a trade-off but does not hand it to the owner as a values question. |
| **GPT-6.1 Sol** | APPROVE (Claude), APPROVE (Gemini), APPROVE (GPT, self) | Reasoning (Claude), alternatives (Gemini), commitment (self) | **Tipping point:** none quantified (Claude). **Experimental pathway:** relies on a discretionary assurance case with no stated TRL floor; independent review mitigates this (Claude). **Options:** could be more distinct (Gemini). **Sources:** the response says the underlying repository files were not independently inspected. **Cost claim:** that the split reduces cost is rated low certainty. | Learning vs mission-success assurance; schedule vs ground maturation; programme concentration (one high-assurance pathfinder) vs diversification (several cheaper, riskier experiments). GPT notes that TRL cannot settle these and that a TRL number is not a probability of mission success. |

**Divergences that are facts to settle, not values** (as identified by Claude and GPT):
- whether launch slots are refundable or rebookable, and whether a scout can be reflown quickly;
- the cost of ground relevant-environment tests relative to scout cost;
- whether the MTR precedes all flight-project PDRs;
- whether binding flight-project standards already exist;
- how tightly the payload is coupled to the spacecraft;
- whether irreversible procurement happens before PDR;
- whether tranche contracts are in practice whole-mission commitments.

## Key Points

- **Classify by commitment, not phase label.** All three models said reversibility depends on what a gate commits. The MTR is two-way. A flight PDR and a launch are one-way for the flight project.
- **TRL 4–5 at the MTR stands as a tranche criterion.** GPT and Claude add that it does not constitute flight authorisation.
- **Flight-enabling technologies need TRL 6 by PDR.** All three models agreed on this. GPT adds "or before an earlier irreversible implementation commitment", and Gemini says "before bending metal".
- **Enabling vs under-test distinction (Claude, GPT).** Both said requiring an experimental technology to reach the maturity its flight is meant to produce is self-defeating. Gemini did not draw the distinction. GPT's vote nonetheless challenged Claude's specific circularity argument against TRL 6 at PDR.
- **"TRL 8 before launch" as GPT's panel position.**
  - Claude reframed it as "flight system qualified and accepted", rejecting it for technologies under test.
  - GPT's round-1 text keeps qualification and acceptance requirements and treats TRL 8 as the target for the completed flight-enabling system.
- **The amendment must be explicit.** Claude and GPT both argued an "interpretation" that adds this distinction is new rule text and should be recorded in `decisions.md`. Gemini used the phrase "amend D-02 interpretation".
- **Claude-only proposals:**
  - a pathfinder cost-share trigger (25 %);
  - Class D waivers for scout enabling technologies, permitted because the no-waiver clause binds only KDP-0B;
  - classification fixed at SRR;
  - AD² as a companion check;
  - closing D-05 (propellant) before pathfinder PDR if propulsion is enabling;
  - pressure towards an earlier metallurgy down-select.
- **GPT-only proposals:**
  - non-compensable musts covering safety, licensing and launch-provider requirements;
  - independent review of the experimental boundary;
  - a technology–function–gate register;
  - "do not make TRL 5 circular" for tests that are themselves meant to establish TRL 5;
  - an explicit statement that a 0A flight does not by itself establish KDP-0B maturity.
- **Shared consequence (Claude, GPT).** Metallurgy routes are judged separately, not averaged.
- **Evidence cited by the panel:**
  - NASA NPR 7123.1 and SP-2016-6105, ECSS-E-HB-11A, DoD Milestone B practice and GAO project assessments (Claude, Gemini);
  - Mankins on TRL and AD² (Claude);
  - NASA's distinction between technology maturity and verification and validation (GPT).
  - Claude rated the outcome evidence moderate for large projects and low for small scouts.

## Unresolved Questions

1. **How technologies under test should be gated.** The options are Claude's numeric floors (TRL 5 at PDR, failure-mode tests before CDR, TRL 6 for those failure modes at launch), GPT's assurance case with no TRL floor, or Gemini's blanket TRL 6.
2. **Whether TRL 6 at PDR is circular for a demonstration flight.** Claude says it over-gates. GPT's vote says the circularity argument does not follow when the flight targets TRL 7.
3. **Whether a pathfinder cost-share trigger should exist, and at what level.** Claude proposes 25 % as an owner value. No other model addressed it.
4. **Whether scouts may waive enabling-technology criteria.** Claude proposes waivers via Class D risk acceptance. GPT allows only the bounded-experiment pathway, and Gemini allows no exception.
5. **Who classifies a technology as enabling or under test, and when.** Claude: the project declares it at SRR. GPT: an independent reviewer with authority.
6. **How the minimum-data-return floor is defined** for each project. Claude and GPT both treat this as a values input.
7. **Whether existing binding flight-project standards make a narrower clarification sufficient.** GPT's Option C depends on this.
8. **Programme concentration vs diversification.** One high-assurance pathfinder, or several cheaper, riskier scouts (GPT)?

## Recommended Actions

1. **Owner:** decide whether to amend D-02 explicitly, as Claude and GPT recommend, and record the change in `decisions.md`. Adopt the shared core in the rule text: the MTR is two-way at TRL 4–5 and is not flight authorisation; TRL 6 applies at project PDR or earlier irreversible commitment for flight-enabling technologies; KDP-0B is unchanged.
2. **Owner:** choose between Claude's numeric floors and GPT's assurance-case pathway for technologies under test, or decide to apply Gemini's blanket TRL 6. Ask for the justification GPT requested for any TRL 5 exception.
3. **Owner:** settle the values inputs the panel identified:
   - the weight on loss avoidance vs learning tempo (Claude's T1 tipping condition);
   - whether any pathfinder cost-share trigger applies, and its level;
   - scout waivability;
   - each project's minimum-data-return floor.
4. **Programme office:** gather the facts that Claude and GPT named as able to change the ruling:
   - launch-contract refundability and scout reflight time;
   - ground-test cost as a share of scout cost, against Claude's 15 % falsifier;
   - the MTR vs PDR schedule;
   - whether irreversible procurement precedes PDR;
   - tranche contract terms;
   - any existing binding flight-assurance standards.
5. **Each scout and pathfinder project:** produce a technology classification keyed to `trl-baseline.yaml` IDs, with hazard and coupling analysis to support it. Decide who reviews the classification (Claude: declared at SRR; GPT: independent review).
6. **WP-A:** add a `flight_project_gates` block, or GPT's technology–function–gate register, to `gates-proposal.yaml`. Align the MTR criteria in §5 with whichever position the owner adopts.
7. **Check dependent decisions** that Claude flagged:
   - whether D-05 (propellant) must close before pathfinder PDR;
   - whether flying a metallurgy route on the pathfinder forces an earlier down-select.
8. **Optionally run a TRL re-assessment for assessor variance.** Claude would make AD² a hard gate if assessors disagree by more than one level on any enabling technology.

```yaml
questionId: "rq-0-74"
topics:
  - id: gate-classification-basis
    topic: Classify D-02 gates by what they commit rather than by phase label
    positions:
      - statement: Reversibility is judged by what a gate commits. MTR tranche releases are two-way (TRL 4-5). Flight PDR and launch are one-way for the flight project and need stricter criteria. MTR passage does not authorise flight.
        models: [Claude Opus 5.5, Gemini 3.1 Pro, GPT-6.1 Sol]
        evidence: D-02's own principle; NASA NPR 7123.1 / SP-2016-6105 TRL 6 by PDR practice; GPT's panel 'TRL 8 before launch' read as conceding launch is one-way
    resolution_status: resolved
    priority: critical
  - id: amendment-vs-interpretation
    topic: Whether D-02 needs an explicit amendment or only an interpretation
    positions:
      - statement: Amend D-02 explicitly. The panel's three readings show the text is ambiguous, and adding the enabling vs under-test distinction is new rule text.
        models: [Claude Opus 5.5, GPT-6.1 Sol]
        evidence: Panel split as evidence the text fails auditability; materiality of spending and launch authority
      - statement: Amend the D-02 interpretation, adding that sub-projects committing flight hardware need TRL 6 at their own PDR.
        models: [Gemini 3.1 Pro]
        evidence: Gate stratification resolves the paradox without changing the principle
    resolution_status: partially-resolved
    priority: high
  - id: under-test-technology-criteria
    topic: Maturity criteria for technologies whose flight is meant to mature them
    positions:
      - statement: TRL 5 at PDR with a documented relevant environment; ground tests of no-data failure modes before CDR; TRL 6 for those failure modes at launch readiness.
        models: [Claude Opus 5.5]
        evidence: TRL definitions place flight demonstration at TRL 7; over-gating would force full ground campaigns before design commitment
      - statement: No fixed TRL floor. Experimental technologies may fly below flight-enabling levels under an approved demonstration assurance case that bounds failure effects, establishes learning outcomes and verifies safe interfaces. The case is independently reviewed.
        models: [GPT-6.1 Sol]
        evidence: NASA SP-2016-6105 distinguishes technology maturity from verification and validation; a TRL number is not a probability of mission success; avoid circular TRL 5 requirements
      - statement: All flight-critical technologies of a project need TRL 6 in a relevant environment at its PDR, with no role distinction.
        models: [Gemini 3.1 Pro]
        evidence: NPR 7123.1C TRL 6 by PDR for flight articles
    resolution_status: open
    priority: critical
  - id: pdr-trl6-circularity
    topic: Whether TRL 6 at PDR is circular for a demonstration flight
    positions:
      - statement: Requiring full TRL 6 at PDR for technologies under test over-gates them before their flight produces TRL 7, and conflicts with the must that a technology need not reach the TRL its own flight produces.
        models: [Claude Opus 5.5]
        evidence: TRL definitions (Mankins; ECSS); cost and schedule of ground relevant-environment campaigns
      - statement: Rejecting TRL 6 at PDR as circular does not follow when the flight is intended to establish TRL 7, so the TRL 5 exception needs better justification.
        models: [GPT-6.1 Sol]
        evidence: Vote critique of Claude's response
    resolution_status: open
    priority: high
  - id: pathfinder-cost-share-trigger
    topic: Pathfinder PDR treated as a programme-level one-way gate above a cost threshold
    positions:
      - statement: If pathfinder cost exceeds an owner-set share of the 0A budget (proposed 25 %), its PDR follows the KDP-0B rule with no waivers for enabling technologies.
        models: [Claude Opus 5.5]
        evidence: Loss of a large-share pathfinder changes the programme, not just the project; the threshold is engineering judgment with low direct evidence
    resolution_status: open
    priority: medium
  - id: scout-waivers
    topic: Waivers of enabling-technology criteria for scouts
    positions:
      - statement: Scouts may waive the TRL 6 enabling-technology requirement by owner-signed Class D risk acceptance. This is permitted because the no-waiver clause binds only KDP-0B.
        models: [Claude Opus 5.5]
        evidence: D-01 real-option logic favours cheap shots on goal; NPR 8705.4 risk-class vocabulary
      - statement: No waiver of flight-enabling criteria. Only the bounded-experiment pathway, under an assurance case, allows flight below maturity levels.
        models: [GPT-6.1 Sol]
        evidence: Non-compensable assurance requirements; risk of relabelling essential functions
    resolution_status: open
    priority: medium
  - id: classification-governance
    topic: Who classifies technologies as enabling or under test, and when
    positions:
      - statement: Each project declares the classification in its Technology Development Plan, fixed at SRR. A technology is enabling if its failure leaves less than a stated minimum data return.
        models: [Claude Opus 5.5]
        evidence: Mitigates sensitivity point S1
      - statement: An independent reviewer with authority must police the experimental boundary. The provision is not permitted if classification rests solely with the delivery team.
        models: [GPT-6.1 Sol]
        evidence: Assumption 4 falsifier; relabelling risk
    resolution_status: open
    priority: high
  - id: launch-readiness-criterion
    topic: What replaces 'TRL 8 before launch'
    positions:
      - statement: The flight system is qualified and accepted, with enabling elements effectively at TRL 8. TRL 8 is rejected for technologies under test.
        models: [Claude Opus 5.5]
        evidence: Must M2; TRL definitions
      - statement: Flight hardware completes qualification, acceptance, integration and operational readiness, with TRL 8 as the target for the completed flight-enabling system.
        models: [GPT-6.1 Sol]
        evidence: NASA SP-2016-6105 distinction between maturity and verification
    resolution_status: partially-resolved
    priority: medium
```