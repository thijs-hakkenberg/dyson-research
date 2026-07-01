---
paper: "02-swarm-coordination-scaling"
version: "bl"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-02-27"
recommendation: "Unknown"
---

## 1. Significance & Novelty — **Rating: 4/5 (Good)**

The manuscript targets a real and timely problem: coordination scalability for very large autonomous spacecraft swarms (10³–10⁵+), with a focus on *sizing equations* rather than only algorithm proposals. The paper’s core novelty is the explicit separation of feasibility into three “layers” (byte budget/utilization \(\eta\), MAC efficiency \(\gamma\), and TDMA airtime schedulability) and the attempt to provide closed-form relationships that practitioners can use early in architecture trades. That emphasis is well aligned with T-AES readership, which values design-relevant modeling and system-level implications.

The strongest contribution is the disciplined byte accounting and the identification that topology-dependent overhead (\(\eta_0\)) is relatively small compared to workload-driven command traffic (\(\eta_{\text{cmd}}\)) *under the authors’ semantics* (centralized command generation; broadcast vs unicast distinction). The explicit schedulability distinction between Type-1 broadcast commands and Type-2 per-node unicast (Eq. (23) / \(\lceil 22\rceil\) cycles) is practically important and not commonly spelled out in swarm/constellation coordination papers.

That said, some novelty claims are overstated because the “verification” largely checks consistency between equations and a DES at the *same abstraction level* (message-layer). This is still useful, but it is not validation against physical/MAC effects, and several headline numbers in the abstract (e.g., “At \(\ge 10\) kbps, all constraints are non-binding”) depend strongly on assumptions about scheduled access, half-duplex partitioning, and what is included/excluded from \(\eta\). With tighter positioning (design equations as *upper-layer* sizing tools), the contribution remains strong.

---

## 2. Methodological Soundness — **Rating: 3/5 (Adequate)**

The modeling approach—cycle-aggregated DES plus closed-form traffic/schedulability equations—is appropriate for RQ1–RQ3 *if the goal is message-layer sizing*. The manuscript is commendably explicit about what is and is not modeled (e.g., Section III-A; “fluid-server ingress” vs analytical TDMA feasibility; Section V-A validation gap). Parameter tables are detailed (Table II), and the code/data availability statement is a major strength for reproducibility.

However, several methodological choices create internal tension that should be resolved more rigorously:

* **Mixing “byte budget” and “airtime feasibility”**: \(\eta\) counts information content per node per cycle, while TDMA feasibility depends on airtime consumed by *transmissions*, not per-node “received bytes.” This is acknowledged (Section IV-A, “Schedulability vs byte budget”), but the paper still uses \(\eta\) as a primary feasibility metric even in scenarios where airtime is the binding constraint (half-duplex coordinator, high ingress fraction). A reader can easily misinterpret \(\eta\approx 46\%\) as “feasible,” while airtime is actually near-saturated (Table V superframe margin only 623 ms at 24 kbps, and effectively negative under retransmissions).

* **Coordinator ingress modeling**: the DES uses a fluid server with drop-tail (Section III-A), but the sizing arguments rely on arrival phase distributions and TDMA slotting. The “Model A/B/TDMA converge to 20–50 kbps” argument is plausible, yet it needs clearer derivations and consistent assumptions (random-phase arrivals vs deterministic slotting are fundamentally different regimes). In particular, Model A’s “minimum spacing quantile” argument is under-specified (what is \(\Delta t_{(1)}^*\) exactly for \(k_c-1\) uniform points?).

* **Loss/retransmission modeling**: the GE model assumes state constant within a cycle, which makes intra-cycle retransmission ineffective “by construction” (Section IV-C). This is acceptable as a bounding case, but then the paper should more explicitly treat \(M_r>0\) as irrelevant in the RF-backup TDMA regime (which you partly do in Section IV-A and Table XIII notes). As written, the paper sometimes presents retransmission improvements (Table XIII) without sufficient emphasis that they are infeasible in the key 1 kbps/24 kbps half-duplex superframe regime.

Statistically, 30 replications with bootstrap CIs is fine for mean overhead and for stable tail estimates given the huge sample sizes, but the paper should clarify independence assumptions in tail sampling (AoI sampled every 100 s; per-run P99 then averaged). That method is reasonable, yet it is not equivalent to a fleet-wide P99 across all time and all nodes; you should state which one you intend.

---

## 3. Validity & Logic — **Rating: 3/5 (Adequate)**

Most conclusions are directionally supported by the analysis: hierarchical aggregation yields \(O(1)\) per-node overhead; global-state mesh explodes; coordinator ingress is the bottleneck; command addressing (broadcast vs unicast) dominates schedulability. The analytic cross-checks are a strength: AoI P99 under geometric inter-arrivals (Eq. (26)) matches DES closely; GE recovery curves are compared to Markov predictions (Section IV-C).

The main concern is that some headline claims are stronger than the evidence supports under the stated abstraction boundary:

* **“At \(\ge 10\) kbps, all constraints are non-binding.”** This is only true if (i) scheduled access with high \(\gamma\) is available, (ii) half-duplex partitioning is not binding, (iii) antenna pointing/visibility is ignored, and (iv) control-plane overhead does not grow with rate. Your own text acknowledges that unmodeled constraints may become binding (Introduction and Section V-A), but the abstract and Table I phrasing reads too categorical for T-AES.

* **AoI interpretation vs operational relevance**: You map AoI P99 = 440 s to along-track uncertainty using a linear growth rate \(\dot{\sigma}=0.5\) m/s (Section IV-B). This is plausible but not justified; orbit prediction error growth is not generally linear and depends on force model, ballistic coefficient uncertainty, maneuver execution error, and measurement cadence. Without a cited covariance propagation model (or at least a more defensible bound), the “within conjunction screening tolerances” claim is suggestive but not rigorous.

* **Availability modeling**: The paper quotes “99.5%” hierarchical availability (Tables XI, XIV; Fig. 12) but also states per-coordinator \(A>99.99\%\) under a two-state Markov with MTTF 50 yr and MTTR 35 s (Section IV-H). The relationship between these numbers is unclear. If the 99.5% includes cascading/system effects, those effects should be explicitly modeled or bounded, otherwise it reads ad hoc.

Overall the logic is coherent, but several key metrics (availability, “non-binding,” conjunction tolerance) need either stronger derivations or more conservative framing.

---

## 4. Clarity & Structure — **Rating: 4/5 (Good)**

The manuscript is generally well organized: clear RQs, explicit contributions, strong parameter table, and a results roadmap that helps navigation. The separation between analytical equations and DES verification is explicitly stated, and the repeated reminders about the message-layer abstraction are helpful.

Figures/tables are mostly effective (notably Table V superframe budget; Table VI AoI; Table XIII link availability notes). The “functional capability matrix” (Table XII) is a good addition because it prevents unfair overhead comparisons across architectures with different service scope.

Clarity issues mostly arise from overloaded terminology and occasional inconsistencies:

* The term “per-node bandwidth allocation 1 kbps” is sometimes a budget and sometimes implicitly treated as a link rate; you do address this (Section III-F), but the paper still requires careful rereading to track “budget vs PHY.”
* The definition of \(\eta\) vs \(\eta_{\text{total}}\) is clear in principle, but the narrative sometimes mixes “baseline telemetry excluded” with plots/tables that appear to include commands/heartbeats in AoI experiments (Table VI footnote). Consider a single “what is included in each metric” box early in Results.
* A few equations and claims would benefit from more explicit variable definitions at first use (e.g., Eq. (23) uses \(\alpha_{\text{RX}}\) introduced later; Eq. (24–25) use \(\bar{M}_r\) without a clear operational definition).

A non-specialist reader in aerospace systems could follow the argument, but a networking/MAC reader may find the abstraction boundary and feasibility claims insufficiently crisp.

---

## 5. Ethical Compliance — **Rating: 4/5 (Good)**

The manuscript includes an explicit disclosure about AI-assisted ideation (Acknowledgment) and cites an internal methodology document. This is better than typical and aligns with emerging transparency expectations. There is no apparent human-subjects or dual-use ethical issue beyond standard considerations for autonomous space operations.

Two improvements are needed for IEEE-style compliance and clarity:

* The acknowledgment mentions specific proprietary model versions (“Claude 4.6, Gemini 3 Pro, GPT-5.2”). This is transparent, but it may raise reproducibility questions; consider stating *what* was AI-assisted (ideation only, not analysis/code) more explicitly and confirming that all results were generated by the authors’ toolchain.
* Conflicts of interest are not discussed. The “Project Dyson Research Team” and project website suggest an organizational entity; T-AES typically expects affiliations and potential COI statements. You note authors/affiliations will be provided later, but the manuscript should still include a standard disclosure if there are commercial ties.

---

## 6. Scope & Referencing — **Rating: 4/5 (Good)**

The topic fits IEEE Transactions on Aerospace and Electronic Systems well: it addresses spacecraft operations, autonomy architectures, and communications constraints with quantitative sizing. The paper also connects to mega-constellation operations and conjunction management, which is relevant and timely.

Referencing is broad and mostly appropriate: constellation networking (Handley, del Portillo), DTN (Cerf/BPv7), distributed algorithms (Lynch, Raft), AoI literature, and swarm robotics surveys. The CCSDS references are helpful for grounding packet/PHY assumptions.

Gaps/concerns:

* Several “non-archival” references (Starlink filings, Kuiper overview, DARPA pages) are acceptable as context but should not carry technical weight. Ensure that key quantitative claims do not depend on them.
* The paper would benefit from citing work on *TDMA scheduling and half-duplex constraints* in satellite proximity networks and/or inter-satellite crosslink MACs (beyond CCSDS Proximity-1). Right now, \(\gamma\) and superframe structure are plausible but lightly supported.
* For conjunction/AoI coupling, consider citing operational SSA/covariance propagation or screening cadence literature beyond Flohrer/Krag/Lemmens and Vallado, to support the “tolerance” argument.

---

## Major Issues

1. **Feasibility metrics are not consistently defined across regimes (byte budget vs airtime).**  
   The paper’s central “three-layer feasibility” idea is good, but the manuscript still presents \(\eta\) as a primary feasibility indicator in regimes where half-duplex TDMA airtime is the actual constraint (Table V shows near-saturation). You should restructure Results to explicitly gate conclusions: first byte budget (\(\eta\)), then MAC efficiency (\(\gamma\)), then airtime schedulability—*for each workload and command addressing mode*. Right now, readers can misinterpret stress-case “feasible” under \(\eta\) while airtime makes unicast infeasible and retransmissions infeasible.

2. **Coordinator ingress sizing derivations need tighter mathematical specification.**  
   Section IV-A’s Model A/B/TDMA comparison is compelling but under-specified. In particular, Model A’s quantile of minimum spacing for uniform random arrivals needs a clear formula/derivation (order statistics of spacings on \([0,T_c)\)), and Model B needs a clear statement of buffer dynamics (token bucket parameters, service discipline). Without this, the “20–50 kbps convergence” reads heuristic.

3. **Availability and duty-cycle claims are not supported by a consistent reliability model.**  
   The manuscript reports “99.5%” hierarchical availability and discusses coordinator failure transients, RF-backup election times, and triple-fault probabilities (Section III-B, coordinator failure transient; Section IV-H). These are useful, but the mapping from component rates (2%/yr node failure, optical outage 1%, GE bad-state probability) to system availability curves (Fig. 12) is not clearly derived. This needs either (i) a formal Markov/renewal model with stated assumptions, or (ii) reframing as illustrative estimates rather than quantitative results.

4. **AoI-to-conjunction relevance is overstated without an orbit error growth model.**  
   The conversion from AoI to along-track uncertainty using \(\dot{\sigma}=0.5\) m/s is not justified and may be misleading. Either provide a defensible bound with citations (covariance propagation / typical TLE error growth / GNSS-denied nav drift), or present AoI as a coordination freshness metric without asserting conjunction tolerance.

---

## Minor Issues

1. **Equation/variable clarity**
   - Eq. (23) (\(L_{\text{cmd}}\)) uses \(\alpha_{\text{RX}}\) before it is defined; consider defining \(\alpha_{\text{RX}}\) earlier in Section IV-A.
   - Eq. (24–25): define \(\bar{M}_r\) precisely (expected retransmission fraction per slot? per message?).
   - Table I: “TDMA required? Yes (\(\gamma \ge 0.67\))” — clarify that this is based on stress-case \(\eta_{\text{total}}\) and assumes slotted ALOHA \(\gamma\approx 0.36\); otherwise the threshold seems arbitrary.

2. **Consistency of “baseline telemetry excluded from \(\eta\)”**  
   Table VI AoI experiments: “Full reporting … \(\eta=46\%\) includes stress-case commands + heartbeats + summaries.” That makes AoI results depend on a workload that includes commands, but AoI is about status freshness. Consider separating AoI experiments from command traffic, or explicitly state that commands are included only to keep a consistent “stress-case channel load,” even though AoI is measured on ephemeris delivery.

3. **DES vs analytical enforcement**  
   Section IV-D correctly notes DES does not enforce TDMA airtime. Consider adding a prominent note near Table XIII (link availability) and Table IX (joint interaction) that these “delivery” rates are *not* airtime-feasible in Regime B, to avoid misinterpretation.

4. **Global-state mesh scaling statement**  
   Section III-B global-state mesh: “59 convergence rounds” at \(N=10^5\) with \(f=N/\log N\) seems inconsistent with typical gossip analyses; since this is an intentional upper bound, consider simplifying: show per-node bytes per round and note even one round is infeasible at 1 kbps, avoiding potentially disputable round-count details.

5. **Editorial/formatting**
   - Fig. 9 includegraphics lacks extension (`fig-cross-cycle-recovery` vs `.pdf`), may break compilation depending on environment.
   - Table XII header “Mesh” vs “Global” is confusing (it lists both “Mesh” and “Global” columns). Consider renaming columns to “Sectorized mesh” and “Global-state mesh.”

---

## Overall Recommendation — **Major Revision**

The paper has strong potential and contains valuable design-level insights, but several core quantitative claims (feasibility across bandwidth regimes, coordinator sizing bounds, availability, and AoI operational interpretation) require tighter, more internally consistent modeling and clearer separation of what is validated vs assumed. With revisions that (i) formalize the coordinator sizing derivations, (ii) consistently gate feasibility by airtime under half-duplex TDMA, and (iii) either formalize or soften reliability/AoI operational claims, the manuscript could be a strong T-AES contribution.

---

## Constructive Suggestions

1. **Reframe Results around a strict feasibility “gating” workflow (byte → MAC → airtime) per workload.**  
   Add a single summary table that, for each workload (Nominal/Event/Stress-bcast/Stress-unicast), reports: \(\eta\), \(\eta_{\text{total}}/\gamma\), ingress airtime, egress airtime, and whether retransmissions fit. This would operationalize your “three-layer feasibility” claim and remove ambiguity.

2. **Provide a rigorous derivation (or appendix) for Model A/B coordinator ingress sizing.**  
   For Model A, derive/approximate the distribution of the minimum spacing among \(k_c-1\) uniform arrival times on \([0,T_c)\) and show how the \(10^{-3}\) quantile yields ~50 kbps. For Model B, specify the queue/buffer evolution equation and prove/compute the zero-overflow condition. This will make Section IV-A publishable as a reusable sizing result.

3. **Unify retransmission discussion with TDMA airtime constraints.**  
   Explicitly set \(M_r=0\) for Regime B in all performance tables/figures that are meant to reflect the RF-backup case, and treat \(M_r>0\) as a separate “Regime A” analysis (as you start to do in Table XIII). This will prevent readers from overestimating reliability in the design-driving regime.

4. **Either formalize availability or clearly label it as illustrative.**  
   If you keep Fig. 12 and “99.5%,” provide the underlying stochastic model (states, transitions, detection time, election time, optical outage process, RF availability assumptions) and show how fleet/cluster availability is computed. Otherwise, re-label as “illustrative availability estimate” and avoid precise percentages in the abstract/conclusion.

5. **Tone down or support the conjunction/AoI coupling with a cited navigation/error-growth model.**  
   Replace the linear \(\dot{\sigma}\) mapping with either (i) a covariance propagation reference and parameterization, or (ii) a requirement-driven statement: “If along-track uncertainty grows at \(\le X\) m/s, then AoI P99 implies \(\le Y\) m.” This keeps the useful intuition without overclaiming operational sufficiency.

If you want, I can also propose a tightened abstract and a revised “Assumptions & Validity Domain” box that would make the message-layer nature and feasibility gating unambiguous to reviewers.