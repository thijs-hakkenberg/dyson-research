---
paper: "02-swarm-coordination-scaling"
version: "cn"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-03-03"
recommendation: "Unknown"
---

# Peer Review: "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms"

## 1. Significance & Novelty
**Rating: 3 (Adequate)**

The paper addresses a genuine gap: no prior work provides closed-form parametric sizing for hierarchical coordination at the $10^3$–$10^5$ node scale with byte-level traffic accounting. The two-layer feasibility framework (byte budget + TDMA airtime) is a useful conceptual contribution, and the identification of the PHY-rate transition (24 kbps infeasible → 30 kbps minimum → 35 kbps recommended) is a concrete, actionable finding. However, the novelty is tempered by several factors: (1) the individual analytical components (M/D/1 queueing, GE channel models, AoI analysis, TDMA slot budgeting) are all well-established; the contribution is their assembly, not methodological innovation; (2) the absence of any external validation means the framework's predictive utility remains undemonstrated; (3) the practical applicability is narrow—the results are most interesting in the 24–35 kbps regime for a specific cluster size, and the paper itself acknowledges that at ≥10 kbps per node, all constraints become trivially non-binding. The paper is better characterized as a "design handbook entry" than a research advance, which is valuable but sits at the lower end of novelty for IEEE T-AES.

## 2. Methodological Soundness
**Rating: 3 (Adequate)**

The analytical framework is internally consistent and carefully constructed. The three-layer decomposition (byte budget, MAC efficiency, TDMA airtime) is logically sound, and the authors are commendably transparent about what each simulation tier can and cannot demonstrate. Specific methodological observations:

- The **campaign duty factor** ($d$) is a welcome addition that substantially improves workload realism. The mapping to concrete mission phases (Table 8) with reverse-derived examples is well done. However, the Bernoulli per-cycle model for command generation is simplistic; the ON/OFF Markov alternative is mentioned but not fully developed analytically.
- The **gamma unification** around 0.76 (CCSDS-grounded, replacing an earlier 0.85) appears consistently applied throughout. The time-domain derivation (Eq. 17) is clean and the decomposition table (Table 11) is useful. The rate-dependent variation ($\gamma_{24} = 0.761$, $\gamma_{30} = 0.745$) is properly tracked.
- The **DES verification** is honestly characterized as Tier-1 code verification. The <0.1% agreement with closed-form means is expected by construction and provides no independent validation. The distributional tail analysis (buffer sizing under correlated campaigns) is the DES's genuine incremental contribution, though the practical guidance (buffer ≥ 1.15× mean) is modest.
- The **slot-level simulator** provides the paper's most interesting finding: the ARQ×TDMA coupling (52.7% deadline misses at 24 kbps with $M_r = 1$). This is a genuinely emergent result invisible to the fluid-server DES.
- The **packet-level validation** (Section IV-J) anchors $\gamma$ in CCSDS standards but does not independently validate the sizing equations. The authors are transparent about this, but it means the paper has no independent validation of its core framework.

The 30 Monte Carlo replications are adequate for mean estimation but marginal for tail characterization (P99 from 30 samples has wide confidence intervals). The 1-year simulation duration is reasonable.

## 3. Validity & Logic
**Rating: 4 (Good)**

The internal logic is generally rigorous, with careful attention to avoiding double-counting between layers (the explicit warning about not multiplying $\eta$ by $1/\gamma$ and also performing the superframe check is appreciated). The parameter dependency map (which parameters affect ingress vs. egress) is clearly stated. Specific observations:

- The **stress-case contextualization** ($\eta_S \approx 46\%$) is now properly framed as a continuous-duty upper bound with the duty factor providing realistic operating points. The worked examples (orbit-raising, station-keeping, collision avoidance) effectively demonstrate that routine operations occupy $\eta \approx 5$–10%.
- The **three-layer feasibility framework** is logically sound. The screening heuristic ($\eta_{\text{total}}/\gamma < 0.50$) is appropriately flagged as non-binding.
- The **GE channel model** is honestly presented as a design assumption with sensitivity curves rather than a calibrated model. The physical mapping (Table 5) is reasonable but speculative.
- One logical concern: the paper claims "topology-invariant" command overhead, but this holds only under centralized broadcast semantics—a significant caveat that is mentioned but could be more prominent given how central this claim is.

## 4. Clarity & Structure
**Rating: 2 (Below Average)**

This is the paper's most significant weakness. Despite evident effort to be thorough, the manuscript is extremely dense, repetitive, and difficult to navigate. At an estimated 12,000+ words of body text plus extensive tables and figures, it substantially exceeds typical IEEE T-AES length guidelines. Specific concerns:

- **Redundancy**: Key results (e.g., $\gamma \approx 0.76$, 35 kbps recommendation, $\eta_S \approx 46\%$, stress-case contextualization) are restated 5–8 times across the abstract, introduction, results, discussion, and conclusion. The paper reads as if each section was written to be self-contained, producing substantial overlap.
- **Defensive over-qualification**: Nearly every quantitative claim is followed by multiple caveats, footnotes, and cross-references. While intellectual honesty is commendable, the effect is that the reader cannot distinguish primary results from secondary qualifications. Example: the superframe table (Table 7) has a footnote that references another table, a section, and an equation, then the margin analysis table (Table 8) re-derives the same margin with additional caveats.
- **Notation overload**: Table 1 lists 18 symbols, but additional notation is introduced throughout without consolidation. The distinction between $\eta$, $\eta_0$, $\eta_{\text{cmd}}$, $\eta_{\text{total}}$, $\eta_S$, $\eta_E$, and $\eta_{\text{consensus}}$ requires constant back-referencing.
- **Model S vs. Model C**: The two-model framework is a source of persistent confusion despite the upfront declaration. Model S appears in tables and figures with disclaimers that it is "not used for recommendations," raising the question of why it is presented at all beyond a single comparison row.
- **Section IV structure**: The results section attempts to serve as both a technical derivation and a design handbook, resulting in an awkward hybrid. The "roadmap" paragraph helps but cannot fully compensate.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**

Exemplary transparency throughout. The AI disclosure is specific and appropriate. Data availability is excellent (GitHub repository with tagged release, specific software versions, runtime estimates). The validation gap is stated repeatedly and prominently. The claim map (Table 10) is an unusually honest and useful addition. The distinction between design assumptions and measured parameters is consistently maintained.

## 6. Scope & Referencing
**Rating: 3 (Adequate)**

The reference list (55 items) covers the major relevant areas: CCSDS standards, constellation operations, swarm robotics, distributed systems theory, AoI, and queueing theory. However:

- **Missing references**: No citation of actual ISL measurement campaigns (e.g., EDRS, OISL demonstrations on Starlink). The Lutz et al. GE framework is cited but more recent LEO ISL channel characterization work is absent. Network calculus (Le Boudec) is cited but not applied—either apply it or remove the citation.
- **Scope fit**: The paper sits at an unusual intersection of systems engineering handbook and research contribution. For IEEE T-AES, the lack of experimental validation or comparison with operational systems is a concern. The paper might be better suited to a systems engineering journal (e.g., JSSE, Systems Engineering) or as a NASA/ESA technical report.
- **DVB-RCS2** is cited for partial external anchoring of $\gamma$ (0.70–0.85), which is a useful comparison point, but the framing differences are not discussed in sufficient detail to assess how meaningful this anchoring is.

---

## Major Issues

1. **No external validation undermines the paper's central claims.**
   - The paper acknowledges this repeatedly, but the absence of any comparison with operational ISL data, NS-3 simulation, or hardware measurements means the framework's predictive accuracy is entirely unknown. The "validation roadmap" (Section V-B) is helpful but does not substitute for actual validation.
   - *Why it matters*: The paper's primary value proposition is as a design tool. Without validation, practitioners cannot assess whether the recommended 35 kbps design point is conservative by 10% or 100%.
   - *Remedy*: At minimum, compare $\gamma$ predictions against published DVB-RCS2 slot efficiency measurements (not just the range). Ideally, conduct an NS-3 simulation of even a single 10-node cluster to provide one external data point. If neither is feasible, the paper should be reframed more explicitly as a "preliminary design methodology" rather than presenting specific numeric recommendations.

2. **The DES provides negligible independent validation.**
   - The DES implements the same equations as the analytical model and achieves <0.1% agreement—this is code verification, not model validation. The distributional tail analysis (buffer sizing) is the only genuinely new information from the DES, and it yields a single practical guideline (buffer ≥ 1.15× mean).
   - *Why it matters*: The paper devotes substantial space to DES methodology and results that confirm what the equations already predict. This inflates the paper's length without proportionate insight.
   - *Remedy*: Reduce DES coverage to ~1 page: state that it confirms analytical means (code verification), present the buffer CDF figure and the 1.15× guideline, and move on. Use the recovered space for validation or for streamlining the presentation.

3. **Manuscript length and redundancy severely impair readability.**
   - The paper is approximately 2× the typical length for an IEEE T-AES article. Key results are repeated 5–8 times. The defensive qualification style, while honest, makes it difficult to extract the primary contributions.
   - *Why it matters*: Reviewers and practitioners will struggle to identify the actionable content. The paper's genuine contributions (two-layer framework, PHY-rate transition identification, ARQ×TDMA coupling) are buried in repetition.
   - *Remedy*: Target a 30–40% reduction. Specific cuts: (a) consolidate all Model S material into a single comparison paragraph; (b) eliminate redundant restatements of $\gamma = 0.76$ and the 35 kbps recommendation; (c) merge Tables 6, 7, 8, and 9 into a single comprehensive feasibility table; (d) move the thundering-herd analysis, GNSS denial sensitivity, and fleet reuse to an appendix or supplementary material; (e) reduce the workload profiles section by combining Tables 4 and 8.

4. **The generalized $\gamma$ expression (Eq. 18) conflates pedagogical value with practical utility.**
   - The multiplicative decomposition (Eq. 14) is explicitly labeled "pedagogical only," yet the bit-domain form (Eq. 18) requires a unit-conversion factor ($10^{-3}$) that invites errors. The time-domain form (Eq. 17) is cleaner and preferred by the authors' own admission.
   - *Why it matters*: Practitioners need one clear equation. Presenting two forms with caveats about which is "preferred" and which is "for spreadsheet use" adds confusion.
   - *Remedy*: Present Eq. 17 (time-domain) as the primary equation. Relegate Eq. 18 to a footnote or appendix. Remove Eq. 14 entirely or present it only once in the decomposition table.

5. **The packet-level validation (Section IV-J) does not provide adequate independent validation.**
   - The section title ("Physical-Layer Parameter Anchoring") accurately describes what it does: it derives $\gamma$ from CCSDS framing parameters. But it does not validate the sizing equations that consume $\gamma$. The cross-model consistency check confirms agreement by construction.
   - *Why it matters*: The section's placement and length suggest it provides more validation than it actually does.
   - *Remedy*: Shorten to ~0.5 pages. State clearly: "We derive $\gamma$ from CCSDS Proximity-1 framing; this anchors the parameter value but does not validate the sizing framework." Present Table 11 and Fig. 7, then move on.

## Minor Issues

1. **Table 1 (notation)**: $\gamma_{24} = 0.761$ and $\gamma_{30} = 0.745$ are listed in the notation table, which is unusual—these are computed results, not notation. Move to the results section.

2. **Eq. 1 ($M_{\text{total}}$)**: The equation counts messages but the paper's primary metric is bytes. A byte-domain version would be more directly useful.

3. **Section III-B-2 (coordinator failure transient)**: The compound probability $6.3 \times 10^{-12}$ s$^{-1}$ assumes independence, which the text acknowledges may not hold. The units (s$^{-1}$) should be clarified—is this a rate or a probability?

4. **Fig. 2 (phase stagger)**: The figure is referenced but the description suggests two panels (a, b). Ensure both panels are clearly labeled and that the caption matches.

5. **Table 3 (simulation parameters)**: The collision avoidance rate ($10^{-4}$/node/s) is described as "screening notifications" in the footnote, but the main text treats them as "priority alerts." Clarify the operational semantics.

6. **Section IV-A**: "Phase-staggered scheduling ($\phi_j = (j / n_{\text{clusters}}) \times T_c$)" — this is introduced without sufficient context. What is $n_{\text{clusters}}$? How does it relate to $k_r$?

7. **Eq. 10 ($\eta_{\text{consensus}}$)**: The assumption that Raft votes are "serialized over the shared channel" is strong and should be justified. In practice, Raft uses parallel RPCs.

8. **Table 6 (joint interaction)**: The "GE+Exc" column header is cryptic. Spell out "GE losses with exception-only telemetry" or similar.

9. **Section IV-E**: "The 60× gap between reverse-derived $d = 0.0016$ and default $d = 0.10$ is intentional design conservatism" — this is a very large margin. Justify why 60× is appropriate rather than, say, 10×.

10. **References**: [3] (Kuiper) and [17] (DARPA OFFSET) are non-archival web pages. Per IEEE policy, these should be cited as such with access dates (which they are) but should be minimized in favor of archival sources where possible.

11. **Abstract**: At 150+ words, the abstract is dense but could be tightened. The sentence about $p_{BG} = 0.50$ being a design assumption belongs in the body, not the abstract.

12. **The "safety-criticality" paragraph in Section I-C** makes a strong claim ("complete situational awareness loss") that is not fully supported by the analysis, which models only the coordination channel, not the full situational awareness pipeline.

---

## Overall Recommendation
**Recommendation: Major Revision**

This paper presents a carefully constructed parametric sizing framework for hierarchical coordination in large autonomous space swarms. Its primary strengths are: (1) the two-layer feasibility decomposition (byte budget + TDMA airtime) is conceptually clean and practically useful; (2) the identification of the PHY-rate feasibility transition (24→30→35 kbps) under CCSDS-grounded slot efficiency is a concrete, actionable finding; (3) the campaign duty factor elegantly resolves the stress-case realism concern; (4) the ARQ×TDMA coupling discovery from slot-level simulation is a genuinely emergent result; and (5) the intellectual honesty throughout—particularly the claim map, validation gap acknowledgment, and careful distinction between design assumptions and validated results—is exemplary.

However, three critical issues prevent acceptance in the current form. First, the complete absence of external validation means the framework's predictive accuracy is unknown; the paper's numeric recommendations (35 kbps, 730 ms margin, etc.) cannot be assessed for conservatism or optimism. Second, the manuscript is approximately twice the appropriate length, with extensive redundancy that obscures the genuine contributions. Third, the DES and packet-level "validation" provide less independent confirmation than their presentation suggests—the paper would be stronger if it honestly characterized these as code verification and parameter anchoring (which it does in places) without devoting disproportionate space to them.

The framework has genuine value as a preliminary design tool, and the paper could make a solid contribution to IEEE T-AES if substantially shortened, if the validation claims are right-sized to match the evidence, and if at least one external comparison point (DVB-RCS2 slot efficiency measurement, NS-3 cluster simulation, or published ISL telemetry) is incorporated.

## Constructive Suggestions

1. **Reduce manuscript length by 30–40%** by eliminating redundant restatements, consolidating tables, and moving secondary analyses (thundering herd, GNSS denial, fleet reuse) to supplementary material. This single change would most improve the paper's impact.

2. **Add one external validation point.** Even a qualitative comparison with DVB-RCS2 measured slot efficiencies, or an NS-3 simulation of a 10-node TDMA cluster, would substantially strengthen the paper's credibility.

3. **Restructure Section IV** into two clear subsections: "Analytical Results" (equations, sensitivity, design curves) and "Simulation Verification" (DES code verification, slot-sim ARQ coupling, packet-sim $\gamma$ anchoring). This would clarify what each tool contributes.

4. **Present a single $\gamma$ equation** (Eq. 17, time-domain) as the primary practitioner tool. Remove or relegate the bit-domain form and the multiplicative decomposition.

5. **Strengthen the GE channel discussion** by citing recent LEO ISL measurement campaigns (if any exist) or by explicitly stating the state of the art in ISL channel characterization to justify why parametric sensitivity is the appropriate approach.

6. **Consider splitting the paper**: the TDMA/PHY-layer analysis (Sections IV-A, IV-D, IV-J) and the message-layer analysis (Sections IV-B, IV-C, IV-E, IV-F) are somewhat independent contributions that might each be stronger as focused shorter papers.