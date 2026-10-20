---
questionId: "rq-0-80"
generatedDate: "2026-10-20"
arxivPapersFound: 0
externalPapersObtained: 0
externalPapersStillNeeded: 7
status: "search brief: no search run yet"
---

# Handover: Target-Grade Evidence Standard (Sampling and Assay)

**Feeds:** rq-0-66, rq-0-73 (owner decision sheet items 2.3, 2.15, 2.16, `reconciliation/phase-0/trl/gate-rulings-sheet.md` in the dyson repo)

## Why

The target gate commits 0B to one asteroid. All three positions on T18 depend on an unanswered question: how many samples from what depth bound a rubble pile's bulk grade to what confidence?

## Known Sources to Obtain

| Citation | Source | Why needed |
|----------|--------|------------|
| Yokoyama et al., "Samples returned from the asteroid Ryugu are similar to Ivuna-type carbonaceous meteorites", *Science* (2023) | DOI search | Representativeness of returned samples |
| OSIRIS-REx Bennu sample overview papers (Lauretta et al., 2024; verify) | MAPS / NASA | Second returned-sample precedent |
| JORC Code (2012); NI 43-101; CRIRSCO International Reporting Template | jorc.org, crirsco.com | How sampling density maps to inferred, indicated and measured resources |

## Search Targets (no specific citation yet)

- Fe-Ni metal heterogeneity in iron and stony-iron meteorites (scale of variation)
- Rubble-pile internal structure and regolith mixing models (Itokawa, Ryugu, Bennu)
- In-situ assay instruments for bulk composition (gamma/neutron spectroscopy, XRF, LIBS): depth sensitivity and uncertainty
- Geostatistics for sparse sampling: confidence intervals with very few drill holes

## Simulation / Analysis

Monte Carlo of grade estimation on synthetic rubble-pile bodies: heterogeneity models from meteorite and returned-sample data, sampling designs (count, depth, spread), resulting confidence interval on bulk grade. Can draw on the dyson `spectral-analysis` and `nea-population.ts` modules.

## Expert Outreach

JAXA Hayabusa2 team (oq-10-2), CRIRSCO / a resource-estimation competent person (oq-13-1). Draft questions are in `src/content/external-organizations/index.yaml` (dyson repo); none sent yet.

## What the Owner Still Decides

The confidence level required before committing 0B to a target.

**Deliverable for each source found:** full text plus a 2-3 sentence annotation naming the decision-sheet item it informs.
