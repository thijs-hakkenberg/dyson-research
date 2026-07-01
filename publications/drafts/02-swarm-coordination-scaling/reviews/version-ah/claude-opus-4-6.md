---
paper: "02-swarm-coordination-scaling"
version: "ah"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-27"
recommendation: "Major Revision"
---

# Peer Review: "Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study"

**Manuscript Version:** AH
**Venue:** IEEE Transactions on Aerospace and Electronic Systems

---

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a genuinely important problem: how to coordinate autonomous spacecraft swarms at scales of 10³–10⁵ nodes. The gap identified—the absence of systematic byte-level traffic accounting for hierarchical coordination at these scales—is real, and the framing around mega-constellation growth (Starlink, Kuiper) is timely. The four headline contributions (coordinator capacity sizing, AoI characterization, GE correlated loss analysis, and joint independence verification) are each useful engineering inputs for system designers.

However, the novelty is more limited than the paper initially suggests. The authors commendably acknowledge throughout that individual metrics are "analytically tractable in isolation" and that the $O(1)$ overhead scaling is "a direct mathematical consequence of the hierarchical structure." The DES confirms closed-form predictions to within 0.1% (Table VII), and the Monte Carlo variance is SD < 0.001%. This raises a fundamental question: what does the simulation discover that the analytical models do not? The authors' answer—joint independence verification (Section IV-D)—is the strongest novel contribution, but it is a negative result (the factors *don't* interact under point-to-point ISLs), and the architectural condition under which it holds (per-link loss, no shared medium) makes the independence almost self-evident from the model structure. The paper would benefit from more clearly positioning itself as a *design reference* rather than a discovery paper.

The comparison with a "realistically provisioned centralized baseline" ($c = N/k_c$) that doesn't diverge until $N \approx 10^6$ significantly undermines the motivation for hierarchical coordination on processing grounds. The authors handle this honestly (the advantage is "fault tolerance and spectrum independence, not processing scalability"), but this admission weakens the paper's impact. The reader is left wondering whether the hierarchical architecture solves a problem that doesn't yet exist at the studied scales.

---

## 2. Methodological Soundness

**Rating: 3 (Adequate)**

The cycle-aggregated DES framework is clearly described and the abstraction level is well-justified for the research questions. The message-layer accounting is meticulous: Table V enumerates all message types, Table IV provides per-node bandwidth breakdowns, and the distinction between offered and delivered overhead is carefully maintained. The analytical cross-checks (Pollaczek-Khinchine for M/D/1, geometric distribution for AoI, Chernoff bound for burstiness) are appropriate and well-executed.

Several methodological concerns warrant attention:

**Near-deterministic simulation.** The SD < 0.001% across 30 replications (Section III-D) indicates the simulation is essentially deterministic for overhead metrics. The 2%/year failure rate perturbs negligibly few nodes per cycle. The authors acknowledge this ("the MC framework serves primarily to confirm this low-variance property"), but this raises the question of whether 30 Monte Carlo replications are scientifically meaningful or merely performative. The simulation is effectively computing a closed-form expression iteratively. The stochastic elements that *would* matter—MAC contention, correlated failures, orbital geometry-driven link intermittency—are precisely the phenomena abstracted away.

**Coordinator link model independence.** The joint independence result (Section IV-D, Table VI) follows almost tautologically from the model architecture: GE losses occur *before* messages reach the coordinator queue, so lost messages never contend for ingress capacity. The authors acknowledge this ("lost messages never contend for coordinator capacity"), but then claim the DES is needed to verify it. A one-paragraph argument about the event ordering would suffice; the 6-point capacity sweep adds little beyond confirming the obvious. The result would be genuinely interesting under shared-medium contention, which the authors correctly identify as future work.

**Sectorized mesh parameterization.** The $k_s = \lceil\sqrt{N}\rceil$ sector size is derived from a heuristic orbital density argument (Section III-B.4) that the authors themselves call "an order-of-magnitude sizing, not a precise orbital mechanics calculation." The capped fanout of 10 neighbors is a design parameter whose adequacy for conjunction screening is unknown without orbital geometry modeling. The sectorized mesh comparison is therefore illustrative rather than definitive.

**Validation scope.** The M/D/1 validation at $N = 100$ (Section III-A) and gossip convergence at $N \leq 1{,}000$ are necessary but insufficient. No validation is performed at the scales where the paper claims its primary contributions ($N = 10^4$–$10^5$). The authors list packet-level validation via NS-3/OMNeT++ as future work (Section V-A, item 2), which is appropriate, but the absence of any physical-layer grounding beyond the TDMA vignette (Section IV-A) limits the practical applicability of the results.

---

## 3. Validity & Logic

**Rating: 4 (Good)**

The paper's conclusions are generally well-supported by the analysis, and the authors are admirably transparent about limitations. Several specific aspects deserve comment:

**Strengths in logical rigor.** The dual-regime interpretation (Section IV-F.3) is excellent: the observation that $\eta = 46\%$ is binding only at 1 kbps (RF backup) and drops to 0.46% at 100 kbps (optical ISL) properly contextualizes the results. The workload decomposition (Section IV-E, Fig. 6) convincingly demonstrates that the headline 46% overhead is dominated by the stress-case command workload assumption, not the architecture. The AoI analytical cross-check (Eq. 12 vs. Table III) is clean and the match to within one cycle is convincing.

**The centralized baseline comparison is handled with intellectual honesty** but creates a logical tension. If $c = N/k_c$ centralized servers handle the load until $N \approx 10^6$, and the studied range is $10^3$–$10^5$, then the hierarchical architecture's advantages (fault tolerance, spectrum independence) are qualitative rather than quantitative within the paper's scope. The paper would be strengthened by either (a) extending the analysis to $10^6$ where the centralized baseline actually diverges, or (b) more explicitly quantifying the fault tolerance and spectrum advantages rather than listing them as bullet points.

**The GE loss analysis** (Section IV-C) is sound but the operational implications could be stronger. The finding that intra-cycle retransmission recovers only 27% during bad-state bursts is useful, but the paper defers the inter-cycle recovery characterization to future work. Without this, the reader cannot assess whether the hierarchical architecture is *viable* under realistic LEO link conditions—only that it is *insufficient* with intra-cycle retry alone.

**One logical gap:** The paper claims the DES "tests joint parameter interactions that analytical models cannot address without independence assumptions" (Section I-D), but the tested interaction (GE × coordinator capacity) turns out to be independent by construction. The paper would be more honest to say the DES *confirms* that the model structure produces independence, rather than implying it discovered something unexpected.

---

## 4. Clarity & Structure

**Rating: 3 (Adequate)**

The paper is technically precise but suffers from excessive length and repetition. At approximately 12,000 words of body text plus extensive tables, it substantially exceeds typical IEEE T-AES page limits. The "Version AH" designation suggests extensive revision history, and the manuscript reads as if material has been accumulated rather than curated.

**Structural issues:**
- The abstract is dense but accurate. However, at ~250 words it pushes IEEE limits and could be tightened.
- Section III (Simulation Framework) is disproportionately long (~40% of the paper). The sectorized mesh model (Section III-B.4) alone spans nearly two columns with three tables. Much of this could be condensed or moved to an appendix.
- The "Roadmap" paragraph at the start of Section IV is helpful but suggests the results section needs better self-organization.
- Key results are scattered across many tables (Tables I–XI) and figures (Figs. 1–12), making it difficult to extract the headline findings without reading the entire paper.

**Positive clarity elements:**
- Table II (Simulation Abstraction Scope) is an excellent addition that clearly delineates what is and isn't modeled.
- The traffic accounting tables (Tables IV, V) provide full reproducibility.
- The design equations summary (Section V-C) is a valuable practitioner-oriented contribution.
- Footnotes throughout are used effectively to clarify parameter choices.

**Repetition:** The 46% overhead figure is stated at least 15 times. The "message-layer estimate; multiply by $1/\gamma$" caveat appears in the abstract, Section I-D, Section III-F, Section IV-F, and the conclusion. While important, this could be stated once prominently and referenced thereafter.

---

## 5. Ethical Compliance

**Rating: 4 (Good)**

The paper includes an appropriate acknowledgment of AI-assisted ideation (Claude 4.6, Gemini 3 Pro, GPT-5.2) in the Acknowledgment section, with a clear statement that the AI-generated concepts "are not validated in the current study." The companion methodology paper [52] is referenced. This level of disclosure meets current IEEE guidelines.

The anonymous authorship ("Project Dyson Research Team") with a note that "individual author names and affiliations will be provided for final publication per IEEE policy" is acceptable for review but must be resolved before publication. The data availability statement with a specific repository tag (`paper-02-v-ah`) supports reproducibility.

One minor concern: the reference to future AI model versions (Claude 4.6, GPT-5.2) that do not exist as of mid-2025 suggests either the paper is set in a near-future context or these are placeholder names. This should be clarified to avoid confusion about the provenance of the work.

---

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is appropriate for IEEE T-AES in scope, addressing autonomous spacecraft coordination with quantitative engineering analysis. The reference list (55 items) is comprehensive and spans the relevant domains: constellation operations, swarm robotics, queueing theory, distributed systems, and space communication standards.

**Reference quality concerns:**
- Several references are non-archival web pages (SpaceX [1], Amazon [3], DARPA [19, 24], DoD [21]) that may not persist. While unavoidable for some operational programs, the paper relies on these for motivational claims about constellation scale.
- Reference [22] (NRL) is described as a "magazine article, non-peer-reviewed" in the bibliography—this candor is appreciated but the reference should be replaced with a peer-reviewed source if available.
- The companion methodology paper [52] is self-published on the project website and not peer-reviewed. Its citation for AI methodology is acceptable but should not be relied upon for technical claims.
- Missing references: the paper does not cite recent work on distributed satellite autonomy from the SmallSat community (e.g., Nag & Ravichandran on autonomous constellation management, or the ESA OPS-SAT experiments on onboard autonomy). The DTN/BPv7 discussion would benefit from citing the Interplanetary Overlay Network (ION) implementation results.

**Scope concern:** The paper's title promises "Large Autonomous Space Swarms" but the validated range is $10^3$–$10^5$ nodes. The $10^6$ extrapolation is analytical only (Fig. 9 dashed line). The Dyson swarm reference in the introduction (and the project name) sets expectations for scales far beyond what is studied. The title should be moderated or the extrapolation validated.

---

## Major Issues

1. **Limited simulation value beyond analytics.** The DES confirms closed-form predictions to within 0.1% for overhead and within one cycle for AoI. The joint independence result (Section IV-D) is the primary DES-specific contribution, but it follows from the model structure (per-link loss before coordinator queue). The paper needs to either (a) identify genuinely emergent behaviors that the DES reveals beyond analytical prediction, or (b) reposition the contribution as a validated design reference tool rather than a simulation study that discovers new phenomena. Currently, the paper oscillates between these framings.

2. **Absence of physical-layer validation.** All results are message-layer estimates with a $1/\gamma$ correction factor. The TDMA vignette (Section IV-A) is a welcome addition but covers only a single cluster at 500 km diameter. No packet-level simulation, hardware-in-the-loop test, or comparison with operational ISL data is provided. For a journal paper in T-AES (which serves a hardware-oriented community), this abstraction gap is significant. At minimum, the authors should provide a more detailed link budget analysis for representative orbital geometries and discuss how MAC-layer effects (hidden terminals, half-duplex constraints, link acquisition latency) would modify the headline results.

3. **Centralized baseline undermines motivation.** The realistic centralized baseline ($c = N/k_c$) handles the studied scale range without divergence. The paper's honest acknowledgment that "processing scalability is not the hierarchical architecture's advantage" is commendable but leaves the reader without a compelling quantitative case for the hierarchical architecture within the studied range. The fault tolerance and spectrum independence advantages are asserted but not quantified with the same rigor as the overhead metrics.

4. **Incomplete GE loss characterization.** The finding that intra-cycle retransmission is "structurally ineffective" during correlated bursts (Section IV-C) is important, but the paper defers inter-cycle recovery to future work. This leaves the most operationally relevant question unanswered: can the hierarchical architecture maintain acceptable coordination quality under realistic LEO link conditions? The paper should either include a basic inter-cycle recovery analysis or more clearly bound the operational implications of the 27% recovery rate.

---

## Minor Issues

1. **Eq. 4 convergence rounds formula:** $R_{\text{conv}} = \max(\lceil\log_2 N\rceil, \lceil N/(bf)\rceil)$ conflates two different convergence mechanisms (epidemic spread vs. throughput-limited delivery). The transition between regimes deserves a sentence of explanation.

2. **Table III (AoI results):** The "Max AoI" column at $p_{\text{exc}} = 0.10$ shows 780 s, but the geometric distribution has unbounded support. Clarify whether this is the maximum observed across 30 replications or a theoretical bound.

3. **Section III-B.4, Eq. 7:** The sector overhead formula $B_{\text{sector}}^{\text{capped}} = 256 + \min(k_s - 1, 10) \times 32$ omits the 512-byte command traffic that is included in the $\eta_{\text{sector}}$ calculation in Table VIII footnote. This inconsistency should be resolved.

4. **Table I (M/D/c sensitivity):** The "Representative System" column labels are informal (e.g., "Hyperscale data center"). These should either be tied to specific published system capacities or removed.

5. **Section IV-A, Chernoff bound (Eq. 9):** The notation $\alpha p$ in $D_{\text{KL}}(\alpha p \| p)$ is used without defining whether this is the KL divergence between Bernoulli parameters or distributions. Clarify.

6. **Figure references:** Several figures (Figs. 1, 3–12) reference PDF files that are not included in the submission. The review assumes these exist and match the descriptions.

7. **Section III-A:** "one-second resolution applies only to collision avoidance events"—but the collision avoidance rate is $10^{-4}$/node/s, meaning most cycles have zero such events. The 1-second resolution is therefore rarely exercised; this should be noted.

8. **Inconsistent notation:** $p_{\text{link}}$ is used both as link availability (Table X) and link success probability. In the GE model, the steady-state availability is 80% but $p_{\text{link}}$ is not explicitly mapped to the GE parameters. Clarify the relationship.

9. **Section I-A:** "the system already requires substantial ground infrastructure and has encountered coordination challenges during conjunction events [2]"—Reference [2] (Flohrer et al. 2017) predates the current Starlink constellation and discusses ESA conjunction assessment, not Starlink-specific challenges. This citation does not support the specific claim.

10. **Typo/formatting:** In Table III, the footnote marker "a" for "Periodic baseline" appears in the table but the footnote text uses a different marker style than other tables.

---

## Overall Recommendation

**Major Revision**

This paper addresses an important problem with meticulous engineering analysis and commendable transparency about limitations. The traffic accounting framework, coordinator capacity sizing, and AoI characterization are useful contributions to the space systems design community. However, the paper's primary methodological tool (the DES) adds limited value beyond confirming analytical predictions, the physical-layer abstraction gap is significant for a T-AES audience, and the centralized baseline comparison undermines the motivation for the studied architecture within the validated scale range. The paper is also substantially too long and repetitive. A major revision should: (1) sharpen the contribution framing around the design reference tool rather than simulation discovery, (2) add at least a basic inter-cycle recovery analysis for GE losses, (3) quantify the fault tolerance advantage rather than asserting it, and (4) reduce length by ~30% through consolidation of repetitive material and moving detailed sectorized mesh analysis to supplementary material.

---

## Constructive Suggestions

1. **Quantify the fault tolerance advantage.** The paper repeatedly states that hierarchical coordination's advantage is fault tolerance, not processing scalability. Dedicate a subsection to quantifying this: simulate correlated ground station outages (duration, frequency) and measure coordination degradation for centralized vs. hierarchical architectures. This would provide the missing quantitative justification for the hierarchical approach and directly address the "why not just use centralized?" question that the realistic baseline raises.

2. **Include basic inter-cycle store-and-forward recovery.** The GE loss analysis (Section IV-C) identifies the problem but defers the solution. Even a simplified carry-forward model (buffer missed reports, retry next cycle, track cumulative recovery over 2–10 cycles) would substantially strengthen the paper by answering whether the hierarchical architecture is viable under realistic link conditions. The analytical framework for this is straightforward (geometric series on per-cycle recovery probability).

3. **Consolidate and shorten.** Target a 30% reduction. Specific candidates: (a) merge Tables VII and IX into a single scaling verification table; (b) move the full sectorized mesh derivation (Section III-B.4, Tables V–VIII) to an appendix, retaining only the comparison result; (c) eliminate repeated statements of the $1/\gamma$ caveat after the first prominent occurrence; (d) combine the workload profiles (Section IV-E) with the command-rate sweep (Fig. 7) into a single concise subsection.

4. **Add a single-cluster packet-level comparison.** Even a simplified NS-3 or analytical MAC model for one 100-node cluster with TDMA scheduling would ground the $\gamma$ assumption and significantly strengthen the paper's credibility with the T-AES hardware-oriented readership. This need not cover the full parameter space—a single validation point at $k_c = 100$ with realistic ISL parameters would suffice.

5. **Reframe the DES contribution explicitly.** Rather than claiming the DES "validates compositional use of single-factor design equations," acknowledge that the model structure makes independence expected and position the DES as a *reference implementation* that (a) provides a reproducible parametric design tool, (b) confirms analytical predictions under full joint conditions as a sanity check, and (c) serves as a foundation for future extensions (MAC contention, correlated failures, orbital geometry) where analytical tractability breaks down. This honest framing would be more convincing than the current implicit claim of emergent discovery.