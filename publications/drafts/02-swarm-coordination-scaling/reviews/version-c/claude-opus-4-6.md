---
paper: "02-swarm-coordination-scaling"
version: "c"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-23"
recommendation: "Major Revision"
---



# Peer Review: Scaling Hierarchical Coordination for Million-Unit Space Swarms

---

## 1. Significance & Novelty — Rating: 3/5

The paper addresses a genuinely important gap: no prior work has systematically compared coordination architectures across the $10^3$–$10^6$ node range for space systems. This is a timely topic given mega-constellation growth trajectories. However, the novelty is tempered by several factors. The conclusion that hierarchical architectures scale better than flat centralized or fully-connected mesh topologies is well-established in distributed systems theory (the authors themselves cite Lynch's textbook for the $O(\log N)$ propagation result). The $O(N^2)$ cost of global-state mesh and the bottleneck of single-server centralized systems are essentially textbook results dressed in space-systems parameters. The most novel contribution—the Shepherd/Flock concept—is explicitly acknowledged as AI-generated ideation rather than rigorously engineered or validated, and the cellular network analogy is immediately obvious. The 50,000-node inflection point is interesting but, as the authors candidly admit, is parameter-dependent and insufficiently characterized.

## 2. Methodological Soundness — Rating: 2/5

This is the weakest aspect of the manuscript and the primary basis for concern.

The simulation framework, while described in reasonable detail, has fundamental modeling gaps that undermine confidence in the quantitative results. The communication model abstracts away Earth occlusion (only 35% line-of-sight acknowledged in limitations), MAC-layer contention, link acquisition/pointing, Doppler effects, and antenna gain patterns. The authors acknowledge these in Section V-E but do not bound their impact beyond rough estimates ("would approximately double," "could add 10–30%"). For a paper whose central contribution is quantitative comparison of overhead percentages, these unmodeled effects are of the same order as the differences being compared (e.g., 2–8% hierarchical vs. 5–15% centralized).

The queueing models are inconsistently applied. The centralized topology uses $M/D/1$, but the hierarchical topology's cluster coordinators are described with service rates without specifying the arrival process or queue discipline. The mesh topology has no queueing model at all—overhead is computed from message complexity alone. This asymmetry in modeling fidelity biases the comparison.

The mesh topology is parameterized for full global state convergence with $O(N^2)$ overhead, which is then compared against a hierarchical topology that achieves "fleet-wide coordination" through aggregation. This is not an apples-to-apples comparison: the hierarchical topology sacrifices per-node trajectory granularity (each node knows $O(k_c)$ trajectories in detail, not $O(N)$) while the mesh provides full $O(N)$ awareness. The paper should either equalize the information requirements or explicitly quantify the coordination capability gap.

The Monte Carlo framework uses 50–100 runs, which is adequate for mean estimation but marginal for tail statistics (99th-percentile latency). No convergence analysis is presented to justify that 50–100 runs are sufficient.

## 3. Validity & Logic — Rating: 3/5

The logical structure is generally sound, and the authors deserve credit for extensive self-criticism in the limitations section. However, several logical issues warrant attention:

The 50,000-node inflection point analysis is internally inconsistent. The analytical approximation (Eq. 8) predicts $5 \times 10^6$, which is two orders of magnitude above the observed $5 \times 10^4$. The authors attribute the discrepancy to "inter-regional state reconciliation overhead" but do not model this mechanism explicitly. With only five data points spanning three orders of magnitude and no intermediate sampling, the claim of a specific inflection point is not well-supported. The piecewise regression or change-point analysis the authors themselves suggest is needed has not been performed.

The argument that mesh topologies require $O(N^2)$ overhead rests on the assertion that fleet-wide collision avoidance requires global state. While the three astrodynamics justifications (coordinated orbit-raising, intersecting planes, conjunction cascades) are reasonable, the paper does not consider intermediate approaches—e.g., regional state with boundary exchange, or probabilistic conjunction screening that could reduce the effective state requirement to $O(N^{1+\epsilon})$. The hierarchical topology itself demonstrates that full $O(N)$ per-node state is not necessary, which undermines the justification for the mesh parameterization.

The duty cycle analysis (Table V) presents handoff success rates that decrease with shorter duty cycles, attributed to cumulative failure probability. However, the per-handoff failure mechanism is not clearly modeled—is it link failure during transfer, processing error, or state corruption? The 95% success rate at 1-hour cycles seems surprisingly low for a 1–10 second transfer over a Gbps link.

## 4. Clarity & Structure — Rating: 4/5

The paper is well-written, clearly structured, and commendably transparent about its limitations. The progressive disclosure of complexity—starting with simple models, then adding nuance—is effective. Tables and figures are well-designed and informative. The notation is consistent throughout.

Minor clarity issues: the paper oscillates between presenting the hierarchical topology as having $O(N)$ complexity (a strength) and acknowledging superlinear growth beyond 50,000 nodes (which contradicts the $O(N)$ claim). The relationship between the fixed four-level hierarchy and the claimed $O(N)$ complexity should be reconciled with the observed superlinear behavior more carefully.

The AI-assisted design section (V-B) is appropriately caveated but feels somewhat disconnected from the rest of the paper. Its placement in the Discussion rather than as a separate section or appendix would better reflect its exploratory nature—though it is already in the Discussion.

## 5. Ethical Compliance — Rating: 4/5

The paper is commendably transparent about AI tool usage, including specific model versions and a candid discussion of limitations (shared training corpora, sycophantic alignment, priming effects). The data availability statement with repository links supports reproducibility, though the commit hash is listed as "[PENDING]."

Two concerns: (1) The author listing as "Project Dyson Research Team" with a note that "individual author names will be provided for final publication" does not meet IEEE authorship requirements. Specific individuals who made substantial contributions must be identified. (2) Several references appear to be to non-peer-reviewed sources (SpaceX website, Amazon website, DARPA program pages, a "manuscript in preparation" self-citation). While some of these are unavoidable for operational systems, the self-citation to [41] (dyson_multimodel, "manuscript in preparation") is used to support methodological claims that cannot be verified.

## 6. Scope & Referencing — Rating: 3/5

The related work section covers swarm robotics, distributed systems theory, and military programs reasonably well. However, several significant omissions weaken the contextual framing:

- No reference to the substantial literature on **distributed space systems** and **fractionated spacecraft** (e.g., DARPA F6 program, which directly studied coordination architectures for disaggregated space systems).
- The **federated satellite systems** literature (e.g., work by Golkar and colleagues at MIT) is entirely absent despite being directly relevant.
- No engagement with the **network science** literature on hierarchical network design and optimization.
- The **consensus in multi-agent systems** literature (Olfati-Saber, Ren & Beard) is not cited despite being foundational for the coordination problem studied.
- Recent work on **autonomous constellation management** using onboard planning (e.g., by Arnas, Lifson, and others) is not discussed.
- The reference to "Claude 4.6," "Gemini 3 Pro," and "GPT-5.2" appears to cite model versions that do not exist as of the reviewer's knowledge cutoff. This raises concerns about the verifiability of the AI-assisted exploration.

---

## Major Issues

1. **Asymmetric modeling fidelity across topologies.** The centralized topology has a formal queueing model ($M/D/1$/$M/D/c$), the hierarchical topology has partial queueing specifications, and the mesh topology has none. The comparison is not conducted on equal analytical footing. All three topologies should be modeled with comparable rigor, or the paper should explicitly characterize how the asymmetry affects conclusions.

2. **Unequal information requirements invalidate direct comparison.** The mesh topology is parameterized for full $O(N)$ per-node state awareness while the hierarchical topology provides only $O(k_c)$ per-node awareness. These are fundamentally different coordination capabilities. The paper must either (a) equalize the information requirement and re-run the comparison, (b) introduce an intermediate mesh parameterization (e.g., locality-aware gossip with regional aggregation), or (c) explicitly quantify the coordination capability gap and discuss its operational implications.

3. **The 50,000-node inflection point is inadequately characterized.** Five data points over three orders of magnitude, with no intermediate sampling, no formal change-point analysis, and a two-order-of-magnitude discrepancy between the analytical prediction and observed value, do not support the claim of a specific inflection point. Either additional simulation runs at intermediate scales must be provided, or the claim must be substantially weakened.

4. **Unmodeled physical-layer effects are of the same magnitude as reported differences.** Earth occlusion, MAC contention, link acquisition overhead, and protocol framing collectively could double or triple the reported overhead values. Since the key finding is that hierarchical overhead is 2–8% versus 10–25% for mesh, these unmodeled effects could potentially alter the relative ranking of topologies under certain parameterizations.

5. **Authorship does not comply with IEEE policy.** A team name without individual authors is not acceptable for IEEE publication. The manuscript cannot proceed to publication without named authors who accept individual responsibility for the work.

6. **Fictitious AI model versions.** The cited model versions (Claude 4.6, Gemini 3 Pro, GPT-5.2) do not correspond to publicly released models. If these are internal/beta versions, this must be clarified; if they are fabricated, this is a serious integrity concern. The companion reference [41] is to a manuscript "in preparation" by the same group, providing no independent verification.

## Minor Issues

1. The collision avoidance rate of $10^{-4}$/node/s (Table II) implies ~8.6 collision avoidance events per node per day. At $N = 10^6$, this is 8.6 million events/day fleet-wide. This seems extremely high and is not justified against operational data. Current conjunction screening rates for LEO are orders of magnitude lower per object.

2. Equation (5) defines mesh message complexity but the derivation jumps from "fanout $f = O(N/\log N)$" to $O(N^2)$ without justifying why this specific fanout is necessary for convergence. Standard gossip with $f = O(\log N)$ achieves $O(N \log^2 N)$ total messages for single-rumor dissemination; the $N$-rumor extension should be derived more carefully.

3. The power analysis (Eq. 7) assumes uniform duty distribution across all cluster members. In practice, not all nodes may be equally capable of serving as coordinator (due to orbital position, power state, hardware degradation). The impact of non-uniform coordinator eligibility on power distribution should be discussed.

4. Table III (Cluster Size) reports values without confidence intervals, despite the Monte Carlo framework. All quantitative results should include uncertainty estimates.

5. The 2% annual failure rate yielding 50-year MTTF is correct for exponential distributions but the reference [Castet] reports significantly higher early-life failure rates for small satellites. The constant-rate assumption may understate failures in the first 1–3 years.

6. The paper claims the simulation is "implemented in Python" but provides no information about validation or verification of the simulation code (e.g., unit tests, comparison against analytical solutions for simple cases, sensitivity to random seeds).

7. Several figures are referenced but not viewable in the review copy (PDF compilation issue). The reviewer assumes they exist and match their captions.

8. The "silence by default" / exception-based telemetry optimization is presented as reducing bandwidth by "approximately two orders of magnitude" without simulation evidence—this appears to be an assertion rather than a measured result.

9. Reference [28] (Hung, NRL) appears to be a magazine article rather than a peer-reviewed source, and the citation is incomplete.

10. The abstract states the hierarchical topology maintains "2–8% overhead past $10^6$ nodes," but Table VI shows 10% overhead at $5 \times 10^5$ nodes without optimizations. The abstract should clarify this refers to the optimized configuration.

---

## Overall Recommendation: **Major Revision**

The paper addresses an important and timely problem, is well-written, and demonstrates commendable intellectual honesty about its limitations. However, the methodological concerns—particularly the asymmetric topology modeling, unequal information requirements, unmodeled physical-layer effects, and inadequately characterized inflection point—are sufficiently serious that the quantitative conclusions cannot be accepted in their current form. The authorship and model version issues must also be resolved.

---

## Constructive Suggestions

1. **Equalize the comparison framework.** Introduce a "locality-aware mesh" variant that uses hierarchical aggregation for non-local state (similar to what the hierarchical topology does), creating a fair three-way comparison at equivalent coordination capability. Alternatively, define a formal "coordination capability metric" and plot overhead against capability for each topology, allowing readers to compare at equal capability levels.

2. **Add intermediate fleet sizes** around the claimed inflection point ($N \in \{20\text{k}, 30\text{k}, 40\text{k}, 60\text{k}, 70\text{k}, 80\text{k}\}$) and apply formal change-point detection (e.g., Bayesian change-point analysis or segmented regression with AIC/BIC model selection) to rigorously characterize the transition.

3. **Incorporate at least first-order physical-layer effects.** A stochastic link availability model (e.g., Bernoulli link failures with probability calibrated to Earth occlusion geometry) and a simple MAC contention model (e.g., slotted ALOHA throughput reduction) would substantially strengthen the results without requiring full RF propagation simulation.

4. **Validate the simulation** against closed-form solutions for degenerate cases (e.g., verify that the centralized topology's latency matches $M/D/1$ theory at low utilization; verify that mesh convergence time matches known gossip bounds for small $N$).

5. **Provide confidence intervals for all tabulated results** (Tables III, V, VI). The Monte Carlo framework exists; the uncertainty quantification should be reported consistently.

6. **Strengthen the mesh topology analysis** by simulating at least one intermediate gossip parameterization (e.g., $f = O(\sqrt{N})$ with regional aggregation) to demonstrate that the $O(N^2)$ characterization is not an artifact of the extreme parameterization chosen.

7. **Separate the AI-assisted exploration** into a clearly delineated subsection or appendix, and remove the Shepherd/Flock concept from the abstract and contributions list unless it can be validated through simulation. As presented, it is speculative ideation rather than a research contribution.

8. **Engage with the fractionated/federated spacecraft literature** and multi-agent consensus theory, which provide directly relevant prior art that strengthens the paper's positioning and may offer analytical tools applicable to the coordination problem.

9. **Resolve authorship** by listing individual contributors with their specific roles, per IEEE policy. If the work is primarily by one or two individuals with AI assistance, this should be stated clearly.

10. **Clarify or correct the AI model versions cited.** If these are hypothetical future models used as a thought experiment, state this explicitly. If they are real tools used in the research, provide verifiable version information and access dates.