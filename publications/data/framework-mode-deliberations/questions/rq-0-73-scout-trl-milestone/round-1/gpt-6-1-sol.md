---
questionId: "rq-0-73"
questionSlug: "scout-trl-milestone"
modelId: "gpt-6-1-sol"
modelName: "GPT-6.1 Sol"
roundNumber: 1
generated: "2026-10-17"
type: "discussion-response"
---

## 1. Frame & decision type

**Recommendation: adopt a three-milestone rule, rather than choose one TRL number for all purposes.**

- **Scout PDR:** TRL 6 for mission-critical novel technologies, including the sampling/assay chain.
- **Each scout launch release:** the actual integrated spacecraft and sampling payload completed and flight-qualified—**TRL 8** under the adopted definition.
- **Target gate:** successful, validated target-specific sampling and assay evidence. Neither launch readiness nor a TRL label substitutes for that evidence.

Retain D-02 separately: **every project-ending technology must reach TRL 6 in a relevant environment before KDP-0B, without waiver.**

This is a **property and executive decision**: it sets maturity requirements and authorises expenditure at successive milestones. The engineering is complicated; the asteroid interaction and representativeness of sampled grade retain substantial uncertainty.

The critical distinction is between:

1. technology maturity;
2. qualification of an actual flight article; and
3. adequacy of mission results for an investment decision.

The panel’s positions partly address different questions. They should not be averaged into a single intermediate TRL.

## 2. Criteria and weights

The following are **swing weights**, assigned before considering options. Scores assess improvement across the stated ranges, not abstract importance.

| Criterion | Range being valued | Weight | Why this weight fits the range |
|---|---|---:|---|
| **C1. Target-decision validity** | From accepting readiness as a proxy for grade to requiring validated, decision-relevant target evidence | **30%** | The scouts exist principally to resolve target uncertainty. Failure here can invalidate the entire resource case. |
| **C2. Flight-loss risk control** | From unspecified launch acceptance to explicit qualification of spacecraft, payload and interfaces | **25%** | Losing a scout destroys hardware and delays the evidence needed for subsequent decisions. |
| **C3. Proportionate cost and schedule** | From requiring a precursor flight merely to establish readiness to using justified ground qualification and existing evidence | **20%** | D-01 funds capability development, not unlimited qualification or an unnecessary extra mission generation. |
| **C4. Verifiability and accountability** | From inconsistent labels and milestones to auditable, configuration-specific acceptance evidence | **15%** | Ambiguity creates both accidental relaxation and unnecessary requalification. |
| **C5. Preservation of programme options** | From committing before uncertainty is resolved to preserving the gated 0B option and Earth-supply fallback | **10%** | Important, but substantially protected already by D-01 and D-02. |

**Non-compensable requirements:** compliance with D-02; applicable safety and licensing obligations; and no target-gate pass without adequate target evidence. A weighted score cannot override these.

## 3. Options

**A. Null: retain the split.**  
Argument for: avoids reopening agreement and lets project reviews resolve detail.  
**Reject:** leaves PDR, launch and target-gate requirements conflated. Different stakeholders could reasonably believe they approved different obligations.

**B. PDR-centred rule: TRL 6 at PDR; higher readiness emerges from the mission.**  
Argument for: correctly recognises that some operational evidence can only come from flight.  
**Reject as a complete rule:** TRL 6 does not itself establish that the actual spacecraft and payload are qualified for launch. Claude’s position can be sufficient only if separate flight-acceptance requirements are supplied.

**C. Target-centred rule: require T11 and T18 at TRL 7 at the target gate.**  
Argument for: demands demonstration in the operational environment.  
**Reject as a complete rule:** does not specify launch acceptance, and a successful demonstration may still produce insufficient or unrepresentative grade evidence. Gemini’s criterion is useful supporting evidence, not a sufficient target-gate condition.

**D. Layered rule: TRL 6 at PDR, actual system TRL 8 before each launch, validated results at the target gate.**  
Argument for: combines the useful elements of the positions without confusing their milestones.  
**Recommend**, subject to the qualification and evidence definitions below.

None of these rejections implies that the panel members intended to omit normal flight-project controls; the issue is what the decision record explicitly guarantees.

## 4. Assessment matrix

Scores: **1 = poor, 5 = strong**. These are structured judgments, not measured probabilities. Options B and C are assessed as written, without silently adding missing controls.

| Option | C1 Target validity 30% | C2 Flight risk 25% | C3 Cost/schedule 20% | C4 Auditability 15% | C5 Options 10% | Weighted score |
|---|---:|---:|---:|---:|---:|---:|
| A. Retain split | 2 | 2 | 3 | 1 | 2 | **2.05** |
| B. TRL 6 at PDR alone | 2 | 2 | 4 | 3 | 3 | **2.65** |
| C. TRL 7 at target alone | 3 | 2 | 3 | 3 | 3 | **2.75** |
| D. Layered rule | 5 | 5 | 3 | 5 | 5 | **4.60** |

The decision is not primarily the numerical margin. D supplies three distinct assurance claims that the other formulations leave incomplete.

## 5. Sensitivity vs trade-off points

### Sensitivity points — factual questions

- **Relevant-environment fidelity:** Can ground testing reproduce the coupled effects of low gravity, anchoring/contact dynamics, uncertain regolith, contamination and assay operation sufficiently for TRL 6? If not, a precursor demonstration may be necessary.
- **Qualification inheritance:** How much spacecraft, avionics and payload evidence is genuinely reusable? Configuration changes can invalidate heritage.
- **Evidence latency:** Cruise, target operations, downlink and independent analysis—not launch—determine the earliest target-gate date.
- **Sampling representativeness:** A working sampler can return a precise measurement of an unrepresentative location. Sampling design may dominate instrument performance.

### Trade-off points — owner values, not facts

- **PDR maturity versus early design flexibility:** Requiring TRL 6 by PDR spends earlier to reduce redesign risk. Accepting TRL 5 at PDR preserves flexibility but requires an explicitly managed closure plan before design commitment.
- **Qualification expenditure versus tolerated scout loss:** A lean mission-class assurance programme can accept greater residual risk, but that is not permission to describe unfinished qualification as TRL 8.
- **More reconnaissance versus delayed 0B:** Additional samples can improve confidence while deferring the real option’s exercise.

**Sensitivity conclusion:** The layered structure survives reasonable changes in weights. Its exact **PDR placement** is less robust than its launch and target-gate requirements. Strong evidence of a lower-cost, controlled TRL-5-at-PDR development path could change that milestone without changing the overall ruling.

## 6. Evidence certainty

GRADE labels below are **adapted to engineering evidence**, not presented as clinical evidence ratings. Likelihood and confidence are kept separate.

| Key claim | Evidence certainty | Confidence and likelihood |
|---|---|---|
| TRL 6, 7 and 8 address different maturity states; TRL 8 concerns an actual system completed and flight-qualified through test and demonstration | **High** for the definitions | **High confidence**; this is definitional, not a probabilistic forecast. |
| TRL 8 does not inherently require a previous successful operational mission by that flight article | **High** under the NASA definition | **High confidence**. Flight qualification and successful mission operation are distinct. |
| TRL 6 alone is insufficient to establish launch readiness | **High** | **High confidence**; no numerical failure probability follows from the TRL. |
| The proposed scouts can achieve the required relevant-environment demonstration entirely on the ground | **Low** on the supplied information | **Low confidence**; likelihood cannot responsibly be quantified without the test architecture. |
| Successful sampling alone establishes exploitable bulk grade | **Low** support for that proposition | **High confidence that it is insufficient as a general rule**; actual adequacy depends on heterogeneity and sampling design. |
| The layered rule will reduce total programme cost | **Low** | **Moderate confidence in reduced ambiguity**, but net savings and schedule effects remain unquantified. |

Definition source: **NASA Systems Engineering Handbook, NASA/SP-2016-6105 Rev 2**, TRL descriptions. Programme constraints are those supplied from D-01, D-02 and the Phase 0 re-baseline; no additional repository contents are assumed.

## 7. Key assumptions

| Assumption | Evidence that would falsify it | Resulting change |
|---|---|---|
| A credible relevant-environment test campaign can precede scout PDR | A test-gap assessment shows essential coupled behaviour cannot be demonstrated without flight | Add a precursor or rephase PDR; do not relabel an inadequate demonstration as TRL 6. |
| The actual flight system can be qualified without a prior mission of the same design | Qualification review identifies an essential acceptance claim that only prior operational flight can establish | Fund that demonstration, change the design or stop. |
| Scout measurements can constrain the resource model at the scale relevant to extraction | Heterogeneity analysis shows feasible sampling cannot bound the resource decision | Expand sampling, narrow the target claim or fail the target gate. |
| The proposed month 12–24 PDR window is compatible with the required work | A resource-loaded schedule and test plan show otherwise | Rebaseline dates explicitly; do not trade away evidence to protect a planning date. |

**ACH ranking, by least disconfirmed explanation of the panel split:**

1. **Different milestones and objects of assessment** — least disconfirmed; the supplied positions explicitly refer to PDR, launch and the target gate.
2. **Different assumptions about what qualifies as relevant-environment or flight-qualification evidence** — plausible, but requires test-plan comparison.
3. **A fundamental disagreement about acceptable scout risk** — possible, but not established by the excerpts.

The first hypothesis warrants clarifying the decision before treating the disagreement as irreconcilable risk preferences.

## 8. Decision, warrant, accepted downside

### Proposed rule text

> **Scout technology readiness.** Before scout PDR, mission-critical novel technologies in T11 and T18, including the integrated sampling-to-assay chain, shall demonstrate TRL 6 in documented relevant environments. Readiness claims shall identify the configuration, functions, environments, test evidence and remaining uncertainties. Existing qualification or heritage evidence may be credited where applicability is demonstrated.
>
> **Launch release.** Before each operational scout launch, the actual integrated spacecraft and its sampling/assay payload shall be completed and flight-qualified through test and demonstration, meeting TRL 8 under the programme’s adopted definition. Launch acceptance shall additionally close required mission-assurance, safety, software, calibration and interface verifications. Qualification scope shall be proportionate to mission class; the TRL label alone is not launch authorisation.
>
> **Target gate.** The gate shall not pass on readiness labels alone. It shall require validated target-specific subsurface sampling and assay results, with predeclared acceptance thresholds covering measurement uncertainty, contamination and calibration, spatial/depth coverage, geological representativeness and relevance to the proposed extraction process. Operational demonstration shall support the applicable TRL assessment, but shall not substitute for resource evidence.
>
> **KDP-0B.** All project-ending technologies shall meet D-02’s TRL-6 relevant-environment requirement without waiver. Successful scout operation does not confer maturity on undemonstrated extraction or production technologies.

The required degree of subsurface coverage and representativeness must be set **before flight**, against the proposed mining decision—not negotiated after seeing favourable samples.

**Warrant:** technology demonstration, flight qualification and investment evidence answer different failure questions. Requiring all three prevents substitution between them.

**Accepted downside:** greater early test expenditure, potentially later PDR, and the possibility that a technically successful scout mission still fails the target gate. That is an intended outcome of honest discrimination, not a programme anomaly.

## 9. Consequences

- Treat **month 12–24 as a planning window**, not evidence that TRL 6 will necessarily be achieved then.
- Schedule the target gate **after the necessary mission data are returned, validated and independently reviewed**. It cannot be brought forward by declaring the spacecraft TRL 8.
- Do not require every scout to launch before the target gate: the required sequence depends on the predeclared evidence sufficiency plan.
- Maintain an evidence register linking each maturity claim to its configuration and relevant environment.
- Budget sampling representativeness and assay validation alongside spacecraft qualification.
- Preserve the four separate target, demand, economics and licence gates. A target pass does not authorise 0B by itself.
- If required evidence cannot be obtained within the authorised envelope, apply the pre-committed failure outcome: **0A only, Earth supply**.

**Decision Y-statement:** In the context of D-01’s gated 0B option and D-02’s reversibility-based assurance policy, facing conflicting scout TRL requirements attached to different milestones, we chose TRL 6 for critical novel technologies at scout PDR, TRL 8 for each actual flight system before launch, and validated sampling evidence for the target gate, to achieve credible flight readiness and an evidence-based resource decision, accepting additional early qualification effort and potentially later gate passage. **The warrant** is that these are distinct assurance claims; **the qualifier** is that PDR timing remains revisable on a documented test-and-cost case, while launch qualification and target evidence do not. This enables scout development and gate scheduling, and constrains KDP-0B against premature commitment.