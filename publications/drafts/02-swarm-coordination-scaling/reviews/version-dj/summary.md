# Version DJ Review Summary

## Recommendations

| Reviewer | Recommendation | Change from DI |
|----------|---------------|----------------|
| Gemini 3 Pro | **Accept with Minor Revisions** | Stable (3M/4m→3M/5m) |
| GPT-5.2 | **Major Revision** | Stable (8M/10m→8M/8m) |
| Claude Opus 4.6 | **Major Revision** | Stable (5M/12m→5M/10m) |

## What DJ Fixed (Acknowledged by Reviewers)

1. **γ renamed to "slot efficiency"** — GPT DI #1 ("γ is not MAC efficiency") acknowledged: GPT DJ #4 still mentions MAC but the rename is partially absorbed. Claude DJ methodology mentions "slot efficiency" without complaint about naming.
2. **Boxed γ definition + feasibility threshold** — Claude DI #5 (scope ambiguity) partially addressed: Claude DJ notes "two-test feasibility framework is well-defined." GPT DJ #4 still wants explicit "contract" for zero-collision assumption.
3. **Formalized p_eff = d·p_cmd** — GPT DI #3 (d/p_cmd under-specified) partially addressed: GPT DJ #1 acknowledges improvement but still wants "3 mission archetypes with numeric schedules."
4. **Removed Model S from joint interaction table** — Claude acknowledges "Model S appears only as a comparison curve."
5. **Compressed DES with "conditional predictions" disclaimer** — Both GPT/Claude acknowledge the honest labeling but DES still too prominent.
6. **1 kbps motivation added** — Claude DI #4 (1 kbps scrutiny) NOT RE-RAISED as major. RESOLVED.
7. **Unicast latency scope statement** — Gemini DI #3 persists but acknowledges the scope statement. GPT did not re-raise.
8. **Stress-case 46% labeling** — GPT DI #4 (stress-case labeling) acknowledged: "improved but still risks being read as typical." Gemini DJ #1 raises a NEW angle (thermal/power sizing).
9. **Algorithm 1 safety factor (margin < 10% warning)** — Gemini DI #2 (T_acq sensitivity) NOT RE-RAISED. RESOLVED.
10. **C_node added to Algorithm 1 REQUIRE** — GPT minor #9 NOT RE-RAISED. RESOLVED.

## What PERSISTS (Structural Barriers)

Three issues persist across ALL reviews and appear unfixable via text edits alone:

1. **No external validation** (Claude #3, GPT implicit, Gemini aware) — All reviewers understand but Claude/GPT make it a blocking major. Cannot be fixed without NS-3 or hardware measurements.
2. **DES/packet-level provide limited independent value** (Claude #1/#2, GPT #5/#6) — Despite honest reframing, the fundamental issue is that DES shares equations with closed-form. Can only be mitigated by (a) reducing prominence or (b) adding non-tautological DES results.
3. **Paper too long/repetitive** (Claude #4, GPT density complaints) — Despite DJ compressions, still ~13 pages. Need aggressive cuts to 10-11 pages.

## Gemini: Stable (3M→3M, 4m→5m)

DI→DJ resolved:
- DI #2 (T_acq sensitivity / safety factor) → RESOLVED (Algorithm 1 margin warning accepted)

DI→DJ persistent:
- DI #3 (unicast latency) → DJ #2 (persists, wants Algorithm 1 warning for max reaction time)

DI→DJ evolved:
- DI #1 (static membership) → DJ #3 (fleet-level interference at poles — different framing)

New:
- DJ #1: Stress-case 46% thermal/power sizing distinction (NEW — differentiate spectrum vs energy dimensioning)

## GPT: Stable (8M→8M, 10m→8m)

DI→DJ persistent (all 8 DI majors persist in some form):
- DI #1 (rename γ) → DJ #4 (framework "MAC efficiency" could be misapplied — still wants "contention factor" placeholder)
- DI #2 (γ ledger) → DJ #2 (γ unification fragile — ACK/framing decomposition, wants reproducibility check)
- DI #3 (d/p_cmd under-specified) → DJ #1 (d still under-justified — wants 3 mission archetypes)
- DI #4 (46% stress-case) → DJ #3 (stress-case still risks "typical" reading — wants η vs d figure)
- DI #5 (DES self-confirmation) → DJ #5 (DES too close to confirming equations)
- DI #6 (packet-level rename) → DJ #6 (packet-level is parameter derivation, not validation)
- DI #7 (probabilistic Test B) → DJ #7 (GE/ARQ coherence-time over-generalization — wants per-slot GE)
- DI #8 (practitioner worksheet) → DJ #8 (practitioner guidance needs measurement protocol)

No new majors. Minor count improved 10→8.

## Claude: Stable (5M→5M, 12m→10m)

DI→DJ resolved:
- DI #4 (1 kbps budget scrutiny) → RESOLVED (CubeSat motivation accepted)
- DI #3 (GE false precision / joint sensitivity) → Demoted to methodology note (no longer separate major)

DI→DJ persistent:
- DI #1 (DES limited) → DJ #1 (DES negligible independent value)
- DI #2 (no external validation / NS-3) → DJ #3 (no external validation)
- DI #5 (scope ambiguity) → DJ #4 (paper too long/repetitive — evolved)

New/elevated:
- DJ #2 (packet-level validation inadequate) — elevated from DI methodology note to full major
- DJ #5 (generalized γ is standard, not novel) — NEW

Minor count improved 12→10.

## Progress Trajectory

| Version | Gemini | GPT | Claude |
|---------|--------|-----|--------|
| DA | Accept w/ Minor (2M/5m) | Major (7M/10m) | Major (5M/12m) |
| DB | Accept w/ Minor (2M/4m) | Major (8M/7m) | Major (5M/13m) |
| DC | Accept w/ Minor (3M/5m) | Major (6M/8m) | Major (6M/13m) |
| DE | Accept w/ Minor (3M/4m) | Major (9M/10m) | Major (5M/12m) |
| DF | Accept w/ Minor (3M/5m) | Major (8M/9m) | Major (5M/14m) |
| DG | Accept w/ Minor (3M/4m) | Major (6M/8m) | Major (4M/14m) |
| DH | Accept w/ Minor (2M/4m) | Major (6M/7m) | Major (5M/10m) |
| DI | Accept w/ Minor (3M/4m) | Major (8M/10m) | Major (5M/12m) |
| **DJ** | **Accept w/ Minor (3M/5m)** | **Major (8M/8m)** | **Major (5M/10m)** |

## Analysis: Why GPT Won't Budge

GPT has been at 6-9 majors for 10+ versions. Its 8 DI majors mapped exactly to 8 DJ majors. The terminology fix (slot efficiency) was acknowledged but spawned a new request (ρ_MAC contention placeholder). The d/p_cmd formalization was acknowledged but GPT now wants full mission archetypes. **Pattern: every fix spawns a follow-on request at the same severity level.** GPT's core issues are structural:
1. Wants probabilistic Test B (not text-fixable)
2. Wants independent validation (not text-fixable)
3. Wants measured modem behavior (not text-fixable)
4. Wants GE sub-slot granularity (not text-fixable)

These are all "real simulation/measurement" requests that cannot be addressed by editing the manuscript.

## Strategy for Version DK

**Key insight: We've hit diminishing returns on text edits. The remaining GPT/Claude majors are ~60% structural (need external validation, NS-3, measurements) and ~40% presentation (need aggressive compression).** The presentation issues ARE fixable.

### Priority 1: Aggressive Compression to ≤11 pages (Claude #4, GPT density)

This is the single highest-impact text-fixable change. Target: cut 20-25% of content.

- **Remove DES framework description from main text** → 1-sentence reference to supplementary. Keep ONLY: Fig. 4 (buffer CDF) + 3 sentences on tail results.
- **Remove link budget table from main text** → move to supplementary. Keep 1-sentence summary.
- **Remove margin analysis table from main text** → move to supplementary. Keep key numbers inline.
- **Consolidate Tables IV + IX + X** into one comprehensive "Rate Feasibility Summary" table
- **Remove Table capability_matrix** (topology comparison table) → replace with 2 sentences
- **Remove repeated 35 kbps statements** — keep in abstract + Algorithm 1 + conclusion only
- **Compress thundering herd to 2 sentences**
- **Compress fleet reuse to equation + 1 sentence**

### Priority 2: One-Page Timing/γ Contract Box (GPT #2, CS #1)

Single authoritative box listing ALL per-slot components with explicit in/out-of-γ marking. This replaces scattered explanations and should actually SAVE space while satisfying GPT.

### Priority 3: Reframe Validation Language (Claude #1/#2, GPT #5/#6)

- Rename Section IV-J to "Standards-Grounded Parameterization" (drop all "validation" language)
- Reduce DES to "Implementation verification + tail estimation"
- Change title word "Design Equations" → "Design Methodology" (Claude CS #3)

### Priority 4: Mission Archetype Timeline (GPT #1)

Add 2-3 line mission timeline (station-keeping, orbit-raising, disposal) with computed (d, p_cmd) values. This is compact and directly addresses GPT's persistent #1.

### Priority 5: Contention Factor Placeholder (GPT #4)

Add one sentence: "Under contention, replace γ with γ·ρ_MAC where ρ_MAC ∈ (0,1] is an empirical MAC utilization factor from NS-3 or measurements."

### Priority 6: Thermal/Power Sizing Note (Gemini #1)

Add 2 sentences: size thermal/power for d=0.10; size spectrum/buffer for d=1.0 burst.

### Priority 7: Polar Convergence Limitation (Gemini #3)

Add 1 sentence to limitations: R=7 may break at high latitudes; dynamic frequency assignment needed.

### Deferred (Structural, Not Text-Fixable)

- NS-3 external validation (Claude #3, GPT implicit)
- Probabilistic Test B with jitter distributions (GPT #7)
- GE per-slot granularity (GPT #7)
- Hardware γ measurement (Claude #2)
- Network calculus bounds (Claude CS #5)

## Text-Fixable Items for DK

1. **Aggressive compression to ≤11 pages** — CRITICAL (remove DES details, link budget, margin table, topology table, consolidate rate tables)
2. **Timing/γ contract box** — single authoritative slot-time decomposition
3. **Reframe validation → parameterization** (Section IV-J rename, DES demotion)
4. **Mission archetype timelines** — 3 lines with (d, p_cmd) values
5. **Contention factor ρ_MAC placeholder** — 1 sentence
6. **Thermal/power sizing distinction for 46%** — 2 sentences
7. **Polar convergence limitation** — 1 sentence
8. **Model S/C mnemonic** — "Simplified"/"CCSDS" labels (Claude minor #9)
9. **η_0 invariance claim softening** — "weakly dependent" (Claude minor #1)
10. **Version tag** → paper-02-v-dk
