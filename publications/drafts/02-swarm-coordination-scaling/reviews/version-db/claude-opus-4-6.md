---
paper: "02-swarm-coordination-scaling"
version: "db"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-03-05"
recommendation: "Unknown"
---



# Peer Review: Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms (Version DB)

---

## 1. Significance & Novelty
**Rating: 3 (Adequate)**

The paper addresses a genuine gap: closed-form parametric sizing for hierarchical coordination of large autonomous spacecraft swarms at the 10³–10⁵ scale with byte-level traffic accounting. The two-test feasibility framework (byte budget + TDMA airtime) is a useful conceptual contribution, and the campaign duty factor parameterization is a sensible engineering abstraction. However, the novelty is tempered by several factors: (1) the core equations are relatively straightforward capacity calculations (information rate / slot efficiency / half-duplex fraction); (2) the hierarchical architecture itself is well-established (LEACH variants, standard tree topologies); (3) the absence of any external validation means the paper's contribution is essentially a parameterized design spreadsheet with analytical self-consistency checks. The work is more of a systems engineering sizing exercise than a fundamental advance in distributed systems or communication theory. The generalized γ expression (Eq. 8) is genuinely useful for practitioners but is not technically novel—it is a standard slot-time decomposition.

## 2. Methodological Soundness
**Rating: 3 (Adequate)**

The analytical framework is internally consistent and the three-layer decomposition (baseline telemetry / architecture-specific / workload-dependent) is clean. The campaign duty factor *d* is a welcome addition that substantially improves workload realism over a continuous-duty assumption. The γ unification via CCSDS Proximity-1 framing (replacing the earlier 0.85) is well-executed and consistently applied throughout—I verified that γ₃₀ = 0.745 appears in all decision-relevant tables and figures.

However, several methodological concerns remain:

- The DES verification is largely tautological. The paper acknowledges this (Tier 1, <0.1% agreement "confirms implementation correctness, not model validity"), but then the DES occupies substantial manuscript real estate. The claimed "sole non-tautological contribution" of distributional tail analysis (Fig. 4) is modest: it provides buffer sizing multipliers (M = 1.30) conditional on a specific ON/OFF Markov campaign model that is itself unvalidated.

- The GE channel model parameters (p_G = 0.01, p_B = 0.90, p_GB = 0.05, p_BG = 0.50) are acknowledged as illustrative, but the paper derives specific numerical conclusions from them (27% intra-cycle recovery, P95 = 4 cycles) that are presented with a precision that belies the complete absence of ISL channel measurements. The "what-if design tool" framing is appropriate but inconsistently maintained—some passages read as findings rather than conditional results.

- The slot-level simulator and the packet-level γ derivation share the same equations as the analytical model. The claim map (Table 9) is commendably honest about this, but it raises the question of what independent verification actually exists.

## 3. Validity & Logic
**Rating: 3 (Adequate)**

The internal logic is generally sound, and the paper is careful about distinguishing information-rate from PHY-rate, and about the role of α_RX as a derived quantity rather than a free parameter. The stress-case η_S ≈ 46% is now properly contextualized as a continuous-duty upper bound occurring <1% of operational time—a significant improvement that addresses prior workload realism concerns.

Several logical issues remain:

1. **The 1 kbps budget derivation is circular.** The link budget (Table IV) derives >200 kbps aggregate capacity, then allocates 1 kbps/node with "~50% margin." But the 50% margin claim depends on the overhead analysis, which depends on the 1 kbps allocation. The paper should acknowledge this circularity explicitly and show that the system is self-consistent (i.e., that the overhead at 1 kbps doesn't consume so much capacity that the 50% margin claim is violated).

2. **The coordinator failure transient analysis** mixes optical ISL (3–5s) and RF-backup (~160s) scenarios but the RF-backup scenario involves Slotted ALOHA with BEB on UHF, which is a completely different MAC from the TDMA framework analyzed throughout. The thundering-herd footnote is interesting but the analysis assumes independence and specific BEB parameters without justification.

3. **Spatial reuse R = 3** is assumed throughout for fleet-level claims but justified only by a back-of-envelope C/I calculation with a single interferer. The paper acknowledges this limitation but still uses R = 3 in Eq. 5 for fleet-level conclusions.

4. **The ARQ × TDMA coupling finding** (52.7% deadline misses at 24 kbps Model S with M_r = 1) is presented as the "sole emergent finding" from the slot-sim, but it is predictable from the margin analysis: at 24 kbps Model S, margin = 614 ms; adding one retransmission slot per node (99 × ~93 ms ≈ 9,207 ms additional) obviously exceeds T_c. The finding is confirmatory, not emergent.

## 4. Clarity & Structure
**Rating: 4 (Good)**

The paper is well-organized with a clear roadmap. The notation table (Table I) is comprehensive. The two-test feasibility framework box is helpful. The rate ladder (Table V) is an excellent practitioner-oriented summary. Algorithm 1 provides an actionable synthesis.

However, the paper is excessively long and repetitive for its technical content. The same γ values, the same 20.2 kbps information rate, and the same 730 ms margin appear dozens of times. Many footnotes contain substantive technical content that should either be in the main text or removed. The paper would benefit from a 25–30% reduction in length, primarily by:
- Consolidating the multiple tables that present the same information in different formats
- Reducing the defensive/qualifying language (every result is hedged 3–4 times)
- Moving the Model S analysis to an appendix (since it is explicitly "not for recommendations")

The slot-timing model declaration at the top of Section I is helpful but unusual for IEEE TAES formatting.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**

The paper is exemplary in its transparency: code/data availability with tagged repository, explicit AI disclosure, honest claim mapping by evidence tier, and repeated acknowledgment that no external validation exists. The V&V tier framework (IEEE 1012) is appropriately applied. The distinction between "standards-based parameter estimate" and "measurement" for γ is carefully maintained.

## 6. Scope & Referencing
**Rating: 3 (Adequate)**

The reference list is broad but has notable gaps:
- No citation of actual TDMA scheduling literature for satellite systems (e.g., Pratt & Bostian, Maral & Bousquet for satellite communications fundamentals)
- Network calculus is cited but not applied; the deterministic worst-case bounds it provides would strengthen the feasibility framework
- No reference to existing ISL link budget analyses (e.g., from Starlink, Telesat, or academic ISL studies)
- The DVB-RCS2 comparison is mentioned but not developed—this is the closest operational analog and deserves more attention
- Missing references to CCSDS AOS (Advanced Orbiting Systems) for space TDMA

The paper's scope is appropriate for IEEE TAES but sits at the boundary between a systems engineering trade study and a research contribution. The absence of any experimental or simulation-based validation against an independent tool (NS-3, STK, MATLAB Satellite Communications Toolbox) weakens the case for a top-tier journal.

---

## Major Issues

1. **Lack of independent validation undermines all quantitative claims.**
   - *Issue:* All three verification tools (analytical, DES, slot-sim) share the same equations. The packet-level γ derivation is a parameter calculation, not validation. The claim map (Table 9) shows no Tier 3 entries.
   - *Why it matters:* Without at least one independent cross-check (NS-3 MAC simulation, hardware-in-the-loop γ measurement, or comparison with an existing satellite TDMA system's published performance), the paper's quantitative recommendations (35 kbps, 730 ms margin, etc.) cannot be assessed for real-world applicability.
   - *Remedy:* At minimum, validate the TDMA scheduling against NS-3 or MATLAB's satellite communications toolbox for a single configuration (k_c = 100, 35 kbps). Alternatively, compare predicted γ against published DVB-RCS2 terminal measurements to establish that the CCSDS-derived γ is in the right ballpark. If neither is feasible pre-publication, the paper should be reframed as a "design methodology" paper rather than one making specific PHY-rate recommendations.

2. **The DES contribution does not justify its manuscript footprint.**
   - *Issue:* The DES confirms its own equations to <0.1%. Its distributional contribution (buffer sizing multipliers) is conditional on an unvalidated campaign model. Sections III-A, IV-F, and portions of IV-A–IV-E could be substantially compressed.
   - *Why it matters:* The DES analysis creates an impression of validation depth that doesn't exist. Readers may mistake Tier 1 verification for model validation.
   - *Remedy:* Reduce DES coverage to ~1 page: state that DES confirms analytical means (one sentence), present the buffer CDF (Fig. 4) as the sole DES-specific result, and move implementation details to supplementary material.

3. **The paper conflates design-space exploration with validated design recommendations.**
   - *Issue:* Despite repeated caveats, the paper makes specific recommendations ("35 kbps recommended," "30 kbps minimum viable") that imply a level of validated engineering judgment. The abstract states these are "preliminary design estimates lacking external validation," but the body text often reads as prescriptive.
   - *Why it matters:* A practitioner reading Table V (Rate Ladder) or Table XII (γ-conditional lookup) might use these values directly without appreciating that they rest on assumed (not measured) timing parameters.
   - *Remedy:* Reframe all "recommendations" as "baseline design points conditional on assumed parameters" and add explicit sensitivity ranges (already partially done in Table XIV but not consistently propagated to recommendations).

4. **The three-layer feasibility framework conflates independent and dependent tests.**
   - *Issue:* Test A (byte budget) and Test B (TDMA airtime) are presented as independent, but they are coupled through the coordinator ingress rate: if Test A shows η_total > 50%, the TDMA schedule must accommodate the corresponding traffic, affecting Test B. The paper partially acknowledges this ("Parameter dependency" paragraph) but doesn't formalize the coupling.
   - *Why it matters:* Under high duty factors (d > 0.5), the byte budget and airtime constraints interact nonlinearly through the egress schedule. The current framework may underestimate the required PHY rate under sustained high-d operation.
   - *Remedy:* Add a brief analysis showing that for the recommended operating range (d ≤ 0.10), the tests are effectively decoupled (ingress-dominated), and identify the d threshold above which coupling becomes significant.

5. **Static cluster membership assumption is inadequately justified for the claimed scale.**
   - *Issue:* The paper assumes static cluster membership for 1-year simulations, justified by J2 analysis showing <0.3% overhead for cross-plane re-association. But at 10⁵ nodes in heterogeneous orbits, cluster topology changes are frequent and the re-association overhead analysis (14.8 kB, 33s AoI transient) is for a single event—the aggregate effect of many concurrent re-associations is not analyzed.
   - *Why it matters:* Dynamic topology is a defining challenge of large-scale space swarms. Dismissing it as <0.5% overhead without analyzing concurrent re-association storms undermines the paper's scaling claims.
   - *Remedy:* Either restrict claims to co-orbital formations (where static membership is exact) or provide a fleet-level analysis of concurrent re-association load under realistic orbital mechanics.

## Minor Issues

1. **Table I notation:** α_RX is described as a "computed output" but its example value (0.908) is given without the conditioning parameters being immediately obvious. Add "(at 30 kbps, M_r = 0, k_c = 100)" to the example.

2. **Eq. 2 (hierarchical messages):** The third term assumes uniform k_r across regions; state this assumption explicitly.

3. **Section III-B-2, coordinator service:** "s_proc = 5 ms/msg" is stated without justification. What processing is assumed? Integrity check of what complexity?

4. **Table III footnote (a):** The collision avoidance rate of 10⁻⁴/node/s is described as a "stress-test parameter" but is 300× the ESA-reported rate. This should be in the main text, not a footnote, given its role in overhead calculations.

5. **Section IV-A:** "Phase-staggered scheduling... DES confirms zero drops at ≥25 kbps vs. 50 kbps under random phase"—this result appears only in passing and is never tabulated or shown in a figure.

6. **Eq. 10 (η_consensus):** f_decision is decisions per cycle but the stability limit f_decision,max ≈ 24 is stated without derivation. Show the calculation.

7. **Fig. 2 (cross-cycle recovery):** The figure is referenced but not shown in the manuscript text. Ensure all figures are properly placed.

8. **Section IV-H (parameter sensitivity):** Referenced in the roadmap but no corresponding subsection header exists. The sensitivity analysis appears scattered across multiple subsections.

9. **The "thundering herd" footnote** (Section III-B-2) contains a full BEB analysis that is more detailed than some main-text results. Either promote to main text or simplify.

10. **Inconsistent use of "≈" vs. "=":** Some γ values are given as exact (0.761) and others as approximate (≈0.745). Since all are computed from Eq. 8 with specific parameters, use consistent notation.

11. **Table III:** "Handoff state size: 10–50 MB" spans a 5× range without guidance on when each end applies.

12. **Abstract:** "CCSDS Proximity-1 framing anchors γ ≈ 0.70–0.76 (rate-dependent)"—the range should specify which rates correspond to which γ values, as done in the body text.

13. **Reference [dyson_multimodel]:** A self-citation to a non-peer-reviewed preprint about AI methodology is unusual for IEEE TAES. Consider removing or replacing with a more conventional reference.

---

## Overall Recommendation
**Recommendation: Major Revision**

This paper presents a well-structured parametric sizing framework for hierarchical coordination in large autonomous space swarms. Its principal strengths are: (1) the clean two-test feasibility decomposition with explicit byte-level accounting; (2) the campaign duty factor parameterization that bridges the gap between continuous-duty stress bounds and realistic operational profiles; (3) the CCSDS-grounded γ derivation that replaces earlier ad hoc values with standards-traceable estimates; and (4) exceptional transparency in acknowledging validation limitations.

The most critical weakness is the complete absence of independent validation. All quantitative tools share the same equations, making the verification circular. The DES confirms analytical means by construction; the slot-sim confirms slot-level scheduling by construction; the packet-level γ is a parameter calculation, not a measurement. The paper is honest about this (Table 9, Section V-A), but honesty about a gap does not fill it. For IEEE TAES, at least one form of independent cross-validation is expected—whether NS-3 simulation, comparison with DVB-RCS2 measured performance, or hardware γ measurement. Without this, the paper reads as a well-documented design spreadsheet rather than a validated engineering methodology.

Secondary concerns include excessive length relative to technical content (the paper could be 30% shorter without losing substance), the DES analysis consuming disproportionate space for its marginal contribution, and the static cluster membership assumption limiting the applicability of scaling claims. The paper would benefit from tighter focus on its genuine contributions (the feasibility framework, the γ parameterization, the duty-factor model) and either addition of independent validation or explicit repositioning as a design methodology paper with worked examples.

## Constructive Suggestions
*(Ordered by impact)*

1. **Add one independent validation point.** Even a single NS-3 run at k_c = 100, 35 kbps confirming the 1,880 ms margin would transform the paper's credibility. Alternatively, obtain DVB-RCS2 published γ measurements and show consistency with the CCSDS-derived values.

2. **Compress the DES material by 50%.** The DES's value is the buffer CDF (Fig. 4) and the campaign-burstiness tail. Present these in ~1 page; move implementation details to supplementary material or the repository.

3. **Formalize the Test A / Test B coupling.** Show analytically that for d ≤ 0.10, the tests decouple (ingress-dominated regime), and identify the critical d above which joint analysis is required.

4. **Reduce overall length by 25–30%.** Consolidate redundant tables (e.g., Tables V, VI, XII, XIII all present aspects of the same rate-selection problem). Remove Model S from the main text entirely (it is explicitly not for recommendations).

5. **Strengthen the dynamic topology analysis.** Either restrict scaling claims to co-orbital formations or analyze concurrent re-association load at fleet scale.

6. **Add a "How to Use This Paper" subsection** that walks a practitioner through the complete sizing procedure for a specific non-default parameter set (e.g., k_c = 200, S_eph = 512 B, T_c = 5 s), demonstrating the generality of the framework.

7. **Tighten the GE analysis framing.** Every GE-derived number should be explicitly conditional: "Under the assumed GE parameters (Table III), which have no ISL measurement basis, ..." Currently this qualification appears in some places but not others.

8. **Consider splitting into two papers:** (a) the feasibility framework and sizing equations (shorter, tighter, methodology-focused), and (b) the DES/simulation analysis with distributional results (once external validation is available).