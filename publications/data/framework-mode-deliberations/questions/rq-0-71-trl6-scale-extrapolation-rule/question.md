---
questionId: "rq-0-71"
slug: "trl6-scale-extrapolation-rule"
title: "Should TRL 6 demonstrations carry a fixed scale-extrapolation limit (e.g. ≤ 10×) or none fixed in advance?"
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
  - "rq-0-78"
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
| **TRL 6 scale rule** | Proposes no more than 10× extrapolation in throughput or power, unless governing regimes are shown to be preserved. Duration can be met by partial test plus a validated wear model. | Not addressed. | "No fixed 'acceptable scale factor' can be assumed in advance." Extrapolation must be justified by test-validated models. Accelerated testing needs a validated degradation model. |

## Why This Matters

Most project-ending technologies need MW-class power or kt/yr throughput that no test facility reaches. The rule decides how far a ground or pathfinder test may be extrapolated before it stops counting as a representative model, and so how big (and costly) the pathfinder must be.

## Key Considerations

- A fixed factor vs a regime-preservation argument per technology.
- Duration and wear: partial test plus a validated degradation model.
- Whether different limits apply to throughput, power and duration.

## Research Directions

1. Decide the ruling, with the criteria stated first and the null option (leave the panel's split as is) assessed.
2. State the gate criterion or rule text that follows from it.
3. Name the evidence that would change the ruling.

## Status (2026-10-20)

No part of this question converged in both syntheses, so nothing is ruled yet. The deliberation could not settle the rest: the positions turn on evidence nobody supplied, and on practice the panel was not given. The open choices (decision sheet `reconciliation/phase-0/trl/gate-rulings-sheet.md`) are routed to evidence questions: rq-0-76, rq-0-78. This question stays open until they report; then the owner rules, or the panel deliberates again with that evidence.
