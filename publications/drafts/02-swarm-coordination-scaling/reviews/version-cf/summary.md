# Version CF Review Summary

## Reviewer Recommendations

| Reviewer | Recommendation | Major Issues | Minor Issues |
|----------|---------------|--------------|--------------|
| Gemini 3 Pro | **Accept** | 0 | 4 |
| GPT-5.2 | Major Revision | 8 | 10 |
| Claude Opus 4.6 | Major Revision | 5 | 12 |

## Rating Summary (1-5 scale)

| Category | Gemini | GPT | Claude |
|----------|--------|-----|--------|
| Significance & Novelty | 5 | 4 | 3 |
| Methodological Soundness | 5 | 3 | 3 |
| Validity & Logic | 5 | 3 | 4 |
| Clarity & Structure | 5 | 4 | 3 |
| Ethical Compliance | 5 | 4 | 5 |
| Scope & Referencing | 4 | 3 | 4 |

## Progress from Version CE

Version CF successfully addressed several CE consensus weaknesses:

1. **k_c vs k_c-1 consistency** (CE: GPT Major #2) -- Fixed. All reviewers now cite consistent notation.
2. **DES reframing** (CE: Summary #2) -- Partially addressed. Gemini rates methodology 5/5. GPT and Claude still want the DES sections compressed further and distributional results tied to concrete sizing outputs.
3. **Stress-case narrative** (CE: Summary #1) -- Addressed. All three reviewers note the improved framing (routine η≈5-10%, stress as episodic upper bound). Claude calls it "a significant improvement."
4. **γ rate-dependence** (CE: GPT Major #4) -- Addressed. Claude notes "consistently applied throughout." GPT finds residual slot-duration mismatches between simplified and standards-grounded models.
5. **Topology comparison** (CE: Summary #5) -- Addressed. The capability matrix and comparability caveat resolve the apples-to-oranges concern.
6. **Feasibility algorithm** (CE: GPT Major #1) -- Added. Gemini rates it "helpful addition for practitioners." GPT wants refinements to the 50% TDMA heuristic.
7. **RF-backup justification** (CE: Gemini Major #1) -- Addressed. No further concerns from Gemini.
8. **ARQ scoping** (CE: GPT Major #9) -- Addressed. The explicit scoping to slow-mixing regimes is noted positively.
9. **γ expression clarity** (CE: Claude Major #3) -- Addressed. Time-domain form added with worked example.
10. **Tail CIs** (CE: Summary #6) -- Partially addressed. AoI P99 CI is present; GE P95 CI added. Claude wants more prominent qualification of GE default-parameter specificity.

## Remaining Consensus Weaknesses (CF → CG)

### Priority 1: Slot-duration / γ model harmonization
**Reviewers:** GPT (Major #1, #2), Claude (Minor)
**Issue:** Table VI superframe uses simplified slot model (92.7 ms, γ=0.949); Table XXIII uses standards-grounded model (115.5 ms, γ=0.760). Both are correct for their respective assumptions but the manuscript interleaves them without clear labeling. GPT: "These cannot all be true simultaneously."
**Fix:** Create explicit "Assumption Set A" (slot-only, no FEC/acq) and "Assumption Set B" (CCSDS standards-grounded). Label every table/claim with which set it uses. Alternatively, make the standards-grounded model primary and relabel the slot-only results as "illustrative simplified model."

### Priority 2: DES section compression
**Reviewers:** Claude (Major #1, #5), GPT (Major #4)
**Issue:** DES verification consumes ~2 pages for results that are tautological by construction. The genuine DES contribution (distributional CDF, ON/OFF tail analysis) is buried.
**Fix:** Reduce Section IV-F to ~0.5 pages. Retain Fig. 8 and ON/OFF analysis. Compress Table VII to a single sentence. Extract concrete buffer-sizing guidance from the distributional results (e.g., "buffer capacity multiplier vs d and burst length").

### Priority 3: Paper length reduction
**Reviewers:** Claude (Major #5), GPT (implicit)
**Issue:** Paper is ~12,000 words body text, substantially exceeding typical IEEE TAES length. Key results are repeated across abstract, introduction, results, discussion, and conclusion.
**Fix:** Target 20% reduction. Candidates: DES section (Priority 2); sectorized mesh (footnote); fleet reuse (appendix); repeated numerical results.

### Priority 4: Feasibility framework layer clarity
**Reviewers:** GPT (Major #3), Claude (Major #3)
**Issue:** The "two-layer" framework presentation mixes "necessary condition" and "decision rule." The η_total/γ < 0.50 threshold is used as a TDMA/CSMA switch criterion but is not derived as such.
**Fix:** Add explicit paragraph stating when each layer is binding. Label η_total/γ as a "coarse utilization indicator." Make the TDMA airtime inequalities (Eqs. 33-34) the actual decision criterion.

### Priority 5: GE parameter qualification
**Reviewers:** Claude (Major #2), GPT (implicit)
**Issue:** "P95 = 4 cycles" appears in abstract and conclusion as if validated, but depends on illustrative parameters lacking ISL-specific empirical grounding.
**Fix:** Qualify in abstract/conclusion: "P95 recovery in 4 cycles *at illustrative parameters* ($p_{BG} = 0.50$); sensitivity curves span 3-18 cycles." Add brief discussion of what ISL-specific measurements would calibrate the model.

### Priority 6: Campaign duty factor correlation
**Reviewers:** GPT (Major #5, #6)
**Issue:** d is per-node Bernoulli, but real campaigns are fleet-correlated (many nodes commanded together). Broadcast vs unicast command semantics not fully explored.
**Fix:** Clarify d as per-node independent. Add one fleet-correlated campaign case. Add broadcast-only stress case showing lower η than per-node command assumption.

### Priority 7: α_RX and stagger consistency
**Reviewers:** GPT (Major #8)
**Issue:** α_RX = 0.918 depends on slot model (simplified vs standards-grounded). L_cmd may change under CCSDS-derived slots.
**Fix:** Recompute α_RX and L_cmd under standards-grounded slot model. Show the difference.

## Constructive Suggestions (High-Value)

1. **Restructure around Algorithm 1** (Claude): Make the feasibility algorithm the central organizing element to reduce repetition
2. **Present γ as parameter band** (GPT): γ ∈ [0.70, 0.82] with sensitivity to acq dwell, guard, code rate
3. **Practitioner's summary sidebar** (Claude): Single-page containing algorithm, γ equation, duty-factor table, GE design curves
4. **Network calculus comparison** (Claude): Periodic traffic model is ideal for network calculus bounds
5. **"What would change conclusions" paragraph** (Claude): Identify which assumption violations invalidate key results

## Action Items for Version CG

1. Harmonize slot model: label "simplified" vs "CCSDS-grounded" everywhere
2. Compress DES section to ~0.5 pages, extract buffer sizing guidance
3. Reduce total paper length by ~20%
4. Add explicit layer-binding paragraph to feasibility framework
5. Qualify GE P95 in abstract and conclusion
6. Add fleet-correlated campaign case
7. Recompute α_RX under standards-grounded model
