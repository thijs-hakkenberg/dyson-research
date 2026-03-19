---
questionId: "rq-0-48"
generatedDate: "2026-03-17"
updatedDate: "2026-03-18"
arxivPapersFound: 3
externalPapersObtained: 5
externalPapersStillNeeded: 4
---

# Handover: MLI Long-Duration Performance and Degradation at L4/L5

## Arxiv Findings Summary

Arxiv had near-zero coverage of MLI degradation in space. Found papers address ground-based MLI (Simons Observatory) and radiation damage to detectors.

**Update 2026-03-18:** External search obtained LDEF materials results, MISSE reports, Fesmire MLI testing, de Groh degradation data, and two reference books. The core materials degradation dataset is now accessible.

## Papers Found on Arxiv

| arxiv_id | Title | Authors | Key Finding | Relevance |
|----------|-------|---------|-------------|-----------|
| 2601.23168 | Simons Observatory RT-MLI on-sky performance | Day-Weiss et al. | MLI thermal models validated against measurements | medium |
| 1306.5040 | Radio-transparent MLI for radiowave receivers | Choi et al. | MLI design tradeoffs | low |
| 2305.10959 | Protocols for healing radiation-damaged detectors | Krynski et al. | Radiation environment context | low |

## External Papers Obtained (2026-03-18)

| # | Citation | Source | DOI/URL | Key Finding |
|---|----------|--------|---------|-------------|
| 8 | "LDEF — 69 Months in Space" (1991-1995) | NASA SP-3134, SP-3141, SP-3154 | https://ntrs.nasa.gov (search "LDEF materials results") | **5.7-year space exposure dataset** — atomic oxygen, UV, micrometeoroid rates on MLI |
| 9 | MISSE Experiment Reports (2001-present) | NASA ISS Program | https://ntrs.nasa.gov (search "MISSE materials") | Current-era ISS external materials exposure data including MLI components |
| 10 | Fesmire et al., MLI testing and characterization | NASA KSC / Cryogenics 46(2-3) | DOI: 10.1016/j.cryogenics.2005.11.007 | **Leading MLI performance measurement methodology** — effective thermal conductivity data |
| 11 | de Groh et al., "MISSE 2 PEACE Polymers" (2008) | High Performance Polymers 20(4-5) | DOI: 10.1177/0954008308089705 | Polymer/coating degradation in space — erosion yields, spectral degradation, predictive models |
| 58 | Gilmore, "Spacecraft Thermal Control Handbook" Vol I, 2nd ed. (2002) | Aerospace Press/AIAA | ISBN: 978-1884989117 | **Chapter 4: comprehensive MLI effective emissivity data and degradation models** |
| 59 | Hastings & Garrett, "Spacecraft-Environment Interactions" (1996) | Cambridge UP | ISBN: 978-0521607568 | L4/L5 environment characterization — radiation, particles, atomic oxygen |

## Papers Still Needed

| Citation | Likely Source | Why Needed |
|----------|-------------|------------|
| Doenecke & Levesque, "MLI Performance in Space" | Cryogenics (Elsevier) | Early MLI space performance baseline data |
| Fesmire full publication set (beyond aerogel paper) | Cryogenics / NASA KSC | Complete MLI characterization methodology |
| ESA MEDET/EXPOSE Reports | ESA publications | European materials degradation data |
| Sunpower/Thales CryoReach program | ESA | European cryocooler-MLI integration |

## Remaining Gaps

1. **L4/L5-specific degradation rates** — LDEF was LEO (atomic oxygen dominated); L4/L5 has no AO but different radiation. Need to extrapolate using Hastings & Garrett environment models.
2. **30-year MLI degradation projection** — LDEF was 5.7 years; need to model longer durations using degradation rate data.
3. **MLI repair/replacement concepts** — still not addressed in any found literature.

## Recommended Next Steps

The external research provides the **core MLI performance and degradation dataset**. With Gilmore Chapter 4, LDEF data, and Fesmire's testing methodology, we can now:
1. Establish baseline MLI effective emissivity at beginning-of-life
2. Apply LDEF degradation rates, adjusted for L4/L5 environment using Hastings & Garrett
3. Calculate end-of-life thermal performance for depot design sizing
