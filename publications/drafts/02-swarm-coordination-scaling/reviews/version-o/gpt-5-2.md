---
paper: "02-swarm-coordination-scaling"
version: "o"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-02-24"
recommendation: "Unknown"
---

## 1. Significance & Novelty — **Rating: 3/5 (Adequate)**

The manuscript targets an important and timely problem: coordination scaling for mega-constellations and future large autonomous swarms. Framing the study around \(10^3\)–\(10^5\) nodes and explicitly contrasting centralized vs. hierarchical vs. an intentionally pessimistic decentralized bound is useful for readers who need first-order architectural intuition. The paper’s strongest “engineering” contribution is not the asymptotic result (which is largely implied by the assumed message model), but the attempt to quantify constants (e.g., \(\eta \approx 20.66\%\)) and identify parameter regimes (cluster size, duty cycle, coordinator bandwidth).

However, the novelty claim “No prior work has systematically compared coordination architectures across this range of scales using quantitative simulation” (Introduction) is too strong as written. There is relevant work in mega-constellation networking/routing, DTN, and distributed control that performs scaling studies (even if not identical metrics/topologies). The paper would benefit from a more careful positioning: what is uniquely contributed here is *a particular DES traffic-accounting comparison with explicit byte counts under a fixed coordination-cycle abstraction*, rather than “no prior work” broadly.

A second novelty concern is that the central headline—constant overhead with hierarchical aggregation—follows almost directly from the modeling choice “each node contributes 1 kbps, each cycle generates \(O(N)\) traffic.” The DES then primarily verifies implementation consistency and queue stability under simplified assumptions. That can still be publishable, but the manuscript should more explicitly treat the DES as a *parameterized accounting/feasibility study* and avoid implying discovery of emergent scaling behavior.

---

## 2. Methodological Soundness — **Rating: 2/5 (Needs Improvement)**

The paper is commendably explicit about what is modeled vs. abstracted (Table “Simulation Abstraction Scope”), provides parameter tables, and defines metrics carefully (Section “Performance Metric Definitions”). The separation between baseline telemetry and protocol overhead (\(\eta\)) is clear and, in principle, appropriate for isolating topology-dependent costs. The coordinator bandwidth stress test (Section “Coordinator Bandwidth Stress Test”) is also a valuable addition because it exposes a key hidden constraint in hierarchical systems: coordinator ingest is not “1 kbps like everyone else.”

That said, several methodological choices substantially weaken the quantitative credibility of the results:

1) **Event volume vs. runtime inconsistency.** The “Full-Participation Simulation Note” claims \(\sim 3.15\times 10^{11}\) node-cycle events for \(N=10^5\) over one year at \(T_c=10\) s, yet also claims ~7 s runtime/run. That is not plausible unless the simulator is *not* processing per-node per-cycle events as discrete events (i.e., it must be aggregating analytically per cycle). If the simulator is aggregating, then many “DES” claims should be reframed as *cycle-based accounting* rather than discrete-event processing at per-message granularity. This is a major reproducibility/credibility issue: the paper must precisely describe the computational approach (per-message events vs. aggregated batch accounting) and reconcile the runtime claim.

2) **Queueing model mismatch at regional level.** The latency explanation attributes ~500 ms to “burst arrivals … near the end of each coordination cycle.” But earlier the model introduces random phase offsets within \([0,T_c)\) to approximate Poisson arrivals (Palm–Khintchine) for centralized processing. Those two statements are in tension: if cluster summaries are generated/forwarded in a synchronized way, you get bursts; if they are phase-randomized, you should not get large periodic bursts. The manuscript needs to specify whether *cluster-to-regional* summary transmissions are synchronized, and if so, why (protocol design), and then the queueing analysis should reflect a *bulk-service / batch-arrival* model rather than \(M/D/1\)-like intuition. As written, the latency results in Table “Hierarchical Protocol Overhead and Latency vs. Cluster Size” (discrete jumps 340 vs 508 vs 675 ms) look like artifacts of a particular scheduling assumption that is not fully documented.

3) **Traffic accounting vs. \(\eta\) interpretability.** Excluding status reports from \(\eta\) is defensible for topology comparison, but many conclusions use \(\eta\) as if it were “coordination overhead” in an engineering sense (Abstract, Contributions, multiple places in Results/Conclusion). Since baseline telemetry is 20.5% of the channel, the system is already at ~41% utilization in the default case; any MAC/PHY overhead pushes this higher. For a reader, “\(\eta=20.66\%\)” can be misinterpreted as “only 20% used.” The paper does mention total utilization, but the narrative emphasis repeatedly returns to \(\eta\). Consider elevating *total* utilization as the primary metric and using \(\eta\) as a decomposition term.

4) **Monte Carlo and confidence intervals are not meaningful for the key outputs.** The paper correctly notes near-deterministic behavior and tiny SD. But then it still reports bootstrap CIs, which may give a misleading sense of statistical rigor. The dominant uncertainty is model-form error (MAC, correlated outages, geometry), not sampling error. The paper should either (i) remove most CI emphasis and instead present sensitivity analyses over uncertain parameters, or (ii) introduce stochastic elements that actually drive variance (e.g., correlated link outages, time-varying contact graphs).

---

## 3. Validity & Logic — **Rating: 3/5 (Adequate)**

The logical structure—define architectures, define metrics, run comparative simulations, then do hierarchical parameter sweeps—is coherent. The manuscript is generally careful to label centralized and mesh cases as “reference bounds,” and it acknowledges that the mesh model is an upper bound that overstates decentralized costs (Baseline Interpretation Note; Section “Sectorized Mesh”). The coordinator bandwidth section appropriately highlights that the hierarchical architecture only “works” if coordinators can ingest much more than 1 kbps, which is a critical practical point.

Nevertheless, several conclusions are overstated relative to what is actually demonstrated:

- The statement that the DES “confirms the absence of queueing-induced nonlinearities” (Abstract, Contributions, Results) is only true within a simplified message-passing abstraction and under fixed service rates that appear comfortably underutilized (e.g., \(\mu_c=200\) msg/s with \(\lambda_c=10\) msg/s). It is not surprising that no nonlinearities appear. To make this claim meaningful, the paper should show stress regimes where nonlinearities *could* appear (e.g., higher \(r\), heavier collision-alert loads, coordinator service-time heterogeneity, or finite link scheduling) and then show where the inflection occurs.

- The “global-state mesh exceeds bandwidth beyond \(10^5\)” argument depends heavily on the chosen fanout and the assumption that each gossip exchange includes \(256\times f\) bytes (Table “Traffic Accounting”). But if global state is required, the payload per exchange should scale with \(N\) unless you assume incremental deltas/compression. Conversely, if you assume deltas, the \(O(N^2)\) upper bound may still hold in information-theoretic terms, but the constant factors can change dramatically. The mesh baseline is acceptable as an upper bound, but the manuscript should be more explicit that the mesh parameterization is not a standard optimized epidemic protocol and is intentionally pessimistic.

- The retransmission analysis (Section “Link Availability Sensitivity”) treats losses as i.i.d. Bernoulli per message and retransmissions as simply extra attempts within \(T_c\). In real ISL systems, losses are correlated (occlusions, pointing interruptions), and retransmissions consume scheduling resources and may not fit within the same cycle without preemption. The offered-load column is a good idea, but the approximation in the table footnote should be replaced by an explicit formula derived from geometric series (expected number of transmissions given retry limit) and then validated against the DES implementation.

Overall, the conclusions are directionally reasonable, but the paper needs tighter alignment between what is proven (under a simplified accounting model) and what is hypothesized for real systems.

---

## 4. Clarity & Structure — **Rating: 4/5 (Good)**

The manuscript is generally well organized and readable. The “Baseline Interpretation Note” is a strong addition that prevents unfair comparisons. Tables are plentiful and usually self-contained; Table “Simulation Parameters” and “Traffic Accounting” are especially helpful. The abstract is dense but informative and largely consistent with the body (with the caveat that some numbers—e.g., \(\eta\) vs total utilization—can be misread).

A few clarity issues reduce accessibility:

- The paper mixes queueing-theory notation and link-capacity notation in ways that can confuse readers (e.g., centralized processing capacity \(C\) in msg/s vs. coordinator link capacity \(C_{\text{coord}}\) in kbps; later “\(C_{\text{node}}=1\) kbps” is a budget). Consider renaming processing capacities to \(\mu\) consistently and reserving \(C\) for bit rates.

- The latency metric is sometimes described as “message processing latency” and sometimes “end-to-end latency,” and it is not always clear which message path is being measured (node→cluster vs cluster→regional vs end-to-ground). Table “Hierarchical Protocol Overhead and Latency vs Cluster Size” should specify exactly which latency is reported.

- Figures referenced (architecture diagram, overhead scaling, latency distribution, etc.) are not visible in the LaTeX excerpt, so I can only assess captions. Captions are generally good, but a few embed key caveats that should be in the main text (e.g., Fig. “latency distribution” includes an analytical extrapolation to \(10^6\); this should be more prominent in the Results narrative to avoid readers treating it as simulated).

---

## 5. Ethical Compliance — **Rating: 4/5 (Good)**

The manuscript includes an explicit disclosure of AI-assisted ideation in the Acknowledgment, naming tools and clarifying that the concept is not validated in the present study. That is aligned with emerging IEEE expectations, and the disclosure is appropriately bounded (it does not claim AI-generated results).

Two improvements are advisable for IEEE T-AES norms:

- Add a short statement clarifying whether AI tools were used for *writing/editing* the manuscript text, code generation, or only “ideation,” and confirm that authors verified all technical content. This avoids ambiguity.

- The “Project Dyson Research Team” placeholder author list is understandable for anonymized review, but the final version must include affiliations and any potential conflicts (e.g., organizational advocacy for “Project Dyson” concepts). Consider adding a brief COI statement in the final submission.

---

## 6. Scope & Referencing — **Rating: 3/5 (Adequate)**

The topic is appropriate for IEEE Transactions on Aerospace and Electronic Systems, particularly given the intersection of constellation operations, distributed coordination, and communication constraints. The paper also uses queueing theory and DES—both within scope for T-AES when tied to aerospace systems.

Referencing is mixed. Foundational citations (Lynch, Kleinrock, Demers gossip, DTN/BPv7, consensus) are appropriate. However:

- Several key operational claims rely on non-archival web sources (SpaceX Starlink ops page; Amazon overview; DARPA program pages). Those are acceptable as context, but the core technical argument would benefit from more peer-reviewed/archival sources on mega-constellation operations, ISL link availability, and conjunction screening workload statistics.

- Some citations appear tangential or not directly used (e.g., Akyildiz 2003 multicast routing is cited for TDMA efficiency; that’s not clearly the right reference for MAC efficiency factors in modern optical ISLs). Consider adding more recent sources on LEO ISL networking and MAC/scheduling, and on conjunction assessment pipelines.

- The “no prior work” claim should be softened and supported with a more comprehensive related-work discussion of constellation network simulations and distributed spacecraft autonomy demonstrations (including any recent AIAA/ION/SpaceOps proceedings if available).

---

## Major Issues

1. **Clarify and correct the simulation/event-processing model (critical).** The claimed number of events (\(\sim 3\times 10^{11}\)) vs. runtime (seconds) is inconsistent. You must explicitly state whether the simulator is (a) true per-message DES with a priority queue, (b) cycle-based batch accounting, or (c) a hybrid. Provide algorithmic complexity and what constitutes an “event.” This affects the credibility of “DES” claims and reproducibility.

2. **Resolve the regional latency/burstiness inconsistency.** The paper simultaneously relies on randomized phase offsets (to justify Poisson arrivals) and on burst arrivals (to explain dominant regional queueing). Specify the scheduling of cluster summaries and commands (synchronous vs asynchronous), and if bursts are intrinsic, use an appropriate batch-arrival queueing interpretation or show sensitivity to scheduling (e.g., randomizing summary send times).

3. **Strengthen the mesh baseline definition or narrow claims.** The “global-state mesh” should be more carefully parameterized: what exactly is in a gossip payload (full state vs deltas), how many peers per round, and what convergence criterion. As an “upper bound,” it’s acceptable, but then comparative statements must consistently label it as such and avoid implying it represents decentralized best practice.

4. **Reframe statistical reporting.** Bootstrap CIs on near-deterministic outputs add little and can mislead. Replace with sensitivity/uncertainty analysis over key engineering uncertainties (MAC efficiency \(\gamma\), reporting rate \(r\), message sizes, coordinator service rates, correlated outages).

5. **Coordinator bandwidth and scheduling need tighter integration.** The coordinator “50 kbps for zero drop” result is primarily an artifact of unscheduled random arrivals. Since the paper already argues TDMA is required, you should either (i) implement a minimal TDMA slot model, or (ii) present the TDMA case analytically alongside the unscheduled case and make TDMA the primary engineering conclusion.

---

## Minor Issues

- **Notation conflict:** Centralized processing uses \(C\) as msg/s capacity (Eq. (1)), later \(C_{\text{coord}}\) is kbps, and \(C_{\text{node}}=1\) kbps is a budget. Consider consistent notation: \(\mu\) for msg/s service rates; \(R\) for bit rates.

- **MTTF arithmetic/interpretation:** “2% annual failure rate ⇒ MTTF 50 years” is fine under exponential assumption, but in LEO many failures are early-life/bathtub shaped. You note correlated failures later; consider acknowledging non-exponential hazard shapes in the limitations.

- **Table “Coordination Topology Comparison”:** The mesh “Scalability limit \(\sim 100{,}000\)” is presented as if a hard threshold; it is parameter-dependent. Consider removing the single number or explicitly tying it to your assumed fanout/payload.

- **Link retransmission offered-load formula:** The footnote approximation in Table “Coordination Success and Overhead vs. Link Availability” should be replaced with an explicit expected-transmissions expression:
  \[
  \mathbb{E}[X]=\sum_{i=1}^{M_r+1} i(1-p)^{i-1}p + (M_r+1)(1-p)^{M_r+1}
  \]
  and then offered load \(=\eta_{\text{base}}\mathbb{E}[X]\). Also clarify whether retransmissions consume additional coordinator processing and queueing.

- **Abstract density:** Consider splitting into (i) what is simulated vs. analyzed, (ii) primary quantitative results, (iii) key limitations. Right now several caveats appear later and could be missed.

- **“Propagation latency 10–240 ms”**: depends strongly on architecture and gateway placement; if used as a key motivation, cite an archival source and specify assumptions (gateway proximity, bent-pipe vs routed).

---

## Overall Recommendation — **Major Revision**

The problem is important and the manuscript has several strong engineering-oriented elements (explicit traffic accounting, coordinator ingest bottleneck, clear baseline caveats). However, core aspects of the methodology and interpretation need substantial clarification and, in places, correction—especially the simulator’s actual event model, the latency/burstiness assumptions, and the over-reliance on near-deterministic MC statistics. With these issues addressed and with either a minimal TDMA scheduling model or a tighter analytical scheduling treatment, the paper could become a solid T-AES contribution.

---

## Constructive Suggestions

1. **Add a “Simulator mechanics” subsection with pseudocode and complexity.** State precisely: what is an event, what is queued, what is aggregated per cycle, and how byte counts/latencies are computed. Reconcile event counts with runtime; this will greatly improve credibility and reproducibility.

2. **Implement (or analytically model) TDMA within \(T_c\) for intra-cluster reporting.** Since you already conclude contention-based access is unsuitable, show results under scheduled slots (drops vs \(C_{\text{coord}}\), latency impacts, guard time via \(\gamma\)). Make TDMA the default and keep random-phase as a “worst-case unscheduled” stress test.

3. **Replace CI-heavy reporting with sensitivity bands.** For example, plot \(\eta_{\text{total}}\) as a function of \(r\), message sizes, and \(\gamma\); show when total utilization approaches stability limits. This will be more informative than \(<0.01\%\) SD.

4. **Tighten the mesh baseline specification and add a sectorized mesh “toy” simulation.** Even a simplified sectorized mesh (fixed sectors, neighbor-limited gossip, occasional inter-sector summary exchange) would provide a much more informative decentralized comparator than the global-state upper bound and would strengthen RQ3 substantially.

5. **Clarify latency metrics and paths.** For each latency table/figure, specify which message(s) are measured (node→cluster, cluster→regional, end-to-ground), and provide 50/95/99th percentiles. If regional queueing dominates due to synchronization, make that a design insight: “avoid synchronized summary bursts by jittering/slotting summaries.”