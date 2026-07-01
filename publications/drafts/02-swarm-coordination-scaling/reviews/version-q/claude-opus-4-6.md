---
paper: "02-swarm-coordination-scaling"
version: "q"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-24"
recommendation: "Major Revision"
---

# Peer Review: "Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study"

**Manuscript Version:** Q
**Venue:** IEEE Transactions on Aerospace and Electronic Systems

---

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a genuinely important problem: how to coordinate autonomous spacecraft swarms at scales of 10³–10⁵ nodes, a regime that is becoming operationally relevant as mega-constellations expand. The framing around the gap between swarm robotics literature (tens to hundreds of agents) and operational constellation management (up to ~10⁴ nodes) is well-articulated, and the claim that "no prior work has systematically compared coordination architectures for autonomous spacecraft swarms across the 10³–10⁵ range using quantitative simulation with explicit byte-level traffic accounting" (Section I-A) is plausible.

However, the novelty is substantially undermined by the nature of the central result. The authors themselves acknowledge repeatedly (Section IV-D, and throughout) that the O(1) overhead scaling of the hierarchical architecture is "a direct mathematical consequence of the hierarchical message structure—not a surprising emergent property." The DES then confirms this analytical prediction to within 0.05% at all ten fleet sizes (Table V). This raises a fundamental question: what does the simulation add beyond validating an arithmetic identity? The authors argue three DES-specific contributions—protocol coefficient quantification, queue stability confirmation, and analytical cross-check—but the first is a single number derivable from Table III, the second is unsurprising given the low utilization levels (ρ_c = 0.05), and the third is explicitly a code-correctness check. The coordinator bandwidth stress test (Section IV-G) and retransmission analysis (Section IV-F) are more genuinely simulation-dependent contributions, but they are secondary to the paper's framing.

The sectorized mesh comparator (Section III-B-4) is a welcome addition that fills the gap between the intentional upper/lower bounds, but the capped-fanout variant (≤10 heartbeat neighbors) is itself a design choice that strongly determines the 2.2× overhead ratio. The paper would benefit from a more thorough exploration of the sectorized mesh parameter space to understand how robust this ratio is.

## 2. Methodological Soundness

**Rating: 2 (Needs Improvement)**

The simulation framework is described with commendable detail, and the traffic accounting (Table III) is precise and reproducible. The Monte Carlo framework (30 replications, seeds 42–71) is appropriate, and the authors are admirably transparent about the near-deterministic nature of the results (SD < 0.001%). The validation against the M/D/1 Pollaczek-Khinchine formula (Section III-A) and gossip convergence bounds provides useful sanity checks.

However, several methodological concerns are significant:

**The simulation is essentially a traffic calculator, not a DES.** Despite being labeled a "discrete event simulation," the cycle-aggregated design processes messages at 10-second granularity with deterministic message generation (every node, every cycle). The only stochastic elements are node failures (2%/year, affecting negligible fractions per cycle) and message phase offsets. The authors acknowledge this ("the MC framework serves primarily to confirm this low-variance property rather than to explore substantial stochastic uncertainty," Section III-D), but this admission undermines the methodological framing. A true DES would model event-driven dynamics—contention, queueing transients, burst arrivals from correlated events—that could reveal emergent scaling behaviors. The cycle-aggregated approach is computationally efficient but methodologically limited: it cannot discover phenomena it does not model.

**The abstraction level creates a circularity problem the authors partially acknowledge (Section V-E).** The DES abstracts away MAC scheduling, link acquisition, half-duplex constraints, correlated failures, and priority queueing—precisely the phenomena most likely to introduce scale-dependent nonlinearities. The paper then concludes that no scale-dependent nonlinearities exist. The MAC efficiency factor γ ∈ [0.7, 0.9] is applied post-hoc as a multiplicative correction, but this assumes MAC overhead is scale-independent, which is not established. At 10⁵ nodes with rotating coordinators, the TDMA slot allocation problem itself becomes non-trivial and potentially scale-dependent.

**The coordinator bandwidth model has internal inconsistencies.** The paper assumes each node has a 1 kbps coordination budget, but coordinators require 20–50 kbps ingest capacity. The resolution—"pooling the cluster's coordination bandwidth"—is presented as a TDMA slot aggregation, but this requires all nodes to have transceivers capable of the coordinator rate (≥50 kbps). This means the actual per-node hardware capability is 50 kbps, not 1 kbps, and the "1 kbps per node" framing is misleading. The paper acknowledges this ("the radio subsystem is sized for the coordinator role on every node"), but the overhead metric η is still normalized against 1 kbps, which understates the true resource commitment.

**The collision avoidance event rate parameterization is weakly justified.** The 10⁻⁴/node/s rate is described as representing screening events at a 1000:1 ratio to actual maneuvers, but no reference supports this specific ratio for the dense orbital shells contemplated at 10⁵ nodes. In dense shells, the screening rate could scale superlinearly with N due to increased conjunction frequency, which would break the O(N) message scaling assumption.

## 3. Validity & Logic

**Rating: 3 (Adequate)**

The paper's conclusions are internally consistent with its model assumptions, and the authors are commendably transparent about limitations. The analytical cross-check (Section IV-D-2) confirms implementation correctness. The coordinator bandwidth stress test (Table VI) provides genuinely useful engineering data, and the retransmission analysis (Table VII) meaningfully extends the results to imperfect links.

The interpretation is generally balanced, with appropriate caveats. The authors explicitly state that the centralized baseline is a worst-case bound (Section I-C), that the global-state mesh is an intentional upper bound, and that the O(1) scaling is analytically guaranteed rather than an emergent finding. The identification of coordination quality metrics as "the most important direction for future work" (Section V-D, item 1) is an honest and critical acknowledgment.

However, several logical issues deserve attention. First, the paper claims the hierarchical architecture "eliminates" propagation latency and spectrum scarcity constraints (end of Section IV-A), but this is overstated. Hierarchical aggregation reduces ground-link traffic but does not eliminate it; the ground station still receives N/(k_c · k_r) region summaries per cycle, and the inter-cluster optical ISL links still require spectrum allocation. Second, the exception-based telemetry validation (Section IV-E) confirms that the Bernoulli filtering mechanism works as expected by the law of large numbers—this is mathematically trivial for N × T/T_c >> 1 independent trials and does not constitute a meaningful simulation result. The authors partially acknowledge this but still present it as a "validation." Third, the latency budget decomposition (Section IV-B) identifies regional coordinator queueing (~500 ms) as the dominant component, but this is an artifact of the burst-arrival model (all cluster summaries arrive near the end of each coordination cycle). In a real system with staggered cluster reporting phases, this burst would be smoothed, and the latency would be substantially lower. The paper does not explore this obvious mitigation.

## 4. Clarity & Structure

**Rating: 4 (Good)**

The paper is well-organized and clearly written, with a logical progression from problem statement through methodology, results, and discussion. The extensive use of tables (12 tables) and figures (9 figures) supports the narrative effectively. Table II (Simulation Abstraction Scope) is particularly valuable for setting reader expectations about what the DES does and does not model. The traffic accounting table (Table III) and metric definitions (Section III-G) provide the precision needed for reproducibility.

The abstract is accurate and comprehensive, though at 250+ words it is dense. The distinction between message-layer overhead (η ≈ 21%) and effective MAC-layer overhead (η_eff ∈ [18%, 27%]) is maintained consistently throughout, which is important for avoiding misinterpretation.

Several structural issues could be improved. The paper is very long for a journal article (~12,000 words excluding references), with substantial repetition. The O(1) scaling property is explained at least five times (abstract, Section I contributions, Section IV-D preamble, Section IV-D results, and conclusion). The baseline interpretation caveat appears three times (Section I-C, Fig. 2 caption, Section V-E). While some repetition aids readability, this level is excessive and could be reduced by 15–20% without loss of content. The sectorized mesh model is split between Sections III-B-4 and V-C, making it difficult to follow as a coherent contribution. Consolidating the model description and results would improve readability.

The notation is generally consistent, though the use of both η and η_eff for different overhead measures, plus η_total for the combined metric, creates potential confusion. A notation table would help.

## 5. Ethical Compliance

**Rating: 4 (Good)**

The paper includes an appropriate acknowledgment of AI-assisted ideation (Claude 4.6, Gemini 3 Pro, GPT-5.2) in the Acknowledgment section, with a clear statement that the AI-generated concepts "are not validated in the current study." This is transparent and appropriate. The reference to a companion methodology paper [45] provides additional context.

The anonymous author block ("Project Dyson Research Team") with a note that "Individual author names and affiliations will be provided for final publication per IEEE policy" is acceptable for review but must be resolved before publication. The data availability statement with a GitHub repository link (pending commit hash) is commendable.

One concern: the paper references future model versions (Claude 4.6, GPT-5.2) that do not exist as of the review date, suggesting either the paper is set in a future timeframe or these are fictional model identifiers. This should be clarified—if the AI tools are real, their actual version numbers should be used; if fictional, this should be stated.

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is appropriate for IEEE TAES in its focus on autonomous spacecraft coordination, though the contribution is more in the distributed systems/communication architecture domain than traditional aerospace engineering. The reference list (50 citations) is adequate in breadth, covering constellation operations, swarm robotics, distributed algorithms, queueing theory, and space networking standards.

However, several important gaps exist. The paper does not cite recent work on satellite constellation coordination using reinforcement learning or machine learning approaches (e.g., work by Chen et al. on RL-based constellation management, or Hu et al. on distributed satellite task allocation). The DTN/BPv7 literature is cited but not engaged with substantively—given that store-and-forward networking is listed as "abstracted" in Table II, a discussion of how DTN protocols would interact with the hierarchical coordination model would strengthen the paper. The mean-field game theory references (Lasry & Lions, Huang et al.) are cited in the related work but never connected to the methodology; if MFG is relevant, it should be discussed in the context of the hierarchical model's assumptions.

Several references are non-archival (SpaceX website, Amazon website, DARPA program pages, DoD fact sheets), which is unavoidable for operational systems but should be minimized. The NRL reference [22] is described as a "magazine article, non-peer-reviewed," which is unusually candid but raises the question of whether it should be cited at all.

---

## Major Issues

1. **The central result is analytically trivial and the DES adds minimal value beyond it.** The O(1) overhead scaling is a mathematical identity (O(N)/O(N) = O(1)), and the protocol coefficient (η ≈ 21%) is derivable from the traffic accounting table without simulation. The DES confirms this to within 0.05%, which validates the implementation but does not constitute a scientific finding. The paper needs to either (a) reframe the contribution around the genuinely simulation-dependent results (coordinator bandwidth thresholds, retransmission robustness, sectorized mesh comparison) rather than the overhead scaling, or (b) introduce physical-layer effects (MAC contention, correlated outages, priority queueing) that could produce emergent scale-dependent behavior not predictable from the analytical model.

2. **Absence of any coordination quality metric.** The paper measures the *cost* of coordination but not its *effectiveness*. Without at least one quality metric (state estimation error, conjunction detection probability, coordination completeness), it is impossible to assess whether the hierarchical architecture actually *works*—only that it consumes 21% of bandwidth. The authors identify this as priority future work, but for a journal publication in TAES, some measure of coordination effectiveness should be included, even if simplified (e.g., age-of-information at the coordinator as a function of reporting rate and failure rate).

3. **The abstraction level creates an unfalsifiable claim.** By abstracting away MAC scheduling, link acquisition, correlated failures, and priority queueing, the DES cannot detect the scale-dependent effects most likely to perturb the O(1) scaling. The paper then claims no scale-dependent effects exist. This circularity is acknowledged in Section V-E but not resolved. At minimum, a TDMA scheduling model within T_c (with guard intervals and slot allocation) should be implemented to test whether intra-cycle contention introduces scale-dependent overhead.

4. **The 1 kbps per-node budget is inconsistent with the coordinator capacity requirement.** If every node must be capable of 50 kbps (to serve as coordinator), the effective per-node hardware commitment is 50 kbps, not 1 kbps. The overhead metric should be discussed in terms of both the traffic budget (1 kbps) and the hardware capability (50 kbps) to avoid misleading readers about the true resource cost.

## Minor Issues

1. **Section III-A:** "Individual bit-level or packet-level events are not instantiated" — this should be stated more prominently, perhaps in the abstract, since it fundamentally limits what the DES can discover.

2. **Table IV (Cluster Size):** The overhead values vary by only ±0.2% across k_c = 50–500, which is within the model-form uncertainty band. The table could be simplified or the near-invariance stated without the full table.

3. **Eq. (7):** The analytical cross-check equation includes collision avoidance at 0.128 B/node/cycle, which is negligible. This term could be dropped for clarity.

4. **Section IV-C (Duty Cycle):** The handoff success rates (95.0%–99.9%) are stated without derivation. How is handoff failure modeled? Is it a function of link availability during the handoff window, or a fixed probability?

5. **Fig. 3 caption:** References an analytical extrapolation to 10⁶ nodes but the figure is not provided (PDF figures are referenced but not included in the LaTeX source). All figure descriptions should be self-contained.

6. **Section III-F:** "Transport-layer overhead (headers, retransmissions) is not included; this understates true overhead by an estimated 10–20%." This is a significant omission that should be quantified more precisely or bounded analytically.

7. **Table I (M/D/c Sensitivity):** The "Hyperscale data center" row (c = 1000, N_max = 10⁷) is unrealistic for space operations and may mislead readers about the practical limits of centralized architectures.

8. **Section IV-F:** The Bernoulli link model assumes i.i.d. losses, but LEO link outages are dominated by Earth occlusion, which produces deterministic periodic outages correlated across nearby nodes. The sensitivity of the retransmission results to correlated outages should be at least discussed qualitatively.

9. **Notation:** Both $r$ (reporting rate) and $\rho$ (utilization) are used extensively; a consolidated notation table would aid readability.

10. **Section V-A:** "Starlink's expansion to 42,000 satellites enters the regime where centralized coordination incurs significant overhead" — this claim is not supported by the paper's own analysis, which shows that parallelized centralized systems (c ≥ 100) handle 10⁶ nodes without processing saturation.

---

## Overall Recommendation

**Major Revision**

This paper addresses an important problem with a well-documented simulation framework and commendable transparency about its limitations. However, the central contribution—confirming an analytically predictable O(1) scaling property via simulation—is insufficient for a top-tier journal publication. The paper needs to either introduce physical-layer modeling that could reveal emergent scaling behaviors, or include at least one coordination quality metric that demonstrates the hierarchical architecture actually achieves its coordination objectives. The coordinator bandwidth stress test and retransmission analysis are genuinely useful engineering contributions that should be elevated in the paper's framing. The sectorized mesh comparator adds value but needs more thorough parameterization. With substantial revision addressing the abstraction-level circularity and the absence of quality metrics, this could become a solid contribution to the TAES literature on mega-constellation coordination.

---

## Constructive Suggestions

1. **Add a minimal coordination quality metric.** Implement age-of-information (AoI) tracking at the coordinator: for each node, record the time since the coordinator last received a valid status update. Report mean and 99th-percentile AoI as a function of N, p_link, and p_exc. This is straightforward to add to the existing DES and would transform the paper from measuring coordination *cost* to measuring coordination *capability*. Even a simplified conjunction detection probability metric (probability that a conjunction geometry is detected within one coordination cycle) would substantially strengthen the contribution.

2. **Implement intra-cycle TDMA scheduling in the DES.** Rather than treating TDMA analytically (Section IV-I), model k_c time slots within each T_c with configurable guard intervals. This would (a) validate the analytical TDMA capacity predictions, (b) test whether slot allocation overhead introduces scale-dependent effects, and (c) resolve the coordinator bandwidth inconsistency by explicitly modeling the slot aggregation mechanism.

3. **Reframe the contribution around the simulation-dependent results.** The coordinator bandwidth thresholds (50 kbps unscheduled / 24 kbps TDMA), retransmission robustness envelope (p_link ≥ 0.5 with M_r = 2), and sectorized mesh comparison (2.2× overhead ratio) are the genuinely novel, simulation-dependent findings. Make these the primary contributions in the abstract and introduction, and demote the O(1) scaling confirmation to a validation result.

4. **Explore the sectorized mesh parameter space more thoroughly.** The 2.2× overhead ratio depends on the capped-fanout parameterization (≤10 heartbeat neighbors). Sweep the fanout cap from 1 to k_s and report the overhead ratio as a function of fanout, identifying the crossover point where sectorized mesh overhead equals hierarchical overhead (if one exists). This would provide a more complete picture of the architectural trade-off space.

5. **Replace at least one Bernoulli link model scenario with deterministic Earth-occlusion outages.** For a representative LEO shell (e.g., 550 km, 53° inclination), compute the fraction of each orbit during which ISL connectivity to the cluster coordinator is occluded by Earth. Use this as a deterministic periodic outage model and compare results against the i.i.d. Bernoulli model. This would address the most significant physical-layer gap at modest implementation cost.