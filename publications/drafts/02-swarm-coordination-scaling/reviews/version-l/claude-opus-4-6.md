---
paper: "02-swarm-coordination-scaling"
version: "l"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-24"
recommendation: "Major Revision"
---



# Peer Review: "Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study"

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a genuinely important problem: how coordination architectures scale for autonomous spacecraft swarms in the $10^3$–$10^5$ range, a regime that is indeed under-explored in the literature. The motivation is timely given Starlink's expansion plans and emerging mega-constellation concepts. The systematic comparison across scales using DES, rather than purely analytical methods, has practical value for constellation designers.

However, the novelty is substantially undermined by the nature of the central result. The authors themselves acknowledge repeatedly (Section IV-D, multiple times) that the $O(1)$ overhead scaling of the hierarchical architecture is "a direct mathematical consequence of the hierarchical message structure—not a surprising emergent property." When the primary quantitative finding ($\eta = 20.66\% \pm 0.01\%$ constant across scales) is analytically predictable from the message model, and the DES merely confirms the absence of second-order effects in a simulation that abstracts away most of the physical phenomena that *would* produce such effects (MAC contention, correlated link failures, orbital dynamics, priority queueing), the contribution becomes somewhat circular. The DES cannot find second-order effects that it does not model.

The absence of a sectorized mesh comparator—acknowledged by the authors as the most important future work—significantly limits the paper's practical contribution. Without this intermediate baseline, the paper compares a reasonable architecture against two intentional straw men (single-server centralized and global-state mesh), making the comparative claims less informative than they could be. The exception-based telemetry and coordinator bandwidth analyses add genuine engineering value, but these are relatively straightforward parametric studies rather than methodological innovations.

## 2. Methodological Soundness

**Rating: 2 (Needs Improvement)**

The DES framework, while clearly described, has fundamental limitations that weaken the claimed contributions. The most critical issue is the level of abstraction: by operating at the message-passing layer and abstracting away MAC scheduling, link acquisition, pointing constraints, Doppler effects, orbital mechanics perturbations, correlated failures, and priority queueing (Table II), the simulation removes precisely the phenomena most likely to produce the "scale-dependent second-order effects" whose absence is claimed as a key finding. The claim that "no scale-dependent second-order effects emerge" (abstract, Section IV-D) is therefore an artifact of the model's abstraction level, not a validated physical finding. The authors partially acknowledge this in the limitations section, but the abstract and contributions list present it as a positive result without adequate qualification.

The Monte Carlo framework is appropriately designed (30 replications, bootstrap CIs), but the authors themselves note that the SD < 0.001% reflects the "near-deterministic nature of the message model" (Section III-D, Table V footnote). When the only stochastic component is a 2%/year failure rate that perturbs an "insignificant fraction of nodes during any single coordination cycle," the MC framework is essentially validating code correctness rather than exploring meaningful uncertainty. This is acknowledged but should temper the presentation of "30 MC replications" as a methodological strength.

The Bernoulli link availability model (Section IV-F) is a useful addition but is physically unrealistic for LEO: link outages due to Earth occlusion are deterministic and correlated (affecting all links crossing a geometric shadow simultaneously), not i.i.d. per-message. The retransmission model assumes retries within $T_c = 10$s with only propagation delay penalty, ignoring the possibility that the same geometric obstruction persists across retry attempts. The Poisson arrival assumption for the centralized baseline is well-justified via Palm-Khintchine, and the CV verification ($0.98 \pm 0.03$) is a nice validation detail.

The wall-clock runtime of 0.2–7 seconds per run for $10^3$–$10^5$ nodes raises questions about simulation fidelity. A one-year simulation of $10^5$ nodes completing in 7 seconds implies extremely coarse event modeling—roughly $10^5$ nodes × $3.15 \times 10^6$ cycles/year ÷ 7s ≈ $4.5 \times 10^{9}$ node-cycles per second, which is only feasible if each node-cycle involves minimal computation. This is consistent with the message-passing abstraction but should be discussed more explicitly as a trade-off between scale and fidelity.

## 3. Validity & Logic

**Rating: 3 (Adequate)**

The internal logic of the paper is generally sound, and the authors deserve credit for extensive self-qualification. The "Baseline Interpretation Note" (Section I-C), the explicit acknowledgment that the central result is analytically expected (Section IV-D), and the thorough limitations section (Section V-D) demonstrate intellectual honesty. However, several logical issues deserve attention.

There is a tension between the paper's framing and its actual contribution. The title promises "Characterizing Hierarchical Coordination Scaling," but the characterization is largely confirmatory of known analytical properties. The abstract states the DES "quantifies this constant factor under realistic message sizes and timing"—but the message sizes are assumed parameters (Table III), not derived from realistic spacecraft operations, and the timing model abstracts away the physical-layer effects that make real timing complex. The word "realistic" overstates the fidelity.

The exception-based telemetry validation (Section IV-E, Table VII) is presented as a contribution, but the validation merely confirms that a Bernoulli filter with parameter $p_{\text{exc}}$ reduces message counts by factor $p_{\text{exc}}$—which is, as the authors note, "expected by the law of large numbers." The more interesting question—what $p_{\text{exc}}$ values are achievable with real orbital prediction algorithms, and what coordination quality degradation results—is explicitly deferred. Similarly, the coordinator bandwidth stress test (Section IV-G, Table VIII) provides useful engineering bounds, but the finding that a coordinator receiving 20.48 kbps of inbound traffic needs at least ~25 kbps of link capacity is not surprising.

The comparison framework is logically structured but the asymmetry in modeling depth is problematic. The hierarchical architecture receives detailed parameterization (cluster size, duty cycle, exception-based telemetry, coordinator bandwidth, link availability), while the baselines receive minimal treatment. This asymmetry makes it impossible to determine whether the hierarchical architecture's advantages would persist under equally detailed modeling of alternatives.

Table I (topology comparison) reports availability figures (99.0%, 99.99%, 99.5%) without clearly explaining how these are computed or what failure scenarios they encompass. The centralized baseline's 99.0% availability seems to assume a single ground station with no redundancy, which is unrealistic for any operational system.

## 4. Clarity & Structure

**Rating: 4 (Good)**

The paper is well-organized and clearly written. The progressive disclosure of the simulation framework (Section III), followed by results (Section IV) and discussion (Section V), follows a logical structure. The extensive use of tables for parameter documentation (Tables III–VI) supports reproducibility. The explicit traffic accounting (Table VI) and metric definitions (Section III-G) are commendable practices that many simulation papers neglect.

The paper is, however, excessively long and repetitive. The constant overhead result ($\eta = 20.66\%$) is stated in the abstract, contributions list, Section IV-D (multiple times), Table V, the conclusion, and various intermediate discussions. The qualification that the baselines are "intentional bounds" is repeated at least five times. While some repetition aids clarity, the current level suggests the paper could be shortened by 20–30% without loss of content. The abstract alone is 250+ words and reads more like an executive summary.

The figures are referenced but not provided (as expected for a LaTeX source review). The figure captions are descriptive and informative. Figure 3's caption appropriately flags the $10^6$-node curve as an "analytical extrapolation," which is good practice. The bandwidth breakdown table (Table IV) helpfully distinguishes analytical per-node estimates from fleet-level DES measurements, though the footnotes explaining the discrepancy between ~9% analytical and ~21% DES overhead could be clearer.

One structural concern: the coordinator bandwidth analysis (Section IV-G) and link availability analysis (Section IV-F) feel like they were added iteratively in response to reviewer feedback (the retransmission section explicitly states "In response to reviewer feedback"). While the content is valuable, the integration into the overall narrative could be smoother.

## 5. Ethical Compliance

**Rating: 4 (Good)**

The paper includes an appropriate acknowledgment of AI-assisted ideation (Claude 4.6, Gemini 3 Pro, GPT-5.2) in the Acknowledgment section, with a clear statement that the AI-generated concepts are "not validated in the current study." This is transparent and appropriate. The reference to a companion methodology paper [46] provides additional context.

The data availability statement promises open-source code and datasets, which is commendable, though the commit hash is listed as "[PENDING]." The author attribution ("Project Dyson Research Team" with a note about individual names for final publication) is unusual but acceptable per the stated IEEE policy accommodation.

One minor concern: the paper references future model versions (Claude 4.6, GPT-5.2) that do not exist as of the review date, suggesting either a speculative timeline or a different versioning convention. This should be clarified.

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is appropriate for IEEE T-AES in topic, though the contribution level is borderline as discussed above. The reference list is comprehensive (50 references) and covers the relevant literature in constellation management, swarm robotics, distributed systems, and queueing theory. The inclusion of both foundational works (Lamport, Kleinrock, Demers) and recent developments (Tolstaya GNN, Dorigo 2021 survey) demonstrates good literature awareness.

However, several important gaps exist. The paper does not cite recent work on distributed satellite autonomy frameworks such as the ESA's OPS-SAT experiments or NASA's autonomous operations research. The mean-field game references (Lasry, Huang) are mentioned in the related work but never connected to the methodology—if MFG theory is relevant, it should be discussed in relation to the hierarchical approach; if not, the citations are gratuitous. There is no reference to recent work on LEO constellation collision avoidance coordination (e.g., the Space Safety Coalition's best practices, or recent work on automated conjunction assessment), which is directly relevant to the collision avoidance event rate parameterization.

Several references are non-archival (SpaceX website, Amazon website, DARPA program pages, DoD fact sheets), which is noted but still weakens the scholarly foundation. The NRL reference [22] is explicitly flagged as "non-peer-reviewed," which is appreciated. The self-citation to the companion methodology paper [46] is to a non-peer-reviewed online publication.

---

## Major Issues

1. **Circular validation of the central claim.** The paper's primary finding—constant overhead scaling—is analytically guaranteed by the message model and confirmed by a simulation that abstracts away the physical phenomena most likely to violate it. The claim of "no scale-dependent second-order effects" (abstract, Section IV-D) is unfalsifiable within the current simulation framework because MAC contention, correlated link failures, priority queueing conflicts, and orbital geometry effects are not modeled. Either (a) the claim must be substantially weakened to "no second-order effects *within the message-passing abstraction layer*," or (b) at least one physical-layer effect (e.g., TDMA scheduling within $T_c$) must be added to the DES to provide a meaningful test.

2. **Absence of a realistic decentralized comparator.** The global-state mesh is acknowledged as an "intentional upper bound," and the sectorized mesh is identified as the "most important direction for future work." Without this comparator, the paper cannot support claims about the relative merit of hierarchical coordination versus practical decentralized alternatives. Given that the sectorized mesh analysis in Section V-C is already well-developed analytically ($O(N^{3/2})$ scaling), implementing even a simplified DES version would substantially strengthen the paper.

3. **Exception-based telemetry validation is incomplete.** The bandwidth reduction validation (Table VII) confirms only that a Bernoulli filter works as expected—a trivial result. The coordination quality impact is explicitly deferred, but this is the engineering-critical question. Without any characterization of how stale state estimates affect collision avoidance performance, the exception-based telemetry results cannot be used for system design. At minimum, a simple staleness metric (e.g., mean age of information at the coordinator) should be reported.

4. **Inconsistency between per-node and fleet-level overhead accounting.** Table IV reports analytical per-regular-node overhead of ~9% for the hierarchical architecture, while Table V reports DES-measured fleet-level overhead of ~21%. The footnotes explain this discrepancy (coordinator ingest traffic distributed across fleet budget), but the two numbers measure fundamentally different things. The paper should clearly define a single primary metric and use it consistently, or present both with clear labels throughout.

5. **The $10^6$-node claims are unsupported.** Table I lists the hierarchical scalability limit as "1,000,000+," and Figure 3 includes a $10^6$-node analytical extrapolation, but the DES only covers $10^3$–$10^5$. Extrapolating by an order of magnitude beyond the validated range, especially when the simulation abstracts away scale-dependent physical effects, is not justified. The scalability limit claim should be restricted to the validated range or clearly flagged as a projection.

---

## Minor Issues

1. **Abstract length.** At 250+ words, the abstract exceeds typical IEEE T-AES guidelines (~200 words) and contains excessive detail (specific $p_{\text{exc}}$ values, TDMA efficiency factors). Consider condensing.

2. **Eq. (4) notation.** $M_{\text{total}}$ is used for hierarchical messages but $M_{\text{mesh}}$ for mesh (Eq. 5). Use consistent notation or define both clearly.

3. **Table III footnote (a).** The collision avoidance rate justification ($10^{-4}$/node/s representing screening events) is important but buried in a footnote. Consider promoting to main text.

4. **Section III-F, paragraph 2.** "Transport-layer overhead (headers, acknowledgments, retransmissions) is not included in the reported protocol overhead figures; this simplification understates true overhead by an estimated 10–20%." This 10–20% understatement should be reflected in the uncertainty bounds of the reported $\eta$ values.

5. **Table VIII.** The $C_{\text{coord}} = \infty$ row is redundant with $C_{\text{coord}} = 100$ kbps (both show identical results). Remove or explain why it is included.

6. **Section IV-C.** The duty cycle analysis (Table III) reports "Handoff Success" percentages but the failure model underlying these numbers is not clearly specified. Is this derived from the DES or analytically computed?

7. **Eq. (7), MAC efficiency.** The reference to Akyildiz et al. [48] for $\gamma \approx 0.80$–$0.90$ is for a 2003 paper on multi-layered satellite IP networks. More recent references on LEO ISL TDMA efficiency would strengthen this parameterization.

8. **Section V-B.** The comparison with terrestrial systems (cellular, BGP, ATC) is interesting but superficial. Either develop it with quantitative parallels or shorten it.

9. **Acknowledgment section.** References to "Claude 4.6" and "GPT-5.2" appear to be future/fictional model versions. Clarify.

10. **Data Availability.** The commit hash "[PENDING]" must be resolved before publication.

11. **Figure 3 caption.** States $10^6$-node curve is "analytical extrapolation" but the figure is also referenced in the context of DES-validated results. Ensure the figure clearly distinguishes validated from extrapolated regions (e.g., different line styles).

12. **Section III-B-3.** The derivation of $O(N^2)$ mesh complexity conflates two different arguments: (a) global state convergence requiring $O(N^2)$ information flow, and (b) gossip protocol message complexity. These should be separated more clearly.

---

## Overall Recommendation

**Major Revision**

The paper addresses a relevant problem and demonstrates competent simulation methodology with commendable transparency about limitations. However, the central contribution—confirming analytically expected $O(1)$ overhead scaling in a simulation that abstracts away the phenomena most likely to violate it—is insufficient for a top-tier journal without additional depth. The absence of a realistic decentralized comparator (sectorized mesh), the incomplete exception-based telemetry validation (bandwidth only, no coordination quality), and the circularity of the "no second-order effects" claim in a model that doesn't include the relevant physics are major gaps. A revision should: (1) implement at least a simplified sectorized mesh DES, (2) add at least one physical-layer effect (e.g., TDMA scheduling) to provide a meaningful test of second-order effects, (3) report age-of-information metrics for exception-based telemetry, and (4) restrict scalability claims to the validated range. With these additions, the paper would make a solid contribution to the constellation coordination literature.

---

## Constructive Suggestions

1. **Implement a simplified sectorized mesh DES.** The analytical framework in Section V-C is already well-developed. Even a simplified implementation (fixed sectors, local gossip within sector, aggregated inter-sector exchange) would transform the paper from "hierarchical vs. straw men" to "hierarchical vs. practical alternative," dramatically increasing the contribution's value.

2. **Add a TDMA scheduling model within $T_c$.** This is the lowest-hanging fruit for testing second-order effects. Model each coordination cycle as $k_c$ TDMA slots with guard intervals; measure whether slot scheduling at $k_c = 100$–500 introduces contention or timing violations that the current message-passing abstraction misses. This would make the "no second-order effects" claim credible.

3. **Report age-of-information (AoI) for exception-based telemetry.** For each $p_{\text{exc}}$ value, compute the mean and worst-case age of the coordinator's state estimate for each cluster member. This metric directly quantifies the coordination quality trade-off without requiring a full dynamics simulator, and would make the exception-based telemetry results actionable for system designers.

4. **Consolidate the overhead metric.** Choose either per-node or fleet-level overhead as the primary metric and use it consistently in all tables and figures. Present the other as a secondary metric with clear derivation. The current dual presentation (Tables IV vs. V) creates confusion.

5. **Tighten the scope and shorten the paper.** The paper tries to cover too many parametric studies (cluster size, duty cycle, exception telemetry, link availability, coordinator bandwidth) at insufficient depth. Consider focusing on the 2–3 most novel analyses (coordinator bandwidth stress test and link availability with retransmission are the strongest) and treating the others more briefly, or splitting into two papers.