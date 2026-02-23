---
paper: "02-swarm-coordination-scaling"
version: "g"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-02-23"
recommendation: "Major Revision"
---

## 1. Significance & Novelty — **Rating: 4/5**

The manuscript tackles a genuinely important question for future mega-constellation and swarm-scale autonomy: how coordination architectures scale from \(10^3\) to \(10^6\) nodes, and where/why scaling “knees” appear. The paper’s strongest novelty claim is not that hierarchy scales better than mesh (well-known), but that it *quantifies* overhead/latency/availability across three orders of magnitude using a DES framework, and attempts to localize a regime change (\(N^\*\approx 45{,}000\)) via intermediate-scale sweeps and model comparison. That kind of “engineering scaling characterization” is valuable for T-AES readers because it translates asymptotic arguments into parameterized, operationally interpretable curves.

The deliberate use of two “bounds” (centralized ground as a conservative processing bottleneck; global-state mesh as an upper bound on decentralized global-awareness overhead) is a defensible framing and helps structure the design space. The explicit separation of topology-invariant baseline telemetry (20.5%) from topology-dependent protocol overhead is also a helpful contribution for clarity.

That said, the novelty is partially constrained by how idealized the communication model is (notably the “1 kbps per node” abstraction combined with a coordinator pooling assumption) and by the fact that the most important “fix” for the superlinear regime is handled via analytical projection rather than fully simulated implementation (two of three optimizations). The paper is still significant, but the strongest claims should be positioned more as *scaling insights under a specified abstraction* than as near-operational predictions.

---

## 2. Methodological Soundness — **Rating: 3/5**

A DES with Monte Carlo replication is an appropriate tool for this study, and the manuscript does several things right for reproducibility: it enumerates parameters (Table I), defines traffic accounting (Table IV), states the Monte Carlo run counts and CI method (bootstrap BCa), and mentions validation checks against \(M/D/1\) and gossip bounds. The explicit metric definitions (Section III-H) are also a strength—particularly the distinction between baseline telemetry and protocol overhead \(\eta\).

However, several modeling choices materially affect the results and need tighter specification or rework:

* **Bandwidth model inconsistency / pooling assumption:** The paper assigns “1 kbps per node” but then allows coordinators to effectively use \(k_c\times 1\) kbps by pooling cluster bandwidth (“coordinators operate on a separate, higher-capacity link budget”). This is a major architectural assumption that changes feasibility and scaling. It is plausible in some systems (e.g., coordinator has higher-rate ISL or scheduled access to aggregate spectrum), but it is not topology-neutral and should be explicitly parameterized and stress-tested. As written, the normalization “against total fleet bandwidth” can mask that coordinator links are the true bottleneck.

* **Timebase inconsistency in coordination cycle definition:** Section III-H defines coordination cycle period \(T_c=1/r=10\) s at \(r=0.1\) msg/s, but earlier the DES states routine events use one-minute resolution and repeatedly refers to “per reporting cycle (1 minute)” traffic. This ambiguity affects success criteria (“within \(T_c\)”) and latency interpretation. The DES can be valid with mixed resolutions, but the coordination cycle definition must be consistent.

* **Queueing/processing model mapping:** The hierarchical coordinator service rates (\(C_{\text{cluster}}=200\) msg/s, etc.) appear chosen to avoid saturation; the U-shape is then attributed to topology effects. That’s fine, but then the paper should show that results are not an artifact of these service rates (sensitivity study), and clarify what “msg” means when message sizes differ (256B reports vs 512B commands vs 10–50MB handoff). Treating all as equal “messages” for service time can bias latency and success outcomes.

* **Link loss model:** The Bernoulli per-message loss model (Section IV-F) is a useful first step, but it omits retransmission, coding, contact windows, and correlated fades/occlusion. Since a key conclusion is “hierarchical is disproportionately sensitive below \(p_{\text{link}}=0.6\),” the absence of even simple retransmission/ARQ within-cycle is a methodological limitation (and may overstate failure rates for hierarchy relative to mesh).

Overall: the framework is promising and mostly well described, but key assumptions (bandwidth pooling, cycle period, service model) need correction/clarification and some sensitivity analyses to be methodologically convincing for T-AES.

---

## 3. Validity & Logic — **Rating: 3/5**

Most qualitative conclusions follow logically from the constructed models: centralized \(M/D/1\) saturates near \(N=10^4\) for the chosen \(C\) and \(r\); global-state dissemination with full per-node state is information-theoretically \(O(N^2)\); fixed-depth hierarchy is \(O(N)\) in message count. The per-tier decomposition (Fig. 8) is a good practice and strengthens the argument that the “knee” is driven by inter-cluster/regional traffic rather than ground processing.

Where validity is weaker is in the *quantitative* interpretation and in a few internal logical tensions:

* **“Superlinear” in an \(O(N)\) design:** The manuscript claims a superlinear transition for a fixed-depth hierarchy whose analytical message count is \(M_{\text{total}} = N + N/k_c + N/(k_ck_r)\) (Eq. 6), i.e., strictly linear in \(N\) for fixed \(k_c,k_r\). A superlinear *measured* overhead can still occur due to second-order mechanisms (e.g., retries, handoffs, collision alerts scaling with density, coordinator election chatter, buffer drops), but then those mechanisms must be explicitly defined and shown to scale superlinearly. Currently the text attributes it to “inter-cluster coordination traffic” and later to “quadratic growth of inter-regional reconciliation traffic,” but the hierarchical model description does not clearly define a reconciliation mechanism with quadratic dependence. This is a major logic gap: either the protocol includes an \(O(\#\text{clusters}^2)\) component (e.g., pairwise coordinator coordination, regional broadcast, etc.) that must be specified, or the “superlinear” claim needs reframing (e.g., superlinear in *bandwidth utilization* due to fixed per-node capacity and coordinator pooling constraints, or due to collision-alert rate scaling with \(N\)).

* **Collision avoidance event scaling:** The collision alert process is modeled as Poisson with rate \(10^{-4}\)/node/s (constant per node). In real orbital environments, conjunction screening load tends to increase faster than linearly with object count (roughly with spatial density and pair counts, though screening volumes and filtering complicate this). If your model keeps it linear, that cannot explain a knee. If you intend density-driven scaling, you should model the event rate as a function of \(N\) (or shell occupancy), and then the “superlinear regime” may be physically grounded.

* **Projected optimizations:** The dashed “optimized” curve is a combination of (i) one DES-validated mechanism (exception telemetry) and (ii) two unvalidated projections (dynamic partitioning, heterogeneous hardware). The paper is generally candid about this, but several statements in abstract/conclusion read as stronger than warranted (“reduce to 4–5% at \(10^6\) nodes”). For T-AES, projections are acceptable if clearly marked and derived, but you should provide the actual multiplicative factors, how they were calibrated to Fig. 8 decomposition, and uncertainty bounds.

Net: the paper’s *directional* conclusions are credible, but the “knee/superlinear” mechanism needs sharper definition and/or revised claims to ensure the conclusions are supported by the modeled protocol.

---

## 4. Clarity & Structure — **Rating: 4/5**

The manuscript is generally well organized: problem → baselines → DES framework → metrics → results → discussion/limitations. The “Baseline Interpretation Note” early in the paper is a good move and reduces reviewer confusion about strawman comparisons. Traffic accounting (Table IV) and explicit metric definitions (Section III-H) are unusually clear for a simulation paper and should be retained.

The abstract is information-dense and mostly accurate, but it is arguably overpacked with numbers and subordinate claims (AIC, breakpoint CI, duty cycle, link-loss sensitivity, exception telemetry validation). For T-AES readability, consider trimming the abstract to the 3–4 most important quantitative findings and moving the rest to the introduction or results summary.

A few clarity issues materially affect comprehension:

* **Coordination cycle period inconsistency (10 s vs 60 s)** appears in multiple places and will confuse readers evaluating latency/success.
* **Definition of “protocol overhead” vs. “coordination load”** is good, but the coordinator bandwidth pooling assumption should be highlighted earlier and more explicitly because it changes interpretation of \(\eta\).
* **Figures are referenced but not shown in the LaTeX**; assuming they exist, ensure they directly support the “knee” claim (e.g., include residuals for model fits, show decomposition vs \(N\), show confidence bands clearly).

---

## 5. Ethical Compliance — **Rating: 4/5**

The manuscript includes an explicit disclosure of AI-assisted ideation in the Acknowledgment, and it clearly states that the “Shepherd/Flock” concept is not validated in this study. That is appropriate and transparent. No human subjects or sensitive datasets appear involved.

Two improvements would strengthen compliance with evolving IEEE expectations:

1. Add a brief statement clarifying that AI tools were not used to generate results/data/code (if true), only ideation; and
2. Replace “commit hash [PENDING]” with an archival artifact upon publication (Zenodo DOI or similar). For review, “pending” is fine, but T-AES typically expects a stable link for reproducibility claims.

No obvious conflict-of-interest statement is present; if “Project Dyson” has a stake in the architecture, consider adding a short COI disclosure.

---

## 6. Scope & Referencing — **Rating: 3/5**

Topically, the paper fits T-AES: distributed coordination, autonomy at scale, link/latency constraints, reliability, and constellation operations. The queueing and DES angle is also within scope.

Referencing is broad and generally current, spanning constellation operations, DTN/CCSDS, distributed systems, and swarm robotics. However, several citations are non-archival (SpaceX/Amazon/DARPA web pages, internal Project Dyson publication). That is sometimes unavoidable for ops facts, but key technical claims should lean more on archival sources. In particular, the paper would benefit from citing:

* mega-constellation autonomy/operations studies beyond marketing pages (e.g., academic/IAA/IAC papers on Starlink operations, collision avoidance workflows, or ISL constraints),
* more recent work on large-scale distributed control/estimation with hierarchical aggregation,
* work on contact graph routing / DTN performance for intermittent links (since link intermittency is central to your sensitivity study).

Also, the “global-state mesh” is framed as an upper bound; it would help to cite representative scalable decentralized approaches (sectorized/locality gossip, hierarchical gossip, federated filtering) to better contextualize the bound and avoid the appearance of a strawman—even if you do not simulate them.

---

## Major Issues

1. **Coordination cycle definition inconsistency (10 s vs 60 s) affects success/latency/overhead.**  
   *Where:* Section III-A (one-minute resolution for routine events), Section III-G (per cycle = 1 minute), Section III-H (“\(T_c=1/r=10\) s”).  
   *Why it matters:* Coordination success is defined relative to \(T_c\); overhead per cycle and handoff/failure detection timing depend on cycle length.  
   *Fix:* Choose a single coordination round period (e.g., 60 s) and adjust \(r\) accordingly, or keep \(r=0.1\) msg/s and define \(T_c\) separately from \(1/r\). Then recompute success metrics and any per-cycle traffic calculations.

2. **“Superlinear scaling transition” mechanism is under-specified and appears inconsistent with Eq. (6).**  
   *Where:* Section IV-D (“superlinear regime… inter-regional dominated”), model comparison subsection, and Fig. 8 discussion (“quadratic growth of inter-regional reconciliation traffic”).  
   *Why it matters:* A core contribution is identifying \(N^\*\) and explaining a knee; but the described hierarchical message model is linear in \(N\) for fixed parameters.  
   *Fix:* Explicitly define the additional inter-cluster/regional protocol component that grows faster than \(N\) (e.g., pairwise coordinator coordination, regional consensus, reconciliation floods, etc.), include it in traffic accounting, and show its measured scaling vs \(N\). If no such mechanism exists, revise the claim: it may be a *change in slope* within linear scaling due to fixed per-tier constants, or an artifact of other modeled processes.

3. **Coordinator bandwidth pooling assumption needs to be parameterized and stress-tested.**  
   *Where:* Section III-G (“coordinators use combined coordination bandwidth of its cluster”).  
   *Why it matters:* This assumption can be the difference between feasibility and infeasibility; it effectively introduces a privileged channel for coordinators.  
   *Fix:* Add a parameter \(C_{\text{coord-link}}\) (kbps) and evaluate overhead/latency when coordinators are limited to (i) 1 kbps, (ii) \(\beta k_c\) kbps with \(\beta\in[0.1,1]\), and (iii) a realistic ISL schedule share. Report when coordinator ingress becomes the bottleneck.

4. **Service model conflates “message” types with widely varying sizes.**  
   *Where:* Hierarchical queueing description (Section III-B-2), handoff transfers (10–50 MB), buffer size in “messages”.  
   *Why it matters:* Latency and drop probability depend on bytes and serialization time; treating 50 MB as “one message” with the same service model as 256 B can distort tail latency and coordination success.  
   *Fix:* Use byte-based service (bits/s) or at least size-dependent service times; separate control-plane message processing from bulk transfer serialization.

5. **Link-loss sensitivity conclusions may be overstated without retransmission/contact modeling.**  
   *Where:* Section IV-F.  
   *Why it matters:* “No retransmission within the cycle” penalizes hierarchy more than protocols that would naturally add redundancy/ARQ for aggregated summaries.  
   *Fix:* Add a simple reliability mechanism (e.g., 1–2 retransmission attempts within \(T_c\), or forward error correction overhead) and show whether the \(p_{\text{link}}=0.6\) “cliff” persists.

---

## Minor Issues

1. **Table VIII vs earlier overhead numbers:** Table VI says fixed \(k_c=100\) yields 12.8% at \(10^6\); abstract says 10.0% at \(5\times10^5\) and 10.0% at \(5\times10^5\) matches Table VI, but abstract also states “10.0% at \(5\times10^5\)” excluding baseline. Ensure all places consistently specify fixed vs optimized cluster sizing and whether baseline is excluded.

2. **Eq. (6) description “uplink reporting only” but later overhead includes many downlink/control messages.** Consider adding a parallel expression for total bidirectional message volume used in DES, or explicitly state Eq. (6) is illustrative only.

3. **Global-state mesh fanout argument is confusing:** The claim “fanout \(f=O(N/\log N)\) follows…” is not standardly presented and may read as forced to achieve \(O(N^2)\). Since you later argue information-theoretic \(O(N^2)\) regardless, simplify: state that total information delivered is \(\Theta(N^2)\) entries and therefore bytes must scale \(\Omega(N^2)\), independent of gossip details.

4. **System availability definition differs across topologies** (Section III-H). For centralized, availability is coordinator uptime; for mesh, “reach at least \(f\) gossip partners.” These are not comparable notions. Consider reporting two metrics: (i) fraction of nodes receiving required coordination outputs; (ii) fraction of time coordination service meets deadline.

5. **Non-archival citations:** Several key operational claims rely on non-archival sources (Starlink ops, Kuiper overview, DARPA pages). Where possible, replace or supplement with archival/technical reports.

6. **Reproducibility:** “commit hash [PENDING]” should be replaced before publication; also specify Python version and key libraries (sim framework, RNG, bootstrap implementation).

---

## Overall Recommendation — **Major Revision**

The paper has a strong motivating problem, a generally well-structured DES framework, and potentially valuable scaling insights for hierarchical coordination. However, several core claims—especially the “superlinear knee” mechanism and the quantitative overhead/availability results—are currently undermined by internal inconsistencies (coordination cycle timing), under-specified protocol components (what exactly grows superlinearly), and a major bandwidth pooling assumption that is not parameterized. Addressing these issues will likely require re-analysis and at least some re-simulation, hence a Major Revision.

---

## Constructive Suggestions

1. **Resolve the coordination-cycle/timebase and re-derive success/overhead accordingly.**  
   Define a single “coordination round” period (e.g., 60 s) and ensure \(r\), \(T_c\), event scheduling resolution, and success deadlines are consistent. Then update Tables VI–VIII and any text that interprets “per cycle” quantities.

2. **Make the hierarchical protocol explicit enough to justify the knee.**  
   Add a short pseudo-protocol (message types per round per tier, including any reconciliation/consensus among coordinators/regionals). Then show measured scaling of each component vs \(N\). If the knee is actually driven by collision-alert traffic or handoffs, demonstrate that with plots (component bytes vs \(N\)).

3. **Parameterize coordinator link capacity instead of assuming perfect pooling.**  
   Introduce a coordinator ingress/egress capacity model (kbps or scheduled slots) and run a sensitivity sweep. Report the minimum coordinator link rate required to sustain \(k_c=100\) at \(r=0.1\) msg/s without drops, and how that changes the optimal \(k_c\).

4. **Switch to byte-based service/queueing (or at least size-dependent service times).**  
   This will improve credibility of latency distributions (Fig. 3) and handoff success modeling. It will also let you incorporate MAC/serialization overhead in a principled way.

5. **Strengthen the “optimized projection” with transparent factors and uncertainty.**  
   Provide the exact reduction factors used for exception telemetry, dynamic partitioning, and heterogeneous hardware; explain how they map onto Fig. 8 decomposition; and add uncertainty bands (even if heuristic). This will make the projection defensible even before full DES implementation of the latter two optimizations.