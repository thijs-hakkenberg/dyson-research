---
paper: "02-swarm-coordination-scaling"
version: "cg"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-03-01"
recommendation: "Major Revision"
---

## 1. Significance & Novelty  
**Rating: 4 (Good)**  
The manuscript tackles a real and under-served problem: providing *closed-form* sizing relationships for coordination traffic and schedulability in very large autonomous swarms (10³–10⁵). The explicit separation between (i) message-layer byte budget and (ii) PHY/MAC schedulability (half-duplex TDMA airtime) is a meaningful contribution for practitioners who routinely conflate “bps budget” with “fits in a frame.” The duty-factor parameterization is also a useful bridge between stress-case sizing and operational realism.

Novelty is strongest in the *engineering synthesis*: a coherent workflow (Algorithm 1) connecting workload semantics → byte budget → MAC efficiency γ → TDMA airtime feasibility → coordinator ingress sizing, plus GE-based burst-loss recovery curves. The novelty is weaker where results mostly restate arithmetic from the assumed message model (e.g., many “scale invariance” findings are structurally implied).

---

## 2. Methodological Soundness  
**Rating: 3 (Adequate)**  
The analytical accounting is generally sound and the two additional simulators (slot-level TDMA and packet-level γ derivation) address real gaps in a cycle-aggregated DES. The explicit acknowledgement of evidence tiers is commendable and rare.

However, several methodological choices remain only partially justified: (a) the operational workload model (especially command semantics and addressing) drives the main stress-case; (b) the GE coherence assumption is pivotal to conclusions about ARQ infeasibility; (c) the TDMA superframe budget is tight (hundreds of ms margin) and sensitive to acquisition/guard assumptions that are not tied to a specific radio implementation or link acquisition concept of operations. These are not fatal, but they limit the paper’s “standards-grounded” positioning.

---

## 3. Validity & Logic  
**Rating: 3 (Adequate)**  
Internally, the paper is largely consistent and the “Layer 1 vs Layer 2” logic is helpful. The duty-factor framing appropriately contextualizes the 46% stress-case as a continuous-duty upper bound, and the revised γ baseline (0.760) is clearly presented.

Key validity concerns are: (i) inconsistent use/interpretation of γ across 24 vs 30 kbps in some feasibility narratives and tables; (ii) the DES “verification” is sometimes presented as stronger evidence than it is (you do note this, but the Results section still leans on DES agreement); (iii) some numerical claims appear to conflict (notably consensus overhead vs centralized command overhead, see Major Issue #6).

---

## 4. Clarity & Structure  
**Rating: 4 (Good)**  
The manuscript is well organized, with strong signposting, explicit notation, and a clear separation of models (DES vs slot-sim vs packet-level). The “tool scope disambiguation” is particularly helpful.

That said, the manuscript is long and occasionally repetitive (e.g., repeated restatement that DES agreement is expected). Some tables mix regimes (24 kbps vs 30 kbps; Model S vs Model C) in ways that invite misreading. A tighter “practitioner takeaway” section consolidating the design-point logic would improve readability.

---

## 5. Ethical Compliance  
**Rating: 4 (Good)**  
Open-source code/data availability is strong and specific (tagged repo, versions, runtime). AI assistance is disclosed in Acknowledgment, which is good practice.

Two improvements: (i) add a short *reproducibility checklist* style description (how to regenerate each key figure/table from the repo), and (ii) clarify whether any non-archival sources materially affect quantitative claims (e.g., Starlink ops references).

---

## 6. Scope & Referencing  
**Rating: 3 (Adequate)**  
The paper is plausibly in-scope for IEEE TAES / Adv. Space Research (coordination architectures, comms constraints, autonomy). Referencing covers distributed systems and some space networking standards.

Gaps: more direct engagement with spacecraft MAC/TDMA practice (beyond Proximity-1), and with LEO constellation operational comms constraints (contact schedules, spectrum constraints, ISL acquisition overheads). Also, several key citations are non-archival; for a top-tier journal, try to anchor critical operational claims in archival/standards sources where possible.

---

# Major Issues

1. **γ unification is not fully “consistently applied” across the paper’s feasibility reasoning (24 vs 30 kbps, Model C vs Model S).**  
   - **Why it matters:** The central design conclusion—“30 kbps minimum viable”—depends on γ. Any ambiguity in which γ applies where will undermine trust in the feasibility boundary.  
   - **Evidence:** You state “All feasibility claims use Model C,” but Table/claims mix: e.g., Table 8 uses γ\_{24}=0.760 header while Layer-2 “31 cycles” uses 30 kbps Model C; Table 7/9/10 mix Model S and Model C results; ARQ coupling result is explicitly Model S at 24 kbps. These are fine scientifically, but the reader can easily conclude the paper is inconsistent.  
   - **Remedy:** Add a single “Feasibility baseline matrix” early in Results: rows = {Model S, Model C}, cols = {24, 30 kbps}, and explicitly label which results use which cell. Also, enforce a rule: every time γ appears numerically, it must be subscripted (γ\_{24} or γ\_{30}) unless it is the functional γ(R\_{PHY}). Finally, revise any “TDMA required when …” heuristics to specify which γ and which rate.

2. **The three-layer feasibility framing (byte budget → MAC translation → TDMA airtime) needs sharper formalization: MAC translation is currently half a layer but treated like a layer in places.**  
   - **Why it matters:** Practitioners could misapply η\_{total}/γ as a sufficient schedulability test, which you explicitly say it is not. The framework is a key contribution; it must be unambiguous.  
   - **Remedy:** Rename explicitly to **two layers + one necessary condition**:  
     - Layer 1: message-layer byte budget (η, η\_{total} ≤ 1)  
     - Condition: PHY utilization estimate η\_{total}/γ (screening only)  
     - Layer 2: TDMA airtime inequalities (Eqs. 21–22)  
     Then update Table 8 headings accordingly and adjust Algorithm 1 language to avoid “Layer” wording for the utilization screening.

3. **DES “verification” still risks being perceived as circular; the paper should more clearly articulate what DES contributes beyond confirming arithmetic.**  
   - **Why it matters:** Reviewers/readers at TAES will discount simulation that re-implements the same equations unless it produces new insight. You have some (buffer tails under ON/OFF), but it is not foregrounded as the *main* DES value.  
   - **Remedy:** In Results, restructure Section IV-G so the first paragraph states: “DES is not validation of the equations; its unique contributions are (i) distributional buffer sizing under stochastic campaigns, (ii) AoI distributions under exception reporting, (iii) empirical confirmation of independence assumptions under joint parameter sweeps (if any).” Then move the “<0.1% agreement” to a short appendix/footnote or a single summary sentence.

4. **Packet-level validation of γ (Section IV-J) is helpful but still not fully “independent validation” of the end-to-end feasibility claim.**  
   - **Why it matters:** Deriving γ from CCSDS framing anchors one parameter, but the decisive feasibility boundary also depends on acquisition time, guard time, and half-duplex turnaround—all of which are partly assumed. If those are off by a few ms/slot, the 30 kbps margin can evaporate.  
   - **Remedy:** Provide a sensitivity band on *T\_{acq}* and *T\_{guard}* (and turnaround) showing the break-even rate for k\_c=100. For example: compute required R\_{PHY,min} as a function of T\_{acq} ∈ [0,10] ms and guard ∈ [3,10] ms. This would convert the “standards-grounded” claim into a robust design chart.

5. **The stress-case η\_S ≈ 46% is now better contextualized, but the workload realism still hinges on centralized command semantics that may not reflect autonomous swarms.**  
   - **Why it matters:** Your headline overhead numbers are dominated by commands (≈41 percentage points). If autonomous coordination shifts decision-making cluster-local, command traffic changes qualitatively (consensus, intent dissemination, differential updates). The paper acknowledges this, but the results section still treats η\_S as a central “bound.”  
   - **Remedy:** Add a second stress-case variant: “distributed-planning stress” with explicit message model (e.g., Raft-like or leader-based agreement + intent broadcast), and compute η and airtime feasibility for that. Even a coarse bounding case would help practitioners map the equations to non-centralized autonomy.

6. **Potential inconsistency/ambiguity in the “distributed planning” overhead numbers (η\_{consensus}).**  
   - **Why it matters:** In one place you state cluster-local Raft adds ~3.1% per decision (3,840 B), later you state η\_{consensus} ≈ 30.7%—an order-of-magnitude discrepancy. This is likely a units/cycle interpretation issue (per *decision* vs per *cycle* vs per *node*). Such inconsistencies directly undermine confidence in the accounting.  
   - **Remedy:** Audit and reconcile all consensus-overhead statements. Provide one canonical formula for η\_{consensus} analogous to η\_{cmd}, clearly specifying: payload bytes, number of rounds, quorum size, whether counted per node or per cluster, and whether it occurs every cycle or only during campaign cycles. Then ensure the 3.1% vs 30.7% discrepancy is resolved.

7. **ARQ infeasibility conclusion depends strongly on the GE coherence assumption; the mapping from physical mechanisms to (p\_{BG}, coherence) is not sufficiently supported.**  
   - **Why it matters:** The paper makes a strong claim: intra-cycle ARQ is structurally ineffective under correlated bursts. That may be true for blockage/mispointing, but the key is whether coherence ≳ T\_c and whether retransmissions are constrained by TDMA margins. Without stronger linkage, the claim may be seen as scenario-specific.  
   - **Remedy:** (i) Make the ARQ conclusion explicitly conditional in the abstract/conclusion (“for obstructions with coherence ≥ T\_c”). (ii) Add a short derivation showing the exact margin vs expected retransmission airtime, and identify the threshold coherence (in slots) where ARQ becomes feasible. Your Fig. 14 gestures at this; formalize it into a design rule.

8. **Coordinator ingress sizing equation needs to be consistently presented with γ and half-duplex partitioning.**  
   - **Why it matters:** Eq. (11) / Eq. (19) style expressions sometimes present coordinator ingress as a raw bps requirement and sometimes as PHY requirement divided by γ. Practitioners need a single canonical sizing equation: “required PHY rate” vs “required information rate.”  
   - **Remedy:** Present two explicit equations side-by-side:  
     - Information rate requirement: \(C_{\text{coord,info}} \ge (k_c-1)S_{\text{eph}}8/T_c\)  
     - PHY rate requirement under TDMA: \(R_{\text{PHY}} \ge C_{\text{coord,info}}/\gamma\) plus airtime feasibility constraints.  
     Then ensure all numeric examples state which one they compute.

---

# Minor Issues

1. **Table 8 header uses γ\_{24}=0.760 while the Layer-2 feasibility discussion uses 30 kbps Model C (γ\_{30}=0.745).** Clarify in caption or split into two tables.  
2. **In Table 14 (rate feasibility), “Slot” at 24 kbps is 115.5 ms, while earlier time-domain example gives 111.5 ms.** Reconcile (likely framing/acq/guard rounding or different assumptions).  
3. **Algorithm 1 line 7 heuristic threshold (0.50) is not justified.** Provide rationale or remove; it may be misused.  
4. **The term “MAC efficiency” for γ is slightly overloaded** (it includes PHY framing/FEC/acquisition). Consider renaming to “slot efficiency” or “airtime efficiency.”  
5. **Some non-archival references are used for key context (Starlink ops, Kuiper overview).** Where possible, add archival alternatives or clarify these are contextual only.  
6. **Clarify whether “baseline telemetry 20.5%” includes only uplink (node→coord) or also downlink components.** Several readers will assume bidirectional.  
7. **AoI section:** explicitly state whether AoI is computed per member at coordinator (uplink) only, or includes command freshness (downlink).  
8. **GE model:** you define p\_{success} under i.i.d. as \(1-(1-p)^{3}\) but later use \(1-p_B^{M_r+1}\); ensure consistent notation for “loss probability” vs “link availability.”  
9. **Coordinator processing model:** D[k\_c]/D/1 batch latency statement is plausible but should cite or briefly justify the approximation.  
10. **Typographic:** a few places use “kbps” for both info-rate and PHY-rate; consider using “kbps (info)” vs “kbps (PHY)” in key tables.

---

## Overall Recommendation  
**Recommendation:** **Major Revision**

The paper has a strong core idea and is close to publishable in a top-tier venue, but several issues must be addressed to make the main conclusions robust and unambiguous. The biggest strengths are (i) the explicit separation of byte-budget feasibility from half-duplex TDMA airtime feasibility, (ii) the introduction of duty factor \(d\) to contextualize stress workloads, and (iii) the standards-grounded derivation of γ (0.760) which materially changes the feasibility boundary and is a meaningful improvement over earlier “assumed γ” approaches.

The most critical improvements are: (1) eliminate remaining ambiguities/inconsistencies in how γ is applied across models/rates and how feasibility is concluded; (2) strengthen the “independence” of validation by adding sensitivity to acquisition/guard and by tightening the role of DES (distributional value, not equation confirmation); and (3) reconcile conflicting statements around distributed-planning/consensus overhead so that practitioners can credibly adapt the equations beyond centralized command semantics.

---

## Constructive Suggestions (ordered by impact)

1. **Add a one-page “Design-point traceability” section**: start from assumptions → compute η components → compute γ\_{24}, γ\_{30} → show Layer-2 airtime inequality → conclude 24 infeasible / 30 feasible, all in one place with consistent numbers.  
2. **Provide a sensitivity chart for R\_{PHY,min} vs (T\_{acq}, T\_{guard}, FEC rate)** for k\_c=100. This will greatly strengthen the “standards-grounded” claim.  
3. **Resolve the η\_{consensus} inconsistency** and provide a canonical alternative workload model for decentralized decision-making (even if approximate).  
4. **Refactor the feasibility framework terminology** to “two layers + necessary condition,” and revise Table 8 and Algorithm 1 accordingly.  
5. **Reframe DES results around what only DES can provide** (buffer tail risk under temporally correlated campaigns; distributional ingress sizing), and demote “DES matches equations” to a brief confirmation.  
6. **Tighten ARQ conclusions**: make them explicitly conditional on coherence ≥ T\_c and show the threshold coherence where ARQ becomes viable given margin.  
7. **Standardize units and labeling** (PHY vs info rate; γ subscripts; Model S/C flags) across all tables and captions.  
8. **Improve practitioner usability of Eq. (33) γ(R\_{PHY})** by providing a worked example for a second payload size (e.g., 64 B heartbeat) showing how γ changes with small packets (important in TDMA).  
9. **Clarify scope of baseline telemetry and bidirectionality** in η accounting, ideally with a single schematic showing what is counted where.  
10. **Strengthen archival referencing** for operational analogues and for acquisition/turnaround timing assumptions (even if only by citing typical radio datasheets or mission comms papers).

If you address the γ consistency, feasibility formalization, and workload/consensus accounting issues, the manuscript would present a compelling, practitioner-relevant sizing framework with a defensible 30 kbps “minimum viable” result under clearly stated assumptions.