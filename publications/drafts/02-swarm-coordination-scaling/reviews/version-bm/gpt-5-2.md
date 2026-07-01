---
paper: "02-swarm-coordination-scaling"
version: "bm"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-02-27"
recommendation: "Unknown"
---

## 1. Significance & Novelty — **Rating: 4/5**

The manuscript targets a real and timely scaling gap: coordination architectures for autonomous swarms in the \(10^3\)–\(10^5\) regime with explicit byte budgets and cycle timing. The paper’s core contribution—closed-form “sizing equations” that separate (i) byte budget/utilization \(\eta\), (ii) MAC efficiency \(\gamma\), and (iii) TDMA airtime feasibility—is practically valuable. The explicit superframe budget (Table \ref{tab:superframe}) and the distinction between information budget vs. airtime schedulability (Type 1 broadcast vs. Type 2 unicast; Eq. \ref{eq:unicast_stagger}) are particularly useful to system designers and are not commonly laid out in the swarm/constellation autonomy literature.

That said, some novelty claims are slightly overstated. There is substantial prior work on hierarchical aggregation, cluster heads, and constellation networking (routing/scheduling/DTN), and the paper’s novelty is best framed as: *a coherent, parameterized accounting framework with closed-form design equations and explicit feasibility layers*, rather than “no prior work provides” such relationships. The paper would be stronger if it more crisply positions itself against: (a) hierarchical control/telemetry architectures in distributed spacecraft missions, (b) cluster-head WSN-style analyses (even if terrestrial), and (c) ISL scheduling literature that already addresses TDMA-like constraints in constellations.

Overall, the contribution is important and likely to influence early-phase architecture trades. The work is also unusually explicit about what is and is not modeled, which improves its utility as an engineering “sizing” reference.

---

## 2. Methodological Soundness — **Rating: 3/5**

The methodology is internally consistent: a message-layer DES is used primarily as an implementation cross-check for the derived equations (e.g., Table \ref{tab:inflection}) and to estimate tail behavior under the GE model (Fig. \ref{fig:cross_cycle_recovery}). The cycle-aggregated DES is appropriate for scaling to \(10^5\) nodes and for the stated objective (“message-layer predictions”), and the paper is commendably transparent that it is not packet/PHY validated (Section \ref{sec:validation_gap}). Reproducibility is also a strength: code and tag are provided.

However, several modeling choices materially affect the results and are not yet justified to “transactions” standards:

* **Coordinator ingress modeling mismatch:** The DES uses a *fluid server* ingress with drop-tail (Section \ref{sec:des_architecture}), while the key feasibility claims hinge on *half-duplex TDMA airtime* (Section \ref{sec:coordinator_bandwidth}, Eqs. \ref{eq:ingress_feasibility}–\ref{eq:egress_feasibility}). This is not just an implementation detail: under TDMA, corrupted packets consume airtime, retransmissions consume airtime, and half-duplex partitioning couples ingress/egress tightly. The paper acknowledges this (Joint Interaction section) but still uses DES drop counts (Table \ref{tab:joint_interaction}) in ways that could be misread as validating the TDMA sizing. A reviewer would expect either (i) a TDMA-enforcing simulation for at least a single cluster, or (ii) a more formal separation: “DES validates byte accounting only; TDMA feasibility rests solely on analytic budget.”

* **Loss model granularity:** The GE model is defined per-cycle constant state (Section \ref{sec:ge_link}), which *by construction* makes intra-cycle retransmission ineffective. The manuscript acknowledges this, but then uses the result to motivate design conclusions about retransmission infeasibility. This is acceptable as a conservative bound, but you should provide at least a sensitivity case with sub-cycle coherence (e.g., state transitions per slot or per second) to show how much the “27% vs 87.5%” conclusion depends on the coherence assumption.

* **Statistical reporting:** For overhead, 30 replications are fine because variance is tiny. For tail metrics (AoI P99, recovery P95), the paper reports bootstrap CIs, which is good, but it should be clearer about dependence/ergodicity: AoI samples every 100 s over a 1-year run are not independent; bootstrapping across per-run P99s is reasonable, but you should state that the CI is across runs, not across raw samples. Similarly, GE recovery tails depend on the number of burst events; reporting the number of recovery events observed would strengthen credibility.

---

## 3. Validity & Logic — **Rating: 3/5**

Many conclusions are supported by the presented accounting, especially those that follow directly from deterministic byte math: e.g., \(\eta_{\text{cmd}}\) scaling with \(C_{\text{node}}\) and \(T_c\), the small contribution of summaries, and the coordinator ingress mean-rate requirement \(k_c S_{\text{eph}}8/T_c\). The separation into three feasibility layers is logically clean and helps avoid common confusion between *information volume* and *airtime schedulability*.

The main validity concerns are where the manuscript moves from message-layer accounting to strong feasibility statements:

* **“At \(\ge 10\) kbps, all constraints are non-binding.”** This is plausible *within the model*, but the paper’s own superframe analysis suggests tight coupling among \(\gamma\), guard times, ranging, and half-duplex turnaround at 24–30 kbps. At 10 kbps, airtime per 256 B report is \(\sim 205\) ms (before overhead), which implies very different slot timing; the paper should explicitly recompute the TDMA feasibility layer at 10 kbps rather than infer it from byte utilization. Otherwise, readers may interpret “non-binding” as a physical conclusion rather than a message-layer one.

* **AoI interpretation:** Eq. \ref{eq:aoi_analytic} matches the DES under the exception-telemetry Bernoulli model, which is good. But the paper’s AoI narrative risks conflating “exception reporting probability” with a realistic sensor/estimator triggering policy. In practice, exception triggers correlate with dynamics, conjunction seasons, maneuver campaigns, etc. The paper should more strongly qualify that AoI here is a function of a stylized Bernoulli exception process, not an estimator-driven event trigger.

* **Command model and \(\eta\):** You define \(\eta\) as information content per node per cycle, not PHY airtime, which is defensible. But then comparisons across architectures (hierarchical vs sectorized mesh) implicitly assume comparable semantics. The paper does attempt to address functional scope (Table \ref{tab:capability_matrix}), but the central claim “commands dominate stress-case, topology-invariant” depends on assuming centralized command generation and identical addressing semantics. This should be elevated from a parenthetical to a clearly stated assumption in the model definition, because alternative architectures (distributed decision making, local negotiation) change command volume and addressing.

Limitations are acknowledged candidly (Section \ref{sec:limitations}), which improves balance. Still, a few conclusions should be softened or bounded more explicitly as “under the message-layer abstraction and dedicated scheduled access.”

---

## 4. Clarity & Structure — **Rating: 4/5**

The manuscript is generally well organized for an IEEE T-AES audience. The “roadmap” at the start of Results is helpful, and the repeated emphasis on what the DES validates (consistency) vs. what remains future work (packet/PHY) is good scholarly hygiene. Tables are mostly effective; Table \ref{tab:superframe} is a standout because it turns abstract \(\gamma\) discussions into concrete timing.

There are, however, clarity issues stemming from overloaded terminology and occasional mixing of layers:

* **\(\eta\) vs \(\eta_{\text{total}}\) vs \(\eta/\gamma\):** The paper defines these clearly, but the narrative sometimes jumps between them without reminding the reader which one is being used to claim feasibility. For example, Table \ref{tab:schedulability} is good, but the text around “stress-case exceeds Slotted ALOHA capacity, confirming TDMA is required” could be tightened to explicitly reference \(\eta_{\text{total}}/\gamma\) and the assumed \(\gamma\) values.

* **Centralized baseline:** The centralized model is compute-queue only, while others are communication-layer. You do label this, but the comparison plots/tables (e.g., Fig. \ref{fig:overhead_scaling}, Table \ref{tab:topology_comparison}) still risk confusing readers because they place “centralized” alongside comm-overhead numbers. Consider visually separating “compute-only bound” from “comms-modeled” architectures, or removing centralized from overhead plots entirely.

* **Some numerical claims need tighter provenance:** e.g., “Coordinator ingress requires 24 kbps under half-duplex TDMA with 623 ms per-cycle margin” is supported by Table \ref{tab:superframe}, but the abstract also states “At \(\ge 10\) kbps, all constraints are non-binding,” which is not shown via an equivalent superframe at 10 kbps.

Overall readability is strong, but the paper would benefit from a more explicit “model stack” diagram (message model → MAC abstraction via \(\gamma\) → TDMA airtime check → DES used only for byte/loss event accounting).

---

## 5. Ethical Compliance — **Rating: 4/5**

The manuscript includes an explicit disclosure that AI-assisted ideation influenced aspects of the architecture (Acknowledgment with citation \cite{dyson_multimodel}). This is aligned with emerging transparency expectations, and it appropriately states that the AI-derived aspects are “not validated here.” Data/code availability is also strong and supports reproducibility.

Two improvements are needed for full compliance/clarity in an IEEE Transactions context:

1. **Authorship/affiliation placeholder:** The author block currently uses a “Project Dyson Research Team” placeholder with a note that names will be provided later. That may be acceptable for review, but final submission must include full authorship, affiliations, and any conflicts of interest/funding sources. Consider adding a standard “Funding/COI” statement even if “none.”

2. **AI use boundary:** The acknowledgment is good, but it would be clearer to state whether AI tools were used for *writing/editing* vs. only ideation. IEEE venues increasingly care about whether AI generated text/figures/code. A one-sentence clarification would prevent misunderstandings.

---

## 6. Scope & Referencing — **Rating: 3/5**

The topic is appropriate for IEEE Transactions on Aerospace and Electronic Systems: it sits at the intersection of spacecraft autonomy, constellation operations, and communications architecture sizing. The paper also uses relevant concepts (AoI, queueing, GE channels) that are within scope.

Referencing is broad and includes key classics (Lynch, Lamport, Raft, AoI survey) and constellation networking (Handley, del Portillo). However, several citations are non-archival or “accessed 2026” web sources (Kuiper overview, DARPA pages, etc.). While some of this is unavoidable for operational programs, T-AES generally expects archival sources where possible. Also, the paper would benefit from stronger engagement with:

* **Spacecraft formation flying / distributed spacecraft autonomy literature** that discusses hierarchical telemetry/command architectures and onboard autonomy constraints (beyond the single NASA DSA reference).
* **TDMA/proximity networking in space** beyond CCSDS Proximity-1, including more recent smallsat crosslink MAC/PHY studies.
* **WSN cluster-head scaling analyses** (even terrestrial) as a conceptual prior art for hierarchical aggregation and coordinator rotation overheads.

Finally, some claims cite no source (e.g., specific radio turnaround times “Proximity-1 class radios \(\sim 2\) ms” is plausible but should be tied more directly to a spec, measurement, or range).

---

## Major Issues

1. **DES does not enforce TDMA/half-duplex airtime constraints, yet results are used alongside TDMA feasibility claims.**  
   *Where:* Section \ref{sec:des_architecture} (fluid-server ingress), Section \ref{sec:coordinator_bandwidth} (TDMA feasibility), Section \ref{sec:joint_interaction} (explicit note).  
   *Why it matters:* Under TDMA, losses and retransmissions consume airtime; half-duplex partitions ingress/egress; queueing/drops and schedulability are coupled. The current DES cannot validate claims such as “drops eliminated at 25 kbps with phase staggering” in a way that maps to TDMA operation.  
   *What to change:* Either implement a minimal TDMA scheduler in the DES (single-cluster is sufficient) or strictly reframe DES outputs as “byte-layer only,” removing/softening any implication of airtime validation.

2. **GE coherence assumption makes retransmission ineffectiveness a modeling artifact; needs sensitivity.**  
   *Where:* Section \ref{sec:ge_link}.  
   *Why it matters:* The key contrast (27% vs 87.5%) is largely driven by “state constant within cycle.” Real channels may change state within 10 s.  
   *What to change:* Add at least one alternative GE configuration with sub-cycle transitions (e.g., per-slot or per-1s) and show how intra-cycle recovery changes, or justify empirically/with references that coherence \(\ge T_c\) is typical for the RF-backup scenario.

3. **The “\(\ge 10\) kbps non-binding” claim is not demonstrated at the airtime layer.**  
   *Where:* Abstract; Table \ref{tab:bandwidth_scaling}; Discussion/Conclusion statements.  
   *Why it matters:* Byte utilization scaling alone does not ensure half-duplex schedulability, especially with guard times, control overhead, and retransmissions.  
   *What to change:* Provide a 10 kbps TDMA superframe budget (analogous to Table \ref{tab:superframe}) and explicitly show ingress/egress feasibility, or qualify the claim as “byte-budget non-binding.”

4. **Centralized baseline is compute-only; mixing it with comm-modeled architectures risks invalid comparisons.**  
   *Where:* Section “Centralized Ground Processing,” Fig. \ref{fig:overhead_scaling}, Table \ref{tab:topology_comparison}.  
   *What to change:* Separate compute scaling from comm scaling more cleanly (e.g., a dedicated figure/table), or add a minimal comm model for centralized (uplink/downlink scheduling) so that “overhead” comparisons are apples-to-apples.

---

## Minor Issues

1. **Equation/definition consistency:** Table \ref{tab:notation} defines \(\eta_{\text{total}} = \eta + 20.5\%\) baseline, but some prose refers to “protocol overhead adds 1–41%” and “stress-case command traffic adds 1–41%” (Abstract/Contributions). Consider explicitly stating whether those percentages are of the 1 kbps budget *excluding* baseline, to avoid confusion.

2. **Coordinator ingress formula uses \((k_c-1)\) in places and \(k_c\) in others.**  
   *Where:* Section \ref{sec:coordinator_bandwidth} (e.g., \(k_c-1\) members send reports; Eq. \ref{eq:tdma_capacity} uses \(k_c-1\); later “\(k_c\) members each send … requiring 20.5 kbps”).  
   *Fix:* Standardize: either define “cluster size includes coordinator” and always use \(k_c-1\) for member uplinks, or define \(k_c\) as non-coordinator members.

3. **Fig. \ref{fig:cross_cycle_recovery} includegraphics missing extension** (`fig-cross-cycle-recovery` no `.pdf`). Likely a LaTeX build issue.

4. **Table \ref{tab:cluster_size} latency note conflicts with earlier decomposition.** It says latency includes cycle alignment \(T_c/2\), but Table \ref{tab:latency_breakdown} totals \(\sim 260\) ms without alignment. Ensure consistent latency definition across tables/figures.

5. **Availability numbers are not tightly derived.** Table \ref{tab:topology_comparison} lists hierarchical “Graceful (99.5%)” while Section on duty cycle says per-coordinator \(A>99.99\%\) and 99.5% is “conservative.” Consider either deriving 99.5% from an explicit model or labeling it as an illustrative placeholder.

6. **Non-archival citations:** Several web/program references are non-archival; where possible, add archival counterparts or technical reports (FCC filings are fine; marketing pages less so).

---

## Overall Recommendation — **Major Revision**

The paper is promising and likely publishable, but it currently blurs the boundary between message-layer accounting (what the DES validates) and airtime/MAC feasibility (what the strongest design conclusions rely on). The central results would be significantly strengthened by either (i) adding a minimal TDMA/half-duplex enforcing simulation at the single-cluster level, or (ii) more rigorously limiting claims to the message layer and demonstrating airtime feasibility across bandwidth regimes with explicit superframe budgets. Addressing the GE coherence sensitivity and cleaning up baseline comparisons would also be necessary for a Transactions-level contribution.

---

## Constructive Suggestions

1. **Add a “single-cluster TDMA enforcement” experiment (even small-scale) to validate Table \ref{tab:superframe} and the ingress/egress feasibility inequalities.**  
   Implement slot-level scheduling with half-duplex switching and model packet errors consuming airtime. Use it to validate the 24–30 kbps sizing and to quantify how much margin is lost under realistic control/FEC overhead.

2. **Provide a TDMA superframe budget at 10 kbps (and/or 100 kbps) to support the “non-binding” regime claims.**  
   Mirror Table \ref{tab:superframe} at 10 kbps, showing slot durations, ingress fraction, and egress window. If infeasible without changing \(T_c\) or \(k_c\), that is an important correction to the current narrative.

3. **Add GE coherence-time sensitivity (sub-cycle transitions) and report how intra-cycle retransmission effectiveness changes.**  
   A simple extension: allow GE transitions every \(m\) slots or every 1 s; show recovery probability and P95 recovery cycles vs. coherence. This will prevent readers from dismissing the retransmission conclusions as purely an artifact.

4. **Make command semantics and addressing assumptions explicit in the model definition, and separate “information budget” from “airtime budget” in the overhead comparisons.**  
   Consider adding a small table that lists for each command type: information counted toward \(\eta\), PHY transmissions required, and schedulability condition. This will also clarify why \(\eta_{\text{cmd}}\) can be topology-invariant while airtime is not.

5. **Refactor centralized baseline presentation to avoid apples-to-oranges comparisons.**  
   Either (a) remove centralized from overhead plots/tables and keep it only as a compute-latency bound, or (b) add a minimal comm model (contact time, uplink rate) so the centralized baseline can be compared on the same axes as hierarchical/mesh.

If you’d like, I can also propose a concise “model stack” figure and a rewritten abstract that more carefully separates message-layer results from airtime/MAC feasibility claims.