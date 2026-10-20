---
questionId: "rq-0-65"
questionSlug: "gate-risk-class-split-technologies"
modelId: "gpt-6-1-sol"
modelName: "GPT-6.1 Sol"
roundNumber: 1
generated: "2026-10-17"
type: "discussion-response"
---

## 1. Frame & decision type

**Recommendation:** classify **T02, T10, T14, T15, T22, T24 and T25 as project-ending for the selected 0B production architecture**. Retain **T26 as architecture-change under rq-0-64**, but require a bounded closure test at KDP-0A; absent evidence that its loss is survivable, elevate it to project-ending.

The governing question is not “Could another engineering solution exist?” It is:

> **If this technology fails its qualification, is there an evidenced alternative that preserves an authorised 0B production capability before irreversible commitment?**

“Project-ending” here means ending the proposed **0B production commitment**, not cancelling the funded 0A capability programme. “0A only, Earth supply” is the programme’s safe exit under D-01—not a fallback that justifies admitting an immature 0B production architecture.

This is a **property and executive decision**: classification remains revisable during 0A, but determines assurance requirements at the one-way KDP-0B gate.

There is also a source-control issue. The supplied “agreed core” includes technologies whose individual panel classifications differ. I would treat that list as a proposed gate baseline, **not evidence of unanimous agreement**. The owner’s ruling must resolve this explicitly.

## 2. Criteria and weights

**Non-compensable requirements**

- Respect D-02: project-ending technologies require TRL 6 in a relevant environment at KDP-0B, without waiver.
- Preserve D-01: 0B remains a demand-sized real option; classification cannot create an obligation to proceed.
- Do not count an unverified replacement, or retreat to Earth supply, as proof of continued 0B production.

For options passing those requirements, use these **swing weights**:

| Criterion | Weight | Range being valued and justification |
|---|---:|---|
| **C1. Avoid unsupported irreversible commitment** | **45%** | From committing with an unproven indispensable function to requiring demonstrated capability or a qualified substitute. This is the largest swing because failure can invalidate the entire 0B investment. |
| **C2. Avoid unnecessary qualification cost and delay** | **25%** | From forcing every implementation to TRL 6 regardless of replaceability to qualifying only what the selected production architecture actually needs. This materially affects the cost and duration of 0A. |
| **C3. Auditability and enforceability** | **20%** | From unresolved labels and discretionary exceptions to a reproducible dependency-and-evidence test. A gate rule has little value if it can be reinterpreted at commitment. |
| **C4. Preserve useful architecture options** | **10%** | From locking one implementation prematurely to allowing demonstrated substitutes without weakening functional assurance. Important, but subordinate to protecting the irreversible decision. |

These are proposed owner value judgments, not empirically measured constants.

## 3. Options

**A. Null: retain the split and current interim holds.**  
Argument for: avoids premature classification and preserves the existing conservative TRL 6 holds.  
**Reject:** the split remains unresolved, T26 remains ambiguous, and development teams cannot reliably plan qualification scope.

**B. Permanently classify all eight as project-ending.**  
Argument for: simple, conservative, and resistant to optimistic fallback claims.  
**Reject:** confuses essential functions with replaceable implementations, especially for T26, and may impose avoidable bespoke qualification.

**C. Evidence-conditioned classification, with seven project-ending and bounded T26 closure. — Recommended.**  
Argument for: protects indispensable capabilities while making declassification depend on demonstrated, affordable alternatives rather than opinion.

**D. Classify all eight as architecture-change unless impossibility of substitution is proven.**  
Argument for: maximises flexibility and initially reduces qualification burden.  
**Reject:** reverses the burden of proof. Proving that no imaginable alternative exists is infeasible; the relevant question is whether a usable alternative has actually been established.

## 4. Assessment matrix

Scores are **ordinal judgments**, 1 = poor and 5 = strong. Weighted totals structure the debate; they are not probabilities or measured benefits.

| Option | C1: Commitment protection 45% | C2: Cost/delay 25% | C3: Auditability 20% | C4: Options 10% | Weighted score / 5 |
|---|---:|---:|---:|---:|---:|
| A. Retain split | 3 | 2 | 1 | 3 | **2.35** |
| B. All eight permanently project-ending | 5 | 1 | 4 | 1 | **3.55** |
| **C. Evidence-conditioned ruling** | **5** | **3** | **4** | **5** | **4.30** |
| D. All architecture-change | 1 | 4 | 2 | 5 | **2.40** |

### Recommended technology rulings

| Technology | Ruling | Reason; evidence that could change it |
|---|---|---|
| **T02: MW-scale deployable arrays** | **Project-ending** | Selected tug/site power architecture depends on power at scale. Declassify only after an alternative closes power, deployment, mass, thermal and transport budgets at accepted production throughput. “Use smaller arrays” alone is not evidence. |
| **T10: Long-duration autonomy** | **Project-ending** | Intermittently supervised operations must sustain production and manage hazardous states. A less autonomous alternative must demonstrate workload, latency tolerance, safe recovery and communications dependence—not merely nominal teleoperation. |
| **T14: Large-scale propellant storage/feed** | **Project-ending** | Propellant delivery is integral to tug performance. Alternate propellant, tanking or mission staging must close feed behaviour, storage losses as applicable, mass, transfer cadence and delivered-cargo performance. |
| **T15: Site power generation/transfer** | **Project-ending** | Mining and processing require an integrated power service. Reclassification requires demonstrated operating power, duty cycle, distribution and fault recovery for the selected site—not source nameplate power alone. |
| **T22: Product consolidation, packaging, qualification** | **Project-ending** | Producing material is insufficient if it cannot be accepted, transported and used. A simpler product form could change the ruling, but requires an agreed acceptance specification and qualified handling/transport chain. |
| **T24: Dust-tolerant mechanisms/seals** | **Project-ending** | Common environmental failures could disable multiple production functions. Demonstrated dust exclusion, reduced mechanism dependence, or replaceable short-life modules could justify reclassification if logistics and maintenance close. |
| **T25: Local/node navigation and control** | **Project-ending** | Safe acquisition, approach and cargo exchange are indispensable to the selected logistics chain. Alternate nodes, cooperative aids or supervised operations must demonstrate capture margins, abort behaviour, traffic capacity and outage tolerance. |
| **T26: Communications/resilient command** | **Architecture-change, bounded by rq-0-64 closure** | Retain the existing owner ruling provisionally. By KDP-0A, demonstrate that loss of the proposed implementation permits a qualified alternative service and tolerable disconnected operation. Otherwise automatically elevate to **project-ending**. |

A technology ID may contain both essential and replaceable elements. Split the requirement where necessary; do not let a broad label hide an unqualified essential function.

## 5. Sensitivity vs trade-off points

### Sensitivity points—facts that can change the ruling

- **Minimum authorised production:** lower throughput may make smaller power systems, batch processing or slower logistics viable.
- **Disconnected endurance:** affects T10, T25 and T26 together.
- **Maintenance concept:** replaceable modules could reduce T24 life requirements, but increase spares and transport demand.
- **Product acceptance requirements:** directly determine T22’s qualification burden.
- **Common-cause independence:** a backup sharing the same software, power system or geometry may not provide meaningful substitution.

### Trade-off points—owner values, not facts to discover

- How much production reduction is acceptable to preserve 0B?
- How much additional 0A cost and delay is worth reducing irreversible exposure?
- How much staffing and recurring communications expenditure is acceptable in exchange for reduced autonomy?

**Recommendation sensitivity:** Option C’s advantage over B depends on its evidence process being enforceable. If the programme cannot independently review fallback claims or control requirements changes, B becomes the safer operational policy.

## 6. Evidence certainty

These are **adapted GRADE judgments**, not formal clinical-style evidence reviews. The available record is the supplied synthesis of `gates.md`, `gates-proposal.yaml`, `trl-baseline.yaml` and `decisions.md`; no supporting test reports or costed fallback studies were provided.

| Key claim | Evidence certainty | Analytic confidence; likelihood |
|---|---|---|
| D-01/D-02 establish the stated real-option and no-waiver principles | **High within the supplied decision record** | High confidence in the policy interpretation; not a probabilistic claim. |
| The seven proposed project-ending technologies support indispensable production functions | **Moderate** | Moderate confidence from functional dependencies; architecture-specific substitution remains unresolved. |
| No admissible fallback has yet been established for those seven | **Low** | High confidence that none is demonstrated **in this record**; low confidence about whether undisclosed work exists. |
| T26 can remain architecture-change without weakening 0B assurance | **Low** | Conditional judgment only; depends on service alternatives and disconnected operations evidence. |
| Evidence-conditioned classification will reduce unnecessary qualification spending | **Low** | Plausible benefit, but magnitude and likelihood cannot be estimated from the supplied material. |

The panel’s TRL spreads are not probability distributions. In particular, T26’s competing maturity assessments require a common **unit of assessment**: component, link, or integrated command service.

## 7. Key assumptions

| Assumption | Evidence that would falsify it |
|---|---|
| 0B production requires the functions represented by the seven project-ending technologies | A controlled production architecture that removes a function while satisfying authorised output, safety, licence and economics constraints. |
| No currently evidenced fallback warrants lower classification | An independently reviewed fallback package with relevant demonstrations, resources, interfaces and executable transition plan. |
| T26’s implementation can potentially be substituted without losing the production mission | Evidence of unavoidable command dependence, inadequate communications alternatives, or failure of safe disconnected operation. This would trigger elevation. |
| TRL demonstrations can be scoped meaningfully to the selected architecture | Findings that interactions, duration or scale effects are not represented by the proposed demonstration; the verification scope must then expand. |

**ACH ranking, least disconfirmed first:**

1. **Essential functions with potentially replaceable implementations**—best fits the functional dependencies and classification disagreements.
2. **Every listed implementation is indispensable**—possible, but too strong without architecture-level fallback analysis.
3. **All eight have readily usable alternatives**—least supported; no qualifying fallback packages are presented.

This ranks hypotheses by current contradiction, not numerical probability.

## 8. Decision, warrant, accepted downside

Adopt Option C and insert this rule into the gate proposal:

> **A technology is project-ending where failure of its required capability leaves no evidenced alternative preserving authorised 0B production within approved safety, licence, performance, schedule and cost limits. Unproven alternatives do not justify lower classification. Project-ending technologies shall achieve TRL 6 in the relevant environment before KDP-0B, without waiver.**
>
> **Reclassification requires owner approval of an independently reviewed fallback package identifying the replacement, qualification evidence, integrated budgets, transition resources, dependencies and common-cause vulnerabilities. A fallback requiring an unqualified project-ending technology is inadmissible.**
>
> **T26 retains rq-0-64’s architecture-change ruling until KDP-0A. Failure to demonstrate survivable substitution or disconnection by that review automatically makes the affected capability project-ending.**

**Warrant:** failure consequences and reversibility—not panel vote counts, current TRL or generic technological familiarity—determine required assurance.

**Accepted downside:** additional 0A analysis and testing, and potentially a delayed or rejected 0B commitment. This is preferable to discovering after commitment that an “architecture change” is actually a new production programme.

## 9. Consequences

- **Owner:** approve the classifications and define acceptable fallback performance/cost boundaries at KDP-0A.
- **Technology leads:** produce function-specific qualification plans and bounded fallback packages.
- **Systems engineering:** maintain dependency and common-cause analyses, especially across power, autonomy, navigation and communications.
- **Gate authority:** assess the selected integrated service, not merely mature components; architecture-change status is not blanket permission for immature critical functions.
- **Programme control:** preserve “0A only, Earth supply” as the exit if KDP-0B fails. Target, demand, economics and licence gates remain independent.

**Y-statement:** *In the context of a funded 0A capability programme and optional 0B production commitment, facing unresolved classifications and unevidenced fallbacks, we chose seven project-ending classifications and a time-bounded architecture-change ruling for T26, to protect irreversible investment while permitting demonstrated substitution, accepting additional 0A qualification effort.*

**Warrant and qualifier:** indispensable production functions require demonstrated capability before commitment; these classifications remain revisable only when architecture-specific evidence establishes a credible alternative. This enables qualification planning and rq-0-64 closure, while constraining KDP-0B from proceeding on optimistic substitution claims.