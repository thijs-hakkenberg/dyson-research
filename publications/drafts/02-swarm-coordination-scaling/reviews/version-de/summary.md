# Version DE Review Summary

## Recommendations

| Reviewer | Recommendation | Change from DC |
|----------|---------------|----------------|
| Gemini 3 Pro | **Accept with Minor Revisions** | Stable (3M/5m→3M/4m, improved minors) |
| GPT-5.2 | **Major Revision** | Regressed (6M/8m→9M/10m) |
| Claude Opus 4.6 | **Major Revision** | Improved (6M/13m→5M/12m) |

## What DE Fixed (Acknowledged by Reviewers)

1. **Eq. mac_efficiency relabeled** — GPT: Still raises three-layer (#1), but now says "sometimes treats these as separable gates" (acknowledges improvement). Claude: No longer cites three-layer as standalone major — absorbed into general validation concern.
2. **Unicast command-type qualification** — Gemini: No longer raises unicast stagger as a major (was #3 in DC). GPT: Evolved into deeper operational concern (#4) — our explicit breakdown triggered demand for operational implications analysis.
3. **RF-backup recovery transient** — Gemini: Dropped as major; raised thundering herd instead (#2). Claude: Not re-raised.
4. **γ expression reframed as convenience** — Claude: Explicitly acknowledges "the paper is honest about this" but still calls it standard. GPT: Not mentioned as novelty concern.
5. **Coordinator failure "order-of-magnitude"** — Claude: Mentioned in minor #3 (thundering herd footnote detail) — partially effective.
6. **Aggregate C/I for 6 interferers** — Gemini: Still raises R=3 (#3). GPT: **BACKFIRED** — promoted to Major #7: "The text itself shows R=3 becomes marginal/insufficient with 6 interferers. This is a major gap."

## GPT Regression Analysis (6M→9M) — CRITICAL

DC→DE comparison:
- DC #1 (three-layer) → DE #1 (PERSISTENT)
- DC #2 (campaign d) → DE #2 (PERSISTENT, evolved: wants stochastic model)
- DC #3 (γ consistency) → DE #3 (PERSISTENT, expanded: wants parameter ledger)
- DC #4 (stress-case) → DE #4 (WORSENED: explicit command-type breakdown triggered operational analysis demand)
- DC #5 (DES) → DE #5 (PERSISTENT)
- DC #6 (packet γ) → DE #6 (PERSISTENT)
- **NEW** DE #7 (fleet reuse) — Our aggregate C/I calculation (18.2 dB < 20 dB) proved R=3 fails; GPT now uses this against us
- **NEW** DE #8 (ARQ×TDMA Model C) — Was constructive in DC, elevated to major
- **NEW** DE #9 (γ recipe in Design Equations) — Was constructive in DC, elevated to major

Root cause: Two of our DE edits backfired (aggregate C/I created new major; unicast qualification deepened operational concern). Two DC constructive suggestions were promoted to majors when not addressed.

## Claude Improvement (6M→5M)

DC→DE resolved:
- DC #6 (C_node parametric sweep) → Dropped. Claude no longer requests C_node sweep.
- Remaining 5 are persistent structural concerns (circular validation, DES, packet-level, γ standard, static clusters).

## Gemini Stability (3M/4m)

- Major #1 (p_BG dependency): Wants explicit ARQ qualification under fast fading
- Major #2 (thundering herd): Wants BEB specification — new framing, evolved from RF-backup
- Major #3 (R=3 aggregate): Wants aggregate C/I calculation (we provided it, but Gemini still wants R corrected)
- 4 minor issues (down from 5)

## Major Issues Remaining

### Priority 1: Three-layer perception (GPT #1 — PERSISTENT)
Despite relabeling Eq. mac_efficiency as "Unit conversion within Test B," GPT still perceives three separable gates.
**Fix:** Remove Eq. mac_efficiency as standalone equation; inline C_raw = C_info/γ directly into Test B equations. Eliminate the visual appearance of a third equation.

### Priority 2: Fleet reuse R=3→R=7 (GPT #7, Gemini #3 — NEW/SELF-INFLICTED)
Our aggregate C/I calculation proved R=3 is insufficient (18.2 < 20 dB). Need to own this.
**Fix:** Recommend R=7 as default for dense deployments; update fleet capacity claims. Frame R=3 as "isolated clusters only." This converts criticism from "your claim is wrong" to "correctly identified."

### Priority 3: ARQ×TDMA under Model C (GPT #8 — ELEVATED from constructive)
Wants Model C coupling results, not just Model S.
**Fix:** Add brief Model C statement: at 35 kbps Model C, margin ≈ 1,880 ms → sufficient for M_r=1 (one retry); at 30 kbps, margin 730 ms → insufficient for retry (consistent with 35 kbps recommendation).

### Priority 4: γ measurement recipe in Design Equations (GPT #9 — ELEVATED from constructive)
Recipe exists but is in Section IV (Analysis). Practitioners want it in Section V (Design Equations).
**Fix:** Move measurement protocol paragraph from Section IV to Section V. Text relocation only.

### Priority 5: Campaign d stochastic model (GPT #2 — PERSISTENT, evolved)
Wants distributions for campaign start times, durations, correlation scope.
**Fix:** Add compact sensitivity table: η_bar and P95 buffer under 3 burst-length assumptions. Partially text-fixable.

### Priority 6: γ consistency ledger (GPT #3 — PERSISTENT, expanded)
Wants table listing exact γ used in every table/figure.
**Fix:** Add footnote or small table mapping each derived result to its γ value.

### Priority 7: DES tautological (GPT #5, Claude #2 — PERSISTENT)
Both want DES reduced. GPT: "limited publishable value beyond confirming means." Claude: "DES consumes significant paper real estate."
**Fix:** Further compress DES to 1 paragraph + figure reference. Move campaign model detail to footnote.

### Priority 8: Packet-level γ not validation (GPT #6, Claude #3 — PERSISTENT)
Both want "validated via CCSDS" eliminated everywhere and consistent "standards-anchored parameterization" language.
**Fix:** Final audit for any remaining "validated" language.

### Priority 9: Circular validation (Claude #1 — PERSISTENT STRUCTURAL)
Wants at least one external anchor point. Not text-fixable without NS-3 or hardware measurement.
**Fix:** Strengthen limitations statement; explicitly quantify sensitivity of 35 kbps recommendation to T_acq and p_BG in single table.

### Priority 10: Static cluster membership (Claude #5 — PERSISTENT)
Wants dynamic reassociation simulation or prominent scope limitation.
**Fix:** Add explicit scope limitation in abstract: "static cluster membership; dynamic reassociation overhead estimated analytically (< 0.3%)."

### Priority 11: p_BG dependency for ARQ (Gemini #1 — EVOLVED)
Wants explicit qualification that ARQ is effective under fast fading (τ_c ≪ T_c).
**Fix:** Add conditional sentence in ARQ conclusion. Text-fixable.

### Priority 12: Thundering herd BEB (Gemini #2 — NEW)
Wants backoff mechanism specified for UHF election.
**Fix:** Add "Slotted ALOHA with BEB, W_min=32" specification. Text-fixable.

## Minor Issues (26 total)

### Gemini (4 minor)
1. α_RX clarification (computed output, not tunable)
2. Table III "single-threaded" conservative bound note
3. Figure 2 labels vs k_c/k_r parameters
4. Doppler/preamble verification for 50 kHz

### GPT (10 minor)
1. Abstract γ range clarification ("over 24–50 kbps under cold-start acquisition")
2. α_RX never treated as tunable (ensure consistency)
3. Baseline 20.5% labeling (η vs η_total)
4. Coordinator summary metadata 371 B justification
5. GE coherence note (adaptive ARQ could change schedulability)
6. fig-cross-cycle-recovery missing extension
7. Link budget table N₀ label
8. C/I patch pattern -10 dBi assumption citation
9. P99 buffer "20-30% above deterministic" label as DES-observed
10. Reference hygiene for non-archival sources

### Claude (12 minor)
1. Abstract "validated" phrasing → "estimated"
2. Table I α_RX example value may confuse
3. Section III-B-2 thundering herd footnote length
4. Eq. 5 f_decision not introduced in text
5. Table VI "Model S Only" header emphasis
6. Fig. 4 specify which three p_BG values
7. Section IV-A phase-stagger DES configuration detail
8. Eq. 8 L_cmd denominator connection to Table VIII
9. Reference [47] self-citation restriction
10. Model C / Model S terminology (define as acronyms)
11. Table IX aggregate capacity derivation
12. Section IV-E time fraction justification

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
| **DE** | **Accept w/ Minor (3M/4m)** | **Major (9M/10m)** | **Major (5M/12m)** |

**GPT worst since DB (8M).** The DC→DE regression is 3 new majors: fleet reuse (self-inflicted), ARQ Model C (elevated), γ recipe location (elevated).

## Structural Assessment

The GPT regression is driven by two categories:
1. **Self-inflicted** (1 major): The aggregate C/I calculation we added honestly proved R=3 fails, giving GPT ammunition. Fix: own it — recommend R=7 as default.
2. **Elevated constructive suggestions** (2 majors): ARQ Model C coupling and γ recipe location were constructive suggestions in DC but promoted when not addressed. Fix: address both directly.

The remaining 6 GPT majors are persistent structural concerns that have been present since CW–CZ. These require either (a) structural reorganization (three-layer, DES compression) or (b) new analysis (campaign d stochastic model, external validation).

## Text-Fixable Items for DF

1. **Remove Eq. mac_efficiency as standalone** — Inline C_raw = C_info/γ into Test B. Eliminate three-layer visual.
2. **Recommend R=7 as default** — Update fleet claims, scope R=3 to isolated clusters.
3. **Add Model C ARQ coupling** — "At 35 kbps Model C: margin ≈ 1,880 ms, sufficient for M_r=1; at 30 kbps: 730 ms, insufficient."
4. **Move γ recipe to Design Equations** — Relocate measurement protocol paragraph.
5. **Add γ consistency ledger** — Small footnote/table mapping derived results to exact γ values.
6. **Further compress DES** — Target: 1 paragraph + figure reference.
7. **Final "validated" audit** — Replace any remaining validation-implying language.
8. **p_BG ARQ qualification** — "If τ_c ≪ T_c (fast fading), intra-cycle ARQ is effective; the ineffectiveness conclusion is conditional on slow fading."
9. **Thundering herd BEB** — Add "Slotted ALOHA with BEB, W_min=32, W_max=1024."
10. **Static cluster scope** — Add to abstract: "static cluster membership."
11. **Version tag** → paper-02-v-df

## Recommended Strategy

Address all 12 priority items. Expected impact:
- **GPT**: 9M→5-6M. Removing Eq. mac_efficiency resolves #1. R=7 resolves #7. Model C coupling resolves #8. γ recipe relocation resolves #9. γ ledger partially resolves #3. DES compression partially resolves #5. = 4 resolved, 2 partial = target 5M.
- **Claude**: 5M→4-5M. DES compression helps #2. Static cluster scope helps #5. Persistent #1/#3/#4 are structural.
- **Gemini**: 3M→2M. p_BG qualification resolves #1. BEB specification resolves #2. R=7 resolves #3.
