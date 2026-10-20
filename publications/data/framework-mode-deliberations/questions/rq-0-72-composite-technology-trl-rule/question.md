---
questionId: "rq-0-72"
slug: "composite-technology-trl-rule"
title: "How should the headline TRL of a composite technology be set: capped by its weakest critical part, or assessed on the integration?"
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
| **Composite and system TRL** | Weakest critical sub-rating (as Claude attributes its own position). | Not addressed. | Do not average and do not automatically take the weakest. Assess the integration itself. An unvalidated critical function still blocks the system claim. |

The same split is open in rq-0-64 (T26): Claude proposed capping the headline by the lowest critical sub-rating and a TRL 4 ceiling without an integrated article; GPT challenged that as insufficiently justified and argued for configuration-specific integration assessment. The owner ruled T26's headline at TRL 3 (4 conditional) without settling the general rule.

## Why This Matters

The rule applies to every composite in the baseline (propulsion clusters, power, processing chains) and to how sub-ratings are published.

## Key Considerations

- A mechanical rule (minimum, ceiling) vs a judged integration assessment with stated criteria.
- How sub-ratings are reported alongside the headline.
- Consistency with the T26 ruling.

## Research Directions

1. Decide the ruling, with the criteria stated first and the null option (leave the panel's split as is) assessed.
2. State the gate criterion or rule text that follows from it.
3. Name the evidence that would change the ruling.

## Status (2026-10-20)

No part of this question converged in both syntheses, so nothing is ruled yet. The deliberation could not settle the rest: the positions turn on evidence nobody supplied, and on practice the panel was not given. The open choices (decision sheet `reconciliation/phase-0/trl/gate-rulings-sheet.md`) are routed to evidence questions: rq-0-76. This question stays open until they report; then the owner rules, or the panel deliberates again with that evidence.
