---
paper: "02-swarm-coordination-scaling"
version: "df"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-03-05"
recommendation: "Unknown"
---



# Peer Review: "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version DF)

---

## 1. Significance & Novelty
**Rating: 3 (Adequate)**

The paper addresses a genuine gap: closed-form parametric sizing equations for hierarchical coordination in large autonomous spacecraft swarms at the 10³–10⁵ scale. The two-test feasibility framework (byte budget + TDMA airtime) is a useful conceptual contribution, and the campaign duty factor parameterization is a sensible engineering abstraction. However, the core novelty is modest. The individual analytical components—TDMA slot budgeting, M/D/1 queueing, Gilbert-Elliott channel modeling, AoI under geometric sampling—are well-established. The contribution is primarily in their *assembly* for this specific application context. The paper would benefit from a clearer articulation of what is genuinely new versus what is a known technique applied to a new parameter regime. The claim of being the first to provide "closed-form parametric sizing relationships for coordination architectures across 10³–10⁵ nodes with byte-level traffic accounting" is plausible but hard to verify given the breadth of constellation and sensor network literature.

## 2. Methodological Soundness
**Rating: 3 (Adequate)**

The analytical framework is internally consistent and the equations are correctly derived from stated assumptions. The three-layer feasibility decomposition (byte budget, MAC efficiency, TDMA airtime) is logically structured, though as the paper itself notes, the MAC efficiency layer ($C_{\text{raw}} = C_{\text{coord,info}}/\gamma$) is a unit conversion within Test B rather than an independent test—this is appropriately clarified. The campaign duty factor $d$ is a welcome addition that substantially improves workload realism over a continuous-duty assumption. The mapping in Table VII from mission phases to $(d, q)$ pairs is practical, and the empirical anchoring to ESA conjunction statistics grounds the default $d = 0.10$.

However, several methodological concerns remain:

- The DES verification is acknowledged as Tier 1 (confirming its own equations), which is honest but raises the question of what the simulation adds beyond the closed-form results. The distributional tails (Fig. 4) under campaign burstiness are the claimed incremental contribution, but these are conditioned on an assumed ON/OFF Markov burst model with no empirical basis.
- The GE channel model parameters ($p_G$, $p_B$, $p_{GB}$, $p_{BG}$) are acknowledged as illustrative, but the paper draws specific quantitative conclusions from them (e.g., "27% intra-cycle recovery," "P95 = 4 cycles") that may mislead readers into treating these as validated performance predictions.
- The slot-level simulator and the analytical model share the same $\gamma$ computation; the packet-level "validation" in Section IV-J is parameter anchoring, not independent validation. This is stated but could be more prominently flagged.

## 3. Validity & Logic
**Rating: 4 (Good)**

The internal logic is generally sound and self-consistent. The gamma unification around CCSDS-derived values (0.76 at 24 kbps, 0.745 at 30 kbps, 0.732 at 35 kbps) is consistently applied throughout—I verified this across Tables III, IV, V, VIII, IX, X, and Algorithm 1. The earlier Model S value (0.949) is properly quarantined to Table VI and Fig. 3 with clear "not for design" labels. The stress-case $\eta_S \approx 46\%$ is now properly contextualized as a continuous-duty upper bound occurring <1% of operational time (Table VII, yearly mixture calculation yielding $\bar{\eta} = 5.6\%$). This is a significant improvement.

The rate ladder (Table IV) provides a clear logical chain from information rate through slot overhead, half-duplex allocation, to PHY rate recommendation. The distinction between $\alpha_{\text{RX}}$ as a computed output (not a free parameter) is correctly maintained.

One logical concern: the paper claims topology-invariance of command overhead under centralized command generation, but then introduces Raft consensus (Eq. 8) as an alternative that breaks this invariance. The conditions under which the topology-invariance claim holds should be stated more precisely as a conditional rather than a general property.

## 4. Clarity & Structure
**Rating: 3 (Adequate)**

The paper is dense but generally well-organized. The roadmap at the start of Section IV is helpful. The notation table (Table I) is comprehensive. The two-test feasibility framework box is a good structural device.

However, the paper suffers from significant information overload. At approximately 12,000 words of technical content (excluding references), it attempts to cover architecture design, TDMA sizing, link budgets, GE channel modeling, AoI analysis, buffer sizing, fleet-level reuse, spatial interference, Raft consensus, coordinator failure transients, thundering herd analysis, and more. Many of these topics receive only cursory treatment (e.g., the thundering herd footnote, the sectorized mesh model) that adds complexity without proportionate insight.

The repeated caveats ("no external validation exists," "what-if design tool," "preliminary estimates") are appropriate but become somewhat numbing by repetition. Consider consolidating these into a single prominent limitations statement rather than distributing them throughout.

Specific clarity issues:
- The relationship between $C_{\text{node}}$ (1 kbps logical allocation), the S-band channel (35 kbps PHY), and the link budget aggregate capacity (>200 kbps) requires careful reading of Table II and Section III-E to understand. A simple figure showing the rate hierarchy would help.
- The superframe structure (Table V) would benefit from a timing diagram figure.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**

The paper is exemplary in its transparency. The AI disclosure is specific (tools named, scope of use delineated). Data availability is comprehensive (GitHub repository with tagged release, all simulators, configuration files). The V&V tier structure explicitly labels what is confirmed by construction versus what requires external validation. The claim map (Table XI) is an unusually honest and useful device. The paper repeatedly and prominently states the absence of external validation. This level of intellectual honesty is commendable and sets a good standard.

## 6. Scope & Referencing
**Rating: 3 (Adequate)**

The reference list (55 items) covers the major relevant areas: CCSDS standards, constellation operations, swarm robotics, distributed systems theory, AoI, and queueing theory. The CCSDS Proximity-1, DVB-RCS2, and ITU-R P.681 references appropriately ground the physical-layer assumptions.

However, several gaps exist:
- No reference to the substantial body of work on TDMA scheduling for LEO satellite networks (e.g., Ekici et al., IEEE JSAC 2001; Alagöz et al.).
- The AoI treatment cites foundational work but misses recent results on AoI in scheduled access systems (e.g., Talak et al., IEEE Trans. Info. Theory, 2020).
- Network calculus is mentioned (Le Boudec) but not applied; if it's relevant, it should be used or the citation removed.
- The DVB-RCS2 comparison ($\gamma = 0.70$–$0.85$) is valuable but deserves more than a passing mention—it's the closest empirical anchor for the $\gamma$ range.
- Some references are non-archival (Amazon Kuiper overview, DARPA program pages, DoD fact sheets); while understandable for context, they weaken the scholarly foundation.

---

## Major Issues

**1. The DES provides negligible independent value and should be reframed or reduced.**

The paper honestly acknowledges that DES mean-value agreement is "by construction" (Tier 1). The claimed incremental contribution—distributional tails under campaign burstiness (Fig. 4)—is conditioned on an assumed ON/OFF Markov model with no empirical calibration. The buffer multipliers (1.30× for $d=0.10$, 1.50× for $d=0.50$) are artifacts of this assumed model. A reader cannot distinguish whether these tails reflect real operational risk or simply the assumed burst distribution.

*Why it matters:* The DES consumes significant manuscript space (Sections III-A, III-D, IV-F) and creates an impression of validation that doesn't exist. The 30 MC replications, bootstrap CIs, and runtime statistics suggest rigor that is undermined by the tautological nature of the verification.

*Remedy:* Either (a) reduce the DES to a brief implementation-verification paragraph and remove Fig. 4 and Section IV-F, redirecting that space to strengthening the analytical contributions; or (b) use the DES to explore scenarios that the closed-form equations *cannot* capture (e.g., correlated failures, priority preemption, dynamic cluster reassignment) and present those as the DES's unique contribution.

**2. The GE channel model conclusions are presented with more specificity than the evidence supports.**

Specific quantitative claims ("27% intra-cycle recovery," "P95 = 4 cycles," "52.7% deadline misses") are derived from assumed GE parameters ($p_G = 0.01$, $p_B = 0.90$, $p_{GB} = 0.05$, $p_{BG} = 0.50$) that have no ISL measurement basis. While the paper labels the GE model a "what-if design tool," the specific numbers propagate into design recommendations (e.g., "35 kbps recommended" partly because of GE ARQ demands).

*Why it matters:* The 35 kbps recommendation is the paper's primary actionable output. If the GE parameters are wrong by a factor of 2 in either direction, the recommendation could shift to 30 kbps or 40+ kbps. The sensitivity analysis (Fig. 2b) partially addresses this but only varies $p_{BG}$, not the full parameter space.

*Remedy:* (a) Present a full sensitivity analysis varying $p_B$, $p_{BG}$, and $M_r$ jointly, showing the region of GE parameter space where each PHY rate is feasible. (b) More prominently condition the 35 kbps recommendation on the GE regime: "35 kbps is recommended *if* the channel exhibits slow fading with $p_B \geq 0.7$ and $p_{BG} \leq 0.5$; otherwise 30 kbps suffices." (c) Consider whether the Lutz et al. land-mobile satellite channel model parameters can be adapted to provide at least order-of-magnitude ISL channel estimates.

**3. The paper lacks a clear comparison with existing TDMA sizing methodologies.**

The TDMA slot efficiency derivation (Eq. 14) is presented as a contribution, but TDMA frame efficiency analysis is standard in satellite communication system design (e.g., Maral & Bousquet, "Satellite Communications Systems"; Elbert, "Introduction to Satellite Communication"). The DVB-RCS2 comparison ($\gamma = 0.70$–$0.85$) is mentioned but not developed.

*Why it matters:* Without comparison to existing TDMA sizing approaches, it's unclear what the paper adds beyond applying known methods to a specific parameter set. The generalized $\gamma$ expression (Eq. 14) is useful but not novel.

*Remedy:* Add a brief comparison showing how the paper's $\gamma$ derivation relates to standard TDMA efficiency calculations in satellite communications textbooks and DVB-RCS2 specifications. Highlight what is specific to the swarm coordination context (e.g., the rate-dependent parameterization under CCSDS framing, the coupling with ARQ and half-duplex constraints).

**4. Static cluster membership is a significant limitation that is insufficiently addressed.**

The paper assumes static cluster membership for the entire 1-year simulation duration and claims this is "exact for co-planar formations." The J2 analysis in Section V-C estimates <0.3% overhead for cross-plane reassociation, but this analysis is cursory (one sentence) and doesn't address the transient coordination disruption during reassociation.

*Why it matters:* For the target scale (10⁴–10⁵ nodes), many practical constellation geometries (Walker constellations, heterogeneous orbits) will have significant cross-plane relative motion. Cluster reassociation involves coordinator handoff, state transfer, and potential coordination gaps—exactly the scenarios where the sizing equations are most stressed.

*Remedy:* Either (a) restrict the scope explicitly to co-planar formations and remove claims about cross-plane applicability, or (b) provide a more rigorous analysis of reassociation frequency, duration, and overhead for representative Walker constellation geometries, including the impact on AoI and coordination availability during transitions.

**5. The coordinator single-point-of-failure analysis is incomplete.**

The coordinator failure transient analysis (Section III-B.2) provides order-of-magnitude estimates but doesn't fully address the operational impact. The thundering herd analysis is relegated to a footnote. The claim that "hierarchical coordination is suspended" during RF-backup is significant but its implications for mission safety are hand-waved ("conjunction probability per node per 300 s ≈ 10⁻⁸").

*Why it matters:* For a system designed to coordinate 10⁴–10⁵ nodes, coordinator failure is a critical design driver. The paper's sizing equations assume a functioning coordinator; the failure mode analysis should be proportionate to the system's dependence on this assumption.

*Remedy:* Promote the coordinator failure analysis from footnotes and parenthetical remarks to a proper subsection. Quantify: (a) expected number of coordination gaps per year per cluster; (b) duration distribution of gaps under different failure modes; (c) impact on fleet-level coordination availability (not just per-cluster). Consider whether dual-coordinator architectures change the sizing equations.

---

## Minor Issues

1. **Table I notation:** $\alpha_{\text{RX}}$ is described as both "Ingress fraction of $T_c$" and "Computed output of Alg. 1 (line 6), not a free parameter." The second description belongs in the algorithm, not the notation table. Keep the notation table clean.

2. **Eq. 1 ($M_{\text{total}}$):** The equation counts messages but the paper's primary metric is bytes/bandwidth. Clarify the connection or remove.

3. **Section III-B.2, "Operational impact":** The parenthetical "(order-of-magnitude estimate; simulation validation needed)" should be a proper caveat, not a parenthetical.

4. **Table III (link budget):** The system noise temperature is listed as "290 K + 50 K" but the dBm/Hz value (-173.7) corresponds to 340 K. This is correct but should be written as $T_{\text{sys}} = 340$ K for clarity.

5. **Eq. 6 ($\gamma = 0.949$):** Despite clear labeling as Model S, this equation appears before the Model C derivation (Eq. 14). Consider reordering to present Model C first, then Model S as the simplified bound.

6. **Table VI:** The caption says "Model S Only" but this isn't visually prominent enough given the paper's emphasis on Model C for all design decisions. Consider adding a colored/shaded header or bold warning.

7. **Section IV-B (AoI):** The statement "DES: 441 s (95% CI: [438, 444] s)" for a quantity analytically computed as 440 s is a 1-second discrepancy that adds no information. The CI width (6 s) on a 441 s quantity is meaninglessly precise for a design tool.

8. **Algorithm 1, Line 3:** The Test A computation includes $\eta_{\text{baseline}}$ in $\eta_{\text{total}}$ but the comment says "$\eta_0 = 5\%$ (hb+summ+elec); $\eta_{\text{baseline}} = 20.5\%$"—clarify that $\eta_0$ and $\eta_{\text{baseline}}$ are distinct additive terms.

9. **Section IV-A:** "Phase-staggered scheduling ($\phi_j = (j/n_{\text{clusters}}) \times T_c$) spreads the regional ingress burst; DES confirms zero drops at ≥25 kbps vs. 50 kbps under random phase." This is a significant result buried in a single sentence. Either develop it or remove it.

10. **References:** [3] (Amazon Kuiper) and [48] (Project Dyson multi-model AI) are non-archival and self-referential respectively. Consider whether they're necessary.

11. **Abstract:** At 198 words, the abstract is dense but within IEEE limits. However, it contains too many specific numbers ($\gamma \approx 0.70$–$0.76$, 35 kbps, 27 kbps, 5 ms, 4.7 ms, 46%, <1%) that obscure the high-level message. Simplify.

12. **Section II-B:** The list of references (Reynolds, Brambilla, Dorigo, LEACH, ACO, PSO, ABC, Lamport, Raft, Olfati-Saber, Ren & Beard, GNN, mean-field games, OFFSET, Blackjack, Replicator, SWIM) reads as a catalog rather than a critical review. Trim to the most relevant and explain *how* each relates to the current work.

13. **Eq. 8 ($\eta_{\text{consensus}}$):** The stability limit $f_{\text{decision,max}} \approx 24$ is stated without derivation. Show the inequality from which this is derived.

14. **"Tight formation control requires optical ISL"** (abstract): This scope exclusion should be justified more explicitly. Why can't the S-band channel support tight formation control with appropriate protocol design?

---

## Overall Recommendation
**Recommendation: Major Revision**

This paper makes a useful engineering contribution by assembling known analytical tools (TDMA slot budgeting, queueing theory, GE channel modeling, AoI analysis) into a coherent two-test feasibility framework for sizing hierarchical coordination in large spacecraft swarms. The campaign duty factor parameterization is a practical and well-motivated addition that substantially improves workload realism. The paper is commendably transparent about its limitations, validation gaps, and the preliminary nature of its results—the claim map (Table XI) and V&V tier structure set a high standard for intellectual honesty.

However, the paper has significant issues that prevent acceptance in its current form. The DES verification adds negligible independent value beyond confirming its own equations, yet consumes substantial manuscript space. The GE channel model conclusions are presented with more quantitative specificity than the assumed (unmeasured) parameters warrant, and the primary design recommendation (35 kbps) is partly conditioned on these unvalidated parameters. The static cluster membership assumption limits applicability to co-planar formations without adequate acknowledgment. The paper attempts to cover too many topics (TDMA sizing, link budgets, GE modeling, AoI, buffer sizing, fleet reuse, spatial interference, Raft consensus, coordinator failure, thundering herd) at insufficient depth for any single one to constitute a strong contribution.

The most impactful revision would be to sharpen the paper's focus: either (a) present the two-test feasibility framework and Algorithm 1 as the primary contribution with the GE and DES material reduced to supporting roles, or (b) develop the ARQ×TDMA coupling analysis into a deeper contribution with proper comparison to existing TDMA sizing methodologies. In either case, the GE-conditioned recommendations should be presented as parametric design curves rather than point estimates, and the DES should either be reduced or redirected toward scenarios the closed-form equations cannot address.

---

## Constructive Suggestions
*(Ordered by impact)*

1. **Sharpen the contribution statement.** The two-test framework + Algorithm 1 + campaign duty factor is the core contribution. Present it as such, with the GE analysis and DES as supporting material rather than co-equal contributions.

2. **Replace GE point estimates with parametric design regions.** Instead of "35 kbps recommended," present a figure showing the feasible PHY rate as a function of ($p_B$, $p_{BG}$, $M_r$) jointly. This is more useful to practitioners and avoids over-specificity from assumed parameters.

3. **Reduce the DES to a verification paragraph** or redirect it toward scenarios that closed-form equations cannot capture (correlated failures, dynamic reassociation, priority preemption).

4. **Add a TDMA sizing comparison** with DVB-RCS2 and standard satellite communications references to establish what is genuinely new in the $\gamma$ parameterization.

5. **Develop the coordinator failure analysis** into a proper subsection with quantified availability impact at fleet scale.

6. **Add a timing diagram figure** for the TDMA superframe to complement Table V—this would significantly improve accessibility.

7. **Trim Section II** to focus on the most directly relevant prior work, with explicit statements of how each reference relates to the current contribution.

8. **Simplify the abstract** to convey the high-level message without excessive numerical detail.

9. **Consider splitting** the paper into two: (a) the feasibility framework and sizing equations (Sections IV-A, IV-E, V-D, Algorithm 1); (b) the channel modeling and ARQ analysis (Sections IV-C, IV-D, IV-J). Each would be stronger as a focused contribution.