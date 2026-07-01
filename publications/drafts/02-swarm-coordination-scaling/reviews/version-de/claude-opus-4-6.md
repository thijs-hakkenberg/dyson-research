---
paper: "02-swarm-coordination-scaling"
version: "de"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-03-05"
recommendation: "Unknown"
---



# Peer Review: "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version DE)

---

## 1. Significance & Novelty
**Rating: 3 (Adequate)**

The paper addresses a genuine gap: no prior work provides closed-form parametric sizing relationships for hierarchical coordination architectures at the $10^3$–$10^5$ node scale with byte-level traffic accounting. The two-test feasibility framework (byte budget + TDMA airtime) is a useful conceptual contribution, and the campaign duty factor $d$ is a practical parameterization. However, the novelty is tempered by the fact that the individual analytical components (TDMA slot budgets, GE channel models, M/D/1 queueing, AoI under geometric sampling) are all well-established. The contribution is primarily one of *integration and systematization* rather than methodological advance. The paper is honest about this, which is appreciated, but the significance is limited by the absence of any external validation—the framework remains entirely self-referential.

## 2. Methodological Soundness
**Rating: 3 (Adequate)**

The three-layer feasibility framework (byte budget, MAC efficiency via $\gamma$, TDMA airtime) is logically structured and internally consistent. The campaign duty factor $d$ adequately addresses workload realism: the mapping from mission phases to $(d, q)$ pairs (Table VII) is well-motivated, and the empirical anchoring to ESA CA rates is appropriate. The gamma unification around 0.70–0.76 (CCSDS-grounded, replacing the earlier 0.85) appears consistently applied throughout—all feasibility claims, recommendations, and decision-relevant tables use Model C values, with Model S clearly labeled as a comparison bound only.

However, several methodological concerns remain:

- The DES verification (Tier 1) confirms analytical means to <0.1%, which is by construction since both share the same equations. The paper acknowledges this explicitly, but the DES then contributes only distributional tails under specific campaign models—a narrow incremental value.
- The GE channel model parameters ($p_{BG} = 0.50$, $p_B = 0.90$) are acknowledged as illustrative with no ISL measurements for calibration. While the sensitivity curves (Fig. 4b) partially mitigate this, the default parameterization drives several key results (27% intra-cycle recovery, P95 = 4 cycles) that are presented with more specificity than the evidence warrants.
- The slot-level simulator and the packet-level $\gamma$ derivation share the same timing model; calling this "Tier 2" validation overstates the independence.

## 3. Validity & Logic
**Rating: 4 (Good)**

The internal logic is generally sound and well-documented. Specific strengths:

- The stress-case $\eta_S \approx 46\%$ is now properly contextualized as a continuous-duty upper bound occurring <1% of operational time (yearly mixture: $\bar{\eta} = 5.6\%$). This is a significant improvement.
- The rate ladder (Table IV) provides a clear, traceable chain from information-rate through PHY-rate to design recommendation.
- The distinction between $\alpha_{\text{RX}}$ as a computed output (not a free parameter) is clearly stated and consistently maintained.
- The paper correctly identifies that Test A and Test B decouple for $d \leq 0.10$ and that joint analysis is needed only at high duty factors.

One logical concern: the paper claims the ARQ×TDMA coupling (52.7% deadline misses at 24 kbps Model S with $M_r = 1$) is the "sole emergent finding" from the slot simulator. But this result is predictable from the timing budget: adding retransmission slots to an already-tight schedule will cause deadline misses. The 52.7% figure is specific and useful, but calling it "emergent" may overstate its surprise value.

## 4. Clarity & Structure
**Rating: 3 (Adequate)**

The paper is extraordinarily detailed—perhaps excessively so for a journal article. At its current length, it reads more like a technical report than a focused journal paper. Specific concerns:

- The notation table (Table I) is comprehensive but the paper introduces additional notation throughout that requires constant cross-referencing.
- The two-paragraph slot-timing model preamble in Section I is unusual and suggests the authors are preemptively defending against confusion from prior versions—this should be integrated more naturally.
- The boxed feasibility framework definition (Section IV) is helpful but verbose; the warning "Do not apply the heuristic AND separately compute slot-level ingress" reads like a response to reviewer confusion rather than exposition.
- Table footnotes are extremely dense (e.g., Table III has footnotes a–d totaling ~150 words). Some of this material belongs in the main text.
- The coordinator failure transient discussion (Section III-B-2) includes a detailed thundering-herd analysis in a footnote that is longer than many main-text paragraphs.

The paper would benefit substantially from moving detailed derivations and edge-case analyses to appendices.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**

Exemplary transparency: code/data availability with tagged repository, explicit AI disclosure with specific tool versions, clear acknowledgment that all results lack external validation, and honest V&V tier classification. The claim map (Table X) is a model of scientific transparency.

## 6. Scope & Referencing
**Rating: 3 (Adequate)**

The reference list (56 items) covers the relevant domains adequately: CCSDS standards, swarm robotics, distributed systems, AoI theory, queueing theory, and constellation operations. However:

- The paper cites no work on actual ISL channel characterization or measurement campaigns, which is the critical missing validation domain.
- Network calculus [Le Boudec] is mentioned but not used; the paper could benefit from comparing its mean-value approach against deterministic worst-case bounds.
- The DVB-RCS2 comparison ($\gamma = 0.70$–$0.85$) is the closest external anchor but is acknowledged as a different domain (user terminals vs. ISL).
- Some references are non-archival (Amazon Kuiper overview, DARPA program pages) and may not persist.

---

## Major Issues

**1. Circular validation architecture undermines confidence in quantitative claims.**
- *Issue:* The analytical equations, DES, slot simulator, and packet-level $\gamma$ derivation all share the same underlying timing and traffic models. The paper acknowledges this (Table X, Section V-A) but still presents specific quantitative results (e.g., "margin = 730 ms," "35 kbps recommended") with a precision that implies higher confidence than the evidence supports.
- *Why it matters:* Without any external validation point, the entire quantitative framework rests on assumed parameters ($T_{\text{acq}}$, $T_{\text{guard}}$, GE parameters, message sizes). A single incorrect assumption propagates through all "verification" layers undetected.
- *Remedy:* (a) Explicitly quantify the sensitivity of the 35 kbps recommendation to the two most uncertain parameters ($T_{\text{acq}}$ and $p_{BG}$) in a single consolidated sensitivity table. The paper does this partially (Fig. 3, Table XII) but scattered across sections. (b) Consider adding a comparison against NS-3 or a published TDMA scheduling benchmark, even for a simplified scenario, to provide at least one external anchor point.

**2. The DES provides limited incremental value beyond confirming its own equations.**
- *Issue:* The DES matches analytical means to <0.1% (by construction). Its sole non-tautological contribution is the distributional tail under campaign burstiness (Fig. 5). But the campaign model itself (ON/OFF Markov) is assumed, not validated, so the tail distribution is conditional on an unvalidated input.
- *Why it matters:* The DES consumes significant paper real estate (Sections III-A, IV-F) for what amounts to a code-correctness check plus one conditional distributional result.
- *Remedy:* Either (a) reduce the DES discussion to a brief verification statement and move details to supplementary material, or (b) use the DES to explore scenarios that the analytical model *cannot* handle (e.g., correlated node failures, dynamic cluster reassignment, priority queueing under mixed traffic) to provide genuine incremental insight.

**3. The packet-level validation (Section IV-J) does not provide independent validation.**
- *Issue:* Section IV-J derives $\gamma$ from CCSDS Proximity-1 framing parameters. This is a *parameter estimation* exercise, not validation. The paper correctly labels it as a "standards-based parameter estimate" but still lists it as "Tier 2" in the claim map, implying a higher level of independence than exists.
- *Why it matters:* Readers may interpret "Tier 2: Slot-sim" and "Std.-based est.: CCSDS $\gamma$" as providing independent corroboration when they are actually different computations using the same timing assumptions.
- *Remedy:* Relabel the evidence tiers more conservatively. "Tier 2" should require at least a different modeling tool or independently measured parameters. The CCSDS $\gamma$ derivation is better described as "parameter anchoring" (which the paper already uses in one place but not consistently).

**4. The generalized $\gamma$ expression (Eq. 14) is standard TDMA engineering, not a novel contribution.**
- *Issue:* Eq. 14 decomposes slot time into payload + FEC + framing + guard + acquisition. This is textbook TDMA slot budgeting. The paper claims the "specific contribution is the rate-dependent parameterization under CCSDS framing with explicit sensitivity to acquisition and guard assumptions."
- *Why it matters:* Presenting standard engineering as a contribution risks undermining the paper's credibility with practitioners who routinely perform such calculations.
- *Remedy:* Frame Eq. 14 as a *systematization for the specific application context* rather than a novel equation. The value is in the specific CCSDS instantiation and the sensitivity analysis (Fig. 3, Table XII), not in the general form.

**5. Static cluster membership assumption limits applicability.**
- *Issue:* The DES assumes static cluster membership for 1 year. The J2 analysis (Section V-C) estimates <0.3% overhead for cross-plane reassociation, but this is an analytical estimate for a Walker constellation, not a simulation result. Heterogeneous orbits are acknowledged but not analyzed.
- *Why it matters:* For the target scale ($10^4$–$10^5$ nodes), many practical architectures involve heterogeneous orbits where cluster membership changes frequently. The static assumption may be the binding limitation on applicability.
- *Remedy:* Either (a) simulate dynamic reassociation in the DES for at least one heterogeneous orbit scenario, or (b) more prominently bound the applicability to co-planar or near-co-planar formations and state this as a scope limitation in the abstract.

---

## Minor Issues

1. **Abstract length:** At ~200 words, the abstract is dense but within IEEE limits. However, the phrase "All results are per-cluster ($k_c = 50$–$500$) preliminary design estimates lacking external validation" is important but buried at the end; consider moving it earlier.

2. **Table I notation:** $\alpha_{\text{RX}}$ is listed as a "computed output" with an example value (0.908). Providing a specific number in the notation table for a derived quantity may confuse readers who expect it to be a parameter.

3. **Section III-B-2 footnote:** The thundering-herd analysis (Slotted ALOHA with BEB) is interesting but the level of detail is inappropriate for a footnote. Either promote to main text or remove.

4. **Eq. 5 ($\eta_{\text{consensus}}$):** The variable $f_{\text{decision}}$ appears without prior definition in the equation context (it is in Table I but not introduced in the surrounding text).

5. **Table VI (TDMA Joint Interaction):** The table header says "Model S Only" but this is easy to miss. Consider adding a prominent warning or shading.

6. **Fig. 4 description:** "DES verification at three $p_{BG}$ values (squares)" — specify which three values.

7. **Section IV-A, "Phase-staggered scheduling":** The claim "DES confirms zero drops at ≥25 kbps vs. 50 kbps under random phase" lacks detail on the DES configuration for this specific test.

8. **Eq. 8 ($L_{\text{cmd}}$):** The denominator uses $(1 - \alpha_{\text{RX}})$ but the text says "net egress = 0.92 s" in Table VIII footnote c, which is $T_c \times (1 - \alpha_{\text{RX}})$. Make the connection explicit.

9. **Reference [47] (dyson_multimodel):** Self-citation of a non-peer-reviewed preprint. Acceptable for AI disclosure but should not be cited for technical claims.

10. **"Model C" and "Model S" terminology:** These labels are introduced in Section I but are not standard. Consider defining them as acronyms (e.g., CCSDS-grounded Model and Simplified Model) for clarity.

11. **Table IX (Link Budget):** The "Aggregate capacity >200 kbps" entry lacks a derivation. Is this $C/N_0$-limited or interference-limited?

12. **Section IV-E, "Empirical anchoring":** The yearly mixture calculation ($\bar{\eta} = 5.6\%$) assumes specific time fractions (95%, 4.9%, 0.1%) that are not justified beyond "conservative."

---

## Overall Recommendation
**Recommendation: Major Revision**

This paper makes a legitimate contribution by systematizing the sizing problem for hierarchical coordination in large space swarms and providing a coherent two-test feasibility framework with closed-form equations. The campaign duty factor $d$ is a practical and well-motivated parameterization that properly contextualizes the stress-case overhead. The gamma unification around CCSDS-grounded values (0.70–0.76) is consistently applied, and the paper is commendably transparent about its limitations, validation gaps, and the what-if nature of the GE channel model.

However, the paper suffers from three fundamental issues that require major revision. First, the validation architecture is entirely self-referential: all tools share the same equations and assumptions, so agreement between them confirms only implementation correctness, not model validity. The paper needs at least one external anchor point (NS-3 comparison, published benchmark, or hardware measurement) to move beyond Tier 1. Second, the paper is substantially too long for a journal article, with detailed edge-case analyses, lengthy footnotes, and defensive clarifications that suggest iterative revision history rather than focused exposition. A 30–40% reduction in length, with material moved to appendices or supplementary files, would significantly improve readability. Third, the practical utility of the framework is limited by the static cluster membership assumption and the absence of any dynamic topology analysis beyond analytical estimates.

The core framework is sound and potentially useful for preliminary mission design. With tighter presentation, at least one external validation point, and honest reframing of the DES and packet-level analysis as implementation verification rather than independent validation, this could become a solid contribution to the field.

---

## Constructive Suggestions
*(Ordered by impact)*

1. **Add one external validation point.** Even a simplified NS-3 TDMA scenario with 100 nodes would provide genuine Tier 2/3 evidence. Alternatively, compare against published DVB-RCS2 scheduling benchmarks with equivalent parameters.

2. **Reduce paper length by 30–40%.** Move the thundering-herd analysis, detailed GE sensitivity derivations, and margin inventory to appendices. Consolidate Tables IV, VIII, X, XI, XII into fewer tables.

3. **Consolidate sensitivity analysis.** Create a single "tornado diagram" showing the sensitivity of $R_{\text{PHY,min}}$ to all uncertain parameters ($T_{\text{acq}}$, $T_{\text{guard}}$, $\gamma$, $p_{BG}$, $S_{\text{eph}}$, $k_c$) ranked by impact. This would be more useful to practitioners than the current scattered sensitivity discussions.

4. **Relabel evidence tiers honestly.** Reserve "Tier 2" for tools with at least partially independent models or parameters. The current slot-sim and CCSDS $\gamma$ derivation are "Tier 1b" (same model, different granularity) at best.

5. **Simulate dynamic cluster reassociation** for at least one non-Walker orbit scenario to bound the static-membership assumption.

6. **Use the DES for scenarios the analytical model cannot handle** (correlated failures, priority queueing, mixed traffic with preemption) to justify its inclusion.

7. **Frame Eq. 14 as systematization, not novelty.** The value is in the specific CCSDS instantiation and the $\gamma$-conditional lookup table (Table XIII), not in the general time-domain expression.

8. **Add a "Quick-Start" box** with the 5 key equations a practitioner needs (Eqs. 1, 4, 14, 15, 16 + Algorithm 1), clearly separated from the analytical development. This would significantly increase practical utility.