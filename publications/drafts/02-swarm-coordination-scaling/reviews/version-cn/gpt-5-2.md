---
paper: "02-swarm-coordination-scaling"
version: "cn"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-03-03"
recommendation: "Major Revision"
---

## 1. Significance & Novelty  
**Rating: 4 (Good)**  
The manuscript targets an important and under-served problem: *preliminary sizing* of coordination/communication for very large autonomous swarms (10³–10⁵ nodes) with explicit byte accounting and a TDMA schedulability check. The “rate ladder” and the separation into message-layer utilization (η) and airtime feasibility (γ + superframe timing) are practically useful as a *design workflow* rather than yet another architecture proposal. The explicit campaign duty factor \(d\) and the recognition that stress traffic is an upper bound (not routine) are meaningful improvements for workload realism.

Novelty is strongest in (i) the three-step sizing workflow that prevents double-counting (byte budget → γ mapping → explicit superframe check), (ii) the CCSDS-grounded γ anchoring replacing an optimistic constant, and (iii) the articulation of when ARQ becomes structurally ineffective under slow-mixing GE coherence. That said, several elements are more “engineering synthesis” than new theory; the paper’s value hinges on correctness, consistency, and how convincingly it translates into guidance.

---

## 2. Methodological Soundness  
**Rating: 3 (Adequate)**  
The methodology is generally coherent for a sizing paper: closed-form equations, a cycle-aggregated DES for distributional tails, and a slot-level simulator to test TDMA timing/ARQ coupling. The explicit V&V tiering is candid and appropriate.

However, there are methodological weaknesses that limit confidence in the quantitative recommendations:
- The DES is *not* a packet/MAC simulator and cannot validate timing-layer feasibility; the paper sometimes risks implying broader validation than is warranted (even if it includes caveats).
- The GE model is used appropriately as a sensitivity tool, but the mapping between physical mechanisms and \(p_{BG}\) remains speculative, and the coherence-time modeling choices (per-cycle vs per-slot) need sharper justification and clearer boundaries of applicability.
- Some timing numbers appear internally inconsistent (see Major Issues), which is critical because the main conclusion (30 kbps min; 35 kbps recommended) depends on small margins.

---

## 3. Validity & Logic  
**Rating: 3 (Adequate)**  
The overall logic—separating offered load from airtime feasibility, and explicitly warning against double-counting \(1/\gamma\)—is a strength. The stress-case contextualization as a continuous-duty upper bound is also clearer than in many earlier swarm-comm papers.

Nonetheless, several internal consistency issues remain:
- Some equations/definitions (e.g., \(C_{\text{TDMA}}\) vs “info-rate” vs “PHY-rate”) are mixed in prose in ways that can confuse readers and may conceal unit/interpretation errors.
- The “three-layer feasibility framework” is described as two layers plus a mapping; that is fine, but the manuscript must be extremely disciplined in terminology because γ is simultaneously (a) a MAC/PHY efficiency factor and (b) embedded again in explicit slot timing. Right now it is *mostly* disciplined, but not perfectly.
- The generalized γ expression is useful, but only if practitioners can replicate the 0.761/0.745 values and understand which overheads are already included vs must be added (acq/guard/ranging/ACKs).

---

## 4. Clarity & Structure  
**Rating: 4 (Good)**  
The paper is unusually explicit about assumptions, tiers of validation, and what is and is not claimed. The “rate ladder” table and the superframe budget table are effective. The duty factor \(d\) explanation and the separation from unicast fraction \(q\) is also well done.

Clarity issues remain in a few key places:
- Some symbol naming and “rate” terminology is overloaded (information rate vs raw PHY vs “coord ingress link rate”).
- A few critical numerical statements conflict across sections/tables (Major Issues), which will undermine reader trust unless reconciled.
- The manuscript is long and occasionally repeats the same caveats; consider consolidating repeated disclaimers into one “Assumptions and applicability” box.

---

## 5. Ethical Compliance  
**Rating: 5 (Excellent)**  
Strong reproducibility posture: code + tag, parameter tables, and explicit statement of absent external validation. AI disclosure is present and appropriately scoped (ideation and prose editing only). No human/animal subjects.

One suggestion: add a short “Reproducibility checklist” (exact commit hash, how to regenerate each key figure/table, runtime/machine spec) in the Data Availability section or appendix.

---

## 6. Scope & Referencing  
**Rating: 4 (Good)**  
The references are broadly appropriate across constellation ops, distributed algorithms, AoI, DTN/space protocols, and TDMA standards. Anchoring γ to CCSDS Proximity-1 is on-scope for IEEE TAES / ASR.

Gaps:
- For TDMA efficiency and framing overheads, consider adding at least one additional space link layer reference beyond Proximity-1 (e.g., CCSDS Space Link Extension / AOS/TC framing contexts) *or* clarify why Proximity-1 is the closest analog for the assumed ISL.
- For MAC/TDMA scheduling and demand-assigned systems, DVB-RCS2 is a good touch; adding a small set of classic TDMA scheduling / real-time network references would help (even if you keep the model simple).

---

# Major Issues

1) **Numerical inconsistency in coordinator ingress requirement (20.2 kbps vs 26.7 kbps vs “27 kbps info-rate”)**  
- **Issue:** The manuscript states:  
  - Eq. (coord info) gives ~20.2 kbps info-rate for \(k_c=100, S=256\) B, \(T_c=10\) s (correct: \(99\times256\times8/10 \approx 20.3\) kbps).  
  - Eq. (tdma capacity) reports \(C_{\text{TDMA}}\approx 26.7\) kbps *at* \(\gamma=0.761\), which is a **PHY/raw rate** requirement, not an info-rate.  
  - Abstract/Conclusion also say “requires ≈27 kbps (info-rate) at γ≈0.76” which appears wrong by definition (should be ≈20.3 kbps info-rate; ≈26.7 kbps PHY-rate before half-duplex partitioning; ≈29.9 kbps after \(\alpha_{RX}\)).  
- **Why it matters:** This is central to the paper’s headline conclusion (30 kbps minimum; 35 kbps recommended). If the rate ladder’s semantics are inconsistent, practitioners cannot safely apply the method.  
- **Remedy:** Audit and standardize terminology everywhere:  
  - Use **\(C_{\text{coord,info}}\)** strictly for info-rate (≈20.3 kbps).  
  - Use **\(R_{\text{PHY,raw}}\)** or similar for \(C_{\text{coord,info}}/\gamma\) (≈27.1 kbps at 30 kbps γ).  
  - Use **\(R_{\text{PHY,min}}\)** for \(C_{\text{coord,info}}/(\gamma\alpha_{RX})\) (≈29.9 kbps).  
  - Fix Abstract/Conclusion wording and any “27 kbps info-rate” statements. Consider a single boxed “Units and rate definitions” section.

2) **γ unification (0.76 from CCSDS) is improved, but not consistently propagated and cross-checked against all tables/claims**  
- **Issue:** You clearly state Model C is used for feasibility claims, and you provide \(\gamma_{24}=0.761\), \(\gamma_{30}=0.745\). However, some derived quantities appear to mix models or assumptions (e.g., “ingress 99×91.7 ms at 30 kbps” is Model C; elsewhere 24 kbps feasibility statements sometimes implicitly rely on Model S-like timing unless carefully read).  
- **Why it matters:** The paper’s credibility depends on “single source of truth” for γ and slot timing. Small differences shift the feasibility boundary by several kbps.  
- **Remedy:**  
  - Create a single table listing **all timing components** (payload, framing, FEC, guard, acquisition, ACK minislot if any) for 24/30/35 kbps under Model C, and derive slot time and γ from that table only.  
  - Add a short automated consistency check in the repo (unit test) that recomputes γ and slot times and reproduces Tables 6/7/Rate Ladder.

3) **Stress-case \(\eta_S\approx 46\%\) is better contextualized, but still risks being interpreted as “typical” without a clearer operational envelope**  
- **Issue:** You now label stress as a continuous-duty bound and provide duty-factor mapping. Still, the manuscript frequently uses the stress utilization in feasibility heuristics and in narrative emphasis (“safety-criticality: undersizing causes 100% deadline misses”), which could be misread as routine. Also, stress-case η is an *egress/byte-budget* phenomenon, while the 24 kbps infeasibility is *ingress timing*—the paper states this, but the rhetoric occasionally blends them.  
- **Why it matters:** Reviewers/readers will challenge realism if they think 46% is normal. Practitioners might also incorrectly tie the 24 kbps infeasibility to stress traffic rather than coordinator ingress.  
- **Remedy:**  
  - Add a prominent figure/table showing **routine vs peak**: e.g., \(d\in[10^{-3},10^{-1}]\) typical, and what η_total looks like across that range, with stress shown as a dashed ceiling.  
  - In the Introduction/Contributions, separate “ingress-driven min PHY rate” from “workload-driven utilization” in two bullet points with no cross-references.

4) **Three-layer feasibility framing: conceptually sound, but the mapping \(\eta_{\text{total}}/\gamma\) risks misuse and may be mathematically misleading**  
- **Issue:** You call it a “screening heuristic” and warn it’s not a criterion, which is good. But \(\eta_{\text{total}}/\gamma\) conflates message-layer utilization with airtime under assumptions that may not hold (half-duplex partitioning, asymmetric ingress/egress, fixed control overheads, and the fact that baseline telemetry is uplink-only). A single scalar can be wrong even when the full superframe passes/fails.  
- **Why it matters:** This heuristic is likely to be copied into quick sizing spreadsheets and misapplied, undermining the paper’s goal of preventing double-counting and confusion.  
- **Remedy:** Either (a) remove the heuristic entirely, or (b) redefine it as two separate approximate airtime utilizations: **uplink airtime fraction** and **downlink airtime fraction**, each derived from slot timing and message counts, explicitly including \(\alpha_{RX}\). Provide conditions under which the heuristic is valid.

5) **DES “verification value” remains limited; distributional tails are useful, but the paper should sharpen what decisions DES changes**  
- **Issue:** You appropriately admit DES reproduces its own equations. The incremental value claimed is distributional tail/buffer sizing under correlated campaigns. However, the buffer results are presented as multipliers (e.g., 1.15× mean) without tying them to a concrete engineering decision (buffer size in messages/bytes, overflow probability targets, effect on AoI or drop rate).  
- **Why it matters:** TAES readers will ask: what does DES enable that a simpler analytic bound could not? If it’s just “P99 is 15% higher,” that may not justify the simulation section length.  
- **Remedy:** Add one explicit design example: choose a target overflow probability (e.g., 10⁻³ per cycle), compute required buffer in messages/bytes for Bernoulli vs ON/OFF vs cluster-correlated, and show resulting drop probability difference. If possible, compare to a simple analytic bound (Chernoff/Kingman approximation) to contextualize DES.

6) **Packet-level validation (Section IV-J) anchors γ but is not fully “independent”; also some overhead components are treated inconsistently (ACK minislot, ranging, acquisition amortization)**  
- **Issue:** You correctly state it anchors γ, not the whole framework. But the packet-level simulator appears to be a deterministic accounting tool rather than an independent implementation with potential to catch modeling errors. Additionally:  
  - ACK minislot (0.5 ms) is said to be “absorbed within guard” (Table superframe footnote), which is a strong assumption that should be explicitly justified (guard is usually for timing uncertainty/turnaround, not protocol signaling).  
  - Ranging is listed as “unmodeled overhead” (50 ms) but it is unclear whether it occurs per node per cycle, per superframe, or intermittently; that changes feasibility materially.  
- **Why it matters:** The main conclusion is margin-based. If ACK/ranging/acquisition are handled optimistically, 30 kbps may not be viable even without ARQ.  
- **Remedy:**  
  - Make ACK/ranging explicit in the superframe definition and recompute margin with/without them.  
  - Provide two superframe budgets: “minimal” and “conservative,” and show how the recommended PHY rate shifts.  
  - Describe the packet-level simulator as a separate codepath and include a cross-check that reproduces γ from raw bit counts and from time-domain equation to avoid hidden unit errors.

7) **Generalized γ expression is useful, but practitioners need clearer guidance on parameter selection and applicability to non-Proximity-1 ISLs**  
- **Issue:** Eq. (gamma_time) and (gamma_general) are good, but the paper mixes Proximity-1 framing (ASM+addr+ctrl+FCS) and LDPC assumptions in a way that may not match common ISL modems. Also, guard/acquisition are highly implementation-dependent.  
- **Why it matters:** If the paper’s main output is a sizing method, it must be robust to alternative PHY/MAC designs; otherwise it reads as a Proximity-1-specific case study.  
- **Remedy:** Add a short “How to instantiate γ for your modem” subsection with 2–3 worked examples: (i) Proximity-1 baseline (already there), (ii) a more continuous-tracking TDMA case (acq amortized), (iii) a non-CCSDS proprietary frame with different overhead. Include a template table for users to fill.

---

# Minor Issues

1) **Abstract/Conclusion wording:** Replace “requires ≈27 kbps (info-rate) at γ≈0.76” with consistent rate terminology (see Major Issue 1).  
2) **Notation table:** \(C_{\text{coord}}\) described as “Coordinator ingress link rate (kbps)” but later you distinguish info-rate vs PHY-rate; reflect that in notation (e.g., \(C_{\text{coord,info}}\), \(R_{\text{PHY}}\)).  
3) **Equation labeling:** Eq. (mac_efficiency) uses \(C_{\text{raw}} = C_{\text{coord,info}}/\gamma\). Consider renaming \(C_{\text{raw}}\) to \(R_{\text{PHY,eff}}\) or similar to avoid confusion with capacity.  
4) **Guard time derivation:** You compute differential propagation ~1.7 ms at 500 km, turnaround 2 ms, jitter 1 ms → 4.7 ms. Clarify whether 2 ms turnaround is one-way or includes both TX→RX and RX→TX, since you also add separate “turnaround ×2 = 4 ms” in the superframe table. Potential double counting unless carefully defined.  
5) **“Ingress 11,435 ms at 24 kbps Model C” vs Table rate_feasibility “ingress 11,108 ms”:** reconcile these numbers (likely rounding or different slot time assumptions). Since feasibility hinges on margins, explain any discrepancy.  
6) **AoI section:** You state “mean AoI ≈ Tc/2” under periodic reporting; that’s true under instantaneous service, but with losses/queueing it shifts. You partly address this; consider one sentence clarifying service-time assumptions.  
7) **Fleet reuse equation:** \(T_c^{fleet}=\max(T_c, G\cdot T_c)\) is tautological; likely you mean cycle period increases by factor \(G\) when time-sharing. Consider writing \(T_c^{fleet}=G\,T_c\) when \(G>1\).  
8) **Thundering herd analysis:** The BEB/ALOHA election timing is interesting but feels disconnected from the main sizing framework; consider moving to an appendix unless you later use it to size margins or buffers.  
9) **Reference quality:** Some “non-archival” web references are acceptable but should be minimized in TAES; where possible, replace with filings/technical papers or add archival alternatives.  
10) **Typographic/consistency:** Ensure all figures have file extensions or consistent naming (e.g., `fig-unicast-stagger` missing `.pdf` in includegraphics).

---

# Overall Recommendation  
**Recommendation:** **Major Revision**

The manuscript has a strong premise and is close to being a valuable “engineering sizing” reference, but it currently contains central numerical/terminology inconsistencies and a few timing-accounting ambiguities that directly affect the main conclusion (30 kbps minimum; 35 kbps recommended). These must be corrected and the framework must be made more foolproof for practitioner use.

Strengths include: clear decomposition of workload realism via duty factor \(d\); improved γ anchoring to CCSDS with explicit Model C vs Model S separation; and a genuinely useful insight that intra-cycle ARQ can be structurally ineffective under slow-mixing blockage coherence, motivating inter-cycle recovery. The explicit acknowledgment of validation limits and the open-source release are also commendable.

The most critical improvements are (i) reconcile and standardize all rate definitions and numeric values in the rate ladder and abstract/conclusion, (ii) tighten the superframe timing inventory so there is no hidden double counting (guard vs ACK vs turnaround vs ranging), and (iii) clarify what the DES adds in terms of actionable design decisions (buffer sizing with explicit targets), rather than primarily confirming mean equations.

---

# Constructive Suggestions (ordered by impact)

1) **Do a full “rate semantics + unit audit” and propagate fixes everywhere**  
   - Add a boxed glossary: info-rate vs PHY-rate vs “required raw” vs “min viable PHY.”  
   - Fix the “27 kbps info-rate” misstatement and any similar slips.

2) **Make the superframe timing budget internally watertight**  
   - One authoritative table that derives slot time at 24/30/35 kbps under Model C, including *all* assumed components.  
   - Explicitly state whether ACK minislot is extra airtime or truly inside guard (and why).  
   - Clarify turnaround accounting so it is not counted both in guard and as separate 4 ms.

3) **Strengthen Section IV-J into a more convincing parameter anchoring**  
   - Emphasize it as an *independent codepath* and show a “recompute γ two ways” consistency check.  
   - Provide a short sensitivity showing how γ changes with (a) different framing overhead, (b) different FEC rate, (c) acquisition amortization.

4) **Elevate the duty factor \(d\) result into a clearer operational envelope**  
   - One figure: η (and η_total) vs \(d\) with annotated mission phases; stress shown as a ceiling.  
   - Keep stress-case prominently labeled “continuous-duty upper bound.”

5) **Make DES tail results decision-relevant**  
   - Choose a buffer overflow target and compute required buffer sizes for the different burst models; show impact on drop probability and/or AoI.  
   - If possible, add a simple analytic approximation baseline to show DES necessity.

6) **Either remove or refine the \(\eta_{\text{total}}/\gamma\) screening heuristic**  
   - If retained, split into uplink and downlink approximate airtime fractions and state validity conditions.

7) **Add one practitioner-facing “how to use Algorithm 1” worked example**  
   - Provide a step-by-step sizing for a non-default \(k_c\), \(T_c\), and \(S\), showing how the recommended PHY shifts.

If these issues are addressed, the manuscript would be well-positioned for TAES/ASR as a practical sizing and early-phase architecture trade study reference.