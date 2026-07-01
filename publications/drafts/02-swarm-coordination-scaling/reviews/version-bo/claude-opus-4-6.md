---
paper: "02-swarm-coordination-scaling"
version: "bo"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-27"
recommendation: "Major Revision"
---

# Peer Review: "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms"

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a genuine gap: there is no published work providing closed-form parametric sizing relationships for coordination architectures at the $10^3$–$10^5$ node scale with byte-level traffic accounting. The authors correctly identify that swarm robotics literature operates at 10–100 agents, constellation management at ~$10^4$, and networking literature treats routing but not coordination overhead budgets. The three-layer feasibility framework (byte budget, MAC efficiency, TDMA airtime) is a useful conceptual contribution that practitioners could apply.

However, the novelty is somewhat circumscribed by the level of abstraction. The central finding—that architecture-specific overhead ($\eta_0 \approx 5\%$) is small while command traffic dominates—is, upon reflection, almost tautological: heartbeats (64 B) and summaries (512 B amortized over $k_c$) are inherently small relative to per-node commands (512 B). The "design equations" are largely dimensional analysis (bytes × 8 / bandwidth / cycle time) rather than non-obvious scaling laws. The AoI P99 result (Eq. 12) is a direct application of the geometric distribution quantile, and the GE recovery analysis is a standard two-state Markov chain. While collecting these into a coherent sizing framework has engineering value, the intellectual contribution is more in the nature of a well-organized design handbook than a research advance.

The paper would be significantly strengthened if it demonstrated that the sizing equations lead to non-obvious design decisions—e.g., parameter regimes where the hierarchy is definitively superior to alternatives in a way that was not predictable a priori, or where interactions between the three feasibility layers produce emergent constraints. The joint interaction test (Table VIII) actually shows the opposite: the mechanisms decouple cleanly, meaning the design equations are simply additive.

## 2. Methodological Soundness

**Rating: 3 (Adequate)**

The methodology is internally consistent but operates at a level of abstraction that limits its utility for actual system design. The DES is cycle-aggregated with fluid-server ingress—meaning it does not model the very TDMA slot-level dynamics that the paper identifies as the binding constraint. The authors acknowledge this clearly (Section III-A, "The DES does not validate TDMA airtime feasibility"), but this creates an uncomfortable situation: the paper's most interesting results (superframe timing, half-duplex partitioning, unicast stagger) are purely analytical, while the DES validates only the straightforward byte-counting arithmetic.

The $<0.1\%$ agreement between DES and closed-form (Table V) is presented as a validation result, but given that both implement the same message-layer accounting with the same parameters, this is really a verification of code correctness, not model validation. The authors do acknowledge this distinction (Section V-A, line "confirms implementation correctness, not physical validity"), which is commendable, but the abstract and several other passages blur this distinction (e.g., abstract: "an open-source Monte Carlo tool confirms implementation consistency to $<$0.1\%").

The Monte Carlo configuration (30 replications) is adequate for mean estimation given the reported SD $< 0.001\%$, but for tail statistics (P99 AoI, maximum GE streaks), 30 replications may be insufficient. The P99 is computed over ~$3.15 \times 10^6$ samples per run, which is reasonable, but the bootstrap CI methodology for tail quantiles should be more carefully justified—standard bootstrap can be unreliable for extreme quantiles.

The GE model's per-cycle coherence assumption (state constant within $T_c$) is acknowledged as conservative for recovery but is not validated against any physical channel measurement. The "physical mapping" paragraph (Section IV-C) provides useful context but the three obstruction mechanisms span coherence times from 1 s to 35 min, making the 10 s cycle-level GE a poor fit for at least two of the three. Earth occultation (deterministic, 35 min) should not use a stochastic model at all, as the authors note, but this means the GE model really only applies to structural shadowing—a narrow use case.

## 3. Validity & Logic

**Rating: 3 (Adequate)**

The logical structure is generally sound, and the authors are commendably transparent about limitations. The three-layer feasibility framework is logically coherent, and the distinction between architecture-specific ($\eta_0$) and workload-dependent ($\eta_{\text{cmd}}$) overhead is well-motivated. The observation that command traffic is topology-invariant "given the assumed workload semantics" (Section I-C) is an important qualifier that is consistently maintained.

Several logical concerns arise:

First, the comparison framework is asymmetric in ways that weaken the conclusions. The centralized baseline models only compute-queue scalability (M/D/c), not communication overhead; the global-state mesh is an intentional worst case; and the sectorized mesh provides different functional scope (Table XI). The authors acknowledge all of this, but it means the paper's topology comparison (Table IX, Fig. 8) is not really a fair comparison—it's more of a bounding exercise. The "14× bandwidth efficiency per unit of awareness" claim (Section IV-G) compares architectures providing fundamentally different services.

Second, the stress-case workload ($p_{\text{cmd}} = 1.0$, 512 B command every cycle to every node) is described as motivated by "fleet-wide reconfiguration campaigns" but is never justified against actual operational data. How often do real constellations issue per-node unique commands every 10 seconds? The event-driven profile ($\eta_E \approx 6\%$) is likely far more representative, which would make the headline $\eta \approx 46\%$ figure misleading as a characterization of the architecture.

Third, the coordinator failure analysis (Section III-B.2) provides recovery times for single, double, and triple faults, but the availability numbers in Table X (99.5% for hierarchical) appear to come from an illustrative two-state Markov model that is acknowledged as insufficient ("a full multi-state model is needed for operational use"). This undermines the reliability claims.

## 4. Clarity & Structure

**Rating: 4 (Good)**

The paper is well-organized with a clear roadmap (Section IV opening paragraph) and consistent notation (Table I). The three-layer feasibility framework provides a useful organizing principle. Tables are generally well-constructed with appropriate footnotes explaining assumptions and caveats.

The writing quality is high, with careful qualification of claims throughout. The authors consistently distinguish between message-layer predictions and physical-layer reality, which is a significant strength. The "Design Equations Summary" (Section V-C) is a valuable practitioner-oriented contribution.

However, the paper is excessively long for the depth of its contribution. At approximately 12–13 pages of dense content (excluding references), it could be shortened by 25–30% without loss of substance. Several sections are repetitive: the overhead decomposition is explained in the introduction (Section I-C), the simulation framework (Section III-F), the results (Section IV-E), and the design equations summary (Section V-C). The superframe analysis, while thorough, occupies disproportionate space for what is essentially a time-budget arithmetic exercise.

The notation, while defined in Table I, becomes unwieldy. The proliferation of subscripted $\eta$ variants ($\eta_0$, $\eta_{\text{cmd}}$, $\eta_E$, $\eta_S$, $\eta_{\text{total}}$, $\eta_{\text{eff}}$, $\eta_{\text{sector}}$, $\eta_{\text{sync}}$) creates cognitive load. A consolidated notation table mapping all variants would help.

Figures are referenced but not provided (understandable for LaTeX source review), making it impossible to assess their quality. The figure captions are informative.

## 5. Ethical Compliance

**Rating: 4 (Good)**

The AI-assistance disclosure in the Acknowledgment section is transparent: "An AI-assisted ideation exercise (Claude 4.6, Gemini 3 Pro, GPT-5.2; see [dyson_multimodel]) motivated aspects of the coordinator architecture but is not validated here." This is appropriately scoped—acknowledging the role without overclaiming.

The author block uses a team name ("Project Dyson Research Team") with a note that individual names will be provided for final publication. This is unusual for IEEE T-AES and should be resolved before acceptance. IEEE policy requires named authors who can certify authorship.

The open-source data availability statement with a specific repository tag is commendable and supports reproducibility. The Monte Carlo configuration is fully specified (Table III), enabling independent replication.

One concern: the reference to future AI model versions (Claude 4.6, GPT-5.2) suggests either the paper is set in the future or these are hypothetical version numbers. This should be clarified to avoid confusion about the provenance of the work.

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is within scope for IEEE T-AES, which publishes work on space systems, autonomous operations, and communication architectures. However, the paper sits at an unusual intersection: it is too abstract for a systems engineering audience (no physical-layer validation) and too applied for a theoretical audience (the mathematical contributions are elementary).

The reference list is comprehensive (50+ references) and covers the relevant literature across constellation management, swarm robotics, distributed systems, and communication theory. Key works are cited: LEACH [heinzelman_leach], Raft [ongaro_raft], SWIM [das_swim], AoI framework [kaul_aoi, yates_aoi], GE model foundations. The CCSDS standards references (SPP, Proximity-1, BPv7) ground the message sizes in real protocol specifications.

Several gaps exist. The paper does not cite recent work on distributed satellite autonomy beyond NASA DSA [nasa_dsa]—e.g., ESA's OPS-SAT experiments, or the growing literature on onboard AI for constellation management. The LEACH comparison (Section II-B) could be deepened: LEACH's energy-efficiency analysis and cluster-head rotation overhead are directly analogous to the coordinator duty-cycle analysis here. The paper also omits reference to the substantial literature on TDMA scheduling in satellite networks (e.g., Bertsekas and Gallager's treatment, or more recent work on demand-assigned TDMA for LEO constellations).

Several references are non-archival (Amazon Kuiper overview, DARPA program pages, DoD fact sheets). While understandable for emerging programs, these weaken the scholarly foundation. The self-citation [dyson_multimodel] to an apparently unpublished methodology paper is premature.

---

## Major Issues

1. **The DES validates only trivial arithmetic, not the interesting physics.** The paper's most consequential results—TDMA superframe feasibility, half-duplex partitioning, unicast stagger cycles—are purely analytical. The DES confirms byte-counting to $<0.1\%$, which is verification, not validation. The paper needs either (a) a packet-level simulation of at least one cluster to validate the TDMA analysis, or (b) a much more prominent and honest framing that this is a *sizing methodology paper* whose predictions are untested. Currently, the framing oscillates between these positions.

2. **The topology comparison is not a fair comparison.** The four architectures provide different functional capabilities (Table XI), operate at different abstraction levels (centralized = compute-queue only; mesh = communication only), and the "reference bounds" are intentionally extreme. The paper should either (a) restrict comparison to hierarchical vs. sectorized mesh (the only pair modeled at the same abstraction level with comparable scope), or (b) restructure the comparison as explicit bounding analysis rather than architecture selection guidance.

3. **The stress-case workload lacks operational justification.** The $\eta_S \approx 46\%$ headline figure assumes every node receives a unique 512 B command every 10 seconds—a scenario that is never justified against operational data from any existing constellation. The paper should either provide evidence that such workloads occur (with duration and frequency estimates) or reframe the event-driven profile ($\eta_E \approx 6\%$) as the primary result, with the stress-case as a clearly labeled upper bound.

4. **Coordinator availability claims are unsupported.** The 99.5% availability figure (Table IX) comes from an "illustrative" two-state Markov model that the authors themselves call insufficient. The triple-fault analysis (Section III-B.2) uses independent failure probabilities ($0.02 \times 0.01 \times 0.09$) without justifying independence—the very scenario described (power-negative tumbling) would correlate optical outage with coordinator failure. This analysis needs either rigorous treatment or removal.

5. **The 1 kbps design point is inadequately motivated as the primary analysis regime.** The paper states that 1 kbps applies during optical outages ($<1\%$ of operational time) and that at $\geq$10 kbps "all constraints are non-binding." This means the entire paper's detailed analysis applies to a rare degraded mode. While designing for worst-case is legitimate, the paper should lead with the nominal regime and present the 1 kbps analysis as a degraded-mode appendix, not the reverse.

---

## Minor Issues

1. **Eq. (2), M/D/1 waiting time:** The formula $W_q = \rho / [2\mu_s(1-\rho)]$ is the Pollaczek-Khinchine result for M/D/1, but the notation is non-standard. Typically $W_q = \rho^2 / [2\lambda(1-\rho)]$ or equivalently $\rho / [2\mu(1-\rho)]$. Clarify that $\mu_s$ here is the service rate, not the mean service time.

2. **Table I:** $\eta$ is defined as "$\eta_0 + \eta_{\text{cmd}}$, beyond baseline" but $\eta_{\text{total}}$ is defined as "$\eta + 20.5\%$ baseline." The relationship between these should be stated as an equation in the table or immediately after.

3. **Section III-B.2, Raft election over RF:** The calculation "$51 \times 0.8 / 0.36 \approx 113$ s" is unclear. Is 0.8 the transmission time per vote at 1 kbps (100 B × 8 / 1000 = 0.8 s)? And 0.36 is Slotted ALOHA throughput? This should be made explicit.

4. **Eq. (6), sectorized mesh overhead:** The equation gives bytes, not bits or bps. The footnote to Table IV converts to $\eta$ using bps, but the equation itself should be dimensionally consistent with the overhead definition.

5. **Table VII, "GE + Exc." column:** The dramatic drop in drops (122,510 → 377 at 15 kbps) is attributed to "load-reduction effect," but this deserves more explanation. Exception telemetry at $p_{\text{exc}} = 0.10$ reduces offered load by ~90%, so the 99.7% drop reduction is expected. This is not really testing interaction—it's testing load reduction.

6. **Section III-E:** "Peak vs. average rate distinction" is important but buried. This should appear earlier, perhaps in Section III-A or even the introduction, as it fundamentally affects how readers interpret the 1 kbps figure.

7. **Acknowledgment:** "Claude 4.6, Gemini 3 Pro, GPT-5.2" — these version numbers do not correspond to any publicly released models as of mid-2025. Clarify whether these are internal designations or future projections.

8. **Table III footnote (c):** "$\mu_s = 1,000$ msg/s" is described as "set low for single-server bound" but 1,000 msg/s with 5 ms processing time implies 5 parallel threads. Clarify the relationship between $\mu_s$ and $s_{\text{proc}}$.

9. **Fig. 7 caption:** References "30 MC replications, $N = 10,000$, $k_c = 100$" but the GE sensitivity sweep (panel b) presumably uses different configurations. Clarify.

10. **Section V-B:** The re-association overhead bound ($f_h = 0.8\%$) assumes $t_h \approx 30$ s, but the RF-backup seed handoff alone takes 16 s, and the text earlier states 1–3 cycles (10–30 s) for state rebuild. These should be reconciled.

---

## Overall Recommendation

**Major Revision**

The paper addresses a legitimate gap in the literature and provides a well-organized sizing framework for hierarchical coordination in large space swarms. The three-layer feasibility decomposition, the explicit superframe time budget, and the GE recovery design curves are useful engineering contributions. However, the paper suffers from five significant issues: (1) the DES validates only trivial byte-counting, not the TDMA dynamics that are the binding constraint; (2) the topology comparison is asymmetric and potentially misleading; (3) the stress-case workload is unjustified; (4) coordinator availability claims rest on an admittedly inadequate model; and (5) the paper's primary analysis regime (1 kbps) applies to $<1\%$ of operational time. A major revision addressing these issues—particularly adding packet-level validation of at least the single-cluster TDMA analysis—would substantially strengthen the contribution.

---

## Constructive Suggestions

1. **Add a single-cluster packet-level simulation.** Even a simplified NS-3 or custom TDMA simulator for one cluster ($k_c = 100$, 24 kbps PHY, half-duplex) would transform this paper from a sizing exercise into a validated design methodology. The superframe specification in Table VI provides the exact parameters. This is the single highest-impact improvement.

2. **Restructure around the nominal regime.** Lead with the $\geq$10 kbps optical ISL regime where the hierarchy operates nominally, present the event-driven workload ($\eta_E \approx 6\%$) as the primary result, and treat the 1 kbps RF-backup analysis as a degraded-mode design case. This better reflects operational reality and avoids the misleading impression that 46% overhead is the normal cost of hierarchical coordination.

3. **Strengthen the sectorized mesh comparison with matched functional scope.** Either (a) increase the mesh neighbor cap until it provides comparable awareness to the hierarchy (100 peers), showing the overhead crossover, or (b) design a hybrid architecture that combines mesh local awareness with hierarchical aggregation, demonstrating the complementarity rather than competition between the approaches.

4. **Provide operational workload data or scenarios.** Contact SpaceX, OneWeb, or ESA operations teams for even rough command-rate statistics, or derive workload profiles from published conjunction screening rates [esa_conjunction] and station-keeping maneuver frequencies. This would ground the three workload profiles in reality rather than assumption.

5. **Tighten the paper by 25%.** Consolidate the repeated overhead decomposition discussions (currently in Sections I-C, III-F, IV-E, and V-C) into a single definitive treatment. Move the detailed superframe arithmetic to an appendix. This would improve readability and make room for the packet-level validation suggested above.