---
questionId: "rq-0-68"
questionSlug: "demand-gate-definitions"
modelId: "claude-opus-5-5"
modelName: "Claude Opus 5.5"
roundNumber: 1
generated: "2026-10-17"
type: "discussion-response"
---

# g-demand: ruling on "within 3×" and "signed"

## 1. Frame & decision type

**Decision type.** This is a property decision about the definition of one gate criterion. The definition then acts as an executive constraint on how 0B is sized, because D-01 sizes 0B "by signed Phase 1 demand". The definition therefore decides 0B scale.

**Reversibility.**
- **The definition itself** is two-way until KDP-0B and costs little to change before then.
- **What it governs** is one-way. KDP-0B commits capital to a 0B plant at a chosen nameplate.

Under D-02, stringency follows reversibility. The definition must be written to the one-way standard now, while changing it is still cheap.

**Cynefin domain.** The wording question is *complicated*: there is a right answer and analysis finds it. Whether real demand will exist is *complex*, and no definition can settle it. The definition's job is narrower: make the gate objectively passable or failable, and stop the project from certifying its own demand.

**Problem with the status quo.** GPT is right that, as written, the gate has no numerator, denominator or epoch. A reviewer could pass or fail the same evidence. A gate that cannot be failed is not a gate.

## 2. Criteria and weights (stated before options)

Swing weights reflect how much the options differ on each criterion, not how important the criterion sounds in the abstract.

| # | Criterion | Weight | Why this weight fits the range |
|---|---|---|---|
| C1 | **Objective passability.** Two independent reviewers given the same evidence reach the same verdict. | 0.30 | Options range from "unpassable/arbitrary" (null) to fully mechanical. This is the widest swing, and it is the failure GPT identified. |
| C2 | **Resistance to circularity and self-certification.** The project cannot manufacture the demand that justifies its own next phase. | 0.25 | Wide swing, from "the 0B team writes its own demand memo" to "only third-party money counts". This is Claude's circularity flag, the most likely way the gate silently fails. |
| C3 | **Fidelity to D-01/D-02.** 0B is a real option sized by demand. The fallback "0A only, Earth supply" stays live. | 0.20 | Moderate swing. Most options respect D-01 in spirit. The timing-only and no-gate options do not. |
| C4 | **Feasibility / option preservation.** The bar is attainable for a first-of-kind space-resource programme, so 0B is not killed by definition. | 0.15 | Moderate swing. Only the external-offtaker-only option risks making the gate structurally unpassable. |
| C5 | **Evidence burden.** The cost of producing and auditing the evidence. | 0.10 | Narrow swing. Every serious option needs a specification, schedule and budget artefact anyway, because T22 needs a product specification regardless. |

**Musts (Kepner-Tregoe screen) before scoring:**
- M1: The criterion names numerator, denominator, units and epoch.
- M2: It contains a test for "signed" that a project-internal memo cannot satisfy alone.

## 3. Options

**O0 — Null: leave the panel split as recorded.**
- Fails M1. KDP-0B reviewers would choose a reading at the gate, after the evidence is known.
- That is the worst time to define a criterion, because the reading can be chosen to fit the result.
- *Rejected.*

**O1 — Quantity reading, "signed" left to the owner later (Claude/Gemini as stated).**
- Captures the right meaning: kt/yr against capacity, per rq-0-58.
- Fails M2. It defers exactly the hard part.
- *Rejected as incomplete. Its quantity core is retained in O3.*

**O2 — Timing reading (GPT's proposal).** The accepted delivery date span is ≤ 3× the elapsed time from a common epoch.
- It is objective.
- It answers a question D-01 does not ask. D-01 says demand *sizes* 0B, and sizing is a quantity.
- A timing-only gate could pass a 10 t/yr order against a 2 kt/yr plant.
- *Rejected as the meaning of "3×". GPT's underlying concern, demand that is real in quantity but arrives too late, is valid. It is retained as a separate timing clause with its own bound, not by overloading "3×".*

**O3 — Composite definition (recommended).** Four parts:
1. Quantity ratio with fully defined terms: nameplate ≤ 3 × accepted demand.
2. A separate delivery-window clause.
3. A counterfactual test for "signed".
4. A sizing cap.

**O4 — Strict external.** Only binding third-party offtake counts, and 0B is sized exactly to it.
- Maximal on C2.
- In practice it very likely makes the gate unpassable at KDP-0B, because no external market for kt-scale space-processed material is likely to exist by then.
- It collapses D-01's real option into "never".
- *Rejected as the rule. Kept as a credit, not a requirement (see O3).*

**O5 — Delete g-demand and rely on g-economics.**
- The economics gate prices demand but does not verify it exists.
- Removing the only gate that asks "who takes delivery?" is the classic megaproject failure mode: capacity built ahead of committed use.
- *Rejected.*

## 4. Assessment matrix (QOC; scores 1–5)

| Option | C1 Passability (0.30) | C2 Circularity (0.25) | C3 D-01 fidelity (0.20) | C4 Feasibility (0.15) | C5 Burden (0.10) | Weighted | Musts |
|---|---|---|---|---|---|---|---|
| O0 Null | 1 | 1 | 2 | 4 | 5 | **2.05** | Fails M1, M2 |
| O1 Quantity, signed TBD | 3 | 1 | 4 | 4 | 4 | **3.00** | Fails M2 |
| O2 Timing only | 4 | 2 | 1 | 3 | 4 | **2.75** | Passes M1 only |
| **O3 Composite** | **5** | **4** | **5** | **4** | **3** | **4.40** | **Passes** |
| O4 External only | 5 | 5 | 2 | 1 | 4 | **3.70** | Passes |
| O5 No gate | 2 | 1 | 1 | 5 | 5 | **2.15** | Fails M1, M2 |

O3 leads by 0.7 over its nearest rival (O4). The gap closes only if C4 is down-weighted to near zero, that is, if the owner would rather lose 0B than risk circular demand. That is a values question (§5), not an analytical one.

## 5. Sensitivity vs trade-off points

**Sensitivity points** are parameters that strongly move one attribute:

- **S1 — Planning availability × yield factor (η).** The sizing cap is roughly accepted demand ÷ η, capped at 3× accepted demand.
  - If first-of-kind ISRU plant η is about 0.3–0.5 (plausible for early operations), the 3× cap binds almost exactly at the honest sizing.
  - If η turns out to be about 0.8, 3× is generous and invites overbuild.
  - The ratio's meaning is therefore highly sensitive to η, which is why η must be declared and justified in the 0B plan, not assumed.
- **S2 — Averaging window length.** Annualising signed demand over a 3-year window versus the first operating year changes the numerator by a large factor during ramp-up. I recommend a 3-year window starting at the planned first-nameplate date.
- **S3 — Which internal demand qualifies.** The counterfactual test (below) is the single strongest lever on C2. Loosen it and C2 collapses.

**Trade-off points** are values questions, not facts to settle:

- **T1 — Rigour vs option survival (C2 vs C4).**
  - Counting internal Phase 1 demand at all is a trade.
  - Excluding it (O4) makes the gate honest and probably unpassable.
  - Including it under a counterfactual test accepts some residual self-dealing risk to keep 0B alive.
  - **The owner must state which way they lean.** I lean to inclusion under the test, because D-01 explicitly names *Phase 1* demand as the sizing basis. The owner already accepted that internal demand counts. The question is only how to make it non-circular.
- **T2 — Minimum economic or technical scale vs overproduction (Claude vs GPT on sizing).**
  - GPT: "3× is not permission to overproduce."
  - Claude: demand sizes 0B.
  - Both hold if the 3× is read as a **ceiling** on the nameplate-to-demand ratio, with excess requiring justification. If a pilot plant cannot be built below some minimum scale, that is a real conflict, and it is resolved by an explicit owner waiver recorded against g-economics, not by stretching g-demand.
  - **I keep this disagreement visible.** GPT's "size only to accepted demand" is stricter than my ruling, which allows up to 3× with a declared η.

## 6. Evidence certainty

Likelihood (how probable) and confidence (how good the evidence is) are kept separate.

| Claim | Likelihood | Evidence certainty (GRADE) / confidence | Basis |
|---|---|---|---|
| The drafters meant a quantity ratio, not timing | Likely | Moderate / medium | D-01 "sized by signed Phase 1 demand" is a sizing statement. Claude and Gemini both read rq-0-58 as kt/yr against capacity. GPT's ambiguity point stands, and the text never says so explicitly. |
| No binding external offtaker for kt-scale space material will exist by KDP-0B | Very likely | Low / medium | No such market exists today. Extrapolation over the Phase 0 horizon is speculative. |
| Project-internal demand estimates are optimistically biased if unpoliced | Likely | Moderate / high | Documented optimism bias and strategic misrepresentation in large infrastructure projects (Flyvbjerg's work on megaproject cost and demand overruns). Transfer to space programmes is by analogy. |
| First-of-kind process plants operate well below nameplate during ramp-up | Very likely | Moderate / medium | Well established qualitatively in process-industry ramp-up experience. Magnitude for space ISRU is unknown, hence S1. |
| The counterfactual (Earth-supply) test removes most circularity | About as likely as not to fully succeed; likely to remove most of it | Very low / low | This is a design argument, not tested evidence. Residual risk: Phase 1 baselines can themselves be inflated. |

The weakest evidence sits under my own recommendation (the counterfactual test). That is why §7 gives it an explicit falsifier and §8 an accepted downside.

## 7. Key assumptions and falsifiers

**ACH on what "within 3×" means.**

| Hypothesis | Disconfirming evidence | Rank |
|---|---|---|
| H1: quantity ratio (nameplate vs demand) | None in the record. D-01 wording supports it. | **1 — least disconfirmed** |
| H3: both quantity and timing intended | Only one multiplier appears. Two dimensions under one number is unusual drafting. | 2 |
| H2: timing ratio | D-01 says demand *sizes* 0B, and a timing ratio cannot size anything. | 3 — most disconfirmed |

**Assumptions:**

- **A1. Phase 1 has a baseline in which Earth-supplied material meets some need.**
  - *Falsified if* the Phase 1 architecture has no Earth-supply variant, that is, if the material is useful only when produced in space. Then the counterfactual test cannot be run, and an alternative test is needed, such as a funded Phase 1 line item approved by an authority independent of 0B.
- **A2. A signatory distinct from the 0B proposer exists** (Phase 1 programme authority or owner).
  - *Falsified if* the same team owns both budgets. Then "signed" degenerates and only O4 is honest.
- **A3. 3× approximates honest early-operation overcapacity.**
  - *Falsified if* 0A pilot data show η ≥ 0.7 early, in which case tighten to 2×, or η ≤ 0.25, in which case the plant is not ready for 0B anyway (refer to the TRL gate).
- **A4. T22 qualification needs a frozen product specification.**
  - *Falsified if* T22 is re-scoped to be specification-agnostic. Then the specification requirement could be relaxed, though I would still keep it, because an order without a specification is not demand.

**Premortem.** Suppose 0B is built and idle three years later. The most likely story: Phase 1 "demand" was a planning line nobody funded, the plant was sized at 3× a soft number, and Earth supply turned out cheaper. Every clause below is aimed at one step of that story.

## 8. Decision, warrant, accepted downside

### Ruling: adopt O3

**Proposed gate text** (for `gates-proposal.yaml`, g-demand):

```yaml
g-demand:
  applies_at: KDP-0B   # one-way; D-02 stringency
  definitions:
    accepted_demand:
      units: kt/yr
      computation: >
        Sum of qualifying demand instruments, annualised over the
        averaging window, counting only quantity deliverable to the
        named node within the window.
      averaging_window: >
        3 years starting at planned first-nameplate date (epoch E0),
        as baselined in the 0B plan at KDP-0B.
    nameplate: >
      0B design output in kt/yr at the delivery node, per rq-0-58.
    planning_factor_eta: >
      Declared availability x yield for years 1-3, with basis
      (0A data where available).
  qualifying_instrument:   # meaning of "signed"; all must hold
    - product specification sufficient to qualify T22
    - quantity, delivery node, dated delivery schedule
    - signatory with budget authority independent of the 0B proposer
      (Phase 1 programme authority, the owner, or an external party)
    - committed funding for the purchase, OR a costed Earth-supply
      line in the Phase 1 baseline that this demand displaces
      (counterfactual test: the demand must exist if 0B is cancelled)
    - not conditional on 0B approval
    - letters of intent, MoUs and planning assumptions do not qualify
  pass_criteria:
    quantity: nameplate <= 3 x accepted_demand
    timing: first qualifying delivery due no later than E0 + 24 months
    sizing_cap: >
      nameplate <= min(3 x accepted_demand, accepted_demand / eta).
      Any nameplate above accepted_demand requires the eta basis on
      record. Exceeding the cap requires an owner decision logged
      against g-economics, not g-demand.
  credit:
    external_offtake: >
      Reported separately; strengthens g-economics; not required.
  fail_outcome: >
    Pre-committed: 0A only, Earth supply (per gate fallback),
    or resize 0B to pass.
```

**How this resolves each point of disagreement:**
- **"Within 3×"** is a quantity ratio: nameplate over accepted demand, in kt/yr, over a defined window from E0.
- **GPT's timing concern** becomes its own 24-month clause, not a second meaning of "3×".
- **Claude's circularity flag** is answered by the counterfactual test plus an independent signatory. Internal Phase 1 demand counts only if it would exist without 0B. Earth supply is the counterfactual, which ties the gate to the pre-agreed fallback.
- **On sizing**, 3× is a ceiling and never a target. GPT's stricter "size only to accepted demand" is recorded as a dissent the owner can adopt by setting the cap to 1×.

**Y-statement.** In the context of a one-way KDP-0B commitment sized under D-01 by signed Phase 1 demand, facing an undefined ratio and a buyer that is the project itself, we chose a quantity-ratio definition with a separate timing clause, a counterfactual "signed" test and a 3× sizing ceiling, to achieve an objectively passable gate that the project cannot satisfy by self-certification, accepting that internal Phase 1 baselines can still be inflated and that a plant with a high minimum viable scale may fail the gate.

**Toulmin structure:**
- **Grounds:** D-01 wording; rq-0-58 units; GPT's unpassability finding; Claude's circularity flag; megaproject optimism-bias evidence.
- **Warrant:** a gate protecting a one-way door must be decidable before the evidence arrives and must test demand that exists independently of the decision it justifies.
- **Backing:** D-02's stringency-follows-reversibility principle.
- **Qualifier:** likely correct as the intended meaning. Medium confidence that the counterfactual test is sufficient.
- **Rebuttal conditions:** A1 or A2 false; 0A η data outside 0.25–0.7.

**Accepted downside.** The gate may block a 0B that a bolder owner would build on strategic grounds. That is intended. Strategic builds go through an explicit owner decision, not through a loosened demand gate.

**Evidence that would change the ruling:**
1. A Phase 1 architecture with no Earth-supply variant (A1 false). Replace the counterfactual test with an independent-authority funded line item.
2. Shared 0B/Phase 1 budget authority (A2 false). Move to O4 for internal demand.
3. 0A ramp-up data. Retune the 3× ceiling to the measured η.
4. The drafters of rq-0-58 confirming a timing intent. Swap the clause roles, though D-01 would then need amending.

## 9. Consequences

**Enables:**
- An objective KDP-0B verdict.
- The 0A mid-term review can check *leading indicators*: draft specification, named node, and whether the Phase 1 authority has opened a costed Earth-supply line.
- T22 gets a frozen specification target.

**Constrains:**
- 0B nameplate is now bounded by documented demand and η. The economics gate must use the same accepted-demand figure, with no separate optimistic case.
- Phase 1 planning must carry an Earth-supply baseline, which is good practice anyway.
- The 0B team cannot be the signatory.

**Follow-on owner decisions unlocked:**
- (a) Lean on T1: confirm internal demand counts under the test.
- (b) Lean on T2: 3× ceiling (my ruling) or 1× (GPT's dissent).
- (c) Accept or adjust the 24-month timing bound and 3-year window.
- (d) Name the independent signatory role in `decisions.md`.

**Kept disagreements:**
- GPT's 1× sizing position versus my 3×-with-η ceiling stands unaveraged for the owner.
- Gemini's silence on "signed" is recorded as silence, not assent.