---
paper: "02-swarm-coordination-scaling"
version: "dg"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-03-05"
recommendation: "Unknown"
---



# Peer Review: "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version DG)

---

## 1. Significance & Novelty
**Rating: 3 (Adequate)**

The paper addresses a genuine gap: closed-form per-cluster sizing equations for hierarchical coordination at the 10³–10⁵ node scale with byte-level traffic accounting. The two-test feasibility framework (byte budget + TDMA airtime) is a useful conceptual contribution, and the campaign duty factor parameterization is a sensible engineering abstraction. However, the novelty is tempered by several factors: (1) the individual analytical components (TDMA slot efficiency, GE channel models, M/D/1 queueing, AoI under geometric sampling) are well-established; (2) the integration, while thorough, is essentially a parametric bookkeeping exercise rather than a fundamentally new analytical result; (3) the absence of any external validation means the contribution remains a design framework proposal rather than a validated methodology. The practical value hinges entirely on whether the parameter assumptions (1 kbps, 256 B, static clusters) are representative—something the paper cannot yet demonstrate.

---

## 2. Methodological Soundness
**Rating: 3 (Adequate)**

The analytical framework is internally consistent and carefully constructed. The three-layer decomposition (byte budget, MAC efficiency, TDMA airtime) is logically sound, and the authors are commendably transparent about what each layer does and does not capture. However, several methodological concerns remain:

- The DES is cycle-aggregated and shares the same equations as the analytical model, making the "verification" largely tautological (the authors acknowledge this). The distributional tails from the DES (Fig. 3) are the only non-trivial DES output, but these are conditioned on the ON/OFF Markov burst model—itself unvalidated.
- The slot-level simulator provides genuine value in quantifying the ARQ×TDMA coupling (52.7% miss rate), but this result applies only to Model S at 24 kbps—a configuration the paper already declares infeasible under Model C. The design-relevant coupling analysis at 30–35 kbps under Model C is done analytically (margin arithmetic), not via simulation.
- The GE channel model is appropriately framed as a what-if tool, but the default parameterization (p_BG = 0.50, p_B = 0.90) lacks any empirical grounding for ISL channels. The geometric coherence-time argument (1 m panel, 2°/s tumble → τ_c ≈ 14 s) is a rough order-of-magnitude estimate that conflates structural shadowing with channel fading.

---

## 3. Validity & Logic
**Rating: 4 (Good)**

The internal logic is generally rigorous. Specific strengths:

- The gamma unification is now consistently applied: γ₂₄ = 0.761, γ₃₀ = 0.745, γ₃₅ = 0.732, all derived from Eq. 8 with CCSDS Proximity-1 framing. The consistency ledger (Table IX footnote) is a welcome addition. Model S (γ = 0.949) is clearly quarantined to Table VI and Fig. 4.
- The stress-case η_S ≈ 46% is now properly contextualized as a continuous-duty upper bound occurring <1% of operational time (Table VII, yearly mixture calculation). The campaign duty factor d provides a clean parameterization.
- The α_RX clarification (computed output, not free parameter) resolves a potential circularity concern.
- The three-layer framework is logically coherent: Test A is necessary (information-theoretic), Test B is sufficient (scheduling), and the heuristic is correctly identified as a lower bound equivalent to Test B under simplifying assumptions.

One logical concern: the paper claims topology-invariance of η_cmd under centralized command generation, but this holds only for broadcast commands. For unicast (q > 0), the stagger L_cmd depends on α_RX, which depends on the hierarchical topology. The paper partially addresses this (Eq. 6) but could be clearer that topology-invariance is conditional on q = 0.

---

## 4. Clarity & Structure
**Rating: 3 (Adequate)**

The paper is thorough to the point of being dense. At ~12 pages of technical content with 12 tables, 4 figures, and an algorithm, the information density is very high. Several structural issues:

- The notation table (Table I) is comprehensive but the sheer number of symbols (>25) creates cognitive load. Some symbols are overloaded or context-dependent (e.g., γ with various subscripts, multiple η variants).
- The "slot-timing models" paragraph at the very start of the introduction is jarring—this is implementation detail that belongs in Section IV or V.
- The paper oscillates between presenting results and re-explaining the framework. For example, the feasibility framework box in Section IV is helpful, but the subsequent "Parameter dependency and test coupling" paragraph largely restates what was already said.
- The validation gap is discussed in at least four separate locations (abstract, Section III-A, Section V-A, Section V-B), creating redundancy. While transparency about limitations is valued, consolidation would improve readability.
- Several tables (especially Tables II, VIII, IX, X) have extensive footnotes that contain substantive technical content—sometimes more than the table itself. This material should be in the main text.

---

## 5. Ethical Compliance
**Rating: 5 (Excellent)**

Exemplary transparency: code and data are publicly available with a specific version tag; AI usage is disclosed with specific model identifiers and scope limitations; the validation gap is prominently acknowledged in the abstract, body, and conclusion; the claim map (Table XI) explicitly categorizes every result by evidence tier. This level of disclosure exceeds typical standards.

---

## 6. Scope & Referencing
**Rating: 3 (Adequate)**

The reference list (60+ entries) covers the major relevant areas: CCSDS standards, constellation operations, swarm robotics, distributed systems, AoI theory, and queueing theory. However:

- The paper would benefit from citing recent work on actual ISL channel characterization (e.g., Laser Communication Relay Demonstration results, or Starlink ISL performance analyses) to ground the GE parameterization discussion.
- Network calculus [Le Boudec] is cited but not used; the paper could strengthen its worst-case bounds by applying service-curve analysis rather than relying solely on mean-value accounting.
- The DVB-RCS2 comparison is appropriate but brief; a more detailed comparison of the γ derivation methodology with DVB-RCS2 terminal efficiency measurements would strengthen Section IV-J.
- Some references are non-archival (Amazon Kuiper, DARPA programs) and may not be accessible long-term.

---

## Major Issues

**1. The DES provides negligible independent verification value.**
The authors correctly acknowledge (Section III-A, Table XI) that the DES reproduces analytical means "by construction" and that agreement is tautological. The sole non-tautological contribution is distributional tails (Fig. 3), which are conditioned on an unvalidated burst model. The slot-sim's primary result (52.7% miss rate) applies to a configuration already declared infeasible. This means the paper's core claims rest entirely on analytical equations with no independent verification.

*Why it matters:* For a journal publication, readers need confidence that the framework produces correct results beyond self-consistency. The current V&V structure is honest but insufficient.

*Remedy:* (a) Implement the TDMA scheduling in NS-3 (even for a single cluster) to provide genuine Tier-2 validation of the slot-timing model. (b) Alternatively, compare the γ derivation against published DVB-RCS2 terminal efficiency measurements at comparable data rates to provide at least one external anchor point. (c) If neither is feasible pre-publication, restructure the paper as a "design framework proposal" rather than implying validated results, and reduce the DES discussion to a brief implementation-correctness note.

**2. The 1 kbps per-node budget is a critical assumption that is insufficiently justified.**
The entire feasibility analysis—including the binding coordinator bottleneck, the 35 kbps recommendation, and the stress-case η—is conditioned on C_node = 1 kbps. The link budget (Table IV) derives this from aggregate S-band capacity with 50% margin, but the 50% margin allocation is itself an assumption. At 2 kbps (which the link budget could support), stress-case η halves and TDMA sizing becomes non-binding (as the authors note in Section III-E). This means the paper's most interesting results (the PHY rate transition, ARQ infeasibility at 24 kbps) are artifacts of the 1 kbps choice.

*Why it matters:* If the binding constraint disappears at 2 kbps, the elaborate TDMA analysis (Sections IV-A through IV-J) becomes unnecessary for most practical deployments. The paper should either justify why 1 kbps is the appropriate design point or present results parametrically across the feasible budget range.

*Remedy:* Add a systematic sensitivity analysis showing how the feasibility boundary (minimum PHY rate, ARQ viability, stagger requirements) varies with C_node ∈ {0.5, 1, 2, 5, 10} kbps. Table II-A provides a start but lacks the TDMA-layer analysis. This would transform the paper from a single-point design study into a genuinely parametric sizing tool.

**3. Static cluster membership assumption limits applicability.**
The paper assumes static cluster membership for 1-year simulations and claims this is "exact for co-planar formations." However, the target scale (10⁵ nodes) necessarily involves multiple orbital planes. The J2 analysis (Section V-C) estimates cross-plane re-association at ~0.014/orbit fleet-wide, but this is a fleet-average that masks worst-case clusters at plane boundaries. More critically, re-association triggers coordinator handoffs (3–5 s optical, ~160 s RF), which interact with the TDMA superframe in ways not analyzed.

*Why it matters:* For Walker constellations at 10⁵ nodes, cross-plane dynamics are not a corner case—they are the dominant topology change mechanism. The interaction between re-association, handoff, and TDMA scheduling could invalidate the static-membership feasibility results.

*Remedy:* Either (a) restrict the scope to co-planar formations (reducing the claimed applicability) or (b) analyze the worst-case re-association rate for boundary clusters and its impact on effective η and TDMA margin. A simple model: if a cluster at a plane boundary experiences re-association every ~90 min, what fraction of cycles are disrupted?

**4. The generalized gamma expression (Eq. 8) is presented as a contribution but is standard TDMA engineering.**
Eq. 8 is T_payload / T_slot with the slot decomposed into payload + FEC + framing + guard + acquisition. This is textbook TDMA efficiency (as the authors acknowledge by citing DVB-RCS2). The "specific contribution" claimed—rate-dependent parameterization under CCSDS framing—amounts to substituting CCSDS Proximity-1 parameters into the standard formula. While useful as a reference calculation, this does not constitute a novel analytical result.

*Why it matters:* Overclaiming the novelty of standard engineering calculations weakens the paper's credibility and distracts from the genuine contributions (the two-test framework, campaign duty factor, ARQ×TDMA coupling analysis).

*Remedy:* Reframe Eq. 8 as a "reference parameterization" rather than a contribution. Emphasize instead the coupling between γ(R_PHY), ARQ margin, and half-duplex partitioning—which is the actual novel element.

---

## Minor Issues

1. **Abstract length.** At ~200 words, the abstract is dense but within IEEE limits. However, the parenthetical notation (γ₂₄ = 0.761, γ₃₀ = 0.745) is excessive for an abstract; summarize as "γ ≈ 0.70–0.76."

2. **Table I placement.** Placing the notation table before the introduction text is unconventional for IEEE TAES. Consider moving it after Section I-A or to an appendix.

3. **Eq. 1 (M_total).** The third term (N/(k_c · k_r)) assumes uniform fan-out; state this assumption explicitly.

4. **Section III-B.2, "thundering herd" analysis.** The Slotted ALOHA with BEB analysis is interesting but tangential to the main TDMA sizing contribution. Consider moving to an appendix.

5. **Fig. 1 is referenced but described generically.** The caption says "Labels: aggregation ratios" but the figure content is not described in sufficient detail for a reader without access to the PDF.

6. **Table VI header.** "Illustrative ARQ×TDMA Coupling: Deadline Miss Rate (%) Under Optimistic Timing (Model S Only)" — the "(Model S Only)" caveat should be more prominent, perhaps in the table title rather than a superscript.

7. **Section IV-B.** "Mean ≈ T_c/2 = 5 s" — this holds only for periodic reporting (p_exc = 1.0); for exception reporting, mean AoI = T_c / p_exc. Clarify.

8. **Eq. 4 (η_consensus).** The variable f_decision is decisions per cycle but the equation doesn't clearly distinguish between decisions requiring full quorum rounds vs. leader-only operations. Raft leader operations (log replication) are cheaper than elections.

9. **Table III footnote (d).** Message size justification is valuable but should be in the main text, not a footnote.

10. **Section IV-A, "Phase-staggered scheduling."** The claim "DES confirms zero drops at ≥25 kbps vs. 50 kbps under random phase" lacks detail—what was the DES configuration? How many runs?

11. **Consistency:** The abstract says "γ ≈ 0.70–0.76" but the text uses γ₃₅ = 0.732 and γ₅₀ = 0.695, which fall outside this range. Expand to "0.70–0.76 at 24–35 kbps."

12. **Reference [12] (dyson_multimodel)** is a self-citation to a non-peer-reviewed preprint. Consider removing or replacing with a methodological reference.

13. **"Tight formation control requires optical ISL"** (abstract, first sentence) — this scope exclusion should be justified with a quantitative argument (e.g., formation control bandwidth requirements exceed S-band capacity by X×).

14. **Algorithm 1, Line 3.** The comment says "η₀ = 5% (hb+summ+elec)" but the decomposition in Section III-E gives heartbeats = 5.1%, summaries = 0.4%, elections < 0.1%, totaling ~5.6%. Reconcile.

---

## Overall Recommendation
**Recommendation: Major Revision**

This manuscript presents a carefully constructed parametric sizing framework for hierarchical coordination in large space swarms. The two-test feasibility decomposition (byte budget + TDMA airtime), the campaign duty factor parameterization, and the systematic treatment of ARQ×TDMA coupling represent genuine engineering contributions. The transparency about validation gaps, the claim map by evidence tier, and the open-source data availability are exemplary practices that should be commended.

However, the paper suffers from three fundamental weaknesses that prevent acceptance in its current form. First, the absence of any external validation—combined with a DES that is tautological by construction—means the framework's correctness rests entirely on analytical self-consistency. For a journal of IEEE TAES's stature, at least one independent verification anchor (NS-3 single-cluster simulation, DVB-RCS2 efficiency comparison, or hardware γ measurement) is needed. Second, the entire analysis is conditioned on a 1 kbps per-node budget that, if relaxed to 2 kbps, renders the most interesting results (PHY rate transition, ARQ constraints) non-binding. The paper needs to either justify this specific budget or present truly parametric results. Third, the static cluster membership assumption limits applicability to co-planar formations, which is a significant scope restriction for the claimed 10⁵-node scale.

The paper's strengths—rigorous internal consistency, transparent limitation disclosure, actionable Algorithm 1, and comprehensive sensitivity analysis—provide a strong foundation for revision. Addressing the major issues above would elevate this from a preliminary design exercise to a publishable sizing methodology.

---

## Constructive Suggestions
*(Ordered by impact)*

1. **Add one external validation anchor.** Even a simplified NS-3 simulation of a single 100-node cluster with CCSDS-like framing would provide genuine Tier-2 evidence. Alternatively, compare γ predictions against published DVB-RCS2 terminal measurements at 24–64 kbps.

2. **Parametrize over C_node.** Present the feasibility boundary (minimum PHY rate, ARQ viability, stagger) as a function of C_node ∈ {0.5, 1, 2, 5} kbps. This transforms the paper from a point design to a design tool and honestly shows where the TDMA analysis adds value (low C_node) vs. where it's unnecessary (high C_node).

3. **Analyze dynamic cluster membership.** For a Walker constellation, compute the worst-case re-association rate at plane boundaries and its impact on effective η and TDMA margin. Even a simple analytical bound would suffice.

4. **Tighten the paper.** The manuscript is ~30% longer than necessary. Consolidate the validation gap discussion into one location; move the thundering-herd analysis and detailed footnotes into an appendix or supplementary material; reduce redundancy between the feasibility framework box and surrounding text.

5. **Reframe the γ contribution.** Present Eq. 8 as a reference parameterization, not a novel result. Emphasize the coupling analysis (γ × ARQ × half-duplex) as the actual contribution.

6. **Strengthen the GE discussion.** Add a brief survey of measured ISL channel statistics (even from optical ISL campaigns) to provide context for the assumed p_BG and p_B ranges. If no ISL data exist, state this explicitly and frame the entire GE analysis as a sensitivity study over plausible parameter ranges.