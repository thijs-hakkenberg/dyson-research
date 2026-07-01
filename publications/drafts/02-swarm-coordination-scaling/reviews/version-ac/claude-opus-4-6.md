---
paper: "02-swarm-coordination-scaling"
version: "ac"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-27"
recommendation: "Major Revision"
---

# Peer Review: "Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms"

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a legitimate gap: systematic, byte-level traffic characterization of hierarchical coordination architectures for autonomous spacecraft swarms at the $10^3$–$10^5$ scale. The authors correctly identify that existing literature covers swarm robotics at small scales, constellation management at moderate scales, and networking architectures for mega-constellations, but rarely combines autonomous (non-ground-directed) coordination with explicit byte-level overhead accounting at $10^4$+ nodes. The four contributions—coordinator capacity sizing, AoI-based coordination quality, correlated loss characterization, and workload design envelope—are individually useful for system designers.

However, the novelty is significantly tempered by the authors' own repeated acknowledgment that individual results are "analytically tractable in isolation." The $O(1)$ overhead scaling is, as stated, a direct mathematical consequence of fixed-depth hierarchy with fixed fan-out—this is well-known from distributed systems theory (Lynch, 1996, which the authors cite). The AoI result matches the geometric distribution exactly (Eq. 16, confirmed to within one cycle). The GE loss result ($1 - 0.9^3 = 27.1\%$) is a one-line calculation. The claimed contribution of "systematic integration across the full parameter space" is reasonable in principle, but the near-zero MC variance (SD < 0.001%) and sub-0.1% DES-to-analytical agreement raise the question of whether the DES is genuinely integrating interacting effects or simply computing the same closed-form expressions with extra machinery. The paper would benefit from identifying at least one result where the DES reveals behavior that is *not* predictable from the analytical model—the joint AoI distribution under simultaneous link losses and exception reporting is mentioned but not demonstrated to produce surprising outcomes.

The sectorized mesh comparator is a welcome addition that provides a more realistic decentralized baseline than the global-state mesh upper bound. However, the $1.35$–$1.95\times$ overhead ratio is again largely determined by the message size parameterization rather than emergent simulation dynamics.

## 2. Methodological Soundness

**Rating: 3 (Adequate)**

The cycle-aggregated DES framework is clearly described and the abstraction level is explicitly documented (Table VI). The choice to operate at the message layer rather than the packet layer is defensible for a parametric design-space study, and the authors are commendably transparent about what is and is not modeled. The Monte Carlo framework (30 replications, bootstrap CIs) is appropriate, and the validation against M/D/1 analytical solutions and gossip convergence bounds provides confidence in the implementation.

Several methodological concerns warrant attention:

**The 1 kbps budget is simultaneously the most important and least justified parameter.** The authors argue it represents an RF backup constraint (S-band TT&C during optical outages), but then analyze the system as if this is the *primary* coordination channel. If the optical ISL is the normal operating link (1–10 Gbps), the coordination protocol would typically run over the optical link with RF as fallback. The entire overhead analysis ($\eta$ values, channel saturation conclusions, TDMA requirements) is predicated on this single parameter. The statement "results scale linearly with $C_{\text{node}}$" (Section III-F) is true but somewhat undermines the specificity of the numerical results. A sensitivity analysis varying $C_{\text{node}}$ over at least one order of magnitude would strengthen the paper.

**The collision avoidance event rate ($10^{-4}$/node/s) is three orders of magnitude higher than operational maneuver rates.** The authors justify this as screening events rather than maneuvers, citing a 1000:1 ratio. While this ratio is plausible, the sensitivity analysis showing only ±1.5 percentage points variation suggests this parameter has minimal impact—which raises the question of why collision avoidance is modeled at all, given it contributes ~0.1 bps per node (Table VIII).

**The fixed 4-level hierarchy is never justified against alternatives.** Why not 3 levels or 5? The paper states "hierarchy depth is fixed at 4 levels throughout this study" but does not explore whether depth is a meaningful design parameter. For $N = 10^3$, a 4-level hierarchy with the stated fan-outs seems over-structured; for $N = 10^5$, it may be under-structured.

**The coordinator election model is underspecified.** The Raft-style consensus is mentioned (Section III-H) but the interaction between election latency, cluster dead time, and coordination quality during transitions is not characterized beyond the statement that dead time contributes "<0.01% availability loss." Under correlated failures (acknowledged as unmodeled), multiple simultaneous coordinator losses could produce cascading election storms.

## 3. Validity & Logic

**Rating: 3 (Adequate)**

The conclusions are generally supported by the analysis, and the authors are careful to qualify their claims. The distinction between reference bounds (intentional worst-case) and the architecture under study is clearly maintained. The acknowledgment that the centralized baseline with $c = 1$ is deliberately pessimistic (Table II) is appropriate.

However, several logical issues deserve attention:

**The topology comparison (Table X, Fig. 5) is not a fair comparison.** The centralized model uses $c = 1$ (intentionally worst-case), the global-state mesh requires full fleet state replication (intentionally worst-case), and the hierarchical model uses optimized parameters. While the authors label these as "reference bounds," the paper's structure and figures inevitably invite the reader to conclude that hierarchical is "better"—a conclusion that is largely an artifact of the baseline parameterization. The $M/D/c$ sensitivity (Table II) shows that with $c = 100$, centralized processing scales to $10^6$ nodes, and the authors acknowledge that "the binding constraints on centralized architectures are propagation latency and uplink spectrum scarcity, not processing capacity." This is a crucial admission that somewhat undermines the motivation for the entire study: if centralized architectures are not processing-limited, the hierarchical architecture's advantage must be demonstrated on latency and spectrum grounds—which the paper does not do rigorously.

**The per-cycle cluster completion metric (Section IV-C) conflates two different operational requirements.** Requiring *all* $k_c$ members to report in a single cycle is an extremely stringent criterion that may not be operationally necessary. A coordinator can function with partial cluster state; the paper should discuss what fraction of reports is *sufficient* for coordination decisions rather than treating 100% completion as the only acceptable outcome.

**The AoI-to-position-error coupling (Eq. 17) is acknowledged as first-order but is then used to draw operational conclusions** ("below the >1 km action threshold"). The linear growth model ($\dot{\sigma} = 0.5$ m/s) is reasonable for short timescales but becomes increasingly inaccurate over the 440 s P99 AoI window, where atmospheric drag variability, solar radiation pressure, and maneuver uncertainty produce nonlinear covariance growth. The caveat is present but the conclusion is still stated.

**Table IX (cluster size sensitivity) shows suspiciously discrete latency values.** The latency jumps from 508 ms to 340 ms between $k_c = 75$ and $k_c = 100$ at $N = 10^4$, with no intermediate values. This suggests the latency is dominated by a discrete queueing effect (likely the number of summaries per regional coordinator crossing a threshold) rather than a smooth function. This discretization should be explained.

## 4. Clarity & Structure

**Rating: 4 (Good)**

The paper is well-organized with a clear roadmap at the beginning of Section IV. The abstract is accurate and specific, providing quantitative results rather than vague claims. The use of tables to summarize parameters (Table IV), abstraction scope (Table VI), and traffic accounting (Table VII) significantly aids reproducibility. The distinction between message-layer and MAC-layer overhead is consistently maintained throughout.

The paper is, however, quite long and repetitive. The same $\eta \approx 46\%$ figure is stated in the abstract, introduction, contributions list, multiple results subsections, and conclusion. The coordinator capacity result (21–50 kbps) appears in at least six locations. While some repetition aids readability, the current level suggests the paper could be tightened by ~20% without loss of content. Specifically:

- Section III-F (Communication Overhead Definition) and Section III-G (Traffic Accounting) could be merged.
- The extensive discussion of the global-state mesh (Section III-B.3) is disproportionate to its role as an intentional upper bound that the authors acknowledge is unrealistic.
- Table V (State Completeness by Topology) adds little beyond what is stated in prose.

The notation is generally consistent, though the use of $\eta$ for protocol overhead (excluding baseline telemetry) while also discussing $\eta_{\text{total}}$ and $\eta_{\text{eff}}$ creates some confusion. A notation table would help.

Figures are referenced but provided as PDF placeholders; I cannot evaluate their quality. The captions are informative and appropriately detailed.

## 5. Ethical Compliance

**Rating: 4 (Good)**

The paper includes an explicit acknowledgment of AI-assisted ideation (Claude 4.6, Gemini 3 Pro, GPT-5.2) in the Acknowledgment section, with a clear statement that the AI-generated concepts "are not validated in the current study." This is commendable transparency. The data availability statement provides repository links, tags, and software versions, supporting reproducibility.

Two minor concerns: (1) The author block uses a team name ("Project Dyson Research Team") with a footnote promising individual names for final publication. IEEE policy requires named authors; this should be resolved before acceptance. (2) The reference to "Claude 4.6" and "GPT-5.2" suggests either future model versions or fictional version numbers (as of my knowledge cutoff), which is unusual and should be clarified—if these are actual tools used, the version numbers should be verifiable.

The collision avoidance event rate discussion and conjunction screening implications are handled responsibly, with appropriate caveats about the limitations of the position-error model.

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is appropriate for IEEE TAES in its focus on autonomous spacecraft coordination architectures. The reference list (48 citations) covers the relevant domains: distributed systems theory, swarm robotics, constellation management, queueing theory, and space communications standards.

However, several gaps exist:

- **No references to actual ISL implementations.** The paper assumes 1–10 Gbps optical ISLs but does not cite the substantial literature on operational laser communication terminals (e.g., EDRS, LCRD, Starlink's ISL implementation). This is relevant because the handoff state transfer (10–50 MB over optical ISL) and the coordinator bandwidth pooling both depend on ISL availability and capacity.

- **Missing references on space network simulation.** The paper does not cite existing space network simulation tools (e.g., SNS3 for NS-3, or the STK Communications module) that could provide the packet-level validation the authors identify as future work. Acknowledging these tools would strengthen the discussion of limitations.

- **The AoI literature coverage is adequate** (Kaul, Yates, Kadota) but could include more recent work on AoI in multi-hop networks and scheduling-aware AoI optimization, which is directly relevant to the hierarchical topology.

- **Several references are non-archival** (SpaceX website, Amazon website, DARPA program pages, DoD fact sheets). While unavoidable for some operational programs, the paper relies on these for key claims about current constellation scale and operational practices. At minimum, the ESA Space Debris Office report [55] and Castet & Saleh [36] provide archival grounding for the failure and conjunction rate parameters.

- **Self-citation [41] ("dyson_multimodel")** is to an apparently unpublished companion paper at a project URL. This should be clearly marked as a preprint/working paper if not yet peer-reviewed.

## Major Issues

1. **The DES adds minimal value beyond closed-form analysis.** The sub-0.1% DES-to-analytical agreement and near-zero MC variance indicate that the simulation is essentially computing the same deterministic traffic accounting as the closed-form model. The paper needs to either (a) identify specific results where the DES reveals emergent behavior not captured by analysis, or (b) reframe the contribution more honestly as a "validated reference implementation and parameter sweep tool" rather than implying the DES discovers new phenomena. The joint AoI distribution under combined loss and exception reporting is a candidate for (a) but is not exploited.

2. **The 1 kbps budget drives all quantitative conclusions but is weakly justified.** The RF backup argument is plausible but the paper then treats 1 kbps as the primary operating constraint. If the system normally operates over optical ISLs at orders-of-magnitude higher rates, the entire overhead analysis applies only to a degraded fallback mode. The paper should either (a) present results at multiple $C_{\text{node}}$ values to demonstrate robustness, or (b) more carefully scope the applicability of the 1 kbps results to the RF-backup scenario.

3. **The topology comparison is structurally biased.** The centralized baseline ($c = 1$) and global-state mesh (full replication) are intentionally worst-case, making the hierarchical architecture appear favorable by construction. The sectorized mesh is a better comparator but its $1.35$–$1.95\times$ overhead ratio is modest and parameter-dependent. The paper should present the $M/D/c$ centralized model with realistic $c$ values (e.g., $c = 10$–$100$) as a primary comparator, not just a sensitivity table, and should discuss the latency and spectrum advantages of hierarchical coordination over parallelized centralized processing.

4. **No validation against any physical-layer or packet-level simulation.** The MAC efficiency factor $\gamma \in [0.7, 0.9]$ is assumed but never validated. Given that the paper's conclusions about channel saturation (e.g., "Slotted ALOHA insufficient, TDMA required") depend critically on $\gamma$, at least a simplified packet-level validation for a single cluster would substantially strengthen the claims.

## Minor Issues

1. **Eq. 4 ($M_{\text{total}}$):** This counts only uplink messages but the text immediately states "the DES models the full bidirectional traffic." The equation should either include bidirectional terms or be clearly labeled as uplink-only.

2. **Table IX (cluster size):** The latency column shows only two discrete values (508 ms and 675 ms at $N = 10^5$). This should be explained—is the latency quantized by the number of regional coordinator queue slots?

3. **Section III-B.3:** The convergence round formula $R_{\text{conv}} = \max(\lceil\log_2 N\rceil, \lceil N/(bf)\rceil)$ conflates two different bottlenecks (epidemic spread time vs. throughput limit) without clearly explaining the transition. At $N = 10^5$, the throughput term dominates, meaning convergence is not epidemic-like at all—it is simply a bulk transfer.

4. **Table VI (Simulation Parameters):** The footnote marker "c" appears in the table but the corresponding footnote text uses the same superscript as a column in Table XII. This creates cross-reference confusion.

5. **Section IV-A:** "At $C_{\text{coord}} = 1$ kbps, 100% of inbound messages are dropped" appears after Table VIII already shows this result, creating redundancy.

6. **The paper uses "coordination success rate" and "per-message delivery rate" and "per-cycle completion" somewhat interchangeably in early sections** before the formal definitions in Section III-H. The metric definitions should appear earlier or forward references should be more explicit.

7. **Eq. 12 ($B_{\text{sector}}^{\text{uncapped}}$):** Missing the inter-sector relay term that appears in the capped version's traffic accounting.

8. **Section III-E (Monte Carlo Framework):** "seeds 42–71" is an implementation detail that does not belong in the methodology description. What matters is that seeds are independent, which is already stated.

9. **The Acknowledgment section mentions "Claude 4.6," "Gemini 3 Pro," and "GPT-5.2"**—these version numbers do not correspond to any publicly released models as of my knowledge. If these are internal/beta versions, this should be noted; if fictional, they should be removed.

10. **Reference [1] (Starlink operations):** "accessed February 2026" suggests the paper was written with knowledge of future events. This date should be verified.

## Overall Recommendation

**Major Revision**

The paper addresses a relevant problem and provides a well-documented parametric study with commendable transparency about assumptions and limitations. The four contributions (coordinator sizing, AoI characterization, correlated loss analysis, workload envelope) are individually useful for system designers. However, the near-perfect DES-to-analytical agreement undermines the claimed contribution of the simulation framework, the 1 kbps budget assumption drives all quantitative conclusions without adequate justification or sensitivity analysis, and the topology comparison is structurally biased by intentionally worst-case baselines. The paper reads more as a validated reference implementation with parameter sweeps than as a study revealing new scaling phenomena. A major revision should (1) demonstrate at least one DES result that diverges meaningfully from closed-form prediction, (2) present results at multiple $C_{\text{node}}$ values, (3) strengthen the topology comparison with realistic centralized baselines, and (4) ideally include at least a simplified packet-level validation for a single cluster.

## Constructive Suggestions

1. **Exploit the DES for what analysis cannot do.** Run scenarios with simultaneous coordinator failures, correlated link outages across orbital regions, and dynamic cluster reassignment under load. These are precisely the cases where closed-form analysis breaks down and a DES adds genuine value. Even one such scenario demonstrating emergent behavior (e.g., cascading coordinator elections under correlated failures producing a latency spike not predicted by the i.i.d. model) would substantially strengthen the novelty claim.

2. **Present a "realistic centralized" comparator.** Add a column to Table X and Fig. 5 showing the $M/D/c$ centralized model with $c = 10$ or $c = 100$, including propagation latency to ground. This would make the hierarchical architecture's advantage concrete: not processing capacity (which centralized can scale) but latency (which it cannot). Quantify the latency advantage as a function of orbital altitude.

3. **Validate $\gamma$ with a packet-level experiment.** Even a single NS-3 or OMNeT++ simulation of one 100-node cluster with TDMA scheduling over a realistic optical ISL model would ground the $\gamma \in [0.7, 0.9]$ assumption and demonstrate that the message-layer abstraction is valid. This would transform the paper from a purely analytical/message-layer study to one with physical-layer grounding.

4. **Restructure around the design envelope rather than the headline number.** The $9\times$ spread ($\eta \in [5\%, 46\%]$) is more informative than the stress-case $\eta = 46\%$ alone. Lead with the workload decomposition (currently Section IV-D) to establish that the overhead is workload-dominated, then present coordinator sizing and AoI as design tools for navigating the envelope. This reframing would better match the paper's actual contribution.

5. **Add a $C_{\text{node}}$ sensitivity sweep.** Present key results (coordinator zero-drop threshold, AoI, channel saturation) at $C_{\text{node}} \in \{0.1, 1, 10, 100\}$ kbps. This would demonstrate the generality of the framework and help readers apply the results to their specific link budgets, rather than anchoring everything to the 1 kbps assumption.