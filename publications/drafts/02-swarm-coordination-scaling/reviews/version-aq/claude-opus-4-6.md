---
paper: "02-swarm-coordination-scaling"
version: "aq"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-27"
recommendation: "Major Revision"
---



# Peer Review: "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms"

## Manuscript Version: AQ

---

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a genuine gap at the intersection of mega-constellation operations and swarm coordination: the absence of closed-form sizing equations for hierarchical coordination architectures at the 10³–10⁵ node scale. The authors correctly identify that swarm robotics literature operates at 10–100 agents, constellation management at ~10⁴, and networking literature treats routing but not autonomous coordination with byte-level accounting. This positioning is reasonable and the practitioner-oriented sizing table is a useful contribution concept.

However, the novelty is more limited than the framing suggests. The "design equations" are relatively straightforward: the protocol overhead equation is a linear traffic accounting identity; the AoI expression is a standard geometric quantile; the GE recovery formula is a textbook Markov chain result; and the coordinator ingress is a throughput calculation. The intellectual contribution is not in deriving these individually but in demonstrating their compositionality—yet this compositionality result (Section IV-D) is shown to hold only under the specific (and acknowledged) assumption of point-to-point ISLs with independent links, which is precisely the condition under which one would *expect* independence. The more interesting and practically relevant case—shared-medium RF contention—is explicitly deferred.

The paper's honest framing of the RF-backup regime (<1% of operational time) is commendable but simultaneously undermines significance: if optical ISLs are available >99% of the time and coordination overhead is "negligible" under nominal operation, the entire analysis characterizes a rare degraded mode. The practical impact depends on how critical that degraded mode is, which is asserted but not rigorously justified (e.g., no analysis of optical ISL outage duration distributions or correlation with conjunction event rates).

## 2. Methodological Soundness

**Rating: 3 (Adequate)**

The cycle-aggregated simulation approach is appropriate for the stated research questions, and the authors are transparent about what is modeled versus abstracted (Table VI is exemplary). The vectorized implementation enabling ~7s runtimes at N=10⁵ is practical. The 30 MC replications per configuration with bootstrap CIs is standard, though the reported SD < 0.001% for overhead (Section III-E) raises a concern: this extraordinarily tight variance suggests the simulation is essentially deterministic for the overhead metric, which is expected given that overhead is a ratio of deterministic message sizes to a fixed budget. This means the MC framework adds little value for the primary metric—it is useful mainly for stochastic quantities like AoI and link loss recovery.

Several methodological concerns arise:

**Validation circularity.** The DES matches closed-form predictions to within 0.1% (Table VIII). While presented as validation, this near-perfect agreement suggests the simulation is implementing the same arithmetic as the closed-form equations rather than independently testing them. A true validation would involve a higher-fidelity simulator (NS-3, OMNeT++) or hardware-in-the-loop testing. The authors acknowledge this (Section V-A, item 2) but it weakens the "validated by simulation" claim in the abstract.

**M/D/1 centralized baseline.** The single-server (c=1) centralized model with μ_s = 1,000 msg/s is acknowledged as an intentional worst-case bound, but it is so unrealistic that comparisons against it have limited value. The more realistic M/D/c model (Table I) shows centralized processing scales to 10⁶ with modest parallelism—effectively conceding that the hierarchical advantage is not computational but operational (fault tolerance, spectrum independence). This is stated clearly in Section IV-G, but the abstract and several figures (Fig. 8) still visually emphasize the c=1 divergence.

**Gilbert-Elliott parameterization.** The GE model parameters (p_G=0.01, p_B=0.90, p_GB=0.05, p_BG=0.20) are stated without empirical justification. For LEO ISLs, these parameters should be derived from or calibrated against measured link statistics. The steady-state availability of 80% (p_BG/(p_GB+p_BG)) seems low for ISLs but may be appropriate for RF backup—this should be explicitly justified with reference to measured RF link statistics in LEO.

**Inter-cycle recovery is analytical only.** The "4–7 cycles to 95% recovery" result (Section IV-C) is explicitly not DES-validated. Presenting it alongside DES-validated results without consistent visual distinction risks reader confusion.

## 3. Validity & Logic

**Rating: 3 (Adequate)**

The core logical structure is sound: define a message model, derive traffic equations, verify with simulation, and characterize the design space. The conclusions are generally well-supported by the analysis, and the authors are commendably careful about stating conditionality (e.g., the joint independence result's dependence on point-to-point ISLs).

However, several logical issues merit attention:

**The 9× envelope claim.** The abstract highlights a "9× envelope dominated by workload assumptions rather than topology." This is true but somewhat trivially so: the 9× ratio (46%/5%) is between stress-case (every node receives a 512-byte command every cycle) and nominal (exception telemetry at p_exc=0.10). Since commands are workload-driven and topology-invariant in the hierarchical model, this ratio would hold for *any* architecture with the same command model. The insight is that topology-specific overhead (summaries) is <1%—a useful finding, but the 9× framing overstates it.

**Sectorized mesh comparison.** The √N sector sizing is described as an "order-of-magnitude heuristic" (Section III-B.4), and the capped-fanout variant (cap=10) reduces the sectorized mesh to O(N) complexity—the same as hierarchical. The 1.4–1.5× overhead ratio (Table IV) then depends entirely on the heartbeat parameterization (32 bytes × 10 neighbors vs. 64 bytes × 1 coordinator). This is a parameter choice, not an architectural insight. A fairer comparison would equalize the neighbor-monitoring function.

**Cluster size invariance.** Table XI shows η is invariant to k_c (±0.1%), which follows directly from the traffic model: per-node overhead is dominated by commands (512 B/node/cycle) and heartbeats (64 B/node/cycle), neither of which depends on k_c. The summary traffic (512 B per coordinator per cycle, amortized over k_c nodes) contributes ~0.4 bps/node—negligible. This invariance is a property of the message model, not a deep architectural result.

**Extrapolation to 10⁶.** The abstract and Fig. 9 reference N≈10⁶ as the centralized divergence point, but this is an analytical projection, not simulated. The disclaimer in Fig. 9's caption is appropriate, but the abstract's phrasing ("analytical projection; simulated to 10⁵") could be clearer that the 10⁶ claim carries significant uncertainty.

## 4. Clarity & Structure

**Rating: 4 (Good)**

The paper is well-organized with a clear roadmap (Section IV opening paragraph) and consistent notation. The separation of reference bounds from the architecture under study is well-handled. Tables are generally informative, and the traffic accounting (Tables III, V, VI) provides excellent reproducibility. The abstract is dense but accurate.

Several clarity issues:

The paper is *extremely* long for the depth of its analytical contribution. Much space is devoted to parameter tables, sensitivity sweeps, and caveats that, while thorough, could be condensed. The 14 figures are excessive; several (Figs. 5, 6, 10, 11) could be moved to supplementary material without loss.

The notation is mostly consistent but the dual use of η (offered overhead) and η_delivered, η_eff, η_total, η_sector, η_0, η_S, η_N, η_E creates a proliferation that taxes the reader. A notation table would help.

The "Baseline Interpretation Note" (Section I-C) is crucial context but is easy to miss. Consider promoting this to a more prominent position or using a boxed callout.

The coordinator link model distinction (Model A vs. Model B) in Section IV-A is important but introduced abruptly. The physical interpretation—Model A is a hard deadline, Model B allows token carry-over—should be stated before the technical details.

## 5. Ethical Compliance

**Rating: 4 (Good)**

The AI-assistance disclosure in the Acknowledgment section is transparent: "An AI-assisted ideation exercise (Claude 4.6, Gemini 3 Pro, GPT-5.2; see [48]) motivated aspects of the coordinator architecture but is not validated here." This is appropriate and honest. The code availability commitment (GitHub tag paper-02-v-aq) supports reproducibility. The anonymous authorship ("Project Dyson Research Team") with a note about final publication is unusual but acceptable per IEEE policy.

One concern: the reference to "Claude 4.6, Gemini 3 Pro, GPT-5.2" includes model versions that do not exist as of my knowledge cutoff. If these are speculative/future model names, this should be clarified; if the paper is set in a near-future context, this is unconventional for a technical journal submission.

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is appropriate for IEEE TAES in scope. The reference list (50 items) covers the major relevant areas: constellation operations, swarm robotics, queueing theory, gossip protocols, AoI, and distributed consensus. Key references (Kleinrock, Demers, Lamport, Raft, AoI literature) are appropriate.

However, several gaps exist:

- **No references to actual ISL link budget analyses** or measured RF backup channel statistics for LEO constellations. The 1 kbps budget and GE parameters need empirical grounding.
- **Missing recent work on distributed space systems coordination**, particularly from the SmallSat and CubeSat communities (e.g., Radhakrishnan et al., 2016 on inter-satellite link design; Kak et al., 2020 on LEO satellite networking).
- **No reference to CCSDS AOS or TC/TM standards** beyond Proximity-1, which would ground the message size assumptions.
- **The DTN/BPv7 reference** [41] is cited but never substantively engaged—how does the hierarchical model relate to bundle protocol custody transfer?
- Several references are non-archival (Amazon website, DARPA program pages, DoD fact sheets). While understandable for program descriptions, these weaken the scholarly foundation. At minimum, 5–6 of these should be replaced with peer-reviewed sources or supplemented with archival alternatives.

---

## Major Issues

1. **Validation circularity (Section IV-F).** The DES matching closed-form to 0.1% demonstrates arithmetic consistency, not independent validation. The paper needs either (a) a packet-level simulation comparison (even for a single configuration), (b) comparison against a published benchmark, or (c) explicit reframing of the DES role from "validation" to "implementation verification." The abstract's "validated by simulation" is currently misleading.

2. **GE model parameterization lacks empirical basis (Section IV-C, Table II).** The Gilbert-Elliott parameters are presented without justification. For the results to be useful to practitioners, these must be tied to measured link statistics or at minimum a sensitivity analysis over the GE parameter space (not just steady-state availability). The 80% steady-state availability is a critical assumption driving the 4–7 cycle recovery result.

3. **The joint independence result (Section IV-D) is architecturally trivial under stated conditions.** Under point-to-point ISLs with independent links, the fact that pre-ingress losses don't affect post-ingress queueing is a direct consequence of the pipeline architecture, not an empirical finding. The paper acknowledges this but still presents it as a "key finding." The interesting case (shared-medium) is deferred. This section should be reframed as a verification of model consistency rather than a novel result.

4. **Absence of orbital dynamics coupling.** The paper treats cluster membership as static within coordination cycles, but LEO satellites at different altitudes have significant differential drift. The 500 km cluster diameter assumption needs justification: how long does a cluster maintain spatial coherence? What is the re-clustering rate? The handoff analysis (Section III-B.2) addresses coordinator rotation but not cluster dissolution/reformation, which could dominate overhead at certain orbital configurations.

5. **The practical relevance framing is internally contradictory.** The paper simultaneously argues that (a) the RF-backup regime is <1% of operational time, (b) under nominal optical ISLs overhead is "negligible," and (c) the design equations are important for practitioners. If the regime is rare and the overhead is negligible when it's not active, the sizing equations have limited practical impact unless the consequences of failure during that <1% are catastrophic—which is asserted but not analyzed (e.g., what is the probability of a conjunction event coinciding with an optical outage?).

---

## Minor Issues

1. **Eq. (2):** The M/D/1 waiting time formula W_q = ρ/(2μ_s(1-ρ)) is correct for the mean but should be explicitly labeled as the Pollaczek-Khinchine result for deterministic service, not the general M/G/1 formula.

2. **Table II footnote c:** "Set low for single-server bound" — the value μ_s = 1,000 msg/s is not obviously "low" without context. What would a realistic ground station achieve?

3. **Section III-B.2, RF-backup handoff:** The "seed handoff" concept (~2 kB) is interesting but the claim that it "enables emergency re-election" needs more detail. What state is lost? How does the new coordinator reconstruct cluster state?

4. **Table VII:** The "No Loss" and "GE Only" columns show identical drop counts at every capacity level. This is the independence result, but it's visually confusing—add a footnote explaining why these are identical.

5. **Section III-F:** "Total utilization is η_total = B_status + O_protocol ≈ 67% (stress-case)" — this should be η_total = (B_status + O_protocol)/C_node to be dimensionally consistent.

6. **Fig. 1** is referenced but described as a PDF figure that presumably shows the four-level hierarchy. The caption mentions "Labels: aggregation ratios" but these ratios (10–100) should be defined more precisely.

7. **Eq. (6):** The sector overhead equation B_sector^capped includes only status and heartbeats but not inter-sector relay (512 B × ≤2), which is mentioned in the text. Clarify whether Eq. (6) is per-node average or per-interior-node.

8. **Section IV-B:** "P99 AoI > 440 s" — the ">" symbol is confusing since the exact value is 440 s (Eq. 8) and the DES gives 441 s. Use "≈" or "= 440 s."

9. **Acknowledgment:** "Total MC wall-clock time: ~90 min on commodity hardware" — specify hardware (CPU, RAM) for reproducibility.

10. **Reference [1]:** Combining an FCC filing with Jonathan's Space Report (non-archival blog) in a single reference is unusual. Separate these or use only the FCC filing.

11. **Table IX, footnote a:** "SD < 0.001%" — report the actual SD value rather than an upper bound, or explain why it is so small (deterministic message model).

---

## Overall Recommendation

**Major Revision**

The paper addresses a legitimate gap in the literature and provides a well-structured, transparent analysis with commendable attention to assumptions and limitations. The practitioner-oriented sizing equations and open-source simulation are valuable contributions in principle. However, the current version has several significant issues: (1) the "validation" is circular—the DES implements the same arithmetic as the closed-form equations; (2) key parameters (GE model, collision rate, cluster diameter) lack empirical grounding; (3) the joint independence result is architecturally trivial under the stated conditions; (4) the practical relevance framing is internally contradictory regarding the RF-backup regime's rarity versus importance; and (5) the paper is substantially longer than warranted by the analytical depth. A major revision addressing the validation methodology, empirical parameterization, and tighter framing of contributions would make this a solid contribution to IEEE TAES.

---

## Constructive Suggestions

1. **Replace "validation" with "verification" and add one packet-level comparison.** Run a single configuration (e.g., N=1,000, k_c=100) through NS-3 or OMNeT++ with a realistic MAC layer. Even a single data point showing the message-layer estimates are within 20% of packet-level results would dramatically strengthen the paper. Alternatively, clearly reframe the DES as "implementation verification" throughout.

2. **Ground the GE parameters empirically and add a 2D sensitivity sweep.** Cite measured RF link statistics for LEO (e.g., from Iridium or amateur satellite observers) to justify the baseline GE parameters. Then sweep p_GB × p_BG to show how recovery time varies across the plausible parameter space. This converts a single-point result into a design chart.

3. **Quantify the conjunction-during-outage risk.** The practical case for the RF-backup analysis depends on the probability that a conjunction screening event occurs during an optical ISL outage. Use published conjunction rates (~10⁻⁴/node/s from your own model) and optical availability (~99%) to compute this joint probability. If it's negligibly small, acknowledge this honestly; if it's significant, it strengthens the motivation.

4. **Condense by ~30%.** Move Tables IV, VI, and X and Figures 5, 6, 10, 11 to supplementary material. Merge the three workload profiles into a single parametric equation (already given: η(p_cmd) = η₀ + p_cmd × 4096/(C_node × T_c)) with a brief discussion rather than a full subsection. This would sharpen the paper's impact considerably.

5. **Address cluster coherence time.** Add a brief analysis (even order-of-magnitude) of how long a 500 km cluster maintains membership stability under differential orbital drift. If re-clustering occurs on timescales comparable to the coordinator duty cycle (24–48 h), the handoff analysis is incomplete. If cluster coherence is much longer (weeks), state this with a supporting calculation.