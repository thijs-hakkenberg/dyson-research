---
questionId: "rq-0-79"
generatedDate: "2026-10-20"
arxivPapersFound: 0
externalPapersObtained: 0
externalPapersStillNeeded: 7
status: "search brief: no search run yet"
---

# Handover: MW-Class EP (T01): Ground Facilities, Cluster Model, Flight Subset

**Feeds:** rq-0-75 (owner decision sheet items 2.19, `reconciliation/phase-0/trl/gate-rulings-sheet.md` in the dyson repo)

## Why

T01 is project-ending and the largest scale gap in the baseline. The three test paths (small flight anchor; ground-only; representative flight subset) turn on facility pumping limits, cluster-interaction modelling and flight cost, none of which is established.

## Known Sources to Obtain

| Citation | Source | Why needed |
|----------|--------|------------|
| Goebel & Katz (2008), facility-effects and plume chapters | JPL DESCANSO | Background-pressure effects on thruster performance |
| rq-0-16 handover: HERMeS/AEPS, NEXT, NSTAR test records | this folder | Single-thruster ground-test baseline |

## Search Targets (no specific citation yet)

- Facility-effect studies on Hall and gridded thrusters: background-pressure sensitivity of thrust, efficiency, oscillations, plume
- Published pumping speeds and power limits of the main high-power EP vacuum facilities (NASA GRC, JPL, AFRL, ESA, industry)
- Multi-thruster cluster tests: plume overlap, thermal and electromagnetic coupling, cathode sharing
- Iodine, krypton and argon high-power operation and facility compatibility (links rq-0-53, rq-0-54)
- Rideshare and host-spacecraft options and cost bands for a multi-module flight demonstration

## Simulation / Analysis

Facility model: propellant flow vs pumping speed and resulting background pressure, per propellant and module size. Cluster-interaction model: which effects appear at 2, 4 and N modules. Both new; candidates for a new module in the dyson simulation suite.

## Expert Outreach

NASA EP facilities (oq-1-6), JPL clusters (oq-2-3), Busek (oq-4-2), Aerojet Rocketdyne (oq-5-2). Draft questions are in `src/content/external-organizations/index.yaml` (dyson repo); none sent yet.

## What the Owner Still Decides

Whether a flight anchor is worth its cost in reduced risk at KDP-0B.

**Deliverable for each source found:** full text plus a 2-3 sentence annotation naming the decision-sheet item it informs.
