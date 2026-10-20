---
questionId: "rq-0-81"
generatedDate: "2026-10-20"
arxivPapersFound: 0
externalPapersObtained: 0
externalPapersStillNeeded: 4
status: "search brief: no search run yet"
---

# Handover: Bankable Demand and Capacity Sizing

**Feeds:** rq-0-68 (owner decision sheet items 2.7, 2.8, `reconciliation/phase-0/trl/gate-rulings-sheet.md` in the dyson repo)

## Why

D-01 sizes 0B by signed Phase 1 demand. The owner ruled "within 3x" is a quantity ratio and "signed" means financially backed; what backing qualifies and how much capacity a pass authorises are open.

## Known Sources to Obtain

| Citation | Source | Why needed |
|----------|--------|------------|
| NASA COTS, Commercial Crew and CLPS programme documents and GAO reviews | nasa.gov, gao.gov | Government anchor-tenant service contracts as demand instruments |

## Search Targets (no specific citation yet)

- Offtake agreements in project finance: take-or-pay, bankability tests, counterparty credit requirements
- Captive or affiliated offtakers: how lenders treat demand from a related party
- Capacity sizing under uncertain demand: stranded-capacity cost vs shortfall cost (operations research literature)

## Simulation / Analysis

Capacity vs demand under uncertain availability, yield and ramp; expected cost of each sizing rule (Claude, Gemini, GPT) across the rq-0-58 demand range. Reuses dyson `isru-economics` and `supply-chain`.

## Expert Outreach

Project-finance practitioners (organisation still to identify). Draft questions are in `src/content/external-organizations/index.yaml` (dyson repo); none sent yet.

## What the Owner Still Decides

How much stranded-capacity risk to accept.

**Deliverable for each source found:** full text plus a 2-3 sentence annotation naming the decision-sheet item it informs.
