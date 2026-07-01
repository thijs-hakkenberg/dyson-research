---
paper: "02-swarm-coordination-scaling"
version: "bu"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-02-27"
recommendation: "Unknown"
---

## 1. Significance & Novelty — **Rating: 4/5 (Good)**

The manuscript targets a real and increasingly important problem: coordination/command-and-control scaling for autonomous mega-constellation–class swarms (10³–10⁵). The paper’s central value is the attempt to provide *closed-form sizing equations* with byte-level accounting, and to separate feasibility into three layers (byte budget, MAC efficiency via \(\gamma\), and TDMA airtime schedulability). That layered framing is useful and, if tightened, could become a practical engineering “back-of-the-envelope” tool for early architecture trades.

The novelty is strongest where the paper (i) explicitly distinguishes information-content budgeting (\(\eta\)) from airtime feasibility (broadcast vs per-node unicast, Eq. (36) / \(\ref{eq:unicast_stagger}\)), and (ii) couples a simple GE loss model to inter-cycle recovery distributions with an analytical Markov cross-check. The “design equations summary” section is aligned with T-AES readers who want actionable sizing relations rather than only simulation plots.

That said, some “closed-form” claims are partially undercut by key results relying on Monte Carlo (e.g., Model A “hard deadline” needing \(C_A\approx 50\) kbps is described as an MC estimate) and by the fact that the DES and the equations share the same abstraction layer. The contribution is still meaningful, but the paper should more carefully delimit what is genuinely derived vs. empirically fitted/validated within the same model class.

---

## 2. Methodological Soundness — **Rating: 3/5 (Adequate)**

The methodology is generally coherent: a cycle-aggregated DES is appropriate for exploring message-layer scaling and for cheaply sweeping \(N\), \(k_c\), and workload parameters over a 1-year horizon. Assumptions are often stated explicitly (e.g., cycle time \(T_c=10\) s, fixed message sizes, per-cycle GE state), and the paper commendably distinguishes what is modeled vs. abstracted into \(\gamma\) (Section III, “Not modeled”; Section V-A).

However, several modeling choices materially affect the conclusions and need stronger justification or sensitivity treatment. Examples: (i) the GE coherence assumption “state constant within a cycle” makes intra-cycle ARQ ineffective *by construction* (Section IV-C); this is acknowledged, but the paper then uses that result to motivate “intra-cycle ARQ infeasible” in the TDMA superframe (Section IV-A). These are different mechanisms (channel coherence vs. airtime margin). They should be disentangled with a model variant where GE transitions can occur within-cycle, or at least a sensitivity argument showing when the conclusion holds. (ii) The DES uses a fluid-server ingress and explicitly does **not** enforce TDMA slotting/half-duplex partitioning (Section IV-D); yet several headline claims (e.g., coordinator bottleneck, “zero-drop ingress requires 24 kbps,” margin 623 ms) are fundamentally airtime/slot-level. The current split “DES for bytes, analytic for airtime” is acceptable, but the paper should more rigorously ensure the two are consistent under loss/retransmission and under the assumed scheduling discipline.

Reproducibility is a strength: code and tag are provided. Still, for T-AES, the manuscript should add a short “verification/validation plan” describing what would constitute *physical-layer* validation and which conclusions are most likely to change once contention/pointing/visibility are modeled (beyond the current general disclaimer).

---

## 3. Validity & Logic — **Rating: 3/5 (Adequate)**

Many conclusions follow logically from the stated message model. For instance, \(\eta_{\text{cmd}}\) being “topology-invariant” is true *given the assumption* that the same per-node command information content must be delivered regardless of architecture (Section IV-E, decomposition). Similarly, the AoI P99 derivation under exception reporting (Eq. (44) / \(\ref{eq:aoi_analytic}\)) is consistent and matches DES.

The main validity concerns are about *what the results imply* beyond the message-layer abstraction. The abstract and conclusions sometimes read as if the sizing is close to operational reality (“Coordinator ingress requires 24 kbps under half-duplex TDMA with 623 ms margin”), but the paper later notes that TDMA scheduling is not simulated and that antenna scheduling/visibility are unmodeled. In particular, the claim “At \(\ge 10\) kbps per node … all message-layer constraints are non-binding” (Abstract; Table II) is likely fragile: at higher rates, *airtime* ceases to bind but *contact opportunities, pointing dwell time, and interference coordination* often become the dominant constraints. The paper mentions this, but the statement is currently too categorical; it should be reframed as “byte-budget constraints become non-binding under continuous scheduled access” and explicitly list what new constraints replace them.

There are also a few internal logic tensions. Example: Section IV-A states “intra-cycle ARQ is therefore infeasible; recovery relies on inter-cycle repetition” because expected retransmission airtime exceeds the 623 ms margin. But this argument uses an expected retransmission fraction derived from GE steady-state; retransmissions are not “fraction of slots” in a deterministic TDMA schedule unless you allocate explicit retransmission mini-slots or extend slots. If retransmissions occur, they must be scheduled, which changes the frame design. The paper should specify an explicit retransmission policy (reserved slack slots, end-of-frame contention, or defer-to-next-cycle) and then compute feasibility accordingly.

---

## 4. Clarity & Structure — **Rating: 4/5 (Good)**

Overall organization is strong: Introduction → Related Work → Simulation Framework → Results → Discussion/Limitations is conventional and easy to navigate. The “Roadmap” at the start of Results is helpful. Tables are generally informative (notably Tables I, II, VII, VIII, X), and the paper repeatedly provides sanity checks and cross-references.

The biggest clarity issue is the overloading and shifting meaning of “overhead” and “utilization.” You define baseline telemetry excluded from \(\eta\), then define \(\eta_{\text{total}}=\eta+20.5\%\), and also define effective overhead \(\eta_{\text{eff}}=\eta/\gamma\). This is fine, but the narrative sometimes mixes “byte budget feasibility” with “airtime feasibility,” and the reader can lose track of which layer is being discussed. I recommend adding a single boxed definition early (end of Section III-F) with a consistent naming scheme and explicitly stating the units (information bits per cycle vs. PHY bits per second vs. airtime fraction).

A few statements would benefit from tighter phrasing to avoid overclaiming. For instance, “open-source Monte Carlo tool confirms implementation consistency to <0.1%” (Abstract) is accurate but could be misread as validation; consider “equation-to-simulator consistency.” Also, some figures are referenced but not visible in the manuscript text here (e.g., Fig. \ref{fig:cross_cycle_recovery} file name missing extension; Fig. \ref{fig:cross_cycle_recovery} includegraphics lacks “.pdf”), which may be a LaTeX artifact but should be checked for final submission quality.

---

## 5. Ethical Compliance — **Rating: 4/5 (Good)**

The manuscript includes an explicit AI-assistance disclosure in the Acknowledgment, naming tools and clarifying that the ideation is not validated. That is aligned with emerging IEEE expectations and is preferable to non-disclosure.

Two items should be strengthened. First, the “Project Dyson Research Team” placeholder authorship is not acceptable for final IEEE publication, but you already note that names/affiliations will be provided later. Second, potential conflicts of interest should be clarified: the work is tied to “Project Dyson” with a website and GitHub; if this is an organizational effort with funding or commercial intent, a brief COI/funding statement would help. Nothing in the manuscript suggests unethical experimentation; the work is computational and uses public references.

---

## 6. Scope & Referencing — **Rating: 4/5 (Good)**

The topic fits IEEE T-AES (autonomous spacecraft operations, distributed coordination, comms constraints, resilience). The literature coverage is broad and mostly relevant: constellation operations, ISL routing, DTN, swarm robotics scaling, consensus/election, AoI, and queueing. The paper’s positioning—“byte-level accounting at 10⁴–10⁵ scale”—is plausible as a gap.

Referencing could be improved in two ways. (i) Several key operational claims rely on non-archival sources (e.g., Kuiper overview page; Starlink FCC filings; NRL magazine). Some are unavoidable, but for T-AES you should bolster with archival/peer-reviewed sources where possible (e.g., ISL scheduling/TDMA in space links; practical MAC efficiency measurements; constellation autonomy demonstrations). (ii) The paper uses Raft and SWIM analogies; it would help to reference space-specific autonomy and FDIR coordination protocols (even if limited) and/or CCSDS cross-support service management literature if applicable.

Finally, the paper currently compares hierarchical to a “sectorized mesh” whose functional scope is explicitly narrower (Table XIII). You acknowledge this, but the comparison still risks being interpreted as apples-to-apples. Either broaden the mesh baseline to provide comparable functions (at least within-sector full coverage) or more clearly label it as a “local neighbor monitoring baseline” rather than a coordination alternative.

---

## Major Issues

1. **TDMA/half-duplex schedulability is central but not simulated; retransmission policy is underspecified.**  
   - Sections IV-A and IV-D explicitly state the DES uses a fluid server and does not enforce TDMA slotting or half-duplex partitioning, yet key conclusions rely on superframe margins (Table VI) and on infeasibility of intra-cycle ARQ.  
   - Required change: specify an explicit TDMA frame design including how (or whether) retransmissions are scheduled (reserved slack slots, per-slot extension, or deferred ARQ). Then recompute feasibility under that policy and ensure consistency with GE assumptions.

2. **GE model coherence assumption drives the “retransmissions ineffective” conclusion by construction.**  
   - Section IV-C states GE state is constant within each 10 s cycle; therefore all \(M_r\) retries see the same state. This makes intra-cycle ARQ ineffective in bad state regardless of airtime.  
   - Required change: add a sensitivity variant where GE transitions can occur within-cycle (or where coherence time is a parameter), and show whether conclusions about ARQ infeasibility and recovery times remain.

3. **Coordinator ingress sizing mixes three regimes (TDMA deterministic, random-phase hard deadline, token bucket) without a unifying analytic bound.**  
   - The “Model A” \(C_A\approx 50\) kbps is MC-derived; “Model B” yields 21 kbps empirically; TDMA yields 24 kbps. The reader is left without a clear rule for choosing among them.  
   - Required change: provide a clear statement of the assumed access discipline for the architecture (it appears to be TDMA), and relegate Model A/B to “if unscheduled arrivals” with a more formal bound (e.g., order-statistic + backlog bound) or a clearer explanation of why 30 kbps is the recommended point.

4. **“Topology-invariant command traffic” and “all constraints non-binding at ≥10 kbps” are overgeneralized.**  
   - Command traffic is invariant only under centralized command semantics and identical per-node information content; decentralized planning or differential addressing changes this.  
   - At ≥10 kbps, byte budget constraints may vanish, but contact/pointing/interference constraints can dominate.  
   - Required change: rephrase these as conditional statements and add a short section enumerating which constraints become dominant and how they could be incorporated.

---

## Minor Issues

1. **Figure includegraphics filename inconsistency:**  
   - Fig. \ref{fig:cross_cycle_recovery} uses `\includegraphics{fig-cross-cycle-recovery}` without an extension while others use `.pdf`. Ensure consistent figure compilation.

2. **Notation/definitions could be tightened:**  
   - Table I defines \(\eta_{\text{total}}=\eta+20.5\%\) baseline, but later “effective overhead” \(\eta_{\text{eff}}=\eta/\gamma\) appears (Table VIII). Consider adding \(\eta_{\text{total,eff}}=\eta_{\text{total}}/\gamma\) explicitly to avoid confusion.

3. **Equation references and numbering:**  
   - Some text references “Section IV-I” etc.; ensure IEEEtran section labels match final numbering. Also check internal references like “Section~IV-I” (cluster-size trade-off) vs actual subsection titles.

4. **Centralized baseline is compute-only but appears in overhead plots:**  
   - Fig. \ref{fig:overhead_scaling} includes centralized curves but admits comms not modeled. Consider visually distinguishing (different axis/marker) or removing from “overhead vs nodes” to avoid misinterpretation.

5. **Coordinator election timing at 1 kbps under Slotted ALOHA:**  
   - The computation “\(51 \times 0.8/0.36\) s” assumes 100 B messages and 0.36 throughput; clarify the mapping from throughput to completion time (collision model, offered load), since election is a bursty many-to-one response pattern.

---

## Overall Recommendation — **Major Revision**

The paper has a strong premise and several useful analytic relations, and it is plausibly within T-AES scope. However, the current version’s most operationally salient claims (coordinator PHY sizing, TDMA margin, ARQ infeasibility, and “non-binding” constraints at higher rates) depend on a split model where TDMA/half-duplex scheduling is analytic-only and loss/retransmission behavior is partly driven by GE coherence assumptions. A major revision should tighten the scheduling model, specify retransmission policy, and add sensitivity to within-cycle channel variation so that the conclusions are robust and not artifacts of modeling choices.

---

## Constructive Suggestions

1. **Add a single, explicit “access discipline specification” for the baseline architecture.**  
   State clearly: “RF-backup uses deterministic TDMA with half-duplex coordinator; no intra-cycle ARQ, only inter-cycle repetition,” *or* define how ARQ is scheduled. Then ensure all results and tables use that same discipline.

2. **Introduce a coherence-time parameter in the GE model and run a small sensitivity sweep.**  
   For example, allow 1–5 state transition opportunities within a 10 s cycle (or model per-slot GE). Report how intra-cycle success and P95 recovery change. This will make Section IV-C’s conclusions credible beyond the “state constant per cycle” assumption.

3. **Unify coordinator ingress sizing into one recommended equation with clearly scoped alternatives.**  
   If TDMA is the intended design, make Eq. \(\ref{eq:tdma_capacity}\) the primary sizing rule, and present Model A/B as “if you cannot schedule arrivals.” Provide a conservative bound (e.g., \(C_{\text{coord}}\ge \frac{(k_c-1)S_{\text{eph}}8}{T_c\gamma} \times (1+\text{margin})\)) with a justified margin.

4. **Strengthen the fairness of topology comparisons by aligning functional scope.**  
   Either (i) extend the sectorized mesh baseline to provide full within-sector coverage (cap = \(k_s-1\)) and show it exceeds budget, or (ii) rename it throughout as “local neighbor monitoring baseline” and avoid “coordination architecture” language in comparative claims.

5. **Reframe high-level claims as conditional and add a short “dominant constraints by regime” table.**  
   A compact table could list: at 1 kbps RF-backup → TDMA airtime & half-duplex dominate; at ≥10 kbps continuous scheduled links → pointing/visibility/interference dominate; at Earth occultation → DTN/contact scheduling dominates. This will prevent readers from over-interpreting message-layer results as end-to-end feasibility.

If you provide an updated Version with an explicit TDMA+retransmission policy and GE coherence sensitivity, I can re-review focusing on whether the main sizing conclusions remain stable.