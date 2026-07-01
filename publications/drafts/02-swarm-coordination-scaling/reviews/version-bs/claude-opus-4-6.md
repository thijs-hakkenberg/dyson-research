---
paper: "02-swarm-coordination-scaling"
version: "bs"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-27"
recommendation: "Major Revision"
---

# Peer Review: "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms"

## 1. Significance & Novelty
**Rating: 3 (Adequate)**

The paper addresses a genuine gap at the intersection of mega-constellation operations and autonomous swarm coordination: no prior work provides closed-form parametric sizing equations with byte-level traffic accounting for hierarchical coordination across $10^3$–$10^5$ nodes. The three-layer feasibility framework (byte budget, MAC efficiency, TDMA airtime) is a useful conceptual contribution that practitioners could apply to early-phase system design. The decomposition of overhead into architecture-specific ($\eta_0$) and workload-dependent ($\eta_{\text{cmd}}$) components, with the finding that the latter dominates and is topology-invariant, is a clean and actionable insight.

However, the novelty is tempered by the fact that the core result—$\eta_0 \approx 5\%$—follows almost directly from the message size definitions and the assumed traffic model. The "closed-form equations" are largely dimensional analysis (bytes × rate / bandwidth) rather than deep analytical derivations. The AoI result (Eq. 12) is a standard geometric tail bound; the GE recovery analysis is a straightforward Markov chain. While packaging these together for the space swarm context has value, the individual analytical contributions are modest. The paper would benefit from a clearer articulation of what is *surprising* or *non-obvious* in the results—currently, the central finding that command traffic dominates overhead is somewhat predictable given that commands (512 B) are twice the size of status reports (256 B) and are sent every cycle in the stress case.

The claim of addressing $10^5$ nodes is validated only at the message layer with a cycle-aggregated DES that, by construction, produces $O(1)$ overhead for the hierarchical topology. The scaling "validation" is therefore tautological: the DES implements the same linear accounting as the closed-form equations. The paper acknowledges this (Section V-A), but the abstract and introduction could more clearly distinguish between "we derived equations that predict constant overhead" and "we validated that constant overhead is achievable in practice."

## 2. Methodological Soundness
**Rating: 3 (Adequate)**

The methodology is internally consistent and well-documented. The simulation parameters (Table III) are comprehensive, the Monte Carlo configuration (30 replications, bootstrap CIs) is appropriate, and the code availability enhances reproducibility. The three sanity-check models for coordinator ingress (TDMA, hard-deadline Model A, token-bucket Model B) provide useful cross-validation. The TDMA superframe budget (Table V) is a particularly well-executed piece of engineering analysis.

The fundamental methodological concern is that the DES and the closed-form equations operate at *exactly the same abstraction level*—they are not independent validation. The paper states this clearly (Section V-A: "confirms implementation correctness, not physical validity"), but the $<0.1\%$ agreement is then cited repeatedly as if it constitutes validation. A cycle-aggregated fluid-server DES that counts bytes per cycle will, by construction, agree with a formula that counts the same bytes. The inter-cycle GE recovery analysis (Fig. 5) is the one area where the DES provides genuinely independent information (tail statistics of streak lengths), and this is appropriately highlighted.

The Gilbert-Elliott model's per-cycle coherence assumption (GE state constant within $T_c = 10$ s) is stated as conservative for recovery but is actually a strong structural assumption that eliminates intra-cycle dynamics entirely. The paper argues this is conservative, but it also means the $M_r = 2$ retransmission mechanism is rendered useless by construction during bad states—this is a modeling choice, not a physical finding. The physical mapping (Section IV-C) acknowledges three obstruction mechanisms but does not provide measured GE parameters for any of them; the $p_{BG} = 0.50$, $p_B = 0.90$ defaults appear to be assumed rather than derived from channel measurements.

The static topology assumption is a significant limitation for LEO constellations. The quantitative bound ($f_h = 0.8\%$ of nodes in handoff transient) is helpful but relies on a single re-association rate ($\lambda_h = 1/3600$ s$^{-1}$) without sensitivity analysis. For Walker-Delta constellations with significant cross-plane relative motion, cluster membership could change on timescales comparable to $T_c$, fundamentally altering the traffic model.

## 3. Validity & Logic
**Rating: 3 (Adequate)**

The logical structure is generally sound, and the paper is commendably transparent about its limitations. The three-layer feasibility framework is logically coherent, and the workload profiles (nominal/event/stress) provide a reasonable design envelope. The distinction between broadcast (Type 1) and unicast (Type 2) commands, with the 22-cycle stagger result for unicast, is a useful practical finding.

Several logical concerns merit attention:

First, the comparison framework is asymmetric. The centralized baseline models only compute-queue scalability (M/D/c), not communication overhead; the global-state mesh is an intentional worst case; the sectorized mesh provides different functionality. The paper acknowledges all of this (Table VIII), but the topology comparison (Table VII, Fig. 8) still visually implies a fair comparison. The "14× bandwidth efficiency per unit of awareness" claim (Section IV-G) compares hierarchical monitoring of 100 cluster peers against sectorized monitoring of 10 neighbors—but these serve fundamentally different operational purposes (fleet coordination vs. local collision avoidance), making the ratio somewhat misleading.

Second, the coordinator failure analysis (Section III-B.2) presents a triple-fault probability of $1.8 \times 10^{-5}$/yr per cluster, but the three events (coordinator failure, optical outage, GE bad-state) are explicitly noted as potentially correlated ("power-negative or tumbling"). The independence assumption used to compute the joint probability contradicts the stated correlation concern. The RF-backup recovery time of ~160 s (16 cycles) is significant and deserves more analysis of its operational impact.

Third, the AoI P99 = 440 s result is contextualized against a 24-hour conjunction response window, but this comparison conflates two different operational timelines. The 24-hour window is for ground-based conjunction assessment; autonomous swarm coordination presumably requires much faster response for close-approach scenarios. The paper notes that "final maneuver decisions require AoI < 10 s via optical ISL," but this means the RF-backup channel (the design-driving case) cannot support the most critical operational scenario.

## 4. Clarity & Structure
**Rating: 4 (Good)**

The paper is well-organized with a clear roadmap (beginning of Section IV) and consistent notation (Table I). The three-layer feasibility framework provides an effective organizing principle. Tables are generally well-constructed, with Table V (TDMA superframe budget) being particularly informative. The explicit labeling of reference bounds vs. architecture under study (Table VII) is good practice.

The writing is dense but precise. The extensive use of inline qualifications ("under the message-layer model with dedicated scheduled access," "given the assumed workload semantics") demonstrates intellectual honesty but occasionally impedes readability. Some passages read more like internal design documentation than a journal article—for example, the detailed RF-backup handoff calculation in Section III-B.2 ($51 \times 0.8 / 0.36$ s $\approx 113$ s) could be moved to an appendix.

The abstract is accurate but extremely dense; it packs too many specific numbers (5%, 6%, 46%, 22-cycle, 24 kbps, 623 ms, 440 s, 4 cycles, 10 kbps, 0.1%) into a single paragraph, making it difficult to extract the key message on first reading. The notation table (Table I) is helpful but incomplete—$\alpha_{\text{RX}}$, $\beta$, $f_c$, $B_{\text{status}}$, and several other symbols used in the text are not defined there.

Figures are referenced but not provided (as expected for a LaTeX source review). The captions are descriptive and include appropriate caveats (e.g., Fig. 7 noting the $10^6$-node curve is an extrapolation). However, the paper includes 13 figures, which is excessive for a journal article of this scope; several could be consolidated or moved to supplementary material.

## 5. Ethical Compliance
**Rating: 4 (Good)**

The paper includes an explicit acknowledgment of AI-assisted ideation (Claude 4.6, Gemini 3 Pro, GPT-5.2) with a citation to a methodology paper and a clear statement that the AI contributions are "not validated here." This is transparent and appropriate. The anonymous authorship ("Project Dyson Research Team") with a note about IEEE policy compliance is acceptable for review but will need resolution for publication.

The open-source code availability (GitHub with tagged release) and detailed parameter tables support reproducibility. The data availability statement is complete. No conflicts of interest are apparent, though the "Project Dyson" affiliation is opaque—it is unclear whether this is an academic institution, industry group, or independent research organization, which could be relevant for assessing potential biases.

One minor concern: the AI tool versions cited (Claude 4.6, GPT-5.2) do not correspond to any publicly known releases as of the review date, suggesting either future/hypothetical versions or internal designations. This should be clarified.

## 6. Scope & Referencing
**Rating: 3 (Adequate)**

The paper is appropriate for IEEE TAES in its focus on autonomous spacecraft coordination, though it sits at the boundary between systems engineering and communications engineering. The reference list (50 items) is comprehensive and spans the relevant domains: constellation operations, swarm robotics, distributed systems, queueing theory, AoI, and space standards.

Several important gaps exist in the referencing. The paper does not cite recent work on distributed space systems coordination by Radhakrishnan et al. (2016, *IEEE Systems Journal*) on inter-satellite link design for small satellite constellations, or the substantial body of work on satellite cluster flight formation communication architectures. The LEACH citation [heinzelman_leach] is appropriate but the paper should also reference more recent cluster-head rotation protocols (e.g., HEED, TEEN) that address similar energy-balancing concerns. The GE channel model for satellite links has been characterized empirically by Lutz et al. and others; citing measured parameters would strengthen the channel model justification.

Several references are non-archival (Amazon Kuiper overview, DARPA program pages, DoD fact sheets, NRL magazine article). While these are appropriately flagged, the paper relies on them for establishing the operational context. The Castet and Saleh [castet_smallsat_reliability] reference for the 2%/yr failure rate is from 2009 and may not reflect current small-satellite reliability; more recent data from Jacklin (2019) or Langer and Bouwmeester (2016) would be more appropriate.

---

## Major Issues

1. **Tautological validation.** The $<0.1\%$ DES-analytic agreement is presented as a key result but is architecturally guaranteed by the shared abstraction level. The paper needs either (a) a genuinely independent validation (packet-level simulation, hardware-in-the-loop, or comparison with operational constellation data) or (b) a much more prominent and explicit framing that this is a *consistency check*, not validation. Currently, the abstract says "confirms implementation consistency to $<0.1\%$" which is accurate, but the repeated citation of this number throughout the paper inflates its significance. **Recommendation:** Restructure the contribution claims to center on the design equations themselves and the GE recovery analysis (which does provide independent DES insight), rather than on DES-analytic agreement.

2. **Command traffic topology-invariance undermines the architecture comparison.** The paper's central finding is that $\eta_{\text{cmd}}$ dominates and is topology-invariant. This means the hierarchical architecture's advantage over alternatives is confined to $\eta_0 \approx 5\%$—a modest saving that could easily be consumed by unmodeled overheads (cluster re-association, distributed TDMA coordination, priority queueing). The paper should more directly confront the implication: if commands dominate, the choice of coordination topology matters relatively little for bandwidth sizing, and the real differentiator is fault tolerance and functional capability—which are not quantitatively compared at the same level of rigor. **Recommendation:** Either strengthen the fault-tolerance comparison with quantitative availability analysis (beyond the illustrative two-state Markov) or reframe the contribution as "the topology choice is bandwidth-neutral; here are the equations that apply regardless."

3. **No physical-layer grounding for the 1 kbps design point.** The entire analysis is driven by a 1 kbps per-node budget that is described as an "S-band RF backup" applying during optical outages ($<1\%$ of operational time). Yet the paper derives all its design equations, feasibility limits, and stress-case results at this rate. At $\geq 10$ kbps (the nominal operating point), all constraints are "non-binding" (Table II). This means the paper's most detailed and interesting results (TDMA superframe, unicast stagger, coordinator bottleneck) apply only to a degraded-mode edge case. **Recommendation:** Either provide a physical-layer justification for why 1 kbps is the appropriate design point (link budget, regulatory constraints, hardware limitations) or restructure the paper to present the $\geq 10$ kbps regime as the primary result with the 1 kbps case as a degraded-mode appendix.

4. **Coordinator failure recovery is underanalyzed for the claimed scale.** At $N = 10^5$ with $k_c = 100$, there are 1,000 cluster coordinators. The RF-backup recovery time of ~160 s (16 cycles) means that at any given time, with 2%/yr node failure rate, approximately $0.02 \times 1000 \times 160 / (365.25 \times 86400) \approx 10^{-4}$ coordinators are in recovery—seemingly negligible. But the paper does not analyze cascading failures (regional coordinator failure during cluster coordinator recovery), correlated failures (solar particle events affecting multiple coordinators simultaneously), or the interaction between coordinator failure and GE bad-state (the "triple fault" is dismissed with a probability estimate that assumes independence despite acknowledging correlation). **Recommendation:** Provide a multi-state availability model that accounts for correlated failures and cascading effects, or clearly scope the reliability claims to independent single-fault scenarios.

## Minor Issues

1. **Table I (Notation):** Missing definitions for $\alpha_{\text{RX}}$, $\beta$, $f_c$, $B_{\text{status}}$, $L_{\text{cmd}}$, $T_{\text{cmd}}$, $T_{\text{hb}}$, $T_{\text{sync}}$, $\pi_G$, $\pi_B$, $s_{\text{proc}}$, and several other symbols used in the body.

2. **Eq. (4), mesh complexity:** The stated $O(N^2)$ follows from $f = N/\log N$, but the text says this is chosen "for single-cycle convergence." Standard gossip with constant fanout achieves $O(\log N)$ convergence rounds at $O(N \log N)$ total messages. The choice of $f = N/\log N$ seems designed to make the mesh look maximally bad. This should be acknowledged more explicitly as a worst-case construction.

3. **Section III-B.2, Raft election over RF:** The calculation "$51 \times 0.8 / 0.36$ s $\approx 113$ s" is unclear. Presumably 0.8 s is the per-message transmission time (100 B × 8 / 1000 bps = 0.8 s) and 0.36 is Slotted ALOHA throughput, but this should be spelled out. Also, Raft requires a *majority* quorum, not all $k_c/2 + 1$ responses to arrive sequentially—some parallelism is possible.

4. **Table IV (AoI results):** The column header "$\eta$ (%)" in an AoI table is confusing; it's unclear why overhead is reported alongside AoI. The connection should be made explicit (exception telemetry reduces both AoI freshness and overhead).

5. **Section IV-A, "Model A" Monte Carlo:** The $10^5$ random arrival patterns used to estimate $C_A \approx 50$ kbps should be described more precisely—is this an independent MC, or part of the main DES? The confidence interval should be reported.

6. **Eq. (6), sector overhead:** The equation gives bytes, not a dimensionless overhead ratio. The conversion to $\eta_{\text{sector}}$ (Table III footnote) should be presented as a formal equation.

7. **Section III-D, "vectorized (~7 s at $N = 10^5$)":** This runtime claim should specify the hardware (CPU model, RAM) for reproducibility.

8. **Table VI (Joint Interaction):** The "GE Only" column is identical to "No Loss" because of the fluid-server abstraction. This is explained in the text but the table presentation is misleading—consider adding a footnote directly in the table or removing the redundant column.

9. **References:** [starlink_ops] cites both an FCC filing and a non-archival website in a single entry; these should be separated. [nrl_swarm] is a magazine article cited for a factual claim about demonstration scale; a peer-reviewed source would be preferable.

10. **Abstract:** "Project Dyson Research Team" with a footnote about individual author names is unusual. The acknowledgment section references AI tools with version numbers (Claude 4.6, GPT-5.2) that do not correspond to known releases—verify accuracy.

11. **Section IV-G, "99.5%" availability for hierarchical:** This number appears in Table VII but the derivation (Section IV-H.2) describes a two-state Markov model yielding $>99.99\%$ per-coordinator, then states "99.5% conservatively accounts for cascading effects." The gap between $99.99\%$ and $99.5\%$ is not analytically justified.

12. **Eq. (8), unicast stagger:** The denominator uses $T_c \cdot (1 - \alpha_{\text{RX}})$ but $\alpha_{\text{RX}}$ is not formally defined until Eq. (9). Reorder or add a forward reference.

## Overall Recommendation

**Major Revision**

This paper addresses a relevant problem and provides a well-structured engineering analysis of hierarchical coordination overhead for large space swarms. The three-layer feasibility framework, TDMA superframe budget, and GE recovery design curves are useful contributions. However, the paper suffers from three fundamental issues that require substantial revision: (1) the validation is tautological at the message layer, inflating the significance of the DES-analytic agreement; (2) the central finding that command traffic dominates and is topology-invariant undermines the motivation for detailed topology comparison without being adequately confronted; and (3) the entire detailed analysis applies to a degraded-mode edge case (1 kbps RF backup) while the nominal operating regime ($\geq 10$ kbps) trivially satisfies all constraints. A major revision should reframe the contributions around the design equations as engineering tools (rather than validated predictions), provide physical-layer grounding for the design point, and strengthen either the fault-tolerance analysis or the acknowledgment that topology choice is primarily a reliability decision rather than a bandwidth decision.

## Constructive Suggestions

1. **Add a single-cluster NS-3 simulation.** The paper itself identifies this as the "priority next step" (Section V-A) and provides the TDMA specification (Table V). Even a simplified NS-3 model with 100 nodes, half-duplex TDMA, and GE fading would transform the validation story from tautological to meaningful. This would likely reveal whether the 623 ms margin survives real MAC-layer dynamics and provide the first physical-layer data point.

2. **Restructure around the design equation toolkit.** Rather than framing this as a topology comparison paper (which is weakened by the asymmetric modeling), frame it as providing a *parametric sizing toolkit* for any hierarchical coordination architecture. Present the equations (Section V-C) as the primary contribution, with the DES as a consistency check and the topology comparison as context. This better matches the actual strength of the work.

3. **Provide a link budget for the 1 kbps design point.** A one-paragraph link budget (transmit power, antenna gain, path loss at 500 km, noise figure, required $E_b/N_0$ for the assumed modulation) would ground the 1 kbps assumption in physics and allow readers to assess whether 24 kbps coordinator PHY rate is achievable with the stated 5–15 W power budget. This would also clarify whether the "S-band RF backup" framing is realistic.

4. **Quantify the fault-tolerance advantage analytically.** The paper claims hierarchical coordination provides "graceful degradation" but supports this only with an illustrative two-state Markov model. A rigorous multi-cluster availability analysis—accounting for coordinator failure rate, election time, and the probability that $\geq k$ clusters are simultaneously without a coordinator—would provide the quantitative fault-tolerance comparison that the bandwidth analysis cannot.

5. **Consolidate figures and tighten the presentation.** The paper has 13 figures and 12 tables for what is fundamentally a parametric sizing study. Figures 7 (latency distribution), 9 (failure resilience), and 10 (topology summary) could be consolidated into a single multi-panel figure. Tables IV and VI could be merged. This would free space for the additional analysis suggested above without exceeding page limits.