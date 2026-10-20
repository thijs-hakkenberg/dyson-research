---
questionId: "rq-0-75"
questionSlug: "t01-mw-sep-trl6-test-path"
modelId: "gpt-6-1-sol"
modelName: "GPT-6.1 Sol"
roundNumber: 1
generated: "2026-10-17"
type: "discussion-response"
---

## 1. Frame & decision type

**Recommend ground qualification plus a representative flight subset as the baseline T01 evidence programme.** Ground modules and a cluster model remain essential, but should not currently be accepted as the sole route to KDP-0B.

This is an **executive decision about verification strategy**, constraining the propulsion architecture. It is reversible during 0A; accepting its evidence at KDP-0B is not. Under D-02, the question is therefore not “must TRL 6 include flight?”—it need not—but:

> Can the chosen demonstration establish that the MW-class cluster’s project-ending behaviours are understood and bounded in a relevant environment?

The information supplied does not yet establish that ground-module tests plus modelling can do that. Equally, Claude’s facility-limit claim is not sufficient evidence that every suitable ground campaign is impossible.

The immediate decision should fund an evidence strategy, not prematurely certify either route.

## 2. Criteria and weights

**Non-compensable musts**

- Demonstrate T01 at TRL 6 in its relevant environment before KDP-0B, without waiver.
- Cover project-ending cluster interactions, not merely individual thruster maturity.
- Trace the demonstration to the selected propellant under D-05 and the applicable requirements, including rq-0-16/rq-0-54.
- Provide an independently reviewable verification argument, including model uncertainty and extrapolation limits.

A high weighted score cannot offset failure of a must.

The following **swing weights** compare plausible programme outcomes, not abstract importance:

| Criterion | Weight | Worst-to-best swing being valued |
|---|---:|---|
| **C1. Cluster-level evidence strength** | 40% | Major coupled behaviours remain extrapolated → flight-scale behaviour is bounded by representative tests and validated predictions. Largest weight because T01 is project-ending. |
| **C2. Diagnostic value** | 20% | An anomaly cannot distinguish competing causes → measurements discriminate facility effects, module effects and cluster interactions. This substantially affects whether failures can be corrected. |
| **C3. Incremental 0A cost** | 15% | Major new spacecraft/facility development → reuse of funded equipment and infrastructure. Important under D-01, but cannot buy down the assurance standard. |
| **C4. Evidence availability before KDP-0B** | 15% | Critical evidence arrives after the decision window → reviewed evidence arrives with time for correction. |
| **C5. Adaptability and reusable capability** | 10% | Evidence tied to one brittle configuration → reusable test assets and methods across credible architecture changes. Smaller weight because reuse is secondary to gate closure. |

These weights are proposed owner value judgments. They are not empirical findings.

## 3. Options

**N — Null: leave the split unresolved.**  
Preserves short-term discretion and avoids immediate commitment. Reject: neither facilities nor a flight demonstrator can be credibly scheduled around an undecided evidence architecture. The apparent saving is purchased by allowing T01 to become a late programme veto.

**A — Ground modules plus a validated cluster model; no planned flight subset.**  
Strong argument: controlled, repeatable tests support diagnostics and endurance testing, potentially at much lower incremental cost. Reject **as today’s baseline**, because no supplied evidence establishes that the decisive cluster effects are sufficiently local, separable and measurable on the ground. Keep as a possible later substitution.

**B — Ground qualification plus a representative flight subset.**  
Ground tests establish module performance, endurance, off-nominal behaviour and controlled interactions. Flight tests address the coupled effects whose relevant environment cannot be convincingly reproduced on the ground. Recommend this option.

**C — Full intended MW-class cluster flight demonstration.**  
Strongest direct coverage of full-power geometry and simultaneous operation. Reject as the default: it risks turning the verification vehicle into an expensive precursor mission, with launch, power, thermal and spacecraft integration on the critical path. Full-cluster flight remains a possible escalation if subset scaling cannot be justified.

A new full-power ground facility is not a separate preferred route here: it is a potential implementation of A that would need its own facility-effectiveness, cost and schedule case.

## 4. Assessment matrix

Illustrative scores: **1 = weak; 5 = strong**. These are structured judgments, not measured utilities or probabilities.

| Option | C1 Evidence 40% | C2 Diagnostics 20% | C3 Cost 15% | C4 Schedule 15% | C5 Adaptability 10% | Weighted /5 |
|---|---:|---:|---:|---:|---:|---:|
| N — Unresolved | 1 | 1 | 3 | 1 | 2 | **1.40** |
| A — Ground + model | 2 | 3 | 5 | 4 | 3 | **3.05** |
| **B — Ground + flight subset** | **4** | **4** | **2** | **2** | **4** | **3.40** |
| C — Full-cluster flight | 5 | 4 | 1 | 1 | 1 | **3.20** |

All substantive routes remain **conditional on satisfying the musts**. In particular, neither a flight subset nor a full-cluster flight automatically qualifies as TRL 6.

The ranking favours B, but not overwhelmingly. Its warrant must come from the verification case, not the decimal score.

## 5. Sensitivity vs trade-off points

### Sensitivity points — facts that could change the ranking

1. **Nonlocal cluster physics.** Do plume overlap, spacecraft potential, neutral transport or power-system interactions change materially as active area and total power increase?
2. **Facility perturbation.** Can background pressure, ingestion, charge exchange and wall effects be measured and corrected within the required uncertainty?
3. **Flight-subset representativeness.** Does the selected geometry reproduce the controlling interactions, or merely show that several thrusters operate together?
4. **Host availability.** A pathfinder with compatible power, propellant, thermal rejection, communications and schedule could substantially improve B’s cost and schedule scores.
5. **Propellant choice under D-05.** A change can invalidate discharge, erosion, plume and facility assumptions; transferability must be demonstrated rather than presumed.

### Trade-off points — owner values, not unresolved physics

- **Additional 0A expenditure versus residual extrapolation risk at an irreversible gate.**
- **Shared pathfinder efficiency versus independent demonstrator scheduling and design control.**
- **Earlier commitment to a propulsion configuration versus retaining propellant and architecture flexibility.**

Under D-01/D-02, I favour spending more on discriminating evidence rather than lowering the standard or relying on schedule optimism. That does **not** justify unlimited demonstrator spending: if the evidence programme becomes uneconomic, retain “0A only, Earth supply.”

## 6. Evidence certainty

GRADE labels below are adapted to engineering evidence. Confidence concerns the strength of the assessment; likelihood concerns a future outcome. They are not interchangeable.

| Key claim | Evidence certainty / confidence | Likelihood judgment |
|---|---|---|
| TRL 6 requires a representative system/subsystem demonstration in a relevant environment; flight is not universally mandatory. | **High / high.** Consistent with NASA’s *Systems Engineering Handbook*, NASA/SP-2016-6105 Rev 2. | Not a probability claim. |
| Facility background and boundaries can alter electric-propulsion measurements. | **High / high** for the general phenomenon; **low / low** for its magnitude in this particular T01 configuration. | Material distortion is plausible; no project-specific probability is justified. |
| No available facility can support the required T01 demonstration. | **Very low / low** on the supplied record: one panel assertion, without a facility/configuration comparison. | Undetermined. |
| A flight subset plus ground evidence can close full-cluster TRL 6. | **Low / low-to-moderate** before configuration and scaling validation. It is a testable engineering hypothesis. | Plausible, not established. |
| Ground-only closure can satisfy D-02 for this architecture. | **Low / low** for the same reason. | Plausible under favourable scaling and facility evidence; not yet demonstrated. |
| Requiring a dedicated flight demonstrator increases integration and schedule exposure. | **Moderate / moderate** as an engineering judgment; no project cost estimate is supplied. | More likely than not relative to ground-only work, but the increment is unquantified. |

I have not inspected the referenced repository files or the full text of rq-0-16/rq-0-54. Their acceptance limits must be incorporated before this becomes a controlled specification.

## 7. Key assumptions

### ACH: competing hypotheses, ranked by least disconfirmed

The available record is too sparse for a decisive empirical ranking. A provisional, **low-confidence** ranking is:

1. **H-B: ground evidence plus a flight subset can bound the important scaling effects.** No supplied observation directly contradicts it, but representative scaling remains unproven.
2. **H-A: ground modules and modelling alone suffice.** More exposed to the unresolved facility and cluster-integration concerns.
3. **H-C: only full-cluster flight can suffice.** Makes a stronger necessity claim than the supplied evidence supports.

This is a ranking of working hypotheses, not proof of B.

| Key assumption | Evidence that would falsify it |
|---|---|
| A subset can reproduce the controlling interaction topology. | Tests show new collective behaviour with increasing active area, cluster size or total power that the subset cannot reproduce or predict. |
| Ground tests can establish module endurance and degradation. | Facility-dependent erosion or ingestion prevents mission-relevant life inference within allocated uncertainty. |
| Cluster models can predict rather than merely fit. | Pre-registered predictions fail on withheld configurations, operating points or flight measurements. |
| A suitable host or dedicated demonstrator is feasible within 0A. | Resource budgets, interfaces, procurement or schedule analysis show no credible route to reviewed results before KDP-0B. |
| The demonstrated propellant/configuration represents the eventual design. | D-05 or later architecture changes introduce materially different operating physics outside the validated domain. |

**What would change my ruling:** an independently reviewed ground-only assurance case demonstrating acceptable facility effects, successful blind predictions across cluster configurations, and bounded full-scale extrapolation would justify switching to A. Conversely, evidence of unbounded size-dependent interactions would require C—or stopping 0B.

## 8. Decision, warrant, accepted downside

### Proposed gate rule

> **T01 shall demonstrate TRL 6 before KDP-0B through a configuration-controlled verification case combining representative hardware tests and validated analysis. The baseline shall include ground qualification and a representative flight subset.**
>
> **The demonstration shall cover the selected propellant, relevant cluster geometry, simultaneous operation, shared power/PPU interactions, thermal behaviour, plume–spacecraft interactions, and representative operating and fault transitions. Each project-ending behaviour shall be demonstrated directly or bounded by validated extrapolation against applicable requirements and allocated uncertainty.**
>
> **A ground-only substitution requires independent technical approval of equivalent evidence; this is an alternative means of compliance, not a TRL waiver. Missing or inconclusive evidence shall block KDP-0B.**

The flight subset should be sized by **interaction coverage**, not a nominal power percentage or arbitrary thruster count. It must include the neighbour relationships, shared electrical architecture and spacecraft interfaces needed to test the scaling argument. A single thruster flown on an unrelated bus would not close cluster integration.

Ground endurance evidence remains necessary: a short flight cannot establish mission life.

**Accepted downside:** B adds spacecraft integration, launch dependence and possible propulsion-design commitment before 0B is authorised. It can also fail to close the gate. Those are preferable to declaring full-cluster maturity from an unvalidated extrapolation.

## 9. Consequences

- **At KDP-0A:** approve the T01 verification architecture, uncertainty budget, facility survey and flight-host trade—not a claim of achieved maturity.
- **At the 0A mid-term review:** require representative ground data, withheld-data model predictions, the subset scaling argument, D-05 alignment and a credible demonstrator delivery plan. Decide whether to continue B, substitute proven A, escalate, or stop 0B preparation.
- **Before KDP-0B:** independently review the evidence against rq-0-16/rq-0-54 and all linked T01 requirements. No launch, no useful telemetry, or failed scaling validation means no closure.
- Choose the pathfinder as host only if it can carry the evidence obligations without compromising its primary objectives; otherwise assess a dedicated tug demonstrator explicitly.
- Preserve the pre-committed outcome: **0A capability programme only, Earth supply** if T01 cannot close affordably and on time.

**Y-statement:** In the context of D-01’s gated capability programme and D-02’s no-waiver KDP-0B, facing unresolved facility effects and MW-cluster scaling, we choose ground qualification plus a representative flight subset to obtain defensible cluster-level evidence, accepting added cost, launch dependence and possible gate failure. **Warrant:** complementary environments test different failure mechanisms and reduce reliance on unsupported extrapolation. **Qualifier:** this recommendation is provisional on representative scaling; independently demonstrated ground equivalence may replace flight, while unbounded scaling may require full-cluster demonstration or termination. It enables demonstrator and facility planning, constrains D-05 and propulsion configuration changes, and does not authorise 0B.