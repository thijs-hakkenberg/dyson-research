# Version DF Review Summary

## Recommendations

| Reviewer | Recommendation | Change from DE |
|----------|---------------|----------------|
| Gemini 3 Pro | **Accept with Minor Revisions** | Stable (3M/4m→3M/5m) |
| GPT-5.2 | **Major Revision** | Improved (9M/10m→8M/9m) |
| Claude Opus 4.6 | **Major Revision** | Mixed (5M/12m→5M/14m, minors regressed) |

## What DF Fixed (Acknowledged by Reviewers)

1. **Eq. mac_efficiency removed as standalone** — GPT: "you already state in the boxed text" — acknowledges improvement; three-layer issue reduced to #3 (messaging inconsistency only). Claude: "appropriately clarified" — explicitly positive.
2. **R=7 recommended** — GPT: No longer criticizes R=3 as "insufficient." Now says R=7 recommendation is "too thin" — evolved from "wrong" to "under-justified." Gemini: "recommendation for R=7 is based on simple geometric arguments" — wants qualification.
3. **Model C ARQ coupling** — GPT: Not re-raised as major. The explicit Model C results (30 kbps 12% miss, 35 kbps zero miss) were absorbed. GPT instead raises new #6 (ARQ demand derivation).
4. **γ measurement recipe in Design Equations** — GPT: Not re-raised as major. Absorbed.
5. **γ ledger footnote** — GPT: Acknowledges "you partly do this in Table 12 note" but wants full authoritative table. Partial credit.
6. **p_BG ARQ qualification** — Gemini: Still raises (#1) but now wants "per slot" fast-fading analysis, not just statement.
7. **DES further compressed** — Claude: Still raises as #1 but acknowledges the tighter language.

## GPT Improvement (9M→8M)

DE→DF resolved:
- DE #9 (γ recipe location) → Resolved (moved to Design Equations)
- DE #8 (Model C coupling) → Resolved (explicit Model C results added)

DE→DF evolved/new:
- DE #1 (three-layer) → DF #3 (narrower: "messaging inconsistency" only)
- DE #7 (fleet reuse R=3 insufficient) → DF #8 (R=7 "too thin for strength of recommendation")
- NEW: DF #1 (per-slot acquisition) — Fundamental modeling assumption challenge
- NEW: DF #6 (ARQ demand derivation) — Wants analytical distribution, not just "8 retries"

## Claude Evolution (5M stable, 14m regressed)

- DE #4 (γ expression standard) → RESOLVED — no longer raised as major
- NEW: DF #3 (TDMA sizing comparison) — wants comparison to DVB-RCS2 and textbook methods
- Persistent: DES (#1), GE specificity (#2), static clusters (#4), coordinator SPOF (#5)
- Minors regressed 12→14: new issues about related work trimming, Eq. 1 relevance, abstract simplification

## Gemini Evolution (3M stable)

- DE #1 (p_BG) → DF #1 (ARQ coherence): Now wants per-slot fast-fading model
- DE #2 (thundering herd BEB) → RESOLVED — not re-raised
- DE #3 (R=3 aggregate) → DF #3 (R=7 qualification): Evolved to "geometric baseline" request
- NEW: DF #2 (k_c sensitivity on γ) — Does γ break at k_c=500 with fixed T_c?

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
| **DF** | **Accept w/ Minor (3M/5m)** | **Major (8M/9m)** | **Major (5M/14m)** |

## Major Issues Remaining

### Priority 1: Per-slot acquisition assumption (GPT #1 — NEW, HIGH IMPACT)
GPT argues the 35 kbps recommendation is driven by per-slot cold-start acquisition (5 ms × 99 nodes = 495 ms overhead). If tracking-mode TDMA is used, γ increases and 30 kbps suffices.
**Fix:** Table rate_feasibility already shows cold-start/reacquire/tracking modes. Make this more prominent. Add text explaining why per-slot cold-start is the conservative default for Prox-1 (burst-mode demod) while tracking mode requires stable link. Already addressed — needs emphasis.

### Priority 2: ARQ demand derivation (GPT #6 — NEW)
Wants analytical distribution of failed packets per cycle, not just "8 concurrent retries."
**Fix:** Add explicit GE calculation: E[failed] = k_c · π_B · p_B ≈ 100 × 0.091 × 0.90 = 8.2; P95 via binomial.

### Priority 3: TDMA sizing comparison (Claude #3 — NEW)
Wants comparison to DVB-RCS2 and textbook TDMA efficiency methods.
**Fix:** Add brief paragraph: "Standard TDMA efficiency (Maral & Bousquet) computes η_TDMA = payload/frame; Eq. 14 extends this with rate-dependent parameterization under CCSDS framing and half-duplex constraints."

### Priority 4: DES reduction (GPT #4, Claude #1 — PERSISTENT)
Both agree DES adds little beyond verification. Claude wants Fig. 4 removed.
**Fix:** Consider removing Fig. 4 (buffer CDF) to save space and reduce DES prominence.

### Priority 5: GE specificity (Claude #2 — PERSISTENT)
Wants parametric design regions rather than point estimates.
**Fix:** The paper already has Fig. 2b (P95 vs p_BG). Add sentence: "The 35 kbps recommendation applies when p_B ≥ 0.7 and p_BG ≤ 0.5; for p_B < 0.7 (benign channel), 30 kbps suffices."

### Priority 6: γ ledger (GPT #2 — PERSISTENT, narrower)
Wants full authoritative ledger table (not just footnote).
**Fix:** Promote footnote to small standalone table showing rate/T_slot/γ/source for each used value.

### Priority 7: Three-layer messaging (GPT #3 — PERSISTENT, narrower)
Now just about messaging inconsistency, not structural.
**Fix:** Text audit: replace any remaining "byte budget / MAC efficiency / TDMA airtime" with "Test A / Test B."

### Priority 8: k_c sensitivity on γ (Gemini #2 — NEW)
Does γ break at k_c=500?
**Fix:** γ is independent of k_c (it depends on slot parameters only). The binding constraint at k_c=500 is total cycle time: 499 × T_slot. Add brief note.

### Priority 9: R=7 qualification (GPT #8, Gemini #3 — EVOLVED)
Wants "geometric baseline" framing with parametric sensitivity.
**Fix:** Add "geometric baseline" language. Already partially addressed.

### Priority 10: Static clusters (Claude #4 — PERSISTENT)
**Fix:** Already scoped in abstract. Add one more sentence about reassociation transient impact.

### Priority 11: Coordinator SPOF (Claude #5 — PERSISTENT)
**Fix:** Promote thundering herd from footnote to brief subsection paragraph.

### Priority 12: Campaign d mapping (GPT #7 — PERSISTENT)
**Fix:** Already has Table VII with mission phases. Add ESA station-keeping ops cadence example.

## Text-Fixable Items for DG

1. **Justify per-slot acquisition** — Add 2 sentences: "Per-slot cold-start is conservative because Prox-1 uses burst-mode demodulation with individual preamble per packet; tracking-mode systems (Table XIII) reduce T_acq to 0-2 ms, shifting R_PHY,min to 25-28 kbps."
2. **ARQ demand derivation** — Add: "E[failed nodes per cycle] = k_c · π_B · p_B = 100 × 0.091 × 0.90 ≈ 8.2; P95 (binomial) ≈ 14 nodes × T_slot ≈ 1,288 ms. At 35 kbps: margin 1,880 ms > P95 demand."
3. **TDMA sizing comparison** — Add brief paragraph near γ derivation.
4. **k_c independence of γ** — Add note: "γ depends only on per-slot parameters; k_c affects total ingress time T_ing = (k_c-1) × T_slot but not T_slot itself."
5. **GE recommendation conditioning** — Add explicit p_B/p_BG condition for 35 vs 30 kbps.
6. **γ ledger promotion** — Move from footnote to small inline table in Design Equations.
7. **Three-layer messaging audit** — Replace any "three-layer" or "three-test" with "two-test."
8. **R=7 "geometric baseline"** — Add qualifier.
9. **Promote thundering herd** — Move from footnote to inline paragraph (compact).
10. **Version tag** → paper-02-v-dg
