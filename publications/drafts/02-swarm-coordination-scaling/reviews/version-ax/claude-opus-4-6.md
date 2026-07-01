---
paper: "02-swarm-coordination-scaling"
version: "ax"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-27"
recommendation: "Major Revision"
---

# Peer Review: "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms"

**Manuscript Version:** AX
**Venue:** IEEE Transactions on Aerospace and Electronic Systems

---

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a genuine gap: the absence of closed-form sizing equations for hierarchical coordination in autonomous space swarms at the 10³–10⁵ scale. The authors correctly identify that swarm robotics literature operates at 10–100 agents, constellation management at ~10⁴, and networking literature treats routing but not byte-level coordination overhead. The practitioner-oriented "design equation" framing is valuable—engineers sizing future mega-constellation coordination systems would benefit from the AoI, coordinator ingress, and GE recovery expressions collected in Section V-D.

However, the novelty is more integrative than fundamental. The individual analytical components—M/D/1 queueing (Kleinrock), Gilbert-Elliott channel modeling, Age of Information (Kaul/Yates), gossip convergence bounds (Demers), Raft consensus (Ongaro)—are all well-established. The paper's contribution is assembling these into a coherent sizing framework and verifying internal consistency via Monte Carlo. This is acknowledged by the authors ("assembling standard queueing, geometric, and Markov-chain results"), but the question is whether the assembly itself constitutes sufficient novelty for T-AES. The design equations in Section V-D are essentially substitutions into known formulas with domain-specific parameter values.

The 1 kbps RF-backup operating regime is an interesting and well-motivated design point, but it is also quite narrow. The authors argue generalizability (linear scaling with $C_{\text{node}}$), and the observation that at 10 kbps the coordinator bottleneck vanishes entirely is important—but it also somewhat undermines the paper's central tension. If the hierarchical architecture's quantitative challenges disappear at modest bandwidth, the elaborate analysis of the 1 kbps regime becomes more of an academic exercise than a practical design tool. The paper would benefit from more clearly articulating *when* the RF-backup regime is operationally binding and for how long (the abstract says <1% of operational time).

## 2. Methodological Soundness

**Rating: 3 (Adequate)**

The authors are commendably transparent about the verification-vs-validation distinction (Section III-A, Section V-A). The DES operates at the same abstraction layer as the closed-form equations, so the <0.1% agreement (Table VI) confirms implementation correctness, not physical fidelity. This is clearly stated and appropriately caveated.

**Strengths:** The byte-level traffic accounting (Tables III, IV, V) is thorough and internally consistent. The TDMA frame analysis (Section IV-A, Eq. 6–7) deriving γ = 0.949 from first principles rather than assuming a value is good engineering practice. The GE parameter sensitivity sweep (Fig. 5b) providing design curves across $p_{BG}$ and $p_B$ is the most useful analytical contribution. The joint interaction verification (Section IV-D, Table VIII) demonstrating pipeline decoupling under point-to-point links is a clean result with clear scope limitations stated.

**Concerns:**

(a) *Circular verification.* The DES and closed-form equations share identical assumptions (same message sizes, same cycle structure, same loss model). The <0.1% agreement is expected by construction—it verifies coding correctness, not model validity. The paper acknowledges this but still presents the agreement prominently as a result. The inter-cycle GE recovery tail statistics (Fig. 5a) are the one place where the DES provides genuinely independent information, and this should be emphasized more strongly.

(b) *Statistical rigor of tail metrics.* The P99 AoI methodology (Table V footnote) uses per-run P99 values averaged across 30 runs. With ~3.15 × 10⁶ samples per run, the per-run P99 is well-estimated, but the bootstrap CI of [438, 444] s on the mean of 30 per-run P99s conflates estimation uncertainty with run-to-run variability. The authors should report the full distribution of per-run P99 values (min, max, IQR), not just the mean and CI.

(c) *Centralized baseline asymmetry.* The centralized model is acknowledged as a compute-queue-only model (no uplink scheduling, no spectrum constraints), yet it appears in Table XI and Fig. 8 as a direct comparator. The caveat in Section IV-G is clear, but the visual presentation in Fig. 8 ("Centralized diverges at 10⁴") is misleading because it compares a communication-layer model (hierarchical) against a processing-layer model (centralized). The paper should either model centralized communication overhead or remove the centralized curve from communication-overhead comparison figures.

(d) *Sectorized mesh parameterization.* The $k_s = \lceil\sqrt{N}\rceil$ sizing is described as "an order-of-magnitude heuristic" (Section III-B.4). The conjunction screening volume argument is hand-waved; the actual number of satellites within a screening volume depends on constellation geometry, not simply $\sqrt{N}$. This weakens the sectorized mesh as a meaningful comparator.

## 3. Validity & Logic

**Rating: 3 (Adequate)**

The internal logic is generally sound, and the authors are careful about stating scope limitations. Several specific concerns:

**Pipeline decoupling (Section IV-D).** The identical "No Loss" and "GE Only" columns in Table VIII are presented as a key architectural insight, but this is trivially true by construction: if losses occur on point-to-point links before the coordinator queue, lost messages cannot affect queue occupancy. The insight is valid but obvious given the architecture. The more important contribution is identifying *when this breaks down* (shared-medium contention), which is appropriately noted but not quantified.

**AoI-to-position-error coupling (Section IV-B).** The 441 s → ~230 m along-track uncertainty calculation uses a linear drift rate of 0.5 m/s, citing Vallado. This is a gross simplification: along-track error growth depends on differential drag, which is nonlinear and orbit-dependent. The 230 m figure could be off by an order of magnitude for high-drag LEO orbits. The authors note this is "a coarse screening value, not a navigation input," but the number is still presented without adequate uncertainty bounds.

**Coordinator failure transient (Section III-B.2).** The analysis claims coordinator failure occurs "approximately once per 50 years per coordinator" at 2%/yr failure rate. This assumes the coordinator failure rate equals the node failure rate, but coordinators operate at higher power (20 W vs. 5 W) and may have different thermal/radiation profiles. The equal-rate assumption should be explicitly justified or sensitivity-tested.

**Static topology assumption.** The cross-plane drift analysis (Section V-C) bounds re-association overhead at <0.5%, but the 1–3 cycle AoI transient during re-association is dismissed as "well within tolerance" relative to the P99 AoI of 441 s at $p_{\text{exc}} = 0.10$. This comparison is misleading: the 441 s P99 is already identified as problematic (motivating "future coupling to orbital prediction models"), so using it as a baseline to dismiss another degradation is circular.

**Workload profiles (Section IV-E).** The stress-case (one 512-byte command per node per cycle) is described as "fleet-wide maneuver campaigns," but no evidence is provided that such campaigns actually require per-node-per-cycle commands. Real maneuver campaigns are typically staggered over hours/days. The stress case may be unrealistically conservative, inflating the headline overhead number.

## 4. Clarity & Structure

**Rating: 4 (Good)**

The paper is well-organized with a clear roadmap (Section IV opening paragraph). The separation of architecture-specific overhead (~5%) from workload-dependent total overhead (5–46%) is a useful conceptual distinction that is maintained consistently. Tables are generally well-constructed and informative; Table V (traffic accounting) and Table VI (overhead scaling) are particularly clear.

**Strengths:** The abstract is unusually detailed and accurate—every quantitative claim in the abstract is traceable to a specific table or equation. The design equations summary (Section V-D) is a valuable practitioner reference. The explicit enumeration of what is modeled vs. abstracted (Table II) sets appropriate expectations.

**Weaknesses:** The paper is very long for a journal article (~12 pages of dense technical content before references). Several sections could be condensed: the sectorized mesh analysis (Section III-B.4) occupies significant space for what is ultimately a secondary comparator. The notation is generally consistent but the overloading of $\eta$ (offered vs. delivered vs. effective vs. total) creates confusion despite the definitions in Section III-D. A notation table would help.

The half-duplex TX/RX partitioning discussion (Section IV-A) is important but feels like an afterthought—it was clearly added in response to a prior review. It should be integrated more naturally into the TDMA frame analysis rather than appended as a separate paragraph.

Figure quality cannot be assessed from the LaTeX source, but the figure captions are informative and self-contained, which is good practice.

## 5. Ethical Compliance

**Rating: 4 (Good)**

The AI-assistance disclosure in the Acknowledgment section is transparent: "An AI-assisted ideation exercise (Claude 4.6, Gemini 3 Pro, GPT-5.2; see [dyson_multimodel]) motivated aspects of the coordinator architecture but is not validated here." This is appropriately scoped. The open-source data availability statement with a specific repository tag is commendable.

The anonymous authorship ("Project Dyson Research Team") with a note that "Individual author names and affiliations will be provided for final publication per IEEE policy" is unusual but not unprecedented for pre-publication manuscripts. IEEE policy requires named authors for publication; this should be resolved before acceptance.

One minor concern: the reference to future AI model versions (Claude 4.6, GPT-5.2) that do not exist as of mid-2025 suggests either the paper is set in a near-future context or these are placeholder names. This should be clarified.

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is appropriate for T-AES in scope, addressing autonomous spacecraft coordination at scale. The reference list (50+ entries) is comprehensive, covering constellation operations, swarm robotics, distributed systems, queueing theory, and AoI theory.

**Gaps:** The paper does not cite several relevant works on distributed satellite autonomy and ISL network design that have appeared in T-AES itself. Notably absent: (1) recent work on autonomous collision avoidance for mega-constellations (e.g., Bombardelli et al., Sánchez-Arriaga); (2) ISL topology optimization literature (e.g., Ekici et al. in IEEE JSAC); (3) the substantial body of work on DTN scheduling for LEO constellations that directly addresses the intermittent-link regime this paper targets. The NASA DSA reference [nasa_dsa] is appropriate but the discussion of how DSA's approach compares to the proposed hierarchy is superficial.

Several references are non-archival (SpaceX FCC filings, Amazon web pages, DoD fact sheets, NRL magazine articles). While some of these are unavoidable for current constellation data, the paper relies on them for key claims (e.g., Starlink node count, Kuiper plans). The authors should note which claims depend on non-archival sources.

The self-citation [dyson_multimodel] to an unpublished methodology paper on the project website is not independently verifiable.

---

## Major Issues

1. **Validation gap undermines practical utility.** The paper's central claim is providing "practitioner design equations," but the equations are verified only against a DES that shares identical assumptions. No comparison to any physical-layer simulation, hardware testbed, or operational telemetry is provided. The validation gap discussion (Section V-A) is honest but the estimated impacts (5–18% for MAC contention, 2–5% for antenna pointing) are themselves unvalidated. For a T-AES publication claiming practitioner utility, at least one physical-layer validation case (even a simplified NS-3 scenario for a single cluster) should be provided, or the title/claims should be moderated to "message-layer design equations."

2. **Centralized baseline comparison is structurally unfair.** The centralized model captures only compute-queue scalability (M/D/c) while the hierarchical model captures communication-layer overhead. This asymmetry is acknowledged in text but not in figures (Fig. 8) or the abstract. The claim that "the hierarchical advantage is fault tolerance during ground outages" is asserted but not quantitatively demonstrated—no ground-outage scenario is simulated. Either model centralized communication overhead (uplink scheduling, contact windows) or restrict all cross-architecture comparisons to the hierarchical vs. sectorized mesh pair, which are modeled at the same layer.

3. **The 1 kbps regime's practical relevance is unclear.** The abstract states this regime applies "<1% of operational time." The paper devotes ~12 pages to analyzing an operating condition that, by the authors' own admission, is rarely encountered. The generalizability argument (Section I-C) that equations scale linearly with $C_{\text{node}}$ is valid but should be demonstrated with at least one additional bandwidth point (e.g., 10 kbps) analyzed with the same rigor, showing how the design trade-offs change qualitatively.

4. **Inter-cycle GE recovery P95 derivation (Section IV-C) has an approximation error.** The simplified P95 formula in Section V-D ($\lceil \ln(0.05) / \ln(1 - p_{\text{eff}}) \rceil$) assumes geometric recovery, but the actual Markov chain has time-varying recovery probabilities (the channel state distribution evolves over cycles). The geometric approximation is conservative (overestimates P95) only if $p_{\text{eff}}$ is computed at the steady-state mixing probability, but the formula uses a first-cycle approximation. The authors should either derive the exact Markov CDF (which they describe in the "Markov recovery derivation" paragraph) or bound the approximation error.

---

## Minor Issues

1. **Eq. (2):** The M/D/1 waiting time formula $W_q = \rho / [2\mu_s(1-\rho)]$ is correct for M/D/1 but should be cited as the Pollaczek-Khinchine result specialized to deterministic service, not just referenced to Kleinrock generically.

2. **Table I:** The "Representative System" column (e.g., "Hyperscale data center" for c=1000) is speculative and not referenced. Either cite evidence that hyperscale data centers are used for constellation management or remove the column.

3. **Section III-B.2:** "Coordinator rotation: state transfer (10–50 MB) over optical ISL (80–400 ms)" — the 80 ms figure assumes 10 MB at 1 Gbps, but the text says "1–10 Gbps." The range should be 8–400 ms or the ISL capacity should be fixed.

4. **Eq. (5):** $M_{\text{mesh}} = O(N \cdot f \cdot \log N) = O(N^2)$ requires $f = O(N/\log N)$, which is stated but not justified. Standard gossip uses $f = O(\log N)$, giving $O(N \log^2 N)$ total messages. The $O(N^2)$ bound comes from full state replication, not message count. Clarify.

5. **Table V (AoI results):** The "Max AoI" column reports 780 s at $p_{\text{exc}} = 0.10$, but no confidence interval is given for the maximum. As an extreme-value statistic, the max is highly variable across MC runs; report the range.

6. **Section IV-A, half-duplex paragraph:** "commands may be deferred to a separate TDMA frame" — this is a significant architectural assumption that affects the stress-case analysis. If commands require a separate frame, the effective $T_c$ for command delivery doubles. This should be analyzed, not hand-waved.

7. **Section III-C:** "exponential failures at 2%/year (MTTF = 50 yr)" — MTTF = 1/λ = 1/0.02 = 50 yr is correct for the exponential distribution, but the cited reference (Castet & Saleh, 2009) reports infant mortality and wear-out phases that are not exponential. The constant-hazard assumption should be explicitly justified for the operational phase.

8. **Table VII (sim params):** Collision avoidance rate $10^{-4}$/node/s yields ~10 events/node/year, but the text says this represents "screening events, not maneuvers." At $N = 10^5$, this is $10^6$ screening events/year fleet-wide, which seems high. Cross-reference with ESA conjunction statistics.

9. **Notation:** $p_{\text{link}}$ (Table IX) appears to be $1 - p_{\text{loss}}$ (probability of successful transmission), but this is never explicitly defined. In the GE model, $p_G$ and $p_B$ are loss probabilities. Unify notation.

10. **Section V-D, safe-mode floor:** "$\gamma_{\min} = \eta_{\text{total}} / 1.0$" — the denominator of 1.0 is the channel capacity normalized to what? This should be $\gamma_{\min} = \eta_{\text{total}}$ (dimensionless), which is trivially true. Clarify the physical meaning.

11. **Abstract:** "Project Dyson Research Team" with a URL is unusual for IEEE authorship. The acknowledgment references AI model versions that appear to be from the future (Claude 4.6, GPT-5.2). Clarify timeline.

---

## Overall Recommendation

**Major Revision**

The paper addresses a legitimate gap in the literature and provides a well-organized, internally consistent framework for sizing hierarchical coordination in large space swarms. The byte-level traffic accounting, GE sensitivity curves, and design equation collection have genuine practitioner value. However, three issues require substantial revision: (1) the absence of any physical-layer validation, even partial, limits the paper's claim to practical utility—at minimum, a single-cluster NS-3 or OMNeT++ case study should be added, or the scope claims should be explicitly narrowed to "message-layer sizing"; (2) the centralized baseline comparison is structurally asymmetric and should either be made fair (by modeling centralized communication overhead) or restricted to the hierarchical vs. sectorized mesh comparison where both are modeled at the same layer; (3) the practical relevance of the 1 kbps regime needs stronger justification or the analysis should be extended to at least one additional bandwidth point with comparable depth. The paper's transparency about limitations is commendable but does not substitute for addressing them.

---

## Constructive Suggestions

1. **Add a single-cluster physical-layer validation case.** Use NS-3 or OMNeT++ to simulate one 100-node cluster with TDMA scheduling, realistic propagation (free-space + shadowing), and half-duplex constraints. Compare the realized overhead and AoI against the message-layer predictions. Even a single validation point would dramatically strengthen the paper's credibility. This need not cover all phenomena in Section V-A—just MAC contention and half-duplex effects.

2. **Present a dual-bandwidth analysis.** Alongside the 1 kbps RF-backup analysis, provide a parallel column at 10 kbps (or 100 kbps) showing how every design equation's output changes. This would demonstrate the claimed generalizability concretely and help practitioners interpolate to their specific bandwidth regime. The observation that the coordinator bottleneck vanishes at 10 kbps is buried in the introduction; it deserves a table.

3. **Replace the centralized comparison with a ground-outage resilience analysis.** Since the stated hierarchical advantage is "fault tolerance during ground outages," simulate a ground-outage scenario (e.g., 30-minute loss of all ground contact) and quantify the coordination degradation for centralized vs. hierarchical. This would provide the missing quantitative justification for the hierarchical architecture's primary claimed benefit.

4. **Tighten the inter-cycle recovery analysis.** Present the exact Markov-chain CDF (which is already derived in the text) as the primary result, and relegate the geometric approximation to a simplified design rule with a stated conservatism bound. Show the approximation error explicitly (e.g., "geometric P95 = 4 cycles vs. exact P95 = 4 cycles; maximum CDF error = X% at cycle Y").

5. **Add a notation table and reduce $\eta$ overloading.** Define $\eta_{\text{arch}}$ (architecture-specific, ~5%), $\eta_{\text{cmd}}$ (command-dependent), $\eta_{\text{total}}$ (including baseline), and $\eta_{\text{eff}}$ (MAC-adjusted) as distinct symbols used consistently throughout. This would eliminate the need for repeated clarifications about which $\eta$ is being discussed.