---
paper: "02-swarm-coordination-scaling"
version: "w"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-02-24"
recommendation: "Unknown"
---

## 1. Significance & Novelty — **Rating: 4 (Good)**

This manuscript tackles a timely and practically important problem: how coordination/control-plane communication scales for very large autonomous spacecraft swarms under a stringent per-node control-plane budget (1 kbps/node). The focus on *byte-level accounting* and explicit “design envelope” reporting (5–46% protocol overhead across workload regimes) is valuable for system architects, particularly given the current trajectory toward mega-constellations and more autonomous operations. The inclusion of a hybrid sectorized-mesh comparator is also helpful; it avoids a false dichotomy between pure hierarchy and an intentionally pessimistic global-state mesh.

That said, the novelty is somewhat mixed. Many core scaling conclusions are analytically implied by the model (fixed-depth hierarchy + constant cluster size ⇒ \(O(1)\) overhead ratio), and the DES is explicitly cycle-aggregated rather than packet/MAC-realistic. The strongest “beyond closed-form” claim is the scheduling interaction affecting coordinator capacity thresholds (random-phase vs TDMA). This is a meaningful systems insight, but the paper should better demonstrate that this effect is robust to alternative timing/jitter models and to realistic MAC/PHY constraints, otherwise it risks being an artifact of the particular within-cycle abstraction.

Overall, the work is significant as an engineering characterization study and a parametric exploration tool. The manuscript would be stronger if it more clearly positioned its novelty as: (i) a reproducible parametric envelope under explicit byte budgets, (ii) coordinator ingress sizing with timing-dependent burst effects, and (iii) coupling cost (overhead) to a freshness proxy (AoI) to expose the cost/quality tradeoff of exception reporting.

---

## 2. Methodological Soundness — **Rating: 3 (Adequate)**

The simulation framework is clearly described at a high level: cycle-aggregated DES with a 10 s coordination cycle, message-layer events, byte accounting, and simple queue/buffer models. The manuscript also does a good job of listing parameters (Table 9) and stating what is modeled vs abstracted (Table 10). The analytical cross-check (Eq. 21–22 and Table 17) is a useful sanity check for implementation correctness.

However, several methodological choices undermine robustness for an IEEE T-AES audience unless strengthened. First, the DES appears to be largely deterministic accounting with limited stochasticity; the Monte Carlo (30 runs) is acknowledged to have negligible variance (SD < 0.001% for overhead). That is fine, but then statistical framing (bootstrap CIs, 30 replications) becomes mostly performative. More importantly, the key “non-derivable” result—coordinator capacity thresholds of 50 kbps (random-phase) vs 24 kbps (TDMA)—depends heavily on the within-cycle arrival model and the *specific drop policy* (“byte-budget queue” with tail-drop within a cycle). This is not a standard queueing abstraction, and the paper does not provide enough detail to reproduce it unambiguously (e.g., whether capacity is enforced as a token bucket, whether unused capacity carries over, whether drops occur only after a per-cycle byte cap, etc.). The coordinator model in Section III and Section IV-G mixes message service rates (\(\mu_c\)) with a separate byte-budget capacity \(C_{\text{coord}}\); their interaction is not fully specified.

Second, several assumptions are free parameters without physical grounding: exception probability \(p_{\text{exc}}\), event probability \(p_{\text{event}}\), and the “screening alert rate” \(10^{-4}\)/node/s. The paper acknowledges this, but the conclusions (e.g., “P99 AoI > 400 s at \(p_{\text{exc}}=0.1\)”) could be misread as operationally meaningful rather than a parametric illustration. For T-AES, you likely need at least one scenario mapping these parameters to orbital dynamics and/or conjunction screening practice (even a simplified one), or you should more forcefully scope claims as “communication-layer envelope only.”

---

## 3. Validity & Logic — **Rating: 3 (Adequate)**

Many conclusions are internally consistent with the stated accounting. The decomposition that commands dominate overhead (512 B/node/cycle) and thus drive the 46% stress-case is logically consistent with Eq. 22 and Table 15. The discussion that exception-based telemetry reduces overhead approximately linearly in \(p_{\text{exc}}\) is also consistent with the Bernoulli-per-cycle reporting model. The AoI behavior (geometric inter-report intervals ⇒ heavy tail) is directionally correct, and the manuscript appropriately labels AoI as a proxy rather than a safety metric.

Concerns arise where the manuscript implies stronger engineering generality than the model supports. The coordinator bandwidth “zero-drop threshold” result is presented as a central DES finding, but it is contingent on: (i) the per-cycle byte-cap drop rule, (ii) random-phase being fixed per node across the whole run (Section III-L says \(\phi_i\) assigned at initialization), and (iii) the absence of MAC contention and link-layer framing/ARQ. In real systems, access is typically scheduled, shaped, and buffered across cycles; a strict per-cycle byte cap with tail-drop is a particular design choice. If instead the coordinator had buffering across cycles (token bucket / leaky bucket shaping), the required capacity might be closer to the mean offered load plus a smaller burst margin. The paper should either justify why the per-cycle cap is the right abstraction (e.g., hard real-time deadline per cycle) or explore alternatives.

Similarly, the link-loss analysis mixes “delivered \(\eta\)” and “offered load” (Table 20) in a way that is potentially confusing and may not be computed consistently. The offered-load approximation in the footnote is heuristic; it should be derived cleanly from Eq. 23 (expected number of attempts) and applied consistently to both baseline telemetry and protocol bytes. Also, the statement in Table 20 footnote that “total offered (including baseline retransmission) exceeds 100% at \(p_{\text{link}} \le 0.5\)” is plausible, but the paper should show the explicit calculation since it is an important feasibility boundary.

---

## 4. Clarity & Structure — **Rating: 4 (Good)**

The manuscript is generally well organized, with a clear narrative arc: problem → architectures → DES framework → results → implications/limitations. The “Baseline Interpretation Note” early in the introduction is helpful and reduces the risk of misinterpreting the centralized and global-mesh curves as strawman comparisons. Tables are detailed and often useful (Tables 9–11, 15, 17, 20). The abstract is information-dense and accurately reflects the major claims.

That said, the paper is long and sometimes repeats the same interpretive caution multiple times (e.g., centralized baseline is worst-case; mesh is upper bound). Some consolidation would improve readability. A bigger clarity issue is definitional: the paper uses “overhead” \(\eta\) to mean “protocol bytes excluding baseline status reports” (Section III-H), but then sometimes discusses “total utilization” and “effective overhead \(\eta_{\text{eff}}\)” with MAC efficiency \(\gamma\). This is fine, but the notation and the plotted quantities must be extremely consistent—otherwise readers will misread 46% as total channel occupancy. Consider adding a single boxed definition early (or a summary table) listing: baseline load, protocol overhead, total utilization, offered vs delivered under loss, and message-layer vs MAC-layer.

Figures are referenced but not shown in the LaTeX; assuming they are well-made, the captions are generally good. One caution: Fig. 3 includes a “\(10^6\)-node curve” that is explicitly analytical extrapolation; for T-AES, reviewers may push back on including extrapolated curves in the same plot as DES results unless visually separated and clearly caveated (you do caveat it, but it may still be seen as overreach).

---

## 5. Ethical Compliance — **Rating: 4 (Good)**

The manuscript discloses AI-assisted ideation in the Acknowledgment and points to a companion methodology paper. This is good practice and increasingly important. The disclosure is framed as ideation rather than generation of results, and the core technical claims are supported by the described DES/analysis.

Two suggestions for improvement: (i) move a brief AI-disclosure sentence into the main text (e.g., end of Introduction or Data Availability) rather than only in Acknowledgment, since some venues prefer prominent disclosure; and (ii) clarify whether any AI tools were used in code generation, data analysis, or figure generation, and if so how correctness was validated. Also, the author block “Project Dyson Research Team” without names is understandable for a draft, but for IEEE submission you will need author identities and affiliations; if anonymity is for review, state that explicitly (currently it reads like a publication plan rather than double-blind review practice).

---

## 6. Scope & Referencing — **Rating: 3 (Adequate)**

The topic is appropriate for IEEE Transactions on Aerospace and Electronic Systems: constellation operations, autonomous coordination, communication architecture scaling, and reliability. The references cover distributed algorithms, gossip, AoI, constellation networking, and some operational sources. The paper is strongest when it connects to queueing theory and AoI literature and when it frames architectures as bounds.

However, referencing and positioning could be improved in several ways:
- Several key operational claims rely on non-archival sources (SpaceX/Amazon web pages, DARPA pages, internal “Project Dyson” publication). For T-AES, you should minimize dependence on non-archival web sources for technical assertions (e.g., “Starlink operations,” “Kuiper overview”). Use them for context only, and cite archival/technical sources for system parameters when possible.
- The ISL/MAC modeling discussion would benefit from more recent LEO optical ISL and scheduling literature (beyond CCSDS Proximity-1, which is not an optical ISL MAC). If you are claiming TDMA guard efficiency \(\gamma=0.85\) as “typical,” it needs stronger citation support.
- Related work on distributed spacecraft autonomy and fractionated architectures exists beyond DARPA F6 (e.g., more recent formation flying autonomy, distributed mission management). Even if not directly about byte accounting, it would help contextualize the autonomy assumptions.

---

## Major Issues

1. **Coordinator bandwidth threshold result depends on a nonstandard and underspecified drop model (Section IV-G, Table 21, Fig. 12).**  
   The “byte-budget per cycle” tail-drop mechanism is central to the 50 kbps vs 24 kbps conclusion, but the model is not fully formalized. You need a precise definition (token bucket? strict per-cycle cap? buffer across cycles?) and justification that this corresponds to a real coordination deadline constraint. Otherwise the threshold may be an artifact.

2. **Mixing message-service queues (\(\mu_c,\mu_r\)) with byte-capacity \(C_{\text{coord}}\) without clearly defining their interaction (Sections III-B, III-C, IV-B, IV-G).**  
   At different points, coordinators are modeled as \(M/D/1\) servers with service rate in msg/s, but drops are later driven by a kbps byte budget. Are both enforced? Which is binding when? This ambiguity affects latency and drop conclusions.

3. **Loss/retransmission “offered load” calculations are heuristic and may be inconsistent (Section IV-F, Table 20).**  
   The offered-load approximation in the Table 20 footnote should be replaced by an explicit expected-attempts derivation and applied to *all* traffic components (baseline + protocol). Feasibility conclusions (“exceeds 100%”) should be numerically demonstrated.

4. **Parameters driving the design envelope (especially \(p_{\text{exc}}\), \(p_{\text{event}}\), and alert rate) are not tied to orbital dynamics or operational screening practice.**  
   The paper acknowledges this, but the result is that the “design envelope” is hard to interpret as an aerospace systems contribution rather than a generic parametric exercise. At minimum, include one physically motivated scenario mapping (even coarse) or strengthen the scope statement to avoid overinterpretation.

5. **The “global-state mesh” upper bound is so pessimistic that it risks being dismissed, and the sectorized mesh comparator is capped to force \(O(N)\).**  
   You do explain these as bounds, but the mesh section still spends substantial space. Consider tightening it and spending more effort on realistic decentralized comparators (e.g., k-nearest neighbor dissemination based on conjunction volumes, or probabilistic screening) to make the hierarchy-vs-decentralized comparison more meaningful.

---

## Minor Issues

- **Inconsistency/possible confusion in TDMA parameter naming:** Section III-L defines guard-time fraction \(g\) and \(\gamma=1-g\), but later Section IV-H says “guard-time fraction \(\gamma=0.85\)” (Fig. 12 caption and nearby text). Use one convention consistently: guard fraction \(g\), efficiency \(\gamma\).  
- **Eq. 12–13 sector overhead arithmetic:** Eq. (13) gives \(B_{\text{sector}}^{\text{capped}}=256+\min(k_s-1,10)\times 32\), but the text says “yielding ~576 B/node/cycle” for heartbeats+status reports; that corresponds to 256+320=576 (fine), but then later “With addition of commands … total overhead 65–67%.” It would help to show the actual per-cycle bytes including commands and ACKs to support that percentage.  
- **Cluster size vs latency table (Table 18):** latency values are piecewise constant in a way that suggests a threshold effect (likely regional burst/queue discretization). Explain why 75 and 50 have identical latency and why 100–500 are identical; otherwise it looks suspiciously quantized.  
- **Fig. 3 includes \(10^6\) analytical extrapolation:** consider visually separating extrapolated curves or moving to an appendix to avoid conflating simulated and extrapolated results.  
- **Citation quality:** several “non-archival” citations are used for major framing. For T-AES, reduce reliance or reframe as contextual, not evidentiary.  
- **Terminology:** “protocol overhead” is not only “protocol” in the networking sense; it includes workload-dependent commands. Consider renaming to “coordination traffic fraction beyond baseline telemetry” or similar.

---

## Overall Recommendation — **Major Revision**

The manuscript addresses an important problem and contains potentially publishable insights (notably, the explicit control-plane budget envelope and the timing/scheduling dependence of coordinator ingress sizing). However, key results hinge on modeling choices that are currently underspecified or potentially unrealistic (coordinator byte-cap drop model; interaction of msg/s service with kbps caps; retransmission offered-load math). To meet IEEE T-AES standards, the paper needs clearer formalization of these mechanisms, stronger reproducibility detail, and at least one physically grounded scenario tying free parameters (exception rates, alert rates) to orbital operations. With these revisions, the work could become a solid engineering characterization paper.

---

## Constructive Suggestions

1. **Formalize the coordinator ingress model and provide an alternative buffering/shaping sensitivity.**  
   Define \(C_{\text{coord}}\) precisely (token bucket with bucket size \(B\)? strict per-cycle cap? buffer across cycles with deadline?). Then re-run the coordinator threshold experiment under at least one alternative (e.g., token bucket with carry-over) to show robustness of the 50→24 kbps scheduling conclusion.

2. **Unify the queueing and bandwidth constraints into a single consistent service model.**  
   Either: (i) model service in bytes/s everywhere (message sizes matter naturally), or (ii) keep msg/s servers but remove byte-cap drops, or (iii) explicitly state both constraints and show which binds in each experiment. A concise model diagram/table would help.

3. **Replace the retransmission offered-load heuristic with a clean derivation and report total offered utilization (baseline + protocol).**  
   Use \(E[\text{attempts}]=\sum_{i=1}^{M_r+1} P(\text{need attempt }i)\) under Bernoulli, and compute offered bytes exactly. For GE, compute expected attempts conditioned on state, or simulate it directly and report offered utilization from the DES counters (since you already do byte accounting).

4. **Add one operationally grounded parameter mapping case study.**  
   Even a simplified orbital prediction error growth model (e.g., along-track uncertainty growth rate) could map AoI percentiles to position uncertainty and then to conjunction-screening volume inflation. This would make the AoI section much more compelling and aerospace-specific.

5. **Strengthen the decentralized comparator story.**  
   Keep the global-state mesh as a bound, but emphasize the sectorized mesh (and possibly add a k-nearest-neighbor / screening-volume dissemination variant without coordinator commands) so the hierarchy vs “practical decentralization” comparison is more balanced and informative.