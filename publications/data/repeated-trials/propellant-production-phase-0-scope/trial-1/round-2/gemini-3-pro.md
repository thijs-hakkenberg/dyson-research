---
questionId: "rq-0-14"
questionSlug: "propellant-production-phase-0-scope"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
roundNumber: 2
generated: "2026-02-23"
type: "discussion-response"
---

# Discussion: Propellant production in Phase 0 scope

## Response: The Case for "Water-First" Logistics and Storable Propellants

As a systems engineer reviewing the Phase 0 architecture, I agree with the previous round's consensus on a modular, deferred approach for *cryogenic* propellant production. However, the previous discussion missed a critical intermediate step that dramatically lowers risk while securing the logistical benefits we need.

**My Recommendation:** Phase 0 scope must include **Water Extraction and Storage** as a Day 1 capability, but **Propellant Synthesis (Electrolysis/Liquefaction)** should be deferred to Phase 1 or a Phase 0.5 upgrade. Furthermore, we must pivot the baseline propellant architecture away from cryogenic Hydrogen/Oxygen (LH2/LOX) for Phase 0 tugs and toward **Water Plasma or Steam propulsion**.

This approach decouples the feedstock acquisition (easy) from the chemical processing (hard), solving the logistics bottleneck without breaking the power budget.

### 1. The "Water-First" Architecture

The previous arguments assume that "propellant production" equals "making LH2/LOX." This is a trap. Electrolyzing water and liquefying hydrogen is energy-intensive and thermally complex.

*   **The Reality of Feedstock:** Carbonaceous chondrites (C-type) are our primary target. They contain 5-20% water by mass. In a 50,000 tonne/year facility, we are potentially discarding or managing 2,500–10,000 tonnes of water annually.
*   **The Waste Heat Synergy:** The metal refining process (smelting) generates massive amounts of waste heat. We can use this "free" thermal energy to bake out volatiles and water from the asteroid regolith *before* the high-temperature melt.
*   **The Proposal:** The Phase 0 station should capture this water, filter it, and store it as **ice or liquid water**. This is low-tech, low-power, and high-density storage.

**Why this changes the equation:**
Water *is* propellant.
*   **Steam Propulsion:** Nuclear thermal or solar thermal tugs can use water directly as reaction mass.
*   **Electric Propulsion (EP):** Modern Hall-effect thrusters and RF plasma thrusters can run on water vapor. While the ISP is lower than Xenon, the propellant is free.
*   **Radiation Shielding:** Stored water provides excellent radiation protection for the habitat module and sensitive electronics, serving a dual purpose.

### 2. Power Budget Reality Check

The background document notes a 1–2.5 MW power ceiling. Let's look at the numbers for LH2/LOX production versus Water extraction.

*   **LH2/LOX Scenario:** Electrolysis requires ~50 kWh/kg. To produce just 1,000 tonnes of propellant (a fraction of the water available), we need 50 GWh/year. That requires a continuous draw of **~5.7 MW**, completely blowing the entire station's power budget (2.5 MW max) just for fuel, leaving nothing for metallurgy.
*   **Water Extraction Scenario:** Heating regolith to ~500°C to release water requires significantly less energy, most of which can be scavenged from the cooling loops of the metal smelters. The active power draw is minimal (pumps, filtration).

**Conclusion:** Full LH2/LOX production is **technically impossible** within the current 2.5 MW Phase 0 envelope without sacrificing the primary mission of metal production. Therefore, Phase 0 *cannot* include electrolysis at scale.

### 3. The "Storable" Compromise: Hypergolic Synthesis

If high-thrust chemical propulsion is absolutely required (e.g., for time-critical intercept maneuvers where electric propulsion is too slow), we should not look at Cryogens, but at **Storables**.

Carbonaceous asteroids contain carbon, nitrogen, and hydrogen. Instead of difficult-to-store LH2, we should investigate a Phase 0.5 module capable of synthesizing **Methane (CH4)** or simple hydrocarbons via the Sabatier process.
*   **Methane/Oxygen:** Easier to store than Hydrogen (higher boiling point), higher density.
*   **Power Cost:** Sabatier is exothermic (releases heat), though electrolysis for the hydrogen feedstock is still needed. However, Methane offers a better trade-off for long-duration storage at L4/L5 than LH2.

### 4. Revised Phase 0 Requirements

To execute this strategy, the Phase 0 Material Processing Station specifications must be updated:

1.  **Thermal Integration (Mandatory):** The thermal control system must be designed to route waste heat from the smelters to a "pre-processing" volatile extraction kiln.
2.  **Fluid Transfer Standard (Mandatory):** The station must have a standardized water transfer interface (compatible with Artemis/Gateway standards) to offload water to tugs.
3.  **Volume Allocation:** Reserve 5% of station volume for water storage bladders (which can be launched empty/collapsed).
4.  **Propulsion Bus Change:** The tugs procured for Phase 0 must be specified to utilize water (solar thermal or plasma) or Methane, *not* LH2.

### Summary

We must stop treating "Propellant Production" as a binary choice between "Nothing" and "Full Cryogenic Refinery."

**The Answer:** Phase 0 includes **Water Extraction** as a byproduct of the refining process. This water serves as reaction mass for electric/thermal tugs and radiation shielding. We **exclude** electrolysis and liquefaction from Phase 0 because the 2.5 MW power budget cannot support it alongside metallurgy. This approach secures the logistics supply chain without bankrupting the power budget.