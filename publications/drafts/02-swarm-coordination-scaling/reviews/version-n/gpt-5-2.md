---
paper: "02-swarm-coordination-scaling"
version: "n"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-02-24"
recommendation: "Unknown"
---

## 1. Significance & Novelty — **Rating: 4/5**

The manuscript tackles a real and increasingly important problem: coordination architecture scaling for very large autonomous space swarms (10³–10⁵, with discussion toward 10⁶). The framing around mega-constellation operations and future large-scale orbital infrastructures is timely, and the paper’s focus on *engineering design parameters* (cluster size, duty cycle, coordinator bandwidth, retransmission) is practically relevant to T-AES readers.

The novelty is mixed but still meaningful. The high-level claim that a fixed-depth hierarchy yields \(O(1)\) *normalized* overhead is largely a direct consequence of the assumed message model (as the authors explicitly acknowledge in Section IV-C). The paper’s main “new” contribution is therefore not asymptotic scaling theory but quantifying constants under a specific traffic model and validating that the DES implementation does not introduce unexpected nonlinearities within the chosen abstraction. This is a legitimate contribution if positioned as “parameterization and stress-testing” rather than discovery of scaling laws.

The most impactful part, in my view, is the explicit coordinator bandwidth stress test (Section IV-G) and the careful distinction between delivered vs offered load under loss and retransmission (Section IV-F, Table 10). Those are the kinds of engineering-facing results that can be reused by others. However, the significance is somewhat limited by the intentionally weak/upper-bound baselines and by the abstraction level (no MAC scheduling, no orbital contact geometry, i.i.d. loss), which makes it difficult to claim operational conclusions beyond the message-passing layer.

## 2. Methodological Soundness — **Rating: 3/5**

The DES framework is described in substantial detail (Tables 4–6, Section III), with clear parameter tables and explicit traffic accounting (Table 7). Reproducibility is partially supported via the stated code repository, but the “commit hash [PENDING]” in Data Availability is a problem for reviewability and reproducibility. The paper does a good job separating baseline telemetry from protocol overhead (Section III-F) and explicitly enumerating what is included/excluded in \(\eta\) (Table 7), which is often a source of confusion in similar studies.

That said, several modeling choices materially affect the reported constants and should be stress-tested more rigorously. Examples: (i) the coordinator ingress saturation model in Section IV-G uses a per-cycle byte budget with tail-drop; this is effectively a *token bucket with bucket size \(C_{\text{coord}}T_c\)* but without explicit service discipline or MAC scheduling—results like “zero drop requires 50 kbps” depend strongly on burstiness assumptions and scheduling. (ii) The regional coordinator latency dominates (Section IV-B “Latency budget”), but the arrival process at regionals is not well characterized: cluster summaries are generated periodically, so burst synchronization effects and phase assumptions matter. The paper claims uniform random phase offsets at node reporting, but the phase behavior of aggregated summaries (cluster-to-regional) is not clearly specified; if all clusters forward summaries near the end of the cycle, you can induce synchronized bursts and large queueing delays.

Statistically, the Monte Carlo approach is described, but the authors themselves note near-deterministic outputs (SD < 0.001%) due to the model structure (Section III-D, Table 9). This is fine, but it means the bootstrap CIs add little. The more important uncertainty is *model-form uncertainty* (MAC, correlated outages, contact schedules), which is acknowledged but not quantified. A stronger methodological posture would include sensitivity sweeps over the parameters that drive the constant \(\eta\): reporting rate \(r\), message sizes, ACK rate, command rate, and coordinator service rates \(\mu_c,\mu_r\), rather than emphasizing Monte Carlo replication of a nearly deterministic model.

## 3. Validity & Logic — **Rating: 3/5**

Within the stated abstraction (Table 6), the conclusions are mostly consistent with the model. The constant \(\eta\) result follows from the linear message structure and the normalization by \(N \times 1\) kbps, and the paper is appropriately explicit that this is not an emergent property (Section IV-C). The coordinator bandwidth results are logically derived from the inbound load calculation (20.48 kbps required for \(k_c=100\)), and the retransmission analysis is internally consistent (Eq. 17, Table 10) in distinguishing offered vs delivered load.

However, there are several places where the logic risks overreach or internal inconsistency:

* **Global-state mesh scaling and “limit”**: Section III-B.3 asserts global-state mesh is \(O(N^2)\) due to “each node must receive \(O(N)\) entries.” That is correct for full replication, but the paper then mixes epidemic dissemination complexity \(O(N f \log N)\) with the information-theoretic requirement. In Table 8 and Section IV-A, the claim that the mesh “exceeds bandwidth beyond \(10^5\)” depends entirely on the assumed state vector size and update frequency; those are not explicitly parameterized for the mesh in the same way as hierarchical traffic is. As written, the mesh baseline is not a controlled, apples-to-apples comparison; it is an upper bound, but the paper still reports specific “10–25%” overhead and a “~100,000 limit” (Table 8) without enough detail to reproduce those numbers.

* **Latency numbers vs link rate**: In Section IV-B “Latency budget,” serialization delay is computed as “256 B at 1 kbps ≈ 2 ms,” which is off by ~\(256\times 8/1000 \approx 2.048\) **seconds**, not milliseconds. This is a major technical error because it affects the entire latency interpretation and undermines the later claim that regional queueing dominates. If this is a typo (1 **Mbps** intended?), it must be corrected everywhere and reconciled with the 1 kbps/node coordination channel assumption.

* **Duty cycle / handoff reliability model**: Table 9 reports “handoff success” varying with duty cycle, but the reliability model is not specified (bit error rate? link outage probability? dependence on handoff size?). Since handoff uses 1–10 Gbps optical ISL and takes 1–10 seconds, the dominant failure modes would be acquisition/pointing interruptions and contact geometry, none of which are modeled. Without an explicit model, the numeric success rates (95% at 1h, 99.5% at 24h, etc.) read as arbitrary and may be misleading.

Overall, the paper is careful about limitations in Section V-E, but a few numerical/units issues and baseline comparability issues need correction for the conclusions to be considered robust.

## 4. Clarity & Structure — **Rating: 4/5**

The manuscript is generally well organized and readable. The “Baseline Interpretation Note” (Section I-C) is a strong addition: it clarifies that centralized and global-mesh are reference bounds rather than direct competitors. The explicit metric definitions (Section III-I) and traffic accounting table (Table 7) are also strong and should help readers interpret \(\eta\) correctly.

The abstract is information-dense and largely consistent with the body, but it includes many quantitative claims (e.g., \(\eta=20.66\%\pm 0.01\%\), \(C_{\text{coord}}\ge 50\) kbps, \(p_{\text{link}}\ge 0.5\)) that depend on assumptions later shown to be idealized. Consider softening the abstract language to emphasize “within the message-passing abstraction” earlier, not only later.

Figures and tables appear to be thoughtfully chosen, but several claims rely on figures not visible in the LaTeX (e.g., architecture diagram, overhead curves). Ensure axes, units, and definitions match the text—especially after correcting the serialization-delay unit issue noted above. Also, the paper sometimes mixes “overhead” as protocol-only \(\eta\) and “total utilization” (\(\eta + 20.5\%\))—you do define both, but some tables (e.g., Table 8) could be misread without close attention.

## 5. Ethical Compliance — **Rating: 4/5**

The manuscript includes an explicit disclosure of AI-assisted ideation in the Acknowledgment, including naming tools and clarifying that the concept is not validated in the current study. That is a positive step and aligns with emerging transparency expectations.

Two concerns remain. First, the “Project Dyson Research Team” authorship with deferred individual names/affiliations is unusual for peer review and may conflict with IEEE authorship policies depending on submission stage; at minimum, the final version must include full authorship and conflict-of-interest disclosures. Second, the use of non-archival web references for operational claims (e.g., Starlink operations) is not an ethics issue per se, but it affects verifiability and should be handled carefully (archived sources, retrieval dates, or more stable citations).

No human/animal subjects are involved; no immediate ethical red flags beyond authorship transparency and reproducibility completeness.

## 6. Scope & Referencing — **Rating: 3/5**

The topic fits IEEE T-AES: it intersects autonomous spacecraft operations, constellation networking, distributed coordination, and performance modeling. The paper also uses queueing theory and DES, which are within the methodological scope of the journal.

Referencing is broad and includes classic distributed algorithms (Lynch, Lamport), gossip (Demers), and space networking (CCSDS, Handley). However, several citations are non-archival operator webpages or program pages (Starlink, OFFSET, Blackjack, Kuiper). For T-AES, the manuscript would benefit from more archival references on (i) operational constellation autonomy and ground segment scaling, (ii) inter-satellite link MAC/scheduling and contact patterns, and (iii) conjunction assessment pipelines and locality properties. Also, some key claims (e.g., MAC efficiency \(\gamma \approx 0.85\) attributed to Akyildiz 2003) are not well supported by that older terrestrial-style satellite IP networking reference; more recent LEO ISL MAC/PHY references would strengthen credibility.

Finally, the paper is positioned as “no prior work has systematically compared architectures across this range using quantitative simulation.” That may be directionally true, but you should more carefully scope the claim and acknowledge adjacent work in large-scale network simulation of LEO constellations (routing, DTN, contact graphs) even if not focused on swarm coordination per se.

---

## Major Issues

1. **Critical units/latency calculation error (Section IV-B “Latency budget”)**  
   The serialization delay for “256 B at 1 kbps” is stated as ~2 ms; it should be ~2.048 **seconds**. This is not a minor typo: it changes the latency decomposition and may invalidate the conclusion that regional queueing dominates latency. You must correct the units and re-evaluate all latency results and any downstream interpretations.

2. **Mesh baseline not sufficiently specified to reproduce quantitative overhead/limits (Sections III-B.3, IV-A, Table 8)**  
   The global-state mesh is described as an upper bound, but the paper still reports concrete overhead numbers and a “~100,000” scalability limit. The state size, update rate, and exact exchanged payload per gossip round need to be explicitly parameterized (analogous to Table 4 for hierarchical). Otherwise, the mesh curve/percentages are not reproducible and can be challenged as arbitrary.

3. **Duty-cycle / handoff success rates lack a defined reliability model (Section IV-C, Table 9)**  
   Numeric “handoff success” values appear without an explicit stochastic model tied to link outage, acquisition time, BER, or contact window length. Given handoff is over 1–10 Gbps optical ISL, the dominant failure modes are not captured by the current abstraction. Either (a) define and justify a probabilistic model (and show sensitivity), or (b) present handoff cost/reliability qualitatively and avoid specific percentages.

4. **Coordinator bandwidth stress test depends on an implicit traffic shaping/MAC assumption (Section IV-G)**  
   The “per-cycle byte budget with tail-drop” is effectively a particular shaping model. Results like “zero-drop requires 50 kbps” should be accompanied by (i) analytical offered-load calculations with burstiness factor, (ii) sensitivity to phase assumptions, and ideally (iii) a simple TDMA slot model (even coarse) since the paper already argues TDMA as the mechanism.

5. **Reproducibility incomplete (Data Availability commit hash pending)**  
   For a simulation-based paper, the exact code version and configuration files used to generate each figure/table should be pinned (commit hash, DOI/Zenodo snapshot, or supplementary material). “[PENDING]” is not sufficient for archival publication.

---

## Minor Issues

- **Equation/parameter consistency**: In Eq. (1) you use \(C\) as processing capacity (msg/s), later \(C_{\text{coord}}\) as kbps. The notation is mostly clear, but consider renaming centralized processing capacity to \(\mu\) consistently to avoid confusion with bandwidth \(C\).  
- **Table 8 “Failure Mode / availability”**: The mesh “Distributed (99.99%)” and hierarchical “Graceful (99.5%)” appear as fixed numbers without clear derivation; if these are from Fig. 5, cite the exact assumed failure rate and define the metric in the table caption.  
- **Palm–Khintchine justification** (Section III-B.1): the superposition of many independent renewal processes tends toward Poisson under certain conditions; your periodic-with-random-phase assumption is reasonable, but you may want to cite a more direct result for “randomly phased periodic sources” or provide a short derivation.  
- **Transport overhead exclusion** (Section III-F): you mention 10–20% understatement; consider adding a simple multiplicative factor sensitivity plot/table since it directly affects the headline \(\eta\).  
- **Centralized baseline messaging**: you state “each node receives one command” per cycle; clarify whether commands are always sent or only when needed—this affects protocol overhead comparison.  
- **Non-archival references**: several “accessed February 2026” web pages; consider archiving via perma.cc or replacing with filings/technical papers where possible.

---

## Overall Recommendation — **Major Revision**

The paper is promising and largely well structured, with a clear engineering motivation and useful parameterization results (especially coordinator bandwidth and offered vs delivered load under retransmission). However, at least one major technical error (serialization delay units) undermines the latency analysis, and several key quantitative results (mesh baseline numbers, duty-cycle success rates) are not yet sufficiently specified or justified for an IEEE T-AES archival publication. Addressing these issues requires re-analysis and likely re-running simulations after correcting units and clarifying traffic models.

---

## Constructive Suggestions

1. **Fix the link-rate/serialization-delay inconsistency and re-validate latency results end-to-end**  
   Audit every place where 1 kbps/node is used to compute time (serialization, handoff feasibility on coordination channel vs optical ISL, coordinator ingress). Recompute Table 12/latency figures and update the “regional queue dominates” narrative accordingly.

2. **Fully specify the mesh payload model and provide a parameter table analogous to Table 4**  
   Define: per-node state vector size, update interval, whether exchanges send full tables or deltas, compression assumptions, and fanout scheduling. Then your mesh “upper bound” can still be an upper bound, but it becomes reproducible and its numeric overhead claims defensible.

3. **Replace (or justify) Table 9 “handoff success” with an explicit probabilistic model and sensitivity**  
   For example: define acquisition failure probability per handoff, outage probability during the 1–10 s transfer, and how these scale with duty cycle. If you cannot justify a model, remove the percentages and focus on handoff *frequency* and *data volume* as primary outputs.

4. **Add a minimal TDMA scheduler model for intra-cluster reporting to coordinators**  
   Even a simple “\(k_c\) slots per \(T_c\) with guard time \(g\)” model would make Section IV-G much stronger and would connect directly to your MAC efficiency factor \(\gamma\). This also helps test whether “burstiness” is an artifact of the random-phase assumption.

5. **Strengthen sensitivity analysis around the constant \(\eta\) coefficient**  
   Since the MC variance is near zero, add sweeps over \(r\), command/ACK rates, and message sizes (or header overhead multipliers). This would turn the main result from a single constant (20.66%) into a usable design surface (e.g., \(\eta(r, s, \text{ACK rate})\)), which would significantly increase archival value.