---
paper: "02-swarm-coordination-scaling"
version: "db"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-03-05"
recommendation: "Major Revision"
---

## 1. Significance & Novelty  
**Rating: 4 (Good)**  
The manuscript targets a real and under-served need: *closed-form, parametric* sizing rules for hierarchical coordination traffic in very large autonomous swarms under tight per-node bandwidth allocations. The two-test feasibility decomposition (byte budget + TDMA airtime) is a useful framing for early design, and the explicit “rate ladder” from information-rate to PHY-rate is practitioner-friendly. Novelty is primarily in the *engineering synthesis* (consistent accounting + schedulability + parameterized slot efficiency), not in new theory.

## 2. Methodological Soundness  
**Rating: 3 (Adequate)**  
The methodology is generally coherent for a preliminary sizing paper: analytical accounting, a cycle-aggregated DES for workload burstiness/tails, and a slot-level TDMA simulator for schedulability. However, several parts remain fragile or internally coupled (DES verifies equations it implements; GE/ARQ conclusions are strongly shaped by the coherence assumption; and some timing/ACK/half-duplex details are handled in ways that can bias margins). The paper is honest about the Tier-3 validation gap, which helps.

## 3. Validity & Logic  
**Rating: 3 (Adequate)**  
Core logic (ingress dominates; 24 kbps infeasible under CCSDS-grounded timing; 30 kbps minimum; 35 kbps recommended with margin) is plausible and mostly consistent. The campaign duty factor \(d\) is a meaningful knob and is now better contextualized. Remaining validity concerns are mainly about (i) whether the “three-layer” story is consistently presented without double counting, (ii) whether \(\gamma\) is applied consistently everywhere and separated cleanly from half-duplex partitioning and ACK assumptions, and (iii) whether the GE/ARQ results are presented as conditional artifacts vs general findings.

## 4. Clarity & Structure  
**Rating: 4 (Good)**  
The paper is substantially clearer than typical sizing manuscripts: notation table, explicit “two-test” box, rate ladder table, and a candid claim/evidence map. The repeated reminders about Model C vs Model S are helpful. Some sections are still overly dense and occasionally self-contradictory in emphasis (e.g., “\(\gamma\) is not a separate test” yet later a “three-layer” interpretation appears implicitly via \(C_{\text{raw}}=C_{\text{info}}/\gamma\) and \(\alpha_{\text{RX}}\)).

## 5. Ethical Compliance  
**Rating: 4 (Good)**  
Strong: code/data availability with a tag, explicit environment, and an AI disclosure. The manuscript appropriately warns that no external validation exists. One improvement: provide a minimal reproducibility checklist (exact commands, seed handling, and how to regenerate key figures/tables).

## 6. Scope & Referencing  
**Rating: 3 (Adequate)**  
The scope fits T-AES / space systems communications and autonomy, but the literature grounding is uneven: good coverage of distributed algorithms and some space networking, but limited engagement with (i) satellite TDMA/DAMA return-link scheduling literature beyond DVB-RCS2, (ii) CCSDS timing/Prox-1 implementation experience papers, and (iii) AoI over scheduled access networks. References are adequate for an engineering sizing note, but for a top-tier journal the MAC/TDMA and satellite networking citations should be strengthened.

## 7. Technical Depth (models, parameters, derivations)  
**Rating: 3 (Adequate)**  
The \(\gamma(R_{\text{PHY}})\) derivation via a time-domain decomposition (payload/FEC/framing/guard/acq) is a solid step toward realism and is more actionable than a fixed efficiency constant. Still, some parameter choices (ACK placement inside guard; acquisition time per slot; half-duplex partition; ranging amortization) need sharper justification or sensitivity analysis because they directly determine the 30 vs 35 kbps conclusion.

## 8. Results & Interpretation  
**Rating: 3 (Adequate)**  
Key results are clearly stated and summarized. The stress-case \(\eta_S\approx 46\%\) is now contextualized as a continuous-duty upper bound, which addresses prior realism concerns. The DES tail/buffer result is a legitimate incremental contribution. However, some results risk over-interpretation given the conditional nature of the GE model and the limited independence between tools.

## 9. Reproducibility & Robustness  
**Rating: 4 (Good)**  
Open repository and parameter tables are strong. Robustness is partially addressed via sensitivity (acq/guard, \(\gamma\) uncertainty propagation). Remaining robustness gaps: dependence on the per-cycle GE coherence assumption, limited exploration of alternative campaign processes beyond the shown ON/OFF example, and limited exploration of schedule variants (e.g., explicit ACK slots vs embedded ACK).

## 10. Practical Utility for Practitioners  
**Rating: 4 (Good)**  
Algorithm 1, the rate ladder, and the \(\gamma\)-conditional lookup table are genuinely useful as early design tools. The general \(\gamma\) expression (Eq. 62 / \(\ref{eq:gamma_time}\)) is a good “bridge” between standards framing and sizing. Utility would increase materially if the paper supplied a short worked example “recipe” that starts from measured modem logs (\(T_{\text{acq}}\), turnaround, framing, FEC) and produces \(R_{\text{PHY}}\), margin, and allowable \(k_c\).

---

# Major Issues

1) **Campaign duty factor \(d\): realism improved, but the mapping still mixes “command probability” and “campaign gating” in a way that can confuse workload interpretation**  
- **Why it matters:** The central claim that routine \(\eta\approx 5\)–10% hinges on \(d\) being a defensible abstraction. Right now, \(d\) gates campaigns while \(p_{\text{cmd}}\) gates per-cycle commands “within campaigns,” but the examples sometimes implicitly fold one into the other. This makes it hard to translate an ops concept (e.g., station-keeping cadence, orbit-raising plan) into \((d,p_{\text{cmd}})\) unambiguously.  
- **Remedy:** Add a short subsection that defines a *single* canonical mapping from an operational schedule to \((d,p_{\text{cmd}})\): e.g., given “X commands per day for Y days,” show how to compute \(d\) and \(p_{\text{cmd}}\) without double counting. Consider collapsing to an “effective per-cycle command rate” \(\lambda_{\text{cmd}}\) plus an optional burstiness parameter, then show how \(d\) is one way to realize that \(\lambda_{\text{cmd}}\). Provide 2–3 mission-phase exemplars with consistent arithmetic.

2) **\(\gamma\) unification (0.76 CCSDS-grounded) is mostly consistent, but there are still places where Model S and Model C could leak into decision-relevant reasoning**  
- **Why it matters:** The paper’s key design conclusion (24 infeasible, 30 minimum, 35 recommended) is sensitive to \(\gamma\) and fixed-time overheads. Any ambiguity about which \(\gamma\) is used where undermines confidence. The manuscript does a good job flagging Model S as non-decision, but it still uses Model S to demonstrate ARQ×TDMA coupling in a prominent table (Table IV-D / \ref{tab:tdma_joint_interaction}), which can be misread as supporting the 24–30 kbps decision.  
- **Remedy:** (i) Move the Model-S-only coupling table to an appendix or explicitly label it “mechanism illustration only; not numerically applicable.” (ii) Provide the same coupling sweep under Model C at 30 and 35 kbps (even if the conclusion is “30 marginal for ARQ slots; 35 robust”), so the coupling evidence aligns with the decision model.

3) **Three-layer feasibility narrative: the framework is sound, but the presentation still risks double counting and conceptual confusion (byte budget vs MAC efficiency vs TDMA airtime)**  
- **Why it matters:** You correctly state \(\gamma\) is a parameter within Test B, not a separate test. Yet the text and equations sometimes read like: Test A (bytes), then “MAC efficiency conversion” \(1/\gamma\), then TDMA airtime—suggesting a third layer. Practitioners may apply both the heuristic and the explicit slot schedule, or apply \(1/\gamma\) twice (once in \(C_{\text{TDMA}}\), again via slot time).  
- **Remedy:** Add a single “accounting equivalence” figure or boxed derivation showing:  
  \[
  \text{bytes} \rightarrow \text{information time} \rightarrow \text{slot time} \rightarrow \text{superframe time}
  \]
  and explicitly prove equivalence between (a) \(C_{\text{info}}/\gamma\) and (b) summing slot times, under stated assumptions. Then state a rule: *use either the rate ladder OR the explicit superframe budget, not both*, except as a cross-check.

4) **DES verification value: currently mostly self-confirmation; the tail/buffer result is useful but under-specified and potentially non-general**  
- **Why it matters:** For a top-tier journal, simulation must add insight beyond confirming equations. You acknowledge this, but the buffer-sizing guidance depends heavily on the chosen ON/OFF campaign model and correlation scope. Without clearer characterization, readers may overgeneralize “1.3× buffer” as a robust rule.  
- **Remedy:** Quantify tail sensitivity to at least two additional workload processes (e.g., heavy-tailed ON durations, or a Markov-modulated command arrival with different burst lengths but same mean \(d\)). Report how the P99/P999 ingress and recommended buffer multiplier \(M\) change. If you cannot extend, then narrow the claim: present the DES tail as *an example* and remove prescriptive multipliers, or bound them in terms of burst-length statistics.

5) **Packet-level validation (Section IV-J): good step, but it is not independent validation; the paper should tighten what is being validated and what is merely parameter anchoring**  
- **Why it matters:** The manuscript says \(\gamma\) is “anchored in CCSDS framing,” but the term “packet-level simulator” can be misconstrued as validating channel access performance. In reality, it computes efficiency from assumed framing and timing. That’s fine, but it must be framed as such to avoid overstating evidence.  
- **Remedy:** Rename “packet-level simulator” to “framing/slot accounting model” (or similar) and explicitly list its inputs/outputs: it does not simulate acquisition failures, Doppler tracking loops, or BER-to-PER curves; it only accounts for time/bit overhead. Add one small table showing which PHY/MAC phenomena are included vs excluded in \(\gamma\).

6) **GE/ARQ conclusions are structurally driven by the per-cycle coherence assumption; the manuscript states this, but the narrative still presents some outcomes as findings rather than conditional artifacts**  
- **Why it matters:** The headline “27% intra-cycle recovery” and “ARQ structurally ineffective” are only true under the model where the channel state is constant over the whole cycle and across all retransmissions. That is a strong assumption and will not hold for many impairment sources (fast fading, interference variability, tracking loop dynamics).  
- **Remedy:** Recast Section IV-C/IV-D around a decision tree keyed on \(\tau_c/T_c\): show explicitly that intra-cycle ARQ success is a function of *state mixing within the ARQ window*, not just \(p_{BG}\). If you keep the per-cycle GE, present the 27% result as “by construction under \(\tau_c\ge T_c\)” (you already say this in places) and avoid using it as evidence of real-world ARQ inefficacy.

7) **Half-duplex, ACK placement, and guard-time accounting: current treatment may be optimistic and should be stress-tested because it directly affects the 30 kbps margin**  
- **Why it matters:** At 30 kbps Model C you have only ~730 ms margin before ARQ/ranging/unmodeled overhead. The assumption that 0.5 ms ACKs “fit inside jitter sub-slot” of the guard is nonstandard and could be invalid depending on radio turnaround constraints and timing uncertainty. If ACKs require explicit airtime (or additional turnarounds), margins shrink.  
- **Remedy:** Provide a conservative alternative superframe with explicit ACK mini-slots (you mention +50 ms) *and* include any required additional turnarounds if ACK direction differs. Then rerun the minimum-rate feasibility under that conservative framing for 30 and 35 kbps. Make the conservative framing the default for recommendations, or justify why embedded ACK is implementable with Prox-1-class hardware.

8) **Generalized \(\gamma\) expression: useful, but practitioners need clearer guidance on how to measure/estimate each term (especially \(T_{\text{acq}}\))**  
- **Why it matters:** Eq. \(\ref{eq:gamma_time}\) is one of the most practically valuable contributions. But without measurement guidance, readers cannot reliably instantiate it; \(T_{\text{acq}}\) dominates the rate dependence and can swing conclusions (your Table \ref{tab:rate_feasibility} shows 30 kbps breaks at ~7.4 ms).  
- **Remedy:** Add a concise “measurement protocol” paragraph: what to log on a modem (time from TX enable to first decoded frame; distribution across SNR/Doppler), how to estimate turnaround, and how to compute an empirical \(\gamma\) with confidence intervals. Then show how the CI propagates to \(R_{\text{PHY,min}}\).

---

# Minor Issues

1) **Terminology:** “MAC efficiency” vs “slot efficiency” vs “TDMA slot efficiency” are used interchangeably. Pick one term (recommend “slot efficiency”) and keep “MAC efficiency” only if you explicitly include contention overhead (which you do not).  

2) **Equation/variable hygiene:** In Algorithm 1, Test A uses \(C_{\text{node}}\) but it is not in the REQUIRE list; add it or state it as fixed default.  

3) **Units consistency:** Some tables report “kbps” but are “info-rate” vs “PHY-rate.” You often clarify, but ensure every table column header includes “info” or “PHY” where relevant.  

4) **Table \ref{tab:tdma_joint_interaction}:** Since it is Model S only, it should not be located where it appears to support the main feasibility boundary. Stronger captioning or relocation recommended (see Major Issue 2).  

5) **AoI discussion:** You state AoI P99 is “sampling-limited” for exception reporting; consider adding one sentence clarifying that network-induced losses/deadline misses would add additional AoI mass at multiples of \(T_c\).  

6) **Fleet reuse (Section \ref{sec:fleet_reuse}):** The C/I back-of-envelope uses a single interferer and a rough antenna sidelobe. Add a note that aggregate interference from multiple clusters could reduce C/I; at minimum, mention power-sum worst case and that reuse factor is provisional.

7) **Related work:** Add a few more citations on satellite TDMA/DAMA scheduling and burst-mode acquisition overhead characterization (even if not CCSDS-specific), to better situate the framing.

---

# Overall Recommendation  
**Recommendation:** **Major Revision**

The manuscript is promising and has clear practitioner value, especially with the explicit rate ladder, the two-test feasibility framing, and the CCSDS-grounded \(\gamma(R)\) accounting that replaces earlier ad hoc efficiency constants. The campaign duty factor \(d\) is a meaningful abstraction and is now better contextualized; presenting \(\eta_S\approx 46\%\) as a continuous-duty upper bound occurring <1% of time is a substantial improvement and addresses workload realism concerns.

The main reasons for major revision are not formatting but *scientific defensibility and interpretability*: several conclusions (particularly around ARQ efficacy and the tightness of 30 kbps feasibility) depend on modeling/implementation details (GE coherence, ACK/guard accounting, half-duplex timing) that need either conservative bounding or clearer conditional framing. Additionally, while the paper is admirably transparent about limited validation, the internal multi-simulator verification story still reads too self-referential; the DES tail result is valuable but should be presented with stronger sensitivity or narrower claims.

---

# Constructive Suggestions (ordered by impact)

1) **Make the 30 vs 35 kbps conclusion robust to conservative ACK/turnaround assumptions.** Provide an explicit conservative superframe and recompute margins under Model C.  

2) **Reframe GE/ARQ as a conditional design tool keyed on \(\tau_c/T_c\)** (decision tree + avoid “finding” language when it’s by construction). Add at least one alternative coherence regime example (e.g., sub-cycle mixing) to demonstrate how conclusions change.

3) **Tighten the workload model mapping:** provide a single unambiguous translation from operational command schedules to \((d,p_{\text{cmd}})\) (or define an effective \(\lambda_{\text{cmd}}\)) and ensure all examples follow it.

4) **Clarify the feasibility/accounting equivalence and prevent double counting** with a boxed derivation and a “do not apply both methods simultaneously” rule.

5) **Strengthen the DES tail contribution** by adding sensitivity to burst-length distributions (or narrowing claims about buffer multipliers).

6) **Improve the practitioner instantiation of Eq. \(\ref{eq:gamma_time}\)** with a short measurement protocol and CI propagation example.

7) **Align all decision-relevant coupling evidence with Model C** (move Model S table to appendix or replicate key coupling results under Model C at 30/35 kbps).

8) **Augment related work** on satellite TDMA/DAMA and burst-mode acquisition overhead characterization to better anchor assumptions.

If the authors address the above, the paper could become a strong “design equations + sizing” contribution appropriate for a top-tier aerospace systems journal, with clear boundaries on validity and a genuinely useful parameterization for early-phase architecture trades.