---
paper: "02-swarm-coordination-scaling"
version: "cq"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-03-04"
recommendation: "Unknown"
---



# Peer Review: "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version CQ)

---

## 1. Significance & Novelty
**Rating: 3 (Adequate)**

The paper addresses a genuine gap: closed-form sizing equations for hierarchical coordination at the $10^3$–$10^5$ node scale with byte-level traffic accounting. The two-layer feasibility framework (byte budget + TDMA airtime) is a useful conceptual contribution, and the campaign duty factor $d$ is a sensible parameterization. However, the novelty is tempered by several factors: (1) the core equations are relatively straightforward engineering calculations (traffic accounting, slot timing) rather than deep analytical contributions; (2) the absence of any external validation means the practical significance remains speculative; (3) the paper's primary concrete output—a PHY rate recommendation of 35 kbps for a specific parameter set—is narrow. The generalized $\gamma$ expression (Eq. 7) is useful but is essentially a definition of slot efficiency that any TDMA practitioner would derive. The paper is better characterized as a design methodology paper than a research contribution with novel findings.

## 2. Methodological Soundness
**Rating: 3 (Adequate)**

The three-layer feasibility framework (byte budget, MAC efficiency, TDMA airtime) is logically structured, and the authors are commendably transparent about what each tool can and cannot do. The DES is cycle-aggregated at message granularity, which is appropriate for the byte-budget layer but cannot capture the phenomena that matter most (MAC contention, packet-level timing). The slot-level simulator provides genuine incremental value by revealing the ARQ×TDMA coupling (52.7% deadline misses), which is invisible to the DES—this is the paper's strongest methodological contribution.

However, several methodological concerns remain:

- The GE channel model parameters are entirely assumed, with no empirical grounding for ISL channels. While the sensitivity sweep partially mitigates this, the default parameterization ($p_{BG} = 0.50$, $p_B = 0.90$) drives key results (ARQ infeasibility, inter-cycle recovery times) and could mislead practitioners who take these as representative.
- The coordinator queueing model uses a fluid server with drop-tail, which is inconsistent with the TDMA slot structure that the paper argues is critical. The MMPP/D/1 characterization is acknowledged but deferred.
- The static cluster membership assumption is justified for co-planar formations but the paper targets $10^3$–$10^5$ nodes, which almost certainly implies multi-plane constellations. The 0.5% re-association overhead estimate deserves more rigorous treatment.

## 3. Validity & Logic
**Rating: 3 (Adequate)**

The internal logic is generally sound, and the authors have clearly invested significant effort in ensuring consistency across the manuscript. The parameter dependency map (Section IV preamble) is a welcome addition that clarifies which results depend on which inputs.

Key validity concerns:

- **Circularity of DES verification.** The authors acknowledge this explicitly (Tier 1 verification confirms implementation, not model validity), which is appropriate. However, the paper still devotes substantial space to DES-analytical agreement ($<$0.1%), which provides minimal scientific value. The distributional tail analysis (buffer sizing under correlated campaigns) is the DES's genuine contribution and should be more prominently featured relative to the mean-value verification.

- **The $\gamma$ unification.** The transition from the earlier 0.85 to the CCSDS-grounded 0.76 is well-motivated and consistently applied throughout. Model S (0.949) and Model C (0.761/0.745) are clearly distinguished, and the paper correctly uses Model C for all recommendations. However, I note that $\gamma$ is weakly rate-dependent ($\gamma_{24} = 0.761$, $\gamma_{30} = 0.745$) but the text sometimes uses unsubscripted $\gamma$ without specifying the rate—this could cause confusion.

- **Stress-case contextualization.** The $\eta_S \approx 46\%$ is now properly framed as an episodic worst-case bound with the duty factor decomposition. The time-weighted mean $\eta \approx 5.9\%$ and the explicit statement that stress conditions occupy $<$1\% of operational time are convincing. This is a significant improvement over what I would expect from earlier versions.

- **The "100% deadline misses at 24 kbps" claim** is valid under Model C but the paper should note more explicitly that this is a deterministic consequence of $(k_c - 1) \times T_{\text{slot}} > T_c$, not a stochastic finding.

## 4. Clarity & Structure
**Rating: 3 (Adequate)**

The paper is dense but generally well-organized. The roadmap at the beginning of Section IV is helpful. The notation table (Table I) is comprehensive. The rate ladder (Table V) effectively communicates the design flow.

However, the paper suffers from several clarity issues:

- **Excessive length and redundancy.** Many results are stated multiple times in slightly different forms across the abstract, introduction, results, and discussion. The paper would benefit from a 20-30% reduction in length.
- **The two-model presentation (Model S vs. Model C)** is a source of ongoing confusion despite the authors' efforts. Table VII uses Model S slot timing but this is buried in a footnote. A reader skimming the table would draw incorrect conclusions.
- **Algorithm 1** is useful but trivial—it is essentially a sequential evaluation of two inequalities. Its presentation as a formal algorithm overstates its complexity.
- **Figure quality** cannot be assessed from the LaTeX source, but the descriptions suggest appropriate content. The sensitivity sweep (Fig. 3b) is the most valuable figure.
- **The boxed framework definition** (Section IV) is helpful but interrupts the flow; it would be better placed in Section III or as a standalone subsection.

## 5. Ethical Compliance
**Rating: 4 (Good)**

The paper is commendably transparent about: (1) the absence of external validation; (2) the assumed nature of GE parameters; (3) the limitations of DES verification; (4) AI tool usage (ideation and prose editing, not results generation). Data availability is excellent (GitHub repository with tagged release, full parameter tables, runtime estimates). The claim map (Table IX) is an exemplary practice that more papers should adopt. The only gap is the anonymous authorship, which is noted as temporary per IEEE policy.

## 6. Scope & Referencing
**Rating: 3 (Adequate)**

The literature coverage is broad, spanning constellation management, swarm robotics, distributed systems theory, queueing theory, and CCSDS standards. Key references (CCSDS Proximity-1, DVB-RCS2, Lutz et al. GE model, AoI framework) are appropriate. However:

- The paper does not engage with the substantial literature on TDMA scheduling optimization for satellite networks (e.g., demand-assigned TDMA, MF-TDMA in DVB-RCS2 beyond the single citation).
- Recent work on distributed satellite systems (e.g., ESA's OPS-SAT, NASA's Starling mission) that have demonstrated ISL-based coordination is not cited.
- The network calculus reference (Le Boudec) is mentioned but not used; either apply it or remove the citation.
- Several references are non-archival (DARPA program pages, Amazon Kuiper overview) and may not meet IEEE T-AES standards for permanence.

---

## Major Issues

**1. The DES provides insufficient independent validation beyond confirming its own equations.**

The paper acknowledges this (Section V-A) but still presents DES-analytical agreement as a significant result. The $<$0.1\% agreement is by construction since both tools implement the same traffic accounting equations. The distributional analysis (buffer CDFs) is genuinely useful but represents perhaps 10% of the DES-related content.

*Why it matters:* Readers may overestimate the validation status of the framework. The claim map helps, but the body text still reads as though DES confirmation strengthens confidence in the model's predictive accuracy.

*Remedy:* Restructure Section IV-F to lead with the distributional/buffer-sizing results as the primary DES contribution. Reduce the mean-value verification to a single sentence. Consider moving the DES description to a shorter appendix and promoting the slot-level simulator findings (ARQ×TDMA coupling) as the primary simulation contribution.

**2. No sensitivity analysis on the most consequential assumed parameter: $C_{\text{node}} = 1$ kbps.**

The entire framework is sized around a 1 kbps per-node budget. While Section III-E provides a brief scaling argument ($\eta \propto 1/C_{\text{node}}$), the paper does not systematically explore how the design recommendations change at 2, 5, or 10 kbps—rates that are far more realistic for S-band ISLs. Table II-A provides three data points but does not trace through the full feasibility algorithm for each.

*Why it matters:* The 1 kbps budget drives the paper's most interesting finding (the 30–35 kbps PHY rate recommendation and the tight TDMA margin). At higher per-node budgets, both feasibility layers become trivially satisfied, and the paper's contribution reduces to the $\gamma$ expression and the GE sensitivity curves.

*Remedy:* Add a systematic sensitivity analysis showing how the rate ladder (Table V), margin analysis (Table VI), and ARQ feasibility change across $C_{\text{node}} \in \{0.5, 1, 2, 5, 10\}$ kbps. This would significantly strengthen the paper's practical utility.

**3. The packet-level validation (Section IV-J) provides parameter anchoring, not independent validation.**

The CCSDS-grounded $\gamma$ derivation is presented as "Tier 2" evidence, but it is a calculation from a standard's framing specification, not an independent measurement or simulation. The $\gamma$ value feeds directly into the same equations used by the DES and slot-sim. The DVB-RCS2 comparison (measured 0.70–0.85 vs. calculated 0.76) provides a useful sanity check but is for a different system (ground terminals, not ISL).

*Why it matters:* The paper's feasibility conclusions are highly sensitive to $\gamma$ (a 10% reduction shifts the minimum PHY rate by ~3 kbps). Without hardware measurement or high-fidelity simulation (NS-3 with realistic PHY), the calculated $\gamma$ remains an estimate.

*Remedy:* Downgrade the CCSDS $\gamma$ derivation from "Tier 2 cross-model anchoring" to "standards-based parameter estimation." Add explicit uncertainty bounds on $\gamma$ (e.g., $\gamma = 0.745 \pm 0.07$ based on the DVB-RCS2 measured range) and propagate these through the rate ladder.

**4. The three-layer feasibility framework conflates a unit conversion with a feasibility layer.**

The paper defines three layers (byte budget, MAC efficiency, TDMA airtime) but then states "Do not double-count: $C_{\text{raw}} = C_{\text{coord,info}}/\gamma$ is a unit conversion, not a third test." This is confusing—if it's not a test, it shouldn't be presented as a layer. The actual framework is two-layer (byte budget + airtime schedulability), with $\gamma$ serving as a parameter in the airtime calculation.

*Why it matters:* The "three-layer" framing in the abstract and introduction creates an expectation of three independent tests, which is misleading.

*Remedy:* Consistently present the framework as two-layer throughout. Remove "three-layer" language from the abstract and introduction. Present $\gamma$ as a parameter of the airtime layer, not a separate layer.

**5. The GE model lacks any empirical grounding for ISL channels, and the default parameters may be misleading.**

The Lutz et al. reference and ITU-R P.681 are for land-mobile satellite channels, not ISLs. ISL channels face fundamentally different impairments (no multipath, no terrain shadowing; instead: structural self-shadowing, antenna mispointing, solar interference). The default $p_{BG} = 0.50$ implies a mean bad-state duration of 2 cycles (20 s), which may be optimistic for antenna mispointing or pessimistic for structural shadowing.

*Why it matters:* The GE parameterization drives the ARQ infeasibility finding and the inter-cycle recovery characterization—two of the paper's key results.

*Remedy:* (1) State explicitly that the Lutz/ITU-R references are for land-mobile channels and that ISL-specific GE parameters do not exist in the open literature. (2) Provide a more detailed physical mapping from ISL impairment mechanisms to GE parameters, ideally with order-of-magnitude estimates from first principles (e.g., tumble rate → shadowing duration → $p_{BG}$). (3) Consider presenting results for 3–5 representative GE parameter sets rather than a single default.

---

## Minor Issues

1. **Abstract:** "three-layer feasibility framework" should be "two-layer" per the paper's own clarification in the boxed definition.

2. **Table I:** $\alpha_{\text{RX}}$ is listed as "derived from schedule" but Algorithm 1 line 6 computes it as $T_{\text{ing}}/T_c$—clarify that this is a deterministic function of the other parameters, not a free variable.

3. **Eq. 1 ($M_{\text{total}}$):** The third term assumes uniform $k_c$ across all clusters and uniform $k_r$ across all regions. State this assumption explicitly.

4. **Section III-B-2:** "Coordinator sends a single 512-byte summary" but Table III lists "Cluster summary size = 512 B" and "Region summary size = 1024 B." The text should clarify the distinction earlier.

5. **Table VII footnote:** "Model S slot timing (simplified, NOT for design recommendations)" is critical information that should be in the table title, not a footnote.

6. **Eq. 6 ($\eta_{\text{consensus}}$):** The assumption that Raft votes are serialized over the shared channel should be justified—parallel voting over separate slots would change the overhead calculation.

7. **Section IV-A:** "Phase-staggered scheduling... DES confirms zero drops at ≥25 kbps vs. 50 kbps under random phase"—this is a significant finding buried in a single sentence. Elaborate or provide a figure.

8. **Table VI (margin analysis):** "Acq. variability (1σ) = 10 ms" is labeled "Eng. assumption"—this is the largest unmodeled overhead and deserves justification or a reference.

9. **Section IV-E:** The empirical anchoring paragraph cites ESA collision avoidance statistics but the connection to $d$ values is loose. Provide a more rigorous mapping (e.g., 10 maneuvers/yr × 6 cycles/event × 10 s/cycle = $d \approx 0.00002$, which is far below the "conservative default" of $d = 0.10$).

10. **Bibliography:** References [3] (Kuiper), [17] (DARPA OFFSET), [18] (Replicator), [24] (DARPA Blackjack) are non-archival URLs. IEEE T-AES typically requires archival references; consider replacing with published technical descriptions where available.

11. **Section V-C:** The $\gamma$-conditional PHY lookup table ($\gamma \in [0.65, 0.70] \Rightarrow 40$ kbps, etc.) is useful but should note that it applies only to the specific parameter set ($k_c = 100$, $S = 256$ B, $T_c = 10$ s).

12. **Eq. 7 ($\gamma$ time-domain):** $T_{\text{framing}} = O_{\text{frame}} / (R_{\text{FEC}} \cdot R_{\text{PHY}})$—this implies framing bits are also FEC-encoded, which is standard for CCSDS but should be stated explicitly.

13. **The "thundering herd" analysis** (footnote in Section III-B-2) is interesting but the Slotted ALOHA convergence analysis deserves more than a footnote if it is to be credible. The claim that BEB converges within ~640 ms at $G \approx 25$ needs justification.

14. **Section III-E:** "At $\gamma \in [0.7, 0.9]$, stress-case exceeds Slotted ALOHA capacity"—this comparison is not meaningful since the paper assumes centrally scheduled TDMA, not Slotted ALOHA.

---

## Overall Recommendation
**Recommendation: Major Revision**

This paper presents a well-structured engineering methodology for sizing hierarchical coordination architectures in large space swarms. The two-layer feasibility framework (byte budget + TDMA airtime) is a useful conceptual contribution, and the campaign duty factor parameterization effectively addresses workload realism. The CCSDS-grounded $\gamma$ derivation (replacing the earlier 0.85 with the validated 0.76) is consistently applied and represents a meaningful improvement in rigor. The stress-case ($\eta_S \approx 46\%$) is now properly contextualized as an episodic upper bound, with convincing empirical anchoring showing routine operations at 5–10%.

However, the paper's central limitation—the complete absence of external validation—is severe for a journal of this caliber. The DES verification is acknowledged as circular, the slot-level simulator shares the same equations, and the CCSDS $\gamma$ derivation is a calculation rather than a measurement. The GE channel model, which drives key results, has no empirical basis for ISL channels. The paper would be substantially strengthened by: (1) propagating $\gamma$ uncertainty through the rate ladder; (2) systematic sensitivity analysis on $C_{\text{node}}$; (3) clearer separation of the two-layer (not three-layer) framework; and (4) honest reframing of the CCSDS $\gamma$ as parameter estimation rather than validation. The slot-level simulator's ARQ×TDMA coupling finding is the paper's most genuinely novel result and should be more prominently featured.

The paper is publishable after major revision if the authors address the validation framing, reduce redundancy, and strengthen the sensitivity analysis. The methodology is sound for its stated purpose (preliminary design sizing), but the current presentation occasionally overstates the confidence level of the results.

---

## Constructive Suggestions
*(Ordered by impact)*

1. **Add systematic $C_{\text{node}}$ sensitivity analysis** tracing the full feasibility algorithm at 0.5, 1, 2, 5, 10 kbps. This would transform the paper from a single-point design study into a genuinely parametric tool.

2. **Propagate $\gamma$ uncertainty** ($\pm$10% based on DVB-RCS2 measured range) through the rate ladder and present the resulting PHY rate recommendation as a range rather than a point estimate.

3. **Restructure to lead with the slot-level simulator's ARQ×TDMA coupling** as the primary simulation finding, and reduce the DES mean-value verification to a brief confirmation statement.

4. **Present 3–5 representative GE parameter sets** mapped to specific ISL impairment mechanisms (structural shadowing, mispointing, solar interference) with first-principles duration estimates, rather than a single default.

5. **Reduce manuscript length by 20–30%** by eliminating redundant restatements of key results across sections and consolidating the Model S/Model C comparison into a single, clearly labeled subsection.

6. **Reframe the CCSDS $\gamma$ derivation** as "standards-based parameter estimation" rather than "Tier 2 cross-model anchoring" to avoid implying independent validation.

7. **Add a concise "How to Use This Paper" subsection** in the Discussion that walks a practitioner through Algorithm 1 with a worked example using non-default parameters (e.g., $k_c = 50$, $S = 512$ B, Ka-band link).