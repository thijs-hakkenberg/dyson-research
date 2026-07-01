---
paper: "02-swarm-coordination-scaling"
version: "bj"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-02-27"
recommendation: "Unknown"
---

## 1. Significance & Novelty — **Rating: 4/5 (Good)**

The manuscript targets a real and increasingly important problem: how to size and reason about coordination/command-and-control communications for very large autonomous spacecraft swarms (10³–10⁵). The emphasis on *closed-form* sizing relationships (byte budgets, coordinator ingress capacity, TDMA airtime feasibility, and AoI/recovery tails) is a useful engineering contribution, and the paper’s intent to provide “design equations” rather than only simulation is aligned with what practitioners need for early trades.

The strongest novelty claim is the explicit separation into three feasibility layers—(i) byte budget/utilization \(\eta\), (ii) MAC efficiency \(\gamma\), and (iii) TDMA airtime schedulability—plus the observation that “stress-case” information demand may be within byte budgets yet not schedulable in a 10 s cycle under half-duplex + unicast. That distinction is important and not commonly made in constellation/swarm coordination papers, which often blur information content with airtime feasibility.

That said, some novelty is diminished by the fact that several results are driven primarily by the chosen message model (fixed 256 B status, 512 B commands, 10 s cycle) and by the “RF backup at 1 kbps average / 24 kbps burst PHY” premise. The paper would read as more broadly generalizable if it more explicitly positioned its equations as *parametric templates* and provided a clearer mapping from mission classes (e.g., station-keeping vs. collision avoidance vs. distributed sensing) to the assumed message semantics.

---

## 2. Methodological Soundness — **Rating: 3/5 (Adequate)**

The cycle-aggregated DES is a reasonable approach for exploring scaling to 10⁵ nodes with Monte Carlo, and it is commendable that the authors (i) provide an open-source repository and (ii) use the DES primarily to cross-check closed-form accounting (e.g., Table~\ref{tab:inflection}) and to estimate tail recovery distributions (Fig.~\ref{fig:cross_cycle_recovery}). The per-run-then-aggregate approach for tail statistics in Table~\ref{tab:aoi_results} is also methodologically thoughtful and avoids overstating confidence by pooling correlated samples.

However, several modeling choices materially affect the headline conclusions and need stronger justification or sensitivity analysis. Most importantly: (a) the half-duplex TDMA superframe is treated as feasible with a tight 623 ms margin (Table~\ref{tab:superframe}) while simultaneously acknowledging unmodeled overheads (ranging, calibration, FEC, control) that are folded into \(\gamma\) somewhat ad hoc; (b) the GE model assumes channel state is constant within a 10 s cycle, making intra-cycle retransmissions ineffective “by construction” (Section~\ref{sec:ge_link}). While the authors acknowledge this, the resulting recovery conclusions depend strongly on the coherence-time assumption; the paper would be stronger with an explicit intermediate regime model (e.g., sub-cycle Markov transitions or a burst-length distribution) rather than only bounding arguments.

Reproducibility is partially addressed via the repository tag and parameter tables, but the manuscript still omits key implementation details needed to reproduce *exactly* the reported numbers: e.g., the precise definition of “drops” vs “deadline misses” (you state deadline misses are not tracked), the queue service model at coordinators during TDMA (does service occur continuously or in a post-reception batch?), and the exact handling of per-cycle cutoffs and buffering across cycles. These details matter for the coordinator-capacity experiments (Fig.~\ref{fig:phase_stagger}, Table~\ref{tab:joint_interaction}) and for AoI sampling.

---

## 3. Validity & Logic — **Rating: 3/5 (Adequate)**

Many conclusions are logically consistent with the provided accounting: e.g., the coordinator ingress requirement of \(\approx 20.5\) kbps for \(k_c=100\), 256 B per member per 10 s is straightforward; the TDMA airtime calculation is clear; and the AoI P99 formula (Eq.~\ref{eq:aoi_analytic}) matches the DES in Table~\ref{tab:aoi_results}. The “byte budget vs schedulability” distinction is also correctly argued: \(\eta\) counts information content, while half-duplex airtime determines whether per-node unicast commands fit in-cycle (Eq.~\ref{eq:unicast_stagger}, Table~\ref{tab:schedulability}).

The main validity risk is that the paper’s headline overhead statements can be misread because \(\eta\) is defined as “protocol overhead beyond baseline telemetry,” yet the stress-case \(\eta\approx 46\%\) is dominated by *commands* that are arguably not “protocol overhead” but mission workload. You do flag this (Contribution bullets and Section~\ref{sec:workload_profiles}), but the terminology still risks confusing readers: “architecture-specific overhead” is ~5%, while “total non-baseline traffic including commands” reaches 46%. The abstract currently blends these in a way that could be interpreted as “protocol overhead is 46%,” which is not what your later decomposition (Fig.~\ref{fig:decomposition}) says.

A second logic concern: the coordinator half-duplex budget assumes command dissemination is broadcast (Type 1) for the one-cycle feasible stress-case, while the stress-case itself seems to be defined as “512 B command per node per cycle” (Table~\ref{tab:bw_breakdown}, Table~\ref{tab:schedulability}). Those are different semantics. If stress-case information demand is truly “per-node unique command,” then the one-cycle feasibility claim should not be attached to the stress-case without a clearer separation of (i) information volume, (ii) addressing mode, and (iii) airtime feasibility. Right now Table~\ref{tab:schedulability} tries to split “Stress (bcast)” vs “Stress (unicast),” but earlier tables (e.g., Table~\ref{tab:bw_breakdown}) and the abstract could be read as mixing them.

---

## 4. Clarity & Structure — **Rating: 4/5 (Good)**

The manuscript is generally well organized for an IEEE T-AES style paper: clear RQs, explicit notation table (Table~\ref{tab:notation}), strong use of summary tables (e.g., Table~\ref{tab:bandwidth_scaling}, Table~\ref{tab:schedulability}, Table~\ref{tab:superframe}), and repeated reminders about modeling scope (message-layer vs PHY/MAC). The “Roadmap” at the beginning of Results is helpful, and the design-equations summary in Discussion is valuable for practitioners.

That said, the paper is dense and sometimes internally inconsistent in terminology. The repeated use of “protocol overhead” to include commands (which are workload/application traffic) will confuse many readers, especially those from networking backgrounds where protocol overhead means headers, retransmissions, control-plane, etc. I recommend renaming \(\eta\) to something like “non-baseline coordination traffic fraction” and reserving “protocol overhead” for heartbeats/summaries/election/sync/retransmissions.

Several figures are referenced but not available in the LaTeX excerpt (e.g., architecture diagram, multiple PDFs). That is fine for review of the source, but it increases the importance of captions being self-contained (many are good) and of ensuring that key numeric claims do not rely solely on figures. In a few places, critical claims are figure-backed without enough inline numeric support (e.g., “Fleet-wide TDMA cost is 0.28 kbps/node (1% coordinators); see Fig.~\ref{fig:tdma}” — this should be derivable in text).

---

## 5. Ethical Compliance — **Rating: 4/5 (Good)**

The manuscript includes an explicit disclosure of AI-assisted ideation in the Acknowledgment, which is good practice and increasingly necessary. The disclosure appears appropriately scoped (“motivated aspects… but is not validated here”), and it does not claim AI-generated results.

Two improvements are advisable for IEEE compliance and reader trust: (i) clarify whether any text, code, figures, or analysis were AI-generated vs. only ideation support; and (ii) ensure the repository includes provenance for generated plots and the exact commit/tag used for the reported numbers (you provide a tag, which is good—add a short “repro steps” note).

No obvious ethical red flags appear regarding human subjects, sensitive data, or dual-use beyond the general military relevance of swarms (which is not inherently disallowed). Still, given potential defense interest, a brief statement that the work is conceptual/analytical and uses no controlled data could preempt concerns.

---

## 6. Scope & Referencing — **Rating: 3/5 (Adequate)**

The topic fits IEEE Transactions on Aerospace and Electronic Systems, particularly at the intersection of autonomous spacecraft operations, distributed coordination, and communications sizing. The paper also has relevance to mega-constellation operations, and it appropriately cites key networking and constellation references (Handley; Del Portillo; CCSDS standards; AoI surveys; SWIM; Raft; classic gossip).

However, the reference set is somewhat uneven: several citations are non-archival web pages or filings (Starlink FCC filing; Kuiper overview page; DARPA program pages). Some of these are unavoidable, but the manuscript would benefit from stronger anchoring in archival constellation operations literature and space networking standards/practice (e.g., CCSDS SLE/space link layers beyond Proximity-1 where relevant; DTN operational studies; LEO crosslink scheduling papers beyond HotNets-era work). Also, the “global-state mesh” is positioned as an intentional upper bound; you cite Demers gossip, but the specific fanout scaling \(f=O(N/\log N)\) is not typical for practical epidemic dissemination and should be justified more carefully (or replaced with a more standard fixed-fanout analysis plus convergence time trade).

Finally, the paper claims “no prior work provides closed-form parametric sizing relationships…” That is plausible, but the claim should be softened or supported by a more systematic comparison table against closest prior analytical sizing work in satellite network management/TT&C scaling, even if not at 10⁵.

---

## Major Issues

1. **Terminology and accounting ambiguity around “protocol overhead” vs. workload traffic (commands).**  
   Throughout (Abstract, Contributions, Table~\ref{tab:bw_breakdown}, Section~\ref{sec:workload_profiles}), \(\eta\) is sometimes described as protocol overhead and sometimes as workload-dependent traffic beyond baseline telemetry. Since the stress-case \(\eta\approx 46\%\) is dominated by commands (Fig.~\ref{fig:decomposition}), calling it “protocol overhead” is misleading. This is not just wording: it affects how readers interpret the main conclusion (“hierarchical overhead is small”).

2. **Stress-case command semantics are inconsistent with one-cycle feasibility claims.**  
   The stress-case is described as “512 B/node/cycle commands” (per-node information content), but one-cycle feasibility in Table~\ref{tab:schedulability} depends on broadcast (Type 1) which is *not* per-node unique. If stress-case is per-node unique, then one-cycle feasibility fails under the half-duplex TDMA budget. The paper needs a cleaner separation of (i) command *information volume*, (ii) addressing mode, and (iii) airtime feasibility.

3. **GE model coherence-time assumption makes retransmission ineffectiveness a modeling artifact.**  
   Section~\ref{sec:ge_link} explicitly fixes GE state within each cycle, so intra-cycle retries cannot help in bad state. This is acceptable as a conservative bound, but the paper currently uses it to argue structural ineffectiveness. You partially mitigate with the “fast-mixing vs slow-mixing” discussion, but you do not simulate or analytically treat intermediate \(\tau_c\) regimes. Given that your conclusions about retry policy and TDMA feasibility depend on this, the paper needs either (a) an added model with sub-cycle transitions, or (b) a clearer statement that the retry result is conditional and not general.

4. **Coordinator ingress capacity analysis mixes “byte-rate sizing” with “deadline/drop modeling” without fully specifying the service model.**  
   In Section~\ref{sec:coordinator_bandwidth}, Model A/B/TDMA are compared, but it is unclear what exact queueing model is assumed for the random-phase arrivals (e.g., is there a continuous server draining at \(C_{\text{coord}}\) with a hard cutoff at \(T_c\)?). The “token bucket” buffer size (25 kB) appears chosen to match “25 reports,” but the mapping from buffer to overflow probability over a cycle needs to be explicitly derived or referenced.

5. **Centralized baseline is not a communication baseline, yet appears in overhead comparison narratives.**  
   You do include disclaimers (Table~\ref{tab:topology_comparison} footnotes), but the paper still risks readers comparing hierarchical \(\eta\) vs centralized without a consistent comms accounting. Either remove centralized from bandwidth/overhead comparison plots, or add a minimal comms model for centralized uplink/downlink to make comparisons meaningful.

---

## Minor Issues

- **Eq. (unicast stagger) numeric inconsistency in available egress time.**  
  In Section~\ref{sec:coordinator_bandwidth}, you compute \(16.9/0.8\) using 0.8 s available egress, while Table~\ref{tab:superframe} states an egress window of 0.82 s and “0.80 s available” after fixed overheads—this is close, but the definition of \(\alpha_{\text{RX}}\) and subtraction of fixed overheads should be made consistent (Eqs.~\ref{eq:ingress_feasibility}–\ref{eq:egress_feasibility} vs Eq.~\ref{eq:unicast_stagger}).

- **Table~\ref{tab:bw_breakdown} appears to list “Coord. commands 512 B” as ~100 bps centralized vs ~410 bps hierarchical.**  
  This seems to imply different command rates/semantics across architectures; if so, state explicitly. If not, correct the numbers or explain the difference.

- **Global-state mesh fanout statement.**  
  The claim “With gossip fanout \(f = O(N/\log N)\)” is atypical; standard epidemic gossip uses constant fanout and yields \(O(\log N)\) rounds. If you intend an aggressive fanout to achieve one-cycle convergence, state that and justify why one-cycle convergence is required.

- **AoI sampling cadence (every 100 s) vs cycle time (10 s).**  
  In Table~\ref{tab:aoi_results} footnote, AoI is sampled every 100 s. This can bias maxima/tails unless you confirm that AoI changes only at cycle boundaries (it does, under your model) or that sampling is sufficient. A brief justification would help.

- **Reference quality.**  
  Several non-archival references are fine as context, but for a T-AES submission, consider replacing or supplementing with archival sources where possible (especially for constellation ops claims).

- **Typos/formatting:**  
  - Fig.~\ref{fig:cross_cycle_recovery} includegraphics missing file extension in LaTeX excerpt (`fig-cross-cycle-recovery` no `.pdf`), likely just an excerpt issue.  
  - Ensure consistent use of units (kbps vs kbit/s) and consistent significant figures (e.g., 9,177 ms vs 9.18 s).

---

## Overall Recommendation — **Major Revision**

The paper has a strong core idea—closed-form sizing equations plus a fast DES cross-check—and several results are potentially valuable to the community. However, key claims are currently vulnerable due to (i) ambiguous terminology/accounting around “protocol overhead,” (ii) inconsistent stress-case command semantics relative to airtime feasibility, and (iii) a correlated-loss model whose main retransmission conclusion is partly an artifact of the per-cycle coherence assumption. Addressing these issues requires substantive revision of definitions, narrative, and at least one additional sensitivity/modeling layer, but does not require a complete rethinking of the approach.

---

## Constructive Suggestions

1. **Refactor the traffic taxonomy and rename metrics to remove ambiguity.**  
   Split \(\eta\) into at least two reported quantities:  
   - \(\eta_{\text{arch}}\): architecture/control-plane overhead (heartbeats, summaries, election, sync)  
   - \(\eta_{\text{app}}\): workload/application traffic (commands, alerts) beyond baseline telemetry  
   Keep \(\eta_{\text{total}} = \eta_{\text{baseline}} + \eta_{\text{arch}} + \eta_{\text{app}}\). Update Abstract, Table~\ref{tab:bandwidth_scaling}, and Conclusions accordingly.

2. **Make command semantics first-class and propagate consistently through all tables/claims.**  
   Define a parameter for command *addressing mode* (broadcast vs per-node unicast) and a parameter for command *entropy* (unique payload fraction). Then restate stress-case as either:  
   - “broadcast stress-case” (512 B broadcast/cycle) and separately  
   - “per-node unique stress-case” (512 B/node/cycle)  
   Ensure Table~\ref{tab:bw_breakdown}, Table~\ref{tab:schedulability}, and the abstract align.

3. **Add an intermediate correlated-loss regime analysis beyond the cycle-constant GE state.**  
   Either simulate a GE chain with sub-cycle transitions (e.g., 1 s steps within \(T_c\)) or analytically bound retry success as a function of coherence time \(\tau_c\). Even a small sweep demonstrating when intra-cycle retries become effective would make Section~\ref{sec:ge_link} much more convincing and less “by construction.”

4. **Tighten and formalize the coordinator ingress sizing models (A/B/TDMA).**  
   Provide explicit derivations (or an appendix) for Model A’s quantile minimum spacing and Model B’s token-bucket overflow condition, with clear assumptions (arrival process, service model, cutoff). This will make the 21–50 kbps convergence claim in Section~\ref{sec:coordinator_bandwidth} more defensible.

5. **Either (a) add a minimal comms model for the centralized baseline or (b) remove it from overhead comparisons.**  
   If centralized is kept as a compute-queue bound only, keep it out of plots/tables that readers will interpret as bandwidth/overhead comparisons (e.g., Fig.~\ref{fig:overhead_scaling}, Table~\ref{tab:bw_breakdown}). Alternatively, add a simple centralized uplink/downlink scheduling model (even coarse) so the baseline is comparable on the comms axis.