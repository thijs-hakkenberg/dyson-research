---
paper: "02-swarm-coordination-scaling"
version: "ct"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-03-04"
recommendation: "Major Revision"
---

## 1. Significance & Novelty  
**Rating: 4 (Good)**  
The manuscript’s core contribution—closed-form, *byte-accounted* sizing equations for hierarchical coordination, explicitly separating (i) message-layer byte budget utilization \(\eta\) from (ii) physical/MAC-layer TDMA schedulability via \(\gamma\)—is valuable and relatively rare in the swarm/constellation literature. The “rate ladder” and the consolidated feasibility procedure (Algorithm 1) are practitioner-oriented and, if correct and consistently applied, could become a useful early-phase sizing reference.

That said, the novelty is primarily in *integration and parameterized synthesis* rather than in new theory. The paper is strongest as a design-note / engineering sizing framework; it is weaker as a validated performance claim for real ISLs.

---

## 2. Methodological Soundness  
**Rating: 3 (Adequate)**  
The two-layer framework (byte budget + TDMA airtime) is a sound modeling decomposition for early design. The authors are appropriately explicit that DES is Tier-1 verification, not external validation, and that \(\gamma\) is standards-anchored rather than measured.

However, several methodological gaps reduce confidence in the quantitative recommendations: (i) the DES is “cycle-aggregated” and largely algebraic accounting; (ii) the slot-sim is used to support key feasibility claims but mixes Model S and Model C in a way that can confuse what is actually proven; (iii) the GE process is defined at the cycle timescale, which structurally predetermines the “ARQ is ineffective intra-cycle” conclusion; and (iv) the “three-layer feasibility” narrative is not always internally clean (see Major Issues).

---

## 3. Validity & Logic  
**Rating: 3 (Adequate)**  
The paper is generally internally consistent, and Version CT is notably improved in transparency: the duty factor \(d\) is now explicitly framed as episodic, \(\gamma\) is re-anchored to CCSDS Prox-1 with rate dependence, and the “stress case” is labeled as a continuous-duty upper bound.

Remaining logic issues are mostly about boundary conditions and double-counting risks:
- The relationship between \(\gamma\), \(\alpha_{\mathrm{RX}}\), and the airtime test is sometimes presented as if it were multiple tests, despite the boxed guidance saying not to double-count.
- Some feasibility statements depend critically on schedule assumptions (e.g., fixed per-cycle slot allocations, ACK-in-guard, reserved ARQ slots) that are not fully justified as implementable under Prox-1-like radios.

---

## 4. Clarity & Structure  
**Rating: 4 (Good)**  
The paper is well organized, with strong “roadmap” signposting, good notation discipline, and helpful tables (Rate Ladder, Feasibility, \(\gamma\) decomposition). The explicit disclaimer of Model S vs Model C is a major improvement relative to typical confusion in such work.

Clarity still suffers in a few places:
- The feasibility framework is described as “two-layer” but later effectively becomes “2 + ARQ sublayer + unit conversion,” which risks reader misinterpretation.
- Some critical parameters (e.g., \(\alpha_{\mathrm{RX}}\), ACK placement, acquisition model) are explained, but the *operational plausibility* of these assumptions is not fully defended.

---

## 5. Ethical Compliance  
**Rating: 5 (Excellent)**  
Strong: code and data availability with a tag; explicit statement of no external validation; explicit AI disclosure (scope-limited to ideation/editing). This is exemplary for reproducibility norms.

---

## 6. Scope & Referencing  
**Rating: 4 (Good)**  
The manuscript cites relevant constellation/networking/swarm and CCSDS references, plus AoI and GE channel modeling. It is appropriate for T-AES / Adv. Space Res. in topic.

Two gaps:
- TDMA/DAMA and satellite MAC literature beyond DVB-RCS2 is thin (e.g., LEO ISL MAC studies, CCSDS Prox-1 implementation papers, or recent smallsat crosslink modem timing reports).
- The paper leans heavily on Prox-1 framing but does not clearly reconcile Prox-1’s actual operational modes with the proposed superframe/slotting (e.g., burst acquisition assumptions, ranging integration, ACK semantics).

---

# Major Issues

1) **The “three-layer feasibility framework” is not fully sound as presented (risk of double-counting and conceptual drift).**  
**Why it matters:** The paper claims a clean decomposition: Layer 1 byte budget (\(\eta\)) and Layer 2 airtime schedulability (TDMA time using \(\gamma\)). But in multiple places the narrative introduces \(C_{\text{raw}}=C_{\text{info}}/\gamma\) and \(R_{\text{PHY,min}}=C_{\text{info}}/(\gamma\alpha_{\mathrm{RX}})\) as if they are additional feasibility layers. Readers can easily misapply the method (e.g., check byte budget, then multiply by \(1/\gamma\), then also run airtime, effectively penalizing twice).  
**Specific remedy:**  
- In Section IV-A and Section V-C, rewrite the framework as **exactly two feasibility tests**:  
  - **Test A (bytes):** \(\eta_{\text{total}}\le 1\).  
  - **Test B (airtime):** \(T_{\text{ing}}(R_{\text{PHY}},\gamma)+T_{\text{egr}}(R_{\text{PHY}},\gamma)+T_{\text{ARQ}} \le T_c\).  
- Present \(C_{\text{info}}\to C_{\text{raw}}\to R_{\text{PHY}}\) explicitly as **a design heuristic / lower bound** derived from Test B under simplified assumptions, not as a separate “layer.”  
- Add a short “common mistakes” box: *do not apply both \(R_{\text{PHY,min}}=C_{\text{info}}/(\gamma\alpha)\) and also separately compute ingress slots using \(\gamma\); they are algebraically connected.*

2) **\(\gamma\) unification (0.76 CCSDS-anchored, rate-dependent) is mostly improved but not consistently enforced across all claims/tables.**  
**Why it matters:** The manuscript emphasizes “all recommendations use Model C,” yet Table IV-D (joint interaction) uses Model S timing and includes 24 kbps results that can be misread as contradicting the “24 kbps infeasible” conclusion. Also, some earlier equations/phrases still give the impression of a fixed \(\gamma\) (or mix \(\gamma_{24}\) and \(\gamma_{30}\)) when computing capacity vs schedulability.  
**Specific remedy:**  
- Move Table \ref{tab:tdma_joint_interaction} to an appendix or visually quarantine it (e.g., gray background + “illustrative only”), and **remove** 15/20 kbps rows (they are non-actionable and amplify confusion).  
- In every place you compute a numeric rate, annotate the exact \(\gamma(R_{\text{PHY}})\) used. For example, in Eq. \(\ref{eq:tdma_capacity}\) you cite \(\gamma_{C,24}\) but then discuss 30 kbps feasibility; ensure the example uses \(\gamma_{30}\) when discussing 30 kbps.  
- Add a single “\(\gamma\) lookup” table (already partly present) and require all numeric examples to reference it.

3) **Campaign duty factor \(d\) is a good addition, but workload realism is still under-argued and could be misused.**  
**Why it matters:** \(d\) is doing heavy lifting to reconcile a high stress utilization (\(\eta_S\approx 46\%\)) with “routine operations” (\(\eta\approx 5\)–10%). Without a clearer mapping from mission operations to command-generation processes, \(d\) can become a free parameter that makes any design look feasible. Also, the distinction between \(d\) (campaign gating) and \(p_{\text{cmd}}\) (within-campaign probability) is easy to muddle.  
**Specific remedy:**  
- Provide at least one **fully specified** workload model (e.g., ON/OFF Markov-modulated command process) with parameters tied to a concrete scenario (orbit raising, station-keeping, collision response), and show how it implies a particular \(d\) and burst length distribution.  
- Clarify whether “routine \(\eta\approx 5\)–10%” assumes \(p_{\text{cmd}}=1\) during ON windows or smaller \(p_{\text{cmd}}\). Right now, both appear in different places.  
- Add a sensitivity plot: \(\eta\) vs \((d, p_{\text{cmd}}, S_{\text{cmd}})\) to show what combinations produce \(\eta\in[5,10]\%\).

4) **The stress-case \(\eta_S\sim 46\%\) is now labeled as episodic/upper bound, but the operational contextualization remains incomplete.**  
**Why it matters:** Even if it is “<1% of time,” the *system must still remain safe* during those periods. High utilization interacts with (i) unicast staggering delays, (ii) AoI tails, (iii) coordinator buffer overflow risk, and (iv) loss recovery. The manuscript states “degrades gracefully” but does not quantify worst-case coordination latency/AoI under the stress bursts with GE losses and without intra-cycle ARQ.  
**Specific remedy:**  
- Add a table reporting worst-case (or P99) **command completion time** and **AoI** during stress bursts for both broadcast and unicast, under the slow-mixing GE case (inter-cycle recovery).  
- Explicitly state the *control authority* expected over the RF coordination channel during stress (e.g., “not for closed-loop control”), and connect that to acceptable delays (you partially do this; make it quantitative and central).

5) **DES “verification value” remains limited; distributional claims need stronger separation from algebraic accounting.**  
**Why it matters:** You correctly state DES matches closed-form means “by construction,” but then use DES to support buffer sizing rules (e.g., 1.30× mean). That can be valuable, but only if the arrival process and service process are defined independently enough to produce nontrivial tails. As written, much of the DES appears to be deterministic per-cycle generation plus a campaign gate—so the tail results may be largely an artifact of the assumed ON/OFF model rather than an emergent property of the architecture.  
**Specific remedy:**  
- Make the coordinator ingress queue model explicit: what is the service rate in bytes/s? is service continuous or slotted? is there per-cycle batching?  
- Validate the buffer rule against at least one alternative stochastic process (e.g., MMPP with same mean and duty factor but different burstiness), showing robustness of the 1.30×/1.50× heuristics.  
- If you cannot, downgrade the buffer rule from “rule” to “illustrative example under assumed ON/OFF parameters.”

6) **Packet-level validation (Section IV-J) is not independent validation; this is acknowledged, but the manuscript still risks overstating confidence in \(\gamma\).**  
**Why it matters:** The key design recommendation (30 kbps min, 35 kbps recommended) hinges on \(\gamma\) and acquisition/guard assumptions. Section IV-J uses CCSDS nominal framing and assumed \(T_{\text{acq}}\), \(T_{\text{guard}}\). This is parameter anchoring, not validation. The paper is mostly honest about this, but the recommendation language is still strong.  
**Specific remedy:**  
- Rephrase “confirms 35 kbps as recommended design point” to “**implies** 35 kbps under assumed \(T_{\text{acq}},T_{\text{guard}},R_{\text{FEC}}\); measured modem timing could shift by X kbps.”  
- Add a small “what to measure” checklist for practitioners: \(T_{\text{acq}}\) distribution, turnaround time, effective guard needed, framing overhead actually used, and achieved \(\gamma\) under Doppler.

7) **Generalized \(\gamma\) expression is useful, but practitioner usability would improve with a clearer recipe and constraints.**  
**Why it matters:** Eq. (45) is a good generic time-domain \(\gamma\), but practitioners need to know (i) which overhead terms are FEC-encoded vs not, (ii) how ACKs/ranging fit, and (iii) how to handle continuous tracking vs burst reacquisition. Currently these are scattered.  
**Specific remedy:**  
- Provide a compact “\(\gamma\) recipe” subsection: define which bits are encoded, where acquisition happens (per slot/per burst/per superframe), and explicitly include optional terms (ACK, ranging) as add-ons.  
- Provide a worked example for 30 and 35 kbps showing all intermediate times (not just the final \(\gamma\)).

---

# Minor Issues

1) **Table \ref{tab:tdma_joint_interaction}**: Even with the warning, it remains easy to misread. Consider moving to appendix and/or renaming to “Illustrative ARQ×TDMA coupling under optimistic timing (Model S).”

2) **Eq. \(\ref{eq:tdma_capacity}\)**: numeric example uses \(\gamma_{C,24}\) but text around it discusses 30 kbps feasibility; tighten the alignment.

3) **ACK-in-guard assumption** (Table \ref{tab:superframe} footnote): this is a nonstandard-looking trick. It may be feasible, but you need a clearer timing diagram or justification that it does not erode jitter margin in worst case.

4) **\(\alpha_{\mathrm{RX}}\)**: You state it is derived from schedule; good. But Algorithm 1 line 15 uses \(T_c-T_{\text{ing}}\) for unicast stagger while earlier you use \(T_c(1-\alpha_{\mathrm{RX}})\). Make the definitions consistent and show equivalence.

5) **Fleet reuse factor \(R\)**: currently an “order-of-magnitude” claim; fine, but the paper would benefit from a single sentence stating that *all fleet-scale numbers are illustrative* and that the validated unit is per-cluster.

6) **Terminology**: “byte budget” vs “utilization” vs “overhead” sometimes conflates baseline telemetry exclusion. Consider a one-line reminder near key plots/tables: “\(\eta\) excludes baseline 20.5%.”

7) **References**: consider adding at least one citation on burst-mode acquisition times / smallsat S-band crosslink modem performance if available (even vendor app notes, if archival is impossible).

---

## Overall Recommendation  
**Recommendation:** Major Revision

The manuscript is a strong and substantially improved engineering sizing framework with good transparency about assumptions and validation gaps. The separation into \(\eta\) (message-layer byte accounting) and \(\gamma\) (TDMA slot efficiency) is a meaningful contribution, and the CCSDS-grounded, rate-dependent \(\gamma\) treatment is a clear step forward. The duty factor \(d\) also directly addresses prior workload realism concerns by explicitly parameterizing episodic operations and reframing the 46% stress case as a continuous-duty upper bound.

The main reasons for Major Revision are (i) the feasibility-framework presentation still risks conceptual misuse (double-counting and “extra layers”), (ii) the key quantitative recommendation (30 kbps min / 35 kbps recommended) depends on assumptions about acquisition/guard/ACK placement that need tighter justification and clearer practitioner guidance, and (iii) the DES/slot-sim validation story needs refinement so the reader can distinguish what is emergent vs what is “equations confirming themselves.” Addressing these issues would substantially increase the paper’s credibility and usefulness to T-AES readers.

---

## Constructive Suggestions (ordered by impact)

1) **Refactor the feasibility framework into two tests + optional ARQ add-on**, and rewrite the rate ladder as a *derivation/heuristic* consistent with the airtime test (eliminate any “third layer” interpretation).

2) **Enforce Model C consistently** in all decision-relevant sections; quarantine Model S results to an appendix and use them only to illustrate coupling phenomena.

3) **Strengthen the operational grounding of \(d\)** with one concrete, parameterized workload model and show how it maps to \(d\), \(p_{\text{cmd}}\), and burst lengths; add sensitivity over \((d,p_{\text{cmd}})\).

4) **Quantify worst-case coordination QoS during stress bursts** (AoI and command completion time) under slow-mixing GE with inter-cycle recovery (since intra-cycle ARQ is often infeasible at 30 kbps).

5) **Make the \(\gamma\) recipe more implementable**: explicitly include optional timing terms (ACK, ranging), clarify what is FEC-encoded, and provide intermediate calculations for 30/35 kbps.

6) **Upgrade the DES tail/buffer section** by testing robustness to at least one alternative burstiness model, or clearly label the buffer multipliers as conditional on the assumed ON/OFF process.

7) **Add a “measurement checklist” for external validation** (what parameters to log from a modem and how they map into \(\gamma\), GE parameters, and schedule feasibility).