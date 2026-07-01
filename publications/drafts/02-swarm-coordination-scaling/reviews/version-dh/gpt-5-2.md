---
paper: "02-swarm-coordination-scaling"
version: "dh"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-03-06"
recommendation: "Major Revision"
---

## 1. Significance & Novelty  
**Rating: 4 (Good)**  
The manuscript targets an important and under-served gap: *parametric, per-cluster sizing equations* for hierarchical coordination traffic in very large swarms under a fixed per-node budget, with explicit separation of message-layer byte accounting and airtime schedulability. The “rate ladder” (info-rate → γ expansion → half-duplex → margin) and the explicit superframe timing budget are practically useful, and the paper is unusually explicit about what is and is not validated.  

Novelty is strongest in (i) the two-test feasibility framing tied to a concrete TDMA superframe, (ii) the explicit coupling of γ(R) with half-duplex partitioning and ARQ margin, and (iii) the campaign duty factor \(d\) as a workload realism knob. The paper is less novel in the individual ingredients (TDMA efficiency, GE channel, AoI tails), but the *integration into a sizing workflow* is a meaningful contribution.

---

## 2. Methodological Soundness  
**Rating: 3 (Adequate)**  
The analytical accounting is generally careful and the manuscript makes a commendable effort to prevent “double counting” (e.g., clarifying that γ is a parameter inside Test B, not a third test). The CCSDS-grounded slot model (Model C) is a step forward versus earlier “optimistic” timing models, and the explicit decomposition of acquisition/guard/framing/FEC is appropriate for preliminary sizing.

However, several methodological weaknesses remain: (a) the DES is largely a bookkeeping engine that shares assumptions with the equations (the paper admits this), (b) the slot simulator still relies on assumed acquisition and ACK behavior that materially affects feasibility at 30 kbps, (c) the GE model is not calibrated and the coherence-time regime switch is asserted rather than derived/validated, and (d) some key parameters (e.g., “coordinator summary = 512 B with 371 B metadata/CRC”) appear arbitrary and could dominate conclusions if changed.

---

## 3. Validity & Logic  
**Rating: 3 (Adequate)**  
Internal consistency is improved relative to what I would expect from earlier versions: (i) the campaign duty factor \(d\) is explicitly defined and mapped to mission phases, (ii) the stress case \(\eta_S \approx 46\%\) is clearly framed as a *continuous-duty upper bound* and mixed into a year-average, and (iii) the γ values (≈0.73–0.76) are consistently presented as CCSDS-parameterized rather than measured.

That said, there are still logic/validity risks:
- The three-layer narrative (byte budget, MAC/γ, TDMA airtime) is sometimes presented as “two-test” and sometimes as a “rate ladder” that can read like an additional feasibility gate. You try to address this with boxed text, but the paper still risks confusing practitioners about what is necessary/sufficient.
- The half-duplex partitioning and α_RX being “computed output” is good, but in practice α_RX is also a design choice (how much egress you reserve; how you schedule retransmissions), so calling it “not a free parameter” is only true under your specific superframe contract.
- The ARQ feasibility argument mixes mean/P95 binomial approximations with a GE model whose correlation structure makes binomial assumptions questionable (especially under cluster-common fades, which you mention but do not propagate through the ARQ slot demand distribution).

---

## 4. Clarity & Structure  
**Rating: 4 (Good)**  
Organization is strong: clear definitions, explicit test framework, and helpful “do not double count” warnings. Tables (rate ladder, superframe, γ decomposition, feasibility by acquisition mode) are the paper’s strongest communication artifacts. The explicit “V&V tiers” section is unusually transparent and welcome.

Clarity issues remain in a few places:
- Some sections are over-defensive and repetitive (multiple warnings about γ/test equivalence), which suggests the underlying framework could be simplified in presentation.
- Several numerical claims are scattered (e.g., 27 kbps vs 29.9 vs 30 vs 35) and would benefit from a single “canonical design point” panel that ties all assumptions together (k_c, S, T_c, T_guard, T_acq, ACK policy, FEC rate).

---

## 5. Ethical Compliance  
**Rating: 4 (Good)**  
Data/code availability is excellent (repository + tag + environment). AI disclosure is explicit and appropriately scoped (ideation/editing only). There are no human-subject or sensitive-data issues.

A remaining concern is reproducibility of *figures that depend on assumed PHY timing* (acquisition distributions, ACK timing). You provide point assumptions but not distributions; if the code samples those, the manuscript should state so.

---

## 6. Scope & Referencing  
**Rating: 3 (Adequate)**  
The paper is broadly within scope for T-AES / space systems networking and autonomy. References cover constellation ops, DTN/CGR, swarm robotics, AoI, GE channels, CCSDS, DVB-RCS2, and queueing basics.

Gaps:
- TDMA/return-link scheduling literature beyond DVB-RCS2 (e.g., demand-assigned TDMA in satellite networks, deterministic scheduling for half-duplex radios) is thin.
- Spacecraft crosslink MAC/PHY implementation references are limited; CCSDS Prox-1 is fine, but there are other CCSDS crosslink-related documents and practical modem papers that could strengthen γ realism.
- The paper positions “no prior work provides closed-form parametric sizing across 10^3–10^5 nodes with byte-level accounting.” That may be defensible, but it should be softened or better supported (there is related work in mega-constellation network dimensioning and control-plane scaling).

---

# Major Issues

1) **The “two-test” framework is sound, but the *three-layer feasibility narrative* is still easy to misapply**  
**Why it matters:** Practitioners may incorrectly treat \(C_{\text{raw}}=C_{\text{info}}/\gamma\) or the heuristic \(R_{\text{PHY,min}}\ge C_{\text{info}}/(\gamma\alpha_{\text{RX}})\) as an additional independent gate, or apply both and double-count. The manuscript tries to prevent this, but the repeated caveats indicate the presentation is not yet robust.  
**Remedy:**  
- Provide a single formal statement: “Necessary and sufficient conditions under the assumed superframe contract are Test A + Test B.” Then explicitly define *derived quantities* (γ, α_RX, heuristic bound) as intermediate computations.  
- Add a short worked example that executes Algorithm 1 step-by-step and shows that the heuristic equals Test B only under \(M_r=0\) and negligible egress; otherwise it is a lower bound.  
- Consider renaming “rate ladder” steps 2–3 as “unit conversion” and “duplex factor,” and label them explicitly as *intermediate computations* rather than “steps.”

2) **Campaign duty factor \(d\) improves workload realism, but the mapping from operations to \((d, p_{\text{cmd}})\) is still under-justified and potentially inconsistent**  
**Why it matters:** The paper’s key realism claim is that \(\eta_S\approx46\%\) is a continuous-duty bound occurring <1% of time. This hinges on how \(d\) and \(p_{\text{cmd}}\) are interpreted and combined. Right now, \(d\) “gates campaigns” and \(p_{\text{cmd}}\) is “per-cycle command probability within campaigns,” but several tables implicitly assume \(p_{\text{cmd}}=1\) during on-time. Many missions will have *bursty* command issuance within a campaign (not i.i.d. Bernoulli), and command sizes/types vary.  
**Remedy:**  
- Add a short subsection that distinguishes three regimes: (i) deterministic periodic commands, (ii) Bernoulli per-cycle commands, (iii) burst processes (e.g., ON/OFF within ON).  
- Provide at least one alternative mapping example (e.g., “X commands per hour during a 2-day reconfiguration”) showing how it translates to \(d\) and \(p_{\text{cmd}}\), and how sensitive \(\eta\) is to each.  
- If the DES uses an ON/OFF Markov model for campaigns, specify the parameters and show that the year-average \(\bar{\eta}\) is robust to plausible burstiness (not just the mean).

3) **γ “unification” (≈0.76 CCSDS-based) is mostly consistent, but there are still places where Model S results could be misconstrued as design-relevant**  
**Why it matters:** The manuscript correctly says Model S is “not for recommendations,” yet Table IV-D (deadline misses) uses Model S and contains striking numbers (52.7% misses) that can anchor reader perception. This undermines the “all feasibility claims use Model C” message.  
**Remedy:**  
- Move Table \ref{tab:tdma_joint_interaction} to an appendix or visually fence it with a stronger label: “Illustrative coupling only; not representative of CCSDS timing.”  
- Provide the same coupling table under Model C for at least two PHY rates (30 and 35 kbps) and one ARQ setting, even if approximate, so the reader sees coupling in the *actual design model*. You already state “~12% miss at 30 kbps Model C”; show it numerically with the simulator.

4) **DES “verification” currently adds limited scientific value beyond confirming accounting; tails are asserted but not demonstrated with sufficient specificity**  
**Why it matters:** A top-tier journal will expect either (i) novel analytical results, or (ii) simulation that reveals behaviors not captured analytically. You explicitly acknowledge Tier-1 tautology, but then the DES-tail contribution is not substantiated with concrete distributions/plots (buffer overflow probability vs. \(d\), ON/OFF parameters, cluster-correlation cases).  
**Remedy:**  
- Add one figure: buffer occupancy CDF (or P99) vs \(d\) for at least two burst models (Bernoulli vs ON/OFF Markov) and show how the recommended \(1.3\times\) / \(1.5\times\) factors arise.  
- Clarify what “distributional tails under campaign burstiness” means operationally: queue drops? deadline misses? AoI excursions? Provide at least one tail metric with confidence intervals.

5) **Packet-level validation in Section IV-J is still not independent validation; it is parameter anchoring—this is stated, but the paper still leans on it to justify a sharp 30→35 kbps recommendation**  
**Why it matters:** The central design conclusion (“24 infeasible, 30 minimum, 35 recommended”) depends critically on assumed \(T_{\text{acq}}\), \(T_{\text{guard}}\), ACK policy, and FEC framing. Without measurement or at least a conservative uncertainty treatment, the recommendation may not generalize.  
**Remedy:**  
- Expand uncertainty propagation: treat \(T_{\text{acq}}\) and \(T_{\text{guard}}\) as random variables (e.g., P95) and show \(P(\text{margin}<0)\) at 30 and 35 kbps. A simple Monte Carlo over timing uncertainties would be convincing and still “preliminary.”  
- Alternatively, provide a “robust design” table: required PHY for worst-case \(T_{\text{acq}}\) and \(T_{\text{guard}}\) percentiles, not just means.

6) **Generalized γ expression is useful, but the practitioner workflow still lacks a clear “measurement-to-design” pipeline that respects half-duplex and scheduling choices**  
**Why it matters:** Eq. (γ_time) is standard, but practitioners need to know *what exactly to measure* (acquisition per burst? per slot? tracking loss probability?) and how that maps into superframe feasibility when ACKs, retransmissions, and duplex turnaround are included.  
**Remedy:**  
- Strengthen the “measurement protocol for γ” into a concrete checklist including: burst acquisition distribution, turnaround distribution, BER/FER vs Eb/N0, and whether ACKs can be embedded in guard.  
- Provide a compact “design contract” summary: what assumptions must hold (GNSS timing, cold-start acquisition, half-duplex switching, fixed slot count) for Algorithm 1 to be valid.

---

# Minor Issues

1) **Coordinator summary size breakdown seems implausible**: “metadata/CRC (371 B)” dominates a 512 B summary. Clarify what constitutes metadata and why it is so large; otherwise readers will suspect padding.  

2) **Equation labeling / consistency**: You use \(\eta_{\text{TDMA}}\) and \(\gamma\) in different places; ensure the terminology is consistent (γ as slot efficiency, η as overhead/utilization).  

3) **AoI interpretation**: You correctly call P99 = 440 s a sampling tail under geometric exception reporting; consider explicitly stating that network delay is assumed negligible relative to \(T_c\) in that derivation, and point to where deadline misses would add \(mT_c\).  

4) **GE independence assumption**: You note per-node independent GE and mention cluster-common fading. Consider adding a short note that “independent GE implies binomial failed-slot demand; common-mode implies heavier tails,” and quantify with one number in the ARQ margin section (not only in prose).  

5) **Fleet reuse factor R=7**: The C/I aggregation estimate is very coarse. This is fine as a preliminary bound, but label it more explicitly as “order-of-magnitude geometry” and avoid implying it is a recommendation without RF simulation.  

6) **Algorithm 1 Test A uses \(C_{\text{node}}\) but it is not in REQUIRE**: Add \(C_{\text{node}}\) to the inputs or define it as global/default.  

7) **ACK accounting**: You state ACK is “not included in γ” and separately budget it; good. But Table \ref{tab:superframe} footnote offers “embed ACK within guard.” That would change the effective guard/jitter assumptions and should be treated as an alternative slot contract, not merely an optimization note.

---

## Overall Recommendation  
**Recommendation:** **Major Revision**

The paper has a strong core contribution (a practical sizing framework with explicit timing/byte accounting and a clear rate recommendation under stated assumptions), and Version DH shows meaningful improvements in workload realism (\(d\)), γ consistency (≈0.73–0.76 CCSDS-based), and contextualization of the 46% stress case as a continuous-duty upper bound. The structure, transparency about validation limits, and actionable tables are all strengths.

The main reason for Major Revision is that the manuscript still falls short of top-tier expectations in (i) demonstrating non-tautological simulation value (DES tails need concrete evidence), (ii) preventing misapplication of the feasibility framework (two-test vs “three-layer” narrative), and (iii) substantiating the sharp 30→35 kbps recommendation under uncertainty in acquisition/guard/ACK behavior and under correlated-loss demand distributions. These are addressable without new hardware experiments by tightening the presentation and adding targeted uncertainty/tail analyses.

---

## Constructive Suggestions (ordered by impact)

1) **Add a robust-feasibility uncertainty analysis for Test B**: Monte Carlo over \(T_{\text{acq}}\), \(T_{\text{guard}}\), turnaround, ACK placement; report \(P(\text{margin}<0)\) at 30 and 35 kbps. This would materially strengthen the central recommendation.

2) **Provide Model C ARQ×TDMA coupling results (not just Model S)**: even a small table for (30, 35 kbps) × (M_r=0,1) under the stated GE parameters would eliminate the current “illustrative but not design” disconnect.

3) **Make DES tails concrete**: include at least one queue/buffer occupancy distribution figure and show how the 1.3×/1.5× buffer factors are derived and how sensitive they are to burst model parameters.

4) **Tighten the feasibility framework exposition**: one theorem-like statement of sufficiency/necessity under the superframe contract, plus a worked example showing equivalence/inequivalence of the heuristic.

5) **Strengthen the operational mapping for \(d\) and \(p_{\text{cmd}}\)**: add a second mapping example and discuss non-i.i.d. command bursts within campaigns; show sensitivity of \(\bar{\eta}\) to plausible alternatives.

6) **Clarify and justify message-size assumptions that drive results** (especially coordinator summaries and command sizes), and provide a short sensitivity note: “if summary is X bytes, η0 changes by Y.”

7) **Improve practitioner guidance for measuring γ and timing parameters**: turn the measurement protocol into a reproducible checklist and explicitly state which percentiles (mean vs P95) should be used for design.

If you address items (1)–(3), the manuscript would be much closer to “Good/Acceptable with revisions” for a top-tier venue despite the acknowledged lack of external validation, because it would then present a *robust preliminary design method* rather than a point-estimate sizing exercise.