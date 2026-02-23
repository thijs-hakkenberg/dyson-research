---
paper: "02-swarm-coordination-scaling"
version: "b"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-23"
recommendation: "Major Revision"
---

# Peer Review: "Scaling Hierarchical Coordination for Million-Unit Space Swarms"

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a genuinely important gap: no prior work has systematically compared coordination architectures across the $10^3$–$10^6$ node range using quantitative simulation. The scaling challenge for mega-constellations is real and timely, with Starlink approaching 10,000 nodes and approved for 42,000. The research questions are well-motivated and the problem framing is compelling. The paper correctly identifies that the intermediate regime of $10^4$–$10^6$ nodes is underexplored in the literature.

However, the novelty is somewhat limited. The conclusion that hierarchical architectures scale better than centralized or flat mesh topologies is well-established in distributed systems theory (as the authors themselves acknowledge via Lynch [7], Li et al. [19], and the BGP/cellular analogies in Section VI-B). The simulation essentially confirms what queueing theory and information-theoretic arguments predict: centralized systems hit processing bottlenecks, flat gossip for global state is $O(N^2)$, and hierarchical aggregation achieves $O(N)$. The 50,000-node "inflection point" is parameter-dependent (as the authors commendably acknowledge), which limits its value as a generalizable finding. The Shepherd/Flock concept, while interesting, is essentially the cellular network paradigm applied to space—an analogy the authors themselves draw explicitly. The AI-assisted exploration in Section V, while transparently presented, does not produce insights that a competent systems architect would not reach through conventional design analysis.

The paper would be significantly more novel if it provided (a) analytical closed-form expressions for the overhead inflection as a function of the parameter space, enabling designers to compute thresholds for their specific configurations, or (b) validation against real operational data from Starlink or another constellation, or (c) a deeper treatment of the dynamic spatial partitioning algorithm with convergence guarantees.

## 2. Methodological Soundness

**Rating: 2 (Needs Improvement)**

The DES framework is described at a reasonable level of detail, and the Monte Carlo approach with bootstrap confidence intervals is appropriate. The parameter table (Table I) is commendably thorough and supports reproducibility. The choice of 50–100 runs per configuration is adequate for the metrics reported.

However, several methodological concerns are significant:

**Centralized model fairness.** While the authors acknowledge that the $M/D/1$ single-server model is a "worst-case bound" and discuss $M/D/c$ extensions (Eq. 3), the simulation results and figures (Table II, Figs. 2–3) appear to report only the $c=1$ case. This creates an asymmetric comparison: the centralized topology is evaluated at its worst case while the hierarchical topology is evaluated at its optimized configuration ($k_c = 100$, optimal duty cycle). A fair comparison would simulate the centralized topology with $c = 10$ or $c = 100$ parallel servers—values easily achievable with modern cloud infrastructure—and show where it still fails relative to the hierarchical approach. The qualitative argument that "the limit remains linear in the number of servers while fleet growth may be exponential" (Section III-B-1) is valid but needs quantitative support in the results.

**Mesh model parameterization.** The $O(N^2)$ characterization of mesh overhead assumes every node needs full trajectory awareness of all $N$ nodes. This is a strong assumption. In practice, collision avoidance in orbital mechanics is inherently local: conjunction screening uses spatial filters (e.g., the conjunction assessment process screens by orbital element similarity before computing close approaches). The paper argues this is justified by "fleet-wide collision avoidance," but a more realistic model would use a hybrid approach where local gossip handles nearby conjunctions and a hierarchical overlay handles rare long-range coordination events. The current parameterization appears designed to make mesh look bad, even though the authors discuss this trade-off honestly in Section III-B-3.

**Abstracted communication model.** The simulation abstracts away MAC-layer scheduling, link acquisition, pointing constraints, Doppler effects, and Earth occlusion—all of which are first-order effects for inter-satellite links in LEO. The authors acknowledge this in Section VI-D, but these simplifications are severe enough to question whether the overhead percentages reported (2–8% for hierarchical) are meaningful in absolute terms. For a journal of this caliber, at minimum a sensitivity analysis showing how overhead changes with realistic link availability (e.g., 50% duty cycle due to Earth occlusion) would be expected.

**Statistical rigor of the inflection point.** The 50,000-node threshold is identified from five data points (Table V) spanning three orders of magnitude. The authors acknowledge this limitation ("five data points... provide limited resolution"), but then proceed to build significant architectural recommendations on it. A piecewise regression or change-point detection analysis with finer granularity in the $10^4$–$10^5$ range is needed to substantiate this claim.

**Reproducibility.** The paper states that source code is available at projectdyson.org, but this URL does not appear to host a peer-reviewable repository at the time of review. The simulation is described as "implemented in Python using an event-driven architecture" without specifying the DES library (SimPy? custom?), Python version, or dependency versions. For a simulation-based paper, this level of detail is insufficient.

## 3. Validity & Logic

**Rating: 3 (Adequate)**

The logical structure of the paper is generally sound: the research questions are clearly stated, the simulation framework is designed to address them, and the conclusions follow from the results within the stated assumptions. The authors deserve credit for extensive and honest discussion of limitations throughout the paper—the caveats on the centralized model (Section III-B-1), mesh parameterization (Section III-B-3), inflection point (Section IV-D), and AI exploration (Sections V-A and V-E) are unusually thorough and demonstrate intellectual honesty.

Several logical concerns merit attention. First, the claim that hierarchical coordination is "the only viable topology at million-node scale" (abstract) is overstated given the modeling choices. The centralized topology is modeled at worst case; the mesh topology is parameterized for global convergence. A hybrid topology—hierarchical for routine coordination with mesh-like local gossip for collision avoidance—is not evaluated but is arguably the most realistic architecture. The paper's framing as a three-way comparison among pure topologies, while clean, may miss the most practical design point.

Second, the duty cycle analysis (Section IV-C, Table IV) presents results that are internally consistent but the "paradoxical" result about shorter duty cycles having lower handoff success rates is not paradoxical at all—it is a straightforward consequence of more frequent handoffs having more opportunities for failure. The framing as paradoxical suggests the authors may be over-dramatizing a simple statistical result.

Third, the power budget analysis (Eq. 7) is overly simplistic. The 0.15 W average overhead per node assumes uniform rotation, but in practice, nodes with better solar exposure, thermal margins, or communication geometry would be preferred as coordinators, creating non-uniform duty distributions. The analysis also ignores the mass penalty of equipping every node with coordinator-capable hardware (higher-power transmitters, additional processing), which is precisely the motivation for the Shepherd/Flock concept but is not quantified.

The connection between the DES results and the AI-generated concepts is handled carefully. The authors correctly note that the AI models were primed with simulation results and that their convergence may reflect training data consensus rather than independent validation. This is a model of transparent reporting for AI-assisted research.

## 4. Clarity & Structure

**Rating: 4 (Good)**

The paper is well-organized and clearly written. The progression from problem motivation (Section I) through related work (Section II), methodology (Section III), results (Section IV), AI exploration (Section V), and discussion (Section VI) is logical and easy to follow. The abstract is accurate and comprehensive, though at 250+ words it is longer than typical for IEEE T-AES.

The figures are well-conceived: the architecture diagram (Fig. 1), overhead scaling (Fig. 2), latency distributions (Fig. 3), failure resilience (Fig. 4), cluster optimization (Fig. 5), duty cycle Pareto front (Fig. 6), scaling trajectory (Fig. 7), and topology summary (Fig. 8) collectively tell a coherent visual story. However, since the paper is submitted in LaTeX without actual figure files, the reviewer cannot assess the quality of the actual visualizations—only the captions and textual descriptions.

The mathematical notation is consistent and the equations are clearly presented. The distinction between $O(N)$ complexity for the fixed four-level hierarchy versus $O(N \log N)$ for an adaptive hierarchy (Section III-B-2) is a useful clarification. The explanation of why mesh overhead is $O(N^2)$ for global state convergence (Section III-B-3) is thorough, though as noted above, the assumption driving this result is debatable.

Minor clarity issues: The paper occasionally uses imprecise language ("approximately two orders of magnitude" for exception-based telemetry reduction in Section IV-D) without supporting data. The transition between the DES results (Section IV) and the AI exploration (Section V) is somewhat jarring—the paper effectively presents two different studies stitched together, and the connection could be smoother.

## 5. Ethical Compliance

**Rating: 5 (Excellent)**

This paper sets an exemplary standard for transparency in AI-assisted research. The AI models used are explicitly named with version numbers (Section V-A), the methodology is described in detail, and—most importantly—the limitations of the AI-assisted process are discussed with unusual candor (Sections V-A and V-E). The authors explicitly warn against interpreting AI convergence as independent validation, identify priming effects, note shared training corpora, and acknowledge sycophantic alignment tendencies. This level of self-critical transparency exceeds what most papers in the field provide.

The acknowledgment section appropriately discloses AI tool usage and computational resources. The note about provisional affiliation and forthcoming author names is unusual but acceptable for review purposes; IEEE authorship guidelines will need to be satisfied before publication. The data availability statement promises open-source code and datasets, which is commendable if fulfilled.

The only minor concern is the use of model version numbers (Claude 4.6, Gemini 3 Pro, GPT-5.2) that do not correspond to any publicly released models as of the review date, raising questions about whether these are real model designations or placeholders. This should be clarified.

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is appropriate for IEEE T-AES in its treatment of space systems coordination, though the AI-assisted design exploration (Section V) and the IoT/autonomous vehicle applications (Section VI-A) stretch the scope somewhat. The core DES study is squarely within scope.

The reference list of 35 items covers the major relevant areas: constellation operations, swarm robotics, distributed systems theory, queueing theory, and gossip protocols. However, several notable gaps exist:

- **No references to actual Starlink coordination architecture papers.** The SpaceX reference [1] is a website, not a technical publication. Recent papers by Handley (2018, "Delay is not an option") and others analyzing Starlink's ISL topology and routing would strengthen the related work.
- **Missing key distributed systems references.** The paper does not cite Birman et al.'s work on scalable gossip protocols, nor the extensive literature on hierarchical consensus (e.g., Guerraoui and Rodrigues). The SWIM protocol (Das et al., 2002) is directly relevant to failure detection in large-scale distributed systems.
- **No references to actual space-based distributed computing work.** The DARPA Blackjack program, which explicitly targets autonomous satellite mesh networking, is not cited. Nor is the ESA's work on distributed satellite systems or the extensive literature on formation flying coordination (e.g., Scharf et al., 2004).
- **The self-citation [34] is to a manuscript "in preparation"** and cannot be verified. This is acceptable for methodology description but should not carry evidentiary weight.
- **Reference [30] (Surowiecki, "The Wisdom of Crowds")** is a popular science book, not a peer-reviewed source, and its citation to support a claim about LLM training data overlap is a stretch.

Several references are to websites or gray literature (SpaceX [1], Amazon [3], DARPA [20], DoD [22], Google S2 [33]) that may not be stable or peer-reviewed. While some of these are unavoidable for current operational systems, the paper would benefit from more peer-reviewed sources where available.

---

## Major Issues

1. **Asymmetric topology comparison.** The centralized topology is evaluated at worst case ($c=1$) while the hierarchical topology is evaluated at its optimized configuration. The paper must either (a) simulate the centralized topology with realistic parallelization ($c = 10, 100, 1000$) and show where it still fails, or (b) reframe the contribution as characterizing the hierarchical topology's performance rather than claiming it is "the only viable" option. The current framing overstates the case against centralized architectures.

2. **Mesh topology parameterization assumes global state convergence is required.** The argument that every node needs trajectory awareness of all $N$ nodes for collision avoidance is not well-justified for orbital mechanics, where conjunction screening is inherently spatial. The paper should either (a) provide a rigorous argument for why global state is necessary (e.g., for coordinated orbit-raising maneuvers affecting the entire fleet simultaneously), (b) simulate a hybrid mesh with local gossip + hierarchical overlay, or (c) clearly label the mesh results as an upper bound on overhead for the worst-case coordination requirement.

3. **Insufficient statistical support for the 50,000-node inflection point.** Five data points across three orders of magnitude cannot reliably identify a change point. The paper needs (a) additional simulation runs at $N \in \{20000, 30000, 40000, 60000, 70000, 80000\}$, and (b) formal change-point detection or piecewise regression analysis with confidence intervals on the threshold location.

4. **No validation against real systems.** The paper makes claims about Starlink's coordination challenges and the applicability of results to mega-constellations, but provides no validation against real operational data. Even a qualitative comparison showing that the model's predictions at $N = 7000$ are consistent with known Starlink operational characteristics would significantly strengthen the paper.

5. **Communication model abstractions are too severe for quantitative claims.** The absence of Earth occlusion, MAC-layer contention, link acquisition delays, and pointing constraints means the absolute overhead percentages (2–8% for hierarchical) are not credible for real space systems. At minimum, a sensitivity analysis varying link availability from 100% down to realistic values (30–70% for LEO ISLs) is needed.

## Minor Issues

1. **Abstract length.** At approximately 280 words, the abstract exceeds the typical IEEE T-AES guideline of ~200 words. Consider condensing.

2. **Section III-B-2, Eq. 5.** The message complexity expression $M_{\text{total}} = N + N/k_c + N/(k_c \cdot k_r)$ omits downlink command messages. If the hierarchy is bidirectional (commands flow down as well as reports flow up), the total should be approximately doubled.

3. **Table IV column headers.** "Power Var." and "Handoff Success" are ambiguous without units or definitions in the table caption. Define power variance (is this coefficient of variation? standard deviation as percentage of mean?) and specify what constitutes a handoff "success."

4. **Section IV-E, Eq. 7.** The power overhead calculation assumes exactly one coordinator per cluster at all times. During handoffs, two nodes may simultaneously operate in coordinator mode, briefly doubling the overhead. This transient effect should be noted.

5. **Section V-A.** The model version numbers (Claude 4.6, Gemini 3 Pro, GPT-5.2) do not correspond to publicly known model versions. Clarify whether these are internal designations, future versions, or errors.

6. **Section II-C.** The claim that Li et al. [19] "establishes bounds" on propagation time with "$O(\log N)$ propagation time" for hierarchical topologies conflates the specific result of that paper (GNN-based path planning) with general hierarchical propagation bounds. The $O(\log N)$ result for tree-depth propagation is elementary and does not require this citation.

7. **Section III-A.** "The simulation clock operates at one-second resolution for collision avoidance events and one-minute resolution for routine coordination"—how are events at different resolutions interleaved? Is there a priority queue with mixed granularity? This implementation detail affects correctness.

8. **Table II.** The "Failure Mode" column uses qualitative descriptors ("Single point," "Graceful," "Excellent") rather than quantitative metrics. Replace with or supplement with quantitative availability figures from the simulation.

9. **Typo/style.** Section I-A: "foremost unsolved challenges" is hyperbolic—coordination at $10^4$ nodes is solved (Starlink operates). The unsolved challenge is at $10^5$+ nodes.

10. **Missing figure files.** All eight figures are referenced but no PDF files are provided. The review is based solely on captions and textual descriptions.

## Overall Recommendation

**Major Revision**

The paper addresses a timely and important problem—scaling coordination architectures for mega-constellations and beyond—and presents a well-structured simulation study with commendably transparent discussion of limitations. The AI-assisted exploration section sets an excellent standard for ethical disclosure. However, the asymmetric comparison between topologies (worst-case centralized vs. optimized hierarchical), the debatable mesh parameterization, the insufficient statistical support for the claimed inflection point, and the absence of validation against real systems collectively undermine the paper's central claims. The communication model abstractions are too severe for the quantitative conclusions drawn. The core finding—that hierarchical architectures scale better than centralized or flat mesh—is well-known in distributed systems theory, and the paper needs to more clearly articulate what is genuinely new beyond confirming this expectation in a space systems context. With substantial revisions addressing the asymmetric comparison, finer-grained inflection point analysis, realistic communication modeling, and some form of validation, this could become a solid contribution to IEEE T-AES.

## Constructive Suggestions

1. **Equalize the comparison.** Simulate the centralized topology with $c \in \{1, 10, 100, 1000\}$ parallel servers and the mesh topology with both global and local-only gossip variants. Present all results together so readers can see where the hierarchical advantage genuinely emerges versus where it is an artifact of parameterization choices. This would transform the paper from "hierarchical wins" (predictable) to "here is the precise crossover point as a function of parallelization and gossip scope" (novel and useful).

2. **Develop the inflection point analysis rigorously.** Add simulation runs at 8–10 additional fleet sizes in the $10^4$–$10^5$ range. Apply formal change-point detection (e.g., Bayesian change-point analysis or segmented regression) and report the threshold location with confidence intervals as a function of the key parameters ($r$, $k_c$, link capacity). Derive an approximate analytical expression for the threshold, enabling designers to compute it for their specific configurations without running the full simulation.

3. **Add a realistic communication layer.** Incorporate at minimum Earth occlusion (nodes in LEO cannot communicate when the Earth blocks line-of-sight) and a simple link availability model. Show how the overhead results change when link availability drops from 100% to realistic values. This would dramatically increase the paper's credibility for the space systems community.

4. **Validate against Starlink or another real constellation.** Even a limited validation—showing that the model's predicted overhead at $N = 7000$ is consistent with publicly available information about Starlink's ground infrastructure requirements, or that the predicted latency distributions match reported conjunction avoidance response times—would significantly strengthen the paper's claims.

5. **Sharpen the novelty claim.** Rather than claiming hierarchical coordination is "the only viable topology" (which is both overstated and unsurprising), reframe the contribution around the quantitative design guidelines: the optimal cluster size range, the duty cycle Pareto analysis, and the parameter-dependent threshold. These are the genuinely useful outputs for system designers, and they deserve to be the headline contribution.