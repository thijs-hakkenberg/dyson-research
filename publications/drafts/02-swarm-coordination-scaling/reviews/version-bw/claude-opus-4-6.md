---
paper: "02-swarm-coordination-scaling"
version: "bw"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-27"
recommendation: "Major Revision"
---

# Peer Review: "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms"

## 1. Significance & Novelty
**Rating: 3 (Adequate)**

The paper addresses a genuine gap: there is no prior work providing closed-form parametric sizing equations for coordination architectures at the $10^3$–$10^5$ node scale with byte-level traffic accounting. The three-layer feasibility framework (byte budget, MAC efficiency, TDMA airtime) is a useful conceptual contribution that practitioners could apply. The decomposition of overhead into architecture-specific ($\eta_0$) and workload-dependent ($\eta_{\text{cmd}}$) components, with the finding that the latter dominates and is topology-invariant, is a clean and actionable result.

However, the novelty is tempered by the fact that the core analytical results are relatively straightforward accounting exercises. The overhead equations are essentially byte-counting identities verified by a simulation that implements the same byte-counting logic—the $<0.1\%$ agreement (Table VII) is expected by construction, not a validation of physical fidelity. The AoI result (Eq. 12) is a direct application of the geometric distribution quantile. The GE recovery analysis, while useful, applies standard two-state Markov chain analysis. The paper's primary contribution is therefore more of a *systems engineering reference design* than a fundamental advance in distributed systems theory or swarm coordination. This is valuable but should be positioned more honestly—the current framing ("closed-form sizing equations") somewhat overstates the analytical depth.

The operational context—sizing an RF-backup channel for ISL outages expected to occupy $<1\%$ of orbital lifetime—is important but narrow. The paper acknowledges this (Section I) but the abstract and title suggest broader applicability than the 1 kbps regime that drives all the interesting constraints. At $\geq$10 kbps, the authors themselves note all message-layer constraints are "non-binding."

## 2. Methodological Soundness
**Rating: 3 (Adequate)**

The analytical framework is internally consistent and the assumptions are stated with commendable transparency. The three-layer feasibility decomposition is well-structured. The slot-level TDMA simulator provides genuine added value beyond the DES, particularly for the ARQ infeasibility finding (52.7% deadline miss rate) and the coherence-time sensitivity analysis (Fig. 7).

**Critical methodological concern: circular verification.** The DES is described as verifying the closed-form equations, but both implement identical message-layer accounting. The $<0.1\%$ agreement (Table VII) demonstrates code consistency, not model validity. The paper acknowledges this distinction in places ("implementation consistency") but the abstract and several results sections blur the line. The claim "Monte Carlo tool verifies implementation consistency to $<0.1\%$" is accurate but the 30-replication MC configuration with SD $< 0.001\%$ for overhead is a red flag—this variance is so small because the system is essentially deterministic for the overhead metric (fixed message sizes, fixed rates, fixed $k_c$). The MC replications add value only for tail statistics (AoI, GE recovery), not for $\eta$.

**Static topology assumption.** The justification that "$\eta$ depends on $k_c$ and message sizes, not node identities" is correct for steady-state overhead but misses the point. In LEO mega-constellations, cluster membership changes on orbital timescales (45–90 min for cross-plane). The $<0.5\%$ overhead estimate for re-association (Section V-B) accounts only for seed handoff bytes, not for the transient period where the coordinator lacks full cluster state, the AoI spikes, or the potential for simultaneous re-associations across multiple clusters. This is acknowledged as future work but significantly limits the applicability claim.

**MAC efficiency abstraction.** Using a single scalar $\gamma$ to capture all MAC-layer effects is a reasonable first-order approach, but the paper draws conclusions that depend sensitively on $\gamma$. At $\gamma = 0.80$, the superframe margin shrinks to 98 ms (Table V)—a regime where the abstraction is likely to break down. The comparison between hierarchical and sectorized mesh (Section IV-G) assumes both operate at $\gamma = 0.85$, but the paper correctly notes the mesh would need distributed TDMA coordination or CSMA/CA ($\gamma \approx 0.3$–$0.5$). This asymmetry should be more prominently flagged in the abstract and conclusions, as it significantly affects the comparative claims.

**Statistical methodology.** The 30-replication MC design is adequate for mean estimation but marginal for P99 tail statistics. Each run produces $\sim 3.15 \times 10^6$ AoI samples, so the per-run P99 is well-estimated, but the inter-run variability of P99 is the relevant uncertainty. The bootstrap CI approach is appropriate but the paper should report the actual CI widths for all tail metrics, not just the AoI example ($[438, 444]$ s).

## 3. Validity & Logic
**Rating: 3 (Adequate)**

The internal logic is generally sound, and the paper is notably careful about qualifying claims. The distinction between message-layer predictions and physical-layer validation is maintained throughout, and Table IX (Claim Map) is an exemplary practice that more papers should adopt.

**Concern 1: Sectorized mesh comparison fairness.** The paper repeatedly emphasizes that the capped sectorized mesh provides only 3.2% sector coverage vs. 100% cluster coverage for the hierarchy. This is true but the comparison is structurally unfair: the mesh is deliberately capped at 10 neighbors to fit the 1 kbps budget, while the hierarchy achieves 100-node awareness through the coordinator aggregation mechanism. The "14× bandwidth efficiency per unit of awareness" metric (Section IV-G) is misleading because it compares a local-monitoring protocol against a hierarchical aggregation protocol—they solve different problems. The paper acknowledges this ("different functional scope") but then uses the comparison to support the hierarchy's superiority. A fairer comparison would be: what mesh topology achieves equivalent cluster-wide awareness, and at what cost? The answer (Table IV, $k_s - 1$ row: $>100\%$ overhead) actually strengthens the hierarchy's case but should be the primary comparison point.

**Concern 2: Command traffic topology-invariance claim.** The claim that $\eta_{\text{cmd}}$ is "topology-invariant" (repeated throughout) is true only under the specific assumption of centralized command generation with fixed $S_{\text{cmd}}$. The paper acknowledges this but the qualification is often buried in footnotes. In practice, hierarchical architectures enable cluster-local decision-making that could dramatically reduce command traffic—this is arguably the hierarchy's main advantage, yet the paper's workload model doesn't capture it. The topology-invariance claim, while technically correct under the stated assumptions, may mislead readers about the hierarchy's practical benefits.

**Concern 3: Coordinator failure recovery.** The RF-backup handoff recovery time of ~160 s (16 cycles) is substantial. The paper states this is "modest vs. P99 = 441 s" for AoI, but this comparison conflates two different failure modes. During coordinator failure recovery, the *entire cluster* loses coordination capability, not just one node's state freshness. The triple-fault scenario ($1.8 \times 10^{-5}$/yr) is dismissed as rare, but at $N = 10^5$ with 1,000 clusters, the fleet-level probability of at least one triple fault per year is $\sim 1.8\%$—not negligible.

**Concern 4: The $10^6$-node extrapolation.** Figure 10 includes a $10^6$-node analytical extrapolation that is not DES-validated. While labeled as such, including it in the figure implicitly extends the paper's claims beyond the validated range. The $O(N)$ scaling argument is sound for message counts but does not account for the multi-cluster channel reuse constraint (Section IV-A), which the paper itself identifies as "binding before the message-layer equations."

## 4. Clarity & Structure
**Rating: 4 (Good)**

The paper is well-organized and the writing is generally clear, though dense. The roadmap at the beginning of Section IV is helpful. The notation table (Table I) is essential given the number of symbols. The three-layer feasibility framework provides a clear organizing principle.

**Strengths:** The abstract is detailed and accurate (perhaps too detailed—it reads more like an executive summary). Table IX (Claim Map) is excellent. The operational context paragraph in Section I clearly motivates the 1 kbps focus. The superframe time budget (Table V) is a model of transparent engineering analysis.

**Weaknesses:** The paper is extremely long for the analytical depth. Much of the length comes from extensive qualification and cross-referencing (e.g., "Table~\ref{tab:schedulability}, not baseline telemetry alone" type parentheticals). While this thoroughness is admirable, it makes the paper difficult to read linearly. Section IV-A alone spans nearly 3 pages and mixes TDMA frame design, half-duplex partitioning, command dissemination models, multi-cluster reuse, synchronization, and guard-time sensitivity—each of which could be a separate subsection.

The paper would benefit from a clearer separation between the *design equations* (which are the claimed contribution) and the *verification/sensitivity analysis* (which supports them). Currently, the design equations are scattered across Sections IV-A through IV-E and then re-collected in Section V-C. Consider leading with the collected equations and then presenting verification.

Several figures are referenced but not shown (as this is LaTeX source without the actual PDFs). The figure captions are detailed and informative, suggesting the figures are well-designed.

## 5. Ethical Compliance
**Rating: 4 (Good)**

The paper includes an explicit acknowledgment of AI-assisted ideation (Claude 4.6, Gemini 3 Pro, GPT-5.2) with a reference to a methodology paper. This is transparent and appropriate. The disclaimer that the AI-assisted aspects "are not validated here" is honest.

The anonymous authorship ("Project Dyson Research Team") with a note that individual names will be provided for final publication is unusual but acceptable per the stated IEEE policy. The open-source code availability with a specific tag (`paper-02-v-bw`) supports reproducibility.

One concern: the paper cites "Claude 4.6" and "GPT-5.2"—these version numbers do not correspond to any publicly released models as of my knowledge. If these are internal/beta versions, this should be clarified. If the version numbers are speculative or placeholder, this is problematic.

## 6. Scope & Referencing
**Rating: 3 (Adequate)**

The paper is appropriate for IEEE TAES in scope, addressing autonomous spacecraft coordination at scale. The reference list (50+ entries) is comprehensive, covering constellation operations, swarm robotics, distributed systems theory, queueing theory, and relevant standards (CCSDS).

**Gaps:** The paper does not cite several directly relevant works: (1) Satellite Tool Kit (STK) or similar operational tools used for constellation coordination analysis; (2) Recent work on distributed satellite systems by Radhakrishnan et al. (2016, IEEE Access) on inter-satellite link design; (3) The substantial literature on cluster-based wireless sensor networks beyond LEACH (e.g., HEED, TEEN) which face analogous scaling challenges; (4) Recent AoI literature specific to satellite networks (e.g., Leyva-Mayorga et al., 2022).

Several references are non-archival (Amazon Kuiper overview, DARPA program pages, DoD fact sheets). While these provide context, the paper should not rely on them for technical claims. The Starlink FCC filing [1] is the primary operational reference but is a regulatory document, not a peer-reviewed technical source.

The paper cites O'Neill (1976) and Badescu (2006) to motivate the $10^5$–$10^6$ scale, but these are speculative infrastructure concepts, not engineering programs. The gap between current constellations (~7,000 nodes) and the paper's target range ($10^3$–$10^5$) is acknowledged but the practical relevance of the upper end ($10^5$) is not well-motivated by near-term programs.

---

## Major Issues

1. **Circular verification masquerading as validation.** The DES and closed-form equations implement identical message-layer accounting; their agreement is tautological for the overhead metric. The paper must clearly distinguish between (a) code verification (DES matches equations: confirmed), (b) model verification (equations correctly represent the intended abstraction: confirmed by slot-level sim for TDMA), and (c) model validation (abstraction represents physical reality: not performed). The abstract's phrasing "Monte Carlo tool verifies implementation consistency" is accurate but the paper's overall framing suggests stronger validation than exists. **Recommendation:** Restructure Section III-A to explicitly use V&V terminology (IEEE 1012 or similar) and downgrade claims accordingly.

2. **Missing physical-layer coupling analysis.** The paper identifies MAC contention, antenna scheduling, and multi-cluster channel reuse as future work, but these are not merely refinements—they are potentially *invalidating* constraints. At $N = 10^5$ with 1,000 clusters sharing 4 RF channels (Section IV-A), the inter-cluster scheduling problem dominates the intra-cluster TDMA problem that the paper solves. Without even a first-order analysis of this constraint, the paper's sizing equations are necessary but not sufficient conditions for feasibility. **Recommendation:** Add at minimum an analytical bound on multi-cluster scheduling feasibility (e.g., required number of orthogonal channels as a function of $N$ and spatial reuse factor).

3. **Unfair topology comparison.** The sectorized mesh comparison (65–67% overhead for 3.2% coverage vs. 46% for 100% coverage) compares protocols with fundamentally different functional scope, then draws conclusions about the hierarchy's superiority. The "14× bandwidth efficiency per unit of awareness" metric is particularly problematic. **Recommendation:** Either (a) design a mesh variant that provides equivalent cluster-wide awareness (even if it exceeds the budget, quantify by how much) or (b) restrict comparative claims to "the hierarchy provides cluster-wide awareness within the 1 kbps budget; no mesh variant tested can match this capability at this budget" without efficiency-per-peer metrics.

4. **Fleet-level coordinator failure probability.** The per-cluster coordinator failure analysis is adequate but the fleet-level implications at $N = 10^5$ (1,000 clusters) are not addressed. With 160 s RF-backup recovery per event and non-negligible fleet-level event rates, the aggregate impact on fleet coordination quality needs quantification. **Recommendation:** Add a fleet-level availability analysis: expected number of clusters in coordinator-recovery transient at any given time, and the resulting fleet-wide coordination degradation.

## Minor Issues

1. **Eq. 2 ($W_q$ for $M/D/1$):** The formula $W_q = \rho / (2\mu_s(1-\rho))$ is the standard $M/D/1$ result but should include the service time explicitly: $W_q = \rho / (2\mu_s(1-\rho))$ gives waiting time in queue, not sojourn time. Clarify units and confirm this is waiting time only (as stated).

2. **Table III, collision avoidance rate:** $10^{-4}$/node/s yields ~8.6 events/node/year. At $N = 10^5$, this is ~860,000 fleet-level alerts/year, or ~0.27/s. This seems high for screening notifications. Justify or cite source.

3. **Section III-B, Eq. 4 ($M_{\text{total}}$):** The equation counts uplink messages only. The paper states "the DES models full bidirectional traffic" but Eq. 4 doesn't reflect this. Clarify whether Eq. 4 is uplink-only and provide the bidirectional equivalent.

4. **Table V (Superframe):** The sync beacon is listed as TX (0.3 ms) within the ingress section. This is a TX event during the RX phase—clarify the timing (presumably at the start of the frame before member slots begin).

5. **Section IV-A, "Multi-cluster channel reuse":** The statement "$F = 4$ and $R = 3$: 12 simultaneous clusters" assumes independent spatial reuse, but LEO orbital geometry constrains which clusters can reuse channels. This needs qualification.

6. **Table VI (Joint Interaction):** The "No Loss" and "GE Only" columns are identical, which the paper explains as pipeline decoupling. But this means the GE model has *zero* impact on coordinator queue drops—a result that should be highlighted more prominently as it validates the compositional design approach.

7. **Section V-C, "Safe-mode floor":** The statement "Nominal ($\eta_{\text{total}} \approx 26\%$) survives Slotted ALOHA ($\gamma = 0.36$)" should clarify that this refers to throughput capacity, not collision probability—at $\rho = 0.72$ under Slotted ALOHA, packet delay variance would be substantial.

8. **Acknowledgment section:** "Claude 4.6, Gemini 3 Pro, GPT-5.2" — verify these model version numbers are accurate. They do not correspond to publicly known releases.

9. **Notation inconsistency:** $p_{\text{link}}$ (Table VIII) vs. $p_G$/$p_B$ (GE model) — clarify that $p_{\text{link}}$ in Table VIII is the Bernoulli per-packet delivery probability, distinct from the GE state-conditional probabilities.

10. **Missing CI widths:** Bootstrap 95% CIs are reported for AoI P99 ($[438, 444]$ s) but not for other tail metrics (GE P95 recovery, coordinator drops). Report CIs for all key results.

## Overall Recommendation

**Major Revision**

The paper addresses a real engineering need and provides a well-structured analytical framework for sizing hierarchical coordination in large space swarms. The three-layer feasibility decomposition, the TDMA superframe analysis, and the GE coherence-time sensitivity study are genuine contributions. However, three issues require substantial revision: (1) the verification/validation distinction must be sharpened throughout—the current framing overstates the confidence level of message-layer-only results; (2) the topology comparison with the sectorized mesh needs restructuring to avoid misleading efficiency claims across protocols with different functional scope; and (3) the multi-cluster channel reuse constraint, acknowledged as "binding before the message-layer equations," needs at least a first-order analytical treatment to establish that the intra-cluster sizing equations are not rendered moot by inter-cluster scheduling infeasibility. With these revisions, the paper would make a solid contribution as a systems engineering reference for mega-constellation coordination sizing.

## Constructive Suggestions

1. **Lead with the design equations.** Move the collected equations from Section V-C to a prominent position (e.g., Section II or early Section IV) and organize the rest of the paper as derivation and verification. This would make the paper immediately useful to practitioners and clarify the contribution.

2. **Add a multi-cluster scheduling feasibility bound.** Even a simple analysis—required number of orthogonal channels $F_{\min}(N, k_c, R)$ for all clusters to complete one coordination cycle—would significantly strengthen the paper by connecting the intra-cluster TDMA analysis to the fleet-level scheduling problem. This could be analytical (no simulation needed).

3. **Replace the per-peer efficiency metric with a Pareto analysis.** Instead of the "14× bandwidth efficiency per unit of awareness" comparison, present a Pareto frontier of overhead vs. awareness scope, showing where the hierarchy and various mesh configurations (cap = 5, 10, 20, 50, $k_s-1$) fall. This would be a more honest and more useful visualization of the design space.

4. **Conduct a single NS-3 validation case.** Even one validated NS-3 simulation of a single cluster ($k_c = 100$, 24 kbps TDMA, GE channel) would transform the paper from "message-layer predictions pending physical-layer validation" to "message-layer predictions validated at the single-cluster level." This is explicitly identified as the priority next step (Section VI) and would dramatically increase the paper's impact.

5. **Tighten the paper by 20–30%.** The extensive inline qualifications, while individually appropriate, collectively make the paper difficult to read. Move detailed caveats to a consolidated assumptions/limitations section and use forward references. The current 14+ page length could be reduced to ~10 pages without losing content by eliminating redundant cross-references and consolidating sensitivity analyses.