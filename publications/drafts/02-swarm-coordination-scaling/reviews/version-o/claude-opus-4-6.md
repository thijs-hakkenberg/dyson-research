---
paper: "02-swarm-coordination-scaling"
version: "o"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-24"
recommendation: "Major Revision"
---

# Peer Review: "Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study"

**Manuscript ID:** Version O
**Venue:** IEEE Transactions on Aerospace and Electronic Systems

---

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a genuinely important problem: how to coordinate autonomous spacecraft at scales beyond current operational experience (>10⁴ nodes). The gap between swarm robotics literature (tens to hundreds of agents) and mega-constellation operations (~10⁴ nodes) is real, and the scaling regime of 10⁴–10⁶ is indeed underexplored. The motivation is timely given Starlink's expansion trajectory and emerging constellation programs.

However, the novelty of the core finding is limited. The authors themselves acknowledge repeatedly (Section IV-D, and throughout) that the O(1) overhead scaling of a hierarchical architecture with fixed fan-out is "a direct mathematical consequence of the hierarchical message structure—not a surprising emergent property." The DES essentially confirms an analytically predictable result: O(N) messages divided by O(N) bandwidth yields O(1) overhead. The quantification of the constant (η = 20.66%) is useful but is entirely determined by the input parameters (message sizes, reporting rates, channel capacity) through a straightforward calculation. The extremely low MC variance (SD < 0.001%) further underscores that the simulation is confirming arithmetic rather than discovering emergent behavior.

The paper's value proposition would be substantially stronger if it included the sectorized mesh comparator that is repeatedly identified as future work. Without it, the paper compares a reasonable architecture against two intentional strawmen (single-server centralized, global-state mesh), which limits the practical insight. The coordinator bandwidth stress test (Section IV-G) and the link availability analysis (Section IV-F) are the most novel and practically useful contributions, as they provide engineering design parameters not derivable from simple analytical models.

---

## 2. Methodological Soundness

**Rating: 2 (Needs Improvement)**

The methodological framework has several significant concerns that undermine confidence in the results.

**Near-tautological simulation design.** The central claim—constant overhead at η ≈ 20.66%—follows directly from the message model specification. Each node sends one 256-byte status report per cycle (excluded from η), receives one 512-byte coordination command (included), sends/receives heartbeats (64 B), and occasionally generates collision alerts (128 B). With fixed message sizes and deterministic per-cycle message counts, the overhead ratio is algebraically determined. The DES adds value only through the queueing dynamics at coordinator nodes, but with ρ_c = 0.05 (utilization 5%), there is essentially no queueing to speak of. The claim of "confirming the absence of queueing-induced nonlinearities" is trivially true when utilization is 5%. A more informative study would push coordinator utilization into the 0.5–0.9 range to identify where nonlinearities actually emerge.

**Abstraction level concerns.** The paper operates at a message-passing abstraction that excludes precisely the phenomena most likely to produce scale-dependent effects: MAC contention, correlated link outages, antenna scheduling, half-duplex constraints, and priority queueing. The authors acknowledge this (Section V-E, Table II), but the acknowledgment does not resolve the problem—it means the central scaling claim is conditional on an abstraction that excludes the most relevant physics. The statement that "physical-layer effects not modeled... could introduce additional scale-dependent behavior" effectively concedes that the O(1) finding may not hold in practice.

**Statistical framework mismatch.** Running 30 Monte Carlo replications is standard practice, but the near-zero variance (SD < 0.001%) reveals that the stochastic elements (node failures at 2%/year, message jitter) have negligible impact on the metrics of interest. The authors acknowledge this ("the MC framework serves primarily to confirm this low-variance property"), but this raises the question of why 30 replications are presented as a methodological contribution rather than simply stating the analytical result with a sensitivity analysis over input parameters. A parametric sensitivity analysis varying message sizes (±50%), reporting rates, and coordinator service rates would be far more informative than 30 replications of a near-deterministic model.

**Collision avoidance rate justification.** The 10⁻⁴/node/s rate is justified as "proximity monitoring events" with a 1,000:1 ratio to actual maneuvers. While the sensitivity analysis (varying from 10⁻⁵ to 10⁻³) is appreciated, the base rate itself is not well-grounded in published operational data. The cited ESA reference reports maneuver rates, not screening event rates; the 1,000:1 ratio appears to be an assumption rather than a measured quantity.

**Wall-clock time concern.** Processing 3.15 × 10¹¹ node-cycle events in 7 seconds (for N = 10⁵) implies ~45 billion events per second, which is implausible on commodity hardware even with minimal per-event computation. The "cycle-level event model" description suggests that events are not individually processed but rather batch-computed per cycle—effectively a closed-form calculation executed iteratively. This should be stated more transparently, as it further supports the interpretation that the DES is computing an analytical formula rather than simulating emergent dynamics.

---

## 3. Validity & Logic

**Rating: 3 (Adequate)**

The authors demonstrate commendable intellectual honesty in their limitations discussion and baseline interpretation notes. The repeated caveats about the reference baselines being "intentional bounds, not realistic competitors" (Section I-C) and the acknowledgment that the O(1) result is analytically expected are appreciated. The paper does not overclaim.

However, several logical issues deserve attention. First, the paper's framing creates a tension: it presents a simulation study whose primary result is analytically predictable, then spends considerable effort explaining why the simulation was necessary to confirm the analytical prediction. The argument that the DES "quantifies the protocol coefficient" and "confirms queue stability" is valid but modest—the coefficient is parameter-determined, and queue stability at ρ = 0.05 is not in doubt. The more interesting results (coordinator bandwidth thresholds, link availability sensitivity, exception-based telemetry) receive less emphasis than the overhead scaling result.

Second, the comparison framework is asymmetric in a way that favors the hierarchical architecture. The centralized baseline uses c = 1 (worst case), the mesh baseline uses global state (worst case), but the hierarchical architecture uses optimistic assumptions: perfect coordinator election, negligible handoff disruption, and no correlated failures. A fairer comparison would apply pessimistic assumptions uniformly or optimistic assumptions uniformly across all architectures.

Third, the exception-based telemetry validation (Section IV-E) confirms that a Bernoulli filter reduces message counts by the expected factor—this is again a law-of-large-numbers result, not a simulation finding. The authors correctly note that the coordination quality impact is unaddressed, but this is the entire question of interest: whether exception-based telemetry is viable depends on whether reduced reporting degrades coordination, not on whether it reduces bandwidth (which is trivially true).

The latency budget decomposition (Section IV-B) is well-constructed and informative. The identification of regional coordinator queueing as the dominant latency component, driven by burst arrivals of cluster summaries, is a genuine simulation insight that would not be obvious from analytical models alone.

---

## 4. Clarity & Structure

**Rating: 4 (Good)**

The paper is exceptionally well-organized and clearly written. The progressive disclosure of assumptions, the explicit abstraction scope table (Table II), the traffic accounting table (Table VI), and the metric definitions (Section III-F) all demonstrate careful attention to reproducibility and reader comprehension. The baseline interpretation note (Section I-C) is a model of transparent framing that other simulation studies should emulate.

The paper is, however, excessively long for the content it delivers. At approximately 12,000 words (estimated from the LaTeX source), it substantially exceeds typical IEEE T-AES article length. Much of the length comes from repeated caveats and qualifications—the same limitations are stated in the abstract, introduction, results, discussion, and conclusion. While thoroughness is appreciated, consolidating the caveats into a single comprehensive limitations section would improve readability without sacrificing transparency.

Tables are generally effective, though Table IV (Hierarchical Communication Overhead Scaling) is striking in its uniformity—ten rows of identical values (20.66%) with identical SDs (<0.01). While this confirms the O(1) scaling, a table of identical values conveys less information than a single sentence. The table could be replaced by a statement with a figure showing the flat line, or supplemented with additional metrics (latency, availability) that do vary with N.

The figures are referenced but not provided (as expected for a LaTeX source review). The figure captions are detailed and informative, which is good practice. Figure 2 (latency distribution) includes an analytical extrapolation to 10⁶ nodes that is clearly labeled as such—appropriate handling of unvalidated projections.

---

## 5. Ethical Compliance

**Rating: 4 (Good)**

The paper includes an appropriate acknowledgment of AI-assisted ideation (Claude 4.6, Gemini 3 Pro, GPT-5.2) in the Acknowledgment section, with a clear statement that the AI-generated concepts are "not validated in the current study." This is transparent and appropriate. The reference to a companion methodology paper [dyson_multimodel] provides additional context.

The author attribution ("Project Dyson Research Team" with a note that individual names will be provided for final publication) is unusual but not inappropriate for a preprint/initial submission. IEEE policy requires individual author identification for publication, which the authors acknowledge.

The data availability statement is commendable, though the repository commit hash is listed as "[PENDING]"—this must be resolved before publication. The promise of open-source code and interactive simulators supports reproducibility.

One minor concern: the paper references model versions (Claude 4.6, GPT-5.2) that do not exist as of the review date, suggesting either future-dated references or fictional model names. This should be clarified—if these are hypothetical, they should be labeled as such; if the paper is set in a future context, this framing should be explicit.

---

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is appropriate for IEEE T-AES in topic, though the contribution level is borderline for this venue given the methodological concerns raised above. The references are generally relevant and span the appropriate domains (distributed systems, queueing theory, constellation management, swarm robotics).

Several reference concerns: (1) Multiple references are non-archival web pages (SpaceX, Amazon, DARPA, DoD) that may not persist. While unavoidable for some operational programs, the paper relies on these for key claims about current constellation scale. (2) The NRL swarm reference [nrl_swarm] is explicitly noted as "non-peer-reviewed," which is appropriate transparency but weakens the evidentiary basis. (3) The companion paper [dyson_multimodel] is self-published on the project website and has not undergone peer review. (4) Several important related works are missing: Bhatt et al. (2023) on distributed satellite autonomy, the ESA Clean Space initiative's work on autonomous deorbiting coordination, and recent work on federated learning for satellite constellations that addresses similar scaling questions from a different angle.

The related work section (Section II) is comprehensive but could better position the paper's contribution relative to the closest prior work. The DARPA Blackjack program, in particular, targets autonomous satellite mesh networking at scales comparable to this study's lower range—a more detailed comparison of architectural choices would strengthen the paper.

---

## Major Issues

1. **Near-tautological central result.** The primary finding (η = 20.66%, O(1) scaling) is algebraically determined by the input parameters and message model. The DES confirms arithmetic rather than revealing emergent behavior. The paper needs either (a) a substantially richer physical-layer model that could produce scale-dependent effects, or (b) a reframing that positions the coordinator bandwidth, link availability, and exception telemetry results as the primary contributions rather than the overhead scaling confirmation.

2. **Missing realistic comparator.** The two reference baselines are acknowledged strawmen. Without a sectorized mesh or other practical decentralized architecture, the paper cannot support claims about the relative merit of hierarchical coordination. The repeated identification of sectorized mesh as "priority future work" suggests the authors recognize this gap; it should be addressed before publication in a top-tier venue.

3. **Physical-layer abstraction undermines scaling claims.** The paper claims to characterize "scaling properties" but excludes the physical-layer phenomena (MAC contention, correlated outages, antenna scheduling) most likely to produce scale-dependent behavior. The O(1) finding is valid only within the message-passing abstraction, which is explicitly acknowledged but insufficiently addressed. At minimum, a TDMA scheduling model within T_c should be implemented to test whether slot contention introduces scale-dependent effects at the upper end of the tested range.

4. **Computational model transparency.** The claimed wall-clock times (0.07 ms per node per run for a one-year simulation) imply batch computation rather than individual event processing. The paper should clearly state whether the DES processes individual message events or computes per-cycle aggregates analytically. If the latter, the term "discrete event simulation" may be misleading—"cycle-level analytical model with stochastic failure injection" would be more accurate.

5. **Exception-based telemetry validation is incomplete.** Validating that a Bernoulli filter reduces message counts by the expected factor is trivial. The engineering question—whether reduced reporting degrades coordination quality—is explicitly deferred. Without this analysis, the exception-based telemetry results cannot support design recommendations.

---

## Minor Issues

1. **Eq. (2):** The M/D/1 waiting time formula W_q = ρ / [2μ(1-ρ)] is the Pollaczek-Khinchine result for M/D/1. Confirm this is the waiting time (not sojourn time); the standard P-K formula for M/D/1 gives W_q = ρ / [2μ(1-ρ)], which is correct.

2. **Table III (Cluster Size):** The latency values show discrete jumps (508→340 ms between k_c = 75 and k_c = 100) rather than smooth variation. The explanation (burst-driven regional queueing) is provided but the discrete nature suggests a threshold effect that deserves more investigation—is there a critical N/k_c ratio?

3. **Section III-E, paragraph on coordinator bandwidth:** The statement "each node's transceiver must be capable of the coordinator ingest rate (≥50 kbps)" has significant implications for spacecraft radio design that are mentioned but not fully explored. This is a non-trivial hardware requirement that should be more prominently flagged as a design constraint.

4. **Table I (M/D/c Sensitivity):** The "Representative System" column labels are informal (e.g., "Hyperscale data center"). More precise characterization of what c = 1000 means in terms of actual ground infrastructure would be helpful.

5. **Section III-A, validation paragraph:** "Simulated mean latency agreed with the Pollaczek-Khinchine formula... to within 2%" at N = 100 is a weak validation. Validation at N = 10⁴ (near the saturation point) would be more meaningful.

6. **Abstract:** The abstract is dense and contains too many specific numbers. Consider reducing to the 3-4 most important quantitative findings.

7. **Section V-B (Comparison with Terrestrial Systems):** The claim that "none of these systems manages 10⁶ fully autonomous nodes" is debatable—cellular networks manage billions of devices with substantial local autonomy (handoff decisions, power control). The distinction should be more carefully drawn.

8. **References:** [starlink_ops] is cited as "2024 (non-archival; accessed February 2026)"—the access date is in the future relative to the publication date of 2024. Clarify the timeline.

9. **Eq. (5):** The mesh message complexity derivation jumps from f = O(N/log N) to M_mesh = O(N²) without showing the intermediate steps clearly. The choice of f = O(N/log N) to achieve O(log N) convergence should be justified more carefully.

10. **Section IV-H (Power Budget):** The 3% average power overhead is well-characterized, but the peak-to-average ratio (20W/5W = 4×) for coordinator mode has implications for battery sizing and solar array design that are not discussed.

---

## Overall Recommendation

**Major Revision**

The paper addresses an important problem space and demonstrates commendable transparency in its assumptions and limitations. However, the central contribution—confirming an analytically predictable O(1) scaling result through a message-level simulation that excludes the physical-layer effects most likely to perturb that result—is insufficient for IEEE T-AES in its current form. The most valuable contributions (coordinator bandwidth thresholds, link availability sensitivity, exception telemetry bandwidth reduction) are presented as secondary results when they should be primary. A major revision should: (1) implement at minimum a TDMA scheduling model to test for physical-layer scale dependence; (2) include a sectorized mesh comparator or substantially reframe the contribution to avoid reliance on strawman baselines; (3) reposition the coordinator bandwidth and link availability results as primary contributions; and (4) provide greater transparency about the computational model's actual event-processing granularity.

---

## Constructive Suggestions

1. **Reframe the primary contribution.** Instead of leading with the O(1) overhead confirmation (which is analytically expected), lead with the engineering design parameters that are genuinely simulation-derived: the coordinator bandwidth threshold (50 kbps for zero-drop), the link availability robustness boundary (p_link ≥ 0.5 with M_r = 2), and the regional coordinator queueing bottleneck. These are the results that would most interest T-AES readers designing real systems.

2. **Implement a minimal TDMA model.** Add a within-cycle TDMA slot scheduler with realistic guard intervals (e.g., 1 ms per slot for clock uncertainty and propagation). This would cost minimal implementation effort but would substantially strengthen the scaling claim by demonstrating that slot contention does not introduce scale-dependent effects—or, more interestingly, identifying the scale at which it does.

3. **Add a sectorized mesh comparator.** Even a simplified version—gossip limited to the k nearest orbital neighbors with k = O(√N)—would provide a far more informative comparison than the global-state mesh upper bound. This is the single change that would most improve the paper's contribution.

4. **Replace the overhead scaling table (Table IV) with a parametric sensitivity analysis.** Instead of 10 rows of η = 20.66%, show how η varies with message size (±50%), reporting rate (0.05–0.2 msg/s), and coordinator service rate (100–500 msg/s). This would characterize the engineering uncertainty bounds that matter for system design, rather than confirming that a deterministic calculation produces the same answer at different N.

5. **Couple exception-based telemetry to a simple dynamics model.** Even a two-body Keplerian propagator with J2 perturbation would allow estimation of realistic p_exc values as a function of prediction horizon and position uncertainty threshold. This would transform the exception telemetry results from a bandwidth accounting exercise into an actionable design guideline.