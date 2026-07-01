---
paper: "02-swarm-coordination-scaling"
version: "da"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-03-05"
recommendation: "Unknown"
---



# Peer Review: "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms"

## 1. Significance & Novelty
**Rating: 3 (Adequate)**

The paper addresses a genuine gap: closed-form parametric sizing equations for hierarchical coordination in large space swarms with byte-level traffic accounting. The two-test feasibility framework (byte budget + TDMA airtime) is a useful conceptual contribution, and the identification of the PHY rate transition (24 kbps infeasible → 30 kbps minimum → 35 kbps recommended) under CCSDS framing is practically relevant. However, the novelty is tempered by the fact that the individual components (TDMA scheduling, GE channel models, hierarchical clustering, AoI analysis) are well-established; the contribution is primarily their synthesis and parameterization for a specific (hypothetical) application domain. The paper is essentially a parametric design study rather than a methodological advance. The absence of any external validation makes it difficult to assess whether the synthesis produces insights beyond what an experienced systems engineer would derive from first principles.

## 2. Methodological Soundness
**Rating: 3 (Adequate)**

The analytical framework is internally consistent and the equations are correctly derived. The three-layer decomposition (byte budget, MAC efficiency, TDMA airtime) is logically structured. However, several methodological concerns arise:

- The DES is acknowledged to reproduce its own equations (Tier 1 verification), which limits its independent value. The distributional analysis (buffer sizing under campaign burstiness) is the sole non-tautological DES contribution, but it depends entirely on the assumed ON/OFF Markov campaign model.
- The slot-level simulator and packet-level simulator share the same equations as the analytical model, making cross-verification circular.
- The GE channel model is parameterized without any ISL measurement data; the per-cycle coherence assumption ($\tau_c \geq T_c$) is a strong structural choice that predetermines the ARQ ineffectiveness finding.
- The 1 kbps per-node budget is derived from a link budget (Table VII) that itself contains assumptions (6 dBi patch antennas, 500 km range, 290+50 K noise temperature) that are not validated.

## 3. Validity & Logic
**Rating: 3 (Adequate)**

The internal logic is generally sound, and the paper is commendably transparent about its limitations. The campaign duty factor $d$ adequately addresses workload realism: the mapping from mission phases to $d$ values (Table IX) is well-motivated, and the yearly mixture calculation ($\bar{\eta} = 5.6\%$, full-load $<0.1\%$ of time) properly contextualizes the stress-case $\eta_S \approx 46\%$ as a continuous-duty upper bound. The gamma unification around CCSDS-derived values (0.70–0.76 rate-dependent) is consistently applied throughout, with Model S clearly labeled as a comparison bound only.

However, several logical concerns remain:

- The claim that architecture-specific overhead ($\eta_0 \approx 5\%$) is "small" while command traffic "dominates" is somewhat misleading—command traffic dominance is a consequence of the assumed message model, not an architectural finding.
- The $\alpha_{\text{RX}}$ notation is confusing: it is described as both a "computed output" and appears in the design heuristic (Eq. 14) in a way that suggests it is a design parameter.
- The coordinator failure transient analysis (thundering herd, Slotted ALOHA with BEB) is detailed but disconnected from the main TDMA analysis—it operates on UHF, which is explicitly excluded from the sizing framework.

## 4. Clarity & Structure
**Rating: 3 (Adequate)**

The paper is dense but generally well-organized. The roadmap at the beginning of Section IV is helpful. The notation table (Table I) is comprehensive. However:

- The paper is excessively long for the depth of novel content. Much space is devoted to caveats, disclaimers, and restatements of limitations (which, while commendable for honesty, could be consolidated).
- The two slot-timing models (Model S and Model C) create confusion despite the clear labeling. Model S appears to exist only for historical reasons and could be eliminated entirely.
- The footnotes are extremely dense and contain substantive technical content that should be in the main text or appendices.
- Several tables (e.g., Tables V, VI, X, XI, XII) contain overlapping information that could be consolidated.
- The paper oscillates between being a design handbook and a research paper, which creates structural tension.

## 5. Ethical Compliance
**Rating: 4 (Good)**

The data availability statement is exemplary: source code, configuration, MC datasets, and all simulators are publicly available with a specific tag. The AI disclosure is transparent and appropriately scoped. The paper is forthright about the absence of external validation—indeed, almost to a fault. The V&V tier structure (IEEE 1012) is a good practice. The only concern is that the "Project Dyson Research Team" authorship without individual names is unusual for IEEE and should be resolved before publication.

## 6. Scope & Referencing
**Rating: 3 (Adequate)**

The literature coverage is broad, spanning constellation management, swarm robotics, distributed systems, queueing theory, and CCSDS standards. Key references (CCSDS Proximity-1, DVB-RCS2, Lutz et al. GE model, ITU-R P.681) are appropriate. However:

- The paper does not engage with recent work on LEO ISL channel characterization (e.g., measurements from Starlink or similar systems that may have become available).
- Network calculus (Le Boudec) is cited but not used; the mean-value approach is acknowledged as complementary but the deterministic worst-case bounds would strengthen the analysis.
- The comparison with DVB-RCS2 $\gamma$ values (0.70–0.85) is useful but superficial—a deeper analysis of why ISL conditions might differ would strengthen the plausibility argument.
- Some references are non-archival (Amazon Kuiper, DARPA programs, DOD Replicator) and may not meet IEEE archival standards.

## Major Issues

1. **Circular validation undermines confidence in results.**
   The paper acknowledges (commendably) that the DES, slot-sim, and packet-sim all share the same equations, making cross-verification tautological. However, this means the paper has *no* independent validation of any kind. The packet-level $\gamma$ derivation (Section IV-J) is presented as "Tier 2" evidence, but it is a parameter calculation from CCSDS specifications, not a validation exercise. The claim map (Table XIV) should more honestly reflect that all "Conf." entries are self-confirmations.
   - **Why it matters:** Without any independent check, the entire framework could contain systematic errors in its assumptions that propagate consistently through all tools.
   - **Remedy:** At minimum, perform an NS-3 simulation of the TDMA scheduling with realistic MAC behavior for a single cluster. Alternatively, benchmark against published DVB-RCS2 performance data for a comparable TDMA configuration. If neither is feasible pre-publication, downgrade all claims from "design recommendations" to "preliminary estimates" (which the paper partially does, but inconsistently).

2. **The GE channel model findings are predetermined by assumptions.**
   The per-cycle coherence assumption ($\tau_c \geq T_c$) directly causes the 27% intra-cycle ARQ recovery finding. The paper acknowledges this ("a direct consequence of the per-cycle GE coherence assumption, not an emergent finding") but then presents the ARQ ineffectiveness as a key result driving the 35 kbps recommendation. This is circular: the assumption determines the result, which determines the recommendation.
   - **Why it matters:** If $\tau_c < T_c$ (which is plausible for some ISL geometries), intra-cycle ARQ is effective and 30 kbps suffices. The 35 kbps recommendation is thus conditional on an unvalidated assumption.
   - **Remedy:** Present the 30 kbps and 35 kbps recommendations as conditional on $\tau_c/T_c$ (which the paper partially does) but remove the unconditional "35 kbps recommended" framing. Make the coherence regime the primary design variable, not a secondary consideration.

3. **The DES provides minimal value beyond confirming its own equations.**
   The paper states the DES's "sole non-tautological contribution is distributional tail analysis under campaign burstiness" (Section IV-F). This is honest but raises the question of whether the DES warrants the space devoted to it. The buffer sizing results (Fig. 4) depend entirely on the assumed ON/OFF Markov campaign model, which is itself unvalidated.
   - **Why it matters:** Journal space devoted to a tool that confirms its own inputs could be better used for sensitivity analysis or external benchmarking.
   - **Remedy:** Consolidate DES description to ~1 column. Use recovered space for: (a) a more thorough sensitivity analysis of the campaign model assumptions, or (b) a comparison with network calculus worst-case bounds, which would provide a genuinely independent analytical check.

4. **Fleet-level claims are insufficiently supported.**
   The spatial reuse analysis (Section IV-A.1) uses a back-of-envelope C/I calculation with a single-interferer model and an assumed antenna pattern. The paper acknowledges this but still uses $R = 3$ throughout for fleet-level scaling claims. Multi-interferer analysis, realistic antenna patterns, and orbital geometry effects could significantly change the reuse factor.
   - **Why it matters:** If $R = 7$ is required instead of $R = 3$, the number of required frequency channels doubles, potentially making the S-band allocation infeasible.
   - **Remedy:** Either remove fleet-level claims entirely (keeping the paper strictly per-cluster) or provide a more rigorous reuse analysis. At minimum, show sensitivity of fleet-level results to $R \in \{3, 5, 7\}$.

5. **The paper lacks a clear comparison with achievable alternatives.**
   The centralized and mesh baselines are intentionally extreme (centralized is compute-bound by construction; mesh is $O(N^2)$). No realistic alternative architectures (e.g., multi-hop relay, partial mesh, gossip-based hierarchical) are compared. This makes the "favorable" conclusion for hierarchy somewhat vacuous.
   - **Why it matters:** Without realistic alternatives, the paper cannot support claims about the relative merit of hierarchical coordination.
   - **Remedy:** Either include at least one realistic alternative (e.g., gossip-based partial dissemination with bounded staleness) or explicitly state that the paper does not claim architectural optimality—only feasibility characterization.

## Minor Issues

1. **Notation overload.** The paper defines $\eta$, $\eta_0$, $\eta_{\text{cmd}}$, $\eta_{\text{total}}$, $\eta_{\text{baseline}}$, $\eta_S$, $\eta_{\text{consensus}}$—too many variants of the same symbol. Consider a cleaner notation.

2. **Table I** lists $\alpha_{\text{RX}}$ with a "canonical: 0.908" value despite being described as a computed output. Remove the canonical value or clearly mark it as an example.

3. **Eq. (1)** counts messages but is never used quantitatively in the subsequent analysis. Either use it or remove it.

4. **The "thundering herd" footnote** (Section III-B.2) contains a detailed BEB analysis that is tangential to the main contribution. Move to an appendix or remove.

5. **Fig. 1** is referenced but the content is a placeholder ("fig-architecture-diagram.pdf"). Ensure the figure clearly shows the four-level hierarchy with quantitative annotations.

6. **Table III** footnote (d): the message size justification is useful but should be in the main text near the first use of these sizes.

7. **Section IV-B**: "AoI P99 = 441 s is < 0.5% of a 24 h TCA window" — this comparison is misleading. AoI measures staleness of routine telemetry, not conjunction assessment timeliness. The relevant comparison is whether 441 s staleness affects orbit determination accuracy.

8. **Algorithm 1, line 3**: $\eta_{\text{baseline}} = 20.5\%$ is added to $\eta_{\text{total}}$ but $\eta_0 = 5\%$ is also included. Verify this doesn't double-count the heartbeat component (which is listed under both baseline and $\eta_0$). The text says baseline is "excluded from $\eta$" but $\eta_0$ includes heartbeats—clarify.

9. **The abstract** is too long (>250 words) for IEEE TAES format. Condense.

10. **Reference [55]** (Project Dyson multi-model AI) is a self-citation to a non-peer-reviewed preprint. Consider removing or replacing with a more general AI-assisted design reference.

11. **Table VIII (Superframe)**: The sync beacon at 0.3 ms (8 bits at 30 kbps) seems too short for reliable synchronization. Clarify whether this is a timing marker within an already-synchronized frame or a standalone sync signal.

12. **Eq. (6)**: The consensus overhead formula assumes serialized votes over a shared channel but doesn't account for the TDMA scheduling constraint. How are Raft messages scheduled within the TDMA frame?

## Overall Recommendation
**Recommendation: Major Revision**

This paper presents a well-structured parametric sizing framework for hierarchical coordination in large space swarms, with commendable transparency about its limitations and validation gaps. The two-test feasibility framework (byte budget + TDMA airtime), the campaign duty factor parameterization, and the CCSDS-grounded gamma derivation are useful contributions to the preliminary design toolkit for future mega-constellation architects.

However, the paper suffers from a fundamental validation deficit: all internal tools share the same equations, making cross-verification circular. The GE channel model findings are predetermined by the coherence assumption, and the DES provides minimal value beyond confirming analytical means. The paper is also too long for its novel content, with excessive caveating and redundant tabulation consuming space that could be used for more substantive analysis (e.g., network calculus bounds, NS-3 benchmarking, or realistic alternative architectures).

For a major revision, the authors should: (1) obtain at least one form of genuinely independent validation (NS-3 MAC simulation or DVB-RCS2 benchmarking); (2) restructure the GE/ARQ analysis to make the coherence regime the primary design variable; (3) consolidate the DES description and use recovered space for stronger analytical content; and (4) reduce the paper length by ~25% through elimination of redundant tables and consolidation of caveats. The core framework is sound and potentially useful; it needs stronger evidence and tighter presentation to meet the standards of IEEE TAES.

## Constructive Suggestions

1. **Highest impact: Obtain independent validation.** Even a simplified NS-3 simulation of 100-node TDMA scheduling with CCSDS-like framing would transform the paper from "self-consistent analytical exercise" to "validated design tool." This is the single most important improvement.

2. **Restructure around coherence regime.** Make $\tau_c/T_c$ the primary design axis. Present two clean design points: fast-fading (30 kbps, ARQ effective) and slow-fading (35 kbps, inter-cycle recovery). This eliminates the circularity of the GE analysis and provides clearer practitioner guidance.

3. **Replace DES space with network calculus bounds.** Le Boudec is already cited; deriving deterministic worst-case bounds would provide a genuinely independent analytical check on the mean-value results and would be more useful to practitioners designing safety-critical systems.

4. **Consolidate tables.** Tables IV, V, VIII, IX, X, XI, XII contain overlapping information. A single comprehensive "design summary" table plus the rate ladder (Table VI) would suffice. Move detailed decompositions to an online supplement.

5. **Eliminate Model S entirely.** It serves no purpose in the current manuscript except as a historical artifact. All references to it (Table VII row, Fig. 5 curve, Table VII footnote) can be removed, simplifying the presentation considerably.

6. **Strengthen the fleet-level reuse analysis.** If fleet-level claims are retained, provide sensitivity to $R \in \{3, 5, 7\}$ and acknowledge the multi-interferer limitation more prominently. Alternatively, scope the paper explicitly as per-cluster only.

7. **Shorten the abstract** to ≤200 words, focusing on the two-test framework, the PHY rate recommendation, and the validation status.