# Version CG Review Summary

## Reviewer Recommendations

| Reviewer | Recommendation | Major Issues | Minor Issues |
|----------|---------------|--------------|--------------|
| Gemini 3 Pro | **Accept with Minor Revisions** | 2 | 4 |
| GPT-5.2 | Major Revision | 8 | 10 |
| Claude Opus 4.6 | Major Revision | 5 | 12 |

## Rating Summary (1-5 scale)

| Category | Gemini (CG) | GPT (CG) | Claude (CG) | Gemini (CF) | GPT (CF) | Claude (CF) |
|----------|-------------|----------|-------------|-------------|----------|-------------|
| Significance & Novelty | 5 | 4 | 3 | 5 | 4 | 3 |
| Methodological Soundness | 5 | 3 | 3 | 5 | 3 | 3 |
| Validity & Logic | 4 | 3 | 4 | 5 | 3 | 4 |
| Clarity & Structure | 4 | 4 | 3 | 5 | 4 | 3 |
| Ethical Compliance | 5 | 4 | 5 | 5 | 4 | 5 |
| Scope & Referencing | 5 | 3 | 3 | 4 | 3 | 4 |

**Rating deltas (CG minus CF):** Gemini Validity 5->4, Clarity 5->4, Scope 4->5. GPT unchanged across all categories. Claude Scope 4->3. Most ratings stable; Gemini's slight dips reflect newly surfaced RF-backup and topology-invariance concerns rather than regressions.

## Progress from Version CF

Version CG addressed several CF consensus weaknesses:

1. **Slot model harmonization** (CF Priority 1) -- Substantially addressed. Model S (simplified) and Model C (CCSDS-grounded) labels are now used throughout. Gemini: "the authors handle this reasonably well by explicitly flagging which model is used for feasibility claims." GPT still finds residual ambiguity in how gamma is applied across 24 vs 30 kbps and across models in tables, requesting a single "feasibility baseline matrix" and subscripted gamma notation everywhere.

2. **DES section compression** (CF Priority 2) -- Partially addressed. Table and two figures were removed. Claude and GPT still consider DES verification overweight and want it reframed around what only DES can provide (distributional buffer sizing, stochastic campaign tails). GPT: "DES is not validation of the equations; foreground its unique contributions."

3. **Table VI rebuilt at 30 kbps Model C** (CF Priority 7) -- Addressed. The 363 ms margin is now explicitly shown. Claude raises concern that 3.6% margin is "uncomfortably thin" and below typical space-systems engineering practice (10-20% at PDR). GPT requests sensitivity bands on T_acq and T_guard.

4. **alpha_RX updated to 0.944** (CF Priority 7) -- Addressed. Claude notes a minor discrepancy: alpha_RX is stated as 0.944 in notation but Table V shows ingress = 9,445 ms = 0.9445 of T_c. Needs clarification.

5. **L_cmd updated to 31 cycles** (CF Priority 7) -- Addressed. No further concerns from reviewers on this specific point.

6. **Layer-binding paragraph added** (CF Priority 4) -- Addressed. Gemini finds the two-layer framework "well-reasoned." GPT wants further formalization: rename to "two layers + one necessary condition" to distinguish the MAC utilization screening from true TDMA airtime feasibility.

7. **GE P95 qualified with "illustrative parameters"** (CF Priority 5) -- Addressed. Claude: "The paper honestly acknowledges that no ISL-specific GE measurement data are available." GPT: the ARQ conclusion should be explicitly conditional on coherence >= T_c.

8. **Minor items** (IEEE 1012 adapted, Eq 1 unnumbered, coordinator rotation clarified, campaign duty factor clarified as per-node Bernoulli) -- All addressed. No reviewers re-raised these.

## Remaining Consensus Weaknesses (CG -> CH)

### Priority 1: gamma consistency across models and rates
**Reviewers:** GPT (Major #1), Gemini (Minor #1), Claude (Minor #2)
**Issue:** While Model S/Model C labeling is improved, gamma still appears numerically without consistent subscripts (gamma_24 vs gamma_30) or model labels in several tables and claims. Table VIII header uses gamma_24 = 0.760 while Layer-2 feasibility discussion uses 30 kbps Model C (gamma_30 = 0.745). GPT: "Any ambiguity in which gamma applies where will undermine trust in the feasibility boundary."
**Fix:** Add a "feasibility baseline matrix" early in Results: rows = {Model S, Model C}, cols = {24, 30 kbps}. Subscript every numeric gamma appearance. Ensure every "TDMA required when..." heuristic specifies which gamma and which rate.

### Priority 2: DES/verification narrative reframing
**Reviewers:** Claude (Major #1, #2), GPT (Major #3, #4)
**Issue:** DES-analytical agreement is still presented as stronger evidence than warranted. The packet-level simulator derives gamma but does not independently validate the sizing equations (circular: all four models use the same slot duration formula). Claude: "Calling it 'verification' overstates the evidence." GPT: "Restructure so first paragraph states DES's unique contributions."
**Fix:** (a) Replace "verification" with "internal consistency check" for Tier 1 DES-analytical agreement. (b) Foreground DES distributional contributions (buffer tails, AoI distributions under stochastic campaigns). (c) Rename Section IV-J from "validation" to "parameter derivation" or "standards-grounded anchoring." (d) Compress "<0.1% agreement" to a single sentence or footnote.

### Priority 3: 30 kbps margin robustness (363 ms)
**Reviewers:** Claude (Major #3), GPT (Major #4)
**Issue:** 363 ms unallocated margin (3.6% of T_c) is thin by space-systems standards. Under GE steady-state, expected retransmission airtime (~755 ms) already exceeds this margin. Unmodeled overheads (ranging, control-plane, clock drift, acquisition variability) are identified but not systematically accounted for.
**Fix:** Conduct systematic margin analysis: tabulate all unmodeled overheads with conservative estimates, compute residual margin. Provide sensitivity band on T_acq and T_guard showing break-even R_PHY for k_c = 100. If margin becomes negative under conservative assumptions, revise minimum viable PHY rate recommendation (possibly to ~35 kbps).

### Priority 4: Distributed planning / consensus overhead reconciliation
**Reviewers:** GPT (Major #5, #6), Claude (Major #4, Minor #1), Gemini (Major #2)
**Issue:** eta_consensus = 3.1% per decision vs 30.7% per cycle -- an order-of-magnitude discrepancy likely due to per-decision vs per-cycle vs per-node accounting. The paper targets "autonomous swarms" but the sizing equations assume centralized command generation. Gemini: "topology-invariant" claim needs qualification for distributed consensus where traffic scales as O(k_c^2) or O(k_c).
**Fix:** (a) Audit and reconcile all consensus-overhead statements with one canonical formula specifying payload bytes, number of rounds, quorum size, per-node vs per-cluster, and frequency. (b) Add a worked distributed-planning stress case showing how eta and airtime feasibility change. (c) Qualify the "topology-invariant" claim in the abstract to note it applies under centralized command generation.

### Priority 5: RF-backup mode operational clarity
**Reviewers:** Gemini (Major #1), Claude (implicit in Major #3)
**Issue:** Coordinator requires ~27 kbps ingress but RF-backup (UHF Omni) provides only ~2.5 kbps. The hierarchical coordination protocol cannot function in RF-backup mode. The text mentions "safe hold" and "inertial coasting" but feasibility analysis is ambiguous about whether coordination continues or the system reverts to beacon-only.
**Fix:** Explicitly state that hierarchical coordination is suspended during RF-backup due to the 2.5 kbps < 27 kbps deficit. Clarify that RF-backup is exclusively for survival/safe-mode (heartbeats + collision alerts). Consider adding a "Mode Check" step at the beginning of Algorithm 1.

### Priority 6: ARQ conclusion conditionality
**Reviewers:** GPT (Major #7), Claude (Major #5)
**Issue:** The "intra-cycle ARQ is structurally ineffective" conclusion depends on GE coherence >= T_c and illustrative parameters. Without ISL-specific data, this is scenario-specific. GPT wants a derivation of the threshold coherence (in slots) where ARQ becomes feasible given margin.
**Fix:** (a) Make ARQ conclusion explicitly conditional in abstract/conclusion ("for obstructions with coherence >= T_c"). (b) Formalize the margin-vs-retransmission-airtime relationship from Fig. 14 into a design rule. (c) Identify specific ISL measurement campaigns that could calibrate the model.

### Priority 7: Coordinator ingress equation presentation
**Reviewers:** GPT (Major #8)
**Issue:** Coordinator ingress is sometimes presented as raw bps requirement and sometimes as PHY requirement divided by gamma. Practitioners need a single canonical equation distinguishing information-rate from PHY-rate requirements.
**Fix:** Present two explicit equations side-by-side: (1) information rate requirement C_coord,info, (2) PHY rate requirement R_PHY >= C_coord,info / gamma + airtime feasibility constraints. Ensure all numeric examples state which one they compute.

### Priority 8: Paper length
**Reviewers:** Claude (Major, constructive suggestion #4), GPT (implicit)
**Issue:** At ~12,000+ words body text, the manuscript substantially exceeds typical IEEE T-AES limits. Sensitivity analyses and detailed eta_0 audit could move to supplementary material.
**Fix:** Target ~20-30% reduction. Candidates: FEC rate sensitivity, coherence-time sensitivity, detailed eta_0 audit, sectorized mesh discussion. Consider splitting into two papers: (a) sizing framework with Algorithm 1; (b) TDMA schedulability analysis with slot-level and packet-level simulation.

## Minor Issues (Grouped)

### Notation and Units
1. **gamma subscripts:** Enforce gamma_24 or gamma_30 subscripts on every numeric appearance; never bare gamma with a number (GPT Minor #1, #4, #10)
2. **Eq. 5/13 units:** Explicitly state R_PHY units (bps vs kbps) near the equation to prevent implementation errors (Gemini Minor #1, Claude Minor #2)
3. **alpha_RX precision:** 0.944 vs 0.9445 discrepancy needs resolution (Claude Minor #3)
4. **"MAC efficiency" terminology:** gamma includes PHY framing/FEC/acquisition; consider renaming to "slot efficiency" or "airtime efficiency" (GPT Minor #4)
5. **kbps labeling:** Distinguish "kbps (info)" vs "kbps (PHY)" in key tables (GPT Minor #10)
6. **Baseline telemetry directionality:** Clarify whether 20.5% includes only uplink (node->coord) or also downlink (GPT Minor #6, #7)

### Tables and Figures
7. **Table VIII Model S/C mixing:** Caption or split needed to avoid misreading across 24/30 kbps and Model S/Model C (GPT Minor #1)
8. **Table XIV slot-duration mismatch:** 115.5 ms vs 111.5 ms at 24 kbps -- reconcile framing/acq/guard rounding (GPT Minor #2)
9. **Table VIII Regime B footnote:** Clarify that M_r = 2 is theoretical/byte-budget only for RF-backup regime (Gemini Minor #3)
10. **Table II collision avoidance rate:** 10^-4/node/s yields ~8.6 events/node/day; distinguish screening notifications from maneuver commands in table itself (Claude Minor #5)
11. **Table III bandwidth breakdown:** Show actual value at N = 10^5 for G.-S. Mesh O(N) aggregation (Claude Minor #11)
12. **Figure 10 caption:** Distinguish between Bernoulli process and resultant bimodal buffer state distribution (Gemini Minor #2)

### Scope and Referencing
13. **Non-archival references:** Strengthen archival referencing for operational analogues, acquisition/turnaround timing (GPT Minor #5, Claude Scope)
14. **Network calculus:** Reference mentioned once but not meaningfully engaged with despite direct relevance (Claude Scope)
15. **TDMA in space systems:** No references to actual ISL MAC protocols (Iridium NEXT, Starlink); add or note absence (Claude Scope)
16. **GE loss notation:** Ensure consistent notation for p_success under i.i.d. vs p_B^{M_r+1} under GE (GPT Minor #8)

### Presentation
17. **Abstract length:** ~350 words exceeds IEEE T-AES guidelines (150-250 words); condense (Claude Minor #8)
18. **Abstract precision:** Clarify coordinator ingress ~27 kbps is for cluster coordinator specifically (Gemini Minor #4)
19. **Algorithm 1 line 7 threshold (0.50):** Not justified; provide rationale or remove (GPT Minor #3)
20. **eta_0 audit 0.5 pp gap:** Detailed explanation could be a footnote (Claude Minor #7)
21. **Coordinator D[k_c]/D/1 batch latency:** Cite or briefly justify the approximation (GPT Minor #9)
22. **Slotted ALOHA fallback:** Note expected delay under ALOHA, not just throughput feasibility (Claude Minor #12)
23. **Coordinator failure independence:** State explicitly that 6.3 x 10^-12 assumes independence; common-cause failures could correlate (Claude Minor #4)
24. **Authorship:** "Project Dyson Research Team" needs named authors before IEEE submission (Claude Minor #9)
25. **Reference [52] (dyson_multimodel):** Note that it is not peer-reviewed (Claude Minor #10)

## Constructive Suggestions (High-Value, Ordered by Impact)

1. **Systematic margin analysis at 30 kbps** (Claude, GPT): Tabulate all unmodeled overheads, compute residual margin, provide margin-vs-R_PHY curve. This directly affects the paper's primary design recommendation.
2. **Feasibility baseline matrix** (GPT): Single table early in Results: rows = {Model S, Model C}, cols = {24, 30 kbps}, with gamma, slot duration, margin for each cell. Every subsequent result references this matrix.
3. **Reconcile and integrate distributed planning overhead** (all three): Canonical eta_consensus formula with worked example for cluster-local planning.
4. **Reframe verification narrative** (Claude, GPT): Each tool's unique contribution stated upfront; drop "validation" for Tier 1; foreground distributional insights.
5. **Sensitivity chart for R_PHY,min** (GPT): Plot vs (T_acq, T_guard, FEC rate) for k_c = 100. Converts "standards-grounded" claim into a robust design chart.
6. **Algorithm 1 mode check** (Gemini): Add RF-backup capacity check at algorithm entry to formalize the finding that hierarchy is bandwidth-constrained in backup modes.
7. **Practitioner's quick-start subsection** (Claude): Walk through Algorithm 1 with two worked examples at different scales.
8. **Tighten ARQ design rule** (GPT): Formalize threshold coherence (in slots) where ARQ becomes viable given margin.
9. **gamma vs R_PHY subplot** (Gemini): Show efficiency sweet spot vs PHY rate for practitioners.
10. **Consider two-paper split** (Claude): (a) Sizing framework + Algorithm 1; (b) TDMA schedulability with slot/packet simulation.

## Action Items for Version CH

1. Add feasibility baseline matrix: {Model S, Model C} x {24, 30 kbps} with subscripted gamma throughout
2. Conduct systematic margin analysis at 30 kbps with all unmodeled overheads
3. Reconcile eta_consensus (3.1% vs 30.7%) with canonical formula; add distributed-planning stress case
4. Reframe DES as "internal consistency check"; foreground distributional contributions; compress further
5. Rename packet-level Section IV-J from "validation" to "parameter derivation"
6. Explicitly state hierarchical coordination is suspended during RF-backup mode
7. Make ARQ conclusion conditional on coherence >= T_c; formalize threshold coherence design rule
8. Present coordinator ingress as paired equations (information-rate vs PHY-rate)
9. Reduce paper length ~20-30% (move sensitivity analyses to supplementary material)
10. Enforce gamma subscripts, distinguish info-rate vs PHY-rate in all tables, condense abstract
