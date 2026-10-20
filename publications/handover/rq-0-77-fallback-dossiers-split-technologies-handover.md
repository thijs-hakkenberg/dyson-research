---
questionId: "rq-0-77"
generatedDate: "2026-10-20"
arxivPapersFound: 0
externalPapersObtained: 0
externalPapersStillNeeded: 6
status: "search brief: no search run yet"
---

# Handover: Fallback Dossiers for the Split Technologies

**Feeds:** rq-0-65, rq-0-66 (owner decision sheet items 2.1, 2.2, 2.4, `reconciliation/phase-0/trl/gate-rulings-sheet.md` in the dyson repo)

## Why

Claude and GPT agree a technology is project-ending unless a credible, costed, non-common-cause fallback keeps 0B production viable. Gemini named fallbacks nobody has costed. The split is about missing facts.

## Known Sources to Obtain

| Citation | Source | Why needed |
|----------|--------|------------|
| Hayabusa2 and OSIRIS-REx navigation and proximity-operations papers | JAXA / NASA, AIAA | Heritage for a single-craft navigation fallback (T25) |
| Roll-out and 100 kW-class solar array programme papers (e.g. iROSA, ROSA flight experiment) | NTRS, AIAA | Heritage for a smaller-array fallback (T02, T15) |
| DSN capacity and loading studies | JPL / IPN Progress Reports | Comms fallback capacity for 15-29 endpoints (T26) |

## Search Targets (no specific citation yet)

- Per technology (T02, T09, T10 safety/productivity, T12, T14, T15, T20, T22, T24, T25, T26): the best-documented alternative and its maturity
- Storable-propellant tug designs at hundreds of tonnes (T14 fallback)
- Dust-tolerant mechanism life tests: lunar and Mars mechanism heritage (T24)

## Simulation / Analysis

Run each fallback through the existing ISRU economics, supply-chain and reliability models (dyson repo `src/lib/services/simulation/isru-economics`, `supply-chain`, `reliability-model.ts`): 0B output and cost per kg, with uncertainty.

## Expert Outreach

Mostly internal analysis; heritage questions go to the agencies already in the registry.. Draft questions are in `src/content/external-organizations/index.yaml` (dyson repo); none sent yet.

## What the Owner Still Decides

The boundary for "viable 0B production" (minimum output, maximum cost increase) each dossier is judged against.

**Deliverable for each source found:** full text plus a 2-3 sentence annotation naming the decision-sheet item it informs.
