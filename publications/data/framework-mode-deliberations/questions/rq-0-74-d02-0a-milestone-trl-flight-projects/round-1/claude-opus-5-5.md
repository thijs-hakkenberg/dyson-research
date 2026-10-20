---
questionId: "rq-0-74"
questionSlug: "d02-0a-milestone-trl-flight-projects"
modelId: "claude-opus-5-5"
modelName: "Claude Opus 5.5"
roundNumber: 1
generated: "2026-10-17"
type: "discussion-response"
---

# D-02 for 0A flight projects: a ruling

## 1. Frame & decision type

**The question.** D-02 sorts gates into two classes. One-way gates (KDP-0B) need TRL 6 in a relevant environment. "Two-way, internal 0A milestones" need TRL 4–5. 0A also contains flight projects (scouts and the pathfinder), and each has its own lifecycle gates: PDR, CDR, and launch readiness. Are those gates "internal 0A milestones" in D-02's sense?

**Decision type.** This is a *property* decision about the gate regime, in Kruchten's terms, with an *executive* element: does the accepted text change?

- **Reversibility.** The decision itself is cheap to revise before any 0A project reaches PDR. The cost of a wrong rule shows up later as cost growth or a lost flight, and those cannot be undone.
- **Cynefin domain.** Complicated. The relevant practice is well documented, and a defensible answer exists.

**My framing claim.** D-02's principle ("stringency follows reversibility") is right. Its sentence about categories is a heuristic that misclassifies flight projects.

- A 0A launch is one-way. The hardware is gone, the slot is spent, and so is the integration cost.
- A project PDR is also close to one-way, because it is the point where design and build spending is committed.
- The MTR tranche release is genuinely two-way. A tranche can be withheld, re-scoped or re-released.

So the disagreement is not really about TRL numbers. It is about whether to classify by **who owns the gate** (0A vs 0B) or by **what the gate commits**. D-02's own principle says the second.

There is a second distinction no panelist drew, and it matters more than the numbers. A flight project carries two kinds of technology:

- **Enabling technologies.** If these fail, the mission ends with no useful data: bus, power, comms, ADCS, propulsion when it is not the experiment.
- **Technologies under test.** The flight exists to raise these from TRL 5–6 to TRL 7.

Requiring TRL 8 for a technology under test before its own demonstration flight is a contradiction. Requiring only TRL 4–5 for an enabling technology at PDR invites the cost-growth pattern that the evidence below documents.

## 2. Criteria and weights (stated before options)

Swing weights reflect the spread between the best and worst option on each criterion, not its abstract importance.

| # | Criterion | Swing weight | Why this weight fits the range |
|---|---|---|---|
| C1 | **Loss avoidance on irreversible commitments.** Avoid cost and schedule growth after PDR, and avoid flights lost without data. | **0.30** | Widest consequence range. At worst, a pathfinder lost to an immature bus, which could consume a large share of 0A funds and credibility. At best, failures are confined to the experiment and still yield data. |
| C2 | **Learning yield and tempo.** Protect 0A's purpose as a fast capability programme (D-01). | **0.25** | Wide range. Over-strict gates push scouts right by quarters. Lax gates bring early flights that may teach little. |
| C4 | **Unambiguity and auditability.** A reviewer can apply the rule without asking the owner. | **0.20** | The panel split is itself evidence that the current text fails here. The range runs from "three reviewers, three readings" to a mechanical test. |
| C3 | **Fidelity to D-02 and minimal governance churn.** | **0.15** | Moderate range. Every option keeps D-02's principle. They differ only in whether the text changes. |
| C5 | **Cost of compliance.** Extra ground relevant-environment testing before PDR. | **0.10** | Narrow range. Engineering-model environmental tests are a small fraction of flight-project cost and are partly incurred anyway. |

These are musts, applied before scoring (Kepner-Tregoe):

- **M1.** KDP-0B keeps TRL 6 in a relevant environment with no waivers, as accepted.
- **M2.** The rule must not require a technology to reach the TRL its own flight is meant to produce.

## 3. Options

**O0 — Null: leave the split.** Each reviewer applies their own reading. Claude enforces TRL 6 at PDR, GPT TRL 8 before launch, Gemini TRL 4–5 at the MTR only.

- **Rejected.** It fails C4 by construction, and the gate outcome would depend on which reviewer sits on the board.
- It also passes the real disagreement to the first scout PDR, the worst time to settle it.
- The null option's one virtue is no governance churn. That virtue is not worth the ambiguity.

**O1 — Literal D-02: TRL 4–5 at every 0A gate, including flight PDR.**

- **Rejected.** It contradicts D-02's own principle.
- It would approve design commitment on enabling technologies at TRL 4, against established NASA practice (TRL 6 by PDR) and DoD practice (TRL 6 at Milestone B).
- It is the option most likely to produce the "0A slips and overruns" story that would discredit the 0B real option D-01 depends on.

**O2 — Claude's panel position: TRL 6 at project PDR for all scout and pathfinder critical technologies; 4–5 only for 0B development milestones.**

- **Partly adopted.** It is right about enabling technologies.
- It is too blunt for technologies under test. If the pathfinder payload (T04, T05, T08, T16, T19, T24) must be fully TRL 6 at PDR, 0A pays for a full ground relevant-environment campaign before design commitment.
- The schedule then slips for a flight whose value is to retire environmental uncertainty that ground tests capture poorly (long-duration vacuum, thermal cycling, operational microgravity).
- It also misses M2's subtlety: the experiment's *flight* TRL comes from the flight.

**O3 — GPT's position: TRL 4–5 at MTR as tranche releases; TRL 8 before launch; no PDR technology gate.**

- **Partly adopted.** It is right that the MTR is a tranche decision, and right that "unmet ⇒ no planned demonstration" is a clean rule.
- It fails M2 as written: "TRL 8 before launch" cannot apply to a technology under test. It should be read as "flight system qualified and accepted," which is a qualification statement, not a TRL.
- Leaving PDR unguarded is the main defect. Immaturity found at CDR or in qualification costs far more than immaturity found at PDR.

**O4 — Recommended: classify gates by commitment and technologies by role.**

| Gate | Requirement |
|---|---|
| MTR tranche releases (two-way) | TRL 4–5, as GPT and Gemini propose |
| Project PDR (one-way for design commitment) | Enabling technologies at TRL 6; technologies under test at TRL 5, with a documented relevant-environment definition and a test plan |
| Before CDR or flight-unit build | Technologies under test pass a ground test of the failure modes that would leave the flight yielding no data |
| Launch readiness (one-way) | Flight system qualified and accepted (enabling elements effectively TRL 8); technologies under test at TRL 6 for those failure modes |

D-02 is amended for clarity: the principle is unchanged and the category sentence is replaced by a reversibility test.

**O5 — Tie TRL to a NASA-style mission risk class (e.g., NPR 8705.4 Class D for scouts).**

- **Not adopted as the primary rule.** It is absorbed as a waiver path.
- Risk class is a useful vocabulary, but it governs assurance processes, not technology maturity.
- Using it alone would let "Class D" become a blanket reason to skip maturity gates.
- In O4, a scout may waive the TRL 6 enabling-technology requirement only with an owner-signed Class D risk acceptance. This is permitted because the D-02 no-waiver clause binds only KDP-0B.

## 4. Assessment matrix (QOC)

Scores run from 1 (poor) to 5 (best).

| Option | C1 Loss avoidance (0.30) | C2 Learning tempo (0.25) | C4 Unambiguity (0.20) | C3 D-02 fidelity (0.15) | C5 Compliance cost (0.10) | **Weighted** |
|---|---|---|---|---|---|---|
| O0 Null split | 2 | 3 | 1 | 3 | 4 | **2.40** |
| O1 Literal 4–5 | 1 | 4 | 4 | 2 | 5 | **2.90** |
| O2 TRL 6 at PDR, all | 5 | 2 | 4 | 3 | 2 | **3.45** |
| O3 MTR 4–5 + TRL 8 launch | 3 | 3 | 3 | 4 | 3 | **3.15** |
| **O4 Role × commitment** | **4** | **4** | **4** | **4** | **3** | **3.90** |

Notes on the scores:

- **O4's C4 score is 4, not 5.** Classifying a technology as "enabling" or "under test" takes judgment. The mitigation is that each project declares the classification in its Technology Development Plan, and the classification is fixed at SRR.
- **O1 scores 2 on fidelity.** It honours D-02's text while violating D-02's principle.

## 5. Sensitivity vs trade-off points

**Sensitivity points.** Each of these is one decision that strongly drives one attribute.

- **S1 — The enabling vs under-test classification.** This one choice drives C1. If propulsion is labelled "under test" on a scout whose mission fails without it, O4 collapses into O1 for that project. *Mitigation:* a technology counts as enabling if its failure leaves the flight with less than a stated minimum data return. Define that floor in each project's success criteria.
- **S2 — The cost-at-risk share of the pathfinder.** If the pathfinder is a large fraction of 0A's budget, its loss changes the programme, not just the project. Its PDR then becomes one-way at programme level. *Rule:* above a threshold (I propose 25 % of 0A budget, an owner value), pathfinder PDR follows the KDP-0B rule with no waivers for enabling technologies.
- **S3 — Launch-window rigidity.** A scout with a rare target window, such as an asteroid flyby with a multi-year next opportunity, has a far less reversible launch than a rideshare to low Earth orbit. Window rigidity should raise stringency on that scout.

**Trade-off points.** These are values questions, not facts to settle.

- **T1 — Flight-loss risk vs learning tempo (C1 vs C2).** O2 overtakes O4 only if w₁ > 2w₂ + w₃ + w₅.
  - With w₃ and w₅ held at 0.15 and 0.10, O2 wins at roughly w₁ ≥ 0.5 with w₂ ≤ 0.12.
  - In words, O2 wins only if the owner weights avoiding loss about four times more than learning tempo.
  - That would contradict D-01's framing of Phase 0 as a capability programme, but it is the owner's call. I do not claim it is settled by fact.
- **T2 — Waivability on scouts (C2 vs C4).** Allowing Class D waivers buys tempo but reintroduces judgment. I accept it because scouts are where D-01's real-option logic most wants cheap shots on goal.

## 6. Evidence certainty

| Claim | Evidence | GRADE certainty | Likelihood (calibrated) |
|---|---|---|---|
| Projects entering design commitment with critical technologies below TRL 6 show higher cost and schedule growth | GAO's annual *Assessments of Major Projects* for NASA, repeated over many years; DoD Milestone B practice codified in statute (10 U.S.C. §2366b, now §4252) | **Moderate** for large projects: observational, consistent, confounded by project size. **Low** for small scouts: indirect. | *Likely* (≈66–90 %) that it holds for the pathfinder; *about as likely as not* for small scouts |
| TRL 6 by PDR is established NASA practice | NPR 7123.1 / NASA SP-2016-6105 Systems Engineering Handbook; ESA ECSS-E-HB-11A TRL guidance | **High**: documented policy and practice | n/a (factual) |
| A technology demonstration flight can legitimately carry a technology below TRL 7 | The TRL definitions themselves (Mankins; ECSS): flight demonstration is how TRL 7 is reached | **High** | n/a |
| TRL ratings are reproducible to within one level between assessors | Mankins (2009), *Technology readiness and risk assessments*, Acta Astronautica, which proposes AD² precisely because TRL alone is insufficient; general assessor-variance literature | **Low** | *About as likely as not*. This is why I support Claude's AD² ≤ 5 check as a companion. |
| Small-satellite missions using immature buses fail more often | Published smallsat reliability surveys exist but mix many causes | **Low** | *Likely* in direction; magnitude uncertain |

**Overall confidence in the ruling: medium.** The direction is well supported by high-certainty practice and moderate-certainty outcome data. The specific thresholds (TRL 5 at PDR for technologies under test, the 25 % pathfinder threshold) are engineering judgment with low direct evidence.

## 7. Key assumptions (with falsifiers) and competing hypotheses

| # | Assumption | What would falsify it |
|---|---|---|
| A1 | 0A launches are effectively one-way: non-refundable slots, no rapid reflight | Rideshare contracts with refundable slots *and* a scout unit cost and build time that allow a reflight within about 6–9 months. Then scout launches are near two-way and O1-level stringency becomes defensible for scouts (not the pathfinder). |
| A2 | Enabling and under-test technologies can be separated cleanly per project | A project where the payload *is* the bus, for example a propulsion-demonstration scout. That project must then meet TRL 6 at PDR for the thing it demonstrates, in a ground relevant environment. |
| A3 | Ground relevant-environment tests for enabling technologies cost little relative to the flight project | Cost estimates in the 0A plan showing these tests above about 15 % of a scout's cost. Then C5's weight should rise and Class D waivers become routine. |
| A4 | MTR precedes all 0A flight-project PDRs | A scout PDR scheduled before the MTR. The PDR gate then governs that scout, and the MTR TRL 4–5 criterion is irrelevant to it. |

**ACH over the three readings**, ranked by least disconfirmed:

| Hypothesis | Disconfirming evidence | Status |
|---|---|---|
| **H3 (O4):** reversibility is graded by commitment and by technology role | Nothing material. A2 is a stress, handled by the propulsion-scout rule. | **Least disconfirmed** |
| **H1 (Claude):** every 0A flight gate is one-way, so TRL 6 at PDR applies to all critical technologies | M2. Technologies under test would be over-gated before their flight produces TRL 7. | Second |
| **H2 (implicit in Gemini and GPT):** 0A flights are cheap and repeatable, so 0A gates are two-way | Non-refundable launch slots, rigid target windows, and pathfinder cost share. Also GPT's own "TRL 8 before launch," which concedes launch is one-way. | **Most disconfirmed** |

## 8. Decision, warrant, accepted downside

**Ruling.** Amend D-02 by clarification. The principle is unchanged. The sentence classifying "internal 0A milestones" as two-way is replaced by a reversibility test, plus a flight-project clause. This is an amendment, not an interpretation: three panelists read the existing text three ways, and an "interpretation" that adds the enabling vs under-test distinction is new rule text whatever it is called.

**Proposed D-02 text (replacing the second and third sentences):**

> *Stringency follows reversibility, judged by what a gate commits, not by which phase owns it.*
> *(a) One-way programme gates (KDP-0B, and pathfinder PDR where pathfinder cost exceeds 25 % of the 0A budget): TRL 6 in a relevant environment for project-ending technologies, no waivers.*
> *(b) Two-way programme milestones (MTR and other tranche releases): TRL 4–5 for the technologies the tranche funds; an unmet criterion withholds that tranche's planned demonstration.*
> *(c) 0A flight projects, at project PDR: enabling technologies at TRL 6; technologies under test at TRL 5 with a documented relevant-environment definition. Before CDR: technologies under test pass ground tests of the failure modes that would leave the flight without minimum data return. At launch readiness: flight system qualified and accepted. Each project declares its enabling / under-test classification at SRR. For scouts only, enabling-technology criteria may be waived by owner-signed Class D risk acceptance.*

**Y-statement.** In the context of Phase 0A, which funds both reversible tranches and irreversible flight projects, and facing a panel split over whether D-02's TRL 4–5 applies to scout and pathfinder gates, we chose to classify gates by what they commit and technologies by their role in the flight. The result is TRL 6 at PDR for enabling technologies, TRL 5 plus targeted ground tests for technologies under test, and TRL 4–5 for MTR tranche releases. We did this to achieve design commitments that do not repeat the documented post-PDR cost-growth pattern, while keeping 0A's learning tempo. We accept a classification judgment at SRR that can be gamed, a modest extra ground-test bill, and an amendment to an already-accepted decision.

**Toulmin.**

| Element | Content |
|---|---|
| Claim | O4 as worded above |
| Grounds | NASA and DoD TRL 6 practice at design commitment (high certainty). GAO cost-growth findings (moderate). TRL definitions that place flight demonstration at TRL 7 (high). |
| Warrant | D-02's own principle. Irreversibility is a property of the commitment, so the same principle that puts TRL 6 at KDP-0B puts it at any gate committing comparably irreversible resources. Gate stringency should also stop short of requiring the evidence a gate exists to produce. |
| Backing | Mankins' TRL and AD² work; ECSS-E-HB-11A |
| Qualifier | *Probably right* for the pathfinder (medium confidence). *Plausibly right* for small scouts, where outcome evidence is indirect (low–medium confidence). |
| Rebuttal | If A1 fails (cheap, rapid reflight), scout launches become near two-way and clause (c) should relax to TRL 5 at PDR for scouts. |

**Evidence that would change the ruling:**

1. **Towards relaxing the scout rule.** Launch contracts with refundable or rebookable slots, a scout unit cost below a small fraction of 0A, and demonstrated build-and-reflight within about 9 months.
2. **Towards O2 (TRL 6 at PDR for everything).** The owner sets w₁ at about 0.5 or higher (trade-off T1). Or the pathfinder becomes the sole carrier of a 0B project-ending technology with no ground-test substitute, so that its loss blocks KDP-0B.
3. **Towards adding AD² as a hard gate.** A TRL re-assessment showing assessor disagreement of more than one level on any enabling technology.

## 9. Consequences

**Enables:**

- **§5 MTR criteria reconcile.** Gemini's and GPT's TRL 4 scope stands as the tranche criterion. Claude's "TRL 5 for pathfinder payload at MTR" becomes the PDR criterion for technologies under test, applying at MTR only if pathfinder PDR precedes or coincides with it (A4). GPT's "an unmet item cannot receive its planned demonstration" is adopted verbatim into clause (b).
- **`gates-proposal.yaml`.** A `flight_project_gates` block per scout and pathfinder, with `enabling[]` and `under_test[]` technology lists keyed to `trl-baseline.yaml` IDs.
- **D-05 (propellant).** Becomes a classification input. If the pathfinder's propulsion is enabling, D-05 must close before pathfinder PDR so that TRL 6 can be shown.

**Constrains:**

- **Owner decisions.** The owner must set the pathfinder cost-share threshold (proposed 25 %) and each project's minimum-data-return floor. These are values, not engineering facts.
- **Metallurgy down-select.** Routes T06, T17, T07 and T23 remain under the two-way MTR rule (TRL 4 for funded routes). Any route flown on the pathfinder becomes a technology under test, at TRL 5 by pathfinder PDR. This pressures an earlier down-select to at most two routes, in line with Claude's position.
- **KDP-0B.** No change. The no-waiver TRL 6 requirement for project-ending technologies stands. Clause (a) only extends it to a programme-scale pathfinder.

**Kept, not averaged.** Claude's stricter reading (O2) remains the right answer if the owner's values sit at the loss-averse end of T1. GPT's "TRL 8 before launch" is retained in substance as "qualified and accepted" for the flight system, and rejected for technologies under test.