---
paper: "02-swarm-coordination-scaling"
version: "dm"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-03-07"
recommendation: "Unknown"
---

# Peer Review: "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version DM)

---

## 1. Significance & Novelty
**Rating: 3 (Adequate)**

The paper addresses a genuine gap: closed-form per-cluster sizing equations for hierarchical coordination at scales beyond current constellation practice. The two-test feasibility framework (byte budget + TDMA airtime) is a useful conceptual contribution, and the campaign duty factor $d$ is a sensible parameterization. However, the novelty is incremental rather than transformative. The core analytical content is essentially TDMA slot accounting applied to a specific (reasonable) message model—standard systems engineering rather than new theory. The LEACH-style hierarchy is well-established; the contribution is in the specific parameterization for space ISL, not in architectural innovation. The paper would benefit from a clearer articulation of what a practitioner can do with these equations that they could not do before with standard link budget and TDMA sizing tools.

## 2. Methodological Soundness
**Rating: 3 (Adequate)**

The analytical framework is internally consistent and the decomposition into Test A and Test B is clean. Several methodological concerns remain:

- The DES (Tier 1) verification is acknowledged as confirming its own equations, which is appropriate transparency. However, the paper leans heavily on this for validation language despite the acknowledged circularity.
- The NS-3 validation (Tier 3) is the strongest methodological element, but critical details raise concerns (see Major Issues).
- The GE channel model is appropriately framed as a "what-if tool," which is an improvement over treating it as a validated channel model. However, the default parameters ($p_B = 0.90$, $p_{BG} = 0.50$) are drawn from land-mobile satellite literature (Lutz et al.), and the paper acknowledges ISL conditions would differ substantially. This weakens the quantitative GE results even as design illustrations.
- The slot-level simulator (Tier 2) provides useful ARQ×TDMA coupling results but its independence from the analytical model is unclear.

## 3. Validity & Logic
**Rating: 4 (Good)**

The logical structure is generally sound. The two-test framework is well-motivated, and the paper is careful to distinguish between information-layer and physical-layer constraints. Specific strengths:

- The campaign duty factor $d$ adequately addresses workload realism. The stress case ($\eta_S \sim 46\%$) is now properly contextualized as a continuous-duty upper bound occurring "<1% of operational time," with concrete mission-phase examples (station-keeping, collision avoidance).
- The $\gamma$ unification around 0.73–0.76 via CCSDS Proximity-1 framing is consistently applied; Model C is clearly designated as the primary model, and Model S appears only for comparison. This is a clear improvement.
- The three-layer framework (byte budget, MAC efficiency, TDMA airtime) is logically coherent, and the paper correctly notes that $C_{\text{raw}} = C_{\text{coord,info}}/\gamma$ is a unit conversion within Test B, not a separate test.

One logical gap: the 1% deadline miss threshold is derived from an AoI argument (conjunction screening within 24 h), but the connection between a 10-second cycle miss and 24-hour conjunction screening timelines spans three orders of magnitude and deserves more rigorous justification.

## 4. Clarity & Structure
**Rating: 4 (Good)**

The paper is well-organized with clear notation (Table I), a useful rate ladder (Table IV), and Algorithm 1 providing a practical synthesis. The writing is generally precise. The explicit labeling of Model C as primary and Model S as comparison-only eliminates earlier confusion. Tables are informative and well-formatted.

Areas for improvement: the paper is dense, and the relationship between the many tables could be streamlined. Some readers may struggle to distinguish which results are analytical, which are DES, which are slot-sim, and which are NS-3 without careful reading.

## 5. Ethical Compliance
**Rating: 4 (Good)**

The AI disclosure is specific and appropriate (tools named, scope of use delineated). Data availability is excellent with a tagged GitHub repository. The NS-3 scenarios being included in supplementary material is valuable for reproducibility. The "TODO" comments in the LaTeX source (lines related to NS-3 figures and slot structure values) raise a concern about manuscript completeness—see Major Issues.

## 6. Scope & Referencing
**Rating: 3 (Adequate)**

The reference list covers the key areas (CCSDS standards, DVB-RCS2, swarm robotics, DTN, AoI) but has notable gaps. Missing: recent work on distributed satellite autonomy beyond NASA DSA (e.g., ESA OPS-SAT experiments), CCSDS SPP framing analysis, and the broader TDMA scheduling literature (e.g., Ramanathan & Lloyd's unified framework). The DVB-RCS2 cross-comparison in the Discussion is a welcome addition. The paper would benefit from engaging more deeply with the network calculus literature it cites—Le Boudec & Thiran could provide deterministic worst-case bounds that complement the mean-value approach.

---

## Major Issues

**1. NS-3 Validation Completeness and Credibility**

The NS-3 validation section (IV-B) contains two `% TODO` comments in the LaTeX source indicating that figures and table values have not yet been generated from actual simulation runs. The text reads as if results exist ("Fig. 4(a) compares..."), but the TODO comments suggest these may be projected rather than measured values. This is the single most critical issue in the manuscript.

*Why it matters:* The NS-3 validation is presented as the paper's primary independent validation. If the results are placeholders, the paper's central validation claim is unsupported.

*Remedy:* Complete the NS-3 simulations and report actual measured values. If the simulations have been run but the TODOs are vestigial, remove them and confirm in a cover letter that all reported NS-3 values are from actual simulation runs.

**2. The 3–8% Discrepancy Needs Decomposition**

The paper states that NS-3 $\gamma$ values are "systematically 3–8% lower" than analytical predictions and attributes this to "queuing delays, stochastic acquisition jitter, discrete bit-error realizations." This is hand-waving. A systematic bias suggests a structural difference, not random effects.

*Why it matters:* The 16-bit framing difference (88 vs. 104 bits) is acknowledged but its quantitative contribution to the 3–8% gap is not isolated. Without decomposition, the reader cannot assess whether the discrepancy validates the model or reveals an error.

*Remedy:* Decompose the discrepancy: (a) compute the $\gamma$ difference attributable solely to the 88-bit vs. 104-bit framing difference; (b) run NS-3 with fixed (non-stochastic) acquisition to isolate jitter contribution; (c) report residual unexplained discrepancy. This decomposition would substantially strengthen the validation claim.

**3. Spatial Reuse Factor $R = 7$ is Unvalidated**

The fleet-level channel reuse equation (Eq. 14) uses $R = 7$, acknowledged as "provisional pending RF simulation." This parameter directly determines whether fleet-level TDMA is non-binding, which is a key claim.

*Why it matters:* If $R < 4$ (plausible in dense orbital shells with omnidirectional S-band antennas), the fleet-level constraint becomes binding and the per-cluster analysis is insufficient.

*Remedy:* Either (a) provide a sensitivity analysis showing the $R$ value at which fleet-level TDMA becomes binding, or (b) remove the "non-binding" claim and present Eq. 14 purely as a framework awaiting parameterization.

**4. AoI Threshold Justification is Weak**

The 1% deadline miss threshold is justified by: "conjunction screening within 24 h requires status AoI $P_{99} < 500$ s." The logical chain from 24-hour conjunction timelines to 500-second AoI to 1% per-cycle miss rate involves several unstated assumptions.

*Why it matters:* The feasibility boundary (30 kbps infeasible, 35 kbps feasible) depends directly on this threshold. A 5% threshold would change the recommendation.

*Remedy:* Provide a rigorous derivation of the 500 s AoI requirement from conjunction screening operations, or present the 1% threshold as a design choice with sensitivity analysis showing how the PHY rate recommendation changes at 0.1%, 1%, 5%, and 10% thresholds.

**5. DES Verification Value is Overstated**

The paper correctly acknowledges that the DES "confirms implementation, not model" (Tier 1). However, it still occupies significant space in the methodology and is counted as one of three V&V tiers. A tool that confirms its own equations to <0.1% provides no scientific value beyond debugging.

*Why it matters:* Counting DES as a validation tier inflates the apparent rigor of the verification strategy.

*Remedy:* Reduce DES to a single sentence acknowledging implementation verification. Elevate the slot-level simulator and NS-3 as the two meaningful validation tiers, and be explicit that the slot-sim's independence from the analytical model should be characterized (shared assumptions vs. independent implementation).

---

## Minor Issues

1. **Eq. 7 ($\eta_{\text{consensus}}$):** The variable $N_R$ is undefined in the main text. Define it (presumably number of Raft rounds per decision).

2. **Table V (Superframe):** "Re-sync preamble + ACK mini-slots = 54 ms" is not decomposed. Provide the breakdown.

3. **Section II-C:** "Results scale linearly ($\eta \propto 1/C_{\text{node}}$)" — this is inverse proportionality, not linear scaling. Clarify language.

4. **Algorithm 1, Line 11:** The ARQ time budget uses $M_r \cdot T_{\text{slot}}$, but under GE slow fading, retransmissions target the same failed nodes. The slot count should be $\min(M_r \cdot n_{\text{failed}}, \text{margin}/T_{\text{slot}})$, not $M_r \cdot T_{\text{slot}}$.

5. **Table II (Simulation Parameters):** "CA rate = $10^{-4}$ msg/s" — clarify whether this is per-node or fleet-wide.

6. **Eq. 10 (AoI):** The ceiling function assumes geometric reporting; state this assumption explicitly.

7. **Fig. 1:** Referenced but described only generically. Ensure the figure clearly shows the four levels with fan-out ranges.

8. **Section V, "Falsification conditions":** Condition (iv) states 35 kbps would be "unnecessary" if $\tau_c \ll T_c$ with $p_B < 0.3$. This is not falsification (proving the model wrong) but rather a regime where the design is over-provisioned. Distinguish between falsification and over-design.

9. **Abstract:** "replacing the earlier 0.85" — this refers to a previous version and should not appear in the abstract of a standalone manuscript.

10. **Table III, Panel B:** The column header "30 kbps" appears in the sub-header but the PHY rate context is unclear for the "Rec. PHY" column.

11. **Eq. 6 (Unicast stagger):** The generalized form (Eq. 6a) adds "+1 for coordinator broadcast" but this is not explained—why does the coordinator broadcast to itself?

12. **Reference [13]:** Self-citation to an unpublished technical report on "multi-model AI deliberation." If this is not peer-reviewed, note it as such.

---

## Overall Recommendation
**Recommendation: Major Revision**

This paper makes a useful contribution by providing a structured sizing framework for hierarchical coordination in large space swarms. The two-test decomposition (byte budget + TDMA airtime) is clean and practical, the campaign duty factor $d$ sensibly parameterizes workload variability, and the CCSDS-grounded $\gamma$ values provide credible slot efficiency estimates. The cross-standard comparison with DVB-RCS2 and the explicit falsification conditions demonstrate engineering maturity.

However, the manuscript has a critical completeness issue: the NS-3 validation—presented as the paper's primary independent verification—appears to contain placeholder results (TODO comments in source). This must be resolved before the paper can be accepted. Beyond this, the 3–8% NS-3 discrepancy needs proper decomposition, the spatial reuse factor requires sensitivity analysis, and the AoI-based feasibility threshold needs stronger justification. The DES verification tier should be de-emphasized in favor of the genuinely independent validation elements.

The analytical framework is sound and the paper is well-written. With the NS-3 validation completed and the major issues addressed, this could become a solid reference for preliminary design of swarm coordination architectures. The authors should also consider whether the contribution is better positioned as a systems engineering design tool (which it is) rather than as a research advance in distributed systems theory (which it is not).

## Constructive Suggestions

1. **Complete and verify all NS-3 results.** This is non-negotiable for publication. Remove all TODO comments and confirm that every reported value comes from actual simulation runs. Consider adding a reproducibility appendix with exact NS-3 command lines.

2. **Decompose the NS-3 discrepancy.** Isolate framing, acquisition jitter, and residual contributions. This transforms a weakness into a strength by showing the authors understand their abstraction error budget.

3. **Add a PHY rate sensitivity table for the feasibility threshold.** Show $R_{\text{PHY,min}}$ at miss rate thresholds of 0.1%, 1%, 5%, 10%. This makes the framework more useful to practitioners with different reliability requirements.

4. **Provide spatial reuse sensitivity.** Plot fleet-level cycle time $T_c^{\text{fleet}}$ vs. $R$ for $R \in \{1, 3, 5, 7, 12\}$ at $N = 10^5$. This honestly characterizes the fleet-level uncertainty.

5. **Strengthen the practitioner value proposition.** Add a "How to Use This Paper" paragraph early in the introduction, explicitly stating: "Given your cluster size, message sizes, and PHY rate, Algorithm 1 returns feasibility status and margin in under 1 second." This positions the work correctly as a design tool.

6. **Consider network calculus bounds.** Since Le Boudec & Thiran is already cited, derive a deterministic worst-case bound for the ingress phase using arrival curves and service curves. This would complement the mean-value analysis and appeal to the safety-critical aerospace audience.

7. **Engage with DVB-RCS2 demand assignment.** The current comparison is limited to $\gamma$ ranges. DVB-RCS2's demand-assigned TDMA (DA-TDMA) mechanisms are directly relevant to the exception-reporting mode. Discuss whether DA-TDMA could replace fixed TDMA for the command/alert traffic classes.