# Version CZ Review Summary

## Recommendations

| Reviewer | Recommendation | Change from CY |
|----------|---------------|----------------|
| Gemini 3 Pro | **Accept with Minor Revisions** | Stable (3M/4m→3M/5m) |
| GPT-5.2 | **Major Revision** | Improved (7M/10m→7M/8m) |
| Claude Opus 4.6 | **Major Revision** | Improved (5M/13m→5M/12m) |

## What CZ Fixed (Acknowledged by Reviewers)

1. **"Two-test" terminology** — GPT: "you emphasize 'two-test feasibility'" — acknowledges the systematic Layer→Test rename. Still finds residual quasi-independent language around γ ("the narrative still sometimes treats 1/γ as quasi-independent").
2. **RF-backup survival mode** — Gemini: "Section III.B.2 states hierarchical coordination is 'suspended' and nodes enter safe-hold." The text was strengthened but Gemini reframes the concern as a ConOps contradiction (suspended vs. Raft election occurring).
3. **Doppler budget** — Not re-raised by Gemini as a separate concern. The explicit "Doppler compensation is an acquisition function, not a guard function" statement resolved the CY Gemini #2 issue.
4. **Table 10 column header** — Changed from "Param. est." to "Std.-based est." Not specifically re-raised.
5. **Stress-case contextualization** — All three reviewers acknowledge the <1% operational time framing. GPT: "stress-case η_S ≈ 46% is now better contextualized." Claude: "yearly mixture calculation (η̄ = 5.6%) providing useful context."
6. **γ consistency** — Claude: "gamma unification appears consistently applied: γ₂₄ = 0.761, γ₃₀ = 0.745, γ₃₅ = 0.732." No γ consistency issues raised by any reviewer.

## Gemini Detail (Stable 3M → 3M but +1 minor)

CY→CZ changes:
- CY Major #1 (R=3 spatial reuse) → Persistent as CZ Major #3
- CY Major #2 (γ Doppler sensitivity) → **RESOLVED** by Doppler budget note
- CY Major #3 (RF-backup ConOps) → Persistent as CZ Major #2 (reframed: "suspended" vs Raft election contradiction)
- NEW: CZ Major #1 (T_acq sensitivity — want breaking point at 35 kbps)

Net: Doppler resolved, T_acq sensitivity appeared. Major count stable at 3.

## Major Issues Remaining

### Priority 1: Per-Slot Acquisition Assumption (GPT #1, Gemini #1 — CONVERGING CONCERN)
Both GPT and Gemini now highlight that T_acq = 5 ms per slot drives the entire PHY recommendation. GPT wants alternate acquisition modes computed in the feasibility table. Gemini wants the breaking point of T_acq at 35 kbps. The paper already has an "Acquisition architecture" paragraph (3 modes) but it's not promoted to the feasibility table.

**Text-fixable?** Partially. Can add a column to the rate feasibility table showing per-burst and continuous-tracking modes. No new simulation needed — the γ formula is already parameterized.

### Priority 2: Circular Validation / DES Tautology (Claude #1 — PERSISTENT STRUCTURAL)
Claude: "The DES, slot-level simulator, and packet-level simulator all implement the same equations... extensive internal cross-checking may give readers a false sense of confidence."

**Text-fixable?** Can further compress DES emphasis and restructure framing. Cannot add external validation without new work.

### Priority 3: Fleet-Level Scaling / R=3 (Gemini #3, Claude #2 — PERSISTENT)
Both want either a link budget calculation for R=3 or restriction of claims to per-cluster. Claude: "explicitly restrict all claims to per-cluster sizing and remove fleet-level scaling from the abstract and conclusions."

**Text-fixable?** Yes — can add a simple back-of-envelope link budget or restrict claims. A 3-line path loss calculation at 500 km with standard patch antenna gain roll-off could satisfy this.

### Priority 4: GE Coherence Tautology (GPT #4, Claude #3 — PERSISTENT)
Both want the GE analysis reframed as sensitivity tool, not design prescription. Claude: "Present GE analysis purely as a sensitivity tool."

**Text-fixable?** Yes — reframe the dual coherence-regime recommendation as conditional on measured τ_c/T_c.

### Priority 5: ACK-in-Guard Treatment (GPT #2 — NEW)
GPT: "guard time is typically 'dead time' to prevent overlap; using it for deterministic transmissions requires tight timing guarantees." Wants explicit ACK timing in superframe budget.

**Text-fixable?** Partially. Can add explicit timing argument showing deterministic offset. No new simulation needed.

### Priority 6: α_RX Definition Tightness (GPT #3 — PERSISTENT)
GPT wants α_RX formally defined as schedule decision variable, not appearing as both input and output.

**Text-fixable?** Yes — can add formal definition clarifying it's computed, not assumed.

### Priority 7: RF-Backup ConOps Contradiction (Gemini #2, Claude #4 — EVOLVED)
Both frame it as: if hierarchy is "suspended," why is a Raft election (coordination task) occurring? Claude extends: wants full Markov availability model.

**Text-fixable?** Can clarify ConOps (UHF = recovery transient to restore S-band, not coordination). Cannot add Markov availability model without new work.

### Priority 8: 1 kbps Link Budget (Claude #5 — PERSISTENT)
Wants complete S-band ISL link budget table. Paper currently states parameters but doesn't show full budget.

**Text-fixable?** Yes — can add a link budget table (Tx power, antenna gain, path loss, noise figure, coding gain, margin). Straightforward calculation.

### Priority 9: Workload d Sensitivity (GPT #6 — PERSISTENT)
Wants sensitivity table for different burst-length distributions and correlation structures.

**Text-fixable?** Partially. Can add text-based analysis. Full parametric sweep requires new simulation.

### Priority 10: γ "Validation" Language (GPT #7 — PERSISTENT)
Still finds "validated" phrasing. GPT minor #8: "validated via CCSDS, replacing earlier 0.85" — wants "revised/anchored."

**Text-fixable?** Yes — find and replace remaining "validated" near γ.

## Minor Issues (25 total)

### Gemini (5 minor)
1. α_RX duty cycle definition
2. Proprietary ISL γ=0.530 assumptions
3. Fig 3 Bernoulli vs Markov clarification
4. Eq 11 q definition placement
5. "Emergent finding" → "emergent system dynamic"

### GPT (8 minor — improved from 10)
1. γ values and rounding consistency
2. η vs η_total naming
3. Table IV-D Model S only (move to appendix)
4. 512 B summary with 371 B metadata justification
5. R=3 fleet reuse justification
6. AoI P99 misinterpretation preempt
7. Algorithm 1 η₀=5% constant vs variable
8. "Validated via CCSDS" → "anchored"

### Claude (12 minor — improved from 13)
1. α_RX default value context
2. M_total unused
3. 371 B metadata/CRC decomposition
4. Sync beacon 8 bits too short
5. Raft messages in TDMA frame
6. AoI/TCA conflation
7. Fig 2 bars vs CDF
8. Table VII margin column header
9. Eq model terminology
10. Reference [43] unreferenced
11. Abstract detail level
12. Algorithm 1 Line 4 equivalence

## Progress Trajectory

| Version | Gemini | GPT | Claude |
|---------|--------|-----|--------|
| CJ | Accept w/ Minor (3M/4m) | Major (7M/8m) | Major (5M/12m) |
| ... | ... | ... | ... |
| CW | Accept w/ Minor (2M/4m) | Major (7M/8m) | Major (5M/14m) |
| CX | Accept w/ Minor (2M/4m) | Major (7M/7m) | Major (5M/14m) |
| CY | Accept w/ Minor (3M/4m) | Major (7M/10m) | Major (5M/13m) |
| **CZ** | **Accept w/ Minor (3M/5m)** | **Major (7M/8m)** | **Major (5M/12m)** |

**Assessment:** GPT and Claude both improved from CY regression. Gemini stable. The "Layer" → "Test" rename and Doppler budget note had positive effects (GPT -2 minor, Claude -1 minor, Gemini Doppler resolved). However, the structural ceiling remains firm.

## Structural Ceiling Status (Post-CZ)

After 17 versions (CJ–CZ):
- **Gemini**: Oscillates 2-3 M, 4-5 m. Accept with Minor consistently. Issues are R=3 and T_acq sensitivity.
- **GPT**: Locked at 7 M, 7-10 m. Has never gone below 7M. Core issues: per-slot acquisition, ACK-in-guard, α_RX, GE tautology, three-layer residual, workload sensitivity, γ "validation" language.
- **Claude**: Locked at 5 M, 12-14 m. Has never gone below 5M. Core issues: circular validation, fleet scaling, GE model, coordinator failure, 1 kbps link budget.

## Actionable Text-Only Edits for DA

Several items are text-fixable and could yield modest improvement:

1. **Add acquisition-mode columns to rate feasibility table** — Show γ and R_PHY,min under per-slot/per-burst/continuous tracking. Addresses GPT #1, Gemini #1. (HIGH IMPACT)
2. **Add simple R=3 link budget** — Back-of-envelope: path loss at 500 km vs 1500 km (R=3 spacing), antenna gain roll-off, C/I calculation. 3-4 lines. Addresses Gemini #3, Claude #2.
3. **Reframe GE as sensitivity tool** — Change "Dual coherence-regime recommendation" to "Dual coherence-regime sensitivity" in conclusion. Present R_PHY,min as function of τ_c/T_c. Addresses GPT #4, Claude #3.
4. **Add S-band link budget table** — Straightforward: Tx 1W (+30 dBm), antenna 6 dBi, path loss -157 dB, noise figure 3 dB, coding gain 5 dB, etc. Addresses Claude #5.
5. **Explicit ACK timing argument** — State: "ACK transmitted at deterministic offset t₀ + T_slot - 0.5 ms within the 1.0 ms jitter sub-allocation; requires clock sync < 0.5 ms (satisfied by GPS/GNSS < 100 ns)." Addresses GPT #2.
6. **Clarify RF-backup as recovery transient** — "The Raft election is a recovery mechanism to restore the S-band control plane, not a continuation of coordination." Addresses Gemini #2, Claude #4.
7. **Fix remaining "validated via CCSDS"** — Addresses GPT #7, GPT minor #8.
8. **Add α_RX formal definition** — "α_RX(R_PHY, M_r) = T_ing(R_PHY, M_r) / T_c, computed from schedule parameters." Addresses GPT #3.

## Recommended Strategy

**Option A: One more text round (DA).** Apply edits 1-8 above. Expected: Gemini 2-3M (may resolve T_acq), GPT 6-7M (may drop one major), Claude 5M (structural unchanged). Low effort, modest return.

**Option B: Submit with structural ceiling.** Gemini's consistent Accept with Minor is the strongest signal for journal review. GPT and Claude's persistent majors are structural and would require:
- NS-3 simulation (Claude #1)
- Hardware γ measurement (Claude #1)
- Antenna pattern analysis (Gemini #3, Claude #2)
- Sub-cycle GE model (GPT #4)
- Additional campaign models (GPT #6)

These are multi-week engineering tasks beyond text editing.

**Option C: Hybrid — one more round targeting the text-fixable high-impact items, then submit.**

**Recommend Option C**: Apply edits 1-3 (acquisition modes table, R=3 link budget, GE reframe) which are the highest-impact text changes, then submit. The link budget table (edit 4) is also high-value and straightforward.
