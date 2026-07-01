---
paper: "02-swarm-coordination-scaling"
version: "az"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-27"
recommendation: "Major Revision"
---



# Peer Review: "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms"

**Manuscript Version:** AZ
**Venue:** IEEE Transactions on Aerospace and Electronic Systems

---

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a genuine gap: there is no published, systematic byte-level comparison of coordination architectures for autonomous space swarms at the $10^3$–$10^5$ scale. The framing as a "practitioner toolkit" of closed-form design equations is appealing and, if validated, would be useful for mission architects sizing coordination links for future mega-constellations. The assembly of standard queueing, AoI, and Gilbert-Elliott results into a coherent sizing framework has practical value.

However, the novelty is limited in several respects. The individual analytical components (M/D/1 queueing, geometric AoI under Bernoulli reporting, GE Markov-chain recovery) are textbook results. The paper's contribution is their *assembly and parameterization* for a specific application domain, not new theory. The authors acknowledge this ("assembling standard queueing, geometric, and Markov-chain results"), which is honest but undercuts the novelty claim. The $O(1)$ overhead scaling of hierarchical architectures with fixed fan-out is well-known from distributed systems theory; demonstrating it numerically at $N = 10^5$ with specific message sizes, while useful, is not surprising.

The claimed operating regime—1 kbps RF backup used <1% of operational time—raises a question of practical significance. If this regime is rarely encountered, the design equations govern an edge case. The authors argue the equations generalize to any $C_{\text{node}}$, but the entire quantitative analysis (stress-case utilization, coordinator bottleneck) is specific to 1 kbps. At 10 kbps, the authors themselves note the coordinator bottleneck "disappears entirely," which somewhat undermines the urgency of the sizing problem. The paper would benefit from a clearer articulation of *when* these equations are decision-critical versus merely confirmatory.

## 2. Methodological Soundness

**Rating: 3 (Adequate)**

The analytical framework is internally consistent and the closed-form derivations are correct as far as I can verify. The TDMA frame analysis (Eq. 6–7), AoI geometric derivation (Eq. 8), and GE Markov recovery CDF are standard and properly applied. The DES verification achieving <0.1% agreement with closed forms is expected given that both operate at the same abstraction level—this is a code-correctness check, not an independent validation, and the authors are commendably clear about this distinction (Section III-A).

**Concern 1: Circular verification.** The DES and closed-form equations share identical assumptions (message sizes, rates, loss models, no MAC dynamics). The <0.1% agreement therefore verifies arithmetic consistency, not model adequacy. The paper repeatedly emphasizes this, but the sheer volume of DES results (30 MC replications, multiple parameter sweeps) may give readers a false sense of empirical grounding. The inter-cycle GE recovery tail statistics (Fig. 5) are the one area where the DES provides genuinely independent information beyond the closed forms, and this is a legitimate contribution.

**Concern 2: Abstraction level.** Table IV lists critical phenomena that are abstracted away: MAC-layer contention, link acquisition, half-duplex turnaround, antenna beam scheduling, Earth-occlusion outages, priority queueing, and multi-hop store-and-forward. The $\gamma$ parameter is asked to absorb MAC efficiency, FEC overhead, ranging, control channels, antenna slew, and contention—a heavy burden for a single scalar. The derived $\gamma = 0.949$ (Eq. 6) accounts only for guard time; the conservative $\gamma = 0.85$ is stated to cover FEC (~7%), ranging (~3%), and control channels (~5%), but these percentages are asserted without derivation or citation. The gap between 0.949 and 0.85 (6.4 percentage points) is smaller than the sum of the claimed additional overheads (15%), suggesting internal inconsistency.

**Concern 3: Static topology assumption.** The analytical bound on re-association overhead (<0.5%) is reasonable for byte-level overhead but does not address the more serious concern: cluster membership churn affects the *coordinator's state completeness* and the validity of aggregated summaries during transitions. The 1–3 cycle AoI transient is acknowledged but not modeled in the DES, which uses fixed membership for the full year. For a Walker-delta constellation at 550 km with 72 planes, boundary crossings would affect a non-trivial fraction of nodes quasi-continuously, not just "5–15% at any instant."

**Concern 4: Message model rigidity.** The fixed message sizes (256 B status, 512 B command, 64 B heartbeat) are asserted without sensitivity analysis on message size itself. The 512-byte cluster summary is stated to contain "mean elements + covariance" for up to 100 members—this is extremely compressed (5.12 bytes per member for a 6-element state vector plus covariance). The information-theoretic adequacy of this compression for conjunction screening is not discussed.

## 3. Validity & Logic

**Rating: 3 (Adequate)**

The conclusions are logically supported *within the stated abstraction level*, and the authors are unusually transparent about limitations. The distinction between verification and validation (Section III-A) is well-drawn. The pipeline decoupling result (Section IV-D, Table VII) is clearly stated with its conditions and limitations. The coherence-time bounds for the GE model (Section IV-C) are a thoughtful addition.

**Issue 1: Comparison fairness.** The topology comparison (Table X) is structurally asymmetric. The centralized model captures only compute-queue scalability (no communication overhead modeled); the global-state mesh is an intentional worst case; the sectorized mesh uses a capped fanout that limits it to 3.2% sector awareness. The hierarchical architecture is the only topology modeled with full bidirectional traffic accounting. While the authors acknowledge this (footnote d in Table X, and Section IV-G), the paper's structure—with the hierarchical architecture as the "architecture under study" and all others as "reference baselines"—creates an inherently favorable framing. The sectorized mesh comparison is the most meaningful, but the functional utility argument (full cluster awareness vs. 3.2% sector coverage) conflates two different design objectives: the mesh provides *local* awareness to every node, while the hierarchy provides *aggregated* awareness through a coordinator. These serve different operational needs.

**Issue 2: The stress-case dominance.** The paper's headline result ($\eta \approx 46\%$) is driven almost entirely by the stress-case command model (512 B per node per cycle). The decomposition (Fig. 8) shows commands account for >60% of stress-case traffic, independent of topology. This means the overhead comparison between hierarchical and sectorized mesh is largely a comparison of how each handles the *same* command traffic, not a comparison of coordination overhead per se. The architecture-specific overhead (~5%) is the more meaningful differentiator, but it receives less emphasis.

**Issue 3: Coordinator ingress as "bottleneck."** The paper identifies coordinator ingress (21–50 kbps) as the binding constraint, but this is an artifact of the 1 kbps per-node budget. At any reasonable ISL rate (even 10 kbps), the bottleneck vanishes. The extensive analysis of Models A/B, token-bucket smoothing, and phase staggering addresses a problem that exists only in the specific RF-backup regime. This is acknowledged but could be stated more prominently.

**Issue 4: Half-duplex feasibility.** The TDMA frame-time analysis (Eqs. 9–10) reveals that intra-cycle retransmission is infeasible under GE steady-state conditions (ingress = 10,829 ms > $T_c$ = 10,000 ms). This is presented as confirming the inter-cycle recovery design, but it also means the system cannot achieve full per-cycle completion under correlated loss—a significant operational limitation that deserves more discussion. The 27.1% intra-cycle recovery rate under GE bad-state means that during a bad-state cycle, ~73 out of 100 members' reports are lost, and the coordinator's summary for that cycle is based on only ~27 members. The quality of the aggregated summary under such conditions is not analyzed.

## 4. Clarity & Structure

**Rating: 3 (Adequate)**

The paper is ambitious in scope and generally well-organized, with a clear roadmap at the start of Section IV. The design equations summary (Section V-D) is a useful practitioner reference. Tables are generally well-constructed with appropriate footnotes. The explicit distinction between $\eta$ (protocol overhead beyond baseline) and $\eta_{\text{total}}$ (including baseline telemetry) is helpful once understood.

However, the paper suffers from excessive length and density. At approximately 12,000 words of body text plus extensive tables, it substantially exceeds typical IEEE TAES limits. The abstract alone is ~280 words and reads more like an executive summary, attempting to convey every nuance rather than the key findings. Many qualifications and caveats, while individually valuable, collectively make the paper difficult to parse. For example, the coordinator bandwidth section (IV-A) discusses Models A and B, TDMA frame analysis, half-duplex partitioning, broadcast vs. unicast commands, frame-time feasibility, synchronization, degraded-mode fallback, and load-shedding rules—all for a single subsection. A reader seeking the design equation ($C_{\text{coord}} \geq 20.5$ kbps) must navigate through extensive discussion of edge cases.

The notation is mostly consistent but occasionally overloaded. $\eta$ appears with subscripts (DES, analytic, eff, total, sector, stress) that are not always defined at first use. The relationship between $\eta$, $\eta_{\text{total}}$, and $\eta_{\text{eff}}$ requires careful tracking. The paper would benefit from a notation table.

Several figures are referenced but provided as filenames only (e.g., `fig-architecture-diagram.pdf`), making it impossible to evaluate their quality. The figure captions are informative, but without seeing the actual figures, I cannot assess whether they effectively communicate the results.

## 5. Ethical Compliance

**Rating: 4 (Good)**

The paper includes an explicit acknowledgment of AI-assisted ideation (Claude 4.6, Gemini 3 Pro, GPT-5.2) with appropriate caveats ("motivated aspects of the coordinator architecture but is not validated here"). The open-source data availability statement with a specific repository tag is commendable. The use of anonymous authorship ("Project Dyson Research Team") with a note about final publication is unusual but not inherently problematic if resolved before publication.

One concern: the reference to the AI methodology paper [44] is self-referential and appears to be a non-peer-reviewed web publication. The AI model version numbers (Claude 4.6, GPT-5.2) do not correspond to any publicly known releases as of my knowledge, raising questions about the timeline or accuracy of this disclosure.

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is appropriate for IEEE TAES in its focus on space systems coordination, though it sits at the boundary between systems engineering and communication theory. The reference list (52 items) is comprehensive, covering constellation operations, swarm robotics, distributed systems, queueing theory, and space standards. Key works are cited: Kleinrock for queueing, Demers for gossip, Ongaro for Raft, Kaul/Yates for AoI, and relevant CCSDS standards.

**Gaps in referencing:** (1) The paper does not cite recent work on distributed satellite autonomy beyond NASA DSA [50], such as the ESA OPS-SAT experiments or the Starlink autonomous collision avoidance system described in IAC papers. (2) The GE channel model for ISLs lacks domain-specific references; the cited parameters ($p_G$, $p_B$, $p_{GB}$, $p_{BG}$) are not grounded in measured ISL channel statistics. (3) The TDMA frame analysis would benefit from citing actual space-qualified S-band transceiver specifications beyond the general SMAD reference. (4) Several references are non-archival (Amazon Kuiper overview, DARPA program pages, DoD fact sheets), which is acceptable for context but weakens the empirical grounding. (5) The 2%/year failure rate is attributed to Castet and Saleh [30], but that 2009 paper covers historical satellites, not modern small-satellite constellations; more recent reliability data (e.g., from Starlink operational experience) would be more appropriate.

---

## Major Issues

1. **Validation gap is too large for the claims made.** The paper's core contribution—design equations for sizing hierarchical coordination—cannot be meaningfully evaluated without at least one level of physical-layer validation. The DES verification confirms arithmetic correctness but not model adequacy. The $\gamma$ parameter absorbs too many unmodeled phenomena (MAC contention, FEC, ranging, antenna scheduling, Earth occlusion) to provide confidence that the message-layer results translate to realized performance. **Required:** Either (a) perform packet-level simulation (NS-3/OMNeT++) for at least one representative configuration to bound the message-to-packet gap, or (b) substantially downgrade the claims to "message-layer sizing estimates pending physical-layer validation" throughout (not just in the abstract and Section V-A).

2. **The comparison framework is structurally unfair.** The centralized baseline lacks communication-layer modeling; the global-state mesh is an intentional worst case; the sectorized mesh is handicapped by the 3.2% coverage cap. Only the hierarchical architecture receives full bidirectional traffic accounting. **Required:** Either (a) model the sectorized mesh with sufficient fanout to achieve comparable *functional utility* (e.g., full sector awareness) and compare overhead at equal awareness levels, or (b) restrict claims to "hierarchical overhead is X% at the message layer" without comparative advantage claims.

3. **The stress-case command model needs justification.** The 512 B per-node-per-cycle command rate drives the headline $\eta \approx 46\%$ but is not grounded in operational data. No existing constellation issues individual orbit-adjustment commands to every satellite every 10 seconds. **Required:** Provide operational justification for the stress-case rate, or reframe the stress case as a theoretical upper bound with the nominal/event-driven profiles as the primary results.

4. **GE channel parameters are not grounded in ISL measurements.** The GE model parameters ($p_G = 0.01$, $p_B = 0.90$, $p_{GB} = 0.05$, $p_{BG} = 0.50$) are stated without reference to measured S-band ISL channel statistics. The coherence-time discussion (Section IV-C) is qualitative. **Required:** Either cite measured channel statistics for LEO ISLs at S-band to justify the parameter choices, or present the GE analysis purely as a parametric design tool (which the sensitivity sweep in Fig. 5(b) already supports) without implying the default parameters are representative.

---

## Minor Issues

1. **Abstract (lines 1–20):** The abstract attempts to convey every result and caveat, making it nearly impenetrable. The parenthetical qualifications ("($\gamma = 0.85$ conservatively, derived from TDMA frame analysis)") belong in the body, not the abstract. Recommend cutting to ~150 words focusing on the three key results.

2. **Eq. 2 ($W_q$):** The M/D/1 waiting time formula $W_q = \rho / [2\mu_s(1-\rho)]$ is correct but should be cited as the Pollaczek-Khinchine result for deterministic service, not just attributed to Kleinrock generally.

3. **Table I:** The "Representative System" column (e.g., "Hyperscale data center" for $c = 1000$) is speculative and not grounded in actual ground-station architectures. Consider removing or replacing with actual system references.

4. **Section III-B-2, Eq. 4:** $M_{\text{total}}$ counts messages but the overhead metric $\eta$ is defined in bytes. The connection between message count and byte-level overhead should be made explicit.

5. **Table V (Simulation Parameters):** The collision avoidance rate ($10^{-4}$/node/s) footnote says "screening events, not maneuver-triggering," but the message is labeled "Collision avoidance msg" (128 B, "Priority alert"). Clarify whether this represents a screening notification or an evasive maneuver command.

6. **Section IV-A, half-duplex analysis:** The broadcast command model (171 ms for 512 B at 24 kbps) assumes all members can receive simultaneously. In practice, directional antennas may require sequential transmissions. This should be noted as a limitation.

7. **Table VIII (AoI results):** The footnote describes the tail-statistic methodology (per-run P99 aggregation), which is methodologically sound. However, the 95% bootstrap CI of [438, 444] s for a theoretical value of 440 s, with only 30 replications, suggests the variance is dominated by discretization ($T_c = 10$ s steps), not sampling uncertainty. This should be noted.

8. **Section IV-D (Joint Interaction):** The identical "No Loss" and "GE Only" columns in Table IX are presented as a key finding, but this is a direct consequence of the model architecture (lost messages removed before reaching the queue). This is a property of the *simulation design*, not a discovered result. Reframe accordingly.

9. **Section V-C (Limitations):** "A 10% coordinator failure inflates neighboring clusters by ~10%, absorbable at $C_{\text{coord}} \geq 28$ kbps"—this assumes uniform redistribution, but in practice, geographic proximity would cause non-uniform loading. The 28 kbps figure should be derived, not asserted.

10. **References:** [44] (dyson_multimodel) is a self-citation to a non-peer-reviewed web publication. Consider removing or replacing with a methodological note.

11. **Eq. 6 ($\gamma = 0.949$):** The guard time calculation uses 500 km cluster diameter, but this value is not derived from the orbital mechanics of the assumed constellation. At 550 km altitude with $k_c = 100$ co-orbital nodes, the along-track spacing would be ~400 km (circumference / nodes-per-plane), but cross-track extent depends on plane separation. Justify the 500 km assumption.

12. **Section III-E:** "Effective range $\eta_{\text{eff}} \in [51\%, 66\%]$ for $\gamma \in [0.7, 0.9]$"—this range is presented without noting that $\gamma = 0.7$ is below the derived TDMA efficiency of 0.85–0.949, implying a non-TDMA MAC. Clarify which MAC protocols correspond to which $\gamma$ values.

13. **Acknowledgment section:** "Total MC wall-clock time: ~90 min on commodity hardware" is useful but belongs in the methodology or data availability section, not the acknowledgment.

---

## Overall Recommendation

**Major Revision**

This paper tackles a worthwhile problem—providing sizing equations for hierarchical coordination in large space swarms—and demonstrates commendable transparency about its assumptions and limitations. The analytical framework is internally consistent, the design equations are correctly derived, and the open-source tooling is a positive contribution. However, the paper has three fundamental weaknesses that prevent acceptance in its current form: (1) the validation gap between message-layer analysis and physical-layer reality is too large to support the design-equation claims without at least one intermediate validation step; (2) the topology comparison is structurally asymmetric, undermining the comparative conclusions; and (3) the stress-case command model that drives the headline results lacks operational grounding. A major revision addressing these issues—particularly adding packet-level simulation for even one configuration, equalizing the comparison framework, and grounding the workload model in operational data—would substantially strengthen the contribution.

---

## Constructive Suggestions

1. **Add a single packet-level validation point.** Run one NS-3 or OMNeT++ simulation at $N = 1{,}000$, $k_c = 100$ with a realistic S-band TDMA PHY to quantify the message-to-packet overhead gap. Even a single data point showing that the message-layer $\eta$ is within, say, 20% of the packet-layer value would dramatically strengthen the paper's credibility. This need not be exhaustive—one well-characterized configuration suffices.

2. **Restructure around the nominal workload.** Make the nominal/event-driven profiles ($\eta \approx 5$–$6\%$) the primary results and the stress case the sensitivity bound. This better reflects operational reality (no constellation commands every satellite every 10 s) and highlights the more interesting finding: architecture-specific overhead is only ~5%, meaning the hierarchical structure is remarkably lightweight.

3. **Equalize the sectorized mesh comparison.** Model a sectorized mesh variant that achieves comparable *functional awareness* to the hierarchical architecture (e.g., full sector awareness via a sector coordinator that aggregates all $k_s$ members, analogous to the cluster coordinator). This would enable a fair overhead-per-unit-of-awareness comparison and likely show that the hierarchical advantage comes from the *aggregation structure*, not the topology per se.

4. **Ground the GE parameters in measured data or reframe as purely parametric.** The sensitivity sweep (Fig. 5(b)) is already the most useful part of the GE analysis. Lean into this: present the design curves as a parametric tool for arbitrary channel conditions, and either cite measured S-band ISL statistics to anchor the default parameters or remove the implication that they are representative.

5. **Shorten the paper by 30%.** The current length (~12,000 words plus tables) exceeds IEEE TAES norms. The TDMA synchronization fallback, load-shedding rules, and degraded-mode analysis (while individually interesting) could be condensed into a single paragraph each or moved to supplementary material. The abstract should be cut to ~150 words. This would improve readability without sacrificing technical content.