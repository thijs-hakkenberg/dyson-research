---
paper: "02-swarm-coordination-scaling"
version: "x"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-02-24"
recommendation: "Accept"
---

## 1. Significance & Novelty — **Rating: 4/5**

The manuscript targets a real and timely systems problem: how coordination architectures scale for autonomous swarms in the \(10^3\)–\(10^5\) regime (with discussion of extrapolation). The explicit framing around *control-plane reservation* (1 kbps/node) and byte-level accounting is valuable for constellation operations and distributed autonomy communities, where many papers remain qualitative or focus on routing/data-plane throughput rather than coordination-plane sizing. The paper’s strongest “engineering” novelty is the coordinator ingress sizing result showing burstiness-driven headroom (50 kbps unscheduled vs. 24 kbps TDMA), and the demonstration that mean-rate reasoning can be materially misleading (Section IV-G / Section IV-J).

That said, some of the headline “scaling” claims are less novel than implied because the constant-overhead result is largely a direct consequence of the assumed message model (fixed-depth hierarchy, fixed per-node message sizes/rates), which the paper itself acknowledges (Section IV-D). The work is best positioned as a *parameterized capacity/robustness characterization under a specific workload model*, rather than a discovery of new scaling laws. The paper would benefit from sharpening the novelty claim: the DES is not needed to show \(O(1)\) overhead ratio under those assumptions, but it *is* needed to quantify burstiness, tail latency, AoI tails, and correlated-loss effects.

Finally, the sectorized mesh comparator is a helpful addition that makes the evaluation less “strawman vs. bound” (Section III-D and Section V-A). However, the sector model is still fairly stylized (sector size \(\sqrt{N}\), capped neighbors = 10, coordinator defined as “first node”), and the conclusions about “architectural convergence” would be stronger if the sectorization were tied to orbital geometry and conjunction screening volumes more concretely.

---

## 2. Methodological Soundness — **Rating: 3/5**

The simulation framework is clearly described and appears reproducible at a high level (Tables III/IV: parameters, abstraction scope, traffic accounting; Section III-A event model; Section III-E Monte Carlo). The separation between message-layer offered load, MAC efficiency \(\gamma\), and physical link rate is a good practice and avoids a common pitfall. The closed-form cross-check (Section IV-E / Eq. (26)) is also useful for implementation verification.

However, several methodological choices materially shape the results and need stronger justification or sensitivity treatment:

1) **Cycle-aggregated DES with strict per-cycle deadline cap** for coordinator ingress (Section IV-G). This is effectively a “hard real-time batching” model; it amplifies burstiness penalties and drives the 50 kbps unscheduled threshold. That may be conservative, but the paper should either (i) justify why unused capacity cannot be carried over (token bucket/leaky bucket), or (ii) present both models and show how thresholds shift. Right now, the coordinator sizing result is sensitive to that design decision.

2) **Workload model dominance by per-node-per-cycle 512 B commands** (stress case). This assumption drives \(\eta\approx 46\%\) and makes overhead nearly invariant to cluster size (Section IV-B). It is acceptable as an upper bound, but it should be more explicitly tied to plausible operational modes (e.g., maneuver campaigns, differential-drag station-keeping) and contrasted with more realistic command sparsity distributions (burst campaigns, spatial correlation, per-cluster commands). The “event-driven” profile uses i.i.d. per-node events with \(p=0.01\), which may underrepresent correlated conjunction campaigns.

3) **Statistical treatment is somewhat mismatched to model stochasticity.** The manuscript reports 30 Monte Carlo runs and bootstrap CIs, but also states SD < 0.001% for overhead and that the model is near-deterministic (Section III-E). For many metrics, the uncertainty of interest is model-form (MAC, geometry, contact schedules), not sampling error. Consider reducing emphasis on bootstrap CIs and instead presenting structured sensitivity/uncertainty bands for the dominant assumptions (e.g., \(\gamma\), contact duty factors, deterministic occlusion, correlated events).

Reproducibility is close but not complete: the code link is “commit hash [PENDING]” (Data Availability). For IEEE T-AES review standards, a fixed artifact version (tag/commit) is important.

---

## 3. Validity & Logic — **Rating: 3/5**

Most conclusions follow logically from the stated model. In particular: (i) constant overhead ratio under fixed-depth hierarchy and fixed per-node traffic is correct; (ii) retransmission effectiveness under i.i.d. vs burst losses is correctly explained (Section IV-L); (iii) AoI heavy tails under Bernoulli exception reporting are expected and well illustrated (Section IV-F). The manuscript is also commendably explicit that some baselines are bounds, not competitors (Section I-C, Table IV).

The main validity concern is *interpretation drift* from “within this abstraction” to “actionable sizing” without sufficiently bounding dependence on unmodeled physical effects. Two examples:

- **Latency numbers** (e.g., 340–675 ms in Table IV-B) are dominated by “regional coordinator burst queueing near end of cycle” (Section IV-B). But this burstiness is an artifact of the cycle-aggregated reporting and summary timing (and perhaps of how regional ingest is modeled). In a real system with pipelined reporting, staggered cluster schedules, or continuous-time aggregation, the latency distribution could differ substantially. The paper should clarify whether the regional queueing is a modeling artifact (synchronous end-of-cycle summaries) versus an inherent architectural property.

- **AoI-to-km mapping** (Section IV-F “Orbital context”) is presented as a concrete consequence (2.6–3.5 km along-track after 440 s). This is plausible, but currently not derived from an explicit dynamics/estimation model and may be misleadingly specific. Since the paper explicitly defers orbital perturbation realism, the mapping should be framed as an order-of-magnitude illustrative calculation with clear assumptions (drag regime, ballistic coefficient dispersion, estimator model), or moved to a sensitivity box/appendix.

The paper’s limitations section is candid (Section V-C), but the strongest claims in Abstract/Contributions could be more consistently hedged to remain within the message-layer scope, especially around “coordinator capacity sizing” and “requires simulation beyond closed-form analysis.” The 2× coordinator threshold reduction indeed requires modeling intra-cycle burstiness, but it also depends heavily on the chosen deadline/cycle model and access assumptions.

---

## 4. Clarity & Structure — **Rating: 4/5**

The manuscript is generally well organized, with clear separation of topology models, traffic accounting, metrics, and results. The “Baseline Interpretation Note” (Section I-C) is particularly helpful and should reduce reviewer confusion about strawman baselines. Tables are detailed and mostly consistent with the narrative (e.g., Tables on traffic accounting and overhead composition are a strong point).

The abstract is dense but accurate and quantitative; for IEEE T-AES it is acceptable, though it risks overwhelming readers with several numbers and acronyms at once. Consider slightly reducing abstract complexity by moving one of the three headline results (e.g., GE vs Bernoulli retransmission) into the introduction summary, or by tightening phrasing around what is DES-measured vs analytically computed.

A few clarity issues recur:

- Terminology around \(\eta\), “protocol overhead,” “total utilization,” “delivered \(\eta\)” vs “offered load” (Section IV-G / Table IV-K) is mostly correct but could be easier to follow with a single consistent notation table early (perhaps near Section III-H). Right now the reader must track multiple definitions across sections.

- The paper references several figures (e.g., architecture diagram, TDMA comparison, sensitivity sweep) that are not visible in the LaTeX review. Assuming they exist, ensure captions are self-contained and that axes/units match the text (especially for “effective overhead” vs “protocol overhead”).

---

## 5. Ethical Compliance — **Rating: 4/5**

The manuscript includes an explicit disclosure of AI-assisted ideation (Acknowledgment) and states that the concept is not validated in the current study. That is appropriate and transparent. There is no obvious ethical issue with the simulation study itself.

Two improvements are recommended for compliance and perception:

1) Consider moving the AI disclosure from the Acknowledgment into a brief “Use of AI tools” statement aligned with evolving IEEE guidance, clarifying that AI tools were used for ideation only (not for data generation, coding, or analysis), if that is the case.

2) The author block is “Project Dyson Research Team” with a footnote that names/affiliations will be provided later. IEEE typically requires authorship transparency during review (even if double-blind is not used, T-AES is generally single-blind). If the venue requires named authors at submission, this should be corrected.

---

## 6. Scope & Referencing — **Rating: 4/5**

The topic fits IEEE Transactions on Aerospace and Electronic Systems: it intersects constellation operations, distributed coordination, and communications architecture. The paper also appropriately situates itself relative to mega-constellation networking (Handley, Del Portillo, Akyildiz), DTN/BPv7, and distributed algorithms.

Referencing is generally adequate and reasonably up-to-date, but there are a few gaps and some reliance on non-archival sources:

- Starlink/Kuiper/OneWeb operational claims are largely supported by non-archival webpages or conference presentations. For T-AES, it would be better to add archival or regulatory filings (FCC, ITU, published constellation architecture papers) where possible, especially for quantitative claims (e.g., “encountered coordination challenges during conjunction events”).

- The AoI literature is minimally cited (Kadota et al.). If AoI is a central metric, consider citing additional foundational AoI work (Kaul/Yates/Gruteser line of work) and any space-network AoI applications if available.

- For the coordinator bandwidth pooling/TDMA efficiency \(\gamma\), the citation to Akyildiz (2003) is not a strong match for modern optical ISLs. Consider adding more recent ISL/MAC references (optical crosslink scheduling, contact planning, or LEO laser terminal performance papers).

---

## Major Issues

1) **Coordinator bandwidth “50 kbps vs 24 kbps” depends strongly on a strict per-cycle deadline byte-cap model.**  
   Location: Section IV-G (“deadline-constrained byte budget”), Table IV-G, Table IV-H, Section IV-J.  
   Why it matters: The main engineering sizing claim could shift materially under alternative but plausible models (token bucket with carry-over; pipelined aggregation; staggered member schedules; continuous-time service).  
   What to change: Add at least one alternative coordinator service model and show sensitivity of the zero-drop threshold. At minimum, justify why strict per-cycle caps reflect the intended control loop and why carry-over is invalid.

2) **Latency results appear dominated by synchronous burst arrivals at regional coordinators, which may be a modeling artifact.**  
   Location: Section IV-B “regional burst arrivals near end of each coordination cycle” explanation; Table IV-B shows discrete jumps.  
   Why it matters: If the burst is an artifact of assuming all clusters summarize at the same time, the latency conclusions (and the cluster-size “optimization”) may not generalize.  
   What to change: Specify the timing of summary generation/forwarding. Consider adding a “staggered cluster schedule” experiment (randomize cluster summary times within the cycle) and show how latency distributions and the \(k_c\) trade change.

3) **Exception-based telemetry modeled as i.i.d. Bernoulli per cycle is too disconnected from orbital dynamics to support operational AoI conclusions.**  
   Location: Section IV-F and Abstract/Contributions statements about \(p_{\text{exc}}=0.10\) causing P99 AoI > 400 s and km-scale uncertainty.  
   Why it matters: The AoI tail is mathematically correct for Bernoulli sampling, but mapping \(p_{\text{exc}}\) to real spacecraft behavior is the key engineering step; without it, the “nominal 5% overhead” point may be unrealistic or misleading.  
   What to change: Either (i) keep AoI results but remove/soften the km mapping and position it strictly as “given \(p_{\text{exc}}\)”; or (ii) add a simple dynamics-driven exception model (e.g., threshold crossings from a bounded random-walk or Gauss–Markov perturbation in along-track error) to relate \(p_{\text{exc}}\) to physical parameters.

4) **Global-state mesh “upper bound” traffic model mixes gossip convergence arguments with a hard batch cap in a way that may overstate required traffic.**  
   Location: Section III-C and Table III-A (“\(R_{\text{conv}}=\max(\lceil\log_2 N\rceil,\lceil N/(bf)\rceil)\)”).  
   Why it matters: You intend it as an upper bound, but reviewers may challenge the derivation and the choice \(f=O(N/\log N)\) plus batch cap.  
   What to change: Tighten the argument: explicitly define the state model (full \(N\) entries) and show a lower bound on per-node bytes per cycle independent of protocol (information-theoretic: each node must receive \(\Omega(N)\) entries). Then present your gossip accounting as one realizable scheme, not *the* requirement.

---

## Minor Issues

- **Inconsistency/possible error in Table IV-K narrative:** In “Results Without Retransmission,” it states delivered overhead falling to 16.9% at \(p_{\text{link}}=0.8\), but Table IV-K shows delivered \(\eta=36.8\%\) for \(p_{\text{link}}=0.8, M_r=0\). (Section IV-I, “Results Without Retransmission”). Please reconcile.

- **Coordinator ingress demand calculation uses \(k_c\) vs \(k_c-1\)** inconsistently. In Section IV-G you compute demand as \(k_c \times 256 \times 8/T_c = 20.48\) kbps; later TDMA uses \((k_c-1)\). Clarify whether the coordinator itself also sends a “member report” in that cycle and whether it is included in ingress.

- **Traffic accounting table entry “Gossip exchange (mesh) size \(256\times f\)”** (Table III-I) seems dimensionally off: message size should be \(256\times b\) (batch), not \(256\times f\) (fanout). You use \(256\times b\) elsewhere (Table III-A). Fix to avoid confusion.

- **AoI sampling method:** Table IV-F says “AoI sampled every 100 s.” For a 10 s cycle, this may miss some dynamics; explain why 100 s is sufficient and whether percentiles are stable vs sampling interval.

- **Authorship/affiliation placeholder** may violate submission requirements; ensure anonymization policy matches the journal.

- **Non-archival citations**: Starlink ops, DARPA pages, etc. are acceptable as context, but key quantitative claims should lean on archival/regulatory sources where possible.

---

## Overall Recommendation — **Major Revision**

The paper is promising and contains several potentially publishable engineering insights (coordinator capacity sizing under burstiness/TDMA, AoI-tail trade-offs, correlated-loss retransmission limits). However, the strongest headline results are currently too sensitive to modeling choices that are either (i) not sufficiently justified (strict per-cycle cap, synchronous summary bursts), or (ii) not sufficiently tied to physical/operational reality (exception telemetry parameterization, AoI-to-position uncertainty mapping). Addressing the major issues above would substantially improve credibility and generalizability and would likely move the manuscript toward acceptance.

---

## Constructive Suggestions

1) **Add a “staggered scheduling” experiment**: randomize member transmit slots and/or cluster summary forwarding times within the cycle (and optionally across regions). Report how this changes (i) coordinator zero-drop threshold under unscheduled access, and (ii) regional queueing latency and the \(k_c\) sensitivity in Table IV-B.

2) **Introduce an alternative coordinator service model** (token bucket with carry-over, or continuous-time service with deadline constraint on computation). Provide a small sensitivity table showing how the 50 kbps unscheduled threshold shifts. This will make the coordinator sizing claim robust rather than model-specific.

3) **Ground exception telemetry in a minimal dynamics/estimation model**: e.g., along-track prediction error evolving as Gauss–Markov with threshold-triggered reporting. Then \(p_{\text{exc}}\) becomes an output of physical parameters (process noise, threshold), and AoI can be linked to conjunction screening false-alarm probability more defensibly.

4) **Strengthen the decentralized upper-bound argument**: add an information-flow lower bound for “full-state awareness” (each node must receive \(\Omega(N)\) entries per update horizon), then present the gossip/batch calculation as one instantiation. This will reduce vulnerability to protocol-specific critiques.

5) **Fix internal consistency and notation**: correct the delivered-\(\eta\) discrepancy in Section IV-I, harmonize \(k_c\) vs \(k_c-1\) in ingress calculations, and unify the definitions of \(\eta\), \(\eta_{\text{total}}\), \(\eta_{\text{eff}}\), “delivered,” and “offered” in a single table near Section III-H.