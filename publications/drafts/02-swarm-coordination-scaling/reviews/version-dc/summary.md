# Version DC Review Summary

## Recommendations

| Reviewer | Recommendation | Change from DB |
|----------|---------------|----------------|
| Gemini 3 Pro | **Accept with Minor Revisions** | Mixed (2M/4m→3M/5m issues, still Accept) |
| GPT-5.2 | **Major Revision** | Improved (8M/7m→6M/8m) |
| Claude Opus 4.6 | **Major Revision** | Mixed (5M/13m→6M/13m) |

## What DC Fixed (Acknowledged by Reviewers)

1. **R=3 warning added** — Gemini: Still raises R=3 but now frames it as "aggregate interference" calculation request rather than a missing acknowledgment. The explicit warning was partially effective but Gemini wants more.
2. **Orbital safety during 300s gap** — Gemini: No longer cites "unaddressed safety risk" — instead raises a semantics issue about "suspension" vs "Raft election." The safety statement was effective.
3. **d mapping canonical formula** — GPT: "Your Table V (duty mapping) is a start" — acknowledges improvement but wants procedural mapping with uncertainty bounds. Reduced from a pure gap to a scope concern.
4. **Conservative ACK as default** — GPT: Major #5 (ACK handling) now wants "one ACK model for primary results propagated everywhere." The conservative default was partially absorbed.
5. **γ measurement recipe** — GPT: No longer raises γ measurement as a standalone major (was #8 in DB). Absorbed into constructive suggestion #1.
6. **Test A/B decoupling statement** — Claude: The coupling concern was not re-raised as a major (was #4 in DB). Resolved.
7. **DES tail claim narrowed** — Claude: Still raises DES as #1 but notes "the paper acknowledges this."

## GPT Significant Improvement (8M→6M)

DB→DC resolved majors:
- DB Major #7 (ACK/guard conservative) → Partially absorbed into DC Major #5 (narrower: consistency rather than absence)
- DB Major #8 (γ measurement recipe) → Resolved as standalone major; absorbed into constructive suggestions
- DB Major #1 (d mapping) → Persistent but narrowed (DC Major #2)
- DB Major #2 (γ/Model S leak) → Dropped as separate major; merged into DC Major #3 (three-layer)

## Gemini Regression Detail (2M→3M)

NEW Major #3 (Unicast stagger latency): "For formation flying or collision avoidance, 190s might be too long." The paper already addresses this (safety-critical broadcasts = single cycle; unicast = non-time-critical only) but Gemini wants more explicit qualification.

Major #1 (R=3): Despite the added warning, Gemini now wants aggregate C/I calculation (6 co-channel clusters).
Major #2 (RF-backup): Semantic concern about "suspension" while Raft runs. Already addressed — needs clearer separation.

## Claude Regression Detail (5M→6M)

NEW Major #5 (C_node parametric sweep): Previously a constructive suggestion, now elevated to major. Wants C_node ∈ [0.5, 5] kbps sweep.
Major #4 reframed: γ expression novelty → now says it's "overstated" rather than absent. More nuanced.
Claude #4 from DB (Test A/B coupling) → RESOLVED by decoupling statement.

## Major Issues Remaining

### Priority 1: "Validated" language (GPT #1, Claude #2 — PERSISTENT)
Both want "validated via CCSDS" replaced with "anchored" or "estimated." Text-fixable.

### Priority 2: Three-layer perception (GPT #3, Claude #3 — PERSISTENT)
GPT: "Eq. (mac_efficiency) reads like a third constraint." Claude: "three-layer language persists."
**Fix:** Remove Eq. mac_efficiency or explicitly label it "unit conversion within Test B." Text-fixable.

### Priority 3: Unicast stagger qualification (Gemini #3 — NEW)
Already stated in paper but needs explicit per-command-type qualification.
**Fix:** Add explicit sentence near Eq. unicast_stagger. Text-fixable.

### Priority 4: RF-backup semantics (Gemini #2 — EVOLVED)
Gemini sees contradiction: "suspended" but Raft runs. Already addressed — needs one sentence: "Raft election is a recovery transient, not coordination."
**Fix:** Already present. Strengthen. Text-fixable.

### Priority 5: d mapping procedural (GPT #2 — PERSISTENT)
Still wants uncertainty bounds on d. Partially text-fixable.

### Priority 6: ARQ provisioning alternative (GPT #4 — PERSISTENT)
Wants shared retransmission pool analysis. Requires new analysis — not text-fixable.

### Priority 7: DES tautological (Claude #1 — PERSISTENT STRUCTURAL)
Claude wants DES reduced to 1 paragraph. Requires structural cuts.

### Priority 8: γ expression novelty (Claude #4 — EVOLVED)
Now "overstated" rather than absent. Text-fixable via reframing.

### Priority 9: C_node parametric sweep (Claude #5 — NEW)
Requires new figure/analysis. Not text-fixable.

### Priority 10: R=3 aggregate C/I (Gemini #1 — PERSISTENT)
Wants calculation for 6 co-channel interferers. Brief analytical addition possible.

### Priority 11: Coordinator failure rigor (Claude #6 — EVOLVED from minor)
Wants footnote promoted to subsection or explicitly marked as order-of-magnitude.

## Minor Issues (18 total)

### Gemini (5 minor)
1. Table I section reference alignment
2. DVB-RCS2 return vs forward link clarification
3. Fig. 3 marker visibility
4. Eq. 10 ASM coding (framing bits FEC-encoded?)
5. "Slot-sim" capitalization consistency

### GPT (8 minor)
1. Replace "validated" everywhere
2. Abstract γ range inconsistency
3. Table IV rate ordering (non-monotonic)
4. AoI "sampling tail" warning placement
5. R=3 aggregate interference equation
6. Algorithm 1 η₀ fixed vs k_c-dependent
7. GE p_BG approximation (exponential vs linear)
8. Model S table emphasis

### Claude (13 minor)
1. Abstract "validated" → "estimated"
2. α_RX dependency order
3. Eq. 2 excludes commands/heartbeats
4. Sectorized mesh k_s = √N motivation
5. Table IV caption standardization
6. Fig. 2 forward reference
7. Eq. 6 parallel voting assumption
8. J2 perturbation calculation
9. Sync beacon 8 bits clarity
10. Eq. gamma_time over-referenced
11. kbps vs bps formatting
12. "0.1% of time" traceability
13. Reference [3] date

## Progress Trajectory

| Version | Gemini | GPT | Claude |
|---------|--------|-----|--------|
| CW | Accept w/ Minor (2M/4m) | Major (7M/8m) | Major (5M/14m) |
| CX | Accept w/ Minor (2M/4m) | Major (7M/7m) | Major (5M/14m) |
| CY | Accept w/ Minor (3M/4m) | Major (7M/10m) | Major (5M/13m) |
| CZ | Accept w/ Minor (3M/5m) | Major (7M/8m) | Major (5M/12m) |
| DA | Accept w/ Minor (2M/5m) | Major (7M/10m) | Major (5M/12m) |
| DB | Accept w/ Minor (2M/4m) | Major (8M/7m) | Major (5M/13m) |
| **DC** | **Accept w/ Minor (3M/5m)** | **Major (6M/8m)** | **Major (6M/13m)** |

**GPT best-ever major count (6M).** Previous low was 7M (CW, CX, CY, CZ, DA).

## Structural Assessment

GPT's improvement to 6M is significant — the d mapping formula, conservative ACK, γ measurement recipe, and test decoupling collectively resolved 2 majors. However, the remaining 6 are largely structural:
- "Validated" language (text-fixable)
- Three-layer perception (partially text-fixable)
- ARQ alternative policy (requires new analysis)
- ACK consistency (partially text-fixable)
- d procedural mapping (partially text-fixable)
- 1 kbps logical vs physical (text-fixable)

Claude's regression (5M→6M) via C_node sweep is not text-fixable but the resolution of Test A/B coupling is a positive signal.

## Text-Fixable Items for DE

1. **Remove "validated" language everywhere** — Search and replace "validated via CCSDS" with "anchored in CCSDS framing" (or "estimated from"). Addresses GPT #1, Claude #2, multiple minors.
2. **Remove or relabel Eq. mac_efficiency** — Add explicit label: "Unit conversion within Test B (not a separate feasibility test):" before the equation. Addresses GPT #3, Claude #3.
3. **Unicast stagger qualification** — Add after Eq. unicast_stagger: "This applies to non-time-critical operations (orbit-raising, software updates); safety-critical commands use 128 B broadcast (43 ms, single-cycle)." Addresses Gemini #3.
4. **Strengthen RF-backup recovery transient** — Add emphasis: the Raft election occurs during the recovery transient, not during the suspended coordination state. Addresses Gemini #2.
5. **Reframe γ expression as convenience** — Add: "Eq. (11) systematizes the standard TDMA slot-budget calculation for the swarm coordination context; the rate-dependent parameterization is the specific contribution." Addresses Claude #4.
6. **Aggregate C/I estimate** — Add: "With 6 co-channel interferers at 1,500 km: aggregate I ≈ 6 × I_single; C/I_agg ≈ 26 − 10 log₁₀(6) = 18.2 dB, marginally below 20 dB—confirming R = 7 may be needed." Addresses Gemini #1.
7. **Coordinator failure framing** — Add "order-of-magnitude estimate" qualifier to the thundering-herd calculation. Addresses Claude #6.
8. **Version tag** → paper-02-v-de

## Recommended Strategy

Apply items 1–8. This addresses all 3 Gemini majors and 3 of 6 GPT majors (text-fixable ones). Expected: Gemini 1-2M (stronger Accept), GPT 4-5M (still Major but improved), Claude 5-6M (stable to slight improvement). The remaining GPT/Claude majors (ARQ alternative, C_node sweep, external validation) require new analysis or simulation beyond text editing.
