---
paper: "02-swarm-coordination-scaling"
version: "dh"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-03-06"
recommendation: "Unknown"
---



# Peer Review: "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version DH)

---

## 1. Significance & Novelty
**Rating: 3 (Adequate)**

The paper addresses a genuine gap: closed-form per-cluster sizing equations for hierarchical coordination at scales of 10³–10⁵ nodes with byte-level traffic accounting. The two-test feasibility framework (byte budget + TDMA airtime) is a useful conceptual contribution. However, the novelty is tempered by several factors: (a) the individual equations are straightforward applications of standard TDMA analysis, queueing theory, and AoI formulas—the contribution is their assembly rather than any single analytical advance; (b) the CCSDS-grounded γ parameterization, while carefully executed, is acknowledged as a standard slot-efficiency formula (cf. DVB-RCS2); (c) the paper's value proposition rests heavily on the claim that no prior work combines autonomous coordination + byte-level accounting + 10⁴–10⁵ scale, but the analysis remains entirely per-cluster (k_c = 50–500), making the "large swarm" framing somewhat aspirational. The campaign duty factor d is a sensible and practical parameterization that meaningfully contextualizes the stress-case results.

## 2. Methodological Soundness
**Rating: 3 (Adequate)**

The three-layer feasibility framework (byte budget, MAC efficiency, TDMA airtime) is logically structured, and the paper is commendably transparent about what each layer does and does not prove. However, several methodological concerns arise:

- The DES is cycle-aggregated and shares the same equations as the analytical model, so the <0.1% agreement is tautological (acknowledged as Tier 1). The claimed "incremental value" of distributional tails under campaign burstiness is asserted but not convincingly demonstrated—no tail distributions are actually shown in figures or tables beyond the buffer sizing heuristic (M = 1.30).
- The slot-level simulator provides genuine value in revealing the ARQ×TDMA coupling (52.7% miss rate), but operates only under Model S timing for the joint interaction table, limiting its direct applicability to design recommendations.
- The GE channel model is appropriately framed as a what-if tool, but the default parameterization (p_BG = 0.50, p_B = 0.90) is acknowledged as having no ISL measurement basis. The sensitivity curves partially mitigate this, but the paper's quantitative recommendations (e.g., "35 kbps recommended") are conditioned on these unvalidated parameters.
- The M/D/1 centralized baseline and O(N²) mesh bound are useful reference points but are intentionally simplified (compute-bound, not spectrum-bound for centralized; full-state gossip for mesh). This makes the topology comparison somewhat asymmetric.

## 3. Validity & Logic
**Rating: 3 (Adequate)**

The internal logic is generally sound, and the paper is careful about distinguishing information-rate from PHY-rate, Model S from Model C, and computed outputs from free parameters. Specific concerns:

- **γ unification:** The paper states γ ≈ 0.73–0.76 across 24–35 kbps (Model C), replacing an earlier 0.85. The consistency ledger in Table IX is helpful. However, I found one potential inconsistency: Eq. (6) gives γ_S = 0.949 at 24 kbps, and the abstract mentions γ ≈ 0.73–0.76, but the notation table lists γ₂₄ = 0.761, γ₃₀ = 0.745, γ₃₅ = 0.732—all Model C. The paper is generally consistent, but the dual-model presentation (Model S vs. Model C) creates cognitive overhead and opportunities for reader confusion despite the clear labeling.

- **Stress-case contextualization:** The η_S ≈ 46% is now properly framed as a continuous-duty upper bound occurring <1% of operational time, with the yearly mixture calculation (η̄ = 5.6%) providing good context. This is a significant improvement.

- **α_RX circularity:** The paper correctly notes that α_RX is a computed output, not a free parameter. However, the heuristic R_PHY,min ≥ C_coord,info / (γ · α_RX) creates a circular dependency since α_RX depends on R_PHY. Algorithm 1 resolves this iteratively (line 8: "increase R_PHY; repeat"), but this should be stated more explicitly as a fixed-point iteration with guaranteed convergence (which it has, since T_ing is monotonically decreasing in R_PHY).

- **Static cluster assumption:** The J2 analysis for dynamic topology is appreciated but cursory. The claim that cross-plane re-association adds <0.5% overhead relies on a single Walker constellation geometry; heterogeneous orbits could produce substantially different results.

## 4. Clarity & Structure
**Rating: 4 (Good)**

The paper is well-organized with a clear roadmap. The notation table is comprehensive. The two-test framework box is effective. The rate ladder (Table IV) and γ-conditional lookup (Table IX) are genuinely useful for practitioners. Several clarity issues remain:

- The paper is extremely dense—nearly every paragraph introduces a quantitative result, caveat, or cross-reference. While thoroughness is valued, the density makes it difficult to extract the core contribution. A reader seeking to use Algorithm 1 must navigate ~15 pages of context.
- The dual-model presentation (Model S / Model C) is well-labeled but adds complexity. Since Model S is explicitly "not for recommendations," consider relegating it entirely to an appendix.
- Some figures are referenced but not shown in the manuscript text (the PDF generation would need to be verified). The descriptions suggest they exist, but reviewers cannot assess figure quality without seeing them.
- The thundering-herd analysis (Section III-B-2) is interesting but feels like a tangent—it addresses a failure mode that occurs <1/yr per cluster and is not integrated into the feasibility framework.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**

The paper is exemplary in its transparency: explicit V&V tiers with honest acknowledgment that no external validation exists; clear AI disclosure; open-source code with tagged release; reproducible MC configuration. The claim map (Table XII) is a model of intellectual honesty. The "preliminary design estimates" qualifier is consistently applied.

## 6. Scope & Referencing
**Rating: 3 (Adequate)**

The reference list covers the major relevant areas (CCSDS standards, AoI theory, swarm robotics, constellation management, distributed systems). However:

- Several references are non-archival (Amazon Kuiper overview, DARPA program pages, DoD fact sheets). While understandable for context, these weaken the scholarly foundation.
- The paper does not cite recent work on distributed TDMA scheduling for satellite networks (e.g., work by Radhakrishnan et al. on distributed resource allocation for small satellite networks, or Marchese et al. on inter-satellite link scheduling).
- Network calculus [Le Boudec] is cited but not used; the paper could benefit from comparing its mean-value approach against deterministic worst-case bounds.
- The DVB-RCS2 comparison is valuable but brief; a more detailed comparison of the γ parameterization against measured DVB-RCS2 terminal efficiencies would strengthen the standards-based anchoring.

---

## Major Issues

1. **The DES provides negligible independent validation beyond confirming its own equations.**
   - *Why it matters:* The paper's V&V framework honestly acknowledges this (Tier 1), but the DES still occupies significant manuscript real estate. The claimed "incremental contribution" of distributional tails is not substantiated with figures or quantitative tail analysis beyond the buffer sizing factor (M = 1.30 at d = 0.10).
   - *Remedy:* Either (a) present actual tail distribution plots (CDF of per-cycle overhead, buffer occupancy distributions) showing where the DES reveals behavior not predicted by the analytical model, or (b) significantly reduce the DES discussion and reframe it purely as a code-correctness check. The current middle ground overstates the DES's contribution.

2. **The packet-level validation (Section IV-J) is parameter anchoring, not validation.**
   - *Why it matters:* Computing γ from CCSDS framing specifications and then using that γ in the same sizing equations is a self-consistent parameterization, not an independent check. The paper acknowledges this ("standards-based parameter estimate, not a measurement") but still lists it as "Tier 2" evidence in Table XII, which overstates its epistemic status.
   - *Remedy:* Relabel the CCSDS γ derivation as "standards-based parameterization" throughout (including Table XII column header). Reserve "Tier 2" for the slot-sim's ARQ×TDMA coupling result, which genuinely reveals emergent behavior. Alternatively, compare the derived γ against published DVB-RCS2 measured efficiencies to provide a genuine external anchor.

3. **The generalized γ expression (Eq. 14) has limited practitioner utility without hardware measurements.**
   - *Why it matters:* The measurement protocol (Section V-D) is well-specified, but until hardware measurements exist, the γ values are computed from assumed timing parameters (T_acq = 5 ms, T_guard = 4.7 ms). The sensitivity analysis (γ₃₀ ∈ [0.72, 0.78]) partially addresses this, but the ±0.07 range translates to a 6 kbps range in R_PHY,min—significant relative to the 5 kbps gap between the minimum (30 kbps) and recommended (35 kbps) rates.
   - *Remedy:* Explicitly state that the 35 kbps recommendation is robust to the full γ uncertainty range (which it appears to be from Table X), and provide a simple closed-form expression for ∂R_PHY,min/∂γ so practitioners can propagate their measured γ uncertainty to PHY rate selection without re-running Algorithm 1.

4. **Fleet-level claims are unsupported by per-cluster analysis.**
   - *Why it matters:* The title mentions "large autonomous space swarms" and the introduction discusses 10⁵–10⁶ nodes, but all analysis is per-cluster (k_c = 50–500). Fleet-level reuse (Eq. 10, R = 7) is a single analytical estimate with no multi-interferer simulation. The spatial reuse analysis (Section IV-A-1) acknowledges this but the gap between per-cluster sizing and fleet-level feasibility is substantial.
   - *Remedy:* Either (a) scope the title and claims to "per-cluster sizing" explicitly, or (b) provide at minimum a parametric fleet-level analysis showing how many simultaneous clusters can operate under the R = 7 reuse assumption across representative constellation geometries (even analytically, using orbital shell geometry).

5. **The topology comparison is asymmetric and potentially misleading.**
   - *Why it matters:* The centralized baseline is intentionally compute-bound (not spectrum-bound), making it appear to scale to 10⁶. The mesh baseline uses full-state gossip (O(N²)), which no real system would implement. These are acknowledged as "intentional bounds," but the comparison in Section IV-G could mislead readers into thinking hierarchy is necessary when a properly designed centralized system with selective forwarding might suffice.
   - *Remedy:* Add a brief discussion of intermediate architectures (e.g., centralized with regional aggregation, or partial-state mesh with bounded neighborhood) to show where hierarchy becomes genuinely advantageous. Alternatively, strengthen the argument for why the chosen baselines are the right comparison points.

## Minor Issues

1. **Eq. (1) counts messages but the overhead metric η counts bytes.** The connection between M_total and η should be made explicit (multiply by respective message sizes and divide by budget).

2. **Table I notation:** The entry for α_RX says "Example: 0.908 at 30 kbps, M_r = 0" but the superframe table shows this is for Model C. Specify the model.

3. **Section III-B-2 (thundering herd):** The Slotted ALOHA analysis assumes all 100 nodes simultaneously attempt election, but Raft has a randomized election timeout specifically to prevent this. The analysis should note that Raft's built-in randomization reduces G significantly below 25.

4. **Table III (Simulation Parameters):** The collision avoidance rate of 10⁻⁴/node/s is described as a "conservative upper bound" but is 300× higher than the ESA figure cited in the footnote. "Stress-test parameter" would be more accurate than "conservative."

5. **Algorithm 1, Line 3:** The formula computes η_total but the variable name suggests it includes baseline. The comment says "baseline = 20.5%" but the formula adds η_baseline separately. Verify the formula matches the canonical definition (Eq. 5).

6. **Section IV-B (AoI):** The geometric distribution assumption for exception reporting is memoryless, but real exception triggers (threshold crossings) are correlated with state evolution. The paper notes this ("threshold-triggered or correlated reporting would differ") but could quantify the impact with a simple Markov-modulated reporting model.

7. **Table VII (Duty Mapping):** Collision avoidance is listed as d = 1.0 "during event" with a footnote saying "background d < 0.01." This is confusing—d should represent the fraction of time in the phase, not the intensity during the phase. Clarify whether d = 1.0 means "every cycle has a command during the CA event window."

8. **References:** [12] (Dorigo ACO), [13] (Kennedy PSO), [14] (Karaboga ABC) are cited in the bibliography but do not appear to be referenced in the text. Remove or add citations.

9. **The abstract is 197 words but contains highly specific numbers** (0.73–0.76, 35 kbps, 20 kbps, 5 ms, 4.7 ms, 46%, <1%). Consider a more concise abstract focusing on the framework and key findings rather than parameter values.

10. **Eq. (14) framing term:** T_framing = O_frame / (R_FEC · R_PHY) implies framing bits are FEC-encoded. This is stated as "per CCSDS standard practice" but CCSDS Proximity-1 applies coding to the entire transfer frame including header. Confirm this is consistent with the 104-bit framing overhead in Table VIII.

---

## Overall Recommendation
**Recommendation: Major Revision**

This manuscript makes a credible contribution by assembling a two-test feasibility framework for per-cluster coordination sizing in hierarchical space swarms, with careful CCSDS-grounded parameterization and commendable transparency about validation limitations. The campaign duty factor d effectively addresses earlier concerns about workload realism, and the stress-case (η_S ≈ 46%) is now properly contextualized as an episodic upper bound. The γ unification around 0.73–0.76 (Model C) is consistently applied throughout, and the rate ladder from information-rate to PHY recommendation is a genuinely useful practitioner tool.

However, the paper suffers from a significant gap between its ambitious framing (large autonomous space swarms, 10⁵–10⁶ nodes) and its actual analytical scope (per-cluster, k_c = 50–500, static membership, no external validation). The DES verification provides minimal value beyond code correctness, and the packet-level γ derivation—while carefully executed—is parameter anchoring rather than independent validation. The topology comparison uses intentionally extreme baselines that may not represent realistic alternatives. The manuscript would benefit from either scoping its claims more tightly to match its evidence, or providing additional analysis (fleet-level reuse, intermediate architectures, measured γ comparison) to support its broader framing.

The paper's greatest strength is its intellectual honesty: the claim map, V&V tiers, and explicit "no external validation" disclaimers set a high standard for preliminary design studies. With revisions addressing the fleet-level gap, DES contribution, and validation tier labeling, this could become a useful reference for the space systems community.

## Constructive Suggestions (ordered by impact)

1. **Tighten scope to match evidence:** Retitle to emphasize "per-cluster sizing" rather than "large autonomous space swarms." This immediately resolves the fleet-level gap and sets appropriate expectations.

2. **Strengthen the DES contribution or reduce its footprint:** Present actual distributional results (tail CDFs, buffer occupancy under campaign bursts) that the analytical model cannot produce, or compress the DES discussion to a single paragraph confirming code correctness.

3. **Provide a closed-form sensitivity expression for γ → R_PHY,min:** Something like ∂R_PHY,min/∂γ ≈ −C_coord,info/(γ² · α_RX) would let practitioners propagate hardware-measured γ uncertainty without re-running the algorithm.

4. **Add one intermediate topology baseline:** A centralized system with regional aggregation (similar to the hierarchy but without autonomous coordination) would show where the hierarchical overhead is actually justified.

5. **Consolidate Model S into an appendix:** Since it is explicitly "not for recommendations," moving it out of the main flow would reduce cognitive load and eliminate a persistent source of potential confusion.

6. **Quantify the fleet-level reuse claim:** Even a simple analytical treatment showing the number of simultaneous active clusters under R = 7 for 2–3 representative constellation shells would substantially strengthen the scalability argument.

7. **Relabel Table XII evidence tiers:** "Standards-based parameterization" for the CCSDS γ column; reserve "Tier 2" for genuinely emergent simulation results (ARQ×TDMA coupling).