---
questionId: "rq-0-68"
questionSlug: "demand-gate-definitions"
modelId: "gpt-6-1-sol"
modelName: "GPT-6.1 Sol"
roundNumber: 1
generated: "2026-10-17"
type: "discussion-response"
---

## 1. Frame & decision type

**Recommendation:** interpret “within 3×” as a **quantity-coverage test**, not a timing tolerance. Define “signed” as an **authorised, resource-backed demand commitment**, with product, quantity, delivery node and schedule specified. Apply a separate sizing rule: **passing the 3× test does not authorise building three times the accepted demand.**

This is a **property decision** defining the demand gate and an **executive decision** governing commitment authority. The definition is reversible before procurement; the resulting KDP-0B investment may not be. Accordingly, D-02 supports a stringent, auditable rule at KDP-0B without requiring equally mature commitments at every internal 0A review.

The decision concerns **demand credibility and sizing**, not whether demand alone justifies 0B. Target, economics, licence and the applicable TRL requirements remain independent gates.

**Source limitation:** I rely on the supplied extracts from `gates.md`, `gates-proposal.yaml`, `trl-baseline.yaml` and `decisions.md`, not an independent inspection of those files.

## 2. Criteria and weights

These are proposed **swing weights**, not measured programme preferences.

| Criterion | Evaluated swing | Weight | Why this weight fits that range |
|---|---|---:|---|
| **C1. Objective auditability** | From materially different interpretations to reproducible pass/fail results using frozen definitions | **25%** | An unauditable gate cannot reliably govern an irreversible commitment. |
| **C2. Commitment credibility** | From an aspirational internal signature to an authorised, resource-backed buyer obligation | **30%** | Circular internal demand can create the appearance of a market without any actual resource commitment. |
| **C3. Capital discipline and D-01 consistency** | From speculative capacity justified by the multiplier to demand-sized investment with explicit treatment of indivisibility | **30%** | The principal financial exposure is committing 0B capital beyond credible need. |
| **C4. Feasibility and option preservation** | From excluding legitimate internal demand or forcing premature funding to a practicable gate that preserves staged investment | **15%** | Excessively rigid contracting could destroy a useful real option, but convenience must not dominate credibility. |

**Musts, before scoring:** the final rule must be objectively testable, accommodate genuinely authorised internal Phase 1 demand, preserve D-01 demand-led sizing, and leave the other gates intact. Weighted scores cannot compensate for failing these conditions.

## 3. Options

**A. Null: retain the split and resolve it at KDP-0B.**  
Argument for: avoids premature prescription.  
Reject: bidders, designers and reviewers would work against different requirements; later interpretation could determine the outcome retrospectively.

**B. Quantity interpretation, ordinary signatures.**  
Require signed annual demand of at least one-third of nameplate capacity, with specification and dates, but no explicit resource-backing requirement.  
Argument for: simple and close to Claude’s and Gemini’s quantity reading.  
Reject: a project team can sign its own demand forecast without creating an independently authorised commitment.

**C. Timing interpretation, strong commitments.**  
Require accepted delivery dates to fall within a factor-of-three interval measured from a common epoch, alongside resource-backed orders.  
Argument for: addresses schedule compatibility explicitly.  
Reject: absent an independently justified epoch and schedule-risk model, the multiplier is arbitrary. It also does not establish adequate quantity coverage.

**D. Quantity interpretation, resource-backed internal or external demand, separate sizing constraint. — Recommended.**  
Argument for: distinguishes three questions: *is there enough demand, is it credible, and what capacity should be authorised?*  
Downside: requires more evidence and governance than a signed requirements document.

**E. Quantity interpretation, external offtake only.**  
Argument for: reduces internal circularity.  
Reject: unnecessarily excludes the internal Phase 1 demand expressly contemplated by D-01. External signatures also remain vulnerable to cancellation, counterparty failure and unfunded obligations.

## 4. Assessment matrix

Scores: **0 = poor; 4 = strong**. These are decision judgments, not empirical measurements.

| Option | C1 Auditability 25% | C2 Credibility 30% | C3 Capital discipline 30% | C4 Feasibility 15% | Weighted /4 | Musts |
|---|---:|---:|---:|---:|---:|---|
| A. Leave split unresolved | 0 | 1 | 1 | 2 | **0.90** | Fail |
| B. Quantity + ordinary signature | 3 | 1 | 2 | 4 | **2.25** | Fail |
| C. Timing + strong commitment | 2 | 4 | 2 | 2 | **2.60** | Fail as a standalone demand rule |
| **D. Quantity + backed commitment + sizing constraint** | **4** | **4** | **4** | **3** | **3.85** | **Pass** |
| E. External-only commitments | 4 | 3 | 4 | 1 | **3.25** | Fail internal-demand accommodation |

### Proposed rule text

> **g-demand — KDP-0B**
>
> **1. Quantity coverage.** For each predeclared annual delivery period in the initial commitment window, accepted firm demand \(D_t\) shall satisfy:
>
> \[
> D_t \ge C_t/3
> \]
>
> Here, \(D_t\) is accepted demand in tonnes/year and \(C_t\) is the proposed commissioned nameplate output in tonnes/year for the same period, product and delivery boundary. Thus “within 3×” means \(C_t/D_t \le 3\), not a permitted delivery-date slip.
>
> Product conformity, delivery losses, conversion yields and the nameplate reference conditions shall be explicitly reconciled. Unlike products shall not be added as interchangeable tonnes without a validated conversion.
>
> **2. Delivery compatibility.** Count only quantities that the proposed system can deliver to the specified node within the buyer’s accepted delivery windows. The commitment window, annual periods and commissioning profile shall be frozen before gate assessment. Demand shall not be shifted between periods merely to obtain a pass.
>
> **3. Accepted commitment.** Demand counts only where an accountable customer authority has signed a controlled commitment specifying product requirements, quantities, delivery node, dated schedule, acceptance criteria, resource backing, and cancellation or change terms.
>
> For internal Phase 1 demand, resource backing requires an authorised funded line item or equivalent approved budget commitment covering the counted purchases and necessary receiving/use capability. Technical-user endorsement alone is insufficient. The customer budget authority must be distinct from the 0B production proposer.
>
> For external demand, require an enforceable offtake commitment plus evidence of counterparty ability to perform; a signature or letter of interest alone is insufficient.
>
> **4. Conditionality.** A commitment may be conditional on the explicit KDP-0B authorisation and successful delivery of conforming product. It shall not count if its funding or need remains contingent on an otherwise unapproved downstream programme. Count the firm committed quantity, not optional upside.
>
> **5. Sizing.** Passing the coverage test is necessary, not sufficient. Authorise the smallest technically feasible configuration capable of meeting accepted demand and its approved reliability requirements. Do not use the 3× allowance to justify speculative modules, inventory or sales.
>
> Any unavoidable capacity surplus from minimum module size, redundancy or production-rate constraints shall be quantified and justified through the economics gate against smaller, staged and Earth-supply alternatives.
>
> **6. Failure outcome.** Without accepted demand and a compliant configuration, do not authorise 0B; retain the agreed “0A only, Earth supply” fallback.

The cited **0.2–0.8 kt/yr** is therefore illustrative, not a universal threshold. The threshold follows from the actual proposed configuration.

## 5. Sensitivity vs trade-off points

### Sensitivity points — evidence can change the result

- **Minimum viable module size:** if even the smallest credible plant exceeds three times firm demand, the quantity gate fails. That is information, not a reason to redefine demand.
- **Commitment duration:** one year of purchases does not establish a decade of economic utilisation. The initial window must be specified, while uncontracted asset-life exposure remains visible in the economics gate.
- **Delivery-boundary yields:** plant output can materially exceed useful tonnes received. Inconsistent boundaries can create a false pass.
- **Budget conditionality:** an approved appropriation, an authorised future commitment and an unfunded planning allowance are not equivalent.
- **Product fungibility:** demand for different products or destinations may not support the same production capacity.

### Trade-off points — owner values, not facts to discover

- **Financing flexibility versus commitment credibility:** requiring stronger commitments may delay 0B but reduces unsupported capital exposure.
- **Modular efficiency versus strict demand matching:** minimum-size hardware may provide unavoidable headroom; permitting it accepts some underutilisation risk.
- **Longer committed horizons versus buyer flexibility:** stronger utilisation assurance can impose costly cancellation exposure on Phase 1.

The recommendation remains preferred under reasonable weight changes because it performs strongly on the three highest-priority criteria. The unresolved issue is not its ranking but **how stringent the backing and duration requirements should be**.

## 6. Evidence certainty

GRADE labels below are adapted to this engineering decision; they do not imply clinical-quality evidence.

| Key claim | Evidence certainty | Confidence and likelihood |
|---|---|---|
| D-01 requires demand-led sizing; D-02 increases stringency for irreversible commitments | **High within the supplied record** | High confidence in that reading; likelihood is not applicable to a recorded decision. |
| Quantity is the better-supported interpretation of “3×” | **Moderate** | Moderate confidence: Claude and Gemini support quantity; the exact text of rq-0-58 is not supplied. No probability assigned to original authorial intent. |
| A technical signature alone does not establish funded internal demand | **Moderate** | High confidence in the logical distinction; the likelihood of actual unfunded commitment here is unknown. |
| Separate coverage and sizing rules reduce the opportunity to justify speculative capacity | **Moderate** | Moderate confidence in the mechanism; no project-specific loss reduction can be quantified. |
| One-third coverage is economically sufficient | **Very low / unestablished** | No such claim is warranted. Economic viability must be demonstrated separately. |
| Internal demand can be made credible without external sales | **Moderate** | Moderate confidence, conditional on actual budget authority and enforceable programme controls. |

Agreement by two panel members supports interpretation; it is not independent validation of the threshold’s economics. Gemini’s silence on “signed” supplies no evidence of agreement.

## 7. Key assumptions

| Assumption | Evidence that would falsify it |
|---|---|
| The multiplier originated as a capacity-to-demand ratio | The controlled rq-0-58 text or its approved rationale explicitly defining a time ratio and epoch |
| Internal Phase 1 can make a meaningful resource-backed commitment | Financial/governance evidence that its authority cannot reserve or commit the relevant resources |
| Proposed output can be reconciled to usable demand | Demonstrated non-fungibility, unqualified product requirements, or delivery losses that defeat the claimed match |
| Staging, throttling or modular selection provides some sizing discretion | A validated design showing a technically indivisible minimum plant |
| An initial commitment window can support a defensible investment decision | Lifecycle economics showing that plausible post-window demand loss makes the investment unacceptable |

**ACH ranking of interpretations, least disconfirmed first:**

1. **Quantity coverage plus an independent schedule test:** consistent with two stated panel positions and D-01’s sizing purpose.
2. **Quantity coverage intended to permit general 3× oversizing:** compatible with the inequality alone, but in tension with demand-led sizing.
3. **Timing ratio as the primary demand test:** least supported by the supplied requirement context; neither its epoch nor its engineering basis is established.

Evidence of timing intent would change the interpretation ruling. It would **not eliminate the need for a separate quantity-and-sizing test**.

## 8. Decision, warrant, accepted downside

Adopt **Option D**.

The warrant is that **a credible buyer commitment and a feasible delivery obligation justify capacity; signatures and a coverage ratio alone do not**. This implements D-01 without treating an internal buyer as either automatically credible or inherently invalid.

Accepted downside: stronger commitment evidence may postpone 0B, and indivisible hardware may remain unauthorised despite technical readiness. That is consistent with preserving 0B as a real option rather than making technical success an entitlement to deployment.

**Qualifier:** this is a recommended owner ruling, not a claim that the unseen controlled requirement already has this wording. No existing gate should be recorded as passed until the definition and evidence package are approved.

## 9. Consequences

- **Update the controlled baseline:** reconcile rq-0-58, the demand-gate text and D-01’s sizing language.
- **Assign decision rights:** customer budget authority signs demand; the gate authority accepts it; independent assurance verifies quantities, boundaries and non-duplication.
- **Enable T22 qualification planning:** signed product and acceptance requirements become controlled inputs, not substitutes for qualification evidence.
- **Constrain 0B architecture:** commission only justified tranches; expansion requires additional accepted demand.
- **Expose economic risk:** report firm-demand utilisation separately from forecast utilisation across the asset life.
- **Preserve fallback:** a failed demand gate does not undo useful 0A capability work or waive the Earth-supply alternative.

**Decision record — Y-statement:** *In the context of D-01’s demand-sized 0B real option and D-02’s stringent irreversible gate, facing ambiguous “within 3×” and circular internal signatures, we choose quantity coverage backed by authorised customer commitments and a separate demand-led sizing constraint, to achieve auditable investment discipline, accepting additional commitment burden and possible deployment delay.* **Warrant:** resource-backed, deliverable obligations—not nominal signatures—support capital commitment. **Qualifier:** subject to controlled-requirement verification and independent economics approval. This enables configuration selection and customer-interface baselining, while constraining speculative capacity and unauthorised 0B commitment.