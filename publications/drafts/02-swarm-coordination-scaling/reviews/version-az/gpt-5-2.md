---
paper: "02-swarm-coordination-scaling"
version: "az"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-02-27"
recommendation: "Unknown"
---

## 1. Significance & Novelty — **Rating: 4/5 (Good)**

The manuscript targets a real and timely scaling problem: coordination of autonomous spacecraft swarms in the \(10^3\)–\(10^5\) regime under severe “RF-backup” bandwidth constraints. The paper’s main value is packaging a set of closed-form sizing relationships (overhead, coordinator ingress capacity, AoI tails under exception telemetry, and GE burst-loss recovery) into a coherent design toolkit, and then verifying those closed forms with a fast Monte Carlo DES. For practitioners, the coordinator-ingress sizing and the “slot-time vs. byte-rate” distinction under TDMA are especially useful.

Novelty is moderate-to-strong in the *integration* and *byte-level accounting* across architectures at this scale. Many components are individually standard (AoI geometric tails, GE models, epidemic gossip bounds, M/D/c baselines), but the manuscript’s contribution is the end-to-end synthesis with explicit message sizes, cycle timing, and the explicit recognition that coordinator ingress is a bottleneck even when per-node budgets are low. The explicit stress-case decomposition showing commands dominate (and largely topology-independent) is a helpful insight for system designers.

That said, some novelty claims are overstated or need tightening. The statement in the Introduction that “No prior work has systematically compared…” is hard to defend without a more careful positioning against constellation operations literature (e.g., ISL scheduling, TT&C capacity planning, DTN operational concepts, and existing hierarchical control approaches). The paper would benefit from reframing novelty as: *closed-form parametric sizing equations + verified accounting tool* under a clearly defined message model and RF-backup regime, rather than implying the first systematic comparison in general.

---

## 2. Methodological Soundness — **Rating: 3/5 (Adequate)**

The methodology is internally consistent for what it claims: message-layer design equations verified by a cycle-aggregated DES. Assumptions are mostly explicit (e.g., \(T_c=10\) s, message sizes, coordinator processing times, GE coherence equal to cycle, static clustering) and the reproducibility posture is good (open-source code and tagged version). The use of per-run quantiles (Table IV-B AoI methodology footnote) is a good practice to avoid pseudo-replication from correlated samples.

However, there are several methodological fragilities that currently limit confidence in the quantitative conclusions:

1. **Coordinator ingress modeling mixes incompatible abstractions.** In Section IV-A, “Model B” token-bucket carry-over is said not to violate timeliness because tokens accumulate during idle time—not from deferred reports. But in a strict per-cycle deadline system, the feasibility is dominated by *slot time* and *arrival phasing*, not token accounting. If the coordinator can only receive during allocated slots, token carry-over does not create additional reception opportunities. The paper later correctly emphasizes TDMA slot-time feasibility (Eqs. (17)–(18)), which undercuts the earlier “21 kbps via carry-over” framing unless the physical layer truly permits continuous reception outside the cycle structure.

2. **TDMA/half-duplex assumptions are underdeveloped.** The derived \(\gamma\) in Section IV-A (\(\gamma=0.949\) from a slot breakdown) is reasonable as a *payload efficiency*, but then the manuscript conservatively adopts \(\gamma=0.85\) to cover FEC and other overheads. This is fine, yet the paper also assumes a half-duplex coordinator that must allocate 9.18 s of 10 s to ingress for \(k_c=100\). This leaves little margin for *any* additional control traffic, ranging, resync, or retransmissions. The later conclusion that intra-cycle retransmission is infeasible is plausible, but the analysis needs to be made consistent throughout: either the system is fundamentally “one attempt per member per cycle” under RF backup, or the earlier retransmission load models (e.g., \(\bar{M}_r=0.18\)) should be reinterpreted as *inter-cycle* attempts.

3. **The sectorized mesh comparator is not functionally comparable.** Section III-B(4) explicitly admits the capped sector graph is not connected and only provides ~3% “coverage.” Yet overhead comparisons are then used to argue hierarchical superiority. At minimum, the paper should separate “bandwidth cost” from “coordination utility” using a clearer metric (e.g., probability of detecting a conjunction within a sector, expected neighbor-set recall, or a graph connectivity/diameter target). As written, the sectorized mesh is both (i) not delivering the same function and (ii) penalized for that, which weakens RQ1/RQ3 claims.

Overall, the methods are appropriate for a *first-order sizing paper*, but several model couplings (TDMA time, retransmissions, and coordinator ingress) need reconciliation so the sizing equations are physically interpretable.

---

## 3. Validity & Logic — **Rating: 3/5 (Adequate)**

Many conclusions are directly supported by the manuscript’s own accounting and checks. Examples: the AoI P99 formula (Eq. (22)) matches DES (Table IV-B), the overhead constancy with \(N\) follows from Eq. (7) and the accounting tables, and the GE inter-cycle recovery curves are sensibly validated against Markov-chain calculations (Section IV-C and Fig. 7). The paper is also commendably explicit that the DES is “verification, not validation” (Section III-A, Section V-A), which appropriately bounds claims.

The main validity risk is that some headline numeric requirements (e.g., “coordinator ingress 21–25 kbps”) are presented as robust despite being sensitive to the underlying access model. In particular, the “decoupling” claim (Section IV-D) that GE losses do not increase coordinator drops depends on the DES drop model (“lost messages removed before they reach the queue”). That is true for a model where loss occurs *before* queue admission and where slot time is not the binding shared resource. But in a TDMA system, failed transmissions still consume time (which the paper acknowledges), and time scarcity can translate into effective “drops” (missed deadlines) for other members. The paper partially addresses this by distinguishing queue overflow vs. slot-time coupling, but the narrative sometimes treats the decoupling as a broad architectural principle rather than a narrow statement about *byte-queue occupancy under orthogonal links*.

Similarly, the baseline comparisons should be interpreted carefully. The centralized baseline is compute-only (M/D/c) and omits the actual dominant constraints (uplink scheduling, spectrum, contact windows). The manuscript acknowledges this (Section IV-G), but the presence of centralized curves/figures can still mislead readers into over-weighting those comparisons. If RQ3 is about “where hierarchical overhead falls relative to baselines,” then baselines should be commensurate in what is modeled (communication vs. compute), or the paper should restructure RQ3 to focus on *hierarchical vs. decentralized comms architectures* only.

---

## 4. Clarity & Structure — **Rating: 4/5 (Good)**

The paper is generally well organized, with a clear roadmap (start of Section IV), consistent notation for overhead, and a useful “Design Equations Summary” in Section V-D. Tables are detailed and helpful, especially the traffic accounting tables and the coordinator ingress model comparison (Table IV-A). The manuscript also does a good job of separating “offered vs delivered” overhead and highlighting that \(\gamma\) converts message-layer to MAC-layer utilization.

Clarity issues arise mainly where multiple abstractions are layered: token-bucket smoothing vs TDMA slot feasibility, retransmission policies (intra-cycle vs inter-cycle), and the mixed meaning of “drops” (queue overflow vs deadline misses vs link loss). For example, Section IV-A states “reports arriving after the aggregation deadline are treated as AoI-degrading misses, not drops,” but later tables report “Drops” as a metric (Table IV-D). These distinctions should be made explicit at the metric-definition level (Section III-H), otherwise readers may misinterpret results.

A smaller clarity concern is that several figures are referenced but not shown in the LaTeX excerpt (e.g., architecture figure, recovery figure). Assuming they exist in the submission, the captions are informative. Still, some key claims would benefit from a single consolidated figure/table that ties together: \(k_c\), TDMA slot duration, feasible ingress attempts per cycle, and resulting required coordinator PHY rate.

---

## 5. Ethical Compliance — **Rating: 4/5 (Good)**

The manuscript includes an explicit disclosure of AI-assisted ideation in the Acknowledgment, naming tools and clarifying that the AI exercise “motivated aspects” but is not validated here. This is a positive step and aligns with emerging disclosure norms. The paper also provides code and data availability, supporting transparency and reproducibility.

Two improvements are advisable for IEEE T-AES norms: (i) move the AI disclosure from Acknowledgment into a more formal “Author Contributions / Use of Generative AI” statement if the journal’s current policy recommends it, and (ii) clarify whether any text, figures, or code were generated by AI tools (beyond “ideation”), and whether outputs were independently verified. Also, the author block is anonymized as “Project Dyson Research Team”; that may be acceptable for review but the final version should ensure conflicts of interest and affiliations are fully disclosed.

No human/animal subject concerns are present. The open-source release is a plus.

---

## 6. Scope & Referencing — **Rating: 4/5 (Good)**

The topic is well within IEEE Transactions on Aerospace and Electronic Systems: constellation operations, autonomous coordination architectures, and comms/queueing-driven sizing. The references cover relevant distributed systems and swarm robotics foundations (Lynch, Lamport, Raft, SWIM), AoI surveys, DTN standards, and some mega-constellation networking literature (Handley, del Portillo, Bhattacherjee). The constellation operations context (Starlink/OneWeb/Kuiper) is present, though some citations are non-archival web sources; that is understandable for operational details but should be minimized where possible.

The paper would benefit from deeper engagement with: (i) satellite TT&C capacity planning and spectrum coordination literature, (ii) CCSDS cross-support / space link services work that relates to scheduling and link-layer realities, and (iii) operational conjunction assessment pipelines (screening, covariance management, tasking) to better justify the message model and the sectorized-mesh heuristic. Also, the mesh baseline uses gossip bounds from Demers et al.; there is a large literature on rumor spreading and epidemic dissemination with tighter constants and bandwidth-aware variants that could strengthen the mesh discussion.

Overall scope fit is good, but the literature positioning should be tightened to avoid overclaiming and to ground the message model in operational practice.

---

## Major Issues

1. **Inconsistency between coordinator ingress sizing (21–25 kbps) and TDMA slot-time feasibility under loss/retransmissions.**  
   - Section IV-A presents “Model B” and TDMA results suggesting 21–25 kbps suffices, but later the slot-time analysis shows that with retransmissions (and especially under GE bursts) the cycle cannot accommodate all attempts. If the intended design is “one attempt per member per cycle; inter-cycle recovery only,” then the earlier retransmission load factors and “zero-drop” language should be revised accordingly.  
   - Action: explicitly define the RF-backup MAC policy (number of attempts per member per cycle) and derive coordinator capacity and feasibility under that policy; separate *byte-rate* sizing from *slot-time* scheduling constraints in a single coherent model.

2. **Sectorized mesh baseline is not functionally comparable, undermining RQ1/RQ3 conclusions.**  
   - Section III-B(4) admits the capped sectorized mesh is not connected and only monitors ~3% of sector peers at cap=10, yet overhead comparisons are used to argue hierarchical superiority. This is an apples-to-oranges comparison unless the paper defines a common utility target.  
   - Action: either (i) redesign the sectorized mesh baseline to meet a defined connectivity/coverage/awareness target comparable to hierarchical cluster awareness, or (ii) reframe results as “cost per unit awareness” with a formal metric and avoid implying direct architectural superiority.

3. **Drop/latency/AoI semantics are not consistently defined across models.**  
   - “Drops” sometimes mean queue overflow (token bucket), sometimes deadline misses (“AoI-degrading misses”), and link loss is separate. Table IV-D reports “Drops” but it is unclear whether these are queue drops, deadline misses, or both.  
   - Action: in Section III-H, define distinct counters: link-loss, queue-drop, deadline-miss; report them separately throughout.

4. **Centralized baseline modeling is compute-only; figures/tables risk overstating cross-architecture comparisons.**  
   - The manuscript acknowledges this caveat, but still presents centralized “divergence” curves and scalability limits that may be misinterpreted as end-to-end.  
   - Action: move centralized results to a clearly labeled “compute-only reference” subsection/appendix and avoid mixing them with communication-layer overhead comparisons unless a comms model is added.

---

## Minor Issues

1. **Equation/parameter clarity:**  
   - Eq. (15) uses \((k_c-1)\) rather than \(k_c\) for TDMA capacity; earlier coordinator ingress demand uses \(k_c\). Clarify whether the coordinator itself is excluded from “members” consistently across all derivations.  
   - In Section IV-A “Fleet-wide TDMA cost is 0.28 kbps/node (1% coordinators)”—this needs a short derivation or citation; it is not obvious.

2. **GE model coherence assumption is strong and partly self-fulfilling.**  
   - Section IV-C states retransmissions are ineffective “by model construction” because the state is constant within the cycle. This is acceptable as a bound, but the paper should more explicitly label intra-cycle retry results as an artifact of the coherence assumption and provide at least one sensitivity case with sub-cycle transitions (even if approximate).

3. **Mesh workload numbers:**  
   - Table III-B(3) footnote computes 51 MB send+receive then inflates to 73 MB with 1.4× redundancy. Provide the basis for 1.4× (citation or derivation), otherwise it appears ad hoc.

4. **Citation quality:**  
   - Several key operational claims rely on non-archival sources (Kuiper overview page, DARPA program pages). Where possible, replace with filings, standards, or peer-reviewed/archival conference sources, especially for constellation scale and operational constraints.

5. **Terminology:**  
   - “Zero-drop” is used for coordinator ingress sizing, but later the system allows deadline misses treated as AoI misses. Consider renaming to “zero-queue-drop” vs “deadline-feasible” to avoid confusion.

---

## Overall Recommendation — **Major Revision**

The manuscript has strong potential and a useful set of design equations, but several core results (especially coordinator ingress sizing and the claimed decoupling under loss) need to be made internally consistent with the TDMA slot-time feasibility constraints and with clearly defined drop/miss metrics. In addition, the sectorized mesh comparator must be reframed or redesigned to be functionally comparable; otherwise, the architecture comparison conclusions are not well supported. With these revisions, the paper could become a solid, practically relevant sizing reference for large autonomous constellation coordination.

---

## Constructive Suggestions

1. **Unify the RF-backup MAC model into one explicit “feasible schedule” and re-derive coordinator sizing from it.**  
   Provide a single table that, for given \((k_c, T_c, S_{\text{eph}}, R_{\text{PHY}}, \gamma)\), computes: slot duration, number of slots available, maximum attempts per member per cycle, and resulting feasible retransmission policy. Then express \(C_{\text{coord}}\) as a consequence of this schedule rather than mixing token-bucket and TDMA arguments.

2. **Split “drops” into three reported metrics and use them consistently.**  
   Track and report separately: (i) link-loss events, (ii) queue/byte-budget drops, (iii) deadline misses (arrived after aggregation cutoff). Revisit Table IV-D and the decoupling claim using these metrics; the decoupling may hold for (ii) but not for (iii).

3. **Make the sectorized mesh comparison utility-aware.**  
   Define a measurable “awareness” target (e.g., probability a node is aware of all neighbors within screening radius, or expected fraction of relevant conjunction candidates discovered) and tune the mesh baseline to meet that target, then compare overhead. Alternatively, formalize “cost per monitored peer” and avoid implying direct replacement equivalence.

4. **Add a short sensitivity case for GE coherence shorter than \(T_c\).**  
   Even a simple variant where the GE state can transition \(m\) times per cycle (or where retries sample independent states with probability \(\epsilon\)) would let readers see how strongly the “intra-cycle retry is ineffective” conclusion depends on the coherence assumption.

5. **Tighten the claims and positioning around “verification vs validation” and baseline comparability.**  
   Consider moving centralized M/D/c to an appendix and focusing the main comparisons on architectures modeled at the same layer (hierarchical vs sectorized vs mesh). Reword novelty claims to emphasize the parametric sizing toolkit and verified accounting at scale under an explicit RF-backup regime.