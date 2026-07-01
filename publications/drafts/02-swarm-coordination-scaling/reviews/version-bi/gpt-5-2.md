---
paper: "02-swarm-coordination-scaling"
version: "bi"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-02-27"
recommendation: "Unknown"
---

## 1. Significance & Novelty — **Rating: 4/5**

The manuscript targets a real and timely scaling problem: how to size and reason about coordination communications for very large autonomous spacecraft swarms (10³–10⁵ nodes) under tight per-node bandwidth budgets, including an RF “backup” regime. The paper’s core value is its attempt to provide **closed-form sizing equations** (overhead, coordinator ingress capacity, AoI tails under exception reporting, and recovery under burst losses) that practitioners can use as first-order design tools. This “design equation toolkit” framing is a meaningful contribution for early-phase architecture trades, and it is more engineering-actionable than much of the existing swarm/constellation literature, which often stays at conceptual or algorithmic levels without byte/time budgets.

Novelty is strongest in the **integration**: (i) a consistent message-layer accounting across architectures, (ii) explicit coordinator ingress sizing under burstiness with a TDMA superframe budget, (iii) AoI tail quantification tied to exception reporting probability, and (iv) GE-based inter-cycle recovery curves presented as parametric design curves. The paper is also unusually explicit about what is and is not modeled, and it provides an open-source tool/tag, which strengthens practical impact.

That said, the novelty claim in the Introduction/Abstract (“no prior work provides closed-form parametric sizing… with byte-level traffic accounting”) is plausible but currently **over-broad**. There is a body of work in satellite networking/DTN, constellation ops, and distributed systems performance modeling that provides sizing-style analyses (though not necessarily for this exact four-level hierarchy and workload). The manuscript would benefit from tightening the novelty statement to: *closed-form, byte- and cycle-budgeted sizing equations for hierarchical coordination under a specific event-driven workload and backup RF regime*, rather than implying near-absence of comparable sizing work.

---

## 2. Methodological Soundness — **Rating: 3/5**

The methodology is generally coherent for the stated goal (message-layer sizing), and the authors do a good job stating assumptions and separating baseline telemetry from “protocol overhead” via \(\eta\). The cycle-aggregated DES is appropriate for sweeping 10⁵ nodes, and the paper provides multiple analytical cross-checks (e.g., AoI P99 geometric tail in Eq. (36), coordinator ingress sizing sanity checks, Markov recovery derivation for GE). Reproducibility is aided by the stated GitHub tag and parameter tables.

However, several key modeling choices materially affect the results and are not yet methodologically “tight” enough for T-AES without further clarification/justification:

1) **Command model ambiguity (broadcast vs unicast) and its coupling to \(\eta\)**: The manuscript’s headline stress-case \(\eta_S \approx 46\%\) is driven largely by “commands,” but then the schedulability analysis shows per-node unicast is not deliverable in one cycle at 24 kbps half-duplex (22-cycle staggering, Eq. (25), Table 9). This creates a methodological mismatch: \(\eta\) is treated as “information content per node per cycle,” while the feasibility of delivering that information is time/PHY constrained. That’s acceptable as a *definition*, but then the stress-case should be framed as **not a feasible workload under the RF-backup timing model unless broadcast semantics apply** (or unless higher PHY/full duplex exists). Right now, the stress-case is simultaneously presented as an “upper bound” and used in multiple places as if it were a meaningful operating point.

2) **Coordinator ingress sizing under random phase**: The “Model A worst-case inter-arrival” argument giving ~50 kbps is not fully specified and appears to mix a continuous-time worst-case with a uniform random phase assumption. If arrivals are uniform i.i.d. phases in \([0,T_c)\), the true worst-case minimum spacing goes to 0 with nonzero probability as \(k_c\) grows; “zero-drop” under strict deadline becomes probabilistically impossible unless you define an outage probability target (e.g., 10⁻⁶). The token bucket Model B is more defensible, but then “zero-drop requires 21 kbps” depends strongly on buffer \(D\) and the assumed scheduler. This section needs a clearer stochastic formulation (e.g., “drop probability < 10⁻⁶ per cycle”) rather than “zero-drop” under random phasing.

3) **GE coherence assumption**: The GE model is intentionally conservative by holding state constant within a cycle, but then the paper uses conclusions like “intra-cycle retransmission is structurally ineffective” (Section IV-C) that are true **by construction** under that assumption. You do acknowledge this, but the design implication should be softened: retransmissions are ineffective in the *slow-mixing regime* relative to the retry spacing, not universally. The later “coherence time bounds” paragraph helps; it should be elevated earlier and integrated into the main claim.

Statistically, the bootstrap approach for P99 AoI is described carefully (Table 7 footnote), which is good. But several other reported quantities (e.g., “DES verifies overhead <0.1%”) are deterministic given the byte accounting and would not require Monte Carlo; conversely, tail recovery metrics do require careful sampling and should report CI bands (not just point P95/P99).

---

## 3. Validity & Logic — **Rating: 3/5**

Many conclusions follow logically from the defined workload and accounting. In particular: (i) \(\eta = O(1)\) under the hierarchical model is consistent with Eq. (10) and the fixed per-node budget; (ii) AoI P99 under exception telemetry matches the geometric tail (Eq. (36)); (iii) the coordinator ingress bottleneck at \(k_c=100\) and 256 B/cycle is correctly on the order of 20.5 kbps; and (iv) the half-duplex superframe budget (Table 6) is a valuable and internally consistent piece of engineering reasoning.

The main concern is that the manuscript sometimes **over-generalizes** from its specific assumptions. Examples:
- The abstract claims “commands dominate only under the stress-case upper bound” and that this is “topology-invariant given workload semantics.” This is true for the paper’s centralized command generation assumption, but in many autonomous swarms, command generation is partially decentralized (e.g., cluster-level planning), which changes both command volume and addressing (broadcast vs unicast vs multicast). The paper notes this in the Contributions, but the abstract and conclusions still read more universal than warranted.
- The statement “All equations scale linearly with bandwidth; at ≥10 kbps the coordinator bottleneck vanishes” is directionally correct for byte-rate constraints, but **not necessarily** for time-division and half-duplex constraints unless you also scale PHY rate and/or adjust \(\gamma\), turnaround, and scheduling. Some of the “vanishes” claim should be conditioned on the PHY and duplex assumptions.

Limitations are acknowledged (Section V-B), but a few are actually **central validity conditions** rather than “future work,” notably: (i) deterministic occultation/outage schedules (you mention GE is poor there), (ii) MAC contention if TDMA sync is lost (you partially address via \(\gamma\) and safe-mode), and (iii) neighbor discovery/orbital dynamics for sectorized mesh (the “oracle” is a strong assumption). The conclusions should more explicitly state: *the results are message-layer sizing bounds contingent on a TDMA-like scheduled access and on the specific command/addressing semantics.*

---

## 4. Clarity & Structure — **Rating: 4/5**

The paper is generally well organized, with a clear roadmap in Section IV and strong use of tables/figures to summarize results. The notation table is helpful, and the manuscript repeatedly restates key assumptions (1 kbps as average budget, 24 kbps PHY under TDMA, \(\gamma\) definition, baseline telemetry excluded from \(\eta\)). The TDMA superframe table is especially effective for conveying feasibility.

The abstract is information-dense and mostly accurate, but it risks being **too packed** for T-AES readers: it includes several quantitative claims (6%, 46%, 22-cycle staggering, 623 ms margin, AoI P99 440 s, GE recovery P95 4 cycles) without clearly separating what is an analytical bound vs DES result vs assumption-driven. Consider slightly restructuring the abstract into: (i) problem + architecture, (ii) main sizing equations and key numeric sizing points, (iii) validation approach and limitations.

A clarity issue arises from the overloaded use of “overhead” and “utilization.” The paper defines \(\eta\) as “protocol overhead beyond baseline,” but later uses \(\eta_{\text{total}}/\gamma\) as an “effective overhead” (Table 9). Some readers will interpret “overhead” as MAC+PHY+protocol, while others as application-layer. You do define it, but the writing would benefit from consistently using: **message-layer utilization**, **MAC efficiency**, and **PHY airtime feasibility** as separate concepts.

---

## 5. Ethical Compliance — **Rating: 4/5**

The manuscript includes an explicit disclosure that AI-assisted ideation motivated aspects of the coordinator architecture (Acknowledgment) and cites an internal/non-archival reference. This is better than many submissions and aligns with emerging transparency expectations. There is no indication of human-subjects data or other sensitive ethical issues.

Two improvements are needed for stronger compliance with IEEE/T-AES norms:
1) The AI disclosure should clarify **what** was AI-assisted (ideation only, not text generation? not data analysis? not code?) and confirm that authors verified correctness. Right now it says “motivated aspects… but is not validated here,” which could be read as ambiguous about manuscript preparation.
2) The author block currently withholds individual names/affiliations “to be provided,” which is understandable for a draft, but T-AES review typically expects author identity and conflict-of-interest checks. For peer review, this may be handled by the submission system, but the manuscript text should not suggest bypassing IEEE policy.

---

## 6. Scope & Referencing — **Rating: 3/5**

The topic is appropriate for **IEEE Transactions on Aerospace and Electronic Systems**: constellation operations, autonomous coordination, communication architecture sizing, and resilience under outages fit well. The references cover distributed algorithms (Lynch, Lamport, Raft), AoI survey papers, CCSDS standards, and constellation networking work (Handley, del Portillo, Bhattacherjee). The paper is also reasonably up-to-date through 2024–2025 in several areas.

However, the referencing has gaps and some sources are non-archival (e.g., “Project Kuiper overview,” DARPA program pages, internal Project Dyson publication). For T-AES, key operational claims (e.g., “Starlink uses centralized ground coordination,” “conjunction challenges,” “typical TCA ~24h”) should rely more on archival/peer-reviewed or official reports with stable URLs/DOIs. Also, the “sectorized mesh” heuristic based on \(\sqrt{N}\) orbital density is asserted with minimal citation; if this is original, it should be labeled as such and/or supported with a short derivation or reference to spatial point process results.

Finally, the paper frames centralized compute queueing as a baseline but explicitly does not model centralized communication overhead. That is fine as a bound, but it means RQ3 (“relative to centralized ground processing”) is only partially answered. Either add a minimal centralized comm/spectrum model (even if coarse), or narrow RQ3 to “relative to global-state dissemination and local-neighborhood mesh baselines.”

---

## Major Issues

1. **Random-phase “zero-drop” coordinator sizing is not well-posed as written (Section IV-A).**  
   The claim that “zero-drop requires ~50 kbps under worst-case inter-arrival” under uniform random phases needs a probabilistic formulation (drop probability target) or a deterministic scheduler assumption. As-is, “zero-drop under random phase” is mathematically problematic because arbitrarily small inter-arrival gaps occur with nonzero probability.  
   *Required change:* Redefine sizing as \(P(\text{drop}) \le \epsilon\) per cycle, or assume TDMA/assigned slots from the start and remove the “zero-drop under random phase” language.

2. **Stress-case command traffic mixes incompatible semantics (broadcast vs per-node unicast) while using a single \(\eta_S\) headline (Sections IV-A, IV-E; Table 9).**  
   The paper’s biggest numeric headline (\(\eta_S \approx 46\%\)) is dominated by commands, but the feasibility depends on whether those commands are broadcast (single transmission) or unique unicast (22-cycle staggering). Treating them under one “stress-case” risks misleading readers about what is operationally deliverable in the RF-backup regime.  
   *Required change:* Split stress-case into two distinct workload definitions throughout (not just Table 9): **Stress-Bcast** and **Stress-Unicast**, with separate implications for AoI, schedulability, and “upper bound” interpretation.

3. **Coordinator half-duplex airtime feasibility under loss/retransmission is internally inconsistent with the offered-load tables (Eq. (28) discussion vs Table 15).**  
   Section IV-A argues retransmissions are infeasible in the 24 kbps, \(k_c=100\) TDMA frame (ingress exceeds \(T_c\) at \(\bar{M}_r=0.18\)). Yet Table 15 presents \(M_r=2\) delivery improvements across \(p_{\text{link}}\) without clearly restricting to the regime where retries fit. You do add a “Regime A/B” note later, but the presentation still invites misapplication.  
   *Required change:* Move the “Regime A/B” constraint earlier and label Table 15 prominently as **not applicable** to the RF-backup TDMA case unless \(k_c\) or PHY rate changes.

4. **Centralized baseline is not commensurate with hierarchical/mesh comparisons for RQ3 (Sections III-B, IV-G).**  
   You compare hierarchical vs sectorized mesh at the communication layer but treat centralized only as compute queueing. This undermines the RQ3 framing and may confuse readers about what “baseline” means.  
   *Required change:* Either (a) add a coarse centralized comm model (uplink scheduling, spectrum, contact windows) or (b) rewrite RQ3 and the baseline discussion to avoid implying a full comm comparison.

---

## Minor Issues

- **Equation/parameter consistency:** In Section IV-A, TDMA sizing uses \((k_c-1)\) members; elsewhere some formulas use \(k_c\). Ensure consistent definition of whether the coordinator is included in cluster size \(k_c\) (it appears yes, hence \(k_c-1\) members). Consider adding a note in Table 1.
- **\(\gamma\) derivation vs conservative value:** Eq. (19) yields \(\gamma=0.949\) but the paper retains 0.85. This is fine, but then several “requires TDMA” conclusions depend on \(\gamma\). Consider showing sensitivity explicitly in the schedulability table (e.g., one row at \(\gamma=0.95\)).
- **Figure referencing:** Fig. 9 (“fig-cross-cycle-recovery”) lacks a file extension in LaTeX (`\includegraphics{fig-cross-cycle-recovery}`), unlike others; may break compilation.
- **Terminology:** “Protocol overhead” includes commands in several places (e.g., Table 4 breakdown, \(\eta\) definition). Many readers would not call mission commands “protocol overhead.” Consider renaming \(\eta\) to “coordination traffic fraction beyond baseline telemetry” and then sub-divide into “architecture overhead” vs “workload traffic.”
- **Sectorized mesh connectivity:** You correctly state the capped mesh is not a connected graph at cap=10. Consider moving that warning earlier (Section III-B-4) so readers don’t misinterpret it as a decentralized coordination architecture comparable in capability.
- **Citation quality:** Replace or supplement non-archival sources where possible (Kuiper overview page, internal Dyson publication) with archival/official filings, technical reports, or peer-reviewed papers.

---

## Overall Recommendation — **Major Revision**

The manuscript has strong potential and contains several valuable engineering contributions (TDMA superframe sizing, AoI tail equation validation, GE inter-cycle recovery curves, and a reproducible tool). However, multiple core claims—especially around “zero-drop” coordinator sizing under random phasing and the stress-case command model—need reframing and tighter methodological definitions to avoid misleading conclusions. With revisions that clearly separate byte-budget accounting from airtime feasibility, formalize probabilistic sizing targets, and align baselines with the stated research questions, this could become a solid T-AES paper.

---

## Constructive Suggestions

1. **Make the sizing problem probabilistic where appropriate.**  
   Replace “zero-drop under random phase” with a target such as \(P(\text{any drop in a cycle}) \le 10^{-x}\) and derive \(C_{\text{coord}}\) accordingly (order statistics of uniform phases, or a simple Chernoff/union bound). This will make the coordinator ingress sizing mathematically well-posed.

2. **Separate three layers of feasibility throughout: bytes, MAC efficiency, and airtime schedule.**  
   Present a consistent triad:  
   - message-layer utilization (\(\eta\), \(\eta_{\text{total}}\)),  
   - MAC/PHY efficiency (\(\gamma\)),  
   - TDMA airtime inequalities (Eqs. (28)–(29)).  
   Then explicitly label which results depend on which layer.

3. **Refactor workload profiles to explicitly include addressing semantics.**  
   Define workloads as tuples: \((p_{\text{exc}}, p_{\text{cmd}}, \text{cmd addressing mode})\). Carry “Stress-Bcast” and “Stress-Unicast” through all summary tables/figures and the abstract, and avoid a single stress-case headline number unless it is explicitly “information upper bound, not necessarily deliverable.”

4. **Strengthen and narrow the baseline comparisons to match RQs.**  
   Either add a minimal centralized comm model (even a coarse spectrum/contact constraint) or revise RQ3 and related text to say: “relative to global-state dissemination and local-neighborhood mesh baselines,” with centralized used only as a compute-queue bound.

5. **Add one compact “parameter-to-physics” table for the RF-backup regime.**  
   Summarize: assumed RF band, PHY rate, modulation/FEC overhead (mapped into \(\gamma\)), half-duplex turnaround, cluster diameter, and timing uncertainty. This will help aerospace readers judge whether the 24 kbps TDMA superframe is realistic across plausible hardware and geometry.