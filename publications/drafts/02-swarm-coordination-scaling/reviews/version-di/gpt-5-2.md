---
paper: "02-swarm-coordination-scaling"
version: "di"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-03-06"
recommendation: "Major Revision"
---

## 1. Significance & Novelty  
**Rating: 3 (Adequate)**  
The paper’s main contribution is a *design-oriented* “two-test” feasibility framework (byte budget + TDMA airtime) with closed-form sizing equations for per-cluster hierarchical coordination, plus a standards-anchored slot-efficiency parameterization \(\gamma(R_{\text{PHY}})\) and a rate-ladder that turns message assumptions into a PHY-rate recommendation (30 kbps min / 35 kbps recommended). This is useful as a preliminary sizing guide and as a structured way to avoid common “1 kbps per node” fallacies (average budget vs burst ingress).  

However, novelty is limited by (i) heavy reliance on deterministic accounting, (ii) absence of external validation, and (iii) the fact that many components (TDMA airtime checks, GE what-if, AoI under geometric sampling) are known individually. The manuscript’s novelty is primarily in *integration and packaging* for practitioners, not in new theory.

---

## 2. Methodological Soundness  
**Rating: 3 (Adequate)**  
The methodology is internally consistent: a message-layer accounting model, a slot-time model with explicit overheads, and a slot-level simulator to explore ARQ×TDMA coupling. The separation between Test A (information bytes) and Test B (airtime) is a sensible engineering decomposition.  

Key weaknesses are: (i) the DES is largely a bookkeeping engine that shares assumptions with the equations; (ii) the slot simulator appears deterministic aside from loss, and does not model realistic MAC dynamics (capture, timing jitter distributions, missed acquisitions, or sync loss); (iii) the GE model is explicitly not calibrated, which is acceptable for sensitivity studies but then cannot support strong rate recommendations unless the recommendation is framed as conditional. The paper *does* try to frame results as conditional, but occasionally slips into definitive language.

---

## 3. Validity & Logic  
**Rating: 3 (Adequate)**  
Overall logic is good: the “1 kbps logical allocation” vs “coordinator must ingest sequential bursts” point is correct and important. The stress-case \(\eta_S \approx 46\%\) is now more clearly contextualized as a continuous-duty upper bound and you provide a duty-factor mixture argument (<1% time), which addresses realism concerns better than earlier versions typically do.

Remaining validity concerns:  
- Some parameter choices (e.g., per-slot cold-start acquisition every burst, guard sizing, ACK handling, retransmission slot provisioning) dominate conclusions, yet are treated as “reasonable.” They may be reasonable, but the paper needs to be explicit about which are *contractual requirements* vs *design choices*.  
- The three-layer feasibility narrative (byte budget, MAC efficiency/slot efficiency, and TDMA airtime) is mostly sound, but you must be careful: \(\gamma\) is not “MAC efficiency” in the usual sense; it is a *PHY/slot overhead factor*. If you call it MAC efficiency, readers will expect contention/collision behavior, which is explicitly out of scope. You partially address this, but terminology still risks confusion.

---

## 4. Clarity & Structure  
**Rating: 4 (Good)**  
The manuscript is unusually explicit about definitions (\(\eta\) vs baseline, what \(\gamma\) is/is not, what is validated vs parameterized). The rate ladder (Table “Rate Ladder”) and the superframe budget table are strong, decision-relevant artifacts. The “claim map by evidence tier” is also a good practice and helps the reader calibrate trust.

Clarity issues remain: (i) the paper is long and sometimes repetitive (multiple places restate that \(\gamma\) is not a separate test); (ii) some key equations are scattered (e.g., where exactly \(\alpha_{\text{RX}}\) changes with \(M_r\) and egress); (iii) some claims about feasibility boundaries are stated globally while they are actually conditional on \(k_c=100, S=256\)B, \(T_c=10\)s, and the specific slot contract.

---

## 5. Ethical Compliance  
**Rating: 4 (Good)**  
The paper includes a data/code availability statement with a repository tag, environment details, and an explicit AI-use disclosure. That is above-average for the field.  

Two items to tighten:  
- Ensure the repository contains (a) exact scripts to regenerate each figure/table, (b) frozen dependency environment (e.g., `requirements.txt`/`poetry.lock`/`uv.lock`), and (c) deterministic seeds per experiment. You mention “sequential seeds,” but reviewers will look for exact reproducibility.  
- If any non-archival sources (e.g., vendor typical TCXO drift, acquisition assumptions) influenced quantitative margins, document them more formally (even as engineering assumptions with ranges).

---

## 6. Scope & Referencing  
**Rating: 3 (Adequate)**  
Referencing is broad (CCSDS, DVB-RCS2, AoI, distributed systems, constellation networking). The CCSDS anchoring is appropriate for T-AES / Adv. Space Res.  

Gaps:  
- TDMA/return-link scheduling literature beyond DVB-RCS2 (e.g., demand-assigned TDMA, MF-TDMA, satellite random access vs scheduled access comparisons) could be cited to position the scheduling assumptions and to justify why contention is ignored.  
- Spacecraft crosslink standards beyond Proximity-1 (e.g., CCSDS space link extensions, modern smallsat ISL implementations) are not deeply engaged—though that may be unavoidable if data is proprietary.  
- Queueing-theoretic treatment is light relative to claims about MMPP/D/1 tails; you acknowledge “future work,” but then use tail results to justify buffer factors. That’s okay, but cite more directly relevant MMPP bounds or use conservative bounds.

---

# Major Issues

1. **The “three-layer feasibility framework” is not cleanly separated; \(\gamma\) is sometimes framed like a MAC efficiency layer.**  
   **Why it matters:** Readers will interpret “MAC efficiency” as including contention/collisions, whereas \(\gamma\) here is primarily *slot overhead efficiency* (framing+FEC+guard+acq). This affects how practitioners apply the equations and how reviewers judge completeness.  
   **Remedy:** Rename consistently to “slot efficiency” or “slot overhead factor,” and explicitly reserve “MAC efficiency” for contention-based effects (which are out of scope). Consider a short boxed definition: “\(\gamma\) accounts for per-slot non-payload time/bits under scheduled TDMA; it does not include contention losses.”

2. **\(\gamma\) unification (0.76 CCSDS-based) is improved, but consistency still needs auditing across all rate-dependent uses.**  
   **Why it matters:** Your feasibility boundary (24 infeasible, 30 minimum, 35 recommended) depends sensitively on \(\gamma_{24},\gamma_{30},\gamma_{35}\) and whether ACK and turnaround are included. Any inconsistency undermines the central claim.  
   **Remedy:** Add a single “\(\gamma\) ledger” table (you partially have this in Table \(\gamma\)-lookup footnote) promoted to a main-text table, listing for each rate: \(T_{\text{slot}}\), \(\gamma\), included components, and whether ACK is excluded. Then, in every place that uses \(\gamma\), cite that ledger table. Also add a unit-test style check in the repo that recomputes all reported \(\gamma\) values from Eq. (gamma_time) and asserts equality within tolerance.

3. **Campaign duty factor \(d\) addresses workload realism better than typical, but the mapping from operations to \((d,p_{\text{cmd}})\) remains under-specified and risks double-counting or misinterpretation.**  
   **Why it matters:** The “\(<1\%\) of operational time” claim is crucial to defusing the \(\eta_S\approx46\%\) stress-case. If practitioners misapply \(d\) (e.g., treat it as per-cycle probability rather than fraction of time in campaign) they will get wrong sizing.  
   **Remedy:** Provide a formal definition: \(d\) is fraction of cycles in ON state; \(p_{\text{cmd}}\) is conditional probability given ON. Then define effective command probability \(p_{\text{eff}}=d\cdot p_{\text{cmd}}\) and rewrite Eq. (eta_canonical) in terms of \(p_{\text{eff}}\) to reduce confusion. Add a short worked example that reproduces the “yearly mixture” calculation step-by-step and clarifies assumptions about campaign durations and command rates.

4. **Stress-case \(\eta_S\sim46\%\) is now contextualized as continuous-duty, but still appears in places that could be read as typical system load.**  
   **Why it matters:** Reviewers/practitioners may conclude the architecture is inherently heavy. Also, the stress-case interacts with TDMA egress only under certain command types (broadcast vs unicast).  
   **Remedy:** In every table/figure that includes the stress-case, label it “continuous-duty upper bound (rare)” and pair it with at least one realistic \((d,p_{\text{cmd}})\) scenario. Also separate “byte budget stress” from “airtime stress”: one is Test A dominated, the other is Test B dominated depending on \(q\) and stagger.

5. **DES verification provides limited incremental value and is close to self-confirmation; the paper acknowledges this but still leans on DES for credibility.**  
   **Why it matters:** For a top-tier journal, simulation should either (i) capture phenomena not in the equations, or (ii) be validated against independent models/data. Here, the DES largely shares the same assumptions and accounting.  
   **Remedy:** Strengthen the DES contribution by adding at least one phenomenon the closed-form does not capture and that materially affects design choices, e.g.:  
   - coordinator queue with finite buffer + service time variability, showing when CPU becomes binding;  
   - heterogeneous \(k_c\) distribution and its impact on fleet-level worst-case coordinator;  
   - stochastic acquisition failures leading to missed slots (modeled as additional loss/time).  
   Alternatively, reduce DES prominence and position it as an implementation artifact supporting reproducibility rather than as validation.

6. **Packet-level validation (Section IV-J) is not truly independent validation; it is a standards-based parameter estimate.**  
   **Why it matters:** Calling it “packet-level validation” (even implicitly) can overstate evidentiary strength. CCSDS framing gives plausibility, not measured performance, especially for acquisition time and burst-mode behavior.  
   **Remedy:** Rename the subsection and all references to it as “standards-anchored parameterization” (you already do in places). Make explicit that the only “independent” element is the use of CCSDS documented overhead bits/structures; timing parameters \(T_{\text{acq}}, T_{\text{turn}}\) remain assumptions. If possible, add even a small empirical anchor (e.g., published Prox-1 modem acquisition times, or vendor datasheet ranges) to reduce arbitrariness.

7. **The TDMA airtime test assumes centrally scheduled TDMA with perfect compliance and no timing jitter distribution; guard is treated deterministically.**  
   **Why it matters:** Your margin at 30 kbps is only 7.3% of \(T_c\) and is consumed by ARQ under GE. Any realistic jitter/acquisition variance could push feasibility.  
   **Remedy:** Replace deterministic \(T_{\text{acq}}\) and \(T_{\text{guard}}\) with distributions (even simple normal/lognormal with stated P95) and report probability of deadline miss vs rate. This would convert the “30 min / 35 rec” claim into a more defensible probabilistic schedulability statement.

8. **Generalized \(\gamma\) expression usefulness: good idea, but the practitioner workflow is still somewhat fragile.**  
   **Why it matters:** Practitioners need a robust recipe: measure or assume a small set of parameters and get a safe rate. Right now, \(\gamma\) depends on multiple overhead terms and the half-duplex partitioning, and it is easy to misapply.  
   **Remedy:** Provide a minimal “inputs checklist” and a “safe defaults” set, plus an explicit “do not do this” list (e.g., don’t multiply by \(1/\gamma\) twice; don’t treat \(\alpha_{\text{RX}}\) as free). Consider adding a one-page “engineering worksheet” in an appendix.

---

# Minor Issues

1. **Terminology:** avoid calling \(\gamma\) “MAC efficiency” anywhere; use “slot efficiency” consistently.  
2. **Equation/parameter coupling:** \(\alpha_{\text{RX}}\) is said to be “computed output,” but later you discuss values at different \(M_r\). Add a direct formula or table mapping \(M_r\rightarrow \alpha_{\text{RX}}\) under the assumed schedule.  
3. **ACK accounting:** sometimes ACK is “conservative default explicit mini-slot,” elsewhere “can be embedded in guard.” Make one choice for all design-relevant tables, and treat the alternative as sensitivity.  
4. **Link budget table:** “Aggregate capacity \(>200\) kbps” is asserted from \(C/N_0\) but without modulation/coding spectral efficiency assumptions. Add the assumed modulation and required \(E_b/N_0\) mapping for those higher rates.  
5. **Fleet reuse factor \(R=7\):** the C/I aggregation argument is very approximate. Either (i) downgrade to “illustrative geometry,” or (ii) provide a clearer derivation and assumptions (antenna pattern, sidelobe levels, altitude dispersion).  
6. **AoI section:** clarify that AoI results ignore deadline-miss-induced drops except where explicitly stated; otherwise readers may misinterpret AoI as including TDMA infeasibility.  
7. **Exception reporting:** \(p_{\text{exc}}\) is introduced, but its interaction with byte budget and ingress timing is not fully connected—does exception reporting reduce ingress load and thus reduce \(R_{\text{PHY,min}}\)? If yes, show it explicitly.  
8. **Reference quality:** several citations are non-archival web pages; acceptable in moderation, but key claims (e.g., Starlink ops scaling, Kuiper) should not hinge on them.  
9. **Algorithm 1:** line 3 uses \(C_{\text{node}}\) but it is not listed as an input to the algorithm; add it to REQUIRE or set it explicitly.  
10. **Consistency:** some tables use rounded margins (1,891 vs 1,891/1,891?)—ensure consistent rounding and units.

---

## Overall Recommendation  
**Recommendation:** Major Revision

The manuscript is a solid engineering sizing study with clear definitions, a useful two-test framework, and a much-improved treatment of workload realism via the campaign duty factor \(d\). The updated \(\gamma\) parameterization (CCSDS-grounded \(\approx 0.73{-}0.76\)) and the explicit separation of Model C (design-relevant) from Model S (upper bound) are meaningful improvements, and the rate ladder (20 kbps info \(\rightarrow\) ~27 kbps after \(\gamma\) \(\rightarrow\) ~30 kbps min / 35 kbps rec) is a practical artifact.

The main barrier to acceptance in a top-tier venue is evidentiary strength and interpretability: the DES largely confirms its own accounting, and the “packet-level validation” is not independent validation but standards-anchored parameter estimation with key timing assumptions left unmeasured. Additionally, the feasibility narrative still risks confusion between byte budget, slot overhead efficiency, and true MAC effects (contention), which matters because the central design conclusion is margin-sensitive at 30 kbps. A major revision should tighten terminology, strengthen probabilistic schedulability (jitter/acquisition distributions), and clarify the practitioner workflow so the equations can be safely applied without double-counting.

---

## Constructive Suggestions (ordered by impact)

1. **Make Test B probabilistic (deadline-miss probability) rather than deterministic margin**, using distributions for \(T_{\text{acq}}\), \(T_{\text{guard}}\), and turnaround; report \(P(\text{miss})\) vs \(R_{\text{PHY}}\) for 30 and 35 kbps. This directly strengthens the core claim.  
2. **Refactor workload modeling into \(p_{\text{eff}}=d\cdot p_{\text{cmd}}\)** and rewrite the main overhead equation and tables accordingly; add a clear operational mapping example and prevent misinterpretation.  
3. **Promote a single authoritative \(\gamma\) ledger** (rates, slot times, included components) and enforce consistency across all results; add repository checks.  
4. **Reposition DES as tail exploration with at least one nontrivial phenomenon** not present in the closed-form (e.g., acquisition failures, heterogeneous clusters, service-time variability), or reduce its role.  
5. **Rename and reframe Section IV-J** to avoid “validation” language; explicitly separate “standards-based bits accounting” from “timing assumptions.”  
6. **Clarify the scope of the 46% stress-case everywhere** and ensure tables/figures do not inadvertently present it as typical; always pair with realistic \(d\) scenarios.  
7. **Provide a one-page practitioner worksheet/checklist** (inputs, defaults, warnings about double-counting \(\gamma\), interpreting \(\alpha_{\text{RX}}\), and command type \(q\)/stagger effects).  

If these are addressed, the paper could become a strong design-reference contribution despite the unavoidable external-validation gap.