---
paper: "02-swarm-coordination-scaling"
version: "cm"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-03-03"
recommendation: "Major Revision"
---

## 1. Significance & Novelty  
**Rating: 4 (Good)**  
The manuscript tackles an important and under-served niche: *closed-form, parametric sizing* of hierarchical coordination traffic and TDMA feasibility for very large swarms (10³–10⁵). The two-layer decomposition (message-layer byte budget + physical-layer TDMA schedulability) is a useful framing for early-phase architecture trades, and the explicit “rate ladder” from information-rate to PHY-rate is practitioner-friendly. The paper is also unusually candid about validation limits, which is commendable.

Novelty is strongest in (i) the explicit separation of topology overhead \(\eta_0\) from workload-dependent command traffic via a duty factor \(d\), and (ii) the standards-anchored slot-efficiency \(\gamma\) derivation used to change the design conclusion (24 kbps infeasible, 30 kbps minimum, 35 kbps recommended). The GE sweep is a helpful sensitivity tool, though it is more “design curve generation” than validation.

---

## 2. Methodological Soundness  
**Rating: 3 (Adequate)**  
The analytical accounting is generally coherent and the paper does a good job distinguishing what is computed at message level (DES/closed-form) versus what requires slot-level timing. The three “tiers” of V&V are clearly described, and the manuscript avoids over-claiming external realism.

However, several methodological choices materially affect conclusions and need tighter justification or bounding: (a) the workload model (commands as 512 B per node per cycle in stress) and the duty-factor mapping to real operations; (b) the half-duplex schedule and the derivation/use of \(\alpha_{\text{RX}}\); (c) the ARQ model (ACK minislot, retransmission slot pool appended, non-preemptive) and its interaction with GE coherence assumptions; and (d) the extent to which the DES “tail results” are robust to alternative arrival correlation models beyond the specific ON/OFF constructions used.

---

## 3. Validity & Logic  
**Rating: 3 (Adequate)**  
Internally, the decomposition into Layer 1 (bytes) and Layer 2 (airtime) is mostly consistent and the manuscript repeatedly warns against double-counting \(\gamma\). The stress-case \(\eta_S \approx 46\%\) is now explicitly framed as a *continuous-duty upper bound* and the campaign duty factor \(d\) is used to address workload realism—this is a clear improvement versus a static “always-stress” interpretation.

Remaining logic gaps are mainly around:  
* whether the “recommended 35 kbps” conclusion is robust to plausible alternative slot structures (e.g., amortized acquisition, different ACK strategy, different guard assumptions) given that \(\gamma\) and “unmodeled overhead” are doing a lot of work;  
* whether the DES verification adds independent evidence (it mostly verifies means by construction, as admitted); and  
* whether the packet-level \(\gamma\) anchoring is consistently propagated everywhere (there are still places where Model S/C comparisons could confuse readers about which \(\gamma\) is binding in which table/claim).

---

## 4. Clarity & Structure  
**Rating: 4 (Good)**  
Overall organization is strong: notation table, clear definition of \(\eta\) vs baseline, explicit “workflow,” and the claim-evidence map are all above average for this topic. The “do not double-count” paragraph is particularly helpful.

That said, the manuscript is dense and occasionally self-contradictory in phrasing (e.g., “1 kbps drives the design” vs “TDMA sizing applies to S-band coordination channel,” which is correct but easy to misread). Some tables mix Model S and Model C results without sufficiently prominent labeling at the point of use. A short “Assumptions that drive the 30/35 kbps conclusion” box would reduce reader confusion.

---

## 5. Ethical Compliance  
**Rating: 5 (Excellent)**  
Strong reproducibility posture: code and tag provided, environment specified, and limitations clearly stated. AI assistance is disclosed with a reasonable scope statement. Data availability is appropriate for a simulation-based design paper.

---

## 6. Scope & Referencing  
**Rating: 4 (Good)**  
The paper is broadly suitable for T-AES / space systems networking audiences. Referencing is decent across distributed algorithms, swarm robotics, AoI, CCSDS, and satellite networking. The CCSDS anchoring is appropriate.

Gaps: the MAC/TDMA literature is referenced lightly given how central TDMA efficiency and framing overhead are. Consider adding a few more directly comparable TDMA efficiency/overhead references beyond DVB-RCS2 (e.g., demand-assigned TDMA analyses in satellite return links, Proximity-1 implementation notes if available, or smallsat ISL MAC papers). Also, the “Starlink ops” and “Kuiper overview” are non-archival; acceptable as context, but key technical claims should not depend on them.

---

# Major Issues

1. **Ambiguity/inconsistency in the “three-layer feasibility framework” vs “two-layer” framing**  
   - **Issue:** The abstract and intro describe a two-layer framework (\(\eta\) and \(\gamma\)), but later text emphasizes “three-tier decomposition” (baseline/architecture/workload) and also uses \(\eta_{\text{total}}/\gamma\) as an intermediate mapping. Some readers will interpret this as a third feasibility layer or as double counting.  
   - **Why it matters:** This is the central conceptual contribution; any confusion undermines uptake by practitioners and reviewers.  
   - **Remedy:** Add a single canonical figure (or boxed definition) explicitly stating:  
     (i) baseline vs \(\eta\) decomposition is *accounting*, not a feasibility layer;  
     (ii) feasibility layers are exactly two: bytes and airtime;  
     (iii) \(\eta_{\text{total}}/\gamma\) is only a *screening heuristic* and never a binding constraint.  
     Also ensure the abstract uses the same terminology.

2. **Campaign duty factor \(d\): improved, but still under-validated and potentially misleading as “workload realism”**  
   - **Issue:** The introduction/contributions claim \(d\) addresses episodic workloads; however the mapping from mission phases to \(d\) remains largely narrative and the “reverse-derived example” yields \(d\approx 0.0016\), while the “conservative default” uses \(d=0.10\). That is a ~60× gap, which strongly affects the headline “routine \(\eta\approx 5\)–10%” claim.  
   - **Why it matters:** A key prior concern (as you note) is workload realism. Without tighter anchoring, readers may view \(d\) as a free knob that can justify almost any conclusion.  
   - **Remedy:** Provide a more formal method to derive \(d\) from (a) maneuver frequency distributions, (b) command burst length distributions, and (c) command addressing mode \(q\). At minimum:  
     - present a table of \(d\) computed from the cited ESA “~10 maneuvers/spacecraft/yr” under explicit assumptions about cycles per maneuver;  
     - show sensitivity of \(\eta\) and coordinator buffer P99 to \(d\in[10^{-4},10^{-1}]\);  
     - clarify whether \(d\) is meant for *peak design within an outage window* vs *annual average utilization*. Right now both interpretations appear.

3. **\(\gamma\) unification to 0.761/0.745 is a strong improvement, but not fully “consistently applied” in conclusions and some tables**  
   - **Issue:** You correctly replace the earlier optimistic \(\gamma\) with CCSDS-anchored \(\gamma_{C,24}=0.761\), \(\gamma_{C,30}=0.745\). But the manuscript still uses Model S in several plots/tables (e.g., unicast stagger figure caption references Model S curves and then states Model C result). The risk is that readers will cherry-pick the upper-bound model.  
   - **Why it matters:** The 24 kbps infeasible / 30 kbps minimum conclusion hinges on \(\gamma\). Any ambiguity weakens the main design recommendation.  
   - **Remedy:** Enforce a strict presentation rule: every figure/table must have an explicit “Model C (used for claims)” label if it is used to support a recommendation, and Model S results must be visually boxed as “upper bound only.” Consider moving Model S to an appendix or to a single “optimistic bound” section.

4. **Stress-case \(\eta_S\approx 46\%\) is better contextualized, but still conflates “continuous duty” with “peak within a campaign”**  
   - **Issue:** You now state stress is a synthetic bound and episodic. But later, safety-critical language (“undersizing causes 100% deadline misses… complete situational awareness loss”) is tied to the TDMA ingress feasibility (which is independent of \(\eta_S\)), while readers may associate it with stress-case command load.  
   - **Why it matters:** It risks overstating operational severity by blending two different bottlenecks: coordinator ingress (status traffic) vs command egress (stress-case).  
   - **Remedy:** Separate clearly:  
     - coordinator ingress feasibility is dominated by *status reports* and is largely independent of \(d\);  
     - stress-case \(\eta_S\) is about *command traffic* and mostly affects byte budget and egress scheduling (especially for unicast).  
     A simple dependency diagram (“what depends on \(d\), what depends on \(k_c\), what depends on \(\gamma\)”) would fix this.

5. **Layer-2 TDMA model: half-duplex partitioning and \(\alpha_{\text{RX}}\) derivation need a more rigorous schedule specification**  
   - **Issue:** You state \(\alpha_{\text{RX}}\) is “derived from schedule,” but the schedule is not fully specified as a general algorithm beyond the default superframe budget. It is unclear how \(\alpha_{\text{RX}}\) changes with added control slots (ACKs, ranging, sync beacons), retransmission pools, or unicast fraction \(q\).  
   - **Why it matters:** The feasibility boundary is tight at 30 kbps; small schedule changes can flip the conclusion.  
   - **Remedy:** Provide a formal superframe definition: ordered segments, fixed vs variable slot counts, and a closed-form expression for \(\alpha_{\text{RX}}\) as a function of \(k_c\), \(M_r\), and control-plane options. Then compute margins under at least two plausible schedule variants (e.g., ACK-per-slot vs bitmap ACK, ranging periodicity).

6. **DES “verification value”: still limited; tail claims may be too dependent on chosen burst model**  
   - **Issue:** You appropriately admit DES matches analytical means by construction. The incremental value is tail/buffer sizing under campaign correlation. But the burst models (Bernoulli gating, ON/OFF Markov, cluster-correlated ON/OFF) are only a small subset of plausible operational processes, and the buffer “1.15× mean” style guidance may not generalize.  
   - **Why it matters:** Practitioners may treat these tail multipliers as robust engineering rules when they are model-contingent.  
   - **Remedy:** Add at least one additional arrival correlation model that is structurally different (e.g., heavy-tailed ON durations, or Hawkes/self-exciting bursts for fault cascades), and show whether P99 multipliers materially change. Alternatively, explicitly scope the tail guidance: “valid for geometric ON/OFF with these parameters.”

7. **Packet-level validation (Section IV-J) anchors \(\gamma\), but is not “independent validation” and should not be framed as such**  
   - **Issue:** You mostly do this correctly, but some phrasing (“packet-level TDMA simulator,” “cross-model consistency”) can read like validation of the overall framework rather than parameter anchoring. Also, the \(\gamma\) derivation uses an assumed acquisition time (5 ms) that is not directly from CCSDS (you call it “assumed; Prox-1 class”).  
   - **Why it matters:** Reviewers will scrutinize whether the 0.761 number is truly standards-derived or partially assumed.  
   - **Remedy:** Tighten language: call it “standards-based framing + assumed acquisition/guard model.” Provide a range for \(T_{\text{acq}}\) and show how \(\gamma\) and the 30/35 kbps recommendation move (you partly do this in Fig. margin sensitivity; elevate it to the main conclusion).

8. **Generalized \(\gamma\) expression: useful, but dimensional form (Eq. 36) is error-prone and may confuse practitioners**  
   - **Issue:** Eq. \(\ref{eq:gamma_general}\) mixes bits and a converted “ms·bps” term; although you provide a dimensional check, this is exactly the kind of equation practitioners misapply.  
   - **Why it matters:** You explicitly aim for practitioner usability. A small unit mistake can change feasibility conclusions.  
   - **Remedy:** Make the time-domain form (Eq. \(\ref{eq:gamma_time}\)) the *primary* equation and demote Eq. \(\ref{eq:gamma_general}\) to an alternate form or appendix. Provide a short pseudocode function for \(\gamma\) computation with units.

---

# Minor Issues

1. **Terminology conflict:** “RF-backup channel (1 kbps per-node budget)” vs “S-band coordination channel (35 kbps recommended).” Consider consistently calling 1 kbps an *allocation* and the 30–35 kbps a *cluster PHY*, every time.  
2. **Table consistency:** Table \(\ref{tab:bandwidth_scaling}\) lists “Coord. bottleneck? Yes (20.3 kbps info)” but earlier abstract says “anchors \(\gamma\approx 0.76\), confirming 35 kbps recommended.” Consider adding the PHY equivalent in that table to prevent mixing info-rate and PHY-rate.  
3. **ARQ accounting:** In Table \(\ref{tab:superframe}\) there is no explicit line item for ACK minislot overhead, yet Section IV-D describes per-slot ACK/NACK minislot (0.5 ms). Either include it or justify why it is negligible/absorbed.  
4. **GE parameter mapping:** The mapping \(p_{BG}\approx T_c/\bar{T}_B\) is only approximate (memoryless). Consider stating explicitly it is a first-order mapping for geometric burst lengths.  
5. **AoI interpretation:** Good note that AoI P99 is sampling-policy-driven. Consider moving that caveat to the first paragraph of the AoI section to prevent misinterpretation.  
6. **Exception telemetry definitions:** Profiles define \(p_{\text{exc}}\) in a way that “Nominal: \(p_{\text{exc}}=1.0\) (periodic)” is counterintuitive (exception probability = 1 means always). Rename to \(p_{\text{rep}}\) (report probability) or clarify \(p_{\text{exc}}\) is “reporting probability” not “exception probability.”  
7. **Reference hygiene:** Several “accessed February 2026” non-archival references are fine for context but should not support technical parameter choices. Ensure all parameter claims (e.g., acquisition times, turnaround times) cite standards or hardware sources where possible.

---

## Overall Recommendation  
**Recommendation:** **Major Revision**

The paper has clear potential and several strong elements (explicit sizing equations, consistent accounting, standards-anchored \(\gamma\), candid validation map). However, because the main design recommendation (30 kbps minimum, 35 kbps recommended) is margin-tight and heavily schedule/assumption dependent, and because the workload realism argument hinges on a loosely anchored duty factor \(d\), the manuscript needs revision to (i) tighten the schedule model and its parameters, (ii) formalize the interpretation/derivation of \(d\), and (iii) enforce consistent Model C usage throughout all decision-relevant claims.

With these changes, the work could become a valuable “engineering methods” reference for early-phase swarm coordination sizing. Without them, it risks being read as internally consistent but too assumption-sensitive to support the strength of its safety-critical conclusions.

---

## Constructive Suggestions (ordered by impact)

1. **Add a single “Design conclusion robustness” section**: vary \(T_{\text{acq}}\), guard, ACK strategy, and ranging periodicity; show when 30 kbps fails and whether 35 kbps still holds.  
2. **Formalize the superframe/schedule** and provide closed-form expressions for \(T_{\text{ing}}\), \(T_{\text{egr}}\), and \(\alpha_{\text{RX}}\) including control-plane overheads and retransmission pools.  
3. **Strengthen duty-factor realism**: compute \(d\) from at least one cited operational statistic with explicit assumptions; distinguish annual average vs peak-within-outage sizing.  
4. **Make Model C the default everywhere**: relegate Model S to a bounded “optimistic upper bound” subsection or appendix; ensure all recommendation-supporting tables/figures are Model C.  
5. **Clarify what DES adds** by either (a) adding another burst model to show tail robustness, or (b) narrowing claims so P99 multipliers are explicitly conditional.  
6. **Promote Eq. \(\ref{eq:gamma_time}\)** as the primary practitioner equation; provide a small unit-safe computation snippet in the paper or repository README.  
7. **Rename \(p_{\text{exc}}\)** or clarify it, to avoid semantic confusion in the AoI section.