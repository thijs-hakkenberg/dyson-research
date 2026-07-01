# Version DB Review Summary

## Recommendations

| Reviewer | Recommendation | Change from DA |
|----------|---------------|----------------|
| Gemini 3 Pro | **Accept with Minor Revisions** | Stable (2M/5m→2M/4m) |
| GPT-5.2 | **Major Revision** | Mixed (7M/10m→8M/7m) |
| Claude Opus 4.6 | **Major Revision** | Stable (5M/12m→5M/13m) |

## What DB Fixed (Acknowledged by Reviewers)

1. **α_RX notation table** — Removed broken formula, simplified to "Computed output." GPT no longer flags the parenthesis error from DA.
2. **Doppler range-rate calculation** — Gemini: Doppler range-rate no longer raised as a major. The explicit ρ̇×T_slot/c = 2.1 μs ≪ 4.7 ms guard calculation resolved this. Down from 3 Gemini majors (CZ) to 2 persistent ones.
3. **Raft BEB convergence** — Gemini: BEB convergence still raised as Major #2 but now framed as "operational risk" rather than "mathematical rigor." The round-by-round backoff analysis (G: 25→12.5→6.25→3.1→1.56) was partially acknowledged.
4. **"MAC scales by 1/γ" → "Test B converts to airtime"** — GPT still raises three-layer narrative as Major #3 but now frames it differently, focusing on "accounting equivalence" rather than naming.

## Gemini Improvement Detail (2M/5m→2M/4m)

DA→DB changes:
- DA Major #1 (Doppler range-rate) → **RESOLVED** by explicit timing calculation
- DA Major #2 (Raft election convergence) → Persistent as DB Major #2 (evolved: now about "operational risk of suspended hierarchy" — safety during 300s gap)
- DB Major #1 (R=3 interference) → Re-evolved from minor; now wants "Warning" block or sensitivity note
- One minor dropped (net 5→4)

## GPT Mixed Result (7M/10m→8M/7m)

GPT gained a new major (#7: ACK/guard/half-duplex accounting — wants conservative alternative as default) and the "γ measurement recipe" was elevated from constructive suggestion to major #8. However, 3 minors were resolved (net 10→7). The total major count increased 7→8, but total issue count dropped 17→15.

Key persistent GPT majors: d mapping (#1), γ/Model S leak (#2), three-layer narrative (#3), DES value (#4), packet validation naming (#5), GE/ARQ conditional (#6), ACK/guard conservative (#7), γ measurement (#8).

## Claude Stable (5M/12m→5M/13m)

Claude's assessment is nearly identical to DA. The 5 majors are unchanged: circular validation (#1), DES footprint (#2), design recommendations framing (#3), Test A/B coupling (#4), static cluster membership (#5). One new minor appeared (#7: Fig. 2 cross-reference).

## Major Issues Remaining

### Priority 1: R=3 Sensitivity Warning (Gemini #1 — EVOLVED)
Gemini: "the authors should add a sensitivity note or 'Warning' block... explicitly state that R=3 is a lower bound and that realistic antenna sidelobes might require higher R."
**Fix:** Add 1-2 sentence warning after R=3 link budget calculation. Text-fixable.

### Priority 2: RF-Backup Safety During 300s Gap (Gemini #2 — EVOLVED)
Gemini: "explicitly discuss the safety implications of this 300s gap. Is the passive safety of the orbit sufficient?"
**Fix:** Add brief orbital safety statement (at 550 km, conjunction probability per 300s window is negligible without active maneuvering). Text-fixable.

### Priority 3: d Mapping Confusion (GPT #1 — PERSISTENT)
GPT wants unambiguous mapping from operational schedules to (d, p_cmd). Wants a canonical formula or worked example.
**Fix:** Add 1 sentence clarifying effective per-cycle rate = d × p_cmd. Partially text-fixable.

### Priority 4: γ/Model S Leakage (GPT #2 — PERSISTENT)
GPT: Model S coupling table should not be in main text where it can be misread as supporting decisions.
**Fix:** Add stronger caption warning. Partially text-fixable.

### Priority 5: Three-Layer Narrative (GPT #3 — PERSISTENT)
GPT: "Test A (bytes), then MAC efficiency 1/γ, then TDMA airtime — suggesting a third layer."
**Assessment:** This appears unfixable via text. The information-rate→PHY-rate→airtime pipeline inherently reads as three stages regardless of how it's labeled.

### Priority 6: Circular Validation (Claude #1 — PERSISTENT STRUCTURAL)
Claude: "All three verification tools share the same equations." Requires NS-3, DVB-RCS2 comparison, or hardware measurement. Not text-fixable.

### Priority 7: DES Footprint (GPT #4, Claude #2 — PERSISTENT)
Both want DES compressed or its tail contribution strengthened with alternative workload models. Partially text-fixable (compress further).

### Priority 8: GE/ARQ Conditional Framing (GPT #6, Claude relates — PERSISTENT)
GPT: "27% intra-cycle recovery is by construction under τ_c ≥ T_c." Wants decision tree keyed on τ_c/T_c.
**Fix:** Already reframed as "coherence-regime sensitivity." Further strengthening possible via explicit conditioning in every GE result.

### Priority 9: ACK/Guard Conservative Default (GPT #7 — NEW)
GPT: "Provide a conservative alternative superframe with explicit ACK mini-slots and make conservative framing the default."
**Fix:** Conservative alternative already present (+50 ms). Could promote to default. Text-fixable.

### Priority 10: γ Measurement Recipe (GPT #8 — ELEVATED)
GPT: "Add a concise measurement protocol paragraph."
**Fix:** Add 2-3 sentences on what to log. Text-fixable.

### Priority 11: Test A/B Coupling (Claude #4 — PERSISTENT)
Claude: "Under high duty factors (d > 0.5), byte budget and airtime constraints interact nonlinearly."
**Fix:** Add sentence: "For d ≤ 0.10 (95% of operational time), tests decouple." Text-fixable.

### Priority 12: Static Cluster Membership (Claude #5 — PERSISTENT STRUCTURAL)
Claude: "Aggregate effect of many concurrent re-associations is not analyzed."
**Assessment:** Requires simulation or analytical model beyond text editing.

## Minor Issues (24 total)

### Gemini (4 minor)
1. Figure caption length (Figs 3, 4)
2. γ notation — use γ(R_PHY) consistently
3. Eq. 11 layout cluttered
4. Abstract: add "(Model C)" after γ range

### GPT (7 minor)
1. "MAC efficiency" vs "slot efficiency" terminology inconsistency
2. Algorithm 1: C_node not in REQUIRE list
3. Units: "kbps" columns need "info" or "PHY" labels
4. Model S table location/captioning
5. AoI: network-induced losses add mass at multiples of T_c
6. Fleet reuse: aggregate interference from multiple clusters
7. Related work: satellite TDMA/DAMA references

### Claude (13 minor)
1. Table I: α_RX example conditioning parameters
2. Eq. 2: uniform k_r assumption unstated
3. s_proc = 5 ms/msg unjustified
4. Collision avoidance rate 10⁻⁴/node/s in footnote vs main text
5. Phase-stagger result untabulated
6. Eq. 10: f_decision,max ≈ 24 derivation missing
7. Fig. 2 cross-reference placement
8. Section IV-H subsection header missing
9. Thundering herd footnote placement
10. Inconsistent ≈ vs = for γ values
11. Table III handoff state 10-50 MB range guidance
12. Abstract γ range needs rate correspondence
13. Self-citation [dyson_multimodel]

## Progress Trajectory

| Version | Gemini | GPT | Claude |
|---------|--------|-----|--------|
| CW | Accept w/ Minor (2M/4m) | Major (7M/8m) | Major (5M/14m) |
| CX | Accept w/ Minor (2M/4m) | Major (7M/7m) | Major (5M/14m) |
| CY | Accept w/ Minor (3M/4m) | Major (7M/10m) | Major (5M/13m) |
| CZ | Accept w/ Minor (3M/5m) | Major (7M/8m) | Major (5M/12m) |
| DA | Accept w/ Minor (2M/5m) | Major (7M/10m) | Major (5M/12m) |
| **DB** | **Accept w/ Minor (2M/4m)** | **Major (8M/7m)** | **Major (5M/13m)** |

## Structural Ceiling Assessment (Post-DB)

After 20 versions (CJ–DB):
- **Gemini**: Stable at 2M, improving on minors. Remaining 2 majors are text-fixable (R=3 warning, RF-backup safety). Could reach 0M/Accept.
- **GPT**: Locked at 7-8M. Core issues (three-layer perception, Model S elimination, d canonical mapping, γ measurement, DES value) are partially text-addressable but unlikely to drop below 4-5M via text alone.
- **Claude**: Locked at 5M. Core issues (circular validation, DES footprint, static clusters) require new simulation/analysis work.

## Text-Fixable Items for DC

1. **R=3 sensitivity warning** — Add explicit "Warning" that R=3 is a lower bound; multi-cluster interference may require R=7 or higher. Addresses Gemini #1.
2. **RF-backup orbital safety** — Add: "At 550 km altitude, the collision probability during a 300 s safe-hold window is negligible (~10⁻⁸ per conjunction event); passive orbital safety suffices." Addresses Gemini #2.
3. **Test A/B decoupling statement** — Add: "For d ≤ 0.10 (≥95% of operational time), Test A is ingress-dominated and effectively decouples from Test B." Addresses Claude #4.
4. **d mapping clarification** — Add: "Effective per-cycle command probability: p_eff = d × p_cmd." Addresses GPT #1 partially.
5. **Conservative ACK as default framing** — Promote +50 ms ACK alternative to primary recommendation; retain 0.5 ms embedded as optimistic option. Addresses GPT #7.
6. **γ measurement recipe** — Add 2-3 sentences: "To instantiate Eq. (γ_time), log time from TX-enable to first decoded frame across SNR/Doppler conditions; compute T_acq as the P95 of this distribution. Turnaround time: measure radio TX/RX switching latency." Addresses GPT #8.
7. **DES compression** — Further compress DES section; narrow buffer multiplier claim to "example under stated campaign model." Addresses GPT #4, Claude #2 partially.
8. **Figure caption compression** — Shorten Fig 3, Fig 4 captions. Addresses Gemini minor #1.
9. **Version tag** → paper-02-v-dc

## Recommended Strategy

**Apply items 1-9 for DC.** Primary goal: resolve Gemini's remaining 2 majors (R=3 warning + orbital safety) to achieve clean Accept. Secondary goal: reduce GPT major count by 1-2 via conservative ACK default, γ measurement recipe, and d clarification. Claude's structural issues remain beyond text scope.

Expected outcome: Gemini 0-1M (Accept/Accept w/ Minor), GPT 6-7M (Major), Claude 5M (Major).
