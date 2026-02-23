---
paper: "02-swarm-coordination-scaling"
version: "a"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-23"
recommendation: "Major Revision"
---

# Peer Review: "Scaling Hierarchical Coordination for Billion-Unit Space Swarms"

**Manuscript submitted to IEEE Transactions on Aerospace and Electronic Systems**

---

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a genuinely important gap: the systematic comparison of coordination architectures at scales between current mega-constellations (~10⁴) and hypothetical future swarms (~10⁶). This intermediate regime is indeed underexplored, and the research questions are well-motivated. The identification of a 50,000-node inflection point and the duty cycle optimization are potentially useful contributions for the mega-constellation community.

However, the novelty is substantially undermined by two factors. First, the conclusion that hierarchical architectures outperform centralized and flat mesh topologies at scale is well-established in distributed systems theory (the authors themselves cite Lynch [7] and the $O(\log N)$ propagation result from Li et al. [19]). The simulation essentially confirms what queueing theory and distributed systems fundamentals predict. The paper would be significantly more novel if it explored *which* hierarchical designs work best, rather than spending considerable space establishing that hierarchy beats centralized and mesh—a result that is almost axiomatic in the distributed systems literature.

Second, the title promises "Billion-Unit Space Swarms" but the simulation only reaches 10⁶ nodes—three orders of magnitude short of a billion. This discrepancy between the title's ambition and the actual scope is misleading. The paper also frames itself around "Dyson swarm precursors," which are speculative constructs far beyond any engineering horizon. While aspirational framing is acceptable, it risks undermining credibility when the actual technical contributions are more modest and applicable to near-term systems (42,000-satellite Starlink, military drone swarms). The paper would benefit from a more grounded framing that emphasizes the near-term applicability highlighted in Section VI.

---

## 2. Methodological Soundness

**Rating: 2 (Needs Improvement)**

The DES framework is described at a reasonable level of abstraction, but several critical methodological concerns arise:

**Queueing model oversimplification.** The centralized topology is modeled as a single M/D/1 queue (Eq. 1–2), which assumes a single-server, single-queue system. No real ground station operates this way—Starlink's ground infrastructure uses distributed processing across multiple servers and ground stations. The 10,000-node "scalability limit" is thus an artifact of the single-server assumption rather than a fundamental property of centralized architectures. A more realistic model would use M/D/c queues or networks of queues. The authors should at minimum acknowledge this and perform sensitivity analysis on the processing capacity parameter $C$.

**Mesh topology mischaracterization.** Equation (4) claims $O(N^2)$ message complexity by setting fanout $f = O(N/\log N)$, but this is not how gossip protocols are typically parameterized. Standard gossip protocols use constant or logarithmic fanout (e.g., $f = O(\log N)$), achieving $O(N \log^2 N)$ total messages for convergence—far from quadratic. The claim that mesh becomes impractical at 10⁵ nodes may be an artifact of this unfavorable parameterization. The authors should simulate gossip with standard fanout values and compare against structured peer-to-peer overlays (e.g., Chord, Kademlia) that achieve $O(N \log N)$ complexity.

**Missing validation against real systems.** The simulation is never validated against any real-world system. The authors could calibrate against published Starlink operational data (conjunction avoidance response times, telemetry cadences) or Iridium crosslink performance. Without any empirical anchor, the absolute numbers (overhead percentages, latency values) are difficult to interpret. The authors acknowledge this in the limitations section but do not attempt even order-of-magnitude validation.

**Monte Carlo concerns.** The paper states 50–100 runs per configuration but does not justify this number. For rare-event analysis (e.g., coordinator failure cascades), 50 runs may be grossly insufficient. No convergence analysis is presented to demonstrate that the confidence intervals have stabilized. The bootstrap method is mentioned but no details are provided on the bootstrap procedure (number of resamples, bias correction).

**Reproducibility.** While a repository URL is provided, the paper does not describe the simulation implementation language, computational requirements, or wall-clock time for the largest configurations. Simulating 10⁶ nodes over one year at one-second resolution for collision avoidance events would generate an enormous number of events—the computational feasibility of this is not discussed.

---

## 3. Validity & Logic

**Rating: 2 (Needs Improvement)**

Several logical issues weaken the paper's conclusions:

**Circular reasoning in the AI validation (Section V).** The three LLMs were "provided with the simulation results" before generating their architectural proposals. Their convergence on hierarchical coordination therefore cannot be considered independent validation—they were primed with the conclusion. True independent validation would require the models to arrive at the same conclusion from first principles or from the problem specification alone, without seeing the simulation results. The paper claims this provides "epistemic triangulation analogous to expert panel consensus," but expert panels are valuable precisely because experts bring independent domain knowledge and can challenge assumptions. LLMs provided with the same input data and asked the same question are not epistemically independent in the same way. The citation of Surowiecki's *Wisdom of Crowds* [30] is inapt—Surowiecki's thesis requires independent judgment, which is violated when the models are shown the results.

**The 50,000-node inflection point.** Table V shows overhead values of 1.0%, 2.0%, 4.0%, 6.0%, 10.0% at five data points. These five points are insufficient to establish an "inflection point" with any statistical rigor. The overhead growth from 2% to 4% to 6% appears roughly linear on a log scale, not superlinear. The claim of superlinear growth beyond 50,000 nodes requires more data points in the 10,000–100,000 range and a formal statistical test (e.g., fitting piecewise linear models and comparing via AIC/BIC). The term "inflection point" has a precise mathematical meaning (change in sign of the second derivative) that is not demonstrated.

**Inconsistency in hierarchical complexity claims.** The paper states the hierarchical topology has $O(N \log N)$ message complexity (below Eq. 3), but Eq. (3) itself shows $M_{\text{total}} = N + N/k_c + N/(k_c \cdot k_r)$, which is $O(N)$ for fixed $k_c$ and $k_r$. The $O(N \log N)$ claim is justified by noting "each level of the hierarchy contributes $O(N)$ messages and the number of levels scales as $O(\log N)$," but this is only true if the hierarchy depth grows with $N$. For a fixed four-level hierarchy (as described), the complexity is $O(N)$, not $O(N \log N)$. This inconsistency needs resolution.

**Pareto analysis (Fig. 6, Table III).** The claim that the 7-day duty cycle is "Pareto-dominated" by 24–48h configurations requires that 24h or 48h be strictly better on *all* objectives. But Table III shows the 7-day cycle has the highest handoff success rate (99.9%) and lowest handoff cost. It is not Pareto-dominated; it trades availability for handoff reliability. The Pareto analysis needs correction.

---

## 4. Clarity & Structure

**Rating: 4 (Good)**

The paper is generally well-written, clearly organized, and follows IEEE TAES formatting conventions. The progression from problem statement through simulation framework to results and discussion is logical and easy to follow. The abstract accurately summarizes the main findings, and the research questions are clearly stated.

Tables I–V are well-formatted and informative. The described figures (which cannot be evaluated since only placeholders are provided) appear to be appropriately chosen—log-log scaling plots, latency distributions, and Pareto frontiers are all standard and appropriate visualizations for this type of analysis.

Minor clarity issues include: the notation switches between $k_c$ for cluster size and the cluster size values in Table II without always being explicit about which is being used; the term "overhead" is used to mean both bandwidth fraction and a more general coordination cost without always disambiguating; and the transition from DES results (Section IV) to AI deliberation (Section V) is somewhat jarring—the reader is not prepared for the methodological shift.

The paper is somewhat long for the depth of its technical contribution. Section II (Related Work) is thorough but could be condensed. Section VI (Discussion) contains valuable material on near-term applicability but also includes speculative comparisons (e.g., to BGP, ATC) that, while interesting, dilute the technical focus.

---

## 5. Ethical Compliance

**Rating: 3 (Adequate)**

The paper is transparent about the use of LLMs in Section V and the Acknowledgment section, which is commendable. However, several concerns arise:

The use of LLM deliberation as a "validation methodology" raises significant questions about research integrity standards. The paper acknowledges this is "a novel methodology whose robustness requires further study," but then proceeds to present the LLM convergence as one of the paper's principal contributions. IEEE does not currently have established guidelines for LLM-as-validator methodologies, and the paper should more explicitly discuss the epistemological limitations. Specifically: LLMs are trained on overlapping corpora and may share systematic biases; their "convergence" may reflect training data consensus rather than independent reasoning; and their outputs are not reproducible across model versions or even across runs with temperature > 0.

The author affiliation is listed only as "Project Dyson Research Team" with a URL. No individual authors are named, which is unusual for IEEE publications and raises questions about accountability. IEEE authorship guidelines require that all listed authors have made substantial contributions and can take responsibility for the work. An anonymous team affiliation does not meet this standard.

The reference to a "companion paper" [35] that is "manuscript in preparation" and published by the same group is acceptable but the self-citation should be noted. The data availability statement references a URL but the repository's existence and contents cannot be verified from the manuscript.

---

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is broadly appropriate for IEEE TAES, which publishes work on aerospace systems, including constellation management and autonomous systems. However, the paper sits at an awkward intersection: the DES methodology is standard distributed systems work, the application domain is speculative space infrastructure, and the AI validation is a novel (and contested) methodology. A more focused version targeting either the near-term mega-constellation community or the distributed systems community might find a more natural home.

The references are generally appropriate but have notable gaps. The distributed systems literature is underrepresented—there is no citation of Lamport's foundational work on distributed clocks and consensus, no reference to Raft or Paxos consensus protocols (directly relevant to coordinator election), and no citation of structured overlay networks (Chord, Kademlia, Pastry) that achieve better-than-$O(N^2)$ scaling in peer-to-peer systems. The omission of these is particularly problematic given that the paper's core contribution is comparing distributed coordination topologies.

Several references are to websites or press releases (SpaceX, Amazon, DARPA, DoD) rather than peer-reviewed sources. While some of these are unavoidable for current operational systems, the paper would benefit from more peer-reviewed references on constellation operations. Recent work on autonomous constellation management (e.g., by Arnas, Lifson, and others on distributed orbit determination and autonomous collision avoidance) is not cited.

The LLM model versions cited (Claude 4.6, Gemini 3 Pro, GPT-5.2) do not correspond to any publicly released models as of mid-2025, raising questions about whether these are real or hypothetical model designations.

---

## Major Issues

1. **Unfair topology comparison (Section III-B).** The centralized model uses a single-server queue while real centralized systems use distributed processing. The mesh model uses an adversarial fanout parameterization that inflates complexity to $O(N^2)$. These modeling choices systematically favor the hierarchical topology. The comparison must use realistic parameterizations for all three topologies, including multi-server centralized models and standard gossip fanout.

2. **AI "validation" is not independent (Section V).** Providing the simulation results to the LLMs before asking for architectural proposals invalidates the claim of independent validation. This section should either be removed, reframed as "AI-assisted architectural exploration" (not validation), or redone with the models receiving only the problem specification.

3. **Insufficient evidence for the 50,000-node inflection point (Section IV-D).** Five data points cannot establish an inflection point. The paper needs at least 10–15 data points in the 10⁴–10⁶ range, formal statistical testing for change in scaling behavior, and sensitivity analysis showing the inflection point is robust to parameter choices.

4. **Inconsistent complexity analysis (Section III-B-2).** The paper claims $O(N \log N)$ complexity for the hierarchical topology but the equations show $O(N)$ for a fixed-depth hierarchy. This must be resolved—either the hierarchy depth is fixed (and complexity is $O(N)$) or it grows with $N$ (and the four-level structure described is not the actual model).

5. **No empirical validation.** The simulation is never calibrated against any real system. Even approximate validation against published Starlink or Iridium operational parameters would substantially strengthen the paper.

---

## Minor Issues

1. **Title mismatch.** "Billion-Unit" in the title; maximum simulated scale is 10⁶ (one million). Change the title to reflect the actual scope.

2. **Eq. (2):** The M/D/1 mean waiting time formula shown is the standard result, but the paper models the coordinator as M/D/1 while also stating messages arrive from $N$ nodes at rate $r$—this is actually a D/D/1 or at best a superposition of $N$ deterministic streams, which for large $N$ approaches Poisson (justifying M/D/1) but this should be stated explicitly.

3. **Table III:** "Power Var." column—variance of what, exactly? Is this the coefficient of variation of power consumption across nodes, the temporal variance for a single node, or something else? Units or a clearer definition are needed.

4. **Section IV-E, Eq. (6):** The power overhead calculation assumes uniform duty distribution, but the paper also discusses dedicated Shepherd spacecraft (Section V-C) that would *not* rotate. These two models are contradictory and should be reconciled.

5. **Section III-B-3:** The claim $D = O(N^{1/3})$ for a random geometric graph in 3D orbital space is stated without justification. Orbital shells are approximately 2D (thin shells), suggesting $D = O(N^{1/2})$ might be more appropriate.

6. **Reference [35]** is a self-citation to a manuscript "in preparation" by the same group. This cannot be verified by reviewers and should either be made available or removed.

7. **Section III-C:** The 2% annual failure rate yielding 50-year MTTF is correct for exponential distributions, but the cited source [28] (Castet & Saleh 2009) reports significantly higher failure rates for early-life satellites. The 2% figure should be justified more carefully, noting whether it applies to the operational phase only.

8. **Fig. 1 caption** references "message aggregation ratios" but these ratios are not defined until the text following the figure. Consider adding the ratios to the caption.

9. **Section II-C:** The claim that Li et al. [19] establish $O(\log N)$ propagation for hierarchical topologies is a mischaracterization—that paper addresses GNN-based path planning, not general hierarchical propagation bounds.

---

## Overall Recommendation

**Major Revision**

The paper addresses a relevant problem and is well-written, but suffers from methodological issues that undermine its core claims. The topology comparison is biased by unrealistic modeling of the centralized and mesh alternatives. The AI "validation" methodology is fundamentally flawed as presented (not independent). The 50,000-node inflection point lacks statistical rigor. The complexity analysis contains internal contradictions. These are not minor issues—they affect the paper's primary contributions. However, the underlying research direction is sound, the simulation framework could be strengthened, and the near-term applicability to mega-constellations is genuinely valuable. A substantially revised version that addresses the major issues could be suitable for publication.

---

## Constructive Suggestions

1. **Strengthen the centralized and mesh baselines.** Model the centralized topology as an M/D/c queue (multiple parallel servers) with realistic ground infrastructure capacity, and the mesh topology with standard gossip fanout ($f = O(\log N)$). If the hierarchical topology still wins—which it likely will at the largest scales—the result will be far more convincing. Consider also including structured P2P overlays as a fourth topology.

2. **Reframe Section V as architectural exploration, not validation.** Remove the claim of "independent validation." Instead, present the LLM deliberation as a structured brainstorming exercise that generated the Shepherd/Flock concept—which is genuinely interesting and novel. Alternatively, repeat the exercise with models receiving only the problem specification (not the results) and report whether they still converge on hierarchical architectures.

3. **Densify the scaling analysis around the claimed inflection point.** Run simulations at $N \in \{10k, 20k, 30k, 40k, 50k, 60k, 70k, 80k, 90k, 100k\}$ and fit piecewise regression models to rigorously identify any change in scaling behavior. Report the inflection point with confidence bounds.

4. **Calibrate against Starlink.** Use publicly available data on Starlink's conjunction avoidance response times, telemetry cadences, and ground station processing to calibrate the centralized model. Then show that the calibrated model's predicted bottleneck is consistent with SpaceX's known infrastructure investments as the constellation grows. This would transform the paper from a theoretical exercise into a practically grounded prediction.

5. **Resolve the fixed-depth vs. growing-depth hierarchy question.** If the hierarchy has a fixed four levels, state that complexity is $O(N)$ and explain why this is sufficient. If the depth grows with $N$, describe the adaptive hierarchy algorithm and analyze its overhead. Either way, the current inconsistency must be eliminated.