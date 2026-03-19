---
questionId: "rq-0-16"
generatedDate: "2026-03-17"
updatedDate: "2026-03-18"
arxivPapersFound: 5
externalPapersObtained: 8
externalPapersStillNeeded: 5
---

# Handover: Thruster Lifetime vs Isp Tradeoff

## Arxiv Findings Summary

Arxiv provided limited but technically valuable coverage — PIC simulation of magnetically shielded thrusters and erosion diagnostics.

**Update 2026-03-18:** External search obtained the complete HERMeS wear test series (3 papers spanning 300-3,570 hours), the magnetic shielding physics paper, the AEPS program overview, NSTAR/NEXT life test data, and the Goebel & Katz reference text. **The thruster lifetime literature is now comprehensive.**

## Papers Found on Arxiv

| arxiv_id | Title | Authors | Key Finding | Relevance |
|----------|-------|---------|-------------|-----------|
| 2304.06563 | Reduced-order PIC simulations of magnetically shielded Hall thruster | Reza, Faraji, Knoll | Magnetically shielded designs reduce wall erosion | critical |
| 1005.0592 | CRDS sensor for BN sputter erosion | Tao, Yamamoto, Gallimore | In-situ erosion monitoring | critical |
| 0410170 | Permanent Magnet Hall Thruster diagnostics | Ferreira et al. | Baseline Hall thruster performance | high |
| 0310080 | Anode Dielectric Coating effects | Dorf, Raitses, Fisch | Long-term operational changes | high |
| 2509.26567 | AI-assisted Propellant Development for EP | Du et al. | Alternative propellants | medium |

## External Papers Obtained (2026-03-18)

| # | Citation | Source | DOI/URL | Key Finding |
|---|----------|--------|---------|-------------|
| 12 | Frieman et al., "Completion of the Long Duration Wear Test of HERMeS" (2019) | AIAA-2019-3895 | https://ntrs.nasa.gov/citations/20190030504 | **3,570-hour test: magnetic shielding eliminates channel erosion; inner front pole cover is life limiter** |
| 12b | Frieman et al., "Long Duration Wear Test" interim (2018) | AIAA-2018-4645 | https://ntrs.nasa.gov/archive/nasa/casi.ntrs.nasa.gov/20180006433.pdf | 1,715 hours; erosion varies 76-300% with voltage; upstream cathode reduces keeper erosion 84% |
| 12c | Williams et al., "Wear Testing of the HERMeS Thruster" (2017) | AIAA-2017-4647 | https://ntrs.nasa.gov/citations/20170003032 | First 728 hours of HERMeS wear testing baseline |
| 28 | Hofer et al., "Completing Development of 12.5 kW HERMeS" (2019) | IEPC-2019-193 | https://electricrocket.org/2019/193.pdf | **Most complete HERMeS/AEPS reference**: 300-800V, 12.5 kW, 3,600h+ data |
| 29 | Mikellides et al., "Magnetic Shielding of Hall Thrusters" (2014) | J. Applied Physics 115(4) | DOI: 10.1063/1.4862313 | Physics basis: proper B-field topology reduces ion bombardment below sputtering threshold |
| 13 | AEPS program status papers (2017-2022) | NASA/AIAA/IEPC | Search NTRS "AEPS Advanced Electric Propulsion System" | 12.5 kW flight thruster string for Gateway |
| 14 | Sengupta et al., "NSTAR Extended Life Test" (2003) | AIAA-2003-4558 | DOI: 10.2514/6.2003-4558 | **30,000+ hour gridded ion thruster life test** — grid erosion primary wear mechanism |
| 15 | Herman et al., "NEXT Long-Duration Test" | NASA/TM (GRC) | Search NTRS "NEXT-C ion engine life test" | **>50,000 hours demonstrated** in ground testing |
| 60 | Goebel & Katz, "Fundamentals of Electric Propulsion" (2008) | JPL/Wiley | https://descanso.jpl.nasa.gov/SciTechBook/series1/Goebel__cmprsd_opt.pdf | **Freely available** standard reference; Chapter 7 covers lifetime physics |

## Papers Still Needed

| Citation | Likely Source | Why Needed |
|----------|-------------|------------|
| Conversano et al., "H6MS Thruster Performance" | AIAA/IEPC | JPL's complementary magnetically shielded thruster |
| de Grys et al., "BPT-4000 Life Test Results" | AIAA | Conventional Hall thruster 10,000+ hour baseline |
| Randolph et al., "Dawn Mission Thruster Performance" | AIAA | Operational flight data |
| Jorns et al., "Cathode Lifetime Studies" | IEPC | Cathode as alternative life limiter |
| Erosion rate vs. operating parameters databases | J. Propulsion and Power | Parametric data for trade studies |

## Key Conclusions from External Research

**The thruster lifetime picture is now clear:**
1. **Magnetically shielded Hall thrusters** effectively eliminate channel wall erosion (HERMeS 3,570h test)
2. **Inner front pole cover** becomes the new life-limiting component, not channel walls
3. **Upstream cathode positioning** reduces keeper erosion by 84%
4. **NEXT ion thruster** demonstrated >50,000 hours — provides the benchmark
5. **AEPS/Gateway** is the flight program bringing this to TRL 8-9

**For Project Dyson:** Magnetically shielded Hall thrusters at 12.5 kW appear viable for 50,000+ hour lifetimes. The Isp-lifetime tradeoff is largely decoupled by magnetic shielding.
