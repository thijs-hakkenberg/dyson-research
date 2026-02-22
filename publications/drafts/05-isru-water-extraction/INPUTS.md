# Paper 05: ISRU Water Extraction — Input Catalog

**Working Title:** ISRU Water Extraction for Space Propellant: Asteroid vs. Lunar Sources at Dyson-Scale Production

**Type:** Parametric cost model + Monte Carlo (Paper 01 methodology)
**Addresses:** Project-ending risk #2 (TRL 3-4)
**Decision Gate:** Gate 3 — ISRU Water Extraction (month 48)

---

## Research Questions

| ID | Title | Status | Type | File |
|----|-------|--------|------|------|
| rq-0-6 | Regolith excavation behavior in microgravity | investigating | experimentation | `src/content/research-questions/phase-0/rq-0-6-regolith-excavation-microgravity.md` |
| rq-0-7 | Anchoring technology reliability across asteroid types | investigating | experimentation | `src/content/research-questions/phase-0/rq-0-7-anchoring-technology-reliability.md` |
| rq-0-27 | Water-first resource extraction strategy | **answered** | engineering-decision | `src/content/research-questions/phase-0/rq-0-27-water-first-resource-strategy.md` |
| rq-0-39 | Asteroid subsurface characterization | investigating | experimentation | `src/content/research-questions/phase-0/rq-0-39-subsurface-mechanical-characterization.md` |
| rq-1-50 | Lunar regolith processing for swarm materials | open | analysis | `src/content/research-questions/phase-1/rq-1-50-lunar-regolith-processing-swarm-materials.md` |
| rq-2-32 | Comparative feedstock economics (multi-source) | open | analysis | `src/content/research-questions/phase-2/rq-2-32-comparative-feedstock-economics-multi-source.md` |

## Blog Posts

- `src/content/blog/research-resolutions/water-first-resource-extraction-strategy.md`
- `src/content/blog/research-resolutions/resolution-feedstock-isru-timeline.md`
- `src/content/blog/research/alternative-material-sources-beyond-asteroid-isru.md`
- `src/content/blog/research/isru-crossover-point-findings.md` (Paper 01 preliminary)
- `src/content/blog/research/isru-economic-crossover-paper.md` (Paper 01 final)

## BOM Consensus Documents

- `static/content/bom-specs/phase-0/mining-robots/consensus.md` — regolith excavation, anchoring
- `static/content/bom-specs/phase-0/material-processing-station/consensus.md` — water processing
- `static/content/bom-specs/phase-0/ispp-systems/consensus.md` — water electrolysis
- `static/content/bom-specs/phase-3a/feedstock-supply-chain-pipeline/consensus.md` — long-term feedstock

## Simulation Code

- `src/lib/services/simulation/isru-economics/` — cost models, Monte Carlo (Paper 01 codebase)
- `publications/scripts/isru_model.py` — NPV cost model (reusable framework)
- `publications/scripts/isru_mc.py` — Monte Carlo engine (reusable framework)

## Discussion Transcripts / Conclusions

- `src/content/research-questions/phase-1/rq-1-21-feedstock-acquisition-isru-timeline/` — multi-round discussion with conclusion

## TRL Assessment

- **ISRU water extraction from asteroids:** TRL 3-4, target 6-7, gap 3, project-ending risk
- Evidence: OSIRIS-REx confirmed hydrated minerals; meteorite analog lab demos show promise
- Fallback: Lunar water sources (significantly increases transport cost)

## Key Literature to Review

- OSIRIS-REx sample analysis results (Bennu composition)
- Hayabusa2 sample analysis (Ryugu composition)
- C-type / CM chondrite water content measurements
- Lunar polar ice deposit characterization (LCROSS, Chandrayaan)
- Thermal extraction energy budgets (asteroid vs. lunar)
- Transport delta-v: NEA → L4/L5 vs. Moon → L4/L5

## Scope Notes

- **Directly extends Paper 01**: reuse NPV framework, add source comparison dimension
- Monte Carlo over: extraction yield, water purity, energy cost, transport delta-v
- Must produce optimal source selection as function of program scale
- Comparative analysis: C-type asteroid vs. lunar polar ice vs. Phobos/Deimos
