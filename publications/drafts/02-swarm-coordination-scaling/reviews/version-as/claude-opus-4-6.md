---
paper: "02-swarm-coordination-scaling"
version: "as"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-27"
recommendation: "Major Revision"
---



# Peer Review: "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms"

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a genuine gap at the intersection of mega-constellation operations and swarm coordination: the lack of byte-level traffic accounting for hierarchical architectures at the 10³–10⁵ node scale. The authors correctly identify that swarm robotics literature rarely exceeds ~100 agents, constellation management literature treats routing but not autonomous coordination overhead, and no prior work systematically derives closed-form sizing equations for this regime. The practitioner-oriented design equations (Section V-C) and the sizing table approach have clear engineering utility.

However, the novelty is tempered by several factors. First, the core analytical results are relatively straightforward applications of existing theory: the AoI result is a direct geometric-distribution quantile (Eq. 12), the GE recovery is a standard Markov-chain calculation, and the coordinator capacity is essentially a bandwidth accounting exercise. The intellectual contribution is more in the *assembly* and *validation* of these known results than in new theoretical insight. Second, the paper's central finding—that protocol overhead is O(1) and scale-invariant under a hierarchical tree with fixed fan-out—is essentially a restatement of the well-known property that tree aggregation yields O(N) total messages with O(1) per-node cost. The DES "validation" of this known property adds limited scientific value.

The most novel contribution is arguably the joint-independence verification (Section IV-D), which demonstrates that GE loss and coordinator saturation decouple under point-to-point ISLs. This is a useful engineering insight, though the authors appropriately note it is a property of the modeled pipeline rather than a general principle. The workload envelope characterization (5%–46%) and the identification that commands, not topology-induced overhead, dominate the stress case is practically useful but not deeply surprising.

## 2. Methodological Soundness

**Rating: 3 (Adequate)**

The simulation framework is clearly described and the cycle-aggregated approach is appropriate for the message-layer analysis claimed. The vectorized implementation enabling ~7s runtimes at N=10⁵ is pragmatic. The validation against Pollaczek-Khinchine (within 2% at N=100) and gossip convergence bounds (N≤1,000) provides some confidence, though these are low-N checks that do not stress the simulation at the scales where it is most needed.

**Concerns about the simulation's discriminating power:** The DES-to-analytical agreement is *too* perfect (Table VII: Δ < 0.1% across all fleet sizes, SD < 0.001%). This raises the question of whether the simulation is genuinely an independent validation or merely a re-implementation of the same byte-counting arithmetic. If the simulation deterministically generates exactly the messages prescribed by the traffic model (Table VI), processes them through a pipeline with no stochastic contention (point-to-point links, deterministic processing), and counts bytes, then the DES is algebraically equivalent to the closed-form—not an independent check. The only stochastic elements (GE loss, node failures, exception telemetry) are validated separately. The authors should clarify what emergent behaviors, if any, the DES can reveal that the closed-form cannot.

**Monte Carlo configuration:** 30 replications with SD < 0.001% suggests the variance is entirely from the stochastic elements (failures, loss), not from the overhead calculation itself. This is consistent with the above concern. The bootstrap CIs are appropriate but the near-zero variance makes them uninformative for the primary metric.

**The M/D/1 centralized baseline** is acknowledged as an intentional bound, but the paper's framing occasionally implies a stronger comparison than warranted. The realistic M/D/c baseline (Table I) correctly shows centralized processing scales to ~10⁶, which significantly weakens the case for hierarchical coordination on processing grounds alone. The authors acknowledge this (Section IV-G) but the abstract and introduction could be more upfront.

**GE model parameterization:** The GE parameters (p_GB = 0.05, p_BG = 0.20) yield 80% steady-state availability, which is reasonable for RF backup but not well-justified from empirical ISL data. The sensitivity to these parameters is not explored—a significant gap given that the inter-cycle recovery time (the paper's key GE contribution) is dominated by p_BG.

## 3. Validity & Logic

**Rating: 3 (Adequate)**

The conclusions are generally supported by the analysis, and the authors are commendably transparent about limitations. The paper correctly identifies that the hierarchical advantage is fault tolerance and spectrum independence rather than processing scalability—a nuanced and honest assessment that strengthens credibility.

**Logical concerns:**

1. **The 1 kbps budget framing creates a somewhat artificial problem.** The paper acknowledges this is the RF-backup regime (<1% of operational time), and that under nominal optical ISLs "coordination overhead is negligible." This means the entire analysis characterizes a degraded mode that rarely occurs. While designing for degraded modes is important, the paper should more clearly articulate *why* the RF-backup sizing is the binding design constraint rather than, say, the optical-ISL coordination architecture that operates 99%+ of the time.

2. **Static cluster membership (Section III-B, limitation in V-B):** The assumption of fixed cluster membership for one year is a significant simplification for LEO mega-constellations. The authors acknowledge cross-plane drift but understate the impact: in a Walker constellation with multiple inclinations, inter-plane relative motion creates neighbor changes on orbital-period timescales (~90 min). The claim that "co-moving elements in the same orbital shell change neighbor distances on timescales of hours to days" is true only for co-planar elements and misrepresents the general LEO case.

3. **Table V (Duty Cycle Trade-offs):** The power variance, handoff success, and system availability columns appear to be analytically derived but are presented without derivation details sufficient for reproduction. The system availability of 99.5% at 24h duty cycle is stated to "conservatively account for cascading re-election effects" but no cascading failure model is presented. This is a hand-wave in what is otherwise a carefully quantified paper.

4. **Sectorized mesh parameterization:** The √N sector sizing is described as an "order-of-magnitude heuristic" (Section III-B.4), and the capped-fanout variant (cap=10) is the DES default. The choice of cap=10 significantly affects the comparison: at cap=50, the sectorized mesh overhead rises to ~90% (Table III), making the hierarchical advantage more pronounced. The paper should discuss which cap value is operationally realistic.

5. **The "joint independence" finding (Section IV-D, Table IV):** The result that GE drops equal no-loss drops at every capacity level is presented as a key finding, but it follows trivially from the architecture: if lost messages never reach the coordinator queue, they cannot cause drops. This is not an empirical discovery but a logical consequence of the pipeline model. The finding would be more interesting if the paper also tested the shared-medium case where independence breaks down.

## 4. Clarity & Structure

**Rating: 4 (Good)**

The paper is well-organized with a clear roadmap (beginning of Section IV) and consistent notation. The abstract is accurate and appropriately detailed. The separation of reference bounds from the architecture under study is clearly maintained throughout. Tables are generally well-formatted and informative, particularly Table VI (traffic accounting) and Table VIII (abstraction scope).

**Strengths:** The "Baseline Interpretation Note" (Section I-C) is an excellent practice that preempts misinterpretation. The design equations summary (Section V-C) is genuinely useful for practitioners. The explicit distinction between offered and delivered overhead is carefully maintained.

**Weaknesses:**

- The paper is *very* long for the depth of its analytical contribution. Much of the content is careful bookkeeping (byte counts, parameter tables) rather than insight. Sections IV-F through IV-I could be substantially compressed.
- Figure descriptions reference PDFs that are not available for review (e.g., fig-architecture-diagram.pdf, fig-phase-stagger.pdf). While this is standard for LaTeX submissions, it makes it impossible to evaluate the figures' effectiveness.
- The notation is mostly consistent but there are occasional ambiguities: $\eta$ is used for both offered and delivered overhead in different contexts, and the reader must track which is meant. The subscript convention ($\eta_{\text{DES}}$, $\eta_{\text{analytic}}$, $\eta_{\text{eff}}$, $\eta_{\text{sector}}$, $\eta_S$, $\eta_N$, $\eta_E$, $\eta_0$) proliferates.
- The paper would benefit from a single consolidated "design table" that a practitioner could use directly, rather than requiring assembly from multiple tables and equations scattered across Sections IV and V.

## 5. Ethical Compliance

**Rating: 4 (Good)**

The paper includes an appropriate disclosure about AI-assisted ideation (Acknowledgment section), noting that Claude 4.6, Gemini 3 Pro, and GPT-5.2 "motivated aspects of the coordinator architecture but is not validated here." This is transparent and appropriately scoped. The code and data availability statement (Section VI*) with a specific GitHub tag enables reproducibility.

The anonymous authorship ("Project Dyson Research Team") with a note that individual names will be provided for final publication is unusual but acceptable per the stated IEEE policy. The lack of institutional affiliations makes it difficult to assess potential conflicts of interest. The reference to the project's own multi-model AI paper [46] as a self-citation should be noted but is not problematic given the disclosure.

One concern: the model versions cited (Claude 4.6, GPT-5.2) do not correspond to any publicly known releases as of the apparent submission date, which is puzzling and should be clarified.

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is appropriate for IEEE TAES in its treatment of autonomous spacecraft coordination, though it sits closer to the communications/networking boundary than the journal's core aerospace focus. The references span the relevant domains (constellation operations, swarm robotics, queueing theory, distributed systems) and include foundational works (Kleinrock, Lamport, Demers).

**Gaps in referencing:**

- The paper does not cite the substantial body of work on **satellite network topology design and optimization** (e.g., Bhattacherjee & Singla, "Network topology design at 27,000 km/hour," CoNEXT 2019), which directly addresses ISL topology dynamics in mega-constellations.
- The **CCSDS Spacecraft Onboard Interface Services (SOIS)** standards for intra-spacecraft and proximity communication are relevant but not cited.
- Recent work on **distributed space systems** by Radhakrishnan et al. (2016, survey) and **autonomous constellation management** by Legge (MIT, 2014) would strengthen the related work section.
- The AoI literature is well-cited but the connection to **value of information** frameworks (Ayan et al., 2019) could strengthen the AoI-to-position-error coupling discussion.
- Several references are non-archival (Amazon website, DARPA program pages, DoD fact sheets). While understandable for program descriptions, the paper relies on 6+ non-archival sources, which is high for an archival journal.

---

## Major Issues

1. **The simulation adds minimal independent validation beyond the closed-form.** The near-perfect DES-to-analytical agreement (Δ < 0.1%, SD < 0.001%) across all fleet sizes suggests the DES is algebraically equivalent to the traffic accounting, not an independent check. The authors must either (a) identify specific emergent behaviors the DES reveals that the closed-form cannot predict, or (b) reframe the DES contribution as a *reproducible parametric tool* rather than a *validation*. The inter-cycle GE recovery (Fig. 5) is the one area where the DES genuinely adds value; this should be emphasized more strongly.

2. **GE parameter sensitivity is absent.** The inter-cycle recovery time—one of the paper's primary contributions—is dominated by p_BG, yet no sensitivity analysis over GE parameters is presented. At minimum, sweep p_BG ∈ {0.1, 0.2, 0.5} and p_B ∈ {0.5, 0.7, 0.9} and show how P95 recovery cycles vary. Without this, the "4 cycles, mean 1.7" result is a single point, not a design equation.

3. **Static topology assumption undermines applicability to LEO mega-constellations.** The one-year fixed cluster membership is unrealistic for the target application (Starlink-class constellations with multiple orbital shells and inclinations). The paper should either (a) bound the cluster re-association overhead analytically (e.g., state transfer frequency × handoff cost), or (b) restrict the applicability claim to co-planar formations and state this prominently.

4. **The centralized baseline comparison is misleading in places.** The abstract states the hierarchical advantage is "fault tolerance during ground outages and spectrum independence at scale," but the paper spends substantial space on processing scalability comparisons (Table I, Fig. 8) that are acknowledged to be non-binding. The paper should lead with the actual advantages (fault tolerance, spectrum independence, ground-contact independence) and de-emphasize the processing comparison.

5. **Missing shared-medium analysis.** The joint-independence result (Section IV-D) is explicitly conditioned on point-to-point ISLs, and the paper repeatedly notes it would not hold under shared-medium RF. Since the RF-backup scenario (the paper's operating regime) is precisely where shared-medium contention is most likely (omnidirectional S-band), this is a critical gap. At minimum, a bounding analysis of the shared-medium case should be provided.

## Minor Issues

1. **Eq. (2):** The M/D/1 mean waiting time formula $W_q = \rho / [2\mu_s(1-\rho)]$ is the P-K result for M/D/1, but should be explicitly stated as applying to the mean *waiting* time (excluding service), as the notation could be confused with sojourn time.

2. **Table VII:** Reporting "η_DES = 46.0% at all 8 intermediate sizes" with a note "omitted for brevity" is appropriate, but the claim of SD < 0.001% should include the actual SD value for at least one configuration.

3. **Section III-E (Communication Overhead Definition):** The paragraph beginning "Baseline telemetry ($B_{\text{status}} = 204.8$ bps, 20.5%, topology-invariant) is excluded from η" appears before the formal definition of η, creating a forward-reference issue.

4. **Eq. (12):** The ceiling function in the AoI P99 formula should be accompanied by a note that this is exact for the geometric distribution on integer multiples of T_c, not an approximation.

5. **Table IV (Joint Interaction):** The "No Loss" and "GE Only" columns show identical drop counts. This should be explicitly explained in the table note (it follows from the pipeline architecture) rather than requiring the reader to infer it from the text.

6. **Section I-D, item 4:** "Sectorized mesh: 1.35–1.95× higher" — this range does not match the 1.4–1.5× stated elsewhere (Section IV-E, Fig. 6). Reconcile.

7. **Acknowledgment section:** "Total MC wall-clock time: ~90 min on commodity hardware" — specify the hardware (CPU, RAM) for reproducibility.

8. **Reference [1]:** The Starlink FCC filing is cited alongside "Jonathan's Space Report" (non-archival, personal website). These should be separate references with the non-archival nature clearly flagged.

9. **Eq. (6):** The mesh message complexity $M_{\text{mesh}} = O(N \cdot f \cdot \log N) = O(N^2)$ requires $f = O(N/\log N)$ to yield $O(N^2)$, but this fanout is unrealistically high. Standard gossip uses $f = O(\log N)$, yielding $O(N \log^2 N)$ total messages. The $O(N^2)$ bound comes from full state replication ($N$ entries × $N$ nodes), not from the gossip protocol itself. Clarify.

10. **The "safe-mode floor" concept (Section V-C):** The γ_min = η/1.0 formula is trivially η itself. The insight is that different workloads have different γ_min thresholds, but the formula adds no value.

---

## Overall Recommendation

**Major Revision**

The paper addresses a legitimate engineering need—sizing equations for hierarchical coordination in large autonomous spacecraft swarms—and the practitioner-oriented design equations have clear utility. The work is carefully executed with transparent assumptions and honest limitation acknowledgments. However, the paper suffers from three fundamental issues that require substantial revision: (1) the simulation's role as "validation" is overstated when it is algebraically equivalent to the closed-form for the primary metric; (2) critical sensitivity analyses are missing (GE parameters, shared-medium contention); and (3) the static topology assumption significantly limits applicability to the stated target domain of LEO mega-constellations. The paper is also longer than warranted by its analytical depth, with substantial space devoted to bookkeeping that could be compressed. A major revision addressing these issues—particularly reframing the simulation's contribution, adding GE sensitivity, and bounding dynamic topology effects—would produce a solid contribution to the field.

---

## Constructive Suggestions

1. **Reframe the simulation contribution.** Position the DES as (a) a reproducible parametric sizing tool, (b) a validator for the inter-cycle GE recovery (where it genuinely adds value), and (c) a joint-condition testbed. De-emphasize the overhead "validation" where DES and closed-form are algebraically equivalent. This honest reframing would actually strengthen the paper.

2. **Add GE parameter sensitivity.** Sweep p_BG ∈ {0.1, 0.2, 0.5} and p_B ∈ {0.5, 0.7, 0.9} to produce a *family* of inter-cycle recovery curves. This transforms the single-point result into a genuine design equation parameterized by link quality—significantly increasing the paper's utility.

3. **Bound dynamic topology overhead analytically.** Estimate cluster re-association frequency for representative Walker constellations (e.g., Starlink shell 1: 53° inclination, 22 planes, 72 satellites/plane) and compute the additional state-transfer traffic as a fraction of the 1 kbps budget. Even a rough bound (e.g., "re-association every 45 min adds ~X% overhead") would substantially strengthen applicability claims.

4. **Consolidate into a single practitioner design table.** Create one table with columns: {Parameter, Design Equation, Nominal Value, Stress Value, Units, Equation Reference}. This would be the paper's most-cited artifact and would justify the "practitioner-oriented" claim in the abstract.

5. **Add a minimal shared-medium bounding analysis.** Even a simple model—e.g., Slotted ALOHA with N_cluster = k_c contenders, showing how retransmission-induced load increase maps to throughput collapse—would address the most significant conditionality in the joint-independence result and demonstrate awareness of the RF-backup scenario's actual physics.