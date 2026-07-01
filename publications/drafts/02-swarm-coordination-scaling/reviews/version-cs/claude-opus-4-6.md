---
paper: "02-swarm-coordination-scaling"
version: "cs"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-03-04"
recommendation: "Unknown"
---



# Peer Review: Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms

## 1. Significance & Novelty
**Rating: 3 (Adequate)**

The paper addresses a genuine gap: closed-form sizing equations for hierarchical coordination at the 10³–10⁵ node scale with byte-level traffic accounting. The two-layer feasibility decomposition (byte budget + TDMA airtime) is a useful conceptual contribution, and the identification of the PHY rate transition boundary (24 kbps infeasible → 30 kbps minimum → 35 kbps recommended) is actionable for practitioners. However, the novelty is tempered by several factors: (1) the core equations are relatively straightforward traffic accounting and slot-timing arithmetic rather than fundamentally new analytical results; (2) the absence of any external validation means the practical significance remains speculative; (3) the claimed scale range (10⁵ nodes) is achieved through hierarchical decomposition that reduces the problem to per-cluster sizing at k_c = 100, which is not itself a novel scaling technique. The paper is more accurately characterized as a careful systems engineering parametric study than a research contribution advancing the state of the art in distributed systems theory.

## 2. Methodological Soundness
**Rating: 3 (Adequate)**

The three-layer framework (byte budget, MAC efficiency, TDMA airtime) is logically structured, and the authors are commendably transparent about what each tool can and cannot demonstrate. The campaign duty factor *d* is a welcome addition that substantially improves workload realism—the mapping to mission phases (Table VII) with empirical anchoring from ESA conjunction data is well done. The gamma unification around CCSDS Proximity-1 framing (γ₃₀ = 0.745) is consistently applied throughout, and the rate-dependent formulation (Eq. 14) is genuinely useful.

However, several methodological concerns remain:

- The DES verification (Tier 1) confirms its own equations to <0.1%, which is expected by construction. The authors acknowledge this but still devote substantial space to it. The distributional tail analysis (buffer sizing) is the DES's genuine incremental contribution, but it is relatively thin—a single CDF figure and a buffer multiplier rule.
- The GE channel model parameters are entirely assumed. While the sensitivity sweep partially mitigates this, the default p_BG = 0.50 is presented with geometric justifications that are plausible but unvalidated. The coherence assumption (GE transitions once per T_c) is a strong structural choice that makes intra-cycle ARQ ineffective *by construction*—this is a modeling decision, not a finding.
- The slot-level simulator and packet-level simulator share the same γ expression (Eq. 14); the "cross-model anchoring" (Tier 2) is therefore parameter consistency checking, not independent validation.

## 3. Validity & Logic
**Rating: 3 (Adequate)**

The internal logic is generally sound, and the authors have done a good job of maintaining consistency across the gamma values (the earlier 0.85 appears to have been fully replaced by the CCSDS-grounded values). The stress-case η_S ≈ 46% is now properly contextualized as an episodic upper bound with the duty factor framework, which is a significant improvement.

Several logical concerns:

- The claim that "architecture-specific overhead (η₀ ≈ 5%) is small" and "command traffic dominates (>60%) and is topology-invariant under centralized command generation" somewhat undermines the paper's own motivation. If the dominant overhead is topology-invariant, the choice of hierarchical vs. centralized architecture matters less than the paper implies.
- The static cluster membership assumption is justified for co-planar formations, but the paper's claimed applicability to 10⁵-node swarms implicitly requires cross-plane configurations where this assumption breaks down. The 0.5% re-association overhead estimate needs more rigorous treatment for the general case.
- The spatial reuse analysis (R = 3, F = 4) is acknowledged as order-of-magnitude, but it underpins the fleet-level scaling claims. Without NS-3 validation, the fleet-level feasibility statements are unsupported.
- The 1 kbps per-node budget is a design choice, not a physical constraint. The paper argues it ensures "coordination invariance across failure modes," but this conflates the RF-backup survival mode (where hierarchy is suspended anyway, per Table III) with the S-band coordination channel. If hierarchy is suspended during RF-backup, why must the coordination budget be sized for RF-backup capacity?

## 4. Clarity & Structure
**Rating: 4 (Good)**

The paper is well-organized with a clear roadmap, consistent notation (Table I is comprehensive), and explicit model labeling (Model S vs. Model C). The repeated warnings about which model is used for recommendations vs. comparison bounds are helpful. Algorithm 1 is a genuine contribution to practitioner usability. The claim map (Table IX) is an excellent transparency device.

Areas for improvement:
- The paper is extremely dense and long for a journal article. There is significant repetition—the 35 kbps recommendation, the γ values, and the stress-case contextualization are each stated 5+ times.
- The notation table lists α_RX as "derived from schedule" but it appears in equations before the schedule is fully defined, creating a forward-reference issue.
- Some figures are referenced but not shown in the manuscript text (the PDF generation is assumed; this review assumes they exist as described).
- The boxed feasibility framework definition in Section IV is helpful but interrupts the flow.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**

The paper is exemplary in its transparency: AI tool usage is explicitly disclosed with specific model versions; data availability includes tagged source code, simulators, and configuration; the claim map explicitly identifies what has and has not been validated; limitations are stated prominently (including in the abstract). The V&V tier structure with explicit acknowledgment that "no external validation exists; predictive accuracy for real ISL channels is unknown" sets a high standard for intellectual honesty.

## 6. Scope & Referencing
**Rating: 3 (Adequate)**

The reference list covers the major relevant areas (CCSDS standards, swarm robotics, constellation management, distributed systems theory, AoI). However:
- Several references are non-archival (Amazon Kuiper overview, DARPA program pages, DOD fact sheets) and may not persist.
- The related work section is broad but shallow—it lists many works without critically engaging with how they relate to the specific sizing problem.
- Missing references: no citation of actual TDMA scheduling literature for satellite systems (e.g., Pratt & Bostian for satellite communications fundamentals); no reference to the substantial body of work on cluster-based satellite network architectures; no engagement with the network calculus literature beyond a single citation despite the deterministic worst-case framing being directly relevant.
- The DVB-RCS2 comparison for γ uncertainty bounds is creative but the analogy (ground terminals vs. ISL) is weak and acknowledged as such.

---

## Major Issues

1. **The DES provides negligible independent verification value.**
   - *Issue:* The DES reproduces closed-form means to <0.1% because it implements the same equations. The authors acknowledge this (Tier 1 verification) but still present it as a significant validation step. The distributional analysis (buffer sizing) is the only genuine DES contribution, but it amounts to one CDF figure and a buffer multiplier.
   - *Why it matters:* Readers may overestimate the validation status of the results. Journal space devoted to confirming arithmetic correctness could be better used.
   - *Remedy:* Reduce DES mean-value comparison to a single sentence. Expand the distributional analysis with additional scenarios (e.g., varying k_c, correlated failures) to justify the DES's existence. Alternatively, acknowledge that the DES is primarily a design tool rather than a validation instrument.

2. **The packet-level validation (Section IV-J) does not provide independent validation.**
   - *Issue:* The CCSDS-grounded γ derivation computes γ from Eq. 14 using assumed timing parameters (T_acq = 5 ms, T_guard = 4.7 ms). The slot-sim and packet-sim use the same equation. This is parameter estimation, not validation. The DVB-RCS2 comparison (γ = 0.70–0.85) provides a plausibility check but not validation of the specific Proximity-1 implementation.
   - *Why it matters:* The paper's central recommendation (35 kbps) depends critically on γ ≈ 0.745. If real Proximity-1 implementations achieve γ = 0.65 (due to longer acquisition, Doppler compensation, etc.), the minimum PHY rate shifts to ~34 kbps and the 35 kbps recommendation has only ~3% margin.
   - *Remedy:* (a) Clearly label Section IV-J as "parameter estimation" throughout (partially done but inconsistently). (b) Provide a sensitivity table showing how the PHY recommendation shifts for γ ∈ [0.60, 0.85] in 0.05 increments. (c) Identify specific Proximity-1 implementations where T_acq could be measured.

3. **The 1 kbps per-node budget justification is circular.**
   - *Issue:* The paper argues that 1 kbps ensures "coordination invariance across failure modes" (Section III-E). But Table III shows that during RF-backup (the failure mode motivating the low budget), hierarchical coordination is *suspended*—nodes enter safe-hold with beacon-only communication. If the architecture doesn't operate during the failure mode it's supposedly designed for, the 1 kbps constraint is not justified by failure-mode invariance.
   - *Why it matters:* The 1 kbps budget is the single most consequential design choice in the paper. All overhead percentages, the stress-case concern, and the PHY rate recommendation flow from it. If 2 kbps is acceptable, stress-case η drops to ~23% and the entire TDMA analysis becomes non-binding.
   - *Remedy:* Provide a clearer justification for 1 kbps that does not rely on RF-backup invariance. Possible justifications: spectrum allocation constraints, interference budget, power constraints on the S-band ISL. Alternatively, present results parametrically across C_node ∈ {0.5, 1, 2, 5} kbps with explicit identification of which constraints bind at each level.

4. **Fleet-level scaling claims are unsupported.**
   - *Issue:* The paper claims applicability to 10⁵ nodes but the analysis is per-cluster (k_c = 100). Fleet-level scaling depends on spatial reuse (R = 3), which is justified by a free-space path loss argument that ignores sidelobe coupling, near-far effects, and orbital dynamics.
   - *Why it matters:* The title and abstract promise "large autonomous space swarms" at 10³–10⁵ scale, but the validated analysis covers only the per-cluster regime.
   - *Remedy:* Either (a) scope the claims to per-cluster sizing and remove fleet-level scaling from the title/abstract, or (b) provide NS-3 or equivalent multi-cluster simulation results. At minimum, add a quantitative uncertainty bound on the spatial reuse assumption.

5. **The GE coherence assumption predetermines the ARQ ineffectiveness finding.**
   - *Issue:* By assuming GE transitions once per T_c, all intra-cycle retransmissions face the same channel state. This makes the "finding" that intra-cycle ARQ achieves only 27% recovery a direct consequence of the modeling assumption, not an emergent result.
   - *Why it matters:* The ARQ ineffectiveness drives the recommendation for inter-cycle recovery and influences the PHY rate recommendation (35 kbps for ARQ vs. 30 kbps without).
   - *Remedy:* (a) Model sub-cycle GE transitions (e.g., transition probability per slot rather than per cycle) and show how ARQ effectiveness varies with coherence time. (b) At minimum, clearly state that the 27% figure is a *lower bound* on ARQ effectiveness that applies only when τ_c ≥ T_c, and provide the complementary upper bound for τ_c ≪ T_c (partially done with the 98.9% figure but not systematically).

## Minor Issues

1. **Inconsistent γ subscript notation.** The paper uses γ₂₄, γ₃₀, γ_C, γ_S, γ_{C,24}, γ_{C,30} interchangeably. Standardize to γ(R_PHY, Model) throughout.

2. **Table V (TDMA Joint Interaction) uses Model S timing but is presented in the main results.** Despite the bold warning, placing a Model S table in the results section risks confusion. Move to an appendix or present Model C results alongside.

3. **The "thundering herd" analysis (footnote 1) is interesting but buried.** The Slotted ALOHA with BEB convergence analysis deserves main-text treatment or a separate subsection, as it affects the RF-backup failure recovery time.

4. **Eq. 7 (η_consensus) assumes serialized Raft votes over the shared channel.** This is stated but the implications for multi-decision scenarios (f_decision > 1) are not fully explored. At f_decision = 2, η_consensus ≈ 31%—does this interact with the TDMA schedule?

5. **The abstract states "γ ≈ 0.74–0.76 (rate-dependent; γ₃₀ = 0.745 at 30 kbps)"** but the text also gives γ₂₄ = 0.761. The range 0.74–0.76 doesn't clearly include 0.761. Clarify the range or specify it as γ(24–50 kbps).

6. **Table II Panel B** lists "Rec. PHY" values but doesn't specify whether these include half-duplex partitioning. Add a footnote.

7. **Section III-B-2 states "each cluster coordinator sends a single 512-byte summary"** and provides a byte-level breakdown totaling 141 B of structured data + 371 B of "metadata/CRC." The 371 B of metadata/CRC seems disproportionate—clarify what this contains.

8. **The collision avoidance rate (10⁻⁴/node/s)** is stated as Poisson but the ESA anchoring gives ~10 events/spacecraft/year ≈ 3.2×10⁻⁷/s, three orders of magnitude lower. Reconcile or explain the discrepancy.

9. **Reference [53] (dyson_multimodel)** is a self-citation to a non-peer-reviewed preprint. This is acceptable for AI disclosure but should not be cited as methodological support.

10. **The paper lacks a complexity analysis** of Algorithm 1 itself. While trivial (O(1) per evaluation), stating this explicitly would be useful.

11. **Fig. 3 caption** references "DES bars (30 MC replications, N = 10,000, k_c = 100)" but the text states the DES runs at N = 10⁵. Clarify which N is used for this figure.

12. **Eq. 14 (γ time-domain):** The framing term T_framing = O_frame / (R_FEC · R_PHY) assumes framing bits are FEC-encoded. This is stated but should be flagged as a design choice—some implementations place framing outside the FEC codeword.

---

## Overall Recommendation
**Recommendation: Major Revision**

This paper presents a carefully constructed parametric sizing framework for hierarchical coordination in large space swarms. Its principal strengths are: (1) the clean two-layer feasibility decomposition with explicit boundary conditions; (2) exceptional transparency about assumptions, limitations, and validation status; (3) the actionable Algorithm 1 and rate ladder (Table IV); and (4) the campaign duty factor framework with mission-phase mapping, which substantially improves workload realism over a continuous stress-case assumption.

However, the paper suffers from several significant issues that prevent acceptance in its current form. The most critical is the validation gap: all internal tools share the same equations, making the multi-tool "verification" largely tautological. The DES confirms arithmetic; the packet-level analysis estimates a parameter; neither provides independent evidence that the framework produces correct predictions for real systems. The 1 kbps budget justification is circular (RF-backup suspends hierarchy), and the fleet-level scaling claims are unsupported beyond order-of-magnitude plausibility. The GE coherence assumption predetermines the ARQ ineffectiveness finding rather than discovering it.

For a major revision, the authors should: (1) clearly delineate what is a modeling *decision* vs. a *finding*; (2) resolve the 1 kbps justification; (3) either scope claims to per-cluster sizing or provide multi-cluster simulation; (4) reduce redundancy (the paper could lose 20–30% of its length without losing content); and (5) consider whether the contribution is better positioned as a systems engineering design tool paper rather than a research paper advancing fundamental understanding.

## Constructive Suggestions

1. **Highest impact: Provide one external validation point.** Even a single comparison—e.g., reproducing a published TDMA efficiency measurement from a Proximity-1 or DVB-RCS2 testbed—would dramatically strengthen the paper. If no measurement is available, an NS-3 simulation of a single 100-node cluster with realistic MAC would suffice.

2. **Reframe the contribution.** The paper's strongest contribution is the *design procedure* (Algorithm 1 + rate ladder + duty factor mapping), not the specific numeric results. Reframing around the procedure—with numeric results as instantiation examples—would better match the evidence level.

3. **Add sub-cycle GE analysis.** Parameterize the GE transition rate per slot (not per cycle) and show ARQ effectiveness as a function of coherence time. This would transform the ARQ finding from a modeling assumption into a genuine result.

4. **Consolidate and shorten.** The 35 kbps recommendation, γ values, and stress-case contextualization are each repeated 5+ times. A single definitive statement with forward/backward references would improve readability and reduce length by ~15%.

5. **Expand the practitioner interface.** The γ-conditional PHY lookup and worked examples (Section IV-J) are the most practically useful parts of the paper. Add 2–3 more worked examples spanning different orbit regimes (GEO relay, lunar, deep-space) to demonstrate generality.

6. **Address the C_node justification directly.** Present a table showing which constraints bind at C_node ∈ {0.5, 1, 2, 5, 10} kbps. This would make the 1 kbps choice transparent and allow readers to assess their own scenarios.