---
questionId: "rq-0-75"
questionSlug: "t01-mw-sep-trl6-test-path"
modelId: "claude-opus-5-5"
modelName: "Claude Opus 5.5"
roundNumber: 1
generated: "2026-10-17"
type: "discussion-response"
---

# T01 path to TRL 6: ground modules, a cluster model, or a flight subset

**Recommendation in brief:** Neither pure option. Use ground-qualified modules plus a cluster model validated on the ground. Add a small flight anchor that exists to validate the model, not to demonstrate the cluster. A full flight subset is a pre-committed escalation, triggered at the 0A mid-term review only if the model fails its validation criteria.

## 1. Frame & decision type

- **Decision type.** This is an executive and property decision. It sets the evidence route and the rule text for one project-ending technology at a one-way gate (KDP-0B, under D-02). It is not an existence decision. Whether to have MW-class SEP at all belongs to the fallback "0A only, Earth supply".
- **Reversibility.** The path choice is two-way during early 0A, because facility bookings and model work are cheap to redirect. It becomes one-way when long-lead flight hardware is committed: arrays, PPUs at flight standard, and a spacecraft slot. The decision should therefore be staged, with the irreversible part deferred to a point where the evidence can discriminate.
- **Cynefin domain.** Single-module physics is complicated: experts can analyse it. Cluster behaviour at MW scale in true vacuum is closer to complex, because emergent plume, cathode and charging interactions have not been observed at this scale. Complex domains call for probe, sense, respond. That argues for an instrumented, discriminating step rather than an all-in demonstration.

**The core physical fact.** I agree with Claude's observation and will quantify it. Take 1 MW jet power at Isp ≈ 2,500 s, xenon, and about 60% efficiency:

- Mass flow is ṁ ≈ 2ηP/v² ≈ 1.9 g/s, which is about 19,000–20,000 sccm Xe.
- Holding background pressure near 10 µTorr (1.3×10⁻³ Pa) requires an effective xenon pumping speed of about 2.5×10⁷ L/s.
  - That figure matters because Hall thruster operation is measurably pressure-sensitive above roughly that level. Thrust, discharge oscillations, plume divergence and cathode coupling all shift.
- The largest EP facilities provide xenon pumping speeds of order 10⁶ L/s. NASA Glenn VF-5 is the usual reference.
- The same arithmetic at 100 kW gives about 2.5×10⁶ L/s. That is consistent with the ~100 kW X3 nested-Hall tests at Glenn running at elevated background pressure, which is a useful sanity check.

So ground facilities are short by roughly an order of magnitude at full cluster scale. Ground can credibly test a module of 50–150 kW and a small cluster of a few modules at reduced power. Ground cannot test the MW cluster at space-representative pressure.

**The second fact, which both pure options ignore.** TRL 6 for propulsion includes life and wear evidence. Thousands of hours of wear testing cannot be obtained in flight within Phase 0. The flight path is therefore never "flight instead of ground". It is always "ground modules plus flight". The real question is narrower: **what evidence about the cluster, beyond the module, is needed for KDP-0B, and where can it be obtained?**

## 2. Criteria and weights

These are stated before the options. Swing weights reflect the spread of each criterion across plausible paths, not its abstract importance.

| # | Criterion | Range across plausible paths | Swing weight | Why this weight |
|---|---|---|---|---|
| C1 | **Validity of the TRL 6 claim at a one-way gate.** Does the evidence close the space-vs-facility and cluster-vs-module gaps? | From "extrapolated 10× with no anchor" to "flown and measured at representative scale" | **30** | Widest consequential range. D-02 forbids waivers, so a weak claim either fails the gate or invites a de facto waiver. |
| C2 | **Discriminating power (strong inference).** Does each test separate "the model works" from "it doesn't" early? | From a single pass/fail at the end to staged, falsifiable predictions | **15** | Determines whether failure arrives at the mid-term review (cheap) or at KDP-0B (expensive). |
| C3 | **0A cost** | From about $50–150M (ground plus model) to about $0.5–1.5B (dedicated flight subset of several hundred kW). Order-of-magnitude only. | **15** | The range is large, but D-01 already accepts Phase 0 as a capability programme rather than a cost saving. That reduces the weight below its raw dollar span. |
| C4 | **Schedule to KDP-0B** | Facility-limited (~3–4 years) vs flight-limited (~5–7 years including spacecraft, launch and operations) | **15** | A flight path can put KDP-0B on the critical path of a launch. |
| C5 | **Coupling and risk concentration.** Does T01 evidence tie its fate to the pathfinder or another programme element? | From independent to the pathfinder carrying the propulsion verdict | **10** | Moderate. Coupling can be mitigated by design, but it shapes who owns the failure. |
| C6 | **Option value and reversibility** | From committing flight hardware on day 1 to committing only when triggered | **15** | D-02 says stringency follows reversibility. Preserving the ability to escalate or abandon is directly valued. |

Total: 100.

## 3. Options

- **O0 Null.** Leave the panel split as it stands: no facility rule, no path. *Rejected.* With no rule text, KDP-0B will be argued from whatever evidence happens to exist. Facility limits are known now, so the null option does not defer the problem. It converts a planned trade into an unplanned waiver request. It also leaves undecided whether the pathfinder must carry propulsion, which blocks pathfinder sizing.
- **O1 Ground modules plus validated cluster model (pure Claude option a).** Covers:
  - module qualification and wear at full module power in the best available facility;
  - small-cluster ground tests;
  - pressure sweeps;
  - a physics-based cluster model extrapolated to MW in vacuum.
- **O2 Flight subset (pure option b).** A dedicated tug demonstrator flying a substantial fraction of the cluster, roughly 200–500 kW across 4–10 modules, on top of ground module qualification.
- **O3 Hybrid with staged escalation (recommended).** O1, plus a *flight anchor*:
  - **What it is.** 2–4 production-representative modules at 50–200 kW total, flown on the pathfinder if its power budget allows, otherwise on a hosted or small dedicated bus.
  - **What it is for.** It exists to measure the near-zero-pressure end of the pressure-dependence curve and the small-N interaction terms. Those are precisely the parameters the cluster model must extrapolate.
  - **Escalation.** A full O2 flight subset is pre-committed as the response if the model fails its validation criteria at the 0A mid-term review.
- **O4 Build an MW-class vacuum facility.** *Rejected as the primary path, kept as a contingency study.*
  - At about 10⁵ L/s per m² of xenon cryopanel, roughly 250 m² of cryosurface would be needed.
  - The plume dumps on the order of 1 MW of beam power that must be kept off the cryopanels.
  - Credible cost runs to hundreds of $M and the schedule is 4+ years before the first test.
  - It buys ground validity at one propellant only. The facility case changes sharply under D-05; see section 7.
- **O5 Re-scope.** Lower module count or power, or defer MW clustering to Phase 1 and treat KDP-0B as a module-level gate. *Rejected.* D-02 forbids waiving project-ending technologies, and downgrading the scope of "T01" to pass the gate is a waiver by redefinition. The honest version of O5 is the existing fallback "0A only, Earth supply", which remains available.

## 4. Assessment matrix (QOC)

Scores run 0–10, where 10 is best on the criterion. Weighted totals are /1000.

| Option | C1 Validity (30) | C2 Discrimination (15) | C3 Cost (15) | C4 Schedule (15) | C5 Coupling (10) | C6 Option value (15) | **Weighted** |
|---|---|---|---|---|---|---|---|
| O0 Null | 1 | 1 | 9 | 5 | 6 | 3 | **385** |
| O1 Ground plus model | 5 | 7 | 9 | 8 | 9 | 8 | **720** |
| O2 Flight subset | 9 | 5 | 2 | 3 | 4 | 2 | **535** |
| **O3 Hybrid, staged** | **8** | **9** | 6 | 6 | 6 | 9 | **750** |
| O4 New facility | 7 | 6 | 3 | 3 | 9 | 4 | **525** |
| O5 Re-scope | 2 | 4 | 9 | 9 | 9 | 6 | **545** |

**Reasoning behind the key cells:**

- **O1 on C1 (5).** The model must extrapolate about 10× in power and from roughly 10⁻⁵ Torr to space vacuum, with no zero-pressure anchor. Known pressure effects make that an unanchored extrapolation at a one-way gate.
- **O3 on C1 (8).** The anchor converts the pressure-dependence extrapolation into interpolation. What remains is the N-scaling from about 4 modules to the full count. That is a smaller and more tractable gap, provided interaction terms saturate with spacing, which the ground small-cluster tests can probe.
- **O2 on C2 (5).** A large flight subset tends to be a single, late, expensive pass/fail. It is also ambiguous on failure: was it the thruster, the PPU, the bus or the operations?
- **O3 on C2 (9).** The model makes pre-registered predictions for the anchor flight before it flies.

**Result:** O3 and O1 are close, at 750 versus 720. The gap comes almost entirely from C1, which is why the sensitivity analysis matters.

## 5. Sensitivity vs trade-off points

**Sensitivity points.** These strongly affect one attribute and can be settled by facts.

- **S1. Gap between ground facility pressure and space at module scale.** If facility effects on the chosen thruster type are small and well characterised below ~10 µTorr, the anchor's value falls. O1 then beats O3 because of its cost and schedule advantage.
  - Gridded ion engines are less sensitive to background pressure in performance than Hall thrusters, though charge-exchange erosion still matters.
  - **Thruster type selection is therefore a sensitivity point for this decision.**
- **S2. Pathfinder power budget.** If the pathfinder cannot supply about 50 kW or more to an EP payload, the anchor needs its own bus. O3's cost then rises towards O2's lower bound and its C5 score improves.
- **S3. Propellant (D-05).**
  - **Iodine** condenses readily, which eases facility pumping enormously. O1 and O4 strengthen, but contamination and material compatibility become new cluster-model terms.
  - **Krypton** is harder to cryopump than xenon, which widens the facility gap. O3 and O2 strengthen.
  - **Argon** widens the gap further.
  - **Rule:** re-run this matrix when D-05 closes.
- **S4. Interaction saturation.** If plume, cathode and charging interactions saturate at N ≈ 3–4 with realistic spacing, small-N ground plus flight data bound the MW cluster. If they grow with N, as collective charging or shared-bus dynamics might, no subscale path suffices and O2 or O4 becomes necessary.

**Trade-off points.** These affect two attributes in opposite directions. They are values questions for the owner, not facts to settle.

- **T1. Validity vs cost and schedule (C1 against C3 and C4).** How much residual extrapolation risk is the owner willing to carry through a one-way gate in exchange for a programme $0.3–1B cheaper and 2–3 years faster? D-02 says "no waivers", but it does not say how wide an extrapolation still counts as "demonstrated". **The owner must state a maximum allowed extrapolation ratio.** I propose ≤ 5× in total cluster power from the largest tested configuration, with the pressure axis anchored.
- **T2. Pathfinder coupling (C5 against C3).** Putting the anchor on the pathfinder saves a bus but makes the pathfinder's success partly hostage to T01, and vice versa. This is a values question about programme risk ownership.

## 6. Evidence certainty

Likelihood (how probable) is kept separate from confidence (how good the evidence is).

| Claim | GRADE certainty | Likelihood / confidence |
|---|---|---|
| MW-class xenon EP needs ~10⁷ L/s pumping for ≤10 µTorr. Existing facilities are ~10⁶ L/s. | **High** for the arithmetic; **moderate** for exact facility figures | *Virtually certain* that a full-scale gap of ≥5× exists; high confidence |
| Hall thruster performance and plume depend measurably on background pressure | **High.** Multiple facility-effects studies; community recommended practice on pressure measurement and effective pumping speed (Dankanich et al., *J. Propulsion and Power*, 2017) | *Very likely*; high confidence |
| ~100 kW-class Hall operation demonstrated on the ground (X3 at Glenn), with elevated background pressure | **Moderate** | High confidence it occurred; medium confidence on representativeness |
| Multi-thruster Hall cluster interactions are characterised at small N and low power (AFRL cluster work, early 2000s) | **Moderate** at low power; **very low** at 100 kW+ per module | Medium confidence it transfers |
| Validated models can extrapolate to zero pressure within ±5% thrust and ±10% on divergence | **Low** | *About as likely as not* without a flight anchor; low confidence |
| Interaction terms saturate by N≈4 | **Very low.** No data at relevant scale. | Unknown; this is what the programme must test |
| Flight subset cost of ~$0.5–1.5B for several hundred kW | **Low.** Analogy to the Gateway PPE-class contract (~50 kW SEP, ~$375M for the 2019 award) scaled for power and arrays. | Medium confidence on order of magnitude only |
| T01 is TRL 2–4 today | **Moderate.** The panel agrees on the bracket, not the point. | High confidence that it is below 5 |

The weakest evidence sits exactly where the decision hinges: model extrapolation and interaction saturation. That is the argument for buying the cheapest test that discriminates on those two, rather than the most impressive one.

## 7. Key assumptions

Each is listed with the evidence that would falsify it.

- **A1. Cluster-level risk is dominated by a small set of measurable terms.** Those terms are pressure-dependent performance, plume and plume interaction, cathode coupling, PPU and bus dynamics, and spacecraft charging.
  - *Falsified if* the small-N ground tests show unexplained behaviour not captured by these terms, such as unmodelled oscillatory coupling between modules.
- **A2. Module wear and life can be qualified on the ground at full module power.**
  - *Falsified if* the facility pressure at module scale exceeds the threshold where erosion mechanisms change. Facility carbon backsputter that contaminates wear data is one example.
  - If so, life evidence also needs an anchor, or a module power reduction.
- **A3. The flight anchor can be production-representative.** That means the same module, PPU design and cathode configuration.
  - *Falsified if* pathfinder power or mass forces a derated or substitute thruster. In that case the anchor no longer anchors.
- **A4. The model can be pre-registered and judged against fixed tolerances.**
  - *Falsified if* modelling teams cannot commit to predictions before data arrive. That is an organisational failure, not a technical one.
- **A5. D-05 does not select a propellant that removes the facility gap.**
  - *Falsified by* an iodine selection with demonstrated cluster-scale condensation pumping. O1 then likely dominates.
- **A6. Dependencies on rq-0-16 and rq-0-54.** I assume the requirements these entries carry, plausibly covering propellant logistics and pathfinder scope, do not already fix pathfinder power or propellant. I have not verified their content; the owner should confirm. If either fixes pathfinder EP power below ~50 kW, S2 triggers.

**ACH: why might O1 vs O3 come out differently?**

| Hypothesis | Disconfirming evidence | Status |
|---|---|---|
| H1. Ground plus model is sufficient | Known Hall pressure sensitivity (disconfirms unanchored extrapolation); no flight data at 100 kW+ | Moderately disconfirmed |
| H2. Only a large flight subset suffices | Small-N cluster data exist; the module physics is well understood; the large-flight path still needs ground life | Moderately disconfirmed |
| H3. Anchored model is sufficient unless interactions grow with N | Nothing currently disconfirms it; the S4 risk is untested | **Least disconfirmed. Adopt H3, and design tests that would disconfirm it early.** |

## 8. Decision, warrant, accepted downside

**Y-statement.** In the context of a project-ending T01 at a no-waiver, one-way KDP-0B, with ground vacuum facilities about 10× short of MW-class pumping, we chose ground-qualified modules plus a pre-registered cluster model, validated by small-N ground cluster tests and pressure sweeps and anchored by a 2–4-module production-representative flight anchor, with a pre-committed escalation to a full flight subset if validation fails at the 0A mid-term review. We did so to reach a defensible TRL 6 claim at least cost and with the earliest discriminating failure. We accept that KDP-0B rests on an interpolated model with up to ~5× extrapolation in N, carrying residual collective-interaction risk into the first Phase 1 vehicle.

**Toulmin structure:**
- **Claim.** O3 gives TRL 6 evidence adequate to a one-way gate.
- **Grounds.** The facility arithmetic; the established pressure-sensitivity literature; existing small-N cluster data; ground-only life qualification is unavoidable regardless of path.
- **Warrant.** TRL 6 permits a relevant environment, which may be ground or space, with a representative prototype. A model counts as "demonstrated" when it has predicted, before the fact, independent measurements spanning the extrapolation axes. The anchor supplies the one axis, pressure, that ground cannot.
- **Backing.** Standard verification-by-analysis practice used for structures and large deployables that cannot be tested at full scale in 1g; D-02's reversibility principle.
- **Qualifier.** *Probably sufficient.* I would put about 65–75% on passing the mid-term validation without escalation, at low-to-medium confidence.
- **Rebuttal conditions.** Interaction growth with N (S4); D-05 propellant change (S3); pathfinder unable to host a representative anchor (S2/A3).

**Proposed gate rule text** (for `gates-proposal.yaml`, T01):

```yaml
T01_evidence_path:
  kdp_0b_criterion: >
    TRL 6 in a relevant environment, no waiver. Demonstrated by ALL of:
    (1) Module: full-power module qualification and wear test to ≥50% of
        mission life (balance by validated wear model) at background
        pressure ≤ P_max (default 10 µTorr Xe-equivalent, propellant-adjusted
        per D-05), with pressure sweep ≥3 points spanning ≥5×.
    (2) Ground cluster: ≥3 production-representative modules on a shared
        PPU/bus architecture, operated simultaneously at the highest power
        the facility sustains at ≤ 3×P_max.
    (3) Cluster model: predictions pre-registered before (2) and (4);
        within ±5% thrust, ±10% plume divergence, cathode-coupling voltage
        and bus-stability margins as specified.
    (4) Flight anchor: ≥2 production-representative modules in space,
        ≥500 h cumulative, measuring thrust, plume, charging, bus dynamics
        against pre-registered predictions.
    (5) Max extrapolation from largest tested configuration to flight
        cluster ≤ 5× in total power; pressure axis anchored by (4).
  mid_term_0A_trigger: >
    If (3) fails against (2) or against the ground pressure sweep, or if
    interaction terms grow with N across tested configurations, escalate to
    a flight subset of ≥20% of cluster power (owner-approved budget line
    pre-reserved), or invoke fallback "0A only, Earth supply".
  rerun_on: [D-05 closure, pathfinder power baseline, thruster-type selection]
```

**Evidence that would change the ruling:**

- **Towards O1:**
  - A facility demonstrated at ≤10 µTorr with ≥500 kW of propellant flow;
  - an iodine or other condensable propellant selection with demonstrated pumping;
  - flight data from other programmes (for example, 50 kW-class Gateway PPE operations) showing ground-to-space agreement within the model tolerances for the same thruster family.
- **Towards O2 or O4:**
  - Small-N tests showing interaction terms growing with N;
  - a model failing its pre-registered predictions;
  - selection of krypton or argon.
- **Towards the fallback:**
  - Escalation triggered and the flight-subset budget not available.

## 9. Consequences

**Enables:**
- Pathfinder sizing can proceed with a defined EP payload: 2–4 modules at 50–200 kW, plus power and thermal provisions. It is no longer an open "might carry propulsion".
- Facility booking and an upgrade study for the best available facility can start now.
- Model work can begin under pre-registration discipline.

**Constrains:**
- **D-05** must now report its effect on facility pumping, not just on supply.
- **Thruster type** (Hall vs gridded) inherits S1 as an explicit criterion.
- **Pathfinder** gains a T01 dependency that must be firewalled. The pathfinder's own success criteria should not fail if the anchor underperforms; the anchor's purpose is measurement, not mission.

**Conflicts to record:**
- O3 pre-reserves a contingent flight-subset budget line that sits outside D-01's 0A envelope until triggered. The owner must accept that contingent liability or accept the fallback as the response.

**Subsumes:**
- The "test facility" split in the panel table. With this ruling, Claude's (a)/(b) framing becomes a staged (a)+anchor, then (b) on trigger. GPT's "MW cluster integration unproven" becomes gate criteria (2)–(5).