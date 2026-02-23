# Divergent View Coding Manual

## Purpose

This manual provides operational definitions and boundary examples for categorizing
divergent views produced by the multi-model deliberation protocol described in Paper 03
("Multi-Model AI Consensus for Megastructure Engineering"). It is intended to be precise
enough for an independent coder to replicate the four-category classification with high
inter-rater reliability.

All examples are drawn from actual divergent view records in the Project Dyson BOM
specification corpus (`static/content/bom-specs/`).

---

## Categories

### 1. Genuine Technical Trade-offs

**Definition:** The divergent view reflects fundamentally different engineering approaches
to solving the same problem, where each approach has distinct, well-understood advantages
and disadvantages. The positions are not reconcilable by gathering more data; rather, they
represent legitimate design alternatives that require a deliberate architectural decision.

**Inclusion criteria:**
- Each position names a specific engineering method, mechanism, or architecture
- The advantages of one approach correspond to disadvantages of another (true trade-off)
- An expert panel could reasonably defend any of the positions
- The impact statement references system-level consequences (mass, power, cost, reliability)

**Exclusion criteria:**
- Positions differ only in parameter magnitude (reclassify as Category 2)
- One position is clearly superior given available data (reclassify as Category 3 if data-dependent)
- The disagreement stems from different project goals rather than technical analysis (reclassify as Category 4)

**Prototypical example:**
> **Mining Robots -- Mobility Architecture** (phase-0/mining-robots)
> - Claude: Hexapod design
> - Gemini: Wheeled rovers for simplicity
> - GPT: Hybrid wheel-leg systems
>
> *Impact:* "Mobility system choice directly affects robot mass, power consumption, terrain
> capability, and manufacturing complexity. Wrong choice could result in robots unable to
> traverse asteroid terrain effectively."

This is prototypical because each mobility approach (hexapod, wheeled, hybrid) has well-known
engineering trade-offs in mass, terrain capability, and complexity, and no amount of additional
data alone will eliminate the trade-off.

**Boundary example (included):**
> **Assembly Robots -- Primary Joining Technology** (phase-1/assembly-robots)
> - Claude: Electron beam welding (60-150 kV, up to 25 kW) and friction stir welding as
>   primary methods
> - Gemini: Snap-fits and thermal welding with zero screws
> - GPT: Mechanical latching with kinematic docking and compliant connectors
>
> *Impact:* "Joining technology determines structural integrity, repairability, and assembly
> speed. Welding provides strong permanent joints but prevents repair. Mechanical joints allow
> disassembly but add mass and failure points."

Included because the trade-off between permanent (strong but irreparable) and mechanical
(repairable but heavier) joints is an inherent engineering tension, not resolvable by data alone.

**Boundary example (excluded -- reclassified as Category 2):**
> **Transport Vehicles -- Payload Capacity** (phase-0/transport-vehicles)
> - Claude: 200,000 kg
> - Gemini: 150,000 kg for faster transits
> - GPT: Variable configuration

At first glance, the mention of "faster transits" suggests a trade-off. However, the core
disagreement is about the magnitude of a single parameter (payload mass), and the speed
implication is a secondary consequence. The positions do not represent fundamentally different
engineering architectures -- they are reasonable judgments about where to set a continuous
design parameter. Reclassify as **Category 2**.

---

### 2. Reasonable Engineering Judgments

**Definition:** The divergent view reflects different but defensible choices for quantitative
parameters, sizing, or scaling within the same overall architectural framework. All models
agree on the general approach but differ on specific numerical values or scale factors.

**Inclusion criteria:**
- Positions primarily differ in magnitude, quantity, or sizing of the same concept
- The underlying technology or method is shared (or closely related) across positions
- Differences could be resolved through parametric optimization or sensitivity analysis
- Each value falls within a plausible engineering range

**Exclusion criteria:**
- Positions name fundamentally different technologies or mechanisms (reclassify as Category 1)
- The range of disagreement spans orders of magnitude AND different architectures
  (e.g., 85 kg vs. 1,850 kg units with completely different designs -- reclassify as Category 1)
- Positions differ because of unknown material properties or undemonstrated TRLs
  (reclassify as Category 3)

**Prototypical example:**
> **Solar Power Arrays -- Module Size** (phase-0/solar-power-arrays)
> - Claude: 2 MW modules
> - Gemini: 1 MW for easier handling
> - GPT: 5 MW for efficiency
>
> All three models agree on modular solar arrays; they disagree on the optimal module power
> rating. The 5x range (1-5 MW) is within normal engineering parametric variation for a
> module-based system.

**Boundary example (included):**
> **Solar Power Arrays -- Energy Storage** (phase-0/solar-power-arrays)
> - Claude: 500 MWh Li-ion
> - Gemini: 200 MWh is sufficient
> - GPT: Flow batteries for longer life

Included despite GPT proposing a different battery chemistry, because the core disagreement
is about storage capacity sizing (200-500 MWh). GPT's "flow batteries" remark is a secondary
preference within the same functional role (energy storage), not a fundamentally different
system architecture. The flow battery suggestion could alternatively push this toward
Category 1, but the primary axis of disagreement is capacity, so it stays in Category 2.

**Boundary example (excluded -- reclassified as Category 1):**
> **Collector Units -- Unit Size/Power Class** (phase-1/collector-units)
> - Claude: 10,000 m^2 collectors producing 52 MW each at 1,850 kg total mass
> - Gemini: 6,500 m^2 hexagonal sails producing 44 MW at 85 kg
> - GPT: Smaller 40 m^2 tile units producing 10 kW at 69 kg for manufacturing simplicity
>
> *Impact:* "Difference between 85 kg and 1,850 kg per unit is 20x mass difference affecting
> launch costs fundamentally."

Although the positions involve "sizes," the 250x variation in area (40 m^2 to 10,000 m^2) and
the correspondingly different structural, manufacturing, and deployment approaches make this a
genuine architectural trade-off, not merely parametric sizing. Reclassify as **Category 1**.

---

### 3. Knowledge Gaps / Insufficient Data

**Definition:** The divergent view exists because the relevant technical data is not yet
available, the technology is at low readiness, or the answer depends on measurements,
experiments, or demonstrations that have not been performed. Models adopt different assumptions
about unknowns, leading to divergent positions that could converge once data becomes available.

**Inclusion criteria:**
- At least one position explicitly or implicitly depends on technology readiness level (TRL)
- The resolution path references testing, experiments, or future data collection
- Positions differ primarily in optimism/pessimism about an undemonstrated capability
- Removing the uncertainty (e.g., a successful test) would likely collapse the disagreement

**Exclusion criteria:**
- All proposed technologies are at high TRL and well-characterized (reclassify as Category 1 or 2)
- The disagreement is about project philosophy or goals rather than technical unknowns
  (reclassify as Category 4)

**Prototypical example:**
> **Collector Units -- PV Technology Selection** (phase-1/collector-units)
> - Claude: Perovskite-silicon tandem (TRL 5, 31% efficiency, best mass efficiency)
> - Gemini: Perovskite/CIGS flexible thin-film (45% claimed, aggressive)
> - GPT: Space-proven multi-junction III-V cells (TRL 7-9) despite higher cost, citing
>   radiation tolerance concerns
>
> *Impact:* "PV technology choice affects efficiency, radiation degradation rate, manufacturing
> scalability, and cost per watt. TRL differences mean different development timelines."
>
> *Resolution path:* "Conduct accelerated radiation testing on perovskite samples. Track TRL
> advancement of tandem cells."

This is prototypical because the disagreement hinges on whether perovskite cells will achieve
adequate radiation tolerance and manufacturing maturity -- questions that can only be answered
through testing and development.

**Boundary example (included):**
> **ISPP Systems -- Power Source** (phase-0/ispp-systems)
> - Claude: Nuclear fission (Kilopower-class, 10 kWe units scaling to megawatt-class)
>   as baseline for lunar operations, citing lunar night resilience and power density
> - Gemini: Solar-only with large concentrators
> - GPT: Hybrid-ready architecture with solar baseline and optional nuclear plug-in,
>   explicitly declining to commit until site selection

Included because the choice depends critically on site selection (which has not been made)
and on the maturation of space nuclear power systems. GPT's explicit deferral ("declining
to commit until site selection") signals that missing information -- not a philosophical
preference -- drives the divergence.

**Boundary example (excluded -- reclassified as Category 1):**
> **Mining Robots -- Anchoring System** (phase-0/mining-robots)
> - Claude: Microspines
> - Gemini: Gecko-inspired adhesives
> - GPT: Harpoon-tethers
>
> *Resolution path:* "Test all three approaches on asteroid simulant materials in vacuum
> chamber."

Although testing is mentioned in the resolution path, all three anchoring technologies are
reasonably well-understood mechanistically. The disagreement is not about whether they *work*
in principle but about which trade-off profile (mechanical grip vs. adhesion vs. penetration)
is best suited to asteroid surfaces. The need for testing reflects normal engineering
validation, not a fundamental knowledge gap. Reclassify as **Category 1**.

---

### 4. Value-Laden / Philosophical Differences

**Definition:** The divergent view reflects different design philosophies, risk tolerances,
programmatic strategies, or values about how a megastructure project should be conducted.
These differences cannot be resolved by technical analysis alone because they involve
normative judgments about priorities, acceptable risk, and strategic direction.

**Inclusion criteria:**
- Positions reflect different attitudes toward risk, autonomy, cost, or timeline
- The disagreement persists even if all technical parameters were known with certainty
- Language includes normative terms: "should," "mandatory," "philosophy," "strategy"
- Different stakeholders with different values would legitimately choose different positions

**Exclusion criteria:**
- Disagreement would dissolve if a specific technical measurement were available
  (reclassify as Category 3)
- Positions differ in specific mechanisms rather than overall approach
  (reclassify as Category 1)

**Prototypical example:**
> **ISPP Systems -- Target Location and Tier Strategy** (phase-0/ispp-systems)
> - Claude: Three-tier architecture (Lunar south pole, then C-type asteroids, then Mercury)
>   with explicit timelines and the Moon as the mandatory first node
> - Gemini: Exclusively Near-Earth Asteroids as the primary and essentially only resource
>   node, arguing that "escaping gravity wells is fundamentally wrong for megastructure
>   logistics"
> - GPT: Site-agnostic modular plant adaptable to any ice-bearing body, deferring site
>   selection as an open question
>
> Gemini's position that gravity-well operations are "fundamentally wrong" is a philosophical
> stance about project strategy, not a technical finding. Claude's insistence on the Moon as
> "mandatory first node" reflects a programmatic value (risk reduction through proven
> accessibility). GPT's deferral reflects a different value (flexibility over commitment).

**Boundary example (included):**
> **Swarm Control System -- Manufacturing Philosophy** (phase-1/swarm-control-system)
> - Claude: Full rad-hard components (100 krad tolerance) with 50-year MTBF
> - Gemini: Automotive-grade (AEC-Q100) with spot shielding, accepting 2-3% annual
>   failure rate
> - GPT: Middle path with COTS + radiation characterization and selective hardening

Included because the core disagreement is about risk tolerance and cost philosophy:
Claude prioritizes reliability and long life (conservative, high-cost); Gemini accepts
higher failure rates in exchange for dramatically lower unit costs (aggressive, high-volume);
GPT seeks a middle ground. The same technical data about radiation environments would not
resolve this -- it is a value judgment about acceptable failure rates versus unit cost.

**Boundary example (excluded -- reclassified as Category 3):**
> **Material Processing Station -- Crew Presence** (phase-0/material-processing-station)
> - Claude, GPT: Human-tended with quarterly visits
> - Gemini: Fully autonomous with annual visits only

At first glance, "human-tended vs. fully autonomous" appears philosophical (a value judgment
about human involvement). However, the feasibility of "fully autonomous with annual visits"
depends on whether current autonomous systems can reliably operate processing equipment for
12 months without human intervention -- a capability that is undemonstrated at this scale.
The disagreement is better explained by different assumptions about autonomous system
maturity. Reclassify as **Category 3**.

---

## Coding Procedure

1. **Read the full divergent view entry**, including topic name, all positions with model
   attribution, priority rating, impact statement, and resolution path.

2. **Identify the primary axis of disagreement.** Ask: What is the single most important
   dimension along which the positions differ? Is it mechanism/architecture, parameter
   magnitude, data availability, or values/philosophy?

3. **Apply the primary category** based on the dominant axis:
   - Different mechanisms or architectures with inherent trade-offs --> **Category 1**
   - Same architecture, different parameter values --> **Category 2**
   - Positions hinge on undemonstrated capabilities or unavailable data --> **Category 3**
   - Positions reflect different risk tolerances or strategic philosophies --> **Category 4**

4. **If ambiguous between two categories, apply the tiebreaker rule:**
   - If the resolution path mentions *testing or experiments* AND the technology is below
     TRL 6, prefer **Category 3** over Category 1.
   - If positions span more than 10x in a quantitative parameter AND involve different
     architectures, prefer **Category 1** over Category 2.
   - If a normative/philosophical framing is used by at least one model but the underlying
     question is empirically resolvable, prefer **Category 3** over Category 4.
   - When genuinely torn between Categories 1 and 4, ask: "If we had perfect technical
     knowledge, would the disagreement persist?" If yes, assign **Category 4**. If no,
     assign **Category 1**.

5. **Record confidence** for each coding decision:
   - **High:** Category assignment is unambiguous; no boundary cases apply.
   - **Medium:** One tiebreaker rule was needed, but the result is clear.
   - **Low:** Multiple tiebreaker rules were considered, or the coder finds the assignment
     debatable. Flag for adjudication.

6. **Record any notes** explaining the reasoning, especially for Medium and Low confidence
   assignments.

---

## Inter-Rater Protocol

### Training Phase
1. Both raters independently read this manual in full.
2. Both raters independently code a shared calibration set of 10 divergent views
   (not included in the study sample).
3. Raters meet to compare calibration codings, discuss disagreements, and clarify
   manual interpretations. Resolve differences by consensus; update manual if needed.

### Coding Phase
1. Each rater independently codes the full sample.
2. For each divergent view, record: (a) primary category, (b) confidence level,
   (c) brief reasoning note.
3. Do not discuss individual codings with the other rater during this phase.

### Reconciliation Phase
1. Compute Cohen's kappa for inter-rater reliability on the primary category.
2. For any disagreements, both raters provide their reasoning in writing.
3. A third adjudicator (or the original two raters in conference) resolves
   disagreements by consensus, guided by this manual's tiebreaker rules.
4. Report both the initial kappa and the post-reconciliation agreement rate.

### Acceptable Reliability Thresholds
- Cohen's kappa >= 0.70: acceptable for primary analysis.
- Cohen's kappa 0.60-0.69: acceptable with reconciliation; note limitation.
- Cohen's kappa < 0.60: manual requires revision; re-train and re-code.
