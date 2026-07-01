# Version CT Review Summary

## Recommendations

| Reviewer | Recommendation | Change from CS |
|----------|---------------|----------------|
| Gemini 3 Pro | **Accept with Minor Revisions** | Stable (3M/5m vs 3M/4m; Validity 5/5, Clarity 5/5 — both improved) |
| GPT-5.2 | **Major Revision** | **Worsened** (7M/7m vs 6M/7m — new γ recipe major) |
| Claude Opus 4.6 | **Major Revision** | Stable (5M/14m vs 5M/12m — minors up, Validity improved 3→4) |

## What CT Fixed (Acknowledged by Reviewers)

1. **1 kbps circularity resolved** — Claude: no longer calls it "circular"; now says "derives from a link budget (200 kbps / 100 nodes × γ ≈ 1.5 kbps, with 50% margin → 1 kbps)." Reframed concern as "lacks independent justification" (wants parametric C_node table, not circularity fix). GPT: not raised.
2. **ARQ in Algorithm 1** — GPT: acknowledges Layer 2b but wants it presented as part of "two tests + optional ARQ add-on." Claude: not raised as separate concern.
3. **Raft stability condition resolved** — Gemini: f_decision saturation concern from CS not raised in CT (resolved by f_decision,max ≈ 24 calculation).
4. **GE predetermination acknowledged** — Claude: explicitly quotes "direct consequence of the per-cycle GE coherence assumption, not an emergent finding." Concern reframed as "still presents it as a result" → wants "what-if design tool" framing.
5. **Fleet → limitations noted** — All three acknowledge caveats. Claude: "correctly identifies NS-3 validation as needed but still makes fleet-level claims in abstract/conclusion." GPT: "consider removing fleet-level claims from abstract entirely."
6. **γ rate dependence** — GPT: "γ unification (0.76 CCSDS-anchored, rate-dependent) is mostly improved." Claude: "consistently applied throughout."
7. **Abstract γ range fixed** — Claude minor #7: "unusual level of detail in abstract" (cosmetic concern, not range error).
8. **Collision rate reconciled** — Claude minor #2: acknowledges "conservative upper bound" description; suggests "stress-test parameter" wording instead.
9. **35 kbps in rate table** — Implicitly acknowledged (Gemini Validity 5/5, Claude Validity improved to 4/5).

## Major Issues Remaining

### Priority 1: Three-Layer Confusion (GPT #1 — PERSISTENT)
**GPT Major #1.** Despite the "do not double-count" box, GPT still sees risk of misapplication. Wants exactly two tests: Test A (η_total ≤ 1) and Test B (T_ing + T_egr + T_ARQ ≤ T_c), with C_raw → R_PHY presented as a "design heuristic / lower bound" derived from Test B. Wants a "common mistakes" box.

### Priority 2: γ Consistency Enforcement (GPT #2 — PERSISTENT)
**GPT Major #2.** Table V (joint interaction) still uses Model S timing; wants it moved to appendix or "visually quarantined." Wants numeric examples to annotate exact γ(R_PHY) used. Eq. (TDMA capacity) uses γ_{C,24} but discusses 30 kbps feasibility.

### Priority 3: Campaign d Workload Model (GPT #3 — PERSISTENT)
**GPT Major #3.** Wants fully specified workload model (ON/OFF Markov-modulated) tied to concrete scenario. Distinguish d (campaign gating) from p_cmd clearly. Wants sensitivity plot: η vs (d, p_cmd, S_cmd).

### Priority 4: Stress-Case QoS (GPT #4 — PERSISTENT)
**GPT Major #4.** Wants table of worst-case command completion time and AoI during stress bursts under slow-mixing GE with inter-cycle recovery. Quantify control authority during stress.

### Priority 5: DES Value (Claude #1, GPT #5 — STRUCTURAL CEILING)
**Claude Major #1, GPT Major #5.** Persistent. Both want DES condensed to distributional analysis only. GPT: wants buffer rule validated against alternative stochastic process or downgraded to "illustrative example."

### Priority 6: §IV-J Not Validation (Claude #2, GPT #6 — STRUCTURAL CEILING)
**Claude Major #2, GPT Major #6.** Persistent. Both want: recommendation language softened ("implies" not "confirms"), measurement checklist for practitioners.

### Priority 7: Fleet-Level Claims (Claude #3 — PERSISTENT)
**Claude Major #3.** Wants abstract/conclusion restricted to per-cluster sizing. Fleet as "preliminary extension" only.

### Priority 8: C_node Parametric Sensitivity (Claude #4 — REFRAMED from circularity)
**Claude Major #4.** The 1 kbps circularity is resolved, but Claude now wants C_node ∈ {0.5, 1, 2, 5} kbps sensitivity table as a "primary result" (not a footnote). The link budget assumptions (6 dBi, 1 W, S-band, 500 km) are noted as unvalidated.

### Priority 9: GE Parameters Unanchored (Claude #5 — PERSISTENT)
**Claude Major #5.** Present GE as "what-if" design tool, not predictive model. Add references to available ISL propagation data (EDRS, Starlink v2 optical). Discuss Lutz et al. applicability to ISL.

### Priority 10: γ Recipe (GPT #7 — NEW)
**GPT Major #7.** Wants compact "γ recipe" subsection: which bits are FEC-encoded, where acquisition happens, optional terms (ACK, ranging), worked example for 30/35 kbps showing all intermediate times.

### Priority 11: Spatial Reuse R=3 (Gemini #1 — PERSISTENT)
**Gemini Major #1.** Wants geometric C/I calculation or explicit impact if R=7 required.

### Priority 12: Unicast Latency (Gemini #2 — PERSISTENT)
**Gemini Major #2.** Wants abstract/intro to state explicitly that architecture supports *loose* coordination, not tight formation flying.

### Priority 13: Oscillator Drift in Guard (Gemini #3 — NEW)
**Gemini Major #3.** Wants explicit calculation linking guard time to oscillator stability (ppm) and sync interval.

## Minor Issues (26 total)

### Gemini (5 minor)
1. Table I η/η_total distinction in captions
2. Fig. 4 "Bernoulli d=0.10" label ambiguity
3. §IV-J DVB-RCS2 throughput vs slot efficiency clarification
4. Algorithm 1 Line 12: add "Fallback to Inter-cycle ARQ"
5. Eq. 5 fleet reuse consistency

### GPT (7 minor)
1. Table V: move to appendix or rename "Illustrative"
2. Eq. TDMA capacity: tighten γ_{C,24} vs 30 kbps alignment
3. ACK-in-guard timing diagram
4. α_RX definition consistency
5. Fleet numbers explicitly labeled "illustrative"
6. η/utilization/overhead terminology
7. Burst-mode acquisition time reference

### Claude (14 minor)
1. α_RX described as derived but appears as input
2. Collision rate: "stress-test parameter" not "conservative"
3. Raft serialization under TDMA scheduling
4. Slotted ALOHA context (only during coordinator failure?)
5. ACK mini-slot robustness if jitter consumed
6. Algorithm 1 η₀ = 5% hardcoded
7. Abstract γ detail unusual
8. SWIM reference connection to spacecraft
9. Eq. 14 framing FEC encoding verification
10. Repository tag versioning
11. Fig. 2 markers grayscale distinguishability
12. 512 B summary: 371 B metadata disproportionate
13. Eq. 3 messages vs bytes accounting
14. γ-conditional PHY interval notation ambiguity

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
| **CT** | **Accept w/ Minor (3M/5m)** | **Major (7M/7m)** | **Major (5M/14m)** |

**Assessment:** CT shows mixed results:

- **Gemini improved** in substance (Validity 5/5, Clarity 5/5) despite stable major count. The Raft stability concern is resolved. New oscillator drift concern is actionable via text (brief calculation). Spatial reuse and unicast latency persist but are well-characterized.

- **GPT regressed slightly** (6M→7M) with a new γ recipe concern. The three-layer confusion is the most persistent GPT issue across 11 versions. The ARQ integration into Algorithm 1 was acknowledged but folded into the broader "two tests + optional ARQ" reframing request rather than credited as a resolved major. GPT appears to have a structural floor of ~6-7 majors driven by wanting more operational grounding (d workload, stress QoS) and tighter presentation (feasibility framework, γ consistency) than text edits can fully achieve.

- **Claude stable** at 5M. The 1 kbps circularity was resolved (reframed as "lacks independent justification" for the link budget parameters, not circularity). Validity improved from 3→4. The persistent majors (DES, §IV-J, fleet, GE) are structural ceiling issues requiring new data.

**The 1 kbps circularity fix worked.** Claude no longer calls the justification circular — it now accepts the spectrum/power framing but wants parametric C_node sensitivity (a different, more tractable concern).

**GPT's three-layer concern** is the most important actionable item. Despite the "do not double-count" box, GPT wants the framework explicitly presented as "two tests + derivation heuristic" rather than allowing any narrative where C_raw/γ could be misread as a third test. This is achievable via rewording.

## Recommended Strategy for CU

### Achievable via Text Edits

1. **Two-test framework rewrite** (GPT #1) — Rename the framework as "Test A (bytes) + Test B (airtime)" throughout. Present R_PHY,min = C_info/(γ·α_RX) as a "design heuristic derived from Test B under simplified scheduling." Add a 2-line "common mistakes" note: "Do not apply the heuristic AND separately compute slot-level ingress; they are algebraically connected."

2. **Table V quarantine** (GPT #2) — Add gray-background visual marker. Remove 15/20 kbps rows (non-actionable). Rename caption: "Illustrative ARQ×TDMA Coupling Under Optimistic Timing (Model S Only)."

3. **Recommendation language softening** (GPT #6, Claude #2) — "implies" not "confirms" in abstract/conclusion. Add measurement checklist: T_acq distribution, turnaround time, guard adequacy under Doppler, achieved γ.

4. **Oscillator drift calculation** (Gemini #3) — Δt = drift_ppm × T_sync. TCXO ±1 ppm × 600 s = 0.6 ms; guard 4.7 ms covers with 4.1 ms margin.

5. **Abstract loose-coordination qualifier** (Gemini #2) — Add "supporting loose coordination (task assignment, orbit maintenance) via RF; tight formation control requires optical ISL."

6. **C_node parametric note** (Claude #4) — Already have Table II-A showing linear scaling. Add: "All results scale linearly with C_node; at 0.5 kbps, η_stress ≈ 92% (infeasible); at 2 kbps, η_stress ≈ 23%; at 5 kbps, all workloads are single-cycle feasible."

7. **GE → "what-if design tool"** (Claude #5) — Reframe GE section header and introductory sentence.

8. **Buffer rule → conditional** (GPT #5) — Relabel: "Buffer sizing rule (conditional on assumed ON/OFF Markov process; untested under alternative burstiness models)."

9. **Fleet claims → abstract restriction** (Claude #3) — Remove "fleet-level" from abstract; keep in limitations section only.

10. **γ worked example at 35 kbps** (GPT #7, partial) — Add intermediate times for 35 kbps alongside existing 30 kbps decomposition.

11. **R=7 fallback note** (Gemini #1) — "If R = 7 is required, F must increase to 8 or G doubles; both are solvable via additional spectrum allocation."

12. **Minor batch** — Collision rate wording, Algorithm 1 fallback text, α_RX consistency, η baseline reminder near plots.

### NOT Achievable Without New Work

- NS-3 single-cluster validation
- Modem γ measurement
- ISL channel measurement data (EDRS, Starlink v2)
- Alternative burstiness model validation for buffer rule
- Full d/p_cmd/S_cmd sensitivity plot
- Stress-case QoS table (worst-case AoI/command time under GE)

### Expected Outcome
With text edits: GPT might drop 7→5-6 majors (two-test rewrite + Table V quarantine + recommendation softening resolves 1-2; γ recipe partial). Claude might drop 5→3-4 (fleet restriction + C_node + GE reframing resolves 1-2). Gemini maintained at Accept (oscillator drift + unicast context resolves 2). Residual 4-5 majors (DES value, §IV-J, d workload model, stress QoS) require new simulation data.
