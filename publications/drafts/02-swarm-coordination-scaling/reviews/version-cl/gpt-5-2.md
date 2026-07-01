---
paper: "02-swarm-coordination-scaling"
version: "cl"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-03-03"
recommendation: "Major Revision"
---

## 1. Significance & Novelty  
**Rating: 4 (Good)**  
The manuscript tackles an important and under-served problem: *parametric, closed-form sizing* of coordination communications for very large autonomous swarms (10³–10⁵). The proposed “two-layer feasibility” decomposition (byte-budget utilization + TDMA airtime schedulability) is a useful framing for early-phase design and trade studies, and the explicit rate ladder culminating in a recommended PHY rate is practitioner-friendly. The strongest novelty is not a new protocol but a *design-equation toolkit* with clearly defined parameters (e.g., \(k_c, T_c, S\), \(d\), \(\gamma\), \(\alpha_{\mathrm{RX}}\)) and a workflow (Algorithm 1) that can be reused.

That said, some “novelty” claims are weakened by the fact that many results are direct algebraic consequences of the assumed message model and a fixed TDMA structure; the paper’s main value is in packaging and parameter anchoring rather than discovering new scaling laws.

---

## 2. Methodological Soundness  
**Rating: 3 (Adequate)**  
The methodology is generally coherent for a *preliminary sizing* paper: analytical accounting, a cycle-aggregated DES for distributional tails, and a slot-level simulator to expose TDMA timing/ARQ coupling. The explicit acknowledgment of the validation gap (no external ISL data/NS-3) is appropriate.

However, the DES is intentionally constructed to reproduce the equations (Tier-1 verification), so its evidentiary weight is limited. The slot-level simulator is the most methodologically valuable component, but several key assumptions (e.g., per-slot acquisition, guard derivation, retransmission slotting policy, half-duplex partitioning) materially drive conclusions (30 vs 35 kbps, ARQ infeasibility at 30 kbps) and need tighter specification and sensitivity treatment.

---

## 3. Validity & Logic  
**Rating: 3 (Adequate)**  
Internally, the paper is mostly consistent and the logic of the feasibility layers is sound: Layer-1 checks information-byte budget; Layer-2 checks superframe timing with \(\gamma\) and half-duplex partitioning. The separation between topology-dependent overhead \(\eta_0\) and workload-dependent command traffic \(\eta_{\mathrm{cmd}}\) is clear.

Key risks to validity stem from (i) realism/interpretation of the workload model (especially the stress case and duty factor), (ii) whether \(\gamma\) is applied *consistently* everywhere (including tables/heuristics), and (iii) whether the “recommended 35 kbps” conclusion is robust to alternative acquisition/FEC/guard assumptions and to more realistic retransmission and scheduling policies.

---

## 4. Clarity & Structure  
**Rating: 4 (Good)**  
The manuscript is unusually explicit for a sizing paper: notation table, mode map, rate ladder, superframe budget, and a claim/evidence tier map are all strong. The repeated reminders about “anchoring vs validation” and “Model S vs Model C” reduce reader confusion.

Opportunities remain: the story is long and occasionally repetitive (e.g., feasibility workflow, rate ladder, and multiple restatements of 24/30/35 kbps). Some definitions (e.g., \(\eta\) vs \(\eta_{\text{total}}\), “1 kbps design point” vs “coordination channel 35 kbps”) require careful re-reading; a single consolidated “assumption box” and a single consolidated “design outputs box” would help.

---

## 5. Ethical Compliance  
**Rating: 5 (Excellent)**  
Strong reproducibility posture: code + tag + environment versions + datasets and simulators are provided. AI disclosure is explicit and appropriately scoped (ideation + prose editing only). No human/animal subjects. This section meets (and exceeds) typical expectations.

---

## 6. Scope & Referencing  
**Rating: 3 (Adequate)**  
The paper is within scope for T-AES / space systems communications and autonomy, especially as a design/sizing contribution. References cover distributed algorithms, AoI basics, CCSDS standards, and some constellation networking.

Gaps: the MAC/TDMA literature for satellite crosslinks and proximity links is broader than cited (beyond DVB-RCS2). Also, there is limited engagement with existing LEO ISL implementations (even if only public high-level descriptions), and with analytical schedulability/real-time communication literature that could support the Layer-2 arguments (e.g., real-time TDMA/ARQ deadline analysis, network calculus as mentioned but not leveraged).

---

# Major Issues

1) **Workload realism: duty factor \(d\) is a good addition, but the traffic model still risks “self-fulfilling” conclusions**  
**Why it matters:** Many headline numbers (\(\eta_S\approx 46\%\), “commands dominate,” “routine \(\eta\approx 5\)–10%”) follow directly from assuming (a) 512 B commands, (b) per-cycle command generation under stress, and (c) independent Bernoulli gating with \(d\). Reviewers and practitioners will ask whether these assumptions match realistic coordination workloads (especially for 10⁵ nodes) and whether the chosen \(d\) mapping is defensible beyond anecdote.  
**Remedy:**  
- Add a short *workload justification table* linking each message type and size to a concrete coordination function (e.g., formation control, fault response, station-keeping) with citations where possible.  
- Replace or augment Bernoulli \(d\) with at least one *burst model* that is explicitly cluster-correlated and time-correlated as a first-class default (you already simulate ON/OFF; elevate it from “tail sensitivity” to a co-equal workload model).  
- Provide a “reverse sizing” example: given a mission phase with X maneuvers/day and Y parameters per maneuver, derive \(d\) and \(S_{\mathrm{cmd}}\) rather than selecting them.

2) **Stress-case contextualization improved, but still over-emphasized relative to operational claims**  
**Why it matters:** You now label \(\eta_S\sim 46\%\) as a “continuous-duty upper bound,” which is the right framing. But the manuscript still uses stress-case results to motivate safety-critical conclusions (e.g., TDMA necessity, “complete situational awareness loss”) and to anchor multiple tables. Readers may conflate the bound with typical operations.  
**Remedy:**  
- Reorganize results so that *nominal/event* cases lead, and stress-case is clearly a bounding envelope.  
- Add a figure showing \(\eta(d)\) and \(\eta_{\text{total}}(d)\) with annotated mission phases (from Table VIII) to visually demote \(d=1\) as exceptional.  
- When stating “TDMA required,” qualify: TDMA required **for the high-utilization regime** (e.g., \(\eta_{\text{total}}/\gamma \gtrsim 0.5\) or when deadline constraints bind), not universally.

3) **Gamma “unification” at 0.761/0.745 is a major improvement, but consistency checks are still needed across the manuscript**  
**Why it matters:** The paper’s central feasibility boundary (24 kbps infeasible, 30 kbps minimum, 35 kbps recommended) depends critically on \(\gamma\). Any lingering use of older values (e.g., 0.85) or mixing Model S and Model C in conclusions would undermine trust.  
**Remedy:**  
- Add an explicit “Model C is used for all feasibility claims” compliance checklist and audit: for every table/figure that implies feasibility, annotate the \(\gamma\) used.  
- Ensure *all* computed ratios \(\eta_{\text{total}}/\gamma\), rate ladders, and feasibility tables use the same \(\gamma(R_{\text{PHY}})\) function (Eq. 54) rather than a constant. Right now some places treat \(\gamma\) as a single number, others as rate-dependent; make that uniform.

4) **Three-layer feasibility framing is promising but currently mixes layers and terminology (byte budget vs MAC efficiency vs TDMA airtime)**  
**Why it matters:** You describe “two-layer” (byte budget + airtime) but also effectively introduce a third concept: “MAC efficiency scaling by \(1/\gamma\)” which is neither purely Layer-1 nor purely Layer-2. Practitioners could misapply the equations (e.g., multiply \(\eta\) by \(1/\gamma\) and also do a superframe check, double-counting).  
**Remedy:**  
- Formalize the framework as **three explicit layers** (as the prompt notes):  
  1) Information-byte budget (messages and payload bytes)  
  2) Data-link/PHY efficiency mapping (payload → raw airtime via \(\gamma\))  
  3) TDMA/half-duplex schedulability (slot placement + RX/TX partition)  
- Provide a single “do not double count” note with an example: show how a 256 B report maps to time once via \(\gamma\) and then via TDMA schedule.

5) **DES verification provides limited incremental value; the paper should be clearer on what is actually learned from DES**  
**Why it matters:** You correctly state that DES reproducing the equations is code verification, not validation. But the paper still spends significant narrative effort on DES agreement. The incremental value seems to be (i) tails under bursty duty models and (ii) buffer sizing heuristics. These should be the headline DES contributions.  
**Remedy:**  
- Condense mean-matching discussion to a short V&V paragraph and move detailed agreement statements to an appendix or repository note.  
- Expand the distributional results: provide quantitative tail metrics (e.g., P95/P99 ingress bytes, overflow probability vs buffer size) across at least two workload correlation models (Bernoulli vs ON/OFF vs cluster-correlated), and show how those tails translate into coordinator buffer sizing or required \(C_{\mathrm{coord}}\).

6) **Packet-level “validation” of \(\gamma\) is helpful anchoring, but it is not independent validation; the manuscript should avoid over-selling it and strengthen it**  
**Why it matters:** Section IV-J is framed appropriately as parameter anchoring, but the packet-level simulator is still essentially implementing the same accounting. The real question is whether the assumed framing/acquisition/guard are representative for the targeted ISL radio and whether per-slot acquisition is required.  
**Remedy:**  
- Strengthen by adding a *hardware/standard mapping table*: Prox-1 is a protocol; many modern ISLs have different acquisition and framing. Provide at least 2–3 alternative “profiles” (e.g., Prox-1-like, continuous tracking, different framing overhead) and show resulting \(\gamma\) and the minimum feasible PHY rate.  
- Explicitly separate “standards-derived example” from “recommended for ISL design” and state conditions under which Prox-1 assumptions are conservative or optimistic.

7) **ARQ × TDMA coupling result is valuable but depends on retransmission policy and slot allocation assumptions that are under-specified**  
**Why it matters:** The conclusion “30 kbps insufficient for intra-cycle ARQ under blockage-dominated coherence” is plausible, but it hinges on: how retransmission slots are provisioned, whether they preempt egress, whether selective repeat vs go-back-N, ACK timing, and whether retransmissions can be deferred without “deadline miss” being catastrophic.  
**Remedy:**  
- Specify the retransmission mechanism precisely (ACK/NACK timing, number and placement of retransmission slots, whether retransmissions replace future nodes’ slots, etc.).  
- Add sensitivity: show miss rate vs number of reserved ARQ slots (or ARQ budget fraction), not just vs PHY rate.  
- Consider an alternative policy: **no intra-cycle ARQ, but prioritized inter-cycle retransmission**; quantify AoI/delivery impact vs the current “deadline miss” metric.

8) **Half-duplex partitioning and \(\alpha_{\mathrm{RX}}\) treatment needs tightening**  
**Why it matters:** \(\alpha_{\mathrm{RX}}\) is derived from schedule and drives the PHY-rate requirement. But in several places it is treated as a parameter/value (e.g., notation table lists 0.908 at a specific case). This can confuse readers into thinking it is an independent knob.  
**Remedy:**  
- Define \(\alpha_{\mathrm{RX}}\) formally as an *output* of Layer-2 scheduling and remove it from the notation table as if it were an input (or mark it explicitly as derived).  
- Provide a general expression for \(\alpha_{\mathrm{RX}}\) under your superframe structure (ingress slots + fixed egress components), and show how it changes with \(k_c\), \(S\), and \(R_{\mathrm{PHY}}\).

9) **Claims about “TDMA required” and “CSMA suffices” at ≥10 kbps are too strong without contention/hidden terminal modeling**  
**Why it matters:** At low utilization, random access often works, but “CSMA suffices” is topology-, propagation-, and radio-dependent, and in space half-duplex and long propagation can break terrestrial CSMA intuitions. Without NS-3 or analytical contention bounds, this reads as an overreach.  
**Remedy:**  
- Rephrase as: “At ≥10 kbps, the *airtime budget is non-binding* under the assumed traffic; contention performance is not evaluated.”  
- Optionally add a simple contention bound (e.g., slotted ALOHA throughput limit vs offered load) consistently across regimes rather than invoking CSMA.

---

# Minor Issues

1) **Terminology:** “1 kbps design point” is repeatedly used, but the coordination channel is 30–35 kbps PHY. Consider consistently saying “1 kbps per-node information budget within a 30–35 kbps shared PHY.”  

2) **Equation/units audit:** Eq. (54) \(\gamma\) expression mixes bps and kbps with a \(10^{-3}\) factor; it is easy to misapply. Provide a unit-checked version (all in SI) or explicitly define \(R_{\mathrm{PHY}}\) units in that equation line.  

3) **Table II (Design Equation Scaling):** The AoI row being invariant across bandwidth regimes is correct under your assumptions, but many readers will find it counterintuitive. Add a one-line explanation in the table caption or a footnote: AoI is dominated by sampling policy, not service, in that regime.  

4) **Global-state mesh calculation:** The 73 MB/node/cycle figure depends on gossip rounds and forwarding; show the intermediate assumptions explicitly (rounds × payload × fanout).  

5) **Static topology:** You justify reassociation overhead as <0.3–0.5%, but the more important effect is transient coordination quality (AoI spikes, command routing disruption). You mention it as future work; consider adding one quantified “worst-case transient” example even if coarse.  

6) **Acquisition assumptions:** The paper sometimes treats 5 ms acquisition as “typical S-band ISL” and elsewhere as Prox-1-like. Tighten wording: “assumed” vs “standard-derived” vs “hardware-typical.”  

7) **Figure referencing:** Ensure every figure file name includes extension consistently (e.g., `fig-unicast-stagger` missing `.pdf` in the LaTeX snippet).  

8) **Baseline 20.5%:** This is clear but easy to forget. Consider adding \(\eta_{\text{total}}\) in more plots/tables rather than \(\eta\) alone to prevent misinterpretation.

---

## Overall Recommendation  
**Recommendation:** **Major Revision**

The paper has a strong, publishable core as a preliminary design/sizing framework, with unusually good transparency about assumptions, and a genuinely useful standards-grounded \(\gamma\) derivation that supports the 24/30/35 kbps boundary argument. The duty factor \(d\) addition is a meaningful improvement toward workload realism, and the stress-case is now more appropriately framed as an upper bound.

The primary reasons for Major Revision are (i) several conclusions remain highly sensitive to under-specified MAC/ARQ/superframe policy choices, (ii) the feasibility framework needs clearer layer separation to prevent double counting and misuse, and (iii) the evidentiary value of DES and packet-level simulation should be refocused on what they truly add (tails, policy sensitivity, parameter anchoring) rather than equation confirmation. Addressing these issues would substantially increase practitioner confidence and make the contribution more durable across different radio/link implementations.

---

## Constructive Suggestions (ordered by impact)

1) **Formalize feasibility as a three-layer framework (info bytes → \(\gamma\) mapping → TDMA schedulability)** with a one-page “how to apply” recipe and a worked numerical example that carries a single configuration through all layers without switching models.

2) **Strengthen workload realism around \(d\):** elevate ON/OFF and cluster-correlated duty models to first-class defaults; add a reverse-derived \(d\) example from mission operations; provide a sensitivity plot \(\eta(d)\) and coordinator buffer P99 vs \(d, L_{\text{on}}\), and correlation scope.

3) **Tighten and expand ARQ × TDMA analysis:** fully specify retransmission policy; add sensitivity to reserved ARQ airtime; compare “no intra-cycle ARQ + prioritized inter-cycle recovery” vs current policy using delivery/AoI and deadline miss.

4) **Make \(\gamma\) application fully consistent and auditable:** one table summarizing \(\gamma(R)\) for the rates used; annotate each feasibility claim with Model C; ensure no residual Model S numbers leak into conclusions.

5) **Broaden the \(\gamma\) anchoring beyond Proximity-1:** add 2–3 alternative framing/acquisition profiles representative of modern ISLs and show how the minimum PHY rate shifts; this will make Eq. (54) and the generalized \(\gamma\) expression more useful to practitioners.

6) **Rephrase “CSMA suffices” claims** to avoid implying contention performance is proven; limit to airtime non-binding statements unless you add even a simplified contention model.

7) **Condense Tier-1 verification narrative and expand Tier-1 tail results** into actionable buffer sizing guidance (e.g., required buffer factor for 10⁻³ overflow probability under each duty model).

If the authors implement the above, the manuscript would be much closer to a strong T-AES contribution: a reusable sizing methodology with clearly bounded validity, robust sensitivity treatment, and practitioner-ready equations.