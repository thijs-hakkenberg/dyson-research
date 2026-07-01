---
paper: "02-swarm-coordination-scaling"
version: "da"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-03-05"
recommendation: "Major Revision"
---

## 1. Significance & Novelty  
**Rating: 4 (Good)**  
The manuscript targets an important and under-served niche: *closed-form* sizing relationships for hierarchical coordination traffic in very large space swarms under a fixed per-node bandwidth allocation, with explicit TDMA airtime feasibility rather than purely byte-counting. The “two-test” framework (Test A byte budget, Test B TDMA airtime) plus a standards-anchored slot-efficiency parameterization is a useful contribution for early-phase architecture trades. The paper is also unusually explicit about the validation gap and about what the simulations do *not* validate.

That said, novelty is partly incremental: much of the analysis is careful accounting plus deterministic TDMA timing, and the DES mainly verifies means already implied by the equations. The strongest differentiator is the *engineering-ready rate ladder* that ties cluster ingress to a minimum PHY rate with explicit guard/acquisition/FEC overheads, and the explicit separation of “continuous-duty bound” vs realistic duty-cycled campaigns.

---

## 2. Methodological Soundness  
**Rating: 3 (Adequate)**  
Core methodology (byte accounting + deterministic TDMA superframe timing + simple correlated-loss what-if model) is coherent for preliminary sizing. The CCSDS Proximity-1–based decomposition for \(\gamma(R_{\rm PHY})\) is a sensible anchoring choice given the lack of ISL measurements.

Main weaknesses are (i) the reliance on a *cycle-coherent* GE model that structurally makes intra-cycle ARQ ineffective (acknowledged, but it limits what conclusions can be drawn), (ii) ambiguity around the “three-layer feasibility” narrative vs the stated “two-test” framework, and (iii) some internal inconsistencies/notation issues (notably \(\alpha_{\rm RX}\) definition/usage) that matter because the paper positions itself as design-equation driven.

---

## 3. Validity & Logic  
**Rating: 3 (Adequate)**  
The logic of ingress being the binding constraint at 1 kbps/node and \(k_c\sim 100\) is convincing, and the contextualization of the \(\eta_S\approx 46\%\) case as a continuous-duty upper bound is much improved relative to typical “stress-case” presentations.

However, several claims still read stronger than the evidence supports. In particular: “24 kbps causes 100% deadline misses under Model C” should be carefully scoped to the specific superframe definition and assumptions (acquisition per slot, guard, half-duplex partition, etc.). Also, the equivalence/relationship between the heuristic \(R_{\rm PHY,min}\ge C_{\rm coord,info}/(\gamma\alpha_{\rm RX})\) and Test B is described, but the current presentation risks circularity because \(\alpha_{\rm RX}\) is itself a function of \(R_{\rm PHY}\) and the schedule. This is fixable by tightening the definition and providing a short proof/derivation.

---

## 4. Clarity & Structure  
**Rating: 4 (Good)**  
The manuscript is generally well organized: notation table, explicit “what the DES validates,” clear “rate ladder,” and a useful algorithmic summary. The repeated reminders that Model S is *not* for recommendations are good practice.

Remaining clarity issues: (i) the paper alternates between “two-test” and language that suggests a third layer/check (byte budget, MAC efficiency, TDMA airtime); (ii) some parameters are defined in a way that is syntactically confusing (e.g., \(\alpha_{\rm RX}\) in Table I appears to have a parenthesis/formatting error and mixes “computed output” with “canonical value”); (iii) the practitioner-facing “generalized gamma expression” is helpful, but it needs a cleaner “how to measure/estimate each term in practice” box and a sanity-check example using the exact numbers in Table IX to prove consistency.

---

## 5. Ethical Compliance  
**Rating: 4 (Good)**  
Strong data availability statement with a tagged repository and environment details. AI disclosure is explicit and appropriately limited to ideation/editing. No obvious ethical red flags.

One improvement: explicitly state whether the repository includes scripts to regenerate *all* figures/tables from raw simulation outputs, and whether random seeds/configs are preserved for bitwise reproducibility.

---

## 6. Scope & Referencing  
**Rating: 3 (Adequate)**  
Citations cover distributed algorithms, AoI, GE channels, CCSDS, and relevant constellation/networking work. For IEEE TAES / Adv. Space Res., the scope is acceptable.

Gaps: limited engagement with (i) satellite return-link DAMA/TDMA scheduling literature beyond DVB-RCS2, (ii) deterministic scheduling / real-time analysis that could strengthen Test B (e.g., network calculus / real-time TDMA schedulability results), and (iii) existing smallsat ISL modem characterization papers (even if not Prox-1) that could better justify acquisition/turnaround assumptions.

---

# Major Issues

1) **\(\alpha_{\rm RX}\) is underspecified and risks circular sizing logic**  
- **What:** The paper states \(\alpha_{\rm RX}=T_{\rm ing}/T_c\) is “computed output, not a free parameter,” yet it is also used in the heuristic \(R_{\rm PHY,min}\ge C_{\rm coord,info}/(\gamma\alpha_{\rm RX})\). But \(T_{\rm ing}\) depends on \(T_{\rm slot}\), which depends on \(R_{\rm PHY}\) and \(\gamma(R_{\rm PHY})\). As written, the heuristic can look like it uses \(\alpha_{\rm RX}\) as an independent constant (e.g., “Canonical: 0.908 at 30 kbps/Mr=0”).  
- **Why it matters:** This paper positions itself as providing *closed-form sizing equations*. Any perceived circularity or “plug in canonical values” undermines practitioner trust and can lead to incorrect use outside the default case.  
- **Remedy:**  
  - Define \(\alpha_{\rm RX}\) solely as a *derived schedule fraction* given a specific superframe design (ingress slots + optional ARQ reservation + egress).  
  - Provide a short derivation showing when the heuristic reduces to Test B (e.g., with negligible egress and \(M_r=0\)), and otherwise is a lower bound.  
  - Remove “canonical \(\alpha_{\rm RX}\)” from the notation table or clearly label it as “example value under default schedule at 30 kbps, \(M_r=0\)” and not to be reused.

2) **“Two-test framework” vs “three-layer feasibility (byte budget, MAC efficiency, TDMA airtime)” messaging remains inconsistent**  
- **What:** The abstract and boxed framework emphasize two tests, but the narrative repeatedly introduces MAC efficiency as if it were a separate feasibility layer/check. Equation (27) \(C_{\rm raw}=C_{\rm coord,info}/\gamma\) is correctly described as a unit conversion embedded in Test B, yet the paper’s framing still suggests a three-layer gate.  
- **Why it matters:** Reviewers/practitioners will interpret “three-layer feasibility” as three independent constraints, which can lead to double-counting or misapplication (the manuscript even warns against this).  
- **Remedy:** Make the hierarchy explicit and consistent everywhere:  
  - Either (A) keep “two tests” and describe \(\gamma\) strictly as a parameter within Test B (recommended), or (B) formally define a third “conversion layer” but then show it is not an independent test.  
  - Audit the Introduction/Abstract/Conclusion and ensure the same wording is used consistently.

3) **\(\gamma\) unification (0.76 via CCSDS) is mostly consistent, but there are still places where Model S results can be misconstrued as decision-relevant**  
- **What:** You correctly state “All feasibility claims use Model C,” but Table VII (ARQ×TDMA coupling) is Model S only, and it is easy to over-interpret the numeric miss rates as representative. Additionally, some earlier equations/sections (e.g., the initial derivation of \(\gamma=0.949\)) occupy a lot of space relative to the decision-relevant Model C results.  
- **Why it matters:** For a sizing paper, readers may cherry-pick optimistic Model S results (especially because they produce “nice” margins at 24 kbps) and miss the key conclusion that 24 kbps is infeasible under CCSDS-like timing.  
- **Remedy:**  
  - Move Model S to an appendix or compress it substantially.  
  - For Table VII, add a companion Model C version (even if trivial: 24 kbps always infeasible; 30 kbps marginal for ARQ; 35 kbps feasible) to prevent misinterpretation.  
  - Add a prominent “Model C only” banner on any figure/table that could be misread.

4) **Campaign duty factor \(d\) is a good addition, but workload realism still depends heavily on assumptions that need stronger grounding**  
- **What:** The duty-factor framing is improved and the “<1% of time” contextualization helps. However, the mapping from mission phases to \(d\) and \(p_{\rm cmd}\) is still largely illustrative, and some examples mix “campaign gating” and “per-cycle command probability” in ways that can confuse how commands actually arrive (burstiness, correlation scope, and command addressing mode).  
- **Why it matters:** Your headline utilization numbers (\(\eta\approx 5\)–10% routine; 46% continuous-duty bound) are central to the paper’s significance. If \(d\) is not credibly tied to operational scenarios, the results look arbitrary.  
- **Remedy:**  
  - Provide one or two concrete end-to-end workload instantiations (e.g., orbit-raising week, station-keeping month) with explicit: number of commands, addressing mode (broadcast/unicast fraction \(q\)), expected correlation scope, and resulting \(d\) and \(p_{\rm cmd}\).  
  - Clarify whether \(d\) gates *cycles* (ON/OFF periods) while \(p_{\rm cmd}\) gates *within-campaign per-cycle command generation*, and show a simple timeline example.

5) **DES “verification value” remains limited; the paper should sharpen what DES uniquely contributes**  
- **What:** The manuscript is admirably honest that Tier-1 DES agreement is code verification, not validation. Still, many DES results are presented alongside equations without adding new insight, risking the impression of “simulation to confirm algebra.” The one truly incremental item is the tail/buffer analysis under correlated campaigns.  
- **Why it matters:** TAES-level papers usually need either (i) external validation, or (ii) strong methodological novelty/rigor. If DES is mostly self-confirmation, the paper’s evidentiary weight rests on deterministic accounting alone.  
- **Remedy:**  
  - Rebalance: reduce DES mean-agreement plots/tables and expand the distributional analysis: sensitivity of buffer factor \(M\) to ON/OFF parameters, correlation scope, and drop probability targets.  
  - Alternatively, add at least one additional “emergent” DES result not implied by the equations (e.g., interaction of coordinator queue drops with AoI tail under bursty campaigns, or multi-cluster phase staggering quantified more fully).

6) **Packet-level validation in Section IV-J is parameter anchoring, not independent validation; the paper should avoid over-claiming**  
- **What:** You state this correctly in places, but the section title and some phrasing (“validated via CCSDS”) could be read as “validated against measured packets.” What you actually do is standards-based accounting.  
- **Why it matters:** Overstating validation is a common rejection trigger.  
- **Remedy:**  
  - Change wording from “validated via CCSDS” to “anchored/parameterized using CCSDS nominal framing.”  
  - Consider renaming IV-J to “Standards-anchored \(\gamma\) estimation” and add one paragraph explicitly distinguishing: *standard conformance* vs *implementation performance* vs *channel-dependent acquisition failures*.

7) **Generalized \(\gamma\) expression is useful, but practitioner utility would improve with a measurement recipe and error bars**  
- **What:** Eq. (37) is good, but practitioners need to know what to measure and how sensitive \(R_{\rm PHY,min}\) is to each term (especially \(T_{\rm acq}\) and turnaround).  
- **Why it matters:** This is one of the paper’s most transferable contributions; making it “plug-and-play” increases impact.  
- **Remedy:** Add a short “How to measure \(\gamma\) on the bench” procedure: log timestamps for burst start to first valid frame, turnaround time distribution, guard requirement from timing sync error, and then compute \(\gamma\) with confidence intervals; propagate to \(R_{\rm PHY,min}\).

---

# Minor Issues

1) **Notation table: \(\alpha_{\rm RX}\) entry appears to have a parenthesis/formatting error** (extra “)$” and ambiguous formula).  
2) **In several places “all rates are PHY unless labeled info-rate” conflicts with earlier uses of \(C_{\text{coord}}\) in kbps without always labeling**—tighten consistent labeling.  
3) **Table IV message-size justifications**: the “metadata/CRC 371 B” for a 512 B summary is plausible but reads arbitrary; consider listing actual fields and sizes summing cleanly.  
4) **AoI discussion**: clarify that the AoI P99 formula is for i.i.d. Bernoulli sampling; you mention this, but it would help to explicitly state it is not a network tail metric.  
5) **GE model**: per-cycle transition assumption is critical; consider adding a brief note on how results would change if transitions occurred per-slot (fast mixing) vs per-cycle (slow mixing).  
6) **Fleet reuse factor \(R=3\)**: the C/I back-of-envelope is helpful but optimistic; add “single interferer” assumption explicitly and note aggregate interference.  
7) **Table VII (Model S)**: add a bold reminder in the caption header row itself (“Model S only; not for design”) to prevent screenshot misuse.  
8) **Algorithm 1**: Line 4 Test A uses \(\eta_0\) but does not define it as an input/constant there; ensure Algorithm inputs/assumptions are self-contained.  
9) **Link budget table**: “Aggregate capacity >200 kbps shared among \(k_c=100\)” is asserted; show the calculation or cite the limiting factor (C/N0-limited) more explicitly.  
10) **Referencing**: consider adding a citation for demand-assigned TDMA scheduling theory or satellite DAMA systems beyond DVB-RCS2 (even if only for context).

---

## Overall Recommendation  
**Recommendation:** **Major Revision**

The manuscript has a solid core: a practical sizing framework that cleanly separates byte-budget feasibility from TDMA airtime feasibility, and a standards-anchored way to compute slot efficiency \(\gamma(R_{\rm PHY})\) that leads to a clear design recommendation (30 kbps minimum, 35 kbps recommended under conservative acquisition/guard assumptions). The improvements in this version—especially the campaign duty factor \(d\), the explicit contextualization of the \(\eta_S\approx 46\%\) case as a continuous-duty bound, and the clearer “Model C only for decisions” stance—materially strengthen the paper.

The main remaining barrier to acceptance is not the absence of external validation (you are appropriately transparent about that), but rather internal presentation/logic issues that can cause misapplication: the ambiguous role/definition of \(\alpha_{\rm RX}\), lingering “two-test vs three-layer” confusion, and the risk that Model S results are misread as decision-relevant. Addressing these with tighter definitions, a small derivation, and clearer separation of illustrative vs recommended results would substantially improve rigor and practitioner usability. Strengthening the workload realism argument for \(d\) with one or two concrete operational instantiations would further solidify the central utilization claims.

---

## Constructive Suggestions (ordered by impact)

1) **Tighten the feasibility framework narrative**: enforce “two tests” everywhere; treat \(1/\gamma\) strictly as a conversion inside Test B; audit abstract/introduction/conclusion for consistency.  
2) **Fix \(\alpha_{\rm RX}\)**: redefine cleanly, remove “canonical” implication, and add a short derivation showing how the heuristic relates to Test B and when it is exact.  
3) **Make Model C dominant**: compress/appendix Model S; replicate any key qualitative conclusions (e.g., ARQ×TDMA coupling) under Model C to avoid optimistic-table misuse.  
4) **Upgrade duty-factor realism**: include at least one fully specified mission-phase workload trace (commands/day, \(q\), correlation scope, resulting \(d,p_{\rm cmd}\)) and show resulting \(\eta\) and any Test B implications.  
5) **Increase DES unique value**: expand distributional/tail results (buffer sizing vs ON/OFF parameters and correlation scope) and reduce “DES matches mean” repetition.  
6) **Recast IV-J as anchoring, not validation**: rename section and adjust wording (“anchored/parameterized”), and add a bench-measurement recipe for \(\gamma\) with uncertainty propagation.  
7) **Add a practitioner checklist**: one-page “how to use Algorithm 1” with required measured inputs (\(T_{\rm acq}\) distribution, turnaround, guard from sync error, FEC/framing bits) and typical pitfalls (double-counting \(\gamma\), reusing \(\alpha_{\rm RX}\)).