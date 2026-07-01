---
paper: "02-swarm-coordination-scaling"
version: "cr"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-03-04"
recommendation: "Unknown"
---



# Peer Review: Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms

## 1. Significance & Novelty
**Rating: 3 (Adequate)**

The paper addresses a genuine gap: closed-form parametric sizing for hierarchical coordination at the 10³–10⁵ node scale with byte-level traffic accounting. The two-layer feasibility framework (byte budget + TDMA airtime) is a useful conceptual contribution. However, the novelty is tempered by several factors: (a) the core analytical results are relatively straightforward engineering calculations (traffic accounting, slot timing, M/D/1 queueing) rather than fundamentally new theory; (b) the architecture-specific overhead (η₀ ≈ 5%) is small and the dominant cost (commands, >60%) is acknowledged as topology-invariant, which somewhat undermines the case for hierarchical coordination as a distinct contribution; (c) the absence of any external validation means the practical significance remains speculative. The campaign duty factor parameterization and the γ-conditional PHY rate lookup are genuinely useful for practitioners, but the paper reads more as a detailed design study than a research contribution advancing the state of the art.

## 2. Methodological Soundness
**Rating: 3 (Adequate)**

The three-layer feasibility framework (byte budget, MAC efficiency, TDMA airtime) is logically structured and internally consistent. The CCSDS Proximity-1 grounding of γ is a clear improvement over assumed values. The campaign duty factor d is a well-motivated parameterization that addresses workload realism. However:

- The DES operates at message-layer granularity and shares equations with the analytical model, making the "verification" largely tautological for mean values. The distributional analysis (buffer CDFs) is the genuine incremental contribution of the DES, but this is a narrow addition.
- The slot-level simulator reveals the ARQ×TDMA coupling, which is valuable, but operates under Model S (simplified) for the key interaction table (Table VII), creating an awkward disconnect with the Model C recommendations.
- The GE channel model uses entirely assumed parameters with no empirical grounding for ISL channels. While sensitivity curves are provided, the default parameterization (p_BG = 0.50) lacks justification beyond geometric plausibility arguments.
- The queueing model (MMPP/D/1) is mentioned but not solved; closed-form tail bounds are deferred to future work.

## 3. Validity & Logic
**Rating: 4 (Good)**

The internal logic is generally sound and the paper is commendably transparent about its limitations. Specific strengths:

- The stress-case (η_S ≈ 46%) is now properly contextualized as an episodic worst-case bound (<1% of operational time), with the time-weighted mean η ≈ 5.9% providing a realistic operational estimate. This is a significant improvement.
- The gamma unification is consistently applied: γ₃₀ = 0.745 is used for all feasibility claims and design recommendations; Model S appears only as a labeled comparison bound. I verified consistency across Tables III, V, VI, VIII, IX, and the rate ladder (Table IV).
- The parameter dependency map (Section IV preamble) clearly separates ingress-side constraints (independent of d) from egress/byte-budget concerns.
- The claim map (Table X) is admirably honest about evidence tiers.

One logical concern: the paper claims the framework applies to 10³–10⁵ nodes, but the TDMA analysis is fundamentally per-cluster (k_c = 100). The fleet-level reuse analysis (Eq. 14, Section IV-A.1) is cursory, relying on an order-of-magnitude spatial reuse argument that the authors themselves flag as requiring NS-3 validation.

## 4. Clarity & Structure
**Rating: 3 (Adequate)**

The paper is dense but generally well-organized. The roadmap paragraph at the start of Section IV is helpful. The notation table (Table I) is comprehensive. However:

- The paper is excessively long for a journal article. Significant redundancy exists: the same quantities (γ values, rate recommendations, margin calculations) are repeated across multiple tables, equations, and prose passages. The superframe budget appears in at least four places.
- The two-model system (Model S vs. Model C) adds complexity. While the paper is careful to label which model is used where, the reader must constantly track this distinction. Since Model S is "never used for recommendations," one questions whether it should appear at all beyond a single comparative figure.
- Some sections read as defensive responses to prior review comments rather than flowing exposition (e.g., the extensive caveats about what the DES does and does not validate).
- The footnotes are overloaded with critical information that belongs in the main text (e.g., the thundering herd analysis in footnote 1).

## 5. Ethical Compliance
**Rating: 5 (Excellent)**

Exemplary transparency: code and data are publicly available with a tagged release; simulation parameters are fully specified; AI usage is disclosed with specific model versions; the validation gap is prominently acknowledged in the abstract, throughout the text, and in a dedicated section. The claim map (Table X) with evidence tiers is a model of responsible reporting.

## 6. Scope & Referencing
**Rating: 3 (Adequate)**

The literature coverage is broad but somewhat shallow in key areas. Missing or underrepresented:

- No engagement with the substantial literature on TDMA scheduling optimization for satellite networks (e.g., Choi & Shin, Ramanathan & Lloyd on TDMA scheduling complexity).
- Network calculus is cited but not applied; a deterministic worst-case bound via network calculus would strengthen the framework significantly.
- The DVB-RCS2 comparison is mentioned once but not developed—this is the closest operational analog and deserves deeper treatment.
- No discussion of CCSDS File Delivery Protocol (CFDP) for the handoff state transfers.
- The swarm robotics references are dated (Reynolds 1987, Brambilla 2013); more recent work on communication-constrained multi-robot coordination (e.g., Prorok, Queralta) is absent.

---

## Major Issues

**1. The DES verification provides minimal value beyond confirming its own equations.**

The paper acknowledges this (Tier 1 verification, <0.1% agreement "by construction"), but then devotes substantial space to DES results. The distributional tail analysis (Fig. 5, buffer sizing) is the sole genuine DES contribution, yet it relies on the same GE model with assumed parameters. The paper should either (a) significantly reduce DES coverage and reframe it purely as a buffer-sizing tool, or (b) introduce genuinely independent verification (e.g., comparison with an NS-3 model for even a single cluster).

*Why it matters:* Readers may overestimate the validation level. The current framing—three V&V tiers with only Tier 1 populated—highlights rather than resolves this gap.

*Remedy:* Condense DES results to one paragraph plus one figure (buffer CDF). Move the DES architecture description to an appendix. Be explicit that the DES is a distributional analysis tool, not a validator.

**2. The packet-level validation (Section IV-J) does not provide independent validation.**

The γ derivation from CCSDS Proximity-1 framing is a parameter estimation exercise, not validation. The paper correctly labels it as such ("standards-based parameter estimate, not independent validation"), but the section title ("CCSDS-Grounded Slot Efficiency Calculation") and its placement as the culminating results subsection may mislead readers. The γ value feeds directly into the same equations used throughout; there is no independent check.

*Why it matters:* The paper's central claim—that 35 kbps is the recommended PHY rate—rests entirely on γ ≈ 0.745, which is computed from assumed acquisition and guard times (5 ms and 4.7 ms respectively). A ±2 ms change in acquisition time shifts the recommendation by ~3–5 kbps.

*Remedy:* Rename the section to "Slot Efficiency Parameter Estimation" or similar. Present the DVB-RCS2 measured range (0.70–0.85) more prominently as the uncertainty envelope. Consider adding a simple sensitivity table: γ vs. (T_acq, T_guard) → R_PHY,min.

**3. Fleet-level scalability analysis is insufficient for the claimed 10³–10⁵ range.**

The TDMA analysis is fundamentally per-cluster. The fleet-level extension (Eq. 14) assumes spatial reuse R = 3 with an order-of-magnitude plausibility argument. For a paper claiming to address 10⁵-node swarms, the inter-cluster coordination, frequency planning, and multi-hop relay aspects are underdeveloped.

*Why it matters:* At N = 10⁵ with k_c = 100, there are 1,000 clusters. The assumption that these can be independently scheduled with R = 3 spatial reuse is non-trivial and unvalidated. Dynamic orbital geometry means the reuse pattern changes continuously.

*Remedy:* Either (a) reduce the claimed scope to per-cluster sizing (which is what the analysis actually provides) and frame fleet-level extension as future work, or (b) provide a more rigorous fleet-level analysis including time-varying reuse patterns under representative orbital geometries.

**4. The GE channel model lacks any empirical grounding for ISL channels.**

While the paper is transparent about this ("design assumptions, not measured ISL data"), the entire loss recovery analysis—including the key finding that intra-cycle ARQ recovers only 27% under bad-state bursts—depends on assumed GE parameters. No ISL-specific channel measurements exist in the open literature, and the paper does not attempt to derive GE parameters from link budget analysis or ray-tracing.

*Why it matters:* The ARQ×TDMA coupling finding (52.7% deadline misses) and the 35 kbps recommendation both depend critically on the GE parameterization. If the actual ISL channel is better (or worse) than assumed, the design point shifts significantly.

*Remedy:* (a) Derive GE parameters from first principles using the link budget (Section IV-A) and ITU-R P.681 propagation models. (b) Present results as a family of curves parameterized by (p_BG, p_B) rather than anchoring to a single "default." The sensitivity sweep in Fig. 4b partially does this but should be the primary presentation rather than a supplement.

---

## Minor Issues

1. **Table I notation:** α_RX is listed as "≈ 0.908" but this is derived from the schedule (Algorithm 1, line 6). The table should note it is a derived quantity more prominently (it does say "derived" but this is easy to miss).

2. **Eq. 5 (η_canonical):** The equation shows η = η₀ + d·η_cmd, but η_cmd itself is not given a standalone equation. Define η_cmd = p_cmd · S_cmd × 8 / (C_node · T_c) explicitly.

3. **Table VII (Joint Interaction):** Uses Model S slot timing but the caption footnote explaining this is easy to miss. Consider adding "MODEL S" to the table title itself.

4. **Section III-B.2:** "Each cluster coordinator sends a single 512-byte summary per cycle" — the breakdown (48+48+13+32+371 = 512 B) allocates 371 B to "metadata/CRC," which seems excessive. CRC-32 is 4 bytes; what fills the remaining 367 bytes?

5. **Eq. 10 (η_consensus):** The factor f_decision appears both as "decisions per cycle" and multiplied by the per-decision cost, but the equation seems to assume all decisions are serialized. Clarify whether parallel decisions are possible and how they would affect the equation.

6. **Fig. 3 (margin sensitivity):** The axis labels and legend are not described in sufficient detail. What are the contour levels? Is this a 2D sweep or multiple 1D curves?

7. **Section IV-A:** "Phase-staggered scheduling... DES confirms zero drops at ≥25 kbps vs. 50 kbps under random phase." This is stated without supporting data. Add a brief table or reference to supplementary material.

8. **Table IX (Duty Mapping):** The collision avoidance row shows d = 1.0 "during event" but the text says background d < 0.01. Clarify the temporal scope—is d = 1.0 for 6 cycles per event?

9. **References:** Several are non-archival (Amazon Kuiper overview, DARPA program pages, DoD fact sheets). While understandable, these should be minimized for a journal publication. Consider replacing with archival FCC filings or conference papers where possible.

10. **Abstract:** "Results are preliminary design estimates lacking external validation" is commendably honest but may be better placed as the penultimate rather than final sentence, ending instead with the actionable design recommendation.

11. **Eq. 8 (gamma_time):** T_framing = O_frame / (R_FEC · R_PHY) assumes framing bits are FEC-encoded. This is stated in the text but should be noted directly in the equation or its immediate context, as some implementations send framing outside the FEC codeword.

12. **Section V-C (Limitations):** The J2 analysis for dynamic topology is interesting but feels like it belongs in an appendix. The main text should simply state the applicability assumption and the re-association overhead bound.

---

## Overall Recommendation
**Recommendation: Major Revision**

This paper presents a well-structured engineering analysis of hierarchical coordination sizing for large autonomous space swarms. Its principal strengths are: (1) the clean two-layer feasibility decomposition (byte budget + TDMA airtime); (2) the CCSDS-grounded γ derivation replacing earlier assumed values; (3) the campaign duty factor parameterization that realistically contextualizes the stress-case overhead; (4) exceptional transparency about limitations and validation gaps; and (5) full code/data availability.

However, the paper suffers from three fundamental weaknesses that prevent acceptance in its current form. First, the validation architecture is circular: the DES, slot-sim, and packet-level analysis all share the same underlying equations, and the paper's honesty about this does not resolve the scientific concern. The sole emergent finding (ARQ×TDMA coupling at 52.7%) comes from the slot-sim under Model S parameters, not the recommended Model C. Second, the fleet-level scalability claim (10⁵ nodes) is not adequately supported—the analysis is per-cluster, and the inter-cluster coordination problem is addressed only with an order-of-magnitude spatial reuse argument. Third, the GE channel model is entirely assumed, making the loss recovery analysis and the 35 kbps recommendation contingent on unvalidated parameters.

The paper would benefit significantly from: reducing its length by ~30% (eliminating redundancy, moving DES details to supplementary material); reframing the contribution as per-cluster sizing equations with fleet-level extension as future work; deriving GE parameters from link budget first principles; and either providing one external validation point (even a simplified NS-3 single-cluster model) or more explicitly framing the work as a design methodology paper rather than a validated system analysis.

## Constructive Suggestions

1. **Highest impact: Add one external validation point.** Even a simplified NS-3 simulation of a single 100-node cluster with TDMA scheduling would transform the paper's credibility. This need not be comprehensive—a single operating point confirming the γ and deadline-miss predictions would suffice.

2. **Reduce length by 25–30%.** Consolidate the rate ladder information (currently spread across Tables III, IV, V, VI, XI, and multiple prose passages) into a single authoritative table. Move Model S results to supplementary material. Condense the DES description.

3. **Reframe the contribution scope.** The paper's actual contribution is per-cluster sizing equations + a feasibility algorithm. Frame it as such, with fleet-level extension as a clearly delineated future direction rather than a claimed result.

4. **Derive GE parameters from physics.** Use the S-band link budget (already computed) with ITU-R P.681 to derive plausible (p_BG, p_B) ranges. This would ground the channel model in something beyond assumption.

5. **Strengthen the practitioner value proposition.** Algorithm 1 is excellent. Consider adding a second worked example with different parameters (e.g., k_c = 50, S = 128 B, T_c = 5 s) to demonstrate the generality of the sizing procedure.

6. **Address the "why not just use more bandwidth?" question.** At ≥10 kbps per node, both feasibility layers are trivially satisfied. The paper should more explicitly justify why the 1 kbps regime is the interesting design point—the RF-backup argument is made but could be strengthened with a quantitative assessment of how often optical ISL outages occur in practice.