---
questionId: "rq-0-74"
questionSlug: "d02-0a-milestone-trl-flight-projects"
modelId: "gpt-6-1-sol"
modelName: "GPT-6.1 Sol"
roundNumber: 1
generated: "2026-10-17"
type: "discussion-response"
---

## 1. Frame & decision type

**Recommended ruling: retain TRL 4–5 for reversible 0A funding decisions, but explicitly exclude flight authorisation. Adopt a narrow amendment to D-02 that distinguishes flight-enabling technologies from technologies carried as experiments.**

A 0A launch is a one-way commitment of the spacecraft, launch expenditure, and associated external risks. It does **not**, however, make the downstream 0B investment irreversible. These are different decisions and need different assurance cases.

This is a **property and executive decision**: it defines readiness requirements and who may authorise commitments. The engineering problem is largely complicated; the performance of novel extraction and processing technologies remains experimental.

The relevant unit is therefore **the authorised activity and its consequences**, not whether a milestone happens to sit inside Phase 0A.

## 2. Criteria and weights

### Non-compensable requirements

No weighted benefit may override:

- Flight safety, licensing, launch-provider requirements, or protection of other spacecraft.
- Accepted D-02’s **TRL 6 in a relevant environment, without waivers, for project-ending technologies at KDP-0B**.
- An explicit readiness decision before irreversible flight commitments; passing the MTR alone cannot authorise launch.

### Weighted preferences

Weights below are proposed **swing weights**, not empirical measurements. Each refers to improvement across the stated range.

| Criterion | Range being valued | Weight | Why this swing matters |
|---|---|---:|---|
| **C1. Assurance proportional to consequence** | A phase-wide threshold that misses irreversible risks → decision-specific evidence that controls them | 35% | Largest swing: an otherwise economical rule is unacceptable if it permits poorly understood mission-loss or external hazards. |
| **C2. Learning and option preservation** | Require maturity before the experiment that creates it → enable bounded experiments while retaining cancellation options | 30% | D-01 funds a capability programme; suppressing useful learning can defeat 0A’s purpose. |
| **C3. Cost and schedule proportionality** | Blanket maturation and testing → targeted work on consequential uncertainties | 20% | Premature qualification can consume the budget meant to resolve feasibility. |
| **C4. Auditability and implementability** | Ambiguous milestone labels and discretionary exceptions → clear classifications, evidence and decision rights | 15% | The rule must survive delivery pressure and differing interpretations across projects. |

## 3. Options

**A. Null: leave D-02 and the panel split unchanged.**  
Argument: avoids reopening an accepted decision; project reviews could resolve details.  
**Reject:** the ambiguity concerns spending and launch authority, not merely terminology. Different projects could legitimately implement incompatible rules.

**B. Blanket flight-project thresholds.**  
Require every critical scout/pathfinder technology to reach TRL 6 at its PDR and TRL 8 before launch; restrict 4–5 to downstream 0B development.  
Argument: clear and conservative for operational flight functions.  
**Reject as a blanket rule:** it can require an experimental payload to demonstrate the maturity that its flight is intended to establish. It also unnecessarily excludes reversible development of 0A flight technologies from the 4–5 tranche framework.

**C. Programme-level interpretation only.**  
Apply TRL 4–5 at the MTR and leave flight readiness entirely to existing project processes.  
Argument: minimal amendment and no duplication of standard reviews.  
**Reject on current evidence:** the supplied record does not establish that binding, adequate flight-project standards already cover the gap. This could become acceptable if those standards are produced.

**D. Activity- and function-specific amendment — recommended.**  
Keep 4–5 for reversible development releases; impose distinct flight-project maturity requirements; permit explicitly bounded experimental technologies below those flight-enabling thresholds.

The experiment provision is **not** a waiver of KDP-0B’s no-waiver requirement.

## 4. Assessment matrix

Scores: 1 = poor, 5 = strong. These are transparent judgments for discussion, not measured performance.

| Option | C1: Assurance 35% | C2: Learning 30% | C3: Proportionality 20% | C4: Auditability 15% | Weighted score |
|---|---:|---:|---:|---:|---:|
| A. Null | 2 | 3 | 3 | 1 | **2.35** |
| B. Blanket flight thresholds | 4 | 1 | 1 | 4 | **2.50** |
| C. Programme interpretation only | 3 | 4 | 4 | 2 | **3.35** |
| D. Function-specific amendment | 5 | 4 | 4 | 4 | **4.35** |

A high score cannot cure failure of a non-compensable requirement. Option C’s eligibility depends on evidence of the existing flight-governance regime.

D’s principal weakness is classification overhead and the possibility of relabelling essential functions as “experiments.” Its advantage disappears unless that boundary is independently reviewed.

## 5. Sensitivity vs trade-off points

### Sensitivity points — factual matters that could change implementation

1. **Payload–spacecraft coupling.** Can experimental failure compromise attitude control, power, communications, containment or disposal? If yes, more of the payload belongs within flight-enabling assurance.
2. **Minimum useful mission return.** Is a scout collecting operationally essential target data, or testing uncertain instruments? Losing the former may invalidate the mission even without creating a safety hazard.
3. **What “PDR” authorises.** If irreversible procurement occurs earlier, the relevant readiness decision must also occur earlier.
4. **Existing mandatory standards.** A binding project assurance plan could make a D-02 clarification sufficient instead of a substantive amendment.

### Trade-off points — owner value judgments

- **Learning versus mission-success assurance:** how much probability of an inconclusive pathfinder is acceptable for a lower-cost, earlier experiment?
- **Schedule versus ground maturation:** when does another ground test cost more option value than it buys in risk reduction?
- **Programme concentration versus diversification:** is one high-assurance pathfinder preferable to several cheaper, explicitly riskier experiments?

TRL cannot settle these values questions. In particular, **a TRL number is not a probability of mission success**.

## 6. Evidence certainty

GRADE labels below describe confidence in the evidence base, adapted to this engineering-policy decision.

| Key claim | Evidence and certainty | Likelihood versus confidence |
|---|---|---|
| D-01 and D-02 establish capability funding and consequence-sensitive stringency | **High**, for the decision text supplied in the question; underlying repository files were not independently inspected | High confidence in this interpretation; no probabilistic claim needed. |
| TRL alone does not establish flight readiness | **High**: NASA’s *Systems Engineering Handbook*, NASA/SP-2016-6105 Rev 2, distinguishes technology maturity from broader verification, validation and technical reviews | High confidence; numerical failure likelihood cannot be inferred from TRL. |
| A blanket TRL 8-before-launch rule can obstruct technology-demonstration missions | **Moderate**: established TRL definitions distinguish qualification from operational demonstration, but suitability depends on the technology and demonstration design | High confidence that the conflict can occur; frequency in Dyson is unknown. |
| TRL 6 by PDR is a sound default for flight-enabling critical technologies | **Moderate** as an engineering policy recommendation; not asserted as a universal requirement for every flight project | Moderate confidence in applicability; no Dyson-specific schedule or reliability estimate available. |
| The recommended split will reduce unnecessary cost relative to blanket thresholds | **Low**: plausible engineering-economic judgment without project work breakdowns or test costs | Direction is plausible; magnitude and likelihood are unquantified. |

The published panel disagreement is evidence of unresolved governance, not evidence that any particular maturity threshold guarantees success.

## 7. Key assumptions

| Assumption | Evidence that would falsify it | Effect on ruling |
|---|---|---|
| Some experimental functions can fail without threatening the host or external parties | Hazard analysis, interface testing or common-cause analysis shows uncontained failure effects | Reclassify affected functions as flight-enabling; require isolation, redesign or maturation. |
| Useful learning can survive experimental underperformance | Test design shows failure produces no discriminating data or recoverable diagnostics | Reject or redesign that demonstration; low maturity is not itself a justification to fly. |
| MTR releases can remain bounded | Contract terms show approval commits most lifecycle expenditure or unavoidable flight obligations | Treat that release as an irreversible commitment and move assurance earlier. |
| An independent reviewer can police the experimental boundary | Governance assigns classification solely to the delivery team, without review authority | Do not permit the experimental provision until governance is corrected. |

**ACH ranking, least disconfirmed first:**

1. **Function-specific readiness:** best fits both D-02’s reversibility principle and the purpose of demonstration missions.
2. **Existing flight standards already close the gap:** plausible, but not established by the supplied record.
3. **All 0A flight-critical technologies require identical maturity:** weakened by the distinction between experimental success and safe spacecraft operation.
4. **An internal 0A label makes every milestone reversible:** contradicted by launch and irreversible procurement commitments.

Evidence that would change my recommendation includes a binding flight standard already incorporated into D-02, a pathfinder architecture with no separable experimental functions, or contract evidence that the supposed reversible tranches are effectively whole-mission commitments.

## 8. Decision, warrant, accepted downside

### Proposed D-02 amendment

> **TRL 4–5 applies to bounded, reversible 0A development and funding milestones; it does not constitute flight authorisation.**
>
> Each scout and pathfinder shall identify:
> 1. flight-enabling critical technologies whose failure defeats the approved minimum mission or creates unacceptable external consequences; and
> 2. experimental technologies whose uncertain performance is the purpose of the demonstration.
>
> Flight-enabling critical technologies shall demonstrate TRL 6 in their documented relevant environments by project PDR, or before an earlier irreversible implementation commitment. Flight hardware shall complete applicable qualification, acceptance, integration and operational-readiness requirements before launch; TRL 8 is the target maturity for the completed flight-enabling system.
>
> Experimental technologies may fly below those maturity levels only under an approved demonstration assurance case that bounds failure effects, establishes useful learning outcomes, verifies safe interfaces and operations, and explicitly accepts experiment failure risk. This provision does not relax launch safety or licensing requirements.
>
> At KDP-0B, every project-ending technology remains subject to TRL 6 in a relevant environment, without waivers. A 0A flight or launch approval does not itself establish this maturity.

This preserves Claude’s concern about flight-project discipline, while retaining Gemini/GPT’s interpretation of the MTR as a tranche decision. It rejects both a programme-wide flight-readiness shortcut and a universal requirement that experimental subjects be mature before their demonstration.

**Accepted downside:** additional classification and assurance work, possible PDR delays, and the possibility that an approved experimental mission returns less learning than planned. Those costs are preferable to either hidden flight risk or unnecessary pre-flight maturation.

## 9. Consequences

1. **Amend D-02 explicitly.** Record the change in `decisions.md` and align the gate proposal and baseline. An interpretation alone would leave a materially important exception implicit.
2. **Separate the MTR from flight authorisation.** The MTR may fund development toward a maturity target; it may not substitute for PDR, qualification or launch-readiness decisions.
3. **Use a technology–function–gate register.** For each retained technology, record criticality, environment, current evidence, next authorised activity, expenditure exposure and failure disposition. Do not assign identical requirements solely from a technology identifier.
4. **Do not make TRL 5 circular.** A demonstration intended to establish TRL 5 cannot universally require TRL 5 beforehand. Require sufficient readiness for that test’s hazards and objectives.
5. **Keep route evidence separate.** Funded metallurgy routes must each meet their applicable continuation criterion; maturity is not averaged across routes.
6. **Preserve D-01’s option.** A successful scout can inform target selection without authorising 0B. An unsuccessful experiment can justify redesign, termination or the accepted **“0A only, Earth supply”** fallback.

**Final decision — Y-statement:** In the context of D-01’s capability programme and D-02’s consequence-sensitive gates, facing ambiguous treatment of 0A flight projects, we chose a function-specific amendment separating reversible development releases, flight-enabling readiness and bounded experiments, to achieve useful learning without weakening irreversible-commitment assurance, accepting additional governance and explicit experiment-failure risk. **Warrant:** readiness must match the consequences of the authorised action, not its phase label. **Qualifier:** this holds only where experimental failure is demonstrably bounded and the learning case is credible. It enables tailored scout/pathfinder tranches, constrains flight authorisation, and leaves KDP-0B’s no-waiver requirement intact.