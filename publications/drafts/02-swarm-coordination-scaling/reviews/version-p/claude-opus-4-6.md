---
paper: "02-swarm-coordination-scaling"
version: "p"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-24"
recommendation: "Major Revision"
---



# Peer Review: "Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study"

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a genuine gap in the literature: the systematic quantitative comparison of coordination architectures for autonomous space swarms in the $10^3$–$10^5$ node regime. The authors correctly identify that swarm robotics literature typically operates at 10–100 agents, constellation management at <15,000 nodes, and that the intermediate regime is underexplored. The motivation from mega-constellation growth (Starlink, Kuiper) is timely and well-articulated.

However, the novelty of the core finding is limited. The authors themselves acknowledge repeatedly (Section IV-D, lines around Eq. 5) that the $O(1)$ overhead scaling of the hierarchical architecture is "a direct mathematical consequence of the hierarchical message structure—not a surprising emergent property." The DES contribution is then reduced to (1) quantifying the protocol coefficient at 20.66% and (2) confirming queue stability. While quantification has value, the result that a well-provisioned hierarchical system with $\rho_c = 0.05$ at the cluster coordinator does not exhibit queueing instabilities is unsurprising. The paper would benefit from a stronger articulation of what is genuinely non-obvious in the results—for instance, the coordinator bandwidth threshold analysis (Section IV-G) and the TDMA comparison (Section IV-I) provide more actionable engineering insights than the central overhead-scaling result.

The sectorized mesh addition is a welcome intermediate comparator, but its parameterization (capped fanout at 10 neighbors, sector size $\sqrt{N}$) is somewhat arbitrary and not derived from orbital mechanics or conjunction screening requirements. The claimed $2.2\times$ overhead ratio relative to hierarchical is interesting but its practical significance depends on whether the sectorized mesh provides sufficient coordination quality—a question the authors explicitly defer.

## 2. Methodological Soundness

**Rating: 2 (Needs Improvement)**

The DES framework has several methodological concerns that undermine confidence in the quantitative results:

**Abstraction level vs. claims.** The simulation operates at the message-passing layer (Table II), abstracting away MAC scheduling, link acquisition, pointing, Doppler, correlated failures, priority queueing, and half-duplex constraints. The authors acknowledge this (Section V-E) but then make quantitative claims (e.g., "$C_{\text{coord}} \geq 50$ kbps for zero-drop operation," "$\eta = 20.66\% \pm 0.01\%$") with a precision that the abstraction level cannot support. The four-significant-figure overhead reporting is particularly misleading: the model-form uncertainty from abstracted effects (estimated by the authors themselves at 10–30% for MAC alone) dwarfs the reported MC variance by four orders of magnitude. Reporting $\eta = 20.66\% \pm 0.01\%$ when the true uncertainty band is arguably $\eta \approx 21\% \pm 5\%$ (accounting for MAC, transport headers, priority queueing) creates a false impression of precision.

**Near-deterministic model and MC framework.** The authors repeatedly note that MC standard deviation is $<0.001\%$, which they attribute to the "near-deterministic message model." This raises a fundamental question: if the model is near-deterministic, what is the DES actually contributing beyond an analytical calculation? The only stochastic element affecting overhead is the node failure process (2%/year), which perturbs an insignificant fraction of nodes per cycle. The 30 MC replications appear to serve primarily as a code-correctness check rather than as a meaningful uncertainty quantification. The authors partially acknowledge this but should be more forthright: the DES is essentially computing an analytical formula with minor stochastic perturbations, and the "simulation study" framing overstates the computational contribution.

**Coordinator queueing model.** The cluster coordinator is modeled as an $M/D/1$ queue with $\rho_c = 0.05$ at $k_c = 100$. At this utilization, the queue is trivially stable and the Pollaczek-Khinchine waiting time is negligible. The claim that the DES "confirms the absence of queueing-induced nonlinearities" is therefore a confirmation of a trivially expected result. A more interesting analysis would stress the coordinator queue to higher utilization (e.g., by increasing $r$ or $k_c$) to find the actual instability threshold.

**Validation.** The validation against the Pollaczek-Khinchine formula (Section III-A, "to within 2%") is mentioned only in passing for $N = 100$ at low utilization. This is a weak validation point. No validation is provided for the hierarchical or sectorized mesh topologies against independent analytical results or external simulators. The gossip convergence validation against Demers et al. is mentioned for $N \leq 1,000$ only.

**Bernoulli link model.** The i.i.d. Bernoulli link loss model (Section IV-F) is acknowledged as a simplification, but it fundamentally misrepresents LEO link availability, which is dominated by deterministic Earth occlusion (predictable, correlated, periodic) rather than random losses. The retransmission analysis built on this model may not transfer to realistic link conditions.

## 3. Validity & Logic

**Rating: 3 (Adequate)**

The logical structure of the paper is generally sound, and the authors are commendably transparent about limitations. Several specific validity concerns merit attention:

**Circular reasoning in the central result.** The paper's central claim—that hierarchical overhead is $O(1)$—follows directly from the model construction: $O(N)$ messages divided by $O(N)$ bandwidth yields $O(1)$. The DES then confirms this at 10 fleet sizes. But the DES uses the same message model that produces the analytical prediction, so the "confirmation" is tautological within the message-passing abstraction. The authors acknowledge this (Section IV-D: "not a surprising emergent property") but the abstract and conclusion still frame the $O(1)$ result as a primary finding rather than a model property. The genuine DES contribution—queue stability confirmation and protocol coefficient quantification—should be foregrounded more honestly.

**Sectorized mesh overhead interpretation.** The sectorized mesh overhead of $\sim$45% is reported as "$2.2\times$ the hierarchical overhead," but this comparison conflates different coordination capabilities. The sectorized mesh provides local trajectory awareness for $O(\sqrt{N})$ neighbors (useful for conjunction screening), while the hierarchical architecture provides only aggregated fleet summaries beyond the cluster. Whether the hierarchical architecture's lower overhead comes at the cost of reduced coordination quality for cross-cluster conjunctions is not assessed. The $2.2\times$ ratio is therefore not a clean apples-to-apples comparison.

**Exception-based telemetry.** The validation (Table VII) confirms that the Bernoulli filtering mechanism works as expected—which is trivially guaranteed by the law of large numbers for $N \times T/T_c \gg 1$ independent trials. The authors acknowledge this. The more important question—what $p_{\text{exc}}$ values are realistic given orbital perturbation spectra—is deferred. Without this coupling, the exception-based results are parameterically valid but operationally ungrounded.

**Latency budget (Section IV-B).** The decomposition showing $\sim$500 ms dominated by regional coordinator queueing is informative, but the regional coordinator model ($\mu_r = 500$ msg/s) is not well justified. Why 500 msg/s? Is this a processing constraint, a communication constraint, or arbitrary? The sensitivity to $n_r$ and $\mu_r$ is acknowledged as "deferred to future work" but these are first-order design variables that significantly affect the latency results.

## 4. Clarity & Structure

**Rating: 3 (Adequate)**

The paper is well-organized with a logical flow from framework description through results to discussion. The extensive use of tables (12 tables) and figures (9 figures) supports the quantitative narrative. However, the paper suffers from several clarity issues:

**Length and redundancy.** At approximately 12,000 words of body text plus extensive tables, the paper is significantly longer than typical IEEE T-AES articles (typically 6,000–8,000 words). Much of this length comes from defensive qualifications and repeated caveats about the reference baselines, the abstraction scope, and the near-deterministic nature of the model. While transparency is valued, the same caveats appear in the abstract, introduction (Section I-C), results (Section IV-D), and limitations (Section V-E), creating substantial redundancy. A single, thorough limitations section would suffice.

**Abstract overload.** The abstract attempts to convey too many quantitative results (overhead percentages, cluster sizes, duty cycles, exception probabilities, coordinator bandwidth thresholds, MAC adjustments, retransmission parameters, link availability thresholds). A more focused abstract highlighting 2–3 key results would be more effective. The current abstract reads more like an executive summary than a concise problem-method-result statement.

**Notation consistency.** The paper uses $\eta$ for protocol overhead, $\eta_{\text{total}}$ for total utilization, $\eta_{\text{sector}}$ for sectorized mesh overhead, and $O_{\text{protocol}}$ (Table I) apparently synonymously with $\eta$. The relationship between these is clarified in Section III-F but could be streamlined. Similarly, $C$ (processing capacity in msg/s), $C_{\text{node}}$ (link bandwidth in kbps), and $C_{\text{coord}}$ (coordinator link capacity in kbps) use the same letter for dimensionally different quantities.

**Figure quality.** All figures reference PDF files that are not available for review. The captions are detailed and informative, but without seeing the actual figures, it is impossible to assess their effectiveness. The authors should ensure that Fig. 1 (architecture diagram) clearly shows the four-level hierarchy with message flow directions and aggregation ratios, and that Fig. 2 (overhead vs. nodes) uses appropriate axis scaling to show the constant hierarchical overhead against the diverging baselines.

## 5. Ethical Compliance

**Rating: 4 (Good)**

The paper includes an appropriate acknowledgment of AI-assisted ideation (Claude 4.6, Gemini 3 Pro, GPT-5.2) in the Acknowledgment section, with a clear statement that the AI-generated concepts are "not validated in the current study." This is a responsible disclosure. The reference to a companion methodology paper [43] provides traceability.

The anonymous authorship ("Project Dyson Research Team") with a note that individual names will be provided for final publication is unusual but not unprecedented for IEEE submissions. The data availability statement with a GitHub repository link (pending commit hash) supports reproducibility, though the repository should be populated before acceptance.

One concern: the paper references future AI model versions (Claude 4.6, GPT-5.2) that do not exist as of the review date, suggesting either speculative attribution or a manuscript from a future timeline. This should be clarified or corrected.

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is appropriate for IEEE T-AES in scope, addressing autonomous spacecraft coordination at scale. The reference list (48 citations) covers the relevant literature adequately, including distributed systems theory (Lynch, Lamport, Ongaro), queueing theory (Kleinrock), swarm robotics (Brambilla, Dorigo), constellation operations (Handley, del Portillo), and gossip protocols (Demers).

Several gaps in the referencing deserve attention. The paper does not cite recent work on distributed satellite autonomy from the small-sat community, particularly the growing literature on autonomous constellation management using onboard processing (e.g., Nag et al., 2018, "Scheduling algorithms for rapid imaging using agile CubeSat constellations"). The mean-field game references (Lasry, Huang) are mentioned but not connected to the analysis—if MFG is relevant, the connection should be developed; if not, the citations are gratuitous. The CCSDS Proximity-1 reference [35] is cited for physical-layer effects but the more relevant CCSDS 732.1-B (AOS Space Data Link Protocol) for ISL scheduling is not cited.

Several references are non-archival (SpaceX website, Amazon website, DARPA program pages, DoD fact sheets), which is acceptable for context but should not be relied upon for technical claims. The NRL swarm reference [22] is explicitly noted as "non-peer-reviewed," which is appreciated.

---

## Major Issues

1. **False precision in the central result.** The reported $\eta = 20.66\% \pm 0.01\%$ implies four-significant-figure precision that the message-passing abstraction cannot support. The model-form uncertainty (MAC scheduling, transport headers, correlated failures, priority queueing) is estimated by the authors at 10–30%, dwarfing the MC variance. The paper should report $\eta \approx 21\%$ with explicit model-form uncertainty bounds (e.g., $\eta \in [18\%, 27\%]$ accounting for MAC efficiency $\gamma \in [0.7, 0.9]$ and transport overhead of 10–20%). The current presentation conflates sampling precision with engineering accuracy.

2. **Tautological DES contribution.** The $O(1)$ scaling result is a mathematical property of the hierarchical message model, not an empirical finding from the DES. The paper should restructure its claims to clearly separate the analytical result ($O(1)$ scaling is guaranteed by the architecture) from the DES contributions (protocol coefficient quantification, queue stability confirmation, coordinator bandwidth thresholds). Currently, the framing suggests the DES "discovered" constant scaling, which is misleading.

3. **Absence of coordination quality metrics.** The paper measures only bandwidth overhead, latency, and delivery rate—all communication-layer metrics. No coordination quality metric is defined or measured: How well does the swarm actually coordinate? What is the collision avoidance miss rate? What is the state estimation error at coordinators? Without such metrics, the paper cannot claim that the hierarchical architecture provides adequate coordination, only that it uses a certain amount of bandwidth. This is a fundamental gap for a paper claiming to characterize "coordination scaling."

4. **Inadequate validation.** The DES is validated only against the $M/D/1$ Pollaczek-Khinchine formula at $N = 100$ (trivially low scale) and gossip convergence bounds at $N \leq 1,000$. No validation is provided for the hierarchical topology, the sectorized mesh, or any configuration at $N > 1,000$. For a paper whose primary contribution is simulation results across $10^3$–$10^5$ nodes, this validation is insufficient. At minimum, the hierarchical overhead should be validated against the closed-form expression (Eq. 4) at all tested scales, and the sectorized mesh against its analytical prediction (Eq. 6).

5. **Unrealistic link model undermines robustness claims.** The Bernoulli i.i.d. link loss model fundamentally misrepresents LEO link availability, which is dominated by deterministic, correlated Earth occlusion. The retransmission analysis (Section IV-F) and the claim that "robust coordination extends to $p_{\text{link}} \geq 0.5$" may not hold under realistic occlusion-driven outage patterns, where multiple links fail simultaneously for predictable durations. This is acknowledged in the limitations but the robustness claims in the abstract and conclusion are not adequately qualified.

---

## Minor Issues

1. **Abstract, line 1:** "full-participation enumeration" is jargon that should be defined or replaced with "all $N$ nodes active in every coordination cycle."

2. **Section I-A, paragraph 1:** "approximately 7,000 active satellites (as of mid-2024)" — the paper's acknowledgment references "February 2026." The Starlink count should be updated for consistency.

3. **Eq. 2:** The $M/D/1$ waiting time formula $W_q = \rho / [2\mu(1-\rho)]$ is correct but should cite Kleinrock more specifically (Chapter 3, Eq. 3.35 or equivalent).

4. **Section III-B-2, Eq. 4:** The message count $M_{\text{total}} = N + N/k_c + N/(k_c \cdot k_r)$ counts only uplink messages. The text notes this but the equation should be labeled accordingly (e.g., $M_{\text{up}}$).

5. **Table III:** The "Collision avoidance rate" footnote (a) explains the $10^{-4}$/node/s rate well, but the sensitivity analysis varying this rate from $10^{-5}$ to $10^{-3}$ (Section III-E, last paragraph) should be presented in a table or figure rather than described in prose.

6. **Section III-F:** The statement "Slotted ALOHA ($\sim$36%)" should cite the original Abramson or Roberts result for this throughput limit.

7. **Table V (cluster size):** The latency values show discrete jumps (508 → 340 ms) rather than smooth variation. The text explains this as burst-driven regional queueing, but the mechanism deserves a more formal treatment—why does the jump occur between $k_c = 75$ and $k_c = 100$ specifically?

8. **Section IV-C (duty cycle):** Table VI reports "Handoff Success" rates (95.0%–99.9%) but the derivation of these values is not shown. Are they from the DES or analytical? The failure model for handoffs should be specified.

9. **Section IV-G:** The coordinator bandwidth stress test uses $N = 10^4$ only. Given that the paper claims results across $10^3$–$10^5$, the bandwidth analysis should be repeated at $N = 10^5$ to confirm scale-independence.

10. **Eq. 10 (power overhead):** $\Delta P_{\text{avg}} = 15\text{ W} / 100 = 0.15\text{ W}$ assumes uniform duty cycle distribution. With 24-hour cycles and 100 nodes, each node serves $\sim$3.65 days/year as coordinator, not exactly 1%. The calculation should use the exact duty fraction.

11. **Section V-B:** The comparison with terrestrial systems (cellular, BGP, ATC) is interesting but superficial. A more substantive comparison with BGP's hierarchical aggregation (which faces similar scalability challenges with route table growth) would strengthen the discussion.

12. **Bibliography:** References [1], [3], [20], [21], [22], [36] are non-archival web sources. While acceptable for context, the paper should minimize reliance on these for technical claims.

13. **Data Availability:** The commit hash is listed as "[PENDING]"—this must be resolved before publication.

---

## Overall Recommendation

**Major Revision**

The paper addresses a relevant problem—coordination architecture scaling for large autonomous space swarms—and provides a well-structured simulation framework with commendable transparency about limitations. However, the central contribution is undermined by three issues: (1) the primary result ($O(1)$ overhead scaling) is a mathematical tautology of the model rather than an empirical finding, yet is presented as the main DES contribution; (2) the false precision of the reported overhead ($20.66\% \pm 0.01\%$) misrepresents the actual engineering uncertainty, which is dominated by model-form errors orders of magnitude larger than the MC variance; and (3) the absence of any coordination quality metric means the paper characterizes communication cost without establishing that the communication is sufficient for its purpose. The coordinator bandwidth analysis, TDMA comparison, and sectorized mesh addition are genuinely useful engineering contributions that deserve to be foregrounded over the overhead-scaling result. A major revision should restructure the claims around these actionable findings, introduce at least one coordination quality metric (e.g., state estimation staleness, conjunction detection latency), provide adequate DES validation at scale, and replace the false-precision reporting with honest engineering uncertainty bounds.

---

## Constructive Suggestions

1. **Introduce a coordination quality metric.** Define and measure at least one metric that captures whether the coordination is *effective*, not just how much bandwidth it consumes. Candidates include: coordinator state estimation error (how stale is the coordinator's knowledge of member positions?), conjunction detection latency (time from conjunction geometry arising to alert generation), or coordination completeness (fraction of cross-cluster conjunctions detected within a decision window). This would transform the paper from a communication cost study into a coordination effectiveness study.

2. **Restructure claims around actionable engineering results.** The coordinator bandwidth threshold ($C_{\text{coord}} \geq 50$ kbps for zero drops, $\geq 59$ kbps MAC-adjusted), the TDMA vs. random-phase comparison, and the retransmission robustness envelope ($p_{\text{link}} \geq 0.5$ with $M_r = 2$) are the most useful results for system designers. Elevate these to primary contributions and demote the $O(1)$ scaling confirmation (which is analytically obvious) to a supporting result.

3. **Replace false precision with engineering uncertainty bands.** Report overhead as $\eta \approx 21\%$ (message-layer) with explicit bounds: $\eta_{\text{eff}} \in [23\%, 30\%]$ at the MAC layer for $\gamma \in [0.7, 0.9]$, and $\eta_{\text{eff}} \in [25\%, 36\%]$ including estimated transport overhead. This honest uncertainty reporting would be more useful to designers than four-significant-figure MC statistics that reflect only sampling precision.

4. **Implement a minimal TDMA scheduling model within the DES.** Rather than treating TDMA analytically (Section IV-I), implement $k_c$ time slots with guard intervals within each $T_c$ cycle. This would (a) provide a DES-validated TDMA result rather than an analytical estimate, (b) test whether slot synchronization introduces scale-dependent effects, and (c) address the most important physical-layer gap identified in the limitations.

5. **Validate the DES against its own analytical predictions at all scales.** Compute the analytical overhead from Eq. 4 and the traffic accounting table (Table IV) for each of the 10 fleet sizes, and show that the DES matches to within a specified tolerance. This is a minimal validation that should be straightforward given the near-deterministic model, and would substantially strengthen confidence in the implementation.