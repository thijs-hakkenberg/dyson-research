---
questionId: "rq-0-72"
questionSlug: "composite-technology-trl-rule"
type: "discussion-conclusion"
generatedBy: "claude-opus-5-5"
generated: "2026-10-17"
framework: "18f503fe4ec6"
roundCount: 1
terminationReason: "unanimous-conclude"
role: "alternate synthesis"
---

## Summary

The panel answered in one round. All three models (Claude Opus 5.5, Gemini 3.1 Pro, GPT-6.1 Sol) rejected three options:

- averaging or any other arithmetic on ordinal TRLs;
- the null option of leaving the split unresolved;
- a headline that conceals an unvalidated critical function.

All three treated this as a programme-wide property decision in the *complicated* domain. They also agreed the rule's rigour should follow D-02's asymmetry, because the rule feeds the one-way, no-waiver KDP-0B gate.

Claude and Gemini both recommended a hybrid. The weakest critical sub-rating acts as an upper bound, and a separate integration assessment can only hold the headline at that bound or lower it. Claude specified this most fully as rules R1–R7:

- a TRL 4 ceiling until an integrated article of the rated configuration has been tested;
- downward-only judgment, with a named finding required for each level below the cap;
- an evidence-attribution rule (R4), under which integrated test evidence re-rates the part before the cap is applied.

GPT recommended configuration-specific integration assessment with a mandatory critical-function evidence constraint, and explicitly not an automatic minimum. Under GPT's rule, a lower constituent rating must stay visible and be reconciled in one of three ways: by applicable evidence, by a "justified scope distinction", or by reducing the composite claim.

The votes converged on Claude's response, which received three APPROVEs; GPT said R4 stops stale component ratings from imposing artificial limits. Two residual differences remain:

- **Scope distinction.** Whether a lower critical rating can be set aside by a justified scope distinction without being updated. Claude called this an escape hatch at a no-waiver gate.
- **The TRL 4 ceiling.** Whether a blanket ceiling without an integrated article is justified. GPT called "integrated article" underspecified; Claude answered with a proposed definition (S2).

The models also differed on how T26 fits. Gemini asserted the rule retroactively justifies the ruling. Claude flagged this as an unverified assumption (A4). GPT treated preserving T26 as a must and did not reassess it.

## Decision record

The panel partially converged. The votes favour the bounded-integration position, but GPT's written position differs on how lower ratings may be reconciled. Both positions are recorded.

**Position 1: bounded integration assessment (Claude Opus 5.5; Gemini 3.1 Pro in a less specified form, "Headline = min(Integration TRL, Lowest Critical Sub-component TRL)")**

> In the context of a Phase 0 TRL baseline whose composite ratings feed a one-way KDP-0B gate with no waivers, facing a panel split between "cap at the weakest part" and "assess the integration", we chose a bounded integration assessment. The weakest critical sub-rating and a ceiling that applies when no integrated article exists set upper bounds. A criteria-based integration judgment sets the headline at or below them. We did this to achieve headlines that cannot overstate readiness yet still fall when mature parts are combined in unproven ways. We accept extra assessor effort, about ±1 level of judgment variance below the cap, and occasional under-rating of benign integrations.

- **Warrant (Claude):** the minimum is a valid upper bound, because a system cannot be more demonstrated than its least-demonstrated essential function. Under R4, system evidence that would justify exceeding the bound also raises the bound. The minimum is not a valid estimate, because integration adds failure modes. So the bound is mechanical and the estimate is judged.
- **Warrant (Gemini):** a system cannot operate in a relevant environment if a critical piece cannot, and it cannot operate if the pieces cannot work together.
- **Qualifier (Claude):** the rule holds where critical functions can be enumerated and attributed. Overall confidence is moderate, and confidence in judgment reproducibility is low.
- **Accepted downside:** assessor effort and false-negative cost, which D-02 already chose to pay (Claude). Heavier interface documentation and testing (Gemini).

**Position 2: configuration-specific integration assessment with a critical-function evidence constraint (GPT-6.1 Sol)**

> In the context of Project Dyson's capability programme and irreversible KDP-0B commitments, facing conflicting rules for composite maturity, we chose configuration-specific integration assessment with mandatory critical-function evidence. We did this to achieve defensible and auditable readiness claims. We accept greater assessment effort.

- **Warrant:** maturity is established by applicable demonstration, not by arithmetic over labels. Integration success cannot erase an unvalidated critical dependency.
- **Qualifier:** a lower component rating that is current, applicable and reflects an undemonstrated critical function "does cap the defensible headline in practice".
- **Accepted downside:** more engineering judgment, documentation and independent review than a mechanical minimum.

GPT voted APPROVE on Claude's response. This suggests GPT may accept Position 1 if R4 covers its stale or scope-mismatched rating concern. Claude records the remaining disagreement as follows: if GPT holds that a system can exceed its weakest critical part without that part's sub-rating being updated, the two positions still differ.

## Decision-quality audit

| Response (Round 1) | Votes | Weakest link named | Missing or unsupported scaffold steps | Trade-off points (values, not facts) |
|---|---|---|---|---|
| **Claude Opus 5.5** | APPROVE ×3 (Claude, Gemini, GPT) | Information (Claude, GPT); none (Gemini) | T26 sub-ratings not verified (A4 open). Assessor reproducibility rated low confidence and not yet calibrated. Both are flagged, with a calibration step and an O5 fallback. | T1: auditability vs integration fidelity. T2: false-negative vs false-positive cost, with Claude recommending against forking the rule by gate. |
| **Gemini 3.1 Pro** | REJECT (Claude); NEUTRAL (Gemini, GPT) | Alternatives (Claude); reasoning (Gemini, GPT) | The chosen hybrid was never scored as an option, so the analysis does not support the decision (all three voters). The matrix is qualitative with no aggregation. Weights reflect importance, not swing range. Certainty does not separate likelihood from confidence (Claude). The "absolute gate integrity" claim conflicts with the stated limits of mechanical caps (GPT). T26 is said to be retroactively justified without checking the record (Claude, GPT). | Mechanical strictness vs engineering accuracy (O1 vs O2). |
| **GPT-6.1 Sol** | APPROVE (Gemini, GPT); NEUTRAL (Claude) | Reasoning (Claude); information (GPT); none (Gemini) | The "justified scope distinction" route lets a lower critical rating be reconciled without a mechanical cap, yet Option B scores 5 on false-claim prevention (Claude). Listing "preserve T26" as a non-compensable must mixes continuity with technical requirements (Claude). GPT notes it did not inspect the source files independently, and that the consistency gain from B has low certainty and needs a pilot. | Consistency vs assessment effort. Conservatism vs useful maturity information. Breadth vs depth of early 0A testing. |

**Divergences that are values questions:**

- **How much false-negative cost to accept for false-positive protection.** This is the scope-distinction and blanket-ceiling dispute. Claude cites D-02 as having already settled this toward conservatism at KDP-0B.
- **Auditability vs fidelity.** This is how much judgment to allow.

**Divergences that are facts to settle:**

- Whether integrated evidence can always be attributed to parts. This is Claude's A1 falsifier, and it decides whether R4 removes GPT's objection.
- Whether assessors reproduce each other's ratings within ±1 level.
- What the T26 record actually contains.

## Key Points

- **Unanimous:** no averaging, weighting or multiplying of TRLs. Claude cites ordinal measurement and Kujawski's (2013) critique of SRL arithmetic; GPT and Gemini also screened it out.
- **Unanimous:** an unvalidated critical function blocks the system claim.
- **Unanimous:** the null option is rejected because it produces incompatible headlines in one baseline (Claude, GPT) and inconsistency at KDP-0B (Gemini).
- **Unanimous:** component maturity does not establish integration maturity. GPT cites the NASA SE Handbook; Gemini cites aerospace practice; Claude cites the NPR 7123.1 and ISO 16290 definitions at TRL 5 and above, which presuppose integrated configurations.
- **The core disagreement is narrower than it looks.** Claude framed it as whether the minimum is the *estimate* or only a *bound*, and all three treat it as at least a bound in practice. The remaining question is how a lower critical rating may be discharged:
  - Claude: only by updating that rating through evidence (R4).
  - GPT: by evidence, by reducing the claim, or by a justified scope distinction that does not remove a dependency the claimed capability actually requires.
- **Sensitivity points named by all three:** the definition of "critical"; the definition of "integrated article" or assessment boundary (Claude, GPT); configuration identity and environment fidelity (Claude, GPT).
- **Publication.** Claude and GPT converge on publishing, alongside the headline:
  - the configuration ID;
  - critical sub-ratings with evidence pointers;
  - integration findings;
  - the conditions for the next level.

  Claude adds the binding bound (R1 or R2). GPT adds evidence dates, scopes, assessor, reviewer and decision authority. Gemini proposes a tripartite report: integration TRL, lowest critical TRL, and headline.
- **KDP-0B criterion.** Claude's R7 requires headline ≥ 6, every critical sub-rating ≥ 6, and a configuration match. GPT requires every project-ending technology to satisfy D-02 independently, with no portfolio averaging or waiver.

## Unresolved Questions

1. Can a "justified scope distinction" (GPT) discharge a lower critical rating without updating it, or is that a waiver in another form (Claude)?
2. Should a blanket TRL 4 ceiling apply when no integrated article exists? This depends on whether Claude's S2 definition satisfies GPT's objection that the article must follow the claimed level and boundary.
3. Does the T26 record fit the adopted rule? Gemini says yes; Claude says it is unverified; GPT says to preserve the ruling without reassessing it.
4. Do assessors reproduce downward-only judgments within ±1 level? Claude puts this at "about as likely as not", with low confidence.
5. Do R3 downgrades need owner sign-off, or only a documented finding? Claude raised this.
6. Can critical functions be enumerated in advance? Claude's A2 and GPT's assumption table both name this, and both say to treat the criticality list as an output of integration review if it cannot.

## Recommended Actions

1. **Owner rules on the general rule**, choosing between Position 1 (Claude R1–R7, endorsed by vote) and Position 2 (GPT). The decisive sub-question is the scope-distinction route, and GPT's residual disagreement should be recorded as Claude proposed.
2. **Approve definitions.** "Critical function": Claude's S1, under which redundancy counts only if the redundant path is itself rated. "Integrated article": Claude's S2, assessed against GPT's boundary objection.
3. **Run a calibration or pilot exercise.** Claude proposes three assessors rating three composites; GPT proposes a blind reassessment across propulsion, power and processing composites. The result decides between O3/B, a fallback to the mechanical O5, or a simpler default.
4. **Verify T26's sub-ratings and evidence** against the adopted rule, and record exactly which evidence would satisfy the "4 conditional" condition (Claude, GPT).
5. **Adopt the publication fields** common to Claude's R6 and GPT's §9 in `trl-baseline.yaml`. If Position 1 is adopted, add Claude's lint check: headline ≤ the lowest critical sub-rating and within the R2 ceiling.
6. **Budget integrated-article hardware earlier in 0A**, and use the 0A mid-term review for the first integration assessments (Claude).
7. **Monitor triggers for revisiting the rule** (Claude A1–A3; GPT §6–7):
   - integrated evidence that cannot be attributed to parts;
   - unlisted critical functions surfaced by tests;
   - more than a third of composites downgraded without named findings;
   - assessor divergence greater than one level.

```yaml
questionId: "rq-0-72"
topics:
  - id: weakest-part-as-bound-vs-reconcilable
    topic: Whether the lowest critical sub-rating is a hard upper bound or a constraint that can be reconciled
    positions:
      - statement: Headline may not exceed the lowest critical sub-rating; integrated evidence that demonstrates a critical function updates that sub-rating first (R4), so the cap never binds wrongly; integration judgment may only hold at or lower the headline
        models: [Claude Opus 5.5]
        evidence: TRL definitions at 5 and above presuppose integration (NPR 7123.1, ISO 16290); a system cannot be more demonstrated than its least-demonstrated essential function; D-02 already accepts false-negative cost at one-way gates
      - statement: Headline = min(integration TRL, lowest critical sub-component TRL)
        models: [Gemini 3.1 Pro]
        evidence: D-02 no-waiver rule; integration commonly less mature than parts (NASA SE practice)
      - statement: Do not automatically inherit the minimum; lower ratings stay visible and are reconciled by applicable evidence, a justified scope distinction, or reducing the claim; a current, applicable, undemonstrated critical deficiency caps in practice
        models: [GPT-6.1 Sol]
        evidence: Component ratings may concern different configurations, environments or boundaries, or be stale; NASA/SP-2016-6105 Rev 2 on integration maturity
    resolution_status: partially-resolved
    priority: critical
  - id: scope-distinction-escape-hatch
    topic: Whether a justified scope distinction may discharge a lower critical rating at a no-waiver gate
    positions:
      - statement: A scope distinction that releases a critical rating without updating it is an escape hatch at a one-way, no-waiver gate
        models: [Claude Opus 5.5]
        evidence: Vote critique of GPT; D-02 no-waiver requirement
      - statement: Scope distinctions are legitimate provided they do not remove a dependency actually required by the claimed capability
        models: [GPT-6.1 Sol]
        evidence: Scope-mismatched or stale component ratings can mischaracterise maturity (moderate certainty, frequency unknown)
    resolution_status: open
    priority: critical
  - id: integrated-article-ceiling
    topic: Blanket TRL 4 ceiling without a tested integrated article
    positions:
      - statement: Headline capped at 4 without an integrated article of the rated configuration (all critical functions and coupled-load interfaces present, simulations excluded); at most 5 without a relevant-environment test; at most 6 without a system or subsystem model or prototype in a relevant environment
        models: [Claude Opus 5.5]
        evidence: NPR 7123.1 and ISO 16290 TRL definitions; S2 definition
      - statement: "Integrated article" is underspecified; the required article must follow the claimed level and assessment boundary, not an arbitrary whole-system boundary; TRL 6 needs a representative model or prototype in a justified relevant environment
        models: [GPT-6.1 Sol]
        evidence: Assessment-boundary sensitivity (thruster vs cluster)
    resolution_status: partially-resolved
    priority: high
  - id: t26-consistency
    topic: How the T26 ruling (TRL 3, 4 conditional) relates to the general rule
    positions:
      - statement: T26 is retroactively justified because the integration lacked a validated article
        models: [Gemini 3.1 Pro]
        evidence: Asserted, record not checked (flagged by Claude and GPT)
      - statement: Consistency is assumed but unverified (A4); T26 sub-ratings must be checked and reconciled
        models: [Claude Opus 5.5]
        evidence: T26 sub-rating detail not inspected
      - statement: Preserve T26 as ruled, as a non-compensable requirement; the general rule neither upgrades nor changes it
        models: [GPT-6.1 Sol]
        evidence: Supplied owner ruling record (high certainty of what was ruled, not an independent reassessment)
    resolution_status: open
    priority: medium
  - id: judgment-reproducibility
    topic: Whether bounded or traceable integration judgment is reproducible across assessors at acceptable cost
    positions:
      - statement: Downward-only judgment with a named finding per level; reproducibility within ±1 is about as likely as not (low confidence); calibrate, and fall back to the mechanical O5 if variance exceeds one level
        models: [Claude Opus 5.5]
        evidence: No calibration data for this panel
      - statement: Traceability should improve consistency, but magnitude is low certainty; pilot with a blind reassessment and adopt a simpler default if the mechanical minimum gives the same defensible result more cheaply
        models: [GPT-6.1 Sol]
        evidence: Prospective governance judgment; weight sensitivity shows the mechanical option overtakes B only at about 50% weight on economy
    resolution_status: open
    priority: high
  - id: no-arithmetic-aggregation
    topic: Averaging or arithmetic aggregation of TRLs
    positions:
      - statement: Reject averaging, weighting, products and SRL-style matrices because TRL is ordinal
        models: [Claude Opus 5.5, Gemini 3.1 Pro, GPT-6.1 Sol]
        evidence: Ordinal measurement theory; Kujawski (2013) critique of SRL (Claude)
    resolution_status: resolved
    priority: low
  - id: null-option
    topic: Leaving the panel split unresolved
    positions:
      - statement: Reject; produces incompatible headlines and inconsistent KDP-0B evidence, and T26 shows the case-by-case cost
        models: [Claude Opus 5.5, Gemini 3.1 Pro, GPT-6.1 Sol]
        evidence: T26 required a specific owner ruling without a general rule; risk of assessors choosing whichever convention suits them
    resolution_status: resolved
    priority: medium
```