---
paper: "02-swarm-coordination-scaling"
version: "ae"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-27"
recommendation: "Major Revision"
---



# Peer Review: "Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study"

**Manuscript for IEEE Transactions on Aerospace and Electronic Systems**

---

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a real and growing engineering concern: how to coordinate very large autonomous spacecraft fleets beyond the capabilities of current centralized ground-based approaches. The scale range of $10^3$–$10^5$ nodes is timely given approved mega-constellation expansions (Starlink 42k, Kuiper 3.2k+), and the authors correctly identify that byte-level traffic accounting under a fixed per-node budget has not been systematically performed in the literature for this regime.

However, the novelty claim requires careful scrutiny. The authors repeatedly and commendably acknowledge that "individual metrics are analytically tractable in isolation" and that the DES serves as a "validated parametric design tool." This honesty is appreciated but simultaneously undermines the novelty argument. The $O(1)$ overhead scaling is, as stated, a direct mathematical consequence of the fixed-depth hierarchy with fixed fan-out—not a discovery. The AoI result matches the geometric distribution exactly. The GE retransmission result ($1 - 0.9^3 = 27.1\%$) is a one-line calculation. The question then becomes: does the systematic integration of these known results into a single framework constitute sufficient novelty for IEEE T-AES? The answer is borderline. The coordinator capacity sizing (Section IV-A) with its comparison of four scheduling models is the most novel contribution, as it provides actionable design guidance not readily available elsewhere. The workload decomposition showing that commands dominate the stress case is useful but unsurprising.

The paper would benefit from a stronger articulation of what the DES reveals that pure analysis cannot. The joint distribution of AoI across all node-coordinator pairs under simultaneous loss and exception reporting is mentioned but never quantitatively exploited—the reported P99 matches the marginal geometric prediction exactly. If the DES's value is integration, the paper should demonstrate cases where integration produces non-obvious interactions.

## 2. Methodological Soundness

**Rating: 3 (Adequate)**

The cycle-aggregated DES methodology is clearly described and appropriate for the research questions at the message-passing layer. The abstraction level is well-chosen for a parametric sweep study, and the authors are transparent about what is and is not modeled (Table 6). The Monte Carlo framework with 30 replications per configuration is standard, and the bootstrap confidence intervals are appropriate.

Several methodological concerns warrant attention:

**Near-zero variance undermines the MC framework.** The authors acknowledge (Section III-D) that SD < 0.001% across replications, meaning the simulation is essentially deterministic for the overhead metric. The 30-replication MC framework is then primarily confirming that the code correctly implements the analytical model, not exploring stochastic uncertainty. This is a validation exercise, not a Monte Carlo study in the traditional sense. The paper should be more forthright about this: the only stochastic element affecting most metrics is the 2%/year failure process, which perturbs an insignificant fraction of nodes per cycle. The latency and availability metrics presumably have more variance, but confidence intervals are not reported for these in Tables VII or VIII.

**The sectorized mesh comparator has questionable parameterization.** The $\sqrt{N}$ sector sizing (Section III-B.4) is derived from a heuristic nearest-neighbor argument that the authors themselves call "an order-of-magnitude sizing, not a precise orbital mechanics calculation." The capped fanout of 10 neighbors is a free parameter that dramatically affects the comparison: at cap = 5, the overhead ratio drops to $62.1\%/46\% \approx 1.35\times$; at cap = 50, it rises to $89.7\%/46\% \approx 1.95\times$. The headline "1.35–1.95×" range is thus an artifact of the chosen sweep bounds, not a robust architectural comparison. A more principled approach would derive the minimum neighbor count from conjunction screening requirements (e.g., probability of detecting a conjunction within a screening volume given $n$ monitored peers).

**The collision avoidance event rate ($10^{-4}$/node/s) is poorly justified.** The authors cite a 1000:1 screening-to-maneuver ratio, but this ratio is for current operations with ~7,000 Starlink satellites. At $10^5$ nodes in dense shells, the conjunction rate per node could be substantially higher due to $O(N^2)$ pairwise interactions. The sensitivity analysis (varying from $10^{-5}$ to $10^{-3}$) shows the qualitative ranking is preserved, which is reassuring, but the baseline parameterization should be better grounded.

**Validation against closed-form solutions is circular for the overhead metric.** The DES-to-analytical agreement of <0.1% (Table IX) demonstrates correct implementation of the traffic accounting model, not validation of the model against physical reality. The M/D/1 validation at $N = 100$ (Section III-A) and gossip convergence validation at $N \leq 1000$ (Section III-A) are more meaningful but cover only the reference baselines, not the hierarchical architecture under study.

## 3. Validity & Logic

**Rating: 3 (Adequate)**

The conclusions are generally well-supported by the analysis, and the authors are commendably careful about qualifying their claims. The paper has clearly undergone significant revision (this appears to be Version AE), and the hedging language is appropriate—e.g., the AoI-to-position-error coupling is explicitly labeled as "illustrative back-of-the-envelope" rather than a validated risk assessment.

Several logical issues deserve attention:

**The 1 kbps budget is simultaneously the most important and least justified assumption.** The authors motivate it as an RF backup constraint (Section III-F), but then note that optical ISLs provide 1–10 Gbps. If the coordination protocol must operate over 1 kbps RF backup, the entire overhead analysis is relevant; if it normally operates over optical ISLs at orders-of-magnitude higher rates, the overhead percentages become negligible and the study's practical relevance diminishes. The paper should more clearly distinguish between the "RF fallback" sizing case (where 46% overhead is binding) and the "normal optical operation" case (where 46% of 1 kbps is 460 bps out of a 1 Gbps link—essentially free). The claim that "since overhead is a dimensionless ratio, $\eta$ values apply at any $C_{\text{node}}$" (Section I-D) is technically correct but misleading: the *engineering significance* of 46% overhead depends entirely on whether the system is bandwidth-constrained.

**The centralized baseline is too weak.** The $c = 1$ single-server model saturates at $N = 10,000$, but the authors immediately acknowledge that $c = 100$ extends this to $10^6$ and that "the binding constraints on centralized architectures are propagation latency and uplink spectrum scarcity, not processing capacity." This admission effectively concedes that the centralized baseline comparison is not informative for the processing dimension. The propagation latency argument (10–240 ms round-trip) is valid but never quantitatively compared against the hierarchical latency (340–675 ms from Table VII), which is actually *worse*. The paper should address this apparent contradiction: if hierarchical coordination has higher latency than centralized ground processing, what is the advantage beyond fault tolerance?

**The "stress case" dominates the headline numbers but is acknowledged as extreme.** The abstract leads with $\eta \approx 46\%$, but the nominal operating point is $\eta \approx 5\%$. The $9\times$ design envelope is useful, but the paper's framing (abstract, title implications) emphasizes the stress case. The nominal case—where the hierarchical architecture adds only 5% overhead beyond baseline telemetry—is arguably the more important result for system designers, as it shows the architecture is lightweight during routine operations.

**Per-cycle completion analysis (Section IV-C) conflates link loss with coordination failure.** The finding that per-cycle full completion drops below 1% under 50% i.i.d. loss is mathematically correct but operationally misleading. As the authors note, a coordinator receiving 95/100 reports can still compute a useful summary. The paper should lead with the relaxed threshold analysis rather than the full-completion metric, which sets an unrealistically strict bar.

## 4. Clarity & Structure

**Rating: 4 (Good)**

The paper is well-organized and clearly written for its length. The roadmap at the beginning of Section IV is helpful, and the consistent use of Table V (traffic accounting) as a reference point for all overhead calculations aids reproducibility. The design equations summary (Section V-C) is a valuable addition for practitioners.

Several structural issues could be improved:

**The paper is excessively long for the novelty content.** At approximately 12,000 words of body text plus extensive tables and figures, this manuscript exceeds typical T-AES length guidelines. Much of the length comes from careful qualification and cross-checking, which is admirable but could be condensed. For example, the sectorized mesh model (Section III-B.4) spans nearly two full columns and includes three tables (Tables II, IV, V) for what is ultimately a comparator architecture. The neighbor-cap sensitivity (Table IV) could be moved to an appendix.

**Table density is high.** The paper contains 12 tables, many of which report near-identical overhead values (e.g., Table IX shows $\eta = 46.0\%$ at every fleet size). While this confirms the $O(1)$ scaling, a single sentence stating "DES-measured $\eta = 46.0 \pm 0.001\%$ at all ten fleet sizes" would suffice, with the full table in supplementary material.

**Figure references are sometimes forward-looking.** For instance, Fig. 1 (architecture diagram) is referenced in Section III-B.2 but the figure itself is described as showing "message aggregation ratios at each level"—these ratios are not labeled in the caption or (presumably) the figure. Several figures (e.g., Figs. 5, 8, 10, 11) are referenced but their content must be inferred from captions since the actual graphics are not available for review. The captions are generally informative but should be self-contained.

**The abstract is dense but accurate.** It correctly conveys the four main results and their qualifications. However, at 250+ words, it pushes the upper limit for T-AES and could be tightened by removing the sectorized mesh comparison (which is a secondary result).

## 5. Ethical Compliance

**Rating: 4 (Good)**

The paper includes an appropriate acknowledgment of AI-assisted ideation (Claude 4.6, Gemini 3 Pro, GPT-5.2) in the Acknowledgment section, with a clear statement that the AI-generated concepts "are not validated in the current study." The reference to a companion methodology paper [49] provides a traceable record of the AI involvement. This level of disclosure exceeds current IEEE requirements and is commendable.

The author attribution ("Project Dyson Research Team" with a note that individual names will be provided for final publication) is unusual but acceptable for a review manuscript. The data availability statement with a specific repository tag (`paper-02-v-ae`) supports reproducibility.

One concern: the Acknowledgment references "Claude 4.6," "Gemini 3 Pro," and "GPT-5.2"—model versions that do not exist as of the reviewer's knowledge cutoff. If these are speculative future versions, this should be clarified; if the paper is set in a near-future context, this is unconventional for a technical journal submission and may confuse readers.

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is within scope for IEEE T-AES, which publishes work on space systems, autonomous systems, and communication architectures. The combination of distributed systems theory, queueing analysis, and space systems engineering is appropriate for the journal's readership.

The reference list (53 items) is comprehensive and covers the relevant literature in constellation management, swarm robotics, distributed algorithms, and space communication standards. Key works are cited appropriately: Lynch [7] for distributed algorithms, Kleinrock [27] for queueing theory, Demers et al. [28] for gossip protocols, and the CCSDS standards [31, 42] for space communication protocols.

However, several gaps exist:

- **No references to actual ISL implementations.** The paper assumes 1–10 Gbps optical ISLs but cites no literature on optical ISL performance, link acquisition times, or pointing constraints—all of which are abstracted away but acknowledged as important. Recent work by Kaushal and Kaddoum (IEEE Commun. Surveys Tuts., 2017) on free-space optical communication, or Chaudhry and Musumpuka (IEEE Access, 2021) on ISL architectures, would strengthen the physical-layer discussion.

- **Missing references on DTN for satellite networks.** The paper repeatedly mentions DTN/BPv7 as future work but cites only the original RFC 4838 and CCSDS BPv7 standard. Recent work on DTN performance in LEO constellations (e.g., Fraire et al., IEEE/ACM Trans. Netw., 2021) would contextualize the inter-cycle store-and-forward discussion.

- **Several references are non-archival.** References [1], [3], [17], [18], [19], and [22] are websites, press releases, or non-peer-reviewed sources. While some (SpaceX, DARPA) are unavoidable, the paper should minimize reliance on non-archival sources for technical claims.

- **The companion methodology paper [49] is self-published** on the project website and not peer-reviewed, yet is cited as supporting the AI methodology disclosure. This is acceptable for transparency but should not be relied upon for technical claims.

---

## Major Issues

1. **The DES adds negligible value beyond closed-form analysis for the reported metrics.** The overhead metric matches analytical predictions to within 0.1% with SD < 0.001%. The AoI P99 matches the geometric distribution exactly. The GE retransmission result is a one-line calculation. The paper must either (a) demonstrate a metric where the DES reveals behavior not predicted by analysis (e.g., joint AoI distributions, transient coordinator overload during handoff cascades, interaction between exception telemetry and GE losses), or (b) reframe the contribution more modestly as a validated reference implementation and parametric design tool—which the current version partially does but then contradicts by positioning results as "DES-unique contributions" (Section IV roadmap).

2. **The sectorized mesh comparison lacks principled parameterization.** The neighbor cap (5–50) and sector size ($\sqrt{N}$) are free parameters whose values determine the overhead ratio. Without grounding these in conjunction screening requirements derived from orbital mechanics, the 1.35–1.95× comparison is not actionable. At minimum, the paper should state what conjunction detection probability each cap value achieves under a simplified screening model, or explicitly defer this to future work and weaken the comparative claims accordingly.

3. **The 1 kbps budget creates a misleading framing.** Under normal optical ISL operation, the overhead percentages are engineering-irrelevant (460 bps out of Gbps-class links). Under RF fallback, the stress-case 46% overhead plus 20.5% baseline = 66.5% utilization is concerning but the nominal 5% + 20.5% = 25.5% is comfortable. The paper should present results for both regimes explicitly, rather than implying the 46% figure is always the relevant design point.

4. **Hierarchical latency exceeds centralized latency but this is never discussed.** Table VII shows hierarchical latency of 340–675 ms at $N = 10^4$–$10^5$, while centralized ground processing latency is dominated by propagation delay (10–240 ms round-trip for LEO-to-ground). The hierarchical architecture's latency advantage over centralized is unclear from the presented data. If the advantage is fault tolerance rather than latency, this should be stated explicitly and the latency comparison should be presented honestly.

---

## Minor Issues

1. **Eq. (4), line defining $M_{\text{total}}$**: This counts only uplink messages. The text below acknowledges this but the equation should be labeled as "uplink only" or a bidirectional version should be provided.

2. **Table I ($M/D/c$ sensitivity)**: The "Representative System" column labels are speculative (e.g., "Hyperscale data center" for $c = 1000$). These should be labeled as illustrative examples, not representative systems.

3. **Section III-B.3**: The convergence formula $R_{\text{conv}} = \max(\lceil\log_2 N\rceil, \lceil N/(bf)\rceil)$ conflates two different convergence requirements (epidemic spread vs. throughput-limited delivery) without formal justification. A brief derivation or reference would help.

4. **Table VI (Simulation Parameters)**: The footnote markers are inconsistent—footnote (b) is missing, and footnotes (c) and (d) appear without (b).

5. **Section IV-A**: "Model B: Leaky-bucket shaper (recommended baseline)" — the paper should clarify that this is a *simulation model recommendation*, not an operational system recommendation, since the authors have not validated the model against real hardware.

6. **Eq. (11), AoI analytic cross-check**: The ceiling function $\lceil \cdot \rceil$ is correct but the derivation assumes the AoI is sampled at the worst case (just before the next report). The DES samples every 100 s (Table VIII footnote), which would produce a different distribution. The close agreement (441 vs. 440 s) suggests the sampling interval is small relative to the P99 value, but this should be noted.

7. **Section III-B.4**: "first node in each sector" as sector coordinator is an arbitrary choice that should be justified or noted as a simplification.

8. **Table XII (Link Availability)**: Footnote markers (b) and (c) are swapped—the "Per-message delivery rate" note is marked (b) but the column header references it for the delivery percentage, while (c) refers to offered load exceeding 100%.

9. **Abstract**: "byte-level traffic accounting" is slightly misleading since the simulation operates at the message level, not the byte level. "Message-level traffic accounting with byte-granularity sizing" would be more precise.

10. **References**: [29] (Castet and Saleh) covers satellite reliability broadly but does not specifically address "modern small satellites in low Earth orbit" as claimed. More recent CubeSat/SmallSat reliability data (e.g., Langer and Bouwmeester, 2016) would be more appropriate.

---

## Overall Recommendation

**Major Revision**

The paper addresses a relevant problem, is carefully written with appropriate qualifications, and provides useful parametric design guidance for hierarchical coordination of large spacecraft swarms. The coordinator capacity sizing, AoI characterization, and correlated loss analysis are individually sound. However, the central methodological contribution—the DES—adds negligible value beyond closed-form analysis for the metrics actually reported, undermining the paper's claim as a simulation study. The sectorized mesh comparison lacks principled parameterization, the 1 kbps budget framing is misleading for normal operations, and the paper is longer than warranted by its novelty content. A major revision should demonstrate DES-unique insights (joint distributions, transient dynamics, parameter interactions not captured by marginal analysis), ground the sectorized mesh comparison in orbital mechanics, and condense the presentation. With these changes, the paper could make a solid contribution to T-AES as a parametric design reference for mega-constellation coordination architectures.

---

## Constructive Suggestions

1. **Demonstrate a DES-unique result.** Run a scenario where multiple parameters interact in ways not predicted by marginal analysis—e.g., simultaneous GE burst loss + coordinator handoff + exception telemetry. If the joint effect on cluster-level AoI or coordination success differs from the product of marginal effects, this would justify the DES methodology. Alternatively, model transient coordinator overload during cascading handoffs (e.g., a solar particle event triggering simultaneous coordinator failures across an orbital region) and show that the transient dynamics produce non-obvious bottlenecks.

2. **Ground the sectorized mesh in conjunction screening.** Derive the minimum neighbor count from a simplified conjunction detection model: given $N$ nodes in a shell, what is the probability that a conjunction partner is among the $n$ monitored peers? This converts the free parameter (cap = 5–50) into a detection probability, making the overhead comparison actionable. Even a back-of-the-envelope calculation (e.g., assuming uniform distribution in a shell) would substantially strengthen the comparison.

3. **Present a dual-regime analysis.** Show results at both $C_{\text{node}} = 1$ kbps (RF fallback) and $C_{\text{node}} = 100$ kbps (optical ISL coordination allocation). At 100 kbps, the stress-case overhead drops to 0.46% and the coordinator ingress requirement becomes trivial relative to the ISL capacity. This would clarify when the overhead analysis is engineering-relevant and when it is academic.

4. **Condense the presentation by 25–30%.** Move the full fleet-size sweep table (Table IX) to supplementary material (one sentence suffices for the $O(1)$ result). Consolidate the sectorized mesh tables (Tables II, IV, V) into a single table. Shorten Section III-B.3 (global-state mesh) since it is an intentional upper bound that the authors acknowledge is unrealistic. Target 9,000–10,000 words of body text.

5. **Add a packet-level validation for one configuration.** Even a single NS-3 or OMNeT++ run for a 100-node cluster with realistic TDMA scheduling would ground the $\gamma$ assumption and demonstrate that the message-layer abstraction is valid. This would address the most critical limitation (Section V-B) and significantly strengthen the paper's credibility for the T-AES audience, which expects physical-layer awareness.