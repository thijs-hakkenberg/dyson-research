---
questionId: "rq-0-69"
questionSlug: "phase-0-sunset-rule"
modelId: "gpt-6-1-sol"
modelName: "GPT-6.1 Sol"
roundNumber: 1
generated: "2026-10-17"
type: "discussion-response"
---

## 1. Frame & decision type

**Recommendation: make M180 an automatic expiry of the existing 0B development authorisation, with “0A only, Earth supply” as the default programme disposition. Require a review before expiry; do not let a missed decision extend funding. Any continuation needs a new, explicit, bounded owner decision.**

This separates three things that the present wording risks conflating:

- **A planning boundary:** when the integrated schedule expects a decision.
- **An authority boundary:** when permission to continue spending expires.
- **A supply commitment:** what Earth-supply contracts are actually authorised.

M180 should perform the first two functions, **not automatically create a fifteen-year Earth-supply procurement commitment**.

This is an **executive governance decision** governing a reversible option and its eventual one-way exercise. It must preserve D-01’s demand-sized real option and D-02’s non-waivable KDP-0B requirements.

I use the supplied extracts from `gates.md`, `gates-proposal.yaml`, `trl-baseline.yaml`, and `decisions.md`; I have not independently inspected those files. Proposed dates and controls below are recommendations, not existing specifications.

## 2. Criteria and weights

### Mandatory constraints

Before weighted assessment, any adopted policy must:

1. Preserve the KDP-0B TRL 6 relevant-environment requirement for project-ending technologies, without waivers.
2. Require signed Phase 1 demand to size 0B at the gate.
3. Prevent schedule approval, silence, or option-keeping expenditure from becoming implicit production authority.
4. Preserve safety, legal compliance, and necessary disposition of existing assets when funding authority expires.

### Swing weights

These weights value movement across the **specified worst-to-best ranges**, not abstract importance.

| Criterion | Range being valued | Weight | Why this swing merits the weight |
|---|---|---:|---|
| **C1. Financial exposure control** | Ambiguous duration and cumulative spend → enforceable expiry and capped exceptions | **30%** | Fifteen years of potentially repeated deferrals makes cumulative exposure the largest governance concern. |
| **C2. Decision integrity and reversibility** | Silence can determine programme direction → accountable, explicit decisions without premature irreversible commitments | **25%** | D-01 and D-02 explicitly distinguish preserving an option from exercising it. |
| **C3. Avoidable capability loss** | Abrupt loss of valuable teams, data, assets and learning → proportionate retention where justified | **20%** | Space-system capability can be expensive to reconstruct, but retaining it cannot justify indefinite development. |
| **C4. Operational executability** | Unclear ownership and contracts at expiry → implementable transition with auditable authority | **15%** | A sunset that cannot be executed safely or contractually is not a credible control. |
| **C5. Demand and schedule adaptability** | Fixed response despite changed demand → bounded adjustment to material new evidence | **10%** | Adaptability matters, but must remain subordinate to financial control and gate integrity. |

These are proposed owner values, not empirically measured weights.

## 3. Options

**N — Null: leave the panel split unresolved.**  
Argument for: avoids deciding before rq-0-63 establishes the integrated schedule.  
**Reject:** baseline and contracting decisions would inherit an unresolved authority question. Silence is not a neutral implementation rule.

**A — Hard automatic fallback at M180.**  
All permitted slips terminate at M180 and the existing programme executes fallback, with no continuation route within this policy.  
Argument for: strongest pre-commitment against drift.  
**Reject as the complete rule:** it needs a more precise definition of “fallback” and can destroy useful capability regardless of the marginal cost of preservation. If “fallback” means a long-term procurement commitment, it also exceeds what a sunset should authorise.

**B — M180 is only a mandatory decision point.**  
The owner reviews the programme and selects continuation, deferral or fallback.  
Argument for: accommodates uncertain mission schedules and future demand.  
**Reject unless paired with an expiry default:** it leaves unresolved what happens if the owner does not decide. If all relevant authority expires pending that decision, this converges toward Option C.

**C — Automatic authority expiry, pre-expiry review, explicit replacement authority.**  
Absent a new owner decision, the existing 0B development authorisation expires at M180 and fallback becomes the programme baseline. A new decision may authorise tightly bounded preservation or corrective work, but cannot waive KDP-0B.

**Select C.** It preserves Claude’s enforceable default while accepting GPT’s objection to interpreting a planning date as automatic authority for a long-duration commitment.

## 4. Assessment matrix

**QOC question:** What should M180 do if KDP-0B has not passed?

Scores: **0 = worst, 4 = best** within the criterion ranges above. Totals are weighted scores out of 100. These are transparent policy judgments, not predicted programme outcomes.

| Option | C1 Exposure 30% | C2 Integrity 25% | C3 Capability 20% | C4 Execution 15% | C5 Adaptability 10% | Total |
|---|---:|---:|---:|---:|---:|---:|
| N — Unresolved split | 0 | 2 | 2 | 0 | 1 | **25.0** |
| A — Hard automatic fallback | 4 | 2 | 1 | 3 | 2 | **63.8** |
| B — Decision point only | 1 | 4 | 4 | 2 | 4 | **70.0** |
| **C — Expiry plus explicit replacement authority** | **3** | **4** | **3** | **4** | **3** | **85.0** |

C loses a point on exposure because exceptions can increase cumulative expenditure, and loses capability/adaptability points because an expiry can still cause interruption. Those are real costs, not implementation defects to assume away.

## 5. Sensitivity vs trade-off points

### Sensitivity points — facts or implementation details

- **Meaning of “automatic fallback.”** If it means only cessation of 0B development and adoption of an Earth-supply baseline, the disagreement with C narrows substantially.
- **rq-0-63 schedule feasibility.** If an independently reviewed critical path cannot plausibly support qualification and gate review by M180, the owner must reconsider the date explicitly—not allow the schedule team to move it implicitly.
- **Preservation cost and restart cost.** Low preservation cost relative to demonstrable restart cost strengthens C. Expensive preservation with little retained value strengthens A.
- **Enforceability of exceptions.** If budgets and contracts cannot prevent recurring “temporary” extensions, C’s exposure score falls sharply.

With the illustrative scores held fixed and other weights reduced proportionally, A overtakes C only when exposure control receives roughly **62%** of total weight. This is a weight sensitivity test, not evidence that C is objectively optimal.

### Trade-off points — owner values

- **Credible fiscal commitment versus preserving a potentially valuable capability.**
- **Protecting future-owner discretion versus binding the programme against drift.**
- **Accepting a temporary capability interruption versus funding continuity before demand exists.**

These cannot be settled by better schedule estimates alone.

## 6. Evidence certainty

GRADE labels below describe certainty supporting the substantive claim. Likelihood is stated separately; no numerical probabilities are justified by the supplied material.

| Key claim | Evidence and GRADE certainty | Likelihood versus analytic confidence |
|---|---|---|
| D-01 and D-02 require a demand-sized option and non-waivable technical readiness at KDP-0B. | Explicit in the supplied accepted-decision summaries. **High certainty for the supplied governance record**, not independently verified against files. | Documentary interpretation, not a probabilistic forecast; **high confidence**. |
| The supplied positions do not establish M180 as an integrated, feasible critical-path deadline. | Wide KDP-0B windows and GPT’s reference to rq-0-63. **Low certainty about actual schedule feasibility**. | Whether M180 is achievable: **likelihood unassessed; low confidence**. |
| Explicit expiry removes authority arising merely from inaction. | Direct consequence of the proposed rule, subject to enforceable budget and contractual implementation. **Moderate certainty**. | **High confidence in the rule’s logic**; actual compliance likelihood remains unquantified. |
| The expiry rule will reduce actual expenditure drift. | Plausible governance mechanism, but no Project Dyson expenditure or exception-history evidence supplied. **Low certainty**. | Direction is plausible; magnitude and likelihood are **unquantified, low confidence**. |
| Limited preservation may cost less than later reconstitution. | No asset inventory, retention plan or restart estimate supplied. **Very low certainty**. | Could be true for particular assets; **likelihood unassessed, low confidence**. |
| Expiry alone does not justify long-term Earth procurement. | Consistent with D-01’s demand-sized approach and separation of supply strategy from purchasing authority. **Moderate certainty as governance interpretation**. | Not a forecast; **high confidence** in the distinction. |

The weakest evidential link is **the economic value of keeping the option alive**, not the ability to write an expiry rule.

## 7. Key assumptions

| Assumption | Evidence that would falsify it |
|---|---|
| 0B development authority can be separated from 0A operations, safety and preservation obligations. | Contractual and systems dependency analysis showing that stopping 0B necessarily disables essential 0A functions or creates unacceptable hazards. |
| The owner can act before expiry. | Governance and procurement lead-time analysis showing that a complete decision cannot be obtained within the proposed review period. |
| Earth supply can serve as the fallback baseline. | A qualified supply-chain and delivery analysis demonstrating that required Phase 1 demand cannot be met through Earth supply within acceptable constraints. |
| Some option-retention activities may have positive value. | Independent costing showing preservation costs exceed conservative avoided restart costs and credible information value. |
| M180 is a defensible provisional limit, though not yet a demonstrated schedule outcome. | rq-0-63 showing an unavoidable, justified critical path beyond M180, or showing that a materially earlier sunset achieves the same capability outcome. |

### Competing hypotheses: least-disconfirmed ranking

This is a provisional ACH assessment, not a probability ranking:

1. **Expiry plus separately authorised retention best reconciles the accepted decisions.** Least disconfirmed by D-01’s option framing and the need for bounded spending.
2. **Hard fallback is necessary to stop drift.** Plausible, but not yet supported by evidence that bounded exceptions cannot be controlled.
3. **A mandatory review alone provides adequate control.** Most challenged by the unresolved outcome when no decision is made.

Evidence of systematic abuse of capped exceptions would move hypothesis 2 upward.

## 8. Decision, warrant, accepted downside

### Proposed gate-rule text

> **Sunset and authority expiry.** Unless KDP-0B has been formally passed, existing authorisation for 0B development expires at M180, measured from the programme epoch recorded in the controlled baseline. Schedule re-baselining does not reset that epoch.
>
> **Pre-expiry review.** The owner shall receive a sunset disposition package by M168, or earlier if contractual notice and safe-transition lead times require. The package shall recommend KDP-0B approval, fallback, or a separately authorised bounded programme.
>
> **Default disposition.** Without replacement authority effective before expiry, cease new discretionary 0B development commitments and adopt “0A only, Earth supply” as the planning baseline. Execute only authorised 0A activities, unavoidable obligations, safety and compliance work, and approved transition or disposition tasks. This does not authorise a long-term Earth-supply purchase.
>
> **Replacement authority.** Any post-sunset corrective or preservation programme requires a new owner decision specifying scope, absolute funding cap, expiry, deliverables, stop conditions and cumulative expenditure. No evergreen option-keeping allowance is permitted.
>
> **Gate integrity.** Replacement authority does not constitute KDP-0B approval and cannot waive its technical, target, demand, economics or licence requirements.

**Warrant:** a real option requires both a controlled exercise decision and a controlled cost of waiting. Expiring the old authority controls waiting; a new decision preserves accountability when circumstances genuinely change.

**Accepted downside:** capability continuity may be interrupted, preservation may prove uneconomic, and preparing the review consumes resources. These are preferable to implicit continuation.

## 9. Consequences

- **rq-0-63:** establish the epoch, assess M180 feasibility, and include gate-review, contractual notice and safe-stop durations. It may recommend changing the sunset; it cannot change spending authority by itself.
- **KDP-0B window:** retain M180 as the provisional outer limit under current authority. The panel’s 72–180-month envelope is not evidence of a validated schedule.
- **Failure outcomes:** corrective plans, scout waves and slips remain inside the sunset unless a new owner decision explicitly supersedes that constraint. No silent clock restart.
- **Demand deferral:** before sunset, option-keeping requires a separately identified budget and evidence-producing scope. After sunset, there is no automatic entitlement to continue it.
- **Permitted preservation:** justify specific data, samples, software, storage, minimum maintenance or time-limited personnel retention. Do not disguise production tooling, facility expansion or long-lead production procurement as preservation.
- **Change evidence:** move toward a harder sunset if exception controls fail; reconsider timing if rq-0-63 establishes an unavoidable critical-path conflict; permit bounded retention only when independently reviewed costs and benefits support it.

**Final Y-statement:** In the context of D-01’s demand-sized 0B real option and D-02’s non-waivable readiness gate, facing an unresolved M180 sunset, we chose automatic expiry of existing 0B development authority with a pre-expiry review and explicit replacement-authority mechanism, to achieve credible spending control without silently committing to long-term supply, accepting possible capability interruption and the administrative cost of justified exceptions.

**Warrant and qualifier:** this preserves accountable choice while making inaction terminate discretionary authority; it remains conditional on enforceable financial controls and rq-0-63 validating—or explicitly prompting revision of—the sunset date. It **enables** bounded preservation and demand-driven re-entry, and **constrains** automatic extensions, schedule-driven clock resets, gate waivers and unapproved long-term procurement.