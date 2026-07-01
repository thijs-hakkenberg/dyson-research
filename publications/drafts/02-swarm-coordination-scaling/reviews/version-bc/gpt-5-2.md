---
paper: "02-swarm-coordination-scaling"
version: "bc"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-02-27"
recommendation: "Unknown"
---

## 1. Significance & Novelty — **Rating: 4/5 (Good)**

The manuscript tackles a real and timely systems-engineering problem: how to *size* coordination communications for very large autonomous space swarms (10³–10⁵ nodes) under stringent per-node bandwidth constraints. The emphasis on “closed-form sizing relationships” plus byte-level accounting is practically valuable; many papers either stay at algorithmic complexity (big‑O) or focus on routing/ISL capacity without tying results to a concrete traffic model and a fixed per-node budget. The paper’s framing around coordinator ingress sizing, AoI tails under exception telemetry, and recovery under correlated loss is a coherent set of design questions.

Novelty is strongest in the *packaging* and synthesis: assembling queueing/AoI/Markov results into a parametric “toolkit,” and explicitly separating topology-invariant workload traffic (commands) from architecture-specific overhead (summaries/heartbeats/elections). The claim that architecture-specific overhead is ~5% while commands dominate stress-case overhead is an important insight for practitioners—*if* the command model is representative and the accounting is consistent.

That said, several results depend heavily on specific modeling choices that are not yet convincingly tied to operational reality (e.g., “one unique 512 B command per node per 10 s” as stress-case; GE coherence fixed to cycle; static membership for 1 year; coordinator egress feasibility relying on broadcast while overhead assumes per-node unicast information content). These do not negate significance, but they reduce the strength of novelty as a general result rather than a scenario-specific sizing exercise.

---

## 2. Methodological Soundness — **Rating: 3/5 (Adequate)**

The paper is commendably explicit about abstraction level (message-layer DES, cycle-aggregated) and repeatedly states that the DES is for arithmetic/implementation consistency rather than physical-layer fidelity (Section III-A and Section V-A). The traffic accounting tables are detailed, and the analytic cross-checks (e.g., AoI P99 via geometric tail in Eq. (29), hierarchical message count Eq. (5), coordinator ingress sizing) are appropriate for the stated goal: closed-form sizing relationships.

However, several methodological choices are internally inconsistent or under-specified in ways that matter for the headline conclusions:

* **Coordinator ingress vs. TDMA feasibility vs. retransmissions:** Section IV-A derives a TDMA slot model and then correctly observes that under GE steady-state, intra-cycle retransmissions make ingress exceed \(T_c\). Yet later tables (e.g., Table XXIII “Coordination Success vs Link Availability”) present delivery improvements for \(M_r=2\) under an assumption that “values assume \(M_r\) feasible,” which is *not true under the derived TDMA schedule* for \(k_c=100\). This is not just a caveat; it undermines the applicability of those success numbers to the constrained 1 kbps RF-backup regime that motivates the paper.

* **Token-bucket smoothing claim vs. timeliness:** In Section IV-A, Model B claims token carry-over “does not violate timeliness” because tokens accumulate during idle intervals, not from deferred reports. But in a per-cycle reporting model where each member sends once per cycle, the only way carry-over helps is by allowing the coordinator to accept a burst above average *within a cycle*—which still requires the instantaneous PHY schedule to support it. Token-bucket is a network-layer admission model; it does not substitute for a PHY/MAC schedule unless the PHY rate is already sufficient. The paper partially acknowledges this via TDMA, but the equivalence statement (“functionally equivalent to TDMA”) is too strong without clarifying the underlying instantaneous-rate assumption.

Reproducibility is generally good (code link, tag, parameter table), but for an IEEE T-AES submission the manuscript should more clearly map each key metric to (i) analytic equation, (ii) DES implementation, and (iii) which assumptions are required for the equation to apply (dedicated links vs shared medium; broadcast vs unicast; feasibility of retransmissions under TDMA frame-time).

---

## 3. Validity & Logic — **Rating: 3/5 (Adequate)**

Many conclusions are logically supported *within the model*: overhead is \(O(1)\) because both traffic and budget scale \(O(N)\); AoI tails under exception telemetry follow geometric inter-arrivals; GE burstiness makes intra-cycle retry ineffective by construction; coordinator ingress must scale with \(k_c S_{\text{eph}}/T_c\). The manuscript is also transparent that the “DES validates arithmetic consistency, not physical fidelity,” which is an appropriate limitation statement.

The main validity concern is that several “design recommendations” are presented as broadly applicable, while they hinge on modeling choices that are either conservative in one direction but optimistic in another:

* The headline “coordinator ingress at 21–25 kbps under TDMA” is plausible for \(k_c=100\) and 256 B reports, but the manuscript’s own TDMA timing budget leaves ~0.8 s for egress and contingencies. This margin disappears quickly if (a) ranging/control overhead is larger than assumed, (b) per-node reports are larger or include authentication, (c) more than one command/heartbeat per cycle is needed, or (d) retransmissions consume slot time (which you show they do). The paper would benefit from explicitly quantifying how much slack remains and how sensitive the 21–25 kbps recommendation is to slot overhead and egress needs.

* The “commands dominate stress-case overhead independent of topology” is true given the overhead definition (per-node information content), but the *physical feasibility* differs dramatically between broadcast and per-node unicast. The paper acknowledges unicast egress would exceed \(T_c\) (Section IV-A), but still uses the unicast-per-node stress-case as the main overhead headline. This is logically consistent for *budgeting information*, yet it risks misleading readers into thinking the system can actually deliver those commands at 1 kbps RF-backup without multi-cycle scheduling/higher PHY rate. The conclusion should more clearly separate “budget fraction” from “schedulability.”

Overall, the logic is good but would be substantially strengthened by tightening the boundary between (i) accounting identities that are always true and (ii) operationally feasible regimes under the derived TDMA constraints.

---

## 4. Clarity & Structure — **Rating: 4/5 (Good)**

The manuscript is well structured for a design-equations paper: notation table up front, clear RQs and contributions, explicit abstraction scope (Table XII), and a “Design Equations Summary” in Discussion. The repeated reminders about what \(\eta\) includes/excludes and the separation between baseline telemetry and protocol overhead are helpful and reduce ambiguity.

Figures/tables are generally effective, especially the traffic accounting tables and the workload decomposition. The AoI table (Table XVIII) includes a thoughtful methodology note about tail estimation (per-run P99 then aggregate), which is unusually rigorous for simulation papers. The “joint interaction” table is also a good idea: it tests compositionality of the sizing equations.

Clarity issues remain in a few high-impact places: (1) the paper uses “drop,” “miss,” and “loss” carefully in Section III-F, but later some tables/claims could still be misread as end-to-end reliability under TDMA; (2) the “token-bucket ≈ TDMA” phrasing is likely to confuse readers from communications backgrounds; and (3) some baselines are intentionally non-equivalent (sectorized mesh provides only local awareness), which is acknowledged, but the narrative sometimes still invites direct overhead comparisons without repeatedly reminding the reader of the functional mismatch.

---

## 5. Ethical Compliance — **Rating: 4/5 (Good)**

The manuscript includes an explicit AI-assistance disclosure in the Acknowledgment, naming models and stating that AI-assisted ideation motivated aspects of the architecture but is not validated. This is a good-faith disclosure and aligns with emerging norms.

Potential conflicts of interest are not clearly addressed: the authorship is “Project Dyson Research Team” with deferred individual names/affiliations. IEEE policy typically requires author identities at submission/review (even if anonymized for double-blind, which T-AES is generally not). If the venue requires named authors and affiliations for peer review, this needs correction. Also, the GitHub repository is run by the same organization; that is fine, but it would be good to clarify governance and long-term availability (archival DOI via Zenodo would be preferable).

No human/animal subjects are involved; the work is simulation/analysis. Ethical concerns mainly relate to transparency and reproducibility, which are mostly handled well.

---

## 6. Scope & Referencing — **Rating: 4/5 (Good)**

The topic fits IEEE Transactions on Aerospace and Electronic Systems: autonomous spacecraft operations, coordination architectures, and communication sizing under constraints. The paper is more “systems engineering + networking/queueing” than pure avionics, but that is within T-AES scope.

Referencing is broad and mostly relevant: constellation operations, DTN/CCSDS, gossip, AoI, distributed algorithms. The manuscript appropriately positions global-state mesh and centralized compute as bounds. A weakness is the reliance on several non-archival references for key context (Kuiper overview page, DARPA program pages, McDowell blog). That’s acceptable for background, but core claims (e.g., Starlink operational coordination details, “<1% operational time” optical outage regime) would benefit from more archival or standards-based citations, or at least clearer labeling as assumptions.

Also missing are some directly relevant works on (i) ISL MAC scheduling and beam hopping in LEO constellations, (ii) contact graph / deterministic outage models (Earth occlusion) beyond DTN architecture, and (iii) more recent constellation operations/conjunction automation literature. These omissions are fixable with targeted citations and a short discussion of how those results would alter \(\gamma\), \(p_{\text{link}}\), or burst models.

---

## Major Issues

1. **Schedulability vs. byte-budget conflation for commands (high impact).**  
   In Section IV-A (“Command dissemination model and overhead accounting”), stress-case assumes per-node unique 512 B commands each cycle, but TDMA feasibility analysis uses broadcast egress and notes unicast egress would exceed \(T_c\). The paper still uses the unicast stress-case to headline \(\eta\approx 46\%\). You need to explicitly separate:  
   (a) *information budget fraction* (what \(\eta\) measures), from  
   (b) *feasible delivery schedule* at 1 kbps RF-backup with half-duplex TDMA.  
   At minimum, provide a schedulability condition for per-node unicast commands (e.g., required PHY rate or multi-cycle staggering factor) and restate the stress-case as “budget upper bound, not deliverable in one cycle at 24 kbps half-duplex.”

2. **Retransmission results presented in regimes where retransmission is infeasible under your TDMA frame model.**  
   Section IV-A shows that under GE steady-state, intra-cycle retransmissions push ingress beyond \(T_c\). Yet Table XXIII reports delivery gains for \(M_r=2\) as if they are attainable. This needs restructuring: either (i) remove/relocate those results to a “non-TDMA / higher-rate PHY” regime, or (ii) incorporate slot-time feasibility directly into the success analysis (effective \(M_r\) becomes state-dependent and limited by remaining frame time).

3. **Token-bucket “carry-over” model equivalence to TDMA is overstated and can mislead.**  
   Model B (Section IV-A) implies 21 kbps suffices due to token carry-over. But if reports must arrive within-cycle, smoothing only helps if the instantaneous receive capacity and scheduling support it. Clarify what physical assumption makes Model B realizable (e.g., coordinator instantaneous PHY rate is \(C_{\text{raw}}\) and the only burstiness is random phase; token bucket approximates time-division admission). Otherwise, Model B reads like it violates the timeliness premise.

4. **Baseline comparisons are partly non-equivalent and risk over-interpretation.**  
   The paper correctly notes sectorized mesh is not functionally equivalent (local awareness only), and centralized baseline models compute only. However, several plots/tables still juxtapose overhead numbers in ways that could be read as “hierarchical beats mesh for the same function.” Consider adding a “capability matrix” (which functions each topology supports under the modeled assumptions) and ensure every cross-topology overhead comparison is explicitly conditioned on comparable function.

5. **GE model coherence assumption drives the retransmission conclusion “by construction.”**  
   You acknowledge this (Section IV-C), but the paper’s conclusion “intra-cycle retry is structurally ineffective” is only true under \(\tau_c \ge T_c\). Provide a clearer parametric condition: when does intra-cycle retry help (e.g., expected number of state transitions within \(T_c\)), and how would the design equations change? Without this, readers may overgeneralize.

---

## Minor Issues

- **Equation/variable consistency:** In Eq. (31) “Retransmission success (GE bad state): \(p_{\text{success}} = 1 - p_B^{M_r+1}\)” — earlier text uses \(p_{\text{loss}}=p_B\) and “attempts face \(p_{\text{loss}}=0.90\)”. That’s consistent, but elsewhere you use \(p_{\text{link}}\) as availability rather than loss. Consider a notation cleanup: reserve \(p_{\text{loss}}\) for erasure probability and \(p_{\text{avail}}\) for 1−loss to avoid confusion (Table XXIII mixes \(p_{\text{link}}\) with “losses”).

- **Coordinator ingress equation uses \((k_c-1)\)** in Eq. (28) but earlier text uses \(k_c\) members sending. Ensure whether coordinator is included as a member report source; currently you alternate between \(k_c\) and \(k_c-1\) (e.g., “\(k_c\) members each send” vs. TDMA uses \(k_c-1\) slots). Clarify in one sentence and apply consistently.

- **Figure file name missing extension:** `\includegraphics{fig-cross-cycle-recovery}` lacks `.pdf` unlike others; may break compilation depending on toolchain.

- **Centralized baseline server capacity choice:** Section III-B sets \(\mu_s=1000\) msg/s so \(\rho=1\) at \(N=10{,}000\). That is an intentionally tight bound, but you should justify why 1000 msg/s is representative for “processing” of a report/command pair, or emphasize more strongly that it is purely illustrative.

- **Static topology churn overhead estimate:** Section V-C claims re-association overhead ~0.3% with 2 kB seed handoff taking 16 s at 1 kbps. But if it takes 16 s, it spans >1 cycle; does it block normal reporting or is it parallel? Clarify whether this is additive traffic or displaces baseline/overhead within the same 1 kbps budget.

- **Availability numbers in Table XXII:** “Hierarchical … Graceful (99.5%)” is not clearly derived in the text; duty-cycle section mentions 99.96% per stint but then “99.5% conservatively accounts…” Provide the explicit formula/assumptions for the 99.5% so it is auditable.

---

## Overall Recommendation — **Major Revision**

The paper is promising and largely well executed as a message-layer sizing and synthesis contribution, but several core results are currently too easy to misinterpret as operationally feasible in the most constrained 1 kbps RF-backup regime. The biggest needed revision is to reconcile byte-budget overhead claims with TDMA/half-duplex schedulability—especially for stress-case per-node unicast commands and for retransmission-based reliability tables. Addressing these issues mainly requires clearer regime separation, a few additional feasibility equations, and reorganization of results rather than a complete rework of the framework.

---

## Constructive Suggestions

1. **Add an explicit “Schedulability Conditions” subsection (likely in IV-A) with two inequalities:**  
   (i) ingress frame-time feasibility (you already have Eq. (26)), and  
   (ii) egress feasibility for *broadcast vs unicast* commands, including the required PHY rate or the required multi-cycle staggering factor \(L\) such that unicast commands complete within \(L T_c\). Then restate stress-case as “requires \(L\ge \lceil k_c T_{\text{cmd}}/T_c\rceil\)” (or higher rate).

2. **Refactor retransmission analysis into two regimes:**  
   - **Regime A (frame-time allows retries):** higher PHY rate or smaller \(k_c\), where \(M_r>0\) is feasible; keep Table XXIII here.  
   - **Regime B (RF-backup TDMA at 24–28 kbps, \(k_c=100\)):** \(M_r\approx 0\) intra-cycle; rely on inter-cycle recovery only.  
   This will make the GE conclusion stronger and more defensible.

3. **Clarify coordinator ingress sizing logic by separating “average rate” from “peak/instantaneous rate”** and avoid implying token-bucket alone solves PHY burstiness. A short statement like: “Model B assumes coordinator instantaneous PHY rate equals \(C_{\text{coord}}\) and that only arrival-phase randomness causes burstiness; token bucket approximates time-division admission” would prevent misreadings.

4. **Introduce a capability/functionality matrix for the four topologies** (1 table). Columns: supports full-fleet command dissemination, supports full cluster awareness, supports local neighbor monitoring, requires global state replication, etc. Then condition overhead comparisons on comparable capabilities.

5. **Strengthen the channel/outage modeling discussion with one deterministic occlusion example** (even analytically): show how a 35 min/orbit outage maps to an effective \(p_{BG}\) (or a semi-Markov on/off model) and how it would shift the recovery/AoI tails. This can remain parametric but will connect the GE curves to a recognizable LEO phenomenon.