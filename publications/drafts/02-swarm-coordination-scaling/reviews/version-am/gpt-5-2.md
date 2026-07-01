---
paper: "02-swarm-coordination-scaling"
version: "am"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-02-27"
recommendation: "Major Revision"
---

## 1. Significance & Novelty  
**Rating: 4 (Good)**  

The manuscript tackles a timely and practically relevant problem: how coordination/control-plane communication scales for very large autonomous spacecraft swarms (10³–10⁵, with discussion toward 10⁶). The explicit framing around an RF-backup/safe-mode budget (1 kbps/node) is a useful systems-engineering anchor that many constellation papers avoid. The paper’s main “novelty” is less a new algorithm and more a disciplined *sizing/characterization* study: byte-level accounting, coordinator-ingress bottleneck quantification (21–50 kbps), AoI trade curves under exception telemetry, and correlated-loss recovery behavior. For T-AES, that kind of engineering characterization can be publishable if the modeling is defensible and the results are presented as design guidance rather than universal laws.

That said, several headline claims are not as novel as the framing suggests. The O(1) overhead ratio for fixed-depth hierarchies is essentially immediate from the accounting model, and the AoI P99 under Bernoulli/exception reporting is exactly geometric (as you correctly show in Eq. (34)). The strongest contribution is therefore the *integration* and the toolchain (open-source DES, joint-condition verification), plus the coordinator-ingress burstiness analysis, which is more subtle than the overhead scaling. The paper would benefit from sharpening the novelty statement: emphasize (i) coordinator ingress sizing under bursty arrivals and different smoothing assumptions, (ii) explicit workload-envelope decomposition showing “architecture vs workload” dominance, and (iii) conditional independence results under point-to-point vs shared-medium access.

Overall, the topic is important; the contribution is meaningful as a reproducible sizing study, but the manuscript should more carefully delimit what is new versus what is a repackaging of analytically obvious relationships.

---

## 2. Methodological Soundness  
**Rating: 3 (Adequate)**  

The simulation approach is clearly described (cycle-aggregated DES, 10 s coordination cycles, vectorized implementation, one-year runs, 30 seeds). The traffic accounting is unusually explicit for this literature (Tables 6–8, 11), and the paper does a good job cross-checking several quantities against closed-form approximations (e.g., AoI P99 Eq. (34), retransmission success Eq. (35), centralized M/D/1 sanity checks). The open-source release and parameter table (Table 10) are strong reproducibility positives.

However, several modeling choices materially affect the conclusions and are either under-justified or internally inconsistent with the stated “byte-level” rigor:

- **Cycle aggregation vs within-cycle queueing:** The paper sometimes reasons about within-cycle batch queueing (e.g., D[k]/D/1 behavior, Table 23), but the DES is described as cycle-aggregated and vectorized. It is not fully clear whether within-cycle arrival times and service are truly simulated (with random phases and per-message service), or approximated analytically while still calling it DES. This matters for the 21–50 kbps coordinator-ingress thresholds and the latency distributions. You should explicitly state what is simulated at sub-cycle resolution for coordinator ingress (arrival timestamps, service completion times), and what is only computed from formulas.

- **Coordinator capacity model mixes bytes and messages:** In Section III (“DES cycle mechanics”) the coordinator ingress drop is based on a per-cycle byte budget or token bucket, but elsewhere coordinator processing is described as deterministic 5 ms/message. These are two different bottlenecks (link-rate vs CPU). The paper needs a clean separation: (i) ingress *link* capacity C_coord (bps) and buffering; (ii) coordinator *CPU* service rate (msg/s) and queueing. Right now, both appear, but it is unclear which dominates in which experiments and whether both are enforced simultaneously.

- **Loss and retransmission modeling:** Retransmissions are “intra-cycle only” with M_r = 2, but the store-and-forward recovery discussion in Section IV-C effectively assumes multi-cycle retries (“after n cycles”). If cross-cycle retry is abstracted (Table 13 says cross-cycle ARQ is abstracted), the recovery curves need to be clearly labeled as *analytic extrapolation* rather than simulated behavior, or you need to implement cross-cycle buffering/retry in the DES and report it as such.

- **Sectorized mesh neighbor discovery is treated as free:** Section III-D uses a global oracle updated every cycle at zero cost. You acknowledge this, but the conclusions comparing hierarchical vs sectorized mesh overhead depend on that assumption. At minimum, include a sensitivity term (even a simple beacon cost model) in the reported η for sectorized mesh, or position the sectorized mesh results as optimistic.

Statistically, the Monte Carlo layer is somewhat performative: you correctly observe overhead variance is near-zero because the workload is near-deterministic. That is fine, but then the paper should pivot to where randomness *does* matter (loss processes, failure processes, correlated outages) and ensure those are actually exercised in DES rather than mainly discussed analytically.

---

## 3. Validity & Logic  
**Rating: 3 (Adequate)**  

Most conclusions about overhead composition are supported by the byte accounting: if you assume 512 B commands per node per 10 s cycle, then ~410 bps/node is indeed the dominant term, and the 46% overhead figure is plausible given the 1 kbps budget (Table 18). The paper is commendably explicit that the 9× envelope is workload-driven, and that topology-induced summary overhead is small (<1%). The conditional nature of some claims is also acknowledged (e.g., independence under point-to-point ISLs vs shared-medium RF).

The main validity concern is that several “results” are either tautological given the assumptions or depend on assumptions that are not sufficiently defended for spacecraft operations:

- **Centralized baseline interpretation:** The “centralized compute does not diverge until N≈10⁶” conclusion is driven by the chosen μ_s=1000 msg/s and the assumed ability to scale c linearly with N (Table 1). That is not wrong, but it is also not a particularly meaningful systems conclusion without incorporating ground contact windows, spectrum constraints, and operational latency constraints more explicitly in the baseline model. You do discuss spectrum/availability qualitatively in Section IV-G, but the baseline remains a strawman in some plots (e.g., single-server bound). Consider either (i) making the realistic baseline the default in figures, or (ii) parameterizing ground contact and uplink scheduling in a way comparable to the RF-backup swarm regime.

- **AoI operational coupling is very weak:** The AoI calculation is sound, but the mapping to conjunction screening via a linear σ_pos growth (Eq. (35)) is too hand-wavy for the strength of language used (“quantitative input to conjunction screening trade studies”). As written, it risks over-interpretation. Either strengthen it with a minimal covariance propagation model (even a simplified two-body + drag uncertainty growth with representative values and citations) or clearly demote it to an illustrative aside and avoid operationally suggestive numbers in the abstract.

- **Coordinator ingress sizing:** The 50 kbps “deadline model” bound is plausible for worst-case burstiness, but the argument mixes “random-phase arrivals” (which should *reduce* synchronization) with “synchronized forwarding bursts” (phase staggering reduces drops). The narrative around what is synchronized and what is random needs tightening: are member reports random-phase but cluster summaries synchronized? Are drops measured on member-to-coordinator ingress or on coordinator-to-regional ingress? Section IV-A says the binding bottleneck is cluster ingress, but the phase-stagger experiment is described as spreading *regional* inbound traffic. The logical chain is muddled here and needs clarification.

Limitations are acknowledged in Section V-B, but some need to be elevated because they directly affect the major claims (MAC contention, deterministic occlusion outages, cross-cycle ARQ/DTN).

---

## 4. Clarity & Structure  
**Rating: 4 (Good)**  

The manuscript is generally well organized and readable, with a strong “systems paper” structure: clear RQs, explicit baselines, parameter tables, and design-equation summaries. The abstract is dense but largely consistent with the results sections. The traffic accounting tables are a major strength; they help the reader verify claims.

Areas needing improvement for clarity:

- **Terminology drift:** “DES,” “cycle-aggregated,” “priority queue,” and “vectorized” are used together in ways that could confuse readers about what is actually event-simulated. A short schematic of the simulation time model (what happens at 1 s vs 10 s; what is continuous-time within the cycle) would help.

- **Overhead definition and what is excluded:** You exclude baseline status reports from η (reasonable for topology comparison), but then many headline numbers in the abstract are “overhead as % of 1 kbps budget,” which can be misread as total utilization. You do define η_total later, but the abstract and early sections should more explicitly state both: e.g., “η=46% overhead beyond baseline; total utilization ≈67%.” Otherwise, a reader may assume 46% is total.

- **Figures are referenced but not shown here:** Several key claims hinge on figures (phase staggering, workload comparison, sensitivity). Ensure captions are self-contained and that axes/units make the claims verifiable. Also, Fig. 20 notes a 10⁶-node curve is analytic extrapolation—good practice; apply that labeling consistently wherever extrapolation is used (e.g., store-and-forward recovery curves if not simulated).

Overall, the paper is close to publishable clarity, but a few internal inconsistencies (especially around coordinator bottlenecks and timing) should be resolved.

---

## 5. Ethical Compliance  
**Rating: 4 (Good)**  

The manuscript includes an explicit disclosure about AI-assisted ideation in the Acknowledgment, and it appropriately states that the “Shepherd/Flock” concept is not validated in the current study. No human subjects, dual-use experimentation, or sensitive data issues are apparent. The open-source code and data availability statement is a positive for transparency.

Two suggestions for improvement: (i) move the AI-assistance disclosure from Acknowledgment to a short “Author Contributions / Use of AI Tools” note if permitted by the journal’s evolving policies, and (ii) add a brief conflict-of-interest statement (even if “none”) because “Project Dyson Research Team” and the associated website/repository could be perceived as having advocacy goals; T-AES reviewers often expect an explicit COI line.

---

## 6. Scope & Referencing  
**Rating: 4 (Good)**  

The topic fits IEEE T-AES well: constellation/swarm operations, comms architecture sizing, resilience, and queueing/simulation. The references cover distributed algorithms, AoI, DTN, constellation networking, and swarm robotics. Citations are mostly relevant and reasonably current (through ~2024), with appropriate classics (Lynch, Kleinrock, Demers gossip).

Concerns: several operational references are “non-archival” (Starlink ops filing commentary, Kuiper overview, DARPA webpages). Some are unavoidable, but key factual claims (e.g., Starlink operational numbers, ISL availability >99%, ground station availability 98–99.5%) should be backed by archival or at least technical reports where possible. Also, some networking/megasatellite literature could be expanded (e.g., more recent work on LEO control-plane management, inter-satellite laser link acquisition statistics, or CCSDS optical comm standards), since MAC efficiency γ is central to the conclusions.

The paper is more “space systems communications/operations” than “space economics,” despite the prompt; it is appropriate for T-AES.

---

## Major Issues  

1. **Clarify what is actually simulated vs computed analytically (core reproducibility/validity).**  
   - Sections III-A/III (“Cycle-Aggregated DES,” “DES cycle mechanics”) and IV-A/IV-H discuss within-cycle random phases, coordinator service times, queueing, and a priority queue, but also state the simulation is vectorized and not per-message event-based. You need to state precisely: do you generate per-message timestamps and simulate service completion, or do you approximate batch latency and drops with closed-form calculations? This directly affects coordinator capacity thresholds and latency distributions.

2. **Separate coordinator *link capacity* from coordinator *CPU processing* constraints.**  
   - Currently, C_coord drop models (Model A/B token bucket) and μ_c (5 ms/message) are both present, but their interaction is unclear. Define experiments that isolate each bottleneck, or enforce both simultaneously and report which is active. Otherwise, the 21–50 kbps “ingress requirement” is ambiguous (is it RF receive bandwidth, CPU budget, or both?).

3. **Resolve the apparent inconsistency in the phase-stagger discussion (what bottleneck is being relieved).**  
   - Section IV-A states the binding bottleneck is cluster coordinator ingress. But phase staggering is described as spreading regional inbound traffic. Yet Fig. 11 claims phase staggering “eliminates coordinator drops” at 25 kbps vs 50 kbps. Which coordinator (cluster or regional)? Which link is capacity-limited in that experiment? This needs to be unambiguous.

4. **Store-and-forward / multi-cycle recovery needs consistent modeling status.**  
   - Table 13 says cross-cycle ARQ and multi-hop store-and-forward are abstracted, but Section IV-C reports inter-cycle recovery to 95% in 4–7 cycles. Either implement cross-cycle buffering/retry in the DES and report it as such, or label these as analytic projections and avoid presenting them as simulated “results.”

5. **Strengthen or downscope the AoI-to-conjunction operational interpretation.**  
   - Eq. (35) and the 230 m “P99 uncertainty” mapping is too weakly justified to support strong operational statements. Either add a minimal but defensible covariance growth model (with parameter justification and bounds) or treat it as a non-result (remove from abstract-level claims and keep as a brief illustrative note).

---

## Minor Issues  

- **Notation overload / potential confusion:** You use \(C\) for capacities in multiple places (C_node, C_coord, μ). Consider a consistent convention: bps capacities as \(C_\cdot\), processing as μ, service time as s.  
- **Table 26 (link availability) footnote labeling:** Footnotes a/b/c appear inconsistent; the table references “\textsuperscript{b}” and “\textsuperscript{c}” but the note text does not align cleanly (there is a “\textsuperscript{c} Total offered…” but the column header marks differ).  
- **Centralized baseline message sizes:** Centralized “protocol overhead 5–15%” in Table 24 is not clearly derived from the same accounting rules as hierarchical (especially since centralized commands are ~100 bps/node in Table 18 but hierarchical is ~410 bps/node under stress). Clarify whether centralized uses the same stress-case command model or a different one.  
- **Global-state mesh assumptions:** The mesh model assumes full replication and uses a batch cap b=100; the resulting MB/node/cycle numbers are plausible, but the convergence-round formula \(R_{conv}=\max(\lceil\log_2 N\rceil,\lceil N/(bf)\rceil)\) should be cited or briefly justified (it is not a standard single-line result in epidemic dissemination).  
- **Failure model realism:** 2%/year exponential is fine as a placeholder, but “MTTF 50 years per node” is likely optimistic for smallsats depending on class; consider giving a range and showing sensitivity in Fig. 21 (failure resilience).  
- **Editorial:** Several places would benefit from tightening to avoid overclaiming “validated” when it is “cross-checked against closed form under simplified assumptions.”

---

## Overall Recommendation  
**Major Revision**

The paper is promising and potentially publishable in IEEE T-AES due to its explicit traffic accounting, parameterized sizing focus, and open-source tool release. However, several central results (coordinator capacity thresholds, phase staggering effect, inter-cycle recovery) are currently undermined by ambiguity about what the DES actually simulates versus what is analytically inferred, and by inconsistent bottleneck descriptions. Addressing the major issues above would substantially improve technical credibility and make the design guidance defensible.

---

## Constructive Suggestions  

1. **Add a “Simulation Time Model & Bottlenecks” subsection with a definitive truth table.**  
   Explicitly state for each experiment whether you simulate: (i) per-message arrival timestamps within cycle, (ii) coordinator CPU service/queue, (iii) link serialization and capacity, (iv) buffering/token bucket, (v) retransmission timing. A small table mapping “enabled/disabled” would eliminate most ambiguity.

2. **Refactor Section IV-A into two clean experiments: link-limited ingress vs CPU-limited processing.**  
   - Experiment A: infinite CPU, finite C_coord → drops purely due to link budget/burstiness.  
   - Experiment B: infinite C_coord, finite μ_c → latency/queueing purely due to CPU.  
   Then optionally a combined experiment. This will make the 21–50 kbps guidance interpretable as a *radio/PHY* requirement rather than conflated with CPU.

3. **Fix the phase-stagger narrative by clearly identifying the constrained node and link.**  
   If phase staggering is meant to relieve *regional* ingress bursts, show that explicitly (regional drops/queueing vs staggering). If it somehow affects *cluster* ingress drops, explain the coupling mechanism (currently unclear).

4. **Make inter-cycle recovery either fully simulated or explicitly analytic.**  
   If simulated: implement cross-cycle buffering and retry logic (even simplified) and report both delivered bytes and AoI impact. If analytic: label recovery curves as analytic projections and avoid presenting “95% within 4–7 cycles” as a DES outcome.

5. **Rebalance the abstract and conclusions to separate “tautological” from “empirical.”**  
   For example, present O(1) overhead scaling as a property of the accounting model, not as a simulation finding; reserve “simulation verified” language for joint-condition composition, burstiness thresholds, and any nontrivial interactions you actually observe.

If you address these points, the manuscript would read as a rigorous, transparent systems-sizing paper rather than a mix of accounting identities and partially specified simulation outcomes.