# Paper 06: Cryogenic Propellant Architecture — Input Catalog

**Working Title:** Cryogenic vs. Storable Propellant Architecture for Deep-Space ISRU: A Systems Trade Study

**Type:** Systems trade study with parametric model
**Addresses:** Architecture-change risk (cryocooler TRL 4-5)
**Decision Gate:** Gate 2 — Cryogenic Propellant Architecture (month 30) — NEAREST GATE

---

## Research Questions

| ID | Title | Status | Type | File |
|----|-------|--------|------|------|
| rq-0-30 | Cryogenic boiloff management | investigating | engineering-decision | `src/content/research-questions/phase-0/rq-0-30-cryogenic-boiloff-management.md` |
| rq-0-49 | Cryocooler scaling for space ZBO | investigating | engineering-decision | `src/content/research-questions/phase-0/rq-0-49-cryocooler-scaling-space-zbo.md` |
| rq-0-40 | Thermal management for volatile preservation | open | engineering-decision | `src/content/research-questions/phase-0/rq-0-40-excavation-thermal-volatile-preservation.md` |
| rq-0-16 | Thruster lifetime vs. Isp tradeoff | investigating | engineering-decision | `src/content/research-questions/phase-0/rq-0-16-thruster-lifetime-isp-tradeoff.md` |
| rq-0-14 | Propellant production Phase 0 scope | **answered** | discussion | `src/content/research-questions/phase-0/rq-0-14-propellant-production-phase-0-scope.md` |
| rq-0-31 | Propellant demand modeling precision | investigating | engineering-decision | `src/content/research-questions/phase-0/rq-0-31-propellant-demand-modeling.md` |

## Blog Posts

- `src/content/blog/research-resolutions/resolution-propellant-production-scope.md`
- `src/content/blog/research/cryogenic-storage-extended-literature-review.md`

## BOM Consensus Documents

- `static/content/bom-specs/phase-0/ispp-systems/consensus.md` — extensive cryogenic discussion
- `static/content/bom-specs/phase-0/transport-vehicles/consensus.md` — propellant systems
- `static/content/bom-specs/phase-1/orbital-tugs/consensus.md` — propellant budgets

## Simulation Code

- `src/lib/services/simulation/supply-chain/` — propellant supply models
- `src/lib/services/simulation/depot-logistics/` — depot operations
- `src/lib/services/simulation/orbital-trade/thermal-model.ts` — thermal management

## Discussion Transcripts / Conclusions

- `src/content/research-questions/phase-0/rq-0-14-propellant-production-phase-0-scope/` — concluded (propellant is in scope)

## TRL Assessment

- **Cryocooler scaling to 100-500W at 20K:** TRL 4-5, target 7, gap 2-3, architecture-change risk
- Evidence: NASA GODU-LH2 ground demo at 20W; flight units at milliwatt-to-watt class
- Fallback: Storable propellants (NTO/MMH or similar) — 30% Isp reduction

## Key Literature to Review

- NASA GODU-LH2 program results
- Ball Aerospace / Lockheed cryocooler development
- JWST sunshield thermal performance data
- Reverse-Brayton vs. Stirling vs. pulse tube at 20K
- ESA cryogenic upper stage heritage
- Storable bipropellant performance data (NTO/MMH, MON/MMH)
- Isp cascade: how 30% reduction propagates through fleet sizing

## Scope Notes

- **Highest urgency**: Gate 2 at month 30 is the nearest decision point
- Must produce a clear decision framework: "at what cryocooler TRL does LH2 close?"
- Parametric model comparing total program cost under cryo vs. storable architectures
- Include fleet sizing cascade: lower Isp → more vehicles → more propellant → larger ISRU plant
