---
paper: "02-swarm-coordination-scaling"
version: "y"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-02-24"
recommendation: "Unknown"
---

## 1. Significance & Novelty — **Rating: 4/5 (Good)**

The manuscript targets a real and timely scaling question: how to coordinate autonomous spacecraft swarms in the \(10^3\)–\(10^5\) regime under tight per-node control-plane budgets. The paper’s emphasis on *byte-level traffic accounting* plus *latency tails*, *AoI*, and *correlated loss* is valuable for aerospace systems engineering, where “big-O” arguments alone are often insufficient to dimension links and deadlines. The explicit coordinator-capacity sizing result (random-phase vs. TDMA) is particularly actionable and is a good example of something that mean-rate analysis can miss.

That said, several “headline” results are essentially direct consequences of the chosen workload model (e.g., the \(O(1)\) overhead ratio under fixed-depth hierarchy and fixed per-node budget; and the near-zero Monte Carlo variance). The paper is candid about this in places (e.g., Section IV-D and Section IV-E), but the novelty claim should be framed more as: *quantifying coefficients and tail behaviors under explicit accounting*, and *identifying design levers (scheduling, exception telemetry, correlated outage recovery)*, rather than “discovering” scaling laws.

The inclusion of sectorized mesh as an intermediate comparator is a strength; it helps avoid a straw-man comparison between an intentionally pessimistic centralized baseline and an intentionally pessimistic global-state mesh upper bound. However, the sectorized mesh model is still quite stylized (e.g., fixed neighbor cap, coordinator-like sector head), and readers may question whether it meaningfully represents modern decentralized/DTN-enabled constellation operations. Strengthening the justification and/or adding one additional decentralized baseline (even analytically) would improve perceived novelty and fairness.

Overall, the contribution is relevant to T-AES audiences interested in autonomy, constellation operations, and comms/architecture scaling. With revisions that better separate “model-implied invariants” from “DES-derived engineering insights,” this could be a strong design-space characterization paper.

---

## 2. Methodological Soundness — **Rating: 3/5 (Adequate)**

The cycle-aggregated DES is appropriate for the questions posed (RQ1–RQ3) *if* the goal is message-layer offered-load sizing and queueing/burst effects at the coordination-cycle granularity. The paper does a good job documenting message sizes, cycle time, and what is/waswo isn’t included in \(\eta\) (Tables 7–9). The cross-check in Section IV-E-2 (Eq. 22) is helpful for implementation verification.

However, a central methodological concern is that many “simulation” results are effectively deterministic accounting under fixed per-cycle message generation. This is acknowledged (MC SD \(<0.001\%\)), but then raises the question: what does DES add beyond closed-form accounting for most metrics? The paper answers this partially (coordinator burstiness/capacity threshold; AoI tails; GE vs Bernoulli retransmission), but the methodology section should more clearly delineate which metrics are *analytically derivable* vs *require DES* given the modeling choices. As written, the DES framework is somewhat oversold as a general-purpose simulator, while it is primarily a structured accounting/queueing calculator with a few stochastic overlays.

Several modeling assumptions need tighter specification to be reproducible and to support the queueing/latency claims:
- **Regional coordinator burstiness / latency**: Section IV-B attributes ~500 ms mean latency primarily to “burst arrivals near end of each cycle,” but the mechanism is unclear because earlier (Section III-A) nodes have random phase offsets. Are *cluster summaries* phase-aligned (all sent at \(t=T_c\)) while member reports are random-phase? If so, that should be explicitly stated in the hierarchy model; if not, the burst explanation is inconsistent.  
- **Queueing model consistency**: Centralized is described as \(M/D/1\) with Poisson-like arrivals via Palm–Khintchine; hierarchical coordinators are also treated as \(M/D/1\), but the arrival processes differ (periodic-with-jitter, synchronized summaries, etc.). Some of the observed tail/mean delays depend critically on this.  
- **Coordinator capacity test**: The “deadline-constrained byte budget” per cycle is a strong assumption (no carry-over). It is reasonable as a conservative real-time model, but then the reported 50 kbps “zero-drop” threshold becomes highly model-specific. The paper does discuss this, but the capacity-sizing result should be presented explicitly as: *for a hard per-cycle deadline and random-phase member access*.

Statistically, bootstrapped CIs on near-deterministic outputs are not very meaningful; the paper admits this (Section IV-K). For AoI and loss experiments, variance and tail quantiles matter; here, reporting confidence intervals on P99 AoI and on drop probabilities (especially under GE) would be more informative than CIs on \(\eta\).

---

## 3. Validity & Logic — **Rating: 3/5 (Adequate)**

Most conclusions follow from the model as specified, and the manuscript is generally careful to label the centralized and global-state mesh as “bounds.” The coordinator scheduling insight (random-phase burstiness vs TDMA) is logically sound and aligns with known access-control behavior: with hard deadlines, peak-to-mean effects dominate. Likewise, the GE result (retries ineffective within a correlated bad state) is correct and well explained (Section IV-J).

The main validity risk is *interpretation drift* from “message-layer offered load” to “system-level feasibility.” The paper repeatedly notes that MAC/pointing/acquisition are abstracted and introduces \(\gamma\), but several parts still read like definitive feasibility claims at scale (e.g., “validated to \(10^5\)” and extrapolation to \(10^6\)” in Table 10 / Fig. 5). Given the abstraction, the strongest defensible claim is: *under this message model and cycle discipline, the offered-load overhead ratio is scale-invariant and the coordinator ingress must be dimensioned for burstiness or scheduled access*. Claims about absolute latency acceptability and “scalability limits” should be softened or tied to explicit physical assumptions.

The AoI analysis is a good addition, but its mapping to “\(\sim 2.8\) km along-track uncertainty” is currently too hand-wavy for T-AES. You do label it “order-of-magnitude,” but it uses an asserted 6–8 m/s growth rate “not modeled here.” This is fine as motivation, but it should not be used in the abstract as a quasi-quantitative mission impact without either (i) a cited orbital-estimation source, or (ii) a small coupled propagation/estimation submodel. Right now, the abstract’s kilometer-level uncertainty statement is not adequately supported by the presented model.

Finally, the sectorized mesh comparison is directionally plausible, but the conclusion that it “isolates the cost of peer heartbeats” (Section V-A) is only partially true because the sectorized mesh also includes a coordinator-like role and specific relay assumptions. The comparison is still useful, but the paper should avoid implying that the ratio 1.4–1.5× is general; it is a product of the chosen heartbeat size, cap=10, and command model.

---

## 4. Clarity & Structure — **Rating: 4/5 (Good)**

The paper is well organized, with clear RQs, explicit baseline interpretation, and a strong effort toward reproducibility (parameter tables; traffic accounting; validation cross-check). The abstract is dense but informative and does reflect the major quantitative takeaways. Tables 7–10 (traffic accounting, abstraction scope, overhead scaling) are especially helpful for readers to understand what is being counted.

That said, the manuscript is long and at times repetitive: the “intentional bounds” disclaimer appears in multiple places (Introduction, Results, figure captions). Consider consolidating and tightening these caveats to reduce cognitive load. Also, several results sections blend *model description* and *interpretation* in a way that makes it hard to tell what is an input assumption vs an emergent outcome (notably in the hierarchical topology description and in the latency decomposition in Section IV-B).

Some terms are used in potentially confusing ways:
- \(\eta\) is “protocol overhead beyond baseline telemetry,” but later “total utilization” is \(\eta + 20.5\%\). This is consistent, yet readers may misread \(\eta\) as total channel utilization. You do explain it, but consider renaming \(\eta\) to \(\eta_{\text{proto}}\) throughout figures/tables for clarity.
- “Coordinator capacity sizing” mixes *ingress capacity* and *ingress+egress* in places; the coordinator bandwidth parameter \(C_{\text{coord}}\) is defined as ingress+egress, but the stress test appears to be ingress-dominated and egress is stated to be on a separate optical ISL. This should be made consistent.

Figures are referenced appropriately, but because the PDF figures are not included here, I can only comment on captions and intended content. Captions are generally strong and interpretive (good for T-AES), but a few include strong claims that should be toned down given abstraction (e.g., Fig. 4 and Fig. 5 captions discussing “scalability limits”).

---

## 5. Ethical Compliance — **Rating: 4/5 (Good)**

The manuscript includes an explicit disclosure of AI-assisted ideation in the Acknowledgment and clarifies that the concept is not validated in the current study. This is aligned with emerging transparency expectations. There is no indication of human-subjects issues or sensitive data use.

Two improvements are advisable. First, “Project Dyson Research Team” with deferred author list is unusual for peer review; IEEE policy typically requires author identities at submission (even if masked for double-blind review, which T-AES does not generally use in the same way). If this is a placeholder for arXiv-style circulation, it must be resolved before journal submission.

Second, the data/code availability statement includes a “PENDING” commit hash. For reproducibility claims, the repository should be frozen to a specific release/tag at submission time (or provided as supplementary material). As it stands, the reproducibility disclosure is incomplete.

---

## 6. Scope & Referencing — **Rating: 4/5 (Good)**

The topic fits IEEE T-AES: coordination architectures, latency/overhead scaling, and robustness for large autonomous spacecraft swarms. The paper also connects to mega-constellation operations and DTN standards, which are within scope.

References are broadly relevant and include foundational distributed algorithms (Lynch), gossip (Demers), AoI (Yates et al.), DTN/BPv7, and constellation/networking work (Handley, del Portillo). However, several operational claims rely on non-archival sources (SpaceX/Kuiper webpages; DARPA pages). For a T-AES paper, it would be better to replace or supplement these with archival or regulatory filings (e.g., FCC filings for constellation sizes and operational descriptions; peer-reviewed analyses of Starlink operations and conjunction handling).

There is also a gap in citing constellation networking/control-plane literature that directly addresses scheduling, access control, and ISL MAC constraints in LEO optical networks. You cite CCSDS Proximity-1 (more proximal links) and Akyildiz (older satellite IP networks), but the “\(\gamma=0.85\)” assumption and TDMA feasibility would benefit from citations to more recent optical ISL system papers or standards (even if vendor-neutral), as well as recent mega-constellation ISL topology/control analyses.

---

## Major Issues

1. **Latency/burstiness mechanism is under-specified and partially inconsistent.**  
   Section III-A states per-node reports have random phase offsets; Section IV-B attributes dominant regional queueing delay to “all clusters … forward summaries simultaneously near \(t=T_c\).” The model must explicitly state whether cluster summaries are synchronized (and why), whether they inherit member-report phases, and how aggregation timing is computed. Without this, the latency results in Table 12/Fig. 7 are hard to trust or reproduce.

2. **Coordinator bandwidth sizing result depends strongly on a hard per-cycle deadline/no carry-over model.**  
   The 50 kbps “zero-drop” threshold (Section IV-G) is a key headline. Because the coordinator is modeled as a strict per-cycle byte cap with tail-drop and no inter-cycle buffering, the result is not general. You discuss alternatives briefly, but the paper should (i) formalize the deadline model, (ii) provide sensitivity to a token bucket / limited carry-over, or (iii) reframe the result as a conservative bound and quantify how conservative it is.

3. **AoI-to-mission impact claim in the abstract is not supported by the model.**  
   The “\(\sim 2.8\) km along-track uncertainty” mapping is not derived from the simulation or from a cited estimator/perturbation model. Given its prominence (abstract and conclusions), either remove the kilometer claim from the abstract or add a minimal coupled orbital uncertainty growth model with citations and clear assumptions.

4. **Baselines risk being perceived as straw-man despite disclaimers.**  
   The centralized baseline uses \(\mu_s=1000\) msg/s and \(c=1\) intentionally to “diverge,” and the global-state mesh is intentionally worst-case. This is acceptable as bounding, but the paper’s “topology comparison” framing (Table 11, Fig. 4) may still be read competitively. Strengthen the intermediate baselines (sectorized mesh) further and/or include a parallelized centralized control-plane baseline in the *main* figures (not only Table 1) to prevent misinterpretation.

5. **Reproducibility is incomplete (code commit hash pending; some parameters derived but not fully specified).**  
   Several derived quantities (e.g., how \(k_r\) and \(n_r\) scale with \(N\), regional coordinator assignment policy, propagation distance distribution) are not fully specified in algorithmic form. For a DES paper, include pseudocode or an explicit configuration schema.

---

## Minor Issues

- **Terminology consistency:**  
  - Table 9 lists “Gossip exchange (mesh) size \(256\times f\)” but earlier Table 5 defines gossip message size \(256\times b\). This is inconsistent (fanout vs batch size). Please correct the mesh traffic accounting definitions to avoid confusion.
- **Coordinator bandwidth definition inconsistency:**  
  Section “Coordinator Link Capacity Parameterization” defines \(C_{\text{coord}}\) as ingress+egress, but later egress is said to use separate optical ISL. Align the definition with the implemented bottleneck (likely ingress only).
- **Equation/parameter clarity:**  
  - Eq. (21) uses \(k_r=100\) in the numeric substitution, but Table 6 says \(k_r=\lceil N/(k_c\cdot n_r)\rceil\). If \(k_r\) is fixed at 100 in experiments, state it; if derived, then it varies with \(N\) and affects region-summary terms.
- **Failure/availability modeling for mesh:**  
  The statement “mesh availability is the fraction of time a node can reach at least \(f\) gossip partners” needs a connectivity model; currently link geometry is abstracted. Clarify whether this is purely probabilistic or geometry-based.
- **Formatting/presentation:**  
  Table 10 (“inflection”) includes a line “\(\eta_{\text{DES}}=46.0\%\) at all 8 intermediate sizes; omitted.” Consider including at least a small appendix table or provide the full dataset in supplementary material.

---

## Overall Recommendation — **Major Revision**

The paper addresses an important problem and contains several potentially publishable engineering insights (coordinator ingress sizing under burstiness vs TDMA; AoI/overhead trade-off; GE correlated-loss retransmission limits). However, key results depend on under-specified timing/burst assumptions and a strict per-cycle deadline model, and one prominent abstract-level mission-impact claim (km-level uncertainty) is not supported by the presented model. Strengthening model specification, adding sensitivity to the coordinator deadline/buffering assumption, and tightening claims to match the abstraction level are necessary before the work can be evaluated as a rigorous T-AES contribution.

---

## Constructive Suggestions

1. **Make the timing model explicit and reproducible (especially for hierarchical aggregation).**  
   Add a short subsection (or pseudocode) defining exactly when member reports occur, when coordinators aggregate, and when summaries are forwarded (e.g., “member reports uniform in \([0,T_c)\); coordinator aggregates at \(t=T_c-\epsilon\); summary forwarded at \(t=T_c\)”). Then re-run and report latency results under (i) synchronized summaries and (ii) phase-staggered summaries to demonstrate sensitivity.

2. **Add a buffering/deadline sensitivity study for coordinator capacity sizing.**  
   Keep the strict per-cycle cap as a conservative case, but include at least one alternative: token bucket with bucket size \(B\) (e.g., 0.5–2 cycles of carry-over) or EDF scheduling with limited lateness. Report how the “zero-drop” threshold moves between the mean-load bound (~20.5 kbps) and the current 50 kbps result.

3. **Either justify or remove the along-track km mapping from the abstract.**  
   Preferred: add a lightweight orbital uncertainty growth model (even a cited linearized along-track growth bound under differential drag) and clearly state assumptions. Otherwise, keep AoI in seconds and move the km mapping to discussion with citations and explicit caveats.

4. **Strengthen baselines to avoid misinterpretation.**  
   Add a “centralized with \(c=10,100\)” curve to the main overhead/latency figures (not just Table 1), and clarify what remains limiting (spectrum/propagation). For decentralized, consider adding an analytically defined DTN/store-and-forward “regional relay” baseline or a more standard neighbor-based dissemination model to complement the sectorized mesh.

5. **Resolve accounting inconsistencies and tighten definitions (\(\eta\), gossip size, \(k_r\), coordinator bandwidth).**  
   Fix the mesh message size discrepancy (\(b\) vs \(f\)), explicitly list which parameters are fixed vs derived in each experiment, and rename \(\eta\) in plots/tables to \(\eta_{\text{proto}}\) to reduce confusion with total utilization.