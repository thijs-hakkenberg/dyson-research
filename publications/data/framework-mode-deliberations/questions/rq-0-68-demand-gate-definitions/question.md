---
questionId: "rq-0-68"
slug: "demand-gate-definitions"
title: "What do 'within 3×' and 'signed' mean in the demand gate?"
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
  - "rq-0-81"
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

### g-demand

| Element | Claude | Gemini | GPT |
|---|---|---|---|
| Meaning of "within 3×" | **Quantity:** signed annual demand at least one third of nameplate output, about 0.2–0.8 kt/yr, overlapping the delivery window | **Quantity:** kt/yr demanded against capacity, set by rq-0-58 | **Ambiguous:** numerator, denominator and epoch are unspecified. GPT proposes a **timing** reading (accepted date span ≤ 3× elapsed time from a common epoch). The gate is "not objectively passable" until this is resolved. |
| "Signed" | Flags circularity, since Phase 1 is the same project. Proposes a funded Phase 1 line item or an external offtaker. The owner defines the term. | — | Signed specification, quantities, delivery node and dated schedule |
| Product specification | Required; needed to qualify T22 | — | Required (T22) |
| Sizing | Demand sizes 0B scale | — | Size only to accepted demand. A 3× allowance is not permission to overproduce. |

## Why This Matters

GPT calls the gate 'not objectively passable' until the terms are defined. Claude flags that 'signed' is circular when Phase 1 is the same project. D-01 sizes 0B by signed Phase 1 demand, so these definitions set 0B scale.

## Key Considerations

- Quantity reading vs timing reading of '3×', with numerator, denominator and epoch.
- What counts as signed when the buyer is the project itself (funded line item, external offtaker, specification and schedule).
- Whether demand may size 0B above accepted demand.

## Research Directions

1. Decide the ruling, with the criteria stated first and the null option (leave the panel's split as is) assessed.
2. State the gate criterion or rule text that follows from it.
3. Name the evidence that would change the ruling.

## Status (2026-10-20)

The owner confirmed the converged part (G-1.1, G-1.2 in `reconciliation/phase-0/trl/gate-rulings.yaml`). The deliberation could not settle the rest: the positions turn on evidence nobody supplied, and on practice the panel was not given. The open choices (decision sheet `reconciliation/phase-0/trl/gate-rulings-sheet.md`) are routed to evidence questions: rq-0-81. This question stays open until they report; then the owner rules, or the panel deliberates again with that evidence.
