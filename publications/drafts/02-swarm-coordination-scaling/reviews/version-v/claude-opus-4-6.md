---
paper: "02-swarm-coordination-scaling"
version: "v"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-24"
recommendation: "Major Revision"
---

# Peer Review: "Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study"

## IEEE Transactions on Aerospace and Electronic Systems

---

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a genuinely important problem: how to coordinate autonomous spacecraft swarms at scales of 10³–10⁵ nodes under realistic bandwidth constraints. The framing around mega-constellation growth (Starlink, Kuiper) is timely, and the 1 kbps/node control-plane budget is a reasonable and well-motivated design constraint. The workload-dependent design envelope (5–46% overhead) is a useful engineering contribution, and the explicit byte-level traffic accounting is a methodological strength that distinguishes this work from more abstract analyses.

However, the novelty is substantially undermined by the paper's own admissions. The central scaling result—O(1) overhead ratio for a fixed-depth hierarchy with constant cluster size—is, as the authors acknowledge repeatedly (Section IV-D, Section VI), "a direct mathematical consequence of the hierarchical message structure—not a surprising emergent property." The DES confirms the analytical prediction to within 0.1%, which is a validation exercise rather than a discovery. The paper is commendably honest about this, but it raises the question of what the DES actually contributes beyond what could be derived analytically. The authors identify two DES-specific contributions: (1) TDMA vs. random-phase scheduling effects on coordinator drops, and (2) the workload design envelope. The first is a meaningful but relatively narrow finding (50 kbps vs. 24 kbps threshold). The second is essentially a parameterization of the analytical formula across three command-rate assumptions.

The AoI analysis, Gilbert-Elliott link model, and sectorized mesh comparator add breadth, but each is treated at a relatively shallow level. The AoI analysis applies the established Kaul/Yates framework without coupling to orbital dynamics, limiting its operational relevance. The Gilbert-Elliott analysis, while yielding the useful insight that intra-cycle retransmission is ineffective during correlated bursts, uses a coarse per-cycle discretization that the authors acknowledge may miss sub-cycle phenomena. The sectorized mesh is an interesting hybrid comparator but its parameterization (capped at 10 heartbeat neighbors) is somewhat arbitrary.

The claim of being the first to "systematically compare coordination architectures for autonomous spacecraft swarms across the 10³–10⁵ range using quantitative simulation with explicit byte-level traffic accounting" is plausible but narrow. The comparison is between a studied architecture and intentional bounds, not between realistic competing designs. The sectorized mesh partially addresses this gap but is itself a hybrid that closely resembles the hierarchical architecture.

---

## 2. Methodological Soundness

**Rating: 3 (Adequate)**

The cycle-aggregated DES framework is clearly described and the abstraction level is well-justified for the research questions. The explicit traffic accounting (Table IV), abstraction scope table (Table III), and metric definitions (Section III-G) are exemplary in their precision and transparency. The Monte Carlo framework (30 replications, bootstrap CIs) is appropriate, and the authors are refreshingly candid that the near-deterministic message model renders the MC framework primarily a code-correctness check rather than an exploration of meaningful stochastic uncertainty.

**Concern 1: The DES is largely a deterministic accounting exercise.** The SD < 0.001% across replications, the < 0.1% deviation from closed-form predictions, and the authors' own characterization of the MC framework as confirming "low-variance property rather than exploring substantial stochastic uncertainty" (Section III-D) collectively suggest that the simulation adds minimal information beyond the analytical model. The within-cycle timing model (random-phase vs. TDMA) is the one area where the DES produces genuinely non-trivial results, but this is a relatively small portion of the paper's claims.

**Concern 2: The reference baselines are too weak to support meaningful comparison.** The centralized baseline uses c=1 (acknowledged as worst-case), and the global-state mesh requires O(N²) traffic (acknowledged as an upper bound). While the authors are transparent about this and provide the M/D/c sensitivity table and sectorized mesh comparator, the paper's comparative claims still rest on showing that a reasonable architecture outperforms intentionally extreme bounds. The sectorized mesh is the most informative comparator, but the 1.4–1.5× overhead ratio is specific to the capped-fanout parameterization and may not generalize.

**Concern 3: Key parameters are free variables disconnected from physics.** The exception probability p_exc, the collision avoidance event rate (10⁻⁴/node/s), and the coordinator processing rates (μ_c = 200 msg/s, μ_r = 500 msg/s) are assumed rather than derived. The authors acknowledge this for p_exc but not as explicitly for the other parameters. The sensitivity analysis (Section IV-I) covers reporting rate and MAC efficiency but not the processing rates or collision avoidance rate (beyond a brief mention in Section III-E).

**Concern 4: Spatial model is essentially absent.** The paper studies "space swarms" but the orbital geometry is abstracted to the point where the results are largely topology-independent. Propagation delays are modeled as light-speed distances, but there is no orbital mechanics model determining which nodes can communicate, when links are occluded, or how cluster membership should evolve. The "dynamic spatial partitioning" optimization is identified as future work but is arguably a prerequisite for claiming relevance to space systems.

**Concern 5: Validation is internal only.** The DES is validated against its own analytical model (Section IV-D.2) and against standard queueing theory (M/D/1 at low utilization). There is no validation against external data, hardware-in-the-loop experiments, or higher-fidelity simulations. The authors acknowledge this implicitly by calling for "packet-level simulation of a single cluster" as future work.

---

## 3. Validity & Logic

**Rating: 4 (Good)**

The paper's conclusions are generally well-supported by the analysis, and the authors are commendably careful about qualifying their claims. The distinction between "DES-measured" and "analytically projected" results is maintained throughout. The acknowledgment that the O(1) scaling is an analytical consequence rather than a simulation finding (Section IV-D) is intellectually honest and rare in simulation-based papers.

The workload profile framework (Section III-H) is a well-conceived contribution. The recognition that the 46% stress-case is an upper bound while nominal operations would see ~5% overhead is an important nuance that prevents misinterpretation. The AoI analysis (Section IV-F) correctly identifies the trade-off between bandwidth savings and state staleness, and the caveat that AoI is a "proxy for coordination freshness" rather than a direct safety metric is appropriate.

The Gilbert-Elliott analysis (Section IV-L) yields a clear and operationally relevant conclusion: intra-cycle retransmission is ineffective during correlated bursts. The per-cycle discretization is acknowledged as a limitation, and the recommendation for store-and-forward recovery is well-supported.

One logical concern: the paper argues that hierarchical coordination is motivated by propagation latency and spectrum scarcity (Section IV-A), but the DES does not model either of these constraints. The propagation latency argument is made qualitatively (10–240 ms round-trip), and the spectrum scarcity argument is made analytically (~205 Mbps at 10⁶ nodes), but neither is quantified within the simulation framework. The DES results therefore do not directly support the stated motivation for hierarchical coordination; they support only the overhead and latency characterization of the hierarchical architecture itself.

The coordinator bandwidth stress test (Section IV-G, Table VIII) is one of the paper's strongest contributions, providing actionable engineering bounds. However, the claim that "offered-load is directly measured from DES-instrumented byte counts including retransmission attempts, not approximated" (abstract) slightly overstates the case, since the DES operates at the message layer and does not include transport headers, link acquisition overhead, or Doppler compensation—all of which contribute to true offered load.

---

## 4. Clarity & Structure

**Rating: 3 (Adequate)**

The paper is thorough to the point of being exhausting. At approximately 15,000 words of body text plus extensive tables and figures, it is significantly longer than typical IEEE TAES papers (which target 8,000–10,000 words). The level of detail in the traffic accounting, metric definitions, and abstraction scope is admirable for reproducibility but creates a dense reading experience that obscures the main contributions.

**Structural issues:**

- The paper would benefit from a more aggressive editorial pass to reduce redundancy. The O(1) scaling result is explained at least four times (Sections I-D, IV-D, IV-D.2, VI). The baseline interpretation caveat appears in Sections I-C, IV-A, and V-E. The MAC efficiency qualification appears in Sections III-F, IV-D, IV-I, and VI.

- Section III (Simulation Framework) is 5+ pages and contains material that could be condensed or moved to appendices. The detailed mesh traffic accounting (Table II), sectorized mesh traffic (Table IV), and bandwidth breakdown (Table V) are important for reproducibility but interrupt the narrative flow.

- The contributions list in Section I-D contains 10 bullet points spanning nearly a full page. Several of these are sub-contributions of others (e.g., "Protocol coefficient validation" is a sub-result of the DES framework). A more focused list of 4–5 top-level contributions would be more effective.

- Table I (Simulation Parameters) is comprehensive but dense. The footnotes contain important qualifications that are easy to miss.

**Figures:** The paper references 11 figures, all described via captions but not viewable in the LaTeX source. The captions are detailed and informative, suggesting well-designed figures. However, several figures appear to show results that are essentially flat lines (e.g., Fig. 5 showing constant η ≈ 46% across fleet sizes), which may not justify dedicated figure space.

**Abstract:** The abstract is dense but accurate. It successfully conveys the design envelope (5–46%), the sectorized mesh comparison, the GE link analysis, the AoI contribution, and the coordinator capacity bounds. At ~200 words, it is within IEEE limits but could be tightened.

---

## 5. Ethical Compliance

**Rating: 5 (Excellent)**

The paper includes a transparent acknowledgment of AI-assisted ideation (Claude 4.6, Gemini 3 Pro, GPT-5.2) in the Acknowledgment section, with appropriate qualification that the AI-generated concepts "are not validated in the current study." The reference to a companion methodology paper [53] provides additional context. This level of disclosure exceeds current IEEE requirements and sets a good precedent.

The data availability statement is commendable, with a GitHub repository link (pending commit hash) and interactive web simulators. The open-source commitment supports reproducibility.

The author attribution is unusual ("Project Dyson Research Team" with a footnote about individual names for final publication). This should be resolved before publication per IEEE policy, but is acceptable for review.

No conflicts of interest are apparent. The research does not involve human subjects, classified data, or dual-use concerns beyond the general applicability to military swarm systems (which is discussed openly in Section II-C).

---

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is appropriate for IEEE TAES in its focus on autonomous spacecraft coordination, though the results are more relevant to communication systems engineering than to traditional aerospace topics (guidance, navigation, control). The message-layer abstraction means the results are largely domain-agnostic—they would apply equally to terrestrial IoT networks or drone swarms—which somewhat weakens the aerospace-specific contribution.

**References:** The bibliography contains 55 entries spanning distributed systems theory, swarm robotics, constellation management, queueing theory, and AoI. Coverage is generally good, with appropriate citations to foundational works (Lamport, Kleinrock, Demers et al.) and recent surveys (Dorigo et al. 2021, Yates et al. 2021).

**Notable gaps:**
- No citation to the extensive DTN/CGR (Contact Graph Routing) literature for scheduled space networks, which is directly relevant to the TDMA scheduling analysis. Fraire et al. (2021, IEEE TNET) and Araniti et al. (2015) are relevant.
- No citation to the CCSDS AOS/TM/TC standards that define actual space link protocols, which would ground the message-size assumptions.
- The paper cites Castet and Saleh (2009) for satellite reliability but does not reference more recent reliability analyses of mega-constellations (e.g., Lal et al., 2017; Foreman et al., 2023).
- The mean-field game references (Lasry & Lions, Huang et al.) are mentioned in the related work but never connected to the paper's methodology. If they are not used, they should be removed or their relevance clarified.
- Several references are non-archival (SpaceX website, Amazon website, DARPA program pages, DoD fact sheets). While understandable for current operational systems, the paper should acknowledge the fragility of these citations.

---

## Major Issues

1. **The DES contributes minimally beyond closed-form analysis.** The central overhead result (η ≈ 46%) matches the analytical prediction to within 0.1%, and the O(1) scaling is an analytical tautology for fixed-depth hierarchies. The paper acknowledges this but does not sufficiently address why a simulation study is the right vehicle for these results. The TDMA scheduling analysis (Section IV-J) is the strongest DES-specific contribution but occupies only ~1 page of a ~20-page paper. **Recommendation:** Either (a) substantially expand the DES-specific contributions (e.g., add stochastic workload models, correlated failures, dynamic cluster membership) to justify the simulation approach, or (b) reframe the paper as primarily an analytical design-space characterization with DES validation, reducing the simulation methodology to a supporting role.

2. **Absence of orbital mechanics undermines space-systems relevance.** The paper claims to study "autonomous space swarms" but the spatial model is essentially absent. Cluster membership is static, link availability is modeled as i.i.d. or two-state Markov (not geometry-driven), and the "sectorized mesh" sectors are defined by an arbitrary √N rule rather than orbital geometry. The propagation delay model (light-speed distance) does not account for which nodes are in line-of-sight. **Recommendation:** At minimum, implement a simplified orbital model (e.g., Walker constellation geometry) to derive link availability patterns, cluster membership evolution, and sector boundaries from physics rather than assumptions. This would transform the paper from a generic distributed-systems study into a genuine space-systems contribution.

3. **The comparator architectures are too weak or too similar.** The centralized (c=1) and global-state mesh baselines are intentional extremes that no practitioner would deploy. The sectorized mesh, while more realistic, is architecturally a hybrid that closely resembles the hierarchical architecture (it uses sector coordinators). The paper lacks a comparison against a genuinely different and competitive alternative—e.g., a flat gossip protocol with locality-aware dissemination, a consensus-based approach, or a market-based coordination mechanism. **Recommendation:** Add at least one comparator that represents a realistic alternative design philosophy, not just a parameterization variant of the hierarchical approach.

4. **AoI analysis is disconnected from operational relevance.** The AoI metric is correctly identified as a "proxy for coordination freshness" but is never connected to conjunction detection probability, maneuver decision quality, or any other operational outcome. The statement that "whether this staleness is acceptable depends on the conjunction screening timeline" (Section IV-F) is a punt—this is precisely the question the paper should answer. **Recommendation:** Couple AoI to a simplified conjunction screening model (e.g., probability of detecting a conjunction within a decision window as a function of state age and orbital prediction uncertainty) to produce an operationally meaningful quality metric.

---

## Minor Issues

1. **Section III-F, Eq. (7):** The analytical cross-check equation uses $k_r = 100$ but this value is not clearly justified. The text states $n_r = 10$ regional coordinators (Table I) and $k_r = \lceil N/(k_c \cdot n_r) \rceil$, which at $N = 10^5$ gives $k_r = 10$, not 100. Please clarify whether $k_r$ refers to clusters per region or regions per ground station.

2. **Table VI (Cluster Size):** The latency values show discrete jumps (508→340 ms between k_c=75 and k_c=100) rather than smooth variation. The explanation (burst-driven regional queueing) is plausible but the discretization seems artificial. Is this an artifact of the cycle-aggregated timing model?

3. **Section III-C:** The node communication power (5W baseline, 15–20W coordinator) is stated without justification. What link budget produces these values? At 1 kbps, 5W seems high; at the coordinator's 50 kbps, 20W may be low depending on range and modulation.

4. **Section IV-F, Table IX:** The AoI results at p_exc = 0.10 show Max AoI = 780s. This seems inconsistent with the geometric distribution: at p_exc = 0.10, the probability of no report in 78 cycles (780s) is 0.9^78 ≈ 2.4×10⁻⁴, which for 100 nodes over a year should produce many instances exceeding this. Please verify.

5. **Eq. (1):** The centralized utilization equation uses λ = N·r, but the text later states that arrivals approximate Poisson by the Palm-Khintchine theorem. The M/D/1 model assumes Poisson arrivals and deterministic service; if service times vary by message type (256B vs. 512B vs. 1024B), the model should be M/G/1 with the Pollaczek-Khinchine formula.

6. **Section V-C:** "A sectorized mesh with inter-sector aggregation... closely resembles the hierarchical architecture studied here." This is an important observation that somewhat undermines the value of the sectorized mesh as an independent comparator. The paper should discuss more explicitly what distinguishes the two architectures beyond parameterization.

7. **Table I footnote (a):** The 10⁻⁴/node/s screening alert rate and the 1000:1 screening-to-maneuver ratio are stated without citation. The ESA reference [50] is cited for maneuver rates but not for the screening ratio.

8. **Section III-B.3:** The gossip convergence formula $R_{\text{conv}} = \max(\lceil\log_2 N\rceil, \lceil N/(bf)\rceil)$ conflates two different convergence requirements (epidemic spread of individual entries vs. throughput-limited delivery of all entries). The max() formulation is correct but deserves more careful derivation.

9. **Formatting:** Several tables have footnotes that are nearly as long as the table body (e.g., Tables II, IV, V). Consider moving extended explanations to the main text.

10. **The "Version V" designation** in the review instructions suggests extensive prior revision. The paper reads as if it has been iteratively refined in response to previous feedback, with numerous caveats and qualifications that, while individually appropriate, collectively create a defensive tone. A final editorial pass should aim for confident, concise presentation.

---

## Overall Recommendation

**Major Revision**

This paper addresses a timely and important problem—coordination scaling for large autonomous spacecraft swarms—with commendable methodological transparency and intellectual honesty. The traffic accounting framework, workload design envelope, and coordinator capacity bounds are useful engineering contributions. However, the paper suffers from a fundamental tension: the DES produces results that are almost entirely predictable from closed-form analysis, undermining the justification for a simulation study. The absence of orbital mechanics, the weakness of the comparator architectures, and the disconnection of the AoI metric from operational outcomes limit the paper's contribution to the aerospace systems community specifically. The paper is also significantly too long for its content density, with substantial redundancy that obscures the genuine contributions.

A major revision should: (1) add orbital geometry to ground the spatial model in physics, (2) include at least one genuinely competitive alternative architecture, (3) couple AoI to a simplified conjunction screening model, and (4) reduce length by ~30% through elimination of redundancy and consolidation of supporting material into appendices. With these changes, the paper could make a solid contribution to IEEE TAES.

---

## Constructive Suggestions

1. **Add a Walker constellation geometry model** to derive link availability, cluster membership, and sector boundaries from orbital mechanics rather than assumptions. Even a simplified model (circular orbits, J2 perturbation only) would dramatically strengthen the space-systems relevance. This would also naturally produce the correlated, geometry-driven link outages that the Gilbert-Elliott model approximates.

2. **Implement a conjunction screening quality metric** that couples AoI to orbital prediction uncertainty. For example: model each node's position uncertainty as growing linearly with time since last update (σ_pos ∝ AoI × σ_vel), and compute the probability that a conjunction within a screening volume is detected within a decision window. This would transform the AoI analysis from a generic freshness metric into an operationally meaningful coordination quality measure.

3. **Add a flat consensus-based comparator** (e.g., locality-aware gossip with bounded dissemination radius) that represents a genuinely different design philosophy from hierarchical coordination. This would strengthen the comparative claims and provide system architects with a broader menu of options.

4. **Consolidate the paper around its strongest DES-specific contributions**: the TDMA scheduling analysis, the coordinator capacity stress test, and the workload design envelope. The O(1) scaling validation, while necessary, should be presented concisely as a verification step rather than a central result. This reframing would reduce length and sharpen the contribution.

5. **Perform a single-cluster packet-level validation** using an established network simulator (e.g., ns-3 or OMNeT++) to validate the message-layer abstraction. Even a single configuration (k_c = 100, TDMA scheduling, realistic optical ISL model) would substantially strengthen confidence in the results and address the "internal validation only" concern.