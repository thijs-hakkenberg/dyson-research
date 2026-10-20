---
questionId: "rq-0-70"
slug: "licence-gate-redesign-reapply"
title: "After a failed licence gate, may 0B be redesigned and reapplied, or does failure end 0B?"
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
  - "rq-0-83"
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

### g-licence

| Element | Claude | Gemini | GPT |
|---|---|---|---|
| Status of ≤ 1 t/yr | Interim, ALARP; final value set by rq-0-41 | Used as the threshold | Interim, "not a licence." rq-0-41 and the licensing state set the binding limit, particle and velocity classes, confidence, averaging interval and abnormal-event limits. |
| Verification | Pathfinder-measured escape below the limit, with detection limit ≤ 10% of the limit (Claude's proposal). T08 at TRL 6. | T08 at TRL 6 | Uncertainty-bounded annualised escape including credible failures. T04, T08 and T19 at TRL 6. Measurement uncertainty must fit within the limit. |
| Other | ITU and national frequency coordination for 15–29 assets | — | GPT notes the ceiling equals about 99.992–99.998% retention of tailings |
| Fail | No waiver: no 0B production; 0A only | 0A only | Redesign and reapply within a bounded extension, **or** prohibit 0B |

---

| Trigger | Claude | Gemini | GPT |
|---|---|---|---|

## Why This Matters

Claude and Gemini make failure final (0A only); GPT allows a redesign and reapplication within a bounded extension. The ≤ 1 t/yr escape figure (D-03) is interim and still unsigned; the licensing state sets the binding limit.

## Key Considerations

- Bounded reapplication (how many, how long) vs no waiver.
- What redesign may change (site, throughput, containment) without restarting KDP-0B.
- Dependence on D-03 and rq-0-41.

## Research Directions

1. Decide the ruling, with the criteria stated first and the null option (leave the panel's split as is) assessed.
2. State the gate criterion or rule text that follows from it.
3. Name the evidence that would change the ruling.

## Status (2026-10-20)

The owner confirmed the converged part (G-1.3 in `reconciliation/phase-0/trl/gate-rulings.yaml`). The deliberation could not settle the rest: the positions turn on evidence nobody supplied, and on practice the panel was not given. The open choices (decision sheet `reconciliation/phase-0/trl/gate-rulings-sheet.md`) are routed to evidence questions: rq-0-83. This question stays open until they report; then the owner rules, or the panel deliberates again with that evidence.
