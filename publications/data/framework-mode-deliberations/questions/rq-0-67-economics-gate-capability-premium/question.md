---
questionId: "rq-0-67"
slug: "economics-gate-capability-premium"
title: "May the economics gate pass 0B at a cost above Earth supply (a capability premium R), or does any premium need a separate owner decision?"
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
  - "rq-0-82"
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

### g-economics

| Element | Claude | Gemini | GPT |
|---|---|---|---|
| Threshold | 0B P70 $/kg ≤ R × Earth-supply P50 $/kg at SEL1. R is set by the owner. Claude cites D-01 ("capability programme, not a cost saving") as implying R may exceed 1. | Delivered $/kg must **undercut** Earth supply | Expected delivered cost no higher than Earth supply, plus an owner-approved downside bound. A capability subsidy requires a **new explicit owner decision**, "not a relabelled economics pass." |
| Robustness | The decision must not reverse across the launch-price range. Notes current dispersion: $22–195B from the panel against $15.7B in the BOM. | — | Sensitivity to grade, utilisation, replacement and delay |
| Estimate band | ±30% or better | — | — |

The models disagree on whether a premium above cost parity can pass inside this gate (Claude) or needs a separate owner decision (GPT). Gemini sets the threshold below parity.

## Why This Matters

D-01 calls Phase 0 a capability programme, not a cost saving, which Claude reads as allowing R > 1 inside the gate. GPT holds that a capability subsidy must be a new explicit owner decision, 'not a relabelled economics pass'. Gemini sets the threshold below parity. The choice determines whether the economics gate can ever fail on cost alone.

## Key Considerations

- Value of R, if any, and what it buys (capability, learning, Phase 1 option value).
- Whether a premium belongs in the gate or in a separate decision.
- Robustness across launch-price scenarios and the cost dispersion ($22–195B panel vs $15.7B BOM).

## Research Directions

1. Decide the ruling, with the criteria stated first and the null option (leave the panel's split as is) assessed.
2. State the gate criterion or rule text that follows from it.
3. Name the evidence that would change the ruling.

## Status (2026-10-20)

The owner confirmed the converged part (G-1.7 in `reconciliation/phase-0/trl/gate-rulings.yaml`). The deliberation could not settle the rest: the positions turn on evidence nobody supplied, and on practice the panel was not given. The open choices (decision sheet `reconciliation/phase-0/trl/gate-rulings-sheet.md`) are routed to evidence questions: rq-0-82. This question stays open until they report; then the owner rules, or the panel deliberates again with that evidence.
