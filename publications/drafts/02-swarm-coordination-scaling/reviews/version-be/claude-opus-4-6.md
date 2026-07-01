---
paper: "02-swarm-coordination-scaling"
version: "be"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-27"
recommendation: "Major Revision"
---

# Peer Review: "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms"

## 1. Significance & Novelty
**Rating: 3 (Adequate)**

The paper addresses a genuine gap: there is no published, unified set of closed-form sizing relationships for hierarchical coordination architectures spanning $10^3$–$10^5$ autonomous spacecraft nodes with byte-level traffic accounting. The authors correctly identify that swarm robotics literature operates at 10–100 agents, constellation management at ~$10^4$, and networking literature treats routing but not coordination protocol sizing. Assembling queueing, Markov-chain, and AoI results into a "practitioner toolkit" has practical value.

However, the novelty is primarily one of *assembly and parameterization* rather than fundamental methodological advance. The individual analytical components—M/D/1 queueing, Gilbert-Elliott channel models, geometric AoI distributions, Raft consensus—are well-established. The paper's central finding that architecture-specific overhead is ~5% while commands dominate at >60% is useful but somewhat unsurprising: in any hierarchical aggregation scheme, the aggregation cost should be small relative to the payload traffic it organizes. The paper would benefit from a clearer articulation of what *surprising* or *counterintuitive* insights emerge from the analysis, beyond confirming that hierarchical aggregation works as expected.

The claimed scale range ($10^3$–$10^5$) is validated only at the message layer with a cycle-aggregated DES that, by the authors' own admission, checks "arithmetic consistency, not physical fidelity." This significantly limits the practical significance claim. A system designer considering a 100,000-node constellation would need the physical-layer validation that is explicitly deferred. The contribution is therefore better characterized as a *message-layer reference model* than as validated design equations.

## 2. Methodological Soundness
**Rating: 3 (Adequate)**

The analytical framework is internally consistent and the individual models are correctly applied. The M/D/1 queueing model for centralized processing, the geometric distribution for exception-based AoI, and the Markov-chain GE recovery derivation are all standard and correctly implemented. The three coordinator ingress models (deadline, token-bucket, TDMA) provide useful bracketing. The TDMA frame derivation (Eq. 7, Section IV-A) with explicit guard-time accounting is well done.

The principal methodological concern is the **circularity of the DES validation**. The DES and closed-form equations operate at the same abstraction level with the same message model; their agreement to <0.1% confirms only that both implement the same arithmetic. The paper acknowledges this (Section III-A), but the framing throughout still implies stronger validation than is warranted. For example, the abstract states "An open-source Monte Carlo tool checks implementation consistency to <0.1%" but the paper's title promises "Design Equations and Parametric Sizing"—implying these equations are ready for engineering use. The gap between message-layer consistency and engineering applicability is substantial.

The **static topology assumption** is a significant methodological limitation for LEO constellations. The authors bound re-association overhead at <0.5% (Section V-B), but this estimate is itself unvalidated and the transient AoI distributions during churn are not modeled. For cross-plane configurations at 550 km (the Starlink regime explicitly referenced), cluster boundary crossings on 45–90 min timescales are frequent enough to matter operationally. The claim that "only 5–15% of nodes near orbital-plane intersections experience churn at any instant" needs substantiation.

The **Monte Carlo configuration** (30 replications) is adequate for mean estimates but may be marginal for the tail statistics (P99 AoI, P95 recovery) that are central to the paper's contributions. The per-run-then-aggregate methodology for tail statistics (Table V footnote) is appropriate, but the paper should report the bootstrap CIs for all tail metrics, not just the AoI P99. The claim of SD < 0.001% for overhead is expected given the deterministic message model and large N; it does not validate the model, only its implementation.

## 3. Validity & Logic
**Rating: 3 (Adequate)**

The logical structure is generally sound, and the authors are commendably transparent about limitations. The distinction between offered overhead ($\eta$) and delivered overhead ($\eta_{\text{delivered}}$), the separation of baseline telemetry (20.5%) from protocol overhead, and the loss/miss taxonomy (Section III-E) all reflect careful thinking. The joint interaction verification (Section IV-D, Table VIII) demonstrating pipeline decoupling under dedicated links is a useful result.

However, several logical issues merit attention:

**The stress-case $\eta \approx 46\%$ framing is problematic.** The paper repeatedly presents this as a key result, but then reveals (Eq. 6, Section IV-A) that per-node unicast commands require 22 cycles to deliver—meaning the 46% is not achievable in a single cycle. The abstract says "the stress-case per-node command bound reaches $\eta \approx 46\%$ (information-demand upper bound, not single-cycle deliverable)" but this caveat is buried in parentheses. A metric that cannot be realized within its own accounting period ($T_c$) is misleading as a "design equation." The event-driven profile ($\eta_E \approx 6\%$) is acknowledged as operationally representative, which raises the question of why the stress-case dominates the paper's presentation.

**The sectorized mesh comparison is structurally unfair**, and while the authors acknowledge this (Table XI, Section IV-G), the paper still draws overhead ratio comparisons (e.g., "1.35–1.95× higher") that are conditioned on unequal functional scope. The hierarchical architecture provides full cluster awareness (100 nodes) while the capped mesh provides awareness of ~10 neighbors. Comparing their overhead ratios without normalizing by functional output is like comparing the fuel efficiency of a sedan and a bus without noting passenger capacity.

**The 1 kbps budget framing creates confusion.** The paper states this represents the "RF-backup regime (<1% of operational time)" but then builds the entire analysis around it. If optical ISLs are available >99% of the time at Gbps rates, the coordinator bottleneck, TDMA requirements, and most of the interesting design tensions vanish (as Table II confirms). The paper should more clearly position itself: is this a contingency-mode analysis, or a general coordination framework? The answer appears to be the former, but the presentation suggests the latter.

## 4. Clarity & Structure
**Rating: 2 (Needs Improvement)**

The paper is **excessively long and dense** for a journal article. At approximately 12,000 words of body text plus 15 tables and 14 figures, it substantially exceeds typical IEEE T-AES length guidelines. The information density is high but the signal-to-noise ratio suffers. Many results are stated multiple times in slightly different forms (e.g., the 46% overhead appears in the abstract, introduction, Section IV-F, Table VII, and the design equations summary).

The **organizational structure** is problematic. The "Results" section (Section IV) contains nine subsections spanning coordinator capacity, AoI, GE recovery, joint interactions, workload profiles, verification, topology comparison, and parameter sensitivity. This is too many disparate topics for a single results section. The paper would benefit from consolidating around 2–3 core contributions with supporting material moved to appendices.

**Notation and terminology** are generally well-defined (Table I), but the paper introduces many ad hoc symbols ($\alpha_{\text{RX}}$, $L_{\text{cmd}}$, $\eta_0$, $p_{\text{eff}}$, $\gamma_{\min}$, $B_{\text{sector}}^{\text{capped}}$) that are not in the notation table. The distinction between $\eta$, $\eta_{\text{total}}$, $\eta_{\text{eff}}$, $\eta_{\text{delivered}}$, $\eta_{\text{sector}}$, $\eta_E$, $\eta_N$, $\eta_S$, and $\eta_{\text{stress}}$ is confusing—there are at least nine variants of the overhead metric.

The **abstract** is overloaded with specific numbers (6%, 46%, 21–25 kbps, 440 s, 4 cycles, 22 cycles, 0.1%) that are difficult to contextualize without reading the paper. A more effective abstract would emphasize the methodology and key insights, with fewer numerical details.

Tables are generally well-constructed, but there are too many of them (15 tables). Several could be consolidated or moved to supplementary material (e.g., Tables III, IV, VI could be merged; Tables IX and X are largely redundant with the text).

## 5. Ethical Compliance
**Rating: 4 (Good)**

The paper includes an appropriate acknowledgment of AI-assisted ideation (Claude 4.6, Gemini 3 Pro, GPT-5.2) in the Acknowledgment section, with a citation to a methodology paper and an explicit statement that the AI contributions "are not validated here." This is transparent and appropriate.

The anonymous authorship ("Project Dyson Research Team") with a note that "Individual author names and affiliations will be provided for final publication per IEEE policy" is acceptable for review but must be resolved before publication. IEEE requires individual author identification for accountability.

The open-source data availability statement with a specific repository tag is commendable and supports reproducibility. The Monte Carlo configuration details (Table V) are sufficient for replication.

One minor concern: the paper references future AI model versions (Claude 4.6, GPT-5.2) that do not exist as of mid-2025, suggesting either speculative naming or a future publication date. This should be clarified.

## 6. Scope & Referencing
**Rating: 3 (Adequate)**

The paper is appropriate for IEEE T-AES in scope, addressing autonomous spacecraft coordination at scale. The reference list (52 citations) covers the relevant domains: constellation operations, swarm robotics, distributed systems, queueing theory, and AoI. Key foundational works are cited (Kleinrock, Lamport, Lynch, Demers et al., Ongaro/Ousterhout).

However, several gaps exist in the referencing:

- **No citation of actual S-band ISL channel measurements** for LEO. The GE model parameters are presented as parametric design curves, which is appropriate, but the paper should cite existing LEO link characterization studies (e.g., from ESA's OPS-SAT or similar missions) to ground the parameter ranges.

- **Missing references on hierarchical satellite network architectures.** The paper does not cite Ekici et al. (2001, IEEE JSAC) on hierarchical LEO satellite networks, or Marchese (2007) on inter-satellite link routing architectures—both directly relevant.

- **The AoI literature** is cited but the application to satellite networks specifically is not connected to recent work by Yin et al. (2023, IEEE TWC) on AoI in LEO satellite networks.

- Several references are non-archival (Amazon website, DARPA program pages, DoD fact sheets). While understandable for program descriptions, the paper relies on these for factual claims about operational scale (e.g., "~250 units" for OFFSET). These should be supplemented with peer-reviewed sources where possible.

- The self-citation [42] to a "multi-model AI deliberation" paper hosted on the project website is not peer-reviewed and should be flagged as such.

---

## Major Issues

1. **The DES validates nothing beyond arithmetic consistency.** The paper's central claim is providing "design equations" for practitioners, but the validation is entirely self-referential. The DES and closed forms share identical assumptions, message models, and abstraction levels. The <0.1% agreement confirms correct implementation, not model validity. The paper needs either (a) a packet-level simulation comparison for at least one configuration, (b) comparison against published operational data from an existing constellation, or (c) a much more prominent and honest framing that these are *unvalidated message-layer models*. Currently, the framing oscillates between these positions.

2. **The stress-case $\eta \approx 46\%$ is not physically realizable within one cycle.** Equation 6 shows that per-node unicast commands require 22 cycles at the assumed PHY rate. This means the headline metric is an accounting abstraction, not an achievable operating point. The paper should either (a) restructure around the event-driven profile ($\eta_E \approx 6\%$) as the primary result, with the stress-case as a bound, or (b) provide the multi-cycle scheduling analysis as a first-class result with its own design equations (e.g., command staleness, priority scheduling under multi-cycle delivery).

3. **The 1 kbps regime analysis has limited practical applicability.** The paper acknowledges this is the RF-backup contingency (<1% of operational time), yet the entire analytical framework is built around it. At ≥10 kbps (Table II), the coordinator bottleneck and TDMA requirements vanish. The paper should either (a) provide equally detailed analysis for the 10 kbps and 100 kbps regimes, or (b) explicitly reframe as a contingency-mode sizing study. The current presentation risks misleading readers about the operational relevance of the results.

4. **The topology comparison lacks equivalent functional scope.** Comparing hierarchical ($\eta \approx 5$–46%) against sectorized mesh ($\eta \approx 65$–67%) without normalizing by the service provided (100% cluster awareness vs. 3.2% local awareness) is not a fair comparison. Table XI helps but is insufficient. The paper needs a metric like "overhead per unit of awareness" or "bits per monitored neighbor" to enable meaningful cross-topology comparison.

5. **Missing sensitivity to orbital dynamics.** The static topology assumption is a significant gap for the claimed scale range. At $N = 10^5$ in LEO, relative motion causes continuous cluster membership changes. The 0.5% re-association overhead bound is asserted without derivation or simulation. The paper should either validate this bound or restrict claims to co-orbital (static) configurations.

---

## Minor Issues

1. **Eq. 2 (M/D/1 waiting time):** The standard Pollaczek-Khinchine formula for M/D/1 is $W_q = \rho/(2\mu_s(1-\rho))$, which is correct, but the paper should note this is the *mean* waiting time and that the variance is $\rho^2/(12\mu_s^2(1-\rho)^2)$ for completeness, given that tail latencies are discussed elsewhere.

2. **Table I:** $\eta_{\text{total}}$ is defined as $\eta + 20.5\%$ baseline, but this additive relationship only holds if both are fractions of the same denominator ($C_{\text{node}} \times T_c$). This should be stated explicitly.

3. **Section III-B-2:** "Four-level tree structure (Fig. 1)" but Eq. 4 shows only three levels (Ground → Regional → Cluster → Node is four levels, but the message count formula Eq. 5 only has three terms). Clarify whether Ground is a level in the message-counting sense.

4. **Section IV-A, half-duplex partitioning:** The statement "Total egress: ~200 ms, fitting within the remaining ~0.8 s with margin" should quantify the margin explicitly (0.8 - 0.2 = 0.6 s, or 75% margin).

5. **Table V:** The collision avoidance rate footnote says "Screening events, not maneuver-triggering" but the text later (Section III-E) says sensitivity from $10^{-5}$ to $10^{-3}$ shows ±1.5 pp impact on $\eta$. This sensitivity result should be in a table or figure, not buried in text.

6. **Eq. 8 ($\gamma$ derivation):** The guard time calculation assumes 500 km cluster diameter. This should be justified—is this consistent with $k_c = 100$ nodes at LEO densities?

7. **Section IV-B:** "P99 AoI exceeds 440 s" at $p_{\text{exc}} = 0.10$. The operational implication (230 m along-track uncertainty) is mentioned but not connected to conjunction assessment requirements. What is the acceptable AoI for conjunction screening? Without this context, the 440 s number is difficult to evaluate.

8. **Table VIII (Joint Interaction):** The "GE + Exc." column shows *fewer* drops than "No Loss" at all capacity levels. This is because exception telemetry reduces offered load. This counterintuitive result deserves more prominent explanation.

9. **Section V-B:** "A 10% coordinator failure inflates neighboring clusters by ~10%, absorbable at $C_{\text{coord}} \geq 28$ kbps." This cascading failure analysis is too brief for such an important operational concern. How many simultaneous coordinator failures can the system absorb?

10. **Figures:** Several figures are referenced but not viewable in the LaTeX source (PDF compilation required). The captions suggest appropriate content, but the review cannot assess figure quality. Figure 8 caption notes the $10^6$-node curve is "analytical extrapolation, not DES-measured"—this should also be noted in any text referencing this figure.

11. **Acknowledgment section:** "Claude 4.6, Gemini 3 Pro, GPT-5.2" appear to be future/fictional model versions. Clarify.

12. **Data Availability:** The repository tag `paper-02-v-be` suggests this is version BE of paper 02. The versioning scheme should be explained or removed for publication.

---

## Overall Recommendation

**Major Revision**

The paper addresses a legitimate gap in the literature and provides a useful collection of parameterized sizing relationships for hierarchical space swarm coordination. The analytical framework is internally consistent, the traffic accounting is thorough, and the open-source commitment supports reproducibility. However, the paper suffers from four significant issues that prevent acceptance in its current form: (1) the validation is entirely self-referential, with the DES confirming only arithmetic consistency at the same abstraction level as the closed forms; (2) the headline stress-case metric ($\eta \approx 46\%$) is not physically realizable within one coordination cycle, undermining the "design equation" framing; (3) the paper is substantially too long and repetitive, with too many overhead metric variants and insufficient focus on 2–3 core contributions; and (4) the topology comparison lacks functional-scope normalization, making cross-architecture conclusions unreliable. A major revision should restructure around the event-driven workload as the primary operating point, include at least one packet-level validation case, reduce length by ~30%, and provide a normalized comparison metric across topologies.

---

## Constructive Suggestions

1. **Add a single-cluster NS-3 validation.** Even a simplified packet-level simulation of one cluster ($k_c = 100$, TDMA, GE channel) would dramatically strengthen the paper. Compare message-layer predictions against packet-level results for overhead, AoI, and recovery time. This is identified as future work but is essential for a "design equations" paper to be credible for practitioners.

2. **Restructure around the event-driven profile as the primary result.** Present $\eta_E \approx 6\%$ as the main operating point, with the stress-case as an explicitly labeled upper bound. Develop the multi-cycle command scheduling (Eq. 6) into a proper design equation with command staleness metrics, rather than treating it as a caveat to the 46% figure.

3. **Introduce a normalized comparison metric.** Define "overhead efficiency" as $\eta / (\text{fraction of fleet monitored})$ or similar. This would show that hierarchical achieves 46%/100% = 0.46 bits-per-monitored-fraction while the capped mesh achieves 65%/3.2% = 20.3—a 44× efficiency advantage. This single metric would replace pages of caveated comparisons.

4. **Reduce paper length by 30%.** Consolidate Tables III/IV/VI into one comprehensive traffic table. Move the sectorized mesh sensitivity analysis (Table VI, Section III-B-4) to an appendix. Eliminate redundant restatements of the 46% result. Target 8–9 pages for the body text.

5. **Validate the static topology bound.** Run a simple orbital propagation (SGP4) for one Starlink-like shell to count cluster boundary crossings per orbit and compute actual re-association overhead. This would either confirm the 0.5% bound or reveal it as an underestimate, and would take minimal additional effort given the existing simulation infrastructure.