---
paper: "02-swarm-coordination-scaling"
version: "al"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-02-27"
recommendation: "Unknown"
---

## 1. Significance & Novelty — **Rating: 4/5 (Good)**

The manuscript addresses an important and timely problem: how coordination/control-plane communication scales for very large autonomous spacecraft swarms (10³–10⁵, with discussion toward 10⁶). The focus on a *control-plane budget* (1 kbps/node) and explicit byte accounting is valuable, particularly because many “swarm” papers stay at algorithmic complexity or small-N demonstrations, and many mega-constellation networking papers focus on data-plane routing rather than autonomy-oriented coordination workloads. The paper’s emphasis on the RF-backup/safe-mode regime is also a credible engineering framing that differentiates it from “optical links make everything free” narratives.

Novelty is strongest in (i) the structured workload accounting tied to a fixed per-node budget, (ii) the coordinator ingress sizing analysis (21–50 kbps) with multiple scheduling models (deadline vs token-bucket vs TDMA), and (iii) the explicit statement and DES verification of “compositionality” (independence) under point-to-point ISLs (Section IV-D). The AoI framing (Section IV-B) is not new per se, but its use as a coordination-quality metric in this specific hierarchical-swarm setting is a meaningful contribution, especially with the clear geometric-tail cross-check (Eq. 33).

That said, some claims of novelty are overstated in the Introduction/Abstract (“no prior work has systematically compared… using quantitative simulation with explicit byte-level traffic accounting…”). There is adjacent literature in constellation operations, DTN/control-plane design, and distributed estimation that could partially overlap; the paper would benefit from tightening the novelty statement to “to the authors’ knowledge, no prior work has combined *these specific elements* (10⁴–10⁵, byte-level control-plane accounting, hierarchical vs baselines, RF-safe-mode budget) in one reproducible study.”

---

## 2. Methodological Soundness — **Rating: 3/5 (Adequate)**

The cycle-aggregated DES is a reasonable methodological choice given the research questions: you are not trying to resolve PHY/MAC waveforms but to quantify message-layer offered load, queueing, and staleness under workload models. The manuscript is unusually careful in providing analytical cross-checks (e.g., M/D/1, AoI geometric tail, retransmission success under Bernoulli and GE), and the traffic accounting tables (Tables 3–5, 10–11) make the offered-load model auditable. The stated code/data availability is a strong reproducibility point for T-AES.

However, key modeling assumptions materially drive results and are not always sufficiently justified *as representing spacecraft coordination*. The largest issue is the **workload model**: the stress-case assumes one 512 B command per node per 10 s cycle fleet-wide, which dominates η (as you acknowledge). That is fine as a bound, but several other message types (heartbeats, acknowledgments, elections, summaries) are “protocol overhead” and should be tied to a more explicit protocol specification (even if abstract). For example, “Heartbeats/ACK 64 B bidirectional per member per cycle” is a large contribution (~5%); it is not obvious this must be per-cycle rather than slower (e.g., SWIM-style failure detection intervals, adaptive heartbeat rates). Similarly, assuming deterministic per-cycle reports (except in exception mode) is a strong choice; many real systems use adaptive reporting based on dynamics and link state.

The **queueing/latency model** needs clarification and likely revision. You model coordinator processing as deterministic 5 ms per message (Table 7) and service rates (μc=200 msg/s), but then Table 19 reports *mean coordinator queueing 325 ms*, which is unexpectedly large at the stated utilization (ρ≈0.05 for kc=100). This suggests either (a) burst arrivals without intra-cycle service smoothing, (b) service only at cycle boundaries, or (c) a modeling artifact of the cycle-aggregated approach. As written, the latency decomposition could be internally inconsistent with the M/D/1 intuition. Since latency is used to motivate cluster-size choices (Section IV-I), this needs a more explicit description of the coordinator service discipline within a cycle (continuous service vs “batch at end of cycle”), and ideally a validation that the queueing delay behavior matches an analytically expected model under the assumed arrival process.

Finally, the Monte Carlo framework is somewhat performative: you correctly note SD < 0.001% for overhead because the model is nearly deterministic. That is fine, but then the paper should avoid implying strong statistical inference from 30 runs; instead, emphasize determinism and use MC primarily for stochastic components (failures, GE state, random phases). Consider reducing emphasis on bootstrap CIs for metrics that are deterministic functions of the workload.

---

## 3. Validity & Logic — **Rating: 3/5 (Adequate)**

Many conclusions are logically supported *within the stated abstraction*. The coordinator ingress sizing result is well argued: average demand is 20.5 kbps for kc=100; the “50 kbps” bound is explicitly tied to the strict deadline/burstiness model; and TDMA feasibility is checked with a concrete timing budget (Section IV-A). The AoI P99 result at p_exc=0.1 is exactly consistent with Eq. (33), and the manuscript is appropriately cautious in interpreting AoI-to-conjunction implications (Section IV-B).

The “independence/compositionality” result (Section IV-D) is plausible given your event ordering (loss before coordinator ingress) and point-to-point links. You do a good job stating the conditionality: it would not hold under shared-medium contention. That said, the way Table 16 is interpreted could be tightened: retransmissions *do* increase offered load on the member-to-coordinator links and can violate the per-node 1 kbps budget (as you discuss elsewhere); they simply don’t increase *coordinator ingress drops* under your pipeline ordering. This distinction should be made more explicit to avoid a reader concluding that retransmissions are “free” in the system.

Two validity concerns remain. First, the **baseline comparisons** risk being misleading despite the “intentional bounds” note. You later introduce a “realistic centralized baseline (c=N/kc)” (Section IV-H), but earlier sections and figures (e.g., Fig. 16 caption, Table 20) still foreground the single-server centralized bound and global-state mesh upper bound. This is acceptable if clearly framed as bounds, but the narrative sometimes mixes “baseline” with “reference limit,” which could confuse readers about what is being compared and why.

Second, several numerical statements feel under-supported or inconsistent: e.g., the abstract claims “exception-based telemetry at 10% reporting yields P99 AoI of 440 s,” which is correct, but it also implies this is a coordination-quality result under the overall protocol overhead budget; yet under p_exc=0.1 you also reduce overhead dramatically (η≈5%). In reality, exception telemetry should also reduce baseline telemetry (which you exclude from η), so the *total* channel utilization change is larger than is reflected by η alone. You discuss this later, but the abstract’s compactness makes it easy to misread. Consider explicitly stating whether baseline telemetry is also exception-filtered in that experiment (your DES cycle mechanics suggest yes, but your η definition excludes baseline telemetry, which complicates interpretation).

---

## 4. Clarity & Structure — **Rating: 4/5 (Good)**

The paper is generally well structured and unusually explicit about definitions (η, offered vs delivered, baseline telemetry vs protocol overhead, scheduling models, etc.). The “design equations summary” in Discussion is helpful, and the repeated analytical cross-checks strengthen reader confidence. Tables are mostly clear and tie back to parameter definitions (Table 7 is especially useful). The scope/abstraction table (Table 8) is also a good practice for simulation papers.

The main clarity weakness is that the manuscript is *very dense* and occasionally repeats itself (e.g., multiple places restate that optical makes overhead negligible; multiple places explain that η excludes baseline telemetry). Some consolidation would improve readability. Also, some sections refer to figures/tables that are not visible in the LaTeX excerpt (e.g., Fig. 1, 9, 10, etc.); assuming they exist, ensure captions are self-contained and axes/units are explicit (especially for η vs N plots and latency distributions).

Several points need clearer exposition to avoid confusion:
- The centralized baseline interpretation note says centralized uses c=1, but later Section IV-H emphasizes c=N/kc as “realistic.” This should be reconciled earlier (perhaps by consistently calling c=1 the “processing bound” and c=N/kc the “provisioned baseline”).
- The latency modeling/service discipline (as noted above) needs a clearer description in Section III-A/III-B and in the latency tables.
- The relationship between “1 kbps per-node budget” and “coordinator pooling/TDMA” is conceptually important; you explain it, but the narrative could benefit from a concise schematic of time-slot pooling and what hardware capability is required on *all* nodes (since coordinators rotate).

---

## 5. Ethical Compliance — **Rating: 4/5 (Good)**

The manuscript includes an explicit disclosure of AI-assisted ideation in the Acknowledgment and clearly states that the “Shepherd/Flock” concept is not validated in this study. This is consistent with emerging norms on transparency. The paper does not appear to involve human subjects, sensitive data, or dual-use claims beyond generic military program references.

Two improvements would strengthen ethical compliance for IEEE T-AES norms:
1. Add a short statement clarifying that AI tools were not used to generate results/code/figures (if true), only for ideation, and that authors verified all technical content. Right now, the disclosure is honest but could leave ambiguity about whether AI contributed to manuscript text or analysis.
2. Consider conflict-of-interest clarity: “Project Dyson Research Team” with a project website is fine, but if the project has commercial goals, an explicit COI statement (even “none”) is helpful.

---

## 6. Scope & Referencing — **Rating: 4/5 (Good)**

The topic is appropriate for IEEE Transactions on Aerospace and Electronic Systems: it sits at the intersection of space systems architecture, autonomous constellation operations, and communication/control-plane scaling. The paper also bridges to distributed systems and queueing theory in a way that is relevant to aerospace implementations.

References are generally relevant and include core works in distributed algorithms (Lynch), gossip (Demers), AoI surveys, CCSDS Proximity-1 and BPv7, constellation networking (Handley, del Portillo), and constellation ops/conjunction context (Flohrer/Krag/Lemmens). The inclusion of SMAD and Vallado is appropriate for the engineering audience.

Gaps: the paper would benefit from citing more directly related work on (i) hierarchical/federated constellation autonomy and onboard planning, (ii) control-plane design for large constellations (even if proprietary, there are some academic treatments), and (iii) DTN/custody transfer implications for control loops (you cite Cerf/BPv7 but do not connect to control-plane timeliness constraints). Also, some sources are non-archival (Amazon Kuiper overview, DARPA webpages, McDowell blog). Those are acceptable as context but should not be load-bearing for key claims (e.g., Starlink ops scale, optical availability). Where possible, replace or supplement with archival/peer-reviewed or official filings (FCC/ITU) that are stable.

---

## Major Issues

1. **Latency/queueing model appears internally inconsistent and under-specified.**  
   - Table 19 reports coordinator queueing delays (~325 ms mean) that do not align with the stated service rate (μc=200 msg/s, deterministic 5 ms/message) and low utilization at kc=100. This suggests the DES may be batching service at cycle boundaries or imposing an artificial gating mechanism.  
   - Required revision: explicitly define the coordinator service discipline within each cycle (continuous service vs end-of-cycle batch), show the implied queueing model, and validate latency statistics against an analytical expectation under the same discipline. If the cycle-aggregated approach induces artifacts, quantify them and bound their effect on conclusions about cluster size and end-to-end latency.

2. **Workload/protocol specification is not sufficiently grounded to justify several dominant overhead terms.**  
   - Heartbeats/ACKs “64 B bidirectional per member per cycle” and “512 B command per node per cycle” dominate η, yet the protocol rationale (why per-cycle, why these sizes, why bidirectional at that rate) is not derived from a concrete coordination function or existing standard.  
   - Required revision: provide a concise “protocol sketch” (message types, rates, triggers, timers) and justify timer choices (e.g., SWIM failure detection interval vs 10 s cycle). Include sensitivity results for heartbeat interval and command rate beyond the three workload profiles, since these drive the headline envelope.

3. **Baseline framing risks misinterpretation (bounds vs realistic comparators).**  
   - The paper oscillates between “centralized baseline c=1” (intentional bound) and “realistic centralized baseline c=N/kc,” and between “global-state mesh upper bound” and “sectorized mesh realistic comparator.”  
   - Required revision: restructure the baseline section so that the realistic baseline is primary and bounds are clearly labeled as such throughout figures/tables/captions. Ensure plots do not visually privilege the strawman baselines without clear labeling.

4. **Interaction of retransmission traffic with the 1 kbps/node budget is not consistently handled in the “independence” discussion.**  
   - Section IV-D correctly states retransmissions do not increase coordinator drops under point-to-point loss-before-ingress ordering, but retransmissions *do* increase offered load and can violate per-node budgets (as Table 23 suggests when combined with baseline telemetry).  
   - Required revision: explicitly distinguish “coordinator ingress saturation” from “member link budget saturation,” and report both constraints in the joint sweeps.

---

## Minor Issues

- **Equation/notation clarity:**  
  - Eq. (5) \(M_{\text{total}} = N + N/k_c + N/(k_ck_r)\) is described as “uplink reporting only,” but later overhead includes bidirectional commands/heartbeats; consider avoiding reusing “message complexity” without specifying direction and message class.  
  - Eq. (12) \(T_{\text{converge}} = D \tau_{\text{gossip}}\): the stated \(D=O(N^{1/3})\) for a “random geometric graph in 3D orbital space” is not obviously applicable to a LEO shell (approximately 2D manifold). Clarify geometry assumptions.

- **Coordinator handoff transfer time arithmetic:**  
  - In the handoff definition: “10–50 MB at 1 Gbps completes in 80–400 ms” is correct for raw serialization, but earlier you mention “1–10 seconds” for handoff completion (Section III-B). Reconcile these numbers (e.g., include protocol overhead, pointing/acquisition, verification, election time).

- **Table 23 footnote labeling:**  
  - In Table 23, footnote markers appear inconsistent: the table references \textsuperscript{b} and \textsuperscript{c} but the footnote text labels don’t match cleanly (there is a “\textsuperscript{c} Total offered including baseline exceeds 100% …” but the table marks are \textsuperscript{b} on offered values). Fix to avoid confusion.

- **Non-archival citations:**  
  - Several web sources are fine for context but should not be used for quantitative claims without archival support. Where you cite “Starlink v2 optical availability >99%,” consider adding a more stable reference or qualify as an assumption.

- **Monte Carlo description:**  
  - Since many metrics are nearly deterministic, consider stating explicitly which metrics exhibit meaningful variance and for which the 30-run CI is informative (failures/availability, GE burst outcomes), versus those that are essentially fixed by accounting.

---

## Overall Recommendation — **Major Revision**

The paper has strong potential and contains several valuable, publishable insights (coordinator ingress sizing under burstiness/scheduling; AoI tail behavior under exception telemetry; GE vs i.i.d. retransmission effectiveness; careful byte-level accounting). However, substantial revision is needed to (i) clarify and validate the latency/queueing model (currently potentially inconsistent), (ii) ground the dominant workload/protocol assumptions with a clearer protocol sketch and sensitivity, and (iii) present baselines in a way that avoids strawman interpretations. Addressing these points would significantly strengthen methodological credibility and the practical interpretability of the results for T-AES readers.

---

## Constructive Suggestions

1. **Add a “Protocol & Timers” subsection (1–1.5 pages) with a concrete coordination protocol sketch.**  
   Include heartbeat interval, failure detection timeout, command triggers, acknowledgment semantics, and whether heartbeats are piggybacked. Then rerun η sensitivity to heartbeat interval (e.g., 1×, 2×, 6×, 12× cycles) and show how much of η is actually mandatory.

2. **Fix/clarify the coordinator service discipline and re-validate latency.**  
   Provide pseudocode for within-cycle processing (continuous vs batch), then compare DES latency to an analytical queueing model consistent with that discipline (e.g., periodic batch arrivals into a deterministic server, or M/D/1 with superposed periodic sources). Update Table 19/22 and cluster-size conclusions if needed.

3. **Reframe baselines and figures to prioritize realistic comparators.**  
   Make “centralized provisioned (c=N/kc)” and “sectorized mesh” the primary comparators; move “centralized c=1” and “global-state mesh UB” to a clearly labeled “bounds” panel or appendix. Ensure captions repeatedly label them as bounds.

4. **Report both link-budget saturation and coordinator-ingress saturation in joint sweeps.**  
   In Section IV-D, add columns for “member link utilization” (including retransmissions and baseline telemetry) and indicate when the 1 kbps/node budget is exceeded, separate from coordinator drops. This will prevent misinterpretation of the independence result.

5. **Strengthen the physical-layer coupling discussion with one minimal packet/MAC validation target.**  
   Even if you do not run NS-3 in this paper, specify a concrete validation plan: modulation/coding assumptions, framing overhead, acquisition time, half-duplex constraints, and how these map to γ. This will make the γ-scaling more defensible and actionable.