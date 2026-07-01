# Version CV Review Summary

## Recommendations

| Reviewer | Recommendation | Change from CU |
|----------|---------------|----------------|
| Gemini 3 Pro | **Accept with Minor Revisions** | Stable (Significance 5→4; minors 5→4) |
| GPT-5.2 | **Major Revision** | **Improved (7M→6M; 10m→7m)** |
| Claude Opus 4.6 | **Major Revision** | Stable (5M/12m) |

## What CV Fixed (Acknowledged by Reviewers)

1. **24 kbps numerical inconsistency resolved** — GPT CU Minor #3 (11,435 vs 11,108 ms) no longer raised. Text and table now consistent.
2. **35 kbps FEC parity resolved** — GPT CU Minor #4 (293 vs 308 bits) no longer raised. Table decomposition used consistently.
3. **Stress → continuous-duty acknowledged** — GPT: "the stress-case η_S ≈ 46% is now explicitly framed as a continuous-duty upper bound." No longer a separate major.
4. **Worked sizing example partially acknowledged** — GPT no longer specifically asks for a worked example (was CU #1 in part). Still wants feasibility flow simplification.
5. **Algorithm 1 T_slot equivalence acknowledged** — GPT: "Algorithm 1 already computes T_ing explicitly." The footnote resolved the inconsistency concern.
6. **p_cmd in notation table** — Claude no longer raises this as a minor.
7. **d gates commands clarification** — GPT: "d gates command generation at the coordinator" is acknowledged. Still wants more operational grounding.
8. **Broadcast vs unicast safety** — Gemini acknowledges conjunction timeline context; no longer requests explicit contrast (CU constructive #3 addressed).

## GPT Improvement Detail (7M→6M, 10m→7m)

Resolved/merged majors:
- CU Major #4 (stress relabeling) → resolved (continuous-duty bound throughout)
- CU Minors #3, #4 (numerical inconsistencies) → resolved (numbers reconciled)
- CU Minor #8 (baseline 20.5% derivation) → resolved (inline derivation added)

## Major Issues Remaining

### Priority 1: Feasibility Framework Confusion (GPT #1 — PERSISTENT/EVOLVED)
**GPT Major #1.** Still about two-test vs three-check ambiguity. CV improvement: worked sizing example helps, but GPT now wants a "feasibility flow diagram" (single figure) showing bytes → slot time → airtime → decision. Algorithm 1's Eq. 19 "heuristic" still confuses.

### Priority 2: γ Consistency Audit (GPT #2 — PERSISTENT)
**GPT Major #2.** Wants explicit audit showing every place γ is used confirms Model C values. "Add a short 'Consistency audit' subsection or appendix table."

### Priority 3: d Realism Strengthening (GPT #3 — PERSISTENT/EVOLVED)
**GPT Major #3.** Wants one fully worked operational scenario: orbit-raising for X days → Y commands → implied d and p_cmd. Table VII is heuristic; needs concrete mapping. Also wants d vs η sensitivity for multiple S_cmd and p_cmd.

### Priority 4: DES Value (GPT #4, Claude #1 — STRUCTURAL CEILING)
**GPT Major #4, Claude Major #1.** Both want DES condensed. Claude: "Reduce DES description to ~1 column." GPT: "Either robustify with additional burst models or reposition as implementation sanity check."

### Priority 5: §IV-J Not Validation (GPT #5, Claude #2 — STRUCTURAL CEILING)
**GPT Major #5, Claude Major #2.** Both want section renamed "Standards-Based Parameter Estimation" and stronger γ sensitivity (Claude wants γ ∈ [0.50, 0.85] figure). GPT wants "if-then" practitioner guidance.

### Priority 6: Fleet-Level Claims (Claude #3, Gemini #2 — PERSISTENT)
**Claude Major #3.** Wants title change to "Per-Cluster Sizing Equations." Gemini: wants R ∈ {3, 5, 7} sensitivity calculation.

### Priority 7: 1 kbps Justification (Claude #4, Gemini #1 — PERSISTENT)
**Claude Major #4.** Wants proper link budget table with margin analysis. Show feasibility for C_node ∈ {0.5, 1, 2, 5, 10} kbps. Gemini: "Clarify 1 kbps is a baseline design target, not a hard physical limit."

### Priority 8: γ Practitioner Guidance (GPT #6, Claude #5 — PERSISTENT)
**GPT Major #6, Claude Major #5.** Eq. 7 needs "How to instantiate" checklist and uncertainty quantification. Claude wants Monte Carlo over (T_acq, T_guard) distributions.

### Priority 9: Thundering Herd (Gemini #3 — PERSISTENT)
**Gemini Major #3.** BEB convergence at ~160s on UHF still questioned. "Did the simulation explicitly model collision/backoff dynamics?"

## Minor Issues (23 total)

### Gemini (4 minor)
1. Table I γ equation reference (Eq. 2 vs Eq. 10)
2. Fig. 2 ON/OFF model clarification (Markovian vs Bernoulli)
3. §IV-J γ decreases with rate — add intuitive explanation
4. Algorithm 1 line 4: reference Eq. 10 directly

### GPT (7 minor)
1. η notation inconsistency (η₀ + dη_cmd vs η₀ + η_cmd in prose)
2. α_RX varies with M_r; note "nominal M_r = 0"
3. AoI: separate "network latency" vs "information staleness"
4. ACK-in-guard timing diagram
5. Fleet reuse R=3: no downstream reliance on it as validated
6. Centralized baseline: clearly labeled "compute-only bound"
7. kbps (info) vs kbps (PHY) labeling in tables

### Claude (12 minor)
1. Eq. 1 M_total: per-cycle vs per-second
2. Table II Panel B: Rec. PHY scaling convention
3. Thundering herd: move from footnote to main text
4. Eq. 5 Raft serialization assumption
5. Table VI d=1.00 checkmark ambiguity
6. Fig. 2 grayscale readability
7. Phase-stagger claim without data
8. Table VIII margin 192 ms source
9. Abstract γ range endpoints (0.695–0.761 vs stated 0.70–0.76)
10. Sizing walkthrough α_RX = 0.792 vs 0.908 discrepancy
11. Non-archival references
12. Eq. eta_canonical referenced before definition

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
| **CV** | **Accept w/ Minor (3M/4m)** | **Major (6M/7m)** | **Major (5M/12m)** |

**Assessment:** CV shows measurable GPT improvement:

- **GPT improved** from 7M/10m to 6M/7m. The numerical fixes (24 kbps, FEC parity), worked sizing example, stress→continuous-duty rename, and Algorithm 1 equivalence footnote collectively resolved 1 major and 3 minors. This is the first GPT improvement in majors since CP (6M). The persistent concerns are structural (feasibility flow, γ audit, d operational grounding, DES robustness, §IV-J, γ practitioner guidance).

- **Gemini stable** at Accept w/ Minor (3M/4m). Significance dropped 5→4 (may be stochastic; CU's 5/5 was the first ever). Same 3 persistent majors (1 kbps, R=3, thundering herd). Minor count improved 5→4.

- **Claude stable** at 5M/12m. Persistent structural ceiling: DES, §IV-J, fleet, 1 kbps, γ uncertainty. These require new simulation data or hardware measurements.

## Recommended Strategy for CW

### Achievable via Text Edits

1. **Rename §IV-J** (GPT #5, Claude #2) — Change section title to "Standards-Based Slot Efficiency Parameterization". Remove any residual "validation" language. Add "if measured γ < 0.65, increase R_PHY to 40 kbps" practitioner guidance.

2. **Add γ-conditional lookup as standalone table** (Claude #2) — Elevate the inline γ → R_PHY mapping to a small formal table with columns: γ range, R_PHY,min, Margin %, Application note.

3. **Add "How to instantiate Eq. 7" checklist** (GPT #6, Claude #5) — After Eq. gamma_time, add 3-line checklist: (a) T_acq from modem reacquisition spec, (b) T_guard = propagation + turnaround + timing margin, (c) O_frame from framing standard (ASM+header+FCS).

4. **Compress DES to ~1 column** (Claude #1, GPT #4) — Move mean-value comparison to a single sentence. Focus entirely on buffer sizing rule with explicit conditional caveat.

5. **η notation fix** (GPT Minor #1) — Audit all prose for η = η₀ + η_cmd (without d) and change to η = η₀ + d·η_cmd throughout.

6. **α_RX sizing walkthrough discrepancy** (Claude Minor #10) — Add note: "α_RX = T_ing/T_c = 7920/10000 = 0.792 at 35 kbps (vs 0.908 at 30 kbps; α_RX is rate-dependent)."

7. **Abstract γ range** (Claude Minor #9) — Change "0.70–0.76" to "0.70–0.76 (24–50 kbps)" or use exact values "γ₂₄ = 0.761, γ₃₅ = 0.732."

8. **Table VIII margin source** (Claude Minor #8) — Add "192 ms = egress (Table V)" to footnote.

9. **1 kbps framing** (Gemini #1, Claude #4) — Strengthen existing text: "1 kbps is a baseline design target for low-power omnidirectional coordination, not a hard physical limit. Results scale linearly with C_node (Table II-A)."

10. **Feasibility flow simplification** (GPT #1, partial) — Add 2-sentence clarification after the two-test box: "The heuristic (Eq. 19) is a rearrangement of Test B under simplified scheduling; it is not a separate test. When using Algorithm 1, only Tests A and B are evaluated."

### NOT Achievable Without New Work

- NS-3 MAC simulation for independent γ validation
- Monte Carlo over (T_acq, T_guard) distributions for γ uncertainty
- C_node parametric feasibility figure (heatmap over C_node × k_c)
- Alternative burstiness models for buffer sizing
- R ∈ {3, 5, 7} quantitative sensitivity with antenna patterns
- Title change ("Per-Cluster Sizing Equations...")
- Network calculus worst-case bounds
- Hardware γ measurement

### Expected Outcome
With text edits: GPT might drop 6→5M (§IV-J rename + feasibility clarification + γ checklist). Claude stable at 4-5M (structural ceiling). Gemini maintained at Accept. Residual 4-5 majors (DES robustness, fleet scope, 1 kbps parametric, γ uncertainty) require new data.
