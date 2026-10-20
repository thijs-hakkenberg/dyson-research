---
questionId: "rq-0-65"
slug: "gate-risk-class-split-technologies"
title: "Which risk class should apply to the eight technologies the panel split on (T02, T10, T14, T15, T22, T24, T25, T26)?"
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
  - "rq-0-77"
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

| Technology | Claude | Gemini | GPT | Panel headline |
|---|---|---|---|---|
| T02 MW-scale deployable solar arrays (tug; site per Gemini and G | TRL 2–4, AD² 5, architecture-change | TRL 3–4, AD² 5, architecture-change | TRL 2–3, AD² 5, project-ending | TRL 2–4, project-ending |
| T10 Long-duration autonomy for mining, processing and proximity  | TRL 2–3, AD² 6, architecture-change | TRL 3–4, AD² 6, project-ending | TRL 3–4, AD² 6, project-ending | TRL 2–4, project-ending |
| T14 Propellant storage and feed at hundreds of tonnes per tug | TRL 2–4, AD² 5, architecture-change | TRL 2–3, AD² 6, architecture-change | TRL 2–3, AD² 6, project-ending | TRL 2–4, project-ending |
| T15 Site power generation and transfer | TRL 2–3, AD² 6, architecture-change | TRL 2–3, AD² 6, project-ending | TRL 2–3, AD² 5, project-ending | TRL 2–3, project-ending |
| T22 Product consolidation, packaging and qualification | TRL 2–4, AD² 5, project-ending | TRL 2–3, AD² 6, architecture-change | TRL 2–2, AD² 6, project-ending | TRL 2–4, project-ending |
| T24 Dust-tolerant long-life mechanisms and seals | TRL 2–4, AD² 6, architecture-change | TRL 4–5, AD² 5, project-ending | TRL 3–4, AD² 6, project-ending | TRL 2–5, project-ending |
| T25 Target-local and SEL1 cargo-node navigation and control | TRL 2–3, AD² 5, architecture-change | TRL 3–4, AD² 4, project-ending | TRL 2–3, AD² 6, architecture-change | TRL 2–4, project-ending |
| T26 Deep-space communications and resilient command service | TRL 5–7, AD² 3, cost-increase | TRL 6–7, AD² 3, cost-increase | TRL 3–4, AD² 4, architecture-change | TRL 3–3, architecture-change (owner ruling) |

Claude's list of split classes needing a ruling: T02, T10, T14, T15, T22, T24, T25, T26. Claude holds these at TRL 6, no waiver, until they are ruled on. T26 already carries an owner ruling from rq-0-64 (architecture-change, possibly project-ending).

### Project-ending classification for KDP-0B

**Agreed core (all three models):** T01, T02, T03, T04, T05, T08, T10, T14, T15, T16, T19, T21, T22, T24.

**Disputed members:**

| Technology | Claude | Gemini | GPT |
|---|---|---|---|
| T25 | Project-ending (split; ruling due at KDP-0A) | Project-ending | TRL 6 as "selected reference implementation," grouped with T09, T12, T20 |
| T26 | Claude's view: project-ending for integrated fleet command. Owner ruling is architecture-change, "possibly project-ending." Open in rq-0-64. | Not listed | TRL 6 integrated service at KDP-0B |
| T18 | 0A flight technology (TRL 6 at scout PDR) | Project-ending | TRL 6 technology maturity before KDP-0B |
| T11 | 0A flight technology | In prose list; absent from YAML | TRL 6 technology maturity before KDP-0B |
| T09, T12, T20 | Architecture-change: TRL ≥ 5, waiverable, with a funded path to 6 | Not listed | TRL 6 for selected implementations; substitutions reassessed |

**Split classes needing an owner ruling (Claude's list):** T02, T10, T14, T15, T22, T24, T25, T26. Claude holds these at TRL 6, no waiver, until they are ruled on.

## Why This Matters

The class decides whether a technology must be at TRL 6 with no waiver at KDP-0B (project-ending) or may pass at a lower level with a funded path (architecture-change, schedule-delay, cost-increase). Over-classing lengthens 0A; under-classing lets 0B commit on an unproven function.

## Key Considerations

- Rule per technology, or a rule that generates the classes (e.g. 'project-ending if no credible fallback keeps 0B production').
- Whether the fallbacks the models named are credible and costed.
- How the ruling interacts with rq-0-64 for T26.

## Research Directions

1. Decide the ruling, with the criteria stated first and the null option (leave the panel's split as is) assessed.
2. State the gate criterion or rule text that follows from it.
3. Name the evidence that would change the ruling.

## Status (2026-10-20)

No part of this question converged in both syntheses, so nothing is ruled yet. The deliberation could not settle the rest: the positions turn on evidence nobody supplied, and on practice the panel was not given. The open choices (decision sheet `reconciliation/phase-0/trl/gate-rulings-sheet.md`) are routed to evidence questions: rq-0-76, rq-0-77. This question stays open until they report; then the owner rules, or the panel deliberates again with that evidence.
