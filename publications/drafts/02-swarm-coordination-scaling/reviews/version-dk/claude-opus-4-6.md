---
paper: "02-swarm-coordination-scaling"
version: "dk"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-03-06"
recommendation: "Unknown"
---



# Peer Review: "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version DK)

---

## 1. Significance & Novelty
**Rating: 3 (Adequate)**

The paper addresses a genuine gap: no prior work provides closed-form parametric sizing relationships for hierarchical coordination architectures at the $10^3$–$10^5$ node scale with byte-level traffic accounting. The two-test feasibility framework (byte budget + TDMA airtime) is a useful conceptual contribution, and the campaign duty factor $d$ is a pragmatic parameterization that maps well to operational realities. However, the novelty is primarily in the *assembly* of well-known techniques (TDMA slot efficiency, GE channel models, M/D/1 queueing, AoI) rather than in fundamental methodological advances. The equations themselves—Eqs. (1)–(11)—are straightforward applications of standard communication engineering. The paper is best characterized as a systems engineering sizing study rather than a research contribution advancing the state of the art in any one constituent discipline.

## 2. Methodological Soundness
**Rating: 3 (Adequate)**

The three-layer feasibility framework (byte budget, MAC efficiency, TDMA airtime) is logically structured and internally consistent. The decomposition into Test A and Test B is clean, and Algorithm 1 provides a usable synthesis. However, several methodological concerns persist:

- The DES is cycle-aggregated and message-layer only; it cannot capture the phenomena (MAC contention, link-layer dynamics, Doppler) that would most challenge the analytical results. The DES essentially re-implements the closed-form equations with stochastic sampling, which limits its independent verification value.
- The GE channel model is acknowledged as a "what-if design tool," which is appropriate, but the default parameterization ($p_{BG} = 0.50$, $p_B = 0.90$) lacks empirical grounding for ISL channels. The geometric justification (1 m panel, 2°/s tumble) is illustrative but not validated.
- The slot-level simulator shares the same $\gamma$ formula as the analytical model; its confirmation of analytical results is therefore largely tautological for mean values. The ARQ×TDMA coupling result (52.7% misses at 24 kbps) is the one genuinely non-trivial finding from the slot-sim.

## 3. Validity & Logic
**Rating: 4 (Good)**

The internal logic is generally sound and self-consistent. Specific improvements over what appear to be earlier versions:

- The campaign duty factor $d$ now adequately addresses workload realism. The mapping from mission phases to $(d, q)$ pairs (Table in §IV-E) is well-constructed, and the yearly mixture calculation ($\bar{\eta} = 5.6\%$) properly contextualizes the 46% stress bound as a continuous-duty upper bound occurring <1% of operational time. This is a significant improvement.
- The gamma unification around $\gamma \approx 0.73$–$0.76$ (Model C, CCSDS-derived) is consistently applied throughout. The earlier 0.85 value appears to have been replaced, and the consistency ledger in Table VII is a welcome addition. I verified spot-checks of $\gamma_{30} = 0.745$ against Eq. (7) and they are consistent.
- The stress-case $\eta_S \approx 46\%$ is now properly framed as a continuous-duty upper bound with explicit temporal context.

One logical concern: the paper claims $\alpha_{RX}$ is a "computed output, not a free parameter" (Table I, Algorithm 1 line 6), yet it appears in the design heuristic Eq. (10) as if it were known *a priori*. The circularity is acknowledged in the sizing walkthrough but could confuse practitioners. The iterative nature of the procedure (line 8: "increase $R_{PHY}$; repeat") should be more prominently flagged.

## 4. Clarity & Structure
**Rating: 3 (Adequate)**

The paper is extremely dense—arguably too dense for a journal article. The sheer volume of inline qualifications, footnotes, cross-references, and parenthetical caveats makes it difficult to follow the main argument. Specific issues:

- The Introduction front-loads notation (Table I) and model selection (Model C vs. Model S) before the reader has context for why these matter. The "slot-timing model" paragraph before §I-A is jarring.
- Section IV is 8+ pages covering coordinator sizing, AoI, GE losses, joint interactions, workload profiles, DES tails, topology comparison, parameter sensitivity, and packet-level validation—each deserving focused treatment. The result is that important findings (e.g., 35 kbps recommendation, ARQ infeasibility at 30 kbps) compete for attention with secondary details.
- Many tables serve dual purposes (parameter specification + results + footnoted caveats), making them hard to parse. Table III (Simulation Parameters) has four footnotes totaling ~150 words.
- The paper would benefit significantly from a clear "main result" figure or table early in Section IV that summarizes the key design recommendations, with subsequent subsections providing supporting analysis.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**

The paper is exemplary in its transparency: all code, data, and simulators are publicly available with a tagged release. The AI disclosure is specific (tools named, scope of use delineated). The validation gap is explicitly acknowledged in multiple locations (abstract, §III-A, §V-A, §V-B, conclusion). The claim map (Table IX) is an unusually honest and useful artifact. The paper does not overclaim.

## 6. Scope & Referencing
**Rating: 3 (Adequate)**

The reference list (58 items) covers the major relevant areas but has notable gaps:

- No references to actual ISL measurement campaigns or channel characterization studies beyond the terrestrial-mobile Lutz et al. [55] and ITU-R P.681 [56]. The ISL channel is fundamentally different from land-mobile satellite channels.
- The TDMA/MAC literature for satellite networks is underrepresented. Beyond DVB-RCS2, there is substantial work on demand-assigned TDMA in satellite systems (e.g., Maral & Bousquet's satellite communications textbook, ETSI S-MIM standards).
- Network calculus [57] is cited but not used; the deterministic worst-case bounds it provides would be a natural complement to the mean-value analysis.
- The AoI literature citations are appropriate but the connection to scheduling-for-AoI (Kadota et al. [48]) could be developed further.
- Several references are non-archival (Amazon Kuiper overview, DARPA program pages) and should be flagged as such per IEEE style.

---

## Major Issues

**1. The DES provides limited independent verification value.**
- *Issue:* The DES reproduces analytical means to <0.1% (acknowledged as "Tier 1: confirms implementation, not model"). The distributional tails (Fig. 4) under campaign burstiness are the DES's claimed incremental contribution, but these are conditional on assumed burst models (ON/OFF Markov) that are themselves unvalidated. The buffer factor $M = 1.30$ is a prediction under these assumptions, not a validated finding.
- *Why it matters:* The paper devotes significant space to DES results that are essentially self-confirming. A reader might reasonably ask what the DES adds beyond a more expensive way to compute the same quantities.
- *Remedy:* Either (a) explicitly reduce the DES's role to "implementation verification + illustrative distributional exploration under assumed burst models," removing any implication of independent validation; or (b) introduce genuinely independent verification (e.g., NS-3 MAC simulation for at least one configuration). The former is more honest given current capabilities; the latter would substantially strengthen the paper.

**2. The packet-level validation (§IV-J) does not provide adequate independent validation.**
- *Issue:* Section IV-J derives $\gamma$ from CCSDS Proximity-1 framing parameters. This is a standards-based *parameter estimate*, not a measurement or independent validation. The same formula (Eq. 7) is used in the analytical model, the slot-sim, and the packet-level derivation. The paper acknowledges this ("not independent validation") but the section title and placement suggest otherwise.
- *Why it matters:* The $\gamma$ value is the single most consequential parameter in the feasibility framework—it determines whether 24, 30, or 35 kbps is required. Anchoring it to CCSDS standards is reasonable for preliminary design, but the paper should not present this as "validation."
- *Remedy:* Rename the section to "Standards-Based Slot Efficiency Estimation" (which it effectively already is in the text). More importantly, provide a quantitative uncertainty analysis: what is the distribution of $\gamma$ across real CCSDS Proximity-1 implementations? The sensitivity analysis ($\gamma = 0.745 \pm 0.07$) is a start but lacks empirical grounding.

**3. Absence of any external validation limits the paper's contribution to "preliminary design framework."**
- *Issue:* Table IX (Claim Map) shows no Tier 3 entries. All verification is internal (analytical ↔ DES ↔ slot-sim, all sharing the same equations). The paper repeatedly acknowledges this, but it fundamentally limits what can be claimed.
- *Why it matters:* For IEEE T-AES, readers expect at least partial validation against independent tools (NS-3, STK) or measurements. The paper's value proposition—sizing equations for practitioners—is undermined if the equations have never been checked against reality.
- *Remedy:* At minimum, validate one key result against an independent tool. For example: (a) run the TDMA superframe in NS-3 with CCSDS-like framing to verify $\gamma$ and deadline miss rates; (b) compare the GE recovery statistics against published ISL measurement data (even from optical ISL campaigns, with appropriate caveats); (c) validate the spatial reuse assumption ($R = 7$) against STK RF interference analysis for one representative constellation shell. Any one of these would move a result to Tier 3 and substantially strengthen the paper.

**4. The generalized $\gamma$ expression (Eq. 7) needs clearer practitioner guidance on its domain of validity.**
- *Issue:* Eq. (7) is presented as a general formula, but it assumes: single-packet-per-slot TDMA, cold-start acquisition per slot, LDPC FEC applied to the entire frame (payload + framing), and specific CCSDS Proximity-1 framing. These assumptions are not always stated when the equation is invoked.
- *Why it matters:* Practitioners using Algorithm 1 with different framing standards (e.g., CCSDS TC, AOS, or proprietary) need to know which terms to modify. The $T_{\text{framing}}$ term in particular—where framing bits are FEC-encoded per "CCSDS standard practice"—is non-obvious and could lead to errors if applied to systems where framing is outside the FEC codeword.
- *Remedy:* Add a brief "applicability conditions" paragraph to §V-D listing the assumptions under which Eq. (7) is valid, and indicate which terms change under alternative framing. The measurement protocol is a good start but focuses on timing parameters rather than structural assumptions.

**5. The coordinator failure transient analysis is incomplete.**
- *Issue:* The thundering-herd analysis (Slotted ALOHA/BEB, 140–160 s election) is interesting but assumes all $k_c = 100$ nodes simultaneously attempt Raft elections over the shared RF channel. The interaction between election traffic and ongoing status reporting is not analyzed. During the 140–160 s election period, 14–16 cycles of status reports are also competing for the channel.
- *Why it matters:* The claim that "gaps < 1/yr per cluster" depends on the election completing before the next coordinator failure, but the election duration (140–160 s) is comparable to the RF-backup suspension period (~160 s). If status traffic contends with election traffic, the election may take longer.
- *Remedy:* Either (a) analyze the joint election + status traffic load during the transient, or (b) specify that status reporting is suspended during elections (and quantify the AoI impact), or (c) acknowledge this as an unanalyzed interaction.

---

## Minor Issues

1. **Eq. (3) notation:** $M_{\text{total}}$ counts messages but the overhead metric $\eta$ is in bits/s. The connection between message count and bandwidth utilization should be made explicit.

2. **Table II, Panel A:** "Coord. bottleneck? Yes (20 kbps)" at 1 kbps—the 20 kbps figure refers to $C_{\text{coord,info}}$, not $C_{\text{node}}$. This could confuse readers scanning the table.

3. **§III-B.2, coordinator summary breakdown:** The 371 B metadata/CRC allocation (including 256 B authentication and 23 B padding) seems large relative to the 141 B of actual content. Is HMAC-SHA256 assumed? This should be stated.

4. **Eq. (6), AoI:** The ceiling function produces a step function; the DES result (441 s) vs. analytical (440 s) difference is just the ceiling vs. continuous approximation. This is not meaningful verification.

5. **Fig. 2 (cross-cycle recovery):** The figure is referenced but not shown in the manuscript text. Ensure the PDF includes all figures.

6. **§IV-A, "Phase-staggered scheduling":** The claim "DES confirms zero drops at ≥25 kbps vs. 50 kbps under random phase" appears without supporting data or figure. Either provide evidence or remove the specific numbers.

7. **Table VI (Superframe):** The total (9,270 ms) doesn't include the ACK mini-slots (50 ms per footnote a). The "unallocated margin" should be 680 ms, not 730 ms, under the conservative ACK assumption. This inconsistency appears in multiple places.

8. **§IV-E, "Yearly mixture":** The weights (0.95, 0.049, 0.001) sum to 1.0 but the mapping to mission phases is not explicit. Which phases correspond to which weights?

9. **Abstract:** "CCSDS Proximity-1 framing yields $\gamma \approx 0.73$–$0.76$ across 24–35 kbps" — the range is inverted (higher $\gamma$ at lower rate because fixed overhead is a smaller fraction... wait, no: fixed *time* overhead is a larger fraction at lower rates, so $\gamma$ decreases with decreasing rate). Actually, $\gamma_{24} = 0.761 > \gamma_{35} = 0.732$. This is counterintuitive and should be briefly explained: at lower PHY rates, the payload transmission time increases more than the fixed overheads, so $\gamma$ actually *increases*. This deserves a sentence of explanation.

10. **Reference [3] (Kuiper):** Non-archival corporate webpage; consider replacing with an FCC filing or peer-reviewed source.

11. **§I, "Model C (primary)":** Stating the primary model before the reader knows what models exist or why they matter is confusing. Move this to after the model derivation.

12. **Algorithm 1, line 11:** "$M_r \cdot T_{\text{slot}}$" allocates $M_r$ full slots for ARQ. In practice, only failed nodes need retransmission. The expected ARQ demand is $E[\text{failed}] \times T_{\text{slot}}$, which is much less than $M_r \times T_{\text{slot}}$ for small $M_r$. Clarify whether $M_r$ is per-node or total retransmission slots.

---

## Overall Recommendation
**Recommendation: Major Revision**

This manuscript presents a well-structured preliminary design framework for sizing hierarchical coordination architectures in large autonomous space swarms. Its principal strengths are: (1) the clean two-test feasibility decomposition (byte budget + TDMA airtime); (2) the campaign duty factor $d$ as a practical parameterization of episodic workloads; (3) exceptional transparency regarding validation limitations, with the claim map (Table IX) setting a high standard for intellectual honesty; and (4) full code/data availability.

However, the paper suffers from three fundamental limitations that prevent acceptance in its current form. First, the complete absence of external validation (Tier 3) means all results are self-confirming—the DES, slot-sim, and analytical model share the same equations, so their agreement is by construction. For a journal of IEEE T-AES's caliber, at least one key result should be validated against an independent tool (NS-3, STK, or hardware measurement). Second, the paper is excessively dense, attempting to cover coordinator sizing, AoI, GE channel modeling, ARQ×TDMA coupling, workload profiling, distributional analysis, topology comparison, and packet-level parameterization in a single manuscript. The core contribution—the two-test framework with Algorithm 1—is obscured by secondary analyses. Third, the generalized $\gamma$ expression, while useful, needs clearer domain-of-validity specification and empirical grounding beyond standards-document parameter extraction.

The most impactful revision would be to obtain even one external validation point (e.g., NS-3 TDMA simulation confirming the deadline miss rates in Table VIII), which would move the paper from "internally consistent preliminary framework" to "validated design tool." Streamlining the presentation to focus on the core sizing framework, with secondary analyses moved to appendices or supplementary material, would also significantly improve readability and impact.

---

## Constructive Suggestions
*(Ordered by impact)*

1. **Add one external validation point.** Even a simplified NS-3 simulation of the TDMA superframe (99 nodes, GE channel, 35 kbps) confirming zero deadline misses would transform the paper's credibility. This is achievable with moderate effort and would move the ARQ×TDMA coupling result to Tier 3.

2. **Restructure Section IV.** Lead with a summary table/figure of key design recommendations (35 kbps, $k_c = 100$–200, $d = 0.10$ default), then provide supporting analysis in focused subsections. Consider moving the GE sensitivity analysis and distributional tail analysis to an appendix.

3. **Sharpen the DES's claimed contribution.** Be explicit that the DES's value is (a) implementation verification and (b) exploratory distributional analysis under assumed burst models. Remove any language suggesting independent validation.

4. **Provide empirical $\gamma$ bounds.** Survey published TDMA slot efficiency measurements from operational satellite systems (DVB-RCS2 terminals, Iridium, etc.) to bound the plausible range of $\gamma$ for ISL applications. Even order-of-magnitude comparison would help.

5. **Add a "Quick-Start" box** early in the paper: "For $k_c = 100$, $S = 256$ B, $T_c = 10$ s: use 35 kbps PHY, expect $\eta \approx 10\%$ routine / 46% stress-bound. See Algorithm 1 for other parameters." This would dramatically improve accessibility.

6. **Clarify the $\alpha_{RX}$ circularity** in Algorithm 1 by adding an explicit iteration loop with convergence criterion, rather than the current "increase $R_{PHY}$; repeat" instruction.

7. **Extend the coordinator failure analysis** to account for joint election + status traffic during the transient period, or explicitly state the simplifying assumption.

8. **Add domain-of-validity conditions** for Eq. (7) to guide practitioners using non-CCSDS framing.