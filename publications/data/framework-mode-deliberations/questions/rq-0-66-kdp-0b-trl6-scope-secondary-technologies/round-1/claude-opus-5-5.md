---
questionId: "rq-0-66"
questionSlug: "kdp-0b-trl6-scope-secondary-technologies"
modelId: "claude-opus-5-5"
modelName: "Claude Opus 5.5"
roundNumber: 1
generated: "2026-10-17"
type: "discussion-response"
---

# Must T11, T18, T09, T12 and T20 be at TRL 6 at KDP-0B?

**Short answer: no, not uniformly. The five do not form one class, and treating them as one is what produces the Claude/GPT split.**

- **T18 (sampling and assay)** stays project-ending at KDP-0B. Its evidence should come from the 0A scout mission itself, which is a higher bar than ground TRL 6.
- **T11 (scout spacecraft)** leaves the KDP-0B technology list. It returns only under a named re-entry condition.
- **T09, T12 and T20** are held at TRL 6 for the selected reference implementation by default. A waiver is allowed only for an item that has a qualified TRL 6 fallback, and only if the economics gate still closes with every waived item on its fallback at the same time.

This position is neither Claude's nor GPT's. I argue it below. Gemini's stated positions are counted only where it actually stated them.

---

## 1. Frame & decision type

**Decision type.** This is a property decision on the KDP-0B gate: what membership and criterion apply to five technologies. Two executive sub-decisions sit inside it: what "selected reference implementation" binds, and what conditions a waiver must meet.

**Reversibility.**
- The gate text is cheap to change before KDP-0B.
- The gate outcome is not cheap to change. Under D-02, KDP-0B is a one-way door, so the rule must be written as if it will be applied mechanically by people under schedule pressure.

**Cynefin domain.** Complicated, not complex. The facts that matter are knowable before KDP-0B:
- whether the scouts returned assay data;
- whether a fallback exists for each item;
- whether economics closes with that fallback.

So the decision can be made now and resolved by evidence later. That is the property a real-options gate under D-01 should have.

**What is actually being decided.** The question as posed asks "TRL 6 or not?". The more useful question is: what failure must KDP-0B protect against for each item, and is TRL 6 the right instrument for it?
- **T11 and T18.** The risk is committing Phase 1 to a target whose grade was never measured. TRL is a weak proxy for that. The target gate is the real instrument.
- **T09, T12 and T20.** The risk is committing Phase 1 to an architecture that fails economically if one of these is late or underperforms. TRL 6 is one guard against that. A proven fallback that closes economics is a second, equally valid guard.

---

## 2. Criteria and weights

These are swing weights, stated before options. Each weight reflects how much the options differ on that criterion, not how important the topic is in the abstract.

| # | Criterion | Swing range across options | Weight | Why this weight |
|---|---|---|---|---|
| C1 | **Protection against an irreversible wrong commitment at KDP-0B** | From "a Phase 1 commitment can go through with an unmeasured target or an unfallbacked TRL 4–5 item" to "cannot" | 0.35 | Under D-02 this is the reason the gate exists. The options differ sharply here. |
| C2 | **Cost of delay at KDP-0B** | From "the gate can slip by more than 12 months waiting on T12 TRL 6" to "no slip from these items" | 0.20 | Real but bounded. D-01 sizes 0B by signed demand, and demand has a shelf life. |
| C3 | **Auditability and resistance to gaming** | From "a waiver is a promise ('funded path')" to "a waiver is a pass/fail check on stated evidence" | 0.20 | One-way gates fail through erosion more than through bad initial rules. The options differ a lot here. |
| C4 | **Consistency with D-01, D-02 and the four discriminating gates** | From "duplicates or conflicts with the target and economics gates" to "composes with them" | 0.15 | Matters, but the differences are mostly drafting quality. |
| C5 | **Phase 0 resource burden** | From "fund TRL 6 campaigns for all five plus fallbacks" to "fund only what the gate needs" | 0.10 | The swing is a few qualification campaigns. It is meaningful but small relative to the 0B commitment. |

A deliberate omission: "agreement with the panel majority" is not a criterion. Per the guidelines, disagreements are kept, not averaged away.

---

## 3. Options

### Group A: T11 and T18 (0A flight technologies)

- **A0 (null).** Leave the split as it is.
  - Effect: T18 is project-ending (Gemini, GPT, panel headline). T11 is project-ending in GPT's view and the panel headline, absent from Gemini's YAML, and architecture-change in Claude's view.
  - Result: the gate text is ambiguous, and whoever drafts the YAML decides.
- **A1 (GPT).** Both at TRL 6 technology maturity before KDP-0B.
- **A2 (Claude).** Both treated as 0A flight technology, gated at scout PDR (TRL 6), and absent from the KDP-0B list.
- **A3 (recommended).**
  - T18 stays project-ending at KDP-0B. Its criterion is evidence provenance: the target gate must be satisfied by T18-class measurements made at the target. Ground TRL 6 alone does not satisfy KDP-0B.
  - T11 is off the KDP-0B list. It re-enters if any Phase 1 element inherits T11 hardware or software, for example a scout-derived bus for repeat prospecting or a T12 handling vehicle.

### Group B: T09, T12, T20 (supporting systems)

- **B0 (null).** Leave the split. In practice this means GPT's TRL 6 for the drafter who reads the headline, and Claude's TRL ≥ 5 waiverable for the drafter who reads the classification. This is the worst outcome for a one-way gate.
- **B1 (GPT).** TRL 6 for selected implementations, no waiver. Substitutions trigger reassessment.
- **B2 (Claude).** TRL ≥ 5, waiverable, with a funded path to TRL 6.
- **B3 (recommended): TRL 6 default with a substitution-backed waiver.**
  - The selected reference implementation must be at TRL 6.
  - A waiver down to TRL ≥ 5 is permitted only if all three conditions hold:
    1. A named fallback implementation is at TRL 6 in a relevant environment.
    2. The economics gate passes in a joint-fallback case, with every waived item on its fallback simultaneously.
    3. The fallback's mass, power and schedule penalties are carried in the Phase 1 baseline, not held in reserve.
- **B4 (rejected): make them project-ending.** This is TRL 6 with no waiver and no fallback route. It differs from B1 only in labelling, and it overstates the consequence of failure. These are architecture-change by unanimous classification.

### Why I reject the alternatives

- **A1.** It asks for ground TRL 6 on technologies that, by KDP-0B, should have flight evidence or should have failed the target gate. The criterion is redundant when the scouts succeed. When they fail it is misleading, because a TRL 6 sampler on the ground does not make an unmeasured target investable. It also puts T11 bus maturity on a gate where it has no decision value.
- **A2.** It is right about T11 but leaves a gap for T18.
  - If the target gate were satisfied by remote sensing alone, which nothing in the current four-gate text forbids, KDP-0B could pass without bulk grade ever being measured in situ.
  - Phase 1 site selection also depends on T18-class assay, not just Phase 0.
  - Dropping T18 from the list removes its only binding hook.
- **B1.** It is safe but blunt.
  - T12, autonomous handling of 150–300 t payloads, is the item least likely to reach TRL 6 by KDP-0B. Panel estimates are TRL 2–4, with AD² 5–6.
  - Under B1 the whole Phase 1 decision waits on T12, even where smaller-payload handling at TRL 6 could carry the architecture at a known cost.
  - That turns an architecture-change technology into a project-schedule-ending one, which is the classification error D-02 was meant to avoid.
- **B2.** It is efficient but not auditable.
  - A "funded path to 6" is a budget line, not evidence. It does not answer what happens to Phase 1 if the path fails, and that is the only question a one-way gate should ask.
  - Three independent waivers can also stack. Each item is survivable alone, but the joint failure was never tested.

---

## 4. Assessment matrix (QOC)

Scores run from 1 (poor) to 5 (best) on each criterion's swing range, weighted per Section 2.

**Group A: T11 and T18**

| Option | C1 (0.35) | C2 (0.20) | C3 (0.20) | C4 (0.15) | C5 (0.10) | Weighted |
|---|---|---|---|---|---|---|
| A0 null | 2 | 3 | 1 | 2 | 3 | **2.05** |
| A1 GPT | 3 | 3 | 4 | 2 | 2 | **2.95** |
| A2 Claude | 3 | 5 | 3 | 4 | 5 | **3.80** |
| **A3** | **5** | 4 | 5 | 5 | 4 | **4.65** |

Rationale for the key cells:
- **A3 on C1 (5).** It closes the remote-sensing loophole. A2 does not, so A2 scores 3.
- **A1 on C4 (2).** It duplicates the target gate with a weaker criterion.

**Group B: T09, T12, T20**

| Option | C1 (0.35) | C2 (0.20) | C3 (0.20) | C4 (0.15) | C5 (0.10) | Weighted |
|---|---|---|---|---|---|---|
| B0 null | 2 | 3 | 1 | 1 | 3 | **1.95** |
| B1 GPT | 5 | 1 | 5 | 3 | 2 | **3.60** |
| B2 Claude | 2 | 5 | 2 | 3 | 4 | **2.95** |
| **B3** | **4** | 4 | 4 | 5 | 2 | **3.95** |
| B4 project-ending | 5 | 1 | 5 | 1 | 2 | **3.30** |

Rationale for the key cells:
- **B3 on C1 (4, not 5).** A fallback at TRL 6 protects against the item failing. It does not protect against the fallback's penalty being underestimated.
- **B3 on C5 (2).** It requires qualifying fallbacks, which is real money.
- **B3 on C4 (5).** It makes the economics gate test the architecture-change consequence directly, which is what "architecture-change" means.

**Robustness of the Group B ranking.** B3's margin over B1 is about 0.35, which is not large.
- If C2 falls below roughly 0.10 and C1 rises to roughly 0.45, B1 wins. This is the trade-off point in Section 5.
- The ranking is robust to any reasonable C3/C4/C5 reweighting.

---

## 5. Sensitivity vs trade-off points

### Sensitivity points (facts that, once settled, decide the issue)

- **S1: When the scouts report relative to KDP-0B.**
  - If scout assay data reliably arrives before KDP-0B, A3 costs nothing extra.
  - If the KDP-0B date is planned before scout return, A3 forces a slip. That is correct: the target gate could not honestly pass anyway. But the owner should see the slip now.
- **S2: Whether a TRL 6 fallback exists or can be qualified for T12.**
  - Plausible fallbacks are smaller handling units (30–60 t class) with more transfers, or crewed or teleoperated assist.
  - If no fallback can be qualified, B3 collapses to B1 for T12. That is acceptable and honest.
- **S3: Economics margin in the joint-fallback case.**
  - Example penalties include a lower-voltage T09 with more conductor mass, a smaller-unit T12 with more cycles, and an oversized T20.
  - If the margin is thin, B3 effectively forbids the waivers. The rule self-adjusts; the owner does not need to rule twice.
- **S4: Whether any Phase 1 element inherits T11.** This determines whether T11 re-enters the list.

### Trade-off points (values questions for the owner, not facts)

- **T-1: Schedule versus one-way safety for T12.**
  - B3 accepts a Phase 1 that may run on a fallback with a worse cost per tonne, in exchange for not waiting on T12 TRL 6.
  - B1 accepts waiting.
  - No evidence settles this. It depends on how the owner values a signed-demand window under D-01 against architecture purity. I recommend B3, but this is the owner's call and should be recorded as such.
- **T-2: Phase 0 spend on fallbacks versus Phase 0 spend on primaries.**
  - Money spent qualifying a fallback is not spent advancing the primary.
  - This is the "capability programme, not a cost saving" framing of D-01, made concrete.

---

## 6. Evidence certainty

Likelihood (how probable) is kept separate from confidence (how good the evidence is). Every TRL estimate here is panel judgment, not test data.

| Claim | Likelihood | Confidence / GRADE | Basis |
|---|---|---|---|
| T18 current TRL is 2–4 | — | Low (three estimates span two levels; no cited test campaigns) | Panel table |
| T12 reaches TRL 6 for 150–300 t by a nominal KDP-0B | Unlikely (~20–35%) | Low | Lowest TRL and highest AD² in the group; no analogue at that payload class in an autonomous surface or proximity context |
| T20 reaches TRL 6 by KDP-0B | Likely (~60–75%) | Medium | Storage cell technology is mature terrestrially. The risk is environment (thermal cycling, dust, radiation) and microgrid management if GPT's scope is used. AD² 4–5 is the lowest in the group. |
| T09 reaches TRL 6 by KDP-0B | About as likely as not | Low | High-voltage distribution over regolith couples arcing, charging and dust; little directly relevant heritage |
| Remote sensing alone could satisfy the current target-gate text | Likely | Medium | Inferred from the gate structure as summarised; worth confirming against `gates-proposal.yaml` |
| Independent waivers stack into an untested joint failure | Very likely (structural) | High | Follows from B2's text, which contains no joint test |
| Gemini's T11 classification is a drafting inconsistency (prose vs YAML), not a considered position | Likely | Medium | Gemini's response was brief; prose and YAML disagree |

**What these probabilities are.** They are my judgment, offered as calibrated language so others can disagree in numbers. They are not elicited estimates. Before KDP-0A they should be replaced by a structured elicitation, using Cooke's classical method or SHELF, on T12 and T09 specifically.

---

## 7. Key assumptions

| # | Assumption | What would falsify it |
|---|---|---|
| K1 | The 0A scout mission carries a T18-class instrument capable of bulk grade assay | Scout payload definition at 0A mid-term review omits in-situ assay or limits it to surface spectroscopy. A3's provenance rule then cannot be met, and either the scout scope or the target gate must change. |
| K2 | Phase 1 does not reuse T11 hardware or software | Phase 1 concept baseline lists a scout-derived bus for prospecting, tugs or handling. T11 re-enters at TRL 6. |
| K3 | Credible TRL 6 fallbacks exist for T09 and T20, and plausibly for T12 | A fallback trade at 0A mid-term shows no fallback within, say, a 2× penalty on the affected subsystem. That item reverts to B1. |
| K4 | The economics model can represent fallback penalties at subsystem resolution | The economics gate model is top-down (cost per tonne) without subsystem hooks. B3's joint-fallback test becomes unauditable, and B1 is the safer default. |
| K5 | Waivers are granted by an authority independent of the Phase 1 advocate | Decision rights (RAPID) give the 0B programme manager waiver authority. Raise C3 weight; B1 gains. |

### Competing hypotheses for why GPT holds TRL 6 on T09, T12 and T20 (ACH)

The test was which hypothesis the panel record disconfirms least.

1. **H1: Waiver erosion (fewest disconfirmations).** GPT distrusts waiver processes at one-way gates. Its "substitutions reassessed" clause targets this.
   - B3 answers H1 directly: a waiver becomes a pass/fail check on fallback evidence.
2. **H2: Fallbacks would not close economics.** No disconfirming evidence, but no confirming evidence either. Nobody has run the joint case.
   - B3 makes this testable rather than assumed.
3. **H3: TRL 5 to 6 is a large step for these items.** Partially disconfirmed. GPT's own AD² for T09, T12 and T20 is 5, lower than its 6 for T11 and T18. That suggests GPT sees them as less hard, not harder.

If H1 is the real driver, B3 should be acceptable to GPT. If H2 is, the joint-fallback test will vindicate GPT empirically. Either way B3 is the better-structured rule.

---

## 8. Decision, warrant, accepted downside

### Recommended gate text

Drafted for `gates-proposal.yaml`:

```yaml
kdp_0b_technology_criteria:
  T18:
    class: project-ending
    criterion: >
      Bulk grade assay of the selected target obtained by a T18-class
      instrument operating at the target (TRL >= 7 by flight). Ground TRL 6
      alone does not satisfy KDP-0B. The target gate shall not pass on
      remote-sensing evidence without T18 in-situ confirmation.
    waiver: none
    if_phase1_assay_differs_from_scout_instrument: Phase 1 variant at TRL 6
  T11:
    class: 0A flight technology (not on KDP-0B list)
    governed_by: scout PDR, TRL 6
    re_entry: >
      If any Phase 1 element inherits T11 hardware or software, T11
      is added to KDP-0B at TRL 6, class architecture-change.
    failure_path: captured by target-gate pre-committed failure outcome
  T09, T12, T20:
    class: architecture-change
    reference_implementation: >
      The specific design (operating point, payload class, chemistry and
      control scope) named in the Phase 1 configuration baseline frozen at
      KDP-0B. Any post-KDP-0B substitution triggers reclassification and
      a re-run of the economics gate.
    criterion: TRL 6 in a relevant environment for the reference implementation
    waiver:
      permitted_to: TRL >= 5
      all_conditions_required:
        - named fallback implementation at TRL 6 in a relevant environment
        - economics gate passes in the joint-fallback case
          (every waived item on its fallback simultaneously)
        - fallback penalties carried in the Phase 1 baseline, not in reserve
        - waiver authority independent of the Phase 1 programme office
      if_no_qualified_fallback: no waiver (reverts to TRL 6, no waiver)
```

### Y-statement

In the context of a one-way KDP-0B gate under D-02, facing a panel split between "TRL 6 for all five" and "TRL ≥ 5 waiverable for the supporting three, 0A-only for the scouts", we chose to:
- bind T18 to flight-provenance evidence through the target gate;
- remove T11 from the list, with a re-entry condition;
- hold T09, T12 and T20 at TRL 6 with a waiver earned only by a qualified fallback that closes joint-fallback economics,

to achieve a gate that tests the actual irreversible consequence of each technology failing, accepting:
- that Phase 1 may start on a costlier fallback architecture, most likely for T12;
- that Phase 0 must fund fallback qualification;
- that KDP-0B cannot precede scout assay return.

### Toulmin structure

- **Grounds.** All three models classify T09, T12 and T20 as architecture-change. Two of three plus the headline classify T18 as project-ending. T11's classification is inconsistent across sources.
- **Warrant.** For a one-way gate, the right test of a technology is whether the commitment survives that technology's failure. For architecture-change items, a qualified fallback that closes economics answers this as well as TRL 6 on the primary. For a sampling technology that should already have flown, flight evidence answers it better than ground TRL.
- **Backing.** D-02's "stringency follows reversibility". The real-options logic of D-01.
- **Qualifier.** Probably the right rule for T09 and T20 (medium confidence). Plausibly right for T12, low confidence, contingent on S2. Very likely right for T18 and T11.
- **Rebuttal conditions.** The rule fails if:
  - fallback penalties are systematically underestimated (K4);
  - waiver authority is captured (K5);
  - no T12 fallback exists, in which case B1 holds for T12.

### Accepted downside, stated plainly

- A Phase 1 baseline carrying, for example, smaller-unit T12 handling with a cost-per-tonne penalty of unknown size.
- A KDP-0B date that is hostage to scout return.

I would rather slip the gate than pass it on an unmeasured grade.

---

## 9. Consequences

### Enables
- An economics-gate specification that must include a joint-fallback case. This is new work for the economics gate owner.
- Clean KDP-0B YAML with no drafter-dependent ambiguity. It also resolves the Gemini prose/YAML inconsistency on T11.
- A defined meaning for "selected reference implementation" that the other open choices can reuse, notably T25 and T26 if they land as architecture-change.

### Constrains
- **0A mid-term review** must deliver:
  - the scout payload definition confirming T18-class in-situ assay (K1);
  - a fallback trade for T09, T12 and T20 naming fallback implementations and their penalties;
  - a structured elicitation of T12 and T09 TRL trajectories.
- **Phase 0 budget** must carry fallback qualification lines, roughly one campaign each, likely smaller than the primary campaigns.
- **The KDP-0B schedule** must be set after nominal scout assay return plus analysis margin.
- **The target gate text** must be amended to forbid a remote-sensing-only pass.

### Related open decisions
- **T25 and T26.** If ruled architecture-change, they inherit B3 and should not get a separate rule.
- **Claude's split classes** (T02, T10, T14, T15, T22, T24) are unaffected. They stay at TRL 6 with no waiver pending ruling.

### Evidence that would change this ruling
1. **The scout scope excludes in-situ bulk assay.** A3 then fails, and the target gate needs an alternative provenance rule.
2. **The Phase 1 concept reuses T11.** T11 then returns at TRL 6.
3. **The fallback trade shows no TRL 6 fallback for T12 within a tolerable penalty.** T12 then reverts to B1, TRL 6 with no waiver. I would accept that without reopening the rule.
4. **The joint-fallback economics case fails with all three waived.** The rule then forbids waivers in practice. B3 converges to B1 empirically, which is the intended behaviour.
5. **Decision rights put waiver authority inside the Phase 1 programme office.** I would then switch my recommendation to B1, because B3's protection depends on independent adjudication.