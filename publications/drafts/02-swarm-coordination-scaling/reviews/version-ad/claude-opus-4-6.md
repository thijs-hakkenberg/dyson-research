---
paper: "02-swarm-coordination-scaling"
version: "ad"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-27"
recommendation: "Major Revision"
---



# Peer Review: "Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study"

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a legitimate gap: systematic comparison of coordination architectures for autonomous spacecraft swarms at the 10³–10⁵ scale with explicit byte-level traffic accounting. The motivation is timely given mega-constellation growth (Starlink, Kuiper, OneWeb) and aspirational concepts for larger fleets. The framing around a fixed 1 kbps per-node coordination budget is a useful engineering constraint that grounds the analysis.

However, the novelty is more limited than the paper initially suggests. The authors commendably acknowledge (Section I-D, Section IV-E) that the $O(1)$ overhead scaling is "a direct mathematical consequence of the hierarchical structure" with fixed depth, and that "individual metrics are analytically tractable in isolation." The DES essentially confirms closed-form predictions to within 0.1% (Table VII), with Monte Carlo variance below 0.001%. This raises a fundamental question about the incremental contribution of the simulation over the analytical framework. The authors position the DES as a "validated parametric sweep tool," but the near-perfect agreement with analytics across the entire parameter space suggests the system is too simple to produce emergent or non-obvious behaviors. The most interesting results—coordinator burstiness (Section IV-A), AoI characterization (Section IV-B), and Gilbert-Elliott loss analysis (Section IV-C)—are themselves analytically tractable (the authors provide closed-form cross-checks that match to within one cycle period).

The sectorized mesh comparator (Section III-B.4) is a welcome addition that provides a more realistic decentralized baseline than the global-state mesh upper bound. The neighbor-cap sensitivity analysis (Table IV) adds practical value. However, the paper would benefit from comparison against more sophisticated existing architectures—e.g., hierarchical gossip protocols, structured overlays (Chord/Pastry adapted for space), or the GNN-based controllers cited in the related work (Tolstaya et al., Li et al.) that claim linear communication complexity.

## 2. Methodological Soundness

**Rating: 3 (Adequate)**

The simulation framework is clearly described and the parameter space is comprehensive. The cycle-aggregated DES approach is appropriate for the message-layer abstraction level, and the full-participation model (all N nodes active every cycle) avoids sampling artifacts. The Monte Carlo framework with 30 replications per configuration is standard, though the authors correctly note the near-deterministic nature makes this largely confirmatory.

Several methodological concerns warrant attention:

**Cycle-aggregated abstraction validity.** The paper abstracts away MAC-layer scheduling, link acquisition, pointing constraints, half-duplex turnaround, and antenna beam scheduling (Table III). While the $\gamma \in [0.7, 0.9]$ factor is offered as a correction, this is a scalar multiplier applied to a complex, potentially scale-dependent phenomenon. At 10⁵ nodes with rotating coordinators, MAC contention, hidden terminal problems, and link acquisition overhead could introduce nonlinear effects that a simple efficiency factor cannot capture. The authors acknowledge this (Section V-B) but the gap between the message-layer model and physical reality is substantial enough to question whether the quantitative results (e.g., "21–50 kbps" coordinator capacity) are actionable for system design without the packet-level validation they identify as future work.

**Queueing model assumptions.** The centralized baseline uses an M/D/1 queue with $\mu_s = 1000$ msg/s, which the authors acknowledge is an "intentional worst-case bound." While the M/D/c sensitivity analysis (Table I) partially addresses this, the centralized baseline still serves as a comparison point in figures and tables. A reader skimming results could misinterpret the centralized divergence at 10⁴ nodes as a fundamental limitation rather than an artifact of the single-server parameterization. The paper would benefit from plotting the $c = 10$ or $c = 100$ centralized curves alongside the hierarchical results in Fig. 6.

**Gilbert-Elliott parameterization.** The GE model parameters ($p_G = 0.01$, $p_B = 0.90$, $p_{GB} = 0.05$/cycle, $p_{BG} = 0.20$/cycle) are stated without empirical justification from actual LEO ISL measurements. The steady-state availability of 80% and the transition rates are design parameters, not validated against operational data. The qualitative conclusion (correlated losses defeat intra-cycle retransmission) is sound, but the specific recovery percentages (27% vs. 87.5%) are parameter-dependent.

**Collision avoidance rate.** The $10^{-4}$/node/s rate is justified as a screening event rate (1000:1 ratio to maneuvers), but this ratio is cited without a specific reference. The sensitivity analysis ($10^{-5}$ to $10^{-3}$) showing preserved topology ranking is helpful but reported only in text without tabulated data.

## 3. Validity & Logic

**Rating: 3 (Adequate)**

The paper is generally careful about distinguishing what is analytically derived versus DES-measured, and the authors are transparent about the near-deterministic nature of the results. The closed-form cross-checks (Eq. 8 for AoI, Eq. 7 for retransmission, traffic accounting in Table VI) are a strength. The conclusions are appropriately hedged—particularly the AoI-to-position-error coupling (Eq. 9), which is clearly labeled as "illustrative back-of-the-envelope."

However, several logical issues deserve attention:

**Circular validation concern.** The DES and the analytical model use identical message sizes, rates, and accounting rules. The <0.1% agreement (Table VII) is expected by construction—the DES is essentially computing the same sums as the closed-form expressions, with the only stochastic perturbation being the 2%/year failure process. The paper claims the DES "ensures the analytical bookkeeping is correctly integrated across the full parameter space," but this is a weak form of validation. A more convincing validation would compare against an independent implementation or a higher-fidelity simulator.

**Topology comparison fairness.** The comparison between hierarchical ($\eta \approx 46\%$) and sectorized mesh ($\eta \approx 65–67\%$) is sensitive to workload assumptions. The sectorized mesh includes peer heartbeats (32 B × 10 neighbors) that the hierarchical topology does not require because the coordinator aggregates state. But the hierarchical topology requires coordinator commands (512 B per node per cycle under stress-case) that the sectorized mesh may not need if nodes can coordinate locally. The comparison implicitly assumes identical workloads across architectures, but the architectures may enable different operational paradigms with different command rates.

**Extrapolation beyond validated range.** Fig. 5 includes a $10^6$-node curve labeled as "analytical extrapolation, not DES-measured." While this is clearly noted, the extrapolation assumes the fixed-depth hierarchy continues to work at $10^6$ nodes. At this scale, the number of regional coordinators or the regional coordinator ingress rate may become a bottleneck not captured by the current model.

**Per-cycle completion metric.** The per-cycle completion analysis (Section IV-C) correctly shows that $(1-p_{\text{loss}})^{k_c}$ decays rapidly, but this metric may be overly conservative. In practice, a coordinator receiving 95 of 100 reports can still compute a useful cluster summary; requiring 100% completion per cycle is an unnecessarily strict criterion. The paper would benefit from analyzing a softer completion threshold (e.g., 90% or 95% of members reporting).

## 4. Clarity & Structure

**Rating: 4 (Good)**

The paper is well-organized with a clear roadmap at the beginning of Section IV. The writing is precise and technical terms are consistently defined. The extensive use of tables (I–XI) and figures (1–14) supports the quantitative arguments effectively. The abstraction scope table (Table III) is particularly helpful for understanding what the DES does and does not model.

The abstract is dense but accurate, covering all four primary contributions with appropriate quantitative specifics. The "Baseline Interpretation Note" (Section I-C) is a valuable addition that preempts misinterpretation of the reference baselines.

Several clarity issues remain:

**Paper length and redundancy.** At approximately 12,000 words of body text plus extensive tables, the paper is at the upper limit for IEEE T-AES. There is noticeable redundancy: the $\eta \approx 46\%$ figure is stated at least 15 times; the MAC efficiency caveat ($\times 1/\gamma$) appears in the abstract, contributions, multiple results sections, and conclusion. The traffic accounting is explained in Section III-E, Table VI, Table V, and again in Section IV-E. Consolidating these would improve readability without losing information.

**Notation consistency.** The paper uses $C_{\text{node}}$ for per-node bandwidth, $C_{\text{coord}}$ for coordinator capacity, $\mu_s$ for server processing rate, and $\mu_c$ for cluster coordinator processing rate. While each is defined, the proliferation of capacity-related symbols can be confusing. A notation table would help.

**Figure quality.** All figures are referenced as PDF includes but not provided for review. The captions are descriptive, but several figures appear to present straightforward analytical relationships (e.g., Fig. 10 showing linear $\eta$ vs. $p_{\text{cmd}}$) that could be replaced by equations, freeing figure slots for more informative visualizations.

## 5. Ethical Compliance

**Rating: 4 (Good)**

The paper includes an appropriate acknowledgment of AI-assisted ideation (Claude 4.6, Gemini 3 Pro, GPT-5.2) in the Acknowledgment section, with a reference to a companion methodology paper. The disclosure is specific about what the AI tools contributed ("architectural concepts including a heterogeneous 'Shepherd/Flock' hardware class design") and clearly states this concept "is not validated in the current study." This is a responsible and transparent disclosure.

The author attribution uses a team name ("Project Dyson Research Team") with a note that individual names will be provided for final publication. While this is acceptable for review, IEEE policy requires named authors for publication. The data availability statement is comprehensive, including repository URL, version tag, and software environment details.

One minor concern: the AI model version numbers cited (Claude 4.6, GPT-5.2) do not correspond to any publicly known releases as of the apparent submission date. If these are internal/beta versions, this should be clarified; if they are speculative future versions, this raises questions about the timeline of the work.

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is appropriate for IEEE T-AES given its focus on autonomous spacecraft coordination architectures. The reference list (50 citations) covers the relevant domains: constellation operations, swarm robotics, distributed systems theory, queueing theory, and space communication standards.

Several referencing gaps are notable:

**Missing recent work.** The paper does not cite recent work on distributed space systems coordination that has appeared since 2020, including: (a) the growing literature on federated learning for satellite constellations; (b) recent DTN performance studies over operational ISLs; (c) the CCSDS Spacecraft Onboard Interface Services (SOIS) standards relevant to intra-cluster communication; (d) recent results from the Starlink V2 ISL deployment that provide empirical data on ISL performance at scale.

**Non-archival references.** Several references are non-archival (SpaceX website, Amazon website, DARPA program pages, DoD fact sheets). While these are appropriately flagged, the paper relies on them for key claims about current operational scale. Where possible, peer-reviewed or conference sources should be substituted.

**Self-citation.** Reference [38] (companion methodology paper) is cited but appears to be unpublished and hosted on the project website. This is acceptable for context but should not be relied upon for methodological claims that reviewers cannot verify.

**Age of Information literature.** The AoI citations (Kaul 2012, Yates 2021, Kadota 2018) are appropriate foundational references, but the paper does not engage with the substantial recent AoI literature on scheduling policies for multi-source systems, which is directly relevant to the exception-based telemetry analysis.

---

## Major Issues

1. **Limited incremental value of DES over closed-form analysis.** The DES matches analytical predictions to within 0.1% across the entire parameter space, with MC variance below 0.001%. The paper acknowledges this but does not adequately justify why a simulation paper is needed when the analytical framework appears sufficient. The authors should either (a) identify specific parameter regimes where the DES reveals behaviors not predicted by the closed-form model, or (b) reframe the contribution more explicitly as a validated reference implementation and design tool, with the analytical framework as the primary contribution. Currently the paper oscillates between these framings.

2. **Physical-layer gap undermines quantitative design guidance.** The headline results (21–50 kbps coordinator capacity, $\eta = 46\%$) are presented as design inputs, but the message-layer abstraction omits MAC scheduling, link acquisition, beam scheduling, and half-duplex constraints that could introduce scale-dependent effects. The $\gamma$ correction factor is a first-order approximation. Without at least a single-cluster packet-level validation (identified as future work in Section V-A item 2), the quantitative precision of the results exceeds the accuracy of the model. The paper should either include a preliminary packet-level comparison or more prominently caveat the quantitative results as order-of-magnitude estimates.

3. **Unfair topology comparison.** The centralized baseline ($c = 1$) and global-state mesh (full replication) are acknowledged as intentional bounds, but they still appear in comparison figures (Fig. 6) and tables (Table VIII) alongside the hierarchical architecture, creating a visual impression of superiority that is partly an artifact of parameterization. The sectorized mesh is a fairer comparator, but the comparison assumes identical workloads. The paper should (a) include $c = 10$ or $c = 100$ centralized curves in Fig. 6, and (b) discuss whether the sectorized mesh might enable lower command rates through local coordination, which would change the overhead comparison.

4. **Absence of dynamic topology effects.** The hierarchical topology is static within each coordination cycle: cluster assignments are fixed, coordinator rotation follows a deterministic schedule, and the hierarchy depth is constant at 4. Real autonomous swarms would experience dynamic cluster membership (nodes entering/leaving due to orbital mechanics), contested coordinator elections, and topology adaptation. The paper does not model or discuss these effects, which could significantly impact the $O(1)$ scaling claim at larger scales.

---

## Minor Issues

1. **Section I-D, contribution 1:** "any form of temporal spreading (TDMA, phase stagger, or token-bucket shaping) converges to ~21–25 kbps" — this convergence is expected since all three methods eliminate burstiness; the result is not surprising but the framing suggests it is a finding.

2. **Eq. 4 and surrounding text:** The hierarchical message count $M_{\text{total}} = N + N/k_c + N/(k_c \cdot k_r)$ counts only uplink reporting. The text notes bidirectional traffic "approximately doubles the overhead," but the factor is not exactly 2 — it depends on the command rate. This should be made precise.

3. **Table II (Mesh Traffic Accounting):** The gossip redundancy factor "~1.4×" is stated without derivation. This factor depends on the gossip protocol variant and should be justified or cited.

4. **Section III-B.4:** The sectorized mesh heartbeat size (32 B) vs. hierarchical heartbeat size (64 B) is explained in a footnote. This asymmetry should be discussed in the main text, as it affects the overhead comparison.

5. **Table VII:** The intermediate fleet sizes (5k–80k) are "omitted for brevity" with a note that $\eta_{\text{DES}} = 46.0\%$ at all sizes. Given that the point of the table is to demonstrate scale invariance, showing at least 3–4 intermediate points would strengthen the claim without excessive space.

6. **Section IV-B, Eq. 9:** The along-track uncertainty growth rate $\dot{\sigma} = 0.5$ m/s is cited as "typical for LEO at 400–600 km altitude" with reference to Vallado. This is a reasonable order of magnitude but varies significantly with solar activity, ballistic coefficient, and altitude. A range (e.g., 0.1–1.0 m/s) would be more appropriate.

7. **Section IV-C:** "Per-cycle cluster completion drops below 1%" — this is for the i.i.d. case at $p_s = 0.875$, $k_c = 50$. The text should clarify that this is the i.i.d. case; the GE case is astronomically worse.

8. **Table IX (Duty Cycle):** "Handoff Success" of 95.0% at 1-hour duty cycle seems low. What failure mode causes 5% handoff failures? This is not explained.

9. **Acknowledgment section:** "Claude 4.6 (Anthropic), Gemini 3 Pro (Google DeepMind), and GPT-5.2 (OpenAI)" — these version numbers do not correspond to known public releases. Clarify whether these are actual or projected model versions.

10. **Data Availability:** The repository tag "paper-02-v-ad" suggests this is version AD of paper 02. The versioning scheme should be explained or simplified for publication.

11. **Eq. 6, convergence time:** $T_{\text{converge}} = D \cdot \tau_{\text{gossip}}$ with $D = O(N^{1/3})$ for a random geometric graph in 3D. This assumes uniform spatial distribution; LEO constellations have highly non-uniform spatial distributions (concentrated in orbital shells). The diameter scaling may differ.

12. **Section III-D (Monte Carlo):** Seeds 42–71 are sequential integers, which is fine for Mersenne Twister but should be noted as producing independent streams only if the generator period is much larger than the per-run consumption (it is, but stating this explicitly would be good practice).

---

## Overall Recommendation

**Major Revision**

The paper addresses a relevant problem with a well-documented simulation framework and provides useful engineering design guidance for hierarchical coordination of large spacecraft swarms. The traffic accounting is meticulous, the analytical cross-checks are thorough, and the presentation is generally clear. However, the near-perfect agreement between DES and closed-form predictions raises fundamental questions about the simulation's incremental value, the physical-layer abstraction gap limits the actionability of the quantitative results, and the topology comparison is partially an artifact of baseline parameterization. A major revision should: (1) more clearly delineate what the DES reveals beyond the analytical framework; (2) include at least a preliminary packet-level validation for a single cluster; (3) present fairer centralized baselines ($c > 1$) in comparison figures; and (4) discuss dynamic topology effects. The core contributions—coordinator capacity sizing, AoI characterization, and correlated loss analysis—are sound and publishable after these revisions.

---

## Constructive Suggestions

1. **Include a single-cluster packet-level validation.** Even a simplified NS-3 or OMNeT++ model of one 100-node cluster with realistic TDMA scheduling would ground the $\gamma$ assumption and dramatically strengthen the paper's credibility. This need not cover the full parameter space—a single operating point showing agreement (or calibrated disagreement) between message-layer and packet-layer models would suffice.

2. **Reframe the DES contribution around the joint parameter sweep.** Rather than positioning the DES as discovering new phenomena, emphasize its value as a *design tool* that allows practitioners to quickly evaluate specific operating points (workload profile × cluster size × duty cycle × loss model × MAC efficiency) without re-deriving the analytics. Provide a worked example: "A system engineer designing a 50,000-node swarm with 10 kbps/node budget and TDMA scheduling would use Table X to select $k_c = 150$, $\tau_d = 24$ h, $p_{\text{exc}} = 0.30$, yielding $\eta_{\text{eff}} \approx 18\%$ with P99 AoI $\approx 130$ s."

3. **Add a relaxed completion metric.** Replace or supplement the all-or-nothing per-cycle completion with a threshold-based metric (e.g., fraction of cycles where ≥90% of cluster members report). This would provide a more operationally relevant measure of coordination quality under lossy conditions and would differentiate the i.i.d. and GE cases more meaningfully.

4. **Strengthen the sectorized mesh comparison.** The sectorized mesh is the most interesting comparator but receives relatively brief treatment. Consider: (a) allowing the sectorized mesh to use local coordination (reducing command overhead), (b) analyzing the conjunction screening effectiveness as a function of neighbor cap (not just overhead), and (c) discussing hybrid architectures that use sectorized mesh for local collision avoidance and hierarchical coordination for fleet-wide tasking.

5. **Discuss operational deployment path.** The paper would benefit from a brief discussion of how hierarchical coordination could be incrementally deployed in existing constellations—e.g., starting with ground-designated coordinators (no autonomous election) and progressively delegating authority as the protocol matures. This would connect the theoretical framework to near-term engineering practice and increase the paper's impact for the T-AES readership.