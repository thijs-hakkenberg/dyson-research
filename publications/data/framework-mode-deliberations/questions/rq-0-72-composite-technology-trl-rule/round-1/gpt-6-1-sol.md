---
questionId: "rq-0-72"
questionSlug: "composite-technology-trl-rule"
modelId: "gpt-6-1-sol"
modelName: "GPT-6.1 Sol"
roundNumber: 1
generated: "2026-10-17"
type: "discussion-response"
---

## 1. Frame & decision type

**Recommendation: assess the integration, subject to an explicit critical-function evidence constraint—not an automatic minimum of published component TRLs.**

The headline should describe the maturity of a **named technology, configuration, function set and environment**. An unresolved critical function blocks any headline level whose requirements depend on that function. However, a legacy component rating should not mechanically cap a composite when configuration-specific evidence demonstrates the necessary maturity.

This is a programme-wide **property and governance decision**. The rule is revisable; commitments made using it may not be. Therefore, apply D-02’s asymmetry:

- **Internal 0A milestones:** proportionate evidence at TRL 4–5.
- **KDP-0B:** demonstrated TRL 6 in a relevant environment for every project-ending technology, without waivers.

The engineering assessment is complicated but tractable; defining acceptable residual uncertainty is a governance choice. Neither should be hidden inside a single number.

**Scope limitation:** project-specific facts below come from the supplied decision summaries and source paths, not an independent inspection of those files.

## 2. Criteria and weights

### Non-compensable requirements

No weighted score may override these requirements:

1. No averaging of ordinal TRLs.
2. No unsupported critical function or interface may be concealed by a headline.
3. No dilution of D-02’s KDP-0B requirement.
4. Preserve T26’s current **TRL 3, with TRL 4 conditional** ruling unless new evidence supports a separate change.

### Swing-weighted preferences

Weights describe the value of moving across the stated performance range—not abstract importance.

| Criterion | Performance swing being valued | Weight | Rationale |
|---|---|---:|---|
| **C1: Prevent false maturity claims** | From allowing hidden project-ending gaps to reliably exposing and blocking them | **35%** | Largest swing because false readiness can trigger irreversible expenditure. |
| **C2: Technical validity** | From assigning misleading numbers to accurately characterising configuration-specific maturity | **25%** | Both inflated and unnecessarily depressed ratings misallocate development resources. |
| **C3: Auditability and consistency** | From assessor-dependent conclusions to reproducible evidence-to-claim reasoning | **20%** | A programme-wide rule must survive changes of assessor and supplier. |
| **C4: Assessment and test economy** | From duplicated testing and lengthy adjudication to proportionate evidence reuse | **15%** | Important during a capability programme, but subordinate to valid readiness claims. |
| **C5: Decision continuity** | From reopening accepted decisions to implementing them without substantive reinterpretation | **5%** | Administrative continuity matters, but should not preserve a technically poor rule. |

These are proposed owner preferences, not empirically measured constants.

## 3. Options

**A. Mechanical weakest-critical-part rule, plus a blanket TRL 4 ceiling without an integrated article.**  
Its strongest argument is simplicity: conservative, legible and difficult to manipulate. Reject as the general rule because component ratings may concern different configurations, environments or boundaries. Also, “integrated article” is underspecified: the required article must follow the claimed technology level and assessment boundary, not an arbitrary whole-system boundary.

**B. Configuration-specific integration assessment with a critical-function evidence constraint. — Recommended**  
Assess the composite directly. Require evidence for every critical function and interface at the claimed level. Reconcile lower component ratings explicitly rather than ignoring them or mechanically inheriting them. This combines technical validity with a non-negotiable blocker rule.

**C. Integration-led expert judgment without mandatory critical-function traceability.**  
Its strongest argument is flexibility and low documentation burden. Reject because a successful demonstration can obscure unexercised operating modes, interfaces or failure conditions.

**D. Null option: retain the panel split.**  
Its strongest argument is preserving owner flexibility while experience accumulates. Reject because assessors could select whichever interpretation produces the preferred headline. That creates inconsistent gate evidence and later rework.

**E. Average or weighted-average component TRLs.**  
Its strongest argument is ease of reporting. Reject: ordinal maturity labels are not quantities whose average demonstrates integration or resolves a critical deficit.

## 4. Assessment matrix

Scores: **1 = poor; 5 = strong**. These are transparent engineering judgments, not measured performance. Totals are weighted scores out of 100; they do not override the requirements above.

| Option | C1 35% | C2 25% | C3 20% | C4 15% | C5 5% | Total | Disposition |
|---|---:|---:|---:|---:|---:|---:|---|
| A. Mechanical minimum and ceiling | 4 | 3 | 4 | 4 | 4 | **75** | Reject as general rule |
| **B. Integration + evidence constraint** | **5** | **5** | **4** | **3** | **5** | **90** | **Select** |
| C. Unstructured integration judgment | 3 | 4 | 2 | 4 | 4 | **65** | Reject |
| D. Retain split | 2 | 2 | 1 | 3 | 3 | **40** | Reject |
| E. Average ratings | 1 | 1 | 3 | 5 | 2 | **41** | Fails requirements |

The main uncertainty is whether B’s traceability requirements achieve the anticipated consistency without excessive assessment cost. A pilot should test that, rather than treating the scores as proof.

## 5. Sensitivity vs trade-off points

### Sensitivity points — evidence can resolve these

- **Assessment boundary:** changing from a thruster to a propulsion cluster changes which interactions require demonstration.
- **Meaning of “critical”:** omitting a shared power, thermal, control or contamination interface can invalidate the assessment.
- **Environment fidelity:** a nominal laboratory run may not demonstrate the relevant combined loads or operating modes.
- **Evidence applicability:** a component’s old TRL may be either genuinely limiting or simply stale and out of scope.

### Trade-off points — owner values must resolve these

- **Consistency versus assessment effort:** mandatory traceability costs engineering time but reduces discretionary claims.
- **Conservatism versus useful maturity information:** a blanket minimum is simpler, but can obscure demonstrated progress.
- **Breadth versus depth of early testing:** 0A can investigate more alternatives or retire fewer uncertainties more thoroughly.

The recommendation is reasonably robust to ordinary weight changes. At the scores above, A overtakes B only if assessment economy becomes dominant—for example, approximately **50% weight**, with the other weights reduced proportionally. That would be a material departure from D-02’s risk posture.

## 6. Evidence certainty

GRADE labels below are **adapted to engineering evidence**; they are not clinical GRADE assessments.

| Key claim | Evidence and certainty | Confidence and likelihood |
|---|---|---|
| KDP-0B requires TRL 6 for project-ending technologies, without waivers | **High** for the stated policy: supplied accepted D-02 record | High confidence in the requirement; no probability estimate is applicable. |
| Component maturity alone does not establish integration maturity | **High**: established systems-engineering principle, reflected in NASA’s *Systems Engineering Handbook*, NASA/SP-2016-6105 Rev 2 | High confidence; failure likelihood remains configuration-dependent. |
| A blanket minimum can mischaracterise maturity when scopes differ | **Moderate**: strong logical basis, but no supplied Dyson case comparison | Moderate confidence in programme-wide significance; frequency unknown. |
| Option B will improve consistency at acceptable cost | **Low**: prospective governance judgment, not demonstrated programme performance | Moderate confidence in direction; low confidence in magnitude. No numerical likelihood justified. |
| T26 remains TRL 3, conditionally 4 | **High** for the reported ruling | High confidence in what the supplied record states, not an independent reassessment of T26. |

**Evidence that would change the ruling:** a blind reassessment exercise across representative propulsion, power and processing composites showing that B produces materially inconsistent conclusions, admits unsupported critical claims, or costs substantially more without improving validity. Conversely, repeated cases in which A produces the same defensible result at much lower cost would support adopting a simpler default.

## 7. Key assumptions

| Assumption | Falsifying evidence | Response if falsified |
|---|---|---|
| Critical functions and interfaces can be identified with reasonable completeness | Hazard analysis or testing repeatedly discovers omitted project-ending dependencies | Strengthen functional and interface analysis; withhold affected claims. |
| Assessors can trace evidence to a defined configuration | Missing provenance, uncontrolled substitutions or conflicting test configurations | Require configuration control before accepting the headline. |
| Some low component ratings are stale or scope-mismatched | Review shows all disputed ratings are current and directly applicable | Apply their demonstrated limitations; the practical result may equal the minimum. |
| B can be audited consistently | Independent assessors produce materially different ratings from the same evidence | Tighten criteria and exemplars; consider a conservative interim default. |

**ACH ranking—least disconfirmed, provisionally:**

1. **Integration maturity must be assessed directly, with critical-function constraints.** Best accommodates both interface failures and applicable evidence reuse.
2. **The lowest critical component rating is always the correct headline.** Not disproven for every case, but weakened by scope mismatch and its inability to establish integration maturity.
3. **Successful integration testing alone establishes maturity.** Most vulnerable to untested functions, environments and operating modes.

This ranking is conceptual, not the result of a completed Dyson evidence trial.

## 8. Decision, warrant, accepted downside

Adopt the following rule:

> **Composite TRL rule:** Assign the headline TRL to a defined technology configuration using evidence applicable to its required functions, critical interfaces and environment. Do not average constituent TRLs or automatically inherit their minimum. Every critical function and interface shall have evidence sufficient for the claimed level. Any unresolved deficiency blocks that level.
>
> A lower constituent rating shall remain visible and shall be reconciled through applicable evidence, a justified scope distinction, or a reduction of the composite claim. A scope distinction shall not remove a dependency actually required by the claimed capability.
>
> TRL 6 requires demonstration of an appropriately representative system/subsystem model or prototype in a justified relevant environment. Analysis and constituent tests may support, but shall not substitute for, that demonstration.
>
> At KDP-0B, every project-ending technology must satisfy D-02 independently; no portfolio average, compensating strength or waiver is permitted.

**Warrant:** maturity is a claim about demonstrated technological capability. Consequently, evidence applicability—not arithmetic over labels—must determine the claim. Equally, integration success cannot erase an unvalidated critical dependency.

**Qualifier:** when a lower component rating is current, applicable and reflects a critical function not demonstrated at the proposed composite level, it **does cap the defensible headline in practice**.

**Accepted downside:** B requires more engineering judgment, documentation and independent review than a mechanical minimum.

## 9. Consequences

Publish each composite with:

- headline TRL and configuration identifier;
- constituent ratings, scopes and evidence dates;
- critical-function/interface evidence map;
- relevant-environment justification;
- unresolved blockers and conditions for the next level;
- assessor, independent reviewer and decision authority.

Use existing evidence wherever applicable; do not require a full flight article or full mission-duration test merely because the assessment concerns a composite. Conversely, do not accept separate component tests as proof that critical interactions work.

For **T26**, retain **TRL 3, with TRL 4 conditional**. This general rule neither upgrades it nor retroactively changes the owner’s ruling. Record precisely which evidence satisfies the condition.

This decision **enables** consistent baseline publication and test planning; **constrains** headline upgrades and KDP-0B evidence acceptance; and leaves the target, demand, economics and licence gates independent. It does not displace D-01’s demand-sized 0B option or the fallback **“0A only, Earth supply.”**

**Final decision — Y-statement:** In the context of Project Dyson’s capability programme and irreversible KDP-0B commitments, facing conflicting rules for composite maturity, we chose configuration-specific integration assessment with mandatory critical-function evidence, to achieve defensible and auditable readiness claims, accepting greater assessment effort. **Warrant:** applicable demonstration establishes maturity; labels alone do not. **Qualifier:** unresolved applicable critical deficiencies remain binding blockers. This enables evidence-led upgrades while constraining unsupported headlines and irreversible commitments.