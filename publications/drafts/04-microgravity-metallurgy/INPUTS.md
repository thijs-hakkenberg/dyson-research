# Paper 04: Microgravity Metallurgy — Input Catalog

**Working Title:** Microgravity Metallurgy at Industrial Scale: State of the Art, Scaling Laws, and Technology Maturation Pathways

**Type:** Literature review + parametric analysis
**Addresses:** Project-ending risk #1 (TRL 2-3, gap 4-5 levels)
**Decision Gate:** Gate 1 — Microgravity Materials Processing (month 36)

---

## Research Questions

| ID | Title | Status | Type | File |
|----|-------|--------|------|------|
| rq-0-11 | Microgravity metallurgy scaling to industrial production | investigating | experimentation | `src/content/research-questions/phase-0/rq-0-11-microgravity-metallurgy-scaling.md` |
| rq-0-12 | Optimal zone refining in zero-g | investigating | experimentation | `src/content/research-questions/phase-0/rq-0-12-zero-g-zone-refining-process.md` |
| rq-0-15 | Silicon purity achievability in vacuum | investigating | experimentation | `src/content/research-questions/phase-0/rq-0-15-silicon-purity-achievability.md` |
| rq-0-33 | Industrial-scale microgravity electrolysis | investigating | experimentation | `src/content/research-questions/phase-0/rq-0-33-microgravity-electrolysis-separation.md` |
| rq-0-44 | In-situ semiconductor fabrication feasibility | investigating | experimentation | `src/content/research-questions/phase-0/rq-0-44-in-situ-semiconductor-fabrication.md` |

## Blog Posts

- `src/content/blog/research-resolutions/isru-chemical-processing-beyond-thermal-metallurgy.md`

## BOM Consensus Documents

- `static/content/bom-specs/phase-0/material-processing-station/consensus.md` — extensive metallurgy discussion
- `static/content/bom-specs/phase-0/ispp-systems/consensus.md` — electrolysis discussion
- `static/content/bom-specs/phase-2/manufacturing-expansion/consensus.md` — silicon purity, zone refining

## Simulation Code

- `src/lib/services/simulation/radiation-degradation/` — silicon degradation models (partial overlap)

## Discussion Transcripts / Conclusions

- None concluded yet for these RQs

## TRL Assessment

- **Microgravity metallurgy at industrial scale:** TRL 2-3, target 6-7, gap 4-5, project-ending risk
- **In-space silicon purification:** TRL 2-3, target 6, gap 3-4, architecture-change risk
- Evidence: Sub-100g ISS experiments only; no industrial-scale precedent

## Key Literature to Review

- ISS Materials Science Lab experiments (ESA Columbus, JAXA Kibo, NASA MSFC)
- Marangoni convection in microgravity (grain structure formation)
- Buoyancy-free solidification studies
- Terrestrial zone refining scaling laws
- NASA GODU-LH2 related metallurgy work

## Scope Notes

- This paper is primarily a **literature review with parametric scaling analysis**
- Does NOT require new simulation code — relies on existing experimental literature
- Must address the artificial gravity fallback: cost and mass implications of rotational station design
- Should produce quantitative go/no-go criteria for Gate 1
