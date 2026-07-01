---
paper: "02-swarm-coordination-scaling"
version: "cm"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-03-03"
recommendation: "Unknown"
---



# Peer Review: Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms

## 1. Significance & Novelty
**Rating: 3 (Adequate)**

The paper addresses a genuine gap: closed-form parametric sizing for hierarchical coordination at the 10³–10⁵ node scale with byte-level traffic accounting. The two-layer feasibility framework (byte budget + TDMA airtime) and the generalized γ expression are potentially useful contributions for preliminary mission design. However, the novelty is tempered by several factors: (a) the core analytical results are relatively straightforward engineering calculations (message counting, slot timing, geometric AoI) rather than fundamentally new theory; (b) the absence of any external validation limits the paper's impact to a design methodology rather than validated engineering guidance; (c) the practical applicability is narrow—the TDMA analysis is binding only for the 1 kbps RF-backup channel (<1% of operational lifetime), while at ≥10 kbps everything is trivially feasible. The campaign duty factor and GE sensitivity sweep are useful framing contributions, but the paper's core value proposition—that hierarchical coordination overhead is manageable—is perhaps unsurprising given the aggregation ratios involved.

## 2. Methodological Soundness
**Rating: 3 (Adequate)**

The three-layer verification structure (analytical → DES → slot-sim) is well-conceived, and the authors are commendably transparent about what each tier does and does not demonstrate. However, several methodological concerns persist:

The DES operates at message-layer granularity with cycle-aggregated updates, which by construction reproduces the analytical equations. The authors acknowledge this (Tier 1 verification), but the DES distributional analysis—its claimed primary incremental contribution—is itself conditioned on the same message model and GE parameterization. The bimodal buffer CDF (Fig. 5) is a direct consequence of the ON/OFF campaign model, not an emergent finding.

The slot-level simulator reveals the ARQ×TDMA coupling (52.7% deadline misses), which is a genuinely useful finding. However, this simulator still operates under idealized assumptions (perfect synchronization, no multi-access interference, deterministic slot boundaries).

The packet-level γ derivation from CCSDS Proximity-1 framing is a parameter anchoring exercise, not independent validation. The authors correctly characterize it as such, but the paper's length devoted to this derivation may overstate its contribution.

The GE channel model is applied with per-cycle state transitions, which is a significant simplification. The coherence-time sensitivity analysis (Fig. 4) partially addresses this, but the mapping from physical mechanisms to GE parameters (Table IV) is speculative without ISL measurements.

## 3. Validity & Logic
**Rating: 4 (Good)**

The internal logic is generally sound and self-consistent. Several specific improvements are evident in this version:

- The campaign duty factor (d) adequately addresses workload realism. The decomposition η = η₀ + d·η_cmd with worked examples (orbit-raising, station-keeping, collision avoidance) and the reverse-derived example (d = 0.0016) convincingly demonstrate that routine operations occupy η ≈ 5–10%. The stress case (η_S ≈ 46%) is now properly contextualized as a continuous-duty upper bound that is episodic in practice.

- The gamma unification appears consistently applied: γ₂₄ = 0.761 and γ₃₀ = 0.745 from CCSDS Proximity-1 framing replace the earlier 0.85 throughout. The time-domain form (Eq. 14) is authoritative; the multiplicative decomposition is correctly labeled as pedagogical. I verified dimensional consistency of Eq. 13.

- The three-layer feasibility framework is logically coherent, with the explicit warning against double-counting (mapping η_total/γ as screening heuristic, not design criterion) being a valuable clarification.

- The claim that commands are "topology-invariant" is correctly qualified as holding only under centralized broadcast semantics, with the Raft consensus alternative quantified (Eq. 5).

One logical concern: the paper claims the framework applies to "deep-space swarms where 1–10 kbps is the operational norm," but the GE model, link budget, and orbital dynamics are all parameterized for LEO. This generalization is unsupported.

## 4. Clarity & Structure
**Rating: 3 (Adequate)**

The paper is extraordinarily detailed—perhaps excessively so for a journal article. At its current length, it reads more like a technical report than a focused journal paper. The notation table (Table I) is helpful, but the sheer number of parameters, tables (15+), figures (7+), and cross-references makes navigation difficult.

Strengths: The roadmap paragraph at the start of Section IV is helpful. The rate ladder (Table VII) and Algorithm 1 are excellent practitioner-facing summaries. The claim map (Table XIII) is unusually transparent and commendable.

Weaknesses: The paper repeatedly states the same caveats (e.g., "no external validation exists" appears in at least 5 places). While transparency is valued, this repetition consumes space. The distinction between Model S and Model C, while important, is introduced in the introduction, re-explained in Section IV-A, and re-referenced throughout—a single definitive treatment would suffice. Several footnotes contain substantive technical content that should be in the main text or removed.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**

The paper is exemplary in its transparency: data availability with tagged repository, explicit AI disclosure, clear acknowledgment of validation gaps, and honest characterization of evidence tiers. The claim map (Table XIII) is a model for the field. The acknowledgment that "predictive accuracy for real ISL channels is unknown" is refreshingly candid.

## 6. Scope & Referencing
**Rating: 3 (Adequate)**

The reference list is broad (50+ references) covering constellation management, swarm robotics, distributed systems, queueing theory, and CCSDS standards. However, several gaps exist:

- No references to actual ISL measurement campaigns (e.g., EDRS, LCRD, or Starlink ISL performance reports), which would strengthen the GE parameterization discussion.
- The DVB-RCS2 comparison (γ ≈ 0.70–0.85) is mentioned but not deeply engaged with—this is the closest operational analogue and deserves more analysis.
- Network calculus (Le Boudec) is cited but dismissed as "future work" without explaining why the deterministic worst-case approach might be more appropriate for safety-critical coordination than the mean-value approach taken here.
- Missing references to recent work on LEO constellation autonomous coordination (e.g., Kulu's NewSpace database for fleet sizes, or ESA's OPS-SAT autonomous operations).

The paper is appropriate for IEEE TAES in scope, though the contribution may be better suited to a shorter format (letter or correspondence) given the preliminary nature of the validation.

## Major Issues

1. **The DES verification provides limited value beyond confirming its own equations.**
   - The authors acknowledge this (Tier 1), but the DES still occupies significant paper real estate. The distributional tail analysis (Fig. 5) is the claimed incremental contribution, yet the bimodal CDF is a direct, predictable consequence of the ON/OFF campaign model—not an emergent finding requiring simulation. The ~44% P99 increase over Bernoulli under cluster-correlated campaigns could be derived analytically from the MMPP/D/1 framework the authors themselves identify.
   - *Why it matters:* The paper's length is already excessive; space devoted to DES verification of known equations could be better used for deeper analysis of genuinely uncertain aspects (e.g., MAC contention, antenna scheduling).
   - *Remedy:* Reduce DES coverage to a single paragraph confirming <0.1% agreement, plus the buffer CDF figure. Move distributional analysis to supplementary material or derive the MMPP/D/1 tail bounds analytically.

2. **The packet-level validation (Section IV-J) provides parameter anchoring, not independent validation.**
   - The γ derivation from CCSDS framing is useful but is fundamentally a calculation exercise: given known frame formats and assumed guard/acquisition times, compute slot efficiency. This does not validate the sizing *framework*—it validates one *input parameter*. The cross-model consistency (Table XIV, all models agree on 9,078 ms) is expected by construction since all implement the same equations.
   - *Why it matters:* The paper's validation narrative may mislead readers into thinking the framework has been independently verified at the physical layer.
   - *Remedy:* Rename Section IV-J to "Physical-Layer Parameter Derivation" (already partially done). Remove the "Cross-Model Consistency" subsection or reduce to a single sentence. Be explicit that the only genuinely emergent finding from the multi-tool approach is the ARQ×TDMA coupling (52.7% misses).

3. **The framework's practical utility is undermined by its narrow binding regime.**
   - The TDMA schedulability analysis (Layer 2) is binding *only* for the 1 kbps RF-backup channel at k_c = 100, which the authors state represents <1% of operational lifetime. At ≥10 kbps, both layers are trivially satisfied (η_total < 7.1%, margin > 90%). This means the elaborate TDMA analysis—the paper's most technically interesting contribution—applies to a corner case.
   - *Why it matters:* Reviewers and practitioners need to understand whether the framework justifies its complexity for the regimes where it matters most.
   - *Remedy:* Either (a) reframe the paper around the RF-backup/deep-space regime where the analysis is binding, with the ≥10 kbps case as a brief corollary; or (b) extend the analysis to scenarios where Layer 2 is binding at higher rates (larger k_c, shorter T_c, higher-rate status reports, multi-hop relay).

4. **Absence of MAC contention analysis weakens the TDMA claims.**
   - The paper assumes perfect TDMA scheduling (deterministic slot assignment, no contention) but acknowledges that "contention performance is not evaluated and would require NS-3." For a paper recommending specific PHY rates (35 kbps) for safety-critical coordination, the absence of any contention analysis is a significant gap. The thundering-herd analysis (Slotted ALOHA with BEB) is a rough estimate, not a validated model.
   - *Why it matters:* Real TDMA systems experience slot collisions from clock drift, hidden terminals, and multi-cluster interference. The 730 ms margin at 30 kbps could be consumed by these effects.
   - *Remedy:* At minimum, provide a sensitivity analysis showing how much contention-induced slot waste the 730 ms margin can absorb (e.g., what fraction of slots can be wasted before deadline misses occur). Ideally, include a simplified NS-3 or analytical contention model for a 10-node cluster.

5. **The GE parameterization lacks empirical grounding.**
   - The default parameters (p_BG = 0.50, p_B = 0.90) are described as "illustrative" with no ISL measurements available. The physical mechanism mapping (Table IV) is speculative. The paper states "actual P95 recovery could be ~3× higher or lower depending on measured channel statistics"—this is a very wide uncertainty band for a design recommendation.
   - *Why it matters:* The 35 kbps recommendation depends critically on the GE parameterization through the ARQ viability analysis. If p_BG is actually 0.10 (antenna mispointing), P95 recovery is 12–18 cycles, fundamentally changing the design.
   - *Remedy:* (a) Cite any available ISL or proximity-link measurement data (EDRS, LCRD, Mars relay); (b) present the design recommendation as conditional on GE parameters rather than as a single point; (c) provide a table mapping measured channel statistics to recommended PHY rates.

## Minor Issues

1. **Inconsistent γ subscripting.** The paper uses γ₂₄, γ₃₀, γ_C,24, γ_C,30, γ_S, and unsubscripted γ. While Table I defines the convention, consistent notation throughout would improve readability.

2. **Table I notation density.** Several symbols (α_RX, q, L_cmd) are defined with forward references to equations not yet introduced. Consider splitting into "primary" and "derived" notation tables.

3. **Eq. 13 unit conversion.** The 10⁻³ factor converting ms·bps to bits is error-prone. The authors recommend the time-domain form (Eq. 14)—consider presenting only Eq. 14 in the main text and relegating Eq. 13 to an appendix.

4. **"Project Dyson Research Team" authorship.** IEEE requires individual author names. The footnote acknowledges this but should be resolved before publication.

5. **Non-archival references.** References [3] (Amazon Kuiper), [18] (DARPA OFFSET), [19] (DoD Replicator), and [22] (DARPA Blackjack) are non-archival web pages. Replace with archival sources where possible.

6. **Fig. 1 not shown.** The architecture diagram (Fig. 1) is referenced but its content cannot be evaluated from the LaTeX source alone.

7. **Section III-B-2 coordinator self-exclusion.** The footnote explaining the 0.5 pp gap between analytical η₀ (5.6%) and DES (5.0%) is substantive and should be in the main text.

8. **"Stress-case" terminology.** The paper alternates between "stress-case," "stress case," and "stress bound." Standardize.

9. **Algorithm 1 line 2.** The hardcoded 0.205 should reference the baseline definition for clarity.

10. **Table II AoI column.** The footnote "AoI depends on p_exc and T_c, not C_node" is important and should be more prominent—perhaps a separate remark.

11. **Deep-space applicability claim** (Introduction, last paragraph of contributions): "The framework also applies to deep-space swarms where 1–10 kbps is the operational norm" is unsupported. Deep-space links have fundamentally different propagation delays, Doppler profiles, and link margins. Either justify or remove.

12. **Eq. 6 (η_consensus):** The variable N_R is undefined. Presumably it is the number of Raft rounds, but this should be stated.

## Overall Recommendation
**Recommendation: Major Revision**

This paper presents a well-structured parametric sizing framework for hierarchical coordination in large space swarms, with commendable transparency about its limitations and validation gaps. The two-layer feasibility decomposition (byte budget + TDMA airtime), the campaign duty factor parameterization, and the generalized γ expression are useful contributions for preliminary mission design. The CCSDS-grounded γ derivation (0.76, replacing the earlier 0.85) is consistently applied and well-justified. The stress-case contextualization via the duty factor is a significant improvement that makes the overhead figures operationally meaningful.

However, the paper suffers from three fundamental issues that require major revision. First, the framework's most interesting technical content (TDMA schedulability) applies only to a narrow corner case (<1% of operational lifetime at 1 kbps), undermining the practical significance. Second, the multi-tool verification approach (DES + slot-sim + packet-sim) is largely self-confirming, with only the ARQ×TDMA coupling representing a genuinely emergent finding. Third, the absence of any MAC contention analysis or empirical channel data means the specific PHY rate recommendation (35 kbps) rests on unvalidated assumptions. The paper would benefit substantially from either narrowing its scope to the binding regime with deeper analysis, or broadening the binding regime by considering more demanding scenarios. The current version is too long for a journal article given its validation maturity.

## Constructive Suggestions

1. **Condense by ~30%.** Eliminate redundant caveats, reduce DES verification to essentials, merge Model S/C discussion into a single treatment. Target 10–12 pages.

2. **Reframe around the binding regime.** Lead with the insight that at ≥10 kbps coordination is trivially feasible, then focus the technical depth on the RF-backup/deep-space regime where the framework provides genuine value. This sharpens the contribution.

3. **Add a contention margin analysis.** Even without NS-3, compute how many slot collisions the 730 ms margin absorbs. This converts an acknowledged gap into a quantified design margin.

4. **Make the PHY recommendation conditional.** Present Table: {if measured γ ∈ [0.65, 0.70] → 40 kbps; [0.70, 0.80] → 35 kbps; [0.80, 0.90] → 30 kbps}. This is more useful than a single-point recommendation.

5. **Seek partial external anchoring.** DVB-RCS2 slot efficiencies, EDRS/LCRD link statistics, or even terrestrial TDMA measurements would significantly strengthen the paper. Even a qualitative comparison would help.

6. **Derive the MMPP/D/1 tail bounds.** The authors identify this as future work but have all the ingredients. Replacing the DES distributional analysis with an analytical tail bound would be a stronger contribution.

7. **Add a "quick-start" summary table.** For practitioners: given {k_c, S, T_c, FEC rate, acquisition model}, read off {minimum PHY rate, margin, stagger cycles}. Algorithm 1 partially serves this role but a pre-computed table for common configurations would be more accessible.