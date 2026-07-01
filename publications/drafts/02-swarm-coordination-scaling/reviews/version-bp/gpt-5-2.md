---
paper: "02-swarm-coordination-scaling"
version: "bp"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-02-27"
recommendation: "Unknown"
---

## 1. Significance & Novelty — **Rating: 4/5 (Good)**

The manuscript targets a real and increasingly important problem: coordination architectures for very large autonomous spacecraft fleets in the \(10^3\)–\(10^5\) regime under tight per-node communications budgets. The framing around “design equations” and parametric sizing is valuable for practitioners, and the explicit separation into three feasibility layers—(i) byte budget \(\eta\), (ii) MAC efficiency \(\gamma\), and (iii) TDMA airtime schedulability—provides a helpful conceptual scaffold that is often missing in swarm/constellation coordination papers.

The most novel element is the attempt to provide *closed-form* sizing relationships with byte-level accounting and to connect those to schedulability constraints (e.g., broadcast vs unicast command feasibility, coordinator ingress sizing, and the superframe time budget in Table~\ref{tab:superframe}). The paper also usefully distinguishes topology-dependent overhead (\(\eta_0\)) from workload-dependent overhead (\(\eta_{\text{cmd}}\)), which is a practical decomposition for early-phase architecture trades.

That said, the novelty claim is somewhat overstated in places because the core results depend heavily on a particular message/workload model and on a message-layer abstraction that explicitly excludes several effects that often dominate in space networks (visibility/contact schedules, pointing/acquisition overhead, interference, distributed MAC overhead for non-hierarchical baselines). As written, the paper’s main contribution is best characterized as a *message-layer sizing framework* for a specific hierarchical coordination design point, rather than a broadly general sizing theory for “autonomous space swarms.”

---

## 2. Methodological Soundness — **Rating: 3/5 (Adequate)**

The combination of closed-form accounting plus a cycle-aggregated DES used primarily as a consistency check is reasonable for the stated goal (message-layer sizing). Key assumptions are generally stated (e.g., fixed \(T_c\), fixed message sizes, per-node average budget, GE coherence constant within cycle). The manuscript is also commendably reproducible: code and tag are provided, and parameter tables are detailed (Table~\ref{tab:sim_params}).

However, there are methodological mismatches that weaken robustness. The DES uses a *fluid-server ingress* with drop-tail buffering (Section III-A) while the main feasibility bottleneck is later argued to be *TDMA airtime under half-duplex* (Section IV-A, Eqns. \ref{eq:ingress_feasibility}–\ref{eq:egress_feasibility}). This split is acknowledged, but it means the simulation cannot validate the most critical “layer 3” claim (schedulability) and cannot capture coupling between loss, retransmissions, and airtime consumption. The manuscript partially compensates with analytical checks, but then the DES “joint interaction” conclusion (Section IV-D / Table~\ref{tab:joint_interaction}) is not actually about the true TDMA system; it is about a different queueing abstraction where losses do not consume time.

Statistically, the Monte Carlo approach is fine for estimating means/tails at the message layer, but some tail claims (AoI P99, GE recovery P95) are essentially deterministic under the chosen models. In particular, AoI under exception reporting is analytically geometric and independent across nodes; the DES adds little beyond confirming implementation. Conversely, for the GE recovery, the per-cycle coherence assumption makes intra-cycle ARQ ineffective “by construction” (Section IV-C), which is acceptable as a conservative bound, but then the paper should more clearly position GE results as *conditional on coherence \(\ge T_c\)* and provide at least one sensitivity case where coherence is shorter than \(T_c\) (even analytically) to show how quickly conclusions change.

---

## 3. Validity & Logic — **Rating: 3/5 (Adequate)**

Many conclusions are supported *within the paper’s model*: e.g., coordinator ingress sizing around \(\sim 20\)–\(30\) kbps for \(k_c=100\) given 256 B reports every 10 s; the broadcast vs unicast command airtime infeasibility at 24 kbps; and the decomposition \(\eta=\eta_0+\eta_{\text{cmd}}\) with \(\eta_0\) dominated by heartbeats at the chosen parameters. The explicit superframe budget (Table~\ref{tab:superframe}) is a strong piece of engineering logic.

The main validity concern is that the manuscript sometimes generalizes beyond what the model supports. For example, the abstract and conclusions suggest that “at \(\ge 10\) kbps per node all message-layer constraints are non-binding,” but this depends on coordinator PHY scaling proportionally, perfect scheduling, and no additional constraints from pointing/acquisition, visibility, or interference—precisely the factors that often become binding at higher rates and tighter beams. The paper does mention these as unmodeled, but the narrative still reads like a broad feasibility claim rather than a conditional one.

A second logic issue is the repeated assertion that stress-case command traffic is “topology-invariant.” It is invariant only under the assumed semantics (centralized command generation and identical per-node command volume regardless of topology). In decentralized/hybrid architectures, command traffic can change drastically due to local decision-making, compression/aggregation, differential addressing, or “policy broadcast + local optimization” schemes. The paper notes this briefly, but because “topology-invariant” is a headline result, it should be more carefully qualified and possibly reframed as: *given per-node individualized control authority remains centralized, command payload dominates and does not benefit from hierarchical aggregation*.

---

## 4. Clarity & Structure — **Rating: 4/5 (Good)**

The manuscript is generally well organized, with clear sectioning and a consistent set of symbols (Table~\ref{tab:notation}). The “three feasibility layers” framing is easy to follow and helps connect byte accounting to MAC and schedulability. Tables are mostly effective, especially Table~\ref{tab:superframe}, Table~\ref{tab:schedulability}, and the breakdown tables that clarify what is and is not included in \(\eta\).

There are, however, several places where clarity suffers due to mixed abstractions. The reader must track when results are message-layer throughput, when they are airtime/half-duplex feasibility, and when they are compute/queue bounds (centralized baseline). For example, Table~\ref{tab:joint_interaction} can be misread as validating TDMA behavior under GE losses, but it explicitly does not. Similarly, Table~\ref{tab:bandwidth_scaling} lists AoI P99 constant across bandwidth regimes, which is true under the exception model, but may mislead readers into thinking AoI is generally bandwidth-independent.

The abstract is information-dense and accurately reflects many numerical results, but it is arguably overpacked for IEEE T-AES and mixes too many findings (byte budget, MAC, TDMA, coordinator ingress, AoI, GE recovery, tool verification) without a clear hierarchy. Consider prioritizing 2–3 key quantitative takeaways and moving the rest to the introduction/conclusion.

---

## 5. Ethical Compliance — **Rating: 4/5 (Good)**

The manuscript includes an explicit AI-assistance disclosure in the Acknowledgment (“AI-assisted ideation exercise…”), which is appropriate and increasingly important. The disclosure is reasonably scoped (ideation, not validation), and the paper provides open-source code and data, supporting transparency and reproducibility.

Two improvements are recommended. First, IEEE and many journals increasingly expect an explicit statement of what AI tools were used for (e.g., text editing vs. technical derivations vs. code) and confirmation that authors verified technical correctness; the current disclosure is brief and could be expanded slightly to avoid ambiguity. Second, because the author list is anonymized as “Project Dyson Research Team,” the final version should ensure compliance with IEEE authorship and affiliation policies, and should include any potential conflicts of interest (e.g., if the project is affiliated with a commercial constellation effort).

No human/animal subject issues arise, and the work is primarily analytical/simulation-based.

---

## 6. Scope & Referencing — **Rating: 4/5 (Good)**

The topic is within scope for IEEE Transactions on Aerospace and Electronic Systems: autonomous spacecraft operations, coordination architectures, comms constraints, and resilience. The references span constellation operations, DTN/space networking, distributed algorithms, and AoI literature. Including CCSDS standards and Proximity-1 is a plus for grounding assumptions.

That said, several citations are non-archival or web sources (e.g., Kuiper overview, DARPA pages). While acceptable in moderation, key claims (e.g., operational practices, constellation management constraints) should lean more on archival/peer-reviewed sources where possible. Also, the paper’s MAC-layer discussion would benefit from citing relevant satellite TDMA/return-link standards and/or recent LEO ISL MAC studies (beyond Proximity-1, which is not representative of modern LEO swarm intra-formation links). Similarly, for AoI and scheduling, there is a rich body of work on AoI under scheduled access and broadcast that could strengthen the mapping from AoI metrics to coordination requirements.

Finally, the “centralized baseline” is a compute-queue model; if kept, it should cite relevant ground segment scheduling/contact constraints literature or else be more explicitly labeled as a limited illustrative bound.

---

## Major Issues

1. **Simulation does not validate the binding constraint (TDMA airtime under half-duplex).**  
   The DES uses a fluid-server ingress and does not enforce TDMA slotting or half-duplex partitioning (Section III-A; reiterated in Section IV-D). Yet the paper’s key feasibility claims (e.g., ARQ infeasibility, unicast staggering, margin exhaustion under retransmissions) are airtime-based. This is not fatal, but it requires either (i) adding a minimal packet/slot-level simulator for a single cluster to validate airtime feasibility under loss and control overhead, or (ii) sharply reframing DES results as *only* message-layer throughput checks and moving all airtime claims to a purely analytical section with clearer assumptions.

2. **The “independence/decoupling” conclusion in Section IV-D is potentially misleading.**  
   Table~\ref{tab:joint_interaction} shows identical drops for “No Loss” and “GE Only” because the model drops losses before queueing. In a TDMA system, losses consume airtime and can increase deadline misses and reduce effective throughput, coupling loss and schedulability. The paper acknowledges this, but the section headline and takeaway still risk overclaiming. This should be rewritten to avoid implying real-system independence.

3. **Command traffic “topology-invariant” claim needs stronger qualification and/or alternative architectures.**  
   The manuscript’s central conclusion that commands dominate stress-case and are topology-invariant holds only under centralized command generation with fixed per-node command sizes. If the paper aims to provide design equations for “hierarchical coordination,” it should at least discuss (preferably model) one alternative: e.g., policy broadcast + local optimization, cluster-level command compression, or differential updates. Otherwise, the main “topology doesn’t matter for commands” message may be interpreted too broadly.

4. **GE coherence assumption (state constant for \(T_c\)) is a strong modeling choice that drives ARQ conclusions.**  
   Section IV-C is transparent that this makes intra-cycle retransmissions ineffective by construction. Still, the paper should include a sensitivity analysis to coherence time relative to \(T_c\) (even a simple extension: GE transitions at sub-cycle granularity) to show when intra-cycle ARQ becomes feasible and how it affects the superframe margin in Table~\ref{tab:superframe}.

5. **Centralized baseline is not commensurate with other architectures for overhead comparison.**  
   The manuscript repeatedly warns about this, but the centralized model still appears in several comparative figures/tables (e.g., Fig.~\ref{fig:overhead_scaling}, Table~\ref{tab:topology_comparison}) and can be misread as a fair baseline. Consider either (i) adding a minimal comms model for centralized (uplink scheduling + spectrum budget) or (ii) moving centralized to a separate “context” figure and keeping quantitative comparisons among architectures that share the same comms-layer model.

---

## Minor Issues

1. **Equation/parameter consistency:**  
   - Eq.~\ref{eq:unicast_stagger} uses \(1-\alpha_{\text{RX}}\approx 0.8\), but Table~\ref{tab:superframe} implies the egress window is \(\approx 0.82\) s and net margin \(\approx 0.62\) s after fixed overhead. Consider defining \(\alpha_{\text{RX}}\) precisely (gross ingress fraction vs net after fixed control) and using one consistent value throughout.

2. **\(\eta_0\) dominated by heartbeats may be double-counted conceptually.**  
   In several places \(\eta_0\) is described as topology-dependent, but heartbeats “each node sends and receives one per cycle” is arguably a coordination *policy* rather than topology necessity. If heartbeats are only needed for coordinator-based membership (SWIM-like), say so explicitly; otherwise readers may interpret \(\eta_0\) as inherent to hierarchy.

3. **AoI interpretation:**  
   Section IV-B ties AoI P99 (441 s) to conjunction response windows. This is plausible context, but it risks conflating “freshness of coordination state at coordinator” with “orbit knowledge quality.” Consider adding one sentence emphasizing that orbit error growth can be nonlinear and mission-dependent; the current wording may appear too reassuring.

4. **Sectorized mesh comparator fairness:**  
   The manuscript correctly notes that sectorized mesh lacks a coordinator for TDMA and may not achieve \(\gamma=0.85\) without extra overhead. This is important; consider quantifying a plausible distributed TDMA control overhead or explicitly evaluating sectorized mesh at a lower \(\gamma\) range to avoid an optimistic comparison.

5. **Figure file naming / LaTeX:**  
   Fig.~\ref{fig:cross_cycle_recovery} includes `\includegraphics{fig-cross-cycle-recovery}` without an extension, while others include `.pdf`. Ensure consistent figure inclusion to avoid compilation issues.

6. **Reference quality:**  
   Several key operational claims cite non-archival sources (e.g., Kuiper overview page). Where feasible, replace or supplement with regulatory filings, technical papers, or standards documents.

---

## Overall Recommendation — **Major Revision**

The manuscript has strong potential and contains useful engineering-style sizing equations and a clear feasibility-layer framework. However, the current version’s main bottleneck conclusions hinge on TDMA airtime/half-duplex schedulability and correlated-loss behavior that are not validated by the DES (and in places the DES results could be misinterpreted as validating them). A major revision should (i) align simulation with the binding airtime model or (ii) re-scope claims and restructure results to avoid overreach, while strengthening sensitivity analyses around coherence time, scheduling overhead, and baseline fairness.

---

## Constructive Suggestions

1. **Add a minimal slot-level TDMA/half-duplex simulator for a single cluster (even if only \(k_c=100\)).**  
   This would directly validate Table~\ref{tab:superframe}, Eqns. \ref{eq:ingress_feasibility}–\ref{eq:egress_feasibility}, and the retransmission margin exhaustion claim under GE/i.i.d. losses. It can be lightweight (no orbital dynamics), but should model: slot consumption on loss, guard times, turnarounds, and at least one control channel element.

2. **Reframe Section IV-D to avoid implying real-system independence of loss and congestion.**  
   Rename it to something like “Independence under the fluid-server abstraction” and add a companion analytical paragraph for TDMA showing the coupling mechanism (loss \(\rightarrow\) airtime consumption \(\rightarrow\) deadline misses) to prevent misinterpretation.

3. **Provide a coherence-time sensitivity for the GE model.**  
   Keep the per-cycle coherence case as a conservative bound, but add one additional case (e.g., GE transitions every slot or every 1 s) and show how intra-cycle ARQ effectiveness and required margin change. This would materially strengthen Section IV-C and the design guidance.

4. **Strengthen the “command topology-invariance” discussion with at least one alternative command semantics.**  
   Even a simple analytical variant—e.g., “policy broadcast (512 B) + local solve” vs “per-node unicast (512 B each)”—would clarify when hierarchy helps and when it cannot. This would also make Table~\ref{tab:schedulability} more actionable.

5. **Make baseline comparisons commensurate or visually separated.**  
   Either (i) add a minimal centralized comms-layer budget (uplink spectrum/time-on-contact) so “centralized” appears on the same \(\eta\) axis, or (ii) move centralized compute-only results to a separate figure/appendix and keep quantitative overhead comparisons among architectures evaluated under the same comms abstraction (hierarchical vs sectorized mesh vs global mesh bound).