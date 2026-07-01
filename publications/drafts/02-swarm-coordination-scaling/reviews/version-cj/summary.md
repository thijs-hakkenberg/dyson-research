# Version CJ Review Summary

## Recommendations

| Reviewer | Recommendation | Change from CI |
|----------|---------------|----------------|
| Gemini 3 Pro | **Accept with Minor Revisions** | Maintained |
| GPT-5.2 | **Major Revision** | Maintained |
| Claude Opus 4.6 | **Major Revision** | Maintained |

## What CJ Fixed (Acknowledged by Reviewers)

1. **Rate ladder table** — GPT and Gemini both acknowledge the improved rate narrative (Table V)
2. **V&V language sharpened** — Claude notes "bold-faced caveats" and "commendable transparency"; all three note improved code verification vs validation distinction
3. **Screening heuristic demoted** — GPT notes the 0.50 threshold is now labeled heuristic with empirical sweep
4. **Acquisition amortization** — GPT acknowledges per-slot vs per-superframe bounding
5. **Safety-criticality argument** — Claude notes deep-space/cislunar extension
6. **GE language softened** — All three note ARQ infeasibility now qualified "under assumed parameterization"
7. **MMPP queueing** — Claude notes the analytical sketch and DES consistency
8. **ALOHA back-off** — Gemini notes it still needs stronger integration
9. **γ calibration checklist** — GPT notes it exists but wants more worked examples
10. **Practitioner d/q recipe** — GPT acknowledges but wants recommended default model

## Major Issues Remaining

### Priority 1: γ Computation Inconsistency (Claude Major #5, GPT Major #1)
The 0.760 vs 0.765 discrepancy (0.7%) is concerning when margin is 2.9%. Need single computation path with full precision. Remove rounding from multiplicative decomposition.

### Priority 2: Formalize Feasibility as 3-Step Workflow (GPT Major #2)
Paper says "two-layer" but effectively has three steps: byte budget → rate/efficiency → TDMA timing. Formalize consistently. Ensure η/γ is never presented as a feasibility test.

### Priority 3: DES Mean-Value Verification Still Too Prominent (Claude Major #1, GPT Major #5)
Move <0.1% agreement to appendix or single sentence. Lead with distributional/buffer results. Add buffer sizing factor rule from DES tails.

### Priority 4: Packet-Level Language — "Anchoring" Not "Validation" (Claude Major #2, GPT Major #6)
Relabel in claim map and narrative. Justify Proximity-1 as conservative stand-in for ISL.

### Priority 5: Abstract/Conclusion Scope Claims (Claude Major #3)
Add explicit statement that results are preliminary design estimates, not externally validated predictions.

### Priority 6: Campaign Duty Model Defaults (GPT Major #3)
Provide recommended conservative default duty model for sizing. Add mapping table from mission phases to (d, L_on, correlation scope).

### Priority 7: GE Parameter Mapping Formula (GPT Major #4)
Add p_BG ≈ T_c/T_B mapping. Move default GE point out of "representative instantiation" label. Add P95 vs T_c sensitivity.

### Priority 8: γ Worked Examples for Generality (GPT Major #7, Claude Major #4)
Add a second worked γ example (different payload/FEC/acquisition). Present time-domain form as primary.

## Minor Issues (23 total)

### Gemini (4 minor)
1. α_RX definition: generalize or note as example value
2. Figure 6 (AoI) y-axis labeling
3. Info-rate vs PHY-rate qualification in Section IV-J
4. Reference URL accessibility

### GPT (8 minor)
1. "1 kbps regime" → "1 kbps per-node budget regime" consistently
2. Slot time/γ numeric reconciliation (same as Major #1)
3. Table labeling: info-rate vs PHY-rate columns
4. AoI P99 is sampling policy tail, not network latency — clarify
5. Centralized baseline: consider adding comms-limited variant
6. Unicast staggering: clarify serialization assumption
7. Evidence tier table: add "depends on γ?" column
8. Non-archival citations: replace where possible

### Claude (12 minor)
1. Table I: add R_FEC, O_frame, T_payload definitions
2. Reference [19] Iridium: 1995 paper predates NEXT by 20 years
3. Global-state mesh 73 MB calculation: show explicitly
4. Collision avoidance msg: screening alert vs maneuver command
5. Eq. 7 floor vs ceiling for conservative sizing
6. Fig. 4 phase stagger: verify figure file exists
7. AoI geometric sampling: acknowledge threshold-crossing would differ
8. Algorithm 1 line 7: make control flow explicit (heuristic is informational)
9. J2 perturbation: clarify analytical vs simulation
10. Runtime inconsistency: ~7s vs 0.2–7s
11. Table VI: specify which γ in header
12. Fleet-wide TDMA cost 0.28 kbps/node: show calculation

## Progress Trajectory

| Version | Gemini | GPT | Claude |
|---------|--------|-----|--------|
| CI | Accept w/ Minor (3M/4m) | Major Revision (7M/7m) | Major Revision (4M/11m) |
| CJ | **Accept w/ Minor (3M/4m)** | **Major Revision (7M/8m)** | **Major Revision (5M/12m)** |

**Assessment:** Gemini maintained Accept with only presentation-level concerns. GPT and Claude both maintained Major Revision, but concerns are increasingly focused on *precision and presentation* rather than *missing content*: γ numerical consistency, feasibility framework formalization, DES restructuring, and practitioner packaging. The core technical content is largely accepted; the path to Accept requires (1) resolving the γ computation path, (2) tightening the narrative, and (3) adding a few more worked examples for generality.

## Recommended Next Steps for CK

1. **Unify γ computation**: adopt time-domain Eq. 15 as authoritative, carry full precision, reconcile all tables
2. **Formalize 3-step feasibility**: L1 byte budget → L2 rate/efficiency → L3 TDMA timing
3. **Compress DES mean-value verification**: single sentence + supplementary reference
4. **Relabel packet-level as "parameter anchoring"** in claim map and narrative
5. **Add scope limitation to abstract/conclusion**: "preliminary design estimates"
6. **Add recommended default duty model** and mission-phase mapping table
7. **Add p_BG ≈ T_c/T_B mapping formula** and default GE as "illustrative example"
8. **Add second γ worked example** (different payload/FEC) for generality
9. **Fix minor issues**: α_RX generalization, Iridium reference, AoI interpretation, consistent "per-node budget" language
