<!--
Outside literature review answering publications/handover/rq-0-52-nea-tug-cycles-literature-brief.md.
Written by a separate research agent on 2026-11-24; kept as received apart from the figure note.
Read levels (F/A/M/S) are the reviewer's, not ours. Our response, including three points where the
review misreads our runs, is in rq-0-52, section "Novelty and positioning review (2026-11-24)".
-->

# NEA tug cycles through a Sun–Earth halo node: novelty and positioning review

**Research question:** rq-0-52 (with rq-0-61) · **Reviewed:** 2026-11-24 · **Scope:** brief questions 1a–3b, claims C1–C9

---

## Bottom line

There is a paper here, but not the one the claim list currently describes. The counting result, meaning how many NEAs
a reusable tug can service through a Sun–Earth halo node under a joint Δv-and-cycle-time cap with the Earth-side
legs solved in the CR3BP from an actual halo phase on an actual date, has no published equivalent, and C1, C2
and C5 appear genuinely new. The force-model result (C7) is also new, but its headline number is an order of
magnitude larger than every published patched-to-full-model transition penalty I could find, so it will be the
first thing a referee attacks. Against that, two claims should be withdrawn or heavily reframed. **C6 is
substantially pre-published**: the chord-like scaling, the independence from initial phase, and even the
manifold detour the brief names as the team's "open next step" all appear in
[Sato, Kitamura & Shima 2015](https://doi.org/10.2322/tjsass.58.261) and
[Chen & Ma 2017](https://doi.org/10.2514/1.g002518). **C8 is a known property of bicircular-type models**,
stated plainly as non-coherence by [Jorba-Cuscó, Farrés & Jorba 2018](https://doi.org/10.3389/fams.2018.00032).
C9 is likewise already established, in quantitative detail, by
[Casalino & Lantoine 2020](https://doi.org/10.1007/s40295-020-00229-w).

The single most important omission from the brief's source list is
[Chen, Kawakatsu & Hanada 2016b](https://doi.org/10.1016/j.actaastro.2016.05.003), *Phasing Delta-V for transfers
from Sun–Earth halo orbits to the Moon*, by the same authors the team already cites, in the same volume of *Acta
Astronautica* as two other papers in this review. It answers brief question 3b directly and bears hard on C6.

---

## Verdicts on C1–C9

| Claim | Verdict | Deciding evidence |
|---|---|---|
| **C1** — 2–6 targets close at 5 km/s / 4 yr, one station | **new** | No published survey counts round-trip-accessible NEAs from a libration-point node. Nearest comparators measure something else: [Xie & Dempster 2022](https://doi.org/10.1109/aero53065.2022.9843463) count low-thrust round trips from Earth, [Peng, Zhang & Gao 2024](https://doi.org/10.3390/aerospace11070546) count flybys from a lunar DRO. |
| **C2** — 11–15 at best arrangement; falsifier of 20 unmet | **new** | No published multi-station or parked-and-phased halo arrangement is counted against a target list. |
| **C3** — 17–27 at 6.5 km/s; 26–34 at 5 yr | **partly known** | The specific numbers are new; the *sensitivity* is published — [Tyler & Wittig 2021](https://doi.org/10.1016/j.actaastro.2021.03.002) show a 20 % threshold increase raises the ERO count by 50 %. |
| **C4** — interpolated reach tables over-count by ⅓–½ | **partly known** | The phenomenon is documented, the direction and magnitude are not. Tyler & Wittig found a pre-filter that *under*-counted EROs by 30 %; [Murphy 2015](https://doi.org/10.5281/zenodo.32160) tested Shoemaker–Helin Δv approximations against ~1,200 asteroids. No published validation of v∞ reach tables against a direct multi-body solve. |
| **C5** — station phase on the halo worth a factor 2–3 in count | **new** | Halo phase is treated as a variable by [Chen, Kawakatsu & Hanada 2016b](https://doi.org/10.1016/j.actaastro.2016.05.003) and [Qi & de Ruiter 2020](https://doi.org/10.2514/1.g004751), but never propagated to a target count. |
| **C6** — chord scaling, ~512 m/s per half orbit, time-independent | **known, and partly contradicted** | Shape, magnitude class and phase-independence published by [Sato, Kitamura & Shima 2015](https://doi.org/10.2322/tjsass.58.261); even spacing of N craft on a halo by [Chen & Ma 2017](https://doi.org/10.2514/1.g002518). Time-independence contradicted by [Fu, Wang & Zhang 2023](https://doi.org/10.3389/fspas.2023.1177573). |
| **C7** — patched swingby underestimates by median +135 m/s | **new, but an outlier** | No comparable statistic published for libration-point lunar-swingby legs. Every published transition penalty for related problems is far smaller (see §2a). |
| **C8** — mixed-frame indirect term gives ~12.5 m/s per node | **known (as a class) — recommend dropping** | [Jorba-Cuscó, Farrés & Jorba 2018](https://doi.org/10.3389/fams.2018.00032) state that the bicircular problem's primaries "do not obey Newton's laws"; [Rosales, Jorba & Jorba-Cuscó 2023](https://doi.org/10.1007/s10569-023-10129-4) and [Li, Masdemont, Zhu & Gao 2025](https://doi.org/10.1016/j.cnsns.2025.109356), [2026](https://doi.org/10.1016/j.cnsns.2026.110231) build the coherent alternatives for exactly this reason. |
| **C9** — v∞ 1.2–1.46 km/s in 60–200 d, direction limited by the Moon's plane | **known** | [Casalino & Lantoine 2020](https://doi.org/10.1007/s40295-020-00229-w) map escape C₃ against right ascension and declination for double lunar swingbys; their guaranteed-all-directions value and declination ceiling bracket the team's band precisely. |

---

## Priority 1 — overlap

### 1a Retrieval and accessibility counts

The asteroid-retrieval literature counts targets, but it counts a different quantity than the team does, and the
difference is the team's opening. The canonical screen,
[García Yárnoz, Sanchez & McInnes 2013](https://doi.org/10.1007/s10569-013-9495-6), filtered JPL's small-body
database as of 27 July 2012 and found **twelve** "easily retrievable objects" capturable below a 500 m/s total
Δv, with 25 trajectories to periodic orbits near Sun–Earth L2 and six near L1; the cheapest was 58 m/s to move
2006 RH120 onto a southern halo family on 1 February 2021. Three features of that screen matter for positioning.
It models only the **inbound leg**, with no return, no reuse and no cycle cadence. Its transfers are impulsive Lambert
arcs onto a stable hyperbolic manifold, with all burns far from Earth, so there is no Earth-side phase to solve
at all. And it explicitly excludes both the Moon's third-body perturbation and lunar swingbys, which the authors
flag as outside scope. Durations run 2.2–10 years against an arrival window of 2016–2100, with no cycle-time cap.
The team's architecture is therefore not a variant of the ERO problem; it is a different problem that happens to
end at the same orbits.

That line has since been recomputed rather than extended, and the recomputation is the most useful precedent the
team has for C3 and C4. [Tyler & Wittig 2021](https://doi.org/10.1016/j.actaastro.2021.03.002) reproduced the ERO
list with an average improvement of 176.7 m/s (σ = 147.6) and raised the count from 17 to 44, of which 27 are new,
with the cheapest transfer at 13.97 m/s. Their diagnosis is almost entirely about screening artefacts rather than
dynamics. The earlier pre-filter threshold "limits the final number of EROs by 30 %", an epoch constraint in the
original work inflated optimal Δv by roughly 50 m/s, and the Lambert formulation itself goes singular near
180° transfer angles, "an artefact of the definition of the Lambert arc" rather than of the dynamics, so that local
optimisation alone is insufficient. Their remark that "by increasing the threshold by as little as 20 %, the
number of EROs increases by 50 %" is the published form of C3's sensitivity, and the team should cite it rather
than present cap-sensitivity as a discovery. Their validation step also bears on C7: transfers re-converged in
the full CR3BP "differ only on the order of m/s".

The reusable-vehicle architecture itself has recent precedent that the brief does not mention, and a referee will
find it immediately. [Peng, Zhang & Gao 2024](https://doi.org/10.3390/aerospace11070546) set and solved the 12th
China Trajectory Optimization Competition problem: twenty reusable probes making round trips from a service
station in a lunar distant retrograde orbit, reaching **105 potentially hazardous asteroids** inside a ten-year
window, with [Wang et al. 2024](https://doi.org/10.1016/j.cja.2024.09.010) reporting a competing solution. The
architectural similarity (station, reusable fleet, round trips, maximise targets) is close enough to require
explicit differentiation, and the differentiators are real. Those probes perform close *flybys*, not a ≥60-day
stay with mass return; the station is in cislunar rather than Sun–Earth space; and the objective is a tour-design
optimisation rather than a feasibility census against a falsifier.

The broadest accessibility census is [Xie & Dempster 2022](https://doi.org/10.1109/aero53065.2022.9843463), which
screened 24,149 NEAs for low-thrust round-trip missions and found 1,684 — about 7 % — accessible, with 95.4 % of
those requiring propellant mass fractions between 0.08 and 0.29, and accessible targets clustering below 9°
inclination and 0.4 eccentricity. Two things follow. First, a referee will ask why the team's architecture admits
single-digit to mid-teens targets where Xie and Dempster admit 1,684. Their departures
and arrivals are Earth-relative with no node orbit, no halo phase and no lunar-swingby constraint, so the team is
pricing a constraint that survey never imposed. Second, their method is a deep-network surrogate trained on
low-thrust optimisations and embedded in a grid search, a different way of avoiding the interpolation error C4
identifies and the natural comparison for C4's methodology. The same group's follow-up,
[Xie, Saydam & Dempster 2023](https://doi.org/10.1016/j.ast.2023.108304), extends this to supply delivery and
resource transportation with high-power SEP, and [Yu, Shang & Wei 2021](https://doi.org/10.1016/j.ast.2021.106944)
run a comparable accessibility assessment for multi-asteroid tours.

For context the team should cite but need not compete with:
[Brophy, Culick & Friedman 2012](https://doi.org/10.26206/wn0e-vn09) (the Keck study),
[Sanchez, Neves & Urrutxua 2018](https://doi.org/10.3389/fams.2018.00044) (the review that tabulates the endgame
options and their delivery Δv — 170 m/s to a lunar DRO for 2008 HU4 on the ARRM concept, 58 m/s to a Sun–Earth
libration orbit for 2006 RH120, 79 m/s using a lunar gravity assist for 2000 SG344), and
[Elvis et al. 2011](https://doi.org/10.1016/j.pss.2011.05.006) on ultra-low-Δv objects.

**On C4 specifically.** I could not find a published study that validates an interpolated reachability or v∞ reach
table against a direct multi-body solve and reports an over-count fraction. The nearest comparators are Murphy's
assessment of the Shoemaker–Helin Δv approximations, Tyler and Wittig's threshold finding (which runs the other
way), and the accuracy statements attached to modern surrogates;
[Yang, Zhang, Li & Jiang 2025](https://doi.org/10.1109/taes.2025.3567278) build a deep-network map of
three-dimensional lunar gravity assists in the CR3BP precisely because the underlying solve is expensive. C4 is
therefore close to new, and is best framed as a *method* claim, that reach tables credited across a node-and-swingby
phase are optimistic by a stated factor, rather than as a general statement about accessibility surveys.

### 1b Halo departures to a required v∞ vector

The team's departure problem has been posed before, but never swept over many targets with feasibility rates
reported, and the directional physics in C9 is already published in more detail than the claim states.

[Casalino & Lantoine 2020](https://doi.org/10.1007/s40295-020-00229-w) is the paper that settles C9. Working with
double lunar gravity assists and a pre-computed database of Moon-to-Moon transfers in the Sun–Earth CR3BP, they
report that solar-perturbed double-flyby sequences deliver escape C₃ between 2.5 and 3.2 km²/s² for planar
departures, that **"an escape C₃ up to 1.5 km²/s² is guaranteed for any right ascension and declination"**, and
that **"the maximum declination available with an escape … C₃ of 2 km²/s² is ±30 deg"**, with maximum C₃ falling
as declination rises "since a flyby is most effective when the v∞ vector of the spacecraft aligns with the orbital
velocity of the encountered body". Converting the team's band, v∞ = 1.2–1.46 km/s is C₃ = 1.44–2.13 km²/s², exactly the interval between
Casalino and Lantoine's all-directions guarantee and their ±30° ceiling. C9 is not
a new result; it is a rediscovery of their Figure 7, and the team should cite it and say so. Two caveats preserve
some ground: their geocentric phase begins at a launch perigee, not a halo orbit, and their CR3BP database places
the Moon in the ecliptic, neglecting the 5.1° inclination the team models explicitly. The direction limit the team
attributes to the Moon's plane is, in Casalino and Lantoine's model, a consequence of flyby geometry in a *planar*
Moon, so the team's inclined, regressing-node treatment is a genuine refinement and is where the novelty in C9
actually sits.

The two titles the brief lists as unread resolve from that paper's own reference list:
**Landau, D., McElrath, T. P., Grebow, D. & Strange, N., "Efficient Lunar Gravity Assists for Solar Electric
Propulsion Missions", AAS 12-165, *Advances in the Astronautical Sciences* vol. 143 (2012)**, and
**Lantoine, G. & McElrath, T. P., "Families of Solar-Perturbed Moon-to-Moon Transfers", AAS 14-233 (2014)**. Both
are AAS conference papers in the McElrath–Lantoine–Landau–Strange line the team already cites via GLEX-2012, and
the second is the direct antecedent of Casalino and Lantoine's Sun-perturbed Moon-to-Moon database. Neither is
indexed in OpenAlex or reachable from this sandbox; I have them as citations within a paper I read in full, not
as papers I read.

The active frontier here is a Chinese-led effort to systematise exactly the escape search the team performs by
brute force. [Fu et al. 2026](https://doi.org/10.2514/1.g009571) introduce an "energy transition domain" for
constructing gravity-assist escape trajectories, [Liu, Fu, Wu & Gong 2026](https://doi.org/10.1016/j.ast.2026.112274)
give a dynamical search strategy for lunar-gravity-assist escapes, and
[Shen et al. 2026](https://doi.org/10.1007/s11433-025-2836-7) review escape, capture and transfer design via
multiple gravity assists. [Mascolo & Casalino 2022](https://doi.org/10.3390/aerospace9040186) solve the
complementary problem — optimal *low-thrust* escape directly from Sun–Earth and Earth–Moon L2 in a four-body
JPL-ephemeris model with solar radiation pressure, including escapes toward near-Earth asteroids — which is the
natural control case for the team's result: it is the same departure point without the lunar swingby. None of
these poses the fixed-phase, fixed-date, specified-v∞-vector problem with a feasibility rate, which is where the
team's contribution lies.

### 1c Phasing along libration-point orbits

**This is where the brief's claim list is weakest, and the team should read the three papers below before writing
anything.** C6 is not new. Its shape, its phase-independence, and its order of magnitude were published in 2015,
and the manifold alternative the brief calls the team's "open next step" was published in the same paper with a
quantified saving.

[Sato, Kitamura & Shima 2015](https://doi.org/10.2322/tjsass.58.261) solve rendezvous between two spacecraft on a
common Earth–Moon L2 halo orbit (amplitudes 12,320 / 35,518 / 12,069 km, period 14.8064 d) by two methods. Their
"Method 1" is phasing along the orbit, and its cost against initial phase difference ψ is 61.2 m/s at 20°,
180.0 m/s at 60°, 331.2 m/s at 120° and 397.0 m/s at 180°, rising monotonically to a maximum at 180° and then
decreasing symmetrically toward 350°, and — critically for C6 — "almost independent of the initial phase φ". That
is the chord law, measured seven years before C6 was formulated: a curve that peaks at half an orbit, is
symmetric about it, and does not care where on the orbit you start. The figure below overlays the team's claimed
values on Sato's, with a chord law normalised to the team's own 512 m/s half-orbit figure.

> *Figure not archived (it was made in the reviewer's session). Its caption:* Phasing cost against phase shift around a halo orbit. Project Dyson's C6 values (Sun–Earth halo, Az ≈ 1.2 × 10⁵ km) track a chord law of 512 m/s × sin(Δφ/2). Sato, Kitamura & Shima's measured Earth–Moon L2 values follow the same shape at roughly 0.8× the magnitude, and their manifold detour cuts the half-orbit cost by a factor of 3.2. Chen & Ma's four-spacecraft deployment sits an order of magnitude lower on a much smaller halo. Lower is better.

Their "Method 2" is the manifold detour: the chaser leaves the halo on its unstable manifold, passes near the Moon
through a homoclinic intersection, and returns on the stable manifold, with the arrival time adjusted en route.
At ψ = 180° it costs **122.4 m/s against Method 1's 397.0 m/s**, a factor of 3.2, in 36.3 days (2.45 orbital
periods), with no single burn exceeding 4 m/s across 61 manoeuvres. The crossover is at ψ ≈ 70°: below it,
direct phasing wins; above it, the manifold route wins, and total cost stays under about 220 m/s for any phase
difference. The team's planned next step therefore has a published answer in the Earth–Moon case, including the
expected magnitude of the saving and the phase angle at which it starts paying.

[Chen & Ma 2017](https://doi.org/10.2514/1.g002518) solve the team's multi-station problem directly, deploying
several spacecraft evenly spaced around a halo orbit, for four CubeSats at 90° spacing on an Earth–Moon L2 halo
with Az = 15,000 km, at 55, 99, 101 and 42 m/s, a maximum of 101 m/s per vehicle and roughly 100 m/s total. They
compare three mechanisms: phasing around the orbit, touring the Moon, and manifold-plus-symmetric-connection
trajectories. [Qi & de Ruiter 2020](https://doi.org/10.2514/1.g004751) invert the question, mapping the phase
change *achievable* from a given impulse budget on short-range halo phasing orbits, and examining how the start
and end points on the halo change it, which is C5's mechanism, published.

Two further results bound the picture. [Bucchioni et al. 2022](https://doi.org/10.1016/j.asr.2022.10.036) compare
phasing strategies for Earth–Moon NRHOs against a 100 m/s design ceiling set with CNES: a direct two-impulse
transfer costs 4–100 m/s over 1–3.28 days but recovers only a limited phase, a halo-family parking strategy admits
no solution below 45 m/s, and a butterfly-orbit parking strategy costs 300–800 m/s with a 17.45-day minimum wait.
[Down, Majji & Howell 2026](https://doi.org/10.2514/1.g009468) formulate low-thrust rephasing on quasi-periodic
invariant tori and prove that staying on the torus while thrusting is infeasible for a large class of mechanical
systems — This matters if the team's parked-and-phased option is ever flown with electric propulsion rather than
impulses. They report no scaling law against phase-shift magnitude, so C6's functional form remains un-generalised
in the low-thrust case.

**The time-independence half of C6 is contested.** [Fu, Wang & Zhang 2023](https://doi.org/10.3389/fspas.2023.1177573)
find for two-impulse phasing on a 2:1 lunar-synodic-resonant DRO that "the required Δv decreases with the
increasing time of flight of phasing", with concrete numbers: a 30° phase change costs 67.1 m/s at the baseline
time of flight but 16.1 m/s when one extra orbital period is allowed, and a 20° change falls from 53.3 to 14.7 m/s.
Their saturation point is later than the team's: "the decreasing trend of the phasing pulse slows down with an
increase in the TOF when the TOF is larger than 1.5 orbit period", whereas C6 reports insensitivity beyond about
120 days, which is roughly 0.67 of a Sun–Earth halo period. Either the team's multiple-shooting phasing solutions
are time-bounded in a way that masks the remaining improvement, or Sun–Earth halo phasing genuinely saturates
earlier than cislunar phasing does. Sato's data hints at the former: their Method 1 total time "reaches its upper
bound … around ψ = 180 deg", i.e. the large-phase cases are the ones pressed against the time constraint. This is
worth re-checking before C6 is asserted in print.

**Recommendation.** Drop C6 as a claim of discovery. Re-pose it as a *calibration*: the chord law holds for a
Sun–Earth halo of Az ≈ 1.2 × 10⁵ km with a coefficient of ~512 m/s per half orbit, which places the Sun–Earth
case relative to the published Earth–Moon values. The ratio between systems is itself the
interesting number, since Sato's Earth–Moon L2 halo peaks at 397 m/s and Chen and Ma's smaller one at ~100 m/s.
Then pursue the manifold detour, citing Sato's 3.2× as the expectation to beat.

---

## Priority 2 — the Moon's gravity on patched swingby legs

### 2a Patched versus full-force penalties (C7)

No published study reports the statistic C7 reports: a distribution of deterministic correction cost incurred
when patched lunar-swingby legs from a libration-point orbit are re-flown with the Moon's gravity throughout. In
that narrow sense C7 is new. The problem is that every published transition penalty for an adjacent problem is one
to two orders of magnitude smaller, and the team will have to explain the gap rather than assert the number.

The comparisons a referee will reach for: Tyler and Wittig's ERO transfers re-converged in the full CR3BP "differ
only on the order of m/s"; Fu, Wang and Zhang's DRO phasing rises from 12.56 m/s in the CR3BP to 13.64 m/s in an
ephemeris model, about 8 %, and they note the total "did not increase significantly"; and Casalino and Lantoine's
approximate double-LGA solution, re-optimised in a four-body DE405 model with an eighth-degree Earth potential and
solar radiation pressure, changed theoretical escape mass by 28 kg out of 9,664 kg, requiring a "slightly smaller
launch C₃". Their solar-perturbed numerical case needed its launch moved from mid-February to late December 2021
to accommodate phasing loops, a schedule penalty rather than a Δv one.

The team's own attribution is both the explanation and the defence: the cost accrues over the months the vehicle
spends near the Moon's orbital radius *before* the swingby, not at the swingby. That is consistent with Casalino
and Lantoine's framing, "solar perturbation is relevant during longer Moon-to-Moon transfers", and it is the
reason their short 41-day analytical cases transition almost for free while the team's 60–200-day legs do not. The
paper should make this the claim: *the patched-swingby approximation is cheap for short geocentric phases and
expensive for long Sun-perturbed ones, with the penalty scaling with time spent near lunar distance, and here is
the distribution over 1,816 legs.* Framed that way, +135 m/s median with quartiles at 70 and 222 is a contribution
rather than an outlier. Framed as "patched swingbys cost 135 m/s", it reads as a modelling error.

I did not find a published statistical treatment of this penalty for libration-point departures, and I searched
for one specifically (terms in §Gaps). The closest systematic treatment of patched-to-multi-body transition is
[Zhang, Yu & Dai 2022](https://doi.org/10.32604/cmes.2022.022585), a review of Earth–Moon transfer modelling and
design that walks the fidelity ladder.

### 2b The frame convention, and whether C8 is textbook (it is)

Placing the Sun–Earth CR3BP secondary at the Earth–Moon barycentre with Earth and Moon either side of it is the
standard bicircular construction, and the literature states both the convention and its defect explicitly.
[Jorba-Cuscó, Farrés & Jorba 2018](https://doi.org/10.3389/fams.2018.00032) set out the mirror-image construction
for the Earth–Moon-centred case, with Earth and Moon on a circular orbit about their barycentre CEM and Sun and CEM
on a further circular orbit about CSEM, and then say plainly that **"the BCP is not coherent, that is, the
trajectories followed by the primaries do not obey Newton's laws"**, calling this "a remarkable shortcoming".
They also establish what the defect is *not*. The bicircular problem remains "a
Hamiltonian system with three and a half degrees of freedom", and its solar perturbation has size
O(mS/aS³) ≈ 0.0056. They quantify no drift attributable to incoherence, and they treat only the Earth–Moon system;
Sun–Earth L1/L2 is not discussed.

The coherent alternatives exist precisely because of this. The quasi-bicircular problem imposes a genuine
three-body solution on the primaries, with invariant manifolds near L1 and L2 computed by
[Rosales, Jorba & Jorba-Cuscó 2023](https://doi.org/10.1007/s10569-023-10129-4), and
[Li, Masdemont, Zhu & Gao](https://doi.org/10.1016/j.cnsns.2025.109356) have built Sun–Earth heteroclinics in
restricted four-body non-autonomous models and then, in [2026](https://doi.org/10.1016/j.cnsns.2026.110231), a
framework whose title is literally *Consistent four-body invariant-manifold framework* for Earth–Moon to Sun–Earth
low-energy heteroclinics. A referee seeing C8 will point at these and ask why a known inconsistency needed
rediscovering.

**Recommendation.** Withdraw C8 as a claim. Keep the 12.5 m/s per node as a one-line methods note, along the lines of "mixing a
fixed-Earth direct term with a barycentric indirect term produces a spurious ~12.5 m/s per node, consistent with
the known non-coherence of bicircular models [cite Jorba-Cuscó 2018]; we therefore use the consistent construction
of [Li et al. 2026]", and cite the coherent-model line for the construction actually used. The team should also
check its own model against the quasi-bicircular formulation, because a referee from the Barcelona or Masdemont
school will ask.

### 2c Correction budgets for lunar-swingby legs

Flown TCM budgets for this trajectory class are very small, and the team needs to say clearly that its 135 m/s is
a *deterministic model-transition* cost rather than a navigation budget, or the comparison will look damning.

[Folta, Woodard, Howell, Patterson & Schlei 2011](https://doi.org/10.1016/j.actaastro.2011.11.007) give the
ARTEMIS numbers in detail. The mission allocated 4 % of total propellant to trajectory-correction manoeuvres. On
P1, the deep-space manoeuvre was 7.30 m/s and the four subsequent TCMs were 0.18, 0.18, 0.66 and 1.90 m/s; on P2,
a lunar-flyby correction of 0.65 m/s was followed by deep-space manoeuvres of 3.68, 24.25 and 1.63 m/s and TCMs
of 2.22 and 0.64 m/s. Navigation solutions were generated every three days from three-hour contacts every other
day; realised manoeuvre errors were of order 0.4–11 cm/s. Manoeuvre spacing on P1 ran 29–61 days, and the double
gravity assist had a 13-day interval between lunar encounters. The paper quantifies no Δv penalty for moving from
the lower-fidelity circular model to the full DE405 ephemeris with an eighth-degree Earth field and solar
radiation pressure; it simply designs in both and transitions.

Against ARTEMIS, then, a deterministic 135 m/s per leg is roughly five times the largest single deep-space manoeuvre
flown and two orders of magnitude above the statistical TCMs. The team's cadence of 5–10 burns per leg at 10-day
spacing is, by contrast, *tighter* than ARTEMIS's 29–61 days, which is defensible given a 60–200-day Sun-perturbed
leg but should be justified. [Ozaki et al. 2022](https://doi.org/10.1016/j.actaastro.2022.03.029) on DESTINY+ is
the right modern comparison for a low-thrust vehicle spiralling out through lunar gravity assists; I have it as
metadata and abstract only.

I was not able to reach NTRS or the JHU APL Technical Digest from this sandbox, so the WIND, STEREO and Geotail
budgets are identified but not quantified: **Dunham, Guzmán & Sharer, "STEREO Trajectory and Maneuver Design",
*Johns Hopkins APL Technical Digest* 28(2):104–125 (2009)** and **Uesugi, Kawaguchi, Ishii & Ishii, "Design of
double lunar swingby orbits for Muses-A and Geotail" (1989)**, with NASA technical reports on the Geotail launch
window and first-lunar-encounter correction strategy from 1989–1990. These are the right sources for
double-lunar-swingby correction practice and should be obtained directly.

---

## Priority 3 — consensus inputs

### 3a Capture of a loaded tug back to a Sun–Earth halo

The mirror-image assumption is untested in the literature as the team poses it, but the capture side has been
designed for payloads rather than vehicles.
[Tan, Zhang & Li 2023](https://doi.org/10.1016/j.asr.2023.03.034) address long-term capture of asteroids to
Sun–Earth L1/L2 using a lunar flyby plus station-keeping manoeuvres, following
[Tan, Shen & Ma 2022](https://doi.org/10.1016/j.actaastro.2022.05.059) on the energy structure of Sun–Earth stable
manifolds reached with a lunar flyby, and [Tan, Zhang & Wang 2021](https://doi.org/10.1016/j.actaastro.2021.08.041)
on capture to Sun–Earth distant retrograde orbits. This is the closest published work to the team's inbound leg
and the team does not cite it; I have all three as metadata only, since none is open access and none returned an
abstract. [Nakamiya, Scheeres, Yamakawa & Yoshikawa 2008](https://doi.org/10.2514/1.33796) analyse capture
trajectories into periodic orbits about libration points, which is the general form of the arrival problem, and
[Howell & Kakoi 2006](https://doi.org/10.1016/j.actaastro.2006.02.010) treat transfers between the Earth–Moon and
Sun–Earth systems using manifolds and transit orbits.

What none of these do is capture a *vehicle* arriving with v∞ ≈ 1–1.5 km/s and a mass payload under low thrust,
nor test whether the escape solution time-reverses. The asymmetries a referee will raise are concrete. The Sun's
direction relative to the halo is not time-symmetric over a multi-year cycle, the Moon's node has regressed
between departure and return, and the vehicle's mass differs by the payload. The team should treat the mirror
assumption as a stated limitation with a bounded check on a few legs, not as a result.

### 3b Waiting for a lunar encounter

This is substantially answered, by the paper missing from the brief's source list.
[Chen, Kawakatsu & Hanada 2016b](https://doi.org/10.1016/j.actaastro.2016.05.003) solve the minimum phasing Δv to
reach the Moon from a Sun–Earth halo orbit *for every initial lunar phase*, motivated by ISEE-3-style extended
missions, and note that "most previous studies present the orbit-to-orbit transfers where the lunar phase is not
considered". Their headline numbers: the Δv required to cover all initial lunar phases is **about 45 m/s for a halo
with Az greater than 3.5 × 10⁵ km, and 14 m/s for a small halo with Az = 1 × 10⁵ km**, the latter being within
20 % of the team's node orbit amplitude. They also discuss phasing planning and "the shift of lunar phase with halo
orbit revolution", which is exactly the encounter-recurrence question 3b asks. A methodological point of theirs is
worth absorbing too: a general constrained optimiser "that does not identify multiple feasible solutions is shown
to miss minima", and they build a two-step differential corrector with a two-body Lambert solver to recover both
short-way and long-way branches.

The tension with C6 is the thing to resolve before writing. Chen, Kawakatsu and Hanada price *access to any lunar
phase* from a comparable Sun–Earth halo at 14 m/s; the team prices *relocation around the halo* at 185–512 m/s.
These are not the same manoeuvre, since theirs adjusts the departure to meet the Moon while the team's moves a station, but
in an architecture whose purpose is to catch lunar encounters, the cheaper manoeuvre may make the expensive one
unnecessary. If a tug can buy any lunar phase for tens of m/s by adjusting its departure, the multi-station and
parked-and-phased arrangements in C2 may be solving a problem that does not need solving, and the target counts
could change. **This should be checked before the paper is framed around station arrangements.**

---

## Disagreements worth reporting side by side

**Phasing cost magnitude on a halo.** Sato, Kitamura & Shima report 397 m/s to move half-way round an Earth–Moon L2
halo of ~12,000–36,000 km amplitude; Chen & Ma report ~100 m/s to space four craft 90° apart on an Earth–Moon L2
halo of Az = 15,000 km; the team reports 350 m/s for 90° on a Sun–Earth halo of Az ≈ 1.2 × 10⁵ km. The spread is
explained by system, amplitude and manoeuvre strategy rather than by disagreement, but the paper must state which
of the three it is comparing against, because the numbers differ by a factor of three at the same phase angle.

**Does waiting help?** The team says cost is independent of transfer time beyond ~120 days. Fu, Wang & Zhang find
cost falls substantially with time of flight on a DRO and only stops improving past 1.5 orbital periods; Down,
Majji & Howell find the low-thrust torus-rephasing cost monotonically decreasing out to their time-window
boundary for one of their two formulations and multi-minimum for the other. Sato's time-to-bound behaviour at
large phase differences suggests the team's finding may be an artefact of a bounded time horizon.

**Model-transition penalty.** The team: median +135 m/s per leg. Tyler & Wittig: order of m/s for heliocentric
retrieval transfers. Fu, Wang & Zhang: ~1 m/s, 8 %, CR3BP to ephemeris for DRO phasing. Casalino & Lantoine:
28 kg of 9,664 kg mass, no Δv penalty quoted, for a 41-day geocentric phase. The assumption that separates them is
leg duration near lunar distance: the team's 60–200 days against Casalino and Lantoine's 41 days.

**ERO counts.** García Yárnoz, Sanchez & McInnes: 12 objects below 500 m/s from ~2012 data. Sanchez & García Yárnoz
(per their 2018 review): 17 low-thrust solutions. Tyler & Wittig: 44, of which 27 new, with one previously listed
object (2011 BL45) not recoverable below 617 m/s. The disagreement is about pre-filter thresholds, epoch
constraints and global-versus-local optimisation, not about dynamics.

---

## Gaps — searched and not found

Databases reachable from this environment: OpenAlex (full works index including AAS, AIAA, IAC and NTRS records),
arXiv, Crossref, Unpaywall, J-STAGE and publisher open-access PDFs via DOI resolution, plus general web search.
**NASA ADS (adsabs.harvard.edu), NTRS (ntrs.nasa.gov) and the AIAA ARC and AAS proceedings portals were not
reachable**, so AAS and ISSFD conference papers are identified by citation rather than read; the two titles in §1b
and the STEREO and Geotail papers in §2c are the material cases.

Searches that returned nothing relevant:

- *Over-counting of interpolated reachability tables.* "near-Earth asteroid accessibility map delta-v
  Shoemaker-Helin approximation accuracy", "low-thrust many-revolution trajectory optimization asteroid
  reachability map interpolation", "validation accessibility survey against full optimisation". Nothing that
  validates a v∞ reach table against a direct multi-body solve and reports an error fraction. **C4 is a real gap.**
- *Target-count sensitivity to station phase on a libration-point orbit.* "halo orbit phase station location
  target accessibility", "libration point station phase dependence mission capability". Nothing. **C5 is a real gap.**
- *Deterministic patched-to-full-model penalty statistics for libration-point lunar-swingby legs.* "patched conic
  lunar gravity assist accuracy full ephemeris comparison", "patched conic lunar flyby error correction cost",
  "initial guess patched conics differential correction cost m/s". Only qualitative fidelity-ladder discussions.
  **C7's statistic is a real gap.**
- *Capture of a loaded low-thrust vehicle to a Sun–Earth halo from v∞ 1–1.5 km/s.* "halo orbit insertion from
  hyperbolic approach lunar gravity assist capture", "low-thrust capture into halo orbit asteroid sample return",
  "ballistic capture libration point orbit stable manifold Earth arrival". Asteroid-payload capture is covered
  (Tan et al.); vehicle capture with return mass is not. **3a is a real gap.**
- *Round-trip cycle cadence for a reusable tug through a libration-point node.* "reusable space tug solar electric
  propulsion cislunar logistics fleet sizing", "asteroid mining logistics reusable spacecraft propellant",
  "round-trip mission near-Earth asteroid delta-v trip time survey targets". The counting studies are either
  one-way (ERO line), Earth-departing (Xie & Dempster), or cislunar-flyby (Peng et al.). **C1 and C2 are real gaps.**
- *Lunar-encounter recurrence from a Sun–Earth halo* returned exactly one directly relevant paper
  (Chen, Kawakatsu & Hanada 2016b), which is why 3b is largely answered rather than open.

---

## References

Read level: **F** = read in full from retrieved text; **A** = abstract read; **M** = metadata only, meaning authors, venue and
title resolved against OpenAlex but content not read; **S** = cited secondhand from a paper read in full.

| Authors | Year | Title | Venue | DOI / ref | Read |
|---|---|---|---|---|---|
| Brophy, Culick & Friedman | 2012 | Asteroid Retrieval Feasibility Study | Keck Institute for Space Studies | [10.26206/wn0e-vn09](https://doi.org/10.26206/wn0e-vn09) | M |
| Bucchioni, Lizy-Destrez, Vaujour, Thoraval, Rouverand & Silva | 2022 | Phasing with near rectilinear Halo orbits: Design and comparison | Adv. Space Res. 71:2449–2466 | [10.1016/j.asr.2022.10.036](https://doi.org/10.1016/j.asr.2022.10.036) | F |
| Capdevila & Howell | 2018 | A transfer network linking Earth, Moon, and the triangular libration point regions | Adv. Space Res. 62:1826–1852 | [10.1016/j.asr.2018.06.045](https://doi.org/10.1016/j.asr.2018.06.045) | M |
| Casalino & Lantoine | 2020 | Design of Lunar-Gravity-Assisted Escape Trajectories | J. Astronaut. Sci. 67:1374–1390 | [10.1007/s40295-020-00229-w](https://doi.org/10.1007/s40295-020-00229-w) | F |
| Chen | 2023 | Capacity of Sun-driven lunar swingby sequences and their application in asteroid retrieval | Astrodynamics 7:315–334 | [10.1007/s42064-023-0161-9](https://doi.org/10.1007/s42064-023-0161-9) | M (team holds) |
| Chen, Kawakatsu & Hanada | 2016a | Earth Escape from a Sun-Earth Halo Orbit using Unstable Manifold and Lunar Swingbys | Trans. JSASS 59:269–277 | [10.2322/tjsass.59.269](https://doi.org/10.2322/tjsass.59.269) | M (team holds) |
| **Chen, Kawakatsu & Hanada** | **2016b** | **Phasing Delta-V for transfers from Sun–Earth halo orbits to the Moon** | **Acta Astronaut. 127:464–473** | [10.1016/j.actaastro.2016.05.003](https://doi.org/10.1016/j.actaastro.2016.05.003) | **A** |
| **Chen & Ma** | **2017** | **Phasing Trajectories to Deploy a Constellation in a Halo Orbit** | **J. Guid. Control Dyn. 40:2662–2667** | [10.2514/1.g002518](https://doi.org/10.2514/1.g002518) | **A** |
| Down, Majji & Howell | 2026 | On-Manifold Low-Thrust Rephasing of Quasi-Periodic Orbits | J. Guid. Control Dyn. 49:1300–1316 | [10.2514/1.g009468](https://doi.org/10.2514/1.g009468) | F |
| Elvis, McDowell, Hoffman & Binzel | 2011 | Ultra-low delta-v objects and the human exploration of asteroids | Planet. Space Sci. 59:1408–1412 | [10.1016/j.pss.2011.05.006](https://doi.org/10.1016/j.pss.2011.05.006) | M |
| Folta, Woodard, Howell, Patterson & Schlei | 2011 | Applications of multi-body dynamical environments: The ARTEMIS transfer trajectory design | Acta Astronaut. 73:237–249 | [10.1016/j.actaastro.2011.11.007](https://doi.org/10.1016/j.actaastro.2011.11.007) | F |
| Fu, Liu, Wu, Shi & Gong | 2026 | Energy Transition Domain and Its Application in Constructing Gravity-Assist Escape Trajectories | J. Guid. Control Dyn. 49:1514–1522 | [10.2514/1.g009571](https://doi.org/10.2514/1.g009571) | M |
| **Fu, Wang & Zhang** | **2023** | **Phasing analysis on DRO with impulsive maneuver** | **Front. Astron. Space Sci. 10:1177573** | [10.3389/fspas.2023.1177573](https://doi.org/10.3389/fspas.2023.1177573) | **F** |
| García Yárnoz, Sanchez & McInnes | 2013 | Easily retrievable objects among the NEO population | Celest. Mech. Dyn. Astron. 116:367–388 | [10.1007/s10569-013-9495-6](https://doi.org/10.1007/s10569-013-9495-6) | F |
| Howell & Kakoi | 2006 | Transfers between the Earth–Moon and Sun–Earth systems using manifolds and transit orbits | Acta Astronaut. 59:367–380 | [10.1016/j.actaastro.2006.02.010](https://doi.org/10.1016/j.actaastro.2006.02.010) | M |
| **Jorba-Cuscó, Farrés & Jorba** | **2018** | **Two Periodic Models for the Earth-Moon System** | **Front. Appl. Math. Stat. 4:32** | [10.3389/fams.2018.00032](https://doi.org/10.3389/fams.2018.00032) | **F** |
| Landau, Dankanich, Strange, Bellerose, Llanos & Tantardini | 2013 | Trajectories to Nab a NEA | AAS 13-409 | — | M (team holds) |
| Landau, McElrath, Grebow & Strange | 2012 | Efficient Lunar Gravity Assists for Solar Electric Propulsion Missions | AAS 12-165, Adv. Astronaut. Sci. 143 | — | S |
| Lantoine & McElrath | 2014 | Families of Solar-Perturbed Moon-to-Moon Transfers | AAS 14-233 | — | S |
| Li, Masdemont, Zhu & Gao | 2025 | The Sun-Earth heteroclinics in restricted four-body non-autonomous models | Commun. Nonlinear Sci. Numer. Simul. 152:109356 | [10.1016/j.cnsns.2025.109356](https://doi.org/10.1016/j.cnsns.2025.109356) | M |
| Li, Masdemont, Zhu & Gao | 2026 | Consistent four-body invariant-manifold framework for designing Earth–Moon to Sun–Earth low-energy heteroclinics | Commun. Nonlinear Sci. Numer. Simul. 162:110231 | [10.1016/j.cnsns.2026.110231](https://doi.org/10.1016/j.cnsns.2026.110231) | M |
| Liu, Fu, Wu & Gong | 2026 | Search strategy for lunar gravity assist escape trajectories based on dynamical analysis | Aerosp. Sci. Technol. 177:112274 | [10.1016/j.ast.2026.112274](https://doi.org/10.1016/j.ast.2026.112274) | M |
| Lizy-Destrez, Beauregard, Blazquez, Campolo, Manglativi & Quet | 2019 | Rendezvous Strategies in the Vicinity of Earth-Moon Lagrangian Points | Front. Astron. Space Sci. 5:45 | [10.3389/fspas.2018.00045](https://doi.org/10.3389/fspas.2018.00045) | M |
| Mascolo & Casalino | 2022 | Optimal Escape from Sun-Earth and Earth-Moon L2 with Electric Propulsion | Aerospace 9:186 | [10.3390/aerospace9040186](https://doi.org/10.3390/aerospace9040186) | A |
| Murphy | 2015 | Delta-v to Near-Earth Asteroids: An Examination of the Shoemaker-Helin Equations | Zenodo | [10.5281/zenodo.32160](https://doi.org/10.5281/zenodo.32160) | A |
| Nakamiya, Scheeres, Yamakawa & Yoshikawa | 2008 | Analysis of Capture Trajectories into Periodic Orbits About Libration Points | J. Guid. Control Dyn. 31:1344–1351 | [10.2514/1.33796](https://doi.org/10.2514/1.33796) | M |
| Ozaki, Yamamoto, Gonzalez-Franquesa, Gutierrez-Ramon et al. | 2022 | Mission design of DESTINY+: Toward active asteroid (3200) Phaethon and multiple flyby of asteroids | Acta Astronaut. 196:42–56 | [10.1016/j.actaastro.2022.03.029](https://doi.org/10.1016/j.actaastro.2022.03.029) | M |
| **Peng, Zhang & Gao** | **2024** | **Trajectory Design of Potentially Hazardous Asteroid Exploration with Reusable Probes from Cislunar Space** | **Aerospace 11:546** | [10.3390/aerospace11070546](https://doi.org/10.3390/aerospace11070546) | **A** |
| Qi & de Ruiter | 2020 | Achievable Halo Phasing with Short-Range Trajectories | J. Guid. Control Dyn. 43:928–938 | [10.2514/1.g004751](https://doi.org/10.2514/1.g004751) | A (partial) |
| Rosales, Jorba & Jorba-Cuscó | 2023 | Invariant manifolds near L1 and L2 in the quasi-bicircular problem | Celest. Mech. Dyn. Astron. 135:15 | [10.1007/s10569-023-10129-4](https://doi.org/10.1007/s10569-023-10129-4) | M |
| Sanchez & García Yárnoz | 2016 | Asteroid retrieval missions enabled by invariant manifold dynamics | Acta Astronaut. 127:667–677 | [10.1016/j.actaastro.2016.05.034](https://doi.org/10.1016/j.actaastro.2016.05.034) | M |
| Sanchez, Neves & Urrutxua | 2018 | Trajectory Design for Asteroid Retrieval Missions: A Short Review | Front. Appl. Math. Stat. 4:44 | [10.3389/fams.2018.00044](https://doi.org/10.3389/fams.2018.00044) | F |
| **Sato, Kitamura & Shima** | **2015** | **Spacecraft Rendezvous Utilizing Invariant Manifolds for a Halo Orbit** | **Trans. JSASS 58:261–269** | [10.2322/tjsass.58.261](https://doi.org/10.2322/tjsass.58.261) | **F** |
| Shen, Qian, Li, Chen & Liu | 2026 | Deep space trajectory design using multiple gravity assists: A review of escape, capture, transfer | Sci. China Phys. Mech. Astron. 69:234501 | [10.1007/s11433-025-2836-7](https://doi.org/10.1007/s11433-025-2836-7) | M |
| Tan, Zhang & Wang | 2021 | Strategies to capture asteroids to distant retrograde orbits in the Sun–Earth system | Acta Astronaut. 189:181–195 | [10.1016/j.actaastro.2021.08.041](https://doi.org/10.1016/j.actaastro.2021.08.041) | M |
| Tan, Shen & Ma | 2022 | Energy analysis of Sun-Earth stable manifolds with a lunar flyby and with application to capture | Acta Astronaut. 198:87–99 | [10.1016/j.actaastro.2022.05.059](https://doi.org/10.1016/j.actaastro.2022.05.059) | M |
| **Tan, Zhang & Li** | **2023** | **Long-term capture of asteroids to the Sun-Earth L1/L2 using a lunar flyby and station-keeping maneuvers** | **Adv. Space Res. 72:270–283** | [10.1016/j.asr.2023.03.034](https://doi.org/10.1016/j.asr.2023.03.034) | **M** |
| Tamakoshi & Kojima | 2018 | Set-oriented design of interplanetary low-thrust trajectories using Earth Gravity Assist | Acta Astronaut. 156:208–218 | [10.1016/j.actaastro.2018.10.012](https://doi.org/10.1016/j.actaastro.2018.10.012) | M |
| **Tyler & Wittig** | **2021** | **On asteroid retrieval missions enabled by invariant manifold dynamics** | **Acta Astronaut. 183:43–51** | [10.1016/j.actaastro.2021.03.002](https://doi.org/10.1016/j.actaastro.2021.03.002) | **F** |
| Wang, Wang, Dong, Zhao, Jing, Li, Yu & Zheng | 2024 | Trajectory optimization of near-Earth asteroids exploration by using reusable probes from cislunar space | Chin. J. Aeronaut. 38:103234 | [10.1016/j.cja.2024.09.010](https://doi.org/10.1016/j.cja.2024.09.010) | M |
| **Xie & Dempster** | **2022** | **A Survey of Near-Earth Asteroids for Low-Thrust Round-Trip Missions** | **IEEE Aerospace Conf., 1–11** | [10.1109/aero53065.2022.9843463](https://doi.org/10.1109/aero53065.2022.9843463) | **A** |
| Xie, Saydam & Dempster | 2023 | Low-thrust trajectory design for near-Earth asteroid supply delivery and resource transportation | Aerosp. Sci. Technol. 137:108304 | [10.1016/j.ast.2023.108304](https://doi.org/10.1016/j.ast.2023.108304) | M |
| Yang, Zhang, Li & Jiang | 2025 | Deep Neural Networks-Based Efficient Mapping of Three-Dimensional Lunar Gravity Assist | IEEE Trans. Aerosp. Electron. Syst. 61:10768–10783 | [10.1109/taes.2025.3567278](https://doi.org/10.1109/taes.2025.3567278) | M |
| Yu, Shang & Wei | 2021 | Accessibility assessment and trajectory design for multiple Near-Earth-asteroids exploration | Aerosp. Sci. Technol. 118:106944 | [10.1016/j.ast.2021.106944](https://doi.org/10.1016/j.ast.2021.106944) | M |
| Zhang, Yu & Dai | 2022 | Overview of Earth-Moon Transfer Trajectory Modeling and Design | Comput. Model. Eng. Sci. 135:5–43 | [10.32604/cmes.2022.022585](https://doi.org/10.32604/cmes.2022.022585) | M |
| Dunham, Guzmán & Sharer | 2009 | STEREO Trajectory and Maneuver Design | JHU APL Tech. Digest 28:104–125 | not retrieved | M |
| Uesugi, Kawaguchi, Ishii & Ishii | 1989 | Design of double lunar swingby orbits for Muses-A and Geotail | conference paper, 319–331 | not retrieved | M |

Bold rows are the papers the brief's source list does not contain and that a referee would expect to see cited.

