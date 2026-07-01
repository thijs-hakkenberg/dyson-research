# Version CR Review Summary

## Recommendations

| Reviewer | Recommendation | Change from CQ |
|----------|---------------|----------------|
| Gemini 3 Pro | **Accept with Minor Revisions** | Improved (2M/4m vs 3M/5m; validity 4/5, clarity 5/5) |
| GPT-5.2 | **Major Revision** | Worsened (8M/10m vs 7M/7m — new concerns added) |
| Claude Opus 4.6 | **Major Revision** | Improved (4M/12m vs 5M/14m; validity 4/5 up from 3/5) |

## What CR Fixed (Acknowledged by Reviewers)

1. **γ rate dependence** — GPT: no longer raised as major (was Priority 1 in CQ). The explicit decomposition ("time-constant guard/acq, bit-proportional FEC/framing") resolved the counterintuitive concern. Gemini: not mentioned.
2. **Two-layer terminology** — Claude: three-layer confusion major is **DROPPED** (was Major #4 in CQ, not present in CR). GPT: still mentions (Major #1) but acknowledges "you emphasize a two-layer framework" — concern is now about Layer 2 naming and Algorithm 1 presentation rather than abstract/intro language.
3. **§IV-J reframing** — Claude: "correctly labels it as 'standards-based parameter estimate, not independent validation'" but still wants section title change and more prominent uncertainty. GPT: "manuscript states this" but wants stronger anchoring language everywhere.
4. **ACK timing** — GPT minor #5: "could be contentious" (downgraded from major). Claude: not raised.
5. **35 kbps conditionality** — Claude: not raised as separate major. GPT Major #7: still wants alternative ARQ comparison but acknowledges conditional framing.
6. **Re-association in abstract** — Gemini: major #2 now about unicast stagger context, not re-association (resolved). Claude: fleet-level scope is new major #3.
7. **Spatial reuse caveat** — Gemini: still Major #1 but weakened (wants INR calc). GPT minor #7: "label as order-of-magnitude" (already done). Claude: folded into fleet-level major #3.
8. **ALOHA comparison** — Claude: not raised. GPT: not raised. Resolved.
9. **ESA d mapping** — Claude: not raised as separate minor. GPT Major #3: still wants end-to-end operational derivation.
10. **Framing FEC note** — Claude minor #11: "stated in text but should be noted in equation context" (partially addressed). GPT: not raised.
11. **Thundering herd BEB** — Claude minor (footnote critique is about placement, not content). Gemini: not raised (was Major #3 in CQ, now dropped).

## Major Issues Remaining

### Priority 1: DES Verification Narrative Reduction (Claude #1, GPT #5)
**Claude Major #1, GPT Major #5.** DES mean-value verification is by construction. Both want: condense to one paragraph + one figure (buffer CDF); move DES architecture to appendix; expand distributional contribution with buffer multiplier rules.

### Priority 2: §IV-J Section Title and γ Uncertainty Presentation (Claude #2, GPT #6)
**Claude Major #2, GPT Major #6.** Despite "standards-based parameter estimate" language, section title still suggests validation. GPT: "validated via CCSDS phrasing remains too strong." Rename section. Present DVB-RCS2 measured range more prominently.

### Priority 3: Fleet-Level Scalability Scope (Claude #3 — NEW)
**Claude Major #3.** Per-cluster analysis with R=3 order-of-magnitude argument is insufficient for 10⁵-node claims. Either reduce scope to per-cluster sizing with fleet extension as future work, or provide rigorous fleet-level analysis.

### Priority 4: GE Model Grounding (Claude #4, GPT implicit)
**Claude Major #4.** No ISL-specific channel measurements. Wants derivation from link budget + ITU-R P.681, and family of curves as primary presentation. Persistent across all versions.

### Priority 5: Model S Leakage into Conclusions (GPT #2)
**GPT Major #2.** Table VII (joint interaction) uses Model S. Wants "Upper-bound timing model; not design-valid" watermark, or move to appendix. Add Model C/S map.

### Priority 6: Campaign Duty Factor d Operational Mapping (GPT #3)
**GPT Major #3.** d mapping still ad hoc despite ESA anchoring. Wants end-to-end worked example from published operational concept yielding d from first principles.

### Priority 7: Stress-Case η_S Presentation (GPT #4)
**GPT Major #4.** Still wants "time-at-load" chart and operational degradation description during stress bursts.

### Priority 8: Two-Layer vs Conversion Naming (GPT #1)
**GPT Major #1.** Despite two-layer language, γ conversion step can still be misinterpreted as third test. Wants Layer 2 renamed to "Airtime schedulability" and Algorithm 1 clarified.

### Priority 9: ARQ Policy Breadth (GPT #7)
**GPT Major #7.** Conditional framing acknowledged but wants explicit alternative policy comparison (inter-cycle-only as first-class option with AoI trade quantified).

### Priority 10: T_acq Taxonomy for Practitioners (GPT #8 — NEW)
**GPT Major #8.** Wants taxonomy table: cold-start per slot, reacquire per burst, continuous tracking with typical T_acq values and measurement recipe.

### Priority 11: Spatial Reuse R=3 (Gemini #1)
**Gemini Major #1.** Weakened: wants INR calculation with specific antenna beamwidth assumptions rather than general path loss argument.

### Priority 12: Unicast Stagger Operational Context (Gemini #2 — NEW)
**Gemini Major #2.** 190s unicast stagger needs operational constraint discussion. Clarify tight formation uses optical ISL; RF is for high-level orchestration only.

## Minor Issues (26 total)

### Gemini (4 minor)
1. α_RX: note includes retransmission slots
2. DVB-RCS2: explain why valid proxy for ISL
3. Fig. 5 (buffer CDF): ensure high contrast
4. Eq. 10: O_frame consistency with Table I

### GPT (10 minor)
1. "validated via CCSDS" → "anchored/derived"
2. Algorithm 1 p_cmd/d double-gating
3. α_RX "derived from schedule" circularity
4. 20.2 kbps: clarify k_c-1 (not k_c)
5. ACK-in-guard: add timing diagram or appendix
6. GE: intra-cycle ARQ ineffective by construction when τ_c ≥ T_c — state explicitly
7. R=3: label order-of-magnitude more prominently
8. AoI: mention formation keeping tighter loops → optical ISL
9. Reference hygiene (non-archival)
10. kbps units (info vs PHY) occasionally ambiguous

### Claude (12 minor)
1. α_RX derived quantity — more prominent notation
2. η_cmd standalone equation missing
3. Table VII: "MODEL S" in title
4. 512B summary: 371B metadata/CRC excessive — clarify
5. Eq. 10 f_decision: parallel decisions?
6. Fig. 3 axis labels insufficient
7. Phase stagger zero drops: no supporting data
8. Table IX d=1.0: clarify temporal scope (6 cycles)
9. Non-archival references
10. Abstract: reorder final sentences
11. Eq. 8 framing FEC: note at equation level
12. §V-C J2 analysis: move to appendix

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
| CQ | Accept w/ Minor (3M/5m) | Major (7M/7m) | Major (5M/14m) |
| **CR** | **Accept w/ Minor (2M/4m)** | **Major (8M/10m)** | **Major (4M/12m)** |

**Assessment:** CR made targeted fixes (γ rate dependence, two-layer terminology, §IV-J reframing, ACK timing, conditionality, spatial reuse caveat, ALOHA fix, ESA d mapping). Results:

- **Gemini improved** (3M→2M, 5m→4m; validity 4/5 up from 5/5→same): thundering herd major dropped (was #3 in CQ), re-association major resolved. New: unicast stagger context (minor-level concern elevated to major).
- **Claude improved** (5M→4M, 14m→12m; validity 4/5 up from 3/5): three-layer confusion **resolved** (was Major #4 in CQ). Fleet-level scalability crystallized as new major #3. §IV-J acknowledged correctly reframed but wants title change.
- **GPT worsened** (7M→8M, 7m→10m): γ rate dependence resolved, but two NEW majors added: T_acq taxonomy (#8, wants measurement recipe) and strengthened Model S watermarking (#2). Multiple minors added for things already partially addressed.

**Structural ceiling confirmed.** GPT's major count has oscillated 6-9 across 9 versions. Each time an issue resolves, GPT adds 1-2 new concerns. The pattern suggests GPT's review model has a ~7-8 major floor for papers without external validation. Claude's 4-5 major floor is driven by category gaps (no external validation, no GE calibration, no C_node sweep). These require new simulation data or measurements that cannot be achieved via text edits alone.

## Recommended Strategy for CS

### Achievable via Text Edits (Priority)

1. **§IV-J title rename** (Claude #2, GPT #6) — Change "CCSDS-Grounded Slot Efficiency Calculation" to "Slot Efficiency Parameter Estimation from CCSDS Framing." Check for any residual "validated" language.

2. **DES narrative compression** (Claude #1, GPT #5) — Condense DES verification to 1 sentence. Move DES architecture details to a footnote. Lead with distributional/buffer contribution. Add buffer multiplier rule: "1.3× mean at d=0.10, 1.5× at d=0.50."

3. **Model S watermark** (GPT #2) — Add "MODEL S (not for design)" to Table VII title. Add 1-line Model C/S map note in Section IV.

4. **T_acq taxonomy** (GPT #8) — Add 3-line taxonomy in §IV-J: cold-start per slot (5 ms), reacquire per burst (2 ms), continuous tracking (per-superframe, 5 ms once). Already partially covered by "Acquisition architecture as design axis" paragraph.

5. **Fleet-level scope reduction** (Claude #3) — Reframe abstract/contributions to "per-cluster sizing with fleet-level extension." Add explicit qualifier: "Fleet-level scaling (Eq. 14) is an order-of-magnitude estimate requiring NS-3 validation."

6. **Unicast stagger context** (Gemini #2) — Add sentence: "Tight formation control uses optical ISL (T_c/2 = 5 s); the RF coordination channel handles orchestration-level commands where 190 s latency is acceptable."

7. **Stress degradation** (GPT #4) — Add 2-3 sentences describing what happens during stress bursts: "Buffer occupancy peaks, AoI increases by 1-2 cycles, command latency increases proportionally to d; safety-critical broadcasts remain single-cycle."

8. **Minor batch** — "validated via CCSDS" audit, p_cmd/d semantics clarification, Table VII title, η_cmd equation, DVB-RCS2 proxy explanation, R=3 INR estimate, GE τ_c by-construction note, abstract sentence reorder.

### NOT Achievable Without New Work (Defer/Acknowledge)

- NS-3 single-cluster validation (Claude #1 constructive, GPT implicit)
- GE derivation from link budget + ITU-R P.681 (Claude #4)
- Full C_node parametric sweep
- Buffer multiplier as function of d, L_on, GE params (requires new DES runs)
- Alternative ARQ policy comparison in slot-sim (GPT #7)
- Fleet-level time-varying reuse under orbital geometry

### Expected Outcome
With text edits above, expect: Gemini maintained at Accept (2→1-2 majors); Claude might drop 4→3 majors (§IV-J title + fleet scope fixes resolve 1-2); GPT might drop 8→6-7 majors (Model S watermark + T_acq taxonomy + DES compression resolve 2-3, but GPT tends to add new concerns). Moving GPT/Claude to Minor Revision will likely require at minimum one external validation point (NS-3).
