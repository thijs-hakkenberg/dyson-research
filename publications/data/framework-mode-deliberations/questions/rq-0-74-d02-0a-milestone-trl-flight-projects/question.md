---
questionId: "rq-0-74"
slug: "d02-0a-milestone-trl-flight-projects"
title: "How should D-02's 'TRL 4–5 for internal 0A milestones' apply to 0A flight projects (scouts, pathfinder)?"
questionType: "discussion"
priority: "high"
status: "investigating"
sourcePhase: "phase-0"
sourceBOMItemId: "bom-0-7"
sourceBOMItemSlug: "organizational-infrastructure"
sourceBOMItemName: "Organizational Infrastructure"
relatedBOMItems:
  - "bom-0-7"
relatedResearchQuestions:
  - "rq-0-62"
  - "rq-0-63"
  - "rq-0-76"
tags:
  - "gates"
  - "trl"
  - "decision-frameworks"
createdDate: "2026-10-18"
---

## Background

The Phase 0 TRL re-baseline (work package WP-A, `reconciliation/phase-0/trl/`) has produced a gate proposal under owner decision D-02: three programme decisions (KDP-0A, a 0A mid-term review, KDP-0B), four discriminating gates TRL cannot express (target, demand, economics, licence) and pre-committed failure outcomes. The panel (Claude Opus 5.5, Gemini 3.1 Pro, GPT-6.1 Sol) agreed on that structure, on TRL 6 in a relevant environment with no waiver for project-ending technologies at KDP-0B, and on the fallback "0A only, Earth supply". It left eleven choices for the owner. This question is one of them.

D-01 (accepted): fund 0A; hold 0B as a gated real option sized at the gate by signed Phase 1 demand; call Phase 0 a capability programme, not a cost saving. D-02 (accepted): stringency follows reversibility; one-way gates (KDP-0B) need TRL 6 in a relevant environment for project-ending technologies with no waivers; two-way internal 0A milestones need TRL 4–5. Gemini's gate response was brief, so several positions below are Claude against GPT; where Gemini is silent that is not agreement.

Sources: `reconciliation/phase-0/trl/round-1/gates/synthesis/gates.md`, `gates-proposal.yaml`, `trl-baseline.yaml`, `reconciliation/phase-0/decisions.md`.

### What the panel said

| Issue | Claude | Gemini | GPT |
|---|---|---|---|
| **D-02 "TRL 4–5 for internal 0A milestones"** | Conflicts with flight-project practice. Scout and pathfinder critical technologies should be at TRL 6 at their own PDR. 4–5 should apply only to 0B development milestones. | Applies TRL 4–5 at MTR. | TRL 4 or 5 at MTR as tranche releases. Scouts must be TRL 8 before launch. |

D-02 as accepted:

> Stringency follows reversibility. One-way gates (KDP-0B): TRL 6 in a relevant environment for project-ending technologies, with no waivers. Two-way, internal 0A milestones: TRL 4–5 is enough.

## 5. Technology criteria at the MTR

| Criterion | Claude | Gemini | GPT |
|---|---|---|---|
| TRL 4 scope | All project-ending 0B technologies, with relevant environment documented | T04, T06, T07, T16, T18, T23 | Retained pathfinder-critical functions (adds T09, T20, T25); T11 and T18 |
| TRL 5 | Pathfinder payload (T04, T05, T08, T16, T19, T24) at MTR | "TRL 4–5" in prose | TRL 5 as a release condition before each relevant-environment demonstration; not a blanket MTR criterion |
| Metallurgy | At least two routes (of T06, T17, T07, T23) at TRL 4; narrow to two or fewer at pass | Down-select the route at MTR; T17 not listed | TRL 4 for any route that continues to receive funding; routes are not averaged |
| AD² re-assessment | ≤ 5 for every project-ending technology | — | — |
| Other | D-05 propellant decided; T26 at TRL 4; licensing state engaged in writing; indicative demand schedule | — | T26 at TRL 4; this is a "tranche decision," so an unmet item cannot receive its planned demonstration |

---

## Why This Matters

Claude says the rule conflicts with flight-project practice: a launch is one-way, so scout and pathfinder critical technologies should be at TRL 6 at their own PDR, with 4–5 only for 0B development milestones. Gemini and GPT apply TRL 4–5 at the MTR as tranche releases. The answer may amend an accepted decision.

## Key Considerations

- Whether a 0A launch is a one-way gate under 'stringency follows reversibility'.
- Which 0A milestones are two-way.
- Whether D-02 needs an amendment or only an interpretation.

## Research Directions

1. Decide the ruling, with the criteria stated first and the null option (leave the panel's split as is) assessed.
2. State the gate criterion or rule text that follows from it.
3. Name the evidence that would change the ruling.

## Status (2026-10-20)

The owner confirmed the converged part (G-1.4 in `reconciliation/phase-0/trl/gate-rulings.yaml`). The deliberation could not settle the rest: the positions turn on evidence nobody supplied, and on practice the panel was not given. The open choices (decision sheet `reconciliation/phase-0/trl/gate-rulings-sheet.md`) are routed to evidence questions: rq-0-76. This question stays open until they report; then the owner rules, or the panel deliberates again with that evidence.
