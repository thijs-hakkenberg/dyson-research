---
paper: "02-swarm-coordination-scaling"
version: "cf"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-03-01"
recommendation: "Unknown"
---



# Peer Review: Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms

## 1. Significance & Novelty
**Rating: 3 (Adequate)**

The paper addresses a genuine gap: no prior work provides closed-form parametric sizing relationships for hierarchical coordination across $10^3$–$10^5$ spacecraft with byte-level traffic accounting. The two-layer feasibility framework (byte budget + TDMA airtime schedulability) and the generalized $\gamma$ expression are useful contributions. However, the novelty is tempered by the fact that the core equations are relatively straightforward engineering accounting (summation of known message sizes over known periods), and the "scaling" result ($\eta$ is constant with $N$ at fixed $k_c$) is essentially by construction—hierarchical decomposition with fixed fan-out yields $O(1)$ per-node overhead by definition. The paper is more accurately characterized as a careful parametric sizing exercise than a fundamental advance in distributed systems theory. The campaign duty factor $d$ is a welcome addition that substantially improves realism, but it is a simple Bernoulli gate on an already-simple linear model.

## 2. Methodological Soundness
**Rating: 3 (Adequate)**

The analytical framework is internally consistent and the three-layer verification structure (analytical, DES, slot-level/packet-level) is well-organized. However, several methodological concerns persist:

The DES operates at message-layer granularity and computes the same equations as the analytical model—the $<0.1\%$ agreement is a verification of implementation correctness, not validation. The authors acknowledge this explicitly (commendably), but the paper still devotes substantial space to DES results that add limited independent information beyond the distributional analysis of Fig. 8.

The slot-level TDMA simulator provides genuine Tier-2 value by revealing the ARQ×TDMA coupling (52.7% deadline misses at 24 kbps), which is the strongest cross-model finding. The packet-level $\gamma$ derivation from CCSDS Proximity-1 framing is a solid anchoring exercise.

The GE channel model is acknowledged as illustrative, but the paper draws fairly specific conclusions (P95 = 4 cycles, intra-cycle ARQ infeasible) from parameters that lack ISL-specific empirical grounding. The sensitivity sweeps (Fig. 5b) partially mitigate this, but the default parameterization receives disproportionate emphasis relative to its evidential basis.

## 3. Validity & Logic
**Rating: 4 (Good)**

The logical structure is generally sound. The decomposition $\eta = \eta_0 + d \cdot \eta_{\text{cmd}}$ is clean and consistently applied. The stress-case ($d=1$, $\eta_S \approx 46\%$) is now properly contextualized as a continuous-duty upper bound applying $<1\%$ of operational time—a significant improvement over what appears to have been a prior presentation issue. The empirical anchoring of $d$ via ESA collision avoidance statistics and Starlink orbit-raising windows is effective.

The $\gamma$ unification at 0.76 (replacing an earlier 0.85) appears consistently applied throughout: Table VI, the feasibility algorithm, and the rate feasibility table all use $\gamma_{24} = 0.760$. The rate-dependent notation ($\gamma_{24}$, $\gamma_{30}$) is helpful.

One logical tension: the paper repeatedly emphasizes that the 1 kbps RF-backup channel is the *only* regime requiring TDMA analysis, yet the TDMA analysis constitutes roughly 40% of the paper's technical content. This is justified if the RF-backup is design-driving for safety, but the paper could be more concise about the non-binding regimes.

The three-layer feasibility framework is sound in principle: byte budget → MAC translation → TDMA airtime. However, the "MAC translation" ($\eta_{\text{total}}/\gamma$) is presented somewhat ambiguously—Table IV's footnote correctly notes it is "necessary but not sufficient," yet it appears as a quasi-independent check in several places.

## 4. Clarity & Structure
**Rating: 3 (Adequate)**

The paper is comprehensive but overlong and repetitive. Key results are stated in the abstract, re-stated in the introduction, re-stated in the contributions list, derived in the results, and summarized again in the discussion. The notation table is helpful, but the sheer number of parameters, sub-cases, and cross-references makes the paper difficult to follow linearly.

The roadmap paragraph at the start of Section IV is appreciated. Figures are generally clear, though some (Fig. 10, fleet reuse) address edge cases that could be relegated to supplementary material. The superframe time budget (Table V) is excellent—one of the most informative tables in the paper.

The paper would benefit substantially from consolidation: the DES verification section (IV-F) could be reduced to a single paragraph plus the CDF figure, since the authors themselves acknowledge the agreement is by construction.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**

Exemplary transparency: open-source code with tagged release, full parameter tables, explicit AI disclosure, clear delineation of what is modeled vs. not modeled, and honest acknowledgment of the validation gap (Table IX). The tiered evidence framework (IEEE 1012) is a model for how simulation-based papers should present their claims.

## 6. Scope & Referencing
**Rating: 4 (Good)**

References are appropriate and span the relevant domains (CCSDS standards, AoI theory, swarm robotics, constellation management, distributed consensus). The Lutz et al. and ITU-R P.681 references properly ground the GE model. Network calculus (Le Boudec) is cited but not deeply engaged—a missed opportunity, since the periodic traffic model is exactly the regime where network calculus provides tight deterministic bounds that could complement the stochastic analysis.

Missing references: the paper does not cite recent work on distributed TDMA scheduling for satellite networks (e.g., Radhakrishnan et al., IEEE TAES 2016; or the CCSDS USLP standard 732.1-B-2 which supersedes some of the cited protocols). The AoI literature engagement is adequate but could note the peak-AoI metric (Sun et al., IEEE TIT 2019) as potentially more relevant for safety-critical applications than mean/P99 AoI.

---

## Major Issues

1. **The DES provides limited independent validation beyond distributional analysis.**
   - *Issue:* The DES and analytical model implement the same sizing equations. The $<0.1\%$ agreement (Table VII) is verification, not validation. The paper acknowledges this but still devotes ~2 pages to DES results.
   - *Why it matters:* Readers may overestimate the evidential weight of the DES confirmation. Journal space is consumed by results that are tautological by construction.
   - *Remedy:* Reduce Section IV-F to ~0.5 pages. Retain Fig. 8 (CDF, genuine distributional contribution) and the ON/OFF tail analysis. Remove or compress Table VII to a single sentence ("DES confirms analytical equations to $<0.1\%$ at all fleet sizes, as expected by construction"). Redirect saved space to strengthening the slot-level and packet-level analyses, which provide genuine cross-model value.

2. **The GE channel parameterization lacks empirical grounding for ISL applications, yet specific numerical conclusions are prominently featured.**
   - *Issue:* The default GE parameters ($p_{GB}=0.05$, $p_{BG}=0.50$) are acknowledged as illustrative, but "P95 = 4 cycles" appears in the abstract, conclusion, and multiple tables as if it were a validated result.
   - *Why it matters:* Practitioners reading the abstract may take "4 cycles" as a design number rather than an output of assumed parameters. The Lutz model was developed for land-mobile channels, not ISL self-blockage.
   - *Remedy:* (a) In the abstract and conclusion, qualify the GE result: "GE inter-cycle P95 recovery in 4 cycles *at illustrative parameters* ($p_{BG}=0.50$); sensitivity curves (Fig. 5b) span 3–18 cycles across the plausible range." (b) Add a brief discussion of what ISL-specific measurements would be needed to calibrate the GE model (e.g., antenna pattern measurements, structural blockage geometry analysis).

3. **The paper claims a "two-layer" (or "three-layer") feasibility framework, but the layers are not cleanly independent.**
   - *Issue:* The byte budget (Layer 1) and TDMA airtime (Layer 2) are presented as separate tests, but they share parameters ($k_c$, $S_{\text{eph}}$, $T_c$) and the MAC translation ($\eta_{\text{total}}/\gamma$) bridges them in a way that blurs the boundary. Table IV lists $\eta_{\text{total}}/\gamma$ as a column but notes it is "necessary but not sufficient." Algorithm 1 interleaves the layers.
   - *Why it matters:* The framework's value to practitioners depends on clarity about what each layer tests and when each is binding.
   - *Remedy:* Add a concise 2–3 sentence paragraph explicitly stating: "Layer 1 is binding when $\eta_{\text{total}} > 1$ (byte budget exceeded regardless of MAC). Layer 2 is binding when $\eta_{\text{total}} < 1$ but half-duplex airtime is exceeded (the 24 kbps case). The MAC translation $\eta_{\text{total}}/\gamma$ is a necessary condition for Layer 2 feasibility but does not capture half-duplex partitioning." This would crystallize the framework.

4. **Scale-invariance of $\eta$ is by construction, not a finding.**
   - *Issue:* The paper presents $\eta = 46\%$ across $10^3$–$10^5$ as a result (Table VII, Fig. 11), but with fixed $k_c$ and fixed message sizes, per-node overhead is independent of $N$ by the hierarchical decomposition itself.
   - *Why it matters:* Presenting a tautology as an empirical finding weakens the paper's credibility.
   - *Remedy:* State explicitly in Section IV-F: "Scale-invariance of $\eta$ with $N$ at fixed $k_c$ is a structural property of the hierarchical decomposition (Eq. 2), not an empirical finding. The DES confirms this property holds under stochastic failures and GE losses." This reframes the result honestly while preserving its utility.

5. **The paper length is excessive for the technical content.**
   - *Issue:* At ~12,000 words of body text plus extensive tables and figures, the paper substantially exceeds typical IEEE TAES length. Much content is repeated across sections.
   - *Why it matters:* Reviewer and reader fatigue; key contributions are diluted.
   - *Remedy:* Target ~20% reduction. Specific candidates for compression: (a) DES verification (Major Issue 1); (b) the sectorized mesh, which is acknowledged as functionally non-comparable and could be a footnote; (c) the fleet-level reuse analysis (Section IV-A, Eq. 8), which addresses an edge case and could move to an appendix; (d) repeated statements of the same numerical results across abstract, introduction, results, and conclusion.

## Minor Issues

1. **Eq. (1)** is not an equation—it is a label for the hierarchy levels. Consider removing the equation number or replacing with a figure reference.

2. **Table I notation:** $\gamma$ is listed with two specific values and a section reference. Consider simplifying to "$\gamma$: MAC efficiency (Section IV-J)" and listing specific values only where used.

3. **Section III-A, "Evidence tiers":** The IEEE 1012 citation is for V&V of software/hardware systems, not specifically for simulation evidence tiers. The mapping is reasonable but should be noted as an adaptation, not a direct application.

4. **Table III, collision avoidance rate:** $10^{-4}$/node/s is stated as Poisson, but the footnote says "screening notifications." Clarify whether this rate is per-node or fleet-wide, and whether it represents the rate of *alerts generated* or *alerts requiring action*.

5. **Section IV-A, "Phase-staggered scheduling":** Fig. 3 is referenced but the phase-stagger analysis is not connected to the main feasibility framework. Is phase-staggering assumed in the recommended design point? Clarify.

6. **Eq. (11), $\gamma$ general expression:** The $10^{-3}$ unit conversion factor is error-prone. Consider expressing entirely in consistent units (seconds and bits, or milliseconds and kilobits) to reduce practitioner implementation errors.

7. **Table IX (Claim Map):** The "Ext." column contains only "NS-3" and "Future"—consider merging these or adding a brief note on what specific NS-3 experiments would be most informative.

8. **Section V-B, dynamic topology:** The J2 perturbation analysis is valuable but appears only in the limitations section. Consider promoting the key result (re-association overhead $<0.3\%$) to the main results with a brief derivation.

9. **Abstract:** "CCSDS Proximity-1 standards-grounded derivation yields $\gamma = 0.76$ (24 kbps), confirming 30 kbps as the minimum viable coordinator PHY rate"—the logical connection between $\gamma$ at 24 kbps and 30 kbps being the minimum is not self-evident in the abstract. Add "since $\gamma_{24} = 0.76$ makes 24 kbps infeasible (Table VI)."

10. **Fig. 5(a):** The DES bars and Markov-chain CDF overlap almost perfectly. Consider using a residual plot or explicitly noting the maximum deviation to make the comparison more informative.

11. **"Project Dyson Research Team" authorship:** While the footnote promises individual names for final publication, IEEE policy typically requires named authors at submission. The editor should clarify whether this is acceptable.

12. **Reference [55] (dyson_multimodel):** This is a self-citation to an unpublished work at a project URL. It should either be submitted as a companion paper or the AI methodology details should be incorporated into this manuscript's acknowledgment section.

---

## Overall Recommendation
**Recommendation: Major Revision**

This paper makes a useful engineering contribution by providing a complete parametric sizing framework for hierarchical coordination in large spacecraft swarms, with careful byte-level accounting, a well-structured feasibility test (Algorithm 1), and a standards-grounded MAC efficiency derivation. The campaign duty factor $d$ effectively addresses workload realism, and the $\gamma$ unification at 0.76 via CCSDS Proximity-1 is consistently applied and well-motivated. The tiered evidence framework and open-source release set a high standard for reproducibility.

However, the paper suffers from three interrelated weaknesses that require revision. First, the DES verification consumes disproportionate space for results that are tautological by construction; the genuine DES contribution (distributional analysis) should be retained but the verification tables compressed. Second, the GE channel results are presented with a specificity that exceeds their evidential basis—the sensitivity sweeps are valuable, but the default-parameter conclusions should be qualified more prominently. Third, the paper is substantially overlong, with key results repeated across multiple sections; a 20% reduction focused on the areas identified above would significantly improve readability and impact.

The strongest technical contributions—the slot-level TDMA analysis revealing ARQ×TDMA coupling, the CCSDS-grounded $\gamma$ decomposition, the unicast stagger equation, and the feasibility algorithm—deserve prominent treatment in a more focused manuscript. The generalized $\gamma$ expression (Eq. 11) is genuinely useful for practitioners and should be highlighted as a standalone contribution.

## Constructive Suggestions

1. **Restructure around the feasibility algorithm.** Make Algorithm 1 the central organizing element; present each equation as it appears in the algorithm's flow. This would eliminate much of the current repetition and give practitioners a clear entry point.

2. **Elevate the slot-level and packet-level results.** These provide the paper's strongest cross-model evidence. The ARQ×TDMA coupling finding (52.7% misses at 24 kbps) is the most operationally significant result and should be more prominent—consider making it a key finding in the abstract.

3. **Provide a single-page "practitioner's summary"** (perhaps as a structured sidebar or appendix) containing: the feasibility algorithm, the $\gamma$ equation with worked example, the duty-factor table, and the GE design curves. This would maximize the paper's practical impact.

4. **Engage more deeply with network calculus.** The periodic, deterministic traffic model is ideal for network calculus bounds. A brief comparison showing that the sizing equations produce results consistent with (or tighter than) network calculus service curves would strengthen the theoretical grounding.

5. **Add a "what would change the conclusions" paragraph.** Explicitly identify which assumptions, if violated, would invalidate the key results (e.g., "if $\gamma < 0.60$ due to unmodeled interference, the 30 kbps design point fails; if command generation is cluster-local, $\eta_{\text{cmd}}$ drops by ~10×"). This would help practitioners assess applicability to their specific missions.

6. **Consider splitting the paper.** The TDMA/MAC analysis (Sections IV-A, IV-D, IV-J) and the message-layer sizing (Sections IV-B, IV-C, IV-E) are somewhat independent contributions. A focused letter on the CCSDS-grounded feasibility boundary (with the $\gamma$ decomposition and ARQ coupling result) might have higher impact than the current comprehensive treatment.