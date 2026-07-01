---
paper: "02-swarm-coordination-scaling"
version: "al"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-27"
recommendation: "Major Revision"
---

# Peer Review: "Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study"

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a genuinely important problem: how to coordinate autonomous spacecraft swarms at scales of 10³–10⁵ nodes under bandwidth-constrained conditions. The framing around the RF-backup/safe-mode regime (1 kbps per node) is well-motivated and practically relevant—this is indeed the binding design point for coordination protocol sizing. The systematic byte-level traffic accounting across multiple topologies fills a gap between the swarm robotics literature (which rarely exceeds hundreds of agents) and the constellation management literature (which assumes centralized ground control).

However, the novelty is significantly undermined by the paper's own admissions. The $O(1)$ overhead scaling is described as "an analytical property of the fixed-depth hierarchical message structure" (Section I-D), and the DES matches closed-form predictions to within 0.1% at all fleet sizes (Table VII). The AoI result matches the geometric distribution exactly. The GE retransmission result ($1 - 0.9^3 = 27.1\%$) is a one-line calculation. The paper repeatedly and commendably acknowledges that "we do not claim the DES discovers emergent phenomena," but this raises the question of what the DES *does* contribute that could not be obtained from the analytical expressions alone. The joint-independence verification (Section IV-D) is the strongest candidate for DES-specific value, but the independence result is explained post hoc by the observation that lost messages never reach the coordinator queue—an insight that is arguably obvious from the architecture description.

The contribution would be stronger if the paper either (a) identified a regime where analytical predictions break down and the DES reveals unexpected behavior, or (b) positioned itself more explicitly as a *design tool paper* providing a validated, open-source parametric framework for the community, rather than claiming characterization results that are largely analytical.

## 2. Methodological Soundness

**Rating: 3 (Adequate)**

The simulation framework is clearly described and the parameter choices are generally well-justified. The cycle-aggregated approach is appropriate for the message-layer abstraction, and the vectorized implementation enabling ~7s runtimes at N=10⁵ is practical. The Monte Carlo framework with 30 replications per configuration is standard, and the authors correctly note that the near-deterministic message model renders MC variance negligible (SD < 0.001%).

**Concerns about the simulation's fidelity and value proposition:**

First, the term "discrete event simulation" is used loosely. The authors acknowledge this is not a per-packet DES but a cycle-aggregated model where "individual bit-level or packet-level events are not instantiated" (Section III-A). The atomic unit is a message-layer event within a fixed 10-second cycle. This is closer to a *cycle-stepped analytical accounting tool* than a DES in the traditional sense (e.g., as implemented in NS-3 or OMNeT++). The paper should either adopt more precise terminology or justify the DES label more rigorously.

Second, the spatial model is essentially absent. Nodes are not placed in orbits; there is no orbital mechanics, no Earth occlusion geometry, no time-varying link topology. The "cluster" concept assumes co-moving nodes but does not model the dynamics of cluster membership as orbits precess. The neighbor discovery in the sectorized mesh uses a "global position oracle" updated at zero bandwidth cost (Section III-B.4). These abstractions are acknowledged but significantly limit the applicability of the results to real constellation operations.

Third, the coordinator queueing model deserves scrutiny. The cluster coordinator is modeled as M/D/1 with $\mu_c = 200$ msg/s, but the arrival process from $k_c$ members with uniform random phase offsets within a 10-second cycle is not Poisson—it is a superposition of periodic sources. The Palm-Khintchine justification (Section III-B.1) applies to the centralized server with large N, but at the cluster level with $k_c = 100$, the Poisson approximation is less accurate. The authors should quantify the departure from Poisson at the cluster level.

Fourth, the validation against the Pollaczek-Khinchine formula "at low utilization ($N = 100$, $r = 0.01$)" is a weak test—any reasonable model agrees at low utilization. Validation should target the high-utilization regime where queueing effects matter.

## 3. Validity & Logic

**Rating: 3 (Adequate)**

The analytical cross-checks are thorough and the paper is commendably honest about the limitations of its results. The dual-regime interpretation (Section IV-F.3) correctly contextualizes the 1 kbps constraint. The acknowledgment that centralized compute "does not diverge until $N \approx 10^6$" (Section IV-G) is refreshingly candid and prevents the paper from overclaiming the hierarchical architecture's advantages.

**However, several logical issues require attention:**

The baseline comparisons are problematic despite the authors' disclaimers. The single-server centralized model ($c = 1$) is acknowledged as an "intentional worst-case bound," and the global-state mesh is an "intentional upper bound." While these are labeled as such, they still appear in the topology comparison table (Table IX) and Figure 8, where a reader scanning results could draw misleading conclusions. The realistic centralized baseline ($c = N/k_c$) is the appropriate comparator, and the paper should lead with this comparison more prominently in all figures and tables.

The claim that "the hierarchical advantage is fault tolerance during ground outages (7–29 min/day)" deserves more rigorous treatment. The 7–29 min/day figure assumes a single ground station; operational constellations use multiple ground stations and relay satellites (e.g., TDRSS), achieving much higher availability. The paper should compare against a multi-station ground architecture.

The joint-independence result (Section IV-D, Table VI) shows identical drop counts under "No Loss" and "GE Only" conditions. This is presented as a DES finding, but it follows directly from the architecture: if GE losses occur before the coordinator ingress queue, lost messages cannot cause drops. The DES confirms this but does not discover it. The paper should be more explicit that this is an architectural property verification, not an empirical finding.

The AoI-to-position-error coupling (Eq. 14) uses a linear model ($\dot{\sigma} = 0.5$ m/s) that the authors correctly caveat as "order-of-magnitude." However, the resulting 230 m uncertainty at P99 AoI is then compared to conjunction screening thresholds without accounting for the fact that conjunction probability depends on the *relative* position uncertainty of two objects, not the absolute uncertainty of one. This comparison, even as a "back-of-the-envelope" calculation, could mislead readers about the operational implications.

## 4. Clarity & Structure

**Rating: 4 (Good)**

The paper is generally well-written and logically organized. The roadmap at the beginning of Section IV is helpful. The traffic accounting tables (Tables III, IV, V) provide excellent transparency about what is and is not included in the overhead metric. The design equations summary (Section V-C) is a useful practitioner reference.

The paper is, however, excessively long for the results it presents. At approximately 12,000 words of body text plus extensive tables, it could be reduced by 30–40% without loss of content. Specific areas for compression: the sectorized mesh model (Section III-B.4) occupies nearly two columns but serves primarily as an intermediate comparator; the coordinator capacity analysis (Section IV-A) repeats the same result (21–50 kbps) through four different scheduling models; and the exception-based telemetry validation (Section IV-F.4) confirms a trivially predictable Bernoulli scaling.

The notation is generally consistent, though the paper uses both $\eta$ and $O_{\text{protocol}}$ for protocol overhead, and the distinction between offered and delivered overhead ($\eta$ vs. $\eta_{\text{delivered}}$) is introduced in Section III-E but not consistently maintained in all results tables. Table IV (coordinator bandwidth) reports $\eta$ but the caption does not specify whether this is offered or delivered.

Figures are referenced but provided as PDF placeholders (e.g., `fig-architecture-diagram.pdf`), so their quality cannot be assessed. The figure captions are informative.

## 5. Ethical Compliance

**Rating: 5 (Excellent)**

The paper provides exemplary transparency about AI-assisted methodology. The Acknowledgment section explicitly names the AI models used (Claude 4.6, Gemini 3 Pro, GPT-5.2), describes their role as "exploratory AI-assisted ideation," and clearly states that the AI-generated concepts are "not validated in the current study." The companion methodology paper is cited. The data availability statement provides repository URLs, version tags, and software environment details. Author anonymization is noted as temporary per IEEE policy.

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is appropriate for IEEE TAES in scope, addressing autonomous spacecraft coordination at scale. The reference list is comprehensive (50 references) and covers the relevant literature in distributed systems, swarm robotics, constellation management, and queueing theory.

**However, several referencing issues exist:**

Multiple references are to non-archival sources (FCC filings, DARPA program pages, Amazon marketing materials, DoD fact sheets). While some of these are unavoidable for operational constellation data, the paper should minimize reliance on non-archival sources for technical claims. The SpaceX reference [1] cites an FCC filing and a personal website ("planet4589.org"); the latter is inappropriate for a journal publication even with the "non-archival" caveat.

The paper does not cite several relevant works on distributed satellite autonomy: the ESA OPS-SAT mission (on-board autonomous operations), the NASA Autonomous Sciencecraft Experiment (EO-1), or recent work on distributed space systems by Nag et al. and Radhakrishnan et al. The DTN/BPv7 literature is cited but not engaged with substantively—given that store-and-forward recovery is a key result (Section IV-C), deeper engagement with the DTN transport literature would strengthen the paper.

The reference to future AI models (Claude 4.6, GPT-5.2) in the Acknowledgments suggests this paper may be set in a near-future timeframe, which is unusual for a technical journal submission. If these are real model versions, no issue; if speculative, this should be clarified.

## Major Issues

1. **The DES adds minimal value beyond analytical predictions.** The paper's own cross-checks show <0.1% deviation between DES and closed-form results for overhead, exact agreement for AoI, and architecturally obvious independence for the joint interaction test. The paper needs to either (a) identify a concrete scenario where the DES reveals behavior not predicted by analysis, or (b) reframe the contribution as a validated open-source design tool rather than a characterization study. The current framing falls between these two stools.

2. **Absence of spatial/orbital modeling undermines applicability claims.** The paper claims relevance to "autonomous space swarms" but models neither orbital mechanics, Earth occlusion, nor time-varying link topology. Cluster membership is static; the "500 km cluster diameter" vignette (Section IV-A) is a one-off calculation, not integrated into the simulation. For a paper targeting IEEE TAES, the lack of any orbital dynamics—even simplified J₂-perturbed two-body—is a significant gap. At minimum, the title and abstract should more clearly scope the contribution as a *communication protocol* characterization rather than a *space systems* characterization.

3. **Baseline comparisons are structurally unfair despite disclaimers.** The single-server centralized model and global-state mesh are straw men. While the paper acknowledges this, the topology comparison table (Table IX) and Figure 8 still present these alongside the hierarchical architecture in a way that visually suggests superiority. The realistic centralized baseline ($c = N/k_c$) shows that centralized processing is viable to $N \approx 10^6$, and the hierarchical architecture's latency (335–675 ms) is *worse* than centralized (10–240 ms). The paper should restructure Section IV-G to lead with the realistic comparison and relegate the bounds to an appendix or supplementary material.

4. **The 46% overhead headline number is misleading.** This is the stress-case (one 512-byte command per node per cycle), which the paper itself describes as "an extreme bound" representing "fleet-wide coordinated maneuver campaigns." The nominal operating point is ~5%. Leading with 46% in the abstract and throughout creates a false impression of high overhead. The abstract should lead with the nominal 5% and present the 46% as the stress-case upper bound.

## Minor Issues

1. **Section III-A, paragraph 1:** "We use the term 'discrete event simulation (DES)' in the sense that..." — this defensive definition suggests the authors are aware the term is being stretched. Consider "cycle-aggregated message-layer simulation" as a more accurate descriptor.

2. **Eq. (6), mesh convergence:** The claim $R_{\text{conv}} = \max(\lceil\log_2 N\rceil, \lceil N/(bf)\rceil)$ conflates two different convergence criteria (epidemic spread of a single entry vs. throughput-limited delivery of all entries). The max operator is correct but the derivation should be clearer.

3. **Table II (M/D/c sensitivity):** The "Hyperscale data center" row ($c = 1000$, $N_{\max} = 10^7$) is speculative and not grounded in any cited reference for space operations ground systems.

4. **Section III-D (Monte Carlo):** "SD < 0.001% for overhead across 30 replications" — if variance is this low, 30 replications are unnecessary. The paper should either justify 30 runs (e.g., for failure-process statistics) or reduce to a smaller number with justification.

5. **Table V (coordinator bandwidth):** The $C_{\text{coord}} = 1$ kbps row showing 100% drops and 0% delivery is trivially obvious and wastes table space.

6. **Eq. (9), Chernoff bound:** The notation $\alpha p$ in $D_{\text{KL}}(\alpha p \| p)$ is non-standard; clarify that this is the KL divergence between Bernoulli($\alpha p$) and Bernoulli($p$).

7. **Section IV-B:** "Bootstrap 95% confidence intervals on the DES P99 are [438, 444] s" — a 6-second CI on a 440-second quantity (1.4% relative width) from a near-deterministic model is not informative. This reinforces the concern that the MC framework adds little value.

8. **Table VIII (link availability):** Footnote markers are inconsistent — superscript "b" is used for both "Per-message delivery rate" and the offered-load warning, and superscript "c" appears in the footnote but not in the table body.

9. **Section V-B:** "Simplified orbital mechanics suffice for communication distances but not perturbation dynamics" — this understates the issue. No orbital mechanics are modeled at all; communication distances are fixed parameters, not computed from orbital state.

10. **Data Availability:** The repository URL (github.com/projectdyson/dyson) should be verified as accessible. The tag `paper-02-v-al` suggests this is version AL of paper 02, which is unusual versioning for a journal submission.

## Overall Recommendation

**Major Revision**

The paper addresses an important problem and demonstrates commendable transparency about its assumptions, limitations, and the role of AI assistance. The traffic accounting framework is thorough and the design equations summary is practically useful. However, the core contribution—a DES that reproduces analytical predictions to within 0.1%—does not meet the novelty threshold for IEEE TAES without either (a) demonstrating scenarios where the simulation reveals behavior beyond analytical prediction, or (b) substantially reframing the contribution as a validated design tool with demonstrated utility for practitioners. The absence of orbital dynamics modeling, the structurally unfair baseline comparisons (despite disclaimers), and the misleading stress-case headline number require significant revision. The paper is approximately 40% longer than necessary for its content.

## Constructive Suggestions

1. **Add a single-cluster packet-level validation.** Even a simplified NS-3 or OMNeT++ model of one 100-node cluster with TDMA scheduling would ground the MAC efficiency assumption ($\gamma$) and demonstrate that the message-layer abstraction is valid. This would transform the paper from "analytical results verified by a cycle-stepped calculator" to "message-layer model validated against packet-level simulation," substantially strengthening the contribution.

2. **Incorporate minimal orbital dynamics.** A J₂-perturbed propagator for a single orbital shell would enable time-varying cluster membership, realistic Earth-occlusion link outages, and dynamic neighbor sets for the sectorized mesh. This would create scenarios where analytical predictions may not hold (e.g., correlated link outages across a cluster during Earth shadow), giving the DES genuine discovery potential.

3. **Restructure around the nominal operating point.** Lead with $\eta \approx 5\%$ (nominal) as the headline result, present the $9\times$ design envelope as the range, and relegate the stress-case 46% to a sizing bound. This more accurately represents the expected operational regime and avoids the impression that hierarchical coordination consumes half the control-plane bandwidth.

4. **Compress the paper by ~30%.** Merge the four coordinator ingress models (Section IV-A) into a single table with a brief narrative; reduce the sectorized mesh description to essential parameters; eliminate trivially predictable validation results (exception telemetry Bernoulli scaling); and move the global-state mesh and single-server centralized bounds to supplementary material.

5. **Engage more deeply with DTN/BPv7 for the inter-cycle recovery result.** The store-and-forward recovery to 95% coverage in 4–7 cycles (Section IV-C) is the most operationally relevant finding. Connecting this to BPv7 custody transfer semantics and comparing recovery timelines against DTN bundle lifetime parameters would strengthen the paper's relevance to the space networking community and provide actionable design guidance.