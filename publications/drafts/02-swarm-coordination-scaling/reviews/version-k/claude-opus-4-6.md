---
paper: "02-swarm-coordination-scaling"
version: "k"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-24"
recommendation: "Major Revision"
---



# Peer Review: "Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study"

**Manuscript Version:** K
**Venue:** IEEE Transactions on Aerospace and Electronic Systems

---

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a genuinely important problem: how coordination architectures scale for autonomous spacecraft swarms in the $10^3$–$10^5$ range, a regime that is indeed under-explored in the literature. The motivation is timely given Starlink's expansion plans and emerging mega-constellation concepts. The paper correctly identifies that current swarm robotics literature rarely exceeds hundreds of agents, while constellation management literature has not systematically studied scaling properties across orders of magnitude.

However, the novelty is substantially undermined by the nature of the central result. The authors themselves acknowledge (Section IV-D) that the constant overhead ratio $\eta = O(1)$ is "a direct mathematical consequence of the hierarchical message structure—not a surprising emergent property." When the primary quantitative finding—that $O(N)/O(N) = O(1)$—is analytically trivial, the DES contribution reduces to confirming the constant factor (20.66%) and verifying the absence of second-order effects. The extremely low variance (SD < 0.001%) across Monte Carlo replications further suggests the simulation is essentially computing a deterministic formula with negligible stochastic perturbation, raising the question of what the DES adds beyond what a spreadsheet calculation would provide. The paper would benefit from identifying scenarios where the DES reveals genuinely non-obvious behavior—perhaps under correlated failures, dynamic topology changes, or realistic orbital mechanics—rather than confirming analytically predictable results.

The comparison framework, while carefully caveated, compares the hierarchical architecture against intentionally weak baselines (single-server centralized, global-state mesh). The authors are commendably transparent about this (Section I-C), but it limits the practical significance of the comparative claims. The absence of the sectorized mesh comparator—acknowledged as "priority future work"—is a meaningful gap, as this is arguably the most relevant competitor for the hierarchical approach.

## 2. Methodological Soundness

**Rating: 2 (Needs Improvement)**

There are several methodological concerns that require attention:

**Simulation fidelity vs. claims.** The paper repeatedly emphasizes "full-fidelity" simulation (abstract, Section III-E, Section IV-D), but the model abstracts away MAC-layer scheduling, link acquisition, pointing constraints, Doppler effects, orbital mechanics perturbations, and correlated failures. The term "full-fidelity" refers only to the fact that all $N$ nodes participate in every cycle (no sampling), which is a completeness property, not a fidelity property. This terminology is misleading and should be revised. A simulation that runs $N = 10^5$ nodes in 7 seconds of wall-clock time (Section III-E) is clearly operating at a very high level of abstraction—this is not a criticism per se, but the "full-fidelity" framing overstates the model's realism.

**Monte Carlo design.** Section III-D states "2–5 independent runs per configuration," while the abstract, Table III, and Section IV-D claim 30 replications. This inconsistency must be resolved. If 30 replications were used for the final results, the "2–5 runs" text in Section III-D appears to be a remnant from an earlier version and should be corrected. More fundamentally, when 30 replications produce SD < 0.001%, the stochastic component of the simulation is negligible, and the Monte Carlo framework is not meaningfully exercising the model's uncertainty. The authors should discuss what sources of variability the MC framework is intended to capture and whether 30 replications are justified given the near-deterministic outcomes.

**Queueing model validity.** The $M/D/1$ model for centralized processing assumes Poisson arrivals, but with a fixed reporting rate of $r = 0.1$ msg/s per node and deterministic cycle timing ($T_c = 10$ s), arrivals within each cycle are likely synchronized (all nodes report once per cycle), producing batch arrivals rather than Poisson arrivals. The $M/D/1$ model may significantly underestimate queueing delays for synchronized reporting. The authors should justify the Poisson assumption or use a $D/D/1$ or $D^{[N]}/D/1$ model.

**Link availability model.** The Bernoulli i.i.d. link loss model (Section IV-F) is acknowledged as a simplification, but it is a particularly poor model for LEO ISLs, where link outages are dominated by Earth occlusion (deterministic, periodic, and spatially correlated) and atmospheric effects (temporally correlated). The retransmission analysis (Eq. 7) assumes independent retry outcomes, which is invalid under correlated outages. The paper should either implement a more realistic link model or more prominently caveat that the link availability results are illustrative only.

**Exception-based telemetry validation.** Table VI validates that a Bernoulli($p_{\text{exc}}$) thinning of a deterministic message stream produces the expected fraction of messages—a result that is trivially correct by the law of large numbers. The "within 1% of analytical predictions" claim (abstract, contributions) overstates the significance of this validation. The interesting question—what $p_{\text{exc}}$ values are realistic for actual spacecraft state evolution—is not addressed.

## 3. Validity & Logic

**Rating: 3 (Adequate)**

The paper's conclusions are generally supported by the presented data, though several logical issues deserve attention:

The constant overhead result ($\eta = 20.66\%$) is internally consistent and well-documented across ten fleet sizes (Table V). However, the paper's framing sometimes implies this is a discovered property rather than a confirmed analytical prediction. The honest framing in Section IV-D ("not a surprising emergent property") should be the dominant narrative throughout, including in the abstract.

The coordinator bandwidth analysis (Section IV-G, Table VIII) is one of the paper's more valuable contributions, providing actionable engineering guidance. The identification of $\beta \geq 0.50$ for zero-drop operation and the MAC efficiency correction ($\gamma \approx 0.85$, yielding 59 kbps raw requirement) are useful design parameters. However, the analysis assumes a single coordinator serves all $k_c = 100$ members simultaneously within each $T_c$, which implicitly assumes a TDMA-like access scheme—yet the paper explicitly states that MAC-layer scheduling is not modeled. The offered-load analysis is necessary but not sufficient; a TDMA scheduling model within $T_c$ would strengthen these results considerably.

The duty cycle analysis (Table IV, Fig. 5) presents a reasonable multi-objective trade-off, but the inverse relationship between duty cycle and handoff success rate (Section IV-C) is not well justified. The claim that "cumulative probability of at least one handoff failure per day reaches 5% under our reliability model" at 1-hour duty cycles implies a per-handoff failure rate of approximately 0.2%, but Table IV reports 95% handoff success—these numbers are inconsistent unless "handoff success" in the table refers to something different from per-handoff completion probability. The metric definitions need clarification.

The paper appropriately acknowledges limitations (Section V-E), and the baseline interpretation note (Section I-C) is a commendable addition that prevents misinterpretation. The discussion of sectorized mesh (Section V-C) is thoughtful and correctly identifies the architectural convergence between sectorized mesh with inter-sector aggregation and the hierarchical topology.

## 4. Clarity & Structure

**Rating: 4 (Good)**

The paper is generally well-written and logically organized. The progression from problem statement through simulation framework to results and discussion follows a clear arc. The extensive use of tables for parameter documentation (Tables I–III) supports reproducibility. The traffic accounting table (Table III) and metric definitions (Section III-G) are particularly helpful for understanding exactly what is being measured.

Several structural issues merit attention. The paper is quite long for a journal article, and some material is repetitive. The constant overhead result ($\eta = 20.66\%$) is stated in the abstract, contributions list, Section IV-D (twice), Table V, and the conclusion—at least six times with nearly identical wording. The "full-fidelity" qualifier appears over a dozen times. Consolidating these repetitions would improve readability without sacrificing clarity.

The figures are referenced but provided as PDF placeholders (e.g., `fig-architecture-diagram.pdf`), so their quality cannot be assessed. The figure captions are detailed and informative. Fig. 3's caption appropriately flags the $10^6$-node curve as analytical extrapolation rather than DES-measured—this is good practice.

The abstract is comprehensive but long (approximately 250 words). It could be tightened by removing the parenthetical details (e.g., "SD < 0.001%", "$\beta \geq 0.50$") and focusing on the key findings at a higher level.

Section III-F (Communication Overhead Definition) is unusually detailed for a methods section and includes material that reads more like a response to reviewer comments than a self-contained exposition. The coordinator bandwidth pooling discussion, while important, could be streamlined.

## 5. Ethical Compliance

**Rating: 4 (Good)**

The paper includes an appropriate acknowledgment of AI-assisted ideation (Acknowledgment section), specifying the models used (Claude 4.6, Gemini 3 Pro, GPT-5.2) and the scope of their contribution (architectural concept generation, not validation). The disclaimer that the AI-generated "Shepherd/Flock" concept is "not validated in the current study" is appropriate. The reference to a companion methodology paper [44] provides a trail for readers interested in the AI-assisted design process.

The author attribution is unusual ("Project Dyson Research Team" with a footnote promising individual names for final publication). While this may be acceptable during review, IEEE policy generally requires named authors. The "Project Dyson" affiliation with a URL but no institutional affiliation raises questions about the research context—is this an academic group, a startup, or an independent research project? This should be clarified.

The data availability statement is commendable, though the commit hash is listed as "[PENDING]"—this should be populated before publication. The claim of reproducibility is strengthened by the detailed parameter tables and the promise of open-source code.

One concern: the paper references future model versions (Claude 4.6, GPT-5.2) and an access date of "February 2026" in multiple bibliography entries, suggesting either the paper is set in the near future or these are placeholder dates. This should be clarified or corrected.

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is appropriate for IEEE T-AES in its focus on autonomous spacecraft coordination, though the contribution leans more toward communication systems engineering than traditional aerospace content. The simulation framework, while applied to space systems, is essentially a message-passing network simulation with space-specific parameterization.

The reference list is reasonably comprehensive (48 references) and covers the relevant domains: constellation operations, swarm robotics, distributed systems theory, queueing theory, and military swarm programs. Key foundational works are cited (Lamport, Lynch, Kleinrock, Demers et al.). However, several gaps exist:

- No references to the substantial literature on satellite network simulation tools (e.g., STK, MATLAB Satellite Communications Toolbox, ns-3 satellite modules). How does the custom DES compare to established tools?
- The DTN/BPv7 references (Cerf et al., CCSDS) are cited but not meaningfully integrated into the simulation model. If store-and-forward networking is relevant to intermittent ISL connectivity, it should be modeled or explicitly excluded with justification.
- Recent work on distributed satellite systems coordination (e.g., Radhakrishnan et al., 2016, "Survey of inter-satellite communication for small satellite systems"; Marchetti et al., 2023 on autonomous constellation management) appears to be missing.
- The Reynolds [1987] "Boids" reference is cited in the bibliography but never referenced in the text.

Several references are non-archival (SpaceX website, Amazon website, DARPA program pages, DoD fact sheets). While understandable for operational systems, the paper should minimize reliance on these for technical claims. The NRL reference [20] is explicitly noted as "non-peer-reviewed."

---

## Major Issues

1. **Misleading "full-fidelity" terminology.** The paper uses "full-fidelity" to mean "all nodes participate" but the simulation abstracts away MAC scheduling, link acquisition, pointing, Doppler, orbital perturbations, and correlated failures. This terminology will mislead readers into thinking the simulation captures physical-layer effects. **Required action:** Replace "full-fidelity" with "full-participation" or "complete-enumeration" throughout, and add a clear statement early in Section III that the simulation operates at the message-passing abstraction layer.

2. **Inconsistent Monte Carlo replication counts.** Section III-D states "2–5 independent runs per configuration" while the abstract and results sections claim 30 replications. **Required action:** Resolve this inconsistency. If 30 replications were used for all reported results, correct Section III-D. If different replication counts were used for different analyses, document this clearly.

3. **Near-deterministic results undermine the DES contribution.** With SD < 0.001% across 30 replications, the simulation is essentially computing a deterministic formula. The paper needs to articulate more clearly what the DES reveals that analytical calculation does not. **Required action:** Either (a) introduce scenarios where stochastic effects are significant (correlated failures, dynamic topology, realistic link models) and show the DES captures behavior that analytics cannot predict, or (b) reframe the contribution as a validated analytical framework rather than a simulation study.

4. **Queueing model mismatch.** The $M/D/1$ model assumes Poisson arrivals, but the reporting model (fixed rate $r$, cycle period $T_c$) produces synchronized/batch arrivals. **Required action:** Justify the Poisson assumption (e.g., by showing that random phase offsets across nodes produce approximately Poisson aggregate arrivals) or use an appropriate batch-arrival model.

5. **Absence of the most relevant comparator.** The sectorized mesh is identified as the most promising decentralized alternative and "priority future work," but its absence means the paper cannot make meaningful claims about the hierarchical architecture's advantage over practical decentralized approaches. **Required action:** Either implement a basic sectorized mesh model (even analytically) to bound its performance, or significantly temper the comparative claims in the abstract and conclusion.

---

## Minor Issues

1. **Section III-D vs. abstract inconsistency on MC runs:** "2–5 independent runs" vs. "30 Monte Carlo replications." One of these is incorrect.

2. **Eq. (2):** The $M/D/1$ waiting time formula $W_q = \rho / [2\mu(1-\rho)]$ is the Pollaczek-Khinchine result for $M/D/1$. Confirm this is the correct form (some references use $W_q = \rho^2 / [2\lambda(1-\rho)]$, which is equivalent but expressed differently).

3. **Table IV (Duty Cycle):** The "Handoff Success" column shows values increasing with duty cycle duration (95% → 99.9%), but the text explains this as fewer handoff events reducing cumulative failure probability. Clarify whether the reported percentage is per-handoff or per-day success probability.

4. **Table V:** All ten fleet sizes show $\eta = 20.66\%$ or $20.67\%$ (for $N=1000$). The 0.01% difference at $N=1000$ may be a finite-size effect worth noting explicitly.

5. **Section III-F, paragraph 3:** "the coordinator uses the combined coordination bandwidth of its cluster (effectively $k_c \times 1$ kbps = 100 kbps available, of which 20.5 kbps is consumed)"—this bandwidth pooling assumption is later superseded by the explicit parameterization in Section III-F-1. The earlier text should forward-reference the parameterization to avoid confusion.

6. **Bibliography [10] (Reynolds 1987):** Cited in the bibliography but never referenced in the text. Remove or add a citation.

7. **Abstract:** "SD < 0.001%" appears twice—once as a parenthetical and once after the $\pm$ notation. Consolidate.

8. **Section V-B:** "none of these systems manages $10^6$ fully autonomous nodes"—the paper's own simulation only reaches $10^5$, making the $10^6$ comparison somewhat aspirational.

9. **Eq. (6), mesh convergence:** $T_{\text{converge}} = D \cdot \tau_{\text{gossip}}$ with $D = O(N^{1/3})$ for 3D orbital space—this assumes a random geometric graph, but LEO constellations occupy thin shells (quasi-2D), where $D = O(N^{1/2})$ may be more appropriate.

10. **Table II (Bandwidth Breakdown):** The "Aggregation" row for the mesh column shows "$O(N)$" in a table of bps values. Use a consistent unit or add a footnote.

---

## Overall Recommendation

**Major Revision**

The paper addresses a relevant problem and presents a well-structured simulation study with commendable transparency about limitations and baseline interpretation. However, the central contribution is weakened by three issues: (1) the primary result ($O(1)$ overhead scaling) is analytically trivial and the DES adds minimal insight beyond confirming the constant factor; (2) the "full-fidelity" framing overstates the simulation's realism given the extensive physical-layer abstractions; and (3) the comparison against intentionally weak baselines, without the most relevant comparator (sectorized mesh), limits the practical significance of the findings. The coordinator bandwidth parameterization and link availability analysis are the paper's strongest engineering contributions but need MAC-layer modeling support. A major revision should reframe the contribution around the engineering design parameters (coordinator bandwidth thresholds, duty cycle trade-offs, exception-based telemetry) rather than the analytically predictable scaling result, and should either implement a sectorized mesh comparator or substantially temper the comparative claims.

---

## Constructive Suggestions

1. **Reframe the core contribution.** The most valuable results are the engineering design parameters: coordinator bandwidth thresholds (50 kbps for zero-drop), duty cycle sweet spots (24–48 h), exception-based telemetry reduction factors, and link availability robustness bounds. Lead with these actionable findings rather than the analytically predictable $O(1)$ scaling. Consider restructuring the abstract and conclusion to emphasize "design guidelines for hierarchical space swarm coordination" rather than "characterizing scaling properties."

2. **Implement a minimal sectorized mesh model.** Even an analytical model (not full DES) of sectorized gossip with $O(\sqrt{N})$ neighborhood size would provide a far more meaningful comparator than the global-state mesh upper bound. This would transform the paper from "hierarchical beats worst-case baselines" to "hierarchical outperforms practical decentralized alternatives by factor X," which is a much stronger claim.

3. **Add a scenario where the DES reveals non-obvious behavior.** Consider implementing correlated coordinator failures (e.g., a solar particle event disabling 10% of coordinators simultaneously) or a dynamic cluster reassignment scenario. If the DES shows that the $O(1)$ scaling breaks down under correlated failures or that recovery time exhibits nonlinear scaling, this would be a genuinely novel finding that justifies the simulation approach.

4. **Add a minimal TDMA scheduling model within $T_c$.** The coordinator bandwidth analysis (Section IV-G) is the paper's strongest engineering contribution but lacks MAC-layer support. Implementing even a simple slotted-ALOHA or TDMA model within each 10-second cycle would validate the $\gamma \approx 0.85$ assumption and strengthen the 59-kbps design recommendation.

5. **Replace "full-fidelity" with precise language and add a simulation abstraction table.** Create a table listing what is modeled (message generation, routing, byte counting, node failures) and what is abstracted (MAC scheduling, link acquisition, pointing, Doppler, orbital perturbations, correlated failures). This would be more informative than the current "full-fidelity" claim and would help readers assess the results' applicability to their specific use cases.