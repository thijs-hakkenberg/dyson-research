# Literature brief: is our NEA tug-cycle result new, and what does it contradict?

**For:** an outside literature research agent (no access to our repository; everything needed is here)
**Written:** 2026-11-24
**Research question:** rq-0-52 (low-thrust trajectories and cycle cadence to candidate NEAs), with rq-0-61 (chain cost model)
**Purpose:** novelty and positioning check before writing a paper (provisionally Paper 12, "NEA tug cycles through a Sun–Earth halo node with lunar swingbys")

## Why this brief exists

Project Dyson is a non-profit planning study for building large solar collectors from
asteroid material. Its Phase 0 plan relies on reusable solar-electric tugs that shuttle
between a staging station and near-Earth asteroids (NEAs). Several AI models proposed the
architecture and disagreed on how often a tug can complete a round trip. That disagreement
decides fleet size and propellant demand. The consensus spec set a falsifier: **at least 20
candidate asteroids must be reachable by a tug round trip of at most 5 km/s per leg (low
thrust) and at most 4 years per cycle.** If fewer qualify, the architecture does not close.

We built our own trajectory pipeline over several passes and now have results we think may
be worth publishing. Before writing, we need to know:

1. whether these results, or close equivalents, are already published;
2. which published results agree or disagree with our numbers, and under what assumptions;
3. what we must cite and compare against, so that a reviewer in astrodynamics would accept
   the framing.

**A finding that our result is already known, or that the literature contradicts it, is as
useful as one that supports it. Do not look for confirmation.** Where sources disagree with
each other, report both positions with their assumptions; do not average them or pick one.

## What we did (enough to judge overlap)

The architecture: a station on a Sun–Earth L1/L2 halo orbit (the "node orbit"; our best
case is a halo with ~120,000 km out-of-plane amplitude). A tug leaves the station with a
small impulsive burn (≤ 150–300 m/s) and falls toward Earth. A lunar swingby then raises its
Earth-relative excess speed (v∞), and it escapes. It flies a low-thrust heliocentric leg to
the asteroid, stays at least 60 days, and returns by the mirror route: capture by lunar
swingby, back to the node. The asteroid list is a catalogue screen of about 150 NEAs of about
100 m or more.

The pipeline, in order:

1. **Heliocentric legs:** multi-revolution low-thrust transfers (our own solver), with the
   Earth-relative v∞ at departure and arrival as free variables. A table of reachable v∞ is
   credited for the node-and-swingby phase.
2. **Node-to-escape leg:** solved directly in the circular restricted Sun–Earth three-body
   problem (CR3BP), from the station's actual place on the halo on the actual date. The Moon
   is on its real inclined orbit (5.1°), with its node line regressing, and the swingby is
   patched (instantaneous turn at the Moon's orbital distance, ≥ 100 km perilune). The leg
   must deliver the exact v∞ vector the heliocentric leg needs, within ±10 days. Any shortfall
   is charged to the tug's thrusters one for one. We solved 1,816 distinct legs from each of
   8 station places.
3. **Counting:** a target counts if an out leg and an in leg both fit the Δv cap and the
   node-to-node cycle fits the cycle cap.
4. **Station arrangements:** 1, 2, 4 or 8 stations evenly spaced round the halo, or one
   station with tugs that park and phase round the orbit (phasing costed by multiple
   shooting: about 187 m/s per eighth of the orbit; the cost follows the chord of the phase
   shift, as for a linear oscillator, so waiting longer does not help).
5. **Full-model check (new, 2026-11-23):** the node-to-escape legs of the best cycles flown
   again with the Moon's gravity throughout. The CR3BP's Earth point is taken as the
   Earth–Moon barycentre, with the Earth and the Moon either side of it. The legs are solved
   by multiple shooting from the patched path, with correction burns allowed every 10 days
   and the sum of burns minimised.

### Results we would claim

| Claim | Number |
|---|---|
| C1. At the consensus caps (5 km/s, 4 yr), one station: targets that close | 2–6 (depends on the station's place on the halo) |
| C2. Same caps, best arrangement (4–8 stations or free parking) | 11–15: falsifier of 20 not met |
| C3. Relaxing either cap meets it with one station | 17–27 at 6.5 km/s & 4 yr; 26–34 at 5 km/s & 5 yr |
| C4. Interpolated reach tables over-count | direct solve keeps about ⅔ (consensus caps) to ½ (relaxed) of table counts |
| C5. Station place on the halo matters | factor ~2–3 in count between places |
| C6. Phasing round a halo costs ≈ chord of phase shift × ~512 m/s per half orbit | 185 / 350 / 468 / 512 m/s for 1–4 eighths; independent of transfer time beyond ~120 d |
| C7. Patched lunar swingby underestimates leg cost | median +135 m/s per leg (quartiles 70 / 222; 90th percentile 348; max 572), mostly from the months spent near the Moon's orbit before the swingby, not the swingby itself; 32 → 24–27 targets |
| C8. Mixing frames (fixed Earth plus the Moon's indirect term) against patched Sun–Earth CR3BP states gives a spurious drift of ~12.5 m/s per node | modelling pitfall |
| C9. Lunar-swingby escape from a halo delivers a v∞ of ~1.2–1.46 km/s in 60–200 days; the direction is limited by the Moon's plane | supported earlier by the sources listed below |

## What I need back

### Priority 1: overlap (decides whether there is a paper)

**1a. Asteroid retrieval and mining logistics with reusable tugs and cycle counts.** Studies
that count how many NEAs a reusable vehicle can service within a Δv and round-trip-time
limit, ideally from an Earth–Moon or Sun–Earth libration-point station. For each: target
list size, Δv and time limits, the propulsion model, how Earth departure and arrival were
modelled (C3 given, lunar swingby, libration point), and the count found. In particular,
look at the "Easily Retrievable Objects" literature (e.g. García Yárnoz, Sánchez & McInnes
2013 and follow-ups), the Asteroid Redirect Mission trade studies, the Keck Institute
asteroid retrieval study (2012), and Strange/Landau/Brophy et al. on NEA accessibility via
lunar gravity assists.

**1b. Halo-orbit departures with lunar swingbys to a required v∞ vector.** Has anyone solved,
for many targets, the problem "from a fixed place on a Sun–Earth halo on a fixed date, reach
a given escape v∞ vector via a lunar swingby", and reported how often it is feasible?
Especially work that treats the station's phase on the halo as a variable (C5). We know Chen,
Kawakatsu & Hanada (2016) and Matsumoto & Kawaguchi (2005) (listed below); find what has
followed them.

**1c. Phasing along libration-point orbits.** Published costs for changing phase along a
halo or Lissajous orbit (rendezvous, constellation reconfiguration, formation flying), with
impulsive or low-thrust manoeuvres. Does anyone report the cost scaling with the chord of the
phase angle, or that waiting longer does not help (C6)? Also any phasing via the orbit's
stable and unstable manifolds, and what it costs in time and Δv. That is our open next step.

### Priority 2: the Moon's gravity on patched swingby legs (C7, C8)

**2a.** Published comparisons of patched-conic or instantaneous lunar swingby models against
full-force models (CR3BP plus Moon, bicircular four-body, or ephemeris), for libration-point
departures or Earth escape. What Δv penalty, deterministic correction cost or rate of lost
feasibility do they report? A median of about 135 m/s per leg is our number; is it in line,
high or low?

**2b.** Standard practice for the frame: is treating the Sun–Earth CR3BP secondary as the
Earth–Moon barycentre, with the Earth and Moon placed either side of it (a bicircular-type
model), the accepted way to add the Moon for L1/L2 work? Find sources that state this, and
any that describe the indirect-term pitfall in C8. If C8 is textbook material, say so; we
would then drop it as a claim.

**2c.** Typical statistical and deterministic trajectory-correction budgets for lunar-swingby
legs of 60–200 days (flown missions such as ARTEMIS, WIND, STEREO, Hiten, Nozomi,
ESCAPADE, or mission designs such as Hayabusa2 extended mission or DESTINY+), for comparison
with our 5–10 correction burns per leg.

### Priority 3: consensus inputs we have not sourced

**3a.** Capture of a loaded tug (low-thrust, arriving with v∞ ~1–1.5 km/s) back to a
Sun–Earth halo via lunar swingby: has it been designed or costed? Our in legs are the mirror
image of escapes, which is an assumption.

**3b.** Waiting at a libration-point node for a suitable lunar encounter: any published
analysis of encounter geometry recurrence (the Moon's phase against the halo phase) and the
resulting wait times.

## Sources we already have (do not re-report; do report anything that contradicts them)

- Chen, H. (2023). Capacity of Sun-driven lunar swingby sequences and their application in asteroid retrieval. *Astrodynamics* 7.
- Chen, H., Kawakatsu, Y., Hanada, T. (2016). Earth escape from a Sun–Earth halo orbit using unstable manifold and lunar swingbys. *Trans. JSASS* 59(5), 269–277.
- Landau, D., Dankanich, J., Strange, N., Bellerose, J., Llanos, P., Tantardini, M. (2013). Trajectories to nab a NEA. AAS 13-409.
- Casalino, L., Filizola, L. (2017). Design of high-energy escape trajectories with lunar gravity assist. ISSFD-2017-023.
- McElrath, T., Lantoine, G., Landau, D., Grebow, D., Strange, N., Wilson, R., Sims, J. (2012). Using gravity assists in the Earth–Moon system as a gateway to the solar system. GLEX 2012.
- Matsumoto, M., Kawaguchi, J. (2005). Escape trajectory and connection to interplanetary voyage from the Sun–Earth L2 point. *Space Technology Japan* 4, 43–52.
- Titles only so far, not yet read: "Efficient lunar gravity assists for solar electric propulsion missions"; "Families of solar-perturbed Moon-to-Moon transfers".

## Format of the reply

1. **Verdict per claim C1–C9:** *new* / *partly known* / *known* / *contradicted*, with one or
   two sentences and the sources that decide it.
2. **Closest prior work:** the 5–10 papers a reviewer would expect us to cite and compare
   against, each with what it did, its assumptions, its headline numbers, and how it differs
   from ours.
3. **Per question above (1a–3b):** findings with full references (authors, year, title,
   venue, DOI or URL). Mark each source as read in full, abstract only, or cited secondhand.
4. **Disagreements:** where sources disagree with each other or with us, both positions and
   their assumptions, side by side.
5. **Gaps:** what you searched for and did not find (search terms and databases), so that
   absence is evidence rather than silence.

Useful databases: NASA ADS, NTRS, AIAA ARC, AAS proceedings, ISSFD and IAC archives,
J-STAGE (Japanese work on halo escapes is strong), arXiv (astro-ph.EP, math.DS), Google
Scholar. Suggested terms: "near-Earth asteroid accessibility reusable", "asteroid retrieval
lunar gravity assist", "easily retrievable objects", "halo orbit escape lunar swingby",
"libration point orbit phasing", "halo orbit rendezvous phasing cost", "bicircular
restricted four-body problem L2 escape", "patched conic lunar flyby error", "Sun–Earth–Moon
transfer correction manoeuvre budget".

Do not include anything behind a paywall verbatim. Summaries with references are what we need.
