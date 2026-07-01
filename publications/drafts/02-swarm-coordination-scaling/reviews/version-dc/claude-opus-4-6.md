---
paper: "02-swarm-coordination-scaling"
version: "dc"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-03-05"
recommendation: "Unknown"
---



# Peer Review: "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version DC)

---

## 1. Significance & Novelty
**Rating: 3 (Adequate)**

The paper addresses a genuine gap: closed-form parametric sizing for hierarchical coordination at $10^3$–$10^5$ node scales with byte-level traffic accounting. The two-test feasibility framework (byte budget + TDMA airtime) is a useful conceptual contribution, and the campaign duty factor $d$ is a practical parameterization. However, the core contribution is essentially a bookkeeping exercise—summing message sizes, dividing by bandwidth, and checking against a cycle deadline. The novelty lies more in the systematic assembly of known techniques (TDMA scheduling, GE channel models, Raft consensus, AoI analysis) than in new analytical methods. The paper would benefit from a clearer articulation of what is intellectually new versus what is a careful engineering compilation. The absence of any external validation significantly limits the impact claim.

## 2. Methodological Soundness
**Rating: 3 (Adequate)**

The analytical framework is internally consistent and carefully constructed. The three-layer decomposition (byte budget, MAC efficiency, TDMA airtime) is logically sound, and the authors are commendably transparent about what each layer does and does not capture. Several methodological concerns remain:

- The DES is cycle-aggregated and shares the same equations as the analytical model, making mean-value agreement tautological (the authors acknowledge this). The distributional tail analysis (Fig. 4) is the DES's genuine contribution, but the campaign burstiness model (ON/OFF Markov) is itself assumed, not validated.
- The GE channel model is parameterized without ISL measurements. While framed as a "what-if design tool," the specific numerical results (27% intra-cycle recovery, P95 = 4 cycles) are presented with a precision that may mislead readers into treating them as predictions.
- The slot-level simulator confirms the analytical slot-timing equations—again, by construction. The 52.7% deadline miss finding at 24 kbps with $M_r = 1$ is the sole emergent result, and it follows directly from the timing arithmetic.

## 3. Validity & Logic
**Rating: 4 (Good)**

The internal logic is rigorous and well-documented. The paper is unusually honest about its limitations—the validation gap table (Table VIII), the explicit V&V tier structure, and the repeated disclaimers about the absence of external validation are exemplary. Specific strengths:

- The campaign duty factor $d$ adequately addresses workload realism. The mapping from mission phases to $(d, q)$ pairs (Table VI) is practical, and the empirical anchoring to ESA conjunction rates is appropriate.
- The stress-case $\eta_S \approx 46\%$ is now properly contextualized as a continuous-duty upper bound occurring <1% of operational time. The yearly mixture calculation ($\bar{\eta} = 5.6\%$) is convincing.
- The $\gamma$ unification via Eq. (11) is consistently applied throughout, with rate-dependent values ($\gamma_{24} = 0.761$, $\gamma_{30} = 0.745$, $\gamma_{35} = 0.732$) properly tracked.

One logical concern: the paper claims $\eta$ is "scale-invariant" across $N = 10^3$ to $10^5$, but this follows trivially from the per-cluster formulation—it is a modeling assumption (static clusters, no inter-cluster interference), not a finding.

## 4. Clarity & Structure
**Rating: 3 (Adequate)**

The paper is thorough to the point of being overwhelming. At ~12,000 words of dense technical content with 12 tables, 5 figures, and an algorithm, it reads more like a technical report than a journal article. Specific issues:

- The notation table (Table I) is helpful but incomplete—some symbols appear in the text before being defined (e.g., $\alpha_{\text{RX}}$ is used in Section IV-A before its formal definition).
- The two-model framework (Model S vs. Model C) is a source of persistent confusion despite the authors' efforts. Table IV uses Model S "only for illustration" but the reader must constantly track which model applies.
- The paper repeats key results (e.g., "35 kbps recommended") in at least 8 locations. While this aids standalone reading of sections, it inflates length.
- The boxed feasibility framework definition in Section IV is excellent—more of this structured presentation would help.
- Several footnotes contain substantive technical content (e.g., the thundering-herd analysis) that arguably belongs in the main text or an appendix.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**

The paper is exemplary in transparency: code/data availability with a tagged release, explicit AI disclosure, clear acknowledgment of the validation gap, and honest V&V tier labeling. The claim map (Table VIII) is a model of scientific honesty that other papers should emulate.

## 6. Scope & Referencing
**Rating: 3 (Adequate)**

The reference list (55 items) covers the relevant domains but has gaps:

- No citation of actual TDMA scheduling literature for satellite systems (e.g., Pratt & Bostian, or the extensive DVB-S2/RCS literature beyond the single DVB-RCS2 standard reference).
- Network calculus is mentioned but not applied; the Le Boudec reference feels perfunctory.
- The swarm robotics references are dated (Reynolds 1987, Brambilla 2013); more recent work on communication-constrained multi-robot systems is missing.
- No reference to actual ISL measurement campaigns (e.g., EDRS, LCRD) that could provide empirical grounding for the GE parameters.

The paper's scope is appropriate for IEEE T-AES, though the absence of external validation weakens the case for this venue versus a workshop or letters format.

---

## Major Issues

1. **The DES verification is largely tautological and does not justify its prominence.**
   - The DES reproduces the analytical equations to <0.1%—by construction, since both implement the same message-counting logic. The paper acknowledges this (Tier 1) but still devotes significant space to DES results. The distributional tail analysis (Fig. 4) is the sole non-tautological contribution, but it depends on the assumed ON/OFF Markov campaign model, which is itself unvalidated.
   - *Why it matters:* Readers may overestimate the validation status of the results. The DES creates an illusion of independent confirmation.
   - *Remedy:* Reduce DES coverage to a single paragraph acknowledging code verification. Elevate the distributional tail analysis as a clearly labeled "conditional on assumed campaign model" result. Consider removing the DES entirely and presenting the tail analysis as a direct Markov chain calculation.

2. **The packet-level validation (Section IV-J) provides parameter anchoring, not independent validation.**
   - The $\gamma$ derivation from CCSDS Proximity-1 framing is a standards-based calculation, not a measurement. The paper correctly labels this but then uses the term "validated" in several places (e.g., abstract: "0.76 validated via CCSDS"). Computing $\gamma$ from a standard's framing specification is parameter estimation, not validation.
   - *Why it matters:* The word "validated" implies empirical confirmation. Real $\gamma$ depends on acquisition failures, Doppler dynamics, thermal noise, and implementation-specific timing that the CCSDS standard does not capture.
   - *Remedy:* Replace "validated" with "anchored" or "estimated" throughout. Add a sensitivity analysis showing how $\gamma$ uncertainty (e.g., $\pm 15\%$) propagates to the PHY rate recommendation—the paper partially does this but should make it the primary framing.

3. **The three-layer feasibility framework conflates what are really two tests with a unit conversion.**
   - The paper presents "byte budget, MAC efficiency, TDMA airtime" as three layers, but MAC efficiency ($\gamma$) is simply a unit conversion from information bytes to airtime. The authors acknowledge this in the boxed framework ("$\gamma$ is a parameter within Test B, not a separate test") but the three-layer language persists elsewhere.
   - *Why it matters:* Presenting two tests as three inflates the apparent complexity of the framework.
   - *Remedy:* Consistently present the framework as two tests throughout. Remove "three-layer" language.

4. **The generalized $\gamma$ expression (Eq. 11) is useful but its practical value is overstated.**
   - Eq. (11) decomposes slot time into payload, FEC, framing, guard, and acquisition—a straightforward time-budget calculation that any TDMA system designer would perform. The "rate paradox" ($\gamma$ decreases with $R_{\text{PHY}}$) is well-known in TDMA literature.
   - *Why it matters:* Claiming this as a contribution risks appearing naive to the TDMA community.
   - *Remedy:* Frame Eq. (11) as a convenience for practitioners unfamiliar with TDMA design, not as a novel result. Cite prior TDMA slot-efficiency analyses.

5. **No sensitivity analysis on the 1 kbps per-node budget assumption.**
   - The entire paper is conditioned on $C_{\text{node}} = 1$ kbps. Table II-A shows that at $\geq 10$ kbps, all constraints are trivially satisfied. The paper acknowledges this but does not explore the design space between 1 and 10 kbps, which is where the interesting engineering tradeoffs live.
   - *Why it matters:* The 1 kbps assumption drives all the interesting results (TDMA binding, 35 kbps recommendation). If the link budget supports 2 kbps (which it does with 3 dB less margin), the entire TDMA analysis becomes non-binding.
   - *Remedy:* Add a parametric sweep of $C_{\text{node}} \in [0.5, 5]$ kbps showing how the feasibility boundary shifts. This would significantly increase the paper's practical value.

6. **The coordinator failure transient analysis is incomplete.**
   - The thundering-herd analysis (footnote 1) is a back-of-envelope Slotted ALOHA calculation that assumes BEB convergence without modeling the actual election protocol dynamics. The 140–160 s estimate is presented without confidence bounds. The claim that "orbital safety suffices for 300 s" relies on a single conjunction probability estimate.
   - *Why it matters:* Coordinator failure recovery is a critical safety argument. The analysis should be rigorous, not relegated to a footnote.
   - *Remedy:* Either promote this to a proper subsection with a Markov chain model of the election process, or explicitly state that the recovery time is an order-of-magnitude estimate requiring simulation validation.

---

## Minor Issues

1. **Abstract length:** At ~200 words, the abstract is dense but within IEEE limits. However, the phrase "0.76 validated via CCSDS" should be "0.76 estimated from CCSDS framing" per Major Issue 2.

2. **Table I:** $\alpha_{\text{RX}}$ is described as a "computed output" but appears as a parameter in equations before Algorithm 1 computes it. Clarify the dependency order.

3. **Eq. (2):** The hierarchical message count $M_{\text{total}}$ excludes command traffic and heartbeats. State this explicitly.

4. **Section III-B-3 (Sectorized Mesh):** The $k_s = \lceil\sqrt{N}\rceil$ choice is unmotivated. Why square root?

5. **Table IV (Joint Interaction):** The table header says "Model S Only" but the caption says "Illustrative." Standardize the warning language.

6. **Fig. 2 (Cross-cycle recovery):** The figure is referenced before the GE model parameters are fully introduced. Consider reordering.

7. **Eq. (6):** The consensus overhead equation assumes serialized votes over a shared channel. This is a strong assumption that should be flagged—parallel voting over ISL would change the scaling.

8. **Section V-C (Limitations):** "J2 analysis" is mentioned but no J2 perturbation equations are shown. Either provide the calculation or cite a specific result from Vallado.

9. **Table III (Superframe):** The sync beacon at "8 bits at 30 kbps = 0.3 ms" seems unrealistically small for a synchronization function. Clarify what this beacon contains.

10. **Typographical:** "Eq.~\ref{eq:gamma_time}" is referenced ~15 times; consider a shorter label or reducing redundant references.

11. **The paper uses both "kbps" and "bps" without consistent formatting.** Use \si{kbps} throughout.

12. **Section IV-E:** "Full-load: 0.1% of time" appears in running text after the yearly mixture calculation. This should be in Table V or VI for traceability.

13. **Reference [3] (Kuiper):** "Non-archival; accessed February 2026" — this is a future date. Verify.

---

## Overall Recommendation
**Recommendation: Major Revision**

This paper makes a genuine contribution by systematically deriving closed-form sizing equations for hierarchical coordination in large space swarms, assembling a two-test feasibility framework that is logically sound and practically useful. The campaign duty factor parameterization is well-motivated, the stress-case contextualization is now appropriate, and the scientific honesty (validation gap acknowledgment, claim map, V&V tiers) is exemplary—setting a standard that other preliminary-design papers should follow.

However, the paper suffers from three fundamental weaknesses that must be addressed. First, the validation architecture is circular: the DES, slot simulator, and analytical model share the same equations, making their agreement uninformative. The paper needs either genuine external validation (NS-3, hardware measurements) or a much more modest framing that presents the work as a design methodology paper rather than a validated sizing tool. Second, the paper is significantly too long for a journal article, with extensive repetition and technical content in footnotes that should be restructured. Third, the practical value is narrowly conditioned on the 1 kbps assumption; a parametric treatment of the per-node budget would substantially broaden the contribution.

The strongest elements—the two-test framework, Algorithm 1, the $\gamma$-conditional lookup table, and the campaign duty factor mapping—should be preserved and elevated. The weakest elements—the DES mean-value verification, the Model S results, and the extensive repetition—should be compressed or removed.

---

## Constructive Suggestions
*(Ordered by impact)*

1. **Reframe as a design methodology paper.** Drop claims of "validation" for internal tool agreement. Present the framework as: "Given these assumptions, here are the sizing equations and their sensitivity." This is honest and still valuable.

2. **Add a $C_{\text{node}}$ parametric sweep** ($0.5$–$5$ kbps) showing where TDMA analysis becomes binding vs. non-binding. This single figure would double the paper's practical value.

3. **Compress the DES sections** to ~1 paragraph of code verification + the distributional tail figure. Remove all DES mean-value comparisons.

4. **Eliminate Model S from all tables and figures** except a single comparison row. It creates confusion and is never used for recommendations.

5. **Shorten the paper by ~30%.** Consolidate repeated statements of the 35 kbps recommendation. Move the thundering-herd analysis and link budget details to an online supplement.

6. **Add a "Quick-Start" box** early in the paper: "For $k_c = 100$, $S = 256$ B, $T_c = 10$ s: use 35 kbps PHY, expect $\eta \approx 5$–$10\%$ routine, $\leq 46\%$ stress." This would dramatically improve accessibility.

7. **Cite TDMA slot-efficiency literature** to contextualize Eq. (11) and avoid appearing to claim novelty for a standard calculation.

8. **Provide a concrete NS-3 simulation plan** with specific configurations, metrics, and success criteria—not just "NS-3 is needed."