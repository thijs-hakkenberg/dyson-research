---
paper: "02-swarm-coordination-scaling"
version: "f"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-23"
recommendation: "Major Revision"
---

# Peer Review: "Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study"

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a genuine gap in the literature: the systematic comparison of coordination architectures across the $10^3$–$10^6$ node range for autonomous space systems. The authors correctly identify that swarm robotics literature rarely exceeds ~1,000 agents and constellation management literature rarely exceeds ~10,000 nodes, leaving the intermediate regime largely unexplored. The research questions are well-motivated and the problem is timely given the growth trajectories of Starlink, Kuiper, and OneWeb.

However, the novelty is tempered by several factors. The finding that hierarchical architectures scale better than flat centralized or fully-connected mesh topologies is well-established in distributed systems theory (the authors themselves cite Lynch [7] for the $O(\log N)$ propagation time result). The primary contribution is therefore quantitative characterization rather than architectural innovation. While quantification has value, the results are obtained under idealized conditions that abstract away the very physical-layer effects (Earth occlusion, MAC contention, pointing overhead) that make the space domain uniquely challenging. The three "optimizations" in Section IV-D (exception-based telemetry, dynamic spatial partitioning, heterogeneous hardware) are modeled analytically rather than simulated—substantially weakening the claim that they "restore overhead to acceptable levels." The paper would be significantly more novel if it either (a) proposed and validated a new coordination protocol, or (b) incorporated realistic space link physics into the simulation.

The applicability discussion (Section V-A) is broad but shallow—claiming relevance to mega-constellations, military drones, IoT, and autonomous vehicles without deep engagement with any of these domains. This breadth dilutes the contribution's impact for the T-AES readership, who would benefit more from deeper treatment of the space-specific aspects.

## 2. Methodological Soundness

**Rating: 2 (Needs Improvement)**

The discrete event simulation framework is described at a reasonable level of detail, and the Monte Carlo approach with 50–100 runs per configuration is appropriate. The parameter table (Table II) supports reproducibility, and the validation against Pollaczek-Khinchine and gossip convergence bounds (Section III-A) is a positive step. However, several methodological concerns are significant.

**The comparison is structurally unfair.** The centralized baseline uses a deliberately worst-case single-server model ($c=1$), while the hierarchical architecture is optimized across multiple parameters ($k_c$, $\tau_d$). Although the authors acknowledge this in Section V-E and Table I, the framing throughout the paper—particularly in the abstract, Table III, and Fig. 2—presents the comparison as if the three architectures are on equal footing. The $M/D/c$ sensitivity analysis (Table I) is a welcome addition but is not carried through to the results: the overhead comparison in Table III still uses $c=1$. A fair comparison would show the centralized baseline at $c=100$ alongside the hierarchical results, since a "dedicated ground station cluster" is a realistic deployment for a $10^6$-node constellation.

**The global-state mesh baseline is a straw man.** The requirement that every node maintain full trajectory state for all $O(N)$ peers is an extreme assumption. The authors acknowledge this (Section III-B-3, Table II) and discuss the sectorized mesh alternative, but do not simulate it. Since the sectorized mesh would likely achieve $O(N^{1.5})$ or better scaling while providing trajectory-level accuracy (which the hierarchical architecture sacrifices), its omission leaves a critical gap in the comparison. The information completeness discussion (Table II) is appreciated but insufficient—the architectures provide fundamentally different coordination capabilities, making overhead comparison alone misleading.

**Physical-layer abstraction is too aggressive.** The authors estimate that unmodeled effects could increase overhead by 2–4× (Section V-E). A factor of 2–4× is not a minor correction—it could shift the hierarchical architecture's overhead from 8% to 16–32% at $10^6$ nodes, fundamentally changing the conclusions. The claim that these effects are "approximately topology-neutral" is asserted but not demonstrated. The hierarchical architecture concentrates traffic at coordinator nodes, making it more vulnerable to link unavailability at those specific points, as the authors themselves note. At minimum, a stochastic link availability model should be incorporated.

**The superlinear transition analysis is unconvincing.** The claim of a "gradual superlinear scaling transition between 30,000 and 60,000 nodes" (Section IV-D) is based on overhead values that increase from 3.3% to 4.8% across this range (Table V). Given that 95% CIs are reported as "within ±5% of reported means," the actual confidence intervals overlap substantially across adjacent data points. For example, at $N=30,000$ the overhead is $3.3\% \pm 0.165\%$ and at $N=40,000$ it is $3.6\% \pm 0.18\%$—these intervals overlap. The $R^2 > 0.99$ claim for the linear fit below 50,000 nodes is not independently verifiable and seems implausibly high given the stochastic nature of the simulation. The per-tier message decomposition (Fig. 6) is a valuable diagnostic, but the claim that "inter-cluster coordination grows superlinearly" needs formal statistical testing (e.g., comparison of linear vs. power-law fits with AIC/BIC).

**Collision avoidance rate parameterization.** The $10^{-4}$/node/s rate is justified by a 1,000:1 screening-to-maneuver ratio, but this ratio is for current operations with ~7,000 LEO objects. In a dense swarm of $10^6$ nodes, the conjunction rate per node would scale with local density, potentially increasing the screening rate by orders of magnitude. The sensitivity analysis (varying from $10^{-5}$ to $10^{-3}$) is helpful but does not address density-dependent scaling.

## 3. Validity & Logic

**Rating: 3 (Adequate)**

The logical structure of the paper is generally sound: reference baselines are established, the hierarchical architecture is characterized, and optimizations are proposed for the superlinear regime. The authors are commendably transparent about limitations (Section V-E) and the conditional nature of their results ("under the parameterization described herein" appears frequently).

However, several logical issues merit attention. First, the abstract and conclusion claim that hierarchical coordination "maintains protocol overhead ranging from 2% at $10^3$ nodes to 8% at $10^6$ nodes," but Table V shows 10% overhead at $5 \times 10^5$ nodes. The 8% figure at $10^6$ apparently comes from the "optimized" curve in Fig. 5, which uses analytically projected (not simulated) optimizations. This conflation of simulated and projected results is misleading and should be clearly distinguished throughout.

Second, the $O(N^2)$ characterization of the global-state mesh (Eq. 5) contains a logical gap. The authors argue that fanout $f = O(N/\log N)$ is required for convergence in $O(\log N)$ rounds, but this assumes all $N$ state entries must be disseminated within a fixed number of rounds. In practice, trajectory updates have different staleness tolerances depending on conjunction geometry—nearby nodes need fresh data while distant nodes can tolerate stale data. The $O(N^2)$ bound thus represents a worst case that is unlikely to be operationally required.

Third, the coordinator bandwidth analysis (Section III-F) reveals that a cluster coordinator requires ~20.5 kbps inbound while each node has only 1 kbps allocated. The resolution—assuming coordinators use the "combined coordination bandwidth of its cluster"—is physically reasonable but represents a significant departure from the stated per-node bandwidth model. This shared-bandwidth assumption should be stated as a simulation parameter, not buried in explanatory text.

The limitations section is thorough and honest, which strengthens the paper's credibility. The acknowledgment that the three optimizations are "modeled analytically rather than implemented as discrete event mechanisms" is appropriately candid.

## 4. Clarity & Structure

**Rating: 4 (Good)**

The paper is well-organized and generally well-written. The progression from problem statement through related work, simulation framework, results, and discussion follows a logical arc. The extensive use of tables (seven total) and figures (seven total) supports the narrative effectively. The abstract is detailed and accurately represents the paper's content, though it is somewhat long for IEEE T-AES standards.

Several specific clarity issues should be addressed. The overhead definition (Section III-F) is explained at considerable length but remains confusing due to the dual-component structure (baseline telemetry + protocol overhead). The reader must constantly remember that reported percentages exclude the 20.5% baseline. A single, clearly defined metric reported consistently would be preferable—or at minimum, a table showing total overhead (baseline + protocol) alongside protocol-only overhead for each configuration.

The related work section (Section II) is comprehensive—perhaps excessively so. At approximately 1.5 pages, it covers constellation operations, swarm robotics, mathematical foundations, and military programs. Some of this material (e.g., the discussion of ant colony optimization, particle swarm optimization, and artificial bee colony algorithms) has only tangential relevance and could be condensed. The mathematical foundations subsection, however, is well-curated and directly relevant.

The notation is generally consistent, though the use of $O_{\text{protocol}}$ in tables versus "protocol overhead" in text could be more uniform. Equation numbering is sequential and references are correct. The figures are described but not provided (as expected for a LaTeX source review); the captions are informative and self-contained.

One structural concern: the paper is quite long for a journal article. The combination of three topology models, parameter sweeps across four dimensions, duty cycle analysis, superlinear transition characterization, and three optimization proposals creates a broad but shallow treatment. Focusing on fewer contributions with deeper analysis would strengthen the paper.

## 5. Ethical Compliance

**Rating: 4 (Good)**

The paper includes a transparent acknowledgment of AI-assisted ideation (Acknowledgment section), specifying the models used (Claude 4.6, Gemini 3 Pro, GPT-5.2) and the nature of their contribution (architectural concept generation). The disclosure that the "Shepherd/Flock" concept was AI-generated but "not validated in the current study" is appropriately scoped. The reference to a companion methodology paper [42] provides an audit trail.

The author attribution ("Project Dyson Research Team" with a note that individual names will be provided for final publication) is unusual but acceptable for initial submission. The data availability statement with a GitHub repository link supports reproducibility, though the commit hash is listed as "[PENDING]."

One concern: the AI models cited (Claude 4.6, GPT-5.2) do not correspond to any publicly released versions as of mid-2025, suggesting either future-dated references or internal/beta versions. This should be clarified.

The dual-use implications of the military drone swarm discussion (Sections II-D, V-A) are not explicitly addressed but are within normal bounds for T-AES publications.

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is appropriate for IEEE T-AES in its treatment of autonomous spacecraft coordination, though the breadth of claimed applications (IoT, autonomous vehicles, drone swarms) dilutes the aerospace focus. The references are generally relevant and span the appropriate literature, including foundational distributed systems work (Lamport, Lynch), swarm robotics (Brambilla, Dorigo), and space systems (Wertz, Castet).

However, several referencing concerns exist. First, a significant number of references are non-archival (SpaceX website, Amazon website, DARPA program pages, DoD fact sheets). While some of these are unavoidable for current operational systems, the paper would benefit from replacing non-archival sources with peer-reviewed alternatives where possible. Second, the reference list omits several directly relevant works: (a) Radhakrishnan et al.'s survey of inter-satellite link architectures for small satellite systems; (b) the extensive literature on hierarchical task allocation in multi-robot systems (e.g., Korsah et al., 2013); (c) recent work on distributed space situational awareness; and (d) the CCSDS Spacecraft Onboard Interface Services (SOIS) standards, which address inter-spacecraft communication protocols.

Third, the self-citation [42] to a "companion methodology paper" hosted on the project's own website is not peer-reviewed and should not be cited as a primary reference. If the AI methodology is important enough to cite, it should be submitted for peer review independently.

The paper does not cite any work on actual distributed satellite operations beyond Iridium (1995), which is nearly 30 years old. More recent distributed operations experience from missions like ESA's Cluster, MMS, or the various CubeSat swarm demonstrations would strengthen the grounding.

---

## Major Issues

1. **Unfair baseline comparison.** The centralized baseline at $c=1$ is a deliberate worst case, while the hierarchical architecture is fully optimized. The results section should include centralized performance at $c=10$ and $c=100$ in all comparison tables and figures, not just in the sensitivity table (Table I). Without this, the claimed advantage of hierarchical coordination is overstated.

2. **Analytically projected optimizations presented as simulation results.** The abstract states "protocol overhead ranging from 2% at $10^3$ nodes to 8% at $10^6$ nodes," but the 8% figure at $10^6$ comes from the analytically projected "optimized" curve, not from DES. The unoptimized DES result at $5 \times 10^5$ is already 10% (Table V), and $10^6$ is not shown in the table. This conflation must be resolved—either by clearly separating simulated from projected results in all summaries, or by implementing the optimizations in the DES.

3. **Physical-layer abstraction undermines quantitative claims.** The authors' own estimate of 2–4× overhead increase from unmodeled effects means that all reported overhead percentages have an uncertainty factor of 2–4×. This is not a minor limitation—it means the hierarchical architecture could exceed the 10% "operationally significant" threshold at scales well below $10^6$ nodes. At minimum, a sensitivity analysis with a simple stochastic link availability model (e.g., 50% duty cycle to represent Earth occlusion) should be included.

4. **Statistical rigor of superlinear transition claim.** The transition between 30,000 and 60,000 nodes is the paper's most specific empirical contribution, but it is not supported by formal statistical testing. The overlapping confidence intervals across adjacent data points, combined with the unverifiable $R^2$ claim, weaken this finding. Formal model comparison (linear vs. power-law vs. piecewise-linear) with appropriate information criteria is needed.

5. **Missing sectorized mesh simulation.** The authors identify the sectorized mesh as a "priority candidate for future simulation" (Section V-C) and acknowledge it would "closely resemble the hierarchical architecture." This admission undermines the paper's central comparison: if the most practical decentralized alternative was not simulated, the claim that hierarchical coordination is superior to decentralized approaches is unsupported. Either simulate the sectorized mesh or substantially qualify the comparative claims.

## Minor Issues

1. **Abstract length.** At approximately 250 words, the abstract exceeds typical IEEE T-AES guidelines (~150–200 words). Consider condensing.

2. **Eq. (2):** The Pollaczek-Khinchine formula as written ($W_q = \rho / [2\mu(1-\rho)]$) is the $M/D/1$ waiting time, but the text references it as the $M/D/1$ mean waiting time without noting it applies only to the waiting time in queue (not total sojourn time). Clarify.

3. **Table V, "Status" column.** Labels like "Nominal," "Transition," and "Requires optimization" are subjective and not defined. Either define threshold criteria or remove this column.

4. **Section III-A:** "one-second resolution applies only to collision avoidance events, while all other events use one-minute resolution"—this dual-resolution scheme could introduce artifacts at the boundary. Was sensitivity to clock resolution tested?

5. **Section III-B-2:** "Eq. 4 counts uplink (node-to-coordinator) reporting only; total bidirectional overhead is approximately 1.5–2× the reported values"—this factor should be incorporated into the reported results rather than noted as a caveat.

6. **Section IV-E, Eq. (8):** The power overhead calculation assumes uniform rotation, but the text elsewhere discusses heterogeneous hardware where dedicated coordinators would not rotate. Clarify which scenario the calculation applies to.

7. **Reference [1]:** "accessed February 2026" appears to be a future date. Verify.

8. **Table IV, footnote b:** "Probability that coordinator state transfer completes without error within the allocated handoff window"—what is the allocated handoff window duration? This parameter is not specified.

9. **Fig. 1 caption:** References "10–100 regional coordinators" and "10–100 cluster coordinators," but the text uses specific values ($k_c = 50$–$500$, $k_r$ not explicitly bounded). Reconcile.

10. **Section III-F:** The coordinator bandwidth resolution (shared cluster bandwidth) should be formalized as a simulation parameter in Table II rather than explained in prose.

## Overall Recommendation

**Major Revision**

The paper addresses a timely and relevant problem—scaling coordination architectures for large autonomous space systems—and provides a reasonably well-structured simulation study. The identification of the superlinear transition regime and the cluster size/duty cycle optimization are useful contributions. However, the structurally unfair baseline comparison, the conflation of simulated and analytically projected results, the aggressive physical-layer abstraction (with the authors' own 2–4× uncertainty estimate), and the insufficient statistical support for the superlinear transition claim collectively prevent acceptance in the current form. The omission of the sectorized mesh—acknowledged by the authors as the most natural competitor to the hierarchical architecture—is a significant gap. A major revision incorporating (1) fair multi-server centralized baselines in all comparisons, (2) clear separation of simulated vs. projected results, (3) at minimum a stochastic link availability model, and (4) formal statistical testing of the scaling transition would substantially strengthen the contribution.

## Constructive Suggestions

1. **Implement a simple stochastic link model.** Even a Bernoulli link availability model with 50% duty cycle (representing Earth occlusion) applied uniformly to all topologies would dramatically strengthen the paper's claims. If the topology ranking is preserved under this model, the paper's conclusions become much more robust. If not, that is itself an important finding.

2. **Run the centralized $M/D/c$ baseline at $c=100$ through the full DES.** Present the results alongside the hierarchical architecture in all comparison tables and figures. This would transform the comparison from "hierarchical beats a straw man" to "hierarchical provides advantages even against a well-resourced centralized alternative"—a much stronger claim if it holds.

3. **Implement at least one of the three optimizations in the DES.** Exception-based telemetry is the simplest to implement (replace periodic reporting with threshold-triggered reporting) and would convert the most important projected result into a simulated one. This single change would substantially increase the paper's credibility.

4. **Apply formal model selection to the superlinear transition.** Fit linear, power-law ($aN^b$), and piecewise-linear models to the overhead data. Report AIC/BIC values and confidence intervals on the breakpoint location. This would either confirm the transition with statistical rigor or reveal that the data are insufficient to distinguish between models—either outcome is informative.

5. **Narrow the scope and deepen the analysis.** The paper attempts to cover too much ground (three topologies, four-dimensional parameter sweep, three optimizations, four application domains). Consider focusing on the hierarchical architecture alone, with the centralized and mesh baselines presented briefly as bounds, and devoting the freed space to deeper analysis of the physical-layer sensitivity and the superlinear transition mechanism.