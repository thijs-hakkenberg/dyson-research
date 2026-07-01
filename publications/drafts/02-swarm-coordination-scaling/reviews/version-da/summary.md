# Version DA Review Summary

## Recommendations

| Reviewer | Recommendation | Change from CZ |
|----------|---------------|----------------|
| Gemini 3 Pro | **Accept with Minor Revisions** | Improved (3M/5m→2M/5m) |
| GPT-5.2 | **Major Revision** | Regressed (7M/8m→7M/10m) |
| Claude Opus 4.6 | **Major Revision** | Stable (5M/12m→5M/12m) |

## What DA Fixed (Acknowledged by Reviewers)

1. **R=3 spatial reuse link budget** — Gemini: No longer raises R=3 as a major issue (was Major #3 in CZ). The back-of-envelope C/I calculation (26 dB > 20 dB required) resolved the persistent Gemini concern. GPT minor #6 notes it's "helpful but optimistic" (single interferer); Claude #4 acknowledges but wants multi-interferer analysis.
2. **Acquisition-mode table** — GPT: "The 'how to measure γ on the bench' procedure [is needed]" — acknowledges the multi-mode table but wants it extended to a measurement recipe. Gemini doesn't re-raise the T_acq sensitivity as a major.
3. **S-band link budget table** — Claude: "The 1 kbps per-node budget is derived from a link budget (Table VII)" — acknowledges the table exists but questions its assumptions. GPT minor #9 wants aggregate capacity calculation shown more explicitly.
4. **GE reframe as sensitivity tool** — Claude: "the paper acknowledges this ('a direct consequence of the per-cycle GE coherence assumption, not an emergent finding')" — the reframe was noticed. Both Claude and GPT still want further de-emphasis of the unconditional 35 kbps recommendation.
5. **RF-backup recovery justification** — Gemini: Major #2 now asks for UHF election convergence rigor (evolved from ConOps contradiction). The "time-critical because safe-hold lacks collision avoidance" explanation partially addressed the concern.

## Gemini Improvement Detail (3M→2M)

CZ→DA changes:
- CZ Major #1 (T_acq sensitivity) → **RESOLVED** by acquisition-mode table with breaking points
- CZ Major #2 (RF-backup ConOps) → Persistent as DA Major #2 (evolved: now about BEB convergence rigor)
- CZ Major #3 (R=3 spatial reuse) → **RESOLVED** by link budget calculation
- NEW: DA Major #1 (Doppler range-rate impact on guard time — re-evolved from CY concern)

Net: Two resolved, one re-appeared from CY. Major count improved from 3 to 2.

## GPT Regression Detail (8m→10m)

The α_RX notation table edit introduced a formatting error (extra parenthesis). GPT minor #1 flagged this specifically. Additionally, GPT still finds the "three-layer" narrative despite extensive "Layer→Test" renaming. Two new minors appeared (link budget calculation, referencing).

## Major Issues Remaining

### Priority 1: α_RX Circular Sizing (GPT #1 — PERSISTENT, WORSENED)
GPT: "α_RX is itself a function of R_PHY and the schedule. As written, the heuristic can look like it uses α_RX as an independent constant." The notation table edit introduced a formatting error that made things worse.

**Fix:** Fix the parenthesis error. Simplify: remove the formula from notation table, keep only "computed output of Algorithm 1."

### Priority 2: Two-Test vs Three-Layer (GPT #2 — PERSISTENT)
GPT: "narrative repeatedly introduces MAC efficiency as if it were a separate feasibility layer/check."

**Fix:** Audit for any remaining "MAC efficiency" language. May be unfixable at this point — GPT consistently interprets the γ conversion discussion as implying a third layer.

### Priority 3: Circular Validation (Claude #1 — PERSISTENT STRUCTURAL)
Claude: "the paper has no independent validation of any kind." Requires NS-3 or external benchmarking — not text-fixable.

### Priority 4: GE Predetermined Findings (GPT #4, Claude #2 — PERSISTENT)
Both want coherence regime as primary design variable. The reframe from "recommendation" to "sensitivity" was noticed but deemed insufficient.

### Priority 5: Doppler Range-Rate (Gemini #1 — RE-EVOLVED)
Gemini now asks about range-rate impact on slot timing, not just frequency offset. Wants max ρ̇ × T_slot calculation.

### Priority 6: Raft Election Convergence (Gemini #2 — PERSISTENT)
Wants more rigorous BEB convergence justification for N=100.

### Priority 7: DES Value (GPT #5, Claude #3 — PERSISTENT)
Both want DES contribution consolidated or expanded with non-tautological content.

### Priority 8: Model S Misinterpretation Risk (GPT #3 — PERSISTENT)
Wants Model S compressed to appendix or ARQ coupling table replicated under Model C.

### Priority 9: Workload d Realism (GPT #4 — PERSISTENT)
Wants fully specified mission-phase workload trace.

### Priority 10: Realistic Alternatives (Claude #5 — NEW)
Wants comparison with at least one non-extreme alternative (e.g., gossip-based partial dissemination).

### Priority 11: γ "Validation" Language (GPT #6 — PERSISTENT)
Still finds "validated via CCSDS" phrasing (likely stale concern; text already uses "anchored").

### Priority 12: γ Measurement Recipe (GPT #7 — PERSISTENT)
Wants practitioner bench-measurement procedure.

## Minor Issues (27 total)

### Gemini (5 minor)
1. "Logical" vs "Physical" 1 kbps reiteration
2. α_RX notation density
3. Fig 3 Model S visual de-emphasis
4. f_decision definition (integer vs frequency)
5. "Deficit" vs negative margin wording

### GPT (10 minor — regressed from 8)
1. α_RX notation formatting error (NEW — introduced by DA edit)
2. PHY vs info-rate labeling consistency
3. 371 B metadata justification
4. AoI Bernoulli sampling clarification
5. GE per-slot vs per-cycle note
6. R=3 single-interferer assumption
7. Table VII Model S caption banner
8. Algorithm 1 η₀ self-containment
9. Link budget aggregate capacity calculation (NEW)
10. DAMA/satellite scheduling references (NEW)

### Claude (12 minor — stable)
1. η notation overload
2. α_RX canonical value in notation
3. Eq 1 M_total unused
4. Thundering herd footnote placement
5. Fig 1 placeholder
6. Message size justification placement
7. AoI/TCA conflation
8. Algorithm 1 double-counting check
9. Abstract length
10. Self-citation [55]
11. Sync beacon 8 bits
12. Eq 6 Raft in TDMA

## Progress Trajectory

| Version | Gemini | GPT | Claude |
|---------|--------|-----|--------|
| CW | Accept w/ Minor (2M/4m) | Major (7M/8m) | Major (5M/14m) |
| CX | Accept w/ Minor (2M/4m) | Major (7M/7m) | Major (5M/14m) |
| CY | Accept w/ Minor (3M/4m) | Major (7M/10m) | Major (5M/13m) |
| CZ | Accept w/ Minor (3M/5m) | Major (7M/8m) | Major (5M/12m) |
| **DA** | **Accept w/ Minor (2M/5m)** | **Major (7M/10m)** | **Major (5M/12m)** |

**Assessment:** Gemini improved significantly — R=3 and T_acq concerns resolved. GPT regressed due to α_RX notation error. Claude stable.

## Structural Ceiling Status (Post-DA)

After 18 versions (CJ–DA):
- **Gemini**: Now at 2M/5m (best since CW/CX). Remaining majors: Doppler range-rate (calculable) and Raft convergence (text-arguable). Both are text-fixable.
- **GPT**: Locked at 7M, 8-10m. The α_RX and three-layer issues are persistent despite multiple edit rounds. Core issues require structural reorganization (Model S elimination, feasibility pipeline figure) beyond text tweaks.
- **Claude**: Locked at 5M, 12-14m. Core issues require external work (NS-3, network calculus, alternative architectures).

## Text-Fixable Items for DB

1. **Fix α_RX notation table** — Remove formula, keep "computed output" only. Fixes GPT #1 and GPT minor #1.
2. **Doppler range-rate calculation** — At 500 km, max ρ̇ ≈ 7 km/s for cross-plane links. Timing error = ρ̇/c × T_slot = 7000/(3×10⁸) × 91.7 ms ≈ 2.1 μs ≪ 4.7 ms guard. State this explicitly. Addresses Gemini #1.
3. **Raft BEB convergence strengthening** — Add: "At G=25, P_success ≈ e^{-25} ≈ 10^{-11} per slot; BEB expands window to 64, reducing G to 100/64 ≈ 1.56; P_success = 1.56×e^{-1.56} ≈ 0.33 per slot. Expected rounds to first success ≈ 3." Addresses Gemini #2.
4. **Audit "MAC efficiency" language** — Search for and remove any remaining phrasing that implies MAC efficiency is a separate check. Addresses GPT #2.
5. **Version tag** → paper-02-v-db

## Recommended Strategy

**Apply items 1-5 (targeted text fixes for the two text-fixable Gemini majors and GPT's α_RX error), then evaluate.** If Gemini reaches 1M or 0M, the paper has one strong Accept signal. GPT and Claude's majors are structural and likely require:
- Model S elimination (GPT #3)
- NS-3 simulation (Claude #1)
- Network calculus bounds (Claude #3 constructive suggestion)
- Realistic alternative architecture comparison (Claude #5)

These are beyond text editing scope.
