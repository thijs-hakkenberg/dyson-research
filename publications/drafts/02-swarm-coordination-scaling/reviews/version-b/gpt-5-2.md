---
paper: "02-swarm-coordination-scaling"
version: "b"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-02-23"
recommendation: "Unknown"
---

## 1. Significance & Novelty — **Rating: 4/5 (Good)**

The manuscript tackles a genuinely important scalability question: what coordination architecture remains viable when moving from today’s mega-constellations (10³–10⁴) toward 10⁶-node “swarms.” For T-AES readership, this is significant because the field is rapidly approaching regimes where coordination/operations—not just launch or manufacturing—becomes the dominant system constraint. The paper’s explicit cross-architecture comparison (centralized vs hierarchical vs mesh) across three orders of magnitude, with a common simulation framework and common metrics, is a valuable contribution.

The novelty is strongest in (i) the attempt to quantify “break points” (e.g., ~10⁴ for centralized under a single-server assumption; ~10⁵ for mesh under global convergence assumptions; ~50k inflection under the chosen hierarchical parameters), and (ii) the parameter sweeps over cluster size and duty cycle with Monte Carlo uncertainty reporting. The “Shepherd/Flock” concept is not, by itself, a new idea in distributed systems (it resembles cellular/cluster-head paradigms), but packaging it as a design hypothesis linked to the DES findings is potentially useful.

That said, the paper sometimes overclaims “only viable topology at million-node scale” (Abstract; Conclusion) given the strong dependence on modeling assumptions—especially the mesh definition (global all-to-all trajectory awareness) and the centralized single-server baseline. The core contribution is still strong, but it should be framed as “under the stated requirements and parameterization” rather than as a near-universal architectural law.

---

## 2. Methodological Soundness — **Rating: 2/5 (Needs Improvement)**

Using DES with queueing models and Monte Carlo runs is an appropriate methodological direction for RQ1–RQ3. The manuscript also commendably lists many parameters (Table I) and reports confidence intervals via bootstrap. The explicit use of an \(M/D/1\) model for the centralized coordinator (Sec. III-B-1, Eq. (1)–(3)) is a reasonable first-order abstraction for processing bottlenecks, and the discussion of \(M/D/c\) acknowledges parallelization.

However, several key elements required for methodological robustness and reproducibility are currently underspecified or internally inconsistent:

* **Traffic model vs. bandwidth budget mismatch.** You state “Per-node bandwidth: 1 kbps” (Table I) while also setting a status reporting rate \(r=0.1\) msg/s with 256 B reports (Table I). That alone is \(0.1 \times 256 \times 8 = 204.8\) bps per node, before coordination messages (512 B), gossip exchanges, handoff chatter, collision alerts, headers, retransmissions, etc. Overhead percentages (e.g., 2–8%) are not interpretable without a clear definition of *total available bandwidth* and what constitutes “overhead” vs “operational data.” Right now, “overhead” seems to be computed relative to the 1 kbps coordination channel, but the text describes it as “fraction of total bandwidth” (Sec. III-D). Those are different denominators and lead to very different conclusions.

* **Hierarchy processing model is unclear.** Centralized processing is explicitly modeled as an \(M/D/1\) queue with capacity \(C\). For hierarchical, you provide message counts (Eq. (6)) and handoff transfer times, but you do not specify service disciplines/capacities at cluster and regional coordinators. Yet Table III reports latencies (ms) that must come from some processing/queueing model. Without explicit coordinator service rates, buffering, and scheduling policies at each level, the latency results (and the U-shaped cluster-size curve) are not reproducible and may be fragile.

* **Mesh “global convergence” assumption is too coarse to serve as a general mesh baseline.** The mesh is parameterized as disseminating a full \(N\)-node trajectory table to every node (Sec. III-B-3), yielding \(O(N^2)\). That is a legitimate *worst-case* information requirement, but it is not the only way to support collision avoidance or conjunction screening. In practice, collision risk is local in phase space and time horizon; one uses spatial indexing, covariance screening, and/or sectorization—concepts you later propose as “optimizations” for hierarchy but not allowed for mesh. This asymmetry biases the comparison: hierarchy is allowed to “aggregate” and “summarize,” while mesh is forced to replicate the full global table. If the goal is to compare architectural topologies fairly, you need a consistent task requirement (e.g., maintain safe separation with a given detection horizon and false-negative bound) and then implement the best-known feasible algorithm per topology under that requirement.

Overall, the DES approach is promising, but the paper needs a clearer, internally consistent definition of traffic loads, bandwidth constraints, service models, and fairness of baseline implementations for each topology.

---

## 3. Validity & Logic — **Rating: 3/5 (Adequate)**

The high-level qualitative conclusions are directionally plausible: centralized coordination tends to bottleneck on processing/decision throughput; flat all-to-all dissemination does not scale; hierarchical aggregation and locality generally help. The queueing argument for centralized saturation at \(N \approx C/r\) is logically consistent given the \(M/D/1\) assumption and the chosen \(C=1000\) msg/s, \(r=0.1\) msg/s (Sec. III-B-1). The duty-cycle trade discussion (Sec. IV-C; Table V) also has a coherent structure (handoff frequency vs failure exposure vs power variance).

Where validity becomes weaker is in the quantitative specificity of thresholds and overhead numbers. The “50,000-node inflection” (Sec. IV-D; Table VI) is explicitly acknowledged as parameter-dependent, which is good, but it is still presented prominently as a design guideline without enough mechanistic explanation of *why* superlinear effects appear despite a fixed-depth \(O(N)\) message count. The manuscript attributes it to “inter-regional coordination, global state reconciliation, and managing coordinator rotations” (Sec. IV-D) but does not show which event types dominate, nor does it provide decomposition plots vs. \(N\) to demonstrate the claimed causal drivers.

Similarly, the mesh conclusion “exceeds 25% bandwidth beyond 100,000 nodes” (Abstract; Sec. IV-A) depends entirely on the assumption that each node must receive all nodes’ trajectories. That is a strong requirement; if it truly is the requirement, it needs to be justified more rigorously (e.g., by specifying the collision avoidance model, decision horizon, orbital density, and acceptable risk). Without that, the reader cannot tell whether the result is a property of mesh topologies or a property of an overly globalized safety requirement.

Finally, several reported latency values (e.g., 85–150 ms in Table III at \(N=10^6\)) appear incompatible with the earlier statement that propagation delay is proportional to inter-node distance at light speed (Sec. III-A). Inter-satellite distances in LEO can be thousands of km, implying one-way propagation on the order of milliseconds to tens of milliseconds; but end-to-end coordination latency across multiple hierarchy levels plus queueing could plausibly be >100 ms. The issue is that the paper does not provide enough detail (distances, topology geometry, path lengths, per-hop processing) to validate that these latencies emerge naturally rather than being artifacts of a simplified model.

---

## 4. Clarity & Structure — **Rating: 4/5 (Good)**

The manuscript is generally well organized: clear RQs, clear topology definitions, a parameter table, and results organized around the RQs (topology comparison, cluster size, duty cycle, threshold/optimizations). The abstract is informative and largely consistent with the body, and the limitations section is unusually explicit for an engineering DES paper (a strength).

Figures and tables are conceptually well chosen (architecture diagram; overhead vs \(N\); latency distributions; failure resilience; Pareto plot). The narrative is readable for a mixed audience spanning distributed systems and space operations. The paper also does a good job of distinguishing qualitative from quantitative claims in a few places (e.g., centralized \(M/D/1\) as a worst-case bound; Sec. VI Limitations).

Areas that need improvement for clarity are mostly about definitions and denominators: “communication overhead” is used throughout, but the baseline bandwidth and what counts as overhead vs mission traffic is not consistently defined (Sec. III-D vs Table I vs Fig. 2 caption). Also, several claims would benefit from explicit “model-to-metric mapping” text: e.g., how exactly is “coordination success rate” defined (deadline length? per-cycle? per-message?), and what deadlines are used for routine coordination vs collision avoidance?

The AI-assisted section is clearly labeled as ideation and includes thoughtful caveats. However, in an IEEE T-AES manuscript, Section V currently occupies a large fraction of narrative attention relative to its evidentiary weight; it may distract from the DES contribution unless tightened or reframed.

---

## 5. Ethical Compliance — **Rating: 4/5 (Good)**

The paper provides unusually thorough disclosure regarding AI assistance (Sec. V; Acknowledgment), including model names, the nature of the protocol, and limitations such as priming and shared training corpora. This is aligned with emerging transparency expectations and is better than many current submissions.

Potential ethical/compliance issues remain: authorship is listed as “Project Dyson Research Team” with a note that names will be provided later. IEEE authorship policies generally require identifiable authors at submission/review stages; anonymity is not typical for T-AES peer review (unless the journal uses double-blind with separate metadata, which is not indicated here). At minimum, the submission should clarify corresponding author responsibility, accountability for data/code, and conflict-of-interest statements.

Also, the “Data Availability” statement points to a general website/repository but does not provide a specific immutable artifact (commit hash, DOI, Zenodo archive). For reproducibility ethics, the paper should pin the exact version used to generate figures/tables.

---

## 6. Scope & Referencing — **Rating: 3/5 (Adequate)**

The topic fits IEEE Transactions on Aerospace and Electronic Systems in spirit—architecture and scalability of autonomous space systems, communications/coordination, and operations modeling. The DES/queueing framing is also in-scope for T-AES readers interested in system-level performance analysis.

Referencing is a mix of strong foundational citations (Lamport, Lynch, Kleinrock, Demers) and less satisfactory operational citations (e.g., Starlink ops via a marketing webpage). For claims about Starlink operational practices, conjunction handling, and scale numbers, you should cite regulatory filings, technical conference papers, or peer-reviewed/archival sources (FCC filings, SpaceX technical presentations, ESA/USSF conjunction analysis papers, etc.) rather than corporate web pages. Similarly, the “7,000 active satellites mid-2024” and “12,000 approved” figures should cite an authoritative database or filing.

The related work could be strengthened by including: (i) constellation operations/autonomy literature (e.g., autonomy frameworks, onboard planning, distributed space mission ops), (ii) DTN/space networking considerations (delay/disruption tolerant networking, contact plans), and (iii) conjunction assessment/collision avoidance scaling literature (screening algorithms, spatial indexing, covariance-based filtering). These are directly relevant to the mesh vs hierarchy framing and would help justify the “global convergence” requirement or replace it with a more defensible safety requirement.

---

## Major Issues

1. **Define “communication overhead” rigorously and fix denominator inconsistencies.**  
   Throughout Sec. III-D and Sec. IV (Table II; Fig. 2; Table III; Table VI), overhead percentages are central to the conclusions, but the paper does not unambiguously define:
   * the total available bandwidth per node and/or per link,
   * whether 1 kbps is a dedicated coordination channel or total comms budget,
   * what “operational data” load is assumed (if any),
   * whether protocol overhead (headers, retransmissions) is included.  
   Without this, claims like “mesh exceeds 25% of available bandwidth beyond 100,000 nodes” are not scientifically checkable.

2. **Specify the service/queueing model for hierarchical coordinators (cluster/regional/ground).**  
   Centralized has \(M/D/1\) with \(C\). Hierarchical provides message counts but not processing capacities, queue disciplines, or buffering at each level, yet reports latencies (Table III) and tail behavior (Fig. 3). Provide explicit per-level service rates (messages/s), whether coordinators are single-threaded, and how aggregation affects service time.

3. **Mesh baseline is not a fair or sufficiently justified representation of “mesh coordination.”**  
   Sec. III-B-3 assumes every node must receive every node’s trajectory table (global all-to-all replication). If that is the requirement, justify it with a collision avoidance model and risk requirement. If it is not, then implement collision avoidance using locality-aware dissemination (sectorization, spatial hashing, time horizon filtering) and compare mesh under that more realistic requirement. As written, hierarchy is credited for aggregation/locality while mesh is denied analogous locality mechanisms, biasing RQ1.

4. **Centralized baseline is framed as “worst-case,” but results are presented as architectural limits.**  
   You acknowledge \(M/D/c\) (Sec. III-B-1), yet Table II labels “scalability limit ~10,000” without clearly tying it to \(c=1\). Provide sensitivity analysis over \(c\) (e.g., \(c\in\{1,10,100\}\)) or report limits as a function of \(c\) to avoid misleading readers.

5. **Reproducibility gaps: code/version pinning and missing model details.**  
   “Project Dyson open-source repository” is not sufficient without a permanent link/version. Also missing are: orbital geometry assumptions (altitude, shell thickness, inter-node distance distribution), link error/loss model, and deadlines for “coordination success rate.”

---

## Minor Issues

- **Eq. (6) hierarchical message count appears incomplete / unclear.**  
  \(M_{\text{total}} = N + N/k_c + N/(k_c k_r)\) counts upward reporting, but does it include downward commands (ground→regional→cluster→node), acknowledgments, coordinator election traffic, and collision alerts? Clarify what is included in “per coordination cycle.”

- **Inconsistency in hierarchy complexity discussion.**  
  Sec. III-B-2 states fixed-depth hierarchy yields \(O(N)\) and that adaptive depth yields \(O(N\log N)\). That’s true for message *count* under certain assumptions, but depth increase can reduce fanout and may reduce constants or congestion; the argument reads one-sided. Consider rephrasing to avoid implying fixed depth is always superior.

- **Failure model vs “single point” language.**  
  Table II lists centralized failure mode “Single point.” But the centralized model is a single coordinator; real systems have redundancy. Either state explicitly “single coordinator instance” or include redundant coordinator modeling.

- **Duty-cycle “handoff success” model is not defined.**  
  Table V reports handoff success rates (95% to 99.9%) but the reliability model for handoff is not described (is it link outage probability? bit error? coordinator failure during transfer?). Add a subsection defining handoff failure probability components.

- **Use more archival citations for Starlink/Kuiper/OneWeb operational claims.**  
  Replace or supplement web URLs with filings, conference proceedings, or journal papers where possible.

- **Authorship placeholder may conflict with IEEE policy.**  
  The note “individual author names will be provided for final publication” should be resolved before final acceptance; consider adding a corresponding author now.

---

## Overall Recommendation — **Major Revision**

The paper addresses an important problem and has a promising DES-based comparative approach, but the central quantitative results (overhead %, scaling limits, and the mesh/hierarchy conclusions) are not yet methodologically defensible due to unclear metric definitions, incomplete service/queueing specification for the hierarchical case, and an arguably biased mesh baseline. With clearer definitions, fairer baselines, and added sensitivity analyses, this could become a strong T-AES contribution; in its current form, it requires substantial revision.

---

## Constructive Suggestions

1. **Tighten metric definitions and add a “traffic accounting” table.**  
   Add a subsection that defines *exactly* how “communication overhead” is computed (numerator/denominator), what bandwidth is provisioned (per node, per link type), and what background/mission traffic is assumed. Provide a per-node average bps breakdown by message type for each topology at a few \(N\) values.

2. **Make the hierarchical processing model explicit and symmetric with centralized.**  
   Specify \(C_{\text{cluster}}, C_{\text{regional}}, C_{\text{ground}}\) (messages/s), queue types (e.g., \(M/D/1\) each level), aggregation service times, and buffer sizes. Then show which level saturates first as \(N\) grows and how that relates to the “50k inflection.”

3. **Reformulate the mesh comparison around a collision-avoidance requirement rather than “global table replication.”**  
   Define a safety requirement (time horizon, miss distance, probability-of-collision threshold). Implement (a) a naive global dissemination mesh (your current model) and (b) a locality-aware mesh (sectorized dissemination / spatial index / publish-subscribe by region). This will let you claim something stronger and fairer: e.g., “flat mesh without hierarchy requires strong locality mechanisms; once you add locality, it becomes implicitly hierarchical.”

4. **Add sensitivity analyses for the most consequential parameters.**  
   At minimum: reporting rate \(r\), per-node bandwidth (1 kbps is very low for optical ISLs but plausible for a narrow control channel), coordinator capacity \(C\), and centralized parallelism \(c\). Present scaling limits as surfaces/contours, not single points.

5. **Pin reproducibility artifacts and add missing scenario geometry.**  
   Provide a DOI or commit hash for the simulator and datasets, plus a concise description of the orbital shell model (altitude, distribution, distance statistics) and link assumptions (loss, latency model). This will materially improve credibility and make the work reusable by the community.