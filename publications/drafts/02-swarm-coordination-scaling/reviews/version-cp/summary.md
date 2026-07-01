# Version CP Review Summary

## Recommendations

| Reviewer | Recommendation | Change from CO |
|----------|---------------|----------------|
| Gemini 3 Pro | **Accept with Minor Revisions** | Maintained (3M/5m; clarity 5/5!) |
| GPT-5.2 | **Major Revision** | Similar (6M/10m vs 7M/7m — fewer majors, more minors) |
| Claude Opus 4.6 | **Major Revision** | Similar (5M/12m; clarity 3→adequate — density concern) |

## What CP Fixed (Acknowledged by Reviewers)

1. **Link/mode disambiguation** — Gemini: clarity 5/5 (was 5/5, maintained); CP's enhanced Table mode_map with "Sizing" column accepted. GPT acknowledges "channel/mode map" but wants more formal boxed definition. Claude: "Table I is comprehensive."
2. **γ worked examples** — Table gamma_examples with 3 link configurations (S-band γ=0.745, Ka-band γ=0.422, proprietary γ=0.530) accepted by all three. GPT: "genuinely useful for practitioners." Claude: "Table IX demonstrates generalized γ expression."
3. **Buffer sizing table** — Table buffer_sizing accepted. GPT still wants design curves (sweep L_on, d, correlation). Claude doesn't flag buffer as major issue anymore.
4. **Model C/S labels** — "NOT FOR RECOMMENDATIONS" markers on Table joint_interaction, Fig gamma_vs_rate, and Eq. 2→15 cross-reference. Gemini: fully resolved. GPT minor #3: still wants more prominent caption. Claude: doesn't raise this as major.
5. **Message-size sensitivity** — Table msg_sensitivity accepted by all. Claude: no longer raises as major (was CO #6).
6. **§IV-J renamed** — Now "Standards-Based Parameter Anchoring." Claude still wants further retitle to "CCSDS-Grounded Slot Efficiency Calculation." GPT: "correctly states it is parameter anchoring, not validation."
7. **Static membership scoped** — "co-planar or near-co-planar" added. Gemini: wants more; Claude: wants per-cluster stats; GPT: no longer raises.
8. **Rate terminology** — Fully resolved across all versions since CO. No reviewer raises this.
9. **Stress-case pairing** — Duty factor d "properly framed as episodic" (Claude). GPT still wants campaign mixture model.
10. **f_decision in notation table** — Fixed. No reviewer raises.
11. **AoI upper bound qualifier** — Added. GPT still notes minor scope.
12. **Thundering herd units** — Fixed (/yr per cluster). Gemini still wants explicit BEB parameters in main text.

## Major Issues Remaining

### Priority 1: Framework Definition Box (GPT #1 — NEW EMPHASIS)
**GPT Major #1.** The three-layer feasibility decomposition (byte budget → γ conversion → TDMA airtime) needs a boxed formal definition: (a) η = information bytes above baseline, independent of PHY; (b) γ = TDMA slot-structure efficiency (payload/slot, FEC/framing/guard/acquisition ONLY, excluding contention); (c) Layer 2 = deterministic superframe feasibility. Add explicit "boundary conditions" paragraph: centrally scheduled TDMA, no inter-cluster interference, contention out-of-scope.

### Priority 2: γ Usage Convention Audit (GPT #2)
**GPT Major #2.** Abstract says "γ≈0.76" but computations use γ₃₀=0.745 and γ₂₄=0.761. Need strict convention: γ₃₀ when computing at 30 kbps, γ₂₄ at 24 kbps, never generic "≈0.76" except as coarse descriptor. Abstract/conclusion should use "γ≈0.74–0.76" or specifically γ₃₀=0.745.

### Priority 3: C_node Sensitivity Analysis (Claude #2 — NEW)
**Claude Major #2.** The 1 kbps per-node budget drives all quantitative results but is asserted without derivation. Need: rate ladder for C_node ∈ {0.5, 1, 2, 5} kbps showing how η values scale and PHY recommendation shifts. Table II partially addresses η but not PHY rate.

### Priority 4: Paper Density / Table Count (Claude #4 — RE-EMERGED)
**Claude Major (implicit, via clarity 3/5).** Paper now has 14 tables. Claude rates clarity 3/5 ("extraordinarily dense," "reads more like technical report," "~30% longer than typical IEEE T-AES"). Need to cut/merge tables. Candidates: merge feasibility-related tables, move some to appendix/supplementary.

### Priority 5: Stress-Case Campaign Mixture (GPT #3)
**GPT Major #3.** d=0.10 "conservative default" needs credible campaign distribution. Provide: (a) yearly timeline illustration with ON/OFF campaigns, or (b) conservative mixture model (e.g., 95% routine d=0.01, 4.9% reconfig d=0.10, 0.1% emergency d=1.0).

### Priority 6: DES Design Curves (GPT #4, Claude #1)
**GPT Major #4, Claude Major #1.** DES reproduces equations by construction. Need to either: (a) elevate DES to produce reusable buffer-multiplier contour plots (P95/P99 vs L_on, d, correlation), or (b) reduce DES prominence to "implementation testing." Both reviewers suggest NS-3 but acknowledge it's out of scope.

### Priority 7: Timing Parameter Provenance (GPT #5)
**GPT Major #5.** The 30/35 kbps recommendations depend on timing assumptions (ACK in guard, ranging 50 ms, acquisition 5 ms). Need: (a) "parameter provenance" table: each timing component with source (CCSDS standard / vendor typical / engineering assumption); (b) robustness bound: show feasibility at 30/35 kbps under +X% acquisition and +Y ms guard.

### Priority 8: γ-Conditional Lookup Guardrails (GPT #6)
**GPT Major #6.** The conditional PHY mapping (γ∈[0.70,0.80]→35 kbps) risks being applied outside assumed k_c=100, T_c=10s, S=256B regime. Need: explicit applicability caveat + scaled form R_PHY,min ∝ (k_c-1)S/(T_c·γ·α_RX) with guidance for different regimes.

### Priority 9: Multi-Cluster RF Interference (Claude #3 — NEW)
**Claude Major #3.** At N=10⁵ with k_c=100, 1000 clusters share RF spectrum. Spatial reuse R=3 is assumed without interference analysis. Need: geometric argument for R=3 (minimum cluster separation vs interference range at S-band).

### Priority 10: §IV-J Further Retitle (Claude #4)
**Claude Major #4.** Retitle to "CCSDS-Grounded Slot Efficiency Calculation." Add paragraph on gap between calculated and measured γ, citing DVB-RCS2 measured efficiencies.

### Priority 11: Static Membership Per-Cluster Stats (Claude #5)
**Claude Major #5.** Re-association 0.014/orbit is fleet-wide mean. Per-cluster worst-case could be much higher for cross-plane clusters. Need per-cluster statistics or restrict to co-planar.

## Minor Issues (27 total)

### Gemini (5 minor)
1. Table I (Notation): γ definition cites Eq. 3 (Model S) instead of Eq. 12 (generalized)
2. §III-B.2: Clarify if thundering herd simulation models random backoff explicitly
3. Fig. 3: Caption describes panel (a) in detail but not panel (b)
4. Eq. 10 (AoI): Note correlated losses (GE) could increase worst-case AoI
5. Table III: Check unit consistency (μ_s in msg/s vs ms/msg)

### GPT (10 minor)
1. Abstract: "≈27 kbps at γ=0.76" — use γ₃₀=0.745 giving 27.1 kbps, or state range
2. Table IV (Notation): Ensure every later γ use is γ(R_PHY) consistently
3. Table X: Add sentence "not used in 30/35 kbps recommendation; qualitative only"
4. ACK "absorbed in guard" (Table VII footnote a): nonstandard — justify
5. Ranging 50 ms/node/cycle (Table VIII): clarify if amortized or per-cycle
6. "≥10 kbps no TDMA analysis needed": rephrase as conditional on contention-free
7. 73 MB/cycle global state: provide one-line derivation
8. Failure model: note correlated failures' effect on coordinator load
9. Algorithm 1 Line 3: clarify p_cmd vs d double-gating
10. Typographic: "kbps" vs "kbit/s" — adopt SI consistently

### Claude (12 minor)
1. Table VI "Model S ONLY" should be in table title, not just footnote
2. Eq. 6 (η_consensus): N_R not in Table I — add it
3. Thundering herd footnote: main-text or appendix (substantive content)
4. Table IX Ka-band: γ=0.422 surprisingly low — explain rate-1/2 LDPC choice
5. §IV-B AoI P99: conflates AoI freshness with TCA timeline — rephrase
6. Reference [3] Kuiper: "accessed February 2026" — verify
7. Abstract: "γ≈0.76" but body shows γ₂₄=0.761, γ₃₀=0.745 — note rate dependence
8. Algorithm 1 Line 3: η_total appears to omit heartbeat/summary — clarify η₀
9. Table VII: sync beacon listed under "Ingress (RX)" but labeled "TX" — fix category
10. "kbps" vs "bps" inconsistent formatting — use siunitx
11. Fig. 5 caption: describes panel (a) but not panel (b) markers
12. §V-C: γ-conditional lookup should note k_c=100, S=256B, T_c=10s applicability

## Progress Trajectory

| Version | Gemini | GPT | Claude |
|---------|--------|-----|--------|
| CJ | Accept w/ Minor (3M/4m) | Major (7M/8m) | Major (5M/12m) |
| CK | Accept w/ Minor (3M/5m) | Major (7M/7m) | Major (5M/13m) |
| CL | Accept w/ Minor (2M/3m) | Major (9M/8m) | Major (5M/11m) |
| CM | Accept w/ Minor (3M/4m) | Major (8M/7m) | Major (5M/12m) |
| CN | Accept w/ Minor (3M/4m) | Major (7M/10m) | Major (5M/12m) |
| CO | Accept w/ Minor (3M/5m) | Major (7M/7m) | Major (5M/12m) |
| **CP** | **Accept w/ Minor (3M/5m)** | **Major (6M/10m)** | **Major (5M/12m)** |

**Assessment:** CP made meaningful progress on technical content — three new tables (gamma_examples, buffer_sizing, msg_sensitivity) accepted by all reviewers. GPT major count dropped 7→6. However, the additions pushed page count to 13 and table count to 14, triggering Claude's density concern (clarity 3/5). GPT raised minor count 7→10, suggesting new editorial attention needed.

Key insight: **the paper has hit diminishing returns on adding content**. Further tables/subsections risk a density spiral — adding material to satisfy one reviewer while triggering length/density complaints from another. CQ strategy must be **net-negative on content volume**: every addition must be offset by larger cuts.

## Recommended Strategy for CQ

### Constraint: Net-Negative Content Volume
Every addition must be offset by cuts ≥1.5× the added lines. Target: ≤12 pages, ≤12 tables.

### Priority Edits

1. **Framework definition box** (GPT #1) — Add compact boxed definition (~8 lines). Cut: merge Tables joint_interaction + rate_feasibility context into prose (~-10 lines). **Net: -2 lines.**

2. **γ usage convention** (GPT #2) — Replace "γ≈0.76" with "γ₃₀=0.745" in abstract/conclusion. Add 1-line convention statement. **Net: 0 lines.**

3. **C_node sensitivity** (Claude #2) — Add 1 row to existing Table msg_sensitivity showing C_node sweep, or add compact 4-row inline display. Cut: remove Table buffer_sizing (fold key numbers into footnote) if needed. **Net: 0-3 lines.**

4. **Table consolidation** (Claude #4) — **CRITICAL for density.** Merge targets:
   - Merge Table msg_sensitivity + Table bandwidth_scaling → single "Parameter Sensitivity" table
   - Merge Table buffer_sizing into DES section text (2 sentences)
   - Merge Table gamma_examples into §IV-J paragraph
   - Target: 14 → 11 tables. Save ~30 lines.

5. **γ-conditional lookup guardrails** (GPT #6, Claude minor #12) — Add 1 sentence stating k_c/S/T_c applicability + scaled form. **Net: +2 lines.**

6. **Timing parameter provenance** (GPT #5) — Add "provenance" column to existing Table margin_analysis. **Net: +1 column, 0 lines.**

7. **Campaign mixture model** (GPT #3) — Add 1 compact sentence with conservative mixture (95%/4.9%/0.1%). **Net: +2 lines.**

8. **Multi-cluster RF interference** (Claude #3) — Add 2-sentence geometric argument for R=3. **Net: +3 lines.**

9. **DES positioning** (GPT #4, Claude #1) — Replace "DES-validated" with "DES-verified" everywhere. Compress DES section further. **Net: -3 lines.**

10. **§IV-J retitle** (Claude #4) — Retitle to "CCSDS-Grounded Slot Efficiency" + add 1 sentence on calculated-vs-measured gap. **Net: +1 line.**

### Minor Fixes (batch)
- γ₃₀ in abstract/conclusion (GPT minor #1, Claude minor #7)
- N_R in notation table (Claude minor #2)
- Table VII sync beacon category fix (Claude minor #9)
- Algorithm 1 η₀ clarification (Claude minor #8)
- "≥10 kbps" conditional rephrase (GPT minor #6)
- ACK in guard justification (GPT minor #4)

### Expected Net: ~-25 lines → target ~1080 lines / 12 pages / 11 tables
