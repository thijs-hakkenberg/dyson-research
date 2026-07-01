# Version CH Review Summary

## Reviewer Recommendations

| Reviewer | Recommendation | Major Issues | Minor Issues |
|----------|---------------|--------------|--------------|
| Gemini 3 Pro | **Accept with Minor Revisions** | 3 | 4 |
| GPT-5.2 | Major Revision | 6 | 10 |
| Claude Opus 4.6 | Major Revision | 5 | 12 |

## Rating Summary (1-5 scale)

| Category | Gemini (CH) | GPT (CH) | Claude (CH) | Gemini (CG) | GPT (CG) | Claude (CG) |
|----------|-------------|----------|-------------|-------------|----------|-------------|
| Significance & Novelty | 5 | 4 | 3 | 5 | 4 | 3 |
| Methodological Soundness | 5 | 3 | 3 | 5 | 3 | 3 |
| Validity & Logic | 4 | 3 | 4 | 4 | 3 | 4 |
| Clarity & Structure | 5 | 4 | 3 | 4 | 4 | 3 |
| Ethical Compliance | 5 | 4 | 4 | 5 | 4 | 5 |
| Scope & Referencing | 4 | 3 | 3 | 5 | 3 | 3 |

**Rating deltas (CH minus CG):** Gemini Clarity 4->5, Scope 5->4. GPT unchanged across all categories. Claude Ethical 5->4. Most ratings stable. Gemini's clarity improvement reflects satisfaction with notation/model disambiguation; scope dip reflects desire for more optical-ISL interaction discussion. Claude's ethical dip is on AI disclosure specificity (IEEE expects itemized scope).

## Progress from Version CG

Version CH addressed all 8 CG priority items and 25 minor issues:

1. **Feasibility baseline matrix + gamma subscripts** (CG Priority 1) -- Substantially addressed. New Table (feasibility_matrix) provides {Model S, Model C} x {24, 30 kbps} with explicit gamma subscripts. "MAC efficiency" renamed to "slot efficiency" throughout. GPT acknowledges "slot efficiency (gamma) and its impact on the 24 vs 30 kbps boundary is a meaningful improvement." GPT still wants further formalization of the feasibility framework layers (Layer 1 message-layer vs Layer 2 PHY/MAC vs eta/gamma screening heuristic). Claude satisfied with gamma consistency but notes "the intellectual contribution lies more in the systematic assembly and parameterization than in analytical depth."

2. **DES/verification narrative reframing** (CG Priority 2) -- Partially addressed. "Verification" replaced with "internal consistency check" for Tier 1; Section IV-J renamed to "Standards-Grounded Parameter Derivation"; DES <0.1% agreement compressed to footnote. However: Claude still finds "the DES verification remains primarily an internal consistency check" with "disproportionate emphasis relative to its evidential value." GPT: "DES 'verification' is correctly described as internal consistency, but still occupies substantial space." Both want further compression and rebalancing toward distributional/tail insights.

3. **30 kbps margin robustness** (CG Priority 3) -- Substantially addressed. New margin analysis table with systematic unmodeled overhead inventory (74 ms total -> 289 ms residual = 2.9%). New margin sensitivity figure (fig-margin-sensitivity) shows R_PHY,min vs (T_acq, T_guard). Claude and GPT both acknowledge the analysis but converge on a stronger recommendation: **elevate 35 kbps as the design point** (not just a footnote). Claude: "A sizing framework intended for practitioners should include adequate margin... the current framing of 30 kbps as 'minimum viable' with 2.9% margin is inconsistent with good engineering practice." GPT: "make the 30 kbps conclusion robust: elevate the conservative 35-38 kbps recommendation."

4. **Distributed planning overhead reconciliation** (CG Priority 4) -- Addressed. Canonical formula (Eq eta_consensus) with per-decision (2.8%) and per-cycle (31%) interpretations added. Distributed-planning stress case included. Claude: "The distributed consensus analysis (Eq. 5) shows eta_consensus ranges from 2.8% to 31% -- a fundamentally different scaling behavior" and wants centralized/distributed presented as "co-equal design options" rather than centralized-as-baseline.

5. **RF-backup mode operational clarity** (CG Priority 5) -- Addressed. Explicit hierarchical coordination suspension statement added; Algorithm 1 mode check added. GPT raises a new concern: the "1 kbps design-driving" narrative vs "hierarchy suspended during RF-backup" creates apparent contradiction. GPT wants a "Modes & Links" clarification artifact (figure/table) disambiguating per-node budget vs coordinator ingress PHY vs RF-backup capability. Gemini: coordinator failure "thundering herd" (100 nodes simultaneously detecting timeout) not accounted for in 160s recovery estimate.

6. **ARQ conclusion conditionality** (CG Priority 6) -- Addressed. ARQ viability threshold formalized; ISL measurement opportunities cited; conclusion conditional on coherence >= T_c. Gemini still wants a geometric justification for the 1-10s coherence estimate (e.g., solar array angular width / tumble rate).

7. **Coordinator ingress paired equations** (CG Priority 7) -- Addressed. Paired equations (info-rate and PHY-rate) added. GPT wants further disambiguation: "info-rate" vs "PHY rate" mixed in prose. GPT proposes a single "channel/mode map" figure early in the paper.

8. **Paper length** (CG Priority 8) -- Not improved. CG was 1221 lines / 15 pages; CH is 1295 lines / 16 pages. Content additions (new tables, canonical formula, paired equations, margin analysis, figures) outweighed compressions (fleet_reuse figure removal, eta_0 footnote). Claude: "The paper's length (14+ pages of dense material with substantial repetition) works against its goal of providing a clear, usable framework." Both Claude and GPT recommend consolidating tables and moving sensitivity analyses to supplementary material.

## Remaining Consensus Weaknesses (CH -> CI)

### Priority 1: Elevate 35 kbps design point recommendation
**Reviewers:** Claude (Major #2), GPT (Major #4, constructive #3)
**Issue:** All three reviewers now agree that 30 kbps with 2.9% residual margin is too thin for a practitioner-facing design framework. The margin sensitivity figure shows conservative assumptions push the minimum to ~35-38 kbps, yet 30 kbps is still stated as "the minimum viable design point."
**Fix:** Make 35 kbps the recommended design point in abstract, conclusion, and Algorithm 1. Present 30 kbps as the theoretical minimum with a caveat. This is the single most impactful change for reviewer acceptance.

### Priority 2: Channel/mode map clarification
**Reviewers:** GPT (Major #1), Gemini (Major #1 related)
**Issue:** The "1 kbps design-driving" narrative creates ambiguity: per-node budget (1 kbps) vs coordinator PHY (>=30 kbps) vs RF-backup link capability (~2.5 kbps). Which coordination functions run in each mode is not visually disambiguated. GPT: "Add a concise 'channel/mode map' figure/table early."
**Fix:** Add a boxed figure or table in Section II showing: (a) normal mode: optical ISL primary, RF control plane at 30+ kbps, full hierarchy; (b) RF-backup mode: beacon-only safe hold at ~2.5 kbps, hierarchy suspended; (c) per-node budget allocation: 1 kbps info-rate within the 30 kbps coordinator ingress.

### Priority 3: Further DES narrative compression
**Reviewers:** Claude (Major #1), GPT (Major #3)
**Issue:** Despite improvements, DES-analytical agreement still receives more space than warranted. Claude: "Reduce DES-analytical agreement discussion to a single sentence. Expand the distributional analysis with quantitative buffer-sizing recommendations." GPT: "Shorten repetitive 'DES matches analytical' statements."
**Fix:** (a) Cut all remaining DES-analytical agreement statements beyond the existing footnote. (b) Derive quantitative buffer-sizing recommendations from Fig. 7 (e.g., "buffer >= X kB for P99 < Y"). (c) Move DES methodology details to appendix.

### Priority 4: External validation (Tier 3) gap
**Reviewers:** Claude (Major #4), GPT (Major #4 implicit)
**Issue:** Table XII (claim map) shows Tier 3 (external validation) empty for all results. Claude: "For a journal publication claiming to provide 'design equations' for practitioners, the absence of any comparison to operational data, hardware-in-the-loop testing, or even NS-3 simulation is a significant limitation."
**Fix:** Options: (a) Implement single-cluster NS-3 simulation to validate gamma and superframe timing (Claude's top constructive suggestion). (b) Compare coordinator ingress sizing against published Iridium NEXT or Starlink parameters (even order-of-magnitude). (c) If neither is feasible, strengthen limitations section with explicit confidence bounds.

### Priority 5: Paper length and consolidation
**Reviewers:** Claude (Major implicit, constructive #3), GPT (implicit)
**Issue:** Paper grew from 15 to 16 pages despite compression goals. Multiple tables contain overlapping information (Tables V, VIII, X address feasibility at different granularities). Claude recommends merging into a single comprehensive feasibility table.
**Fix:** (a) Merge overlapping feasibility tables. (b) Move sectorized mesh, FEC rate sensitivity, and detailed DES methodology to supplementary material. (c) Target 12-13 pages. (d) Eliminate result restatements (eta ≈ 46% appears in 5+ locations).

### Priority 6: Formalize feasibility framework layers
**Reviewers:** GPT (Major #2)
**Issue:** The "three-layer feasibility framework" is described informally. eta_total/gamma appears as a decision boundary in Algorithm 1 but is actually a screening heuristic. GPT: "Formalize: Layer 1 = message-layer feasibility; Layer 2 = PHY/MAC feasibility; eta_total/gamma = derived utilization indicator, not a layer."
**Fix:** Add formal definitions box. Revise Algorithm 1 and table labels so eta_total/gamma is labeled "screening heuristic" with definitive checks pointing to the ingress/egress inequalities.

### Priority 7: GE coherence geometric justification
**Reviewers:** Gemini (Major #1), Claude (Major #5)
**Issue:** The 1-10s coherence estimate for structural shadowing lacks geometric derivation. Gemini: "Calculate the angular width of a solar array at typical spacecraft dimensions and divide by a representative tumble rate."
**Fix:** Add back-of-envelope calculation: 1m panel at 2m distance subtends ~26 deg; at 2 deg/s tumble rate, blockage lasts ~13s. This anchors tau_c >= T_c assumption with one paragraph.

### Priority 8: Correlated campaign model
**Reviewers:** GPT (Major #5)
**Issue:** Campaign duty factor d uses independent Bernoulli per node, but the most operationally relevant stress is fleet-correlated (conjunction response, mass orbit raising). GPT: "Add one correlated campaign model variant (e.g., all nodes in a cluster ON together)."
**Fix:** Add a simple "cluster-correlated ON/OFF" variant: all k_c nodes enter ON state simultaneously with probability d_cluster. Show effect on coordinator buffer tails and regional burstiness. Can reuse existing DES infrastructure.

## Minor Issues (Grouped)

### Notation and Units
1. **Info-rate vs PHY-rate in prose:** GPT notes several places where "info-rate" vs "PHY rate" vs "per-node budget" are mixed. Add consistent parenthetical labels.
2. **Eq. 14 dimensional clarity:** Claude: "The 10^-3 conversion factor is error-prone. Consider expressing guard/acquisition in seconds throughout." GPT: provide boxed "how to compute gamma" with one unit system.
3. **Eq. 5 symbol conflict:** Claude: R for Raft rounds conflicts with R for spatial reuse factor in Table I. Use distinct symbol.

### Tables and Figures
4. **Tables V/VIII/X consolidation:** Claude: merge into single comprehensive feasibility table.
5. **Fig. 3 caption:** Claude: specify whether "phase staggering" result is Model S or Model C.
6. **Table IX footnote b:** Claude: per-message rate formula assumes independence, contradicts GE model used elsewhere.
7. **Re-sync preamble 4 ms:** Claude: "Appears without derivation. At 30 kbps, 4 ms = 120 bits. Justify this value."
8. **Section V-B Walker constellation:** Claude: "Introduced without motivation. Is this Starlink-like? State explicitly."

### Scope and Referencing
9. **Satellite TDMA/DAMA references:** GPT: cite DVB-RCS2 or generic satellite DAMA/TDMA beyond Proximity-1.
10. **AoI canonical result:** GPT: cite specific AoI under Bernoulli sampling theorem, not just surveys.
11. **CCSDS 414.0-G-2:** Claude: cited in Table VII but missing from bibliography.
12. **Iridium/Starlink ISL data:** Claude: some conference proceedings contain Iridium crosslink data.
13. **DTN/CGR scheduling:** Claude: relevant scheduling results not cited.

### Presentation
14. **"TDMA required when eta/gamma > 50%":** GPT: label as heuristic, cite definitive test.
15. **AoI Eq. 29 scope:** GPT: clarify applies to geometric inter-report with deterministic service, no queueing coupling.
16. **M/D/1 compute bound:** GPT: "so disconnected from comms that it risks being a strawman."
17. **"stress-case commands account for >60% of stress-case traffic":** GPT: confusing tautology. Rephrase.
18. **Table 3 AoI P99 constant:** GPT: add note that this assumes exception probability unchanged.
19. **MAC contention not modeled:** GPT: add warning that CSMA feasibility at >=10 kbps is not guaranteed under dense interference.
20. **AI disclosure scope:** GPT: IEEE expects itemized scope (no AI-generated results, no AI-written text, etc.).
21. **Coordinator failure thundering herd:** Gemini: 100 nodes simultaneously detecting coordinator timeout could cause MAC collapse. Account for contention backoff.
22. **Unicast 310s command latency:** Gemini: explicitly state whether 5-minute latency is operationally acceptable for emergency reconfiguration.
23. **Abstract length:** Claude: at 280 words, exceeds IEEE T-AES guidelines (typically 200 words).
24. **LDPC rate 7/8 choice:** Gemini: briefly mention why 7/8 over 1/2.
25. **Table XI "Delivered" column:** Gemini: rename to "Theoretical Delivery (Byte Budget Only)" for Regime B.

## Constructive Suggestions (Ordered by Impact)

1. **Elevate 35 kbps as the recommended design point** (all three). Single highest-impact change for moving toward acceptance.
2. **Add channel/mode map figure** (GPT). One diagram resolving the 1 kbps / 30 kbps / 2.5 kbps confusion.
3. **Implement single-cluster NS-3 simulation** (Claude). Even a simplified version provides Tier 3 validation.
4. **Consolidate tables** (Claude). Merge V/VIII/X into one comprehensive feasibility table; cut 1-2 pages.
5. **Add geometric coherence justification** (Gemini). One paragraph anchoring tau_c >= T_c with concrete calculation.
6. **Add correlated campaign model** (GPT). Simple "all-ON" variant showing coordinator buffer impact.
7. **Formalize feasibility layers** (GPT). Box with Layer 1/Layer 2 definitions; eta/gamma as screening heuristic.
8. **Boxed "how to compute gamma"** (GPT). Worked example in one unit system with O_frame definition.
9. **Present centralized/distributed as co-equal** (Claude). Side-by-side comparison table showing architecture dependence.
10. **Address thundering herd** (Gemini). Slotted ALOHA throughput calculation for election traffic under coordinator failure.

## Action Items for Version CI

1. Make 35 kbps the recommended design point throughout (abstract, conclusion, Algorithm 1)
2. Add channel/mode map figure disambiguating per-node budget vs coordinator PHY vs RF-backup
3. Further compress DES narrative; derive quantitative buffer-sizing recommendations from tail distributions
4. Formalize feasibility framework: Layer 1 / Layer 2 definitions; eta/gamma as screening heuristic
5. Add geometric coherence justification (1 paragraph back-of-envelope calculation)
6. Add correlated campaign model variant (cluster-correlated ON/OFF)
7. Consolidate overlapping feasibility tables (V/VIII/X -> single table)
8. Provide boxed "how to compute gamma" recipe with consistent units and worked example
9. Address thundering herd in coordinator failure recovery (Slotted ALOHA contention estimate)
10. State unicast 310s latency acceptability explicitly
11. Fix Eq. 5 symbol conflict (R for Raft vs R for spatial reuse)
12. Add CCSDS 414.0-G-2 to bibliography
13. Target 12-13 pages (move DES methodology + sensitivity details to supplementary)
