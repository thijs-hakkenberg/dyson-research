---
questionId: "rq-0-71"
questionSlug: "trl6-scale-extrapolation-rule"
modelId: "claude-opus-5-5"
modelName: "Claude Opus 5.5"
roundNumber: 1
generated: "2026-10-17"
type: "discussion-response"
---

# TRL 6 Scale-Extrapolation Rule: Fixed Limit or Case-by-Case

**Position in brief.** Neither panel position should be adopted as it stands.

- **Claude's** fixed 10× limit is a good *default*, but a poor *test of truth*.
- **GPT's** "no fixed factor" is physically correct but cannot be audited at a one-way gate.

I recommend a **pre-registered, axis-specific, rebuttable presumption with a hard backstop**:

- **Default:** ≤10× single-unit extrapolation in throughput or power.
- **10–100×:** allowed only with a regime-preservation case that is pre-registered and independently reviewed, plus an intermediate anchor test.
- **Above 100×:** never counts as TRL 6 for a single unit.
- **Modular systems:** numbering-up is assessed separately, through interaction tests.
- **Duration:** has its own rule, based on a validated degradation model.

The decisive feature is **pre-registration**. Each technology's allowed factor and governing regimes are fixed at the 0A mid-term review, *before* the pathfinder data exist. This answers GPT's objection (one number cannot fit all physics) and Claude's implicit concern (case-by-case arguments made after the data arrive drift toward a pass).

---

## 1. Frame & decision type

- **Decision type.** This is a *property* decision in Kruchten's ontology: it sets an attribute of the KDP-0B gate criterion defined under D-02. It is not an executive decision about any single technology. It enables a later executive decision: how large each pathfinder must be.
- **Reversibility.** The rule itself can be changed until the pathfinders are specified (around the 0A mid-term review). After that it becomes effectively irreversible. Pathfinder hardware is sized to the rule, and changing the rule afterwards either strands that hardware or invites accusations of moving the goalposts.
- **What the rule governs.** It governs KDP-0B, which is a one-way door. Under D-02, stringency follows reversibility, so the rule should lean towards protecting against a false pass.
- **Cynefin domain.** Complicated, not complex. Whether a 1 kW plasma torch says anything about a 1 MW one is knowable with expert analysis: dimensionless groups, mechanism maps, and physics-of-failure. That favours analysable rules over pure judgement. The analysis, however, differs by technology, so it should not be collapsed into a single number.
- **Decision rights.** The owner decides. The panel is advisory. Gemini did not address this question, and its silence is recorded as non-agreement.

**The real question** is not "10× or nothing". It is: *what evidence standard makes a sub-scale demonstration count as a "representative model" at a gate that cannot be reversed, and who fixes that standard, and when?*

## 2. Criteria and weights

These are stated before the options. I use swing weights: each weight reflects how much it matters to move from the worst plausible option on that criterion to the best.

| # | Criterion | Swing range across plausible options | Weight | Why this weight |
|---|---|---|---|---|
| C1 | **One-way-gate protection.** Probability that a technology passes KDP-0B but fails at full scale or full life. | From "any argued extrapolation passes" to "only near-full-scale evidence passes". A false pass commits Phase 1 capital to a project-ending failure. | **0.30** | Largest consequence swing. This is what D-02 exists to protect. |
| C2 | **Discrimination and technology fit.** Avoids false fails. Recognises regime-preserving or modular systems that can legitimately be extrapolated far. | From "rejects modular MW arrays tested at 50 kW" to "accepts them on physics". | **0.20** | A false fail sends the programme to the "0A only, Earth supply" fallback without need, or forces a needlessly large pathfinder. Recoverable, but expensive. |
| C3 | **Auditability and resistance to motivated reasoning.** Can an independent reviewer check compliance? Is the standard fixed before results arrive? | From a bright line that is fully checkable to "persuade the board". | **0.20** | One-way gates fail through advocacy as often as through physics. Wide swing. |
| C4 | **Pathfinder cost and schedule.** | From test facilities that already exist to purpose-built facilities costing 10–30× more. | **0.15** | Real, but partly double-counted with C2. D-01 already accepts that Phase 0 is a capability programme, not a cost saving. |
| C5 | **Adaptability.** Can the rule absorb new evidence or technologies without being rewritten? | Moderate swing. | **0.10** | Phase 0 will discover technologies and failure modes that are not yet on the list. |
| C6 | **Governance burden.** Review effort and time to administer. | Small swing. Every option needs some review. | **0.05** | Low, because review cost is small compared with pathfinder cost. |

**Must criteria** (Kepner-Tregoe screening, applied before scoring):

- **M1.** Consistent with D-02: no waivers at KDP-0B for project-ending technologies.
- **M2.** Duration and wear are explicitly covered.

## 3. Options

| ID | Option | Origin |
|---|---|---|
| **O0** | **Null.** Leave the split. Each KDP-0B review argues extrapolation adequacy on the day. | Status quo |
| **O1** | **Hard fixed cap.** ≤10× on every axis, no exceptions. | Strict reading of Claude |
| **O2** | **No fixed factor.** Extrapolation justified only by test-validated models, decided per case at the gate. | GPT |
| **O3** | **10× unless regimes are preserved.** The escape clause is argued at the gate. | Claude as written |
| **O4** | **Pre-registered, axis-specific, rebuttable presumption with a hard backstop.** Described in §8. | Recommended synthesis |
| **O5** | **Fully bespoke, pre-registered factor per technology.** No default and no backstop. | Variant of GPT with pre-commitment |

**Rejected options, with arguments:**

- **O0 (null) is rejected.**
  - It postpones the decision until after pathfinders are sized, which is exactly when the decision stops being reversible.
  - Every pathfinder team would size to the most permissive reading.
  - The standard would be set at the gate, by the people whose programme depends on passing.
  - It also fails M1 in spirit: argument at the gate is a waiver by another name.
- **O1 (hard cap) is rejected.**
  - It treats numbering-up of identical modules (solar collector panels, power-beaming emitter tiles, mass-driver coil stages) like scale-up of a single reactor. Thin-film collector arrays scale by replication. A 10× cap on total array power would demand absurd pathfinders while adding little evidence.
  - Conversely, 10× is not conservative when a regime transition occurs inside the factor. Examples: laminar to turbulent melt flow, onset of electromagnetic skin-depth limits, thermal runaway once the ratio of radiative area to volume falls. A hard cap gives false comfort there.
- **O2 (no fixed factor) is rejected as written.**
  - The physics is right, but the governance fails. "Justified by test-validated models" leaves undefined who sets the validation standard, and when.
  - Assessed at the gate, it scores worst on C3.
  - It provides no basis for sizing pathfinders at 0A, which is the decision this rule exists to feed.
- **O3 is rejected, narrowly.**
  - It is close to the right answer, but the escape clause is argued at the gate, after the data exist. That re-imports O2's weakness.
  - It has no ceiling, so "regimes preserved" can be argued for 1000×.
  - It does not distinguish numbering-up from scale-up.
- **O5 is rejected, narrowly.**
  - Pre-registration fixes most of O2's problems.
  - But without a default it has no anchor. Every factor is negotiated from zero, which raises governance burden and invites optimistic factors.
  - Without a backstop it has no guard against model hubris.

## 4. Assessment matrix (QOC)

Scores run from 1 (poor) to 5 (best). The weighted total is the sum of each score times its criterion weight.

| Option | C1 Gate protection (0.30) | C2 Fit (0.20) | C3 Audit (0.20) | C4 Cost (0.15) | C5 Adapt (0.10) | C6 Burden (0.05) | **Weighted** | Musts |
|---|---|---|---|---|---|---|---|---|
| O0 Null | 1 | 3 | 1 | 4 | 3 | 2 | **2.05** | M1 fails in spirit |
| O1 Hard 10× | 3 | 1 | 5 | 1 | 1 | 5 | **2.65** | Pass |
| O2 No factor | 2 | 5 | 2 | 4 | 5 | 2 | **3.20** | M2 pass; M1 weak |
| O3 10× unless | 3 | 4 | 3 | 3 | 4 | 3 | **3.30** | Pass |
| O4 Recommended | 4 | 4 | 4 | 3 | 4 | 3 | **3.75** | Pass |
| O5 Bespoke, pre-registered | 3 | 5 | 3 | 4 | 4 | 2 | **3.60** | Pass |

**Robustness.** O4 leads under every reweighting I tried, except one. If C4 (cost) is raised above roughly 0.30 at the expense of C1, O5 overtakes it. That reweighting amounts to valuing cheap pathfinders over one-way-gate protection, which contradicts D-02. O1 never wins unless C3 alone is weighted above about 0.45.

## 5. Sensitivity vs trade-off points

**Sensitivity points.** These are facts or parameters that strongly move one attribute.

- **S1. The default factor (10× versus 30×)** drives pathfinder cost (C4) almost alone. Gate protection is far less sensitive to it, because the regime case does the real work in the 10–100× band. That is why I am comfortable with 10× as a default and not as a limit.
- **S2. The backstop (100× versus 1000×)** drives gate protection (C1) for single-unit technologies. The obvious candidates are ISRU regolith processing at kt/yr and MW-class single-aperture power conversion. Tens of t/yr pilot-scale ISRU is plausible in Phase 0. That is already near 100× short of kt/yr, so the backstop decides whether ISRU can pass KDP-0B on a ground pilot at all.
- **S3. Where the numbering-up boundary is drawn** (what counts as the "smallest replicated unit") drives C2 for modular technologies. A generous unit definition lets single-unit scale-up masquerade as replication. The rule must therefore define the unit by its governing physics, not by its packaging.

**Trade-off points.** These are values questions for the owner, not facts to be settled.

- **T1. False pass versus false fail at KDP-0B.** Every tightening of the band edges or backstop buys C1 and costs C2 and C4. D-02 has already leaned this towards protection. What it has *not* said is how much pathfinder money that protection is worth. My recommendation assumes the owner prefers a one-to-two-year slip and a larger pathfinder over a material chance of committing 0B on a mis-scaled technology. The owner should confirm or reject that.
- **T2. Auditability versus physical fidelity.** A bright line is easy to audit but physically naive. A regime argument is faithful but hard to audit. O4 splits the difference with pre-registration. Someone who distrusts all expert review would prefer O1; someone who distrusts all fixed rules would prefer O5. Which way to lean is a values question.
- **T3. Schedule versus life evidence.** Longer duration tests delay KDP-0B. Accelerated tests save time but need a validated acceleration model. How much modelling risk to accept in exchange for time is a values question.

## 6. Evidence certainty

The certainty ratings below are GRADE-style, describing evidence quality. Likelihood terms follow IPCC conventions and describe how probable the claim is, which is a separate judgement.

| Claim | Certainty of evidence | Likelihood | Notes |
|---|---|---|---|
| Scale-up failures cluster where governing regimes change: new dominant mechanism, dimensionless group crossing a threshold. | **Moderate** | Very likely | Standard in chemical-engineering scale-up practice. Consistent with RAND's pioneer process plant studies (Merrow et al., early 1980s), which tied performance shortfalls to poor process understanding and new technology. The evidence comes from terrestrial process plants, not space hardware, so it is indirect. |
| ~10× per scale-up step is a common practitioner heuristic for single-unit novel processes. | **Low** | Likely | Folklore-grade, not codified. Practice varies widely (10–100× per step, depending on how mature the process models are). Use it as a default anchor, not a law. |
| No fixed scale factor appears in the standard TRL definitions. | **High** | Virtually certain | ISO 16290 / ECSS and NASA NPR 7123.1 define TRL 6 as a representative model or prototype in a relevant environment, without numerical scale limits. GPT is correct on this. A Project Dyson factor would therefore be a programme-specific supplement, which is permissible. |
| Numbering-up of identical modules carries less scale risk than unit scale-up, but adds interaction risk (thermal coupling, EMI, control, fault propagation). | **Moderate** | Likely | Well established in power electronics and phased-array practice. Interaction effects are often under-tested. |
| Accelerated life tests are valid only if the failure mechanism is unchanged across stress levels. | **High** | Virtually certain | A core tenet of physics-of-failure reliability. |
| Long-duration life tests tend to reveal failure modes absent from early hours. | **Moderate** | Very likely | Electric-propulsion life-test history (for example the NSTAR and NEXT long-duration tests) shows erosion and wear findings that emerged only with accumulated hours. |
| Pre-registering criteria before data reduces motivated pass decisions. | **Moderate** | Likely | Strong evidence in clinical trials. Transfer to engineering gate reviews is plausible but not directly measured. |

**Overall.** I hold moderate confidence in the *structure* of O4 and low confidence in the *specific numbers* (10× and 100×). The numbers are deliberately exposed as sensitivity points S1 and S2.

## 7. Key assumptions

| # | Assumption | What would falsify it |
|---|---|---|
| A1 | Governing regimes for each project-ending technology can be identified in advance by mechanism mapping and dimensionless analysis. | A Phase 0 pathfinder shows a dominant failure mechanism that was absent from its pre-registered regime list. Two or more such surprises across technologies would mean pre-registration is not capturing reality. I would then tighten towards O1 for single units. |
| A2 | Most MW-class Project Dyson power systems are modular and can be legitimately numbered up. | Design studies show that critical power conversion or beaming needs monolithic single apertures or single units at MW scale. S2 then dominates, and the cost case shifts. |
| A3 | Independent review at the 0A mid-term review is genuinely independent of the pathfinder teams. | Reviewers are drawn from teams whose funding depends on the outcome. If that is true, O4 degrades to O3, and a stricter fixed cap becomes preferable. |
| A4 | Validated degradation models with mechanism-invariant acceleration can be built for the dominant wear modes within Phase 0 timescales. | Mechanism change is observed between stress levels, or acceleration factors are not reproducible. Duration evidence must then come from real-time testing, and KDP-0B moves later. |
| A5 | The owner's values match D-02's lean towards protection (T1). | The owner states that schedule or cost dominates. O5 then becomes preferable. |

**ACH on the competing hypotheses about what makes extrapolation fail.** Each hypothesis is tested against the evidence in §6.

- **H1: "Scale factor magnitude is the main predictor."** Contradicted by modular systems that scale far without trouble, and by regime transitions that occur within small factors. This is the **most disconfirmed** of the three.
- **H2: "Regime change is the main predictor."** Consistent with the process-plant and life-test evidence. This is the **least disconfirmed** on the physics.
- **H3: "Review discipline is the main predictor"** (that is, gate failures are advocacy failures). This is also **weakly disconfirmed**. It is consistent with megaproject literature, with clinical pre-registration findings, and with the history of space programme gate failures driven by schedule pressure.

**Ranking:** H2 ≈ H3 > H1. O4 is the only option designed around *both* surviving hypotheses: regime analysis addresses H2, and pre-registration addresses H3. The factor magnitude is kept only as a default and backstop, which fits H1's weak standing.

## 8. Decision, warrant, accepted downside

### Recommended gate rule text (for `gates-proposal.yaml`, KDP-0B, technology criterion)

> **TR-6-SCALE. Representative-model scaling for TRL 6 at KDP-0B (project-ending technologies).**
>
> **(a) Pre-registration.** At the 0A mid-term review, each project-ending technology shall pre-register a Scaling Basis. It shall contain:
> 1. the **smallest replicated unit (SRU)**, defined by governing physics;
> 2. the governing regimes and dimensionless groups for throughput, power density and thermal and structural load;
> 3. the planned test scale and the full-scale target on each axis;
> 4. the dominant wear mechanisms and the planned degradation model.
>
> Once accepted by independent review, the Scaling Basis is frozen. Changes after test data exist require the change, and the reason for it, to be recorded, and they reset the evidence clock for the affected axis.
>
> **(b) Single-unit scale-up (throughput or power per SRU).**
> - **≤10×:** acceptable with a model correlated to test data.
> - **>10× to ≤100×:** acceptable only if all three hold:
>   - (i) the pre-registered regime case shows that every governing dimensionless group stays within its regime between test and full scale;
>   - (ii) at least one intermediate-scale anchor point (geometric mean of test and full scale, ±3×) confirms the model's predictions within pre-registered tolerances;
>   - (iii) the review is independent.
> - **>100×:** does not satisfy TRL 6 regardless of argument. No waiver applies (per D-02).
>
> **(c) Numbering-up (system scale from replicated SRUs).** There is no fixed limit on replication count, provided all three hold:
> - (i) each SRU meets (b);
> - (ii) an interaction test of at least the larger of 4 units or a representative cell is passed in the relevant environment. The cell must include interior and edge or boundary units, shared thermal, power and control paths, and injected single-unit faults;
> - (iii) a validated model shows that coupling effects (thermal, electromagnetic, control-loop, fault propagation) do not grow beyond pre-registered bounds at full count.
>
> **(d) Duration and wear.** Life may be shown by partial test plus a degradation model, provided all four hold:
> - (i) real-time test time is at least the larger of 10% of design life or the time for the dominant mechanism to reach at least 25% of its failure criterion;
> - (ii) any acceleration is calibrated at at least 3 stress levels, with demonstrated mechanism invariance (same failure mode, same signature);
> - (iii) demonstrated equivalent life, real plus accelerated, is at least 1.5× design life;
> - (iv) time extrapolation beyond the demonstrated equivalent life is not credited.
>
> **(e) Axes are independent.** Each axis (throughput, power, duration) must pass on its own; there is no averaging across axes. Combined-environment effects (for example thermal cycling with vacuum and irradiation) must be present in at least one test article.

### Y-statement

> In the context of a one-way KDP-0B gate requiring TRL 6 for project-ending technologies with no waivers, **facing** MW-class and kt/yr targets that no test facility reaches and a panel split between a fixed 10× cap and no fixed factor, **we chose** a pre-registered, axis-specific rebuttable presumption (≤10× default, 10–100× with regime case and anchor test, >100× never, numbering-up assessed through interaction tests, duration through a mechanism-invariant degradation model with 1.5× equivalent-life margin), **to achieve** auditable gate protection that respects technology-specific physics and lets pathfinders be sized at 0A, **accepting** larger and costlier pathfinders for single-unit technologies (ISRU processing especially), more review effort at the 0A mid-term review, and the possibility that a sound technology fails KDP-0B solely on the 100× backstop.

### Toulmin structure

- **Claim:** adopt TR-6-SCALE.
- **Grounds:**
  - Scale-up failures are driven by regime change.
  - Gate failures are often driven by advocacy.
  - Standard TRL definitions give no number, so the programme must set one.
- **Warrant:** at an irreversible gate, the evidence standard should be (a) tied to the physics that causes failure and (b) fixed before the evidence exists. A default number is useful only as a burden-shifting anchor, and a backstop is needed because models validated over two orders of magnitude rarely hold over three for novel hardware.
- **Backing:**
  - process-plant scale-up experience;
  - physics-of-failure reliability practice;
  - electric-propulsion life-test history;
  - pre-registration practice from clinical trials;
  - D-02's reversibility principle.
- **Qualifier:** probably the right structure (moderate confidence). The specific numbers 10×, 100×, 10% and 1.5× are low-confidence defaults that the owner should treat as tunable until the Scaling Bases are frozen.
- **Rebuttal conditions:** the ruling should change if the evidence in §9 materialises.

### Accepted downside, stated plainly

- ISRU at tens of t/yr on the ground cannot pass KDP-0B against a kt/yr target without either an approximately 100 t/yr anchor or a modular SRU argument.
- Such an anchor adds cost and possibly a year or more to 0A. That is the intended effect. If it is unaffordable, the pre-committed fallback "0A only, Earth supply" applies, and that is an acceptable outcome under D-01.

## 9. Consequences

**Enables:**

- **Pathfinder sizing at the 0A mid-term review.** For each technology, the Scaling Basis yields a minimum test scale (full scale ÷ 100 as an absolute floor; full scale ÷ 10 if no regime case is attempted). This converts an argument into a budget line.
- **Programme architecture pressure towards modular SRUs.** The rule rewards architectures whose scale comes from replication. This is a design signal to Phase 1 concept teams, and probably a healthy one for collector, beaming and mass-driver elements.
- **A clean failure trigger.** A technology exceeding 100× single-unit scale-up with no affordable anchor test is a pre-committed KDP-0B fail, which routes to the fallback without debate.

**Constrains:**

- **The "relevant environment" definition** (another of the eleven owner choices). Clause (e) needs that definition to specify which combined environments are mandatory.
- **The project-ending technology list.** Classification now carries cost consequences, so there will be pressure to declassify technologies. The list should be frozen alongside the Scaling Bases.
- **The 0A mid-term review agenda.** It must include an independent Scaling Basis review, staffed by people outside the pathfinder teams (assumption A3).

**Evidence that would change the ruling:**

1. **Two or more pre-registered regime cases fail** during 0A, through unforeseen mechanisms. Move towards O1: hard 10× for single units, no 10–100× band.
2. **Anchor tests repeatedly confirm models across about 100×** with tight tolerances, in two or more technologies. Raise the default to around 30× and consider a 300× backstop.
3. **Accelerated-test mechanism invariance cannot be shown** for dominant wear modes. Drop accelerated credit, require real-time testing at 25% of design life or more, and accept a later KDP-0B.
4. **The owner states that schedule or cost outweighs gate protection** (a reversal of T1). Adopt O5: bespoke pre-registered factors, no backstop.
5. **Review independence cannot be staffed.** Adopt O1, because a bright line is the only defence that does not depend on reviewers.

**Note for later rounds.** I expect GPT's objection to be that the 100× backstop is exactly the "fixed acceptable scale factor assumed in advance" it rejected. I accept that it is. My defence is that, at a no-waiver one-way gate, *some* number must exist that argument cannot cross, and refusing to state it only moves it into the reviewers' heads. That disagreement should be kept for the owner, not averaged away.