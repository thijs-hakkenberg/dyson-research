# Can hydrogen strip sulfur from asteroid Fe-Ni before melting? What the literature says

**For:** the project owner
**Compiled:** 2026-11-12
**Answers:** `publications/handover/rq-0-56-fe-ni-desulfurisation-literature-brief.md`
**Companions:** `papers.yaml`, `parameters.yaml`

## Verdict

**Undetermined, and undetermined for a specific reason: the one number the route stands on has
never been measured, as far as the accessible literature goes.** The chemistry itself survives
scrutiny - the equilibrium the simulator assumes is confirmed against a standard thermodynamic
compilation to within 20 percent, and the awkward consequence of that equilibrium, that several
hundred moles of hydrogen must circulate per mole of sulfur removed, is confirmed rather than
exaggerated. What does not exist is any measured rate for stripping sulfur out of FeS with
hydrogen between 700 and 950 C. One paper has it as its stated subject, from 1987, and it is
closed through every route tried. Everything the simulator reports about the hydrogen route -
the 24-hour, 48-hour and 96-hour hold times, the pass rates, the grind-size thresholds - rests
on a parameter with no source behind it, and that is unchanged by this review.

Separately, the review turned up a measured limit the simulator does not model and that works
against its headline result. Sulfur does not simply leave; it sits in an equilibrium with the
gas, and reduced iron holds 0.02 mass% of it dissolved in the bulk whenever FeS is still
present, with up to ten times that much adsorbed on surfaces and segregated to grain
boundaries. The model's claim of **under 0.01 percent sulfur is below the bulk solubility at
the Fe/FeS boundary**, so it is reachable only if the recirculating gas is held meaningfully
cleaner than the brief's own equilibrium figures imply, and only if the product is dense rather
than porous. That is a real constraint on the cold trap and on the product form, and it was not
in the model.

Nothing found kills the route. Nothing found supports it either, in the sense the brief
intended. The honest position is that this is a bench-test question, not a literature question,
and the bench test is specified at the end of this document.

## Parameters where the supported range falls outside the assumed one

None of the assumed ranges is contradicted outright by a source. Three corrections and
additions are worth carrying:

1. The free-energy expression is mildly conservative, not wrong. The simulator's
   `dG = 59960 - 3.2*T` J/mol gives an equilibrium constant 0.82 times the tabulated value at
   900 C and 1.03 times it at 600 C. A fit to the tabulated data over 873-1173 K is
   `dG = 66388 - 10.34*T` J/mol. Swapping it in makes the hydrogen route slightly easier, not
   harder; it is not urgent.
2. A residual-sulfur floor of 0.02 to 0.2 mass% needs to enter the model as a new parameter.
   The simulator currently has no floor and can report arbitrarily low sulfur.
3. Sulfur re-absorption from the recirculating gas needs to enter the model as an equilibrium,
   not be assumed away. It is fast at process temperature.

## Priority 1: the hydrogen step

### 1a. Reaction rate - not found

This is the central result of the review, and it is a negative one. Searches were run across
OpenAlex free text and restricted to *Metallurgical and Materials Transactions B*,
*Metallurgical Transactions B*, *ISIJ International*, *Canadian Metallurgical Quarterly*,
*Minerals Engineering*, *JOM* and *Journal of Sustainable Metallurgy*, in both the American and
British spellings, under eleven query families covering troilite, pyrrhotite, iron sulfide,
sulfide concentrates, sponge iron, direct-reduced iron and powder-metallurgy hydrogen
annealing; plus arXiv and the NASA Technical Reports Server. Crossref's search endpoint was
also tried and did not respond.

Exactly one indexed paper has the reduction of iron sulfide by hydrogen as its stated subject:
Wiltowski, Hinckley, Smith and Nishizawa, *Journal of Solid State Chemistry* 71 (1987) 95. It
is closed through Unpaywall, Semantic Scholar, PubMed Central, Crossref text-and-data-mining
links and direct DOI resolution, and the publisher releases no abstract. **None of its numbers
appear anywhere in `parameters.yaml`**, and it should be obtained through interlibrary loan
before any further modelling of this route. Its twenty-seven citing papers are almost entirely
about underground hydrogen storage and iron-oxide reduction, which suggests it has not been
used as a kinetics source by anyone since.

What exists instead is adjacent and worth reading as such:

- **The reverse reaction, measured, on particles of our size.** Kimura and colleagues sulfurised
  porous reduced iron with H2S in 75 percent hydrogen at 457-704 C, particle radius 90-500 um,
  and separated an intrinsic rate constant from pore diffusion. The activation energy is low,
  5.5 kcal/mol or 23 kJ/mol, meaning the surface chemistry is fast and the observed rate is set
  by diffusion through the solid. Two things transfer. First, if the chemistry is fast in one
  direction it is fast in the other, and the time constant we need is a transport number, which
  is consistent with the simulator's shrinking-core treatment and its grain-size-squared
  scaling. Second, their solid *lost* porosity as sulfide grew, because FeS is bulkier than Fe.
  Run backwards, the same volume change opens porosity instead of sealing it, which argues
  against the brief's worry that an iron product layer sinters shut and stalls the reaction.
  Both of these are inferences by reversal, not measurements of our reaction, and their
  temperature range stops below ours.
- **Nickel sulfide in hydrogen**, 723-873 K, linear kinetics, activation energy 103 kJ/mol.
  Wrong sulfide, below our window, and linear rather than diffusion-controlled, so it cannot be
  converted into `tau_h2_h`. It is listed because it is the nearest measured sulfide-plus-
  hydrogen rate found.

### 1b. Equilibrium - confirmed

Iguchi and Itoh tabulate the equilibrium ratio pH2S/pH2 in equilibrium with solid Fe and solid
FeS, taken from Knacke, Kubaschewski and Hesselmann's *Thermochemical Properties of Inorganic
Substances* (2nd ed., Springer 1991) - a named standard compilation, as the brief required:

| Temperature | (pH2S/pH2) at equilibrium |
|---|---|
| 873 K (600 C) | 3.70 x 10^-4 |
| 973 K (700 C) | 9.47 x 10^-4 |
| 1073 K (800 C) | 2.03 x 10^-3 |
| 1173 K (900 C) | 3.84 x 10^-3 |

The simulator's K at 900 C is 3.14 x 10^-3 against a tabulated 3.84 x 10^-3. Close enough that
the model's conclusions do not move, and conservative in direction.

The gas-circulation consequence follows directly and is now sourced: at 900 C, hydrogen
circulated per mole of sulfur removed is 289 mol at 90 percent approach to equilibrium, 521 mol
at 50 percent and 868 mol at 30 percent. The brief's figure of 300 to 1000 mol H2 per mol S is
supported across the whole assumed approach range. This is a large gas inventory to move and
re-clean, but the model was not being pessimistic about it.

Whether nickel - in pentlandite, or dissolved in the metal - shifts the equilibrium could not
be established. No source was found either way.

### 1c. Side reactions

**Sulfur does come back.** This is the clearest and most useful measured result in the review.
Iguchi and Itoh measured how much sulfur porous reduced iron takes up from H2-H2S mixtures at
sulfur activities *below* the Fe/FeS boundary, so no FeS forms - and it still takes up sulfur,
quickly, from gas containing only a few hundred to a few thousand ppm H2S. The uptake follows a
Langmuir isotherm, controlled by surface diffusion of adsorbed sulfur at 873 K shifting towards
pore diffusion as temperature rises. Practically: the cold trap and the cooling path are part
of the sulfur specification. Cooling the product in gas that has not been cleaned puts sulfur
back on it.

**And there is a floor.** They state the bulk solubility limit of sulfur in reduced iron is
0.020 +/- 0.002 mass% at 1173 K, and that this is only 10 percent of the saturated sorption
content of 0.2 mass% they measure - the rest being adsorbed on pore surfaces and segregated to
grain boundaries, tracking BET specific surface area. For the project this means two things.
Reaching 0.01 wt% sulfur requires holding the gas below the Fe/FeS boundary, around half the
equilibrium ratio, roughly pH2S/pH2 under 1.9 x 10^-3 at 900 C. And the 0.2 mass% plateau was
measured on highly porous iron reduced from ore; our concentrate is dense metal grains with a
far smaller specific surface area, so the surface term should be far smaller - but scaling it
down is an inference from their surface-area correlation, not a measurement on dense grains.
This is the first thing a bench test should settle.

**Hydrogen does attack silicate FeO.** Sargeant and colleagues reduced Apollo soils, a lunar
meteorite and a simulant at 1000 C for 4 h in about 420 mbar hydrogen and report that pyroxene
and olivine, not only ilmenite, showed minor reduction, with the mare soil yielding 0.94 wt%
oxygen. So the second consumable loss the brief suspected is real. It is an upper-bound
analogue rather than our case - lunar soil is finer, more ilmenite-rich and space-weathered,
and 1000 C is above our ceiling - and no rate constant is available. Note that the water
produced competes with H2S for the same cold trap.

**Sintering of the bed** is a genuine risk but is unquantified for our material. Iguchi and
Itoh observed sintering of their particles at 973 K and record specific surface area falling as
temperature rises; again, fine porous reduced iron is far more sinter-prone than dense 60-250
um grains. No source was found describing what practitioners do about it over 24-96 hour holds.

**Phosphorus, carbon and chromium: nothing found.** Schreibersite, carbide and chromite
behaviour under hydrogen at 800-950 C was searched for and not found. The product phosphorus
content remains unconstrained, and no product specification can be written against it yet.

### 1d. Prior art - the informative near-miss

No hydrogen desulfurisation of iron sulfide at any scale was found, on Earth or proposed for
space. The closest industrial analogue is instructive precisely because of the route it did
*not* take. Yu, Liu, Zhang and Barati set out to raise the Fe/S ratio of a fine nickeliferous
pyrrhotite concentrate at 873-1173 K in order to precipitate an Fe-Ni alloy out of the sulfide
- structurally the same problem as ours. Their route is partial oxidation, driving sulfur off
as SO2, followed by hydrogen reduction of the oxide that forms. Hydrogen is used on the oxide,
not to strip the sulfide. A group working on exactly this transformation, with no constraint on
reagents, did not choose direct hydrogen stripping. That is weak evidence rather than a
refutation - they had cheap air and an SO2 plant, and we have neither - but it is the kind of
evidence worth recording, and it is consistent with the equilibrium being as unfavourable as
the table above says.

The separate terrestrial trick for making sulfide reduction thermodynamically easy is to add
lime, so that the sulfur leaves as solid CaS rather than as H2S. That literature exists, for
copper sulfides. It is the option the project has already ruled out on import mass.

## Priority 2: the feed

This section is mostly a list of things that are not written down, which matters because the
simulator's pass rate for a 48-hour hold falls from 1.00 at 60 um to 0.18 at 250 um.

- **Metal grain size distributions for H, L and LL chondrites by petrologic type: not found.**
  The right papers were located but their distributions are in paywalled figures and tables.
  One structural point does come through: Kimura, Grossman and Weisberg establish that in type
  3 ordinary and CO chondrites metal occurs inside chondrules, on chondrule surfaces, and as
  isolated grains in the matrix. A single d50 is a poor description of that feed whatever its
  value - the distribution is at least bimodal by mode of occurrence, and the simulator should
  probably not be parameterised with one number.
- **Fraction of troilite locked in metal: no number.** Only qualitative evidence, and from
  enstatite chondrites rather than ordinary ones: van Niekerk and Keil report metal assemblages
  in EL3s usually intergrown with silicate, and sulfides sometimes intergrown with silicate.
  The brief's judgement that sulfide fully enclosed in metal is the most likely hidden failure
  is neither confirmed nor refuted.
- **Magnetic separation of crushed chondrite: not found, and probably never done.** The NASA
  Space Resources beneficiation chapter is a research-needs document that recommends bench
  separation experiments on crushed rock and meteorite be carried out, rather than reporting
  any. That is positive evidence of absence rather than a failed search.
- **Grinding energy of chondritic material: not found.** The meteorite mechanical-properties
  literature is about strength, porosity and density, not comminution work index.
- **Bulk feed composition by class:** the standard compilation is Jarosewich's Smithsonian
  analyses. The record was confirmed but the tables were not reachable, so no numbers are drawn
  from it and the simulator's `FEEDS` definitions remain unchecked. One independent constraint
  did surface: Gattacceca and colleagues report bulk metal content of ordinary chondrites
  falling with increasing petrologic type, a dependence the class-only feed definition does not
  carry.

## Priority 3: the alternatives

Only the liquation question was reached; the melt-with-slag and carbonyl parameters are
deferred under the brief's stop rule.

**Liquation is undermined by measurement, which agrees with the simulator.** Matsubara,
Terasaki, Yoshino and Urakawa measured dihedral angles between solid iron and Fe-S liquid of 30
to 48 degrees, all below the 60 degree percolation threshold, and conclude that the melt forms
interconnected networks and that a fraction remains as trapped melt - the "trapped melt" seen
in iron meteorites. Crossley and colleagues reach a compatible conclusion for sulfide melt
percolating through silicate-metal matrices. A wetting liquid in an interconnected network is
exactly the capillary hold-up the simulator says defeats draining. Two caveats: a dihedral
angle is not the simulator's contact-angle cosine, and no conversion between them is attempted
here; and the experiments are at 0.5-3.0 GPa, while a centrifuge crucible runs near zero
pressure. The direction is nonetheless unambiguous, and the simulator's verdict on liquation is
now supported by measurement rather than by the model alone.

**Carbonyl extraction: nothing.** No carbonylation rate on meteoritic or Fe-Ni alloy feed, no
treatment of sulfur as catalyst or poison, no passivation study, no demonstration on real
meteorite. Searches returned iron pentacarbonyl as a chemical-vapour-deposition and
nanoparticle precursor instead. All three carbonyl parameters remain unsupported.

**Surface tension of Fe-S liquids: not found** alongside the wetting work.

## What a bench test would have to measure

The literature cannot settle this route. A tube-furnace campaign can, and it is small. In
priority order:

1. **The rate, and whether it stalls.** Stoichiometric synthetic troilite - obtainable in bulk
   by the pyrite-decomposition route of Moreau and colleagues - sieved into narrow size
   fractions at roughly 50, 100 and 200 um. Hold in flowing hydrogen at 800, 875 and 950 C.
   Measure fractional conversion against time by thermogravimetry, to at least 100 hours or
   until the curve flattens. This gives `tau_h2_h` directly, gives the activation energy from
   the three temperatures, gives the size scaling from the three fractions - settling whether
   time goes as grain size squared as the simulator assumes or linearly - and shows any
   conversion ceiling. Nothing else in this programme matters as much.
2. **The floor.** On the same material taken to apparent completion, measure total sulfur by
   combustion analysis *and* BET specific surface area, then repeat after consolidation by hot
   pressing. This separates the bulk-dissolved sulfur, which is capped near 0.02 mass% while
   any FeS remains, from the surface and grain-boundary sulfur that scales with area and that
   Iguchi and Itoh found to be ninety percent of the total on porous iron. It is what decides
   whether "under 0.01 percent" is a real product specification or a modelling artefact.
3. **The gas, run dirty.** Repeat the 900 C run with H2S deliberately added at
   pH2S/pH2 of about 1 x 10^-3 and 3 x 10^-3, bracketing the 3.84 x 10^-3 equilibrium ratio.
   This measures the approach term `h2_approach`, which no source constrains, and establishes
   how clean the cold trap actually has to be - a design input for the recirculation loop.
4. **The real feed.** The same 900 C, 48-hour hold on a crushed and magnetically separated
   ordinary-chondrite sample or a faithful simulant, sectioned afterwards and examined for
   residual sulfide. This is the only way to get at `locked_fes` - whether sulfide enclosed in
   metal is reached by the gas at all - and it also exposes whether the bed sinters over a long
   hold, and where phosphorus ends up if the feed carries schreibersite.
5. **The side reaction.** Weigh water as well as H2S in the trap on run 4, to bound how much
   hydrogen is lost reducing silicate FeO at 900 C rather than at the 1000 C of the lunar work.

Runs 1 and 2 answer the question the brief was written around. Runs 3 to 5 size the plant.

## Review notes (2026-11-12, simulator author)

Checked: all 17 DOIs resolve in Crossref to the stated title, first author and year; the
free-energy fit reproduces the tabulated ratios to within 20 J/mol; every simulator parameter
named in the brief has an entry and every `assumed` range matches `PHYSICS_RANGES`.

Three qualifications to the text above. The estimates in them are mine, back-of-envelope, and
unsourced.

1. **The 0.02% figure is an equilibrium with the gas, not a floor.** Dissolved sulfur scales
   with pH2S/pH2, so once the last FeS is gone it keeps falling as the return gas gets cleaner.
   What it sets is a cold-trap requirement: the H2S vapour pressure at the trap temperature,
   divided by the loop pressure, must be below about 1.9 x 10^-3 for 0.01% S. At 1 bar that is
   a trap colder than roughly 140 K; a trap at 150 K would return gas dirtier than equilibrium
   and remove nothing. The simulator has no trap temperature and needs one.
2. **"Fast in one direction, so fast in the other" is weak.** It holds near equilibrium only.
   The stronger statement is a bracket: if the iron product layer is porous, H2S diffusing out
   through it clears a 100 um grain in under a minute and the step is limited by gas
   throughput, which the model already carries; if the layer is dense, sulfur must diffuse
   through solid iron and the same grain takes on the order of 100 hours. The assumed 2-40 h
   lies between the two, so product-layer morphology decides the route. Bench run 1 should
   section the partly converted grains, not only weigh them.
3. **Several "not found" entries reflect what the search could reach, not what exists.** Metal
   grain sizes in ordinary chondrites, Fe-S liquid surface tension, slag sulfur partition and
   silicate melt viscosity all have substantial literatures behind paywalls. Only `tau_h2_h`,
   magnetic separation and grinding energy should be read as probably unmeasured. For
   `tau_h2_h` the unexplored lead is coal science: pyrite and pyrrhotite reduction in hydrogen
   during coal hydropyrolysis (journals such as *Fuel* and *Fuel Processing Technology*),
   which is where the Wiltowski group worked.
