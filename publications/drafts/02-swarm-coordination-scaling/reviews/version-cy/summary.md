# Version CY Review Summary

## Recommendations

| Reviewer | Recommendation | Change from CX |
|----------|---------------|----------------|
| Gemini 3 Pro | **Accept with Minor Revisions** | Regressed (2M/4m→3M/4m) |
| GPT-5.2 | **Major Revision** | Regressed (7M/7m→7M/10m) |
| Claude Opus 4.6 | **Major Revision** | Slightly improved (5M/14m→5M/13m) |

## What CY Fixed (Acknowledged by Reviewers)

1. **γ as parameter not layer** — Claude: "The boxed framework correctly states that γ is 'a parameter within Test B' and that C_raw = C_coord,info/γ is 'a unit conversion embedded in Test B, not a third check.'" GPT: "the boxed definition correctly states two tests (A and B) with γ as a parameter inside B." Both acknowledge the correct framing but still find "three-layer" language elsewhere.
2. **Dual coherence-regime recommendation** — Claude: "Present the dual coherence-regime recommendation more prominently." This was added but Claude wants it elevated further.
3. **Orbit-raising worked example** — Claude: "The yearly mixture calculation (η̄ = 5.6%) and mission-phase mapping (Table 7) are convincing." GPT: "stress-case is clearly labeled as continuous-duty upper bound."
4. **DVB-RCS2 transferability** — GPT: "you should more explicitly delineate which aspects transfer (burst framing overhead) and which do not." The transferability note was partially acknowledged.
5. **γ uncertainty propagation** — Added T_acq±2ms, T_guard±1ms ranges. Claude wants wider range [0.65, 0.82].
6. **ARQ provisioning policy** — Clarified worst-case reserved slots vs expected demand. GPT still finds mixing.
7. **Abstract reframe** — "1 kbps time-averaged per-node traffic allocation" and "35 kbps burst-rate PHY channel" framing. Gemini still wants more clarity.

## Gemini Regression Detail (2M→3M)

CX→CY changes:
- CX Major #1 (RF-backup ConOps) → **RETURNED** as CY Major #3 despite fix text being present. Stochastic — the CW fix was acknowledged in CX but CY re-raises it.
- CX Major #2 (R=3 spatial reuse) → Persistent as CY Major #1
- NEW: CY Major #2 (γ Doppler sensitivity) — Wants Doppler budget within 4.7 ms guard time

## Major Issues Remaining

### Priority 1: Three-Layer vs Two-Test (GPT #3, Claude #3 — PERSISTENT TERMINOLOGY)
All three reviewers acknowledge the boxed definition correctly says "two tests" but still find "three-layer" implicit language. GPT: "the 'rate ladder' and 'raw conversion' risk being interpreted as a third check." This may be unfixable with text edits — the readers project a three-layer structure even when the text says two tests.

### Priority 2: GE Coherence Tautology (GPT #2 — PERSISTENT)
GPT wants sub-cycle GE transitions or a coherence-granularity parameter m. This requires new simulation data.

### Priority 3: γ Unification Leak Paths (GPT #1 — PERSISTENT)
Table IV-D (ARQ coupling) is Model S only. GPT wants Model C coupling results or the table reframed as purely pedagogical. This requires rerunning the slot simulator.

### Priority 4: d Workload Realism (GPT #4 — PERSISTENT)
Wants sensitivity plot η vs (d, S_cmd, p_cmd). The orbit-raising worked example was acknowledged but insufficient — needs a compact parametric sweep.

### Priority 5: DES Value (GPT #5, Claude #1 — PERSISTENT STRUCTURAL CEILING)
Both want either additional burst model or DES reduced to ~1 page. Claude: "~3 pages of DES that add little."

### Priority 6: §IV-J Validation Language (GPT #6, Claude #2 — PERSISTENT)
GPT wants "standards-anchored parameterization" everywhere. Claude wants Table 10 column header changed.

### Priority 7: γ Measurement Recipe (GPT #7 — PERSISTENT)
Wants parameter sourcing table and worked examples for two modem architectures. Already partially addressed by acquisition architecture paragraph.

### Priority 8: 1 kbps Justification (Claude #4 — PERSISTENT)
Wants link budget uncertainty analysis. If per-node budget is 5 kbps, TDMA analysis is non-binding.

### Priority 9: Static Cluster Membership (Claude #5 — EVOLVED)
Wants parametric expression for re-association overhead vs differential precession rate.

### Priority 10: R=3 Spatial Reuse (Gemini #1 — PERSISTENT)
Wants link budget calculation for 20 dB isolation claim.

### Priority 11: γ Doppler Sensitivity (Gemini #2 — NEW)
Wants Doppler budget within guard time.

### Priority 12: RF-Backup ConOps (Gemini #3 — RETURNED)
Re-raised despite CX fix. Stochastic regression.

## Minor Issues (27 total)

### Gemini (4 minor)
1. α_RX derived nature
2. GE M_r scalability note
3. Fig 4 Bernoulli/ON-OFF distinction
4. Typos (negative sign, ArXiv refs)

### GPT (10 minor — regressed from 7)
1. "~28 kbps" vs 30 kbps minimum reconciliation
2. α_RX notation table fixed value
3. ACK timing diagram/appendix
4. Cluster diameter sensitivity
5. Sectorized mesh "3.2% coverage" definition
6. Centralized baseline M/D/c scope
7. Figure extensions
8. "validated" vs "anchored" (still)
9. Algorithm 1 L_cmd consistency
10. Repository DOI/Zenodo

### Claude (13 minor — improved from 14)
1. Abstract implementation detail (T_acq, T_guard)
2. Table 1 γ values in notation
3. η vs η_total clarification
4. Thundering herd BEB independence
5. ACK 0.5 ms window verification
6. f_decision,max ≈ 24 derivation
7. AoI/TCA misleading
8. Table 7 CA d transition
9. Priority queueing guarantee
10. Reference [3] date
11. Eq 14 FEC encoding standard clause
12. Algorithm 1 Line 4 equivalence
13. Phase-stagger result buried

## Progress Trajectory

| Version | Gemini | GPT | Claude |
|---------|--------|-----|--------|
| CJ | Accept w/ Minor (3M/4m) | Major (7M/8m) | Major (5M/12m) |
| ... | ... | ... | ... |
| CV | Accept w/ Minor (3M/4m) | Major (6M/7m) | Major (5M/12m) |
| CW | Accept w/ Minor (2M/4m) | Major (7M/8m) | Major (5M/14m) |
| CX | Accept w/ Minor (2M/4m) | Major (7M/7m) | Major (5M/14m) |
| **CY** | **Accept w/ Minor (3M/4m)** | **Major (7M/10m)** | **Major (5M/13m)** |

**Assessment:** Regression for Gemini and GPT. The CY edits added content (orbit-raising example, uncertainty propagation, ARQ policy clarification, DVB-RCS2 transferability) that may have introduced new surface area for criticism while not resolving the core structural issues.

## Structural Ceiling Confirmed

After 16 versions (CJ–CY):
- **Gemini**: Oscillates 2-3 M, 3-5 m. Best: 2M (CL, CW, CX). Issues are R=3 and terminology.
- **GPT**: Locked at 6-7 M, 7-10 m. Has never gone below 6M. Core issues require new simulations (Model C coupling, sub-cycle GE, η sensitivity plot).
- **Claude**: Locked at 4-5 M, 11-14 m. Has never gone below 4M. Core issues require external validation (NS-3), link budget analysis, and 30% length reduction.

**Text-only edits have fully exhausted their potential.** Further improvement requires:
1. Running Model C ARQ coupling simulation (addresses GPT #1, #3)
2. Sub-cycle GE model or fast/slow quantitative comparison (GPT #2)
3. η sensitivity parametric sweep (GPT #4)
4. Link budget uncertainty table (Claude #4)
5. NS-3 validation (Claude #1 — long-term)

## Recommended Strategy

**Option A: Accept structural ceiling.** The paper is at Gemini Accept / GPT Major / Claude Major. Submit to venue. Gemini's Accept with Minor is the strongest signal; GPT and Claude's persistent majors are structural and would require significant new work (simulations, measurements) to resolve. This is typical of a good systems engineering paper that lacks experimental validation.

**Option B: New simulation work.** Run Model C coupling at 30/35 kbps, add η sensitivity sweep, add 1 kbps link budget uncertainty. This could move GPT to 5-6M and strengthen Gemini. Claude likely stays at 4-5M (NS-3 requirement).

**Option C: One more text-only round (CZ).** Target the stochastic regression items: re-emphasize RF-backup fix, audit all "three-layer" language, remove remaining "validated" uses, compress DES further. Expected outcome: Gemini back to 2M, GPT stable at 7M, Claude stable at 5M.

Recommend **Option C** as a quick cleanup, then **Option A or B** based on available time.
