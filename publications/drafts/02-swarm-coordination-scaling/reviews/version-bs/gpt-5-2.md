---
paper: "02-swarm-coordination-scaling"
version: "bs"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-02-27"
recommendation: "Unknown"
---

## 1. Significance & Novelty — **Rating: 4/5 (Good)**

The manuscript tackles a practically important question for future mega-constellation and “space swarm” operations: how coordination traffic, scheduling feasibility, and recovery behavior scale from \(10^3\) to \(10^5\) nodes under a constrained per-node communications budget. The emphasis on *closed-form sizing equations* with byte-level accounting and explicit separation into feasibility layers (byte budget \(\eta\), MAC efficiency \(\gamma\), and TDMA airtime) is a meaningful contribution that could be useful to system architects early in design. The paper also makes a commendable effort to map abstract quantities (e.g., \(\gamma\), TDMA guard time, half-duplex partitioning) to plausible radio timing numbers (Table~\ref{tab:superframe}, Eq.~\ref{eq:gamma_derived}).

Novelty is strongest in (i) the explicit “design-equation” framing with parametric sizing relationships, (ii) the clear identification that command traffic dominates stress cases while topology-specific aggregation overhead is small (within the paper’s workload semantics), and (iii) the explicit schedulability distinction between broadcast commands and per-node unicast commands (Eq.~\ref{eq:unicast_stagger}, Table~\ref{tab:schedulability}). The GE burst-loss discussion and the separation between intra-cycle ARQ infeasibility and inter-cycle recovery curves are also useful.

That said, the novelty claim “no prior work provides closed-form parametric sizing relationships … across \(10^3\)–\(10^5\)” is directionally plausible but currently stated too strongly without a more careful positioning against (a) WSN clustering/aggregation sizing literature (LEACH-family and later analytical models), (b) DTN/contact-scheduled constellation networking sizing work, and (c) AoI + scheduled access literature. You cite some of these areas, but the manuscript would benefit from a sharper statement of *what is new relative to those models* (e.g., half-duplex coordinator superframe feasibility + workload semantics + scale regime).

---

## 2. Methodological Soundness — **Rating: 3/5 (Adequate)**

The approach—closed-form accounting plus a cycle-aggregated DES used primarily for consistency checks and tail statistics—is reasonable for the stated goal of *message-layer* sizing. Assumptions are generally enumerated (Table~\ref{tab:sim_params}) and the manuscript is unusually explicit about what is and is not modeled (e.g., Section~\ref{sec:validation_gap}, the “fluid-server” ingress abstraction, and the role of \(\gamma\)). The open-source code release is a strong reproducibility point, and the analytical/DES agreement in Table~\ref{tab:inflection} is a good internal consistency check.

However, several key modeling choices materially drive the results and need stronger justification and/or sensitivity:  
- **Workload semantics**: The conclusion that \(\eta_{\text{cmd}}\) is “topology-invariant” depends on a centralized command generation model and on counting “information content per node” rather than actual airtime/PHY transmissions. The paper correctly distinguishes broadcast vs unicast schedulability, but the *overhead metric* still treats a broadcast command as 512 B per node per cycle (received content) rather than 512 B transmitted once per cluster. This is defensible if \(\eta\) is intentionally “information budget,” but then it should not be used interchangeably with channel occupancy or energy usage. Right now, the manuscript sometimes compares architectures using \(\eta\) as if it were comms resource consumption; that is methodologically inconsistent unless you define separate metrics (see “Major Issues”).
- **DES abstraction**: The DES does not implement TDMA slotting, yet many conclusions hinge on TDMA airtime feasibility and half-duplex partitioning (Section~\ref{sec:coordinator_bandwidth}). You do provide an analytical TDMA budget, but the interaction of loss, retransmission, and scheduling is only partially represented (and the “decoupling” note in Section~\ref{sec:joint_interaction} underscores that). For an IEEE TAES audience, the lack of even a minimal packet/slot-level simulation for a single cluster weakens methodological robustness, especially for the most constrained regime (1 kbps budget / 24–30 kbps coordinator PHY).
- **Statistical reporting**: “30 MC replications” is fine for mean overhead (tiny variance), but for tail metrics (AoI P99, recovery P95) the manuscript should be more explicit about *what distribution is being estimated* (per-node, per-coordinator, per-time sample), and whether the bootstrap CI method is appropriate given strong temporal correlation in AoI samples (sampled every 100 s). The AoI analytic cross-check is good (Eq.~\ref{eq:aoi_analytic}), but the DES tail-estimation methodology needs tightening.

Overall, the methods are promising and mostly transparent, but the paper needs clearer metric definitions and a more defensible bridge from “message-layer bytes” to “actual comms resource use” for architecture comparisons.

---

## 3. Validity & Logic — **Rating: 3/5 (Adequate)**

Many conclusions are logically consistent *within the paper’s model*. Examples: the coordinator ingress sizing for \(k_c=100\) follows directly from \((k_c-1)S_{\text{eph}}\) per cycle; the TDMA slot accounting is coherent; the unicast staggering result (22 cycles) is a straightforward consequence of half-duplex egress time; and the AoI P99 under geometric exception reporting matches the DES (Table~\ref{tab:aoi_results}, Eq.~\ref{eq:aoi_analytic}). The manuscript is also appropriately candid that “all results are message-layer predictions” and that packet/MAC validation is future work.

The main validity risk is **metric conflation**: \(\eta\) is defined as “information content bytes per node per cycle / budget,” but the coordinator capacity and TDMA feasibility are driven by *transmitted airtime bytes*, not “received information content.” This matters most for broadcast: a single broadcast transmission consumes airtime once, but \(\eta\) counts it \(k_c\) times (as received content). Consequently, statements like “command traffic dominates the stress-case” and “\(\eta_{\text{cmd}}\) is topology-invariant” are only valid for an information-freshness/semantic budget, not for RF airtime, coordinator energy, or interference footprint. Yet the paper uses \(\eta\) to motivate TDMA requirements and to compare to the sectorized mesh. This is currently a logical inconsistency that could mislead readers about actual channel loading.

A second validity issue is the **GE intra-cycle retransmission infeasibility** conclusion. You argue intra-cycle ARQ is infeasible because expected retransmission airtime (computed from a steady-state bad fraction) exceeds margin (Section~\ref{sec:coordinator_bandwidth}). But the derivation uses an approximate 8% slot retransmission fraction; it is not fully consistent with the GE model definition (state constant per cycle) and with the half-duplex superframe structure. If the GE state is constant per cycle, then in bad cycles *most* packets fail and retransmissions are wasted; in good cycles retransmissions are rare. The expected airtime consumed by retransmissions depends on the policy (do you retransmit immediately within the same cycle? do you attempt all \(M_r\) retries?) and on whether retransmissions are scheduled as additional slots or reuse slack. The manuscript’s high-level conclusion (“don’t rely on intra-cycle ARQ in the constrained regime”) may still be right, but the supporting quantitative argument needs to be made more rigorous and aligned with the stated GE coherence assumption.

---

## 4. Clarity & Structure — **Rating: 4/5 (Good)**

The paper is generally well structured: clear RQs, explicit contributions, a consistent notation table (Table~\ref{tab:notation}), and a “roadmap” at the start of Results. The separation between analytical sizing and DES verification is also clearly communicated. Tables and figures are used effectively to summarize key points (e.g., Table~\ref{tab:superframe}, Table~\ref{tab:schedulability}, Fig.~\ref{fig:phase_stagger}, Fig.~\ref{fig:cross_cycle_recovery}). The “Design Equations Summary” section is particularly helpful for practitioners.

Several clarity improvements are still needed. First, the manuscript would benefit from **a single, unambiguous definition of \(\eta\)**: is it “bytes transmitted,” “bytes received,” or “semantic information delivered”? Currently it is described as “per-node bandwidth budget” and “information content per node per cycle,” which is nonstandard for comms sizing and invites misinterpretation. Second, some claims in the abstract are too dense and occasionally ambiguous (e.g., “Coordinator ingress requires 24 kbps … with 623 ms per-cycle margin” is specific, but depends on assumptions about guard time, \(\gamma\), and no intra-cycle ARQ; these dependencies are not visible in the abstract). Third, the centralized baseline is repeatedly labeled as a “reference bound,” but the paper then plots it against communication-layer results (Fig.~\ref{fig:overhead_scaling}); even with caveats, this can confuse readers.

Finally, there are a few places where the manuscript could be more careful about units and terminology (e.g., “1 kbps per node allocation is average throughput, not instantaneous PHY rate” is good, but then the coordinator PHY is 24 kbps—fine—yet the relationship between “budget” and “airtime” should be made explicit with a consistent model).

---

## 5. Ethical Compliance — **Rating: 4/5 (Good)**

The manuscript includes an explicit disclosure of AI-assisted ideation in the Acknowledgment, which is increasingly important and is handled transparently. There is no indication of human-subjects issues or dual-use experimentation that would trigger special ethical review requirements for this venue.

Two items to strengthen: (i) clarify whether any of the cited “Project Dyson Research Team” materials constitute prior publication or self-plagiarism risk (e.g., \cite{dyson_multimodel}), and (ii) provide a more standard conflict-of-interest statement (even if “none”) given the unusual author placeholder and project-based affiliation. IEEE TAES typically expects clear authorship and affiliation; the current “names later” note may be acceptable for review but should be flagged as requiring completion.

---

## 6. Scope & Referencing — **Rating: 4/5 (Good)**

The topic fits IEEE Transactions on Aerospace and Electronic Systems well: autonomous spacecraft operations, coordination architectures, link constraints, and resilience. The references are broadly relevant and include both space networking (Handley, Del Portillo, DTN/BPv7, CGR) and distributed systems foundations (Lynch, Raft, gossip) as well as AoI surveys and seminal papers.

A few referencing gaps stand out. The paper would benefit from:  
- More direct engagement with **scheduled-access satellite network** literature (beyond citing Proximity-1) and with **constellation MAC/ISL scheduling** work, since \(\gamma\) and TDMA feasibility are central.  
- Some **queueing/AoI under periodic updates with erasures** literature that directly matches the “cycle-based” model (AoI with Bernoulli/Markov losses and scheduled service).  
- Stronger sourcing for key operational claims (e.g., Starlink operational behavior is partly based on FCC filings and a non-archival blog; that may be acceptable as context, but core technical arguments should not rely on non-archival sources).

Also, several citations are “non-archival; accessed 2026,” which is acceptable for background but should be minimized for central claims in a TAES paper.

---

## Major Issues

1. **Metric inconsistency: \(\eta\) mixes “information received” with “channel resource consumed,” especially for broadcast.**  
   - In Section~\ref{sec:coordinator_bandwidth} (“Command dissemination model and overhead accounting”), the manuscript explicitly states \(\eta\) counts information content per node, not PHY time. Yet later, \(\eta\) is used to argue channel utilization and to compare architectures (e.g., Table~\ref{tab:bw_breakdown}, Fig.~\ref{fig:workload}, Table~\ref{tab:topology_comparison}). This is a fundamental definitional issue: broadcast consumes airtime once, but \(\eta\) counts it \(k_c\) times.  
   - Required fix: define **two separate metrics** (e.g., \(\eta_{\text{info}}\) and \(\eta_{\text{air}}\), or “semantic load” vs “airtime load”), and redo key comparisons and claims accordingly. At minimum, every place \(\eta\) is interpreted as comms resource must be revised.

2. **DES does not model the key mechanism (TDMA half-duplex scheduling) that drives the 1 kbps “design-driving” regime.**  
   - The DES uses a fluid server (Section~\ref{sec:des_architecture}) and explicitly does not enforce slot-level airtime; yet the tightest conclusions are about superframe margin (Table~\ref{tab:superframe}), ARQ infeasibility, and unicast staggering.  
   - Required fix: add at least a **single-cluster slot-level simulator** (even if simplified) to validate: (i) ingress completion under guard time and jitter, (ii) the effect of packet loss on wasted slots and effective throughput, and (iii) whether any intra-cycle retransmission policy can fit in the margin. If this is deferred, the claims about “required coordinator ingress 24 kbps” and “ARQ infeasible” should be softened and clearly labeled as purely analytical.

3. **Topology comparison fairness: sectorized mesh assumes \(\gamma=0.85\) without modeling how distributed nodes achieve that MAC efficiency.**  
   - Section~\ref{sec:topology_comparison} acknowledges this (“would require distributed TDMA coordination… adding unmodeled overhead”), but the comparison tables still present sectorized mesh overhead numbers as if achieved under the same MAC regime.  
   - Required fix: either (a) include a plausible distributed MAC overhead model for the sectorized mesh (control traffic + synchronization), or (b) present results under a more realistic \(\gamma\) range for mesh (e.g., CSMA/CA-like), while keeping hierarchical under TDMA.

4. **Centralized baseline is not commensurate and risks confusing readers.**  
   - The centralized model is compute-queue only (Section~III-B), but appears in overhead/scaling figures (Fig.~\ref{fig:overhead_scaling}) and comparison tables. Even with caveats, this invites misinterpretation.  
   - Required fix: either remove centralized from comms-overhead plots or add a minimal comms model (uplink scheduling/contact constraints) so the baseline is comparable on at least one shared axis.

---

## Minor Issues

1. **Equation/parameter consistency:**  
   - Eq.~\ref{eq:tdma_capacity} uses \((k_c-1)\) whereas later “Coordinator ingress” in the Design Equations Summary uses \(k_c\). Please standardize and explain whether the coordinator itself reports to itself.  
   - Eq.~\ref{eq:mac_efficiency} defines \(C_{\text{raw}} = C_{\text{coord}}/\gamma\); terminology is confusing (usually “raw PHY” is higher than “net payload,” so \(C_{\text{payload}}=\gamma C_{\text{PHY}}\)). Consider renaming to avoid inversion mistakes.

2. **GE retransmission airtime argument needs tightening:**  
   - In Section~\ref{sec:coordinator_bandwidth}, the “expected fraction of slots requiring retransmission” expression and the 740 ms figure should be derived more transparently and aligned with the GE model (state constant per cycle). As written, it reads like a stationary per-slot loss probability, which conflicts with per-cycle coherence.

3. **AoI sampling/CI methodology clarity:**  
   - Table~\ref{tab:aoi_results} footnote: “AoI sampled every 100 s across all coordinators.” With \(T_c=10\) s, this subsamples the process and may bias maxima/tails. Clarify whether AoI is updated every cycle internally but only sampled for storage, and whether P99 is computed from full-resolution or subsampled values.

4. **Figure file issue:**  
   - Fig.~\ref{fig:cross_cycle_recovery} includes `\includegraphics{fig-cross-cycle-recovery}` without extension; ensure consistent compilation and that the PDF/PNG exists.

5. **Capability matrix labels:**  
   - Table~\ref{tab:capability_matrix} uses columns “Mesh” and “Global” where earlier you use “Sectorized Mesh” and “Global-State Mesh.” Rename for consistency.

6. **Typographic/wording:**  
   - Several places use “\(\sim\)” heavily in running prose; consider tightening for journal style (reserve \(\sim\) for approximate numeric values).  
   - Abstract is very dense; consider reducing the number of numeric claims or grouping them by the three feasibility layers.

---

## Overall Recommendation — **Major Revision**

The manuscript has strong potential and contains useful analytical sizing results, but it currently suffers from a central definitional problem: the overhead/utilization metric \(\eta\) is not consistently tied to physical channel resource consumption, particularly under broadcast. Because many conclusions and comparisons rely on \(\eta\), this issue propagates through the results, topology comparisons, and stress-case interpretations. In addition, the most constrained regime’s key claims (TDMA schedulability, ARQ infeasibility) are not validated by a slot/packet-level model. Addressing these points would substantially strengthen technical credibility for IEEE TAES.

---

## Constructive Suggestions

1. **Split the overhead metric into “airtime load” vs “information load,” and redo the key tables/claims accordingly.**  
   Concretely: define \(\eta_{\text{air}}\) based on *bytes transmitted over the channel* per cycle (count broadcast once), and \(\eta_{\text{info}}\) based on *bytes of information delivered/received* (count broadcast per receiver). Then restate which metric is used for byte-budget feasibility, energy, and interference.

2. **Add a minimal TDMA slot-level simulator for one cluster (or one region) to validate Table~\ref{tab:superframe} and loss/retransmission interactions.**  
   You do not need a full ns-3 study to address the biggest concern: implement slot timing, half-duplex switching, guard time, and a simple erasure channel; verify ingress completion probability and effective throughput under GE bursts and under any proposed retransmission policy.

3. **Make the workload model more operationally grounded and provide sensitivity on command addressing patterns.**  
   The broadcast vs unicast distinction is excellent—extend it by adding intermediate cases (e.g., multicast to a subset, per-plane commands, or sparse individualized commands). Show how the “22-cycle” result changes with fraction individualized.

4. **Improve fairness of topology comparisons by modeling MAC control overhead for the sectorized mesh (or by using different \(\gamma\) values per architecture).**  
   If hierarchical assumes coordinator-assigned TDMA (\(\gamma\approx0.85\)), the sectorized mesh should either (a) include distributed synchronization/control overhead to reach similar \(\gamma\), or (b) be evaluated under a contention MAC efficiency range with explicit impact on feasibility.

5. **Tighten the GE analysis to be internally consistent with the “state constant within a cycle” assumption.**  
   Provide a clear derivation of inter-cycle recovery (good), but also clarify what intra-cycle ARQ means under your GE coherence model (it will almost never help in bad cycles). If you keep the “ARQ infeasible due to margin” claim, support it with a policy-specific airtime budget and (ideally) the slot-level validation above.