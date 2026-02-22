# Paper 07: Collision Avoidance Certification — Input Catalog

**Working Title:** Certification Pathways for Billion-Unit Autonomous Collision Avoidance in Heliocentric Orbit

**Type:** Analysis + simulation
**Addresses:** rq-2-3 (collision avoidance certification, critical priority)

---

## Research Questions

| ID | Title | Status | Type | File |
|----|-------|--------|------|------|
| rq-2-3 | Billion-unit collision avoidance certification | open | discussion | `src/content/research-questions/phase-2/rq-2-3-billion-unit-collision-avoidance.md` |
| rq-1-6 | Swarm collision probability | **answered** | simulation | `src/content/research-questions/phase-1/rq-1-6-swarm-collision-probability.md` |
| rq-2-30 | Megaswarm collisional cascade timescales | open | analysis | `src/content/research-questions/phase-2/rq-2-30-megaswarm-collisional-cascade-timescales.md` |
| rq-2-17 | Fleet coordination scale constraints | **answered** | simulation | `src/content/research-questions/phase-2/rq-2-17-fleet-coordination-scale-constraints.md` |

## Blog Posts

- `src/content/blog/research-resolutions/resolution-billion-unit-collision-avoidance.md`
- `src/content/blog/research/megaswarm-lifetime-lacki-review.md` — Lacki (2016) analysis
- `src/content/blog/research/swarm-dynamics-station-keeping-collision-findings.md`

## BOM Consensus Documents

- `static/content/bom-specs/phase-2/collector-satellites/consensus.md` — collision avoidance discussion
- `static/content/bom-specs/phase-1/swarm-control-system/consensus.md` — coordination algorithms
- `static/content/bom-specs/phase-2/maintenance-drones/consensus.md` — debris management

## Simulation Code

- `src/lib/services/simulation/swarm-dynamics/collision-model.ts` — collision probability model
- `src/lib/services/simulation/swarm-dynamics/monte-carlo.ts` — MC wrapper for dynamics
- `src/lib/services/simulation/swarm-coordination/` — coordination models (Paper 02 code)

## Discussion Transcripts / Conclusions

- `src/content/research-questions/phase-2/rq-2-3-billion-unit-collision-avoidance/` — discussion with conclusion

## Key Literature to Review

- Lacki (2016) — Kessler syndrome for Dyson spheres
- USSPACECOM catalog and conjunction assessment methodology
- ESA Space Debris Office publications
- NASA Orbital Debris Program Office models (ORDEM, MASTER)
- Mean-field collision dynamics for large populations
- Air traffic control certification frameworks (FAA, EASA)
- Maritime AIS / COLREGS as analogy

## Scope Notes

- Builds on Paper 02's hierarchical coordination but focuses specifically on **certification**
- Must define what "safe enough" means at 10^6 objects
- Kessler cascade threshold analysis: how many collisions before self-sustaining cascade?
- Regulatory framework proposal: who certifies and how?
- Strong synergy with Paper 02 — could share simulation infrastructure
