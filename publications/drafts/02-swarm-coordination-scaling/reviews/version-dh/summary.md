# Version DH Review Summary

## Recommendations

| Reviewer | Recommendation | Change from DG |
|----------|---------------|----------------|
| Gemini 3 Pro | **Accept with Minor Revisions** | Improved (3M/4m->2M/4m) |
| GPT-5.2 | **Major Revision** | Stable (6M/8m->6M/7m) |
| Claude Opus 4.6 | **Major Revision** | Mixed (4M/14m->5M/10m, majors regressed, minors improved) |

## What DH Fixed (Acknowledged by Reviewers)

1. **1 kbps / 35 kbps clarification** -- Gemini: Major reduced to abstract wording suggestion only. Claude: "1 kbps budget" DROPPED as major (was DG #2). The scope text ("TDMA analysis most relevant at C_node ≤ 1 kbps") resolved the concern.
2. **GE correlation structure** -- GPT: DG #2 (ARQ/GE correlation) NOT re-raised as major. The per-node independent specification with mixture-of-binomials note was absorbed.
3. **Slot timing contract** -- GPT: DG #6 (implementation contract) NOT re-raised as major. The compact contract text was absorbed.
4. **γ reframe** -- Claude: DG #4 (γ standard TDMA) evolved to narrower DH #3 (γ limited without hardware). The "reference parameterization" framing was accepted.
5. **Static clusters** -- Claude: DG #3 NOT re-raised as major (boundary cluster note absorbed).
6. **Doppler/range γ sensitivity** -- Gemini: DG #2 NOT re-raised. Calculation absorbed.
7. **BEB stability** -- Gemini: DG #3 NOT re-raised. Probability calculation absorbed.
8. **η₀ reconciliation** -- Claude minor: NOT re-raised. 5.6% consistent throughout.
9. **Rate dependence wording** -- GPT: NOT re-raised. Clarified direction absorbed.
10. **Campaign p_cmd sensitivity** -- GPT: Acknowledged but wants MORE (p_cmd alternatives).

## What BACKFIRED

1. **Removing Fig. coordinator_buffer_cdf** -- GPT DH #4 now EXPLICITLY asks: "Add one figure: buffer occupancy CDF." Claude DH #1 also says: "present actual tail distribution plots." REMOVING THE FIGURE MADE THINGS WORSE. Both now want it back.

## Gemini Improvement (3M->2M -- BEST-EVER)

Resolved from DG:
- DG #2 (Doppler γ sensitivity) → RESOLVED
- DG #3 (BEB thundering herd) → RESOLVED

Remaining:
- DH #1: Abstract wording for 1 kbps vs 35 kbps (trivial fix)
- DH #2: Inter-cycle recovery p_BG sensitivity (already addressed, wants slight elevation)

## GPT Evolution (6M stable, minors improved 8→7)

DG→DH resolved:
- DG #2 (ARQ/GE correlation structure) → RESOLVED
- DG #6 (slot timing contract) → RESOLVED

DG→DH evolved:
- DG #1 (validation thin) → DH #5 (packet-level not independent — narrower)
- DG #3 (three-layer) → DH #1 (persistent — wants worked example)
- DG #4 (campaign d) → DH #2 (persistent — wants p_cmd alternatives)
- DG #5 (DES real estate) → DH #4 (BACKFIRED — now wants buffer CDF BACK)

New/elevated:
- DH #3: Model S table misconstrued (was minor, now major — wants Model C coupling table)
- DH #6: γ measurement pipeline (was implicit, now explicit — wants checklist)

## Claude Mixed (4M→5M majors regressed; 14→10 minors improved)

DG→DH resolved:
- DG #2 (1 kbps budget) → RESOLVED (C_node scope text absorbed)
- DG #3 (static clusters) → RESOLVED (boundary cluster note absorbed)

DG→DH evolved:
- DG #1 (DES) → DH #1 (persistent — now "show actual tails or reduce")
- DG #4 (γ standard) → DH #3 (narrower — "limited without hardware, add ∂R/∂γ")

New:
- DH #2: Packet-level is parameter anchoring (persistent — wants Tier 2 relabeling)
- DH #4: Fleet-level claims unsupported by per-cluster analysis (NEW — title vs scope)
- DH #5: Topology comparison asymmetric (NEW — wants intermediate baseline)

## Progress Trajectory

| Version | Gemini | GPT | Claude |
|---------|--------|-----|--------|
| CW | Accept w/ Minor (2M/4m) | Major (7M/8m) | Major (5M/14m) |
| CX | Accept w/ Minor (2M/4m) | Major (7M/7m) | Major (5M/14m) |
| CY | Accept w/ Minor (3M/4m) | Major (7M/10m) | Major (5M/13m) |
| CZ | Accept w/ Minor (3M/5m) | Major (7M/8m) | Major (5M/12m) |
| DA | Accept w/ Minor (2M/5m) | Major (7M/10m) | Major (5M/12m) |
| DB | Accept w/ Minor (2M/4m) | Major (8M/7m) | Major (5M/13m) |
| DC | Accept w/ Minor (3M/5m) | Major (6M/8m) | Major (6M/13m) |
| DE | Accept w/ Minor (3M/4m) | Major (9M/10m) | Major (5M/12m) |
| DF | Accept w/ Minor (3M/5m) | Major (8M/9m) | Major (5M/14m) |
| DG | Accept w/ Minor (3M/4m) | Major (6M/8m) | Major (4M/14m) |
| **DH** | **Accept w/ Minor (2M/4m)** | **Major (6M/7m)** | **Major (5M/10m)** |

## Major Issues Remaining

### Priority 1: RESTORE Fig. coordinator_buffer_cdf (GPT #4, Claude #1 — BACKFIRED)
Both reviewers now want the buffer CDF figure back. Removing it was counterproductive.
**Fix:** Restore the figure. Keep DES section compact but include the plot.

### Priority 2: Abstract wording (Gemini #1 — trivial)
Change "Under a 1 kbps time-averaged per-node traffic allocation" to include "enforced via TDMA on a burst channel."
**Fix:** One sentence in abstract.

### Priority 3: Fleet-level scope (Claude #4 — NEW)
Title says "large autonomous space swarms" but analysis is per-cluster. Claude suggests retitling or adding fleet-level analysis.
**Fix:** Add brief fleet-level paragraph showing simultaneous active clusters under R=7 for representative shells. Or add "(Per-Cluster)" to title. Title change is safer.

### Priority 4: Model C coupling table (GPT #3 — elevated from minor)
GPT wants Model C ARQ×TDMA results in table form (30/35 kbps × M_r=0,1).
**Fix:** Add Model C rows to Table tdma_joint_interaction.

### Priority 5: Three-layer worked example (GPT #1 — persistent)
Wants step-by-step Algorithm 1 execution showing heuristic = Test B equivalence.
**Fix:** The sizing walkthrough is already there ("Sizing walkthrough: k_c=100, d=0.10, 35 kbps"). Expand slightly with explicit Test A/B steps.

### Priority 6: Topology comparison discussion (Claude #5 — NEW)
Wants intermediate architectures discussed.
**Fix:** Brief sentence acknowledging centralized+aggregation as an intermediate.

### Priority 7: Evidence tier relabeling (Claude #2 — persistent)
Wants CCSDS γ column relabeled from "Tier 2" to "Standards-based parameterization."
**Fix:** Rename column header in Table claim_map.

### Priority 8: p_cmd alternatives (GPT #2 — persistent)
Wants second mapping example showing non-i.i.d. commands.
**Fix:** Add one example: "ESA station-keeping: 5 commands/orbit-raising session, L_on=500 cycles → p_cmd ≈ 0.01."

### Priority 9: ∂R/∂γ sensitivity expression (Claude CS #3)
**Fix:** Add closed-form: ∂R_PHY,min/∂γ ≈ −C_coord,info/(γ² · α_RX).

### Priority 10: Raft randomized timeout (Claude minor #3)
Thundering herd analysis ignores Raft's built-in randomization.
**Fix:** Add note: "Raft randomized election timeout (150-300 ms) partially mitigates..."

## Text-Fixable Items for DI

1. **Restore Fig. coordinator_buffer_cdf** — CRITICAL
2. **Abstract wording** — "logical traffic allocation (enforced via TDMA on a burst channel)"
3. **Fleet-level paragraph or title qualification** — Brief analysis or scope qualifier
4. **Model C coupling rows** — Add to Table tdma_joint_interaction
5. **Sizing walkthrough expansion** — Explicit Test A/B steps
6. **Intermediate topology note** — Brief sentence
7. **Claim map column rename** — "Std.-based est." → "Std.-based param."
8. **p_cmd mapping example** — Second example
9. **∂R/∂γ expression** — Closed-form sensitivity
10. **Raft timeout note** — Brief caveat
11. **Unreferenced bibliography** — Remove dorigo_aco, kennedy_pso, karaboga_abc if not cited
12. **Coordinator summary size** — Clarify 371 B metadata
13. **Version tag** → paper-02-v-di
