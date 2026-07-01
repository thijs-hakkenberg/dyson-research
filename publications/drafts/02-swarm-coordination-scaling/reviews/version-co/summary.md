# Version CO Review Summary

## Recommendations

| Reviewer | Recommendation | Change from CN |
|----------|---------------|----------------|
| Gemini 3 Pro | **Accept with Minor Revisions** | Maintained (3M/5m vs 3M/4m) |
| GPT-5.2 | **Major Revision** | Improved (7M/7m vs 7M/10m) |
| Claude Opus 4.6 | **Major Revision** | Improved (5M/12m; clarity 2→4/5) |

## What CO Fixed (Acknowledged by Reviewers)

1. **Rate terminology precision** — Claude: "clearly distinguishes info-rate, PHY-rate, γ, and half-duplex partitioning α_RX"; GPT: no longer lists rate terminology as major issue (was CN #1 CRITICAL)
2. **Paper length/clarity** — Claude: clarity 4/5 (was 2/5 in CN!); "well-organized with clear roadmap"; "notation table comprehensive"; manuscript length no longer a major issue for ANY reviewer
3. **Single γ equation** — Claude: no longer a major issue (was CN #4); GPT: Eq. 15 acknowledged as "key deliverable"
4. **Screening heuristic removed** — GPT: no longer mentions η_total/γ misuse risk (was CN #4)
5. **Packet-level validation scoped** — Claude: "correctly labels it as parameter anchoring in Table VII"; no longer a major issue (was CN #7)
6. **Superframe timing** — GPT: no longer lists turnaround double-counting as major (was CN #3)
7. **Stress-case pairing** — Gemini: acknowledges episodic framing; Claude: "properly framed as episodic worst-case bound"
8. **Fleet reuse equation** — tautological equation fixed; no longer mentioned

## Major Issues Remaining

### Priority 1: Link/Mode Confusion — 1 kbps vs 35 kbps (ALL THREE REVIEWERS)
**Gemini #1, GPT #1, Claude #4.** The mapping between the 1 kbps per-node budget (traffic allocation within the coordinator's shared channel), the 35 kbps S-band TDMA coordinator channel, and the 2.5 kbps UHF backup is confusing. Table II helps but text still blurs the distinction. Need: (a) a rate-hierarchy figure or diagram; (b) explicit statement that sizing equations apply to S-band coordination channel; (c) consistent terminology pairing.

### Priority 2: γ Worked Examples Beyond Proximity-1 (GPT #7, Claude #2)
Eq. 15 is correct but hard for practitioners to apply without knowing realistic T_acq, T_guard, O_frame ranges for their hardware. Need: 3-4 worked examples spanning S-band/Ka-band/non-CCSDS framing with computed γ and resulting R_PHY,min. The Ka-band footnote is a start but needs expansion.

### Priority 3: DES Value — Buffer Sizing Tables (GPT #5, Claude #1)
DES matches equations by construction. The tail/buffer contribution needs concrete engineering guidance: table of recommended buffer sizes (messages/bytes) for k_c=100, d∈{0.01, 0.10, 0.50}, for <1% overflow, with correlation scope sensitivity.

### Priority 4: Model C vs Model S Residual Confusion (GPT #3)
Table VIII shows 0% misses at 24 kbps for "No Loss" and "GE M_r=0", but Table XIII shows 24 kbps infeasible (negative margin). This is Model S vs Model C, but must be stated explicitly. Add "NOT FOR RECOMMENDATIONS" label to any table/figure using Model S.

### Priority 5: Campaign Duty Factor Realism (GPT #2)
d = 0.10 "conservative default" is still somewhat ad hoc. Need: (a) compact derivation for each row in duty mapping table; (b) at least one heavier-burstiness sensitivity; (c) clearly separate d (commands) from p_exc (telemetry sampling).

### Priority 6: Message-Size Sensitivity (Claude #5 — NEW)
No sensitivity analysis on S_eph, S_cmd. Need: sweep S_eph ∈ {128, 256, 512, 1024} B showing shift in minimum viable PHY rate and η. Straightforward extension.

### Priority 7: Static Cluster Membership Scoping (Claude #3 — NEW)
Re-association 0.014/orbit applies only to Starlink-like Walker. Heterogeneous orbits could have much higher rates. Either restrict applicability or provide parametric expression.

### Priority 8: Two-Layer vs Three-Layer Framing (GPT #4 — NEW)
Eq. 34 (C_raw = C_coord,info/γ) plus superframe checks can be interpreted as two independent constraints when they're not. Need to tighten formalism: Layer 1 = bits/cycle; Layer 2 = time-domain slots. η/γ is intuition only.

### Priority 9: Stress-Case Pairing in Abstract/Conclusion (Gemini #3)
Still want 46% explicitly paired with "5-10% routine" in same sentence in abstract and conclusion. (CO partially does this but can be sharper.)

### Priority 10: §IV-J Title Rename (GPT #6)
Rename to "Standards-based parameter anchoring of γ" and remove/avoid "validation" language.

### Priority 11: γ Sensitivity to Acquisition Time (Gemini #2)
Want a sensitivity plot of γ and min PHY rate vs T_acq. (Fig. margin_sensitivity already does this! Need to reference it more prominently or expand caption.)

### Priority 12: ARQ Conditionality (GPT #7 partial)
ARQ infeasibility at 30 kbps is contingent on specific GE params. Frame more conditionally; provide a small sweep (margin vs p_BG, p_B, M_r).

## Minor Issues (24 total)

### Gemini (5 minor)
1. Table II footnote: move 1 kbps explanation to main text
2. Fig 4: ensure legend clearly distinguishes solid/dashed
3. Eq. 11: define ceiling function notation
4. §IV-J: check "unsubscripted γ" consistency
5. CCSDS citations: verify latest Blue/Green book numbers

### GPT (7 minor)
1. Table VIII vs Table XIII: resolve 24 kbps apparent contradiction (Model C vs S)
2. "RF-backup" vs "coordination channel" terminology consistency
3. AoI P99: note Eq. 19 is upper bound under memoryless sampling
4. 512-B breakdown metadata (371 B) seems large — justify or show sensitivity
5. ACK mini-slots "absorbed within guard" — justify
6. Table VII: add explicit "35 kbps recommendation" row
7. Non-archival references: note as potentially ephemeral

### Claude (12 minor)
1. Abstract: consider removing "Results are preliminary..." (stated in body)
2. Table I: α_RX line reference should be Alg. 1 line 6, not line 5
3. Eq. 2 vs Eq. 15: both define γ; add clearer cross-reference
4. Fig. 4: verify "DES bars" matches figure content (step function?)
5. Thundering herd footnote: units "s⁻¹" — rate vs probability
6. §IV-E: cite specific ESA report section, not just general report
7. Table VI: expand "GE+Exc" header
8. Eq. 6: f_decision not in Table I
9. γ-conditional footnote Ka-band: γ = 0.422 below lookup table range
10. Non-archival refs [3], [48]
11. Authorship: "Project Dyson Research Team" may not comply with IEEE
12. §III-B.2: note single-threaded processing as conservative assumption

## Progress Trajectory

| Version | Gemini | GPT | Claude |
|---------|--------|-----|--------|
| CJ | Accept w/ Minor (3M/4m) | Major (7M/8m) | Major (5M/12m) |
| CK | Accept w/ Minor (3M/5m) | Major (7M/7m) | Major (5M/13m) |
| CL | Accept w/ Minor (2M/3m) | Major (9M/8m) | Major (5M/11m) |
| CM | Accept w/ Minor (3M/4m) | Major (8M/7m) | Major (5M/12m) |
| CN | Accept w/ Minor (3M/4m) | Major (7M/10m) | Major (5M/12m) |
| **CO** | **Accept w/ Minor (3M/5m)** | **Major (7M/7m)** | **Major (5M/12m)** |

**Assessment:** Major breakthrough on clarity — Claude's clarity rating jumped 2→4/5, the single most persistent complaint across all versions. Paper length no longer an issue for any reviewer. Rate terminology audit (CN's #1 critical) fully resolved. GPT minor count dropped 10→7.

The reviews now converge on a clearer set of remaining issues:

1. **LINK/MODE DIAGRAM** (all three): Simple rate-hierarchy figure resolving 1 kbps / 35 kbps / 2.5 kbps confusion
2. **γ WORKED EXAMPLES** (GPT + Claude): Expand beyond Prox-1 to 3-4 hardware cases
3. **BUFFER SIZING TABLE** (GPT + Claude): Translate DES tails to concrete buffer recommendations
4. **MODEL C/S LABELS** (GPT): Explicit labels on every table/figure
5. **MESSAGE-SIZE SENSITIVITY** (Claude): Straightforward S_eph sweep

## Recommended Strategy for CP

### Priority Edits (addressing cross-reviewer convergence)

1. **Add rate-hierarchy figure** — Simple TikZ/table showing: UHF backup (2.5 kbps, survival only) → S-band TDMA (35 kbps, coordination) → Optical ISL (≥1 Gbps, bulk data). Per-node 1 kbps allocation shown within S-band channel. ~8 lines. Addresses Priority 1.

2. **Add γ worked examples** — Expand footnote to proper subsection with 3 worked examples: (i) Prox-1 baseline (already present), (ii) Ka-band continuous tracking (low T_acq, high rate), (iii) non-CCSDS proprietary frame. Show computed γ and resulting PHY recommendation. ~15 lines. Addresses Priority 2.

3. **Add buffer sizing table** — k_c=100, d∈{0.01, 0.10, 0.50}, Bernoulli vs ON/OFF vs cluster-correlated: recommended buffer size (messages) for <1% overflow. ~10 lines. Addresses Priority 3.

4. **Add Model C/S labels** — Add explicit "(Model C)" or "NOT FOR RECOMMENDATIONS" to Table VIII caption and any figure using Model S. Fix Table VIII vs Table XIII apparent contradiction with explicit note. ~5 lines. Addresses Priority 4.

5. **Add message-size sensitivity** — Compact table: S_eph ∈ {128, 256, 512, 1024} → C_coord,info → min PHY rate → η. ~8 lines. Addresses Priority 6.

6. **Rename §IV-J** — "Standards-Based Parameter Anchoring" (remove "validation"). ~1 line. Addresses Priority 10.

7. **Scope static membership** — Add sentence restricting applicability to "co-planar or near-co-planar constellations." ~2 lines. Addresses Priority 7.

8. **Tighten Layer 1/2 definitions** — Move Eq. 34 to "useful conversion" box. Rename to "byte-feasibility + schedule-feasibility." ~3 lines. Addresses Priority 8.

### Cuts to Offset Additions (~40-50 lines)
- Compress topology comparison to 2 sentences (currently 3 sentences)
- Compress AoI mission coupling paragraph
- Compress GNSS denial paragraph
- Compress thundering herd footnote further
- Remove redundant "24 infeasible, 30 minimum, 35 recommended" restatements beyond 3 occurrences

### Net Target: ~1040-1060 lines / 12 pages
