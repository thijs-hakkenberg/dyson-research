# Version DK Review Summary

## Recommendations

| Reviewer | Recommendation | Change from DJ |
|----------|---------------|----------------|
| Gemini 3 Pro | **Accept with Minor Revisions** | Stable (3M/5m→3M/5m) |
| GPT-5.2 | **Major Revision** | Improved majors (8M/8m→7M/10m) |
| Claude Opus 4.6 | **Major Revision** | Stable majors (5M/10m→5M/12m) |

## What DK Fixed (Acknowledged by Reviewers)

1. **Aggressive compression to 12 pages** — Gemini Clarity improved to 5/5 (Excellent). Claude DJ #4 (paper too long) RESOLVED.
2. **Contention factor ρ_MAC placeholder** — GPT DJ #4 (MAC efficiency naming) partially resolved; GPT still wants framework figure.
3. **Thermal/power sizing distinction** — Gemini DJ #1 partially addressed; Gemini DK #1 still wants sharper stress-case contextualization.
4. **Polar convergence limitation** — Gemini DJ #3 (fleet interference) RESOLVED as separate major; absorbed into GPT DK #7.
5. **η_0 invariance softened** — Claude minor RESOLVED.
6. **Model S/C mnemonics** — Claude minor RESOLVED.
7. **Stress-case 46% consistent labeling** — GPT DJ #3 (stress-case still risks "typical") RESOLVED.
8. **Practitioner measurement protocol compressed** — GPT DJ #8 RESOLVED.

## What PERSISTS (Structural Barriers)

Three issues persist across ALL reviews and appear unfixable via text edits alone:

1. **No external validation** (Claude #3, GPT implicit) — Cannot be fixed without NS-3 or hardware measurements.
2. **DES/packet-level provide limited independent value** (Claude #1/#2, GPT #4/#5) — Fundamental issue: shared equations. Can only mitigate by further reducing prominence.
3. **GE model lacks empirical grounding** (GPT #6) — Cannot be fixed without ISL channel measurements.

## Gemini: Stable (3M/5m→3M/5m)

DJ→DK resolved:
- DJ #2 (unicast latency operational acceptability) → NOT RE-RAISED. RESOLVED.
- DJ #3 (fleet interference at poles) → polar convergence note added; NOT RE-RAISED. RESOLVED.

DJ→DK persistent:
- DJ #1 (stress-case thermal/power) → DK #1 (persists, wants sharper distinction spectrum vs energy dimensioning)

New:
- DK #2: T_acq sensitivity — wants specific R_PHY recommendation for slow hardware (T_acq > 10ms)
- DK #3: 1 kbps logical vs physical confusion — wants explicit "traffic policing policy" statement

## GPT: Improved (8M/8m→7M/10m)

DJ→DK resolved:
- DJ #3 (stress-case 46% still risks "typical" reading) → RESOLVED (consistent labeling + thermal/power note)
- DJ #8 (practitioner measurement protocol) → RESOLVED (compressed protocol accepted)

DJ→DK persistent (6 of 8 DJ majors persist):
- DJ #1 (d under-justified) → DK #2 (campaign duty factor — wants 2-3 traceable mission archetypes)
- DJ #2 (γ unification fragile) → DK #3 (γ/ACK consistency — wants timing ledger table)
- DJ #4 (MAC efficiency framework) → DK #1 (three-layer framework — wants figure showing Test A/B/γ)
- DJ #5 (DES self-confirmation) → DK #4 (DES verification — wants alternative burst model)
- DJ #6 (packet-level not validation) → DK #5 (packet-level — wants falsification conditions)
- DJ #7 (GE/ARQ coherence) → DK #6 (GE/ARQ — wants design decision chart)

New:
- DK #7: Fleet-level reuse R=7 — wants sensitivity table or explicit scope-down

Net: 8M - 2 resolved + 1 new = 7M. Minors regressed 8→10 (compression removed tabular context).

## Claude: Stable majors, minors regressed (5M/10m→5M/12m)

DJ→DK resolved:
- DJ #4 (paper too long/repetitive) → RESOLVED by compression to 12 pages
- DJ #5 (γ is standard) → evolved into DK #4 (γ domain of validity — different focus)

DJ→DK persistent:
- DJ #1 (DES limited value) → DK #1 (same)
- DJ #2 (packet-level not independent) → DK #2 (same)
- DJ #3 (no external validation) → DK #3 (same)

New/evolved:
- DK #4 (γ domain of validity) — wants applicability conditions for Eq. 7
- DK #5 (coordinator failure transient) — wants analysis of joint election + status traffic

Minor count regressed 10→12: compression removed contextual clarity.

## Progress Trajectory

| Version | Gemini | GPT | Claude |
|---------|--------|-----|--------|
| DH | Accept w/ Minor (2M/4m) | Major (6M/7m) | Major (5M/10m) |
| DI | Accept w/ Minor (3M/4m) | Major (8M/10m) | Major (5M/12m) |
| DJ | Accept w/ Minor (3M/5m) | Major (8M/8m) | Major (5M/10m) |
| **DK** | **Accept w/ Minor (3M/5m)** | **Major (7M/10m)** | **Major (5M/12m)** |

GPT showed first improvement in 4 versions (7M, lowest since DH's 6M). Compression strategy is working.

## Analysis: What Moved GPT

GPT dropped 8M→7M. Key factors:
1. Stress-case labeling + thermal/power note resolved DJ #3
2. Compressed measurement protocol resolved DJ #8
3. Fleet reuse elevated as new DK #7

GPT's remaining 7 majors break down:
- 3 structural (DES #4, packet-level #5, GE #6) — need external validation/measurements
- 2 presentation (framework figure #1, timing ledger #3) — TEXT-FIXABLE
- 2 content (mission archetypes #2, fleet reuse #7) — TEXT-FIXABLE

**4 of 7 GPT majors are text-fixable.** Resolving them could push GPT to 3M structural only.

## Analysis: Claude's Path

Claude's 5 majors:
- 3 structural (DES #1, packet-level #2, no external validation #3) — UNFIXABLE by text
- 2 text-fixable (γ domain #4, coordinator transient #5)

Resolving text-fixable items → 3M structural only.

## Strategy for Version DL

### Priority 1: γ Timing Ledger Table (GPT #3, Claude #4 partial)
Single authoritative table: per-rate payload bits, framing, FEC, preamble, acquisition, guard, turnaround, ACK — each marked "in γ" or "outside γ / in Test B." ~10 lines.

### Priority 2: Falsification Conditions Paragraph (GPT #5, Claude #3 partial)
"What would falsify our conclusion?" — if T_acq P95 > 25ms, turnaround > 10ms, γ reduced by > 0.1. ~4 lines.

### Priority 3: γ Domain of Validity (Claude #4)
Applicability conditions for Eq. 7: single-packet-per-slot, cold-start per slot, LDPC FEC entire frame, CCSDS Proximity-1. ~4 lines.

### Priority 4: Coordinator Failure Transient (Claude #5)
Status reporting suspended during elections; quantify AoI impact (+14-16 cycles). ~3 lines.

### Priority 5: 1 kbps Traffic Policing (Gemini #3)
"1 kbps is a traffic policing policy enforced by the scheduler, not a hardware limit." 1 line.

### Priority 6: Section IV-J Rename (Claude #2, GPT #5)
"Standards-Based Parameterization" — drop "validation" language. 0 net lines.

### Priority 7: T_acq Slow Hardware (Gemini #2)
"For T_acq > 10ms: R_PHY ≥ 40 kbps recommended." 1-2 lines.

### Priority 8: ARQ Design Trade (GPT #6)
Brief M_r=0/1/2: M_r=0 → inter-cycle recovery, +1 cycle AoI penalty; M_r=2 → doubles ARQ, tightens TDMA. ~4 lines.

### Priority 9: Fleet Reuse Scope-Down (GPT #7)
"R=7 placeholder pending RF simulation; if R=5, G increases 40%." ~2 lines.

### Priority 10: Tab Label Fix (GPT minor #1)
Convert remaining \label{tab:} on inline paragraphs to proper formatting.

### Priority 11: Stress-Case Power Budget (Gemini #1)
Sharpen existing thermal/power note. 1 line.

### Deferred (Structural)
- NS-3 external validation (Claude #3, GPT implicit)
- DES independence (Claude #1, GPT #4)
- GE empirical grounding (GPT #6)
- Heavy-tailed burst model (GPT #4)

## Text-Fixable Items for DL

1. γ timing ledger table — ~10 lines
2. Falsification conditions — ~4 lines
3. γ domain of validity — ~4 lines
4. Coordinator failure transient — ~3 lines
5. 1 kbps traffic policing — 1 line
6. Section IV-J rename — 0 net lines
7. T_acq slow hardware — 1-2 lines
8. ARQ design trade — ~4 lines
9. Fleet reuse scope-down — ~2 lines
10. Stress-case power budget — 1 line
11. Tab label fix — edits only
12. Version tag → paper-02-v-dl
