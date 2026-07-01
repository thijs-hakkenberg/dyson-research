---
paper: "02-swarm-coordination-scaling"
version: "dl"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-03-06"
recommendation: "Unknown"
---



# Peer Review: Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms

## 1. Significance & Novelty
**Rating: 3 (Adequate)**

The paper addresses a genuine gap: closed-form parametric sizing for hierarchical coordination at $10^3$–$10^5$ node scales with byte-level traffic accounting. The two-test feasibility framework (byte budget + TDMA airtime) and the campaign duty factor parameterization are useful conceptual contributions. However, the novelty is primarily in the *assembly* of well-known components (TDMA slot efficiency, M/D/1 queueing, Gilbert-Elliott channels, Raft consensus, AoI) rather than in new analytical methods. The slot efficiency formula (Eq. 7) is acknowledged as standard (cf. DVB-RCS2). The paper's value proposition rests on the specific coupling of these elements for space swarm sizing—a reasonable but incremental contribution. The restriction to loose coordination via S-band (with tight formation control explicitly deferred to optical ISL) narrows the practical scope considerably.

## 2. Methodological Soundness
**Rating: 3 (Adequate)**

The three-layer feasibility framework (byte budget, MAC efficiency, TDMA airtime) is logically structured, and the authors are commendably transparent about what each layer does and does not capture. The campaign duty factor $d$ is a welcome addition that substantially improves workload realism—the mapping to mission phases (Table in §IV-E) with empirical anchoring to ESA CA statistics is well done. The yearly mixture calculation ($\bar{\eta} = 5.6\%$) effectively contextualizes the stress-case.

However, several methodological concerns remain:

- The DES verification is acknowledged as tautological (Tier 1: same equations, <0.1% agreement "by construction"). The claimed incremental value—distributional tails under campaign burstiness—is conditional on the assumed Markov ON/OFF model, which is itself unvalidated. The DES thus provides limited genuine value beyond confirming implementation correctness.
- The packet-level validation (§IV-J) anchors $\gamma$ to CCSDS Proximity-1 standards, which is a parameter *derivation* rather than *validation*. The authors correctly label this, but the claim map (Table VII) listing "CCSDS $\gamma$" as a separate evidence tier somewhat overstates its independence.
- The GE channel model parameters ($p_G = 0.01$, $p_B = 0.90$, $p_{BG} = 0.50$) lack any empirical grounding for ISL channels. While the authors frame this as a "what-if design tool," the specific numeric results (P95 = 4 cycles, 27% intra-cycle recovery) are presented with a precision that may mislead readers about their reliability.

## 3. Validity & Logic
**Rating: 3 (Adequate)**

The gamma unification to 0.76 (replacing the earlier 0.85) via CCSDS derivation is consistently applied throughout—I verified this across Tables III, V, VI, VIII, IX, X, and Algorithm 1. The $\gamma$ consistency ledger (Table X footnote) is a good practice.

The stress-case ($\eta_S \approx 46\%$) is now properly contextualized as a continuous-duty upper bound occurring <1% of operational time, with the yearly mixture calculation providing concrete grounding. This is a significant improvement.

Logical concerns:

1. **Circular dependency in $\alpha_{RX}$**: The paper states $\alpha_{RX}$ is a "computed output, not a free parameter" (Table I, Algorithm 1 line 6), yet it appears in the design heuristic (Eq. 6) which is used to *determine* $R_{PHY}$. The iterative resolution (Algorithm 1, line 8: "increase $R_{PHY}$; repeat") handles this, but the heuristic presentation in the feasibility box could confuse practitioners.

2. **The three-layer framework collapses to two tests**: The authors state "Do not apply the heuristic AND separately compute slot-level ingress; they are algebraically equivalent" and "$C_{raw} = C_{coord,info}/\gamma$ is a unit conversion within Test B, not a separate test." This is correct but raises the question of why the framework is described as having three layers in some places.

3. **Static cluster membership assumption**: The J2 analysis showing <0.5% overhead for cross-plane re-association is reassuring for Walker constellations, but the worst-case boundary cluster analysis (once per orbit) is insufficiently developed—coordinator state continuity during handoff is flagged but not analyzed.

## 4. Clarity & Structure
**Rating: 2 (Below Average)**

This is the paper's most significant weakness. The manuscript is extremely dense, heavily cross-referenced, and suffers from organizational problems that impede comprehension:

- **Excessive defensive annotation**: Nearly every claim is followed by parenthetical qualifiers, cross-references, and caveats. While intellectual honesty is commendable, the result is prose that is nearly unreadable. Example: "Under Model~C (CCSDS;CCSDS-grounded, Table~\ref{tab:rate_feasibility}): ingress $= 11{,}108$~ms at 24~kbps (infeasible, margin $= -1{,}300$~ms); ingress $= 9{,}078$~ms at 30~kbps, margin $= 680$~ms (incl.\ ACK)."

- **Redundancy**: The same results are stated multiple times across different sections. The 35 kbps recommendation appears in at least 8 distinct locations. The $\gamma$ values are repeated in Tables III, VI, VIII, IX, X, and the consistency ledger.

- **Section organization**: Results (§IV) mixes derivation, simulation, and discussion. The "Discussion" (§V) contains key design equations that belong in a methods section. The notation table is placed before the reader has context for most symbols.

- **Figure quality**: Figures are referenced but not evaluable in this review format. The descriptions suggest appropriate content, but the paper would benefit from a consolidated design-space figure showing the feasibility region in ($k_c$, $R_{PHY}$, $d$) space.

- **Length**: At ~12 pages of dense technical content plus extensive tables, the paper exceeds what is digestible. A 20-30% reduction focusing on the core two-test framework would improve impact.

## 5. Ethical Compliance
**Rating: 4 (Good)**

The paper provides commendable transparency: code/data availability with specific repository tag, explicit AI disclosure (ideation only, not results/figures), clear labeling of validation tiers, and honest acknowledgment that "no external validation exists." The claim map (Table VII) is an excellent practice that more papers should adopt. The only concern is that the AI tool versions cited (Claude 4.6, GPT-5.2) appear to be future/hypothetical versions, which is unusual.

## 6. Scope & Referencing
**Rating: 3 (Adequate)**

The reference list (55 items) covers the relevant domains: CCSDS standards, AoI theory, swarm robotics, constellation management, queueing theory, and distributed consensus. Key omissions:

- No references to actual CubeSat S-band ISL demonstrations (e.g., KSAT, Kepler Communications)
- Limited coverage of actual TDMA implementations in space (beyond DVB-RCS2, which is ground-terminal focused)
- No reference to the extensive literature on TDMA scheduling optimization (e.g., graph coloring approaches for spatial reuse)
- Network calculus [Le Boudec] is cited but not used; either apply it or remove the citation
- The Huang [2006] and Li [2020] references appear in the bibliography but are not cited in the text

The paper is appropriate for IEEE T-AES in scope, though the lack of external validation weakens the case for this venue versus a workshop or letters format.

---

## Major Issues

1. **The DES provides negligible independent value and consumes significant page budget.**
   - *Issue*: The authors acknowledge the DES reproduces closed-form means "by construction" (<0.1% agreement). The sole claimed incremental contribution—distributional tails under Markov ON/OFF burstiness—is conditional on an unvalidated burst model. The MMPP/D/1 fluid bound already corroborates the buffer factor analytically.
   - *Why it matters*: ~2 pages of DES description and results (§III-A, §IV-F, Fig. 3) add little scientific content while consuming space that could strengthen the core analytical contribution.
   - *Remedy*: Reduce DES to a single paragraph confirming implementation correctness. Move distributional analysis to supplementary material. Use recovered space to develop the analytical framework more clearly or add the NS-3 comparison from the validation roadmap.

2. **The paper lacks any form of external or independent validation.**
   - *Issue*: All three verification tools (closed-form, DES, slot-sim) share the same equations and assumptions. The CCSDS-based $\gamma$ derivation is a parameter calculation, not validation. Table VII honestly shows empty Tier 3 columns, but this means every quantitative claim is unverified.
   - *Why it matters*: For a journal publication, the complete absence of independent validation—even a comparison against NS-3 for a simplified scenario, or against published DVB-RCS2 performance data—significantly weakens confidence in the results.
   - *Remedy*: (a) Compare $\gamma$ predictions against published DVB-RCS2 slot efficiency measurements (available in ETSI test reports). (b) Implement a minimal NS-3 scenario (single cluster, 100 nodes, TDMA) to validate at least the deadline miss rates. (c) If neither is feasible, reframe the paper explicitly as a "design methodology" contribution and submit to a venue where preliminary analytical frameworks are appropriate (e.g., conference proceedings or a short communication).

3. **Presentation density renders the paper nearly impenetrable.**
   - *Issue*: The manuscript attempts to be exhaustively self-contained, resulting in extreme density. Key insights are buried in parenthetical annotations. The reader must track ~30 symbols, 10 tables, and extensive cross-references.
   - *Why it matters*: The paper's practical value (Algorithm 1, Table X) is undermined if practitioners cannot extract the design procedure without extensive study.
   - *Remedy*: (a) Create a 1-page "Quick Start" summary (possibly as an appendix) with Algorithm 1, Table X, and the rate ladder. (b) Move detailed derivations (GE Markov chain, thundering herd analysis, J2 re-association) to appendices. (c) Reduce inline caveats by consolidating assumptions in a single "Modeling Assumptions and Limitations" subsection. Target 20-25% reduction in main text.

4. **The generalized $\gamma$ expression (Eq. 7) needs clearer practitioner guidance on applicability boundaries.**
   - *Issue*: Eq. 7 is presented as useful for practitioners, but its applicability conditions (single-packet-per-slot, cold-start acquisition, CCSDS framing, FEC over entire frame) are restrictive. The sensitivity expression (Eq. 8) is helpful but the paper does not discuss how $\gamma$ changes under multi-packet aggregation, frequency hopping, or spread-spectrum PHY layers common in modern CubeSat radios.
   - *Why it matters*: Practitioners using non-CCSDS radios (e.g., LoRa-based ISL, UHF COTS) cannot directly apply Eq. 7 without understanding which terms to modify.
   - *Remedy*: Add a brief subsection or table showing $\gamma$ under 3-4 alternative PHY configurations (CLTU is mentioned in passing—expand). Provide explicit guidance: "For [PHY type], modify Eq. 7 as follows: ..."

5. **The spatial reuse analysis ($R = 7$) is insufficiently developed for the claims it supports.**
   - *Issue*: The fleet-level feasibility claim ($G = 1$, non-binding) depends entirely on $R = 7$, which is acknowledged as a "provisional placeholder pending RF simulation." The hexagonal geometry assumption breaks down for orbital shells, especially at polar convergence zones.
   - *Why it matters*: If $R$ must increase to 10+ due to orbital geometry, $F$ requirements change, potentially making the fleet-level claim binding for large $N$.
   - *Remedy*: Either (a) perform a basic STK-level analysis for one representative Walker constellation to validate $R = 7$, or (b) present results parameterically across $R \in [3, 12]$ showing where fleet-level scheduling becomes binding, or (c) explicitly remove fleet-level claims and restrict all results to per-cluster only.

---

## Minor Issues

1. **Inconsistent model labeling**: "Model~C (CCSDS;CCSDS-grounded, Table~X)" appears with varying parenthetical content throughout. Standardize to "Model C" after first definition.

2. **Table I notation**: $\alpha_{RX}$ is listed as a "computed output" but appears alongside free parameters without visual distinction. Use a separate section or formatting (e.g., italics) for derived quantities.

3. **Eq. 2 ($M_{total}$)**: The third term assumes uniform fan-out ($k_r$ clusters per region), but the text says $k_r = \lceil N/(k_c \cdot n_r) \rceil$—this is derived, not assumed. Clarify.

4. **"Thundering herd" analysis** (§III-B.2): The Slotted ALOHA/BEB analysis is interesting but tangential. The conclusion (election takes ~160s, <1/yr) could be stated in one sentence with the derivation in an appendix.

5. **Bibliography**: References [23] (Huang) and [24] (Li) appear uncited in the text. Reference [15] (DoD Replicator) is non-archival and tangential—consider removing.

6. **Eq. 3 ($\eta_{consensus}$)**: The stability limit $f_{decision,max} \approx 24$ should show the derivation or at least the inequality from which it is obtained.

7. **Table IV (Simulation Parameters)**: The collision avoidance rate ($10^{-4}$/node/s) is described as a "conservative upper bound" but is 300× higher than ESA data. "Stress-test parameter" would be more accurate than "conservative."

8. **Section IV-B**: "DES: 441 s (95% CI: [438, 444] s, n = 30)" — reporting a 6-second CI on a quantity that is analytically 440 s by construction is misleading precision.

9. **Missing units**: Several equations mix bits and bytes without explicit conversion factors visible in the equation itself (e.g., Eq. 5 uses $S_{eph} \times 8$ inline).

10. **The "yearly mixture" calculation** (§IV-E) assumes independence between campaign phases—state explicitly.

---

## Overall Recommendation
**Recommendation: Major Revision**

This paper tackles a worthwhile problem—parametric sizing for hierarchical coordination in large space swarms—and develops a logically sound two-test feasibility framework with useful practitioner tools (Algorithm 1, lookup tables, sensitivity expressions). The campaign duty factor is a well-motivated addition that properly contextualizes the stress-case bounds. The intellectual honesty regarding validation gaps (Table VII, explicit Tier 3 absence) is commendable and unusual.

However, three fundamental issues prevent acceptance in the current form. First, the complete absence of any external or independent validation means all quantitative claims rest on internal consistency alone—insufficient for a top-tier journal. Even a minimal NS-3 comparison or DVB-RCS2 benchmarking would substantially strengthen the paper. Second, the presentation is so dense as to be counterproductive: the core contribution (a clean two-test sizing framework) is obscured by exhaustive defensive annotation, redundant cross-referencing, and tangential analyses. Third, the DES consumes significant page budget while providing negligible value beyond implementation verification, which the authors themselves acknowledge.

The path to acceptance requires: (1) at least one form of external validation, even partial; (2) substantial restructuring for clarity, targeting 20-25% reduction with key derivations moved to appendices; and (3) sharper focus on the analytical framework as the primary contribution, with the DES demoted to a verification footnote. The underlying technical work is solid and the design equations are potentially useful—the paper needs to let them shine.

---

## Constructive Suggestions
*(Ordered by impact)*

1. **Add minimal external validation**: Compare predicted $\gamma$ against DVB-RCS2 published measurements, or implement a 100-node TDMA scenario in NS-3 to validate deadline miss rates. Even partial validation of one subsystem would move the paper from "analytical exercise" to "validated design tool."

2. **Restructure for a practitioner audience**: Lead with Algorithm 1 and Table X as the main results. Move the derivation chain (GE analysis, thundering herd, J2 re-association, DES distributional analysis) to appendices. Create a 1-page design guide.

3. **Develop the $\gamma$ expression for multiple PHY types**: Show how Eq. 7 adapts to CLTU, LoRa-ISL, and COTS UHF radios. This would significantly increase the paper's practical reach.

4. **Parameterize the spatial reuse analysis**: Present fleet-level results across $R \in [3, 12]$ rather than fixing $R = 7$. This converts a limitation into a design trade.

5. **Consolidate the rate ladder narrative**: The progression from 20.2 kbps (info) → 27.1 kbps (slot expansion) → 29.9 kbps (half-duplex) → 35 kbps (recommended) is the paper's clearest result. Make it the central narrative thread rather than one of many parallel analyses.

6. **Reduce redundancy**: The 35 kbps recommendation, $\gamma$ values, and stress-case contextualization each appear 5-8 times. State once definitively, then cross-reference.

7. **Sharpen the GE framing**: Either commit to the GE model as a design tool (with explicit guidance on parameter selection from mission-specific measurements) or reduce it to a sensitivity appendix. The current treatment is too detailed for a "what-if" tool but too unvalidated for a primary result.