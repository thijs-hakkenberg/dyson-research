---
paper: "02-swarm-coordination-scaling"
version: "dj"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-03-06"
recommendation: "Unknown"
---



# Peer Review: Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms

## 1. Significance & Novelty
**Rating: 3 (Adequate)**

The paper addresses a genuine gap: closed-form parametric sizing for hierarchical coordination at $10^3$–$10^5$ node scales with byte-level traffic accounting. The two-test feasibility framework (byte budget + TDMA airtime) is a useful conceptual contribution, and the campaign duty factor $d$ is a sensible parameterization for bridging continuous-duty bounds to realistic operational profiles. However, the novelty is primarily in the *assembly* of well-known components (TDMA slot efficiency formulas, GE channel models, M/D/1 queueing, Raft consensus, AoI analysis) rather than in any individual analytical advance. The $\gamma$ formula (Eq. 12) is acknowledged as standard (cf. DVB-RCS2). The core insight—that coordinator ingress is the binding constraint at 1 kbps per-node budgets and that 35 kbps PHY suffices—is useful for practitioners but narrow in scope.

## 2. Methodological Soundness
**Rating: 3 (Adequate)**

The three-layer feasibility framework (byte budget, MAC efficiency, TDMA airtime) is logically structured, and the paper is commendably transparent about what each layer does and does not capture. The analytical equations are straightforward and appear correct. Several methodological concerns remain:

- The DES is cycle-aggregated and message-layer only; it shares the same equations as the closed-form analysis, making mean-value agreement tautological (acknowledged as Tier 1). The distributional tail analysis (Fig. 4) provides incremental value but is conditioned on assumed burst models with no empirical grounding.
- The slot-level simulator reveals the ARQ×TDMA coupling (Table VI), which is the most substantive non-tautological simulation result. However, this too follows directly from the timing arithmetic—it confirms that 730 ms < 1,288 ms, which is apparent from the closed-form analysis.
- The GE channel model is parameterized with illustrative values ($p_{BG} = 0.50$, $p_B = 0.90$) that lack ISL measurement support. While the paper correctly labels this a "what-if design tool," the extensive analysis around these specific parameters (inter-cycle recovery CDFs, P95 values) risks creating false precision.

## 3. Validity & Logic
**Rating: 4 (Good)**

The internal logic is generally sound and self-consistent. The paper has clearly evolved through multiple revisions, and several previously problematic areas have been addressed:

- The campaign duty factor $d$ now adequately contextualizes the stress-case $\eta_S \approx 46\%$ as a continuous-duty upper bound occurring <1% of operational time. The yearly mixture calculation ($\bar{\eta} = 5.6\%$) and the mission-phase mapping (Table VIII) are helpful.
- The gamma unification around Model C (0.73–0.76 from CCSDS Proximity-1) is consistently applied throughout. Model S appears only as a comparison curve. The $\gamma$ consistency ledger in Table X is a good practice.
- The stress-case is now properly framed. The distinction between $d$ (campaign duty) and $p_{\text{cmd}}$ (conditional command probability) is clear.
- The three-layer framework is internally consistent: Test A and Test B are well-defined, and the paper correctly notes that the $C_{\text{raw}} = C_{\text{coord,info}}/\gamma$ conversion is embedded in Test B, not a separate check.

One logical concern: the paper claims $\eta$ is "invariant to $k_c \in \{50, 100, 200, 500\}$ ($\pm 0.1\%$)" (Section IV-G), but $\eta_0$ includes coordinator summaries that amortize differently with $k_c$ (acknowledged in Algorithm 1 footnote: $\eta_0 \approx 5.4\%$ at $k_c = 200$). This is minor but the "invariant" claim should be softened.

## 4. Clarity & Structure
**Rating: 3 (Adequate)**

The paper is extraordinarily detailed—perhaps excessively so. At its current length and density, it reads more like a technical report than a journal article. Key issues:

- **Information overload:** The paper contains 12 tables, 5 figures, 1 algorithm, and extensive inline calculations. Many results are stated multiple times in different forms (e.g., the 35 kbps recommendation appears in the abstract, Section IV-A, Table IV, Table IX, Table X, Section V-C, and Section VI). While internal consistency is good, the repetition obscures the core contribution.
- **Notation table:** Table I is comprehensive but the sheer number of symbols (>25) signals excessive parameterization for what is fundamentally a straightforward TDMA sizing problem.
- **Roadmap effectiveness:** The paper provides roadmaps (Section IV header) but the section organization still feels like an accretion of analyses rather than a narrative arc. The reader must work hard to extract the key takeaways.
- **Defensive writing:** Extensive caveats, boundary conditions, and disclaimers (e.g., "All results are preliminary per-cluster design estimates lacking external validation") are appropriate but their frequency disrupts readability.

The figures are functional. Fig. 3 (cross-cycle recovery) and Fig. 5 (gamma vs. rate) are the most informative. Fig. 1 (architecture) is generic. Fig. 2 (margin sensitivity) and Fig. 4 (buffer CDF) provide limited insight beyond confirming the equations.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**

The paper is exemplary in transparency: code/data availability with a specific repository tag, explicit AI disclosure (ideation only, not results/figures), clear identification of all assumptions, and honest labeling of validation gaps. The claim map (Table XI) is a model of scientific honesty. The V&V tier structure (Section III-A) clearly delineates what is confirmed vs. assumed.

## 6. Scope & Referencing
**Rating: 3 (Adequate)**

The references are appropriate and span the relevant domains (CCSDS standards, swarm robotics, constellation management, queueing theory, AoI). However:

- Several references are non-archival (Amazon Kuiper overview, DARPA program pages) and should be flagged or replaced where possible.
- The paper could benefit from citing recent work on LEO ISL channel characterization (if any exists) to better contextualize the GE parameter choices.
- Network calculus [Le Boudec] is cited but not used; the paper could strengthen its contribution by providing deterministic worst-case bounds alongside the mean-value analysis.
- The DVB-RCS2 comparison for $\gamma$ is mentioned but not developed—a more detailed comparison would strengthen the standards-based anchoring claim.

---

## Major Issues

1. **The DES verification provides negligible independent value beyond confirming its own equations.**
   - *Issue:* The paper acknowledges (Section V-A, Table XI) that DES mean-value agreement is "by construction" (Tier 1). The distributional tails (Fig. 4) are the claimed incremental contribution, but these are conditioned on assumed burst models (ON/OFF Markov with $L_{\text{on}} = 100$) that have no empirical basis. The buffer factor $M = 1.30$ is a prediction under these assumptions, not a validated finding.
   - *Why it matters:* A significant portion of the paper (Section III, Section IV-F) is devoted to the DES framework, yet its incremental contribution over the closed-form analysis is minimal. This inflates the paper's length without proportionate insight.
   - *Remedy:* Either (a) substantially reduce the DES description to a brief verification appendix, acknowledging it as implementation confirmation only, or (b) use the DES to explore scenarios that the closed-form analysis *cannot* handle (e.g., correlated failures, dynamic topology, priority preemption)—which would require extending the simulation model.

2. **The packet-level validation (Section IV-J) does not provide adequate independent validation.**
   - *Issue:* The $\gamma$ derivation from CCSDS Proximity-1 framing is a standards-based *calculation*, not a measurement. It uses the same formula (Eq. 12) that feeds into all other analyses. The paper correctly labels this "standards-based parameter estimate (not a measurement)" but then devotes substantial space to it as if it were validation.
   - *Why it matters:* Without hardware measurements of actual slot efficiency (including acquisition failures, Doppler effects, antenna pattern variations), the entire TDMA feasibility analysis rests on assumed parameters. The $\gamma = 0.745 \pm 0.07$ uncertainty band is an engineering estimate, not a confidence interval.
   - *Remedy:* (a) Reduce the framing of Section IV-J from "validation" to "parameter derivation." (b) Provide a clearer sensitivity analysis: what is the *minimum* $\gamma$ at which the 35 kbps recommendation fails? (The paper partially does this but it's scattered.) (c) Consider whether a simple table showing $R_{\text{PHY,min}}$ vs. $\gamma$ (which exists as Table X) could replace much of the detailed derivation.

3. **The paper lacks any external validation, limiting the strength of all quantitative claims.**
   - *Issue:* Every quantitative result (overhead percentages, PHY rate recommendations, recovery times) is derived from the same internal model. The validation roadmap (Section V-B) identifies the needed steps but none have been taken.
   - *Why it matters:* For a journal publication, the complete absence of external validation—even a comparison with NS-3 for a simplified scenario, or a bench measurement of $\gamma$ on a COTS S-band radio—significantly limits the paper's contribution. The results are internally consistent design *estimates*, not validated findings.
   - *Remedy:* At minimum, provide one external anchor point: (a) an NS-3 simulation of the TDMA scheduling for a single cluster, or (b) a bench measurement of slot efficiency on representative hardware, or (c) a detailed comparison with published DVB-RCS2 slot efficiency measurements. If none is feasible for this submission, the paper should be reframed as a "design methodology" paper rather than a "results" paper, with the title and claims adjusted accordingly.

4. **The paper is substantially too long and repetitive for a journal article.**
   - *Issue:* At its current length (estimated 12–14 journal pages with figures/tables), the paper exceeds typical IEEE TAES limits. More importantly, the core contribution (two-test framework, rate ladder, Algorithm 1) could be communicated in roughly half the space. The extensive inline calculations, repeated results, and defensive caveats dilute the impact.
   - *Why it matters:* Reviewers and readers will struggle to identify the key contributions amid the detail. The paper's value as a practitioner reference is undermined by its density.
   - *Remedy:* (a) Move the DES framework details, link budget, and margin analysis to appendices or supplementary material. (b) Consolidate the rate feasibility analysis into a single comprehensive table rather than distributing it across Tables IV, V, IX, X, and XI. (c) Reduce the GE channel analysis to the sensitivity sweep (Fig. 3b) and the key conclusion (35 kbps for slow fading, 30 kbps for fast fading). (d) Target 8–10 journal pages.

5. **The generalized gamma expression (Eq. 12) is presented as a contribution but is standard.**
   - *Issue:* The paper acknowledges that Eq. 12 is "not novel (cf. DVB-RCS2)" but still devotes significant space to its derivation, decomposition (Table VII), sensitivity analysis (Eq. 13, Fig. 5), and measurement protocol. The actual contribution is the *application* of this formula to the specific ISL TDMA sizing problem with CCSDS framing parameters.
   - *Why it matters:* Overclaiming the $\gamma$ formula as a contribution weakens the paper's credibility. The measurement protocol (Section V-C) is useful but generic.
   - *Remedy:* Present Eq. 12 as a standard formula with CCSDS-specific parameter instantiation. Reduce the derivation to a single table (Table VII is sufficient). The $\gamma$-conditional lookup (Table X) is genuinely useful for practitioners and should be retained.

## Minor Issues

1. **Inconsistent $\eta$ invariance claim:** Section IV-G claims $\eta$ is invariant to $k_c$ ($\pm 0.1\%$), but Algorithm 1 footnote notes $\eta_0$ changes from 5.6% to 5.4% at $k_c = 200$. Clarify that $\eta_{\text{cmd}}$ is invariant but $\eta_0$ has weak $k_c$ dependence.

2. **Collision avoidance rate:** The $10^{-4}$/node/s rate is described as a "conservative upper bound" but is 300× higher than ESA's reported rate. While used as a stress parameter, this should be more clearly flagged as unrealistic in the parameter table.

3. **Thundering herd analysis:** The Slotted ALOHA + BEB analysis (Section III, "Thundering herd") assumes worst-case simultaneous onset but then notes Raft's randomized timeout partially mitigates this. The 140–160 s recovery estimate should include the mitigated case as well.

4. **Table I notation:** $\alpha_{\text{RX}}$ is listed as a "computed output" but appears in Eq. 8 as if it were a parameter. The dependency chain ($\alpha_{\text{RX}}$ depends on $R_{\text{PHY}}$ and $M_r$) should be made more explicit in the equation presentation.

5. **Figure quality:** Fig. 1 (architecture diagram) is referenced but appears generic. Consider adding specific parameter values (fan-out ratios, message sizes) directly on the figure.

6. **Reference [dyson_multimodel]:** This is a self-citation to a non-peer-reviewed preprint. Per IEEE policy, this should be clearly labeled and its role minimized.

7. **Abstract length:** The abstract exceeds typical IEEE limits (~250 words) and contains excessive detail (specific $\gamma$ values, duty factor percentages). Shorten to focus on the framework, key finding (35 kbps recommendation), and the validation gap.

8. **Eq. 5 (hierarchical messages):** The equation assumes uniform fan-out but the text mentions "configurable fan-out." Clarify the uniformity assumption.

9. **"Model S" naming:** Using "Model S" and "Model C" without mnemonic connection (S = Simplified? C = CCSDS?) forces the reader to repeatedly check definitions. Consider "Simplified" and "CCSDS" throughout.

10. **Section IV-J title:** "Standards-Based Slot Efficiency Parameterization" is more accurately a parameter derivation than a "result." Consider moving to Section III or V.

---

## Overall Recommendation
**Recommendation: Major Revision**

This paper tackles a worthwhile problem—parametric sizing for hierarchical coordination in large space swarms—and provides a logically sound, internally consistent framework. The two-test feasibility decomposition (byte budget + TDMA airtime), the campaign duty factor parameterization, and Algorithm 1 are genuinely useful for preliminary mission design. The paper's transparency about assumptions and validation gaps is commendable and sets a good standard.

However, the paper suffers from three fundamental weaknesses that must be addressed. First, the complete absence of external validation means all quantitative claims are internal design estimates; at least one external anchor point (NS-3, hardware measurement, or detailed DVB-RCS2 comparison) is needed for journal publication. Second, the paper is substantially too long, with extensive repetition and detail that obscures the core contribution; a reduction of 30–40% is needed. Third, the DES and packet-level analyses are presented as providing validation when they are largely tautological confirmations of the closed-form equations; their role should be honestly reframed and their presentation condensed.

The strongest elements—the rate ladder (Table IV), the $\gamma$-conditional lookup (Table X), the duty factor mapping (Table VIII), and Algorithm 1—should be foregrounded. The GE sensitivity curves (Fig. 3b) are a useful design tool. With significant condensation, honest reframing of the validation status, and ideally one external validation point, this could become a solid practitioner-oriented contribution to the literature.

## Constructive Suggestions

1. **Add one external validation point.** Even a single-cluster NS-3 simulation comparing TDMA deadline miss rates against Table VI would transform the paper's credibility. Alternatively, bench-test $\gamma$ on a COTS S-band SDR (e.g., USRP + GNU Radio with CCSDS framing).

2. **Reduce length by 30–40%.** Move DES framework details, link budget derivation, and margin inventory to supplementary material. Consolidate rate feasibility into one comprehensive table. Eliminate repeated statements of the 35 kbps recommendation.

3. **Reframe the contribution honestly.** Title suggestion: "Design Methodology and Parametric Sizing for..." rather than implying validated results. Emphasize the framework and sizing procedure (Algorithm 1) as the primary contribution, with specific numeric results as illustrative instantiations.

4. **Strengthen the practitioner value.** The $\gamma$-conditional lookup table (Table X) and the measurement protocol are the most directly useful elements. Consider adding a one-page "quick-start guide" that walks through Algorithm 1 for a specific mission scenario different from the default parameters.

5. **Develop the network calculus connection.** Le Boudec is cited but unused. Deterministic worst-case bounds via network calculus would complement the mean-value analysis and provide a stronger theoretical contribution than the current DES tail analysis.

6. **Clarify the scope boundary with optical ISL.** The paper repeatedly notes that tight formation control requires optical ISL, but the interaction between S-band coordination and optical ISL data paths is underspecified. A clearer operational concept showing when each link is used would help practitioners.