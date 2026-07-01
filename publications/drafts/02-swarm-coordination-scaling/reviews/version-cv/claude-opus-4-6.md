---
paper: "02-swarm-coordination-scaling"
version: "cv"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-03-05"
recommendation: "Unknown"
---



# Peer Review: Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms

## 1. Significance & Novelty
**Rating: 3 (Adequate)**

The paper addresses a genuine gap: closed-form parametric sizing for hierarchical coordination at scales beyond current constellations. The two-layer feasibility framework (byte budget + TDMA airtime) and the campaign duty factor parameterization are useful conceptual contributions. However, the novelty is tempered by several factors: (a) the core equations are relatively straightforward traffic accounting and TDMA slot arithmetic—individually none is new; (b) the claimed scale ($10^3$–$10^5$) is explored only at the per-cluster level ($k_c = 50$–$500$), with fleet-level extension relegated to an order-of-magnitude reuse argument; (c) the absence of any external validation means the practical utility remains speculative. The paper is best characterized as a useful preliminary design methodology rather than a validated engineering contribution.

## 2. Methodological Soundness
**Rating: 3 (Adequate)**

The analytical framework is internally consistent and the decomposition into layers is logical. The DES is appropriately characterized as Tier-1 verification. However, several methodological concerns arise:

- The DES is cycle-aggregated and shares the same equations as the analytical model, so agreement is tautological for means. The authors acknowledge this clearly (a significant improvement over what one might expect), but this limits the DES to distributional analysis only.
- The GE channel model is applied with per-cycle coherence by construction, which predetermines the ARQ ineffectiveness finding. While the authors now transparently label this, the "27% intra-cycle recovery" is still presented as a result rather than a direct consequence of the modeling choice.
- The slot-level simulator and packet-level simulator share the same $\gamma$ expression (Eq. 7), so cross-tool "verification" is parameter propagation, not independent validation.
- The M/D/1 centralized baseline is intentionally compute-bound (ignoring propagation and spectrum), making the topology comparison asymmetric.

## 3. Validity & Logic
**Rating: 4 (Good)**

The internal logic is generally sound and the paper is notably self-aware about its limitations. Specific strengths:

- The campaign duty factor $d$ adequately addresses workload realism. The mapping from mission phases to $d$ values (Table VII) is well-motivated, and the empirical anchoring to ESA CA maneuver rates is appropriate. The time-weighted yearly mixture ($\eta \approx 5.9\%$) provides a credible operational estimate.
- The gamma unification is consistently applied: $\gamma(R_{\text{PHY}})$ from Eq. (7) is used throughout, with $\gamma_{24} = 0.761$ and $\gamma_{30} = 0.745$ properly replacing the earlier 0.85. Model S is clearly labeled as a comparison bound only.
- The stress-case ($\eta_S \approx 46\%$) is now properly contextualized as a continuous-duty upper bound that is episodic ($<1\%$ of operational time). This is a significant improvement.
- The three-layer feasibility framework is logically sound, and the paper correctly warns against double-counting the heuristic and Test B.

Concerns:
- The claim that $\eta$ is "scale-invariant" across $N = 10^3$ to $10^5$ is trivially true because $\eta$ is defined per-node within a cluster and depends only on $k_c$, not $N$. This is presented as a finding but is an artifact of the model structure.
- The $\alpha_{\text{RX}} = 0.908$ is described as "derived from schedule" but is actually a consequence of the ingress-dominated superframe design; it would change significantly under different egress requirements.

## 4. Clarity & Structure
**Rating: 3 (Adequate)**

The paper is thorough but suffers from excessive density and self-referential complexity. At ~15 pages of dense technical content with numerous cross-references, forward/backward pointers, and caveats embedded in footnotes, the readability is significantly impaired. Specific issues:

- The notation table (Table I) lists 22 symbols but several key quantities ($\eta_{\text{total}}$, $C_{\text{TDMA}}$, $C_{\text{raw}}$) are defined inline rather than in the table.
- The paper oscillates between Model S and Model C throughout, requiring the reader to constantly verify which model is being used. Despite the clear labeling, this creates cognitive overhead.
- Algorithm 1 is a valuable synthesis but arrives at page ~12; many readers will have lost the thread by then.
- Several tables contain dense footnotes that carry substantive technical content (e.g., Table III footnote d, Table V footnote a). This material should be in the main text.
- The "roadmap" paragraph at the start of Section IV is helpful but insufficient given the section's complexity.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**

The paper is exemplary in its transparency: AI tool usage is disclosed with specific model versions; data availability includes code, configuration, and datasets with a specific repository tag; the validation gap is prominently acknowledged in the abstract, throughout the text, and in a dedicated section; the claim map (Table IX) explicitly categorizes every result by evidence tier. The distinction between "what-if design tool" and "measured data" for the GE model is consistently maintained. This level of epistemic honesty is commendable and should be a model for the field.

## 6. Scope & Referencing
**Rating: 3 (Adequate)**

The literature coverage is broad but somewhat shallow in key areas:

- The TDMA/MAC scheduling literature is underrepresented. No reference to classical TDMA frame design texts (e.g., Rappaport, Proakis) or to specific satellite TDMA standards beyond DVB-RCS2.
- The AoI literature is cited but the application is limited to a single geometric formula; the rich literature on AoI optimization under scheduling constraints (e.g., Modiano's group, Sun/Uysal-Biyikoglu) is not leveraged.
- Network calculus is mentioned but not applied; the deterministic worst-case bounds it provides would be directly relevant to the feasibility framework.
- No comparison with existing constellation coordination overhead measurements (even approximate ones from Iridium or Starlink FCC filings).
- The paper cites 50+ references but many are contextual rather than technically engaged.

---

## Major Issues

1. **The DES verification provides limited value beyond confirming its own equations.**
   - *Issue:* The DES reproduces closed-form means to <0.1% by construction (shared equations). The claimed "primary incremental contribution" is distributional tail analysis (buffer sizing), but this is based on an assumed ON/OFF Markov campaign process that is itself unvalidated. The buffer sizing rule ($M = 1.30$ at $d = 0.10$) is conditional on this assumed process.
   - *Why it matters:* Readers may overestimate the validation status. The DES adds one genuinely useful finding (buffer sizing under correlated campaigns) but this is a narrow contribution relative to the space devoted to DES description.
   - *Remedy:* Reduce DES description to ~1 column. State explicitly that the DES's sole non-tautological contribution is the buffer sizing rule under campaign burstiness, and that this rule is conditional on the assumed campaign process. Consider whether the buffer sizing could be derived analytically (MMPP/D/1 bounds exist in the literature).

2. **The packet-level validation (Section IV-J) does not provide independent validation.**
   - *Issue:* Section IV-J derives $\gamma$ from CCSDS Proximity-1 framing specifications using Eq. (7). This is a parameter estimation exercise, not validation. The same equation is used in the slot-level simulator and Algorithm 1. The DVB-RCS2 comparison ($\gamma = 0.70$–$0.85$) is the closest thing to external anchoring, but DVB-RCS2 is a ground terminal standard, not an ISL standard.
   - *Why it matters:* The paper's central design recommendation (35 kbps) depends critically on $\gamma \approx 0.73$–$0.76$. If real ISL implementations achieve $\gamma = 0.60$ (plausible with acquisition failures, Doppler, and antenna pattern effects), the minimum PHY rate shifts to ~45 kbps.
   - *Remedy:* Rename Section IV-J to "Standards-Based Parameter Estimation" (which it already partially does) and remove any language suggesting validation. Add a sensitivity analysis showing how the design recommendation shifts for $\gamma \in [0.50, 0.85]$ in a single clear figure. The $\gamma$-conditional lookup table is a good start but should be expanded.

3. **Fleet-level scaling claims are insufficiently supported.**
   - *Issue:* The paper's title and abstract imply applicability to "large autonomous space swarms" but all validated results are per-cluster ($k_c = 50$–$500$). Fleet-level extension relies on Eq. (6) with $R = 3$ spatial reuse, which is an order-of-magnitude estimate based on free-space path loss. The paper acknowledges this but continues to make fleet-level statements (e.g., "$10^5$ nodes").
   - *Why it matters:* Inter-cluster interference, near-far effects, and dynamic orbital geometry could invalidate the $R = 3$ assumption. If $R = 7$ is required, the spectrum/channel requirements double.
   - *Remedy:* Modify the title to explicitly indicate per-cluster scope (e.g., "...Per-Cluster Sizing Equations..."). Restrict fleet-level claims to a single clearly-labeled subsection. Add a quantitative sensitivity analysis for $R \in \{3, 5, 7\}$.

4. **The 1 kbps per-node budget lacks sufficient justification as a design constraint.**
   - *Issue:* The entire feasibility analysis hinges on $C_{\text{node}} = 1$ kbps. The physical justification (Section III-E) derives this from a 200 kbps aggregate S-band capacity shared among 100 nodes, but this aggregate capacity itself depends on link budget assumptions (2.2 GHz, 1 W, 6 dBi, 500 km) that are stated without uncertainty analysis. The 50% margin claim (1.5 kbps usable → 1 kbps budget) conflates margin for retransmissions with margin for the protocol overhead that the paper is trying to size.
   - *Why it matters:* At 2 kbps, stress-case $\eta$ halves to ~23% and most of the paper's TDMA analysis becomes non-binding. At 0.5 kbps, the architecture is infeasible. The choice of 1 kbps is therefore the single most consequential assumption.
   - *Remedy:* Provide a proper link budget table with margin analysis. Show feasibility results parametrically for $C_{\text{node}} \in \{0.5, 1, 2, 5, 10\}$ kbps in a single summary figure. Acknowledge that the 1 kbps choice is a design assumption, not a physical constraint.

5. **The generalized gamma expression (Eq. 7) utility for practitioners is limited without uncertainty quantification.**
   - *Issue:* Eq. (7) is presented as a tool for practitioners to compute $\gamma$ for their specific link. However, the inputs ($T_{\text{acq}}$, $T_{\text{guard}}$) are the most uncertain parameters and no guidance is provided on their distributions. The worked example at 35 kbps uses point estimates throughout.
   - *Why it matters:* A practitioner using Eq. (7) with optimistic $T_{\text{acq}}$ could undersize their PHY rate. The equation is useful only if accompanied by input uncertainty guidance.
   - *Remedy:* Add a Monte Carlo sensitivity analysis over $(T_{\text{acq}}, T_{\text{guard}})$ distributions (e.g., uniform or triangular) showing the resulting $\gamma$ distribution and its impact on $R_{\text{PHY,min}}$. Fig. 4 partially addresses this but uses only two point estimates.

---

## Minor Issues

1. **Eq. (1):** The hierarchical message count $M_{\text{total}}$ should clarify whether this is per-cycle or per-second, and whether it includes bidirectional traffic.

2. **Table II, Panel B:** The "Rec. PHY" column jumps from 35 kbps to 70 kbps to 140 kbps for $S = 256$→512→1024 B, but these are not simply $2\times$ scalings. Clarify the rounding/margin convention.

3. **Section III-B-2, coordinator failure transient:** The thundering herd analysis in the footnote is substantive and should be in the main text or a dedicated subsection.

4. **Eq. (5), $\eta_{\text{consensus}}$:** The assumption that Raft votes are serialized over the shared channel is restrictive. In practice, Raft uses parallel RPCs. Clarify the impact of this assumption.

5. **Table VI:** The "1-Cyc?" column uses checkmarks but the meaning for the $d = 1.00$ row with footnote b is ambiguous—broadcast is single-cycle but unicast is not.

6. **Fig. 2:** The CDF figure description mentions "Bernoulli $d = 0.10$" and "ON/OFF $d = 0.10$" but the visual distinction between solid and dash-dot may be difficult in grayscale printing.

7. **Section IV-A, "Phase-staggered scheduling":** The claim "DES confirms zero drops at ≥25 kbps" is stated without supporting data. Provide the DES results or a reference to a figure.

8. **Table VIII (Rate Feasibility):** The margin calculation "Margin = $T_c$ − Ingress − 192 ms" should explicitly state that 192 ms is the total egress allocation from Table V.

9. **Abstract:** "CCSDS Proximity-1 framing anchors $\gamma \approx 0.70$–$0.76$ (rate-dependent)" — the range 0.70–0.76 is not clearly derivable from the text, which gives $\gamma_{50} = 0.695$ and $\gamma_{24} = 0.761$. Clarify the range endpoints.

10. **Section V-C, sizing walkthrough:** The heuristic cross-check uses $\alpha_{\text{RX}} = 0.792$ but earlier text states $\alpha_{\text{RX}} = 0.908$. The difference is because 35 kbps changes the ingress duration; this should be explicitly noted.

11. **References:** Several references are non-archival (Amazon Kuiper overview, DARPA program pages, DOD fact sheets). While acceptable for context, the paper should not make technical claims based on these sources.

12. **Typo/style:** "Eq.~\ref{eq:eta_canonical}" is referenced before it appears in the text flow (in the Contributions subsection). Consider reordering.

---

## Overall Recommendation
**Recommendation: Major Revision**

This manuscript presents a well-structured preliminary design methodology for hierarchical coordination sizing in large space swarms. Its principal strengths are: (1) the clean two-layer feasibility decomposition (byte budget + TDMA airtime); (2) the campaign duty factor parameterization, which credibly addresses workload realism; (3) exceptional transparency about validation limitations, with the claim map (Table IX) and explicit V&V tier labeling setting a high standard for epistemic honesty; and (4) the generalized $\gamma$ expression (Eq. 7) with CCSDS grounding, which provides a useful starting point for practitioners.

However, the paper has significant weaknesses that prevent acceptance in its current form. The most critical is the absence of any external validation—the DES, slot-sim, and packet-level analysis all share the same underlying equations, making cross-tool agreement tautological for all but distributional tails. The fleet-level scaling claims are not supported by the per-cluster analysis. The 1 kbps per-node budget, which drives the entire feasibility analysis, lacks rigorous justification. The paper is also excessively dense, with important technical content buried in footnotes and the reader required to track two slot-timing models, three overhead tiers, and numerous cross-references.

The path to acceptance requires: (a) honest scoping of claims to per-cluster sizing (modifying the title accordingly); (b) at minimum one form of external validation (NS-3 MAC simulation or hardware $\gamma$ measurement); (c) parametric treatment of $C_{\text{node}}$ rather than a single point design; and (d) significant condensation of the presentation, particularly the DES description and the Model S/Model C comparisons.

---

## Constructive Suggestions
*(Ordered by impact)*

1. **Add NS-3 MAC simulation** for a single cluster ($k_c = 100$) to validate $\gamma$ and contention effects. This would elevate the strongest claims from Tier 1 to Tier 2 and address the most critical reviewer concern. Even a simplified NS-3 model with TDMA scheduling would provide genuine independent validation.

2. **Create a single "practitioner summary" figure** showing feasibility regions in $(C_{\text{node}}, k_c)$ space for fixed $T_c = 10$ s and $d \in \{0.01, 0.10, 1.0\}$, with $\gamma$ as a parameter. This would be the paper's most impactful contribution and would replace several tables.

3. **Restructure the paper** to lead with Algorithm 1 and the design equations (current Section V-C), then present the supporting analysis. The current structure buries the actionable content after 10+ pages of derivation.

4. **Provide a proper S-band ISL link budget table** with explicit margin analysis, replacing the single-line link budget statement. Include rain/atmospheric loss (negligible for ISL but should be stated), pointing loss, and implementation loss.

5. **Reduce the DES description** to focus exclusively on the buffer sizing contribution. Move the V&V tier discussion to a methods appendix.

6. **Add a $\gamma$ uncertainty propagation analysis** showing how $R_{\text{PHY,min}}$ varies with $\gamma \in [0.50, 0.85]$ for the recommended parameter set. This directly addresses the paper's most consequential uncertainty.

7. **Consolidate Model S and Model C** presentation. Model S could be introduced once as a pedagogical upper bound and then dropped entirely from subsequent analysis. The current interleaving creates unnecessary complexity.