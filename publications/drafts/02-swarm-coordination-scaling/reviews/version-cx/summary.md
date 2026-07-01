# Version CX Review Summary

## Recommendations

| Reviewer | Recommendation | Change from CW |
|----------|---------------|----------------|
| Gemini 3 Pro | **Accept with Minor Revisions** | Stable (2M/4m both) |
| GPT-5.2 | **Major Revision** | Slightly improved (7M/8m→7M/7m) |
| Claude Opus 4.6 | **Major Revision** | Stable (5M/14m both) |

## What CX Fixed (Acknowledged by Reviewers)

1. **RF-backup ConOps clarification** — Gemini no longer raises the "suspended hierarchy vs election" concern (was CW Major #1). The recovery transient framing resolved it.
2. **"Validated" → "anchored" language audit** — GPT #6 and Claude still want further tightening, but the §IV-J title change and language audit are acknowledged. GPT: "You mostly do this correctly." Claude: "The paper acknowledges this (Table IX, Section V-A)."
3. **<1% of operational time arithmetic** — Claude validates: "the stress-case η_S ≈ 46% is properly contextualized as episodic (<1% of operational time), with the time-weighted annual average of 5.6%." GPT: "You now state that the stress case is episodic (<1%), which is good."
4. **Dual coherence-regime recommendation** — Claude: "Present the dual coherence-regime recommendation more prominently (it is currently buried)." Acknowledged as existing but wants elevation. GPT doesn't raise this separately.
5. **Model C coupling result** — Added "24 kbps infeasible regardless of ARQ; 30 kbps supports M_r = 1 with 2.9% margin; 35 kbps with 18.8%." No reviewer specifically flagged this as incomplete anymore.
6. **γ₃₅ in notation table** — No reviewer flagged missing γ₃₅ anymore.
7. **Table V "stagger" footnote** — No reviewer flagged the "—" ambiguity anymore.

## Gemini Detail (Stable 2M/4m)

Resolved from CW:
- CW Major #1 (RF-backup ConOps) → Dropped

Persistent:
- CX Major #1 (1 kbps vs 35 kbps clarification) — Wants "time-averaged per-node traffic allocation" vs "burst-rate coordinator ingress requirement" in abstract
- CX Major #2 (R=3 spatial reuse) — Wants sensitivity sentence for R=7

Minors: α_RX derived nature, Fig 4 legend, §IV-J "Note:" cue for rate paradox, Eq 5 ceiling brackets

## Major Issues Remaining

### Priority 1: d Realism (GPT #1 — PERSISTENT)
**GPT Major #1.** Wants quantitative derivation: orbit-raising → commands/day → implied d. Wants sensitivity plot η vs (d, L_on). The existing Table VIII mapping and empirical anchoring are insufficient; wants one worked operational example with arithmetic.

### Priority 2: γ Role Clarification (GPT #2, #3, Claude #3 — PERSISTENT/STRUCTURAL)
**GPT Major #2/3, Claude Major #3.** Still sees "three-layer" framing despite text never saying "three-layer." The issue is that γ is presented both as a "unit conversion" and as a "model of per-slot time overhead that changes schedulability." Wants: γ is not a layer but a parameter linking Test A bytes to Test B time. Remove "MAC efficiency" as separate concept.

### Priority 3: ARQ Reserved vs Stochastic (GPT #4 — NEW)
**GPT Major #4.** The paper mixes "reserved M_r worst-case slots" (Algorithm 1) with "expected GE demand ~726 ms" (narrative). Wants one consistent metric: deadline miss probability under a defined policy.

### Priority 4: DES Value (GPT #5, Claude #2 — PERSISTENT STRUCTURAL CEILING)
**GPT Major #5, Claude Major #2.** Both want either additional burst model or DES demoted to appendix/paragraph. Claude: "Approximately 2 pages devoted to DES that add little."

### Priority 5: §IV-J Validation Language (GPT #6 — PERSISTENT)
**GPT Major #6.** Wants "parameter plausibility bound" instead of anchoring. Also wants discussion of what transfers from DVB-RCS2 to ISL and what doesn't.

### Priority 6: γ Measurement Recipe (GPT #7 — PERSISTENT)
**GPT Major #7.** Wants uncertainty propagation example: if T_acq = 5±2 ms and T_guard = 4.7±1 ms, what is γ range?

### Priority 7: Circular Validation (Claude #1 — PERSISTENT STRUCTURAL CEILING)
**Claude Major #1.** Wants prominent caveat box in conclusion, consolidated sensitivity table, and reframing as "design methodology" paper.

### Priority 8: Fleet-Level Claims (Claude #4, Gemini #2 — PERSISTENT)
**Claude Major #4, Gemini Major #2.** Both want either fleet-level analysis or scope restriction. Claude suggests title change.

### Priority 9: GE Structural Assumptions (Claude #5 — EVOLVED)
**Claude Major #5.** The dual coherence-regime text exists but is "buried." Wants it elevated to a key finding. Suggests 30 kbps as primary recommendation with 35 kbps as conservative option.

## Minor Issues (25 total)

### Gemini (4 minor)
1. α_RX derived nature clarity in table
2. Fig 4 Bernoulli/ON-OFF legend distinction
3. §IV-J rate paradox "Note:" cue
4. Eq 5 ceiling bracket consistency

### GPT (7 minor)
1. η "beyond baseline" vs "protocol overhead" phrase consistency
2. T_cmd Model C consistency in stagger equations
3. Table III AoI P99 footnote (no deadline misses assumption)
4. Fleet reuse f_RF ≤ 1.2% arithmetic
5. ACK mini-slot timing diagram
6. Link budget "max >200 kbps" assumptions
7. Citation hygiene (non-archival refs)

### Claude (14 minor)
1. Abstract parenthetical density
2. Table I γ values belong in results
3. Eq 1 Model S before Model C ordering
4. Coordinator summary 371B metadata
5. Table V ACK mini-slot footnote → main text
6. Fig 2 analytical vs DES distinction
7. β parameterization self-reference
8. f_decision,max ≈ 24 derivation
9. Table VIII CA row d=1.0 misleading
10. T_framing FEC encoding inconsistency
11. Reference [47] self-cite
12. Eq gamma_time shorthand
13. Thundering herd footnote → main text
14. Fig 1 architecture diagram reference

## Progress Trajectory

| Version | Gemini | GPT | Claude |
|---------|--------|-----|--------|
| CJ | Accept w/ Minor (3M/4m) | Major (7M/8m) | Major (5M/12m) |
| CK | Accept w/ Minor (3M/5m) | Major (7M/7m) | Major (5M/13m) |
| CL | Accept w/ Minor (2M/3m) | Major (9M/8m) | Major (5M/11m) |
| CM | Accept w/ Minor (3M/4m) | Major (8M/7m) | Major (5M/12m) |
| CN | Accept w/ Minor (3M/4m) | Major (7M/10m) | Major (5M/12m) |
| CO | Accept w/ Minor (3M/5m) | Major (7M/7m) | Major (5M/12m) |
| CP | Accept w/ Minor (3M/5m) | Major (6M/10m) | Major (5M/12m) |
| CQ | Accept w/ Minor (3M/5m) | Major (7M/7m) | Major (5M/14m) |
| CR | Accept w/ Minor (2M/4m) | Major (8M/10m) | Major (4M/12m) |
| CS | Accept w/ Minor (3M/4m) | Major (6M/7m) | Major (5M/12m) |
| CT | Accept w/ Minor (3M/5m) | Major (7M/7m) | Major (5M/14m) |
| CU | Accept w/ Minor (3M/5m) | Major (7M/10m) | Major (5M/12m) |
| CV | Accept w/ Minor (3M/4m) | Major (6M/7m) | Major (5M/12m) |
| CW | Accept w/ Minor (2M/4m) | Major (7M/8m) | Major (5M/14m) |
| **CX** | **Accept w/ Minor (2M/4m)** | **Major (7M/7m)** | **Major (5M/14m)** |

**Assessment:** Stable. Gemini holds at 2M. GPT improved slightly (8m→7m minors). Claude stable.

## Structural Ceiling Analysis

GPT and Claude have been at 5-7 majors for 15 versions (CJ–CX). The remaining majors fall into three categories:

**Category A: Achievable via text edits (diminishing returns)**
- γ role clarification (Priority 2) — can add one more clarifying sentence
- ARQ reserved vs stochastic (Priority 3) — can add explicit policy definition
- §IV-J language (Priority 5) — can tighten further
- 1 kbps vs 35 kbps framing (Gemini #1) — can rephrase in abstract

**Category B: Requires new content but no new simulations**
- d operational derivation (Priority 1) — could add one worked orbit-raising example
- γ uncertainty propagation (Priority 6) — could add ±range calculation
- Dual coherence-regime elevation (Priority 9) — structural rewrite

**Category C: Requires new work outside tex file**
- NS-3 validation (Claude #1, GPT #5)
- Alternative DES burst model (GPT #5, Claude #2)
- Fleet interference analysis (Claude #4, Gemini #2)
- Hardware γ measurement

**Recommendation for CY:** Focus on Category A (text clarity) and one Category B item (d derivation with orbit-raising worked example) to attempt to move GPT to 6M. Claude's structural concerns (circular validation, DES value, fleet-level) require Category C work and are unlikely to change with text edits.

## Recommended Strategy for CY

### Achievable via Text Edits

1. **γ is a parameter, not a layer** — Add after boxed definition: "γ is a parameter within Test B that maps information bytes to airtime; it is not a separate feasibility layer. The heuristic R_PHY,min ≥ C_info/(γ·α_RX) is a rearrangement of Test B for quick screening."

2. **ARQ policy definition** — Add: "Algorithm 1 uses worst-case reserved M_r slots per node per cycle (deterministic provisioning). The 'GE demand ~726 ms' (Section IV-C) is the expected additional airtime under stochastic arrivals—a different metric. Under deterministic provisioning: 30 kbps has 656 ms available vs 726 ms demand (marginally infeasible); 35 kbps has 1,880 ms (comfortably feasible)."

3. **1 kbps vs 35 kbps abstract reframe** — Change "1 kbps" references in abstract to "time-averaged per-node traffic allocation" and "burst-rate coordinator ingress" for 35 kbps.

4. **DVB-RCS2 transferability note** — Add: "What transfers from DVB-RCS2 to ISL: preamble/guard/FEC overhead structure. What does not: propagation environment, Doppler dynamics, terminal class, acquisition architecture."

5. **γ uncertainty range** — Add: "If T_acq = 5±2 ms and T_guard = 4.7±1 ms: γ₃₀ ∈ [0.72, 0.78]; R_PHY,min ∈ [26, 28] kbps. The 35 kbps recommendation absorbs this uncertainty."

6. **d orbit-raising worked example** — Add: "Orbit-raising: 4 burns/orbit × 16 orbits/day × 2 commands/burn = 128 commands/day. At 10 s cycles: 8,640 cycles/day; p_cmd = 128/8,640 ≈ 0.015. Campaign duration ~30 days of 180-day mission: d = 30/180 ≈ 0.17. Product: d × p_cmd ≈ 0.0025, yielding η_cmd ≈ 10 bps."

7. **Minor batch** — Remove "MAC efficiency" as separate concept language if any exists; Eq 5 ceiling bracket check; version tag.

### Expected Outcome
Gemini likely stable at 2M (1 kbps/R=3 are persistent structural issues). GPT might drop to 6M (d derivation + ARQ clarification + γ role fix address 3 of 7 majors). Claude stable at 5M.
