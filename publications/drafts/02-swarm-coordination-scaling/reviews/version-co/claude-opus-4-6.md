---
paper: "02-swarm-coordination-scaling"
version: "co"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-03-03"
recommendation: "Unknown"
---



# Peer Review: Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms

## 1. Significance & Novelty
**Rating: 3 (Adequate)**

The paper addresses a genuine gap: closed-form parametric sizing for hierarchical coordination at the 10³–10⁵ node scale with byte-level traffic accounting. The two-layer feasibility framework (byte budget + TDMA airtime) is a useful conceptual contribution, and the identification of the PHY-rate transition point (24 kbps infeasible → 30 kbps minimum → 35 kbps recommended) is actionable. However, the novelty is tempered by several factors: (a) the individual analytical components (M/D/1 queueing, GE channel models, AoI under geometric sampling, TDMA slot accounting) are well-established; (b) the integration, while careful, is primarily bookkeeping rather than methodological innovation; and (c) the absence of any external validation limits the contribution to a preliminary design exercise. The paper is forthright about this limitation, which is appreciated.

## 2. Methodological Soundness
**Rating: 3 (Adequate)**

The three-layer verification structure (DES, slot-sim, packet-level γ derivation) is well-organized and the V&V tiers are clearly labeled per IEEE 1012. However, several methodological concerns arise:

- The DES operates at message-layer granularity and confirms its own closed-form equations to <0.1%—this is code verification, not model validation, and the paper correctly acknowledges this. The distributional tail analysis (Fig. 5) is the DES's genuine incremental contribution, but the practical guidance ("buffer ≥ 1.15× mean") is derived under geometric ON/OFF assumptions that are themselves unvalidated.

- The slot-level simulator reveals the ARQ×TDMA coupling (52.7% misses at 24 kbps with M_r=1), which is a genuinely useful finding invisible to the DES. This is the strongest methodological contribution.

- The CCSDS Proximity-1 γ derivation (Section IV-J) anchors a parameter value in standards, which is appropriate. However, calling this "packet-level validation" overstates its role—it is parameter anchoring, not framework validation. The paper now correctly labels it as such in Table VII.

- The GE channel model uses design assumptions throughout. The sensitivity sweep (Fig. 4b) is the right approach for handling this uncertainty, but the default p_BG = 0.50 is presented with a geometric justification that conflates structural shadowing timescales with GE state transition probabilities in a way that deserves more careful treatment.

## 3. Validity & Logic
**Rating: 3 (Adequate)**

The internal logic is generally consistent, and the paper has clearly undergone significant revision to address prior concerns. Several specific observations:

- **Campaign duty factor (d):** The introduction of d is a significant improvement for workload realism. The mapping in Table V (mission phase → duty model) is helpful, and the empirical anchoring via ESA maneuver statistics is a good touch. The 60× gap between reverse-derived d = 0.0016 and the default d = 0.10 is acknowledged as intentional conservatism, which is appropriate.

- **Gamma unification:** The replacement of the earlier 0.85 with CCSDS-derived γ ≈ 0.76 is consistently applied throughout. Model S (0.949) is clearly labeled as a comparison bound. The rate-dependent γ (Eq. 15) is properly used. I verified consistency across Tables III, IV, VI, VIII, and IX—no discrepancies found.

- **Stress-case contextualization:** η_S ≈ 46% is now properly framed as an episodic worst-case bound (<1% of operational time), with routine operations at η ≈ 5–10%. This is a substantial improvement over presenting 46% as a representative operating point.

- **Double-counting warning:** The explicit warning against multiplying η by 1/γ AND performing the superframe check is valuable and shows careful thinking about how practitioners might misuse the framework.

- However, the claim that "commands account for >60% of protocol overhead" and are "topology-invariant under centralized command generation" deserves scrutiny. This is true only under the specific assumption that command generation is centralized and broadcast. The paper acknowledges this (Eq. 6, distributed consensus), but the framing sometimes implies topology-invariance is a general result rather than a conditional one.

## 4. Clarity & Structure
**Rating: 4 (Good)**

The paper is well-organized with a clear roadmap. The notation table (Table I) is comprehensive. The two-model distinction (Model C vs. Model S) is clearly stated upfront and consistently maintained. The rate ladder (Table III) is an excellent pedagogical device. Algorithm 1 provides an actionable synthesis.

Weaknesses: The paper is dense—at approximately 12 pages of IEEE two-column format, it pushes the limits of readability. Some material could be condensed (e.g., the thundering herd footnote, while interesting, is tangential). The number of tables (9) and figures (5) is appropriate but the cross-referencing is sometimes circular. The "Parameter dependency map" paragraph in Section IV is valuable but could be a figure.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**

Exemplary transparency: code/data availability with tagged repository, explicit AI disclosure with specific model versions, clear labeling of design assumptions vs. validated results, and honest acknowledgment that "no external validation exists; predictive accuracy for real ISL channels is unknown." The claim map (Table VII) is a model of intellectual honesty that other papers in this space should emulate.

## 6. Scope & Referencing
**Rating: 3 (Adequate)**

The reference list (56 items) covers the major relevant areas. The CCSDS standards are properly cited. However:

- Network calculus (Le Boudec) is cited but not used—a deterministic worst-case analysis via network calculus would strengthen the framework significantly and is a missed opportunity.
- The DVB-RCS2 comparison (γ ∈ [0.70, 0.85]) is useful but brief; a more detailed comparison with DVB-RCS2 slot structures would strengthen the γ anchoring.
- Missing references: Kodheli et al. (2021, IEEE COMST survey on satellite IoT) for the broader context; Leyva-Mayorga et al. for LEO constellation MAC protocols; the CCSDS Unified Space Data Link Protocol (USLP, 732.1-B) which is more current than the cited TM SDLP.
- Some references are non-archival (Amazon Kuiper, DARPA programs, DOD Replicator) and may not be accessible long-term.

---

## Major Issues

1. **The DES provides limited independent value beyond code verification.**
   - *Issue:* The DES confirms closed-form means to <0.1%, which is expected since both implement the same equations. The distributional tail analysis (Fig. 5, buffer sizing) is the sole incremental contribution, but it depends on the geometric ON/OFF campaign model, which is itself an assumption.
   - *Why it matters:* Readers may overestimate the validation strength. The paper's three-tool structure suggests triangulation, but the tools share the same underlying model.
   - *Remedy:* Either (a) explicitly state in the abstract/conclusion that the DES serves only for code verification and distributional tail characterization, not model validation; or (b) introduce a genuinely independent validation element (e.g., compare coordinator ingress statistics against DVB-RCS2 terminal return-link measurements, even if approximate). The paper partially does (a) but could be more concise about it.

2. **The generalized γ expression (Eq. 15) lacks practical calibration guidance beyond the CCSDS case.**
   - *Issue:* Eq. 15 is presented as a tool for practitioners, but the acquisition time T_acq and guard interval T_guard are the dominant uncertainty drivers, and the paper provides only two data points (CCSDS Prox-1 and a "conservative" estimate). The γ-conditional PHY lookup table (Section V-C footnote) is useful but coarse.
   - *Why it matters:* Practitioners designing for Ka-band ISL, optical-backup RF, or non-CCSDS framing need more guidance on how to estimate T_acq and T_guard for their specific hardware.
   - *Remedy:* Add a short subsection or appendix with 3–4 worked examples spanning different frequency bands, framing standards, and acquisition architectures, computing γ and the resulting PHY recommendation for each. The Ka-band example in the footnote is a start but needs expansion.

3. **The static cluster membership assumption may be more consequential than claimed.**
   - *Issue:* The paper claims re-association overhead is <0.5% based on J2 analysis of a Starlink-like Walker constellation. However, the 0.014/orbit fleet-wide re-association rate applies to a specific orbital geometry. For heterogeneous orbits (different altitudes, inclinations), re-association rates could be much higher.
   - *Why it matters:* The byte-budget analysis assumes fixed k_c per coordinator; frequent re-association changes the effective k_c and introduces transient overhead (state transfer, election) that could be significant.
   - *Remedy:* Either (a) restrict the applicability claim to co-planar or near-co-planar constellations, or (b) provide a parametric expression for re-association overhead as a function of differential precession rate, allowing practitioners to evaluate their specific geometry.

4. **The 1 kbps per-node budget justification conflates two different design drivers.**
   - *Issue:* The paper argues that sizing for the "lowest-common-denominator" RF-backup link (1 kbps) ensures architectural invariance across failure modes. But the TDMA analysis (Sections IV-V) applies to the S-band coordination channel at 24–35 kbps, not the UHF backup. The 1 kbps budget is a traffic allocation within the coordinator's PHY channel, but this distinction is sometimes blurred.
   - *Why it matters:* A reader might conclude that the entire swarm operates at 1 kbps, when in fact the coordinator link operates at 30–35 kbps and the 1 kbps is a per-node share of that capacity.
   - *Remedy:* Table II helps, but the text in Section III-E ("Why 1 kbps drives the design") should more clearly separate: (i) the per-node traffic allocation (1 kbps information budget), (ii) the coordinator PHY rate (30–35 kbps), and (iii) the UHF backup rate (2.5 kbps). A simple figure showing the rate hierarchy would help.

5. **No sensitivity analysis on message sizes.**
   - *Issue:* The entire framework is parameterized on fixed message sizes (256 B status, 512 B command, 128 B alert). These are justified by reference to CCSDS SPP and SMAD, but no sensitivity analysis explores how results change if, e.g., status reports grow to 512 B (adding sensor data) or commands shrink to 256 B.
   - *Why it matters:* Message sizes directly drive both η and the TDMA feasibility boundary. The rate ladder (Table III) would shift significantly with different message sizes.
   - *Remedy:* Add a sensitivity sweep of S_eph ∈ {128, 256, 512, 1024} B showing the resulting shift in minimum viable PHY rate and η. This is a straightforward extension of the existing framework.

## Minor Issues

1. **Abstract length:** At ~120 words, the abstract is dense but acceptable. Consider removing "Results are preliminary design estimates lacking external validation" from the abstract (it's stated multiple times in the body) and using the space for a clearer statement of the primary quantitative finding.

2. **Table I notation:** α_RX is listed as "derived from schedule, Alg. 1 line 5" but Algorithm 1 line 6 computes it. Check line numbering.

3. **Equation numbering:** Eq. 2 (γ_derived) and Eq. 15 (γ_time) both define γ but with different models. Consider numbering them as 2a/2b or adding a clearer forward reference from Eq. 2 to Eq. 15.

4. **Fig. 4 caption:** "DES bars (30 MC replications, N = 10,000, k_c = 100)" — the figure description says bars but the figure likely shows discrete points or a step function. Verify caption matches figure content.

5. **Thundering herd footnote (Section III-B.2):** The compound probability "~6.3 × 10⁻¹² s⁻¹" has units of rate, not probability. Clarify whether this is a rate or a probability per some time window.

6. **Section IV-E, empirical anchoring:** "ESA reports ~10 maneuvers/spacecraft/yr" — cite the specific ESA report section/table, not just the general annual report.

7. **Table VI (TDMA Joint Interaction):** The "GE+Exc" column header is cryptic. Expand to "GE, M_r=0, exception telemetry" or similar.

8. **Eq. 6 (η_consensus):** The variable f_decision is introduced but not included in Table I notation. Add it.

9. **Section V-C, γ-conditional PHY footnote:** The Ka-band example gives γ = 0.422, which is below the lowest bracket in the lookup table ([0.65, 0.70] → 40 kbps). This suggests the lookup table needs extension or the example needs annotation.

10. **Bibliography:** Reference [3] (Amazon Kuiper) and [48] (DOD Replicator) are non-archival web pages. Per IEEE style, these should be marked as accessed dates and noted as potentially ephemeral.

11. **"Project Dyson Research Team" authorship:** While the footnote indicates individual names will be provided for final publication, the current anonymization may not comply with IEEE's author identification requirements for review. Clarify with the editor.

12. **Section III-B.2, coordinator service:** "s_proc = 5 ms/msg (μ_c = 200 msg/s)" — this assumes single-threaded processing. Modern spacecraft processors may support multi-threading; note this as a conservative assumption.

---

## Overall Recommendation
**Recommendation: Major Revision**

This paper makes a useful contribution by providing a structured, two-layer feasibility framework for sizing hierarchical coordination in large autonomous space swarms. The framework is internally consistent, the CCSDS-grounded γ derivation is a meaningful improvement over assumed values, the campaign duty factor d addresses workload realism, and the stress-case is now properly contextualized. The paper's intellectual honesty about its limitations—particularly the absence of external validation—is commendable and sets an appropriate standard for preliminary design studies.

However, several issues prevent acceptance in the current form. The DES verification, while correctly labeled as code verification, still occupies disproportionate space relative to its incremental value. The generalized γ expression needs more worked examples to be genuinely useful for practitioners beyond the CCSDS Proximity-1 case. The static cluster membership assumption needs either tighter scoping or parametric treatment. Most critically, the absence of any message-size sensitivity analysis is a significant gap given that message sizes are the primary drivers of both feasibility layers.

The strongest elements of the paper—the rate ladder derivation, the ARQ×TDMA coupling discovery, the GE sensitivity sweep as a design tool, and Algorithm 1—should be preserved and potentially expanded. The weaker elements—extensive DES mean-value confirmation, the topology comparison (which adds little beyond establishing that mesh is infeasible), and some of the failure-mode analysis—could be condensed to make room for the recommended additions.

## Constructive Suggestions

1. **Add message-size sensitivity analysis** (highest impact): Sweep S_eph and S_cmd; show how the rate ladder and η shift. This directly strengthens the framework's practical utility.

2. **Expand γ worked examples** (high impact): Provide 3–4 examples spanning S-band/Ka-band/optical-backup with different framing and acquisition architectures. This makes Eq. 15 genuinely useful.

3. **Condense DES sections** (medium impact): Reduce Sections IV-F and IV-G; move distributional tail guidance to a compact subsection. Reclaim space for sensitivity analyses.

4. **Add a rate-hierarchy figure** (medium impact): A simple block diagram showing UHF backup (2.5 kbps) → S-band coordination (30–35 kbps) → Optical ISL (≥1 Gbps) with the 1 kbps per-node allocation clearly positioned would resolve persistent confusion about operating modes.

5. **Scope the static-membership claim** (medium impact): Either restrict to co-planar constellations or provide a parametric re-association overhead expression.

6. **Consider network calculus comparison** (lower impact, high novelty): A deterministic worst-case bound via network calculus would complement the mean-value approach and strengthen the theoretical contribution.

7. **Tighten the abstract and conclusion** (lower impact): Remove redundant limitation statements; use the space for sharper quantitative claims.