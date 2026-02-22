# Paper 10: In-Space Thin-Film Deposition — Input Catalog

**Working Title:** In-Space Thin-Film Photovoltaic Deposition: Technology Assessment and Economic Crossover Analysis

**Type:** Technology assessment + parametric crossover model
**Addresses:** PV self-fabrication viability for long-term swarm scaling

---

## Research Questions

| ID | Title | Status | Type | File |
|----|-------|--------|------|------|
| rq-1-46 | In-space thin-film deposition economics crossover | open | analysis | `src/content/research-questions/phase-1/rq-1-46-in-space-thin-film-deposition-economics.md` |
| rq-1-45 | UMG silicon viability for collector cells | open | analysis | `src/content/research-questions/phase-1/rq-1-45-umg-silicon-viability-collector-cells.md` |
| rq-0-44 | In-situ semiconductor fabrication feasibility | investigating | experimentation | `src/content/research-questions/phase-0/rq-0-44-in-situ-semiconductor-fabrication.md` |
| rq-2-14 | Space-based silicon purity achievement | open | experimentation | `src/content/research-questions/phase-2/rq-2-14-space-silicon-purity-achievement.md` |
| rq-2-15 | Thin-film material selection | open | engineering-decision | `src/content/research-questions/phase-2/rq-2-15-thin-film-material-selection.md` |

## Blog Posts

- `src/content/blog/research-resolutions/alternative-materials-collector-manufacturing.md`

## BOM Consensus Documents

- `static/content/bom-specs/phase-2/manufacturing-expansion/consensus.md` — extensive thin-film discussion
- `static/content/bom-specs/phase-1/pv-blanket-arrays/consensus.md` — PV manufacturing specs
- `static/content/bom-specs/phase-1/collector-units/consensus.md` — solar cell specifications
- `static/content/bom-specs/phase-0/material-processing-station/consensus.md` — silicon processing

## Simulation Code

- No dedicated thin-film simulation exists — **new crossover model needed**
- Paper 01 framework (NPV crossover methodology) is directly reusable

## Discussion Transcripts / Conclusions

- None concluded yet — all RQs are open or investigating

## Key Literature to Review

- First Solar CdTe roll-to-roll manufacturing process
- Perovskite thin-film deposition methods (solution vs. vapor)
- CIGS co-evaporation in vacuum (natural fit for space?)
- UMG silicon (upgraded metallurgical grade) — 4N vs. 6N purity tradeoffs
- Amorphous silicon thin-film at reduced purity requirements
- Vacuum deposition advantages: no atmospheric contamination, no pumping costs
- ISS thin-film experiments (if any exist)
- Terrestrial PV efficiency vs. purity curves

## Scope Notes

- **Extends Paper 01 methodology** to a different crossover question: when does in-space PV deposition beat Earth-launched panels?
- Overlaps with Paper 04 (metallurgy) on silicon purification — coordinate scopes
- CdTe and perovskite chemistries may bypass the silicon purity problem entirely
- Must assess: which PV chemistry is most ISRU-friendly given asteroid/lunar feedstock?
- Economic model: capital cost of deposition equipment vs. cumulative Earth-launch savings
