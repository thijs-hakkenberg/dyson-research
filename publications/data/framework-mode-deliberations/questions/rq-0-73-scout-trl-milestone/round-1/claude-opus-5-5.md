---
questionId: "rq-0-73"
questionSlug: "scout-trl-milestone"
modelId: "claude-opus-5-5"
modelName: "Claude Opus 5.5"
roundNumber: 1
generated: "2026-10-17"
type: "discussion-response"
---

# Scout and Sampling-Payload TRL Milestones: Ruling Proposal (Round 1)

## 1. Frame & decision type

**What is being decided.** This is a *property decision* in Kruchten's terms. It sets the readiness rule attached to the 0A scout flight project, which covers T11 (rendezvous scout spacecraft) and T18 (subsurface sampling and in-situ bulk grade assay). It also sets how that rule connects to the target gate and KDP-0B.

**The panel split is mostly about milestones, not levels.** The three positions sit at three different milestones:

| Panel member | Level | Milestone |
|---|---|---|
| Claude | TRL 6 | PDR |
| GPT | TRL 8 | each launch |
| Gemini | TRL 7 | target gate |

Laid on one timeline, they are close to a monotone ladder: 6 at PDR, 8 at launch, 7 at the target gate. They are not three competing thresholds. The real disagreements are two:

1. **Which TRL scale applies?** NASA's definition (NPR 7123.1) and ISO 16290 / ESA differ on TRL 7–8.
2. **Should a TRL label appear at the target gate at all?** That gate consumes *data*, not technology.

**Reversibility.**
- PDR is two-way. Under D-02, TRL 4–5 is the norm for internal 0A milestones, but PDR on flight hardware is the conventional TRL 6 point.
- Launch release is one-way *for that unit* but two-way *for the programme*, provided the fleet has more than one scout.
- The target gate feeds KDP-0B, which is one-way.

**Cynefin domain.**
- T11, the bus, is mostly *complicated*. Small-body rendezvous buses have flight heritage and the analysis is knowable.
- T18, sampling plus assay, is partly *complex*. Anchoring, penetration and assay behaviour in unknown low-gravity regolith cannot be fully reproduced on the ground.

That asymmetry should drive the rule.

## 2. Criteria and weights (swing weights, stated before options)

| # | Criterion | Swing weight | Why the weight fits the range |
|---|---|---|---|
| C1 | **Probability that scout #1 returns gate-grade sampled data** | 30 | Across the options the range is large, from about 0.3 (fly immature payload) to about 0.7 (qualified bus and payload). This is the evidence the target gate exists to consume. |
| C2 | **Time to target gate (cost of delay)** | 25 | Options range from adding nothing to adding 18–36 months (a precursor demo flight). KDP-0B and the D-01 real option both wait on this gate. |
| C3 | **Definitional coherence and auditability** | 15 | The range runs from "same words mean different things at different gates" to one declared scale with milestone-specific meaning. It matters because D-02 forbids waivers at KDP-0B, and an ambiguous criterion is a waiver in disguise. It ranks below C1 and C2 because it is cheap to fix once chosen. |
| C4 | **0A cost** | 15 | Options range from about +0 to about +$50–150M (a precursor mission). Under D-01, 0A is funded and 0B is sized at the gate, so 0A cost is real but not decisive. |
| C5 | **Consistency with D-02 (stringency follows reversibility)** | 15 | Options range from "TRL 8 on a two-way programme step" to "matched to door type". It is an accepted owner principle, so departures need a reason. |

Two criteria were considered and dropped:
- **Industrial base and supplier maturity.** It does not discriminate between the options.
- **Safety.** It is not relevant: no crew and no planetary-protection category concern for NEA sampling without return.

## 3. Options

**O0. Null: leave the split as is.** The three positions are recorded and the owner does not pick.
- *Argument for:* zero effort, and each reviewer can apply their own reading.
- *Argument against:* the scout PDR, launch review and target gate would each lack an agreed criterion. The panel already showed that "TRL 7–8 for scouts" was read three ways. A future gate review would then relitigate the scale, which is the kind of disguised waiver D-02 excludes.
- **Rejected.**

**O1. Claude's position: TRL 6 at PDR; 7–8 are mission outcomes only.**
- *For:* matches NASA practice (TRL 6 by PDR) and avoids an impossible pre-flight "operational environment" requirement.
- *Against:* it is silent on flight qualification at launch release. That leaves the riskiest commitment, spending a scout, without a stated entry criterion.

**O2. GPT's position: TRL 6 technology before KDP-0B; TRL 8 actual system before each launch.**
- *For:* TRL 8 in NASA's own wording ("actual system completed and flight qualified through test and demonstration") and in ISO 16290 ("accepted for flight") is reachable on the ground. It is ordinary flight-project discipline.
- *Against:* "TRL 6 before KDP-0B" for T18 is too weak if the scouts have flown, and moot if they have not. For a first-of-kind T18, strict NASA TRL 8 presupposes TRL 7, which needs the operational environment. That is the conflation Claude flagged.

**O3. Gemini's position: T11 and T18 at TRL 7 within the target-gate criterion.**
- *For:* it ties gate evidence to demonstrated in-space function.
- *Against:* it makes the gate's pass criterion a technology label when it should be a data-quality specification. A scout could "reach TRL 7" and still return non-decision-grade grade data, or the reverse.

**O4. Laddered composite (proposed).** One declared scale (ISO 16290 / ECSS-E-HB-11A, cross-walked to NASA), with milestone-specific criteria:
- TRL 5 at scout SRR, consistent with D-02 for two-way steps.
- TRL 6 at scout PDR for T11 and T18. For T18, the relevant environment is a defined ground and analogue test envelope.
- Flight-qualified, ISO TRL 8, at launch release. Qualification happens once, by protoflight or qualification model; later units need acceptance only.
- In-situ T18 performance (NASA TRL 7) is a recorded mission outcome. It is not an entry criterion.
- The target gate is keyed to a sampled-data specification, not to TRL.
- KDP-0B requires T18 at TRL 7 demonstrated in flight, because the technology is project-ending with no waiver, *or* the gate takes the pre-committed fallback "0A only, Earth supply".

**O5. Precursor pathfinder: TRL 7 flight demo of T18 before any scout launch.** Examples: a rideshare impactor-anchoring demo, or a lunar or Phobos-analogue test.
- *Against:* adds 18–36 months and an estimated $50–150M (judgement, not costed). The demo environment is still not the target's regolith, so it buys less TRL 7 than it appears to.
- **Rejected.** The scouts *are* the pathfinder.

**O6. GAO-style TRL 7 at CDR.**
- *Against:* for T18 this is infeasible pre-flight under the NASA definition. Under the ISO definition it collapses into O4.
- **Rejected.**

## 4. Assessment matrix (QOC; 1 = poor, 5 = best)

| Option | C1 data success (30) | C2 time (25) | C3 coherence (15) | C4 cost (15) | C5 D-02 fit (15) | Weighted |
|---|---|---|---|---|---|---|
| O0 Null | 2 | 3 | 1 | 4 | 2 | 2.40 |
| O1 Claude | 3 | 5 | 3 | 5 | 4 | **4.00** |
| O2 GPT | 4 | 4 | 2 | 3 | 3 | 3.40 |
| O3 Gemini | 3 | 3 | 2 | 4 | 3 | 3.00 |
| **O4 Ladder** | 4 | 4 | 5 | 4 | 5 | **4.30** |
| O5 Precursor | 5 | 1 | 4 | 1 | 2 | 2.80 |
| O6 TRL 7 at CDR | 4 | 2 | 2 | 2 | 2 | 2.70 |

How the key cells were scored:
- **C1 for O1 vs O4.** O4 adds an explicit qualification gate at launch release. Without one, environmental-test escapes (thermal-vacuum, vibration, sampler mechanism life) are the classic cause of small-spacecraft first-unit loss.
- **C2 for O2 vs O4.** O4 is about equal to O2 because qualification testing happens in either. The difference is that O4 does not demand "TRL 8" in a sense that implies a prior flight.
- **C3 for O2.** The low score comes from the scale ambiguity, not the content.

O1 and O4 are close. The margin is the launch-release criterion and the coherence gain. **This ranking is sensitive to C3's weight**: drop it to 5 and O1 and O4 roughly tie.

## 5. Sensitivity points vs trade-off points

**Sensitivity points** (facts that move the answer):
- **S1: which TRL scale is declared.**
  - Under ISO 16290, TRL 7 and 8 are ground-achievable. GPT's "TRL 8 before launch" is then just a flight-qualification requirement and is fully compatible with Claude.
  - Under strict NASA wording, TRL 7 needs the operational environment. "TRL 8 before launch" is then incoherent for first-of-kind T18. Declaring the scale dissolves most of the panel disagreement.
- **S2: scout fleet size.**
  - With two or more scouts on staggered launches, each launch is a two-way door at programme level, and qualify-once-then-accept is proportionate.
  - With a single scout, launch release becomes effectively one-way for the target gate. That would justify a stricter T18 ground campaign, closer to O5's rigour without the flight.
- **S3: fidelity of a low-gravity regolith analogue for T18.** Candidates are drop towers, parabolic flight, vacuum chambers with cohesive simulant, and reduced-gravity rigs. If credible analogues exist, TRL 6 at PDR is meaningful. If not, TRL 6 at PDR is a label on TRL 5 evidence.

**Trade-off points** (values, not facts):
- **T1: first-scout risk vs time to target gate.** O4 accepts roughly a 30–40% chance (my judgement, low confidence) that scout #1 fails to return decision-grade grade data. In exchange it avoids an 18–36-month precursor. This is an owner risk-appetite call, and D-01's "capability programme" framing points towards accepting it.
- **T2: label vs data at the target gate.** Keying the gate to data specification rather than TRL trades familiar vocabulary for discriminating power. I value discrimination. Someone who values a uniform TRL vocabulary across all gates would side with Gemini, and that is a legitimate values difference.

## 6. Evidence certainty

| Claim | Certainty (GRADE-style) | Likelihood / confidence |
|---|---|---|
| NASA practice expects TRL 6 for critical technologies by PDR (NPR 7123.1 / 7120.5 context) | High | — |
| ISO 16290 defines TRL 7–8 so they are achievable through ground qualification and flight acceptance | High | — |
| The NASA definition of TRL 7 requires demonstration in an operational environment | High | — |
| A small-body sampling interaction (anchoring, penetration, assay in low-g regolith) cannot be fully reproduced on the ground | Moderate. Hayabusa2 and OSIRIS-REx surface responses diverged notably from pre-flight regolith expectations. | Very likely; high confidence |
| T11 bus can reach TRL 6 by month 12–24 from TRL 3–4 | Low–moderate. Depends on heritage reuse, and the panel's baseline is TRL 2–4. | Likely (about 65%); medium confidence |
| T18 can reach TRL 6 by PDR in month 12–24 | Low. The panel baseline is TRL 2–4, and the assay part (bulk grade in situ) has thin precedent. | About as likely as not; low confidence |
| Probability that scout #1 returns decision-grade sample data under O4 | Very low (elicited judgement only) | 0.6–0.7; low confidence |

The weak link is the T18 maturation schedule. Every option inherits it.

## 7. Key assumptions, falsifiers, and competing hypotheses

**Assumptions and what would falsify them.**

| # | Assumption | What would falsify it |
|---|---|---|
| A1 | The fleet has at least two scouts with launch stagger of 6 months or more. | A budget or manifest decision fixing a single scout. Then move to the S2 single-scout variant: full qualification model plus an extended analogue test campaign before launch. |
| A2 | A credible ground and analogue relevant environment for T18 can be defined by about month 9. | A test-facility survey finding no reduced-gravity regolith rig with adequate duration and scale. Then TRL 6 at PDR for T18 is unattainable and PDR should be re-planned, not waived. |
| A3 | T11 can reuse heritage small-body bus elements: propulsion, GNC, relative navigation. | The AD² (Advancement Degree of Difficulty) rating stays at 6 after the 0A architecture study. That signals heavy new development, and the PDR window slips. |
| A4 | The target gate's information need can be written as a data specification (sample count, depth, assay accuracy, spatial coverage). | The economics gate (g-economics) cannot state a required grade uncertainty. Then the target gate is undefined regardless of TRL, which is a separate and bigger problem. |

**ACH on why the panel disagrees** (ranked by least disconfirmed):
1. **H1, milestone and vocabulary difference.** Least disconfirmed. The positions are consistent when mapped to a timeline, and GPT already separates "technology TRL 6" from "system TRL 8".
2. **H3, scale definition difference** (NASA vs ISO). Partly confirmed. Claude's "TRL 7–8 is a result of the mission" is true under NASA wording and false under ISO wording.
3. **H2, genuine risk-appetite difference.** Weakly supported. GPT's per-launch TRL 8 implies lower risk tolerance, but nothing in the record shows GPT would refuse a protoflight approach.

If H2 turns out to be true, T1 becomes a live owner choice rather than a drafting fix.

## 8. Decision, warrant, accepted downside

**Ruling: adopt O4, the laddered composite.**

**Rule text proposed for `gates-proposal.yaml`:**

> **R-SCOUT-TRL.** Scale: ISO 16290 / ECSS-E-HB-11A, with the NASA NPR 7123.1 crosswalk recorded in `trl-baseline.yaml`. Each relevant environment is defined per technology in a signed test-envelope document before the milestone that relies on it.
>
> 1. *Scout SRR (0A internal, two-way):* T11 and T18 at TRL 5 or above, with the T18 relevant-environment envelope defined.
> 2. *Scout PDR (month 12–24):* T11 and T18 at TRL 6 or above against that envelope. No waiver. If not met, PDR is replanned, and any slip beyond 6 months is reported to the 0A mid-term review.
> 3. *Launch release, scout n:*
>    - Scout 1: the flight system, including the sampling payload, is flight-qualified (ISO TRL 8: qualification or protoflight campaign complete, with no open qualification nonconformances against mission-critical functions).
>    - Scouts 2 and later: acceptance testing to the qualified design, plus closure of any anomaly from earlier scouts that affects sampling or assay.
> 4. *Target gate (g-target):* the pass criterion is the sampled-data specification. That means N samples or more at stated depth, bulk-grade assay uncertainty no worse than the value derived from g-economics, and stated spatial coverage. In-situ T18 operation is recorded as TRL 7 (NASA sense) when achieved. That record is a consequence, not a separate criterion.
> 5. *KDP-0B:* T18 is project-ending. KDP-0B requires T18 demonstrated in the operational environment (in-situ sampling and assay on at least one target), with no waiver. If no scout has done so by KDP-0B, the pre-committed fallback "0A only, Earth supply" applies, or KDP-0B is deferred under D-01's real-option terms. TRL 6 alone does not clear T18 at KDP-0B.

**Evidence that would change the ruling:**
- A single-scout manifest (A1 fails) moves the ruling towards a stricter pre-launch T18 campaign.
- No credible reduced-gravity regolith analogue (A2 fails) means PDR TRL 6 for T18 must be redefined or the schedule replanned. O5 could then become competitive if a cheap rideshare demo exists.
- If the owner states low risk appetite for scout #1 (T1), the ruling moves towards O5.
- If g-economics shows grade uncertainty barely matters, the target gate weakens and T18 might drop from project-ending to architecture-change.

**Y-statement.**
- *In the context of* the 0A scouts being the first flight hardware and the sole source of sampled-grade evidence for the target gate,
- *facing* a panel split that is mostly about milestones and TRL-scale wording, and a T18 whose decisive behaviour only space can reveal,
- *we chose* a declared ISO 16290 ladder: TRL 5 at SRR, TRL 6 at PDR, flight-qualified (TRL 8) at launch release, a data-specification target gate, and flight-demonstrated T18 at KDP-0B,
- *to achieve* stringency that tracks reversibility, a launch-release criterion that prevents avoidable losses, and a target gate that discriminates on what it actually needs,
- *accepting* that scout #1 may fail in situ (roughly 30–40%, low confidence), which would delay the target gate and possibly trigger the Earth-supply fallback.

**Warrant (Toulmin).** Gate criteria should test the decision the gate actually makes. PDR decides whether to commit to a design, so it needs technology maturity. Launch release decides whether to spend a unit, so it needs qualification. The target gate decides whether the asteroid is worth pursuing, so it needs data. KDP-0B is a one-way commitment, so it needs the project-ending technology proven where it must work.

**Backing:** NASA and ESA flight-project practice, D-02.

**Qualifier:** presumably right, if A1 and A2 hold.

**Rebuttal:** fails if the fleet is a single scout or if no T18 analogue exists.

## 9. Consequences

**Target-gate timing.**
- The gate cannot precede first successful sampling. A plausible chain is: PDR month 12–24, CDR about 6–9 months later, qualification and launch around month 30–42, cruise and proximity operations 6–24 months depending on target.
- That puts the earliest target gate at roughly month 36–66 (judgement, medium confidence on the range, low on the point value).
- KDP-0B sits behind it. This should be stated in `decisions.md` now, so that a later slip is not read as a failure.

**Decisions enabled:**
- The scout qualification strategy: protoflight vs dedicated qualification model, a cost trade that is now well-posed.
- A T18 test-facility budget line for months 0–12.
- Writing the g-target data specification jointly with g-economics.

**Decisions constrained:**
- The fleet size decision. Two or more scouts are now load-bearing for the ruling's proportionality.
- The launch stagger, which must leave time for anomaly closure between scouts 1 and 2.
- KDP-0B scheduling, which can no longer be calendar-fixed.

**Conflicts:**
- With any reading of D-02 that treats all of 0A as TRL 4–5. Launch release is explicitly carved out as qualification-gated.

**Disagreement kept.**
- Against Claude's prior position: TRL 7–8 is *not* wholly a mission result. ISO TRL 8, meaning flight qualification, is a legitimate pre-launch entry criterion.
- Against Gemini: TRL should not be the target-gate pass criterion.
- Against GPT: TRL 6 is insufficient for T18 at KDP-0B.

These are recorded as positions, not averaged.