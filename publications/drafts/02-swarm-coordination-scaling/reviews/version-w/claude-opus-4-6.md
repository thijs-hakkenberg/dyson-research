---
paper: "02-swarm-coordination-scaling"
version: "w"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-24"
recommendation: "Major Revision"
---

# Peer Review: "Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study"

## 1. Significance & Novelty
**Rating: 3 (Adequate)**

The paper addresses a legitimate gap in the literature: systematic comparison of coordination architectures for autonomous spacecraft swarms at the 10³–10⁵ scale with explicit byte-level traffic accounting. The motivation is timely given Starlink's expansion trajectory and planned mega-constellations. The framing around a "design envelope" (5–46% overhead) is useful for system architects, and the application of AoI to hierarchical space swarm coordination is a reasonable contribution.

However, the novelty is substantially undermined by the authors' own analysis. The O(1) overhead scaling—presented as a central result—is acknowledged in Section IV-D as "a direct mathematical consequence of the hierarchical message structure—not a surprising emergent property." The DES-to-analytical agreement of <0.1% (Table VII, Section IV-D-2) confirms that the simulation is essentially computing the same closed-form expression as Eq. (15), raising the question of what the DES adds beyond implementation verification. The authors attempt to address this by highlighting three DES-specific contributions (TDMA vs. random-phase scheduling, Gilbert-Elliott retransmission ineffectiveness, AoI quantification), but these are individually modest findings. The TDMA result (50 kbps vs. 24 kbps threshold) is the strongest DES-unique contribution, though it follows straightforwardly from the elimination of burstiness in deterministic scheduling. The Gilbert-Elliott finding (intra-cycle retry is ineffective during burst losses) is well-known in the communications literature and not specific to space swarms.

The sectorized mesh comparator (1.4–1.5× overhead) is a useful addition but architecturally converges toward the hierarchical model (as the authors note in Section V-C), limiting its value as an independent comparator. The paper would benefit from a clearer articulation of what is genuinely new versus what is a careful parameterization of known results applied to a new domain.

## 2. Methodological Soundness
**Rating: 3 (Adequate)**

The cycle-aggregated DES framework is clearly described and the abstraction level is well-justified for the research questions posed. The traffic accounting (Table IV) is meticulous, and the analytical cross-check (Section IV-D-2, Eq. 15) provides strong internal validation. The Monte Carlo framework (30 replications, seeds 42–71) is appropriate, and the authors are commendably transparent about the near-deterministic nature of the model (SD < 0.001%).

However, several methodological concerns arise:

**The simulation is too close to a spreadsheet calculation.** The <0.1% DES-to-analytical agreement across all fleet sizes, combined with SD < 0.001% across MC replications, indicates that the stochastic elements (2%/year node failures, collision avoidance events at 10⁻⁴/node/s) have negligible impact on the primary metrics. The authors acknowledge this ("the MC framework serves primarily to confirm this low-variance property") but do not adequately grapple with the implication: the DES adds very little information beyond the closed-form analysis for the overhead metric. The within-cycle timing model (Section III-H) is the primary mechanism producing non-trivial DES results, but it is exercised only for the coordinator bandwidth analysis (Section IV-G, IV-I), not for the headline overhead results.

**The workload model is a free parameter, not derived from physics.** The stress-case assumption (one unique 512-byte command per cluster member per cycle) is acknowledged as "a conservative upper bound unlikely to be sustained indefinitely," but it drives the headline 46% figure. The nominal profile (5%) and event-driven profile (6%) are far more realistic but receive less attention. The exception probability p_exc is similarly a free parameter "not derived from spacecraft dynamics" (Section IV-E). This means the design envelope is parameterized by assumptions rather than constrained by physics—useful for exploration but limited for engineering application.

**The coordinator bandwidth pooling assumption is critical but under-examined.** The paper acknowledges that coordinator ingest requires ~20.5 kbps while each node has only 1 kbps (Section III-F), resolved by assuming TDMA bandwidth pooling. This is a significant hardware assumption (every node must be capable of coordinator-rate reception) that is treated as a design choice rather than a constraint. The sensitivity analysis (Section IV-G) is welcome but does not address the fleet-wide cost of this over-provisioning.

**Validation against external references is limited.** The M/D/1 validation (Section III-A, "within 2%") and gossip convergence validation (against analytical bounds for N ≤ 1,000) are internal consistency checks, not independent validation. No comparison against an established network simulator (NS-3, OMNeT++) or real operational data is provided. The authors identify packet-level single-cluster validation as future work (Section V-D), which is appropriate, but its absence limits confidence in the message-layer abstraction.

## 3. Validity & Logic
**Rating: 3 (Adequate)**

The logical structure is generally sound, and the authors are notably transparent about limitations. The baseline interpretation note (Section I-C) and the extensive footnotes on Table III are commendable efforts to prevent misinterpretation. The distinction between delivered and offered overhead (Table IX) is important and well-handled.

Several logical concerns merit attention:

**The comparison framework is asymmetric.** The hierarchical architecture is modeled with full DES fidelity including within-cycle timing, coordinator queueing, and bandwidth constraints. The centralized baseline is a single-server analytical bound (acknowledged as unrealistic). The global-state mesh is an analytical upper bound. The sectorized mesh is simulated but with a capped fanout that makes it architecturally similar to the hierarchical model. This asymmetry means the paper demonstrates that a well-parameterized hierarchical architecture outperforms deliberately pessimistic alternatives—a weaker claim than it initially appears. The authors are transparent about this (Section I-C), but the abstract and conclusion could more clearly reflect this framing.

**The AoI analysis (Section IV-F) conflates two distinct phenomena.** Exception-based telemetry degrades AoI because nodes report less frequently (a design choice), while link losses degrade AoI because reports fail to arrive (an environmental constraint). Table VI presents both in the same framework, but the engineering implications are quite different: exception telemetry AoI can be improved by lowering the threshold (at bandwidth cost), while link-loss AoI requires retransmission or redundancy. The discussion could better separate these mechanisms.

**The claim that "intra-cycle retransmission is ineffective during correlated outage bursts" (Section IV-K) is correct but unsurprising.** If the bad-state loss probability is 0.90, then two retries recover only 1 − 0.9³ = 27.1% of burst-lost messages—this is arithmetic, not a simulation finding. The recommendation for store-and-forward recovery is sensible but is standard practice in DTN literature (which the authors cite). The DES contribution here is confirming the known result in the specific parameterization, not discovering it.

**Table V (cluster size optimization) shows overhead varying by only ±0.1% across k_c = 50–500.** The authors correctly note that the cluster-size trade-off is driven by latency, not overhead. However, the latency values show only two discrete levels (508/675 ms for N = 10⁵), suggesting the latency model may be too coarse to capture the actual optimization surface. The "U-shape" mentioned in Section III-B-2 is not visible in the data.

## 4. Clarity & Structure
**Rating: 4 (Good)**

The paper is well-organized and generally well-written, with a logical progression from framework description through results to discussion. The extensive use of tables for parameter documentation (Tables I–IV) supports reproducibility. The distinction between message-layer and physical-layer results is consistently maintained throughout.

Several structural issues reduce clarity:

**The paper is excessively long for its content.** At approximately 12,000 words of body text plus extensive tables and figures, the manuscript substantially exceeds typical IEEE TAES length guidelines. Much of the length comes from defensive qualifications and repeated caveats (e.g., the centralized baseline being a worst case is stated at least six times across Sections I-C, III-B-1, IV-A, and the figure captions). While transparency is valued, this repetition could be consolidated.

**The abstract attempts to convey too many results.** The abstract mentions six distinct findings (design envelope, TDMA scheduling, Gilbert-Elliott, AoI, sectorized mesh, DES framework), making it difficult to identify the primary contribution. A more focused abstract highlighting the design envelope and the TDMA scheduling result would be more effective.

**Figure quality cannot be assessed** since the manuscript references PDF figures that are not included. The captions are detailed and informative, which partially compensates. The description of Fig. 1 (architecture diagram) suggests it would be helpful for understanding the four-level hierarchy.

**Section III-F (Communication Overhead Definition) is disproportionately long** (~1.5 pages) for what is essentially a metric definition. The MAC protocol implications, coordinator bandwidth pooling, and hardware implications could be moved to a dedicated subsection or appendix.

## 5. Ethical Compliance
**Rating: 4 (Good)**

The paper includes an appropriate acknowledgment of AI-assisted ideation (Claude 4.6, Gemini 3 Pro, GPT-5.2) in the Acknowledgment section, with a clear statement that the AI-generated concepts are "not validated in the current study." The data availability statement with a GitHub repository link (pending commit hash) supports reproducibility. The author attribution note ("Individual author names and affiliations will be provided for final publication per IEEE policy") is unusual but acceptable for initial submission.

One concern: the AI model versions cited (Claude 4.6, GPT-5.2) do not correspond to any publicly released models as of mid-2025, suggesting either future/unreleased tools or incorrect version numbers. This should be clarified. The companion methodology paper [44] is cited but appears to be a self-published working paper rather than a peer-reviewed publication; its status should be clarified.

## 6. Scope & Referencing
**Rating: 3 (Adequate)**

The paper is appropriate for IEEE TAES in scope, addressing autonomous spacecraft coordination at mega-constellation scale. The reference list (50 citations) covers the relevant literature in constellation management, swarm robotics, distributed systems, and AoI theory. Key foundational works are cited (Lynch, Kleinrock, Lamport, Demers et al., Kaul et al., Yates et al.).

Several referencing gaps exist:

**Missing recent work on autonomous satellite coordination.** The paper does not cite recent work on distributed space traffic management (e.g., Hobbs et al., 2020, "Space traffic management standards"; Bonnal et al., 2020, on active debris removal coordination) or on-orbit servicing coordination architectures. The DARPA Blackjack results (now partially published) should be discussed more substantively than a URL reference.

**The DTN/BPv7 literature is cited but not engaged.** Given that store-and-forward recovery is recommended as the preferred strategy for correlated losses (Section IV-K), a more substantive discussion of how BPv7 custody transfer mechanisms would interact with the hierarchical coordination model is warranted.

**Several references are non-archival** (SpaceX website, Amazon website, DARPA program pages, DoD fact sheets). While some non-archival references are unavoidable for current operational systems, the paper relies on them for key claims about operational scale (Starlink ~7,000 satellites) and planned expansions (42,000 satellites). Where possible, these should be supplemented with archival sources (FCC filings, ITU filings, peer-reviewed analyses).

**The AoI literature engagement is appropriate** but could note the gap between the simple geometric-distribution AoI model used here and the more sophisticated multi-source scheduling-aware AoI results in the literature (e.g., Kadota et al., 2018, on scheduling for AoI minimization).

---

## Major Issues

1. **The DES adds minimal information beyond closed-form analysis for the primary overhead metric.** The <0.1% DES-to-analytical agreement and SD < 0.001% across MC replications indicate that the headline result (η ≈ 46%) is an analytical calculation, not a simulation finding. The paper should either (a) reframe the contribution around the genuinely DES-unique results (TDMA scheduling threshold, coordinator drop rates under finite buffers, AoI distributions) and de-emphasize the overhead scaling verification, or (b) introduce physical-layer effects (MAC contention, realistic orbital geometry, correlated failures) that would produce DES results that diverge from closed-form predictions. As currently structured, the paper claims simulation contributions that are largely analytical.

2. **The comparison framework is fundamentally asymmetric.** Comparing a well-parameterized hierarchical DES against intentionally pessimistic analytical bounds (single-server centralized, global-state mesh) does not constitute a meaningful architectural comparison. The sectorized mesh helps but converges architecturally toward the hierarchical model. The paper needs either (a) a fair comparison against a realistically parameterized centralized system (e.g., M/D/100 with realistic ground-to-space latency) or (b) a clearer reframing that the contribution is characterization of the hierarchical architecture's design space, not a comparative study.

3. **Key parameters are free variables unconnected to physics.** The exception probability p_exc, the collision avoidance event rate (10⁻⁴/node/s), the stress-case command rate (one per node per cycle), and the coordinator duty cycle are all free parameters. The design envelope (5–46%) is therefore a parameterization of assumptions, not a physics-constrained result. The paper should either derive at least one key parameter from a simplified orbital dynamics model (e.g., computing p_exc from two-body propagation uncertainty growth) or more clearly frame the results as a parametric trade space requiring mission-specific instantiation.

4. **The cluster-size "optimization" (Section IV-B) shows no meaningful optimization.** Table V shows overhead varying by ±0.1% and latency taking only two discrete values across k_c = 50–500. The claimed "U-shape" is not visible in the data. Either the model is too coarse to capture the optimization surface, or the optimization is trivial (any k_c in [50, 500] works). This section should be revised to accurately reflect what the data shows.

## Minor Issues

1. **Section III-A, paragraph 3**: "Events at both resolutions are managed through a single priority queue ordered by simulated time; one-second resolution applies only to collision avoidance events"—this implies a hybrid resolution model but the implementation details are unclear. How are 1-second and 10-second events interleaved in the priority queue?

2. **Eq. (4)**: The hierarchical message count $M_{\text{total}} = N + N/k_c + N/(k_c \cdot k_r)$ counts only uplink messages. The text notes this but the equation should be labeled accordingly or expanded to include bidirectional traffic.

3. **Table II (M/D/c sensitivity)**: The "Representative System" column labels are misleading. A "single ground station thread" processing 1,000 msg/s is not a realistic single-thread parameterization for modern hardware; a single modern CPU core can process orders of magnitude more messages per second. The μ_s = 1,000 msg/s assumption should be better justified or acknowledged as artificially low.

4. **Section III-B-3**: The convergence round formula $R_{\text{conv}} = \max(\lceil\log_2 N\rceil, \lceil N/(bf)\rceil)$ conflates two different convergence requirements (epidemic spread vs. throughput). The max operation is correct but deserves more explanation—specifically, that the batch-throughput term dominates at large N.

5. **Table VI (AoI results)**: The "Max AoI" column shows values of 780s and 355s for p_exc = 0.10 and 0.30 respectively. These maxima depend on simulation duration and are not statistically meaningful without confidence bounds. Consider removing or replacing with P99.9.

6. **Section IV-H (Power Budget)**: Eq. (16) computes average power overhead but the text then discusses peak thermal design requirements. The thermal design point (20W) is the relevant engineering parameter; the average (0.15W) is misleading for hardware sizing.

7. **Typographical**: Section III-B-2 references "Fig. 1" but the figure is labeled "fig-architecture-diagram.pdf"—ensure figure numbering is consistent in the compiled document.

8. **The Acknowledgment section mentions "Claude 4.6" and "GPT-5.2"**—these version numbers do not correspond to publicly known model releases. Verify and correct.

9. **Table I footnote b**: "Labeled 'screening alert rate' to distinguish from physical maneuver rate"—this distinction is important and should appear in the main text, not just a footnote.

10. **Section III-G (Performance Metric Definitions)**: The handoff description includes both election traffic (~12.8 KB) and state transfer (10–50 MB). The election traffic is said to be "included in the 'Heartbeat/ACK' category"—this is a categorization choice that should be justified (election messages are functionally distinct from heartbeats).

## Overall Recommendation

**Major Revision**

The paper addresses a relevant problem and demonstrates careful engineering analysis with commendable transparency about assumptions and limitations. However, the central methodological concern—that the DES produces results nearly identical to closed-form analysis for the primary metric—undermines the claimed simulation contribution. The asymmetric comparison framework and free-parameter workload model further weaken the contribution. A major revision should (1) reframe the contribution around the genuinely DES-unique results (scheduling-dependent coordinator capacity, AoI distributions, correlated loss behavior) rather than the overhead scaling verification; (2) either introduce physical-layer effects that produce non-trivial simulation dynamics or clearly position the work as a parametric design-space characterization; (3) derive at least one key parameter (e.g., p_exc or collision avoidance rate) from simplified orbital dynamics; and (4) substantially reduce the manuscript length by consolidating repeated caveats and moving detailed metric definitions to supplementary material.

## Constructive Suggestions

1. **Elevate the TDMA scheduling result to the primary contribution.** The 50 kbps → 24 kbps coordinator capacity reduction is the strongest DES-unique finding. Consider restructuring the paper around coordinator capacity design as the central question, with overhead scaling as supporting context. This would better justify the simulation approach and produce a more focused, shorter paper.

2. **Add a single-cluster packet-level validation.** Even a simplified NS-3 or OMNeT++ model of one 100-node cluster with realistic optical ISL parameters would substantially strengthen the message-layer abstraction claim. This need not cover the full parameter space—a single validation point at k_c = 100 with TDMA scheduling would suffice.

3. **Derive p_exc from a simplified orbital prediction model.** A two-body propagator with J2 perturbation could estimate position uncertainty growth over T_c = 10s, yielding a physics-based exception threshold. This would transform p_exc from a free parameter to a derived quantity, connecting the communication model to orbital dynamics and substantially strengthening the engineering applicability.

4. **Reduce manuscript length by 30–40%.** Consolidate the baseline interpretation caveats into a single subsection (currently repeated in Sections I-C, III-B-1, IV-A, and multiple figure captions). Move the detailed traffic accounting derivation (Section IV-D-2) to an appendix. Shorten Section III-F (overhead definition) by separating the metric definition from the MAC protocol discussion.

5. **Add a time-varying workload scenario.** A simulation that transitions between nominal (Profile N) and stress-case (Profile S) during a simulated conjunction campaign would demonstrate the DES's ability to capture transient dynamics that closed-form analysis cannot, while also being more operationally realistic than sustained stress-case operation.