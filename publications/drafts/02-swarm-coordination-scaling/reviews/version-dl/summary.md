# Version DL Review Summary

## Reviewer Recommendations

| Reviewer | Recommendation | Majors | Minors | Trend (from DK) |
|----------|---------------|--------|--------|-----------------|
| Gemini 3 Pro | Accept with Minor | 3 | 5 | Stable |
| GPT-5.2 | Major Revision | 7 | 7 | Minors improved (10→7) |
| Claude Opus 4.6 | Major Revision | 5 | 10 | Minors improved (12→10), **Clarity dropped to 2/5** |

## What Changed DK → DL

### Edits Applied
1. γ Timing Ledger table (in-γ vs outside-γ partitioning)
2. Falsification conditions paragraph
3. γ domain of validity / applicability conditions
4. Coordinator failure transient (election-status interaction)
5. 1 kbps traffic policing clarification
6. T_acq slow hardware recommendation
7. ARQ design trade (M_r = 0/1/2)
8. Fleet reuse scope-down (R=7 provisional)
9. Stress-case thermal note
10. DES further demotion
11. ACK explicit in superframe table (730→680 ms margin cascade)

### What Resolved
- Claude's coordinator failure transient (DK #5) → RESOLVED (no longer appears as major)
- GPT minors improved 10→7 (timing ledger helped)
- Claude minors improved 12→10

### What Persists (Unchanged)
- **No external validation** (Claude #2, GPT #6) — Cannot fix with text alone
- **DES negligible value** (Claude #1, GPT #5) — Further demotion not enough; reviewers want removal or strengthening
- **R=7 spatial reuse** (Claude #5, Gemini #1) — Scope-down language added but still raised
- **Campaign duty factor anchoring** (GPT #2) — Persistent across versions

### What Regressed
- **Claude Clarity: 3→2 (Below Average)** — Critical regression. Claude now calls paper "nearly impenetrable" and wants 20-25% reduction. DL additions (timing ledger, falsification, γ domain, election interaction) increased density.

### New Issues in DL
- **GPT #1: Alternative TDMA designs** — Wants multi-packet burst, tracking mode, ACK compression alternatives. Claims 35 kbps conclusion is artifact of single slot structure.
- **GPT #7: Feasibility threshold arbitrary** — Wants requirement-driven thresholds (AoI P99, command delivery probability) instead of 1% deadline miss proxy.
- **Claude #3: Presentation density** (re-raised as major) — Was resolved in DK, now back with force. "Excessive defensive annotation," "redundancy," wants 20-30% cut.

## Strategic Analysis

### Core Tension
GPT wants **more content** (alternative TDMA designs, sensitivity plots, requirement-driven thresholds). Claude wants **aggressive compression** (20-25% reduction, move derivations to appendices). These are directly contradictory.

### Resolution Strategy for DM
**Prioritize Claude's Clarity concern** — it's the most actionable and affects the most ratings. A shorter, cleaner paper will also satisfy Gemini (stable) and may shift GPT's perception.

### Priority Actions for DM

1. **Aggressive compression (~80-100 lines)** — Target 900 lines / 11-12 pages
   - Remove or compress thundering herd analysis (tangential per Claude #4 minor)
   - Remove Table capability_matrix (context-setting, not essential)
   - Compress DES to 1 paragraph (addresses Claude #1, GPT #5)
   - Compress GE sensitivity details
   - Remove repeated numerical results (35 kbps appears 8+ times per Claude)
   - Compress fleet reuse section
   - Consolidate inline caveats into single "Assumptions" subsection

2. **Add alternative TDMA table (compact)** — 10 lines max
   - GPT #1: Show γ under 2-3 alternative slot structures (multi-packet burst, tracking mode)
   - This is cheap to add analytically and addresses GPT's strongest new concern

3. **Add requirement mapping for 1% threshold** — 3-4 lines
   - GPT #7: Map 1% deadline miss to AoI P99 and command delivery requirements
   - Brief justification, not a new analysis

4. **Shorten abstract to ≤200 words**

5. **Remove redundant numerical repetitions** — State key results once, cross-reference thereafter

### What to Defer (Cannot Fix with Text)
- External validation (NS-3, DVB-RCS2 benchmarking) — out of scope for text edits
- Empirical GE parameters — no data available
- Full RF simulation for R=7 — out of scope

### Expected Impact
- Claude: Clarity 2→3-4 (if compression succeeds), potentially resolves #1 (DES compressed) and #3 (density)
- GPT: Address #1 (alternative TDMA) and #7 (threshold mapping), potentially dropping 2 majors
- Gemini: Maintain Accept with Minor

## Issue Tracking

| # | Issue | Source | Priority | Action |
|---|-------|--------|----------|--------|
| 1 | Presentation density / length | Claude #3 | **CRITICAL** | Aggressive compression: 988→~900 lines |
| 2 | DES overemphasis | Claude #1, GPT #5 | HIGH | Compress to 1 paragraph + footnote |
| 3 | Alternative TDMA designs | GPT #1 (NEW) | HIGH | Add compact comparison table |
| 4 | Feasibility threshold arbitrary | GPT #7 (NEW) | MEDIUM | Add requirement mapping paragraph |
| 5 | No external validation | Claude #2, GPT #6 | DEFERRED | Cannot fix with text |
| 6 | Campaign duty factor anchoring | GPT #2 | LOW | Already addressed in DK/DL |
| 7 | γ subscript consistency | GPT #3 | LOW | Audit pass |
| 8 | Three-layer formalization | GPT #4 | MEDIUM | Formal definition paragraph |
| 9 | R=7 reuse | Claude #5, Gemini #1 | LOW | Already scoped-down in DL |
| 10 | γ applicability | Claude #4 | LOW | Already added in DL |
| 11 | T_acq abstract caveat | Gemini #2 | LOW | Add to abstract/conclusion |
| 12 | Unicast latency context | Gemini #3 | LOW | Add 1-sentence clarification |
