---
questionId: "rq-0-71"
questionSlug: "trl6-scale-extrapolation-rule"
modelId: "gpt-6-1-sol"
modelName: "GPT-6.1 Sol"
roundNumber: 1
generated: "2026-10-17"
type: "discussion-response"
---

## 1. Frame & decision type

**Recommendation: do not impose a universal scale-extrapolation limit. Impose a binding, technology-specific extrapolation envelope, supported by physical demonstrations, test-validated models and independent review.** Neither “less than 10×” nor “preserves the governing regime” should, alone, establish acceptability.

This is a **property decision about evidence admissibility**, supporting the executive decision at KDP-0B. The rule can be revised during 0A; committing 0B on inadequate evidence is much less reversible.

The decision must preserve the accepted Project Dyson positions, as described in the supplied WP-A material:

- **D-01:** 0B remains a real option, sized by signed Phase 1 demand.
- **D-02:** project-ending technologies require TRL 6 in a relevant environment at KDP-0B, without waivers.
- Failure retains the pre-committed **“0A only, Earth supply”** fallback.

The question is not whether a model can replace a demonstration. It cannot. It is how a demonstrated representative prototype can credibly support the **specific deployment configuration** proposed at the gate.

## 2. Criteria and weights

### Non-compensable requirements

Before weighted comparison, any adopted rule must:

1. Preserve the TRL 6 physical demonstration and relevant-environment requirement.
2. Prevent cost or schedule pressure from compensating for insufficient evidence on project-ending technologies.
3. Identify the deployment configuration and operating envelope to which the readiness judgment applies.
4. Produce an auditable pass/fail decision, including treatment of unresolved uncertainty.

The null option below represents leaving the issue unresolved—not permission to bypass these requirements.

### Swing weights

These are proposed owner values, not empirically measured constants.

| Criterion | Evaluated swing | Weight | Why this weight fits that range |
|---|---|---:|---|
| **A. Protection against false readiness** | From accepting poorly supported extrapolation to detecting credible scale-dependent failure | **40%** | This swing affects an irreversible commitment and potential loss of the programme’s rationale. |
| **B. Demonstration cost and feasibility** | From requiring unnecessary near-flight-scale facilities to obtaining adequate evidence with practicable tests | **25%** | The swing can determine whether 0A can affordably preserve the 0B option. |
| **C. Auditability and consistency** | From discretionary interpretation to reproducible, independently reviewable judgments | **20%** | A technically sophisticated rule is ineffective if vendors or reviewers apply it inconsistently. |
| **D. Applicability across technologies** | From one scalar rule that mischaracterises different systems to treatment of power, throughput, replication and life on their own terms | **15%** | This matters across the portfolio, but must not outweigh readiness protection. |

## 3. Options

**N — Null: retain the unresolved panel split.**  
Argument: avoids premature standardisation while designs mature.  
**Reject:** leaves test teams unable to determine what evidence will count and invites gate-time negotiation.

**F — Hard ceiling: require no more than 10× extrapolation.**  
Argument: simple, predictable and visibly conservative.  
**Reject:** the numerical ratio is neither sufficient nor necessary evidence of representativeness. A 3× change can cross an instability threshold; 30× aggregate throughput may come from replicated, already demonstrated modules.

**P — Presumptive 10× ceiling, rebuttable by regime preservation.**  
This approximates Claude’s proposal.  
Argument: provides a planning default while allowing physically justified exceptions.  
**Reject as the programme-wide acceptance rule:** it risks making ≤10× appear inherently acceptable and >10× an “exception” even when replication is less risky than modest unit scaling. It remains defensible as a temporary planning heuristic, explicitly not a gate entitlement.

**E — No universal ratio; mandatory evidence-bounded extrapolation envelope.**  
Argument: evaluates the actual mechanisms that can invalidate scale-up, while making discretion reviewable.  
**Select:** pre-agree the evidence plan, validate predictions against independent test data, quantify uncertainty and limit readiness credit to the resulting deployment envelope.

This agrees with GPT’s objection to a fixed acceptable factor, but adds an important constraint: **“test-validated models” must become an operational acceptance standard, not an open-ended assurance phrase.**

## 4. Assessment matrix

Scores: 1 = weak, 5 = strong. These are structured engineering judgments, not measured utilities or probabilities.

| Option | A: Readiness protection 40% | B: Cost/feasibility 25% | C: Auditability 20% | D: Applicability 15% | Weighted score |
|---|---:|---:|---:|---:|---:|
| N — Unresolved split | 2 | 2 | 1 | 2 | **1.80** |
| F — Hard 10× ceiling | 3 | 1 | 5 | 1 | **2.60** |
| P — Presumptive 10×, rebuttable | 4 | 3 | 4 | 3 | **3.60** |
| E — Evidence-bounded envelope | 4 | 4 | 4 | 5 | **4.15** |

The equal readiness scores for P and E are deliberate: **there is no Project Dyson evidence demonstrating that either governance approach produces fewer false passes.** E wins principally by avoiding unnecessary demonstrations and fitting heterogeneous technologies—not through an asserted, unmeasured safety advantage.

No weighted score can override the non-compensable requirements.

## 5. Sensitivity vs trade-off points

### Sensitivity points — factual questions

- **Validation reach:** how far does a model predict successfully outside its calibration conditions?
- **Emergent coupling:** does increasing unit count introduce shared power, thermal, control, feedstock or maintenance bottlenecks?
- **Damage mechanism:** does accelerated testing reproduce service degradation, or create a different failure process?
- **Deployment architecture:** is growth achieved by enlarging equipment or replicating modules?

These facts can change the preferred test size and potentially the policy ranking.

For example, if P deserves readiness score 5 and E only 3 because independent review proves ineffective, their totals become **4.00 and 3.75**, respectively. The recommendation therefore depends materially on enforceable assurance—not simply opposition to arbitrary numbers.

### Trade-off points — values questions

- How much additional pathfinder expenditure is justified to reduce residual uncertainty before an irreversible commitment?
- How much reviewer discretion is acceptable in exchange for avoiding unnecessary facilities?
- Should the programme prefer a smaller, demonstrable 0B architecture over a larger, economically attractive but less supportable one?

These require owner judgment. More testing can inform them but cannot determine the acceptable balance.

## 6. Evidence certainty

GRADE terms below are **adapted to engineering evidence**, not presented as formal clinical assessments.

| Key claim | Evidence and certainty | Likelihood versus confidence |
|---|---|---|
| A universal 10× ratio does not establish TRL 6 representativeness. | **Moderate certainty.** Established scaling physics and TRL definitions support this; direct comparative Project Dyson gate-outcome evidence is absent. | High confidence in the general limitation; no estimated probability of a Dyson gate failure. |
| Validated models can support—but not replace—representative physical demonstrations. | **Moderate certainty** for application here. NASA’s *Systems Engineering Handbook*, NASA/SP-2016-6105 Rev 2, and NASA-STD-7009, *Standard for Models and Simulations*, support the underlying distinction and credibility disciplines. | High confidence in the principle; project-specific extrapolation success remains unquantified. |
| Modular replication can reduce the required unit-scale extrapolation, while introducing system-level risks. | **Moderate certainty.** Strong engineering basis; applicability depends on architecture and coupling. | Moderate confidence for Dyson until architecture and integrated tests are available; no numerical likelihood assigned. |
| Accelerated endurance evidence is credible only when the degradation mechanism and acceleration relationship are supported. | **Moderate certainty.** Established reliability-engineering reasoning; material- and process-specific evidence is still needed. | High confidence in the constraint; low confidence in any presently unspecified lifetime prediction. |
| E will cost less than P or F for equivalent assurance. | **Low certainty.** Plausible, but no technology-specific facility costs or evidence plans were supplied. | Low confidence; savings magnitude and likelihood are not estimated. |

The Project Dyson decision references establish programme intent as supplied in the question. They do not establish technology-specific model validity.

## 7. Key assumptions

| Assumption | Evidence that would falsify it |
|---|---|
| Independent reviewers can distinguish a validated predictive model from a well-fitted calibration model. | Blind prediction exercises show persistent failures, or separate reviewers cannot reproduce acceptance judgments. |
| Each project-ending technology has identifiable dominant scale-sensitive mechanisms. | Larger-scale tests reveal consequential mechanisms omitted from the approved model and test plan. |
| Representative testing remains feasible without a universal near-full-scale requirement. | Facility and coupling studies show that only nearly full-scale hardware reproduces the critical environment or interactions. |
| The accepted deployment envelope can constrain subsequent design changes. | Procurement or demand decisions repeatedly enlarge the architecture without reopening readiness assessment. |

### Competing hypotheses, ranked by least disconfirmed

1. **Mechanism-specific evidence envelopes best govern admissible extrapolation.** Least contradicted by known differences among physical processes.
2. **A rebuttable 10× presumption materially improves decision discipline.** Plausible, but its benefit over explicit evidence requirements is unproven.
3. **A universal hard 10× ceiling reliably bounds scale-up risk.** Most contradicted by modular replication and threshold-dependent failures.

This is a qualitative ACH ranking, not a claim of measured posterior probabilities.

**Evidence that would change my ruling:** a relevant back-test showing that a particular ratio threshold reliably identifies failures missed by the evidence-envelope approach; poor inter-reviewer reproducibility; or repeated blind-prediction failures that cannot be corrected through improved validation. Conversely, successful cross-scale prediction on representative Dyson technologies would strengthen E.

## 8. Decision, warrant, accepted downside

**Adopt E, with mandatory independent concurrence and configuration control.**

### Proposed gate rule

> **KDP-0B scale and duration evidence**
>
> Each project-ending technology shall demonstrate TRL 6 through a representative system/subsystem model or prototype in a relevant environment. No universal throughput, power or duration extrapolation ratio establishes or prohibits acceptance.
>
> Readiness credit shall be limited to a specified deployment configuration and operating envelope, supported by:
>
> 1. Physical test evidence covering the critical functions, interfaces and relevant environmental conditions.
> 2. Identification of scale-sensitive mechanisms, governing regimes, credible transitions and coupled failure modes.
> 3. Models calibrated against test data and validated against independent data or pre-declared prediction tests, with measurement uncertainty, parameter uncertainty and model discrepancy addressed.
> 4. Demonstrated margins against pre-agreed performance and failure criteria throughout the claimed deployment envelope.
> 5. Independent technical concurrence that unresolved extrapolation uncertainty does not defeat those criteria.
>
> An extrapolation unsupported by this evidence shall receive no readiness credit, irrespective of whether its ratio is below 10×. Supported extrapolation above 10× is not a waiver of the TRL requirement.
>
> If sufficient evidence cannot be obtained, the programme shall reduce the proposed deployment envelope, obtain further evidence, or withhold KDP-0B approval under the pre-committed failure outcomes.

**Additional interpretation:**

- **Throughput:** distinguish unit enlargement from replication; test shared-resource limitations and correlated failures.
- **Power:** assess voltage, current density, heat flux, temperature gradients, control stability and electrical interactions—not aggregate watts alone.
- **Duration:** permit partial-duration plus accelerated testing only where the degradation model and acceleration relationship are validated. Different damage modes may require different tests; a single “hours multiplier” is insufficient.
- **Integration:** component evidence cannot substitute for the representative system/subsystem demonstration.
- **Qualification:** TRL 6 is not full operational qualification. Nevertheless, a project-ending lifetime assumption cannot remain unsupported merely because formal qualification comes later.

The accepted downside is higher front-loaded analysis, independent-review cost and potentially disputed judgments. Some technologies may still require near-deployment-scale tests.

## 9. Consequences

1. **During 0A:** each technology owner produces a scale-and-life evidence plan before committing major pathfinder expenditure. It identifies calibration tests, independent validation tests, uncertainty treatment and acceptance criteria.
2. **At the mid-term review:** assess prediction performance and facility adequacy. Revise test scale while the decision remains reversible.
3. **At KDP-0B:** reconcile the signed-demand-sized architecture under D-01 with the demonstrated envelope. Demand cannot enlarge readiness credit.
4. **After approval:** material changes in module size, operating conditions, coupling or required life trigger reassessment.
5. **Keep gates separate:** technology readiness does not establish target suitability, demand, economics or licence acceptability.

**Y-statement:** In the context of Project Dyson’s irreversible KDP-0B commitment, facing heterogeneous scale-up and lifetime risks, we chose technology-specific, independently reviewed evidence envelopes rather than a universal extrapolation ceiling, to achieve defensible TRL 6 decisions without mandating unnecessary test scale, accepting greater assurance effort and less numerical simplicity.

**Warrant:** representativeness depends on failure mechanisms, interactions and validated predictive reach—not one aggregate ratio. **Qualifier:** this choice holds only while independent review and validation are demonstrably effective; it does not presume any particular extrapolation is acceptable. **Enabled and constrained decisions:** it enables technology-specific pathfinder sizing and modular architectures, while constraining 0B scope to the evidenced envelope and preserving “0A only, Earth supply” when that envelope is insufficient.