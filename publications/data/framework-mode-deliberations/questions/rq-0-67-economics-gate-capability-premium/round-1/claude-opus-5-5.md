---
questionId: "rq-0-67"
questionSlug: "economics-gate-capability-premium"
modelId: "claude-opus-5-5"
modelName: "Claude Opus 5.5"
roundNumber: 1
generated: "2026-10-17"
type: "discussion-response"
---

# Economics gate (g-economics): may 0B pass above Earth-supply cost?

**Ruling in brief.** The economics gate tests cost parity only, with R = 1 written into the gate. Any capability premium (R > 1) is allowed, but only through a **separate owner decision taken before the cost evidence arrives**. That decision is priced in dollars, capped, and tied to a named benefit. It is then frozen into the gate as a ceiling the gate cannot change. On *where* the premium is decided, GPT's position stands. On *whether* a premium is allowed, Claude's position stands. Neither model addressed *when* the premium is set, and that is what decides whether the gate means anything.

---

## 1. Frame & decision type

- **Decision type.** This is a property decision about the KDP-0B economics criterion. It sits inside an executive decision about decision rights: who may set R, and when.
- **Reversibility.**
  - The rule itself is two-way and could be amended later.
  - The gate it governs (KDP-0B) is one-way.
  - Under D-02, stringency follows reversibility. So the rule must stop a one-way gate from being passed by a threshold chosen after the result is known.
- **Cynefin domain.** The cost question is *complicated*: it can be estimated, but current estimates disperse badly ($15.7B BOM against $22–195B from the panel). The premium question is a *values* question. No analysis will settle how much capability is worth to this owner.
- **Real issue.** All three panel positions are about the **value of R**. The failure mode is the **timing of R**.
  - If R can be set at KDP-0B, after the P70 estimate is on the table, the gate cannot fail on cost.
  - Any overrun becomes "capability premium". That is exactly GPT's "relabelled economics pass".
  - Claude's formula is sound. Its governance is open.

## 2. Criteria and weights (stated before options)

Swing weights sum to 100. Each weight reflects how much it matters to move from the worst to the best plausible option on that criterion, not how important the criterion sounds in the abstract.

| # | Criterion | Weight | Why this weight fits the range |
|---|---|---|---|
| C1 | **Pre-commitment integrity**: the threshold cannot be moved after the evidence is seen | 30 | The options run from "goalposts movable at the gate" to "fully frozen ex ante". That is the widest and most consequential swing. KDP-0B is one-way, and escalation of commitment is the dominant megaproject failure. |
| C2 | **Discriminating power**: the gate can fail on cost alone | 20 | A gate that cannot fail adds nothing over the TRL, demand and licence gates. The swing runs from "never fails" to "fails cleanly". |
| C3 | **Robustness** to launch price and estimate dispersion | 20 | Earth-supply $/kg moves with launch price. Our own estimates span roughly 9× ($22–195B). Options differ a lot on whether the verdict flips across scenarios. |
| C4 | **Fidelity to D-01** ("capability programme, not a cost saving") | 15 | This matters, but the swing is moderate. Every option except strict undercut can honour D-01 somewhere in the decision set. |
| C5 | **Decision-rights clarity** (RAPID: who decides the premium) | 10 | The swing runs from "ambiguous between gate reviewers and owner" to "named owner decision". It matters for accountability but does not change outcomes much. |
| C6 | **Simplicity / administrative cost** | 5 | All options are cheap next to Phase 0, so the swing is small. |

## 3. Options

- **O0. Null: leave the panel split as is.** The gate text keeps "R set by owner" with no timing or cap. GPT's objection stays as an unresolved note.
  - *Rejected.* In practice R gets set at KDP-0B by whoever is in the room, after the estimate is known. This is the worst case on C1 and C5. It also guarantees the dispute returns at the one-way gate, where it is most expensive.
- **O1. Gemini: strict undercut (R < 1).**
  - *Rejected.* The comparison is already 0B **P70** against Earth **P50**, which builds in conservatism. Requiring undercut on top of that double-counts margin.
  - It also contradicts D-01, which explicitly says Phase 0 is not a cost saving.
  - With a ±30% estimate band, the difference between R = 0.9 and R = 1.0 is inside the noise. Strict undercut adds false precision, not discrimination.
- **O2. GPT as stated: parity in the gate; any subsidy is a new explicit owner decision, timing unspecified.**
  - Strong on C5. It still allows the subsidy decision to be taken at KDP-0B after the numbers are known. That leaves the escalation path open under a cleaner label.
- **O3. Claude as stated: R set by the owner inside the gate, with R > 1 allowed.**
  - Strong on C4. Weakest on C1 and C2. The gate becomes "whatever R makes it pass".
- **O4. Recommended: pre-committed, capped, priced premium.**
  - The gate computes a parity verdict at R = 1.
  - A separate owner decision, **D-xx (Capability Premium Authorisation)**, is taken no later than the 0A mid-term review. It sets R_max and an absolute dollar cap ΔC_max, each tied to named benefits.
  - At KDP-0B the gate passes only if parity holds, or if the premium is within *both* caps. The gate cannot raise either cap.
  - Default if D-xx is not taken: R_max = 1.0.
- **O5. Drop the economics gate; let the demand gate carry economics through signed prices.**
  - *Rejected as a replacement* and kept as a *component*. Signed demand shows willingness to pay but does not test whether the delivered cost is credible.
  - However, demand signed at above-Earth prices is the best evidence for a premium. O4 uses it (see §8).

## 4. Assessment matrix (QOC; scores 1–5, weighted)

| Criterion (wt) | O0 Null | O1 Undercut | O2 GPT | O3 Claude | O4 Pre-committed cap | O5 Demand-only |
|---|---|---|---|---|---|---|
| C1 Pre-commitment (30) | 1 | 5 | 3 | 1 | **5** | 3 |
| C2 Discrimination (20) | 1 | 4 | 4 | 2 | **4** | 2 |
| C3 Robustness (20) | 2 | 2 | 3 | 3 | **4** | 2 |
| C4 D-01 fidelity (15) | 3 | 1 | 3 | 5 | **4** | 4 |
| C5 Decision rights (10) | 1 | 4 | 5 | 2 | **5** | 3 |
| C6 Simplicity (5) | 5 | 5 | 4 | 4 | 3 | 4 |
| **Weighted total (/500)** | **155** | **350** | **345** | **240** | **435** | **270** |

How to read the matrix:

- O1 and O2 score close. O1 buys integrity by sacrificing D-01, which is a values cost. O2's weakness is purely timing, and that is fixable. O4 is essentially O2 with the timing fixed plus Claude's parameter.
- O4 scores 4, not 5, on C3 for a specific reason: robustness depends on the launch-price scenario rule in §8, which carries its own judgment calls.
- Re-weighting check: if C4 is raised to 30 and C1 cut to 15, O4 still leads (O4 ≈ 420, O3 ≈ 300). The ranking is not fragile to the obvious values shift.

## 5. Sensitivity vs trade-off points

**Sensitivity points** (one attribute moves strongly; facts can settle them):

- **S1. Earth-supply P50 $/kg at SEL1.**
  - This is the denominator, and it is dominated by launch $/kg plus the in-space transfer stage.
  - A fall from about $1,500/kg to about $200/kg to LEO (fully reusable heavy lift at cadence) would cut the Earth baseline by several times.
  - A fixed R therefore implies a moving absolute premium. That is why O4 caps **dollars** as well as the ratio.
- **S2. Estimate band.**
  - At ±30%, R values between about 0.8 and 1.3 cannot be told apart from each other.
  - Today's dispersion, $15.7B BOM against $22–195B, is nowhere near ±30%.
  - Until the band is met, the gate is **"not ready"**, which is a different outcome from "fail on cost".
- **S3. Utilisation and replacement rate.** Per GPT, delivered $/kg is highly sensitive to plant utilisation and refurbishment. These belong in the P70, not in R.

**Trade-off points** (values questions; analysis will not settle them):

- **T1. Capability against cost.** How many dollars above Earth supply is supply independence, learning or Phase 1 option value worth to the owner? This is the content of D-xx. It is a values call and must not be dressed up as an estimate.
- **T2. Gate integrity against flexibility.** Freezing R before the evidence gives up the ability to react to a surprising capability benefit discovered during 0A.
  - I accept this loss.
  - The escape route is an explicit amendment to D-xx, recorded with its own rationale before the KDP-0B package is assembled. It is not an adjustment made at the gate.

## 6. Evidence certainty (GRADE certainty; IPCC/ICD 203 likelihood kept separate)

| Claim | Certainty of evidence | Likelihood judgment |
|---|---|---|
| Our cost estimates currently disperse far beyond ±30% (BOM $15.7B against panel $22–195B) | **High.** This comes directly from the panel record. | n/a; it is an observed fact |
| The true 0B cost lies above the BOM figure | **Low–moderate.** Inference from panel spread and the base rate of BOM-style bottom-up estimates. | *Likely* (≈66–90%) |
| Thresholds that can be set after results are known tend to be relaxed (escalation of commitment, optimism bias) | **Moderate.** Staw (1976) on escalation; Flyvbjerg's megaproject cost-overrun work (e.g., *Project Management Journal*, 2014). Analogous domains, not space ISRU specifically. | *Likely* that an unfrozen R would be raised at KDP-0B if the estimate overran |
| Budgeting one-way commitments at about 70% confidence is accepted practice | **Moderate–high.** NASA's joint cost-and-schedule confidence level policy (70% JCL at KDP-C, NPR 7120.5). | n/a; supports using P70 and not adding an undercut margin |
| Launch $/kg will fall substantially over the Phase 0–1 horizon | **Low.** Credible vehicle trajectories exist, but cadence and pricing are not demonstrated. | *About as likely as not* that a factor-of-3+ fall arrives before Phase 1 |
| Capability value (supply independence, learning) is real but not yet quantified | **Very low** for any dollar figure. | n/a; this is why it is a values decision |

**Calibration note.** I am *confident* in the governance argument (C1 dominates) and *not confident* in any particular R value. The ruling rests on the first and deliberately avoids depending on the second.

## 7. Key assumptions and falsifiers; ACH on what Phase 0 is for

| Assumption | What would falsify it |
|---|---|
| A1. The owner can state a capability premium before seeing the 0B estimate | The owner declines D-xx or can only answer "it depends on the number". In that case the default R_max = 1 applies, and that is itself informative. |
| A2. Earth supply at SEL1 is a well-defined comparator | The panel cannot agree on a reference Earth-supply architecture and launch scenarios before 0A mid-term. Then the denominator is unowned and the gate cannot be evaluated. |
| A3. The ±30% band is achievable by KDP-0B | 0A cost work does not converge, and the spread stays above about 2× in the second iteration. The gate then stays "not ready". That points to the fallback (0A only, Earth supply), not to a premium. |
| A4. Premium value is not already counted in demand | Phase 1 customers sign at above-Earth prices. The premium is then *market-backed*, not a subsidy, and should not be capped by D-xx. |

**ACH: competing hypotheses for the source of Phase 0's value**, scored against the existing record:

1. **H-capability/option value** (Phase 0 buys a Phase 1 option and supply independence). Consistent with D-01's wording and with 0B being sized by signed Phase 1 demand. *Least disconfirmed.*
2. **H-learning** (Phase 0 is mainly a technology demonstrator). Consistent with the TRL work package. It is weakened because a learning goal would not need a 0B production step at all; 0A already serves it.
3. **H-cost saving.** Directly disconfirmed by D-01, and by the panel cost range sitting well above the BOM.

H1 ranking first is why a premium must be *allowed*. The evidence for H1 is qualitative, which is why it must be *priced and decided by the owner*, not inferred at the gate.

## 8. Decision, warrant, accepted downside

### Gate criterion text (proposed for `gates-proposal.yaml`, g-economics)

```yaml
g-economics:
  readiness_precondition:
    - 0B delivered-cost estimate band <= ±30% at P70/P50 spread
    - Earth-supply reference architecture and launch-price scenarios (L-low, L-central, L-high)
      frozen at 0A mid-term review
    - if not met: verdict = NOT READY (route to fallback "0A only, Earth supply"), not FAIL
  parity_test:
    metric: C0B_P70($/kg delivered SEL1) vs E_P50($/kg Earth supply SEL1)
    R: 1.0   # fixed in-gate; not adjustable at KDP-0B
  premium_allowance:
    source: owner decision D-xx (Capability Premium Authorisation)
    deadline: no later than 0A mid-term review; amendments only by recorded owner decision
              before KDP-0B package is assembled
    default_if_absent: R_max = 1.0, dC_max = 0
    contents:
      - R_max (ratio ceiling)
      - dC_max (absolute $ ceiling on (C0B_P70 - E_P50) x Phase-1 signed delivered mass)
      - named benefits bought (supply independence | learning | Phase-1 option value), each with
        the evidence that would show it delivered
    market_backed_exemption: premium covered by signed Phase-1 prices above E_P50 does not
      count against dC_max
  pass_rule:
    PASS if, in L-central AND L-high: C0B_P70 <= R_max x E_P50 AND premium$ <= dC_max
    AND in L-low: premium$ <= dC_max (ratio may exceed R_max only if the $ cap holds)
    FAIL otherwise. Gate reviewers may not alter R_max or dC_max.
  reporting: always report parity verdict (R=1) separately from premium-authorised verdict
```

**Why the L-low rule takes this form.** In a cheap-launch world the ratio can blow out even when the dollar amount at stake is modest. Holding the absolute cap while relaxing the ratio stops the verdict flipping simply because the denominator collapsed. This is Claude's "must not reverse across the launch-price range", made operational.

**Guidance to the owner on D-xx** (a values call; my recommendation only):

- Do not authorise a ratio-only premium.
- If authorising, keep R_max ≤ about 1.5 and set dC_max no higher than the owner would pay to buy the named benefit directly. One example is the cost of a hedge against launch-cadence disruption for the Phase 1 supply chain.
- A premium inside about 1.3 is mostly estimate noise anyway. Be explicit whether D-xx is buying a real capability or absorbing uncertainty.

### Y-statement

In the context of a one-way KDP-0B gate for a programme the owner has declared a capability programme, not a cost saving (D-01), and facing cost estimates dispersed around 9× with an Earth-supply baseline that moves with launch price, we chose a parity-only economics test (R = 1 in-gate) combined with a separate, pre-committed, dollar-capped capability-premium decision (D-xx) taken by the 0A mid-term review. This is to achieve a gate that can fail on cost, a premium that is honest about what it buys, and decision rights that sit with the owner. We accept that a genuinely valuable capability discovered late in 0A cannot be credited at the gate without a recorded amendment, and that a missing D-xx defaults to strict parity.

### Toulmin

- **Claim:** A premium may pass KDP-0B only within a cap the owner fixed before seeing the 0B estimate.
- **Grounds:** Estimate dispersion; launch-price sensitivity; D-01 wording; D-02's "stringency follows reversibility".
- **Warrant:** At a one-way gate, any threshold that can be chosen after the evidence is known stops being a test. A test that cannot fail adds no information to the decision.
- **Backing:** Escalation-of-commitment and megaproject-overrun literature; NASA's practice of committing at 70% JCL with thresholds set before confirmation.
- **Qualifier:** *Likely* the right structure. Confidence is *moderate*, because the behavioural evidence comes from analogous domains.
- **Rebuttal conditions:** If the owner can credibly price capability only once the 0B design is known, D-xx moves later. It must still come before the KDP-0B package, never at the review.

## 9. Consequences (Kruchten relations)

**Enables:**

- **Coupling with g-demand.** The market-backed exemption ties premium tolerance to signed Phase 1 prices. This is the cleanest evidence that H-capability is real.
- **A clean fallback trigger.** "Not ready" and "fail" both route to "0A only, Earth supply", but they are recorded differently. That keeps the lesson legible.

**Requires** (new follow-on decisions and artefacts):

- **D-xx, Capability Premium Authorisation**, as an owner decision due by the 0A mid-term review.
- **An owned Earth-supply reference spec**: architecture, transfer stage, and three launch-price scenarios. It is frozen at the mid-term review and added beside `trl-baseline.yaml`.
- **Cost-method rules** for reaching ±30%: independent estimate, reconciliation of the BOM against the panel range, and explicit modelling of utilisation and replacement in the P70.

**Constrains:**

- KDP-0B reviewers lose the authority to set R. Claude's "R set by the owner" survives, but only *ex ante*.

**Conflicts with:**

- Gemini's undercut threshold. I keep this disagreement rather than averaging it away. If the owner holds that Phase 0 must save money, D-01 itself needs revisiting, not the gate.

**Evidence that would change this ruling:**

1. Independent estimates converge within ±30% at or below Earth P50 in all launch scenarios. The premium machinery is then moot, and O2 (plain parity) suffices.
2. Signed Phase 1 contracts at above-Earth prices cover the full gap. The premium is market-backed, and D-xx shrinks to a formality.
3. Launch prices fall far enough that parity is unattainable in every scenario. The question is then no longer a gate parameter. It becomes whether 0B should exist at all, which is a D-01-level owner decision to be taken immediately, not deferred to KDP-0B.
4. Evidence that the owner's pre-stated values would be *better* informed by the 0B design, for example capability benefits that only become visible at integrated test. That would justify moving the D-xx deadline later, but never to the gate itself.