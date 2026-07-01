---
paper: "02-swarm-coordination-scaling"
version: "t"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-24"
recommendation: "Major Revision"
---

# Peer Review: "Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study"

## 1. Significance & Novelty
**Rating: 3 (Adequate)**

The paper addresses a genuinely important problem: how to coordinate autonomous spacecraft swarms at scales of 10³–10⁵ nodes, a regime that is underexplored in the literature. The motivation is timely given Starlink's expansion plans and emerging mega-constellation concepts. The introduction of Age-of-Information (AoI) as a coordination quality metric for swarm architectures is a welcome contribution, and the coordinator bandwidth stress-testing provides useful engineering design parameters.

However, the novelty claim is significantly undermined by the paper's own analysis. The authors repeatedly and commendably acknowledge that the O(1) overhead scaling of the hierarchical architecture is "a direct mathematical consequence of the hierarchical message structure—not a surprising emergent property" (Section IV-D). The DES then confirms this analytical prediction to within 0.05%, which the authors correctly characterize as "implementation correctness [validation] rather than constituting an independent finding" (Section IV-D.2). This raises a fundamental question: if the central scaling result is analytically trivial and the DES merely confirms the closed-form accounting, what is the simulation actually discovering? The three claimed DES contributions—protocol coefficient quantification, queue stability confirmation, and analytical cross-check—are all relatively modest given the near-deterministic nature of the message model (SD < 0.001%).

The comparison architecture selection also limits novelty. The centralized single-server and global-state mesh baselines are acknowledged as intentional bounds rather than realistic competitors. While the sectorized mesh provides a more meaningful comparator, the 1.4–1.5× overhead ratio is specific to the capped-fanout parameterization and may not generalize. The paper would benefit from comparison against at least one architecture drawn from the operational literature (e.g., a two-tier ground-relay architecture resembling actual Starlink operations, or a DTN-based store-and-forward approach).

## 2. Methodological Soundness
**Rating: 3 (Adequate)**

The cycle-aggregated DES framework is clearly described and the traffic accounting is meticulous. The explicit byte-level accounting (Table V), consistent overhead definitions, and analytical cross-check (Eq. 8, Section IV-D.2) demonstrate careful implementation. The 30 Monte Carlo replications per configuration with bootstrap confidence intervals follow sound statistical practice, and the authors are commendably transparent about the near-deterministic nature of the model making the MC framework primarily a code-correctness check.

However, several methodological concerns are significant:

**The stress-case workload assumption is problematic.** The dominant overhead contributor is the assumption that each coordinator sends one 512-byte command to *every* cluster member *every* coordination cycle (Section IV-D.2: "each cluster coordinator sends one 512-byte command to each of its k_c − 1 members per cycle"). The authors acknowledge this is a "conservative stress-case assumption" and that "many coordination regimes would issue per-cluster commands or event-driven commands at lower rates, reducing the dominant term in η." Since this single assumption accounts for ~40.6% of the 46% overhead (507 of 575.6 bytes/node in the analytical cross-check), the entire quantitative result hinges on a workload model that the authors themselves describe as unrealistic. The paper would be substantially stronger if it presented results under multiple workload models (stress-case, nominal, and light) rather than anchoring on the stress case.

**The Bernoulli link model is overly simplistic.** LEO inter-satellite links experience deterministic periodic outages due to Earth occlusion, not i.i.d. message-level losses. The authors acknowledge this (Section V-E) but the gap between the model and reality is large enough to question the quantitative link availability results. Correlated outages could simultaneously affect multiple members of a cluster, producing burst losses that the Bernoulli model cannot capture.

**The collision avoidance event rate parameterization requires more justification.** The 10⁻⁴/node/s rate is described as including all screening events (not just maneuver-triggering conjunctions), but the 1,000:1 screening-to-maneuver ratio is stated without citation. Given that collision alerts contribute minimally to overhead (~0.1 bps/node), this is not a critical flaw, but the sensitivity analysis (varying from 10⁻⁵ to 10⁻³) should be presented in tabular form rather than summarized in text.

**The exception-based telemetry model treats p_exc as a free parameter** rather than deriving it from orbital dynamics. While the authors acknowledge this limitation, it means the AoI results (a claimed primary contribution) are parameterized over an uncalibrated axis. Without knowing what p_exc values are physically realistic for different orbital regimes, the AoI trade-off curves cannot be applied to engineering decisions.

## 3. Validity & Logic
**Rating: 3 (Adequate)**

The logical structure of the paper is generally sound, and the authors demonstrate unusual intellectual honesty in acknowledging the limitations of their approach. The repeated caveats about the single-server centralized baseline, the circularity of confirming an analytical result with a near-deterministic simulation, and the message-layer abstraction limitations are all appropriate and well-articulated.

Several logical issues deserve attention:

**The claim of "first coordination quality metric for hierarchical swarm coordination" (Contributions, bullet 1) overstates the contribution.** AoI is a well-established metric in the networked control systems literature (Kaul et al., 2012; Sun et al., 2019—neither cited). The contribution is applying AoI to this specific context, not introducing it as a concept. Moreover, the AoI analysis is straightforward: under geometric inter-report intervals, the P99 AoI follows directly from the geometric distribution's quantile function. The DES confirmation adds little beyond what a back-of-envelope calculation provides.

**The sectorized mesh comparison has a subtle fairness issue.** The capped-fanout sectorized mesh (≤10 heartbeat neighbors) is compared against the hierarchical architecture, but the sectorized mesh includes peer-to-peer heartbeats that the hierarchical architecture does not. This is presented as the "cost of maintaining peer-to-peer heartbeats," but it could equally be framed as the hierarchical architecture's *lack* of peer-to-peer awareness—a coordination quality deficit that the AoI metric does not capture. The paper should discuss whether the sectorized mesh's higher overhead buys better local collision detection capability.

**Table III (Coordinator Duty Cycle Trade-offs) presents results without adequate explanation of the underlying model.** How is "handoff success" computed? The text mentions a "reliability model" but does not specify it. The power variance values appear to be analytically derived rather than DES-measured, but this is not stated. The system availability column shows a non-monotonic relationship with duty cycle that is not explained (why does 1h achieve 99.9% but 7d only 98.0%?—presumably longer exposure to coordinator failure, but this should be explicit).

**The extrapolation to 10⁶ nodes (Fig. 2) is insufficiently caveated in the figure itself.** While the caption notes it is analytical extrapolation, readers scanning figures may miss this. The figure should use a clearly different visual treatment (e.g., shaded uncertainty band) for the extrapolated regime.

## 4. Clarity & Structure
**Rating: 4 (Good)**

The paper is well-organized and generally well-written, with a logical flow from problem statement through methodology to results and discussion. The extensive use of tables for parameter documentation (Tables I–VII) supports reproducibility. The traffic accounting framework (Table V) is particularly well-constructed and provides a clear basis for understanding the overhead composition.

Several structural issues could be improved:

The paper is excessively long for its content. At approximately 12,000 words of body text plus extensive tables and figures, it significantly exceeds typical IEEE T-AES length guidelines. Much of the length comes from repeated caveats and qualifications that, while individually appropriate, collectively create redundancy. For example, the single-server centralized baseline is qualified as a worst-case bound in at least six separate locations (Section I-C, Section III-B.1, Table II, Fig. 1 caption, Section IV-A text, and Section V-E). These could be consolidated into a single prominent caveat with forward references.

The abstract is dense but accurate, effectively summarizing the key quantitative results. However, it front-loads the hierarchical overhead result (η ≈ 46%) before establishing context, which may confuse readers unfamiliar with the metric definition.

Table IV (Hierarchical Protocol Overhead and Latency vs. Cluster Size) reveals that overhead varies by only ±0.1% across all cluster sizes—a result that undermines the motivation for the cluster-size parameter study. The authors acknowledge this but still devote substantial space to the analysis. The paper would benefit from presenting this as a negative result more concisely and redirecting space to more informative analyses.

The figures are referenced but provided as placeholder filenames (fig-architecture-diagram.pdf, etc.), making it impossible to evaluate their quality. The captions are detailed and informative, which partially compensates.

## 5. Ethical Compliance
**Rating: 4 (Good)**

The paper includes an appropriate acknowledgment of AI-assisted ideation (Claude 4.6, Gemini 3 Pro, GPT-5.2) in the Acknowledgment section, with a clear statement that the AI-generated concepts "are not validated in the current study." This is transparent and appropriate. The reference to a companion methodology paper [47] provides additional context.

The data availability statement commits to open-source release of simulation code and datasets, which is commendable. The commit hash placeholder ([PENDING]) should be resolved before publication.

The author attribution uses a team name ("Project Dyson Research Team") with a footnote promising individual names for final publication. This is unusual but acceptable if resolved. The potential conflict of interest—that the authors are affiliated with the project whose architecture they are evaluating—should be explicitly addressed. While the paper is reasonably balanced in its treatment of limitations, the framing naturally favors the hierarchical architecture (it is the "architecture under study" while alternatives are "reference bounds" or "comparators").

One minor concern: the paper references future model versions (Claude 4.6, GPT-5.2) that do not exist as of the review date, suggesting either forward-looking speculation or a different timeline. This should be clarified.

## 6. Scope & Referencing
**Rating: 3 (Adequate)**

The paper is appropriate for IEEE T-AES in topic, though the contribution level may be marginal for this venue given the methodological concerns noted above. The related work section (Section II) provides reasonable coverage of constellation coordination, swarm robotics, and military programs.

Several referencing gaps are notable:

- The Age-of-Information literature is not cited despite AoI being a claimed primary contribution. Key references include Kaul et al. (2012, "Real-time status: How often should one update?"), Sun et al. (2019, "Age of Information: A New Concept, Metric, and Tool"), and Yates et al. (2021, "Age of Information: An Introduction and Survey"). This is a significant omission.

- The paper does not cite recent work on distributed satellite autonomy, including NASA's Starling mission (2023) which demonstrated autonomous swarm coordination in LEO, or ESA's ADRIOS/ClearSpace-1 coordination architecture.

- Several references are non-archival (SpaceX website, Amazon website, DARPA program pages, DoD fact sheets). While some non-archival sources are unavoidable for operational systems, the paper relies on approximately 8 non-archival sources out of 48 total—a high fraction for a journal paper.

- The queueing theory treatment cites only Kleinrock (1975). More recent references on finite-buffer queueing, particularly in the context of satellite networks, would strengthen the methodological grounding.

- Mean-field game theory references (Lasry & Lions, 2007; Huang et al., 2006) are cited in the related work but never connected to the methodology. If MFG is not used, it should be discussed as a potential alternative approach rather than merely listed.

---

## Major Issues

1. **Near-tautological central result.** The paper's primary finding—that hierarchical overhead scales as O(1)—is analytically guaranteed by the message model and confirmed by a near-deterministic simulation to within 0.05%. The DES adds minimal information beyond implementation validation. The paper needs to either (a) introduce physical-layer effects that could break the O(1) scaling and show whether they do, or (b) reframe the contribution away from the scaling result and toward the engineering design parameters (AoI trade-offs, coordinator bandwidth bounds, retransmission-exception interaction).

2. **Workload model dominance.** The 512-byte per-node per-cycle command assumption drives 88% of the protocol overhead (507/575.6 bytes). This single assumption determines the quantitative result, yet it is acknowledged as a stress-case upper bound. Results under realistic workload models (per-cluster commands, event-driven commands) must be presented to establish the practical range of η.

3. **Missing AoI literature.** The claim of introducing a "first coordination quality metric" cannot stand without engaging the extensive AoI literature. The contribution should be reframed as applying AoI to hierarchical swarm coordination, with proper citation of foundational AoI work.

4. **Unfair sectorized mesh comparison.** The sectorized mesh includes peer-to-peer heartbeats that provide local collision detection capability not available in the hierarchical architecture. The comparison should account for this coordination quality difference, not just bandwidth overhead.

5. **Bernoulli link model inadequacy.** For a paper targeting IEEE T-AES, the link availability model should at minimum include deterministic periodic outages (Earth occlusion) rather than only i.i.d. Bernoulli losses. The authors identify this as future work, but it is fundamental enough to warrant inclusion.

## Minor Issues

1. **Section III-B.1, Eq. 2:** The M/D/1 waiting time formula is stated without the standard assumption that service times are deterministic. Clarify that D refers to deterministic service.

2. **Table I (Simulation Parameters):** The collision avoidance rate footnote (a) is helpful but should also note the sensitivity analysis results in tabular form rather than only in text (Section III-F, final paragraph).

3. **Section III-E:** "Transport-layer overhead (headers, retransmissions) is not included; this understates true overhead by an estimated 10–20%." This 10–20% estimate should be justified or cited.

4. **Table IV:** The latency values show discrete jumps (508→340 ms between k_c=75 and k_c=100) that suggest quantization effects in the simulation. This should be explained.

5. **Section IV-C:** "The inverse relationship between duty cycle duration and handoff success rate" — this is actually a *direct* relationship (longer duty cycle → higher handoff success), not inverse. The inverse relationship is between duty cycle duration and handoff *frequency*.

6. **Eq. 8 (analytical cross-check):** The denominator should be explicitly derived: N × 1000 bps × 10 s / 8 = 1250 bytes/node/cycle. This is correct but would benefit from a one-line derivation.

7. **Section V-B:** The comparison with terrestrial systems (cellular, BGP, ATC) is superficial and could be shortened or removed without loss.

8. **References:** [1], [3], [4] are non-archival web pages. Consider whether archival alternatives exist (e.g., FCC filings for constellation sizes).

9. **Abstract:** "MAC-adjusted η_eff ≈ 51–66% for γ ∈ [0.7, 0.9]" — the abstract should briefly define γ for readers unfamiliar with the notation.

10. **Throughout:** The paper uses both "favorable" and "optimal" to describe k_c = 100–200. These are different claims; "favorable under the assumed parameters" is more appropriate and should be used consistently.

## Overall Recommendation

**Major Revision**

This paper addresses a relevant problem and demonstrates careful simulation engineering with commendable transparency about limitations. However, the central scaling result is analytically trivial and the DES confirmation adds limited insight beyond implementation validation. The quantitative results are dominated by a single workload assumption (512-byte per-node commands) that the authors acknowledge is a stress-case upper bound. The claimed novelty of introducing AoI as a coordination quality metric is undermined by failure to engage the extensive existing AoI literature. The comparison against the sectorized mesh, while a welcome addition, does not account for the coordination quality difference between architectures. A major revision should: (1) present results under multiple workload models to establish the practical range of overhead; (2) introduce at least minimal physical-layer effects (deterministic occlusion outages, TDMA slot modeling) to test whether the O(1) scaling survives beyond the message-passing abstraction; (3) properly cite and position relative to the AoI literature; and (4) address the coordination quality fairness issue in the sectorized mesh comparison. The engineering contributions (coordinator bandwidth bounds, retransmission-exception interaction, AoI trade-off curves) are the paper's strongest elements and should be elevated as the primary framing.

## Constructive Suggestions

1. **Reframe the contribution around engineering design parameters, not scaling.** The AoI trade-off curves, coordinator bandwidth thresholds, and retransmission-exception interaction are genuinely useful engineering results. Make these the headline contributions and demote the O(1) scaling confirmation to a validation exercise. This reframing would also reduce the need for repeated caveats about the analytical triviality of the scaling result.

2. **Present a workload sensitivity matrix.** Define three workload profiles (stress-case: per-node commands; nominal: per-cluster commands with 10% per-node exceptions; light: event-driven only) and report η for each across the fleet size range. This would transform the single-point result (η ≈ 46%) into a practical design envelope (η ∈ [5%, 46%]) with clear guidance on which workload assumptions drive which overhead levels.

3. **Implement a minimal TDMA model within the DES.** Rather than treating TDMA analytically (Section IV-I), implement k_c time slots with configurable guard intervals within each T_c. This would: (a) validate the analytical TDMA capacity predictions; (b) test whether slot synchronization errors introduce scale-dependent effects; and (c) directly produce the γ parameter rather than treating it as an external assumption. This is identified as future work but is tractable and would substantially strengthen the paper.

4. **Couple AoI to a simplified conjunction detection model.** Even a simple model—e.g., probability of detecting a conjunction within a decision window as a function of AoI and relative velocity—would transform the AoI results from abstract staleness metrics into actionable safety parameters. This would also address the coordination quality gap in the sectorized mesh comparison (where peer heartbeats provide local detection capability that the hierarchical architecture lacks).

5. **Reduce paper length by 25–30%.** Consolidate the repeated baseline caveats into a single prominent discussion (perhaps a boxed callout). Shorten Section V-B (terrestrial comparison). Move the detailed mesh traffic accounting (Table II) to an appendix. Present the cluster-size parameter study more concisely given the ±0.1% overhead invariance result. This would bring the paper within typical T-AES length guidelines while improving readability.