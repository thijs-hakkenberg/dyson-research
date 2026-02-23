---
paper: "02-swarm-coordination-scaling"
version: "e"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-23"
recommendation: "Major Revision"
---

# Peer Review: "Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study"

**Manuscript Version:** E
**Venue:** IEEE Transactions on Aerospace and Electronic Systems

---

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a genuinely important gap: the systematic comparison of coordination architectures across the $10^3$–$10^6$ node range for autonomous space systems. The authors correctly identify that the swarm robotics literature rarely exceeds ~1,000 agents experimentally, and that constellation management literature has not published scalability analyses beyond ~15,000 nodes. This intermediate regime is indeed underexplored, and the question is timely given Starlink's growth trajectory and the emergence of competing mega-constellations.

However, the novelty is tempered by several factors. First, the core finding—that hierarchical architectures scale better than flat centralized or fully meshed topologies—is well established in distributed systems theory (the authors themselves cite Lynch [7] for the $O(\log N)$ propagation result). The contribution is thus primarily quantitative rather than conceptual: putting specific numbers on overhead percentages for a particular parameterization. Second, the "reference baselines" are deliberately extreme (single-server centralized, full global-state mesh), which makes the hierarchical architecture's superiority somewhat predetermined by construction. The paper acknowledges this (Section V-C discusses the sectorized mesh as a more realistic intermediate), but the absence of this intermediate architecture from the actual simulation weakens the comparative contribution. Third, the three optimizations described in Section IV-D (exception-based telemetry, dynamic spatial partitioning, heterogeneous hardware) are described qualitatively rather than rigorously modeled—they are asserted to "restore overhead to acceptable levels" but the simulation evidence for this claim is not presented with the same rigor as the baseline results.

The practical applicability claims (mega-constellations, drone swarms, IoT) are reasonable but somewhat generic. The paper would benefit from a more focused demonstration of how the specific quantitative findings (e.g., the 50,000-node superlinear onset) translate into actionable design decisions for a specific near-term system.

---

## 2. Methodological Soundness

**Rating: 2 (Needs Improvement)**

The discrete event simulation framework is described with reasonable detail, and the Monte Carlo approach with 50–100 runs per configuration is appropriate. The validation against closed-form M/D/1 solutions (Section III-A) and gossip convergence bounds is a positive methodological step, though limited to low-utilization regimes. The parameter table (Table II) is comprehensive and supports reproducibility.

However, several methodological concerns are significant:

**Idealized link model.** The authors acknowledge this limitation (Section V-E) but understate its impact. Earth occlusion alone causes 40–60% link unavailability in LEO, which is not a second-order effect—it fundamentally changes the connectivity graph and could invalidate the hierarchical architecture's performance if coordinator-to-regional links are disrupted during critical windows. The claim that physical-layer effects are "approximately topology-neutral" (Section V-E) is asserted without evidence. The hierarchical architecture concentrates traffic on specific links (node→coordinator, coordinator→regional), making it structurally more vulnerable to link unavailability at those specific points than the mesh topology, which distributes traffic uniformly. This is acknowledged in passing but not quantified, and it represents a potentially critical confound.

**Spatial model abstraction.** The orbital mechanics model is described as "simplified" but the degree of simplification is not specified. Are nodes placed on realistic orbital shells with J2 perturbation? Are they randomly distributed in 3D space? The communication distance calculations, propagation delays, and the validity of the "random geometric graph" assumption for mesh diameter ($D = O(N^{1/3})$) all depend on the spatial distribution, which is never explicitly defined. For a paper in IEEE T-AES, the orbital mechanics fidelity should be at minimum stated precisely.

**Superlinear scaling claim.** The observation of superlinear scaling near 50,000 nodes (Section IV-D) is presented as a finding but is based on only five data points spanning three orders of magnitude. The authors commendably acknowledge this limitation and call for intermediate-scale simulation, but the claim is nonetheless featured prominently in the abstract and conclusions. With the current data density, the "superlinear onset" could equally be an artifact of the specific cluster size parameterization at that scale, a boundary effect of the four-level hierarchy's fan-out structure, or simply noise. The $R^2 > 0.99$ for the linear fit below 50,000 nodes is reported without the corresponding fit statistics for the superlinear regime.

**Missing decomposition.** The paper states (Section IV-D) that instrumenting the simulation to separately track intra-cluster, cluster-to-regional, and regional-to-ground message volumes "would confirm whether inter-regional reconciliation drives the observed superlinearity" but that "we have not performed this decomposition in the current study." This is a significant omission—the decomposition would be straightforward to implement and would substantially strengthen the analysis. Its absence suggests the simulation instrumentation may be less mature than the paper implies.

**Queueing model consistency.** The centralized baseline uses M/D/1 (deterministic service), but the hierarchical model also uses M/D/1 at each level. The "M" (Poisson arrivals) assumption is reasonable for the centralized case where many independent nodes report, but within a cluster of 50–100 nodes, the superposition of periodic reporters does not produce Poisson arrivals—it produces a near-deterministic aggregate arrival process, especially if nodes are synchronized. The D/D/1 model would be more appropriate for intra-cluster traffic, and the discrepancy could affect the latency distributions reported in Table III.

---

## 3. Validity & Logic

**Rating: 3 (Adequate)**

The logical structure of the argument is generally sound: establish reference baselines, characterize the hierarchical architecture against them, optimize parameters, identify scaling regimes. The conclusions are appropriately hedged in most places, with qualifiers like "under the parameterization described herein" and "parameter-dependent threshold."

The overhead decomposition (Section III-F) is well-handled. The separation of topology-invariant baseline telemetry (20.5%) from protocol overhead is a clean analytical choice that enables fair comparison. The bandwidth breakdown table (Table I) at $N = 100,000$ is informative and helps ground the abstract percentages in concrete numbers.

However, several logical issues merit attention:

**Circular reasoning in mesh baseline.** The $O(N^2)$ characterization of the global-state mesh depends on the assumption that every node needs full fleet trajectory state. The justification (Section III-B-3) cites three astrodynamics considerations (coordinated orbit-raising, intersecting planes, conjunction cascades). While these are valid concerns, they apply with varying force depending on the orbital architecture. In a single-shell constellation (like Starlink's operational shells), conjunction risk is dominated by inter-plane crossings at specific latitudes, and most node pairs never approach each other. The paper's own discussion of sectorized mesh (Section V-C) implicitly acknowledges that full global state is not strictly necessary. The $O(N^2)$ baseline thus represents a worst case that may be unrealistically pessimistic, making the hierarchical architecture's advantage appear larger than it would be against a more realistic decentralized alternative.

**State completeness trade-off.** Table I (State Completeness by Topology) correctly notes that the hierarchical architecture provides "aggregated summaries for $O(N)$ fleet" rather than full trajectory state. This is a fundamental capability difference, not merely an efficiency trade-off. The paper does not adequately address whether aggregated summaries are *sufficient* for the fleet-wide collision avoidance that motivates the global-state mesh baseline. If they are sufficient, the mesh baseline is unnecessarily expensive; if they are not, the hierarchical architecture has a capability gap that the overhead comparison does not capture.

**Optimizations not rigorously evaluated.** The three optimizations in Section IV-D are described at a conceptual level and their combined effect is shown in Fig. 7, but the individual contribution of each optimization is not quantified, and the simulation methodology for the "optimized" curve is not described with the same rigor as the baseline. Are these optimizations implemented in the DES, or are they analytical estimates? The text says they "collectively restore overhead to acceptable levels" but the mechanism by which exception-based telemetry achieves "approximately two orders of magnitude" reduction is not derived or validated.

**Duty cycle analysis.** The inverse relationship between duty cycle and handoff success (Table IV) is explained by cumulative failure probability over multiple handoffs per day. However, the 95% handoff success rate at 1-hour duty cycles seems low for a 1–10 second state transfer over a 1–10 Gbps link. The failure model for handoffs is not clearly specified—is it link unavailability during the transfer window, processing errors, or something else? The 5% failure rate per handoff at 1-hour cycles needs justification.

---

## 4. Clarity & Structure

**Rating: 4 (Good)**

The paper is well-organized and clearly written. The progression from problem statement through methodology, results, and discussion follows a logical arc. The abstract is detailed and accurate, though somewhat long for IEEE T-AES conventions. The explicit labeling of research questions (RQ1–RQ3) and their mapping to results sections aids readability.

Several structural choices are particularly effective: the bandwidth breakdown table (Table I), the state completeness comparison (Table I in Section III-B-3), and the explicit separation of baseline telemetry from protocol overhead throughout. The discussion of centralized baseline limitations (processing vs. propagation vs. spectrum) in Section III-B-1 is thorough and well-reasoned.

Areas for improvement: The paper is quite long for a journal article, partly due to extensive defensive qualification of the reference baselines. While this thoroughness is appreciated (and likely reflects responses to prior review rounds), some of this material could be condensed. For example, the M/D/c sensitivity analysis (Table II in Section III-B-1) makes its point effectively in a few sentences; the surrounding discussion could be tightened. The Related Work section is comprehensive but could better distinguish between works that directly inform the simulation design versus those providing general context.

The figures are referenced but not provided (as expected for a LaTeX source review). The figure captions are descriptive and self-contained, which is good practice. However, the paper relies heavily on figures that the reviewer cannot evaluate—particularly Fig. 2 (overhead scaling), Fig. 3 (latency distributions), and Fig. 7 (scaling trajectory with optimizations). The quantitative claims in the text should be verifiable from the tables alone, and in most cases they are.

---

## 5. Ethical Compliance

**Rating: 4 (Good)**

The paper includes a transparent acknowledgment of AI-assisted ideation (Acknowledgment section), specifying the models used (Claude 4.6, Gemini 3 Pro, GPT-5.2) and the scope of their contribution (architectural concept generation, not validation). The statement that the AI-generated "Shepherd/Flock" concept "is not validated in the current study" is appropriately cautious. The reference to a companion methodology paper [42] for details on the AI-assisted process is a reasonable approach.

The data availability statement is commendable, with a specific GitHub repository URL and commit hash placeholder. The computational resource disclosure (2,400 CPU-hours on a 64-core workstation) is transparent.

Two minor concerns: First, the author block uses a team name ("Project Dyson Research Team") with a footnote promising individual names for final publication. IEEE policy requires named authors; this should be resolved before acceptance. Second, the non-archival references (SpaceX website, Amazon website, DARPA program pages, DoD fact sheets) are appropriately flagged but constitute a non-trivial fraction of the bibliography. While unavoidable for some operational systems, the paper should ensure that all quantitative claims are supported by archival sources.

---

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is appropriate for IEEE T-AES in its focus on autonomous spacecraft coordination architectures. The references span the relevant literature: distributed systems theory (Lamport, Lynch), swarm robotics (Brambilla, Dorigo), constellation operations (Handley, del Portillo), consensus theory (Olfati-Saber, Ren & Beard), and queueing theory (Kleinrock). The inclusion of DTN/Bundle Protocol references (Cerf, CCSDS BPv7) and military swarm programs (DARPA OFFSET, Blackjack) demonstrates breadth.

However, several notable omissions weaken the referencing:

- **No references to actual hierarchical satellite coordination implementations.** The ESA OPS-SAT or similar on-orbit autonomy experiments would provide empirical grounding. The paper cites no work that has actually implemented hierarchical coordination on spacecraft.
- **Missing references on space traffic management (STM).** The growing STM literature (e.g., Weeden & Samson, Secure World Foundation reports; Bonnal et al. on active debris removal coordination) is directly relevant to the collision avoidance coordination that motivates the global-state mesh baseline.
- **No reference to the Telesat Lightspeed constellation**, which explicitly uses a mesh ISL topology and has published on its coordination architecture.
- **The GNN references (Tolstaya, Li) are somewhat tangential.** They are cited for communication complexity bounds but the simulation does not use GNN controllers. The connection to the present work is theoretical rather than methodological.
- **Mean-field game theory references (Lasry & Lions, Huang et al.) are cited but never used.** They appear in Related Work as potentially relevant at large scales but play no role in the simulation or analysis. Either develop the connection or remove the references.

The reference to future model versions (Claude 4.6, GPT-5.2) in the Acknowledgment raises a minor concern about the timeline of the work, though this does not affect the technical content.

---

## Major Issues

1. **Absence of realistic link model undermines quantitative claims.** The paper's central quantitative contribution—specific overhead percentages at specific scales—is obtained under idealized link conditions that exclude Earth occlusion, MAC contention, link acquisition delays, and Doppler effects. The authors estimate these could increase overhead by 2–4× (Section V-E), which would push the hierarchical architecture's overhead from 2–8% to 4–32%, potentially overlapping with the centralized baseline's range. Without at minimum a stochastic link availability model, the specific numbers reported cannot be considered reliable for system design. **Required action:** Either incorporate a basic link availability model (even a simple Bernoulli on/off model calibrated to orbital geometry) or substantially downgrade the quantitative claims to qualitative ordering results.

2. **Superlinear scaling regime is under-characterized.** The superlinear onset near 50,000 nodes is featured in the abstract, contributions list, and conclusions, but is supported by only 5 data points without message decomposition, formal change-point analysis, or sensitivity analysis across cluster sizes. **Required action:** Either (a) add simulation runs at intermediate fleet sizes with message decomposition to properly characterize the transition, or (b) demote this from a "finding" to a "preliminary observation" and remove it from the abstract and contributions list.

3. **Optimizations (Section IV-D) lack rigorous evaluation.** The "optimized" curve in Fig. 7 is a key result but the simulation methodology for the three optimizations is not described. Are they implemented in the DES or estimated analytically? What are the individual contributions? The "two orders of magnitude" reduction from exception-based telemetry is stated without derivation. **Required action:** Provide simulation details for the optimized configurations, or clearly label the optimized curve as a projected estimate rather than a simulation result.

4. **Reference baselines are asymmetrically extreme, limiting comparative value.** The centralized baseline (single server, no parallelization) and global-state mesh (full fleet state at every node) represent opposite extremes that bracket the design space so widely that almost any reasonable architecture would fall between them. The paper acknowledges this and discusses the sectorized mesh as a more realistic intermediate, but does not simulate it. **Required action:** Either simulate the sectorized mesh variant or explicitly reframe the contribution as "characterization of hierarchical scaling" rather than "comparison across architectures," since the comparison is against deliberately extreme bounds rather than realistic alternatives.

5. **Queueing model mismatch for intra-cluster traffic.** The M/D/1 assumption for cluster coordinators receiving periodic reports from 50–100 nodes is questionable. Periodic reporters with similar periods produce bursty, near-deterministic arrival patterns, not Poisson arrivals. This could significantly affect the latency distributions in Table III and Fig. 3. **Required action:** Justify the Poisson arrival assumption for intra-cluster traffic (e.g., by showing that reporting phases are randomized) or use a more appropriate arrival model.

---

## Minor Issues

1. **Abstract length.** At approximately 200 words, the abstract is within IEEE limits but dense. Consider whether the specific mention of "20.5% baseline telemetry" in the abstract is necessary—it requires context that the abstract cannot fully provide.

2. **Eq. (4) notation.** The hierarchy levels are described as "Ground → Regional → Cluster → Node" but Eq. (5) uses $k_c$ and $k_r$ without defining the ground-to-regional fan-out. The four-level structure implies a fourth parameter that is never named.

3. **Table III confidence intervals.** The footnote states "95% bootstrap CIs are within ±5% of reported means for all entries." This is ambiguous—does it mean ±5% relative (e.g., 4.8% ± 0.24%) or ±5 percentage points? The former is plausible; the latter would indicate very wide uncertainty. Clarify.

4. **Section III-F, transport-layer overhead.** The statement that transport-layer overhead "understates true overhead by an estimated 10–20%" should specify the basis for this estimate. Is it derived from CCSDS Proximity-1 protocol overhead, or a general assumption?

5. **Collision avoidance rate justification.** The $10^{-4}$/node/s rate is justified by a 1,000:1 screening-to-maneuver ratio applied to ESA's reported 1–3 maneuvers/year/spacecraft. This yields $10^{-4}$ only if the screening events are uniformly distributed in time, which they are not—conjunction screening is concentrated around specific orbital crossings. The temporal clustering of screening events could create burst loads not captured by the Poisson assumption.

6. **Section V-B, cellular network analogy.** The claim that "the hierarchical coordination architecture proposed here can be viewed as a space-based cellular network operating in three dimensions" overstates the analogy. Cellular networks have fixed infrastructure (base stations) and mobile clients; the proposed architecture has mobile infrastructure (rotating coordinators) and mobile clients, which is a fundamentally different coordination problem.

7. **Eq. (8), power overhead.** The calculation $\Delta P_{\text{avg}} = 15\text{W}/100 = 0.15\text{W}$ assumes uniform duty sharing, but the preceding text notes that duty cycles of 24–48 hours are optimal. With 100 nodes and 24-hour cycles, each node serves as coordinator for $24/100 = 0.24$ hours per cycle, not 1% of the time. The calculation should be $\Delta P_{\text{avg}} = (1/k_c) \times \Delta P_{\text{coord}}$, which gives the same result but the textual explanation ("each node serves as coordinator approximately 1% of the time") is correct only if the duty cycle equals $k_c \times$ (rotation period). Clarify.

8. **Reference [1] (SpaceX Starlink operations)** is a corporate website, not a technical reference. The claim of "approximately 7,000 active satellites" should cite a more authoritative source (e.g., Jonathan McDowell's satellite catalog or the FCC filings).

9. **Section III-B-3, fanout derivation.** The statement "The fanout $f = O(N/\log N)$ follows from the requirement that each of $N$ state entries must be disseminated to all $N$ nodes within $O(\log N)$ gossip rounds" is not rigorous. Standard gossip analysis shows that fanout $f = O(\log N)$ suffices for single-rumor dissemination in $O(\log N)$ rounds. The $O(N/\log N)$ fanout arises from the multi-rumor requirement, but the derivation conflates rounds with per-round coverage in a way that needs tightening.

10. **Typo/style.** "Lluch i Cruz" in the bibliography [46] should verify the correct Catalan name formatting per the author's published preference.

---

## Overall Recommendation

**Major Revision**

This paper addresses a relevant and timely problem—scaling coordination architectures for very large autonomous space systems—and presents a well-structured simulation study with commendable transparency about assumptions and limitations. The separation of baseline telemetry from protocol overhead, the explicit parameterization table, and the honest acknowledgment of the superlinear regime's under-characterization all reflect scientific rigor. However, the idealized link model undermines the quantitative precision of the central claims, the reference baselines are too extreme to provide meaningful architectural comparison, the superlinear scaling finding is insufficiently supported for the prominence it receives, and the optimizations that address the scaling challenge are not rigorously evaluated. A major revision incorporating at minimum a stochastic link availability model, intermediate-scale simulation with message decomposition for the superlinear regime, and either simulation of the sectorized mesh or reframing of the comparative claims would substantially strengthen the contribution.

---

## Constructive Suggestions

1. **Add a stochastic link availability layer.** Even a simple two-state Markov model (link available/unavailable) calibrated to LEO orbital geometry would dramatically strengthen the quantitative claims. Parameterize the availability probability as a function of orbital altitude and inclination, and report overhead results as ranges across link availability scenarios. This need not require a full orbital propagator—a statistical model of link availability derived from published constellation geometry analyses (e.g., del Portillo et al. [48]) would suffice.

2. **Simulate the sectorized mesh variant.** This is identified as future work (Section V-C) but is critical for the paper's comparative value. A sectorized mesh with $\sqrt{N}$ sectors and inter-sector aggregation would provide a realistic decentralized baseline that tests whether the hierarchical architecture's advantage persists against a reasonable alternative rather than an extreme bound. Even a simplified implementation at 2–3 scale points would substantially strengthen the paper.

3. **Instrument the simulation for message decomposition.** Separately tracking intra-cluster, cluster-to-regional, and regional-to-ground message volumes is straightforward and would (a) confirm or refute the hypothesized cause of superlinear scaling, (b) validate the 60/25/15% decomposition claimed in Section IV-B, and (c) identify which hierarchical level is the binding constraint at each scale. This is low-hanging fruit that would significantly increase the paper's analytical depth.

4. **Add intermediate-scale simulation points.** The current seven scale points ($10^3$ to $10^6$) are too sparse to characterize the superlinear transition. Adding runs at $N \in \{20\text{k}, 30\text{k}, 40\text{k}, 60\text{k}, 80\text{k}\}$ with the same Monte Carlo methodology would enable formal change-point analysis and either confirm the superlinear onset as a robust finding or reveal it as a parameterization artifact.

5. **Quantify the three optimizations individually.** Run the DES with each optimization enabled separately and in pairwise combinations, reporting the overhead reduction attributable to each. This factorial analysis would transform Section IV-D from a qualitative discussion into a rigorous design trade study, and would identify which optimization provides the greatest benefit at each scale—information directly useful to system designers.