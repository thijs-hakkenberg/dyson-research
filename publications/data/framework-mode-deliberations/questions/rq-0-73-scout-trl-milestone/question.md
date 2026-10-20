---
questionId: "rq-0-73"
slug: "scout-trl-milestone"
title: "What TRL milestone should the rendezvous scouts and their sampling payload meet, and when?"
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
  - "rq-0-80"
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

### Scout readiness

| Model | Position |
|---|---|
| Claude | TRL 6 at scout PDR (month 12–24). Treats TRL 7–8 as "a result of the mission, not an entry criterion." Flags that the panel's target of 8 conflates the two. |
| Gemini | T11 and T18 at TRL 7 within the g-target criterion. |
| GPT | TRL 8 for the actual scout system before each launch. TRL 6 technology maturity before KDP-0B. |

Claude's own summary records the earlier panel baseline as Claude 7, Gemini 8, GPT 6. The positions in this round are as shown in the table. The milestones also differ: PDR, target gate and launch.

---

| Technology | Claude | Gemini | GPT | Panel headline |
|---|---|---|---|---|
| T11 Rendezvous scout spacecraft (with sampling per Gemini and GP | TRL 3–4, AD² 6, architecture-change | TRL 3–4, AD² 5, architecture-change | TRL 2–3, AD² 6, project-ending | TRL 2–4, project-ending |
| T18 Subsurface sampling and in-situ bulk grade assay | TRL 3–4, AD² 6, project-ending | TRL 3–4, AD² 6, project-ending | TRL 2–3, AD² 6, project-ending | TRL 2–4, project-ending |

## Why This Matters

The scouts are the first 0A flight hardware and the source of the target gate's sampled-grade evidence. Claude treats TRL 7–8 as a result of the mission, with TRL 6 at PDR; GPT requires TRL 8 for the actual scout system before each launch.

## Key Considerations

- Milestone (PDR, launch release, target gate) and level.
- Whether flight-project practice or the TRL gate vocabulary governs.
- Consequence for the target gate's timing.

## Research Directions

1. Decide the ruling, with the criteria stated first and the null option (leave the panel's split as is) assessed.
2. State the gate criterion or rule text that follows from it.
3. Name the evidence that would change the ruling.

## Status (2026-10-20)

The owner confirmed the converged part (G-1.5 in `reconciliation/phase-0/trl/gate-rulings.yaml`). The deliberation could not settle the rest: the positions turn on evidence nobody supplied, and on practice the panel was not given. The open choices (decision sheet `reconciliation/phase-0/trl/gate-rulings-sheet.md`) are routed to evidence questions: rq-0-76, rq-0-80. This question stays open until they report; then the owner rules, or the panel deliberates again with that evidence.
