# Paper 08: Space Solar Power Economics — Input Catalog

**Working Title:** Space Solar Power Economics at Dyson Scale: Revenue Thresholds, Transmission Efficiency, and Market Viability

**Type:** Economic model + Monte Carlo
**Addresses:** rq-2-20 (swarm ROI), rq-1-44 (min PV rate), rq-2-23 (GW transmission)

---

## Research Questions

| ID | Title | Status | Type | File |
|----|-------|--------|------|------|
| rq-2-20 | Swarm operational threshold for humanity's energy needs | open | discussion | `src/content/research-questions/phase-2/rq-2-20-swarm-roi-threshold-humanity-power-needs.md` |
| rq-1-44 | Minimum viable photovoltaic production rate | open | analysis | `src/content/research-questions/phase-1/rq-1-44-minimum-viable-pv-production-rate.md` |
| rq-2-23 | GW-scale power transmission efficiency | open | analysis | `src/content/research-questions/phase-2/rq-2-23-gw-scale-power-transmission-efficiency.md` |
| rq-1-11 | Swarm-level power architecture for end-use | open | discussion | `src/content/research-questions/phase-1/rq-1-11-swarm-power-architecture-end-use.md` |

## Blog Posts

- `src/content/blog/research-resolutions/resolved-swarm-roi-threshold-humanity-power.md`
- `src/content/blog/research-resolutions/resolution-swarm-power-architecture.md`

## BOM Consensus Documents

- `static/content/bom-specs/phase-1/pv-blanket-arrays/consensus.md` — PV manufacturing specs
- `static/content/bom-specs/phase-1/collector-units/consensus.md` — power generation specs
- `static/content/bom-specs/phase-2/collector-satellites/consensus.md` — power transmission
- `static/content/bom-specs/phase-0/solar-power-arrays/consensus.md` — baseline solar

## Simulation Code

- No dedicated SSP economics simulation exists — **new code needed**
- Paper 01 revenue breakeven analysis ($0.94M/unit/year threshold) is a starting point
- `publications/scripts/isru_model.py` — NPV framework is reusable

## Discussion Transcripts / Conclusions

- `src/content/research-questions/phase-1/rq-1-11-swarm-power-architecture-end-use/` — discussion with conclusion

## Key Literature to Review

- NASA SSP studies (1997 Fresh Look, 2024 OTEC update)
- ESA Solaris programme
- Caltech SSPP (Space Solar Power Project)
- Microwave power beaming efficiency at GW scale
- Laser power beaming alternatives
- Atmospheric absorption models
- Rectenna ground station economics
- IEA World Energy Outlook projections (demand curves)
- LCOE comparisons: ground solar, wind, nuclear vs. SSP

## Scope Notes

- **New simulation code required** — SSP revenue model with transmission losses
- Extends Paper 01's revenue breakeven from single parameter to full economic model
- Must address: at what swarm size does SSP compete with ground renewables?
- Market size analysis: global energy demand 2030-2100 projections
- Production rate analysis: min PV rate for commercial viability
- Transmission architecture comparison: microwave vs. laser vs. relay
