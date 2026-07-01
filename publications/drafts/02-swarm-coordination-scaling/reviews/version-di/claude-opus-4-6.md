---
paper: "02-swarm-coordination-scaling"
version: "di"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-03-06"
recommendation: "Unknown"
---



# Peer Review: Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms

## 1. Significance & Novelty
**Rating: 3 (Adequate)**

The paper addresses a genuine gap: closed-form parametric sizing for hierarchical coordination in large autonomous spacecraft swarms with byte-level traffic accounting. The two-test feasibility framework (byte budget + TDMA airtime) is a useful conceptual contribution, and the campaign duty factor $d$ is a sensible parameterization for bridging the gap between stress-case bounds and operational reality. However, the core analytical machinery—TDMA slot efficiency calculations, M/D/1 queueing, Gilbert-Elliott channel modeling, AoI under geometric sampling—draws entirely from well-established techniques. The novelty lies in their assembly and application to this specific domain, not in methodological advance. The paper would benefit from a clearer articulation of what design decisions this framework enables that were previously impossible or impractical.

## 2. Methodological Soundness
**Rating: 3 (Adequate)**

The analytical framework is internally consistent and the equations are correctly derived. The three-layer decomposition (byte budget, MAC efficiency, TDMA airtime) is logically sound, and the rate ladder (Table IV) provides a clear progression from information-rate to PHY-rate recommendation. Several methodological concerns remain:

- The DES verification is acknowledged as Tier-1 (confirming its own equations), which is honest but limits the evidentiary value. The distributional tails (Fig. 4) are the DES's incremental contribution, but these are conditioned on assumed burst models with no empirical grounding.
- The GE channel model parameters ($p_G$, $p_B$, $p_{GB}$, $p_{BG}$) are illustrative defaults with no ISL measurement basis. While the paper correctly frames this as a "what-if design tool," the extensive analysis built on these specific parameters (52.7% miss rate, P95 = 4 cycles, etc.) risks conveying false precision.
- The packet-level validation (Section IV-J) anchors $\gamma$ via CCSDS Proximity-1 framing standards, which is a reasonable parameter estimate but not independent validation—the same equations underlie all tools.
- The static cluster membership assumption is reasonable for co-planar formations but the J2 analysis for cross-plane configurations (Section V-C) is cursory.

## 3. Validity & Logic
**Rating: 4 (Good)**

The internal logic is generally tight. The paper is commendably transparent about what constitutes validation versus verification versus parameter anchoring. Specific strengths:

- The campaign duty factor $d$ adequately addresses workload realism. The canonical mapping (Section IV-E) with concrete examples (station-keeping, collision avoidance) and the yearly mixture calculation ($\bar{\eta} = 5.6\%$, full-load 0.1% of time) effectively contextualizes the 46% stress-case as a continuous-duty upper bound.
- The gamma unification around 0.76 (CCSDS-derived) is consistently applied throughout. The $\gamma$ consistency ledger in Table XI is a good practice. I verified spot-checks of $\gamma_{24} = 0.761$ and $\gamma_{30} = 0.745$ against Eq. (8) and they are correct.
- The stress-case ($\eta_S \approx 46\%$) is now properly framed as episodic, with Table VII providing mission-phase mappings and the yearly mixture showing it occurs <1% of operational time.
- The three-layer feasibility framework is sound, and the paper correctly notes that Test A and Test B decouple for $d \leq 0.10$.

One logical concern: the paper claims topology-invariance of $\eta_{\text{cmd}}$ under centralized command generation, but this holds only for broadcast semantics. The unicast stagger analysis (Eq. 5-6) shows that Test B is topology-sensitive through $q$, which somewhat undermines the "topology-invariant" framing.

## 4. Clarity & Structure
**Rating: 3 (Adequate)**

The paper is dense but generally well-organized. The roadmap at the start of Section IV and the two-test feasibility box are helpful. Algorithm 1 effectively synthesizes the sizing procedure. However:

- The paper is excessively long for a journal article. Significant redundancy exists: the same feasibility results are stated in the abstract, introduction, Section IV-A, Table IV, Table VIII, and Section VI. The margin analysis appears in Tables V, VI, IX, and the text of IV-A.
- The notation table (Table I) is comprehensive but the sheer number of symbols and the frequent cross-referencing make the paper difficult to follow linearly. Some symbols ($\alpha_{\text{RX}}$) are defined as "computed outputs, not free parameters" in the notation table—this is good practice but suggests the notation is overloaded.
- Model S vs. Model C distinction is clearly stated upfront and consistently maintained, which is an improvement. However, Model S still appears in several tables and figures, adding length without clear benefit since it is "never used for recommendations."
- Several footnotes are paragraph-length (Tables II, III, XI), suggesting material that should be in the main text or appendices.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**

The paper is exemplary in transparency: data availability with tagged repository, explicit AI disclosure, clear V&V tier labeling, and repeated acknowledgment that no external validation exists. The claim map (Table XII) is a model of honest evidence attribution. The "not peer-reviewed" label on the self-citation [30] is appropriate.

## 6. Scope & Referencing
**Rating: 3 (Adequate)**

The reference list covers the major relevant areas (CCSDS standards, swarm robotics, constellation management, AoI theory, distributed consensus). Some gaps:

- No references to actual ISL measurement campaigns or channel characterization studies beyond Lutz et al. (1991), which addresses land-mobile satellite channels, not ISL.
- The DVB-RCS2 comparison is appropriate but brief. More engagement with the satellite TDMA literature (e.g., MF-TDMA in DVB-S2X return links, VSAT TDMA systems) would strengthen the framing.
- Missing references to recent work on autonomous constellation management (e.g., Autonomous Navigation and Timing work at JPL, ESA's CREAM study).
- The LEACH comparison is apt but LEACH is a WSN protocol from 2000; more recent cluster-head rotation protocols with QoS guarantees would be relevant.

---

## Major Issues

1. **The DES provides limited independent verification value.** The paper honestly acknowledges this (Tier-1, "by construction"), but then devotes substantial space to DES results that confirm analytical equations to <0.1%. The distributional tails (Fig. 4) are the only non-tautological DES output, but they depend entirely on assumed burst models. **Why it matters:** Readers may overweight the DES as validation rather than implementation verification. **Remedy:** Condense DES mean-value confirmation to a single sentence. Expand the distributional analysis with sensitivity to burst model assumptions (e.g., what if ON/OFF durations follow a heavy-tailed distribution rather than geometric?). Be explicit that the DES tail results are conditional predictions, not validated findings.

2. **No external validation pathway is demonstrated, even partially.** The validation roadmap (Section V-B) lists three needed steps but provides no partial results. The paper has been through multiple revisions (Version DI) without any external anchoring. **Why it matters:** For a journal publication, even preliminary external comparison (e.g., NS-3 simulation of a single cluster, comparison with published DVB-RCS2 terminal measurements for $\gamma$) would substantially strengthen the contribution. **Remedy:** Either (a) provide at least one external comparison point (NS-3 single-cluster simulation would be tractable), or (b) reframe the paper explicitly as a "design framework proposal" rather than presenting quantitative results with three significant figures that lack external grounding.

3. **The GE channel model analysis conveys false precision despite "what-if" framing.** Specific numerical results (52.7% miss rate, P95 = 4 cycles, 27.1% intra-cycle recovery) are stated with high precision but depend on unvalidated parameters. The physical mapping (Section IV-C) provides plausible ranges but no calibration. **Why it matters:** Practitioners using Fig. 3(b) need to know the sensitivity of design recommendations to GE parameter uncertainty, not just $p_{BG}$ sweeps at fixed $p_B$. **Remedy:** Add a joint sensitivity analysis over ($p_B$, $p_{BG}$) showing the region in parameter space where the 35 kbps recommendation holds vs. where 30 kbps suffices vs. where >35 kbps is needed. This would make the "what-if" tool genuinely useful.

4. **The 1 kbps per-node budget is a critical assumption that deserves more scrutiny.** The paper derives it from a link budget (Table III) but the link budget assumes specific antenna gains (6 dBi patch), transmit power (1W), and range (500 km). The sensitivity analysis (Section III-E) notes $\eta \propto 1/C_{\text{node}}$ but doesn't explore the design space where $C_{\text{node}} \geq 2$ kbps (where TDMA analysis becomes non-binding). **Why it matters:** If the entire TDMA analysis (Sections IV-A through IV-J) is relevant only at $C_{\text{node}} \leq 1$ kbps, and modern S-band ISL can readily achieve higher rates, the practical relevance of the detailed TDMA analysis is unclear. **Remedy:** Provide a clearer argument for why 1 kbps is a realistic or important design point for the target application (10^3–10^5 node swarms). If it represents a worst-case power/mass constraint for very small spacecraft, state this explicitly with supporting references.

5. **The paper's scope is ambiguous between "design framework" and "system design."** The abstract says "preliminary design estimates lacking external validation," but the level of detail (superframe time budgets to the millisecond, specific PHY rate recommendations, ACK mini-slot timing) suggests system-level design. **Why it matters:** The appropriate level of precision should match the validation level. **Remedy:** Either validate to the precision claimed, or present results as order-of-magnitude design guidance with explicit uncertainty bands on all key outputs (not just $\gamma$).

## Minor Issues

1. **Eq. (1):** The hierarchical message count assumes uniform fan-out. State this assumption explicitly in the equation context (it appears only parenthetically).

2. **Table I:** $\alpha_{\text{RX}}$ is described as a "computed output" with an example value of 0.908. This is confusing in a notation table; consider moving the example to the text.

3. **Section III-B-2, "Thundering herd" analysis:** The Slotted ALOHA with BEB analysis is interesting but tangential. The 140–160s recovery time is acknowledged as rare (<1/yr per cluster), suggesting this could be condensed or moved to an appendix.

4. **Table VI (Margin Analysis):** "Acq. variability (1σ) = 10 ms" is labeled "Eng. assumption" with RSS justification. The RSS of ±2 ms over 99 slots is $2\sqrt{99} \approx 20$ ms (1σ), not 10 ms. Clarify whether this is per-slot or aggregate.

5. **Eq. (3), consensus overhead:** The stability limit $f_{\text{decision,max}} \approx 24$ should show the derivation or at least the inequality used.

6. **Section IV-B:** "P99 = 441 s" is described as a "sampling policy tail, not network-induced latency"—this is an important distinction that should appear earlier (e.g., in the abstract, which mentions AoI only implicitly).

7. **Fig. 2 (cross-cycle recovery):** The figure is referenced before the GE model parameters are fully motivated. Consider reordering or adding a forward reference.

8. **Table XII (Claim Map):** The "Std.-based param." column header is unclear. Consider "Standards-anchored estimate" or similar.

9. **References [6] and [7]:** O'Neill (1976) and Badescu (2006) are cited to justify the 10^5–10^6 scale but are speculative infrastructure concepts, not engineering references. Acknowledge this explicitly.

10. **The paper uses "feasible" and "infeasible" without defining a formal feasibility criterion beyond Tests A and B.** At 30 kbps with $M_r = 1$, ~12% deadline misses are reported—is this "feasible" or not? State an acceptable miss rate threshold.

11. **Typo/style:** "Eq.~\ref{eq:gamma_derived}" in Section IV-A is labeled as Model S but the equation number suggests it's the primary gamma expression. This could confuse readers skimming equations.

12. **The acknowledgment section mentions "Claude 4.6, Gemini 3 Pro, GPT-5.2"—these appear to be future/hypothetical model versions.** If this is intentional (the paper is set in a future context), it should be noted; if not, correct the version numbers.

---

## Overall Recommendation
**Recommendation: Major Revision**

This paper presents a well-structured analytical framework for sizing hierarchical coordination in large autonomous spacecraft swarms. The two-test feasibility decomposition (byte budget + TDMA airtime), the campaign duty factor parameterization, and the CCSDS-grounded slot efficiency derivation are useful contributions. The paper is commendably transparent about its validation limitations, and the claim map (Table XII) sets a high standard for honest evidence attribution.

However, the paper suffers from three fundamental issues that require major revision. First, the absence of any external validation—even partial—limits the paper to a framework proposal rather than a validated design methodology, yet the level of numerical precision (millisecond-level superframe budgets, three-significant-figure efficiency values) implies a maturity that the evidence does not support. Second, the paper is substantially too long, with extensive redundancy across sections; a 30-40% reduction in length with material moved to appendices would improve readability without sacrificing content. Third, the practical relevance of the detailed TDMA analysis needs stronger motivation: if the analysis is binding only at ≤1 kbps per-node budgets, the paper should either justify why this regime is important for the target applications or broaden the analysis to cover the transition region more thoroughly.

The strongest elements—the feasibility framework, Algorithm 1, the $\gamma$-conditional lookup table, and the sensitivity curves—should be preserved and sharpened. The weakest elements—the DES mean-value confirmation, the extensive Model S analysis (which is explicitly not for design), and the repeated restatement of the same results—should be condensed.

## Constructive Suggestions

1. **(Highest impact) Provide at least one external validation point.** A single-cluster NS-3 simulation with CCSDS-like framing would anchor $\gamma$ and the superframe timing independently. Alternatively, compare predicted $\gamma$ against published DVB-RCS2 terminal measurements at comparable data rates.

2. **(High impact) Reduce paper length by 30-40%.** Consolidate the feasibility results into a single definitive table. Move Model S analysis, thundering herd analysis, and detailed link budget to appendices. Eliminate redundant restatements of the 35 kbps recommendation.

3. **(High impact) Add joint ($p_B$, $p_{BG}$) sensitivity analysis** showing the design recommendation boundary in GE parameter space. This transforms the "what-if tool" claim from aspirational to demonstrated.

4. **(Medium impact) Strengthen the 1 kbps motivation.** Either cite specific small-satellite power/mass constraints that make 1 kbps a realistic design point, or expand the analysis to show the framework's utility across the 1–10 kbps range where the TDMA/byte-budget transition occurs.

5. **(Medium impact) Define a formal feasibility threshold** (e.g., deadline miss rate ≤ 1%) and apply it consistently. The current treatment of 12% misses at 30 kbps as "marginally infeasible" is imprecise.

6. **(Medium impact) Expand the dynamic topology analysis.** The J2 perturbation analysis is promising but cursory. A Monte Carlo over realistic Walker constellation parameters would strengthen the static-membership assumption.

7. **(Lower impact) Consolidate the $\gamma$ presentation.** Eq. (2) (Model S), Eq. (8) (Model C), Table VII, Table XI, and Fig. 5 all present $\gamma$ information. A single definitive table with the measurement protocol would suffice.