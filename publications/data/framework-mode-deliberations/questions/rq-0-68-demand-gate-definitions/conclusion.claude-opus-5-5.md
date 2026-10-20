---
questionId: "rq-0-68"
questionSlug: "demand-gate-definitions"
type: "discussion-conclusion"
generatedBy: "claude-opus-5-5"
generated: "2026-10-17"
framework: "18f503fe4ec6"
roundCount: 1
terminationReason: "unanimous-conclude"
role: "alternate synthesis"
---

## Summary

In a single round, all three models (Claude Opus 5.5, Gemini 3.1 Pro, GPT-6.1 Sol) rejected the null option of leaving the split for KDP-0B reviewers to resolve. All three read "within 3×" as a **quantity ratio**: the 0B nameplate output may not exceed three times accepted demand. GPT-6.1 Sol had earlier proposed a timing reading. In this round it adopted the quantity reading, stating that "within 3×" means C_t/D_t ≤ 3, "not a permitted delivery-date slip". Claude and GPT both kept timing as a **separate** delivery clause rather than a second meaning of "3×". Gemini deferred the epoch and delivery window to the owner.

All three agreed that "signed" demand must carry a product specification sufficient for T22, quantities, a delivery node and a dated schedule. All three also agreed that letters of intent, memos or technical endorsements alone do not qualify. Claude and GPT went further on circularity. Each requires a signatory or customer budget authority **distinct from the 0B proposer**, plus resource backing. Claude adds a counterfactual test: the demand must exist if 0B is cancelled, shown either by committed funding or by a costed Earth-supply line that the demand displaces. Gemini accepted either a funded internal Phase 1 line item or a binding external contract, but did not require an independent signatory. Claude's vote flagged that gap. Claude and GPT both rejected an external-offtaker-only rule because D-01 names Phase 1 demand as the sizing basis.

The main remaining divergence is **sizing**. Claude and Gemini treat 3× as a ceiling on nameplate. Claude bounds it further by a declared yield/availability factor η, through the cap nameplate ≤ min(3 × accepted demand, accepted demand / η). GPT holds that passing the 3× test is "necessary, not sufficient". Under GPT's rule, 0B is sized to the smallest feasible configuration that meets accepted demand, and any unavoidable surplus is justified through g-economics. Claude explicitly kept GPT's position visible as a "1× dissent" for the owner. The models also differed on several other points:
- whether a commitment may be conditional on KDP-0B approval;
- how demand is annualised (a 3-year average or a test for each period);
- the specific timing bounds.

On votes, GPT's response was approved by all three. Claude's was approved by Claude and Gemini and rated neutral by GPT. Gemini's was rated neutral by Claude and Gemini and rejected by GPT.

## Decision record

**Converged core (all three models on the quantity reading and specification contents; Claude and GPT on independent resource backing):**

> In the context of a one-way KDP-0B commitment that D-01 sizes by signed Phase 1 demand and D-02 subjects to stringent gating, facing an undefined "within 3×" (no numerator, denominator or epoch) and a buyer that is the project itself, we chose to define "within 3×" as a quantity ratio (nameplate kt/yr ≤ 3 × accepted demand kt/yr at the same product and delivery boundary) and to define "signed" as a controlled commitment with T22-sufficient specification, quantity, delivery node and dated schedule, to achieve a gate that two reviewers would pass or fail identically and that the project cannot satisfy by self-certification, accepting a heavier evidence burden and possible delay or non-authorisation of 0B.

- **Warrant:**
  - Claude: a gate protecting a one-way door must be decidable before the evidence arrives, and must test demand that exists independently of the decision it justifies.
  - GPT: "resource-backed, deliverable obligations, not nominal signatures, support capital commitment."
  - Gemini: because demand sizes 0B, the metric must constrain physical capacity.
- **Qualifier:**
  - Claude: the quantity reading is "likely" the intended meaning, with medium confidence that the counterfactual test is sufficient.
  - GPT: the ruling is a recommendation subject to verifying the controlled rq-0-58 text, which none of the models saw. No gate should be recorded as passed until the definition is approved.
- **Accepted downside:** the gate may block or delay a technically ready 0B (Claude, GPT, Gemini). Claude adds that strategic builds should go through an explicit owner decision, not through a loosened demand gate.

**Divergent positions on sizing:**

- **Claude Opus 5.5 (ceiling with η bound):** *In the context of first-of-kind ramp-up below nameplate, facing the risk of both overbuild and an unviable undersized plant, we chose nameplate ≤ min(3 × accepted demand, accepted demand / η), with the η basis on record. We pair it with a 3-year averaging window from E0 and a requirement that the first qualifying delivery falls due by E0 + 24 months, to achieve honest early-operation sizing, accepting that the cap is highly sensitive to η and that a plant with a high minimum viable scale may fail.* Any excess over the cap goes to an owner decision logged against g-economics.
- **Gemini 3.1 Pro (simple ceiling):** *We chose maximum 0B nameplate = 3 × signed annual demand (for example, 0.2 kt/yr of demand allows at most 0.6 kt/yr), to achieve margin for testing and scaling without unchecked overproduction, accepting delay if offtakers hesitate.* Epoch and delivery window are left to the owner.
- **GPT-6.1 Sol (coverage separated from sizing):** *We chose D_t ≥ C_t/3 for each predeclared annual period as a necessary coverage test, and authorisation of only the smallest technically feasible configuration that meets accepted demand. Any surplus from module size, redundancy or rate constraints must be quantified and justified through g-economics against smaller, staged and Earth-supply alternatives. The aim is capital discipline, accepting that indivisible hardware may remain unauthorised despite technical readiness.*

## Decision-quality audit

| Response (Round 1) | Votes | Weakest link named | Missing or unsupported scaffold steps | Trade-off points (values, not facts) |
|---|---|---|---|---|
| **Claude Opus 5.5** | Claude APPROVE, Gemini APPROVE, GPT NEUTRAL | Reasoning (Claude self-vote; GPT); none (Gemini) | Arithmetic errors in two weighted totals: O1 should be 2.95 and O5 2.30 (Claude's self-vote; ranking unchanged). Per GPT, the 3-year window, the 24-month deadline and the η-based cap lack justification even though they can change gate outcomes. GPT also says the claimed sensitivity of the option ranking was not demonstrated. Claude rated its own counterfactual test "very low / low" certainty. | T1: rigour vs option survival, i.e. whether internal demand counts at all. T2: minimum scale vs overproduction, i.e. a 3× ceiling vs GPT's 1×. Claude labelled both as owner values questions. |
| **Gemini 3.1 Pro** | Claude NEUTRAL, Gemini NEUTRAL, GPT REJECT | Reasoning (Claude); information (Gemini self-vote; GPT) | Matrix is qualitative and weights are not applied, so options C and D are barely distinguished (Claude). "High confidence" on routinely stranded assets is uncalibrated and unsupported (Claude, GPT). No independent signatory is required, so circularity is only partly addressed (Claude, GPT). The demand period and epoch are deferred while the response claims auditability (Claude, GPT). GRADE and ACH are underdeveloped (Gemini self-vote). Per Claude, the 3× ceiling sits uneasily with the 40% weight on preventing overbuilding. | Quantity bounding traded against schedule bounding (Gemini's stated trade-off). |
| **GPT-6.1 Sol** | Claude APPROVE, Gemini APPROVE, GPT APPROVE | Information (Claude); commitment (GPT self-vote); none (Gemini) | The delivery-window bound is unquantified (Claude: does not change the decision). Window and authority choices are reserved for controlled approval (GPT self-vote). GPT notes it relied on supplied extracts, not inspection of the files. Weighted scores verified correct (Claude). | Financing flexibility vs commitment credibility. Modular efficiency vs strict demand matching. Longer committed horizons vs buyer flexibility. GPT labelled all three as owner values. |

**Divergences that are trade-off points rather than facts:**
- The sizing ceiling (Claude/Gemini 3× vs GPT smallest-feasible).
- Whether internal Phase 1 demand should count at all.
- How stringent backing and commitment duration should be.

**Divergences that evidence could settle:**
- η from 0A ramp-up data (Claude).
- Minimum viable module size (GPT).
- The controlled rq-0-58 wording (Claude, GPT).

## Key Points

- **"Within 3×" is a quantity ratio**, nameplate over accepted demand in kt/yr (all three). GPT moved from its earlier timing reading. Claude's ACH ranked the timing hypothesis most disconfirmed, because "a timing ratio cannot size anything". GPT added that evidence of a timing intent would not remove the need for a quantity-and-sizing test.
- **Timing is a separate clause**, not overloaded onto "3×":
  - Claude: first qualifying delivery by E0 + 24 months.
  - GPT: deliverable within the buyer's accepted windows, with windows frozen before assessment and no shifting of demand between periods.
  - Gemini: deferred to the owner.
- **"Signed" requires**, per all three, a T22-sufficient product specification, quantity, delivery node and dated schedule. Claude and GPT add:
  - a signatory or budget authority independent of the 0B proposer;
  - resource backing, i.e. a funded line item (GPT, Claude) or a displaced Earth-supply line (Claude only);
  - exclusion of LoIs, MoUs and planning assumptions.

  GPT also requires acceptance criteria and cancellation or change terms. For external demand, GPT requires evidence that the counterparty can perform.
- **Counterfactual test** (Claude only): the demand must exist if 0B is cancelled. This ties the gate to the "0A only, Earth supply" fallback. Claude rated its own evidence for this test as very low to low.
- **External offtake**:
  - Claude: a credit, not required.
  - GPT: counts if enforceable and the counterparty can perform; an external-only rule was rejected as excluding D-01's internal demand.
  - Gemini: counts as one route.
- **Sizing**:
  - Claude: a ceiling of min(3×, demand/η).
  - Gemini: a ceiling of 3×.
  - GPT: smallest feasible configuration meeting accepted demand; 3× is not an allowance.
  - Claude and GPT agree that any excess goes through g-economics, not g-demand.
- **The 0.2–0.8 kt/yr figure is illustrative only**. The threshold follows from the proposed configuration (GPT).
- **g-economics must use the same accepted-demand figure**, with no separate optimistic case (Claude). GPT similarly says firm-demand utilisation should be reported separately from forecast utilisation over the asset life.
- **Fail outcome**: "0A only, Earth supply" (all three, consistent with the gate fallback). Claude also allows resizing 0B to pass.

## Unresolved Questions

1. **Sizing rule.** Should 3× be a ceiling (Claude, Gemini), with or without an η bound, or should 0B be sized to the smallest feasible configuration meeting accepted demand (GPT)? Claude framed this as an owner choice between 3× and 1×.
2. **Conditionality on 0B approval.**
   - Claude: a qualifying instrument must be "not conditional on 0B approval".
   - GPT: a commitment "may be conditional on the explicit KDP-0B authorisation and successful delivery of conforming product". It may not depend on an otherwise unapproved downstream programme.

   These rules conflict and were not reconciled.
3. **Annualisation.** Should demand be averaged over a 3-year window from E0 (Claude), or must D_t ≥ C_t/3 hold in every predeclared annual period (GPT)?
4. **Timing bounds.** The values of E0, the 24-month first-delivery bound and the commitment window are open. GPT said Claude's values lack justification; Gemini deferred them.
5. **Independent signatory.** Is a funded internal line item sufficient without a signatory independent of the 0B proposer (Gemini)? Claude and GPT say no. Claude adds that if the same team owns both budgets, only external demand is honest.
6. **Counterfactual test.** Is Claude's Earth-supply counterfactual required, or is GPT's resource-backing test sufficient? The test cannot be run if Phase 1 has no Earth-supply variant (Claude's assumption A1).
7. **Controlled wording.** What does rq-0-58 actually say? No model inspected the controlled text (GPT, Claude).

## Recommended Actions

1. **Verify the controlled rq-0-58 text and its rationale** before adopting any ruling (GPT, Claude). Reconcile rq-0-58, the g-demand text and D-01's sizing language in the baseline (GPT).
2. **Record the quantity reading of "within 3×"** in `gates-proposal.yaml` with numerator, denominator, units, product and delivery boundary (all three). Reconcile conversion yields and delivery losses explicitly (GPT).
3. **Owner decision on sizing.** Choose between a 3× ceiling (Gemini), a min(3×, demand/η) ceiling with a declared η basis (Claude), and a smallest-feasible-configuration rule (GPT). Record the losing positions as dissent (Claude).
4. **Owner decision on conditionality.** Decide whether commitments may be conditional on KDP-0B authorisation (GPT) or not (Claude).
5. **Fix the epoch, commitment window, annualisation method and first-delivery bound** before any gate assessment (Claude, GPT, Gemini). Justify the chosen values (GPT's critique of Claude).
6. **Name the independent signatory or customer budget authority** in `decisions.md`, and confirm it is distinct from the 0B proposer (Claude, GPT). Assign independent assurance to verify quantities, boundaries and non-duplication (GPT).
7. **Require Phase 1 planning to carry a costed Earth-supply baseline** if Claude's counterfactual test is adopted (Claude).
8. **Use the 0A mid-term review to check leading indicators**: a draft specification, a named node, and an opened Earth-supply or funded line (Claude).
9. **Collect evidence that could change the ruling**:
   - 0A ramp-up η, to retune the ceiling: tighten to 2× if η ≥ 0.7 (Claude);
   - the minimum viable module size (GPT);
   - the Phase 1 governance and budget structure (Claude A2; GPT);
   - whether offtakers require TRL 6 before committing (Gemini).

```yaml
questionId: "rq-0-68"
topics:
  - id: meaning-of-3x
    topic: Meaning of "within 3×" (quantity vs timing)
    positions:
      - statement: "Quantity ratio: nameplate kt/yr <= 3 x accepted demand kt/yr; timing handled by a separate clause or deferred"
        models: [Claude Opus 5.5, Gemini 3.1 Pro, GPT-6.1 Sol]
        evidence: "D-01 says demand sizes 0B and sizing is a quantity; rq-0-58 read as kt/yr against capacity (Claude, Gemini); ACH ranks timing reading most disconfirmed (Claude, GPT); GPT moved from its earlier timing reading but notes rq-0-58 text not seen"
    resolution_status: resolved
    priority: high
  - id: sizing-rule
    topic: Whether 3× is a sizing ceiling or only a coverage test
    positions:
      - statement: "3× is a ceiling bounded by declared yield/availability: nameplate <= min(3 x accepted demand, accepted demand / eta); excess via owner decision logged against g-economics"
        models: [Claude Opus 5.5]
        evidence: "First-of-kind plants run below nameplate during ramp-up; 3× approximates honest overcapacity if eta ~0.3-0.5; sensitivity to eta requires declared basis from 0A data"
      - statement: "Maximum 0B nameplate is 3 x signed annual demand"
        models: [Gemini 3.1 Pro]
        evidence: "Moderate confidence that 3× gives margin for testing and scaling without unchecked overproduction; dependent on unvalidated yields"
      - statement: "3× coverage is necessary not sufficient; authorise the smallest technically feasible configuration meeting accepted demand; unavoidable surplus justified through g-economics against staged and Earth-supply alternatives"
        models: [GPT-6.1 Sol]
        evidence: "Principal exposure is committing capital beyond credible need; separating coverage from sizing reduces speculative capacity (moderate confidence)"
    resolution_status: open
    priority: critical
  - id: signed-independence
    topic: What makes internal Phase 1 demand "signed" and non-circular
    positions:
      - statement: "Signatory with budget authority independent of the 0B proposer, plus committed funding or a displaced costed Earth-supply line (counterfactual: demand exists if 0B is cancelled); LoIs, MoUs and planning assumptions excluded"
        models: [Claude Opus 5.5]
        evidence: "Megaproject optimism bias (Flyvbjerg, by analogy); counterfactual ties gate to the Earth-supply fallback; own evidence certainty for the test rated very low/low"
      - statement: "Accountable customer authority distinct from the 0B proposer signs a controlled commitment with acceptance criteria, resource backing (funded line item) and change/cancellation terms; technical endorsement insufficient"
        models: [GPT-6.1 Sol]
        evidence: "Logical distinction between a signature and a resource commitment (high confidence); credibility conditional on real budget authority"
      - statement: "A funded internal Phase 1 line item or legally binding external contract suffices, with T22 spec, quantities, node and schedule; no independent signatory specified"
        models: [Gemini 3.1 Pro]
        evidence: "Asserted high confidence that unfunded internal demand leads to stranded assets; challenged by Claude and GPT as uncalibrated and as not fully breaking circularity"
    resolution_status: partially-resolved
    priority: critical
  - id: conditionality-on-0b
    topic: Whether a demand commitment may be conditional on KDP-0B approval
    positions:
      - statement: "Qualifying instrument must not be conditional on 0B approval"
        models: [Claude Opus 5.5]
        evidence: "Counterfactual test: demand must exist independently of the decision it justifies"
      - statement: "Commitment may be conditional on explicit KDP-0B authorisation and delivery of conforming product, but not on an otherwise unapproved downstream programme; count firm quantity only"
        models: [GPT-6.1 Sol]
        evidence: "Distinguishes approved appropriations from unfunded planning allowances; firm vs optional quantity"
    resolution_status: open
    priority: high
  - id: timing-window-epoch
    topic: Epoch, averaging/commitment window and delivery-timing bound
    positions:
      - statement: "3-year averaging window from planned first-nameplate date E0; first qualifying delivery due by E0 + 24 months"
        models: [Claude Opus 5.5]
        evidence: "Annualising over first year vs 3 years changes numerator greatly during ramp-up; values not further justified (GPT critique)"
      - statement: "Test D_t >= C_t/3 in each predeclared annual period; count only quantities deliverable within buyer windows; freeze windows and commissioning profile before assessment; bound left unquantified"
        models: [GPT-6.1 Sol]
        evidence: "Prevents demand shifting between periods; one year of purchases does not establish asset-life utilisation"
      - statement: "Owner to define the exact epoch and delivery window"
        models: [Gemini 3.1 Pro]
        evidence: "Deferred; criticised by Claude and GPT as undermining auditability"
    resolution_status: open
    priority: high
  - id: external-offtake-role
    topic: Role of external offtake
    positions:
      - statement: "External offtake is a credit reported separately, strengthening g-economics, not required; external-only rule would make the gate likely unpassable"
        models: [Claude Opus 5.5]
        evidence: "No kt-scale external market for space-processed material likely by KDP-0B (very likely, low certainty)"
      - statement: "External demand counts if enforceable with evidence of counterparty ability to perform; external-only rejected as excluding D-01 internal demand"
        models: [GPT-6.1 Sol]
        evidence: "External signatures vulnerable to cancellation, counterparty failure and unfunded obligations"
      - statement: "Legally binding external offtaker agreement is one qualifying route"
        models: [Gemini 3.1 Pro]
        evidence: "External legal/financial commitment breaks self-justification"
    resolution_status: partially-resolved
    priority: medium
```