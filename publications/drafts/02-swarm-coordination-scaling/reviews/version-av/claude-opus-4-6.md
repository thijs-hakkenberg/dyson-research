---
paper: "02-swarm-coordination-scaling"
version: "av"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-27"
recommendation: "Major Revision"
---



# Peer Review: "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms"

**Manuscript Version:** AV
**Venue:** IEEE Transactions on Aerospace and Electronic Systems

---

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a genuine gap: there is no published, systematic byte-level traffic accounting framework for comparing coordination architectures at the $10^3$–$10^5$ node scale. The authors correctly identify that swarm robotics literature operates at 10–100 agents, constellation management at ~10,000, and networking literature treats routing without coordination overhead accounting. The "practitioner toolkit" framing—closed-form design equations for coordinator ingress, AoI, and correlated loss recovery—is a useful contribution concept.

However, the novelty is more modest than the presentation suggests. The individual analytical results are standard: the AoI P99 formula (Eq. 12) is a direct geometric quantile; the GE recovery analysis is a textbook two-state Markov chain; the coordinator ingress sizing is elementary throughput accounting; and the $M/D/c$ queueing model is classical. The paper's contribution is the *assembly* of these known results into a specific parametric context, not the derivation of new theory. This is acknowledged in the abstract ("assembling standard queueing, geometric, and Markov-chain results") but the title's "Design Equations" framing implies more analytical depth than is delivered. The pipeline decoupling observation (Section IV-D) is presented as a key finding but is architecturally obvious for point-to-point links—losses upstream of a queue cannot affect queue occupancy.

The practical relevance is also somewhat limited by the operating regime: the 1 kbps RF-backup budget applies to <1% of operational time. The paper is essentially sizing a degraded-mode fallback channel. While this is a valid engineering exercise, the impact is narrower than the abstract's framing of "hierarchical coordination in large autonomous space swarms" suggests. The paper would benefit from more clearly positioning itself as a degraded-mode sizing study rather than a general coordination architecture paper.

## 2. Methodological Soundness

**Rating: 3 (Adequate)**

The cycle-aggregated DES approach is appropriate for the message-layer accounting objective, and the authors are commendably transparent about what is and is not modeled (Table VI). The Monte Carlo configuration (30 replications, bootstrap CIs) is adequate for the overhead metrics, which have extremely low variance (SD < 0.001%). The analytical cross-checks (DES matching closed-form to within 0.1%) are a strength, though they also raise the question of what the DES adds beyond confirming arithmetic.

Several methodological concerns warrant attention:

**Circular validation.** The DES is described as "confirming" the closed-form equations, but the DES implements the *same* message model and traffic accounting rules. When the DES generates exactly the messages specified in Table VII and counts exactly those bytes, agreement to 0.1% is expected by construction—it validates the implementation, not the model. The Pollaczek-Khinchine validation (Section III-A, "within 2% at $N = 100$") is more meaningful but is only performed at a single, small scale point. The gossip convergence validation is limited to $N \leq 1{,}000$.

**GE model coherence assumption.** The assumption that GE state is constant within each 10-second cycle (Section IV-C) is stated to be "conservative" because shorter coherence times would allow some intra-cycle retries to succeed. This is true for intra-cycle recovery but potentially *optimistic* for inter-cycle recovery: if the channel can transition multiple times within a cycle, the effective per-cycle loss probability changes. The authors should more carefully justify the 10-second coherence time against empirical RF channel data for LEO ISLs.

**Static topology assumption.** The analytical bound on cluster re-association overhead (<0.5%, Section V-B) is reasonable for co-planar configurations but the 90-minute timescale for cross-plane drift is optimistic for Walker-delta constellations with multiple shells. The "1–3 cycle AoI transient" during re-association is dismissed as negligible relative to the 441-second P99 AoI at $p_{\text{exc}} = 0.10$, but this comparison is misleading: the 441-second AoI is itself identified as problematic (motivating "future coupling to orbital prediction models"), so using it as a tolerance baseline is circular.

**Sectorized mesh model.** The $\sqrt{N}$ sector sizing is described as "an order-of-magnitude heuristic" (Section III-B.4), which is insufficient justification for a comparator architecture. The capped-fanout variant (cap = 10) monitors only 3.2% of sector peers (Table IV), raising questions about whether it provides adequate conjunction awareness to serve as a meaningful coordination architecture rather than just a traffic accounting exercise.

## 3. Validity & Logic

**Rating: 3 (Adequate)**

The core analytical results are internally consistent and correctly derived. The overhead accounting is meticulous, and the decomposition into topology-dependent (~5%) and workload-dependent (up to 46%) components is a useful clarification. The observation that commands dominate stress-case overhead independent of topology is well-supported by Fig. 8 and Table IX.

However, several logical issues weaken the conclusions:

**Baseline asymmetry.** The paper acknowledges (Section IV-G) that the centralized baseline "does not model uplink scheduling, ground contact windows, or per-station capacity sharing" while the hierarchical analysis is "more complete." This asymmetry undermines the comparative claims. The centralized $M/D/c$ model with $c = N/k_c$ shows no divergence until $N \approx 10^6$—meaning the hierarchical architecture's overhead disadvantage (46% vs. 5–15%) is not compensated by a processing scalability advantage within the studied range. The stated hierarchical advantage—"fault tolerance during ground outages"—is asserted but not quantitatively demonstrated beyond the availability numbers in Table XI (99.5% hierarchical vs. "single point" centralized), which lack a rigorous failure analysis.

**The "pipeline decoupling" result.** Table VIII shows identical drop counts for "No Loss" and "GE Only" columns, presented as validating architectural independence. But this is trivially true: if GE losses prevent messages from reaching the coordinator, the coordinator sees *fewer* messages, not more. The interesting case—whether GE retransmission *successes* during partial-bad-state conditions could cause transient ingress bursts—is not tested because the model assumes per-cycle state coherence. The claim that "shared-medium contention would couple loss with ingress saturation" is stated without analysis.

**Extrapolation beyond validated range.** Fig. 12 includes a $10^6$-node curve labeled as "analytical extrapolation, not DES-measured." While this is properly flagged, the paper's abstract and conclusion make claims about the $10^5$ scale as if it were the validated upper bound, yet the DES runtime of ~7 seconds at $N = 10^5$ suggests the simulation could easily be extended. The decision not to validate at $10^6$ (where the centralized baseline diverges) is a missed opportunity.

**AoI interpretation.** The P99 AoI of 441 seconds at $p_{\text{exc}} = 0.10$ is mapped to ~230 m along-track uncertainty, described as "a coarse screening value." For conjunction assessment, 230 m uncertainty at the screening stage is actually quite large (typical conjunction screening thresholds are 1–5 km miss distance with uncertainties of tens of meters). The paper should more carefully discuss whether this AoI is operationally acceptable.

## 4. Clarity & Structure

**Rating: 3 (Adequate)**

The paper is generally well-organized, with a clear roadmap at the beginning of Section IV and consistent notation throughout. The design equations summary (Section V-C) is a useful practitioner reference. Tables are numerous and mostly well-formatted, though the sheer volume (14 tables, 14 figures) makes the paper dense.

Several clarity issues:

**Notation overload.** The paper introduces many symbols ($\eta$, $\eta_{\text{eff}}$, $\eta_{\text{total}}$, $\eta_{\text{delivered}}$, $\eta_0$, $\eta_S$, $\eta_N$, $\eta_E$, $\eta_{\text{sector}}$) for variants of overhead. While each is defined, the proliferation makes it difficult to track which metric is being reported in any given table. A consolidated notation table would help.

**Abstract density.** The abstract packs in too many specific numbers ($\gamma = 0.949$, P99 = 440 s, $p_{BG} = 0.50$, 4 cycles, 0.1%, <0.5%) without sufficient context for a reader encountering the paper for the first time. The key message—that hierarchical coordination adds only ~5% topology-dependent overhead under a 1 kbps budget—is buried.

**Section III length.** The simulation framework section (III) is disproportionately long (~40% of the paper) relative to the results and discussion. Much of the traffic accounting detail (Tables V, VII, VIII) could be moved to an appendix without loss of readability.

**Missing figures.** All figures reference PDF files (e.g., `fig-architecture-diagram.pdf`) that are not included in the submission. The review must therefore rely on captions and textual descriptions, which is a significant limitation. The captions are generally informative but cannot substitute for the actual visualizations.

**Inconsistent precision.** Some results are reported to 0.1% precision (overhead) while others use rough bounds (<0.5%, ~5%). The paper would benefit from consistent significant figures appropriate to the uncertainty of each quantity.

## 5. Ethical Compliance

**Rating: 4 (Good)**

The paper includes an appropriate disclosure about AI-assisted ideation (Acknowledgment section), specifying the models used (Claude 4.6, Gemini 3 Pro, GPT-5.2) and noting that the AI-motivated aspects "are not validated here." The open-source data availability statement with a specific repository tag is commendable. The use of "Project Dyson Research Team" as author with a note about individual names for final publication is acceptable for review but must be resolved before publication per IEEE policy.

One concern: the reference to [dyson_multimodel] is to the authors' own unpublished work hosted on their project website, which is not peer-reviewed. This self-citation should be flagged as non-archival. The AI model version numbers (Claude 4.6, GPT-5.2) appear to reference future/unreleased versions as of the review date, which is unusual and should be clarified.

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is within scope for IEEE T-AES, which publishes work on space systems, autonomous operations, and communication architectures. The reference list (50 items) is comprehensive, covering constellation operations, swarm robotics, queueing theory, distributed systems, and space standards. Key references (Kleinrock, Lamport, Raft, CCSDS standards, AoI literature) are appropriate.

However, several gaps exist:

- **No references to existing space swarm coordination work** beyond NASA DSA [nasa_dsa] and DARPA F6 [darpa_f6]. The ESA OPS-SAT and related autonomous operations demonstrations are missing.
- **No references to DTN performance analysis** in mega-constellations, despite citing BPv7. Work by Fraire et al. on contact graph routing and Araniti et al. on satellite DTN would be relevant.
- **Limited engagement with the AoI literature.** The paper cites three AoI references but does not engage with the substantial body of work on AoI optimization in scheduled access systems, which is directly relevant to the TDMA coordinator model.
- **Several non-archival references** (Kuiper, DARPA programs, DoD fact sheets) are appropriately flagged but weaken the scholarly foundation. The Starlink reference [starlink_ops] is an FCC filing supplemented by a non-archival blog.
- **The O'Neill [5] and Badescu [6] references** to $10^5$–$10^6$ unit infrastructure concepts are aspirational/speculative and do not provide engineering requirements that would validate the scale range studied.

---

## Major Issues

1. **Circular validation undermines the DES contribution.** The DES implements the same message model as the closed-form equations and confirms them to 0.1%. This validates code correctness, not model validity. The paper needs either (a) validation against a higher-fidelity simulator (NS-3/OMNeT++, as acknowledged in Section V-A) or (b) validation against empirical data from an existing constellation. Without external validation, the DES adds little beyond the closed-form equations themselves. The authors should reframe the DES contribution as implementation verification rather than independent validation.

2. **Asymmetric baseline comparison invalidates the central comparative claim.** The hierarchical architecture is analyzed with full communication-layer detail while the centralized baseline models only processing queues. The paper acknowledges this (Section IV-G) but still draws comparative conclusions. Either the centralized baseline must be modeled with comparable fidelity (uplink scheduling, contact windows, spectrum constraints) or the comparative framing must be abandoned in favor of standalone hierarchical sizing.

3. **The 1 kbps operating regime limits practical impact.** The paper studies a degraded-mode RF backup channel active <1% of operational time. The design equations are specific to this regime (e.g., the stress-case $\eta \approx 46\%$ is meaningful only at 1 kbps). The paper should either (a) demonstrate that the equations generalize to other bandwidth regimes with worked examples or (b) explicitly scope the contribution as degraded-mode sizing. The claim that "results scale linearly with $C_{\text{node}}$" (Section III-D) needs verification—at higher bandwidths, processing constraints and propagation delays may become binding.

4. **Missing figures.** None of the 14 referenced figures are included. While the LaTeX source references external PDFs, the review cannot assess the quality of data presentation, the clarity of design curves (especially Fig. 5, the key GE sensitivity sweep), or whether the figures support the textual claims. This must be resolved before any publication decision.

5. **GE model lacks empirical grounding.** The Gilbert-Elliott parameters ($p_G = 0.01$, $p_B = 0.90$, $p_{GB} = 0.05$, $p_{BG} = 0.50$) are not justified against measured LEO ISL channel data. The sensitivity sweep (Fig. 5b) partially addresses this by covering a range of $p_{BG}$ and $p_B$, but without empirical anchor points, practitioners cannot determine which design curve applies to their system. At minimum, the authors should cite measured burst-error statistics for S-band LEO links.

---

## Minor Issues

1. **Eq. (2):** The $M/D/1$ waiting time formula $W_q = \rho / [2\mu_s(1-\rho)]$ is the Pollaczek-Khinchine result for $M/D/1$, but the notation is slightly non-standard. Conventionally, $W_q = \rho \bar{s} / [2(1-\rho)]$ where $\bar{s} = 1/\mu_s$. Clarify units.

2. **Table I:** The "Representative System" column (e.g., "Hyperscale data center" for $c = 1000$) is speculative and not grounded in actual constellation operations. Consider removing or replacing with actual system references.

3. **Section III-B.3:** The gossip convergence formula $R_{\text{conv}} = \max(\lceil\log_2 N\rceil, \lceil N/(bf)\rceil)$ combines two different convergence criteria without justification. The $\log_2 N$ term is the epidemic spreading bound; the $N/(bf)$ term is a throughput constraint. Their interaction should be explained.

4. **Table IX, footnote a:** "SD < 0.001%" — this extremely low standard deviation suggests the simulation has essentially no stochastic variation in overhead, which is expected given the deterministic message model. This should be stated explicitly rather than presented as a precision achievement.

5. **Section IV-A:** "Fleet-wide TDMA cost is 0.28 kbps/node (1% coordinators)" — the derivation of 0.28 kbps is not shown. Please provide the calculation.

6. **Eq. (8):** $\gamma = 0.949$ is derived from specific assumptions (24 kbps PHY, 500 km cluster, CCSDS Proximity-1 turnaround). The paper then "conservatively retains $\gamma = 0.85$" to account for FEC, ranging, and control overhead. This is reasonable but the 7% + 3% + 5% = 15% additional overhead should be justified rather than asserted.

7. **Section V-B, static topology:** The 7.4 km/s relative velocity figure is the orbital velocity, not the cross-plane relative velocity at orbital intersections. Cross-plane drift rates depend on the inclination difference and RAAN precession rate. Please correct or clarify.

8. **Acknowledgment:** "Total MC wall-clock time: ~90 min on commodity hardware" — specify hardware (CPU, RAM) for reproducibility.

9. **Reference [dyson_multimodel]:** Self-citation to non-peer-reviewed project website. Flag as non-archival or remove.

10. **Throughout:** The paper uses "stress-case" rather than the standard "worst-case" or "stress case" (two words). Standardize terminology.

11. **Table X, $k_c = 50$ row:** Latency at $N = 10^4$ is 508 ms but at $k_c = 100$ it drops to 340 ms. The text says "smaller clusters increase regional queueing delay" but doesn't explain why 508 > 340 when $k_c = 50$ should have *less* within-cluster batch delay ($50 \times 5 = 250$ ms vs. $100 \times 5 = 500$ ms). The regional queueing effect must dominate; please clarify.

12. **Abstract:** "$\gamma = 0.949$ from TDMA frame analysis" appears in the abstract but the paper conservatively uses 0.85. The abstract should report the value actually used in the design recommendations.

---

## Overall Recommendation

**Major Revision**

The paper addresses a legitimate gap in the literature—systematic byte-level traffic accounting for hierarchical coordination at $10^3$–$10^5$ scale—and provides a useful collection of design equations. However, the contribution is undermined by four significant issues: (1) the DES "validation" is circular, confirming the same arithmetic rather than providing independent model validation; (2) the baseline comparison is asymmetric, with the centralized architecture modeled at much lower fidelity than the hierarchical; (3) the practical impact is limited by the narrow 1 kbps degraded-mode operating regime without demonstration of generalizability; and (4) the GE channel model lacks empirical grounding. The paper also suffers from excessive length in the methodology section relative to insights delivered, and the missing figures prevent full assessment. A major revision addressing the baseline asymmetry, providing external validation (even partial), grounding the GE parameters empirically, and tightening the presentation would make this a solid contribution to the T-AES readership.

---

## Constructive Suggestions

1. **Add a packet-level validation vignette.** Even a single-cluster NS-3 or OMNeT++ simulation at $k_c = 100$ with realistic TDMA scheduling would transform the paper's credibility. This would ground the $\gamma$ assumption, validate the pipeline decoupling claim under realistic MAC behavior, and address the circular validation concern. It need not cover the full parameter space—a single anchor point would suffice.

2. **Equalize baseline fidelity or reframe the contribution.** Either add uplink scheduling and contact-window constraints to the centralized model (making the comparison fair) or reframe the paper as "standalone hierarchical sizing equations" without comparative claims. The latter is actually a stronger, more defensible contribution—the design equations have value independent of any baseline comparison.

3. **Ground the GE parameters with empirical data.** Cite measured burst-error statistics for S-band LEO links (e.g., from Iridium, CCSDS test campaigns, or academic measurement studies). Map the $p_{BG}$/$p_B$ design curves (Fig. 5b) to specific physical scenarios (e.g., "solar proton event," "Earth-limb multipath," "antenna handover gap") so practitioners can select the appropriate curve.

4. **Demonstrate bandwidth generalizability.** Add a second worked example at 10 kbps or 100 kbps to show that the design equations remain valid (or identify where they break down). This would significantly broaden the paper's applicability beyond the narrow RF-backup regime and address the concern about processing/propagation constraints becoming binding at higher rates.

5. **Compress Section III and expand Section V.** Move detailed traffic accounting tables (V, VII, VIII) to an appendix. Use the recovered space to expand the discussion of operational implications: What does a 441-second P99 AoI mean for conjunction assessment? Under what mission scenarios is the stress-case workload realistic? How should a constellation operator choose between hierarchical and sectorized mesh? The current discussion section is thin relative to the methodology.