---
paper: "02-swarm-coordination-scaling"
version: "bl"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-27"
recommendation: "Major Revision"
---

# Peer Review: "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms"

## 1. Significance & Novelty
**Rating: 3 (Adequate)**

The paper addresses a genuine gap: there is no published work providing closed-form parametric sizing equations for hierarchical coordination architectures at the $10^3$–$10^5$ node scale with byte-level traffic accounting. The authors correctly identify that swarm robotics literature operates at 10–100 agents, constellation management at ~$10^4$ nodes, and networking literature treats routing rather than coordination overhead. The three-layer feasibility decomposition (byte budget, MAC efficiency, TDMA airtime) is a useful conceptual contribution.

However, the novelty is tempered by the fact that the "closed-form equations" are relatively straightforward accounting identities rather than deep analytical results. Equation (4) for hierarchical message count is elementary combinatorics; Equation (7) for AoI P99 is a standard geometric quantile; the GE recovery analysis is a textbook Markov chain calculation. The intellectual contribution lies more in the systematic assembly and cross-checking of these relationships than in any individual derivation. This is useful engineering work, but the theoretical depth is modest for a top-tier journal.

The central finding—that architecture-specific overhead ($\eta_0 \approx 5\%$) is small while command traffic dominates—is important but somewhat unsurprising once the accounting is laid out. The topology-invariance of command traffic is essentially definitional given the assumed workload semantics (centralized command generation). The paper would benefit from more clearly articulating what non-obvious insight emerges from this analysis that would change engineering practice.

## 2. Methodological Soundness
**Rating: 3 (Adequate)**

The methodology has both strengths and significant concerns. On the positive side, the paper is admirably transparent about its assumptions, the DES architecture is clearly described, and the Monte Carlo configuration (30 replications, bootstrap CIs) is appropriate. The separation of message-layer analysis from physical-layer effects is clearly stated, and the role of $\gamma$ as an abstraction parameter is well-defined.

**Concern 1: Circular validation.** The DES and closed-form equations operate at the same abstraction level with the same assumptions. The $<0.1\%$ agreement (Table VI) confirms only that the DES correctly implements the equations—not that the equations are valid models of physical systems. The authors acknowledge this (Section V-A), but the paper's framing sometimes overstates the validation. For instance, the abstract states the "Monte Carlo tool verifies equation consistency to $<0.1\%$"—this is implementation verification, not validation, and the distinction should be more prominent throughout.

**Concern 2: The fluid-server DES vs. TDMA analysis disconnect.** Table IV (joint interaction) uses fluid-server ingress, but the paper's primary contribution is TDMA sizing. The DES never actually simulates TDMA slot scheduling, half-duplex partitioning, or the 623 ms margin. This means the most operationally critical results (Table III superframe budget, Eq. 8 unicast stagger) are purely analytical with no simulation cross-check. The paper should either implement TDMA in the DES or more prominently flag this gap.

**Concern 3: Static topology assumption.** The 1-year simulation with fixed cluster membership is a significant simplification for LEO constellations. The $<0.5\%$ overhead bound for re-association (Section V-B) accounts only for byte overhead, not for transient coordination gaps, state inconsistency, or the interaction between cluster churn and GE loss events. The quantitative bound ($f_h = 0.8\%$) assumes independence between re-association events and link quality, which may not hold.

**Concern 4: GE model granularity.** The per-cycle GE state transition (constant state within $T_c = 10$ s) is a strong assumption. The authors argue it is conservative for recovery, but it also means the model cannot capture partial-cycle recovery or the interaction between retry timing and fade duration. The "coherence time bounds" discussion (Section IV-C) is helpful but remains qualitative.

## 3. Validity & Logic
**Rating: 3 (Adequate)**

The internal logic is generally sound, and the authors are commendably careful about qualifying their claims. The three-layer feasibility framework is logically coherent, and the distinction between architecture-specific ($\eta_0$) and workload-dependent ($\eta_{\text{cmd}}$) overhead is well-maintained throughout.

**Issue 1: The sectorized mesh comparison is not apples-to-apples.** The paper acknowledges this (Table VII, Section III-B.4), but the overhead comparison ($\eta_{\text{hier}} = 46\%$ vs. $\eta_{\text{sector}} = 65\%$) and the "14× bandwidth efficiency per peer" claim are misleading because the two architectures provide fundamentally different services. The capped mesh at cap=10 is not a coordination architecture—it's a local monitoring scheme. Comparing their overhead is like comparing the fuel cost of a bicycle and a truck without noting they carry different loads. The paper should either (a) design a sectorized mesh variant that provides comparable coordination functionality, or (b) restrict the comparison to clearly stated functional equivalences.

**Issue 2: The 99.5% availability figure.** This appears in Table V but its derivation is unclear. Section IV-H mentions a "two-state Markov (MTTF = 50 yr, MTTR ≈ 35 s)" yielding per-coordinator $A > 99.99\%$, then states "the 99.5% in Table V conservatively accounts for cascading effects." This is hand-waving—what cascading effects, quantified how? The triple-fault analysis (Section III-B.2) gives $1.8 \times 10^{-5}$/yr per cluster, which would not degrade availability to 99.5%. The gap between 99.99% per-coordinator and 99.5% system-level needs rigorous derivation.

**Issue 3: Extrapolation claims.** Figure 8 includes a $10^6$-node analytical extrapolation curve, and the abstract mentions $10^5$ nodes, but the DES validates only up to $10^5$. The $O(N)$ scaling argument is sound for message count, but coordinator ingress, GE recovery, and AoI are all per-cluster metrics that don't depend on $N$—so the "scaling" result is really that per-cluster metrics are $N$-independent, which is trivially true given the hierarchical decomposition. The paper should be more precise about what "scales to $10^5$" actually means.

**Issue 4: Command traffic topology-invariance claim.** The statement that $\eta_{\text{cmd}}$ is "topology-invariant" (repeated multiple times) is true only under the specific assumption of centralized command generation with identical workload semantics across architectures. Under a truly decentralized architecture, command generation, routing, and volume could all differ. The paper qualifies this ("given the assumed workload semantics") but the qualification is sometimes buried.

## 4. Clarity & Structure
**Rating: 4 (Good)**

The paper is generally well-organized and clearly written. The roadmap at the beginning of Section IV is helpful, and the notation table (Table I) is a good practice. The design equations summary in Section V-C is a valuable reference. The figures are described clearly, though they are referenced as PDF files and cannot be evaluated in this review.

The paper is, however, excessively long and detailed for the depth of its contribution. Many subsections read like an engineering report rather than a journal article. For example, the TDMA synchronization discussion (GPS/GNSS, TCXO drift, sync beacon, Slotted ALOHA fallback) in Section IV-A spans several paragraphs for what amounts to "GPS provides timing; a beacon is the backup." The triple-fault scenario analysis, while thorough, occupies substantial space for an event with probability $1.8 \times 10^{-5}$/yr per cluster.

The notation is mostly consistent but occasionally confusing. $\eta$ is defined as protocol overhead beyond baseline, but $\eta_{\text{total}}$ includes baseline—the reader must track both. The distinction between $\eta_{\text{DES}}$ and $\eta_{\text{analytic}}$ adds another layer. The paper would benefit from a single, clean overhead accounting table early on.

One structural concern: the paper presents four topology models but the centralized and global-state mesh are explicitly described as "reference bounds" rather than realistic alternatives. This means the paper's actual comparative analysis is hierarchical vs. sectorized mesh—but the sectorized mesh provides different functionality (as acknowledged). The paper thus lacks a meaningful peer comparator, which weakens the "topology comparison" framing.

## 5. Ethical Compliance
**Rating: 4 (Good)**

The AI-assistance disclosure in the Acknowledgment section is appreciated and appropriate: "An AI-assisted ideation exercise (Claude 4.6, Gemini 3 Pro, GPT-5.2; see [50]) motivated aspects of the coordinator architecture but is not validated here." This is transparent and appropriately scoped.

The author block uses "Project Dyson Research Team" with a note that individual names will be provided for final publication. This is unusual for IEEE and should be resolved before acceptance—IEEE requires named authors for accountability.

The data availability statement is strong: source code, configuration, and MC datasets are publicly available with a specific tag. This supports reproducibility.

One minor concern: the reference to future model versions (Claude 4.6, GPT-5.2) suggests these may be speculative or the paper was written with assistance from tools not yet publicly available. This should be clarified.

## 6. Scope & Referencing
**Rating: 3 (Adequate)**

The paper is appropriate for IEEE T-AES in topic (space systems coordination, autonomous spacecraft), though the contribution leans more toward systems engineering sizing than the signal processing, estimation, or control theory that dominates the journal.

The reference list is comprehensive (55 references) and covers the relevant domains: constellation operations, swarm robotics, distributed systems theory, queueing theory, and AoI. Key works are cited (Olfati-Saber, Raft, SWIM, Kleinrock, AoI literature).

**Gaps in referencing:**
- No citation of the extensive literature on satellite cluster flight and formation flying coordination (e.g., Scharf et al., "A survey of spacecraft formation flying guidance and control," JGCD 2004; Bandyopadhyay et al., "Review of formation flying and constellation missions using nanosatellites," JSMALL 2016).
- The DTN/BPv7 reference is included but the paper does not engage with how DTN store-and-forward would interact with the hierarchical coordination model—this is a significant omission given the intermittent-link scenario.
- No reference to the IETF/CCSDS work on delay-tolerant link protocols (LTP) that would be relevant to the 1 kbps RF backup scenario.
- The NASA DSA reference [52] is very recent and relevant, but the paper does not discuss how its results compare to or complement the DSA approach.

Several references are non-archival (Amazon Kuiper overview, DARPA program pages, DoD fact sheets). While understandable for operational programs, the paper should note their non-archival status more consistently.

---

## Major Issues

1. **Validation gap is more severe than acknowledged.** The DES and analytical equations share identical assumptions; the $<0.1\%$ agreement is tautological. The most critical results (TDMA superframe feasibility, half-duplex partitioning, 623 ms margin) have *no* simulation validation—they are purely analytical. The paper needs either (a) a TDMA-aware DES mode or (b) explicit acknowledgment that the superframe budget is an unvalidated analytical prediction. Currently, the paper's structure implies broader validation than exists.

2. **The sectorized mesh comparison is structurally unfair.** Comparing overhead of architectures with fundamentally different functional scope (100% cluster awareness vs. 3.2% sector coverage) produces misleading metrics. The "14× bandwidth efficiency per peer" figure conflates coverage scope with efficiency. Either design a functionally equivalent comparator or remove the quantitative efficiency comparison and restrict discussion to qualitative trade-offs.

3. **System availability (99.5%) is inadequately derived.** The jump from per-coordinator 99.99% to system-level 99.5% is not rigorously justified. For a paper presenting "design equations," this key reliability metric needs a closed-form derivation, not a qualitative reference to "cascading effects."

4. **The 1 kbps design point needs stronger operational justification.** The paper acknowledges that 1 kbps applies during optical outages ($<1\%$ of operational time) and that at $\geq$10 kbps "all constraints are non-binding." This means the paper's most interesting results (coordinator bottleneck, TDMA requirement, unicast staggering) apply only to a rare degraded mode. The paper should either (a) more prominently frame this as a safe-mode/degraded-operations analysis, or (b) identify constraints that *are* binding at higher bandwidths (antenna scheduling, visibility, interference—currently listed as future work).

5. **No sensitivity to message size assumptions.** The entire analysis depends on fixed message sizes (256 B status, 512 B command, 64 B heartbeat, 128 B alert). These are stated without justification beyond "consistent with CCSDS SPP." A sensitivity analysis varying message sizes by ±50% would significantly strengthen the results, as real coordination messages may vary substantially depending on state vector complexity, compression, and security overhead (authentication tags, encryption).

## Minor Issues

1. **Eq. (2), M/D/1 waiting time:** The formula $W_q = \rho / (2\mu_s(1-\rho))$ is the Pollaczek-Khinchine result for M/D/1, but the notation is slightly non-standard. Clarify that this is the mean waiting time (excluding service) for the M/D/1 queue specifically.

2. **Table I notation:** $p_{BG}$ and $p_{GB}$ are listed but their subscript convention (from-to) should be explicitly stated. The current listing could be read as $p_{BG}$ = probability of being in state B given state G.

3. **Section III-B.2, coordinator failure transient:** The RF-backup Raft election timing ($51 \times 0.8$ s = 41 s at 1 kbps under Slotted ALOHA) assumes sequential transmission of RequestVote messages. Under Slotted ALOHA with $\gamma = 0.36$, the actual time would depend on collision probability among the 51 responders—this interaction is not modeled.

4. **Table II, collision avoidance rate:** $10^{-4}$/node/s seems high for screening notifications. At $N = 10^5$, this yields 10 alerts/s fleet-wide. Cite a source or provide a derivation.

5. **Section IV-A, "Recommended design point: 30 kbps":** This recommendation appears without formal margin analysis. What confidence level does the 1.25× factor provide? Is this a standard engineering margin or derived from the analysis?

6. **Eq. (6), $\gamma$ derivation:** The 88.0 ms data portion calculation uses 2,112 bits (2,048 payload + 32 preamble + 16 header + 16 CRC), but the text says "data portion" which could be confused with payload only. Clarify.

7. **Section IV-B, AoI cross-check:** The ceiling function in Eq. (7) introduces discretization; the DES value of 441 s vs. analytical 440 s is within one $T_c$ step, which is expected. This should be noted as a discretization artifact rather than presented as independent validation.

8. **Table IV column headers:** "No Loss Drops" and "GE Only Drops" have identical values, which is the paper's point—but the table formatting makes this look like a copy-paste error. Add a footnote or merge the columns with explanation.

9. **Section III-B.3:** The gossip fanout $f = N/\log N$ is described as "aggressive" but this is actually the standard epidemic dissemination rate for single-round convergence. The characterization as "intentional worst-case" is appropriate but the fanout choice should be better motivated.

10. **Acknowledgment section:** "Claude 4.6" and "GPT-5.2" do not correspond to publicly known model versions as of the apparent writing date. Clarify whether these are internal designations or future models.

11. **Throughout:** The paper uses both "kbps" and "bps" without always being explicit about whether these are information rates or channel rates (pre/post FEC). Standardize.

12. **Fig. 8 caption:** States "$10^6$-node curve is an analytical extrapolation"—this should also appear in the main text where the figure is discussed, not just the caption.

---

## Overall Recommendation

**Major Revision**

This paper addresses a real gap in the literature and provides a systematic, well-documented framework for sizing hierarchical coordination architectures at scale. The three-layer feasibility decomposition, the design equations summary, and the open-source tooling are genuine contributions. However, the paper has several significant issues that prevent acceptance in its current form: (1) the validation is essentially self-referential (DES implements the same equations it "validates"), with the most critical TDMA results having no simulation cross-check; (2) the topology comparison is structurally unfair due to mismatched functional scope; (3) key reliability figures (99.5% availability) lack rigorous derivation; and (4) the paper's most interesting results apply only to a rare degraded operating mode (1 kbps RF backup) without adequate framing. The paper is also substantially longer than necessary for its analytical depth. A major revision addressing these issues—particularly adding TDMA-aware simulation, fixing the comparator architecture, and deriving the availability figure—would make this a solid contribution to the field.

---

## Constructive Suggestions

1. **Implement a TDMA-aware DES mode for a single cluster.** Even a simplified slot-level simulation of one cluster ($k_c = 100$) over 1,000 cycles would validate the superframe budget (Table III), half-duplex partitioning, and the 623 ms margin. This is the single highest-impact addition: it would bridge the gap between the message-layer DES and the analytical TDMA results that are the paper's primary engineering contribution.

2. **Restructure the topology comparison around functional equivalence.** Either (a) design a sectorized mesh variant that achieves comparable cluster-level awareness (e.g., by increasing the cap to $k_c$ within a sector and comparing overhead at equal awareness), or (b) reframe the comparison as a Pareto analysis of overhead vs. awareness scope, clearly showing that the hierarchy and mesh occupy different points on this frontier rather than claiming one is "14× more efficient."

3. **Add message-size sensitivity analysis.** Sweep $S_{\text{eph}} \in [128, 512]$ B and $S_{\text{cmd}} \in [256, 1024]$ B to show how the design equations scale. This is trivial analytically (linear scaling) but would demonstrate robustness and provide practitioners with confidence that the results apply to their specific message formats. Include the effect of authentication overhead (e.g., 32-byte HMAC per message).

4. **Derive system availability rigorously.** Model the fleet as $N/k_c$ independent clusters, each with a coordinator whose availability follows the two-state Markov model. Compute fleet-level metrics (fraction of nodes with functioning coordination, expected number of clusters in degraded state) as closed-form expressions. Address the correlation between coordinator failure and optical ISL outage explicitly in the Markov model rather than as a qualitative aside.

5. **Reframe the 1 kbps analysis as degraded-mode sizing and add a 10 kbps primary-mode analysis.** Since the paper acknowledges that all constraints are non-binding at ≥10 kbps, the current framing buries the lead. Present the 10 kbps case first (showing the architecture works easily), then present 1 kbps as the design-driving degraded mode with its specific constraints (TDMA requirement, unicast staggering, tight superframe margin). This reframing would make the paper's practical relevance much clearer and would naturally motivate the question: "What new constraints emerge at 10–100 kbps that the message-layer model doesn't capture?"