---
questionId: "rq-0-65"
questionSlug: "gate-risk-class-split-technologies"
modelId: "claude-opus-5-5"
modelName: "Claude Opus 5.5"
roundNumber: 1
generated: "2026-10-17"
type: "discussion-response"
---

# Risk class for T02, T10, T14, T15, T22, T24, T25 and T26

**Recommendation in brief:** adopt a rule that generates the classes, rather than voting technology by technology. Under the rule, a function is project-ending unless an accepted fallback dossier shows a credible, costed fallback that keeps 0B production above the economics gate.

## 1. Frame and decision type

**Decision type.** This is a property decision about technology class, but it behaves like an executive decision.

- The class determines what KDP-0B demands.
- KDP-0B is the one-way door under D-02.
- The class assignment itself is two-way until KDP-0B: we can re-class at KDP-0A or at the 0A mid-term review.

That asymmetry should drive the answer. Erring toward project-ending now is cheap to reverse. Erring toward a lower class at KDP-0B is not.

**Cynefin domain.** The question is complicated, not complex, for most items. The facts that settle each class are knowable within 0A: fallback performance, cost and economics-model elasticity. T10 and T24 lean complex, because their long-duration behaviour can only be learned by operating.

**What the split actually is.** The panel headline used a "max" rule: if any model says project-ending, the item is project-ending. That is why T02 is headlined project-ending although two of three models said architecture-change.

The disagreement is also partly not technical. An ACH check on why the panel split (section 7) suggests most of it is definitional and about scope:

- What does "project-ending" end: the programme, 0B production, or the business case?
- Where are the boundaries: tug versus site arrays, one spacecraft versus a fleet?

Claude's own entries are inconsistent on T25: architecture-change in the class table, project-ending in the disputed list. Any ruling that does not fix definition and scope will reproduce the split.

## 2. Criteria and weights

**Must.** Any option must comply with D-02: no waiver for project-ending items at KDP-0B, and stringency follows reversibility. It must also not overturn the owner's rq-0-64 ruling on T26 outside rq-0-64.

**Wants,** with swing weights. Each weight reflects how much the options differ on that criterion, not its abstract importance.

| # | Criterion | Weight | Why this weight fits the range |
|---|---|---|---|
| C1 | Protection against 0B committing on an unproven function | 40 | Widest consequence range across options. At one end, 0B sinks capital into a fleet that cannot produce. At the other, a hold costs some months. |
| C2 | 0A length and cost (penalty for over-classing) | 25 | Taking one MW-class array or a cryogenic store to TRL 6 in a relevant environment is a multi-year, flight-class effort. So each wrongly held item costs real schedule. The range is roughly 0–3 items over-held. |
| C3 | Auditability and repeatability | 20 | A rule can be re-applied when evidence arrives, and new technologies such as T09, T12, T20, T18 and T11 can be classed without another panel. A vote cannot. The range is large: from "three LLMs disagreed" to a testable criterion. |
| C4 | Responsiveness to evidence | 15 | All options can be revisited at KDP-0A. They differ mainly in whether they say *what* evidence moves an item, so the range is moderate. |

## 3. Options

**A. Null: keep the panel headline (max rule).**
- Seven of the eight are project-ending; T26 stays architecture-change per the owner's ruling.
- *For:* safe, consistent with Claude's interim hold.
- *Against:* it is not a rule, just the union of three opinions.
  - It probably over-holds T24 and T25, and possibly T14.
  - It gives no exit criterion, so items stay at TRL 6 and no waiver by inertia.

**B. Majority vote per technology.**
- Result: T02, T14 and T25 architecture-change; T10, T15, T22 and T24 project-ending; T26 cost-increase.
- *Rejected.* T26 cost-increase conflicts with the owner's ruling (fails the must).
- Agreement among three models of correlated origin is not evidence.
- It under-classes T02, the item with the largest scale gap.

**C. Generating rule (fallback test), applied at function level, defaulting to project-ending.** This is the recommended option.
- A function is project-ending unless an accepted fallback dossier shows a credible, costed fallback that keeps 0B production above the economics gate.
- Technologies whose functions differ in consequence are split, for example T10.

**D. Everything below project-ending; the economics gate is the backstop.**
- *Rejected.* It treats the economics gate as if it could see technical immaturity. It cannot.
- A model fed a TRL 3 fallback's cost estimate gives a precise-looking wrong answer.
- It violates the spirit of D-02 for the one-way gate.

**E. Defer everything to KDP-0A and formalise the interim hold.**
- *Partly adopted inside C* as the default state.
- On its own it is rejected: deferring without a rule means KDP-0A faces the same split with no criterion.

## 4. Assessment matrix (QOC)

Scores run from 1 (poor) to 5 (good).

| Option | C1 (40) | C2 (25) | C3 (20) | C4 (15) | Weighted | Must |
|---|---|---|---|---|---|---|
| A Null / max rule | 5 | 2 | 2 | 2 | 3.30 | pass |
| B Majority | 2 | 4 | 1 | 2 | 2.30 | **fail** (T26) |
| C Fallback rule, function level, default PE | 4.5 | 4 | 5 | 5 | **4.55** | pass |
| D All lower class + economics backstop | 1 | 5 | 3 | 3 | 2.70 | **fail** (spirit of D-02) |
| E Defer only | 5 | 2 | 1 | 2 | 3.10 | pass |

**Why C scores 4.5 on C1, not 5.** The rule depends on dossier quality. An optimistic fallback costing could let an item drop class. Section 8 covers the mitigation.

## 5. Sensitivity points and trade-off points

**Sensitivity points** are facts that strongly drive a single class.

- **T02 and T15:** how sensitive the economics model is to available power (how throughput and cost per kilogram fall as power drops). If halving power roughly halves throughput and the economics gate still passes, a modular-array fallback is credible. If there is a threshold below which processing or tug transit time does not close, it is not.
- **T14:** the propellant choice.
  - If a storable or water-based propellant is an acceptable fallback, T14 is architecture-change.
  - If the architecture is cryogenic-only, it is project-ending.
- **T24:** the spares and replacement mass fraction versus mean time between failures. This is where redundancy stops paying.
- **T10:** the round-trip light time to the selected target, which is set by the target gate. Small light times make supervised operations a credible fallback. Tens of minutes do not.
- **T25:** whether the SEL1 node operates as a cooperative target (beacons, retro-reflectors). That makes the rendezvous problem close to existing practice.

**Trade-off points** are values questions, not facts to settle.

1. **Which way the burden of proof runs.** Defaulting to project-ending buys protection on C1 at the cost of C2 (0A length). This is the owner's appetite for 0A delay versus 0B regret. I recommend the project-ending default because the class is reversible until KDP-0B, but this is a value judgement.
2. **What "project-ending" ends.** Read as "0B production cannot meet the economics gate", the class is broader than "the programme physically cannot proceed". I recommend the broader reading: D-01 sizes 0B on signed demand, so a 0B that cannot meet that demand at viable cost has failed. A narrower reading would be defensible.
3. **Whether a degraded-throughput 0B counts as a fallback.** This is a values question about what counts as success, and it links to D-01's demand sizing.

## 6. Evidence certainty

GRADE certainty is listed separately from likelihood, per IPCC and ICD 203.

| Claim | Certainty (GRADE) | Likelihood / confidence |
|---|---|---|
| Flown space power systems are at most ~100 kW-class (ISS). MW-class deployable arrays are an order of magnitude or more beyond flight heritage. | High | Very likely, high confidence, that T02 at MW scale is ≤ TRL 4. |
| In-space storage and transfer of hundreds of tonnes of cryogenic propellant, over long durations, has not been demonstrated. | High | Very likely, high confidence. |
| Single-spacecraft target-local navigation at small bodies is flight-proven (Hayabusa2, OSIRIS-REx). Repeated cargo operations and SEL1 node operations are not. | High for heritage; low for the fleet extension | Likely (~70%), medium confidence, that a ground-in-the-loop fallback is credible for T25. |
| Dust degraded Apollo mechanisms and seals. Long-life behaviour of asteroid regolith in microgravity is poorly characterised. | Moderate (lunar); very low (asteroid) | About as likely as not that seal life meets requirements without redundancy. Likely, medium confidence, that redundancy plus replacement is a credible fallback. |
| Deep-space network capacity is contended. Point-to-point links are TRL 9; an integrated fleet command *service* is not. | Moderate | The T26 TRL 3–7 spread is mostly scope, high confidence. |
| Panel TRL estimates for these eight items | Very low (2-level spreads, no test data) | Do not use them to set classes. Use the fallback test. |
| Economics-model power and throughput sensitivity | Very low (not yet run with fallback branches) | Unknown. This is the single most valuable 0A analysis for this question. |

## 7. Key assumptions and competing hypotheses

**Why did the panel split?** Three hypotheses, ranked by least disconfirmed (ACH).

1. **H-scope: the models drew different technology boundaries.** Least disconfirmed.
   - T26's TRL 3 versus 7 is only explicable as "link" versus "service".
   - T02 carries a "tug; site per Gemini and GPT" annotation.
   - T10 spans mining, processing and proximity operations, which carry different consequences.
2. **H-definition: the models meant different things by "project-ending".** Second.
   - Claude's own T25 inconsistency fits this.
   - So does Gemini's project-ending for T24 at a higher TRL than the others gave.
3. **H-technical: genuine disagreement about fallback credibility.** Present but most disconfirmed as the main driver.
   - Where the models scoped the same thing (T15, T22), they mostly agreed.

The implication is that function-level splitting and a fixed definition will resolve most of the split. That is why option C beats any vote.

**Key assumptions and what would falsify them:**

| Assumption | Falsified by |
|---|---|
| A1. The economics gate can evaluate a fallback branch if the fallback's cost and performance are given at ≥ TRL 5. | A model audit at KDP-0A showing outputs dominated by unconstrained parameters, e.g. ±50% swings from fallback inputs alone. |
| A2. T02 and T15 failures are common-cause. Site power has no non-array fallback that keeps 0B production. | A costed nuclear-fission or beamed-power site option at TRL ≥ 5 that does not depend on T02. Space fission reactors are not at TRL 5 at this scale, so I do not expect this. |
| A3. A storable or water-based propulsion fallback exists for the tug fleet. | A propulsion trade showing the economics gate fails with storable propellants at any feasible fleet size. |
| A4. Redundancy and replacement can carry dust-induced wear within the mass budget. | Accelerated life tests in vacuum with representative regolith simulant showing failure rates that need spares above the mass-fraction threshold the economics gate tolerates. |
| A5. The selected target's light time allows supervised fallback for productivity autonomy, but not for safety-critical proximity aborts. | A target-gate selection with light times short enough for real-time abort, which would drop T10a. |

**Premortem.** "0B was committed and failed in year three." The most plausible story is that a fallback dossier assumed productivity numbers from a nominal concept of operations, and the economics gate passed on them.

The mitigation is that fallback performance inputs to the economics gate must carry the same TRL evidence as the fallback itself. They are reviewed independently of the team that owns the primary technology.

## 8. Decision, warrant, accepted downside

### Rule text (proposed for `gates-proposal.yaml`)

> **Class rule CR-1.** A technology *function* is **project-ending** for KDP-0B unless the owner has accepted a **fallback dossier** demonstrating all of the following:
>
> - (a) the fallback is at TRL ≥ 5 in a relevant environment;
> - (b) the fallback is costed at estimate class ≤ 4;
> - (c) the economics gate passes with the fallback substituted, using fallback performance evidenced at the same TRL;
> - (d) the fallback is not common-cause with failure of the primary or of another project-ending function;
> - (e) the schedule impact is within the 0B commitment tolerance.
>
> Functions with an accepted dossier are **architecture-change**: TRL ≥ 5 at KDP-0B, waiverable, with a funded path to TRL 6 before the dependent 0B milestone. Until a dossier is accepted, the function is project-ending (TRL 6 in a relevant environment, no waiver). Dossiers are reviewed independently of the technology owner. Classes are confirmed at KDP-0A and may be revised at the 0A mid-term review.

### Per-technology application

| Tech | Ruling now | Basis | Moves if… |
|---|---|---|---|
| **T02** (tug function; site arrays fold into T15) | **Project-ending** | Largest scale gap. The modular-array fallback is not yet shown to pass economics. | A dossier shows a cluster of ~100–300 kW-class arrays passes the economics gate at the resulting power level. Then architecture-change. |
| **T10** → split | **T10a** safety-critical autonomy (fault protection, proximity safe-abort under light time): **project-ending**. **T10b** productivity autonomy (mining and processing scheduling): **architecture-change**, provisional on dossier. | No ground fallback for aborts at minutes of light time. Supervised operations is a throughput fallback that the economics gate can price. | T10b reverts to project-ending if the supervised-operations dossier fails (c). T10a drops only under A5's falsifier. |
| **T14** | **Architecture-change, conditional** | Credible if the propellant trade carries a storable or water fallback. | It becomes project-ending if the KDP-0A propellant selection is cryogenic-only with no storable branch (A3 falsified). |
| **T15** | **Project-ending** | Common-cause with T02. No independent site-power fallback keeps 0B production. | An independent power path at TRL ≥ 5 (A2 falsified). |
| **T22** | **Project-ending** | No qualified product means no demand gate. Agreed in substance by two of three. | TRL 6 is assessed against the **signed buyer product specification** from the demand gate, not a generic standard. It would move only if buyers sign for raw or minimally processed product. |
| **T24** | **Architecture-change** (TRL ≥ 5 plus a life-test campaign) | Redundancy and replacement is a credible, priceable fallback. Wear is a cost and mass question the economics gate can see. | It becomes project-ending if life tests falsify A4. |
| **T25** | **Architecture-change** (TRL ≥ 5, funded path to 6) | Strong single-craft heritage. A cooperative SEL1 node plus ground-in-the-loop navigation is a credible fallback. This resolves Claude's internal inconsistency in GPT's direction. | It becomes project-ending if fleet traffic density makes ground-in-the-loop navigation infeasible. |
| **T26** | **No change: architecture-change per owner ruling.** The "possibly project-ending" question stays in rq-0-64. | Not re-ruled here; it is the must. | CR-1 is offered to rq-0-64 as the test: project-ending if no combination of DSN, ESA tracking and commercial ground service meets fleet command demand. |

**Net effect versus the null option.** T14, T24, T25 and T10b drop to architecture-change, provisional on dossiers. T02, T10a, T15 and T22 remain project-ending.

### Y-statement

*In the context of* Phase 0's TRL re-baseline under D-01 and D-02, with a one-way KDP-0B gate,

*facing* a three-model split on eight technologies, driven mostly by inconsistent scope and definitions rather than technical disagreement,

*we chose* a generating rule (CR-1: project-ending unless a credible, costed, non-common-cause fallback keeps 0B production above the economics gate), applied at function level and defaulting to project-ending,

*to achieve* protection against an irreversible commitment on an unproven function while not lengthening 0A for functions with real fallbacks,

*accepting* that T02 and possibly T10b will be held at TRL 6 longer than may prove necessary, and that the rule's safety depends on the quality of independent review of fallback dossiers.

### Toulmin structure

- **Grounds:** the ACH result that the split is mainly scope and definition, plus the heritage evidence in section 6.
- **Warrant:** D-02's principle that stringency follows reversibility. A class is reversible until KDP-0B, so the burden of proof belongs on the lower class, and the test should ask the question that defines "project-ending" (is there a fallback that keeps 0B viable?) rather than counting opinions.
- **Backing:** standard technology-readiness practice treats criticality, not maturity alone, as the driver of gate stringency.
- **Qualifier:** probably right for T02, T15, T22 and T10a. Provisional for T14, T24 and T25 until their dossiers exist.
- **Rebuttal:** if the economics model cannot discriminate fallback branches (A1 falsified), CR-1 collapses toward option A. In that case the owner should take the null option, with its longer 0A, rather than option D.

## 9. Consequences

**Enables:**
- KDP-0A scoping. Fallback dossiers for T02, T10b, T14, T24 and T25 become named 0A deliverables, each with a defined pass criterion.
- Classing the remaining disputed items (T09, T12, T20, T18, T11) under the same rule without reconvening the panel.
- A concrete test to hand to rq-0-64.

**Constrains:**
- `trl-baseline.yaml` must split T10 into T10a and T10b, and move T02 site arrays under T15.
- The economics model must carry fallback branches with TRL-tagged inputs.
- The propellant selection must be made by KDP-0A. That is now on T14's critical path.
- T22's TRL 6 definition is coupled to the demand gate's signed specification.

**Subsumes:** Claude's interim "hold at TRL 6, no waiver" becomes the formal default state under CR-1.

**Conflicts to watch:**
- If the 0A mid-term review shows the T02 dossier is unlikely to pass, T02 and T15 together become the pacing items for KDP-0B.
- That strengthens the case for the panel-agreed fallback ("0A only, Earth supply"). The owner should expect to decide this explicitly at the mid-term review rather than at KDP-0B.

**Evidence that would change this ruling overall:**
1. An economics-model audit showing it cannot price fallbacks. Revert to option A.
2. Evidence that the three models' scope differences were not the driver: for example, re-elicitation with fixed scope still splits. Then the disagreement is technical and per-item expert elicitation (Cooke or SHELF) should replace the rule-based inference.
3. Owner rejection of the broad reading of "project-ending" (trade-off point 2). T02 and T14 would then likely move to architecture-change.