---
questionId: "rq-0-64"
questionSlug: "t26-comms-trl-rating-object"
modelId: "gpt-6-1-sol"
modelName: "GPT-6.1 Sol"
roundNumber: 1
generated: "2026-10-17"
type: "discussion-response"
---

## 1. Frame & decision type

**T26 should assess the architecture-required, end-to-end communications and resilient command service—not the maturity of its best-established components.** Publish component maturity alongside it so that an integration gap is not mistaken for immature radio technology.

The assessed object should be:

> A configuration-controlled service providing communications, navigation-support interfaces, and authenticated command for the authorized Phase 0 fleet envelope, including disruption recovery and security lifecycle management, while preserving local safety independence from Earth.

Its boundary includes flight and ground endpoints, transport, scheduling, trust infrastructure, operational procedures, and their critical interfaces. It need not absorb the whole navigation subsystem or local autonomy technology; those interfaces require explicit ownership and evidence.

This is a **property decision** about the meaning of the baseline rating, coupled to an **executive decision** about Phase 0A funding and KDP-0B evidence. The rating can be revised readily; procurement and gate commitments based on an inflated rating are harder to reverse.

Apply the same rule to other composite technologies in `reconciliation/phase-0/trl/`: **define the assessed configuration and required environment before assigning maturity.** Split an inventory item when its constituent capabilities have materially different gate obligations.

## 2. Criteria and weights

These are proposed **swing weights**, referring to the actual differences among assessment policies—not probabilities or measures of technical maturity.

| Criterion | Weight | Swing being valued, and why |
|---|---:|---|
| **C1. Fidelity to architectural dependence** | 35% | From ignoring an essential integration dependency to explicitly assessing the service whose failure threatens Phase 0. This is the largest consequential difference. |
| **C2. Gate and assurance usefulness** | 25% | From no defensible acceptance decision to a traceable demonstration obligation under D-02, with conditional linkage to D-03. |
| **C3. Diagnostic and investment value** | 20% | From one opaque number to identifying exactly which integration, security, or capacity gaps require funding. This can prevent expensive redevelopment of mature elements. |
| **C4. Assessment burden and schedule** | 10% | From maintaining existing summaries to operating a controlled evidence register and integrated assessment. Important, but cheaper than discovering a command-service gap after commitment. |
| **C5. Evidence transparency** | 10% | From conflating heritage, assumptions, and demonstrations to explicitly distinguishing them. This supports reproducibility and future reassessment. |

**Non-compensable constraints:** an adopted baseline must state its rating object, cite supporting demonstrations, and preserve D-02 obligations. A high weighted score cannot excuse an unsupported TRL claim.

## 3. Options

**A. Null: retain the panel range and unresolved interpretations.**  
Argument: avoids premature closure and preserves disagreement.  
Reject: leaves the gate authority unable to tell whether T26 needs a funded maturation program.

**B. Heritage-led headline TRL 6–7.**  
Argument: DSN, relay operations, and disruption-tolerant networking provide substantial relevant heritage; reuse should be credited.  
Reject: those demonstrations do not, by themselves, establish the specified authenticated fleet service. This option remains useful for component sub-ratings.

**C. Integrated-service headline only.**  
Argument: directly represents architectural dependence and prevents averaging away integration gaps.  
Reject as the complete reporting policy: a low headline alone obscures extensive heritage and can drive unnecessary reinvention.

**D. Sub-ratings only, without a service headline.**  
Argument: avoids compressing heterogeneous evidence into one number.  
Reject as the baseline policy: decision-makers still need an explicit disposition of the integrated dependency. A dashboard alone can leave that responsibility unowned.

**E. Integrated-service headline plus evidence-linked sub-ratings and a gate assurance case. — Recommended**  
Argument: combines an honest architectural maturity statement with actionable investment information. Its disadvantage is additional configuration and evidence-management work.

## 4. Assessment matrix

Scores are deliberative judgments: **0 = poor, 4 = strong**. Weighted totals are rounded comparison aids, not measured truths.

| Option | C1: Fidelity 35% | C2: Gate utility 25% | C3: Diagnostic value 20% | C4: Low burden 10% | C5: Transparency 10% | Weighted /100 |
|---|---:|---:|---:|---:|---:|---:|
| A. Keep unresolved panel range | 0 | 0 | 1 | 4 | 0 | 15 |
| B. Heritage-led headline | 1 | 1 | 3 | 4 | 1 | 41 |
| C. Integrated headline only | 4 | 4 | 1 | 2 | 3 | 79 |
| D. Sub-ratings only | 3 | 2 | 4 | 2 | 3 | 71 |
| **E. Integrated headline + sub-ratings** | **4** | **4** | **4** | **2** | **4** | **95** |

The important result is not “95.” It is that E preserves the architectural dependency **and** distinguishes reuse from new development.

## 5. Sensitivity vs trade-off points

### Sensitivity points: facts that could change the implementation or rating

- **Fleet concurrency:** simultaneous command-critical sessions versus mostly queued traffic changes scheduling, capacity, and recovery requirements.
- **Traffic budget:** without command deadlines, telemetry volumes, navigation-support needs, and allocated link capacity, there is no quantitative qualification envelope.
- **Orbit-specific outages:** conjunction and solar-exclusion durations determine storage, command validity, key lifecycle, and recovery demands.
- **Security architecture:** authenticated transport is insufficient if ground authorization, onboard execution, trust anchors, or recovery procedures create weaker paths.
- **Demonstration availability:** an existing representative integrated prototype could materially raise the present rating and shorten Phase 0A work.

### Trade-off points: values decisions, not facts to settle

- **More pre-gate assurance versus earlier commitment and lower near-term expenditure.**
- **Maximum initial fleet capability versus a smaller, independently viable initial operating envelope.**
- **Stronger compromise containment versus recovery complexity and operational availability.**
- **Headline simplicity versus faithful representation of heterogeneous maturity.**

The recommendation remains preferred under substantial reweighting unless low reporting burden is valued above identifying an architecture-critical gap. No numerical weighting should override D-02.

## 6. Evidence certainty

The following uses **GRADE-style certainty labels adapted to engineering evidence**, not clinical-study grading. Confidence concerns the strength of the conclusion; likelihood concerns whether an event will occur.

| Key claim | Certainty and confidence | Likelihood statement |
|---|---|---|
| Interplanetary RF communications have extensive operational heritage. | **High certainty; high confidence.** DSN operations are direct evidence. | Not a forecast. |
| DTN has been demonstrated in deep space. | **High certainty; high confidence** for that bounded claim: NASA/JPL reported DINET testing on EPOXI in 2008. This is not evidence of the complete T26 service. | Not a forecast. |
| The supplied evidence does not establish the specified integrated authenticated fleet service at TRL 6. | **Moderate certainty; high confidence as an evidence-register finding.** The inventory may be incomplete. | No defensible probability that an undiscovered precedent exists. |
| Authentication lifecycle and outage recovery deserve explicit maturation work. | **Moderate certainty; moderate confidence.** Supported by the described gaps, but detailed design and threat analysis are absent. | Failure probability cannot yet be quantified. |
| T26 can reach TRL 6 within Phase 0A. | **Low certainty; low confidence** until configuration, facilities, resources, and schedule are defined. | Do not convert the panel’s 1–5-year estimates into a calibrated forecast. |
| Command security will be a licence condition under D-03. | **Low certainty.** Jurisdiction and regulator requirements are not established here. | Treat as a conditional constraint, not an assured outcome. |

**Sources and limits:** NASA’s *Systems Engineering Handbook*, NASA/SP-2016-6105 Rev. 2, supplies the TRL framework; NASA/JPL’s 2008 DINET reporting supplies a specific deep-space demonstration; CCSDS *Space Data Link Security Protocol* and its *Extended Procedures* supply standards, **not proof of deployment on a named mission**. Gemini’s flight-heritage claim therefore remains uncredited until a traceable mission record is supplied.

One correction matters: under NASA’s conventional definitions, **TRL 4 is laboratory validation; TRL 5 introduces a relevant environment; TRL 6 requires a representative system/subsystem model or prototype demonstrated in a relevant environment.** An integrated laboratory breadboard should not be rejected for TRL 4 solely because it lacks the TRL 5 environment.

## 7. Key assumptions

| Assumption | Evidence that would falsify it |
|---|---|
| The integrated command service is essential to the authorized Phase 0B mission. | A validated alternative architecture meeting mission and licensing obligations without it. |
| Existing components can supply most underlying communications functionality. | Interface, capacity, radiation, timing, or security analysis showing extensive redesign is required. |
| A defensible relevant-environment demonstration can combine representative hardware, network emulation, heritage evidence, and operational exercises. | Identification of a critical phenomenon or interface that cannot be represented or bounded without additional flight evidence. |
| The required envelope extends to 29 assets unless formally reduced. | An approved architecture and staged operating concept establishing a smaller, sufficient KDP-0B envelope. |
| Safety remains locally independent of Earth during outages. | Hazard analysis finding any safety-critical action that requires an Earth response within the stated delay or blackout. |

**ACH ranking—least disconfirmed explanations of the rating disagreement:**

1. **Different assessment objects:** strongest fit to the panel’s stated reasoning.
2. **Missing evidence for a potentially mature integrated service:** plausible; requires an evidence search.
3. **A fundamentally immature communications technology:** weakest fit to the extensive RF and operational heritage.

This ranking supports a targeted integration program, not wholesale communications research.

## 8. Decision, warrant, accepted downside

Adopt **Option E**.

### Baseline entry

Record:

- **Assessed object:** the defined integrated service and authorized operating envelope.
- **Current disposition:** **provisional TRL 3 working assessment; TRL 4 not yet evidenced for the integrated configuration**, pending evidence audit.
- **Qualifier:** missing documentation does not itself prove TRL 3. That level also requires evidence of its applicable exit criteria; if absent, record “not demonstrated/evidence incomplete.”
- **Sub-ratings:** retain separate, configuration-specific entries for RF links, transport/DTN, navigation-support interfaces, scheduling/capacity, authenticated command and key management, and disruption recovery.

Do not average sub-ratings, and do not mechanically take their minimum. The service rating depends on demonstrated integration of the critical functions.

### Risk classification

Use **architecture-change as the primary consequence class**, with explicit branches:

- **Cost/schedule increase:** adequate service is achievable through additional resources or a slower cadence.
- **Architecture change:** authorized fleet scale, operations, or command topology must change.
- **Project-ending for the proposed Phase 0B configuration:** no trustworthy command service or acceptable licensing path can be demonstrated.

Severity is not probability. This classification does not assert that failure is likely.

### Accepted downside

The policy creates extra assurance work and may expose a funding or schedule gap earlier. It also risks conflating overall readiness with technology maturity unless TRL, operational readiness, cybersecurity assurance, and licensing compliance remain separate records.

## 9. Consequences

### KDP-0B criterion

For any T26 capability whose absence is project-ending under D-02, require:

> **TRL 6 evidence for the approved integrated configuration and operating envelope, plus a separately accepted operational/security assurance case and closure of applicable licensing conditions.**

The demonstration package should include:

1. **A frozen qualification envelope:** fleet concurrency, traffic, command deadlines, storage, navigation-support interfaces, allocated network access, and target-specific outage cases.
2. **A representative prototype:** flight/ground command boundaries, onboard processing, persistent storage, scheduling, and security implementation representative where critical.
3. **Delay and disruption testing:** the specified 1–25-minute light time, outages, asymmetric links, corrupted or duplicate messages, interrupted transfers, and simultaneous recovery demand.
4. **Command lifecycle testing:** authorization, replay protection, stale-command handling, key rollover, revocation, reboot/state loss, compromised-node containment, and recovery after long disconnection.
5. **Measured acceptance results:** delivery latency, backlog clearance, storage margins, command integrity and availability, and behavior outside the qualified envelope.
6. **Safety evidence:** hazardous operations remain locally safe without Earth intervention; restoration does not execute obsolete commands or bypass authorization.
7. **Independent review:** traceable predictions, results, discrepancies, residual risks, and configuration identity.

Neither full-scale flight deployment nor encryption alone is a universal TRL-6 prerequisite or sufficient proof. The relevant environment must be justified function by function.

Assign one service owner, establish a targeted heritage-evidence search, and fund an early integrated breadboard before committing to a costly demonstration campaign. Reserve a smaller fleet envelope as a real option—but accept it only through an approved architecture change showing that Phase 0B remains viable. Published sub-ratings should retain the panel’s unresolved evidence disagreements rather than average them away.

**Final decision—Y-statement:** In the context of the Phase 0 TRL re-baseline, facing mature communications components but unproven integrated fleet-command assurance, we chose an integrated-service headline with evidence-linked sub-ratings, to achieve an auditable D-02 gate and targeted maturation investment, accepting additional Phase 0A assurance effort and possible schedule pressure.

**Warrant:** component heritage supports reuse, but does not establish the behavior of their required integration. **Qualifier:** the provisional rating must change when configuration-specific evidence satisfies the relevant exit criteria. This decision enables a funded demonstration plan and constrains KDP-0B approval, fleet-envelope selection, and any D-03 licensing claim.