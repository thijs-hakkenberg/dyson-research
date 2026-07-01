---
paper: "02-swarm-coordination-scaling"
version: "cx"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-03-05"
recommendation: "Unknown"
---



# Peer Review: "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version CX)

---

## 1. Significance & Novelty
**Rating: 3 (Adequate)**

The paper addresses a genuine gap: closed-form parametric sizing for hierarchical coordination at the 10³–10⁵ node scale with byte-level traffic accounting. The two-layer feasibility framework (byte budget + TDMA airtime) and the actionable Algorithm 1 are useful contributions for preliminary mission design. However, the novelty is tempered by several factors: (a) the core equations are relatively straightforward engineering calculations (traffic accounting, slot timing) rather than deep analytical contributions; (b) the absence of any external validation means the work remains a self-consistent parametric exercise; (c) the paper's primary finding—that coordinator ingress at ~20 kbps information-rate drives the PHY rate to 30–35 kbps—is an important but narrow result. The campaign duty factor framework and the γ-conditional lookup table add practical value, but the contribution would be substantially stronger with at least one external validation anchor.

## 2. Methodological Soundness
**Rating: 3 (Adequate)**

The three-layer feasibility framework (byte budget, MAC efficiency, TDMA airtime) is logically structured, and the paper is commendably transparent about what each tool can and cannot demonstrate. The V&V tier structure (Section III-A) is well-articulated. However:

- The DES is acknowledged to reproduce its own equations (Tier 1 only), which limits its evidentiary value. The distributional tail analysis (Fig. 4) is the sole non-tautological DES contribution, and it depends entirely on the assumed ON/OFF Markov campaign process.
- The slot-level simulator and the packet-level γ derivation share the same underlying equations, making cross-verification circular. The ARQ×TDMA coupling finding (52.7% misses) is genuinely emergent from the slot simulator, but it is demonstrated only under Model S (which is explicitly not used for design), weakening its practical significance.
- The GE channel model is appropriately framed as a "what-if design tool," but the default parameters (p_BG = 0.50, p_B = 0.90) are not anchored to any ISL measurement, and the per-cycle coherence assumption is a strong structural choice that predetermines the 27% intra-cycle recovery result.

## 3. Validity & Logic
**Rating: 4 (Good)**

The internal logic is generally sound and self-consistent. The paper has clearly evolved through multiple revision cycles, and many potential logical pitfalls are explicitly addressed:

- The campaign duty factor (d) adequately addresses workload realism: the stress-case η_S ≈ 46% is properly contextualized as episodic (<1% of operational time), with the time-weighted annual average of 5.6% being the operationally relevant figure.
- The gamma unification is consistently applied: γ is always computed from Eq. 12 (time-domain), with rate-dependent values (γ₂₄ = 0.761, γ₃₀ = 0.745, γ₃₅ = 0.732) used throughout. The earlier 0.85 value has been replaced. Model S (0.949) is clearly labeled as a comparison bound only.
- The stress-case is properly framed as a continuous-duty upper bound.
- The parameter dependency map (beginning of Section IV) is a helpful addition that clarifies which parameters affect which results.

One logical concern: the paper states that the 1 kbps per-node budget provides "~50% margin for retransmissions" (Section III-E), but the stress-case η_total ≈ 67% already consumes most of this budget. The margin claim applies only to nominal operations.

## 4. Clarity & Structure
**Rating: 3 (Adequate)**

The paper is thorough but suffers from significant organizational challenges:

- At ~12,000 words (estimated), the manuscript is extremely dense. The repeated clarifications ("Do not apply the heuristic AND Test B independently"), defensive footnotes, and cross-references to previous version concerns create a palimpsest quality that impedes readability.
- The two-model framework (Model S vs. Model C) is well-motivated but adds cognitive load. Despite clear labeling, the reader must constantly track which model applies.
- Table density is high (11 tables), and several contain extensive footnotes that carry substantive content (e.g., Table III footnotes contain message size justifications that arguably belong in the main text).
- The roadmap at the beginning of Section IV is helpful, but the section itself spans topics from coordinator sizing through topology comparison, making it feel like multiple papers compressed into one.
- Algorithm 1 is a genuine strength—clear, actionable, and well-annotated.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**

The paper is exemplary in transparency: data availability with tagged repository, explicit AI disclosure, clear acknowledgment of validation gaps, and honest characterization of evidence tiers. The claim map (Table IX) is a model of scientific honesty. The "no external validation exists" statement is repeated appropriately.

## 6. Scope & Referencing
**Rating: 3 (Adequate)**

The reference list (55 items) covers the relevant domains but has gaps:

- No references to actual ISL implementations (e.g., Starlink laser ISL performance data, EDRS/SpaceDataHighway operational experience, or JAXA's LUCAS).
- The DVB-RCS2 comparison for γ uncertainty bounding is creative but acknowledged as non-ISL; actual satellite TDMA implementations (e.g., MF-TDMA in DVB-S2/RCS systems) would strengthen the anchoring.
- Network calculus (Le Boudec) is cited but not applied; a deterministic worst-case bound would complement the mean-value approach.
- Missing references to recent work on distributed satellite autonomy beyond NASA DSA (e.g., ESA's OPS-SAT results, or the growing literature on onboard AI for constellation management).
- Several references are non-archival (Amazon Kuiper overview, DARPA program pages, DOD fact sheets), which is acceptable for context but weakens the scholarly foundation.

---

## Major Issues

**1. Circular validation architecture limits the paper's contribution claims.**
- *Issue:* All three verification tools (analytical equations, DES, slot-sim) share the same underlying model. The packet-level γ derivation (Section IV-J) is a standards-based parameter estimate, not independent validation. The paper acknowledges this (Table IX, Section V-A), but the abstract and conclusion still frame the work as providing "design equations" without adequately qualifying that these equations have zero external validation.
- *Why it matters:* A reader might use Algorithm 1 for actual mission sizing, trusting that the framework has been validated to some degree. The paper's own admission that "predictive accuracy for real ISL channels is unknown" should be more prominent in the conclusion.
- *Remedy:* (a) Add a prominent caveat box in the conclusion (not just Section V-A) stating that all results are unvalidated parametric estimates. (b) Quantify the sensitivity of key recommendations to the most uncertain parameters (γ, T_acq, GE parameters) in a single consolidated sensitivity table. (c) Consider whether the paper would be better positioned as a "design methodology" paper rather than a "results" paper.

**2. The DES provides minimal incremental value beyond confirming its own equations.**
- *Issue:* The DES mean-value agreement (<0.1%) is acknowledged as tautological. The distributional tail analysis (Fig. 4, buffer sizing) is the sole non-tautological contribution, but it depends entirely on the assumed ON/OFF Markov campaign model, which itself is unvalidated. The buffer sizing rule (M = 1.30 at d = 0.10) is labeled "not model-robust."
- *Why it matters:* Approximately 2 pages of the manuscript are devoted to DES description and results that add little beyond what the closed-form equations provide. This dilutes the paper's focus.
- *Remedy:* Either (a) substantially reduce DES coverage to a single paragraph acknowledging code verification and the buffer sizing caveat, or (b) use the DES to explore scenarios that the closed-form equations *cannot* capture (e.g., correlated node failures, dynamic cluster reassignment, priority queueing interactions). Option (b) would add genuine value.

**3. The three-layer feasibility framework conflates two genuinely independent tests with a unit conversion.**
- *Issue:* The paper repeatedly warns readers not to apply the heuristic (Eq. 14) and Test B independently, because they are "algebraically connected." This is correct, but it raises the question of why the heuristic is presented at all. The "three-layer" framing (byte budget, MAC efficiency, TDMA airtime) in the abstract and introduction is misleading—there are really two tests (A and B), with MAC efficiency being a parameter within Test B.
- *Why it matters:* The repeated warnings suggest that earlier reviewers (or the authors themselves) found the framework confusing. Simplifying the presentation would improve clarity and reduce the need for defensive annotations.
- *Remedy:* Present the framework as strictly two tests (A and B) throughout, with γ as a parameter in Test B. Remove or demote the "MAC efficiency" as a separate layer. The heuristic can remain as a quick-check formula but should not be elevated to a "layer."

**4. Fleet-level scaling claims are insufficiently supported.**
- *Issue:* The paper's title and abstract imply applicability to "large autonomous space swarms," but all quantitative results are per-cluster (k_c = 50–500). Fleet-level extension relies on Eq. 8 (spatial reuse), which is described as an "order-of-magnitude plausibility argument." The assumed R = 3 spatial reuse factor is based on free-space path loss at 500 km separation with 6 dBi antennas—a very rough estimate that ignores sidelobe coupling, near-far effects, and dynamic geometry.
- *Why it matters:* The gap between per-cluster sizing (well-developed) and fleet-level feasibility (hand-waving) is the paper's most significant limitation for the target audience of IEEE T-AES.
- *Remedy:* Either (a) restrict the scope explicitly to per-cluster sizing (adjusting title and abstract), or (b) provide a more rigorous fleet-level analysis, even if simplified (e.g., interference calculations for a Walker constellation geometry with realistic antenna patterns).

**5. The GE channel model's structural assumptions predetermine key findings.**
- *Issue:* The per-cycle coherence assumption (GE transitions once per T_c) makes intra-cycle ARQ structurally ineffective by construction when τ_c ≥ T_c. The paper acknowledges this ("not an emergent finding"), but the 27% intra-cycle recovery figure is still presented as a result rather than a modeling assumption.
- *Why it matters:* The recommendation of 35 kbps (vs. 30 kbps) is driven by ARQ margin requirements under this specific GE parameterization. If the coherence assumption is wrong (e.g., if ISL fading is faster than T_c), the 30 kbps minimum suffices.
- *Remedy:* (a) Present the dual coherence-regime recommendation more prominently (it is currently buried in Section IV-C). (b) Make the 35 kbps recommendation explicitly conditional on the slow-mixing assumption. (c) Consider presenting 30 kbps as the primary recommendation with 35 kbps as the conservative option for slow-mixing channels, rather than the reverse.

---

## Minor Issues

1. **Abstract length:** At ~200 words, the abstract is dense but within IEEE limits. However, it contains too many parenthetical qualifications that reduce readability. Consider streamlining.

2. **Table I (Notation):** The entry for γ includes specific numeric values (0.761, 0.745, 0.732) that are results, not notation. Move these to the results section.

3. **Eq. 1 (γ_derived = 0.949):** This Model S value appears before Model C is introduced, potentially confusing readers who encounter it first. Consider reordering to present Model C first.

4. **Section III-B.2 (Hierarchical Topology):** The coordinator summary breakdown (48B + 48B + 13B + 32B + 371B = 512B) allocates 371B to "metadata/CRC," which seems disproportionate. Justify or acknowledge this as padding.

5. **Table V (Superframe):** The footnote about ACK mini-slots being "transmitted within the jitter sub-slot at a deterministic offset" is a non-trivial protocol design choice that deserves main-text discussion, not a footnote.

6. **Fig. 2 (Cross-cycle recovery):** The figure caption references "DES bars (30 MC replications, N = 10,000, k_c = 100)" but the figure is not included in the review. Ensure the figure clearly distinguishes analytical vs. DES results.

7. **Section IV-A (Coordinator Capacity Sizing):** The β parameterization (C_coord = β · k_c) is introduced but results are deferred to "Section IV-A" (self-referential). Clarify where these results appear.

8. **Eq. 6 (η_consensus):** The stability limit f_decision,max ≈ 24 is stated without derivation. Show the calculation or provide a reference.

9. **Table VIII (Duty Mapping):** The collision avoidance row shows d = 1.0 "during event" with a footnote. This is potentially misleading—CA events are extremely rare (d_CA ≈ 0.00002 annually). Consider separating the "during event" and "background" values into separate rows.

10. **Section V-C (Design Equations):** The T_framing expression includes R_FEC in the denominator (framing bits are FEC-encoded), but this is inconsistent with Table IV where framing bits (104) are listed separately from FEC parity (308). Clarify whether the 308-bit FEC parity covers only the payload or payload + framing.

11. **Reference [47] (dyson_multimodel):** This is a self-cited, non-peer-reviewed preprint. Consider removing or replacing with a more standard AI methodology reference.

12. **Typographical:** "Eq.~\ref{eq:gamma_time}" appears ~15 times; consider defining a shorthand after first use.

13. **The "thundering herd" footnote (Section III-B.2):** This contains a substantive analysis (BEB convergence, election traffic calculation) that is too important for a footnote. Promote to main text or a dedicated subsection.

14. **Missing figure:** Fig. 1 (architecture diagram) is referenced but the PDF is not included. Ensure it clearly shows the four-level hierarchy with fan-out ratios.

---

## Overall Recommendation
**Recommendation: Major Revision**

This manuscript represents a substantial engineering effort to provide closed-form sizing equations for hierarchical coordination in large space swarms. The two-test feasibility framework is logically sound, the campaign duty factor elegantly addresses workload realism, and the CCSDS-grounded γ parameterization provides a credible (if unvalidated) anchor for slot efficiency. Algorithm 1 is a genuinely useful practitioner tool, and the paper's transparency about validation gaps (Table IX, V&V tiers) sets a commendable standard for intellectual honesty.

However, the paper faces three fundamental challenges that prevent acceptance in its current form. First, the circular validation architecture—where all tools share the same equations—means the paper's quantitative claims rest entirely on assumed parameters (γ, GE model, message sizes, T_acq) with no external anchor. The packet-level γ derivation (Section IV-J) is a parameter estimate, not validation, and the DES confirms only its own implementation. Second, the manuscript's length and defensive annotation style (clearly accumulated over multiple revision cycles) impede readability; the paper would benefit from a 20–30% reduction in length, focusing on the core two-test framework and eliminating redundant clarifications. Third, the gap between per-cluster results (well-developed) and fleet-level claims (order-of-magnitude) is too large for the paper's ambitious title and scope.

The most impactful revision would be to (a) tighten the scope to per-cluster sizing, (b) consolidate the presentation around the two-test framework and Algorithm 1, (c) add at least one external validation point (even a comparison against published DVB-RCS2 TDMA performance data or NS-3 simulation of a simplified scenario), and (d) reduce length by 25%. The γ generalization (Eq. 12) and the γ-conditional lookup table (Table XI) are the paper's most practically useful outputs and should be given greater prominence.

---

## Constructive Suggestions
*(Ordered by impact)*

1. **Add one external validation anchor.** Even a simplified NS-3 simulation of a single cluster's TDMA schedule (100 nodes, CCSDS framing, GE channel) would transform the paper from a parametric exercise into a validated design tool. This is the single highest-impact improvement.

2. **Reduce manuscript length by 25%.** Consolidate the Model S/Model C discussion (Model S can be reduced to a single paragraph). Remove redundant feasibility warnings. Merge Tables V and VI. Shorten Section III (simulation framework) by moving parameter justifications to an appendix.

3. **Restructure as a two-test framework throughout.** Eliminate "three-layer" language. Present γ as a parameter within Test B, not a separate layer. This removes the need for repeated "do not double-count" warnings.

4. **Promote the γ-conditional lookup table (Table XI) to a more prominent position.** This is the paper's most actionable output for practitioners. Consider making it the centerpiece of the design equations section.

5. **Consolidate sensitivity analysis.** Create a single tornado diagram showing how the 35 kbps recommendation shifts with ±20% changes in each key parameter (γ, T_acq, T_guard, k_c, S_eph). This would be more useful than the current scattered sensitivity discussions.

6. **Strengthen fleet-level analysis or restrict scope.** If fleet-level claims are retained, provide interference calculations for at least one specific orbital geometry (e.g., Walker 53°/550km) with realistic antenna patterns.

7. **Reframe the DES contribution.** Either reduce DES coverage to a verification paragraph, or use it to explore genuinely new scenarios (correlated failures, dynamic reassignment, priority queueing) that closed-form equations cannot capture.

8. **Make the dual coherence-regime recommendation the primary design output.** The slow-mixing vs. fast-fading distinction is the paper's most nuanced contribution to ARQ design; elevate it from a subsection to a key finding.