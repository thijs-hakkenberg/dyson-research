# Version CU Review Summary

## Recommendations

| Reviewer | Recommendation | Change from CT |
|----------|---------------|----------------|
| Gemini 3 Pro | **Accept with Minor Revisions** | Improved (Significance 4→5; oscillator drift resolved) |
| GPT-5.2 | **Major Revision** | Stable majors (7M); minors up 7→10 (new numerical inconsistencies) |
| Claude Opus 4.6 | **Major Revision** | Stable majors (5M); minors improved 14→12; GE "what-if" acknowledged |

## What CU Fixed (Acknowledged by Reviewers)

1. **Oscillator drift resolved** — Gemini did not raise the guard time/oscillator concern from CT. The explicit TCXO ±1 ppm × 600 s = 0.6 ms calculation (4.1 ms margin) resolved it.
2. **GE "what-if design tool" acknowledged** — Claude explicitly praises: "The GE model is clearly labeled as a 'what-if design tool' rather than a calibrated channel model." This was a persistent Major #5 in CT.
3. **Loose-coordination qualifier acknowledged** — Gemini's unicast concern is now reframed from "needs qualifier" to "needs explicit broadcast vs unicast safety distinction" — the abstract qualifier worked.
4. **Two-test framework partially acknowledged** — GPT: "the paper partially addresses this ('common mistake' box)" and "materially improves reader comprehension." Still wants worked sizing example.
5. **Buffer rule conditional acknowledged** — The "conditional on assumed ON/OFF Markov process" label was noted.
6. **Recommendation language softening** — GPT: "you correctly disclaim" the validation status.
7. **Gemini Significance 5/5** — First 5/5 on Significance from any reviewer across all versions (CJ–CU).
8. **R=7 fallback noted** — Gemini constructive #1: "add a note or equation modifier for the Fleet Reuse factor" — we added this in CU Limitations, but Gemini wants it more prominent.

## Major Issues Remaining

### Priority 1: Worked Sizing Example (GPT #1 — NEW/EVOLVED)
**GPT Major #1.** The three-layer confusion evolved: GPT now specifically wants a "worked end-to-end sizing example" (one page, step-by-step) showing Test A and Test B without double-counting, plus a decision tree. The boxed framework helped but narrative still "oscillates between two-layer and rate ladder."

### Priority 2: Numerical Inconsistencies (GPT Minor #3, #4 — NEW)
**GPT Minor #3.** 24 kbps: text says ingress = 11,435 ms, margin = −1,635 ms; Table rate_feasibility says ingress = 11,108 ms, margin = −1,300 ms. These differ because the text uses a slightly different calculation path (including egress differently). Must reconcile.
**GPT Minor #4.** 35 kbps worked example: T_FEC = 293/35000 but Table gamma_decomposition shows 308 FEC parity bits (at 24 kbps). The 293 is payload-only parity; 308 is payload+framing parity. Different valid decompositions of the same total, but inconsistent presentation.

### Priority 3: γ Unification Tightening (GPT #2 — PERSISTENT)
**GPT Major #2.** Algorithm 1 line 5 uses `(S×8 + O_frame)/(R_FEC · R_PHY)` while Eq. gamma_time treats payload and FEC separately. These are algebraically equivalent but risks practitioner confusion. Wants explicit equivalence proof or verbatim alignment.

### Priority 4: Campaign d Mapping (GPT #3 — PERSISTENT)
**GPT Major #3.** Wants explicit time-weighted utilization formula for mission archetypes (deployment month vs steady-state year). Clarify whether d gates only commands.

### Priority 5: Stress-Case Labeling (GPT #4 — PERSISTENT/REFRAMED)
**GPT Major #4.** Wants "stress" renamed to "continuous-duty bound" throughout. The 46% should always be paired with episodic duty factor.

### Priority 6: DES Value (Claude #1, GPT #5 — STRUCTURAL CEILING)
**Claude Major #1, GPT Major #5.** Persistent across all versions. Both want DES condensed further. Claude: "Consolidate DES discussion. State the code-correctness confirmation in one sentence."

### Priority 7: §IV-J Not Validation (Claude #2, GPT #6 — STRUCTURAL CEILING)
**Claude Major #2, GPT Major #6.** Persistent. Claude: "should more prominently quantify the sensitivity of the design recommendation to γ uncertainty." GPT: "elevate uncertainty analysis."

### Priority 8: Fleet-Level Claims (Claude #3 — PERSISTENT)
**Claude Major #3.** Now asks for title change: "Per-Cluster Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms." Or develop fleet analysis more rigorously.

### Priority 9: Static Membership (Claude #4 — PERSISTENT/EVOLVED)
**Claude Major #4.** Was C_node parametric in CT. Now reframed as static membership concern for cross-plane Walker constellations. Wants re-association transient analysis.

### Priority 10: 1 kbps Justification (Claude #5 — PERSISTENT/REFRAMED)
**Claude Major #5.** The "circular" label returned but as a different concern: the 1 kbps is a design choice using specific antenna/power assumptions, not a derived constraint. Wants C_node on x-axis, feasible k_c on y-axis figure.

### Priority 11: Spatial Reuse R=3 (Gemini #1 — PERSISTENT)
**Gemini Major #1.** Wants sensitivity calculation for R=3 vs R=7. CU added R=7 fallback text in Limitations but Gemini wants it more prominent (constructive #1).

### Priority 12: Thundering Herd BEB (Gemini #2 — PERSISTENT/EVOLVED)
**Gemini Major #2.** Now about BEB convergence conservatism: "Does the 160s RF-backup transition account for a 'bad case' election where W_max = 64 might be too small for 100 contenders?" Wants W_max justification.

### Priority 13: Unicast Safety (Gemini #3 — PERSISTENT/EVOLVED)
**Gemini Major #3.** Wants explicit table row contrasting "Broadcast Collision Avoidance" (1 cycle) vs "Unicast Collision Avoidance" (19 cycles) to prevent reader confusion.

## Minor Issues (27 total)

### Gemini (5 minor)
1. α_RX as function of k_c and S_eph in Table I
2. DVB-RCS2 return link vs forward link clarification
3. Fig. 4 "Bernoulli d=0.10" — memoryless vs bursty
4. Raft f_decision,max = 24 "stable leader" note
5. Typos: triple fault exponent, re-sync preamble per-slot vs per-superframe

### GPT (10 minor)
1. Algorithm 1 η₀ = 5% depends on k_c
2. ACK-in-guard timing diagram
3. **24 kbps numbers inconsistency (11,435 vs 11,108 ms)**
4. **35 kbps FEC parity bits (293 vs 308)**
5. Coordinator/TDMA/RX terminology standardization
6. Fleet reuse prominence reduction
7. Non-archival references
8. Baseline 20.5% derivation inline
9. AoI under correlated processes
10. kbps/kbit/s/bps consistency

### Claude (12 minor)
1. Abstract too many numbers
2. α_RX depends on PHY rate
3. p_cmd not in notation table
4. 512 B summary: 371 B metadata disproportionate
5. Thundering herd belongs in main text
6. ACK mini-slot timing diagram
7. Fig. 1 description
8. kbps vs bps info/PHY consistency
9. Phase-stagger claim without data
10. Raft serialization assumption
11. Self-citation [55] flagged as non-peer-reviewed
12. Consolidated assumptions table

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
| **CU** | **Accept w/ Minor (3M/5m)** | **Major (7M/10m)** | **Major (5M/12m)** |

**Assessment:** CU shows incremental improvements but no breakthrough:

- **Gemini improved** substantively (Significance 5/5 — first across all versions). Oscillator drift resolved. Persistent spatial reuse and unicast concerns are well-characterized and actionable.

- **GPT stable** at 7M but minors increased 7→10. The new numerical inconsistencies (24 kbps: 11,435 vs 11,108; 35 kbps FEC: 293 vs 308) are fixable bugs. The structural concerns (worked sizing example, d mapping, stress labeling) are persistent and require new content.

- **Claude stable** at 5M/12m, improving from 14m. GE "what-if" and recommendation language acknowledged. The persistent majors (DES, §IV-J, fleet, 1 kbps, static membership) are structural ceiling issues.

**The two-test framework helped** — GPT acknowledges the "common mistake" box "materially improves reader comprehension" but still wants a full worked example. This is the most tractable remaining GPT concern.

**The numerical inconsistencies are the easiest wins** — fixing the 24 kbps ingress numbers and FEC parity decomposition removes 2 GPT minors immediately.

## Recommended Strategy for CV

### Achievable via Text Edits

1. **Fix 24 kbps numerical inconsistency** (GPT Minor #3) — Reconcile text "11,435 ms / −1,635 ms" with Table "11,108 ms / −1,300 ms." The table is correct (ingress only); text includes egress. Make both use the same basis.

2. **Fix 35 kbps FEC parity decomposition** (GPT Minor #4) — In the worked example, use the table decomposition: "FEC parity = (2048 + 104) × (1/7) = 308 bits → 308/35000 = 8.8 ms; framing = 104/35000 = 3.0 ms; total coded = 70.3 ms."

3. **Add worked sizing example** (GPT #1, partial) — Insert a compact 4-5 line "Sizing walkthrough" after Algorithm 1 showing Test A and Test B for k_c = 100, d = 0.10, 35 kbps, with explicit "do not reapply heuristic" note.

4. **Rename "stress" to "continuous-duty bound"** (GPT #4) — Search-replace "stress" with "continuous-duty" or "full-load" in key locations (workload profiles table, abstract, conclusion).

5. **Add broadcast vs unicast table row** (Gemini #3) — Add "Collision avoidance (broadcast)" and "Software update (unicast)" rows to Table schedulability showing 1-cycle vs 19-cycle latency.

6. **Algorithm 1 T_slot equivalence note** (GPT #2) — Add brief footnote: "Line 5 is algebraically equivalent to Eq. gamma_time; both compute T_slot = (S×8 + O_frame)/(R_FEC × R_PHY) + T_guard + T_acq."

7. **Clarify d gates commands only** (GPT #3, partial) — Add sentence: "d gates command generation at the coordinator; status reporting (baseline 20.5%) is continuous and independent of d."

8. **Elevate γ-conditional lookup** (Claude #2) — Move the [0.65, 0.70] → 40 kbps, [0.70, 0.80] → 35 kbps lookup to a small standalone table (not just inline text) and reference it as a primary result.

9. **Baseline 20.5% inline derivation** (GPT Minor #8) — Add: "256 B × 8 / (1000 × 10) = 0.205."

10. **Minor batch** — α_RX as f(k_c, S, R_PHY) in Table I; p_cmd in notation table; η₀ = 5% conservative note in Algorithm 1.

### NOT Achievable Without New Work

- C_node parametric feasibility figure (Claude wants k_c vs C_node heatmap)
- Alternative burstiness model for buffer rule validation
- NS-3 spatial reuse simulation
- Network calculus worst-case bounds
- Cross-plane re-association transient modeling
- Title change ("Per-Cluster Design Equations...")
- Hardware γ measurement

### Expected Outcome
With text edits: GPT might drop 7→5-6 majors (worked example + numerical fixes + stress relabeling). Claude stable at 4-5M (structural ceiling). Gemini maintained at Accept. Residual 4-5 majors (DES, §IV-J, fleet, 1 kbps parametric) require new simulation data.
