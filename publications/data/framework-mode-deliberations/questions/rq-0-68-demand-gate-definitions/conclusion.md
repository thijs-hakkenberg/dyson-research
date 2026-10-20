---
questionId: "rq-0-68"
questionSlug: "demand-gate-definitions"
type: "discussion-conclusion"
generatedBy: "gpt-6-1-sol"
generated: "2026-10-17"
framework: "18f503fe4ec6"
roundCount: 1
terminationReason: "unanimous-conclude"
---

## Summary

Claude Opus 5.5, Gemini 3.1 Pro and GPT-6.1 Sol converged in Round 1 on interpreting **“within 3×” as a quantity-coverage test, not a timing tolerance**: accepted annual demand must be at least one-third of the corresponding proposed nameplate output. GPT revised its earlier timing interpretation. All three rejected leaving the ambiguity unresolved and required “signed” demand to include product specification, quantity, delivery node, schedule and financial backing—not merely a technical endorsement or forecast.

The panel did **not** converge on the complete gate rule. Claude and Gemini allow a capacity ceiling of three times accepted demand, with Claude adding an availability-and-yield constraint. GPT separates coverage from investment sizing: the ratio is necessary but does not itself authorise excess capacity. Claude and GPT also differ over whether commitments may depend on KDP-0B approval and whether a costed Earth-supply baseline can substitute for committed purchasing resources.

The votes identified GPT’s response as having no substantive rejection, but did not establish agreement on its entire rule. Claude and Gemini approved Claude’s response; GPT remained neutral because its three-year window, 24-month deadline and η-based cap lacked sufficient justification. Those parameters therefore remain proposals, not panel decisions.

## Decision record

### Converged core

**Models: Claude, Gemini and GPT.**

> In the context of D-01’s demand-sized 0B real option and D-02’s stringent irreversible gate, facing an ambiguous multiplier and potentially circular internal demand, we chose a quantity interpretation of “within 3×” and financially backed, specified customer commitments, to achieve an auditable demand gate, accepting that stronger commitment requirements may delay or prevent 0B authorisation.

- **Warrant:** All three argue that demand-led sizing requires a quantity metric, while a signature alone does not establish credible demand.
- **Qualifier:** GPT explicitly treats the wording as a recommended owner ruling pending controlled-requirement verification. Claude and Gemini also leave owner choices outstanding.
- **Accepted downside:** All three accept that a stricter demand gate may block or delay an otherwise technically promising 0B.

### Outstanding position: capacity sizing

**Claude’s position**

> In the context of early-operation capacity planning, facing uncertainty in availability and yield, we chose a nameplate cap of `min(3 × accepted demand, accepted demand / η)`, to accommodate justified operating headroom, accepting residual underutilisation risk and possible exclusion of minimum-scale plants.

Claude’s warrant is that 3× should be a ceiling, not a target, with η justified from operating evidence. Claude qualifies this with a proposed owner decision for exceptions against g-economics.

**Gemini’s position**

> In the context of demand-led investment, facing speculative overbuilding, we chose a maximum nameplate of three times explicitly funded or contracted annual demand, to constrain physical scale, accepting that strict commitment requirements may delay investment.

Gemini treats the quantity ceiling as the capacity constraint; its response does not add Claude’s η cap or GPT’s separate smallest-feasible-configuration rule.

**GPT’s position**

> In the context of D-01’s demand-sized investment, facing the risk that a coverage allowance becomes permission to overbuild, we chose a separate smallest-technically-feasible-configuration rule, to meet accepted demand and approved reliability requirements without speculative capacity, accepting that indivisible hardware may remain unauthorised.

GPT’s warrant is that coverage and investment sizing answer different questions. GPT allows unavoidable surplus to be assessed through g-economics, while retaining the quantity gate.

### Outstanding position: internal commitment credibility

- **Claude:** Count independently authorised demand backed by committed purchasing funding **or** a costed Earth-supply baseline that it displaces; demand must exist if 0B is cancelled and must not be conditional on 0B approval. Claude acknowledges that the counterfactual test is unvalidated and internal baselines may still be inflated.
- **Gemini:** Count a legally binding external offtake agreement or a distinct, formally funded internal Phase 1 line item. Gemini does not specify an independent customer signatory or resolve approval conditionality.
- **GPT:** Require an independent customer budget authority and an authorised funded line item or equivalent approved budget commitment. Explicit KDP-0B and conforming-delivery conditions may be allowed; dependence on an otherwise unapproved downstream programme may not.

## Decision-quality audit

### Round 1 — Claude response

- **Weakest link named by votes:** Claude and GPT named **reasoning**; Gemini named none.
- **Missing or unsupported scaffold elements:** GPT found insufficient justification for the three-year averaging window, 24-month delivery deadline and η-based cap, and found the claimed ranking sensitivity undemonstrated. Claude identified two arithmetic errors in its own assessment matrix, neither changing its ranking.
- **Trade-off rather than factual dispute:** Claude explicitly identifies internal-demand inclusion versus protection from self-certification, and operating headroom versus strict demand matching, as owner value choices.
- **Vote outcome:** Claude and Gemini approved; GPT was neutral.

### Round 1 — Gemini response

- **Weakest link named by votes:** Claude named **reasoning**; Gemini and GPT named **information**.
- **Missing or unsupported scaffold elements:** Claude noted that the qualitative matrix did not apply its weights or clearly distinguish its leading options. Gemini’s self-review identified underdeveloped evidence-certainty and hypothesis-testing sections. GPT challenged unsupported high-confidence historical claims, the sufficiency of a funded internal line item to break circularity, and the undefined demand period.
- **Trade-off rather than factual dispute:** Gemini explicitly prioritises physical-capacity constraint over interpreting 3× as schedule tolerance. Claude questions whether Gemini’s three-times ceiling adequately serves its heavily weighted overproduction criterion.
- **Vote outcome:** Claude and Gemini were neutral; GPT rejected.

### Round 1 — GPT response

- **Weakest link named by votes:** Claude named **information**; GPT named **commitment**; Gemini named none.
- **Missing or unsupported scaffold elements:** Claude noted that the delivery-window bound remained unquantified. GPT’s self-review acknowledged that the window and authority choices still require controlled approval before any gate pass.
- **Trade-off rather than factual dispute:** GPT explicitly identifies stronger financial backing versus financing flexibility, minimum module efficiency versus strict demand matching, and longer commitments versus buyer flexibility.
- **Vote outcome:** All three approved the response. Claude’s separate gate proposal nevertheless retained a different sizing rule.

## Key Points

- **Meaning of 3×:** All three now support a quantity ratio. Claude and Gemini state `nameplate ≤ 3 × accepted annual demand`; GPT applies the equivalent inequality to each predeclared annual delivery period.
- **Specification:** All three require a product specification linked to T22. GPT additionally requires acceptance criteria and reconciliation of product and delivery boundaries.
- **Internal demand:** All three allow internal Phase 1 demand in principle. Claude and GPT explicitly require customer budget authority distinct from the 0B proposer.
- **External demand:** All three reject external-offtake-only as the general rule. GPT additionally requires evidence of counterparty ability to perform.
- **Schedule:** All three require dated deliveries. Claude proposes fixed timing parameters; Gemini defers the epoch and window; GPT requires them to be frozen before assessment.
- **Fallback:** Claude and GPT explicitly retain “0A only, Earth supply” if a compliant 0B cannot be authorised. GPT emphasises that passing demand does not replace the other gates.
- **Threshold economics:** GPT states that one-third coverage has not been shown to be economically sufficient; Claude likewise retains an independent economics assessment.

## Unresolved Questions

1. **Sizing:** Should the owner adopt Gemini’s 3× ceiling, Claude’s 3×-and-η cap, or GPT’s separate smallest-feasible-configuration rule?
2. **Financial backing:** Is Claude’s costed Earth-supply counterfactual sufficient, or must counted demand have the committed resources GPT requires?
3. **Conditionality:** Should Claude’s prohibition on KDP-0B-conditional demand apply, or GPT’s narrower allowance?
4. **Measurement period:** Should Claude’s three-year averaging window apply, or GPT’s period-by-period coverage test? Gemini leaves the window unspecified.
5. **Timing bound:** What evidence supports Claude’s proposed 24-month deadline, or an alternative?
6. **Decision authority:** Which customer budget authority signs, and which authority accepts the evidence? Claude and GPT require these roles to be specified.
7. **Exceptions:** Can an owner decision against g-economics permit excess nameplate, as Claude proposes, or must the configuration continue to satisfy GPT’s demand constraint?

## Recommended Actions

- **Record the shared interpretation:** Following all three responses, replace the ambiguous phrase with an explicit quantity inequality and a separate delivery-compatibility requirement.
- **Resolve sizing before recording a pass:** Put Claude’s, Gemini’s and GPT’s distinct capacity rules to the owner without treating them as equivalent.
- **Approve the commitment standard:** Resolve Claude’s counterfactual option against GPT’s resource-backed standard, including independent authority and approval conditionality.
- **Freeze the measurement rules:** Following Claude’s and GPT’s auditability requirements, approve the delivery boundary, epoch, periods and commitment window before gate assessment; do not treat Claude’s numerical timing proposals as agreed.
- **Check evidence that could change the ruling:** Claude and GPT identify the controlled rq-0-58 wording or drafting rationale as potentially decisive on original timing intent. Claude identifies 0A availability/yield data; GPT identifies validated minimum module size, budget authority and lifecycle economics as relevant to the remaining rules.
- **Update controlled records:** Following GPT’s recommendation, reconcile rq-0-58, the gate text and D-01 sizing language; following Claude’s recommendation, name the independent signatory role in the decision record.

```yaml
questionId: "rq-0-68"
topics:
  - id: multiplier-meaning
    topic: Meaning of within 3×
    positions:
      - statement: Interpret 3× as quantity coverage, not a timing tolerance.
        models: ["Claude Opus 5.5", "Gemini 3.1 Pro", "GPT-6.1 Sol"]
        evidence: All three Round 1 responses connect the quantity interpretation to D-01 demand-led sizing; GPT revises its earlier timing position.
    resolution_status: resolved
    priority: high

  - id: capacity-sizing
    topic: Capacity authorised after passing coverage
    positions:
      - statement: Cap nameplate at the smaller of three times accepted demand and accepted demand divided by justified availability times yield.
        models: ["Claude Opus 5.5"]
        evidence: Claude proposes an eta-based cap and requires justification for nameplate above accepted demand.
      - statement: Permit nameplate up to three times explicitly funded or contracted annual demand.
        models: ["Gemini 3.1 Pro"]
        evidence: Gemini explicitly gives 0.2 kt/yr demand supporting a maximum 0.6 kt/yr capacity.
      - statement: Apply coverage separately and authorise the smallest technically feasible configuration meeting accepted demand and approved reliability requirements.
        models: ["GPT-6.1 Sol"]
        evidence: GPT argues that a coverage allowance does not authorise speculative capacity; unavoidable surplus requires economic assessment.
    resolution_status: open
    priority: critical

  - id: signed-demand-backing
    topic: Financial backing and independence of signed demand
    positions:
      - statement: Accept committed purchase funding or a costed Earth-supply baseline displaced by demand, with an independent budget-authorised signatory.
        models: ["Claude Opus 5.5"]
        evidence: Claude proposes a counterfactual test that demand exists if 0B is cancelled, while acknowledging residual baseline inflation risk.
      - statement: Accept a binding external offtake agreement or a distinct formally funded internal Phase 1 line item.
        models: ["Gemini 3.1 Pro"]
        evidence: Gemini identifies financial commitment and T22 specification artifacts but does not specify an independent signatory.
      - statement: Require an independent customer budget authority and funded or equivalently approved budget commitment; external demand also needs counterparty-performance evidence.
        models: ["GPT-6.1 Sol"]
        evidence: GPT distinguishes resource-backed obligations from technical endorsements and unfunded planning allowances.
    resolution_status: partially-resolved
    priority: critical

  - id: approval-conditionality
    topic: Whether demand may depend on KDP-0B approval
    positions:
      - statement: Qualifying demand must not be conditional on 0B approval.
        models: ["Claude Opus 5.5"]
        evidence: Claude includes this prohibition in its proposed qualifying-instrument rule.
      - statement: Explicit KDP-0B and conforming-delivery conditions may qualify, but dependence on an otherwise unapproved downstream programme may not.
        models: ["GPT-6.1 Sol"]
        evidence: GPT distinguishes deployment conditions from unresolved downstream need or funding.
    resolution_status: open
    priority: high

  - id: demand-window
    topic: Measurement periods and delivery timing
    positions:
      - statement: Average over three years from planned first-nameplate date and require first qualifying delivery within 24 months.
        models: ["Claude Opus 5.5"]
        evidence: Claude proposes these parameters; GPT's review finds their justification insufficient.
      - statement: Require a dated schedule and leave the epoch and delivery window to the owner.
        models: ["Gemini 3.1 Pro"]
        evidence: Gemini explicitly lists those definitions as follow-on decisions.
      - statement: Test coverage in each predeclared annual period and freeze the commitment window and commissioning profile before assessment.
        models: ["GPT-6.1 Sol"]
        evidence: GPT seeks to prevent demand shifting between periods and leaves numerical duration for controlled approval.
    resolution_status: open
    priority: high
```