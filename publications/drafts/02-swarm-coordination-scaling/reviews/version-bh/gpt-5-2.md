---
paper: "02-swarm-coordination-scaling"
version: "bh"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-02-27"
recommendation: "Accept"
---

## 1. Significance & Novelty — **Rating: 4/5 (Good)**

The manuscript targets a real and timely scaling problem: how to size coordination communications for *very* large autonomous spacecraft swarms (10³–10⁵ nodes) under tight per-node bandwidth budgets. The focus on producing **closed-form sizing equations** (overhead, coordinator ingress capacity, AoI tails, correlated-loss recovery) is valuable for practitioners and is not commonly delivered in the constellation operations literature, which tends to emphasize routing/ISL scheduling or ground-centric operations rather than byte-level coordination workload accounting.

The paper’s strongest novelty claim is the combination of (i) hierarchical coordination architecture, (ii) byte-level traffic accounting under a fixed per-node budget, and (iii) parametric design curves for correlated loss recovery—validated by a fast Monte Carlo DES. The explicit distinction between **information budget** (η) and **frame-time schedulability** (TDMA constraints; Table 9 and Eq. (19)) is also a useful contribution; many papers conflate throughput feasibility with real-time deliverability.

That said, the “closed-form” contribution is partly limited by the fact that several major operational determinants are abstracted (MAC contention beyond γ, deterministic visibility/occultation, pointing/acquisition, and network connectivity constraints for the mesh baselines). The work is still significant, but the novelty would be stronger if the manuscript more clearly scoped the intended operational regime (e.g., intra-cluster RF backup with TDMA; optical ISL assumed for state transfer) and separated what is *architectural* vs. what is *workload semantics* (commands, exception telemetry) even more crisply.

## 2. Methodological Soundness — **Rating: 3/5 (Adequate)**

The cycle-aggregated DES is appropriate for the paper’s goal—deriving and validating message-layer sizing equations—because it enables scaling to 10⁵ nodes and year-long horizons. The manuscript generally states assumptions clearly (e.g., static clustering for 1 year; GE state constant within a cycle; γ as MAC efficiency; baseline telemetry excluded from η). The inclusion of analytic cross-checks (Palm–Khintchine for centralized arrivals; geometric AoI P99 in Eq. (24); Markov-chain recovery CDF in Section IV-C) improves credibility.

However, several modeling choices materially affect the conclusions and need tighter justification and/or sensitivity analysis:
- **Command model ambiguity**: stress-case η≈46% is dominated by commands, but the paper alternates between “broadcast directive” and “per-node unicast command” (Section IV-A). The byte accounting treats commands as per-node information content, but schedulability depends critically on broadcast vs. unicast. This is acknowledged (Table 9), yet the workload profiles (Section IV-E) should specify *explicitly* the assumed addressing mode per profile and how it maps to η.
- **Coordinator ingress modeling**: the “Model A/B/TDMA” convergence argument (Section IV-A) is helpful, but Model A’s “worst-case inter-arrival” leading to ~50 kbps is not derived rigorously (it references min(Δt_i) without specifying the distributional bound being used). If the claim is that random-phase arrivals can create arbitrarily small Δt_i as k grows, then “worst-case” is essentially pathological; a high-quantile bound (e.g., 99.9% no-drop) would be more meaningful than absolute worst-case.
- **GE coherence assumption**: the paper correctly notes that making GE constant within-cycle structurally eliminates intra-cycle retransmission gains (Section IV-C). That is fine as a conservative bound, but then the interpretation “intra-cycle retransmission is infeasible” (Section IV-A) is partly a *frame-time* claim (Eq. (20)) and partly a *channel coherence* claim. These should be disentangled with a clear regime map: (i) frame-time feasibility of retries, (ii) channel mixing relative to retry spacing, (iii) net benefit.

Reproducibility is a strength (code + tag provided). Still, for IEEE T-AES standards, the paper should provide enough detail to reproduce key results without the code: e.g., exact per-cycle event ordering, queue service order, whether coordinator ingress is per-member dedicated or multiplexed, and how “phase staggering” is implemented across clusters.

## 3. Validity & Logic — **Rating: 3/5 (Adequate)**

Most conclusions are directionally supported by the presented equations and DES checks, especially the scale-invariance of η under O(N) traffic (Table 10; Eq. (6)) and the AoI P99 dependence on p_exc and T_c (Eq. (24); Table 7). The paper is also careful to acknowledge that centralized comparisons are compute-queue only (Table 12 footnotes; Fig. 17 caption), which avoids an unfair comms-layer comparison.

The main validity risk is that some headline conclusions depend on assumptions that are not yet sufficiently defended as “operationally representative”:
- The abstract states “protocol overhead is η_E≈6% under the operationally representative event-driven workload” and “architecture-specific traffic contributes ~5%.” This hinges on the chosen heartbeat rate (64 B/cycle each direction) and the exception telemetry probability model. In particular, the paper later states “heartbeats dominate η0” (~5.1%), which means the “architecture-specific overhead” is essentially a heartbeat design choice rather than an unavoidable structural cost. A reader could reasonably ask: why is one heartbeat per cycle required, and what failure-detection target does that satisfy?
- The claim “AoI P99=440 s … within conjunction screening tolerances” (abstract; Section IV-B) is plausible but not fully substantiated. Screening tolerances depend on orbit regime, covariance growth, sensor quality, and screening volume policy. The paper uses an along-track uncertainty growth rate (0.5 m/s) and TCA ~24 h to argue acceptability; this is a helpful sanity check, but it is not a general requirement mapping. As written, it risks overgeneralization.

The “coordinator bottleneck vanishes at ≥10 kbps” (abstract; Table 2) is logically true under linear scaling, but only if other constraints (e.g., half-duplex partitioning, acquisition overhead, contention) do not become dominant. Since those are abstracted into γ, the paper should phrase this as “vanishes in the message-layer budget model, assuming γ remains high and scheduling is feasible.”

## 4. Clarity & Structure — **Rating: 4/5 (Good)**

The manuscript is generally well organized: it states RQs, defines notation (Table 1), provides workload/topology definitions, then presents results with analytic cross-checks and sensitivity. The distinction between topology-dependent overhead and topology-invariant baseline telemetry is clear and consistently applied. Tables are numerous and mostly informative (notably Tables 9–11 and the TDMA superframe Table 6).

Two clarity issues stand out:
1. **Overload of “baseline” terminology**: “baseline telemetry excluded from η,” “centralized baseline,” “periodic baseline,” etc. This increases cognitive load. Consider renaming: “topology-invariant telemetry floor” vs. “centralized reference architecture” vs. “periodic reporting mode.”
2. **Inconsistent command accounting narrative**: Table 5 suggests centralized commands ~100 bps while hierarchical ~410 bps (stress-case), but centralized earlier says each node receives one command per cycle (Section III-B). If centralized issues fewer commands (or smaller, or less frequent), that is a workload difference, not an architectural difference, and should be explicitly stated to avoid confusion.

The abstract is dense but mostly accurate. However, it mixes message-layer utilization (η) with frame-time deliverability and with AoI tail claims; it would be clearer to explicitly label which results are “information budget,” which are “TDMA feasibility,” and which are “stochastic recovery/AoI.”

## 5. Ethical Compliance — **Rating: 4/5 (Good)**

The manuscript includes an explicit disclosure of AI-assisted ideation in the Acknowledgment and cites a supporting document. That is aligned with emerging transparency norms. The paper also provides open-source code and datasets, which supports scientific integrity and reproducibility.

Two improvements are advisable for IEEE T-AES expectations:
- The disclosure should clarify whether any AI system contributed to **text generation** or **data/figures/code** (currently phrased as “ideation exercise … motivated aspects”). If AI was used only for brainstorming, say so explicitly; if used in drafting, specify extent and human verification.
- The author block uses “Project Dyson Research Team” with a note that names/affiliations will be provided later. That is understandable for anonymized review, but for final compliance the manuscript must include full author identities, affiliations, funding, and any conflicts of interest (especially given the open-source project framing).

## 6. Scope & Referencing — **Rating: 4/5 (Good)**

The topic is appropriate for IEEE Transactions on Aerospace and Electronic Systems: constellation/swarm coordination, comms architecture sizing, latency/availability, and operational constraints. The paper references relevant areas: constellation ops, DTN/CCSDS, gossip dissemination, Raft, AoI literature, and queueing theory. The inclusion of CCSDS Proximity-1 and Space Packet Protocol is appropriate given the message sizing emphasis.

Some referencing gaps remain:
- For **mega-constellation operational coordination**, more peer-reviewed or archival sources would strengthen claims currently supported by non-archival filings/webpages (Starlink/Kuiper references are partly non-archival). This is common in the area, but adding archival analyses (or SSA/conjunction operations papers beyond ESA 2017) would help.
- For **RF link rates and half-duplex turnaround**, Proximity-1 is cited, but the mapping from that standard to the assumed 24 kbps cluster PHY (and guard times) could use an additional modern smallsat radio reference or a CCSDS S-band recommendation.
- The **sectorized mesh** model is presented as a baseline with narrower functional scope (Table 13). That is fair, but it also means the baseline is not directly comparable unless the paper positions it as “local neighbor awareness protocol” rather than “coordination architecture.” A citation to local broadcast/neighbor discovery protocols in satellite swarms would help ground this baseline.

---

## Major Issues

1. **Command addressing mode is central to feasibility but not fully pinned down in the workload profiles.**  
   In Section IV-A, the stress-case is “not single-cycle deliverable” under per-node unicast (Eq. (19); Table 9), yet η is reported identically (46%) for stress broadcast vs. unicast. The paper needs a clearer definition of workload profiles (Nominal/Event/Stress) that specifies: fraction of commands that are broadcast vs. unicast, command generation locus (ground/regional/cluster), and whether “per-node information content” is an appropriate metric when delivery spans 22 cycles. Otherwise, the main headline “η_S≈46%” risks being interpreted as operationally feasible when it may not be.

2. **Coordinator ingress sizing: “worst-case” Model A is not a meaningful bound as stated.**  
   The argument that random-phase arrivals imply a 50 kbps requirement via min(Δt_i) is effectively an unbounded worst-case as k grows unless you define a probabilistic bound (e.g., 99.9% no-drop) or enforce a minimum inter-arrival due to slotting/guard constraints. This should be reframed as (i) TDMA deterministic requirement, (ii) stochastic multiplexing requirement under a specified drop probability target, with a derivation using order statistics or network calculus/token bucket bounds.

3. **Heartbeat-driven “architecture-specific overhead ≈5%” is a design choice; failure-detection requirements are not specified.**  
   Since heartbeats dominate η0 (Section IV-E), the conclusion that hierarchical overhead is small depends on heartbeat period = T_c. The paper should connect heartbeat rate/size to a failure detection target (e.g., detection time distribution, false suspicion rate) and show sensitivity: what happens to η0 if heartbeats are every 3 cycles, or piggybacked, or replaced by implicit acknowledgments in TDMA?

4. **Mesh baselines are not commensurate in capability and connectivity, which weakens RQ3 comparisons.**  
   The sectorized mesh “cap=10” is explicitly not connected and provides ~3% peer coverage (Section III-B; Table 4). Comparing its η to hierarchical coordination risks being misleading unless the paper either (i) enforces connectivity/coverage constraints for the mesh baseline, or (ii) reframes RQ3 as comparing architectures under *different functional scopes* and makes that the central point.

5. **Physical-layer abstraction is acceptable, but some conclusions are phrased too strongly given what is not modeled.**  
   Statements like “at ≥10 kbps the coordinator bottleneck vanishes” and “AoI P99 within conjunction screening tolerances” should be softened or conditioned on assumptions about γ, scheduling feasibility, and orbit/SSA context. The Discussion acknowledges the gap, but the Abstract/Conclusion currently read more definitive than the model supports.

---

## Minor Issues

- **Table 5 (bandwidth breakdown) appears inconsistent with the centralized model description.** Centralized “Coord. commands ~100 bps” conflicts with “each node receives one command per cycle” stated earlier; if centralized is not issuing 512 B/cycle/node, clarify the centralized workload assumptions or remove that line item.
- **Equation labeling and section cross-references:** “Section IV-I” is referenced in the Hierarchical topology description (“cluster-size trade-off (Section IV-I)”), but the cluster-size discussion appears in Section IV-H. Check all roman numeral references for consistency.
- **Figure file name missing extension:** `\includegraphics{fig-cross-cycle-recovery}` lacks `.pdf` unlike others; may break compilation depending on LaTeX settings.
- **AoI sampling methodology:** Table 7 notes AoI sampled every 100 s. Since T_c=10 s, explain whether AoI is computed continuously but sampled sparsely, or computed only at sampling times. Sparse sampling can bias maxima and tail estimates.
- **GE “steady-state avail. 91%”** in Table 3: provide the calculation (stationary distribution of the 2-state chain) to avoid readers questioning consistency with p_GB and p_BG.
- **Terminology:** “drops” are queue drops only (Section III-E). Consider renaming to “queue drops” throughout tables to prevent misinterpretation.
- **Typographic/formatting:** Some tables are dense with long footnotes (e.g., Table 7). Consider moving methodology to text and simplifying table footnotes.

---

## Overall Recommendation — **Major Revision**

The paper is promising and likely publishable in T-AES after revision: it addresses an important scaling problem, provides useful sizing equations, and supports them with simulation and analytic checks. However, several core claims (stress-case overhead/feasibility, coordinator ingress “worst-case” sizing, and the interpretation of “architecture-specific overhead”) depend on modeling choices that must be better defined, justified, and—where feasible—supported with sensitivity analysis or probabilistic bounds. Clarifying workload semantics and making baseline comparisons commensurate would substantially strengthen the manuscript’s rigor and prevent misinterpretation by practitioners.

---

## Constructive Suggestions

1. **Make workload profiles formally defined and self-contained.**  
   Add a table that specifies for each profile: reporting mode (periodic vs exception with p_exc), command rate, command addressing mix (broadcast/unicast fraction), and whether delivery is required within one cycle. Then report η and *schedulability* jointly per profile (information budget + frame-time feasibility).

2. **Replace “Model A worst-case” with a probabilistic sizing bound.**  
   Define an acceptable drop probability (e.g., ≤10⁻⁶ per cycle per cluster) and derive required C_coord under random-phase arrivals using either order-statistics of inter-arrival gaps or a network-calculus/token-bucket bound. This will make the 21–50 kbps range defensible and interpretable.

3. **Tie heartbeat overhead to a failure-detection requirement and sweep it.**  
   Specify a detection time target (e.g., P95 detection ≤ 2T_c) and show η0 as a function of heartbeat period/size (and whether heartbeats can be piggybacked on scheduled TDMA slots). This will turn the “~5% architecture-specific overhead” claim into a tunable design curve.

4. **Strengthen RQ3 by making baseline comparisons capability-matched.**  
   Either (i) enforce connectivity/coverage constraints on the sectorized mesh (e.g., choose cap to ensure connected graph with high probability) and compare overhead under that constraint, or (ii) explicitly re-scope the comparison as “local neighbor awareness vs full cluster awareness” and quantify “overhead per monitored peer” as the primary comparative metric (you already hint at this; elevate it).

5. **Add a small packet-/slot-level validation for one cluster (even minimal).**  
   Since the paper already derives a detailed superframe (Table 6), a limited ns-3 (or equivalent) experiment for k_c=100 validating γ, slot timing, and half-duplex switching under a simple error model would substantially reduce the current “validation gap” and increase confidence in the TDMA feasibility claims. If full ns-3 is out of scope, provide a deterministic slot-level simulator and publish it with the repository.