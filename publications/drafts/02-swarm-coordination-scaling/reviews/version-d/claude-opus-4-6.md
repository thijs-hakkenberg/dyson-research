---
paper: "02-swarm-coordination-scaling"
version: "d"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-23"
recommendation: "Major Revision"
---

# Peer Review: "Scaling Hierarchical Coordination for Million-Unit Space Swarms"

**Manuscript Version:** D
**Venue:** IEEE Transactions on Aerospace and Electronic Systems

---

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a genuinely important gap: no prior work has systematically compared coordination architectures across the $10^3$–$10^6$ node range using quantitative simulation. The scaling challenge for mega-constellations is real and timely, with Starlink approaching 7,000 nodes and approved for 42,000. The research questions are well-motivated and the problem framing is compelling. The identification of a parameter-dependent superlinear scaling regime and the practical design guidelines (cluster size 50–100, duty cycle 24–48 hours) have clear near-term applicability.

However, the novelty is tempered by several factors. The conclusion that hierarchical architectures scale better than flat centralized or full-mesh topologies is well-established in distributed systems theory (as the authors themselves acknowledge, citing Lynch). The $O(N)$ vs. $O(N^2)$ vs. $O(N)$-with-bottleneck comparison is essentially a restatement of known complexity results instantiated with space-relevant parameters. The paper's primary novelty lies in the quantitative parameterization for space systems and the duty-cycle/cluster-size optimization, which, while useful, represent incremental rather than fundamental contributions. The AI-assisted design exploration in Section V-B, while transparently disclosed, does not constitute a validated contribution and the authors appropriately caveat it. The Shepherd/Flock concept, while interesting, is not simulated and remains speculative.

The paper would benefit from a clearer articulation of what is genuinely new versus what is a known result applied to a new domain. The current framing occasionally overstates novelty—e.g., claiming "the first comparative discrete event simulation of coordination topologies at scales spanning three orders of magnitude" is technically true but somewhat misleading given that the qualitative outcome (hierarchy wins) is predictable from first principles.

## 2. Methodological Soundness

**Rating: 2 (Needs Improvement)**

The DES framework is reasonably well-described, and the authors deserve credit for providing a comprehensive parameter table (Table II), validation against closed-form solutions (M/D/1 and gossip bounds), and Monte Carlo analysis with bootstrap confidence intervals. The explicit queueing models for each topology level (Section III-B-2) are a strength of this version.

However, several methodological concerns are significant:

**Asymmetric topology parameterization.** This is the paper's most fundamental methodological issue. The centralized topology uses a deliberately pessimistic single-server model ($c=1$), while the hierarchical topology is parameterized with generous headroom ($\rho_c = 0.05$ at optimal cluster size). Although the authors acknowledge this in Section III-B-1 and Table I, the asymmetry propagates through all results tables and figures. The "fair" comparison would either use the same processing budget across topologies or present results for multiple values of $c$. The mesh topology is parameterized for global state convergence, which the authors justify with astrodynamics arguments, but this represents the most expensive possible mesh configuration. A sectorized mesh—acknowledged as "promising" but not simulated—would likely perform much closer to the hierarchical topology. The comparison thus pits the best-case hierarchical against worst-case centralized and worst-case mesh, which undermines the comparative conclusions.

**Physical-layer abstraction.** The authors acknowledge this limitation (Section V-E) but understate its severity. Earth occlusion causing 40–60% link unavailability in LEO is not a minor perturbation—it fundamentally changes the connectivity graph and would differentially affect the hierarchical topology (which depends on specific coordinator-to-coordinator links being available) versus the mesh topology (which can route around unavailable links). The claim that physical-layer effects are "approximately topology-neutral" is asserted without evidence and is likely incorrect. MAC-layer contention, link acquisition overhead, and Doppler effects would compound differently across topologies.

**Sparse data for key claims.** The superlinear scaling regime is identified from only five data points (Table V). The authors commendably acknowledge this (Section IV-D), but the claim still appears in the abstract, contributions list, and conclusion as a finding rather than a hypothesis. With $R^2 > 0.99$ for a linear fit below 50,000 nodes and only two points above, the evidence for superlinearity is weak. The recommended intermediate fleet sizes for future work should have been simulated in this study.

**Collision avoidance rate.** The rate of $10^{-4}$/node/s (Table II footnote) is stated to include "all proximity monitoring events" but is not derived from orbital mechanics. For a dense shell of $10^6$ objects, conjunction rates depend critically on orbital geometry, relative velocities, and screening volume—none of which are modeled. This parameter significantly affects the results (collision avoidance drives the most time-critical coordination requirements) and its justification is insufficient.

## 3. Validity & Logic

**Rating: 3 (Adequate)**

The logical structure of the argument is generally sound, and the authors are notably transparent about limitations—Section V-E is one of the most honest limitations sections I have reviewed. The distinction between baseline telemetry and protocol overhead (Section III-F) is well-articulated and prevents a common source of confusion. The treatment of information completeness vs. coordination capability (Table III) is a valuable contribution that adds nuance to the topology comparison.

The conclusions are broadly supported by the simulation results within the stated assumptions, but several logical issues merit attention:

**Circular reasoning in mesh parameterization.** The argument for $O(N^2)$ mesh overhead rests on the claim that "each node must maintain awareness of trajectories beyond its immediate orbital neighborhood" for fleet-wide collision avoidance. But the hierarchical topology achieves fleet-wide coordination through aggregated summaries—precisely the kind of reduced-fidelity information that a sectorized mesh could also use. The paper effectively argues that the mesh must provide full per-node state while the hierarchy can use aggregated state, then concludes the hierarchy is more efficient. This is true by construction rather than by analysis. The authors partially address this in the "Information completeness" discussion, but the asymmetry still biases the comparison.

**Duty cycle analysis.** The inverse relationship between duty cycle duration and handoff success rate (Table IV) is counterintuitive as presented. Longer duty cycles mean fewer handoffs, so the per-handoff success rate should be independent of duty cycle duration (it depends on link quality and state size, not frequency). The 95% success rate at 1-hour cycles vs. 99.9% at 7-day cycles is explained as cumulative daily probability, but this conflates per-event reliability with system-level reliability in a way that could mislead. The explanation in Section IV-C partially clarifies this, but Table IV should report per-handoff success rates consistently.

**Power budget analysis.** Equation (8) correctly computes the average power overhead but the analysis neglects the peak power constraint. During coordinator duty, a node must sustain 15–20W, which is 3–4× the baseline. This requires the power system (solar arrays, batteries) to be sized for the coordinator case, meaning every node carries the mass penalty of coordinator-capable hardware—precisely the motivation for the Shepherd/Flock concept. This tension is not adequately explored.

## 4. Clarity & Structure

**Rating: 4 (Good)**

The paper is well-organized and clearly written. The progression from problem statement through simulation framework to results and discussion follows a logical arc. The abstract accurately summarizes the findings with appropriate caveats. Tables and figures are well-designed and informative, with consistent formatting and clear captions. The explicit separation of baseline telemetry from protocol overhead throughout the paper prevents confusion.

Several specific clarity issues:

The paper is long for a journal article (approximately 12 pages of dense content). Some material could be condensed without loss—particularly the related work section (Section II), which at nearly two pages provides more context than necessary for the IEEE T-AES audience. The discussion of bio-inspired optimization (Section II-B, second paragraph) and mean-field game theory (Section II-C, second paragraph) are tangential and could be cut.

The notation is generally consistent, but the use of $O_{\text{protocol}}$ as both a percentage and a conceptual quantity creates minor ambiguity. The paper would benefit from a notation table.

Section V-B (AI-Assisted Design Exploration) is appropriately caveated but feels out of place in a rigorous simulation study. Its inclusion may actually weaken the paper's credibility with the T-AES audience, despite the transparent disclosure. Consider moving it to an appendix or removing it entirely, retaining only the Shepherd/Flock concept as a "future work" item motivated by the DES results alone.

## 5. Ethical Compliance

**Rating: 5 (Excellent)**

The paper sets a high standard for AI disclosure in academic publishing. Section V-B explicitly describes the AI tools used (Claude 4.6, Gemini 3 Pro, GPT-5.2), the methodology (structured multi-model deliberation), and the limitations (shared training corpora, priming effects, sycophantic alignment). The Acknowledgment section reiterates this disclosure. The authors appropriately characterize the AI output as "generative design ideation, not independent engineering verification" and note that the models were "primed with simulation results."

The anonymous authorship ("Project Dyson Research Team") with a note that individual names will be provided for final publication is unusual but acceptable per IEEE policy. The data availability statement with a GitHub repository link (pending commit hash) supports reproducibility. No conflicts of interest are apparent, though the affiliation with "Project Dyson" should be clarified—is this an academic institution, a nonprofit, or a commercial entity? This matters for assessing potential conflicts.

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is appropriate for IEEE T-AES in scope, addressing autonomous spacecraft coordination with direct relevance to mega-constellation operations. The reference list is comprehensive (42 references) and spans the relevant literature from distributed systems theory through swarm robotics to constellation operations.

However, several referencing issues exist:

**Missing key references.** The paper does not cite several directly relevant works: (1) Del Portillo et al.'s analysis of mega-constellation capacity and interference, which is directly relevant to the spectrum scarcity argument; (2) Akyildiz et al.'s work on inter-satellite link networking architectures; (3) any of the substantial literature on delay-tolerant networking (DTN) for space, which addresses many of the same coordination challenges under intermittent connectivity; (4) the CCSDS standards for space networking beyond Prox-1 (e.g., DTN Bundle Protocol, CCSDS File Delivery Protocol).

**Reference quality.** Several references are to websites, press releases, or non-peer-reviewed sources (refs [1], [3], [4], [20], [22], [35]). While some of these (SpaceX, DARPA) are difficult to replace with peer-reviewed sources, the NRL reference [20] is explicitly noted as "magazine article, non-peer-reviewed" and should be replaced or supplemented. Reference [38] is to a "manuscript in preparation" by the same group, which cannot be verified by reviewers.

**Temporal currency.** The constellation operations references are reasonably current (2017–2024), but the distributed systems foundations are dated (Lamport 1978, Kleinrock 1975, Demers 1987). While these are foundational, the paper should also cite more recent work on scalable consensus (e.g., HotStuff, Tendermint) and modern gossip protocols that have improved on the classical bounds.

---

## Major Issues

1. **Asymmetric topology parameterization undermines the central comparative claim.** The centralized topology uses $c=1$ (worst case), the mesh uses global state convergence (worst case), while the hierarchical topology is parameterized with comfortable headroom. Although acknowledged, this asymmetry propagates through all results. **Required action:** Either (a) simulate the centralized topology with $c \in \{1, 10, 100\}$ and present results for all, showing where the crossover with hierarchical occurs; or (b) simulate a sectorized mesh variant; or (c) reframe the paper's contribution as "characterizing hierarchical coordination" rather than "comparing topologies," since the comparison is not conducted on equal footing.

2. **Insufficient evidence for the superlinear scaling regime.** Five data points cannot support the claim of a "superlinear scaling regime near 50,000 nodes" that appears in the abstract, contributions, and conclusion. **Required action:** Either simulate at the intermediate fleet sizes already identified (20k, 30k, 40k, 60k, 70k, 80k) and perform formal change-point analysis, or substantially downgrade this claim to a preliminary observation requiring further investigation.

3. **Physical-layer effects are not topology-neutral and this matters.** The assertion that Earth occlusion, MAC contention, and link acquisition overhead affect all topologies equally is unsubstantiated and likely incorrect. The hierarchical topology's dependence on specific coordinator links makes it more vulnerable to targeted link outages than the mesh topology. **Required action:** At minimum, conduct a sensitivity analysis with stochastic link availability (e.g., Bernoulli model with $p = 0.5$ for LEO occlusion) to verify the relative topology ordering holds. Alternatively, clearly state that the results apply only under the idealized full-connectivity assumption and that the topology ranking may change under realistic link conditions.

4. **The collision avoidance event rate is unjustified.** The $10^{-4}$/node/s rate is a critical parameter (it drives the most time-sensitive coordination requirements) but is not derived from orbital mechanics or calibrated against operational data. **Required action:** Either derive this rate from conjunction screening analysis for a representative orbital shell, calibrate against published conjunction data (e.g., from the 18th Space Defense Squadron), or conduct a sensitivity analysis showing results are robust to order-of-magnitude variation in this parameter.

---

## Minor Issues

1. **Section III-B-2, Eq. (4):** The message count $M_{\text{total}} = N + N/k_c + N/(k_c \cdot k_r)$ omits downward command messages. The text notes this but the equation should either include both directions or be explicitly labeled as "upward reporting only."

2. **Table IV:** The "Handoff Success" column conflates per-event and cumulative reliability metrics. The 95% at 1-hour duty cycle appears to be a daily cumulative figure (24 handoffs × 99.8% per handoff ≈ 95.3%), while the 99.9% at 7-day is a per-event figure. These should be reported on a consistent basis.

3. **Section III-A:** "One-second resolution applies only to collision avoidance events" — this dual-resolution approach should be validated. Does the 60-second resolution for routine events miss any timing-sensitive interactions?

4. **Section IV-E, Eq. (8):** The denominator should be the number of nodes in the cluster, not the duty cycle period. The equation is correct but the preceding text ("each node serves as coordinator approximately 1% of the time") conflates time fraction with power fraction in a potentially confusing way.

5. **Table II:** The "Optical ISL capacity" of 1–10 Gbps is used only for handoff state transfer. Clarify whether routine inter-node communication also uses optical ISLs or a separate RF link.

6. **Section II-C:** The claim that Tolstaya et al.'s GNN result "provides a theoretical lower bound on communication overhead achievable by any distributed coordination scheme" is incorrect. It provides an achievable bound for GNN controllers, not a lower bound for all schemes.

7. **Abstract:** "addressable via parallelization" in parentheses is awkward. Consider restructuring.

8. **Section V-B:** References to "Claude 4.6," "Gemini 3 Pro," and "GPT-5.2" — these model version numbers do not correspond to any publicly released models as of mid-2025. If these are internal/beta versions, this should be noted; if they are fictional/projected, this is problematic.

9. **Bibliography:** Reference [38] (dyson_multimodel) is "manuscript in preparation" and cannot be verified. Either provide a preprint or remove the citation.

10. **Section III-E:** "Wall-clock runtime ranges from approximately 2 minutes for $N = 10^3$... to approximately 18 hours for $N = 10^6$" — this suggests the simulation complexity is superlinear in $N$, which should be explained (is it $O(N \log N)$ from the event queue? $O(N^2)$ from pairwise interactions?).

---

## Overall Recommendation

**Major Revision**

This paper addresses an important and timely problem with a reasonable simulation-based approach, and the authors demonstrate commendable transparency about limitations, AI usage, and the bounds of their conclusions. However, the central comparative claim—that hierarchical coordination is superior—rests on an asymmetric parameterization that favors the hierarchical topology by construction. The superlinear scaling regime, prominently featured in the abstract and contributions, is supported by insufficient data. The physical-layer abstraction, while acknowledged, may not be topology-neutral as claimed, potentially invalidating the relative topology ranking. These issues require substantial additional simulation work (multi-server centralized, sectorized mesh, stochastic link availability, intermediate fleet sizes) before the comparative conclusions can be considered robust. The paper's strengths—clear writing, honest limitations discussion, practical design guidelines, and thorough parameter documentation—provide a strong foundation for a significantly improved revision.

---

## Constructive Suggestions

1. **Equalize the comparison.** Simulate the centralized topology with $c = 10$ and $c = 100$ parallel servers, and simulate a sectorized mesh variant with local gossip + hierarchical inter-sector aggregation. Present all results together so readers can see where genuine architectural crossovers occur. This would transform the paper from "hierarchy is best" (predictable) to "here is the Pareto frontier across topologies as a function of ground infrastructure investment and coordination fidelity requirements" (novel and useful).

2. **Fill in the scaling curve.** Add simulation runs at $N \in \{20\text{k}, 30\text{k}, 40\text{k}, 60\text{k}, 70\text{k}, 80\text{k}\}$ and perform formal change-point detection (e.g., Bayesian change-point analysis or piecewise linear regression with AIC/BIC model selection). This would either confirm or refute the superlinear regime with statistical rigor and would be a genuinely novel empirical contribution.

3. **Add stochastic link availability.** Even a simple Bernoulli link model ($p_{\text{available}} = 0.5$ for LEO, varying by topology-specific link criticality) would dramatically strengthen the paper's applicability claims. Show whether the hierarchical topology's advantage persists when coordinator-to-coordinator links experience realistic outage rates.

4. **Derive or calibrate the collision avoidance rate.** Use published conjunction data (e.g., ESA's annual space environment report) to estimate per-node conjunction screening rates for a dense LEO shell. Alternatively, sweep this parameter over two orders of magnitude and show the results are qualitatively robust.

5. **Consider removing or relegating Section V-B.** The AI-assisted design exploration, while transparently disclosed, adds little to the paper's core contribution and may reduce credibility with the T-AES audience. The Shepherd/Flock concept can be motivated entirely from the DES results (coordinator power/processing requirements differ from standard nodes → specialize the hardware) without invoking LLM deliberation. Move the AI methodology to a supplementary appendix if the authors wish to preserve it for completeness.