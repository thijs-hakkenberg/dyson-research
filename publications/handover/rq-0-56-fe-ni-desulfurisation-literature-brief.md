# Literature brief: can hydrogen remove sulfur from asteroid Fe-Ni before melting?

**For:** the literature research agent (DB machine)
**Written:** 2026-11-12
**Research question:** rq-0-56 (Fe-Ni refining), with input to rq-0-50 and rq-0-80 (recoverable metal)
**Plan items:** `reconciliation/phase-0/PLAN-2026-11.md` §4.4, and the part of §4.2 that feeds the same simulator

## Why this brief exists

Project Dyson's Phase 0 plan makes structural iron-nickel from ordinary-chondrite asteroid
material. The unsolved problem is sulfur. The metal grains sit next to troilite (FeS), and
simply melting the feed leaves 1–3% sulfur in the product, which makes it brittle. On Earth
this is fixed with large amounts of lime flux and a 1 g furnace; neither is available.

We built a screening simulator (`publications/scripts/smelting_sim.py`) that compares ten
process routes under 23 uncertain physical parameters. One route passes in the model:

1. grind to about 60–100 µm and separate magnetically;
2. hold the concentrate in recirculating hydrogen below about 950 °C, so that
   FeS + H₂ → Fe + H₂S, freeze the H₂S out in a cold trap and reuse the hydrogen;
3. melt the now low-sulfur metal in a small spinning crucible to clear the slag.

In the model this gives under 0.01% sulfur for about 1 kWh/kg and about 10 kg of imports
per tonne. **Every one of those numbers rests on parameter ranges I estimated from general
engineering knowledge, not from sources.** The route stands or falls on one of them: how
fast hydrogen strips sulfur from troilite grains. Your job is to replace the estimates with
sourced values, and to find out whether anything known about this chemistry kills the route.

A result that kills the route is as useful as one that supports it. Do not look for
confirmation.

## What I need back

For each parameter below: the range the literature supports, the conditions it was measured
under, and the sources. Where sources disagree, report both positions with their conditions;
do not average them or pick one. This project keeps disagreements on record.

### Priority 1: the hydrogen step (decides the route)

**1a. Reaction rate of troilite with hydrogen.** Simulator parameter `tau_h2_h`: the time
constant for desulfurising a 100 µm troilite grain at 900 °C in flowing H₂, assumed 2–40 h.
The decision thresholds from the simulator are:

| Time constant at 100 µm, 900 °C | Consequence |
|---|---|
| under ~14 h | a 24-hour hold is enough |
| 14–22 h | a 48-hour hold passes (pass rate 0.94) |
| 22–40 h | a 48-hour hold mostly fails (0.28); 96 hours needed |
| over ~40 h | the route is in trouble at any practical hold time |

So I need measured rates, and specifically:
- rate constants or conversion-against-time curves for FeS (troilite or stoichiometric
  synthetic FeS, and pyrrhotite Fe₁₋ₓS reported separately) in H₂ between 700 and 950 °C;
- the activation energy, so the rate can be moved between temperatures;
- **what controls the rate**: surface reaction, gas diffusion through the porous iron
  product layer, or solid-state diffusion. The simulator assumes a shrinking core with time
  scaling as grain size squared. If the real scaling is linear in size, or if the iron
  product layer sinters shut and the reaction stalls short of completion, say so. A
  conversion ceiling below about 97% would change the result;
- the effect of H₂S partial pressure in the gas on the rate (the gas is recirculated, so it
  is never perfectly clean).

**1b. Equilibrium.** The simulator uses ΔG° = 59,960 − 3.2·T J/mol for
FeS + H₂ = Fe + H₂S, giving K ≈ 3×10⁻³ at 900 °C, which means roughly 300–1,000 mol of H₂
circulated per mol of sulfur removed. Check this against tabulated thermodynamic data and
report the supported expression and its uncertainty. Check whether nickel in the sulfide
(pentlandite) or dissolved in the metal shifts it.

**1c. Side reactions that consume hydrogen or return sulfur.** These are not in the
simulator at all:
- Does H₂ at 800–950 °C reduce the FeO in the olivine and pyroxene that remain in the
  concentrate, and at what rate? That would turn hydrogen into water and be a second
  consumable loss.
- Does the product re-absorb sulfur from H₂S on cooling?
- Do phosphides (schreibersite), carbides, or chromite/daubréelite react, and where do P and
  C end up? The product specification will have a phosphorus limit and we have no number.
- Does the metal powder sinter into a gas-tight mass at 900 °C over 24–96 h, and what do
  practitioners do about it (fluidised beds, rotary kilns, vibration)?

**1d. Prior art.** Has H₂ desulfurisation of iron sulfide been run at any scale, on Earth or
proposed for space? Likely places: hydrogen reduction of pyrrhotite/pyrite concentrates in
extractive metallurgy, sulfur removal in direct-reduced iron and powder metallurgy
(hydrogen annealing of iron powder), lunar ISRU hydrogen-reduction work (sulfur release
from regolith is reported as a nuisance there), and heating experiments on chondrites in
reducing gas from the meteoritics literature. Report scale, temperature, residence time,
residual sulfur achieved.

### Priority 2: the feed (decides how fine we must grind)

The route needs fine grinding: with a 48-hour hold the pass rate is 1.00 at 60 µm, 0.85 at
100 µm, 0.56 at 150 µm and 0.18 at 250 µm. Fine powder is hard to handle in microgravity,
so the real grain sizes matter.

| Parameter | Assumed | Need |
|---|---|---|
| `metal_d50_um` | 80–400 µm | Measured size distributions of metal grains in H, L and LL chondrites, by petrologic type (3–6). Report distributions, not just means. |
| `locked_fes` | 0.08–0.45 | What fraction of troilite is intergrown with or enclosed in metal, against free-standing in silicate. Sulfide fully enclosed in metal cannot be reached by gas; this is the most likely hidden failure. |
| (not modelled) | — | Size distribution of the troilite grains themselves. The rate in 1a scales with troilite size, not metal size. |
| `locked_sil`, `mag_recovery` | 0.4–3%; 0.88–0.98 | Any magnetic-separation tests on crushed chondrite or meteorite simulant: metal recovery and concentrate grade against grind size. |
| `bond_wi` | 12–20 kWh/t | Crushing or grinding energy measured on ordinary chondrites. |

Also report bulk metal, troilite and FeO contents by class (H, L, LL, EH, EL) with spread,
to check the simulator's feed definitions.

### Priority 3: the alternatives (decide whether there is a fallback)

Only after 1 and 2. One paragraph and a parameter range each is enough.

- **Carbonyl (Mond) extraction** — `tau_carb_h` 15–300 h (100 µm, 100 bar CO, 175 °C),
  `carb_cap` 0.80–0.97, `co_loss` 0.2–3%. Measured iron and nickel carbonylation rates on
  meteoritic or Fe-Ni alloy feed specifically (not pure nickel); the role of sulfur as
  catalyst or poison; passivation; any demonstration on real meteorite.
- **Liquation** (draining the Fe–FeS liquid above 988 °C) — `gamma_sulfide` 0.35–0.9 N/m,
  `wetting_cos` 0.6–1.0. Surface tension of Fe–S liquids and their wetting of solid iron.
  The simulator says capillary hold-up defeats this route; dihedral-angle and melt-migration
  experiments from the planetary core-formation literature bear directly on that.
- **Melt with slag** — `ls_native` 0.3–5, `ls_flux` 20–200: sulfur partition between
  FeO-rich chondritic silicate melt and Fe-Ni metal, and with CaO-rich reducing slag.
  `mu_sil_1600` 0.3–5 Pa·s. `k_vac_S` 5×10⁻⁷–10⁻⁵ m/s for vacuum desulfurisation.

## Where to look

Most of this is not on arXiv. It is in extractive-metallurgy, powder-metallurgy and
meteoritics journals (for example *Metallurgical and Materials Transactions B*, *ISIJ
International*, *Meteoritics & Planetary Science*, *Geochimica et Cosmochimica Acta*,
*Acta Astronautica*), in NASA technical reports (NTRS), and in the Space Resources
Roundtable and ASCE Earth & Space proceedings. Older work matters here: much of the sulfide
reduction kinetics dates from the 1950s–1980s. Thermodynamic data should come from a
standard compilation (NIST-JANAF, Barin, or FactSage-derived papers), named explicitly.

I am deliberately not listing papers. I do not have verified citations for this topic, and
a list from memory would steer you towards whatever I happen to recall.

## Rules for evidence

- **Mark how you know each number.** For every value, state whether you read it in the full
  text, took it from an abstract, or inferred it from a figure or from a different material
  or condition. An extrapolated value (for example from pyrite at 500 °C to troilite at
  900 °C) is welcome but must be labelled as one, with the extrapolation shown.
- **Every source needs a DOI, report number or stable URL** that you actually opened. If you
  could not open the full text, say so. Do not cite a paper you only saw referenced.
- **"Not found" is a result.** If there is no measurement for a parameter, say what you
  searched and where, and name the nearest analogue. That tells us a bench test is the only
  way to get the number.
- **Keep disagreements.** Two sources with different rates under different conditions go in
  as two rows.
- Do not edit `smelting_sim.py` or re-run the simulator. I will do that with your ranges.

## What to deliver

Follow the repository's existing layout for research-question literature, under
`src/content/research-questions/phase-0/rq-0-56-no-melt-fe-ni-refining/research/`:

1. `papers.yaml` — every source used: identifier, title, authors, year, relevance
   (critical/high/medium), a two-sentence summary, and `access: full-text | abstract-only`.
   (Same shape as the `arxiv-papers.yaml` files in other RQs, e.g. rq-0-11, but with a
   general `id` field since most sources will not be arXiv.)
2. `parameters.yaml` — one entry per simulator parameter named in this brief, plus any new
   quantity you think the simulator is missing:

   ```yaml
   - key: tau_h2_h
     assumed: [2, 40]            # what the simulator uses now
     supported: [low, high]      # what the literature supports, or null
     conditions: "..."           # material, temperature, gas, grain size as measured
     basis: measured | extrapolated | analogue | not-found
     sources: [id, id]
     note: "..."                 # disagreements, caveats, scaling law
   ```
3. `analysis.md` — written for the project owner, who is not a metallurgist. Start with
   the verdict on the hydrogen route in two or three sentences: supported, undermined or
   undetermined, and on what evidence. Then one section per priority. End with the
   measurements a tube-furnace bench test would have to make to settle whatever the
   literature leaves open (material, temperatures, grain sizes, what to measure).

Commit on a branch off `feature/wp-a-b-rebuild` and push. In your final message, lead with
the verdict and list any parameter where the supported range falls outside the assumed one.

## When to stop

Priority 1 is done when 1a has either two independent measured sources or a documented
"not found", and 1b and 1c each have a sourced answer or a documented gap. Do not let
priority 3 delay delivery of 1 and 2: if time runs short, deliver those and list what is
left.

## Background files

- `publications/scripts/smelting_sim.py` — the model; `PHYSICS_RANGES` near the top is the
  full list of assumed parameters with one-line descriptions.
- `publications/data/smelting-routes/results.json` — the route results and the thresholds.
- `src/content/research-questions/phase-0/rq-0-56-no-melt-fe-ni-refining.md` — the results
  written up.
- `publications/handover/paper-04-microgravity-metallurgy-handover.md` — earlier literature
  on melting in low gravity; do not repeat it.
