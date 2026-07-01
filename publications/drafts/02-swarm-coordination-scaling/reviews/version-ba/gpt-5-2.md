---
paper: "02-swarm-coordination-scaling"
version: "ba"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-02-27"
recommendation: "Unknown"
---

## 1. Significance & Novelty — **Rating: 4/5 (Good)**

The manuscript targets a practically important and timely problem: how to size coordination/telemetry/control communications and coordinator capacity for very large autonomous spacecraft swarms (10³–10⁵) under a stringent per-node RF-backup budget. The focus on *byte-level accounting* and on *parameterized closed-form “design equations”* is a useful contribution for practitioners, especially because much of the constellation literature either (i) assumes ample bandwidth, (ii) focuses on routing/ISLs rather than coordination workloads, or (iii) studies far smaller swarm sizes. The explicit separation of topology-invariant baseline telemetry (20.5%) from topology-dependent overhead \(\eta\) is also a helpful framing.

That said, the novelty is somewhat constrained by the fact that many analytical components are standard (M/D/1, geometric tails for exception reporting, GE/Markov recovery). The paper’s value is primarily in *integration* and *engineering synthesis* (a coherent sizing toolkit with cross-checks), rather than in new theory. For T-AES, that can still be publishable if the assumptions and operational mapping are tightened and the “design equations” are presented as broadly reusable artifacts with clearly defined validity domains.

A further novelty risk is that the “stress-case” command model (one 512 B command per node per cycle) drives many headline numbers (e.g., \(\eta \approx 46\%\)) yet is not convincingly tied to realistic autonomous operations at 10 s cadence. The paper partially addresses this via workload profiles (Section IV-E), but the stress-case still dominates the narrative, and reviewers/readers may question whether the key conclusions depend on an extreme workload.

---

## 2. Methodological Soundness — **Rating: 3/5 (Adequate)**

The cycle-aggregated DES is appropriate for the stated goal—message-layer sizing and accounting—and the manuscript is generally transparent about what is modeled vs abstracted (Table I? actually Table~\ref{tab:abstraction}). The separation between “DES as arithmetic consistency check” and “physical fidelity remains future work” (Sections III-A and V-A) is candid and, in principle, methodologically sound. The Monte Carlo replication count (30) is reasonable for stable mean metrics like overhead; the per-run P99 aggregation approach for AoI is a good practice to avoid pseudo-replication (Table~\ref{tab:aoi_results} note).

However, several modeling choices materially affect the main results and are not yet justified to the level expected for T-AES:

* **Coordinator ingress modeling vs TDMA feasibility**: Section IV-A mixes three ingress models (deadline, token bucket, TDMA) and concludes “21–25 kbps” as the recommendation. But the TDMA feasibility constraints (Eqs. (19)–(20) / \ref{eq:ingress_feasibility}–\ref{eq:egress_feasibility}) show that retransmissions under GE (\(\bar M_r=0.18\)) make ingress time exceed \(T_c\). This means the “token bucket smoothing” analogy to TDMA (Table~\ref{tab:coord_summary_v2} footnote) is not generally valid once time-slot feasibility is binding. The paper recognizes this later, but the sizing recommendation still reads as if byte-rate is the only constraint.

* **GE model coherence assumption**: Section IV-C explicitly assumes the GE state is constant within a 10 s cycle, which indeed makes intra-cycle retries ineffective “by model construction.” While the authors state this is conservative for recovery, it also makes the comparison between i.i.d. and GE partly an artifact of time discretization. A more defensible approach would be to parametrize coherence time \(\tau_c\) explicitly and show regimes where intra-cycle ARQ helps vs does not (even with a simple two-timescale model).

* **Sectorized mesh comparator**: The capped sectorized mesh is acknowledged to be disconnected and to provide only ~3% intra-sector awareness at cap=10 (Section III-B4). This undermines its value as a “coordination architecture” comparator: overhead per “unit of awareness” is an interesting metric, but it is not a standard or validated measure. As written, the comparison risks being seen as a strawman unless the paper either (i) makes the sectorized mesh deliver a defined coordination function (e.g., bounded-diameter dissemination within sector), or (ii) reframes it explicitly as a *local-neighborhood awareness* baseline, not a coordination baseline.

Reproducibility is a strength (open-source tag and environment), but the manuscript would benefit from a concise “how to reproduce Figure X/Table Y” appendix or a reproducibility checklist (inputs, seeds, runtime, scripts), because T-AES readers will not all chase a GitHub repo.

---

## 3. Validity & Logic — **Rating: 3/5 (Adequate)**

Many conclusions are logically consistent with the presented accounting. For example: (i) \(\eta\) being \(O(1)\) under hierarchical aggregation (Eq.~\ref{eq:hierarchical_messages}) is correct; (ii) command bytes dominating stress-case overhead is a straightforward arithmetic consequence (Section IV-E, Fig.~\ref{fig:decomposition}); (iii) AoI P99 under exception reporting matching a geometric tail (Eq.~\ref{eq:aoi_analytic}) is correct and nicely cross-validated against DES (Table~\ref{tab:aoi_results}).

The most important validity concern is that several headline claims blend *offered load accounting* with *feasible scheduling* without fully reconciling them. The paper correctly notes that under TDMA, losses consume slot time and intra-cycle retries are infeasible at the stated parameters (Section IV-A, “TDMA frame-time feasibility”). Yet other parts still discuss retransmissions \(M_r=2\) as if they are implementable within-cycle under TDMA for the full cluster population (e.g., Table~\ref{tab:link_availability} and parts of Section IV-H3). If the intended architecture is TDMA in RF-backup mode, then the link-availability table should either (a) be explicitly labeled as “byte-budget only, ignoring slot feasibility,” or (b) be recomputed under a feasible retransmission policy (e.g., only some nodes retry per cycle, or retries occur in subsequent cycles via ARQ/DTN).

Similarly, the “pipeline decoupling” conclusion (Section IV-D) is valid only under dedicated links where losses prevent arrivals to the queue *and* where the scheduling layer is not the bottleneck. The manuscript does state the caveat (TDMA couples via slot time), but the design implication “size coordinator byte-rate independently of GE parameters” is only safe if the system has enough slack in the TDMA schedule (or uses a different PHY/MAC). As written, a practitioner might under-design time resources while meeting byte-rate.

The limitations section is generally honest and covers key gaps (physical layer, priority, correlated failures, static topology). Still, some limitations are *first-order* for the claimed operating point (1 kbps RF backup + TDMA + half-duplex + retransmissions), and should be elevated earlier (e.g., in the abstract or the beginning of Results) to avoid over-reading of precise numeric recommendations.

---

## 4. Clarity & Structure — **Rating: 4/5 (Good)**

The paper is well structured and unusually explicit about definitions, accounting choices, and what is/ չէ is not included in \(\eta\). The “Roadmap” at the start of Results is helpful, and the tables are generally informative. The manuscript also does a good job of providing “engineering narrative” around equations (e.g., coordinator rotation, half-duplex partitioning, slot composition).

There are, however, clarity issues that could mislead readers:

* **Overload of percentages**: The paper uses baseline utilization (20.5%), protocol overhead \(\eta\), total utilization \(\eta_{\text{total}}\), and effective utilization \(\eta/\gamma\). These are reasonable, but the narrative sometimes jumps between them quickly (e.g., Introduction contributions vs Section IV-A vs sensitivity). A single consolidated notation table (symbols, units, where defined) would reduce cognitive load.

* **Abstract precision vs validation scope**: The abstract reports very specific values (e.g., “AoI P99 = 440 s,” “P95 in 4 cycles,” “verified to within 0.1%”), which is fine for message-layer arithmetic, but it reads like end-to-end performance claims. Given the stated validation gap, the abstract should more explicitly qualify that these are *message-layer design-equation outputs under the assumed traffic/MAC abstraction*.

* **Sectorized mesh framing**: The admission that the capped mesh is disconnected is commendable, but then the architecture comparison table (Table~\ref{tab:topology_comparison}) still positions “sectorized mesh” as an intermediate decentralized architecture with \(\eta\approx 65\%\). That risks confusion: intermediate in what sense—overhead, awareness, or coordination capability? The paper should either define a coordination objective that sectorized mesh satisfies, or avoid presenting it as a coordination competitor.

Figures appear central but are not provided here (only references). Ensure each figure caption is self-contained and that axes/units are explicit—especially for the recovery curves and TDMA feasibility plots.

---

## 5. Ethical Compliance — **Rating: 4/5 (Good)**

The manuscript includes an explicit disclosure about AI-assisted ideation in the Acknowledgment and clarifies that the AI-assisted elements are not “validated here.” That is aligned with emerging IEEE transparency expectations. The open-source release and parameter disclosure also support research integrity.

Two improvements are advisable for full compliance and reader trust: (i) specify whether any text, code, or figures were AI-generated vs merely ideated, and what human verification steps were used; (ii) add a brief conflict-of-interest statement regarding “Project Dyson Research Team” and the hosted website/repo (even if simply “The authors declare no competing financial interests.”). T-AES often expects explicit COI language.

---

## 6. Scope & Referencing — **Rating: 3/5 (Adequate)**

The topic is appropriate for IEEE Transactions on Aerospace and Electronic Systems, particularly at the intersection of constellation operations, autonomy, and comms-constrained coordination. The paper also connects to distributed systems theory and networking, which is acceptable for T-AES when grounded in aerospace operational constraints (RF backup, TT&C, ISL availability, conjunction screening).

References are generally relevant and include key classics (Lynch, Demers gossip, Kleinrock, AoI surveys) and constellation/ISL papers (Handley, del Portillo). However, several citations are non-archival or operational filings (SpaceX FCC filing, Amazon overview, DARPA pages). Some of these are unavoidable for current constellation facts, but T-AES typically prefers archival sources for foundational claims. Where possible, replace or supplement with peer-reviewed/archival sources on (i) Starlink/OneWeb operational coordination practices, (ii) TT&C bandwidth allocations and S-band link budgets, (iii) measured LEO ISL/channel blockage statistics, and (iv) conjunction screening operational pipelines.

Also, the paper’s “no prior work has systematically compared…” claim in the Introduction is strong; it should be softened or better supported with a more systematic related-work gap analysis (what dimensions are missing in prior work: byte-level accounting, 10^5 scale, hierarchical vs mesh, AoI, GE burst recovery, etc.).

---

## Major Issues

1. **TDMA time-feasibility vs retransmission modeling inconsistency (Section IV-A, IV-H3, Table~\ref{tab:link_availability})**  
   The manuscript shows that under TDMA the slot schedule is already ~92% utilized for ingress and that GE-average retransmission load makes ingress exceed \(T_c\) (Eqs.~\ref{eq:ingress_feasibility}–\ref{eq:egress_feasibility}). Yet later results (e.g., Table~\ref{tab:link_availability}) treat \(M_r=2\) as generally applicable. You need a consistent retransmission policy that is *schedulable* under the proposed MAC (or clearly separate “byte-budget success” from “time-feasible success”).

2. **Coordinator ingress sizing recommendation depends on access model; token-bucket ≠ TDMA under deadline semantics (Section IV-A, Table~\ref{tab:coord_summary_v2})**  
   Model B’s carry-over tokens can mask burstiness without violating “timeliness” only if arrivals are not delayed—however in real systems, smoothing implies either buffering at sender or receiver, which can violate per-cycle inclusion unless explicitly scheduled. The paper asserts equivalence to TDMA “when slots fill a full cycle,” but TDMA is a time-division guarantee, not a token accounting mechanism. Tighten the argument: derive sizing directly from TDMA slot budget (including guard, sync, half-duplex partition) and treat token-bucket as a separate non-TDMA abstraction.

3. **Sectorized mesh baseline is functionally under-defined / disconnected (Section~\ref{sec:sectorized_mesh_model})**  
   You acknowledge the capped mesh does not create a connected graph, so it cannot support many coordination tasks. Presenting it as an “intermediate decentralized architecture” then becomes questionable. Either (a) modify the sectorized mesh so it achieves a defined coordination goal (e.g., bounded dissemination within sector with high probability), or (b) reframe it as a *local-neighborhood awareness* baseline and adjust comparative claims accordingly.

4. **GE coherence-time assumption drives the “intra-cycle retries ineffective” conclusion (Section~\ref{sec:ge_link})**  
   Because GE state is constant within \(T_c\), the conclusion that ARQ is ineffective is partly imposed. You should add a sensitivity study where GE transitions occur at sub-cycle granularity (even a simple model with \(m\) sub-slots per cycle) to demonstrate when the conclusion holds. Otherwise, the design guidance about inter-cycle recovery may be over-generalized.

5. **Command model realism and broadcast/unicast ambiguity (Section IV-A “Command dissemination model”, workload profiles in IV-E)**  
   The paper simultaneously (i) counts command bytes per node in \(\eta\), (ii) argues commands can be broadcast once per cluster, and (iii) uses a stress-case of one command per node per cycle. These are different operational semantics. You need to clearly define what a “command” is: cluster-wide command vs individualized per-node command, and how often each occurs. The overhead and feasibility implications differ by orders of magnitude.

---

## Minor Issues

1. **Equation detail/notation**
   - Eq.~\ref{eq:tdma_capacity}: uses \((k_c-1)\) but earlier coordinator ingress demand uses \(k_c\). Clarify whether the coordinator itself is excluded from sending a report (hence \(k_c-1\)) and apply consistently throughout.
   - Eq.~\ref{eq:mesh_messages}: the step “with \(f=O(N/\log N)\)” is an unusual choice; typical gossip uses constant fanout. If you intentionally choose large \(f\) to force convergence within one cycle, state that explicitly and justify why that is the right operational comparator.

2. **Centralized baseline messaging vs compute-only**
   - Table~\ref{tab:topology_comparison} lists centralized “scalability limit” but omits comms overhead by design. This is fine, but then Fig.~\ref{fig:overhead_scaling} caption says “Centralized diverges at 10^4,” which could be misread as comms divergence. Consider renaming curves/labels to “compute queueing only” and avoid mixing with comms-layer curves.

3. **AoI sampling**
   - Table~\ref{tab:aoi_results}: AoI sampled every 100 s. For \(T_c=10\) s, this down-samples the sawtooth process; for P99 tails driven by long gaps it’s probably fine, but state explicitly why 100 s sampling does not bias P99 (or provide a quick check at 10 s sampling for one configuration).

4. **Figure file naming**
   - Fig.~\ref{fig:cross_cycle_recovery} includes `\includegraphics{fig-cross-cycle-recovery}` without extension; ensure consistent compilation and that the PDF is included. (Minor but common LaTeX portability issue.)

5. **Non-archival citations**
   - Several web citations are “non-archival; accessed Feb 2026.” For T-AES, try to anchor key operational facts with archival sources where possible, keeping web sources as supplementary.

---

## Overall Recommendation — **Major Revision**

The manuscript has strong potential as an engineering synthesis paper and is unusually transparent in its accounting and tooling. However, several core quantitative recommendations (coordinator capacity, retransmission effectiveness, and comparative baseline conclusions) are not yet internally consistent across MAC feasibility, retransmission policy, and command semantics. Addressing these issues will likely require reworking parts of the model and re-presenting results with clearer validity domains. With those revisions, the paper could become a solid T-AES contribution.

---

## Constructive Suggestions

1. **Unify the MAC/PHY feasibility story with a single “schedulable policy”**  
   Pick one operational RF-backup MAC (e.g., half-duplex TDMA) and define a feasible retransmission/ARQ policy under that schedule (e.g., no intra-cycle retries; or retries allocated to a reserved contention window; or only a bounded number of nodes retry per cycle). Recompute Table~\ref{tab:link_availability} and any success/overhead claims under that *feasible* policy, and clearly separate “byte budget” from “time budget.”

2. **Clarify command semantics and provide two command workload models**  
   Introduce two explicit command types: (i) *cluster broadcast command* (one message affects many nodes), and (ii) *individualized per-node command*. Provide separate overhead equations and feasibility checks for each, and map the workload profiles (Stress/Nominal/Event-driven) onto these types. This will make the “commands dominate overhead” conclusion more interpretable and actionable.

3. **Strengthen the GE model by adding a coherence-time sensitivity knob**  
   Extend Section~\ref{sec:ge_link} with a simple sub-cycle GE variant: divide \(T_c\) into \(m\) sub-intervals with transitions allowed each sub-interval (or equivalently scale \(p_{GB},p_{BG}\)). Show when intra-cycle retries become useful as \(\tau_c/T_c\) decreases. This will convert the current “by construction” limitation into a parametric design curve.

4. **Reframe or repair the sectorized mesh baseline**  
   Either:
   - make the sectorized mesh connected with high probability (e.g., random geometric graph with degree scaling to ensure connectivity) and evaluate its overhead/latency accordingly; or
   - rebrand it as “local-neighborhood awareness mesh” and remove claims that it is an “intermediate coordination architecture,” adjusting Table~\ref{tab:topology_comparison} and Section~\ref{sec:topology_comparison} language.

5. **Add a one-page “Design Equation Validity Domain” summary**  
   Provide a compact table listing each key equation (coordinator ingress, AoI P99, GE recovery) with: assumptions (traffic model, independence, MAC, buffering, deadlines), required inputs, and what it predicts (mean vs tail). This will significantly improve practitioner usability and reduce the risk of misapplication.