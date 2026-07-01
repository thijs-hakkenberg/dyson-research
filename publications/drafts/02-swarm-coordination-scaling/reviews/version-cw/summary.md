# Version CW Review Summary

## Recommendations

| Reviewer | Recommendation | Change from CV |
|----------|---------------|----------------|
| Gemini 3 Pro | **Accept with Minor Revisions** | **Improved (3M→2M; 4m stable)** |
| GPT-5.2 | **Major Revision** | Regressed (6M→7M; 7m→8m; stress returned) |
| Claude Opus 4.6 | **Major Revision** | Slight regression (5M stable; 12m→14m) |

## What CW Fixed (Acknowledged by Reviewers)

1. **§IV-J renamed to "Standards-Based Slot Efficiency Parameterization"** — Gemini no longer mentions it. GPT still wants to audit "validated via CCSDS" phrasing. Claude acknowledges the title is "accurate" but wants Tier 2 relabeled.
2. **γ-conditional lookup table (Table VII)** — Gemini: "immediately useful for systems engineers" (Practical Applicability: 5/5). This is Gemini's highest-rated aspect.
3. **1 kbps "baseline design target" framing** — Gemini dropped 1 kbps from majors (was CV Major #1). Now only Claude and GPT raise it.
4. **Thundering herd** — Gemini dropped from Major #3 to constructive suggestion. The ConOps clarification text worked partially, but Gemini now raises a related NEW concern about "suspended hierarchy vs election on backup link."
5. **Rate paradox note** — Gemini: "Higher rates transmit payload faster, making fixed guard times a larger percentage of the slot" acknowledged.
6. **Feasibility heuristic note** — GPT: "The manuscript also does a good job warning readers not to double-count heuristic vs. explicit TDMA checks."
7. **α_RX rate-dependence** — Claude: "I verified spot-checks: Table VI, the rate ladder (Table IV), Algorithm 1, and the feasibility summary (Table V) all use Model C values." γ unification confirmed.

## Gemini Improvement Detail (3M→2M)

Resolved:
- CV Major #1 (1 kbps justification) → Dropped (now "baseline design target" suffices)
- CV Major #3 (thundering herd) → Dropped (now constructive suggestion)

New:
- CW Major #1 (RF-backup ConOps) — Tension between "suspended hierarchy" and "Raft election on backup link." Wants clarification that election is a recovery transient, not steady-state.

Persistent:
- R=3 spatial reuse (now Major #2, was #2 in CV)

## Major Issues Remaining

### Priority 1: d Realism (GPT #1 — PERSISTENT)
**GPT Major #1.** Wants quantitative derivation: event counts, durations → implied d. At least one worked mission example. Table VII is "asserted"; needs arithmetic.

### Priority 2: γ Model S/C Confusion (GPT #2 — EVOLVED from "audit")
**GPT Major #2.** Model S ARQ×TDMA coupling table (Table IV-D) can be misread as design-relevant. Wants Model C coupling result or Model S moved to appendix.

### Priority 3: Stress Contextualization (GPT #3 — RETURNED)
**GPT Major #3.** "Paper still uses stress-case numbers in ways that read like expected operations." Wants standardized language: always prepend "continuous-duty bound" to η_S. Wants traceable "<1% of time" arithmetic.

### Priority 4: Three-Layer Framework (GPT #4 — PERSISTENT)
**GPT Major #4.** Still wants formalization: "two tests with embedded conversions." The boxed definition helped but "three-layer" language persists somewhere.

### Priority 5: DES Value (GPT #5, Claude #1 — STRUCTURAL CEILING)
**GPT Major #5, Claude Major #1.** Both want either additional burst model or DES moved to appendix. Claude: "single highest-impact improvement" would be NS-3 validation.

### Priority 6: §IV-J Language (GPT #6, Claude #2 — PERSISTENT)
**GPT Major #6.** "Replace 'validated via CCSDS' with 'anchored to CCSDS.'" Claude: relabel Tier 2 in claim map. Audit for "validated" language.

### Priority 7: γ Practitioner Guidance (GPT #7, Claude #5 — PERSISTENT)
**GPT Major #7.** Wants "parameter measurement protocol" box. Claude: wants dual coherence-regime results (τ_c ≥ T_c vs τ_c ≪ T_c) as co-equal design cases.

### Priority 8: RF-Backup ConOps (Gemini #1 — NEW)
**Gemini Major #1.** "If hierarchy is suspended, why is there a Raft election on the backup link?" Wants clarification: election is a recovery transient to restore S-band hierarchy, not an operational mode.

### Priority 9: Fleet-Level Claims (Claude #3, Gemini #2 — PERSISTENT)
**Claude Major #3, Gemini Major #2.** Both want either fleet-level analysis or scope restriction. Claude suggests title change to "per-cluster."

### Priority 10: 1 kbps Justification (Claude #4 — PERSISTENT)
**Claude Major #4.** Wants rigorous link budget derivation or present 2-5 kbps as nominal with 1 kbps as stress case.

### Priority 11: GE Coherence (Claude #5 — EVOLVED)
**Claude Major #5.** "Present results for both τ_c ≥ T_c and τ_c ≪ T_c as bounding cases." The 35 kbps recommendation should be conditioned on coherence regime (already done in conclusion but wants co-equal treatment).

## Minor Issues (26 total)

### Gemini (4 minor)
1. Table I γ equation reference consistency
2. Fig. 4 vertical line visibility
3. Eq. 12 T_framing encoded vs raw bits
4. "Analogous" vs "similar" for DVB-RCS2

### GPT (8 minor)
1. γ subscript standardization (γ_C vs γ_{C,24})
2. α_RX rate-dependence sentence
3. Table captions too long
4. AoI decision latency connection
5. Fleet reuse → γ degradation link
6. S_cmd sensitivity
7. Algorithm 1 η₀ = 5% hardcoded
8. "Validated" vs "evaluated" terminology

### Claude (14 minor)
1. Eq. 7 framing: ASM outside FEC codeword in Prox-1
2. p_exc subscript clarification
3. 512 B summary: 371 B metadata unexplained
4. Thundering herd: TDMA→Slotted ALOHA transition
5. Table V "—" means stagger, not infeasible
6. Phase-stagger finding buried in one sentence
7. Eq. 4 f_decision,max derivation
8. AoI TCA window comparison misleading
9. Abstract γ subscript convention
10. Reference [55] relevance
11. Table III CA rate "stress-test" vs "conservative"
12. J2 re-association units unclear
13. Algorithm 1 η₀ parameterization
14. Eq. gamma_time forward reference

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
| CR | Accept w/ Minor (2M/4m) | Major (8M/10m) | Major (4M/12m) |
| CS | Accept w/ Minor (3M/4m) | Major (6M/7m) | Major (5M/12m) |
| CT | Accept w/ Minor (3M/5m) | Major (7M/7m) | Major (5M/14m) |
| CU | Accept w/ Minor (3M/5m) | Major (7M/10m) | Major (5M/12m) |
| CV | Accept w/ Minor (3M/4m) | Major (6M/7m) | Major (5M/12m) |
| **CW** | **Accept w/ Minor (2M/4m)** | **Major (7M/8m)** | **Major (5M/14m)** |

**Assessment:** Mixed results. Gemini improved to best-ever 2M; GPT and Claude showed stochastic regression.

- **Gemini improved** from 3M→2M: 1 kbps and thundering herd both dropped from majors. The "baseline design target" framing and the γ-conditional lookup table were the most impactful additions. New ConOps concern (RF-backup vs election) is easily addressable. R=3 persists.

- **GPT regressed** from 6M→7M: the "stress contextualization" returned as a major despite the CV continuous-duty rename. This is likely stochastic — the rename is present but GPT still finds instances that "read like expected operations." The Model S ARQ coupling concern is new/evolved. Other majors are persistent structural issues.

- **Claude stable-to-slightly-regressed** at 5M/14m (was 12m). The GE coherence concern evolved into wanting dual-regime presentation. Minors increased by 2 (new: Prox-1 ASM outside FEC, CA rate terminology).

**Key insight:** GPT and Claude major counts have reached a structural floor. The remaining majors require either:
1. New simulation data (NS-3, alternative burst models)
2. Substantive new content (fleet interference analysis, 1 kbps link budget table, dual-regime ARQ)
3. Major structural changes (Model S to appendix, 30-40% length reduction)

Text-only edits have largely exhausted their potential for GPT/Claude. Gemini continues to improve incrementally.

## Recommended Strategy for CX

### Achievable via Text Edits

1. **RF-backup ConOps clarification** (Gemini #1 — NEW, easy fix) — Add sentence: "Raft election on UHF is a recovery transient to re-establish the S-band control plane; it is not a steady-state operation. During recovery, hierarchy is suspended and nodes operate in safe-hold; the election restores hierarchical coordination."

2. **Audit "validated" language** (GPT #6, Claude #2) — Search-replace any remaining "validated via CCSDS" with "anchored to CCSDS framing." Relabel Tier 2 in claim map.

3. **"<1% of time" arithmetic** (GPT #3) — Add: "At d = 0.10, full-load cycles occur 10% of time; at d_CA = 0.00002 (ESA), effectively 0%. Yearly mixture: 95% × 0 + 4.9% × 0.10 + 0.1% × 1.0 = 0.59% of cycles at full load."

4. **Three-layer → two-test language audit** (GPT #4) — Search for any remaining "three-layer" text and replace with "two-test with embedded conversions."

5. **Model S ARQ table caption** (GPT #2) — Add stronger caption: "Model S only (NOT for design); under Model C, 24 kbps is infeasible regardless of ARQ."

6. **Dual coherence-regime note** (Claude #5) — Strengthen existing text: "35 kbps if τ_c ≥ T_c (slow-mixing, ARQ ineffective); 30 kbps if τ_c ≪ T_c (fast-fading, ARQ effective at 98.9% delivery)."

7. **Table V footnote for "—"** (Claude Minor #5) — Change "—" to "stagger" or add footnote.

8. **Minor batch** — γ₃₅ in notation table; J2 units; Algorithm 1 η₀ note; f_decision,max derivation ref.

### NOT Achievable Without New Work

- NS-3 simulation
- Alternative DES burst model
- Fleet interference geometry analysis
- Rigorous 1 kbps link budget table
- Model S → appendix (structural change)
- 30-40% length reduction (too aggressive for single version)

### Expected Outcome
With text edits: Gemini might drop to 1M (RF-backup fix). GPT likely stable at 6-7M (structural floor). Claude stable at 5M. Further improvement requires new simulation data.
