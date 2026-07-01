---
paper: "02-swarm-coordination-scaling"
version: "ch"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-03-01"
recommendation: "Major Revision"
---



# Peer Review: Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms

## 1. Significance & Novelty
**Rating: 3 (Adequate)**

The paper addresses a genuine gap: closed-form sizing relationships for hierarchical coordination at the $10^3$–$10^5$ node scale with byte-level traffic accounting. The two-layer feasibility framework (byte budget + TDMA airtime) and the decomposition into $\eta_0$ and $\eta_{\text{cmd}}$ are useful structuring contributions. However, the novelty is tempered by the fact that the core equations are relatively straightforward bandwidth accounting—the intellectual contribution lies more in the systematic assembly and parameterization than in analytical depth. The campaign duty factor $d$ is a sensible and practically important addition that substantially contextualizes the stress-case results. The generalized $\gamma$ expression (Eq. 14) is genuinely useful for practitioners. The paper would benefit from a clearer articulation of what design decisions these equations enable that were previously impossible—currently the framing emphasizes the gap more than the enabled capability.

## 2. Methodological Soundness
**Rating: 3 (Adequate)**

The three-layer verification approach (analytical → DES → slot-level/packet-level) is well-structured in principle. The $\gamma$ unification via CCSDS Proximity-1 derivation ($\gamma_{C,24} = 0.760$) is a clear improvement and is consistently applied throughout—I verified this across Tables III, V, VI, VIII, and the feasibility algorithm. The campaign duty factor $d$ adequately addresses workload realism: the Bernoulli/ON-OFF models are appropriate, and the empirical anchoring to ESA maneuver cadence and Starlink orbit-raising is convincing.

However, the DES verification remains primarily an internal consistency check. The authors now acknowledge this explicitly (Tier 1 vs. Tier 2 vs. Tier 3 in Table XII), which is an improvement, but the paper still devotes substantial space to DES-analytical agreement that is, by construction, guaranteed. The DES's distributional contribution (Fig. 7, buffer CDFs under stochastic campaigns) is genuine but modest—it reveals bimodality and ON/OFF tail effects, but these are qualitatively predictable from the model structure. The slot-level simulator provides more genuine cross-model value (ARQ×TDMA coupling discovery), though it too shares the same fundamental assumptions.

The packet-level validation (Section IV-J) provides useful anchoring of $\gamma$ in CCSDS standards, which is a meaningful Tier 2 contribution. It does not, however, validate the message model, traffic assumptions, or coordinator queueing—it validates a single parameter. The claim map (Table XII) is commendably honest about what remains unvalidated.

## 3. Validity & Logic
**Rating: 4 (Good)**

The logical structure is generally sound. The stress-case ($\eta_S \approx 46\%$) is now properly contextualized as a continuous-duty upper bound ($d=1$), with clear statements that routine operations occupy $d = 0.01$–$0.10$ and the stress case applies $<$1% of operational time. This is a significant improvement. The three worked campaign scenarios (orbit-raising, station-keeping, collision avoidance) provide concrete anchoring.

The three-layer feasibility framework is logically coherent: byte budget → MAC translation → TDMA airtime, with clear binding conditions for each layer. The observation that Layer 2 binds only at RF-backup rates (1 kbps regime) while both layers are non-binding at ≥10 kbps is an important and well-supported conclusion.

The GE channel analysis is appropriately framed as a parametric sensitivity study rather than a predictive model—the explicit acknowledgment that no ISL-specific GE measurements exist is important. The coherence-time sensitivity analysis (Fig. 5) and the ARQ viability threshold derivation (Section IV-C) are logically tight.

One concern: the coordinator failure transient analysis (Section III-B.2) claims compound probability of $6.3 \times 10^{-12}$ s$^{-1}$ assuming statistical independence, then notes common-cause failures could correlate these events. This caveat deserves more prominence given that the very scenario motivating RF-backup (solar events) is precisely the common-cause failure mode.

## 4. Clarity & Structure
**Rating: 3 (Adequate)**

The paper is dense but generally well-organized. The roadmap at the start of Section IV is helpful. The notation table (Table I) is comprehensive. The distinction between Model S and Model C is clearly maintained throughout.

However, the paper suffers from excessive length and repetition. Key results are stated in the abstract, restated in the introduction, derived in the results, and summarized again in the discussion. The overhead decomposition ($\eta = \eta_0 + d \cdot \eta_{\text{cmd}}$) appears in at least five locations with varying levels of detail. Several tables contain overlapping information (e.g., Tables V, VIII, and X all address feasibility at different granularities).

The paper would benefit from consolidation: the 14-page manuscript could likely be reduced to 10–11 pages without loss of substance by eliminating redundancy and moving some sensitivity analyses to supplementary material.

Algorithm 1 is a useful practitioner-facing contribution but would benefit from a worked numerical example walking through each step.

## 5. Ethical Compliance
**Rating: 4 (Good)**

Data availability is excellent: open-source code, tagged release, full parameter tables, and reproducible MC configuration. The AI disclosure is present and appropriately scoped. The acknowledgment of validation gaps is commendably transparent. The evidence-tier framework adapted from IEEE 1012 is a good practice.

Minor concern: the author block uses a team name rather than individual authors, with a note about final publication. This should be resolved before acceptance.

## 6. Scope & Referencing
**Rating: 3 (Adequate)**

The reference list (57 items) covers the major relevant areas: CCSDS standards, swarm robotics, constellation management, distributed systems theory, AoI, and queueing theory. The Lutz et al. and ITU-R P.681 references appropriately ground the GE model. Network calculus (Le Boudec) is cited as a complementary approach.

Missing references that would strengthen the paper:
- Recent work on distributed TDMA for satellite networks (e.g., Radhakrishnan et al., IEEE Access, 2016)
- Operational ISL measurement campaigns (limited but some Iridium data exists in conference proceedings)
- CCSDS 414.0-G-2 (cited in Table VII but not in the bibliography)
- More recent AoI work specific to satellite networks
- The DTN/CGR community has relevant scheduling results not cited

The paper's scope is appropriate for IEEE T-AES, though the absence of any orbital mechanics beyond the J2 perturbation mention in Section V-B makes it lean more toward communications/networking than aerospace systems.

---

## Major Issues

1. **The DES provides limited independent validation beyond distributional analysis.**
   - *Issue:* The DES implements the same equations as the analytical model; agreement to <0.1% is expected by construction. While the authors now explicitly acknowledge this (Tier 1), the paper still allocates significant space to this agreement as if it were validating.
   - *Why it matters:* Readers may overestimate the degree of independent verification. The genuine DES contribution (distributional tails under stochastic campaigns) is diluted by the emphasis on mean-value agreement.
   - *Remedy:* Reduce DES-analytical agreement discussion to a single sentence. Expand the distributional analysis (Fig. 7) with quantitative buffer-sizing recommendations derived from the tail behavior. State explicitly: "DES mean-value agreement is an arithmetic verification, not model validation."

2. **The 289 ms residual margin (2.9% of $T_c$) is uncomfortably thin for a design framework.**
   - *Issue:* Table VII shows 363 ms superframe margin minus 74 ms unmodeled overheads = 289 ms. This leaves no room for any unmodeled effect beyond those enumerated. The authors acknowledge this but recommend 30 kbps as the design point anyway.
   - *Why it matters:* A sizing framework intended for practitioners should include adequate margin. The paper's own Fig. 8 shows that conservative assumptions push the minimum to ~35 kbps, yet 30 kbps is repeatedly stated as "the minimum viable design point."
   - *Remedy:* Recommend 35 kbps as the design point (with 30 kbps as the theoretical minimum). Alternatively, present a margin policy (e.g., "design to ≥10% residual margin") and let the PHY rate follow. The current framing of 30 kbps as "minimum viable" with 2.9% margin is inconsistent with good engineering practice for a design framework.

3. **The topology-invariance claim for $\eta_{\text{cmd}}$ requires stronger qualification.**
   - *Issue:* The paper claims command overhead is "topology-invariant" under centralized broadcast semantics, but this is a strong assumption that may not hold for the target audience. The distributed consensus analysis (Eq. 5) shows $\eta_{\text{consensus}}$ ranges from 2.8% to 31%—a fundamentally different scaling behavior.
   - *Why it matters:* Practitioners designing autonomous swarms are likely considering distributed decision-making. The topology-invariance claim, while technically correct under its assumptions, may mislead readers about the generality of the overhead figures.
   - *Remedy:* Present the centralized and distributed cases as co-equal design options in a summary table, rather than treating centralized as the baseline with distributed as an aside. The current structure buries the distributed case in subsections.

4. **No external validation exists for any claim in the paper.**
   - *Issue:* Table XII honestly shows that Tier 3 (external validation) is empty for all results. The entire framework rests on analytical models verified against implementations of those same models.
   - *Why it matters:* For a journal publication claiming to provide "design equations" for practitioners, the absence of any comparison to operational data, hardware-in-the-loop testing, or even NS-3 simulation is a significant limitation.
   - *Remedy:* (a) Implement at least the single-cluster TDMA scenario in NS-3 with a realistic PHY model to validate the $\gamma$ derivation and superframe timing. (b) Alternatively, compare coordinator ingress sizing against published Iridium NEXT or Starlink operational parameters (even order-of-magnitude). (c) If neither is feasible, strengthen the limitations section to explicitly bound the confidence level of the design equations.

5. **The GE channel model lacks ISL-specific grounding.**
   - *Issue:* The authors acknowledge this (Table IV, footnote a), but the default parameterization ($p_{BG} = 0.50$, $p_B = 0.90$) is used for all numerical results and the 4-cycle P95 recovery claim appears prominently in the abstract.
   - *Why it matters:* The Lutz model was developed for land-mobile satellite channels with fundamentally different propagation characteristics than ISL self-blockage. Using it for ISL without calibration data risks providing misleading design guidance.
   - *Remedy:* (a) Remove specific cycle counts from the abstract; replace with "P95 recovery in 3–18 cycles depending on channel burstiness (Fig. 10b)." (b) Present the sensitivity sweep as the primary result, not the single-point $p_{BG} = 0.50$ case. (c) Add a paragraph discussing what ISL measurement campaign would be needed to calibrate the model.

---

## Minor Issues

1. **Table I notation:** $\gamma$ is listed with two specific values ($\gamma_{24} = 0.760$, $\gamma_{30} = 0.745$) in the notation table. Since $\gamma$ is rate-dependent, list only the general form and reference the specific values to Section IV-J.

2. **Eq. 1 vs. DES:** The paper states $M_{\text{total}}$ counts messages but the DES tracks bytes. Clarify the mapping between message count and byte count explicitly.

3. **Section III-B.2, coordinator failure transient:** "AoI impact: +100–200 s, modest vs. P99 = 441 s" — this is a 23–45% increase in P99; "modest" understates the impact.

4. **Table IX, footnote b:** "Per-message rate; per-cycle ≈ $(1 - p_{\text{loss}})^{k_c}$" — this formula assumes independence, which contradicts the GE model used elsewhere. Note this.

5. **Fig. 3 caption:** "Phase staggering eliminates drops at ~25 kbps vs. 50 kbps under random phase" — specify whether this is Model S or Model C.

6. **Eq. 14 (generalized $\gamma$):** The $10^{-3}$ conversion factor is error-prone. Consider expressing guard/acquisition in seconds throughout for dimensional consistency.

7. **Section IV-E, temporal correlation:** "ON/OFF ($L_{\text{on}} = 100$) produces heavier tails" — 100 cycles = 1000 s ≈ 17 min. Is this a realistic campaign burst length? Justify or sweep $L_{\text{on}}$.

8. **Table VI (superframe):** "Re-sync preamble: 4 ms" appears without derivation. At 30 kbps, 4 ms = 120 bits. Justify this value.

9. **Section V-B:** "J2 perturbation analysis (Walker constellation: 53°, 550 km, 72 planes × 22 sats)" — this specific constellation is introduced without motivation. Is this Starlink-like? State explicitly.

10. **Bibliography:** Reference [47] (CCSDS 414.0-G-2) is cited in Table VII but does not appear in the bibliography. Reference [1] cites a non-archival source (Jonathan's Space Report) alongside an FCC filing—separate these.

11. **Abstract:** At 280 words, the abstract exceeds IEEE T-AES guidelines (typically 200 words). Trim by removing parameter-specific numbers that appear in the body.

12. **Eq. 5 ($\eta_{\text{consensus}}$):** The formula uses $R$ for Raft rounds, conflicting with $R$ for spatial reuse factor in Table I. Use a distinct symbol.

---

## Overall Recommendation
**Recommendation: Major Revision**

This paper makes a useful contribution by assembling a systematic sizing framework for hierarchical coordination in large spacecraft swarms. The two-layer feasibility decomposition (byte budget + TDMA airtime), the campaign duty factor parameterization, and the CCSDS-grounded $\gamma$ derivation are the strongest elements. The paper is commendably transparent about its validation limitations (Table XII) and provides excellent reproducibility infrastructure.

However, the paper has significant weaknesses that prevent acceptance in its current form. The complete absence of external validation (Tier 3) is the most serious concern for a paper positioning itself as providing practitioner-facing "design equations." The DES verification, while now properly labeled as internal consistency, still receives disproportionate emphasis relative to its evidential value. The 30 kbps design-point recommendation with only 2.9% residual margin is inconsistent with the paper's own sensitivity analysis showing 35 kbps under conservative assumptions. The GE channel model, while appropriately framed as a sensitivity study in the body, is presented with unjustified specificity in the abstract.

The paper's length (14+ pages of dense material with substantial repetition) works against its goal of providing a clear, usable framework. A more focused presentation—consolidating redundant tables, reducing DES-analytical agreement discussion, and elevating the sensitivity sweeps over single-point results—would significantly improve impact.

## Constructive Suggestions

1. **Elevate the 35 kbps conservative design point** over the 30 kbps theoretical minimum. A sizing framework should recommend designs with adequate margin, not minimum-feasibility points.

2. **Implement a single-cluster NS-3 simulation** (even simplified) to provide one Tier 3 validation point. This would dramatically strengthen the paper's credibility for the modest effort involved.

3. **Consolidate the presentation** by merging Tables V, VIII, and X into a single comprehensive feasibility table; reducing DES-analytical agreement to one sentence; and moving the sectorized mesh and global-state mesh details to an appendix.

4. **Present the GE sensitivity sweep as the primary result** (Fig. 10b), with the $p_{BG} = 0.50$ case as one illustrative point rather than the headline finding.

5. **Add a worked example** walking through Algorithm 1 with a non-default parameter set (e.g., $k_c = 50$, 50 kbps, rate-1/2 LDPC) to demonstrate the framework's generality.

6. **Strengthen the distributed consensus treatment** by presenting centralized and distributed overhead side-by-side in a single comparison table, making the architecture-dependence of $\eta_{\text{cmd}}$ immediately visible.

7. **Address the common-cause failure concern** more prominently: the RF-backup scenario is motivated by events (solar storms) that are precisely the common-cause failures that invalidate the independence assumption in the compound probability calculation.