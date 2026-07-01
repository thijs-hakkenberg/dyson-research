# Version CI Review Summary

## Recommendations

| Reviewer | Recommendation | Change from CH |
|----------|---------------|----------------|
| Gemini 3 Pro | **Accept with Minor Revisions** | Maintained (was Accept w/ Minor) |
| GPT-5.2 | **Major Revision** | Maintained (was Major Revision) |
| Claude Opus 4.6 | **Major Revision** | Maintained (was Major Revision) |

## Score Summary (1-5 scale)

| Dimension | Gemini | GPT | Claude | Mean |
|-----------|--------|-----|--------|------|
| Significance & Novelty | 5 | 4 | 3 | 4.0 |
| Methodological Soundness | 5 | 3 | 3 | 3.7 |
| Validity & Logic | 4 | 3 | 4 | 3.7 |
| Clarity & Structure | 5 | 4 | 3 | 4.0 |
| Ethical Compliance | 5 | 4 | 5 | 4.7 |
| Scope & Referencing | 4 | 3 | 4 | 3.7 |

## What CI Fixed (Acknowledged by Reviewers)

1. **35 kbps design point** — Gemini and GPT both acknowledge the improved design point recommendation
2. **Campaign duty factor** — All three note the d parameter successfully contextualizes the 46% stress case
3. **CCSDS-grounded gamma** — γ derivation from standards is recognized as a genuine improvement
4. **Evidence tier framework** — Claude praises the "refreshingly honest" validation gap identification
5. **AI disclosure** — All rate ethical compliance highly
6. **Thundering herd** — Gemini notes the analysis but wants back-off strategy discussed
7. **Unicast latency** — Gemini accepts the broadcast/unicast separation but wants stronger framing

## Major Issues Remaining

### Priority 1: Rate Ladder Clarity (GPT Major #1)
The 27 kbps / 30 kbps / 35 kbps narrative needs a single canonical "rate ladder" table: info-rate → PHY-rate → schedule feasibility → recommended. Standardize "info-rate" vs "PHY-rate" labels everywhere.

### Priority 2: Circular Validation / Verification vs Validation (Claude Major #1, GPT Major #3)
All tools verify each other but none is validated externally. Reframe DES as "distributional/tail analysis" rather than "verification." The <0.1% agreement is code verification, not model validation. Consider any available external data (DVB-RCS2 measurements, Iridium NEXT stats).

### Priority 3: Screening Indicator Justification (GPT Major #2)
The η_total/γ < 0.50 threshold is called a "screening indicator" but has no derivation or empirical ROC-style justification. Either provide one or demote explicitly to "illustrative heuristic."

### Priority 4: Acquisition Per-Slot vs Per-Burst (GPT Major #4)
The 5 ms per-slot acquisition dwell is a strong assumption. Many systems amortize acquisition across bursts. Provide two bounding cases: per-slot (current) and per-superframe (amortized), show how design point shifts.

### Priority 5: Narrow Binding Regime (Claude Major #2)
TDMA analysis is binding only for 1 kbps RF-backup (<1% of lifetime). Either strengthen the safety-criticality argument or extend to deep-space/cislunar regimes where low rates are the norm.

### Priority 6: GE Model Empirical Grounding (Claude Major #3, GPT Major #6)
ARQ infeasibility conclusion rests on unvalidated GE parameters. Soften language to "under the assumed parameterization." Promote sensitivity sweep as primary result rather than point estimate.

### Priority 7: Stochastic Coordinator Queueing (Claude Major #4)
D[k_c]/D/1 is trivial; compound campaign + GE dynamics need a Markov-modulated arrival model (MMPP/D/1) for proper buffer sizing.

### Priority 8: ALOHA Back-off Strategy (Gemini Major #2)
Thundering herd analysis needs discussion of exponential back-off to ensure system exits saturation regime when >200 nodes share a channel.

## Minor Issues (25 total across reviewers)

### Gemini (4 minor)
1. Table I α_RX definition is case-specific; generalize or note
2. GE geometric justification: clarify antenna location (body vs panel)
3. Algorithm 1 line 7: justify the 0.50 threshold
4. Verify "Gilbert-Elliott" capitalization consistency

### GPT (7 minor)
1. γ_{C,24} numerical inconsistency (0.760 vs 0.765)
2. "MAC efficiency" vs "slot efficiency" terminology consistency
3. Eq. 52 C_raw: clarify C_coord is info-rate or PHY-rate
4. AoI: clarify "no deadline misses" condition
5. Fig. 16: visually separate compute-only baselines
6. Non-archival references: add archival alternatives where possible
7. Algorithm 1 line 7: align early check with time-feasibility check

### Claude (11 minor)
1. Inconsistent γ notation proliferation (γ, γ_S, γ_C, γ_{24}, etc.)
2. Table II vs Table IX threshold inconsistency
3. Eq. 6 η_canonical: make self-contained or reference full expansion
4. Section III-B-2: compound probability vs common-cause contradiction
5. Fig. 3: referenced before TDMA frame fully developed
6. Algorithm 1 line 7: "sufficient but not necessary" vs hard branch
7. Campaign scenarios: 10/yr collision rate may not scale to 10^5 nodes
8. Fig reference ordering in Section IV-C
9. Sectorized mesh: underdeveloped; either expand or remove
10. Reference [62]: mark as preprint per IEEE policy
11. Table I: §III-J section reference inconsistency

## Constructive Suggestions (High Impact)

1. **Rate ladder table** — Consolidate info-rate → PHY-rate → schedule feasibility → margin → recommendation (GPT)
2. **Acquisition amortization** — Per-slot vs per-burst bounding cases for T_acq (GPT)
3. **DES reframing** — Lead with distributional/tail analysis, deemphasize mean agreement (GPT, Claude)
4. **External comparison** — Any DVB-RCS2 or Iridium NEXT data, even approximate (Claude)
5. **Shorten paper** — 25-30% reduction; move sensitivity sweeps to supplement (Claude)
6. **Lead with generalized equations** — Restructure to put sizing equations + Algorithm 1 first, instantiation as worked example (Claude)
7. **Practitioner recipe for d, q** — How to estimate duty factor from operational concepts (GPT)
8. **γ calibration checklist** — Boxed workflow for computing γ for arbitrary systems (GPT)

## Progress Trajectory

| Version | Gemini | GPT | Claude |
|---------|--------|-----|--------|
| CH | Accept w/ Minor (3M/4m) | Major Revision (6M/10m) | Major Revision (5M/12m) |
| CI | **Accept w/ Minor (3M/4m)** | **Major Revision (7M/7m)** | **Major Revision (4M/11m)** |

**Assessment:** Gemini maintained Accept. GPT and Claude both maintained Major Revision, but the nature of their concerns has shifted from "missing content" to "tighter engineering logic and defensibility." The CI additions (35 kbps elevation, mode map, feasibility framework, GE coherence, correlated campaigns, thundering herd, unicast latency) were acknowledged but GPT/Claude now focus on: (1) clearer rate-ladder narrative, (2) verification vs validation distinction, (3) screening indicator justification, (4) acquisition assumption bounding. These are largely framing/presentation issues rather than fundamental content gaps.

## Recommended Next Steps for CJ

1. Add "rate ladder" summary table early in Section IV-A (info → PHY → time → margin → recommendation)
2. Add acquisition amortization bounds (per-slot vs per-burst T_acq) in Section IV-J
3. Restructure DES section to foreground distributional analysis, deemphasize mean agreement
4. Sharpen verification vs validation language throughout; add V&V note
5. Justify or demote the 0.50 screening indicator
6. Shorten: move sectorized mesh detail, extended sensitivity sweeps to supplement
7. Add ALOHA back-off discussion in thundering herd paragraph
8. Soften ARQ infeasibility language to "under assumed GE parameterization"
