# Version DG Review Summary

## Recommendations

| Reviewer | Recommendation | Change from DF |
|----------|---------------|----------------|
| Gemini 3 Pro | **Accept with Minor Revisions** | Stable (3M/5m->3M/4m) |
| GPT-5.2 | **Major Revision** | Improved (8M/9m->6M/8m) |
| Claude Opus 4.6 | **Major Revision** | Improved (5M/14m->4M/14m) |

## What DG Fixed (Acknowledged by Reviewers)

1. **Per-slot acquisition justified** -- GPT: Not re-raised as major (was DF #1). Acquisition model paragraph and rate_feasibility table absorbed. GPT now raises #6 (slot timing contract) which is a narrower follow-up.
2. **ARQ demand derivation** -- GPT: Acknowledged P95 binomial calculation; now wants consistent probabilistic treatment across per-node vs cluster-common correlation (evolved, not dropped).
3. **TDMA sizing comparison** -- Claude: γ expression now #4 with remedy "reframe as reference parameterization" (previously "absent comparison"). Explicit DVB-RCS2 reference absorbed.
4. **k_c independence of γ** -- Gemini: Not re-raised (was DF #2). k_c=500 scaling note resolved.
5. **GE conditioning** -- Partially absorbed. GPT still wants per-node vs cluster-common specification.
6. **γ consistency ledger strengthened** -- GPT: Acknowledges "authoritative" values. Narrower #2 now about correlation structure, not γ values.
7. **Thundering herd promoted** -- Gemini: Re-raised as #3 but wants BEB parameter stability proof, not just the estimate. Claude demotes to minor #4 ("tangential").

## GPT Improvement (8M->6M -- TIED BEST-EVER)

DF->DG resolved:
- DF #1 (per-slot acquisition) -> Resolved (justified; rate_feasibility shows all modes)
- DF #6 (ARQ demand derivation) -> Partially resolved (P95 added; evolved to #2 correlation)

DF->DG evolved/narrowed:
- DF #2 (γ values authoritative) -> DG #6 (slot timing contract table -- narrower, wants consolidated table)
- DF #3 (three-layer) -> DG #3 (still present but narrower: "reframe narrative")
- DF #4 (DES) -> DG #5 (persistent: "too much real estate")
- DF #5 (campaign d) -> DG #4 (persistent: p_cmd=1 assumption)
- DF #7 (validation thin) -> DG #1 (persistent structural)
- DF #8 (R=7 qualification) -> Minor #5 (DEMOTED from major!)

New:
- DG #2: ARQ/GE node correlation structure (per-node independent vs cluster-common) -- NEW angle
- DG #6: Slot timing "implementation contract" table -- NEW (consolidation request)

## Claude Improvement (5M->4M -- BEST-EVER)

DF->DG resolved:
- DF #3 (TDMA comparison absent) -> Resolved (explicit DVB-RCS2 comparison added)

DF->DG evolved/narrowed:
- DF #1 (DES) -> DG #1 (persistent, remedy now "compress or NS-3")
- DF #2 (GE specificity) -> DROPPED as major (absorbed by conditioning text)
- DF #4 (static clusters) -> DG #3 (persistent)
- DF #5 (coordinator SPOF) -> DROPPED as major (thundering herd promotion resolved)

New:
- DG #2: 1 kbps per-node budget insufficiently justified -- NEW, SIGNIFICANT ("if relaxed to 2 kbps, most interesting results become non-binding")

Minors: 14 (stable). Several are new micro-issues (abstract notation, Table I placement, Eq. 1 assumption, η₀ reconciliation).

## Gemini Evolution (3M stable, minors improved)

- DF #1 (ARQ coherence) -> DG #2 (Doppler/range γ sensitivity) -- EVOLVED from channel model to geometric
- DF #2 (k_c sensitivity) -> RESOLVED (k_c independence statement absorbed)
- DF #3 (R=7 qualification) -> DG #3 (thundering herd BEB stability)

New:
- DG #1: 1 kbps vs 35 kbps logical/physical confusion -- NEW but easy fix
- DG #2: γ sensitivity to range/Doppler variations -- NEW, wants brief calculation
- DG #3: BEB parameter justification for thundering herd -- EVOLVED

## Progress Trajectory

| Version | Gemini | GPT | Claude |
|---------|--------|-----|--------|
| CW | Accept w/ Minor (2M/4m) | Major (7M/8m) | Major (5M/14m) |
| CX | Accept w/ Minor (2M/4m) | Major (7M/7m) | Major (5M/14m) |
| CY | Accept w/ Minor (3M/4m) | Major (7M/10m) | Major (5M/13m) |
| CZ | Accept w/ Minor (3M/5m) | Major (7M/8m) | Major (5M/12m) |
| DA | Accept w/ Minor (2M/5m) | Major (7M/10m) | Major (5M/12m) |
| DB | Accept w/ Minor (2M/4m) | Major (8M/7m) | Major (5M/13m) |
| DC | Accept w/ Minor (3M/5m) | Major (6M/8m) | Major (6M/13m) |
| DE | Accept w/ Minor (3M/4m) | Major (9M/10m) | Major (5M/12m) |
| DF | Accept w/ Minor (3M/5m) | Major (8M/9m) | Major (5M/14m) |
| **DG** | **Accept w/ Minor (3M/4m)** | **Major (6M/8m)** | **Major (4M/14m)** |

## Major Issues Remaining

### Priority 1: 1 kbps / 35 kbps logical vs physical clarification (Gemini #1, Claude #2 related)
Gemini wants explicit sentence: "35 kbps is the burst rate at the coordinator; 1 kbps is the time-averaged per-node allocation." Claude's #2 is deeper: "if relaxed to 2 kbps, TDMA analysis becomes unnecessary." Both need addressing.
**Fix:** Add explicit clarifying sentence early in Section III. For Claude's concern: add C_node sensitivity note showing where TDMA becomes non-binding.

### Priority 2: GE correlation structure (GPT #2 -- NEW)
GPT wants explicit specification: per-node independent, per-link independent, or cluster-common (shared fading). Current model is per-node independent (Bernoulli); cluster-common produces heavier tails.
**Fix:** Add explicit statement: "GE is per-node independent (each node experiences independent channel state). Cluster-common (shared fading) would increase P99 by ~25% but does not affect per-cluster TDMA sizing."

### Priority 3: Slot timing contract table (GPT #6 -- NEW)
Wants single consolidated table listing: preamble length, framing bits, FEC rate, acquisition model, guard composition, ACK policy, turnaround handling.
**Fix:** Add small "Slot & Superframe Timing Contract" table in Section IV-J.

### Priority 4: Three-layer reframe (GPT #3 -- PERSISTENT but narrower)
"rate ladder can be read as three checks." Reframe: Test A (bytes), Test B (airtime, γ is parameter within), screening indicator.
**Fix:** Rename rate ladder column; add explicit "algebraic decomposition of Test B" statement.

### Priority 5: γ reframe as reference parameterization (Claude #4)
"Does not constitute novel analytical result." Remedy: "Reframe Eq. 8 as reference parameterization."
**Fix:** Already partially done in DG. Strengthen: explicitly state "Eq. γ_time systematizes standard TDMA slot-time accounting" (already there) and downplay novelty further.

### Priority 6: DES reduction (GPT #5, Claude #1 -- PERSISTENT)
Both agree DES adds negligible value. GPT: "compress to appendix." Claude: "implement NS-3 or remove."
**Fix:** Remove Fig. coordinator_buffer_cdf. Compress DES section to 3 sentences. This saves ~12 lines and reduces DES prominence.

### Priority 7: Campaign p_cmd sensitivity (GPT #4)
"p_cmd=1 during campaigns" is assumed. Real ops have bursty, non-periodic commands.
**Fix:** Add p_cmd < 1 sensitivity: "At p_cmd = 0.2 (5 commands/cycle during campaigns), η_cmd drops 5x; stress case becomes ~13% instead of 46%."

### Priority 8: Doppler/range γ sensitivity (Gemini #2)
Wants brief S-band Doppler calculation confirming guard covers the dynamics.
**Fix:** Add: "Differential Doppler: ΔV ≤ 15 m/s at 500 km cluster → Δf ≈ 100 Hz at 2.2 GHz (S-band), well within Prox-1 acquisition bandwidth (±50 kHz). Propagation delay variation: Δτ = 500 km / c = 1.67 ms ⊂ T_guard = 4.7 ms."

### Priority 9: BEB stability justification (Gemini #3)
Wants probability calculation for successful slot capture.
**Fix:** Add: "P(success in round r) = (1/W_r)·(1-1/W_r)^(k_c-1). After round 4 (W=64): P ≈ 0.015/node/slot, stable throughput S = G·e^{-G} ≈ 0.36 at G=1."

### Priority 10: Static cluster membership (Claude #3 -- PERSISTENT)
Already scoped. The J2 analysis is there. Claude wants worst-case boundary cluster analysis.
**Fix:** Add one sentence: "Worst-case boundary cluster: re-association every ~90 min (1 per orbit); at 3-5 s optical handoff, duty loss ≈ 0.06-0.09%."

## Text-Fixable Items for DH

1. **1 kbps / 35 kbps clarifying sentence** -- Early in system model
2. **C_node sensitivity note** -- Brief: "At C_node = 2 kbps, η halves and TDMA margin doubles; the analysis is most valuable at C_node ≤ 1 kbps where TDMA is binding."
3. **GE correlation: per-node independent** -- Explicit statement
4. **Slot timing contract table** -- Small new table
5. **Three-layer: rename rate ladder** -- "algebraic decomposition of Test B"
6. **γ reframe** -- Further soften novelty claim
7. **Remove Fig. coordinator_buffer_cdf** -- Save space, reduce DES
8. **DES section compressed to 3 sentences**
9. **Campaign p_cmd < 1 sensitivity** -- Brief sentence
10. **Doppler/range calculation** -- Brief sentence
11. **BEB stability probability** -- Brief calculation
12. **Worst-case boundary cluster** -- One sentence
13. **GPT minor #2: γ rate-dependence wording** -- Clarify non-intuitive direction
14. **GPT minor #8: MAC vs slot efficiency** -- Use "slot efficiency" consistently
15. **Claude minor #1: abstract parenthetical** -- Simplify γ notation
16. **Claude minor #3: Eq. 1 uniform fan-out** -- State assumption
17. **Claude minor #7: AoI mean clarification** -- Add p_exc condition
18. **Claude minor #11: abstract γ range** -- Expand to match actual values
19. **Claude minor #14: Algorithm 1 η₀ reconciliation** -- Fix 5% vs 5.6%
20. **Version tag** -> paper-02-v-dh
