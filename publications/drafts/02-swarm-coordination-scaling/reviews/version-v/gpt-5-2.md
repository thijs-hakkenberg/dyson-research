---
paper: "02-swarm-coordination-scaling"
version: "v"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-02-24"
recommendation: "Unknown"
---

## 1. Significance & Novelty — **Rating: 4/5 (Good)**

The manuscript targets a real and increasingly urgent problem: how coordination/control-plane architectures scale for very large autonomous spacecraft swarms under tight per-node control-plane budgets. The paper’s core deliverable—a workload-dependent *overhead design envelope* (roughly 5–46% protocol overhead under a 1 kbps/node budget)—is practically interpretable and is presented as an engineering sizing tool rather than a purely theoretical scaling claim. The addition of a “sectorized mesh” intermediate comparator is also a useful step beyond the typical “centralized vs. fully decentralized” dichotomy, and the explicit separation of “bounds” vs. “competitors” is a healthy framing choice (Intro, “Baseline Interpretation Note”).

That said, several “headline” results are either analytically predetermined by the traffic model (the O(1) overhead ratio under fixed-depth hierarchy and fixed message sizes) or depend heavily on parameter choices that are not tied to orbital dynamics or operational concepts of operations (CONOPS). The paper is candid about this in multiple places (e.g., Scaling Behavior section; Exception-based telemetry caveat that \(p_{\text{exc}}\) is a free parameter), which helps. Still, to claim stronger novelty for T-AES, the paper should more clearly position what is *new knowledge* versus what is *a quantified instance of a known scaling law*.

Overall, the contribution is meaningful: it provides a coherent, byte-accounted, architecture-level comparison and highlights coordinator ingest constraints and scheduling effects (random-phase vs. TDMA) that are easy to miss in closed-form treatments. With additional grounding of workload parameters and improved physical-layer/DTN integration, this could become a strong reference for early-phase constellation/super-swarm architecture sizing.

---

## 2. Methodological Soundness — **Rating: 3/5 (Adequate)**

The cycle-aggregated DES with byte-level accounting is appropriate for the paper’s stated goal: exploring control-plane offered load, queueing at coordinators, and scheduling-induced burstiness without incurring packet-level simulation cost. The manuscript is unusually explicit about what is modeled vs. abstracted (Table “Simulation Abstraction Scope”), and it provides a consistent traffic accounting definition of \(\eta\) (Table “Traffic Accounting”). The analytical cross-check (Eq. (analytical_crosscheck) and Table “Hierarchical Communication Overhead Scaling”) is a good code correctness test.

However, several aspects undermine methodological robustness for an IEEE T-AES audience:

1) **The DES appears largely deterministic given the message model**, and many results are direct consequences of the assumed message sizes and per-cycle behaviors. The paper acknowledges MC SD < 0.001% for overhead; this is fine, but it means the DES is not providing stochastic insight for overhead—only for queueing/burstiness and failure events. The manuscript should tighten the methodology narrative accordingly: emphasize where DES is essential (regional burst order statistics; coordinator drops under finite per-cycle byte budget; retransmission under loss; AoI under exception filtering), and avoid implying that DES “discovers” scaling.

2) **Coordinator capacity stress test model is nonstandard and needs clearer justification.** In Section “Coordinator Bandwidth Stress Test,” drops occur when cumulative bytes in a cycle exceed \(C_{\text{coord}}T_c/8\). This is closer to a per-cycle token bucket than a continuous-time service process. It will generally overstate burst sensitivity relative to a true constant-rate server with buffering across cycle boundaries (or understate it, depending on implementation). If you intend a strict “must be delivered within the same cycle” deadline, then the model is appropriate—but then it is a *deadline-constrained* system and should be framed as such and compared to an EDF/priority scheduler or a queue with per-message deadlines.

3) **Physical/link-layer abstraction is too strong for some quantitative claims.** You correctly label coordinator thresholds as “offered-load lower bounds,” but several conclusions (e.g., 24 kbps TDMA threshold; retransmission feasibility regimes) are sensitive to unmodeled half-duplex constraints, acquisition, pointing, and actual TDMA framing overhead. The guard-time model (\(\gamma=0.85\)) is plausible but not derived from a specific link layer standard or representative optical terminal behavior. For T-AES, you likely need either (a) a more defensible link-layer model tied to CCSDS/industry practice, or (b) a more explicit “translation layer” showing how offered load maps to RF/optical link budgets under realistic framing/ARQ.

Reproducibility is promising (code repository link), but the manuscript currently includes a “commit hash: [PENDING]” placeholder; for review readiness, you should provide an archival tag/hash and a minimal run script + config files matching key figures.

---

## 3. Validity & Logic — **Rating: 3/5 (Adequate)**

The conclusions generally follow from the defined traffic model and reported DES instrumentation. The paper is careful to distinguish delivered vs. offered load under loss (Table “Coordination Success and Overhead vs. Link Availability”), and it appropriately warns that delivered \(\eta\) decreasing under loss is not “efficiency.” The “design envelope” framing (nominal/event-driven/stress-case) is logically coherent and is likely the most useful takeaway for system architects.

The main validity concern is **parameter realism and coupling**. The dominant overhead term is “one unique 512 B command per node per cycle” (stress case). That assumption drives the 46% ceiling and, by construction, makes overhead almost invariant to cluster size and fleet size. The paper does present this as a stress-case bound, but then uses that bound as the default for many downstream analyses (coordinator capacity, link loss, etc.). If the realistic operating point is closer to Profile E or N, then coordinator bandwidth thresholds, retransmission feasibility, and AoI tradeoffs should be re-evaluated under those regimes as well, or at least summarized in a table that shows how the thresholds shift with workload.

Similarly, the exception-based telemetry model uses a Bernoulli per-cycle “exception probability” independent across nodes and time. That yields geometric inter-report times and heavy tails, which you then interpret via AoI (Table “Age of Information”). This is mathematically consistent, but operationally exceptions are likely *temporally correlated* (e.g., drag events, attitude anomalies, maneuver campaigns) and *spatially correlated* (shell/plane/environment). Correlation would materially change AoI tails and offered-load bursts. The manuscript acknowledges this as future work, but because AoI is positioned as a key “coordination quality” metric, the paper should either (i) test a correlated exception model (e.g., 2-state per-node Markov modulated reporting, or campaign-level bursts), or (ii) clearly limit the AoI conclusions to the i.i.d. exception model and avoid implying generality of the P99=400 s finding.

Finally, the sectorized mesh model’s scaling choice \(k_s=\lceil \sqrt{N}\rceil\) is presented as illustrative, but some claims (e.g., “full state for \(O(\sqrt{N})\) sector peers”) depend on this construct and on the capped 10-heartbeat rule. This is fine as a comparator, but the paper should more strongly justify why \(\sqrt{N}\) is a plausible sector size proxy for conjunction neighborhoods (which are driven by spatial density and relative motion, not by \(N\) directly).

---

## 4. Clarity & Structure — **Rating: 4/5 (Good)**

The manuscript is generally well organized, with clear definitions, consistent notation, and an unusually thorough accounting of what is included in \(\eta\). The “Baseline Interpretation Note” is particularly helpful, as is the consistent separation of baseline telemetry (20.5%) from topology-dependent overhead. Figures/tables are referenced appropriately and the narrative often anticipates misinterpretations (e.g., centralized \(c=1\) baseline as a bound, not a real design).

The abstract is dense but accurate to the manuscript’s content; however, it reads more like an executive summary of *all* results rather than a focused abstract. For T-AES, consider reducing the number of quantitative claims in the abstract and prioritizing: (i) the design envelope, (ii) coordinator capacity thresholds under scheduling, and (iii) the correlated loss/retransmission takeaway.

Some sections are repetitive or internally inconsistent in emphasis. Example: the paper states in “Coordinator Bandwidth Stress Test” that TDMA is “priority future work,” but later presents a TDMA analysis section with explicit capacity equation and a figure. This should be reconciled: either TDMA is implemented and validated (then it is not future work), or it is a partially analytical extension (then label it clearly as such and separate it from DES results).

Also, be careful with claims of “validated against Pollaczek–Khinchine for M/D/1” in the DES context: PK is for M/G/1; for M/D/1 the mean waiting time formula is a special case. Your Eq. (md1_waiting) is correct for M/D/1, but the text should be precise about which formula you validated against.

---

## 5. Ethical Compliance — **Rating: 4/5 (Good)**

The manuscript includes an explicit disclosure of AI-assisted ideation in the Acknowledgment, including the tools used and a statement that the concept is not validated in this study. This is a positive step and aligns with emerging transparency norms. There is no obvious ethical issue with the simulation study itself.

Two improvements are recommended for IEEE T-AES norms: (1) move AI-assistance disclosure to a more standard “Author Contributions / Use of AI Tools” statement if the journal provides guidance, and (2) clarify whether AI tools were used for *writing/code generation* versus *ideation only*. Right now it states “ideation exercise,” but readers may still wonder whether any text/code was generated and how it was verified.

Conflict-of-interest is not addressed. Even if none exists, an explicit COI statement is increasingly expected.

---

## 6. Scope & Referencing — **Rating: 3/5 (Adequate)**

The topic fits IEEE Transactions on Aerospace and Electronic Systems: it combines spacecraft operations architectures, inter-satellite networking implications, and coordination/control-plane scaling. The paper also engages appropriately with distributed algorithms, gossip, AoI, and DTN references. Citations are mostly relevant and reasonably up-to-date for foundational work.

Concerns:
- Several key “operational” references are non-archival webpages or fact sheets (e.g., Starlink ops, Kuiper overview, DARPA pages). These are acceptable as context, but core technical assumptions (e.g., ISL terminal counts, link availabilities, coordinator power deltas) should be supported by archival sources where possible (conference papers, journal articles, CCSDS docs, operator filings, or technical reports).
- The mesh comparator uses classic epidemic/gossip references, but the mega-constellation networking literature is broader than Handley + Del Portillo + Akyildiz. Consider adding recent work on LEO routing, topology dynamics, and control-plane design (e.g., more recent SIGCOMM/NSDI/IEEE Network papers on Starlink-like ISL routing and control).
- AoI references are appropriate, but you might cite multi-source AoI scheduling results if you want to interpret coordinator freshness under TDMA vs random-phase more rigorously.

---

## Major Issues

1. **Coordinator bandwidth stress test model needs formalization and justification.** The per-cycle byte budget drop mechanism (Section “Coordinator Bandwidth Stress Test”) is not clearly mapped to a physical or link-layer mechanism. If the intent is “all member reports must arrive within the same \(T_c\) window,” then it is a deadline-constrained system and should be modeled/justified as such. Otherwise, use a continuous-time service model (e.g., deterministic service at \(C_{\text{coord}}\) with finite buffer) and report drop probability and latency relative to deadlines.

2. **Workload realism and sensitivity are insufficient for downstream conclusions.** Many “engineering thresholds” (coordinator kbps, retransmission feasibility) are computed under the stress-case Profile S. Provide parallel results (at least summary tables) for Profiles E and N, or a parametric expression showing how thresholds scale with command rate and heartbeat policy. Without this, the practical relevance of 24/50 kbps thresholds is unclear.

3. **Exception-based telemetry and AoI analysis assume i.i.d. Bernoulli reporting; correlated exceptions could change tails materially.** Since AoI tail behavior is a highlighted insight, add at least one correlated exception model (e.g., Gilbert–Elliott-modulated reporting per node, or campaign bursts affecting a fraction of nodes) and show how P99 AoI changes at equal mean offered load.

4. **TDMA implementation status is ambiguous.** The manuscript alternately claims TDMA is implemented in DES (Contributions; Within-cycle timing model; TDMA Scheduling Analysis) and calls it “priority future work” (Coordinator Bandwidth Stress Test). Reconcile: clearly separate DES-measured TDMA results vs analytical TDMA capacity calculations.

5. **Physical-layer translation is too weak for quantitative claims about feasibility at high utilization.** You acknowledge missing transport headers and MAC overhead, but then report tight utilization regimes (e.g., 74–84% MAC-layer utilization). Add a clearer mapping from message-layer offered load to a plausible CCSDS/optical framing/ARQ overhead model, even if approximate, and propagate it through key thresholds.

---

## Minor Issues

- **Equation/terminology precision:** In Section “Centralized Ground Processing,” you mention validating against Pollaczek–Khinchine for M/D/1; PK is for M/G/1. Suggest: “validated against the standard M/D/1 mean waiting time expression (a special case of PK).”
- **Inconsistency in coordinator ingest accounting:** In several places you compute coordinator inbound as \(k_c \times 256\) B per cycle, elsewhere \((k_c-1)\times256\) B (since coordinator is also a node). Please standardize and state whether the coordinator sends its own status “to itself” or is excluded.
- **Table labeling:** Table “Mesh Traffic Accounting” mixes global-state mesh and sectorized mesh components in one table; consider splitting into two tables or visually separating more strongly to reduce confusion.
- **Claims of “validated to 10^5” vs “analytical extrapolation to 10^6”:** Fig. “latency distribution” includes a 10^6 curve; ensure the caption and main text consistently flag that only hierarchical is extrapolated and that other architectures may not extrapolate similarly.
- **Data availability:** Replace “[PENDING]” commit hash with a real hash/tag before acceptance; provide a DOI/Zenodo archive if possible.
- **Non-archival citations:** Where key numeric assumptions are used (ISL terminal counts, link availability 0.85–0.95, power levels), add archival sources or clearly label as assumptions.

---

## Overall Recommendation — **Major Revision**

The manuscript is promising and contains useful engineering framing (byte-accounted overhead envelope; coordinator scheduling/capacity effects; AoI freshness proxy; correlated loss implications). However, several central quantitative conclusions rely on modeling choices that need stronger justification and/or additional sensitivity analysis (coordinator capacity drop model, stress-case workload dominance, i.i.d. exception reporting). Clarifying what is DES-measured versus analytically derived, reconciling TDMA implementation claims, and adding at least one correlated workload/exception model would substantially improve validity and impact for IEEE T-AES.

---

## Constructive Suggestions

1. **Replace or augment the coordinator capacity model with a continuous-time queue + deadline metric.** Model coordinator ingress as a deterministic-rate server at \(C_{\text{coord}}\) with finite buffer and report (i) drop rate, (ii) latency distribution, and (iii) fraction meeting a per-message deadline \(<T_c\). This would make the 24/50 kbps thresholds much more defensible.

2. **Add a “workload-to-threshold” scaling summary.** Provide a compact formula or plot showing \(C_{\text{coord,min}}\) as a function of: command probability per node per cycle, heartbeat policy, \(k_c\), and \(T_c\), under both random-phase and TDMA. Include at least one table showing thresholds for Profiles S/E/N.

3. **Introduce correlated exception reporting and re-run AoI tails.** A minimal addition: per-node 2-state Markov (quiet/busy) reporting with matched mean \(p_{\text{exc}}\) but bursty behavior. Compare mean/P99 AoI and offered-load peaks to the i.i.d. Bernoulli model.

4. **Make the “translation layer” explicit:** add a subsection mapping message-layer offered load to physical-layer throughput under a representative framing/ARQ model (e.g., header %, FEC overhead, TDMA framing, guard times, half-duplex). Then propagate to “effective utilization” and coordinator raw kbps thresholds.

5. **Tighten novelty claims and streamline the abstract.** Recast the DES as primarily quantifying (a) scheduling-induced burstiness and coordinator capacity thresholds, (b) loss/retransmission behavior under correlated outages, and (c) AoI tradeoffs under exception filtering—while treating O(1) overhead scaling as a known analytical consequence validated by implementation. This will read as more rigorous and less over-claiming.