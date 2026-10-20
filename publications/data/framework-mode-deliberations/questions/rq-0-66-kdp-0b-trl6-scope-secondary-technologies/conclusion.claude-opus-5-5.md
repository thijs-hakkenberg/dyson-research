---
questionId: "rq-0-66"
questionSlug: "kdp-0b-trl6-scope-secondary-technologies"
type: "discussion-conclusion"
generatedBy: "claude-opus-5-5"
generated: "2026-10-17"
framework: "18f503fe4ec6"
roundCount: 1
terminationReason: "unanimous-conclude"
role: "alternate synthesis"
---

## Summary

All three models rejected two options: the null option (leave the panel split as it is) and a blanket requirement that all five technologies reach TRL 6 at KDP-0B. Each argued that the five do not form one class. They split the question the same way: T11 and T18, the 0A flight technologies, in one group; T09, T12 and T20, the supporting systems, in the other.

On **T11** the panel largely converged: no separate KDP-0B TRL 6 demonstration should be required.
- Claude would remove T11 from the KDP-0B list, with a re-entry condition if Phase 1 inherits T11 hardware or software.
- Gemini would assess it "via mission data, not pre-gate TRL".
- GPT would inherit applicable 0A evidence and gate only outstanding critical functions.

On **T18** Claude and GPT converged in substance: target-specific evidence must back the gate, not a ground TRL label alone.
- Claude requires in-situ flight provenance and would forbid a target-gate pass on remote sensing alone.
- GPT requires TRL 6 for the sampling and assay capability plus target-specific evidence that meets predeclared uncertainty criteria.
- Gemini's chosen option (O3) exempts T18 from pre-gate TRL in favour of mission data. Its own matrix, however, rated the hybrid O4 (T18 at TRL 6) higher on risk containment, and it named T18 as its sensitivity point.

On **T09, T12 and T20** the panel only partly converged. Claude and GPT both proposed TRL 6 as the default for the selected reference implementation. Both would allow a lower-maturity exception only when an independently reviewed alternative is demonstrated and preserves the investment case. They differ on the details:

| Detail | Claude | GPT |
|---|---|---|
| Maturity of the alternative | Fallback must be at TRL 6 | "Sufficiently demonstrated for its assigned role" |
| Economics test | Explicit joint-fallback test: all waived items on their fallbacks at once | Not stated |
| Fallback penalties | Carried in the Phase 1 baseline | Not stated |
| Other routes and controls | Not stated | Deferral as an alternative route; latest substitution date; automatic stop trigger |

Gemini held the original tiered position: TRL ≥ 5 with a waiver, a defined fallback and a funded maturation path. All three peer votes rated Gemini's response NEUTRAL. Claude's and GPT's responses each received three APPROVE votes.

## Decision record

The panel did not fully converge on Group B, and Gemini's T18 position differs. One Y-statement per position follows.

**Position 1: Claude Opus 5.5 (A3 + B3)**
> In the context of a one-way KDP-0B gate under D-02, facing a split between "TRL 6 for all five" and "TRL ≥ 5 waiverable / 0A-only for scouts", we chose to bind T18 to flight-provenance in-situ assay through the target gate (no remote-sensing-only pass), remove T11 from the list with a re-entry condition, and hold T09/T12/T20 at TRL 6 with a waiver to TRL ≥ 5 earned only by a TRL 6 fallback that closes joint-fallback economics, with penalties carried in the baseline and an independent waiver authority. This achieves a gate that tests the actual irreversible consequence of each technology failing, accepting a possibly costlier fallback architecture (most likely T12), Phase 0 spend on fallback qualification, and a KDP-0B date that cannot precede scout assay return.

- **Warrant:** a one-way gate should test whether the commitment survives the technology's failure. For architecture-change items, a qualified fallback that closes economics answers that as well as TRL 6 on the primary does.
- **Qualifier:**
  - T09 and T20: "probably", medium confidence.
  - T12: "plausibly", low confidence, contingent on a fallback existing.
  - T18 and T11: "very likely".
- **Rebuttal conditions:** underestimated fallback penalties; captured waiver authority; no T12 fallback.

**Position 2: Gemini 3.1 Pro (O3, tiered exemption)**
> In the context of defining KDP-0B gate criteria, facing a panel split on five non-core technologies, we chose to assess T11/T18 via 0A mission data rather than pre-gate TRL, and to accept T09/T12/T20 at TRL 6 or TRL 5 with an approved waiver, a defined fallback architecture and a fully funded Phase 1 maturation plan. This achieves schedule realism and architectural flexibility, accepting the risk that a waivered TRL 5 technology may require an expensive Phase 1 redesign.

- **Warrant:** architecture-change failures degrade efficiency rather than end the project. Applying pre-gate TRL 6 to self-proving 0A flight technologies creates a circular dependency.
- **Qualifier:** Gemini stated "High" certainty on both claims: that fallbacks exist and that T11/T18 are 0A flight technologies.

**Position 3: GPT-6.1 Sol (O3, dependency-based gate with inherited evidence)**
> In the context of D-01's gated real option and D-02's no-waiver rule, facing disputed technology labels and potentially irreversible dependencies, we chose capability-based TRL 6 gating. This means inherited 0A evidence where configuration, envelope and functions remain applicable. It means TRL 6 for T09/T12/T20 where KDP-0B creates irreversible dependence. TRL ≥ 5 is allowed only with an independently verified, funded, interface-compatible alternative or deferral that preserves demand, economics, safety and licence, with a named owner, latest substitution date and automatic stop trigger. This achieves protection of the investment case without duplicate maturation, accepting more assurance effort and the possibility that all five still end up at TRL 6.

- **Warrant:** irreversibility, not list membership, determines stringency.
- **Qualifier:** any unproven substitution defaults to TRL 6. GPT rated the evidence that executable alternatives exist as "very low" certainty.

## Decision-quality audit

| Response (Round 1) | Weakest link named in votes | Missing or unsupported scaffold steps | Trade-off points (values, not facts) |
|---|---|---|---|
| **Claude Opus 5.5** | Information (Claude self-vote, GPT); "none" (Gemini) | TRL estimates and probabilities are the model's own judgment, not elicited; Claude proposes Cooke or SHELF elicitation before KDP-0A. The remote-sensing loophole rests on the gate text as summarised and has not been checked against `gates-proposal.yaml`, which Claude flags itself. Group B robustness margin is narrow (~0.35); B1 wins if C2 falls below ~0.10 and C1 rises to ~0.45. | T-1: schedule against one-way safety for T12, explicitly left to the owner. T-2: Phase 0 spend on fallbacks against primaries. |
| **Gemini 3.1 Pro** | Reasoning (Claude, GPT); alternatives (Gemini self-vote) | Matrix not aggregated. O4 is rated higher than O3 on risk containment, yet O3 is chosen without explanation. The named T18 sensitivity point is left unresolved. "High" certainty on fallbacks is unsupported (Claude, GPT). No joint-failure or combined-economics test (Claude, GPT). Null option dismissed without full evaluation, and no ACH step (Gemini self-vote). | Weights of 10/8/6 for risk, schedule and flexibility encode a higher value on schedule than Claude's or GPT's weights. That is a values difference, not a factual one. |
| **GPT-6.1 Sol** | Commitment (Claude, GPT self-vote); "none" (Gemini) | The commitment is conditional and less concrete than Claude's; it may conclude that all five need TRL 6 (Claude, GPT). GPT states it did not inspect the source files. Its cost-saving claim is rated low certainty, with no costed work breakdown. "Sufficiently demonstrated for its assigned role" is left to judgment. | Demonstration expenditure against conditional authorisation; delay against implementation flexibility; tolerable residual rework risk. GPT labels all three as owner choices. |

Cross-cutting point: the main remaining difference between Claude and GPT is how specific the waiver test should be (a TRL 6 fallback plus a joint-fallback economics case, against "sufficient for role" plus stop triggers). Evidence can partly inform this, but setting the threshold is a drafting and values choice. The difference between Gemini and the others on waiver strength is principally a trade-off point: the value placed on schedule realism against one-way safety.

## Key Points

- **Rejected by all three:** the null option (O0/A0/B0/O1). Claude and GPT called it unexecutable or drafter-dependent. Gemini said it would make KDP-0B unexecutable.
- **Blanket TRL 6 rejected as the general rule:**
  - Claude: B1 is "safe but blunt" and lets T12 hold Phase 1 hostage.
  - GPT: O1 stays as the default where reversibility is unproven.
  - Gemini: it forces massive delays.
- **T11, broadly convergent:** no duplicate KDP-0B demonstration.
  - Claude adds a re-entry trigger if Phase 1 inherits T11.
  - GPT adds gating of any continuing scout capability on which later irreversible spend depends.
- **T18, Claude and GPT aligned:** target-specific measured evidence is required, and a ground TRL label is insufficient.
  - Claude uniquely requires amending the target gate to forbid a remote-sensing-only pass.
  - Claude uniquely requires that KDP-0B be scheduled after scout assay return.
- **"Selected reference implementation":**
  - Claude defines it as the design (operating point, payload class, chemistry, control scope) frozen in the Phase 1 configuration baseline at KDP-0B. Any later substitution triggers reclassification and an economics re-run.
  - GPT defines it as the configuration used in the approved architecture, performance model, cost estimate, interfaces and qualification plan, "not merely a preferred candidate".
  - The two definitions are compatible. Gemini gave none.
- **Waiver stacking:** Claude identified that independent waivers can combine into an untested joint failure and wrote a joint-fallback test into the rule. GPT's vote on Gemini cited the same gap. GPT's own rule text requires each alternative to preserve the case but does not state a joint test.
- **Independent waiver authority:**
  - Claude makes it a condition and says it would switch to B1 if waiver authority sat inside the Phase 1 office.
  - GPT requires "independent review".
  - Gemini does not address it.
- **T12** is singled out by Claude as least likely to reach TRL 6 (~20–35%, low confidence). GPT requires a validated scaling argument if a small demonstration is used for the 150–300 t regime.
- **T20 scope:** GPT would assess storage together with microgrid functions (transients, fault isolation, degraded operation).

## Unresolved Questions

1. **Group B waiver test:** must the fallback be at TRL 6 (Claude) or only "sufficiently demonstrated for its assigned role" (GPT)? Is an explicit joint-fallback economics case required (Claude), and is deferral an acceptable alternative route (GPT)?
2. **Gemini's position:** does Gemini hold O3 (T18 exempt from pre-gate TRL) or O4 (T18 at TRL 6)? Its matrix and choice are inconsistent.
3. **Target gate text:** does the current target gate permit a pass on remote sensing alone? Claude rated this "likely" at medium confidence, unconfirmed against `gates-proposal.yaml`.
4. **T12 fallback:** does a T12 fallback exist that can be qualified within a tolerable penalty? Claude names 30–60 t handling units or teleoperated assist as plausible. GPT rates substitution evidence for all three as very low certainty.
5. **Timing:** will scout assay data arrive before the planned KDP-0B date? (Claude S1; Gemini assumption 2.)
6. **Commitment boundary:** what does KDP-0B actually authorise that would make replacing T09, T12 or T20 prohibitive? (GPT's primary sensitivity point.)
7. **Waiver authority:** who holds waiver or exception authority under the decision-rights model? (Claude K5.)
8. **Economics model resolution:** can the economics model represent subsystem-level fallback penalties? (Claude K4.)
9. **T11 reuse:** will any Phase 1 element inherit T11 hardware or software? (Claude S4/K2; GPT's continuing-scouting assumption.)

## Recommended Actions

Each action is attributed to the model(s) that proposed it.

1. **Owner ruling on Group B.** Choose between Claude's B3 text and GPT's dependency-based text, or combine them. Record T-1 (schedule against one-way safety for T12) explicitly as an owner values call (Claude, GPT).
2. **Check the target gate text.** Verify `gates-proposal.yaml` for the remote-sensing loophole and amend it if confirmed (Claude).
3. **0A mid-term review deliverables:**
   - Scout payload definition confirming T18-class in-situ assay (Claude K1).
   - Fallback trade for T09, T12 and T20 naming implementations and penalties (Claude). GPT's equivalent is a costed substitution case per proposed exception.
   - Structured elicitation (Cooke or SHELF) of the T12 and T09 TRL trajectories (Claude).
4. **Before KDP-0B:** produce an independently reviewed dependency map and commitment schedule, with a latest substitution date and stop trigger per exception (GPT).
5. **Extend the economics gate specification.** Add a joint-fallback case with subsystem-level hooks (Claude).
6. **Set the KDP-0B schedule** after nominal scout assay return plus analysis margin (Claude).
7. **Fix waiver authority outside the Phase 1 programme office** in the decision-rights record (Claude). GPT requires independent review.
8. **Ask Gemini** to reconcile its O3/O4 choice on T18 and to support its "High" certainty on fallbacks (votes by Claude and GPT).
9. **Apply the outcome to T25 and T26.** If those are ruled architecture-change, apply the same Group B rule rather than writing a separate one (Claude).

```yaml
questionId: "rq-0-66"
topics:
  - id: null-option-and-blanket-trl6
    topic: Leave the split unresolved or apply blanket TRL 6 to all five
    positions:
      - statement: Reject the null option; reject blanket TRL 6 as the general rule (GPT keeps TRL 6 as the default where reversibility is unproven)
        models: [Claude Opus 5.5, Gemini 3.1 Pro, GPT-6.1 Sol]
        evidence: Null leaves the gate drafter-dependent or unexecutable; blanket TRL 6 duplicates 0A evidence and lets T12 delay Phase 1
    resolution_status: resolved
    priority: high
  - id: t11-kdp0b-membership
    topic: Whether T11 belongs on the KDP-0B list
    positions:
      - statement: Remove from KDP-0B list; govern at scout PDR (TRL 6); re-enter at TRL 6 as architecture-change if Phase 1 inherits T11 hardware or software
        models: [Claude Opus 5.5]
        evidence: Bus maturity has no decision value at 0B; failure is captured by target-gate failure outcome
      - statement: Assess via 0A mission data, not pre-gate TRL
        models: [Gemini 3.1 Pro]
        evidence: The 0A flight is the maturation path; pre-gate TRL 6 is circular
      - statement: Inherit applicable 0A evidence; gate outstanding critical or continuing scout functions at TRL 6
        models: [GPT-6.1 Sol]
        evidence: Mission completion alone does not establish applicability of configuration, envelope and functions
    resolution_status: partially-resolved
    priority: medium
  - id: t18-criterion
    topic: KDP-0B criterion for T18 sampling and assay
    positions:
      - statement: Project-ending; satisfied only by in-situ flight assay at the target (TRL >= 7 by flight); target gate must not pass on remote sensing alone; no waiver
        models: [Claude Opus 5.5]
        evidence: Ground TRL 6 does not make an unmeasured target investable; current gate text may allow a remote-sensing pass
      - statement: TRL 6 for the relevant sampling and assay capability plus target-specific evidence meeting predeclared uncertainty and representativeness criteria
        models: [GPT-6.1 Sol]
        evidence: Instrument maturity is distinct from target adequacy
      - statement: Assessed via 0A mission data rather than pre-gate TRL (O3), although its own matrix rated the hybrid O4 (T18 at TRL 6) higher on risk containment
        models: [Gemini 3.1 Pro]
        evidence: T18 is self-proving through the 0A flight; Gemini names T18 classification as its sensitivity point
    resolution_status: partially-resolved
    priority: critical
  - id: t09-t12-t20-waiver-conditions
    topic: Default criterion and waiver conditions for T09, T12, T20
    positions:
      - statement: TRL 6 default; waiver to TRL >= 5 only with a TRL 6 fallback, joint-fallback economics pass, penalties in the baseline and independent authority; no fallback means no waiver
        models: [Claude Opus 5.5]
        evidence: A funded path is a budget line, not evidence; independent waivers stack into an untested joint failure
      - statement: TRL 6 where KDP-0B creates irreversible dependence; TRL >= 5 only with an independently verified, funded, interface-compatible alternative or deferral preserving demand, economics, safety and licence, with owner, latest substitution date and stop trigger
        models: [GPT-6.1 Sol]
        evidence: Irreversibility, not list membership, sets stringency; substitution evidence currently very low certainty
      - statement: TRL 6 or TRL 5 with approved waiver, defined fallback architecture and fully funded Phase 1 maturation plan
        models: [Gemini 3.1 Pro]
        evidence: Architecture-change failures only degrade efficiency; known fallbacks exist (stated High certainty, challenged by Claude and GPT)
    resolution_status: partially-resolved
    priority: critical
  - id: selected-reference-implementation
    topic: Meaning of "selected reference implementation"
    positions:
      - statement: Design (operating point, payload class, chemistry, control scope) in the Phase 1 configuration baseline frozen at KDP-0B; post-0B substitution triggers reclassification and an economics re-run
        models: [Claude Opus 5.5]
        evidence: Needed for an auditable one-way gate and reusable for T25 and T26
      - statement: Configuration used in the approved architecture, performance model, cost estimate, interfaces and qualification plan, not merely a preferred candidate
        models: [GPT-6.1 Sol]
        evidence: Criticality follows the committed dependency chain
    resolution_status: partially-resolved
    priority: high
  - id: waiver-authority
    topic: Who adjudicates waivers or exceptions
    positions:
      - statement: Authority independent of the Phase 1 programme office; if not, switch to no-waiver TRL 6
        models: [Claude Opus 5.5]
        evidence: Protection depends on independent adjudication; one-way gates fail through erosion
      - statement: Independent review must verify each exception
        models: [GPT-6.1 Sol]
        evidence: Unreviewed fallback evidence does not earn gate credit
    resolution_status: partially-resolved
    priority: high
  - id: kdp0b-schedule-vs-scout-return
    topic: Whether KDP-0B must follow scout assay return
    positions:
      - statement: KDP-0B scheduled after nominal scout assay return plus analysis margin; accept the slip
        models: [Claude Opus 5.5]
        evidence: The target gate cannot honestly pass without assay data
      - statement: If 0A cannot deliver decision-quality assay before 0B, hold 0B, obtain more evidence or change target
        models: [GPT-6.1 Sol]
        evidence: A TRL label is not a substitute for missing target knowledge
      - statement: Scout failure to fly before KDP-0B falsifies the T18 exemption
        models: [Gemini 3.1 Pro]
        evidence: Stated as a falsification condition for its assumption 2
    resolution_status: partially-resolved
    priority: high
  - id: schedule-vs-safety-tradeoff
    topic: Owner values trade-off between schedule and one-way safety, especially for T12
    positions:
      - statement: Accept a costlier fallback Phase 1 rather than wait on T12 TRL 6; explicitly an owner call
        models: [Claude Opus 5.5]
        evidence: Signed-demand window under D-01 against architecture purity; no evidence settles it
      - statement: Schedule realism weighted 8/10 against risk containment 10/10; favours waiverable treatment
        models: [Gemini 3.1 Pro]
        evidence: Avoiding multi-year delay for substitutable systems
      - statement: Demonstration spend, delay and residual rework risk are owner choices; unproven substitution defaults to TRL 6
        models: [GPT-6.1 Sol]
        evidence: Testing informs but cannot determine the preferred balance
    resolution_status: open
    priority: high
```