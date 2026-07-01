---
paper: "02-swarm-coordination-scaling"
version: "m"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-02-24"
recommendation: "Unknown"
---

## 1. Significance & Novelty — **Rating: 3/5 (Adequate)**

The manuscript targets an important and timely problem: coordination architectures for very large autonomous spacecraft swarms (10³–10⁵, with discussion toward 10⁶). The focus on *engineering design parameters* (cluster size, duty cycle, coordinator bandwidth, link availability) and on *byte-counted overhead* via DES is potentially valuable to the T-AES readership, particularly given the rapid growth of mega-constellations and renewed interest in autonomous operations.

However, the core “scaling” result—constant overhead ratio for a fixed-depth hierarchy with per-node bandwidth scaling linearly with \(N\)—is largely an algebraic consequence of the modeling choices (as the authors acknowledge explicitly in Section IV-D). As written, the novelty is less in discovering scaling laws and more in quantifying constants under a chosen message model and showing queue stability *within that abstraction*. That can still be publishable, but the paper must more clearly position itself as a *parameterized engineering trade study under a message-layer abstraction*, not as a general scaling characterization of hierarchical coordination.

The comparison baselines are explicitly framed as bounds, which is intellectually honest, but it also reduces the strength of comparative claims. Since sectorized/locality-aware decentralized approaches are not simulated, the paper does not yet provide the “systematic comparison” across realistic architecture alternatives implied in the Introduction (Section I-A). The contribution would be significantly strengthened by at least one simulated “middle-ground” decentralized comparator (even simplified), or by narrowing the claims to “hierarchical parameter study + stress tests” rather than “architecture comparison.”

---

## 2. Methodological Soundness — **Rating: 2/5 (Needs Improvement)**

Reproducibility and accounting discipline are relative strengths: the manuscript defines a consistent overhead metric \(\eta\) (Section III-F/III-H), enumerates message types (Table 7), and states “full-participation” simulation with 30 replications. The explicit coordinator bandwidth stress test (Section IV-G) and the offered-vs-delivered distinction under retransmissions (Section IV-F, Table 11) are also methodologically sound and practically relevant.

That said, several modeling choices undermine the rigor of the DES as evidence for the stated research questions, especially RQ1 (“latency distribution and fault tolerance”) and RQ3 (“relative to baselines”). Key concerns:
- **Deterministic periodic traffic vs queueing claims.** Nodes report once per \(T_c\) with random phase; the paper argues Palm–Khintchine yields Poisson-like arrivals centrally (Section III-B1). That may hold for the centralized baseline, but hierarchical coordinators aggregate *synchronized periodic* arrivals at the cluster level, and the burstiness within each cycle is central to coordinator bandwidth drops (Section IV-G). Yet the queueing model is still largely \(M/D/1\)-style reasoning with fixed service rates; the DES appears to be doing most work, but the paper does not provide enough detail on the service discipline, serialization modeling, and whether coordinator ingress/egress share the same server/link. This is critical because coordinator saturation is a main design outcome.
- **Latency modeling is under-specified and appears inconsistent with space geometry.** Reported mean latencies of ~340–675 ms (Table 9) are not reconciled with the stated propagation delays of a few milliseconds for intra-cluster links (Section IV-F). If most latency is queueing/processing, then service rates and scheduling assumptions must be explicit and validated. If most latency is propagation, then distances/geometry assumptions must be stated. Currently, the latency numbers read as “plausible” but not justified.
- **Monte Carlo is largely unnecessary as implemented.** The manuscript itself notes SD < 0.001% for overhead and that failures barely perturb per-cycle metrics (Section III-D, IV-D). If the stochasticity is negligible, then reporting tight confidence intervals can be misleading: it suggests statistical certainty, but the dominant uncertainty is *model form error* (MAC, link acquisition, correlated outages, orbital dynamics, priority traffic), not sampling error. A better approach would be structured sensitivity/uncertainty analysis over key parameters (message sizes, \(T_c\), service rates, buffer sizes, MAC efficiency), rather than 30 replications of a near-deterministic configuration.
- **Mesh baseline is not a DES peer.** The “global-state mesh” is framed as an upper bound, but it mixes gossip convergence arguments with bandwidth accounting and introduces assumptions like \(f=O(N/\log N)\) (Section III-B3) that are not operationally motivated. If it is an upper bound, it should be presented as an analytical bound with clear derivation, not as a simulated topology with parameter sweeps that may not correspond to any deployable protocol.

Overall, the methods are promising but require stronger specification of the DES mechanics (server/link models, contention model at coordinators, per-tier scheduling, how bytes map to time), and a shift from Monte Carlo replication toward parametric robustness.

---

## 3. Validity & Logic — **Rating: 3/5 (Adequate)**

Many conclusions are logically consistent with the stated abstraction. The paper is careful in multiple places to say “within the message-passing abstraction” (e.g., Abstract; Section IV-D; Limitations). The offered-load framing for coordinator bandwidth and retransmission is correct and helps prevent misinterpretation. The “baseline interpretation note” (Section I-C) is a strong element: it prevents over-claiming against strawman competitors.

However, several conclusions are currently overstated relative to what the DES actually establishes:
- **“Absence of queueing-induced nonlinearities”** (Abstract, Section IV-D) is only shown for the specific service-rate parameterization and in the absence of MAC scheduling and correlated outages. Yet later results (Section IV-G) show strong nonlinear drop behavior when coordinator bandwidth is constrained—suggesting nonlinearities *do* emerge once a more physical constraint is introduced. The paper should reconcile these: queue stability in the *processing queue* may hold, but *link scheduling/ingress constraints* cause nonlinearities; both matter for real systems.
- **Cluster-size explanation conflicts with overhead definition.** In Section IV-B, overhead invariance is attributed to intra-cluster status reporting dominating messages. But baseline telemetry (status reports) is explicitly excluded from \(\eta\) (Table 7; Section III-F). If ephemeris reports are excluded from \(\eta\), they cannot be the dominant contributor to \(\eta\). This is a major internal logic inconsistency affecting interpretation of Figures/Tables on overhead decomposition (e.g., Fig. 8 and the text claiming intra-cluster dominates “overhead”).
- **Coordinator handoff modeling likely underestimates control-plane disruption.** Handoff state transfer is 10–50 MB over 1–10 Gbps optical ISL, taking 1–10 s (Section III-B2, metric definitions). But the coordination cycle is 10 s, and the paper claims routine coordination is deferred during handoff while collision avoidance continues via direct comms. The DES should demonstrate (or at least quantify) how often handoffs overlap with cycles, what fraction of cycles are missed, and how that impacts “coordination success,” especially for short duty cycles (Table 10). Right now, handoff “success” is described probabilistically but without a clearly defined failure model for optical ISLs, nor how that probability is computed from message loss/bit error.
- **Extrapolation to \(10^6\)** in Fig. 3 is explicitly analytical, which is fine, but the paper uses it to discuss tail latency at 10⁶. Given the uncertainty in unmodeled physical-layer effects, that figure risks being over-interpreted. Consider removing the 10⁶ curve or clearly separating it as a non-result.

The manuscript is close to valid within its model, but it needs internal consistency fixes (especially \(\eta\) composition) and tighter linkage between modeled mechanisms and claims.

---

## 4. Clarity & Structure — **Rating: 4/5 (Good)**

The paper is generally well organized, with clear sectioning, explicit research questions, and frequent signposting of assumptions. Tables summarizing parameters (Table 5) and abstraction scope (Table 6) are helpful. The “Baseline Interpretation Note” (Section I-C) is unusually clear and should be retained.

The abstract is dense but informative; it reports key numeric outcomes and caveats. That said, it contains several quantities whose definitions are only later clarified (e.g., \(\eta\), “baseline telemetry,” “MAC-adjusted”), and it mixes delivered vs offered load concepts. A small reorganization in the abstract (define \(\eta\) and “baseline telemetry excluded” in one clause) would improve readability.

Figures/tables are mostly effective, but several need consistency checks:
- The overhead range in Table 8 (hierarchical “2–13%”) conflicts with Table 12 showing \(\eta\approx 20.66\%\) baseline (unless “2–13%” refers to exception telemetry cases only). This reads like a versioning mismatch.
- Table 9 includes \(k_c=\{50,75,100,150,200,500\}\) but the sweep list includes 300 as well (Section III-D). Minor, but suggests results are incomplete or inconsistent.
- The manuscript references “Section V-E” in Section III-A, but the paper’s Discussion/Limitations subsections are not labeled with letters in the LaTeX provided. Ensure cross-references match IEEEtran conventions.

With a pass to remove inconsistencies and clarify metric definitions early, the paper would be quite readable for T-AES.

---

## 5. Ethical Compliance — **Rating: 4/5 (Good)**

The manuscript includes an explicit disclosure of AI-assisted ideation in the Acknowledgment and distinguishes ideation from validated results. That transparency is good practice. The “commit hash pending” in Data Availability is acceptable for a manuscript stage but should be resolved before publication.

Potential ethical/compliance issues to address:
- **Authorship/affiliation placeholder.** The author block says names/affiliations will be provided later. For review this is fine, but for IEEE compliance the final version must include full authorship and COI disclosures; consider adding a statement that no conflicts exist (if true) and that AI tools were not used to generate data/results/code (if true).
- **Non-archival references.** Several key claims rely on operator web pages or non-peer reviewed sources (Starlink ops, DARPA pages). That’s not unethical, but it can be problematic for archival scholarship; see “Scope & Referencing.”

Overall, no major ethical red flags, but tighten final compliance language.

---

## 6. Scope & Referencing — **Rating: 3/5 (Adequate)**

The topic is appropriate for IEEE Transactions on Aerospace and Electronic Systems, especially the intersection of autonomous spacecraft operations, networking, and system-level scalability. The paper cites foundational distributed systems and gossip literature (Lynch, Demers), queueing (Kleinrock), DTN/CCSDS, and some constellation networking work (Handley, Akyildiz, del Portillo). The inclusion of reliability data (Castet & Saleh) is also relevant.

However, several referencing gaps and scope mismatches limit the paper’s scholarly grounding:
- **Mega-constellation operations literature.** The paper makes operational claims about Starlink/Kuiper/OneWeb coordination but relies on non-archival sources. Consider adding more archival references on LEO constellation operations, autonomous stationkeeping, conjunction assessment pipelines, and ISL architectures (including recent AIAA/IAA/USENIX/ACM work).
- **MAC/ISL scheduling and satellite networking.** Since the coordinator bandwidth result is central, it should be situated in existing satellite MAC/ISL scheduling literature (TDMA framing, beam hopping, link acquisition overhead). Current citations are light and somewhat dated for ISL MAC realities.
- **Decentralized collision avoidance / SSA.** The mesh “global state for collision avoidance” assumption is plausible as an upper bound, but there is a large literature on conjunction assessment, screening volumes, covariance propagation, and distributed SSA concepts that could better justify the state requirements and message models.

The manuscript is in-scope, but it needs stronger archival anchoring and clearer separation between “engineering assumptions” and “established operational facts.”

---

## Major Issues

1. **Internal inconsistency in overhead metric \(\eta\) vs interpretation (critical).**  
   - Baseline ephemeris status reports are excluded from \(\eta\) (Table 7; Section III-F), yet Section IV-B and elsewhere attribute \(\eta\)’s invariance and dominance to intra-cluster status reporting. This is logically inconsistent and affects the interpretation of Table 9, Fig. 6, and the message decomposition narrative (Fig. 8).  
   **Required fix:** Re-derive and clearly present the decomposition of \(\eta\) using only “Yes” message types. If you want to discuss total channel utilization, use \(\eta_{\text{total}}=\eta + B_{\text{status}}\) consistently and decompose that instead.

2. **Coordinator bandwidth model is underspecified (ingress/egress, scheduling, burstiness).**  
   Section IV-G finds zero-drop requires \(C_{\text{coord}}\ge 50\) kbps for \(k_c=100\). But the DES assumptions about how coordinator bandwidth is shared across inbound/outbound, whether transmissions are slotted, and how “uniform random phase” interacts with coordinator capacity are not fully specified.  
   **Required fix:** Precisely define the coordinator link model: is \(C_{\text{coord}}\) aggregate (in+out) or per-direction? Is it enforced as a token bucket, per-cycle byte budget, or a queue with service time proportional to bytes? How is burstiness generated? Provide a schematic and pseudo-code-level description sufficient for reproduction.

3. **Latency results lack mechanistic explanation and validation.**  
   Table 9 reports ~340–675 ms mean latency, but the stated propagation delays for ISLs are milliseconds. The paper needs to explain what dominates latency (queueing? serialization? multi-hop?) and show that the latency model corresponds to realistic distances and link rates.  
   **Required fix:** Add a latency budget table (propagation + serialization + queueing per tier) for a representative configuration, and validate at least one component against a known analytical queueing result in the hierarchical case (not only centralized).

4. **Mesh “upper bound” is not presented in a way that is methodologically clean.**  
   The mesh section mixes analytical \(O(\cdot)\) arguments with DES claims but lacks a clear, reproducible mapping from “global state requirement” to bytes exchanged per gossip round and convergence criteria.  
   **Required fix:** Either (a) make mesh purely analytical as an upper bound with explicit derivation and remove DES-like comparisons, or (b) define a concrete protocol (state vector size, delta encoding, convergence threshold, fanout schedule) and simulate it comparably.

5. **Over-precision and emphasis on Monte Carlo CIs despite dominant model-form uncertainty.**  
   Reporting \(\eta=20.66\%\pm 0.01\%\) with SD < 0.001% suggests a level of certainty that is not meaningful given unmodeled MAC/link acquisition/correlated outages.  
   **Required fix:** Reframe uncertainty: keep deterministic coefficients, but add sensitivity bands over key parameters (MAC efficiency, header overhead, \(T_c\), message sizes, service rates). This will better serve engineering design.

---

## Minor Issues

- **Table 8 hierarchical overhead range “2–13%” conflicts with Table 12 \(\eta\approx 20.66\%\).** Check for outdated numbers or mismatched definitions (protocol overhead vs something else).
- **Section/figure cross-reference mismatch:** Section III-A cites “Section V-E,” but subsections are not lettered. Ensure LaTeX labels match.
- **Cluster size sweep mismatch:** Section III-D includes \(k_c=300\), but Table 9 omits it.
- **Equation/parameter naming:** \(C\) is used as messages/s processing capacity (centralized), while \(C_{\text{node}}\) is kbps bandwidth; \(C_{\text{coord}}\) is kbps. Consider renaming processing capacity to \(\mu\) consistently to avoid confusion.
- **Handoff state size inconsistency:** Section III-B2 says 10–50 MB; metric definitions say \(s_{\text{handoff}}=100k_c\) KB which gives 10 MB at \(k_c=100\) and 50 MB at \(k_c=500\) (consistent), but earlier text says “depending on cluster size” without stating the formula—add it once near first mention.
- **Non-archival citations used for key factual claims** (Starlink ops, DARPA pages). Consider demoting these to contextual statements and rely on archival sources where possible.

---

## Overall Recommendation — **Major Revision**

The paper has a solid premise, good transparency about baselines/abstraction, and potentially useful engineering results (especially coordinator bandwidth stress testing and offered-load framing under retransmission). However, there are major internal inconsistencies in the definition and interpretation of the primary metric \(\eta\), insufficient specification of the coordinator bandwidth and latency models, and an unclear methodological status of the mesh “upper bound.” These issues materially affect the validity and interpretability of the main claims and require substantial revision to meet T-AES standards.

---

## Constructive Suggestions

1. **Fix and standardize metrics: introduce \(\eta_{\text{protocol}}\) and \(\eta_{\text{total}}\) and use them consistently.**  
   Rework Section III-F/III-H and all Results text so that:  
   - \(\eta_{\text{protocol}}\) excludes baseline telemetry (as intended), and its decomposition includes only “Yes” messages.  
   - \(\eta_{\text{total}}=\eta_{\text{protocol}} + B_{\text{status}}\) is used for link sizing and “channel utilization” claims.  
   Then update Fig. 8/message decomposition to match the corrected metric.

2. **Add a “DES mechanics” subsection with enough detail to reproduce timing and drops.**  
   Include: event scheduling within \(T_c\), per-link serialization model, whether links are full duplex, queue disciplines, how \(C_{\text{coord}}\) is enforced, and how buffer overflow interacts with retransmissions. A short algorithm box/pseudocode would help.

3. **Provide a latency budget and validate hierarchical queueing against an analytical approximation.**  
   For one representative configuration (e.g., \(N=10^5, k_c=100\)), break latency into propagation/serialization/queueing at node→cluster, cluster→regional, regional→ground. If queueing dominates, show that an \(M/D/1\) or \(D/D/1\) approximation matches DES within tolerance.

4. **Recast the mesh comparator as either (a) purely analytical bound or (b) a concrete simulated protocol.**  
   If kept as a bound, present a clean derivation of bytes required for global state replication and show it exceeds 1 kbps/node beyond some \(N\). If simulated, define state size per node, delta compression, convergence threshold, and show convergence/overhead tradeoffs.

5. **Replace Monte Carlo emphasis with sensitivity analysis over dominant uncertainties.**  
   Keep 1–3 replications for sanity, but add sweeps over: MAC efficiency \(\gamma\), header/ACK overhead, \(T_c\), message sizes, and coordinator service rates. Present results as bands; this will make the design guidance more credible for real systems.

If the above changes are made, the manuscript could become a strong, practically relevant engineering study suitable for T-AES.