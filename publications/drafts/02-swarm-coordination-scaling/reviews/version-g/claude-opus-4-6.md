---
paper: "02-swarm-coordination-scaling"
version: "g"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-23"
recommendation: "Major Revision"
---



# Peer Review: "Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study"

## IEEE Transactions on Aerospace and Electronic Systems

---

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a genuine gap in the literature: the systematic quantitative comparison of coordination architectures across the $10^3$–$10^6$ node range for autonomous space systems. The authors correctly identify that swarm robotics literature rarely exceeds ~1,000 agents and constellation management literature rarely exceeds ~10,000 nodes, leaving the intermediate regime largely unexplored. The identification of a superlinear scaling transition near $N^* \approx 45{,}000$ nodes, supported by formal model comparison with AIC selection, is a useful contribution that could inform architectural decisions for mega-constellation operators.

However, the novelty is tempered by several factors. The core finding—that hierarchical architectures scale better than centralized or fully-connected mesh topologies—is well-established in distributed systems theory (as the authors themselves acknowledge, citing Lynch [7]). The $O(N)$ vs. $O(N^2)$ comparison is an elementary consequence of the topology choices, and the paper's primary contribution is quantifying the constants and identifying the transition point rather than discovering a new architectural principle. The comparison is further weakened by the authors' own admission (Section I-C) that the two baselines are "intentional bounds, not realistic competitors." The most interesting practical alternative—a sectorized mesh—is explicitly deferred to future work (Section V-C), which significantly limits the actionable value of the comparison. The paper would be substantially more impactful if it included at least one realistic competitor architecture rather than only bounding cases.

The applicability claims (mega-constellations, drone swarms, IoT, autonomous vehicles) in Section V-A are reasonable but somewhat superficial. The connection to Starlink's 42,000-satellite expansion is compelling, but the paper does not model any Starlink-specific constraints (orbital shell geometry, laser ISL topology, ground station distribution), making the practical recommendations speculative.

---

## 2. Methodological Soundness

**Rating: 2 (Needs Improvement)**

The DES framework is described in reasonable detail, and the Monte Carlo approach with 50–100 runs per configuration and bootstrap confidence intervals is appropriate. The validation against closed-form $M/D/1$ solutions (Section III-A) and gossip convergence bounds provides some confidence in the implementation. The formal model comparison using AIC (Section IV-D) is a welcome addition that strengthens the superlinear transition claim.

However, several methodological concerns are significant:

**Abstraction level.** The simulation abstracts away essentially all physical-layer and orbital mechanics effects. There is no orbital propagation, no Earth occlusion geometry, no realistic ISL contact schedule, no antenna pointing model, no Doppler compensation, and no MAC-layer contention. The Bernoulli link availability analysis (Section IV-F) is a step in the right direction but is extremely coarse—real link intermittency is highly correlated (Earth occlusion creates deterministic, periodic outages lasting minutes, not independent per-message Bernoulli losses). The authors acknowledge this in Section V-E but the gap between the simulation model and physical reality is large enough to question whether the quantitative results (specific overhead percentages, specific transition points) would survive a higher-fidelity simulation. The 1.5–3× overhead multiplier acknowledged for unmodeled physical-layer effects is itself a rough estimate.

**Coordinator bandwidth assumption.** The resolution of the coordinator bandwidth bottleneck (Section III-F, where the coordinator uses the "combined coordination bandwidth of its cluster") is physically hand-waved. The claim that "the aggregate spectral allocation for the cluster is shared rather than rigidly partitioned per-node" assumes a TDMA or FDMA scheme that is never specified. In practice, $k_c = 100$ nodes sharing a coordination channel to a single coordinator creates a multiple-access problem that is non-trivial, especially with the 1 kbps per-node allocation. This is not merely a detail—it is central to the overhead accounting.

**Collision avoidance rate.** The $10^{-4}$/node/s rate is justified as a "proximity monitoring" rate rather than a maneuver rate, with a claimed 1,000:1 screening-to-maneuver ratio. While the footnote in Table II provides some justification, this rate is a critical parameter that drives a significant fraction of the coordination traffic, and the 1,000:1 ratio is not well-sourced. The sensitivity analysis varying this rate from $10^{-5}$ to $10^{-3}$ is appreciated but reported only in prose without tabulated results.

**Exception-based telemetry validation.** The DES validation at a single point ($N = 10^4$, $p_{\text{exc}} = 0.30$) is insufficient to validate the optimization across the full range. The Bernoulli model for exception events is a significant simplification—in reality, deviation probabilities are correlated across nearby nodes (e.g., after a maneuver or perturbation event) and vary with orbital regime. The claim that this provides a "credibility anchor" for the full projected optimization curve overstates the strength of a single-point validation.

**Reproducibility.** The data availability statement references a GitHub repository with a pending commit hash, which is appropriate for a manuscript but must be resolved before publication. The Python implementation details are sparse—no mention of the DES engine (SimPy? custom?), data structures for the priority queue, or memory management for $10^6$-node configurations.

---

## 3. Validity & Logic

**Rating: 3 (Adequate)**

The paper is generally careful about qualifying its claims, and the extensive discussion of limitations (Section V-E) and the baseline interpretation note (Section I-C) demonstrate intellectual honesty. The distinction between DES-measured and analytically projected results (Table V) is clearly maintained throughout. The formal model comparison for the superlinear transition is well-executed, and the per-tier message decomposition (Fig. 7) provides convincing mechanistic support for the transition.

Several logical concerns merit attention:

**Circular reasoning in mesh overhead.** The $O(N^2)$ mesh overhead is derived from the assumption that every node must maintain full fleet state for collision avoidance (Section III-B-3). However, the hierarchical architecture explicitly does *not* provide full fleet state to every node—it provides aggregated summaries. The paper acknowledges this asymmetry (Table III) but then compares the overhead of these architectures as if they provide equivalent coordination capability. The statement that "the hierarchical architecture achieves global coordination through aggregated state" conflates two different levels of coordination quality. If aggregated state is sufficient for collision avoidance, then the mesh doesn't need $O(N^2)$ overhead either (it could use aggregated gossip). If full state is truly necessary, then the hierarchical architecture is not providing it. This logical tension undermines the fairness of the comparison.

**Superlinear transition mechanism.** The paper attributes the superlinear transition to "inter-cluster coordination traffic between cluster and regional coordinators" growing faster than linearly. But with a fixed four-level hierarchy and fixed $k_c = 100$, the number of cluster coordinators is $N/100$, the number of regional coordinators is $N/10{,}000$, and the message counts at each level are strictly $O(N)$. The paper needs to explain more precisely *which* inter-cluster messages grow superlinearly and *why*. The per-tier decomposition (Fig. 7) shows inter-cluster traffic growing, but the mechanism is not clearly articulated. Is it cross-cluster collision avoidance? Regional coordinator reconciliation? Without this, the superlinear transition could be an artifact of the simulation parameterization rather than a fundamental architectural property.

**Projected optimizations.** The analytically projected curve combining three optimizations (Fig. 5) is presented prominently but only one of the three has any DES validation, and that at a single point. The projected 5.1% overhead at $10^6$ nodes is a central claim of the paper but rests on unvalidated analytical estimates. The paper should more clearly flag this as speculative.

**Link availability analysis interpretation.** The finding that hierarchical architectures are "disproportionately sensitive to coordinator link intermittency" (Section IV-F) is important but somewhat undermines the paper's main thesis. The paper argues this is acceptable because operational LEO ISL availability is 0.85–0.95, but this figure applies to *established* links—it does not account for the fact that coordinator nodes must maintain links to *all* cluster members simultaneously, which is a much more demanding requirement.

---

## 4. Clarity & Structure

**Rating: 4 (Good)**

The paper is well-organized and generally well-written. The four-level structure (Introduction → Framework → Results → Discussion) is logical, and the progressive disclosure of complexity (baselines first, then hierarchical optimization, then sensitivity analysis) aids comprehension. The abstract is detailed and accurate, though at 280+ words it is long for IEEE T-AES (typically 150–200 words). The baseline interpretation note (Section I-C) is an excellent structural choice that preempts misinterpretation.

Tables and figures are generally effective. Table I ($M/D/c$ sensitivity) clearly communicates the parallelization argument. Table V (scaling trajectory) is the central results table and is well-constructed with clear labeling of DES vs. projected values. The traffic accounting table (Table IV) and metric definitions (Section III-G) demonstrate commendable rigor in ensuring reproducibility of the overhead metric.

Some clarity issues:

- The paper is very long (~12,000 words excluding references), which is at the upper limit for IEEE T-AES. Some material could be condensed—particularly the related work section (Section II), which at ~1,500 words covers many tangentially related topics (bio-inspired optimization, mean-field games) that don't directly inform the simulation design.
- The notation is occasionally inconsistent: $O_{\text{protocol}}$ in tables vs. $\eta$ in the text and metric definitions. Standardizing on one symbol would improve readability.
- Section III-B-2 on the hierarchical topology is extremely dense, mixing queueing model specification, U-shape explanation, and handoff mechanics in a single subsection. Breaking this into sub-subsections would help.
- The collision avoidance rate justification is split between Table II footnote and a separate paragraph below the table, making it hard to find.

---

## 5. Ethical Compliance

**Rating: 4 (Good)**

The paper includes an appropriate acknowledgment of AI-assisted ideation (Claude 4.6, Gemini 3 Pro, GPT-5.2) in the Acknowledgment section, with a clear statement that the AI-generated concepts are "not validated in the current study." This is transparent and appropriate. The reference to a companion methodology paper [42] provides an audit trail.

The anonymous authorship ("Project Dyson Research Team") with a note about final publication is unusual but acceptable for review. The data availability statement with a GitHub repository link demonstrates commitment to open science, though the pending commit hash must be resolved.

One concern: the paper references future AI model versions (Claude 4.6, GPT-5.2) that do not exist as of the review date, suggesting either the paper is set in a near-future context or these are placeholder names. This should be clarified—if the AI tools used are current models, they should be accurately named.

The dual-use implications of the military drone swarm discussion (Section V-A) are not addressed but are arguably outside the scope of a technical architecture paper.

---

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is appropriate for IEEE T-AES in topic, though the level of abstraction (no orbital mechanics, no realistic link budgets, no hardware-in-the-loop validation) places it closer to a distributed systems paper than a traditional aerospace engineering paper. The journal's readership would benefit from more aerospace-specific content—realistic orbital geometry, link budget calculations, or at minimum a worked example with a specific constellation design.

The reference list (48 citations) is comprehensive and covers the relevant literature well. The inclusion of Olfati-Saber & Murray, Ren & Beard, Lamport, and Ongaro & Ousterhout demonstrates familiarity with the distributed systems foundations. The constellation management references (Starlink, Kuiper, OneWeb, Iridium) are appropriate. The CCSDS standards references (Prox-1, BPv7) add aerospace credibility.

Several referencing concerns:

- Multiple references are non-archival web pages (SpaceX [1], Amazon [3], DARPA [20, 37], DoD [22], Google S2 [33], Project Dyson [42]). While some are unavoidable (corporate web pages), the ratio of non-archival to archival references is high for a journal paper. At least 8 of 48 references are non-archival.
- The NRL swarm reference [21] is explicitly noted as "magazine article, non-peer-reviewed"—this should either be replaced with a peer-reviewed source or removed.
- The ESA Space Environment Report [48] is a technical report, which is acceptable but should include the full document identifier.
- Missing key references: The paper does not cite any work on space traffic management (STM) standards or frameworks, which is directly relevant to the collision avoidance coordination problem. The IADC Space Debris Mitigation Guidelines and the emerging STM standards from CONFERS or the Space Safety Coalition would strengthen the aerospace context. Additionally, no reference to actual ISL performance data (e.g., from EDRS or Starlink's laser ISL measurements) is provided.

---

## Major Issues

1. **Unfair baseline comparison undermines central claims.** The paper's primary comparison is between the hierarchical architecture and two intentionally extreme baselines (single-server centralized, full-state mesh). The authors acknowledge this but the paper's structure and abstract still frame the results as demonstrating hierarchical superiority. The most relevant comparison—against a sectorized mesh or a parallelized centralized system with ISL-based local autonomy—is explicitly deferred. This is the single most significant weakness: the paper demonstrates that a reasonable architecture outperforms unreasonable ones, which is not a strong contribution. **Recommendation:** Either (a) include a sectorized mesh simulation, even at reduced scale, or (b) substantially reframe the contribution as "characterizing hierarchical scaling properties" rather than "demonstrating hierarchical superiority," removing comparative language from the abstract and conclusions.

2. **Physical-layer abstraction too severe for quantitative claims.** The specific overhead percentages (1.8%, 6.2%, 12.8%) and the specific transition point ($N^* = 45{,}000$) are presented with a precision that the simulation fidelity does not support. The acknowledged 1.5–3× overhead multiplier for unmodeled physical-layer effects means the true overhead could be 2.7%–5.4% at $10^3$ nodes and 19.2%–38.4% at $10^6$ nodes. The Bernoulli link model does not capture correlated outages (Earth occlusion), deterministic contact schedules, or MAC-layer effects. **Recommendation:** Either (a) incorporate at least a simplified orbital geometry model with deterministic Earth occlusion periods and realistic ISL contact schedules, or (b) present all quantitative results as ranges reflecting the physical-layer uncertainty, and qualify the transition point as approximate.

3. **Superlinear transition mechanism insufficiently explained.** The paper claims a superlinear transition but does not provide a clear analytical explanation for why a fixed four-level hierarchy with $O(N)$ theoretical complexity exhibits superlinear scaling in practice. The per-tier decomposition shows *that* inter-cluster traffic grows, but not *why* it grows faster than linearly when the number of inter-cluster messages should be $N/k_c = O(N)$. Is there an implicit cross-cluster coordination mechanism (e.g., for collision avoidance between nodes in different clusters) that is not captured in Eq. 4? If so, this must be explicitly modeled and its complexity analyzed. **Recommendation:** Provide a detailed analytical derivation of the inter-cluster message count as a function of $N$, identifying the specific mechanism that produces superlinear growth, and verify this against the DES message logs.

4. **Projected optimizations lack sufficient validation.** Two of three projected optimizations (dynamic spatial partitioning, heterogeneous hardware) have zero DES validation. The single-point validation of exception-based telemetry ($N = 10^4$, one value of $p_{\text{exc}}$) is insufficient to support the projected curve across three orders of magnitude. The prominent display of the projected curve in Fig. 5 and the 5.1% figure in the abstract risk misleading readers about the confidence level of these projections. **Recommendation:** Either (a) implement at least one additional optimization in DES and validate across multiple scale points, or (b) remove the projected curve from the main results and relegate it to a clearly-labeled "future directions" discussion, removing the 5.1% figure from the abstract.

---

## Minor Issues

1. **Abstract length.** At ~280 words, the abstract exceeds typical IEEE T-AES guidelines. Consider condensing to ~200 words by removing implementation details (e.g., the specific AIC comparison, the exception-based telemetry validation details).

2. **Notation inconsistency.** Protocol overhead is denoted $O_{\text{protocol}}$ in Tables I, III, V but $\eta$ in Section III-G and Table VI. Standardize throughout.

3. **Table V vs. Table III discrepancy.** The text notes these tables use different cluster sizes (fixed $k_c = 100$ vs. optimized), but this is easy to miss. Consider adding a column header or footnote to each table explicitly stating the cluster size used.

4. **Eq. 5 derivation.** The mesh fanout $f = O(N/\log N)$ is stated but the derivation is compressed into a single sentence. A brief appendix or expanded inline derivation would help readers unfamiliar with gossip protocol analysis.

5. **Fig. 1 reference.** The architecture diagram (Fig. 1) is referenced but described as a PDF file that is not included in the submission. All figures must be provided for review.

6. **Section III-E, Monte Carlo runs.** "50–100 independent runs per configuration" with "100 for $N \geq 10^5$" is stated, but the rationale for the variable number of runs is not given. Why not 100 for all configurations?

7. **Power budget analysis (Section IV-G).** The 3% average power overhead calculation assumes uniform rotation probability. In practice, nodes with better link geometry to the regional coordinator would be preferred as coordinators, creating non-uniform duty distributions. This should be noted.

8. **Typo/formatting.** Section IV-D: "30,000 and 60,000 nodes" uses comma-separated thousands inconsistently with the rest of the paper, which uses thin spaces (e.g., "10,000" vs. "10{,}000" in LaTeX).

9. **Reference [42] (companion paper).** Self-citation to an unpublished companion paper hosted on the project website is weak. If this paper is under review elsewhere, state so; if not, the reference should be removed or replaced.

10. **Coordinator failure model.** Table II states "Coordinator failure: Same as node; No enhanced reliability." This is inconsistent with the heterogeneous hardware optimization proposed in Section IV-D, which envisions dedicated coordinator spacecraft. The baseline model should be clearly distinguished from the proposed optimization.

11. **Section III-B-3, "conjunction cascades."** The claim that avoidance maneuvers create "secondary conjunction risks for distant nodes" is physically plausible but unsourced. A reference to conjunction cascade analysis in the space debris literature would strengthen this argument.

---

## Overall Recommendation

**Major Revision**

The paper addresses a relevant and timely problem—scaling coordination architectures for mega-constellations and large autonomous space swarms—and demonstrates competent simulation methodology with appropriate statistical treatment. The identification of the superlinear transition and the formal model comparison are genuine contributions. However, the paper suffers from three fundamental weaknesses that preclude acceptance in its current form: (1) the comparison against only extreme-case baselines rather than realistic alternatives limits the practical value of the findings; (2) the physical-layer abstraction is too severe to support the quantitative precision with which results are presented; and (3) the superlinear transition mechanism is observed but not adequately explained analytically. A major revision addressing these issues—particularly the inclusion of a sectorized mesh comparison and a clearer analytical explanation of the superlinear mechanism—would substantially strengthen the contribution.

---

## Constructive Suggestions

1. **Add a sectorized mesh simulation.** Even a simplified version (e.g., orbital shell divided into $\sqrt{N}$ sectors with intra-sector gossip and inter-sector aggregation) would transform the paper from "hierarchical beats strawmen" to "hierarchical vs. practical decentralized alternative." This is the single highest-impact addition. The analytical framework in Section V-C already outlines the approach; implementing it in the existing DES framework should be tractable.

2. **Incorporate simplified orbital geometry.** Replace the abstract link model with a Walker constellation geometry (e.g., 72 planes × 22 satellites/plane for a Starlink-like shell). Model Earth occlusion as deterministic periodic outages rather than Bernoulli losses. This would dramatically increase the paper's credibility with the aerospace audience and would likely reveal interesting effects (e.g., coordinator handoff timing relative to orbital period, cross-plane coordination challenges) that the current model cannot capture.

3. **Derive the superlinear mechanism analytically.** Instrument the DES to log *every* inter-cluster message type and identify which specific message category grows superlinearly. Then derive an analytical expression for that category's scaling (e.g., if cross-cluster collision screening scales as $O((N/k_c)^2)$ due to pairwise cluster interactions, state this explicitly and verify). This would transform the superlinear transition from an empirical observation to an explained phenomenon.

4. **Validate exception-based telemetry across multiple scales.** Extend the DES validation from the single point ($N = 10^4$) to at least $N \in \{10^4, 10^5, 5 \times 10^5\}$ with multiple values of $p_{\text{exc}}$. This is computationally inexpensive relative to the full Monte Carlo campaign and would substantially strengthen the projected optimization curve.

5. **Tighten the scope and shorten the paper.** The related work section could be reduced by ~40% by focusing on directly relevant work (constellation management, hierarchical distributed systems) and cutting tangential topics (bio-inspired optimization, mean-field games, military programs). The discussion of terrestrial analogies (Section V-B) could be condensed to a single paragraph. This would bring the paper closer to the typical IEEE T-AES length and sharpen the contribution.