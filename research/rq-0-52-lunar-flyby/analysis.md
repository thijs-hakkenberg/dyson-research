# Lunar flybys for tug departure and return: what the literature supports

Compiled 2026-11-13 for rq-0-52. Sources are in `papers.yaml`; the parameter-by-parameter
record is in `parameters.yaml`.

## Verdict

The size of the flyby gain assumed in the trajectory study is supported. Four independent
trajectory analyses put the Earth-relative excess speed a lunar flyby gives on departure, or
absorbs on return, at 1.2–1.46 km/s; the study used 1.0 and 1.5 km/s. Two other parts of
the assumption are not supported as modelled: the study allowed 30 days per assisted leg
where the sources need 60–200, and it let the excess velocity point in any direction where
a short flyby sequence is limited to about 30° from the ecliptic. Correcting both cuts the
number of asteroids that close a four-year tug cycle at 5 km/s per leg from 20–45 to 5–16.

None of this is flight data. No vehicle has flown a lunar-assisted capture, and the escapes
that have flown (ISEE-3, Nozomi, STEREO) were small spacecraft, not 100-tonne tugs. Gravity
assists do not depend on vehicle mass, so the figures carry over; the operations do not.

## How big is the gain?

| Source | Case | Excess speed |
|---|---|---|
| Landau et al. 2013 (Keck retrieval study) | capture of a returning asteroid by one lunar flyby | up to 1.41 km/s (C3 2 km²/s²) |
| McElrath et al. 2012 (abstract only) | escape by lunar flybys within about two months | about 1.4 km/s (C3 ≈ 2) |
| Casalino and Filizola 2017 | one flyby from launch, numerically verified | 1.2, 1.3, 1.4 km/s |
| Chen 2023 | Sun-driven swingby sequences, escape or capture, any direction | 1.46 km/s; 1.8 km/s at best |
| Chen et al. 2016 | escape from a Sun–Earth halo orbit, one swingby | 1.61 km/s for two of four encounter geometries; 0.7 km/s or no escape for the other two |
| Chen et al. 2016 | same, after a second swingby 75–95 days later | about 1.64 km/s for all four |

Longer sequences give more: about 2.1–2.2 km/s (C3 4.5–4.8) from three swingbys over four to
six months (McElrath et al.; Chen 2023). McElrath et al. also state that a burn at Earth
perigee after the flybys can raise C3 from 2–3 to 10 or more; that needs high thrust, which
the tug does not have.

The study's 1.0 km/s case sits inside every source. Its 1.5 km/s case is slightly above the
general figures (1.41–1.46) and inside the favourable-geometry ones. A planning value of
1.4 km/s is the best-supported single number.

## What the study got wrong

**Time.** The study added 30 days per assisted leg. No source supports that. The closest
case to ours, leaving a Sun–Earth halo orbit, coasts along the orbit's unstable manifold to
the Moon and for half the encounter geometries needs a second swingby 75–95 days after the
first. McElrath et al. give about two months for C3 of 2. All-direction coverage in Chen
2023 uses Moon-to-Moon transfers of up to 200 days each. A defensible allowance is 60–90
days per leg, and up to 200 for unfavourable directions.

**Direction.** The study let the excess velocity point anywhere. Landau et al. limit a
single capture flyby at 1.41 km/s to arrivals within 30° of the ecliptic, with higher
energies only for in-plane arrivals at a favourable lunar phase. Chen 2023 reaches all
directions, but by chaining swingbys over months. So direction can be bought with time.

**The wait for the Moon.** Chen et al. 2016 assume the halo orbit is already phased for the
lunar encounter and leave the cost of phasing to later work. I found no source for it.

**Where capture ends.** Both retrieval designs end in lunar orbit after a further transfer
of months by way of the Sun–Earth L1/L2 region, with 20–350 m/s of insertion. Our tug
returns to a node at Sun–Earth L1. The route passes that neighbourhood, but nobody has
computed it for this case.

## Effect on the study's results

`publications/scripts/run_flyby_check.py` re-assembles the tug cycles with longer
allowances and re-solves all 6,863 flyby legs to find where their excess velocity points.
Of those legs, 61% are within 30° of the ecliptic and 80% within 45°; the median is 23°.

Asteroids of about 100 m or more that close a tug cycle of four years or less:

| Flyby, leg Δv cap | Study (30 d, any direction) | 60 d | 90 d | 200 d | 90 d and within 30° | 90 d and within 45° |
|---|---|---|---|---|---|---|
| 1.0 km/s, 5.0 km/s | 20 | 15 | 12 | 7 | 5 | 8 |
| 1.5 km/s, 5.0 km/s | 45 | 32 | 28 | 12 | 16 | 22 |
| 1.0 km/s, 6.5 km/s | 58 | 41 | 33 | 17 | 17 | 26 |
| 1.5 km/s, 6.5 km/s | 82 | 60 | 53 | 20 | 31 | 41 |

The direction columns are lower bounds: they drop legs that point too far out of the
ecliptic, where a re-optimised leg would keep some of them at a higher Δv.

Allowing five-year cycles restores the count: 51 targets (flyby 1.0 km/s, 5 km/s legs,
90 days) and 83 (flyby 1.5 km/s), before the direction limit.

In the chain model (rq-0-61) the longer allowance changes little besides the target count.
At 90 days and four-year cycles the import ratio is 0.42–0.43 and a 20-year run costs
1.6× Earth supply, the same as before. Five-year cycles add three or four tugs: the import
ratio stays at 0.42–0.44, but the six-year run rises from about 4.6× to 5.6–5.9× and the
20-year run from 1.6× to 1.75–1.8×
(`publications/data/phase0-chain/flyby-allowance.json`).

## Three-body model (added 2026-11-13)

Items 2 and 3 below have since been computed; see "Third pass" in the research question.
In short: the model reproduces the literature's swingby gain (up to 1.7 km/s from one
swingby, against 1.61–1.64 in Chen et al. 2016), finds that the coast from the node to the
Moon takes 22–65 days depending on a 300–50 m/s node burn, and gives the reach by direction
that the literature only sketches. With that table in the leg optimiser, 26 targets close at
5 km/s per leg and four years, so the lower bound of 5–16 above was too pessimistic and the
second pass's 20–45 too optimistic.

## What this leaves open

1. **The falsifier of 20 candidates no longer clears at the consensus leg cap.** With a
   supported flyby (about 1.4 km/s, 60–90 days, within 30–45° of the ecliptic) the count at
   5 km/s per leg and four years is roughly 5–22. It clears at 6.5 km/s per leg or at
   five-year cycles. The scout constraint was not re-applied here and can only lower these.
2. **Direction should be a constraint in the optimiser**, not a filter after it, and the
   time allowance should depend on it (short for in-plane, long for out-of-plane).
3. **The node-to-Moon leg and its phasing wait** need computing for a Sun–Earth L1 node, in
   both directions, in a three-body model. This is the part with no source.
4. **Sources not read:** Landau et al. AAS 12-165 and Lantoine and McElrath AAS 14-471 were
   not reachable. McElrath et al. 2012 was read as an abstract only.
