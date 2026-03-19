---
questionId: "rq-0-14"
questionSlug: "propellant-production-phase-0-scope"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
roundNumber: 1
generated: "2026-02-24"
type: "discussion-response"
---

Propellant production should be **in Phase 0 scope only as a “propellant-ready” architecture plus a small, non-cryogenic demonstrator**, not as a full-scale LOX/LH2 depot. In other words: **design the Material Processing Station (MPS) so propellant can be added without redesign**, and fly/operate a **low-power water extraction + electrolysis pilot** to retire the hardest ISRU unknowns early, but defer high-rate production and especially cryogenic storage to Phase 1.

That recommendation fits the current Phase 0 constraints in the consensus spec (50,000 t/yr materials throughput, **1–2.5 MW solar**, **~0.8–1.0 Mkg** full-build mass, human-tended quarterly) while still preventing an Earth-propellant logistics dependency from becoming a program-level trap.

---

## 1) Why full propellant production doesn’t fit Phase 0 (yet)

### Power reality check
At the stated electrolysis figure (50–60 kWh/kg water processed), the MPS baseline power is quickly consumed:

- **500 kW** continuous → ~12,000 kWh/day → **~200–240 kg/day water** → **~70–90 t/year water** → roughly the same order of magnitude propellant mass (as LOX/LH2) if you count oxygen + hydrogen output.
- Even **2 MW** continuous only scales this to **~280–360 t/year** water/prod.

That’s not nothing, but it’s also not obviously enough to justify the **mass, complexity, and thermal burden** of a true depot—especially if tug operations ramp faster than this or if boiloff forces you to “use it immediately or lose it.”

### Cryogenic storage is the real scope killer
LOX/LH2 storage at 1 AU in sunlight is a thermal management project disguised as ISRU. Long-duration storage wants:
- sunshields, MLI, vapor-cooled shields
- cryocoolers with nontrivial continuous power draw
- boiloff capture/reliquefaction plumbing
- high-reliability valves/seals over years

This pushes the MPS toward being a **propellant depot first** and a refinery second, which is not aligned with Phase 0’s primary purpose: proving high-throughput materials processing and providing structural feedstock for the rest of the program.

### Operational complexity conflicts with the “quarterly visit” posture
Propellant plants add:
- contamination control (electrolyzer water purity, gas purity)
- rotating equipment (compressors, pumps)
- safety cases (O2 compatibility, ignition hazards)
- fault management that is hard to fully automate early

If Phase 0 is meant to be human-tended but not continuously crewed, you want the station to fail “gracefully” rather than in ways that demand immediate intervention.

---

## 2) Why propellant cannot be ignored (and should be architected in now)

Excluding propellant entirely creates a long-lived Earth logistics tail that can dominate ops tempo and cost, even if the station itself stays within budget. The risk isn’t just $/kg; it’s **schedule and throughput coupling**: every retrieval/tug mission becomes sensitive to launch cadence, geopolitics, and Earth-side supply chain.

Also, if Phase 0 targets carbonaceous material (as assumed), then water/volatiles are among the *highest leverage* products in terms of enabling future operations. The program should not discover in Phase 1 that it failed to plan interfaces, thermal zoning, or power distribution for ISRU.

So the right move is: **Phase 0 proves the extraction and conversion physics and the autonomy**, while the depot-grade scaling waits until you have real demand numbers and flight data.

---

## 3) Recommended Phase 0 scope: “Propellant-ready + pilot production”

### A. Include a water/volatile extraction and handling module (pilot scale)
Add a module that can:
- accept a side-stream of carbonaceous feedstock
- heat/process it to release water/volatiles
- condense, purify, and store **water** in tanks (water is easy to store)
- optionally electrolyze at **tens of kW to a few hundred kW**, producing gases for immediate use or limited storage

This retires the key unknowns:
- actual water yield and contamination profile from your chosen asteroid class
- clogging/fouling behavior, dust management, filter life
- power/thermal integration with the rest of the plant
- autonomy and fault modes in a real environment

### B. Do **not** include long-duration LOX/LH2 cryogenic depot capability in Phase 0
If you want Phase 0 propellant utility, keep it to:
- **water** as a delivered commodity (for later electrolysis elsewhere)
- **gaseous** O2/H2 for near-term station needs
- small quantities of LOX only if you can consume it quickly (days–weeks), not store it for months

### C. Reserve interfaces and margins explicitly in the Phase 0 station design
This is the most important “include it” action. Concretely:
- **Power**: reserve switchgear, cabling, and thermal rejection capacity for a future **+1–3 MW** ISRU expansion.
- **Thermal**: allocate a “cold zone” with sunshield attachment points and radiator real estate for future cryo systems.
- **Mechanical**: standardized module ports, fluid quick-disconnects, and structural hardpoints for tankage.
- **Operations**: define propellant quality specs, sampling ports, and metrology from day one.

This lets Phase 1 add a depot module without redesigning the core refinery.

---

## 4) Propellant choices: avoid LH2 as the Phase 0 driver

If the program insists on “usable propellant” in Phase 0 beyond pilot scale, the best near-term path is **storable or semi-storable** products that reduce boiloff and cryo complexity:

- **Water as propellant** (for resistojets/steam propulsion) for stationkeeping and low-thrust logistics: extremely storage-friendly and directly enabled by carbonaceous feedstock.
- **LOX + methane** is attractive long-term, but methane synthesis (Sabatier) requires CO2 (or carbon sources) and adds reactors, catalysts, thermal control, and more process risk. Still likely easier than LH2 storage.
- **LOX-only** can be valuable as an oxidizer top-off if your vehicles bring fuel from Earth initially. LOX storage is far easier than LH2, though still cryogenic.

Hydrazine/MMH/NTO-from-asteroids is speculative for Phase 0. Don’t plan critical path around complex organic synthesis.

---

## 5) Decision-driving research: what to model and what “break-even” really means

To resolve this rigorously, the propellant demand model must be tied to the Phase 0 mission set, not generic “future swarm” intuition. I recommend:

1. **Define Phase 0 transportation architecture explicitly**
   - What propulsion do asteroid retrieval vehicles use (solar electric, chemical, hybrid)?
   - Are tugs cycling between L4/L5 and elsewhere, or is Phase 0 mostly local processing?
   - What is the assumed cadence of retrieval missions?

2. **Compute propellant demand by function**
   - Retrieval: trajectory correction, capture, rendezvous margins
   - Tug operations: outbound/inbound burns, stationkeeping, contingency reserves
   - MPS own needs: attitude control, desaturation, collision avoidance

3. **Compare three supply options**
   - Earth-supplied propellant
   - L4/L5-produced water (used directly or shipped)
   - L4/L5-produced LOX/LH2 (or LOX/CH4)

4. **Include the real costs**
   - added solar arrays (mass, deployment risk, pointing)
   - radiators and cryocoolers (mass, failure modes)
   - ops staffing / autonomy development
   - schedule risk (a depot that slips can stall everything)

The likely outcome is that **water extraction becomes cost-effective early**, while **cryogenic depot economics** only close when there is sustained high throughput demand and when you can amortize the depot over many tug cycles.

---

## 6) Concrete Phase 0 recommendation (opinionated)

**Adopt a two-tier Phase 0 requirement:**

1) **Mandatory:** “Propellant-ready” station architecture + water extraction/purification pilot  
- Deliverable: verified water yield and purity from representative feedstock, continuous operation for months, autonomous fault recovery, quantified power/thermal loads.

2) **Optional stretch goal (only if margins allow):** limited electrolysis for station use and demonstration refueling of a small vehicle using **water or gaseous O2/H2**, not long-term cryogenic storage.

**Defer**: full-rate electrolysis, liquefaction, and long-duration LOX/LH2 storage to Phase 1, when you have:
- validated feedstock yields
- validated autonomy
- a transportation system that can actually consume the propellant at scale
- a power system sized for it (likely beyond the current 2.5 MW ceiling)

---

## 7) Implication for the consensus spec

This approach keeps the Phase 0 MPS aligned with the current mass/power/budget envelope while still answering the strategic question (“can we make propellant from asteroid material reliably?”) with flight data—without turning Phase 0 into a depot program.

If the group wants a single sentence for the spec:  
**“Phase 0 MPS shall include water extraction and purification with interfaces reserved for future propellant production; full cryogenic propellant depot capability is out of Phase 0 scope.”**