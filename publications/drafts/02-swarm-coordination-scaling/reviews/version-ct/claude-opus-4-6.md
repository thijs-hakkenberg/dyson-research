---
paper: "02-swarm-coordination-scaling"
version: "ct"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-03-04"
recommendation: "Unknown"
---



# Peer Review: "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version CT)

---

## 1. Significance & Novelty
**Rating: 3 (Adequate)**

The paper addresses a genuine gap: closed-form parametric sizing for hierarchical coordination at scales of 10³–10⁵ spacecraft. The two-layer feasibility framework (byte budget + TDMA airtime) and the actionable Algorithm 1 are useful contributions. However, the novelty is tempered by several factors: (a) the core equations are relatively straightforward traffic accounting and TDMA slot arithmetic—the intellectual contribution lies more in their systematic assembly than in analytical depth; (b) the absence of any external validation means the practical value remains speculative; (c) the paper's primary finding—that coordinator ingress at ~20 kbps information-rate requires ≥30 kbps PHY—is essentially a link budget exercise dressed in a coordination framework. The campaign duty factor and γ-conditional PHY lookup table are genuinely useful for practitioners, but the contribution would be substantially stronger with even one hardware or NS-3 data point.

## 2. Methodological Soundness
**Rating: 3 (Adequate)**

The three-layer feasibility framework (byte budget, MAC efficiency, TDMA airtime) is logically structured, and the paper is commendably transparent about what each layer does and does not capture. Several methodological concerns remain:

- The DES is cycle-aggregated and shares the same equations as the analytical model, making the <0.1% agreement a verification tautology (acknowledged by the authors). The distributional analysis (buffer CDFs) provides some incremental value but is limited by the same message-model assumptions.
- The GE channel model uses design assumptions with no ISL-specific calibration. While the sensitivity sweeps are helpful, the default parameters (p_BG = 0.50, p_B = 0.90) are not grounded in any ISL measurement, and the paper's physical mapping (structural shadowing, antenna mispointing) is qualitative.
- The slot-level simulator and packet-level γ derivation share the same framing assumptions; calling this "Tier 2 cross-model anchoring" overstates the independence of the evidence.
- The fluid-server coordinator model (drop-tail, deterministic service) is simplistic; the MMPP/D/1 acknowledgment is appropriate but the absence of closed-form tail bounds for this model weakens the buffer sizing claims.

## 3. Validity & Logic
**Rating: 4 (Good)**

The internal logic is generally sound and self-consistent. Specific improvements in this version:

- The campaign duty factor (d) now adequately addresses workload realism. The stress-case η_S ≈ 46% is properly contextualized as an episodic upper bound (<1% of operational time), with worked examples (Table 7) mapping mission phases to realistic d values. This is a significant improvement.
- The gamma unification around 0.745 (at 30 kbps) via CCSDS Proximity-1 framing is consistently applied throughout. The earlier 0.85 value has been replaced, and Model S (0.949) is clearly labeled as a comparison bound only. The rate-dependent γ expression (Eq. 14) is correctly derived and consistently used.
- The three-layer framework is logically coherent, with clear separation between information-layer (η), slot-structure (γ), and airtime (ingress + egress ≤ T_c) constraints. The explicit warning against double-counting (Section IV preamble) is helpful.

One logical concern: the paper claims "architecture-specific overhead is small (η₀ ≈ 5%)" and "command traffic dominates (>60%)"—but this makes the hierarchical vs. centralized comparison less meaningful, since the dominant overhead is topology-invariant. The 5 pp difference between hierarchical and centralized is modest, raising the question of whether the hierarchical architecture's complexity is justified by the analysis presented.

## 4. Clarity & Structure
**Rating: 3 (Adequate)**

The paper is exhaustively detailed but suffers from organizational challenges:

- At ~15 journal pages equivalent, the manuscript is dense. The extensive inline caveats, footnotes, and cross-references (while individually appropriate) create a reading experience that is difficult to follow linearly. A reader must track two slot-timing models, three overhead tiers, two feasibility layers, multiple rate definitions, and numerous conditional statements.
- The notation table (Table I) is helpful but incomplete—several symbols used in the text (e.g., π_G, τ_c, β) are not listed.
- Figures are referenced but described as PDF files; the review cannot assess their quality. The figure descriptions in captions are adequate.
- The paper would benefit from a consolidated "design summary" figure showing the complete decision tree from mission parameters to PHY rate recommendation, rather than requiring readers to mentally assemble Algorithm 1, Table V, and the γ-conditional lookup.
- Some sections (e.g., IV-A) mix derivation, simulation results, link budget, and design recommendations in a way that makes it hard to identify the key takeaway.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**

Exemplary transparency: code/data availability with tagged repository, explicit AI disclosure (ideation only, not results), clear acknowledgment of all assumptions and limitations, honest claim mapping (Table IX) with explicit "absent" for external validation. The V&V tier structure (IEEE 1012) is a best practice. The repeated caveats about preliminary design estimates are appropriate and commendable.

## 6. Scope & Referencing
**Rating: 3 (Adequate)**

The reference list (55 items) covers the major relevant areas but has gaps:

- No references to actual ISL measurement campaigns (e.g., EDRS, OISL demonstrations on Starlink v2) that could anchor the GE parameters.
- Limited engagement with the satellite TDMA literature beyond DVB-RCS2; MF-TDMA standards for military satcom (MIL-STD-188-181) and commercial VSAT (DVB-S2X return link) would provide additional γ benchmarks.
- The network calculus reference (Le Boudec) is cited but not used; deterministic worst-case bounds would strengthen the buffer sizing claims.
- No comparison with recent distributed satellite computing frameworks (e.g., OrbitsEdge, Loft Orbital's computation-in-orbit work).
- The self-citation [dyson_multimodel] is a non-peer-reviewed preprint and should be flagged as such (it is, but its inclusion as a reference for the AI methodology is borderline).

---

## Major Issues

**1. The DES verification provides negligible independent value beyond confirming its own equations.**

The <0.1% agreement between DES and closed-form means is explicitly acknowledged as "implementation correctness, not model validity" (Section III-A). However, the paper still devotes substantial space to DES results that are, by construction, identical to the analytical model. The distributional analysis (Fig. 4, buffer CDFs) is the sole incremental DES contribution, but it relies on the same message generation model and fluid-server abstraction. The claim that DES provides "Tier 1 verification" per IEEE 1012 is technically correct but may mislead readers into thinking more validation has occurred than is the case.

*Why it matters:* Readers may overestimate the confidence level of the results. The paper's length is partly driven by reporting DES results that add little beyond the equations.

*Remedy:* Condense DES reporting to the distributional analysis only (Fig. 4, buffer sizing rule). Remove or relegate mean-value DES comparisons to a brief statement. Be explicit in the abstract/conclusion that the DES is a code verification tool, not a model validation tool. Consider whether the distributional analysis could be replaced by a closed-form MMPP/D/1 tail bound.

**2. The packet-level validation (Section IV-J) is parameter estimation, not validation.**

The γ derivation from CCSDS Proximity-1 framing is presented as "Tier 2 cross-model anchoring," but it shares the same slot-structure equations used throughout the paper. The DVB-RCS2 comparison (γ = 0.70–0.85) provides a useful sanity check but is for ground terminals, not ISLs. No modem measurements, no hardware-in-the-loop data, and no independent simulation (e.g., NS-3 with a Proximity-1 PHY model) are used.

*Why it matters:* The entire rate recommendation (30–35 kbps) depends on γ. A 10% error in γ shifts the minimum PHY rate by 3–5 kbps (acknowledged in Section V-B). Without any measured γ, the recommendation is conditional on an untested parameter.

*Remedy:* Rename "Slot Efficiency Parameter Estimation" (already done in the section title—good) and ensure the abstract and conclusion do not imply validation. Add a sensitivity band to the final recommendation: "35 kbps recommended; if measured γ < 0.70, increase to 40 kbps." Consider adding a brief discussion of what modem-level measurements would be needed (acquisition time statistics, guard time adequacy under Doppler).

**3. Fleet-level scaling claims are insufficiently supported.**

The spatial reuse argument (Eq. 8, R = 3, F = 4) is acknowledged as "order-of-magnitude" but is used to extend per-cluster results to 10⁵ nodes. The 20 dB isolation claim at 500 km with 6 dBi antennas is a free-space estimate that ignores sidelobe coupling, near-far effects, and dynamic orbital geometry. The paper correctly identifies NS-3 validation as needed but still makes fleet-level claims in the abstract and conclusion.

*Why it matters:* The paper's title and abstract promise "large autonomous space swarms" at 10⁵ scale, but the validated analysis is per-cluster (k_c = 50–500). Fleet-level feasibility is a different problem involving inter-cluster interference, routing, and dynamic topology.

*Remedy:* Restrict abstract/conclusion claims to per-cluster sizing. Present fleet-level scaling as a "preliminary extension" with explicit caveats. Consider removing fleet-level claims from the abstract entirely, or qualifying them as "per-cluster sizing that is necessary but not sufficient for fleet-level feasibility."

**4. The 1 kbps per-node budget lacks independent justification.**

The paper derives the 1 kbps budget from a link budget (200 kbps aggregate / 100 nodes × γ ≈ 1.5 kbps, with 50% margin → 1 kbps). However, this link budget assumes specific antenna parameters (6 dBi, 1 W, S-band, 500 km) that are not validated against any existing ISL hardware. The entire feasibility analysis is conditioned on this budget; if the actual per-node capacity is 0.5 kbps (e.g., due to higher interference or lower antenna gain), the stress-case becomes infeasible (η_stress ≈ 92%).

*Why it matters:* The 1 kbps budget is the single most consequential assumption in the paper. All overhead percentages, feasibility conclusions, and PHY recommendations scale directly with it.

*Remedy:* Present results for a range of C_node values (0.5, 1, 2, 5 kbps) in a consolidated sensitivity table. The paper already notes linear scaling (Table II-A) but should make this a primary result rather than a footnote. Explicitly state the link budget assumptions and their sensitivity.

**5. The GE channel model parameters are unanchored and the "27% intra-cycle recovery" finding is a direct consequence of the coherence assumption.**

The paper acknowledges this (Section IV-C: "direct consequence of the per-cycle GE coherence assumption, not an emergent finding") but still presents it as a result. The sensitivity sweep (Fig. 3b) is valuable, but without any ISL channel measurements, the default parameters are arbitrary. The physical mapping (structural shadowing, antenna mispointing) is qualitative and not supported by references to ISL propagation measurements.

*Why it matters:* The ARQ infeasibility conclusion and the 35 kbps recommendation both depend on the GE parameterization. If the actual ISL channel has faster mixing (τ_c ≪ T_c), intra-cycle ARQ is effective and 30 kbps may suffice.

*Remedy:* Present the GE analysis as a "what-if" design tool rather than a predictive model. Emphasize the sensitivity sweep as the primary output. Add references to any available ISL propagation data (e.g., EDRS optical link statistics, even if not directly applicable to S-band). Consider whether the Lutz et al. parameters (designed for land-mobile satellite channels) are appropriate for ISL channels and discuss the differences.

---

## Minor Issues

1. **Notation inconsistency:** α_RX is described as "derived from schedule" (Table I) but also appears as an input in some equations. Clarify that it is always computed, never assumed.

2. **Table III footnote (a):** The collision avoidance rate of 10⁻⁴/node/s is described as a "conservative upper bound" but is 300× higher than the ESA-reported rate. "Stress-test parameter" would be more accurate than "conservative."

3. **Eq. 6 (η_consensus):** The formula assumes serialized Raft votes over the shared channel, but the text doesn't discuss whether this serialization is realistic under TDMA scheduling. How are Raft rounds scheduled within the superframe?

4. **Section IV-A, "thundering herd" footnote:** The BEB analysis assumes Slotted ALOHA, but the paper's primary MAC is TDMA. Clarify when the system would actually use Slotted ALOHA (only during coordinator failure recovery?).

5. **Table VI (superframe):** The ACK mini-slot (0.5 ms) is described as fitting within the "jitter sub-slot" of the 4.7 ms guard. This is a tight design; if the jitter budget is consumed by actual jitter, the ACK may be corrupted. Discuss robustness.

6. **Algorithm 1, line 3:** η₀ = 5% is hardcoded. Should this be a parameter for non-hierarchical topologies?

7. **Abstract:** "CCSDS Proximity-1 framing anchors γ ≈ 0.70–0.76 (rate-dependent; γ₃₀ = 0.745 at 30 kbps, γ₂₄ = 0.761, γ₅₀ = 0.695)" — this level of detail in the abstract is unusual and may confuse readers unfamiliar with the notation.

8. **Section II-B:** The SWIM reference [das_swim] is for failure detection in distributed systems, not spacecraft. The connection should be made explicit.

9. **Eq. 14 (γ time-domain):** T_framing = O_frame / (R_FEC · R_PHY) assumes framing bits are FEC-encoded. This is stated but should be verified against CCSDS 211.0-B-6 (Proximity-1 encodes the entire transfer frame including header).

10. **Data availability:** The repository tag "paper-02-v-ct" suggests multiple paper versions. Ensure the final tag matches the published version.

11. **Fig. 2 caption:** "Star: CCSDS default" and "Diamond: conservative" — verify these markers are distinguishable in grayscale printing.

12. **Section III-B-2:** "Each cluster coordinator sends a single 512-byte summary per cycle" — the breakdown (48+48+13+32+371 = 512 B) allocates 371 B to "metadata/CRC," which seems disproportionate. Is this padding? If so, the summary could be compressed.

13. **Eq. 3 (hierarchical messages):** This counts messages but not bytes; the byte accounting is done separately. A unified byte-budget equation would be cleaner.

14. **Section V-C, γ-conditional PHY lookup:** The ranges [0.65, 0.70], [0.70, 0.80], [0.80, 0.90] have boundary ambiguity. Use consistent interval notation (e.g., half-open intervals).

---

## Overall Recommendation
**Recommendation: Major Revision**

This manuscript makes a credible attempt at a difficult problem: providing actionable sizing equations for hierarchical coordination in large spacecraft swarms. The two-layer feasibility framework is logically sound, the campaign duty factor appropriately addresses workload realism, and the CCSDS-grounded γ derivation (replacing the earlier 0.85) is consistently applied throughout. The paper's transparency about limitations—particularly the explicit validation gap acknowledgment, the V&V tier structure, and the honest claim map (Table IX)—sets a commendable standard for preliminary design studies.

However, the paper's central weakness is the absence of any external validation, which limits all results to "preliminary design estimates" (the authors' own characterization). The DES verification is tautological by construction; the packet-level γ derivation is parameter estimation from the same equations; and the GE channel model uses unanchored assumptions. The fleet-level scaling claims exceed the validated scope. The manuscript is also excessively long for its validated content, with substantial space devoted to reporting DES results that confirm the analytical equations by construction.

For a major revision, the authors should: (1) condense the DES reporting to distributional analysis only; (2) restrict fleet-level claims to preliminary projections; (3) present the GE analysis as a design tool with sensitivity sweeps as the primary output; (4) add a consolidated sensitivity analysis over C_node; and (5) consider whether a shorter, more focused paper on the per-cluster sizing framework (with the fleet-level extension as future work) would be more appropriate for the target journal. If even one external data point (NS-3 MAC simulation, modem γ measurement, or ISL channel statistics) could be added, it would substantially strengthen the contribution.

## Constructive Suggestions (ordered by impact)

1. **Add one external validation point.** Even a simple NS-3 simulation of the TDMA superframe with a Proximity-1-like PHY model would elevate the entire paper from "preliminary design estimate" to "simulation-validated framework." This is the single highest-impact improvement.

2. **Consolidate the C_node sensitivity into a primary result.** Present a figure showing η_total vs. C_node for d ∈ {0.01, 0.10, 0.50, 1.0}, with feasibility boundaries marked. This would make the paper immediately useful to practitioners with different link budgets.

3. **Shorten the paper by 20–30%.** Remove redundant DES mean-value comparisons, consolidate the two slot-timing models into a single presentation with Model S as a brief comparison, and reduce inline caveats (move to a consolidated limitations section).

4. **Restructure Section IV-A.** Separate the rate ladder derivation (currently clear in Table IV) from the slot-level simulation results, link budget, and design recommendations. Each should be a distinct subsection.

5. **Provide a one-page "practitioner's guide"** (possibly as an appendix) that walks through Algorithm 1 with a concrete example different from the default parameters, showing how to adapt the framework to a specific mission.

6. **Strengthen the GE physical mapping.** Reference any available ISL propagation data, even from optical links or different frequency bands, to provide at least qualitative anchoring for the coherence time assumption.

7. **Discuss the generalized γ expression's utility more explicitly.** Equation 14 is potentially the most reusable contribution; show 3–4 worked examples for different link types (already partially done in Section IV-J) in a consolidated table with clear input/output formatting.