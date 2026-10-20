---
questionId: "rq-0-69"
questionSlug: "phase-0-sunset-rule"
modelId: "claude-opus-5-5"
modelName: "Claude Opus 5.5"
roundNumber: 1
generated: "2026-10-17"
type: "discussion-response"
---

# Month-180 Sunset: Automatic Fallback or Planning Boundary?

## 1. Frame & decision type

**Decision type.** This is a property decision on the gate set: what the sunset *is*. It is not an executive decision on the schedule. It sits inside D-02, so the reversibility logic applies to it directly.

**Reversibility, which settles most of the question.** The two branches at month 180 are not symmetric.

- **Executing the fallback** ("0A only, Earth supply") stops 0B option spend. It also switches the Phase 1 supply baseline to Earth. Both can be undone: 0B can re-enter later through a new gate. The cost of undoing it is restart cost and lost time, not a commitment that cannot be withdrawn.
- **Continuing past 180 without passing KDP-0B** is the drift path. Each extension looks reversible, but extensions add up to sunk-cost escalation. Under D-02, the burden of proof belongs on the path that tends toward irreversibility, which is continuation.

**What the dispute actually is.** Claude and GPT are mostly arguing about different things.

- Claude's concern is the **default**. What happens if nobody decides?
- GPT's concern is **authority**. A fixed M180 must not be read as authorising fifteen years of spend.

These concerns are compatible. A sunset can remove authority (Claude) without granting any (GPT). The real disagreements are narrower:
- whether the fallback executes without a fresh decision;
- whether the owner can extend in place, or only re-enter through a new decision;
- who sets the number: the panel now, or rq-0-63.

**Cynefin domain.** This is a complicated-to-complex problem. The month-180 state of the world is unknowable now, so the rule must work across all of its possible states. That argues for a rule that fixes the default and the burden of proof, not one that tries to predict the outcome.

**Null option.** Leave the split as drafted ("disputed"). Assessed below; it fails a must-criterion.

## 2. Criteria and weights (stated before options)

**Must-criteria (Kepner-Tregoe screen), pass or fail:**

- **M1.** It bounds every slip permitted in the §6 failure outcomes: the KDP-0A re-plan, the MTR re-plan, the g-target scout wave, the g-demand deferral and the KDP-0B slip.
- **M2.** It authorises no spend by itself. GPT's point, which I accept.
- **M3.** It cannot be used to waive D-02's "TRL 6 in a relevant environment, no waiver" at KDP-0B.

**Want-criteria, with swing weights.** Each weight reflects how far apart the options actually spread on that criterion.

| # | Criterion | Weight | Why this weight fits the range |
|---|---|---|---|
| C1 | **Drift containment.** Caps cumulative 0B option spend and elapsed time. | 0.30 | Widest swing across options: from no ceiling at all (null, rolling) to a hard ceiling. Escalation of commitment is the dominant failure mode of long gated programmes. |
| C2 | **Schedule coherence.** Consistent with rq-0-63, the 72–180 KDP-0B envelope and the §6 slips. | 0.20 | Options range from arithmetically impossible (KDP-0B planned at 180 *and* a slip allowed) to fully nested. Errors here are latent contradictions found late. |
| C3 | **Option value preserved.** Does not kill a nearly ready 0B on a technicality. | 0.20 | The swing is real but narrow. It matters only in the case where 0B is close at month 180. Under the other causes of failure (economics, demand), option value is near zero. |
| C4 | **Decision rights / legitimacy.** The owner keeps real authority. | 0.15 | All workable options leave the owner able to decide something new. The swing is between "the machine decides with no recourse" and "the owner must decide affirmatively". That is a moderate range. |
| C5 | **Auditability / simplicity.** | 0.15 | The range runs from one testable date to a contingent negotiation. This matters because the rule must be enforceable by people who were not on this panel. |

## 3. Options

**A. Null: leave the split.** Both texts stand, and rq-0-63 resolves them implicitly.
- *Rejected.* It fails M1. Claude's g-demand deferral re-tests "at Phase 1 milestones", and GPT allows a "bounded extension" with no bound stated. With no agreed sunset, neither is bounded.
- In practice, ambiguity resolves toward continuation, because continuation is what the funded team proposes. The split would quietly hand GPT's position the win without the owner having chosen it.

**B. Hard automatic sunset (Claude as drafted).** At M180 the fallback executes, with no override.
- It passes all the musts.
- *Rejected as drafted, for three reasons.*
  - No rule can bind a future owner. Pretending it can invites the rule to be ignored rather than used.
  - "Execution of fallback" is not defined. It is unclear what stops, what continues and what Earth supply commits to.
  - The number 180 is asserted by the panel instead of being derived from the integrated schedule.

**C. Planning boundary (GPT).** M180 is set via rq-0-63. At the boundary a mandatory decision is taken, with no pre-set default.
- It passes M2 and M3. It fails M1 in substance: a decision point with no default bounds nothing, because "extend" is always available at the meeting.
- *Rejected.* It puts the burden of proof on stopping, which inverts D-02.

**D. Default-executing ceiling with re-entry by new decision (recommended).** The sunset is S = M180 from the 0A funding start. It is a ceiling, not an entitlement.
- rq-0-63 sets the planned KDP-0B date P at or before S − 24 months, and all §6 slips must complete before S.
- At S, the defined fallback executes by default, with no further decision.
- The owner keeps full authority to *re-enter* 0B later. This is done only by a new decision record that meets the full KDP-0B criteria and is priced as a new commitment. It cannot be done by extending in place.
- An option-keeping spend cap is a second trigger.

**E. Rolling sunset.** S = P + a fixed slip allowance, with no absolute ceiling.
- *Rejected.* Each slip is bounded but the total is not, because re-planning P moves S. This is GPT's position with extra steps. It fails M1 cumulatively.

**F. Spend-only trigger.** Sunset when cumulative 0B option spend reaches a cap.
- *Rejected as a standalone rule.* Time is the binding cost here: Phase 1 schedule, team retention and launch-price drift all run on time.
- It is kept inside D as a second trigger, so that low-burn drift and high-burn drift are both caught.

## 4. Assessment matrix (QOC)

Scores are 1–5 (5 = best).

| Option | M1 | M2 | M3 | C1 Drift (0.30) | C2 Coherence (0.20) | C3 Option value (0.20) | C4 Rights (0.15) | C5 Audit (0.15) | Weighted |
|---|---|---|---|---|---|---|---|---|---|
| A Null | ✗ | ✓ | ? | 1 | 1 | 3 | 2 | 1 | 1.55 |
| B Hard auto | ✓ | ✓ | ✓ | 5 | 4 | 2 | 2 | 5 | 3.75 |
| C Planning boundary | ✗ | ✓ | ✓ | 2 | 3 | 4 | 5 | 3 | 3.20 |
| **D Default + re-entry** | ✓ | ✓ | ✓ | 4 | 5 | 4 | 4 | 4 | **4.20** |
| E Rolling | ✗ | ✓ | ✓ | 2 | 2 | 4 | 3 | 3 | 2.70 |
| F Spend-only | ✓ | ✓ | ✓ | 4 | 2 | 3 | 3 | 3 | 3.15 |

**Why D beats B on C3 and C4.** In D, the owner can bring 0B back at full rigour the day after S. B scores 2 on rights because it pretends otherwise. D scores 4, not 5, on drift because re-entry is a door that can be abused. The rule's job is to make that door expensive: a new business case, full KDP-0B criteria and no inherited budget.

## 5. Sensitivity vs trade-off points

**Sensitivity points** are facts that, if they change, move the ranking.

- **SP1. The critical path to TRL 6 in a relevant environment.** If rq-0-63 shows the relevant-environment demonstration cannot credibly finish by about M156, then P ≤ S − 24 cannot be met. The fallback then becomes the *planned* outcome, not a contingency.
  - The correct response is to change S **now**, by owner decision with the schedule evidence. Discovering the problem at M175 is the wrong response.
  - This is the single most important input, and it is why GPT is right that rq-0-63 must inform the number.
- **SP2. Restart cost of 0B after fallback.** If re-entry after fallback costs little more than continuing (team, data and supplier base survive cheaply), D's advantage over B narrows and B's simplicity wins. If restart is very expensive, pressure for in-place extension rises, and D's discipline matters more.
- **SP3. How often the owner overrides.** If re-entry is used routinely, D collapses toward C. This is observable: it can be tracked against the cost-and-schedule-growth record of major projects.
- **SP4. Launch-window-locked demonstrations.** If a relevant-environment test is tied to a launch window, a slip of a few months can push its result past S. This is where the argument for a carve-out is strongest. I reject a carve-out (see §8), but this is the point where the ruling is most fragile.

**Trade-off points** are values questions, to be decided by the owner and not settled by evidence.

- **TP1. Drift containment vs owner discretion.** Any increase in automaticity reduces the authority of the decision-maker at the moment of decision. I weight containment higher because the moment of decision is when sunk-cost pressure peaks. That is a value judgement, and the owner may weight it differently.
- **TP2. Slip allowance size (my 24 months).**
  - A larger allowance gives schedule realism and protects option value.
  - A smaller allowance reduces spend and moves Phase 1 certainty earlier.
  - This decision also narrows GPT's KDP-0B planning envelope from 96–180 to 96–156 *planned*. GPT should be asked directly whether it accepts that. The disagreement should be recorded, not averaged.
- **TP3. Size of the option-keeping cap.** A larger cap buys cheaper restart at the cost of a larger drift budget.

## 6. Evidence certainty

| Claim | GRADE certainty | Likelihood / confidence |
|---|---|---|
| Decision-makers escalate commitment to failing courses of action after sunk investment (Staw 1976; Arkes & Blumer 1985). | **Moderate.** Robust in experiments; indirect for programme boards. | Very likely that the effect operates at an M180 review; high confidence. |
| Defaults strongly shape outcomes when a choice is required (status-quo bias, Samuelson & Zeckhauser 1988). | **Moderate.** Strong general evidence; indirect here. | Likely that a no-default decision point resolves to "extend"; medium confidence. |
| Large space development projects routinely show schedule growth beyond baselines (GAO, *NASA: Assessments of Major Projects*, annual series). | **Moderate** for NASA; indirect for a Project Dyson ISRU programme. | Likely (~60–80 %) that at least one §6 slip is invoked; medium confidence. |
| Legislative sunset clauses reliably terminate programmes. | **Low.** The literature is mixed; many are routinely renewed. | About as likely as not that a sunset with easy renewal terminates anything; low confidence. *This is why D makes re-entry costly rather than relying on the date alone.* |
| The 24-month slip allowance is adequate. | **Very low.** A panel judgement; rq-0-63 does not exist yet as evidence. | No likelihood assigned; to be replaced by rq-0-63 output. |
| Fallback is cheaply reversible. | **Low.** Restart cost for an ISRU team and data set is not estimated anywhere in `trl-baseline.yaml` as far as I know. | Plausible; low confidence. This is SP2 and should be estimated. |

## 7. Key assumptions (with falsifiers) and competing hypotheses

**Key assumptions.**

| Assumption | Falsified by |
|---|---|
| K1. Phase 0 month 0 is the 0A funding start under D-01. | rq-0-63 defining t₀ differently, for example from Phase 1 award. S must then be re-expressed, not silently shifted. |
| K2. Executing the fallback commits nothing irreversible. Earth supply for Phase 1 remains subject to Phase 1's own gates. | A Phase 1 contract structure in which an Earth-supply baseline locks in long-term launch contracts that cannot be exited. If so, the fallback is itself a one-way door and needs its own D-02 treatment. |
| K3. Option-keeping activities can be separated from development spend. | Audit showing "option-keeping" contracts funding hardware or long-lead items. This is the usual way caps are evaded. |
| K4. The relevant-environment test fits before M156. | rq-0-63 critical path (SP1). |

**Competing hypotheses (ACH)** for the state "KDP-0B not passed at S":

- **H1.** The technology is near-ready and narrowly late.
- **H2.** The economics fail structurally.
- **H3.** Demand is absent.
- **H4.** The target resource is inadequate.

| Hypothesis | Fallback correct? | What disconfirms it at month 180 |
|---|---|---|
| H1 | No | Evidence that is *not* consistent with H1: the TRL 5 relevant-environment test not yet flown, or its outcome adverse. |
| H2 | Yes | g-economics passed. |
| H3 | Yes | Signed demand in hand. |
| H4 | Yes | g-target passed. |

**Implication for the rule.** Only H1 justifies anything other than the fallback. H1 also predicts that the other gates have already passed. So re-entry should require g-target, g-demand and g-economics all passed, plus a scheduled relevant-environment test. That screens out H2–H4, which are the common cases, and lets the owner act only on the hypothesis that survives disconfirmation.

## 8. Decision, warrant, accepted downside

### Ruling: adopt Option D

The proposed rule text for `gates-proposal.yaml`, tagged `sunset`, is below.

> **SUN-1 Ceiling.** The 0B sunset S is month 180 from the 0A funding start (t₀ per rq-0-63). S is a ceiling on 0B option authority. It authorises no tranche or spend. 0A funding continues only through KDP-0A and MTR.
>
> **SUN-2 Planning date.** rq-0-63 shall set the planned KDP-0B date P with P ≤ S − 24 months. If no credible schedule meets this, rq-0-63 reports it to the owner, who either changes S by decision record before KDP-0A or accepts fallback as the planned outcome. S is not adjusted after KDP-0A except by a new owner decision citing schedule evidence, and never within 36 months of S.
>
> **SUN-3 Slip containment.** Every slip permitted by the failure outcomes must complete before S. A slip that cannot complete before S is unavailable, and the fallback applies. In particular:
> - a g-target scout wave (≤ 36 months) is available only if it starts by S − 36;
> - the single KDP-0B slip ends at S.
>
> **SUN-4 Default execution.** If KDP-0B has not been passed by S, the fallback executes at S without further decision:
> - (a) all 0B spend stops, except closure and archiving;
> - (b) the Phase 1 supply baseline becomes Earth supply, subject to Phase 1's own gates;
> - (c) 0A completes its funded plan.
>
> **SUN-5 Second trigger.** The fallback also executes when cumulative option-keeping spend (SUN-6) reaches the cap the owner sets at KDP-0A, if that comes first.
>
> **SUN-6 Option-keeping spend.**
> - *Permitted* after a deferral and before S: data curation; licence and claim maintenance; a standing core team (suggested ≤ 5 FTE); remote-survey data purchase; demand and price re-tests; ground-lab work at TRL ≤ 5 already under contract.
> - *Not permitted*: flight hardware, long-lead procurement, pathfinder work, or new contracts extending past S.
> - *Cap*: owner-set at KDP-0A as a fraction of the 0A annual run rate. A low single-digit percentage is suggested and must be justified by the SP2 restart-cost estimate.
> - *After S*: only archiving and the pre-set g-economics re-test triggers, at a lower cap.
>
> **SUN-7 Re-entry.** After S, 0B may be reopened only by a new owner decision record that:
> - (a) shows g-target, g-demand and g-economics passed;
> - (b) meets KDP-0B criteria in full, with no waiver per D-02, or schedules the relevant-environment test with a funded plan;
> - (c) is priced and approved as a new commitment, not as a continuation of 0A or 0B budgets.
>
> In-place extension of S is not available.
>
> **SUN-8 No early lock.** Nothing in SUN-1 to SUN-7 delays an earlier fallback that the failure outcomes require.

### Y-statement

*In the context of* a gated Phase 0 where 0B is a real option and D-02 ties rigour to reversibility,
*facing* a split between an automatic sunset (Claude) and a planning boundary (GPT), and §6 slips that are unbounded without a common ceiling,
*we chose* a month-180 ceiling that grants no authority, executes the fallback by default, places planned KDP-0B at least 24 months before it (via rq-0-63) and allows 0B back only through a new, fully gated decision,
*to achieve* bounded slips, a capped drift budget, and owner authority exercised where escalation pressure is weakest,
*accepting* that a genuinely near-ready 0B may be stopped and must pay restart cost, and that GPT's 96–180 KDP-0B planning envelope narrows to 96–156.

### Toulmin structure

- **Grounds:** §6 permits at least five slips with no shared bound. The null option leaves them open-ended.
- **Warrant:** under D-02, the burden of proof belongs on the path that tends toward irreversibility. Defaults decide outcomes when commitment pressure is high. So the default must be the reversible branch (fallback), and the escape route must be priced as new.
- **Backing:** the escalation-of-commitment and status-quo-bias literature; the major-project schedule-growth record (§6).
- **Qualifier:** probably right, medium confidence. It depends on SP1 and on the unestimated restart cost.
- **Rebuttal conditions:** see the next subsection.

### Evidence that would change the ruling

The ruling should be reopened if any of the following is shown.

1. **rq-0-63 shows the relevant-environment test cannot complete before ~M156.** Then move S now, or accept fallback as plan.
2. **Restart cost after fallback is a large multiple of option-keeping cost.** That would justify a single in-place extension under SUN-7(a)–(b) criteria, moving toward a C/D hybrid.
3. **Demonstrations are tied to launch windows** in a way that makes a fixed S arbitrary. That would justify anchoring S to "earlier of M180 or first result date of the last scheduled relevant-environment test, if launched before M180". I would accept this only with a hard outer bound.
4. **Phase 1 contract analysis shows Earth supply is itself a one-way door (K2).** Then the fallback needs its own gate, and automatic execution is wrong.

### Note for later rounds

The weakest Decision Quality link in each original position:

- **Claude: alternatives.** It offered no route back after fallback, so it over-claims commitment.
- **GPT: values.** It did not say who carries the burden of proof at M180. Its silence lets the burden fall on stopping.
- **Gemini:** silent. Its "Fallback" entries throughout §6 suggest it would accept the default, but that should not be assumed.

## 9. Consequences

**Enables:**
- rq-0-63 gets a hard constraint: P ≤ S − 24. The integrated schedule becomes falsifiable.
- The §6 failure outcomes become mutually consistent:
  - the g-target scout wave must start by about M144;
  - the KDP-0B slip ends at S;
  - Claude's g-demand "re-test at Phase 1 milestones" runs only until S, and afterwards only as a SUN-7 re-entry trigger.
- Phase 1 planning can carry Earth supply as the baseline, with ISRU as an upside option rather than a dependency.

**Constrains:**
- GPT's KDP-0B upper bound of 180 becomes a sunset rather than a planning date. This is a recorded disagreement for GPT to accept or contest.
- The owner must set the option-keeping cap and confirm t₀ at KDP-0A. Both are new owner-decision items.
- A restart-cost estimate (SP2) becomes a required input to KDP-0A.

**Conflicts with:**
- Any reading of D-01 in which 0B is "held" indefinitely. D-01 says 0B is held as a *gated* option, and SUN-1 to SUN-7 define what gated means in time.

**Follow-on decisions unlocked:**
- the slip allowance (TP2);
- the cap (TP3);
- whether the fallback's Earth-supply baseline needs its own reversibility review (K2).