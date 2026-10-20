---
questionId: "rq-0-70"
questionSlug: "licence-gate-redesign-reapply"
modelId: "claude-opus-5-5"
modelName: "Claude Opus 5.5"
roundNumber: 1
generated: "2026-10-17"
type: "discussion-response"
---

# g-licence failure: may 0B be redesigned and reapplied?

**Recommendation in one line:** allow **one** bounded reapplication, but only for failures pre-classified as recoverable. Every other failure class ends 0B and leaves 0A only, Earth supply. The gate criterion itself is never relaxed.

---

## 1. Frame & decision type

**What is being decided.** This sets the failure clause of g-licence. It is a property of the KDP-0B gate, not a new gate.

**Reversibility.** The rule is cheap to write and hard to change once pathfinder data exist. After a failure, any amendment looks like moving the goalposts. So the rule must be fixed **before** pathfinder design freeze.

**Cynefin domain.** The physics of tailings escape is *complicated*. Regulator behaviour and the binding limit are *complex*. Only the binding limit is unknown, because rq-0-41 is open and D-03 is unsigned. The rule therefore has to work for a limit nobody yet knows.

**The question hides a category error.** "Failure" covers at least six different events:

| Class | What happened |
|---|---|
| F1 | Measurement was inconclusive |
| F2 | Measured escape was modestly above the limit |
| F3 | Measured escape was grossly above the limit, or a credible abnormal event was uncontained |
| F4 | The regulator refused, or set a limit below what is physically achievable |
| F5 | ITU or national frequency coordination was incomplete |
| F6 | No binding limit existed at the gate |

A single answer of "final" or "reapply" for all six is wrong in both directions.

**How the D-02 "no waiver" principle applies.** A waiver means passing KDP-0B without meeting the criterion. A reapplication means meeting the same criterion later with a different design. These are different things. The real risk of reapplication is not that it waives the criterion. The risks are:
- escalation of commitment;
- erosion of the one-way door by repeated extensions;
- forum-shopping for a more lenient licensing state.

## 2. Criteria and weights (stated before options)

Swing weights are set by how much each criterion varies **across the plausible options**, not by how important it sounds in the abstract.

| # | Criterion | Swing range across options | Weight |
|---|---|---|---|
| C1 | **Gate integrity / pre-commitment.** Resistance to sunk-cost relitigation and to drift of the one-way door. | From "renegotiated in the room under pressure" to "mechanically pre-committed". This is the widest swing and goes to the core of D-02. | **30** |
| C2 | **Option value preserved.** Does the rule avoid killing a 0B whose failure was fixable? | From "every fixable defect is fatal" to "every fixable defect gets a chance". Large, because the first-article probability of meeting a ~99.99% retention target is modest (§6). | **25** |
| C3 | **Environmental harm and regulator credibility.** | Narrower than it looks. No option permits production above the limit, so on-orbit harm barely differs between options. What differs is pathfinder repeat-testing exposure and how the regulator reads our seriousness. | **15** |
| C4 | **Cost of delay and disruption to 0A.** | From "0A unaffected" to "0A starved by an open-ended 0B rescue". Moderate, provided the extension is funded from a ring-fenced line. | **15** |
| C5 | **Decision clarity / auditability.** Can a third party tell, from the record, which branch applies? | From "owner discretion" to "classification rule plus independent classifier". | **15** |

C3 is weighted below C1 and C2 for one reason: every option, including the strictest, keeps the emission limit absolute. If an option allowed even interim production above the limit, C3 would dominate and that option would be screened out as a Kepner-Tregoe *must*.

**Musts (binary screens):**
- No 0B production above the binding limit.
- No change of licensing state used to obtain a looser limit.
- TRL 6 in a relevant environment is re-demonstrated for any changed project-ending element, with no TRL waivers.

## 3. Options

| Option | Description | Disposition |
|---|---|---|
| **O0 – Null** | Leave the panel split as recorded and let the owner decide at the gate. | **Rejected.** This is the worst choice for C1 and C5. The decision would be made after the data, by the people with the most sunk cost. It turns D-02's pre-committed failure outcomes into a negotiation. |
| **O1 – Terminal** (Claude/Gemini) | Any g-licence failure → 0A only. | **Rejected as stated.** It treats an inconclusive measurement (F1) or a missing frequency filing (F5) like a factor-of-50 exceedance. That destroys option value for administrative or metrological reasons. It is also unenforceable in practice: an owner facing a 0.1 t/yr miss caused by a gasket will find a way round a rule that cannot tell a gasket from physics. |
| **O2 – Open reapplication** | Redesign and reapply as often as needed. | **Rejected.** It fails the integrity *must*. It is the textbook setting for escalation of commitment (Staw, "Knee-deep in the big muddy", 1976). |
| **O3 – Single bounded reapplication, all failures** (GPT as written) | One redesign within a time and cost box, regardless of cause. | **Partially adopted.** It is better than O1 and O2, but it grants an extension to unrecoverable classes (F3, F4). That spends 0A reserve on rescues that cannot succeed. |
| **O4 – Classified failure, single bounded reapplication for recoverable classes** | Failure class is fixed by a pre-committed rule and an independent classifier. F1/F2 get one bounded reapplication. F5 gets an administrative cure inside the same box. F3/F4 are terminal. F6 is "not ready", not "failed". | **Recommended.** |
| **O5 – Terminal for 0B, re-entry only as a new programme** | 0B ends. Any successor needs a fresh baseline and a full new KDP. | **Retained as the terminal branch of O4**, not as a standalone. It is honest, because nothing can stop a future programme decision. It is wasteful as the *only* path for F1/F2. |

## 4. Assessment matrix (QOC; 1 = poor, 5 = best)

| Criterion (weight) | O0 Null | O1 Terminal | O2 Open | O3 Bounded-all | O4 Classified |
|---|---|---|---|---|---|
| C1 Integrity (30) | 1 | 5 | 1 | 3 | 4 |
| C2 Option value (25) | 3 | 1 | 5 | 4 | 4 |
| C3 Harm/credibility (15) | 2 | 5 | 2 | 3 | 4 |
| C4 Delay/0A (15) | 2 | 5 | 1 | 3 | 4 |
| C5 Clarity (15) | 1 | 4 | 2 | 4 | 4 |
| **Weighted (/500)** | **180** | **395** | **260** | **345** | **400** |

**Reading the matrix:**
- O4 and O1 are effectively tied on the arithmetic. As Roy warns, MCDA structures a debate rather than computing a truth.
- The tie breaks on C2's real magnitude. If F1 or F2 is a likely first-article outcome, O1 throws away the most probable recoverable path.
- O4 scores 4 rather than 5 on C1 because classification is itself a judgement that can be gamed. The mitigation is an independent classifier and thresholds fixed in advance.
- O3 loses to O4 because funding F3/F4 rescues costs 0A reserve and credibility for no option value.

## 5. Sensitivity vs trade-off points

**Sensitivity points** (fact-dependent; the ruling moves if the fact moves):

- **S1 – Probability that first-article failure is recoverable (F1/F2 vs F3).**
  - If pathfinder or ground data show the containment architecture is within roughly a factor of 3 of the limit, O4 dominates.
  - If gross exceedance is the likely mode, O4 collapses to O1 in practice. The extension is rarely granted, and the only cost of keeping it is drafting.
- **S2 – Time-box length.**
  - Too short and redesigning containment to TRL 6 cannot fit, so O4 becomes O1.
  - Too long and 0A is disrupted, so O4 drifts toward O2.
  - I propose **≤ 18 months** from failure classification to resubmission.
  - The basis is that one hardware iteration of a containment module plus a repeat T08 relevant-environment campaign is plausibly 12–18 months. This is an engineering estimate at low confidence; the owner can tune it.
- **S3 – Whether the binding limit exists at KDP-0B (F6).**
  - If rq-0-41 has not produced a binding limit, the gate cannot be failed. It can only be not-ready.
  - This rule then hands over to D-01's option-expiry logic. Conflating the two would let an unresolved regulator question consume the single reapplication.
- **S4 – The F2/F3 threshold.** I propose **> 10× the binding limit** (central estimate) as F3. The reasoning is that a tenfold retention improvement within one iteration is not credible without architecture change, and architecture change is a restart.
  - With a 1 t/yr limit, 10 t/yr means retention falling from about 99.99% to about 99.9%. Those are different design classes.
  - For scale: GPT's 99.992–99.998% retention figure implies a tailings throughput of about 12.5–50 kt/yr at the 1 t/yr limit.

**Trade-off point** (a values question; the owner decides, evidence cannot settle it):

- **T1 – Option value vs pre-commitment discipline.** How much recoverable 0B value is the owner willing to forgo to make the one-way door unarguable? Claude's earlier "no waiver, final" position puts infinite weight on discipline. GPT's position puts more on option value. O4 is my judgement of the balance, not a derivation.
  - If the owner's revealed preference is that any post-failure deliberation is corrosive, O1 is legitimate.
  - That disagreement should be **recorded, not averaged**.

**Second trade-off point:**

- **T2 – Throughput reduction as a cure.** Lowering throughput can bring escape under the limit. It also moves g-economics and g-demand in the wrong direction.
  - Allowing it is a values choice: how small a 0B is still worth doing.
  - The rule should allow it only if both gates are re-run and still pass. It should not pre-judge the answer.

## 6. Evidence certainty (GRADE certainty; likelihood kept separate)

| Claim | Likelihood (IPCC terms) | Confidence / GRADE | Basis |
|---|---|---|---|
| First-article pathfinder meets a ~1 t/yr escape limit with detection limit ≤ 10% of limit | About as likely as not | **Very low** | No flight heritage for vacuum or low-g regolith tailings containment at 99.99%. Terrestrial baghouse and filter efficiencies (≥ 99.9%) transfer poorly. |
| If it fails, failure is F1/F2 rather than F3 | Likely | **Low** | Engineering judgement: designs targeted at a limit tend to miss by small factors unless an unmodelled mode exists. Credible abnormal events (GPT's inclusion) widen the tail. |
| Bounded, pre-committed extensions curb escalation of commitment better than discretionary ones | Likely | **Moderate** | Escalation-of-commitment literature (Staw 1976 and successors). Transfer to space programme gates is inferential. |
| Licensing states will issue numeric annualised escape limits for mining tailings by KDP-0B | About as likely as not | **Very low** | No existing licensing framework for this activity class. Debris mitigation regimes target spacecraft and mission-related objects. For context: Outer Space Treaty Arts VI/IX (authorisation, due regard); IADC Space Debris Mitigation Guidelines; ISO 24113. |
| Frequency coordination for 15–29 assets fits within 18 months if begun early | Likely if filed during 0A, unlikely if filed at the gate | **Low–moderate** | ITU Radio Regulations advance-publication and coordination timelines are typically multi-year for non-geostationary systems. This is why F5 must be filed during 0A, not cured afterwards. |

## 7. Key assumptions (with falsifiers) and competing hypotheses

| Assumption | Falsified by |
|---|---|
| **A1** – Failure classes can be assigned objectively from pathfinder data. | A dry run on synthetic or ground data in which two independent reviewers disagree on class in more than 1 in 5 cases → thresholds must be sharpened, or default to O1. |
| **A2** – One hardware iteration fits in about 18 months. | 0A containment-module schedule data showing build-test cycles longer than 18 months → lengthen the box (≤ 24 months) or accept O4 ≈ O1. |
| **A3** – The 0A reserve can fund one rescue without breaching D-01. | A 0A budget showing reserve below the cost of a repeat T08 campaign → the extension is unfundable, so choose O1 honestly rather than an unfunded O4. |
| **A4** – Regulators treat a reapplication with an improved design as legitimate, not as evidence of unreliability. | rq-0-41 engagement shows the licensing state penalises resubmission → F2 effectively becomes F4. |
| **A5** – Changing containment does not change project-ending technologies beyond T04/T08/T19. | Design analysis showing containment changes propagate into process chemistry or thermal architecture → restart, not reapplication. |

**ACH on why g-licence would fail** (hypotheses ranked by least disconfirmed today; none is yet disconfirmed):

1. **H-meas – metrology immaturity.** Detection at ≤ 0.1 t/yr is unproven. *Least disconfirmed and most likely to be the first failure.*
2. **H-eng – fixable engineering defect** (seals, transfer interfaces, venting).
3. **H-reg – limit set tighter than the design point.**
4. **H-phys – architectural escape floor above the limit.**

Because the two highest-ranked hypotheses (H-meas, H-eng) are the recoverable ones, a purely terminal rule is weakly supported. **The ACH ranking is what tips the matrix tie toward O4.** Ground tests showing an escape floor would promote H-phys, and that would justify O1.

## 8. Decision, warrant, accepted downside

**Y-statement.** *In the context of* a one-way KDP-0B gate under D-02, with an interim, unsigned ≤ 1 t/yr limit (D-03) and an open rq-0-41, *facing* a panel split between terminal failure and open-ended redesign, *we chose* a classified-failure rule with at most one bounded reapplication for recoverable classes only, *to achieve* pre-committed, auditable gate integrity without forfeiting a 0B whose shortfall is metrological or a modest engineering miss, *accepting* up to 18 months' delay to the 0B decision, a ring-fenced 0A reserve draw, and residual risk that classification is contested.

**Warrant (Toulmin).** D-02 ties stringency to reversibility. What must be irreversible is the *criterion* and the *outcome of exhausting the rule*, not the first attempt. One pre-committed, capped retry does not lower the criterion, so it is not a waiver. Unbounded or discretionary retries do lower it in practice, and are excluded.

**Qualifier.** This holds presumably, given A1–A3.

**Rebuttal.** If the owner rules T1 toward absolute discipline, or A1 fails in the dry run, adopt O1. That disagreement with the Claude/Gemini position should be preserved in `decisions.md`.

**Proposed rule text (g-licence, failure clause):**

> **G-LIC-F.1 Basis.** g-licence is assessed against the *binding* limit set by the licensing state per rq-0-41 (limit, particle/velocity classes, confidence level, averaging interval, abnormal-event limits). If no binding limit exists at KDP-0B, the gate status is **NOT READY**, not FAILED. NOT READY is governed by D-01 option expiry and does not consume a reapplication.
>
> **G-LIC-F.2 Pass.** Pass requires the uncertainty-bounded annualised escape, including credible failures, to lie below the binding limit at the stated confidence. The detection limit must be ≤ 10% of the limit. T04, T08 and T19 must be at TRL 6 in a relevant environment. ITU and national frequency filings must be accepted.
>
> **G-LIC-F.3 Classification.** On non-pass, an independent review board **not funded by 0B** classifies the result using thresholds frozen at pathfinder PDR:
> - **F1** — central estimate below the limit, upper bound above it.
> - **F2** — central estimate between 1× and 10× the limit.
> - **F3** — central estimate above 10× the limit, or an uncontained credible abnormal event.
> - **F4** — the licensing state refuses, or sets a limit the board judges unachievable by the demonstrated architecture class.
> - **F5** — the only shortfall is frequency coordination.
>
> **G-LIC-F.4 Outcomes.**
> - **F3, F4: terminal.** No 0B production. Programme proceeds as 0A only, Earth supply. Any successor is a new programme decision with a full new KDP.
> - **F1, F2, F5:** **one** reapplication. Resubmission within **18 months** of classification. Cost capped at a ring-fenced line set at KDP-0B entry. No 0B long-lead commitments during the extension. 0A milestones are unaffected.
> - A second non-pass of any class is **terminal**.
>
> **G-LIC-F.5 Permitted changes without restarting KDP-0B:**
> - containment hardware;
> - operating procedures and duty cycle;
> - measurement instrumentation and campaign length;
> - throughput *reduction*, provided g-economics and g-demand are re-run and pass on the reduced case.
>
> Every changed project-ending element must re-demonstrate TRL 6 in a relevant environment. No TRL waivers.
>
> **G-LIC-F.6 Changes that require a full new KDP-0B** (and do not count as reapplication):
> - change of target body or site (re-opens g-target);
> - change of processing architecture or chemistry;
> - addition of a project-ending technology;
> - throughput increase;
> - change of licensing state.
>
> Under any new state, the applicable limit is no looser than the stricter of the original binding limit and the D-03 ALARP value. This is the anti-forum-shopping clause.
>
> **G-LIC-F.7** The binding limit is never relaxed by the programme to produce a pass.

**Accepted downside.** We accept a possible 18-month slip, one reserve draw, and the chance that a modest F2 consumes the retry and then fails anyway. We also accept that F4 ends 0B even when the regulator, not the engineering, is the obstacle. That is intended: a project that only works under a lenient state is not licensable in the sense D-02 means.

## 9. Consequences (Kruchten relations)

**Constrains:**
- **D-03** must be signed, and the F1–F5 thresholds frozen, **before pathfinder PDR**. Otherwise G-LIC-F.3 is set after the data and O4 degrades to O0.
- **rq-0-41** becomes schedule-critical. Its output defines the averaging interval and confidence level that F1/F2 depend on.
- **Frequency filings** move into 0A. F5 can only be cured within 18 months if filing began years earlier.
- **0A budget** must carry a named g-licence reapplication reserve, or the rule defaults to O1 (A3).
- **Pathfinder design** should target a central estimate below 0.3× the limit, so that F1 rather than F2 is the likely miss mode.

**Enables:**
- an auditable KDP-0B record;
- a containment trade study that is explicitly allowed to iterate once;
- a clean hand-off of the "no binding limit yet" case to D-01's expiry logic rather than to this gate.

**Conflicts with:**
- the Claude/Gemini terminal position (preserved as the T1 alternative);
- any reading of D-02 in which "no waiver" means "no second attempt".

**Evidence that would change this ruling:**
1. A classification dry run with poor inter-rater agreement (→ O1).
2. Ground or vacuum-chamber data showing an architectural escape floor near or above the limit, i.e. H-phys promoted (→ O1).
3. 0A schedule data showing containment iteration longer than 24 months (→ O1, or a longer box with owner sign-off).
4. rq-0-41 showing that the licensing state treats resubmission neutrally and publishes a numeric limit early (→ strengthens O4; could justify allowing F2 up to 10× with confidence).
5. Evidence that the owner's own governance cannot resist discretionary extension (→ O1, because the rule is only as strong as its enforcement).