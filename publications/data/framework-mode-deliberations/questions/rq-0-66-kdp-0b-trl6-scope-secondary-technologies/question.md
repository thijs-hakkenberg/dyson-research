---
questionId: "rq-0-66"
slug: "kdp-0b-trl6-scope-secondary-technologies"
title: "Must T11, T18, T09, T12 and T20 be at TRL 6 at KDP-0B?"
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
  - "rq-0-77"
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

| Technology | Claude | Gemini | GPT | Panel headline |
|---|---|---|---|---|
| T11 Rendezvous scout spacecraft (with sampling per Gemini and GP | TRL 3–4, AD² 6, architecture-change | TRL 3–4, AD² 5, architecture-change | TRL 2–3, AD² 6, project-ending | TRL 2–4, project-ending |
| T18 Subsurface sampling and in-situ bulk grade assay | TRL 3–4, AD² 6, project-ending | TRL 3–4, AD² 6, project-ending | TRL 2–3, AD² 6, project-ending | TRL 2–4, project-ending |
| T09 High-voltage power tethers and site distribution on regolith | TRL 2–3, AD² 5, architecture-change | TRL 3–4, AD² 6, architecture-change | TRL 2–3, AD² 5, architecture-change | TRL 2–4, architecture-change |
| T12 Autonomous handling, docking and transfer of 150-300 t paylo | TRL 2–3, AD² 6, architecture-change | TRL 3–4, AD² 5, architecture-change | TRL 2–3, AD² 5, architecture-change | TRL 2–4, architecture-change |
| T20 Distributed energy storage (GPT: and microgrid power managem | TRL 3–5, AD² 4, architecture-change | TRL 3–4, AD² 4, architecture-change | TRL 3–4, AD² 5, architecture-change | TRL 3–5, architecture-change |

## Why This Matters

These five sit outside the agreed project-ending core. Scouts (T11) and sampling (T18) are 0A flight technologies whose maturity is settled by their own missions; T09, T12 and T20 are supporting systems Claude would let pass at TRL ≥ 5 with a waiver and a funded path, while GPT wants TRL 6 for the selected implementations.

## Key Considerations

- Whether a 0A flight technology belongs in the KDP-0B list at all.
- What 'selected reference implementation' means for the gate.
- Waiver conditions, if any.

## Research Directions

1. Decide the ruling, with the criteria stated first and the null option (leave the panel's split as is) assessed.
2. State the gate criterion or rule text that follows from it.
3. Name the evidence that would change the ruling.

## Status (2026-10-20)

The owner confirmed the converged part (G-1.8 in `reconciliation/phase-0/trl/gate-rulings.yaml`). The deliberation could not settle the rest: the positions turn on evidence nobody supplied, and on practice the panel was not given. The open choices (decision sheet `reconciliation/phase-0/trl/gate-rulings-sheet.md`) are routed to evidence questions: rq-0-77, rq-0-80. This question stays open until they report; then the owner rules, or the panel deliberates again with that evidence.
