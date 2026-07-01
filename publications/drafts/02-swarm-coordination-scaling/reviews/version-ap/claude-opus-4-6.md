---
paper: "02-swarm-coordination-scaling"
version: "ap"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-27"
recommendation: "Major Revision"
---

# Peer Review: "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms"

**Manuscript ID:** Version AP
**Venue:** IEEE Transactions on Aerospace and Electronic Systems

---

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a genuine gap: there is no systematic, byte-level traffic accounting framework for comparing coordination architectures at the $10^3$–$10^5$ node scale. The authors correctly identify that swarm robotics literature stops at ~100 agents, constellation management literature addresses ~$10^4$ nodes without protocol-level detail, and networking literature treats routing without coordination semantics. The "design equations" framing—providing closed-form sizing rules for practitioners—is a useful contribution format for this community.

However, the novelty is more limited than the framing suggests. The core analytical results are relatively straightforward applications of known queueing theory (M/D/1, M/D/c), geometric distributions for exception telemetry, and Gilbert-Elliott channel models. The "design equations" in Section V-C are essentially dimensional analysis of the message model parameters. The headline result—that $\eta$ is $O(1)$ for a hierarchical tree with fixed fan-out—follows directly from the $O(N)$ message count divided by $O(N)$ aggregate bandwidth and does not require simulation to establish. The simulation's primary role is confirming that these single-factor equations compose without interaction (Section IV-D), which is a useful but narrow verification.

The claim of addressing "$10^3$–$10^5$ nodes" is somewhat overstated given that the simulation is vectorized array arithmetic over homogeneous nodes with deterministic message sizes and no spatial dynamics. The complexity that makes large-scale coordination genuinely hard—dynamic topology, heterogeneous link conditions, orbital mechanics coupling, multi-hop routing—is abstracted away (Table VI). The paper is transparent about this, but it means the results characterize a message-accounting model rather than a space swarm coordination system.

## 2. Methodological Soundness

**Rating: 3 (Adequate)**

The message-layer accounting methodology is internally consistent and clearly specified. The traffic model (Table VII), overhead definition (Section III-F), and the separation of baseline telemetry from protocol overhead are well-defined. The Monte Carlo framework (30 replications, bootstrap CIs) is appropriate, though the reported SD < 0.001% (Table IX) suggests the simulation has essentially no stochastic variation beyond the Bernoulli/GE link model—raising the question of what the 30 replications are actually averaging over.

Several methodological concerns warrant attention:

**The cycle-aggregated abstraction is too coarse for the claims made.** The simulation advances in 10-second increments and processes all messages within a cycle as a batch. This is adequate for byte-counting but cannot capture the within-cycle queueing dynamics that determine whether the coordinator link is actually saturated. The paper acknowledges this partially (the $D[k_c]/D/1$ batch model in Section III-B) but then draws conclusions about TDMA slot timing (Eq. 7, Section IV-A) that require sub-cycle temporal resolution the simulation does not provide. The TDMA feasibility claim ("differential propagation delay ~1.7 ms is small relative to the 85 ms TDMA slot duration") is a back-of-envelope calculation, not a simulation result.

**The Gilbert-Elliott model is applied per-cycle rather than per-packet.** State transitions occur once per $T_c = 10$ s, meaning all messages within a cycle experience the same channel state. This is a significant simplification—real correlated fading has state durations on the order of milliseconds to seconds, not 10-second cycles. The "27% intra-cycle recovery" result (Section IV-C) is a direct consequence of this modeling choice: if the bad state persists for an entire cycle, of course all retransmissions within that cycle fail. A more realistic model with sub-cycle state transitions would yield different (likely better) intra-cycle recovery.

**The inter-cycle store-and-forward analysis (Section IV-C) is purely analytical, not simulated.** The paper states this clearly ("This analysis uses closed-form geometric models, not the DES"), but the "4–7 cycles" recovery claim then appears in the abstract and conclusion as a primary result without consistent qualification.

**The sectorized mesh parameterization ($k_s = \lceil\sqrt{N}\rceil$) is acknowledged as heuristic** but is then used for quantitative overhead comparisons (Table IV, Fig. 5). The justification ("a conjunction screening volume contains $O(\sqrt{N})$ nodes when the screening radius scales with mean nearest-neighbor distance") is hand-waving—it depends on the orbital distribution, which is not modeled.

## 3. Validity & Logic

**Rating: 3 (Adequate)**

The internal consistency between analytical predictions and DES measurements is excellent (Table IX: $\Delta < 0.1\%$). However, this tight agreement is itself a concern: it suggests the DES is essentially computing the same closed-form expressions with minor stochastic perturbation, rather than revealing emergent behavior that the analysis might miss. The simulation validates the arithmetic, not the model.

The joint-independence finding (Section IV-D, Table VIII) is the most interesting result but is presented with insufficient nuance. The finding that "GE retransmissions produce zero additional coordinator drops" is a direct consequence of the model architecture: GE losses occur on the link *before* the coordinator queue, so lost messages never arrive. This is not an empirical discovery—it is a structural property of the simulation's event ordering. The paper acknowledges this ("lost messages never contend for coordinator capacity") but still frames it as a "key finding." The more important observation—that this independence would break under shared-medium contention—is relegated to a caveat.

The comparison with centralized processing (Table XI) is carefully qualified but still potentially misleading. The $c = 1$ baseline diverges at $N = 10^4$, but this is an intentional strawman. The realistic $c = N/k_c$ baseline does not diverge until $N \approx 10^6$, and the paper correctly identifies that the binding centralized constraints are spectrum and latency, not processing. This honest assessment somewhat undermines the paper's motivation: if centralized processing works to $10^6$ and the hierarchical advantage is "fault tolerance during ground outages," the contribution is a backup-mode protocol design, not a scalability breakthrough.

The AoI analysis (Section IV-B) is clean but the coupling to operational relevance is weak. The P99 AoI of 441 s at $p_{\text{exc}} = 0.10$ corresponds to ~230 m along-track uncertainty—acknowledged as "a coarse screening value, not a navigation input." This raises the question: for what operational decisions is this AoI adequate? The paper defers this to future work (coupling to conjunction probability), but without it, the AoI numbers lack actionable interpretation.

## 4. Clarity & Structure

**Rating: 4 (Good)**

The paper is well-organized and generally well-written. The roadmap at the beginning of Section IV is helpful. The consistent use of $\eta$ notation, the clear separation of baseline telemetry from protocol overhead, and the traffic accounting tables (Tables V, VII) make the methodology reproducible. The "Baseline Interpretation Note" (Section I-C) and repeated caveats about the RF-backup operating regime show awareness of potential misinterpretation.

Several structural issues reduce clarity:

The paper is dense with tables (14 tables) and figures (13 figures), some of which are redundant. Table IX (overhead scaling) shows $\eta = 46.0\%$ at every fleet size with a note that 8 intermediate sizes are "omitted for brevity"—but the point is that $\eta$ is constant, which could be stated in one sentence. Table XII (latency decomposition) and Table XIII (cluster size) could be consolidated. The sectorized mesh is introduced in Section III-B.4 with its own traffic table (Table IV), sensitivity table (Table IV), and separate traffic accounting (Table V), consuming significant space for what is described as an "intermediate comparator with heuristic parameterization."

The abstract is overloaded with specific numbers (21–50 kbps, P99 = 440 s, 27%, 4–7 cycles, $9\times$ envelope, $N \approx 10^6$) that are difficult to contextualize without reading the paper. A more concise abstract focusing on the key insight—that hierarchical overhead is workload-dominated rather than topology-dominated—would be more effective.

The notation is mostly consistent, but $\eta$ is used for both offered and delivered overhead (Section III-F), with $\eta_{\text{delivered}}$ introduced but rarely used. The MAC efficiency $\gamma$ appears in multiple contexts (TDMA guard time, Slotted ALOHA throughput) without always being clear which is intended.

## 5. Ethical Compliance

**Rating: 4 (Good)**

The paper provides commendable transparency on several fronts: open-source code with a tagged release, explicit acknowledgment of AI-assisted ideation (Claude 4.6, Gemini 3 Pro, GPT-5.2), and clear identification of non-archival references. The data availability statement is specific and actionable.

The author block uses a team name ("Project Dyson Research Team") with a footnote promising individual names for final publication. This is unusual for IEEE T-AES and should be resolved before acceptance. The acknowledgment section's mention of AI tools is appropriate but the phrase "Claude 4.6, Gemini 3 Pro, GPT-5.2" references model versions that do not exist as of mid-2025, suggesting either future-dated writing or placeholder names. This should be clarified.

The paper does not discuss potential dual-use implications of autonomous swarm coordination technology, which is relevant given the military swarm programs cited in Section II-C. While not strictly required, a brief discussion would strengthen the ethical framing.

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is appropriate for IEEE T-AES in scope, addressing spacecraft coordination architectures with quantitative engineering analysis. The reference list (48 citations) covers the relevant domains: constellation operations, swarm robotics, queueing theory, distributed systems, and AoI theory.

Several referencing gaps are notable. The paper does not cite recent work on distributed spacecraft autonomy from the small-satellite community (e.g., Nag & Hewagama on autonomous scheduling, Radhakrishnan et al. on inter-satellite link design for CubeSat constellations). The AoI section cites the foundational papers [Kaul, Yates, Kadota] but misses recent AoI work specifically in satellite networks (e.g., Abd-Elmagid et al., "Age of Information in IoT-Based Space-Air-Ground Integrated Networks"). The Gilbert-Elliott model citation is implicit; the original Gilbert (1960) and Elliott (1963) papers should be cited.

Several references are non-archival (Starlink FCC filing, Amazon Kuiper overview, DARPA program pages, DoD fact sheets, NRL magazine article). While the paper flags these, they weaken the scholarly foundation. The self-citation [dyson_multimodel] points to a URL without publication venue or peer review status.

The paper claims "no prior work has systematically compared coordination architectures for autonomous swarms across $10^3$–$10^5$ nodes using byte-level traffic accounting" (Section I-A). This is likely true as stated but somewhat narrow—there is substantial work on satellite network capacity planning and traffic engineering that addresses similar questions at different abstraction levels (e.g., Ekici et al. on LEO satellite network traffic, Araniti et al. on 5G-satellite integration).

---

## Major Issues

1. **The simulation adds minimal value beyond the closed-form analysis.** The DES matches analytical predictions to within 0.1% (Table IX), the joint-independence result follows from the model's event ordering, and the inter-cycle recovery analysis is purely analytical. The paper should either (a) introduce model complexity that creates genuine analytical intractability (dynamic topology, multi-hop routing, heterogeneous links), or (b) reframe the contribution as primarily analytical with the DES as a consistency check—which would require acknowledging that the "design equations" are essentially the model definition, not derived results.

2. **The GE model's per-cycle state transitions are unrealistically coarse.** Applying channel state transitions at 10-second granularity conflates burst duration with coordination cycle duration. This inflates the severity of correlated losses (all intra-cycle retransmissions fail in bad state) and makes the "27% recovery" result an artifact of the time-scale choice. The authors should either (a) implement sub-cycle GE transitions and show how results change, or (b) explicitly bound the sensitivity of the 27% figure to the state-transition timescale.

3. **The operational relevance of the results is insufficiently established.** The paper characterizes protocol overhead, AoI, and loss recovery but does not connect these to operational requirements. What AoI is *needed* for conjunction screening? What per-cycle completion rate is *required*? Without requirements, the design equations cannot be used for actual sizing. The paper should define at least one concrete operational scenario (e.g., conjunction screening with a specific miss-distance threshold) and show how the design equations map to that requirement.

4. **The $10^6$-node extrapolation in the abstract and conclusion is unsupported.** The claim that "a realistically provisioned centralized processing baseline does not diverge computationally until $N \approx 10^6$" is based on the trivial observation that $N_{\max} = c \cdot \mu_s / r$ with $c = 100$ (Table II). This is not a simulation result or even a meaningful analytical finding—it is a parameter choice. The abstract should not present this as a result.

5. **Absence of spatial/orbital dynamics undermines the "space swarm" framing.** The simulation treats nodes as homogeneous message generators with no orbital mechanics, no dynamic topology changes (beyond failure), no Earth occlusion, and no relative motion effects on link geometry. The cluster structure is static. For a paper targeting IEEE T-AES, some minimal orbital fidelity—even a Walker constellation model with time-varying link availability—would substantially strengthen the relevance claim.

---

## Minor Issues

1. **Eq. (2):** The M/D/1 waiting time formula $W_q = \rho / [2\mu_s(1-\rho)]$ is correct for M/D/1 but should be explicitly identified as the Pollaczek-Khinchine result for deterministic service (coefficient of variation $c_s = 0$). The general P-K formula is $W_q = \rho(1+c_s^2) / [2\mu_s(1-\rho)]$.

2. **Section III-B.2:** "Each cluster coordinator sends a single 512-byte summary per cycle (vs. forwarding $k_c$ individual reports)"—this aggregation ratio should be discussed in terms of information loss. What is lost in the 256→512 byte compression of $k_c = 100$ reports?

3. **Table I:** The "Representative System" column (e.g., "Hyperscale data center" for $c = 1000$) is informal and potentially misleading for a journal paper. Consider replacing with specific processing requirements (FLOPS, memory).

4. **Section III-E:** "Full-participation (no sampling)" is stated but not explained. What would sampling mean in this context?

5. **Table VI:** "Correlated failures (SPE, batch)" is listed as abstracted, but SPE (Solar Particle Events) can disable entire orbital planes simultaneously. Given the paper's focus on fault tolerance, this omission is more significant than a typical abstraction.

6. **Eq. (8):** The AoI P99 formula uses $\lceil \cdot \rceil$ (ceiling), which is correct for discrete geometric distributions, but the derivation should note that this assumes the coordinator samples AoI at cycle boundaries, not continuously.

7. **Section IV-A:** "Model B uses a leaky-bucket shaper" — the term "leaky bucket" typically refers to a specific traffic shaping algorithm. The description sounds more like a token bucket. Please clarify or use standard terminology (RFC 2697/2698).

8. **Table VIII:** The "GE Only" column shows identical drops to "No Loss" at every capacity level. This is the independence result, but it is visually confusing—a reader might think the columns were accidentally duplicated. Add a footnote or in-text explanation.

9. **Acknowledgment section:** "Total MC wall-clock time: ~90 min on commodity hardware" belongs in the methodology section, not acknowledgments.

10. **References:** [1] cites both an FCC filing and "Jonathan's Space Report" (non-archival blog) in the same entry. These should be separate references, or the blog citation should be removed.

11. **Fig. 1:** Referenced but described as a PDF file (`fig-architecture-diagram.pdf`). The figure description mentions "Labels: aggregation ratios" but the actual content cannot be verified from the LaTeX source.

12. **Section I-D:** The notation "$\eta$ as protocol overhead beyond topology-invariant baseline telemetry" is introduced before the formal definition in Section III-F. Consider moving the definition earlier or adding a forward reference.

---

## Overall Recommendation

**Major Revision**

The paper addresses a legitimate gap in the literature and provides a well-organized, reproducible framework for sizing hierarchical coordination protocols. The traffic accounting methodology is clean, the analytical cross-checks are thorough, and the open-source commitment is commendable. However, the contribution is currently positioned between two stools: the analytical results are too straightforward to constitute a significant theoretical advance, and the simulation is too abstract to constitute a significant systems contribution. The major revision should address the operational relevance gap (connecting design equations to concrete mission requirements), improve the GE channel model fidelity, and either add minimal orbital dynamics or honestly reframe the contribution as a communication-protocol sizing tool rather than a space swarm coordination architecture. The paper has a solid foundation and could become a useful reference for the community with these revisions.

---

## Constructive Suggestions

1. **Define an operational requirements baseline.** Select one concrete mission scenario (e.g., LEO conjunction screening with a 1-km miss-distance threshold at 95% confidence) and show end-to-end how the design equations size the architecture. This would transform the paper from a parameter study into a design methodology demonstration. The AoI-to-position-error coupling (currently one sentence citing Vallado) should be the centerpiece of this analysis.

2. **Implement time-varying link topology.** Even a simple model—e.g., Earth occlusion causing periodic link outages with known duty cycles for LEO orbits—would dramatically strengthen the space systems relevance. This would also create genuine analytical intractability that justifies the simulation, and would test whether the joint-independence result holds under time-correlated link availability (which it likely would not).

3. **Refine the GE model to sub-cycle granularity.** Implement state transitions at per-message or per-slot timescales and show how intra-cycle recovery improves. Report the 27% figure as the worst case (full-cycle bad state) alongside the more realistic sub-cycle result. This would make the correlated-loss characterization genuinely useful for link budget design.

4. **Consolidate the presentation.** The paper could lose 2–3 pages without sacrificing content by merging redundant tables (e.g., Tables III/V, IX/X, XII/XIII), reducing the sectorized mesh treatment to a single paragraph with one table, and tightening the abstract. The freed space could accommodate the operational scenario analysis suggested above.

5. **Strengthen the centralized-vs-hierarchical comparison.** The paper's most honest and interesting finding is that centralized processing works to $10^6$ and the hierarchical advantage is fault tolerance, not scalability. Lean into this: quantify the fault-tolerance advantage (e.g., expected coordination outage duration during a 15-minute ground contact gap at $N = 10^5$) and make it the primary motivation rather than an afterthought.