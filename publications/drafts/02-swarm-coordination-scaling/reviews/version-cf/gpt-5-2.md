---
paper: "02-swarm-coordination-scaling"
version: "cf"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-03-01"
recommendation: "Major Revision"
---

## 1. Significance & Novelty  
**Rating: 4 (Good)**  
The manuscript targets a real gap: *closed-form, byte-accounted* sizing relationships for coordination traffic in very large swarms (10³–10⁵) with an explicit bridge to PHY/MAC schedulability. The two-layer feasibility framing (message-byte budget vs. half-duplex TDMA airtime) plus a standards-grounded derivation of MAC efficiency is a meaningful contribution for early-phase architecture sizing, where practitioners need “back-of-the-envelope but defensible” equations. The paper’s novelty is more in *integration and engineering usefulness* than in new theory; that is appropriate for T-AES if the validation story is tightened and the scope/claims are carefully bounded.

## 2. Methodological Soundness  
**Rating: 3 (Adequate)**  
The analytical accounting is straightforward and generally sound, and the separation into Layer 1 (bytes) and Layer 2 (airtime) is conceptually correct. The slot-level TDMA simulator adds real value by enforcing half-duplex timing and exposing ARQ×TDMA coupling. However, the cycle-aggregated DES is largely a re-implementation of the same equations and therefore contributes limited independent evidence; its main value is distributional/buffer-tail characterization, which is currently under-leveraged (few concrete design implications beyond “P99 is heavier”). The GE modeling is presented as a sensitivity study (good), but the mapping to ISL reality remains speculative; the paper should be more explicit about what decisions can be made *without* measured GE parameters.

## 3. Validity & Logic  
**Rating: 3 (Adequate)**  
Internal logic is mostly consistent, and Version CF clearly improved scoping language (e.g., “illustrative GE parameters pending measurement,” explicit “continuous-duty upper bound”). Still, there are some logical tensions:
- The “representative instantiation” mixes a 1 kbps *per-node budget* with a 24–30 kbps *coordinator PHY* and then uses TDMA schedulability arguments that depend on the coordinator’s half-duplex partitioning; this is fine, but the narrative sometimes implies the 1 kbps regime “drives” TDMA at the same time that the coordinator is operating at 24–30 kbps. The connection needs to be stated more crisply as a *safe-mode / RF-backup design case* rather than a nominal operating point.
- The “TDMA required when \(\eta_{\text{total}}/\gamma > 50\%\)” heuristic (Table VIII and Algorithm 1) is plausible for half-duplex with symmetric needs, but it is not derived as a general threshold and may mislead users when ingress/egress asymmetry or multi-cluster interference dominates.

## 4. Clarity & Structure  
**Rating: 4 (Good)**  
The paper is well organized, notation is unusually thorough, and the “claim map by verification tier” is a strong practice. The stress-case contextualization is clearer than typical. That said, several sections remain dense and occasionally self-contradictory in numbers (see Major Issues on \(\gamma\), slot durations, and feasibility tables). The manuscript would benefit from one consolidated “default parameter set + derived quantities” table to prevent readers from chasing values across sections.

## 5. Ethical Compliance  
**Rating: 4 (Good)**  
Open-source code and a tag are provided—excellent for reproducibility. The AI-assisted ideation disclosure is explicit. A remaining issue is *reproducibility-by-reading*: several derived quantities (slot duration, guard, acquisition, framing overhead) appear with inconsistent numeric instantiations across sections/tables, which can impede third-party replication even with code.

## 6. Scope & Referencing  
**Rating: 3 (Adequate)**  
The references cover distributed algorithms, AoI, CCSDS, and constellation networking reasonably. For T-AES / ASR level completeness, I would expect tighter engagement with: (i) satellite MAC/TDMA standards and implementations beyond Proximity-1 (e.g., DVB-S2X style framing/efficiency analogs, though not CCSDS), (ii) LEO ISL channel measurement literature (even if sparse), and (iii) queueing/AoI results for Bernoulli/ON-OFF sampling under periodic service (you cite the key AoI surveys but could connect more directly to your geometric-tail expression). The “centralized ground processing” baseline is explicitly a compute-queue bound; that caveat is good, but the baseline still reads somewhat strawman for comms-limited regimes.

---

# Major Issues

1) **Inconsistent and sometimes contradictory application of the standards-derived \(\gamma\) (0.760) and associated slot/ingress numbers**  
**Why it matters:** \(\gamma\) is the central unifying parameter tying message-layer sizing to PHY feasibility. If tables/derivations disagree, the main conclusion (“30 kbps minimum viable”) looks accidental rather than robust. Reviewers/readers will check these numbers first.  
**Evidence in text:**  
- Eq. (25) / Table VI superframe uses 92.7 ms slots (based on 2112 bits @24 kbps + 4.7 ms guard) and yields feasibility at 24 kbps under “no loss” with 623 ms margin.  
- Section IV-J / Table XXIII (“PHY Rate Feasibility”) gives at 24 kbps: slot = 115.5 ms, ingress = 11,435 ms, infeasible.  
- Table XXII gives \(\gamma_{24}=0.760\) but the “slot” numbers mix 111.5 ms (text) vs 115.5 ms (table).  
These cannot all be true simultaneously.  
**Specific remedy:**  
- Create a single authoritative “slot construction” definition used everywhere:  
  \[
  T_{\text{slot}} = \frac{(S\cdot 8 + O_{\text{frame}})}{R_{\text{PHY}}\cdot R_{\text{FEC}}} + T_{\text{guard}} + T_{\text{acq}}
  \]
  and explicitly state whether \(O_{\text{frame}}\) is *before* or *after* FEC.  
- Recompute and harmonize: Table VI (superframe), Table VII (\(\gamma\) sensitivity), Table XXIII (rate feasibility), and any “ingress≈9.1 s” claims so they match exactly for the same assumptions.  
- Add a short “Assumption set A/B” if you intentionally use two different slot models (e.g., “slot-level timing model without acquisition/FEC” vs “standards-grounded model”). Right now the manuscript interleaves them.

2) **The “gamma unification” is improved (0.85→0.76) but not consistently propagated into earlier feasibility claims and narrative**  
**Why it matters:** Version CF’s key claimed improvement is adopting \(\gamma=0.760\) validated via CCSDS and using it throughout. If earlier sections still implicitly rely on \(\gamma\approx0.90–0.95\) (slot-only), the conclusions about 24 kbps feasibility and 30 kbps margin become ambiguous.  
**Specific remedy:**  
- Add a “standards-grounded baseline” banner: all feasibility statements about 24 vs 30 kbps should explicitly say “under CCSDS-derived \(\gamma_{24}=0.760\)” (or “under simplified slot-only \(\gamma=0.949\)”).  
- Audit and correct: Abstract; Section IV-A (“24 kbps nominal no loss: zero deadline misses”); Table VI; Table VII; any mention of “margin 623 ms at 24 kbps.” Under \(\gamma=0.76\), 24 kbps appears infeasible for \(k_c=100\) in Table XXIII; reconcile.

3) **Three-layer feasibility framework is conceptually good but currently mixes “necessary condition” and “decision rule” in a way that could mislead practitioners**  
**Why it matters:** The paper sells an actionable sizing workflow (Algorithm 1). Practitioners may apply the “\(\eta_{\text{total}}/\gamma < 0.50\)” threshold as if it were a general MAC/TDMA decision boundary, but half-duplex schedulability depends on *ingress/egress structure*, not only total utilization.  
**Specific remedy:**  
- Reframe the framework explicitly as:  
  - Layer 1: message-byte feasibility (per-node budget)  
  - Layer 2: coordinator ingress capacity (bottleneck link)  
  - Layer 3: TDMA airtime schedulability (half-duplex timing)  
  and clearly label \(\eta_{\text{total}}/\gamma\) as a *coarse utilization indicator*, not a TDMA/CSMA switch criterion.  
- Replace the “0.50” rule with a derived inequality using your own ingress/egress equations (Eqs. 33–34): e.g., require \(T_{\text{ingress}}+T_{\text{egress}}\le T_c\) (already there) and reserve the utilization ratio for intuition only.

4) **DES “verification” still risks being perceived as self-confirmation; distributional results need to be tied to concrete design decisions**  
**Why it matters:** The manuscript anticipates this critique (“expected by construction”), which is good, but then leaves the DES contribution underdeveloped. For a top-tier journal, the DES should either (i) validate a phenomenon not in the closed form, or (ii) be reduced in prominence.  
**Specific remedy:**  
- Strengthen the DES value proposition by extracting *actionable* tail-driven sizing outputs: e.g., “buffer size required to keep drop probability <10⁻⁶ under ON/OFF campaigns with parameters X,” or “coordinator ingress capacity multiplier vs. d and burst length.”  
- Alternatively, compress DES sections and emphasize the slot-level and packet-level simulators as the true cross-model validation.

5) **Campaign duty factor \(d\) is a good addition but still underspecified as a workload realism model (especially for command locality and correlation across clusters)**  
**Why it matters:** The earlier workload realism concern was “continuous commands are unrealistic.” You now contextualize \(d=1\) as an upper bound and provide scenarios—this is an improvement. However, \(d\) is applied as a per-node Bernoulli (or ON/OFF) gate that appears independent across clusters/nodes, while real campaigns are often *highly correlated* (many nodes commanded together) and may change addressing mode (broadcast vs unicast) and message size.  
**Specific remedy:**  
- Define clearly whether \(d\) is: (i) per-node independent, (ii) per-cluster correlated, or (iii) fleet-correlated. Provide at least one correlated-fleet case since it is worst for coordinator bursts and fleet-level RF reuse (Eq. 19).  
- Tie \(d\) to command semantics: if commands are broadcast Type 1, then “campaign” may be one message per cluster per cycle, not per node. Your current stress-case assumes 512 B per node per cycle, which is extremely pessimistic for many real “fleet reconfiguration” actions.

6) **Stress-case \(\eta_S \approx 46\%\) is better contextualized, but the paper still blurs “stress-case for bytes” vs “continuous-duty for airtime”**  
**Why it matters:** Readers may conflate “46% overhead” with “nearly saturating the channel,” yet airtime feasibility is dominated by coordinator ingress slots and half-duplex partitioning, not only \(\eta\). Also, the stress-case uses centralized command generation and per-node command volume that may not reflect plausible autonomy architectures.  
**Specific remedy:**  
- Explicitly label stress-case as: “continuous per-node command volume upper bound under centralized command semantics,” and provide an additional “broadcast campaign” stress-case where commands are cluster-broadcast only (one 512 B per cluster per cycle). This would give practitioners a more realistic high-end envelope and show how much of 46% is an artifact of per-node commands.

7) **Packet-level validation (Section IV-J) is the strongest independent anchor, but it stops short of being a true end-to-end validation of \(\gamma\)**  
**Why it matters:** You claim \(\gamma=0.76\) is “standards-derived” and then use it as a design constant. But \(\gamma\) also depends on implementation specifics (acquisition dwell, guard policy, ranging frequency, coding/interleaving, packetization). Without a sensitivity band, “0.760” can look over-precise.  
**Specific remedy:**  
- Present \(\gamma\) as an interval with a nominal value: e.g., \(\gamma\in[0.70,0.82]\) with a decomposition table and the parameters that drive variation (acq dwell 2–10 ms; guard 2–8 ms; code rate 1/2–7/8).  
- Add a short “practitioner recipe”: given radio spec sheet parameters, compute \(\gamma\) and then compute required \(R_{\text{PHY}}\). This would also increase the practical value of Eq. (44).

8) **Coordinator ingress sizing equation and the half-duplex partition parameter \(\alpha_{\text{RX}}\) need clearer derivation and dependence on assumptions**  
**Why it matters:** \(\alpha_{\text{RX}}=0.918\) is treated as a fixed derived constant at \(k_c=100\), but it depends on slot model, PHY rate (via \(\gamma\)), and whether acquisition is per-slot or amortized. This directly affects unicast staggering (Eq. 31–32) and feasibility margins.  
**Specific remedy:**  
- Define \(\alpha_{\text{RX}}\) explicitly as \(\alpha_{\text{RX}} = T_{\text{ingress}}/T_c\) under the *same* slot model used for feasibility.  
- Recompute \(L_{\text{cmd}}\) using the standards-grounded slot model (and show the difference vs the simplified model). If 22 cycles changes materially, update.

---

# Minor Issues

1) **Table VI vs Section IV-A vs Table XXIII numeric mismatch**: reconcile slot duration (92.7/111.5/115.5 ms), ingress time (9.177/9.445/11.435 s), and margin values.  
2) **Equation (27) \(\gamma=88.0/92.7=0.949\)** uses “data portion 2112 bits” but earlier you list payload 2048 + (32+16+16)=2112; later CCSDS framing overhead is 104 bits. Clarify which framing model is used in each place.  
3) **“TDMA required when \(\eta_{\text{total}}/\gamma > 50\%\)”**: mark as heuristic and cite/justify or remove.  
4) **AoI section**: Table IX “Full reporting” line says \(\eta=46\%\) includes stress-case commands; that is not “telemetry” and may confuse. Consider renaming “exception telemetry” experiment to “exception reporting workload.”  
5) **Centralized baseline**: consider adding one sentence quantifying uplink contact/spectrum constraints to avoid misinterpretation even with the caveat.  
6) **GE model**: you vary coherence time in Fig. 14 but the definition of “slots” vs “coherence steps” should be explicit (is coherence measured in slot durations or attempts?).  
7) **Fleet reuse (Eq. 19)**: time-sharing groups \(G\) assumes perfect scheduling and no inter-group guard; mention this is optimistic and would be tightened by NS-3 or a simple interference model.  
8) **Terminology**: “MAC efficiency” \(\gamma\) includes framing/FEC/acquisition; that’s broader than MAC. Consider calling it “PHY+MAC slot efficiency” or “airtime efficiency” to reduce pedantic objections.  
9) **Coordinator rotation traffic excluded from \(\eta\)**: reasonable, but state explicitly whether it is excluded because it uses optical ISL and/or because it is infrequent; otherwise readers may think you are omitting a major cost.  
10) **References**: several are “non-archival; accessed Feb 2026.” For a journal paper, try to replace key factual claims (e.g., Starlink ops constraints) with archival or regulatory filings where possible (some already are).

---

# Overall Recommendation  
**Recommendation:** **Major Revision**

The manuscript has a strong and potentially publishable core: a clear sizing framework, an explicit separation of byte-budget vs airtime schedulability, and a valuable standards-grounded derivation of the efficiency factor \(\gamma\) that materially changes feasibility conclusions. The campaign duty factor \(d\) is a meaningful improvement over earlier “always-on” stress assumptions, and the stress-case is now more responsibly framed as a continuous-duty upper bound rather than a typical operating point.

However, the paper currently suffers from a critical consistency problem: different sections/tables imply contradictory slot durations, ingress times, and 24 kbps feasibility under the *same claimed* standards-derived \(\gamma\). Because the main conclusion (minimum viable coordinator PHY rate ≈30 kbps) is numerically tight, these inconsistencies undermine confidence. In addition, the DES portion still reads partly as self-verification; it should either yield concrete tail-driven sizing guidance or be deemphasized relative to the slot-/packet-level validation, which is genuinely informative.

---

# Constructive Suggestions (ordered by impact)

1) **Perform a full numeric audit and harmonize the slot model across the manuscript** (single source of truth for \(T_{\text{slot}}\), \(\gamma\), ingress time, and margins; update all dependent tables/figures).  
2) **Make the standards-grounded model the primary baseline**; explicitly label any simplified slot-only model as “illustrative” and avoid mixing its feasibility claims with CCSDS-derived \(\gamma\).  
3) **Refine the feasibility framework presentation**: treat \(\eta_{\text{total}}/\gamma\) as a coarse indicator, and make TDMA airtime inequalities (Eqs. 33–34) the actual decision criterion.  
4) **Strengthen workload realism around \(d\)** by adding at least one *fleet-correlated campaign* case and one *broadcast-only campaign* stress case; clarify whether per-node command every cycle is intended as a strict upper bound rather than a plausible autonomy workload.  
5) **Upgrade DES contribution**: translate CDF/tail results into explicit buffer sizing or ingress capacity multipliers vs. burst length and duty factor; otherwise compress DES verification text.  
6) **Present \(\gamma\) as a parameter band with sensitivity** (acquisition dwell, guard, code rate), and provide a practitioner-facing recipe for computing \(\gamma(R_{\text{PHY}})\) from a radio spec.  
7) **Clarify \(\alpha_{\text{RX}}\) and unicast staggering under the standards-grounded slot model**, and ensure \(L_{\text{cmd}}\) results are consistent with the corrected airtime budget.  
8) **Tighten claims around GE**: keep it as a sensitivity tool, but add explicit guidance: “if you measure average burst length \(1/p_{BG}\), read P95 recovery from Fig. 13b and size buffers accordingly.”

If the authors resolve the \(\gamma\)/slot-time inconsistencies and sharpen the practitioner-facing workflow, this could become a strong engineering-synthesis paper suitable for a top-tier aerospace systems journal.