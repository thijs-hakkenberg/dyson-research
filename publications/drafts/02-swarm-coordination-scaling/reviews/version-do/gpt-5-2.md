---
paper: "02-swarm-coordination-scaling"
version: "do"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-03-07"
recommendation: "Major Revision"
---

## 1. Significance & Novelty  
**Rating: 4 (Good)**  
The manuscript targets an important and under-served problem: *parametric* sizing of swarm/mega-constellation coordination links with byte-accurate accounting and explicit schedulability constraints. The two-test decomposition (information-byte budget vs. TDMA airtime feasibility) is a useful framing for early-phase design, and the paper’s emphasis on closed-form equations and “rate ladder” transparency is valuable for practitioners. The explicit treatment of slot efficiency via CCSDS Proximity-1 timing (rather than idealized payload/guard ratios) is a meaningful step beyond much of the conceptual swarm literature.

Novelty is incremental rather than foundational: several elements (hierarchical coordination, TDMA sizing, GE channels, AoI tails) are individually known, but the contribution lies in (i) unifying them into a coherent sizing procedure with traceable parameters, and (ii) providing a standards-grounded, validated \(\gamma\) and its impact on feasibility boundaries.

---

## 2. Methodological Soundness  
**Rating: 3 (Adequate)**  
The analytical framework is mostly sound and clearly parameterized. The CCSDS-based \(\gamma\) derivation is a strength, and the separation between Test A and Test B is conceptually appropriate. The Monte Carlo/DES is positioned as a sanity check, and the NS-3 experiment is a legitimate attempt at independent validation of MAC timing.

However, several methodological choices need tightening to meet top-tier journal expectations: (i) the GE model is used as a “what-if tool,” but the mapping from GE parameters to a plausible ISL environment remains weakly justified; (ii) the ARQ modeling in the feasibility test is simplistic (budgeting \(M_r \cdot T_\text{slot}\) rather than modeling the distribution of retransmission demand across nodes), while later sections implicitly use distributional arguments (P95 failed nodes); (iii) the feasibility threshold \(\epsilon\) and its AoI interpretation contains internal inconsistencies (see Major Issues).

---

## 3. Validity & Logic  
**Rating: 3 (Adequate)**  
The logic of the sizing chain—bytes \(\rightarrow\) coordinator ingress info-rate \(\rightarrow\) slot expansion via \(\gamma\) \(\rightarrow\) half-duplex allocation \(\rightarrow\) schedulability margin—is coherent. The manuscript is improved versus typical “back-of-the-envelope” treatments by explicitly accounting for framing, FEC expansion, acquisition, and guard.

That said, there are several internal consistency issues that undermine validity: (i) inconsistent numerical statements for \(\gamma\) in the abstract vs. tables; (ii) a likely error in the AoI/miss-probability paragraph where \(10^{-6}\) and \(10^{-4}\) are both claimed for the same \(\epsilon\); (iii) the “exactly two tests” claim is directionally right but overstated because \(\epsilon\), the ARQ policy, and the reuse factor \(R\) effectively introduce additional feasibility constraints/assumptions that must be treated as first-class.

---

## 4. Clarity & Structure  
**Rating: 4 (Good)**  
Overall organization is strong: notation table, explicit RQs, then model → feasibility framework → results → validation → discussion/limitations. The “rate ladder” table is particularly effective for readers. The manuscript is generally readable and avoids unnecessary jargon.

Clarity issues remain in a few key places: (i) the role of campaign duty factor \(d\) vs. per-cycle command probability \(p_\text{cmd}\) could be formalized more cleanly (e.g., show the implied long-run mean command rate and variance); (ii) the relationship between Test A’s “per-node 1 kbps” and coordinator ingress rate can confuse readers unless the policing/scheduling policy is stated more explicitly; (iii) the feasibility threshold \(\epsilon\) discussion is currently confusing and contains an apparent arithmetic contradiction.

---

## 5. Ethical Compliance  
**Rating: 5 (Excellent)**  
Strong reproducibility posture: code and NS-3 scenarios are claimed available with a tag; parameters and software versions are listed. AI disclosure is explicit and appropriately scoped (ideation/editing only, not results). No human/animal subjects issues.

One suggestion: include a permanent archive DOI (Zenodo) for the tagged release to meet long-term availability expectations.

---

## 6. Scope & Referencing  
**Rating: 3 (Adequate)**  
The paper fits IEEE TAES / ASR scope (space systems communications + autonomy). Referencing is acceptable but not yet “top-tier complete” for MAC/TDMA scheduling and AoI/real-time networking. DVB-RCS2 is a good cross-standard anchor.

Gaps: more direct engagement with (i) space TDMA/return-link scheduling literature (beyond DVB-RCS2), (ii) deterministic real-time schedulability/network calculus as a comparator (you cite Le Boudec/Thiran but do not leverage it), and (iii) AoI under correlated losses / burst errors and its coupling to periodic scheduling.

---

# Major Issues

1. **AoI / deadline-miss probability paragraph contains a numerical inconsistency (likely an error) and weakly justified mapping from \(\epsilon\) to safety.**  
   - **Why it matters:** This paragraph is used to justify the central feasibility target (\(\epsilon = 1\%\)) and therefore influences the headline 30 vs. 35 kbps recommendation. If the AoI tail argument is wrong or unclear, the engineering justification for \(\epsilon\) is undermined.  
   - **Evidence:** You state \(P(\text{AoI} > 3T_c) = \epsilon^3\). For \(\epsilon=0.01\), \(\epsilon^3=10^{-6}\), but later you write “At \(\epsilon=0.01\): \(P(\text{AoI} > 30\text{s})=10^{-4}\)”—contradictory.  
   - **Remedy:** Correct the arithmetic and rewrite the section to (i) clearly define what constitutes a “deadline miss” (slot overrun? packet failure? both?), (ii) state the independence assumption explicitly, and (iii) provide a short sensitivity table mapping \(\epsilon\) to \(P(\text{AoI}>mT_c)\) for \(m=\{2,3,5\}\). For GE correlation, provide the corresponding bound/approximation consistently.

2. **\(\gamma\) “unification” is not fully consistent across the manuscript (0.73–0.76 vs. 0.732/0.745/0.761; abstract vs. tables).**  
   - **Why it matters:** \(\gamma\) is the key conversion between byte budget and airtime feasibility. Inconsistency invites reviewer skepticism that different sections used different \(\gamma\) (or earlier 0.85) values, which would change the 30/35 kbps boundary.  
   - **Remedy:** Add a single “authoritative” definition: \(\gamma_C(R_\text{PHY}, S, R_\text{FEC}, O_\text{frame}, T_g, T_a)\). Then ensure every numeric claim references the same configuration (Model C). In the abstract, report the specific values used for 30 and 35 kbps (e.g., \(\gamma_{30}=0.745\), \(\gamma_{35}=0.732\)) rather than a range. Audit all places where “0.76 validated via CCSDS” is implied; ensure no residual 0.85-based numbers remain.

3. **The “three-layer feasibility framework” is described as two tests, but in practice there are additional binding assumptions that behave like separate constraints (ARQ policy, \(\epsilon\), spatial reuse \(R\)).**  
   - **Why it matters:** Over-claiming “exactly two tests” risks conceptual pushback: practitioners will treat ARQ feasibility and reuse feasibility as separate gates. Also, Algorithm 1 effectively performs multiple checks (ingress+egress, then ARQ, then stagger).  
   - **Remedy:** Reframe as: **(i)** Test A: byte budget, **(ii)** Test B: per-cluster TDMA schedulability *given* reliability target \(\epsilon\) and ARQ policy, **(iii)** Fleet-level reuse constraint (conditional). You can still emphasize that \(\gamma\) is not a separate test. But be explicit that \(\epsilon\), ARQ choice, and reuse factor are design requirements/assumptions that must be set.

4. **ARQ time budgeting in Algorithm 1 is too coarse and partially inconsistent with later distributional reasoning (P95 failed nodes).**  
   - **Why it matters:** The feasibility boundary between 30 and 35 kbps is driven by margin vs retransmission demand. If the ARQ model is “\(M_r T_\text{slot}\)” (one slot’s worth), it under-represents the fact that multiple nodes may require retransmission in the same cycle, which you later acknowledge by computing expected/P95 failed nodes.  
   - **Remedy:** Make the ARQ component in Test B explicitly **stochastic**: define \(X\) = number of members requiring retransmission(s) in a cycle; then \(T_\text{ARQ}=X \cdot T_\text{slot}\) (or with minislot ACKs etc.). Provide either (a) a closed-form approximation for \(P(T_\text{ing}+T_\text{egr}+T_\text{ARQ}>T_c)\) under i.i.d. loss and under GE slow-fading, or (b) explicitly state that ARQ feasibility is assessed via the slot-level simulator and the analytic test uses a conservative percentile (e.g., \(X_{0.95}\)). Align Table IX and the algorithm accordingly.

5. **Campaign duty factor \(d\) improves realism, but the mapping to operational workloads is still not sufficiently evidenced; the “<1% of operational time” claim is asserted rather than derived.**  
   - **Why it matters:** A central concern in prior versions (as you note) is workload realism. \(d\) is a good abstraction, but reviewers will ask whether the chosen \(d\) values correspond to real mission operations, and whether the stress case is truly an “upper bound” rather than a strawman.  
   - **Remedy:** Provide a short derivation for the “<1%” statement using your Table VI examples (station-keeping + CA + campaigns). For example, compute an annualized duty factor bound from event rates and durations, or cite operations literature for commanding cadence. Also clarify whether \(d\) gates only *command bytes* or also coordinator processing load and scheduling overhead (it appears to gate command bytes only).

6. **DES verification adds limited scientific value as currently positioned (“reproduces analytical means <0.1%”).**  
   - **Why it matters:** Top-tier venues expect simulation to test regimes where analysis is approximate or assumptions break, not merely confirm algebra. Right now the DES reads as a self-check, which is fine, but it occupies methodological space without yielding new insight.  
   - **Remedy:** Either (a) reduce DES discussion to a brief implementation-validation note, or (b) use DES to validate something nontrivial: e.g., queueing at coordinator (\(M/D/c\) mention), bursty arrivals from exception reporting, or the interaction of staggered unicast commands with periodic ingress. If DES can produce distributions (AoI, backlog, deadline misses) under non-i.i.d. workloads, show that.

7. **NS-3 validation is a positive step, but the independence claim would be stronger if you validated an *observable* beyond \(\gamma\) and feasibility boundary, and if you controlled for model mismatch more systematically.**  
   - **Why it matters:** Validating \(\gamma\) is helpful, but \(\gamma\) is itself partly a definition of how you account for overhead. The stronger question is whether the *end-to-end schedulability and miss probability* under realistic timing jitter and loss matches the analytical/sizing prediction.  
   - **Remedy:** Expand Section IV-J with: (i) a table of measured components from NS-3 (mean/variance of acquisition time, realized slot duration distribution, observed \(\gamma\) decomposition), (ii) a direct comparison of predicted vs observed superframe margin consumption, and (iii) a sensitivity run where you set NS-3 framing to 104 bits (or modify analytical to 88 bits) to show the boundary is invariant. If possible, add a second topology (e.g., two clusters sharing a channel) to partially exercise reuse/interference assumptions.

8. **Fleet-level reuse factor \(R\) is acknowledged as provisional, but the paper’s broader “\(10^5\) nodes” framing depends heavily on it.**  
   - **Why it matters:** Per-cluster sizing is solid, but the paper positions itself as addressing \(10^3\)–\(10^5\) nodes. Without even a coarse interference/reuse analysis, the fleet-level extrapolation may be viewed as speculative.  
   - **Remedy:** Keep the per-cluster results as primary (good), but either (i) soften claims about fleet scale in the introduction/abstract, or (ii) add a simple geometric/interference model (e.g., reuse distance vs beamwidth vs orbital separation) yielding plausible \(R\) ranges with citations, plus a sensitivity plot of \(G\) vs \(R\) and \(f_\text{RF}\).

---

# Minor Issues

1. **Abstract \(\gamma\) range:** states “\(\gamma \approx 0.73\)–0.76” but later table gives 0.732–0.761; consider reporting exact \(\gamma_{30}\), \(\gamma_{35}\).  
2. **Feasibility threshold paragraph:** rewrite for clarity; define whether “deadline miss” includes PHY loss or only TDMA overrun.  
3. **Equation (unicast stagger) consistency:** Eq. (20) uses \(T_c(1-\alpha_{RX})\) while Algorithm line 14 uses \(T_c - T_{ing}\); reconcile and ensure egress time subtraction is consistent.  
4. **Table VIII superframe:** ACK mini-slots are labeled RX; but ACKs are typically coordinator TX and member RX (unless you mean member ACKs). Clarify directionality and who transmits ACKs.  
5. **GE parameter grounding:** you cite Lutz for LMS; for ISL, justify why \(p_B=0.90\) is conservative but still relevant, or provide a second “ISL-likely” parameter set.  
6. **Baseline 20.5% telemetry:** briefly show how 20.5% is computed (bytes/cycle and 1 kbps budget) to avoid appearing as a magic constant.  
7. **“Coordinator ingress demands ≈27 kbps PHY-rate”**: this is specifically at 30 kbps with \(\gamma_{30}\); clarify dependence and avoid implying it is universal.  
8. **Typographic/consistency:** ensure all figures have file extensions consistent (Fig. 9 uses `fig-cross_cycle_recovery` without `.pdf`).  
9. **Citations:** add references for Proximity-1 framing practice “framing bits are FEC-encoded per CCSDS practice” (you cite prox1, but sometimes CCSDS sync/coding is the stronger anchor).  
10. **Algorithm 1:** specify termination condition / step size for increasing \(R_\text{PHY}\) (rate ladder? discrete modem rates?).

---

## Overall Recommendation  
**Recommendation:** **Major Revision**

The paper has a strong practitioner-oriented core: a clear sizing framework, standards-based slot efficiency accounting, and a credible conclusion that ~35 kbps is a robust conservative design point for the stated assumptions. The introduction, notation, and rate-ladder presentation are effective, and the explicit incorporation of campaign duty factor \(d\) is a meaningful improvement toward workload realism. The NS-3 validation is also a step in the right direction and is closer to “independent validation” than many papers manage.

However, several issues prevent acceptance in a top-tier aerospace systems journal in the current form. Most critically: the reliability/AoI justification for \(\epsilon\) contains an apparent numerical error and conceptual ambiguity; the ARQ feasibility modeling is not aligned between the algorithm and the later stochastic/P95 argument; and the “two tests only” framing overreaches given the additional constraints (ARQ policy, \(\epsilon\), reuse \(R\)). These are fixable, but they require careful revision to ensure internal consistency and to strengthen the scientific defensibility of the feasibility boundary and headline recommendations.

---

## Constructive Suggestions (ordered by impact)

1. **Fix and strengthen the \(\epsilon\) → AoI tail justification** (correct arithmetic; define miss events; provide a compact sensitivity table and a correlated-loss counterpart).  
2. **Make ARQ schedulability explicitly stochastic and consistent** across Algorithm 1, Table IX, and the P95 retransmission-demand argument; consider a percentile-based analytic bound or clearly delegate ARQ feasibility to the slot-level simulator.  
3. **Audit and unify \(\gamma\) usage everywhere** (abstract, tables, equations, narrative) with a single authoritative parameter set (Model C) and explicit \(\gamma_{30}, \gamma_{35}\).  
4. **Reframe feasibility as per-cluster + conditional fleet-level reuse**; soften fleet-scale claims or add a minimal reuse/interference model to justify plausible \(R\).  
5. **Elevate NS-3 validation from “\(\gamma\) matches” to “time budget/margin consumption matches”** by reporting measured slot-time distributions and comparing predicted vs observed superframe utilization.  
6. **Either reduce DES to a brief implementation check or use it to test nontrivial regimes** (bursty exception reporting, coordinator queueing/backlog, stagger interactions).  
7. **Make the duty factor \(d\) mapping defensible** with a short quantitative derivation for the “<1% stress” statement and clarify what operational processes are/are not gated by \(d\).  
8. **Clarify ACK directionality and superframe signaling details** to avoid confusion about who transmits what in which phase.  
9. **Add a short derivation for the 20.5% baseline** and ensure all “magic numbers” are traceable.  
10. **Add archival reproducibility (DOI) for code/data** and ensure the tagged release contains scripts to regenerate key tables/figures and NS-3 runs.

If these revisions are made carefully, the work could become a solid, publishable reference for early-stage coordination-link sizing in hierarchical swarms.