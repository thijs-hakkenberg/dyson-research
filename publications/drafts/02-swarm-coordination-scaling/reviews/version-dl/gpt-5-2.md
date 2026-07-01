---
paper: "02-swarm-coordination-scaling"
version: "dl"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-03-06"
recommendation: "Major Revision"
---

## 1. Significance & Novelty  
**Rating: 4 (Good)**  
The manuscript targets an important and under-served problem: *parametric sizing* of coordination communications for very large space swarms/mega-constellations, with explicit byte accounting and a schedulability check. The two-test framework (Test A byte budget; Test B TDMA airtime) plus a “rate ladder” is a practically useful structure for early-phase design trades. The explicit separation between logical per-node allocation (1 kbps) and instantaneous coordinator burst rate is a valuable clarification that many papers gloss over.

Novelty is strongest in: (i) the closed-form sizing workflow tied to a standards-based slot-efficiency parameterization, and (ii) the explicit coupling of half-duplex partitioning + TDMA overhead + ARQ margin to derive a *minimum viable PHY rate* for coordinator ingress. However, several elements are “engineering synthesis” rather than fundamentally new theory (e.g., GE model usage, AoI geometric tail, TDMA slot efficiency definition). That is acceptable for T-AES/ASR if claims are positioned as design equations/heuristics and the validation gap is handled rigorously.

---

## 2. Methodological Soundness  
**Rating: 3 (Adequate)**  
The analytical structure is mostly sound: deterministic TDMA timing, explicit overhead ledger (in-γ vs outside-γ), and a clear mapping from message model to utilization. The Monte Carlo DES is correctly framed as Tier-1 implementation verification plus tail exploration.

Main methodological weaknesses: (i) the “three-layer feasibility framework” is described as two tests plus γ as a conversion, but the manuscript sometimes slides between “two tests” and “three layers” without a fully formal, non-overlapping definition; (ii) the slot-level simulator is used to assert feasibility thresholds (deadline misses) but the scheduler, ACK policy, and ARQ slot allocation appear somewhat bespoke and not compared against alternative TDMA/return-link designs (e.g., aggregated slots, piggyback ACK, selective repeat, multi-packet bursts); (iii) GE parameterization is explicitly a what-if tool, but then used to motivate a hard recommendation (35 kbps) without bounding how sensitive that recommendation is to plausible *measured* coherence times and loss statistics.

---

## 3. Validity & Logic  
**Rating: 3 (Adequate)**  
Internal consistency is improved relative to what I infer was an earlier version: the paper now explicitly states “no external validation,” contextualizes the 46% stress case as a continuous-duty upper bound, and provides a timing ledger to prevent double counting. The duty factor \(d\) is a legitimate mechanism to address workload realism, and the mapping examples (station-keeping, CA, software update) help.

Remaining validity concerns are concentrated in:  
- the interpretation of “feasible” (deadline miss ≤1%) and how that maps to real control/coordination requirements;  
- the coordinator ingress model being treated as strictly sequential one-slot-per-node-per-cycle (which drives the 30–35 kbps conclusion);  
- the independence assumptions (per-node independent GE, static cluster membership, no inter-cluster contention) that collectively make the feasibility region optimistic even if each assumption is individually defensible.

---

## 4. Clarity & Structure  
**Rating: 4 (Good)**  
The paper is unusually explicit about definitions (baseline vs overhead, what γ includes, what is excluded). The “rate ladder,” timing ledger, and Algorithm 1 are strong for practitioners. The manuscript also does a good job flagging what is a bound vs a recommendation, and where results are conditional.

Clarity issues remain: the manuscript is long and sometimes repetitive (γ and “not a third test” is reiterated many times), while some critical modeling choices (e.g., why ACK is 0.5 ms/node; why one packet per slot; why no slot aggregation) are not justified to the same degree. Several claims are stated as “confirmed” by internal simulators when they are essentially restatements of the same timing equations.

---

## 5. Ethical Compliance  
**Rating: 4 (Good)**  
Data/code availability is strong (GitHub tag, environment). AI disclosure is explicit and appropriate. No human/animal subjects. Reproducibility is plausible given the repository and parameter tables.

One missing piece: for a top-tier journal, consider providing a minimal “reproduction recipe” (exact commit hash, run scripts, expected key outputs) and archiving to a DOI-backed repository (Zenodo) to ensure persistence beyond GitHub.

---

## 6. Scope & Referencing  
**Rating: 3 (Adequate)**  
Citations cover distributed algorithms, AoI, CCSDS, DTN, and some constellation/networking work. However, for a MAC/TDMA-centric sizing paper aimed at T-AES, the related work on satellite return-link TDMA/DAMA scheduling, burst-mode acquisition, and standards/practice beyond DVB-RCS2 is thin. Also missing are several relevant strands:  
- satellite TDMA burst-mode synchronization/acquisition literature (especially for low-rate burst links),  
- LEO ISL MAC papers (even if optical dominates, RF backup/coordination is central here),  
- more explicit comparisons to CCSDS Proximity-1 operational implementations and measured burst acquisition times (even if only from analogous missions).

---

# Major Issues

1. **Core feasibility conclusion (30 kbps min, 35 kbps recommended) is overly driven by a *single* slot structure (one packet/slot, cold-start acquisition per slot) without exploring standard alternatives.**  
   - **Why it matters:** The main design recommendation hinges on γ and per-slot overhead. If slot aggregation (multiple packets per burst), piggybacking, or coordinator-driven continuous tracking is feasible, the “minimum viable PHY rate” could shift materially. A practitioner may incorrectly conclude 35 kbps is fundamental rather than an artifact of a particular framing/scheduling choice.  
   - **Remedy:** Add a short but quantitative alternative design exploration:  
     - (a) *Multi-packet burst per node per cycle* (aggregate status + optional extras) and its effect on \(T_{\text{acq}}\) amortization and γ.  
     - (b) *Tracking-mode across consecutive member slots* (coordinator keeps lock while different nodes transmit—if not feasible, explain why).  
     - (c) ACK compression (bitmap ACK, group ACK, or ACK-in-guard as default if GNSS sync is assumed).  
     Provide a table: “baseline design vs 2–3 plausible alternatives” showing resulting γ and \(R_{\text{PHY,min}}\). This can be analytic; no need for full new simulation.

2. **Campaign duty factor \(d\) helps realism, but the workload model remains under-anchored and can still be interpreted as arbitrary.**  
   - **Why it matters:** The paper’s headline “routine 5–10%” and “46% <1% of time” depends on the mapping in Table \(duty\_mapping\) and the mixture calculation. Without stronger grounding, reviewers/readers may view \(d\) as a tunable knob used to make results look acceptable.  
   - **Remedy:** Strengthen workload realism by:  
     - explicitly separating *command generation rate* \(p_{\text{cmd}}\) from *campaign ON fraction* \(d\) in all key plots/tables (some places still implicitly assume \(p_{\text{cmd}}=1\) in ON).  
     - adding a sensitivity plot of \(\eta\) vs \(p_{\text{eff}}=d\,p_{\text{cmd}}\) and showing what ranges correspond to plausible ops (station-keeping, CA, rephasing, software update).  
     - if possible, cite at least one public constellation ops source for typical maneuver/command frequencies (even coarse) to bound \(p_{\text{eff}}\).

3. **γ “unification” to ~0.73–0.76 is mostly consistent, but the manuscript still mixes rates/γ subscripts in ways that risk misapplication by practitioners.**  
   - **Why it matters:** The paper’s central contribution is the sizing workflow; any ambiguity in which γ applies (24 vs 30 vs 35 kbps; in-γ vs outside-γ) undermines trust and reproducibility.  
   - **Remedy:**  
     - Create one “authoritative constants” table early (perhaps after Notation) listing \(T_{\text{acq}},T_{\text{guard}},R_{\text{FEC}},O_{\text{frame}}\) and the resulting \(\gamma_{24},\gamma_{30},\gamma_{35}\).  
     - Ensure every time a numeric γ is used, it is explicitly tied to a PHY rate (e.g., always write \(\gamma_{30}\) not γ).  
     - Audit for any remaining instances where older γ≈0.85 logic might persist (e.g., in narrative claims like “CCSDS yields γ≈0.73–0.76 across 24–35 kbps”; verify all downstream computations use those exact values).

4. **The “three-layer feasibility framework” (byte budget, MAC efficiency, TDMA airtime) is not fully formalized and risks double counting or conceptual overlap.**  
   - **Why it matters:** You correctly warn “γ is not a third test,” yet elsewhere you suggest extension under contention by multiplying γ by \(\rho_{\text{MAC}}\). That implicitly *does* introduce a MAC-efficiency layer. Without a clean separation, practitioners may apply both a MAC factor and explicit TDMA slotting incorrectly.  
   - **Remedy:** Provide a formal decomposition:  
     - Layer 1: information bytes generated (Test A).  
     - Layer 2: scheduled airtime mapping from bytes → time under a specific PHY/framing (γ and explicit outside-γ terms) (Test B).  
     - Layer 3 (optional extension): medium access losses/inefficiency under contention/interference (a multiplicative utilization factor \(\rho_{\text{MAC}}\) OR an explicit contention model, but not both).  
     Include a short “how not to double count” boxed guidance with one worked example.

5. **DES verification provides limited incremental value and should be repositioned or strengthened.**  
   - **Why it matters:** The manuscript is commendably honest that Tier-1 agreement is tautological, but then still spends significant space on DES results that are essentially restating analytic means. For a top-tier journal, the simulation should either (i) test regimes where the equations are not exact, or (ii) be reduced to a reproducibility appendix.  
   - **Remedy (choose one):**  
     - **Option A (strengthen):** Use DES to explore a regime that breaks analytic assumptions: heterogeneous \(k_c\), variable packet sizes, correlated ON/OFF across nodes, or coordinator processing variability; quantify impact on tail drops/deadlines.  
     - **Option B (trim):** Condense DES sections, keep only the tail/buffer CDF contribution, and move mean-verification to an appendix.

6. **Packet-level validation in Section IV-J is not independent validation; it is standards-based parameter anchoring. This is acknowledged, but the paper still leans on it to justify strong design recommendations.**  
   - **Why it matters:** A standards-based timing estimate is useful, but not equivalent to measured burst acquisition/turnaround distributions. The key risk is \(T_{\text{acq}}\) variability and implementation-specific overhead.  
   - **Remedy:**  
     - Add an explicit uncertainty treatment: treat \(T_{\text{acq}}\) and \(T_{\text{guard}}\) as random variables (e.g., P95) and propagate to a P95 required PHY rate.  
     - Provide a “design for P95 acquisition time” formula and show the 35 kbps recommendation under that criterion. You already have “breaking point” numbers; elevate them into a clear robustness argument.

7. **Feasibility threshold (≤1% deadline misses) is arbitrary without mapping to control/coordination requirements and consequences.**  
   - **Why it matters:** Whether 1% misses is acceptable depends on what is missed (status vs command), whether misses are correlated, and whether inter-cycle recovery is acceptable for the mission class.  
   - **Remedy:** Define requirement-driven thresholds: e.g., “status AoI P99 must be <X,” “command broadcast must deliver within 1 cycle with probability ≥Y,” etc. Then show how the 1% miss proxy relates to those. At minimum, justify 1% with a sensitivity statement (e.g., how PHY recommendation changes if threshold is 0.1% vs 5%).

---

# Minor Issues

1. **Terminology drift:** sometimes “stress-case \(\eta_S\)” refers to 46% (overhead beyond baseline), while elsewhere stress-case total is 67%. Consider consistently labeling \(\eta\) vs \(\eta_{\text{total}}\) in prose.  
2. **ACK accounting:** ACK is “outside γ” and 0.5 ms/node. Provide a short derivation (bits, modulation assumptions) or cite a standard. Otherwise it reads arbitrary.  
3. **Equation/variable clarity:** \(\alpha_{\text{RX}}\) is said to be computed output, but it is also used in heuristic Eq. (coord_phy). Add a one-line explicit expression for \(\alpha_{\text{RX}}\) under the baseline schedule (e.g., \(\alpha_{\text{RX}}=(k_c-1)T_{\text{slot}}/T_c\) when \(M_r=0\)).  
4. **GE model coherence:** You assume state transitions once per cycle and “intra-cycle retransmissions face same state.” That is a strong assumption; add a short note on how results change if transitions occur per slot instead of per cycle (even qualitatively).  
5. **Fleet reuse factor \(R=7\):** clearly marked as placeholder, but it still supports downstream “non-binding” conclusions. Consider moving fleet reuse to “illustrative” and avoid strong claims until RF sim is done.  
6. **Related work:** add at least a few more citations on burst-mode TDMA acquisition/guard design and satellite DAMA/TDMA return links beyond DVB-RCS2.  
7. **Formatting/organization:** repeated admonitions (“γ is not a third test”) could be consolidated into a single prominent box and removed elsewhere.

---

## Overall Recommendation  
**Recommendation:** **Major Revision**

The manuscript is promising and closer to publishable than many early-phase “design equation” papers because it is explicit about assumptions, provides code, and acknowledges the validation gap. The central contribution—a structured sizing workflow that turns a per-node byte budget into coordinator PHY rate and TDMA schedulability constraints—is valuable for practitioners and appropriate for a top-tier aerospace systems journal.

However, the strongest quantitative conclusion (30 kbps minimum, 35 kbps recommended) is currently too dependent on a particular TDMA slot/framing/ACK design choice and on unmeasured acquisition/turnaround statistics. The paper needs a more robust exploration of alternative, still-standards-consistent scheduling/framing options, and a clearer requirement-based justification of the feasibility threshold. Strengthening (or trimming) the DES component to add non-tautological insight would also improve the paper’s scientific contribution.

---

## Constructive Suggestions (ordered by impact)

1. **Add an “Alternative TDMA design variants” subsection** quantifying how \(R_{\text{PHY,min}}\) changes under 2–3 plausible slot/ACK/acquisition variants (aggregation, ACK bitmap, tracking/reacquire).  
2. **Formalize the feasibility-layer decomposition** to eliminate ambiguity between “two tests” and “three layers,” including a strict anti-double-counting rule when introducing \(\rho_{\text{MAC}}\).  
3. **Strengthen workload realism around \(d\) and \(p_{\text{cmd}}\):** present results versus \(p_{\text{eff}}=d p_{\text{cmd}}\), add citations/anchoring for plausible command rates, and ensure the “<1% of time” statement is clearly tied to an operational scenario.  
4. **Introduce an uncertainty-based robustness argument** for \(T_{\text{acq}}\), \(T_{\text{guard}}\), and γ (P95 design), and restate the 35 kbps recommendation as “robust to P95 acquisition up to X ms” prominently in the abstract/conclusion.  
5. **Rework DES section:** either (A) use it to explore heterogeneity/correlation regimes that the equations do not capture, or (B) compress it and keep only the tail/buffer sizing results.  
6. **Justify or parameterize the 1% deadline-miss feasibility threshold** in terms of AoI/command delivery requirements; provide a sensitivity statement.  
7. **Audit γ usage for consistency** and enforce subscripted γ everywhere numerical values appear; add a single authoritative parameter table early.

If these revisions are made, the paper could become a strong “design equations + sizing workflow” contribution with clear practitioner value and appropriately bounded claims.