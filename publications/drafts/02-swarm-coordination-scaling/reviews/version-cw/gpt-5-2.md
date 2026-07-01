---
paper: "02-swarm-coordination-scaling"
version: "cw"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-03-05"
recommendation: "Major Revision"
---

## 1. Significance & Novelty  
**Rating: 4 (Good)**  
The manuscript’s main contribution—closed-form, *per-cluster* sizing equations that connect message-layer byte budgeting to TDMA airtime feasibility with an explicitly parameterized slot-efficiency term—targets a real gap between “networking papers” (routing/DTN) and “swarm autonomy papers” (control/coordination) that rarely provide byte-accurate, schedulability-aware design rules. The emphasis on coordinator ingress as the binding constraint is practically valuable and, in my view, the strongest “design insight” in the paper.

Novelty is solid but not fully “breakthrough”: much of the structure resembles classical capacity/schedulability accounting, and the DES largely verifies the authors’ own equations. The paper’s novelty is therefore primarily in the *integration* (byte accounting + TDMA timing + workload duty-factor abstraction + practitioner-oriented lookup/algorithm), not in new theory.

---

## 2. Methodological Soundness  
**Rating: 3 (Adequate)**  
The paper is careful about internal V&V tiers and is unusually explicit about what is and is not validated. The slot-efficiency derivation anchored to CCSDS Proximity-1 framing (Model C) is a methodological improvement over arbitrary constants, and the separation into Test A (byte budget) and Test B (airtime) is a sound engineering approach.

However, several methodological choices limit credibility of quantitative recommendations: (i) the GE loss model is explicitly “what-if” and is not mapped to measured ISL behavior; (ii) the TDMA schedule is centrally perfect and interference-free with reuse handled by a coarse factor; (iii) the DES is cycle-aggregated and cannot expose within-cycle contention/queuing phenomena that often dominate MAC feasibility. These are acceptable for a *preliminary sizing* paper, but then the recommendation strength (e.g., “35 kbps recommended design point”) must be consistently framed as conditional.

---

## 3. Validity & Logic  
**Rating: 3 (Adequate)**  
The core logic—coordinator ingress determines minimum PHY rate; command load largely affects byte budget and egress staggering—is coherent and mostly consistent throughout. The manuscript also does a good job warning readers not to double-count heuristic vs. explicit TDMA checks.

Remaining logical weak points are: (a) the “three-layer feasibility framework” is described, but the manuscript sometimes oscillates between “two tests” and additional implied tests (raw/PHY conversions, half-duplex partitioning, reuse), which can confuse what is necessary vs. sufficient; (b) the use and meaning of \(\alpha_{\text{RX}}\) is subtle (derived from schedule, but then used in a bound that looks independent); (c) the ARQ feasibility argument depends strongly on reserved-slot ARQ design choices that are not fully specified (ACK placement, feedback delay, whether retransmissions consume ingress or a separate region, etc.).

---

## 4. Clarity & Structure  
**Rating: 4 (Good)**  
For a dense sizing paper, the structure is comparatively clear: notation table, explicit “Model C vs Model S” statement, boxed feasibility definition, rate ladder, and algorithmic summary all help. The manuscript is also commendably candid about validation gaps.

Clarity issues remain in a few critical places: “baseline” vs “overhead” vs “total utilization” is easy to misread; the relationship between the 1 kbps/node logical budget and the 35 kbps shared PHY channel is explained but still invites confusion; and the packet/slot efficiency section is long and could be tightened while preserving the key equations and tables.

---

## 5. Ethical Compliance  
**Rating: 5 (Excellent)**  
Strong reproducibility posture: code/data availability with a tag, parameter table, and environment. The AI-use disclosure is explicit and appropriately scoped (ideation + prose editing only). No human-subject or sensitive data issues.

One suggestion: include a “reproduction checklist” (exact commands, expected runtimes, figure regeneration mapping) to match best practices in computational aerospace papers.

---

## 6. Scope & Referencing  
**Rating: 4 (Good)**  
The paper is in-scope for IEEE TAES / Adv. Space Res. as a systems/communications sizing study for autonomy-enabled swarms. Referencing covers distributed algorithms, AoI, GE modeling, CCSDS, and constellation networking.

Still missing (or underused) are: (i) more direct links to satellite TDMA/DAMA scheduling literature beyond DVB-RCS2 (e.g., classic MF-TDMA scheduling and satellite return-link analysis); (ii) more explicit connection to CCSDS Proximity-1 operational modes and typical acquisition/turnaround values from vendor datasheets or mission reports (even if not measured, “typical” ranges would strengthen the uncertainty treatment); (iii) any comparison to existing smallsat ISL radios’ burst-mode timing and throughput (even if proprietary, many vendors publish indicative numbers).

---

# Major Issues

1) **Campaign duty factor \(d\): realism improved, but still not operationally grounded enough for the headline conclusions**  
- **Why it matters:** The manuscript’s key narrative is “stress-case \(\eta_S\sim 46\%\) is episodic; routine \(\eta\sim 5\)–10%.” This is plausible, but the mapping from mission phases to \(d\) (Table “Duty mapping”) is largely asserted. Without stronger grounding, readers may treat \(d\) as a tuning knob that can always “make the system feasible,” which undermines the sizing claim.  
- **Remedy:** Add a short quantitative “d derivation” subsection: for each phase, derive \(d\) from event counts and durations (e.g., orbit-raising burns/day, station-keeping maneuvers/week, update campaigns/month) and show sensitivity of feasibility to plausible ranges. Provide at least one worked example with numbers (not just table entries). If real data are unavailable, cite analogous operations (e.g., typical station-keeping cadence) and explicitly bracket uncertainty.

2) **Gamma unification (\(\gamma\approx 0.76\) CCSDS-based) is mostly consistent, but there are still places where Model S results can be misinterpreted as design-relevant**  
- **Why it matters:** The paper is at risk of “two gammas”: a standards-derived Model C used for recommendations, and a simplified Model S used to illustrate coupling. Even with labels, readers may incorrectly generalize Model S findings (especially Table IV-D / ARQ×TDMA coupling).  
- **Remedy:** (i) Move the Model S coupling table into an appendix or explicitly pair it with the corresponding Model C infeasibility statement in the caption *and* in the surrounding text (you do some of this, but tighten further). (ii) Add one Model C coupling result (even if trivial, e.g., “24 kbps always infeasible; 30 kbps has <X% margin; 35 kbps supports Mr=1 under assumed GE”) so that the coupling narrative is not anchored on the non-design model.

3) **Stress-case contextualization is improved (“continuous-duty upper bound”), but the paper still uses stress-case numbers in ways that read like expected operations**  
- **Why it matters:** A 46% overhead and 67% total utilization is a very heavy operational posture; if misread as typical, it could lead reviewers to conclude the architecture is marginal.  
- **Remedy:** Standardize language: whenever \(\eta_S\) or “full-load” appears, prepend “continuous-duty bound.” Add a single summary table that reports *time-weighted* annual utilization for an illustrative mission mixture (you partially do this in text) and ensure that mixture is consistent with your \(d\) mapping. Make the “<1% of time” claim traceable (show the arithmetic).

4) **“Three-layer feasibility framework” is not consistently defined; the paper should formalize what counts as a test vs. a conversion**  
- **Why it matters:** Practitioners will implement your Algorithm 1. Ambiguity about whether “MAC efficiency” and “half-duplex partitioning” are separate feasibility checks or embedded in Test B invites double counting or incorrect sizing.  
- **Remedy:** In one place (preferably right after the boxed definition), define:  
  - Layer/Test A: byte budget at information layer.  
  - Layer/Test B: airtime schedulability given \(\gamma(R)\) and schedule structure.  
  - Conversions: \(C_{\text{raw}}=C_{\text{info}}/\gamma\), half-duplex partitioning, etc., are *components inside Test B*, not separate tests.  
  Then ensure every later section uses exactly this terminology. Consider renaming “three-layer” to “two-test with embedded conversions” unless you truly introduce a third independent constraint.

5) **DES verification: the manuscript correctly admits it is largely tautological; the remaining “value beyond equations” needs to be made more defensible**  
- **Why it matters:** In TAES-style reviews, simulation that reproduces its own analytic model is often viewed as padding unless it produces new insight (e.g., tails, rare events, nonlinearity). You claim the tail/buffer sizing is the “sole non-tautological contribution,” which is honest—but then it should be strengthened or de-emphasized.  
- **Remedy:** Either (a) strengthen the tail result by exploring at least one additional burst model (e.g., heavy-tailed ON durations or self-similar arrivals) to show robustness/limits of the 1.3× rule; or (b) move DES details to an appendix and keep only the tail figure + a concise statement that DES is an implementation check and a tail estimator, not a validation.

6) **Packet-level validation (Section IV-J) is still not independent validation; it is parameter anchoring. This is fine, but the paper should avoid “validated via CCSDS” phrasing**  
- **Why it matters:** “Validated” implies comparison to measurements or implementations. Here \(\gamma\) is *derived* from standards framing plus assumed timing. You do state this, but wording elsewhere (“validated via CCSDS”) could be interpreted as external validation.  
- **Remedy:** Replace “validated via CCSDS” with “anchored to CCSDS framing” or “standards-derived parameterization.” Audit abstract/introduction/conclusion for any “validated” language around \(\gamma\).

7) **Generalized \(\gamma\) expression is useful, but practitioners need clearer guidance on how to measure/estimate \(T_{\text{acq}}\), \(T_{\text{guard}}\), and whether framing bits are FEC-coded**  
- **Why it matters:** Eq. (gamma_time) is only as good as the parameter instantiation. Many real radios have acquisition distributions, missed acquisitions, and nontrivial burst preambles; also, whether overhead is FEC-coded can vary. Small changes shift the 30 vs 35 kbps boundary.  
- **Remedy:** Add a short “parameter measurement protocol” box: what to log on a modem bench test, how to compute effective \(T_{\text{acq}}\) percentiles, how to treat reacquisition-per-burst vs per-slot, and a note on coding of framing bits for CCSDS Prox-1 vs alternatives. You already have a roadmap; make it more operational and tie it directly to Eq. (gamma_time).

---

# Minor Issues

1) **Notation consistency:** \(\gamma_{24}, \gamma_{30}\) sometimes appear as \(\gamma_C\) vs \(\gamma_{C,24}\). Standardize subscripts.  
2) **\(\alpha_{\text{RX}}\) values:** early text cites 0.908 at 30 kbps \(M_r=0\), later the walkthrough computes 0.792 at 35 kbps. That’s correct but can surprise readers—add a sentence explicitly stating \(\alpha_{\text{RX}}\) is rate-dependent because slot time changes.  
3) **Table captions:** Some captions are very long and include key interpretation; consider moving the most critical interpretation into the main text to improve skimmability.  
4) **AoI discussion:** You correctly note P99 is sampling-limited; consider adding one sentence connecting AoI to decision latency requirements for the stated “loose coordination” tasks (task assignment/orbit maintenance) vs tight formation.  
5) **Fleet reuse:** The reuse factor \(R\ge 3\) argument is explicitly order-of-magnitude; good. Still, add a brief note that adjacent-cluster interference may also reduce \(\gamma\) (effective slot efficiency) via increased guard/robust coding, linking fleet reuse back to the \(\gamma\)-conditional lookup.  
6) **Command sizes:** 512 B commands may be reasonable, but the paper would benefit from a brief sensitivity statement for \(S_{\text{cmd}}\) similar to the \(S_{\text{eph}}\) sweep (even one plot or a paragraph).  
7) **Algorithm 1:** Line 3 hard-codes \(\eta_0=5\%\). If \(\eta_0\) depends weakly on \(k_c\), either compute it or state it is a conservative constant bound.  
8) **Terminology:** “validated at per-cluster level” could be read as externally validated; consider “evaluated” or “verified internally.”

---

## Overall Recommendation  
**Recommendation:** **Major Revision**

The manuscript is promising and closer to publishable than many early-stage “swarm architecture” papers because it (i) explicitly decomposes feasibility into byte budget and TDMA airtime, (ii) provides closed-form sizing equations and an implementable algorithm, (iii) anchors slot efficiency to CCSDS framing rather than arbitrary constants, and (iv) is unusually transparent about the absence of external validation. The coordinator-ingress bottleneck identification and the rate ladder (20 kbps info → ~30 kbps min PHY → 35 kbps recommended under ARQ margin) are practically useful.

The main reasons for Major Revision are not presentation but scientific positioning and methodological completeness: the duty-factor realism and stress-case contextualization need to be more quantitatively grounded; the “two-test vs three-layer” framing should be made unambiguous to prevent misuse; and the ARQ×TDMA coupling story should not rely primarily on the non-design (Model S) timing model. Finally, Section IV-J should be carefully reworded to avoid any implication of external validation while still emphasizing the value of a standards-derived \(\gamma\) parameterization.

---

## Constructive Suggestions (ordered by impact)

1) **Add a quantitative derivation/justification of \(d\)** (with at least one worked mission example and sensitivity bounds).  
2) **Make the feasibility framework terminology airtight**: two tests, with explicit embedded conversions; remove/rename “three-layer” if it’s not truly independent.  
3) **Rebalance the ARQ×TDMA coupling evidence**: include at least one Model C coupling result or clearly demote Model S coupling to illustrative appendix material.  
4) **Audit and standardize all \(\gamma\) language** to “standards-derived/anchored,” not “validated,” and ensure no residual 0.85-era assumptions remain (I did not see 0.85, which is good).  
5) **Strengthen the non-tautological DES contribution** by either exploring a second burstiness model (heavy-tailed ON times) or tightening the claim to “illustrative only” and moving details to appendix.  
6) **Add a practitioner measurement box for Eq. (gamma_time)** (how to measure \(T_{\text{acq}}\), turnaround, guard contributors; whether overhead bits are FEC-coded).  
7) **Provide a brief sensitivity note for \(S_{\text{cmd}}\)** and/or command generation models (broadcast vs unicast mix), since command traffic dominates \(\eta\).