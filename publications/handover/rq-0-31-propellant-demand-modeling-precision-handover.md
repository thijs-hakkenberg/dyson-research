---
questionId: "rq-0-31"
generatedDate: "2026-03-17"
updatedDate: "2026-03-18"
arxivPapersFound: 4
externalPapersObtained: 8
externalPapersStillNeeded: 4
---

# Handover: Propellant Demand Modeling Precision for Phase 0-1 Operations

## Arxiv Findings Summary

Arxiv had extremely sparse coverage — adjacent topics only (CFM forecasting, alternative propellants, MDO).

**Update 2026-03-18:** External search obtained the complete MIT/Georgia Tech space logistics optimization series (6 papers from Ho, Ishimatsu, Chen), the ISECG Global Exploration Roadmap, and Sowers' propellant economics paper. **The space logistics methodology is now fully accessible.**

## Papers Found on Arxiv

| arxiv_id | Title | Authors | Key Finding | Relevance |
|----------|-------|---------|-------------|-----------|
| 2508.21802 | Adaptive CFM Forecasting | Cheng, Yang, Ji | ML boil-off prediction | high |
| 2509.26567 | AI-assisted Propellant Development for EP | Du et al. | Alternative propellants | medium |
| 2110.07323 | MDO for Mission Planning and Spacecraft Design | Isaji, Takubo, Ho | Coupled optimization | medium |
| 1404.7430 | Electric sail propulsion | Janhunen | Propellantless option | low |

## External Papers Obtained (2026-03-18)

| # | Citation | Source | DOI/URL | Key Finding |
|---|----------|--------|---------|-------------|
| 37 | Ishimatsu et al., "Generalized Multicommodity Network Flow" (2016) | J. Spacecraft & Rockets 53(1) | https://doi.org/10.2514/1.A33235 | **GMCNF model** for Earth-Moon-Mars logistics with ISRU; shows lunar ISRU improves total mass |
| 37b | Ishimatsu et al., AIAA conference precursor (2013) | AIAA-2013-5414 | https://doi.org/10.2514/6.2013-5414 | Initial GMCNF formulation with network graph |
| 36 | Ho et al., "Dynamic Modeling for Space Logistics" (2014) | Acta Astronautica 105(2) | DOI: 10.1016/j.actaastro.2014.10.026 | Time-expanded network captures temporal dynamics of multi-mission campaigns |
| 36b | Ho et al., "Campaign-Level Dynamic Network" (2016) | Acta Astronautica 123 | DOI: 10.1016/j.actaastro.2016.03.006 | Applies to Flexible Path concept; depot location + ISRU integration analysis |
| 36c | Ho et al., "Space Logistics Review" (2024) | J. Spacecraft & Rockets | https://doi.org/10.2514/1.A35982 | **Comprehensive 2-decade review** — best entry point to all formulations |
| 38 | Chen & Ho, "Integrated Space Transportation Architecture" (2018) | J. Spacecraft & Rockets 55(6) | DOI: 10.2514/1.A34168 | State-of-the-art MINLP for coupled trajectory-logistics |
| 35 | Sowers, "The Business Case for Lunar Ice Mining" (2016) | New Space 4(2) | DOI: 10.1089/space.2015.0036 | Break-even conditions for ISRU vs. Earth-launched propellant |
| 71 | ISECG Global Exploration Roadmap, 4th ed. (2022) | ISECG | https://www.globalspaceexploration.org/documents | International propellant demand estimates from 27 space agencies |

## Papers Still Needed

| Citation | Likely Source | Why Needed |
|----------|-------------|------------|
| NASA Gateway Logistics Studies | NASA/TM or AIAA | Most analogous current depot operations |
| Arney et al., Mars DRA Propellant Analysis | NASA/TM (Langley) | Large-scale demand modeling methodology |
| NASA In-Space Cryogenic Propellant Depot Assessment | NASA/TM | Mission-level depot sizing |
| Merrill et al., "In-Space Propellant Production" | AIAA | ISRU supply-demand coupling |

## Key Conclusions from External Research

**The propellant logistics methodology is now complete:**
1. **GMCNF model** (Ishimatsu/Ho) provides the mathematical framework for depot network optimization
2. **Time-expanded networks** capture temporal dynamics essential for campaign-level analysis
3. **Ho et al. 2024 review** covers all formulation variants — this is the starting point
4. **ISECG roadmap** provides international demand estimates for calibration
5. **Sowers' economics** establish break-even thresholds

**For Project Dyson:** We can now build a propellant demand model using the GMCNF framework, parameterized with our Phase 0-1 mission profiles and validated against ISECG estimates.
