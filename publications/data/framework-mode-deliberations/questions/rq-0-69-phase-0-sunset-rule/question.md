---
questionId: "rq-0-69"
slug: "phase-0-sunset-rule"
title: "Should the month-180 sunset trigger the fallback automatically, or be a planning boundary?"
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

| Gate | Claude | Gemini | GPT | Envelope |
|---|---|---|---|---|
| KDP-0B | 96–156 | 72–120 | 96–180 | 72–180 |
| Sunset | month 180, automatic execution of fallback | — | set via rq-0-63; M180 is "a planning boundary, not authority for an automatic fifteen-year commitment" | disputed |

## 6. Failure outcomes

| Trigger | Claude | Gemini | GPT |
|---|---|---|---|
| KDP-0A | Re-plan 0A, bounded to 6 months | Project hold | Defer, or restrict to ground research and remote survey |
| MTR | One funded re-plan; on a second fail, stop 0B spend | Restructure ground R&D; delay or cancel pathfinder | Stop failed routes; bounded corrective programme, or complete 0A without production |
| g-target | One further scout wave (≤ 36 months, inside sunset), then fallback | Fallback | Resample or change target within a prospecting cap, then fallback |
| g-demand | Defer 0B at minimal option-keeping spend; re-test at Phase 1 milestones | Fallback | Reduce or defer 0B |
| g-economics | Fallback; re-test on pre-set shifts in launch price or demand | Fallback | Earth supply; subsidy only by a new owner decision |
| KDP-0B | One slip inside the month-180 sunset, then fallback | Fallback | Bounded extension, or fallback |
| Water pilot | Drop the pilot | — | Drop the pilot; no lunar-water or cryogenic switch |

---

## Why This Matters

An automatic sunset (Claude) is a pre-commitment that caps 0A spend and prevents drift; GPT says M180 is 'a planning boundary, not authority for an automatic fifteen-year commitment' and should be set via rq-0-63 (integrated schedule). The rule bounds every slip the failure outcomes allow.

## Key Considerations

- Automatic execution vs a mandatory decision point.
- How the sunset relates to rq-0-63 and the KDP-0B window (72–180 months).
- What spend is allowed to keep the 0B option alive after a deferral.

## Research Directions

1. Decide the ruling, with the criteria stated first and the null option (leave the panel's split as is) assessed.
2. State the gate criterion or rule text that follows from it.
3. Name the evidence that would change the ruling.

## Status (2026-10-20)

The owner confirmed the converged part (G-1.6 in `reconciliation/phase-0/trl/gate-rulings.yaml`). The deliberation could not settle the rest: the positions turn on evidence nobody supplied, and on practice the panel was not given. The open choices (decision sheet `reconciliation/phase-0/trl/gate-rulings-sheet.md`) are routed to evidence questions: rq-0-83. This question stays open until they report; then the owner rules, or the panel deliberates again with that evidence.
