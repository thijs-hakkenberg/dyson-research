# Paper 11: High-Voltage Architecture & Arc Management — Input Catalog

**Working Title:** High-Voltage Architecture and Arc Management for Thin-Film Swarm Collectors

**Type:** Engineering analysis + failure-mode assessment + design-guideline synthesis
**Addresses:** A Phase-1/2 project-ending risk — sustained arcing on high-voltage,
ultra-thin collector membranes operating in the LEO/interplanetary plasma environment.

> Created from the 2026 critical-gap literature fill. This cluster closes **three
> critical research questions at once** (rq-1-4, rq-1-8, rq-2-1) and had the strongest,
> most directly on-point literature of any gap addressed — yet mapped to no existing paper.

---

## Research Questions

| ID | Title | Status | Phase | File |
|----|-------|--------|-------|------|
| rq-1-4 | High-voltage arc fault behavior in plasma environment | investigating | 1 | `src/content/research-questions/phase-1/rq-1-4-high-voltage-arc-fault-behavior.md` |
| rq-1-8 | High-voltage arcing prevention on ultra-thin substrates | open | 1 | `src/content/research-questions/phase-1/rq-1-8-high-voltage-arcing-thin-substrates.md` |
| rq-2-1 | Multi-kilovolt arc management in kilometer-scale membranes | open | 2 | `src/content/research-questions/phase-2/rq-2-1-multi-kilovolt-arc-management.md` |

## Core Question

At what array voltage, membrane thickness, and plasma density does sustained arcing
become the binding constraint on thin-film collector design — and what
insulation / grounding / segmentation architecture keeps a kilometre-scale membrane
below the arc-inception threshold?

## Key Literature (from critical-gap fill, 2026)

- Toyoda et al. (2005). *Degradation of High-Voltage Solar Array Due to Arcing in Plasma Environment*. Journal of Spacecraft and Rockets. Cited by 39. [10.2514/1.11602](https://doi.org/10.2514/1.11602)
- Wang et al. (2014). *Simulation of Arcing Process in High-Voltage Self-Blast Circuit Breaker Considering Motion of Valves*. IEEE Transactions on Plasma Science. Cited by 10. [10.1109/tps.2014.2324599](https://doi.org/10.1109/tps.2014.2324599)
- Iwai et al. (2015). *Flight Results of Arcing Experiment Onboard High-Voltage Technology Demonstration Satellite Horyu-2*. Journal of Spacecraft and Rockets. Cited by 9. [10.2514/1.a33007](https://doi.org/10.2514/1.a33007)
- Goebel et al. (2022). *High Voltage Solar Array Development for Space and Thruster-Plume Plasma Environments*. IEEE Transactions on Plasma Science. Cited by 7. [10.1109/tps.2022.3147424](https://doi.org/10.1109/tps.2022.3147424)
- Ferguson et al. (2017). *Voltage Threshold and Power Degradation Rate for GPS Solar Array Arcing*. IEEE Transactions on Plasma Science. Cited by 14. [10.1109/tps.2017.2694387](https://doi.org/10.1109/tps.2017.2694387)
- Liu et al. (2014). *Observations and modeling of GIC in the Chinese large-scale high-voltage power networks*. Journal of Space Weather and Space Climate. Cited by 36. [10.1051/swsc/2013057](https://doi.org/10.1051/swsc/2013057)
- Wright et al. (2012). *Electrostatic Discharge Testing of Multijunction Solar Array Coupons After Combined Space Environmental Exposures*. IEEE Transactions on Plasma Science. Cited by 28. [10.1109/tps.2011.2174447](https://doi.org/10.1109/tps.2011.2174447)
- Ferguson et al. (2014). *Feasibility of Detecting Spacecraft Charging and Arcing by Remote Sensing*. Journal of Spacecraft and Rockets. Cited by 27. [10.2514/1.a32958](https://doi.org/10.2514/1.a32958)
- Lai et al. (2010). *Importance of Surface Conditions for Spacecraft Charging*. Journal of Spacecraft and Rockets. Cited by 16. [10.2514/1.48824](https://doi.org/10.2514/1.48824)

## Scope Notes

- **Anchor physics:** solar-array arc inception in plasma (Toyoda/Kawasaki flight and
  chamber data), ESD thresholds for multijunction arrays (Wright), spacecraft surface
  charging (Lai), and voltage-threshold / power-degradation scaling (Ferguson).
- **Novel angle for the swarm context:** existing literature is GEO/LEO satellite-scale;
  extend to kilometre-scale ultra-thin membranes where surface-to-edge grounding paths,
  segmentation, and self-healing dielectrics dominate. This is the unoccupied niche.
- **Design deliverable:** an arc-management architecture (segmentation voltage caps,
  guard grounding, coating stack) mapped to the Phase-1 collector BOM.
- **Coordinate scope with:** Paper 10 (thin-film deposition — shares the substrate stack)
  and Paper 04 (metallurgy — shares conductor/coating materials).

## Simulation / Analysis Plan

- No dedicated arc model exists yet. Start with an arc-inception threshold model
  (voltage vs. plasma density vs. gap) calibrated to the Toyoda/Ferguson datasets,
  then a segmentation trade study for kilometre-scale membranes.

## Status

- **Scaffold only.** Drafting deferred until the Wave-A (Tier-1) papers are submitted,
  per the publishing strategy. Promoted from "gap cluster" to a paper slot on the
  strength of its literature base.
