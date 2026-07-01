---
paper: "02-swarm-coordination-scaling"
version: "bd"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-27"
recommendation: "Major Revision"
---

# Peer Review: "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms"

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a genuine gap: the absence of closed-form sizing relationships for hierarchical coordination architectures at the 10³–10⁵ node scale with byte-level traffic accounting. This is a practically relevant problem as mega-constellations grow beyond current ground-based coordination paradigms. The "practitioner toolkit" framing—providing design equations that engineers can use for system sizing—is a valuable contribution model for IEEE T-AES.

However, the novelty is more modest than the paper implies. The central finding—that architecture-specific overhead is only ~5% and commands dominate—is, upon reflection, somewhat predictable: summaries compress O(k_c) reports into one message, so of course aggregation overhead is small relative to per-node command traffic. The individual analytical components (M/D/1 queueing, geometric AoI distributions, Gilbert-Elliott Markov chains) are well-established; the contribution is their assembly and parameterization for this specific domain. The paper acknowledges this ("assembles standard queueing, geometric, and Markov-chain results"), but the claim of being the first to provide such relationships (Section I-A) is difficult to verify and somewhat undermined by the narrow operating regime (1 kbps RF-backup, <1% of operational time). The bandwidth scaling table (Table II) effectively shows that at ≥10 kbps, most of the interesting design tensions vanish.

The paper would benefit from a clearer articulation of what design decisions these equations actually change. If the coordinator bottleneck disappears at 10 kbps and the AoI/GE equations are bandwidth-independent, the practical utility of the 1 kbps analysis is limited to a rare contingency mode. This should be positioned more prominently rather than buried in Table II footnotes.

## 2. Methodological Soundness

**Rating: 3 (Adequate)**

The methodological framework has both strengths and significant concerns. On the positive side, the traffic accounting is meticulous (Tables IV, VI, VII), the overhead definition is carefully decomposed (baseline vs. protocol, offered vs. delivered), and the Monte Carlo configuration (30 replications, bootstrap CIs) is reasonable. The explicit TDMA frame derivation (Eq. 7, Section IV-A) and the half-duplex TX/RX partitioning analysis demonstrate engineering rigor.

The fundamental methodological concern is the **circular validation structure**. The DES and the closed-form equations operate at the same abstraction level—both count messages and bytes according to the same traffic model. The <0.1% agreement (Table VIII) confirms arithmetic consistency, not model validity. The paper acknowledges this ("their agreement confirms arithmetic consistency, not physical fidelity," Section III-A), but this acknowledgment does not resolve the problem: the paper's primary quantitative claims rest on unvalidated models. The GE channel model uses per-cycle state transitions with no justification from measured S-band ISL statistics; the coherence assumption (constant state within T_c = 10 s) is acknowledged as conservative but is essentially arbitrary. The collision avoidance rate (10⁻⁴/node/s) is described as "screening events" but the sensitivity analysis (±1.5 pp) suggests this parameter matters little—raising the question of why it is modeled at all.

The joint interaction verification (Section IV-D, Table IX) is a useful contribution, but the "pipeline decoupling" result is almost tautological under dedicated links: if lost messages never reach the queue, of course GE losses don't affect queue drops. The paper correctly notes this breaks under shared-medium contention, but the TDMA slot-time coupling (Eqs. 10–11) reveals that even under TDMA, the decoupling is incomplete—intra-cycle retry is infeasible at k_c = 100. This tension between the decoupling claim and the TDMA feasibility constraint deserves more careful treatment.

The static topology assumption is a significant limitation for LEO constellations. The paper bounds re-association overhead at <0.5% (Section V-B), but this estimate appears to be back-of-envelope rather than simulated. For cross-plane configurations—which are the norm for Walker constellations—cluster membership changes on 45–90 minute timescales, meaning the "static" assumption fails multiple times per orbit.

## 3. Validity & Logic

**Rating: 3 (Adequate)**

The internal logic of the paper is generally sound, and the authors are commendably transparent about limitations. The key results follow from the assumptions: O(N) message complexity yields O(1) overhead, the geometric distribution gives the AoI P99 formula, and the GE Markov chain gives the recovery CDF. The analytical cross-checks (Eq. 6 vs. Table V; Markov chain vs. DES in Fig. 5) are convincing within the model's scope.

Several logical tensions deserve attention. First, the stress-case η ≈ 46% is described as a "byte-budget upper bound" (abstract, Section IV-A), but Eq. 9 shows that per-node unicast commands require 22 cycles to deliver—meaning the stress case is not just a budget bound but is physically undeliverable in a single cycle. The paper acknowledges this but continues to use η ≈ 46% as a primary result metric throughout, which is misleading. The event-driven profile (η ≈ 6%) is described as "operationally representative" but receives far less attention. The paper would be more honest if it led with the 6% figure and treated the 46% as a schedulability analysis.

Second, the comparison between hierarchical and sectorized mesh (Table XII, capability matrix) is asymmetric in a way that favors the hierarchy. The sectorized mesh is evaluated at cap = 10 (3.2% sector coverage), which is deliberately crippled. At cap = 50 (15.8% coverage, η ≈ 90%), the mesh provides substantially more local awareness. The paper frames this as a "bandwidth–robustness tradeoff," which is fair, but the overhead ratios (1.4–1.5×) are computed at the capped variant where the mesh cannot perform fleet-wide functions. This comparison conflates bandwidth efficiency with functional capability.

Third, the coordinator failure transient analysis (Section III-B, labeled \label{sec:coord_failure_transient}) claims the impact is "modest" (+T_c = 10 s vs. P99 = 441 s), but this comparison is between a deterministic penalty and a statistical tail—apples and oranges. During the 3–5 s election window, the cluster has no coordinator; if a conjunction alert arrives during this window, the consequence could be severe regardless of average AoI.

## 4. Clarity & Structure

**Rating: 4 (Good)**

The paper is well-organized and generally well-written for a complex topic. The roadmap at the beginning of Section IV is helpful. The notation table (Table I) is clear. The explicit separation of baseline telemetry (20.5%) from protocol overhead (η) is a good practice that prevents confusion. The design equations summary (Section V-C) is a valuable practitioner reference.

The paper is, however, excessively long and repetitive. The same key numbers (η ≈ 46%, 5%, 6%; coordinator 21–25 kbps; AoI P99 = 440 s; GE P95 = 4 cycles) appear in the abstract, introduction, results, discussion, and conclusion—often with slightly different framing that creates confusion about what is a primary result vs. a derived quantity. The abstract alone is 150+ words of numbers. Significant compression is possible: the sectorized mesh analysis (Section III-B.4) could be shortened; the TDMA synchronization and guard-time sensitivity discussions (Section IV-A) are thorough but could be condensed.

Figures are referenced but not provided (understandable for review), making it difficult to assess their effectiveness. The tables are generally well-constructed, though Table III (simulation parameters) is dense and could benefit from grouping by relevance to specific research questions. The loss/miss taxonomy (Section III-E) is a valuable clarification that should appear earlier.

One structural concern: the paper oscillates between presenting the 1 kbps regime as the primary contribution and acknowledging it applies <1% of operational time. This creates a framing problem—the reader is unsure whether to evaluate the work as a contingency-mode analysis or a general coordination framework.

## 5. Ethical Compliance

**Rating: 4 (Good)**

The paper includes an appropriate AI-assistance disclosure in the Acknowledgment section, noting that Claude 4.6, Gemini 3 Pro, and GPT-5.2 were used for ideation but that results are not validated by those tools. The open-source data availability statement with a specific repository tag is commendable and supports reproducibility.

The anonymous authorship ("Project Dyson Research Team") with a note about providing names for final publication is unusual but not unprecedented. The IEEE policy reference is appropriate. No conflicts of interest are apparent, though the relationship between the authors and the "Project Dyson" organization should be clarified.

One minor concern: the reference to future AI model versions (Claude 4.6, GPT-5.2) suggests this manuscript may be set in a near-future context, which is unusual for a peer-reviewed submission. If these are actual tools used, no issue; if speculative, this should be clarified.

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is appropriate for IEEE T-AES in scope, addressing spacecraft coordination at scale. The reference list (50+ citations) covers the relevant domains: constellation operations, swarm robotics, queueing theory, distributed systems, and AoI. Key works are cited (Kleinrock, Lamport, Ongaro/Raft, Demers gossip, Kaul/Yates AoI).

Several gaps in the references are notable. First, there is no citation of the extensive DTN/contact-graph-routing literature for scheduled LEO contacts (Fraire et al., 2021, IEEE TNSM; Araniti et al., 2015), which is directly relevant to the TDMA scheduling and intermittent-link aspects. Second, the paper does not cite recent work on distributed satellite autonomy beyond NASA DSA—e.g., ESA's OPS-SAT experiments or the growing literature on onboard AI for constellation management. Third, the AoI literature is cited but the connection to the substantial body of work on AoI-optimal scheduling (Sun et al., 2017; Bedewy et al., 2019) is not explored—these works would inform the exception telemetry design. Fourth, several references are non-archival (Amazon Kuiper overview, DARPA program pages, DoD fact sheets), which is acceptable for context but should not be relied upon for technical claims.

The related work section (Section II) is adequate but somewhat superficial—it lists relevant work without deeply engaging with how prior results inform or differ from the present analysis. For example, the Handley [2018] and Del Portillo [2019] papers on mega-constellation routing are cited but their capacity/latency findings are not compared against the present model's predictions.

---

## Major Issues

1. **Validation gap undermines quantitative claims.** The <0.1% DES-to-analytical agreement confirms only arithmetic consistency at the message layer. No physical-layer validation exists—not even a single-cluster NS-3 simulation. The paper's primary quantitative outputs (η values, coordinator capacity, AoI distributions, GE recovery times) are all model-internal. The paper should either (a) include at least a minimal packet-level validation for one configuration, or (b) substantially temper the claims to "design equations pending physical-layer validation" throughout, not just in Section V-A.

2. **Stress-case η ≈ 46% is misleading as a primary metric.** Equation 9 shows per-node unicast requires 22 cycles (3.7 min) to deliver at 1 kbps. This means the stress-case is not achievable in a single coordination cycle—it is a multi-cycle scheduling problem, not an overhead metric. The paper should restructure to lead with the event-driven profile (η ≈ 6%) as the primary result and treat the stress-case as a schedulability/capacity-planning analysis.

3. **GE model parameters are unjustified.** The Gilbert-Elliott parameters (p_GB = 0.05, p_BG = 0.50, p_G = 0.01, p_B = 0.90) are presented without reference to any measured S-band ISL channel data. The paper states "no measured channel statistics assumed" as if this were a feature, but it means the recovery time results (P95 = 4 cycles) are conditional on arbitrary parameters. The sensitivity sweep (Fig. 5b) partially addresses this, but the default parameters should be motivated by at least order-of-magnitude physical reasoning (e.g., typical obstruction durations, antenna shadowing statistics from LEO missions).

4. **Asymmetric baseline comparison.** The centralized baseline models only compute-queue scalability (M/D/c), not communication overhead; the global-state mesh is an intentional worst case. This means the only valid cross-architecture communication comparison is hierarchical vs. sectorized mesh. Yet the paper's framing (Fig. 8, Table XI) presents all four topologies as if they are compared on equal footing. The asymmetry is acknowledged in footnotes but should be elevated to the main text and reflected in the figures.

5. **Static topology assumption is inadequately bounded for the target regime.** The <0.5% re-association overhead estimate and the "1–3 cycle AoI transient" claim (Section V-B) are not simulated. For Walker-type constellations with 10–20 orbital planes, cluster boundary crossings affect a significant fraction of nodes continuously. A single simulation run with periodic re-association events would substantially strengthen the paper.

---

## Minor Issues

1. **Abstract length and density.** The abstract exceeds typical IEEE T-AES guidelines and contains too many specific numbers. Consider reducing to the three key design equations and their implications.

2. **Eq. 2 (M/D/1 waiting time):** The standard Pollaczek-Khinchine formula for M/D/1 is W_q = ρ/(2μ_s(1−ρ)), which is correct, but the paper should note this is the mean waiting time for the *deterministic* service case specifically (coefficient of variation = 0), not the general M/G/1 result.

3. **Table III footnotes:** Footnote markers jump from (a) to (c) to (d), skipping (b). This appears to be a formatting error.

4. **Section III-B.2, Eq. 5:** The message count formula M_total = N + N/k_c + N/(k_c · k_r) counts only upward (report) traffic. The text states "the DES models full bidirectional traffic," but the equation does not reflect this. Either extend the equation or clarify it represents upward flow only.

5. **"Offered vs. delivered overhead" (Section III-E):** This distinction is introduced but η_delivered is never formally defined or used in any equation. Either formalize it or remove the distinction.

6. **Table IX (Joint Interaction):** The "GE + Exc." column shows dramatically fewer drops than "No Loss" at the same capacity (e.g., 377 vs. 122,510 at 15 kbps). This is because exception telemetry reduces offered load, not because of any GE interaction. The table caption should make this clearer—currently it could be misread as GE somehow reducing drops.

7. **Section IV-A, TDMA sync discussion:** The Slotted ALOHA fallback analysis is useful but the load-shedding rule ("upon sync-beacon loss, suppress commands and reduce to exception-only reporting") is stated without analysis of how quickly the system detects sync loss or the transient behavior during mode transition.

8. **Eq. 7 (γ derivation):** The derived γ = 0.949 vs. the assumed γ = 0.85 represents a 12% discrepancy. The additional overheads cited (FEC ~7%, ranging ~3%, control channel ~5%) sum to ~15%, which would give γ ≈ 0.949 × 0.85 ≈ 0.81, not 0.85. The accounting should be made explicit.

9. **Reference [1] (starlink_ops):** Citing an FCC filing and a "non-archival" personal website as the primary Starlink operations reference is weak. A peer-reviewed source or at least an official SpaceX technical document would be preferable.

10. **Section V-C, geometric approximation:** The statement "overestimates P95 by 0–1 cycles" should specify the parameter range over which this bound holds.

11. **Power budget (Section IV-H.3):** The 15 W coordinator increment over 5 W baseline (4× increase) is stated as "within typical power margins," but this is a substantial transient load for a small satellite. The thermal implications of intermittent 20 W operation should be noted.

12. **Inconsistent use of "stress-case" vs. "stress case"** throughout the paper. Standardize.

---

## Overall Recommendation

**Major Revision**

The paper addresses a relevant problem and provides a well-structured analytical framework for sizing hierarchical coordination in large space swarms. The traffic accounting is meticulous, the design equations are clearly presented, and the open-source commitment supports reproducibility. However, three fundamental issues require substantial revision: (1) the absence of any physical-layer validation means all quantitative claims are model-internal, and the <0.1% DES agreement is arithmetic verification, not validation; (2) the stress-case η ≈ 46% is prominently featured despite being undeliverable in a single cycle, creating a misleading impression of the system's actual operating point; and (3) the GE channel model and static topology assumption are insufficiently grounded in physical reality for the target application. A major revision should include at minimum a packet-level validation of one configuration, restructured presentation leading with the operationally representative workload, and either measured channel statistics or a more thorough physical justification of the GE parameters.

---

## Constructive Suggestions

1. **Add a minimal packet-level validation.** Implement a single-cluster (k_c = 100) NS-3 or OMNeT++ simulation with TDMA PHY, half-duplex constraints, and realistic propagation. Compare coordinator ingress, drop rates, and AoI against the message-layer predictions. Even a single configuration point would transform the paper's credibility. This is identified as future work but should be a prerequisite for publication in T-AES.

2. **Restructure around the event-driven workload.** Lead with η_E ≈ 6% as the primary operating point. Present the stress-case (η_S ≈ 46%) as a capacity-planning bound with explicit schedulability analysis (Eq. 9). This reframing is more honest and actually makes the hierarchical architecture look *better*—6% overhead for full cluster coordination is an impressive result.

3. **Ground the GE parameters in physical reasoning.** Even without measured ISL statistics, the authors could derive order-of-magnitude coherence times from known LEO obstruction mechanisms: Earth occultation (~35 min), structural shadowing on multi-panel spacecraft (~seconds), solar panel interference (~minutes). Map these to p_BG ranges and identify which regime each design curve in Fig. 5(b) corresponds to. This would transform the parametric sweep from an abstract exercise into actionable engineering guidance.

4. **Simulate cluster re-association.** Run at least one configuration with periodic membership changes (e.g., every 90 minutes, 10% of nodes re-associate). Measure the actual AoI transient and overhead impact. This would either confirm the <0.5% bound or reveal important dynamics that the static model misses.

5. **Tighten the topology comparison.** Either model centralized communication overhead (uplink scheduling, ground contact windows) to enable fair cross-architecture comparison, or explicitly restrict all comparative claims to hierarchical vs. sectorized mesh. Remove or clearly label the centralized and global-mesh curves in Fig. 8 as "partial models" rather than presenting them alongside fully-modeled architectures.