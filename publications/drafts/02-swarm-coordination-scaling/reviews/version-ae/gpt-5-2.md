---
paper: "02-swarm-coordination-scaling"
version: "ae"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-02-27"
recommendation: "Major Revision"
---

## 1. Significance & Novelty  
**Rating: 4 / 5 (Good)**

The manuscript targets a real and timely problem: scaling coordination/control-plane communication for autonomous swarms in the \(10^3\)–\(10^5\) regime, with explicit attention to bandwidth budgets that resemble RF fallback constraints. The framing around “coordination scaling” for future mega-constellation-like operations is relevant to T-AES readership, and the paper’s emphasis on *byte-level accounting* plus queueing/latency and loss behavior does fill a practical gap between (i) small-\(N\) swarm robotics studies and (ii) mega-constellation networking papers that focus on broadband routing rather than autonomy/control-plane coordination.

That said, the novelty is somewhat nuanced: many headline results are either analytically implied by the workload model (e.g., \(\eta\) linear in command probability \(p_{\text{cmd}}\); AoI geometric tail under Bernoulli exception reporting; retransmission failure under GE bad state) or depend strongly on parameter choices (e.g., 1 kbps/node, 10 s cycle, 512 B command per cycle stress case). The manuscript is candid about this, repeatedly positioning DES as an integration/checking tool rather than a discovery engine—this honesty is a strength, but it also means the paper’s “new knowledge” is primarily a *validated design envelope* and a set of sizing rules, not a new coordination algorithm or protocol.

The most defensible novelty contribution for an IEEE journal is the *coordinator ingress capacity sizing under burstiness/scheduling assumptions* (Sec. IV-A, Tables 9–10, Figs. 6–7): the 21–25 kbps convergence under smoothing/TDMA vs. the 50 kbps conservative bound is a useful engineering outcome. The sectorized mesh comparator is also helpful as an intermediate point between global-state mesh and hierarchy, though the sector model is heuristic and would benefit from stronger grounding (see Major Issues).

---

## 2. Methodological Soundness  
**Rating: 3 / 5 (Adequate)**

The DES methodology is generally appropriate to the stated RQs, and the paper does a good job enumerating message types (Table 8), parameter values (Table 4), and what is/waswo isn’t modeled (Table 5). The explicit separation between message-layer offered load and MAC efficiency via \(\gamma\) (Eq. 29) is also a reasonable abstraction *if* the paper is careful not to overinterpret the results as link-budget-ready. Reproducibility is above average for a simulation paper: code and tag are provided, and the workload accounting is sufficiently explicit that a reader could re-derive many results (indeed, the authors do).

However, several modeling choices reduce robustness and could be challenged by reviewers/readers as “baked-in” outcomes:

- The simulation is cycle-aggregated with a 10 s cycle used “consistently for all topologies” (Sec. III-A, Sec. III-F). This enforces comparability, but it also implicitly defines the offered load, AoI, and burst structure. Many results (e.g., coordinator ingress capacity, AoI percentiles) scale directly with \(T_c\), and the paper does not sufficiently explore sensitivity to \(T_c\) as a first-class parameter.
- Queueing validation is limited: centralized \(M/D/1\) cross-check at one low-utilization point and gossip bounds for \(N\le 1000\) (Sec. III-A). For the hierarchical case, coordinator queues and synchronized bursts are central to several claims, yet there is no comparable queueing-theoretic validation (e.g., deterministic arrivals with random phase, deadline vs. carry-over service) beyond qualitative explanation.
- The Monte Carlo framework (30 runs) is largely unnecessary given the near-deterministic model (the paper acknowledges SD \(<0.001\%\)). That is not inherently a flaw, but it suggests the study’s uncertainty quantification is not aligned with the dominant real uncertainties (orbital geometry-driven intermittency, correlated failures, MAC contention, heterogeneous traffic).

Overall, the methods are transparent and reproducible, but the paper would be stronger if it (i) elevated key sensitivities (cycle time, command size, heartbeat frequency, buffer sizes) and (ii) validated the coordinator-ingress burstiness results with either analytic bounds or a micro packet/MAC study (which the authors list as future work, but it is central to the 21–50 kbps headline claim).

---

## 3. Validity & Logic  
**Rating: 3 / 5 (Adequate)**

Most conclusions follow logically from the defined traffic model, and the manuscript is careful to label baselines as “intentional bounds” (Sec. I-C, Sec. IV-F). The analytical cross-checks are a major strength: AoI P99 (Eq. 30) matches simulation; overhead accounting matches within 0.1% (Table 13); retransmission under GE bad state is correctly derived (Sec. IV-C). The decomposition showing commands dominate stress-case overhead (Fig. 10) is particularly important because it prevents misattribution of \(\eta\approx46\%\) to hierarchy itself.

Where validity becomes weaker is in the leap from message-layer accounting to architectural guidance:

- The coordinator ingress sizing (Sec. IV-A) depends on the assumed arrival process (uniform random phase) and the “deadline vs. carry-over” model. The 50 kbps requirement is described as an artifact of random-phase clustering, but the paper does not provide a quantitative characterization of the burst distribution (e.g., probability that arrivals exceed capacity by factor \(x\) in a cycle for given \(k_c\)). Without that, the 2× factor can look ad hoc.
- The sectorized mesh model relies on a \(\sqrt{N}\) sector-size heuristic and then uses a hard neighbor cap (10–50) to restore \(O(N)\) behavior (Sec. III-D). This is plausible as an engineering heuristic, but the resulting overhead ratio (1.35–1.95×) is sensitive to that cap and to the assumption that “commands” exist similarly in the sectorized mesh (coordinator-to-member commands). The comparator risks being seen as a constructed strawman unless better justified operationally.
- Some claims appear inconsistent or at least confusing: e.g., the abstract says “nominal operations at \(\eta\approx5\%\)” and “event-driven at \(\eta\approx6\%\)” but later “nominal: coordinator sends only the 512-byte cluster summary per cycle” (Sec. IV-D). If commands are absent, why are heartbeats/ACKs still present at the same rate? That may be intended, but it should be explicit because heartbeats are a major fraction of the 5% baseline protocol overhead.

The limitations section is candid and helpful, but several limitations are not merely “future work”—they could change the topology ranking under high utilization (MAC contention, deterministic occlusion, priority traffic). The conclusions should more explicitly bound which results are robust (e.g., linearity of \(\eta\) in \(p_{\text{cmd}}\)) versus which are tentative (e.g., absolute coordinator kbps thresholds).

---

## 4. Clarity & Structure  
**Rating: 4 / 5 (Good)**

The paper is well organized for a long-form IEEE journal manuscript: clear RQs, explicit baseline interpretation, detailed parameter tables, and a results roadmap (start of Sec. IV). The distinction between topology-invariant baseline telemetry and protocol overhead \(\eta\) is clearly explained (Sec. III-F), and the repeated reminders that results are message-layer estimates scaled by \(1/\gamma\) are good practice.

The abstract is information-dense and largely accurate, though it is arguably overloaded for T-AES style: it contains many numbers, parenthetical caveats, and multiple claims that depend on definitions buried later (e.g., “cycle-aggregated DES,” “byte-level traffic accounting,” “\(\eta\)” excluding baseline telemetry, “MAC efficiency \(\gamma\)”). Consider tightening the abstract to emphasize the 2–3 most defensible contributions and moving some detailed numerics to the conclusion.

A few clarity issues impede comprehension for non-specialists:
- The paper uses “coordination cycle” \(T_c\) and “reporting rate” \(r\) interchangeably (with \(T_c=1/r\)), but later introduces exception probability \(p_{\text{exc}}\) which effectively changes the reporting process. A compact summary of the effective per-node offered load under each workload profile (status/heartbeat/command/summary) would reduce reader confusion.
- Several figures are referenced but not shown in the LaTeX (presumably external PDFs). Ensure captions are self-contained and that axes/units are explicitly labeled in the figures (especially for coordinator drops vs. capacity and AoI distributions).

---

## 5. Ethical Compliance  
**Rating: 4 / 5 (Good)**

The manuscript provides an explicit disclosure of AI-assisted ideation in the Acknowledgment, names the tools, and clarifies that the concept is not validated in the study. This is aligned with emerging IEEE expectations for transparency. The disclosure is appropriately scoped: it does not claim AI-generated results, and it does not obscure authorship.

Potential concerns: the author block is “Project Dyson Research Team” with deferred individual names/affiliations. IEEE policy generally requires authorship and affiliations at submission/review stage even if blinded review is not practiced for the journal; if this is a double-blind workflow, it should be handled through the submission system rather than the manuscript author line. Also, a conflict-of-interest statement is not included; if Project Dyson is an organization with a public advocacy/technology agenda, the paper should clarify funding sources and any commercial interests tied to the simulator or “interactive web-based simulators.”

No human/animal subjects, no sensitive datasets, and no dual-use issues are apparent beyond general autonomy/space operations.

---

## 6. Scope & Referencing  
**Rating: 3 / 5 (Adequate)**

The topic is within scope for IEEE T-AES (autonomous spacecraft operations, distributed coordination, comms constraints). The references cover distributed algorithms, swarm robotics surveys, gossip, DTN, satellite networking, and conjunction probability basics. The inclusion of AoI survey references is appropriate and current.

However, several citations are non-archival web pages or program fact sheets (Starlink ops page, DARPA pages, DoD fact sheet). While acceptable for context, key empirical claims (e.g., “Starlink coordination challenges,” “ground infrastructure scale,” operational maneuver/screening ratios) would be stronger with archival sources (conference papers, journal articles, FCC filings, operator technical papers). The manuscript also leans heavily on generic distributed systems references (Lynch) but could benefit from more constellation operations / autonomy-specific literature: e.g., work on onboard autonomy for conjunction assessment, distributed space situational awareness, or crosslink scheduling in large LEO networks.

Finally, the global-state mesh discussion mixes several regimes (fanout choices, batch size, convergence rounds) in a way that reads more like a back-of-envelope than a grounded baseline. If this baseline is meant as an “upper bound,” that is fine, but the paper should ensure the derivations and assumptions are internally consistent and properly cited.

---

## Major Issues

1. **Coordinator ingress sizing lacks a quantitative burstiness model/derivation (Sec. IV-A).**  
   The 50 kbps “deadline model” requirement is attributed to random-phase clustering causing \(\sim 2\times\) bursts, but the paper does not provide a statistical bound or distribution of within-cycle arrivals for finite \(k_c\), nor does it define the token bucket depth \(\sigma\) used in Model B. Since “21–50 kbps” is a headline contribution (abstract, conclusion), this needs stronger support: either (i) an analytic bound (e.g., concentration inequality / order statistics for uniform phases) or (ii) empirical CDFs of peak within-cycle offered load vs. \(k_c\) and required drop probability.

2. **Sectorized mesh comparator is under-justified and potentially a constructed baseline (Sec. III-D, IV-D, Table 3/7/11).**  
   The \(\sqrt{N}\) sector sizing and neighbor cap are heuristic; the architecture includes a “sector coordinator” and coordinator-to-member commands similar to hierarchy, which makes it not clearly “mesh” in the usual sense. The resulting overhead ratio (1.35–1.95×) is sensitive to the cap and to whether commands are modeled identically. The paper should either:  
   - reposition sectorized mesh as a *hybrid hierarchical-local mesh* and justify command/heartbeat semantics operationally, or  
   - provide at least one alternative decentralized comparator (e.g., purely local broadcast beacons within a screening radius; or k-nearest neighbor periodic exchange without a coordinator role), showing robustness of the “hierarchy advantage.”

3. **Key results are highly dependent on fixed \(T_c=10\) s and 1 kbps/node; sensitivity to \(T_c\) is missing.**  
   AoI, coordinator kbps thresholds, and offered-load saturation are all functions of \(T_c\). The paper provides sensitivity to reporting rate \(r\) (Fig. 16a), but not to the *cycle structure* that drives burstiness and deadlines. A sweep over \(T_c\) (or equivalently \(r\)) that also adjusts command frequency assumptions would clarify what is structural vs. parameter choice.

4. **Link loss modeling conclusions are correct but incomplete relative to the architecture’s stated needs (Sec. IV-C, Table 16).**  
   The paper concludes DTN/store-and-forward is “structurally required,” but the DES explicitly abstracts store-and-forward (Table 5) and does not model inter-cycle buffering except in the coordinator ingress shaper. This is acceptable as a limitation, but then the conclusions should be phrased more carefully: i.e., “intra-cycle retransmission alone is insufficient under correlated outages; inter-cycle mechanisms are indicated.” Right now, the wording reads stronger than what is simulated.

5. **Centralized baseline framing may confuse readers (Sec. III-B.1, Table 1, Sec. IV-F).**  
   The paper acknowledges \(c=1\) is an intentional worst-case, but then plots “diverges near \(10^4\)” (Fig. 19 caption) which could be misread as an actual centralized limit. Consider either (i) plotting \(c\in\{1,10,100\}\) as a family, or (ii) removing “divergence” language and emphasizing that centralized limits are spectrum/latency rather than processing.

---

## Minor Issues

- **Token bucket parameters not specified (Sec. IV-A, Model B).** Please define bucket depth \(\sigma\) and whether it is sized to one cycle of traffic, multiple cycles, or derived from buffer size. Without \(\sigma\), “zero-drop” is not reproducible.
- **Inconsistency in MAC efficiency handling for TDMA vs. other models (Table 10).** Table 10 lists TDMA with \(\gamma=0.85\) and “raw link 28 kbps,” but Model A/B list \(\gamma=1.0\). Elsewhere \(\gamma\in[0.7,0.9]\) is used as a generic factor. Consider presenting all coordinator capacities as *raw physical* and *message-layer effective* consistently.
- **Clarify whether heartbeats are per-cycle per-node regardless of workload profile (Tables 6–7, Sec. IV-D).** Since heartbeats are a significant fraction of the nominal \(\eta\approx5\%\), explicitly state heartbeat periodicity and whether it is reduced under nominal operations.
- **Equation/notation clarity:**  
  - Eq. (5) “\(M_{\text{total}} = N + N/k_c + N/(k_ck_r)\)” is uplink-only, but later overhead includes downlink commands/heartbeats. Consider renaming or adding a “reporting messages only” label in the equation environment.  
  - Eq. (24) states \(T_{\text{converge}} = D\tau_{\text{gossip}}\) with \(D=O(N^{1/3})\) for random geometric graph in 3D orbital space; this is not used later and may distract unless tied to results.
- **Figure captions:** Several captions mention panels (a)/(b) and specific results; ensure the actual figures include those panels and match the described experiments (phase-stagger, TDMA comparison, link model comparison).
- **Table 16 footnote lettering appears inconsistent:** In Table 16, the last column “Offered \(M_r=2\)” has superscripts \(\textsuperscript{b}\) and \(\textsuperscript{c}\) but the footnotes label \(\textsuperscript{a}\), \(\textsuperscript{b}\), \(\textsuperscript{c}\) with slightly mismatched text (also “\(\textsuperscript{b}\)” used twice with different meanings).
- **Authorship/affiliation placeholder:** Replace “Project Dyson Research Team” placeholder with actual author list for review-ready submission unless the journal’s workflow explicitly permits this.

---

## Overall Recommendation  
**Major Revision**

The paper is promising, well written, and unusually transparent in its accounting and cross-checks, but several headline conclusions—especially coordinator ingress sizing and the sectorized mesh comparison—need stronger methodological grounding and clearer reproducibility details. Addressing the burstiness/scheduling derivation, tightening the decentralized comparator justification, and adding sensitivity to cycle timing/MAC assumptions would substantially improve the manuscript’s rigor and reduce the risk that readers see key results as artifacts of parameterization rather than generalizable insights.

---

## Constructive Suggestions

1. **Add a quantitative burstiness characterization for coordinator ingress (high impact).**  
   Provide either analytic bounds or empirical distributions for peak within-cycle arrival volume for \(k_c\in\{50,100,200,500\}\) under random phases. Include a plot of \(P(\text{required } C_{\text{coord}} \le x)\) (or drop probability vs. \(C_{\text{coord}}\)) and explicitly define the deadline criterion. This will solidify the 50 kbps bound and explain how it scales with \(k_c\) and \(T_c\).

2. **Fully specify Model B (token bucket) and relate it to buffer size.**  
   State \(\sigma\) (bytes), whether tokens accrue continuously, and whether the coordinator can transmit/receive beyond cycle boundaries. Report how much buffering delay Model B introduces (even if small) and whether it affects AoI or latency metrics.

3. **Rework the sectorized mesh comparator to avoid “strawman” concerns.**  
   Either (i) justify the coordinator-like elements operationally (why a “sector coordinator” exists, why commands are identical), or (ii) introduce an additional decentralized baseline (e.g., k-nearest neighbor beaconing without a coordinator) and show the overhead/latency trade. Also, clarify what “sector coverage” means in terms of conjunction screening probability (even qualitatively).

4. **Add sensitivity sweeps for \(T_c\) (or equivalently, coordinated changes in \(r\) and command cadence).**  
   One figure/table showing how (a) AoI P99, (b) coordinator kbps thresholds, and (c) \(\eta\) change for \(T_c\in\{1,5,10,30,60\}\) seconds would make the results more general and help system designers map to their own control loop periods.

5. **Tighten claims around DTN/store-and-forward and correlated loss.**  
   Keep the strong analytical point (“intra-cycle retransmission fails under burst loss”), but soften “structurally required” unless you simulate at least a minimal inter-cycle buffering policy. Even a simple carry-forward model in the DES (without full BPv7) would substantiate the recovery-time claims (2–3 cycles i.i.d.; 5–10 cycles GE) that are currently asserted without shown data.

If you would like, I can also provide a short “reviewer checklist” of specific additions (plots/tables/equations) that would likely satisfy T-AES reviewers for the coordinator-ingress and decentralized-comparator aspects.