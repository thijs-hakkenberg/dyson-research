# Version CS Review Summary

## Recommendations

| Reviewer | Recommendation | Change from CR |
|----------|---------------|----------------|
| Gemini 3 Pro | **Accept with Minor Revisions** | Stable (3M/4m vs 2M/4m; methodology 5/5, validity 5/5) |
| GPT-5.2 | **Major Revision** | **Improved** (6M/7m vs 8M/10m — significant drop) |
| Claude Opus 4.6 | **Major Revision** | Worsened (5M/12m vs 4M/12m — new 1 kbps circularity concern) |

## What CS Fixed (Acknowledged by Reviewers)

1. **§IV-J title rename** — Claude: "Slot Efficiency Parameter Estimation" correctly labels the section (partially done but "inconsistently"). GPT: "CCSDS-based γ derivation is a step forward."
2. **Model S watermark** — GPT minor #3: "MODEL S TIMING disclaimer is good." GPT still wants appendix move.
3. **DES narrative compression** — GPT: "admittedly honest that DES reproduces its own equations." Buffer multiplier rule acknowledged.
4. **T_acq taxonomy** — GPT: "three acquisition modes" covered (implicit acceptance, no longer raised as separate major).
5. **Fleet-level scope reduction** — Claude: acknowledges abstract says "per-cluster." GPT: acknowledges "per-cluster sizing equations." Both still want more.
6. **Unicast stagger context** — Gemini: still Major #2 but acknowledges optical ISL for tight control. GPT: not raised.
7. **Stress degradation** — GPT #4 from CR not raised as separate major (folded into d mapping).
8. **DVB-RCS2 proxy** — Claude minor: "analogy acknowledged as weak." Gemini: minor #2 (not raised in majors).
9. **GE by-construction note** — Claude #5: "The paper states this" but reframes as "predetermination." GPT minor #5: "you do acknowledge this."

## Major Issues Remaining

### Priority 1: 1 kbps Budget Justification (Claude #3 — NEW)
**Claude Major #3.** The paper argues 1 kbps ensures "coordination invariance across failure modes," but during RF-backup hierarchy is *suspended* (Table III). If the architecture doesn't operate during the failure mode it's designed for, the 1 kbps constraint isn't justified by failure-mode invariance. At 2 kbps, stress-case η drops to ~23% and TDMA analysis becomes non-binding.
*This is the sharpest new observation across all three reviewers.*

### Priority 2: ARQ Integration into Feasibility Test (GPT #1)
**GPT Major #1.** Algorithm 1 / Layer 2 doesn't explicitly incorporate retransmission slot reservation. The 35 kbps recommendation feels "partly ad hoc." Wants explicit ARQ reservation term with target delivery probability.

### Priority 3: Model S Coupling Demo (GPT #2, Claude minor #2)
**GPT Major #2.** Table V (joint interaction) is the only "emergent" finding but uses Model S where 24 kbps is feasible absent ARQ — under Model C, 24 kbps is infeasible regardless. Wants Model C coupling results at 30/35 kbps. Claude: wants appendix move.

### Priority 4: DES Verification Value (Claude #1, GPT #5)
**Claude Major #1, GPT Major #5 (previously #9 rating 3/5).** Persistent. Both want: more distributional scenarios (varying k_c, correlated failures), or reduce further and acknowledge as design tool.

### Priority 5: §IV-J Not Validation (Claude #2, GPT #10 rating 2/5)
**Claude Major #2.** Persistent. Wants γ sensitivity table for γ ∈ [0.60, 0.85] in 0.05 increments. GPT Section 10 rated 2/5: wants SDR measurement or much stronger uncertainty quantification.

### Priority 6: Fleet-Level Scaling (Claude #4, GPT #6)
**Claude Major #4, GPT Major #6.** Persistent despite scope reduction. Both want either (a) remove from title/abstract or (b) provide multi-cluster simulation. GPT: "demote to appendix."

### Priority 7: GE Coherence Predetermination (Claude #5 — REFRAMED)
**Claude Major #5.** "The 27% ARQ recovery is a direct consequence of the modeling assumption, not an emergent result." Wants sub-cycle GE transitions parameterized per slot to show ARQ effectiveness vs coherence time.

### Priority 8: γ Constant Usage Audit (GPT #3)
**GPT Major #3.** Scattered places where γ is used without rate subscript. Wants systematic audit and γ usage checklist.

### Priority 9: Campaign d Operational Mapping (GPT #4)
**GPT Major #4.** Wants command class taxonomy: broadcast schedule update, maneuver plan, software patch, collision alert with typical sizes, fanout, cadence → implied d.

### Priority 10: Raft Consensus Stability (Gemini #3 — NEW)
**Gemini Major #3.** At f_decision > 1, η_consensus can saturate. Wants stability condition: solve Eq. 6 for f_decision where η_total = 1.

### Priority 11: Spatial Reuse R=3 (Gemini #1)
**Gemini Major #1.** Persistent but weakened. Wants INR threshold discussion and mention R=7 as conservative fallback.

### Priority 12: Unicast Stagger (Gemini #2)
**Gemini Major #2.** Wants "priority override" mechanism or explicit statement that time-critical unicast requires optical ISL.

## Minor Issues (23 total)

### Gemini (4 minor)
1. Abstract density (too many numbers)
2. Table II footnotes too long
3. Fig. 2 readability
4. Info rate clarification in Table III

### GPT (7 minor)
1. Three-layer terminology still appears
2. α_RX forward-reference issue
3. Table IV-D appendix consideration
4. AoI decomposition (sampling vs network)
5. GE fast-mixing as selectable regime
6. Command size justification
7. Margin consistency (-1,300 vs -1,635)

### Claude (12 minor)
1. γ subscript inconsistency
2. Table V Model S → appendix
3. Thundering herd footnote → main text
4. Raft f_decision interaction with TDMA
5. Abstract γ range doesn't include 0.761
6. Table II Panel B: Rec PHY includes half-duplex?
7. 512B summary: 371B metadata excessive
8. Collision avoidance rate discrepancy (10⁻⁴ vs 3.2×10⁻⁷)
9. Self-citation [53] caveat
10. Algorithm 1 complexity: O(1)
11. Fig. 3 N=10,000 vs N=10⁵
12. Eq. 14 framing FEC design choice

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
| **CS** | **Accept w/ Minor (3M/4m)** | **Major (6M/7m)** | **Major (5M/12m)** |

**Assessment:** CS shows divergent trends:

- **GPT improved significantly** (8M→6M, 10m→7m). The DES compression, Model S watermark, T_acq taxonomy, fleet scope reduction, and stress degradation description resolved 2 majors and 3 minors. GPT's new concerns (ARQ in feasibility test, γ constant audit) are actionable via text. This is the best GPT result since CP (6M/10m).

- **Gemini stable** at Accept w/ Minor with improved methodology (5/5) and validity (5/5). New Raft stability concern is minor-level. Spatial reuse and unicast stagger persist but are well-characterized boundary issues.

- **Claude worsened** (4M→5M) with a sharp new observation: the 1 kbps circularity. This is a genuine logical gap — the paper claims 1 kbps for failure-mode invariance, but hierarchy is suspended during RF-backup. The GE predetermination reframing is also sharper. However, 3 of Claude's 5 majors (DES, §IV-J, fleet scaling) are structural ceiling issues requiring new data.

**The 1 kbps circularity** (Claude #3) is the most important new finding. It can be addressed via text: the 1 kbps budget is motivated by *S-band ISL capacity constraints* (the link budget gives max ~200 kbps shared among 100 nodes = 2 kbps/node; 1 kbps provides 50% margin and allows 50% for optical relay overhead), not by RF-backup invariance.

## Recommended Strategy for CT

### Achievable via Text Edits

1. **1 kbps justification fix** (Claude #3) — Replace "coordination invariance across failure modes" with physics-based justification: S-band link budget (15.9 dB E_b/N_0 at 24 kbps, max ~200 kbps) shared among k_c=100 nodes gives 2 kbps/node. The 1 kbps budget provides 50% margin for overhead, retransmissions, and control traffic. Add: "The 1 kbps budget is a spectrum/power constraint, not an RF-backup requirement."

2. **ARQ reservation in Algorithm 1** (GPT #1) — Add line after Layer 2: "Layer 2b (ARQ): if $M_r > 0$: $T_{\text{ing}}(1 + M_r) + T_{\text{egr}} \leq T_c$; else inter-cycle recovery (AoI += T_c per loss)."

3. **γ subscript audit** (GPT #3) — Search for unsubscripted γ and add rate labels.

4. **Raft stability condition** (Gemini #3) — Add: "Maximum stable f_decision: $f_{\max} = (1 - \eta_0 - \eta_{\text{baseline}}) / (\text{per-decision cost}) \approx 24$ at k_c = 100."

5. **Fleet reuse → limitations** (Claude #4, GPT #6) — Move fleet reuse paragraph from §IV-A.1 to §V-C (Limitations). Remove "10⁵ nodes" from title/abstract scope.

6. **GE predetermination acknowledgment** (Claude #5) — Add: "The 27% recovery under slow-mixing GE is a consequence of the per-cycle coherence assumption; under fast-fading (per-slot transitions), ARQ achieves 98.9%."

7. **Minor batch** — Abstract γ range, margin consistency, collision rate discrepancy, α_RX forward-reference.

### NOT Achievable Without New Work

- NS-3 single-cluster validation
- Model C coupling experiment at 30/35 kbps
- Sub-cycle GE transition analysis
- SDR/hardware γ measurement
- Full C_node parametric sweep

### Expected Outcome
With text edits: GPT might drop 6→4-5 majors (ARQ reservation + γ audit + fleet demotion resolves 2-3); Claude might drop 5→3-4 (1 kbps fix + GE acknowledgment resolves 1-2); Gemini maintained at Accept (Raft stability resolves 1). The 4-5 residual majors (DES value, §IV-J, fleet validation, Model S coupling) require new simulation data.
