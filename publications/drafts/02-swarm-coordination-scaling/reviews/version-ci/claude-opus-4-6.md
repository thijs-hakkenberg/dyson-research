---
paper: "02-swarm-coordination-scaling"
version: "ci"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-03-01"
recommendation: "Major Revision"
---



# Peer Review: "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms"

## 1. Significance & Novelty
**Rating: 3 (Adequate)**

The paper addresses a genuine gap: closed-form sizing equations for hierarchical coordination at the 10³–10⁵ node scale with byte-level traffic accounting. The two-layer feasibility framework (byte budget + TDMA airtime) and the decomposition into topology-dependent (η₀) and workload-dependent (η_cmd) overhead are useful conceptual contributions. However, the novelty is tempered by several factors: (1) the core analytical results are relatively straightforward traffic accounting rather than deep systems-theoretic contributions; (2) the framework is validated only against itself (Tier 1–2), with no external validation; (3) the practical applicability is narrow—the authors themselves acknowledge that the TDMA analysis is binding only for the 1 kbps RF-backup channel (<1% of operational lifetime). The generalized γ expression (Eq. 17) and Algorithm 1 are useful practitioner tools, but the overall contribution feels more like a well-executed engineering sizing study than a fundamental advance.

## 2. Methodological Soundness
**Rating: 3 (Adequate)**

The analytical framework is internally consistent and the three-layer tool hierarchy (analytical/DES/slot-sim + packet-level) is well-structured. Several methodological concerns remain:

- The DES operates at message-layer granularity with cycle-aggregated updates, which by construction must agree with the closed-form equations. The <0.1% agreement is a verification of implementation correctness, not validation. The authors acknowledge this (Tier 1), which is appreciated.
- The packet-level "validation" (Section IV-J) derives γ from CCSDS framing parameters and feeds it back into the same equations. This is parameter anchoring, not independent validation. It does add value by grounding γ in standards rather than assumption, but the term "validation" should be used cautiously.
- The slot-level simulator provides genuine additional insight (ARQ×TDMA coupling at 24 kbps), representing the strongest cross-model contribution.
- The Monte Carlo configuration (30 replications) is adequate for mean estimation but marginal for tail statistics (P99 AoI). The bootstrap CI methodology is appropriate but the underlying sample size for extreme quantiles deserves more scrutiny.

## 3. Validity & Logic
**Rating: 4 (Good)**

The logical structure is generally sound. The campaign duty factor (d) adequately addresses the earlier concern about workload realism—the stress-case (η_S ≈ 46%) is now clearly contextualized as a continuous-duty upper bound (d = 1) that applies <1% of operational time, with representative campaign scenarios anchored in ESA/Starlink operational data. The γ unification at 0.760 (replacing the earlier 0.85) appears consistently applied throughout, with Model S vs. Model C clearly distinguished. The three-layer feasibility framework is logically coherent.

Minor logical concerns: (1) The claim that command overhead is "topology-invariant" is carefully qualified but could still mislead—it holds only under centralized broadcast semantics, and the distributed consensus analysis (Eq. 10) shows dramatically different scaling. (2) The GE channel model is acknowledged as illustrative, but some conclusions (e.g., "intra-cycle ARQ is structurally ineffective") are stated more strongly than the evidence supports, given the absence of ISL-specific channel measurements.

## 4. Clarity & Structure
**Rating: 3 (Adequate)**

The paper is comprehensive but suffers from excessive length and density. At approximately 12,000+ words with 15+ tables and 10+ figures, it significantly exceeds typical IEEE TAES length. The notation table is helpful, but the sheer volume of cross-references, footnotes, and caveats makes the paper difficult to follow linearly. Several specific issues:

- The distinction between Model S and Model C, while important, is introduced in the preamble, re-explained in Section IV-A, and referenced throughout—creating redundancy.
- The workload profiles section (IV-E) mixes definition, sensitivity analysis, and operational anchoring in a way that could be more cleanly separated.
- Some figures (e.g., Fig. 1 architecture diagram) are referenced but their content is not sufficiently described for a reader without access to the PDF.
- The paper would benefit from a concise "key results" summary table early in Section IV.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**

Exemplary transparency: open-source code with tagged release, full parameter tables, AI disclosure with specific model versions and scope of use, clear delineation of what AI did and did not contribute. The evidence tier framework (adapted from IEEE 1012) is a commendable practice for honestly communicating the strength of different claims. The explicit identification of the NS-3 validation gap (Tier 3) is refreshingly honest.

## 6. Scope & Referencing
**Rating: 4 (Good)**

The literature coverage is broad and appropriate, spanning constellation management, swarm robotics, distributed systems, queueing theory, CCSDS standards, and AoI theory. The DVB-RCS2 reference is a welcome addition for TDMA context. A few gaps: (1) no reference to recent work on LEO constellation autonomous collision avoidance (e.g., Merz et al., or the ESA CREAM system); (2) the network calculus mention (Le Boudec) is superficial—either develop the comparison or remove it; (3) no discussion of how this framework relates to the emerging CCSDS Spacecraft Onboard Interface Services (SOIS) standards for intra-spacecraft and proximity communication.

---

## Major Issues

1. **Circular validation architecture.** The DES, analytical model, and slot-level simulator all implement the same underlying equations at different granularities. The <0.1% DES-analytical agreement is a code verification, not model validation. The packet-level simulator derives γ from standards parameters but feeds it into the same framework. The only genuinely independent finding is the ARQ×TDMA coupling from the slot-level simulator. The paper needs to more clearly distinguish verification (internal consistency) from validation (comparison against independent data or models). Table VIII (Claim Map) partially addresses this but the text still occasionally conflates the two.
   - **Why it matters:** Readers may overestimate the confidence level of the results.
   - **Remedy:** Restructure Section V-A to explicitly state: "All Tier 1 and Tier 2 results are internal consistency checks and parameter anchoring, respectively. No external validation exists. The framework's predictive accuracy for real ISL channels is unknown." Consider adding a comparison against published DVB-RCS2 or Iridium NEXT performance data, even if approximate.

2. **Narrow binding regime undermines practical significance.** The authors acknowledge that the TDMA schedulability analysis is binding only for the 1 kbps RF-backup channel (<1% of operational lifetime), and that at ≥10 kbps "both feasibility layers are non-binding." This means the paper's most technically sophisticated contribution (Layer 2, TDMA airtime analysis) applies to a corner case. The byte-budget analysis (Layer 1) is straightforward traffic accounting.
   - **Why it matters:** The contribution may not justify the paper's length and complexity for a top-tier journal.
   - **Remedy:** Either (a) strengthen the argument for why the RF-backup sizing is design-driving (e.g., quantify the safety consequences of getting it wrong, with reference to specific failure scenarios), or (b) extend the analysis to regimes where it is more broadly applicable (e.g., deep-space swarms where low data rates are the norm, not the exception).

3. **GE channel model lacks empirical grounding for ISL.** The authors repeatedly acknowledge that "no ISL-specific GE measurement data are available in the open literature" and that the Lutz et al. framework was developed for land-mobile satellite channels. Yet the paper draws strong conclusions ("intra-cycle ARQ is structurally ineffective") from this unvalidated model. The geometric justification for structural shadowing τ_c (Section IV-C) is reasonable but speculative.
   - **Why it matters:** The ARQ infeasibility conclusion is one of the paper's key findings, but it rests on assumed channel parameters.
   - **Remedy:** (a) Soften the ARQ infeasibility claim to "under the assumed GE parameterization" throughout; (b) provide a clearer decision tree: "if your measured τ_c < X, use intra-cycle ARQ; if τ_c > X, use inter-cycle recovery"; (c) the sensitivity sweep (Fig. 7b) partially addresses this but should be promoted as the primary result rather than the point estimate.

4. **Missing queueing analysis for coordinator ingress under realistic traffic.** The coordinator is modeled as a D[k_c]/D/1 queue with deterministic service, yielding trivial results (batch latency ≤ 500 ms). Under stochastic campaigns with GE losses, the actual queueing behavior is more complex. The DES provides distributional analysis (Fig. 8) but the analytical framework lacks a proper stochastic queueing model for the coordinator under compound arrivals (campaign ON/OFF × GE state).
   - **Why it matters:** Buffer sizing and drop probability under realistic conditions are critical for system design.
   - **Remedy:** Develop a Markov-modulated arrival model (MMPP/D/1 or similar) for the coordinator queue under compound campaign + GE dynamics, and compare against DES distributions.

## Minor Issues

1. **Inconsistent γ notation.** The paper uses γ, γ_S, γ_C, γ_{24}, γ_{30}, γ_{C,24}, γ_{C,30}, and γ_total. While each is defined, the proliferation is confusing. Consider a consistent two-subscript notation (model, rate) throughout.

2. **Table II (bandwidth scaling):** The "TDMA required?" row says "Yes (γ ≥ 0.67)" at 1 kbps but the feasibility matrix (Table IX) shows different thresholds. Clarify the relationship.

3. **Eq. 6 (η_canonical):** The equation shows η = η₀ + d·η_cmd, but η_cmd itself depends on p_cmd and S_cmd (defined in Section IV-E). The canonical equation should be self-contained or explicitly reference the full expansion.

4. **Section III-B-2 (coordinator failure transient):** The compound probability calculation (6.3 × 10⁻¹² s⁻¹) assumes statistical independence, which is immediately contradicted by the common-cause failure caveat. Either quantify the common-cause contribution or remove the precise number.

5. **Fig. 3 (phase stagger):** Referenced before the TDMA frame model is fully developed. Consider reordering.

6. **Algorithm 1, Line 7:** The screening threshold (η_total/γ < 0.50) is described as "sufficient but not necessary" in the text but implemented as a hard branch in the algorithm. Clarify the operational meaning.

7. **Section IV-E (campaign scenarios):** The ESA collision avoidance rate (10/yr per spacecraft) is for a fleet of ~30 spacecraft. Scaling to 10⁵ nodes with inter-satellite conjunction risks would likely yield much higher per-node rates. This should be noted.

8. **Typo/formatting:** "Fig.~\ref{fig:ge_coherence}" in Section IV-C appears before the figure is introduced in the text flow.

9. **The sectorized mesh (Section III-B-4)** is introduced but barely analyzed. Either develop it as a meaningful comparison point or remove it.

10. **Reference [62] (dyson_multimodel)** is self-referential and "not peer-reviewed." Per IEEE policy, this should be clearly marked as a preprint/technical report.

11. **Table I notation:** The entry for γ references "§III-J" but the section numbering uses Roman numerals inconsistently with the actual section structure (IV-J).

---

## Overall Recommendation
**Recommendation: Major Revision**

This paper presents a thorough and honest engineering sizing study for hierarchical coordination in large space swarms. Its strengths are considerable: the two-layer feasibility framework is well-conceived; the decomposition of overhead into topology-dependent and workload-dependent components is clean; the campaign duty factor elegantly resolves the earlier workload realism concern; the CCSDS-grounded γ derivation is a genuine improvement over assumed values; and the transparency regarding validation gaps, AI use, and evidence tiers is exemplary.

However, several issues prevent acceptance in the current form. The most fundamental is the circular validation architecture: the paper's multiple tools verify each other but none is validated against external data or independent models. The practical significance is also narrower than the paper's length suggests—the sophisticated TDMA analysis applies only to a corner case (<1% of operational lifetime). The GE channel conclusions, while carefully caveated, rest on unvalidated parameters. The paper would benefit substantially from either external validation data (even approximate) or a clearer argument for why the RF-backup sizing case justifies this level of analysis.

The paper should be shortened by approximately 25-30%, focusing on the core contributions (feasibility framework, γ derivation, ARQ infeasibility finding) and moving secondary material (sectorized mesh, extensive sensitivity sweeps) to supplementary material. The distinction between verification and validation should be sharpened throughout. With these revisions, the paper would make a solid contribution to IEEE TAES.

## Constructive Suggestions

1. **Highest impact:** Add a comparison against any available external data—DVB-RCS2 TDMA efficiency measurements, published Iridium NEXT link statistics, or even laboratory CCSDS Proximity-1 testbed results. Even a rough comparison would dramatically strengthen the paper's credibility.

2. **High impact:** Restructure to lead with the generalized sizing equations (currently buried in Section V-C) and Algorithm 1 as the primary contribution, with the specific instantiation as a worked example. This reframing would make the paper more useful to practitioners and less dependent on the specific parameter choices.

3. **High impact:** Shorten the paper by consolidating Tables IV, V, VI, and IX into a single comprehensive feasibility summary, and moving the detailed sensitivity sweeps to an online supplement.

4. **Medium impact:** Develop the stochastic coordinator queueing model (MMPP/D/1) to complement the deterministic analysis and provide analytically grounded buffer sizing under compound campaign + GE dynamics.

5. **Medium impact:** Extend the analysis to deep-space or cislunar swarm scenarios where low data rates are the operational norm, broadening the applicability of the TDMA schedulability analysis beyond the RF-backup corner case.

6. **Lower impact:** Add a brief comparison with network calculus bounds (already mentioned in Related Work) to provide worst-case guarantees complementing the mean-value analysis. This would strengthen the theoretical contribution.