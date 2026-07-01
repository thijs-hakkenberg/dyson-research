---
paper: "02-swarm-coordination-scaling"
version: "cd"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-28"
recommendation: "Unknown"
---



# Peer Review: Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms (Version CD)

---

## 1. Significance & Novelty
**Rating: 3 (Adequate)**

The paper addresses a genuine gap: closed-form sizing equations for hierarchical coordination at the $10^3$–$10^5$ node scale with byte-level traffic accounting. This is a useful contribution for systems engineers designing large constellations. However, the novelty is tempered by several factors. The core analytical results (overhead decomposition, coordinator ingress sizing) are relatively straightforward traffic accounting exercises—the equations follow directly from message sizes and rates. The more interesting contributions (GE correlated loss characterization, three-layer feasibility framework, campaign duty factor) are incremental extensions of well-known techniques (Gilbert-Elliott models, TDMA scheduling theory) applied to a specific domain. The paper does not introduce new algorithms, protocols, or coordination strategies; it sizes an assumed architecture. This is valuable engineering work but sits below the novelty threshold typical of IEEE T-AES research contributions.

## 2. Methodological Soundness
**Rating: 3 (Adequate)**

The three-layer feasibility framework (byte budget → MAC efficiency → TDMA airtime) is logically structured and the decomposition is sound in principle. The standards-grounded γ derivation from CCSDS Proximity-1 framing (Section IV-J) is a welcome improvement over assumed values—the multiplicative decomposition (Eq. 14) is clean and the resulting γ = 0.76 is well-justified. The campaign duty factor *d* is a sensible parameterization that substantially addresses earlier concerns about workload realism; the stress-case (η_S ≈ 46%) is now properly contextualized as a continuous-duty upper bound (d = 1), with realistic operations at d = 0.01–0.10 yielding η ≈ 5–10%.

However, methodological concerns remain:

- The DES verification provides limited independent value. By the authors' own admission, the DES implements the same accounting equations as the closed-form expressions, so <0.1% agreement is "expected by construction." The distributional analysis (Fig. 8) is the DES's genuine contribution, but this could be obtained analytically for the Bernoulli model and via straightforward Markov-chain analysis for the ON/OFF model.
- The cycle-aggregated simulation granularity (10 s steps) cannot resolve sub-cycle dynamics, yet several claims (e.g., coordinator queueing latency of ~260 ms) require sub-cycle resolution.
- The static topology assumption over a 1-year simulation is acknowledged but inadequately addressed. The J2 perturbation analysis (Section V-B) is cursory—a single Walker constellation geometry does not establish generality.

## 3. Validity & Logic
**Rating: 3 (Adequate)**

The internal consistency is generally good. The γ = 0.76 value is now consistently applied throughout (Tables V, VI, VII, VIII; Eqs. 5, 7), replacing the earlier 0.85—this is a significant improvement. The three-layer feasibility check (Table IX) correctly identifies that stress unicast passes byte budget but fails half-duplex airtime, which is a genuinely useful insight.

Logical concerns:

1. **Circular validation structure.** The paper presents four "verification tiers" (Section III-A), but tiers 1–3 are all implementations of the same underlying model at different granularities. The slot-level simulator and packet-level simulator confirm the analytical equations, but since they implement the same physics, this is model-internal consistency checking, not validation. The paper acknowledges this (Table XII) but the presentation still risks overstating the assurance level.

2. **Command traffic topology-invariance claim.** The paper repeatedly states that η_cmd is "topology-invariant" under centralized command generation. This is true by assumption but somewhat tautological—the interesting question is whether centralized command generation is realistic at 10^5 nodes, which the paper does not address.

3. **The sectorized mesh comparison is awkward.** It is described as "not a competing architecture" and having "different functional scope," yet it appears in comparison tables and figures. Either it provides a meaningful comparison or it doesn't; the current hedging weakens the narrative.

4. **GE parameter selection.** The default GE parameters (p_GB = 0.05, p_BG = 0.50) are described as "illustrative rather than predictive" and drawn from land-mobile satellite channels (Lutz et al.), which have fundamentally different propagation characteristics than ISLs. The sensitivity sweep (Fig. 5b) partially mitigates this, but the headline results (P95 = 4 cycles) are conditioned on parameters with no ISL empirical basis.

## 4. Clarity & Structure
**Rating: 4 (Good)**

The paper is well-organized with a clear roadmap (Section IV preamble), consistent notation (Table I), and explicit disambiguation of tool scopes (Section III-A). The three-tier overhead decomposition (Section III-E) is clearly stated and consistently applied. Tables are generally informative, particularly Tables V (γ sensitivity), VII (superframe budget), and IX (workload feasibility).

Areas for improvement:
- The paper is very long (~12 pages of dense technical content) with substantial redundancy. The same results are stated in the abstract, introduction, results, discussion, and conclusion. A 15–20% reduction would improve readability.
- Some figures are referenced but their content is described rather than shown (the review is based on the LaTeX source; actual figure quality cannot be assessed).
- The notation table omits several symbols used later (α_RX, q, L_cmd, f_RF, F, R).

## 5. Ethical Compliance
**Rating: 4 (Good)**

The data availability statement is exemplary: open-source code, tagged release, specific software versions, and runtime estimates. The AI disclosure is present and appropriately scoped. Author anonymization is noted as temporary per IEEE policy. The Monte Carlo configuration (30 replications, bootstrap CIs) is adequately described for reproducibility.

Minor concern: the AI tools cited (Claude 4.6, Gemini 3 Pro, GPT-5.2) appear to be future/unreleased versions, which is unusual and should be clarified.

## 6. Scope & Referencing
**Rating: 3 (Adequate)**

The reference list (55 items) covers the major relevant areas: CCSDS standards, distributed systems theory, swarm robotics, constellation management, AoI theory, and queueing theory. Key omissions:

- No references to actual TDMA scheduling work in satellite networks (e.g., DVB-RCS2, or the substantial literature on demand-assigned TDMA for satellite systems).
- No references to the network calculus literature beyond Le Boudec's textbook, despite claiming the work "complements" network calculus.
- Limited engagement with the substantial body of work on cluster-based satellite network architectures (e.g., virtual node architecture for LEO constellations).
- The Starlink reference is an FCC filing, not a technical publication; operational details are speculative.

The paper's scope is appropriate for IEEE T-AES, though the contribution may be better suited to a systems engineering venue (e.g., Journal of Spacecraft and Rockets, or AIAA JAIS) given its sizing-equation focus.

---

## Major Issues

1. **The DES provides insufficient independent validation beyond confirming its own equations.**
   - *Issue:* The <0.1% DES-analytical agreement is presented as a verification result, but both implement identical accounting. The distributional analysis (Fig. 8) is the only genuinely independent DES contribution, and it addresses a secondary question (buffer sizing under stochastic campaigns).
   - *Why it matters:* The paper's assurance argument rests heavily on multi-tier verification, but the tiers are not independent. A reader might incorrectly infer that the DES provides external validation.
   - *Remedy:* (a) Explicitly downgrade the DES role to "implementation consistency check" throughout (not just in one sentence). (b) Strengthen the distributional analysis: derive closed-form buffer CDFs for the Bernoulli and ON/OFF models and compare against DES to demonstrate the DES adds value beyond what analysis provides. (c) Alternatively, implement a simplified NS-3 model for even one configuration to provide genuine external validation.

2. **The GE channel model lacks ISL-specific empirical grounding.**
   - *Issue:* Default parameters are from land-mobile satellite channels; no ISL measurement data are cited. The "illustrative rather than predictive" caveat is buried in the text.
   - *Why it matters:* The headline GE results (P95 = 4 cycles, intra-cycle ARQ infeasibility) are conditioned on these parameters. If real ISL obstruction statistics differ substantially, the design curves shift.
   - *Remedy:* (a) Elevate the "illustrative" caveat to the abstract and Section I contributions list. (b) Provide a mapping table: for each physical mechanism (structural shadowing, antenna mispointing, Earth occultation), give the expected GE parameter range with references, and read off the corresponding P95 from Fig. 5b. The text in Section IV-C partially does this but should be formalized into a table.

3. **The three-layer feasibility framework conflates two layers that are not independent.**
   - *Issue:* Layer 1 (byte budget, η) and Layer 2 (MAC efficiency, η_total/γ) are related by a simple scaling factor (1/γ). They are not independent feasibility checks—Layer 2 is strictly tighter than Layer 1 for any γ < 1. Only Layer 3 (TDMA airtime, half-duplex scheduling) provides a genuinely independent constraint.
   - *Why it matters:* Presenting three "layers" suggests three independent checks, inflating the apparent rigor of the framework.
   - *Remedy:* Restructure as a two-layer framework: (1) message-layer byte budget (η, parameterized by γ for PHY translation), and (2) half-duplex TDMA airtime schedulability. This is cleaner and more honest about the actual constraint structure.

4. **The generalized γ expression (Eq. 16) has limited practical utility as presented.**
   - *Issue:* Eq. 16 mixes bits and milliseconds with an implicit unit conversion (the /1000 factor), and the denominator structure is non-obvious. The CCSDS TC alternative (γ = 0.79) is mentioned in passing but not developed.
   - *Why it matters:* If the equation is intended for practitioner use, it must be unambiguous and accompanied by worked examples for at least 2–3 standard configurations.
   - *Remedy:* (a) Rewrite Eq. 16 with explicit unit annotations. (b) Provide a table of γ values for 3–4 common CCSDS link configurations (Proximity-1, TC SDLP, AOS, custom). (c) Include a brief worked example showing how a practitioner would compute γ for their specific link.

5. **The stress-case dominance of command traffic undermines the hierarchical architecture's claimed advantage.**
   - *Issue:* Commands constitute >60% of stress-case traffic and are topology-invariant (under the centralized generation assumption). The hierarchical architecture's unique contribution (η_0 ≈ 5%) is small. The paper acknowledges this but does not adequately explore the implication: if commands dominate, the architecture choice matters little for bandwidth sizing.
   - *Why it matters:* This undercuts the paper's central motivation. If the answer is "commands dominate regardless of topology," the sizing equations for hierarchical overhead are of limited practical value.
   - *Remedy:* (a) Develop the cluster-local planning alternative (currently one paragraph in Section IV-A) into a full comparison showing how η changes under distributed decision-making. (b) Alternatively, reframe the contribution: the paper's value is in the *complete* sizing framework (including duty factor, GE recovery, AoI, schedulability), not just the hierarchical overhead decomposition.

## Minor Issues

1. **Table I notation:** α_RX, q, L_cmd, G, f_RF, F, R are used in equations but not defined in the notation table.

2. **Eq. 8 (unicast stagger):** The denominator uses (1 − α_RX) but α_RX is not defined until the surrounding text. Define it explicitly in the equation or notation table.

3. **Section III-A:** "Claude 4.6, Gemini 3 Pro, GPT-5.2" — these appear to be future model versions. Clarify whether these are actual tools used or placeholders.

4. **Table III (link budget):** The "fails" annotation for RF-backup at 24 kbps is informal. State the achieved E_b/N_0 vs. required and the resulting BER.

5. **Section IV-B:** "P99 AoI exceeds 440 s" — this is stated before the analytical derivation (Eq. 11). Reorder for logical flow.

6. **Table VIII (scaling):** "omitted for brevity" for 8 intermediate sizes is acceptable but consider providing these in supplementary material or the repository.

7. **Fig. 3 caption:** References "fig-phase-stagger.pdf" — ensure all figure files are included in the submission package.

8. **Section IV-E:** "η_0 audit" paragraph — the 0.5 pp gap between analytical (5.6%) and DES (5.0%) is attributed to "coordinator self-exclusion" but this should be derived explicitly (coordinator doesn't send status to itself: saves 256 B × 8 / (1000 × 10) = 0.2 bps per coordinator, which is ~0.02% per node, not 0.5 pp).

9. **Eq. 3 (hierarchical messages):** This counts upward messages only. The bidirectional claim in the following paragraph should be reflected in the equation or clearly distinguished.

10. **Section II-B:** The SWIM reference [40] is for failure detection in distributed systems, not specifically space systems. Clarify the adaptation required.

11. **Table XII (claim map):** The "Distrib." column header is unclear—spell out "Distributional Analysis."

12. **Throughout:** Inconsistent use of "kbps" vs. "kbit/s" — IEEE style prefers the latter.

---

## Overall Recommendation
**Recommendation: Major Revision**

This paper makes a useful engineering contribution by providing closed-form sizing equations for hierarchical coordination in large space swarms, with a well-structured three-layer (arguably two-layer) feasibility framework. The standards-grounded γ derivation from CCSDS Proximity-1 framing is a genuine improvement over assumed MAC efficiency values, and the campaign duty factor elegantly resolves earlier concerns about workload realism. The stress-case is now properly contextualized as a continuous-duty upper bound, with realistic operations well within budget.

However, the paper has significant structural issues that must be addressed. The validation architecture is largely self-referential: the DES, slot-level simulator, and packet-level simulator all implement the same underlying model, so their agreement demonstrates implementation consistency rather than model validity. The GE channel parameterization lacks ISL-specific empirical grounding, and the headline results are conditioned on illustrative parameters. Most critically, the finding that command traffic dominates and is topology-invariant undermines the hierarchical architecture's claimed sizing advantage—the paper needs to either develop the distributed planning alternative or reframe its contribution around the complete sizing framework rather than the hierarchical decomposition specifically.

The paper would benefit from a more honest assessment of what the verification hierarchy actually demonstrates, a reduction in length (substantial redundancy exists), and a stronger engagement with the practical implications of its own findings. With these revisions, the work could make a solid contribution to the systems engineering literature for large constellation design.

## Constructive Suggestions (Ordered by Impact)

1. **Develop the distributed planning comparison** (Section IV-A, "Command generation locus"): Expand the one-paragraph treatment of cluster-local Raft consensus into a full workload profile showing η under distributed decision-making. This would demonstrate that the sizing framework is general and that the hierarchical architecture provides genuine bandwidth savings when commands are generated locally.

2. **Provide genuine external validation for at least one configuration:** Even a simplified NS-3 model with 10 nodes and TDMA scheduling would provide an independent check on the slot-level simulator's assumptions. Alternatively, compare against published TDMA performance data from an operational satellite system.

3. **Restructure the feasibility framework as two layers** (byte budget + airtime schedulability) with γ as a translation parameter, rather than three layers where two are algebraically dependent.

4. **Formalize the GE-to-physical-mechanism mapping** into a reference table with parameter ranges and corresponding design curves, making the sensitivity study directly actionable.

5. **Add worked examples for the generalized γ equation** covering 3–4 standard CCSDS configurations, with explicit unit handling.

6. **Reduce paper length by 15–20%** by eliminating redundant restatements of key results across sections and consolidating the verification discussion.