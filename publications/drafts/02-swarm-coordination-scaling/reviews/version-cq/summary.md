# Version CQ Review Summary

## Recommendations

| Reviewer | Recommendation | Change from CP |
|----------|---------------|----------------|
| Gemini 3 Pro | **Accept with Minor Revisions** | Stable (3M/5m; validity 5/5, clarity 5/5) |
| GPT-5.2 | **Major Revision** | Similar (7M/7m vs 6M/10m — more majors, fewer minors) |
| Claude Opus 4.6 | **Major Revision** | Stable (5M/14m; clarity 3/5) |

## What CQ Fixed (Acknowledged by Reviewers)

1. **Framework definition box** — Gemini: validity 5/5 ("meticulously distinguishes drops from misses"); GPT: "improvements over earlier versions" regarding double-counting. Claude: "welcome addition" for parameter dependency map. However: GPT still wants "two-layer" not "three-layer" language; Claude says box "interrupts flow."
2. **γ usage convention** — Abstract now says "γ≈0.74–0.76 (rate-dependent)". Claude: "consistently applied throughout." GPT: still wants full audit of rate dependence at 50 kbps.
3. **C_node sensitivity** — Added scaling statement (η∝1/C_node, 0.5→92%, 2→23%). Claude: "brief scaling argument" but wants systematic analysis at {0.5, 1, 2, 5, 10}. GPT: same.
4. **Table consolidation** — 18→13 tables, 1107→1003 lines, 13→12 pages. Claude: density concern persists ("20-30% reduction needed"). Gemini: clarity 5/5.
5. **γ-conditional guardrails** — Added k_c/S/T_c applicability and rescaling form. Claude minor #11: still notes it. GPT: no longer raises as major.
6. **Timing parameter provenance** — Added Provenance column + ranging amortization + robustness bound. GPT: no longer mentions as separate major. Claude minor #8: "largest unmodeled overhead deserves justification."
7. **Campaign mixture model** — Added 95%/4.9%/0.1% time-weighted mixture (η≈5.9%). Claude: "convincing." GPT: "good," still wants operational derivation.
8. **Multi-cluster RF interference** — Added geometric argument for R=3. Gemini: raises as Major #1 (wants tighter justification). GPT minor #5: "order-of-magnitude plausibility."
9. **DES positioning** — Replaced "validated" with "verified." Claude: still wants further reduction. GPT: same.
10. **§IV-J retitle** — Now "CCSDS-Grounded Slot Efficiency Calculation" with gap paragraph. GPT: still wants "parameter anchoring" in title. Claude: still wants Tier 2 downgrade.
11. **Sync beacon category** — Moved from Ingress to Egress in superframe table. No reviewer raises.
12. **N_R in notation** — Added. No reviewer raises.

## Major Issues Remaining

### Priority 1: γ Rate Dependence Audit (GPT #2 — ESCALATED)
**GPT Major #2.** γ₅₀=0.695 appears to *decrease* with rate, which is counterintuitive if overhead times are constant (γ should increase). Must explicitly define which terms are time-constant vs bit-constant. Provide decomposition at 30 and 50 kbps (currently only 24 kbps in Table 9). If γ₅₀ is computed with different assumptions, explain. **This undermines the central γ-conditional equation.**

### Priority 2: Two-Layer Not Three-Layer (GPT #3, Claude #4)
**GPT Major #3, Claude Major #4.** Despite the boxed definition saying "two-layer + unit conversion," the abstract/introduction still implies three layers. Consistently say "two-layer" everywhere. Present γ as a parameter of Layer 2, not a separate layer.

### Priority 3: C_node Systematic Sensitivity (Claude #2, GPT implicit)
**Claude Major #2.** The brief scaling text is insufficient. Need full feasibility algorithm traced at C_node ∈ {0.5, 1, 2, 5, 10} kbps showing rate ladder shift, margin, and ARQ feasibility for each. Would transform paper from single-point study to parametric tool.

### Priority 4: §IV-J → Parameter Estimation Not Validation (GPT #1, Claude #3)
**GPT Major #1, Claude Major #3.** Despite retitle, §IV-J is still positioned as "Tier 2 cross-model anchoring." Should be "standards-based parameter estimation." Add: "No implemented modem measurements used." Add γ uncertainty bounds (±0.07 from DVB-RCS2 range) and propagate through rate ladder.

### Priority 5: ACK-in-Guard Timing (GPT #6 — PERSISTENT)
**GPT Major #6.** Guard time is for uncertainty; consuming it for deterministic ACKs is only valid if guard budget explicitly includes a scheduled sub-slot. Need rigorous timing diagram or allocate explicit ACK time in the superframe.

### Priority 6: ARQ×TDMA Recommendation Conditionality (GPT #5)
**GPT Major #5.** 35 kbps recommendation is conditional on stop-and-wait ARQ under slow-mixing GE. Different ARQ (selective repeat, no intra-cycle ARQ) would change needed margin. Reframe as: "35 kbps if intra-cycle ARQ required; 30 kbps if inter-cycle only."

### Priority 7: DES Value Reduction (GPT #7, Claude #1)
**GPT Major #7, Claude Major #1.** DES mean-value verification is by construction. Lead with buffer/distributional results. Reduce DES prominence further.

### Priority 8: GE ISL Grounding (Claude #5)
**Claude Major #5.** Lutz/ITU references are for land-mobile channels, not ISLs. State explicitly. Provide first-principles mapping from ISL impairment mechanisms (shadowing duration → p_BG). Consider 3-5 representative parameter sets.

### Priority 9: Spatial Reuse R=3 (Gemini #1 — NEW)
**Gemini Major #1.** S-band is low-gain; 20 dB isolation at 10× cluster diameter may be optimistic with sidelobes and near-far effects. Need path loss vs interference threshold calculation or explicit assumption labeling.

### Priority 10: Re-association Under Cross-Plane (Gemini #2, Claude implicit)
**Gemini Major #2.** Static membership claim needs Abstract/Introduction qualification as "co-planar or co-moving." Already in Limitations but reviewers want it upfront.

### Priority 11: Thundering Herd Convergence (Gemini #3)
**Gemini Major #3.** BEB convergence at G≈25 within 640 ms needs justification. If G remains >1, channel could latch into collision state.

## Minor Issues (26 total)

### Gemini (5 minor)
1. Table I: α_RX — add numeric value (≈0.9) for quick reference
2. §IV-A: Clarify 614 ms (Model S, 24 kbps) vs 730 ms (Model C, 30 kbps) margin difference
3. Fig. 4: Clarify "Bernoulli d=0.10" as "Bernoulli (i.i.d.)"
4. Eq. 5: Can f_decision be fractional? Clarify
5. §IV-J: "doubles symbol time" → "doubles transmission duration"

### GPT (7 minor)
1. Ensure no residual γ=0.85 anywhere
2. Table 11: explain why γ decreases with rate, or fix
3. Algorithm 1: clarify p_cmd vs d double-gating semantics
4. Baseline telemetry: directional consistency with egress budget
5. Spatial reuse: label as "order-of-magnitude assumption"
6. AoI: clarify timescale relevance to conjunction assessment
7. "Mega-constellations" vs "swarms" vs "fleets" — define

### Claude (14 minor)
1. Abstract: "three-layer" → "two-layer"
2. Table I: α_RX is deterministic function, not free variable
3. Eq. 1: state uniform k_c/k_r assumption
4. §III-B-2: clarify 512 B summary vs 1024 B region summary earlier
5. Table VII: Model S label should be in title, not footnote
6. Eq. 6: justify serialized Raft voting assumption
7. Phase stagger: "zero drops at ≥25 kbps" is significant — elaborate
8. Table VI: acq variability 10 ms needs justification or reference
9. §IV-E: d mapping from ESA statistics is loose (10 maneuvers → d≈0.00002 ≪ 0.10)
10. Non-archival refs [3], [17], [18], [24]
11. §V-C: γ-conditional lookup should note k_c/S/T_c applicability
12. Eq. 7: framing bits FEC-encoded — state explicitly
13. Thundering herd BEB convergence needs justification
14. §III-E: ALOHA comparison not meaningful under TDMA — rephrase

## Progress Trajectory

| Version | Gemini | GPT | Claude |
|---------|--------|-----|--------|
| CJ | Accept w/ Minor (3M/4m) | Major (7M/8m) | Major (5M/12m) |
| CK | Accept w/ Minor (3M/5m) | Major (7M/7m) | Major (5M/13m) |
| CL | Accept w/ Minor (2M/3m) | Major (9M/8m) | Major (5M/11m) |
| CM | Accept w/ Minor (3M/4m) | Major (8M/7m) | Major (5M/12m) |
| CN | Accept w/ Minor (3M/4m) | Major (7M/10m) | Major (5M/12m) |
| CO | Accept w/ Minor (3M/5m) | Major (7M/7m) | Major (5M/12m) |
| CP | Accept w/ Minor (3M/5m) | Major (6M/10m) | Major (5M/12m) |
| **CQ** | **Accept w/ Minor (3M/5m)** | **Major (7M/7m)** | **Major (5M/14m)** |

**Assessment:** CQ consolidated content (18→13 tables, 1107→1003 lines, 13→12 pages) without sacrificing substance — Gemini maintained Accept w/ Minor with improved validity (5/5) and clarity (5/5). The framework definition box was partially accepted. However, GPT and Claude remain at Major Revision with persistent structural concerns.

Key patterns across 8 versions:
- **Gemini consistently accepts** with minor boundary-condition requests
- **GPT's major count oscillates 6-9**: new concerns appear as old ones resolve. The γ rate-dependence audit (Priority 1) is new and fundamental.
- **Claude's 5 majors are stable**: DES validation, C_node sensitivity, §IV-J framing, three-layer confusion, GE grounding. Minor count slightly increased (12→14).

**Diagnosis: The paper is approaching a structural ceiling.** GPT and Claude's "Major Revision" recommendations are driven by *category* concerns (no external validation, GE not calibrated, C_node not swept) rather than *fixable errors*. Some require new simulation data (NS-3, multi-C_node sweep) or external measurements (ISL GE parameters) that are beyond the scope of text edits.

## Recommended Strategy for CR

### Achievable via Text Edits (Priority)

1. **γ rate dependence fix** (GPT #2) — The γ₅₀=0.695 value in Table rate_feasibility needs explanation or correction. If guard/acquisition scale with rate, state explicitly. Add decomposition footnote for 30 and 50 kbps. This is the highest-priority fix as it questions internal consistency.

2. **Two-layer terminology** (GPT #3, Claude #4) — Global search-replace "three-layer" with "two-layer." Present γ as Layer 2 parameter consistently.

3. **§IV-J → "parameter estimation"** (GPT #1, Claude #3) — Change claim map Tier 2 to "parameter estimation." Add sentence: "No implemented modem measurements are used."

4. **γ uncertainty propagation** (Claude #3) — Add ±0.07 uncertainty from DVB-RCS2 range: "at γ = 0.745 ± 0.07: R_PHY,min = 27–33 kbps."

5. **ACK timing resolution** (GPT #6) — Either: (a) allocate explicit 0.5 ms ACK in superframe and recompute margin (730→729.5 ms, negligible), or (b) state guard budget includes scheduled control sub-slot with residual 4.2 ms for uncertainty.

6. **35 kbps conditionality** (GPT #5) — Reframe: "35 kbps if intra-cycle ARQ needed under slow-mixing loss; 30 kbps minimum if inter-cycle-only recovery acceptable."

7. **Re-association in abstract** (Gemini #2) — Add "co-planar or co-moving formations" qualifier.

8. **Spatial reuse caveat** (Gemini #1) — Strengthen to "order-of-magnitude plausibility; NS-3 required."

9. **ALOHA comparison fix** (Claude minor #14) — Remove or rephrase.

10. **Minor batch** — α_RX numeric, f_decision clarification, framing FEC note, ESA d mapping tightened, thundering herd BEB note.

### NOT Achievable Without New Work (Defer/Acknowledge)

- Full C_node parametric sweep (requires rerunning Algorithm 1 at 5 values)
- DES buffer→drop→AoI impact chain (requires new simulation runs)
- 3-5 GE parameter sets with first-principles mapping (requires literature analysis)
- NS-3 multi-cluster RF validation
- Hardware γ measurements

### Expected Outcome
With text edits above, expect: Gemini maintained at Accept; GPT might drop 7→5 majors (fixing γ inconsistency + two-layer + ACK + conditionality resolves 4); Claude might drop 5→4 (§IV-J + framework fixes resolve 2, C_node and DES still persist). Moving GPT/Claude to Minor will likely require new simulation data.
