# Version CN Review Summary

## Recommendations

| Reviewer | Recommendation | Change from CM |
|----------|---------------|----------------|
| Gemini 3 Pro | **Accept with Minor Revisions** | Maintained (3M/4m vs 3M/4m) |
| GPT-5.2 | **Major Revision** | Improved (7M/10m vs 8M/7m) |
| Claude Opus 4.6 | **Major Revision** | Maintained (5M/12m vs 5M/12m) |

## What CN Fixed (Acknowledged by Reviewers)

1. **GE as design assumption** — Claude: "correctly framed as design assumption"; GPT: "appropriate"; stated in abstract and conclusion
2. **γ_time promoted as primary** — Claude: "time-domain form is cleaner and preferred"; GPT: "Eq. 17 is good"
3. **Deep-space claim removed** — Claude: no longer lists this as issue
4. **Conditional PHY recommendation** — GPT: "useful"; Gemini: γ-conditional table noted positively
5. **Contention margin analysis** — Claude: no longer lists MAC contention as top issue; GPT acknowledges
6. **DES tail claims scoped** — GPT: "appropriate"; Claude: "honestly characterized in places"
7. **Ingress/egress dependency map** — GPT: "strength"; clearly separates ingress (k_c, γ) from egress (d, q)
8. **Formal superframe segments** — GPT: "improvement"; five-segment ordering defined
9. **d sensitivity** — GPT: "clear improvement"; 60× gap justified
10. **Model C enforcement** — GPT: "correctly separate"; Claude: notes Model S properly relegated
11. **N_R defined** — No longer an issue
12. **Thundering herd BEB params** — Gemini: no longer top concern; GPT: minor placement issue
13. **Stress-case terminology standardized** — No longer mentioned

## Major Issues Remaining

### Priority 1: Rate Terminology Audit (GPT #1 — NEW, CRITICAL)
Abstract/conclusion say "requires ≈27 kbps (info-rate) at γ≈0.76" which is wrong by definition. Should be: ~20.3 kbps info-rate; ~26.7 kbps PHY-rate (before half-duplex); ~29.9 kbps after α_RX. Need: (a) boxed glossary: C_coord,info vs R_PHY,raw vs R_PHY,min; (b) fix abstract/conclusion wording; (c) audit all rate references.

### Priority 2: Manuscript Length 30-40% Reduction (Claude #3 — ESCALATED)
Claude rates Clarity 2/5 ("most significant weakness"). Paper is "approximately 2× typical length for IEEE T-AES." Key results restated 5-8 times. Specific cuts: (a) consolidate Model S to single paragraph; (b) merge Tables 6/7/8/9; (c) move thundering herd, GNSS denial, fleet reuse to appendix/supplementary; (d) reduce DES to ~1 page; (e) shorten packet-level validation to ~0.5 pages.

### Priority 3: Superframe Timing Consistency (GPT #6 — NEW)
ACK mini-slot "absorbed within guard" is a strong assumption — guard is for timing uncertainty, not protocol signaling. Turnaround may be double-counted: 4.7 ms guard + separate "turnaround ×2 = 4 ms" in superframe table. Ranging (50 ms) frequency unclear. Need: (a) justify ACK-in-guard or add explicit ACK line; (b) resolve turnaround double-counting; (c) provide two budgets: minimal and conservative.

### Priority 4: Screening Heuristic Misuse Risk (GPT #4)
η_total/γ conflates message-layer with airtime under assumptions that may not hold. Likely to be copied into spreadsheets and misapplied. Either: (a) remove entirely; (b) redefine as separate uplink/downlink airtime fractions with validity conditions.

### Priority 5: DES Coverage Reduction (Claude #2, GPT #5)
DES implements same equations, achieves <0.1% agreement — code verification only. Buffer sizing (1.15× mean) is sole incremental value. Claude wants ~1 page total. GPT wants concrete engineering decision: choose target overflow probability, compute required buffer, show resulting drop probability difference vs analytic bound.

### Priority 6: Single γ Equation (Claude #4)
Claude: "Present Eq. 17 as primary. Relegate Eq. 18 to footnote or appendix. Remove Eq. 14 entirely." CN promoted Eq. 17 but still has Eq. 18 and the multiplicative decomposition. Need to cut further.

### Priority 7: Packet-Level Validation Reduction (Claude #5, GPT #6)
Claude: "Shorten to ~0.5 pages. State clearly: 'We derive γ from CCSDS Proximity-1 framing; this anchors the parameter value but does not validate the sizing framework.'" Not independent validation — deterministic accounting tool.

### Priority 8: γ Cross-Check Consistency (GPT #2)
Some derived quantities may mix Model C/S assumptions. "Ingress 11,435 ms at 24 kbps" vs "11,108 ms" in table — reconcile. Need single authoritative timing component table for 24/30/35 kbps under Model C only.

### Priority 9: No External Validation (Claude #1 — PERSISTENT)
Complete absence of comparison with operational ISL data, NS-3, or hardware. Framework's predictive accuracy entirely unknown. At minimum: compare γ against published DVB-RCS2 slot efficiency measurements. Cannot be fully resolved without external data but can be further right-sized.

### Priority 10: Stress-Case Contextualization (Gemini #1, GPT #3)
Abstract/conclusion still feature 46% prominently. Pair with "episodic worst-case" and contrast with routine 5-9%. Separate figure showing routine vs peak across d ∈ [10⁻³, 10⁻¹].

### Priority 11: 1 kbps Survival Mode Argument (Gemini #2)
Strengthen: "hierarchical coordination must be invariant to optical link failure." If control plane depends on Gbps optical, swarm becomes uncontrollable when most vulnerable.

### Priority 12: Unicast Stagger Operational Concept (Gemini #3)
190s (or 310s) unicast latency — explicitly state safety-critical commands use broadcast (single-cycle), unicast only for non-urgent (orbit raising, software updates).

### Priority 13: γ Guidance for Non-Proximity-1 ISLs (GPT #7)
Add "How to instantiate γ for your modem" with 2-3 worked examples: (i) Proximity-1 baseline, (ii) continuous-tracking TDMA, (iii) non-CCSDS proprietary frame.

## Minor Issues (22 total)

### Gemini (4 minor)
1. α_RX rate-dependence: note in Table IV footnote that α_RX changes slightly with PHY rate
2. Fig 6 B&W: ensure DES bars vs analytical lines distinguishable in monochrome
3. Rate-1/2 LDPC: briefly state why it makes 30 kbps infeasible (doubles symbol time)
4. Typos: triple fault per-cluster vs fleet-wide; "Practitioners evaluate" → "must evaluate"

### GPT (10 minor)
1. Abstract: replace "requires ≈27 kbps (info-rate)" with correct terminology
2. Notation table: distinguish C_coord,info vs R_PHY in symbol list
3. Eq. labeling: rename C_raw to R_PHY,eff
4. Guard time: clarify 2 ms turnaround is one-way or round-trip (potential double-count with "turnaround ×2 = 4 ms")
5. Ingress numbers: reconcile 11,435 ms vs 11,108 ms
6. AoI: clarify service-time assumptions for "mean AoI ≈ T_c/2"
7. Fleet reuse: T_c^fleet = max(T_c, G·T_c) is tautological; use G·T_c when G>1
8. Thundering herd: feels disconnected; move to appendix unless used for margin sizing
9. Reference quality: minimize non-archival web references
10. Typographic: ensure fig-unicast-stagger.pdf extension consistent

### Claude (12 minor)
1. Table 1: γ₂₄, γ₃₀ are computed results, not notation — move to results
2. Eq. 1: byte-domain version of M_total would be more useful
3. Section III-B-2: compound probability units (s⁻¹) — rate or probability?
4. Fig. 2: ensure both panels clearly labeled and caption matches
5. Table 3: "screening notifications" vs "priority alerts" — clarify semantics
6. Section IV-A: n_clusters vs k_r relationship not explained
7. Eq. 10: Raft parallel RPCs vs serialized assumption — justify
8. Table 6: "GE+Exc" header cryptic — spell out
9. 60× gap: justify why 60× rather than 10×
10. Non-archival references: [3] Kuiper, [17] DARPA OFFSET
11. Abstract: 150+ words, dense; p_BG sentence belongs in body
12. "Complete situational awareness loss" in I-C not fully supported

## Progress Trajectory

| Version | Gemini | GPT | Claude |
|---------|--------|-----|--------|
| CJ | Accept w/ Minor (3M/4m) | Major (7M/8m) | Major (5M/12m) |
| CK | Accept w/ Minor (3M/5m) | Major (7M/7m) | Major (5M/13m) |
| CL | Accept w/ Minor (2M/3m) | Major (9M/8m) | Major (5M/11m) |
| CM | Accept w/ Minor (3M/4m) | Major (8M/7m) | Major (5M/12m) |
| CN | **Accept w/ Minor (3M/4m)** | **Major (7M/10m)** | **Major (5M/12m)** |

**Assessment:** Gemini stable at Accept w/ Minor. GPT improved 8→7 major but gained 3 minor (rate terminology audit surfaced). Claude stable at 5M/12m with clarity now rated 2/5 (escalated concern).

**Key insight for CO:** The reviews converge on TWO critical meta-issues that, if addressed, would resolve the majority of individual complaints:

1. **PAPER LENGTH** (Claude #3, implicit in GPT #5/#7): The paper is 15 pages / ~1157 lines. Claude explicitly says "2× typical" and wants 30-40% reduction. This single change would address: (a) DES over-coverage, (b) packet-level validation over-coverage, (c) redundant restatements, (d) Model S clutter, (e) notation overload. Target: ≤10 pages / ~850 lines.

2. **RATE TERMINOLOGY PRECISION** (GPT #1): The "27 kbps info-rate" error in abstract/conclusion undermines the entire rate ladder. Fixing this with a clear glossary would simultaneously address: (a) GPT #2 (γ cross-check), (b) GPT #3 (turnaround), (c) GPT minor #1-#5, (d) Claude minor #1-#2.

## Recommended Strategy for CO

**Aggressive compression** targeting 10-page limit:

### Cut List (targeting ~300 line reduction)
1. Remove Eq. 14 (multiplicative decomposition) and Eq. 18 (bit-domain γ) entirely — keep only Eq. 17 (γ_time). Save ~15 lines.
2. Remove η_total/γ screening heuristic — causes confusion, non-binding anyway. Save ~8 lines.
3. Remove Table capability_matrix (topology comparison) — replace with 2 sentences. Save ~18 lines.
4. Remove Table link_availability — covered by analytical equations. Save ~20 lines.
5. Compress DES section to 1 page: mean verification (1 sentence) + buffer CDF figure + 1.15× guideline + concrete overflow example. Save ~30 lines.
6. Compress packet-level validation to 0.5 pages: γ derivation statement + Table decomposition + 1 sentence scope. Save ~20 lines.
7. Remove Fig workload-comparison (shows flat lines = scale-invariance). Save ~6 lines.
8. Consolidate all Model S material to single sentence + Table row. Save ~10 lines.
9. Move thundering herd analysis to footnote (3 lines max). Save ~8 lines.
10. Move fleet reuse to footnote or cut entirely. Save ~10 lines.
11. Compress related work by 50%. Save ~6 lines.
12. Compress abstract to ≤150 words. Save ~5 lines.
13. Remove GNSS denial sensitivity if present. Save ~5 lines.
14. Merge feasibility tables (schedulability + duty factor → single table). Save ~15 lines.
15. Compress AoI section. Save ~8 lines.

### Add List
1. Boxed rate glossary: C_coord,info / R_PHY,raw / R_PHY,min (3 lines)
2. Fix abstract/conclusion rate terminology (net 0 lines)
3. Superframe timing: resolve turnaround/guard/ACK accounting (net +2 lines for clarity)
4. Stress-case: pair 46% with "episodic" in abstract/conclusion (net 0)
5. 1 kbps survival mode sentence (1 line)
6. Unicast safety-critical broadcast statement (2 lines)
7. DES concrete buffer sizing example (3 lines)

**Net estimated reduction: ~170-180 lines → target ~980 lines / ~11 pages**
