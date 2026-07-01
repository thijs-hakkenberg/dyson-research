---
paper: "02-swarm-coordination-scaling"
version: "ca"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-28"
recommendation: "Major Revision"
---



# Peer Review: Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms

## 1. Significance & Novelty
**Rating: 3 (Adequate)**

The paper addresses a genuine gap: no prior work provides closed-form parametric sizing for hierarchical coordination at the $10^3$–$10^5$ node scale with byte-level traffic accounting. This is a useful contribution for systems engineers designing future mega-constellations. However, the novelty is tempered by several factors: (a) the core analytical results are relatively straightforward bandwidth accounting rather than deep theoretical contributions; (b) the "design equations" are primarily dimensional analysis and bookkeeping rather than novel mathematical formulations; (c) the most interesting finding—that command traffic dominates and is topology-invariant—is somewhat intuitive once the message model is specified. The three-layer feasibility framework (byte budget, MAC efficiency, TDMA airtime) is a sensible organizational contribution but not conceptually deep. The GE recovery characterization and AoI analysis apply standard tools (Markov chains, geometric distributions) to the specific problem context competently but without methodological novelty.

## 2. Methodological Soundness
**Rating: 3 (Adequate)**

The methodology is internally consistent but raises several concerns:

- The cycle-aggregated DES is well-suited to the problem scope but operates at a level of abstraction where many of the interesting engineering challenges (MAC contention, antenna scheduling, Doppler, interference) are absorbed into a single parameter $\gamma$. The authors acknowledge this clearly.
- The four-tier verification taxonomy (code, model, packet-level, remaining gap) is well-structured and honestly presented. The IEEE 1012 framing is appropriate.
- The Monte Carlo configuration (30 replications) is adequate for mean estimation but potentially thin for tail statistics (P99 AoI). The authors report bootstrap CIs, which partially addresses this.
- The GE channel model is appropriately grounded in Lutz et al. and ITU-R P.681, though the mapping from terrestrial mobile satellite channels to ISL self-blockage is acknowledged as analogical rather than validated.
- The static topology assumption is reasonable for bandwidth sizing but limits the applicability of AoI and latency results to dynamic constellations.

## 3. Validity & Logic
**Rating: 4 (Good)**

The paper demonstrates strong internal consistency:

- The campaign duty factor ($d$) effectively addresses workload realism. The decomposition $\eta = \eta_0 + d \cdot \eta_{\text{cmd}}$ is clean, and Table 8 convincingly shows that realistic $d$ values (0.01–0.10) bring overhead to manageable levels. This is a significant improvement in contextualizing the stress-case.
- The gamma unification ($\gamma = 0.76$) is consistently applied throughout. The derivation from CCSDS Proximity-1 framing (Eq. 7, Table 11) is traceable and the decomposition into four sub-efficiencies is transparent. The replacement of the earlier 0.85 is well-documented.
- The stress-case ($\eta_S \approx 46\%$) is now properly framed as a continuous-duty upper bound ($d = 1$), with Table 8 providing the operational context. This is well-handled.
- The three-layer feasibility framework is logically sound: byte budget → MAC efficiency → TDMA airtime is a natural decomposition, and Table 7 maps each workload profile through all three layers clearly.
- One logical concern: the paper claims the DES "verifies" the analytical equations, but since the DES implements those same equations, the $<0.1\%$ agreement is tautological. The authors acknowledge this ("expected by construction") but could be more forthright about the limited verification value.

## 4. Clarity & Structure
**Rating: 3 (Adequate)**

The paper is comprehensive but suffers from organizational challenges:

- At ~15 journal pages of dense technical content, the paper tries to cover too much ground. The reader must track multiple interacting models (analytical, DES, slot-level, packet-level), four topologies, three workload profiles, and numerous sensitivity analyses.
- The roadmap paragraph at the start of Section IV is helpful but insufficient given the complexity. Several results are introduced in one section and cross-referenced from multiple others, creating a non-linear reading experience.
- Tables are generally well-constructed, but there are 16 tables and 12 figures—an unusually high count that fragments the narrative. Some consolidation would improve readability.
- The notation table (Table I) is appreciated but incomplete; several symbols used later ($\alpha_{\text{RX}}$, $d$, $q$, $L_{\text{cmd}}$) are not listed.
- The distinction between $\eta$, $\eta_0$, $\eta_{\text{cmd}}$, $\eta_{\text{total}}$, $\eta_{\text{eff}}$, $\eta_S$, $\eta_E$, and $\eta_{\text{sector}}$ requires careful tracking and could benefit from a consolidated definition table.

## 5. Ethical Compliance
**Rating: 4 (Good)**

- Data availability is exemplary: open-source code, tagged release, full parameter tables, and reproducible MC configuration.
- AI disclosure is present and appropriately scoped ("motivated aspects... but is not validated here").
- The anonymous authorship ("Project Dyson Research Team") is noted as temporary per IEEE policy, which is acceptable for review but must be resolved for publication.
- The paper honestly identifies validation gaps and does not overclaim.

## 6. Scope & Referencing
**Rating: 3 (Adequate)**

- The reference list (55 items) covers the major relevant areas: constellation management, swarm robotics, distributed systems, CCSDS standards, queueing theory, and AoI.
- Notable gaps: no references to actual TDMA implementations in space (e.g., CCSDS CFDP, AIS for maritime satellites), no citation of network calculus applications to satellite systems specifically, and limited engagement with the DTN/CGR community's scheduling work beyond a single Fraire citation.
- The paper would benefit from engaging with recent work on LEO constellation coordination (e.g., Handley's follow-up work, Bhattacherjee et al.'s network topology optimization) more substantively rather than as passing citations.
- Some references are non-archival (Amazon Kuiper overview, DARPA program pages, DOD fact sheets), which is acceptable for context but should be minimized.

---

## Major Issues

1. **The DES verification provides negligible independent validation, and this should be stated more clearly.**
   - The DES implements the same equations it claims to verify; the $<0.1\%$ agreement (Table 6) is a code correctness check, not model validation. While the authors acknowledge this ("expected by construction"), the paper still presents DES results prominently alongside analytical values as if the comparison is informative.
   - *Why it matters:* Readers may overestimate the validation status of the framework. The genuine validation contributions are the slot-level TDMA simulator (which reveals ARQ coupling invisible to the fluid-server DES) and the packet-level $\gamma$ derivation.
   - *Remedy:* Restructure the verification narrative to lead with the slot-level and packet-level results as the primary validation contributions. Relegate the DES-vs-analytical comparison to a brief implementation correctness statement. Consider removing Table 6 or reducing it to a footnote.

2. **The packet-level validation (Section IV-J), while valuable, validates only $\gamma$—not the full system model.**
   - The packet-level simulator derives $\gamma = 0.76$ from CCSDS framing, which is useful. However, it does not validate the message-layer traffic model, the coordinator queueing behavior, the GE recovery dynamics, or the AoI distributions. The claim of "genuinely independent validation" overstates the scope.
   - *Why it matters:* The paper's central claims about overhead scaling, coordinator sizing, and loss recovery remain validated only by models that share the same assumptions.
   - *Remedy:* Reframe Section IV-J as "$\gamma$ derivation and feasibility boundary validation" rather than general "packet-level validation." Explicitly state which claims remain analytically derived only. Consider whether a comparison against any real-world ISL telemetry data (even from Iridium or Starlink public disclosures) could provide external grounding.

3. **The sectorized mesh comparison is problematic and should be either substantially reworked or removed.**
   - The paper repeatedly disclaims that the sectorized mesh has "different functional scope" and that "overhead comparisons are not meaningful"—yet it appears in every comparison table and figure. This creates cognitive dissonance: why include a comparator that the authors themselves say cannot be meaningfully compared?
   - *Why it matters:* The inclusion implicitly suggests the hierarchy is superior (lower overhead), while the disclaimers attempt to prevent this interpretation. This is confusing and potentially misleading.
   - *Remedy:* Either (a) remove the sectorized mesh entirely and focus the comparison on hierarchical vs. centralized bounds, or (b) define a common functional baseline (e.g., "minimum viable coordination: conjunction screening + health monitoring") and compare architectures at equivalent service levels. Option (a) is simpler and would save ~1 page.

4. **The 1 kbps design point needs stronger operational justification.**
   - The paper acknowledges that normal operations use optical ISLs at ≥10 kbps (where "all constraints are non-binding"), and the 1 kbps regime applies only during ISL outages (<1% of lifetime). Yet the vast majority of the analysis—coordinator bottleneck, TDMA scheduling, ARQ infeasibility, superframe budgets—is specific to this rare operating mode.
   - *Why it matters:* The paper's most technically interesting results (TDMA feasibility boundary, GE recovery, superframe timing) apply to a corner case. The normal-operations regime is dismissed in a single sentence ("all feasibility layers trivially satisfied").
   - *Remedy:* Add a brief section (or expand the existing paragraph) analyzing the ≥10 kbps regime with comparable rigor. What are the binding constraints at 10 kbps? At 100 kbps? If the answer is "none within this model," that itself is a useful finding that deserves more than a table footnote. This would also strengthen the paper's relevance to practitioners designing optical-ISL-primary systems.

5. **The generalized $\gamma$ expression (Eq. 13) conflates protocol-specific and geometry-specific terms in a way that limits practical utility.**
   - Equation 13 hardcodes 104 bits of CCSDS Proximity-1 framing overhead. For practitioners using different protocols (e.g., CCSDS TC, custom framing, or non-CCSDS systems), this constant is wrong. The guard and acquisition times are also highly mission-specific.
   - *Why it matters:* The equation is presented as a general practitioner tool but is actually specific to CCSDS Proximity-1.
   - *Remedy:* Generalize Eq. 13 by replacing 104 with a parameter $O_{\text{frame}}$ (framing overhead in bits) and clearly state the CCSDS Proximity-1 value as one instantiation. Provide a second worked example with a different protocol (e.g., CCSDS TC Space Data Link) to demonstrate generality.

6. **Statistical rigor for tail metrics is insufficient.**
   - P99 AoI is computed as the mean of 30 per-run P99 values. With 30 replications, the sampling distribution of the P99 estimator has high variance, particularly for heavy-tailed distributions. The bootstrap CI ([438, 444] s) appears suspiciously tight for a P99 metric.
   - *Why it matters:* Tail statistics are precisely where design margins matter most; underestimating P99 variability could lead to under-provisioning.
   - *Remedy:* Report the distribution of per-run P99 values (min, max, IQR across 30 runs), not just the mean. Consider pooling all samples across runs and computing the fleet-wide P99 directly. Increase to ≥100 replications for tail-metric configurations, or justify why 30 suffices via a convergence analysis.

---

## Minor Issues

1. **Notation inconsistency:** $p_{\text{link}}$ appears in Table 4 but is not defined in Table I. Similarly, $p_{\text{exc}}$ is used extensively but only implicitly defined.

2. **Eq. 2 ($M_{\text{total}}$):** The equation counts messages but the text discusses bytes. Clarify units or provide the byte-equivalent expression.

3. **Table 2 (bandwidth scaling):** The "Coord. bottleneck?" row answers "Yes (21 kbps)" at 1 kbps but the text derives 27 kbps at $\gamma = 0.76$. Clarify which value applies and under what $\gamma$ assumption.

4. **Section III-B-2:** "excluding the coordinator itself" implies $k_c - 1$ members, but some equations use $k_c$. Verify consistency throughout.

5. **Table 5 (link budget):** The system temperature assumption ($T_{\text{sys}} = 290$ K) is appropriate for ground terminals but pessimistic for space-to-space links where sky noise temperature is ~3–20 K. This makes the RF-backup link budget conservative, which should be noted.

6. **Fig. 3 (phase stagger):** Referenced before the TDMA frame model is fully developed. Consider reordering.

7. **"Collision avoidance rate $10^{-4}$/node/s":** This is described as "screening notifications" in the footnote but "priority alerts" in the table. Clarify the operational concept.

8. **Section IV-E:** "Per-message-class decomposition" is stated but not shown as a figure or table. A stacked bar chart would be informative.

9. **Eq. 10 ($L_{\text{cmd}}$):** The denominator uses $T_c \cdot (1 - \alpha_{\text{RX}})$ but earlier text uses 0.80 s without deriving $\alpha_{\text{RX}}$. Show the derivation.

10. **Table 9 (topology comparison):** The "Failure Mode" column lists "Graceful (99.5%)" for hierarchical but this metric is not formally defined or derived in the paper.

11. **Reference [1]:** Citing an FCC filing and a non-archival personal website as a single reference is unusual. Separate these or find an archival source.

12. **The abstract mentions "centralized command generation" as a parenthetical but this is actually a critical assumption that drives the topology-invariance conclusion. Elevate its prominence.**

13. **Section V-B (Limitations):** The J2 perturbation analysis for dynamic topology is a useful addition but reads as an appendix-level calculation inserted into the limitations section. Consider moving to an appendix.

---

## Overall Recommendation
**Recommendation: Major Revision**

This paper makes a legitimate contribution by providing closed-form sizing equations for hierarchical coordination in large spacecraft swarms—a problem space that lacks such tools. The three-layer feasibility framework is well-conceived, the campaign duty factor effectively contextualizes the stress-case, and the CCSDS-grounded $\gamma$ derivation provides genuine physical-layer anchoring. The open-source release and reproducibility posture are commendable.

However, the paper has significant structural and validation issues that must be addressed. The DES verification is largely tautological and should be de-emphasized in favor of the genuinely informative slot-level and packet-level results. The sectorized mesh comparison creates more confusion than insight and should be either properly grounded in equivalent functional scope or removed. The overwhelming focus on the 1 kbps corner case, while technically interesting, undersells the framework's applicability to the ≥10 kbps regime that constitutes >99% of operational time. The paper is also too long and dense for its core contribution; consolidating tables and figures would improve readability substantially.

The most critical revision is to honestly reframe the validation status: the paper provides a well-verified *analytical framework* with one independent physical-layer anchor point ($\gamma$), not a validated system model. This is still valuable—but the current presentation occasionally implies broader validation than has been achieved.

---

## Constructive Suggestions
*(Ordered by impact)*

1. **Restructure the validation narrative** around a clear hierarchy: (a) $\gamma$ derivation from CCSDS (independent), (b) slot-level TDMA timing (reveals ARQ coupling), (c) DES code correctness (implementation check only). Remove or minimize DES-vs-analytical comparison tables.

2. **Add a substantive ≥10 kbps analysis section** (even 1 page) showing what constraints bind at higher rates and where the model's abstraction boundaries lie. This dramatically increases practical relevance.

3. **Resolve the sectorized mesh comparison** by either removing it or defining equivalent-scope service levels for fair comparison.

4. **Consolidate the paper** by merging related tables (e.g., Tables 6 and 12 could be combined; Tables 7 and 8 are closely related), reducing the figure count, and tightening the sensitivity analysis sections.

5. **Generalize Eq. 13** with protocol-agnostic parameters and provide two worked examples with different framing standards.

6. **Strengthen tail-metric statistics** with convergence analysis or increased replication count for P99 configurations.

7. **Add a "Quick-Start" design procedure** (perhaps as a flowchart or algorithm block) showing how a practitioner would use the equations to size a specific mission. This would significantly increase the paper's practical impact and justify the "design equations" framing in the title.