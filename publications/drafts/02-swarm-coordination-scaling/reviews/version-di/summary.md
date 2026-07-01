# Version DI Review Summary

## Recommendations

| Reviewer | Recommendation | Change from DH |
|----------|---------------|----------------|
| Gemini 3 Pro | **Accept with Minor Revisions** | Regressed (2M/4m→3M/4m) |
| GPT-5.2 | **Major Revision** | REGRESSED (6M/7m→8M/10m) |
| Claude Opus 4.6 | **Major Revision** | Stable/mixed (5M/10m→5M/12m) |

## What DI Fixed (Acknowledged by Reviewers)

1. **Restored Fig. coordinator_buffer_cdf** -- Claude: DH #1 evolved to DI #1 (still wants more, but acknowledges "distributional tails are the DES's incremental contribution"). GPT: DH #4 ("add buffer CDF") was addressed but GPT now wants nontrivial phenomena beyond confirmation.
2. **Fleet-level paragraph** -- Claude DH #4 (fleet-level claims unsupported) NOT re-raised as major. The simultaneous-active-clusters paragraph was absorbed.
3. **Topology comparison intermediate note** -- Claude DH #5 (topology comparison asymmetric) NOT re-raised as major. The intermediate architectures sentence was absorbed.
4. **Model C coupling rows** -- GPT DH #3 (Model S table misconstrued) evolved; the Model C rows were added but GPT now wants a promoted γ ledger table (#2).
5. **Sizing walkthrough expansion** -- GPT DH #1 (three-layer framework) partially addressed. The detailed walkthrough was acknowledged but GPT still wants cleaner separation.
6. **∂R/∂γ expression** -- Claude DH #3 (γ limited without hardware) partially addressed. Claude now wants joint (p_B, p_BG) sensitivity analysis instead.
7. **p_cmd mapping examples** -- GPT DH #2 (p_cmd alternatives) partially addressed. GPT still wants formal d/p_cmd definition.
8. **Raft randomized timeout** -- Claude minor #3: NOT re-raised. Note absorbed.
9. **Unreferenced bibliography** -- Cleaned up. Not re-raised.
10. **Coordinator summary size** -- Metadata breakdown added. Not re-raised.
11. **Abstract wording** -- Gemini DH #1: NOT re-raised as separate issue (absorbed).
12. **Claim map column rename** -- Claude minor #8 says "Std.-based param." still unclear; wants "Standards-anchored estimate."

## What BACKFIRED

1. **Adding content increased paper length to 13 pages** -- Claude DI #5 explicitly criticizes paper as "substantially too long" and wants 30-40% reduction. GPT #4 notes redundancy. The added content (Model C rows, walkthrough, fleet paragraph, ∂R/∂γ eq, intermediate topology) collectively triggered length complaints.
2. **Detailed walkthrough triggered GPT scope creep** -- GPT now wants probabilistic Test B (#7), practitioner worksheet (#8), and formal γ ledger table (#2). The more precise the paper gets, the more precision GPT demands.
3. **Model C coupling rows triggered γ consistency audit request** -- GPT #2 now wants a promoted γ ledger table with unit-test checks in repo.

## Gemini Regression (2M→3M)

DH→DI resolved:
- DH #1 (abstract wording) → RESOLVED

DH→DI evolved:
- DH #2 (p_BG sensitivity) → DI #2 (T_acq sensitivity / safety factor — different concern)

New:
- DI #1: Static membership validation (persistent from earlier versions, re-raised with stronger framing)
- DI #3: Unicast command latency contextualization (NEW — 190s too slow for some autonomy tasks)

## GPT REGRESSION (6M→8M, 7m→10m)

DH→DI resolved:
- DH #4 (buffer CDF figure) → ADDRESSED (figure restored), but DES still major (#5)

DH→DI persistent (6 of 8 DI majors are persistent):
- DH #1 (three-layer framework) → DI #1 (now "γ is not MAC efficiency" — rename request)
- DH #2 (p_cmd alternatives) → DI #3 (campaign d mapping under-specified — wants formal definition)
- DH #5 (packet-level not independent) → DI #6 (persistent — rename subsection)
- DH #6 (γ measurement pipeline) → DI #8 (practitioner workflow fragile — wants worksheet)

New/elevated:
- DI #2: γ consistency ledger (elevated from minor → major; wants promoted table)
- DI #4: 46% stress-case labeling (was implicit concern, now explicit major)
- DI #7: Deterministic guard/acq → probabilistic Test B (NEW — wants P(miss) vs R_PHY)
- DI #8: Practitioner worksheet (elevated from constructive → major)

## Claude Stable (5M→5M, 10m→12m)

DH→DI resolved:
- DH #4 (fleet-level claims) → RESOLVED (fleet paragraph absorbed)
- DH #5 (topology comparison) → RESOLVED (intermediate note absorbed)

DH→DI persistent:
- DH #1 (DES limited) → DI #1 (persistent — condense mean-value, expand sensitivity)
- DH #2 (packet-level is parameter anchoring) → DI #2 (escalated — now wants NS-3)
- DH #3 (γ without hardware) → DI #3 (evolved — wants joint p_B/p_BG sensitivity)

New:
- DI #4: 1 kbps budget scrutiny (NEW — why is 1 kbps important? Modern ISLs can do more)
- DI #5: Scope ambiguity (NEW — "design framework" vs "system design" precision mismatch)

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
| DH | Accept w/ Minor (2M/4m) | Major (6M/7m) | Major (5M/10m) |
| **DI** | **Accept w/ Minor (3M/4m)** | **Major (8M/10m)** | **Major (5M/12m)** |

## Analysis: Why GPT Regressed

GPT's regression from 6M to 8M appears driven by:
1. **Content additions triggered higher expectations.** The detailed Model C coupling table, ∂R/∂γ expression, and expanded walkthrough showed the paper CAN provide more precision, which made GPT demand probabilistic treatment, formal definitions, and practitioner worksheets.
2. **Paper length increased.** 13 pages (from 12) with more content gave GPT more surface area to critique.
3. **Minor→major elevation.** Items that were minor suggestions in DH became majors in DI (γ ledger, stress-case labeling, practitioner workflow).

## Strategy for Version DJ

**Key insight: The paper needs to get SHORTER, not longer.** Adding content has consistently triggered reviewer scope creep. The most successful versions (DH: 12 pages, 6+5 majors) were compact.

### Priority 1: Compress to ≤12 pages (ALL REVIEWERS)
- Remove Model S analysis from main text (GPT #1, Claude #4) — move to appendix
- Remove thundering herd analysis (Claude minor #3 — tangential)
- Consolidate redundant restatements of 46%/35 kbps
- Merge Tables V+VI into one compact feasibility table
- Condense DES mean-value discussion to one sentence (Claude #1, GPT #5)

### Priority 2: Rename γ consistently to "slot efficiency" (GPT #1)
- Replace ALL instances of "MAC efficiency" with "slot efficiency"
- Add boxed definition: "γ accounts for per-slot non-payload time under scheduled TDMA; does not include contention"

### Priority 3: Formalize d/p_cmd (GPT #3)
- Define p_eff = d·p_cmd explicitly
- Rewrite Eq. eta_canonical in terms of p_eff

### Priority 4: Add unicast latency classification (Gemini #3)
- Explicit table: which autonomy tasks work at 190s vs need optical ISL

### Priority 5: Formal feasibility threshold (Claude #5)
- Define: "feasible" = deadline miss rate ≤ 1%
- Apply consistently to 30 kbps (12% misses = infeasible) vs 35 kbps (0% = feasible)

### Priority 6: 1 kbps motivation (Claude #4)
- Add explicit justification: power-constrained CubeSat-class radios, mass budget < 1 kg
- Note that framework extends to higher C_node (Table bandwidth_scaling already shows this)

### Priority 7: Algorithm 1 safety factor (Gemini #2)
- Add margin threshold in Algorithm 1: margin ≥ 10% of T_c

### Priority 8: Stress-case labeling (GPT #4)
- In every table/figure with 46%, label "continuous-duty upper bound (rare)"

### Deferred (structural, not text-fixable)
- NS-3 external validation (Claude #2)
- Probabilistic Test B with jitter distributions (GPT #7)
- Joint (p_B, p_BG) sensitivity heatmap (Claude #3)
- Practitioner worksheet appendix (GPT #8)

## Text-Fixable Items for DJ

1. **Compress paper to ≤12 pages** — CRITICAL (remove Model S from main text, condense DES, merge tables)
2. **Rename γ to "slot efficiency" throughout** — search/replace "MAC efficiency"
3. **Define p_eff = d·p_cmd** — one equation + mapping update
4. **Unicast latency classification** — 2-3 sentences
5. **Formal feasibility threshold** — define miss rate ≤ 1%, apply
6. **1 kbps motivation** — 2 sentences (power/mass constraint)
7. **Algorithm 1 safety factor** — already has margin < 10% warning; strengthen
8. **Stress-case labeling** — audit all 46% occurrences
9. **α_RX → M_r mapping** — add explicit formula or table
10. **C_node to Algorithm 1 REQUIRE** — add input
11. **Version tag** → paper-02-v-dj
