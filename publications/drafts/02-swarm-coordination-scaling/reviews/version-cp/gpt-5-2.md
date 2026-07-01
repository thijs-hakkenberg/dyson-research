---
paper: "02-swarm-coordination-scaling"
version: "cp"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-03-03"
recommendation: "Major Revision"
---

## 1. Significance & Novelty  
**Rating: 4 (Good)**  
The manuscript targets a real and under-served need: *parametric, closed-form sizing* for coordination traffic in very large swarms (10³–10⁵) with explicit byte accounting and an airtime feasibility layer. The two-layer feasibility framing (Layer 1 byte budget; Layer 2 TDMA airtime) is a useful engineering abstraction, and the paper is unusually explicit about what is and is not validated. The “rate ladder” and the conditional PHY recommendation based on measured \(\gamma\) are practitioner-oriented contributions.

Novelty is strongest in (i) the explicit decomposition of feasibility and the “do-not-double-count” guidance, (ii) the standards-anchored \(\gamma\) derivation replacing an assumed value, and (iii) the duty-factor \(d\) campaign model used to reconcile stress vs routine operations. The work is less novel in its queueing/AoI/GE ingredients individually; the novelty is the integrated sizing workflow and the engineering interpretation.

## 2. Methodological Soundness  
**Rating: 3 (Adequate)**  
The analytical accounting is generally careful, the slot-time model is clearly defined, and the paper now distinguishes Model C vs Model S appropriately. The DES is positioned as cycle-aggregated (message-level), which is appropriate for long-horizon campaign burstiness and buffer tails, and the slot-level simulator addresses a different failure mode (deadline misses). That separation is methodologically sound.

However, several modeling choices remain only partially justified for a top-tier aerospace systems journal: (a) the coordinator ingress “fluid server, drop-tail” abstraction is not clearly mapped to the TDMA superframe constraints (which are later enforced elsewhere), (b) the GE model’s coherence assumption (“transitions once per \(T_c\)”) is plausible but not validated and strongly drives the ARQ conclusions, and (c) MAC contention is explicitly out of scope—yet some conclusions (e.g., “at ≥10 kbps no TDMA analysis is needed”) implicitly assume contention-free service. These are acceptable if framed strictly as *preliminary sizing bounds*, but the manuscript occasionally reads like a design recommendation rather than a conditional estimate.

## 3. Validity & Logic  
**Rating: 3 (Adequate)**  
Internal logic is mostly consistent, and the manuscript does a better job than many papers at preventing unit/overhead double counting. The duty factor \(d\) is used coherently in Eq. (13) and Table VII to address realism concerns: routine \(d=0.01\)–0.10 yields \(\eta\approx 5\)–10%, while \(\eta_S\approx 46\%\) is clearly labeled as a continuous-duty bound.

Remaining validity risks are mainly about *interpretation*:
- The three-part mapping “byte budget → MAC efficiency (\(\gamma\)) → TDMA airtime” is presented as two layers plus a unit conversion; that is defensible, but only if \(\gamma\) is strictly a PHY/MAC “slot efficiency” and not also absorbing higher-layer scheduling losses. At times \(\gamma\) is described as “MAC scheduling abstracted,” which could be read as including contention/coordination overhead. Tighten that definition so \(\gamma\) is unambiguously *slot-structure efficiency under TDMA*, not a catch-all.
- The “35 kbps recommended” result is logically derived under Model C and a particular superframe partition; but the recommendation’s robustness depends on acquisition/ranging assumptions and on whether ACKs truly “fit inside guard” without increasing collision/guard requirements.

## 4. Clarity & Structure  
**Rating: 4 (Good)**  
The paper is well organized, with explicit notation, clear separation of models, and strong “what binds” explanations. The “rate ladder” table and the feasibility algorithm are particularly readable. The revised contextualization of stress-case and the explicit statement that DES agreement is code verification (not external validation) are commendable.

Clarity issues remain in a few places where readers may struggle to reconcile numbers across sections (e.g., \(\gamma_{24}\) vs \(\gamma_{30}\) usage, ingress times in different tables, and where exactly \(\alpha_{RX}\) is derived). Some tables mix Model S and Model C results; while labeled, it still risks confusion for skimming readers.

## 5. Ethical Compliance  
**Rating: 5 (Excellent)**  
Strong data availability statement with a tagged repository, environment, and runtime. Clear disclosure of AI-assisted editing/ideation and explicit statement that AI did not generate results/figures/data. This is above-average for reproducibility and disclosure.

## 6. Scope & Referencing  
**Rating: 4 (Good)**  
The manuscript is within scope for IEEE TAES / space systems networking and autonomy. References cover distributed algorithms, swarm robotics, DTN, CCSDS, AoI, and GE modeling. The CCSDS anchoring is appropriate and strengthens engineering credibility.

Gaps: you should cite more directly relevant satellite TDMA return-link / demand-assigned literature beyond DVB-RCS2 (e.g., classic DAMA/TDMA scheduling analyses, satellite MAC surveys, or LEO ISL MAC work) and, importantly, any open literature on smallsat crosslink radios and acquisition/turnaround timing. Even if no ISL GE measurements exist, cite closest analog measurement campaigns (LEO-to-LEO, aeronautical, or land-mobile satellite) to justify plausible parameter regimes.

---

# Major Issues

1) **The “three-layer feasibility framework” is conceptually right but still ambiguous in definition and boundary conditions**  
**Why it matters:** The paper’s core contribution is the decomposition into byte budget (\(\eta\)) and airtime schedulability (\(\gamma\)/TDMA). If \(\gamma\) is interpreted as absorbing “MAC effects” broadly (contention, scheduling inefficiency, control-plane overhead), then Layer 2 risks double-counting or miscounting; if \(\gamma\) is only slot-structure efficiency, then some claims about “no TDMA analysis needed at ≥10 kbps” become conditional on contention assumptions.  
**Remedy:**  
- Add a boxed definition early (end of Sec. I or start of Sec. IV) stating precisely:  
  - \(\eta\): information bytes generated by protocol above baseline telemetry, independent of PHY.  
  - \(\gamma\): *TDMA slot-structure efficiency* (payload time / slot time) including FEC/framing/guard/acquisition **only**, excluding contention and excluding higher-layer retransmission scheduling.  
  - Layer 2: deterministic superframe feasibility under a specified TDMA schedule and half-duplex partition.  
- Add an explicit “boundary conditions” paragraph: the framework assumes centrally scheduled TDMA within a cluster and no inter-cluster interference within a channel; contention is out-of-scope and would reduce effective throughput.

2) **Consistency and propagation of the updated \(\gamma\) unification (\(\approx 0.76\) CCSDS-anchored) needs one final audit pass**  
**Why it matters:** Prior versions apparently used \(\gamma=0.85\). In Version CP, you correctly anchor \(\gamma_{24}=0.761\) and \(\gamma_{30}=0.745\), but there are still places where \(\gamma\approx 0.76\) is used generically while computations use \(\gamma_{30}\), and some narrative statements may inadvertently imply a single constant \(\gamma\). This can cause readers to mistrust the rate ladder.  
**Remedy:**  
- Add a short “\(\gamma\) usage convention” bullet list: whenever computing feasibility at 30 kbps, use \(\gamma_{30}\); at 24 kbps use \(\gamma_{24}\); do not use \(\gamma\approx 0.76\) except as a coarse descriptor.  
- In the Abstract and Conclusion, replace “\(\gamma\approx 0.76\)” with “\(\gamma_{30}=0.745\) (CCSDS Prox-1, Model C)” when discussing the 27 kbps conversion, because that conversion is done at 30 kbps in Table VI. If you want a single number in the abstract, state a range: “\(\gamma\approx 0.74\)–0.76 for 24–30 kbps.”

3) **The stress-case \(\eta_S \approx 46\%\) is now labeled as episodic/upper bound, but its operational mapping remains weak and potentially misleading**  
**Why it matters:** Even with \(d\ll 1\), the paper still uses stress-case heavily in headline tables (e.g., Table II) and statements like “safety-criticality: undersizing causes complete situational awareness loss.” Readers may interpret 46% as a typical requirement rather than a bound. The duty factor \(d\) helps, but only if you show credible campaign distributions and durations that map to real ops.  
**Remedy:**  
- Add one explicit “workload realism” figure/table: e.g., a yearly timeline illustration with ON/OFF campaigns (orbit raising, station keeping, collision response) showing implied \(d\) and total time in stress-like modes.  
- Provide a conservative but plausible distribution for \(d\) across mission phases, not just point examples. Even a simple mixture model (e.g., 95% routine \(d=0.01\), 4.9% reconfig \(d=0.10\), 0.1% emergency \(d=1\)) would help.  
- Ensure every place that quotes \(\eta_S\) also states “continuous-duty bound; expected fraction of time \(<1\%\)” (you do this in several places—make it universal in captions and the scaling table).

4) **DES “verification” currently provides limited incremental value; strengthen the claim or reduce its prominence**  
**Why it matters:** You appropriately admit that DES matches closed-form means “by construction.” For TAES-level contribution, the DES should either (i) reveal emergent behavior not in the equations, or (ii) quantify tails under a rigorously specified stochastic process that cannot be captured analytically. Right now, the strongest incremental DES output is buffer tail multipliers under correlated ON/OFF campaigns, but the campaign processes are somewhat ad hoc and not tied to measured ops.  
**Remedy:**  
- Elevate the DES tail contribution by formalizing the campaign arrival model: specify the ON/OFF Markov parameters (transition probabilities) and correlation scope precisely, and justify them (even if only as design envelopes).  
- Add at least one sensitivity sweep showing how P99/mean buffer multiplier changes with \(L_{on}\), \(d\), and correlation scope. This would make the DES tail result a reusable design curve, analogous to your GE recovery sweep.

5) **Packet/slot-level validation in Sec. IV-J anchors \(\gamma\), but does not yet constitute “independent validation” of the overall framework**  
**Why it matters:** You correctly state it is parameter anchoring, not validation. However, several conclusions (30 kbps minimum; 35 kbps recommended) depend on additional timing elements (ACK mini-slots, ranging, acquisition variability, turnaround) that are partly assumed. The risk is that readers see CCSDS citations and infer stronger validation than warranted.  
**Remedy:**  
- Be explicit about which timing parameters are *from CCSDS* vs *assumed engineering values* (e.g., acquisition dwell 5 ms/slot, ACK-in-guard assumption, ranging 50 ms).  
- Provide a small “parameter provenance” table: each component (guard constituents, acquisition, ACK, ranging) with (standard citation / vendor typical / assumption).  
- If possible, add a simple worst-case bound: show feasibility at 30 kbps and 35 kbps under +X% acquisition and +Y ms guard to demonstrate robustness.

6) **Generalized \(\gamma\) expression is useful, but the practitioner guidance (“\(\gamma\)-conditional PHY”) needs tighter derivation and guardrails**  
**Why it matters:** The conditional mapping \(\gamma\in[0.70,0.80]\Rightarrow 35\) kbps etc. is attractive, but it risks being applied outside the assumed \(k_c, T_c, S\) regime. Practitioners may treat it as universal.  
**Remedy:**  
- State explicitly that the conditional PHY lookup is for the default \(k_c=100, T_c=10\,s, S=256\,B\) unless otherwise scaled.  
- Provide the scaled form: \(R_{\text{PHY,min}} \propto (k_c-1)S/T_c \cdot 1/(\gamma \alpha_{RX})\), and show how to recompute the lookup for other regimes (or provide a small nomogram/contour plot in \((k_c,S)\) space).

---

# Minor Issues

1) **Abstract numeric consistency:** “\(\approx 27\) kbps PHY-rate at \(\gamma=0.76\)” is fine as a rough number, but the main text uses \(\gamma_{30}=0.745\) giving 27.1 kbps. Consider stating “\(\gamma\approx0.74\)–0.76” or explicitly using \(\gamma_{30}\).  

2) **Table IV (Notation):** \(\gamma\) definition lists “Eq. (gamma_time); \(\gamma_{24}=0.761,\gamma_{30}=0.745\)”—good. Ensure every later use of \(\gamma\) in equations that depend on rate uses \(\gamma(R_{\text{PHY}})\) notation consistently.  

3) **Table X / Sec. IV-D (joint interaction):** Table VIII uses Model S slot timing, which is clearly labeled, but many readers will still over-interpret. Consider adding one sentence: “This table is *not* used in the 30/35 kbps recommendation; it only demonstrates coupling qualitatively.”  

4) **ACK “absorbed in guard” assumption (Table VII footnote a):** This is nonstandard; guard is typically for timing uncertainty, not protocol signaling. Clarify whether ACK occurs at a deterministic offset that does not require additional guard, or allocate explicit ACK time.  

5) **Ranging overhead (Table VIII):** “50 ms per node per cycle” seems large relative to the 730 ms margin; clarify whether ranging is truly per-node per-cycle in your assumed Prox-1 mode, or whether it is periodic/round-robin and amortized. If amortized, update Table VIII accordingly.  

6) **“At ≥10 kbps no TDMA analysis is needed” (Sec. I Contributions):** This is only true under your assumed traffic and under contention-free scheduling. Rephrase to: “airtime feasibility is non-binding under assumed TDMA scheduling and traffic; contention not evaluated.”  

7) **Global-state mesh numbers:** “73 MB/cycle per node” at \(N=10^5\) is plausible but will be challenged. Provide one-line derivation in a footnote (state vector size × N × gossip factor).  

8) **Failure model independence:** You acknowledge correlated failures are future work. Consider adding one sentence on how correlated failures would affect coordinator load (e.g., election storms) and whether your buffer sizing is robust.  

9) **Algorithm 1 (Layer 1 equation):** Line 3 uses \(p_{\text{cmd}}\) and \(d\) together; elsewhere \(d\) gates command generation. Ensure \(p_{\text{cmd}}\) is not double-gating with \(d\) (define whether \(p_{\text{cmd}}\) is conditional probability given “active campaign” or unconditional per-cycle probability).  

10) **Typographic/consistency:** Some places use “kbps” for PHY and “kbps info-rate”; you mostly label correctly, but a final consistency pass would reduce reviewer friction.

---

# Overall Recommendation  
**Recommendation:** **Major Revision**

The paper has a strong engineering core: a clear feasibility decomposition, closed-form sizing equations, and a standards-anchored \(\gamma\) that materially improves credibility over an assumed efficiency factor. The campaign duty factor \(d\) substantially improves workload realism by separating continuous-duty stress bounds from routine operations, and the manuscript is unusually transparent about validation limits and the purpose of each simulator. The “rate ladder” and feasibility algorithm are the right kind of artifacts for practitioners.

The key reasons for Major Revision are not about formatting but about *tightening definitions and strengthening the evidentiary story*: the boundaries between byte budget, slot efficiency, and TDMA schedulability must be made unambiguous; the updated \(\gamma\approx0.76\) anchoring should be propagated with strict consistency; and the DES/slot simulations should be positioned and/or extended so they provide design curves or robustness evidence beyond confirming the same assumptions. Finally, the “35 kbps recommended” conclusion is plausible under Model C, but it remains sensitive to assumed acquisition/ranging/ACK timing—these assumptions need clearer provenance and a robustness bound.

---

# Constructive Suggestions (ordered by impact)

1) **Add a one-page “Framework Definition & Applicability” section (or boxed text)**
   - Precisely define \(\eta\), \(\gamma\), Layer 1, Layer 2, and what is excluded (contention, inter-cluster interference, dynamic topology).
   - Include a short checklist: “If your system has X, recompute Y.”

2) **Do a full consistency audit of \(\gamma\) usage**
   - Replace generic \(\gamma\approx0.76\) statements with \(\gamma(R_{\text{PHY}})\) or \(\gamma_{24}/\gamma_{30}\) where computations depend on it.
   - Ensure the abstract/conclusion do not imply a single constant \(\gamma\).

3) **Strengthen workload realism with a minimal, explicit campaign mixture model**
   - Provide a conservative yearly duty-factor mixture and show resulting \(\eta\) distribution (not just mean).
   - Ensure the 46% stress-case is always explicitly “continuous-duty upper bound” in captions and summary tables.

4) **Make DES outputs into reusable design curves**
   - Sweep \(L_{on}\), correlation scope, and \(d\) to produce a “buffer multiplier” contour or curves (P95/P99 vs parameters).
   - This would convert DES from “verification” to “tail characterization tool.”

5) **Clarify timing parameter provenance and add robustness bounds for the 30/35 kbps conclusion**
   - Provide a provenance table and a worst-case sensitivity: e.g., +5 ms acquisition, +3 ms guard, explicit ACK time, and show whether 35 kbps still clears with margin.
   - Revisit the “ACK in guard” and “ranging 50 ms/node/cycle” assumptions—either justify strongly or amortize realistically.

6) **Guardrail the \(\gamma\)-conditional PHY lookup**
   - State explicitly it is for \(k_c=100, T_c=10s, S=256B\) unless rescaled.
   - Provide a generic rescaling recipe or a small nomogram.

7) **Tighten the interpretation of “≥10 kbps makes TDMA non-binding”**
   - Rephrase as “airtime non-binding under assumed TDMA schedule and traffic; contention not modeled.”
   - Optionally add a back-of-envelope contention margin statement (e.g., required utilization bound for slotted ALOHA vs TDMA).

If the authors address the above, the manuscript would be much closer to TAES standards: clearly scoped, internally consistent, and genuinely useful as a preliminary sizing reference with explicit applicability limits.