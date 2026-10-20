---
questionId: "rq-0-72"
questionSlug: "composite-technology-trl-rule"
modelId: "claude-opus-5-5"
modelName: "Claude Opus 5.5"
roundNumber: 1
generated: "2026-10-17"
type: "discussion-response"
---

# Composite TRL: Cap by the Weakest Critical Part, or Assess the Integration?

**Recommendation:** use both, with different jobs. The weakest critical sub-rating sets a ceiling. A judged integration assessment sets the headline at or below that ceiling, never above it. A TRL 4 ceiling applies until an integrated article exists.

## 1. Frame & decision type

- **What kind of decision it is.** This is a *property* decision (Kruchten). It sets a rule that governs how every composite in `trl-baseline.yaml` gets its headline rating. It is not a rating of any one technology.
- **Reversibility.** The rule itself can be changed: we can re-publish ratings. What it feeds cannot. KDP-0B is a one-way gate, and under D-02 project-ending technologies there need TRL 6 in a relevant environment with no waiver.
- **Where the rigour belongs.** The one-way exposure lives in the headline that KDP-0B reads. That headline should get the most rigour, consistent with D-02's principle that stringency follows reversibility.
- **Cynefin domain.** This is *complicated*, not complex. Integration risk in propulsion clusters, power chains and processing chains is analysable by experts with stated criteria. That points to a rule plus bounded judgment, rather than either pure mechanism or pure discretion.
- **The real dispute is narrower than it looks.** Claude says "cap at the weakest". GPT says "don't automatically take the weakest; assess the integration; an unvalidated critical function still blocks". Both agree a weak critical part blocks the claim. They differ on one point: is the minimum the *estimate*, or only a *bound*? That is the decision to make.

## 2. Criteria and weights

Swing weights are set against the realistic range of each criterion across the options below. A criterion where all options score about the same gets little weight, however important it sounds.

| # | Criterion | Swing weight | Why this weight fits the range |
|---|---|---|---|
| C1 | **Gate integrity.** No headline overstates readiness at a one-way gate. | 0.35 | Widest consequential range. Options run from "structurally impossible to overstate" to "overstatement depends on assessor discipline". A false TRL 6 at KDP-0B commits irreversible 0B funding. |
| C2 | **Integration-risk fidelity.** The headline drops when mature parts are combined in an unproven way. | 0.20 | Wide range. Pure-minimum rules score zero here: twelve heritage thrusters in a novel cluster would read as heritage. Integration-aware rules catch it. |
| C3 | **Auditability and reproducibility.** Two assessors reach the same headline from the same evidence. | 0.20 | Wide range. Mechanical rules score near-perfect; free judgment scores poorly. Matters because the panel has three models and an owner who must be able to check them. |
| C4 | **Information content of what is published.** A reader can see *why* the headline is what it is. | 0.10 | Moderate range. Mostly a function of reporting format, which can be bolted onto any option. |
| C5 | **Consistency with D-02 and the T26 ruling.** | 0.10 | Moderate range. Most options can be made consistent with "TRL 3 (4 conditional)". Pure averaging cannot. |
| C6 | **Assessment cost.** Analyst effort per composite. | 0.05 | Narrow range. Every option needs sub-ratings anyway; judgment adds a bounded integration review. |

**Musts (Kepner-Tregoe screen, applied before scoring):**

- No arithmetic on ordinal TRL values.
- An unvalidated critical function must block the system claim. All three panellists accept this.

## 3. Options

**O0. Null: leave the split.** Each assessor applies their own convention, and the owner rules case by case as in T26.
- *Rejected.* The same baseline would carry headlines built on incompatible rules. KDP-0B would then compare propulsion and power ratings that mean different things.
- T26 already shows the cost: the owner had to rule a specific headline because no general rule existed. That will recur for every composite.

**O1. Pure minimum.** Headline = lowest critical sub-rating.
- *Rejected as the full rule.* It treats a bound as an estimate. Combining TRL 7 thrusters, a TRL 7 PPU and a TRL 7 feed system into an untested cluster with shared plume, thermal and EMI interactions would produce TRL 7.
- That violates the TRL definitions themselves. From TRL 5 upward they speak of breadboards, subsystem models or prototypes *in a relevant environment*, that is, integrated configurations (NASA NPR 7123.1 TRL table; ISO 16290:2013).

**O2. Pure integration judgment** (GPT's position read literally). Assess the integrated configuration and set the headline on that evidence.
- *Rejected as the full rule.* Without a stated cap, "assess the integration" can be read upward: "the system test went well, so the system is TRL 5 even though the cathode is TRL 3".
- GPT's own caveat ("an unvalidated critical function still blocks") is an informal cap. Making it explicit costs nothing and removes the ambiguity.

**O3. Bounded integration assessment (recommended).** Three parts:
- (a) The headline may not exceed the lowest *critical* sub-rating.
- (b) It may not exceed TRL 4 unless an integrated article of the rated configuration has been tested.
- (c) Within those bounds, a judged integration assessment against stated criteria sets the headline. That judgment can only hold the headline at the cap or lower it.

**O4. Arithmetic aggregation.** Averages, products, or SRL-style TRL × IRL matrices (Sauser et al., 2006).
- *Rejected at the screen.* TRL is ordinal. Averaging it is meaningless, and the SRL matrix arithmetic has been specifically criticised on those grounds (Kujawski, IEEE Trans. SMC, 2013).
- It also lets mature parts mask an immature critical one, which fails the second must.

**O5. Mechanical minimum plus ceiling, no judgment** (Claude's rq-0-64 proposal in full). Same as O3's bounds (a) and (b), but no downward integration judgment above TRL 4.
- *Rejected, narrowly.* Once an integrated article exists, O5 again falls back to pure minimum. It misses integration shortfalls in, for example, a tested cluster run only at reduced thrust or in a non-representative thermal environment.

## 4. Assessment matrix

Scores run 1–5, higher is better. Weighted totals use the swing weights above.

| Option | C1 Gate integrity (0.35) | C2 Integration fidelity (0.20) | C3 Auditability (0.20) | C4 Information (0.10) | C5 Consistency (0.10) | C6 Cost (0.05) | **Weighted** |
|---|---|---|---|---|---|---|---|
| O0 Null split | 2 | 3 | 1 | 2 | 2 | 4 | **2.05** |
| O1 Pure minimum | 4 | 1 | 5 | 2 | 4 | 5 | **3.45** |
| O2 Pure integration judgment | 3 | 5 | 2 | 4 | 3 | 3 | **3.30** |
| **O3 Bounded integration** | **5** | **5** | **4** | **5** | **5** | **3** | **4.70** |
| O4 Arithmetic | — fails must | — | — | — | — | — | screened out |
| O5 Min + ceiling, mechanical | 5 | 3 | 5 | 3 | 5 | 5 | **4.35** |

**Reading the matrix:**
- O3 beats O5 on C2 and C4. It loses on C3 and C6. The margin (0.35) is real but not large. O5 is the honest runner-up.
- O1 scores only 4 on C1 because, without the ceiling, a minimum over heritage parts can overstate an unintegrated system.

## 5. Sensitivity vs trade-off points

### Sensitivity points

These are decisions that strongly move one attribute. They are facts or definitions to settle.

- **S1. What counts as "critical".** This drives C1. If "critical" is drawn too narrowly, the cap becomes cosmetic.
  - Proposed definition: a function whose failure defeats the system's claimed performance and has no qualified substitute in the *rated configuration*.
  - Redundancy only counts if the redundant path is itself rated.
- **S2. What counts as an "integrated article".** This drives the TRL 4 ceiling.
  - Proposed definition: hardware that implements every critical function in the rated architecture, with the interfaces that carry the coupled loads (thermal, electrical, plume and EMI, mass flow) present.
  - Form and fit need not be flight-like below TRL 6. Function and interfaces must be.
  - Simulations alone do not qualify.
- **S3. Configuration identity.** Ratings attach to a configuration ID. If the cluster size, topology or operating point changes, the integration assessment is void until re-justified.

### Trade-off points

These pull two attributes in opposite directions. They are values questions for the owner, not facts to settle.

- **T1. Auditability (C3) vs integration fidelity (C2).** Every degree of judgment added to catch integration risk costs reproducibility.
  - O3 resolves this by letting judgment act in *one direction only* (downward) and requiring stated criteria. The owner must still accept that two assessors may disagree by one level below the cap.
- **T2. False-negative vs false-positive cost.** O3 will sometimes under-rate a composite that is genuinely ready, for example a cluster whose integration is benign but untested. That delays a 0A milestone or a KDP-0B case.
  - D-02's asymmetry (one-way gates, no waivers) already chose to pay false-negative cost to avoid false positives at KDP-0B.
  - At two-way 0A milestones (TRL 4–5) the owner could reasonably accept more optimism. I recommend *not* forking the rule by gate. Instead, use D-02's existing lower thresholds at 0A, so one rating means one thing everywhere.

## 6. Evidence certainty

Likelihood (how probable the claim is) and confidence (how good the evidence is) are kept separate.

| Claim | Likelihood | Confidence / GRADE | Basis |
|---|---|---|---|
| Arithmetic on TRL is invalid. | Virtually certain | High | Measurement theory on ordinal scales; Kujawski (2013) critique of SRL. |
| TRL ≥ 5 definitions presuppose integrated configurations, so an unintegrated composite cannot honestly exceed about TRL 4. | Very likely | Moderate–high | NPR 7123.1 and ISO 16290 definitions. Some definitional latitude exists at the TRL 4/5 boundary. |
| Immature technology and integration problems are recurrent drivers of cost and schedule growth in NASA projects. | Likely | Moderate | GAO's recurring assessments of major NASA projects and the GAO TRA Guide (GAO-20-48G). Observational, not causal, and not specific to Dyson-class hardware. |
| The minimum cap never wrongly suppresses a system that is genuinely ready. | Very likely | Moderate | By argument, not data; see the warrant in §8. |
| Bounded judgment reproduces within ±1 level across assessors. | About as likely as not | Low | No calibration data yet for this panel. This is the weakest evidence in the chain. |

## 7. Key assumptions

**Competing hypotheses (ACH), ranked by least disconfirmed:**
- **H3. Bound and judgment are both needed.** Least disconfirmed. Neither class of failure below contradicts it.
- **H1. Minimum alone suffices.** Disconfirmed by every documented case of heritage parts failing as a new assembly: thermal coupling, plume interaction, shared-bus transients.
- **H2. Judgment alone suffices.** Disconfirmed by the general record of TRL inflation that motivated GAO's guidance. Also disconfirmed by GPT needing to add an informal cap.

**Assumptions and their falsifiers:**

- **A1. Any test that validates a critical part in the integrated system also re-rates that part.**
  - This answers GPT's "insufficiently justified" challenge. If a cathode has only ever been tested inside the cluster, the cluster test is the cathode's evidence. The cap therefore never binds wrongly; the sub-rating rises with it.
  - *Falsifier:* a credible case where system-level evidence demonstrates a function in a relevant environment, but that evidence cannot be attributed to the part.
  - If such cases occur, add a provision that integrated evidence may satisfy the sub-rating.
- **A2. Critical functions can be enumerated in advance for each composite.**
  - *Falsifier:* a 0A integration test reveals a critical function that was not on the list, such as an emergent thermal-management dependency.
  - Response: the criticality list becomes an output of each integration review, not only an input.
- **A3. One-direction judgment does not drift into routine downgrading that hides real readiness.**
  - *Falsifier:* more than a third of composites are held one or more levels below their cap with no named integration finding.
  - Response: if this happens, require a named finding for any downgrade (this is already in the rule text below) and audit.
- **A4. The T26 ruling (TRL 3, 4 conditional) is consistent with O3.**
  - I am assuming the owner's "3" reflects the lowest critical sub-rating or the absence of integration evidence, and that the "conditional 4" corresponds to a named condition.
  - *Falsifier:* the T26 record shows the owner rated it 3 while all critical sub-ratings were 4 or above and an integrated article existed. That would mean the owner applied something other than O3, and the rule would need reconciling.
  - I have not verified the T26 sub-rating detail, so this assumption is open.

## 8. Decision, warrant, accepted downside

### Proposed rule text for `gates-proposal.yaml` and `trl-baseline.yaml` conventions

**R1. Bound by weakest critical part.** A composite's headline TRL shall not exceed the lowest TRL among its critical functions.
- A function is critical if its failure defeats the system's claimed performance in the rated configuration and no rated substitute exists.

**R2. Integration ceiling.** A composite's headline TRL shall not exceed 4 unless an integrated article of the rated configuration has been tested.
- The article must implement all critical functions and the interfaces carrying coupled loads.
- The headline shall not exceed 5 unless that test was in a relevant environment, and shall not exceed 6 unless the article is a system or subsystem model or prototype in a relevant environment.

**R3. Integration assessment.** Within R1 and R2, the headline is set by a documented integration assessment against these criteria:
- interface coverage;
- operating envelope tested vs claimed;
- coupled-load fidelity;
- configuration match;
- anomaly closure.

The assessment may hold the headline at the cap or lower it. It may not raise it. Every level below the cap requires a named integration finding.

**R4. Evidence attribution.** Evidence from integrated testing that demonstrates a critical function updates that function's sub-rating. R1 is applied after that update.

**R5. No arithmetic.** TRL values shall not be averaged, weighted or multiplied.

**R6. Publication.** Every composite entry publishes:
- the headline;
- the cap and which bound set it (R1 function ID or R2);
- each critical sub-rating with its evidence pointer;
- the integration assessment result and any findings;
- the configuration ID;
- for conditional ratings, the condition that would raise the headline.

Non-critical sub-ratings below the headline are listed and flagged.

**R7. Gate criterion (KDP-0B).** A project-ending composite passes only if the headline is 6 or above under R1–R3, *and* every critical sub-rating is 6 or above, *and* the integrated article matches the configuration being committed. No waivers, per D-02.

### Y-statement

> In the context of a Phase 0 TRL baseline whose composite ratings feed a one-way KDP-0B gate with no waivers, facing a panel split between "cap at the weakest part" and "assess the integration", we chose a bounded integration assessment: the weakest critical sub-rating and a no-integrated-article ceiling set upper bounds, and a criteria-based integration judgment sets the headline at or below them. We did this to achieve headlines that cannot overstate readiness yet still fall when mature parts are combined in unproven ways. We accept extra assessor effort, about ±1 level of judgment variance below the cap, and occasional under-rating of benign integrations.

### Toulmin structure

- **Grounds.** The TRL definitions at 5 and above presuppose integrated configurations. Ordinal scales forbid arithmetic. D-02 already chose to pay false-negative cost at one-way gates.
- **Warrant.** The minimum is a valid *upper bound*, because a system cannot be more demonstrated than its least-demonstrated essential function. Under R4, any system evidence that would justify exceeding the bound also raises the bound.
  - It is not a valid *estimate*, because integration adds failure modes that no part rating captures.
  - So the bound must be mechanical and the estimate must be judged.
- **Qualifier.** Holds for composites whose critical functions can be enumerated and attributed. Confidence is moderate overall, and low on judgment reproducibility.
- **Rebuttal conditions.**
  - The A1 falsifier: evidence that cannot be attributed to parts.
  - Calibration showing assessors diverge by more than one level. In that case, fall back to O5.

### Where each panellist's position lands

- **Claude's position** survives as R1 and R2.
- **GPT's position** survives as R3, and its "critical function blocks" clause becomes explicit as R1. GPT's challenge, that the cap is insufficiently justified, is answered by R4 rather than dismissed.
- **Remaining disagreement.** If GPT holds that a system can exceed its weakest critical part *without* that part's sub-rating being updated, that disagreement remains. It should be recorded, not averaged away.

## 9. Consequences

**Enables:**
- Automated linting of `trl-baseline.yaml`: headline ≤ min(critical) and the R2 ceiling, checked by script.
- Comparable composite ratings at KDP-0B.
- A clean form for conditional ratings like T26's "4 conditional", where the condition is the named R1 or R2 bound to clear.

**Constrains:**
- Every composite now needs an enumerated critical-function list and a configuration ID before it can be rated.
- Propulsion clusters, power chains and processing chains are capped at 4 until 0A builds integrated articles. This pushes integrated-article hardware earlier in the 0A plan and should be budgeted as such.
- The 0A mid-term review becomes the natural point for first integration assessments.

**Follow-on decisions for the owner:**
1. Approve the S1 and S2 definitions.
2. Commission a small calibration exercise: three assessors independently rate three composites under R3 to measure variance.
3. Confirm that T26's sub-ratings and evidence fit R1–R2, or reconcile them.
4. Decide whether R3 downgrades need owner sign-off or only a documented finding.

**Evidence that would change the ruling:**
- **Toward O5 (drop judgment):** the calibration shows assessor variance above one level.
- **Toward O2 (relax the bound):** credible cases where integrated evidence cannot be attributed to a part, falsifying A1.
- **Toward re-defining "critical":** a 0A integration test surfaces an unlisted critical function.
- **Toward a gate-specific fork:** routine downgrading without findings (A3), or under-rating that measurably delays two-way 0A milestones with no safety benefit.