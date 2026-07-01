---
paper: "02-swarm-coordination-scaling"
version: "ao"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-27"
recommendation: "Major Revision"
---

# Peer Review: "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms"

## 1. Significance & Novelty
**Rating: 3 (Adequate)**

The paper addresses a genuine gap at the intersection of mega-constellation operations and swarm coordination: the absence of closed-form sizing equations for hierarchical coordination architectures at the $10^3$–$10^5$ node scale. The authors correctly identify that swarm robotics literature rarely exceeds hundreds of agents, while constellation management literature focuses on ground-directed operations. The practitioner-oriented design equations (Section V-C) are a useful contribution, and the open-source simulation tool adds reproducibility value.

However, the novelty is more limited than the framing suggests. The $O(1)$ overhead scaling of a fixed-depth hierarchy with fixed fan-out is a straightforward mathematical consequence of the architecture definition—the authors acknowledge this (Section IV-F), but the paper's length and apparatus seem disproportionate to the insight. The core analytical results (geometric AoI distribution, GE bad-state retransmission probability, M/D/1 queueing) are textbook derivations applied to a specific parameterization. The simulation's primary role—confirming that single-factor equations compose under point-to-point links—is valuable but narrow. The "joint independence" finding (Section IV-D) is essentially a verification that independent link losses on dedicated links don't interact with coordinator ingress, which is architecturally obvious once the point-to-point assumption is stated.

The paper would benefit from a more honest framing: this is a *parametric sizing study* with useful engineering tables, not a discovery of new scaling laws. The title appropriately reflects this, but the abstract and introduction occasionally overstate the contribution (e.g., "validates them with an open-source cycle-aggregated simulation" implies more than confirming closed-form arithmetic).

## 2. Methodological Soundness
**Rating: 3 (Adequate)**

The simulation framework is clearly described and the cycle-aggregated approach is appropriate for the message-layer abstraction. The Monte Carlo framework (30 replications, seeds 42–71) is adequate, and the authors are commendably transparent that the near-deterministic message model renders MC variance negligible (SD < 0.001%). The analytical cross-checks (AoI geometric distribution, M/D/1 validation at low utilization) are well-executed.

Several methodological concerns warrant attention:

**(a) Simulation vs. analytical redundancy.** The paper repeatedly demonstrates that the DES reproduces closed-form predictions to within 0.1% (Table 7). While this validates implementation correctness, it raises the question of what the simulation adds beyond the analytics. The authors argue it verifies "compositionality under joint conditions" (Section IV-D), but the joint interaction test (Table 5) shows zero additional drops under GE because lost messages never reach the coordinator—a result that follows directly from the architecture description without simulation. The simulation's value proposition needs sharper articulation.

**(b) Sectorized mesh parameterization.** The $\sqrt{N}$ sector sizing is acknowledged as heuristic, and the oracle-based neighbor discovery (zero-bandwidth cost) explicitly favors the mesh. The capped-fanout variant (10 neighbors) produces $O(N)$ scaling identical to the hierarchical architecture, making the comparison one of constant factors rather than asymptotic behavior. The 1.4–1.5× overhead ratio is parameter-dependent and could shift substantially with different heartbeat sizes (32 vs. 64 bytes) or neighbor caps. The paper should more clearly state that the sectorized mesh comparison is illustrative, not definitive.

**(c) Inter-cycle recovery.** The store-and-forward recovery analysis (Section IV-C) is explicitly flagged as "analytical projection, not simulated." This is appropriate disclosure, but the geometric recovery model assumes independence across cycles, which contradicts the GE model's temporal correlation. During a sustained bad state (mean duration $1/p_{BG} = 5$ cycles = 50 s), consecutive retry attempts face $p_B = 0.90$ loss, and the geometric model's assumption of independent per-cycle success probability $p_s$ is violated. The 4–7 cycle recovery projection is therefore optimistic for the GE case.

**(d) Collision avoidance rate.** The $10^{-4}$/node/s rate is described as "proximity monitoring events" rather than maneuver-triggering conjunctions, but the sensitivity analysis ($\pm 1.5$ pp on $\eta$) suggests this parameter has minimal impact. The 1000:1 screening-to-maneuver ratio is reasonable but should cite a primary source beyond the ESA annual report.

## 3. Validity & Logic
**Rating: 3 (Adequate)**

The paper's conclusions are generally supported by the analysis, with several important caveats that the authors partially but incompletely address.

**Strengths in validity:** The dual-regime interpretation (Section IV-F-3) is well-handled—the authors clearly state that the 1 kbps budget is a worst-case RF-backup constraint and that overhead is negligible under optical ISLs. The honest treatment of the centralized baseline (Table 1, Section IV-G) acknowledges that centralized processing scales to $10^6$ with parallelization, and correctly identifies spectrum and ground availability as the binding constraints. The workload decomposition (Section IV-E, Fig. 5) usefully demonstrates that the 46% headline overhead is dominated by the stress-case command assumption, not the hierarchical architecture itself.

**Concerns:** The paper's central claim—that hierarchical coordination is advantageous over centralized at scale—rests on three pillars: fault tolerance during ground outages, spectrum independence, and $O(1)$ overhead scaling. The first two are qualitative arguments not validated by the simulation (ground outage impact is computed analytically as "~9 screening events unhandled per 15-min outage"). The third is a mathematical tautology for fixed-depth hierarchies. The paper would be strengthened by explicitly acknowledging that the simulation does not demonstrate a *performance advantage* of hierarchical over centralized; rather, it characterizes the *cost* of hierarchical coordination to enable an engineering trade study.

The AoI-to-position-error coupling (Eq. 11) is appropriately caveated as "illustrative back-of-the-envelope," but the 230 m figure is prominent enough that readers may take it as a validated result. The linear uncertainty growth model ($\dot{\sigma} = 0.5$ m/s) is reasonable for short-term along-track propagation but breaks down over the 440 s P99 AoI window due to atmospheric density variability and unmodeled perturbations.

The latency values in Table 8 (340–675 ms) appear inconsistent with the latency breakdown in Table 9 (~260 ms mean, ~500 ms P95). The footnote to Table 8 mentions "cycle-alignment overhead ($T_c/2 \approx 5$ s average wait)" which would dominate, but this is not reflected in the 340–675 ms range. This discrepancy needs clarification.

## 4. Clarity & Structure
**Rating: 2 (Needs Improvement)**

The paper is excessively long for its core contribution. At approximately 15,000 words of body text (excluding references), it substantially exceeds typical IEEE TAES limits. The repetitive qualification and cross-referencing—while individually defensible—collectively obscure the main results. Several specific issues:

**(a) Redundancy.** The same results are stated in the abstract, introduction (contributions list), results section, discussion, design equations summary, and conclusion. The coordinator capacity result (21–50 kbps) appears in at least six locations. The paper would benefit from a single authoritative presentation with forward/backward references.

**(b) Defensive over-qualification.** Nearly every quantitative claim is followed by multiple caveats, cross-references, and footnotes. While intellectual honesty is valued, the density of qualifications makes it difficult to extract the primary message. For example, the AoI section (IV-B) contains the result (P99 = 441 s), an analytical cross-check, a position-error coupling, a caveat about the coupling model, a caveat about the caveat, and a statement that "no operational conclusion should be drawn." This level of hedging, while appropriate in isolation, becomes exhausting across 20+ pages.

**(c) Table proliferation.** The paper contains 15 tables, many of which could be consolidated. Tables 2 (mesh traffic), 4 (sector traffic), and 3 (state completeness) could be merged. Tables 7 (overhead scaling) and 10 (exception validation) report essentially the same quantity ($\eta$) under different conditions and could be combined.

**(d) Figure quality.** All figures reference PDF files that are not available for review. The captions are descriptive, but without the actual figures, it is impossible to assess their effectiveness. The authors should ensure figures are embedded or provided as supplementary material for review.

**(e) Notation.** The paper introduces numerous symbols ($\eta$, $\eta_{\text{eff}}$, $\eta_{\text{total}}$, $\eta_{\text{delivered}}$, $\eta_S$, $\eta_N$, $\eta_E$, $\eta_{\text{sector}}$, $B_{\text{status}}$, $O_{\text{protocol}}$, $C_{\text{node}}$, $C_{\text{coord}}$, $C_{\text{TDMA}}$, $C_{\text{raw}}$, etc.) without a consolidated notation table. A nomenclature section would significantly improve readability.

## 5. Ethical Compliance
**Rating: 4 (Good)**

The paper provides appropriate disclosure of AI-assisted methodology in the Acknowledgment section, referencing Claude 4.6, Gemini 3 Pro, and GPT-5.2 for "exploratory AI-assisted ideation." The disclosure is specific about what was AI-assisted (architectural concept generation) and what was not (the current study's validation). The companion methodology paper [dyson_multimodel] is referenced for details.

The anonymous authorship ("Project Dyson Research Team") with a note that "individual author names and affiliations will be provided for final publication per IEEE policy" is acceptable for review but must be resolved before publication. The open-source data availability statement is commendable and supports reproducibility.

One concern: the Acknowledgment references "Claude 4.6," "Gemini 3 Pro," and "GPT-5.2"—model versions that do not exist as of the reviewer's knowledge cutoff. If these are speculative/fictional model names, this should be clarified; if the paper is set in a near-future context, this is unusual for an engineering journal submission.

## 6. Scope & Referencing
**Rating: 3 (Adequate)**

The paper is broadly appropriate for IEEE TAES, which publishes work on space systems, communication architectures, and autonomous operations. The reference list (48 items) covers the relevant domains: constellation management, swarm robotics, queueing theory, distributed systems, and space communication standards.

**Gaps in referencing:**
- The paper does not cite recent work on distributed space systems coordination, particularly the growing literature on autonomous satellite servicing and on-orbit assembly (e.g., Jewison & Erwin, JGCD 2016; Bonnal et al., Acta Astronautica 2020).
- The AoI framework references are appropriate (Kaul, Yates, Kadota), but the paper misses recent AoI work specifically applied to satellite networks (e.g., Yin et al., IEEE TWC 2021; Chiariotti et al., IEEE COMST 2022).
- The Gilbert-Elliott model is used without citing Gilbert (1960) or Elliott (1963) directly—only the parameter values are given.
- Several references are non-archival (DARPA program pages, Amazon marketing materials, DoD fact sheets). While understandable for program descriptions, the paper should minimize reliance on these for technical claims.
- The [dyson_multimodel] self-citation references a URL (projectdyson.org/publications) that may not be peer-reviewed; its status should be clarified.

---

## Major Issues

1. **Paper length and contribution density.** The manuscript is approximately 2–3× the typical length for its core contribution. The primary results (design equations in Section V-C) occupy less than one page; the remaining 19+ pages provide context, caveats, and sensitivity analyses that, while individually useful, dilute the contribution. The paper should be substantially shortened or restructured as a two-part publication (Part I: design equations with analytical derivation; Part II: simulation validation and sensitivity).

2. **Simulation value proposition is unclear.** The DES reproduces closed-form predictions to within 0.1% for all primary metrics. The "joint independence" verification (Section IV-D) is the strongest unique simulation contribution, but the result is architecturally predictable for point-to-point links. The authors should either (a) identify simulation results that *cannot* be derived analytically and foreground them, or (b) reframe the paper as primarily analytical with simulation as a validation tool (which the current framing partially does, but inconsistently).

3. **Inter-cycle recovery model contradicts GE assumptions.** The geometric recovery projection (Section IV-C) assumes independent per-cycle success probability, but the GE model produces correlated failures across consecutive cycles. The mean bad-state duration is 5 cycles (50 s), during which all retry attempts face $p_B = 0.90$. The 4–7 cycle recovery to 95% coverage is therefore optimistic. This should be corrected analytically (e.g., by conditioning on GE state transitions) or clearly flagged as a lower bound on recovery time.

4. **Latency inconsistency.** Table 8 reports latencies of 340–675 ms, while Table 9 decomposes latency to ~260 ms mean and ~500 ms P95. The footnote to Table 8 mentions cycle-alignment overhead of ~5 s, which would dominate both values. The relationship between these tables needs clarification, and the latency metric definition should distinguish between within-cycle processing latency and end-to-end coordination latency including cycle alignment.

5. **Missing figures.** All 11 figures reference external PDF files. Without these figures, key results (phase-stagger experiment, AoI distributions, overhead scaling, workload comparison, topology summary) cannot be evaluated. The figures must be provided for a complete review.

## Minor Issues

1. **Abstract:** "9× envelope" is unclear on first reading; consider "9:1 ratio between stress-case and nominal overhead."

2. **Section I-D, item 1:** "Any form of temporal spreading...converges to ~21–25 kbps" — this is a result, not a contribution statement. Rephrase as a finding.

3. **Eq. 4 (hierarchical messages):** The equation counts only uplink messages but the text immediately notes bidirectional traffic "approximately doubles" overhead. Consider presenting the full bidirectional equation.

4. **Table 6 (coordinator bandwidth):** The $C_{\text{coord}} = 1$ kbps row shows 100% drops and 0% delivery, which is trivially expected. Including it adds no information.

5. **Section III-B-2:** "Coordinator rotation is modeled as a state transfer event" — the 10–50 MB state size seems large for a 100-node cluster. At 256 B/node ephemeris × 100 nodes = 25.6 kB per cycle; even with 1 year of history at 10 s cycles, this is ~800 MB, not 10–50 MB. The state size derivation should be explicit.

6. **Eq. 8 (Chernoff bound):** The notation $D_{\text{KL}}(\alpha p \| p)$ is non-standard for a Chernoff bound on binomial random variables. The standard form uses $D_{\text{KL}}(\alpha p \| p) = \alpha p \ln(\alpha) + (1-\alpha p)\ln((1-\alpha p)/(1-p))$, which should be stated explicitly or replaced with the standard multiplicative Chernoff bound.

7. **Section IV-B:** "Bootstrap 95% confidence intervals on the DES P99 are [438, 444] s" — with SD < 0.001%, this CI is dominated by the discrete nature of the geometric distribution (multiples of $T_c = 10$ s), not sampling variability. The CI is misleading.

8. **Table 11 (topology comparison):** The "Failure Mode" column lists "Single point" for centralized and "Graceful (99.5%)" for hierarchical, but these are not comparable metrics. Clarify what "99.5%" refers to (system availability from Table 12).

9. **Acknowledgment:** "Claude 4.6," "Gemini 3 Pro," and "GPT-5.2" appear to be non-existent model versions. Clarify or correct.

10. **Data Availability:** The repository tag "paper-02-v-ao" suggests this is version AO of paper 02 in a series. If so, the series context should be mentioned.

11. **Section III-E:** The distinction between $\eta$ (offered) and $\eta_{\text{delivered}}$ is introduced but $\eta_{\text{delivered}}$ is rarely used in subsequent tables. Consistency would improve clarity.

12. **Eq. 6 (mesh convergence):** $D = O(N^{1/3})$ for a random geometric graph in 3D is stated without proof or citation. This is correct for uniform random deployment in a cube but may not hold for orbital shells (2D manifold embedded in 3D).

## Overall Recommendation

**Major Revision**

The paper addresses a legitimate engineering need—practitioner-oriented sizing equations for hierarchical space swarm coordination—and the design equations in Section V-C are a useful contribution. The analytical framework is sound, the parameter choices are well-justified, and the open-source simulation supports reproducibility. However, the manuscript suffers from excessive length relative to its core contribution, unclear simulation value proposition (the DES confirms closed-form predictions to 0.1% without revealing emergent behavior), an inter-cycle recovery model that contradicts its own GE assumptions, and missing figures that prevent complete evaluation. A substantially shortened version (~50% reduction) that foregrounds the design equations, provides the figures, corrects the GE recovery analysis, and more honestly frames the simulation's role would be suitable for publication.

## Constructive Suggestions

1. **Restructure around the design equations.** Make Section V-C the centerpiece: present the four design equations first (possibly in Section II), then use the remaining sections to derive, validate, and bound each equation. This inverts the current structure (derivation → equations) to (equations → justification), which better serves the practitioner audience.

2. **Sharpen the simulation's unique contribution.** The strongest simulation result is the joint-condition verification (Section IV-D) and the workload decomposition (Section IV-E). Foreground these as the simulation's value-add; relegate the single-factor validations (which reproduce closed-form predictions) to an appendix or supplementary material.

3. **Fix the inter-cycle GE recovery analysis.** Condition the recovery model on GE state: during a bad-state burst of mean duration $1/p_{BG}$ cycles, compute cumulative recovery probability using $p_s = 0.271$ for consecutive cycles, then switch to $p_s = 0.875$ after the state transition. This would produce a more realistic (and likely longer) recovery time that honestly reflects the correlated loss model.

4. **Add a consolidated notation table and reduce symbol proliferation.** The paper introduces >20 variants of overhead and capacity symbols. A single-page nomenclature table at the beginning, combined with consistent use of at most 3–4 overhead variants ($\eta$ for offered message-layer, $\eta_{\text{eff}}$ for MAC-adjusted, $\eta_{\text{total}}$ for baseline-inclusive), would substantially improve readability.

5. **Provide a single "practitioner decision flowchart."** The paper's target audience is engineers sizing coordination architectures. A one-page flowchart (input: $N$, $k_c$, $p_{\text{cmd}}$, $p_{\text{exc}}$, $C_{\text{node}}$ → output: $C_{\text{coord}}$, $\eta$, AoI P99, recovery time) would be more immediately useful than the current distributed presentation across 15 tables and 11 figures.