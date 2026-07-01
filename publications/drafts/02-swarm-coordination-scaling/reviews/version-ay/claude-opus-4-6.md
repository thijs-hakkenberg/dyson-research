---
paper: "02-swarm-coordination-scaling"
version: "ay"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-27"
recommendation: "Major Revision"
---

# Peer Review: "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms"

## 1. Significance & Novelty
**Rating: 3 (Adequate)**

The paper addresses a genuine gap: there is no systematic, byte-level traffic accounting framework for comparing coordination architectures at the 10³–10⁵ node scale. The assembly of standard queueing, AoI, and Gilbert-Elliott results into a unified "practitioner toolkit" has practical value, and the parameterization by per-node bandwidth is a useful design contribution. The open-source Monte Carlo tool adds reproducibility.

However, the novelty is limited in several respects. The individual analytical components (M/D/1 queueing, geometric AoI under Bernoulli reporting, GE channel models, gossip convergence bounds) are all well-established textbook results. The paper's contribution is their composition and parameterization for a specific application domain, not new theory. The authors acknowledge this ("assembling standard queueing, geometric, and Markov-chain results"), but the framing as "design equations" somewhat overstates the intellectual contribution—these are largely substitutions of application-specific parameters into known formulas. The 1 kbps RF-backup regime, while well-motivated, is explicitly stated to occupy <1% of operational time, which raises questions about the practical significance of optimizing this regime so extensively. The paper would benefit from more clearly articulating what design decisions would change based on these equations that could not be made with back-of-envelope calculations.

The comparison with baselines is structurally asymmetric (acknowledged by the authors): the centralized model omits communication-layer overhead, and the global-state mesh is an intentional worst case. This limits the practical utility of the cross-architecture comparison. The sectorized mesh comparison is the most informative, but the 1.35–1.95× overhead ratio is modest and may not drive architecture selection in practice.

## 2. Methodological Soundness
**Rating: 3 (Adequate)**

The methodology is internally consistent and carefully documented. The distinction between verification (DES confirms closed-form implementation) and validation (physical-layer confirmation) is commendable and unusually honest for this type of paper. The traffic accounting is thorough, with Table VI providing a clear audit trail. The 30 MC replications with bootstrap CIs and the per-run-then-aggregate P99 methodology (Table V footnote) are statistically appropriate.

Several methodological concerns warrant attention. First, the DES is cycle-aggregated at 10 s resolution, which means all within-cycle dynamics (TDMA slot allocation, half-duplex switching, retransmission timing) are not actually simulated—they are analytically imposed. The claim that the DES "verifies" the closed-form equations is therefore somewhat circular: the DES implements the same message-layer accounting as the closed forms, so agreement to 0.1% is expected by construction, not a meaningful validation. The authors state this explicitly in Section III-A, but the paper's structure (presenting DES results as confirmatory evidence) may mislead readers about the strength of this verification.

Second, the coordinator service model assumes deterministic 5 ms/msg processing, but the batch arrival model (D[k_c]/D/1) is not standard and its interaction with the token-bucket shaper (Model B) is not rigorously analyzed. The claim that "cross-cycle token carry-over does not violate the timeliness constraint" (Section IV-A) deserves formal proof rather than assertion—if the coordinator is persistently overloaded, tokens from idle periods may not compensate.

Third, the GE model's per-cycle coherence assumption (state constant within T_c = 10 s) is a strong simplification. While the authors provide coherence-time bounds (Section IV-C), the practical relevance of the default p_BG = 0.50 is unclear—no empirical data or link budget analysis supports this choice for any specific orbit/frequency combination. The sensitivity sweep partially addresses this, but the default parameters drive the headline results.

Fourth, the collision avoidance rate of 10⁻⁴/node/s is stated to represent "screening events, not maneuvers," but the paper does not model the actual conjunction assessment workflow (covariance propagation, screening volume, maneuver decision). The ±1.5 pp sensitivity to this rate suggests it is not a dominant factor, but the disconnect between the simplified alert model and operational conjunction management weakens the practical relevance claim.

## 3. Validity & Logic
**Rating: 3 (Adequate)**

The internal logic is generally sound, and the authors are commendably transparent about limitations. The pipeline decoupling result (Table VIII, identical "No Loss" and "GE Only" columns) is well-explained and the scope limitation to dedicated links is clearly stated. The AoI cross-check (Eq. 11 vs. DES, 440 vs. 441 s) is convincing.

However, several logical issues require attention:

1. **The headline overhead range (5–46%) is misleading.** The 46% stress-case assumes every node receives a 512-byte command every cycle—a fleet-wide maneuver campaign sustained for the entire simulation year. The 5% nominal case assumes no commands at all. The paper acknowledges this but the abstract and conclusion lead with the full range, which obscures the fact that the architecture-specific overhead (summaries, heartbeats, election) is only ~5%. The dominant overhead component (commands) is topology-invariant, as the authors note. This significantly weakens the claim that the hierarchical architecture has distinctive overhead characteristics.

2. **The sectorized mesh comparison assumes identical γ**, but the authors note (Section IV-G) that the sectorized mesh "requires distributed scheduling" while hierarchical "structurally supports TDMA." This is a significant practical difference that is acknowledged but not quantified. The overhead comparison at equal γ may therefore be optimistic for the sectorized mesh.

3. **The static topology assumption** is bounded analytically at <0.5% overhead for cross-plane drift, but this analysis assumes a single re-association per 90 minutes. In practice, Walker-delta constellations with multiple shells would have more complex cluster dynamics, and the 1–3 cycle AoI transient during re-association could compound across multiple simultaneous re-associations in a cluster.

4. **The centralized baseline asymmetry** is well-documented but undermines RQ3. The paper cannot meaningfully answer "where does hierarchical overhead fall relative to centralized" because the centralized model omits communication overhead. The honest framing in Table IX footnote (d) partially addresses this, but the topology comparison figure (Fig. 9) still presents the centralized curve alongside the others, which may mislead.

## 4. Clarity & Structure
**Rating: 4 (Good)**

The paper is well-organized with a clear roadmap (Section IV opening paragraph) and consistent notation. The distinction between η (protocol overhead beyond baseline) and η_total (including baseline telemetry) is maintained throughout. Tables are comprehensive and well-formatted; the traffic accounting tables (V, VI, VII) provide an unusually complete audit trail. The design equations summary (Section V-D) is a valuable practitioner reference.

The paper is, however, excessively long and detailed for a journal article. The TDMA synchronization discussion (Section IV-A, ~500 words on sync beacon loss, Slotted ALOHA fallback, and load-shedding rules) reads more like a system design document than a research paper. Similarly, the half-duplex TX/RX partitioning analysis, while thorough, could be condensed. The paper would benefit from moving some of this operational detail to an appendix or supplementary material.

The abstract is dense but accurate—it correctly qualifies all major claims. However, at ~250 words, it is at the upper limit for IEEE TAES and could be tightened. The parenthetical qualifications (e.g., "(analytical estimate)," "(both modeled at the communication layer)") are necessary but make the abstract difficult to parse on first reading.

Some notation inconsistencies: $p_{\text{link}}$ appears to denote both link availability (Table V) and per-transmission success probability (Table X); the relationship between these and the GE model parameters ($p_G$, $p_B$) could be clearer. The variable $r$ (reporting rate, 0.1 msg/s) is introduced in Eq. 1 but not formally defined until Table IV.

## 5. Ethical Compliance
**Rating: 4 (Good)**

The AI-assistance disclosure in the Acknowledgment section is forthright: "An AI-assisted ideation exercise (Claude 4.6, Gemini 3 Pro, GPT-5.2; see [52]) motivated aspects of the coordinator architecture but is not validated here." This is appropriate and meets current IEEE guidelines. The open-source data availability statement with a specific repository tag enhances reproducibility.

The anonymous authorship ("Project Dyson Research Team") with a footnote promising individual names for final publication is unusual but acceptable for review. The paper should ensure compliance with IEEE's authorship policy, which requires that all listed authors meet the criteria for authorship (intellectual contribution, drafting/revision, approval of final version).

One minor concern: the reference to future AI model versions (Claude 4.6, GPT-5.2) that do not exist as of mid-2025 suggests the paper may be set in a near-future context or uses speculative version numbers. This should be clarified or corrected.

## 6. Scope & Referencing
**Rating: 3 (Adequate)**

The paper is appropriate for IEEE TAES in scope, addressing autonomous spacecraft coordination with quantitative engineering analysis. The reference list (56 entries) is comprehensive, covering constellation operations, swarm robotics, distributed systems theory, queueing theory, and space standards (CCSDS). Key foundational works are cited (Kleinrock, Lamport, Raft, gossip protocols, AoI framework).

Several gaps in the references are notable:

1. **No citation of actual ISL link budget analyses** for LEO constellations. The 1 kbps budget is motivated qualitatively but not grounded in published link budgets for S-band TT&C in LEO. Works by Radhakrishnan et al. (2016) on inter-satellite link design or the CCSDS Proximity-1 link budget methodology would strengthen the parameter justification.

2. **No reference to existing hierarchical constellation management work.** The European Space Agency's Space Safety Programme and the Space Data Association's conjunction screening services implement hierarchical coordination operationally. The DARPA Blackjack program (cited) specifically explored autonomous satellite coordination with hierarchical elements.

3. **The swarm robotics references are dated.** Brambilla (2013) and Dorigo (2021) are surveys; more recent experimental work on large-scale swarm coordination (e.g., Slavkov et al. 2018 on kilobot swarms, or Rubenstein et al. 2014 on 1024-robot swarms) would better contextualize the scalability gap claim.

4. Several references are non-archival (Amazon Kuiper overview, DARPA program pages, DoD fact sheets). While unavoidable for some operational programs, the paper should minimize reliance on these for technical claims.

---

## Major Issues

1. **Circular verification claim.** The DES operates at the identical abstraction level as the closed-form equations (message-layer, cycle-aggregated, same loss models). The <0.1% agreement is therefore a code-consistency check, not an independent verification. The paper should either (a) clearly relabel this as "implementation consistency checking" rather than "verification," or (b) introduce at least one DES feature that operates at a finer granularity than the closed forms (e.g., within-cycle TDMA slot simulation) to provide genuine independent verification. The current framing risks overstating the confidence level.

2. **Topology-invariant command overhead dominates.** The stress-case headline number (η ≈ 46%) is dominated by commands (>60% of traffic), which are topology-invariant. The architecture-specific overhead is only ~5%. This means the paper's primary quantitative result—the overhead comparison—does not meaningfully differentiate the hierarchical architecture from alternatives. The paper should restructure its claims to foreground the architecture-specific 5% and treat the command-inclusive 46% as a system-level budget check, not an architecture comparison metric.

3. **No physical-layer grounding for key parameters.** The GE model parameters (p_BG = 0.50, p_B = 0.90, p_GB = 0.05), the 1 kbps budget, and the 10 s coordination cycle are all assumed without link budget analysis or empirical justification. While the sensitivity sweeps partially address this, the default parameters drive all headline results. The paper should either (a) derive these from a representative link budget (S-band, 500 km range, specific antenna gain, specific interference environment) or (b) present results as a family of curves parameterized by these quantities (partially done for GE parameters in Fig. 7, but not for C_node or T_c).

4. **Asymmetric baseline comparison undermines RQ3.** The centralized baseline models only processing (M/D/c queue) while the hierarchical model includes full communication-layer accounting. The paper acknowledges this repeatedly but still presents cross-architecture comparisons (Table IX, Fig. 9) that implicitly suggest the hierarchical architecture is superior. Either the centralized model should be extended to include communication overhead (uplink scheduling, ground contact windows), or the cross-architecture comparison should be removed entirely, restricting the paper to hierarchical characterization and the sectorized mesh comparison.

5. **Half-duplex feasibility under stress-case is unresolved.** Section IV-A acknowledges that node-specific unicast commands require 16.9 s at 24 kbps, exceeding T_c = 10 s. The proposed solutions (multi-cycle staggering or higher PHY rate) are mentioned but not analyzed. Since the stress-case (one command per node per cycle) is the headline scenario, this feasibility gap is significant. The paper should either (a) formally analyze the staggered command model and its impact on η and AoI, or (b) redefine the stress-case to use broadcast commands only and note the unicast limitation.

---

## Minor Issues

1. **Eq. 2 (M/D/1 waiting time):** The standard Pollaczek-Khinchine formula for M/D/1 is $W_q = \rho / (2\mu_s(1-\rho))$, which is correct, but the paper should note this applies to the waiting time in queue, not the total sojourn time (which adds $1/\mu_s$).

2. **Table I:** "Representative System" column entries are informal (e.g., "Hyperscale data center"). These should either be removed or replaced with specific system references.

3. **Section III-B-3 (Global-State Mesh):** The statement "with f = O(N/log N)" appears without derivation. Standard gossip uses f = O(log N); the O(N/log N) fanout seems to be chosen to force O(N²) total messages. Clarify whether this is a modeling choice or a claimed result.

4. **Eq. 6 (sector overhead):** The equation gives bytes, not bits; the conversion to η in Table III footnote (a) uses ×8 but this should be made explicit in the equation itself.

5. **Table V (AoI results):** The "Periodic baseline" row appears twice (as the first row and as p_exc = 1.0). One should be removed.

6. **Section IV-A, TDMA frame model:** The derived γ = 0.949 (Eq. 9) is based on specific assumptions (32-bit preamble, 16-bit header, CRC-16, 4.7 ms guard). The conservative γ = 0.85 is then retained by adding FEC, ranging, and control-channel overhead as percentages. These additional overheads should be itemized more rigorously rather than estimated as round percentages.

7. **Fig. 8 caption:** States "DES bars (30 MC replications, N = 10,000, k_c = 100)" but the figure is not included for review. Ensure the histogram bin widths are appropriate for the sample size.

8. **Section V-B (Limitations, static topology):** The cross-plane drift analysis assumes "one re-association per 90 min per affected node" but does not quantify what fraction of nodes are "affected" at any given time. For a Walker-delta constellation, this could be a significant fraction at orbital-plane intersections.

9. **Acknowledgment section:** References to "Claude 4.6" and "GPT-5.2" appear to be future/fictional model versions. Correct to actual model identifiers used.

10. **Table IV (Simulation Parameters):** The footnote markers skip from (a) to (c) to (d), missing (b).

11. **Section III-E:** "Peak vs. average rate distinction" paragraph is important but buried. Consider promoting this to a formal definition or moving it earlier in the paper.

12. **Eq. 4 (hierarchical messages):** Should include the bidirectional command traffic to match the claimed η ≈ 46%. As written, it only counts upward-flowing messages.

---

## Overall Recommendation

**Major Revision**

The paper addresses a legitimate gap in the literature and provides a useful engineering framework, but several issues prevent acceptance in its current form. The circular nature of the DES "verification" (same abstraction level as the closed forms), the dominance of topology-invariant command overhead in the headline metric, the asymmetric baseline comparison, and the lack of physical-layer grounding for key parameters all require substantial revision. The paper's greatest strength—its transparency about limitations—also reveals that the actual contribution (assembling known results into a parameterized toolkit) is more modest than the framing suggests. A revised version should (1) restructure claims around the architecture-specific 5% overhead rather than the command-inclusive 46%, (2) either extend the centralized baseline or remove the cross-architecture comparison, (3) ground at least the default GE parameters in a representative link budget, and (4) resolve the half-duplex feasibility issue for the stress-case scenario. The paper has the potential to be a solid practitioner reference if these issues are addressed.

---

## Constructive Suggestions

1. **Restructure the contribution around architecture-specific overhead.** The most defensible and novel claim is that hierarchical coordination adds only ~5% overhead (summaries, heartbeats, election) beyond topology-invariant traffic. Lead with this in the abstract and conclusion. Present the command-inclusive 46% as a system-level feasibility check, not the primary result. This reframing would make the contribution clearer and less vulnerable to the criticism that commands dominate and are topology-invariant.

2. **Add a minimal link budget analysis.** Derive the 1 kbps budget, GE default parameters, and T_c = 10 s from a representative S-band link budget (e.g., 500 km range, 0 dBi omnidirectional antenna, 1 W transmit power, S-band noise temperature). This would ground the parameter choices and demonstrate that the design equations produce physically meaningful results. Even a single-page appendix with a link budget table would substantially strengthen the paper.

3. **Implement within-cycle TDMA slot simulation in the DES.** Adding a sub-cycle simulation layer that models individual TDMA slot allocation, half-duplex switching, and retransmission timing would provide genuine independent verification of the closed-form TDMA analysis (Eqs. 9–10) and resolve the half-duplex feasibility question. This need not be the full NS-3 validation called for in Section V-A—a simplified slot-level model within the existing Python framework would suffice.

4. **Consolidate the operational design detail.** Move the TDMA synchronization fallback, load-shedding rules, sync-beacon loss analysis, and half-duplex partitioning to a dedicated "Operational Considerations" appendix. The main text should present the design equations and their verification; the operational detail, while valuable, obscures the core contribution and makes the paper difficult to follow.

5. **Extend the sectorized mesh comparison.** Since this is the only fair cross-architecture comparison (both modeled at the communication layer), invest more analysis here. Specifically: (a) model the distributed scheduling overhead for the sectorized mesh (which would increase its effective γ penalty), (b) compare fault tolerance quantitatively (not just qualitatively), and (c) analyze the sectorized mesh under GE losses to determine whether the pipeline decoupling property is unique to the hierarchical architecture or also holds for sector-coordinator links.