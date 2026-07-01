---
paper: "02-swarm-coordination-scaling"
version: "ba"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-27"
recommendation: "Major Revision"
---

# Peer Review: "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms"

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a genuine gap: there is no systematic, byte-level traffic accounting framework for comparing coordination architectures at the $10^3$–$10^5$ node scale. The framing as a "practitioner toolkit" of closed-form design equations is appealing and potentially useful for systems engineers sizing future mega-constellation coordination links. The three key equations (coordinator ingress, AoI P99, GE recovery P95) are individually straightforward but their assembly into a coherent sizing methodology has value.

However, the novelty is limited in several respects. The individual analytical results are standard: M/D/1 queueing, geometric inter-arrival AoI, and two-state Markov chain recovery are textbook material. The paper's contribution is primarily one of *integration and parameterization* rather than new theory. The authors partially acknowledge this ("assembling standard queueing, geometric, and Markov-chain results"), but the abstract and introduction overstate the contribution by using phrases like "derive closed-form design equations" when the derivations are elementary applications of known results. The claim of "no prior work has systematically compared coordination architectures" is difficult to verify and potentially overstated—the DTN and ISL scheduling literatures (e.g., work by Fraire et al. on contact-graph routing, or Radhakrishnan et al. on ISL scheduling) perform related analyses at comparable scales, albeit with different abstractions.

The 1 kbps RF-backup regime is a narrow operating point that limits immediate applicability. While the authors argue generalizability via linear scaling with $C_{\text{node}}$, the most interesting regime (optical ISL at Gbps) would fundamentally change the design trade-offs in ways not captured by simple linear scaling—e.g., the coordinator bottleneck vanishes entirely, as the authors themselves note, which undermines the practical relevance of the coordinator sizing equation.

## 2. Methodological Soundness

**Rating: 3 (Adequate)**

The methodology has a fundamental circularity that the authors partially acknowledge but do not fully resolve. The DES and the closed-form equations operate at the *same* abstraction level with the *same* assumptions. The <0.1% agreement (Table VII) therefore confirms arithmetic consistency, not model validity. The authors state this clearly in Section III-A ("their agreement confirms arithmetic consistency, not physical fidelity"), which is commendable, but this means the paper's empirical contribution is essentially a code verification exercise, not a validation study. The title's "Design Equations" implies engineering utility that has not been demonstrated against any physical system or higher-fidelity simulation.

The Monte Carlo configuration (30 replications) is adequate for mean estimation but the tail-statistic methodology deserves scrutiny. The P99 AoI computation (Table IV footnote) correctly uses per-run aggregation to avoid inflated confidence from pooling correlated samples—this is good practice. However, 30 replications provide limited resolution for P99 estimation; the bootstrap CI of [438, 444] s seems surprisingly tight given only 30 per-run P99 values. The authors should clarify whether this tightness arises from the large within-run sample size ($\sim 3.15 \times 10^6$ samples) dominating inter-run variability, which would be expected for a stationary geometric process.

The GE channel model's per-cycle coherence assumption (Section IV-C) is a significant modeling choice that is well-justified as conservative for recovery time but creates an artificial decoupling between intra-cycle retransmission and channel state. The authors correctly note this is "by model construction," but the practical implication is that the intra-cycle recovery result (27.1%) is an artifact of the coherence assumption rather than a general finding. The sensitivity analysis over $p_{BG}$ (Fig. 5b) partially addresses this, but the lack of any measured S-band ISL channel statistics makes it impossible to assess which region of the parameter space is operationally relevant.

The sectorized mesh model (Section III-B.4) has a significant design issue: the capped-fanout variant achieves only 3.2% sector coverage while the hierarchical architecture achieves 100% cluster awareness. The authors acknowledge this asymmetry but still present overhead comparisons ($1.4\times$–$1.5\times$) that are misleading because the architectures provide fundamentally different levels of situational awareness. The "overhead per unit of awareness" framing is more honest but is introduced late and not quantified rigorously.

## 3. Validity & Logic

**Rating: 3 (Adequate)**

The internal logic is generally sound, and the authors are commendably transparent about limitations. The pipeline decoupling result (Section IV-D, Table VI) is well-demonstrated: under dedicated links, GE losses and queue drops are independent because lost messages never reach the queue. The caveat about TDMA slot-time coupling (Eqs. 7–8) is important and correctly identified—under GE steady-state, intra-cycle retransmission makes the TDMA frame infeasible, which is a genuine design constraint.

However, several logical issues merit attention:

**Baseline asymmetry (Section IV-G).** The centralized baseline models only compute-queue scalability (M/D/c) without communication-layer overhead, while the hierarchical model includes full communication accounting. The authors acknowledge this ("cross-architecture overhead comparison is restricted to hierarchical vs. sectorized mesh"), but the paper's figures (Fig. 8, Fig. 12) and narrative still prominently feature the centralized comparison, which is not apples-to-apples. This creates a misleading visual impression of hierarchical superiority.

**The $\eta \approx 46\%$ headline number.** This stress-case value dominates the abstract and conclusions, yet the decomposition (Fig. 7, Section IV-E) shows commands account for >60% of this overhead and are topology-invariant. The topology-dependent overhead is only ~5%. The paper would be more honest to lead with "5% architecture-specific overhead" rather than "46% total overhead," since the latter conflates workload with architecture. The authors do state this, but the emphasis in the abstract and title-level claims is on the larger number.

**Static topology assumption.** The analytical bound on re-association overhead (<0.5%, Section V-C) is reasonable for byte overhead, but the 1–3 cycle AoI transient during re-association is dismissed too quickly. In a Walker-delta constellation at 550 km, cross-plane encounters occur every ~45–90 minutes, meaning a significant fraction of nodes could be in transient states simultaneously. The claim that "this ~30 s transient is well within tolerance" at P99 AoI = 441 s conflates two different things: the steady-state AoI under exception telemetry and the transient AoI during cluster migration.

**Eq. 6 (AoI P99).** The ceiling function is correct for the geometric distribution, and the DES match (440 vs. 441 s) is expected since both implement the same model. But the practical interpretation—441 s of stale ephemeris corresponding to ~230 m along-track uncertainty—is presented without discussing whether this is acceptable for conjunction screening. The Alfano reference [alfano_conjunction] is cited but not used to establish a threshold.

## 4. Clarity & Structure

**Rating: 4 (Good)**

The paper is well-organized with a clear roadmap (beginning of Section IV) and consistent notation. The design equations summary (Section V-D) is a valuable practitioner reference. Tables are generally well-constructed, particularly Table III (simulation parameters) and Table V (traffic accounting), which provide the level of detail needed for reproducibility.

Several aspects could be improved:

The paper is *very long* for a journal article—the LaTeX source suggests it would exceed 12 IEEE two-column pages. Significant compression is possible: Table I (M/D/c sensitivity) conveys a trivial result ($N_{\max} = c \cdot \mu_s / r$) that doesn't need a table; the sectorized mesh discussion (Section III-B.4) is disproportionately detailed for what is an intermediate comparator; and the duty cycle analysis (Section IV-H.2) is tangential to the main contributions.

The notation is mostly consistent but has some ambiguities. $\eta$ is defined as protocol overhead beyond baseline telemetry, but the text sometimes uses $\eta$ where $\eta_{\text{total}}$ is meant (e.g., the abstract's "5% to 46%" refers to $\eta$, but the safe-mode floor discussion uses $\eta_{\text{total}}$). The distinction between offered and delivered overhead ($\eta$ vs. $\eta_{\text{delivered}}$) is introduced in Section III-E but not consistently maintained.

Figures are referenced but provided as PDF placeholders (e.g., `fig-architecture-diagram.pdf`), so their quality cannot be assessed. The captions are informative. Fig. 10 (latency distribution) includes a $10^6$-node analytical extrapolation that is flagged in the caption—good practice, but this extrapolation should be more prominently caveated or removed, as it extends beyond the validated range.

The abstract is accurate but dense. The phrase "Architecture-specific protocol overhead is ~5%; with commands, total overhead ranges from 5% (nominal) to 46% (stress-case)" is confusing on first read because "5%" appears twice with different meanings.

## 5. Ethical Compliance

**Rating: 4 (Good)**

The AI-assistance disclosure (Acknowledgment section) is transparent: "An AI-assisted ideation exercise (Claude 4.6, Gemini 3 Pro, GPT-5.2) motivated aspects of the coordinator architecture but is not validated here." This is appropriate and follows emerging best practices. The reference to a methodology paper [dyson_multimodel] is a good addition.

The anonymous authorship ("Project Dyson Research Team") with a note about final publication is acceptable for review but must be resolved before publication per IEEE policy. The open-source data availability statement with a specific repository tag is excellent for reproducibility.

One concern: the paper cites model versions (Claude 4.6, GPT-5.2) that do not exist as of my knowledge cutoff, suggesting either future versions or fictional designations. This should be clarified.

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is appropriate for IEEE T-AES in scope, addressing autonomous spacecraft coordination at scale. The reference list (50+ entries) is comprehensive and covers the relevant literatures: constellation management, swarm robotics, distributed systems, queueing theory, and AoI.

However, several important gaps exist:

- **Contact-graph routing and DTN scheduling** for mega-constellations (Fraire et al., 2021; Araniti et al., 2015) are directly relevant but not cited. These works perform link-budget and scheduling analyses at comparable scales.
- **Satellite network simulation** literature (e.g., SNS3 for NS-3, or STK-based analyses) would contextualize the validation gap discussion.
- **Recent AoI work in satellite networks** (e.g., Pan et al., IEEE TWC 2023; Liu et al., IEEE JSAC 2022) applies AoI theory to LEO constellations and should be discussed.
- Several references are non-archival (Amazon Kuiper overview, DARPA program pages, DoD fact sheets). While understandable for program descriptions, these weaken the scholarly foundation. The Starlink FCC filing [1] is supplemented by "Jonathan's Space Report" which is explicitly flagged as non-archival—this is honest but the primary reference should be strengthened.
- The NASA DSA reference [nasa_dsa] is highly relevant but cited only once in passing; a more detailed comparison of the DSA coordination approach with the proposed hierarchy would strengthen the related work.

## Major Issues

1. **No physical-layer validation or higher-fidelity comparison.** The entire paper operates at a single abstraction level (message-layer), and the DES merely verifies the closed-form arithmetic. Without at least one packet-level simulation (even a single-cluster NS-3 run at $k_c = 100$), the "design equations" cannot be claimed to have engineering utility. The authors identify this as future work, but for a journal claiming to provide "design equations," at least a preliminary packet-level comparison is expected. **Recommendation:** Add a single-cluster NS-3 or OMNeT++ validation scenario, or substantially downgrade the claims to "message-layer sizing heuristics."

2. **Misleading baseline comparisons.** The centralized model lacks communication-layer overhead while the hierarchical model includes it. Figures 8 and 12 visually compare these architectures despite the acknowledged asymmetry. The global-state mesh is an intentional worst case that no practitioner would implement. These comparisons inflate the apparent advantage of the hierarchical architecture. **Recommendation:** Either model centralized communication overhead (uplink scheduling, ground contact windows) or restrict all figures and tables to hierarchical vs. sectorized mesh comparisons, relegating the centralized and global-state mesh to brief textual mentions as bounds.

3. **Sectorized mesh comparison is not functionally equivalent.** At cap = 10, the sectorized mesh provides 3.2% sector awareness while hierarchical provides 100% cluster awareness. Comparing overhead ratios ($1.4\times$–$1.5\times$) without normalizing for functional utility is misleading. **Recommendation:** Define a common functional requirement (e.g., "awareness of all neighbors within screening distance $d$") and compare the overhead required to achieve it under both architectures.

4. **The 1 kbps regime limits practical relevance.** The RF-backup scenario (<1% of operational time) is a corner case. The paper's most interesting claim—that coordinator bottleneck vanishes at 10 kbps—undermines the practical significance of the coordinator sizing equation, which is one of the three headline contributions. **Recommendation:** Present results at multiple $C_{\text{node}}$ values (1, 10, 100 kbps) to demonstrate the design equations' utility across the operational envelope, not just the backup regime.

## Minor Issues

1. **Abstract, line 1:** "closed-form design equations" overstates the novelty; these are standard results parameterized for a specific application. Consider "closed-form sizing relationships."

2. **Section I-C:** The notation $\eta_{\text{stress}} \approx 4.6\%$ at 10 kbps appears without derivation; it should be $46\% \times (1/10) = 4.6\%$ but this linear scaling should be stated explicitly.

3. **Eq. 2 (M/D/1 waiting time):** The standard Pollaczek-Khinchine formula for M/D/1 is $W_q = \rho / (2\mu_s(1-\rho))$, which is correct, but the paper should note this is the *mean* waiting time and that the P99 would be substantially higher.

4. **Table II (mesh traffic):** The footnote states "$\approx 51$ MB" but then "$\approx 73$ MB with $\sim 1.4\times$ gossip redundancy." The 1.4× factor should be derived or cited.

5. **Section III-B.2:** "Coordinator rotation: state transfer (10–50 MB) over optical ISL (80–400 ms), excluded from $\eta$." The exclusion is justified but the 10–50 MB range is very wide; the scaling with $k_c$ should be made explicit.

6. **Eq. 5 ($\gamma$ derivation):** The derived $\gamma = 0.949$ vs. assumed $\gamma = 0.85$ is a 12% discrepancy. The additional overheads (FEC ~7%, ranging ~3%, control ~5%) total ~15%, which would give $\gamma \approx 0.949 \times 0.85 = 0.807$, not 0.85. The accounting is inconsistent.

7. **Table VI (joint interaction):** The "GE + Exc." column shows dramatically fewer drops (377 vs. 122,510 at 15 kbps), but this is entirely due to reduced offered load from exception telemetry, not a GE interaction effect. The table caption should clarify this.

8. **Section IV-H.2 (duty cycle):** The power variance CV values (5%–35%) are stated without derivation. The claim "CV ≈ 12% at $k_c = 100$" should show the calculation.

9. **Section V-C (static topology):** "cross-plane relative velocities at orbital-plane intersections reach ~0.1–1.0 km/s"—this range is too broad to be useful. A specific Walker constellation (e.g., 72/36/1 at 550 km) would give a concrete number.

10. **References:** [dyson_multimodel] is a self-citation to a URL with no publication venue or date verification. Several DARPA/DoD references lack persistent identifiers.

11. **Eq. 4 ($M_{\text{total}}$):** This counts only uplink messages; the bidirectional traffic (commands, heartbeats) mentioned in the text is not reflected in the equation.

12. **Section III-E:** "Slotted ALOHA capacity" is referenced without stating the value ($1/(2e) \approx 0.184$ or the throughput maximum $1/e \approx 0.368$). The claim that "stress-case effective utilization exceeds Slotted ALOHA capacity" should specify which metric.

## Overall Recommendation

**Major Revision**

This paper addresses a relevant problem and provides a well-organized framework for message-layer sizing of hierarchical coordination in large space swarms. The design equations, while individually standard, are usefully assembled and parameterized. The transparency about limitations (validation gap, static topology, abstraction scope) is commendable and above average for the field. However, the paper suffers from four significant issues that prevent acceptance in its current form: (1) the absence of any physical-layer or packet-level validation means the "design equations" are unvalidated sizing heuristics; (2) the baseline comparisons are structurally asymmetric, inflating the hierarchical architecture's apparent advantage; (3) the sectorized mesh comparison conflates byte-level overhead with functional utility; and (4) the narrow 1 kbps operating regime limits practical relevance. A major revision addressing these issues—particularly adding at least a single-cluster packet-level simulation and presenting results across multiple bandwidth regimes—would substantially strengthen the contribution.

## Constructive Suggestions

1. **Add a packet-level validation scenario.** Even a single-cluster NS-3 simulation ($k_c = 100$, TDMA PHY, GE channel) would quantify the message-to-packet gap and transform the paper from a code-verification exercise into a validated design tool. This is the single highest-impact improvement.

2. **Present results at 3+ bandwidth regimes** (1, 10, 100 kbps) in a unified table/figure. This would demonstrate the design equations' generality and reveal which results are regime-dependent (coordinator bottleneck) vs. structural (AoI scaling, pipeline decoupling).

3. **Equalize the baseline comparisons.** Either add communication-layer modeling to the centralized architecture (ground contact scheduling, uplink contention) or restrict all quantitative comparisons to hierarchical vs. sectorized mesh. Relegate the centralized and global-state mesh to qualitative bounds discussed in text only.

4. **Define a functional equivalence metric for the sectorized mesh comparison.** For example, "overhead to achieve awareness of all neighbors within conjunction screening distance" would allow a fair comparison. The current byte-level comparison at different awareness levels is not informative for architecture selection.

5. **Tighten the paper by ~25%.** Remove Table I (trivial), compress the sectorized mesh discussion, move the duty cycle analysis to an appendix, and consolidate the workload profiles into the overhead verification subsection. This would bring the paper within typical IEEE T-AES length limits and sharpen the narrative focus on the three headline contributions.