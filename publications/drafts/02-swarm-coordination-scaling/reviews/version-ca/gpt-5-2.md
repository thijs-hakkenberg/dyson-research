---
paper: "02-swarm-coordination-scaling"
version: "ca"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-02-28"
recommendation: "Major Revision"
---

## 1. Significance & Novelty  
**Rating: 4 (Good)**  
The manuscript targets a real and under-served need: *engineering sizing equations* (not just algorithms) for coordination traffic in very large space swarms (10³–10⁵). The explicit decomposition into (i) byte budget, (ii) MAC efficiency, and (iii) TDMA airtime is a useful systems-engineering framing, and the paper is unusually “design-forward” (tables, worked numbers, feasibility boundaries). The addition of CCSDS-based packet/framing validation for \(\gamma\) is a meaningful step toward practical relevance.

Novelty is strongest in the *closed-form parametric envelope* (including duty-factor \(d\)) plus the explicit *schedulability layer* showing how something can “fit in bytes” yet fail in airtime (unicast staggering). Novelty is weaker where the DES primarily replays the same accounting equations and where some baselines are not functionally comparable.

---

## 2. Methodological Soundness  
**Rating: 3 (Adequate)**  
The analytical accounting is generally sound and the three-layer feasibility approach is a good organizing principle. The slot-level TDMA simulator and the packet-level CCSDS framing model are appropriate additions and improve methodological credibility.

However, several modeling choices materially affect conclusions and need tightening: (a) the message model’s semantics (512 B “command every cycle per node” in stress) drive the headline 46% and must be more carefully justified and bounded; (b) the DES is cycle-aggregated with a fluid server and therefore cannot validate queueing/scheduling effects it abstracts away; (c) the GE coherence-time assumption (state constant over a 10 s cycle) is conservative but also pivotal for the ARQ infeasibility claim—this should be parameterized more explicitly in the *design equations* rather than treated mostly as a scenario.

---

## 3. Validity & Logic  
**Rating: 3 (Adequate)**  
Internal logic is mostly consistent, and Version CA clearly improves contextualization: the stress case is now labeled as continuous-duty upper bound and the duty factor \(d\) addresses workload realism concerns better than prior “always-on” interpretations.

Remaining validity concerns are about consistency and careful separation of “information budget” vs “airtime feasibility” throughout:
- The paper sometimes mixes “per-node 1 kbps budget” with coordinator PHY requirements in a way that can confuse readers about what is being provisioned where.
- A few equations/tables appear to use \(k_c\) vs \((k_c-1)\) inconsistently (minor numerically, but important for engineering sizing).
- The “validated \(\gamma=0.76\)” is mostly consistently applied in the TDMA feasibility narrative, but there are still places where the text uses 24 kbps feasibility language that implicitly assumes higher \(\gamma\) (or \(\gamma=1\)).

---

## 4. Clarity & Structure  
**Rating: 4 (Good)**  
The paper is well structured, with strong notation, clear sectioning, and useful summary tables (especially the feasibility layers and duty-factor table). The “claim map” is an excellent practice and helps reviewers.

Clarity issues remain in (i) baseline comparisons (centralized/mesh/sectorized) and what is and is not comparable, and (ii) what exactly is “validated” by each simulator tier (DES vs slot-level vs packet-level). Some sections are very dense with numbers; a short “how to use these equations” practitioner flow would improve usability.

---

## 5. Ethical Compliance  
**Rating: 4 (Good)**  
Open-source code/data availability is explicitly stated with a tag—this is strong. AI-assistance is disclosed. No human/animal subjects.

Two improvements needed for reproducibility norms in top-tier venues:
1) Provide a stable archival DOI (Zenodo) for the tagged release and datasets.  
2) Specify exact random seeds (or seed-generation method) per experiment in the artifact, and document how bootstrap CIs are computed (per-run vs pooled samples) in a short reproducibility appendix.

---

## 6. Scope & Referencing  
**Rating: 3 (Adequate)**  
The paper is broadly in-scope for T-AES / space systems networking. References cover distributed algorithms, DTN/space networking, AoI, and GE modeling.

Gaps: the MAC/TDMA framing would benefit from citing classic TDMA/satellite MAC and scheduling analyses (beyond CCSDS), and the queueing/aggregation model could cite more directly relevant hierarchical telemetry/aggregation work in space or WSNs (beyond LEACH). Also, several “non-archival” web references are acceptable for context but should not be load-bearing for technical claims.

---

# Major Issues

1) **Workload realism and interpretation of \(\eta_S \approx 46\%\) still needs a tighter operational mapping**  
**Why it matters:** The headline stress-case drives many conclusions (TDMA requirement, coordinator PHY sizing urgency, “commands dominate”). If the stress semantics are not plausible, the sizing guidance risks being misused. “512 B command per node per cycle” is extremely aggressive for many swarm concepts and conflates “command dissemination” with “per-node individualized actuation.”  
**Remedy:** Add a subsection that maps each workload profile (N/E/S) to *concrete mission operations* with order-of-magnitude justification: e.g., orbit-raising campaign command cadence, collision-avoidance alerting, formation reconfiguration. Provide a table translating \(p_{\text{cmd}}\), \(S_{\text{cmd}}\), addressing mode (broadcast/unicast fraction \(q\)), and duty factor \(d\) into “commands per spacecraft per hour/day.” Include at least one alternative stress definition (e.g., “cluster-level maneuver plan broadcast + occasional per-node deltas”) and show resulting \(\eta\) and Layer-3 airtime outcomes.

2) **Three-layer feasibility framework is a strong idea but needs stricter formalization and consistent use**  
**Why it matters:** The central contribution is the layered feasibility concept; it must be unambiguous for practitioners. Currently Layer 2 is “\(\eta_{\text{total}}/\gamma\)” and a heuristic “TDMA required when >50%,” while Layer 3 is explicit airtime inequalities. The boundary between Layer 2 and Layer 3 is blurry, and the “50%” rule is not derived.  
**Remedy:** Formalize each layer as a necessary condition with explicit parameters:  
- Layer 1: information-rate feasibility: \(B_{\text{msg}} \le C_{\text{node}} T_c\).  
- Layer 2: PHY-time feasibility under MAC overhead abstraction: \(B_{\text{msg}}/\gamma \le C_{\text{node}} T_c\) (or equivalent).  
- Layer 3: schedule feasibility with half-duplex partition: inequalities like (31)–(32) with explicit \(T_{\text{slot}}\), \(\alpha_{\text{RX}}\), and command addressing model.  
Then remove/justify the “50%” criterion or replace it with the actual half-duplex partition constraint (e.g., \(\alpha_{\text{RX}}\) chosen such that ingress+egress+sync+margin \(\le T_c\)). Provide a short “decision procedure” flowchart.

3) **DES verification value: currently too close to “confirms its own equations”**  
**Why it matters:** Reviewers will discount simulation results if the DES is essentially deterministic accounting with randomness only in Bernoulli generation and GE losses, especially when the DES does not implement the TDMA scheduling that is central to feasibility.  
**Remedy:** Reposition the DES as primarily (i) validating *stochastic* metrics not captured by closed forms (tail AoI under mixed workloads, drop probabilities under bursty ingress with phase staggering, distribution of recovery times across fleet), and (ii) exploring interactions that are analytically nontrivial. Concretely: add at least one result where DES produces a distribution that is not trivially implied by a single closed form (e.g., coordinator buffer occupancy distribution under duty-factor campaigns + GE bursts; tail delay under phase staggering vs random phase; sensitivity of coordinator drop probability to buffer size and burstiness). Alternatively, if you keep DES as-is, reduce its prominence and emphasize the slot- and packet-level models as the real verification.

4) **Packet-level validation: good step, but “independent validation” claim is still overstated**  
**Why it matters:** Deriving \(\gamma\) from CCSDS framing is valuable, but it does not validate the traffic model, topology assumptions, or scheduling discipline—only the MAC/PHY efficiency parameterization. The term “validation” may be challenged.  
**Remedy:** Tighten language: call it “standards-grounded parameter derivation” or “cross-check” rather than full validation. Add one additional independent check: e.g., compare derived \(\gamma\) and slot timing against a published Proximity-1 example configuration or a vendor radio timing budget (if available), or provide sensitivity bounds (min/typ/max acquisition dwell, guard time) and show how the 30 kbps conclusion holds across that envelope.

5) **\(\gamma=0.76\) unification: mostly consistent, but a few equations/tables still implicitly assume \(\gamma\approx 1\) or use mixed definitions**  
**Why it matters:** Because the key conclusion is “24 kbps infeasible, 30 kbps minimum viable,” any inconsistency in how \(\gamma\) is applied undermines trust. Also, Eq. (44) for “Coordinator ingress” in the design-equation summary omits \(\gamma\) even though earlier you correctly include it for PHY sizing.  
**Remedy:** Audit and enforce:  
- Any time you compute required PHY rate or airtime, include \(\gamma\) (or explicitly state “message-layer only, \(\gamma=1\)”).  
- In the design-equation summary, present both message-layer and PHY-layer forms:  
  \[
  C_{\text{coord,msg}} \ge \frac{(k_c-1)S_{\text{eph}}8}{T_c},\quad
  C_{\text{coord,PHY}} \ge \frac{(k_c-1)S_{\text{eph}}8}{T_c\gamma}.
  \]
- Ensure all numeric examples (20.3 kbps vs 26.7 kbps vs 27 kbps) clearly correspond to \((k_c-1)\) and to whether \(\gamma\) is applied.

6) **GE model and ARQ infeasibility: conclusions depend strongly on coherence-time; design guidance should expose this dependency more directly**  
**Why it matters:** “Intra-cycle ARQ is infeasible” is only true under slow-mixing relative to the frame; you do discuss this, but the key sizing equations don’t incorporate coherence time, and practitioners might overgeneralize.  
**Remedy:** Add a parameter \(\tau_c\) (coherence time) and define regimes explicitly in the sizing section, not only in results: per-slot vs per-cycle transition. Provide a simple bound/heuristic: expected number of independent fades per cycle \(\approx T_c/\tau_c\), and show how effective retransmission benefit scales with that. Even a coarse “ARQ benefit factor” curve would help operational use.

7) **Command addressing model: broadcast vs unicast fraction \(q\) is excellent, but it’s disconnected from the duty-factor \(d\) narrative and from AoI/latency impacts**  
**Why it matters:** Layer-3 is where the architecture “breaks” (22-cycle stagger), but the paper’s main operational realism lever is \(d\). In reality, \(d\) and \(q\) interact (campaigns may require more individualized commands).  
**Remedy:** Introduce a combined “campaign model” with \((d,q)\) and show a small 2D feasibility map: regions where (i) 1-cycle feasible, (ii) multi-cycle stagger required, (iii) infeasible. Then connect this to AoI/command latency (e.g., command completion time distribution) rather than only reporting \(L_{\text{cmd}}\).

---

# Minor Issues

1) **\(k_c\) vs \((k_c-1)\) inconsistency:** Some places use \(k_c\) in formulas but numerics appear to use \(k_c-1\). Standardize.  
2) **Eq. (45) \(\gamma\) general expression:** Units are hard to parse; \(R_{\text{PHY}}/1000\) factor suggests kbps but elsewhere you use bps. Rewrite with consistent SI units and a clear derivation.  
3) **Table 11 (Cross-model comparison):** “Analyt ingress 30 kbps = 6930 ms” conflicts with the later slot/pkt value 9078 ms; explain that the analytic number is message-layer without slot overhead/half-duplex partition, or remove the confusing row.  
4) **“TDMA required when \(\eta_{\text{total}}/\gamma>50\%\)”** appears heuristic; either justify or remove in favor of Layer-3 inequalities.  
5) **Centralized baseline:** The \(M/D/1\) compute queue is fine as a bound, but it distracts; consider moving to appendix or tightening to one paragraph since you later state communication limits dominate anyway.  
6) **Sectorized mesh comparator:** You correctly warn about functional scope, but the paper still repeatedly shows its overhead next to hierarchical; consider visually separating “non-comparable reference” from “comparable alternatives.”  
7) **AoI section:** For exception telemetry, clarify whether “AoI at coordinator” is per-node AoI aggregated across members, and whether sampling every 100 s biases tails (likely not, but state it).  
8) **Link budget table:** Provide required \(E_b/N_0\) source or at least note modulation/coding assumptions consistent with the \(\gamma\) decomposition (LDPC implies coded threshold differs from uncoded BPSK BER).  
9) **Coordinator failure probability arithmetic:** The “one event per 5,000 years per cluster” calculation should show the exact multiplication assumptions (independence, \(f_{\text{RF}}\), hazard rates).  
10) **Typos/format:** A few “\(\sim\)” and percent spacing inconsistencies; also ensure all figures have units and axes readable at IEEE column width.

---

## Overall Recommendation  
**Recommendation:** **Major Revision**

The manuscript has a strong core contribution: a practitioner-oriented sizing framework with closed-form equations, plus a compelling layered feasibility view that distinguishes byte budget, MAC efficiency, and TDMA airtime. Version CA clearly improves on key prior concerns: the campaign duty factor \(d\) now provides a realistic workload lever; the stress case is more appropriately framed as a continuous-duty upper bound; and the \(\gamma\) unification to 0.76 grounded in CCSDS framing is a substantial improvement that materially affects the coordinator PHY conclusion (24 kbps infeasible; 30 kbps minimum viable).

The main reasons for Major Revision are (i) the need to more rigorously operationalize and justify the workload model that produces the headline overhead numbers, (ii) to formalize the three-layer feasibility framework so it reads as a clean engineering method rather than a mix of heuristics and examples, and (iii) to recalibrate the role of the DES so it provides nontrivial insight beyond confirming accounting identities. Addressing these points would significantly increase the paper’s credibility and usefulness to T-AES readers.

---

## Constructive Suggestions (ordered by impact)

1) **Add an “Operational Workload Mapping” section** tying \((d, p_{\text{cmd}}, S_{\text{cmd}}, q)\) to real mission phases; include at least one alternative stress workload and show how conclusions change.  
2) **Rewrite the feasibility framework as a formal method** (necessary conditions + decision flow), eliminate the “50% TDMA” heuristic unless derived.  
3) **Audit and standardize \(\gamma=0.76\) usage everywhere**, and present message-layer vs PHY-layer formulas side-by-side in the design-equation summary.  
4) **Strengthen DES contribution** with at least one distributional result not implied by closed forms (buffer occupancy, drop probability vs buffer under bursty duty-factor campaigns, etc.).  
5) **Temper/clarify “packet-level validation” claims** and add sensitivity bounds for acquisition/guard/FEC to show robustness of the 30 kbps conclusion.  
6) **Expose coherence time \(\tau_c\) as a first-class design parameter** in the loss/ARQ guidance and include a simple regime map for ARQ usefulness.  
7) **Integrate \(d\) and \(q\) into a combined campaign feasibility map** and connect to command completion latency (not just \(L_{\text{cmd}}\)).  
8) **Tighten baseline presentation** (centralized and sectorized mesh) to reduce non-comparable side-by-side interpretation risk.  
9) **Improve equation/unit clarity** for \(\gamma\) generalization and cross-model comparisons (avoid mixed time/bit-rate abstractions in one table).  
10) **Provide archival artifact DOI and reproducibility appendix** (seeds, CI method, exact configs per figure/table).