---
paper: "02-swarm-coordination-scaling"
version: "cv"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-03-05"
recommendation: "Major Revision"
---

## 1. Significance & Novelty  
**Rating: 4 (Good)**  
The manuscript targets an important and under-served niche: *closed-form, per-cluster sizing* for hierarchical coordination in very large space swarms under explicit byte budgets and TDMA airtime constraints. The two-test feasibility framing (byte budget + TDMA schedulability) and the emphasis on a *rate ladder* from information-rate → PHY-rate is practically valuable. The paper’s novelty is less in new algorithms and more in *engineering design equations* plus a coherent parametric workflow (Algorithm 1) grounded (at least parametrically) in CCSDS framing.

That said, the contribution is bounded by (i) lack of external validation (acknowledged), and (ii) reliance on a simplified traffic model and highly idealized MAC assumptions (central scheduling, no inter-cluster interference). For T-AES/ASR, this is acceptable as a “design sizing framework” paper, but only if the limitations are tightly scoped and the independent anchoring is strengthened.

---

## 2. Methodological Soundness  
**Rating: 3 (Adequate)**  
The modeling stack is generally sensible for early-phase sizing: analytical byte accounting + TDMA time budget + DES for distributional effects + slot simulator for deadline misses + a standards-derived parameter estimate for \(\gamma\). The explicit separation between internal verification and true validation is a strength.

However, several methodological choices weaken the evidentiary chain:
- The DES is largely confirming its own accounting equations; its incremental value is mainly the buffer-tail under ON/OFF campaigns, which is currently too dependent on an assumed burst model.
- The “packet-level validation” in IV-J is not independent validation; it is a parameter derivation from a standard plus assumed timing constants. That is fine, but it should not be framed as “validation” beyond parameter anchoring.
- The GE model is explicitly “what-if,” but the ARQ feasibility conclusions depend strongly on the *coherence assumption* (state constant over \(T_c\)), which makes intra-cycle ARQ “structurally ineffective.” This is transparent, but it also means the ARQ result is not robust unless you show sensitivity to coherence time / transition granularity.

---

## 3. Validity & Logic  
**Rating: 3 (Adequate)**  
The internal logic is mostly consistent, and Version CV improves transparency: you now clearly label Model C as decision-relevant and Model S as an upper bound, and you contextualize the \(\eta_S \approx 46\%\) case as a continuous-duty bound with small duty factor in practice.

Key remaining validity concerns:
- The feasibility framework is described as “two-test,” but in practice you employ (a) byte budget, (b) TDMA airtime, and (c) a heuristic lower bound (Eq. 19 / “design heuristic”). You warn not to double-apply it, but the manuscript still risks confusing readers about whether there are *two* or *three* checks.
- The distinction between *information-rate requirement* and *PHY-rate requirement* is good; however, \(\alpha_{\mathrm{RX}}\) is “derived from schedule” yet also used in Eq. (19) as if it were an independent partition parameter. This is logically fine if you consistently define the schedule first, but the narrative sometimes treats \(\alpha_{\mathrm{RX}}\) as a design knob.
- The “gamma unification” appears improved (0.761/0.745 etc.), but the paper must ensure no residual use of the older 0.85 assumption in any figure/table text, captions, or intermediate computations (see Major Issue #2).

---

## 4. Clarity & Structure  
**Rating: 4 (Good)**  
Strengths:
- Clear notation table and explicit Model C vs Model S statement early.
- The rate ladder (Table 6) is an effective device for practitioners.
- The manuscript repeatedly flags what is and is not used for recommendations.

Weaknesses:
- The paper is long and occasionally repetitive (multiple restatements of “not externally validated,” “Model S not for design,” etc.). This is defensible for transparency but could be tightened.
- Some claims are easy to misread as stronger than intended (e.g., “recommended 35 kbps” feels definitive despite dependence on assumed \(T_{\mathrm{acq}}\), \(T_{\mathrm{guard}}\), and no contention/interference).

---

## 5. Ethical Compliance  
**Rating: 4 (Good)**  
- Data/code availability is strong (GitHub tag, environment versions, runtime).
- AI disclosure is present and appropriately scoped (editing/ideation only).
- No human/animal subjects.

Remaining reproducibility gap: the paper should explicitly state whether the repository contains *all* scripts to regenerate each figure/table from raw runs (including seeds/configs) and whether results are deterministic given provided seeds.

---

## 6. Scope & Referencing  
**Rating: 3 (Adequate)**  
The literature coverage is broad across distributed systems, swarm robotics, and space networking. CCSDS anchoring is appropriate for T-AES. However:
- MAC/TDMA scheduling literature specific to satellite ISLs and demand-assigned TDMA (beyond DVB-RCS2) is thin; there is limited engagement with modern LEO ISL MAC work (even if proprietary, there is still academic literature on scheduled MAC under Doppler/beam steering).
- Queueing theory is invoked (MMPP/D/1), but the paper does not connect to established results/bounds for MMPP queues that could strengthen the buffer-sizing claims.

---

# Major Issues

1. **The “three-layer feasibility framework” is described inconsistently (2-test vs 3 checks), risking reader confusion and misapplication.**  
   **Why it matters:** Practitioners will implement this as a checklist. If “byte budget + MAC efficiency + TDMA airtime” are treated as separate gates, one can double-count \(\gamma\) or apply Eq. (19) incorrectly. The manuscript already warns about this, which indicates the risk is real.  
   **Remedy:**  
   - Make the framework explicitly either **two-layer** (bytes + airtime) *or* **three-step** (bytes → convert to raw via \(\gamma\) → airtime). If you keep “two-test,” then present the \(\gamma\) conversion as a *unit conversion inside Test B*, not as its own “layer.”  
   - Add a single consolidated “Feasibility flow diagram” (one figure) that shows: (i) compute \(\eta_{\mathrm{total}}\); (ii) compute slot time via Eq. (18); (iii) compute ingress/egress/ARQ airtime; (iv) decide feasibility.  
   - In Algorithm 1, consider removing or demoting Eq. (19) to an *optional* cross-check section, since Algorithm 1 already computes \(T_{\mathrm{ing}}\) explicitly.

2. **Gamma unification (0.76 CCSDS-based replacing earlier 0.85) must be audited for complete consistency across all results and narrative.**  
   **Why it matters:** \(\gamma\) is the central “bridge parameter” between message layer and airtime feasibility. Any residual inconsistency invalidates the rate ladder and the 24 vs 30 kbps infeasibility boundary.  
   **Remedy:**  
   - Add a short “Consistency audit” subsection or appendix table listing every place \(\gamma\) is used (tables/figures/equations) and confirming Model C values (\(\gamma_{24}=0.761\), \(\gamma_{30}=0.745\), \(\gamma_{35}=0.732\), etc.).  
   - Ensure Table 2, Table 10, Table 11, Fig. 7 labels, and any intermediate “\(\approx 0.70{-}0.76\)” ranges are aligned with the rate-dependent definition.  
   - If any plots still show a single constant \(\gamma\), explicitly mark them as “constant-\(\gamma\) illustrative only” and keep them out of decision claims.

3. **Campaign duty factor \(d\): improved, but still not fully convincing as “workload realism” without stronger empirical/operational anchoring and clearer mapping to command generation semantics.**  
   **Why it matters:** The stress-case \(\eta_S\approx 46\%\) is large; the acceptability of the architecture hinges on the claim that such load is episodic and \(d\ll 1\). Reviewers will ask whether \(d\) is an arbitrary knob chosen to make results look feasible.  
   **Remedy:**  
   - Provide at least one *worked operational scenario* with a time budget: e.g., orbit-raising for X days with Y commands per satellite per hour, mapped to \(p_{\mathrm{cmd}}\) and \(d\). Right now Table 14 gives plausible \(d\) values, but it remains heuristic.  
   - Clarify whether \(d\) gates **all command traffic** or only a subset (e.g., “reconfiguration campaigns”). If collision avoidance is modeled as \(d=1\) during events, show how long those events last and how frequently they occur, then compute the annualized utilization (you partially do this; expand it into a single coherent calculation).  
   - Consider adding sensitivity: show \(\eta_{\mathrm{total}}\) vs \(d\) for multiple \(S_{\mathrm{cmd}}\) and \(p_{\mathrm{cmd}}\) combinations to demonstrate robustness.

4. **The DES “verification value-add” is still thin; distributional/buffer results depend heavily on an assumed ON/OFF campaign process and do not generalize.**  
   **Why it matters:** If DES mainly re-confirms the analytical mean, it does not justify its complexity in a top-tier journal unless the tail results are robust and actionable.  
   **Remedy:**  
   - Either (a) strengthen the tail analysis by testing multiple burst models (e.g., heavy-tailed ON durations, self-similar traffic, cluster vs regional correlation) and showing how buffer multiplier \(M\) changes, *or* (b) reposition DES as an implementation sanity check and remove strong buffer-sizing prescriptions (e.g., “\(M=1.30\)”) that are not model-robust.  
   - If you keep the buffer rule, provide confidence intervals and quantify sensitivity to \(L_{\mathrm{on}}\), correlation scope, and \(d\).

5. **Packet-level “validation” (IV-J) is not independent validation; it is parameter estimation with assumed timing constants. This is acceptable, but the paper still risks overstating it.**  
   **Why it matters:** The paper’s central numeric recommendation (30 kbps minimum, 35 kbps recommended) depends strongly on \(T_{\mathrm{acq}}\) and guard/turnaround. Without measurement, the recommendation should be framed as conditional.  
   **Remedy:**  
   - Rename IV-J to “Standards-based \(\gamma\) parameterization” (you already lean this way) and avoid the term “validation” except in the “validation roadmap.”  
   - Provide a table of assumed timing constants with sources/justification (some are in Table 12, but consolidate): \(T_{\mathrm{acq}}\), turnaround, guard components, ACK timing.  
   - Add a simple “if-then” practitioner guidance: e.g., “If modem supports burst reacquisition with \(T_{\mathrm{acq}}\le 2\) ms, 30 kbps may suffice; otherwise 35 kbps.”

6. **Generalized \(\gamma\) expression: useful, but practitioners need clearer guidance on what to measure and how to map modem specs to \(T_{\mathrm{acq}}\), \(T_{\mathrm{guard}}\), framing, and FEC.**  
   **Why it matters:** Eq. (18) is one of the paper’s most reusable outputs. As written, it is correct but easy to mis-parameterize (e.g., whether framing is FEC-coded, whether acquisition is per slot or per burst, whether ACKs consume guard).  
   **Remedy:**  
   - Add a short “How to instantiate Eq. (18)” checklist: what fields to extract from CCSDS/implementation, whether ASM is included, whether ACK is separate, etc.  
   - Provide two complete example instantiations: (i) Prox-1 as done; (ii) a hypothetical alternative (e.g., continuous tracking \(T_{\mathrm{acq}}=0\), different FEC) to show how the recommendation shifts.

---

# Minor Issues

1. **Equation/notation consistency:** \(\eta=\eta_0+d\eta_{\mathrm{cmd}}\) is stated, but later \(\eta=\eta_0+\eta_{\mathrm{cmd}}\) appears in prose; ensure the “gated by \(d\)” form is used everywhere.  
2. **Table 2 (“Key Notation”)**: \(\alpha_{\mathrm{RX}}\) is listed as “\(\approx 0.908\)” but later varies with \(M_r\). Consider defining \(\alpha_{\mathrm{RX}}(M_r)\) or stating “nominal \(M_r=0\).”  
3. **AoI interpretation:** You correctly state AoI P99 is sampling-limited. Consider explicitly separating “network latency” vs “information staleness due to policy” in the metric section to avoid misinterpretation.  
4. **ARQ slot accounting:** The ACK-in-guard explanation in Table 11 footnote is subtle and will draw scrutiny. Consider a small timing diagram figure to make it unambiguous that no double counting occurs and that deterministic ACK placement is realistic.  
5. **Fleet reuse factor \(R=3\):** currently presented as order-of-magnitude. Ensure no downstream statements rely on it as if validated; consider moving it into Limitations earlier or adding a “fleet-level results are illustrative only” banner.  
6. **Centralized baseline:** The \(M/D/c\) bound is fine, but the comparison mixes compute-bound and spectrum/latency realities; ensure the baseline is clearly labeled as “intentional compute-only bound” (you do) and avoid implying it is a realistic competitor.  
7. **Typographic:** A few places use “kbps” for info-rate and PHY-rate in close proximity; consider consistently labeling units as “kbps (info)” vs “kbps (PHY)” in tables.

---

## Overall Recommendation  
**Recommendation:** **Major Revision**

The paper has a strong core idea (closed-form per-cluster sizing with a clear \(\gamma\)-anchored airtime model) and Version CV makes meaningful improvements: the campaign duty factor \(d\) is better contextualized; the stress-case \(\eta_S\approx 46\%\) is now explicitly framed as a continuous-duty upper bound; and the CCSDS-based \(\gamma\approx 0.70{-}0.76\) (rate-dependent) is a more defensible anchor than the earlier higher efficiency assumption. The rate ladder and Algorithm 1 are practitioner-friendly contributions.

The primary blockers are not “missing experiments” per se (you are transparent about the validation gap), but rather (i) potential confusion around the feasibility framework (two tests vs three checks), (ii) the need for a rigorous consistency audit of \(\gamma\) usage across all decision-relevant results, and (iii) strengthening the workload realism argument for \(d\) so that feasibility does not appear to hinge on an arbitrary knob. Additionally, the DES value proposition should be either broadened (robust tail analysis across burst models) or narrowed (verification tool only) to avoid over-claiming.

---

## Constructive Suggestions (ordered by impact)

1. **Unify and simplify the feasibility narrative:** present one canonical flow (bytes → slot time → airtime) and eliminate any appearance of a third independent “MAC efficiency test.” Add a single figure summarizing the flow.  
2. **Perform and publish a \(\gamma\) consistency audit:** ensure every table/figure/caption uses Model C values for decision claims; explicitly quarantine Model S to clearly labeled illustrative comparisons.  
3. **Strengthen \(d\) realism with one operationally grounded scenario:** map a mission phase (orbit-raising / reconfiguration) to actual command counts and durations, then compute implied \(d\), \(p_{\mathrm{cmd}}\), and annualized \(\eta\).  
4. **Either robustify or de-emphasize DES tail claims:** test at least one additional burst model (e.g., heavy-tailed ON durations) or remove strong buffer sizing “rules” that depend on a single ON/OFF assumption.  
5. **Reframe IV-J as parameterization, not validation, and add a practitioner instantiation checklist for Eq. (18).**  
6. **Add a small TDMA timing diagram for ACK/guard/acquisition/turnaround** to preempt detailed reviewer objections about double counting and feasibility margins.  
7. **Clarify ARQ conclusions as conditional on coherence time:** provide a small sensitivity showing how intra-cycle ARQ effectiveness changes when GE transitions occur per-slot vs per-cycle (you discuss it qualitatively; a quantitative plot/table would help).

If these revisions are made, the manuscript would be much closer to a publishable “design equations and sizing” contribution appropriate for a top-tier aerospace systems journal.