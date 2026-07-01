---
paper: "02-swarm-coordination-scaling"
version: "n"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-24"
recommendation: "Major Revision"
---



# Peer Review: "Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study"

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a genuine gap in the literature: the systematic quantitative comparison of coordination architectures for autonomous space swarms in the $10^3$–$10^5$ node regime. The authors correctly identify that swarm robotics literature rarely exceeds hundreds of agents and constellation management literature has not published scalability analyses beyond ~15,000 nodes. This intermediate regime is indeed underexplored and practically relevant given Starlink's planned expansion and emerging mega-constellation concepts.

However, the novelty of the core finding is limited. The authors themselves acknowledge repeatedly (Section IV-D, and throughout) that the $O(1)$ overhead scaling of the hierarchical architecture is "a direct mathematical consequence of the hierarchical message structure—not a surprising emergent property." The DES essentially confirms an analytically predictable result with near-zero variance (SD < 0.001%). While quantifying the protocol coefficient at $\eta = 20.66\%$ has some engineering value, the intellectual contribution is modest—it amounts to computing a ratio of known message sizes and rates. The paper would be substantially more novel if it simulated the sectorized mesh (identified as future work in Section V-C) or incorporated physical-layer effects that could genuinely perturb the analytical prediction.

The exception-based telemetry validation and coordinator bandwidth stress test (Sections IV-E and IV-G) provide more interesting engineering contributions, as they address practical design constraints. The retransmission analysis (Section IV-F) is straightforward but useful. Overall, the paper reads more as a thorough parametric engineering study than a research contribution that advances fundamental understanding of distributed coordination.

## 2. Methodological Soundness

**Rating: 2 (Needs Improvement)**

The methodological framework has several significant concerns that undermine confidence in the results' applicability.

**Circularity of the central claim.** The paper's headline result—constant overhead at 20.66%—is analytically guaranteed by the message model (Eq. 5, fixed message sizes, fixed reporting rate, fixed hierarchy). The DES adds value only if it can detect deviations from the analytical prediction, but the authors explicitly abstract away the phenomena most likely to cause such deviations (MAC contention, correlated failures, priority queueing—Table III). The authors acknowledge this circularity in Section V-E ("the DES cannot detect the scale-dependent second-order effects most likely to perturb the predicted $O(1)$ overhead"), which is commendable, but it raises the question of what the DES actually validates beyond code correctness. The claim of "confirming queue stability" is weak when coordinator utilization is $\rho_c = 0.05$—far from any instability regime.

**Reference baselines are straw men despite disclaimers.** While the authors provide extensive caveats (Section I-C, Table I footnotes, Section V-E), the paper's structure still invites comparison between the hierarchical architecture and these intentionally weak baselines. The single-server centralized model ($c=1$) is unrealistic for any modern ground system, and the global-state mesh requiring $O(N^2)$ communication is an extreme worst case. The absence of a simulated sectorized mesh—which the authors themselves describe as "a priority for future work" and which "closely resembles the hierarchical architecture"—is a critical gap. Without this comparator, the paper cannot substantiate claims about the hierarchical architecture's advantages over practical decentralized alternatives.

**Monte Carlo framework is largely ceremonial.** With SD < 0.001% across 30 replications, the stochastic component of the simulation is negligible for the primary metric. The authors acknowledge this ("the MC framework serves primarily to confirm this low-variance property"), but 30 replications of a near-deterministic model do not constitute meaningful uncertainty quantification. The dominant uncertainties—model-form errors from abstracted physical-layer effects—are not quantified. A parametric sensitivity analysis varying message sizes, reporting rates, and service rates (mentioned as "deferred to future work" in the Conclusion) would have been far more informative than 30 replications of the same configuration.

**Wall-clock times raise fidelity questions.** The simulation runs in 0.2–7 seconds for $10^3$–$10^5$ nodes over a simulated year. While event-driven simulation can be efficient, this speed suggests very few events per node per year are actually processed. At $r = 0.1$ msg/s, each node generates ~3.15 million messages per year; for $N = 10^5$, that is $3.15 \times 10^{11}$ messages. Processing this in 7 seconds implies ~$4.5 \times 10^{10}$ events/second, which is implausible on commodity hardware. The authors should clarify whether the simulation actually processes each individual message event or uses batch/analytical shortcuts that would further reduce the DES to an analytical calculator.

## 3. Validity & Logic

**Rating: 3 (Adequate)**

The conclusions are internally consistent with the model assumptions, and the authors are generally careful to qualify their claims. The paper's strongest aspect is its intellectual honesty about limitations—the circularity caveat in Section V-E, the baseline interpretation note in Section I-C, and the explicit enumeration of abstracted phenomena in Table III are all commendable.

However, several logical issues deserve attention. First, the latency budget decomposition (Section IV-B) reveals that ~500 ms of the ~508 ms mean latency at $N = 10^5$ is regional coordinator queueing. This suggests the regional coordinator is a potential bottleneck, yet the paper does not explore sensitivity to $n_r$ (number of regional coordinators) or $\mu_r$ (regional processing rate) with the same rigor applied to $k_c$. The statement that "sensitivity to regional coordinator capacity ($\mu_r$) and number of regionals ($n_r$) should be explored before applying to specific mission designs" is insufficient—this is a first-order design parameter that should be characterized in the current study.

Second, the exception-based telemetry results (Table VII) validate only that the Bernoulli filtering reduces message counts as expected by the law of large numbers. The authors correctly note that "determining realistic exception rates as a function of orbital perturbation models and prediction accuracy is a necessary prerequisite for engineering application," but the gap between the validated bandwidth reduction and any actionable engineering recommendation is substantial. Without knowing what $p_{\text{exc}}$ values are physically realistic, the 2.5% overhead figure at $p_{\text{exc}} = 0.10$ is not meaningful for system design.

Third, the coordinator bandwidth analysis (Table VIII) identifies a 50 kbps zero-drop threshold, but the byte-budget queue model (tail-drop within a cycle) is a simplification. Real TDMA systems would schedule transmissions deterministically within the cycle, eliminating the "intra-cycle burstiness" that drives the gap between 25 kbps (95% success) and 50 kbps (zero-drop). The burstiness artifact is a consequence of the uniform random phase model, not a physical constraint—a TDMA-scheduled cluster would achieve zero drops at the theoretical minimum of ~20.5 kbps.

## 4. Clarity & Structure

**Rating: 4 (Good)**

The paper is well-organized and clearly written. The four-section structure (Introduction, Related Work, Simulation Framework, Results) follows IEEE conventions. The extensive use of tables (eleven total) and figures (eight total) supports the quantitative arguments effectively. The traffic accounting table (Table V) and abstraction scope table (Table III) are particularly valuable for reproducibility.

The abstract is accurate and appropriately detailed, though at ~250 words it is somewhat long for IEEE T-AES. The baseline interpretation note (Section I-C) is an excellent structural choice that preempts misinterpretation. The metric definitions (Section III-F) are precise and well-formulated.

Areas for improvement: The paper is excessively long for the contribution. At approximately 12,000 words (excluding references), it exceeds typical IEEE T-AES limits. Much of the length comes from defensive qualifications and repeated caveats about the reference baselines—while individually justified, their cumulative effect is to dilute the core message. The paper would benefit from consolidating the baseline caveats into a single, prominent discussion rather than repeating them in the abstract, introduction, Section I-C, Section III-B, Section IV-A, Section V-E, and the conclusion. The sectorized mesh discussion (Section V-C) is analytically interesting but, at ~400 words about work not done, could be shortened to a paragraph.

## 5. Ethical Compliance

**Rating: 4 (Good)**

The paper includes an appropriate disclosure of AI-assisted methodology in the Acknowledgment section, identifying specific AI models (Claude 4.6, Gemini 3 Pro, GPT-5.2) and clarifying that the AI-generated concepts are "not validated in the current study." The reference to a companion methodology paper [43] is appropriate. The data availability statement with a GitHub repository link supports reproducibility, though the commit hash is listed as "[PENDING]"—this must be resolved before publication.

The author attribution is unusual ("Project Dyson Research Team" with a footnote about individual names), which should be resolved per IEEE policy before final publication. There are no apparent conflicts of interest, though the affiliation with "Project Dyson" (which appears to be the subject of the study) should be clarified—is this an independent research organization, a university lab, or a commercial entity?

One minor concern: the paper references AI model versions (Claude 4.6, GPT-5.2) that do not exist as of the review date, suggesting either future-dated writing or fictional model names. This should be clarified.

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is appropriate for IEEE T-AES in scope, addressing autonomous spacecraft coordination with quantitative simulation results. The reference list (48 items) is comprehensive and covers the relevant literature in constellation management, swarm robotics, distributed systems, and queueing theory.

However, several important references are missing. The paper does not cite recent work on distributed space systems coordination, including: (1) the growing literature on autonomous satellite servicing and on-orbit assembly coordination; (2) recent publications on Starlink's actual coordination architecture (SpaceX has published some details at IAC conferences); (3) the CCSDS Spacecraft Onboard Interface Services (SOIS) standards relevant to inter-satellite coordination; and (4) recent work on consensus-based coordination specifically for satellite constellations (e.g., work by Bandyopadhyay et al. on SPHERES/Astrobee swarm experiments aboard ISS).

Several references are non-archival (SpaceX website, Amazon website, DARPA program pages, DoD fact sheets)—approximately 7 of 48 references. While some non-archival sources are unavoidable for current operational systems, the paper should minimize reliance on these and note their non-archival status more consistently. The reference to [43] (the companion methodology paper) appears to be a self-citation to an unpublished work hosted on the project's own website, which is not peer-reviewed.

---

## Major Issues

1. **The central DES contribution is circular.** The $O(1)$ overhead scaling is analytically guaranteed by the message model, and the DES abstracts away all phenomena that could perturb it. The paper needs either (a) to incorporate at least a minimal physical-layer model (e.g., TDMA scheduling within $T_c$) to demonstrate that the $O(1)$ property survives under more realistic conditions, or (b) to reframe the contribution away from "confirming $O(1)$ scaling" toward "quantifying the protocol coefficient and its sensitivity to design parameters." The current framing overstates the DES's contribution.

2. **Absence of a realistic decentralized comparator.** The global-state mesh is acknowledged as an intentional upper bound, and the sectorized mesh is identified as the most important future work. Without simulating the sectorized mesh, the paper cannot make meaningful claims about the hierarchical architecture's advantages over practical decentralized alternatives. This is the single most impactful addition that would strengthen the paper.

3. **Simulation fidelity is unclear.** The wall-clock times (0.2–7 seconds for year-long simulations of $10^3$–$10^5$ nodes) are suspiciously fast. The authors must clarify whether every individual message event is processed or whether batch/analytical shortcuts are used. If the latter, the claim of "full-participation DES" is misleading. Additionally, the near-zero MC variance suggests the simulation may be closer to an analytical calculator than a stochastic DES.

4. **Regional coordinator bottleneck is unexplored.** The latency decomposition shows that regional coordinator queueing dominates end-to-end latency (~500 ms of 508 ms). Yet $n_r$ and $\mu_r$ are not swept as design parameters with the same rigor as $k_c$. This is a first-order design variable that must be characterized.

5. **Coordinator bandwidth model conflates scheduling artifacts with physical constraints.** The 50 kbps zero-drop threshold arises from the uniform random phase model creating burstiness at the coordinator. A TDMA-scheduled cluster would eliminate this burstiness, reducing the zero-drop threshold to the theoretical minimum (~20.5 kbps). The paper should distinguish between the scheduling-dependent and scheduling-independent components of the bandwidth requirement.

## Minor Issues

1. **Abstract length.** At ~250 words, the abstract exceeds typical IEEE T-AES guidelines (~200 words). Consider condensing.

2. **Eq. (2):** The $M/D/1$ waiting time formula $W_q = \rho / [2\mu(1-\rho)]$ is the Pollaczek-Khinchine result for $M/D/1$, but the standard form is $W_q = \rho^2 / [2\lambda(1-\rho)]$ or equivalently $\rho / [2\mu(1-\rho)]$. Verify the form matches the reference [28].

3. **Table II (cluster size):** The latency values show discrete jumps (e.g., 508→340 ms between $k_c = 75$ and $k_c = 100$) rather than smooth variation. This is explained in the text as "distinct utilization regimes" at the regional coordinator, but the mechanism deserves more precise characterization—what causes the discrete transition?

4. **Section III-E, collision avoidance rate:** The 1,000:1 screening-to-maneuver ratio is stated but not cited. Provide a reference or mark as an assumption.

5. **Fig. 2 (latency distribution):** The $10^6$-node curve is labeled as "analytical extrapolation" but appears alongside DES-measured curves without clear visual distinction. Ensure the figure clearly differentiates measured from extrapolated data (e.g., different line style, explicit annotation).

6. **Data availability:** The commit hash is "[PENDING]"—must be resolved before publication.

7. **Author block:** "Project Dyson Research Team" with a footnote is non-standard for IEEE. Individual authors must be named per IEEE policy.

8. **Section III-B-3:** The mesh model uses fanout $f = O(N/\log N)$ to achieve $O(N^2)$ total messages, but earlier states that standard gossip uses $f = O(1)$ or $O(\log N)$. The choice of $f = O(N/\log N)$ should be justified more explicitly as a worst-case assumption rather than a standard gossip parameterization.

9. **Table I ($M/D/c$ sensitivity):** The "Representative System" column labels are informal (e.g., "Hyperscale data center"). Consider replacing with more precise descriptions or removing the column.

10. **Eq. (8), power overhead:** $\Delta P_{\text{avg}} = 15\text{ W}/100 = 0.15\text{ W}$, but the text states "incremental power for coordinator mode is 10–15 W above the 5 W baseline." Using the upper bound (15 W) without noting the range is slightly misleading.

11. **References [1], [3], [20], [21], [34], [43]:** Non-archival or self-published. Minimize or clearly flag these.

## Overall Recommendation

**Major Revision**

The paper addresses a relevant problem and is well-written with commendable intellectual honesty about its limitations. However, the central contribution—confirming an analytically predictable $O(1)$ scaling property via a DES that abstracts away all phenomena that could perturb it—is insufficient for IEEE T-AES. The absence of a realistic decentralized comparator (sectorized mesh), the unclear simulation fidelity (suspiciously fast runtimes for claimed full-participation simulation), the unexplored regional coordinator bottleneck, and the ceremonial nature of the Monte Carlo framework collectively indicate that the study, while thorough in its current scope, does not yet provide the depth of insight expected for this venue. A major revision incorporating at least a minimal physical-layer model, a sectorized mesh comparator, and a parametric sensitivity analysis over the dominant model parameters would substantially strengthen the contribution.

## Constructive Suggestions

1. **Implement a minimal TDMA scheduling model within the DES.** Even a simple model with $k_c$ time slots, guard intervals, and deterministic slot assignment would (a) resolve the coordinator bandwidth burstiness artifact, (b) test whether slot scheduling introduces scale-dependent effects, and (c) address the circularity concern by adding a physical-layer mechanism that could genuinely perturb the $O(1)$ prediction. This is the single highest-impact addition.

2. **Simulate the sectorized mesh.** The analytical treatment in Section V-C is promising but insufficient. Even a simplified sectorized mesh DES—with fixed sector sizes and local gossip—would provide a realistic decentralized comparator and transform the paper from a single-architecture characterization into a genuine architectural comparison. The authors' own analysis suggests this architecture "closely resembles" the hierarchical topology; quantifying the actual overhead gap would be a significant contribution.

3. **Replace the 30-replication MC framework with a parametric sensitivity analysis.** Since MC variance is negligible, the computational budget would be better spent sweeping message sizes ($\pm 50\%$), reporting rates ($r \in [0.01, 1.0]$), coordinator service rates, and MAC efficiency factors. This would characterize the engineering uncertainty bounds that practitioners actually need and would provide far more insight than 30 replications of a near-deterministic model.

4. **Characterize the regional coordinator as a design parameter.** Sweep $n_r \in \{5, 10, 20, 50, 100\}$ and $\mu_r \in \{200, 500, 1000, 2000\}$ msg/s. Since regional queueing dominates latency, this is arguably more important than the cluster size sweep already presented.

5. **Clarify simulation fidelity.** Provide explicit event counts per run (total events processed), confirm that every individual message is instantiated as a DES event, and explain how a year-long simulation of $10^5$ nodes completes in 7 seconds. If batch processing or analytical shortcuts are used for any event type, disclose this clearly and discuss implications for the "full-participation" claim.