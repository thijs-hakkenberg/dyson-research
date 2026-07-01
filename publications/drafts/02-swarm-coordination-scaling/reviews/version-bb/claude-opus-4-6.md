---
paper: "02-swarm-coordination-scaling"
version: "bb"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-27"
recommendation: "Major Revision"
---

# Peer Review: "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms"

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a genuine gap: the absence of closed-form sizing relationships for hierarchical coordination architectures at the $10^3$–$10^5$ node scale with byte-level traffic accounting. The claim that no prior work combines autonomous coordination, byte-level accounting, and $10^4$–$10^5$ scale appears defensible, and the practitioner-oriented "design equation" framing is useful. The three key equations (coordinator ingress sizing, AoI P99, GE recovery P95) are individually straightforward but their assembly into a coherent sizing toolkit has practical value for constellation architects.

However, the novelty is limited in a fundamental sense. The individual analytical results—geometric tail for AoI, Markov chain recovery for Gilbert-Elliott, M/D/1 queueing—are textbook. The paper's contribution is essentially an *application integration* of known results into a specific domain context. This is valuable engineering work, but the intellectual contribution is closer to a systems engineering handbook chapter than a research advance. The paper would benefit from a more honest framing: "we assemble known results" (which the authors do say in places) rather than "we derive" (which overstates originality).

The operating regime (1 kbps RF-backup, <1% of operational time) is extremely narrow. While the authors argue generalizability via Table II and the $C_{\text{node}}$ parameterization, the table itself shows that at ≥10 kbps the coordinator bottleneck and TDMA requirement vanish—meaning the most interesting results (Sections IV-A, the TDMA analysis) are irrelevant for the vast majority of operational time. The paper would be strengthened by more clearly articulating *when* these design equations matter operationally and what decisions they actually inform.

## 2. Methodological Soundness

**Rating: 3 (Adequate)**

The methodology has a fundamental circularity that the authors partially acknowledge but do not fully resolve. The DES and the closed-form equations operate at the *same* abstraction level (message-layer), so their agreement to 0.1% confirms arithmetic consistency, not model validity. The authors state this clearly in Section III-A ("their agreement confirms arithmetic consistency, not physical fidelity"), which is commendable, but this means the paper's primary quantitative claim—0.1% agreement—is essentially a code verification result, not a validation result. The distinction between verification and validation should be made more prominent, perhaps in the abstract, which currently reads as though the Monte Carlo "verifies" the design equations in a stronger sense.

The Gilbert-Elliott model's per-cycle coherence assumption (GE state constant within $T_c = 10$ s) is a significant modeling choice that deserves more scrutiny. The authors argue it is conservative for recovery (shorter coherence would help) but acknowledge no measured S-band ISL channel statistics exist. This is acceptable for a parametric study, but the claim that the analysis provides "design curves for arbitrary channel burstiness" (abstract, Section IV-C) overstates what a two-state Markov model with per-cycle transitions can capture. Real ISL channels exhibit frequency-selective fading, Doppler-induced coherence bandwidth changes, and interference patterns that a GE model cannot represent. The parametric sweep over $p_{BG}$ and $p_B$ is useful but should be presented as sensitivity analysis, not as a general channel characterization.

The Monte Carlo configuration (30 replications) is adequate for mean estimation but marginal for tail statistics. The P99 AoI at $p_{\text{exc}} = 0.10$ is computed from ~$3.15 \times 10^6$ samples per run, which is sufficient, but the per-run-then-aggregate methodology (footnote to Table VI) should be validated against pooled estimates to confirm the two approaches converge. The bootstrap CI of [438, 444] s is suspiciously tight for a P99 estimate and may reflect the deterministic nature of the geometric distribution rather than genuine statistical precision.

The static topology assumption is a significant limitation for LEO mega-constellations. The analytical bound of <0.5% overhead for re-association is plausible but relies on assumptions about cluster-boundary crossing rates that are not validated against any specific constellation geometry. The claim that "the dominant concern is not byte overhead but the 1–3 cycle AoI transient" is insightful but the transient behavior is explicitly not modeled.

## 3. Validity & Logic

**Rating: 3 (Adequate)**

The internal logic is generally sound, and the authors are commendably transparent about limitations. The key analytical results check out: Eq. (8) for AoI P99 is a correct application of the geometric quantile; the coordinator ingress sizing follows directly from byte counting; the GE Markov recovery derivation is standard. The joint interaction verification (Section IV-D, Table IX) demonstrating pipeline decoupling under dedicated links is a useful result, though the caveat about shared-medium contention breaking this decoupling somewhat undermines its practical applicability.

There are several logical tensions that weaken the paper's coherence:

1. **Baseline comparison asymmetry.** The centralized baseline models only compute-queue scalability (no communication layer), the global-state mesh is an intentional worst case, and the sectorized mesh provides different functionality than the hierarchical architecture. The authors acknowledge all of this (Table XI footnotes, Section IV-G), but the result is that no fair apples-to-apples comparison exists. The paper's implicit argument—that hierarchical is "better"—is not actually demonstrated; what is demonstrated is that hierarchical coordination *fits* within a 1 kbps budget, which is a feasibility result, not a comparative one.

2. **The 46% headline number.** The stress-case overhead of 46% is prominently featured, but the decomposition (Fig. 8) shows commands account for >60% of this. Commands are topology-invariant (any architecture must deliver them), so the topology-specific overhead is ~5%. This is buried in the text but should be the headline: "hierarchical coordination adds ~5% overhead; the remaining 41% is workload-dependent and topology-invariant." The current framing risks misleading readers about the cost of hierarchical coordination specifically.

3. **TDMA feasibility under GE losses.** The paper derives that intra-cycle retransmission is infeasible under GE bad-state conditions (Eq. 9–10, $\bar{M}_r = 0.18$ causes ingress to exceed $T_c$), then concludes inter-cycle recovery is "the effective mechanism." But this is a consequence of the model construction (per-cycle GE coherence), not a general physical result. If the coherence time were 2–3 seconds (plausible for some obstruction scenarios), intra-cycle retry would be partially effective. The paper should more carefully distinguish model-driven conclusions from physically robust ones.

The limitations section (V-C) is thorough and honest, which partially compensates for the above issues. The identification of priority queueing, correlated failures, and Earth-occlusion modeling as gaps is appropriate.

## 4. Clarity & Structure

**Rating: 4 (Good)**

The paper is well-organized with a clear roadmap (beginning of Section IV) and consistent notation (Table I). The separation of architecture-specific vs. workload-dependent overhead is clearly maintained throughout. Tables are generally well-constructed, with Table VII (traffic accounting) being particularly useful for reproducibility. The design equations summary in Section V-D is a valuable practitioner reference.

Several aspects could be improved:

- The paper is *long* for the depth of its contribution. At approximately 12 pages of dense content (excluding references), it could be tightened by 20–25% without loss. The sectorized mesh analysis (Section III-B.4), while thorough, occupies disproportionate space for what is acknowledged to be a functionally non-equivalent comparator. Tables IV, V, and VI could be consolidated.

- The notation is mostly consistent but $\eta$ vs. $\eta_{\text{total}}$ vs. $\eta_{\text{eff}}$ vs. $\eta_{\text{delivered}}$ vs. $\eta_{\text{sector}}$ creates cognitive overhead. A clearer notational hierarchy would help.

- Figure references are numerous but the figures themselves are described as PDFs that are not included in the review. The captions are informative, which partially compensates. The analytical extrapolation to $10^6$ nodes in Fig. 11 should be more prominently flagged as such (the caption note is easy to miss).

- The abstract is accurate but dense. The parenthetical "(nominal) through 46% (stress-case)" is awkward; the abstract should lead with the 5% architecture-specific result, which is the more meaningful contribution.

## 5. Ethical Compliance

**Rating: 4 (Good)**

The AI-assistance disclosure in the Acknowledgment section is appropriate and specific (naming the models used). The framing as "AI-assisted ideation exercise... not validated here" is honest. The open-source data availability commitment with a specific GitHub tag is commendable and supports reproducibility.

The anonymous authorship ("Project Dyson Research Team") with a footnote promising individual names for final publication is unusual but not unprecedented. The IEEE policy reference is appropriate. However, the lack of institutional affiliations makes it impossible to assess potential conflicts of interest (e.g., commercial interest in specific constellation architectures).

The paper does not raise ethical concerns regarding dual-use or harmful applications, though the military swarm programs cited in Section II-C (DARPA OFFSET, Replicator) could warrant a brief discussion of dual-use implications given the paper's applicability to military swarm coordination.

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is appropriate for IEEE T-AES in scope, addressing autonomous spacecraft coordination at scale. The reference list (52 items) is comprehensive and spans the relevant domains: constellation operations, swarm robotics, queueing theory, distributed systems, and space standards (CCSDS).

Several referencing concerns:

- Multiple references are non-archival (Amazon Kuiper overview, DARPA program pages, DoD fact sheets, McDowell's space report). While unavoidable for some operational programs, the paper relies on these for key claims about current constellation scale and operational approaches.

- The AoI literature coverage is adequate (Kaul, Yates, Kadota) but misses recent work on AoI in multi-hop networks and scheduling for AoI minimization that would be directly relevant to the hierarchical architecture.

- No reference is provided for the claim that "optical ISL availability >99%" (abstract/Section I-C), which is a critical assumption underpinning the entire RF-backup framing.

- The paper does not cite any work on actual ISL channel measurements or characterization, which would strengthen the GE model parameterization discussion. Works by Kaushal and Kaddoum (2017, IEEE Commun. Surveys Tuts.) on free-space optical channel models, or Giggenbach et al. on optical LEO-LEO links, would be relevant.

- The SWIM protocol citation [39] is used for failure detection timing but the connection to the coordinator failure transient analysis is loose; the 35 s MTTR claim should be better justified.

## Major Issues

1. **Verification vs. Validation Conflation.** The paper's central quantitative claim—0.1% agreement between DES and closed-form—is a verification result (code consistency), not validation (physical fidelity). The abstract and several passages imply stronger validation than is warranted. The paper should: (a) use "verification" consistently instead of "verifies" when describing DES-to-analytical agreement; (b) add a brief subsection explicitly distinguishing V&V levels (code verification, model verification, model validation, system validation) and placing this work at the first level; (c) revise the abstract to avoid implying physical validation.

2. **Absence of Physical-Layer Grounding.** No single result in the paper has been validated against physical-layer simulation, hardware measurement, or operational data. While the authors acknowledge this (Section V-A), the paper presents design equations intended for practitioners without any evidence they produce correct results when applied to real systems. At minimum, a single-cluster NS-3 simulation (which the authors themselves identify as the "recommended next step") should be included, or the paper should be reframed as "preliminary sizing relationships pending physical-layer validation" rather than "design equations."

3. **Misleading Headline Overhead.** The 46% stress-case overhead is prominently featured but is dominated by topology-invariant commands (>60%). The architecture-specific contribution is ~5%. The paper should restructure its presentation to lead with the 5% figure and present the 46% as a total system budget that includes workload. Currently, a reader skimming the abstract and conclusions would conclude that hierarchical coordination "costs" 46%, which misrepresents the finding.

4. **Functional Non-Equivalence of Baselines.** The comparison between hierarchical ($\eta \approx 5$–46%) and sectorized mesh ($\eta \approx 65$–67%) is presented as an overhead comparison, but the two architectures provide fundamentally different services (full cluster coordination vs. 3.2% local awareness). The paper acknowledges this (Section III-B.4) but continues to make overhead comparisons throughout. Either the baselines should be redesigned to provide equivalent functionality, or all comparative statements should be qualified with functional scope.

## Minor Issues

1. **Eq. (2):** The M/D/1 waiting time formula $W_q = \rho / [2\mu_s(1-\rho)]$ is the Pollaczek-Khinchine result for deterministic service but is written without the standard $1/\mu_s$ service time factor that makes units consistent. Verify dimensional consistency.

2. **Table II:** The footnote states AoI "depends on $p_{\text{exc}}$ and $T_c$, not $C_{\text{node}}$" but this is only true when the channel is not saturated. At very low $C_{\text{node}}$, queue drops would affect AoI. Clarify the regime of validity.

3. **Section III-B.2:** "Processing delay: Deterministic 5 ms" — this is unrealistically fast for radiation-hardened processors typical of space applications. A RAD750 processes at ~130 MIPS; 5 ms per message implies ~650,000 instructions per message, which may be insufficient for orbit determination updates. Justify or increase.

4. **Table III, collision avoidance rate:** $10^{-4}$/node/s is stated as "screening events, not maneuver-triggering" but the message is labeled "Priority alert" (128 B). Clarify whether these are screening notifications or actionable alerts.

5. **Section IV-A, half-duplex analysis:** The egress model assumes broadcast commands, but the overhead accounting counts 512 B per node. If broadcast, the per-node byte cost should be amortized (one transmission serves all $k_c$ members). Clarify whether $\eta$ counts transmitted bytes or received bytes.

6. **Eq. (8):** The ceiling function produces integer multiples of $T_c$, but AoI is a continuous quantity. The DES value of 441 s vs. analytical 440 s suggests the DES samples at discrete epochs. Clarify the sampling methodology's impact on the P99 estimate.

7. **Section IV-C:** "Buffer requirements are modest (~77 kB per coordinator)" — this claim appears without derivation. Provide the calculation.

8. **Table IX:** The "GE + Exc." column shows dramatically fewer drops than "No Loss" at 15 kbps (377 vs. 122,510). This is because exception telemetry reduces offered load, not because GE helps. The column header is misleading; consider renaming to "Exc. + GE" or adding a "Exc. Only" column.

9. **Section V-D, geometric approximation:** The statement "overestimates P95 by 0–1 cycles" should specify the range of $p_{BG}$ over which this bound holds.

10. **Acknowledgment:** "Claude 4.6, Gemini 3 Pro, GPT-5.2" — these model version numbers do not correspond to any publicly released models as of mid-2025. If these are internal/beta designations, clarify; otherwise, correct.

11. **Throughout:** The paper uses "favorable" (e.g., RQ2, Section IV-H.1) where "preferred" or "recommended" would be more precise. "Favorable" implies a value judgment without specifying the objective function.

## Overall Recommendation

**Major Revision**

The paper addresses a real engineering need—parametric sizing for large autonomous space swarms—and assembles a useful set of design relationships with commendable transparency about limitations. However, the contribution is primarily one of application integration rather than methodological advance, and the absence of any physical-layer validation (even a single-cluster packet-level simulation) significantly limits the paper's utility as a practitioner tool. The misleading headline overhead figure, the functional non-equivalence of baselines, and the verification-validation conflation are issues that require substantive revision. The core analytical content is sound and, with appropriate reframing and the addition of at least preliminary physical-layer grounding, could make a solid contribution to IEEE T-AES.

## Constructive Suggestions

1. **Add a single-cluster NS-3 validation.** Even a minimal packet-level simulation ($k_c = 100$, TDMA PHY, one GE channel realization) would transform this paper from "preliminary sizing" to "validated design equations." This is the single highest-impact addition and is explicitly identified by the authors as feasible.

2. **Restructure the overhead presentation.** Lead with the 5% architecture-specific overhead as the primary result; present the 46% stress-case as a total system budget. Create a clear figure showing the overhead decomposition (similar to Fig. 8) in the introduction or results summary, making the topology-invariant vs. topology-specific distinction immediately visible.

3. **Replace or supplement the sectorized mesh baseline with a functionally equivalent comparator.** Consider a "flat hierarchical" variant (single-level clustering, no regional aggregation) or a "gossip-with-aggregation" protocol that provides the same fleet coordination capability as the four-level hierarchy. This would enable a meaningful overhead comparison between architectures providing equivalent service.

4. **Tighten the paper by ~20%.** Consolidate the sectorized mesh analysis (currently ~2 pages including tables); merge Tables IV/V/VI; reduce the TDMA frame derivation (Section IV-A) which, while thorough, occupies excessive space for a standard calculation. Use the recovered space for the NS-3 validation suggested above.

5. **Explicitly map design equations to decision points.** Add a "practitioner decision flowchart" or table mapping each design equation to the engineering decision it informs (e.g., "Eq. 7 → select coordinator transceiver data rate"; "Eq. 8 → determine acceptable $p_{\text{exc}}$ given conjunction screening AoI requirement"). This would significantly increase the paper's practical utility and differentiate it from a pure analysis paper.