---
paper: "02-swarm-coordination-scaling"
version: "dp"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-03-07"
recommendation: "Unknown"
---



# Peer Review: Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms

**Manuscript Version:** DP
**Target Journal:** IEEE Transactions on Aerospace and Electronic Systems

---

## 1. Significance & Novelty
**Rating: 3 (Adequate)**

The paper addresses a genuine gap: closed-form sizing equations for hierarchical coordination in large autonomous spacecraft swarms with byte-level traffic accounting. The two-test feasibility framework (byte budget + TDMA schedulability) is a useful conceptual contribution, and the campaign duty factor is a practical parameterization. However, the novelty is somewhat constrained by the fact that the individual components (TDMA scheduling, CCSDS framing, GE channel models, LEACH-style clustering) are well-established. The contribution is primarily in their systematic integration and the derivation of sizing relationships—valuable for practitioners but incremental from a research perspective. The paper would benefit from a clearer articulation of what design decisions this framework enables that were previously impossible or impractical.

## 2. Methodological Soundness
**Rating: 3 (Adequate)**

The analytical framework is internally consistent and the equations are correctly derived within their stated assumptions. The three-layer decomposition (byte budget, MAC efficiency, TDMA airtime) is logically sound. However, several methodological concerns arise:

- The DES verification is acknowledged as a "sanity check" that reproduces analytical means to <0.1%—this is expected since both implement the same equations. Its value is minimal beyond confirming implementation correctness.
- The NS-3 validation is a genuine improvement and provides independent code verification. However, the NS-3 scenario itself uses significant idealizations (star topology, no Doppler, event-scheduled TDMA) that limit how much independent validation it truly provides. It validates MAC-level arithmetic against a different codebase, which is useful but not a substitute for physical-layer or system-level validation.
- The GE channel model is appropriately framed as a "what-if tool," but the default parameters are drawn from land-mobile satellite channels (Lutz et al.), which have limited applicability to ISL scenarios. The paper acknowledges this but could be more explicit about the implications.

## 3. Validity & Logic
**Rating: 4 (Good)**

The logical structure is generally sound. The two-test framework is clearly defined, and the paper is careful to distinguish between independent constraints (Tests A and B) and derived quantities within Test B. Several specific improvements are evident in this version:

- The campaign duty factor $d$ is well-motivated with concrete mission-phase mappings (Table IV), and the "<1% of operational time" claim for the stress case is now substantiated with the $d_{\text{SK}} + d_{\text{CA}} < 0.06$ calculation.
- The $\gamma$ values are consistently computed via CCSDS Proximity-1 framing (Model C) throughout, with Model S appearing only for comparison. This is a clear improvement.
- The stress-case ($\eta_S \sim 46\%$) is properly contextualized as a continuous-duty upper bound.
- The alternative slot structures (Table IX) effectively demonstrate that the 35 kbps recommendation is not an artifact of the cold-start assumption.

One logical concern remains: the feasibility threshold $\epsilon = 1\%$ is justified via AoI tail bounds assuming independent per-cycle delivery, but the GE channel introduces positive correlation. The paper acknowledges this but the interaction between the $\epsilon$ threshold and GE correlation deserves more rigorous treatment.

## 4. Clarity & Structure
**Rating: 4 (Good)**

The paper is well-organized and the notation table (Table I) is helpful. The rate ladder (Table VI) effectively traces the computation from information rate to PHY recommendation. Algorithm 1 provides a clear synthesis. The distinction between Tests A and B is clearly maintained throughout. The figures are appropriately referenced, though I cannot evaluate their visual quality from the LaTeX source alone.

Minor clarity issues: the abstract is dense and could be more accessible; the paper occasionally oscillates between presenting general equations and specific numeric instantiations in ways that may confuse readers about what is a general result versus a parameter-specific outcome.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**

The data availability statement is exemplary, with a specific GitHub repository, version tag, and software environment specified. The AI disclosure is transparent and appropriately scoped. Reproducibility appears strong given the provided code, parameters, and methodology.

## 6. Scope & Referencing
**Rating: 3 (Adequate)**

The references cover the relevant domains (CCSDS standards, swarm robotics, constellation management, DTN, queueing theory). However, several gaps exist:

- No reference to the substantial body of work on TDMA scheduling optimization for satellite networks (e.g., Pratt & Bostian, Maral & Bousquet).
- Limited engagement with the network calculus literature beyond a single citation, despite claiming complementarity.
- No discussion of ESA's OPS-SAT or similar onboard autonomy demonstrations that are more directly relevant than the NASA DSA reference.
- The DVB-RCS2 comparison in the Discussion is valuable but could be expanded with more quantitative cross-referencing.

---

## Major Issues

**1. The DES provides negligible independent validation value.**
- *Issue:* The cycle-aggregated DES reproduces analytical means to <0.1%, which is expected since both implement identical message-counting logic. Calling this "verification" overstates its contribution.
- *Why it matters:* Readers may interpret this as independent confirmation of the model's correctness, when it only confirms implementation fidelity of the same equations.
- *Remedy:* Either (a) remove the DES results from the main text entirely and relegate to supplement as an implementation check, or (b) use the DES to explore scenarios the closed-form equations cannot capture (e.g., correlated failures, dynamic cluster membership, bursty traffic patterns). The slot-level simulator and NS-3 validation are far more valuable; emphasize those.

**2. The NS-3 validation, while valuable, validates a narrow slice of the model.**
- *Issue:* The NS-3 scenario validates MAC-level timing arithmetic for a single cluster under idealized conditions. It does not validate the byte-budget model (Test A), the fleet-level reuse model, the GE channel interaction with ARQ, or any multi-cluster dynamics.
- *Why it matters:* The paper's claims span per-cluster sizing through fleet-level scaling, but validation covers only single-cluster TDMA timing.
- *Remedy:* (a) Explicitly scope the validation claims: "NS-3 validates the TDMA timing model (Test B) for a single cluster; Test A is validated by construction (arithmetic); fleet-level claims remain unvalidated." (b) Consider adding a multi-cluster NS-3 scenario, even at small scale, to probe spatial reuse assumptions.

**3. The generalized $\gamma$ expression (Eq. 6) needs clearer practitioner guidance.**
- *Issue:* While the $\gamma$ lookup table (Table V) is useful, the generalized expression requires practitioners to know $T_{\text{acq}}$, $T_{\text{guard}}$, $O_{\text{frame}}$, and $R_{\text{FEC}}$—parameters that may not be available at the preliminary design stage when this tool would be most valuable.
- *Why it matters:* The paper positions itself as providing "design equations" for practitioners, but the key equation requires detailed knowledge of the physical layer.
- *Remedy:* Provide a simplified bounding expression: e.g., $\gamma \in [0.65, 0.85]$ with guidance on which end to use based on technology maturity. The quick-check formula in §III-B is a good start; elevate it and provide clearer guidance on when the full expression is needed versus the lookup table.

**4. Fleet-level scaling claims are insufficiently supported.**
- *Issue:* The paper repeatedly states results are "per-cluster" and that fleet-level scaling is "conditional on spatial reuse validation ($R \geq 3$)." However, Eq. 11 and Table VII present fleet-level results as if they are established, and the abstract mentions fleet-level scaling without adequate caveats.
- *Why it matters:* The jump from per-cluster to fleet-level is the most uncertain part of the analysis, involving RF propagation, orbital geometry, and interference modeling that are entirely absent.
- *Remedy:* (a) Remove or heavily caveat fleet-level numeric results in the abstract. (b) Present Eq. 11 and Table VII explicitly as "conditional projections" rather than results. (c) Consider whether the fleet-level material belongs in a separate future-work paper.

**5. The GE channel parameters lack ISL-specific justification.**
- *Issue:* Default GE parameters are from Lutz et al. (land-mobile satellite, urban, 40° elevation). ISL channels have fundamentally different characteristics: no multipath from terrain, different shadowing mechanisms (structural self-shadowing, solar panel occlusion), and different coherence times.
- *Why it matters:* The ARQ analysis, recovery time estimates, and the slow-vs-fast fading regime distinction all depend on these parameters. Using land-mobile parameters for ISL design could be significantly non-conservative or over-conservative in unpredictable ways.
- *Remedy:* (a) State explicitly that no ISL-specific GE parameterization exists in the open literature (if true). (b) Provide sensitivity analysis showing how results change across a wider parameter range that might encompass ISL conditions. (c) The sensitivity curves in Fig. 4 partially address this; reference them more prominently as the primary design tool rather than the specific default values.

---

## Minor Issues

1. **Abstract density:** The abstract packs too many specific numbers ($\gamma_{30} = 0.745$, $\gamma_{35} = 0.732$, 3–8%, 1.8%, 1.5–4.2%, <1%) that are difficult to parse without context. Consider a more narrative abstract with key takeaways, reserving specific values for the body.

2. **Eq. 1 ($M_{\text{total}}$):** The third term assumes a single ground station or top-level coordinator. State this assumption explicitly.

3. **Table II, Panel A:** The "Coord. bottleneck?" row answers "Yes (20 kbps)" at 1 kbps but the meaning is ambiguous—is 20 kbps the bottleneck rate or the required rate? Clarify.

4. **Section II-D:** "Runtime: ~7 s at $N = 10^5$" — specify whether this is per replication or total (30 replications).

5. **Eq. 8 (AoI):** The geometric assumption (independent per-cycle reporting) contradicts the GE channel's correlated losses. Add a caveat or derive the correlated version.

6. **Table VIII:** "GE exc." column header is unexplained. Define in the table note.

7. **Algorithm 1, Line 11:** The P95 computation assumes Binomial distribution, but under GE correlation, the number of failed members is not Binomial. This should be noted.

8. **Section III-A:** The $\epsilon$ sensitivity discussion mentions specific kbps values (30, 28 kbps) without showing the derivation. Either show the calculation or reference a supplement section.

9. **Falsification condition (ii):** "COTS S-band radios range 2–50 ms" needs a citation.

10. **Reference [13] (dyson_multimodel):** A non-peer-reviewed self-citation used to support the AI disclosure. This is acceptable for transparency but should not be counted as a technical reference.

11. **Eq. 9 ($\eta_{\text{consensus}}$):** The factor $\lfloor k_c/2 \rfloor + 1$ is the Raft majority quorum, but the equation multiplies by $N_R$ rounds. Clarify whether $N_R$ includes the initial proposal or only replication rounds.

12. **Table IX:** The "Margin@35" column uses different units than the margin in Table VII (percentage vs. milliseconds). Standardize or clarify.

13. **"Model C" vs. "Model S" terminology** appears without prior definition in the abstract. Define on first use or remove from abstract.

---

## Overall Recommendation
**Recommendation: Major Revision**

This manuscript presents a systematic and well-structured approach to parametric sizing of hierarchical coordination architectures for large spacecraft swarms. The two-test feasibility framework is a useful conceptual contribution, and the campaign duty factor elegantly parameterizes episodic workloads. The CCSDS-grounded $\gamma$ computation, the alternative slot structure analysis, and the NS-3 validation represent genuine technical content. The paper is generally well-written, with clear notation and a logical progression from model to results.

However, several substantive issues require attention before publication. The validation strategy, while improved by the NS-3 addition, remains narrow: it confirms MAC-level timing arithmetic for a single idealized cluster but does not validate the byte-budget model, fleet-level scaling, or channel model interactions. The DES adds negligible independent value. The GE channel parameters lack ISL-specific grounding, and the fleet-level scaling claims are insufficiently supported for the prominence they receive. The generalized $\gamma$ expression, while correct, needs better practitioner packaging to fulfill the paper's stated design-tool ambition.

The most impactful revisions would be: (1) honestly scoping the validation claims to match what is actually validated; (2) either removing fleet-level results or clearly marking them as conditional projections; (3) strengthening the ISL channel model justification or reframing the GE analysis purely as a sensitivity tool; and (4) enhancing the practitioner utility of the $\gamma$ framework with clearer guidance for preliminary design stages.

---

## Constructive Suggestions
*(Ordered by impact)*

1. **Restructure validation narrative.** Lead with what is validated (single-cluster TDMA timing via independent NS-3 codebase), explicitly state what is not (fleet-level, channel model, byte budget beyond arithmetic), and present a credible roadmap for closing the gaps. This honesty will strengthen rather than weaken the paper.

2. **Elevate the $\gamma$ lookup table and quick-check formula.** These are the most practitioner-useful contributions. Consider making Table V a central figure, adding interpolation guidance, and providing a one-page "sizing recipe" (possibly as a supplement) that a systems engineer could use without reading the full paper.

3. **Add a multi-cluster NS-3 scenario** (even 3–5 clusters with shared spectrum) to provide at least preliminary validation of the spatial reuse model. This would substantially strengthen the fleet-level claims.

4. **Derive or bound the correlated-loss AoI.** The GE channel makes per-cycle independence invalid. A Markov-chain AoI analysis under GE would be a genuine analytical contribution and would strengthen the paper's theoretical depth.

5. **Provide a "design space map"** showing feasible/infeasible regions in the $(k_c, R_{\text{PHY}}, d)$ space. This would be more useful than individual parameter sweeps and would visually synthesize the paper's key results.

6. **Consider splitting the paper.** The per-cluster sizing (Tests A and B, Algorithm 1, NS-3 validation) is a complete, well-supported contribution. The fleet-level scaling, GE sensitivity analysis, and consensus overhead could form a companion paper with appropriate additional validation.