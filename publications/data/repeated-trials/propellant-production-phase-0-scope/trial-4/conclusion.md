---
questionId: "rq-0-14"
questionSlug: "propellant-production-phase-0-scope"
type: "discussion-conclusion"
generatedBy: "claude-opus-4-6"
generated: "2026-02-24"
roundCount: 1
terminationReason: "unanimous-conclude"
---

# Conclusion: Propellant Production in Phase 0 Scope

## Summary

The discussion converges on a clear middle-path recommendation: propellant production should be included in Phase 0 scope, but **only as a constrained, modular, non-cryogenic capability** — not as a full-scale LOX/LH2 depot. The Material Processing Station should be designed from day one with interfaces, plumbing, power ports, and structural provisions to host propellant production modules ("ISRU-ready"), while flying a modest 50–200 kW water extraction and electrolysis demonstrator early in the phase. This approach avoids the two critical failure modes: locking the program into permanent Earth-supplied propellant dependency (which would throttle construction tempo and consume billions in launch costs), and overloading the Phase 0 mass/power/budget envelope with a complex cryogenic plant that becomes the critical path.

The power budget analysis is decisive in shaping this recommendation. At the station's 1–2.5 MW total capacity, dedicating even 500 kW to electrolysis yields only 70–90 tonnes of propellant annually — insufficient for high-tempo logistics but adequate for station RCS, visiting vehicle top-offs, and small tug operations. Full-rate propellant production would directly cannibalize the primary metals/silicon refining mission. Meanwhile, cryogenic hydrogen storage at 1 AU emerges as the most significant technical trap: the boiloff management, zero-loss storage systems, and fault tolerance requirements would impose disproportionate mass, power, and operational complexity on a Phase 0 facility designed for quarterly human-tended visits.

The preferred propellant strategy for Phase 0 centers on **water as both the intermediate product and potentially as propellant itself** (via resistojet/steam propulsion for low-Δv applications), with optional gaseous O₂/H₂ production for immediate use rather than long-term storage. LOX-only production paired with Earth-supplied fuel represents a viable intermediate step. Bulk cryogenic depot operations — particularly anything involving liquid hydrogen — should be deferred to Phase 1 when power capacity, thermal management infrastructure, and autonomous operations maturity can properly support them.

## Key Points

- **Design for propellant from day one, but build it incrementally.** "ISRU-ready" provisions (plumbing, tank mounts, power/data/thermal ports, fluid transfer standards) cost single-digit tonnes and modest budget in Phase 0 but would be extremely expensive to retrofit later. This is the highest-leverage investment.

- **The 1–2.5 MW power envelope cannot support both full-rate refining and full-rate propellant production.** A 50–200 kW demonstrator module is compatible with the baseline power budget; anything larger forces a trade-off against the station's primary 50,000 t/yr materials processing mission.

- **Cryogenic hydrogen storage at L4/L5 is a Phase 1+ capability, not Phase 0.** The thermal management, boiloff control, and continuous oversight requirements conflict with the quarterly human-tended operations concept and would add disproportionate complexity and mass.

- **Water-based propulsion and LOX-only production are the pragmatic Phase 0 propellant options.** Water is trivially storable and usable in resistojets; LOX is far more manageable than LH2 and can be paired with Earth-supplied fuel as a transitional architecture.

- **Propellant demand falls into three distinct bins with different timelines.** Station RCS and utility needs (addressable in Phase 0), local tug operations (partially addressable in Phase 0), and long-haul logistics transport (requires Phase 1+ infrastructure). Conflating these bins leads to over-scoping.

- **The demonstrator serves dual purpose: risk retirement and autonomy validation.** A limited water extraction/electrolysis system is a valuable forcing function for autonomous operations without becoming a single-point program risk.

## Unresolved Questions

1. **What is the actual propellant demand budget for Phase 0–1 operations?** Without a detailed quantitative model separating RCS/utility, local tug, and long-haul transport bins, the break-even point for in-situ production versus Earth-supplied propellant remains undefined. This number drives the entire architecture decision.

2. **Does water resistojet propulsion close the trajectory math for Phase 0 tug operations?** The simplicity and storage advantages are clear, but the low specific impulse may require unacceptably high propellant mass fractions for the Δv budgets involved in L4/L5 operations. A quantitative trade study against LOX/CH4 and LOX/LH2 alternatives is needed.

3. **What contamination and purity standards must asteroid-derived water meet for electrolysis and propulsion use?** Carbonaceous chondrite water will contain dissolved metals, organics, and particulates. The purification chain complexity and mass could significantly alter the cost-benefit calculus of early ISRU.

4. **Can the ISS precursor experiment program meaningfully retire water extraction and electrolysis risks, or do the environmental differences (microgravity thermal regime, feedstock fidelity) limit transferability?** This determines whether Phase 0 propellant ISRU carries residual technology risk at deployment.

## Recommended Actions

1. **Develop a three-bin propellant demand model** (RCS/utility, local tug, long-haul transport) with quantified mass flow rates, Δv budgets, and annual consumption estimates for Phase 0 and Phase 1. Use this to identify the crossover point where in-situ production becomes cheaper than Earth launch at $2,000–5,000/kg to LEO plus transfer costs.

2. **Commission a propulsion trade study** comparing water resistojet, LOX/CH4 (Earth-supplied CH4), and LOX/LH2 architectures for Phase 0 tug operations. Evaluate delivered payload per year, total system mass (including storage and thermal management), and operational complexity under the quarterly human-tended constraint.

3. **Formalize a "Propellant Module Interface Control Document" as a Phase 0 deliverable.** Specify mechanical mounting envelopes, power step allocations (100–250 kW increments), thermal rejection capacity reservations, fluid coupler standards, contamination limits, and software command/telemetry schemas. This document ensures modularity is preserved regardless of when propellant capability is activated.

4. **Include water extraction and electrolysis demonstrations in the ISS precursor experiment program**, scoped to validate electrolyzer longevity, gas separation and purification, and autonomous fault response. Explicitly document which risks transfer to L4/L5 operations and which require in-situ validation.

5. **Conduct a focused LOX-only storage feasibility assessment for L4/L5**, modeling sunshade + passive cooling configurations with short storage durations and rapid turnover cycles. Determine whether a "produce → transfer → burn" operational concept can avoid active cryocooler requirements entirely, and what tug scheduling constraints this imposes.