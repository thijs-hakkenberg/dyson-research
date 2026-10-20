---
questionId: "rq-0-75"
slug: "t01-mw-sep-trl6-test-path"
title: "Which path should take the MW-class SEP cluster (T01) to TRL 6: ground modules plus a cluster model, or a flight subset?"
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
  - "rq-0-78"
  - "rq-0-79"
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
| **T01 test facility** | MW-class plume pumping exceeds demonstrated facilities. The owner chooses between (a) ground modules plus a cluster model and (b) a flight subset. | — | Lists MW cluster integration as unproven. No facility claim. |

| Technology | Claude | Gemini | GPT | Panel headline |
|---|---|---|---|---|
| T01 MW-class SEP thruster and PPU cluster | TRL 2–4, AD² 6, project-ending | TRL 2–3, AD² 6, project-ending | TRL 2–3, AD² 6, project-ending | TRL 2–4, project-ending |

Claude raised this alone: MW-class plume pumping exceeds demonstrated vacuum facilities, so the owner chooses between (a) ground-tested modules plus a validated cluster model and (b) a flight subset. GPT lists MW cluster integration as unproven without a facility claim.

## Why This Matters

T01 is project-ending at KDP-0B for every model. The path sets 0A cost, schedule and whether the pathfinder or a dedicated tug demonstrator carries the propulsion evidence.

## Key Considerations

- Facility limits for MW-class Hall/gridded testing (pumping speed, background pressure) and what a cluster model must validate.
- Flight-subset scale and cost.
- Interaction with D-05 (propellant) and rq-0-16/rq-0-54.

## Research Directions

1. Decide the ruling, with the criteria stated first and the null option (leave the panel's split as is) assessed.
2. State the gate criterion or rule text that follows from it.
3. Name the evidence that would change the ruling.

## Status (2026-10-20)

No part of this question converged in both syntheses, so nothing is ruled yet. The deliberation could not settle the rest: the positions turn on evidence nobody supplied, and on practice the panel was not given. The open choices (decision sheet `reconciliation/phase-0/trl/gate-rulings-sheet.md`) are routed to evidence questions: rq-0-78, rq-0-79. This question stays open until they report; then the owner rules, or the panel deliberates again with that evidence.
