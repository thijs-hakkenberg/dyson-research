---
paper: "02-swarm-coordination-scaling"
version: "av"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-02-27"
recommendation: "Accept"
---

## 1. Significance & Novelty — **Rating: 4/5 (Good)**

The manuscript targets a practically important problem: coordination scaling laws for very large autonomous spacecraft swarms (10³–10⁵, with discussion up to 10⁶). The focus on *byte-level traffic accounting under a strict per-node “RF-backup” budget* is a meaningful niche that is not well covered by either swarm robotics (typically ≤10² agents) or mega-constellation networking (routing/scheduling emphasis rather than coordination protocol sizing). The paper’s attempt to provide “closed-form design equations” and then validate them against a fast DES/Monte Carlo tool is aligned with the kind of engineering-oriented contribution that can be valuable to T-AES readers.

The strongest novelty lies in (i) the explicit decomposition of overhead into topology-dependent vs workload-dependent components (e.g., summaries/heartbeats/election vs commands), (ii) the coordinator ingress sizing discussion with multiple models (deadline vs token bucket vs TDMA), and (iii) the explicit treatment of correlated loss (GE) and the distinction between intra-cycle retries vs inter-cycle recovery. The “pipeline decoupling” observation (loss removes load before coordinator ingress) is also a useful architectural insight, though it is somewhat self-evident given the modeled point-to-point links and could be strengthened by showing when it breaks (shared-medium case) with at least one quantitative counterexample.

That said, the novelty claim in the Introduction (“No prior work has systematically compared… using byte-level traffic accounting under a fixed per-node budget”) is plausible but currently under-supported by the related work discussion. Several adjacent bodies of work (DTN operations, CCSDS scheduling, constellation TT&C capacity planning, and distributed state estimation/tracklet dissemination) are not engaged deeply, which weakens the positioning. The paper is still significant, but it needs sharper differentiation from “networking studies of ISL scheduling” and “ops studies of constellation management” by clarifying what is fundamentally new: *design equations for coordination protocol sizing* rather than routing capacity.

---

## 2. Methodological Soundness — **Rating: 3/5 (Adequate)**

The cycle-aggregated DES is appropriate for exploring coordination-cycle-level scaling and for enabling large-N sweeps. The manuscript is commendably explicit about what is modeled vs abstracted (Table III “Simulation Abstraction Scope”) and gives concrete message sizes (CCSDS-aligned) and rates. The analytical cross-checks are a strength: AoI P99 under geometric inter-report intervals (Eq. 23) matches DES closely; overhead accounting matches within 0.1%; GE inter-cycle recovery is compared to a Markov-chain prediction (Fig. 9).

However, several modeling choices materially affect conclusions and need stronger justification or sensitivity analysis. Examples: (a) the coordination cycle is fixed at \(T_c=10\) s for all topologies; (b) command workload is modeled as 512 B/node/cycle in stress-case, which dominates overhead and drives many “topology-independent” claims; (c) the GE model assumes channel state is constant within a cycle (explicitly making intra-cycle retransmissions ineffective “by construction”). These may be reasonable for an RF-backup regime, but they are not obviously representative across missions and link layers. The paper does include some sensitivity (e.g., \(p_{BG}, p_B\) sweeps; neighbor-cap sweep; reporting rate), but the most consequential knobs—\(T_c\), command rate distribution, and within-cycle coherence time—are not systematically explored.

Reproducibility is partially addressed via the GitHub repository and tag, which is excellent. For T-AES standards, the manuscript should still specify enough to reproduce key curves without the code: exact workload definitions (e.g., how many commands per cycle in nominal/event-driven beyond the prose), the precise coordinator service model (is it strictly serial deterministic 5 ms/message, or are there other delays?), and how “phase offsets” are assigned. Also, 30 replications with bootstrap CIs is fine for smooth metrics like mean overhead, but tail metrics (P95/P99) for recovery and AoI can be sensitive; the paper should justify the adequacy of 30 runs for those tails (or provide convergence checks / confidence intervals on P95).

---

## 3. Validity & Logic — **Rating: 3/5 (Adequate)**

Many conclusions are consistent with the presented accounting: if each node receives 512 B commands every 10 s, that alone is ~410 bps and will dominate any architecture where commands must reach nodes. Thus the claim that stress-case upper bound is “independent of topology” is directionally correct *given the assumed command model*. Likewise, the finding that summary traffic is small relative to commands is plausible with 512 B summaries per cluster per cycle.

The main risk is that some conclusions are framed too generally relative to the specificity of the model. For instance, the abstract states “commands dominating the stress-case upper bound (>60%) independent of topology.” This holds only if commands are per-node unicast of roughly that size and frequency; if commands can be multicast, compressed, parameterized, or replaced by onboard policies, the topology dependence can re-emerge. Similarly, the statement “centralized baseline does not diverge computationally until \(N\approx10^6\)” is based on a simplified \(M/D/c\) processing model with an assumed \(\mu_s\) and does not integrate the communication/scheduling bottlenecks that are arguably the real limit. The paper acknowledges this caveat later (Section IV-G), but the abstract and some summary tables risk over-emphasizing the compute result.

The “pipeline decoupling” result (Table 10: identical drops for “No Loss” vs “GE Only”) is logically consistent with the stated implementation: losses occur before ingress enforcement, so they cannot increase coordinator drops. But because this is a modeling artifact of where the drop accounting is applied, it should be presented more carefully: it is not only an architectural property (point-to-point) but also depends on *where retransmissions are scheduled and how ingress policing is implemented*. In real systems, retransmissions consume airtime and can delay other transmissions even on point-to-point links if there is a shared RF front-end, shared spectrum, or half-duplex constraints. The manuscript flags shared-medium contention as future work, but it should also discuss partial coupling cases (e.g., per-coordinator shared receiver chain, limited simultaneous demodulators).

Limitations are acknowledged (Section V-B), which is good. The paper would be stronger if it more explicitly separated “validated within the model” vs “expected operationally,” especially for claims about safe-mode MAC floors and for the orbital drift re-association estimate (currently a back-of-the-envelope bound without a clear constellation geometry model).

---

## 4. Clarity & Structure — **Rating: 4/5 (Good)**

Overall organization is strong: clear RQs, explicit contributions, and a results roadmap that maps to the contributions. The definitions of \(\eta\), baseline telemetry exclusion, and the distinction between offered vs delivered overhead are helpful and reduce confusion. Tables are generally informative (traffic accounting tables, sensitivity tables), and the inclusion of a “design equations summary” section is useful for practitioners.

The abstract is dense but mostly accurate; it does, however, mix message-layer utilization, MAC efficiency (\(\gamma\)), and topology comparisons in a way that may be hard to parse quickly. Consider simplifying the abstract to emphasize the key equations and the primary quantitative sizing results, while pushing some secondary numbers (e.g., exact utilization ranges) into the body. Also, the paper uses many percentages (5%, 46%, 20.5%, 26–67%, etc.); a single consolidated “budget table” early (per-node bps by class under each workload) would reduce cognitive load.

Some terminology could be tightened. “Protocol overhead” \(\eta\) excludes baseline status reports (256 B every cycle), but many readers will interpret “protocol overhead” as including periodic control/telemetry. You do define it carefully, but because this choice is central to the results, it should be reinforced with a figure or boxed definition early (e.g., in Section III-F). Similarly, “RF-backup regime (<1% of operational time)” is an important assumption, but the paper sometimes reads as though the 1 kbps channel is the primary coordination channel rather than a degraded-mode channel; clarifying this consistently would help.

Figures are referenced appropriately, but a few figures/tables are doing heavy lifting without enough methodological detail in the caption (e.g., Fig. 9 GE recovery curves: what exactly is the analytical Markov chain model? what is the state definition?). The manuscript would benefit from including the actual Markov chain equations in an appendix or short derivation.

---

## 5. Ethical Compliance — **Rating: 4/5 (Good)**

The manuscript contains an explicit disclosure about AI-assisted ideation in the Acknowledgment, including the models used and a citation. This is unusually transparent and aligns with emerging disclosure norms. There is no indication of human-subjects issues, dual-use concerns beyond generic swarm capability, or sensitive data use.

Two points to improve: (i) the disclosure currently says AI-assisted ideation “motivated aspects… but is not validated here.” For IEEE compliance and reader clarity, specify *what* was AI-assisted (e.g., initial architecture brainstorming, parameter choices, writing assistance) vs what was purely author-derived. (ii) Conflict-of-interest is not explicitly addressed; given “Project Dyson Research Team” and an associated website/tool, it would be good to add a brief statement that the authors have no commercial conflict (or disclose if there is one), especially since an open-source tool is promoted and could be perceived as advocacy.

---

## 6. Scope & Referencing — **Rating: 3/5 (Adequate)**

The topic fits T-AES (autonomous spacecraft operations, coordination architectures, comms constraints). The manuscript also has an engineering flavor consistent with T-AES: sizing equations, queueing models, and robustness discussion. It is less “electronics/sensing” and more “systems/operations,” but still within scope.

Referencing is broad and includes key classics (Lynch, Lamport, Raft, gossip, AoI survey) and constellation networking papers (Handley, del Portillo). However, the constellation operations citations are partly non-archival (FCC filings, company webpages, program pages). That is acceptable as context, but core technical claims should rely more on archival sources. Also, several relevant domains are lightly covered or missing: CCSDS scheduling/space link resource management beyond Proximity-1; DTN operational analyses for intermittently connected space networks; work on hierarchical/federated constellation autonomy and onboard planning; and literature on command dissemination strategies (multicast, parameterized policies, event-triggered control) that could challenge the “commands dominate independent of topology” framing.

The “sectorized mesh” justification (\(\sqrt{N}\) neighbors from screening volume arguments) is presented as a heuristic; it would benefit from citations to conjunction screening practice (e.g., spatial indexing / cell-based screening, covariance-based gating) or distributed tracking literature to ground the scaling argument.

---

## Major Issues

1. **Stress-case command model drives most headline conclusions but is under-justified and too rigid.**  
   The assumption “one 512-byte command per node per cycle” (Sections IV-E, Table VIII, Table XII) dominates \(\eta\) and leads to claims like “upper bound independent of topology.” You need either (a) a stronger operational justification (what missions require this sustained command rate?), or (b) broaden the command model (multicast, policy updates, sparse targeting distributions, variable size) and show how conclusions change.

2. **GE coherence-time assumption makes intra-cycle retransmission ineffective by construction; conclusions should be reframed or sensitivity added.**  
   In Section IV-C you explicitly state the GE state is constant within a 10 s cycle, so all retries see the same state. This is a legitimate worst case, but then the paper concludes “intra-cycle retry is structurally ineffective during correlated bursts.” That is only true under that coherence assumption. Add a sensitivity where GE transitions can occur within-cycle (or model burst length distribution in seconds) to quantify when intra-cycle ARQ becomes useful.

3. **Coordinator ingress sizing mixes three models but lacks a unified, rigorous derivation of the 21–25 kbps recommendation under realistic constraints.**  
   Section IV-A compares deadline budget, token bucket, and TDMA. The token bucket result (21 kbps) depends on carry-over across cycles, which may violate timeliness requirements if reports must be processed within the cycle. TDMA sizing uses a PHY rate of 24 kbps but then applies \(\gamma\) in a way that could confuse readers (Eq. 26 uses \(\gamma=0.85\) after deriving 0.949). The paper should clearly state the design requirement (e.g., “no drops, but delivery may slip across cycles” vs “must complete within \(T_c\)”), and then map each model to that requirement.

4. **Centralized baseline comparison is potentially misleading in the abstract and conclusion.**  
   The compute-only \(M/D/c\) analysis (Section III-B, Table I) is fine as a bound, but the statements “does not diverge computationally until \(N\approx 10^6\)” and “hierarchical advantage is fault tolerance during ground outages” need to be separated from comms/spectrum constraints more clearly. As written, a reader may infer centralization is “fine” to 10⁶ absent other issues, which is not established here.

5. **Analytical model details are incomplete for some “design curves.”**  
   The Markov-chain model underpinning Fig. 9 and the “Inter-cycle recovery P95” equation in the Design Equations Summary are not fully derived. Given the paper’s emphasis on “closed-form design equations,” the derivation (states, transition matrix, and how recovery CDF is computed) should be included (appendix is fine).

---

## Minor Issues

- **Equation/parameter consistency:**  
  - Eq. (26) uses \((k_c-1)\) rather than \(k_c\) for TDMA capacity; clarify why (is one slot reserved for coordinator? if so, specify).  
  - Table VI lists “Heartbeat/ACK 64 B bidirectional,” while sectorized mesh heartbeats are 32 B (Table IV/V); clarify whether these are different protocols or a mismatch.
- **Terminology:** “Protocol overhead” \(\eta\) excludes baseline status reports; consider renaming to “additional coordination overhead beyond baseline telemetry” in headings/captions to avoid misinterpretation.
- **AoI sampling methodology:** Table IX says AoI sampled every 100 s. Since \(T_c=10\) s, explain why downsampling doesn’t bias P99/max estimates (or provide AoI computed exactly per update event).
- **Figure references / file names:** Fig. 9 includes `\includegraphics{fig-cross-cycle-recovery}` without extension while others use `.pdf`. Ensure consistent compilation.
- **Claims needing citations or quantification:**  
  - “Optical ISL availability >99%” appears in abstract but is not cited or parameterized.  
  - “Spectrum scarcity (100 Mbps aggregate at N=10^5)” is asserted; provide a short derivation or citation.
- **Writing/structure:** The abstract is very dense; consider reducing the number of parenthetical numeric details and focusing on 2–3 headline sizing outputs.

---

## Overall Recommendation — **Major Revision**

The manuscript has a strong engineering premise, a useful modeling framework, and several results that could be valuable to practitioners. However, several central claims are tightly coupled to specific assumptions (command workload, GE coherence time, timeliness vs carry-over in ingress shaping), and the “closed-form design equation” narrative is undermined by missing derivations for key analytical curves. Addressing these issues requires additional analysis/sensitivity studies and clearer reframing, which goes beyond minor edits.

---

## Constructive Suggestions

1. **Generalize the command/workload model and re-run the key overhead conclusions.**  
   Add at least two alternative command dissemination models: (i) multicast/policy update (same command to many nodes), (ii) sparse targeted commands with a realistic distribution (e.g., heavy-tailed event-driven). Recompute \(\eta\) ranges and revisit the “topology-independent” stress-case claim.

2. **Add a within-cycle burst/coherence sensitivity for the GE model.**  
   Keep the current per-cycle GE as a worst case, but add a model where the GE state can transition at sub-cycle granularity (e.g., every 1 s) or where burst lengths are geometric in *seconds*. Quantify when \(M_r=2\) becomes beneficial and how P95 recovery changes.

3. **Clarify the coordinator ingress requirement as a function of a *timeliness constraint*.**  
   Explicitly define whether member reports must be received/processed within the same cycle to be useful. Then:  
   - If “within-cycle completion” is required, token-bucket carry-over may not be valid; show the required capacity under that constraint.  
   - If cross-cycle slip is acceptable, quantify the induced AoI/latency penalty.

4. **Provide the missing analytical derivations (appendix) for the Markov recovery curves and any “closed-form” results.**  
   Include the GE transition matrix, the definition of a “recovery event,” and the mapping from Markov hitting time to the plotted CDF/P95. This will materially improve rigor and reproducibility.

5. **Rebalance centralized vs hierarchical comparison to avoid over-interpreting the compute-only baseline.**  
   Keep the \(M/D/c\) bound, but adjust abstract/conclusion language to emphasize it is *not* an end-to-end scalability claim. If possible, add a simple uplink capacity bound (even a back-of-envelope) so the centralized baseline is compared on comms as well as compute, consistent with the rest of the paper’s emphasis.