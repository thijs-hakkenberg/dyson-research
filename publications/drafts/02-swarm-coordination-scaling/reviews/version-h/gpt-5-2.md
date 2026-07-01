---
paper: "02-swarm-coordination-scaling"
version: "h"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-02-23"
recommendation: "Unknown"
---

## 1. Significance & Novelty — **Rating: 3/5 (Adequate)**

The manuscript tackles an important and timely problem: how coordination architectures scale from today’s few–tens of thousands of spacecraft to prospective \(10^5\)–\(10^6\) node “swarms.” The framing around mega-constellation operations (Starlink/Kuiper/OneWeb) is relevant to T-AES readership, and the attempt to bound the design space using two “reference baselines” (centralized \(M/D/1\) and a global-state mesh upper bound) is conceptually useful. The paper’s emphasis on discrete-event simulation with explicit byte-count accounting (rather than purely analytical message-complexity arguments) is also a meaningful direction, especially given the field’s tendency to stop at asymptotic claims.

However, the novelty claim is weakened by the fact that many of the key empirical results are not actually present in Version H: multiple “--- will be populated” tables (notably Tables \ref{tab:inflection}, \ref{tab:exception_validation}, \ref{tab:link_availability}, \ref{tab:coord_bw}) mean the central scaling and validation claims are currently not verifiable from the manuscript. In addition, the hierarchical architecture studied is a fairly standard fixed-depth tree with aggregation; the contribution therefore hinges on *quantitative characterization* (overhead/latency/fault tolerance under explicit parameters) rather than a new coordination mechanism. With the missing values filled and the DES artifacts fully documented, the paper could become a useful empirical reference; as-is, it reads partly like a protocol concept paper with placeholders.

A further novelty concern is the “global state required for collision avoidance” premise used to justify the \(O(N^2)\) mesh upper bound (Section III-B-3). Many operational conjunction assessment pipelines do not require every satellite to hold the full fleet state; they require *sufficient* state in a screening volume plus access to authoritative catalogs/ephemerides. Even for fully autonomous systems, the architectural design space includes hybrid approaches (sectorized/neighbor meshes, predictive ephemeris sharing, on-demand queries) that can avoid global replication. You correctly label the mesh as an “upper bound,” but the manuscript still risks setting up a strawman comparator unless you quantify how much global knowledge is truly necessary for the classes of maneuvers you target.

## 2. Methodological Soundness — **Rating: 2/5 (Needs Improvement)**

The DES framework is described at a high level and includes several good practices: event-driven simulation, multi-run Monte Carlo, bootstrap CIs, and some validation against queueing theory and gossip bounds (Section III-A). The explicit traffic accounting definition (Tables \ref{tab:traffic_accounting} and the overhead definition section) is also a strength, and the paper is commendably explicit about the coordination channel budget and the coordinator pooling assumption—then introduces \(C_{\text{coord}}\) to parameterize it.

That said, several methodological aspects currently undermine robustness and reproducibility:

* **Key results are not produced by DES despite being presented as such.** Table \ref{tab:link_availability} explicitly states that “Coordination success values for \(M_r=2\) are computed from Eq. (33)” rather than measured in the DES. This is not a minor detail: end-to-end cycle success is generally **not** equal to per-message success probability, because (i) messages have heterogeneous sizes and paths, (ii) there are multiple required messages per cycle, and (iii) retransmissions consume time/bandwidth and can induce queueing and deadline misses. If you want to claim retransmission “extends robust operating regime,” it should be demonstrated via DES with retransmission events, not computed via a scalar Bernoulli expression.

* **The overhead metric \(\eta\) is defined inconsistently with earlier “protocol overhead beyond baseline telemetry.”** In Section III-F you define \(\eta = \hat{B}_{\text{DES}}/(N C_{\text{node}})\) as “all coordination messages,” but elsewhere you emphasize protocol overhead excluding baseline status telemetry. Table \ref{tab:traffic_accounting} excludes ephemeris status reports from \(\eta\). This is fine, but the manuscript repeatedly blends terms “communication overhead,” “protocol overhead,” and “total coordination load.” You need a single set of symbols: e.g., \(\eta_{\text{proto}}\) excluding baseline and \(\eta_{\text{total}}=\eta_{\text{proto}}+\eta_{\text{status}}\), and then ensure all plots/tables label which is shown.

* **Sampling/scaling for large \(N\) is mentioned but not specified.** Section III-H defines \(\hat{B}_{\text{DES}}\) as “scaled by the inverse sampling rate for large \(N\)”—but the sampling scheme is not described (what is sampled? messages? nodes? time windows?), nor is error introduced by sampling quantified. For \(N=10^6\), this can dominate uncertainty.

* **Physical/link model choices are too stylized to support some claims.** The i.i.d. Bernoulli loss model (Section IV-F) is a very weak proxy for orbital occlusion, acquisition outages, and correlated fades. Likewise, the assumption that coordinator handoff uses a 1–10 Gbps optical ISL while routine coordination uses 1 kbps/node is plausible, but the coexistence of these channels and their scheduling is not modeled. The manuscript itself notes MAC/pointing constraints are abstracted away; that is acceptable if you scope claims accordingly, but several conclusions (e.g., “only hierarchical maintains tight latency at \(10^6\)”) are sensitive to these omitted mechanisms.

## 3. Validity & Logic — **Rating: 2/5 (Needs Improvement)**

The logical structure—bound the design space with baselines, then show hierarchical scaling, then explore cluster size/duty cycle/link availability/coordinator bandwidth—is coherent. The discussion is generally balanced in acknowledging that baselines are “intentional bounds” and that some optimizations are “analytically projected.” The explicit correction that prior versions used an analytical formula that masked DES dynamics is also valuable context.

However, several conclusions are not currently supported by evidence in Version H:

* **Slope-change analysis cannot be evaluated.** Section IV-D claims AIC model comparison and a breakpoint \(N^*\approx 45{,}000\) with CI, and says AIC values are annotated in Fig. \ref{fig:scaling_trajectory}. But Table \ref{tab:inflection} has no numeric \(\eta\) values, and the figures are not included in the LaTeX. Even if the figures exist externally, the manuscript as provided does not contain the data needed for reviewers to verify the breakpoint claim. If this is a “Version H” intended for review, the missing values are a major validity gap.

* **Exception-based telemetry validation is incomplete/misleading.** Table \ref{tab:exception_validation} is entirely placeholders (“---”). Yet the abstract and contributions claim validation at three scales and three \(p_{\text{exc}}\) values with “within 15%.” Those numbers must be present (means, CIs, and ideally absolute overhead reduction, not just ratios). Also, the “Predicted = \(p_{\text{exc}}\)” model is trivial; the meaningful validation is the *system-level* overhead and success-rate impact including cascade effects and coordinator summary sizes, which you mention narratively but do not quantify.

* **Coordinator bandwidth threshold \(\beta_{\min}\approx 0.25\) is asserted without results.** Table \ref{tab:coord_bw} is mostly placeholders, yet Section IV-G concludes a minimum of ~25 kbps for \(k_c=100\). This can be derived analytically from inbound status load (20.5 kbps), but then it is not a “DES stress test” result; it is a back-of-the-envelope requirement. If you keep the claim, label it as analytical and then show DES results including drops, queueing, and cycle success vs. \(C_{\text{coord}}\).

* **Some internal inconsistencies.** In Section III-F you say “Per coordination cycle (1 minute)” but the coordination cycle period is defined as \(T_c=10\) s throughout (Section III-A and metric definitions). This is not just a typo: it affects per-cycle accounting and any “within \(T_c\)” deadline logic. Similarly, the mesh “convergence time scales with diameter \(D\)” (Eq. (11)) is introduced, but the mesh model is otherwise described as global-state gossip with fanout scaling; the relationship between fanout, rounds, and physical network diameter is not reconciled.

Overall, the manuscript has the right *shape* of arguments, but too many key quantitative claims are either missing or computed outside the stated DES, which weakens validity.

## 4. Clarity & Structure — **Rating: 3/5 (Adequate)**

The paper is generally readable, with clear sectioning, explicit research questions, and a helpful “baseline interpretation note” that preempts misreading of the baselines as realistic competitors. The traffic accounting table is particularly helpful for clarity. The discussion section does a good job connecting to terrestrial analogs (cellular, BGP, ATC) without overclaiming equivalence.

Clarity suffers in several places due to terminology drift and parameter inconsistencies. The overhead metric is alternately called “communication overhead,” “protocol overhead,” and “coordination load,” sometimes excluding baseline telemetry and sometimes not. The manuscript should standardize symbols and labels and ensure figures/tables use consistent definitions. The coordination cycle period \(T_c\) is stated as 10 s, but later “per cycle (1 minute)” appears; this needs correction.

The manuscript also includes several “meta” statements about prior versions and reviewer feedback (e.g., “Versions A–G… reviewers correctly identified…”). Some of this is useful context, but for an IEEE Transactions submission it should be minimized and moved to a brief “changes from prior version” cover letter, not embedded repeatedly in the technical narrative. Keep the essential correction (DES byte counts vs analytical) but remove process commentary.

Finally, the absence of actual figure content in the provided source (PDFs referenced but not shown here) and the placeholder tables make it hard to assess whether the visuals are effective. If the figures indeed contain AIC annotations, CIs, and decomposition, the captions are good; but the manuscript must be self-contained for review (at least with populated tables and numerical summaries).

## 5. Ethical Compliance — **Rating: 4/5 (Good)**

The manuscript includes an explicit disclosure of AI-assisted ideation in the Acknowledgment, naming tools and clarifying that the “Shepherd/Flock” concept is not validated in this study. This is aligned with emerging transparency expectations and is preferable to omission. The disclosure is framed as ideation rather than data generation, which reduces ethical risk.

Two improvements are still needed. First, the “Project Dyson Research Team” anonymous authorship is understandable for review, but IEEE policy typically requires author identities to be known to editors even under double-blind processes (journal-dependent). Ensure the submission system separately includes author information and conflicts of interest. Second, the “commit hash: [PENDING]” in Data Availability is not compliant with reproducibility expectations; it should be a fixed archival reference (Zenodo DOI or at minimum a specific commit) at submission or revision.

No obvious ethical red flags appear regarding human/animal subjects. The main ethical/research-integrity concern is instead *overstating validation* when tables are placeholders; that should be corrected to avoid misleading readers.

## 6. Scope & Referencing — **Rating: 3/5 (Adequate)**

The topic fits IEEE T-AES: spacecraft constellation operations, autonomy, distributed coordination, and comms/latency/failure trade-offs are squarely in scope. The paper also appropriately leverages distributed systems foundations (Lamport, Raft, consensus) and queueing theory (Kleinrock). The constellation and DTN references (Handley, CCSDS BPv7) are relevant.

Referencing is somewhat uneven. Several key operational claims rely on non-archival sources (SpaceX web page, DARPA pages, magazine-style NRL review). Some non-archival citations are unavoidable for current programs, but the manuscript should balance them with more archival/peer-reviewed sources on mega-constellation operations, conjunction assessment scaling, and ISL availability statistics. For example, the link availability claim “0.85–0.95 typical” would benefit from a citation (even if approximate) or a derivation from geometry/acquisition assumptions.

Additionally, the “global state required” argument would be strengthened by citing conjunction assessment literature distinguishing local screening volumes, covariance growth, and catalog access architectures. Right now, the mesh upper bound is defended primarily by narrative astrodynamics considerations; adding authoritative sources would make it more credible and reduce the perception of a constructed strawman.

---

## Major Issues

1. **Placeholders in core results tables must be removed before the paper can be reviewed as a scientific contribution.** Tables \ref{tab:inflection}, \ref{tab:exception_validation}, \ref{tab:link_availability}, and \ref{tab:coord_bw} contain “---” for most entries while the abstract/conclusion make quantitative claims (e.g., breakpoint \(N^*\), “within 15%,” \(\beta_{\min}\approx0.25\)). Populate all values with means and 95% CIs, or downgrade claims to “planned” and remove from abstract.

2. **Retransmission/link-availability results are not DES results as presented.** Table \ref{tab:link_availability} states success with retransmission is computed from Eq. \ref{eq:retransmission}. You need to implement retransmission in the DES and compute *cycle success* and *overhead increase* under retries, including deadline misses due to added delay/queueing and increased bandwidth consumption.

3. **Overhead metric definitions are inconsistent and risk invalid comparisons.** The paper alternates between “protocol overhead beyond baseline telemetry” and “communication overhead” while using \(\eta\) ambiguously. Standardize: define \(\eta_{\text{status}}\), \(\eta_{\text{proto}}\), \(\eta_{\text{total}}\), and ensure every table/figure uses one consistently.

4. **Coordination cycle period inconsistency (“per cycle (1 minute)” vs \(T_c=10\) s) undermines traffic accounting.** Fix all per-cycle calculations, ensure event scheduling and deadlines align with \(T_c\), and re-check any derived rates (e.g., “6 status reports per 1 minute” is inconsistent with \(r=0.1\) msg/s unless you are using a 60 s window).

5. **Mesh upper bound justification needs tightening to avoid a strawman comparator.** If you keep the global-state mesh as an upper bound, quantify what “global state” means (trajectory table size, update frequency, acceptable staleness) and clearly separate (i) collision avoidance local screening vs (ii) fleet-wide maneuver planning. Consider adding at least one intermediate decentralized comparator (even analytically), such as sectorized mesh with bounded neighborhood size and periodic inter-sector summaries, to make the design-space mapping more credible.

---

## Minor Issues

- **Section III-F (“Per coordination cycle (1 minute)”)** conflicts with \(T_c=10\) s; likely a leftover from earlier versions. Replace with “per 60 s window” if that’s what you mean, or revise counts to 10 s cycles (1 status report per cycle at \(r=0.1\) msg/s implies *one report per 10 s*, not six).
- **Table \ref{tab:topology_comparison} “Failure Mode” column** shows values like “Single point (99.0%)” but does not define what 99.0% means (availability? annual? per-cycle success?). Add a definition or remove the percentage.
- **Eq. (12) diameter claim \(D=O(N^{1/3})\)** for “random geometric graph in three-dimensional orbital space” is not obviously applicable to satellites constrained to shells/planes; effective dimension may be closer to 2D on a sphere/torus. Either justify the model or avoid the scaling statement.
- **Coordinator queueing model**: you use \(M/D/1\) but arrivals are periodic/deterministic at cycle boundaries (bulk arrivals). A \(D/D/1\) with batch arrivals or \(GI/D/1\) may be more appropriate; at minimum discuss the approximation and whether it affects tail latency.
- **“Global-state mesh convergence validated against analytical gossip bounds for \(N\le 1000\)”**: specify which bound, what fanout, what metric (rounds to full dissemination vs fraction informed), and include a small plot or table in appendix/supplement.
- **Data availability**: replace “[PENDING]” with a real commit hash or an archival DOI at revision.

---

## Overall Recommendation — **Major Revision**

The problem is important and the paper’s overall architecture (DES + explicit traffic accounting + parameter sweeps) is promising for IEEE T-AES. However, Version H contains missing numerical results in multiple central tables and relies on analytical substitutions where DES validation is claimed (notably retransmission/link availability). As a result, key conclusions (slope-change breakpoint, exception-telemetry validation accuracy, coordinator bandwidth thresholds as “stress-test” outcomes) are not currently supported in a reviewable way. With the missing results populated, retransmission modeled end-to-end in the DES, and metric/period inconsistencies corrected, the manuscript could become publishable.

---

## Constructive Suggestions

1. **Make the paper self-contained quantitatively.** Populate all “---” entries; for each major claim (breakpoint \(N^*\), “within 15%,” \(\beta_{\min}\)), include the underlying numbers with CIs. If runtime is the blocker, reduce sweep breadth but keep enough points to support each claim.

2. **Implement retransmission and cycle deadlines in the DES, then re-report success/overhead.** Replace Eq. \ref{eq:retransmission}-derived “coordination success” with DES-measured cycle success, and report the *overhead increase* due to retries (bytes) and any induced queueing/deadline misses.

3. **Standardize metrics and symbols.** Introduce \(\eta_{\text{status}}, \eta_{\text{proto}}, \eta_{\text{total}}\) and use them consistently in all captions/tables. Explicitly state whether figures plot \(\eta_{\text{proto}}\) or \(\eta_{\text{total}}\).

4. **Fix the timing/accounting inconsistency around \(T_c\).** Audit all per-cycle computations, event schedules, and any narrative describing “per minute.” Add a short table mapping rates \((r)\) to per-cycle counts given \(T_c\).

5. **Strengthen the decentralization baseline discussion with one intermediate comparator and better citations.** Even if you do not simulate sectorized mesh, add an analytical bandwidth model for it (with clear assumptions about sector size, neighbor degree, and staleness) so the hierarchical approach is compared against something closer to plausible decentralized practice than the global-state upper bound. This will materially improve credibility and relevance for constellation operators.