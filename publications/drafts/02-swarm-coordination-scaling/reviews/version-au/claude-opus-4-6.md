---
paper: "02-swarm-coordination-scaling"
version: "au"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-27"
recommendation: "Major Revision"
---



# Peer Review: "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms"

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a genuine gap: there is no prior systematic byte-level traffic accounting for hierarchical coordination architectures at the $10^3$–$10^5$ node scale. The operating regime—RF-backup at 1 kbps during optical ISL outages—is well-motivated and practically relevant as mega-constellations grow. The assembly of standard queueing, geometric, and Markov-chain results into a coherent sizing toolkit for space-systems practitioners has clear engineering utility.

However, the authors are commendably honest (Section I-D, and repeatedly throughout) that the individual analytical results are standard: M/D/1 queueing, geometric AoI distributions, and Gilbert-Elliott Markov chains are textbook material. The claimed contribution is their "assembly, cross-validation, and packaging." While packaging has value, the intellectual novelty is limited. The pipeline decoupling observation (Section IV-D) is presented as a "design principle," but it is an immediate consequence of the point-to-point architecture—the authors themselves acknowledge it is "not an empirical discovery." The paper would benefit from at least one result that is not a direct parameterization of an existing formula.

The practical significance is also somewhat constrained by the operating regime. The authors note that the 1 kbps budget applies to <1% of operational time (optical ISL availability >99%). This means the entire analysis characterizes a degraded backup mode. While designing for degraded modes is important, the paper should more prominently discuss whether the hierarchical architecture provides advantages during the 99%+ nominal optical regime, or whether the contribution is purely about graceful degradation.

## 2. Methodological Soundness

**Rating: 3 (Adequate)**

The methodology has several strengths: the traffic accounting is meticulous (Tables V, VI), the overhead definition ($\eta$) is carefully separated from baseline telemetry, and the distinction between offered and delivered overhead is properly maintained. The TDMA frame analysis (Eq. 8–9) deriving $\gamma = 0.949$ from first principles is a nice touch, even if the authors conservatively retain $\gamma = 0.85$. The open-source code availability strengthens reproducibility.

However, there are significant methodological concerns:

**Simulation fidelity.** The "cycle-aggregated" DES is essentially a vectorized accounting exercise, not a discrete-event simulation in the traditional sense. Events are not individually scheduled; instead, array operations accumulate bytes per cycle. This is acknowledged ("not per-packet or per-bit"), but the term "DES" is misleading. The simulation confirms closed-form byte counts to within 0.1%—but this is expected when the simulation implements the same accounting equations. The only area where the simulation adds genuinely independent value is the inter-cycle GE recovery distribution (Fig. 7), which the authors correctly identify. The validation against Pollaczek-Khinchine (Section III-A) at $N=100$ and gossip bounds at $N \leq 1{,}000$ is thin; these are small-scale checks that do not stress the simulation at the target regime.

**Static topology assumption.** The fixed cluster membership over a 1-year simulation is a serious limitation for LEO mega-constellations. The authors acknowledge this (Section V-B) but understate its impact. In Walker-delta constellations (Starlink, Kuiper), cross-plane relative motion causes neighbor changes on ~90-minute timescales. The claim that "co-moving elements in the same orbital shell change neighbor distances on timescales of hours to days" (Section III-B) is only true for intra-plane neighbors; the paper's four-level hierarchy with regional coordinators necessarily spans multiple planes. Cluster re-association overhead could fundamentally alter the overhead budget.

**Baseline fairness.** The centralized $c=1$ baseline is acknowledged as an "intentional worst-case bound," which is appropriate. However, the $c = N/k_c$ baseline (Table I) shows centralized processing scales to $10^6$, which undermines the paper's motivation. The authors correctly note that the hierarchical advantage is fault tolerance and spectrum independence, not processing scalability—but this reframing happens mid-paper and somewhat contradicts the framing in the Introduction and abstract.

**Monte Carlo design.** 30 replications with SD < 0.001% suggests the simulation has essentially zero stochastic variation, which is consistent with a deterministic byte-counting exercise. The bootstrap CIs are technically correct but uninformative when variance is negligible. The GE recovery validation uses only 3 MC replications (Fig. 7 caption)—this should be justified or increased.

## 3. Validity & Logic

**Rating: 3 (Adequate)**

The core analytical results are internally consistent and correctly derived. The AoI cross-check (Eq. 6 vs. DES: 440 vs. 441 s) and the overhead verification (Table VII) demonstrate careful bookkeeping. The joint interaction verification (Table IX) is a valuable contribution showing that GE losses and coordinator capacity decouple under point-to-point links—though as noted, this is architectural rather than empirical.

Several logical issues deserve attention:

**The $\eta \approx 46\%$ headline number is misleading.** The stress-case assumes every node receives a 512-byte command every 10-second cycle. As the authors show (Section IV-E), commands account for >60% of this overhead and are topology-invariant. The architecture-specific overhead is only ~5%. The abstract and title emphasize "hierarchical coordination" sizing, but the dominant cost has nothing to do with hierarchy. This should be reframed: the paper's actual finding is that hierarchical coordination adds minimal overhead (~5%), and the system is command-budget-limited regardless of topology.

**Coordinator ingress range (21–50 kbps) is too wide to be a useful design equation.** The 2.4× range between Model A and Model B reflects different scheduling assumptions, not uncertainty. The paper should recommend one model with sensitivity analysis rather than presenting a range that spans a factor of 2.4.

**The sectorized mesh comparison is underspecified.** The $\sqrt{N}$ sector sizing is described as an "order-of-magnitude heuristic" (Section III-B), and the capped-fanout variant (cap = 10) is acknowledged to provide only 3.2% sector coverage (Table IV). It is unclear whether 3.2% coverage is operationally meaningful for conjunction screening. Without grounding the sector size in conjunction geometry, the comparison lacks physical justification.

**Extrapolation beyond validated range.** The $10^6$-node analytical extrapolation (Fig. 12, noted in caption) and the centralized $M/D/c$ scaling (Table I) extend well beyond the DES-validated $10^5$ range. While analytical extrapolation is legitimate, the paper should be more cautious about conclusions drawn from it.

## 4. Clarity & Structure

**Rating: 3 (Adequate)**

The paper is generally well-organized, with a clear roadmap (Section IV opening) and consistent notation. The design equations summary (Section V-C) is a useful practitioner reference. Tables are numerous and mostly well-formatted, though the sheer volume (16 tables, 14 figures) makes the paper dense.

Several clarity issues:

**Length and redundancy.** The paper is excessively long for a journal article. Many results are stated in the abstract, restated in the contributions list (Section I-D), restated in the results roadmap (Section IV opening), presented in the results, and restated in the design equations summary (Section V-C) and conclusion. The 46% overhead figure appears at least 15 times. Significant compression is possible without losing content.

**Notation inconsistency.** $p_{\text{link}}$ (Table VIII) and $p_{\text{loss}}$ (Section IV-C) are used in overlapping contexts. The relationship between $p_{\text{link}}$ (link availability) and $p_G$, $p_B$ (GE loss probabilities) should be made explicit in one place.

**Figure quality cannot be assessed** since figures are referenced but not provided (PDF includes only filenames). This is a significant gap for review; the paper relies heavily on figures (14 total) for key results.

**The "Baseline Interpretation Note" (Section I-C)** is awkwardly placed and reads as a defensive response to prior review feedback rather than organic exposition. This material should be integrated into the methodology.

**Table VII** omits 8 intermediate fleet sizes "for brevity" but the constant $\eta$ across all sizes is the main result—showing all points would strengthen the claim and take minimal space.

## 5. Ethical Compliance

**Rating: 4 (Good)**

The paper includes an appropriate AI-assistance disclosure in the Acknowledgment section, noting that "Claude 4.6, Gemini 3 Pro, GPT-5.2" contributed to ideation but are "not validated here." The open-source code and data availability statement support reproducibility. The anonymous authorship ("Project Dyson Research Team") with a note about IEEE policy compliance is acceptable for review but must be resolved for publication.

One concern: the reference to the AI methodology paper [42] is self-referential and points to a non-peer-reviewed URL. If AI tools materially influenced the architecture design, the methodology should be described in sufficient detail for independent evaluation, not deferred to an external document. The phrase "motivated aspects of the coordinator architecture" is vague—which aspects?

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is appropriate for IEEE TAES in scope, addressing autonomous spacecraft coordination with quantitative engineering analysis. The reference list (50 citations) covers the relevant domains: constellation operations, swarm robotics, queueing theory, distributed systems, and AoI theory.

However, several gaps exist:

**Missing key references.** The paper does not cite recent work on distributed space systems coordination that is directly relevant: (1) NASA's Distributed Spacecraft Autonomy (DSA) project and associated publications; (2) recent work on inter-satellite link scheduling for mega-constellations (e.g., Bhattacherjee et al., SIGCOMM 2019); (3) the CCSDS Space Packet Protocol and its overhead characteristics, which would ground the message-size assumptions; (4) work on age-of-information in satellite networks specifically (e.g., recent IEEE JSAC special issues).

**Non-archival references.** Several references are non-archival (Amazon Kuiper overview, DARPA program pages, DoD fact sheets, NRL magazine article). While understandable for operational programs, the paper should minimize reliance on these for technical claims. Reference [1] (SpaceX FCC filing + "Jonathan's Space Report") is particularly weak as the primary citation for Starlink operations.

**Self-citation.** Reference [42] (Project Dyson multi-model AI paper) is self-referential and not peer-reviewed. Its inclusion is acceptable for transparency but should not be relied upon for technical claims.

## Major Issues

1. **The simulation does not add substantial value beyond the closed-form equations.** The 0.1% agreement between DES and analytical overhead (Table VII) demonstrates that the simulation implements the same accounting, not that it independently validates it. The only genuinely independent simulation contribution is the inter-cycle GE recovery distribution (Fig. 7), which uses only 3 MC replications. The paper should either (a) enhance the simulation to model phenomena not captured analytically (MAC contention, dynamic topology, correlated failures) or (b) reframe the paper as purely analytical with lightweight numerical verification, dropping the "simulation framework" framing.

2. **Static topology invalidates the 1-year simulation duration for LEO applications.** The paper's target application is mega-constellations (Starlink, Kuiper), where cross-plane relative motion causes topology changes on ~90-minute timescales. The static-cluster assumption is only valid for co-planar formations, which represent a small subset of the claimed application domain. Either (a) restrict claims to co-planar formations, (b) model cluster re-association, or (c) provide an analytical bound on re-association overhead.

3. **The headline result ($\eta \approx 46\%$) is dominated by topology-invariant command traffic.** Since commands account for >60% of stress-case overhead and are independent of coordination topology, the paper's central claim about "hierarchical coordination overhead" is misleading. The architecture-specific overhead is ~5%, which is the more meaningful and novel result. The paper should be restructured around this finding.

4. **Missing physical-layer validation undermines the practical utility of design equations.** The $\gamma$ parameter is derived analytically (Eq. 8) but never validated against a packet-level simulator or hardware measurements. The authors acknowledge this as future work (Section V-A), but since all capacity results scale as $1/\gamma$, the practical accuracy of the design equations depends entirely on this unvalidated parameter. At minimum, a sensitivity analysis showing how results change across the full $\gamma \in [0.3, 0.95]$ range should be provided (partially done in Fig. 9b but not systematically).

## Minor Issues

1. **Eq. 2** ($W_q = \rho / [2\mu_s(1-\rho)]$): This is the M/D/1 waiting time, but the text claims aggregate arrivals are Poisson (CV = 0.98), which would make it M/D/1 only if service is deterministic. Clarify whether this is M/D/1 or M/M/1.

2. **Section III-B, hierarchical topology**: "configurable fan-out" is mentioned but the four-level structure (Eq. 4) is fixed. Clarify what is configurable vs. fixed.

3. **Table II** (mesh traffic): The formula in the footnote gives "~51 MB" but the text says "~73 MB" with 1.4× redundancy. The 1.4× gossip redundancy factor should be derived or cited, not assumed.

4. **Section IV-A**: "Model B uses a leaky-bucket shaper" — the term "leaky bucket" typically refers to a specific traffic shaping algorithm. The description sounds more like a token bucket. Clarify the distinction.

5. **Table IX**: The "No Loss" and "GE Only" columns are identical, which is the paper's point about decoupling. However, the GE model has 91% steady-state good availability, meaning ~9% of messages are lost. The identical drop counts suggest drops are measured at the coordinator ingress, not end-to-end. Clarify what "Drops" measures.

6. **Section III-F**: "CV = 0.98 ± 0.03 for $N \geq 1{,}000$" — report the sample size and method for this estimate.

7. **Acknowledgment**: "Claude 4.6, Gemini 3 Pro, GPT-5.2" — these version numbers do not correspond to any publicly released models as of mid-2025. If these are internal/future versions, note this; if they are errors, correct them.

8. **Eq. 6** (AoI P99): The ceiling function produces a discrete value; the DES reports 441 s while the formula gives 440 s. This 1-s discrepancy is within one $T_c$ discretization but should be explained (likely cycle-boundary alignment).

9. **Table X** (duty cycle): "Handoff Success" of 95% at 1-hour duty cycle is unexplained. If the optical ISL transfer takes 80–400 ms, why would it fail 5% of the time? Clarify the failure mechanism.

10. **Section I-D**: The notation $\eta$ is defined as "protocol overhead beyond topology-invariant baseline telemetry" but is later used for both offered and delivered overhead, with $\eta_{\text{delivered}}$ introduced separately. Establish notation consistently at first use.

11. **Formatting**: Several table footnotes use superscript letters (a, b, c, d) inconsistently—some tables skip letters (Table VI has a, c, d but no b).

## Overall Recommendation

**Major Revision**

The paper addresses a relevant engineering problem and provides careful byte-level traffic accounting for hierarchical coordination in large space swarms. The design equations, while individually standard, are assembled into a useful practitioner toolkit. However, four issues require substantial revision: (1) the simulation adds negligible value beyond the closed-form equations and should be either enhanced or reframed; (2) the static topology assumption limits applicability to the claimed mega-constellation domain; (3) the headline overhead result is dominated by topology-invariant command traffic, obscuring the actual architectural contribution (~5% overhead); and (4) the lack of physical-layer validation leaves the practical accuracy of all capacity results dependent on an unvalidated $\gamma$ parameter. The paper is also significantly too long and would benefit from substantial compression. With these revisions, the paper could make a solid contribution to IEEE TAES as a systems-engineering reference for coordination protocol sizing.

## Constructive Suggestions

1. **Restructure around the 5% architecture-specific overhead as the primary result.** The ~5% figure is the novel, topology-dependent finding. Present the workload envelope (5–46%) as a secondary result showing that command traffic dominates. This reframing would sharpen the contribution and eliminate the misleading impression that hierarchical coordination costs 46%.

2. **Add a dynamic topology model, even if simplified.** Implement periodic cluster re-association (e.g., every 90 minutes for cross-plane nodes) with the associated state-transfer cost. Even a first-order analytical estimate of re-association overhead as a function of orbital geometry would substantially strengthen the paper's applicability to mega-constellations.

3. **Replace or supplement the cycle-aggregated simulation with a packet-level case study.** Even a single-cluster NS-3 or OMNeT++ simulation at $k_c = 100$ would validate the $\gamma$ assumption and the coordinator ingress model under realistic MAC conditions. This would transform the paper from a purely analytical exercise into one with physical-layer grounding.

4. **Compress the paper by ~30%.** Eliminate redundant restatements of key results (the 46% figure need not appear 15+ times). Merge Tables III and IV into the state-completeness discussion. Move the sectorized mesh details to an appendix. The design equations summary (Section V-C) could serve as the primary results presentation, with supporting analysis in appendices.

5. **Strengthen the inter-cycle GE recovery validation.** Increase from 3 to 30 MC replications (matching the rest of the paper) and provide confidence intervals on the CDF. This is the one area where the simulation adds genuine value; it deserves the strongest possible statistical treatment.