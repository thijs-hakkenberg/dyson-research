---
questionId: "rq-0-69"
questionSlug: "phase-0-sunset-rule"
type: "discussion-conclusion"
generatedBy: "claude-opus-5-5"
generated: "2026-10-17"
framework: "18f503fe4ec6"
roundCount: 1
terminationReason: "unanimous-conclude"
role: "alternate synthesis"
---

## Summary

The panel ran one round. All three models moved away from the framing in the background table (Claude "automatic" against GPT "planning boundary"). Each recommended that **M180 carries a default that takes effect without a further decision**, so that inaction cannot extend 0B.

- **Claude Opus 5.5** proposed Option D: a default-executing ceiling with re-entry only by a new decision.
  - M180 is a ceiling that grants no authority.
  - rq-0-63 must place planned KDP-0B at least 24 months before it.
  - Every §6 slip must complete inside it.
  - The fallback executes by default, and an option-keeping spend cap acts as a second trigger.
  - 0B can return after S only through a new, fully gated, newly priced decision. In-place extension is barred.
- **GPT-6.1 Sol** moved from its original "planning boundary" position to Option C: automatic expiry of existing 0B development authority at M180.
  - A pre-expiry review package is due by M168.
  - The default is "0A only, Earth supply" as a *planning baseline* that authorises no long-term procurement.
  - A new owner decision may grant bounded replacement authority. It cannot waive KDP-0B.
- **Gemini 3.1 Pro** chose hard automatic execution (Option 1).
  - It framed the fallback as an irreversible fifteen-year Earth-supply commitment.
  - It added a qualifier allowing an owner-level "D-03" clock pause for catastrophic exogenous shocks.

The panel therefore converged on the **core**: an automatic default at M180, no silent extension, and no gate waivers. It did not converge on four things:

1. Whether bounded continuation can be authorised before expiry (GPT) or only by re-entry after S (Claude).
2. Whether a 24-month planning buffer is imposed now (Claude) or left to rq-0-63 (GPT).
3. What "fallback" commits to. Claude and GPT say it is a reversible baseline with no procurement. Gemini says it is an irreversible paradigm.
4. Whether exogenous shocks justify pausing the clock. Gemini proposed a D-03 pause. Claude rejected a carve-out but flagged it as the point where his ruling is most fragile. GPT routes any change through an explicit owner decision.

Votes:

| Response | Votes received | Overall |
|---|---|---|
| Claude | APPROVE, APPROVE, NEUTRAL | Favourable |
| GPT | APPROVE ×3 | Unanimous approval |
| Gemini | REJECT, NEUTRAL, REJECT | Unfavourable |

Claude and GPT both rejected Gemini's response for uncalibrated certainty and for contradicting D-02's reversibility logic.

## Decision record

The panel **partially converged**. The shared core is recorded first, then one Y-statement per position on the points still in dispute.

**Shared core (Claude Opus 5.5, GPT-6.1 Sol, Gemini 3.1 Pro)**
*In the context of* D-01's gated 0B real option and D-02's non-waivable TRL 6 relevant-environment requirement at KDP-0B,
*facing* §6 failure outcomes that permit several slips with no common bound,
*we chose* to make M180 a sunset at which the fallback takes effect **by default if KDP-0B has not been passed**, with no extension through inaction,
*to achieve* bounded cumulative 0B exposure and a burden of proof placed on continuation,
*accepting* that a viable but late 0B may be stopped.

- **Null option.** All three assessed and rejected leaving the split unresolved.
  - Claude: it fails the must-criterion "bounds every slip", and ambiguity resolves toward continuation.
  - GPT: silence is not a neutral implementation rule.
  - Gemini: it guarantees a governance crisis at the first slip.

**Position 1: default-executing ceiling, re-entry only after S (Claude Opus 5.5)**
*In the context of* a gated Phase 0 where 0B is a real option and D-02 ties rigour to reversibility,
*facing* the split and the unbounded §6 slips,
*we chose* an M180 ceiling that grants no authority and executes the fallback by default (SUN-1 to SUN-8). Under it:
- planned KDP-0B P is at or before S − 24, set via rq-0-63;
- all slips must complete before S;
- an owner-set option-keeping cap is a second trigger;
- re-entry happens only after S, by a new decision record that shows g-target, g-demand and g-economics passed and that is priced as a new commitment;
- in-place extension is unavailable;

*to achieve* bounded slips, a capped drift budget, and owner authority exercised where escalation pressure is weakest,
*accepting* that a near-ready 0B may be stopped and pay restart cost, and that GPT's 96–180 KDP-0B planning envelope narrows to 96–156.

- **Warrant:** under D-02, the burden of proof belongs on the path that tends toward irreversibility, which is continuation. Defaults decide outcomes under commitment pressure.
- **Qualifier:** "probably right, medium confidence". This depends on the rq-0-63 critical path (SP1) and on the restart cost, which has not been estimated (SP2).

**Position 2: automatic expiry of authority with explicit replacement authority (GPT-6.1 Sol)**
*In the context of* D-01's demand-sized 0B option and D-02's non-waivable readiness gate,
*facing* an unresolved M180 sunset,
*we chose* automatic expiry of the existing 0B development authority at M180, measured from a recorded epoch that re-baselining cannot reset. The rule includes:
- a disposition package to the owner by M168;
- "0A only, Earth supply" as the planning baseline, with no long-term procurement authorised;
- a mechanism for a new owner decision to authorise a bounded corrective or preservation programme, specifying scope, an absolute cap, an expiry, deliverables and stop conditions, without waiving KDP-0B;

*to achieve* credible spending control without silently committing to long-term supply,
*accepting* possible capability interruption and the administrative cost of justified exceptions.

- **Warrant:** a real option needs both a controlled exercise decision and a controlled cost of waiting.
- **Qualifier:** conditional on enforceable financial controls, and on rq-0-63 either validating the date or explicitly prompting its revision.

**Position 3: hard automatic execution (Gemini 3.1 Pro)**
*In the context of* the Phase 0 TRL re-baseline,
*facing* the M180 split,
*we chose* automatic execution of the fallback at M180,
*to achieve* definitive sunk-cost prevention and a bounded KDP-0B option,
*accepting* that a viable but delayed project might be forced into Earth supply by an exogenous shock near the deadline.

- **Warrant:** megaprojects resist cancellation once capital is deployed. Only pre-committed guillotines terminate failing paths.
- **Qualifier:** a catastrophic exogenous shock, such as a global launch stand-down, would need an extraordinary owner-level D-03 decision to pause the clock.

## Decision-quality audit

| Response (Round 1) | Votes | Weakest link named by voters | Scaffold steps missing or unsupported |
|---|---|---|---|
| **Claude Opus 5.5** | Self: APPROVE (information). Gemini: APPROVE (information). GPT: NEUTRAL (commitment). | **Information.** The 24-month slip allowance and the restart cost are flagged by Claude itself as very-low and low certainty. **Commitment** (GPT): SUN-7(b) allows re-entry if the relevant-environment test is merely *scheduled*, which conflicts with "meets KDP-0B criteria in full". GPT also called the 24-month buffer unsupported, noting that it materially narrows the planning envelope. | All nine steps present. Supporting evidence for the 24-month buffer and for the restart cost is absent. Rapporteur arithmetic check: Option F totals 3.10 rather than the stated 3.15. The ranking is unchanged. |
| **Gemini 3.1 Pro** | Claude: REJECT (information). Self: NEUTRAL (alternatives). GPT: REJECT (information). | **Information.** It asserts >90% likelihood and high confidence that 180 months suffices, based on loose Apollo/ISS analogues (Claude, GPT). **Alternatives.** Only three options, with no hybrid (self, Claude). | **Frame:** calls the fallback a highly irreversible one-way door, then makes it automatic, which conflicts with D-02 (Claude); conflates the fallback with a fifteen-year procurement commitment (GPT). **Criteria:** confuses capping 0A spend with capping 0B spend (Claude). **Matrix:** qualitative only, with no weighted aggregation (Claude). **Null option:** not scored in the matrix (self). **Consequences:** an M150 cutoff cannot accommodate a 36-month scout wave before M180 (GPT). |
| **GPT-6.1 Sol** | Claude: APPROVE (reasoning). Gemini: APPROVE (values). Self: APPROVE (information). | **Reasoning** (Claude): letting replacement authority be granted before expiry is "slightly looser" than an outright ban on in-place extension, though bounded and explicit. Claude also reported an arithmetic slip in Option B (72.5, not 70). **Values** (Gemini): the swing weights are proposed owner values, though caveated. **Information** (self): schedule feasibility and preservation economics are uncertain. | All steps present. Evidence on preservation and restart economics is very low certainty, as GPT acknowledges. Rapporteur arithmetic check: with GPT's stated weights and 0–4 scale, Option B computes to 70.0. Claude's claimed correction to 72.5 does not reproduce. |

**Divergences that are trade-off points (values questions, not facts to settle):**

| Trade-off | Raised by | Position or framing |
|---|---|---|
| Drift containment against owner discretion at the moment of decision | Claude TP1; GPT ("binding the programme against drift" against "future-owner discretion") | Underlies the dispute between in-place continuation before expiry (GPT) and re-entry only after S (Claude). |
| Size of the slip allowance (24 months or other) | Claude TP2 | Explicitly a values question. Claude asks that GPT's disagreement be recorded, not averaged. |
| Size of the option-keeping cap | Claude TP3 | Framed by Claude as restart cost against drift budget. |
| Credible fiscal commitment against preserving a valuable capability | GPT | Includes accepting a temporary capability interruption against funding continuity before demand exists. |
| Sunk-cost prevention against exogenous shock absorption | Gemini | Gemini resolves it toward sunk-cost prevention, with a D-03 escape. |

**Divergences that are facts to settle:**

| Fact | Raised by | Why it matters |
|---|---|---|
| Whether "fallback" commits to anything irreversible | Claude K2; GPT; contested by Gemini | Settled by Phase 1 contract analysis. Claude: if Earth supply is a one-way door, automatic execution is wrong. |
| The rq-0-63 critical path to TRL 6 in a relevant environment | Claude SP1; GPT | Determines whether the date is feasible. |
| Restart cost against preservation cost | Claude SP2; GPT | Bears on the size of the cap and on whether in-place extension could be justified. |
| Governance and contract-notice lead times | GPT | Whether the owner can decide before expiry. |

## Key Points

- **The original dispute narrowed in Round 1.** GPT accepted an automatic default; its remaining objection is that M180 must not *authorise* a long-term Earth-supply commitment. Claude made the same point separately: the sunset "authorises no spend by itself" (M2, SUN-1).
- **Claude reframed the split.** In Claude's account, Claude's concern was the *default* and GPT's was *authority*, and the two are compatible. GPT's three-way separation of planning boundary, authority boundary and supply commitment is the parallel framing.
- **Claude and GPT agree the fallback is a planning baseline, not a procurement commitment.**
  - Claude SUN-4: 0B spend stops; Phase 1 supply becomes Earth, subject to Phase 1's own gates; 0A completes.
  - GPT: "does not authorise a long-term Earth-supply purchase."
  - Gemini treats the fallback as irreversible, and both peer reviewers flagged this as conflicting with D-02.
- **All §6 slips are to sit inside the sunset** (Claude SUN-3; GPT §9 "no silent clock restart"; Gemini "subsumes" the KDP-0B slip rule).
  - Claude derives timing constraints: a scout wave must start by S − 36 (about M144), and the KDP-0B slip ends at S.
  - GPT noted that Gemini's M150 cutoff is inconsistent with a 36-month scout wave.
- **The epoch is fixed against re-baselining.**
  - GPT: re-baselining does not reset the epoch.
  - Claude: t₀ is the 0A funding start, set per rq-0-63. S may change only by owner decision before KDP-0A, never within 36 months of S, and an "in-place extension is not available".
- **The two models differ on option-keeping spend.**
  - Claude specifies a permitted list: data, licences, ≤ 5 FTE core team, remote-survey purchase, re-tests, TRL ≤ 5 ground work already under contract. Hardware and long-lead items are prohibited. The cap is a low single-digit percentage of the 0A run rate and acts as a second trigger.
  - GPT requires a separately identified, evidence-producing budget, "no evergreen option-keeping allowance", and no tooling or long-lead procurement disguised as preservation.
- **Claude used ACH to shape re-entry criteria.** Only "near-ready and narrowly late" (H1) justifies anything other than the fallback. H1 predicts that the other gates have passed, so re-entry requires g-target, g-demand and g-economics all passed.
- **Supporting evidence cited.**
  - Claude: escalation of commitment (Staw 1976; Arkes & Blumer 1985), status-quo bias (Samuelson & Zeckhauser 1988), GAO NASA schedule growth, and low-certainty evidence that legislative sunsets terminate programmes. The last is why Claude makes re-entry costly rather than relying on the date alone.
  - GPT declined to assign numerical probabilities from the supplied material.

## Unresolved Questions

1. **Continuation before expiry.** May a new owner decision before M180 authorise bounded corrective or preservation work in place (GPT)? Or must 0B lapse at S and re-enter only as a new, fully priced commitment (Claude)? This is a trade-off point.
2. **Planning buffer.** Should P ≤ S − 24 be imposed now (Claude)? GPT called this unsupported and retains 72–180 as the provisional envelope. Claude explicitly asked GPT whether it accepts the narrowing to 96–156; GPT did not accept it.
3. **Meaning of the fallback.** Is it a reversible baseline (Claude, GPT) or an irreversible fifteen-year paradigm (Gemini)? This depends on Phase 1 contract structure (Claude K2).
4. **Exogenous shocks and launch-window-locked tests.**
   - Gemini: a D-03 clock pause.
   - Claude: rejects a carve-out, but would accept "earlier of M180 or first result of the last scheduled relevant-environment test, if launched before M180" with a hard outer bound.
   - GPT: an explicit owner decision only.
5. **SUN-7(b) inconsistency (GPT).** Does re-entry require KDP-0B in full, or is a scheduled and funded relevant-environment test sufficient?
6. **Option-keeping cap.** What is its size and form? Claude proposes a percentage of the 0A run rate set at KDP-0A, acting as a second trigger. GPT proposes an absolute cap per replacement decision.
7. **Restart cost against preservation cost.** No estimate exists (Claude SP2; GPT rates this "very low certainty").
8. **Gemini's position after the peer criticisms.** It is unknown whether Gemini would accept a reversible-fallback definition, given that its §6 "Fallback" entries suggest it would accept the default (Claude).

## Recommended Actions

1. **Owner ruling on the shared core.** Adopt an automatic default at M180 with no extension through inaction and no KDP-0B waiver. All three models support this.
2. **Owner ruling on in-place continuation (Unresolved Question 1).** Choose between Claude SUN-7 (re-entry after S only) and GPT's replacement authority before expiry. Record it as a values decision.
3. **Define "fallback" in `gates-proposal.yaml`.** Claude SUN-4 and GPT's default disposition offer near-identical text: stop 0B discretionary spend, adopt an Earth-supply planning baseline, authorise no procurement, and complete 0A. Record Gemini's divergent reading.
4. **Task rq-0-63** (Claude, GPT) to:
   - fix the epoch t₀;
   - assess whether TRL 6 in a relevant environment can complete by about M156;
   - include gate-review, contract-notice and safe-stop durations (GPT);
   - report infeasibility to the owner before KDP-0A, not near S.
5. **Commission a restart-cost and preservation-cost estimate** as a KDP-0A input (Claude SP2; GPT).
6. **Commission a Phase 1 contract analysis** to test whether an Earth-supply baseline is itself a one-way door (Claude K2; the central point of Gemini's framing).
7. **Resolve the SUN-7(b) wording** that GPT flagged, and put the 24-month buffer to GPT as a recorded agreement or disagreement (Claude TP2).
8. **Add owner-decision items at KDP-0A:**
   - the option-keeping cap and permitted scope (Claude SUN-6; GPT preservation list);
   - confirmation of t₀;
   - a pre-expiry review date (GPT proposes M168).
9. **Track exception and re-entry use.** Per Claude SP3 and GPT, routine use of these routes would justify moving toward a harder sunset.

```yaml
questionId: "rq-0-69"
topics:
  - id: sunset-default-execution
    topic: Whether M180 executes the fallback by default without further decision
    positions:
      - statement: M180 is a ceiling granting no authority; if KDP-0B is not passed by S the fallback executes by default (stop 0B spend except closure, Earth-supply baseline subject to Phase 1 gates, 0A completes)
        models: [Claude Opus 5.5]
        evidence: D-02 reversibility logic puts burden of proof on continuation; escalation-of-commitment (Staw 1976; Arkes & Blumer 1985) and status-quo bias (Samuelson & Zeckhauser 1988) literature; null and planning-boundary options fail the must-criterion of bounding every §6 slip
      - statement: Existing 0B development authority expires automatically at M180; "0A only, Earth supply" becomes the planning baseline by default; inaction cannot extend funding
        models: [GPT-6.1 Sol]
        evidence: a real option requires a controlled cost of waiting; a decision point alone leaves unresolved what happens without a decision; weighted QOC (85.0 against 63.8 hard fallback and 70.0 decision point only)
      - statement: M180 is a hard sunset that automatically triggers the fallback
        models: [Gemini 3.1 Pro]
        evidence: megaprojects resist cancellation once capital is deployed; 180 months judged ample margin (asserted >90% likelihood from Apollo/ISS analogues, which peers called uncalibrated)
    resolution_status: resolved
    priority: critical
  - id: continuation-before-expiry
    topic: Whether bounded continuation can be authorised in place before S or only by re-entry after S
    positions:
      - statement: In-place extension of S is not available; 0B may be reopened only after S by a new owner decision record showing g-target, g-demand and g-economics passed, meeting KDP-0B criteria, priced as a new commitment
        models: [Claude Opus 5.5]
        evidence: re-entry is a door that can be abused and must be made expensive; ACH shows only the near-ready-but-late hypothesis justifies continuation, and it predicts the other gates have passed
      - statement: A new owner decision effective before expiry may authorise a bounded corrective or preservation programme with scope, absolute cap, expiry, deliverables and stop conditions; it cannot constitute or waive KDP-0B
        models: [GPT-6.1 Sol]
        evidence: preserves accountable choice when circumstances change; capability can be expensive to reconstruct; Claude's vote called this slightly looser but bounded and explicit
    resolution_status: open
    priority: critical
  - id: fallback-reversibility
    topic: What the fallback commits to and whether it is reversible
    positions:
      - statement: The fallback is reversible; it switches the Phase 1 supply baseline to Earth subject to Phase 1's own gates and commits nothing irreversible; if contract analysis shows otherwise, the fallback needs its own D-02 treatment and automatic execution is wrong
        models: [Claude Opus 5.5]
        evidence: restart cost, not irrevocable commitment, is the cost of undoing; assumption K2 with a stated falsifier
      - statement: Expiry adopts Earth supply as a planning baseline only and does not authorise a long-term Earth-supply purchase
        models: [GPT-6.1 Sol]
        evidence: D-01's demand-sized approach and the separation of supply strategy from purchasing authority (moderate certainty, high confidence in the distinction)
      - statement: The fallback is a highly irreversible one-way door committing the programme to a fifteen-year Earth-supply paradigm
        models: [Gemini 3.1 Pro]
        evidence: frame statement only; Claude and GPT both flagged it as conflicting with D-02 and conflating fallback with procurement
    resolution_status: partially-resolved
    priority: high
  - id: kdp-0b-planning-buffer
    topic: Whether rq-0-63 must place planned KDP-0B at least 24 months before S
    positions:
      - statement: rq-0-63 shall set planned KDP-0B P at or before S minus 24 months, narrowing the planning envelope to 96–156; if no credible schedule meets this, the owner changes S before KDP-0A or accepts fallback as plan
        models: [Claude Opus 5.5]
        evidence: makes the integrated schedule falsifiable and nests §6 slips; Claude rates the 24-month figure itself very low certainty, to be replaced by rq-0-63 output
      - statement: Retain M180 as the provisional outer limit and the 72–180 envelope pending rq-0-63; the 24-month buffer is unsupported
        models: [GPT-6.1 Sol]
        evidence: the envelope is not evidence of a validated schedule; rq-0-63 must assess feasibility and include review, notice and safe-stop durations
    resolution_status: open
    priority: high
  - id: exogenous-shock-carve-out
    topic: Treatment of exogenous shocks and launch-window-locked tests near S
    positions:
      - statement: A catastrophic exogenous shock warrants an extraordinary owner-level D-03 decision to pause the clock
        models: [Gemini 3.1 Pro]
        evidence: trade-off between sunk-cost prevention and shock absorption; risk of killing a viable architecture at month 179
      - statement: Reject a carve-out; the ruling is most fragile here; would accept anchoring S to the earlier of M180 or the first result of the last relevant-environment test launched before M180, only with a hard outer bound
        models: [Claude Opus 5.5]
        evidence: sensitivity point SP4 on launch-window-locked demonstrations
      - statement: Changes to the sunset date require an explicit owner decision citing schedule evidence; re-baselining cannot reset the epoch
        models: [GPT-6.1 Sol]
        evidence: rq-0-63 may recommend but cannot change spending authority by itself
    resolution_status: open
    priority: medium
  - id: option-keeping-spend
    topic: Scope and cap of spend to keep the 0B option alive after deferral
    positions:
      - statement: Permitted list (data curation, licences, ≤5 FTE core team, remote-survey purchase, re-tests, TRL≤5 ground work already contracted); no flight hardware, long-lead, pathfinder or contracts past S; owner-set cap at KDP-0A as a low single-digit percentage of the 0A run rate, acting as a second sunset trigger; lower cap after S
        models: [Claude Opus 5.5]
        evidence: time and spend drift both need catching; cap to be justified by a restart-cost estimate (low certainty)
      - statement: Separately identified, evidence-producing budget before sunset; no evergreen allowance; any preservation justified item by item (data, samples, software, storage, time-limited personnel) under an absolute cap in a new decision; no tooling or long-lead production disguised as preservation
        models: [GPT-6.1 Sol]
        evidence: weakest evidential link is the economic value of keeping the option alive (very low certainty)
    resolution_status: partially-resolved
    priority: high
  - id: re-entry-criteria-consistency
    topic: Whether re-entry requires full KDP-0B compliance or a scheduled relevant-environment test
    positions:
      - statement: SUN-7(b) permits re-entry if KDP-0B is met in full or the relevant-environment test is scheduled with a funded plan
        models: [Claude Opus 5.5]
        evidence: rule text as drafted
      - statement: This conflicts with the requirement for full KDP-0B compliance and weakens commitment
        models: [GPT-6.1 Sol]
        evidence: peer vote naming commitment as Claude's weakest link
    resolution_status: open
    priority: medium
```