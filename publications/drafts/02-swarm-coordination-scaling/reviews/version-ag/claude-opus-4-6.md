---
paper: "02-swarm-coordination-scaling"
version: "ag"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-27"
recommendation: "Major Revision"
---

# Peer Review: "Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms"

**Manuscript Version:** AG
**Venue:** IEEE Transactions on Aerospace and Electronic Systems

---

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a genuinely important problem: how to coordinate autonomous spacecraft swarms at scales of 10³–10⁵ nodes. The gap identified—the absence of systematic byte-level traffic accounting for hierarchical coordination at these scales—is real and relevant given the trajectory of mega-constellation deployments. The four contributions (coordinator capacity sizing, AoI characterization, correlated loss analysis, and joint independence verification) are each useful engineering inputs for system designers.

However, the novelty is more limited than the framing suggests. The paper's own analysis repeatedly demonstrates that individual metrics are "analytically tractable in isolation" (Abstract, Section IV-B, IV-C). The $O(1)$ overhead scaling is, as the authors acknowledge, "a direct mathematical consequence of the hierarchical structure" (Section IV-F). The AoI result matches a geometric distribution exactly. The GE retransmission result is a straightforward calculation ($1 - 0.9^3 = 27.1\%$). The DES's primary novel contribution—verifying joint independence of failure modes (Section IV-D)—is valuable but narrow: the independence result is intuitively expected (link-layer losses occur before coordinator ingress, so lost messages never contend for queue capacity), and the paper confirms this rather than discovering a surprising interaction.

The honest framing as a "parametric design-space characterization" (Section I-D) is appreciated, but this positions the work closer to a systems engineering trade study than a research contribution advancing fundamental understanding. For IEEE T-AES, the paper would benefit from demonstrating at least one result where the DES reveals behavior that analytical models cannot predict—the joint independence verification comes closest but the result is unsurprising. The workload design envelope ($9\times$ spread) is a useful practical contribution but is essentially a sensitivity analysis over a linear parameter.

---

## 2. Methodological Soundness

**Rating: 3 (Adequate)**

The simulation framework is clearly described and the parameter space is well-documented (Table III is commendably thorough). The Monte Carlo approach with 30 replications per configuration is standard, and the authors are transparent that the near-deterministic message model renders MC variance negligible (SD < 0.001%). The analytical cross-checks throughout (Pollaczek-Khinchine validation, geometric AoI prediction, Chernoff burstiness bound) are a methodological strength.

Several methodological concerns warrant attention:

**Cycle-aggregated abstraction validity.** The core methodological choice—cycle-aggregated DES at 10-second resolution—is the source of both the computational efficiency and the primary limitation. The paper acknowledges this but does not adequately bound the error introduced. The claim that "MAC efficiency γ ∈ [0.7, 0.9] scales absolute bandwidth by 1/γ" (used throughout) assumes MAC overhead is a multiplicative constant independent of offered load, which is only true for scheduled access (TDMA). For contention-based protocols, throughput is a nonlinear function of offered load (the paper notes Slotted ALOHA's 1/e limit in Section III-F but then proceeds to use the linear scaling assumption). The MAC contention caveat in Section IV-G is insufficient—this is a fundamental modeling limitation, not a caveat.

**Baseline construction.** The centralized baseline with $c = 1$ server is acknowledged as an "intentional worst-case bound," but it dominates the visual comparison in Fig. 5 and Table IX. While the $c = N/k_c$ realistic baseline is discussed, it is not given equal visual weight. The global-state mesh requiring $O(N^2)$ traffic is similarly an extreme bound. The paper's topology comparison thus brackets the hierarchical architecture between two unrealistic extremes, with only the sectorized mesh providing a meaningful comparator. This weakens the comparative claims.

**Sectorized mesh parameterization.** The $\sqrt{N}$ sector sizing (Section III-B.4) is described as "an order-of-magnitude sizing, not a precise orbital mechanics calculation." The capped fanout of 10 neighbors is a design parameter that significantly affects the comparison: at cap = 10, the sectorized mesh monitors only 3.2% of sector peers (Table IV). Whether this provides adequate conjunction screening is an open question that the paper cannot answer without orbital mechanics coupling. The comparison between hierarchical ($\eta \approx 46\%$) and sectorized mesh ($\eta \approx 65\%$) is therefore comparing architectures at potentially different levels of coordination capability.

**Statistical reporting.** The bootstrap confidence intervals are mentioned (Section III-D) but rarely reported in results tables. Table VII reports "SD < 0.001%" but individual table entries show no uncertainty. For the AoI results (Table VI), bootstrap CIs are mentioned once ([438, 444] s) but not systematically provided. Given the near-deterministic nature of the model, this is understandable but should be stated more prominently—the engineering uncertainty is dominated by model assumptions (γ, message sizes, reporting rates), not stochastic variability.

---

## 3. Validity & Logic

**Rating: 3 (Adequate)**

The internal consistency of the results is strong. The analytical cross-checks match DES outputs to within stated tolerances, and the traffic accounting is meticulously documented. The joint independence verification (Section IV-D, Table VIII) is logically sound and the explanation (link losses occur before coordinator ingress) is convincing.

However, several logical issues deserve scrutiny:

**Circular validation concern.** Many of the DES results reproduce analytical predictions with near-perfect agreement (Table VII: Δ < 0.1%; Table VI: 441 s vs. 440 s analytical; Table VIII: exception validation within 1%). This raises the question of what the DES is actually testing beyond the analytical model. The authors address this partially in Section IV-D (joint interactions), but the paper would benefit from explicitly identifying which results *cannot* be obtained analytically and which are pure verification. As written, approximately 80% of the quantitative results appear to be analytical calculations verified by simulation rather than simulation discoveries.

**Extrapolation claims.** The paper title says "Large Autonomous Space Swarms" and the abstract mentions 10³–10⁵ nodes, but the $O(1)$ overhead result is a mathematical property of the fixed-depth hierarchy, not an empirical finding. The DES validates this at 10 fleet sizes, but since overhead is analytically constant, the validation adds limited information. The more interesting question—whether the message-layer abstraction remains valid at 10⁵ nodes when MAC contention, link scheduling, and spatial correlations are included—is explicitly deferred to future work.

**Coordinator capacity interpretation.** The 21–50 kbps range (Section IV-A) spans a factor of 2.4×, which is large for a "sizing" result. The paper correctly identifies that the range depends on scheduling assumptions, but the headline presentation of "21–50 kbps" may give a false impression of precision. The TDMA vignette (24 kbps at 500 km) is helpful but assumes co-orbital nodes with <15 m/s relative velocity—a specific orbital configuration, not a general result.

**Limitations acknowledgment.** The paper is commendably honest about limitations (Section V-B, Table V), but some limitations are more consequential than acknowledged. The absence of priority queueing is noted as deserving "investigation," but for a system where collision avoidance alerts (128 B, time-critical) share a channel with routine status reports (256 B), this is a significant gap. The i.i.d. failure model is acknowledged as neglecting correlated failures, but solar particle events can simultaneously disable multiple coordinators in an orbital region—a failure mode that could invalidate the hierarchical architecture's fault tolerance claims.

---

## 4. Clarity & Structure

**Rating: 4 (Good)**

The paper is generally well-written and logically organized. The roadmap at the beginning of Section IV is helpful, and the consistent use of traffic accounting tables (Tables II, III, V, VI) supports reproducibility. The design equations summary (Section V-C) is a valuable practitioner-oriented addition.

The paper is, however, excessively long for a journal article. At approximately 12,000 words of body text plus extensive tables, it exceeds typical T-AES length guidelines. Several sections could be condensed:

- The sectorized mesh model (Section III-B.4) occupies nearly two full columns but contributes a single comparison point ($1.4–1.5\times$ overhead ratio). The neighbor-cap sensitivity (Table IV) could be moved to supplementary material.
- The overhead verification section (IV-F) largely confirms analytical predictions and could be shortened to a single paragraph noting agreement.
- The duty cycle derivations (Section IV-H.2) are detailed but the Pareto frontier result (24–48 h is favorable) is intuitive.

The abstract is accurate but dense—it attempts to summarize five distinct contributions in a single paragraph. The key message (hierarchical coordination is characterized, with specific sizing equations) could be communicated more clearly.

Figures are referenced but not viewable in this review (provided as PDF filenames). Based on captions, they appear appropriate and well-described. Table formatting is consistent and professional.

One structural concern: the paper oscillates between presenting the DES as a novel simulation tool and as a verification instrument for known analytical results. The introduction frames it as addressing an "underexplored" gap (Section I-A), but the results repeatedly show analytical tractability. A clearer positioning—either as a simulation methodology paper or as a design handbook contribution—would strengthen the narrative.

---

## 5. Ethical Compliance

**Rating: 4 (Good)**

The paper includes an appropriate acknowledgment of AI-assisted ideation (Acknowledgment section), specifying the tools used (Claude 4.6, Gemini 3 Pro, GPT-5.2) and their role (exploratory ideation, not validated in the current study). The companion methodology paper is cited. This level of disclosure meets current IEEE guidelines.

The anonymous authorship ("Project Dyson Research Team") with a note that individual names will be provided for final publication is unusual but not unprecedented for team-based submissions. IEEE policy requires individual author identification; this should be resolved before acceptance.

Data availability is addressed with a specific repository URL and version tag, supporting reproducibility. The simulation parameters are thoroughly documented.

One minor concern: the reference to "Claude 4.6," "Gemini 3 Pro," and "GPT-5.2" appears to reference future model versions that do not exist as of the review date. If these are actual tools used, the version numbers should be verified; if they are placeholder names, this should be corrected.

---

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is appropriate for IEEE T-AES in topic (autonomous spacecraft coordination) but sits at the boundary between a systems engineering trade study and a research contribution. The referencing is generally thorough, with 50+ citations spanning constellation operations, swarm robotics, queueing theory, distributed systems, and AoI theory.

Several referencing gaps:

- **DTN/space networking literature**: The paper cites Cerf et al. (RFC 4838) and BPv7 but omits significant work on contact graph routing (CGR) for scheduled space networks, which is directly relevant to the TDMA scheduling discussion. Fraire et al.'s work on CGR for LEO constellations should be cited.
- **Satellite constellation coordination**: Recent work on autonomous collision avoidance for mega-constellations (e.g., Merz et al., 2023 on automated conjunction assessment) is missing.
- **Hierarchical multi-agent systems**: The paper cites Olfati-Saber and Ren/Beard for consensus but omits hierarchical decomposition literature from control theory (e.g., Šiljak's work on decentralized control, or more recent hierarchical MARL approaches).
- **AoI in networked control**: The AoI citations (Kaul, Yates, Kadota) are appropriate but the paper should also cite work on AoI-optimal scheduling under energy constraints, which is directly relevant to the exception-based telemetry trade-off.

Some references are non-archival (SpaceX website, Amazon website, DARPA program pages, DoD fact sheets). While these are appropriate for context, the paper relies on them for specific claims (e.g., "approximately 7,000 active satellites") that may not be verifiable at review time. The NRL reference [22] is described as a "magazine article, non-peer-reviewed"—this should be replaced with a peer-reviewed source if available.

---

## Major Issues

1. **Limited novelty beyond analytical verification.** The DES reproduces analytical predictions with <0.1% error for most metrics. The joint independence result (Section IV-D) is the strongest DES-specific contribution but is intuitively expected. The paper needs to more clearly articulate what the DES reveals that analytical models cannot, or reposition as a validated design handbook rather than a research contribution.

2. **MAC-layer abstraction undermines quantitative claims.** The linear $1/\gamma$ scaling assumption is valid only for scheduled access. The paper's quantitative results (coordinator capacity thresholds, overhead percentages, channel utilization limits) all depend on this assumption, yet the paper acknowledges that "MAC contention could introduce scale-dependent effects beyond the γ efficiency factor" (Section V-B). Without at least a single-cluster packet-level validation, the absolute numbers should be presented with wider uncertainty bounds.

3. **Unfair baseline comparison.** The visual and tabular presentation emphasizes the $c = 1$ centralized baseline and $O(N^2)$ mesh bound, both acknowledged as unrealistic. The realistic centralized baseline ($c = N/k_c$) matches hierarchical performance up to $N \approx 10^6$, which significantly weakens the paper's implicit argument for hierarchical coordination. The paper should lead with the realistic comparison and relegate the extreme bounds to supplementary analysis.

4. **Missing operational validation of coordination capability equivalence.** The sectorized mesh monitors 3.2% of sector peers (cap = 10) while the hierarchical architecture provides full cluster state for $O(k_c)$ peers. These are fundamentally different levels of situational awareness, yet the overhead comparison treats them as equivalent coordination architectures. The paper needs either (a) a formal definition of "coordination capability" that enables fair comparison, or (b) explicit acknowledgment that the overhead comparison is between architectures providing different service levels.

5. **Absence of spatial/orbital modeling.** The paper studies "space swarms" but contains no orbital mechanics beyond the TDMA vignette's propagation delay calculation. Cluster membership, inter-cluster handoffs, and conjunction screening all depend on orbital geometry (relative motion, Earth occlusion, contact windows), none of which is modeled. The title and framing promise space-specific insights, but the results are largely applicable to any hierarchical communication network.

---

## Minor Issues

1. **Section III-B.1, Eq. (2):** The $M/D/1$ waiting time formula is stated without noting it applies only to the waiting time in queue (not total sojourn time). Clarify.

2. **Table I:** The "Representative System" column for $c = 1000$ ("Hyperscale data center") is misleading—no constellation operator would deploy 1000 dedicated processing servers for message routing at 1000 msg/s each. The total throughput ($10^6$ msg/s) is trivially achievable on a single modern server.

3. **Section III-B.3, convergence rounds:** The formula $R_{\text{conv}} = \max(\lceil\log_2 N\rceil, \lceil N/(bf)\rceil)$ conflates two different bottlenecks (epidemic spread time vs. throughput limit) without formal justification. The max operation assumes these are independent constraints, which should be stated.

4. **Section III-B.4:** The footnote explaining why sectorized mesh heartbeats (32 B) differ from hierarchical heartbeats (64 B) is helpful but should be in the main text, as it affects the overhead comparison.

5. **Table VI:** The "Max AoI" column for periodic baseline shows 10.0 s, but with $T_c = 10$ s and uniform phase offsets, the maximum AoI should approach $2 \times T_c = 20$ s (a report generated just after the previous cycle's report, sampled just before the next). Clarify the sampling methodology.

6. **Section IV-A, Eq. (8):** The Chernoff bound uses $\alpha$ for overprovisioning factor, conflicting with $\alpha$ used earlier (Section III-B.2) for aggregation ratio. Use distinct symbols.

7. **Section IV-B, Eq. (10):** The position uncertainty growth model $\dot{\sigma} = 0.5$ m/s is described as "along-track" but the cited value is high for well-tracked LEO objects (typical values are 0.01–0.1 m/s for objects with recent tracking). Clarify whether this represents untracked drift or tracking-limited uncertainty.

8. **Table X, footnote c:** References footnote "c" but the table uses superscript "b" for the relevant note. Check cross-referencing.

9. **Section III-F:** "the effective utilization $\eta_{\text{total}} / \gamma \approx 74$–$84\%$ for $\gamma \in [0.7, 0.9]$"—this should be $(\eta + 0.205) / \gamma$, and the arithmetic should be verified: $(0.46 + 0.205)/0.7 = 0.95$, not 0.84.

10. **Acknowledgment section:** References to "Claude 4.6," "Gemini 3 Pro," and "GPT-5.2" appear to be future/fictional model versions. Verify and correct.

11. **Data Availability:** The repository tag "paper-02-v-ag" suggests this is version AG of paper 02 in a series. Clarify the versioning scheme for readers.

---

## Overall Recommendation

**Major Revision**

This paper addresses a relevant problem and presents a thorough parametric analysis with commendable transparency about assumptions and limitations. The traffic accounting methodology, analytical cross-checks, and design equations summary are valuable contributions to the spacecraft swarm design community. However, the paper suffers from a novelty gap: most quantitative results are analytically predictable, and the DES serves primarily as a verification tool rather than a discovery instrument. The baseline comparisons are constructed to favor the hierarchical architecture (extreme bounds rather than realistic alternatives), and the absence of orbital mechanics modeling limits the space-specific applicability. The MAC-layer abstraction introduces unquantified uncertainty in all absolute bandwidth figures. A major revision should (1) strengthen the DES-specific contributions by identifying results that genuinely require simulation, (2) lead with the realistic centralized baseline comparison, (3) include at least a bounding analysis of MAC contention effects, and (4) either add minimal orbital geometry modeling or adjust the title and framing to reflect the communication-layer scope.

---

## Constructive Suggestions

1. **Reframe the contribution around the joint interaction result and workload envelope.** The strongest DES-specific contributions are (a) the joint independence verification (Section IV-D) and (b) the workload decomposition showing commands dominate overhead. Restructure the paper to lead with these, positioning the analytical results as supporting context rather than primary findings. Consider adding 2–3 additional joint interaction tests (e.g., cluster size × link loss, duty cycle × failure rate) to strengthen the case that the DES provides value beyond single-factor analysis.

2. **Conduct a single-cluster packet-level validation.** Even a simplified NS-3 or OMNeT++ simulation of one 100-node cluster with TDMA scheduling would ground the γ assumption and provide a concrete MAC efficiency value. This would transform the paper from a message-layer study with an unvalidated physical-layer correction factor into a multi-layer analysis with quantified abstraction error.

3. **Add deterministic Earth-occlusion link modeling.** Replace or supplement the GE channel model with a simple geometric occlusion model (two-body orbital mechanics, Earth shadow). This would (a) add space-specific content, (b) test whether deterministic periodic outages alter the topology ranking, and (c) address the most consequential item in the "Unresolved Questions" list (Section V-A, item 4) within the current study.

4. **Restructure the baseline comparison.** Present the realistic centralized baseline ($c = N/k_c$) as the primary comparator in all figures and tables. Move the $c = 1$ bound and global-state mesh to an appendix or supplementary section. This would make the paper's actual finding—that the hierarchical advantage is fault tolerance and spectrum independence, not processing scalability—the central narrative rather than a late-arriving qualification.

5. **Tighten the paper by 30%.** The current length (~25 pages including references) exceeds typical T-AES limits. Candidates for condensation: sectorized mesh details (Section III-B.4, ~2 pages → 1 page), overhead verification (Section IV-F, ~2 pages → 0.5 pages), and duty cycle derivations (Section IV-H.2, ~1 page → 0.5 pages). The design equations summary (Section V-C) should be preserved as a high-value practitioner resource.