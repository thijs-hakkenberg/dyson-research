---
paper: "02-swarm-coordination-scaling"
version: "cu"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-03-05"
recommendation: "Unknown"
---



# Peer Review: Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms

## 1. Significance & Novelty
**Rating: 3 (Adequate)**

The paper addresses a genuine gap: closed-form parametric sizing for hierarchical coordination at scales beyond current constellation practice. The two-layer feasibility framework (byte budget + TDMA airtime) and the campaign duty factor parameterization are useful conceptual contributions. However, the novelty is tempered by the fact that the core analytical results are relatively straightforward engineering calculations (traffic accounting, slot timing, M/D/1 queueing) rather than fundamentally new theory. The paper's value lies primarily in systematically assembling these calculations into a coherent sizing methodology for a specific (and important) application domain. The absence of any external validation limits the significance of the specific numerical recommendations (35 kbps, etc.) to illustrative design exercises.

## 2. Methodological Soundness
**Rating: 3 (Adequate)**

The analytical framework is internally consistent and the decomposition into byte budget and airtime layers is sound in principle. The CCSDS Proximity-1 anchoring of γ is a meaningful improvement over arbitrary assumptions. However, several methodological concerns remain:

- The DES is cycle-aggregated and shares the same equations as the closed-form analysis, making the "verification" largely tautological (the authors acknowledge this, to their credit).
- The GE channel model is parameterized without any ISL measurement data; the per-cycle coherence assumption is a strong structural choice that directly determines the ARQ ineffectiveness finding.
- The slot-level simulator and packet-level simulator both implement the same timing model, so cross-verification between them is weaker than it appears.
- The M/D/1 centralized baseline is intentionally simplified (compute-bound only), making the topology comparison less informative than it could be.

## 3. Validity & Logic
**Rating: 4 (Good)**

The paper demonstrates strong internal logical consistency. The authors are commendably transparent about what is assumption versus derivation, what is verified versus validated, and where the evidence tiers end. Specific strengths:

- The campaign duty factor (d) adequately addresses workload realism: the mapping from mission phases to d values (Table VII) is well-motivated, and the stress-case is now clearly contextualized as a continuous-duty upper bound occurring <1% of operational time.
- The γ unification around 0.76 (CCSDS-derived, replacing the earlier 0.85) appears consistently applied throughout—all feasibility claims, rate recommendations, and tables use Model C values. Model S appears only as a labeled comparison bound.
- The three-layer framework (byte budget, MAC efficiency, TDMA airtime) is logically sound, and the authors correctly note that the MAC efficiency step is a unit conversion rather than an independent test.
- The claim map (Table X) is an exemplary piece of scientific transparency.

One logical concern: the paper simultaneously argues that the 1 kbps budget is justified by the S-band link budget (200 kbps shared among 100 nodes → ~1.5 kbps after γ) and that the coordinator needs 35 kbps PHY. These are consistent (the coordinator channel is a shared resource, not per-node), but the exposition could be clearer about the distinction between the per-node logical allocation and the shared physical channel.

## 4. Clarity & Structure
**Rating: 3 (Adequate)**

The paper is dense but generally well-organized. The roadmap at the start of Section IV is helpful. However:

- The paper is extremely long for a journal article and suffers from significant redundancy. Key results (35 kbps recommendation, γ values, η decomposition) are restated 5-8 times across different sections. This repetition, while perhaps intended for standalone section readability, makes the paper exhausting to review.
- The notation table is comprehensive but the paper introduces additional notation inline that is not always immediately clear.
- The two-model (Model S / Model C) framework, while logically sound, creates cognitive overhead. Every table and figure must be mentally tagged with which model applies.
- Some footnotes are excessively long (e.g., the thundering herd footnote) and would be better as main text or appendix material.
- The abstract is overloaded with specific numbers and caveats, reading more like a summary of results than a motivating abstract.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**

Exemplary. Code and data are publicly available with a specific version tag. The AI disclosure is specific and appropriate (ideation vs. results vs. editing). The validation gap is stated prominently and repeatedly. The claim map explicitly identifies what lacks external validation. The GE model is clearly labeled as a "what-if design tool" rather than a calibrated channel model.

## 6. Scope & Referencing
**Rating: 3 (Adequate)**

The references are generally appropriate and span the relevant domains (CCSDS standards, swarm robotics, constellation management, distributed systems, AoI theory). However:

- The related work section is more of a catalog than a critical synthesis. It would benefit from explicitly positioning this work's contribution relative to the closest prior art (e.g., LEACH, DVB-RCS2 sizing, network calculus bounds).
- Some references are non-archival (Amazon Kuiper overview, DARPA program pages) and may not persist. While flagged as such, the paper relies on them for context.
- Missing references: there is no citation to the substantial body of work on TDMA scheduling for LEO constellations (e.g., work by Radhakrishnan et al. on ISL TDMA, or the extensive Teledesic/Iridium TDMA literature). The DVB-RCS2 reference is used only for γ cross-check, not for its scheduling methodology.
- Network calculus (Le Boudec) is cited but not applied; a deterministic worst-case bound would complement the mean-value approach and strengthen the feasibility claims.

---

## Major Issues

1. **The DES verification provides minimal independent value beyond confirming code correctness.**
   - The authors acknowledge this (Tier 1 verification), but the paper still devotes substantial space to DES results that match closed-form means to <0.1%. The distributional analysis (Fig. 5, buffer sizing) is the DES's genuine contribution, but it is conditional on the assumed ON/OFF Markov campaign process, which is itself unvalidated.
   - *Why it matters:* Readers may overestimate the level of validation. The claim map helps, but the DES sections still read as if they provide stronger evidence than they do.
   - *Remedy:* Consolidate DES discussion. State the code-correctness confirmation in one sentence. Focus DES presentation entirely on the distributional/buffer analysis, with explicit caveats about the campaign process assumption. Consider moving mean-value comparisons to an appendix.

2. **The packet-level validation (Section IV-J) is a parameter estimation exercise, not independent validation.**
   - Computing γ from CCSDS framing specifications is valuable for anchoring the parameter, but it uses the same timing model as the rest of the analysis. The DVB-RCS2 cross-check (γ = 0.745 ± 0.07) is the closest thing to independent evidence, but DVB-RCS2 terminals are ground equipment, not ISL modems.
   - *Why it matters:* The entire rate recommendation (30 vs. 35 kbps) hinges on γ. A 10% error in γ shifts the recommendation by 3-5 kbps (as the authors note). Without hardware measurements, the uncertainty is real.
   - *Remedy:* The authors should more prominently quantify the sensitivity of the design recommendation to γ uncertainty. A table showing: "if γ_measured = X, then R_PHY_min = Y" across the plausible range (0.65-0.85) would be more useful than the current presentation. The γ-conditional PHY lookup in Section V-C partially does this but should be elevated to a primary result.

3. **The fleet-level scaling argument (spatial reuse) is insufficiently developed for the claims made.**
   - The paper titles itself for "large autonomous space swarms" and discusses 10^5 nodes, but all validated results are per-cluster (k_c = 50-500). The fleet-level extension via Eq. 15 (T_c^fleet = G · T_c) is acknowledged as an "order-of-magnitude plausibility argument," but the paper's framing (title, abstract, introduction) implies broader applicability.
   - *Why it matters:* The gap between per-cluster sizing and fleet-level feasibility is where the hardest problems live (inter-cluster interference, dynamic topology, near-far effects). Presenting per-cluster results under a fleet-level title may mislead practitioners.
   - *Remedy:* Either (a) retitle to emphasize per-cluster scope ("Per-Cluster Design Equations..."), or (b) develop the fleet-level analysis more rigorously (at minimum, a parametric sensitivity to R and F with explicit assumptions about antenna patterns and orbital geometry). The current treatment is too thin for the paper's ambitions.

4. **The static cluster membership assumption is more limiting than acknowledged for cross-plane constellations.**
   - The J2 analysis (Section V-C) shows zero re-association for co-orbital clusters but ~0.014/orbit for cross-plane. For a Walker constellation with 72 planes, this is non-trivial. The 14.8 kB re-association overhead may be small per event, but the frequency and coordination complexity of re-association (which nodes move, how state is transferred, what happens during transition) are not modeled.
   - *Why it matters:* Many practical mega-constellations are multi-plane. The paper's applicability to these systems is unclear.
   - *Remedy:* Provide a more detailed analysis of re-association frequency for representative Walker constellations, including the transient coordination gap during handoff. Alternatively, explicitly restrict scope to co-planar formations.

5. **The 1 kbps per-node budget justification is circular in places.**
   - The budget is justified by the S-band link budget (200 kbps / 100 nodes ≈ 2 kbps raw → 1.5 kbps after γ → 1 kbps with margin). But the link budget assumes specific antenna gains (6 dBi), power (1 W), and range (500 km) that are themselves design choices. The paper then derives that the coordinator needs 35 kbps—which is the aggregate channel rate, not the per-node rate—but the relationship between these is not always clear.
   - *Why it matters:* The 1 kbps budget is the single most consequential assumption. If it were 2 kbps, stress-case η halves; if 0.5 kbps, it doubles to infeasibility. The paper acknowledges this scaling but doesn't adequately justify why 1 kbps is the right design point.
   - *Remedy:* Present the 1 kbps budget as a parametric choice (which it is) rather than a derived constraint. Show the feasibility envelope as a function of C_node (e.g., a figure with C_node on x-axis and feasible k_c on y-axis for different d values). This would be more useful to practitioners than fixing C_node = 1 kbps.

## Minor Issues

1. The abstract contains too many specific numbers (20 kbps, 27 kbps, 35 kbps, 5 ms, 4.7 ms, 46%, 5-10%, 0.76, 0.70) making it difficult to parse. Consider a more narrative abstract with key results only.

2. Table I (notation): α_RX is listed as "≈ 0.908" but this is a derived quantity that depends on the PHY rate. The table should note this more clearly or give the formula.

3. Equation 6 (η_canonical): the notation p_cmd appears here but is not in the notation table (Table I). Similarly, the relationship between p_cmd and d is explained in prose but could be formalized.

4. Section III-B-2: "Each cluster coordinator sends a single 512-byte summary per cycle" — the breakdown (48+48+13+32+371 = 512 B) allocates 371 B to "metadata/CRC," which seems disproportionate. Is this padding? If so, the effective summary could be much smaller.

5. The thundering herd analysis (footnote 1) is interesting but belongs in the main text or an appendix, not a footnote. The BEB convergence analysis (2 doubling rounds) deserves more space.

6. Table VI (superframe): the ACK mini-slot explanation in footnote (a) is convoluted. The claim that a 0.5 ms ACK fits within the 1.0 ms jitter sub-slot of the 4.7 ms guard needs a timing diagram.

7. Fig. 1 is referenced but described only as a PDF file. The caption mentions "Labels: aggregation ratios" but without seeing the figure, it's unclear if these are present.

8. The paper uses both "kbps" and "bps" without always being consistent about whether these are information or PHY rates. While the convention is stated (PHY unless labeled), some passages are ambiguous.

9. Section IV-A: "Phase-staggered scheduling... DES confirms zero drops at ≥25 kbps vs. 50 kbps under random phase" — this is stated without supporting data. A brief table or figure would strengthen this claim.

10. The Raft consensus analysis (Eq. 7) assumes serialized votes over the shared channel. In practice, Raft leader election involves parallel vote requests; the serialization assumption may overestimate overhead.

11. Reference [55] (dyson_multimodel) is a self-citation to a non-peer-reviewed preprint. While disclosed, it should be flagged as such in the bibliography.

12. The paper would benefit from a consolidated "assumptions" table listing all key assumptions (static membership, i.i.d. failures, per-cycle GE coherence, centralized command generation, etc.) with their impact on results.

---

## Overall Recommendation
**Recommendation: Major Revision**

This paper makes a credible contribution by systematically deriving closed-form sizing equations for hierarchical coordination in space swarms, anchored in CCSDS standards. The two-layer feasibility framework is conceptually sound, the campaign duty factor elegantly addresses workload realism, and the scientific transparency (claim map, validation gap acknowledgment, V&V tiers) is exemplary for a preliminary design study.

However, the paper has significant issues that prevent acceptance in its current form. The most critical are: (1) the fleet-level claims exceed the per-cluster evidence base; (2) the DES and packet-level "validation" provide less independent evidence than the presentation implies, despite the authors' own caveats; and (3) the paper is substantially too long, with extensive redundancy that obscures rather than clarifies the core contributions. The 1 kbps budget, while acknowledged as parametric, should be treated more explicitly as a design variable rather than a constraint.

The paper would be significantly strengthened by: tightening the scope to match the evidence (per-cluster sizing), reducing length by 30-40% through consolidation of redundant material, presenting the feasibility envelope as a function of C_node (not just at C_node = 1 kbps), and more prominently featuring the γ-conditional design lookup as the primary practitioner tool. The generalized γ expression (Eq. 19) is genuinely useful and should be elevated as a key contribution. With these revisions, the paper would be a solid contribution to the preliminary design literature for large-scale space systems.

## Constructive Suggestions

1. **Highest impact:** Create a single "master feasibility chart" showing feasible (k_c, C_node, d) combinations as a 2D heatmap or contour plot, with γ as a parameter. This would be the paper's most useful practitioner artifact and would subsume many of the individual tables.

2. **Second highest:** Reduce paper length by ~30%. Consolidate the DES sections into a single subsection focused on distributional/buffer analysis. Move Model S results to an appendix. Eliminate redundant restatements of the 35 kbps recommendation.

3. **Third:** Develop the γ-conditional PHY lookup (currently buried in Section V-C) into a primary figure with worked examples for 3-4 representative link types (Prox-1 S-band, Ka-band, proprietary ISL, UHF). This makes Eq. 19 actionable.

4. **Fourth:** Add a network calculus worst-case bound (using the Le Boudec framework already cited) as a complement to the mean-value analysis. This would provide deterministic guarantees that are more appropriate for safety-critical coordination.

5. **Fifth:** Explicitly scope the title and abstract to per-cluster sizing, or develop the fleet-level analysis to the point where it can support the current title. A possible compromise: "Per-Cluster Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms."

6. **Sixth:** Replace the current abstract with a shorter, more narrative version that states the problem, approach, and 3-4 key findings without exhaustive numerical detail.